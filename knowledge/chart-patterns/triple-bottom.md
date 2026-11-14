# Triple Bottom

**Type:** Reversal (bottoming) · **Bars:** typically 25–80

## 1. Shape
Three troughs at roughly the same price with two intervening peaks. Neckline at the **higher of the two peaks**
(conservative) or a line through both.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Prior **downtrend** |
| 2 | Three troughs at approximately equal prices (1–3% tolerance) |
| 3 | Two distinct peaks between them |
| 4 | Real swings, not spikes |
| 5 | Volume often shows a capitulation spike at one trough and drying up at the others |
| 6 | Confirmation: a **close above the neckline** |

## 3. Volume
Two common profiles:
- **Climax-then-dry**: one trough with a volume spike, the others quiet → sellers exhausted.
- **Declining across all three**: progressively less selling pressure.

Either is consistent with a bottom; a *rising* volume into the third trough is a warning that selling persists.

## 4. Confirmation, entry, measurement
```
Confirmation : close above the neckline, volume ≥ 1.3× average
Entry        : neckline break, or a retest that holds
height       = |neckline − lowest trough|
target       = neckline + height
```

## 5. Invalidation
Close below all three troughs; close back below the neckline after a break; third trough meaningfully lower.

## 6. Common false signals
| False signal | Guard |
|--------------|-------|
| Three touches of support without a break | Require the neckline break |
| Very short timeframe | Noise |
| Troughs spread over months with intervening trends | Not one pattern |
| Breakout into an overhead supply zone | Room check |
| Rising volume into the third trough | Reconsider the read |

## 7. Worked example (fictional)
```
Instrument PQR · Daily · downtrend 300 → 251
Trough 1: 253 (vol 1.8M) · peak 268 · trough 2: 252 (vol 3.9M — climax) · peak 266 · trough 3: 254 (vol 1.0M)
Neckline = 268 (higher peak)
Breakout: close 271 on 2.6M (1.9× volume) → CONFIRMED
height = 268 − 251 = 17 → measured target 285
Structural target: 50-EMA 282; prior swing high 279
Invalidation: close below 248
Retest entry 269 · stop 247 · risk 22 · T1 279 = 0.45R FAIL
Verdict: WAIT — measured move is small relative to any defensible stop. A tight-stop variant
         (stop below the third trough at 252 → risk 17) still gives 0.59R. Not viable.
```

## 8. Beginner summary (Hinglish)
**Triple bottom:** teen barabar lows, beech mein do peaks. Upar wale peak ki line = neckline.

**Matlab:** market teen baar same support test karta hai aur teeno baar absorb hota hai — selling khatam.

**Signal:** neckline ke upar close.

**Target:** neckline + height. **Stop:** teeno troughs ke neeche.

**Dhyan:** stop door hota hai, isliye R:R aksar kharab hota hai. Arithmetic check karo, pattern dekh kar
trade mat lo.

## 9. Exercise
Compute the R:R at the breakout close for three triple bottoms. In how many was T1 ≥ 1.5R? Then compute the
same at the best retest entry. Write down whether the pattern or the *entry location* determined viability.

---
*See also: [`triple-top.md`](triple-top.md) · [`double-bottom.md`](double-bottom.md)*
