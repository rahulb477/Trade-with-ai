# Market Intelligence — Sector Rotation and Relative Strength

## 1. Purpose
Answer: "is this instrument's sector helping or hurting it, and is capital rotating into or out of it?"

## 2. Relative strength calculation

Raw returns are misleading across instruments with different volatility. Use **risk-adjusted** relative strength:

```
RS_raw      = price_sector / price_benchmark
RS_momentum = ROC(sector, n) - ROC(benchmark, n)        n = 21, 63, 126 trading days
RS_adj      = ROC(sector, n) / (ATR%(sector) × sqrt(n)) - same for benchmark
```

`RS_raw` is a ratio line: rising = sector outperforming. `RS_momentum` is the excess return. Either is defensible;
state which you used and the lookback.

## 3. Sector rotation procedure

```
1. List the sector indices relevant to the market (India: NIFTY IT, AUTO, PHARMA, FMCG, METAL,
   PSU BANK, REALTY, ENERGY, MEDIA, FIN SERVICES).
2. Compute returns over 1M, 3M, 6M.
3. Rank sectors in each period.
4. Compute the change in rank (3M rank vs 1M rank) — improving vs decaying.
5. Compare the top sector's relative strength line against its own 50-day MA.
6. Relate to the regime: early cycle favours cyclicals/financials; late cycle favours defensives.
```

## 4. Interpreting a stock against its sector

| Stock | Sector | Reading |
|-------|--------|---------|
| Outperforming | Outperforming | Genuine leadership; strongest case |
| Outperforming | Underperforming | Stock-specific strength; fragile if the sector keeps lagging |
| Underperforming | Outperforming | Stock-specific weakness; the sector is not the problem |
| Underperforming | Underperforming | Avoid; two headwinds |

## 5. Reporting template

```
Sector context
  Sector index        : NIFTY BANK
  1M / 3M / 6M return : +2.1% / +6.4% / +11.2%
  Benchmark (NIFTY 50): +0.8% / +4.1% / +8.9%
  Relative strength   : outperforming on all three horizons; RS ratio above its 50-day MA
  Rank change (3M->1M): 4th -> 2nd (improving)
  Reading             : the sector is a tailwind. A long setup here has sector support; a short
                        would fight both the stock's sector and the index.
  Caveat              : rotation measures are regime-dependent; a single period's ranking is not a trend
```

## 6. Failure modes

| Failure | Guard |
|---------|-------|
| Comparing raw returns across different-volatility sectors | Use risk-adjusted measures |
| Using one lookback | Report 1M/3M/6M |
| Claiming rotation from one period | Rotation needs persistence |
| Ignoring index-level context | Sector strength can be index beta |
| Fabricating sector returns | Needs a data source; otherwise omit |
