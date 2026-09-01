"""Non-short-circuit composition of evaluation-only native-oracle requests.

This module is isolated from the frozen method package and registry. It adds no
state-machine semantics: each child is an independently hash-sealed
``NativeOracleRequest`` evaluated by ``predicate_gold_oracle`` over pyfcstm
objects. The parent Boolean is only the explicit conjunction of every child.
"""

from __future__ import annotations

import argparse
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from . import predicate_gold_oracle as native_oracle_module
from .predicate_gold import (
    SHA256_PATTERN,
    ExactnessRelation,
    StrictModel,
    canonical_sha256,
    sha256_path,
    write_json,
)
from .predicate_gold_oracle import (
    ArtifactRole,
    NativeOracleRequest,
)
from .predicate_gold_oracle import execute_request as execute_native_request
from .predicate_gold_oracle import (
    receipt_semantic_projection as native_receipt_semantic_projection,
)

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.native-composite-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.native-composite-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.native-composite-replay.v1"


class NativeCompositeRequest(StrictModel):
    """Pre-result non-short-circuit AND of native-oracle requests."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(
        default=REQUEST_SCHEMA_VERSION,
        description="Evaluation-only native-composite request schema version.",
    )
    request_id: str = Field(
        description="Stable parent request identity.",
        pattern=r"^[A-Za-z0-9_.:-]+$",
    )
    ledger_id: str = Field(description="Ledger issue owning the composite.", min_length=1)
    property_id: str = Field(description="Pre-execution composite property identity.", min_length=1)
    property_proposal_sha256: str = Field(
        description="Hash of O, composite P, inputs, and assumptions frozen before execution.",
        pattern=SHA256_PATTERN,
    )
    exactness_relation: ExactnessRelation = Field(
        description="O/P relation of the complete conjunction."
    )
    operator: Literal["AND"] = Field(
        default="AND", description="The only admitted native-composite operator."
    )
    no_short_circuit: Literal[True] = Field(
        default=True, description="Every child must execute even after a false child."
    )
    artifact_role: ArtifactRole = Field(
        description="Defective artifact or independently justified positive control."
    )
    artifact_path: str = Field(description="Shared repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of the shared FCSTM bytes.", pattern=SHA256_PATTERN)
    constituents: tuple[NativeOracleRequest, ...] = Field(
        description="At least two complete native-oracle child requests.", min_length=2
    )
    assumptions: tuple[str, ...] = Field(
        description="Source-backed assumptions for the complete conjunction."
    )
    expected_boolean_for_acceptance: bool = Field(
        description="False for defective artifacts and true for positive controls."
    )
    created_at: str = Field(description="UTC proposal freeze time.", min_length=1)
    request_sha256: str = Field(
        description="Canonical request digest excluding this field.", pattern=SHA256_PATTERN
    )

    @model_validator(mode="after")
    def validate_request(self) -> NativeCompositeRequest:
        """Require aligned children, role polarity, uniqueness, and a valid seal."""

        ids = [item.request_id for item in self.constituents]
        if len(ids) != len(set(ids)):
            raise ValueError("native-composite child request IDs must be unique")
        for child in self.constituents:
            if (
                child.ledger_id != self.ledger_id
                or child.property_proposal_sha256 != self.property_proposal_sha256
                or child.artifact_role != self.artifact_role
                or child.artifact_path != self.artifact_path
                or child.artifact_sha256 != self.artifact_sha256
                or child.expected_boolean_for_acceptance
                != self.expected_boolean_for_acceptance
            ):
                raise ValueError("native-composite child does not match parent binding")
            if child.exactness_relation not in {
                ExactnessRelation.EQUIVALENT,
                ExactnessRelation.O_IMPLIES_P,
            }:
                raise ValueError("native-composite child must be exact or a sound falsifier")
        if (
            self.artifact_role == ArtifactRole.DEFECTIVE
            and self.expected_boolean_for_acceptance is not False
        ):
            raise ValueError("defective native composite must pre-register false")
        if (
            self.artifact_role == ArtifactRole.POSITIVE_CONTROL
            and self.expected_boolean_for_acceptance is not True
        ):
            raise ValueError("positive-control native composite must pre-register true")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"request_sha256"})
        )
        if self.request_sha256 != expected:
            raise ValueError("native-composite request_sha256 does not match payload")
        return self


class NativeCompositeConstituentReceipt(StrictModel):
    """One completed child receipt summarized without discarding its evidence."""

    request_id: str = Field(description="Child native-oracle request identity.", min_length=1)
    property_id: str = Field(description="Child property or sub-obligation identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(
        description="Relation of the child property to its explicitly identified sub-obligation."
    )
    request_sha256: str = Field(description="Child request digest.", pattern=SHA256_PATTERN)
    receipt_path: str = Field(description="Parent-root-relative child receipt path.", min_length=1)
    receipt_file_sha256: str = Field(description="Hash of child receipt bytes.", pattern=SHA256_PATTERN)
    receipt_payload_sha256: str = Field(description="Canonical child receipt digest.", pattern=SHA256_PATTERN)
    semantic_projection_sha256: str = Field(
        description="Digest of all deterministic child observations.", pattern=SHA256_PATTERN
    )
    verdict: bool = Field(description="Completed child Boolean verdict.")
    acceptance_match: bool = Field(description="Whether the child matched pre-registered polarity.")
    owner_path: tuple[str, ...] = Field(description="Native owner path resolved by the child.", min_length=1)
    constituent_count: int = Field(
        description="Number of non-short-circuited checks in the child receipt.", ge=1
    )


class NativeCompositeReceipt(StrictModel):
    """Hash-sealed completed Boolean receipt for a native conjunction."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(
        default=RECEIPT_SCHEMA_VERSION,
        description="Evaluation-only native-composite receipt schema version.",
    )
    request_id: str = Field(description="Parent request identity.", min_length=1)
    request_sha256: str = Field(description="Parent pre-result request digest.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue owning the result.", min_length=1)
    property_id: str = Field(description="Composite property identity.", min_length=1)
    exactness_relation: ExactnessRelation = Field(description="Frozen relation of O to the complete P.")
    operator: Literal["AND"] = Field(description="Executed Boolean operator.")
    no_short_circuit: Literal[True] = Field(description="Confirms every child was evaluated.")
    artifact_role: ArtifactRole = Field(description="Defective or positive-control artifact.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN)
    state: Literal["COMPLETED_BOOLEAN"] = Field(description="Only completed native Booleans are persisted.")
    verdict: bool = Field(description="Conjunction of every child verdict.")
    acceptance_match: bool = Field(description="Whether verdict matched the pre-registered polarity.")
    constituents: tuple[NativeCompositeConstituentReceipt, ...] = Field(
        description="All child receipts in request order.", min_length=2
    )
    code_hashes: dict[str, str] = Field(description="Hashes of parent and child oracle code.")
    source_commit: str = Field(description="Main repository commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Exact portable replay argv.", min_length=1)
    started_at: str = Field(description="UTC execution start time.", min_length=1)
    completed_at: str = Field(description="UTC completion time.", min_length=1)
    reason: str = Field(description="How the parent Boolean was obtained.", min_length=1)
    basis: str = Field(description="Native child and composition evidence basis.", min_length=1)
    receipt_sha256: str = Field(
        description="Canonical receipt digest excluding this field.", pattern=SHA256_PATTERN
    )

    @model_validator(mode="after")
    def validate_receipt(self) -> NativeCompositeReceipt:
        """Require a complete conjunction and a valid receipt seal."""

        if self.verdict != all(item.verdict for item in self.constituents):
            raise ValueError("native-composite verdict must equal every child verdict")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"receipt_sha256"})
        )
        if self.receipt_sha256 != expected:
            raise ValueError("native-composite receipt_sha256 does not match payload")
        return self


class NativeCompositeReplayReceipt(StrictModel):
    """Semantic replay comparison for one native conjunction."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(
        default=REPLAY_SCHEMA_VERSION,
        description="Evaluation-only native-composite replay schema version.",
    )
    request_sha256: str = Field(description="Replayed parent request digest.", pattern=SHA256_PATTERN)
    original_receipt_path: str = Field(description="Original receipt path.", min_length=1)
    original_receipt_sha256: str = Field(description="Original receipt file hash.", pattern=SHA256_PATTERN)
    replay_receipt_path: str = Field(description="Replay-root-relative receipt path.", min_length=1)
    replay_receipt_sha256: str = Field(description="Replay receipt file hash.", pattern=SHA256_PATTERN)
    original_projection_sha256: str = Field(description="Original semantic digest.", pattern=SHA256_PATTERN)
    replay_projection_sha256: str = Field(description="Replay semantic digest.", pattern=SHA256_PATTERN)
    original_verdict: bool = Field(description="Original parent Boolean.")
    replay_verdict: bool = Field(description="Replay parent Boolean.")
    overall_match: bool = Field(description="Whether the complete semantic projections match.")
    replayed_at: str = Field(description="UTC replay completion time.", min_length=1)
    reason: str = Field(description="Fields compared during replay.", min_length=1)
    receipt_sha256: str = Field(description="Canonical replay digest.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_replay(self) -> NativeCompositeReplayReceipt:
        """Require match and digest fields to reflect the replay evidence."""

        expected_match = (
            self.original_verdict == self.replay_verdict
            and self.original_projection_sha256 == self.replay_projection_sha256
        )
        if self.overall_match != expected_match:
            raise ValueError("overall_match does not reflect native-composite replay")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"receipt_sha256"})
        )
        if self.receipt_sha256 != expected:
            raise ValueError("native-composite replay digest does not match payload")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repo_relative(repo_root: Path, path: Path) -> str:
    """Return a repository-relative path for portable saved commands."""

    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def receipt_semantic_projection(receipt: NativeCompositeReceipt) -> dict[str, object]:
    """Return deterministic parent and child semantics for replay comparison."""

    return {
        "request_sha256": receipt.request_sha256,
        "ledger_id": receipt.ledger_id,
        "property_id": receipt.property_id,
        "exactness_relation": receipt.exactness_relation,
        "operator": receipt.operator,
        "no_short_circuit": receipt.no_short_circuit,
        "artifact_role": receipt.artifact_role,
        "artifact_sha256": receipt.artifact_sha256,
        "state": receipt.state,
        "verdict": receipt.verdict,
        "acceptance_match": receipt.acceptance_match,
        "constituents": tuple(
            {
                "request_id": item.request_id,
                "property_id": item.property_id,
                "exactness_relation": item.exactness_relation,
                "request_sha256": item.request_sha256,
                "semantic_projection_sha256": item.semantic_projection_sha256,
                "verdict": item.verdict,
                "acceptance_match": item.acceptance_match,
                "owner_path": item.owner_path,
                "constituent_count": item.constituent_count,
            }
            for item in receipt.constituents
        ),
        "code_hashes": receipt.code_hashes,
        "source_commit": receipt.source_commit,
        "pyfcstm_commit": receipt.pyfcstm_commit,
    }


def execute_request(
    request: NativeCompositeRequest,
    *,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> NativeCompositeReceipt:
    """Execute every child in order and persist the complete conjunction."""

    started_at = _utc_now()
    receipt_root.mkdir(parents=True, exist_ok=True)
    write_json(receipt_root / "query.json", request.model_dump(mode="json"))
    summaries: list[NativeCompositeConstituentReceipt] = []
    for index, child in enumerate(request.constituents):
        child_root = receipt_root / "constituents" / f"{index:02d}-{child.request_id}"
        child_request_path = child_root / "request.json"
        write_json(child_request_path, child.model_dump(mode="json"))
        child_command = (
            "python",
            "-m",
            "paper_stm_evaluation.predicate_gold_oracle",
            "--request",
            _repo_relative(repo_root, child_request_path),
            "--repo-root",
            ".",
            "--receipt-root",
            _repo_relative(repo_root, child_root),
            "--source-commit",
            source_commit,
            "--pyfcstm-commit",
            pyfcstm_commit,
        )
        child_receipt = execute_native_request(
            child,
            repo_root=repo_root,
            receipt_root=child_root,
            source_commit=source_commit,
            pyfcstm_commit=pyfcstm_commit,
            command=child_command,
        )
        child_receipt_path = child_root / "receipt.json"
        summaries.append(
            NativeCompositeConstituentReceipt(
                request_id=child.request_id,
                property_id=child.property_id,
                exactness_relation=child.exactness_relation,
                request_sha256=child.request_sha256,
                receipt_path=child_receipt_path.relative_to(receipt_root).as_posix(),
                receipt_file_sha256=sha256_path(child_receipt_path),
                receipt_payload_sha256=child_receipt.receipt_sha256,
                semantic_projection_sha256=canonical_sha256(
                    native_receipt_semantic_projection(child_receipt)
                ),
                verdict=child_receipt.verdict,
                acceptance_match=child_receipt.acceptance_match,
                owner_path=child_receipt.owner_path,
                constituent_count=len(child_receipt.constituents),
            )
        )
    verdict = all(item.verdict for item in summaries)
    module_path = Path(__file__).resolve()
    child_module_path = Path(inspect.getsourcefile(native_oracle_module) or "").resolve()
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
        "state": "COMPLETED_BOOLEAN",
        "verdict": verdict,
        "acceptance_match": verdict == request.expected_boolean_for_acceptance,
        "constituents": [item.model_dump(mode="json") for item in summaries],
        "code_hashes": {
            _repo_relative(repo_root, module_path): sha256_path(module_path),
            _repo_relative(repo_root, child_module_path): sha256_path(child_module_path),
        },
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "reason": "Every native-oracle child executed without short-circuiting; the parent Boolean is their explicit conjunction.",
        "basis": "Hash-frozen child requests, complete native child receipts, and an operator-only parent that adds no state-machine semantics.",
    }
    receipt = NativeCompositeReceipt(
        **unsigned, receipt_sha256=canonical_sha256(unsigned)
    )
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def replay_request(
    request: NativeCompositeRequest,
    *,
    original_receipt: NativeCompositeReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> NativeCompositeReplayReceipt:
    """Re-execute every child and compare full parent/child semantics."""

    if original_receipt.request_sha256 != request.request_sha256:
        raise ValueError("replay request does not match original native composite")
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
        original_path = _repo_relative(repo_root, original_receipt_path)
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
        "reason": "Compared parent Boolean and acceptance, every child request and native semantic projection, artifact/code hashes, and pinned commits; paths, commands, and timestamps are excluded.",
    }
    audit = NativeCompositeReplayReceipt(
        **unsigned, receipt_sha256=canonical_sha256(unsigned)
    )
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the provider-free native-composite CLI."""

    parser = argparse.ArgumentParser(
        description="Execute or replay one pre-hashed native-oracle conjunction."
    )
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-against", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate and execute an original or replay native conjunction."""

    args = _parser().parse_args(argv)
    request = NativeCompositeRequest.model_validate_json(
        args.request.read_text(encoding="utf-8")
    )
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_native_composite",
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
        original = NativeCompositeReceipt.model_validate_json(
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
            command=(*command, "--replay-against", str(args.replay_against)),
        )
        output = {
            "replay_audit": str(args.receipt_root / "replay_audit.json"),
            "overall_match": audit.overall_match,
        }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
