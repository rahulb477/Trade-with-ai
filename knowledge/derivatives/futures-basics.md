# Futures Basics

## 1. What a futures contract is
An agreement to buy or sell an underlying at a future date at a price agreed now. Exchange-traded, standardised,
marked to market daily, and margined.

## 2. Basis and roll

```
basis = futures_price − spot_price
```

| Basis | Name | Typical cause |
|-------|------|---------------|
| Positive | Contango | Carry costs (interest, storage) exceed dividends/yield |
| Negative | Backwardation | Convenience yield, shortage, or heavy hedging pressure |

Rolling from one expiry to the next produces an artificial jump in a **continuous** futures series. If you analyse
an unadjusted continuous series, you will see gaps that are roll artefacts, not market events. Always verify
adjustment before drawing levels across a roll.

## 3. Expiry effects

| Effect | Description |
|--------|-------------|
| Liquidity migration | Volume and OI shift from the near month to the next, typically in the days before expiry |
| Pin risk | Price gravitating to a strike near expiry (options-related) |
| Volatility | Expiry days can be erratic as positions unwind |
| Roll cost | Continuous series discontinuities |

**Indian specifics:** NSE/BSE index derivatives have weekly and monthly expiries; individual stock futures are
monthly. The **expiry day and list change periodically** — verify from the exchange's current circular, never from
memory. See `markets/india/derivatives.md`.

## 4. Contract specifications you must check before any analysis

| Specification | Why it matters |
|---------------|----------------|
| Lot size | Determines the notional and the risk per tick |
| Tick size | Determines the minimum price increment and the granularity of stops |
| Expiry date and time | Determines decay and roll timing |
| Margin (initial and maintenance) | Determines leverage and liquidation risk |
| Settlement (cash vs physical) | Determines whether you can hold to expiry |
| Trading hours | Session boundaries, and whether the contract trades in extended hours |

Never apply one contract's specs to another. A NIFTY lot and a BANKNIFTY lot are not comparable in risk.

## 5. Leverage: the arithmetic that ruins people

```
notional = price × lot_size × contracts
margin   = notional × margin_percentage     (broker/exchange dependent)
leverage = notional / margin
```

A 1% adverse move on 10× leverage is a 10% loss of margin. A 10% adverse move wipes out the margin entirely. This
is why futures require **smaller** risk per idea, not larger.

```
Example (illustrative numbers, not current values):
price 24,000 · lot 25 · 1 contract -> notional 600,000
margin 12% -> 72,000 blocked
a 1% move = 6,000 = 8.3% of the margin
```

## 6. Reading futures data honestly

| Data | What it supports |
|------|------------------|
| Price + OI + volume | Positioning description |
| Basis vs spot | Carry and sentiment, weakly |
| Rollover % into the next month | Positional intent, weakly |
| FII/DII derivative positions (EOD) | Aggregate crowding |

None of these is a direction signal on its own. All require the caveats in
[`open-interest.md`](open-interest.md).

## 7. Common errors

| Error | Guard |
|-------|-------|
| Analysing an unadjusted continuous series | Check roll adjustment |
| Assuming lot sizes or margins from memory | Verify with the exchange/broker |
| Applying intuition from equity cash to futures | Leverage changes everything |
| Ignoring the expiry in the risk plan | The contract disappears; positions must be closed or rolled |
| Treating basis as a signal | It is mostly carry |
| Quoting an expiry day without verification | Schedules change |

## 8. Beginner summary (Hinglish)

**Futures kya hai?** Aaj price tay karke baad mein delivery ka contract. Leverage hota hai, daily mark-to-market
hota hai.

**Basis** = futures − spot. Positive = contango (carry), negative = backwardation.

**Sabse zaroori:** futures mein **leverage** hota hai. 10× leverage par 1% galat move = margin ka 10% loss. Isliye
futures par risk **kam** rakhna padta hai, zyada nahi.

**Roll:** expiry ke paas positions next month mein shift hoti hain. Continuous chart par roll se artificial gap
aata hai — adjusted data use karo.

**India:** expiry day list **badalti rehti hai** — exchange circular se verify karo, yaad se mat bolo.

## 9. Exercise

Find the current lot size, tick size, margin, and expiry date for one index futures contract from the exchange
site. Compute the notional, the margin, and the loss on a 1% adverse move as a percentage of margin. Write one
sentence on what that implies for lot count, assuming a 1% risk budget.

---
*See also: [`open-interest.md`](open-interest.md) · [`../markets/india/derivatives.md`](../../markets/india/derivatives.md) ·
[`../core/risk-management.md`](../../core/risk-management.md)*
