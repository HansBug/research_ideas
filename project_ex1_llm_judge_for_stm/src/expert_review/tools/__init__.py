"""``__init__`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from .artifact_io import artifact_excerpt, content_to_text
from .artifact_probe import build_parser_dossier, merge_text_fragments
from .dossier_merge import merge_artifact_dossiers
from .known_format_lift import (
    artifact_family_guess,
    dedupe_strings,
    format_confidence,
    guess_format,
    inventory_from_text,
    parse_transition_signature,
    summary_from_inventory,
    surface_markers_from_text,
)
from .policy_library import QUALITY_ISSUE_TYPES, VV_ROLE_HINTS, build_review_policy, detect_vv_roles, infer_aggregate_signal
from .structured_extract import extract_artifact_dossier, render_artifact_schema_hint, should_use_llm_extractor
from .validation import evidence_summary_from_dimensions, json_safe_report, status_counts, validate_result_shape

__all__ = [
    "artifact_excerpt",
    "artifact_family_guess",
    "build_parser_dossier",
    "QUALITY_ISSUE_TYPES",
    "VV_ROLE_HINTS",
    "build_review_policy",
    "content_to_text",
    "dedupe_strings",
    "detect_vv_roles",
    "evidence_summary_from_dimensions",
    "extract_artifact_dossier",
    "format_confidence",
    "guess_format",
    "infer_aggregate_signal",
    "inventory_from_text",
    "json_safe_report",
    "merge_artifact_dossiers",
    "merge_text_fragments",
    "parse_transition_signature",
    "render_artifact_schema_hint",
    "should_use_llm_extractor",
    "status_counts",
    "summary_from_inventory",
    "surface_markers_from_text",
    "validate_result_shape",
]