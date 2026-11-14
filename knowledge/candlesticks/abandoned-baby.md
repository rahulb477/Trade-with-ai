# Abandoned Baby (Bullish and Bearish)

**Group:** Reversal (both directions) · **Candles:** 3 · **Reliability band:** Higher, but rare
**Detector:** `patterns.detect_abandoned_baby`

## 1. What it is
A three-candle reversal in which the middle candle is **isolated by gaps on both sides**. The star's
entire range sits away from both neighbours — a literal "abandoned" price interval that nobody else
traded.

- **Bullish:** after a decline — bearish candle, doji (or tiny body) gapping **below**, then a
  bullish candle gapping **above** the star.
- **Bearish:** after an advance — bullish candle, doji gapping **above**, then a bearish candle
  gapping **below** the star.

## 2. Formation rules (bullish)
| # | Rule |
|---|------|
| 1 | Prior trend downward |
| 2 | Candle 1 bearish with a real body |
| 3 | Candle 2 is a doji or very small body, with `high₂ < low₁` (full gap down) |
| 4 | Candle 3 bullish with `low₃ > high₂` (full gap up) |
| 5 | Candle 3 closes well into candle 1's body (≥50%) |
| 6 | All three closed |

Bearish is the mirror: `low₂ > high₁`, `high₃ < low₂`, candle 3 closes well into candle 1's body
from above.

**Gap requirement is the hard part.** True gaps require a session break — so this pattern is
essentially unavailable on 24-hour instruments and rare on intraday charts where the "gap" is just a
thin period. If you relax the gap to "body separation", it is a morning/evening doji star, **not** an
abandoned baby. Label it accordingly.

## 3. Anatomy (bullish)
```
 1 (bear)
 ┌────┐
 │    │
 └────┘
              ┌┐   <- doji, fully below candle 1 (gap)
              └┘
                    ┌──────┐
                    │      │   <- gaps above the star
                    └──────┘
```

## 4. Where it means something
At major support/resistance after an extended move; after a capitulation or blow-off; on daily/weekly
charts around exhaustion gaps. On a 1-minute chart, treat any apparent instance as a
morning/evening star at best.

## 5. Interpretation
The isolated candle represents a moment where price traded in a vacuum — no overlap with either
neighbour. Interpretation: the prior move overshot so far that participants refused to transact at
the extreme. It is a strong statement of exhaustion, which is why the literature ranks it highly and
also why it barely ever occurs.

## 6. Confirmation requirements
Candle 3's close completes the pattern. Additional confirmation: a fourth candle holding above
(bullish) the star's high, volume expansion on candle 3, and a subsequent break of the prior swing.

## 7. Volume
Ideal: high on candle 1 (climax), very low on the star (no participation at the extreme), high on
candle 3 (reclaim). Any other profile weakens the case; a star on *high* volume with a doji body is
usually a battle, not a vacuum.

## 8. Paper-trade entry conditions (illustrative)
```
Long trigger  : candle 3 close, or break of candle 3's high
Entry zone    : candle 3 high ± 0.15 × ATR
Invalidation  : below the star's low (bullish) minus 0.25 × ATR
Targets       : T1 candle 1's open · T2 prior swing high · T3 measured move of the decline × 0.618
Note          : stops are typically wide because of the gap structure; recompute R:R carefully
```

## 9. Invalidation
Any close back through the star's gap in the opposite direction; candle 3 giving back its body;
the "gap" turning out to be a data artefact or a corporate action.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| No genuine gap (24h markets) | Refuse the label; use morning/evening doji star |
| Gap caused by a split/bonus/dividend | Check corporate actions before interpreting |
| Gap caused by a data feed error | Cross-check against a second source |
| Candle 3 with a tiny body | Rule 5 |
| Illiquid stock with one printed trade at an odd price | Verify against average volume |

## 11. Historical evidence — honest position
Widely described as one of the strongest reversal formations *because of its strictness*, and equally
widely noted as too rare to build a strategy on. Frequency matters: a pattern that appears three
times a year on a daily chart cannot generate a usable sample from one instrument. Do not quote
performance without a large multi-instrument sample.

## 12. Worked example (illustrative, fictional)
```
Instrument: VWX · 1D · decline from 900 to 780
C1 o812 c786 (bear) · C2 o778 h780 l774 c777 (doji-ish, high 780 < low1 783 ✔ full gap down)
C3 o783 h800 l782 c798 (low 782 > high2 780 ✔ gap up; closes above 50% of C1 body = 799… just below)
Status: POSSIBLE — candle 3 closes marginally below the 50% level (799); label accordingly.
Plan  : if a fourth candle closes above 799, treat as effectively confirmed.
```

## 13. Beginner summary (Hinglish)
**Abandoned baby:** teen candles, beech wali candle **dono taraf se gap** chhodti hai — jaise akela
chhod diya gaya ho.

**Bullish:** pehle red, phir neeche gap ke saath chhoti doji, phir upar gap ke saath green.

**Matlab:** price itna extreme chala gaya ki log wahan trade hi nahi karna chahte the — exhaustion.

**Dhyan:** asli gap chahiye. Crypto/forex jaise 24 ghante wale markets mein yeh nahi milta; wahan
isay morning/evening star hi kahenge.

**Entry:** teesri candle ke close par. **Stop:** beech wali candle ki low ke neeche.

## 14. Exercise
Scan 50 daily charts and count abandoned babies (with the full-gap rule). Compare that count with the
number of morning stars. Explain in two lines why a very strict pattern is both *more informative*
and *less practical* — and what that trade-off means for how you should treat a single occurrence.

---
*See also: [`morning-star.md`](morning-star.md) · [`evening-star.md`](evening-star.md) · [`doji.md`](doji.md)*
