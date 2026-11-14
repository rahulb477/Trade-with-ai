# VWAP (Volume Weighted Average Price)

**Family:** Volume/participation, intraday reference level · **Reset:** every session (standard)
**Implementation:** `indicators.vwap(highs, lows, closes, volumes, reset_index=0)`

## 1. Calculation

```
typical_price_t = (high_t + low_t + close_t) / 3
VWAP_t = Σ(typical_price_i × volume_i) / Σ(volume_i)      for i from the session start to t
```

Key properties:

- **Cumulative and path-dependent.** Adding a bar changes the value; removing one changes history.
- **Resets each session** in the standard form. "Anchored VWAP" starts from a chosen event (an earnings
  date, a swing low) instead.
- Requires volume. Without volume data, VWAP cannot be computed — say so rather than substituting a
  typical-price average.

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| Price above VWAP | Buyers in control *for the session*; average participant is in profit |
| Price below VWAP | Sellers in control; average participant is in loss |
| Price hugging VWAP | Balanced auction; no edge |
| VWAP flat, price whipsawing across | Choppy session; avoid breakout trades |
| Reversion to VWAP after an extended move | Common intraday mean-reversion behaviour |
| VWAP as support on pullbacks in an uptrend day | The standard "buy the dip to VWAP" context |

**The most important framing:** VWAP is the price at which the *average* participant in the session has
transacted. Being above it means the average long is profitable — which affects behaviour (holders are
less likely to panic-sell, and short sellers are under pressure).

## 3. Variants

| Variant | Anchor | Use |
|---------|--------|-----|
| Session VWAP | Today's open | Standard intraday |
| Weekly / monthly VWAP | Week/month start | Swing reference |
| Anchored VWAP | A specific event/level | "Where is the average holder from the earnings gap?" |
| VWAP bands (σ) | Session VWAP ± kσ | Intraday envelope; mean-reversion extremes |

## 4. Limitations

- **Intraday only (by default).** Applying "VWAP" across days without resetting produces a drifting
  average of little use.
- **Volume quality dependent.** Block deals, off-market trades, or bad volume data corrupt it.
- **Not a signal.** Price can stay above VWAP all day in a trend and never "revert".
- **Institutional execution reference, not a prediction.** Its power comes from algos benchmarking to it,
  which is a behavioural effect, not a law.
- **Illiquid instruments** produce a VWAP dominated by a few prints.

## 5. Combining

- **VWAP + market structure**: an intraday trend day holds above VWAP and each pullback to VWAP holds.
  A failure to hold VWAP on a pullback is an early sign the day is turning.
- **VWAP + volume**: rising volume on moves *away* from VWAP and falling volume on returns to it is a
  healthy signature.
- **VWAP + ATR**: distance in ATR from VWAP indicates stretch.
- **VWAP + opening range**: opening-range breakout above VWAP is a stronger signal than either alone.

## 6. Reading from a screenshot

Extractable: whether price is above/below the line; whether the line is flat or sloping; how many times
price has crossed it in the visible session; whether it coincides with a horizontal level.

Not extractable: the VWAP value without a label; the session boundaries if the x-axis is unlabelled
(check the gridline spacing for session breaks).

## 7. Worked example

```
Session bars (fictional):
  H 100, L 98,  C 99,  V 1_000  -> TP 99.00  cumulative = 99_000 / 1_000 = 99.00
  H 101, L 99,  C 100, V 2_000  -> TP 100.00 cumulative = (99_000+200_000)/3_000 = 99.67
  H 102, L 100, C 101, V 1_000  -> TP 101.00 cumulative = (299_000+101_000)/4_000 = 100.00
Price 101 vs VWAP 100: the average participant is 1 point in profit -> buyers in control.
The larger volume in bar 2 (2_000) pulled the VWAP toward 100 more strongly than bar 3's volume.
See tests/indicators/test_vwap.py.
```

## 8. Beginner summary (Hinglish)

**VWAP kya hai?** Din bhar ka **volume-weighted average price** — matlab jitna volume jis price par
hua, usko weight milta hai. Har session start par reset hota hai.

**Matlab kya?** Agar price VWAP ke **upar** hai, to aaj ke average buyer profit mein hain — buyers ka
control. Neeche hai to average buyer loss mein.

**Intraday trend day:** price VWAP ke upar rehta hai aur har pullback VWAP par hold karta hai.

**Galti:** VWAP ko support/resistance ki tarah treat karna bina volume dekhe. Aur intraday ke bahar
VWAP use karna.

## 9. Exercise

Pick one trading day on a 5-minute chart. Mark VWAP. Count how many times price crossed it. Then classify
the day as trending or balanced. Write a rule for what you would do differently on a balanced day versus
a trend day — and check it against three more days.

---
*See also: [`volume-profile.md`](volume-profile.md) · [`obv.md`](obv.md) · [`atr.md`](atr.md)*
