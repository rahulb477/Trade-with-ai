# Python Integration

A dependency-free library (standard library only, Python 3.9+) implementing the repository's calculation
requirements.

```bash
# no installation, no dependencies
export PYTHONPATH="$PWD/integrations/python:$PYTHONPATH"
python3 -c "from trading_intel import indicators; print(indicators.rsi([1,2,3], 2))"
```

## Modules

| Module | Contents |
|--------|----------|
| `trading_intel/indicators.py` | SMA, EMA, RSI, MACD, ATR, ADX, Bollinger, Supertrend, Stochastic RSI, OBV, VWAP, Ichimoku, CCI, ROC, MFI, pivots, Fibonacci, volume profile |
| `trading_intel/patterns.py` | 23 candle detectors, each returning status codes and a rule audit |
| `trading_intel/risk.py` | R-multiples, reward:risk, break-even win rate, expectancy, drawdown, ruin arithmetic, `TradePlan` |
| `trading_intel/sizing.py` | Position sizing (floor to lot), ATR-based stops, stop-width checks, partial exits |
| `trading_intel/metrics.py` | Trade-log metrics in R with confidence intervals |
| `trading_intel/stats.py` | Descriptive statistics, correlation, Sharpe/Sortino, Wilson interval, multiple-testing correction |
| `trading_intel/simulate.py` | Seeded Monte Carlo, bootstrap CIs, synthetic OHLCV |
| `trading_intel/backtest.py` | Event-driven backtester plus walk-forward splits |
| `trading_intel/timeframes.py` | Aggregation, ratio quality, alignment scoring |
| `trading_intel/validation.py` | OHLC validation, jumps/gaps, freshness, chart quality scoring |
| `trading_intel/observation.py` | The `ChartObservation` contract and its gates |
| `trading_intel/providers/` | Provider protocol, in-memory reference provider, environment detection |

## Design rules

1. **`None` means "not computable".** Never zero, never a guess. Every consumer must handle it.
2. **No I/O in the calculation modules.** Files, network, and clock access are the caller's responsibility
   (`validation.freshness` takes the timestamps as arguments rather than reading the clock).
3. **Seeded randomness.** Every stochastic function takes a `seed` and returns it in the result.
4. **No silent repairs.** Validation reports; it does not fix.
5. **No configuration required.** Nothing in the library reads an API key.

## Quick tour

```python
from trading_intel import indicators, patterns, risk, sizing, metrics, backtest, simulate

data = simulate.synthetic_ohlcv(bars=300, seed=1)      # synthetic, not market data
atr  = indicators.atr(data["high"], data["low"], data["close"])
rsi  = indicators.rsi(data["close"])

plan = risk.TradePlan("long", entry=100, stop=95, targets=[107, 112, 120])
print(plan.summary())              # {'R_T1': 1.4, 'R_T2': 2.4, 'R_T3': 4.0, ...}
print(plan.validation_warnings())  # ['R:R to T1 is 1.40, below the 1.5 minimum']

print(sizing.size_position(500_000, 100, 95).as_dict())
# {'units': 750, 'risk_amount': 3750.0, 'notional': 75000.0, ...}

hits = patterns.detect_all(data["open"], data["high"], data["low"], data["close"], data["volume"])
print({k: len(v) for k, v in hits.items() if len(v)})

result = backtest.simulate(data, backtest.simple_ema_cross_strategy(20, 50))
print(result["summary"]["n"], result["final_equity"])
print(result["caveats"])           # what the backtest cannot tell you
```

## Known limitations

- **No live data.** The library computes; it does not fetch.
- **Backtester is a research tool**, not an execution simulator: no queue position, no partial fills, no
  market-impact model.
- **Intrabar order is unknowable** from OHLC; the engine assumes the stop is hit first (pessimistic, and stated).
- **No options pricing model** (Black-Scholes/Greeks) is implemented; the options engine documents rather than
  computes.
- **Synthetic data is synthetic.** `simulate.synthetic_ohlcv` exists for tests; it is labelled everywhere it appears.

## Running the tests

```bash
cd <repo root>
python3 -m unittest discover -s tests -t . -v
```
