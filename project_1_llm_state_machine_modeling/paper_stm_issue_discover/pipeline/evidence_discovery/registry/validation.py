from __future__ import annotations

from collections import Counter
from typing import Any


EXPECTED_FAMILIES = {
    "structure": 6,
    "topology": 4,
    "trajectory": 4,
    "bounded_verification": 5,
}


def validate_registry(data: dict[str, Any]) -> None:
    if data.get("schema") != "evidence-discovery.predicate-registry.v1":
        raise ValueError("registry schema mismatch")
    if data.get("registry_version") != "four-family-19-core.v1":
        raise ValueError("registry version is not the frozen v1 registry")
    if data.get("status") != "frozen-design":
        raise ValueError("registry is not frozen-design")
    families = data.get("families")
    if not isinstance(families, list):
        raise ValueError("registry families must be a list")
    counts = Counter()
    ids: set[str] = set()
    for family in families:
        family_id = family.get("id")
        if family_id not in EXPECTED_FAMILIES:
            raise ValueError(f"unknown predicate family: {family_id}")
        predicates = family.get("predicates")
        if not isinstance(predicates, list):
            raise ValueError(f"predicates missing for family: {family_id}")
        for predicate in predicates:
            predicate_id = predicate.get("id")
            if not isinstance(predicate_id, str) or predicate_id in ids:
                raise ValueError(f"duplicate or invalid predicate id: {predicate_id}")
            ids.add(predicate_id)
            counts[family_id] += 1
            required = ("name", "semantics", "inputs", "sources", "source_types")
            if any(not predicate.get(field) for field in required):
                raise ValueError(f"incomplete predicate entry: {predicate_id}")
            if any(not isinstance(value, str) or not value.strip() for value in predicate["inputs"]):
                raise ValueError(f"invalid predicate inputs: {predicate_id}")
    if dict(counts) != EXPECTED_FAMILIES or len(ids) != 19:
        raise ValueError(f"frozen predicate shape mismatch: {dict(counts)}")
    if data.get("public_predicate_count") != 19:
        raise ValueError("public predicate count mismatch")
    if data.get("w1_is_semantic_hit") is not True:
        raise ValueError("W1 semantic hit contract missing")
    if data.get("unknown_is_violation") is not False:
        raise ValueError("UNKNOWN violation contract missing")

