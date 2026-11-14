# Quick Signal Report Template

> **Everything here is hypothetical and educational.** No order is placed. No money is at risk. The default output is compact — the full research remains available on explicit request (`/full`, `full analysis`, etc.). Copy the structure, fill only what is defensible, write `NOT AVAILABLE — INSUFFICIENT DATA` when no justified price exists, and `NOT AVAILABLE` for an unjustified secondary target. Never fabricate a price, entry, stop, target, probability or countdown.

---

```
{{INSTRUMENT}} | {{EXCHANGE}} | {{TIMEFRAME}}

VERDICT: {{VERDICT}}  — one of WAIT | NO TRADE | PAPER-TRADING SETUP READY

WAIT UNTIL:
{{WAIT_CONDITION_SENTENCE}}

ENTRY:
{{ENTRY_ZONE_OR_PRICE}} — only after the specified confirmation.
ENTRY STATUS: {{PENDING | CONDITIONALLY VALID | INVALIDATED}}

STOP LOSS:
{{STOP_PRICE_OR_SENTINEL}}  — {{STOP_BASIS}}

TAKE PROFIT 1:
{{TP1_PRICE_OR_RANGE_OR_SENTINEL}}  — {{TP1_BASIS}}

TAKE PROFIT 2:
{{TP2_PRICE_OR_RANGE_OR_SENTINEL}}  — {{TP2_BASIS}}

TAKE PROFIT 3:
{{TP3_PRICE_OR_RANGE_OR_SENTINEL}}  — {{TP3_BASIS}}

RISK / REWARD:
{{RR_T1}} | {{RR_T2}} | {{RR_T3}}  (net of estimated costs when available)

REASON:
{{ONE_SHORT_ENGLISH_SENTENCE}}

Hinglish: {{ONE_SHORT_HINGLISH_SENTENCE}}

Data: {{DATA_TIMESTAMP}} | Freshness: {{FRESHNESS}} | Analysis: {{ANALYSIS_TIMESTAMP}}
Educational paper-trading research only. Not investment advice. No real-money order was placed.
```

---

## Example (illustrative — not a current BTC level)

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
T1 1.80 | T2 2.90 | T3 4.20 — calculated from verified entry, stop and each target.

REASON:
Price is consolidating below resistance. Wait for confirmation before considering the hypothetical setup.

Hinglish: Price resistance ke neeche hai. Breakout confirmation ka wait karo.

Data: 2026-11-14T15:29:58+05:30 | Freshness: LIVE
Educational paper-trading research only. Not investment advice. No real-money order was placed.
```

The values above are examples, not current BTC market levels.

---

## Field rules

| Field | Rule |
|-------|------|
| `INSTRUMENT | EXCHANGE | TIMEFRAME` | Observed header; `UNKNOWN` if not visible. |
| `VERDICT` | One of the three quick-mode verdicts. |
| `WAIT UNTIL` | Sentence from `quick_signal.WAIT_TEMPLATES`; fallback `Clear confirmation appears.` Never a time. |
| `ENTRY` | Zone or price (`format_price` / `format_range`). Pending setups annotated; invalidated setups marked. Sentinel only when no defensible price exists. |
| `STOP LOSS` | Single price + basis; sentinel when not justified. |
| `TAKE PROFIT 1/2/3` | Price / range / `NOT AVAILABLE`. T1 always attempted; T2/T3 `NOT AVAILABLE` when insufficient structure — never invented. |
| `RISK / REWARD` | Gross and net (cost-adjusted) R:R per target, via `risk.reward_risk`. Needs entry + stop + TP; otherwise sentinel. |
| `REASON` | One short English sentence. |
| `Hinglish` | One short Hinglish sentence (`HINGLISH_TEMPLATES`). |
| `Data / Freshness / Analysis` | ISO timestamps + freshness class from `validation.freshness`. |
| Disclaimer | Fixed educational disclaimer. |

---

## Full mode

When the user explicitly requests a full analysis (`/full`, `full analysis`, `detailed analysis`, `explain this chart`, `why this entry?`, `show indicators`, `show news`, `show complete research`), render `templates/analysis-report.md` instead. The quick template must never replace it.

---

*Engine: `integrations/python/trading_intel/quick_signal.py` — `render_quick_text`, `render_compact_text_minimal`, `render_quick_html`.*
