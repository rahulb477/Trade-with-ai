# Risk Management — Index

The core arithmetic and rules live in [`../../core/risk-management.md`](../../core/risk-management.md). This
directory holds the practical sub-modules.

| File | Topic |
|------|-------|
| [`position-sizing.md`](position-sizing.md) | Fixed-fractional, ATR-based, Kelly-capped, unit accounting |
| [`stop-loss-design.md`](stop-loss-design.md) | Structural, volatility, time stops; widening traps |
| [`drawdown-and-survival.md`](drawdown-and-survival.md) | Drawdown math, recovery, circuit breakers |
| [`costs-and-slippage.md`](costs-and-slippage.md) | Cost modelling, participation limits, gap risk |

Implementation: `integrations/python/trading_intel/risk.py` and `sizing.py`.

## The five rules that matter most

1. **Size first, direction second.**
2. **No invalidation, no trade.**
3. **Risk per idea 0.25–1.0% of equity** (educational convention, not advice).
4. **Costs are part of the trade** — convert them to R before judging a setup.
5. **Define your maximum drawdown before you trade, not after.**
