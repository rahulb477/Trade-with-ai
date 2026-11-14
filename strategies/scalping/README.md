# Scalping

**Horizon:** seconds to a few minutes. **Holding:** intraday only. **Trades per day:** many.

**Status:** `DOCUMENTED` — no validation is claimed. Scalping is the most cost-sensitive style there is; read
`knowledge/risk-management/costs-and-slippage.md` before anything else.

## 1. Characteristics

| Attribute | Typical |
|-----------|---------|
| Chart timeframes | 1m, 3m, 5m (analysis), tick/1m (execution) |
| Target | 0.3–1.0 ATR on the execution timeframe |
| Stop | 0.3–0.8 ATR |
| Win rate required | High (>55–60%) because costs are a large fraction of R |
| Cost sensitivity | Extreme — a 0.3R round trip can consume the entire target |
| Screen time | Continuous |

## 2. The cost arithmetic that kills most scalping

```
target 1.0R, stop 1.0R, round-trip cost 0.30R
net win  = +0.70R    net loss = -1.30R
break-even win rate = 1.30 / (1.30 + 0.70) = 65%
```

A scalper needs **65% accuracy just to break even** at a 1:1 target with 0.3R of costs. This is why the style is
only viable with genuine fee advantages (e.g. market-maker rebates) or on instruments where the cost/R ratio is
tiny.

## 3. Documented setups (as hypotheses, not validated edges)

| Setup | Condition | Notes |
|-------|-----------|-------|
| VWAP reclaim | Price reclaims VWAP after a failed break below, with volume | The most defensible scalp context |
| Opening-range breakout | Close beyond the first 15/30-minute range | Needs volume; prone to fakeouts |
| Failed breakout reversal | Sweep of a level + close back inside | Best R:R of the scalp setups |
| Trend pullback to EMA | Pullback to the 9/20-EMA in an established intraday trend with a rejection candle | Requires a trending day |

## 4. Required filters

- [ ] Liquidity: tight spread, deep book (otherwise the spread *is* the strategy failure)
- [ ] Regime: scalping in a chop is a lottery; require ADX > 20 or a clear VWAP relationship
- [ ] Time of day: avoid the first 5 minutes and the last 10 minutes
- [ ] No event risk (results, policy decisions)
- [ ] Brokerage structure that makes the cost/R ratio viable

## 5. What this repository will not do

- Present scalping as a beginner-friendly path. It is the hardest style, not the easiest.
- Quote a win rate without a measured, cost-inclusive sample.
- Provide tick-level execution instructions.

## 6. Beginner summary (Hinglish)

**Scalping** = bahut chhote targets, bahut zyada trades, minutes ka holding.

**Sabse bada dushman: costs.** Agar target 1R hai aur round-trip cost 0.3R hai, to break-even ke liye **65% win
rate** chahiye. Zyadatar log yeh calculate nahi karte.

**Kya chahiye:** tight spread, deep liquidity, achha brokerage structure, aur poora din screen time.

**Beginner ke liye:** nahi. Ye sabse mushkil style hai. Swing se shuru karo jahan costs ka asar kam ho.

## 7. Validation notes

To test a scalp setup you must include realistic costs, sub-minute or tick data where possible, and slippage
scaled to the spread. With 5-minute bars and a daily-bar cost model, the backtest will be fiction. See
`engines/backtesting/`.
