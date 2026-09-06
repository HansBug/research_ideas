"""Evaluation-only native FCSTM contracts needed by ledger predicate gold.

The module consumes public ``pyfcstm`` objects through the provenance-preserving
native projection.  It is deliberately outside the frozen method package and
does not parse PlantUML or implement state-machine execution semantics.
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

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.native-contract-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.native-contract-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.native-contract-replay.v1"


class NativeContractId(str, Enum):
    """Closed contracts supported by this evaluation-only oracle."""

    UNREACHABLE_OR_OUTGOING_CARRIER = "UNREACHABLE_OR_OUTGOING_CARRIER"
    FORBIDDEN_EVENTLESS_CARRIER_ABSENT = "FORBIDDEN_EVENTLESS_CARRIER_ABSENT"
    REQUIRED_CARRIER_PRESENT = "REQUIRED_CARRIER_PRESENT"
    OUTPUT_ACTION_CARRIER_PRESENT = "OUTPUT_ACTION_CARRIER_PRESENT"


class ArtifactRole(str, Enum):
    """Role of the exact FCSTM artifact under evaluation."""

    DEFECTIVE = "DEFECTIVE"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"


class NativeContractRequest(StrictModel):
    """Hash-bound request frozen before any same-issue result is visible."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(
        default=REQUEST_SCHEMA_VERSION,
        description="Evaluation-only native-contract request schema version.",
    )
    request_id: str = Field(description="Stable request identity.", pattern=r"^[A-Za-z0-9_.:-]+$")
    ledger_id: str = Field(description="Immutable ledger issue identity.", min_length=1)
    property_id: str = Field(description="Pre-reviewed property identity.", min_length=1)
    property_proposal_sha256: str = Field(description="Pre-result proposal digest.", pattern=SHA256_PATTERN)
    exactness_relation: Literal[ExactnessRelation.EQUIVALENT, ExactnessRelation.O_IMPLIES_P] = Field(
        description="O/P relation fixed by semantic review before execution."
    )
    contract_id: NativeContractId = Field(description="Closed native-object contract.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="SHA-256 of exact artifact bytes.", pattern=SHA256_PATTERN)
    typed_inputs: tuple[TypedInput, ...] = Field(description="Complete source-provenanced contract inputs.", min_length=1)
    assumptions: tuple[str, ...] = Field(description="Explicit source and representation assumptions.")
    expected_boolean_for_acceptance: bool = Field(description="False for defect, true for control.")
    created_at: str = Field(description="UTC pre-result freeze time.", min_length=1)
    request_sha256: str = Field(description="Canonical request digest excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_request(self) -> NativeContractRequest:
        """Close input vocabulary, role polarity, and request digest."""

        names = [item.field_name for item in self.typed_inputs]
        expected = {
            NativeContractId.UNREACHABLE_OR_OUTGOING_CARRIER: {"state_path", "initial_scope"},
            NativeContractId.FORBIDDEN_EVENTLESS_CARRIER_ABSENT: {"owner", "source", "target"},
            NativeContractId.REQUIRED_CARRIER_PRESENT: {"owner", "source", "target"},
            NativeContractId.OUTPUT_ACTION_CARRIER_PRESENT: {"owner_state", "required_output_token"},
        }[self.contract_id]
        if set(names) != expected or len(names) != len(expected):
            raise ValueError(f"{self.contract_id.value} requires exactly {sorted(expected)}")
        values = _values(self)
        if not all(isinstance(values[name], str) and values[name] for name in expected):
            raise TypeError("native-contract inputs must be nonempty strings")
        if self.artifact_role == ArtifactRole.DEFECTIVE and self.expected_boolean_for_acceptance is not False:
            raise ValueError("defective requests must pre-register false")
        if self.artifact_role == ArtifactRole.POSITIVE_CONTROL and self.expected_boolean_for_acceptance is not True:
            raise ValueError("positive-control requests must pre-register true")
        if self.request_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"request_sha256"})):
            raise ValueError("request_sha256 does not match request payload")
        return self


class NativeContractConstituent(StrictModel):
    """One independently evaluated Boolean constituent."""

    constituent_id: str = Field(description="Stable constituent identity.", min_length=1)
    verdict: bool = Field(description="Completed Boolean value.")
    expected: JsonValue = Field(description="Pre-registered expected fact.")
    observed: JsonValue = Field(description="Native observation used for the Boolean.")
    reason: str = Field(description="How the observation determines the value.", min_length=1)


class NativeContractReceipt(StrictModel):
    """Hash-sealed completed Boolean native-contract receipt."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(default=RECEIPT_SCHEMA_VERSION, description="Receipt schema version.")
    request_id: str = Field(description="Request identity.", min_length=1)
    request_sha256: str = Field(description="Pre-result request digest.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue identity.", min_length=1)
    property_id: str = Field(description="Property identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(description="Pre-reviewed O/P relation.")
    contract_id: NativeContractId = Field(description="Executed native contract.")
    artifact_role: ArtifactRole = Field(description="Artifact role.")
    artifact_path: str = Field(description="Repository-relative artifact path.", min_length=1)
    artifact_sha256: str = Field(description="Exact artifact digest.", pattern=SHA256_PATTERN)
    state: Literal["COMPLETED_BOOLEAN"] = Field(description="Only completed Booleans are admitted.")
    verdict: bool = Field(description="Conjunction of all constituent values.")
    acceptance_match: bool = Field(description="Whether verdict matches pre-registration.")
    observations: tuple[dict[str, JsonValue], ...] = Field(description="Complete relevant native observations.")
    constituents: tuple[NativeContractConstituent, ...] = Field(description="All non-short-circuited constituents.", min_length=1)
    query_path: str = Field(description="Receipt-root-relative query path.", min_length=1)
    query_sha256: str = Field(description="Exact query JSON digest.", pattern=SHA256_PATTERN)
    code_hashes: dict[str, str] = Field(description="Oracle, projection, and pyfcstm code hashes.", min_length=3)
    source_commit: str = Field(description="Main repository commit.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Portable provider-free argv.", min_length=1)
    started_at: str = Field(description="UTC start time.", min_length=1)
    completed_at: str = Field(description="UTC completion time.", min_length=1)
    replay_status: Literal["NOT_REPLAYED"] = Field(description="Replay is sealed separately.")
    reason: str = Field(description="Verdict interpretation preserving relation direction.", min_length=1)
    basis: str = Field(description="Native-object and hash basis.", min_length=1)
    receipt_sha256: str = Field(description="Canonical receipt digest.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_receipt(self) -> NativeContractReceipt:
        """Require complete conjunction and a valid digest."""

        if self.verdict != all(item.verdict for item in self.constituents):
            raise ValueError("verdict must equal all constituent Booleans")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match receipt payload")
        return self


class NativeContractReplay(StrictModel):
    """Deterministic semantic replay comparison."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(default=REPLAY_SCHEMA_VERSION, description="Replay schema version.")
    request_sha256: str = Field(description="Replayed request digest.", pattern=SHA256_PATTERN)
    original_receipt_path: str = Field(description="Repository-relative original receipt.", min_length=1)
    original_receipt_sha256: str = Field(description="Original receipt bytes digest.", pattern=SHA256_PATTERN)
    replay_receipt_path: str = Field(description="Replay-root-relative receipt.", min_length=1)
    replay_receipt_sha256: str = Field(description="Replay receipt bytes digest.", pattern=SHA256_PATTERN)
    original_projection_sha256: str = Field(description="Original deterministic projection digest.", pattern=SHA256_PATTERN)
    replay_projection_sha256: str = Field(description="Replay deterministic projection digest.", pattern=SHA256_PATTERN)
    overall_match: bool = Field(description="Whether deterministic projections match.")
    replayed_at: str = Field(description="UTC replay time.", min_length=1)
    receipt_sha256: str = Field(description="Canonical replay-audit digest.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_replay(self) -> NativeContractReplay:
        """Bind match status and digest to compared projections."""

        if self.overall_match != (self.original_projection_sha256 == self.replay_projection_sha256):
            raise ValueError("overall_match does not reflect projection hashes")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match replay payload")
        return self


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _values(request: NativeContractRequest) -> dict[str, JsonValue]:
    return {item.field_name: item.normalized_value for item in request.typed_inputs}


def _carrier_row(carrier: object) -> dict[str, JsonValue]:
    return {
        "owner": carrier.owner_path,
        "source": carrier.source,
        "target": carrier.target,
        "events": [event.path_name for event in carrier.events],
        "has_guard": carrier.guard is not None,
        "effects": [repr(effect) for effect in carrier.effects],
        "source_line": carrier.source_line,
    }


def _canonical_endpoint(owner: str, endpoint: str) -> str:
    return endpoint if endpoint == "[*]" else f"{owner}.{endpoint}"


def _reachable_paths(document: object, carriers: tuple[object, ...], initial_scope: str) -> set[str]:
    """Compute guard/event-agnostic native carrier reachability for a static proxy."""

    from utils.stm_artifacts.fcstm_native_projection import resolve_state

    if resolve_state(document, initial_scope) is None:
        return set()
    seen = {initial_scope}
    changed = True
    while changed:
        changed = False
        for carrier in carriers:
            source = carrier.owner_path if carrier.source == "[*]" else _canonical_endpoint(carrier.owner_path, carrier.source)
            target = _canonical_endpoint(carrier.owner_path, carrier.target)
            if (source in seen or (carrier.source == "[*]" and carrier.owner_path in seen)) and target not in seen:
                seen.add(target)
                changed = True
    return seen


def _normal_token(value: str) -> str:
    return " ".join(value.replace("_", " ").split()).casefold()


def evaluate_request(request: NativeContractRequest, *, repo_root: Path) -> tuple[tuple[dict[str, JsonValue], ...], tuple[NativeContractConstituent, ...]]:
    """Evaluate one closed contract using only public pyfcstm native objects."""

    from utils.stm_artifacts.fcstm_native_projection import (
        all_states,
        all_transition_carriers,
        load_native_document,
        resolve_state,
        state_path,
    )

    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match request")
    document = load_native_document(artifact.read_text(encoding="utf-8"))
    carriers = all_transition_carriers(document)
    observations: list[dict[str, JsonValue]] = [
        {"kind": "state", "path": state_path(state), "parent": state_path(state.parent) if state.parent else None}
        for state in all_states(document)
    ]
    observations.extend({"kind": "carrier", **_carrier_row(carrier)} for carrier in carriers)
    values = _values(request)
    results: list[NativeContractConstituent] = []

    if request.contract_id == NativeContractId.UNREACHABLE_OR_OUTGOING_CARRIER:
        state = resolve_state(document, values["state_path"])
        reachable = _reachable_paths(document, carriers, str(values["initial_scope"]))
        state_is_reachable = state is not None and str(values["state_path"]) in reachable
        outgoing = [] if state is None else [
            _carrier_row(carrier)
            for carrier in carriers
            if carrier.owner_path == state_path(state.parent) and carrier.source == state.name
        ]
        results.extend((
            NativeContractConstituent(
                constituent_id="state_binding_or_absence",
                verdict=state is not None or not state_is_reachable,
                expected={"state": values["state_path"], "absence_is_repair": True},
                observed=state_path(state) if state is not None else None,
                reason="The exact source state was resolved; an absent state is admitted only as the pre-reviewed deletion repair.",
            ),
            NativeContractConstituent(
                constituent_id="unreachable_or_outgoing_carrier",
                verdict=(not state_is_reachable) or bool(outgoing),
                expected={"unreachable_or_has_outgoing": values["state_path"]},
                observed={"reachable": state_is_reachable, "outgoing": outgoing},
                reason="A reachable ordinary state must expose at least one authored outgoing carrier; this remains a source-static necessary condition, not runtime progress proof.",
            ),
        ))
    elif request.contract_id in {
        NativeContractId.FORBIDDEN_EVENTLESS_CARRIER_ABSENT,
        NativeContractId.REQUIRED_CARRIER_PRESENT,
    }:
        matches = [
            _carrier_row(carrier)
            for carrier in carriers
            if carrier.owner_path == values["owner"]
            and carrier.source == str(values["source"]).rsplit(".", 1)[-1]
            and carrier.target == str(values["target"]).rsplit(".", 1)[-1]
            and (
                request.contract_id == NativeContractId.REQUIRED_CARRIER_PRESENT
                or not carrier.events
            )
        ]
        if request.contract_id == NativeContractId.FORBIDDEN_EVENTLESS_CARRIER_ABSENT:
            results.append(NativeContractConstituent(
                constituent_id="forbidden_eventless_carrier_absent",
                verdict=not matches,
                expected={"owner": values["owner"], "source": values["source"], "target": values["target"], "events": []},
                observed=matches,
                reason="Enumerated all native authored carriers and required zero owner/source/target matches with an empty event set.",
            ))
        else:
            results.append(NativeContractConstituent(
                constituent_id="required_carrier_present",
                verdict=len(matches) == 1,
                expected={"exactly_one": {"owner": values["owner"], "source": values["source"], "target": values["target"]}},
                observed=matches,
                reason="Enumerated all native authored carriers and required exactly one direct owner/source/target match; event and guard are outside this issue's direct-edge obligation.",
            ))
    else:
        owner = resolve_state(document, values["owner_state"])
        token = str(values["required_output_token"])
        found: list[dict[str, JsonValue]] = []
        if owner is not None:
            for phase, actions in (("entry", owner.on_enters), ("do", owner.on_durings), ("exit", owner.on_exits)):
                for action in actions:
                    name = getattr(action, "name", None)
                    if isinstance(name, str) and _normal_token(name) == _normal_token(token):
                        found.append({"carrier": phase, "token": name})
            for carrier in carriers:
                if carrier.owner_path == state_path(owner.parent) and carrier.source == owner.name:
                    for effect in carrier.effects:
                        names = [getattr(effect, "name", None), getattr(effect, "var_name", None)]
                        for name in names:
                            if isinstance(name, str) and _normal_token(name) == _normal_token(token):
                                found.append({"carrier": "outgoing_transition_effect", "token": name, "source_line": carrier.source_line})
        results.extend((
            NativeContractConstituent(
                constituent_id="owner_identity",
                verdict=owner is not None,
                expected=values["owner_state"],
                observed=state_path(owner) if owner is not None else None,
                reason="Resolved the exact output owner through pyfcstm.",
            ),
            NativeContractConstituent(
                constituent_id="output_action_carrier_present",
                verdict=bool(found),
                expected={"normalized_output_token": token, "roles": ["entry", "do", "exit", "outgoing_transition_effect"]},
                observed=found,
                reason="Compared only lifecycle actions and native effect-operation identities; event declarations and descriptive state text cannot satisfy the output role.",
            ),
        ))
    return tuple(observations), tuple(results)


def execute_request(request: NativeContractRequest, *, repo_root: Path, receipt_root: Path, source_commit: str, pyfcstm_commit: str, command: tuple[str, ...]) -> NativeContractReceipt:
    """Execute, hash, and persist one completed native-contract query."""

    from pyfcstm.model import model as pyfcstm_model
    from utils.stm_artifacts import fcstm_native_projection

    started_at = _utc_now()
    observations, constituents = evaluate_request(request, repo_root=repo_root)
    verdict = all(item.verdict for item in constituents)
    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    write_json(query_path, request.model_dump(mode="json"))
    module_path = Path(__file__).resolve()
    projection_path = Path(inspect.getsourcefile(fcstm_native_projection) or "").resolve()
    model_path = Path(inspect.getsourcefile(pyfcstm_model) or "").resolve()
    unsigned = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "request_id": request.request_id,
        "request_sha256": request.request_sha256,
        "ledger_id": request.ledger_id,
        "property_id": request.property_id,
        "exactness_relation": request.exactness_relation,
        "contract_id": request.contract_id,
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
            module_path.relative_to(repo_root).as_posix(): sha256_path(module_path),
            projection_path.relative_to(repo_root).as_posix(): sha256_path(projection_path),
            model_path.relative_to(repo_root).as_posix(): sha256_path(model_path),
        },
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "replay_status": "NOT_REPLAYED",
        "reason": "The native-object contract completed with a Boolean; execution does not strengthen the pre-reviewed O/P relation.",
        "basis": "Public pyfcstm State/OnStage/Transition objects and provenance-preserving native carriers; no PlantUML regex, fuzzy state binding, or custom runtime.",
    }
    receipt = NativeContractReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def _projection(receipt: NativeContractReceipt) -> str:
    return canonical_sha256({
        "request_sha256": receipt.request_sha256,
        "contract_id": receipt.contract_id.value,
        "state": receipt.state,
        "verdict": receipt.verdict,
        "acceptance_match": receipt.acceptance_match,
        "observations": receipt.observations,
        "constituents": [item.model_dump(mode="json") for item in receipt.constituents],
        "artifact_sha256": receipt.artifact_sha256,
        "code_hashes": receipt.code_hashes,
    })


def replay_request(request: NativeContractRequest, *, original_path: Path, repo_root: Path, replay_root: Path, source_commit: str, pyfcstm_commit: str, command: tuple[str, ...]) -> NativeContractReplay:
    """Re-execute one query and compare deterministic semantic projections."""

    original = NativeContractReceipt.model_validate_json(original_path.read_text(encoding="utf-8"))
    replay_receipt = execute_request(request, repo_root=repo_root, receipt_root=replay_root, source_commit=source_commit, pyfcstm_commit=pyfcstm_commit, command=command)
    original_projection = _projection(original)
    replay_projection = _projection(replay_receipt)
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": original_path.relative_to(repo_root).as_posix(),
        "original_receipt_sha256": sha256_path(original_path),
        "replay_receipt_path": (replay_root / "receipt.json").relative_to(replay_root.parent).as_posix(),
        "replay_receipt_sha256": sha256_path(replay_root / "receipt.json"),
        "original_projection_sha256": original_projection,
        "replay_projection_sha256": replay_projection,
        "overall_match": original_projection == replay_projection,
        "replayed_at": _utc_now(),
    }
    audit = NativeContractReplay(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def main() -> int:
    """Execute or replay one provider-free native-contract request."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-of", type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    request = NativeContractRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
    command = tuple([
        "python", "-m", "paper_stm_evaluation.predicate_gold_native_contract",
        "--repo-root", ".", "--request", args.request.resolve().relative_to(repo_root).as_posix(),
        "--receipt-root", args.receipt_root.resolve().relative_to(repo_root).as_posix(),
        "--source-commit", args.source_commit, "--pyfcstm-commit", args.pyfcstm_commit,
    ] + (["--replay-of", args.replay_of.resolve().relative_to(repo_root).as_posix()] if args.replay_of else []))
    if args.replay_of:
        replay_request(request, original_path=args.replay_of.resolve(), repo_root=repo_root, replay_root=args.receipt_root.resolve(), source_commit=args.source_commit, pyfcstm_commit=args.pyfcstm_commit, command=command)
    else:
        execute_request(request, repo_root=repo_root, receipt_root=args.receipt_root.resolve(), source_commit=args.source_commit, pyfcstm_commit=args.pyfcstm_commit, command=command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
