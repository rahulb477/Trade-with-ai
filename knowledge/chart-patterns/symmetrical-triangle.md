# Symmetrical Triangle

**Type:** Continuation / neutral resolution · **Bars:** typically 20–80

## 1. Shape
Both boundaries converge: a **falling upper line** (lower highs) and a **rising lower line** (higher lows).
Neither is flat. The market compresses toward an apex with no inherent directional bias.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | ≥2 lower highs forming a falling line |
| 2 | ≥2 higher lows forming a rising line |
| 3 | The lines converge (not parallel — parallel is a channel or rectangle) |
| 4 | A prior trend exists; the pattern usually continues it |
| 5 | Breakout: a **close beyond either boundary**, with volume |
| 6 | Breakout should occur before roughly 70–75% of the way to the apex — later breakouts are weaker |

## 3. Volume
Volume typically contracts through the pattern and expands on the breakout. Because the direction is unknown
until the break, **volume plus the breakout close** is the entire signal.

## 4. Confirmation and entry
```
Standard     : close beyond a boundary + volume ≥ 1.3× average
Conservative : breakout, then a retest of the broken boundary that holds
Straddle alt : bracket both boundaries; accept that one side loses
Never        : enter *inside* the triangle expecting a direction
```

## 5. Measurement
```
height = widest part of the triangle (typically the opening range)
target = breakout point ± height
```
Worked: high 640, low 600 at the widest → height 40. Breakout up at 622 → target 662.

## 6. Invalidation
Close back inside after a breakout (failed breakout — very common with triangles); a breakout that dies at the
apex.

## 7. Common false signals
| False signal | Guard |
|--------------|-------|
| Drawing the lines through noise | Require ≥2 real touches each side |
| "Triangle" that is actually a wedge (both lines same direction) | Check directions |
| Break with no volume | Volume filter |
| Break at the apex | Require room; a break at full convergence has little follow-through |
| Pre-empting direction | The pattern is neutral; wait |
| Confusing a pennant with a triangle | Pennant requires a prior pole and is small/short |

## 8. The honest statement about direction

A symmetrical triangle says **volatility is compressing and a resolution is likely**. It does not say which way.
Any source claiming a reliable directional bias is making a claim that must be backed by a measured sample on a
specific market. Do not repeat such claims as fact.

The one legitimate directional hint is **the prior trend**: continuation is the more common outcome, so a
triangle in an uptrend has an upward lean. That is a tendency, and it fails often enough that the invalidation
is what actually protects you.

## 9. Worked example (fictional)
```
Instrument YZA · 1D · uptrend 560 → 640, then compression
Lower highs: 640 → 634 → 629    Upper... (falling line)
Higher lows: 598 → 606 → 613    (rising line)
Widest height = 640 − 598 = 42
Breakout: close 631 on 2.0× volume → CONFIRMED upward
Measured target = 631 + 42 = 673
Invalidation: close back below 626 (the last higher low + buffer)
Retest entry 632 · stop 624 · risk 8 · T1 660 (prior high area) = 3.5R ✔ · T2 673 = 5.1R
Note: if instead price closes 611 (below the rising line), the same measurement applies downward:
      611 − 42 = 569, and the invalidation becomes a close above the falling line.
```

## 10. Beginner summary (Hinglish)
**Symmetrical triangle:** upar wali line neeche ja rahi hai, neeche wali upar — dono mil rahi hain (compress).

**Matlab:** volatility compress ho rahi hai, bada move aayega. **Direction pata nahi.**

**Kya karein:** break hone do. Jis taraf close ho **volume ke saath**, us taraf.

**Target:** triangle ki sabse badi height, breakout point se project.

**Badi galti:** andar baith kar direction guess karna. Pattern neutral hai — sirf compression ka signal hai.

## 11. Exercise
Find three symmetrical triangles. For each, record: prior trend, breakout direction, volume multiple, and
whether the breakout was before or after 70% of the way to the apex. Then check which of those variables was
associated with follow-through. Report your sample size honestly.

---
*See also: [`ascending-triangle.md`](ascending-triangle.md) · [`pennant.md`](pennant.md) · [`rectangle.md`](rectangle.md)*
