"""Risk arithmetic: R-multiples, reward:risk, break-even win rate, drawdown maths.

All formulas are the ones documented in ``knowledge/risk-management/`` and
``core/risk-management.md``. Nothing here predicts anything; it only converts
prices into risk units.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence


# --------------------------------------------------------------------------
# R-multiples
# --------------------------------------------------------------------------
def risk_per_unit(entry: float, stop: float) -> float:
    """Absolute distance from entry to stop. Raises if zero (an invalid plan)."""
    dist = abs(entry - stop)
    if dist == 0:
        raise ValueError("entry and stop must differ; a zero-risk plan is invalid")
    return dist


def r_multiple(entry: float, stop: float, price: float, direction: str = "long") -> float:
    """Outcome in R units at ``price``.

    Positive = favourable, negative = adverse. Direction determines the sign,
    not the raw price difference.
    """
    dist = risk_per_unit(entry, stop)
    if direction == "long":
        return (price - entry) / dist
    if direction == "short":
        return (entry - price) / dist
    raise ValueError("direction must be 'long' or 'short'")


def reward_risk(entry: float, stop: float, target: float, direction: str = "long") -> float:
    """Reward:risk of a target. Can be negative if the target is behind the entry."""
    return r_multiple(entry, stop, target, direction)


def break_even_win_rate(rr: float, cost_r: float = 0.0) -> float:
    """Win rate required to break even, including a per-trade cost in R.

    ``rr`` is the reward:risk of winners. With costs, effective win = rr - cost_r
    and effective loss = 1 + cost_r.
    """
    if rr <= 0:
        raise ValueError("reward:risk must be positive")
    win = rr - cost_r
    loss = 1.0 + cost_r
    if win <= 0:
        return 1.0  # costs consume the entire reward: no win rate suffices
    return loss / (loss + win)


def expectancy(win_rate: float, avg_win_r: float, avg_loss_r: float = 1.0) -> float:
    """Expected value in R per trade. ``avg_loss_r`` is positive (magnitude)."""
    if not 0.0 <= win_rate <= 1.0:
        raise ValueError("win_rate must be between 0 and 1")
    return win_rate * avg_win_r - (1.0 - win_rate) * avg_loss_r


def kelly_fraction(win_rate: float, rr: float) -> float:
    """Full-Kelly fraction of equity. Reported for reference only.

    Trading guidance in this repository caps risk far below Kelly, because the
    inputs are estimates and over-betting dominates the long run.
    """
    if rr <= 0:
        raise ValueError("reward:risk must be positive")
    b = rr
    p = win_rate
    q = 1.0 - p
    f = (b * p - q) / b
    return max(0.0, f)


# --------------------------------------------------------------------------
# Drawdown
# --------------------------------------------------------------------------
def drawdown_series(equity: Sequence[float]) -> List[float]:
    """Drawdown at each step, as a negative fraction of the running peak."""
    out: List[float] = []
    peak: Optional[float] = None
    for value in equity:
        if peak is None or value > peak:
            peak = value
        out.append(0.0 if not peak else (value - peak) / peak)
    return out


def max_drawdown(equity: Sequence[float]) -> float:
    """Maximum peak-to-trough decline as a positive fraction (0.25 == 25%)."""
    return abs(min(drawdown_series(equity))) if equity else 0.0


def recovery_gain_required(drawdown: float) -> float:
    """Gain needed to recover from a drawdown: ``d / (1 - d)``."""
    if not 0.0 <= drawdown < 1.0:
        raise ValueError("drawdown must be in [0, 1)")
    return drawdown / (1.0 - drawdown)


def risk_of_ruin(risk_fraction: float, ruin_threshold: float = 0.5, max_trades: int = 100) -> float:
    """Probability of a ``ruin_threshold`` loss if every trade loses.

    Not a true ruin model (which needs a distribution); this is the deterministic
    compounding check: ``(1 - f)^n <= 1 - threshold``.
    """
    if not 0.0 < risk_fraction < 1.0:
        raise ValueError("risk_fraction must be in (0, 1)")
    remaining = 1.0 - ruin_threshold
    n = 0
    equity = 1.0
    while n < max_trades and equity > remaining:
        equity *= 1.0 - risk_fraction
        n += 1
    return float(n)


# --------------------------------------------------------------------------
# Plan object
# --------------------------------------------------------------------------
@dataclass
class TradePlan:
    """A hypothetical plan. Nothing here is advice or an order."""

    direction: str
    entry: float
    stop: float
    targets: List[float] = field(default_factory=list)
    instrument: str = ""
    timeframe: str = ""
    notes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.direction not in ("long", "short"):
            raise ValueError("direction must be 'long' or 'short'")
        risk_per_unit(self.entry, self.stop)
        if not self.targets:
            raise ValueError("at least one target is required")
        for t in self.targets:
            if self.direction == "long" and t <= self.entry:
                raise ValueError(f"target {t} is not above the long entry {self.entry}")
            if self.direction == "short" and t >= self.entry:
                raise ValueError(f"target {t} is not below the short entry {self.entry}")

    @property
    def risk(self) -> float:
        return risk_per_unit(self.entry, self.stop)

    def target_r(self, index: int = 0) -> float:
        return reward_risk(self.entry, self.stop, self.targets[index], self.direction)

    def invalidation_price(self) -> float:
        return self.stop

    def summary(self) -> dict:
        out = {
            "instrument": self.instrument,
            "direction": self.direction,
            "entry": self.entry,
            "stop": self.stop,
            "risk_per_unit": round(self.risk, 4),
            "invalidation": self.stop,
            "timeframe": self.timeframe,
        }
        for i, target in enumerate(self.targets, start=1):
            out[f"T{i}"] = target
            out[f"R_T{i}"] = round(self.target_r(i - 1), 2)
        return out

    def validation_warnings(self, min_rr_t1: float = 1.5) -> List[str]:
        """Reasons this plan should not be presented as a valid setup."""
        warns: List[str] = []
        if self.target_r(0) < min_rr_t1:
            warns.append(
                f"R:R to T1 is {self.target_r(0):.2f}, below the {min_rr_t1} minimum"
            )
        if self.risk <= 0:
            warns.append("risk per unit is zero")
        return warns
