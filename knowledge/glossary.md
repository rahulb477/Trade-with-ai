# Master Glossary

Every term used across this repository, grouped by domain. The **English + Hinglish, multi-column** version with
misuse warnings lives in [`education/glossary.md`](education/glossary.md); this file is the single-page reference for
reading any document in the tree.

Conventions: a * means the term is commonly misused — see the misuse note where present. Definitions are operational
(how the term is used *here*), not dictionary-wide.

---

## 1. Chart foundations

| Term | Definition |
|------|------------|
| OHLC | Open, high, low, close — the four prices a candle encodes. |
| Body | The open-to-close distance. |
| Shadow / wick | The high-to-body and body-to-low distance. |
| Range | High − low for the bar. |
| Timeframe | The duration one bar represents (1m, 15m, 1D, 1W). |
| Session | The trading hours of a venue (NSE cash: 09:15–15:30 IST). |
| Gap | A discontinuity between one session's close and the next open. |
| Adjusted price | A price series corrected for splits/bonus/dividends. Unadjusted series create false patterns. |
| Chart type | Candlestick, OHLC bar, line, Heikin-Ashi, Renko. Candle-pattern rules apply **only** to the first two. * |
| Tick | The minimum price increment of an instrument. |
| Volume | Shares/contracts traded in the bar. Absent in forex spot — never substitute tick count for volume. * |

## 2. Structure

| Term | Definition |
|------|------------|
| Swing high/low | A local extreme defined by `k` bars on each side. Always state `k`. * |
| Higher high / higher low (HH/HL) | The sequence that defines an uptrend. |
| Lower high / lower low (LH/LL) | The sequence that defines a downtrend. |
| Structure break | A close beyond the most recent swing point in the direction opposite the trend. |
| Trend | A directional sequence of swings, not a line on a chart. * |
| Range | Price oscillating between two tested boundaries with no net progress. |
| Level* | A price **zone** with ≥2 touches. One touch = a line, not a level. |
| Zone | A band (e.g. 1,232–1,240) rather than a single price. Levels are zones. |
| Touch | A test of a level by price, ending with a reaction. |
| Level exhaustion | A level that has been tested so often it loses meaning (the 4th+ test often breaks). |
| Round number | A psychologically salient price (100, 1,000, 25,000). |
| Trendline | A line connecting ≥2 swing points; the third touch is the confirmation. |
| Regime | Trending / ranging / high-volatility / squeeze / transitional. Selects the toolkit. * |
| Phase | Accumulation, markup, distribution, markdown — a model, not an observable. * |

## 3. Price action

| Term | Definition |
|------|------------|
| Breakout* | A **close** beyond a level, ideally with volume ≥1.3–1.5× average. A wick beyond is not a breakout. |
| Breakdown | A close below support. |
| Retest | Return to a broken level that **holds outside** it. |
| Rejection | A bar that trades beyond a level and closes back inside it. |
| Trap / fakeout* | A break followed by a close back inside, within roughly 1–3 bars. Evidence-scored 0–6. |
| Failed breakout | A breakout that could not hold; the best R:R setups often come from its reversal. |
| Consolidation | A contraction in range, usually after an impulse. |
| Impulse | A directional leg with above-average range and volume. |
| Pullback | A counter-trend move that holds a structural level. |
| Continuation | Resumption of the prior direction after a pause. |
| Reversal | A change of trend direction, confirmed by a structure break — not by an oscillator. |
| Absorption | Volume transacting with little price movement at a level. Requires volume data; on a price chart, only "consistent with". * |
| Liquidity pool | A cluster of stops beyond an obvious level (equal highs/lows, round numbers). |
| Stop run / sweep* | A wick beyond a level followed by a reclaim. Describes behaviour, not intent. |

## 4. Candlestick patterns

| Term | Definition |
|------|------------|
| Confirmation hierarchy | Higher-timeframe context > location at a level > candle shape > volume. * |
| Pin bar | Umbrella term for hammer/shooting star shapes: small body, long single shadow. |
| Hammer* | Small body at the top, long lower shadow, **after a decline**. In an uptrend the same shape is a hanging man. |
| Hanging man | Hammer shape after an advance; bearish reading. |
| Shooting star | Long upper shadow after an advance. |
| Inverted hammer | Long upper shadow after a decline; bullish but needs confirmation. |
| Doji | Body ≤10% of range. Indecision — meaningless unless at a level. * |
| Spinning top | Small body with shadows on both sides. |
| Marubozu | Body ≥90% of range; almost no shadows. |
| Engulfing* | The current body fully contains the prior body. Direction depends on the prior bar's colour. |
| Harami | A small body contained inside the prior large body. |
| Piercing line / dark cloud cover | The two-bar midpoints-crossed pairs; mirror images. |
| Morning star / evening star | Three-bar reversal: large bar, small gapped bar, strong close back into bar one. |
| Three white soldiers / black crows | Three consecutive strong bars in one direction with small opposite shadows. |
| Abandoned baby | A doji isolated by gaps on both sides. Very rare; check for data errors. |
| Pattern status | `CONFIRMED` (rules + context) · `DEVELOPING` (shape, awaiting next bar) · `POSSIBLE` (shape, wrong context) · `UNCLEAR`. |

## 5. Chart patterns

| Term | Definition |
|------|------------|
| Head and shoulders* | Three peaks, the middle highest, with a neckline break on a **close**. Volume should expand on the break. |
| Neckline | The support line connecting the two troughs of H&S (or the two peaks of an inverse). |
| Double/triple top | Repeated failures at one level; confirmed only on the neckline close. |
| Ascending triangle | Flat resistance + rising support → usually a continuation. |
| Descending triangle | Flat support + falling resistance. |
| Symmetrical triangle | Converging trendlines, no directional bias. Apex often produces a false move. |
| Rising wedge | Converging upward lines → typically breaks **down**. |
| Falling wedge | Converging downward lines → typically breaks **up**. |
| Flag | Small counter-tendency channel after an impulse. |
| Pennant | A tiny triangle version of a flag. |
| Rectangle | Horizontal range with tested boundaries. |
| Cup and handle | A rounded base then a shallow pullback, breaking out above the rim. |
| Measured move | Projecting the pattern's height from the breakout point — a convention, not a law. * |
| Prior trend | The trend **before** the pattern. Without it, most patterns are meaningless. * |

## 6. Indicators

| Term | Definition |
|------|------------|
| SMA / EMA | Simple / exponential moving averages. EMA weights recent prices more. |
| Golden / death cross | 50/200 MA crosses. Very lagging; a regime label, not a signal. * |
| MACD | Difference of two EMAs plus a signal EMA; the histogram is the difference of the two. |
| RSI | 0–100 momentum oscillator; 70/30 are conventions, not laws. "Overbought" ≠ "sell". * |
| Stochastic | Position of the close within the recent high–low range. |
| Stochastic RSI | A stochastic of the RSI value; doubly smoothed, very noisy at low timeframes. |
| ADX | Trend *strength* (0–100), not direction. >25 trending, <20 ranging. |
| DI+ / DI− | Directional movement; DI+ above DI− indicates upward pressure. |
| ATR | Average true range: volatility in price units. The basis of every sizing decision. |
| Bollinger Bands | Mean ± n standard deviations. Width measures volatility; a "squeeze" precedes expansion. |
| Bollinger bandwidth | (Upper − lower) / middle — a scale-free volatility measure. |
| Keltner Channel | EMA ± ATR multiple. |
| Supertrend | ATR-based trailing stop that flips side; whipsaws in ranges. * |
| Ichimoku | Five-line system: tenkan, kijun, senkou A/B, chikou. The cloud is senkou A/B. |
| VWAP | Volume-weighted average price, session-anchored. An institutional reference, not a signal. * |
| OBV | Cumulative volume signed by price change. Only its shape matters. |
| MFI | Volume-weighted RSI on typical price. |
| CCI | Deviation of typical price from its mean, scaled by mean absolute deviation. |
| ROC | Percentage price change over n bars. |
| Pivot points | Session-derived support/resistance from the prior bar's H/L/C. |
| Fibonacci retracement | Proportional levels (23.6/38.2/50/61.8/78.6%) of a measured swing. Self-fulfilling to a degree, which is a reason, not a proof. * |
| Volume profile | Volume by price; the POC is the highest-volume price, the value area holds ~70%. |
| Divergence* | Price and an oscillator disagree. A hypothesis, not a signal — requires a structure break. |
| Indicator family | Trend / momentum / volatility / volume / levels. Two from one family = one piece of evidence. * |

## 7. Smart money concepts (SMC)

| Term | Definition |
|------|------------|
| SMC | A framework describing price delivery around liquidity. Descriptive vocabulary, not a mechanism you can verify. * |
| BOS (break of structure) | A close beyond the prior swing in the **trend** direction (continuation). |
| CHoCH (change of character) | The first break against the trend — an early reversal warning. |
| MSS (market structure shift) | A CHoCH with displacement (an impulsive move), treated as stronger evidence. |
| Order block* | The last opposite-direction candle before an impulsive move. A *description* of a price zone, not proof of institutional intent. |
| Fair value gap (FVG)* | A three-bar imbalance where bar 1's high and bar 3's low do not overlap. Never say it "will be filled". |
| Mitigation | Price returning to an order block before continuing. |
| Inducement | A minor liquidity level engineered to trap early entries. Unverifiable intent — describe the behaviour instead. |
| Premium / discount | The upper/lower half of a range (relative to the 50% equilibrium). |
| Liquidity | Resting orders; in practice, clusters of stops beyond obvious levels. |

## 8. Derivatives

| Term | Definition |
|------|------------|
| Open interest (OI) | Outstanding contracts. OI + price describes positioning, **not** direction. * |
| ΔOI | Change in OI, usually read against price change. |
| Futures | Standardised contracts with expiry and margin. Basis = futures − spot. |
| Rollover | Moving a position to the next expiry; creates artefacts in continuous series. |
| Contract multiplier / lot size | Units per contract. Always verify; never recall. |
| Option chain | Struck prices with OI, volume, prices, IV, Greeks for one expiry. |
| Put/call ratio (PCR) | Put OI ÷ call OI. Cannot distinguish bought from sold options. * |
| Max pain | The expiry price minimising total option payout. Arithmetic, not a prediction. * |
| Implied volatility (IV) | The volatility implied by an option's price. |
| IV rank / percentile | IV relative to its own 52-week range — far more useful than raw IV. * |
| IV crush | Post-event collapse in IV; a long option can lose money on a correct direction. |
| Greeks | Delta, gamma, theta, vega, rho — sensitivities, model-dependent. |
| Theta | Time decay. |
| Expiry day | The contract's last trading day. Behaviour is erratic; verify the date, never recall it. * |

## 9. Risk and money management

| Term | Definition |
|------|------------|
| Risk per trade | The amount lost if the stop fills, as a % of equity. Default band here: 0.25–1.0%. |
| Position size | `floor(equity × risk% ÷ |entry − stop|)`. Always round **down**. |
| R | One unit of risk. Every outcome is measured in R. |
| R-multiple | Profit or loss divided by the initial risk. |
| Reward:risk (R:R) | Target distance ÷ risk distance. Minimum here: 1.5 to T1. |
| Stop loss* | The price at which the thesis is proven wrong — structural, not a comfort level. |
| Invalidation | The event (usually a close) that voids the idea. Distinct from the stop order's fill price. |
| Hybrid stop | Structure ± a fraction of ATR (0.25–0.5). |
| Trailing stop | A stop that follows price; it never moves against the position. |
| Maximum adverse excursion (MAE) | The worst unrealised loss during a trade. |
| Maximum favourable excursion (MFE) | The best unrealised profit during a trade. |
| Drawdown | Peak-to-trough equity decline. 50% down needs 100% up to recover. |
| Risk of ruin | Probability of hitting an unrecoverable loss level. |
| Kelly fraction | The growth-optimal bet size. Reported for reference; trading caps are far below it. * |
| Cost_R | Round-trip cost expressed in R. Must be subtracted before any expectancy claim. |
| Notional | Position value (units × price). Capped independently of risk. |
| Correlation | Co-movement of returns; rises in stress. Correlated positions are one risk, not three. * |
| Slippage | Difference between expected and realised fill price. |
| Liquidity risk | The risk that you cannot exit at the intended price. |

## 10. Quant and statistics

| Term | Definition |
|------|------------|
| Expectancy | `win_rate × avg_win − loss_rate × avg_loss`, in R. |
| Profit factor | Gross profit ÷ gross loss. |
| Win rate | Wins ÷ trades. Meaningless without n and a confidence interval. * |
| Confidence interval | A range that plausibly contains the true value. With n < 100 it is very wide. |
| Wilson interval | A proportion CI that behaves well at small n and near 0/1. Used here for hit rates. |
| Standard deviation | Dispersion of a series. |
| Sharpe ratio | Excess return ÷ volatility, annualised. Needs ≥2 years of data to mean anything. |
| Sortino ratio | Like Sharpe but penalising only downside deviation. |
| Sample size | n. Below 30, no rate claim; below 100, no edge claim. * |
| Out-of-sample | Data not used to design the rule. The only test that counts. |
| Walk-forward | Rolling train/test windows; report the concatenated **test** segments only. |
| Overfitting | Fitting noise. Detected by plateau tests and out-of-sample failure. * |
| Look-ahead bias | Using information not available at decision time. |
| Survivorship bias | Analysing only instruments that still exist. |
| Multiple testing | Testing k hypotheses inflates the false-positive rate: `1 − 0.95^k`. |
| Monte Carlo | Resampling to see the distribution of outcomes. Cannot invent unseen events. * |
| Bootstrap | Resampling with replacement to estimate a statistic's distribution. |
| Base rate | How often something happens unconditionally. Report it before any "detection rate". * |
| Correlation ≠ causation | Co-movement does not establish mechanism. |

## 11. Psychology

| Term | Definition |
|------|------------|
| Process vs outcome | Good decisions can lose; bad ones can win. Judge the process. * |
| Loss aversion | Losses hurt roughly twice as much as equivalent gains. |
| Disposition effect | Selling winners early and holding losers. |
| Confirmation bias | Seeking evidence that supports the existing view. |
| Recency bias | Overweighting the most recent observations. |
| Anchoring | Fixating on an entry price or a prior high. |
| Sunk cost | Letting money already lost influence a decision. |
| Tilt | Emotional dysregulation after a loss, producing worse decisions. |
| Revenge trading | Re-entering to recover a loss immediately. |
| Circuit breaker | A pre-written rule that halts trading (daily loss limit, streak limit, time-out). |
| Journal | An append-only record of hypothesis, execution, and review. |
| Hindsight bias | Believing an outcome was obvious after the fact. |
| Rule-breaking | The only discipline failure. A loss within the rules is variance, not failure. * |

## 12. Process and evidence terms

| Term | Definition |
|------|------------|
| Provenance class | chart-observation / computed / external-cited / user-stated / assumption. |
| ASSUMED | A value used because it was needed and not supplied. Must be marked. |
| Quality score | 0–10 screenshot score that caps what the report may claim. |
| Gate | A pass/fail check before a verdict (G1 data … G7 trap risk). |
| Capability block | The list of tools/data the agent actually has. |
| Data mode | Offline / web research / market-data / full research. |
| Confidence label | Strong / Moderate / Weak / Speculative / Not assessable — tied to independent evidence count. |
| Freshness class | LIVE / RECENT / DELAYED / STALE / HISTORICAL. |
| Prediction record | The immutable pre-outcome analysis entry. |
| Executable success | Trigger occurred **and** the invalidation held while a target was reached. |
| Directional accuracy | Price moved the implied way, possibly with an unexecutable path. |
| NOT SAVED | Marker for a record printed but not persisted. |
