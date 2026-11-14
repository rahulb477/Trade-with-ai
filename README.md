# AI Trading Intelligence — Universal Skill Repository

**Version 1.0.0** · Educational research skill · Not investment advice

A portable, platform-independent knowledge and research repository that teaches a compatible
AI agent how to read a stock-chart screenshot, gather market context, reason about it with
evidence, and produce a **beginner-friendly, honest, hypothetical** research report.

The repository ships V1 (core intelligence), V2 (advanced market & multi-timeframe
intelligence) and V3 (quantitative, order-flow, options and institutional-style research) in a
single delivery — nothing is deferred.

---

## Why this exists

Most "AI trading" material is either unusable jargon or confident nonsense. This repository
takes the opposite position:

> **Deep institutional-quality research, explained in simple language, supported by verifiable
> evidence, with honest uncertainty and disciplined risk awareness.**

That means the skill will happily answer **`WAIT — NO CONFIRMED SETUP`**. Refusing to invent a
trade is a feature, not a bug.

---

## Quick start

### If you are a human

1. Clone or unzip the repository.
2. Open a chat with any agent that can read files (Claude Code, Codex, Gemini CLI, Cursor,
   Windsurf, or a plain chat that accepts pasted text).
3. Point it at `SKILL.md` and attach a chart screenshot. Example:

   > Read `SKILL.md` in this repository, then analyse the attached daily chart of a large-cap
   > Indian bank. Research mode, beginner explanation.

4. Read the report. Cross-check the "SOURCES AND DATA QUALITY" section — it tells you exactly
   what the agent could *not* verify.

### If you are an AI agent

1. Read [`SKILL.md`](SKILL.md) end-to-end. It contains the rules, modes, routing table, status
   codes and definition of done.
2. Read [`AGENTS.md`](AGENTS.md) for mechanical loading instructions and loop control.
3. Run capability detection ([`core/capability-detection.md`](core/capability-detection.md)).
4. Load only the modules the routing table points to.

Nothing else is required. No install step, no API key, no configuration wizard.

---

## What is inside

| Layer | Path | Contents |
|-------|------|----------|
| Entry point | `SKILL.md` | Rules, modes, routing, status codes, checklists |
| Agent mechanics | `AGENTS.md` | Loading order, loop control, fallbacks, refusal conditions |
| Core logic | `core/` | Architecture, analysis engine, decision engine, evidence engine, risk, capability detection |
| Knowledge base | `knowledge/` | 25 candlestick patterns (26 variants), 18 indicators, 16 chart patterns, price action, market structure, smart money, fundamentals, quant, psychology, derivatives, risk, beginner education |
| Strategies | `strategies/` | Scalping, intraday, swing, positional + mandatory validation gate |
| Engines | `engines/` | 13 research engines (chart, market, technical, decision, quant, order flow, options, research agent, prediction tracking, backtesting, strategy discovery, self-evaluation, data integrity) |
| Workflows | `workflows/` | Repeatable 8-step and 16-step procedures |
| Markets | `markets/` | India, US, forex, commodities, crypto specifics — never interchangeable |
| Data | `data-sources/` | Provider interfaces, no-key mode, source validation, API config |
| Integrations | `integrations/` | Pure-stdlib Python library, browser research protocol, OCR guidance, agent adapters |
| Templates | `templates/` | Report shells that enforce the mandatory format |
| Examples | `examples/` | Worked analyses including a legitimate no-trade case |
| Tests | `tests/` | 305 deterministic checks (stdlib `unittest`, no dependencies) |
| Docs | `docs/` | Architecture, installation, usage, compatibility, limitations, security, testing report |

Counts are verified by [`scripts/audit_repo.py`](scripts/audit_repo.py).

---

## The Python library

`integrations/python/trading_intel/` is a **zero-dependency** (standard library only) package:

```python
import sys; sys.path.insert(0, "integrations/python")
from trading_intel import indicators as ind, risk, sizing, backtest, metrics

rsi = ind.rsi(closes, period=14)           # Wilder-smoothed, List[Optional[float]]
atr = ind.atr(highs, lows, closes, 14)
plan = risk.TradePlan("long", entry=100, stop=95, targets=[107, 112, 120])
size = sizing.size_position(equity=500_000, entry=100, stop=95)

print(plan.summary())                 # R_T1 1.4 -> validation_warnings() flags it
print(size.as_dict())                 # units 750, risk_amount 3750.0
```

- No numpy, no pandas, no network calls, no telemetry.
- Every function returns `None`/`NaN`-equivalent for undefined values instead of guessing.
- Deterministic; seeded RNG for Monte Carlo.

Run the tests:

```bash
python3 -m unittest discover -s tests -t . -v
```

---

## Operating modes

| Mode | You ask | You get |
|------|---------|---------|
| **LEARNING** | "explain a bull flag" | Teaching answer, no trade plan |
| **RESEARCH** | "analyse this chart" | Full evidence-based report, conditions not calls |
| **PAPER-TRADING** | "plan a hypothetical trade" | Report + Scenario A/B with entry, stop, T1–T3, R:R, invalidation |

---

## Four data modes

| Mode | Needs | What works |
|------|-------|-----------|
| **Offline knowledge** | Nothing | Education, methodology, chart reading from the image, hand arithmetic |
| **Web research** | A search/fetch tool | News, index context, macro calendar — all cited with timestamps |
| **Market-data integration** | Provider credentials (optional) | Live/last OHLCV → real indicator values |
| **Full research** | Both | Everything, with provenance recorded per field |

The core skill is fully functional in **offline knowledge** mode. Credentials are optional
extras, read from environment variables only — never committed, never prompted for in chat.
See [`data-sources/api-configuration.md`](data-sources/api-configuration.md).

---

## Hard boundaries

**This repository will not:**

- **No broker integration, ever.** It will not place orders, connect to a broker, or generate
  executable trading instructions.
- Provide personalised investment advice or position sizes based on your real capital.
- Invent prices, indicator readings, statistics, news or confidence scores.
- Claim the author has decades of personal trading experience. It cites documented
  methodology and research instead.
- Present a backtest as a promise of future returns.

**Read [`docs/limitations.md`](docs/limitations.md) before trusting any output.**

---

## Repository conventions

- **Markdown is the source of truth.** Code implements what the Markdown specifies and is
  tested against it.
- **Every knowledge file is self-contained**: definition → mechanics → interpretation →
  confirmation → invalidation → false signals → mistakes → exercise.
- **Every internal link resolves.** `scripts/check_links.py` enforces it in CI.
- **Deterministic tests only.** Fixed fixtures, no network, no randomness without a seed.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Status

**Everything below is reproducible.** Run `./scripts/run_all_tests.sh`.

| Check | Result |
|-------|--------|
| Unit + repository-integrity tests | 305 passing |
| Internal links | 0 broken across 212 Markdown files |
| Repository audit (structure, placeholders, credentials, imports) | PASS |
| External dependencies | none |

Honest component-by-component status, with evidence and a ranked gap list, is in
[`docs/testing-report.md`](docs/testing-report.md). The headline positions:

| Component group | Status |
|-----------------|--------|
| Documentation, knowledge base, workflows, templates, examples | **COMPLETE** |
| Python library (indicators, patterns, risk, sizing, stats, simulation, backtest) | **COMPLETE** |
| Tests and verification scripts | **COMPLETE** |
| Chart-pattern *geometry* detection in code | **NOT IMPLEMENTED** (rules documented; identification is manual) |
| Live market-data adapters | **NOT IMPLEMENTED** (interface + offline provider shipped) |
| Validate-a-strategy results | **PARTIAL** — every strategy carries status `DOCUMENTED`; none has been validated, and none is claimed to work |
| ML pattern detection | **NOT IMPLEMENTED** — deliberately, and with the reasons written down |

That last group is the part most repositories overstate. This one does not: a strategy that has not been tested is
called untested, and a feature that has no code is called unimplemented.

### What this is not

It is not a signal service, not a robot, and not a source of returns. It is a research method with a tested
arithmetic layer and an honest record. See [`docs/limitations.md`](docs/limitations.md).

---

## Licence

MIT — see [`LICENSE`](LICENSE). Educational use. No warranty. Not financial advice.
