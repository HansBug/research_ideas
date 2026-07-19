from __future__ import annotations

import hashlib
import json
from pathlib import Path


IMPLEMENTATION_ROOTS = (
    "pipeline/conversion/java/plantuml-state-frontend/src/main/java",
    "pipeline/conversion/java/plantuml-state-frontend/Makefile",
    "pipeline/conversion/src/paper_stm_repair_conversion/adapters/plantuml_source.py",
    "pipeline/conversion/src/paper_stm_repair_conversion/evidence_integrity.py",
    "pipeline/representation/src/paper_stm_repair_representation",
    "pipeline/representation/schemas/working_fcstm_contract.schema.json",
    "pipeline/representation/schemas/manual_pair_review.schema.json",
    "pipeline/conversion/tools/run_llms_emp_r45.py",
    "pipeline/conversion/tools/build_llms_emp_pair_pages.py",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relevant_implementation_sha256(*, repo_root: Path, paper_root: Path) -> str:
    rows: list[tuple[str, str]] = []
    for relative_root in IMPLEMENTATION_ROOTS:
        root = paper_root / relative_root
        paths = sorted(root.rglob("*")) if root.is_dir() else [root]
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.resolve().relative_to(repo_root.resolve()).as_posix()
            rows.append((relative, _sha256_bytes(path.read_bytes())))
    payload = json.dumps(
        rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return _sha256_bytes(payload)
