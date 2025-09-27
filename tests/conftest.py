from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is importable when running tests without installation
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
