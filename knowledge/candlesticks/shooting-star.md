# Shooting Star

**Group:** Bearish reversal · **Candles:** 1 · **Reliability band:** Moderate
**Detector:** `patterns.detect_shooting_star`

## 1. What it is
A small-bodied candle with a **long upper wick**, appearing **after an advance**. Buyers pushed price
up during the interval and sellers rejected the high, closing price back near the open/low.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | Prior trend **upward** | Measurable advance, or 3+ higher closes |
| 2 | `upper_wick ≥ 2 × body` | Defining feature |
| 3 | `lower_wick ≤ 0.5 × body` | Body near the low |
| 4 | `body / range ≤ 0.35` | Small body |
| 5 | `range ≥ 0.5 × average_range(20)` | Avoid illiquid noise |
| 6 | Closed candle | Else `DEVELOPING` |
| 7 | Ideally the high exceeds a recent swing high and then fails | Adds meaning |

Same geometry as the inverted hammer — **context decides the name**. After an advance = shooting
star. After a decline = inverted hammer.

## 3. Anatomy
```
   ▲
   │      <- long upper wick: the high was rejected
   │
 ┌─┴─┐
 └───┘     <- small body near the low of the range
```

## 4. Where it means something
At horizontal resistance that already held; at the top of a rising channel or a wedge; at a Fib
extension/cluster; at a round number; after a gap-up open that fails.

## 5. Interpretation
The candle reports that the *high* was refused. In an uptrend, that is the first crack — buyers
over-extended and were met with supply. It is a **warning**, not a sell signal, until price
confirms by breaking structure.

Commonly strongest when it occurs at the top of a **parabolic** move or after several consecutive
up candles, where the failed push represents exhausted momentum.

## 6. Confirmation requirements
| Level | Confirmation |
|-------|--------------|
| Minimum | Next candle closes **below the shooting star's body** (below its open for a bullish prior candle) |
| Good | Next candle closes below the shooting star's low |
| Strong | Price breaks the last swing low, or a short-term uptrend line, on rising volume |
| Invalidated | Close above the shooting star's high |

## 7. Volume
High volume on the shooting star with a long upper wick = distribution into strength (the classic
reading). Low volume = a thin-market spike that may mean nothing.
Rising volume on the following bearish candle is the decisive confirmation.

## 8. Paper-trade entry conditions (illustrative)
```
Short trigger  : close below the shooting star's low (conservative) or body low (aggressive)
Entry zone     : trigger level ± 0.1 × ATR
Invalidation   : above the shooting star's high + 0.25 × ATR
Targets        : T1 nearest support / prior swing low · T2 measured: advance height × 0.5
                 T3 major support / Fib 0.618 of the advance
Note           : shorting requires borrow/margin in cash equity; in India intraday shorts must be
                 closed by the session end. See markets/india/
```

## 9. Invalidation
Close above the star's high (the rejection was temporary); price consolidates above the star for
several candles (absorption); higher-timeframe trend remains strongly up with fresh higher highs.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Called in an uptrend without resistance above | Location filter |
| Single-tick spike creating a fake long wick | Sanity-check the high against neighbouring bars |
| Confused with an inverted hammer | Explicit trend check |
| Appears repeatedly during a strong rally | Strong trends absorb them; require structural break |
| Shorting into a support-dense zone | Check room below before planning targets |

## 11. Historical evidence — honest position
Frequently cited as a warning sign in extended trends; practitioners note that in strong uptrends
shooting stars are routinely negated. No performance figure is claimed here. Test locally.

## 12. Worked example (illustrative, fictional)
```
Instrument: YZA · 1D · advance 640 → 712 in 9 sessions; resistance 710–715 (prior top)
Candle: o706 h714.8 l704.6 c706.8 · body 0.8 · range 10.2 · upper_wick 8.0 · upper/body = 10 ✔
Volume: 1.6× average on the star; next candle 1.9× and closes at 702.4 (below star body) ✔
Status: CONFIRMED (after the confirming close)
Setup : entry 702.0 · invalidation 715.3 · risk 13.3
        T1 690 (prior swing low) → 0.90R FAIL
        T2 676 (50% of the advance) → 1.95R ✔
Verdict: WAIT for a better location; a retest entry at 710 would give risk 5.3 and T1 at 3.8R —
        the same idea is tradeable only with the tighter invalidation.
```

## 13. Beginner summary (Hinglish)
**Shooting star:** upar ki lambi wick wali chhoti candle, jo **uptrend ke baad** aaye.

**Matlab:** buyers ne upar dhakka diya, par sellers ne wapas gira diya — high accept nahi hui.

**Yeh sell signal nahi hai** — sirf warning hai. Pehle agli candle ko is candle ki low ke neeche
close karna hoga.

**Stop:** is candle ki high ke thoda upar.

**Sabse strong kab?** Jab stock pehle se bahut tezi se upar chala ho aur resistance ke paas aaye.

## 14. Exercise
Find a shooting star at a resistance and one in the middle of a strong rally. For each, note what
happened in the next 5 candles. Then write the rule you would use to avoid the second case — and
check whether that rule would also have filtered out the good one.

---
*See also: [`inverted-hammer.md`](inverted-hammer.md) · [`hanging-man.md`](hanging-man.md) · [`evening-star.md`](evening-star.md)*
