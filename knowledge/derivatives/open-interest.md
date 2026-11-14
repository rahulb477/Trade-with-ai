# Open Interest (OI) and Change in OI

## 1. Definitions

```
Open interest = the number of contracts currently outstanding (not yet closed)
Volume        = contracts traded in a period
ΔOI           = OI_today − OI_previous
```

Volume measures **activity**; OI measures **positions held**. A day can have huge volume and falling OI (lots of
closing trades) or small volume and rising OI (new positions held).

## 2. The four-quadrant reading

Combining price change with OI change gives four states. Each has a conventional interpretation — and each is
**ambiguous in practice**, which is why the caveats matter.

| Price | OI | Conventional reading | Caveat |
|-------|----|---------------------|--------|
| Up | Up | New longs entering — bullish | Could also be new shorts being set up against the move |
| Up | Down | Short covering — the rally may be weak | Could be longs taking profit into strength; not necessarily bearish |
| Down | Up | New shorts entering — bearish | Could be longs adding at lower prices |
| Down | Down | Long liquidation — the fall may be ending | Could be shorts taking profit; not necessarily bullish |

**Honest conclusion:** OI + price gives you a description of *positioning change*, not a direction. Use it to
understand crowding and risk, not to generate a signal on its own.

## 3. Where OI genuinely helps

1. **Crowding assessment.** Rapidly rising OI with a one-way price move means a build-up of positions that must
   eventually be closed — raising the risk of a sharp counter-move.
2. **Expiry dynamics.** Approaching expiry, OI concentration by strike tells you where the market has exposure
   (see `options-metrics.md` max pain).
3. **Rollover detection.** In Indian F&O, rollover from the near month to the next is visible in OI. High rollover
   with rising price suggests positional bullishness; the opposite suggests the reverse. Still an inference.
4. **Liquidity assessment.** High OI = liquid contract = tighter spreads and less slippage. This is a *reliable*
   use.

## 4. Indian market specifics

- **Index derivatives** (NIFTY, BANKNIFTY, FINNIFTY) have weekly and monthly expiries. **Expiry schedules change
  periodically** — verify against the exchange's own calendar (`markets/india/`). Never assert an expiry day from
  memory.
- **Stock futures** are monthly only.
- OI and ΔOI are published by the exchange; intraday snapshots exist but are at intervals, not tick-by-tick.
- **FII/DII derivative positions** are published end-of-day in aggregate. A single day is noise.

## 5. Practical reading template

```
Instrument / expiry : NIFTY 2026-11-27 (verify against exchange calendar)
OI                  : 12.4M contracts (previous 11.8M) -> +5.1%
Price               : 24,180 (+0.6%)
Reading             : price up with rising OI = new positions being added on the up move.
                      Direction inference is ambiguous (longs and shorts both add OI);
                      the reliable information is that participation is increasing and
                      closing flow may matter into expiry.
Risk note           : rising OI into an event expiry increases gap/squeeze risk.
```

## 6. Common errors

| Error | Guard |
|-------|-------|
| "OI up = bullish" | OI rising happens with new shorts too |
| Using total OI without ΔOI | A level without change says little |
| Inferring OI from a price chart | Impossible; OI needs derivative data |
| Ignoring expiry effects | The same OI means different things 1 day vs 20 days from expiry |
| Treating a single day's FII derivative data as a trend | Noise |
| Quoting an expiry date from memory | Verify; schedules change |

## 7. Beginner summary (Hinglish)

**OI (Open Interest)** = kitne contracts abhi **khule** hain. **Volume** = kitna trading hua. Dono alag cheezein
hain.

**Char quadrants:**
- Price up + OI up = naye positions ban rahe (conventional: bullish)
- Price up + OI down = short covering (rally kamzor ho sakti hai)
- Price down + OI up = naye shorts (bearish)
- Price down + OI down = long liquidation

**Sabse zaroori baat:** "OI badha = bullish" — yeh **galat** hai. OI naye longs aur naye shorts dono se badhta hai.
OI se aap **crowding aur risk** samajh sakte ho, direction nahi.

**Reliable use:** OI zyada = liquidity zyada = spread kam. Yeh pakka hai.

**India:** expiry schedule badalta rehta hai — exchange calendar se verify karo, yaad se mat bolo.

## 8. Exercise

Find three sessions with rising OI and three with falling OI. Record the price change on each and what happened in
the following 5 sessions. Then answer: could you have predicted direction from the OI quadrant alone? Write the
honest answer in one line.

---
*See also: [`options-metrics.md`](options-metrics.md) · [`../markets/india/derivatives.md`](../../markets/india/derivatives.md) ·
[`../../engines/options-intelligence/README.md`](../../engines/options-intelligence/README.md)*
