# Known Limitations

Written to be uncomfortable. Anything here that sounds like an excuse is a limitation, not a bug report.

---

## 1. What this repository does not do

| Not done | Why |
|----------|-----|
| Place, route, or simulate real orders | Out of scope by design; no execution path exists |
| Give personalised investment advice | Out of scope; would require suitability, licensing, and accountability |
| Fetch live market data | No network code ships; the provider interface is a contract, not an adapter |
| Run ML pattern detection | No labelled dataset, no inter-rater agreement, no out-of-sample work |
| Predict prices | Forecasting is not the goal and the evidence base does not support it |
| Provide probability of profit | Requires assumptions this repository refuses to hide |
| Verify a chart's correctness | It analyses what it is shown; a doctored chart produces a doctored analysis |
| Replace a licensed data feed | It is a reasoning and record-keeping layer |

## 2. Accuracy limits

### 2.1 Chart reading

- **Pixel interpolation.** Levels read from a screenshot are approximate. A 1-pixel error at typical axis density
  can be several ticks.
- **Compressed charts.** A chart with 500 visible candles hides intrabar structure entirely.
- **No tick data.** Everything below the bar interval is invisible.
- **Chart type.** Heikin-Ashi, Renko, and line charts cannot be analysed with candle-pattern rules; the repo refuses
  rather than approximating.

### 2.2 Pattern detection

- **Rules are conventions.** "Hammer" has slightly different thresholds across sources. This repository states its
  thresholds explicitly (`integrations/python/trading_intel/patterns.py`); another source will disagree.
- **Context is a proxy.** Prior-trend classification uses a 20-bar mean comparison, not a full structural analysis.
  It can be wrong, and it is labelled as a heuristic.
- **Base rates are unknown.** The repository does not claim that a hammer "works 60% of the time". No credible,
  reproducible base rate exists for most patterns across markets and regimes.
- **Overlapping patterns.** A single bar can trigger several detectors. The code reports each with a status; it does
  not arbitrate which is "the" pattern.

### 2.3 Indicators

- **Parameters matter.** RSI(14) and RSI(7) can disagree. When the period is not printed, the value is marked
  `ASSUMED`.
- **Redundancy.** Five indicators can be one piece of evidence. The independence audit mitigates this; it cannot
  eliminate it.
- **Regime dependence.** Every indicator fails in some regime (documented per indicator).
- **No volume in forex spot.** Volume indicators are genuinely unavailable there; the repo says so instead of
  substituting tick count.

### 2.4 Technical analysis generally

Technical analysis describes **behaviour and positioning**, not causation. A pattern does not "cause" a move. Any
explanation of *why* a level held is a narrative, and this repository labels narratives as narratives.

## 3. Data limits

| Limit | Consequence |
|-------|-------------|
| No bundled data | Every numeric claim requires a source the user supplies |
| No adjustment handling | If the user's data is unadjusted, splits create false patterns |
| No point-in-time universe | Backtests cannot control survivorship bias without licensed data |
| No intraday history beyond what is supplied | Multi-session intraday patterns cannot be verified |
| Staleness | A screenshot is a moment; by the time it is analysed it may be DELAYED or STALE |
| Timezone ambiguity | An unlabelled timestamp is treated as unknown, not as local time |

## 4. Statistical limits

- **Small samples dominate.** A retail trader's 40-trade history cannot support any edge claim; the confidence
  interval spans most of the plausible range.
- **No probability of profit is output.** Any number would encode assumptions (distribution, correlation, execution)
  that the repository will not hide.
- **Monte Carlo resamples the past.** It cannot generate an unseen tail event.
- **Backtests are upper bounds.** Costs, slippage, and human error push realised results below simulated ones.
- **Regime change breaks stationarity.** Every statistic is a statement about a period, not about the future.

## 5. Behavioural limits of the tool itself

| Limit | Detail |
|-------|--------|
| It can be argued with | A user who insists can push an agent toward a bullish narrative; the gates reduce this but cannot eliminate it |
| It responds to framing | "This looks strong, right?" invites agreement; the evidence-only confidence rule is a partial defence |
| It cannot know your situation | Risk tolerance, horizon, tax position, existing exposure — all unknown, hence no advice |
| It forgets | Without a journal, there is no memory, and without memory there is no measurable track record |
| It is slow by design | Transcription before interpretation is a feature that feels like friction |

## 6. Hard-coded decisions you may disagree with

These are judgement calls, stated so you can override them knowingly:

| Decision | Value | Where to change it |
|----------|-------|-------------------|
| Minimum R:R to T1 | 1.5 | `core/decision-engine.md`, `risk.TradePlan.validation_warnings` |
| Default risk per trade | 0.75% | `sizing.DEFAULT_RISK_PCT` |
| Maximum risk per trade | 2% | `sizing.MAX_RISK_PCT` |
| Room to resistance | ≥2 ATR | `observation.room_class` |
| Stop width ceiling | 3 ATR | `sizing.stop_width_check` |
| Breakout volume confirmation | ≥1.3–1.5× average | `workflows/breakout-analysis.md` |
| Level minimum touches | 2 | `observation.Level.tradable` |
| Timeframe ratio band | 4–6× ideal, ≤12× acceptable | `timeframes.ratio_quality` |
| Minimum sample for a rate | 100 | `engines/backtesting/README.md`, `metrics.summarize` |
| Quality score floor for a verdict | 5/10 | `validation.score_chart_quality` |

## 7. Failure modes you should expect

| Failure | Frequency | Mitigation |
|---------|-----------|------------|
| `WAIT` when you wanted a direction | Common — by design | Read the failing gate; it is usually right |
| "Insufficient data" on a blurry screenshot | Common | Supply a better image or a transcription |
| A pattern the repo does not name | Occasional | Describe the behaviour instead of forcing a label |
| Conflicting evidence reported rather than resolved | Occasional | This is deliberate; false resolution is worse |
| Missing indicator values | Occasional | The value was not printed and was not invented |
| A backtest that cannot be run | Frequent | No data no test; the specification still has value |

## 8. Things that would make this repository better (and are not done)

1. A licensed point-in-time dataset for genuine out-of-sample work.
2. Inter-annotator agreement studies for pattern definitions.
3. A calibrated probability model — which would first require 2–3 years of recorded predictions.
4. Working adapters for two or three major data providers.
5. A browser-based report renderer.
6. Published base rates per pattern, per market, per regime — the honest kind, with n and CIs.

None of these is claimed as complete. See `docs/testing-report.md` for the component-by-component status.

## 9. The limitation that matters most

**This repository cannot make you profitable.** It can make your reasoning auditable, your arithmetic correct, and
your records honest. Whether a documented method earns money depends on execution, costs, position sizing, and the
market regime — none of which a document can guarantee.

Anyone who tells you otherwise is selling something.
