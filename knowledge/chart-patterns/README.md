# Chart Patterns — Index and Method

16 multi-bar patterns, documented with formation rules, volume expectations, confirmation, measurement,
invalidation and failure modes.

---

## 1. What a chart pattern is — and is not

A chart pattern is a **geometric summary of a repeated behavioural sequence**: accumulation, distribution,
indecision, or continuation. It is a shorthand for "the auction has behaved this way recently", not a
mechanical forecast.

Three honest statements about chart patterns:

1. They are **descriptive first, predictive second**. The pattern describes how price behaved; the prediction
   requires a breakout and confirmation.
2. **Pattern recognition is subjective.** Two analysts disagree about the same shape regularly. That is why
   this repository requires every pattern claim to be auditable against written rules.
3. **Base rates must be measured, not assumed.** Published pattern statistics vary enormously by market,
   timeframe and definition. No numbers are asserted here (see §5).

---

## 2. The four-state model

Every pattern in a report carries one state:

| State | Definition |
|-------|-----------|
| `POSSIBLE` | Shape resembles the pattern but at least one rule fails or is unverified. Name the failing rule. |
| `DEVELOPING` | All rules satisfied so far, but the pattern is not complete (e.g. the neckline has not broken). |
| `CONFIRMED` | Complete **and** the confirmation event (breakout/retest) has occurred on a closed bar. |
| `FAILED` | Completed but the confirmation failed (price returned through the boundary). A failed pattern is itself information — it often sets up the opposite move. |

Never write "head and shoulders" without a state. A `DEVELOPING` H&S is a watchlist item, not a trade.

---

## 3. Universal rules for all chart patterns

| Rule | Reason |
|------|--------|
| **Prior trend required** | Reversal patterns need something to reverse; continuation patterns need something to continue. |
| **Boundary touches must be real** | A trendline needs ≥2 touches; a neckline needs ≥2 reaction points. One touch is a "candidate line". |
| **Breakout must be a close** | Intraday wicks through a neckline are not breakouts. |
| **Volume should expand on the breakout** | Breakouts on contracting volume fail disproportionately often. |
| **Retest improves quality** | A breakout that is retested and holds is stronger than one that runs immediately. |
| **Measured move is a target, not a promise** | Compute it, show the arithmetic, treat it as one candidate among structure-based targets. |
| **Invalidation is structural** | Beyond the pattern's extreme, with a volatility buffer. |
| **Timeframe matters** | A daily H&S and a 5-minute H&S are different objects with different reliability. |
| **Log/linear scale matters** | Long-horizon patterns should be read on a log scale; linear scale distorts proportions. |

---

## 4. Measurement conventions used here

```
Reversal patterns (H&S, double/triple top-bottom, rounding):
  target = neckline ∓ pattern height
           where pattern height = |neckline − pattern extreme|

Triangle / wedge / pennant (converging):
  target = breakout point ± widest part of the pattern

Flag:
  target = breakout point ± flagpole height

Rectangle / range:
  target = boundary ± range height

Cup and handle:
  target = rim breakout + cup depth
```

Every measured target is quoted **with its arithmetic** and compared against visible structural levels. If the
measured target is beyond an obvious major resistance, say so and prefer the nearer structure.

---

## 5. Base rates — the honest position

Published works (Bulkowski's *Encyclopedia of Chart Patterns*, Edwards & Magee's *Technical Analysis of Stock
Trends*) contain measured statistics across large samples. Those numbers are from particular markets and
periods, and pattern definitions vary between studies.

**This repository does not reproduce them as fact.** To obtain a usable base rate for your instrument:

1. Code the rules mechanically (`integrations/python/trading_intel/patterns.py` for candles;
   `engines/backtesting/` for chart patterns).
2. Scan a long history with costs.
3. Report sample size, hit rate with a confidence interval, expectancy in R, and max adverse excursion.
4. Split in-sample / out-of-sample.

A pattern with 15 occurrences is an anecdote. Do not present it as an edge.

---

## 6. Catalogue

### Reversal — topping

| Pattern | File | Measured target |
|---------|------|-----------------|
| Head and Shoulders | [`head-and-shoulders.md`](head-and-shoulders.md) | Neckline − height |
| Double Top | [`double-top.md`](double-top.md) | Neckline − height |
| Triple Top | [`triple-top.md`](triple-top.md) | Neckline − height |
| Rising Wedge | [`rising-wedge.md`](rising-wedge.md) | Breakout − widest width |
| Cup and Handle | [`cup-and-handle.md`](cup-and-handle.md) | Bullish, despite the "top" feel — see file |

### Reversal — bottoming

| Pattern | File | Measured target |
|---------|------|-----------------|
| Inverse Head and Shoulders | [`inverse-head-and-shoulders.md`](inverse-head-and-shoulders.md) | Neckline + height |
| Double Bottom | [`double-bottom.md`](double-bottom.md) | Neckline + height |
| Triple Bottom | [`triple-bottom.md`](triple-bottom.md) | Neckline + height |
| Falling Wedge | [`falling-wedge.md`](falling-wedge.md) | Breakout + widest width |

### Continuation

| Pattern | File | Bias |
|---------|------|------|
| Bull Flag | [`bull-flag.md`](bull-flag.md) | Up |
| Bear Flag | [`bear-flag.md`](bear-flag.md) | Down |
| Pennant | [`pennant.md`](pennant.md) | Direction of the pole |
| Rectangle | [`rectangle.md`](rectangle.md) | Either; resolution decides |
| Ascending Triangle | [`ascending-triangle.md`](ascending-triangle.md) | Usually up |
| Descending Triangle | [`descending-triangle.md`](descending-triangle.md) | Usually down |
| Symmetrical Triangle | [`symmetrical-triangle.md`](symmetrical-triangle.md) | Neutral; resolution decides |

---

## 7. Frequently confused pairs

| Pair | Distinguishing test |
|------|---------------------|
| Ascending triangle vs rising wedge | Triangle: flat top, rising bottom, converging. Wedge: **both** boundaries rising and converging |
| Symmetrical triangle vs pennant | Pennant requires a prior pole (a sharp directional move) and is small/short. Triangle has no pole requirement and is larger |
| Double top vs rectangle resistance test | Double top needs a **neckline break**. Two touches of resistance without a break is just a resistance test |
| Bull flag vs bear flag | Direction of the pole. The drift is against the pole in both; the pole decides the bias |
| H&S vs triple top | H&S has a higher middle peak. Triple top has three roughly equal peaks |
| Cup and handle vs rounding bottom | Handle: a small pullback near the rim after the cup. Rounding bottom has no handle |
| Rectangle vs consolidation | A rectangle has defined, tested boundaries. "Consolidation" is a looser description |

---

## 8. Reporting template for a chart pattern

```
Pattern        : <name> (<state>)
Timeframe      : <tf>
Boundaries     : neckline <price> (touches: <n>, dates if visible) · extreme <price>
Volume         : <behaviour on formation and breakout>
Confirmation   : <what must close where>
Measured target: <price> (arithmetic: <neckline> ∓ <height>)
Structural target: <nearest visible level> — <closer/further than measured>
Invalidation   : <price> (basis: <pattern extreme + buffer>)
Failure mode   : <what would make this a failed pattern, and what that would imply>
```

---

*Detectors: `integrations/python/trading_intel/patterns.py` · Tests: `tests/chart-recognition/` ·
Candles: [`../candlesticks/`](../candlesticks/)*
