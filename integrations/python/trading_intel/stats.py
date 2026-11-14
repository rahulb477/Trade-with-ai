"""Descriptive statistics with the honesty requirements of this repository.

Every function that returns an estimate can also return its uncertainty, and
the module deliberately exposes ``wilson_interval`` because small-sample hit
rates are the single most over-reported number in trading.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple


def mean(values: Sequence[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def median(values: Sequence[float]) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def stdev(values: Sequence[float], sample: bool = True) -> Optional[float]:
    """Standard deviation. ``sample=True`` uses n-1 (the usual choice for returns)."""
    n = len(values)
    if n < 2:
        return None
    m = sum(values) / n
    var = sum((v - m) ** 2 for v in values) / ((n - 1) if sample else n)
    return math.sqrt(var)


def percentile(values: Sequence[float], p: float) -> Optional[float]:
    """Linear-interpolated percentile. ``p`` in [0, 100]."""
    if not values:
        return None
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (p / 100.0) * (len(ordered) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return ordered[low]
    frac = rank - low
    return ordered[low] * (1 - frac) + ordered[high] * frac


def quantiles(values: Sequence[float], count: int = 5) -> List[Optional[float]]:
    """Split into ``count`` buckets; returns the boundary values."""
    if count < 2:
        raise ValueError("count must be >= 2")
    return [percentile(values, 100.0 * i / count) for i in range(count + 1)]


def correlation(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    """Pearson correlation. Returns ``None`` if undefined (n<3 or zero variance)."""
    if len(xs) != len(ys):
        raise ValueError("series must be the same length")
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def returns(prices: Sequence[float], log: bool = False) -> List[float]:
    """Simple (or log) returns from a price series."""
    out: List[float] = []
    for i in range(1, len(prices)):
        prev = prices[i - 1]
        if prev == 0:
            continue
        out.append(math.log(prices[i] / prev) if log else (prices[i] - prev) / prev)
    return out


def sharpe(returns_: Sequence[float], periods_per_year: int = 252,
           risk_free: float = 0.0) -> Optional[float]:
    """Annualised Sharpe ratio on periodic returns.

    Requires at least 30 observations; below that it returns ``None`` because
    the estimate is dominated by noise.
    """
    if len(returns_) < 30:
        return None
    sd = stdev(returns_)
    # a near-zero standard deviation is a numerical artefact of a constant
    # series, not a real risk estimate; refuse rather than return a huge ratio
    if sd is None or sd < 1e-12:
        return None
    excess = [r - risk_free / periods_per_year for r in returns_]
    return (sum(excess) / len(excess)) / sd * math.sqrt(periods_per_year)


def sortino(returns_: Sequence[float], periods_per_year: int = 252,
            target: float = 0.0) -> Optional[float]:
    """Annualised Sortino ratio (downside deviation only)."""
    if len(returns_) < 30:
        return None
    excess = [r - target for r in returns_]
    downside = [min(0.0, r) ** 2 for r in excess]
    dd = math.sqrt(sum(downside) / len(downside))
    if dd == 0:
        return None
    return (sum(excess) / len(excess)) / dd * math.sqrt(periods_per_year)


def max_drawdown(equity: Sequence[float]) -> float:
    """Maximum peak-to-trough decline as a positive fraction."""
    if not equity:
        return 0.0
    peak = equity[0]
    worst = 0.0
    for value in equity:
        peak = max(peak, value)
        if peak > 0:
            worst = max(worst, (peak - value) / peak)
    return worst


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for a proportion.

    Preferred over the normal approximation because it behaves sensibly at
    small n and near 0 or 1 — exactly the regime trading samples live in.

    >>> wilson_interval(5, 10)
    (0.2366..., 0.7633...)
    """
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must be between 0 and trials")
    p = successes / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    margin = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denom
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def standard_error_of_mean(values: Sequence[float]) -> Optional[float]:
    sd = stdev(values)
    if sd is None or not values:
        return None
    return sd / math.sqrt(len(values))


def mean_ci(values: Sequence[float], z: float = 1.96) -> Optional[Tuple[float, float]]:
    """Normal-approximation CI for the mean (use n >= 30, or read it as indicative)."""
    se = standard_error_of_mean(values)
    m = mean(values)
    if se is None or m is None:
        return None
    return (m - z * se, m + z * se)


def multiple_testing_probability(tests: int, alpha: float = 0.05) -> float:
    """Chance of at least one false positive when running ``tests`` independent tests."""
    if tests < 0:
        raise ValueError("tests must be >= 0")
    return 1.0 - (1.0 - alpha) ** tests


def describe(values: Sequence[float]) -> Dict[str, Optional[float]]:
    """A summary block that always contains n, so a number is never context-free."""
    return {
        "n": len(values),
        "mean": mean(values),
        "median": median(values),
        "stdev": stdev(values),
        "p05": percentile(values, 5),
        "p25": percentile(values, 25),
        "p75": percentile(values, 75),
        "p95": percentile(values, 95),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }
