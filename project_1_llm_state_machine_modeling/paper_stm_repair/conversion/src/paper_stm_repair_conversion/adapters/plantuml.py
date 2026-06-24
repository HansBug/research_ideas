from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import ConversionResult, Loss
from .scxml import ScxmlOptions, convert_scxml


def convert_plantuml(
    path: Path,
    *,
    example_id: str,
    seed_id: str,
    source_format: str = "plantuml",
    preflight: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> ConversionResult:
    structured_path = (preflight or {}).get("structured_export_path")
    syntax_status = (preflight or {}).get("syntax_status")
    structured_status = (preflight or {}).get("structured_export_status")
    if syntax_status == "ok" and structured_status in {"scxml_export_ok", "scxml_export_reused_tool_missing"} and structured_path:
        scxml_path = (repo_root / structured_path) if repo_root and not Path(structured_path).is_absolute() else Path(structured_path)
        result = convert_scxml(
            scxml_path,
            example_id=example_id,
            seed_id=seed_id,
            options=ScxmlOptions(
                adapter="plantuml",
                source_format=source_format,
                conversion_source="official_scxml",
                canonical_extraction_method="PlantUML -tscxml export parsed by xml.etree.ElementTree",
                status_on_success="converted",
                fallback_used=False,
                fallback_scope=None,
                timing_level="none",
                source_language="PlantUML state diagram",
            ),
            structured_export_relpath=structured_path,
            structured_export_sha256=(preflight or {}).get("structured_export_sha256"),
        )
        result.metadata["source_text_path"] = path.name
        result.metadata["source_text_used_for_canonical"] = False
        return result

    reason = (preflight or {}).get("fallback_reason") or "PlantUML official SCXML export was unavailable; regex/text parser is not allowed as canonical conversion source."
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=source_format,
        adapter="plantuml",
        status="partial" if syntax_status == "failed" else "blocked",
        canonical_model_name=example_id,
        blocking_reason=reason,
    )
    result.metadata.update(
        {
            "conversion_source": "no_canonical_conversion",
            "canonical_extraction_method": "none; official SCXML unavailable or not trusted",
            "structured_export_path": structured_path,
            "structured_export_sha256": (preflight or {}).get("structured_export_sha256"),
            "fallback_used": True,
            "fallback_scope": "debug/audit probe only; not used to populate canonical states/transitions",
            "source_text_used_for_canonical": False,
        }
    )
    result.diagnostics.append(
        {
            "code": "R3.PUML.NO_OFFICIAL_SCXML_CANONICAL",
            "severity": "high",
            "syntax_status": syntax_status,
            "structured_export_status": structured_status,
            "message": reason,
        }
    )
    result.losses.append(
        Loss(
            loss_id=f"{example_id}:plantuml:no_official_scxml_canonical",
            example_id=example_id,
            source_ref=path.name,
            canonical_ref=None,
            loss_type="tooling",
            severity="high" if syntax_status == "failed" else "blocking",
            rationale=reason,
            needs_manual_review=True,
        )
    )
    return result
