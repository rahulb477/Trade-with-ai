# Corporate Actions and Chart Artefacts

Corporate actions are the leading cause of **phantom technical patterns**. A "gap" or a "support break" that is
arithmetic, not price action, will produce a completely wrong analysis.

## 1. Actions that change the price series

| Action | Price effect | Chart artefact |
|--------|--------------|----------------|
| **Split** (e.g. 1:2) | Price halves | A 50% "gap down"; all prior levels must be divided |
| **Bonus issue** (e.g. 1:1) | Price halves | Same as a split |
| **Dividend** | Small drop on ex-date | Minor; matters for long-horizon total return |
| **Rights issue** | Price adjusts | Adjusted series required |
| **Buyback** | Price support around the tender | Can distort volume |
| **Merger / demerger** | Structural discontinuity | Historical technicals largely invalid |
| **Symbol change / rebrand** | None | Ticker mismatch across data sources |
| **Face-value split** | Price change | Same as a split |
| **Consolidation / reverse split** | Price multiplies | A huge "gap up" |

## 2. Adjusted vs unadjusted

```
Adjusted price = raw price × cumulative adjustment factor
```

Adjusted series are what you must use for **any** technical analysis crossing an action date. Unadjusted series
are what you want for **actual traded prices** at a point in time (e.g. "the stock closed at ₹1,204 on that day").

| Use | Series |
|-----|--------|
| Pattern/level analysis across an action | Adjusted |
| Order prices, stops, and "what did it actually trade at" | Unadjusted, for the current period |
| Total return | Adjusted (with dividends) |
| Volume analysis across a split | Split-adjusted volume |

**Critical check:** if you cannot tell whether the data you are looking at is adjusted, say so. Never analyse a
support level that is actually a split artefact.

## 3. How to detect an action from the chart alone

Warning signs (not proof):

1. An inexplicable ~50% or ~2× jump with no news.
2. A one-day "crash" followed by normal trading in the new range.
3. Volume spike coinciding with the price jump (often an artefact of share-count changes).
4. Corporate-action calendars showing an ex-date.

Guard: always cross-check a large unexplained move against the exchange's corporate-action announcements. **Never**
call a 50% single-day drop a "bearish engulfing on the daily" before checking.

## 4. Practical procedure

```
1. Before analysing any chart with a big discontinuity, check the corporate-action calendar.
2. If an action occurred, confirm the data series is adjusted. If not, request/construct an adjusted series.
3. If an action is recent (inside the visible window), state it in the report and explain that
   pre-action levels are not comparable.
4. For the current price and stops, use the actual trading price.
```

## 5. Dividend adjustment in India

Indian price series are typically adjusted for dividends by data vendors, but the convention varies. A "support
break" of 0.5% on an ex-dividend date is arithmetic. If a level sits inside the dividend amount and the date
coincides, flag it.

## 6. Mergers and demergers

After a demerger, the parent's historical price refers to a different entity. Technical analysis across the event
is close to meaningless:

- The share count changed.
- The business changed.
- The float may have changed.

Correct handling: draw a **line in time** at the event and analyse only post-event structure, stating that
pre-event history is not comparable.

## 7. Report template

```
Corporate action check
  Large discontinuities in the visible window : none
  Nearest scheduled action                   : Q2 dividend, ex-date 2026-11-06 (source: exchange notice
                                               dated 2026-10-28), impact ~0.4% of price
  Data series                                : assumed adjusted (vendor default); not verified
  Note                                       : the 2026-11-06 support test sits within half the
                                               dividend amount, so that "break" may be arithmetic
```

## 8. Common errors

| Error | Guard |
|-------|-------|
| Analysing a split as a crash | Check the calendar |
| Comparing pre- and post-action levels | Use adjusted data |
| Assuming data is adjusted | Verify, or state the assumption |
| Using adjusted prices as "actual traded" prices | Use raw for orders |
| Missing a demerger discontinuity | Check for large discontinuities |
| Ticker lookup failing after a rebrand | Verify by ISIN, not by ticker |

## 9. Beginner summary (Hinglish)

**Split / bonus:** price aadha ho jata hai — chart par yeh 50% ka **gap down** dikhta hai, par woh crash nahi
hai. Sirf arithmetic hai.

**Isliye:** analysis se pehle corporate action check karo. Agar action hua hai, to **adjusted data** use karo.

**Dividend:** chhota drop ex-date par — 0.5% ka "support break" arithmetic ho sakta hai.

**Merger/demerger:** us event ke pehle ka chart **different company** ka hai. Us line se pehle ke levels ka matlab
nahi.

**Sabse zaroori:** koi bhi 50% ka achanak jump dekho to pehle company action check karo — pattern name dene se
pehle. Aur agar pata nahi ki data adjusted hai ya nahi, to likho: "assumed adjusted, not verified".

## 10. Exercise

Find a stock that had a split or bonus in the last three years. Look at the raw chart around that date. Note how
many "patterns" appear that are pure arithmetic. Then look at the adjusted chart and note what actually happened.
Write one sentence about the risk of analysing unadjusted data.

---
*See also: [`earnings-and-events.md`](earnings-and-events.md) · [`../markets/india/README.md`](../../markets/india/README.md)*
