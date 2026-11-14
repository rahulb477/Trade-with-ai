# United States Markets

## 1. Exchanges and sessions

| Exchange | Instruments |
|----------|-------------|
| **NYSE** | Listed equities, ETFs |
| **Nasdaq** | Listed equities (tech-heavy), ETFs |
| **Cboe** | Options, volatility products |
| **CME / CBOT / NYMEX / COMEX** | Futures and options (indices, rates, energy, metals, ags) |

| Session | Time (ET) |
|---------|-----------|
| Pre-market | 04:00 – 09:30 |
| **Regular session** | **09:30 – 16:00** |
| After-hours | 16:00 – 20:00 |

Extended hours have thin liquidity and wide spreads; candle behaviour there is **not** comparable to the regular
session. State which session a bar belongs to.

## 2. Key indices

| Index | Character |
|-------|-----------|
| S&P 500 | Broad large-cap benchmark; the global risk barometer |
| Nasdaq 100 | Tech-heavy; higher beta; most liquid futures (NQ) |
| Dow Jones Industrial Average | **Price-weighted** — a quirk that makes it structurally different |
| Russell 2000 | Small caps; domestic risk appetite |
| VIX | Implied volatility on S&P 500 options; not an index you can trade directly |

## 3. Structural features

| Feature | Detail |
|---------|--------|
| Price bands | No hard daily price limits for most equities; **LULD** volatility halts apply |
| Halts | Market-wide circuit breakers (Level 1/2/3) at defined S&P 500 declines; single-stock LULD bands |
| Settlement | T+1 for equities (verify current cycle) |
| Tick size | $0.01 for prices ≥ $1.00 under Reg NMS; sub-penny rules apply in some venues |
| Shorting | Short sale restrictions vary; hard-to-borrow names carry large fees |
| Futures | Nearly 24-hour (Globex), with a daily settlement and maintenance break |
| Pre/post-market gaps | Normal and frequent; a daily candle excludes them unless the vendor says otherwise |

## 4. Macro drivers (first order)

| Driver | Why |
|--------|-----|
| Fed policy and rate expectations | Discount rate for all assets |
| US 10Y Treasury yield | Real-yield pressure on equities and gold |
| CPI, PCE, payrolls, ISM | Scheduled volatility events |
| DXY (dollar index) | Pressure on EM, commodities, and multinational earnings |
| Earnings season | Mid-Jan, Apr, Jul, Oct — concentrated volatility |

## 5. Data sources

| Data | Source |
|------|--------|
| Prices, filings | Exchange feeds, SEC EDGAR, licensed vendors |
| Economic releases | BLS, BEA, Fed (FRED) |
| Options data | Cboe, OPRA-derived vendors |
| Short interest | FINRA (bi-monthly) |

## 6. Common errors

| Error | Guard |
|-------|-------|
| Using IST session times | US session is 09:30–16:00 ET |
| Treating pre-market gaps as intraday moves | Label the session |
| Ignoring the LULD halt regime | A "stop" may not fill |
| Assuming a hard daily price limit | There is none for most equities |
| Comparing a price-weighted index (DJIA) to a cap-weighted one naively | Different construction |
| Quoting current rates/limits from memory | Verify |

## 7. Hinglish summary

**US session:** 09:30–16:00 ET. Pre-market aur after-hours mein liquidity kam hoti hai — wahan ke candles normal
session se compare mat karo.

**Price limits:** US equities mein hard daily limit nahi hota, par **LULD halts** hote hain — price kuch der ke
liye ruk sakta hai.

**Macro drivers:** Fed, 10Y yield, CPI, payrolls, DXY. Earnings season Jan/Apr/Jul/Oct mein concentrated hota hai.

**Dow Jones price-weighted hai** — baaki indices market-cap weighted hain. Isliye Dow ka behaviour structurally
alag hai.
