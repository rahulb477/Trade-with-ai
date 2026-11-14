# Engine — Order Flow Intelligence

**Data gate first.** Nothing in this engine may be produced without genuine order-flow data. Order flow cannot be
inferred from a candlestick chart, and inventing it is the most common fabrication in retail "advanced" analysis.

## 1. Data availability gate

| Construct | Requires | Available from a price chart? |
|-----------|----------|------------------------------|
| Bid/ask imbalance | Level-1 quotes over time | **No** |
| Volume delta / CVD | Trade-level aggressor side (bid vs ask) | **No** |
| Absorption | Volume + minimal price movement, at a level | Partially (volume + range only, coarse) |
| Exhaustion | Declining delta at price extremes | **No** (without delta) |
| Footprint chart | Trade prices + volumes within each bar | **No** |
| Order book imbalance | Level-2/3 depth | **No** |
| Cumulative volume delta divergence | CVD series | **No** |

**If the data is unavailable, say "not available" and do not describe order flow.** A chart showing high volume
with a small range is *consistent with* absorption — that is as far as a price chart permits.

## 2. The constructs, and how to read them when data exists

### 2.1 Bid/ask imbalance
```
imbalance = (bid_size − ask_size) / (bid_size + ask_size)
```
Persistent positive imbalance = more passive buying interest. **Caveat:** displayed size can be spoofed or
withdrawn; it is not a commitment.

### 2.2 Volume delta and CVD
```
delta_t = aggressive_buy_volume_t − aggressive_sell_volume_t
CVD_t   = Σ delta
```
| Reading | Meaning |
|---------|---------|
| Price up, CVD up | Buying is driving the move — healthy |
| Price up, CVD flat/down | The move is happening on passive absorption of selling into bids — often a rally that fails |
| Price down, CVD down | Selling is driving |
| Price down, CVD up | Selling is being absorbed — potential bottom |
| CVD divergence at a price extreme | Exhaustion hypothesis |

### 2.3 Absorption
Large traded volume at a price with little price movement: someone is absorbing. Visible in footprint/delta as
high volume with a small range and a dominant passive side.

### 2.4 Exhaustion
Delta declining while price makes new extremes — the aggressive side is running out of participants. A hypothesis
requiring confirmation.

### 2.5 Footprint
Per-price volume within each bar, split by aggressor. Reading: imbalances between bid and ask volume at specific
prices, and where the "unfinished" levels are.

### 2.6 Order book imbalance
Depth-weighted comparison of resting bids vs asks. **Highly unreliable** in isolation: depth is easy to spoof, and
it is withdrawn before large moves.

## 3. Reporting template (only when data exists)

```
Order flow (source: <provider>, <timestamp>)
  Session delta       : +1.24M contracts
  CVD trend           : rising through the session, flat in the last 30 min
  Absorption observed : 24,050-24,070 band absorbed 3 sessions of selling with no progress
  Divergence          : price made a marginal new high at 14:20 while CVD made a lower high
  Reading             : the marginal new high lacked aggressive participation — exhaustion hypothesis,
                        not a confirmed reversal
  Limitations         : single-venue data; delta requires aggressor classification, which is approximate
                        for some providers
```

## 4. Failure modes

| Failure | Guard |
|---------|-------|
| Describing order flow from a price chart | Refuse; state data unavailable |
| Treating displayed depth as real intent | Spoong is common |
| CVD from a single venue as "the market" | State the venue |
| Calling absorption from volume+range alone | Say "consistent with", not "is" |
| Ignoring the approximate nature of aggressor classification | Disclose |
| Order flow overriding a structural invalidation | It does not |

## 5. Why this engine exists with such strict gates

Order-flow language is the most common way an AI hallucinates authority. "Big absorption at the bid" sounds
precise and is unfalsifiable without data. This engine exists to make the requirement explicit: **no data, no
statement**.
