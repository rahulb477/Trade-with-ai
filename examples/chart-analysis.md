# Example — Full Chart Analysis

> **FICTIONAL.** Instrument "ALPHATECH" (fictional NSE-listed illustrative name), prices invented for
> demonstration. No real security is described.

---

## 1. Data & Provenance

| Field | Value |
|-------|-------|
| Instrument | ALPHATECH (fictional) |
| Exchange | NSE (assumed) |
| Asset class | Equity |
| Timeframes analysed | 1D |
| Other timeframes shown | none |
| Chart type | Candlestick |
| Data source | screenshot (simulated) |
| Data timestamp | 2026-11-14 15:30 IST (assumed session close) |
| Analysis timestamp | 2026-11-14 16:05 IST |
| Freshness class | RECENT (post-close daily data) |
| Last price | 1,248.6 (read from the price axis, approximate) |
| Mode | RESEARCH |
| Data mode | offline (no provider, no browsing) |

## 2. Chart Quality Score

| Dimension | Present? | Weight |
|-----------|----------|--------|
| Instrument identifiable | yes | 2 |
| Timeframe visible | yes | 1 |
| Price axis readable | yes | 2 |
| Volume present | yes | 1 |
| Indicators labelled | yes (20 & 50 EMA, RSI 14) | 1 |
| Candles clear | yes | 2 |
| Axes not distorted | yes | 1 |
| **Total** | | **10/10** |

**Consequence:** full analysis permitted — levels, patterns, R:R and a verdict.

## 3. Element Inventory

**Visible:** ~180 daily candles; volume panel; 20 & 50 EMA (labelled); RSI(14) sub-panel with the value 58.4
printed; no drawings.

**Unreadable:** exact volume bar heights (no volume axis labels) — ratios can be described qualitatively only.

**Absent:** weekly/monthly charts, ADX, ATR, pivot levels, news/event information, option chain.

## 4. Market Structure

| Item | Reading |
|------|---------|
| Prior trend | Uptrend since the October low (higher lows, 3 in sequence) |
| Swing sequence | 3 higher highs, 3 higher lows, no lower low broken |
| Swing definition | k = 3 (this chart is noisy at k = 2) |
| Current leg | Pullback from 1,312 into the 20-EMA, currently 1,248.6 |
| Regime | **Trending up, normal volatility** |
| Regime evidence | Price above a rising 50-EMA; 20-EMA above 50-EMA; price above the 20-EMA midline for 6 of the last 10 bars; swing structure unbroken |

**Level map**

| Price | Type | Touches | Approx? | Note |
|-------|------|---------|---------|------|
| 1,312 | Resistance | 2 | yes | Prior swing high; also a round-ish number |
| 1,285 | Resistance (minor) | 2 | yes | Intraday supply from the last leg |
| 1,232 | Support | 3 | yes | Higher low of the current pullback + 20-EMA confluence |
| 1,198 | Support | 2 | yes | Prior higher low; the structural invalidation for the trend |
| 1,150 | Support (major) | 4 | yes | The base of the October advance |

All levels are approximate: they are interpolated from the axis, not printed as exact prices.

## 5. Candle & Chart Pattern Findings

| Pattern | Bar/period | Status | Rules met | Rules failed |
|---------|-----------|--------|-----------|--------------|
| Bullish engulfing | last bar | **CONFIRMED** | prior bar bearish; current bar bullish; body engulfs; range > 0.8× the 10-bar average; appears after a 4-bar decline | none |
| Bullish flag (higher timeframe read) | last 9 bars | **DEVELOPING** | tight consolidation after an advance; volume contracting | breakout has **not** occurred; volume on the break must be ≥1.3× average |

Note the difference: a confirmed candle pattern is a *bar-level* fact. The flag is a *developing* structure with no
trigger yet. They are not the same kind of evidence, and combining them does not double the confidence.

**Confirmation hierarchy applied:** higher-timeframe context (uptrend intact) > location (support cluster at
1,232–1,240) > candle shape (engulfing) > volume (below average on the reversal bar — a weakness).

## 6. Indicator Readings

| Indicator | Period | Value | Source | Reading | Limitation |
|-----------|--------|-------|--------|---------|-----------|
| EMA | 20 | ~1,241 (visually) | printed label only, value approximate | price above it | approximate |
| EMA | 50 | ~1,186 (visually) | printed label only | rising | approximate |
| RSI | 14 | 58.4 | printed | above 50, below 70 — bullish but not overbought | single timeframe |

**Independent evidence classes represented:** trend (2 MAs = one class), momentum (RSI), volume (panel), levels
(level map) → **4 classes**, but trend and momentum are both derived from the same price series, so treat the real
independence as ~3.

## 7. Volume & Participation

- Volume panel present, **no axis**, so only relative statements are permitted.
- The reversal bar's volume looks *below* the recent average — the reversal lacks conviction.
- The prior advance showed expanding volume, then contraction during the pullback. That is a normal, healthy
  pattern (contraction in a pullback), but it is not confirmation of a new leg up.

## 8. Scenarios

### Scenario A — Bullish continuation (preferred)
- **Trigger (exact):** a daily **close** above 1,268 (the top of the last two bars).
- **Entry zone:** 1,268–1,275 (a retest of 1,268 is acceptable and preferable).
- **Invalidation:** a daily close below **1,228** — that breaks the higher low *and* the 20-EMA together.
- **T1 1,300** (structure: the 1,285 minor resistance, with room) · **T2 1,312** (prior high) ·
  **T3 1,340** (measured move: the 1,232→1,198 base projected).
- **R:R to T1:** from 1,271 entry with a 1,228 stop (risk 43): (1,300 − 1,271)/43 = **0.67R** — *fails the 1.5R
  gate*. From a 1,268 entry: (1,300 − 1,268)/40 = **0.80R** — still fails.
- **What would make this fail:** the reversal bar came on low volume; the 1,285 supply is close above; the
  measured move to T2 is only 1.0R.

### Scenario B — Bearish failure
- **Trigger:** a daily close below **1,228**.
- **Entry zone:** 1,225–1,228 on a retest from below.
- **Invalidation:** a daily close back above 1,244.
- **T1 1,198**, **T2 1,175**, **T3 1,150**.
- **R:R to T1:** (1,226 − 1,198)/(1,244 − 1,226) = 28/18 = **1.56R** — passes, marginally.
- **What would make this fail:** the 50-EMA is rising just below at ~1,186, which is a natural bounce zone; and a
  close below 1,228 after a low-volume pullback can be a shakeout rather than a reversal.

### Scenario C — No trade
- **What "nothing happens" looks like:** price chops between 1,232 and 1,285 for several sessions, with the
  engulfing high and low both holding.
- **Why standing aside is correct:** the bullish case pays only 0.8R to the first real level, and the bearish case
  requires a break that has not happened. Neither offers a favourable risk-reward at the current price.

## 9. Verdict & Risk

| Field | Value |
|-------|-------|
| **Verdict** | **WAIT — NO CONFIRMED SETUP** |
| Confidence | Weak |
| Failing gate | **G4 (location / R:R):** the bullish scenario pays 0.80R to T1, below the 1.5R minimum, because the entry is 45 points below the first real resistance |
| Outstanding confirmation | Either a pullback to 1,240 that gives a tighter stop, or a close above 1,285 that opens room to 1,312 |
| Supporting evidence | Uptrend intact (structure, 3 classes); bullish engulfing confirmed at a support cluster |
| Conflicting evidence | Reversal volume below average; R:R fails; 1,285 supply immediately overhead |
| Preferred scenario | **C** (wait), then A if the entry improves |

**Risk arithmetic (illustrative only):**

```
entry (hypothetical improvement)  = 1,258 (pullback to the 20-EMA)
stop                              = 1,228
risk per unit                     = 30
T1 1,300                          -> (1,300 − 1,258)/30 = 1.40R   (still under 1.5 -> would still be WAIT)
T1 1,312                          -> (1,312 − 1,258)/30 = 1.80R   (only if 1,300 is cleared)
cost estimate 12 bps round trip   -> 0.0012 × 1,258 / 30 = 0.05R
net R at 1,312                    = 1.80 − 0.05 = 1.75R
break-even win rate               = loss / (loss + win)
                                  = 1.05 / (1.05 + 1.70) = 38.2%
```

Check the arithmetic every time. A break-even win rate that "feels" wrong usually is: the formula is
`(1 + cost_R) / ((R − cost_R) + (1 + cost_R))`, and the denominator is a sum of R, not a single R.

```
illustrative size (equity 1,000,000, 0.75%):
  risk budget = 7,500
  units       = floor(7,500 / 30) = 250
  notional    = 250 × 1,258 = 314,500  (31.5% of equity)
```

## 10. Limitations & Disclosure

- **Missing data:** weekly chart, ADX, ATR, volume axis, event calendar, delivery/volume data, option chain.
- **Assumptions:** all levels are axis-interpolated; the EMA values are read visually; the market is assumed to be
  NSE; the session close is assumed to be 15:30 IST.
- **Staleness effect:** the data is post-close, so all levels are valid for the *next* session only.
- **What would change the verdict:** a close above 1,285 with volume ≥1.3× average (turns A into a valid plan); a
  close below 1,228 (turns B into the active scenario); a scheduled event inside 5 sessions (forces NO-TRADE).
- **Not checked:** news, results, delivery data, sector context, higher timeframes.
- **Disclaimer:** educational analysis of a fictional instrument. Not investment advice. No order placed.

## 11. Beginner Explanation (Hinglish)

**Kya dikh raha hai:** price lambi chadhai ke baad thoda neeche aaya hai, aur 20-day average ke paas ruk raha hai.
Aakhri candle bullish engulfing hai — matlab buyers ne wapas control liya, lekin **volume kam** tha.

**Levels:** upar 1,285 par supply hai, uske baad 1,312. Neeche 1,232 par support hai; 1,228 ke neeche daily close
aaya to uptrend ka structure toot jayega.

**Plan A (bullish):** 1,268 ke **close** ke baad entry, stop 1,228 ke neeche, target 1,300/1,312/1,340.

**Problem:** entry 1,268 se T1 1,300 tak sirf **0.8R** banta hai. Rule kehta hai kam se kam **1.5R** chahiye.
Isliye plan accha lag raha hai par **paisa nahi ban raha**.

**Isliye verdict: WAIT.** Wait ka matlab "kuch nahi hoga" nahi — matlab **abhi risk-reward theek nahi hai**.

**Kab interested honge:** ya price 1,240 tak pullback kare (stop chhota hoga, R:R sudhrega), ya 1,285 ke upar
volume ke saath close ho (naya room khulega).

**Invalidation yaad rakho:** 1,228 ke neeche daily close = poora bullish idea cancel.

## 12. Learning Note

- **Concept:** an excellent-looking setup can still be an unexecutable trade. Location and R:R decide, not the
  pattern's name.
- **Mistake this chart punishes:** buying the engulfing candle at 1,250 because it "looks strong", with the first
  resistance 35 points away.
- **Drill:** take five charts, find the nearest resistance above the last close, and compute R:R to it before
  looking at any pattern. Repeat until it is automatic.
