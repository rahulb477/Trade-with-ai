# Piercing Pattern (Piercing Line)

**Group:** Bullish reversal · **Candles:** 2 · **Reliability band:** Moderate
**Detector:** `patterns.detect_piercing`

## 1. What it is
After a decline: a bearish candle, then a bullish candle that **opens below the first candle's low**
(or at least below its close) and **closes above the midpoint of the first candle's body** but
**below its open**. It is the bullish counterpart of the dark cloud cover, and a partial version of
the bullish engulfing — the second body pierces into the first but does not cover it.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 bearish, with a real body (`body₁ ≥ 0.6 × average_range`) |
| 2 | Candle 2 bullish |
| 3 | `open₂ < close₁` (ideally below `low₁`) |
| 4 | `close₂ > midpoint of body₁`: `close₂ > (open₁ + close₁)/2` |
| 5 | `close₂ < open₁` — if it closes above, it is a bullish engulfing instead |
| 6 | Prior trend downward |
| 7 | Both candles closed |

## 3. Anatomy
```
 candle 1 (bear)      candle 2 (bull)
 ┌─────┐
 │     │
 │     │  ← midpoint  ─────  candle 2 closes above here
 └─────┘              ┌──────┐
      └──────────────►│      │  opens below candle 1 close/low
                      └──────┘
```

## 4. Where it means something
At support, at a channel bottom, at a Fib retracement cluster, or after an exhaustion gap down.
Mid-range, it is noise. Under heavy overhead resistance, it has no room.

## 5. Interpretation
Buyers opened the second interval at a disadvantage (below the prior close) and still closed more
than halfway up the prior body. That is a real shift in the intraday auction. Because it is *less*
complete than an engulfing, it is treated as weaker evidence.

## 6. Confirmation requirements
- Minimum: candle 3 closes above candle 2's high.
- Good: close above candle 1's open (converting the pattern into an effective engulfing).
- Strong: break of the recent swing high with volume; retest holds.
- Invalidated: close below candle 2's low.

## 7. Volume
Above average on candle 2 strengthens materially. If candle 2's volume is below average, the
"pierce" often reflects a thin session or short covering rather than demand. If volume is not
visible, cap the pattern at `POSSIBLE` evidence strength and require full price confirmation.

## 8. Paper-trade entry conditions (illustrative)
```
Long trigger  : close above candle 2's high
Entry zone    : candle 2 high ± 0.1 × ATR
Invalidation  : below candle 2's low − 0.25 × ATR
Targets       : T1 candle 1's open · T2 prior swing high · T3 measured decline × 0.5
Preference    : retest entry near candle 2's midpoint to improve R:R
```

## 9. Invalidation
Close below candle 2's low; failure to exceed candle 2's high within ~3 candles; higher-timeframe
support break; the "gap down" in candle 2 turns out to be a corporate-action artefact.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Candle 2 closes only just above the midpoint | Require a clear pierce (>0.1 × body₁ beyond midpoint) |
| Appears in a range | Location filter |
| Candle 1 body tiny | Require `body₁ ≥ 0.6 × avg_range` |
| Confused with engulfing | Apply rule 5 numerically |
| Colour convention misread | Verify against price direction |

## 11. Historical evidence — honest position
Generally described as less informative than bullish engulfing because the reversal is incomplete.
No numeric success rate is claimed. Measure locally via [`README.md`](README.md) §5.

## 12. Worked example (illustrative, fictional)
```
Instrument: JKL · 1D · decline 76 → 68. C1 open 69.4 close 68.1 (body 1.3).
C2 open 67.8 close 68.9 → midpoint of C1 = 68.75, close 68.9 > 68.75 ✔, close < open1 69.4 ✔
Volume: 1.4× average ✔ · Status: CONFIRMED
Entry 69.2 / stop 67.4 (risk 1.8) / T1 69.4 (0.11R FAIL) / T2 72.0 (1.56R)
Verdict: WAIT — T1 unusable; only T2 clears the gate. Needs a retest entry near 68.6 (risk 1.2 → T2 2.83R).
```

## 13. Beginner summary (Hinglish)
**Piercing:** pehli red candle, phir green candle jo neeche open hoke pehli candle ke **aadhe se
zyada** upar close karti hai — par pehli candle ke open tak nahi pahunchti.

**Matlab:** buyers ne kamzor opening ke baad wapsi ki. Engulfing se kamzor, kyunki poora control
wapas nahi aaya.

**Entry:** agli candle is candle ki high ke upar close kare to. **Stop:** is candle ki low ke neeche.

## 14. Exercise
Find a piercing pattern and a bullish engulfing within the same week. Compute the R:R to the nearest
prior swing high for both. Which had the better *tradeable* geometry, and why might the weaker
pattern have given the better trade? (Hint: entry location and stop distance.)

---
*See also: [`dark-cloud-cover.md`](dark-cloud-cover.md) · [`bullish-engulfing.md`](bullish-engulfing.md)*
