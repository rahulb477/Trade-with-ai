# MFI (Money Flow Index)

**Family:** Volume-weighted momentum oscillator · **Default period:** 14 · **Range:** 0–100
**Implementation:** `indicators.mfi(h, l, c, v, 14)`

## 1. Calculation

```
TP_t = (high + low + close) / 3
raw_money_flow_t = TP_t × volume_t

positive_flow = Σ raw_money_flow where TP_t > TP_{t−1}
negative_flow = Σ raw_money_flow where TP_t < TP_{t−1}
(TP unchanged contributes to neither)

money_ratio = positive_flow / negative_flow
MFI = 100 − 100 / (1 + money_ratio)
```

MFI is often described as "volume-weighted RSI". It is defined as 50 when `negative_flow == 0` and no
positive flow exists; this repository returns `100` when negative flow is zero and positive flow is
non-zero, `0` when the reverse holds, and `None` when both are zero.

## 2. Interpretation

| Reading | Conventional meaning |
|---------|---------------------|
| > 80 | Overbought with volume confirmation |
| < 20 | Oversold with volume confirmation |
| 50 line | Balance |
| Divergence | Price makes a new extreme; MFI does not |

The value of MFI over RSI is that it requires **both** price direction and volume to change. A rally on
falling volume does not push MFI up as fast as a rally on rising volume.

## 3. Common settings

| Period | Use |
|--------|-----|
| 14 | Standard |
| 7 / 9 | Short-term intraday |
| 21 / 28 | Swing |

## 4. Limitations

- **Same trend problem as RSI**: MFI can stay above 80 for weeks in a strong uptrend.
- **Volume quality dependent** — bad or missing volume invalidates the indicator.
- **Bar-level approximation.** MFI cannot know whether the volume occurred at the high or the low of the bar.
- **Correlated with RSI** in practice, so using both is redundant.
- **Illiquid instruments** give erratic readings.

## 5. Combining

- **MFI + price structure**: an MFI divergence at a resistance is a stronger warning than an RSI divergence
  because it also implies *falling participation*.
- **MFI + OBV**: MFI is bounded and oscillatory; OBV is cumulative. Together they show participation from two
  angles — but both depend on volume, so they are not fully independent.
- **MFI + ADX**: only fade extremes when ADX is low.
- **MFI + volume profile**: an MFI extreme at a low-volume node is less meaningful than at an HVN.

## 6. Reading from a screenshot

Extractable: whether the line is above 80 / below 20 (if gridlines visible); divergence versus price; whether
a numeric label is printed.

Not extractable: exact values without labels.

If the chart has no volume panel, MFI cannot exist — say so.

## 7. Worked example

```
Window of 3 (illustrative, period truncated for brevity):
 TP 100, vol 1_000 -> positive 100_000
 TP 102, vol 1_500 -> positive 153_000   (positive total 253_000)
 TP 101, vol 1_200 -> negative 121_200
 TP 103, vol   900 -> positive  92_700   (positive total 345_700)
 money_ratio = 345_700 / 121_200 = 2.852
 MFI = 100 − 100/(1+2.852) = 100 − 25.96 = 74.04
Reading: strong, volume-supported bullish flow, below the 80 threshold.
See tests/indicators/test_mfi.py.
```

## 8. Beginner summary (Hinglish)

**MFI kya hai?** RSI jaisa oscillator, par isme **volume bhi** count hota hai. Isliye ise "volume-weighted RSI"
kehte hain.

**Matlab:**
- MFI **80 ke upar** = price upar ja raha hai aur volume bhi support kar raha hai (overbought zone).
- MFI **20 ke neeche** = oversold with volume.
- **Divergence:** price naya high bana raha hai par MFI nahi — matlab rally mein volume/force kam ho rahi hai.

**RSI se behtar kab?** Jab tumhe participation bhi dekhni ho. **Par:** agar volume data kharab hai to MFI
bekaar hai.

**Dhyan:** RSI aur MFI dono ek saath use karna double confirmation nahi hai.

## 9. Exercise

Find a rally where price made a new high twice. Record MFI at both highs and the volume on both. Did MFI confirm
or diverge? Then check what happened over the next 15 bars. Note how many similar cases you would need before
trusting the pattern.

---
*See also: [`rsi.md`](rsi.md) · [`obv.md`](obv.md) · [`volume-profile.md`](volume-profile.md)*
