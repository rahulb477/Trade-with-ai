# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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

## Unreleased

- Nothing pending. All mandatory V1–V3 scope shipped in 1.0.0.
