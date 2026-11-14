# Cup and Handle

**Type:** Continuation (bullish) · **Bars:** typically 30–200 (a longer-horizon pattern)

## 1. Shape
1. **Cup** — a rounded U-shaped correction: price declines, bases, and recovers to roughly the prior high.
2. **Handle** — a small, shallow pullback near the rim after the recovery.
3. **Breakout** — a close above the rim, typically while the handle is completing.

```
      rim ─────╲__╱───────  <- handle (shallow)
        ╱                ╲
      ╱                    ╲
    ╱                        ╲
   ╲                          ╱
    ╲________________________╱
             cup
```

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | A prior uptrend (the pattern is a continuation, not a bottom-fishing tool) |
| 2 | The cup is **rounded**, not V-shaped — a sharp V is a different pattern (and usually weaker) |
| 3 | Cup depth typically 12–35% (deeper cups in high-volatility instruments; shallower in indices) |
| 4 | The right side of the cup recovers to near the prior high (the rim) |
| 5 | The **handle** pulls back shallowly — conventionally 5–15% of price, and less than half the cup depth |
| 6 | The handle drifts down or sideways, on **contracting volume** |
| 7 | Confirmation: a **close above the rim** (the handle's high or the cup's high) with volume expansion |

## 3. Volume
| Stage | Expected |
|-------|----------|
| Cup's decline | Declining or moderate volume |
| Cup's base | Low volume (apathy) |
| Cup's right side | Rising volume |
| Handle | **Contracting** volume — critical |
| Breakout | Expansion |

A handle on rising volume is a red flag: it suggests distribution rather than a final shakeout.

## 4. Confirmation and entry
```
Standard     : close above the rim + volume ≥ 1.3× average
Conservative : breakout, then a retest of the rim that holds
Aggressive   : buy the handle's low with a tight stop (worse — the pattern is not complete)
Never        : buy in the middle of the cup (no pattern yet)
```

## 5. Measurement
```
target = rim + cup depth
cup depth = rim − cup low
```
Worked: rim 500, cup low 440 (depth 60) → target 560.

Alternative: measure the handle's depth and project — less standard, and it gives smaller targets. State which
you used.

## 6. Invalidation
| Event | Meaning |
|-------|---------|
| Close below the handle's low | The handle failed; the pattern is void |
| Handle deeper than ~half the cup | Not a handle — a new decline |
| V-shaped cup | Different (weaker) pattern; reframe |
| Breakout then close back below the rim | Failed breakout |
| Cup's right side fails to reach near the rim | Incomplete cup; `DEVELOPING` |

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| V-shaped recovery called a cup | Require roundness |
| Handle too deep | Rule 5 |
| Handle on rising volume | Volume filter |
| Breakout into a major resistance | Room check |
| Cup after a multi-year top rather than in an uptrend | Rule 1 |
| Pattern identified only in hindsight because the "handle" is one bar | Require a real handle (several bars) |

## 8. Honest note on this pattern

The cup and handle is popular in retail literature and is often presented with impressive-sounding success
rates. Those claims usually lack a stated sample, definition or cost model. The pattern's *definition* also
varies widely between sources (cup depth tolerance, handle depth tolerance, minimum duration), which makes
published statistics non-comparable.

Treat it as a structured way to describe "a rounded correction recovered, then a shallow final pullback was
absorbed." That description is useful. A claimed percentage edge is not something this repository will assert.

## 9. Worked example (fictional)
```
Instrument STU · Daily · prior uptrend 430 → 505
Cup: decline to 462 (depth 43 = 8.5% — shallow but acceptable in a low-vol instrument),
     rounded base over 6 weeks, recovery to 502 on rising volume
Handle: 8 bars, 502 → 493 (1.8% depth, well under half the cup) on 0.6× volume ✔
Breakout: close 507 on 2.0× volume → CONFIRMED
target = 505 + 43 = 548
Invalidation: close below 491 (handle low)
Retest entry 506 · stop 492 · risk 14 · T1 528 (prior swing high) = 1.57R ✔ · T2 548 = 3.0R ✔
Verdict: BULLISH SCENARIO on the retest trigger, with T1 just clearing the 1.5R gate — state that
         it is marginal, not comfortable.
```

## 10. Beginner summary (Hinglish)
**Cup and handle:** pehle ek U-shaped (round) correction (**cup**), phir rim ke paas chhota sa pullback
(**handle**), phir rim ke upar breakout.

**Matlab:** correction ke baad buyers ne poora recovery kiya, aur last mein jo chhota pullback aaya woh kam
volume par absorb ho gaya — matlab demand strong hai.

**Handle ka volume kam hona zaroori hai.** Agar handle par volume badh raha hai, to woh distribution ho sakta hai.

**Target:** rim + cup ki depth. **Stop:** handle ki low ke neeche.

**Galti:** V-shaped recovery ko cup samajhna — woh cup nahi hai.

## 11. Exercise
Find a cup and handle and a V-shaped recovery. Measure each cup's roundness (how many bars near the low),
handle depth as a % of cup depth, and handle volume. Then check follow-through. Write down which of the three
measurements you would use as your quality filter.

---
*See also: [`rounding-bottom` concepts in `double-bottom.md`](double-bottom.md) · [`bull-flag.md`](bull-flag.md) ·
[`../indicators/volume-profile.md`](../indicators/volume-profile.md)*
