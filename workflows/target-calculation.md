# Workflow — Target Calculation (STOP LOSS + TAKE PROFIT Engines)

Covers both `calculate_stop_loss` and `calculate_targets` in `integrations/python/trading_intel/quick_signal.py`.

---

## 1. Stop loss engine

### Principle

A stop is **technical invalidation** — the price that says "my thesis was wrong". It must be traceable to structure, not comfort.

### Inputs

* `direction` — `long` / `short`.
* `swing_level` — relevant swing high/low from the chart (observed).
* `atr` — Average True Range for the timeframe (computed if OHLCV available).
* `structural_price` — a level that invalidates the setup (e.g. swing low − buffer, pattern boundary).
* `atr_multiplier` — buffer fraction, default `0.3`.

### Derivation

| Input | Rule |
|-------|------|
| `structural_price` + `atr` | `long: structural − 0.3 ATR`, `short: structural + 0.3 ATR` — the preferred hybrid stop. |
| `structural_price` alone | Stop at structure (note: "no ATR buffer available"). |
| `swing_level` + `atr` | `swing ± 0.3 ATR`. |
| `swing_level` alone | Stop at the swing (weak — flag as such). |
| `atr` alone without structure | No justified stop → `NOT AVAILABLE — INSUFFICIENT DATA`. ATR alone is not a thesis. |
| Nothing | `NOT AVAILABLE — INSUFFICIENT DATA`. |

### Output

`StopLossResult` with `price` (float or `None`) and `basis` (human explanation). The quick report renders:

* If price exists: `67,800`
* Otherwise: `NOT AVAILABLE — INSUFFICIENT DATA`

Width check: `sizing.stop_width_check(entry, stop, atr)` warns if the stop is > 3 ATR away.

### Honesty

* Never place a stop at an exact obvious level — add the ATR buffer (documented in `core/risk-management.md`).
* If stop placement cannot be justified, return the sentinel — do not invent a round number.
* Gap risk note: a stop is not a guarantee. The report carries the educational disclaimer.

---

## 2. Take profit engine

### Principle

Three separate hypothetical targets, each independently justified:

* **TP1** — First relevant technical objective (nearest structure or 1–1.5 ATR).
* **TP2** — Next meaningful support/resistance or liquidity objective (second structure or 2–2.5 ATR).
* **TP3** — Extended objective supported by market structure and volatility (third structure or 3–3.5 ATR).

### Requirements

* Calculate all three targets when defensible.
* Show price ranges when appropriate (zone rather than a single level).
* Avoid arbitrary round numbers — every TP must map to structure (prior swing, measured move, Fib, volatility multiple) or the engine marks it `NOT AVAILABLE`.
* Check directional consistency: long targets > entry, short targets < entry.
* Calculate risk/reward separately per target.
* Account for estimated transaction costs and slippage when data available (`cost_bps`).
* Explain when a target is not supported.

### Derivation

`calculate_targets` filters `levels_for_targets` to directionally consistent levels, sorted by distance from entry:

```
structural = [lvl for lvl in levels if (long and lvl > entry) or (short and lvl < entry)]
structural.sort(reverse=(short))
```

Then, in priority:

* **TP1:** `structural[0]` if exists; else `entry ± 1.5 ATR` if ATR available. Basis recorded as `"prior swing / structure"` or `"1.5 ATR objective"`.
* **TP2:** `structural[1]` if exists and `len(structural) >= 2`; else `entry ± 2.0–2.5 ATR` depending on how many structural levels exist. Basis `"next S/R / liquidity"` or `"ATR extension"`.
* **TP3:** `structural[2]` if exists; else `entry ± 3.0–3.5 ATR` if sufficient distance from TP2 (≥ 0.8 ATR separation required to avoid near-duplicate targets). Otherwise `None` → `NOT AVAILABLE`.

All TP prices rounded to 2 decimals.

### Rendering

| Availability | Quick report |
|-------------|--------------|
| TP exists | `66,900–67,000` or `66,500` |
| Not enough structure | `NOT AVAILABLE` (distinct from the SL sentinel — the TP3 sentinel omits the suffix to match prompt §7 example `TP3: NOT AVAILABLE.`) |
| No entry to project from | All TPs `NOT AVAILABLE` |

Never manufacture TP3 just to fill the display — the tests assert that `TP3 == None` is permitted and honest.

### Risk / reward

`calculate_risk_reward` calls `risk.reward_risk(entry, stop, target, direction)` for each TP, then subtracts `cost_R = (cost_bps / 10_000 × entry) / |entry − stop|` when a cost estimate exists:

```
risk_per_unit = |entry − stop|
reward_i      = |target_i − entry|  (sign per direction)
R_i           = reward_i / risk_per_unit
cost_R        = cost_per_unit / risk_per_unit
net_R_i       = R_i − cost_R
```

Display: `T1 1.80 (net 1.60) | T2 2.90` etc. A `T1` net R:R below 1.5 escalates to `NO TRADE` per `core/verdict-rules.md` G4.

### Range variant

When a TP is better expressed as a zone (e.g. support cluster spans several ticks), the engine can store `tp1_range_low` / `tp1_range_high` instead of a single price. `TakeProfitResult.tp_display` renders `format_range(low, high)` in that case.

---

## 3. Examples

| Input | Output |
|-------|--------|
| Long entry 1,204, stop 1,186, levels [1,240, 1,275, 1,310], ATR 12 | TP1 1,240 (R 2.0), TP2 1,275 (R 3.9), TP3 1,310 (R 5.9) |
| Long entry 1,204, stop 1,186, no structural levels, ATR 12 | TP1 1,222 (R 1.0) — insufficient, would be NO TRADE; TP2 1,234 (R 1.7) etc. — but gate rejects if TP1 R < 1.5 |
| Short entry 67,400, stop 67,800, levels [66,900, 66,500, 66,200] | TP1 66,900 (R 1.25) — would be rejected; alternatively with entry 67,350 the Rs become defensible |
| Entry missing | All TPs `NOT AVAILABLE` |

---

## 4. Checks

* `calculate_targets` never returns a target that is on the wrong side of entry — filtered at source.
* Round-number test: a target that equals an exact `5,000` / `10,000` without structural basis is not defensible; the engine must trace it to structure or ATR, not a round number.
* `assert_no_fabrication` cross-checks that every price in the output was passed in as an allowed level.

---

*See also: `core/quick-output-engine.md` · `core/risk-management.md` · `workflows/entry-validation.md`.*
