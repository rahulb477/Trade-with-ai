# Monte Carlo and Scenario Simulation

## 1. What it is
Repeatedly resampling from a strategy's (or a distribution's) outcomes to build a distribution of *paths* rather
than a single backtest result. It answers: "given this set of trade outcomes, how bad could the ride have been?"

## 2. The core method (bootstrap)

```
1. Collect the R-multiples of all completed trades in the historical set.
2. For k = 1..N simulations:
     - draw n trades at random WITH replacement from that set
     - compound the equity: equity *= (1 + R_i × risk_fraction)
     - record final equity, max drawdown, longest losing streak
3. Summarise the distributions: median, 5th percentile, 95th percentile, worst case.
```

**Critical assumption:** the historical set is representative of the future. Bootstrap resampling cannot create
outcomes that were not in the sample. If your sample had no 5R loss, the simulation will not produce one — and
real life will.

## 3. Worked example (illustrative, deterministic seed)

```
Trades (R): +2.1, -1.0, +1.8, -1.0, +0.6, -1.0, +3.2, -1.0, +1.4, -1.0, +2.6, -1.0, +0.9, -1.0, +1.1
risk_fraction = 1% of equity, 500 trades simulated, 10 000 paths
Results (illustrative shape, not a claim about any real strategy):
  median final equity  : +62% of starting equity
  5th percentile       : -8%
  95th percentile      : +190%
  median max drawdown  : -12%
  95th-worst drawdown  : -26%
  worst path           : -41%
```

The point of the numbers is the *shape*: a positive median with a meaningful left tail. A single backtest hides
that tail entirely.

## 4. Why it matters even for a profitable strategy

Two strategies can have identical expectancy and completely different tails. Monte Carlo exposes:

1. **Drawdown distribution** — what you should expect to tolerate, not the best case.
2. **Risk of ruin** — probability of hitting a specified loss threshold.
3. **Path dependence** — the same trade set in a different order gives a different experience.
4. **Sizing sensitivity** — rerun at 2× size and watch the ruin probability explode.

## 5. Risk-of-ruin estimation

```
ruin_probability ≈ fraction of paths where equity ever falls below the ruin threshold
```

Run at multiple risk fractions (0.5%, 1%, 2%, 5%) and plot ruin probability vs size. The result is usually a
sharp cliff — the practical answer to "how much should I risk per trade".

## 6. Scenario analysis (deterministic, not random)

Complementary to Monte Carlo: hand-build specific scenarios.

```
Scenario 1 (base)     : continuing range, 1 ATR daily
Scenario 2 (bull)     : breakout holds, 2 ATR daily
Scenario 3 (bear)     : support fails, gap down 3%
Scenario 4 (event)    : results gap -12%
For each: P&L, max loss, whether invalidation triggers, what you do
```

Deterministic scenarios are often more useful for a *single trade decision* than a Monte Carlo, which is a
portfolio-level tool.

## 7. Limitations

| Limitation | Consequence |
|------------|-------------|
| Sample-bound | Cannot produce unseen outcomes |
| Assumes exchangeability | Real markets have regimes; resampled trades ignore clustering |
| Ignores serial correlation | Autocorrelated results are over-optimistic |
| Ignores costs dynamics | Slippage worsens in stress |
| Ignores correlation across positions | Single-strategy simulation misses portfolio effects |
| Seed dependence | Use a fixed seed and report it for reproducibility |

## 8. Beginner summary (Hinglish)

**Monte Carlo kya hai?** Aapke trades ke results ko baar baar **random order** mein mix karke 10,000 baar equity
curve banate hain.

**Kya milta hai:**
- Median result
- **5th percentile** (bura case)
- **Worst drawdown distribution** — asli kaam ki cheez

**Kyun zaroori?** Ek backtest sirf **ek** path dikhata hai. Wahi trades alag order mein aane par brutal drawdown de
sakte hain.

**Sabse badi limitation:** jo sample mein nahi hai, woh simulation mein nahi aayega. Agar sample mein 5R loss nahi
tha, simulation bhi nahi dikhayega — par real life mein aa sakta hai.

**Aur:** different risk % par run karo (0.5%, 1%, 2%, 5%). Ruin probability ka cliff saaf dikh jayega.

## 9. Exercise

Take 20 R-multiples. Write a short script (or use `integrations/python/trading_intel/simulate.py`) to bootstrap
10,000 paths of 100 trades each at 1% risk. Report the median, 5th percentile, and worst max drawdown. Then rerun at
3% risk. Write down what changed and why.

---
*See also: [`expectancy.md`](expectancy.md) · [`../../integrations/python/trading_intel/simulate.py`](../../integrations/python/trading_intel/simulate.py) ·
[`../risk-management/drawdown-and-survival.md`](../risk-management/drawdown-and-survival.md)*
