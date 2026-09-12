"""Evaluation-only native-object relation oracles for predicate gold.

The contracts in this module inspect pyfcstm states, events, hierarchy links,
and provenance-preserving authored transition carriers. They do not implement
an FCSTM parser or runtime and are intentionally outside the frozen method
package and predicate registry.
"""

from __future__ import annotations

import argparse
import inspect
import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import Field, JsonValue, model_validator

from .predicate_gold import (
    SHA256_PATTERN,
    ExactnessRelation,
    StrictModel,
    TypedInput,
    canonical_sha256,
    sha256_path,
    write_json,
)

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.relation-oracle-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.relation-oracle-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.relation-oracle-replay.v1"


class RelationOracleId(str, Enum):
    """Narrow native relation contracts admitted by this evaluator."""

    FORBIDDEN_SIGNATURES_ABSENT = "FORBIDDEN_SIGNATURES_ABSENT"
    REQUIRED_SIGNATURE_PRESENT = "REQUIRED_SIGNATURE_PRESENT"
    UNIQUE_STATE_DIRECT_PARENT = "UNIQUE_STATE_DIRECT_PARENT"
    DIRECT_CHILD_HIERARCHY = "DIRECT_CHILD_HIERARCHY"
    ANCESTOR_EVENT_TARGET_COVERAGE = "ANCESTOR_EVENT_TARGET_COVERAGE"


class ArtifactRole(str, Enum):
    """Role of the FCSTM artifact evaluated by the relation oracle."""

    DEFECTIVE = "DEFECTIVE"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"


class RelationOracleRequest(StrictModel):
    """Hash-bound pre-result request for one native relation contract."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(
        default=REQUEST_SCHEMA_VERSION,
        description="Evaluation-only relation-oracle request schema version.",
    )
    request_id: str = Field(
        description="Stable request identity.", pattern=r"^[A-Za-z0-9_.:-]+$"
    )
    ledger_id: str = Field(
        description="Immutable ledger issue owning the property.", min_length=1
    )
    property_id: str = Field(
        description="Selected pre-execution property identity.", min_length=1
    )
    property_proposal_sha256: str = Field(
        description="Hash of the proposal frozen before execution output was visible.",
        pattern=SHA256_PATTERN,
    )
    exactness_relation: Literal[
        ExactnessRelation.EQUIVALENT,
        ExactnessRelation.O_IMPLIES_P,
    ] = Field(
        description="Exact equivalence or sound necessary-condition direction fixed before execution."
    )
    oracle_id: RelationOracleId = Field(
        description="Narrow native-object relation contract."
    )
    artifact_role: ArtifactRole = Field(
        description="Defective artifact or independently justified positive control."
    )
    artifact_path: str = Field(
        description="Repository-relative FCSTM artifact path.", min_length=1
    )
    artifact_sha256: str = Field(
        description="SHA-256 of the exact FCSTM bytes.", pattern=SHA256_PATTERN
    )
    typed_inputs: tuple[TypedInput, ...] = Field(
        description="Source-provenanced identities and finite sets frozen before execution.",
        min_length=1,
    )
    assumptions: tuple[str, ...] = Field(
        description="Explicit source-static assumptions bounding the property."
    )
    expected_boolean_for_acceptance: bool = Field(
        description="False for defective artifacts and true for controls."
    )
    created_at: str = Field(description="UTC proposal freeze time.", min_length=1)
    request_sha256: str = Field(
        description="Canonical request hash excluding this field.",
        pattern=SHA256_PATTERN,
    )

    @model_validator(mode="after")
    def validate_request(self) -> RelationOracleRequest:
        """Enforce each oracle's input vocabulary, role polarity, and digest."""

        names = [item.field_name for item in self.typed_inputs]
        expected = {
            RelationOracleId.FORBIDDEN_SIGNATURES_ABSENT: {"forbidden_signatures"},
            RelationOracleId.REQUIRED_SIGNATURE_PRESENT: {"required_signature"},
            RelationOracleId.UNIQUE_STATE_DIRECT_PARENT: {"state", "expected_parent"},
            RelationOracleId.DIRECT_CHILD_HIERARCHY: {"expected_hierarchy"},
            RelationOracleId.ANCESTOR_EVENT_TARGET_COVERAGE: {
                "required_sources",
                "events",
                "target",
            },
        }[self.oracle_id]
        if set(names) != expected or len(names) != len(expected):
            raise ValueError(
                f"{self.oracle_id.value} requires exactly {sorted(expected)}"
            )
        values = {item.field_name: item.normalized_value for item in self.typed_inputs}
        if self.oracle_id == RelationOracleId.FORBIDDEN_SIGNATURES_ABSENT:
            self._validate_signatures(values["forbidden_signatures"], allow_many=True)
        elif self.oracle_id == RelationOracleId.REQUIRED_SIGNATURE_PRESENT:
            self._validate_signatures(values["required_signature"], allow_many=False)
        elif self.oracle_id == RelationOracleId.UNIQUE_STATE_DIRECT_PARENT:
            state_input = next(
                item for item in self.typed_inputs if item.field_name == "state"
            )
            if not isinstance(state_input.value, str) or not state_input.value:
                raise TypeError(
                    "state.value must retain the exact local source identity"
                )
            if (
                not isinstance(state_input.normalized_value, str)
                or not state_input.normalized_value
            ):
                raise TypeError(
                    "state.normalized_value must be the required canonical path"
                )
            if (
                not isinstance(values["expected_parent"], str)
                or not values["expected_parent"]
            ):
                raise TypeError("expected_parent must be one canonical path")
        elif self.oracle_id == RelationOracleId.DIRECT_CHILD_HIERARCHY:
            hierarchy = values["expected_hierarchy"]
            if not isinstance(hierarchy, dict) or set(hierarchy) != {
                "parent",
                "direct_children",
            }:
                raise TypeError(
                    "expected_hierarchy must contain parent and direct_children"
                )
            if not isinstance(hierarchy["parent"], str) or not hierarchy["parent"]:
                raise TypeError("expected_hierarchy.parent must be one canonical path")
            children = hierarchy["direct_children"]
            if (
                not isinstance(children, list)
                or not children
                or not all(isinstance(item, str) and item for item in children)
            ):
                raise TypeError(
                    "expected_hierarchy.direct_children must be a nonempty name array"
                )
        else:
            sources = values["required_sources"]
            events = values["events"]
            if (
                not isinstance(sources, list)
                or not sources
                or not all(isinstance(item, str) and item for item in sources)
            ):
                raise TypeError(
                    "required_sources must be a nonempty canonical-path array"
                )
            if (
                not isinstance(events, list)
                or not events
                or not all(isinstance(item, str) and item for item in events)
            ):
                raise TypeError("events must be a nonempty canonical-path array")
            if not isinstance(values["target"], str) or not values["target"]:
                raise TypeError("target must be one canonical path")
        if (
            self.artifact_role == ArtifactRole.DEFECTIVE
            and self.expected_boolean_for_acceptance is not False
        ):
            raise ValueError("defective requests pre-register false")
        if (
            self.artifact_role == ArtifactRole.POSITIVE_CONTROL
            and self.expected_boolean_for_acceptance is not True
        ):
            raise ValueError("positive-control requests pre-register true")
        expected_hash = canonical_sha256(
            self.model_dump(mode="json", exclude={"request_sha256"})
        )
        if self.request_sha256 != expected_hash:
            raise ValueError("request_sha256 does not match the pre-result request")
        return self

    @staticmethod
    def _validate_signatures(value: JsonValue, *, allow_many: bool) -> None:
        """Validate the closed owner/source/event/target signature shape."""

        rows = value if allow_many else [value]
        if not isinstance(rows, list) or not rows:
            raise TypeError("signature input must be a nonempty object or array")
        for row in rows:
            if not isinstance(row, dict) or set(row) != {
                "owner",
                "source",
                "event",
                "target",
            }:
                raise TypeError(
                    "each signature requires owner, source, event, and target"
                )
            if not all(isinstance(row[key], str) and row[key] for key in row):
                raise TypeError("signature fields must be nonempty strings")


class RelationConstituent(StrictModel):
    """One completed Boolean constituent of a native relation property."""

    constituent_id: str = Field(description="Stable check identity.", min_length=1)
    verdict: bool = Field(description="Completed Boolean result.")
    expected: JsonValue = Field(description="Pre-registered relation or identity.")
    observed: JsonValue = Field(
        description="Native pyfcstm observation used by the check."
    )
    reason: str = Field(
        description="How the observation determines the Boolean.", min_length=1
    )


class RelationOracleReceipt(StrictModel):
    """Hash-sealed completed Boolean receipt for a native relation query."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(
        default=RECEIPT_SCHEMA_VERSION,
        description="Evaluation-only relation-oracle receipt schema version.",
    )
    request_id: str = Field(description="Request identity.", min_length=1)
    request_sha256: str = Field(
        description="Hash of the pre-result request.", pattern=SHA256_PATTERN
    )
    ledger_id: str = Field(
        description="Ledger issue owning the property.", min_length=1
    )
    property_id: str = Field(description="Selected property identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(
        description="Pre-execution O/P relation preserved in the receipt."
    )
    oracle_id: RelationOracleId = Field(
        description="Executed native relation contract."
    )
    artifact_role: ArtifactRole = Field(
        description="Defective artifact or positive control."
    )
    artifact_path: str = Field(
        description="Repository-relative FCSTM path.", min_length=1
    )
    artifact_sha256: str = Field(
        description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN
    )
    state: Literal["COMPLETED_BOOLEAN"] = Field(
        description="Only completed Booleans are persisted."
    )
    verdict: bool = Field(description="Conjunction of every persisted constituent.")
    acceptance_match: bool = Field(
        description="Whether verdict equals the pre-registered expected Boolean."
    )
    observations: tuple[dict[str, JsonValue], ...] = Field(
        description="Native state/event/carrier inventory used by the query."
    )
    constituents: tuple[RelationConstituent, ...] = Field(
        description="All constituents evaluated without short-circuiting.", min_length=1
    )
    query_path: str = Field(
        description="Receipt-root-relative query JSON path.", min_length=1
    )
    query_sha256: str = Field(
        description="Hash of the exact query JSON bytes.", pattern=SHA256_PATTERN
    )
    code_hashes: dict[str, str] = Field(
        description="Hashes of oracle, pyfcstm model, and projection code.",
        min_length=3,
    )
    source_commit: str = Field(
        description="Main repository commit used for execution.",
        pattern=r"^[0-9a-f]{40}$",
    )
    pyfcstm_commit: str = Field(
        description="Pinned pyfcstm commit used for execution.",
        pattern=r"^[0-9a-f]{40}$",
    )
    command: tuple[str, ...] = Field(
        description="Exact provider-free replay argv.", min_length=1
    )
    started_at: str = Field(description="UTC execution start time.", min_length=1)
    completed_at: str = Field(
        description="UTC execution completion time.", min_length=1
    )
    replay_status: Literal["NOT_REPLAYED"] = Field(
        description="Replay is stored as a separate audit receipt."
    )
    reason: str = Field(
        description="Verdict interpretation preserving the exact/proxy boundary.",
        min_length=1,
    )
    basis: str = Field(
        description="Native API, input, artifact, and source-static basis.",
        min_length=1,
    )
    receipt_sha256: str = Field(
        description="Canonical receipt hash excluding this field.",
        pattern=SHA256_PATTERN,
    )

    @model_validator(mode="after")
    def validate_receipt(self) -> RelationOracleReceipt:
        """Require complete conjunction and a valid receipt digest."""

        if self.verdict != all(item.verdict for item in self.constituents):
            raise ValueError(
                "relation-oracle verdict must equal all constituent Booleans"
            )
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"receipt_sha256"})
        )
        if self.receipt_sha256 != expected:
            raise ValueError("receipt_sha256 does not match receipt payload")
        return self


class RelationReplayReceipt(StrictModel):
    """Independent replay comparison for one native relation query."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(
        default=REPLAY_SCHEMA_VERSION,
        description="Evaluation-only relation-oracle replay schema version.",
    )
    request_sha256: str = Field(
        description="Hash of the replayed request.", pattern=SHA256_PATTERN
    )
    original_receipt_path: str = Field(
        description="Repository-relative original receipt path.", min_length=1
    )
    original_receipt_sha256: str = Field(
        description="Hash of original receipt bytes.", pattern=SHA256_PATTERN
    )
    replay_receipt_path: str = Field(
        description="Replay-root-relative replay receipt path.", min_length=1
    )
    replay_receipt_sha256: str = Field(
        description="Hash of replay receipt bytes.", pattern=SHA256_PATTERN
    )
    original_projection_sha256: str = Field(
        description="Digest of original deterministic observations.",
        pattern=SHA256_PATTERN,
    )
    replay_projection_sha256: str = Field(
        description="Digest of replay deterministic observations.",
        pattern=SHA256_PATTERN,
    )
    overall_match: bool = Field(
        description="Whether the deterministic semantic projections match."
    )
    replayed_at: str = Field(description="UTC replay completion time.", min_length=1)
    receipt_sha256: str = Field(
        description="Canonical replay-audit digest excluding this field.",
        pattern=SHA256_PATTERN,
    )

    @model_validator(mode="after")
    def validate_replay(self) -> RelationReplayReceipt:
        """Bind overall_match and the audit digest to compared projections."""

        if self.overall_match != (
            self.original_projection_sha256 == self.replay_projection_sha256
        ):
            raise ValueError(
                "overall_match does not reflect semantic projection hashes"
            )
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"receipt_sha256"})
        )
        if self.receipt_sha256 != expected:
            raise ValueError("receipt_sha256 does not match replay payload")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _values(request: RelationOracleRequest) -> dict[str, JsonValue]:
    """Return validated normalized inputs."""

    return {item.field_name: item.normalized_value for item in request.typed_inputs}


def _carrier_observation(carrier: object) -> dict[str, JsonValue]:
    """Project public authored-carrier facts used by every relation query."""

    return {
        "owner": carrier.owner_path,
        "source": carrier.source,
        "target": carrier.target,
        "events": [event.path_name for event in carrier.events],
        "has_guard": carrier.guard is not None,
        "source_line": carrier.source_line,
        "combo_origin_id": carrier.combo_origin_id,
        "forced_origin": carrier.forced_origin,
    }


def _signature_matches(carrier: object, signature: dict[str, JsonValue]) -> bool:
    """Compare one carrier with one exact canonical signature."""

    return (
        carrier.owner_path == signature["owner"]
        and carrier.source == str(signature["source"]).rsplit(".", 1)[-1]
        and carrier.target == str(signature["target"]).rsplit(".", 1)[-1]
        and [event.path_name for event in carrier.events] == [signature["event"]]
    )


def _forbidden_absent(
    request: RelationOracleRequest,
    carriers: tuple[object, ...],
) -> tuple[RelationConstituent, ...]:
    """Check every forbidden signature independently without short-circuiting."""

    signatures = _values(request)["forbidden_signatures"]
    assert isinstance(signatures, list)
    results: list[RelationConstituent] = []
    for index, signature in enumerate(signatures):
        assert isinstance(signature, dict)
        matches = [
            _carrier_observation(carrier)
            for carrier in carriers
            if _signature_matches(carrier, signature)
        ]
        results.append(
            RelationConstituent(
                constituent_id=f"forbidden_signature_absent:{index}",
                verdict=not matches,
                expected={"absent": signature},
                observed=matches,
                reason="Enumerated all native authored carriers and required zero exact owner/source/event/target matches.",
            )
        )
    return tuple(results)


def _required_present(
    request: RelationOracleRequest,
    document: object,
    carriers: tuple[object, ...],
) -> tuple[RelationConstituent, ...]:
    """Check declaration and carrier presence independently for one signature."""

    from utils.stm_artifacts.fcstm_native_projection import (
        resolve_event,
        resolve_state,
        state_path,
    )

    signature = _values(request)["required_signature"]
    assert isinstance(signature, dict)
    target = resolve_state(document, signature["target"])
    source = resolve_state(document, signature["source"])
    event = resolve_event(document, signature["event"])
    matches = [
        _carrier_observation(carrier)
        for carrier in carriers
        if _signature_matches(carrier, signature)
    ]
    return (
        RelationConstituent(
            constituent_id="owner_identity",
            verdict=resolve_state(document, signature["owner"]) is not None,
            expected=signature["owner"],
            observed=signature["owner"]
            if resolve_state(document, signature["owner"]) is not None
            else None,
            reason="Resolved the exact canonical owner path through pyfcstm.",
        ),
        RelationConstituent(
            constituent_id="source_identity",
            verdict=source is not None,
            expected=signature["source"],
            observed=state_path(source) if source is not None else None,
            reason="Resolved the exact canonical source state independently of the carrier search.",
        ),
        RelationConstituent(
            constituent_id="event_identity",
            verdict=event is not None,
            expected=signature["event"],
            observed=event.path_name if event is not None else None,
            reason="Resolved the exact canonical event independently of the carrier search.",
        ),
        RelationConstituent(
            constituent_id="target_identity",
            verdict=target is not None,
            expected=signature["target"],
            observed=state_path(target) if target is not None else None,
            reason="Resolved the required target declaration independently of the carrier search.",
        ),
        RelationConstituent(
            constituent_id="required_signature_present",
            verdict=len(matches) == 1,
            expected={"exactly_one": signature},
            observed=matches,
            reason="Required exactly one native authored carrier with the closed signature; declaration failures do not skip this check.",
        ),
    )


def _unique_parent(
    request: RelationOracleRequest, document: object
) -> tuple[RelationConstituent, ...]:
    """Check local-name uniqueness, canonical path, and direct parent separately."""

    from utils.stm_artifacts.fcstm_native_projection import all_states, state_path

    values = _values(request)
    state_input = next(
        item for item in request.typed_inputs if item.field_name == "state"
    )
    local_name = state_input.value
    matches = [state for state in all_states(document) if state.name == local_name]
    observed = [state_path(state) for state in matches]
    unique = matches[0] if len(matches) == 1 else None
    actual_parent = (
        state_path(unique.parent)
        if unique is not None and unique.parent is not None
        else None
    )
    return (
        RelationConstituent(
            constituent_id="local_state_uniqueness",
            verdict=len(matches) == 1,
            expected={"local_name": local_name, "count": 1},
            observed=observed,
            reason="Enumerated native states by the exact requirement-side local identity; fuzzy matching was not used.",
        ),
        RelationConstituent(
            constituent_id="canonical_state_path",
            verdict=unique is not None and state_path(unique) == values["state"],
            expected=values["state"],
            observed=state_path(unique) if unique is not None else None,
            reason="Compared the unique native state's canonical path with the required shared-state path.",
        ),
        RelationConstituent(
            constituent_id="direct_parent",
            verdict=actual_parent == values["expected_parent"],
            expected=values["expected_parent"],
            observed=actual_parent,
            reason="Compared the native direct parent identity; no reachability surrogate was used.",
        ),
    )


def _direct_children(
    request: RelationOracleRequest, document: object
) -> tuple[RelationConstituent, ...]:
    """Check parent identity, non-leaf status, and every required direct child."""

    from utils.stm_artifacts.fcstm_native_projection import resolve_state, state_path

    hierarchy = _values(request)["expected_hierarchy"]
    assert isinstance(hierarchy, dict)
    parent = resolve_state(document, hierarchy["parent"])
    results = [
        RelationConstituent(
            constituent_id="parent_identity",
            verdict=parent is not None,
            expected=hierarchy["parent"],
            observed=state_path(parent) if parent is not None else None,
            reason="Resolved the exact canonical parent path through pyfcstm.",
        ),
        RelationConstituent(
            constituent_id="parent_non_leaf",
            verdict=parent is not None and not parent.is_leaf_state,
            expected=False,
            observed=parent.is_leaf_state if parent is not None else None,
            reason="Read native State.is_leaf_state; child cardinality beyond the required identities is not asserted.",
        ),
    ]
    for child_name in hierarchy["direct_children"]:
        child = parent.substates.get(child_name) if parent is not None else None
        results.append(
            RelationConstituent(
                constituent_id=f"direct_child:{child_name}",
                verdict=child is not None and child.parent is parent,
                expected={"parent": hierarchy["parent"], "child": child_name},
                observed=state_path(child) if child is not None else None,
                reason="Resolved the child only in native parent.substates and verified the direct parent object identity.",
            )
        )
    return tuple(results)


def _carrier_applies_to_source(
    document: object, carrier: object, source: object
) -> bool:
    """Return whether an authored carrier belongs to the source or an active ancestor."""

    from utils.stm_artifacts.fcstm_native_projection import state_path

    current = source
    while current is not None and current.parent is not None:
        if (
            carrier.owner_path == state_path(current.parent)
            and carrier.source == current.name
        ):
            return True
        current = current.parent
    return False


def _ancestor_coverage(
    request: RelationOracleRequest,
    document: object,
    carriers: tuple[object, ...],
) -> tuple[RelationConstituent, ...]:
    """Check every finite source/event cell against source-or-ancestor carriers."""

    from utils.stm_artifacts.fcstm_native_projection import (
        resolve_event,
        resolve_state,
        state_path,
    )

    values = _values(request)
    target = resolve_state(document, values["target"])
    results: list[RelationConstituent] = [
        RelationConstituent(
            constituent_id="target_identity",
            verdict=target is not None,
            expected=values["target"],
            observed=state_path(target) if target is not None else None,
            reason="Resolved the exact response target independently of coverage cells.",
        )
    ]
    for source_path in values["required_sources"]:
        source = resolve_state(document, source_path)
        results.append(
            RelationConstituent(
                constituent_id=f"source_identity:{source_path}",
                verdict=source is not None,
                expected=source_path,
                observed=state_path(source) if source is not None else None,
                reason="Resolved the exact required source before enumerating active-ancestor carriers.",
            )
        )
        for event_path in values["events"]:
            event = resolve_event(document, event_path)
            matches = []
            if source is not None and event is not None and target is not None:
                matches = [
                    _carrier_observation(carrier)
                    for carrier in carriers
                    if _carrier_applies_to_source(document, carrier, source)
                    and carrier.target == target.name
                    and [item.path_name for item in carrier.events] == [event.path_name]
                ]
            results.append(
                RelationConstituent(
                    constituent_id=f"coverage:{source_path}:{event_path}",
                    verdict=bool(matches),
                    expected={
                        "source": source_path,
                        "event": event_path,
                        "target": values["target"],
                    },
                    observed=matches,
                    reason="Enumerated exact source and active-ancestor authored carriers for this finite source/event cell.",
                )
            )
    return tuple(results)


def evaluate_request(
    request: RelationOracleRequest,
    *,
    repo_root: Path,
) -> tuple[tuple[dict[str, JsonValue], ...], tuple[RelationConstituent, ...]]:
    """Load exact bytes and evaluate every constituent using native objects."""

    from utils.stm_artifacts.fcstm_native_projection import (
        all_states,
        all_transition_carriers,
        load_native_document,
        state_path,
    )

    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match the pre-hashed relation request")
    document = load_native_document(artifact.read_text(encoding="utf-8"))
    carriers = all_transition_carriers(document)
    observations = tuple(
        [
            {
                "kind": "state",
                "path": state_path(state),
                "parent": state_path(state.parent) if state.parent else None,
            }
            for state in all_states(document)
        ]
        + [{"kind": "carrier", **_carrier_observation(carrier)} for carrier in carriers]
    )
    if request.oracle_id == RelationOracleId.FORBIDDEN_SIGNATURES_ABSENT:
        constituents = _forbidden_absent(request, carriers)
    elif request.oracle_id == RelationOracleId.REQUIRED_SIGNATURE_PRESENT:
        constituents = _required_present(request, document, carriers)
    elif request.oracle_id == RelationOracleId.UNIQUE_STATE_DIRECT_PARENT:
        constituents = _unique_parent(request, document)
    elif request.oracle_id == RelationOracleId.DIRECT_CHILD_HIERARCHY:
        constituents = _direct_children(request, document)
    else:
        constituents = _ancestor_coverage(request, document, carriers)
    return observations, constituents


def execute_request(
    request: RelationOracleRequest,
    *,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> RelationOracleReceipt:
    """Execute and persist one completed native relation query."""

    from pyfcstm.model import model as pyfcstm_model
    from utils.stm_artifacts import fcstm_native_projection

    started_at = _utc_now()
    observations, constituents = evaluate_request(request, repo_root=repo_root)
    verdict = all(item.verdict for item in constituents)
    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    write_json(query_path, request.model_dump(mode="json"))
    module_path = Path(__file__).resolve()
    model_path = Path(inspect.getsourcefile(pyfcstm_model) or "").resolve()
    projection_path = Path(
        inspect.getsourcefile(fcstm_native_projection) or ""
    ).resolve()
    unsigned = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "request_id": request.request_id,
        "request_sha256": request.request_sha256,
        "ledger_id": request.ledger_id,
        "property_id": request.property_id,
        "exactness_relation": request.exactness_relation,
        "oracle_id": request.oracle_id,
        "artifact_role": request.artifact_role,
        "artifact_path": request.artifact_path,
        "artifact_sha256": request.artifact_sha256,
        "state": "COMPLETED_BOOLEAN",
        "verdict": verdict,
        "acceptance_match": verdict == request.expected_boolean_for_acceptance,
        "observations": observations,
        "constituents": [item.model_dump(mode="json") for item in constituents],
        "query_path": query_path.relative_to(receipt_root).as_posix(),
        "query_sha256": sha256_path(query_path),
        "code_hashes": {
            module_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(
                module_path
            ),
            model_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(
                model_path
            ),
            projection_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(
                projection_path
            ),
        },
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "replay_status": "NOT_REPLAYED",
        "reason": "The hash-frozen native relation query completed with a Boolean; execution does not upgrade its pre-reviewed O/P relation.",
        "basis": "pyfcstm State/Event/Transition objects and parent links plus provenance-preserving authored carriers; no PlantUML regex, fuzzy binding, or custom runtime was used.",
    }
    receipt = RelationOracleReceipt(
        **unsigned, receipt_sha256=canonical_sha256(unsigned)
    )
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def _semantic_projection(receipt: RelationOracleReceipt) -> dict[str, JsonValue]:
    """Return deterministic facts compared by replay."""

    return {
        "request_sha256": receipt.request_sha256,
        "oracle_id": receipt.oracle_id.value,
        "artifact_sha256": receipt.artifact_sha256,
        "state": receipt.state,
        "verdict": receipt.verdict,
        "observations": list(receipt.observations),
        "constituents": [item.model_dump(mode="json") for item in receipt.constituents],
    }


def replay_request(
    request: RelationOracleRequest,
    *,
    original_receipt: RelationOracleReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> RelationReplayReceipt:
    """Re-execute and compare deterministic native observations."""

    replay = execute_request(
        request,
        repo_root=repo_root,
        receipt_root=replay_root,
        source_commit=source_commit,
        pyfcstm_commit=pyfcstm_commit,
        command=command,
    )
    original_projection = canonical_sha256(_semantic_projection(original_receipt))
    replay_projection = canonical_sha256(_semantic_projection(replay))
    replay_receipt_path = replay_root / "receipt.json"
    try:
        original_path = (
            original_receipt_path.resolve().relative_to(repo_root.resolve()).as_posix()
        )
    except ValueError:
        original_path = (
            original_receipt_path.resolve()
            .relative_to(replay_root.resolve().parent)
            .as_posix()
        )
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": original_path,
        "original_receipt_sha256": sha256_path(original_receipt_path),
        "replay_receipt_path": replay_receipt_path.relative_to(replay_root).as_posix(),
        "replay_receipt_sha256": sha256_path(replay_receipt_path),
        "original_projection_sha256": original_projection,
        "replay_projection_sha256": replay_projection,
        "overall_match": original_projection == replay_projection,
        "replayed_at": _utc_now(),
    }
    audit = RelationReplayReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the provider-free execute/replay CLI."""

    parser = argparse.ArgumentParser(
        description="Execute one pre-hashed predicate-gold relation oracle."
    )
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-against", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate and execute an original or replay relation-oracle request."""

    args = _parser().parse_args(argv)
    request = RelationOracleRequest.model_validate_json(
        args.request.read_text(encoding="utf-8")
    )
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_relation_oracle",
        "--request",
        str(args.request),
        "--repo-root",
        str(args.repo_root),
        "--receipt-root",
        str(args.receipt_root),
        "--source-commit",
        args.source_commit,
        "--pyfcstm-commit",
        args.pyfcstm_commit,
    )
    if args.replay_against is None:
        receipt = execute_request(
            request,
            repo_root=args.repo_root,
            receipt_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command,
        )
        output = {
            "receipt": str(args.receipt_root / "receipt.json"),
            "verdict": receipt.verdict,
            "acceptance_match": receipt.acceptance_match,
        }
    else:
        original = RelationOracleReceipt.model_validate_json(
            args.replay_against.read_text(encoding="utf-8")
        )
        audit = replay_request(
            request,
            original_receipt=original,
            original_receipt_path=args.replay_against,
            repo_root=args.repo_root,
            replay_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command + ("--replay-against", str(args.replay_against)),
        )
        output = {
            "replay_audit": str(args.receipt_root / "replay_audit.json"),
            "overall_match": audit.overall_match,
        }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
