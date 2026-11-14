# Price Action — Index

Price action is the study of **price alone**: its swings, its reactions at levels, and the way it moves between
them. It is the primary evidence in this repository; indicators are secondary.

Why price-first:

1. Indicators are derived from price, so they cannot contain more information.
2. Levels and swings are what orders actually cluster around.
3. A chart with no indicators is still fully analysable; a chart with no price is not.

---

## 1. Swing structure vocabulary

```
Higher High (HH)   — a peak above the previous peak
Higher Low (HL)    — a trough above the previous trough
Lower High (LH)    — a peak below the previous peak
Lower Low (LL)     — a trough below the previous trough
```

| Sequence | Structure |
|----------|-----------|
| HH + HL | Uptrend |
| LH + LL | Downtrend |
| Mixed / overlapping | Range or transition |

---

## 2. Modules

| Topic | File |
|-------|------|
| HH/HL — uptrend structure | [`higher-highs-higher-lows.md`](higher-highs-higher-lows.md) |
| LH/LL — downtrend structure | [`lower-highs-lower-lows.md`](lower-highs-lower-lows.md) |
| Breakout | [`breakout.md`](breakout.md) |
| Breakdown | [`breakdown.md`](breakdown.md) |
| Retest | [`retest.md`](retest.md) |
| Rejection | [`rejection.md`](rejection.md) |
| Consolidation | [`consolidation.md`](consolidation.md) |
| Trend continuation | [`trend-continuation.md`](trend-continuation.md) |
| Trend reversal | [`trend-reversal.md`](trend-reversal.md) |

Related: `knowledge/market-structure/` (phases, ranges, level mapping),
`knowledge/smart-money/` (BOS/CHoCH framing), `workflows/breakout-analysis.md`,
`workflows/breakdown-analysis.md`, `workflows/trap-detection.md`.

---

## 3. How to identify a swing point

A swing high is a bar whose high is greater than the highs of the `k` bars on each side. Common values:
`k = 2` (fast, noisy), `k = 3` (standard), `k = 5` (structural).

**Always state the `k` you used.** A "swing high" with `k=1` is noise; with `k=10` it is a major structure point.
Two analysts using different `k` will disagree about whether the trend is intact — and both can be right about
different things.

Rules of thumb:

- Use a **larger `k`** on higher timeframes.
- A swing that produced a **decisive close** away from the level matters more than one that produced a wick.
- A swing that was **tested again and held** is a stronger level.
- Swings that coincide with high volume are more significant than quiet ones.

---

## 4. Levels: how many touches makes a level real

| Touches | Status | Permitted language |
|---------|--------|--------------------|
| 1 | Candidate | "possible level at X" |
| 2 | Established | "level at X, tested twice" |
| 3+ | Strong | "well-tested level at X" |

A level is not a line you drew; it is a price where the market repeatedly reacted. If you cannot point to two
reactions, you have drawn a line, not found a level.

---

## 5. The price-action reading sequence

For any chart:

```
1. Mark swings (state k)
2. Classify the sequence: HH/HL, LH/LL, or mixed
3. Mark levels (≥2 touches) and the trendlines (≥2 touches)
4. Identify the current location: at a level / mid-range / at an extreme
5. Identify the last decisive event: breakout, rejection, or nothing
6. Only now look at candles and indicators
```

Most analysis errors come from doing step 6 first.

---

## 6. Common errors

| Error | Consequence |
|-------|-------------|
| Drawing levels after seeing the outcome | Confirmation bias; the "level" is fitted to the trade |
| Using `k=1` swings | Every bar becomes a turning point; trend is unreadable |
| Treating a wick as a break | False breakout analysis |
| Ignoring the higher timeframe | Local structure fights the dominant trend |
| Counting the same swing as two pieces of evidence | Inflated confidence (see `core/evidence-engine.md` §6) |

---

*See also: [`../market-structure/`](../market-structure/) · [`../../core/chart-recognition.md`](../../core/chart-recognition.md)*
