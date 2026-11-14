# Three Black Crows

**Group:** Bearish reversal / continuation · **Candles:** 3 · **Reliability band:** Higher
**Detector:** `patterns.detect_three_black_crows`

## 1. What it is
Three consecutive **bearish** candles, each opening **within** the previous candle's body, each
closing **lower**, and each closing **near its own low** with a substantial body.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | Three consecutive bearish candles | Required |
| 2 | Each close < previous close | Monotonic decline |
| 3 | Each open within/near the previous body | No wild gaps |
| 4 | Each close near its low | `close_pos ≤ 0.3` |
| 5 | Substantial bodies | `body ≥ 0.6 × range` |
| 6 | Short lower wicks | `lower_wick ≤ 0.3 × range` |
| 7 | Follows an advance or a consolidation breakdown | Context |
| 8 | All three closed | Else `DEVELOPING` |

## 3. Anatomy
```
 ┌──┐
 │  │ ┌──┐
 │  │ │  │ ┌──┐
 └──┘ │  │ │  │
      └──┘ └──┘
```

## 4. Where it means something
Breaking down from a distribution range; reversing an over-extended advance; failing at a major
resistance. Weak when it occurs after price has already fallen a long way (then it may be the
capitulation rather than the start).

## 5. Interpretation
Three intervals of consistent selling with closes at the lows. Consistent, orderly distribution —
not panic. When it appears right after a blow-off top, it is the mirror of three white soldiers at a
base: the beginning of a trend change.

Caution: three consecutive down days are *common*. The strictness lies in rules 4–6 (closes at lows,
short lower wicks). Without them, you are just counting red candles.

## 6. Confirmation requirements
- Minimum: third candle closes as specified.
- Good: a fourth candle fails to reclaim the third's midpoint, or a bounce fails at the third's low.
- Strong: breakdown of the last swing low with volume; retest of the broken level fails.
- Invalidated: price closes above the first candle's open.

## 7. Volume
Rising volume across the three candles is the ideal. Falling volume suggests a drift rather than
distribution — and drift often reverses. A volume climax on the third candle can mark short-term
exhaustion; a bounce may follow before continuation.

## 8. Paper-trade entry conditions (illustrative)
```
Preferred     : wait for a weak bounce (1–3 candles) that fails below the third candle's midpoint,
                then enter short on the resumption close
Aggressive    : sell the third candle's close (chasing; worse R:R)
Entry zone    : failed-bounce high + 0.1 × ATR
Invalidation  : above candle 2's high (or candle 1's open for a structural stop)
Targets       : T1 measured move = sequence height projected down
                T2 prior swing low · T3 major support
```

## 9. Invalidation
Close above candle 1's open; a strong bullish reversal candle immediately after (e.g. hammer at
support) — that suggests the three crows were a shakeout into support.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Three red candles with big lower wicks (buyers appearing) | Rule 6 |
| Three crows into major support | Check room below |
| Small-bodied drift | Rule 5 |
| Capitulation at the end of a long decline | Check extension from the 20-EMA |
| Low-volume decline | Volume check |

## 11. Historical evidence — honest position
Structurally informative within a distribution or base breakdown; at the end of an extended decline,
the same shape frequently marks exhaustion rather than initiation. Both readings are qualitative.
No statistic is claimed here.

## 12. Worked example (illustrative, fictional)
```
Instrument: NOP · 1D · range 410–430 for a month; breakdown:
 C1 o428 c419 (close_pos 0.2) · C2 o420 c411 (close_pos 0.15) · C3 o412 c402 (close_pos 0.1)
 All bodies ≥ 7 · lower wicks ≤ 2 ✔ · Volume 1.4×, 1.6×, 1.9× ✔ · Status: CONFIRMED
 Plan  : wait for a bounce to 406–408 failing; entry 405.5
         invalidation 413.5 (candle 3 high + buffer) · risk 8.0
         T1 398 (range low / measured) → 0.94R FAIL
         T2 390 → 1.94R ✔ · T3 378 → 3.44R ✔
 Verdict: BEARISH SCENARIO only with T2/T3 as primary; T1 is not viable — state it.
```

## 13. Beginner summary (Hinglish)
**Three black crows:** teen lagatar red candles, har ek pichhli se neeche close, har ek apni low ke
paas band, wicks chhoti.

**Matlab:** teen sessions tak sellers ka lagatar control — distribution ho raha hai.

**Important:** sirf teen red candles dekhna kaafi nahi. Close low ke paas hona chahiye aur wicks
chhoti. Warna woh sirf girawat hai, pattern nahi.

**Entry:** teen candles ke baad ek weak bounce aaye jo fail ho jaye — uske resumption par short.

**Stop:** doosri candle ki high ke upar.

## 14. Exercise
Count the number of times your chosen stock had three consecutive red candles in the last year. Then
count how many met the *full* three-black-crows rules. Note the ratio. That ratio is the difference
between "counting colours" and "reading a pattern" — and it is usually large.

---
*See also: [`three-white-soldiers.md`](three-black-crows.md) · [`marubozu.md`](marubozu.md)*
