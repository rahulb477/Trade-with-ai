# Earnings and Event Risk

## 1. Why events matter for a chart analysis

Technical structure is built from continuous trading. An earnings release replaces continuous trading with a
**jump**. This has three consequences:

1. **Stops are not floors.** A gap through the stop fills at the open, potentially far worse.
2. **Levels are rebuilt.** A 12% gap makes every prior level on the wrong side of the gap mostly irrelevant.
3. **Volatility regime changes.** Implied and realised volatility both spike around results.

## 2. The earnings event, mechanically

| Element | What to know |
|---------|--------------|
| Announcement date/time | Board meeting notice; companies publish in advance. In India, results are typically announced after market hours |
| Consensus estimate | Revenue, EBITDA, PAT expectations |
| Actual vs consensus | The "surprise" — the primary driver of the reaction |
| Guidance | Often more important than the reported quarter |
| Management commentary | Margins, demand, capacity, order book |
| Call timing | The earnings call can move the stock further |

**Never state an earnings date from memory.** Verify from the exchange filing or the company's investor-relations
page, and timestamp it. Dates move.

## 3. The surprise mechanics

```
surprise = (actual − consensus) / |consensus|
```

| Situation | Typical reaction |
|-----------|------------------|
| Beat + raise guidance | Strong gap up |
| Beat + cut guidance | Often a gap down — guidance dominates |
| Miss + raise guidance | Mixed; can go either way |
| In line + in line | Low volatility; attention shifts to the call |
| Large one-off item | The "adjusted" number matters more than the reported one |

Key insight: **the reaction is to the surprise relative to expectations, not to the absolute result.** A company
can report record profit and fall 8% if the market expected more.

## 4. Pre-event decision framework (educational)

```
Option A: flat into the event
  - avoids gap risk entirely
  - forgoes any event-driven gain
Option B: hold with reduced size
  - size such that a plausible gap (use the historical distribution of post-results gaps
    for this stock, if you have it) stays within the risk budget
Option C: hold full size
  - the event is the thesis
  - accepts that the stop may not limit the loss
```

The honest statement: **an event-holding position's risk is not defined by the stop.** Say so explicitly.

If you do not have the historical gap distribution, you cannot quantify the risk; say "unquantified but material"
rather than inventing a number.

## 5. Other scheduled events with the same character

| Event | Market |
|-------|--------|
| RBI MPC decision | India (indices, banks, rate-sensitives) |
| Union Budget | India (broad) |
| CPI / IIP / WPI releases | India |
| F&O expiry | India (weekly and monthly; verify schedule) |
| Index rebalancing / MSCI review | India and global |
| Fed decision, CPI, payrolls | US and global |
| OPEC+ meetings | Commodities |
| Halving / protocol upgrades | Crypto |
| Election results | Any |

Each of these belongs in the event-risk gate (`core/decision-engine.md` G2).

## 6. How to report event risk

```
Event            : Q2 FY26 results
Expected date    : 2026-11-18, after market hours (source: exchange filing dated 2026-11-04)
Consensus        : revenue growth ~9% YoY, margin ~18% (source: <provider>, retrieved 2026-11-14)
Relevance        : inside the intended 2-week holding horizon
Risk assessment  : a 5-12% overnight gap is plausible for this name; I do not have the historical
                   gap distribution for this stock, so this range is an estimate, not a measurement.
Recommendation   : this is a risk-management statement, not advice — a position size that assumes
                   a 12% gap would need to be roughly 1/3 of a position sized on a normal 2% stop.
```

## 7. Common errors

| Error | Guard |
|-------|-------|
| Quoting an earnings date without a source | Verify and timestamp |
| Assuming a good result means a gap up | Guidance dominates |
| Trading through results with a normal stop | Gap risk makes the stop unreliable |
| Confusing reported vs adjusted figures | State which |
| Ignoring the earnings call | It moves prices |
| Using a stale consensus | Timestamp it |

## 8. Beginner summary (Hinglish)

**Result ke din chart badal jata hai.** Price ek gap ke saath khulta hai — aapka stop wahan kaam nahi karta.

**Kya dekha jata hai:** sirf profit nahi — **expectations se comparison** (surprise), aur **guidance**.
Achha result + kamzor guidance = stock gir sakta hai.

**Sabse important:** agar aap result hold kar rahe ho, to **size kam** karo. Kyunki 1R ka planned loss 5R ban
sakta hai.

**Date yaad se mat likho** — exchange filing se verify karo.

**Baaki events:** RBI policy, budget, expiry, Fed — sab gap risk laate hain.

## 9. Exercise

Find the next results date for one stock (from a filing, with the source). Find the last four post-results
one-day moves. Compute the average absolute gap. Then compute what position size keeps a 2× that gap inside a 1%
risk budget. Write down the number and the assumption you made.

---
*See also: [`corporate-actions.md`](corporate-actions.md) · [`../core/decision-engine.md`](../../core/decision-engine.md) §3 G2*
