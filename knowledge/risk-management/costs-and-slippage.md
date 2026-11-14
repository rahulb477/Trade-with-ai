# Costs, Slippage and Gap Risk

## 1. Why costs decide viability

Costs are charged in currency but felt in **R**. Convert them:

```
cost_R = round_trip_cost_per_unit / risk_per_unit
```

Example: risk per unit 4.00, round-trip cost 1.20 → **0.30R**. A 1:1.5 plan becomes roughly 1:1.1 after costs.
For a scalping strategy with a 1:1 target, a 0.3R cost turns a break-even gross edge into a consistent loss.

## 2. Cost components (India, structure — verify current rates with your broker)

| Component | Basis |
|-----------|-------|
| Brokerage | Flat per order (discount) or % of turnover (full service) |
| STT / CTT | % on buy and/or sell; **differs by segment** (delivery / intraday / futures / options) |
| Exchange transaction charges | Small % of turnover |
| SEBI turnover fee | Very small % |
| Stamp duty | % on the buy side |
| GST | % on (brokerage + transaction charges) |
| DP charge | Per sell transaction on delivery |
| **Slippage** | Difference between expected and filled price |

**Do not quote exact rates from memory.** Rates and slabs change; cite the broker's current schedule or the
exchange circular.

## 3. Slippage modelling

```
buy  fill = expected + (half_spread + slippage_bps/10000 × price)
sell fill = expected − (half_spread + slippage_bps/10000 × price)
```

Conservative defaults for research:

| Instrument class | Slippage assumption |
|------------------|--------------------|
| Large-cap index / futures | 2–5 bps |
| Liquid large-cap equity | 5–10 bps |
| Mid-cap | 15–30 bps |
| Small-cap / illiquid | 30–100 bps, and often unfillable at size |
| Options (ATM, weekly) | Spread-dominated; often 0.5–2% of premium |

Slippage is worse when:
- volatility is high,
- the order is large relative to available liquidity,
- the market is at an open/close,
- the order is a stop triggered into a fast move,
- the instrument has a wide spread.

## 4. Liquidity limits

```
max_units ≈ 0.01 × average_daily_volume      (1% participation, conservative)
```

Beyond that, your own order moves the price and the backtest's fill assumption is fiction.

## 5. Gap risk

| Type | Example | Effect |
|------|---------|--------|
| Overnight gap | Index gaps 2% on global news | Stop fills far beyond the level |
| Event gap | Stock gaps 12% after results | Planned 1R loss becomes 4–8R |
| Circuit lock | Illiquid stock hits the band | Cannot exit at all |
| Halt | Trading suspended | Frozen position |
| Expiry gap | Futures roll discontinuity | Artificial "gap" in a continuous series |

**Mitigation (educational):**
1. Reduce size into known events, or exit before them.
2. Prefer instruments with genuine liquidity.
3. Never treat the stop as a guaranteed maximum loss.
4. Model gaps explicitly in backtests (`engines/backtesting/`).

## 6. Impact on backtests (the part people skip)

A backtest without costs and slippage overstates performance. The required disclosures:

```
assumed_cost_bps_round_trip : e.g. 12
assumed_slippage_bps        : e.g. 8
cost_R_per_trade            : e.g. 0.22
gross_expectancy_R          : e.g. 0.35
net_expectancy_R            : e.g. 0.13   <-- the only number that matters
```

A strategy whose edge disappears after realistic costs is not a strategy.

## 7. Beginner summary (Hinglish)

**Costs ko R mein convert karo:**
```
cost_R = cost per share ÷ risk per share
```
Agar risk 4 hai aur cost 1.2 hai → **0.3R** per trade. Matlab 30% edge costs mein chala gaya.

**Brokerage flat ho ya %, STT, GST, stamp duty, DP charge — sab milta hai.** Exact rates **broker se verify**
karo, yaad se mat likho.

**Slippage:** jo price aapko dikha, woh nahi milta. Liquid large-cap mein 5–10 bps, small-cap mein 30–100 bps.

**Gap risk:** stop "floor" nahi hai. Result ke din 1R loss 5R ban sakta hai. Isliye event se pehle **size kam**
karo.

**Scalping ka sach:** agar cost 0.3R hai aur target 1R hai, to aapko bahut high win rate chahiye — warna
mathematically loss.

## 8. Exercise

Take one intraday and one swing trade idea. Estimate round-trip costs in bps and convert them to R using your
planned stop distance. Then recompute the R:R after costs to T1. Write down which one survives and which does not.

---
*See also: [`position-sizing.md`](position-sizing.md) · [`../../engines/backtesting/README.md`](../../engines/backtesting/README.md) ·
[`../../knowledge/quantitative-analysis/expectancy.md`](../quantitative-analysis/expectancy.md)*
