# Forex Markets

## 1. Structure

| Feature | Detail |
|---------|--------|
| Market | Over-the-counter (decentralised), no single exchange |
| Sessions | Sydney → Tokyo → London → New York, roughly 24 hours, 5 days a week |
| Weekly window | Opens Sunday ~22:00 GMT (Sydney), closes Friday ~22:00 GMT (New York) |
| Main pairs | EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD |
| Crosses | EUR/GBP, EUR/JPY, GBP/JPY, etc. |
| Quote convention | Base/quote — `EUR/USD = 1.0850` means 1 EUR = 1.0850 USD |
| Pip | 0.0001 for most pairs; **0.01 for JPY pairs** |

**Pricing differences:** retail brokers quote slightly different spreads and prices. There is no consolidated tape.
Two charts can legitimately differ by a few pips — do not call one of them "wrong".

## 2. Session behaviour

| Session | Characteristics |
|---------|-----------------|
| Tokyo (Asian) | Lower volatility; JPY and AUD most active; ranges often form |
| London open | Highest liquidity; the most common breakout window |
| London/NY overlap (12:00–16:00 GMT) | Highest volume of the day; the biggest moves often occur here |
| New York close / rollover | Spreads widen; a rollover cost applies around 17:00 New York |

**Rollover** is where brokers apply financing adjustments; charts sometimes show a small gap there. Not a market
event.

## 3. Drivers

| Driver | Effect |
|--------|--------|
| Interest-rate differentials | The primary medium-term driver |
| Central-bank policy (Fed, ECB, BoE, BoJ, RBA, BoC, SNB) | First-order |
| Inflation prints | Rate expectations |
| Employment data | Growth expectations |
| Risk sentiment / VIX | JPY and CHF strengthen in risk-off (typical) |
| Commodity prices | AUD (metals), CAD (oil), NOK (oil) |
| DXY | The aggregate dollar read |

## 4. Conventions that trip people up

| Convention | Note |
|------------|------|
| JPY pairs quote to 3 decimals | `USD/JPY = 154.250`; a pip is 0.01 |
| Inverse pairs | EUR/USD and USD/CHF can move "opposite" but are not mirror images |
| Leverage | Very high (often 20–50× retail); risk per idea must be far smaller in R terms |
| Swap/carry | Holding positions overnight has a financing cost or credit |
| No volume | Retail forex has no true volume — OBV, VWAP, volume profile are **unavailable** or broker-proxy only |

**Critical consequence:** any indicator requiring volume (OBV, VWAP, volume profile, MFI, CVD) cannot be computed
from retail forex data. If a chart shows such a panel, it is a tick-count proxy — say so.

## 5. Common errors

| Error | Guard |
|-------|-------|
| Treating forex as 24/7 | It is 24/5; there is a weekly close |
| Using 0.0001 for a JPY pair | JPY pip is 0.01 |
| Applying volume-based indicators | No true volume |
| Ignoring rollover/swap | Affects multi-day P&L |
| Assuming a single "true" price | It is decentralised |
| Forgetting the timezone when quoting a session | Always UTC or New York time |

## 6. Hinglish summary

**Forex 24/5 hai**, 24/7 nahi — Friday raat band, Sunday raat khulta hai.

**Pip:** zyadatar pairs mein 0.0001, par **JPY pairs mein 0.01**.

**Session:** London open sabse active, aur London–New York overlap mein sabse bade moves.

**Sabse zaroori:** retail forex mein **asli volume nahi** hota — isliye OBV, VWAP, volume profile use mat karo.

**Leverage bahut zyada** hota hai — isliye risk per idea bahut chhota rakhna padta hai.
