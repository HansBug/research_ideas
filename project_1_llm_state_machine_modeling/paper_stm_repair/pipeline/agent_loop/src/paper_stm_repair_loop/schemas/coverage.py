from __future__ import annotations

from collections import Counter
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal

from .assertions import FunctionFamily, LogicalAssertionRegistration
from .roots import PropositionRootRegistration


class StrictContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


SegmentKind = Literal["title", "list_item", "prose"]
SegmentDispositionKind = Literal["context_only", "representation_boundary"]
SourceFactKind = Literal[
    "state",
    "event",
    "variable",
    "transition",
    "forced_transition",
    "guard",
    "effect",
    "initial_relation",
    "hierarchy",
    "region",
    "diagnostic",
    "unsupported_marker",
    "source_fcstm_mapping",
]
FactDispositionKind = Literal[
    "implementation_support",
    "diagnostic_support",
    "mapping_support",
    "representation_boundary",
]
CoverageUnitKind = Literal[
    "behavior_obligation",
    "source_behavior",
    "initialization_obligation",
]
BehaviorDimension = Literal[
    "behavior",
    "structure",
    "cardinality",
    "initialization",
    "transition",
    "condition",
    "effect",
    "ordering",
    "continuity",
    "completion",
    "forbidden_behavior",
    "timing",
]
BEHAVIOR_RELEVANT_FACT_KINDS: frozenset[str] = frozenset(
    {
        "state",
        "event",
        "variable",
        "transition",
        "forced_transition",
        "guard",
        "effect",
        "initial_relation",
        "hierarchy",
        "region",
    }
)


class InputSegment(StrictContractModel):
    segment_id: str
    source_role: Literal["nl"] = "nl"
    text: str
    start_offset: int = Field(ge=0)
    end_offset: int = Field(ge=0)
    raw_start_offset: int = Field(ge=0)
    raw_end_offset: int = Field(ge=0)
    sha256: str
    language: str = "en-US"
    segmenter_version: str
    segment_kind: SegmentKind
    ordinal: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_offsets(self) -> "InputSegment":
        if self.end_offset <= self.start_offset:
            raise ValueError("end_offset must be greater than start_offset")
        if self.raw_end_offset <= self.raw_start_offset:
            raise ValueError("raw_end_offset must be greater than raw_start_offset")
        return self


class SegmentDisposition(StrictContractModel):
    segment_id: str
    disposition: SegmentDispositionKind
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"


class SourceFact(StrictContractModel):
    fact_id: str
    fact_kind: SourceFactKind
    qualified_refs: list[str] = Field(default_factory=list)
    producer: str
    producer_version: str | None = None
    provenance: str
    behavior_relevant: bool
    source: str | None = None
    event: str | None = None
    target: str | None = None
    guard: str | None = None
    effects: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_relevance_policy(self) -> "SourceFact":
        expected = self.fact_kind in BEHAVIOR_RELEVANT_FACT_KINDS
        if self.behavior_relevant is not expected:
            raise ValueError(
                f"behavior_relevant must be {expected!r} for fact_kind={self.fact_kind!r}"
            )
        if "semantic_role" in self.payload:
            raise ValueError("SourceFact must not carry semantic_role")
        return self


class CoverageRequirement(StrictContractModel):
    requirement_id: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    clause_id: str = Field(min_length=1)
    clause_text: str = Field(min_length=1)
    clause_start_offset: int = Field(ge=0)
    clause_end_offset: int = Field(ge=0)
    dimension: BehaviorDimension
    cue_text: str = Field(min_length=1)
    cue_start_offset: int = Field(ge=0)
    cue_end_offset: int = Field(ge=0)
    required_function_family_options: list[list[FunctionFamily]] = Field(min_length=1)
    derivation: Literal[
        "deterministic_clause_coverage_v2",
        "deterministic_lexical_cue_v2",
    ]
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_requirement(self) -> "CoverageRequirement":
        if self.cue_end_offset <= self.cue_start_offset:
            raise ValueError("coverage requirement cue span must be non-empty")
        if self.clause_end_offset <= self.clause_start_offset:
            raise ValueError("coverage requirement clause span must be non-empty")
        if not (
            self.clause_start_offset <= self.cue_start_offset
            and self.cue_end_offset <= self.clause_end_offset
        ):
            raise ValueError("coverage requirement cue must be inside its clause span")
        if any(not option for option in self.required_function_family_options):
            raise ValueError("coverage requirement family options must be non-empty")
        return self


class FactDisposition(StrictContractModel):
    fact_id: str
    disposition: FactDispositionKind
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"


class CoverageUnit(StrictContractModel):
    coverage_unit_id: str
    unit_kind: CoverageUnitKind
    segment_ids: list[str] = Field(default_factory=list)
    source_fact_ids: list[str] = Field(default_factory=list)
    requirement_ids: list[str] = Field(default_factory=list)
    dimensions: list[BehaviorDimension] = Field(default_factory=list)
    statement: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"
    in_scope: bool = True

    @model_validator(mode="after")
    def validate_basis(self) -> "CoverageUnit":
        if not self.segment_ids and not self.source_fact_ids:
            raise ValueError("CoverageUnit requires at least one segment or source fact basis")
        if self.unit_kind == "behavior_obligation" and not self.segment_ids:
            raise ValueError("behavior_obligation requires NL segment basis")
        if self.unit_kind == "source_behavior" and self.segment_ids:
            raise ValueError("source_behavior must not claim NL segment basis")
        if self.unit_kind == "source_behavior" and not self.source_fact_ids:
            raise ValueError("source_behavior requires source fact basis")
        return self


class CoveragePlan(StrictContractModel):
    segment_dispositions: list[SegmentDisposition] = Field(default_factory=list)
    fact_dispositions: list[FactDisposition] = Field(default_factory=list)
    coverage_units: list[CoverageUnit] = Field(default_factory=list)
    proposition_roots: list[PropositionRootRegistration] = Field(default_factory=list)
    logical_assertions: list[LogicalAssertionRegistration] = Field(default_factory=list)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_registered_coverage(self) -> "CoveragePlan":
        unit_ids = {unit.coverage_unit_id for unit in self.coverage_units}
        _reject_duplicates(
            "segment_disposition.segment_id",
            [disposition.segment_id for disposition in self.segment_dispositions],
        )
        _reject_duplicates(
            "fact_disposition.fact_id",
            [disposition.fact_id for disposition in self.fact_dispositions],
        )
        _reject_duplicates("coverage_unit_id", [unit.coverage_unit_id for unit in self.coverage_units])

        disposed_segments = {disposition.segment_id for disposition in self.segment_dispositions}
        referenced_segments = {segment_id for unit in self.coverage_units for segment_id in unit.segment_ids}
        overlap_segments = disposed_segments & referenced_segments
        if overlap_segments:
            raise ValueError(
                "segment must not have both CoverageUnit refs and SegmentDisposition: "
                f"{sorted(overlap_segments)}"
            )
        disposed_facts = {disposition.fact_id for disposition in self.fact_dispositions}
        referenced_facts = {fact_id for unit in self.coverage_units for fact_id in unit.source_fact_ids}
        overlap_facts = disposed_facts & referenced_facts
        if overlap_facts:
            raise ValueError(
                "source fact must not have both CoverageUnit refs and FactDisposition: "
                f"{sorted(overlap_facts)}"
            )

        root_unit_ids = [root.coverage_unit_id for root in self.proposition_roots]
        _reject_duplicates("root.coverage_unit_id", root_unit_ids)
        missing_roots = unit_ids - set(root_unit_ids)
        if missing_roots:
            raise ValueError(f"coverage units without exactly one root: {sorted(missing_roots)}")
        unknown_root_units = set(root_unit_ids) - unit_ids
        if unknown_root_units:
            raise ValueError(f"roots reference unknown coverage units: {sorted(unknown_root_units)}")

        root_ids = {root.node_id for root in self.proposition_roots}
        _reject_duplicates("root.node_id", [root.node_id for root in self.proposition_roots])
        required_assertion_root_ids = {
            assertion.root_node_id
            for assertion in self.logical_assertions
            if assertion.required is True
        }
        roots_without_assertions = root_ids - required_assertion_root_ids
        if roots_without_assertions:
            raise ValueError(f"roots without required assertions: {sorted(roots_without_assertions)}")

        assert_texts = [
            assertion.assert_
            for assertion in self.logical_assertions
        ]
        _reject_duplicates("logical_assertion.assert", assert_texts)
        _reject_duplicates(
            "logical_assertion.assertion_chain_id",
            [assertion.assertion_chain_id for assertion in self.logical_assertions],
        )
        root_units = {root.node_id: root.coverage_unit_id for root in self.proposition_roots}
        for assertion in self.logical_assertions:
            if assertion.root_node_id not in root_ids:
                raise ValueError(
                    f"assertion references unknown root: {assertion.root_node_id}"
                )
            if assertion.coverage_unit_id not in unit_ids:
                raise ValueError(
                    "assertion references unknown coverage unit: "
                    f"{assertion.coverage_unit_id}"
                )
            if root_units.get(assertion.root_node_id) != assertion.coverage_unit_id:
                raise ValueError(
                    "assertion root/unit relation is inconsistent: "
                    f"{assertion.assertion_chain_id}"
                )
        return self


def _reject_duplicates(label: str, values: list[str]) -> None:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise ValueError(f"duplicate {label}: {duplicates}")
