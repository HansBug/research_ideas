from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..schemas.dossiers import ArtifactDossier
from ..tools import extract_artifact_dossier


def extract_prediction_dossier(
    text: str | None,
    llm: ChatOpenAI | None,
    notes: list[str],
) -> ArtifactDossier:
    return extract_artifact_dossier("prediction", text, llm, notes)


__all__ = ["extract_prediction_dossier"]
