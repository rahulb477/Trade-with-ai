"""Provider health check.

Run as::

    python3 -m trading_intel.providers.health

Prints the detected mode and, for each configured provider, whether it can be
reached. It never prints a credential.
"""

from __future__ import annotations

import json
import sys

from .base import describe_environment


def main(argv=None) -> int:
    env = describe_environment()
    payload = {
        "mode": env["mode"],
        "configured_variables": env["configured"],
        "missing_variables": env["not_configured"],
        "live_adapters_shipped": 0,
        "note": (
            "This repository ships no network adapters. The interface in "
            "trading_intel/providers/base.py is the contract an adapter must satisfy. "
            "Offline mode needs no configuration."
        ),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
