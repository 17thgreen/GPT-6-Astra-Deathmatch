"""Load the vendored Amendment B script after a sha256 pin check."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

PIN_SHA256 = "049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2"
UNIVERSE_SHA256 = "d8af74515e449b151016105f956c5e54a4fb4eac3ec570364da58f8fe47d8ca6"
SELFTEST_INPUT_SHA256 = "b16ba92bde540a9623f815654bd33b531536aad8b986c4614a08f36dd27cf65e"
SELFTEST_OUTPUT_SHA256 = "0e93e153b7fc03cb996f3200dc576dd770ad638b00a1a0e3ed1e28632b682f23"

LAB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PIN = LAB_ROOT / "pins" / "NH002H_AMENDMENT_B_national_miss.py"

_CACHE: dict[str, object] = {}


class PinMismatch(RuntimeError):
    """Raised when a pinned file's bytes are not the expected sha256."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_national_miss(path: Path | None = None):
    """Import pins/NH002H_AMENDMENT_B_national_miss.py if and only if the sha matches."""
    src = Path(path) if path is not None else DEFAULT_PIN
    data = src.read_bytes()
    digest = sha256_bytes(data)
    if digest != PIN_SHA256:
        raise PinMismatch(digest)
    key = str(src.resolve())
    cached = _CACHE.get(key)
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location("nh002h_amendment_b_national_miss", src)
    if spec is None or spec.loader is None:
        raise PinMismatch("import spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _CACHE[key] = module
    return module
