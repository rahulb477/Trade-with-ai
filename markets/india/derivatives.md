# India — Derivatives Specifics

## 1. Structure

| Instrument | Expiries | Notes |
|------------|----------|-------|
| Index futures | Monthly (and mid-month variants) | Cash-settled |
| Index options | Weekly and monthly | Cash-settled; the most active segment |
| Stock futures | Monthly | Cash-settled |
| Stock options | Monthly | Physically settled in many cases — verify |
| Currency futures/options | Monthly | On exchanges (NSE/BSE) and OTC |

**Expiry days, weekly expiry availability, and the number of weekly expiries have changed repeatedly in recent
years.** Never state an expiry day from memory. Verify from the exchange's current circular and cite it.

## 2. Contract specifications you must look up before any analysis

| Spec | Why |
|------|-----|
| Lot size | Determines notional and risk per tick |
| Tick size | Determines stop granularity |
| Expiry date and time | Determines decay and roll timing |
| Strike interval | Determines the option chain's resolution |
| Settlement type (cash/physical) | Determines whether you can hold to expiry |
| Margin (SPAN + exposure) | Determines leverage and liquidation risk |
| Position limits | Determines whether size is even permitted |

**Never invent these numbers.** They change and they differ per instrument.

## 3. OI and expiry mechanics

| Concept | What is defensible to say |
|---------|---------------------------|
| OI concentration at a strike | "Positions are concentrated there" |
| Max pain | "A computed value from current OI; not a forecast" |
| Rollover | "Positions are migrating to the next expiry" |
| Expiry-day volatility | "Expiry days often show unusual intraday behaviour" |
| Pinning | "Price sometimes gravitates to a high-OI strike near expiry — a tendency, not a rule" |

What is **not** defensible: "institutions will defend 24,000", "the market must close at max pain", "OI shows smart
money is long".

## 4. FII/DII derivative data

- Published end-of-day in aggregate (index futures long/short, index options, stock futures).
- **A single day is noise.** Look at the trend over weeks.
- Cash-market flows and derivative flows are different datasets; do not merge them into one statement.

## 5. Practical constraints for a paper-trade plan

| Constraint | Statement to include |
|------------|---------------------|
| Weekly options decay fast | Theta dominates the outcome; direction alone is insufficient |
| IV crush | Holding long options through an event can lose even if direction is right |
| Physical settlement of stock options | You may be obliged to take/give delivery |
| Margin calls | An adverse move can force liquidation before your thesis resolves |
| Circuit limits on the underlying | Options can become untradeable |
| Expiry-day liquidity | Spreads widen; fills worsen |

## 6. A defensible derivatives paragraph

```
Derivatives context (NIFTY, expiry <verified date>)
  OI              : call OI concentrated at 24,500; put OI at 24,000 (source, snapshot time)
  PCR (OI)        : 1.08 — near neutral crowding
  Max pain        : 24,200 (computed from this snapshot only)
  ATM IV          : 12.4%, IV rank 38 over 52 weeks
  Reading         : no extreme in IV; positioning suggests the market sees 24,000-24,500 as the
                    near-term band. This is a positioning description, not a forecast; an event
                    would invalidate it.
  Limitations     : snapshot, not live; PCR cannot distinguish bought vs sold options;
                    max pain moves as OI shifts.
```

## 7. Common errors

| Error | Guard |
|-------|-------|
| Stating an expiry day from memory | Verify and cite |
| "OI up = bullish" | Ambiguous |
| Treating max pain as a target | It is a computation |
| Ignoring IV crush for long options | State the risk |
| Assuming stock options are cash-settled | Verify |
| Using lot sizes from memory | Look them up |
| Quoting margins from memory | Look them up |

## 8. Hinglish summary

**Index options:** weekly aur monthly dono hote hain — **expiry day badalti rehti hai**, exchange circular se
verify karo.

**OI:** "OI badha = bullish" — galat. OI naye longs aur shorts dono se badhta hai. OI se **crowding** samjho,
direction nahi.

**Max pain:** OI se nikala gaya number hai, **prediction nahi**.

**Lot size, margin, tick size:** yaad se mat likho — exchange se check karo.

**Long options ka risk:** result ke pehle option kharida to **IV crush** se direction sahi hone par bhi loss ho
sakta hai.
