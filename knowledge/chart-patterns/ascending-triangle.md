# Ascending Triangle

**Type:** Continuation (usually bullish) · **Bars:** typically 20–80

## 1. Shape
A **flat upper boundary** (horizontal resistance tested repeatedly) and a **rising lower boundary** (higher
lows). The range narrows as the rising support closes in on the flat resistance.

```
  ────────────────────────────   flat resistance
        ╱      ╱      ╱
      ╱      ╱      ╱              rising support (higher lows)
    ╱      ╱      ╱
```

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | A horizontal resistance level tested **≥2 times** (≥3 is better) |
| 2 | At least **2 higher lows** forming a rising trendline |
| 3 | The two lines converge (the range narrows) |
| 4 | A prior trend exists — usually up (the pattern is a pause in the trend) |
| 5 | Breakout: a **close above the flat resistance** |

**Distinguish from a rising wedge:** in a wedge, **both** boundaries slope upward. Here the top is flat. If the
top is also rising, it is a wedge — a different pattern with different implications.

## 3. Volume
Classic profile: volume tends to **contract** as the triangle narrows, then **expand** on the breakout. A
breakout on contracting volume is the most common failure.

## 4. Confirmation and entry
```
Standard     : close above resistance + volume ≥ 1.3× average
Conservative : close above resistance, then a retest that holds (best R:R)
Aggressive   : buy near the rising support inside the triangle (earlier, worse if it breaks down)
```

## 5. Measurement
```
height  = resistance − lowest point of the triangle
target  = resistance + height
```
A common alternative is to project the widest part of the pattern from the breakout point — the two methods
give slightly different numbers; state which you used.

Worked: resistance 500, widest low 470 → height 30 → target 530.

## 6. Invalidation
| Event | Meaning |
|-------|---------|
| Close below the rising support | Triangle broken down; the bullish bias is void |
| Breakout then close back inside | Failed breakout (bull trap) |
| Resistance never breaks | `DEVELOPING` indefinitely; not a trade |

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Flat "resistance" tested only once | Require ≥2 touches |
| Both boundaries rising | That is a rising wedge, not a triangle |
| Breakout on low volume | Volume filter |
| Apex too close | Late breakouts from a nearly-converged apex have poor follow-through; require room |
| R:R already poor at the breakout | Compute it; often the honest answer is WAIT for a retest |
| Ignoring the broader trend context | A triangle at the top of a trend can precede a reversal |

## 8. Why the bias is "usually" up
Higher lows mean buyers are willing to pay progressively more, while the flat top means sellers keep defending
one price. That is a compression of demand against fixed supply. Documented treats the ascending triangle as
bullish-biased — but "biased" is not "certain". Roughly a third of the time these resolve downward in practice,
which is why the invalidation matters.

## 9. Worked example (fictional)
```
Instrument STU · 15m · uptrend; resistance 1_240 tested at 09:45, 11:10, 13:05
Rising lows: 1_205 → 1_218 → 1_228
Height = 1_240 − 1_205 = 35 → measured target 1_275
Breakout: close 1_243.5 on 2.2× average volume → CONFIRMED
Retest entry 1_241 · stop 1_231 (below the last higher low 1_233, with buffer) · risk 10
T1 1_265 (prior swing high above) = 2.4R ✔ · T2 1_275 (measured) = 3.4R ✔
Verdict: BULLISH SCENARIO on the retest trigger. Note the entry is only valid on the retest hold, not on
the breakout bar itself (where the stop would be 12.5 away and T1 only 1.7R — still acceptable, but worse).
```

## 10. Beginner summary (Hinglish)
**Ascending triangle:** upar ek **flat resistance**, neeche **rising support** (higher lows) — range sikud raha hai.

**Matlab:** buyers dheere dheere zyada price dene ko tayyar hain, par sellers ek hi level par rok rahe hain.
Yeh pressure aksar upar ki taraf tootta hai.

**Signal:** resistance ke upar **close**, volume ke saath.

**Target:** resistance + triangle ki height. **Stop:** last higher low ke neeche.

**Badi galti:** agar upar wali line bhi upar ja rahi hai, to woh triangle nahi — **rising wedge** hai, jiska
matlab ulta hota hai.

## 11. Exercise
Find an ascending triangle and a rising wedge side by side. Draw both boundaries for each and write down which
one has a flat top. Then check what happened after each resolved. Write one line on why the flat top matters.

---
*See also: [`descending-triangle.md`](descending-triangle.md) · [`symmetrical-triangle.md`](symmetrical-triangle.md) ·
[`rising-wedge.md`](rising-wedge.md)*
