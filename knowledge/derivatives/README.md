# Derivatives — Index

Futures and options intelligence: what the data means, what it cannot tell you, and how to read it without
over-claiming.

| File | Topic |
|------|-------|
| [`open-interest.md`](open-interest.md) | OI, change in OI, the four-quadrant reading, rollovers |
| [`options-metrics.md`](options-metrics.md) | PCR, max pain, IV, IV rank, Greeks (delta/gamma/theta/vega) |
| [`options-chain.md`](options-chain.md) | Reading an option chain, and its traps |
| [`futures-basics.md`](futures-basics.md) | Basis, roll, expiry effects, contract specs |

Engine: `engines/options-intelligence/`.

## The three rules of derivatives analysis

1. **Never infer OI direction from total OI alone.** Open interest rises on both new longs and new shorts. You
   need price behaviour *and* OI change together, and even then the inference is ambiguous.
2. **Never treat max pain as a prediction.** It is a computed value from current OI; markets routinely ignore it.
3. **Never quote an IV number you cannot see.** IV is not derivable from a price chart.

## Data requirements

| Metric | Requires |
|--------|----------|
| OI / ΔOI | Exchange derivative data (NSE/BSE publish end-of-day and intraday snapshots) |
| PCR | Full option chain OI by strike |
| Max pain | Full option chain OI by strike |
| IV, IV rank | Option prices + a pricing model, or the exchange's published IV |
| Greeks | Option prices, strikes, time to expiry, rate assumptions |
| Volume delta / CVD | Tick or bid/ask data |

If the data is unavailable, say so. Do not estimate OI from a price chart.
