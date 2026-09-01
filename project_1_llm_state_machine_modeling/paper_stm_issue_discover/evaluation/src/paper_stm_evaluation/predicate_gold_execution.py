"""Evaluation-only execution and receipt sealing for pre-hashed gold queries."""

from __future__ import annotations

import argparse
import hashlib
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

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.execution-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.execution-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.execution-replay.v1"
PREDICATE_IDS = (
    *(f"S{i}" for i in range(1, 7)),
    *(f"G{i}" for i in range(1, 5)),
    *(f"R{i}" for i in range(1, 5)),
    *(f"V{i}" for i in range(1, 6)),
)


class ArtifactRole(str, Enum):
    """Role of the artifact evaluated by one sealed query."""

    DEFECTIVE = "DEFECTIVE"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"


class RelationScope(str, Enum):
    """Whether O/P exactness applies to this query or its parent composite."""

    THIS_PROPERTY = "THIS_PROPERTY"
    PARENT_COMPOSITE = "PARENT_COMPOSITE"


class NormalizedExecutionState(str, Enum):
    """Normalized execution state without conflating failure and false."""

    COMPLETED_BOOLEAN = "COMPLETED_BOOLEAN"
    INVALID_REQUEST = "INVALID_REQUEST"
    UNSUPPORTED = "UNSUPPORTED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"


class PredicateExecutionRequest(StrictModel):
    """Pre-result property query bound to one artifact and proposal digest."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(default=REQUEST_SCHEMA_VERSION, description="Evaluation-only execution request schema version.")
    request_id: str = Field(description="Stable query identity used for receipt paths.", pattern=r"^[A-Za-z0-9_.:-]+$")
    ledger_id: str = Field(description="Immutable ledger issue whose proposal owns this query.", min_length=1)
    property_id: str = Field(description="Stable selected property identity from the pre-execution proposal.", min_length=1)
    property_proposal_sha256: str = Field(description="Hash frozen before any execution result was visible.", pattern=SHA256_PATTERN)
    exactness_relation: ExactnessRelation = Field(description="EQUIVALENT for exact candidates or O_IMPLIES_P for sound proxies.")
    relation_scope: RelationScope = Field(
        default=RelationScope.THIS_PROPERTY,
        description="Whether exactness_relation describes this standalone property or the parent composite containing this constituent.",
    )
    predicate_id: str = Field(description="Frozen predicate dispatched by this request.", pattern=r"^[SGRV][1-6]$")
    artifact_role: ArtifactRole = Field(description="Defective artifact or independently justified positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM artifact path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of the exact FCSTM artifact bytes.", pattern=SHA256_PATTERN)
    typed_inputs: tuple[TypedInput, ...] = Field(description="Complete property inputs frozen before execution.")
    assumptions: tuple[str, ...] = Field(description="All source-backed domain, bound, scope, and environment assumptions.")
    expected_boolean_for_acceptance: bool = Field(description="Pre-registered acceptance value: false for defective exact/proxy queries and true for positive controls.")
    created_at: str = Field(description="UTC request freeze time.", min_length=1)
    request_sha256: str = Field(description="Canonical digest of this request excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_request(self) -> PredicateExecutionRequest:
        """Reject duplicate input names, unknown predicates, and role/verdict inversion."""

        if self.predicate_id not in PREDICATE_IDS:
            raise ValueError("predicate_id is not one of the frozen 19")
        names = [item.field_name for item in self.typed_inputs]
        if len(names) != len(set(names)):
            raise ValueError("typed input field names must be unique")
        if self.relation_scope == RelationScope.THIS_PROPERTY:
            if self.artifact_role == ArtifactRole.DEFECTIVE and self.expected_boolean_for_acceptance is not False:
                raise ValueError("defective standalone gold/proxy requests pre-register false as the acceptance value")
            if self.artifact_role == ArtifactRole.POSITIVE_CONTROL and self.expected_boolean_for_acceptance is not True:
                raise ValueError("standalone positive-control requests pre-register true as the acceptance value")
        expected_hash = canonical_sha256(self.model_dump(mode="json", exclude={"request_sha256"}))
        if self.request_sha256 != expected_hash:
            raise ValueError("request_sha256 does not match the pre-result request payload")
        return self


class CodeArtifactHash(StrictModel):
    """One exact source file that contributed to a backend execution."""

    role: str = Field(description="Backend, native adapter, typed schema, projection, or pyfcstm role.", min_length=1)
    repository_path: str = Field(description="Repository-relative code path.", min_length=1)
    sha256: str = Field(description="Hash of the exact source bytes.", pattern=SHA256_PATTERN)


class PredicateGoldExecutionReceipt(StrictModel):
    """Normalized replayable receipt wrapping one frozen backend RawReceipt."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(default=RECEIPT_SCHEMA_VERSION, description="Evaluation-only normalized receipt schema version.")
    request_id: str = Field(description="Stable request identity.", min_length=1)
    request_sha256: str = Field(description="Digest of the pre-result request.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue owning this execution.", min_length=1)
    property_id: str = Field(description="Selected property identity.", min_length=1)
    predicate_id: str = Field(description="Frozen predicate dispatched.", min_length=1)
    exactness_relation: ExactnessRelation = Field(description="O/P direction frozen before execution.")
    relation_scope: RelationScope = Field(description="Whether exactness applies to this property or its parent composite.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or positive control.")
    artifact_path: str = Field(description="Repository-relative artifact path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact artifact bytes.", pattern=SHA256_PATTERN)
    state: NormalizedExecutionState = Field(description="Completed Boolean, invalid, unsupported, error, or timeout.")
    verdict: bool | None = Field(description="Boolean only for COMPLETED_BOOLEAN; null for every failure/non-result state.")
    acceptance_match: bool = Field(description="Whether a completed Boolean equals the request's pre-registered acceptance value.")
    backend: str = Field(description="Backend label retained from RawReceipt.", min_length=1)
    algorithm_version: str = Field(description="Backend algorithm version retained from RawReceipt metadata.", min_length=1)
    query_path: str = Field(description="Receipt-root-relative canonical query JSON path.", min_length=1)
    query_sha256: str = Field(description="Hash of canonical query JSON bytes.", pattern=SHA256_PATTERN)
    fbmcq_query_path: str | None = Field(description="Receipt-root-relative FBMCQ source path when generated; otherwise null.")
    fbmcq_query_sha256: str | None = Field(description="Hash of FBMCQ source bytes when generated; otherwise null.", pattern=SHA256_PATTERN)
    raw_receipt_path: str = Field(description="Receipt-root-relative frozen RawReceipt JSON path.", min_length=1)
    raw_receipt_sha256: str = Field(description="Hash of serialized RawReceipt bytes.", pattern=SHA256_PATTERN)
    counterexample_json_pointer: str = Field(description="Pointer to the complete raw counterexample array.", min_length=1)
    trace_json_pointer: str = Field(description="Pointer to the complete raw trace array.", min_length=1)
    replay_status: Literal["REPLAY_MATCH", "NOT_APPLICABLE", "REPLAY_FAILED", "NOT_REPLAYED"] = Field(description="Native FBMCQ replay disposition or explicit non-applicability.")
    code_hashes: tuple[CodeArtifactHash, ...] = Field(description="Exact backend, native adapter, typed schema, projection, and pyfcstm source hashes.", min_length=4)
    source_commit: str = Field(description="Main repository commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="pyfcstm submodule commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Exact argv for provider-free replay.", min_length=1)
    started_at: str = Field(description="UTC execution start time.", min_length=1)
    completed_at: str = Field(description="UTC receipt completion time.", min_length=1)
    reason: str = Field(description="Normalized interpretation that never maps failure to false.", min_length=1)
    basis: str = Field(description="Typed-input, native model, backend, artifact, and RawReceipt basis.", min_length=1)
    receipt_sha256: str = Field(description="Canonical digest of this normalized receipt excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_receipt(self) -> PredicateGoldExecutionReceipt:
        """Enforce Boolean/state closure and receipt digest integrity."""

        if self.state == NormalizedExecutionState.COMPLETED_BOOLEAN:
            if self.verdict is None:
                raise ValueError("completed Boolean state requires a verdict")
        elif self.verdict is not None or self.acceptance_match:
            raise ValueError("non-Boolean execution cannot persist a verdict or acceptance match")
        expected_hash = canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"}))
        if self.receipt_sha256 != expected_hash:
            raise ValueError("receipt_sha256 does not match normalized receipt payload")
        return self


class PredicateReplayAudit(StrictModel):
    """Semantic replay comparison for one frozen predicate request."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(default=REPLAY_SCHEMA_VERSION, description="Single-predicate replay-audit schema version.")
    request_sha256: str = Field(description="Hash of the replayed pre-result request.", pattern=SHA256_PATTERN)
    original_receipt_path: str = Field(description="Repository- or invocation-relative original normalized receipt path.", min_length=1)
    original_receipt_sha256: str = Field(description="Hash of the original normalized receipt bytes.", pattern=SHA256_PATTERN)
    replay_receipt_path: str = Field(description="Replay-root-relative normalized replay receipt path.", min_length=1)
    replay_receipt_sha256: str = Field(description="Hash of the replay normalized receipt bytes.", pattern=SHA256_PATTERN)
    original_projection_sha256: str = Field(description="Hash of original terminal semantics excluding paths and timestamps.", pattern=SHA256_PATTERN)
    replay_projection_sha256: str = Field(description="Hash of replay terminal semantics excluding paths and timestamps.", pattern=SHA256_PATTERN)
    original_state: NormalizedExecutionState = Field(description="Original normalized completion state.")
    replay_state: NormalizedExecutionState = Field(description="Replay normalized completion state.")
    original_verdict: bool | None = Field(description="Original Boolean, or null for a non-result.")
    replay_verdict: bool | None = Field(description="Replay Boolean, or null for a non-result.")
    overall_match: bool = Field(description="Whether state, Boolean and complete semantic projection match.")
    replayed_at: str = Field(description="UTC replay-audit completion time.", min_length=1)
    reason: str = Field(description="Exact fields compared and replay interpretation.", min_length=1)
    receipt_sha256: str = Field(description="Canonical replay-audit hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_replay(self) -> PredicateReplayAudit:
        """Require the match flag and payload digest to reflect compared evidence."""

        expected_match = (
            self.original_state == self.replay_state
            and self.original_verdict == self.replay_verdict
            and self.original_projection_sha256 == self.replay_projection_sha256
        )
        if self.overall_match != expected_match:
            raise ValueError("overall_match does not reflect replay comparison")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match replay-audit payload")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp without locale dependence."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repository_path(repo_root: Path, source_file: str | None) -> str:
    """Resolve an imported Python source file to a repository-relative path."""

    if source_file is None:
        raise RuntimeError("imported execution component has no source file")
    return Path(source_file).resolve().relative_to(repo_root.resolve()).as_posix()


def _file_hash(repo_root: Path, *, role: str, source_file: str | None) -> CodeArtifactHash:
    """Build one hash record for imported execution code."""

    relative = _repository_path(repo_root, source_file)
    return CodeArtifactHash(role=role, repository_path=relative, sha256=sha256_path(repo_root / relative))


def _normalized_state(raw_terminal: str, raw_verdict: str) -> tuple[NormalizedExecutionState, bool | None]:
    """Normalize RawReceipt state without treating unknown or failures as false."""

    if raw_terminal == "completed" and raw_verdict in {"true", "false"}:
        return NormalizedExecutionState.COMPLETED_BOOLEAN, raw_verdict == "true"
    if raw_terminal == "timeout":
        return NormalizedExecutionState.TIMEOUT, None
    if raw_terminal == "error":
        return NormalizedExecutionState.ERROR, None
    if raw_terminal == "unsupported":
        return NormalizedExecutionState.UNSUPPORTED, None
    return NormalizedExecutionState.INVALID_REQUEST, None


def execute_request(
    *,
    request: PredicateExecutionRequest,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> PredicateGoldExecutionReceipt:
    """Execute one pre-hashed query through the frozen backend and seal all bytes."""

    from paper_stm_method.backends import (
        bounded_verification,
        fcstm_native,
        run_bounded_verification,
        run_source_static,
        run_topology,
        run_trajectory,
        source_static,
        topology,
        trajectory,
    )
    from paper_stm_method.compiler import inputs as compiler_inputs
    from paper_stm_method.compiler.inputs import (
        UnsupportedPredicateInputs,
        validate_predicate_inputs,
    )
    from paper_stm_method.compiler.lowering import (
        PredicatePlan,
        assess_soundness_fragment,
    )
    from utils.stm_artifacts import models as artifact_models
    from utils.stm_artifacts.models import parse_fcstm

    started_at = _utc_now()
    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match the pre-hashed execution request")
    source_text = artifact.read_text(encoding="utf-8")
    model = parse_fcstm(source_text)
    model_hash = "sha256:" + hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    values: dict[str, JsonValue] = {item.field_name: item.normalized_value for item in request.typed_inputs}
    values["element_refs"] = [item.stable_object_id for item in request.typed_inputs if item.stable_object_id]
    values["model_hash"] = model_hash
    typed = validate_predicate_inputs(request.predicate_id, values)
    if isinstance(typed, UnsupportedPredicateInputs):
        raise TypeError("request typed inputs do not satisfy the frozen predicate input schema")
    fragment_ok, fragment_reason = assess_soundness_fragment(
        request.predicate_id,
        typed.to_backend_dict(),
        model_hash=model_hash,
        model=model,
    )
    if not fragment_ok:
        raise ValueError(f"request is outside the frozen predicate soundness fragment: {fragment_reason}")
    formal_program = json.dumps(
        {"predicate_id": request.predicate_id, "inputs": typed.to_backend_dict(), "artifact_sha256": request.artifact_sha256},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    plan = PredicatePlan(
        plan_id=request.request_id,
        predicate_id=request.predicate_id,
        registry_version="four-family-19-core.v1",
        inputs=typed,
        soundness_fragment="evaluation-only pre-hashed gold request within frozen backend fragment",
        assumptions=request.assumptions,
        formal_program=formal_program,
        formal_program_hash="sha256:" + hashlib.sha256(formal_program.encode("utf-8")).hexdigest(),
        predicate_registered=True,
        binding_precise=True,
        input_shape_valid=True,
        binding_complete=True,
        backend_available=True,
        soundness_fragment_satisfied=True,
        artifact_attribution_complete=True,
        execution_state="not_attempted",
        predicate_verdict=None,
        supported=True,
        executable=True,
        reason="The evaluation-only request was source-reviewed and hash-frozen before backend execution.",
        basis=fragment_reason,
        predicate_name=request.predicate_id,
        family={"S": "structure", "G": "topology", "R": "trajectory", "V": "bounded_verification"}[request.predicate_id[0]],
        semantics="Issue-specific semantics are owned by the frozen predicate-gold proposal, not inferred by this runner.",
        source_ids=(),
        missing_inputs=(),
    )
    dispatch = {
        "S": run_source_static,
        "G": run_topology,
        "R": run_trajectory,
        "V": run_bounded_verification,
    }[request.predicate_id[0]]
    raw = dispatch(plan, model, request.request_id)

    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    raw_path = receipt_root / "raw_receipt.json"
    write_json(query_path, request.model_dump(mode="json"))
    write_json(raw_path, raw.model_dump(mode="json"))
    fbmcq_query = raw.run_metadata.get("fbmcq_query")
    fbmcq_path: Path | None = None
    if isinstance(fbmcq_query, str):
        fbmcq_path = receipt_root / "query.fbmcq"
        fbmcq_path.write_text(fbmcq_query.rstrip() + "\n", encoding="utf-8")

    state, verdict = _normalized_state(raw.terminal_state, raw.verdict)
    replay = raw.run_metadata.get("fbmcq_execution", {}).get("replay")
    if state != NormalizedExecutionState.COMPLETED_BOOLEAN or fbmcq_path is None:
        replay_status = "NOT_APPLICABLE" if fbmcq_path is None else "NOT_REPLAYED"
    elif isinstance(replay, dict) and replay.get("ok") is True:
        replay_status = "REPLAY_MATCH"
    elif isinstance(replay, dict):
        replay_status = "REPLAY_FAILED"
    else:
        replay_status = "NOT_REPLAYED"
    backend_module = {"S": source_static, "G": topology, "R": trajectory, "V": bounded_verification}[request.predicate_id[0]]
    pyfcstm_model_source = inspect.getsourcefile(__import__("pyfcstm.model", fromlist=["*"]))
    code_hashes = (
        _file_hash(repo_root, role="predicate_backend", source_file=inspect.getsourcefile(backend_module)),
        _file_hash(repo_root, role="native_backend_adapter", source_file=inspect.getsourcefile(fcstm_native)),
        _file_hash(repo_root, role="typed_input_schema", source_file=inspect.getsourcefile(compiler_inputs)),
        _file_hash(repo_root, role="native_model_projection", source_file=inspect.getsourcefile(artifact_models)),
        _file_hash(repo_root, role="pyfcstm_model_api", source_file=pyfcstm_model_source),
    )
    unsigned = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "request_id": request.request_id,
        "request_sha256": request.request_sha256,
        "ledger_id": request.ledger_id,
        "property_id": request.property_id,
        "predicate_id": request.predicate_id,
        "exactness_relation": request.exactness_relation,
        "relation_scope": request.relation_scope,
        "artifact_role": request.artifact_role,
        "artifact_path": request.artifact_path,
        "artifact_sha256": request.artifact_sha256,
        "state": state,
        "verdict": verdict,
        "acceptance_match": verdict == request.expected_boolean_for_acceptance if verdict is not None else False,
        "backend": raw.backend,
        "algorithm_version": str(raw.run_metadata.get("algorithm_version", "unknown")),
        "query_path": query_path.relative_to(receipt_root).as_posix(),
        "query_sha256": sha256_path(query_path),
        "fbmcq_query_path": fbmcq_path.relative_to(receipt_root).as_posix() if fbmcq_path else None,
        "fbmcq_query_sha256": sha256_path(fbmcq_path) if fbmcq_path else None,
        "raw_receipt_path": raw_path.relative_to(receipt_root).as_posix(),
        "raw_receipt_sha256": sha256_path(raw_path),
        "counterexample_json_pointer": "/counterexample",
        "trace_json_pointer": "/trace",
        "replay_status": replay_status,
        "code_hashes": [item.model_dump(mode="json") for item in code_hashes],
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "reason": "The frozen backend completed with a Boolean result." if verdict is not None else "The frozen backend did not complete with a Boolean result; no false/true verdict is admitted.",
        "basis": f"pre-hashed request, native FCSTM projection, frozen backend RawReceipt; backend basis: {raw.basis}",
    }
    receipt = PredicateGoldExecutionReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def _raw_semantic_projection(raw_path: Path) -> dict[str, JsonValue]:
    """Project one RawReceipt to deterministic backend semantics."""

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


def replay_request(
    *,
    request: PredicateExecutionRequest,
    original_receipt: PredicateGoldExecutionReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> PredicateReplayAudit:
    """Re-execute one frozen query and compare complete terminal semantics."""

    if original_receipt.request_sha256 != request.request_sha256:
        raise ValueError("original receipt does not belong to the replayed request")
    replay_receipt = execute_request(
        request=request,
        repo_root=repo_root,
        receipt_root=replay_root,
        source_commit=source_commit,
        pyfcstm_commit=pyfcstm_commit,
        command=command,
    )
    original_raw = original_receipt_path.parent / original_receipt.raw_receipt_path
    replay_raw = replay_root / replay_receipt.raw_receipt_path
    original_projection = canonical_sha256(_raw_semantic_projection(original_raw))
    replay_projection = canonical_sha256(_raw_semantic_projection(replay_raw))
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": str(original_receipt_path),
        "original_receipt_sha256": sha256_path(original_receipt_path),
        "replay_receipt_path": "receipt.json",
        "replay_receipt_sha256": sha256_path(replay_root / "receipt.json"),
        "original_projection_sha256": original_projection,
        "replay_projection_sha256": replay_projection,
        "original_state": original_receipt.state,
        "replay_state": replay_receipt.state,
        "original_verdict": original_receipt.verdict,
        "replay_verdict": replay_receipt.verdict,
        "overall_match": (
            original_receipt.state == replay_receipt.state
            and original_receipt.verdict == replay_receipt.verdict
            and original_projection == replay_projection
        ),
        "replayed_at": _utc_now(),
        "reason": "Compared normalized state/Boolean and RawReceipt counterexample, trace, backend, failure kind, and algorithm version; timestamps and invocation paths are excluded.",
    }
    audit = PredicateReplayAudit(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the single-query provider-free execution parser."""

    parser = argparse.ArgumentParser(description="Execute one pre-hashed predicate-gold query without running the method pipeline.")
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-original", type=Path, help="Original normalized receipt to replay and compare.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate, execute, and seal one evaluation-only request."""

    args = _parser().parse_args(argv)
    request = PredicateExecutionRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_execution",
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
    if args.replay_original is not None:
        command = (*command, "--replay-original", str(args.replay_original))
        original = PredicateGoldExecutionReceipt.model_validate_json(args.replay_original.read_text(encoding="utf-8"))
        audit = replay_request(
            request=request,
            original_receipt=original,
            original_receipt_path=args.replay_original,
            repo_root=args.repo_root,
            replay_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command,
        )
        print(json.dumps({"replay_audit": str(args.receipt_root / "replay_audit.json"), "overall_match": audit.overall_match}, sort_keys=True))
        return 0
    receipt = execute_request(
        request=request,
        repo_root=args.repo_root,
        receipt_root=args.receipt_root,
        source_commit=args.source_commit,
        pyfcstm_commit=args.pyfcstm_commit,
        command=command,
    )
    print(json.dumps({"receipt": str(args.receipt_root / "receipt.json"), "state": receipt.state.value, "verdict": receipt.verdict, "acceptance_match": receipt.acceptance_match}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
