# India — Sessions and Holidays

## 1. Session timeline (NSE/BSE equities)

| Window | Time (IST) | Notes |
|--------|-----------|-------|
| Pre-open order entry | 09:00 – 09:08 | Order collection |
| Pre-open matching | 09:08 – 09:15 | Indicative price discovery |
| **Continuous trading** | **09:15 – 15:30** | Normal session |
| Closing price calculation | ~15:30 – 15:40 | Weighted average of the last 30 minutes |
| Post-close (block/bulk) | 15:40 – 16:00 | Limited window |
| Currency derivatives | 09:00 – 17:00 | Different window |
| Commodity (MCX, where applicable) | Roughly 09:00 – 23:30 | Verify per contract |

**Always verify current timings** from the exchange. Timings have changed historically (e.g. market opening was
earlier before 2010).

## 2. What this means for chart analysis

| Consequence | Detail |
|-------------|--------|
| One trading day = 375 minutes | A daily candle spans 09:15–15:30, not 24 hours |
| Intraday bars | A 5-minute chart has 75 bars per session |
| The first 15 minutes are noisy | Opening auction effects; volume spikes |
| The last 15 minutes are noisy | Closing price calculation and position squaring |
| The "lunch lull" | ~12:00–13:30 often shows lower volume; breakouts then are less reliable |
| Overnight gaps are real | The session is closed overnight; gap risk exists |
| Weekly candle = 5 sessions | Holidays create short weeks |

## 3. Holidays

- The exchange publishes a holiday list each year (typically 14–18 trading holidays plus weekends).
- **Never assert a holiday from memory.** Check the exchange list.
- Effect on analysis: a "missing" candle in a continuous series may be a holiday, not a data error. A weekly candle
  covering a holiday week has fewer bars — volume comparisons across weeks must account for this.
- Special sessions (e.g. Muhurat trading) exist on some years — verify.

## 4. Special sessions and events

| Event | Effect |
|-------|--------|
| **Muhurat trading** | A short evening session on Diwali; volume is unusual, often thin |
| **Budget day** | Often a Saturday or a special session; extreme volatility |
| **Election result days** | Counting-day volatility; sometimes special sessions |
| **Expiry days** | Weekly/monthly derivative expiries; see `derivatives.md` |
| **Half-day sessions** | Rare, but announced by the exchange |

## 5. Timezone discipline

All timestamps in a report must carry a timezone. Use `IST` (UTC+5:30). If the user is elsewhere, give both.

```
Wrong: "the stock closed at 1,204"
Right: "the stock closed at 1,204 on 2026-11-14 (NSE, 15:30 IST)"
```

## 6. Session boundaries and indicator behaviour

Indicators computed across session boundaries behave differently from those reset per session:

| Indicator | Behaviour |
|-----------|-----------|
| VWAP | Resets at the session open (standard) — crossing the boundary without a reset is wrong |
| Volume profile | Usually session-scoped |
| Pivot points | Derived from the prior session |
| ATR on intraday | Includes the overnight gap in the true range |
| Daily ATR | Includes only the session range plus gaps between days |

## 7. Common errors

| Error | Guard |
|-------|-------|
| Using 09:30–16:00 (US hours) for an Indian chart | Indian session is 09:15–15:30 IST |
| Asserting a holiday without checking | Verify the exchange list |
| Comparing weekly volume across a holiday week | Normalise per session |
| Treating a Muhurat candle as a normal day | It is not |
| Forgetting the timezone | Always state IST |
| VWAP across multiple days without a reset | Reset per session |

## 8. Hinglish summary

**Indian market timing:** 09:15 se 15:30 IST. Pehle 15 minute aur last 15 minute noisy hote hain.

**Holiday:** exchange ki list se check karo, yaad se mat bolo. Holiday wale week mein volume kam hota hai — usko
normal week se compare mat karo.

**VWAP** har session start par reset hota hai — multiple days par bina reset use karna galat hai.

**Timestamp mein IST likho.** "Close 1,204" nahi — "close 1,204, 15:30 IST".
