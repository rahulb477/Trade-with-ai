# Commodities

## 1. Categories

| Category | Examples | Key venues |
|----------|----------|-----------|
| Energy | Crude oil (WTI, Brent), natural gas, gasoline, heating oil | NYMEX, ICE |
| Precious metals | Gold, silver, platinum, palladium | COMEX, NYMEX |
| Base metals | Copper, aluminium, zinc, nickel, lead | LME, COMEX |
| Agriculturals | Corn, wheat, soybeans, sugar, coffee, cotton | CBOT, ICE |
| Softs | Cocoa, coffee, sugar | ICE |
| India-specific | Crude, gold, silver, copper, natural gas, agri | MCX |

## 2. The feature that makes commodities different: the contract

A commodity chart usually shows a **continuous futures series** assembled from individual contracts. That creates
artefacts:

| Artefact | Cause |
|----------|-------|
| Sudden jumps | Rolling from one contract to the next |
| Distorted levels | Different contracts have different prices (contango/backwardation) |
| Volume discontinuities | Trading migrates to the next contract |
| "Gaps" that were never traded | Roll, not market movement |

**Always check whether a series is back-adjusted.** An unadjusted continuous chart will show "breakouts" that are
roll artefacts.

## 3. Drivers

| Commodity | Primary drivers |
|-----------|-----------------|
| Crude | OPEC+ supply, inventories, global demand, geopolitics, USD |
| Natural gas | Weather, storage levels, LNG flows, seasonality |
| Gold | Real yields, USD, central-bank buying, risk sentiment |
| Silver | Gold + industrial demand; higher beta |
| Copper | China demand, global growth, inventories |
| Agri | Weather, planting/harvest cycles, export policy, stocks-to-use |

Seasonality is real for agriculturals and natural gas; it is much weaker and less tradable for metals.

## 4. India (MCX) specifics

| Feature | Note |
|---------|------|
| Session | Roughly 09:00–23:30 IST (varies by contract and season) |
| Settlement | Cash-settled for most non-agri contracts |
| Currency | INR-denominated; **USD/INR movement affects the price** |
| Reference price | Global benchmarks (NYMEX crude, COMEX gold) plus the rupee |
| Expiry | Monthly, with specific dates per contract |

**Key consequence:** an MCX gold chart is driven by both COMEX gold *and* USD/INR. A pure technical read that
ignores the currency can be badly wrong. Always state both inputs.

## 5. Common errors

| Error | Guard |
|-------|-------|
| Analysing an unadjusted continuous series | Check roll adjustment |
| Ignoring the roll date | Rollovers create artefacts |
| Treating storage/carry as irrelevant | Contango/backwardation describe it |
| Ignoring USD/INR for MCX prices | Both drivers matter |
| Applying equity session hours | Commodity sessions differ |
| Assuming seasonality applies to metals | It is weak there |

## 6. Hinglish summary

**Commodity chart aksar continuous futures series hota hai** — roll hone par artificial gaps aate hain. Adjusted
data use karo, warna aap jhootha breakout dekhoge.

**Gold:** real yields, USD, central banks. **Crude:** OPEC+, inventories, geopolitics. **Copper:** China demand.

**MCX par:** price = global benchmark + USD/INR. Dono dekhna zaroori hai. Sirf technical dekhna adhoora hai.

**Session equity se alag hai** — MCX raat tak chalta hai.
