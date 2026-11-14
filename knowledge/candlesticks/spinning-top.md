# Spinning Top

**Group:** Neutral / indecision · **Candles:** 1 · **Reliability band:** Lower
**Detector:** `patterns.detect_spinning_top`

## 1. What it is
A candle with a **small but real body** and **wicks on both sides** of comparable length. Neither side
dominated, but there was genuine two-way movement — unlike a doji, which shows equilibrium at the
close.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | `body / range` between 0.10 and 0.35 | Small but real body |
| 2 | `upper_wick ≥ 0.25 × range` and `lower_wick ≥ 0.25 × range` | Wicks on both sides |
| 3 | `range ≥ 0.5 × average_range(20)` | Non-trivial range |
| 4 | Closed candle | Else `DEVELOPING` |

If `body/range < 0.05`, label it a doji instead. If both wicks are very long relative to the body
and the range is unusually large, label it a **high wave**.

## 3. Anatomy
```
   │
 ┌─┴─┐
 └─┬─┘
   │
```

## 4. Where it means something
- As the third candle of a morning/evening star (its most important role)
- Inside a compression, before resolution
- At a level, indicating a failed test by both sides

Standalone, mid-trend, it means very little.

## 5. Interpretation
Momentum paused. In a trend, a spinning top is often a rest stop — continuation is more common than
reversal. Only at a *sustained extreme* does it hint at exhaustion, and even then it needs
confirmation.

## 6. Confirmation requirements
A spinning top is not a signal. If used at all:
- Continuation reading: price resumes beyond the candle's high/low.
- Reversal reading: price closes beyond the opposite extreme **and** breaks structure.

## 7. Volume
Low volume supports the "rest stop" reading (participants stepped aside). High volume with a small
body indicates a genuine battle — the next interval's direction becomes more informative.

## 8. Paper-trade entry conditions
No standalone entry. It appears as:
- The star in a morning/evening star: enter per those patterns.
- A compression marker: enter on the range breakout with volume.

## 9. Invalidation
Any close beyond the opposite side of the spinning top's range invalidates the continuation reading.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Treating it as a reversal candle | It is neutral by definition |
| Confusing it with a doji or high wave | Use the ratio bands |
| Reading it on tiny ranges | Range floor |
| Over-weighting it in a strong trend | Trends continue through rest stops |

## 11. Historical evidence — honest position
Described in the literature as an indecision candle; some sources claim it signals a possible reversal
"especially with confirmation", which is essentially a statement that it carries no standalone edge.
No statistic is asserted.

## 12. Worked example (illustrative, fictional)
```
Instrument: ZAB · 1D · uptrend, day 9 of advance
Candle: o320 h326 l315 c322 · body 2 · range 11 · upper 4 · lower 5 → body/range 0.18,
        both wicks > 0.25×range ✔ → spinning top
Interpretation: buyers paused. Continuation is the base case as long as 315 holds.
Next candle closes 327.5 → continuation confirmed; the spinning top was a rest stop, not a top.
```

## 13. Beginner summary (Hinglish)
**Spinning top:** chhoti body, dono taraf wicks. Na buyers jeete, na sellers — bas rukawat.

**Matlab:** momentum ruk gaya. Trend mein yeh aksar "rest" hota hai, reversal nahi.

**Sabse zaroori role:** morning/evening star ka beech wala candle.

**Akela trade kabhi nahi.** Confirm hone do — price kis side nikalta hai, wahi decide karega.

## 14. Exercise
On a daily chart, find five spinning tops inside an established trend. Record whether price continued
or reversed within 5 candles. You will typically find continuation dominates — which is exactly why
"indecision" is not the same as "reversal".

---
*See also: [`doji.md`](doji.md) · [`high-wave.md`](high-wave.md) · [`inside-bar.md`](inside-bar.md)*
