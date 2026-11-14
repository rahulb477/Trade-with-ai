# Valuation Basics (and Their Traps)

Not a valuation course — enough to read a multiple correctly and to avoid the standard mistakes.

## 1. The common multiples

| Multiple | Formula | Best for | Trap |
|----------|---------|----------|------|
| **P/E** | price / EPS | Stable, profitable companies | Meaningless for loss-making firms; distorted by one-offs |
| **Forward P/E** | price / estimated EPS | Growth expectations | Depends entirely on the estimate's quality |
| **EV/EBITDA** | (market cap + net debt) / EBITDA | Capital-intensive, cross-border comparisons | EBITDA ignores capex and interest — flatters debt-heavy firms |
| **P/B** | price / book value | Banks, financials | Book value can be stale or intangible-light |
| **EV/Sales** | EV / revenue | Early-stage, unprofitable | Ignores profitability entirely |
| **Dividend yield** | DPS / price | Income strategies | A high yield can signal a falling price, not generosity |
| **PEG** | P/E / growth rate | Growth comparison | Assumes growth is durable and linear |

## 2. The three rules of multiples

1. **A multiple is a ratio, not a verdict.** A P/E of 40 is not "expensive" without a growth rate and a peer set.
2. **Compare like with like.** Same sector, same accounting standards, same currency, same period.
3. **The denominator matters more than the numerator.** Always check which EPS/EBITDA figure is used: reported,
   adjusted, trailing, forward, consolidated, standalone.

## 3. The traps

| Trap | Explanation |
|------|-------------|
| **Sector-blind comparison** | A 15 P/E is cheap for a software firm, expensive for a utility |
| **Trailing vs forward confusion** | "Cheap on forward" is a statement about forecasts |
| **One-off distortions** | A large asset sale can halve P/E for one year |
| **Negative earnings** | P/E is undefined; do not report it as "0" or "infinity" |
| **Cyclical peaking** | Low P/E at a cyclical top is a warning, not a bargain (earnings are about to fall) |
| **Survivorship in peer sets** | Comparing to peers that exist today |
| **Currency mismatch** | Comparing an ADR multiple to a local one without adjustment |
| **Restatement** | Using restated figures for a historical analysis |

## 4. The one genuinely useful fundamental question for a chart trader

Not "is it cheap?" but: **"is there a scheduled catalyst that will change how this stock trades?"**

| Catalyst | Effect on the chart |
|----------|---------------------|
| Results | Volatility spike, gap risk, level reset |
| Guidance change | Trend change potential |
| Index inclusion/exclusion | Forced flows |
| Promoter/insider activity | Sentiment |
| Regulatory action | Tail risk |
| Capacity expansion / order wins | Structural re-rating potential |

These are **event facts**, verifiable from filings, and they belong in the report's context section with a date.

## 5. What this repository will not do

- Produce a DCF or a target price. That requires assumptions (growth, discount rate, terminal value) that cannot be
  validated from a chart, and presenting a single target price would imply false precision.
- Call a stock "undervalued" without a stated method, peer set and period.
- Use valuation to override a technical invalidation. A cheap stock can fall 40%.

## 6. Report template

```
Context (fundamental)
  Latest results      : Q2 FY26, revenue +9% YoY, PAT +4% YoY (source: filing 2026-11-12)
  Multiple            : trailing P/E 22.4 vs 5-year median 19.8 (source: <provider>, 2026-11-14)
  Debt                : net debt/EBITDA 1.4x (source: Q2 FY26 filing)
  Upcoming catalysts  : results for Q3 due late Jan (date unconfirmed — verify)
  Relevance to chart  : no catalyst inside the 2-week horizon; valuation is a background fact,
                        not a driver of the next 5 sessions.
```

## 7. Common errors

| Error | Guard |
|-------|-------|
| "Cheap" without a comparison | State the peer set and period |
| Quoting a P/E without saying which EPS | Trailing/adjusted/forward |
| Using valuation as a trade trigger | It is background context |
| Ignoring that a low P/E can mean peaking earnings | Check the cycle position |
| Fabricating a target price | Do not produce one |
| Mixing consolidated and standalone | Say which |

## 8. Beginner summary (Hinglish)

**P/E** = price ÷ EPS. Matlab market ek rupee ke profit ke liye kitna de raha hai.

**Sabse badi galti:** P/E ko akela dekhna. 40 ka P/E high-growth company ke liye normal ho sakta hai, aur 15
utility ke liye mehnga.

**Hamesha compare karo:** same sector, same period, same type ka EPS (trailing ya forward).

**Chart trader ke liye asli sawal valuation nahi hai:** "koi **event** aa raha hai jo is stock ka behaviour badal
dega?" Results, guidance, index inclusion, regulation — yeh matter karte hain.

**Yeh repo target price nahi degi.** Kyunki DCF ke assumptions verify nahi ho sakte, aur ek number dena false
precision hai.

## 9. Exercise

Take two companies in the same sector. Look up trailing P/E, forward P/E estimate, EV/EBITDA, and net debt/EBITDA
from the same source and date. Write down which multiple you trust least and why. Then note whether either stock's
chart has a scheduled catalyst in the next month.

---
*See also: [`financial-health.md`](financial-health.md) · [`earnings-and-events.md`](earnings-and-events.md)*
