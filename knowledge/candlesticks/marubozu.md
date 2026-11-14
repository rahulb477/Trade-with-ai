# Marubozu

**Group:** Strength / continuation · **Candles:** 1 · **Reliability band:** Contextual
**Detector:** `patterns.detect_marubozu`

## 1. What it is
A candle with **no wicks** (or negligible ones) — the body spans the entire range. The interval opened
at one extreme and closed at the other, with no rejection in either direction.

- **Bullish marubozu:** open = low, close = high.
- **Bearish marubozu:** open = high, close = low.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | `body / range ≥ 0.95` | Nearly no wicks |
| 2 | `body ≥ 1.2 × average_body(20)` | Meaningfully large |
| 3 | Closed candle | Else `DEVELOPING` |
| 4 | Not the first bar of a session gap in an illiquid stock | Sanity check |

The strict "zero-wick" version barely exists in real data. Common practice uses "shaven head and
shaven bottom" — `upper_wick ≤ 0.05 × range` and `lower_wick ≤ 0.05 × range`.

## 3. Anatomy
```
Bullish              Bearish
 ┌─────┐             
 │     │             ┌─────┐
 │     │             │     │
 │     │             │     │
 └─────┘             └─────┘
 open=low,           open=high,
 close=high          close=low
```

## 4. Where it means something
- Opening drive of a new trend (first strong bar out of a base)
- Resolution of a compression (inside bars, triangles, rectangles)
- Breakout bar through a level
- Continuation bar in the middle of an established trend
- **At the end of an extended trend: a warning of climax** — position, again, decides the meaning

## 5. Interpretation
A marubozu says one side controlled the entire interval and the close was at the extreme. That is the
strongest single-candle statement of intent. Two readings, depending on location:

| Location | Reading |
|----------|---------|
| Out of a base / through a level | Initiation of a move — follow-through is common |
| Mid-trend | Continuation confirmation |
| After 6–10 consecutive up candles, far above the 20-EMA | Possible buying climax — the *last* buyers arrived |

## 6. Confirmation requirements
- For an initiation reading: the next candle holds above the marubozu's midpoint (bullish) and volume
  stays elevated. A retest that holds is the strongest confirmation.
- For a climax reading: the next candle closes below the marubozu's midpoint, or produces a long upper
  wick (supply appeared).

## 7. Volume
High volume is expected for a genuine marubozu. **Extremely** high volume with a marubozu at the end
of a long move is the classic exhaustion signature. Low volume with a marubozu in an illiquid stock is
usually a data artefact, not a signal.

## 8. Paper-trade entry conditions (illustrative)
```
Initiation case:
  trigger    : retest of the marubozu's midpoint holding, or a shallow pullback that holds its low
  entry zone : retest level ± 0.1 × ATR
  invalidation: below the marubozu's low (bullish) − 0.25 × ATR
  targets    : T1 measured move = marubozu body projected from the close
               T2 next major resistance/swing
  never      : buy the close of a marubozu that has already run 3+ ATR from its base
Climax case:
  action     : no new entry in the direction of the marubozu; manage existing positions with a trail
```

## 9. Invalidation
Close below the marubozu's low (bullish case); a long upper-wick candle immediately after (supply
absorbed the move); failure to make progress in the following 2–3 candles.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Chasing an extended marubozu | Measure distance from the base/EMA |
| Illiquid stock with a one-print body | Check volume and spread |
| Gap open creating a fake body | Check the session gap |
| Marubozu into immediate resistance | Room check |
| Treating a large body as a pattern by itself | Enforce `body/range ≥ 0.95` |

## 11. Historical evidence — honest position
The marubozu is descriptive rather than predictive: it states that one side dominated one interval.
Whether that implies continuation depends almost entirely on location and the prior base. No
performance figure is asserted. The "climax vs initiation" distinction is a documented qualitative
observation, not a measured edge.

## 12. Worked example (illustrative, fictional)
```
Instrument: RST · 1D · 5-week base 300–315; breakout day
Candle: o314.5 h330.0 l314.0 c329.6 · body 15.1 · range 16.0 → body/range 94.4%
        upper_wick 0.4 (2.5%), lower_wick 0.5 (3.1%) → shaven top and bottom ✔
Volume: 2.6× average ✔
Status: CONFIRMED (initiation reading — first bar out of the base)
Setup : enter on the retest of 315–318 holding; entry 317.0
        invalidation 312.4 (below base top / inside the base) · risk 4.6
        T1 measured: 315 + 15 = 330 (already at the close) → use the next measured move:
                    330 + 15 = 345 → 6.1R
        T2 352 (prior swing high) → 7.6R
Verdict: BULLISH SCENARIO on the retest trigger only. Buying the close at 329.6 with the same
        invalidation would give risk 17.2 and T1 0.9R — the retest is the whole trade.
```

## 13. Beginner summary (Hinglish)
**Marubozu:** aisi candle jisme wicks na ke barabar ho — body poore range ko cover kare.

**Matlab:** poore session mein ek hi side ka control raha, aur close extreme par hua. Yeh single candle
ka sabse strong intent signal hai.

**Do matlab ho sakte hain:**
- Base/level se nikalte waqt → **shuruaat** ka signal (achha).
- Bahut lambi tezi ke baad, 20-EMA se bahut door → **climax** ka warning (khatarnaak).

**Entry:** breakout candle ko close par chase mat karo. Retest ka wait karo jo hold kare.

**Stop:** marubozu ki low ke neeche.

## 14. Exercise
Find two marubozus: one breaking out of a base, one at the end of a 10-day rally. For each, measure the
distance from the 20-EMA in ATR units and the volume multiple. Then write the two-part rule you would
use to classify a marubozu in real time.

---
*See also: [`three-white-soldiers.md`](three-white-soldiers.md) · [`README.md`](README.md) §2 ·
[`../indicators/ema.md`](../indicators/ema.md)*
