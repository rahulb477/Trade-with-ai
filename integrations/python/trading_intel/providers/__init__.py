"""Provider layer — a documented interface with no bundled credentials.

The repository ships an interface and a reference in-memory provider so that the
rest of the library can be exercised offline. It deliberately ships **no**
network adapter: a working adapter requires a provider's terms, a key, and
current knowledge of its API, none of which can be assumed here.
"""

from .base import (
    Bar,
    Chain,
    NotSupported,
    Provider,
    ProviderError,
    Quote,
    InMemoryProvider,
    describe_environment,
    validate_bars,
)

__all__ = [
    "Bar",
    "Chain",
    "NotSupported",
    "Provider",
    "ProviderError",
    "Quote",
    "InMemoryProvider",
    "describe_environment",
    "validate_bars",
]
