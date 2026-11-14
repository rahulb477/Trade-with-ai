# Pennant

**Type:** Continuation (direction of the pole) · **Bars:** typically 5–20

## 1. Shape
A sharp directional move (the pole) followed by a **small symmetrical triangle** — converging boundaries with
contracting volatility. It is essentially a flag whose consolidation converges instead of forming a parallel
channel.

```
      ╱╲╱╲      <- small converging consolidation
     ╱
    ╱  pole
   ╱
```

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | A sharp prior move (the pole) in the continuation direction |
| 2 | A **converging** consolidation (≥2 lower highs and ≥2 higher lows) |
| 3 | The consolidation is small relative to the pole (typically retracing ≤38.2–50%) |
| 4 | Short duration |
| 5 | Volume contracts through the pennant |
| 6 | Confirmation: a close beyond the pennant in the pole's direction, with volume |

## 3. Pennant vs flag vs triangle

| Feature | Pennant | Flag | Triangle |
|---------|---------|------|----------|
| Boundaries | Converging | Parallel | Converging |
| Prior pole required | Yes | Yes | No |
| Size | Small | Small | Larger |
| Duration | Short | Short | Longer |
| Bias | Direction of the pole | Direction of the pole | Prior trend, or neutral |

The distinction matters mainly for measurement and for how much the pattern is trusted: a pennant without a
pole is just a small triangle.

## 4. Volume
Pole: high. Pennant: contracting. Breakout: expanding. Required, not optional.

## 5. Measurement
```
target = breakout point ± pole height
```
Worked: pole 500 → 520 (height 20), pennant 516–520, breakout 521 → target 541.

## 6. Invalidation
Close beyond the pennant in the *opposite* direction of the pole (the continuation failed); retracement of more
than half the pole.

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| "Pennant" with no pole | It is a triangle |
| Pole on declining volume | No genuine momentum to continue |
| Breakout on low volume | Volume filter |
| Pennant at a major level in the opposite direction | Room check |
| Very tiny pennant on a 1-minute chart | Noise-dominated |
| Forcing direction when the pole's trend conflicts with the higher timeframe | Context |

## 8. Worked example (fictional)
```
Instrument NOP · 15m · pole 1_180 → 1_216 on 3.1× volume (height 36)
Pennant: 10 bars, lower highs 1_214→1_210, higher lows 1_202→1_206, volume 0.5×
Breakout: close 1_215.5 on 2.3× → CONFIRMED
target = 1_215.5 + 36 = 1_251.5
Invalidation: close below 1_201 (pennant low)
Retest entry 1_214 · stop 1_203 · risk 11 · T1 1_232 (prior high) = 1.64R ✔ · T2 1_251.5 = 3.4R ✔
Verdict: BULLISH SCENARIO on the retest trigger. Note that a breakout-chasing entry at 1_216 would
         still work (risk 15 → T1 1.07R) but fails the 1.5R gate — the retest is what makes it valid.
```

## 9. Beginner summary (Hinglish)
**Pennant:** ek tez move (**pole**), phir chhota sa **converging** consolidation (triangle jaisa).

**Matlab:** move ke baad chhota pause — aur phir usi direction mein continuation. Flag jaisa hi, bas boundaries
converge karti hain (parallel nahi).

**Signal:** pennant ke bahar close, pole ki direction mein, volume ke saath.

**Target:** pole ki height, breakout se project.

**Galti:** bina pole ke pattern ko pennant kehna. Woh sirf chhota triangle hai.

## 10. Exercise
Find a pennant and a flag on the same instrument. Note the boundary geometry for each and the measured target.
Compare which gave the better R:R at the retest entry. Write one line on whether the geometry or the entry
timing mattered more.

---
*See also: [`bull-flag.md`](bull-flag.md) · [`bear-flag.md`](bear-flag.md) · [`symmetrical-triangle.md`](symmetrical-triangle.md)*
