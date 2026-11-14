# Source Validation

A source is usable only if it satisfies **all four** tests: attributable, dated, tiered, and corroborated where
material.

## 1. The four tests

### 1.1 Attributable
- Named publisher, not "reports say".
- A URL or a specific tool call that produced it.
- If the path from claim to source cannot be shown, the claim is not usable.

### 1.2 Dated
- A publication timestamp with a timezone.
- An event timestamp if different.
- A retrieval timestamp.

Undated sources are excluded from reports. This is a hard rule: undated data cannot be freshness-classified, and
unstale-able data is unusable.

### 1.3 Tiered
Tier A (primary/regulatory) → D (aggregator). A material claim requires Tier A–C, or two independent sources.

### 1.4 Corroborated (material claims only)
| Claim type | Corroboration needed |
|-----------|---------------------|
| Price/volume | One licensed provider is usually sufficient; two if they disagree |
| Corporate action | Exchange notice (Tier A) alone is sufficient |
| Earnings figures | Filing, or two Tier-B/C sources |
| Macro release | Official agency (Tier A) alone is sufficient |
| "Company plans to..." | Two independent sources, or mark unverified |
| Market rumour | Never usable as evidence |

## 2. Reliability scoring

```python
def source_reliability(tier, dated, attributable, corroborated):
    score = {A: 4, B: 3, C: 2, D: 1}[tier]
    if not attributable: return 0        # unusable
    if not dated:        return 0        # unusable
    if not corroborated: score -= 1      # material claims only
    return max(score, 0)
```

| Score | Use |
|-------|-----|
| 4 | Authoritative; cite directly |
| 3 | Cite; note the licence |
| 2 | Cite; cross-check material claims |
| 1 | Discovery only |
| 0 | Do not use |

## 3. Red-flag scanner (run on every source you intend to cite)

- [ ] Headline only, body inaccessible
- [ ] No publication timestamp
- [ ] "Reportedly" / anonymous sourcing for a material fact
- [ ] Recycled article with a changed date
- [ ] Press release reprinted as independent news
- [ ] Paywalled content you could not read
- [ ] Numbers with no units or as-of date
- [ ] Contradicts a Tier-A source
- [ ] Hostile to correction (no clear publisher)
- [ ] AI-generated content farm (generic phrasing, no byline, no named sources)

Two or more red flags → do not cite.

## 4. Cross-check procedure for material claims

```
1. Identify the exact material fact (number, date, event).
2. Search for a second, independent source (not a reprint of the first).
3. If both agree -> cite both (or the stronger tier).
4. If they disagree -> check for definitional differences (standalone vs consolidated, adjusted vs raw,
   spot vs futures, different as-of times).
5. If still unresolved -> report both, mark UNRESOLVED, exclude from the verdict.
```

## 5. The self-audit question

> "If I were asked to prove this claim, could I produce a link, a timestamp and a publisher in under ten seconds?"

If not, delete the claim from the report. This single question prevents the majority of fabrications.

## 6. Examples

| Claim | Verdict |
|-------|---------|
| "NSE closed at 24,180 on 2026-11-14" | Usable if from a provider or exchange page with a timestamp |
| "The stock is up because of strong results" | Not usable — causal claim without a source |
| "Analysts expect 12% growth" | Usable only with the provider, date and sample |
| "FIIs bought ₹2,400 cr yesterday" | Usable only with the exchange figure and the date |
| "Sentiment is turning positive on social media" | Not usable as evidence |
| "The RBI meets next week" | Not usable unless the RBI's published calendar confirms the date |
