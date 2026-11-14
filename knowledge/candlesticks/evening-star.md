# Evening Star

**Group:** Bearish reversal · **Candles:** 3 · **Reliability band:** Higher
**Detector:** `patterns.detect_evening_star`

## 1. What it is
The mirror of the morning star, at a top:

1. A **long bullish** candle continuing the advance.
2. A **small-bodied** star trading **above** candle 1's body — buying stalls.
3. A **long bearish** candle closing well into candle 1's body.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Prior trend upward |
| 2 | Candle 1 bullish with a long body (`body₁ ≥ 1.0 × avg_body`) |
| 3 | Candle 2 small body (`body₂ ≤ 0.4 × body₁`), positioned **above** candle 1's body |
| 4 | Candle 3 bearish, closing **below the midpoint of candle 1's body** |
| 5 | Candle 3 closes well into candle 1: `close₃ ≤ open₁ + 0.5 × body₁` |
| 6 | All three closed |

Morning/evening **doji** star variant: candle 2 is a doji — a stronger indecision read.

## 3. Anatomy
```
                    ┌──┐   <- star above candle 1
                    └──┘
 ┌──────┐
 │      │                  
 │      │
 └──────┘
              ┌──────┐   <- candle 3 closes below the midpoint of candle 1
              │      │
              └──────┘
```

## 4. Where it means something
At resistance after a sustained advance; at the top of an accelerating trend; at a measured-move or
Fib extension completion; after a gap-up that stalls.

## 5. Interpretation
Buying stopped making progress (candle 2), then sellers took control decisively (candle 3). The
three-interval structure is what gives it weight. The pattern is more informative at the end of an
*extended* move than after a short bounce.

## 6. Confirmation requirements
Candle 3's close completes it. Additional: a fourth candle failing to reclaim candle 3's high;
break of the prior swing low; volume expansion on candle 3.

## 7. Volume
Ideal: high on candle 1 (climax buying), lower on the star, high on candle 3 (distribution).
High volume on the star with a small body can indicate a genuine battle at the top — still
informative, but interpret it as "supply is meeting demand here" rather than "vacuum".

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : candle 3 close, or break of candle 3's low
Entry zone     : candle 3 low ± 0.2 × ATR
Invalidation   : above the star's high (the highest point of the pattern) + 0.25 × ATR
Targets        : T1 candle 1's open (bottom of the bullish body)
                 T2 most recent swing low before the advance
                 T3 measured: advance height × 0.5–0.618 projected down
Sizing note    : the stop is wide (three candles + buffer); size down, not stop-widening
```

## 9. Invalidation
Close above the star's high; candle 3's body fully retraced within two candles; higher timeframe
still making higher highs on rising volume.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Loose definition (star not above candle 1's body) | Rule 3 numerically |
| Candle 3 closes only marginally into candle 1 | Require the midpoint rule |
| Appears in a range | Require a preceding advance |
| Profit-taking dip inside a strong uptrend | Require structure break for a short thesis |
| Repeated evening stars that keep failing in a bull market | Diminishing information; require HTF confirmation |

## 11. Historical evidence — honest position
Regarded in the literature as one of the more reliable bearish reversal formations due to its
three-condition structure; correspondingly less frequent. No number is asserted here. If you want a
base rate, measure it — and be aware that in strongly trending bull markets the pattern's failure
rate rises materially.

## 12. Worked example (illustrative, fictional)
```
Instrument: HIJ · 1D · advance 245 → 291 in 12 sessions; resistance 288–292
C1 o279 c288 (bull, body 9) · C2 o289.5 c290.2 (body 0.7, above C1 body ✔)
C3 o289 c281 (bear, body 8) → closes below C1 midpoint 283.5 ✔
Volume: 1.5×, 0.9×, 1.8× ✔ · Status: CONFIRMED
Entry 280.8 · stop 291.0 (risk 10.2)
T1 279 (C1 open) → 0.18R FAIL · T2 265 (prior swing low) → 1.55R ✔ · T3 251 → 2.92R ✔
Verdict: BEARISH SCENARIO is defensible only if the plan targets T2/T3 with a partial at T1 or
         ignores T1 entirely. Say so; do not present T1 as a viable target.
```

## 13. Beginner summary (Hinglish)
**Evening star:** morning star ka ulta — upar hone wala top pattern.

1. Badi green candle — buyers strong.
2. Chhoti candle upar — buyers thak gaye.
3. Badi red candle — sellers ne control liya aur pehli candle ke aadhe se neeche close kiya.

**Entry:** teesri candle ke close par ya uski low tootne par.

**Stop:** pattern ki sabse upar wali high (star ki high) ke thoda upar.

**Dhyan:** stop chhota karne ke liye stop ko andar mat kheencho — jo high toot gayi, thesis khatam.

## 14. Exercise
Find two evening stars: one after 12+ up candles, one after 3. Compare follow-through over 10 candles.
Write a rule for minimum prior extension, and test whether your rule would have excluded a valid
reversal in a longer sample.

---
*See also: [`morning-star.md`](morning-star.md) · [`shooting-star.md`](shooting-star.md) · [`doji.md`](doji.md)*
