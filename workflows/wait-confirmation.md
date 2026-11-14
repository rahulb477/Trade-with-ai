# Workflow — WAIT Confirmation (WAIT Engine)

The most important workflow in the Quick Signal Output Engine. The user wants one thing first: **WAIT KAB TAK?**

Do not answer with a bare `WAIT`. Name the condition that would allow a hypothetical setup to be considered. Never invent a time.

---

## 1. WAIT KAB TAK?

Every `WAIT` verdict must carry a `WAIT UNTIL:` sentence drawn from the templates in `integrations/python/trading_intel/quick_signal.py::WAIT_TEMPLATES`. Call `quick_signal.evaluate_wait` to produce it.

Available conditions:

* Wait for the 5m candle to close above resistance.
* Wait for a confirmed breakdown below support.
* Wait for a successful retest.
* Wait for volume confirmation.
* Wait for higher-timeframe alignment.
* Wait until volatility becomes suitable.
* Wait until the upcoming major event risk has passed, if relevant.

If the required condition cannot be determined:

```
WAIT UNTIL: Clear confirmation appears.
```

---

## 2. Candle-state discipline

The WAIT sentence must use the correct state term. The distinction is normative:

| State | Meaning | WAIT implication |
|-------|---------|------------------|
| **Candle currently forming** | The rightmost candle is still printing; close not known. | Wait for it to **close**. |
| **Candle that has closed** | Close is known, but breakout test incomplete. | Wait for **confirmation** (volume + hold). |
| **Confirmed breakout** | Close beyond level + volume + hold/retest satisfied. | No wait — eligible for `READY` if other gates pass. |
| **Unconfirmed breakout** | Price beyond level but missing close, volume or hold. | Wait for close + volume + hold. |
| **Failed breakout** | Close back inside the range; breakout fully retraced. | Wait for a **fresh trigger**; prior level is now a trap candidate. |

Inputs to `evaluate_wait`:

* `timeframe` — e.g. `"5m"`.
* `candle_state` — one of `forming`, `closed`, `confirmed_breakout`, `unconfirmed_breakout`, `failed_breakout`, `confirmed_breakdown`, `unconfirmed_breakdown`, `failed_breakdown`, `unknown`.
* `level` — the S/R price that was tested (for the sentence).
* `volume_confirmed` — `True`/`False`/`None`.
* `retest_status` — `"pending"` / `"confirmed"` / `"failed"` / `None`.
* `htf_conflict`, `htf`, `ltf` — timeframe alignment flags.
* `volatility_state` — `"choppy"` / `"compressed"` / `None`.
* `event_risk` — string like `"RBI MPC 2026-11-18"` or `None` (highest priority — overrides technical waits).
* `choppy` — boolean.

The function never invents a countdown or a number of candles without evidence.

---

## 3. Examples

| Situation | Correct WAIT UNTIL |
|-----------|--------------------|
| 5m candle still forming under resistance at 67,800 | `Wait for the 5m candle to close above the identified resistance (67,800) and the breakout is confirmed by the required evidence.` |
| Price closed above resistance but volume flat and no retest | `Wait for a confirmed breakout above 67,800 — close + volume + hold required.` |
| 5m close below support 66,900 without volume | `5-minute candle closes below the identified support (66,900) and the breakdown is confirmed by the required evidence.` |
| Two candles closed back inside after a breakout | `Wait — the breakout failed. Price closed back inside the range. Await a fresh trigger.` |
| RSI bullish on 5m but daily downtrend, no HTF alignment | `Wait for higher-timeframe alignment — daily conflicts with 5m.` |
| Earnings tomorrow | `Wait until the upcoming major event risk has passed (Q2 results 2026-11-18).` |
| No clear condition | `Clear confirmation appears.` |

---

## 4. Rules

* Never promise a breakout "in 10 minutes" or "in 3 candles" without evidence.
* Never average a forming candle into a confirmed one.
* A wick that pierced a level is not a close-through.
* Log-scale vs linear axis confusion must be disclosed — interpolation on a log axis without conversion is wrong.
* Cropped price axis → levels unavailable → WAIT with the limitation stated.

---

## 5. How it reaches the user

* Text quick report: `WAIT UNTIL:` on its own labelled line, then the sentence.
* HTML quick report: `Wait until` row in the compact card, muted label, full sentence on the right.

Both are produced by `render_quick_text` / `render_quick_html` reading `WaitResult.condition`.

---

*See also: `core/quick-output-engine.md` · `workflows/entry-validation.md` · `integrations/python/trading_intel/quick_signal.py`.*
