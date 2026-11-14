"""Provider interface, normalisation and environment detection.

Design notes
------------
* ``Provider`` is a ``typing.Protocol``: adapters do not need to subclass it.
* Every adapter must normalise into :class:`Bar` before anything else sees the
  data, so the rest of the library never deals with provider-specific shapes.
* Credentials are read from the environment only. ``describe_environment``
  reports *which* variables are present — never their values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Protocol, Sequence, runtime_checkable


class ProviderError(RuntimeError):
    """Raised by an adapter when a request cannot be completed."""


class NotSupported(ProviderError):
    """Raised when a provider does not offer the requested data type."""


@dataclass
class Bar:
    timestamp: str          # ISO 8601 with an offset
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None   # None when genuinely unavailable — never 0
    symbol: str = ""
    timeframe: str = ""
    source: str = ""
    adjusted: bool = False

    def as_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "source": self.source,
            "adjusted": self.adjusted,
        }


@dataclass
class Quote:
    symbol: str
    last: float
    timestamp: str
    source: str = ""
    change_pct: Optional[float] = None


@dataclass
class Chain:
    symbol: str
    expiry: str
    timestamp: str
    strikes: List[float] = field(default_factory=list)
    call_oi: List[float] = field(default_factory=list)
    put_oi: List[float] = field(default_factory=list)
    call_volume: List[float] = field(default_factory=list)
    put_volume: List[float] = field(default_factory=list)
    iv: List[Optional[float]] = field(default_factory=list)
    source: str = ""

    def pcr(self) -> Optional[float]:
        """Put/call ratio by open interest."""
        total_calls = sum(self.call_oi)
        total_puts = sum(self.put_oi)
        if total_calls <= 0:
            return None
        return total_puts / total_calls


@runtime_checkable
class Provider(Protocol):
    """The interface every adapter must satisfy."""

    name: str
    requires_credentials: bool

    def fetch_ohlcv(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> List[Bar]:
        ...

    def fetch_quote(self, symbol: str) -> Quote:
        ...

    def fetch_option_chain(self, symbol: str, expiry: str) -> Chain:
        ...

    def health(self) -> dict:
        ...


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
def validate_bars(bars: Sequence[Bar]) -> List[str]:
    """Return a list of problems. An empty list means the series is usable."""
    problems: List[str] = []
    prev_ts: Optional[str] = None
    for i, bar in enumerate(bars):
        if bar.high < max(bar.open, bar.close):
            problems.append(f"bar {i}: high below open/close")
        if bar.low > min(bar.open, bar.close):
            problems.append(f"bar {i}: low above open/close")
        if bar.high < bar.low:
            problems.append(f"bar {i}: high below low")
        if bar.close <= 0:
            problems.append(f"bar {i}: non-positive close")
        if bar.volume is not None and bar.volume < 0:
            problems.append(f"bar {i}: negative volume")
        if not bar.source:
            problems.append(f"bar {i}: missing source")
        if prev_ts is not None and bar.timestamp <= prev_ts:
            problems.append(f"bar {i}: timestamp not increasing")
        prev_ts = bar.timestamp
    return problems


# --------------------------------------------------------------------------
# reference implementation (offline, in-memory)
# --------------------------------------------------------------------------
class InMemoryProvider:
    """A provider backed by a dict. Used by tests and by the examples.

    It exists so the library can be demonstrated end-to-end with zero network
    access, and so that tests never depend on live data.
    """

    name = "in-memory"
    requires_credentials = False

    def __init__(self, series: Dict[str, Dict[str, List[float]]],
                 timestamps: Optional[Dict[str, List[str]]] = None) -> None:
        self._series = series
        self._timestamps = timestamps or {}
        self._quotes: Dict[str, Quote] = {}

    def fetch_ohlcv(self, symbol: str, timeframe: str, start=None, end=None) -> List[Bar]:
        if symbol not in self._series:
            raise ProviderError(f"unknown symbol: {symbol}")
        data = self._series[symbol]
        n = len(data["close"])
        ts = self._timestamps.get(symbol)
        if ts is None:
            ts = [f"2026-01-01T00:00:00+00:00"] * n
        volume = data.get("volume")
        bars = [
            Bar(
                timestamp=ts[i],
                open=data["open"][i],
                high=data["high"][i],
                low=data["low"][i],
                close=data["close"][i],
                volume=volume[i] if volume else None,
                symbol=symbol,
                timeframe=timeframe,
                source=self.name,
                adjusted=True,
            )
            for i in range(n)
        ]
        return bars

    def fetch_quote(self, symbol: str) -> Quote:
        if symbol in self._quotes:
            return self._quotes[symbol]
        if symbol in self._series:
            closes = self._series[symbol]["close"]
            return Quote(symbol=symbol, last=closes[-1], timestamp="2026-01-01T00:00:00+00:00",
                         source=self.name)
        raise ProviderError(f"unknown symbol: {symbol}")

    def fetch_option_chain(self, symbol: str, expiry: str) -> Chain:
        raise NotSupported("in-memory provider has no option chain")

    def health(self) -> dict:
        return {
            "status": "ok",
            "symbols": sorted(self._series),
            "requires_credentials": False,
            "notes": "offline reference provider",
        }


# --------------------------------------------------------------------------
# environment detection
# --------------------------------------------------------------------------
KNOWN_ENV_VARS = (
    "TI_MARKET_DATA_PROVIDER",
    "TI_MARKET_DATA_KEY",
    "TI_NEWS_PROVIDER",
    "TI_NEWS_KEY",
    "TI_CACHE_DIR",
    "TI_LOG_LEVEL",
)


def describe_environment(env: Optional[Dict[str, str]] = None) -> Dict[str, object]:
    """Report which recognised variables are set, without revealing values.

    Never returns a key's contents. If you find yourself wanting the value,
    the calling code is wrong.
    """
    source = os.environ if env is None else env
    present = [name for name in KNOWN_ENV_VARS if source.get(name)]
    missing = [name for name in KNOWN_ENV_VARS if not source.get(name)]

    if "TI_MARKET_DATA_KEY" in present and "TI_MARKET_DATA_PROVIDER" in present:
        mode = "FULL RESEARCH MODE (market data configured)"
    elif present:
        mode = "PARTIAL CONFIGURATION (some variables set; check the adapter)"
    else:
        mode = "OFFLINE KNOWLEDGE MODE (no credentials configured — fully functional)"

    return {
        "configured": present,
        "not_configured": missing,
        "mode": mode,
        "note": "values are never read into this report; only presence is checked",
    }
