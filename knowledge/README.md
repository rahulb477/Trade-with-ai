# Knowledge Base

The reference layer. 117 documents, organised by domain. `SKILL.md` §4 routes questions into this tree.

## How to use it

1. **Find the domain** in the table below.
2. **Open that directory's README** — each one explains the domain's vocabulary and reading order.
3. **Then open the specific file.** Reading a directory whole is rarely necessary and burns context.

## Domains

| Domain | Files | What it covers | Start with |
|--------|-------|----------------|-----------|
| [`candlesticks/`](candlesticks/) | 26 | 25 single/multi-bar patterns with explicit rules and status codes | `candlesticks/README.md` |
| [`chart-patterns/`](chart-patterns/) | 17 | Head & shoulders, triangles, wedges, flags, rectangles, cup & handle | `chart-patterns/README.md` |
| [`indicators/`](indicators/) | 20 | 18 indicators + a combination guide | `indicators/README.md` |
| [`price-action/`](price-action/) | 10 | Breakouts, retests, rejections, consolidation, trend continuation/reversal | `price-action/README.md` |
| [`market-structure/`](market-structure/) | 5 | Trend phases, ranges, level mapping, timeframe alignment | `market-structure/README.md` |
| [`smart-money/`](smart-money/) | 9 | BOS, CHoCH, MSS, order blocks, FVGs, liquidity, premium/discount | `smart-money/README.md` (§0 first) |
| [`derivatives/`](derivatives/) | 5 | Open interest, options metrics, option chains, futures basics | `derivatives/README.md` |
| [`risk-management/`](risk-management/) | 5 | Position sizing, stop design, drawdown survival, costs | `risk-management/README.md` |
| [`quantitative-analysis/`](quantitative-analysis/) | 6 | Statistics, expectancy, correlation, Monte Carlo, overfitting | `quantitative-analysis/README.md` |
| [`fundamental-analysis/`](fundamental-analysis/) | 5 | Earnings/events, valuation basics, corporate actions, financial health | `fundamental-analysis/README.md` |
| [`trading-psychology/`](trading-psychology/) | 4 | Cognitive biases, discipline, journaling, losses and tilt | `trading-psychology/README.md` |
| [`education/`](education/) | 5 | Glossary, Hinglish rules, 10 concept lessons, exercises | `education/README.md` |

Plus [`glossary.md`](glossary.md) — the master term list across all domains.

## The vocabulary contract

Certain words have a fixed meaning here. Using them loosely is a defect, not a style choice.

| Term | Fixed meaning |
|------|--------------|
| **Level** | A price zone with ≥2 touches. A single touch is a *line*, not a level. |
| **Support / resistance** | Zones, not prices. State the width. |
| **Breakout** | A **close** beyond the level, not a wick beyond it. |
| **Retest** | A return to a broken level that **holds outside** it. |
| **Trap** | A break followed by a **close back inside**. Evidence-scored 0–6. |
| **Invalidation** | The price event that proves the idea wrong. Always a close, usually structural. |
| **Confirmation** | An independent evidence class agreeing — not a second view of the same data. |
| **Regime** | Trending / ranging / high-vol / squeeze / transitional. Determines which tools apply. |
| **R** | The distance from entry to stop. Every outcome is expressed in multiples of it. |

## Status codes used throughout

`CONFIRMED` · `DEVELOPING` · `POSSIBLE` · `UNCLEAR` · `INSUFFICIENT DATA — NO VALID SETUP` ·
`WAIT — NO CONFIRMED SETUP`

## Reading order for a beginner

```
education/concept-lessons.md        (lessons 1-3)
candlesticks/README.md              (the confirmation hierarchy)
market-structure/README.md          (trend, ranges, levels)
price-action/README.md              (breakouts, retests)
risk-management/position-sizing.md  (the one skill that decides survival)
trading-psychology/losses-and-tilt.md (the one that decides whether you use it)
```

Everything else can be looked up on demand.

## Writing rules for this tree

Every file in `knowledge/` follows the same conventions:

1. **Definition first**, then the simple version, then the technical version, then a worked example, then the
   mistakes.
2. **No borrowed statistics.** If a file cites a base rate, it names the study and the sample. Otherwise it says the
   base rate is not known — which is the honest position for most chart patterns.
3. **No promises.** "Tends to", "is consistent with", "requires confirmation" — never "will".
4. **A stated limitation section.** Every file admits what it cannot tell you.
5. **Cross-links are relative and must resolve** (`scripts/check_links.py`).
