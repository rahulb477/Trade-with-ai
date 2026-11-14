# Pending Setup Report Template (Quick Mode — WAIT)

> The user sees `WAIT` first. This template is a `WAIT` quick report whose outstanding condition is explicit. It is not a downgraded full report — it is the default.

---

```
{{INSTRUMENT}} | {{EXCHANGE}} | {{TIMEFRAME}}

VERDICT: WAIT

WAIT UNTIL:
{{WAIT_CONDITION_SENTENCE}}

ENTRY:
{{ENTRY_ZONE_OR_PRICE}}
Only after the specified confirmation. (PENDING / CONDITIONALLY VALID)

STOP LOSS:
{{STOP_PRICE_OR_SENTINEL}}

TAKE PROFIT 1:
{{TP1}}

TAKE PROFIT 2:
{{TP2}}

TAKE PROFIT 3:
{{TP3}}

RISK / REWARD:
{{RR_DISPLAY}}

REASON:
{{SHORT_REASON_WAIT}}

Hinglish: {{HINGLISH_WAIT}}

Data: {{DATA_TIMESTAMP}} | Freshness: {{FRESHNESS}}
Educational paper-trading research only. Not investment advice. No real-money order was placed.
```

---

## When to use

* Breakout/breakdown confirmation pending (close-through missing, volume not confirmed, retest incomplete).
* Indicators conflict, market choppy, higher-timeframe disagreement.
* Data sufficient to describe structure but insufficient to clear the entry checklist.

The `WAIT UNTIL:` line distinguishes the *reason* for waiting (see `workflows/wait-confirmation.md`).

---

## Example

```
BTCUSD | Bitstamp | 5m

VERDICT: WAIT

WAIT UNTIL:
5-minute candle closes below the identified support and the breakdown is confirmed by the required evidence.

ENTRY:
67,300–67,400
Only after the specified confirmation. (PENDING)

STOP LOSS:
67,800

TAKE PROFIT 1:
66,900–67,000

TAKE PROFIT 2:
66,500

TAKE PROFIT 3:
66,200

RISK / REWARD:
T1 1.80 | T2 2.90 | T3 4.20

REASON:
Price is consolidating below resistance. Wait for confirmation before considering the hypothetical setup.

Hinglish: Price resistance ke neeche hai. Breakout confirmation ka wait karo.

Data: 2026-11-14T15:29:58+05:30 | Freshness: LIVE
Educational paper-trading research only. Not investment advice.
```

---

## Difference between a forming and a confirmed state

| State | Label | ENTRY STATUS |
|-------|-------|--------------|
| Candle currently forming | `WAIT — candle still forming` | `PENDING` |
| Candle closed, confirmation missing | `WAIT — confirmation pending` | `PENDING` |
| Confirmed breakout/breakdown | Eligible for `READY` | `CONDITIONALLY VALID` → `READY` if other gates pass |
| Unconfirmed breakout | `WAIT — unconfirmed breakout` | `PENDING` |
| Failed breakout/reclaim | `WAIT — fresh trigger needed` | `INVALIDATED` → `NO TRADE` or `WAIT` for new level |

Never blur these five.

---

*Engine: `integrations/python/trading_intel/quick_signal.py` — `VERDICT_WAIT` path.*
