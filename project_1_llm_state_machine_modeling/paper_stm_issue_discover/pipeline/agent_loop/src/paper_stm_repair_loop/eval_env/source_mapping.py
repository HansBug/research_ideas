from __future__ import annotations

import copy
from typing import Any

from .exceptions import UnsupportedEvidence
from .views import FrozenView


MAPPING_FIELDS = frozenset({"source_ref", "model_ref", "relation_policy", "confidence", "producer", "raw"})


class SourceMappingAPI:
    """Read-only source-to-model mapping facade for direct eval assertions.

    Parameters: ``mappings`` is a controller-frozen list of input bridge/source
    trace mapping records or synthetic exact-identity records.  It is not
    obtained from hidden evaluator gold.  All ``source_maps`` / ``mapped_*`` /
    ``bound_*`` style helpers exposed by this module belong to the Issue #164
    ``mapping`` function family, never to a separate ``source_mapping`` family.

    Returns: immutable mapping records and exact-match predicates.

    Execution: filters the frozen mapping list by exact ``source_ref`` and/or
    ``model_ref``.  It does not parse converter exception strings, infer semantic
    equivalence, or upgrade unmapped conversion evidence to confirmed source
    attribution.

    Failure semantics: missing mapping data returns empty results/``False``;
    malformed non-list mapping input raises ``UnsupportedEvidence`` during
    construction.

    Evidence limitations: a mapping can support attribution only under its
    recorded policy and producer.  It does not prove model correctness or NL
    coverage by itself.

    Permissions: read-only in-memory mapping access; no arbitrary paths, shell,
    import, environment, network, mutation, or reference/gold data.

    Example: ``source_maps(source_ref="SEG-NL-003", model_ref="Root.Attack")``
    returns frozen mapping rows for that exact pair.
    """

    family = "mapping"

    def __init__(
        self,
        mappings: list[dict[str, Any]] | None = None,
        *,
        bindings: dict[str, list[str]] | None = None,
    ) -> None:
        if mappings is None:
            mappings = []
        if not isinstance(mappings, list):
            raise UnsupportedEvidence("source mappings must be a list")
        self.mappings = self._normalize_mappings(mappings)
        self.bindings = copy.deepcopy(bindings or {})

    def source_maps(self, *, source_ref: str | None = None, model_ref: str | None = None) -> tuple[FrozenView, ...]:
        out = []
        for row in self.mappings:
            if source_ref is not None and row.get("source_ref") != source_ref:
                continue
            if model_ref is not None and row.get("model_ref") != model_ref:
                continue
            out.append(
                FrozenView(
                    "source_mapping",
                    {
                        "source_ref": row.get("source_ref"),
                        "model_ref": row.get("model_ref"),
                        "relation_policy": row.get("relation_policy"),
                        "confidence": row.get("confidence"),
                        "producer": row.get("producer"),
                        "raw": row,
                    },
                    allowed_fields=MAPPING_FIELDS,
                )
            )
        return tuple(out)

    def has_source_mapping(self, *, source_ref: str, model_ref: str, relation_policy: str | None = None) -> bool:
        rows = self.source_maps(source_ref=source_ref, model_ref=model_ref)
        if relation_policy is None:
            return bool(rows)
        return any(row.relation_policy == relation_policy for row in rows)

    def mapped_source_refs(self, fcstm_ref: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    str(row["source_ref"])
                    for row in self.mappings
                    if row.get("model_ref") == fcstm_ref and row.get("source_ref")
                }
            )
        )

    def mapped_fcstm_refs(self, source_ref: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    str(row["model_ref"])
                    for row in self.mappings
                    if row.get("source_ref") == source_ref and row.get("model_ref")
                }
            )
        )

    def bound_model_refs(
        self, coverage_unit_id: str, fact_kind: str | None = None
    ) -> tuple[str, ...]:
        refs = tuple(self.bindings.get(coverage_unit_id, ()))
        if fact_kind is None:
            return tuple(sorted(refs))
        prefix = fact_kind + ":"
        return tuple(sorted(ref for ref in refs if ref.startswith(prefix)))

    @staticmethod
    def _normalize_mappings(mappings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for row in mappings:
            if not isinstance(row, dict):
                continue
            if row.get("source_ref") is not None or row.get("model_ref") is not None:
                normalized.append(copy.deepcopy(row))
                continue
            sources = row.get("source_elements") or row.get("source_refs") or []
            models = (
                row.get("intermediate_elements")
                or row.get("fcstm_elements")
                or row.get("model_refs")
                or []
            )
            for source_ref in sources:
                for model_ref in models:
                    normalized.append(
                        {
                            "source_ref": str(source_ref),
                            "model_ref": str(model_ref),
                            "relation_policy": row.get("relation_policy"),
                            "confidence": row.get("confidence"),
                            "producer": row.get("producer"),
                            "raw": copy.deepcopy(row),
                        }
                    )
        return normalized


__all__ = ["MAPPING_FIELDS", "SourceMappingAPI"]
