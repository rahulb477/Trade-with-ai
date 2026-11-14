# Bear Flag

**Type:** Continuation (bearish) · **Bars:** typically 5–25

## 1. Shape
1. **Pole** — a sharp decline.
2. **Flag** — a shallow, orderly drift **up or sideways**, staying near the bottom of the pole, inside a small
   rising channel.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Sharp prior decline (pole): ≥3–5 ATR or ≥5% in a few bars |
| 2 | Flag retracement ≤50% of the pole (≤38.2% better) |
| 3 | Narrow flag range, slight upward or flat slope |
| 4 | Short duration relative to the pole |
| 5 | Volume contracts during the flag |
| 6 | Confirmation: a **close below the flag's lower boundary** with volume |

## 3. Volume
Pole: high; flag: contracting; breakdown: expanding. This is the same profile as the bull flag, mirrored — and
it is the primary quality filter.

## 4. Confirmation and entry
```
Standard     : close below the flag's lower boundary on ≥1.3× average volume
Conservative : breakdown then a failed retest from below
Aggressive   : short near the flag's upper boundary with a tight stop
Never        : short mid-flag
Shortability : verify the instrument is shortable in your market/session. In India, cash-equity intraday
               shorts must be squared off before the close; delivery-based shorting requires securities
               lending. See markets/india/
```

## 5. Measurement
```
target = breakdown point − pole height
```
Worked: pole 240 → 228 (height 12), flag 229–232, breakdown 228.5 → target 216.5.

## 6. Invalidation
Close above the flag's high (the pause became a reversal upward); retracement >50% of the pole; breakdown then
a close back inside.

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Steep decline on declining volume, then a "flag" | No real pole |
| Deep retracement called a flag | Rule 2 |
| Breakdown on low volume | Volume filter |
| Flag into major support | Room check |
| Confused with a falling wedge | Wedge converges to a point; flag is a parallel channel |
| Shorting a stock in a strong uptrend just because a bear flag formed on a 5m chart | Higher timeframe context |

## 8. Worked example (fictional)
```
Instrument KLM · 1D · pole 320 → 296 (height 24) over 4 bars on 2.8× volume
Flag: 9 bars drifting 297 → 303 in a rising channel · volume 0.6× ✔
Breakdown: close 295.4 on 2.1× volume → CONFIRMED
target = 295.4 − 24 = 271.4
Invalidation: close above 305 (flag high)
Retest entry 296 · stop 304.6 · risk 8.6 · T1 284 (prior swing low) = 1.4R (marginal) · T2 271.4 = 2.86R ✔
Verdict: viable only with T2 as primary. Present the arithmetic honestly rather than implying T1 is enough.
```

## 9. Beginner summary (Hinglish)
**Bear flag:** pehle tez **neeche** ki move (pole), phir thoda upar/sideways drift (flag), phir neeche breakdown.

**Matlab:** log "dead cat bounce" kharid rahe hain, par selling abhi bhi strong hai — bounce absorb ho raha hai.

**Volume:** pole zyada, flag **kam**, breakdown fir **zyada**.

**Target:** pole ki height, breakdown se neeche. **Stop:** flag ki high ke upar.

**Dhyan:** India mein cash equity intraday short ko session end se pehle band karna hota hai — plan mein yeh
likho.

## 10. Exercise
Find two bear flags. Record the pole height in ATR, flag retracement %, and breakdown volume multiple. Then
check whether the measured target was reached before the invalidation. Compute the hit rate out of 2 and note
honestly that 2 is not a sample.

---
*See also: [`bull-flag.md`](bull-flag.md) · [`pennant.md`](pennant.md) · [`../markets/india/README.md`](../../markets/india/README.md)*
