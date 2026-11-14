# Concept Lessons

Full lessons in the mandated five-part structure. Each is self-contained and usable in LEARNING mode.

**Lesson format:** Definition → Simple explanation → Technical explanation → Chart example → Common mistakes →
Practice.

---

## Lesson 1 — What a candlestick actually is

**Definition.** A candlestick summarises four prices (open, high, low, close) for one time interval.

**Simple.** One candle = one round of a fight. The body shows who won; the wicks show how far each side pushed
before losing.

**Technical.** For an interval `t`: `open` = first trade, `close` = last trade, `high`/`low` = extremes. Body =
`|close − open|`; the ratio `body/range` measures conviction (near 0 = doji, near 1 = marubozu). Colour is a
convention: green/white = close > open in most Western themes, but **some Asian themes invert this** — always
verify against price direction.

**Chart example.** A candle with `open 100, high 108, low 99, close 107` has a body of 7, an upper wick of 1, and a
lower wick of 1 — buyers controlled the interval from start to finish.

**Common mistakes.** (1) Reading colour without checking the convention. (2) Assuming the close is the "most
accurate" price — it is only the last one. (3) Treating one candle as a signal.

**Practice.** Take five candles from any chart. For each, compute `body/range` and classify it as doji-like,
marubozu-like, or normal.

---

## Lesson 2 — Support and resistance are zones, not lines

**Definition.** A support/resistance level is a price area where the market has repeatedly reacted.

**Simple.** Think of a price where buyers keep showing up — like a floor that has held a few times.

**Technical.** A level needs ≥2 touches to be "established" and ≥3 to be "strong". Levels are zones with width
(typically 0.3–0.5 ATR) because participants use slightly different reference prices. **Levels weaken with over-
testing**: the 6th test of support usually breaks, because the orders defending it have been consumed.

**Chart example.** Support at 1,196–1,204, tested on three dates, each producing a rejection of ≥1 ATR. A fourth
test that closes below 1,196 means the zone was consumed.

**Common mistakes.** (1) Drawing a line through a single wick and calling it a level. (2) Ignoring that levels
expire. (3) Placing a stop exactly at the level.

**Practice.** Mark every level with ≥2 touches on one chart. Count the touches. Then note how many of them were
broken on the next test.

---

## Lesson 3 — Breakout vs fakeout

**Definition.** A breakout is a **close** beyond a level after compression. A fakeout is a move beyond a level
that reverses back.

**Simple.** Breakout = price actually committed to the new area. Fakeout = price stuck a toe out and ran back in.

**Technical.** Confirmation requires: a close beyond the level (not a wick), volume ≥1.3–1.5× the 20-bar average,
follow-through on the next bar, and ideally a retest that holds. Space above matters: <1 ATR to the next
resistance makes a breakout untradeable regardless of quality.

**Chart example.** A range 480–510. A close at 512 on 2.1× volume, then a retest at 509 that holds → a high-quality
breakout. A close at 511 on 0.8× volume, then a close back at 505 → a fakeout.

**Common mistakes.** (1) Counting a wick. (2) Ignoring volume. (3) Buying a breakout into overhead resistance.
(4) Chasing a breakout that has already run 2+ ATR.

**Practice.** Find three historical breakouts and three fakeouts. Record volume multiple, distance to the next
resistance, and whether a retest occurred. Tabulate.

---

## Lesson 4 — Why your stop-loss is not a guarantee

**Definition.** A stop-loss is an instruction to exit at a price; it is not a promise of that price being
available.

**Simple.** A stop is a request, not a guarantee. If the market gaps past it, you get the worse price.

**Technical.** Stops fill at the next available price. Gaps (overnight, earnings, macro) can skip over the stop
entirely. Circuit limits can lock price with no fill at all. Therefore planned risk ≠ maximum risk; the stop
bounds the *planned* loss only.

**Chart example.** A stop at 1,186 with an overnight gap opening at 1,161 → the realised loss is 43 points, not 18.

**Common mistakes.** (1) Sizing as if the stop were exact. (2) Holding through results with a normal stop. (3)
Widening a stop after entry.

**Practice.** Find three historical gaps larger than 3% on any stock. Note how far past a hypothetical stop the
open occurred. Use the average to inform a "gap haircut" for your sizing.

---

## Lesson 5 — Position sizing in one formula

**Definition.** `units = (equity × risk%) ÷ (entry − stop)`.

**Simple.** Decide how much you are willing to lose; divide it by the loss-per-share to get the number of shares.

**Technical.** Always round **down**. Then check **notional** (`units × entry`) against an exposure ceiling —
a tight stop can produce an enormous notional. Also check liquidity (`units ≤ 1% of average daily volume`). For
volatility-adjusted sizing use `stop = k × ATR` (k = 1.5–2.5).

**Chart example.** Equity 500,000, risk 0.5% = 2,500. Entry 1,204, stop 1,186 → risk/share 18 → 138 shares,
notional 166,152 (33% of equity). Acceptable only if the single-name ceiling allows it.

**Common mistakes.** (1) Fixed share quantity regardless of volatility. (2) Rounding up. (3) Ignoring notional.
(4) Widening the stop to make the size "work".

**Practice.** Compute size and notional for the same idea at 0.25%, 0.5% and 1% risk. Note which breaches the
notional ceiling.

---

## Lesson 6 — Trend vs range (and why the tool depends on it)

**Definition.** A trend has a direction (HH/HL or LH/LL); a range does not (overlapping swings).

**Simple.** In a trend, follow. In a range, do not fight the edges.

**Technical.** Classify with four markers: swing structure, ADX (>25 trend, <20 range), 50-EMA slope, price
behaviour relative to Bollinger bands. Trend tools (MA pullbacks, Supertrend) fail in ranges; range tools
(oscillator extremes, band fades) fail in trends.

**Chart example.** ADX 13, flat 50-EMA, price crossing the 20-EMA seven times in 20 bars → range. Fade the
boundaries, do not buy breakouts.

**Common mistakes.** (1) Classifying from one measure. (2) Never updating the classification. (3) Using an
oscillator's "overbought" as a short signal in a strong trend.

**Practice.** Classify five charts with the four-marker method. For each, write one tool you would use and one you
would avoid.

---

## Lesson 7 — What R means and why it matters

**Definition.** `R` is one unit of risk: the distance from entry to stop.

**Simple.** If your stop is 20 points away, then 20 points = 1R. A 40-point gain = 2R.

**Technical.** Measuring in R makes results comparable across instruments, prices and sizes. Expectancy is
`E = p × avg_win_R − (1−p) × avg_loss_R`. Break-even win rate for a target of `b` R is `1/(1+b)`. Costs must be
converted to R (`cost/risk_per_unit`) before judging a setup.

**Chart example.** Entry 1,204, stop 1,186 (1R = 18). Targets at 1,213 (0.5R), 1,232 (1.56R), 1,250 (2.56R). The
first target is not worth taking.

**Common mistakes.** (1) Measuring profit in currency only. (2) Ignoring costs. (3) Taking a 0.5R target because
it "looks close".

**Practice.** Take five historical setups. Compute R for each and the realised outcome in R. Compute expectancy.

---

## Lesson 8 — Indicators are derived, not additional

**Definition.** Every indicator is a mathematical transformation of price and/or volume.

**Simple.** An indicator cannot know something the price chart does not already contain.

**Technical.** Because indicators are functions of the same inputs, many are highly correlated (RSI, Stochastic,
CCI). Counting them separately inflates apparent confirmation. Independent evidence classes: structure, candle
formation, volume, momentum, volatility, higher timeframe, derivatives, news.

**Chart example.** "RSI is oversold, Stochastic is oversold, CCI is oversold" = one momentum observation, repeated
three times.

**Common mistakes.** (1) Stacking same-family indicators. (2) Using an indicator as a sole trigger. (3) Inventing
an indicator value not printed on the chart.

**Practice.** List every indicator on a chart you use. Group them by family. Count how many *independent* classes
you actually have.

---

## Lesson 9 — Why "WAIT" is a decision

**Definition.** WAIT means the available evidence does not clear the entry checklist.

**Simple.** Not trading is a position. It costs nothing and preserves the option to trade later.

**Technical.** WAIT applies when: location is mid-range, R:R < 1.5 to the first valid target, the trigger has not
occurred, timeframes conflict, or a trap is unrefuted. Producing a manufactured setup in these conditions
converts a non-edge into a negative-expectancy trade after costs.

**Chart example.** Price at 492 inside a 480–505 range. Stop at 478 → risk 14. T1 at 505 → 13 points = 0.93R.
Verdict: WAIT until a boundary is tested with confirmation.

**Common mistakes.** (1) Treating WAIT as a failure to answer. (2) Forcing a direction to seem useful.
(3) Re-entering repeatedly in the same chop.

**Practice.** Take three historical situations where no setup existed. Write the WAIT verdict with the specific
failing condition for each. Then check what happened — and note that "nothing happened" was the correct outcome.

---

## Lesson 10 — Reading news without being misled

**Definition.** News moves prices through *surprise relative to expectations*, not through absolute quality.

**Simple.** A good result that is worse than expected still pushes the price down.

**Technical.** Requires: the consensus, the actual, the guidance, and the timestamp. Also requires knowing whether
the news is already priced in (if it is >1 session old and the stock has moved, the market has voted). Single-
source material claims must be cross-checked or marked unverified.

**Chart example.** Results: revenue +9% vs consensus +12% → a miss on expectations despite growth. Guidance cut →
the stock gaps down 7%, invalidating every pre-event technical level.

**Common mistakes.** (1) Reading "profit up 20%" as bullish without the consensus. (2) Using old news as if it were
current. (3) Buying because the news is good, ignoring a clear technical invalidation.

**Practice.** Take one recent earnings reaction. Find consensus, actual, guidance, and the price reaction. Explain
the reaction in one sentence using the surprise, not the absolute numbers.
