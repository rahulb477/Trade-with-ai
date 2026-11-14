# No-Trade Report Template (Quick Mode)

> **Output is hypothetical and educational.** A `NO TRADE` verdict is a positive decision not to participate, not a missing-data omission.

---

```
{{INSTRUMENT}} | {{EXCHANGE}} | {{TIMEFRAME}}

VERDICT: NO TRADE

WAIT UNTIL:
{{REASON_NO_TRADE_WAITS_OR_CLEAR}}

ENTRY:
NOT AVAILABLE — INSUFFICIENT DATA
(Setup invalidated or risk/reward unsuitable.)

STOP LOSS:
{{STOP_IF_JUSTIFIED_OR_SENTINEL}}

TAKE PROFIT 1:
{{TP1_OR_NOT_AVAILABLE}}

TAKE PROFIT 2:
{{TP2_OR_NOT_AVAILABLE}}

TAKE PROFIT 3:
{{TP3_OR_NOT_AVAILABLE}}

RISK / REWARD:
{{RR_OR_SENTINEL}}

REASON:
{{SHORT_REASON_NO_TRADE}}

Hinglish: {{HINGLISH_NO_TRADE}}

Data: {{DATA_TIMESTAMP}} | Freshness: {{FRESHNESS}}
Educational paper-trading research only. Not investment advice. No real-money order was placed.
```

---

## When to use

* Setup invalidated (close beyond invalidation / failed breakout reclaimed).
* Risk/reward unsuitable under the documented strategy (`R:R to T1 < 1.5` after costs).
* Market conditions do not support a valid setup (hostile volatility, choppy, illiquid).
* Required evidence unavailable and the condition is unrecoverable (gap risk through event, halt, circuit).

Contrast with `WAIT`: `WAIT` means "not yet, watch for X"; `NO TRADE` means "not this, even if X happens".

---

## Example

```
BTCUSD | Bitstamp | 5m

VERDICT: NO TRADE

WAIT UNTIL:
Clear confirmation appears.

ENTRY:
NOT AVAILABLE — INSUFFICIENT DATA

STOP LOSS:
67,800

TAKE PROFIT 1:
66,900

TAKE PROFIT 2:
NOT AVAILABLE

TAKE PROFIT 3:
NOT AVAILABLE

RISK / REWARD:
T1 1.10 — below the 1.5 minimum.

REASON:
Risk/reward to T1 is 1.10 — below the 1.5 minimum. No valid setup.

Hinglish: Risk/reward sahi nahi hai. Isliye no trade.

Data: 2026-11-14T15:29:58+05:30 | Freshness: LIVE
Educational paper-trading research only. Not investment advice.
```

---

*Engine: `integrations/python/trading_intel/quick_signal.py` — `VERDICT_NO_TRADE` path.*
