from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .model import Predicate, PredicateRegistry
from .validation import validate_registry


def load_registry(path: str | Path | None = None) -> PredicateRegistry:
    registry_path = (
        Path(path)
        if path is not None
        else Path(__file__).resolve().parents[1] / "predicate_registry.json"
    ).resolve()
    raw_bytes = registry_path.read_bytes()
    raw: dict[str, Any] = json.loads(raw_bytes.decode("utf-8"))
    validate_registry(raw)
    source_catalog_value = raw.get("source_catalog_path")
    source_catalog_path = None
    source_audit: dict[str, dict[str, Any]] | None = None
    if isinstance(source_catalog_value, str) and source_catalog_value.strip():
        # The registry path is two directory levels below the paper root:
        # <paper>/pipeline/evidence_discovery/predicate_registry.json.
        source_catalog_path = (registry_path.parents[2] / source_catalog_value).resolve()
        catalog = json.loads(source_catalog_path.read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or catalog.get("registry_version") != raw.get("registry_version"):
            raise ValueError("predicate source catalog does not match frozen registry")
        audit = catalog.get("predicate_audit")
        if not isinstance(audit, dict):
            raise ValueError("predicate source catalog is missing predicate_audit")
        source_audit = {
            str(predicate_id): dict(value)
            for predicate_id, value in audit.items()
            if isinstance(value, dict)
        }
    predicates: dict[str, Predicate] = {}
    families: dict[str, tuple[str, ...]] = {}
    for family in raw["families"]:
        ids: list[str] = []
        for item in family["predicates"]:
            predicate = Predicate(
                id=item["id"],
                name=item["name"],
                family=family["id"],
                semantics=item["semantics"],
                inputs=tuple(item["inputs"]),
                sources=tuple(item["sources"]),
                source_types=tuple(item["source_types"]),
                soundness_fragment=(
                    f"{family['label']}: {item['semantics']} "
                    "仅在声明的封闭输入和边界内成立。"
                ),
            )
            predicates[predicate.id] = predicate
            ids.append(predicate.id)
        families[family["id"]] = tuple(ids)
    return PredicateRegistry(
        version=raw["registry_version"],
        registry_hash="sha256:" + hashlib.sha256(raw_bytes).hexdigest(),
        predicates=predicates,
        families=families,
        raw=raw,
        source_catalog_path=source_catalog_path,
        source_audit=source_audit,
    )
