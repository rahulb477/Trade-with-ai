"""Backend package for AI Trading Intelligence Web Application.

Integrates directly with ``integrations/python/trading_intel`` and the V1+V2+V3
skill knowledge repository. Uses Python standard library only so it runs in any
Python 3.9+ environment without external runtime dependencies.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_LIB = os.path.join(REPO_ROOT, "integrations", "python")
if PYTHON_LIB not in sys.path:
    sys.path.insert(0, PYTHON_LIB)
