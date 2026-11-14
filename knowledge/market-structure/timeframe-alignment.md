# Timeframe Alignment

## 1. The principle

Higher timeframes define **bias**; lower timeframes define **timing**. A trade that violates the higher
timeframe's structure is a counter-trend bet, whether or not its local setup is perfect.

```
Monthly  -> the multi-year regime
Weekly   -> the primary trend
Daily    -> the tradeable trend, swing entries
4H/1H    -> intraday structure, swing intraday entries
15m/5m   -> precision entries and stops
1m/3m    -> execution only; noise-dominated
```

## 2. The alignment ladder

| Relationship | Reading | Allowed action |
|--------------|---------|----------------|
| All aligned up | Strongest bullish case | Long setups, full size |
| Higher up, lower down | Pullback inside an uptrend | Long at higher-timeframe support only |
| Higher down, lower up | Bounce inside a downtrend | Short at higher-timeframe resistance only |
| Higher up, lower range | Consolidation inside an uptrend | Wait for the lower timeframe to resolve up |
| Conflict, both strong | Unresolved | WAIT |
| Higher unknown | Unverified | Cap at WAIT for continuation claims |

## 3. The ratio rule

Use timeframes roughly 4–6× apart: `1m → 5m → 30m → 4H → Daily → Weekly`. A 15m chart and a 20m chart are
effectively the same timeframe and add nothing.

Common working pairs:

| Trading style | Analysis timeframe | Entry timeframe |
|---------------|--------------------|-----------------|
| Scalping | 15m | 1–3m |
| Intraday | 1H | 5–15m |
| Swing | Daily | 1H |
| Positional | Weekly | Daily |

## 4. Never claim what you did not see

**I1-adjacent rule:** if a timeframe was not shown to you and you have no data source, it is *unknown*. Write:

```
| TF  | Source       | Trend | Key level | Conflict |
|-----|--------------|-------|-----------|----------|
| 1D  | screenshot   | up    | 1_196     | —        |
| 1H  | screenshot   | down  | 1_240     | yes — pullback |
| 1W  | not provided | —     | —         | unknown  |
```

Writing "the weekly is bullish" when you have not seen a weekly chart is a fabrication. It is also one of the
most common failures in AI chart analysis.

## 5. Handling conflict

When the higher timeframe and the lower timeframe disagree:

1. **Quantify**: is the lower-timeframe move a retracement (within 38.2–61.8% of the last higher-timeframe leg) or
   a structure break (beyond the last higher-timeframe swing)?
2. If it is a retracement → it is a **pullback**, and the higher-timeframe trend still governs. Long setups at
   higher-timeframe support are valid; short setups against the higher-timeframe trend are not, unless the
   lower timeframe has broken structure *and* retested.
3. If it is a structure break → the higher timeframe's trend is in question. Verdict: WAIT until the higher
   timeframe closes to confirm.
4. If both are strong and neither is a retracement → **WAIT**. Do not average.

## 6. The nested-pullback trap

A 15m pullback inside a 1H pullback inside a daily uptrend is common. Each level can look like a reversal.

Guard: always state the **degree** of the pullback relative to the timeframe above it. A 15m "downtrend" that
retraces 30% of the 1H leg is a 1H pullback, not a 15m downtrend that matters.

## 7. Reading alignment from screenshots

If the user supplies one screenshot, ask for one more at a higher timeframe — that single extra image
substantially improves the analysis. If they cannot, be explicit:

> "I have only the 15m chart. The higher-timeframe trend is unknown, so I cannot assess whether this is a
> pullback or a reversal. The scenarios below are conditional on the higher timeframe being neutral or aligned."

## 8. Common errors

| Error | Guard |
|-------|-------|
| Asserting a higher timeframe you never saw | Unknown is a valid state |
| Using timeframes that are too close together | 4–6× ratio |
| Letting the lower timeframe override the higher one without a structure break | Quantify the retracement |
| Analysing five timeframes and averaging | Pick three: bias, structure, trigger |
| Treating a 1m chart as structural | Execution only |

## 9. Beginner summary (Hinglish)

**Rule:** **bada timeframe direction batata hai, chhota timeframe entry ka time batata hai.**

Example: daily uptrend hai, 15m par girawat — to woh **pullback** hai, reversal nahi. Entry daily support par lo,
15m confirmation ke saath.

**Agar bada timeframe upar aur chhota neeche, aur chhota wala bade ki last swing tod de** → tab WAIT karo, tab
tak jab bada timeframe confirm na kare.

**Sabse badi galti:** jo timeframe dekha hi nahi, uska trend bata dena. "Weekly bullish hai" tabhi likho jab
weekly chart dekha ho. Nahi dekha to likho: **"unknown"**.

## 10. Exercise

Take a screenshot at one timeframe. Write the table with the higher timeframe marked "not provided". Then write
the scenarios conditional on that unknown. Then obtain the higher timeframe and rewrite the analysis. Note which
conclusions changed — and whether the unknown had been material.

---
*See also: [`ranges-and-trends.md`](ranges-and-trends.md) · [`../../workflows/multi-timeframe-analysis.md`](../../workflows/multi-timeframe-analysis.md)*
