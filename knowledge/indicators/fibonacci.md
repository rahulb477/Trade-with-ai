# Fibonacci Retracement and Extension

**Family:** Levels (not an oscillator) · **Common ratios:** 0.236, 0.382, 0.5, 0.618, 0.786 / ext 1.272, 1.618, 2.618
**Implementation:** `indicators.fib_levels(swing_low, swing_high, direction="up")`

## 1. Calculation

Retracement of an up-swing (low `L` → high `H`):

```
level(r) = H − r × (H − L)          for r in {0.236, 0.382, 0.5, 0.618, 0.786}
```

Extension beyond the swing (for targets):

```
ext(r) = H + (r − 1) × (H − L)      for r in {1.272, 1.618, 2.0, 2.618}
```

For a down-swing, mirror the arithmetic.

Note that 0.5 is **not** a Fibonacci ratio — it is included by convention because it frequently acts as a
level. 0.618 and 0.382 are the ratios with an actual mathematical basis (φ and 1−φ).

## 2. Interpretation

| Level | Conventional role |
|-------|-------------------|
| 0.236 | Shallow pullback — occurs in very strong trends |
| 0.382 | Normal pullback in a healthy trend |
| 0.5 | Midpoint; psychologically and structurally relevant |
| 0.618 | The "golden" retracement; the most-watched level |
| 0.786 | Deep retracement; a break here often means the swing fails |
| 1.272 / 1.618 | Common extension targets |

**Critical framing:** Fibonacci levels work (when they work) because many participants watch them, creating
clustered orders — a self-referential effect. They are not physical laws. A level with no other confluence
is weak; a 0.618 that coincides with prior support, a moving average, and a round number is strong.

## 3. Choosing the swing (the hard part)

The entire usefulness of the tool depends on the anchor:

1. Use the **most recent structural** swing (a swing high made by a decisive close, not a wick).
2. Prefer swings that changed market structure.
3. Prefer swings that are visible and obvious on the timeframe — not tiny 3-bar wiggles.
4. If two candidate swings give materially different levels, the retracement is not reliable. Say so.
5. On a screenshot, you can only use swings visible in the image — state the anchors you used.

## 4. Limitations

- **Anchor subjectivity.** Different anchors give different levels; this is the biggest weakness.
- **No timing information.** A level tells you *where*, not *when*.
- **Confirmation bias.** With five levels plus extensions, some level will always be "respected" in
  hindsight. This is the single most over-claimed tool in retail technical analysis.
- **Survivorship of levels.** Textbooks show the ones that worked; nobody publishes the ones that didn't.
- **No volume awareness.**

## 5. Combining

- **Fib + horizontal structure**: the strongest use. A 0.618 that sits on a prior support is a real zone.
- **Fib + EMA**: a 0.5–0.618 zone coinciding with the 50-EMA is a high-quality pullback area.
- **Fib + volume profile**: a retracement into a high-volume node is more likely to be absorbed.
- **Fib + ATR**: if the whole swing is less than 1 ATR, the retracement levels are inside the noise band and
  mean nothing.

## 6. Reading from a screenshot

Extractable: if retracement lines are drawn, their labels and where price sits among them; the swing anchors
if the drawing tool shows them.

Not extractable: the exact price of each level unless labelled. Do not compute Fib levels from pixel heights;
use the axis and mark them approximate.

## 7. Worked example

```
Swing low 1_140 → swing high 1_300 (range 160), retracement levels:
 0.236 → 1_300 − 37.8  = 1_262.2
 0.382 → 1_300 − 61.1  = 1_238.9
 0.5   → 1_300 − 80.0  = 1_220.0
 0.618 → 1_300 − 98.9  = 1_201.1
 0.786 → 1_300 − 125.8 = 1_174.2
Extensions above 1_300: 1.272 → 1_343.5 ; 1.618 → 1_398.9
If a prior support sits at 1_198–1_204, the 0.618 zone (1_201) is a high-quality confluence area.
If nothing else sits near it, it is just a line on a chart.
See tests/indicators/test_fibonacci.py.
```

## 8. Beginner summary (Hinglish)

**Fibonacci retracement kya hai?** Ek swing (low se high) ke baad price kitna wapas aata hai — usko 0.382,
0.5, 0.618 jaisi ratios mein naapna.

**Matlab:** 0.618 par aksar log kharidte hain, isliye woh level "kaam" karta hai — par yeh koi law nahi hai.

**Sabse zaroori:** level ke saath **doosri cheez** honi chahiye — support, EMA, round number. Akela Fib level
bekaar hai.

**Badi galti:** apni marzi se swing chunna taaki level apni trade se match kare. Yeh confirmation bias hai.

## 9. Exercise

Take one swing and compute the levels. Then draw the same swing using two different (but both defensible)
anchors. Compare how far apart the 0.618 levels are. If they differ by more than 0.5 ATR, write down why that
makes precise Fib trading unreliable on that timeframe.

---
*See also: [`pivot-points.md`](pivot-points.md) · [`volume-profile.md`](volume-profile.md) ·
[`../knowledge/price-action/`](../price-action/)*
