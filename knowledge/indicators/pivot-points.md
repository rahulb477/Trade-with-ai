# Pivot Points

**Family:** Levels · **Default:** Classic floor-trader pivots from the prior session
**Implementation:** `indicators.pivot_points(high, low, close, method="classic")`

## 1. Calculation

### Classic

```
P  = (H + L + C) / 3
R1 = 2P − L
S1 = 2P − H
R2 = P + (H − L)
S2 = P − (H − L)
R3 = H + 2 × (P − L)
S3 = L − 2 × (H − P)
```

### Fibonacci

```
P  = (H + L + C) / 3
R1 = P + 0.382 × (H − L)   S1 = P − 0.382 × (H − L)
R2 = P + 0.618 × (H − L)   S2 = P − 0.618 × (H − L)
R3 = P + 1.000 × (H − L)   S3 = P − 1.000 × (H − L)
```

### Camarilla

```
R1 = C + (H − L) × 1.1/12      S1 = C − (H − L) × 1.1/12
R2 = C + (H − L) × 1.1/6       S2 = C − (H − L) × 1.1/6
R3 = C + (H − L) × 1.1/4       S3 = C − (H − L) × 1.1/4
R4 = C + (H − L) × 1.1/2       S4 = C − (H − L) × 1.1/2
```

### Woodie

```
P  = (H + L + 2C) / 4          (weights the close more heavily)
R1 = 2P − L      S1 = 2P − H
```

## 2. Interpretation

| Level | Conventional use |
|-------|------------------|
| Pivot (P) | The session's fair-value dividing line; above = bullish bias, below = bearish |
| R1 / S1 | First targets or first fade levels |
| R2 / S2 | Stronger extension targets |
| R3 / S3 | Extreme levels; often fade candidates on a normal day |
| Camarilla R3/S3 | Common reversal-fade references in intraday trading |

The *method* matters less than *consistency*: pivots work partly because many participants compute the same
numbers from the same prior session.

## 3. Timeframe mapping

| Pivot period | Derived from | Used on |
|--------------|--------------|---------|
| Daily | Prior day's H/L/C | Intraday (5m–1h) |
| Weekly | Prior week | Daily |
| Monthly | Prior month | Weekly/daily |

Mixing periods (e.g. daily pivots on a weekly chart) produces levels nobody else is watching.

## 4. Limitations

- **Derived from one session.** A single unusual session (an expiry, a news spike) produces distorted levels.
- **No regime awareness.** In a strong trend, price blows through R2/R3 and never looks back; fading extremes
  is a range strategy and fails in trends.
- **Method divergence.** Classic, Fibonacci, Camarilla and Woodie give different numbers. Two traders
  "using pivots" may be watching different lines.
- **Gap sessions** distort the calculation (H/L/C from a gapped session).
- **Crowded levels.** Stops cluster just beyond S1/R1 — pivot levels are prime stop-hunt territory (see
  `workflows/trap-detection.md`).

## 5. Combining

- **Pivots + structure**: a pivot that coincides with a prior swing level is much stronger than either alone.
- **Pivots + volume profile**: a pivot near the POC is a high-conviction magnet.
- **Pivots + ATR**: check whether R1 is within 1 ATR of the open (realistic daily target) or 4 ATR (fantasy).
- **Pivots + ADX**: fade R2/R3 only when ADX is low (range regime).

## 6. Reading from a screenshot

Extractable: the drawn pivot lines and their labels, if the platform prints them; where price sits relative to
them.

Not extractable: the values if the labels are hidden. Never compute pivots from a screenshot and present them
as the platform's levels — a second calculation may differ.

## 7. Worked example

```
Prior session: H = 1_260, L = 1_220, C = 1_248
P  = (1_260 + 1_220 + 1_248)/3 = 1_242.67
R1 = 2(1_242.67) − 1_220 = 1_265.33      S1 = 2(1_242.67) − 1_260 = 1_225.33
R2 = 1_242.67 + 40 = 1_282.67            S2 = 1_242.67 − 40 = 1_202.67
R3 = 1_260 + 2(1_242.67 − 1_220) = 1_305.33   S3 = 1_220 − 2(1_260 − 1_242.67) = 1_185.33
If today's open is 1_250 and ATR(14) = 22, R1 at 1_265 is 0.7 ATR away — a realistic intraday target.
R3 at 1_305 is 2.5 ATR away — unlikely on a normal day.
See tests/indicators/test_pivots.py.
```

## 8. Beginner summary (Hinglish)

**Pivot points kya hain?** Pichhle session ke High, Low, Close se banaye gaye levels — P (pivot), R1/R2/R3
(upar), s1/s2/s3 (neeche).

**Kaise use karein:**
- Price **P ke upar** = bullish bias, **neeche** = bearish.
- R1/S1 pehla target ya pehla fade level.
- R3/S3 extreme — normal din mein wahan tak price kam jata hai.

**Dhyan:** strong trend mein price R2/R3 tod deta hai — wahan fade karna range strategy hai, trend mein nahi.
Aur S1/R1 ke thoda bahar stop-hunt hota hai.

## 9. Exercise

Compute classic pivots for five sessions. For each, record: the day's high/low relative to R1/S1, whether R2/S2
were tagged, and the day's ADX. Then answer: on which days would fading R1 have worked, and what did the ADX
tell you in advance?

---
*See also: [`fibonacci.md`](fibonacci.md) · [`volume-profile.md`](volume-profile.md) · [`atr.md`](atr.md)*
