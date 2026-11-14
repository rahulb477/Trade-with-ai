# Market Context

A chart does not exist in isolation. This module defines *which* context matters, *when* it
matters, and how to gather it without fabricating it.

**Gathering is conditional.** If no browsing or provider access exists, this module is used only
to structure the "not performed" statement in report section 6.

---

## 1. Context layers, outermost first

```
L1  Global risk regime        USD, US 10Y yield, crude, global indices, VIX-type gauges
L2  Domestic macro            policy rates, CPI, GDP, currency, liquidity
L3  Index behaviour           NIFTY 50 / BANK NIFTY / Sensex / S&P 500 level & breadth
L4  Sector rotation           which sectors lead/lag today and over 1M/3M
L5  Instrument specifics      news, results, corporate actions, delivery %, OI
L6  Microstructure            spread, volume profile, order flow (only with real data)
```

Analyse L1→L3 for **index-level or regime questions**; L4→L5 always for single stocks.
L6 only when a genuine data feed exists.

---

## 2. India-specific context playbook

### 2.1 Indices that set the tone

| Index | What it tells you | Typical use |
|-------|-------------------|-------------|
| **NIFTY 50** | Broad large-cap sentiment, the default market benchmark | Overall direction, risk-on/off |
| **BANK NIFTY** | Bank sector = highest weight in NIFTY; most liquid F&O | Intraday volatility, options positioning |
| **FINNIFTY** | Financial services ex-bank (NBFC, insurance, AMC) | Breadth within financials |
| **Sensex** | BSE's 30-stock benchmark | Confirmatory; divergence from NIFTY is usually index-construction, not signal |
| **Midcap / Smallcap 100** | Risk appetite at the tail | Divergence signals narrow or broadening participation |

**Divergence reading:** NIFTY up while BANK NIFTY down usually means non-financials are carrying
the index — narrow leadership. Note it, do not over-interpret a single session.

### 2.2 Flows

| Flow | Published | Interpretation caveat |
|------|-----------|----------------------|
| **FII/FPI cash activity** | Exchange end-of-day | A single day is noise; look at weekly/monthly trend. Derivatives flow is separate from cash flow. |
| **DII activity** | Exchange end-of-day | Often absorbs FII selling (SIP flows). |
| **Delivery percentage** | Exchange end-of-day | High delivery on an up move = positional interest; low = intraday churn. |
| **Bulk/block deals** | Exchange notices | Named counterparties matter more than size alone. |

Report the *date* of every flow figure. "FII bought today" without a date is meaningless after 18:00.

### 2.3 Scheduled events that invalidate technicals

- RBI Monetary Policy Committee decisions and minutes
- Union Budget, GST Council, policy announcements
- CPI / WPI / IIP releases
- Monthly F&O expiry (weekly expiries exist on NIFTY/BANKNIFTY — check the current schedule, it
  changes; see `markets/india/`)
- Quarterly results season (mid-Jan/Apr/Jul/Oct, staggered)
- Index rebalancing and MSCI inclusions
- Election results, geopolitical events

### 2.4 Corporate actions that corrupt a price chart

| Action | Chart effect | Handling |
|--------|--------------|----------|
| Split / bonus | Vertical price jump | Use adjusted data; a "support break" may be arithmetic |
| Dividend | Small drop on ex-date | Usually immaterial intraday, material for long-horizon total return |
| Rights issue | Price adjustment | Adjusted series required |
| Merger/demerger | Structural discontinuity | Historical technicals largely invalid |
| Symbol change / rebrand | Ticker mismatch across sources | Verify ISIN, not the ticker |

---

## 3. International context

| Market | Primary indices | Key macro | Session nuance |
|--------|-----------------|-----------|----------------|
| US | S&P 500, Nasdaq 100, Dow, Russell 2000 | Fed funds, CPI, payrolls, 10Y yield, DXY | Pre-market gaps are normal; extended hours are thin |
| Europe | DAX, FTSE 100, CAC 40, Euro Stoxx 50 | ECB, euro, energy | Lunch break in some exchanges (not DAX/FTSE) |
| FX | DXY, EUR/USD, USD/JPY, USD/INR | Rate differentials, central banks | 24/5; rollover at 17:00 New York |
| Commodities | WTI/Brent, gold, copper, natural gas | Inventories, OPEC+, China demand, real yields | Futures roll creates artificial jumps in continuous series |
| Crypto | BTC, ETH, total market cap | Liquidity, regulation, ETF flows | 24/7 — "overnight gap" is a concept that does not exist |

Cross-market rules of thumb (state them as *tendencies*, never as laws):

- Rising USD and rising US real yields are a headwind for gold and often for EM equities.
- Rising crude is a headwind for India (importer) and a tailwind for exporters of energy.
- US tech weakness often transmits to Indian IT services with a lag and imperfectly.
- A strong dollar typically pressures BTC and other risk assets (correlation is regime-dependent).

**Never assert a correlation without stating the sample and period**, or without citing a
measurement. Correlations are unstable — see `engines/quantitative-intelligence/correlation.md`.

---

## 4. News evaluation protocol

For each item you intend to cite:

1. **Headline** as published (do not paraphrase into something more dramatic).
2. **Publisher** and tier (A/B/C/D per `evidence-engine.md` §3).
3. **Publication timestamp**, with timezone.
4. **Event date** — often different from publication.
5. **Relevance** to this instrument: direct / sector / macro / none.
6. **Expected impact direction and magnitude class**: high/medium/low, positive/negative/ambiguous.
   Justify in one clause ("margin guidance cut ⇒ negative for earnings estimates").
7. **Already priced in?** If the news is >1 session old and the stock has moved, the market has
   already voted; note that.

Red flags requiring you to slow down:

- Headline only, no body content accessible
- Single-source claim about a material event (verify or mark unverified)
- "Reportedly", "sources say" — attributed to anonymous sources
- Recycled/updated article with an old event date
- Press release reprinted as news
- Content behind a paywall that you could not read (do not summarise what you did not read)

---

## 5. What context is *not* allowed to do

| Not allowed | Why |
|-------------|-----|
| Overriding a clear structural invalidation | "Good news" does not stop a stop-loss from being hit |
| Being invented when no tools exist | Fabrication |
| Being used as the sole basis for a direction call | News is often priced in and often ambiguous |
| Justifying a bigger position | Context increases uncertainty as often as it reduces it |
| Being quoted without a timestamp | Stale context is worse than none |

---

## 6. Context sufficiency check

Before writing report section 6, answer:

- [ ] Do I know today's index behaviour, or did I say I cannot check?
- [ ] Is there a scheduled event inside the holding horizon?
- [ ] Is there instrument-specific news, cited with time?
- [ ] Has a corporate action occurred recently that changes the price series?
- [ ] Did I mark every unverifiable item as unverified rather than guessing?

If browsing is unavailable, section 6 reads exactly:

> **Web research unavailable in this environment.** No news, flows, sector or macro context was
> retrieved. The analysis below is technical and structural only. Any event risk — results,
> policy decisions, expiry — is unquantified and must be checked by the reader.

---

*See also: [`../engines/market-intelligence/README.md`](../engines/market-intelligence/README.md) ·
[`../workflows/news-research.md`](../workflows/news-research.md) · [`../markets/`](../markets/)*
