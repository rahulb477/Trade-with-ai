# Falling Three Methods

**Group:** Continuation · **Candles:** 5 · **Reliability band:** Higher (within a trend)
**Detector:** `patterns.detect_falling_three_methods`

## 1. What it is
The bearish mirror of rising three methods, in a downtrend:

1. A long **bearish** candle.
2. Three **small** candles (usually bullish) drifting up but staying inside candle 1's range.
3. A long **bearish** candle closing **below candle 1's close**.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Prior trend downward |
| 2 | Candle 1 long bearish (`body₁ ≥ 1.2 × avg_body`) |
| 3 | Candles 2–4 small (`body ≤ 0.5 × body₁`) |
| 4 | Candles 2–4 contained: each `high ≤ high₁` and each `low ≥ low₁` (a small breach of the low is tolerable; breaching the high voids it) |
| 5 | Candle 5 bearish, closing **below candle 1's close** |
| 6 | All five closed |

## 3. Anatomy
```
 ┌─────────┐
 │         │
 │  ┌─┐┌─┐┌─┐
 │  └─┘└─┘└─┘
 └─────────┘ ┌───────┐   <- candle 5 closes below candle 1's close
             │       │
             └───────┘
```

## 4. Where it means something
Mid-trend after a strong down leg; when the bounce fails to reach the prior swing high; after a
breakdown retest that fails. At the *bottom* of an extended decline, a "falling three methods" is more
likely to be a basing attempt — treat with suspicion.

## 5. Interpretation
Sellers absorbed a three-candle bounce without surrendering candle 1's gain. Supply is still dominant.
The pattern says the downtrend is intact, not that it will accelerate forever.

## 6. Confirmation requirements
Candle 5's close completes it. Additional: volume expanding on candle 5; the bounce capped by a moving
average; higher timeframe aligned lower.

## 7. Volume
Ideal: high on candle 1, contracting through 2–4 (no real buying), high on candle 5. Expanding volume
on the bounce candles suggests genuine accumulation — then the pattern is more likely to fail.

## 8. Paper-trade entry conditions (illustrative)
```
Preferred entry : candle 5's close, or a shallow retest of candle 5's midpoint
Entry zone      : candle 5 close ± 0.2 × ATR
Invalidation    : above the highest high of candles 2–4 + 0.25 × ATR
Targets         : T1 measured move = candle 1's range projected down
                  T2 prior swing low · T3 Fib extension of the down leg
Short constraints: verify the instrument is shortable in your market and session; intraday equity
                  shorts in India must be squared off before the close. See markets/india/
```

## 9. Invalidation
Any close above candle 1's high; candle 5 failing to trade below candle 1's close; strong bullish
reversal at a major support.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Bounce breaching candle 1's high | Rule 4 |
| Candle 5 marginal | Require a clear close |
| Pattern at a major support | Check room below |
| Volume expanding on the bounce | Volume check |
| Shorting into a squeeze/event | Event-risk gate from `core/decision-engine.md` |

## 11. Historical evidence — honest position
Treated as a continuation/trend-strength signal in the literature. As with rising three methods, any
performance number depends entirely on the entry convention. None is asserted.

## 12. Worked example (illustrative, fictional)
```
Instrument: OPQ · 1D · downtrend from 410
C1: o404 c392 (range 390–405, body 12)
C2: o393 c396 · C3: o396 c399 · C4: o399 c397 (all inside 390–405 ✔)
C5: o397 c389 (closes below C1 close 392 ✔) volume 1.8× ✔
Status: CONFIRMED
Entry 388.8 · invalidation 401.2 (above C3 high 400 + buffer) · risk 12.4
T1 measured: 405 − 15 = 390 → negative (already through) — recompute from the breakdown:
            390 − 15 = 375 → 1.11R FAIL
T2 368 (prior swing low) → 1.68R ✔ · T3 355 → 2.73R ✔
Verdict: BEARISH SCENARIO with T2/T3 as primary; T1 is not usable — say so explicitly.
```

## 13. Beginner summary (Hinglish)
**Falling three methods:** downtrend mein ek badi red candle, phir teen chhoti candles jo uske andar
rahein, phir ek badi red candle jo pehli ke close ke neeche band ho.

**Matlab:** bounce aaya par usne pehli candle ka loss wapas nahi liya — sellers abhi bhi strong hain.

**Entry:** paanchvi candle ke close par. **Stop:** beech ki teen candles ki sabse upar wali high ke upar.

**Dhyan:** agar bounce par volume badh raha hai, to yeh pattern fail ho sakta hai.

## 14. Exercise
Find a falling three methods. Compute the measured-move target and compare it with the R:R. Then check
what the bounce candles' volume was. Write one line on whether the volume profile would have changed
your decision.

---
*See also: [`rising-three-methods.md`](rising-three-methods.md) · [`three-black-crows.md`](three-black-crows.md)*
