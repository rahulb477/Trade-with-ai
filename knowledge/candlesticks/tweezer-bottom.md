# Tweezer Bottom

**Group:** Bullish reversal · **Candles:** 2 · **Reliability band:** Lower–Moderate
**Detector:** `patterns.detect_tweezer_bottom`

## 1. What it is
Two consecutive candles with **matching lows** (within a small tolerance) after a decline: typically
a bearish candle followed by a bullish candle, both rejecting the same price level. The name comes
from tweezers gripping a price and refusing to let it go lower.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Two consecutive candles after a **downtrend** |
| 2 | `|low₁ − low₂| ≤ 0.1 × ATR` (or ≤ 0.25 × average range) — matched lows |
| 3 | Candle 2 is bullish (colour-inverted variants exist and are weaker) |
| 4 | Both candles have a visible lower wick (the rejection is visible, not implied) |
| 5 | Both closed |
| 6 | Combined range is not abnormally small relative to recent volatility |

## 3. Anatomy
```
   ┌───┐
   │   │ ┌───┐
   └─┬─┘ └─┬─┘
     │     │
     ▼═════▼   <- equal / near-equal lows: same price rejected twice
```

## 4. Where it means something
At a horizontal support, at a round number with prior reactions, at the bottom of a channel, at the
termination of a measured move. The pattern is essentially a **double rejection** at one price.

## 5. Interpretation
Two separate attempts to break a price both failed at the same level. That is a small but real
statement about supply/demand at that price. Because it requires no meaningful body or gap
structure, it is treated as weaker evidence than engulfing or morning star.

## 6. Confirmation requirements
- Minimum: candle 3 closes above the higher of the two candles' bodies.
- Good: close above the higher of the two highs.
- Strong: break of the minor swing high, volume expansion, retest holds.
- Invalidated: any close below the matched lows.

## 7. Volume
More meaningful when candle 2's volume exceeds candle 1's — the second rejection carried more
participation. Two quiet candles at the same low can simply be a paused market. If volume is absent
from the chart, downgrade one reliability band and demand full price confirmation.

## 8. Paper-trade entry conditions (illustrative)
```
Long trigger  : close above max(high₁, high₂)
Entry zone    : trigger level ± 0.1 × ATR
Invalidation  : below min(low₁, low₂) − 0.25 × ATR
Targets       : T1 nearest prior swing high · T2 measured: decline height × 0.5 · T3 major resistance
Tight-stop alt: some traders use the matched low directly; expect more stop-outs from intraday noise
```

## 9. Invalidation
Close below the matched lows; price stalls at the level for many candles without progress; the
matched low sits inside a larger breakdown structure.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| "Matched" lows that differ by more than 0.25 ATR | Enforce the tolerance numerically |
| Pattern mid-range with no level | Location filter |
| Both candles small and quiet | Require range ≥ recent average |
| Equal lows are simply a limit-order cluster | Requires the following bullish close; do not pre-empt |
| Appears repeatedly in a downtrend | Repeated tweezers down a trend = the trend is absorbing them |

## 11. Historical evidence — honest position
A commonly cited but weakly documented pattern; the definition is not standardised across sources
(some require matching closes, some matching lows). Because definitions vary, published statistics
are not comparable. Treat as a *location confirmation* rather than a standalone signal.

## 12. Worked example (illustrative, fictional)
```
Instrument: PQR · 15m · decline 240 → 231; support zone 230.5–231.2
Candle 1: o232.4 h232.8 l230.9 c231.3 (bear)
Candle 2: o231.2 h232.6 l230.95 c232.5 (bull)  |low1 - low2| = 0.05 ≤ 0.1 ATR(15m)=0.3 ✔
Volume: C2 = 1.5× C1 ✔ · Status: CONFIRMED
Entry 232.7 / stop 230.6 (risk 2.1) / T1 234.8 (1.0R) / T2 237.2 (2.14R)
Verdict: WAIT — T1 fails; a retest entry at 231.9 gives risk 1.3 → T1 2.23R ✔
```

## 13. Beginner summary (Hinglish)
**Tweezer bottom:** do lagatar candles jinki **low bilkul same** (ya lagbhag same) ho, girte market
ke baad.

**Matlab:** ek hi price par do baar selling aayi aur do baar reject hui. Isliye woh level important
ban jata hai.

**Entry:** jab price dono candles ki high ke upar close kare.

**Stop:** dono lows ke neeche.

**Yaad rakho:** yeh akela strong signal nahi hai. Sirf support ke saath mil kar kaam karta hai.

## 14. Exercise
Find three tweezer bottoms. For each, measure the exact low difference in ATR units. Note which ones
you would have accepted under the 0.1 ATR rule. Then explain in one line why a strict tolerance
matters: with a loose tolerance, *every* support test becomes a "tweezer".

---
*See also: [`tweezer-top.md`](tweezer-top.md) · [`harami.md`](harami.md)*
