# Workflow — News and Market Research

**Precondition:** a working web search/fetch tool, or a configured data provider. If neither exists, skip to the
"no research" output at the end — do not simulate research.

## Step 1 — Capability gate
```
web_search : yes / no
web_fetch  : yes / no
provider   : configured / not configured
```
If `web_search: no` and no provider → emit the standard paragraph and stop.

## Step 2 — Define the question precisely
Bad: "what's the news?"
Good: "Is there any scheduled or unscheduled event between now and <horizon> that would make a technical plan on
<instrument> unreliable?"

## Step 3 — Source prioritisation

| Priority | Source type | Examples |
|----------|-------------|----------|
| 1 | Exchange / regulatory | NSE, BSE, SEBI, SEC, company filings |
| 2 | Company IR | Earnings releases, investor presentations |
| 3 | Official macro | RBI, MoSPI, Fed, BLS |
| 4 | Licensed data / wires | Paid providers, major financial press |
| 5 | Aggregators / forums | Discovery only — never sole support |

## Step 4 — Per-item extraction

For every item you intend to use, capture all seven fields:

```
headline      : as published (do not dramatise)
publisher     : + tier (A/B/C/D)
published_at  : ISO timestamp + timezone
event_time    : when the thing happened (may differ)
url_or_tool   : traceable reference
relevance     : direct / sector / macro / none
impact        : direction + magnitude class, with a one-clause justification
```

## Step 5 — Freshness classification

| Class | Condition | Use |
|-------|-----------|-----|
| LIVE | ≤60 s | Any |
| RECENT | ≤15 min | Any (note delay) |
| DELAYED | 15 min – 1 session | Label; no "current price" claims |
| STALE | >1 session | Methodology only |
| HISTORICAL | >1 week | Education only |

## Step 6 — Cross-check material claims
Two independent sources, or explicitly mark the claim unverified. If sources conflict → report both, unresolved.

## Step 7 — Priced-in test
If the news is >1 session old and the instrument has already moved, the market has voted. Note that. Do not
present stale news as a catalyst.

## Step 8 — Red flags
- Headline only, body inaccessible
- Single source for a material claim
- "Reportedly" / anonymous sourcing
- Recycled article with an old event date
- Paywalled content you could not read (do not summarise it)
- Numbers without units or as-of dates

## Step 9 — Output block

```
NEWS AND MARKET CONTEXT
Index context    : NIFTY 50 -0.4% today; BANK NIFTY -0.9% (source, time)
Sector           : <sector> -1.1% — underperforming the index (source, time)
Instrument news  : <headline> (publisher, published 2026-11-13 18:40 IST) — relevance: direct
                   likely impact: negative for near-term estimates (guidance cut)
Scheduled events : Q2 results 2026-11-18 (exchange filing, 2026-11-04)
Global           : US 10Y +4bp; DXY flat (source, time)
Already priced in: the guidance cut was published yesterday and the stock fell 3.2% on the day —
                   the market has already reacted
Conflicts        : none found / <describe>
```

## No-research output (when tools are unavailable)

> **Web research unavailable in this environment.** No news, flows, sector or macro context was retrieved. The
> analysis is technical and structural only. Event risk — results, policy decisions, expiry — is unquantified and
> must be checked independently before acting on any scenario.

That paragraph is mandatory when browsing is unavailable. Never substitute recollection.
