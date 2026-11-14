# Descending Triangle

**Type:** Continuation (usually bearish) · **Bars:** typically 20–80

## 1. Shape
A **flat lower boundary** (horizontal support tested repeatedly) and a **falling upper boundary** (lower
highs). The range narrows as sellers press down against fixed support.

```
    ╲      ╲      ╲              falling resistance (lower highs)
      ╲      ╲      ╲
        ╲      ╲      ╲
  ────────────────────────────   flat support
```

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Horizontal support tested **≥2 times** |
| 2 | At least **2 lower highs** forming a falling trendline |
| 3 | Converging boundaries |
| 4 | A prior trend exists — usually down |
| 5 | Breakout: a **close below the flat support** |

**Distinguish from a falling wedge:** in a wedge, **both** boundaries slope down. Here the bottom is flat.

## 3. Volume
Contraction during formation, then expansion on the breakdown. A breakdown on contracting volume is the classic
failed pattern.

## 4. Confirmation and entry
```
Standard     : close below support + volume ≥ 1.3× average
Conservative : breakdown then a failed retest of the support from below
Aggressive   : short the falling resistance inside the triangle (worse if it breaks up)
```

## 5. Measurement
```
height = highest point of the triangle − support
target = support − height
```
Worked: support 240, first high 262 → height 22 → target 218.

## 6. Invalidation
Close above the falling resistance (the pattern failed upward); breakdown then a close back above support.

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Support tested only once | Require ≥2 |
| Both boundaries falling | That is a falling wedge — which is often *bullish* |
| Breakdown on low volume | Volume filter |
| Apex nearly converged | Late breakouts have poor follow-through |
| Breakdown into a major support cluster | Room check |
| Pattern at the *end* of a long decline | Could be basing/capitulation rather than continuation |

## 8. Why the falling wedge confusion is dangerous
A descending triangle and a falling wedge look similar on a casual glance, but the documented implications are
opposite: the triangle is usually bearish-continuation, while the falling wedge is usually **bullish** (a
declining structure that loses momentum and resolves upward). Getting this wrong inverts the trade. Always
check whether the **lower** boundary is flat or falling.

## 9. Worked example (fictional)
```
Instrument VWX · 1D · downtrend; support 412 tested three times (1_412 appears at 3 dates)
Lower highs: 440 → 431 → 424
Height = 440 − 412 = 28 → measured target 384
Breakdown: close 408.5 on 1.8× average volume → CONFIRMED
Retest entry 410 · stop 418 (above the last lower high 416 + buffer) · risk 8
T1 396 (prior swing low) = 1.75R ✔ · T2 384 (measured) = 3.25R ✔
Verdict: BEARISH SCENARIO on the failed-retest trigger. Point out that the short must be closed
before the session ends if this is a cash-equity intraday position in India (see markets/india/).
```

## 10. Beginner summary (Hinglish)
**Descending triangle:** neeche **flat support**, upar **falling resistance** (lower highs).

**Matlab:** sellers har baar kam price par bech rahe hain, buyers ek hi level bacha rahe hain. Support aksar
toot jata hai.

**Signal:** support ke **neeche close**, volume ke saath.

**Target:** support − height. **Stop:** last lower high ke upar.

**Sabse khatarnak galti:** neeche wali line bhi neeche ja rahi ho to woh **falling wedge** hai — aur uska
matlab aksar **bullish** hota hai. Dono ka signal ulta hai.

## 11. Exercise
Find a descending triangle and a falling wedge. For each, note whether the lower boundary was flat or falling,
and what happened after resolution. Write two lines: one rule to tell them apart, and one sentence on what the
consequence of confusing them would be.

---
*See also: [`ascending-triangle.md`](ascending-triangle.md) · [`falling-wedge.md`](falling-wedge.md)*
