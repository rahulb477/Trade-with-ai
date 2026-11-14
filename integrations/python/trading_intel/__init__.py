"""trading_intel — dependency-free trading research primitives.

Pure standard library. No network calls. No telemetry. Undefined values are
returned as ``None`` rather than guessed.

Typical use::

    from trading_intel import indicators as ind, risk, metrics

    rsi = ind.rsi(closes, 14)
    plan = risk.size_position(equity=500_000, risk_pct=0.75, entry=1204, stop=1186)
"""

from . import (
    indicators,
    patterns,
    risk,
    sizing,
    metrics,
    stats,
    simulate,
    backtest,
    timeframes,
    validation,
    observation,
)

__version__ = "1.0.0"

__all__ = [
    "indicators",
    "patterns",
    "risk",
    "sizing",
    "metrics",
    "stats",
    "simulate",
    "backtest",
    "timeframes",
    "validation",
    "observation",
    "__version__",
]
