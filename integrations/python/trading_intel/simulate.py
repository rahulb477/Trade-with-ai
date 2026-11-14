"""Simulation utilities: Monte Carlo resampling and synthetic price paths.

Nothing here forecasts. A simulation re-arranges the past; it cannot produce an
outcome that is not in the input series (beyond what the resampling rule allows).
All randomness is seeded so results are reproducible and testable.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


def monte_carlo_trades(
    r_multiples: Sequence[float],
    trades_per_run: int = 100,
    runs: int = 10_000,
    seed: int = 42,
    cost_r: float = 0.0,
    initial_equity: float = 1.0,
    risk_pct: float = 0.01,
) -> Dict[str, object]:
    """Bootstrap a trade sequence with compounding.

    Returns the distribution of ending equity and maximum drawdown across runs.
    Because it resamples the observed set, it *cannot* show a worse streak than
    the sample contains unless the sample is large — state that limitation
    whenever you report these numbers.
    """
    if not r_multiples:
        raise ValueError("need at least one observation to resample")
    if trades_per_run < 1 or runs < 1:
        raise ValueError("trades_per_run and runs must be >= 1")
    rng = random.Random(seed)
    pool = [r - cost_r for r in r_multiples]

    endings: List[float] = []
    drawdowns: List[float] = []

    for _ in range(runs):
        equity = initial_equity
        peak = initial_equity
        worst = 0.0
        for _ in range(trades_per_run):
            r = rng.choice(pool)
            equity += equity * risk_pct * r
            if equity <= 0:
                equity = 0.0
                break
            peak = max(peak, equity)
            worst = max(worst, (peak - equity) / peak)
        endings.append(equity)
        drawdowns.append(worst)

    from . import stats as _stats

    endings_sorted = sorted(endings)
    drawdowns_sorted = sorted(drawdowns)

    def pct(sorted_values: List[float], p: float) -> float:
        if not sorted_values:
            return 0.0
        rank = (p / 100.0) * (len(sorted_values) - 1)
        lo, hi = int(math.floor(rank)), int(math.ceil(rank))
        if lo == hi:
            return sorted_values[lo]
        frac = rank - lo
        return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac

    terminal_loss_fraction = sum(1 for e in endings if e <= 0) / runs

    return {
        "runs": runs,
        "trades_per_run": trades_per_run,
        "seed": seed,
        "cost_r": cost_r,
        "risk_pct": risk_pct,
        "ending_equity_mean": round(sum(endings) / runs, 4),
        "ending_equity_median": round(pct(endings_sorted, 50), 4),
        "ending_equity_p05": round(pct(endings_sorted, 5), 4),
        "ending_equity_p95": round(pct(endings_sorted, 95), 4),
        "max_drawdown_median": round(pct(drawdowns_sorted, 50), 4),
        "max_drawdown_p95": round(pct(drawdowns_sorted, 95), 4),
        "fraction_ruined": round(terminal_loss_fraction, 6),
        "sample_size_used": len(pool),
        "caveats": [
            "resamples the observed set only; unseen tail events are not represented",
            "assumes independence between trades, which is false in clustered regimes",
            "compounding at a fixed risk fraction; real sizing varies",
        ],
    }


def random_walk(
    start: float = 100.0,
    steps: int = 500,
    volatility: float = 0.01,
    drift: float = 0.0,
    seed: int = 7,
) -> List[float]:
    """Synthetic GBM path. For tests and demonstrations only — never data."""
    rng = random.Random(seed)
    prices = [start]
    for _ in range(steps):
        shock = rng.gauss(0.0, 1.0)
        prices.append(prices[-1] * math.exp(drift - 0.5 * volatility**2 + volatility * shock))
    return prices


def synthetic_ohlcv(
    start: float = 100.0,
    bars: int = 300,
    volatility: float = 0.012,
    drift: float = 0.0004,
    seed: int = 11,
    base_volume: float = 1_000_000.0,
) -> Dict[str, List[float]]:
    """Deterministic synthetic OHLCV.

    The series is generated as a random walk with per-bar noise and a
    volume series that rises with absolute returns. It exists so the test
    suite has data that is explicitly not real market history.
    """
    rng = random.Random(seed)
    closes: List[float] = []
    price = start
    for _ in range(bars):
        price *= math.exp(drift - 0.5 * volatility**2 + volatility * rng.gauss(0.0, 1.0))
        closes.append(price)

    opens: List[float] = []
    highs: List[float] = []
    lows: List[float] = []
    volumes: List[float] = []

    prev_close = start
    for close in closes:
        open_ = prev_close + (close - prev_close) * rng.uniform(0.1, 0.5)
        body_high = max(open_, close)
        body_low = min(open_, close)
        wick_up = abs(rng.gauss(0.0, 1.0)) * volatility * close * 0.5
        wick_dn = abs(rng.gauss(0.0, 1.0)) * volatility * close * 0.5
        high = body_high + wick_up
        low = max(0.01, body_low - wick_dn)
        ret = abs(close - prev_close) / prev_close if prev_close else 0.0
        volume = base_volume * (0.6 + 40 * ret) * rng.uniform(0.75, 1.3)
        opens.append(open_)
        highs.append(high)
        lows.append(low)
        volumes.append(volume)
        prev_close = close

    return {
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes,
    }


def bootstrap_ci(
    values: Sequence[float],
    statistic: str = "mean",
    runs: int = 2000,
    seed: int = 42,
    confidence: float = 0.95,
) -> Optional[Dict[str, float]]:
    """Percentile bootstrap CI for the mean or median. ``None`` for n < 5."""
    if len(values) < 5:
        return None
    rng = random.Random(seed)
    from . import stats as _stats

    fn = _stats.mean if statistic == "mean" else _stats.median
    samples: List[float] = []
    n = len(values)
    for _ in range(runs):
        draw = [values[rng.randrange(n)] for _ in range(n)]
        value = fn(draw)
        if value is not None:
            samples.append(value)
    if not samples:
        return None
    samples.sort()
    alpha = (1.0 - confidence) / 2.0 * 100.0

    def pct(p: float) -> float:
        rank = (p / 100.0) * (len(samples) - 1)
        lo, hi = int(math.floor(rank)), int(math.ceil(rank))
        if lo == hi:
            return samples[lo]
        return samples[lo] * (1 - (rank - lo)) + samples[hi] * (rank - lo)

    return {
        "statistic": statistic,
        "point": fn(values),  # type: ignore[assignment]
        "ci_low": pct(alpha),
        "ci_high": pct(100.0 - alpha),
        "confidence": confidence,
        "runs": runs,
        "n": n,
    }
