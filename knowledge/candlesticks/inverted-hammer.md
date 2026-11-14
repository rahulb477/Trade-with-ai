# Inverted Hammer

**Group:** Bullish reversal · **Candles:** 1 · **Reliability band:** Moderate (weaker than hammer)
**Detector:** `patterns.detect_inverted_hammer`

---

## 1. What it is

A single small-bodied candle with a **long upper wick**, appearing **after a decline**. Buyers
attempted a rally during the interval and were pushed back, but the attempt itself signals that
buying interest has appeared where previously there was none.

It is the mirror image of the hammer, and the weaker of the two: a long upper wick means the close
is *not* near the high, so sellers still had the final say in that interval.

---

## 2. Formation rules

| # | Rule | Threshold |
|---|------|-----------|
| 1 | Prior trend is **downward** | Measurable decline over recent candles |
| 2 | `upper_wick ≥ 2 × body` | Defining feature |
| 3 | `lower_wick ≤ 0.5 × body` | Body sits near the bottom |
| 4 | `body / range ≤ 0.35` | Small real body |
| 5 | Range is not abnormally small | `range ≥ 0.5 × average_range(20)` |
| 6 | Closed candle | Otherwise `DEVELOPING` |

Distinguishing from the **shooting star**: identical shape, opposite context. Shooting star appears
after an *advance*. The same candle can be an inverted hammer or a shooting star depending on
where it sits — context is the whole pattern.

---

## 3. Anatomy

```
     ▲
     │      <- long upper wick: buyers tried, sellers pushed back
     │
   ┌─┴─┐
   └───┘    <- small body near the low of the range
```

---

## 4. Where it means something

- At support, after a decline, especially the **second or third** test of a level
- On the day of a gap-down that gets partially filled
- At the bottom of a falling channel, or at a Fib 0.618 retracement of a prior advance
- Following a volume climax (capitulation bar), the next interval's failed rally is informative

Weak locations: mid-range, at a level that has already broken, in a strong downtrend with no other
evidence.

---

## 5. Interpretation

The candle says: sellers were still in control at the close, but the *range* expanded upward for the
first time in a while. It is a "first attempt", not a "success".

Documented treatments consistently rank it below the hammer because the close is weak. Some
practitioners require it to be **confirmed by a gap up** or by the next candle closing above the
inverted hammer's high before considering it at all.

---

## 6. Confirmation requirements

| Level | Confirmation |
|-------|--------------|
| Minimum | Next candle closes above the inverted hammer's **body** high |
| Good | Next candle closes above the inverted hammer's **high** |
| Strong | Gap up above the high, or break of the prior swing high on rising volume |
| Invalidated | Close below the inverted hammer's low |

Because the close is weak, be stricter here than with a hammer: prefer level *good* or better.

---

## 7. Volume

- Above-average volume on the attempt = genuine buying interest being absorbed.
- A volume spike plus a modest close is ambiguous: it can be distribution into strength.
- Rising volume on the following bullish candle is the decisive input.

---

## 8. Paper-trade entry conditions (illustrative)

```
Long trigger   : close above inverted-hammer high (preferred) or body high (aggressive)
Entry zone     : breakout level ± 0.1 × range
Invalidation   : below inverted-hammer low (buffer 0.25 × ATR)
Targets        : T1 prior swing high / nearest resistance
                 T2 measured move = height of the decline × 0.5–1.0
                 T3 major resistance / prior consolidation
Note           : because confirmation is weaker, consider half-size relative to a hammer setup
```

---

## 9. Invalidation

1. Close below the inverted hammer's low.
2. Two consecutive closes back inside the prior candle's range without progress.
3. Higher-timeframe structure breaks lower.
4. The long upper wick is explained by a news spike that fully reversed and stayed reversed.

---

## 10. Common false signals

| False signal | Guard |
|--------------|-------|
| Confusing it with a shooting star in an uptrend | Check the preceding trend explicitly |
| Counting it as confirmation without a following bullish close | Require the confirmed status |
| Ignoring that the long wick is *supply*, not demand | Treat the wick high as resistance until broken |
| Mid-trend appearance with no support | Location filter |
| Very long wick from a single erroneous tick (illiquid stock) | Sanity-check the tick data / average range |

---

## 11. Historical evidence — honest position

This pattern is widely described as *less reliable than the hammer* in the technical-analysis
literature, largely because the close is away from the extreme. No specific performance statistic
is asserted here. Measure it yourself with `engines/backtesting/` if you intend to trade it.

---

## 12. Worked example (illustrative, fictional)

```
Instrument: XYZ · Timeframe: 4H · Context: decline from 88 to 71, support zone 70–72.
Candle: open 72.0, high 74.8, low 71.6, close 72.4
        body 0.4, range 3.2, upper_wick 2.4, lower_wick 0.4
        upper/body = 6.0 · body_ratio 0.125 -> rules satisfied
Volume: slightly above average (1.2×)
Status: CONFIRMED
Setup : trigger close > 74.8 · entry 74.9 · invalidation 71.3
        risk 3.6 · T1 78.6 (prior swing high) -> 3.7/3.6 = 1.03R (fails)
Verdict: WAIT — not enough room. Would only qualify if T1 were ≥ 80.3 (1.5R).
```

---

## 13. Beginner summary (Hinglish)

**Inverted hammer kya hai?** Girte market ke baad ek candle jisme upar ki wick lambi ho aur body
neeche ki taraf chhoti ho.

**Matlab:** buyers ne upar jaane ki koshish ki, par sellers ne wapas gira diya. Isliye yeh hammer se
kamzor hai — close upar nahi hua.

**Kab manna?** Jab agli candle is candle ki high ke upar close kare. Bina confirmation ke yeh sirf
"koshish" hai, "jeet" nahi.

**Stop loss:** is candle ki low ke neeche.

**Yaad rakho:** same shape, agar uptrend ke baad aaye to yeh **shooting star** ban jata hai — bearish.

---

## 14. Exercise

Find an inverted hammer and the nearest shooting star on the same chart. Write down the preceding
trend for each. Then check: does the *shape alone* tell you which is which? (It does not.) Write one
sentence explaining why context changes the meaning of identical geometry.

---

*See also: [`hammer.md`](hammer.md) · [`shooting-star.md`](shooting-star.md)*
