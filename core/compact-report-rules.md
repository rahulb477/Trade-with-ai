# Compact Report Rules

> The textual output should follow a compact, structured presentation inspired by the Chartick.AI reference — dark-background compatible, instrument/timeframe at the top, prominent verdict, entry in blue, stop in red, TPs in green, risk/reward neutral, one short reason, timestamp and disclaimer. No branding, logo or proprietary assets are copied.

---

## 1. Goals

* **5-second comprehension.** The user understands WAIT/ENTRY/SL/T1/T2/T3 without reading a paragraph.
* **No hallucination.** A missing value renders as `NOT AVAILABLE` — never a guess.
* **Printable on dark and light.** The text template works on both; the HTML variant uses dark colours.

---

## 2. Mandatory fields (every quick report)

| Field | Source | Rendering |
|-------|--------|-----------|
| Instrument \| Exchange \| Timeframe | Observed header | `BTCUSD \| Bitstamp \| 5m` |
| Verdict | `quick_signal.decide_verdict` | `VERDICT: WAIT` etc. |
| WAIT UNTIL | `quick_signal.evaluate_wait` | One sentence, no countdown |
| Entry | `quick_signal.evaluate_entry` | Zone `67,300–67,400` or `NOT AVAILABLE — INSUFFICIENT DATA` |
| Stop loss | `quick_signal.calculate_stop_loss` | Single price or sentinel |
| TP1 / TP2 / TP3 | `quick_signal.calculate_targets` | Price / range / sentinel per target |
| Risk / reward | `quick_signal.calculate_risk_reward` | `T1 1.8 (net 1.6) \| T2 2.9 …` or sentinel |
| Reason | English one-liner | Plain English |
| Hinglish | `quick_signal.hinglish_reason` | One Hinglish line |
| Data timestamp + freshness | `validation.freshness` | `Data: ... \| Freshness: ...` |
| Disclaimer | Fixed string | Educational disclaimer |

No other sections appear in quick mode. Full indicator tables, complete candlestick encyclopedia explanations, long news summaries, detailed market structure, long fundamental analysis, historical backtesting tables and full research methodology are suppressed — they live in `templates/analysis-report.md` (full mode).

---

## 3. Length

Default textual quick report is **8–12 short lines** when rendered with `render_compact_text_minimal`. The fuller `render_quick_text` variant is ~25 lines but still avoids paragraphs — it uses labelled blocks with blank separators. Either satisfies the "8–12 short lines" principle in spirit: a compact report must not exceed ~30 logical lines and must not contain long paragraphs.

Enforced by `tests/quick_output/test_output_length.py`.

---

## 4. Price formatting

* `format_price` in `quick_signal.py`: comma separators, decimals inferred from magnitude.
* Zone rendered with an en-dash: `67,300–67,400`.
* `NOT AVAILABLE — INSUFFICIENT DATA` is the only allowed substitute for a missing price.
* `NOT AVAILABLE` (without the suffix) is the only allowed substitute for a missing secondary target (TP2/TP3 when insufficient structure).
* No arbitrary round numbers for TPs — every target maps to structure or volatility, per `workflows/target-calculation.md`.

---

## 5. WAIT / ENTRY / SL / TP rules

* **WAIT:** never a bare word — always `WAIT UNTIL: <condition>` where condition is one of the templates in `WAIT_TEMPLATES` or the fallback. See `workflows/wait-confirmation.md`.
* **ENTRY:** label shows zone + status hint (`PENDING`, `CONDITIONALLY VALID`, `INVALIDATED`). A pending setup is never described as active. Candlestick pattern alone is never sufficient — the engine requires a close-through plus volume/retest/HTF/freshness per `workflows/entry-validation.md`.
* **STOP LOSS:** single price. Basis recorded in `StopLossResult.basis` (invalidation + ATR buffer). If not justified, sentinel. See `workflows/target-calculation.md` §stop annex.
* **TAKE PROFIT:** three hypotheses. T1 first technical objective, T2 next S/R/liquidity, T3 extended. Each directionally consistent, each with separate R:R, each cost-aware. If three defensible targets cannot be built, verified targets are shown and the remainder is `NOT AVAILABLE`. Never manufactured to fill the display.

---

## 6. Risk / reward

* Computed via `risk.reward_risk` (gross) and adjusted for `cost_bps` (net).
* Display: `T1 1.80 (net 1.60) | T2 2.90` etc.
* Gross R:R below 1.5 to T1  →  verdict becomes `NO TRADE` (see `core/verdict-rules.md`).
* Always after-cost R:R is shown when a cost estimate exists; the gross value is kept for audit.

---

## 7. Hinglish

* One short Hinglish line per report, after the English reason.
* Simple English-tinged Hinglish (see `knowledge/education/hinglish-explanations.md`): short sentences, trading terms stay in English, numbers identical, invalidation named, no "pakka" / "sure shot" / unsourced win rate.
* Templates: `HINGLISH_TEMPLATES` in `quick_signal.py`.

Examples:

* "Price resistance ke neeche hai. Breakout confirmation ka wait karo."
* "Support break hua hai, lekin volume confirmation abhi nahi mili."
* "Price sideways hai. Abhi clear setup nahi hai."
* "Retest complete nahi hua. Entry condition pending hai."

Checked by `tests/quick_output/test_quick_mode.py`.

---

## 8. Visual HTML (Chartick-inspired, not a clone)

`quick_signal.render_quick_html` emits self-contained dark-background HTML:

* Dark background compatibility (`#0f1115` / `#1a1d24`).
* Instrument/timeframe at the top.
* Prominent verdict pill (yellow WAIT, red NO TRADE, green READY).
* Entry blue (`#3b82f6`), stop red (`#ef4444`), TP green (`#22c55e`), R:R neutral.
* One short reason + Hinglish + timestamps + disclaimer.

No Chartick.AI branding, logo or source is used. Only the compact information hierarchy is shared.

---

## 9. Anti-patterns

| Anti-pattern | Correct |
|--------------|---------|
| Fabricating a third target to fill three rows | `TP3: NOT AVAILABLE` |
| Writing a bare `WAIT` with no condition | `WAIT UNTIL: Clear confirmation appears.` at minimum |
| Presenting a pending entry as active | Status `PENDING`, confirmation sentence states "only after …" |
| Using round numbers because they look tidy | Targets traced to structure / ATR / Fib, per target-calculation workflow |
| Promising a breakout "in 3 candles" | Never invent a countdown — describe the condition |
| Blurring forming vs closed vs confirmed | Use the exact candle-state term from `workflows/wait-confirmation.md` |

---

*See also: `templates/quick-signal-report.md` · `workflows/quick-screenshot-analysis.md` · `integrations/python/trading_intel/quick_signal.py`.*
