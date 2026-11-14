# Options Metrics — PCR, Max Pain, IV, Greeks

All of these require **option-chain data**. None can be derived from a price chart. If you do not have chain
data, you cannot report them.

---

## 1. Put-Call Ratio (PCR)

```
PCR (OI-based)     = total put OI / total call OI
PCR (volume-based) = put volume / call volume
```

| Reading | Conventional interpretation | Reality |
|---------|----------------------------|---------|
| PCR > 1.2–1.3 | Heavy put OI → often read as "excess bearishness" → contrarian bullish | Depends on whether puts are bought as protection or sold for income |
| PCR < 0.7–0.8 | Heavy call OI → "excess bullishness" → contrarian bearish | Calls may be sold for income too |
| PCR ≈ 1 | Balanced | Little information |

**The fundamental ambiguity:** PCR cannot distinguish **buying** puts from **selling** puts. Those are opposite
positions. A high put OI could mean fear (bullish contrarian read) or aggressive put selling / income strategies
(bearish-neutral). Without knowing the initiating side, PCR is coarse.

Use it as **context about crowding**, never as a standalone signal, and always state which PCR (OI or volume) you
used.

---

## 2. Max Pain

**Definition:** the strike at which the total value of outstanding options (calls + puts) at expiry would be
lowest for option *buyers* — i.e. the price at which the most option premium expires worthless.

**Calculation (mechanical):**

```
for each candidate expiry price S (each strike):
    total_payout = sum over calls: max(0, S - strike) * call_OI
                 + sum over puts:  max(0, strike - S) * put_OI
max_pain = the strike S minimising total_payout
```

(The factor of contract size cancels and can be ignored.)

**What it is:** an arithmetic consequence of the **current** OI distribution.

**What it is not:** a prediction. The market does not have to close at max pain. OI changes continuously, so max
pain moves. And large participants can be positioned to profit from exactly the outcome max pain "predicts"
against.

Honest phrasing: "max pain is currently at 24,000 based on this chain snapshot; historically price has sometimes
drifted toward it into expiry, but this is a tendency, not a rule, and the value changes as OI shifts."

---

## 3. Implied Volatility (IV), IV rank, IV percentile

```
IV         = the volatility input that makes a pricing model reproduce the option's market price
IV rank    = (IV_now - IV_min_52w) / (IV_max_52w - IV_min_52w) * 100
IV pctile  = % of the last 252 trading days with IV below today's IV
```

| Reading | Meaning |
|---------|---------|
| High IV rank | Options are expensive relative to their own history |
| Low IV rank | Options are cheap relative to history |
| IV expanding before an event | The market is pricing uncertainty |
| IV collapsing after an event | "Volatility crush" — long options can lose money even when direction is right |

**The IV crush is the single most important practical fact for beginners:** buying an option before results and
being right on direction can still lose money if IV collapses.

IV rank is **more useful than raw IV**, because IV levels are not comparable across instruments or regimes.

---

## 4. Greeks

| Greek | Definition (per unit price change) | Practical meaning |
|-------|-----------------------------------|-------------------|
| **Delta** | ∂option/∂underlying; ≈ 0 to 1 (calls), 0 to −1 (puts) | Directional exposure; also a rough probability proxy (contested) |
| **Gamma** | ∂delta/∂underlying | How fast delta changes; high near expiry at the money |
| **Theta** | ∂option/∂time | Daily decay; the cost of holding long options |
| **Vega** | ∂option/∂IV | Sensitivity to implied volatility |

Approximate Black-Scholes behaviour worth knowing:

- **ATM options have the highest gamma and vega**, and are most sensitive to theta relative to value.
- **Gamma rises sharply into expiry** for ATM strikes — risk for sellers, opportunity for buyers.
- **Theta decay accelerates in the final week** for ATM options.
- **Deep ITM options behave like the underlying** (delta ≈ 1, gamma ≈ 0).
- **Deep OTM options are almost pure vega/theta** plays.

Greeks are model outputs, not market facts. Different models and inputs (rate, dividend, volatility surface) give
different values.

---

## 5. What to report, and how

```
Chain snapshot   : NIFTY expiry 2026-11-27, retrieved 2026-11-14 15:20 IST (source: <provider>)
PCR (OI)         : 1.08
Max pain         : 24,000 (computed from this snapshot)
ATM IV           : 12.4%; IV rank 38 (over 52 weeks)
Greeks (ATM)     : delta 0.51, gamma 0.0004, theta -18/day, vega 42
Interpretation   : IV is mid-range; no obvious vol extreme. PCR near 1 means no strong crowding signal.
                   Max pain at 24,000 is 180 points below spot — I would not treat that as a target.
Limitations      : snapshot, not live; PCR cannot distinguish bought vs sold options; max pain moves with OI.
```

## 6. Common errors

| Error | Guard |
|-------|-------|
| Quoting IV without a source | Chain data required |
| Treating max pain as a target | It is a computation, not a forecast |
| Reading PCR as a signal | Coarse crowding measure only |
| Ignoring IV crush around events | The most common beginner loss |
| Using delta as a literal probability | It is a hedge ratio; the probability interpretation is approximate and model-dependent |
| Comparing raw IV across stocks | Use IV rank |
| Quoting an expiry date from memory | Verify against the exchange calendar |

## 7. Beginner summary (Hinglish)

**PCR (Put-Call Ratio):** put OI ÷ call OI. Bahut zyada put = log darr rahe hain (ya puts bech rahe hain — pata
nahi). **Akela signal nahi hai.**

**Max Pain:** woh strike jahan sabse zyada option premium zero par expire hota hai. Yeh **calculation** hai,
prediction nahi. Market ko max pain par jaana zaroori nahi.

**IV (Implied Volatility):** option kitna mehnga hai. **IV rank** zyada = option mehnga, kam = sasta.

**Sabse important practical baat:** result ke pehle option kharidna — direction sahi hone par bhi **IV crush** se
loss ho sakta hai.

**Greeks:** delta = direction, gamma = delta kitna badlega, theta = roz ka time decay (long option ka kharcha),
vega = IV ke liye sensitivity.

## 8. Exercise

Compute max pain for one chain snapshot by hand (spreadsheet). Then note where price closed at expiry. Do this for
four expiries. Write down whether max pain was closer to the expiry price than the starting spot — and be honest
about the sample size.

---
*See also: [`options-chain.md`](options-chain.md) · [`open-interest.md`](open-interest.md) ·
[`../../engines/options-intelligence/README.md`](../../engines/options-intelligence/README.md)*
