# Dark Cloud Cover

**Group:** Bearish reversal · **Candles:** 2 · **Reliability band:** Moderate
**Detector:** `patterns.detect_dark_cloud_cover`

## 1. What it is
After an advance: a **bullish** candle, then a **bearish** candle that **opens above the first
candle's high** and **closes below the midpoint of the first candle's body**, without fully
engulfing it. The bearish counterpart of the piercing pattern.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 bullish with a real body (`body₁ ≥ 0.6 × avg_range`) |
| 2 | Candle 2 bearish |
| 3 | `open₂ > high₁` (gap up above the prior high; in 24h markets accept `open₂ > close₁` and say so) |
| 4 | `close₂ < (open₁ + close₁)/2` — closes below the midpoint |
| 5 | `close₂ > open₁` — otherwise it is a bearish engulfing |
| 6 | Prior trend upward |
| 7 | Both closed |

## 3. Anatomy
```
                 ┌──────┐   <- candle 2 opens above candle 1's high, then sells off
                 │      │
 ┌─────┐         │      │
 │     │         └──────┘
 │     │  midpoint ─────────  candle 2 closes below here
 └─────┘
```

## 4. Where it means something
At resistance; at the upper boundary of a rising channel; at a gap-up open into supply; at a Fib
extension.

## 5. Interpretation
The market opened enthusiastically above the prior high and then closed below the halfway point of
the prior body. That is a failed auction: the high price did not attract enough demand to hold.
It is meaningful but incomplete — hence lower weight than a bearish engulfing.

## 6. Confirmation requirements
- Minimum: candle 3 closes below candle 2's low.
- Good: a lower high is established and the prior swing low breaks.
- Strong: the gap-up zone is retested from below and fails.
- Invalidated: close above candle 2's high (or above candle 1's high on a closing basis).

## 7. Volume
High volume on candle 2 strengthens the read substantially: the gap-up was sold into. Low volume
suggests a thin opening rather than genuine supply. Note that gap opens are often low-liquidity, so
volume comparison should include the *following* bar.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : close below candle 2's low
Entry zone     : candle 2 low ± 0.1 × ATR
Invalidation   : above candle 2's high + 0.25 × ATR
Targets        : T1 candle 1's open · T2 prior swing low · T3 measured: advance height × 0.5
```

## 9. Invalidation
Close above candle 2's high; a re-attack that takes out candle 1's high; the "gap up" being a
corporate-action artefact (verify adjustments).

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| No real gap in a 24-hour market | State the relaxation explicitly or drop to `POSSIBLE` |
| Candle 2 closes only just below the midpoint | Require a clear penetration |
| Gap from a split/bonus | Check adjustments |
| Appears in a range | Location filter |
| Confused with bearish engulfing | Rule 5 |

## 11. Historical evidence — honest position
Generally regarded as slightly weaker than the bearish engulfing because the reversal is partial.
No specific success rate is claimed. Measure locally.

## 12. Worked example (illustrative, fictional)
```
Instrument: KLM · 1D · advance 150 → 172
C1 o165.0 h171.0 l164.4 c170.2 (body 5.2) · midpoint 167.6
C2 o172.4 (> high1 171 ✔) h173.0 l166.8 c167.1 (< 167.6 ✔, > open1 165 ✔)
Volume: 1.7× ✔ · Status: CONFIRMED
Entry 166.6 · stop 173.3 (risk 6.7) · T1 165.0 (0.24R FAIL) · T2 158 (1.28R FAIL) · T3 149 (2.6R ✔)
Verdict: WAIT — the nearest two targets fail the gate. Only defensible with a tighter invalidation
         (e.g. the retest of 171 failing) giving risk 4.0 → T3 4.5R.
```

## 13. Beginner summary (Hinglish)
**Dark cloud cover:** pehli green candle, phir red candle jo **pehli ki high ke upar open** hoke
**pehli ke aadhe body se neeche** close kare.

**Matlab:** market ne upar gap kiya, log khushi se kharida, par phir sab bik gaya — "failed auction".

**Entry:** doosri candle ki low tootne par.

**Stop:** doosri candle ki high ke thoda upar.

**Yaad rakho:** yeh engulfing se kamzor hai kyunki poori body cover nahi hoti.

## 14. Exercise
Find a dark cloud cover and a nearby bearish engulfing. Compare: which had a higher volume on candle
2, which gave the better R:R to the nearest support, and which "looked" more convincing. Write down
whether appearance and arithmetic agreed.

---
*See also: [`piercing-pattern.md`](piercing-pattern.md) · [`bearish-engulfing.md`](bearish-engulfing.md)*
