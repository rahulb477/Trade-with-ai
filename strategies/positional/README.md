# Positional / Long-Horizon Trading

**Horizon:** months to years. **Holding:** 1 month – several years. **Trades per year:** few.

**Status:** `DOCUMENTED` — method described, not validated.

## 1. Characteristics

| Attribute | Typical |
|-----------|---------|
| Analysis timeframe | Weekly and monthly |
| Entry timeframe | Daily or weekly |
| Target | 20–100%+ or until the thesis changes |
| Stop | Structural, often wide (10–20%) or thesis-based |
| Cost impact | Minimal (a few bps over a year) |
| Key risks | Fundamental deterioration, regime change, opportunity cost |

## 2. What is different at this horizon

1. **Fundamentals dominate.** A weekly chart is a summary of a business trajectory.
2. **Stops are wider**, so position size must be smaller; you cannot risk 1% with a 20% stop unless the position is
   small relative to equity.
3. **Time in the market** matters more than timing; drawdowns of 20–30% are normal along the way.
4. **Corporate actions** (splits, bonuses, dividends) matter for the chart's continuity.
5. **Regime shifts** (rate cycles) are the dominant driver.

## 3. Position sizing at a wide stop

```
units = risk_amount / |entry − stop|

equity 1,000,000 · risk 0.75% = 7,500
entry 500 · stop 420 (16% away) -> risk per unit 80
units = 93  -> notional 46,500 (4.7% of equity)
```

Note how a wide stop forces a **small** position. That is correct behaviour, not a mistake.

## 4. Process

```
Quarterly
  1. Review the macro regime (rates, inflation, currency, growth).
  2. Review sector positioning.
  3. For each holding: has the thesis changed? (Not "has the price changed".)
  4. Update the level map on the weekly chart.

Monthly
  1. Check the weekly structure: is the trend intact?
  2. Check the corporate-action calendar.
  3. Review drawdown vs tolerance.

On a trigger
  1. Confirm the weekly close.
  2. Size from the structural stop.
  3. Log it.
```

## 5. Failure modes

| Failure | Guard |
|---------|-------|
| Using intraday stops on a positional position | Match the stop to the timeframe |
| Confusing price volatility with thesis change | Re-read the thesis |
| Ignoring valuation because the chart looks good | Cite fundamentals |
| Oversizing because "it's long term" | Wide stops require small size |
| Not reviewing the thesis | Quarterly review is mandatory |

## 6. Beginner summary (Hinglish)

**Positional** = mahino/saalon ka holding. Weekly/monthly chart dekho.

**Yahan fundamentals matter karte hain** — sirf chart nahi.

**Stop wide hota hai** (10–20%), isliye **position size chhota** hota hai. Yeh galti nahi, sahi behaviour hai.

**Review:** har quarter mein thesis check karo — "price gira" nahi, "business badla" — yeh sawal.

**Costs negligible** hote hain, isliye yeh sabse "cost-friendly" style hai.

## 7. Validation notes

Use monthly/weekly data over a decade or more. Beware survivorship bias (delisted names matter enormously at this
horizon). Benchmark against a simple index buy-and-hold — if the method cannot beat that after costs, say so.
