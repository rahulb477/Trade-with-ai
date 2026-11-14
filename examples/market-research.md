# Example — Market Research With and Without Web Access

> **FICTIONAL** instrument; the two variants below demonstrate the two data modes. The "with web" variant contains
> **placeholder citations** — a real report must contain actual URLs and timestamps, which this file cannot
> fabricate. Read it as a format, not as evidence.

---

## Variant 1 — Web research unavailable (offline mode)

This is the section that must appear **verbatim in spirit** whenever browsing is not available:

> **Web research unavailable.** I cannot retrieve current news, announcements, FII/DII flows, sector performance,
> index levels, macroeconomic releases, or corporate events for this instrument. Everything below is derived from
> the supplied chart only. Any statement about "why" price moved, about upcoming results, or about market-wide
> context would be fabricated, so none is made. To complete a research-mode analysis, provide: the latest
> exchange announcement page, the sector index performance, and the event calendar for the next 2–4 weeks.

What remains possible in offline mode:

| Analysis | Permitted |
|----------|-----------|
| Structure, levels, patterns from the chart | ✅ |
| Candle and chart-pattern rule audits | ✅ |
| Indicator readings (printed values only) | ✅ |
| Risk arithmetic and position sizing | ✅ |
| Causal explanation of the move | ❌ not available |
| Event risk assessment | ❌ not available |
| Sector relative strength | ❌ not available |
| Index context | ❌ not available |

**Effect on the verdict:** with event risk unknown, size is capped and the report states `event risk: unknown`.
That is not a formality — an unnoticed earnings date is the single most common way a technically valid plan fails.

---

## Variant 2 — Web research available (full research mode)

### 2.1 Index context

| Item | Value | Source | Timestamp |
|------|-------|--------|-----------|
| NIFTY 50 | `<value>` | `<provider/citation>` | `<ISO>` |
| BANK NIFTY | `<value>` | `<citation>` | `<ISO>` |
| Index trend (daily) | `<up/down/range>` | chart or provider | `<ISO>` |

A real report fills these with retrieved numbers. **If the numbers cannot be retrieved, variant 1 applies.**

### 2.2 Sector context

| Item | Value | Source |
|------|-------|--------|
| Sector index 1M/3M/6M return | `<...>` | `<citation>` |
| Benchmark 1M/3M/6M return | `<...>` | `<citation>` |
| Relative strength | outperforming / inline / underperforming | computed from the above |
| Rank change | `<from> → <to>` | `<citation>` |

Reading: *"A long in this name would have sector support / would fight the sector."*

### 2.3 Instrument news (7-field extraction)

| Headline | Publisher | Tier | Published | Event time | Relevance | Impact |
|----------|-----------|------|-----------|------------|-----------|--------|
| `<headline>` | `<publisher>` | A/B/C | `<ISO>` | `<ISO>` | direct | `<direction + one-clause reason>` |

**Every row must be a real, retrieved item.** A row whose `Published` field is blank, or whose URL cannot be
produced on demand, is deleted — not marked "approximately".

### 2.4 Priced-in test

Before treating news as a reason for a trade, ask:

1. Was the information public before the current move began?
2. Did volume expand *after* the news or before it?
3. Is the reaction already extended (e.g. +8% in one session)?

If the move already happened, the news is **context, not a trigger**. Entering after an extended reaction to known
news is buying someone else's exit.

### 2.5 Flow data (India)

| Item | Value | Date | Caveat |
|------|-------|------|--------|
| FII net cash | `<₹ cr>` | `<date>` | end-of-day only; provisional figures are revised |
| DII net cash | `<₹ cr>` | `<date>` | same |

Flows describe who transacted yesterday. They are not a forecast, and a single day's flow is noise.

### 2.6 Event calendar (the risk gate)

| Date | Event | Affects | Action |
|------|-------|---------|--------|
| `<date>` | Quarterly results | this instrument | **NO-TRADE** inside a 3-session window, or half size |
| `<date>` | RBI policy | whole market | reduce size; no new positions on the day |
| `<date>` | Monthly F&O expiry | index + heavyweights | expect erratic intraday behaviour |

**Gate G2:** a binary event before the first target converts the verdict to `NO-TRADE` unless the plan explicitly
accounts for it.

### 2.7 Cross-checks performed

| Claim | Source A | Source B | Outcome |
|-------|----------|----------|---------|
| `<claim>` | `<tier>` | `<tier>` | agreed / unresolved / superseded |

Unresolved conflicts are reported as unresolved and excluded from the verdict.

### 2.8 What this mode changes

| Aspect | Offline | Full research |
|--------|---------|---------------|
| Structural analysis | identical | identical |
| Event risk gate | unknown → capped size | can be cleared or triggered |
| Causal narrative | not attempted | supported by citations |
| Sector context | absent | present with timestamps |
| Confidence ceiling | Weak | up to Strong |

**The technical analysis does not get better with browsing.** Only the context does. A common failure is to treat
fresh news as extra technical evidence — it is not; it is a separate input with its own gate.

---

## Beginner Explanation (Hinglish)

**Do modes hote hain.**

**Offline mode:** sirf chart dekh sakte hain. News, result date, sector — kuch nahi. Isliye report mein saaf likhna
padta hai: **"web research unavailable"**. Guess karke "result aa raha hai" likhna **fabrication** hai.

**Full research mode:** web se news, index, sector, event calendar laa sakte hain. Har cheez ka **source aur time**
likhna padta hai.

**Sabse important:** news milna technical analysis ko **behtar nahi** banata — sirf context deta hai. Aur agar
result 3 din baad hai, to achha setup bhi **NO-TRADE** ban sakta hai.

**Rule:** jo cheez verify nahi kar sakte, use report mein mat likho.
