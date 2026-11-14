# Double Bottom

**Type:** Reversal (bottoming) · **Bars:** typically 15–60

## 1. Shape
Two troughs at approximately equal prices, separated by a peak. The **neckline** is drawn at that peak.
Confirmation requires a close above it.

```
       ╱╲              ╱╲
      ╱  ╲            ╱  ╲___
     ╱    ╲          ╱
    ╱      ╲        ╱
   ╱        ╲______╱
  ╱          trough        trough
```

## 2. Formation rules

| # | Rule |
|---|------|
| 1 | Prior **downtrend** |
| 2 | Two troughs at approximately the same price (1–3% tolerance, or ≤0.3 × ATR — state which) |
| 3 | A distinct peak between them (the neckline) |
| 4 | Troughs separated by enough bars to be independent attempts |
| 5 | Second trough often comes on a **volume spike** (capitulation) then recovery |
| 6 | Confirmation: a **close above the neckline** |

## 3. Volume
| Stage | Expected |
|-------|----------|
| First trough | Heavy selling |
| Neckline peak | Lower volume |
| Second trough | Often a volume climax — the last sellers |
| Breakout | Expansion — required |

## 4. Confirmation and entry
```
Standard     : close above the neckline with volume expansion
Conservative : close above the neckline + a retest that holds
Aggressive   : break of the neckline peak's high before the close (weaker)
```

## 5. Measurement
```
height = |neckline − trough|
target = neckline + height
```
Worked: troughs 410, neckline 448 → height 38 → target 486.

## 6. Invalidation
| Event | Meaning |
|-------|---------|
| Close below both troughs | Structure destroyed; downtrend resumes |
| Close back below the neckline after a break | Failed pattern (bull trap) |
| Second trough meaningfully lower | Not a double bottom — a continuation of the decline |
| Neckline never breaks | `DEVELOPING` forever; not a trade |

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Two equal lows, no neckline break | Require the break |
| Troughs 2 bars apart | Require independence |
| Tolerance too wide | State the tolerance and keep it tight |
| "Double bottom" in a range | Require a prior downtrend |
| Breakout into heavy resistance | Room check |
| Second trough with *low* volume and no spike | Weaker profile — downgrade reliability |
| Break on a wick | Require a close |

## 8. Related: the "stop-hunt below equal lows"
Two equal lows are an obvious place for stops. Price frequently dips slightly below both and closes back above
— a sweep. If that happens and then the neckline breaks, the pattern is arguably stronger, because the
remaining sellers were cleared out. Treat the sweep as an observation and note it, not as proof of intent.

## 9. Worked example (fictional)
```
Instrument JKL · Daily · downtrend 500 → 405
Trough 1: 408 (vol 2.4M) · neckline peak 446 (vol 1.1M) · trough 2: 407 (vol 4.1M — climax)
Breakout: close 452 on 3.0M (2.0× average) → CONFIRMED
height = 446 − 408 = 38 → measured target 484
Structural target: prior swing high 476 (nearer); 50-EMA at 470
Invalidation: close below 402 (troughs − buffer)
Retest entry 447 · stop 404 · risk 43 · T1 470 = 0.53R FAIL
Note: the available structure is too near for an acceptable R:R at this stop distance.
Honest verdict: WAIT, or look for a lower-timeframe entry to shrink risk.
```

## 10. Beginner summary (Hinglish)
**Double bottom:** downtrend ke end mein do barabar lows, beech mein ek peak. Peak ki line = neckline.

**Matlab:** do baar ek hi price par selling aayi aur absorb ho gayi, aur doosri baar volume spike (capitulation)
ke saath.

**Signal:** neckline ke **upar close** hone par.

**Target:** neckline + height. **Stop:** dono lows ke neeche.

**Dhyan:** do barabar lows dekh kar turant khareedna galti hai. Break chahiye, aur R:R check bhi.

## 11. Exercise
Find a double bottom where the second trough has a clear volume spike and one where it doesn't. Compare the
follow-through. Then check the R:R at the breakout close versus at the retest entry — write down which entry
convention you would adopt and why.

---
*See also: [`double-top.md`](double-top.md) · [`triple-bottom.md`](triple-bottom.md) · [`inverse-head-and-shoulders.md`](inverse-head-and-shoulders.md)*
