from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .config import PAIRS_JSONL, REPO_ROOT, SELECTED_ROOT
from .pyfcstm_adapter import sha256_text
from .records import RecordStore, sha256_file


@dataclass(frozen=True)
class PreparedCase:
    case_id: str
    pair_id: str | None
    nl: str
    raw_source: str
    raw_source_format: str
    fcstm: str
    source_trace: dict[str, Any]
    metadata: dict[str, Any]
    input_mode: str

    @property
    def fcstm_sha256(self) -> str:
        return sha256_text(self.fcstm)


def _hash_paths(paths: list[str]) -> str:
    payload = json.dumps(
        paths,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8", "surrogateescape")
    return hashlib.sha256(payload).hexdigest()


def _hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8", "surrogateescape")
    return _hash_bytes(payload)


def _decode_git_path(raw_path: bytes) -> str:
    return raw_path.decode("utf-8", "surrogateescape")


def _untracked_content_manifest(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    for relative_path in paths:
        path = repo_root / relative_path
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            file_type = "symlink"
            git_mode = "120000"
            symlink_target = os.readlink(path)
            content = os.fsencode(symlink_target)
        elif stat.S_ISREG(metadata.st_mode):
            file_type = "regular_file"
            git_mode = "100755" if metadata.st_mode & 0o111 else "100644"
            symlink_target = None
            content = path.read_bytes()
        else:
            raise ValueError(
                f"unsupported untracked file type for provenance: {relative_path}"
            )
        manifest.append(
            {
                "path": relative_path,
                "file_type": file_type,
                "git_mode": git_mode,
                "lstat_mode_octal": format(stat.S_IMODE(metadata.st_mode), "04o"),
                "size_bytes": metadata.st_size,
                "content_sha256": _hash_bytes(content),
                "symlink_target": symlink_target,
            }
        )
    return manifest


def _code_provenance() -> dict[str, Any]:
    """Capture repository code identity while excluding only ``runs/**`` outputs."""

    excluded_pathspecs = ["runs/**"]
    unavailable = {
        "status": "unavailable",
        "git_commit": None,
        "git_branch": None,
        "tracked_worktree_dirty": None,
        "tracked_dirty_paths": [],
        "tracked_dirty_count": None,
        "tracked_dirty_paths_sha256": None,
        "canonical_git_diff_binary_head_sha256": None,
        "canonical_git_diff_binary_head_empty": None,
        "reproducible_tracked_head": None,
        "code_state_reproducible": None,
        "reproducible_code_head": None,
        "non_run_untracked_paths": [],
        "non_run_untracked_count": None,
        "non_run_untracked_paths_sha256": None,
        "non_run_untracked_content_manifest": [],
        "non_run_untracked_content_manifest_sha256": None,
        "non_run_untracked_content_complete": None,
        "untracked_run_outputs_excluded": True,
        "excluded_pathspecs": excluded_pathspecs,
    }
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        branch_result = subprocess.run(
            ["git", "symbolic-ref", "--short", "-q", "HEAD"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        status_result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain=v2",
                "-z",
                "--untracked-files=all",
                "--",
                ".",
                ":(exclude)runs/**",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        tracked_worktree_dirty = False
        untracked_paths: list[str] = []
        for record in status_result.stdout.split(b"\0"):
            if not record:
                continue
            if record.startswith((b"1 ", b"2 ", b"u ")):
                tracked_worktree_dirty = True
            elif record.startswith(b"? "):
                untracked_paths.append(_decode_git_path(record[2:]))
        tracked_dirty_result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "-z",
                "HEAD",
                "--",
                ".",
                ":(exclude)runs/**",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        canonical_diff_result = subprocess.run(
            [
                "git",
                "diff",
                "--binary",
                "HEAD",
                "--",
                ".",
                ":(exclude)runs/**",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        untracked_paths = sorted(untracked_paths)
        tracked_dirty_paths = sorted(
            _decode_git_path(path)
            for path in tracked_dirty_result.stdout.split(b"\0")
            if path
        )
        canonical_diff = canonical_diff_result.stdout
        tracked_worktree_dirty = bool(tracked_dirty_paths)
        untracked_manifest = _untracked_content_manifest(REPO_ROOT, untracked_paths)
        code_state_reproducible = not tracked_worktree_dirty and not untracked_paths
        return {
            "status": "completed",
            "git_commit": commit,
            "git_branch": branch_result.stdout.strip() or None,
            "tracked_worktree_dirty": tracked_worktree_dirty,
            "tracked_dirty_paths": tracked_dirty_paths,
            "tracked_dirty_count": len(tracked_dirty_paths),
            "tracked_dirty_paths_sha256": _hash_paths(tracked_dirty_paths),
            "canonical_git_diff_binary_head_sha256": _hash_bytes(canonical_diff),
            "canonical_git_diff_binary_head_empty": canonical_diff == b"",
            "reproducible_tracked_head": None if tracked_worktree_dirty else commit,
            "code_state_reproducible": code_state_reproducible,
            "reproducible_code_head": commit if code_state_reproducible else None,
            "non_run_untracked_paths": untracked_paths,
            "non_run_untracked_count": len(untracked_paths),
            "non_run_untracked_paths_sha256": _hash_paths(untracked_paths),
            "non_run_untracked_content_manifest": untracked_manifest,
            "non_run_untracked_content_manifest_sha256": _hash_json(
                untracked_manifest
            ),
            "non_run_untracked_content_complete": True,
            "untracked_run_outputs_excluded": True,
            "excluded_pathspecs": excluded_pathspecs,
        }
    except Exception as exc:
        result = dict(unavailable)
        result["reason"] = type(exc).__name__
        return result


def _read_pairs() -> dict[str, dict[str, Any]]:
    return {
        row["pair_id"]: row
        for row in (json.loads(line) for line in PAIRS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip())
    }


def _selected_dir(pair_id: str) -> Path | None:
    matches: list[Path] = []
    for directory in sorted(p for p in SELECTED_ROOT.iterdir() if p.is_dir()):
        meta_path = directory / "source_meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if pair_id in {meta.get("pair_id"), meta.get("discover_pair_id")}:
                matches.append(directory)
    if len(matches) > 1:
        raise ValueError(
            "PAIR_SELECTED_DIRECTORY_AMBIGUOUS: "
            f"{pair_id} resolves to {[path.name for path in matches]}"
        )
    return matches[0] if matches else None


def _trace_from_selected(directory: Path, meta: dict[str, Any]) -> dict[str, Any]:
    source_meta = json.loads(
        (directory / "source_meta.json").read_text(encoding="utf-8")
    )
    fcstm_meta = json.loads((directory / "fcstm_meta.json").read_text(encoding="utf-8"))
    if fcstm_meta.get("discover_source_policy") == "fcstm_identity":
        return {
            "schema_version": "source_trace_base.v1",
            "trace_scope": "manual_conversion_safe_smoke",
            "relation_policy": "exact_identity",
            "entries": [],
            "source_traceability": {
                "source_meta_path": str(directory / "source_meta.json"),
                "fcstm_meta_path": str(directory / "fcstm_meta.json"),
                "source_stm0_sha256": fcstm_meta.get("selected_fcstm_sha256"),
                "fcstm_sha256": fcstm_meta.get("selected_fcstm_sha256"),
                "original_source_stm0_sha256": (
                    source_meta.get("source_stm0_sha256")
                    or source_meta.get("stm0_sha256")
                    or meta.get("stm0_sha256")
                ),
                "closure_claim_allowed": False,
                "attribution": "manual_canonicalization_identity_smoke",
                "academic_eligible": False,
            },
            "notes": (
                "The manually adjudicated FCSTM is frozen as both source and intermediate input "
                "for Discover engineering smoke. The original PlantUML remains in the selected "
                "example directory for provenance but is not exposed as the run source."
            ),
        }
    return {
        "schema_version": "source_trace_base.v1",
        "trace_scope": "pilot_candidate",
        "relation_policy": "evidence_only",
        "entries": [],
        "source_traceability": {
            "source_meta_path": str(directory / "source_meta.json"),
            "fcstm_meta_path": str(directory / "fcstm_meta.json"),
            "canonical_output_path": fcstm_meta.get("canonical_output_path"),
            "source_stm0_sha256": meta.get("stm0_sha256"),
            "fcstm_sha256": fcstm_meta.get("selected_fcstm_sha256"),
            "closure_claim_allowed": False,
            "attribution": "representation_lowering_not_repair",
        },
        "notes": "Selected smoke snapshot exposes bridge provenance; element-level source closure remains a later C-stage responsibility.",
    }


def load_pair(pair_id: str, *, fcstm_file: Path | None = None, source_trace_file: Path | None = None) -> PreparedCase:
    if fcstm_file is not None or source_trace_file is not None:
        raise ValueError("PAIR_INPUT_OVERRIDE_FORBIDDEN: use custom mode for non-canonical model or trace inputs")
    pairs = _read_pairs()
    selected = _selected_dir(pair_id)
    selected_source_meta = (
        json.loads((selected / "source_meta.json").read_text(encoding="utf-8"))
        if selected is not None
        else {}
    )
    source_pair_id = str(
        selected_source_meta.get("source_pair_id")
        or selected_source_meta.get("pair_id")
        or pair_id
    )
    if source_pair_id not in pairs:
        raise ValueError(f"unknown pair_id: {pair_id}")
    row = pairs[source_pair_id]
    if selected is None or not (selected / "model.fcstm").exists():
        raise ValueError(f"PAIR_FCSTM_NOT_PREPARED: {pair_id}; prepare A-stage fcstm before Discover")
    fcstm_file = selected / "model.fcstm"
    fcstm = fcstm_file.read_text(encoding="utf-8")
    fcstm_meta = json.loads((selected / "fcstm_meta.json").read_text(encoding="utf-8"))
    discover_source_policy = str(fcstm_meta.get("discover_source_policy") or "raw_source")
    if discover_source_policy not in {"raw_source", "fcstm_identity"}:
        raise ValueError(f"PAIR_DISCOVER_SOURCE_POLICY_UNSUPPORTED: {discover_source_policy}")
    trace = _trace_from_selected(selected, row)
    expected_sha = trace.get("source_traceability", {}).get("fcstm_sha256")
    actual_sha = sha256_text(fcstm)
    if not expected_sha or expected_sha != actual_sha:
        raise ValueError("PAIR_FCSTM_TRACE_MISMATCH: source trace must bind the selected fcstm")
    if hashlib.sha256(row["nl_text"].encode("utf-8")).hexdigest() != row["nl_sha256"]:
        raise ValueError(f"pair NL hash mismatch: {pair_id}")
    metadata = {k: v for k, v in row.items() if k != "reference_plantuml_sha256"}
    metadata.update(
        {
            "discover_pair_id": pair_id,
            "source_pair_id": source_pair_id,
            "selected_example_dir": str(selected),
            "discover_source_policy": discover_source_policy,
            "academic_eligible": fcstm_meta.get("academic_eligible"),
            "academic_ineligibility_reason": fcstm_meta.get("academic_ineligibility_reason"),
        }
    )
    return PreparedCase(
        case_id=selected.name if selected is not None else pair_id,
        pair_id=pair_id,
        nl=row["nl_text"],
        raw_source=fcstm if discover_source_policy == "fcstm_identity" else row["stm0_text"],
        raw_source_format=(
            "fcstm-identity"
            if discover_source_policy == "fcstm_identity"
            else row.get("stm_format", "unknown")
        ),
        fcstm=fcstm,
        source_trace=trace,
        metadata=metadata,
        input_mode="pair",
    )


def load_custom(case_id: str, nl_file: Path, fcstm_file: Path, *, raw_source_file: Path | None = None, source_trace_file: Path | None = None) -> PreparedCase:
    if (raw_source_file is None) != (source_trace_file is None):
        raise ValueError("--raw-source-file and --source-trace-file must be supplied together")
    fcstm = fcstm_file.read_text(encoding="utf-8")
    if raw_source_file is None:
        raw_source, source_format, trace = fcstm, "fcstm-identity", {"schema_version": "source_trace_base.v1", "trace_scope": "pilot_candidate", "relation_policy": "exact_identity", "entries": [], "notes": "Custom fcstm is used as both source and intermediate model."}
    else:
        raw_source, source_format = raw_source_file.read_text(encoding="utf-8"), raw_source_file.suffix.lstrip(".") or "unknown"
        trace = json.loads(source_trace_file.read_text(encoding="utf-8"))
        traceability = trace.get("source_traceability") or {}
        expected_fcstm_sha256 = traceability.get("fcstm_sha256")
        expected_source_sha256 = traceability.get("source_stm0_sha256")
        if expected_fcstm_sha256 != sha256_text(fcstm):
            raise ValueError("CUSTOM_FCSTM_TRACE_MISMATCH: source trace must bind the supplied fcstm")
        if expected_source_sha256 != sha256_text(raw_source):
            raise ValueError("CUSTOM_SOURCE_TRACE_MISMATCH: source trace must bind the supplied raw source")
    return PreparedCase(
        case_id=case_id,
        pair_id=None,
        nl=nl_file.read_text(encoding="utf-8"),
        raw_source=raw_source,
        raw_source_format=source_format,
        fcstm=fcstm,
        source_trace=trace,
        metadata={"nl_path": str(nl_file), "fcstm_path": str(fcstm_file)},
        input_mode="custom",
    )


def prepare_run_dir(
    run_dir: Path,
    case: PreparedCase,
    *,
    profile: str,
    content_language: str,
    renderer: str,
    formal_profile: bool = True,
    replay_file: Path | None = None,
    agent_limits: Mapping[str, int | float] | None = None,
    reviewer_limits: Mapping[str, int | float] | None = None,
    fbmcq_limits: Mapping[str, int | float] | None = None,
) -> None:
    """Materialize the immutable Stage API input boundary for one new run."""

    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"run directory is not empty: {run_dir}")
    inputs = run_dir / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    files = {
        "nl": inputs / "nl.txt",
        "raw_source": inputs / "raw_stm_0.txt",
        "model": inputs / "STM_0.fcstm",
        "source_trace": inputs / "source_trace_base.json",
        "case_metadata": inputs / "case_metadata.json",
    }
    files["nl"].write_text(case.nl, encoding="utf-8")
    files["raw_source"].write_text(case.raw_source, encoding="utf-8")
    files["model"].write_text(case.fcstm, encoding="utf-8")
    files["source_trace"].write_text(json.dumps(case.source_trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files["case_metadata"].write_text(json.dumps(case.metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    limits = dict(agent_limits or {})
    allowed_limits = {"model_calls", "tool_calls", "turns", "seconds"}
    if set(limits) - allowed_limits:
        raise ValueError(f"unknown Agent limit keys: {sorted(set(limits) - allowed_limits)}")
    if any(not isinstance(value, (int, float)) or value <= 0 for value in limits.values()):
        raise ValueError("Agent limits must be positive numbers")
    review_limits = dict(reviewer_limits or {})
    if set(review_limits) - allowed_limits:
        raise ValueError(
            f"unknown reviewer limit keys: {sorted(set(review_limits) - allowed_limits)}"
        )
    if any(
        not isinstance(value, (int, float)) or value <= 0
        for value in review_limits.values()
    ):
        raise ValueError("reviewer limits must be positive numbers")
    formal_limits = dict(fbmcq_limits or {})
    allowed_formal_limits = {
        "process_wall_seconds",
        "solver_timeout_ms",
        "max_bound",
    }
    if set(formal_limits) - allowed_formal_limits:
        raise ValueError(
            "unknown FBMCQ limit keys: "
            f"{sorted(set(formal_limits) - allowed_formal_limits)}"
        )
    if any(
        not isinstance(value, (int, float)) or value <= 0
        for value in formal_limits.values()
    ):
        raise ValueError("FBMCQ limits must be positive numbers")
    manifest = {
        "schema_version": "paper1.discover.manifest.v1",
        "run_id": run_dir.name,
        "stage": "B-discover",
        "case_id": case.case_id,
        "pair_id": case.pair_id,
        "input_mode": case.input_mode,
        "raw_source_format": case.raw_source_format,
        "profile": profile,
        "content_language": content_language,
        "renderer": renderer,
        "formal_profile": formal_profile,
        "agent_limits": limits,
        "reviewer_limits": review_limits,
        "fbmcq_limits": formal_limits,
        "code_provenance": _code_provenance(),
        "main_result_eligible": False,
        "reference_assets_visible": False,
        "input_files": {name: str(path.relative_to(run_dir)) for name, path in files.items()},
        "input_sha256": {name: sha256_file(path) for name, path in files.items()},
    }
    if replay_file is not None:
        manifest["test_replay_file"] = str(replay_file.resolve())
    RecordStore(run_dir).write_immutable_json("manifest.json", manifest)


def load_run_case(run_dir: Path) -> tuple[PreparedCase, dict[str, Any]]:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError("run manifest is missing or not a regular file")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "paper1.discover.manifest.v1" or manifest.get("stage") != "B-discover":
        raise ValueError("run manifest schema/stage mismatch")
    required_roles = {"nl", "raw_source", "model", "source_trace", "case_metadata"}
    if set(manifest.get("input_files", {})) != required_roles or set(manifest.get("input_sha256", {})) != required_roles:
        raise ValueError("run manifest input roles mismatch")
    run_root = run_dir.resolve()
    paths: dict[str, Path] = {}
    for name, relative in manifest["input_files"].items():
        relative_path = Path(relative)
        if relative_path.is_absolute():
            raise ValueError(f"run input path must be relative: {name}")
        path = (run_root / relative_path).resolve()
        try:
            path.relative_to(run_root)
        except ValueError as exc:
            raise ValueError(f"run input path escapes run root: {name}") from exc
        paths[name] = path
    for role, path in paths.items():
        if not path.is_file() or path.is_symlink() or sha256_file(path) != manifest["input_sha256"][role]:
            raise ValueError(f"run input is missing, linked, or stale: {role}")
    case = PreparedCase(
        case_id=manifest["case_id"],
        pair_id=manifest.get("pair_id"),
        nl=paths["nl"].read_text(encoding="utf-8"),
        raw_source=paths["raw_source"].read_text(encoding="utf-8"),
        raw_source_format=manifest["raw_source_format"],
        fcstm=paths["model"].read_text(encoding="utf-8"),
        source_trace=json.loads(paths["source_trace"].read_text(encoding="utf-8")),
        metadata=json.loads(paths["case_metadata"].read_text(encoding="utf-8")),
        input_mode=manifest["input_mode"],
    )
    return case, manifest
