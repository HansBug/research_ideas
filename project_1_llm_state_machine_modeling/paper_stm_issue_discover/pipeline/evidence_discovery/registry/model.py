from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceAdmission(BaseModel):
    """One catalog-backed, shape-restricted W2 source admission.

    Predicate-wide catalog status remains the default source gate. An admission
    records the exceptional, independently reviewed proposition that can be
    used only after compiler-side typed-shape validation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    id: str = Field(min_length=1, description="Stable catalog identifier for this restricted source admission.")
    predicate_id: str = Field(min_length=1, description="Frozen predicate ID to which this admission is restricted.")
    kind: Literal["s3_initial_outgoing_without_trigger"] = Field(description="Compiler-recognized restricted proposition shape; unsupported kinds cannot open a W2 gate.")
    status: Literal["partial_pass"] = Field(description="Reviewed admission status; this does not change the predicate-wide source audit status.")
    source_ids: tuple[str, ...] = Field(min_length=1, description="Catalog source IDs that directly support this limited proposition.")
    citations: tuple[str, ...] = Field(min_length=1, description="Stable local citation locations retained in every admitted plan and receipt.")
    proposition: str = Field(min_length=1, description="Precisely scoped proposition supported by the cited source.")
    boundary: str = Field(min_length=1, description="Explicit semantic boundary preventing this admission from widening to neighboring checks.")

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
    source_catalog_path: Path | None = Field(default=None, description="Resolved source catalog path used for source gating, if available.")
    source_audit: dict[str, dict[str, Any]] | None = Field(default=None, description="Per-predicate source audit status used by the W2 gate.")
    source_admissions: dict[str, tuple[SourceAdmission, ...]] = Field(default_factory=dict, description="Catalog-backed restricted source admissions keyed by frozen predicate ID; these never replace the predicate-wide audit status.")

    def get(self, predicate_id: str | None) -> Predicate | None:
        return self.predicates.get(predicate_id) if predicate_id else None

    def require(self, predicate_id: str) -> Predicate:
        try:
            return self.predicates[predicate_id]
        except KeyError as exc:
            raise KeyError(f"unknown frozen predicate: {predicate_id}") from exc
