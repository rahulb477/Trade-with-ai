# Markets — Index

**Trading rules are not interchangeable across markets.** Applying Indian session conventions to a crypto chart,
or US tick sizes to an Indian stock, produces wrong analysis and wrong risk calculations.

| Market | Directory | Key files |
|--------|-----------|-----------|
| India (NSE/BSE) | [`india/`](india/) | `README.md`, `sessions-and-holidays.md`, `derivatives.md`, `indices.md` |
| United States | [`united-states/`](united-states/) | `README.md` |
| Forex | [`forex/`](forex/) | `README.md` |
| Commodities | [`commodities/`](commodities/README.md) | `README.md` |
| Crypto | [`crypto/`](crypto/README.md) | `README.md` |

## What must be checked per market

| Attribute | Why it matters |
|-----------|----------------|
| Trading session and timezone | Candle boundaries, gap behaviour, volume profile of the day |
| Weekly schedule (which days) | Crypto 24/7, forex 24/5, equities session-based |
| Holidays | A "missing" candle may be a holiday, not a data error |
| Tick size | Minimum stop granularity and cost per tick |
| Lot size | Notional and risk per lot |
| Circuit/limit rules | Whether you can exit at all |
| Settlement | Whether you can hold to expiry/delivery |
| Corporate-action conventions | Chart adjustment |
| Data-source requirements | What is even obtainable |

## Rule

When a user asks about "the market" without naming one, infer from context (an Indian user's "the market" is NSE),
**state the assumption**, and apply only that market's rules.

When you analyse an instrument you cannot place in a market with confidence, ask. A wrong session assumption
invalidates candle boundaries, gap analysis, and volatility comparisons simultaneously.
