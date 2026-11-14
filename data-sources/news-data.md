# News Data — Sources, Fields, and Verification

## 1. Required fields per item

```
headline        : as published
publisher       : name
tier            : A (primary/regulatory) | B (licensed/professional) | C (established media) | D (aggregator)
published_at    : ISO 8601 with timezone
event_time      : when the thing happened (may differ from publication)
url_or_tool     : traceable reference
retrieved_at    : ISO 8601
relevance       : direct | sector | macro | none
impact          : direction + magnitude class, with a one-clause justification
already_priced  : yes/no/unknown, with reasoning
```

Any item missing `published_at` or `url_or_tool` is not usable and must be omitted.

## 2. Source tiers

| Tier | Definition | Permitted use |
|------|-----------|---------------|
| **A** | Exchange notices, SEBI/SEC filings, central-bank releases, official statistics | Authoritative; cite directly |
| **B** | Licensed data providers, professional wires | Cite with licence note |
| **C** | Established financial media with correction policies | Cite; cross-check material claims |
| **D** | Blogs, aggregators, social posts | Discovery only; never sole support |

## 3. Verification protocol

```
1. Is the publication timestamp present and plausible?
2. Is the event date consistent with the publication date?
3. Does a second, independent source report the same material fact?
4. Is the claim attributed to a named source, or "reportedly"?
5. Is the article a reprint of a press release (i.e. a Tier-A claim dressed as news)?
6. Has it been superseded/corrected by a later article?
```

Material claim with only one source → mark `UNVERIFIED` and exclude it from the verdict.

## 4. Detecting outdated information

| Symptom | Action |
|---------|--------|
| Publication date is old relative to the question | Mark STALE; do not present as current |
| Article body refers to a previous quarter/year | Check for an update |
| Headline recycled across outlets with a newer date | Find the original timestamp |
| Price referenced in the article is far from the current price | It is historical context, not current news |

## 5. Conflict handling

Report both, state "unresolved", and lower confidence one rung. Never average.

Example:

```
Conflict: two sources report different Q2 revenue figures (₹1,240 cr vs ₹1,262 cr).
Resolution attempt: one is standalone, one consolidated — the difference is consistent with that,
but neither article states it explicitly.
Action: report both, mark as unresolved, and do not use the figure in any calculation.
```

## 6. India-specific official sources

| Need | Source type |
|------|-------------|
| Company results, announcements | Exchange announcement pages (NSE/BSE) |
| Corporate actions | Exchange corporate-action pages |
| Regulatory circulars | SEBI |
| Policy rates, MPC decisions | RBI |
| Macro data (CPI, IIP, GDP) | MoSPI and RBI publications |
| FII/DII flows | Exchange end-of-day publications |

**Never assert a figure or date from memory.** Verify and timestamp.

## 7. International official sources

| Need | Source type |
|------|-------------|
| US filings | SEC EDGAR |
| US economic data | BLS, BEA, Fed (FRED) |
| EU data | Eurostat, ECB |
| Global indices | Exchange sites and licensed vendors |

## 8. What must never happen

- A fabricated headline.
- A real headline attributed to the wrong publisher.
- A publication date presented as an event date.
- A paywalled article summarised as if read.
- A single-source material claim influencing the verdict.
- Social-media sentiment presented as evidence.
