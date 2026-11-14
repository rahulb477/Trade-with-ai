# Providers — Interface and Catalogue

## 1. The interface (implement this, nothing else)

```python
class Provider(Protocol):
    name: str
    requires_credentials: bool

    def fetch_ohlcv(self, symbol: str, timeframe: str, start, end) -> list[Bar]:
        """Return normalised bars. Raise ProviderError on failure. Never return partial data silently."""

    def fetch_quote(self, symbol: str) -> Quote:
        """Return a last-trade snapshot with a timestamp."""

    def fetch_option_chain(self, symbol: str, expiry) -> Chain:
        """Raise NotSupported if unavailable."""

    def health(self) -> dict:
        """Return {status, latency_ms, last_success, notes}."""
```

Reference stub: `integrations/python/trading_intel/providers/base.py`.
Examples (documentation only, not live implementations): `providers_examples.py`.

## 2. Normalisation rules

Every provider adapter must return data in this shape, or be rejected:

```python
Bar = {
    "timestamp": datetime,      # tz-aware, UTC or IST — must be explicit
    "open": float, "high": float, "low": float, "close": float,
    "volume": float | None,     # None if the provider lacks it — never 0 as a placeholder
    "symbol": str,
    "timeframe": str,
    "source": str,
    "adjusted": bool,           # is the series adjusted for splits/dividends?
}
```

Normalisation must:
1. Convert timestamps to a single timezone with an offset.
2. Validate `high ≥ max(open, close)` and `low ≤ min(open, close)`; reject the payload otherwise.
3. Sort by timestamp, de-duplicate, and report gaps.
4. Record `source` and `adjusted` on every bar.

## 3. Catalogue of categories (not endorsements)

| Category | Examples of the type of provider | What they typically offer |
|----------|--------------------------------|---------------------------|
| Exchange official | NSE, BSE, SEC EDGAR | Filings, corporate actions, EOD data, circulars |
| Licensed market data | Major vendors and broker APIs | Real-time/15-min delayed OHLCV, OI, chains |
| Historical EOD | Data vendors, open datasets | Daily OHLCV, sometimes adjusted |
| News wires | Established financial press APIs | Headlines, timestamps, full text |
| Economic calendars | Statistical agencies, calendar providers | Scheduled releases with times |
| Fundamentals | Filings aggregators, IR pages | Financial statements, shareholding |

**No specific provider is recommended here.** Terms, licensing, and availability change constantly, and this
repository does not have current knowledge of them. Evaluate providers yourself against: coverage, latency,
adjustment quality, licensing, rate limits, and cost.

## 4. Adapter requirements

- Read credentials from **environment variables only** (`data-sources/api-configuration.md`).
- Respect rate limits; implement exponential backoff with a cap of 2 retries.
- Cache responses with a documented TTL (`data-sources/market-data.md` §cache).
- Log every request's outcome (not the credentials).
- Raise a typed error; never return partially parsed data.
- Never attempt to bypass authentication, paywalls, or terms.

## 5. Degradation ladder

```
1. Provider configured and healthy   -> full research mode
2. Provider configured but failing   -> retry twice, then fall back to cached EOD, marked STALE
3. No provider, web available        -> web research mode (news/context only, no computed indicators)
4. No provider, no web               -> offline knowledge mode (education, chart reading from image)
```

Each mode must be declared in report section 10.

## 6. What this repository will not ship

- Any hardcoded API key, token, or credential.
- Scrapers that violate terms of service.
- A bundled market dataset (licensing and size).
- Claims about a provider's current pricing, limits, or uptime.
