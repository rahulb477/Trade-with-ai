# Bull Flag

**Type:** Continuation (bullish) · **Bars:** typically 5–25 (short by design)

## 1. Shape
Two parts:

1. **Pole** — a sharp, nearly vertical advance (the "flagpole").
2. **Flag** — a shallow, orderly drift **down or sideways** that stays near the top of the pole, contained
   within a small channel.

```
        │╲╱╲╱╲        <- flag: shallow drift, tight range
        │
        │  pole       <- sharp advance
        │
        │
```

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | A sharp prior advance (the pole): typically ≥ 3–5 ATR or ≥5% within a few bars |
| 2 | The flag is **shallow**: retracement usually ≤ 50% of the pole (≤38.2% is tighter, better) |
| 3 | The flag's range is narrow relative to the pole, with a slight downward or flat slope |
| 4 | Duration is short relative to the pole's speed (flags are pauses, not consolidations of weeks) |
| 5 | Volume **contracts** during the flag |
| 6 | Confirmation: a **close above the flag's upper boundary** with volume expansion |

## 3. Volume
The signature profile:
- Pole: **high volume** (the move is real)
- Flag: **contracting volume** (profit-taking without distribution)
- Breakout: **volume expansion** — required

Flag volume that is *high* suggests distribution rather than a pause. That is the main failure profile.

## 4. Confirmation and entry
```
Standard     : close above the flag's upper boundary on ≥1.3× average volume
Conservative : breakout then a retest of the flag's upper boundary that holds
Aggressive   : buy near the flag's lower boundary with a tight stop (best R:R, higher failure rate)
Never        : buy in the middle of the flag with no confirmation
```

## 5. Measurement
```
target = breakout point + pole height
pole height = pole high − pole low
```
Worked: pole 100 → 112 (height 12), flag 108–112, breakout 113 → target 125.

A conservative alternative is 50–61.8% of the pole height projected. State which you used.

## 6. Invalidation
| Event | Meaning |
|-------|---------|
| Close below the flag's low | The pause became a reversal; the pole is being retraced |
| Retracement > 50% of the pole | Weak flag; downgrade |
| Breakout then close back inside | Failed breakout |
| Flag dragging on for many bars | It is now a consolidation; the flag logic no longer applies |

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Steep advance on *declining* volume, then a "flag" | No real pole; skip |
| Flag retracing most of the pole | Rule 2 |
| Breakout on low volume | Volume filter |
| Flag at a major resistance | Room check |
| Confusing with a bull pennant | Pennant converges to a point; flag is a parallel channel |
| A 15% pullback called a "flag" | That is a correction, not a flag |
| Buying the flag's midpoint | No confirmation |

## 8. Why flags work when they work
Interpretation: a fast advance attracts quick profit-taking; if that selling is absorbed without price giving
back much, demand is strong and the next leg can be as large as the first. The shallow depth and contracting
volume are what distinguish absorption from distribution.

## 9. Worked example (fictional)
```
Instrument HIJ · 15m · pole 460 → 478 (height 18) over 6 bars on 3× volume
Flag: 12 bars drifting 477 → 472 in a narrow channel · volume 0.5× average ✔ (contracting)
Breakout: close 478.6 on 2.4× average → CONFIRMED
target = 478.6 + 18 = 496.6
Invalidation: close below 471 (flag low)
Entry on retest 477.8 · stop 470.5 · risk 7.3 · T1 488 (prior swing high) = 1.40R (marginal)
T2 496.6 = 2.58R ✔
Verdict: acceptable only with T2 as the primary target — or with a tighter stop below the flag's last
         higher low at 474 (risk 3.8 → T1 2.6R, T2 4.9R). State which stop and why.
```

## 10. Beginner summary (Hinglish)
**Bull flag:** ek tez upar ki move (**pole**), phir thodi si neeche/sideways drift jo tight range mein rahe
(**flag**), phir upar breakout.

**Matlab:** log profit book kar rahe hain, par selling itni kam hai ki price zyada neeche nahi aata — demand
strong hai.

**Volume ka pattern:** pole par zyada, flag mein **kam**, breakout par **fir zyada**. Yeh sabse zaroori clue
hai.

**Target:** pole ki height, breakout se upar. **Stop:** flag ki low ke neeche.

**Galti:** flag ke beech mein khareedna. Confirmation (flag ki upper boundary ke upar close) chahiye.

## 11. Exercise
Find three bull flags. For each, record: pole height in ATR units, flag retracement % of the pole, flag volume
versus the 20-bar average, breakout volume multiple. Then check follow-through. Rank the three by quality and
write the two checks you would use before entering.

---
*See also: [`bear-flag.md`](bear-flag.md) · [`pennant.md`](pennant.md) ·
[`../candlesticks/rising-three-methods.md`](../candlesticks/rising-three-methods.md)*
