# High Wave

**Group:** Neutral / indecision · **Candles:** 1 · **Reliability band:** Lower
**Detector:** `patterns.detect_high_wave`

## 1. What it is
A candle with **very long wicks on both sides** and a **small body** — the range is much larger than
normal, yet the close lands near the open. It records an interval of exceptional two-way volatility
that resolved nowhere.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | `range ≥ 1.8 × average_range(20)` (or ≥ 2×) | Abnormally large range |
| 2 | `body / range ≤ 0.25` | Small body |
| 3 | `upper_wick ≥ 0.3 × range` and `lower_wick ≥ 0.3 × range` | Long both sides |
| 4 | Closed candle | Else `DEVELOPING` |

The 1.8× multiplier is a convention used by this repository's detector for reproducibility; other
sources use 2× or express it in ATR units (`range ≥ 2 × ATR`). State which you used.

## 3. Anatomy
```
     │
     │
   ┌─┴─┐
   └─┬─┘
     │
     │
```

## 4. Where it means something
- After a strong trend, as a possible climax (both sides exhausted themselves)
- At a major level, indicating violent rejection in both directions
- Around news events or expiry, where the volatility is event-driven rather than structural

## 5. Interpretation
A high wave says: **volatility expanded and nothing was decided.** In the literature it is often read
as "confusion at a potential turning point" — which is close to saying it is not a directional signal.
Its practical value is as a **volatility and risk marker**: stops placed inside a high-wave range are
likely to be swept.

## 6. Confirmation requirements
None possible from the candle. The *following* candle's behaviour decides:
- Close above the high → resolution upward.
- Close below the low → resolution downward.
- Another high wave → the market is unstable; stand aside.

## 7. Volume
Very high volume on a high wave = a violent battle (often news). Expect follow-through volatility in
whichever direction resolves. Low volume on a high wave is unusual and often indicates a data/spike
artefact — verify before interpreting.

## 8. Paper-trade entry conditions (illustrative)
```
Approach 1 (breakout)  : enter on a close beyond the high wave's high/low, with volume
Approach 2 (avoidance) : treat as a no-trade zone; the risk of stop-sweep is elevated
Preferred             : approach 2 unless a clean structural level sits just outside the range
Sizing note           : if you do trade, the invalidation must sit beyond the wave's extreme,
                        which is wide — size down accordingly
```

## 9. Invalidation
A close back inside the range after a breakout attempt; a subsequent high wave in the opposite
direction (whipsaw regime).

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Reading it as a reversal | It is neutral |
| Trading inside the range | Wait for resolution |
| Ignoring the stop-sweep risk | Widen buffer or skip |
| Chasing the breakout candle on weak volume | Volume check |
| Misreading a data spike | Cross-check neighbouring bars |

## 11. Historical evidence — honest position
Treated in the literature as an indecision/extreme-volatility candle. No directional edge is
documented reliably. Its more defensible use is as a **volatility warning**, which is how this
repository uses it.

## 12. Worked example (illustrative, fictional)
```
Instrument: CDE · 1D · uptrend, then a results-day candle
Candle: o505 h537 l481 c508 · range 56 vs 20-day avg range 18 → 3.1× ✔ body 3 → body/range 5% ✔
Volume: 4.2× average
Reading: results-day battle. Nothing decided. Stops inside 481–537 will very likely be swept.
Plan   : no position. If price later closes above 537 with volume, a breakout plan becomes valid
         with invalidation below the wave's low (wide stop ⇒ small size).
```

## 13. Beginner summary (Hinglish)
**High wave:** bahut lambi wicks dono taraf, chhoti body, aur range normal se kaafi badi.

**Matlab:** bahut hulchul hui par kuch decide nahi hua. Aksar news ya result ke din aata hai.

**Trade?** Nahi — iske andar trade karne ka matlab hai stop sweep hone ka risk lena.

**Agar trade karna hi ho:** sirf iski high/low ke bahar close hone par, aur stop iske extreme ke bahar
— jo bada hoga, isliye size chhota.

## 14. Exercise
Find a high-wave candle on a results day. Note the subsequent 5 candles. How far did price travel from
the wave's midpoint in each direction? Then answer: would a stop placed 1 ATR inside the range have
survived?

---
*See also: [`doji.md`](doji.md) · [`spinning-top.md`](spinning-top.md) · [`../indicators/atr.md`](../indicators/atr.md)*
