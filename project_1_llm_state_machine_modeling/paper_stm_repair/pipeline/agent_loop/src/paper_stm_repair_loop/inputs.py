from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .config import PAIRS_JSONL, SELECTED_ROOT
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


def _read_pairs() -> dict[str, dict[str, Any]]:
    return {
        row["pair_id"]: row
        for row in (json.loads(line) for line in PAIRS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip())
    }


def _selected_dir(pair_id: str) -> Path | None:
    for directory in sorted(p for p in SELECTED_ROOT.iterdir() if p.is_dir()):
        meta_path = directory / "source_meta.json"
        if meta_path.exists() and json.loads(meta_path.read_text(encoding="utf-8")).get("pair_id") == pair_id:
            return directory
    return None


def _trace_from_selected(directory: Path, meta: dict[str, Any]) -> dict[str, Any]:
    fcstm_meta = json.loads((directory / "fcstm_meta.json").read_text(encoding="utf-8"))
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
    if pair_id not in pairs:
        raise ValueError(f"unknown pair_id: {pair_id}")
    row = pairs[pair_id]
    selected = _selected_dir(pair_id)
    if selected is None or not (selected / "model.fcstm").exists():
        raise ValueError(f"PAIR_FCSTM_NOT_PREPARED: {pair_id}; prepare A-stage fcstm before Discover")
    fcstm_file = selected / "model.fcstm"
    fcstm = fcstm_file.read_text(encoding="utf-8")
    trace = _trace_from_selected(selected, row)
    expected_sha = trace.get("source_traceability", {}).get("fcstm_sha256")
    actual_sha = sha256_text(fcstm)
    if not expected_sha or expected_sha != actual_sha:
        raise ValueError("PAIR_FCSTM_TRACE_MISMATCH: source trace must bind the selected fcstm")
    if hashlib.sha256(row["nl_text"].encode("utf-8")).hexdigest() != row["nl_sha256"]:
        raise ValueError(f"pair NL hash mismatch: {pair_id}")
    return PreparedCase(
        case_id=selected.name if selected is not None else pair_id,
        pair_id=pair_id,
        nl=row["nl_text"],
        raw_source=row["stm0_text"],
        raw_source_format=row.get("stm_format", "unknown"),
        fcstm=fcstm,
        source_trace=trace,
        metadata={k: v for k, v in row.items() if k != "reference_plantuml_sha256"},
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
