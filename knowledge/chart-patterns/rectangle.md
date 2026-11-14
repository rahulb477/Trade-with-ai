# Rectangle (Trading Range)

**Type:** Continuation or reversal, depending on resolution · **Bars:** typically 20–100

## 1. Shape
A horizontal trading range with **two well-tested boundaries** — resistance at the top, support at the bottom.
Price oscillates between them.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | A horizontal resistance tested ≥2 times (≥3 is better) |
| 2 | A horizontal support tested ≥2 times |
| 3 | The range is wide enough to be tradable (≥2 ATR at least) |
| 4 | The boundaries are roughly parallel (a slight slope is acceptable; a strong slope makes it a channel) |
| 5 | Resolution: a **close beyond a boundary** with volume |

## 3. Interpretation depends entirely on context

| Context | Typical resolution |
|---------|-------------------|
| Range forms after an advance (consolidation) | Continuation upward more often |
| Range forms after a decline | Continuation downward more often |
| Range forms at a top after a long advance | Could be distribution → downward |
| Range forms at a bottom after a long decline | Could be accumulation → upward |
| Range forms mid-trend for a long time | Genuinely neutral; wait |

A rectangle is the clearest example of "the pattern describes, the context predicts."

## 4. Volume
- Inside the range: volume often declines as the range matures.
- Range fades (buying support / selling resistance) work best on *declining* volume.
- Breakouts need expansion. A breakout on contracting volume is the classic failed break.

## 5. Two ways to trade a rectangle

### A. Range fade (mean reversion)
```
Long at support with a rejection candle, stop below support, target mid-range/resistance
Short at resistance with a rejection candle, stop above resistance, target mid-range/support
Requires: ADX < 20, range boundaries clearly tested, no event risk
Fails when: the range breaks
```

### B. Breakout (trend initiation)
```
Long on close above resistance + volume, stop back inside the range
Short on close below support + volume
Requires: volume expansion, room beyond the boundary
Fails when: it is a false breakout (very common — see workflows/trap-detection.md)
```

**Never do both on the same signal.** Decide the regime and the plan before the boundary is tested.

## 6. Measurement
```
target = boundary ± range height
```
Worked: range 480–510 (height 30), breakout up at 511 → target 541.

Fade targets are the opposite boundary, which is by definition the range height — the same arithmetic.

## 7. Invalidation
For a fade: a close beyond the boundary (the range broke).
For a breakout: a close back inside the range (false breakout).

## 8. Common false signals
| False signal | Guard |
|--------------|-------|
| "Support" tested once | Require ≥2 |
| Fading boundaries when ADX is high | Check regime first |
| Breakout on low volume | Volume filter |
| Range too narrow to cover costs | Require ≥2 ATR |
| Repeating fades after two boundary breaks | The range is over |
| Ignoring the mid-range trap | Range mid-point is where most false signals occur; avoid entries there |

## 9. Worked example (fictional)
```
Instrument QRS · 1D · range 480–510 for 18 sessions, tested 3 times each side, ADX 13
Setup A (fade): long at 482 with a bullish rejection candle, stop 476, risk 6, target 508 -> 4.3R
Setup B (breakout): if price closes 512 on 2× volume, long with stop 505 (back inside), risk 7,
        target 540 (measured) -> 4.0R
Both are described in advance; only one triggers. That is conditional planning, which is the point.
Invalidation for A: a close below 476. For B: a close back below 511.
```

## 10. Beginner summary (Hinglish)
**Rectangle:** ek horizontal range — upar resistance, neeche support, dono baar baar test hue.

**Do tarah se trade hota hai:**
1. **Range fade:** support par kharido, resistance par becho. ADX kam ho (range regime) tab hi.
2. **Breakout:** boundary ke bahar close + volume par trade lo.

**Dono ek saath mat karo** — pehle decide karo ki aap range maan rahe ho ya breakout.

**Target:** range ki height. **Stop:** boundary ke doosri taraf.

**Badi galti:** range ke **beech** mein entry lena — wahan sabse zyada false signals hote hain.

## 11. Exercise
Find a rectangle. Estimate the ADX. Then simulate both plans (fade and breakout) on paper for the following
20 bars. Which would have made money? Write down whether the regime call (ADX) or the entry rule determined
the outcome.

---
*See also: [`../candlesticks/inside-bar.md`](../candlesticks/inside-bar.md) ·
[`../workflows/breakout-analysis.md`](../../workflows/breakout-analysis.md) · [`ascending-triangle.md`](ascending-triangle.md)*
