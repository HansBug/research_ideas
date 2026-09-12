"""Non-short-circuit execution and replay for AND/NOT predicate gold."""

from __future__ import annotations

import argparse
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import Field, JsonValue, model_validator

from . import predicate_gold_execution as predicate_execution_module
from .predicate_gold import (
    SHA256_PATTERN,
    ExactnessRelation,
    StrictModel,
    canonical_sha256,
    sha256_path,
    write_json,
)
from .predicate_gold_execution import (
    ArtifactRole,
    CodeArtifactHash,
    NormalizedExecutionState,
    PredicateExecutionRequest,
    PredicateGoldExecutionReceipt,
    RelationScope,
)
from .predicate_gold_execution import (
    execute_request as execute_predicate_request,
)

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.composite-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.composite-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.composite-replay.v1"


class CompositeExecutionRequest(StrictModel):
    """Pre-result AND or unary NOT property with hash-frozen constituents."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(
        default=REQUEST_SCHEMA_VERSION,
        description="Evaluation-only composite request schema version.",
    )
    request_id: str = Field(description="Stable parent request identity.", pattern=r"^[A-Za-z0-9_.:-]+$")
    ledger_id: str = Field(description="Immutable ledger issue owning the composite.", min_length=1)
    property_id: str = Field(description="Selected composite property identity.", min_length=1)
    property_proposal_sha256: str = Field(
        description="Hash frozen before any constituent was executed.",
        pattern=SHA256_PATTERN,
    )
    exactness_relation: ExactnessRelation = Field(description="O/P relation of the complete composite, not of an individual constituent.")
    operator: Literal["AND", "NOT"] = Field(description="Explicit conjunction or unary-negation truth operator.")
    no_short_circuit: Literal[True] = Field(
        default=True,
        description="Requires every constituent query to execute even after a false or failed result.",
    )
    artifact_role: ArtifactRole = Field(description="Defective artifact or independently justified positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM artifact path shared by all constituents.", min_length=1)
    artifact_sha256: str = Field(description="Hash of the exact FCSTM artifact bytes.", pattern=SHA256_PATTERN)
    constituents: tuple[PredicateExecutionRequest, ...] = Field(
        description="Ordered constituent requests frozen with relation_scope=PARENT_COMPOSITE.",
        min_length=1,
    )
    assumptions: tuple[str, ...] = Field(description="Source-backed completeness, scope, and execution assumptions of the composite.")
    expected_boolean_for_acceptance: bool = Field(description="Pre-registered Boolean for the complete composite property.")
    created_at: str = Field(description="UTC request freeze time.", min_length=1)
    request_sha256: str = Field(description="Canonical request hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_request(self) -> CompositeExecutionRequest:
        """Close parent/child identity, role, artifact, relation, and digest boundaries."""

        request_ids = [item.request_id for item in self.constituents]
        if len(request_ids) != len(set(request_ids)):
            raise ValueError("composite constituent request IDs must be unique")
        if self.operator == "AND" and len(self.constituents) < 2:
            raise ValueError("AND requires at least two constituents")
        if self.operator == "NOT" and len(self.constituents) != 1:
            raise ValueError("NOT requires exactly one constituent")
        for constituent in self.constituents:
            if constituent.relation_scope != RelationScope.PARENT_COMPOSITE:
                raise ValueError("every composite constituent must declare relation_scope=PARENT_COMPOSITE")
            if constituent.ledger_id != self.ledger_id or constituent.property_id != self.property_id:
                raise ValueError("constituent ledger/property identity differs from its parent")
            if constituent.property_proposal_sha256 != self.property_proposal_sha256:
                raise ValueError("constituent proposal hash differs from its parent")
            if constituent.exactness_relation != self.exactness_relation:
                raise ValueError("constituent relation must explicitly refer to the parent composite relation")
            if constituent.artifact_role != self.artifact_role:
                raise ValueError("constituent artifact role differs from its parent")
            if constituent.artifact_path != self.artifact_path or constituent.artifact_sha256 != self.artifact_sha256:
                raise ValueError("constituent artifact identity differs from its parent")
        if self.artifact_role == ArtifactRole.DEFECTIVE and self.expected_boolean_for_acceptance is not False:
            raise ValueError("defective composite requests pre-register false")
        if self.artifact_role == ArtifactRole.POSITIVE_CONTROL and self.expected_boolean_for_acceptance is not True:
            raise ValueError("positive-control composite requests pre-register true")
        if self.request_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"request_sha256"})):
            raise ValueError("request_sha256 does not match the pre-result composite payload")
        return self


class CompositeConstituentResult(StrictModel):
    """One persisted constituent result in a non-short-circuited composite."""

    request_id: str = Field(description="Constituent request identity.", min_length=1)
    request_sha256: str = Field(description="Hash of the frozen constituent request.", pattern=SHA256_PATTERN)
    predicate_id: str = Field(description="Frozen predicate executed for this constituent.", min_length=1)
    expected_boolean_for_acceptance: bool = Field(description="Pre-registered constituent-level mechanics expectation.")
    state: NormalizedExecutionState = Field(description="Normalized constituent completion or failure state.")
    verdict: bool | None = Field(description="Completed Boolean, or null for a non-result.")
    acceptance_match: bool = Field(description="Whether the constituent result matched its pre-registration.")
    receipt_path: str | None = Field(description="Parent-receipt-root-relative normalized child receipt path, or null after a runner exception.")
    receipt_sha256: str | None = Field(description="Hash of the normalized child receipt, or null after a runner exception.", pattern=SHA256_PATTERN)
    raw_semantic_projection_sha256: str | None = Field(
        description="Hash of terminal state, verdict, counterexample, trace, backend, and algorithm metadata used for replay comparison.",
        pattern=SHA256_PATTERN,
    )
    error_type: str | None = Field(description="Exception type when no child receipt could be sealed; otherwise null.")
    error_message: str | None = Field(description="Exception message when no child receipt could be sealed; otherwise null.")

    @model_validator(mode="after")
    def validate_result(self) -> CompositeConstituentResult:
        """Keep completed receipts and runner failures disjoint."""

        if self.receipt_path is not None:
            if self.receipt_sha256 is None or self.raw_semantic_projection_sha256 is None:
                raise ValueError("a persisted constituent receipt requires both receipt and semantic projection hashes")
            if self.error_type is not None or self.error_message is not None:
                raise ValueError("a persisted constituent receipt cannot also be a runner exception")
        elif self.error_type is None or self.error_message is None:
            raise ValueError("a missing constituent receipt requires an exception type and message")
        if self.state == NormalizedExecutionState.COMPLETED_BOOLEAN:
            if self.verdict is None:
                raise ValueError("a completed constituent requires a Boolean verdict")
        elif self.verdict is not None or self.acceptance_match:
            raise ValueError("a non-Boolean constituent cannot carry a verdict or acceptance match")
        return self


class CompositeExecutionReceipt(StrictModel):
    """Hash-sealed Boolean or failure receipt for one complete composite property."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(default=RECEIPT_SCHEMA_VERSION, description="Composite receipt schema version.")
    request_id: str = Field(description="Parent request identity.", min_length=1)
    request_sha256: str = Field(description="Hash of the pre-result parent request.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue owning the composite.", min_length=1)
    property_id: str = Field(description="Selected composite property identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(description="O/P relation of the complete composite.")
    operator: Literal["AND", "NOT"] = Field(description="Composite truth operator.")
    no_short_circuit: Literal[True] = Field(description="Confirms every constituent has a result entry.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact artifact bytes.", pattern=SHA256_PATTERN)
    state: NormalizedExecutionState = Field(description="Completed Boolean only when every constituent completed with a Boolean.")
    verdict: bool | None = Field(description="Declared truth-function result, or null when any constituent has no Boolean.")
    acceptance_match: bool = Field(description="Whether the complete composite matched its pre-registered Boolean.")
    constituents: tuple[CompositeConstituentResult, ...] = Field(description="All ordered constituent results.", min_length=1)
    query_path: str = Field(description="Receipt-root-relative parent query JSON path.", min_length=1)
    query_sha256: str = Field(description="Hash of parent query JSON bytes.", pattern=SHA256_PATTERN)
    code_hashes: tuple[CodeArtifactHash, ...] = Field(description="Composite and predicate execution code hashes.", min_length=2)
    source_commit: str = Field(description="Main repository commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Exact provider-free parent replay argv.", min_length=1)
    started_at: str = Field(description="UTC execution start time.", min_length=1)
    completed_at: str = Field(description="UTC execution completion time.", min_length=1)
    replay_status: Literal["NOT_REPLAYED"] = Field(description="Replay is sealed separately because replay bytes have independent timestamps.")
    reason: str = Field(description="Overall Boolean or failure interpretation.", min_length=1)
    basis: str = Field(description="Constituent, backend, native object, and request-hash basis.", min_length=1)
    receipt_sha256: str = Field(description="Canonical receipt hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_receipt(self) -> CompositeExecutionReceipt:
        """Require complete non-short-circuit closure and the declared truth result."""

        if self.state == NormalizedExecutionState.COMPLETED_BOOLEAN:
            if any(item.state != NormalizedExecutionState.COMPLETED_BOOLEAN or item.verdict is None for item in self.constituents):
                raise ValueError("a completed composite requires every constituent Boolean")
            if self.verdict != _truth(self.operator, tuple(bool(item.verdict) for item in self.constituents)):
                raise ValueError("composite verdict does not match the declared truth operator")
        elif self.verdict is not None or self.acceptance_match:
            raise ValueError("a non-Boolean composite cannot carry a verdict or acceptance match")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match composite receipt payload")
        return self


class ReplayConstituentComparison(StrictModel):
    """Semantic replay comparison for one constituent."""

    request_id: str = Field(description="Constituent request identity.", min_length=1)
    original_projection_sha256: str | None = Field(description="Original semantic projection hash, or null after a runner exception.", pattern=SHA256_PATTERN)
    replay_projection_sha256: str | None = Field(description="Replay semantic projection hash, or null after a runner exception.", pattern=SHA256_PATTERN)
    match: bool = Field(description="Whether state, verdict, counterexample, trace, backend, and algorithm matched.")
    reason: str = Field(description="Comparison-specific explanation.", min_length=1)


class CompositeReplayReceipt(StrictModel):
    """Independent semantic replay comparison for a composite receipt."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(default=REPLAY_SCHEMA_VERSION, description="Composite replay-audit schema version.")
    request_sha256: str = Field(description="Hash of the replayed parent request.", pattern=SHA256_PATTERN)
    original_receipt_path: str = Field(description="Repository- or invocation-relative original receipt path.", min_length=1)
    original_receipt_sha256: str = Field(description="Hash of the original composite receipt bytes.", pattern=SHA256_PATTERN)
    replay_receipt_path: str = Field(description="Replay-root-relative replay receipt path.", min_length=1)
    replay_receipt_sha256: str = Field(description="Hash of the replay composite receipt bytes.", pattern=SHA256_PATTERN)
    original_state: NormalizedExecutionState = Field(description="Original normalized composite state.")
    replay_state: NormalizedExecutionState = Field(description="Replay normalized composite state.")
    original_verdict: bool | None = Field(description="Original composite Boolean or null.")
    replay_verdict: bool | None = Field(description="Replay composite Boolean or null.")
    constituents: tuple[ReplayConstituentComparison, ...] = Field(description="Ordered constituent semantic comparisons.", min_length=1)
    overall_match: bool = Field(description="Whether parent state/verdict and every constituent semantic projection matched.")
    replayed_at: str = Field(description="UTC replay-audit completion time.", min_length=1)
    receipt_sha256: str = Field(description="Canonical replay-audit hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_replay(self) -> CompositeReplayReceipt:
        """Require overall_match to reflect every persisted comparison."""

        expected = (
            self.original_state == self.replay_state
            and self.original_verdict == self.replay_verdict
            and all(item.match for item in self.constituents)
        )
        if self.overall_match != expected:
            raise ValueError("overall_match does not reflect the replay comparisons")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match replay-audit payload")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _truth(operator: Literal["AND", "NOT"], values: tuple[bool, ...]) -> bool:
    """Evaluate the declared transparent truth operator."""

    if operator == "AND":
        if len(values) < 2:
            raise ValueError("AND requires at least two Boolean values")
        return all(values)
    if len(values) != 1:
        raise ValueError("NOT requires exactly one Boolean value")
    return not values[0]


def _receipt_interpretation(
    *, operator: Literal["AND", "NOT"], completed: bool
) -> tuple[str, str]:
    """Describe the persisted operator without misreporting unary NOT as conjunction."""

    if not completed:
        return (
            "At least one constituent lacked a Boolean; every remaining constituent was still executed and no composite verdict was admitted.",
            "Hash-frozen parent and child requests, one frozen backend result per attempted constituent, and explicit non-short-circuit failure closure.",
        )
    if operator == "AND":
        return (
            "Every constituent completed with a Boolean and the persisted verdict is their conjunction.",
            "Hash-frozen parent and child requests, one frozen backend receipt per constituent, and an explicit non-short-circuit AND truth function.",
        )
    return (
        "The unary constituent completed with a Boolean and the persisted verdict is its logical negation.",
        "A hash-frozen parent request, one hash-frozen child request and backend receipt, and an explicit unary NOT truth function.",
    )


def _code_hash(*, repo_root: Path, role: str, path: Path) -> CodeArtifactHash:
    """Hash one evaluation-only execution module."""

    resolved = path.resolve()
    return CodeArtifactHash(
        role=role,
        repository_path=resolved.relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(resolved),
    )


def _raw_semantic_projection(raw_path: Path) -> dict[str, JsonValue]:
    """Extract deterministic backend semantics while excluding timestamps and paths."""

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    metadata = raw.get("run_metadata") if isinstance(raw.get("run_metadata"), dict) else {}
    return {
        "terminal_state": raw.get("terminal_state"),
        "verdict": raw.get("verdict"),
        "counterexample": raw.get("counterexample"),
        "trace": raw.get("trace"),
        "backend": raw.get("backend"),
        "failure_kind": raw.get("failure_kind"),
        "algorithm_version": metadata.get("algorithm_version"),
    }


def _constituent_result(
    *,
    request: PredicateExecutionRequest,
    receipt: PredicateGoldExecutionReceipt,
    child_root: Path,
    receipt_root: Path,
) -> CompositeConstituentResult:
    """Project one persisted child receipt into the parent composite."""

    raw_path = child_root / receipt.raw_receipt_path
    projection_sha256 = canonical_sha256(_raw_semantic_projection(raw_path))
    receipt_path = child_root / "receipt.json"
    return CompositeConstituentResult(
        request_id=request.request_id,
        request_sha256=request.request_sha256,
        predicate_id=request.predicate_id,
        expected_boolean_for_acceptance=request.expected_boolean_for_acceptance,
        state=receipt.state,
        verdict=receipt.verdict,
        acceptance_match=receipt.acceptance_match,
        receipt_path=receipt_path.relative_to(receipt_root).as_posix(),
        receipt_sha256=sha256_path(receipt_path),
        raw_semantic_projection_sha256=projection_sha256,
        error_type=None,
        error_message=None,
    )


def execute_composite_request(
    *,
    request: CompositeExecutionRequest,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> CompositeExecutionReceipt:
    """Execute all child requests, including those after a false or exception."""

    started_at = _utc_now()
    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match the pre-hashed composite request")
    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    write_json(query_path, request.model_dump(mode="json"))
    results: list[CompositeConstituentResult] = []
    for constituent in request.constituents:
        child_root = receipt_root / "constituents" / constituent.request_id
        child_command = (
            "python",
            "-m",
            "paper_stm_evaluation.predicate_gold_execution",
            "--request",
            str(child_root / "query.json"),
            "--repo-root",
            str(repo_root),
            "--receipt-root",
            str(child_root),
            "--source-commit",
            source_commit,
            "--pyfcstm-commit",
            pyfcstm_commit,
        )
        try:
            child_receipt = execute_predicate_request(
                request=constituent,
                repo_root=repo_root,
                receipt_root=child_root,
                source_commit=source_commit,
                pyfcstm_commit=pyfcstm_commit,
                command=child_command,
            )
            results.append(
                _constituent_result(
                    request=constituent,
                    receipt=child_receipt,
                    child_root=child_root,
                    receipt_root=receipt_root,
                )
            )
        except Exception as exc:  # noqa: BLE001 - persisted while remaining constituents still run.
            child_root.mkdir(parents=True, exist_ok=True)
            error = {
                "request_id": constituent.request_id,
                "request_sha256": constituent.request_sha256,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
            write_json(child_root / "runner_error.json", error)
            results.append(
                CompositeConstituentResult(
                    request_id=constituent.request_id,
                    request_sha256=constituent.request_sha256,
                    predicate_id=constituent.predicate_id,
                    expected_boolean_for_acceptance=constituent.expected_boolean_for_acceptance,
                    state=NormalizedExecutionState.ERROR,
                    verdict=None,
                    acceptance_match=False,
                    receipt_path=None,
                    receipt_sha256=None,
                    raw_semantic_projection_sha256=None,
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                )
            )

    completed = all(item.state == NormalizedExecutionState.COMPLETED_BOOLEAN for item in results)
    state = NormalizedExecutionState.COMPLETED_BOOLEAN if completed else NormalizedExecutionState.ERROR
    verdict = _truth(request.operator, tuple(bool(item.verdict) for item in results)) if completed else None
    composite_module_path = Path(__file__).resolve()
    predicate_module_path = Path(inspect.getsourcefile(predicate_execution_module) or "").resolve()
    reason, basis = _receipt_interpretation(
        operator=request.operator, completed=completed
    )
    unsigned = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "request_id": request.request_id,
        "request_sha256": request.request_sha256,
        "ledger_id": request.ledger_id,
        "property_id": request.property_id,
        "exactness_relation": request.exactness_relation,
        "operator": request.operator,
        "no_short_circuit": request.no_short_circuit,
        "artifact_role": request.artifact_role,
        "artifact_path": request.artifact_path,
        "artifact_sha256": request.artifact_sha256,
        "state": state,
        "verdict": verdict,
        "acceptance_match": verdict == request.expected_boolean_for_acceptance if verdict is not None else False,
        "constituents": [item.model_dump(mode="json") for item in results],
        "query_path": query_path.relative_to(receipt_root).as_posix(),
        "query_sha256": sha256_path(query_path),
        "code_hashes": [
            _code_hash(repo_root=repo_root, role="composite_runner", path=composite_module_path).model_dump(mode="json"),
            _code_hash(repo_root=repo_root, role="predicate_runner", path=predicate_module_path).model_dump(mode="json"),
        ],
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "replay_status": "NOT_REPLAYED",
        "reason": reason,
        "basis": basis,
    }
    receipt = CompositeExecutionReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def replay_composite_request(
    *,
    request: CompositeExecutionRequest,
    original_receipt: CompositeExecutionReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> CompositeReplayReceipt:
    """Re-execute a composite and compare deterministic semantic projections."""

    replay_receipt = execute_composite_request(
        request=request,
        repo_root=repo_root,
        receipt_root=replay_root,
        source_commit=source_commit,
        pyfcstm_commit=pyfcstm_commit,
        command=command,
    )
    replay_by_id = {item.request_id: item for item in replay_receipt.constituents}
    comparisons: list[ReplayConstituentComparison] = []
    for original in original_receipt.constituents:
        replayed = replay_by_id.get(original.request_id)
        match = bool(
            replayed is not None
            and original.state == replayed.state
            and original.verdict == replayed.verdict
            and original.raw_semantic_projection_sha256 == replayed.raw_semantic_projection_sha256
        )
        comparisons.append(
            ReplayConstituentComparison(
                request_id=original.request_id,
                original_projection_sha256=original.raw_semantic_projection_sha256,
                replay_projection_sha256=replayed.raw_semantic_projection_sha256 if replayed else None,
                match=match,
                reason="State, Boolean, and raw semantic projection matched." if match else "State, Boolean, or raw semantic projection differed or was missing.",
            )
        )
    overall_match = (
        original_receipt.state == replay_receipt.state
        and original_receipt.verdict == replay_receipt.verdict
        and all(item.match for item in comparisons)
    )
    replay_receipt_path = replay_root / "receipt.json"
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": str(original_receipt_path),
        "original_receipt_sha256": sha256_path(original_receipt_path),
        "replay_receipt_path": replay_receipt_path.relative_to(replay_root).as_posix(),
        "replay_receipt_sha256": sha256_path(replay_receipt_path),
        "original_state": original_receipt.state,
        "replay_state": replay_receipt.state,
        "original_verdict": original_receipt.verdict,
        "replay_verdict": replay_receipt.verdict,
        "constituents": [item.model_dump(mode="json") for item in comparisons],
        "overall_match": overall_match,
        "replayed_at": _utc_now(),
    }
    audit = CompositeReplayReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the provider-free composite execution CLI."""

    parser = argparse.ArgumentParser(description="Execute or replay one pre-hashed composite predicate-gold query.")
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-against", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate and execute an original or semantic replay composite request."""

    args = _parser().parse_args(argv)
    request = CompositeExecutionRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_composite",
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
        receipt = execute_composite_request(
            request=request,
            repo_root=args.repo_root,
            receipt_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command,
        )
        output = {"receipt": str(args.receipt_root / "receipt.json"), "state": receipt.state.value, "verdict": receipt.verdict, "acceptance_match": receipt.acceptance_match}
    else:
        original = CompositeExecutionReceipt.model_validate_json(args.replay_against.read_text(encoding="utf-8"))
        audit = replay_composite_request(
            request=request,
            original_receipt=original,
            original_receipt_path=args.replay_against,
            repo_root=args.repo_root,
            replay_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command + ("--replay-against", str(args.replay_against)),
        )
        output = {"replay_audit": str(args.receipt_root / "replay_audit.json"), "overall_match": audit.overall_match}
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
