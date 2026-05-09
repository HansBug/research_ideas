"""Prediction Extractor agent —— 把 NL pred_output 解析为 :class:`ArtifactDossier`。

本模块仅是 :func:`tools.structured_extract.extract_artifact_dossier`
的薄包装；``role`` 固定为 ``"prediction"``。

**作用**：

把上游传入的预测制品文本（PlantUML / SysML XML / 等）解析为结构化
:class:`ArtifactDossier`（含 elements / relations / behaviors /
constraints / surface_markers / 等），供后续 traceability /
equivalence / pragmatic_quality / score_composer 多个 agent 复用。

**设计思路**：薄包装层；真正的 parser 逻辑在
:mod:`tools.structured_extract` 与 :mod:`tools.known_format_lift` 中。
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..schemas.dossiers import ArtifactDossier
from ..tools import extract_artifact_dossier


def extract_prediction_dossier(
    text: str | None,
    llm: ChatOpenAI | None,
    notes: list[str],
) -> ArtifactDossier:
    """把预测制品文本解析为 :class:`ArtifactDossier` (role='prediction')。

    :param text: 预测制品文本；``None`` 时返回 stub dossier
    :param llm: LLM client（``None`` 走 deterministic parser-only）
    :param notes: 由调用方提供，用于追加 audit 笔记
    :return: :class:`ArtifactDossier`
    """
    return extract_artifact_dossier("prediction", text, llm, notes)


__all__ = ["extract_prediction_dossier"]
