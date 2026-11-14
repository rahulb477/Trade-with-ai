# Quick Signal Output Engine

> **Principle:** *Perform deep research internally. Deliver simple answers externally.*

The AI may perform extensive internal chart analysis, quantitative research, news research and market verification. The **default user-facing response is extremely short** — 8 to 12 short lines — so the user understands within five seconds:

* WAIT KAB TAK?
* ENTRY KAB?
* STOP LOSS KAHAN?
* TAKE PROFIT 1 / 2 / 3?

---

## 1. Purpose

The Quick Signal Output Engine is a **presentation layer** added on top of the existing V1–V3 pipeline (`core/analysis-engine.md`, 16 stages). It does not replace any analysis. It selects the shortest defensible summary and renders it using the mandatory format in `templates/quick-signal-report.md`.

```
V1-V3 pipeline (16 stages, 20 internal checks)
        │
        ▼
Quick Signal Output Engine  (this file)
        │
        ├─► QUICK MODE  (default)  -> compact report
        └─► FULL MODE   (explicit) -> full V1-V3 report
```

All V1–V3 engines remain intact: candlesticks, indicators, chart patterns, smart-money concepts, market structure, news research, quantitative intelligence, order flow, options intelligence, risk management, backtesting, prediction tracking, self-evaluation, strategy discovery, multi-market architecture, data integrity, beginner education. See `core/verdict-rules.md` and `core/compact-report-rules.md` for the normative constraints.

---

## 2. Mandatory default output format

Every quick-mode response follows this structure (values are illustrative only; never copy them as real levels):

```
BTCUSD | Bitstamp | 5m

VERDICT: WAIT

WAIT UNTIL:
5-minute candle closes below the identified support and the breakdown is confirmed by the required evidence.

ENTRY:
67,300–67,400
Only after the specified confirmation.

STOP LOSS:
67,800

TAKE PROFIT 1:
66,900–67,000

TAKE PROFIT 2:
66,500

TAKE PROFIT 3:
66,200

RISK / REWARD:
Calculated from the verified entry, stop loss, and each target.

REASON:
Price is consolidating below resistance. Wait for confirmation before considering the hypothetical setup.
```

Implementation rules (§3 of the upgrade prompt):

* Short — clear labels — readable price formatting.
* No long paragraphs, no unnecessary technical terminology.
* No repetition of the complete analysis.
* Never invent a price, entry, stop, target or probability.
* Never generate a setup when evidence is insufficient.
* Around 8–12 short lines.

The renderer is `integrations/python/trading_intel/quick_signal.py::render_quick_text` and the even shorter `render_compact_text_minimal`. The visual variant is `render_quick_html` (dark background, Chartick-inspired hierarchy, no branding copy).

---

## 3. Strict output rules

1. Be short.
2. Use clear labels.
3. Use readable price formatting (`format_price` in `quick_signal.py`).
4. Avoid long paragraphs.
5. Avoid unnecessary technical terminology.
6. Avoid repeating the complete analysis.
7. Avoid unnecessary explanations of every indicator.
8. Never invent a price / entry / stop / target / probability.
9. Never generate a setup when evidence is insufficient.

Checked by `tests/quick_output/test_output_length.py`, `test_missing_data.py`, and the fabrication guards in `quick_signal.assert_no_fabrication` / `validate_no_probability`.

---

## 4. Internal research pipeline (20 steps)

Before producing the short output the agent follows the existing pipeline, logically:

1. Read and understand the screenshot.
2. Identify instrument and exchange.
3. Verify timeframe.
4. Extract available price information.
5. Assess screenshot quality.
6. Analyze candlestick formations.
7. Analyze market structure.
8. Calculate indicators when sufficient OHLCV exists.
9. Analyze volume.
10. Detect breakout and breakdown conditions.
11. Evaluate bull traps and bear traps.
12. Compare available timeframes.
13. Research relevant current news when browsing is available.
14. Verify current market data when an authorized provider is available.
15. Check data freshness.
16. Calculate hypothetical entry, stop loss and targets.
17. Evaluate risk/reward.
18. Identify contradictory evidence.
19. Select the final verdict.
20. Generate the compact output.

The AI must not claim to have completed a step whose tools or data were unavailable. That claim is tracked in the `QuickSignalOutput.provenance` ledger and surfaced in `data_freshness` / quality-score gating.

---

## 5. Image and screenshot handling

Improvements to the existing workflow (`core/chart-recognition.md`):

* Recognize header, symbol, exchange, timeframe, price scale, candle colours, indicator panels, volume panel, S/R annotations, chart drawings.
* Never confuse chart image coordinates with actual market prices.
* Never invent price levels from a blank, blurry or unreadable chart.
* If the screenshot is incomplete, communicate the limitation.
* If the screenshot says BTCUSD but the market data provider returns another instrument, do not combine the datasets.

Quality gating: the same 0–10 rubric in `validation.score_chart_quality` applies. A score below 5 caps the quick verdict at `WAIT` and the output notes the quality.

---

## 6. Integration points

| Area | File |
|------|------|
| Verdict mapping | `core/verdict-rules.md` |
| Compact formatting | `core/compact-report-rules.md` |
| WAIT conditions | `workflows/wait-confirmation.md` |
| ENTRY conditions | `workflows/entry-validation.md` |
| Target calculation | `workflows/target-calculation.md` |
| Screenshot path | `workflows/quick-screenshot-analysis.md` |
| Report shell | `templates/quick-signal-report.md` |
| Visual HTML | `integrations/python/trading_intel/quick_signal.py::render_quick_html` |
| Logic | `integrations/python/trading_intel/quick_signal.py` |

---

## 7. Mode switching

Default is **QUICK MODE**. Full analysis is activated only when the user explicitly requests:

* "full analysis", "detailed analysis", "explain this chart", "why this entry?", "show indicators", "show news", "show complete research", "/full".

Detection lives in `quick_signal.detect_mode`. The quick output carries a flag `full_mode_requested`; when true the agent should delegate to the full `templates/analysis-report.md` path instead of the compact renderer. Tests: `tests/quick_output/test_full_mode.py` and `test_quick_mode.py`.

---

## 8. Safety and honesty

* Educational, research and hypothetical paper-trading only.
* No real-money execution, no broker connection, no promised profits, no certainty about future moves.
* Clearly distinguishes screenshot observations, verified market data, calculated values, estimates and unknown information.
* Prefers `WAIT` or `NO TRADE` over an unsupported setup.
* Never invents countdowns or future times for breakouts.

---

*See also: `core/verdict-rules.md` · `core/compact-report-rules.md` · `workflows/quick-screenshot-analysis.md` · `integrations/python/trading_intel/quick_signal.py`.*
