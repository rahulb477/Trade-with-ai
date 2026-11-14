# Three Inside Down

**Group:** Bearish reversal · **Candles:** 3 · **Reliability band:** Moderate–Higher
**Detector:** `patterns.detect_three_inside_down`

## 1. What it is
A **bearish harami** followed by a third bearish candle that closes **below the first candle's open**.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 bullish with a real body |
| 2 | Candle 2 bearish and **inside** candle 1's body: `open₂ < close₁` and `close₂ > open₁` |
| 3 | Candle 3 bearish, closing **below candle 1's open** |
| 4 | Prior trend upward |
| 5 | All three closed |

## 3. Anatomy
```
 1 (bull)        2 (inside)          3 (bear)
 ┌──────┐
 │      │        ┌──┐
 │      │        └──┘                    ┌──────┐
 └──────┘                                │      │  closes below candle 1's open
                                         └──────┘
```

## 4. Where it means something
At resistance; as the resolution of compression near a top; when candle 2 stalls exactly at a
resistance level and candle 3 breaks the compression downward.

## 5. Interpretation
Compression followed by downward expansion. Sellers first showed up (candle 2 killed the advance),
then took control (candle 3 broke the origin of the prior candle). It is a clean structural
statement: the buyers who made candle 1 are now underwater.

## 6. Confirmation requirements
Candle 3 completes it. Additional: candle 4 does not reclaim candle 1's open; volume expansion on
candle 3; a lower high confirmed and the prior swing low broken.

## 7. Volume
Candle 3's volume is the decisive input. Breakouts from compression on weak volume fail often.
Rising volume from candle 2 to candle 3 is ideal.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : candle 3 close, or break of candle 3's low
Entry zone     : candle 3 low ± 0.1 × ATR
Invalidation   : above max(high₁, high₂) + 0.25 × ATR
Targets        : T1 = candle 1's low (bottom of the compression) · T2 prior swing low
                 T3 measured: height of candle 1's range × 2 projected down
```

## 9. Invalidation
Close back above candle 1's open; candle 3 fully retraced; strong support immediately below
(no room).

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Candle 2 not fully inside | Rule 2 numerically |
| Candle 3 only marginally below candle 1's open | Require a clear close (+0.1 ATR) |
| Low-volume breakdown | Volume check |
| Into a support-dense zone | Check room below |
| Repeated inside-bar breakdowns in a rising market | Count prior failures |

## 11. Historical evidence — honest position
The three-candle form filters some of the false inside-bar breakouts by requiring a close beyond the
range. No success rate is claimed. Test locally via `engines/backtesting/`.

## 12. Worked example (illustrative, fictional)
```
Instrument: TUV · 1D · advance to resistance 690
C1 o672 c688 (bull) · C2 o686 c681 (inside: 686<688 ✔, 681>672 ✔)
C3 o680 c670 (closes below C1 open 672 ✔) volume 1.8× ✔ · Status: CONFIRMED
Entry 669.5 · stop 691.0 (risk 21.5) · T1 672 (→ negative, untradeable) · T2 655 (0.67R FAIL)
Verdict: WAIT — stop too wide relative to the available target.
        The tradeable version is the failed retest at 688 (risk 4 → T2 8.25R) if it occurs.
```

## 13. Beginner summary (Hinglish)
**Three inside down:** pehli badi green, doosri chhoti red jo pehli ke andar, teesri red jo pehli ke
open ke neeche close kare.

**Matlab:** pehle buying ruki, phir compression se neeche breakdown hua.

**Entry:** teesri candle ke close par ya uski low tootne par. **Stop:** dono upar wali highs ke upar.

## 14. Exercise
Find three inside-down patterns and record the stop distance in ATR units. In how many cases was the
stop wider than 1.5×ATR, making the setup impractical? Write the rule you would add.

---
*See also: [`three-inside-up.md`](three-inside-up.md) · [`harami.md`](harami.md)*
