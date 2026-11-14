# Bearish Engulfing

**Group:** Bearish reversal · **Candles:** 2 · **Reliability band:** Moderate–Higher
**Detector:** `patterns.detect_bearish_engulfing`

## 1. What it is
After an advance: a **bullish** candle, then a **bearish** candle whose body completely engulfs the
first candle's body — opening at or above the prior close and closing at or below the prior open.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 bullish |
| 2 | Candle 2 bearish |
| 3 | `open₂ ≥ close₁` |
| 4 | `close₂ ≤ open₁` |
| 5 | Prior trend upward |
| 6 | `body₂ ≥ 1.0 × body₁` (≥1.2× preferred) |
| 7 | Both closed |

## 3. Anatomy
```
 candle 1 (bull)          candle 2 (bear)
   ┌───┐                  ┌─────┐
   │   │                  │     │
   │   │  <- engulfed --> │     │
   └───┘                  └─────┘
```

## 4. Where it means something
At resistance with prior reactions; at the top of a rising channel; after a gap-up that fails and
reverses (a "bull trap" candle — the strongest context); at a Fib extension cluster.

## 5. Interpretation
A transfer of control from buyers to sellers within a single interval, and the second interval
started strong (opened up) and ended weak (closed down). The gap-up-then-reverse version is
particularly informative: it traps late buyers.

## 6. Confirmation requirements
| Level | Confirmation |
|-------|--------------|
| Minimum | Pattern complete (candle 2 closes below candle 1's open) |
| Good | Candle 3 closes below candle 2's low |
| Strong | A lower high forms and the prior swing low breaks on volume |
| Invalidated | Close above candle 2's high |

## 7. Volume
High volume on candle 2 = genuine distribution. Very high volume with a long lower wick on candle 2
means sellers were met with buyers — weaker. Low volume weakens the signal materially.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : close below candle 2's low, or a failed retest of the engulf zone
Entry zone     : candle 2 low ± 0.1 × ATR
Invalidation   : above candle 2's high + 0.25 × ATR
Targets        : T1 prior swing low / the base of the last leg up
                 T2 measured: advance height × 0.5
                 T3 major support
```

## 9. Invalidation
Close above candle 2's high; price consolidating above the engulf with rising higher lows; the
higher timeframe making fresh highs with volume.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Engulf into strong support with no room | Check room below |
| Tiny candle 1 | Require `body₁ ≥ 0.5 × avg_range` |
| Low-volume engulf | Volume check |
| One-off news spike that reverses the next day | Check for event-driven candles |
| Bull-market dips routinely produce bearish engulfings that fail | Require structure break, not just the pattern |

## 11. Historical evidence — honest position
Structurally stronger than single-candle patterns because it encodes two intervals. No win rate is
asserted. Measure locally with `engines/backtesting/`.

## 12. Worked example (illustrative, fictional)
```
Instrument: EFG · 1H · advance 88.2 → 93.6; resistance 93.4–93.8
C1 o92.1 h93.3 l92.0 c93.1 (bull, body 1.0)
C2 o93.4 h93.5 l91.6 c91.9 (bear, body 1.5) — open2 93.4 ≥ close1 93.1 ✔ close2 91.9 ≤ open1 92.1 ✔
Volume: C2 = 1.8× ✔ · Status: CONFIRMED
Entry 91.8 · stop 93.7 (risk 1.9) · T1 90.2 (1.0R) · T2 88.4 (1.79R) · T3 87.0 (2.5R)
Verdict: WAIT on T1 arithmetic; acceptable if the plan uses T2 as the primary target with a partial
         at 90.2 — state this explicitly rather than pretending T1 is viable.
```

## 13. Beginner summary (Hinglish)
**Bearish engulfing:** pehli green candle, doosri red candle jo pehli ko poora nigal le.

**Matlab:** buyers ka control ek hi session mein chala gaya. Agar doosri candle upar gap karke neeche
band ho, to yeh sabse strong version hai — late buyers fase.

**Entry:** doosri candle ki low tootne par.

**Stop:** doosri candle ki high ke thoda upar.

**Dhyan:** agar neeche turant strong support hai, to short ka koi matlab nahi.

## 14. Exercise
Find five bearish engulfings at resistance and five mid-trend. Compute the R:R to the nearest support
for each. Which group had acceptable arithmetic? Write the conclusion you would apply next time.

---
*See also: [`bullish-engulfing.md`](bullish-engulfing.md) · [`dark-cloud-cover.md`](dark-cloud-cover.md) · [`harami.md`](harami.md)*
