# Three White Soldiers

**Group:** Bullish reversal / continuation · **Candles:** 3 · **Reliability band:** Higher
**Detector:** `patterns.detect_three_white_soldiers`

## 1. What it is
Three consecutive **bullish** candles, each closing **higher** than the previous, each opening
**within** the previous candle's body, and each closing **near its own high** with a solid body.
It depicts sustained, orderly accumulation across three intervals — buyers in control repeatedly,
without a single dominant gap.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | Three consecutive bullish candles | Required |
| 2 | Each close > previous close | Monotonic advance |
| 3 | Each open within (or near) the previous body | No wild gaps |
| 4 | Each close near its high | `close_pos ≥ 0.7` for each |
| 5 | Each body substantial | `body ≥ 0.6 × range` |
| 6 | Upper wicks short | `upper_wick ≤ 0.3 × range` |
| 7 | The sequence follows a decline or a consolidation breakout | Context |
| 8 | All three closed | Otherwise `DEVELOPING` |

## 3. Anatomy
```
  ┌──┐
  │  │ ┌──┐
  │  │ │  │ ┌──┐
  └──┘ │  │ │  │
       └──┘ └──┘
 each open inside prior body; each close near its high
```

## 4. Where it means something
- Emerging from a base or a long consolidation (strongest)
- Reversing a downtrend from a tested support
- Resuming after a healthy pullback in an established uptrend
Weak when it appears after an already-extended rally — then it is often the *climax*, not the start.

## 5. Interpretation
Three intervals of consistent buying. The pattern's value is **consistency**, not size. If the third
candle is much larger than the first two, the sequence may be a blow-off rather than accumulation.
Documented treatments caution specifically about "three soldiers at the top of a move" — the same
shape that starts a trend can end one. Position within the larger structure decides which.

## 6. Confirmation requirements
- Minimum: the third candle closes as specified (the pattern is then complete).
- Good: a fourth candle holds above the third's midpoint, or a shallow pullback holds the third
  candle's low.
- Strong: consolidation above the sequence, then continuation; volume stays elevated.
- Invalidated: price returns below the first candle's open (all three intervals' gains surrendered).

## 7. Volume
Ideal: rising volume across the three candles, or at least above average on candles 2 and 3.
Falling volume across the sequence is a warning — the advance is losing participation.
A volume climax on candle 3 with an unusually long body suggests exhaustion; wait for a pullback.

## 8. Paper-trade entry conditions (illustrative)
```
Preferred     : wait for a shallow pullback (1–3 candles) that holds above candle 3's midpoint,
                then enter on the resumption close
Aggressive    : enter on candle 3's close (chasing risk; worse R:R)
Entry zone    : pullback low + 0.1 × ATR, or breakout above candle 3's high
Invalidation  : below candle 2's low (tighter) or candle 1's open (structural)
Targets       : T1 = measured move = height of the sequence projected up
                T2 = prior swing high above
                T3 = next major resistance / Fib extension
Never         : enter after a gap-up open beyond candle 3's high — that is chasing.
```

## 9. Invalidation
Close below candle 1's open; a long upper-wick candle immediately after the sequence (supply
appeared); volume collapsing on the pullback below average while price bleeds; higher-timeframe
trend pointed down with the sequence hitting a resistance.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Three soldiers into major resistance | Check overhead room first |
| Climax at the end of a parabolic move | Look at prior extension (e.g. >3 ATR above the 20-EMA) |
| Small bodies counted as soldiers | Enforce rules 4–5 |
| Sequence with big upper wicks | Rule 6 fails → `POSSIBLE`, not confirmed |
| Low-volume drift upward | Volume check |
| Gap-opened candles (not "within previous body") | Rule 3 |

## 11. Historical evidence — honest position
Three-candle continuation patterns are structurally informative, and the literature treats this one
as a genuine strength signal *within a base*. At trend extremes it is often cited as a warning.
Both observations are qualitative. No success rate is asserted. Test locally.

## 12. Worked example (illustrative, fictional)
```
Instrument: MNO · 1D · base 120–128 for 3 weeks; sequence:
 C1 o121.0 c124.2 (close_pos 0.88, body 3.2)
 C2 o123.8 c127.6 ✔ open inside C1 body
 C3 o127.2 c130.4 ✔ open inside C2 body, close near high
Volume: 1.3×, 1.6×, 1.9× ✔
Status: CONFIRMED
Plan  : wait for pullback to 128–129 holding above C3 midpoint 128.8; entry 129.0
        invalidation 126.9 (below C2 low) · risk 2.1
        T1 132.4 (measured: 9.4 sequence height from 121.0) -> 1.62R ✔
        T2 136.0 -> 3.3R · T3 141.0 -> 5.7R
Verdict: BULLISH SCENARIO on the pullback trigger only, not at the current price.
```

## 13. Beginner summary (Hinglish)
**Three white soldiers:** teen lagatar green candles, har ek pichhli se upar close, har ek apni high
ke paas band, aur wicks chhoti.

**Matlab:** teen sessions tak buyers lagatar control mein rahe — yeh strength ka signal hai.

**Sabse important:** yeh pattern base/consolidation se nikalte waqt best hota hai. Agar stock pehle
se bahut upar chala gaya hai, to yahi pattern **exhaustion** bhi ho sakta hai.

**Entry:** teen candles ke baad thoda pullback aaye aur third candle ke midpoint ke upar hold kare —
tab enter karo. Seedha chase mat karo.

**Stop:** doosri candle ki low ke neeche.

## 14. Exercise
Find one three-white-soldiers at the *start* of a move and one at the *end*. Compare: distance from
the 20-period EMA, volume trend across the three candles, and what happened in the next 10 candles.
Write two sentences on how you would tell them apart **before** the outcome was known.

---
*See also: [`three-black-crows.md`](three-black-crows.md) · [`marubozu.md`](marubozu.md)*
