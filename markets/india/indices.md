# India — Indices and Sector Context

## 1. The main indices

| Index | Base | Constituents | Weighting | Character |
|-------|------|--------------|-----------|-----------|
| NIFTY 50 | NSE | 50 large caps | Free-float market cap | The benchmark |
| BANK NIFTY | NSE | 12 largest banks | Free-float market cap | Highest-beta major index |
| FINNIFTY | NSE | Financial services (banks, NBFCs, insurance, AMCs) | Free-float | Broader financials |
| SENSEX | BSE | 30 large caps | Free-float | BSE benchmark |
| NIFTY NEXT 50 | NSE | Next 50 by size | Free-float | Large-cap breadth |
| NIFTY MIDCAP 150 | NSE | Mid caps | Free-float | Risk-appetite gauge |
| NIFTY SMALLCAP 250 | NSE | Small caps | Free-float | Risk-appetite tail |
| Sector indices | NSE | e.g. IT, AUTO, PHARMA, FMCG, METAL, PSU BANK, REALTY, ENERGY, MEDIA | Free-float | Rotation analysis |

**Verify composition and methodology** from the exchange's index documents before making any claim about weights.
Constituents change; weights change.

## 2. Reading index divergence

| Observation | Likely meaning | Confidence |
|-------------|----------------|-----------|
| NIFTY up, BANK NIFTY down | Non-financials carrying the index; narrow leadership | Low–moderate |
| NIFTY up, midcaps down | Risk appetite narrowing; defensive leadership | Low–moderate |
| NIFTY flat, VIX-type gauge rising | Complacency breaking down | Moderate |
| NIFTY at new high, advances below declines | Poor breadth | Moderate |
| BANK NIFTY leading up | Risk-on (banks are domestic cyclical) | Low–moderate |

**Caveat:** index divergence in a single session is mostly noise. It matters when it persists for several sessions.
Always state the lookback.

## 3. Sector rotation

```
Steps:
1. Compute each sector index's return over 1M, 3M, 6M.
2. Rank them (relative strength).
3. Compare the ranking against the previous period — what is improving, what is decaying.
4. Relate to the current regime (early cycle: financials/industrials; late cycle: defensives/energy).
```

Report as a table with the lookback period stated. Do not claim a rotation from one period's ranking.

## 4. Why BANK NIFTY behaves differently

- It is concentrated (a handful of banks dominate), so single-stock news moves it more.
- Banks are sensitive to rate expectations and credit growth — RBI policy is a first-order driver.
- It has the deepest derivatives market, so expiry effects are strongest there.
- Its volatility is structurally higher than NIFTY's.

Consequence: a BANK NIFTY plan needs wider stops (relative to price) and more attention to event risk.

## 5. Index technicals vs index futures vs index options

| Instrument | Notes |
|------------|-------|
| **Index level** | A computed number, not tradable directly |
| **Index futures** | Tradable, has basis and roll; gaps reflect both index and basis |
| **Index options** | Time-decaying derivatives; direction is only part of the outcome |
| **Index ETF** | Tradable, has tracking error, liquidity constraints, and premium/discount to NAV |

Do not treat a futures chart and an index chart as identical: the basis changes near expiry.

## 6. Data requirements

| Need | Source |
|------|--------|
| Index levels | Exchange / licensed vendor |
| Index constituents and weights | Exchange index methodology documents |
| Sector index levels | Exchange / vendor |
| Advance/decline data | Exchange end-of-day |
| FII/DII flows | Exchange end-of-day publications |
| Volatility index (India VIX) | Exchange |

None of these may be fabricated. If unavailable, say so.

## 7. Hinglish summary

**NIFTY 50** = 50 badi companies, main benchmark. **BANK NIFTY** = 12 bade banks, sabse zyada volatile. **Sensex** =
BSE ka 30-stock benchmark.

**Divergence ka matlab:** agar NIFTY upar ja raha hai par BANK NIFTY neeche, to index ko non-financials utha rahe
hain — leadership narrow hai. **Ek session se conclusion mat nikaalo** — 3-4 sessions dekho.

**Sector rotation:** 1M/3M/6M returns se sectors rank karo, aur dekho kaun improve ho raha hai.

**Index level trade nahi hota** — futures, options ya ETF trade hote hain. Futures chart mein basis hota hai,
isliye index chart se exactly same nahi hota.
