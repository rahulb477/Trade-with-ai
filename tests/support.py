"""Shared test helpers: deterministic series and a provider stub."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "integrations", "python"))

from trading_intel import simulate  # noqa: E402

FLAT = [100.0] * 30
RISING = [100.0 + i for i in range(40)]
FALLING = [140.0 - i for i in range(40)]


def synthetic(bars=250, seed=5):
    return simulate.synthetic_ohlcv(bars=bars, seed=seed)


def bars_from_closes(closes, spread=1.0):
    """Build OHLC around a close series with a fixed intrabar spread."""
    o = [c for c in closes]
    h = [c + spread for c in closes]
    l = [c - spread for c in closes]
    return {"open": o, "high": h, "low": l, "close": list(closes),
            "volume": [1000.0] * len(closes)}


def assert_series(testcase, series, expected_len):
    testcase.assertEqual(len(series), expected_len)
