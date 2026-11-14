# Engine — Market Intelligence

**Purpose:** supply *cited* context without fabricating it. Everything here is conditional on data access.

**Inputs:** instrument, horizon, capability block, optional provider credentials.
**Outputs:** index/sector state, instrument news, flows, macro events, global sentiment — each with a timestamp,
tier and freshness class.

## Modules

| Module | Function |
|--------|----------|
| `README.md` (this file) | Context gathering protocol |
| [`market-regime.md`](market-regime.md) | Regime classification (trend/range/vol) |
| [`sector-analysis.md`](sector-analysis.md) | Sector rotation and relative strength |

## Protocol

```
1. Capability gate: no web, no news. Emit the standard "unavailable" paragraph and stop.
2. Index context: NIFTY 50 / BANK NIFTY / Sensex (India) or the relevant benchmark.
3. Sector: the instrument's sector index vs the benchmark, over stated lookbacks.
4. Instrument news: cited, timestamped, tiered.
5. Flows: FII/DII (India) or equivalent — end-of-day only, with dates.
6. Events: results, policy, expiry — inside the horizon.
7. Global: US yields, DXY, crude, global indices — directional only.
8. Cross-check material claims; report conflicts.
```

## What "cited" means here

Every item carries: `headline`, `publisher`, `tier (A–D)`, `published_at`, `event_time`, `url_or_tool`,
`relevance`, `impact`. See `core/evidence-engine.md` §5.

Items missing any of those fields do not enter the report.

## Freshness propagation

| Data age | Effect |
|----------|--------|
| ≤15 min | Usable as current |
| 15 min – 1 session | Label DELAYED; no "current price" claims |
| > 1 session | STALE; methodology only |
| > 1 week | HISTORICAL; education only |

A `STALE` context may not support an intraday verdict (`core/decision-engine.md`).

## Failure modes

| Failure | Response |
|---------|----------|
| No browsing | Standard "unavailable" paragraph; analysis becomes technical-only |
| Provider timeout after 2 retries | Mark source unavailable; continue at lower confidence |
| Conflicting sources | Report both, unresolved; lower confidence one rung |
| Undated source | Do not cite; find a dated one or omit |
| Paywalled | Do not summarise; state that it could not be read |

## Non-negotiable

Never state a news item, flow figure, macro release, or index level that was not retrieved. The most damaging
failure mode in this entire repository is a fabricated headline.
