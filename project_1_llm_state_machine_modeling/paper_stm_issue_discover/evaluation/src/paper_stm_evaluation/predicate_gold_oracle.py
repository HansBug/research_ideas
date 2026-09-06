"""Evaluation-only native pyfcstm oracles for predicate gold.

This module is intentionally outside the frozen method package.  It consumes
pyfcstm model objects and never parses PlantUML text or invents an execution
semantics.  Each oracle has a narrow, explicit contract and records every
constituent check without short-circuiting.
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

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.native-oracle-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.native-oracle-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.native-oracle-replay.v1"
ORACLE_ID = "NATIVE_INITIAL_TRANSITION_CONTRACT"


class ArtifactRole(str, Enum):
    """Role of the FCSTM artifact evaluated by the native oracle."""

    DEFECTIVE = "DEFECTIVE"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"


class Cardinality(str, Enum):
    """Supported cardinality requirements for one owner's initial edges."""

    EXACTLY_ONE = "EXACTLY_ONE"
    AT_LEAST_ONE = "AT_LEAST_ONE"


class NativeOracleRequest(StrictModel):
    """Pre-result request for the initial-transition native oracle."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(
        default=REQUEST_SCHEMA_VERSION,
        description="Evaluation-only native-oracle request schema version.",
    )
    request_id: str = Field(description="Stable request identity.", pattern=r"^[A-Za-z0-9_.:-]+$")
    ledger_id: str = Field(description="Ledger issue owning this proposal.", min_length=1)
    property_id: str = Field(description="Pre-execution property identity.", min_length=1)
    property_proposal_sha256: str = Field(
        description="Hash of O, P, inputs, and assumptions frozen before execution.",
        pattern=SHA256_PATTERN,
    )
    exactness_relation: ExactnessRelation = Field(
        description="EQUIVALENT for exact candidates or O_IMPLIES_P for sound proxies."
    )
    oracle_id: Literal[ORACLE_ID] = Field(
        default=ORACLE_ID,
        description="Narrow evaluation-only oracle identifier.",
    )
    artifact_role: ArtifactRole = Field(description="Defective artifact or independently justified control.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN)
    typed_inputs: tuple[TypedInput, ...] = Field(
        description="Hash-frozen inputs: owner_path, cardinality, required_target_path, require_no_event, and require_no_guard."
    )
    assumptions: tuple[str, ...] = Field(description="Source-backed assumptions used to compare O and P.")
    expected_boolean_for_acceptance: bool = Field(
        description="False for defective requests and true for positive controls."
    )
    created_at: str = Field(description="UTC proposal freeze time.", min_length=1)
    request_sha256: str = Field(description="Canonical request hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_request(self) -> NativeOracleRequest:
        """Reject incomplete, duplicate, or role-inverted requests."""

        values = {item.field_name: item.normalized_value for item in self.typed_inputs}
        expected_names = {
            "owner_path",
            "cardinality",
            "required_target_path",
            "require_no_event",
            "require_no_guard",
        }
        if set(values) != expected_names or len(self.typed_inputs) != len(expected_names):
            raise ValueError(f"native initial-transition oracle requires exactly {sorted(expected_names)}")
        owner_path = values["owner_path"]
        target_path = values["required_target_path"]
        if not isinstance(owner_path, list) or not owner_path or not all(isinstance(part, str) and part for part in owner_path):
            raise ValueError("owner_path must be a nonempty array of exact native state names")
        if target_path is not None and (
            not isinstance(target_path, list)
            or not target_path
            or not all(isinstance(part, str) and part for part in target_path)
        ):
            raise ValueError("required_target_path must be null or a nonempty exact native path")
        try:
            Cardinality(values["cardinality"])
        except (TypeError, ValueError) as exc:
            raise ValueError("unsupported initial-transition cardinality") from exc
        if not isinstance(values["require_no_event"], bool) or not isinstance(values["require_no_guard"], bool):
            raise TypeError("require_no_event and require_no_guard must be Boolean")
        if self.artifact_role == ArtifactRole.DEFECTIVE and self.expected_boolean_for_acceptance is not False:
            raise ValueError("defective requests pre-register false")
        if self.artifact_role == ArtifactRole.POSITIVE_CONTROL and self.expected_boolean_for_acceptance is not True:
            raise ValueError("positive-control requests pre-register true")
        if self.request_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"request_sha256"})):
            raise ValueError("request_sha256 does not match the pre-result request")
        return self


class ConstituentResult(StrictModel):
    """One non-short-circuited Boolean constituent of the native property."""

    constituent_id: str = Field(description="Stable check identity.", min_length=1)
    verdict: bool = Field(description="Completed Boolean result of this constituent.")
    expected: JsonValue = Field(description="Pre-registered expected value or condition.")
    observed: JsonValue = Field(description="Native pyfcstm value observed from the artifact.")
    reason: str = Field(description="How the observed value determines this constituent.", min_length=1)


class NativeOracleReceipt(StrictModel):
    """Hash-sealed result of one native initial-transition contract query."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(
        default=RECEIPT_SCHEMA_VERSION,
        description="Evaluation-only native-oracle receipt schema version.",
    )
    request_id: str = Field(description="Request identity.", min_length=1)
    request_sha256: str = Field(description="Hash of the pre-result request.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue owning the request.", min_length=1)
    property_id: str = Field(description="Selected property identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(
        description="O/P direction frozen before this native child or standalone query executed."
    )
    oracle_id: Literal[ORACLE_ID] = Field(description="Executed native oracle identity.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN)
    state: Literal["COMPLETED_BOOLEAN"] = Field(description="Only a completed native Boolean query is persisted.")
    verdict: bool = Field(description="Conjunction of all recorded constituent verdicts.")
    acceptance_match: bool = Field(description="Whether verdict equals the pre-registered acceptance value.")
    owner_path: tuple[str, ...] = Field(description="Exact native owner path resolved by pyfcstm.", min_length=1)
    initial_transitions: tuple[dict[str, JsonValue], ...] = Field(
        description="Complete native initial-transition inventory used by every constituent."
    )
    constituents: tuple[ConstituentResult, ...] = Field(
        description="All cardinality, target, event, and guard checks evaluated without short-circuiting.",
        min_length=3,
    )
    code_hashes: dict[str, str] = Field(description="Hashes of this oracle and pyfcstm model loader source.")
    source_commit: str = Field(description="Main repository commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Exact provider-free replay argv.", min_length=1)
    started_at: str = Field(description="UTC start time.", min_length=1)
    completed_at: str = Field(description="UTC completion time.", min_length=1)
    replay_status: Literal["NOT_REPLAYED", "REPLAY_MATCH", "REPLAY_MISMATCH"] = Field(
        description="Independent replay disposition."
    )
    reason: str = Field(description="Verdict interpretation and exact oracle boundary.", min_length=1)
    basis: str = Field(description="Native object and source-code basis.", min_length=1)
    receipt_sha256: str = Field(description="Canonical receipt hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_receipt(self) -> NativeOracleReceipt:
        """Require the overall verdict to equal the full conjunction and seal."""

        if self.verdict != all(item.verdict for item in self.constituents):
            raise ValueError("overall verdict must equal all non-short-circuited constituents")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match receipt payload")
        return self


class NativeOracleReplayReceipt(StrictModel):
    """Semantic replay comparison for one native-oracle request."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(
        default=REPLAY_SCHEMA_VERSION,
        description="Evaluation-only native-oracle replay schema version.",
    )
    request_sha256: str = Field(
        description="Hash of the replayed pre-result request.",
        pattern=SHA256_PATTERN,
    )
    original_receipt_path: str = Field(
        description="Repository- or invocation-relative original receipt path.",
        min_length=1,
    )
    original_receipt_sha256: str = Field(
        description="SHA-256 of the original receipt bytes.",
        pattern=SHA256_PATTERN,
    )
    replay_receipt_path: str = Field(
        description="Replay-root-relative replay receipt path.", min_length=1
    )
    replay_receipt_sha256: str = Field(
        description="SHA-256 of the replay receipt bytes.",
        pattern=SHA256_PATTERN,
    )
    original_projection_sha256: str = Field(
        description="Digest of the original terminal semantic projection.",
        pattern=SHA256_PATTERN,
    )
    replay_projection_sha256: str = Field(
        description="Digest of the replay terminal semantic projection.",
        pattern=SHA256_PATTERN,
    )
    original_verdict: bool = Field(description="Original completed Boolean verdict.")
    replay_verdict: bool = Field(description="Replay completed Boolean verdict.")
    overall_match: bool = Field(
        description="Whether verdict and complete native observations match."
    )
    replayed_at: str = Field(description="UTC replay completion time.", min_length=1)
    reason: str = Field(
        description="Exact native fields included in the replay comparison.",
        min_length=1,
    )
    receipt_sha256: str = Field(
        description="Canonical replay-audit digest excluding this field.",
        pattern=SHA256_PATTERN,
    )

    @model_validator(mode="after")
    def validate_replay(self) -> NativeOracleReplayReceipt:
        """Require the match flag and replay digest to reflect the evidence."""

        expected_match = (
            self.original_verdict == self.replay_verdict
            and self.original_projection_sha256 == self.replay_projection_sha256
        )
        if self.overall_match != expected_match:
            raise ValueError("overall_match does not reflect native replay comparison")
        expected_hash = canonical_sha256(
            self.model_dump(mode="json", exclude={"receipt_sha256"})
        )
        if self.receipt_sha256 != expected_hash:
            raise ValueError("receipt_sha256 does not match native replay audit")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def receipt_semantic_projection(receipt: NativeOracleReceipt) -> dict[str, object]:
    """Return deterministic native observations, excluding paths and timestamps."""

    return {
        "request_sha256": receipt.request_sha256,
        "ledger_id": receipt.ledger_id,
        "property_id": receipt.property_id,
        "exactness_relation": receipt.exactness_relation,
        "oracle_id": receipt.oracle_id,
        "artifact_role": receipt.artifact_role,
        "artifact_sha256": receipt.artifact_sha256,
        "state": receipt.state,
        "verdict": receipt.verdict,
        "acceptance_match": receipt.acceptance_match,
        "owner_path": receipt.owner_path,
        "initial_transitions": receipt.initial_transitions,
        "constituents": tuple(
            item.model_dump(mode="json") for item in receipt.constituents
        ),
        "source_commit": receipt.source_commit,
        "pyfcstm_commit": receipt.pyfcstm_commit,
        "code_hashes": receipt.code_hashes,
    }


def _resolve_state(machine: object, path: list[str]) -> object:
    """Resolve one exact pyfcstm state path without fuzzy matching."""

    root = machine.root_state
    if path[0] != root.name:
        raise ValueError(f"owner path must start with native root {root.name!r}")
    current = root
    for part in path[1:]:
        state = current.substates.get(part)
        if state is None:
            raise ValueError(f"exact state path component {part!r} did not resolve")
        current = state
    return current


def _transition_target_path(owner: object, transition: object) -> list[str] | None:
    """Resolve an initial transition target to its exact owner-local path."""

    target = transition.to_state
    if not isinstance(target, str):
        return None
    state = owner.substates.get(target)
    if state is None:
        return None
    return list(state.path)


def evaluate_request(request: NativeOracleRequest, *, repo_root: Path) -> tuple[tuple[str, ...], tuple[dict[str, JsonValue], ...], tuple[ConstituentResult, ...]]:
    """Evaluate every initial-transition constituent on native pyfcstm objects."""

    from pyfcstm.model import load_state_machine_from_text

    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match the pre-hashed request")
    machine = load_state_machine_from_text(artifact.read_text(encoding="utf-8"))
    values = {item.field_name: item.normalized_value for item in request.typed_inputs}
    owner = _resolve_state(machine, values["owner_path"])
    transitions = tuple(owner.init_transitions)
    observed: list[dict[str, JsonValue]] = []
    for index, transition in enumerate(transitions):
        observed.append(
            {
                "index": index,
                "target_path": _transition_target_path(owner, transition),
                "event": transition.event.name if transition.event is not None else None,
                "guard": str(transition.guard) if transition.guard is not None else None,
                "effect_count": len(transition.effects),
            }
        )

    cardinality = Cardinality(values["cardinality"])
    cardinality_ok = len(transitions) == 1 if cardinality == Cardinality.EXACTLY_ONE else len(transitions) >= 1
    target = values["required_target_path"]
    target_ok = target is None or (len(transitions) > 0 and all(row["target_path"] == target for row in observed))
    event_ok = not values["require_no_event"] or (len(transitions) > 0 and all(row["event"] is None for row in observed))
    guard_ok = not values["require_no_guard"] or (len(transitions) > 0 and all(row["guard"] is None for row in observed))
    constituents = (
        ConstituentResult(constituent_id="cardinality", verdict=cardinality_ok, expected=cardinality.value, observed=len(transitions), reason="Compared the complete native owner.init_transitions cardinality."),
        ConstituentResult(constituent_id="target", verdict=target_ok, expected=target, observed=[row["target_path"] for row in observed], reason="Compared every native initial-transition target; null means the obligation did not constrain the target."),
        ConstituentResult(constituent_id="event", verdict=event_ok, expected=None if values["require_no_event"] else "ANY", observed=[row["event"] for row in observed], reason="Checked every native initial transition; no transition was skipped after another failure."),
        ConstituentResult(constituent_id="guard", verdict=guard_ok, expected=None if values["require_no_guard"] else "ANY", observed=[row["guard"] for row in observed], reason="Checked every native initial transition; no transition was skipped after another failure."),
    )
    return tuple(owner.path), tuple(observed), constituents


def execute_request(
    request: NativeOracleRequest,
    *,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> NativeOracleReceipt:
    """Execute, hash, and persist one completed native-oracle query."""

    from pyfcstm.model import model as pyfcstm_model

    started_at = _utc_now()
    owner_path, transitions, constituents = evaluate_request(request, repo_root=repo_root)
    verdict = all(item.verdict for item in constituents)
    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    write_json(query_path, request.model_dump(mode="json"))
    module_path = Path(__file__).resolve()
    pyfcstm_path = Path(inspect.getsourcefile(pyfcstm_model) or "").resolve()
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
        "owner_path": owner_path,
        "initial_transitions": transitions,
        "constituents": [item.model_dump(mode="json") for item in constituents],
        "code_hashes": {
            module_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(module_path),
            pyfcstm_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(pyfcstm_path),
        },
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "replay_status": "NOT_REPLAYED",
        "reason": "The native pyfcstm initial-transition inventory was evaluated completely; the Boolean is the conjunction of the persisted constituents.",
        "basis": "pyfcstm State.init_transitions, exact native state paths, and the hash-frozen request; no PlantUML regex or custom runtime semantics were used.",
    }
    receipt = NativeOracleReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def replay_request(
    request: NativeOracleRequest,
    *,
    original_receipt: NativeOracleReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> NativeOracleReplayReceipt:
    """Re-execute one native request and compare every semantic observation."""

    if original_receipt.request_sha256 != request.request_sha256:
        raise ValueError("replay request does not match original native receipt")
    replay = execute_request(
        request,
        repo_root=repo_root,
        receipt_root=replay_root,
        source_commit=source_commit,
        pyfcstm_commit=pyfcstm_commit,
        command=command,
    )
    original_projection = canonical_sha256(
        receipt_semantic_projection(original_receipt)
    )
    replay_projection = canonical_sha256(receipt_semantic_projection(replay))
    replay_receipt_path = replay_root / "receipt.json"
    try:
        original_path = (
            original_receipt_path.resolve()
            .relative_to(repo_root.resolve())
            .as_posix()
        )
    except ValueError:
        original_path = original_receipt_path.as_posix()
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": original_path,
        "original_receipt_sha256": sha256_path(original_receipt_path),
        "replay_receipt_path": replay_receipt_path.relative_to(replay_root).as_posix(),
        "replay_receipt_sha256": sha256_path(replay_receipt_path),
        "original_projection_sha256": original_projection,
        "replay_projection_sha256": replay_projection,
        "original_verdict": original_receipt.verdict,
        "replay_verdict": replay.verdict,
        "overall_match": (
            original_receipt.verdict == replay.verdict
            and original_projection == replay_projection
        ),
        "replayed_at": _utc_now(),
        "reason": "Compared the completed Boolean, full initial-transition inventory, every non-short-circuited constituent, artifact/code hashes, and pinned commits; paths, commands, and timestamps are excluded.",
    }
    audit = NativeOracleReplayReceipt(
        **unsigned, receipt_sha256=canonical_sha256(unsigned)
    )
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the provider-free native-oracle CLI."""

    parser = argparse.ArgumentParser(description="Execute one pre-hashed evaluation-only native oracle request.")
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-against", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Execute one native-oracle request and print its normalized result."""

    args = _parser().parse_args(argv)
    request = NativeOracleRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_oracle",
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
        original = NativeOracleReceipt.model_validate_json(
            args.replay_against.read_text(encoding="utf-8")
        )
        replay_command = (*command, "--replay-against", str(args.replay_against))
        audit = replay_request(
            request,
            original_receipt=original,
            original_receipt_path=args.replay_against,
            repo_root=args.repo_root,
            replay_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=replay_command,
        )
        output = {
            "replay_audit": str(args.receipt_root / "replay_audit.json"),
            "overall_match": audit.overall_match,
        }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
