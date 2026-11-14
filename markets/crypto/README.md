# Crypto Markets

## 1. Structure

| Feature | Detail |
|---------|--------|
| Trading hours | **24/7/365** — no session close, no weekend gap |
| Venues | Centralised exchanges (spot, perpetuals, futures) and DEXs |
| Quote pairs | USDT, USD, BTC, ETH, INR (on Indian exchanges) |
| Perpetuals | Futures with no expiry; funding payments every few hours |
| Leverage | Very high on many venues (up to 100× on some) |
| Custody | Counterparty risk is real — exchange insolvencies have happened |

## 2. What 24/7 changes in the analysis

| Consequence | Detail |
|-------------|--------|
| **No overnight gaps** | The concept does not exist; a "gap" is a data artefact |
| No session boundaries | VWAP must be anchored deliberately, not session-reset |
| No pre-open or close auction | No closing-print effects |
| Volume has a daily rhythm | Even without a session, liquidity concentrates around US and EU hours |
| Weekend liquidity is thinner | Moves can be exaggerated; stops are more easily swept |
| Daily candles are arbitrary | Many traders use UTC 00:00; state the convention |

## 3. Crypto-specific drivers

| Driver | Effect |
|--------|--------|
| Liquidity / risk appetite | High beta to global risk sentiment |
| Regulation | Binary, headline-driven |
| ETF flows (where applicable) | Structural demand |
| Network events | Halvings, upgrades, forks |
| Funding rates (perps) | Crowding indicator; extreme funding precedes squeezes |
| Stablecoin health | Systemic risk for the whole market |
| Exchange health | Counterparty risk |

## 4. Funding rates and open interest

```
funding_rate > 0  -> longs pay shorts (crowded long)
funding_rate < 0  -> shorts pay longs (crowded short)
```

Extreme funding is a **crowding** indicator. It does not predict direction, but it does describe positioning
stress. Same caveats as OI (`knowledge/derivatives/open-interest.md`).

## 5. Data quality issues specific to crypto

| Issue | Why it matters |
|-------|----------------|
| **Wash trading** reported volume | Reported volume on some venues is unreliable |
| Different prices across venues | No consolidated tape; arbitrage keeps them close but not identical |
| Exchange outages during volatility | You may not be able to exit |
| Data revisions | Some venues revise historical candles |
| Perp vs spot basis | Different instruments |
| Stablecoin de-pegs | A USDT pair can move because the quote asset moved, not the base |

**Practical rule:** for any crypto analysis, state the **venue and pair** exactly. "BTC is at 96,000" is incomplete —
BTC/USDT on which exchange, at what timestamp?

## 6. India-specific

| Feature | Note |
|---------|------|
| INR pairs | Available on Indian exchanges; price differs from USDT pairs by the INR rate and local premium |
| Taxation | A specific tax regime applies to virtual digital assets — verify current rules; do not state rates from memory |
| Banking/on-ramp constraints | Have changed over time; verify current status |
| Regulatory status | Evolving; do not assert the current position without a cited source |

## 7. Common errors

| Error | Guard |
|-------|-------|
| Talking about "overnight gaps" in crypto | They do not exist |
| Using session VWAP | Anchor it explicitly instead |
| Trusting reported volume blindly | Cross-check venues |
| Comparing BTC/USDT to BTC/INR as if identical | Different quote assets |
| Quoting tax or regulatory rules from memory | Verify and cite |
| Assuming a 100× leverage venue is "normal" | State the venue's specifics |
| Ignoring funding on perps | It is a real cost/revenue |

## 8. Hinglish summary

**Crypto 24/7 chalta hai** — session close nahi, overnight gap nahi. Isliye "gap analysis" ka concept yahan lagu
nahi hota.

**VWAP** ko session reset nahi milta — manually anchor karna padta hai.

**Volume par andha bharosa mat karo** — kuch exchanges wash trading karte hain. Cross-check karo.

**Hamesha venue aur pair likho:** "BTC/USDT, <exchange>, <timestamp>". Sirf "BTC 96,000" adhoora hai.

**Funding rate:** positive = longs pay shorts (crowded long). Yeh **crowding** batata hai, direction nahi.

**India:** tax aur regulatory rules badalte rehte hain — yaad se mat likho, source ke saath likho.
