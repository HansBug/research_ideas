"""Load the R1 predicate/polarity publication decisions without altering runtime facts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..registry.model import PredicateRegistry


_POLARITIES = ("true", "false")
_CATALOG_RELATIVE_PATH = Path("related_work/provenance/current_source_catalog.json")


@dataclass(frozen=True)
class PublicationEligibilityAudit:
    """Boolean strongest-claim decisions derived from the paper-side R1 audit catalog."""

    catalog_hash: str | None
    by_predicate: dict[str, dict[str, bool]]
    reason: str


def default_publication_audit_path() -> Path:
    """Return the paper-side audit catalog when this is a source checkout."""

    return Path(__file__).resolve().parents[4] / _CATALOG_RELATIVE_PATH


def load_publication_eligibility_audit(
    registry: PredicateRegistry,
    *,
    catalog_path: Path | None = None,
) -> PublicationEligibilityAudit:
    """Return exact Boolean-polarity strongest-claim eligibility, failing closed.

    The frozen method registry contains predicate semantics, whereas the R1
    paper-side catalog carries publication interpretation.  Keeping the latter
    outside the registry prevents a citation-audit revision from rewriting a
    frozen runtime artifact.  A missing or malformed catalog returns explicit
    false decisions for every registry predicate rather than raising a runtime
    a stronger paper claim.
    """

    closed = {predicate_id: {polarity: False for polarity in _POLARITIES} for predicate_id in registry.predicates}
    path = catalog_path or default_publication_audit_path()
    try:
        raw_bytes = path.read_bytes()
        payload = json.loads(raw_bytes.decode("utf-8"))
        by_predicate = _parse_catalog(payload, registry)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        return PublicationEligibilityAudit(
            catalog_hash=None,
            by_predicate=closed,
            reason=f"publication audit unavailable or invalid: {type(exc).__name__}",
        )
    return PublicationEligibilityAudit(
        catalog_hash="sha256:" + hashlib.sha256(raw_bytes).hexdigest(),
        by_predicate=by_predicate,
        reason="validated paper-side R1 predicate/polarity publication audit",
    )


def _parse_catalog(payload: Any, registry: PredicateRegistry) -> dict[str, dict[str, bool]]:
    if not isinstance(payload, dict) or payload.get("registry_version") != registry.version:
        raise ValueError("publication audit registry version mismatch")
    audit = payload.get("r1_citation_audit")
    if not isinstance(audit, dict) or audit.get("status") != "complete_publication_audit":
        raise ValueError("publication audit is not complete")
    rows = audit.get("predicate_audits")
    if not isinstance(rows, list):
        raise ValueError("publication audit has no predicate rows")
    by_id: dict[str, dict[str, bool]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("publication audit contains a non-object predicate row")
        predicate_id = row.get("predicate_id")
        rules = row.get("publication_eligibility_by_polarity")
        if not isinstance(predicate_id, str) or not isinstance(rules, dict):
            raise ValueError("publication audit predicate row is incomplete")
        if predicate_id in by_id or set(rules) != {"true", "false", "unknown", "failure"}:
            raise ValueError("publication audit predicate/polarity keys are not exact")
        eligible: dict[str, bool] = {}
        for polarity in _POLARITIES:
            rule = rules[polarity]
            if not isinstance(rule, dict):
                raise ValueError("publication audit polarity rule is not an object")
            ceiling = rule.get("runtime_witness_ceiling")
            eligibility = rule.get("publication_eligibility")
            if ceiling not in {"W0", "W1", "W2", "NOT_APPLICABLE"} or eligibility not in {
                "ELIGIBLE", "CONDITIONAL", "INELIGIBLE"
            }:
                raise ValueError("publication audit polarity rule has an unknown enum")
            eligible[polarity] = eligibility == "ELIGIBLE" and ceiling == "W2"
        by_id[predicate_id] = eligible
    if set(by_id) != set(registry.predicates):
        raise ValueError("publication audit predicate keyset does not match frozen registry")
    return by_id
