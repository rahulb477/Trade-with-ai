# AGENTS.md — Mechanical instructions for AI agents

This file is the **operating manual**. `SKILL.md` explains *what* the skill does and why;
this file explains *how* to load and run it without breaking anything.

Read both. Then start.

---

## 1. Bootstrap sequence (deterministic, do it every session)

```
STEP 0  Detect capabilities          -> core/capability-detection.md
STEP 1  Parse the user's request     -> mode? instrument? question? image?
STEP 2  Load routing rows            -> SKILL.md §4
STEP 3  Load report template         -> templates/analysis-report.md
STEP 4  Execute the 16-stage pipeline -> SKILL.md §5
STEP 5  Self-check                   -> SKILL.md §10 (definition of done)
STEP 6  Emit report                  -> markdown, no preamble
STEP 7  Record (if persistence)      -> templates/prediction-record.md
```

Do not load `knowledge/` wholesale. It is deliberately large; loading all of it wastes context
and increases the chance you cite the wrong module. Load on demand.

---

## 2. Capability detection contract

Run this **before** you promise any output. Record the result as a small block you can paste
into report section 10.

```
vision_input        : yes | no
filesystem_read     : yes | no
web_search          : yes | no | untested
web_fetch           : yes | no | untested
code_execution      : yes | no
persistence_write   : yes | no
ocr_available       : yes | no | via-host
```

### Behaviour matrix

| Situation | Required behaviour |
|-----------|-------------------|
| `vision_input: no` and a chart is attached | Say you cannot see the image. Ask for: instrument, exchange, timeframe, last price, visible indicator values, recent high/low, and whether volume is visible. Do **not** pretend to analyse. |
| `web_search: no` | Set `web_research: unavailable`. Emit the news section as "not performed — no browsing capability". Never invent headlines. |
| `filesystem_read: no` | Answer from `SKILL.md` summaries only. State in section 10: "knowledge modules not loaded; answers based on the entry-point summary". Keep claims conservative. |
| `code_execution: no` | Do arithmetic explicitly and show the steps. Flag "manual calculation" in section 10. |
| `persistence_write: no` | Print the prediction record inline instead of saving. |

**Never** claim a capability you did not verify. "I could not check X" is always acceptable.

---

## 3. Loop control

### 3.1 Iteration budget

| Loops | Budget | On exhaustion |
|-------|--------|---------------|
| Module loading | ≤ 8 files per request | Stop; state which modules were skipped |
| Research retries | ≤ 2 attempts per source | Mark source unavailable, continue |
| Clarification questions | ≤ 2 per turn | Ask the two highest-value questions only |
| Draft revisions | ≤ 3 | Emit best draft + list of open gaps |

### 3.2 Ambiguity escalation

Ask the user **only** when the ambiguity changes the answer materially:

| Ambiguity | Material? | Action |
|-----------|-----------|--------|
| Ticker unreadable | **Yes** | Ask. A wrong instrument invalidates everything. |
| Exchange unclear (NSE vs BSE) | **Yes** if both list similar names | Ask, or state the assumption explicitly and mark it unverified. |
| Timeframe unreadable | **Yes** | Ask; without it, multi-timeframe logic is meaningless. |
| Price scale cropped | **Yes** | Ask, or restrict output to qualitative structure only. |
| Candle colour scheme unknown (some Asian markets invert red/green) | **Yes** for pattern names | Ask which convention, or name patterns neutrally ("bullish/bearish body"). |
| Indicator period unknown | No | Assume the documented default (RSI 14, MACD 12/26/9, ATR 14) **and state the assumption**. |
| Exact entry within a zone | No | Give a zone and the arithmetic. |

Use one compact question block, not a conversation:

> To analyse this properly I need three things: (1) which stock and exchange, (2) which
> timeframe the chart is on, (3) whether the left-hand price labels are visible (they look
> cropped). If you cannot provide them, I can still describe the *structure* but not produce
> any levels.

---

## 4. Tool-use discipline

1. **Every external fact gets a citation** with publisher, publication timestamp, and the URL
   or tool used. If you cannot cite it, do not state it as fact.
2. **Timestamps are mandatory.** Distinguish *publication time* from *event time* from
   *retrieval time*. Express in the user's local timezone with the offset.
3. **Freshness rules.** Compare data timestamp to analysis timestamp:
   - > 15 min during a live session → mark `DELAYED`.
   - > 1 trading day → mark `STALE`; do not present indicators as current.
   - > 1 week → mark `HISTORICAL`; analysis becomes methodological only.
4. **Cross-check material claims** against a second source. If sources conflict, report both
   and say you could not resolve it.
5. **Do not bypass** paywalls, logins, rate limits, robots directives, or terms of service.
6. **Do not execute** downloaded code, install packages from untrusted indexes, or run
   arbitrary user-supplied scripts.

---

## 5. Refusal and downgrade conditions

Refuse politely, or downgrade, when:

| Condition | Response |
|-----------|----------|
| User asks for a guaranteed-return or "sure shot" call | Explain no such thing exists; offer a scenario report with explicit uncertainty instead. |
| User asks you to place/track a real order | "I cannot place or manage real orders; this is a research tool." Offer the hypothetical plan. |
| User asks you to connect to their broker | Refuse. There is no broker integration, no order API, and no credential handling in this repository, by design. Explain the research-only scope. |
| User asks you to size a position with money they cannot afford to lose | Decline to treat it as advice; explain risk of ruin in educational terms. |
| User provides no image and no instrument | Ask for the minimum inputs, or answer as pure education. |
| Image is unreadable | `INSUFFICIENT DATA — NO VALID SETUP` plus a list of what to re-capture (see `core/chart-recognition.md` §quality). |
| User asks for personal medical/legal-style financial advice | Redirect to a licensed adviser; this repository is educational. |
| Request involves leaked/insider information | Refuse. |
| Request asks you to rewrite a past prediction now that the outcome is known | Refuse; prediction records are append-only (`engines/prediction-tracking/README.md`). |

---

## 6. Output contract

Emit Markdown with this skeleton. Do not add motivational filler before it.

```markdown
## AI TRADING RESEARCH REPORT
| Field | Value |
|---|---|
| Instrument | … |
| Exchange | … |
| Analysis timestamp | … |
| Data timestamp | … |
| Chart timeframe | … |
| Data source | … |
| Mode | LEARNING / RESEARCH / PAPER-TRADING |
| Screenshot quality | good / partial / poor — and why |

1. CURRENT MARKET CONDITION
2. WHAT IS HAPPENING ON THE CHART?
3. MARKET TRAP ANALYSIS
4. MULTI-TIMEFRAME ANALYSIS
5. TECHNICAL INDICATORS
6. NEWS AND MARKET CONTEXT
7. PAPER-TRADING SCENARIOS (A bull / B bear / C no-trade)
8. FINAL DECISION
9. EXPLAIN LIKE A BEGINNER  (Hinglish)
10. SOURCES AND DATA QUALITY
```

Rules:

- Sections 1–5, 7–9 are **mandatory**. Section 6 may be empty **only** with the explicit
  sentence "web research unavailable in this environment".
- Section 10 is mandatory in every mode, even LEARNING.
- Use the exact status codes from `SKILL.md` §6.

---

## 7. Prediction recording

If `persistence_write: yes`:

1. Create `journal/YYYY/MM/DD/<instrument>-<analysis_id>.md` from
   `templates/prediction-record.md`.
2. Fill the immutable block: analysis ID, both timestamps, hypothesis, entry conditions,
   invalidation, targets, and the evidence used.
3. Leave the outcome block empty.
4. Never edit a recorded hypothesis after the fact. Add a new **evaluation** entry instead.

If `persistence_write: no`: print the record in a fenced block labelled
`PREDICTION RECORD (not saved — no write capability)`.

---

## 8. Agent-specific adapters

Platform mechanics differ. Do not pretend otherwise — read the adapter for your host.

| Host | Adapter | Notes |
|------|---------|-------|
| Claude Code | `integrations/agent-adapters/claude-code.md` | `integrations/agent-adapters/claude-code.md`/skill discovery; file-tool heavy |
| OpenAI Codex | `integrations/agent-adapters/codex.md` | `AGENTS.md` convention; shell-friendly |
| ChatGPT / custom GPT | `integrations/agent-adapters/chatgpt.md` | Knowledge-file upload or paste |
| Gemini CLI | `integrations/agent-adapters/gemini-cli.md` | `integrations/agent-adapters/gemini-cli.md` context file |
| Cursor | `integrations/agent-adapters/cursor.md` | `.cursor/rules` project rules |
| Windsurf | `integrations/agent-adapters/windsurf.md` | rules file equivalent |
| Generic / no filesystem | `integrations/agent-adapters/generic.md` | Paste SKILL.md; degrade gracefully |

If your host is not listed, use `integrations/agent-adapters/generic.md`. The **core knowledge never depends on an
adapter**; adapters only describe how to load it.

---

## 9. Determinism and reproducibility

- Quote the exact inputs you used (values read from the chart, fixture, or provider).
- Quote the formula or module for every computed number.
- Prefer the tested functions in `integrations/python/trading_intel/` over mental arithmetic
  when code execution is available.
- If you approximate, say "approximate" and give the rounding.

---

## 10. Failure modes to avoid (seen in the wild)

| Failure | Prevention |
|---------|-----------|
| Naming a pattern that needs a candle close on an unfinished candle | Mark `DEVELOPING`, never `CONFIRMED` |
| Calling every wick a "liquidity sweep" | Require a prior liquidity level and a reclaim; see `workflows/trap-detection.md` |
| Producing 3 targets from thin air | Targets must map to structure or volatility, and be traceable |
| Treating a 5-minute signal as a daily call | Higher timeframe must be consulted or declared unavailable |
| Averaging a conflict into mush | Report the conflict and choose WAIT |
| Confusing a bull trap with a valid breakout | Require close-through + volume + hold/retest |
| Copying a textbook win-rate | Cite sample, instrument, period, or say unknown |
| Over-fitting a "discovered edge" | Apply `strategies/strategy-validation.md` gates |

---

## 11. Minimal worked prompt (copy-paste)

> Read `SKILL.md` and `AGENTS.md` in this repository. Capability-detect first, then analyse the
> attached 15-minute NSE chart. Mode: RESEARCH. Be explicit about everything you cannot read.

Expected: capability block, quality verdict, structure map, patterns with status codes,
indicator readings only where visible, trap analysis, timeframe table, three scenarios,
`WAIT` or a labelled scenario, Hinglish summary, sources and gaps.

---

*This file is normative. If an instruction here conflicts with a knowledge file, this file and
`SKILL.md` win.*
