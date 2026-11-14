"""Trade-log metrics.

The unit is R (risk multiples), not currency, so results are comparable across
instruments and account sizes. Every rate statistic is reported with its sample
size, and hit rates can be accompanied by a Wilson interval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import stats


@dataclass
class Trade:
    """One closed trade. ``r`` is the realised outcome in R multiples."""

    r: float
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    instrument: str = ""
    direction: str = "long"
    mae_r: Optional[float] = None  # maximum adverse excursion
    mfe_r: Optional[float] = None  # maximum favourable excursion
    tags: List[str] = field(default_factory=list)


def from_dicts(rows: Sequence[dict]) -> List[Trade]:
    trades = []
    for row in rows:
        trades.append(
            Trade(
                r=float(row["r"]),
                entry_time=row.get("entry_time"),
                exit_time=row.get("exit_time"),
                instrument=row.get("instrument", ""),
                direction=row.get("direction", "long"),
                mae_r=row.get("mae_r"),
                mfe_r=row.get("mfe_r"),
                tags=list(row.get("tags", [])),
            )
        )
    return trades


def summarize(trades: Sequence[Trade]) -> Dict[str, object]:
    """Aggregate metrics. Returns ``notes`` explaining what is not reportable."""
    n = len(trades)
    notes: List[str] = []
    if n == 0:
        return {"n": 0, "notes": ["no trades: no metrics are defined"]}

    rs = [t.r for t in trades]
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r < 0]
    scratches = [r for r in rs if r == 0]

    gross_win = sum(wins)
    gross_loss = abs(sum(losses))
    expectancy = sum(rs) / n

    equity = [0.0]
    for r in rs:
        equity.append(equity[-1] + r)

    # longest losing streak
    streak = longest = 0
    for r in rs:
        if r < 0:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 0

    hit_rate = len(wins) / n
    ci = stats.wilson_interval(len(wins), n)

    if n < 30:
        notes.append(
            f"n={n}: below 30, no rate statistic is meaningful; treat these as anecdotes"
        )
    if n < 100:
        notes.append(
            f"n={n}: below 100, the confidence interval is too wide for any edge claim"
        )
    if scratches:
        notes.append(f"{len(scratches)} scratch trade(s) counted as non-wins")

    result: Dict[str, object] = {
        "n": n,
        "wins": len(wins),
        "losses": len(losses),
        "scratches": len(scratches),
        "hit_rate": round(hit_rate, 4),
        "hit_rate_ci95": (round(ci[0], 4), round(ci[1], 4)),
        "avg_win_r": round(sum(wins) / len(wins), 4) if wins else None,
        "avg_loss_r": round(sum(losses) / len(losses), 4) if losses else None,
        "expectancy_r": round(expectancy, 4),
        "profit_factor": round(gross_win / gross_loss, 4) if gross_loss else None,
        "gross_r": round(sum(rs), 4),
        "max_drawdown_r": round(max_drawdown_r(equity), 4),
        "longest_losing_streak": longest,
        "best_r": round(max(rs), 4),
        "worst_r": round(min(rs), 4),
        "notes": notes,
    }
    return result


def max_drawdown_r(equity_r: Sequence[float]) -> float:
    """Max peak-to-trough in R units (absolute, not a fraction)."""
    if not equity_r:
        return 0.0
    peak = equity_r[0]
    worst = 0.0
    for value in equity_r:
        peak = max(peak, value)
        worst = max(worst, peak - value)
    return worst


def equity_curve(trades: Sequence[Trade]) -> List[float]:
    """Cumulative R. Starts at 0.0."""
    out = [0.0]
    for t in trades:
        out.append(out[-1] + t.r)
    return out


def expectancy_with_costs(trades: Sequence[Trade], cost_r: float) -> Optional[float]:
    """Expectancy after subtracting ``cost_r`` per trade."""
    if not trades:
        return None
    return sum(t.r for t in trades) / len(trades) - cost_r


def by_tag(trades: Sequence[Trade]) -> Dict[str, Dict[str, object]]:
    """Per-tag breakdown, so a strategy is not judged only in aggregate."""
    tags: Dict[str, List[Trade]] = {}
    for t in trades:
        for tag in (t.tags or ["untagged"]):
            tags.setdefault(tag, []).append(t)
    return {tag: summarize(group) for tag, group in tags.items()}


def mae_mfe_table(trades: Sequence[Trade]) -> Dict[str, Optional[float]]:
    """Average excursions. Useful for judging whether stops are too tight."""
    maes = [t.mae_r for t in trades if t.mae_r is not None]
    mfes = [t.mfe_r for t in trades if t.mfe_r is not None]
    return {
        "avg_mae_r": round(sum(maes) / len(maes), 4) if maes else None,
        "avg_mfe_r": round(sum(mfes) / len(mfes), 4) if mfes else None,
        "n_with_mae": len(maes),
        "n_with_mfe": len(mfes),
    }
