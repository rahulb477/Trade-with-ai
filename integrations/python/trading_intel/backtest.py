"""A minimal, honest event-driven backtester.

Design constraints, each of which corresponds to a documented bias:

* Signals are evaluated on a **closed** bar and filled at the **next** bar's
  open (no look-ahead).
* Stops are checked before targets inside a bar (pessimistic whenever both are
  touched — the intrabar order is unknown from OHLC alone).
* Gaps fill at the open when the open is already beyond the stop.
* Costs are charged on both legs, in R.
* Position sizing happens inside the loop, so compounding is real.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence


@dataclass
class BacktestConfig:
    initial_equity: float = 1_000_000.0
    risk_pct: float = 0.01
    cost_bps_round_trip: float = 12.0
    max_bars_in_trade: int = 40
    allow_short: bool = True


@dataclass
class Signal:
    """A strategy's opinion at a closed bar."""

    direction: str          # "long" | "short" | "flat"
    stop: float


@dataclass
class SimTrade:
    entry_index: int
    exit_index: int
    direction: str
    entry_price: float
    exit_price: float
    stop: float
    r: float
    reason: str
    equity_before: float
    equity_after: float
    cost_r: float


def simulate(
    ohlc: Dict[str, Sequence[float]],
    strategy: Callable[[Dict[str, Sequence[float]], int], Optional[Signal]],
    config: Optional[BacktestConfig] = None,
) -> Dict[str, object]:
    """Run a bar-by-bar simulation.

    ``strategy(ctx, i)`` is called with data up to and including bar ``i`` and
    must return a :class:`Signal` or ``None``. The trade is opened at bar
    ``i+1``'s open.
    """
    cfg = config or BacktestConfig()
    opens = list(ohlc["open"])
    highs = list(ohlc["high"])
    lows = list(ohlc["low"])
    closes = list(ohlc["close"])
    n = len(closes)
    if not (len(opens) == len(highs) == len(lows) == n):
        raise ValueError("OHLC series must be the same length")
    if cfg.risk_pct <= 0 or cfg.risk_pct >= 0.5:
        raise ValueError("risk_pct must be in (0, 0.5)")

    equity = cfg.initial_equity
    trades: List[SimTrade] = []
    i = 0

    while i < n - 1:
        signal = strategy(ohlc, i)
        if signal is None or signal.direction == "flat":
            i += 1
            continue
        if signal.direction == "short" and not cfg.allow_short:
            i += 1
            continue

        entry_index = i + 1
        entry_price = opens[entry_index]
        stop = signal.stop
        direction = signal.direction

        if direction == "long" and stop >= entry_price:
            i += 1
            continue
        if direction == "short" and stop <= entry_price:
            i += 1
            continue

        risk_per_unit = abs(entry_price - stop)
        if risk_per_unit <= 0:
            i += 1
            continue

        risk_amount = equity * cfg.risk_pct
        units = risk_amount / risk_per_unit
        cost_r = (cfg.cost_bps_round_trip / 10_000.0) * entry_price / risk_per_unit

        exit_index: Optional[int] = None
        exit_price: Optional[float] = None
        reason = "time"

        for j in range(entry_index, min(n, entry_index + cfg.max_bars_in_trade)):
            if direction == "long":
                if opens[j] <= stop:
                    exit_index, exit_price, reason = j, opens[j], "gap_stop"
                    break
                if lows[j] <= stop:
                    exit_index, exit_price, reason = j, stop, "stop"
                    break
            else:
                if opens[j] >= stop:
                    exit_index, exit_price, reason = j, opens[j], "gap_stop"
                    break
                if highs[j] >= stop:
                    exit_index, exit_price, reason = j, stop, "stop"
                    break

        if exit_index is None:
            last_index = min(n - 1, entry_index + cfg.max_bars_in_trade - 1)
            exit_index = last_index
            exit_price = closes[last_index]

        if direction == "long":
            gross_r = (exit_price - entry_price) / risk_per_unit
        else:
            gross_r = (entry_price - exit_price) / risk_per_unit
        net_r = gross_r - cost_r

        equity_before = equity
        equity += equity * cfg.risk_pct * net_r
        equity = max(equity, 0.0)

        trades.append(
            SimTrade(
                entry_index=entry_index,
                exit_index=exit_index,
                direction=direction,
                entry_price=entry_price,
                exit_price=exit_price,
                stop=stop,
                r=net_r,
                reason=reason,
                equity_before=equity_before,
                equity_after=equity,
                cost_r=cost_r,
            )
        )
        if equity <= 0:
            break
        i = exit_index  # no overlapping positions

    from . import metrics as _metrics, stats as _stats

    trade_objs = [_metrics.Trade(r=t.r) for t in trades]
    summary = _metrics.summarize(trade_objs) if trade_objs else {"n": 0}
    curve = _metrics.equity_curve(trade_objs) if trade_objs else [0.0]

    return {
        "config": cfg.__dict__,
        "trades": trades,
        "summary": summary,
        "equity_r": curve,
        "max_drawdown_r": _metrics.max_drawdown_r(curve),
        "final_equity": round(equity, 2),
        "total_return": round(equity / cfg.initial_equity - 1.0, 6),
        "caveats": [
            "intrabar order is unknown from OHLC: stops are assumed hit before targets",
            "no slippage model beyond the flat cost in bps",
            "signal uses only bars up to i; the fill is at bar i+1 open",
            "must be run out-of-sample before any performance claim is made",
        ],
    }


def walk_forward_splits(n_bars: int, train: int, test: int) -> List[tuple]:
    """Chronological (train_start, train_end, test_start, test_end) windows."""
    if train < 1 or test < 1:
        raise ValueError("train and test must be >= 1")
    splits = []
    start = 0
    while start + train + test <= n_bars:
        splits.append((start, start + train, start + train, start + train + test))
        start += test
    return splits


def simple_ema_cross_strategy(
    fast: int = 20, slow: int = 50, atr_mult: float = 2.0
) -> Callable[[Dict[str, Sequence[float]], int], Optional[Signal]]:
    """A reference strategy: EMA cross with an ATR stop.

    Included to exercise the engine, not because it is profitable. It has no
    filters, no regime gate, and no claim attached to it.
    """
    from . import indicators as _ind

    cache: Dict[int, object] = {}

    def strategy(ohlc: Dict[str, Sequence[float]], i: int) -> Optional[Signal]:
        closes = ohlc["close"][: i + 1]
        if len(closes) < slow + 1:
            return None
        if id(ohlc) not in cache:
            fast_ema = _ind.ema(list(ohlc["close"]), fast)
            slow_ema = _ind.ema(list(ohlc["close"]), slow)
            atr_series = _ind.atr(list(ohlc["high"]), list(ohlc["low"]), list(ohlc["close"]), 14)
            cache[id(ohlc)] = (fast_ema, slow_ema, atr_series)
        fast_ema, slow_ema, atr_series = cache[id(ohlc)]  # type: ignore[misc]

        f_now, s_now = fast_ema[i], slow_ema[i]
        f_prev, s_prev = fast_ema[i - 1], slow_ema[i - 1]
        if None in (f_now, s_now, f_prev, s_prev) or atr_series[i] is None:
            return None
        close = closes[-1]
        if f_prev <= s_prev and f_now > s_now:
            return Signal("long", close - atr_mult * atr_series[i])
        if f_prev >= s_prev and f_now < s_now:
            return Signal("short", close + atr_mult * atr_series[i])
        return None

    return strategy
