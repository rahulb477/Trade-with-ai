# Verdict Rules — Quick Signal Output Engine

This file defines the **quick-mode closed verdict set** introduced by the upgrade and its relationship to the existing V1–V3 vocabulary. Nothing here removes or weakens prior gates — it narrows the user-facing surface to the three answers that matter for the compact report.

---

## 1. Quick-mode verdicts (3, and only 3)

| Verdict | When | What it means |
|---------|------|---------------|
| **WAIT** | Breakout/breakdown confirmation pending, retest incomplete, indicators conflict, choppy range, or data insufficient for an entry. | No hypothetical setup meets its documented conditions yet. The report names the outstanding confirmation. |
| **NO TRADE** | Setup invalidated, risk/reward unsuitable under the documented strategy, market conditions hostile, or required evidence unavailable. | A positive decision *not* to participate — even if the missing trigger later appears, the location or arithmetic rejects it. |
| **PAPER-TRADING SETUP READY** | Required conditions satisfied, entry clearly defined, stop loss justified, targets supported, data quality acceptable, relevant risks disclosed. | A hypothetical educational setup meets its documented conditions. It is not a recommendation to place a real-money trade. |

These strings appear verbatim in `integrations/python/trading_intel/quick_signal.py`:

* `VERDICT_WAIT = "WAIT"`
* `VERDICT_NO_TRADE = "NO TRADE"`
* `VERDICT_READY = "PAPER-TRADING SETUP READY"`

The textual quick report renders them as `VERDICT: WAIT` / `VERDICT: NO TRADE` / `VERDICT: PAPER-TRADING SETUP READY`.

---

## 2. Relationship to the V1–V3 vocabulary

The repository's original decision vocabulary (SKILL.md §6, `core/decision-engine.md`) remains normative for the full report path:

| Legacy verdict | Meaning |
|----------------|---------|
| `BULLISH SCENARIO` | Evidence-backed long condition currently valid or reachable with a defined trigger, R:R ≥ 1.5 to T1. |
| `BEARISH SCENARIO` | Mirror. |
| `WAIT — NO CONFIRMED SETUP` | Data sufficient but no scenario clears the checklist. |
| `NO-TRADE` | Hostile conditions: event risk, illiquidity, untenable regime. |
| `INSUFFICIENT DATA — NO VALID SETUP` | Essential inputs missing. |

Quick-mode mapping:

* `BULLISH SCENARIO` / `BEARISH SCENARIO` with all gates passed  →  `PAPER-TRADING SETUP READY` (direction lives in the ENTRY block, not the verdict word).
* `WAIT — NO CONFIRMED SETUP`  →  `WAIT`.
* `NO-TRADE` / `INSUFFICIENT DATA`  →  `NO TRADE` when the setup is actively rejected; otherwise `WAIT` when the data is merely pending.

Preserving both vocabularies is intentional: `tests/docs/test_repository.py` asserts the five legacy strings remain in `SKILL.md` and the template. The quick engine is additive, not a replacement.

---

## 3. WAIT gate ladder (adapted for the compact path)

The compact decision in `quick_signal.decide_verdict` applies these gates in order. The first gate that triggers determines the verdict:

```
G1  Data integrity      — quality < 5 or instrument missing  -> WAIT (cap)
G2  Event risk          — binary event inside horizon         -> NO TRADE
G3  Structure           — no defensible invalidation          -> WAIT
G4  Location            — R:R to T1 < 1.5                     -> NO TRADE
G5  Trigger             — no close-through / retest hold      -> WAIT
G6  Alignment           — HTF contradicts without explanation -> WAIT
G7  Trap risk           — unrefuted trap evidence             -> WAIT (or NO TRADE if invalidated)
G8  Verdict             — direction chosen; otherwise WAIT
```

Additional quick-mode gates:

* **Stale data** (`data_fresh == False`) downgrades `READY` to `WAIT`.
* **Quality score < 5** caps `READY` at `WAIT` and the report notes the score.
* **Choppy / compressed volatility**  →  `WAIT` (or `NO TRADE` if R:R also fails).

---

## 4. WAIT KAB TAK? — the most important block

`WAIT` is never bare. The `WAIT UNTIL:` line must name the condition:

* Wait for the 5m candle to close above resistance.
* Wait for a confirmed breakdown below support.
* Wait for a successful retest.
* Wait for volume confirmation.
* Wait for higher-timeframe alignment.
* Wait until volatility becomes suitable.
* Wait until the upcoming major event risk has passed.

If the condition cannot be determined:

```
WAIT UNTIL: Clear confirmation appears.
```

The WAIT engine (`workflows/wait-confirmation.md`) is responsible for this sentence. It never promises a future time, never invents a countdown, and distinguishes:

* A candle currently forming vs a candle that has closed.
* A confirmed breakout vs an unconfirmed breakout vs a failed breakout.

Each state maps to a distinct template in `quick_signal.WAIT_TEMPLATES`.

---

## 5. PAPER-TRADING SETUP READY — qualification

`PAPER-TRADING SETUP READY` is emitted only when **all** hold:

* [ ] Entry conditions clearly defined (zone + trigger + timeframe + status).
* [ ] Stop loss justified (structural price ± ATR buffer, not a round number).
* [ ] Targets supported (each maps to structure or volatility; directionally consistent).
* [ ] Data quality acceptable (quality ≥ 5, data fresh or delay disclosed).
* [ ] Relevant risks disclosed (costs, slippage, event risk, gap risk).
* [ ] R:R ≥ 1.5 to T1 after costs.

Any failure  →  `WAIT` or `NO TRADE`, with the failing gate named. See `workflows/entry-validation.md` and `workflows/target-calculation.md`.

---

## 6. Examples

### WAIT (unconfirmed breakdown)

```
BTCUSD | Bitstamp | 5m
VERDICT: WAIT
WAIT UNTIL:
5-minute candle closes below the identified support and the breakdown is confirmed by the required evidence.
ENTRY: 67,300–67,400  (PENDING)
STOP LOSS: 67,800
TAKE PROFIT 1: 66,900–67,000
REASON: Support break hua hai, lekin volume confirmation abhi nahi mili.
```

### NO TRADE (poor R:R)

```
BTCUSD | Bitstamp | 5m
VERDICT: NO TRADE
WAIT UNTIL: Clear confirmation appears.
ENTRY: NOT AVAILABLE — INSUFFICIENT DATA
STOP LOSS: 67,800
TAKE PROFIT 1: NOT AVAILABLE
REASON: Risk/reward to T1 is 0.87 — below the 1.5 minimum. No valid setup.
```

### PAPER-TRADING SETUP READY

```
BTCUSD | Bitstamp | 5m
VERDICT: PAPER-TRADING SETUP READY
WAIT UNTIL: No further wait — entry trigger is satisfied (close above 67,400).
ENTRY: 67,400 (CONDITIONALLY VALID)
STOP LOSS: 67,800
TAKE PROFIT 1: 66,900 (R 1.8) …
REASON: Conditions met for a hypothetical educational setup.
```

---

## 7. Honesty invariant

* No fabricated price, entry, stop, target, probability or countdown.
* No unsupported percentage win rate.
* The difference between a forming candle and a closed candle is never blurred.
* If the screenshot is blurry/unreadable, the verdict is `WAIT` or `NO TRADE` with the limitation stated.

*Enforced by: `quick_signal.assert_no_fabrication`, `validate_no_probability`, and the `NOT AVAILABLE — INSUFFICIENT DATA` sentinel, which is the only permitted substitute for a missing number.*

---

*See also: `core/decision-engine.md` · `core/quick-output-engine.md` · `workflows/wait-confirmation.md`.*
