"""Build an evaluator-only compatibility view of immutable method releases."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Literal, Sequence

from pydantic import BaseModel, ConfigDict, Field

from paper_stm_method.inputs import FROZEN_PAIR_IDS


PROJECTION_SCHEMA = "evidence-discovery.judge-input-projection.v1"
AUDIT_SCHEMA = "evidence-discovery.judge-input-projection-audit.v1"
PROJECTION_ALGORITHM_VERSION = "judge-input-compatibility-projection/1"


class ProjectedMethodRelease(BaseModel):
    """Minimal release surface accepted by the frozen semantic Judge adapter."""

    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

    schema_version: Literal["evidence-discovery.judge-input-projection.v1"] = Field(
        default=PROJECTION_SCHEMA,
        alias="schema",
        description="Explicit evaluator-only schema; this record is not a replacement method cell.",
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="Compatibility status required by the frozen Judge adapter after projection policy validation.",
    )
    eligible: Literal[True] = Field(
        default=True,
        description="Evaluator input eligibility; it does not revise the original method eligibility decision.",
    )
    pair_id: str = Field(
        min_length=4,
        description="Frozen corpus pair identifier copied from the immutable method cell.",
    )
    round: int = Field(
        ge=1,
        description="Method round copied from the immutable method cell.",
    )
    report_issue_clusters: tuple[dict[str, Any], ...] = Field(
        description="Eligible published reports preserved exactly, or an empty surface for an ineligible method cell.",
    )
    projection_action: Literal[
        "normalize_eligible_diagnostic", "empty_ineligible_publication_surface"
    ] = Field(
        description="Deterministic compatibility operation applied without changing Judge semantics.",
    )
    original_method_record_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 hash of the immutable source method record.",
    )
    original_method_status: str = Field(
        min_length=1,
        description="Original method terminal status retained for evaluator audit.",
    )
    original_method_eligible: bool = Field(
        description="Original method eligibility retained without reinterpretation.",
    )
    reason: str = Field(
        min_length=1,
        description="Why this evaluator-only projection is valid for the frozen Judge adapter.",
    )
    basis: str = Field(
        min_length=1,
        description="Concrete source status, eligibility, report count, and hash supporting the projection.",
    )


class JudgeInputProjectionCellAudit(BaseModel):
    """Hash-closed audit row for one method cell and its evaluator projection."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pair_id: str = Field(
        min_length=4,
        description="Frozen corpus pair identifier validated against the source record and path.",
    )
    round: int = Field(
        ge=1,
        description="Method round validated against the source record and path.",
    )
    action: Literal[
        "hardlink_unchanged",
        "normalize_eligible_diagnostic",
        "empty_ineligible_publication_surface",
    ] = Field(
        description="Exact operation used to construct this evaluator input.",
    )
    original_path: str = Field(
        min_length=1,
        description="Absolute path of the immutable method cell.",
    )
    original_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 hash of the immutable method cell bytes.",
    )
    projected_path: str = Field(
        min_length=1,
        description="Absolute path consumed by the frozen Judge adapter.",
    )
    projected_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 hash of the projected evaluator input bytes.",
    )
    hardlink_identity_preserved: bool = Field(
        description="Whether source and projection share one inode because no projection was needed.",
    )
    original_status: str = Field(
        min_length=1,
        description="Method terminal status before compatibility projection.",
    )
    projected_status: Literal["completed"] = Field(
        default="completed",
        description="Status visible to the frozen Judge adapter after policy validation.",
    )
    original_eligible: bool = Field(
        description="Method eligibility before compatibility projection.",
    )
    projected_eligible: Literal[True] = Field(
        default=True,
        description="Evaluator input eligibility after applying the explicit compatibility policy.",
    )
    original_report_count: int = Field(
        ge=0,
        description="Number of report clusters present in the immutable method cell.",
    )
    projected_report_count: int = Field(
        ge=0,
        description="Number of report clusters exposed to the frozen Judge adapter.",
    )
    original_reports_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Canonical SHA-256 hash of the original report cluster list.",
    )
    projected_reports_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Canonical SHA-256 hash of the report cluster list exposed to Judge.",
    )
    report_semantics_preserved: bool = Field(
        description="Whether every eligible report payload is exposed byte-for-value without semantic rewriting.",
    )
    reason: str = Field(
        min_length=1,
        description="Why the action is allowed and what publication boundary it enforces.",
    )
    basis: str = Field(
        min_length=1,
        description="Concrete status, eligibility, hashes, and counts supporting this audit row.",
    )


class JudgeInputProjectionAudit(BaseModel):
    """Complete provenance record for one evaluator-only method release tree."""

    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

    schema_version: Literal[
        "evidence-discovery.judge-input-projection-audit.v1"
    ] = Field(
        default=AUDIT_SCHEMA,
        alias="schema",
        description="Versioned schema for the evaluator compatibility projection audit.",
    )
    source_root: str = Field(
        min_length=1,
        description="Absolute immutable method run root from which cells were selected.",
    )
    projection_root: str = Field(
        min_length=1,
        description="Absolute evaluator-only source root supplied to the frozen Judge.",
    )
    projection_algorithm_version: Literal[
        "judge-input-compatibility-projection/1"
    ] = Field(
        default=PROJECTION_ALGORITHM_VERSION,
        description="Frozen deterministic projection policy implementation version.",
    )
    projection_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Clean repository commit containing the projection implementation.",
    )
    source_method_tree_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Deterministic hash over relative paths and immutable method cell bytes.",
    )
    projected_method_tree_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Deterministic hash over relative paths and evaluator projection bytes.",
    )
    cell_count: int = Field(
        ge=1,
        description="Total number of pair-round method inputs in the projection.",
    )
    unchanged_hardlink_count: int = Field(
        ge=0,
        description="Number of completed eligible cells reused through verified hardlinks.",
    )
    eligible_diagnostic_projection_count: int = Field(
        ge=0,
        description="Number of eligible diagnostic cells whose reports were preserved and status normalized.",
    )
    empty_publication_projection_count: int = Field(
        ge=0,
        description="Number of ineligible cells represented by an empty publication surface.",
    )
    cells: tuple[JudgeInputProjectionCellAudit, ...] = Field(
        min_length=1,
        description="One hash-closed audit row for every projected pair-round input.",
    )
    reason: str = Field(
        min_length=1,
        description="Why the projection preserves fixed expected denominators without judging ineligible reports.",
    )
    basis: str = Field(
        min_length=1,
        description="Compatibility policy and complete cell-level hash closure supporting this audit.",
    )


def _sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return _sha256_bytes(payload)


def _tree_hash(paths: Sequence[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def _write_model(path: Path, model: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = model.model_dump_json(indent=2, by_alias=True).encode("utf-8") + b"\n"
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _identity_from_path(path: Path) -> tuple[str, int]:
    pair_id = path.parent.name
    stem = path.stem
    if not stem.startswith("round-") or not stem.removeprefix("round-").isdigit():
        raise ValueError(f"invalid method release path: {path}")
    return pair_id, int(stem.removeprefix("round-"))


def _project_cell(
    source_path: Path,
    projected_path: Path,
) -> JudgeInputProjectionCellAudit:
    source_bytes = source_path.read_bytes()
    original_hash = _sha256_bytes(source_bytes)
    record = json.loads(source_bytes)
    path_pair_id, path_round = _identity_from_path(source_path)
    pair_id = str(record.get("pair_id") or "")
    round_no = int(record.get("round") or 0)
    if (pair_id, round_no) != (path_pair_id, path_round):
        raise ValueError(
            f"method identity mismatch at {source_path}: "
            f"record={(pair_id, round_no)}, path={(path_pair_id, path_round)}"
        )
    status = str(record.get("status") or "")
    eligible = bool(record.get("eligible"))
    reports = record.get("report_issue_clusters")
    if not isinstance(reports, list):
        raise TypeError(f"method release lacks report_issue_clusters list: {source_path}")

    action: Literal[
        "hardlink_unchanged",
        "normalize_eligible_diagnostic",
        "empty_ineligible_publication_surface",
    ]
    projected_reports: list[dict[str, Any]]
    hardlink_identity = False
    if status == "completed" and eligible:
        action = "hardlink_unchanged"
        projected_path.parent.mkdir(parents=True, exist_ok=True)
        os.link(source_path, projected_path)
        projected_reports = reports
        hardlink_identity = source_path.stat().st_ino == projected_path.stat().st_ino
        if not hardlink_identity or projected_path.read_bytes() != source_bytes:
            raise RuntimeError(f"hardlink identity check failed: {projected_path}")
        reason = (
            "The method cell is completed and eligible, so its immutable release is reused without projection."
        )
    elif status == "completed_with_diagnostics" and eligible:
        action = "normalize_eligible_diagnostic"
        projected_reports = reports
        projection = ProjectedMethodRelease(
            pair_id=pair_id,
            round=round_no,
            report_issue_clusters=tuple(reports),
            projection_action=action,
            original_method_record_hash=original_hash,
            original_method_status=status,
            original_method_eligible=eligible,
            reason=(
                "The method explicitly marked this cell eligible; diagnostic failures did not manufacture or invalidate its published report surface."
            ),
            basis=(
                f"status={status}; eligible={eligible}; reports={len(reports)}; original={original_hash}"
            ),
        )
        _write_model(projected_path, projection)
        reason = (
            "Eligible published reports are preserved exactly while the evaluator-only status is normalized for the frozen adapter."
        )
    elif status == "failed_with_receipt" and not eligible:
        action = "empty_ineligible_publication_surface"
        projected_reports = []
        projection = ProjectedMethodRelease(
            pair_id=pair_id,
            round=round_no,
            report_issue_clusters=(),
            projection_action=action,
            original_method_record_hash=original_hash,
            original_method_status=status,
            original_method_eligible=eligible,
            reason=(
                "The method cell is ineligible, so no report cluster is exposed; the empty surface preserves the fixed expected denominator as NONE outcomes."
            ),
            basis=(
                f"status={status}; eligible={eligible}; excluded_reports={len(reports)}; original={original_hash}"
            ),
        )
        _write_model(projected_path, projection)
        reason = (
            "Ineligible report clusters are excluded and only an empty evaluator publication surface is supplied."
        )
    else:
        raise ValueError(
            f"unsupported method terminal contract at {source_path}: "
            f"status={status!r}, eligible={eligible!r}"
        )

    projected_hash = _sha256_bytes(projected_path.read_bytes())
    original_reports_hash = _canonical_hash(reports)
    projected_reports_hash = _canonical_hash(projected_reports)
    semantics_preserved = reports == projected_reports
    return JudgeInputProjectionCellAudit(
        pair_id=pair_id,
        round=round_no,
        action=action,
        original_path=str(source_path.resolve()),
        original_hash=original_hash,
        projected_path=str(projected_path.resolve()),
        projected_hash=projected_hash,
        hardlink_identity_preserved=hardlink_identity,
        original_status=status,
        original_eligible=eligible,
        original_report_count=len(reports),
        projected_report_count=len(projected_reports),
        original_reports_hash=original_reports_hash,
        projected_reports_hash=projected_reports_hash,
        report_semantics_preserved=semantics_preserved,
        reason=reason,
        basis=(
            f"original={original_hash}; projected={projected_hash}; "
            f"original_reports={original_reports_hash}; projected_reports={projected_reports_hash}"
        ),
    )


def build_judge_input_projection(
    source_root: Path,
    projection_root: Path,
    *,
    projection_code_commit: str,
    expected_pair_ids: tuple[str, ...] | None = None,
    expected_rounds: tuple[int, ...] | None = None,
) -> JudgeInputProjectionAudit:
    """Create one immutable, hash-audited evaluator view without changing method files."""

    source_root = source_root.expanduser().resolve()
    projection_root = projection_root.expanduser().resolve()
    source_method_root = source_root / "method"
    if not source_method_root.is_dir():
        raise FileNotFoundError(source_method_root)
    if projection_root.exists() and any(projection_root.iterdir()):
        raise FileExistsError(f"projection root is non-empty: {projection_root}")
    projection_root.mkdir(parents=True, exist_ok=True)

    source_paths = tuple(sorted(source_method_root.glob("*/round-*.json")))
    if not source_paths:
        raise FileNotFoundError(f"no method releases under {source_method_root}")
    observed_keys = {_identity_from_path(path) for path in source_paths}
    if len(observed_keys) != len(source_paths):
        raise ValueError("duplicate pair-round method release identity")
    if expected_pair_ids is not None and expected_rounds is not None:
        expected_keys = {
            (pair_id, round_no)
            for pair_id in expected_pair_ids
            for round_no in expected_rounds
        }
        if observed_keys != expected_keys:
            missing = sorted(expected_keys - observed_keys)
            extra = sorted(observed_keys - expected_keys)
            raise ValueError(f"method release closure mismatch: missing={missing}, extra={extra}")

    cells: list[JudgeInputProjectionCellAudit] = []
    projected_paths: list[Path] = []
    for source_path in source_paths:
        relative_path = source_path.relative_to(source_root)
        projected_path = projection_root / relative_path
        cells.append(_project_cell(source_path, projected_path))
        projected_paths.append(projected_path)

    cells.sort(key=lambda item: (item.round, item.pair_id))
    audit = JudgeInputProjectionAudit(
        source_root=str(source_root),
        projection_root=str(projection_root),
        projection_code_commit=projection_code_commit,
        source_method_tree_hash=_tree_hash(source_paths, source_root),
        projected_method_tree_hash=_tree_hash(projected_paths, projection_root),
        cell_count=len(cells),
        unchanged_hardlink_count=sum(
            item.action == "hardlink_unchanged" for item in cells
        ),
        eligible_diagnostic_projection_count=sum(
            item.action == "normalize_eligible_diagnostic" for item in cells
        ),
        empty_publication_projection_count=sum(
            item.action == "empty_ineligible_publication_surface" for item in cells
        ),
        cells=tuple(cells),
        reason=(
            "The frozen Judge receives every fixed pair-round input: eligible report semantics are unchanged, while ineligible cells contribute an empty publication surface and therefore only NONE expected outcomes."
        ),
        basis=(
            "Immutable source hashes; hardlink identity for unchanged cells; explicit completed_with_diagnostics/eligible and failed_with_receipt/ineligible projection rules."
        ),
    )
    _write_model(projection_root / "judge_input_projection_audit.json", audit)
    return audit


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--projection-root", type=Path, required=True)
    parser.add_argument("--pair-id", action="append", dest="pair_ids")
    parser.add_argument("--round", action="append", type=int, dest="rounds")
    return parser


def _require_clean_commit(repository_path: Path) -> str:
    status = subprocess.check_output(
        ("git", "status", "--porcelain", "--untracked-files=no"),
        cwd=repository_path,
        text=True,
    ).strip()
    if status:
        raise RuntimeError(
            "Judge input projection requires a clean tracked commit"
        )
    return subprocess.check_output(
        ("git", "rev-parse", "HEAD"), cwd=repository_path, text=True
    ).strip()


def main(argv: Sequence[str] | None = None) -> int:
    """Build the compatibility tree and print its validated audit record."""

    args = _parser().parse_args(argv)
    code_commit = _require_clean_commit(args.source_root.expanduser().resolve())
    audit = build_judge_input_projection(
        args.source_root,
        args.projection_root,
        projection_code_commit=code_commit,
        expected_pair_ids=tuple(args.pair_ids or FROZEN_PAIR_IDS),
        expected_rounds=tuple(args.rounds or (1, 2, 3)),
    )
    print(audit.model_dump_json(indent=2, by_alias=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
