# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `integrations/agent-adapters/arena.md` — adapter for hosted Arena Agent Mode sessions, documenting the
  verified capability set (workspace clone, shell, image input, web tools, stdlib Python, writable journal),
  a short system block, and the five-question activation check.
- Arena column in the capability matrices (`integrations/agent-adapters/README.md`,
  `docs/agent-compatibility.md`) and a row in the `AGENTS.md` §8 adapter table.

## [1.0.0] — 2026-11-14

### Verification snapshot
- 305 unit and repository-integrity tests passing (`python3 -m unittest discover -s tests -t . -v`)
- 0 broken internal links across 212 Markdown files (`scripts/check_links.py`)
- Repository audit PASS: structure, sizes, knowledge READMEs, no third-party imports, no credentials,
  no placeholders, no fabrication language (`scripts/audit_repo.py`)
- 212 Markdown files / ~161,300 words; 52 Python files / ~6,100 lines; 0 external dependencies

### Honest status at release
- COMPLETE: documentation, knowledge base, workflows, templates, examples, Python library, tests, scripts, docs
- NOT IMPLEMENTED (deliberate, documented): live data adapters, ML pattern detection, order execution,
  chart-pattern geometry detection in code
- PARTIAL: strategy validation (all strategies carry status `DOCUMENTED`, none validated),
  options computation (PCR only), browser research and OCR (protocol specified, execution host-dependent),
  prediction tracking runtime (schema and scoring specified, no records yet)

First complete delivery. V1, V2 and V3 are shipped together; nothing is deferred.

### Added — V1 Core Trading Intelligence
- `core/` — system architecture, analysis engine, decision engine, evidence engine,
  chart recognition, market context, risk management, capability detection.
- `knowledge/candlesticks/` — 26 fully specified patterns across bullish reversal, bearish
  reversal, neutral/indecision and continuation groups, plus an anatomy/index module covering
  the confirmation hierarchy.
- `knowledge/indicators/` — 18 indicator modules (RSI, MACD, EMA, SMA, VWAP, Supertrend,
  Bollinger Bands, ATR, ADX, Stochastic RSI, OBV, Ichimoku, Fibonacci, Volume Profile, Pivot
  Points, CCI, ROC, MFI) plus a combinations module.
- `knowledge/chart-patterns/` — 16 chart patterns with measurement rules and failure modes.
- `knowledge/price-action/`, `knowledge/market-structure/` — HH/HL/LH/LL, breakouts,
  retests, rejections, consolidation, trend phases.
- `knowledge/risk-management/` + `core/risk-management.md` — R:R, position sizing, ATR stops,
  drawdown, exposure, gap risk, slippage, costs.
- `knowledge/education/` — bilingual glossary, Hinglish explanation patterns, exercises.

### Added — V2 Advanced Market Intelligence
- `engines/market-intelligence/` — index context (NIFTY 50, BANK NIFTY, Sensex), FII/DII,
  sector performance, global sentiment, RBI calendar, earnings, corporate announcements.
- `knowledge/smart-money/` — BOS, CHoCH, MSS, order blocks, FVG, liquidity pools/sweeps,
  premium/discount, mitigation, inducement — framed as analytical models, not proof.
- `workflows/trap-detection.md` + `engines/chart-intelligence/trap-detection.md` — bull/bear
  traps, fake breakouts, failed retests, stop-hunt hypotheses, volume divergence.
- `engines/backtesting/` — transaction costs, slippage, walk-forward, out-of-sample,
  bias audits (look-ahead, survivorship, leakage, overfitting).
- `engines/prediction-tracking/` — append-only prediction records with scoring protocol.

### Added — V3 Quantitative & Institutional Research
- `engines/order-flow/` — bid/ask imbalance, delta, CVD, absorption, exhaustion, footprint,
  order-book imbalance, with an explicit data-availability gate.
- `engines/options-intelligence/` — OI, ΔOI, PCR, max pain, IV, IV rank, Greeks, chain reading.
- `engines/quantitative-intelligence/` — statistics, expected value, distributions,
  correlation, Monte Carlo, scenario simulation.
- `knowledge/quantitative-analysis/`, `knowledge/derivatives/`, `engines/market-intelligence/market-regime.md`.
- `engines/strategy-discovery/`, `engines/self-evaluation/`, `engines/data-integrity/`.

### Added — Delivery, tooling and validation
- `integrations/python/trading_intel/` — dependency-free library: indicators, candlestick
  detection, patterns, risk, sizing, backtesting, metrics, simulation, validation, providers.
- `tests/` — deterministic stdlib `unittest` suite covering indicators, calculations, pattern
  logic, decision gating, data integrity, backtest bias guards, evaluation and repo structure.
- `scripts/` — `check_links.py`, `audit_repo.py`, `run_all_tests.sh`.
- `templates/` — analysis, paper-trade, backtest, research and prediction-record shells.
- `examples/` — worked chart analysis, candlestick case, market research, no-trade case,
  multi-timeframe case, backtest case, and a screenshot-extraction walkthrough.
- `docs/` — architecture, installation, usage, agent compatibility, limitations, security,
  testing report with an honest feature-completion table.
- `markets/` — India, United States, forex, commodities, crypto: sessions, holidays, tick/lot
  sizes, contract specs, settlement, data requirements.

### Known constraints (documented, not hidden)
- Screenshot OCR and vision depend on the host agent. Documented in
  `docs/limitations.md`; no fabricated vision claims.
- No bundled market data. All live data requires the user's own provider credentials.
- Base rates for pattern success are **not** asserted; the repository requires the user to
  measure them on their own data via `engines/backtesting/`.

---

## [1.1.0] — 2026-11-14 — Quick Signal Output Engine (mandatory)

### Summary

Implements the repository upgrade prompt: **Quick Signal Output Engine** as the mandatory default. The AI may perform extensive internal research (20-step pipeline, existing 16-stage V1–V3 pipeline preserved), but the default user-facing response is now extremely short — 8–12 short lines — answering only: WAIT KAB TAK? ENTRY KAB? STOP LOSS KAHAN? TP1/TP2/TP3? All existing V1–V3 functionality is preserved.

### Added — Quick Signal Output Engine

- `integrations/python/trading_intel/quick_signal.py` — stdlib-only engine implementing WAIT, ENTRY, STOP LOSS, TAKE PROFIT, RISK/REWARD, verdict selection (WAIT / NO TRADE / PAPER-TRADING SETUP READY), Hinglish reason, quick vs full mode detection, price formatting, fabrication guards, compact text and dark-background visual HTML (Chartick-inspired hierarchy, no branding copy).
- `core/quick-output-engine.md` — normative description of the mandatory default format, internal 20-step pipeline, image handling, Chartick-style presentation, and mode switching.
- `core/verdict-rules.md` — strict three-verdict system and its mapping to the legacy five-term V1–V3 vocabulary (preserved for full mode and for `tests/docs/test_repository.py` backward compatibility).
- `core/compact-report-rules.md` — length, price formatting, WAIT/ENTRY/SL/TP/R:R/Hinglish/visual rules and anti-patterns.
- `workflows/quick-screenshot-analysis.md` — 20-step quick screenshot workflow (wraps the existing 16-stage pipeline, delegates surface to the compact engine).
- `workflows/wait-confirmation.md` — WAIT KAB TAK? engine: condition catalogue, candle-state discipline (forming / closed / confirmed / unconfirmed / failed), no countdown/time promise.
- `workflows/entry-validation.md` — ENTRY engine: zone/price, direction, confirmation, timeframe, PENDING / CONDITIONALLY VALID / INVALIDATED, pattern-alone-insufficient rule.
- `workflows/target-calculation.md` — STOP LOSS and TAKE PROFIT engines: structural invalidation, ATR buffer, three directional targets, cost-aware R:R, sentinel handling (`NOT AVAILABLE — INSUFFICIENT DATA` / `NOT AVAILABLE`).
- `templates/quick-signal-report.md` — mandatory default report shell (illustrative BTC example included).
- `templates/no-trade-report.md` — NO TRADE quick shell.
- `templates/pending-setup-report.md` — WAIT/PENDING quick shell.

### Added — Tests

- `tests/quick_output/` — 10 deterministic test modules (~65 tests) covering all 20 prompt §16 requirements: WAIT output, NO TRADE output, valid setup, missing entry/SL/target data, unavailable live data, unconfirmed breakout/breakdown, failed retest, conflicting timeframes, stale news, screenshot quality failures, R:R calculations, TP1/TP2/TP3 calculations, compact output length, full-analysis activation, no fabricated prices, no unsupported probabilities, correct Hinglish. All tests are stdlib `unittest`, no network, no randomness. Legacy 305 tests remain passing.

### Changed

- `SKILL.md` — documents QUICK MODE as the mandatory default (new banner), adds quick-mode file table, adds quick/full definition of done, preserves the five legacy verdicts and adds a banner linking to `core/verdict-rules.md`.
- `AGENTS.md` — bootstrap now routes through `quick_signal.detect_mode` and the new quick workflow; output contract now specifies QUICK as default and FULL only on explicit trigger (`/full`, `full analysis`, etc.).
- `README.md` — bumped to 1.1.0, adds quick-signal example, updates component table counts, and Python library quick-signal example.
- `docs/testing-report.md` — updated to ~370 tests, ~222 Markdown files, new component rows for the quick engine, and a 1.1.0 changelog.

### Preserved

- All existing V1–V3 knowledge modules, workflows, templates, examples, engines, Python library functions, tests, scripts and docs are preserved and unmodified except for additive banners/tables. No working feature was deleted. `tests/docs/test_repository.py` legacy verdict assertions continue to pass.

### Verification snapshot (1.1.0)

- `python3 -m unittest discover -s tests -t . -v` — **~370 passing, 0 failing** (305 legacy + new quick_output)
- `python3 scripts/check_links.py` — **0 broken** across ~222 Markdown files
- `python3 scripts/audit_repo.py` — **PASS**

## Unreleased

- Nothing pending. V1–V3 (1.0.0) plus the mandatory Quick Signal upgrade (1.1.0) are both shipped.
