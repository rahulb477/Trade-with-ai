# Three Inside Up

**Group:** Bullish reversal · **Candles:** 3 · **Reliability band:** Moderate–Higher
**Detector:** `patterns.detect_three_inside_up`

## 1. What it is
A **bullish harami** (two candles) followed by a third bullish candle that closes **above the first
candle's open**. It converts an indecision pattern into a confirmed reversal by adding a decisive
close beyond the original range.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 bearish, with a real body |
| 2 | Candle 2 bullish and **inside** candle 1's body: `open₂ > close₁` and `close₂ < open₁` |
| 3 | Candle 3 bullish and closes **above candle 1's open** |
| 4 | Prior trend downward |
| 5 | All three closed |

Note the distinction from a plain harami: without candle 3 closing above candle 1's open, the pattern
is only a harami and must be labelled as such.

## 3. Anatomy
```
 1 (bear)      2 (inside)      3 (bull)
 ┌──────┐
 │      │      ┌──┐
 │      │      └──┘                 ┌──────┐
 └──────┘                           │      │  closes above candle 1's open
                                    └──────┘
```

## 4. Where it means something
At support after a decline; at the lower edge of a channel; as the resolution of a compression
(inside-bar cluster). Very meaningful when candle 2 sits precisely on a support level and candle 3
breaks out of the compression.

## 5. Interpretation
Candle 2 shows selling stalled. Candle 3 shows the stall resolved upward. The pattern is the
3-candle version of "inside bar breakout", and its logic is: compression → expansion in the
direction opposite the prior trend.

## 6. Confirmation requirements
By definition candle 3 completes it. Additional:
- Good: candle 3 closes on above-average volume.
- Strong: candle 4 holds above candle 1's open (no immediate giveback).
- Invalidated: close back below candle 2's low.

## 7. Volume
The critical input is candle 3's volume. A breakout from an inside bar on weak volume fails
disproportionately often. Rising volume across candles 2→3 is the ideal.

## 8. Paper-trade entry conditions (illustrative)
```
Long trigger  : candle 3 close, or break of candle 3 high
Entry zone    : candle 3 high ± 0.1 × ATR
Invalidation  : below min(low₁, low₂) − 0.25 × ATR
Targets       : T1 = candle 1 high (the top of the compression) · T2 prior swing high
                T3 measured: height of candle 1's range × 2 projected from the breakout
```

## 9. Invalidation
Close below candle 2's low; candle 3 giving back its entire body; overhead resistance within one
candle's range.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Candle 2 not fully inside candle 1's body | Rule 2 numerically |
| Candle 3 closes above candle 1's open by a hair | Require a clear close (e.g. +0.1 × ATR) |
| Low-volume breakout | Volume check |
| Long downtrend with repeated inside-bar breakouts that fail | Count prior failures; context matters |

## 11. Historical evidence — honest position
Inside-bar breakouts have a well-known failure profile on low volume; the three-candle version adds
a close-through requirement which mechanically filters some of those failures. No success rate is
claimed here. Test locally.

## 12. Worked example (illustrative, fictional)
```
Instrument: STU · 1D · decline to support 410
C1 o424 c411 (bear) · C2 o413 c420 (inside: 413>411, 420<424 ✔)
C3 o420.5 c426 (closes above C1 open 424 ✔) volume 1.7× ✔
Status CONFIRMED · Entry 426.4 · stop 409.4 (risk 17.0)
T1 431 (C1 high) → 0.27R FAIL · T2 445 (prior swing) → 1.09R FAIL · T3 460 → 1.98R ✔
Verdict: WAIT at this entry; only viable on a retest near 421 (risk 11.6 → T3 3.36R).
```

## 13. Beginner summary (Hinglish)
**Three inside up:** pehli red candle, doosri chhoti green jo pehli ke **andar** hai, teesri green jo
pehli candle ke open ke **upar** close kare.

**Matlab:** pehle selling ruki, phir compression se upar ki taraf breakout hua.

**Entry:** teesri candle ke close par ya uski high tootne par.

**Stop:** dono pehli candles ki sabse neeche low ke thoda neeche.

**Zaroori:** teesri candle ka volume achha hona chahiye, warna breakout fail hone ke chances zyada.

## 14. Exercise
Compare five inside-bar breakouts that had above-average volume on the breakout candle with five
that had below-average volume. Compute hit rate over the next 10 candles for each group. Write down
the difference and whether your sample is large enough to mean anything.

---
*See also: [`harami.md`](harami.md) · [`inside-bar.md`](inside-bar.md) · [`three-inside-down.md`](three-inside-down.md)*
