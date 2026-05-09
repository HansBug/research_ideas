"""``structured_extract`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..agents.llm_helpers import invoke_llm_json
from ..prompts.extraction import ARTIFACT_EXTRACTOR_SYSTEM_PROMPT
from ..schemas.dossiers import ArtifactDossier
from .artifact_io import artifact_excerpt
from .artifact_probe import build_parser_dossier
from .dossier_merge import merge_artifact_dossiers


def render_artifact_schema_hint() -> dict[str, Any]:
    """``render_artifact_schema_hint`` 函数。
    :return: 见函数签名与上下文。
    """
    return {
        "artifact_family_guess": "behavior_model",
        "summary": "Short evidence-grounded summary.",
        "major_elements": [
            {
                "element_id": "e1",
                "kind": "state",
                "label": "Idle",
                "text": "Idle state",
                "evidence_text": "short supporting snippet",
            }
        ],
        "major_relations": [
            {
                "relation_id": "r1",
                "kind": "relation",
                "source_label": "Idle",
                "target_label": "Ready",
                "trigger": "login",
                "condition": "authorized",
                "action": "",
                "description": "Idle to Ready when login and authorized.",
                "evidence_text": "short supporting snippet",
            }
        ],
        "behaviors": ["A short behavior statement."],
        "constraints": ["A short constraint statement."],
        "ambiguities": ["A short ambiguity statement if needed."],
        "observability": "high",
        "observability_reason": "Short reason for the observability judgement.",
    }


def should_use_llm_extractor(dossier: ArtifactDossier, text: str | None) -> bool:
    """``should_use_llm_extractor`` 函数。

    :param dossier: 见函数签名与上下文。
    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not text or not text.strip():
        return False
    if dossier.format_guess in {"json_structured_model", "plantuml_like"} and dossier.observability == "high":
        return False
    if dossier.observability == "low":
        return True
    if dossier.format_guess in {"ttool_xml", "xml", "free_text", "summary_text", "json_generic", "json_list"}:
        return True
    return len(dossier.behaviors) < 2 and len((text or "").strip()) >= 200


def extract_artifact_dossier(
    role: str,
    text: str | None,
    llm: ChatOpenAI | None,
    notes: list[str],
) -> ArtifactDossier:
    """``extract_artifact_dossier`` 函数。

    :param role: 见函数签名与上下文。
    :param text: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :param notes: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    parser_dossier = build_parser_dossier(role, text)
    if llm is None or not should_use_llm_extractor(parser_dossier, text):
        return parser_dossier
    llm_payload = invoke_llm_json(
        llm,
        [
            ("system", ARTIFACT_EXTRACTOR_SYSTEM_PROMPT),
            (
                "user",
                "Normalize the following artifact into the schema below.\n\n"
                f"Schema:\n{json.dumps(render_artifact_schema_hint(), ensure_ascii=False, indent=2)}\n\n"
                f"Artifact role: {role}\n"
                f"Observed format guess: {parser_dossier.format_guess}\n"
                f"Observed parser summary: {parser_dossier.summary}\n"
                f"Artifact text:\n{artifact_excerpt(text)}",
            ),
        ],
    )
    if not isinstance(llm_payload, dict):
        notes.append(f"{role} extractor fell back to parser-only dossier because the LLM extractor returned no JSON.")
        return parser_dossier
    notes.append(f"{role} dossier used parser + LLM extraction.")
    return merge_artifact_dossiers(parser_dossier, llm_payload)


__all__ = ["extract_artifact_dossier", "render_artifact_schema_hint", "should_use_llm_extractor"]