# Position Sizing

All examples use **hypothetical** equity. This is educational arithmetic, not advice.

## 1. Fixed-fractional sizing (the default)

```
risk_amount = equity × risk_pct
units       = risk_amount / |entry − stop|
notional    = units × entry
```

Example: `equity 500,000 · risk 0.75% = 3,750 · entry 1,204 · stop 1,186 · risk/unit 18`
→ `units = 208.3 → 208` (round **down**), `notional = 250,432` (50.1% of equity).

## 2. ATR-based sizing (volatility-adjusted)

```
stop_distance = k × ATR(14)         k = 1.5–2.5 (swing), 1.0–1.5 (intraday)
units         = risk_amount / stop_distance
```

Why it is better: as volatility expands, `stop_distance` grows and `units` shrink automatically. Risk per trade
stays roughly constant in currency terms across regimes.

Example: `ATR = 18 · k = 2 → stop 36 · risk_amount 3,750 → 104 units`.

## 3. Combining structure and volatility

The recommended hybrid:

```
stop = structural_level ± (0.25 × ATR buffer)
stop_distance = |entry − stop|
units = risk_amount / stop_distance
```

Structure gives the *reason*; ATR gives the *buffer* that prevents noise from invalidating a correct thesis.

## 4. Notional and exposure checks (do these too)

Sizing by risk alone can produce enormous notional if the stop is tight.

```
notional_pct = notional / equity
```

| Check | Reasonable ceiling (convention) |
|-------|--------------------------------|
| Single-name notional | ≤20–25% of equity |
| Total notional (cash) | ≤100% unless leverage is intended |
| Total open risk | ≤3–6% of equity |
| Correlated risk | Treat similar names as one bet |
| Liquidity | units ≤1% of average daily volume |

If notional breaches a ceiling, reduce units or find a wider-stop/lower-size variant — do not simply accept the
notional.

## 5. Fractional Kelly (only with a measured edge)

```
f* = (p × b − q) / b        p = win rate, q = 1−p, b = payoff ratio
use 1/4 to 1/2 of f*
```

Kelly is meaningless without a trustworthy `p` and `b`. If you have not measured them on a large out-of-sample
sample, do not use Kelly. Percentage-risk sizing does not require an edge estimate, which is why it is the default
here.

## 6. Unit accounting (R multiples)

Track everything in **R** (multiples of initial risk), not currency:

```
R_multiple = (exit − entry) / (entry − stop)      for a long
```

Benefits: results are comparable across position sizes and volatility regimes; a 2R win is a 2R win whether the
stock is ₹50 or ₹5,000.

## 7. Worked multi-scenario example

```
equity 500,000 · risk_pct 0.5% -> risk_amount 2,500

A) entry 1,204 · stop 1,186 (18)      -> 138 units · notional 166,152 (33.2%)
B) entry 1,204 · stop 1,176 (28)      ->  89 units · notional 107,156 (21.4%)
C) entry 1,204 · stop 1,150 (54)      ->  46 units · notional  55,384 (11.1%)

Same idea, three stop designs, three very different exposures.
D) wide stop (C) with 2,500 risk -> 46 units; if you instead forced 138 units with the 54-point stop,
   your risk would be 7,452 = 1.49% of equity — nearly triple the intended risk.
```

That is the arithmetic that makes "I'll just use the same quantity" dangerous.

## 8. Common errors

| Error | Guard |
|-------|-------|
| Fixed share quantity across different volatility regimes | Use ATR-based sizing |
| Rounding units up | Always round down |
| Ignoring notional | Check notional_pct |
| Ignoring correlated positions | Aggregate risk by sector/thesis |
| Sizing to a stop you do not believe in | If the stop is too far, the trade is wrong for the account |
| Using leverage without re-computing risk | Notional risk, not margin risk, is what you lose |
| Kelly without a measured edge | Do not |

## 9. Beginner summary (Hinglish)

**Position size ka formula:**
```
units = (equity × risk%) ÷ (entry − stop)
```
Example: equity 5,00,000, risk 0.5% = 2,500. Entry 1,204, stop 1,186 → risk per share 18 → 138 shares.

**Hamesha neeche round karo.** 138.8 → 138.

**ATR-based sizing better hai:** stop = 2 × ATR. Volatility badhe to size automatic chhota ho jayega.

**Notional bhi check karo:** 138 × 1,204 = 1,66,152 — equity ka 33%. Agar yeh zyada lage to size kam karo, stop
badha kar nahi.

**Sabse badi galti:** har trade mein same quantity. Alag stocks ki volatility alag hoti hai.

## 10. Exercise

Take one trade idea. Compute the size using three different stop designs (tight, structural, wide) with the same
1% risk budget. Compute notional for each. Then answer: which stop design gives an acceptable notional AND an
acceptable R:R? Write down the trade-off in one sentence.

---
*See also: [`stop-loss-design.md`](stop-loss-design.md) · [`costs-and-slippage.md`](costs-and-slippage.md) ·
[`../../core/risk-management.md`](../../core/risk-management.md)*
