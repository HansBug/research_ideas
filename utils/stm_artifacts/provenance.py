from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain(
    *,
    pair_id: str,
    nl_path: Path,
    model_path: Path,
    model_hash: str,
    obligation_id: str,
    plan_id: str | None,
    receipt_id: str | None,
) -> dict[str, Any]:
    return {
        "requirement": {
            "pair_id": pair_id,
            "obligation_id": obligation_id,
            "path": str(nl_path),
            "hash": sha256_file(nl_path),
        },
        "model": {
            "path": str(model_path),
            "hash": model_hash,
        },
        "plan": {"plan_id": plan_id, "reason": "The compiled plan is determined by the frozen registry and bound inputs."},
        "receipt": {"receipt_id": receipt_id, "reason": "The backend receipt was produced by the deterministic execution backend."},
    }
