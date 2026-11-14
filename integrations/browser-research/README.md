# Browser Research Integration

How an agent with web access should gather context — and what it must do without it.

**This directory contains a specification, not a scraper.** The repository ships no network code: browsing depends on
the host agent's tools, and any scraper would need to respect terms we cannot assume.

## 1. Capability gate

```
if no browsing tool -> emit the standard "web research unavailable" paragraph
                       (workflows/news-research.md §7) and continue technically
if browsing exists -> follow the extraction protocol below
```

## 2. The research sequence (maximum 8 retrievals)

| Step | Target | Purpose |
|------|--------|---------|
| 1 | Exchange announcement page for the instrument | primary-source events |
| 2 | Corporate actions (split/bonus/dividend) | price-series continuity |
| 3 | The instrument's own recent news | direct catalysts |
| 4 | The sector index performance | relative context |
| 5 | The benchmark index level and trend | market context |
| 6 | Event calendar for the horizon | the risk gate |
| 7 | Macro items only if directly relevant | rates, currency, commodity input |
| 8 | A cross-check for the single most material claim | verification |

The 8-retrieval budget exists because research expands to fill the time available, and depth in step 1–3 is worth
more than breadth in step 8.

## 3. Extraction protocol (per page)

```
1. Identify the publisher and the publication timestamp. No timestamp -> do not cite.
2. Extract the 7 fields: headline, publisher, tier, published, event_time, url, relevance.
3. Note whether it is a press release, a reprint, an opinion piece, or reported fact.
4. Extract figures with their as-of dates and units. "₹1,240 crore, Q2FY27, consolidated" — not "good revenue".
5. Check whether a later item corrects or supersedes this one.
```

## 4. Forbidden

| Forbidden | Why |
|-----------|-----|
| Summarising an article you could not open (paywall) | Fabrication |
| Inventing a URL or a headline | Fabrication |
| Presenting an old article as current | Misleading |
| Using social media sentiment as evidence | Not verifiable |
| Bypassing authentication or paywalls | Against terms and illegal in many places |
| Bulk-scraping a site | Resource abuse |
| Collecting personal data | Out of scope |

## 5. India-specific primary sources

| Need | Where |
|------|-------|
| Company results and announcements | Exchange announcement pages (NSE / BSE) |
| Corporate actions | Exchange corporate-actions page |
| Regulatory circulars | SEBI |
| Policy rate and MPC | RBI |
| CPI, IIP, GDP | MoSPI / RBI publications |
| FII/DII flows | Exchange end-of-day data |

Verify the specific page each time; do not assume a URL pattern still works.

## 6. The "unavailable" paragraph

When browsing is not possible, the report must include, near the top of the context section:

> **Web research unavailable.** I cannot retrieve current news, announcements, flows, or events for this
> instrument. The analysis below is technical only. Event risk is unknown, which caps position size and is stated
> in the limitations section. I have not invented any news or context to fill this gap.

Anything shorter tends to be omitted; anything longer tends to become an excuse.

## 7. Verification

Every material claim: two independent sources, or a Tier-A source, or it is excluded from the verdict. Full
procedure in `data-sources/source-validation.md`.
