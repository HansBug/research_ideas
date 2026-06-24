from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import ConversionResult, Loss
from .scxml import ScxmlOptions, convert_scxml


def _find_after_tokens(line: str) -> list[str]:
    """Find simple Umple `after(...)` timing tokens without parsing state structure."""
    tokens: list[str] = []
    pos = 0
    lower = line.lower()
    while True:
        start = lower.find("after", pos)
        if start < 0:
            return tokens
        cursor = start + len("after")
        while cursor < len(line) and line[cursor].isspace():
            cursor += 1
        if cursor >= len(line) or line[cursor] != "(":
            pos = cursor
            continue
        end = line.find(")", cursor + 1)
        if end < 0:
            pos = cursor + 1
            continue
        tokens.append(line[start : end + 1])
        pos = end + 1


def _audit_umple_timing(path: Path, result: ConversionResult) -> None:
    text = path.read_text(encoding="utf-8")
    matches = [(i, token) for i, line in enumerate(text.splitlines(), start=1) for token in _find_after_tokens(line)]
    if not matches:
        return
    result.status = "partial"
    result.timing_level = "qualitative"
    result.blocking_reason = "Umple official SCXML rewrites after(...) timer-like transitions; R3 preserves this as targeted timing loss while canonical structure remains SCXML-derived."
    for lineno, token in matches:
        loss_id = f"{result.example_id}:umple:timing_after:{lineno}"
        result.losses.append(
            Loss(
                loss_id=loss_id,
                example_id=result.example_id,
                source_ref=f"{path.name}:{lineno}:{token}",
                canonical_ref=result.metadata.get("structured_export_path"),
                loss_type="timing",
                severity="medium",
                rationale="Raw Umple after(...) timing syntax is not preserved verbatim by official SCXML export; recorded as qualitative timing loss, not as timed-automata clock semantics.",
                needs_manual_review=True,
            )
        )
        result.diagnostics.append(
            {
                "code": "R3.UMPLE.TIMING_RAW_AUDIT",
                "severity": "medium",
                "raw_ref": f"{path.name}:{lineno}",
                "loss_ref": loss_id,
                "message": f"Targeted raw Umple audit found timer-like syntax {token}; canonical structure remains official SCXML-derived.",
            }
        )
    result.metadata["targeted_audit_used"] = True
    result.metadata["targeted_audit_scope"] = "raw Umple timing token audit only; states/transitions remain official SCXML-derived"
    result.metadata["source_text_used_for_canonical"] = False


def convert_umple(
    path: Path,
    *,
    example_id: str,
    seed_id: str,
    source_format: str = "umple",
    preflight: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> ConversionResult:
    structured_path = (preflight or {}).get("structured_export_path")
    syntax_status = (preflight or {}).get("syntax_status")
    structured_status = (preflight or {}).get("structured_export_status")
    if syntax_status == "ok" and structured_status == "scxml_export_ok" and structured_path:
        scxml_path = (repo_root / structured_path) if repo_root and not Path(structured_path).is_absolute() else Path(structured_path)
        result = convert_scxml(
            scxml_path,
            example_id=example_id,
            seed_id=seed_id,
            options=ScxmlOptions(
                adapter="umple",
                source_format=source_format,
                conversion_source="official_scxml",
                canonical_extraction_method="Umple -g Scxml export parsed by xml.etree.ElementTree",
                status_on_success="converted",
                fallback_used=False,
                fallback_scope=None,
                timing_level="none",
                source_language="Umple textual state machine",
            ),
            structured_export_relpath=structured_path,
            structured_export_sha256=(preflight or {}).get("structured_export_sha256"),
        )
        result.metadata["source_text_path"] = path.name
        result.metadata["source_text_used_for_canonical"] = False
        _audit_umple_timing(path, result)
        return result

    reason = (preflight or {}).get("fallback_reason") or "Umple official structured export was unavailable; source-text parser is not allowed as canonical conversion source."
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=source_format,
        adapter="umple",
        status="blocked",
        canonical_model_name=example_id,
        blocking_reason=reason,
    )
    result.metadata.update(
        {
            "conversion_source": "no_canonical_conversion",
            "canonical_extraction_method": "none; official Umple structured export unavailable or not trusted",
            "structured_export_path": structured_path,
            "structured_export_sha256": (preflight or {}).get("structured_export_sha256"),
            "fallback_used": False,
            "fallback_scope": None,
            "source_text_used_for_canonical": False,
        }
    )
    result.diagnostics.append(
        {
            "code": "R3.UMPLE.NO_OFFICIAL_STRUCTURED_CANONICAL",
            "severity": "blocking",
            "syntax_status": syntax_status,
            "structured_export_status": structured_status,
            "message": reason,
        }
    )
    result.losses.append(
        Loss(
            loss_id=f"{example_id}:umple:no_official_structured_canonical",
            example_id=example_id,
            source_ref=path.name,
            canonical_ref=None,
            loss_type="tooling",
            severity="blocking",
            rationale=reason,
            needs_manual_review=True,
        )
    )
    return result
