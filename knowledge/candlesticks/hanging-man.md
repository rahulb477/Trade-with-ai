# Hanging Man

**Group:** Bearish reversal · **Candles:** 1 · **Reliability band:** Moderate (needs strong confirmation)
**Detector:** `patterns.detect_hanging_man`

## 1. What it is
A small body near the **top** of the range with a **long lower wick**, appearing **after an advance**.
Same geometry as the hammer; the context inverts the meaning. After a rally, a long lower wick means
price had to drop sharply intra-interval before recovering — a warning that supply appeared below.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | Prior trend **upward** | Measurable advance |
| 2 | `lower_wick ≥ 2 × body` | Defining feature |
| 3 | `upper_wick ≤ 0.5 × body` | Body near the top |
| 4 | `body / range ≤ 0.35` | Small body |
| 5 | Candle opens near/above the prior close (ideally gaps up) | Confirms "hanging" position |
| 6 | Closed candle | Else `DEVELOPING` |

## 3. Anatomy
```
   ┌───┐   <- small body near the top (often a gap up from the prior close)
   └─┬─┘
     │
     │     <- long lower wick: sharp intra-interval drop, then recovery
     ▼
```

## 4. Where it means something
At resistance after an extended advance; at the top of a channel; after a gap-up open that gets sold.
Meaningless mid-range in a drifting market.

## 5. Interpretation
This is the **weakest-conviction** of the classic bearish candles, and the literature is consistently
cautious: the close is near the high, which is bullish on its face. What makes it bearish is *what
had to happen* to produce the wick — a sharp sell-off was absorbed but the fact that it occurred at
all signals that sellers are testing.

Treat it as a *warning about participation*, not as a reversal.

## 6. Confirmation requirements
Stricter than for a hammer, because the pattern is inherently ambiguous:

| Level | Confirmation |
|-------|--------------|
| Minimum | Next candle closes **below the hanging man's body** |
| Good | Next candle closes **below the hanging man's low** (fully negates the recovery) |
| Strong | A lower high forms and the prior swing low breaks |
| Invalidated | Close above the hanging man's high; or a new higher high on strong volume |

## 7. Volume
High volume on the hanging man suggests genuine distribution with absorption. Volume is more
important here than for most single-candle patterns because the shape alone is ambiguous.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : close below the hanging man's low (do not short the pattern itself)
Entry zone     : trigger ± 0.1 × ATR
Invalidation   : above the hanging man's high + 0.25 × ATR
Targets        : T1 prior swing low · T2 measured: advance height × 0.5 · T3 major support
Alternative    : do nothing until a lower high + structure break confirms a trend change
```

## 9. Invalidation
New high above the candle's high; continuation of the uptrend with higher highs; the long wick
explained by an intraday news spike that fully reversed and stayed reversed (nothing changed).

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Called a hammer in the wrong context | Trend check first, always |
| Shorting immediately on the pattern | Require a close below the low |
| Long-wick artefacts (bad tick, illiquid market) | Verify the low against neighbours |
| Repeated hanging men in a strong trend | Trends absorb warnings; require structure break |
| Confusion with a spinning top | Body/range thresholds |

## 11. Historical evidence — honest position
Consistently described in the literature as requiring confirmation and as one of the less reliable
single-candle bearish patterns, mainly because the close position is bullish. No statistic is
claimed. Measure before relying on it.

## 12. Worked example (illustrative, fictional)
```
Instrument: BCD · 1D · advance 1_050 → 1_180; resistance 1_175–1_185
Candle: o1_176 h1_178 l1_158 c1_174 · body 2 · range 20 · lower_wick 16 → lower/body = 8 ✔
        gap up open above prior close ✔
Volume: 1.7× average ✔
Status: CONFIRMED
Setup : short trigger close < 1_158 → entry 1_157.5 · invalidation 1_178.5 · risk 21
        T1 1_140 (prior swing low) → 0.83R FAIL
Verdict: WAIT — no acceptable R:R to the first structural target. A failed-retest short at 1_176
        with invalidation at 1_186 (risk 10) to T1 1_140 would be 3.6R — that is the tradeable version.
```

## 13. Beginner summary (Hinglish)
**Hanging man:** uptrend ke baad ek candle jisme neeche ki lambi wick ho aur body upar ho — shape
hammer jaisi, par jagah ulti.

**Matlab:** us din price tezi se neeche gira, phir wapas upar aa gaya. Close strong hai, isliye yeh
kamzor signal hai — bas warning hai ki sellers test kar rahe hain.

**Kab short karein?** Jab agli candle is candle ki **low** ke neeche close kare. Pattern dekh kar
turant short mat karo.

**Stop:** is candle ki high ke thoda upar.

## 14. Exercise
Find three hanging men. Record whether the next candle closed below the body, below the low, or
higher. Then compute: if you had shorted on the pattern alone (without confirmation), how many of the
three would have stopped out? This exercise is designed to make the confirmation rule feel expensive
— and necessary.

---
*See also: [`hammer.md`](hammer.md) · [`shooting-star.md`](shooting-star.md)*
