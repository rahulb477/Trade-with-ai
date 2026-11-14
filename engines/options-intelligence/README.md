# Engine — Options Intelligence

**Data gate:** requires an option chain (OI, volume, prices, ideally IV and Greeks). None of this is derivable from
a price chart.

## Inputs
Option chain snapshot(s) with timestamp; underlying price; expiry date (verified).

## Outputs
PCR, max pain, OI concentration, ΔOI, IV and IV rank, ATM Greeks — each with the snapshot time and limitations.

## Computations

```python
# PCR (OI-based)
pcr = sum(put_oi) / sum(call_oi)

# Max pain: the expiry price that minimises total option payout
def total_payout(S, chain):
    calls = sum(max(0, S - k) * oi for k, oi in chain.calls)
    puts  = sum(max(0, k - S) * oi for k, oi in chain.puts)
    return calls + puts
max_pain = min(chain.strikes, key=lambda S: total_payout(S, chain))

# IV rank
iv_rank = (iv_now - iv_min_52w) / (iv_max_52w - iv_min_52w) * 100
```

Reference: `knowledge/derivatives/options-metrics.md`.

## Interpretation limits (state these every time)

| Metric | Permitted claim | Forbidden claim |
|--------|-----------------|-----------------|
| PCR | "Crowding is neutral / put-heavy / call-heavy" | "Bullish because PCR is high" |
| Max pain | "The OI-weighted minimum-payout strike is X" | "Price will close at X" |
| OI concentration | "Positions are concentrated at these strikes" | "Institutions will defend X" |
| ΔOI | "Positions are being added at this strike today" | "Smart money is buying calls" |
| IV rank | "Options are expensive/cheap vs their own history" | "Volatility will fall" |
| Greeks | Sensitivity given the model's assumptions | A probability of profit |

## Reporting template

```
Options context
  Chain            : <instrument> expiry <date> (verified from exchange calendar)
  Snapshot         : 2026-11-14 15:20 IST (source: <provider>)
  Spot             : 24,180
  PCR (OI)         : 1.08
  Max call OI      : 24,500 (2.9M)
  Max put OI       : 24,000 (2.4M)
  Max pain         : 24,200
  ATM IV / IV rank : 12.4% / 38
  Reading          : positioning implies the market sees roughly 24,000-24,500 as the near-term
                     band. IV is mid-range, so there is no vol extreme to fade.
  Limitations      : snapshot only; PCR cannot distinguish bought from sold options; max pain
                     shifts as OI changes; expiry day verified but subject to change.
```

## Failure modes

| Failure | Guard |
|---------|-------|
| Producing any of these without chain data | Refuse |
| Quoting an expiry from memory | Verify and cite |
| Treating max pain as a target | Arithmetic only |
| Reporting IV without saying where it came from | Source + timestamp |
| Ignoring the bid-ask spread | Include it in any tradability note |
| Computing Greeks without disclosing model assumptions | Disclose |

## IV crush warning (always include when relevant)

If a binary event falls before expiry, state: "a long option position can lose money even if the direction is
correct, because implied volatility typically collapses after the event."
