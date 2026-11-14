# Rising Three Methods

**Group:** Continuation · **Candles:** 5 · **Reliability band:** Higher (within a trend)
**Detector:** `patterns.detect_rising_three_methods`

## 1. What it is
A five-candle continuation pattern in an uptrend:

1. A **long bullish** candle (the "method" candle).
2. **Three small candles** (usually bearish) that drift down but stay **inside candle 1's range**.
3. A **long bullish** candle that closes **above candle 1's close**, resuming the trend.

It is the candlestick expression of a healthy pullback: profit-taking contained within the prior
candle's range, then continuation.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Prior trend upward |
| 2 | Candle 1 is a long bullish candle (`body₁ ≥ 1.2 × avg_body`), ideally a wide-range bar |
| 3 | Candles 2–4 are small-bodied (each `body ≤ 0.5 × body₁`) |
| 4 | Candles 2–4 stay within candle 1's range: each `low ≥ low₁` and each `high ≤ high₁` (a small breach of the high is acceptable; breaching the low voids the pattern) |
| 5 | Candle 5 is bullish and closes **above candle 1's close** |
| 6 | All five closed |

Bearish mirror = **falling three methods** ([`falling-three-methods.md`](falling-three-methods.md)).

## 3. Anatomy
```
             ┌───────┐   <- candle 5 closes above candle 1's close
 ┌─────────┐ │       │
 │         │ │       │
 │  ┌─┐┌─┐┌─┐│       │
 │  └─┘└─┘└─┘│       │      <- candles 2-4: small, contained
 └─────────┘└───────┘
   candle 1
```

## 4. Where it means something
- During a healthy uptrend, especially after a strong impulse leg
- When the pullback holds above a moving average or a breakout retest level
- In the middle of a trend, not at its end (at an end it is more likely a top formation)

## 5. Interpretation
A trend that can absorb three down candles without giving back candle 1's gains is a trend with
genuine demand. The pattern is a **quality indicator for the trend**, which is why it is a
continuation rather than a reversal pattern.

Caution: by the time candle 5 completes, price has already resumed. The entry is often late. Many
practitioners use the pattern as *confirmation of trend health* rather than as an entry trigger.

## 6. Confirmation requirements
Candle 5's close completes it. Additional: volume expanding on candle 5; the pullback's low holding a
moving average or prior breakout level; higher timeframe aligned.

## 7. Volume
Ideal profile: high on candle 1, **contracting** through candles 2–4 (no selling pressure), high on
candle 5. If volume expands on the down candles, the "pullback" is actually distribution — a serious
warning.

## 8. Paper-trade entry conditions (illustrative)
```
Preferred entry : on candle 5's close, or on a shallow retest of candle 5's midpoint
Entry zone      : candle 5 close ± 0.2 × ATR
Invalidation    : below the lowest low of candles 2–4 (the pullback low) − 0.25 × ATR
Targets         : T1 measured move = candle 1's range projected from the breakout
                  T2 prior swing high / next resistance
                  T3 Fib extension of the impulse leg
Alternative     : use the pattern as a filter — do not short while it is forming
```

## 9. Invalidation
Any close below candle 1's low (the containment failed, so it was not a contained pullback); candle 5
failing to exceed candle 1's close; volume expanding on the down candles.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Down candles breaching candle 1's low | Rule 4 |
| Candle 5 tiny / closes only just above candle 1 | Require a clear close |
| Distribution disguised as a pullback (rising volume on down bars) | Volume check |
| Pattern at the top of an extended trend | Check extension and overhead resistance |
| Four or five small candles instead of three | Looseness changes the pattern's information; note the variant |

## 11. Historical evidence — honest position
Widely described as a continuation signal indicating trend strength. Because the pattern completes
only after price has resumed, measured "performance" depends heavily on the entry convention chosen.
Any statistic must specify the entry rule. None is asserted here.

## 12. Worked example (illustrative, fictional)
```
Instrument: LMN · 1D · uptrend from 240
C1: o246 c258 (bull, range 246–259, body 12) — long
C2: o257 c254 (small) · C3: o254 c251 (small) · C4: o251 c253 (small) — all inside 246–259 ✔
C5: o253.5 c261.5 (closes above C1 close 258 ✔) volume 1.7× ✔
Status: CONFIRMED
Entry 261.5 · invalidation 249.4 (below C3 low 250, buffer) · risk 12.1
T1 measured: 246 + 13 = 272.5 from breakout → 11/12.1 = 0.91R FAIL
T2 279 (prior swing high) → 1.45R (marginal) · T3 291 → 2.44R ✔
Verdict: marginal — BEARISH? No: BULLISH SCENARIO only with T3 as primary and a tighter stop at
        251.8 (below C4 low) giving risk 9.7 → T2 1.80R, T3 3.04R.
```

## 13. Beginner summary (Hinglish)
**Rising three methods:** ek badi green candle, phir teen chhoti candles jo uske range ke **andar** hi
rehti hain, phir ek badi green candle jo pehli ke close ke **upar** band ho.

**Matlab:** uptrend mein profit-booking aayi, par usne pehli candle ka gain wapas nahi liya — demand
abhi bhi strong hai. Isliye yeh **continuation** pattern hai.

**Entry:** paanchvi candle ke close par.

**Stop:** beech ki teen candles ki sabse neeche low ke neeche.

**Dhyan:** agar neeche wali candles par volume badh raha ho, to woh pullback nahi — distribution hai.

## 14. Exercise
Find a rising three methods and check the volume profile across all five candles. Compute the ratio
average(down-candle volume) / average(up-candle volume). If it exceeds 1.0, note it as a red flag and
check whether the trend continued. Repeat on five examples to see how often the flag mattered.

---
*See also: [`falling-three-methods.md`](falling-three-methods.md) · [`marubozu.md`](marubozu.md) ·
[`../price-action/trend-continuation.md`](../price-action/trend-continuation.md)*
