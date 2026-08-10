from __future__ import annotations

import sys
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parent
for src in [
    PIPELINE_ROOT / "conversion/src",
    PIPELINE_ROOT / "evaluation/src",
    PIPELINE_ROOT / "representation/src",
    PIPELINE_ROOT / "readiness_audit/src",
]:
    if src.exists():
        src_str = str(src)
        if src_str not in sys.path:
            sys.path.insert(0, src_str)
