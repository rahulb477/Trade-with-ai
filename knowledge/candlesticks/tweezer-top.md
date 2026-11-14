# Tweezer Top

**Group:** Bearish reversal · **Candles:** 2 · **Reliability band:** Lower–Moderate
**Detector:** `patterns.detect_tweezer_top`

## 1. What it is
Two consecutive candles with **matching highs** after an advance: typically bullish then bearish, both
rejected at the same price. The mirror of the tweezer bottom.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Two consecutive candles after an **uptrend** |
| 2 | `|high₁ − high₂| ≤ 0.1 × ATR` (or ≤ 0.25 × average range) |
| 3 | Candle 2 bearish (the stronger variant) |
| 4 | Both candles have a visible upper wick |
| 5 | Both closed |
| 6 | Combined range not abnormally small |

## 3. Anatomy
```
     ▲═════▲      <- equal / near-equal highs
   ┌─┴─┐ ┌─┴─┐
   │   │ │   │
   └───┘ └───┘
```

## 4. Where it means something
At resistance with prior reactions, at a round number, at the top of a channel or wedge, or at the
second failure of a breakout above a level.

## 5. Interpretation
The same price was offered twice and refused twice. That establishes a supply reference. As with the
tweezer bottom, this is weaker evidence than patterns with body structure, and it is best used as a
**level confirmation** rather than a standalone signal.

## 6. Confirmation requirements
- Minimum: candle 3 closes below the lower of the two bodies' lows.
- Good: close below the lower of the two lows.
- Strong: lower high forms and the prior swing low breaks on volume.
- Invalidated: close above the matched highs.

## 7. Volume
More convincing when candle 2's volume exceeds candle 1's. Two quiet candles at the same high can be
a paused market; the second rejection carrying more volume suggests actual selling.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : close below min(low₁, low₂)
Entry zone     : trigger ± 0.1 × ATR
Invalidation   : above max(high₁, high₂) + 0.25 × ATR
Targets        : T1 nearest prior swing low · T2 measured: advance height × 0.5 · T3 major support
```

## 9. Invalidation
Close above the matched highs (the level was absorbed); price consolidating at the highs with rising
lows; higher-timeframe uptrend intact with volume.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| "Matching" highs differing by more than tolerance | Enforce numerically |
| Mid-range appearance | Location filter |
| Both candles tiny and quiet | Range requirement |
| Equal highs caused by a single large resting sell order | Wait for the confirming close |
| Repeated tweezers in a strong uptrend | The trend is absorbing them; require structure break |

## 11. Historical evidence — honest position
Not standardised across sources, and the available literature does not support treating it as a
standalone reversal signal. Use it as confluence, and do not quote performance figures.

## 12. Worked example (illustrative, fictional)
```
Instrument: QRS · 15m · advance 512 → 528 into resistance 527.5–528.5
C1 o525.0 h528.1 l524.6 c527.4 (bull) · C2 o527.6 h528.0 l525.4 c525.8 (bear)
|528.1 − 528.0| = 0.1 ≤ 0.1 × ATR(15m) ✔ · Volume C2 = 1.4× C1 ✔ · Status: CONFIRMED
Entry 525.3 · stop 528.6 (risk 3.3) · T1 521.0 (1.30R FAIL) · T2 518.2 (2.15R ✔)
Verdict: WAIT on T1; acceptable with T2 as primary and a partial — or wait for a tighter retest entry.
```

## 13. Beginner summary (Hinglish)
**Tweezer top:** do lagatar candles jinki **high same** ho, upar trend ke baad.

**Matlab:** ek hi price par do baar buyers fail hue. Us level par supply hai.

**Entry:** jab price dono candles ki low ke neeche close kare.

**Stop:** dono highs ke thoda upar.

**Yaad rakho:** yeh akela kaafi nahi — resistance ke saath milkar hi useful hai.

## 14. Exercise
Find three tweezer tops. For each, measure the high difference in ATR units and note whether the
second candle closed below the first. Then decide which would have passed a strict filter and
explain, in one sentence, why strictness helps here.

---
*See also: [`tweezer-bottom.md`](tweezer-bottom.md) · [`double-top.md`](../chart-patterns/double-top.md)*
