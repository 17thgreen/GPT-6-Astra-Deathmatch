"""Scorability runner. Sha-checks pins, builds quotes and fills, then joins.

Quote and fill construction does not open the settlement folder.
"""
import hashlib
import json
from pathlib import Path

import fill_engine
import scoring
import settled_join
import tape_quotes
from tape_quotes import (
    UNIVERSE,
    Admit1WindowRejected,
    CaptureSqliteRefused,
    ClosedUniverseRefused,
    LabError,
    PinMismatch,
    assert_open_universe,
    canonical_bytes,
    in_admit1_window,
    refuse_sqlite_path,
    sha256_file,
    stamp_from_name,
)


LAB_ROOT = Path(__file__).resolve().parent
REPO_ROOT = LAB_ROOT.parent
PINS = LAB_ROOT / 'pins'
ACCEPT_SHA256 = '9c6e19ca11a855015fb4e3e63cd65ae5e5c334875240e817e164e988426df9f5'
FREEZE_SHA256 = '213ee6dd33f292c8041977b0b8d7566da9412fd3debe0597643c500dc1e42db4'
BUNDLE_SHA256 = 'bd94757c4c5748fc3447cf596435ddee0af129c87599d4c48f002b2b61756308'
FREEZE_JSON_SHA256 = '6399ebe6687c64972d2826df8cc36772582604e7a30b60e1b890a6d7e9cb0e55'
PACKET_MANIFEST_SHA256 = '6e89b8098d29971070098e196347f9f75247ade83cc7ba4d79f694d55a790134'
TAPE_SOURCE_PINS_SHA256 = '1846a9710375dd418983e1a03e05ac15386138ada7c405923b7fd0514cf116a1'
READY_SHA256 = '0dd61920f8e622c336cf9ab2ac88d0d78b04d4152c93cf98cecb14550b7d924c'
DIGESTS_SHA256 = '5905c137089d42ae07c53720762b9dcc9c8b0ad9c4f17ebe51340d18198a1044'
FOLDER_DIGEST_SHA256 = '65cfe9e4855038263853b236df8eb4852d85d789546215a59f350c6a91feed03'
JOIN_MANIFEST_SHA256 = '73af8822508ce95f5a6765ba0dd3949b58e0cbc8df8cce8301b313337a722e17'
PR60_FREEZE_SHA256 = '9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d'
PARENT_FREEZE_SHA256 = '4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e'
SIMULATOR_READY_SHA256 = '973692b0c83e8068f4623d7e47168f40c5cd8d3da85c7a66dac86710259c40b0'
PACKET_FROZEN_SHA256 = '0b6ea2acf23698316551e5f64dfe700b95b7f1003cb143ed405b61be708547bb'
PACKET_EMPTY_SHA256 = '1cf857c660a5f08c8a13535221b7208a3edb336c0338713b8484bd498711db83'

CODE_PINS = {
    'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/orchestrator.py':
        '296cfe64ff24c2fad0437ce9a9ec11458f557ee94ee900bd621160dc283fa597',
    'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/tests/test_orchestrator.py':
        '0877f7d142ea04ee568a81bf878d8b13ebab88076b75d59aa254bdd04ae970b3',
    'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/EXPERIMENT_SPEC.md':
        '33806f416c7c21acebbd0b32e632ded7567d5bccb48f2af5f8c2c57270a4517a',
    'kalshi_q6s5_kxmlbspread_feequue_lab_20260925/orchestrator.py':
        'e224686a1bbe4173f00e62c3d2cba78a3c48eecef45ed77c678564def9d5bbfc',
    'kalshi_feebook_lab_20260922/feebook.py':
        'eaf5aac7126efcd574c972fa77438c4118d44d50acafa17c504bdd48768bebe7',
    'kalshi_feebook_lab_20260922/series_fee_table.stub.json':
        '600d56beda64c2edd9af2c9d220398ff1a7158dba140603a42f7cb7f95212384',
    'kalshi_rails_lab_20260922/rails.py':
        '834386506dd72210d77ee063d4a96248d76ce09a4be6ce771b9609337d3388e1',
    'kalshi_r2p1_hygiene_000_lab_20260922/hygiene.py':
        '65310a88ec7602a3fa2e50f2444e64c431dd29ef648992cb7861a5b74ca3b69f',
    'kalshi_q6s5_kxmlbspread_game_phase_settled_tape_lab_20261001/orchestrator.py':
        'c6c4c0a13be65e51250c011cca58c22a000e0d2cc65163520a3ad719a1646521',
}

NAMED_PINS = {
    'Q6S5_PR60_SCORABILITY_authentic_pins_2026-10-02.tgz': BUNDLE_SHA256,
    'CONDUCTOR_ACCEPT_VARIANTS_Q6S5_PR60_SCORABILITY_FREEZE_2026-10-02.json': ACCEPT_SHA256,
    'lab/governance/astra/packets/VARIANTS_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SCORABILITY_FREEZE_2026-10-02.md': FREEZE_SHA256,
    'lab/governance/astra/packets/VARIANTS_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SCORABILITY_FREEZE_2026-10-02.json': FREEZE_JSON_SHA256,
    'lab/governance/astra/packets/Q6S5_PR60_SCORABILITY/MANIFEST.sha256': PACKET_MANIFEST_SHA256,
    'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/SOURCE_PINS.json': TAPE_SOURCE_PINS_SHA256,
    'lab/astra-capture/q6s5-kxmlbspread/settlement_only_2026-10-02/COLLECTOR_READY_SETTLEMENT_ONLY.json': READY_SHA256,
    'lab/astra-capture/q6s5-kxmlbspread/settlement_only_2026-10-02/DIGESTS.txt': DIGESTS_SHA256,
    'lab/astra-science/kalshi_q6s5_kxmlbspread_strategy_fill_settled_run_20261002/outputs/SETTLEMENT_JOIN_MANIFEST_SEP25.json': JOIN_MANIFEST_SHA256,
    'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md': PR60_FREEZE_SHA256,
    'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md': PARENT_FREEZE_SHA256,
    'lab/governance/astra/packets/SIMULATOR_READY_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SETTLED_2026-10-02.json': SIMULATOR_READY_SHA256,
    'lab/governance/astra/packets/Q6S5_PR60_SCORABILITY/FROZEN_EXPERIMENT.json': PACKET_FROZEN_SHA256,
    'lab/governance/astra/packets/Q6S5_PR60_SCORABILITY/EMPTY_RESULTS.json': PACKET_EMPTY_SHA256,
}

LABELS = {
    'evidence_class': 'IN_SAMPLE_DEV / HISTORICAL_REPLAY',
    'family_size': 1,
    'verdict_domain': 'ITERATE|INCONCLUSIVE',
    'counts_toward_keep': False,
    'promote': False,
    'fills_are_MODEL': True,
    'fee': 'CACHE_NOT_R1P1',
    'accept_sha256': ACCEPT_SHA256,
    'freeze_sha256': FREEZE_SHA256,
    'A1_null_reason': 'STALE_BIN_EMPTY',
    'live_promotion': False,
    'counted_as_experiment_pnl': False,
    'verdict': None,
}

_TAPE = None


def _split_manifest_line(line):
    digest, rel = line.split('  ', 1)
    return digest, rel.strip()


def check_pin(path, expected):
    refuse_sqlite_path(path)
    got = sha256_file(path)
    if got != expected:
        raise PinMismatch(str(path))
    return got


def _manifest_paths(manifest_path, root, boundary=None):
    found = {}
    limit = (boundary or root).resolve()
    for line in manifest_path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = _split_manifest_line(line)
        target = (root / rel).resolve()
        if limit not in target.parents and target != limit:
            raise PinMismatch(rel)
        check_pin(target, digest)
        found[rel] = digest
    return found


def verify_manifest():
    """Rehash every pins/MANIFEST entry and the named freeze pins."""
    manifest = PINS / 'MANIFEST.sha256'
    found = _manifest_paths(manifest, PINS)
    for rel, expected in NAMED_PINS.items():
        if found.get(rel) != expected:
            raise PinMismatch(rel)
        check_pin(PINS / rel, expected)
    bundle = _manifest_paths(PINS / 'BUNDLE_MANIFEST.sha256', PINS)
    if bundle != {key: value for key, value in found.items() if key in bundle}:
        for rel, digest in bundle.items():
            if found.get(rel) != digest:
                raise PinMismatch(rel)
    packet = PINS / 'lab/governance/astra/packets/Q6S5_PR60_SCORABILITY'
    _manifest_paths(packet / 'MANIFEST.sha256', packet, boundary=PINS)
    for rel, expected in CODE_PINS.items():
        repo = REPO_ROOT / rel
        vendored = PINS / 'pr60s_main' / rel
        check_pin(repo, expected)
        check_pin(vendored, expected)
    admitted = REPO_ROOT / 'lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json'
    if admitted.exists():
        raise LabError('panel_admitted')
    return found


def read_pinned(rel):
    verify_manifest()
    path = PINS / rel
    expected = NAMED_PINS.get(rel)
    if expected is None:
        text = (PINS / 'MANIFEST.sha256').read_text().splitlines()
        for line in text:
            digest, name = _split_manifest_line(line)
            if name == rel:
                expected = digest
                break
    if expected is None:
        raise PinMismatch(rel)
    check_pin(path, expected)
    return path.read_bytes()


def _load_requests(path, excluded):
    ends = {ticker: [] for ticker in UNIVERSE}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        ticker = row.get('ticker')
        stamp = row.get('ts_utc')
        if ticker not in set(UNIVERSE):
            continue
        if in_admit1_window(stamp):
            excluded[0] += 1
            continue
        ends[ticker].append(stamp)
    tape_ends = {}
    for ticker, stamps in ends.items():
        if not stamps:
            raise LabError('tape end missing')
        tape_ends[ticker] = min(stamps)
    return tape_ends


def load_tape():
    """Read SOURCE_PINS inputs after the sha check. Sep-24 bytes are not parsed."""
    global _TAPE
    if _TAPE is not None:
        return _TAPE
    verify_manifest()
    source_rel = 'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/SOURCE_PINS.json'
    check_pin(PINS / source_rel, TAPE_SOURCE_PINS_SHA256)
    source = json.loads((PINS / source_rel).read_text())
    inputs = {}
    inputs.update(source['inputs_core'])
    inputs.update(source['inputs_raw'])
    for rel, digest in inputs.items():
        check_pin(PINS / rel, digest)
    snapshots = []
    market_gets = []
    prints = []
    excluded = [0]
    ignored_undated = 0
    for rel in sorted(inputs):
        path = PINS / rel
        if '/orderbooks/' in rel:
            stamped = stamp_from_name(path.name)
            if stamped is None:
                ignored_undated += 1
                continue
            iso, ticker = stamped
            if ticker not in set(UNIVERSE):
                continue
            if in_admit1_window(iso):
                excluded[0] += 1
                continue
            payload = json.loads(path.read_text())
            snapshots.append({
                'ticker': ticker,
                'captured_utc': iso,
                'orderbook_fp': payload['orderbook_fp'],
                'path': rel,
            })
        elif '/markets/' in rel and '/raw/markets/' in rel:
            stamped = stamp_from_name(path.name)
            if stamped is None:
                ignored_undated += 1
                continue
            iso, ticker = stamped
            if ticker not in set(UNIVERSE):
                continue
            if in_admit1_window(iso):
                excluded[0] += 1
                continue
            payload = json.loads(path.read_text())
            market = payload['market']
            if market['ticker'] != ticker:
                raise LabError('ticker')
            market_gets.append({
                'ticker': ticker,
                'captured_utc': iso,
                'status': market['status'],
                'path': rel,
            })
        elif '/raw/trades/' in rel:
            ticker = path.parent.name
            if ticker not in set(UNIVERSE):
                continue
            payload = json.loads(path.read_text())
            for trade in payload.get('trades') or []:
                created = trade['created_time']
                if in_admit1_window(created):
                    excluded[0] += 1
                    continue
                if trade['ticker'] != ticker:
                    raise LabError('ticker')
                prints.append({
                    'count_fp': trade['count_fp'],
                    'created_time': created,
                    'is_block_trade': trade['is_block_trade'],
                    'no_price_dollars': trade['no_price_dollars'],
                    'taker_book_side': trade['taker_book_side'],
                    'taker_outcome_side': trade['taker_outcome_side'],
                    'taker_side': trade['taker_side'],
                    'ticker': trade['ticker'],
                    'trade_id': trade['trade_id'],
                    'yes_price_dollars': trade['yes_price_dollars'],
                })
    requests_rel = 'lab/astra-capture/q6s5-kxmlbspread/trades_fills_2026-09-25/requests.jsonl'
    tape_ends = _load_requests(PINS / requests_rel, excluded)
    _TAPE = {
        'snapshots': snapshots,
        'market_gets': market_gets,
        'tape_ends': tape_ends,
        'prints': prints,
        'excluded_admit1_window_n': excluded[0],
        'ignored_undated_n': ignored_undated,
    }
    return _TAPE


def _envelope(kind, body):
    return {
        'kind': kind,
        'labels': LABELS,
        'rows': body['rows'],
        'counts': body['counts'],
    }


def run_quote_fill(tape=None):
    """Quotes and fills from the tape only. The settlement folder stays closed."""
    if tape is None:
        tape = load_tape()
    quotes = tape_quotes.build_quotes(
        tape['snapshots'], tape['market_gets'], tape['tape_ends'], trades=None,
    )
    fills = fill_engine.run_fills(quotes, tape['prints'])
    quote_doc = _envelope('quotes', quotes)
    fill_doc = _envelope('fills', fills)
    quote_bytes = canonical_bytes(quote_doc)
    fill_bytes = canonical_bytes(fill_doc)
    return {
        'quote_document': quote_doc,
        'fill_document': fill_doc,
        'quote_bytes': quote_bytes,
        'fill_bytes': fill_bytes,
        'quotes_sha256': hashlib.sha256(quote_bytes).hexdigest(),
        'fills_sha256': hashlib.sha256(fill_bytes).hexdigest(),
        'quote_counts': quotes['counts'],
        'fill_counts': fills['counts'],
        'excluded_admit1_window_n': tape['excluded_admit1_window_n'],
    }


def settlement_dir():
    return PINS / 'lab/astra-capture/q6s5-kxmlbspread/settlement_only_2026-10-02'


def join_manifest_path():
    return (
        PINS / 'lab/astra-science/kalshi_q6s5_kxmlbspread_strategy_fill_settled_run_20261002'
        / 'outputs/SETTLEMENT_JOIN_MANIFEST_SEP25.json'
    )


def run_join(fill_bytes, fills_sha256):
    """Join after fills are frozen. Folder digest is checked here, then the manifest."""
    verify_manifest()
    folder = settlement_dir()
    if settled_join.settlement_folder_digest(folder) != FOLDER_DIGEST_SHA256:
        raise PinMismatch('settlement folder')
    check_pin(folder / 'COLLECTOR_READY_SETTLEMENT_ONLY.json', READY_SHA256)
    check_pin(folder / 'DIGESTS.txt', DIGESTS_SHA256)
    manifest_path = join_manifest_path()
    check_pin(manifest_path, JOIN_MANIFEST_SHA256)
    joined = settled_join.settled_join(fill_bytes, fills_sha256, folder)
    settled_join.assert_join_manifest(joined, manifest_path.read_bytes())
    return joined


def structural_counts(tape=None):
    """Placement and fill counts. PnL, ROI, and arm values stay null."""
    packed = run_quote_fill(tape)
    quotes = packed['quote_counts']
    fills = packed['fill_counts']
    return {
        'labels': LABELS,
        'n_books': quotes['n_books'],
        'eligible_placements': quotes['eligible_placements'],
        'crossed_or_locked_n': quotes['crossed_or_locked_n'],
        'empty_side_n': quotes['empty_side_n'],
        'fresh_n': quotes['fresh_n'],
        'stale_n': quotes['stale_n'],
        'requested_maker_contracts': quotes['requested_maker_contracts'],
        'requested_taker_contracts': quotes['requested_taker_contracts'],
        'prints_in': fills['prints_in'],
        'excluded_block_n': fills['excluded_block_n'],
        'excluded_native_conflict_n': fills['excluded_native_conflict_n'],
        'excluded_price_inconsistent_n': fills['excluded_price_inconsistent_n'],
        'maker_filled_n': fills['maker_filled_n'],
        'maker_unfilled_n': fills['maker_unfilled_n'],
        'taker_filled_n': fills['taker_filled_n'],
        'taker_unfilled_n': fills['taker_unfilled_n'],
        'excluded_admit1_window_n': packed['excluded_admit1_window_n'],
        'quotes_sha256': packed['quotes_sha256'],
        'fills_sha256': packed['fills_sha256'],
        'pnl': None,
        'roi': None,
        'Q6S5A0_maker_vs_taker_roi_delta': None,
        'Q6S5A1_fresh_vs_stale_gap': None,
        'A1_null_reason': 'STALE_BIN_EMPTY',
        'counts_toward_keep': False,
        'verdict': None,
    }


def refuse_capture(path):
    refuse_sqlite_path(path)
    raise CaptureSqliteRefused(path)
