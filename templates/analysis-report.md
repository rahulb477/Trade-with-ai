# Analysis Report Template

> **Instructions.** Fill every section. Sections 1–3 are facts, 4–7 are analysis, 8–9 are plans, 10 is disclosure.
> Delete no headings. Where a value is unknown, write `unknown` and say what would be needed.

---

## 1. Data & Provenance

| Field | Value |
|-------|-------|
| Instrument | |
| Exchange / venue | |
| Asset class | |
| Timeframe(s) analysed | |
| Other timeframes shown | |
| Chart type | candlestick / OHLC bar / line / other |
| Data source | screenshot / provider:<name> / user transcription |
| Data timestamp | (with timezone) |
| Analysis timestamp | (with timezone) |
| Freshness class | LIVE / RECENT / DELAYED / STALE / HISTORICAL |
| Last price | |
| Mode | LEARNING / RESEARCH / PAPER-TRADING |
| Data mode | offline / web research / market-data integration / full research |

## 2. Chart Quality Score

| Dimension | Present? | Weight |
|-----------|----------|--------|
| Instrument identifiable | | 2 |
| Timeframe visible | | 1 |
| Price axis readable | | 2 |
| Volume present | | 1 |
| Indicators labelled | | 1 |
| Candles clear | | 2 |
| Axes not distorted | | 1 |
| **Total** | | **/10** |

**Consequence of this score:** (full analysis / no precise levels / qualitative only / stop)

## 3. Element Inventory

**Visible:** candles (~n), volume panel, indicators (list with periods), drawings (trendlines, levels, Fib).

**Unreadable:** ...

**Absent:** ... (each absence becomes a limitation in §10)

## 4. Market Structure

| Item | Reading |
|------|---------|
| Prior trend | |
| Swing sequence | (HH/HL count, LH/LL count) |
| Swing definition | k = 2 / 3 / 5 |
| Current leg | |
| Regime | trending / ranging / high-vol / squeeze / transitional |
| Regime evidence | (ADX, MA slope, BB walk, swing structure) |

**Level map** (resistance first; each with touch count):

| Price | Type | Touches | Approx? | Note |
|-------|------|---------|---------|------|
| | | | | |

## 5. Candle & Chart Pattern Findings

| Pattern | Bar/period | Status | Rules met | Rules failed |
|---------|-----------|--------|-----------|--------------|
| | | CONFIRMED / DEVELOPING / POSSIBLE / UNCLEAR | | |

**Confirmation hierarchy applied:** (higher-TF context > location at a level > candle shape > volume)

## 6. Indicator Readings

| Indicator | Period | Value | Source | Reading | Limitation |
|-----------|--------|-------|--------|---------|-----------|
| | | | printed / computed | | |

**Independent evidence classes represented:** trend / momentum / volatility / volume / levels → count: ___

## 7. Volume & Participation

| Item | Reading |
|------|---------|
| Volume panel present | |
| Last bar vs 20-bar average | |
| Breakout/breakdown volume ratio | |
| Climax or exhaustion evidence | |
| Divergence | |

## 8. Scenarios (all three mandatory)

### Scenario A — Bullish
- **Trigger (exact):**
- **Entry zone:**
- **Invalidation (price + what it means):**
- **T1 / T2 / T3:**
- **R:R to T1:**
- **What would make this fail:** (trap audit)

### Scenario B — Bearish
- Same fields.

### Scenario C — No-trade / range continuation
- **What "nothing happens" looks like:**
- **Why standing aside is correct here:**

## 9. Verdict & Risk

| Field | Value |
|-------|-------|
| **Verdict** | BULLISH SCENARIO / BEARISH SCENARIO / WAIT — NO CONFIRMED SETUP / NO-TRADE / INSUFFICIENT DATA — NO VALID SETUP |
| Confidence | Strong / Moderate / Weak / Speculative / Not assessable |
| Failing gate (if WAIT/NO-TRADE) | |
| Outstanding confirmation | |
| Supporting evidence | (each with provenance class) |
| Conflicting evidence | |
| Preferred scenario | A / B / C |

**Risk arithmetic (illustrative only):**

```
risk per unit      = |entry − stop| = ...
illustrative size  = equity 1,000,000 × 0.75% ÷ risk_per unit = ... units
notional           = ... ( ... % of equity )
cost_R             = ... bps round trip → ... R
break-even win rate= ...
```

**Hard prohibitions restated:** this is not advice; no order was placed; the size is illustrative arithmetic.

## 10. Limitations & Disclosure

- Missing data: (every `unknown` from above)
- Assumptions made: (`ASSUMED` default periods, approximate levels, assumed market)
- What would change the verdict:
- Data staleness effect:
- What was **not** checked: (news, fundamentals, higher timeframes not shown, option chain)
- Standing disclaimer: educational analysis, not investment advice, no real-money execution.

## 11. Beginner Explanation (Hinglish)

> 150–300 words, in the structure from `knowledge/education/hinglish-explanations.md`.
> Keep English trading terms in English. Numbers identical to the English section. Never promise a direction.
> Always name the invalidation. Never use "pakka", "sure shot", or unsourced win rates.

## 12. Learning Note (optional, LEARNING mode)

- One concept this chart demonstrates:
- One mistake this chart would punish:
- One drill to practise:
