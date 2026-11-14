"""Test package.

Adds ``integrations/python`` to ``sys.path`` so the library can be imported
without installation. Run the suite with::

    python3 -m unittest discover -s tests -t . -v
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LIB = os.path.join(_ROOT, "integrations", "python")
if _LIB not in sys.path:
    sys.path.insert(0, _LIB)

REPO_ROOT = _ROOT
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
