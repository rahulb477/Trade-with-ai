# Reading an Options Chain

## 1. What an option chain shows

For each strike, on both the call and put side:

| Field | Meaning |
|-------|---------|
| LTP | Last traded premium |
| Bid / Ask | Current quote; the spread is your immediate cost |
| Volume | Contracts traded today |
| OI | Contracts outstanding |
| ΔOI | Change vs the previous snapshot |
| IV | Implied volatility for that strike |
| Greeks | Delta, gamma, theta, vega if the platform shows them |

## 2. Reading order (most useful first)

```
1. Spread       -> is this strike even tradeable? (wide spread = high cost)
2. OI by strike -> where is the market's exposure concentrated?
3. ΔOI          -> what is being added or closed today?
4. IV by strike -> is there a skew (puts vs calls)? Is there an IV spike at one strike?
5. Greeks       -> what is the sensitivity of the specific option you are considering?
6. Volume       -> activity confirmation
```

Beginners usually start at LTP. That is the least informative entry point.

## 3. What the chain tells you

| Observation | Legitimate inference |
|-------------|---------------------|
| Large OI at a strike | That strike matters; price may gravitate/pin near it into expiry |
| Large ΔOI at a strike | Positions are being built there today |
| Steep put IV skew | Downside protection is relatively expensive — the market prices downside risk higher |
| Very low IV across the chain | The market expects little movement (or is complacent) |
| Wide bid-ask spreads | Illiquid strike; you will pay to enter and exit |
| Call OI concentrated above spot | Overhead "resistance" in option terms, often a supply zone |

## 4. What the chain cannot tell you

- **Who** is buying or selling (hedge funds, retail, market makers).
- **Why** (protection, income, speculation, hedging a cash position).
- **Direction** with any reliability.
- Whether the OI is "real" conviction or market-maker hedging flow.
- Anything about a stock's **price chart** — the chain is a separate dataset.

## 5. The pinning effect (and its limits)

Approaching expiry, price often gravitates toward strikes with large OI because market makers' hedging creates
flows in that direction. This is a documented phenomenon, but:

- It is strongest in the last day or two and mainly for index options.
- It is a **tendency**, not a constraint.
- Events (news, macro data) override it entirely.

## 6. Practical template

```
Chain            : BANKNIFTY weekly, expiry <verify from exchange calendar>
Spot             : 52,140
Max call OI      : 52,500 (2.9M) — overhead supply reference
Max put OI       : 51,800 (2.4M) — support reference
ATM IV           : 14.1% ; call IV 13.8% ; put IV 14.6% -> mild put skew
Spread (ATM)     : 0.6 points wide -> tradeable
Reading          : the chain implies an expected weekly range of roughly 51,800-52,500 based on where OI is
                   concentrated. That is a positioning description, not a forecast; a macro event would
                   invalidate it.
```

## 7. Common errors

| Error | Guard |
|-------|-------|
| Reading OI as "smart money direction" | It is not identifiable |
| Ignoring the bid-ask spread | The spread is a guaranteed cost |
| Trading an illiquid strike because the premium looks cheap | Cheap premiums are often cheap for a reason |
| Confusing volume with OI | Different measures |
| Assuming a strike will pin | Tendency only; events override |
| Using a stale chain | Timestamp the snapshot; chains change constantly |

## 8. Beginner summary (Hinglish)

**Option chain kya dikhata hai:** har strike par calls aur puts ka premium, OI, volume, IV aur Greeks.

**Padhne ka order:**
1. **Spread** — pehle dekho ki strike trade karne layak hai ya nahi.
2. **OI** — kahan positions concentrated hain.
3. **ΔOI** — aaj kya add ho raha hai.
4. **IV** — kahan mehnga/sasta hai.
5. Greeks.

**Sabse zaroori:** chain aapko **positioning** batati hai, **direction nahi**. "Smart money" kaun hai — pata nahi
chal sakta.

**Galti:** sasta premium dekh kar illiquid strike lena. Woh sasta isliye hai kyunki exit mushkil hai.

## 9. Exercise

Take one chain snapshot. Identify the top three OI strikes on each side. Compute the spread at the ATM strike.
Then write three sentences: what the chain says about positioning, what it does *not* say, and what event could make
all of it irrelevant.

---
*See also: [`options-metrics.md`](options-metrics.md) · [`open-interest.md`](open-interest.md) · [`futures-basics.md`](futures-basics.md)*
