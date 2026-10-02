#!/usr/bin/env python3
"""
weather-nowcast prospective collector (panel 2026-09-24.cw-weather-nowcast-v0)

GET-only, unauthenticated, public endpoints only. No orders, no portfolio routes, no Kalshi auth.
Never fills / interpolates / backfills. Every failed, 429'd or stale poll becomes a gap row.
Every stored record carries received_at_utc (box clock at receipt) and the source's own fields untouched
(raw JSON bodies are stored verbatim, zlib-compressed, alongside extracted index columns).

Streams:
  kalshi_events      GET /events?series_ticker=S&status=open&with_nested_markets=true   (discovery, ~30 min)
  kalshi_event_meta  GET /events/{event_ticker}?with_nested_markets=true  (per-event; market metadata/status/result, ~15 min open, ~30 min closed; row stored only on change)
  kalshi_orderbook   GET /markets/orderbooks?tickers=A&tickers=B...  (public batch; fallback per-market /markets/{t}/orderbook) (~60 s)
  kalshi_trades      GET /markets/trades?ticker=T&min_ts=...  (~90 s for markets whose orderbook changed since their last trades poll (a fill always
                     changes the book), capped per round; plus a full sweep of all tracked markets ~20 min), dedup trade_id
  nws_obs            GET api.weather.gov/stations/{ST}/observations/latest and /observations?limit=12 (~5 min), dedup (station, timestamp, sha)
  nws_cli / nws_cf6  GET api.weather.gov/products/types/{CLI|CF6}/locations/{LOC} (~30/60 min) + GET /products/{id} for each new product
Config: stations.json (reloaded on SIGHUP, on mtime change (checked every 60 s) and at least daily).
"""
import re, json, os, sys, time, signal, sqlite3, zlib, hashlib, urllib.request, urllib.error, urllib.parse
import datetime, traceback, fcntl, random, socket
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "archive.sqlite")
MANIFEST = os.path.join(ROOT, "MANIFEST.json")
STATIONS = os.path.join(ROOT, "stations.json")
PIDFILE = os.path.join(ROOT, "collector.pid")
LOCKFILE = os.path.join(ROOT, ".collector.lock")
STATUS = os.path.join(ROOT, "status.json")
FORCE_PHASE_B_FILE = os.path.join(ROOT, "FORCE_PHASE_B")   # touch this file to drop to Phase B caps immediately (budget tripwire)
LOG429 = os.path.join(ROOT, "logs", "kalshi_429.jsonl")
LOGHOURLY = os.path.join(ROOT, "logs", "kalshi_hourly.jsonl")
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
NWS = "https://api.weather.gov"
UA = "AstraCollector/1.0 (research archive; weather-nowcast)"
# GET-only allowlist (full-path regexes). Anything else raises before a request is made.
ALLOWED_URL_RES = [re.compile(x) for x in (
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/events\?series_ticker=[A-Z0-9]+&status=open&with_nested_markets=true$",
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/events/[A-Z0-9.\-]+\?with_nested_markets=true$",
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/markets/orderbooks\?tickers=[A-Z0-9.\-]+(&tickers=[A-Z0-9.\-]+)*$",
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/markets/[A-Z0-9.\-]+/orderbook$",
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/markets/trades\?ticker=[A-Z0-9.\-]+&min_ts=\d+&limit=\d+(&cursor=[A-Za-z0-9_%\-=]+)?$",
    r"^https://api\.elections\.kalshi\.com/trade-api/v2/series/[A-Z0-9]+$",
    r"^https://api\.weather\.gov/stations/[A-Z0-9]+/observations(/latest|\?limit=\d+)$",
    r"^https://api\.weather\.gov/products/types/(CLI|CF6)/locations/[A-Z0-9]+$",
    r"^https://api\.weather\.gov/products/[0-9a-f\-]+$",
    r"^https://api\.weather\.gov/points/-?[0-9.]+,-?[0-9.]+$",
    r"^https://api\.weather\.gov/gridpoints/[A-Z]{3}/\d+,\d+/forecast(/hourly)?$",
)]

# ---- poll intervals (seconds) ----
IV = {
    "kalshi_discover": 1800, "kalshi_events": 6 * 3600, "kalshi_event_meta": 900, "kalshi_event_meta_closed": 1800, "kalshi_orderbook": 60,
    "kalshi_trades": 5, "kalshi_series_meta": 12 * 3600,
    "nws_obs": 300, "nws_cli": 1800, "nws_cf6": 3600, "nws_forecast": 3600, "config_check": 60, "status": 60,
}
# ---- Kalshi GET budget: /workspace/lab/governance/astra/COLLECTOR_KALSHI_GET_BUDGET_2026-09-24.md ----
KALSHI_MIN_SPACING = 6.0          # Phase A floor: >= 6 s between any two Kalshi GETs (<= 10 rpm)
KALSHI_MIN_SPACING_B = 12.0       # Phase B floor: >= 12 s (<= 5 rpm)
LIST_RPM_A = 4                    # list endpoints (/events, /markets, /markets/trades, /series) <= 4 rpm in A -> >= 15 s apart
LIST_RPM_B = 2                    # <= 2 rpm in B -> >= 30 s apart
PHASE_B_START = datetime.datetime(2026, 9, 27, 16, 30, tzinfo=datetime.timezone.utc)
PHASE_B_END = datetime.datetime(2026, 10, 2, 6, 15, tzinfo=datetime.timezone.utc)
LIST_CLASSES = ("events_list", "trades", "series", "markets_list")
# Conductor note 2026-09-24 ~20:04 ET: a one-off audit (<= 3 rpm) may run from this IP until 2026-09-25T03:10Z and counts inside
# this poller's 10 rpm slice -> until then: >= 9 s spacing (<= 6.7 rpm, +3 = 9.7 rpm) and list endpoints >= 60 s apart (<= 1 rpm, +3 = 4 rpm).
AUDIT_WINDOW_END = datetime.datetime(2026, 9, 25, 3, 10, tzinfo=datetime.timezone.utc)
AUDIT_SPACING = 9.0
AUDIT_LIST_INTERVAL = 60.0
PENALTY_429_S = 2.0               # after any 429: +2 s spacing for 30 min (per 429 in the window, cumulative, capped at +10 s)
PENALTY_429_CAP = 10.0
PENALTY_429_WINDOW = 1800
STORM_N, STORM_WINDOW, STORM_PAUSE = 3, 600, 600   # >=3 429s in 10 min -> pause all Kalshi GETs 10 min (PAUSE_429_STORM)
KALSHI_BACKOFF_BASE = 30.0        # 429 without Retry-After: 30, 60, 120, 240, ... capped at 600; reset after one success
KALSHI_BACKOFF_CAP = 600.0
RETRY_FAILED_DISCOVERY_SEC = 180  # failed predicted-event discovery (429 etc.) retries sooner than the 30 min cadence (new logical request, paced by budget)
TRADES_SWEEP_TARGET_A = 1800      # every tracked market gets a trades poll at least this often (else budget_shortfall gap)
TRADES_SWEEP_TARGET_B = 3600
BOOK_LATE_SEC = 150               # open market without a book snapshot for this long -> orderbook_late gap
LIST_DISCOVERY_SEC = 6 * 3600     # cross-check discovery via list endpoint (predicted per-event GETs are primary)
NWS_MIN_SPACING = 1.0
OBS_STALE_SEC = 90 * 60
CLI_STALE_SEC = 36 * 3600
CF6_STALE_SEC = 36 * 3600
TRACK_CLOSED_DAYS = 10            # keep polling closed markets for result/metadata this long after close_time

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)
def iso(dt=None):
    return (dt or utcnow()).isoformat(timespec="milliseconds").replace("+00:00", "Z")
def parse_iso(s):
    if not s: return None
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None
def z(b):
    if isinstance(b, str): b = b.encode()
    return zlib.compress(b, 6)
def sha(b):
    if isinstance(b, str): b = b.encode()
    return hashlib.sha256(b).hexdigest()

LOGF = None
def log(*a):
    line = iso() + " " + " ".join(str(x) for x in a)
    print(line, flush=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(run_id INTEGER PRIMARY KEY, pid INT, host TEXT, started_at TEXT, last_heartbeat TEXT, ended_at TEXT, end_reason TEXT);
CREATE TABLE IF NOT EXISTS polls(id INTEGER PRIMARY KEY, run_id INT, stream TEXT, key TEXT, url TEXT, requested_at TEXT, received_at TEXT,
    http_status INT, ok INT, n_items INT, n_new INT, latency_ms INT, error TEXT);
CREATE INDEX IF NOT EXISTS polls_sk ON polls(stream, key, requested_at);
CREATE TABLE IF NOT EXISTS gaps(id INTEGER PRIMARY KEY, stream TEXT, key TEXT, started_at TEXT, ended_at TEXT, reason TEXT, detail TEXT, n_polls INT DEFAULT 1);
CREATE INDEX IF NOT EXISTS gaps_open ON gaps(stream, key, ended_at);
CREATE TABLE IF NOT EXISTS config_versions(id INTEGER PRIMARY KEY, loaded_at TEXT, sha256 TEXT, body TEXT, trigger TEXT);
CREATE TABLE IF NOT EXISTS kalshi_series_meta(id INTEGER PRIMARY KEY, series_ticker TEXT, received_at TEXT, sha256 TEXT, raw BLOB);
CREATE TABLE IF NOT EXISTS kalshi_events(id INTEGER PRIMARY KEY, series_ticker TEXT, event_ticker TEXT, received_at TEXT, sha256 TEXT, strike_date TEXT, raw BLOB);
CREATE INDEX IF NOT EXISTS kev_t ON kalshi_events(event_ticker, received_at);
CREATE TABLE IF NOT EXISTS kalshi_markets(id INTEGER PRIMARY KEY, series_ticker TEXT, event_ticker TEXT, ticker TEXT, received_at TEXT, sha256 TEXT,
    status TEXT, result TEXT, close_time TEXT, expiration_time TEXT, updated_time TEXT, volume_fp TEXT, open_interest_fp TEXT,
    yes_bid_dollars TEXT, yes_ask_dollars TEXT, last_price_dollars TEXT, raw BLOB);
CREATE INDEX IF NOT EXISTS km_t ON kalshi_markets(ticker, received_at);
CREATE TABLE IF NOT EXISTS kalshi_orderbook(id INTEGER PRIMARY KEY, series_ticker TEXT, ticker TEXT, requested_at TEXT, received_at TEXT, via TEXT,
    sha256 TEXT, same_as_prev INT, n_yes INT, n_no INT, best_yes_bid TEXT, best_no_bid TEXT, raw BLOB);
CREATE INDEX IF NOT EXISTS kob_t ON kalshi_orderbook(ticker, received_at);
CREATE TABLE IF NOT EXISTS kalshi_trades(trade_id TEXT PRIMARY KEY, series_ticker TEXT, ticker TEXT, created_time TEXT, received_at TEXT,
    yes_price_dollars TEXT, no_price_dollars TEXT, count_fp TEXT, taker_side TEXT, raw TEXT);
CREATE INDEX IF NOT EXISTS ktr_t ON kalshi_trades(ticker, created_time);
CREATE TABLE IF NOT EXISTS nws_obs(id INTEGER PRIMARY KEY, station TEXT, obs_timestamp TEXT, received_at TEXT, via TEXT, sha256 TEXT,
    pre_archive_start INT, temperature_c REAL, raw_message TEXT, raw BLOB, UNIQUE(station, obs_timestamp, sha256));
CREATE INDEX IF NOT EXISTS nobs_t ON nws_obs(station, obs_timestamp);
CREATE TABLE IF NOT EXISTS nws_product_index(product_id TEXT, product_type TEXT, location TEXT, issuance_time TEXT, issuing_office TEXT,
    wmo_collective_id TEXT, first_seen_at TEXT, status TEXT, PRIMARY KEY(product_id, location));
CREATE TABLE IF NOT EXISTS nws_products(product_id TEXT PRIMARY KEY, product_type TEXT, location TEXT, issuance_time TEXT, issuing_office TEXT,
    wmo_collective_id TEXT, received_at TEXT, sha256 TEXT, product_text TEXT, raw BLOB);
CREATE TABLE IF NOT EXISTS nws_forecast(id INTEGER PRIMARY KEY, station TEXT, kind TEXT, url TEXT, requested_at TEXT, received_at TEXT,
    update_time TEXT, generated_at TEXT, sha256 TEXT, same_as_prev INT, raw BLOB);
CREATE INDEX IF NOT EXISTS nfc_t ON nws_forecast(station, kind, received_at);
CREATE TABLE IF NOT EXISTS nws_listing_snapshots(id INTEGER PRIMARY KEY, product_type TEXT, location TEXT, received_at TEXT, sha256 TEXT, same_as_prev INT, raw BLOB);
"""

class Stop(Exception): pass

class Collector:
    def __init__(self):
        self.manifest = json.load(open(MANIFEST))
        self.started_at = parse_iso(self.manifest["archive_started_at"])
        self.stop_at = parse_iso(self.manifest["stop_at"])
        self.db = sqlite3.connect(DB_PATH, timeout=60, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.execute("PRAGMA busy_timeout=60000")
        self.db.executescript(SCHEMA)
        self.run_id = None
        self.cfg = None; self.cfg_sha = None; self.cfg_mtime = None; self.cfg_loaded_at = 0
        self.hup = False; self.term = False
        self.last = {}                 # schedule: name -> last run monotonic
        self.k_last_req = 0.0; self.k_last_list = 0.0; self.k_cooldown = {}; self.k_429_streak = {}
        self.k429_times = []           # wall-clock times of recent 429s
        self.k_pause_until = 0.0       # monotonic; PAUSE_429_STORM
        self.hour_key = None; self.hour_counts = {}
        self.last_book_at = {}         # ticker -> wall time of last stored book
        self.tracked_since = {}        # ticker -> wall time first tracked in this run
        self.n_last_req = 0.0
        self.tracked = {}              # ticker -> dict(series, event, close_time, status, result, volume)
        self.trade_cursor = {}         # ticker -> last created_time epoch seconds seen
        self.book_at_trade_poll = {}   # ticker -> orderbook sha at last successful trades poll
        self.trade_polled_at = {}      # ticker -> wall time of last trades poll attempt
        self.trade_ok_at = {}          # ticker -> wall time of last successful trades poll
        self.prev_book_sha = {}
        self.prev_mkt_sha = {}
        self.prev_evt_sha = {}
        self.prev_listing_sha = {}
        self.batch_ok = True; self.batch_retry_at = 0
        self.stats = {"started": iso()}
        self.lastsuccess = {}

    # ---------- infra ----------
    def gap_open(self, stream, key, reason, detail=""):
        cur = self.db.execute("SELECT id, reason FROM gaps WHERE stream=? AND key=? AND ended_at IS NULL ORDER BY id DESC LIMIT 1", (stream, key)).fetchone()
        if cur and cur[1] == reason:
            self.db.execute("UPDATE gaps SET n_polls=n_polls+1, detail=? WHERE id=?", (detail[:500], cur[0])); return
        if cur:
            self.db.execute("UPDATE gaps SET ended_at=? WHERE id=?", (iso(), cur[0]))
        self.db.execute("INSERT INTO gaps(stream,key,started_at,reason,detail) VALUES(?,?,?,?,?)", (stream, key, iso(), reason, detail[:500]))
        log("GAP open", stream, key, reason, detail[:200])
    def gap_close(self, stream, key):
        cur = self.db.execute("SELECT id FROM gaps WHERE stream=? AND key=? AND ended_at IS NULL", (stream, key)).fetchall()
        for (gid,) in cur:
            self.db.execute("UPDATE gaps SET ended_at=? WHERE id=?", (iso(), gid))
            log("GAP close", stream, key)

    def poll_row(self, stream, key, url, req_at, rec_at, status, ok, n_items=None, n_new=None, lat=None, err=None):
        self.db.execute("INSERT INTO polls(run_id,stream,key,url,requested_at,received_at,http_status,ok,n_items,n_new,latency_ms,error) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (self.run_id, stream, key, url, req_at, rec_at, status, 1 if ok else 0, n_items, n_new, lat, (err or "")[:500] or None))
        if ok: self.lastsuccess[f"{stream}:{key}"] = rec_at

    def check_url(self, url):
        if not any(r.match(url) for r in ALLOWED_URL_RES) or "/portfolio" in url:
            raise RuntimeError("URL not in GET allowlist: " + url[:300])

    def sleep(self, sec):
        end = time.monotonic() + sec
        while True:
            if self.term: raise Stop()
            r = end - time.monotonic()
            if r <= 0: return
            time.sleep(min(r, 1.0))

    def kclass(self, url):
        path = url[len(KALSHI):].split("?")[0]
        if path == "/events": return "events_list"
        if path.startswith("/events/"): return "event"
        if path == "/markets/orderbooks": return "orderbooks"
        if path == "/markets/trades": return "trades"
        if path.startswith("/series/"): return "series"
        return "other"

    def in_cooldown(self, cls):
        return time.monotonic() < self.k_cooldown.get(cls, 0) or time.monotonic() < self.k_pause_until

    def phase(self):
        if os.path.exists(FORCE_PHASE_B_FILE): return "B_forced"
        now = utcnow()
        return "B" if PHASE_B_START <= now < PHASE_B_END else "A"
    def spacing_now(self):
        base = KALSHI_MIN_SPACING_B if self.phase().startswith("B") else KALSHI_MIN_SPACING
        if utcnow() < AUDIT_WINDOW_END: base = max(base, AUDIT_SPACING)
        n = len([x for x in self.k429_times if time.time() - x < PENALTY_429_WINDOW])
        return base + min(PENALTY_429_CAP, PENALTY_429_S * n)
    def list_interval(self):
        v = 60.0 / (LIST_RPM_B if self.phase().startswith("B") else LIST_RPM_A)
        if utcnow() < AUDIT_WINDOW_END: v = max(v, AUDIT_LIST_INTERVAL)
        return v
    def list_ready(self):
        return time.monotonic() >= self.k_last_list + self.list_interval()
    def sweep_target(self):
        return TRADES_SWEEP_TARGET_B if self.phase().startswith("B") else TRADES_SWEEP_TARGET_A

    def count(self, field):
        hk = utcnow().strftime("%Y-%m-%dT%H:00Z")
        if self.hour_key != hk:
            self.flush_hour(partial=False)
            self.hour_key = hk; self.hour_counts = {}
        self.hour_counts[field] = self.hour_counts.get(field, 0) + 1
    def flush_hour(self, partial):
        if self.hour_key is None: return
        rec = {"hour_utc": self.hour_key, "poller": "weather", "partial": partial, "phase": self.phase(), "spacing_now_s": self.spacing_now(),
               "requests": self.hour_counts.get("requests", 0), "ok": self.hour_counts.get("ok", 0), "http_429": self.hour_counts.get("http_429", 0),
               "other_error": self.hour_counts.get("other_error", 0), "list_requests": self.hour_counts.get("list_requests", 0),
               "skipped_cooldown_or_pause": self.hour_counts.get("skipped", 0), "run_id": self.run_id, "pid": os.getpid()}
        with open(LOGHOURLY, "a") as f: f.write(json.dumps(rec) + "\n")
    def log429(self, rec):
        with open(LOG429, "a") as f: f.write(json.dumps(rec) + "\n")

    def http_get(self, url, kalshi, accept="application/json"):
        """Returns (status, body_bytes, requested_at_iso, received_at_iso, latency_ms, err). Never raises on HTTP errors."""
        self.check_url(url)
        if kalshi:
            cls = self.kclass(url); is_list = cls in LIST_CLASSES
            now = time.monotonic()
            if now < self.k_pause_until:
                self.count("skipped")
                return (None, None, iso(), iso(), 0, f"skipped_kalshi_pause_429_storm class={cls}")
            if self.k_pause_until and now >= self.k_pause_until:
                self.k_pause_until = 0.0; self.gap_close("kalshi_all", "pause_429_storm"); log("PAUSE_429_STORM ended")
            if now < self.k_cooldown.get(cls, 0):
                self.count("skipped")
                return (None, None, iso(), iso(), 0, f"skipped_kalshi_cooldown_after_429 class={cls}")
            wait = self.k_last_req + self.spacing_now() - now
            if is_list: wait = max(wait, self.k_last_list + self.list_interval() - now)
            if wait > 0: self.sleep(wait)
            self.k_last_req = time.monotonic()
            if is_list: self.k_last_list = self.k_last_req
            self.count("requests")
            if is_list: self.count("list_requests")
        else:
            wait = self.n_last_req + NWS_MIN_SPACING - time.monotonic()
            if wait > 0: self.sleep(wait)
            self.n_last_req = time.monotonic()
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA, "Accept": accept})
        t0 = time.monotonic(); req_at = iso()
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read(); rec_at = iso()
                if kalshi: self.k_429_streak[cls] = 0; self.count("ok")
                return (r.status, body, req_at, rec_at, int((time.monotonic() - t0) * 1000), None)
        except urllib.error.HTTPError as e:
            rec_at = iso()
            try: body = e.read()
            except Exception: body = b""
            err = f"HTTP {e.code}"
            if kalshi and e.code != 429: self.count("other_error")
            if e.code == 429 and kalshi:
                ra = e.headers.get("Retry-After")
                try: wait = float(ra)
                except Exception: wait = None
                self.k_429_streak[cls] = self.k_429_streak.get(cls, 0) + 1
                if wait is None:
                    wait = min(KALSHI_BACKOFF_CAP, KALSHI_BACKOFF_BASE * (2 ** (self.k_429_streak[cls] - 1)))
                wait += random.uniform(0, 3)   # jitter only ever lengthens the wait
                self.k_cooldown[cls] = time.monotonic() + wait
                self.count("http_429")
                tnow = time.time(); self.k429_times.append(tnow)
                self.k429_times = [x for x in self.k429_times if tnow - x < PENALTY_429_WINDOW]
                path = url[len(KALSHI):].split("?")[0]
                self.log429({"ts_utc": iso(), "poller": "weather", "path": path, "status": 429, "retry_after": ra,
                             "spacing_now_s": self.spacing_now(), "cooldown_s": round(wait, 1), "class": cls, "phase": self.phase()})
                err += f" class={cls} retry_after={ra} cooldown={wait:.0f}s"
                log("KALSHI 429", url, err)
                n10 = sum(1 for x in self.k429_times if tnow - x < STORM_WINDOW)
                if n10 >= STORM_N and time.monotonic() >= self.k_pause_until:
                    self.k_pause_until = time.monotonic() + STORM_PAUSE
                    log(f"PAUSE_429_STORM n429_10min={n10} n429_30min={len(self.k429_times)} pause_s={STORM_PAUSE}")
                    self.log429({"ts_utc": iso(), "poller": "weather", "event": "PAUSE_429_STORM", "n429_10min": n10,
                                 "n429_30min": len(self.k429_times), "pause_s": STORM_PAUSE, "spacing_now_s": self.spacing_now()})
                    self.gap_open("kalshi_all", "pause_429_storm", "pause_429_storm", f"{n10} 429s in 10 min; all Kalshi GETs paused {STORM_PAUSE}s")
            return (e.code, body, req_at, rec_at, int((time.monotonic() - t0) * 1000), err)
        except Exception as e:
            if kalshi: self.count("other_error")
            return (None, None, req_at, iso(), int((time.monotonic() - t0) * 1000), f"{type(e).__name__}: {e}")

    def fail_reason(self, status, err):
        if err and err.startswith("skipped_kalshi_cooldown"): return "kalshi_429_cooldown"
        if err and err.startswith("skipped_kalshi_pause"): return "kalshi_pause_429_storm"
        if status == 429: return "http_429"
        if status is None: return "network_error"
        return f"http_{status}"

    # ---------- config ----------
    def load_config(self, trigger):
        try:
            st = os.stat(STATIONS)
            body = open(STATIONS).read()
            cfg = json.loads(body)
            series = cfg["series"]
            for s in series:
                assert s["series_ticker"] and s["nws_station"] and s["cli_location"]
        except Exception as e:
            log("CONFIG load failed (keeping previous):", e)
            if self.cfg is None: raise
            self.cfg_mtime = os.stat(STATIONS).st_mtime if os.path.exists(STATIONS) else None
            return
        h = sha(body)
        self.cfg_mtime = st.st_mtime; self.cfg_loaded_at = time.time()
        if h != self.cfg_sha:
            self.db.execute("INSERT INTO config_versions(loaded_at,sha256,body,trigger) VALUES(?,?,?,?)", (iso(), h, body, trigger))
            log("CONFIG loaded", trigger, h[:12], [s["series_ticker"] for s in series])
            old = set(self.series_list()) if self.cfg else set()
            self.cfg = cfg; self.cfg_sha = h
            if set(self.series_list()) != old:
                self.last.pop("kalshi_events", None)   # rediscover immediately
                self.last.pop("kalshi_series_meta", None)
                # drop tracked tickers of removed series (archive rows are kept)
                for t in [t for t, v in self.tracked.items() if v["series"] not in self.series_list()]:
                    self.tracked.pop(t, None)
        else:
            self.cfg = cfg

    def series_list(self):
        return [s["series_ticker"] for s in self.cfg["series"]]
    def stations(self):
        seen = []; out = []
        for s in self.cfg["series"]:
            if s["nws_station"] not in seen:
                seen.append(s["nws_station"]); out.append(s["nws_station"])
        return out
    def locations(self, key):
        out = []
        for s in self.cfg["series"]:
            v = s.get(key)
            if v and v not in out: out.append(v)
        return out

    # ---------- Kalshi ----------
    def do_series_meta(self):
        for st in self.series_list():
            url = f"{KALSHI}/series/{urllib.parse.quote(st)}"
            status, body, rq, rc, lat, err = self.http_get(url, True)
            ok = status == 200
            self.poll_row("kalshi_series_meta", st, url, rq, rc, status, ok, 1 if ok else 0, None, lat, err)
            if ok:
                self.db.execute("INSERT INTO kalshi_series_meta(series_ticker,received_at,sha256,raw) VALUES(?,?,?,?)", (st, rc, sha(body), z(body)))
                self.gap_close("kalshi_series_meta", st)
            else:
                self.gap_open("kalshi_series_meta", st, self.fail_reason(status, err), err or "")

    def do_events(self):
        failed = False
        for st in self.series_list():
            url = f"{KALSHI}/events?series_ticker={urllib.parse.quote(st)}&status=open&with_nested_markets=true"
            status, body, rq, rc, lat, err = self.http_get(url, True)
            if status != 200:
                self.poll_row("kalshi_events", st, url, rq, rc, status, False, None, None, lat, err)
                self.gap_open("kalshi_events", st, self.fail_reason(status, err), err or "")
                failed = True
                continue
            try:
                d = json.loads(body)
            except Exception as e:
                self.poll_row("kalshi_events", st, url, rq, rc, status, False, None, None, lat, "bad json")
                self.gap_open("kalshi_events", st, "bad_json", str(e)); continue
            n_new = 0
            evs = d.get("events") or []
            for e in evs:
                raw = json.dumps(e, sort_keys=True, separators=(",", ":"))
                h = sha(raw)
                if self.prev_evt_sha.get(e["event_ticker"]) != h:
                    self.db.execute("INSERT INTO kalshi_events(series_ticker,event_ticker,received_at,sha256,strike_date,raw) VALUES(?,?,?,?,?,?)",
                                    (st, e["event_ticker"], rc, h, e.get("strike_date"), z(raw)))
                    self.prev_evt_sha[e["event_ticker"]] = h
                for m in e.get("markets") or []:
                    t = m["ticker"]
                    if self.track(t, st, e["event_ticker"], "events_list"): n_new += 1
                    self.store_market(st, m, rc)
                    self.update_tracked(t, m)
            self.poll_row("kalshi_events", st, url, rq, rc, status, True, len(evs), n_new, lat, None)
            self.gap_close("kalshi_events", st)
        if failed:   # list endpoint is only a cross-check; retry in 30 min rather than 6 h
            self.last["kalshi_events"] = time.monotonic() - IV["kalshi_events"] + 1800

    def restore_tracked(self):
        """After a restart, resume tracking markets already seen in the archive (latest stored metadata row per ticker)."""
        rows = self.db.execute("""SELECT k.series_ticker, k.event_ticker, k.ticker, k.status, k.result, k.close_time, k.volume_fp FROM kalshi_markets k
            JOIN (SELECT ticker, max(id) mid FROM kalshi_markets GROUP BY ticker) x ON x.mid = k.id""").fetchall()
        now = utcnow(); n = 0
        for series, ev, t, status, result, ct, vol in rows:
            if series not in self.series_list(): continue
            c = parse_iso(ct)
            if c and (now - c).total_seconds() > TRACK_CLOSED_DAYS * 86400: continue
            self.tracked[t] = {"series": series, "event": ev, "status": status, "result": result, "close_time": ct, "volume": vol}
            self.trade_cursor[t] = self.initial_trade_cursor(t); self.tracked_since[t] = time.time(); n += 1
        if n: log("restored", n, "tracked markets from archive")

    def initial_trade_cursor(self, t):
        r = self.db.execute("SELECT max(created_time) FROM kalshi_trades WHERE ticker=?", (t,)).fetchone()
        if r and r[0]:
            dt = parse_iso(r[0])
            if dt: return int(dt.timestamp())
        return int(self.started_at.timestamp())   # prospective: never before archive_started_at

    def update_tracked(self, t, m):
        tr = self.tracked[t]
        tr["close_time"] = m.get("close_time"); tr["status"] = m.get("status"); tr["result"] = m.get("result")
        tr["volume"] = m.get("volume_fp")

    def open_tickers(self):
        out = []
        for t, v in self.tracked.items():
            if v.get("status") in ("active", "open", "initialized", None):
                out.append(t)
        return sorted(out)

    def closed_pending(self):
        out = []; now = utcnow()
        for t, v in self.tracked.items():
            if t in self.open_tickers(): continue
            ct = parse_iso(v.get("close_time"))
            if v.get("status") in ("finalized", "settled") and v.get("result"): continue
            if ct and (now - ct).total_seconds() > TRACK_CLOSED_DAYS * 86400: continue
            out.append(t)
        return sorted(out)

    def store_market(self, series, m, rc):
        t = m.get("ticker")
        raw = json.dumps(m, sort_keys=True, separators=(",", ":")); h = sha(raw)
        if self.prev_mkt_sha.get(t) == h: return 0
        self.db.execute("""INSERT INTO kalshi_markets(series_ticker,event_ticker,ticker,received_at,sha256,status,result,close_time,expiration_time,
            updated_time,volume_fp,open_interest_fp,yes_bid_dollars,yes_ask_dollars,last_price_dollars,raw) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (series, m.get("event_ticker"), t, rc, h, m.get("status"), m.get("result"), m.get("close_time"),
             m.get("expiration_time"), m.get("updated_time"), m.get("volume_fp"), m.get("open_interest_fp"), m.get("yes_bid_dollars"),
             m.get("yes_ask_dollars"), m.get("last_price_dollars"), z(raw)))
        self.prev_mkt_sha[t] = h
        return 1

    def track(self, t, series, ev, why):
        if t in self.tracked: return False
        self.tracked[t] = {"series": series, "event": ev}
        self.tracked_since.setdefault(t, time.time())
        self.trade_cursor.setdefault(t, self.initial_trade_cursor(t))
        log("TRACK new market", t, "via", why)
        return True

    def fetch_event(self, ev, series, stream, missing_is_gap=True):
        """Single-object GET /events/{event_ticker}?with_nested_markets=true. Returns http status (None on skip/network)."""
        url = f"{KALSHI}/events/{urllib.parse.quote(ev)}?with_nested_markets=true"
        status, body, rq, rc, lat, err = self.http_get(url, True)
        if status == 404 and not missing_is_gap:
            self.poll_row(stream, ev, url, rq, rc, status, False, 0, 0, lat, "not_listed_yet (404; predicted ticker, not a gap)")
            return status
        if status != 200:
            self.poll_row(stream, ev, url, rq, rc, status, False, None, None, lat, err)
            self.gap_open(stream, ev, self.fail_reason(status, err), err or "")
            return status
        try:
            d = json.loads(body); e = d.get("event") or {}
            ms = e.get("markets") or d.get("markets") or []
        except Exception as ex:
            self.poll_row(stream, ev, url, rq, rc, status, False, None, None, lat, "bad json"); self.gap_open(stream, ev, "bad_json", str(ex)); return None
        series = e.get("series_ticker") or series
        ev_raw = json.dumps({k: v for k, v in e.items() if k != "markets"}, sort_keys=True, separators=(",", ":")); h = sha(ev_raw)
        if self.prev_evt_sha.get(ev + "#meta") != h:
            self.db.execute("INSERT INTO kalshi_events(series_ticker,event_ticker,received_at,sha256,strike_date,raw) VALUES(?,?,?,?,?,?)",
                            (series, ev, rc, h, e.get("strike_date"), z(ev_raw)))
            self.prev_evt_sha[ev + "#meta"] = h
        n_new = 0
        for m in ms:
            t = m.get("ticker")
            if not t: continue
            self.track(t, series, ev, stream)
            n_new += self.store_market(series, m, rc)
            self.update_tracked(t, m)
        self.poll_row(stream, ev, url, rq, rc, status, True, len(ms), n_new, lat, None)
        self.gap_close(stream, ev)
        return status

    def predicted_events(self):
        """Event tickers for 'today' and 'tomorrow' in each series' local timezone (Kalshi format SERIES-YYMONDD).
        Only used to issue single-event GETs; a 404 means not listed yet. Nothing is stored unless Kalshi returns it."""
        out = []
        for s in self.cfg["series"]:
            tz = ZoneInfo(s.get("timezone") or "America/New_York")
            today = datetime.datetime.now(tz).date()
            for i, d in enumerate((today, today + datetime.timedelta(days=1))):
                out.append((s["series_ticker"], f"{s['series_ticker']}-{d.strftime('%y')}{d.strftime('%b').upper()}{d.strftime('%d')}", i == 0))
        return out

    def do_discover(self):
        known = {v["event"] for v in self.tracked.values()}
        failed = False
        for series, ev, is_today in self.predicted_events():
            if ev in known: continue
            st = self.fetch_event(ev, series, "kalshi_discover", missing_is_gap=is_today)
            if st not in (200, 404): failed = True
            if st == 429 or self.in_cooldown("event"): break
        if failed:
            self.last["kalshi_discover"] = time.monotonic() - IV["kalshi_discover"] + RETRY_FAILED_DISCOVERY_SEC

    def do_event_meta(self, which):
        opent = set(self.open_tickers()); pend = set(self.closed_pending())
        want = opent if which == "open" else (pend - opent)
        evs = sorted({(self.tracked[t]["event"], self.tracked[t]["series"]) for t in want})
        for ev, series in evs:
            st = self.fetch_event(ev, series, "kalshi_event_meta")
            if st == 429 or self.in_cooldown("event"): break

    def book_summary(self, ob):
        fp = ob.get("orderbook_fp") or ob.get("orderbook") or {}
        yes = fp.get("yes_dollars") or fp.get("yes") or []
        no = fp.get("no_dollars") or fp.get("no") or []
        by = yes[-1][0] if yes else None   # levels are ascending by price; best bid = last
        bn = no[-1][0] if no else None
        return len(yes), len(no), (str(by) if by is not None else None), (str(bn) if bn is not None else None)

    def store_book(self, t, obj, rq, rc, via):
        raw = json.dumps(obj, sort_keys=True, separators=(",", ":")); h = sha(raw)
        same = 1 if self.prev_book_sha.get(t) == h else 0
        ny, nn, by, bn = self.book_summary(obj)
        self.db.execute("INSERT INTO kalshi_orderbook(series_ticker,ticker,requested_at,received_at,via,sha256,same_as_prev,n_yes,n_no,best_yes_bid,best_no_bid,raw) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (self.tracked.get(t, {}).get("series"), t, rq, rc, via, h, same, ny, nn, by, bn, None if same else z(raw)))
        self.prev_book_sha[t] = h
        self.last_book_at[t] = time.time()

    def do_orderbooks(self):
        tickers = self.open_tickers()
        if not tickers: return
        if self.batch_ok or time.monotonic() > self.batch_retry_at:
            for i in range(0, len(tickers), 100):
                chunk = tickers[i:i + 100]
                url = f"{KALSHI}/markets/orderbooks?" + "&".join("tickers=" + urllib.parse.quote(t) for t in chunk)
                status, body, rq, rc, lat, err = self.http_get(url, True)
                if status == 200:
                    try:
                        obs = json.loads(body).get("orderbooks") or []
                    except Exception as e:
                        obs = None; err = "bad json"
                    if obs is not None:
                        got = set()
                        for ob in obs:
                            t = ob.get("ticker")
                            if t in chunk:
                                got.add(t); self.store_book(t, ob, rq, rc, "batch")
                        self.poll_row("kalshi_orderbook", "batch", url[:300], rq, rc, status, True, len(obs), len(got), lat, None)
                        self.gap_close("kalshi_orderbook", "batch")
                        for t in chunk:
                            if t in got: self.gap_close("kalshi_orderbook", t)
                            else: self.gap_open("kalshi_orderbook", t, "ticker_missing_from_batch", "")
                        self.batch_ok = True
                        continue
                self.poll_row("kalshi_orderbook", "batch", url[:300], rq, rc, status, False, None, None, lat, err)
                self.gap_open("kalshi_orderbook", "batch", self.fail_reason(status, err), f"{len(chunk)} tickers; {err or ''}")
                if status in (400, 401, 403, 404, 405):
                    # batch route unavailable unauthenticated -> fall back to per-market GETs (paced by KALSHI_MIN_SPACING)
                    self.batch_ok = False; self.batch_retry_at = time.monotonic() + 3600
                    log("batch orderbook unavailable, falling back to per-market", status)
        if not self.batch_ok:
            for t in tickers:
                url = f"{KALSHI}/markets/{urllib.parse.quote(t)}/orderbook"
                status, body, rq, rc, lat, err = self.http_get(url, True)
                ok = status == 200
                if ok:
                    try:
                        ob = json.loads(body); ob = dict(ob); ob.setdefault("ticker", t)
                        self.store_book(t, ob, rq, rc, "single")
                    except Exception as e:
                        ok = False; err = "bad json"
                self.poll_row("kalshi_orderbook", t, url, rq, rc, status, ok, 1 if ok else None, None, lat, err)
                if ok: self.gap_close("kalshi_orderbook", t)
                else: self.gap_open("kalshi_orderbook", t, self.fail_reason(status, err), err or "")
                if status == 429 or (err or "").startswith("skipped"): break
        # shortfall accounting: open markets without a fresh snapshot (budget, 429, fallback too slow) are gaps, never filled
        now = time.time()
        for t in tickers:
            ref = self.last_book_at.get(t, self.tracked_since.get(t, now))
            if now - ref > BOOK_LATE_SEC:
                self.gap_open("kalshi_orderbook_late", t, "orderbook_snapshot_late", f"no snapshot for {now - ref:.0f}s")
            else:
                self.gap_close("kalshi_orderbook_late", t)

    def do_trades(self, sweep=False):
        """Issues at most ONE logical trades poll per call (list endpoint budget: 4 rpm A / 2 rpm B).
        Priority: (1) markets overdue vs sweep target, oldest first; (2) markets whose book changed since their last trades poll
        (a fill always changes the book); (3) routine sweep for markets not polled for >= half the sweep target."""
        if not self.list_ready() or self.in_cooldown("trades"):
            self.trades_shortfall(); return
        now = time.time(); target = self.sweep_target()
        cands = self.open_tickers() + self.closed_pending()
        if not cands: return
        age = lambda t: now - self.trade_polled_at.get(t, self.tracked_since.get(t, now))
        overdue = sorted([t for t in cands if age(t) >= target], key=lambda t: -age(t))
        changed = sorted([t for t in self.open_tickers() if t in self.prev_book_sha and self.book_at_trade_poll.get(t) != self.prev_book_sha.get(t)], key=lambda t: -age(t))
        routine = sorted([t for t in cands if age(t) >= target / 2], key=lambda t: -age(t))
        pick = (overdue or changed or routine or [None])[0]
        if pick is None:
            self.trades_shortfall(); return
        for t in [pick]:
            self.trade_polled_at[t] = time.time()
            book_sha_now = self.prev_book_sha.get(t)
            book_sha_now = self.prev_book_sha.get(t)
            cursor = None; n_items = 0; n_new = 0; ok_all = True; last_status = None
            min_ts = max(int(self.started_at.timestamp()), self.trade_cursor.get(t, int(self.started_at.timestamp())) - 1)
            max_seen = self.trade_cursor.get(t, min_ts)
            for page in range(10):
                url = f"{KALSHI}/markets/trades?ticker={urllib.parse.quote(t)}&min_ts={min_ts}&limit=1000" + (f"&cursor={urllib.parse.quote(cursor, safe='')}" if cursor else "")
                status, body, rq, rc, lat, err = self.http_get(url, True)
                last_status = status
                if status != 200:
                    ok_all = False
                    self.poll_row("kalshi_trades", t, url, rq, rc, status, False, None, None, lat, err)
                    self.gap_open("kalshi_trades", t, self.fail_reason(status, err), err or "")
                    break
                try:
                    d = json.loads(body)
                except Exception:
                    ok_all = False; self.poll_row("kalshi_trades", t, url, rq, rc, status, False, None, None, lat, "bad json"); self.gap_open("kalshi_trades", t, "bad_json", ""); break
                trs = d.get("trades") or []
                pn = 0
                for tr in trs:
                    raw = json.dumps(tr, sort_keys=True, separators=(",", ":"))
                    cur = self.db.execute("INSERT OR IGNORE INTO kalshi_trades(trade_id,series_ticker,ticker,created_time,received_at,yes_price_dollars,no_price_dollars,count_fp,taker_side,raw) VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (tr.get("trade_id"), self.tracked[t]["series"], tr.get("ticker", t), tr.get("created_time"), rc, tr.get("yes_price_dollars"),
                         tr.get("no_price_dollars"), tr.get("count_fp"), tr.get("taker_side"), raw))
                    pn += cur.rowcount
                    ct = parse_iso(tr.get("created_time"))
                    if ct: max_seen = max(max_seen, int(ct.timestamp()))
                n_items += len(trs); n_new += pn
                self.poll_row("kalshi_trades", t, url, rq, rc, status, True, len(trs), pn, lat, None)
                cursor = d.get("cursor")
                if not cursor or not trs: break
                if page == 9:
                    self.gap_open("kalshi_trades", t, "trades_page_limit", "10 pages x 1000 exhausted; older trades in window not fetched")
            if ok_all:
                if not (cursor and trs): self.gap_close("kalshi_trades", t)
                self.trade_cursor[t] = max_seen
                self.book_at_trade_poll[t] = book_sha_now
                self.trade_ok_at[t] = time.time()
        self.trades_shortfall()

    def trades_shortfall(self):
        """Markets that have not had a successful trades poll within the sweep target -> budget_shortfall gap (never filled)."""
        now = time.time(); target = self.sweep_target()
        for t in self.open_tickers() + self.closed_pending():
            ref = self.trade_ok_at.get(t, self.tracked_since.get(t, now))
            if now - ref > target:
                self.gap_open("kalshi_trades_budget", t, "budget_shortfall_sweep_late", f"last ok trades poll {now - ref:.0f}s ago > target {target}s")
            else:
                self.gap_close("kalshi_trades_budget", t)

    # ---------- NWS ----------
    def store_obs(self, station, feat, rc, via):
        p = feat.get("properties") or {}
        ts = p.get("timestamp")
        if not ts: return 0
        raw = json.dumps(feat, sort_keys=True, separators=(",", ":"))
        h = sha(json.dumps(p, sort_keys=True, separators=(",", ":")))   # version key = source properties (identical obs via /latest and list dedupe)
        t = parse_iso(ts)
        pre = 1 if (t and t < self.started_at) else 0
        temp = (p.get("temperature") or {}).get("value")
        cur = self.db.execute("INSERT OR IGNORE INTO nws_obs(station,obs_timestamp,received_at,via,sha256,pre_archive_start,temperature_c,raw_message,raw) VALUES(?,?,?,?,?,?,?,?,?)",
                              (station, ts, rc, via, h, pre, temp, p.get("rawMessage"), z(raw)))
        return cur.rowcount

    def do_obs(self):
        for st in self.stations():
            # latest
            url = f"{NWS}/stations/{st}/observations/latest"
            status, body, rq, rc, lat, err = self.http_get(url, False, "application/geo+json")
            latest_ts = None
            if status == 200:
                try:
                    feat = json.loads(body); n = self.store_obs(st, feat, rc, "latest")
                    latest_ts = (feat.get("properties") or {}).get("timestamp")
                    self.poll_row("nws_obs_latest", st, url, rq, rc, status, True, 1, n, lat, None)
                    self.gap_close("nws_obs_latest", st)
                except Exception as e:
                    self.poll_row("nws_obs_latest", st, url, rq, rc, status, False, None, None, lat, "bad json"); self.gap_open("nws_obs_latest", st, "bad_json", str(e))
            else:
                self.poll_row("nws_obs_latest", st, url, rq, rc, status, False, None, None, lat, err)
                self.gap_open("nws_obs_latest", st, self.fail_reason(status, err), err or "")
            # recent list
            url = f"{NWS}/stations/{st}/observations?limit=12"
            status, body, rq, rc, lat, err = self.http_get(url, False, "application/geo+json")
            list_max = None
            if status == 200:
                try:
                    fs = json.loads(body).get("features") or []
                    n = 0
                    for f in fs:
                        n += self.store_obs(st, f, rc, "list")
                        ts = (f.get("properties") or {}).get("timestamp")
                        if ts and (list_max is None or parse_iso(ts) > parse_iso(list_max)): list_max = ts
                    self.poll_row("nws_obs_list", st, url, rq, rc, status, True, len(fs), n, lat, None)
                    self.gap_close("nws_obs_list", st)
                except Exception as e:
                    self.poll_row("nws_obs_list", st, url, rq, rc, status, False, None, None, lat, "bad json"); self.gap_open("nws_obs_list", st, "bad_json", str(e))
            else:
                self.poll_row("nws_obs_list", st, url, rq, rc, status, False, None, None, lat, err)
                self.gap_open("nws_obs_list", st, self.fail_reason(status, err), err or "")
            # staleness (feed returned but newest source timestamp too old)
            cand = [x for x in (latest_ts, list_max) if x]
            if cand:
                newest = max(parse_iso(x) for x in cand)
                age = (utcnow() - newest).total_seconds()
                if age > OBS_STALE_SEC:
                    self.gap_open("nws_obs_fresh", st, "stale", f"newest obs {newest.isoformat()} age {age/60:.0f} min > {OBS_STALE_SEC/60:.0f}")
                else:
                    self.gap_close("nws_obs_fresh", st)

    def do_products(self, ptype, locs, stale_sec):
        stream = "nws_" + ptype.lower()
        for loc in locs:
            url = f"{NWS}/products/types/{ptype}/locations/{loc}"
            status, body, rq, rc, lat, err = self.http_get(url, False, "application/ld+json")
            if status != 200:
                self.poll_row(stream + "_list", loc, url, rq, rc, status, False, None, None, lat, err)
                self.gap_open(stream + "_list", loc, self.fail_reason(status, err), err or ""); continue
            try:
                d = json.loads(body); items = d.get("@graph") or []
            except Exception as e:
                self.poll_row(stream + "_list", loc, url, rq, rc, status, False, None, None, lat, "bad json"); self.gap_open(stream + "_list", loc, "bad_json", str(e)); continue
            h = sha(body); k = (ptype, loc)
            if k not in self.prev_listing_sha:
                r = self.db.execute("SELECT sha256 FROM nws_listing_snapshots WHERE product_type=? AND location=? ORDER BY id DESC LIMIT 1", k).fetchone()
                self.prev_listing_sha[k] = r[0] if r else None
            same = 1 if self.prev_listing_sha[k] == h else 0
            self.db.execute("INSERT INTO nws_listing_snapshots(product_type,location,received_at,sha256,same_as_prev,raw) VALUES(?,?,?,?,?,?)", (ptype, loc, rc, h, same, None if same else z(body)))
            self.prev_listing_sha[k] = h
            first_ever = self.db.execute("SELECT count(*) FROM nws_product_index WHERE product_type=? AND location=?", k).fetchone()[0] == 0
            n_new_idx = 0
            for it in items:
                pid = it.get("id"); it_iss = it.get("issuanceTime")
                if not pid: continue
                exists = self.db.execute("SELECT status FROM nws_product_index WHERE product_id=? AND location=?", (pid, loc)).fetchone()
                if exists: continue
                iss = parse_iso(it_iss)
                status_ = "pre_archive_baseline" if (first_ever and iss and iss < self.started_at) else "pending"
                self.db.execute("INSERT INTO nws_product_index(product_id,product_type,location,issuance_time,issuing_office,wmo_collective_id,first_seen_at,status) VALUES(?,?,?,?,?,?,?,?)",
                                (pid, ptype, loc, it_iss, it.get("issuingOffice"), it.get("wmoCollectiveId"), rc, status_))
                n_new_idx += 1
            self.poll_row(stream + "_list", loc, url, rq, rc, status, True, len(items), n_new_idx, lat, None)
            self.gap_close(stream + "_list", loc)
            # fetch bodies for pending products (prospective: only those not in the pre-archive baseline)
            pend = self.db.execute("SELECT product_id, issuance_time FROM nws_product_index WHERE product_type=? AND location=? AND status IN ('pending','fetch_failed') ORDER BY issuance_time", k).fetchall()
            for pid, it_iss in pend:
                have = self.db.execute("SELECT 1 FROM nws_products WHERE product_id=?", (pid,)).fetchone()
                if have:
                    self.db.execute("UPDATE nws_product_index SET status='fetched' WHERE product_id=? AND location=?", (pid, loc)); continue
                purl = f"{NWS}/products/{pid}"
                s2, b2, rq2, rc2, lat2, err2 = self.http_get(purl, False, "application/ld+json")
                if s2 == 200:
                    try:
                        pd = json.loads(b2)
                        self.db.execute("INSERT OR IGNORE INTO nws_products(product_id,product_type,location,issuance_time,issuing_office,wmo_collective_id,received_at,sha256,product_text,raw) VALUES(?,?,?,?,?,?,?,?,?,?)",
                            (pid, ptype, loc, pd.get("issuanceTime"), pd.get("issuingOffice"), pd.get("wmoCollectiveId"), rc2, sha(b2), pd.get("productText"), z(b2)))
                        self.db.execute("UPDATE nws_product_index SET status='fetched' WHERE product_id=? AND location=?", (pid, loc))
                        self.poll_row(stream + "_product", loc, purl, rq2, rc2, s2, True, 1, 1, lat2, None)
                        self.gap_close(stream + "_product", loc)
                        log("NEW", ptype, loc, pid, pd.get("issuanceTime"))
                        continue
                    except Exception as e:
                        err2 = f"bad json {e}"
                self.db.execute("UPDATE nws_product_index SET status='fetch_failed' WHERE product_id=? AND location=?", (pid, loc))
                self.poll_row(stream + "_product", loc, purl, rq2, rc2, s2, False, None, None, lat2, err2)
                self.gap_open(stream + "_product", loc, self.fail_reason(s2, err2), f"{pid} {err2 or ''}")
            # staleness: newest issuance in listing older than threshold
            iss_all = [parse_iso(it.get("issuanceTime")) for it in items if it.get("issuanceTime")]
            if iss_all:
                age = (utcnow() - max(iss_all)).total_seconds()
                if age > stale_sec: self.gap_open(stream + "_fresh", loc, "stale", f"newest issuance age {age/3600:.1f} h > {stale_sec/3600:.0f} h")
                else: self.gap_close(stream + "_fresh", loc)

    def do_forecast(self):
        """NWS point forecast baseline input (handoff 2026-09-24): /points/{lat},{lon} -> forecast + forecastHourly URLs, hourly.
        Stored verbatim with receipt time; raw blob only when content changed (same_as_prev=1 rows keep the poll record)."""
        if not hasattr(self, "fc_urls"): self.fc_urls = {}; self.fc_prev = {}
        for s in self.cfg["series"]:
            st = s["nws_station"]; lat = s.get("lat"); lon = s.get("lon")
            if lat is None or lon is None: continue
            ent = self.fc_urls.get(st)
            if not ent or time.time() - ent["at"] > 86400:
                url = f"{NWS}/points/{round(float(lat), 4)},{round(float(lon), 4)}"
                status, body, rq, rc, lat_ms, err = self.http_get(url, False, "application/geo+json")
                if status == 200:
                    try:
                        pr = json.loads(body).get("properties") or {}
                        self.fc_urls[st] = ent = {"at": time.time(), "forecast": pr.get("forecast"), "forecastHourly": pr.get("forecastHourly")}
                        self.db.execute("INSERT INTO nws_forecast(station,kind,url,requested_at,received_at,sha256,same_as_prev,raw) VALUES(?,?,?,?,?,?,?,?)",
                                        (st, "points", url, rq, rc, sha(body), 0, z(body)))
                        self.poll_row("nws_points", st, url, rq, rc, status, True, 1, 1, lat_ms, None); self.gap_close("nws_points", st)
                    except Exception as e:
                        self.poll_row("nws_points", st, url, rq, rc, status, False, None, None, lat_ms, f"bad json {e}"); self.gap_open("nws_points", st, "bad_json", str(e)); continue
                else:
                    self.poll_row("nws_points", st, url, rq, rc, status, False, None, None, lat_ms, err); self.gap_open("nws_points", st, self.fail_reason(status, err), err or "")
                    if not ent: continue
            for kind in ("forecast", "forecastHourly"):
                url = ent.get(kind)
                if not url: continue
                try: self.check_url(url)
                except Exception as e:
                    self.gap_open("nws_forecast", f"{st}:{kind}", "url_not_allowlisted", url); continue
                status, body, rq, rc, lat_ms, err = self.http_get(url, False, "application/geo+json")
                key = f"{st}:{kind}"
                if status == 200:
                    try:
                        pr = json.loads(body).get("properties") or {}
                        h = sha(json.dumps(pr, sort_keys=True)); same = 1 if self.fc_prev.get(key) == h else 0
                        self.db.execute("INSERT INTO nws_forecast(station,kind,url,requested_at,received_at,update_time,generated_at,sha256,same_as_prev,raw) VALUES(?,?,?,?,?,?,?,?,?,?)",
                                        (st, kind, url, rq, rc, pr.get("updateTime"), pr.get("generatedAt"), h, same, None if same else z(body)))
                        self.fc_prev[key] = h
                        self.poll_row("nws_forecast", key, url, rq, rc, status, True, 1, 1 - same, lat_ms, None); self.gap_close("nws_forecast", key)
                        continue
                    except Exception as e:
                        err = f"bad json {e}"
                self.poll_row("nws_forecast", key, url, rq, rc, status, False, None, None, lat_ms, err)
                self.gap_open("nws_forecast", key, self.fail_reason(status, err), err or "")

    # ---------- status ----------
    def write_status(self):
        self.db.execute("UPDATE runs SET last_heartbeat=? WHERE run_id=?", (iso(), self.run_id))
        q = lambda s: self.db.execute(s).fetchall()
        st = {"updated_at": iso(), "pid": os.getpid(), "run_id": self.run_id, "archive_started_at": self.manifest["archive_started_at"],
              "stop_at": self.manifest["stop_at"], "config_sha256": self.cfg_sha, "series": self.series_list(),
              "tracked_open": self.open_tickers(), "tracked_closed_pending": self.closed_pending(),
              "kalshi_phase": self.phase(), "kalshi_spacing_now_s": self.spacing_now(), "kalshi_list_interval_s": self.list_interval(),
              "kalshi_pause_remaining_s": max(0, round(self.k_pause_until - time.monotonic())), "kalshi_429_last_30min": len([x for x in self.k429_times if time.time() - x < 1800]),
              "kalshi_hour": {"hour_utc": self.hour_key, **self.hour_counts},
              "kalshi_cooldown_remaining_s": {k: round(v - time.monotonic()) for k, v in self.k_cooldown.items() if v > time.monotonic()},
              "open_gaps": [dict(zip(("stream", "key", "started_at", "reason", "n_polls"), r)) for r in q("SELECT stream,key,started_at,reason,n_polls FROM gaps WHERE ended_at IS NULL")],
              "last_success": self.lastsuccess}
        tmp = STATUS + ".tmp"
        json.dump(st, open(tmp, "w"), indent=1); os.replace(tmp, STATUS)

    def due(self, name):
        now = time.monotonic()
        if name not in self.last or now - self.last[name] >= IV[name]:
            self.last[name] = now; return True
        return False

    def run(self):
        self.run_id = self.db.execute("INSERT INTO runs(pid,host,started_at,last_heartbeat) VALUES(?,?,?,?)", (os.getpid(), socket.gethostname(), iso(), iso())).lastrowid
        # record downtime since the previous run's last heartbeat (collector not running = gap, never filled)
        prev = self.db.execute("SELECT run_id,last_heartbeat,ended_at,end_reason FROM runs WHERE run_id<? ORDER BY run_id DESC LIMIT 1", (self.run_id,)).fetchone()
        if prev and prev[1]:
            self.db.execute("INSERT INTO gaps(stream,key,started_at,ended_at,reason,detail) VALUES('collector','all',?,?,?,?)",
                            (prev[1], iso(), "collector_not_running", f"prev run {prev[0]} end_reason={prev[3]}"))
        self.db.execute("UPDATE gaps SET ended_at=? WHERE stream='supervisor' AND ended_at IS NULL", (iso(),))
        self.load_config("startup")
        self.restore_tracked()
        # budget priority at (re)start: predicted per-event discovery, books and trades first; the list cross-check waits one full
        # interval (6 h) and series metadata waits 30 min, so scarce shared budget is not spent on low-priority GETs right after launch
        self.last["kalshi_events"] = time.monotonic()
        self.last["kalshi_series_meta"] = time.monotonic() - IV["kalshi_series_meta"] + 1800
        log("RUN", self.run_id, "pid", os.getpid(), "stop_at", self.manifest["stop_at"])
        end_reason = "unknown"
        try:
            while True:
                if self.term: raise Stop()
                if utcnow() >= self.stop_at:
                    end_reason = "stop_at_reached"; log("stop_at reached, exiting cleanly"); break
                if self.hup:
                    self.hup = False; self.load_config("SIGHUP")
                if self.due("config_check"):
                    try:
                        m = os.stat(STATIONS).st_mtime
                    except Exception: m = None
                    if m != self.cfg_mtime or time.time() - self.cfg_loaded_at > 86400:
                        self.load_config("mtime_or_daily")
                tasks = [
                    ("kalshi_discover", self.do_discover),
                    ("kalshi_events", self.do_events),
                    ("kalshi_orderbook", self.do_orderbooks),
                    ("kalshi_event_meta", lambda: self.do_event_meta("open")),
                    ("kalshi_trades", self.do_trades),
                    ("kalshi_event_meta_closed", lambda: self.do_event_meta("closed")),
                    ("nws_obs", self.do_obs),
                    ("nws_cli", lambda: self.do_products("CLI", self.locations("cli_location"), CLI_STALE_SEC)),
                    ("nws_forecast", self.do_forecast),
                    ("nws_cf6", lambda: self.do_products("CF6", self.locations("cf6_location"), CF6_STALE_SEC)),
                    ("kalshi_series_meta", self.do_series_meta),
                    ("status", self.write_status),
                ]
                for name, fn in tasks:
                    if self.term: raise Stop()
                    if self.due(name):
                        try:
                            fn()
                        except Stop: raise
                        except Exception as e:
                            log("TASK ERROR", name, repr(e)); traceback.print_exc()
                            self.gap_open(name, "task", "collector_exception", repr(e))
                self.sleep(1.0)
        except Stop:
            end_reason = "signal_term"
        except Exception as e:
            end_reason = "crash: " + repr(e); log("CRASH", repr(e)); traceback.print_exc()
            raise
        finally:
            try:
                self.flush_hour(partial=True)
                self.write_status()
                self.db.execute("UPDATE runs SET ended_at=?, end_reason=?, last_heartbeat=? WHERE run_id=?", (iso(), end_reason, iso(), self.run_id))
            except Exception: pass
            log("EXIT", end_reason)
        return 0 if end_reason == "stop_at_reached" else 3

def main():
    lockf = open(LOCKFILE, "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another collector holds the lock; exiting", flush=True); return 4
    c = Collector()
    if utcnow() >= c.stop_at:
        log("stop_at already passed; not starting"); return 0
    open(PIDFILE, "w").write(str(os.getpid()) + "\n")
    def on_term(sig, frm): c.term = True
    def on_hup(sig, frm): c.hup = True
    signal.signal(signal.SIGTERM, on_term); signal.signal(signal.SIGINT, on_term); signal.signal(signal.SIGHUP, on_hup)
    return c.run()

if __name__ == "__main__":
    sys.exit(main())
