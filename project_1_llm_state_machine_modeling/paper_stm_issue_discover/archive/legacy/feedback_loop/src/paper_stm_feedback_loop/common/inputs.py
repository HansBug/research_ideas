from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .source_trace import SourceTraceBundle, load_source_trace
from .telemetry import sha256_text


@dataclass(frozen=True)
class TextArtifact:
    path: Path
    text: str
    sha256: str


@dataclass(frozen=True)
class JsonArtifact:
    path: Path
    data: dict[str, Any]
    sha256: str


@dataclass(frozen=True)
class FeedbackLoopInputs:
    pair_id: str
    nl: TextArtifact
    fcstm: TextArtifact
    source_trace: SourceTraceBundle
    working_contract: JsonArtifact | None = None
    report_root: Path | None = None
    pair_dir: Path | None = None

    @property
    def nl_text(self) -> str:
        return self.nl.text

    @property
    def fcstm_text(self) -> str:
        return self.fcstm.text

    def summary(self) -> dict[str, Any]:
        return {
            "pair_id": self.pair_id,
            "paths": {
                "nl": str(self.nl.path),
                "fcstm": str(self.fcstm.path),
                "source_trace": str(self.source_trace.path),
                "working_contract": (
                    str(self.working_contract.path)
                    if self.working_contract is not None
                    else None
                ),
            },
            "sha256": {
                "nl": self.nl.sha256,
                "fcstm": self.fcstm.sha256,
                "source_trace": self.source_trace.sha256,
                "working_contract": (
                    self.working_contract.sha256
                    if self.working_contract is not None
                    else None
                ),
            },
            "source_trace_entries": self.source_trace.entry_count,
            "working_contract_schema_version": (
                self.working_contract.data.get("schema_version")
                if self.working_contract is not None
                else None
            ),
        }


def clean_path(path: str | Path, *, must_exist: bool = True, base_dir: str | Path | None = None) -> Path:
    raw = str(path)
    if not raw or "\x00" in raw:
        raise ValueError("path must be non-empty and must not contain NUL bytes")
    resolved = Path(path).expanduser().resolve()
    if base_dir is not None:
        base = Path(base_dir).expanduser().resolve()
        try:
            resolved.relative_to(base)
        except ValueError as exc:
            raise ValueError(f"path escapes base directory: {resolved} not under {base}") from exc
    if must_exist and not resolved.exists():
        raise FileNotFoundError(resolved)
    return resolved


def _read_text_artifact(path: Path) -> TextArtifact:
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    return TextArtifact(path=path, text=text, sha256=sha256_text(text))


def _read_json_artifact(path: Path) -> JsonArtifact:
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return JsonArtifact(path=path, data=data, sha256=sha256_text(text))


def infer_report_root_from_pair_dir(pair_dir: str | Path) -> Path:
    pair = clean_path(pair_dir)
    if not pair.is_dir():
        raise NotADirectoryError(pair)
    if pair.parent.name != "pairs":
        raise ValueError(f"pair_dir must be under a pairs/ directory: {pair}")
    return pair.parent.parent.resolve()


def infer_pair_id(pair_dir: str | Path, report_root: str | Path | None = None) -> str:
    pair = clean_path(pair_dir)
    case = pair.name
    root = clean_path(report_root) if report_root is not None else infer_report_root_from_pair_dir(pair)
    case_report = root / "case_reports" / f"llms_emp_feedback_final_{case}.json"
    if case_report.is_file():
        data = json.loads(case_report.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("pair_id"), str):
            return data["pair_id"]
    return f"llms_emp_feedback_final_{case}" if case.isdigit() else case


def load_feedback_loop_inputs(
    *,
    pair_dir: str | Path | None = None,
    report_root: str | Path | None = None,
    pair_id: str | None = None,
    nl_path: str | Path | None = None,
    fcstm_path: str | Path | None = None,
    source_trace_path: str | Path | None = None,
    working_contract_path: str | Path | None = None,
) -> FeedbackLoopInputs:
    """Load NL, FCSTM, source trace, and working contract from pair or files.

    Pair mode expects the representation report layout:
    ``reports/.../pairs/0000/{nl.txt,fcstm.fcstm}`` plus sibling
    ``source_traces/<pair_id>.json`` and ``working_contracts/<pair_id>.json``.
    Custom-file mode may pass all four explicit paths.
    """

    resolved_pair_dir: Path | None = None
    resolved_report_root: Path | None = clean_path(report_root) if report_root is not None else None
    if pair_dir is not None:
        resolved_pair_dir = clean_path(pair_dir)
        if not resolved_pair_dir.is_dir():
            raise NotADirectoryError(resolved_pair_dir)
        if resolved_report_root is None:
            resolved_report_root = infer_report_root_from_pair_dir(resolved_pair_dir)
        pair_id = pair_id or infer_pair_id(resolved_pair_dir, resolved_report_root)
        nl_path = nl_path or resolved_pair_dir / "nl.txt"
        fcstm_path = fcstm_path or resolved_pair_dir / "fcstm.fcstm"
        source_trace_path = source_trace_path or resolved_report_root / "source_traces" / f"{pair_id}.json"
        working_contract_path = working_contract_path or resolved_report_root / "working_contracts" / f"{pair_id}.json"
    missing = [
        name
        for name, value in {
            "pair_id": pair_id,
            "nl_path": nl_path,
            "fcstm_path": fcstm_path,
            "source_trace_path": source_trace_path,
        }.items()
        if value is None
    ]
    if missing:
        raise ValueError(f"missing required input(s): {', '.join(missing)}")
    nl = _read_text_artifact(clean_path(nl_path))
    fcstm = _read_text_artifact(clean_path(fcstm_path))
    source_trace = load_source_trace(clean_path(source_trace_path))
    working_contract = (
        _read_json_artifact(clean_path(working_contract_path))
        if working_contract_path is not None
        else None
    )
    return FeedbackLoopInputs(
        pair_id=str(pair_id),
        nl=nl,
        fcstm=fcstm,
        source_trace=source_trace,
        working_contract=working_contract,
        report_root=resolved_report_root,
        pair_dir=resolved_pair_dir,
    )
