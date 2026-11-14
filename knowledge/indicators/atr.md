# ATR (Average True Range)

**Family:** Volatility · **Default period:** 14 · **Implementation:** `indicators.atr(highs, lows, closes, 14)`

## 1. Calculation

```
TR_t = max( high_t − low_t,
            |high_t − close_{t−1}|,
            |low_t  − close_{t−1}| )

# ATR uses Wilder smoothing (same as RSI):
ATR_1 = mean(TR[1..period])
ATR_t = (ATR_{t−1} × (period−1) + TR_t) / period
```

The `|high − prev close|` terms capture **gaps**, which is why ATR is more honest than a high-low range
average. A gap-heavy instrument (many Indian mid-caps, crypto) produces a materially higher ATR than its
intraday range would suggest.

## 2. Interpretation

ATR is not directional. It answers three questions:

| Question | How |
|----------|-----|
| How far does this instrument typically move per bar? | ATR in price units |
| How wide should a stop be to avoid noise? | 1.5–2.5 × ATR beyond structure |
| How volatile is it relative to its own history? | ATR / price (%), or ATR percentile |

| Reading | Meaning |
|---------|---------|
| ATR rising | Volatility expanding — usually with a trend or event |
| ATR falling | Compression — often precedes expansion |
| ATR at multi-month low | Squeeze regime |
| ATR spike | Event/climax; stops are more likely to be swept |
| ATR% very high (>5% daily) | Position sizing must be much smaller |

## 3. Using ATR for stops and sizing

```
stop_distance = k × ATR        k typically 1.5–2.5 for swing, 1.0–1.5 for intraday
position_size = (equity × risk_pct) / stop_distance      (units)
```

Why ATR-based sizing is superior to fixed-share sizing: as volatility expands, ATR expands, so the position
shrinks automatically. The risk per trade stays roughly constant in currency terms.

Worked: `equity 500_000 × 0.75% = 3_750` risk; `ATR = 18`, `k = 2` → stop 36 away → 104 units.

## 4. Common settings

| Period | Use |
|--------|-----|
| 14 | Standard |
| 7 | More responsive; noisier |
| 21 / 28 | Smoother; better for regime classification |

Also common: **ATR as a percentage of price** (`ATR/close × 100`) to compare across instruments, and
**normalised ATR percentile** over 1–2 years to classify the current volatility regime.

## 5. Limitations

- **Not directional.** A high ATR tells you nothing about up or down.
- **Lagging.** Wilder smoothing responds slowly to a shock; a 14-period ATR takes many bars to reflect a
  new regime.
- **Gap distortion.** On instruments with frequent gaps, ATR overstates typical intrabar movement.
- **Period sensitivity** changes stop widths materially, which changes results — do not tune `k` and the
  period on the same sample you report.
- **Illiquid instruments** have meaningless ATR (a single print can dominate TR).

## 6. Combining

- **ATR + structure**: the stop goes *beyond structure*, with an ATR buffer added — never purely ATR, never
  purely structure with a round-number buffer.
- **ATR + Bollinger bandwidth**: both are volatility; use one for sizing, the other for regime.
- **ATR + ADX**: ADX for direction strength, ATR for magnitude.
- **ATR + position sizing**: the only combination that directly protects capital.

## 7. Reading from a screenshot

Extractable: whether a volatility panel is expanding or contracting; the numeric label if printed;
relative candle sizes (a good proxy — you can see whether recent candles are larger than the visible
average).

Not extractable: the ATR value without a label. You may say "recent candles are visibly larger than the
prior ones, suggesting rising volatility", which is an observation, not a number.

## 8. Worked example

```
Bars (fictional):
 prev close 100
 bar1: H 104 L 99  C 102 -> TR = max(5, 4, 1) = 5
 bar2: H 106 L 101 C 105 -> TR = max(5, 4, 1) = 5
 bar3: H 103 L  97 C  99 -> TR = max(6, 2, 8) = 8   (note the |low − prev close| term dominating)
 If period = 3: ATR = (5+5+8)/3 = 6.0
 Stop at k = 2 -> 12 points. Position = risk_amount / 12 units.
See tests/indicators/test_atr.py.
```

## 9. Beginner summary (Hinglish)

**ATR kya hai?** Ek average of "true range" — matlab har candle mein price kitna hilta hai (gaps ko bhi
count karke).

**Direction nahi batata** — sirf batata hai ki movement kitni badi hoti hai.

**Kaam kaise aata hai:**
1. **Stop loss:** structure se bahar + ATR buffer, taaki normal noise se stop na hate.
2. **Position size:** `risk amount ÷ (2 × ATR)` = kitne shares.
3. **Volatility regime:** ATR kam = squeeze, bada move aa sakta hai. ATR zyada = risk zyada, size chhota.

**Best practice:** ATR badhne par position automatic chhoti ho jati hai — yahi capital protection hai.

## 10. Exercise

Compute ATR(14) as a percentage of price for your instrument across two years. Find its 20th and 80th
percentiles. Then take ten historical trades sized with fixed shares and re-size them with ATR-based
sizing. Compare the worst single loss in each case. Write one sentence about what changed.

---
*See also: [`bollinger-bands.md`](bollinger-bands.md) · [`adx.md`](adx.md) · [`../core/risk-management.md`](../../core/risk-management.md)*
