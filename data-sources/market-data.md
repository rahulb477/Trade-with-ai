# Market Data — Requirements, Validation, Caching

## 1. Minimum viable dataset for each analysis type

| Analysis | Required |
|----------|----------|
| Candle pattern detection | OHLC for the analysis timeframe + the previous ~50 bars |
| Indicator computation | OHLC + volume + at least `3 × period` bars |
| Multi-timeframe | OHLC for each timeframe used |
| Volume analysis | Volume per bar |
| VWAP | Intraday OHLCV with a session boundary |
| Volatility (ATR/sizing) | OHLC, ≥20 bars |
| Options context | Option chain with OI, volume, prices, expiry |
| Order flow | Tick or bid/ask data (rarely available) |

## 2. Adjustment requirements

| Requirement | Reason |
|-------------|--------|
| Split/bonus adjusted | Otherwise historic levels are wrong |
| Dividend adjusted (for total-return work) | Otherwise ex-date drops look like breaks |
| Continuous futures back-adjusted | Otherwise roll gaps are artefacts |
| Point-in-time index membership | Otherwise survivorship bias |

Every bar carries an `adjusted: bool` flag. If `False`, the analysis must not draw levels across a corporate action.

## 3. Staleness and session awareness

```
expected_bar_time(timeframe, session_calendar) -> the most recent bar that should exist
age = now - last_bar.timestamp
```

| Age | Class | Use |
|-----|-------|-----|
| ≤60 s | LIVE | Any |
| ≤15 min | RECENT | Any; note delay |
| ≤1 session | DELAYED | Label; no "current price" claims |
| ≤1 week | STALE | Methodology only |
| >1 week | HISTORICAL | Education only |

Holidays must be accounted for: a missing bar on a holiday is not missing data. Use the market's calendar
(`markets/`).

## 4. Validation checklist

- [ ] `high ≥ max(open, close)`, `low ≤ min(open, close)`, `high ≥ low`
- [ ] Volume ≥ 0 (and `None`, not 0, when genuinely unavailable)
- [ ] Timestamps strictly increasing, no duplicates
- [ ] No unexplained jumps > 8 × ATR (investigate splits/bad ticks)
- [ ] Bar count matches the session calendar
- [ ] Timezone explicit on every timestamp
- [ ] `source` and `adjusted` recorded
- [ ] Coverage: enough history for the longest indicator period used

## 5. Caching

| Layer | TTL | Notes |
|-------|-----|-------|
| Intraday quotes | 5–15 s | Never serve a stale quote as live |
| Intraday bars | 1 bar interval | A 5m bar is final once the 5m closes |
| Daily bars | Until the next session close | Re-fetch after the close |
| Option chain | 30–60 s | Chains change fast |
| Filings/news | 15 min – 1 day | Depends on the source |
| Economic calendar | 1 day | Rarely changes intraday |

Cache keys must include: symbol, timeframe, adjustment flag, and the source. A cache hit must still carry its
original timestamp so staleness can be computed.

## 6. Missing data handling

```
1. Detect: bar count vs calendar, or a None field.
2. Classify: holiday / outage / genuinely not traded / unsupported timeframe.
3. Do NOT interpolate. Do NOT forward-fill prices.
4. Mark every affected indicator as unavailable.
5. State it in report section 10.
```

Forward filling is the most dangerous habit in market-data handling: it manufactures zero-volatility bars and
silently corrupts ATR, Bollinger width, and every volatility-based measure.

## 7. Licensing and terms

Data is licensed, not owned. Requirements:
- Respect the licence's redistribution terms (usually: no redistribution).
- Do not store licensed data in a public repository (see `.gitignore`).
- Do not scrape against a site's terms.
- Cite the provider in every report that uses its data.

## 8. What never goes in this repository

- Raw licensed datasets.
- API keys or tokens.
- Credentials in URLs, logs, or error messages.
