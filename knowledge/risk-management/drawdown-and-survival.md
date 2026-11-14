# Drawdown and Survival

## 1. Definitions

```
equity_curve : running account value
peak         : max equity so far
drawdown_t   = equity_t / peak_t − 1
max_drawdown = min over t of drawdown_t
recovery_factor = net_profit / max_drawdown
```

Measure drawdown in **R units** as well as currency, so that position-size changes do not distort the record.

## 2. The recovery arithmetic

| Drawdown | Gain needed to recover |
|----------|------------------------|
| 5% | 5.3% |
| 10% | 11.1% |
| 20% | 25.0% |
| 33% | 50.0% |
| 50% | 100.0% |
| 75% | 300.0% |
| 90% | 900.0% |

This asymmetry is the entire argument for drawdown control: a 50% loss requires a 100% gain just to break even.

## 3. Where drawdown comes from

```
max_drawdown ≈ f(loss_rate, average_loss, position_size, correlation, streak length)
```

Understated factors:

1. **Losing streaks are normal.** With a 45% win rate, a run of 7 losses occurs regularly over a few hundred trades.
   `P(7 losses in a row) ≈ 0.55^7 ≈ 1.5%` per window — which over 300 trades is likely at least once.
2. **Correlation.** Five "different" trades in the same sector are one bet. Aggregate correlated risk; do not sum
   independent risks.
3. **Costs.** A 0.2R cost per trade on a 1R winner is a 20% haircut on gross edge.
4. **Size creep.** Increasing size after wins (or after losses) turns a controlled curve into a volatile one.

## 4. Circuit breakers (define them in advance)

| Breaker | Example rule (educational) | Purpose |
|---------|---------------------------|---------|
| Per-trade | 0.25–1.0% risk | Bounds a single mistake |
| Daily loss limit | Stop after −2% or 2–3× per-trade risk | Prevents tilt |
| Weekly loss limit | Halve size after −4% | Prevents regime mismatch |
| Consecutive losses | After 4 losses, halve size until 2 wins | Addresses streak clustering |
| Max drawdown | Stop trading and review at −15% | Preserves the account |
| Correlation cap | ≤3% aggregate in one sector | Avoids one-factor ruin |

These are **conventions**, not prescriptions. The critical part is that they are written **before** trading and
followed without negotiation.

## 5. Underwater curve analysis

The **underwater curve** is `drawdown_t` over time. Reading it:

| Shape | Meaning |
|-------|---------|
| Short, shallow dips | Healthy; strategy matches regime |
| Long flat underwater period | Edge may have decayed; check out-of-sample |
| Deepening dips within an uptrend | Size too large relative to edge |
| Step changes (sudden jumps down) | Tail events / gap risk / correlation failure |

## 6. Risk of ruin (the arithmetic worth internalising)

With risk fraction `f` per trade and a losing streak of length `n`:

```
remaining_equity = (1 − f)^n
```

| f | 10 losses in a row |
|---|-------------------|
| 1% | 90.4% remaining |
| 2% | 81.7% |
| 5% | 59.9% |
| 10% | 34.9% |
| 25% | 5.6% |

Ten losses in a row happens to almost every strategy eventually. At 10% risk per trade, that is a two-thirds loss
of capital. This single table is why risk per trade is small.

## 7. What to do when you are in drawdown

1. **Reduce size** (halve it) — do not increase it to "get it back".
2. **Check whether the regime changed** (ADX, volatility, trend structure).
3. **Check execution**: are you following your rules, or improvising?
4. **Check the sample**: is this within the historical distribution of outcomes for your method, or outside it?
5. **Pause** if the max-drawdown breaker is hit. Review the journal before resuming.

## 8. Beginner summary (Hinglish)

**Drawdown** = peak se abhi tak ka girawat.

**Recovery ka ganit:**
- 10% loss → 11.1% gain chahiye
- 20% loss → 25% gain
- 50% loss → **100% gain**

Yeh asymmetry hi risk management ka poora reason hai.

**Risk of ruin:** 10 lagatar losses sabke saath hote hain.
- 1% risk → 90% bacha
- 10% risk → sirf 35% bacha

Isliye per-trade risk chhota rakha jata hai — skill ke liye nahi, **survive** karne ke liye.

**Pehle se likho:** daily loss limit, max drawdown, consecutive-loss rule. Baad mein negotiate mat karo.

**Drawdown mein kya karein:** size **aadha** karo, regime check karo, journal padho. Size badha kar "recover"
karne ki koshish = ruin.

## 9. Exercise

Using 1% risk, compute the equity remaining after 6 consecutive losses. Then compute it for 3% risk. Then compute
the gain required to recover each. Write one sentence about which risk level you could psychologically and
financially survive — and whether that changes your per-trade risk.

---
*See also: [`position-sizing.md`](position-sizing.md) · [`../quantitative-analysis/`](../quantitative-analysis/) ·
[`../../engines/backtesting/README.md`](../../engines/backtesting/README.md)*
