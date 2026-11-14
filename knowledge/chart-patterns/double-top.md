# Double Top

**Type:** Reversal (topping) · **Bars:** typically 15–60

## 1. Shape

Two peaks at approximately the same price, separated by a trough. The **neckline** is drawn at that trough's
low. Confirmation requires a close below it.

```
        ╱╲          ╱╲
       ╱  ╲        ╱  ╲
      ╱    ╲      ╱    ╲
     ╱      ╲    ╱      ╲
    ╱        ╲__╱        ╲
               ╲          ╲
             neckline      ╲___
```

## 2. Formation rules

| # | Rule |
|---|------|
| 1 | Prior **uptrend** |
| 2 | Two peaks at approximately the same price — tolerance commonly 1–3% of price (or ≤0.3 × ATR); state the tolerance used |
| 3 | A clear trough between them (the neckline) at least a few bars deep |
| 4 | The two peaks are separated by enough bars to be independent attempts (not two adjacent bars) |
| 5 | Second peak volume typically **lower** than the first |
| 6 | Confirmation: a **close below the neckline** |

**Two touches of a resistance level without a neckline break is not a double top** — it is a resistance test.
This distinction prevents most false double tops.

## 3. Volume

| Stage | Expected |
|-------|----------|
| First peak | High volume |
| Trough | Lower |
| Second peak | **Lower than the first** — the rally lacks participation |
| Neckline break | Expansion |

Declining volume into the second peak is the pattern's core evidence of weakening demand.

## 4. Confirmation and entry

```
Conservative : close below the neckline, then a failed retest
Standard     : close below the neckline + volume expansion
Aggressive   : short the rejection at the second peak (earlier; much lower reliability)
```

## 5. Measurement

```
height = |peak − neckline|
target = neckline − height
```

Worked: peaks 720, neckline 690 → height 30 → target 660.

## 6. Invalidation

| Event | Meaning |
|-------|---------|
| Close above the peaks | The level was absorbed; bullish continuation |
| Close back above the neckline after a break | Failed pattern (bear trap) |
| Second peak meaningfully above the first | Not a double top — it is a continuation |
| Neckline never breaks | The pattern remains `DEVELOPING` indefinitely; it is not a trade |

## 7. Common false signals

| False signal | Guard |
|--------------|-------|
| Equal highs with no neckline break | Require the break |
| Peaks separated by only 2–3 bars | Require independence |
| Tolerance too wide (e.g. 8%) | State and tighten the tolerance |
| "Double top" inside a range | Require a prior uptrend |
| Break on low volume | Volume filter |
| Second peak on *higher* volume | Suggests absorption, not distribution — downgrade |
| Pattern at a major breakout level | Could be a consolidation before continuation |

## 8. Related pattern: the "equal highs" liquidity read

Two equal highs create an obvious stop cluster above them. Some traders read this as a liquidity pool and
expect a sweep before a reversal. That is a **hypothesis** (see `knowledge/smart-money/`), not a rule. If the
sweep occurs and price then closes back below the highs, that behaviour is consistent with the hypothesis — but
it does not prove institutional intent.

## 9. Worked example (fictional)

```
Instrument GHI · 4H · uptrend 640 → 724
Peak 1: 721 (vol 1.2M) · trough 690 (vol 0.6M) · Peak 2: 723 (vol 0.8M)
Tolerance |721 − 723|/721 = 0.28% ✔ · separation 14 bars ✔
Breakout: close 687 on 1.5M (1.8× average) → CONFIRMED
height = 721 − 690 = 31 → measured target 659
Structural target: prior swing low 665 (nearer)
Invalidation: close above 726 (peaks + buffer)
Retest entry 689 · stop 727 · risk 38 · T1 665 = 0.63R FAIL at this entry
Better: enter the failed retest at 694 with stop 724 → risk 30 → T1 665 = 0.97R (still marginal)
Honest verdict: WAIT — the stop is too wide relative to the target. Say so.
```

## 10. Beginner summary (Hinglish)

**Double top:** uptrend ke end mein do barabar highs, beech mein ek trough. Trough ki line = neckline.

**Matlab:** doosri baar upar jaane ki koshish fail hui, aur us baar volume bhi kam tha — buyers thak gaye.

**Asli signal:** neckline ke **neeche close**. Sirf do barabar highs dekhna double top nahi hai.

**Target:** neckline se pattern ki height jitna neeche.

**Stop:** peaks ke thoda upar.

**Badi galti:** R:R check kiye bina pattern dekh kar short karna. Bahut baar stop itna bada hota hai ki target
tak pahunchne ka koi matlab nahi bachta — us case mein WAIT hi sahi answer hai.

## 11. Exercise

Find three double tops (with the neckline break) and three resistance tests (two touches, no break). Compare
what happened over the next 20 bars. Then write the one-line test you would apply to tell them apart *before*
the outcome was known.

---
*See also: [`double-bottom.md`](double-bottom.md) · [`triple-top.md`](triple-top.md) ·
[`../workflows/trap-detection.md`](../../workflows/trap-detection.md)*
