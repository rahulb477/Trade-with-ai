# Evidence Engine

Provenance, reliability, freshness and conflict handling. Every sentence that influences a verdict
must be classifiable here.

---

## 1. Provenance classes

| Class | Definition | Example | Weight |
|-------|-----------|---------|--------|
| `OBSERVED` | Read directly from the supplied image by the agent's vision. | "Last candle is a bullish engulfing closing at 1_204" | High |
| `USER-STATED` | Provided by the user in text. | "This is RELIANCE on NSE, daily" | High, but unverified |
| `COMPUTED` | Derived arithmetically from `OBSERVED`/`USER-STATED` values, with the formula shown. | "R:R = (1_240−1_204)/(1_204−1_186) = 2.0" | High if inputs are High |
| `CITED` | From an external source with publisher, timestamp and link. | NSE press release dated 2026-11-12 | Medium–High |
| `PROVIDER` | From a licensed market-data API the user configured. | Last trade 1_204.35 at 15:29:58 IST | High if fresh |
| `MODEL` | Output of a computational model (Monte Carlo, correlation, backtest) with assumptions disclosed. | "5 000-path bootstrap: 5th–95th percentile …" | Medium, assumption-bound |
| `DOCUMENTED` | A rule/definition from `knowledge/`, i.e. established methodology, not a claim about this chart. | "An engulfing requires body 2 to contain body 1" | Context, not evidence of state |
| `ASSUMED` | A default adopted because the true value was unavailable, and labelled. | "RSI period assumed 14 (not printed)" | Low — must be flagged in section 10 |
| `UNVERIFIED` | Plausible but not confirmed. May be mentioned only as a hypothesis. | "Ticker could be TATAPOWER or TATAMTRDVR" | Must not drive a verdict |

**Hard rule:** a verdict may be driven only by `OBSERVED`, `USER-STATED`, `COMPUTED`, `CITED`,
`PROVIDER` or `MODEL`. `ASSUMED` and `UNVERIFIED` may shape wording, never direction.

---

## 2. Freshness

Attach to every external fact:

| Class | Condition (equity, live session) | Permitted use |
|-------|----------------------------------|----------------|
| `LIVE` | ≤ 60 s old | Any use |
| `RECENT` | ≤ 15 min | Any use; note delay if the source is delayed |
| `DELAYED` | 15 min – 1 session | Levels and indicators may be used but must be labelled; no "current price" claims |
| `STALE` | > 1 session, ≤ 1 week | Methodology only; not an intraday verdict |
| `HISTORICAL` | > 1 week | Education/backtest only |

Non-equity sessions differ (crypto 24/7, forex 24/5). Use market-specific windows from
`markets/`.

Always store three timestamps:

1. `event_time` — when the thing happened
2. `publication_time` — when the source published it
3. `retrieval_time` — when the agent read it

A news item published at 09:05 about an event at 08:00 read at 14:00 has three distinct times.
Conflating them is how analyses end up citing "breaking" news that is six hours old.

---

## 3. Reliability tiers for sources

| Tier | Sources | Use |
|------|---------|-----|
| **A — Primary/regulatory** | Exchange notices (NSE/BSE), SEBI, RBI, SEC/EDGAR, company filings & investor-relations pages, official statistics agencies | Cite as authoritative; still timestamp |
| **B — Licensed/professional** | Paid market-data APIs, major financial wires, audited data vendors | Cite; note licensing |
| **C — Established media** | Reputable financial press with named journalists and correction policies | Cite; cross-check material claims |
| **D — Aggregators/forums** | Blogs, aggregator sites, social posts | Never sufficient alone; use only to *discover* a lead that is verified in A–C |

Tier D is not banned from the *conversation*; it is banned from being the *sole support* for a
material claim.

---

## 4. Conflict handling

When two sources disagree on a material fact:

```
1. Identify the material fact precisely (price, date, ratio, verdict).
2. Check whether the difference is explained by timing (different as-of times).
3. Check whether it is explained by definition (adjusted vs unadjusted close; consolidated vs
   standalone financials; spot vs futures).
4. If still conflicting -> report BOTH with provenance, state "unresolved", lower confidence one
   rung, and do not let the conflict silently resolve in favour of the more convenient number.
```

Never average two conflicting numbers to produce a tidy one.

---

## 5. Evidence ledger (required in every report's section 10)

| # | Claim | Class | Source | Event time | Retrieved | Freshness | Reliability |
|---|-------|-------|--------|-----------|-----------|-----------|-------------|
| 1 | Last close 1_204.35 | PROVIDER | <provider> | 2026-11-14 15:29 IST | 15:31 IST | LIVE | B |
| 2 | Bullish engulfing on 15m | OBSERVED | screenshot | — | 15:31 IST | — | vision, good quality |
| 3 | Q2 results on 2026-11-18 | CITED | exchange filing | 2026-11-10 | 15:32 IST | RECENT | A |
| 4 | RSI 14 = 61 | ASSUMED period | screenshot | — | — | — | low |

This ledger is the antidote to fabrication: if a claim has no row, it does not belong in the report.

---

## 6. Independence of evidence

The engine must count *independent* evidence classes, not raw bullet points.

Independent classes:

1. **Price structure** (swings, trend, S/R)
2. **Candle formation** (pattern shape on closed candles)
3. **Volume / participation**
4. **Momentum indicator** (RSI/MACD family)
5. **Volatility regime** (ATR, Bollinger width)
6. **Higher-timeframe state**
7. **Derivatives positioning** (OI/PCR — only with real data)
8. **Fundamental/news context** (cited)

Not independent: two oscillators measuring the same thing (RSI + Stochastic RSI ⇒ one class);
a trendline and a support level drawn from the same two pivots (⇒ one class).

**Independence audit question:** *"If I removed this entire screenshot, could I still have stated
this evidence?"* If no for several bullets, they are one class.

---

## 7. Language calibration

| Evidence state | Phrase |
|----------------|--------|
| Multiple independent classes, no conflict | "The evidence is consistent with…" |
| One strong class | "This candle/setup is one input; it is not confirmation by itself." |
| Conflicting | "Two readings disagree: X says …, Y says …. I cannot resolve this from the data provided." |
| Missing | "Not visible / not available / not provided — I have not assessed it." |
| Assumed | "I am assuming the default period of 14 because it is not printed." |
| Model output | "Under these assumptions, the simulation gives … These are assumptions, not forecasts." |

Banned phrasings: "guaranteed", "sure shot", "confirmed breakout" (when only `DEVELOPING`),
"smart money is buying", "the market will", "historically this wins 80% of the time" (unless a
specific test is cited), "trust me".

---

## 8. Self-audit before publishing

1. Every number traceable? (ledger check)
2. Every external fact timestamped and tiered?
3. Any `UNVERIFIED` item leaking into the verdict?
4. Any two bullets that are secretly the same evidence class?
5. Is any conflict omitted for tidiness?
6. Does the confidence label match the count of independent classes?

If any answer is unsatisfactory, revise downward — reduce claims, not standards.

---

*See also: [`../engines/data-integrity/README.md`](../engines/data-integrity/README.md) ·
[`../data-sources/source-validation.md`](../data-sources/source-validation.md)*
