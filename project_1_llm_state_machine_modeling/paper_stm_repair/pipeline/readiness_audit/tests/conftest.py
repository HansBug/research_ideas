from __future__ import annotations

import sys
from pathlib import Path


def _repo_root() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PIPELINE = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline"
for src in [
    PIPELINE / "readiness_audit/src",
    PIPELINE / "representation/src",
    PIPELINE / "conversion/src",
]:
    src_str = str(src)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
