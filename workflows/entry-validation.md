# Workflow — Entry Validation (ENTRY Engine)

Validates and describes a hypothetical entry. Called by `workflows/quick-screenshot-analysis.md` stage 13 and implemented in `integrations/python/trading_intel/quick_signal.py::evaluate_entry`.

---

## 1. What an entry needs

For every hypothetical setup, define:

* Entry price or entry zone.
* Entry direction (`long` / `short`).
* Confirmation condition (the trigger that must still occur).
* Required timeframe.
* Whether the setup is confirmed or pending.

No entry is described without all five.

---

## 2. Possible states

| Status | Meaning | Shown as |
|--------|---------|----------|
| **PENDING** | Trigger not yet met; price has not satisfied the required evidence. | `ENTRY STATUS: PENDING` |
| **CONDITIONALLY VALID** | Trigger met plus at least 3 confirming evidence classes; final validation still required (freshness / event risk / trap audit). | `ENTRY STATUS: CONDITIONALLY VALID` |
| **INVALIDATED** | Price closed beyond the invalidation level; prior breakout/breakdown failed; or the thesis has been disproved. | `ENTRY STATUS: INVALIDATED` |

A pending setup is never described as an active signal.

Implementation: `EntryResult.status` and `EntryResult.status_line()`.

---

## 3. Confirmation hierarchy

A candlestick pattern alone is **insufficient** confirmation. Evidence is counted from:

* Candle **close** beyond the level (required).
* Support / resistance test (≥2 touches).
* Volume confirmation (expansion vs 20-bar average).
* Retest hold (price returns to the broken level and closes back in the breakout direction).
* Market structure (HH/HL vs LH/LL sequence, trend phase).
* Higher-timeframe context (alignment, not conflict).
* Data freshness (LIVE/RECENT vs DELAYED/STALE).

`evaluate_entry` counts independent evidence classes that are present:

```python
evidence_count = sum([
    has_close_confirmation,
    has_volume,
    has_retest,
    htf_aligned,
])
```

* `evidence_count >= 3` + close → `CONDITIONALLY VALID`.
* `evidence_count >= 1` + close → `PENDING` (needs more confirmation).
* No close → `PENDING` regardless; message: "pattern alone is not enough".
* Closed beyond invalidation → `INVALIDATED`.

The `confirmation` string explains the outstanding check in plain language.

---

## 4. Examples

| Situation | Status | Confirmation text |
|-----------|--------|--------------------|
| Hammer printed but candle still forming, no close above level | PENDING | `Entry pending — waiting for candle close confirmation beyond the level.` |
| Close above resistance + volume + retest done + HTF aligned | CONDITIONALLY VALID | `Entry conditionally valid — close + 3 confirmations present. Needs final validation.` |
| Close above resistance but volume missing, HTF conflicts | PENDING | `Entry pending — close-through seen but additional confirmation (volume/retest/HTF) still required.` |
| Prior breakout candle closed back inside, now below swing low | INVALIDATED | `Entry invalidated — prior breakout/breakdown failed.` |
| Data is stale (2 sessions old) on intraday timeframe | PENDING | `Data is stale — cannot confirm entry.` |

---

## 5. Rendering

* Quick report `ENTRY:` line shows the zone (`67,300–67,400`) or single price, then:
  * If `PENDING`: `Only after the specified confirmation. (PENDING)` (or the full confirmation sentence in the detailed quick text variant).
  * If `CONDITIONALLY VALID`: `(CONDITIONALLY VALID — awaiting final validation)`.
  * If `INVALIDATED`: `(INVALIDATED)` and verdict becomes `NO TRADE`.
* If no price can be justified at all → `NOT AVAILABLE — INSUFFICIENT DATA`.

---

## 6. Anti-patterns

* Calling a `DEVELOPING` pattern `CONFIRMED`.
* Naming an entry at the exact middle of a range ("poor location" — see `core/decision-engine.md` G4).
* Placing an entry with no structural level (invented round number).
* Promising "this will trigger in 5 minutes".

---

*See also: `workflows/wait-confirmation.md` · `workflows/target-calculation.md` · `core/decision-engine.md`.*
