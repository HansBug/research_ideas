from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Predicate(BaseModel):
    """One frozen registry predicate and its source/soundness metadata."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    id: str = Field(min_length=1, description="Frozen public predicate identifier.")
    name: str = Field(min_length=1, description="Stable predicate name from the frozen registry.")
    family: str = Field(min_length=1, description="Frozen predicate family identifier.")
    semantics: str = Field(min_length=1, description="Exact semantic statement registered for this predicate.")
    inputs: tuple[str, ...] = Field(min_length=1, description="Minimal named inputs required to compile this predicate.")
    sources: tuple[str, ...] = Field(min_length=1, description="Source identifiers supporting the registered predicate claim.")
    source_types: tuple[str, ...] = Field(min_length=1, description="Source classes supporting the registered predicate claim.")
    soundness_fragment: str = Field(min_length=1, description="Soundness boundary under which the predicate result is valid.")


class PredicateRegistry(BaseModel):
    """Validated frozen registry snapshot used by compilation and audit."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, arbitrary_types_allowed=True)

    version: str = Field(min_length=1, description="Frozen registry version used by every compiled plan.")
    registry_hash: str = Field(min_length=1, description="SHA-256 hash of the machine-readable registry source.")
    predicates: dict[str, Predicate] = Field(description="Predicate lookup keyed by the frozen public identifier.")
    families: dict[str, tuple[str, ...]] = Field(description="Family-to-predicate ID mapping validated against the registry shape.")
    raw: dict[str, Any] = Field(description="Validated machine-readable registry payload retained for audit.")
    source_catalog_path: Path | None = Field(default=None, description="Resolved scholarly provenance catalog associated with the frozen registry; it is never a runtime W or execution gate.")

    def get(self, predicate_id: str | None) -> Predicate | None:
        return self.predicates.get(predicate_id) if predicate_id else None

    def require(self, predicate_id: str) -> Predicate:
        try:
            return self.predicates[predicate_id]
        except KeyError as exc:
            raise KeyError(f"unknown frozen predicate: {predicate_id}") from exc
