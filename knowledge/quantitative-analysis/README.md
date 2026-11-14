# Quantitative Analysis — Index

Statistics, probability and simulation for research decisions — with the emphasis on **what a number does not
prove**.

| File | Topic |
|------|-------|
| [`statistics-basics.md`](statistics-basics.md) | Distributions, sampling error, confidence intervals, significance |
| [`expectancy.md`](expectancy.md) | Expectancy, profit factor, payoff, R-multiples, sizing interaction |
| [`correlation-and-regression.md`](correlation-and-regression.md) | Correlation, its instability, and regression pitfalls |
| [`monte-carlo.md`](monte-carlo.md) | Path simulation, drawdown distributions, ruin estimates |
| [`overfitting-and-bias.md`](overfitting-and-bias.md) | Overfitting, look-ahead, survivorship, multiple testing |

Implementation: `integrations/python/trading_intel/stats.py`, `simulate.py`, `metrics.py`.

## The four questions every quantitative claim must answer

1. **What is the sample size?**
2. **What are the assumptions?**
3. **Was it out of sample?**
4. **Does it survive costs?**

A number without those four is decoration.
