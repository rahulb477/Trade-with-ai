# Expectancy and Trade Metrics

## 1. Core definitions

```
win_rate    p   = wins / total
payoff      b   = average_win / average_loss          (in R, average_loss is positive)
expectancy  E   = p × avg_win_R − (1 − p) × avg_loss_R
profit_factor   = gross_profit / gross_loss
break_even_p    = 1 / (1 + b)
```

## 2. Worked examples

**Trend-following profile** (low win rate, big winners):

```
p = 0.38, avg_win = 2.6R, avg_loss = 1.0R
E = 0.38 × 2.6 − 0.62 × 1.0 = 0.988 − 0.62 = +0.368R per trade
profit factor = (0.38 × 2.6) / (0.62 × 1.0) = 0.988 / 0.62 = 1.59
break_even p  = 1 / 3.6 = 27.8%  -> the method has margin
```

**Mean-reversion profile** (high win rate, small winners):

```
p = 0.72, avg_win = 0.8R, avg_loss = 1.4R
E = 0.72 × 0.8 − 0.28 × 1.4 = 0.576 − 0.392 = +0.184R
profit factor = 0.576 / 0.392 = 1.47
break_even p  = 1 / 1.571 = 63.6%  -> only 8.4 points of margin; fragile
```

Note how the second has a much higher win rate and a *lower* expectancy. Win rate alone is not a measure of
quality.

## 3. Expectancy vs R:R

For a fixed target R:R, the break-even win rate is `1/(1+R)`. Costs raise it:

```
required_p = (1 + cost_R) / (1 + R)      approximately, for a cost paid on every trade
```

Example: R = 1.5, cost 0.25R → required p ≈ 1.25/2.5 = 50% instead of 40%. That is a 10-point swing from costs
alone — often the difference between a viable and a non-viable strategy.

## 4. Beyond expectancy: the numbers that decide survival

| Metric | Definition | Why it matters |
|--------|-----------|----------------|
| Max drawdown | Deepest peak-to-trough | Determines whether you can stay in the game |
| Max consecutive losses | Longest losing streak | Determines required psychological + capital buffer |
| Ulcer index | `sqrt(mean(drawdown²))` | Penalises deep AND long drawdowns |
| Recovery factor | net profit / max drawdown | Return per unit of pain |
| Sharpe ratio | `mean(returns)/std(returns) × sqrt(periods)` | Risk-adjusted return, assumes normality |
| Sortino ratio | Same but with downside deviation | Better for skewed returns |
| Calmar ratio | annual return / max drawdown | Drawdown-focused |
| Max adverse excursion | Worst unrealised loss per trade | Shows how much heat positions take |

Sharpe and Sortino are **estimates from a sample** with large uncertainty (see
`statistics-basics.md`). A Sharpe of 1.5 on 60 trades is not meaningfully different from 0.5.

## 5. The distribution matters more than the average

Two strategies with the same expectancy can have completely different experiences:

```
Strategy A: 38% wins of 2.6R, losses of 1.0R   -> smooth-ish
Strategy B: 38% wins of 2.6R, losses of 1.0R but 5% of losses are 4R+
```

Strategy B has higher variance and a much deeper drawdown for the same mean. Always report the **worst 5% of
outcomes** and the maximum drawdown, not just expectancy.

## 6. How to compute expectancy correctly

1. Use **R multiples**, not currency (position size varies).
2. Include **all** costs: commission, taxes, slippage.
3. Include **all** trades, including scratches (R ≈ 0) — excluding them inflates the win rate.
4. Use **out-of-sample** trades for the reported number.
5. Report the **confidence interval** around the mean R (`mean ± 1.96 × SD/sqrt(n)`).

## 7. Beginner summary (Hinglish)

**Expectancy** = ek trade se average kitne R milte hain.

```
E = (win rate × average win) − (loss rate × average loss)
```

**Example:** 38% jeet, average win 2.6R, average loss 1R → E = +0.37R per trade. Yeh positive hai — matlab
long run mein fayda.

**Win rate akela bekaar hai:** 72% win rate wale system ki expectancy 18% win rate wale se kam ho sakti hai, agar
uske losses bade hain.

**Costs dekho:** agar har trade par 0.25R cost hai, to 1.5R target par break-even win rate 40% se 50% ho jata hai.

**Sabse zaroori:** expectancy ke saath **max drawdown** aur **max consecutive losses** bhi dekho. Sirf average
dekhne se account blow ho sakta hai.

## 8. Exercise

Take 20 completed trades (real log or a rule-generated set). Compute win rate, average win in R, average loss in R,
expectancy, profit factor, and max consecutive losses. Then subtract a 0.2R cost per trade and recompute
expectancy. Write down whether the edge survived.

---
*See also: [`statistics-basics.md`](statistics-basics.md) · [`monte-carlo.md`](monte-carlo.md) ·
[`../../integrations/python/trading_intel/metrics.py`](../../integrations/python/trading_intel/metrics.py)*
