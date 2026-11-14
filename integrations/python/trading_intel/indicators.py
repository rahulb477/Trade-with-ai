"""Technical indicators, pure standard library.

Conventions used throughout:

* Every function takes plain sequences (lists/tuples) of floats.
* A result is a list the same length as the input.
* Values that cannot be computed (insufficient history, undefined division)
  are ``None`` — never 0, never an approximation.
* Wilder smoothing is used where the original definition specifies it
  (RSI, ATR, ADX). EMA seeds with the SMA of the first ``period`` values.
"""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Sequence, Tuple

Number = Optional[float]


def _as_list(values: Iterable[float]) -> List[float]:
    return [float(v) for v in values]


# --------------------------------------------------------------------------
# Moving averages
# --------------------------------------------------------------------------
def sma(values: Sequence[float], period: int) -> List[Number]:
    """Simple moving average. ``None`` until ``period`` values exist."""
    if period <= 0:
        raise ValueError("period must be positive")
    vals = _as_list(values)
    out: List[Number] = [None] * len(vals)
    if len(vals) < period:
        return out
    window = sum(vals[:period])
    out[period - 1] = window / period
    for i in range(period, len(vals)):
        window += vals[i] - vals[i - period]
        out[i] = window / period
    return out


def ema(values: Sequence[float], period: int) -> List[Number]:
    """Exponential moving average, seeded with the SMA of the first ``period``."""
    if period <= 0:
        raise ValueError("period must be positive")
    vals = _as_list(values)
    out: List[Number] = [None] * len(vals)
    if len(vals) < period:
        return out
    alpha = 2.0 / (period + 1.0)
    seed = sum(vals[:period]) / period
    out[period - 1] = seed
    prev = seed
    for i in range(period, len(vals)):
        prev = alpha * vals[i] + (1.0 - alpha) * prev
        out[i] = prev
    return out


def _wilder_smooth(values: Sequence[float], period: int) -> List[Number]:
    vals = _as_list(values)
    out: List[Number] = [None] * len(vals)
    if len(vals) < period:
        return out
    prev = sum(vals[:period]) / period
    out[period - 1] = prev
    for i in range(period, len(vals)):
        prev = (prev * (period - 1) + vals[i]) / period
        out[i] = prev
    return out


# --------------------------------------------------------------------------
# RSI
# --------------------------------------------------------------------------
def rsi(closes: Sequence[float], period: int = 14) -> List[Number]:
    """Relative Strength Index with Wilder smoothing.

    Edge cases: all gains -> 100; all losses -> 0; both zero -> 50 (flagged
    by convention, since the oscillator is undefined for a flat series).
    """
    if period <= 0:
        raise ValueError("period must be positive")
    vals = _as_list(closes)
    n = len(vals)
    out: List[Number] = [None] * n
    if n < period + 1:
        return out

    gains = [0.0] * n
    losses = [0.0] * n
    for i in range(1, n):
        change = vals[i] - vals[i - 1]
        if change > 0:
            gains[i] = change
        elif change < 0:
            losses[i] = -change

    avg_gain = sum(gains[1 : period + 1]) / period
    avg_loss = sum(losses[1 : period + 1]) / period

    def _rsi_from(ag: float, al: float) -> float:
        if al == 0.0 and ag == 0.0:
            return 50.0
        if al == 0.0:
            return 100.0
        rs = ag / al
        return 100.0 - 100.0 / (1.0 + rs)

    out[period] = _rsi_from(avg_gain, avg_loss)
    for i in range(period + 1, n):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        out[i] = _rsi_from(avg_gain, avg_loss)
    return out


# --------------------------------------------------------------------------
# MACD
# --------------------------------------------------------------------------
def macd(
    closes: Sequence[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> Tuple[List[Number], List[Number], List[Number]]:
    """Return ``(macd_line, signal_line, histogram)``."""
    if fast >= slow:
        raise ValueError("fast period must be shorter than slow period")
    vals = _as_list(closes)
    n = len(vals)
    ema_fast = ema(vals, fast)
    ema_slow = ema(vals, slow)

    macd_line: List[Number] = [None] * n
    for i in range(n):
        f, s = ema_fast[i], ema_slow[i]
        if f is not None and s is not None:
            macd_line[i] = f - s

    # signal = EMA of the defined part of the macd line
    first = next((i for i, v in enumerate(macd_line) if v is not None), None)
    signal_line: List[Number] = [None] * n
    hist: List[Number] = [None] * n
    if first is None or n - first < signal:
        return macd_line, signal_line, hist

    defined = macd_line[first:]
    sig = ema([v for v in defined], signal)  # type: ignore[list-item]
    for offset, value in enumerate(sig):
        signal_line[first + offset] = value
        if value is not None and macd_line[first + offset] is not None:
            hist[first + offset] = macd_line[first + offset] - value  # type: ignore[operator]
    return macd_line, signal_line, hist


# --------------------------------------------------------------------------
# True range / ATR
# --------------------------------------------------------------------------
def true_range(
    highs: Sequence[float], lows: Sequence[float], closes: Sequence[float]
) -> List[Number]:
    """True range, incorporating gaps. First bar's TR is high-low."""
    h, l, c = _as_list(highs), _as_list(lows), _as_list(closes)
    if not (len(h) == len(l) == len(c)):
        raise ValueError("highs, lows and closes must be the same length")
    out: List[Number] = [None] * len(h)
    if not h:
        return out
    out[0] = h[0] - l[0]
    for i in range(1, len(h)):
        out[i] = max(
            h[i] - l[i],
            abs(h[i] - c[i - 1]),
            abs(l[i] - c[i - 1]),
        )
    return out


def atr(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int = 14,
) -> List[Number]:
    """Average True Range with Wilder smoothing."""
    tr = true_range(highs, lows, closes)
    vals = [v if v is not None else 0.0 for v in tr]
    return _wilder_smooth(vals, period)


# --------------------------------------------------------------------------
# ADX / DI
# --------------------------------------------------------------------------
def adx(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int = 14,
) -> Tuple[List[Number], List[Number], List[Number]]:
    """Return ``(adx, plus_di, minus_di)``."""
    h, l, c = _as_list(highs), _as_list(lows), _as_list(closes)
    n = len(h)
    if not (len(h) == len(l) == len(c)):
        raise ValueError("highs, lows and closes must be the same length")

    plus_dm = [0.0] * n
    minus_dm = [0.0] * n
    for i in range(1, n):
        up = h[i] - h[i - 1]
        down = l[i - 1] - l[i]
        plus_dm[i] = up if (up > down and up > 0) else 0.0
        minus_dm[i] = down if (down > up and down > 0) else 0.0

    tr = [v if v is not None else 0.0 for v in true_range(h, l, c)]

    s_tr = _wilder_smooth(tr, period)
    s_plus = _wilder_smooth(plus_dm, period)
    s_minus = _wilder_smooth(minus_dm, period)

    plus_di: List[Number] = [None] * n
    minus_di: List[Number] = [None] * n
    dx: List[Number] = [None] * n
    for i in range(n):
        if s_tr[i] and s_tr[i] != 0 and s_plus[i] is not None and s_minus[i] is not None:
            pdi = 100.0 * s_plus[i] / s_tr[i]  # type: ignore[operator]
            mdi = 100.0 * s_minus[i] / s_tr[i]  # type: ignore[operator]
            plus_di[i] = pdi
            minus_di[i] = mdi
            denom = pdi + mdi
            if denom != 0:
                dx[i] = 100.0 * abs(pdi - mdi) / denom

    first = next((i for i, v in enumerate(dx) if v is not None), None)
    adx_line: List[Number] = [None] * n
    if first is None or n - first < period:
        return adx_line, plus_di, minus_di

    # ADX = Wilder smoothing of DX, seeded with the mean of the first `period` DX values
    window = [dx[i] for i in range(first, first + period)]
    if any(v is None for v in window):
        return adx_line, plus_di, minus_di
    prev = sum(window) / period  # type: ignore[arg-type]
    adx_line[first + period - 1] = prev
    for i in range(first + period, n):
        if dx[i] is None:
            continue
        prev = (prev * (period - 1) + dx[i]) / period  # type: ignore[operator]
        adx_line[i] = prev
    return adx_line, plus_di, minus_di


# --------------------------------------------------------------------------
# Bollinger Bands
# --------------------------------------------------------------------------
def bollinger_bands(
    closes: Sequence[float], period: int = 20, num_std: float = 2.0
) -> Tuple[List[Number], List[Number], List[Number]]:
    """Return ``(upper, middle, lower)`` using population standard deviation."""
    vals = _as_list(closes)
    n = len(vals)
    middle = sma(vals, period)
    upper: List[Number] = [None] * n
    lower: List[Number] = [None] * n
    for i in range(n):
        if middle[i] is None:
            continue
        window = vals[i - period + 1 : i + 1]
        mean = middle[i]  # type: ignore[assignment]
        var = sum((x - mean) ** 2 for x in window) / period
        sd = math.sqrt(var)
        upper[i] = mean + num_std * sd
        lower[i] = mean - num_std * sd
    return upper, middle, lower


def bollinger_bandwidth(
    closes: Sequence[float], period: int = 20, num_std: float = 2.0
) -> List[Number]:
    """``(upper - lower) / middle`` — a scale-free volatility measure."""
    upper, middle, lower = bollinger_bands(closes, period, num_std)
    out: List[Number] = [None] * len(closes)
    for i, (u, m, lo) in enumerate(zip(upper, middle, lower)):
        if u is not None and m not in (None, 0) and lo is not None:
            out[i] = (u - lo) / m  # type: ignore[operator]
    return out


# --------------------------------------------------------------------------
# Stochastic RSI
# --------------------------------------------------------------------------
def stochastic_rsi(
    closes: Sequence[float],
    rsi_period: int = 14,
    stoch_period: int = 14,
    k: int = 3,
    d: int = 3,
) -> Tuple[List[Number], List[Number]]:
    """Return ``(percent_k, percent_d)`` scaled to 0-100."""
    r = rsi(closes, rsi_period)
    n = len(r)
    raw: List[Number] = [None] * n
    for i in range(n):
        if i < stoch_period - 1 or r[i] is None:
            continue
        window = [r[j] for j in range(i - stoch_period + 1, i + 1)]
        if any(v is None for v in window):
            continue
        lo = min(window)  # type: ignore[arg-type]
        hi = max(window)  # type: ignore[arg-type]
        if hi == lo:
            continue  # undefined: flat RSI window
        raw[i] = (r[i] - lo) / (hi - lo) * 100.0  # type: ignore[operator]

    def _smooth(series: List[Number], length: int) -> List[Number]:
        out: List[Number] = [None] * len(series)
        for i in range(len(series)):
            window = series[i - length + 1 : i + 1] if i >= length - 1 else []
            if len(window) == length and all(v is not None for v in window):
                out[i] = sum(window) / length  # type: ignore[arg-type]
        return out

    pct_k = _smooth(raw, k)
    pct_d = _smooth(pct_k, d)
    return pct_k, pct_d


# --------------------------------------------------------------------------
# OBV
# --------------------------------------------------------------------------
def obv(closes: Sequence[float], volumes: Sequence[float]) -> List[Number]:
    """On-Balance Volume. The starting level is arbitrary; only the shape matters."""
    c, v = _as_list(closes), _as_list(volumes)
    if len(c) != len(v):
        raise ValueError("closes and volumes must be the same length")
    out: List[Number] = [None] * len(c)
    if not c:
        return out
    running = 0.0
    out[0] = running
    for i in range(1, len(c)):
        if c[i] > c[i - 1]:
            running += v[i]
        elif c[i] < c[i - 1]:
            running -= v[i]
        out[i] = running
    return out


# --------------------------------------------------------------------------
# VWAP
# --------------------------------------------------------------------------
def vwap(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    volumes: Sequence[float],
    reset_index: int = 0,
) -> List[Number]:
    """Cumulative volume-weighted average price, resetting at ``reset_index``."""
    h, l, c, v = _as_list(highs), _as_list(lows), _as_list(closes), _as_list(volumes)
    if not (len(h) == len(l) == len(c) == len(v)):
        raise ValueError("all inputs must be the same length")
    if not (0 <= reset_index < len(h)):
        raise ValueError("reset_index out of range")
    out: List[Number] = [None] * len(h)
    pv = 0.0
    vol = 0.0
    for i in range(reset_index, len(h)):
        tp = (h[i] + l[i] + c[i]) / 3.0
        pv += tp * v[i]
        vol += v[i]
        if vol > 0:
            out[i] = pv / vol
    return out


# --------------------------------------------------------------------------
# Supertrend
# --------------------------------------------------------------------------
def supertrend(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int = 10,
    multiplier: float = 3.0,
) -> Tuple[List[Number], List[Optional[str]]]:
    """Return ``(line, direction)`` where direction is ``"up"`` or ``"down"``.

    The band-carrying rule follows the common published formulation: a final
    upper band only tightens while price stays below it, and vice versa.
    """
    h, l, c = _as_list(highs), _as_list(lows), _as_list(closes)
    if not (len(h) == len(l) == len(c)):
        raise ValueError("highs, lows and closes must be the same length")
    a = atr(h, l, c, period)
    n = len(h)
    line: List[Number] = [None] * n
    direction: List[Optional[str]] = [None] * n

    final_upper: Optional[float] = None
    final_lower: Optional[float] = None
    trend: Optional[str] = None

    for i in range(n):
        if a[i] is None:
            continue
        mid = (h[i] + l[i]) / 2.0
        basic_upper = mid + multiplier * a[i]  # type: ignore[operator]
        basic_lower = mid - multiplier * a[i]  # type: ignore[operator]

        if final_upper is None or final_lower is None:
            final_upper, final_lower = basic_upper, basic_lower
            trend = "up" if c[i] >= final_lower else "down"
        else:
            if basic_upper < final_upper or c[i - 1] > final_upper:
                final_upper = basic_upper
            if basic_lower > final_lower or c[i - 1] < final_lower:
                final_lower = basic_lower

            if trend == "up" and c[i] < final_lower:
                trend = "down"
            elif trend == "down" and c[i] > final_upper:
                trend = "up"

        line[i] = final_lower if trend == "up" else final_upper
        direction[i] = trend
    return line, direction


# --------------------------------------------------------------------------
# Ichimoku
# --------------------------------------------------------------------------
def ichimoku(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    conversion: int = 9,
    base: int = 26,
    span_b: int = 52,
) -> dict:
    """Return the Ichimoku components (leading spans are *not* shifted here)."""
    h, l, c = _as_list(highs), _as_list(lows), _as_list(closes)
    if not (len(h) == len(l) == len(c)):
        raise ValueError("highs, lows and closes must be the same length")

    def _mid(length: int) -> List[Number]:
        out: List[Number] = [None] * len(h)
        for i in range(len(h)):
            if i >= length - 1:
                out[i] = (max(h[i - length + 1 : i + 1]) + min(l[i - length + 1 : i + 1])) / 2.0
        return out

    tenkan = _mid(conversion)
    kijun = _mid(base)
    span_a: List[Number] = [None] * len(h)
    for i in range(len(h)):
        if tenkan[i] is not None and kijun[i] is not None:
            span_a[i] = (tenkan[i] + kijun[i]) / 2.0  # type: ignore[operator]
    span_bb = _mid(span_b)

    shift = base
    span_a_shifted: List[Number] = [None] * len(h)
    span_b_shifted: List[Number] = [None] * len(h)
    for i in range(len(h)):
        if i + shift < len(h):
            span_a_shifted[i + shift] = span_a[i]
            span_b_shifted[i + shift] = span_bb[i]

    chikou: List[Number] = [None] * len(h)
    for i in range(len(h)):
        if i - shift >= 0:
            chikou[i - shift] = c[i]

    return {
        "tenkan": tenkan,
        "kijun": kijun,
        "senkou_a": span_a_shifted,
        "senkou_b": span_b_shifted,
        "chikou": chikou,
    }


# --------------------------------------------------------------------------
# CCI / ROC / MFI
# --------------------------------------------------------------------------
def cci(
    highs: Sequence[float], lows: Sequence[float], closes: Sequence[float], period: int = 20
) -> List[Number]:
    """Commodity Channel Index using mean absolute deviation."""
    h, l, c = _as_list(highs), _as_list(lows), _as_list(closes)
    if not (len(h) == len(l) == len(c)):
        raise ValueError("highs, lows and closes must be the same length")
    tp = [(h[i] + l[i] + c[i]) / 3.0 for i in range(len(h))]
    ma = sma(tp, period)
    out: List[Number] = [None] * len(tp)
    for i in range(len(tp)):
        if ma[i] is None:
            continue
        window = tp[i - period + 1 : i + 1]
        md = sum(abs(x - ma[i]) for x in window) / period  # type: ignore[operator]
        if md == 0:
            continue  # undefined
        out[i] = (tp[i] - ma[i]) / (0.015 * md)  # type: ignore[operator]
    return out


def roc(closes: Sequence[float], period: int = 12) -> List[Number]:
    """Rate of change in percent."""
    vals = _as_list(closes)
    out: List[Number] = [None] * len(vals)
    for i in range(period, len(vals)):
        base = vals[i - period]
        if base == 0:
            continue
        out[i] = 100.0 * (vals[i] - base) / base
    return out


def mfi(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    volumes: Sequence[float],
    period: int = 14,
) -> List[Number]:
    """Money Flow Index (volume-weighted RSI on typical price)."""
    h, l, c, v = _as_list(highs), _as_list(lows), _as_list(closes), _as_list(volumes)
    if not (len(h) == len(l) == len(c) == len(v)):
        raise ValueError("all inputs must be the same length")
    n = len(h)
    tp = [(h[i] + l[i] + c[i]) / 3.0 for i in range(n)]
    flow = [tp[i] * v[i] for i in range(n)]
    out: List[Number] = [None] * n
    for i in range(period, n):
        pos = 0.0
        neg = 0.0
        for j in range(i - period + 1, i + 1):
            if tp[j] > tp[j - 1]:
                pos += flow[j]
            elif tp[j] < tp[j - 1]:
                neg += flow[j]
        if pos == 0.0 and neg == 0.0:
            continue
        if neg == 0.0:
            out[i] = 100.0
        elif pos == 0.0:
            out[i] = 0.0
        else:
            ratio = pos / neg
            out[i] = 100.0 - 100.0 / (1.0 + ratio)
    return out


# --------------------------------------------------------------------------
# Levels
# --------------------------------------------------------------------------
def pivot_points(
    high: float, low: float, close: float, method: str = "classic"
) -> dict:
    """Session pivot levels.

    ``method`` is one of ``classic``, ``fibonacci``, ``camarilla``, ``woodie``.
    """
    rng = high - low
    if method == "classic":
        p = (high + low + close) / 3.0
        levels = {
            "P": p,
            "R1": 2 * p - low,
            "S1": 2 * p - high,
            "R2": p + rng,
            "S2": p - rng,
            "R3": high + 2 * (p - low),
            "S3": low - 2 * (high - p),
        }
    elif method == "fibonacci":
        p = (high + low + close) / 3.0
        levels = {
            "P": p,
            "R1": p + 0.382 * rng,
            "R2": p + 0.618 * rng,
            "R3": p + 1.000 * rng,
            "S1": p - 0.382 * rng,
            "S2": p - 0.618 * rng,
            "S3": p - 1.000 * rng,
        }
    elif method == "camarilla":
        levels = {
            "R1": close + rng * 1.1 / 12,
            "R2": close + rng * 1.1 / 6,
            "R3": close + rng * 1.1 / 4,
            "R4": close + rng * 1.1 / 2,
            "S1": close - rng * 1.1 / 12,
            "S2": close - rng * 1.1 / 6,
            "S3": close - rng * 1.1 / 4,
            "S4": close - rng * 1.1 / 2,
        }
    elif method == "woodie":
        p = (high + low + 2 * close) / 4.0
        levels = {
            "P": p,
            "R1": 2 * p - low,
            "S1": 2 * p - high,
        }
    else:
        raise ValueError(f"unknown pivot method: {method}")
    return levels


def fib_levels(swing_low: float, swing_high: float, direction: str = "up") -> dict:
    """Retracement and extension levels for a swing."""
    if swing_low >= swing_high:
        raise ValueError("swing_low must be below swing_high")
    rng = swing_high - swing_low
    ratios = [0.236, 0.382, 0.5, 0.618, 0.786]
    ext = [1.272, 1.618, 2.0, 2.618]
    if direction == "up":
        levels = {f"retr_{r}": swing_high - r * rng for r in ratios}
        levels.update({f"ext_{r}": swing_low + r * rng for r in ext})
    elif direction == "down":
        levels = {f"retr_{r}": swing_low + r * rng for r in ratios}
        levels.update({f"ext_{r}": swing_high - r * rng for r in ext})
    else:
        raise ValueError("direction must be 'up' or 'down'")
    return levels


def volume_profile(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    volumes: Sequence[float],
    bins: int = 50,
    value_area: float = 0.70,
) -> dict:
    """Volume by price.

    Volume for each bar is distributed proportionally across the price bins it
    spans. Returns the point of control and the value-area boundaries.
    """
    h, l, c, v = _as_list(highs), _as_list(lows), _as_list(closes), _as_list(volumes)
    if not (len(h) == len(l) == len(c) == len(v)):
        raise ValueError("all inputs must be the same length")
    if not h:
        raise ValueError("empty input")
    if bins < 1:
        raise ValueError("bins must be >= 1")

    lo = min(l)
    hi = max(h)
    if hi <= lo:
        raise ValueError("degenerate price range")
    step = (hi - lo) / bins
    counts = [0.0] * bins

    for i in range(len(h)):
        b_lo = int((l[i] - lo) / step)
        b_hi = int((h[i] - lo) / step)
        b_lo = max(0, min(bins - 1, b_lo))
        b_hi = max(0, min(bins - 1, b_hi))
        span = b_hi - b_lo + 1
        share = v[i] / span
        for b in range(b_lo, b_hi + 1):
            counts[b] += share

    total = sum(counts)
    poc_index = max(range(bins), key=lambda i: counts[i])

    # expand around the POC until the target share of volume is included
    included = counts[poc_index]
    left = right = poc_index
    target = total * value_area
    while included < target and (left > 0 or right < bins - 1):
        left_vol = counts[left - 1] if left > 0 else -1.0
        right_vol = counts[right + 1] if right < bins - 1 else -1.0
        if right_vol >= left_vol:
            right += 1
            included += counts[right]
        else:
            left -= 1
            included += counts[left]

    def _price(index: int) -> float:
        return lo + (index + 0.5) * step

    return {
        "poc": _price(poc_index),
        "vah": _price(right) + step / 2.0,
        "val": _price(left) - step / 2.0,
        "bin_width": step,
        "bins": counts,
        "total_volume": total,
    }
