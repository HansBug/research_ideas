"""Reference Extractor agent —— 把 NL ref_output 解析为 :class:`ArtifactDossier`。

与 :mod:`prediction_extractor` 对称的薄包装；``role`` 固定为
``"reference"``。``text`` 为 ``None`` 时返回 stub dossier，让 regime
后续标 ``has_reference=False``，pipeline 仍可继续。

**设计思路**：见 :mod:`prediction_extractor` 同位置——本模块只是
为了 stage label 与 dossier role 标识对称而存在的薄包装。
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..schemas.dossiers import ArtifactDossier
from ..tools import extract_artifact_dossier


def extract_reference_dossier(
    text: str | None,
    llm: ChatOpenAI | None,
    notes: list[str],
) -> ArtifactDossier:
    """把参考制品文本解析为 :class:`ArtifactDossier` (role='reference')。

    :param text: 参考制品文本；``None`` 时返回 stub dossier
    :param llm: LLM client
    :param notes: 由调用方提供，用于追加 audit 笔记
    :return: :class:`ArtifactDossier`
    """
    return extract_artifact_dossier("reference", text, llm, notes)


__all__ = ["extract_reference_dossier"]
