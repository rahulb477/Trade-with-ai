# Engine — Data Integrity

**Purpose:** make sure nothing enters an analysis that is stale, malformed, misattributed, or invented.

## 1. Validation checks

| Check | Method | On failure |
|-------|--------|-----------|
| **Completeness** | Every required field present | Reject the record; do not partially parse |
| **Type/format** | OHLCV numeric, timestamps ISO with offset | Reject |
| **Sanity** | `high ≥ max(open, close)`, `low ≤ min(open, close)`, `high ≥ low`, volumes ≥ 0 | Reject or repair with a logged flag |
| **Monotonicity** | Timestamps strictly increasing, no duplicates | De-duplicate; log |
| **Gap detection** | Expected bar count vs actual (session calendar) | Flag; distinguish holiday from missing data |
| **Extreme detection** | Return > k × ATR (default k=8) in one bar | Suspicious; cross-check for split/bad tick |
| **Zero-volume bars** | Volume == 0 on a trading bar | Flag as illiquid/halted |
| **Adjustment check** | Unexplained ~50% or ~2× jump | Check corporate actions before use |
| **Staleness** | Data age vs market session | Classify LIVE/RECENT/DELAYED/STALE/HISTORICAL |
| **Provenance** | Source, retrieval time, licence | Record every field's origin |

## 2. Staleness policy

| Class | Equity condition | Permitted use |
|-------|------------------|---------------|
| LIVE | ≤60 s | Any |
| RECENT | ≤15 min | Any; note delay |
| DELAYED | 15 min – 1 session | Levels/indicators usable if labelled; no "current price" claims |
| STALE | >1 session | Methodology only |
| HISTORICAL | >1 week | Education/backtest only |

Non-equity markets differ: crypto is 24/7, forex 24/5. Use the calendar in `markets/`.

## 3. Provenance recording

Every numeric field carries:
```
value, source, retrieval_timestamp, event_timestamp, freshness_class, reliability_tier
```

A field without provenance may not influence the verdict (`core/evidence-engine.md`).

## 4. Malformed input handling

```
1. Reject the payload — do not partially parse.
2. Log the reason and the payload hash.
3. Fall back to the previous valid snapshot if one exists, marked as such.
4. If no fallback: mark the data unavailable and downgrade the analysis.
5. Never interpolate or "repair" silently.
```

## 5. The fabrication guards

| Prohibited | Guard |
|-----------|-------|
| Inventing an indicator value | Only printed values or computed from real data |
| Inventing a price level | Only axis-interpolated (marked approximate) or provided |
| Inventing a news headline | Only retrieved, with source and timestamp |
| Inventing volume | Only from a volume panel or provider |
| Inventing a timeframe | Only observed or user-stated |
| Inventing a statistic | Only measured with n and period |

## 6. Freshness propagation to the verdict

```
if any KEY input is STALE:
    verdict is capped at WAIT for any intraday claim
if the instrument identity is UNVERIFIED:
    verdict is INSUFFICIENT DATA
if the price scale is unavailable:
    no numeric levels may be reported
```

## 7. Audit log format

```
{timestamp, check, target, result, detail, action_taken}
```

Example:
```
2026-11-14T15:31:02+05:30 | sanity | bar 2026-11-14T15:15 | FAIL high(1201.2) < close(1203.8) | REJECTED payload
2026-11-14T15:31:05+05:30 | staleness | provider:xyz | DELAYED (18 min) | FLAGGED in report section 10
2026-11-14T15:31:06+05:30 | gap     | 2026-10-20 | missing bar | CHECKED: exchange holiday -> OK
```

## 8. Failure modes

| Failure | Guard |
|---------|-------|
| Silently parsing a partial payload | Reject whole |
| Treating a holiday as missing data | Calendar check |
| Using a split as a crash | Corporate-action check |
| Presenting delayed data as live | Freshness class in the report |
| Repairing bad data without disclosure | Log every repair |
| Trusting one source for a material claim | Cross-check or mark unverified |

## 9. Why this engine is load-bearing

Every other engine's output inherits this engine's failures. A wrong instrument, a stale price, or a split artefact
invalidates the structure map, the patterns, the levels, the R:R, and the verdict — simultaneously and silently.
This is the cheapest place to prevent the most expensive errors.
