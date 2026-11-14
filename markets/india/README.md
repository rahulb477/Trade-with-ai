# India — NSE and BSE

## 1. Exchanges and instruments

| Exchange | Instruments |
|----------|-------------|
| **NSE** | Equities, indices (NIFTY 50, BANK NIFTY, FINNIFTY, NIFTY MIDCAP 150, etc.), equity derivatives, currency derivatives, commodity derivatives (via NSE IX for some), ETFs |
| **BSE** | Equities (incl. SME), Sensex and other indices, derivatives, currency |

**Ticker conventions:** `SYMBOL` (NSE), `SYMBOL.BO` (BSE), `SYMBOL.NS` (NSE, some data vendors). The same company
trades on both with near-identical prices but different tickers, different liquidity, and sometimes different
circuits. **Never assume which one a chart is from** — check the header suffix or ask.

## 2. Indices

| Index | Composition | Notes |
|-------|-------------|-------|
| **NIFTY 50** | 50 large caps, float-weighted | The benchmark; highest-liquidity derivatives |
| **BANK NIFTY** | 12 major banks | Highest-weight sector; most-traded derivative |
| **FINNIFTY** | Financial services (banks + NBFC + insurance + AMC) | Broader than BANK NIFTY |
| **SENSEX** | 30 large caps (BSE) | Confirmatory; divergence from NIFTY is usually construction |
| **NIFTY MIDCAP 150 / SMALLCAP 250** | Mid/small caps | Risk-appetite gauge |
| **NIFTY IT, AUTO, PHARMA, FMCG, METAL, PSU BANK, REALTY** | Sector indices | Sector rotation analysis |

Index levels are **not tradable directly**; only futures, options, or ETFs are.

## 3. Equity specifics

| Attribute | Value / rule |
|-----------|--------------|
| Session | 09:15–15:30 IST (pre-open 09:00–09:08, post-close session exists) |
| Settlement | T+1 (rolling; verify current cycle with the exchange) |
| Price bands | Circuit limits apply per stock (2%, 5%, 10%, 20% variants; some scrips have no band in F&O) |
| Tick size | ₹0.01 for most equities; verify per scrip |
| Intraday equity shorting | Must be squared off before session close (no naked overnight cash short) |
| Delivery shorting | Requires borrowed shares / SLB facility |
| Corporate actions | Split, bonus, dividend, rights — all require adjusted data |

## 4. Index behaviour worth knowing

- **BANK NIFTY is the highest-beta major index.** It moves more than NIFTY in both directions.
- **Expiry days** can produce unusual index behaviour (see `derivatives.md`).
- **Index divergence:** NIFTY up while BANK NIFTY down usually means non-financials are carrying the index —
  narrow leadership. Note it; do not over-interpret one session.
- **Midcap/smallcap divergence from NIFTY** is a risk-appetite signal. Midcaps underperforming while NIFTY rises
  often precedes broadening weakness.

## 5. Data sources (official first)

| Data | Source |
|------|--------|
| Prices, OI, volumes | NSE / BSE websites and official feeds; licensed vendors |
| Corporate announcements and filings | Exchange announcement pages |
| Corporate actions and results calendar | Exchange corporate-action pages |
| FII/DII activity | Exchange end-of-day publications |
| Index methodology and rebalancing | NSE/BSE index methodology documents |
| Regulation | SEBI circulars |
| Macro | RBI, MoSPI |

**Never fabricate an exchange figure.** If you cannot reach the source, say so and mark the figure unavailable.

## 6. Common errors in Indian market analysis

| Error | Guard |
|-------|-------|
| Confusing NSE and BSE listings | Check the ticker suffix; ask if unclear |
| Applying US session hours | 09:15–15:30 IST |
| Assuming a fixed expiry day | Schedules change — verify from the exchange calendar |
| Treating an intraday cash short as holdable | It must be squared off before the close |
| Ignoring circuit limits on small caps | Price can lock; stops cannot fill |
| Using unadjusted data across a split/bonus | Adjust |
| Quoting STT/GST rates from memory | Verify with the broker |
| Assuming a holiday | Check the exchange holiday list |

## 7. Files in this directory

- [`sessions-and-holidays.md`](sessions-and-holidays.md) — session timings, the pre-open, and how to handle holidays
- [`indices.md`](indices.md) — index construction, divergence reading, sector rotation
- [`derivatives.md`](derivatives.md) — F&O specifics, expiry mechanics, OI interpretation caveats

## 8. Hinglish note

Indian market timing **09:15–15:30 IST** hai. Intraday cash short ko **market band hone se pehle** square off
karna padta hai. Circuit limits ke wajah se chhote stocks mein stop fill nahi hota. NSE aur BSE ke tickers alag
hote hain — chart dekh kar confirm karo, guess mat karo.
