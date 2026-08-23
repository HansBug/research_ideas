"""Typed input closure and deterministic inspection-equivalent facts.

This module is deliberately independent from ``pyfcstm`` and from the legacy
feedback-loop inspection helpers.  It reads already published representation
artifacts as facts, and computes the small closed-world inventory needed by the
new evidence method with algorithms owned by this package.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import ModelIR
from .provenance import sha256_text


ArtifactRole = Literal[
    "natural_language",
    "plantuml_source",
    "fcstm_model",
    "canonical_source_ir",
    "source_inventory",
    "working_contract",
    "source_trace",
    "case_report",
    "reference_inspection_facts",
    "inspection_equivalent_facts",
    "verify_facts",
    "smt_facts",
]
SourceRole = Literal[
    "author_source",
    "closed_model",
    "deterministic_facts",
    "mapping",
    "provenance",
    "runtime_summary",
]
PromptStage = Literal[
    "nl_contract_extraction",
    "discovery_grounding",
    "d_adjudication",
]


class ArtifactRef(BaseModel):
    """Versioned hash reference for one method-visible artifact.

    The reference is the receipt boundary.  A prompt may contain a payload,
    but an auditor can always identify the exact file, producer, algorithm,
    schema, and bytes that were supplied to the method.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    role: ArtifactRole = Field(description="Stable role of the artifact in the input closure.")
    source_role: SourceRole = Field(description="Provenance role: authored source, closed model, deterministic facts, mapping, or runtime summary.")
    path: str = Field(min_length=1, description="Resolved source path recorded for audit; the method uses the payload, not path discovery.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 digest of the exact artifact bytes supplied to the method.")
    schema_version: str = Field(min_length=1, description="Schema version of the artifact payload.")
    algorithm_version: str = Field(min_length=1, description="Producer algorithm version, or an explicit artifact-export version.")
    producer: str = Field(min_length=1, description="Named producer of the artifact; never inferred from diagnostic prose.")
    prompt_included: bool = Field(description="Whether the corresponding structured payload is included in method/grounding context.")
    reason: str = Field(min_length=1, description="Why this artifact is part of the method input closure.")
    basis: str = Field(min_length=1, description="Concrete file, algorithm, or protocol basis for including this artifact.")


def _artifact_prompt_ref(ref: ArtifactRef) -> dict[str, Any]:
    """Project receipt identity without exposing filesystem layout to the provider."""

    return {
        key: value
        for key, value in ref.model_dump(mode="json").items()
        if key != "path"
    }


class StructuredArtifact(BaseModel):
    """JSON artifact together with its immutable provenance reference."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    ref: ArtifactRef = Field(description="Versioned provenance reference for the JSON artifact.")
    payload: dict[str, Any] = Field(description="Parsed JSON object supplied as structured context; it is never treated as an execution result by itself.")

    def to_prompt_dict(self) -> dict[str, Any]:
        """Return the structured payload with a path-free receipt projection."""

        return {"ref": _artifact_prompt_ref(self.ref), "payload": self.payload}


_CASE_REPORT_HASH_FIELDS = {
    "canonical_source": "canonical_sha256",
    "closed_model": "fcstm_sha256",
    "inspection_facts": "parse_inspect_sha256",
    "source_trace": "source_trace_sha256",
    "working_contract": "working_contract_sha256",
    "source_artifact": "source_sha256",
}


def case_report_prompt_dict(artifact: StructuredArtifact | None) -> dict[str, Any] | None:
    """Expose only case identity/status fields from the published case report.

    The complete case report remains hash-addressed in the input receipt, but
    historical stage lineage, prior LLM payloads, comparison summaries, and
    review outputs are not method inputs. Keeping this projection explicit
    prevents old experiment answers from entering a new method prompt.
    """

    if artifact is None:
        return None
    payload = {
        "case_id": artifact.payload.get("case_id"),
        "case_index": artifact.payload.get("pair_index"),
        "source_hashes": {
            public_name: artifact.payload[source_name]
            for public_name, source_name in _CASE_REPORT_HASH_FIELDS.items()
            if source_name in artifact.payload
        },
        "artifact_status": {
            "input": artifact.payload.get("official_raw_status"),
            "validated": artifact.payload.get("official_validation_status"),
        },
    }
    return {
        "ref": _artifact_prompt_ref(artifact.ref),
        "payload": payload,
        "reason": "Only case identity and artifact status are prompt-visible; historical run outputs are receipt-only.",
        "basis": "case-report prompt projection v1",
    }


def reference_inspection_prompt_dict(
    artifact: StructuredArtifact | None,
) -> dict[str, Any] | None:
    """Project the published inspection artifact into a compact fact summary.

    The complete artifact remains hash-addressed by ``artifact.ref`` and is
    retained in the run inputs.  Grounding receives the structured inventory,
    diagnostics, reachability, and transition facts that are useful for
    routing, while repetitive legacy projections are represented by explicit
    count/hash receipts instead of being silently dropped or copied wholesale
    into every prompt.
    """

    if artifact is None:
        return None
    payload = artifact.payload
    diagnostics = [
        {
            key: row[key]
            for key in ("code", "severity", "refs", "span")
            if isinstance(row, dict) and key in row
        }
        for row in payload.get("diagnostics", [])
        if isinstance(row, dict)
    ]
    diagnostic_counts: dict[str, int] = {}
    for row in diagnostics:
        code = str(row.get("code") or "UNKNOWN")
        diagnostic_counts[code] = diagnostic_counts.get(code, 0) + 1

    inventory_sections = (
        "states",
        "transitions",
        "actions",
        "events",
        "variables",
        "forced_transitions",
        "reachability_graph",
        "event_emission_map",
        "var_dataflow",
    )
    inventory_receipts = {
        key: {
            "count": len(value) if isinstance(value, (list, dict, str)) else None,
            "sha256": _artifact_hash_payload({"value": value}),
        }
        for key in inventory_sections
        if (value := payload.get(key)) is not None
    }
    selected = {
        "metrics": payload.get("metrics", {}),
        "root_state_path": payload.get("root_state_path"),
        "diagnostic_counts": diagnostic_counts,
        "diagnostics": diagnostics,
        "forced_transitions": payload.get("forced_transitions", []),
        "inventory_receipts": inventory_receipts,
        "reason": "The prompt carries compact inspection status, metrics, exact diagnostic references, and inventory identities; exact source/closed-model inventories and owned facts are supplied separately.",
        "basis": "published compact inspection shape plus compact-inspection-projection.v2",
    }
    return {
        "ref": _artifact_prompt_ref(artifact.ref),
        "payload": selected,
        "reason": "Compact inspection facts remain prompt-visible without duplicating the exact inventories supplied by the other closure artifacts.",
        "basis": "compact-inspection-projection.v2; complete source bytes remain hash-addressed in the manifest",
    }


class NumberedNLSegment(BaseModel):
    """One deterministic numbered natural-language segment."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Stable NL segment identifier; duplicate source numbers receive a deterministic suffix.")
    source_number: int = Field(ge=1, description="Number printed or recoverable at the start of this source clause.")
    ordinal: int = Field(ge=1, description="One-based deterministic segment order in the artifact.")
    text: str = Field(min_length=1, description="Exact segment text after removing only the leading source number marker.")
    raw_start: int = Field(ge=0, description="Zero-based character offset of the segment in the exact NL artifact.")
    raw_end: int = Field(ge=1, description="Exclusive zero-based character offset of the segment in the exact NL artifact.")
    reason: str = Field(min_length=1, description="Why this segment boundary was selected by the deterministic splitter.")
    basis: str = Field(min_length=1, description="Splitter version and exact source-marker basis for this segment.")


class CanonicalState(BaseModel):
    """Author-source state entry from the canonical PlantUML source IR."""

    model_config = ConfigDict(extra="allow", frozen=True, str_strip_whitespace=True)

    id: str = Field(min_length=1, description="Canonical source state identity used for source attribution.")
    kind: str = Field(min_length=1, description="Canonical source state kind, such as composite, state, or pseudo.")
    label: str = Field(default="", description="Author-source display label, if present.")
    parent: str | None = Field(default=None, description="Canonical parent state identity, or null for a root state.")
    raw_ref: str = Field(min_length=1, description="Exact PlantUML source reference for this state.")
    attributes: dict[str, Any] = Field(default_factory=dict, description="Structured canonical source attributes retained for source localization.")


class CanonicalTransition(BaseModel):
    """Author-source transition entry from the canonical PlantUML source IR."""

    model_config = ConfigDict(extra="allow", frozen=True, str_strip_whitespace=True)

    id: str = Field(min_length=1, description="Canonical transition identity used for source attribution.")
    source: str = Field(min_length=1, description="Canonical source endpoint.")
    target: str = Field(min_length=1, description="Canonical target endpoint.")
    event: str | None = Field(default=None, description="Author-source event or label projection, if present.")
    guard: str | None = Field(default=None, description="Author-source guard, if present.")
    action: str | None = Field(default=None, description="Author-source action, if present.")
    label: str | None = Field(default=None, description="Original canonical transition label, if present.")
    raw_ref: str = Field(min_length=1, description="Exact PlantUML source reference for this transition.")
    attributes: dict[str, Any] = Field(default_factory=dict, description="Structured canonical transition attributes retained for source localization.")


class CanonicalConcurrentRegion(BaseModel):
    """Canonical author-source partition for one UML concurrent region.

    The PlantUML canonical adapter produces this row and source grounding plus the
    deterministic frontier consume it.  It is authoritative only for the exact
    authored owner, separator, state, and transition inventory.  It does not state
    a normative requirement, closed-model behavior, predicate result, W/D/L level,
    or judge relation.  A composite with no such rows can still have one implicit
    UML region; that derived count belongs to the frontier, not this source row.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.canonical-concurrent-region.v1"] = Field(
        default="evidence-discovery.canonical-concurrent-region.v1",
        description="Typed schema version of this canonical concurrent-region row; it records artifact and algorithm provenance and is not a source-file region ID.",
    )
    id: str = Field(
        min_length=1,
        description="Stable source identity generated by the canonical adapter for this explicit UML region; downstream code uses it only for exact enumeration and never infers semantics from its spelling.",
    )
    owner_scope: str | None = Field(
        default=None,
        description="Exact canonical owner-state ID of this region; null means only a model-level region, not an unresolved owner or permission to guess by name.",
    )
    region_index: int = Field(
        ge=0,
        description="Zero-based region position within the exact owner in author-source order; this is a factual location, not a normative cardinality.",
    )
    separator_after_raw_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact PlantUML separator source references immediately after this region; an empty tuple means no following explicit separator, not that the region is absent.",
    )
    separator_before_raw_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact PlantUML separator source references immediately before this region; the first explicit region normally has none.",
    )
    state_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact state IDs assigned to this region in the canonical source inventory; an empty tuple may represent an explicit region with no state declaration.",
    )
    transition_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact transition IDs assigned to this region in the canonical source inventory; an empty tuple means no authored transition and is not a behavioral satisfaction verdict.",
    )
    reason: str = Field(
        default="This row preserves one explicit canonical author-source UML region without adding a semantic verdict.",
        min_length=1,
        description="Explains why this object is only a canonical source-partition fact with no requirement, W, D, or Judge authority.",
    )
    basis: str = Field(
        default="canonical PlantUML source IR model.concurrent_regions",
        min_length=1,
        description="Exact canonical artifact field that produced this row; downstream audit verifies its provenance with the source artifact hash.",
    )


class CanonicalModel(BaseModel):
    """Typed source model portion of the canonical PlantUML IR."""

    model_config = ConfigDict(extra="allow", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Canonical source model name.")
    hierarchy_level: str = Field(default="unknown", description="Canonical hierarchy classification.")
    timing_level: str = Field(default="unknown", description="Canonical timing classification; unknown is preserved rather than inferred.")
    initial_states: tuple[str, ...] = Field(default_factory=tuple, description="Canonical initial state identities.")
    final_states: tuple[str, ...] = Field(default_factory=tuple, description="Canonical explicit final state identities.")
    concurrent_regions: tuple[CanonicalConcurrentRegion, ...] = Field(
        default_factory=tuple,
        description="Explicit canonical UML region partitions; an empty tuple means no separator-derived rows, while the frontier may still count one implicit region for an exact owner with direct child states.",
    )
    variables: tuple[dict[str, Any], ...] = Field(default_factory=tuple, description="Canonical source variable facts, if any.")
    states: tuple[CanonicalState, ...] = Field(default_factory=tuple, description="Exact canonical source state inventory in source order.")
    transitions: tuple[CanonicalTransition, ...] = Field(default_factory=tuple, description="Exact canonical source transition inventory in source order.")


class CanonicalSourceIR(BaseModel):
    """Complete author-source IR context used for source localization only."""

    model_config = ConfigDict(extra="allow", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="Canonical source IR schema version.")
    source_format: str = Field(min_length=1, description="Source format represented by this IR, normally plantuml.")
    example_id: str = Field(min_length=1, description="Stable source example identity.")
    seed_id: str = Field(min_length=1, description="Stable source seed identity.")
    adapter: str = Field(min_length=1, description="Canonical source adapter that produced this IR.")
    status: str = Field(min_length=1, description="Canonical conversion status.")
    status_reason_code: str = Field(min_length=1, description="Structured conversion status reason code.")
    model: CanonicalModel = Field(description="Typed canonical source model.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Canonical metadata required for source identity and mapping review.")


class SourceInventoryState(BaseModel):
    """Exact source state inventory row with no semantic verdict."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source_id: str = Field(min_length=1, description="Exact source state identity.")
    name: str = Field(min_length=1, description="Source display or short name.")
    kind: str = Field(min_length=1, description="Source state kind.")
    parent: str | None = Field(default=None, description="Exact source parent identity, if any.")
    raw_ref: str = Field(min_length=1, description="Exact source line reference.")
    line: int | None = Field(default=None, ge=1, description="One-based source line when recoverable from raw_ref.")
    reason: str = Field(min_length=1, description="Why this row is an inventory fact rather than a method judgment.")
    basis: str = Field(min_length=1, description="Canonical source IR field basis for this row.")


class SourceInventoryTransition(BaseModel):
    """Exact source transition inventory row with separate source attribution fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    transition_id: str = Field(min_length=1, description="Exact source transition identity.")
    source: str = Field(min_length=1, description="Exact source endpoint identity.")
    target: str = Field(min_length=1, description="Exact target endpoint identity.")
    event: str | None = Field(default=None, description="Source event or label projection, if present.")
    guard: str | None = Field(default=None, description="Source guard, if present.")
    action: str | None = Field(default=None, description="Source action, if present.")
    raw_ref: str = Field(min_length=1, description="Exact source line reference.")
    line: int | None = Field(default=None, ge=1, description="One-based source line when recoverable from raw_ref.")
    reason: str = Field(min_length=1, description="Why this row is an exact source inventory fact.")
    basis: str = Field(min_length=1, description="Canonical source transition field basis for this row.")


class ExactSourceInventory(BaseModel):
    """Versioned exact source/transition inventory derived from canonical source IR."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="Exact source inventory schema version.")
    algorithm_version: str = Field(min_length=1, description="Deterministic source inventory projection version.")
    source_ir_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the canonical source IR artifact used for projection.")
    states: tuple[SourceInventoryState, ...] = Field(description="Complete exact source state inventory.")
    transitions: tuple[SourceInventoryTransition, ...] = Field(description="Complete exact source transition inventory.")
    events: tuple[str, ...] = Field(default_factory=tuple, description="Unique source event/label values in source order.")
    reason: str = Field(min_length=1, description="Why this inventory is supplied to method grounding.")
    basis: str = Field(min_length=1, description="Canonical source IR and deterministic projection basis.")


class InspectionStateFact(BaseModel):
    """Inspection-equivalent state inventory row computed from the closed FCSTM model."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    state_ref: str = Field(min_length=1, description="Stable owned-parser state reference.")
    name: str = Field(min_length=1, description="FCSTM state identifier.")
    parent: str | None = Field(default=None, description="FCSTM enclosing state identifier, if any.")
    line: int = Field(ge=1, description="One-based FCSTM declaration line.")
    is_composite: bool = Field(description="Whether the state has a nested declaration in the owned parser model.")
    reachable_from_initial: bool = Field(description="Whether the state is reached by the owned finite hierarchical entry traversal.")
    outgoing_transition_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact owned-parser transition refs leaving this state.")
    reason: str = Field(min_length=1, description="Why this is a deterministic inventory fact.")
    basis: str = Field(min_length=1, description="Owned FCSTM parser fields used for this row.")


class InspectionTransitionFact(BaseModel):
    """Inspection-equivalent transition inventory row computed from FCSTM."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    transition_ref: str = Field(min_length=1, description="Stable owned-parser transition reference.")
    source: str = Field(min_length=1, description="FCSTM transition source endpoint.")
    target: str = Field(min_length=1, description="FCSTM transition target endpoint.")
    triggers: tuple[str, ...] = Field(default_factory=tuple, description="Normalized FCSTM trigger set.")
    guard: str | None = Field(default=None, description="Normalized FCSTM guard, if any.")
    effects: tuple[str, ...] = Field(default_factory=tuple, description="Normalized FCSTM effect fragments.")
    line: int = Field(ge=1, description="One-based FCSTM transition line.")
    scope: str | None = Field(default=None, min_length=1, description="Nearest enclosing FCSTM state scope, or null for a top-level transition.")
    resolved_source_ref: str | None = Field(default=None, min_length=1, description="Exact state ref resolved for the transition source, when the owned scope algorithm can resolve it.")
    resolved_target_ref: str | None = Field(default=None, min_length=1, description="Exact state ref resolved for the transition target, or null for a final pseudostate.")
    reachable_from_initial: bool = Field(description="Whether the transition source is reachable in the finite hierarchical entry traversal.")
    reason: str = Field(min_length=1, description="Why this is a deterministic inventory fact.")
    basis: str = Field(min_length=1, description="Owned FCSTM parser fields used for this row.")


class EventConsumerFact(BaseModel):
    """Finite event-to-transition consumer coverage fact for model grounding."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    event: str = Field(min_length=1, description="Exact normalized event or trigger name under review.")
    declared_ref: str | None = Field(default=None, min_length=1, description="Exact declared FCSTM event ref, when the event is declared.")
    consumer_transition_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact transitions whose normalized trigger set contains this event.")
    consumer_state_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact source state refs of the consumer transitions.")
    reachable_consumer_transition_refs: tuple[str, ...] = Field(default_factory=tuple, description="Consumer transitions whose source state is reachable in the finite closed-model traversal.")
    reachable_consumer_state_refs: tuple[str, ...] = Field(default_factory=tuple, description="Reachable source state refs that consume this event.")
    reason: str = Field(min_length=1, description="Why this event-consumer coverage row was emitted.")
    basis: str = Field(min_length=1, description="Exact event declarations, transition triggers, and hierarchical reachability facts used.")


class InspectionDiagnostic(BaseModel):
    """Structured deterministic diagnostic; message text is never parsed downstream."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    code: str = Field(min_length=1, description="Stable diagnostic code emitted by the owned inspection-equivalent algorithm.")
    severity: Literal["info", "warning", "error"] = Field(description="Diagnostic severity from the deterministic algorithm.")
    refs: tuple[str, ...] = Field(default_factory=tuple, description="Stable model refs directly implicated by the diagnostic.")
    line: int | None = Field(default=None, ge=1, description="Primary FCSTM line when the diagnostic has one.")
    message: str = Field(min_length=1, description="Human-readable diagnostic message; not a machine parsing interface.")
    reason: str = Field(min_length=1, description="Why the algorithm emitted this diagnostic.")
    basis: str = Field(min_length=1, description="Deterministic fact rule and input basis for this diagnostic.")


class InspectionEquivalentFacts(BaseModel):
    """Versioned inspection-equivalent inventory and diagnostics for grounding."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="Inspection-equivalent fact schema version.")
    algorithm_version: str = Field(min_length=1, description="Owned deterministic algorithm version; no Python inspect or legacy inspector is used.")
    fcstm_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the exact FCSTM bytes inspected by this algorithm.")
    states: tuple[InspectionStateFact, ...] = Field(description="Complete closed-model state inventory.")
    transitions: tuple[InspectionTransitionFact, ...] = Field(description="Complete closed-model transition inventory.")
    events: tuple[str, ...] = Field(default_factory=tuple, description="Unique closed-model event inventory in source order.")
    diagnostics: tuple[InspectionDiagnostic, ...] = Field(default_factory=tuple, description="Structured deterministic diagnostics, never semantic issue decisions.")
    reachability: dict[str, tuple[str, ...]] = Field(default_factory=dict, description="Finite graph reachability facts keyed by deterministic root names.")
    machine_root_ref: str | None = Field(default=None, min_length=1, description="Exact parser state ref used as the closed-model machine container, when the FCSTM has one.")
    reachable_state_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact state refs reached from top-level initial entries under the owned hierarchical traversal.")
    event_consumers: tuple[EventConsumerFact, ...] = Field(default_factory=tuple, description="Exact event-to-transition consumer coverage facts, including reachable and unreachable consumers.")
    metrics: dict[str, int | float] = Field(default_factory=dict, description="Deterministic inventory metrics such as state and transition counts.")
    reason: str = Field(min_length=1, description="Why these facts are supplied to method/grounding.")
    basis: str = Field(min_length=1, description="Owned parser and inspection-equivalent algorithm basis.")


class VerificationCheck(BaseModel):
    """One finite closed-model verification fact."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    check_id: str = Field(min_length=1, description="Stable deterministic verification check identifier.")
    kind: Literal["reachability", "initial_entry", "deadlock", "event_consumer", "guard_inventory"] = Field(description="Verification fact family.")
    status: Literal["proved", "refuted", "unknown"] = Field(description="Deterministic result status; unknown is never promoted to a violation.")
    subject_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact model refs examined by this check.")
    details: dict[str, Any] = Field(default_factory=dict, description="Structured check facts and finite-domain boundaries.")
    reason: str = Field(min_length=1, description="Why this deterministic check has its status.")
    basis: str = Field(min_length=1, description="Algorithm and closed-model facts supporting the check.")


class VerificationFacts(BaseModel):
    """Versioned finite verification summary passed to grounding and compiler planning."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="Verification fact summary schema version.")
    algorithm_version: str = Field(min_length=1, description="Owned finite verification algorithm version.")
    scope: str = Field(min_length=1, description="Closed-model verification scope; it is never a source-author claim.")
    checks: tuple[VerificationCheck, ...] = Field(description="Structured finite verification checks.")
    terminal_state: Literal["completed", "unknown"] = Field(description="Whether the finite verification summary completed deterministically.")
    reason: str = Field(min_length=1, description="Why the summary is supplied and what it does not claim.")
    basis: str = Field(min_length=1, description="Inspection-equivalent facts and owned finite graph algorithm basis.")


class SMTFormulaFact(BaseModel):
    """One normalized bounded-formula inventory row without claiming solver execution."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    formula_id: str = Field(min_length=1, description="Stable normalized formula inventory identifier.")
    source_ref: str = Field(min_length=1, description="Exact FCSTM transition or state ref supplying the formula text.")
    expression: str = Field(min_length=1, description="Normalized guard/invariant expression supplied to a future bounded backend.")
    variables: tuple[str, ...] = Field(default_factory=tuple, description="Identifiers conservatively extracted from the expression.")
    solver_status: Literal["not_run", "unknown"] = Field(description="This input summary does not claim a solver result.")
    reason: str = Field(min_length=1, description="Why this formula is included in the bounded-verification context.")
    basis: str = Field(min_length=1, description="Owned parser normalization basis; no solver output is inferred.")


class SMTFacts(BaseModel):
    """Versioned SMT/formal-program context with explicit non-execution boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="SMT fact summary schema version.")
    algorithm_version: str = Field(min_length=1, description="Owned formula-normalization algorithm version.")
    scope: str = Field(min_length=1, description="Bounded formal context scope.")
    formulas: tuple[SMTFormulaFact, ...] = Field(description="Normalized guard and invariant formula inventory.")
    solver_status: Literal["not_run", "unknown"] = Field(description="Explicitly records that this summary is not a solver result.")
    reason: str = Field(min_length=1, description="Why the formula summary is supplied.")
    basis: str = Field(min_length=1, description="Owned deterministic formula extraction basis.")


class PromptSection(BaseModel):
    """Manifest entry describing one prompt context section."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    section_id: str = Field(min_length=1, description="Stable prompt section identifier.")
    artifact_roles: tuple[ArtifactRole, ...] = Field(description="Artifact roles represented in this section.")
    purpose: str = Field(min_length=1, description="What the section lets the method decide.")
    excluded_claims: tuple[str, ...] = Field(default_factory=tuple, description="Claims this section must not be used to make, preserving source-role boundaries.")
    reason: str = Field(min_length=1, description="Why this section is present.")
    basis: str = Field(min_length=1, description="Artifact and protocol basis for this section.")


class ContextManifest(BaseModel):
    """Auditable manifest for the complete method/grounding input closure."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(min_length=1, description="Input context manifest schema version.")
    protocol_version: str = Field(min_length=1, description="Frozen method input protocol version.")
    pair_id: str = Field(min_length=1, description="Frozen pair identifier.")
    artifacts: tuple[ArtifactRef, ...] = Field(min_length=1, description="Every artifact supplied to method/grounding, including deterministic summaries.")
    sections: tuple[PromptSection, ...] = Field(min_length=1, description="Prompt sections and their role boundaries.")
    forbidden_inputs: tuple[str, ...] = Field(min_length=1, description="Data classes excluded from method generation, including evaluation ground truth, scores, and reviewer outputs.")
    manifest_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash over the manifest content excluding this field.")
    reason: str = Field(min_length=1, description="Why this manifest is the method's input closure boundary.")
    basis: str = Field(min_length=1, description="Frozen protocol and artifact reference basis for the manifest.")


def _line_from_ref(raw_ref: str) -> int | None:
    match = re.search(r":line:(\d+)$", raw_ref)
    return int(match.group(1)) if match else None


def _canonical_source_ir(payload: dict[str, Any]) -> CanonicalSourceIR:
    """Validate the stable canonical fields while retaining forward-compatible extras."""

    model_payload = payload.get("model")
    if not isinstance(model_payload, dict):
        raise ValueError("canonical source IR must contain a model object")
    return CanonicalSourceIR(
        schema_version=str(payload.get("schema_version", "canonical-source-ir.unknown")),
        source_format=str(payload.get("source_format", "unknown")),
        example_id=str(payload.get("example_id", "unknown")),
        seed_id=str(payload.get("seed_id", payload.get("example_id", "unknown"))),
        adapter=str(payload.get("adapter", "unknown")),
        status=str(payload.get("status", "unknown")),
        status_reason_code=str(payload.get("status_reason_code", "unknown")),
        model=CanonicalModel(
            name=str(model_payload.get("name", payload.get("example_id", "unknown"))),
            hierarchy_level=str(model_payload.get("hierarchy_level", "unknown")),
            timing_level=str(model_payload.get("timing_level", "unknown")),
            initial_states=tuple(str(value) for value in model_payload.get("initial_states", ()) if value is not None),
            final_states=tuple(str(value) for value in model_payload.get("final_states", ()) if value is not None),
            concurrent_regions=tuple(
                CanonicalConcurrentRegion.model_validate(value)
                for value in model_payload.get("concurrent_regions", ())
                if isinstance(value, dict)
            ),
            variables=tuple(value for value in model_payload.get("variables", ()) if isinstance(value, dict)),
            states=tuple(CanonicalState.model_validate(value) for value in model_payload.get("states", ()) if isinstance(value, dict)),
            transitions=tuple(CanonicalTransition.model_validate(value) for value in model_payload.get("transitions", ()) if isinstance(value, dict)),
        ),
        metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {},
    )


def build_numbered_nl_segments(text: str) -> tuple[NumberedNLSegment, ...]:
    """Split explicit numbered clauses without interpreting requirement text.

    Multi-line artifacts use ``N`` or ``N.`` markers at physical line starts. A
    constrained fallback retains historical one-line artifacts: dotted markers
    and ``N when``/``Nwhen`` delimiters remain explicit, while a plain ``N``
    marker is accepted only at the artifact start or after sentence punctuation.
    Numeric quantities and decimals are therefore retained inside their clause.
    """

    line_marker = re.compile(r"(?m)^[ \t]*(?P<number>[1-9]\d*)(?:\.)?(?=[ \t]+)")
    legacy_marker = re.compile(
        r"(?<![A-Za-z0-9_.])(?P<number>[1-9]\d*)"
        r"(?:(?P<dot>\.)(?=[ \t]+)|(?P<attached_when>(?=when\b))|"
        r"(?P<spaced_when>(?=[ \t]+when\b))|(?P<plain>(?=[ \t]+)))"
    )

    line_matches: list[re.Match[str]] = []
    last_line_number = 0
    for match in line_marker.finditer(text):
        number = int(match.group("number"))
        if number == 1 and not line_matches:
            line_matches.append(match)
            last_line_number = number
        elif line_matches and number in {last_line_number, last_line_number + 1}:
            line_matches.append(match)
            last_line_number = number
    if "\n" in text or "\r" in text:
        matches = line_matches
        algorithm_basis = "nl-segmentation.v2; contiguous physical-line-start N or N. marker"
        boundary_reason = "A physical line starts with a contiguous N or N. source marker; the next such line bounds this segment."
    else:
        matches = []
        for match in legacy_marker.finditer(text):
            if match.group("plain") is not None:
                prefix = text[: match.start("number")].rstrip()
                if prefix and prefix[-1] not in ".!?":
                    continue
            matches.append(match)
        algorithm_basis = "nl-segmentation.v2; constrained one-line legacy delimiter"
        boundary_reason = "An explicit one-line legacy source delimiter bounds this segment without interpreting clause text."

    segments: list[NumberedNLSegment] = []
    seen: dict[int, int] = {}
    for index, match in enumerate(matches):
        number = int(match.group("number"))
        if number > 99:
            continue
        start = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        end = matches[index + 1].start("number") if index + 1 < len(matches) else len(text)
        value = text[start:end].strip()
        if not value:
            continue
        seen[number] = seen.get(number, 0) + 1
        suffix = f".{seen[number]}" if seen[number] > 1 else ""
        segment_id = f"NL{number}{suffix}"
        segments.append(
            NumberedNLSegment(
                segment_id=segment_id,
                source_number=number,
                ordinal=len(segments) + 1,
                text=value,
                raw_start=match.start("number"),
                raw_end=end,
                reason=boundary_reason,
                basis=algorithm_basis,
            )
        )
    if not segments and text.strip():
        segments.append(
            NumberedNLSegment(
                segment_id="NL1",
                source_number=1,
                ordinal=1,
                text=text.strip(),
                raw_start=0,
                raw_end=len(text),
                reason="No numbered marker was recoverable; the complete artifact is retained as one segment.",
                basis="nl-segmentation.v2 fallback; exact artifact preservation",
            )
        )
    return tuple(segments)


def build_exact_source_inventory(canonical: CanonicalSourceIR, canonical_hash: str) -> ExactSourceInventory:
    """Project canonical source IR into a small, exact, promptable inventory."""

    states = tuple(
        SourceInventoryState(
            source_id=item.id,
            name=item.label or item.id,
            kind=item.kind,
            parent=item.parent,
            raw_ref=item.raw_ref,
            line=_line_from_ref(item.raw_ref),
            reason="The row is copied from the canonical author-source state identity and raw reference.",
            basis="canonical source IR model.states",
        )
        for item in canonical.model.states
    )
    transitions = tuple(
        SourceInventoryTransition(
            transition_id=item.id,
            source=item.source,
            target=item.target,
            event=item.event or item.label,
            guard=item.guard,
            action=item.action,
            raw_ref=item.raw_ref,
            line=_line_from_ref(item.raw_ref),
            reason="The row is copied from the canonical author-source transition identity and raw reference.",
            basis="canonical source IR model.transitions",
        )
        for item in canonical.model.transitions
    )
    events = tuple(
        dict.fromkeys(
            item.event or item.label
            for item in canonical.model.transitions
            if (item.event or item.label)
        )
    )
    return ExactSourceInventory(
        schema_version="evidence-discovery.source-inventory.v1",
        algorithm_version="canonical-source-projection.v1",
        source_ir_hash=canonical_hash,
        states=states,
        transitions=transitions,
        events=events,
        reason="The method needs exact author-source locations and transition identities for grounding and attribution.",
        basis="canonical PlantUML source IR; source inventory is not the FCSTM execution model",
    )


def _endpoint_name(value: str) -> str:
    """Normalize only structural FCSTM endpoint markers, never free text."""

    normalized = value.strip().replace("[ * ]", "[*]")
    return normalized[1:] if normalized.startswith("!") else normalized


def _machine_scope(model: ModelIR) -> str | None:
    """Identify the optional outer FCSTM container used by representation exports."""

    for state in model.states:
        if state.parent is None and (
            any(child.parent == state.name for child in model.states)
            or any(item.scope == state.name for item in model.transitions)
        ):
            return state.name
    return None


def _resolve_state_ref(
    model: ModelIR,
    value: str,
    *,
    owner: str | None,
) -> str | None:
    """Resolve an endpoint within its exact declaration scope."""

    normalized = _endpoint_name(value)
    if normalized in {"[*]", ""}:
        return None
    matches = [
        state
        for state in model.states
        if state.parent == owner and state.name == normalized
    ]
    return matches[0].ref if len(matches) == 1 else None


def _hierarchical_graph_facts(
    model: ModelIR,
) -> tuple[
    str | None,
    dict[str, list[tuple[str | None, str]]],
    tuple[str, ...],
    dict[str, tuple[str, ...]],
    dict[str, tuple[str | None, str | None]],
    set[str],
]:
    """Resolve scoped transitions and traverse the finite hierarchy by refs.

    The representation exporter uses ``[*]`` for both machine and nested
    initial entries.  Transition scope captured by the owned parser keeps
    those entries separate.  The traversal also expands direct composite
    children when a composite state is entered, which records structural
    entry reachability without claiming a runtime scheduler or concurrency
    semantics.
    """

    machine_scope = _machine_scope(model)
    children: dict[str | None, list[str]] = {}
    for state in model.states:
        children.setdefault(state.parent, []).append(state.ref)
    composite_refs = {
        state.ref
        for state in model.states
        if any(child.parent == state.name for child in model.states)
    }

    def owner_for(item_scope: str | None) -> str | None:
        return machine_scope if item_scope == machine_scope else item_scope

    def resolve(value: str, owner: str | None) -> str | None:
        return _resolve_state_ref(model, value, owner=owner)

    def owner_ref(owner: str | None) -> str | None:
        if owner is None:
            return None
        matches = [state.ref for state in model.states if state.name == owner]
        return matches[0] if len(matches) == 1 else None

    edges: dict[str, list[tuple[str | None, str]]] = {
        state.ref: [] for state in model.states
    }
    root_targets: list[str] = []
    resolved_transitions: dict[str, tuple[str | None, str | None]] = {}
    for transition in model.transitions:
        owner = owner_for(transition.scope)
        if _endpoint_name(transition.source) == "[*]":
            target_ref = resolve(transition.target, owner)
            resolved_transitions[transition.ref] = (None, target_ref)
            if target_ref is not None:
                if owner is None or owner == machine_scope:
                    root_targets.append(target_ref)
                else:
                    enclosing_ref = owner_ref(owner)
                    if enclosing_ref is not None:
                        edges.setdefault(enclosing_ref, []).append((target_ref, transition.ref))
            continue
        source_ref = resolve(transition.source, owner)
        target_ref = resolve(transition.target, owner)
        resolved_transitions[transition.ref] = (source_ref, target_ref)
        if source_ref is not None:
            edges.setdefault(source_ref, []).append((target_ref, transition.ref))

    reachable: set[str] = set(root_targets)
    queue = list(root_targets)
    while queue:
        current = queue.pop(0)
        if current in composite_refs:
            current_name = next(state.name for state in model.states if state.ref == current)
            for child_ref in children.get(current_name, ()):
                if child_ref not in reachable:
                    reachable.add(child_ref)
                    queue.append(child_ref)
        for target_ref, _transition_ref in edges.get(current, ()):
            if target_ref is not None and target_ref not in reachable:
                reachable.add(target_ref)
                queue.append(target_ref)

    names = tuple(state.name for state in model.states if state.ref in reachable)
    reachability = {"[*]": names}
    return machine_scope, edges, tuple(dict.fromkeys(root_targets)), reachability, resolved_transitions, reachable


def build_inspection_equivalent_facts(model: ModelIR, fcstm_hash: str) -> InspectionEquivalentFacts:
    """Compute versioned inventory, scoped reachability, and event facts."""

    machine_scope, edges, _root_targets, reachability, resolved_transitions, reachable_refs = _hierarchical_graph_facts(model)

    outgoing: dict[str, list[str]] = {state.ref: [] for state in model.states}
    for source_ref, resolved_edges in edges.items():
        outgoing[source_ref].extend(
            transition_ref for _target_ref, transition_ref in resolved_edges
        )
    is_composite = {
        state.ref: any(child.parent == state.name for child in model.states)
        for state in model.states
    }
    diagnostics: list[InspectionDiagnostic] = []
    transitions: list[InspectionTransitionFact] = []
    for item in model.transitions:
        resolved_source_ref, resolved_target_ref = resolved_transitions.get(item.ref, (None, None))
        if _endpoint_name(item.source) != "[*]" and resolved_source_ref is None:
            diagnostics.append(
                InspectionDiagnostic(
                    code="FCSTM_SOURCE_UNRESOLVED",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message=f"Transition source {item.source!r} is not resolvable in its declared scope.",
                    reason="The scoped endpoint does not identify exactly one declared FCSTM state.",
                    basis="fcstm-line-parser.v2 scoped endpoint membership",
                )
            )
        if _endpoint_name(item.target) != "[*]" and resolved_target_ref is None:
            diagnostics.append(
                InspectionDiagnostic(
                    code="FCSTM_TARGET_UNRESOLVED",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message=f"Transition target {item.target!r} is not resolvable in its declared scope.",
                    reason="The scoped endpoint does not identify exactly one declared FCSTM state.",
                    basis="fcstm-line-parser.v2 scoped endpoint membership",
                )
            )
        if _endpoint_name(item.source) == "[*]" and (item.triggers or item.guard):
            diagnostics.append(
                InspectionDiagnostic(
                    code="INITIAL_ENTRY_CONDITIONAL",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message="An initial pseudostate transition carries a trigger or guard.",
                    reason="Initial-entry conditionality is a deterministic structural fact.",
                    basis="inspection-equivalent.initial-entry.v2 scoped transition",
                )
            )
        transitions.append(
            InspectionTransitionFact(
                transition_ref=item.ref,
                source=item.source,
                target=item.target,
                triggers=item.triggers,
                guard=item.guard,
                effects=item.effects,
                line=item.line,
                scope=item.scope,
                resolved_source_ref=resolved_source_ref,
                resolved_target_ref=resolved_target_ref,
                reachable_from_initial=bool(resolved_source_ref in reachable_refs),
                reason="The row preserves parser fields and exact scoped endpoint resolution.",
                basis="fcstm-line-parser.v2 plus inspection-equivalent hierarchical graph.v2",
            )
        )

    for state in model.states:
        if state.ref == machine_scope:
            continue
        if not is_composite[state.ref] and not outgoing.get(state.ref) and state.ref in reachable_refs:
            diagnostics.append(
                InspectionDiagnostic(
                    code="LEAF_WITHOUT_OUTGOING",
                    severity="warning",
                    refs=(state.ref,),
                    line=state.line,
                    message=f"Reachable leaf state {state.name!r} has no outgoing FCSTM transition.",
                    reason="The exact leaf is reachable in the finite hierarchical graph and has no outgoing transition.",
                    basis="inspection-equivalent.deadlock-frontier.v2 reachable leaf filter",
                )
            )
        if state.ref not in reachable_refs:
            diagnostics.append(
                InspectionDiagnostic(
                    code="STATE_UNREACHABLE_FROM_INITIAL",
                    severity="info",
                    refs=(state.ref,),
                    line=state.line,
                    message=f"State {state.name!r} is not reached from a top-level initial entry in the finite hierarchy.",
                    reason="Complete scoped traversal found no initial-entry path to this exact state ref.",
                    basis="inspection-equivalent.hierarchical-reachability.v2",
                )
            )

    declared_events = {event.name: event.ref for event in model.events}
    event_names = list(declared_events)
    for transition in model.transitions:
        for trigger in transition.triggers:
            if trigger not in event_names:
                event_names.append(trigger)
    event_consumers: list[EventConsumerFact] = []
    for event_name in event_names:
        consumer_rows = [item for item in transitions if event_name in item.triggers]
        consumer_refs = tuple(item.transition_ref for item in consumer_rows)
        consumer_states = tuple(
            dict.fromkeys(
                item.resolved_source_ref
                for item in consumer_rows
                if item.resolved_source_ref is not None
            )
        )
        reachable_consumer_refs = tuple(
            item.transition_ref
            for item in consumer_rows
            if item.resolved_source_ref in reachable_refs
        )
        reachable_consumer_states = tuple(
            dict.fromkeys(
                item.resolved_source_ref
                for item in consumer_rows
                if item.resolved_source_ref in reachable_refs
            )
        )
        event_consumers.append(
            EventConsumerFact(
                event=event_name,
                declared_ref=declared_events.get(event_name),
                consumer_transition_refs=consumer_refs,
                consumer_state_refs=consumer_states,
                reachable_consumer_transition_refs=reachable_consumer_refs,
                reachable_consumer_state_refs=reachable_consumer_states,
                reason="The row joins exact declared/trigger names with resolved transition source refs and finite reachability.",
                basis="fcstm-line-parser.v2 event trigger inventory plus hierarchical graph.v2",
            )
        )
        refs = consumer_refs or ((declared_events[event_name],) if event_name in declared_events else ())
        if not consumer_refs:
            diagnostics.append(
                InspectionDiagnostic(
                    code="EVENT_WITHOUT_CONSUMER",
                    severity="warning",
                    refs=refs,
                    message=f"Event {event_name!r} has no transition consumer in the closed model.",
                    reason="The exact event inventory contains no transition with this normalized trigger.",
                    basis="inspection-equivalent.event-consumer.v1",
                )
            )
        elif not reachable_consumer_refs:
            diagnostics.append(
                InspectionDiagnostic(
                    code="EVENT_CONSUMER_UNREACHABLE",
                    severity="warning",
                    refs=refs,
                    message=f"Event {event_name!r} has consumers but none is reachable from a top-level initial entry.",
                    reason="All exact consumer transition sources are outside the finite reachable state set.",
                    basis="inspection-equivalent.event-consumer.v1",
                )
            )

    state_facts = tuple(
        InspectionStateFact(
            state_ref=state.ref,
            name=state.name,
            parent=state.parent,
            line=state.line,
            is_composite=is_composite[state.ref],
            reachable_from_initial=state.ref in reachable_refs,
            outgoing_transition_refs=tuple(outgoing.get(state.ref, ())),
            reason="The row is computed from owned-parser declarations, scoped transitions, and finite entry traversal.",
            basis="fcstm-line-parser.v2 plus inspection-equivalent hierarchical graph.v2",
        )
        for state in model.states
    )
    reachability_names = tuple(
        state.name for state in model.states if state.ref in reachable_refs
    )
    metrics: dict[str, int | float] = {
        "state_count": len(model.states),
        "composite_state_count": sum(is_composite.values()),
        "event_count": len(event_names),
        "event_consumer_count": sum(bool(item.consumer_transition_refs) for item in event_consumers),
        "reachable_state_count": len(reachable_refs),
        "unreachable_state_count": len(model.states) - len(reachable_refs),
        "transition_count": len(model.transitions),
        "diagnostic_count": len(diagnostics),
        "reachable_node_count": len(reachable_refs),
        "guarded_transition_count": sum(1 for item in model.transitions if item.guard),
    }
    return InspectionEquivalentFacts(
        schema_version="evidence-discovery.inspection-equivalent.v2",
        algorithm_version="inspection-equivalent.fcstm-graph.v2",
        fcstm_hash=fcstm_hash,
        states=state_facts,
        transitions=tuple(transitions),
        events=tuple(event_names),
        diagnostics=tuple(diagnostics),
        reachability={"[*]": reachability_names},
        machine_root_ref=(
            next((state.ref for state in model.states if state.name == machine_scope and state.parent is None), None)
            if machine_scope
            else None
        ),
        reachable_state_refs=tuple(state.ref for state in model.states if state.ref in reachable_refs),
        event_consumers=tuple(event_consumers),
        metrics=metrics,
        reason="The method receives deterministic scoped inventory, reachability, and event-consumer facts without invoking Python inspect, pyfcstm.inspect, or legacy inspect backends.",
        basis="owned FCSTM scoped parser, exact endpoint resolution, hierarchical entry traversal, leaf filtering, and event coverage algorithm v2",
    )


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_FORMULA_KEYWORDS = {"and", "or", "not", "true", "false", "if", "else"}


def build_verification_facts(model: ModelIR, inspection: InspectionEquivalentFacts) -> VerificationFacts:
    """Summarize finite verification facts without claiming an external solver run."""

    checks: list[VerificationCheck] = []
    reachable_refs = set(inspection.reachable_state_refs)
    for state in inspection.states:
        if state.state_ref == inspection.machine_root_ref:
            continue
        is_reachable = state.state_ref in reachable_refs
        status = "proved" if is_reachable else "refuted"
        checks.append(
            VerificationCheck(
                check_id=f"reachability:{state.state_ref}",
                kind="reachability",
                status=status,
                subject_refs=(state.state_ref,),
                details={"state": state.name, "reachable_from_initial": is_reachable, "finite_scope": "closed_fcstm_hierarchy"},
                reason="Finite scoped traversal found the state from a top-level initial entry." if is_reachable else "The complete finite scoped traversal found no top-level initial-entry path to this exact state ref.",
                basis=inspection.algorithm_version,
            )
        )
    for transition in model.transitions:
        if transition.source.strip().replace("[ * ]", "[*]") == "[*]":
            checks.append(
                VerificationCheck(
                    check_id=f"initial-entry:{transition.ref}",
                    kind="initial_entry",
                    status="refuted" if transition.triggers or transition.guard else "proved",
                    subject_refs=(transition.ref,),
                    details={"has_trigger": bool(transition.triggers), "has_guard": bool(transition.guard), "scope": transition.scope},
                    reason="Initial-entry conditionality is directly determined from normalized transition fields.",
                    basis=inspection.algorithm_version,
                )
            )
    for state in inspection.states:
        if (
            state.state_ref != inspection.machine_root_ref
            and state.reachable_from_initial
            and not state.is_composite
            and not state.outgoing_transition_refs
        ):
            checks.append(
                VerificationCheck(
                    check_id=f"deadlock:{state.state_ref}",
                    kind="deadlock",
                    status="refuted",
                    subject_refs=(state.state_ref,),
                    details={"outgoing_count": 0},
                    reason="The exact reachable state is a finite leaf frontier with no outgoing transition in the closed model.",
                    basis=inspection.algorithm_version,
                )
            )
    for event in inspection.event_consumers:
        if not event.consumer_transition_refs:
            status = "refuted"
        elif event.reachable_consumer_transition_refs:
            status = "proved"
        else:
            status = "refuted"
        checks.append(
            VerificationCheck(
                check_id=f"event-consumer:{event.event}",
                kind="event_consumer",
                status=status,
                subject_refs=event.consumer_transition_refs or ((event.declared_ref,) if event.declared_ref else ()),
                details={
                    "event": event.event,
                    "consumer_transition_refs": list(event.consumer_transition_refs),
                    "reachable_consumer_transition_refs": list(event.reachable_consumer_transition_refs),
                },
                reason="Event consumer coverage is computed from exact trigger membership and finite source reachability; it is not an execution claim.",
                basis=event.basis,
            )
        )
    return VerificationFacts(
        schema_version="evidence-discovery.verify-facts.v2",
        algorithm_version="verify-equivalent.finite-graph.v2",
        scope="closed_fcstm_finite_graph",
        checks=tuple(checks),
        terminal_state="completed",
        reason="The method receives finite verification facts as structured context; they are not copied into W/D levels and do not replace backend execution.",
        basis="inspection-equivalent inventory and deterministic finite graph checks",
    )


def build_smt_facts(model: ModelIR) -> SMTFacts:
    """Build a bounded formula inventory with an explicit no-solver boundary."""

    formulas: list[SMTFormulaFact] = []
    for transition in model.transitions:
        if not transition.guard:
            continue
        variables = tuple(
            dict.fromkeys(
                token
                for token in _IDENTIFIER_RE.findall(transition.guard)
                if token.lower() not in _FORMULA_KEYWORDS
            )
        )
        formulas.append(
            SMTFormulaFact(
                formula_id=f"guard:{transition.ref}",
                source_ref=transition.ref,
                expression=transition.guard,
                variables=variables,
                solver_status="not_run",
                reason="The guard is retained as a normalized bounded-verification input, not evaluated by this summary builder.",
                basis="fcstm-line-parser.v2 guard normalization",
            )
        )
    return SMTFacts(
        schema_version="evidence-discovery.smt-facts.v1",
        algorithm_version="smt-input-normalization.v1",
        scope="closed_fcstm_guard_fragment",
        formulas=tuple(formulas),
        solver_status="not_run",
        reason="This summary preserves formal-program inputs and makes the solver boundary explicit; unknown is never promoted to violation or W2.",
        basis="owned FCSTM guard fields; no pyfcstm.inspect, legacy inspect backend, or hidden solver result is used",
    )


def _artifact_hash_payload(payload: dict[str, Any]) -> str:
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _project_large_sequence(value: Any, *, label: str) -> dict[str, Any]:
    """Keep a deterministic receipt for a repetitive contract sequence."""

    if not isinstance(value, (list, tuple, dict, str)):
        value = []
    if isinstance(value, (list, tuple)):
        json_value: Any = [
            item.model_dump(mode="json") if isinstance(item, BaseModel) else item
            for item in value
        ]
    else:
        json_value = value
    count = len(json_value)
    return {
        "count": count,
        "sha256": _artifact_hash_payload({"items": json_value}),
        "label": label,
        "reason": "The complete sequence remains available through the hash-addressed artifact; only a repetition receipt is prompt-visible.",
        "basis": "stage-context-projection.v2 repetitive-sequence omission",
    }


def _compact_fact_rows(
    rows: Any,
    *,
    fields: tuple[str, ...],
    label: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Project typed fact rows while hash-addressing repeated audit rationale."""

    raw_rows = [
        row.model_dump(mode="json") if isinstance(row, BaseModel) else row
        for row in (rows or ())
        if isinstance(row, (BaseModel, dict))
    ]
    projected = [
        {key: row[key] for key in fields if key in row}
        for row in raw_rows
    ]
    receipt = {
        "count": len(raw_rows),
        "sha256": _artifact_hash_payload({"items": raw_rows}),
        "omitted_fields": ["reason", "basis"],
        "label": label,
        "reason": "Typed fact fields remain prompt-visible; repeated per-row audit rationale remains in the hash-addressed complete artifact.",
        "basis": "stage-context-projection.v6 typed-fact projection",
    }
    return projected, receipt


def _inspection_equivalent_prompt_dict(
    facts: InspectionEquivalentFacts | None,
) -> dict[str, Any] | None:
    """Keep the complete owned inventory semantics without repeated row prose."""

    if facts is None:
        return None
    states, state_receipt = _compact_fact_rows(
        facts.states,
        fields=(
            "state_ref",
            "name",
            "parent",
            "line",
            "is_composite",
            "reachable_from_initial",
            "outgoing_transition_refs",
        ),
        label="inspection_equivalent_facts.states",
    )
    transitions, transition_receipt = _compact_fact_rows(
        facts.transitions,
        fields=(
            "transition_ref",
            "source",
            "target",
            "triggers",
            "guard",
            "effects",
            "line",
            "scope",
            "resolved_source_ref",
            "resolved_target_ref",
            "reachable_from_initial",
        ),
        label="inspection_equivalent_facts.transitions",
    )
    diagnostics, diagnostic_receipt = _compact_fact_rows(
        facts.diagnostics,
        fields=("code", "severity", "refs", "line", "message"),
        label="inspection_equivalent_facts.diagnostics",
    )
    event_consumers, consumer_receipt = _compact_fact_rows(
        facts.event_consumers,
        fields=(
            "event",
            "declared_ref",
            "consumer_transition_refs",
            "consumer_state_refs",
            "reachable_consumer_transition_refs",
            "reachable_consumer_state_refs",
        ),
        label="inspection_equivalent_facts.event_consumers",
    )
    return {
        "schema_version": facts.schema_version,
        "algorithm_version": facts.algorithm_version,
        "fcstm_hash": facts.fcstm_hash,
        "states": states,
        "transitions": transitions,
        "events": facts.events,
        "diagnostics": diagnostics,
        "reachability": facts.reachability,
        "machine_root_ref": facts.machine_root_ref,
        "reachable_state_refs": facts.reachable_state_refs,
        "event_consumers": event_consumers,
        "metrics": facts.metrics,
        "row_rationale_receipts": {
            "states": state_receipt,
            "transitions": transition_receipt,
            "diagnostics": diagnostic_receipt,
            "event_consumers": consumer_receipt,
        },
        "reason": facts.reason,
        "basis": facts.basis,
    }


def _verification_facts_prompt_dict(
    facts: VerificationFacts | None,
) -> dict[str, Any] | None:
    """Project finite check results and exact subjects without row-level repetition."""

    if facts is None:
        return None
    checks, receipt = _compact_fact_rows(
        facts.checks,
        fields=("check_id", "kind", "status", "subject_refs", "details"),
        label="verify_facts.checks",
    )
    non_proved = [row for row in checks if row.get("status") != "proved"]
    proved_index = [
        {
            key: row[key]
            for key in ("check_id", "kind", "subject_refs")
            if key in row
        }
        for row in checks
        if row.get("status") == "proved"
    ]
    return {
        "schema_version": facts.schema_version,
        "algorithm_version": facts.algorithm_version,
        "scope": facts.scope,
        "checks": {
            "non_proved": non_proved,
            "proved_index": proved_index,
            "count": len(checks),
            "sha256": receipt["sha256"],
            "reason": "Non-proved finite results retain their full structured details; proved rows retain exact check and subject identity because their underlying positive facts are already present in the owned inspection inventory.",
            "basis": "verify-facts-prompt-projection.v2",
        },
        "terminal_state": facts.terminal_state,
        "row_rationale_receipt": receipt,
        "reason": facts.reason,
        "basis": facts.basis,
    }


def _smt_facts_prompt_dict(facts: SMTFacts | None) -> dict[str, Any] | None:
    """Project normalized formulas while preserving the explicit no-solver boundary."""

    if facts is None:
        return None
    formulas, receipt = _compact_fact_rows(
        facts.formulas,
        fields=("formula_id", "source_ref", "expression", "variables", "solver_status"),
        label="smt_facts.formulas",
    )
    return {
        "schema_version": facts.schema_version,
        "algorithm_version": facts.algorithm_version,
        "scope": facts.scope,
        "formulas": formulas,
        "solver_status": facts.solver_status,
        "row_rationale_receipt": receipt,
        "reason": facts.reason,
        "basis": facts.basis,
    }


def _compact_trace_entries(entries: Any, *, label: str) -> dict[str, Any]:
    """Retain exact trace edges without repeating uniform relation metadata."""

    if not isinstance(entries, list):
        entries = []
    raw_rows = [
        {
            key: row[key]
            for key in (
                "trace_id",
                "trace_class",
                "trace_dimension",
                "trace_relation",
                "source_elements",
                "intermediate_elements",
                "trace_evidence",
                "projection_status",
            )
            if isinstance(row, dict) and key in row
        }
        for row in entries
        if isinstance(row, dict)
    ]
    uniform_fields: dict[str, Any] = {}
    for key in (
        "trace_class",
        "trace_dimension",
        "trace_relation",
        "projection_status",
    ):
        values = {json.dumps(row.get(key), sort_keys=True) for row in raw_rows}
        if len(values) == 1 and raw_rows:
            uniform_fields[key] = raw_rows[0].get(key)
    edges = [
        {
            key: row[key]
            for key in (
                "trace_id",
                "source_elements",
                "intermediate_elements",
                "trace_evidence",
                "trace_class",
                "trace_dimension",
                "trace_relation",
                "projection_status",
            )
            if key in row
            and key not in uniform_fields
            and not (key == "trace_evidence" and not row[key])
        }
        for row in raw_rows
    ]
    return {
        "common_relation": uniform_fields,
        "edges": edges,
        "count": len(entries),
        "sha256": _artifact_hash_payload({"items": entries}),
        "omitted_fields": [
            "attribution_boundary",
            "behavioral_fidelity",
            "issue_binding_policy",
            "reviewer_notes",
            "trace_relation_rationale",
        ],
        "reason": "Exact source/intermediate identity edges remain prompt-visible while uniform relation fields are stated once; repeated policy prose remains in the source-trace hash.",
        "basis": f"{label}.v3",
    }


def _canonical_source_prompt_dict(canonical: Any) -> dict[str, Any] | None:
    """Project canonical source IR to exact identity rows plus metadata receipts.

    Source grounding needs authored state/transition identity and raw locations.
    Large adapter metadata is retained by the canonical artifact hash and does
    not belong in every grounding prompt.
    """

    if canonical is None:
        return None
    model = canonical.model
    inventory_payload = {
        "states": [item.model_dump(mode="json") for item in model.states],
        "transitions": [
            item.model_dump(mode="json") for item in model.transitions
        ],
    }
    return {
        "projection_version": "canonical-source-prompt-projection.v4",
        "source_format": canonical.source_format,
        "conversion_status": canonical.status,
        "model": {
            "hierarchy_level": model.hierarchy_level,
            "timing_level": model.timing_level,
            "initial_states": list(model.initial_states),
            "final_states": list(model.final_states),
            "concurrent_regions": _project_large_sequence(model.concurrent_regions, label="canonical.concurrent_regions"),
            "variables": _project_large_sequence(model.variables, label="canonical.variables"),
            "inventory_receipt": {
                "state_count": len(model.states),
                "transition_count": len(model.transitions),
                "sha256": _artifact_hash_payload(inventory_payload),
                "projection": "Exact source rows are supplied once in exact_source_inventory; this canonical IR section retains model-level semantics and the hash of its complete row inventory.",
            },
        },
        "metadata": _project_large_sequence(canonical.metadata, label="canonical.metadata"),
        "reason": "Exact authored state and transition identities are prompt-visible for source localization; adapter metadata remains hash-addressed.",
        "basis": "canonical-source-prompt-projection.v3",
    }


def _exact_source_inventory_prompt_dict(inventory: Any) -> dict[str, Any] | None:
    """Expose complete exact source rows once, without repeated row rationale."""

    if inventory is None:
        return None
    states, state_receipt = _compact_fact_rows(
        inventory.states,
        fields=("source_id", "name", "kind", "parent", "raw_ref", "line"),
        label="exact_source_inventory.states",
    )
    transitions, transition_receipt = _compact_fact_rows(
        inventory.transitions,
        fields=(
            "transition_id",
            "source",
            "target",
            "event",
            "guard",
            "action",
            "raw_ref",
            "line",
        ),
        label="exact_source_inventory.transitions",
    )
    return {
        "schema_version": inventory.schema_version,
        "algorithm_version": inventory.algorithm_version,
        "source_ir_hash": inventory.source_ir_hash,
        "states": states,
        "transitions": transitions,
        "events": inventory.events,
        "row_rationale_receipts": {
            "states": state_receipt,
            "transitions": transition_receipt,
        },
        "reason": inventory.reason,
        "basis": inventory.basis,
    }


def _owned_model_ir_prompt_dict(model: Any) -> dict[str, Any]:
    """Project owned ModelIR identity while inspection facts carry parsed rows."""

    payload = model.to_dict()
    return {
        "algorithm_version": model.algorithm_version,
        "source_hash": payload.get("source_hash"),
        "full_model_ir_hash": _artifact_hash_payload(payload),
        "state_refs": [item.ref for item in model.states],
        "events": [
            {"ref": item.ref, "name": item.name, "line": item.line}
            for item in model.events
        ],
        "transition_refs": [item.ref for item in model.transitions],
        "inventory_projection": "Exact parsed state/transition fields are supplied once in inspection_equivalent_facts; raw syntax remains in fcstm_model.text.",
        "reason": "The owned parser identity and complete ref inventory remain prompt-visible without duplicating every parsed row.",
        "basis": "owned-model-ir-prompt-projection.v2",
    }


def _source_trace_prompt_dict(artifact: StructuredArtifact | None) -> dict[str, Any] | None:
    """Keep exact trace entries while collapsing repetitive exclusion indexes."""

    if artifact is None:
        return None
    payload = artifact.payload
    projected: dict[str, Any] = {
        key: payload[key]
        for key in (
            "schema_version",
            "trace_scope",
            "relation_policy",
            "notes",
            "boundary_entries",
            "entries",
            "source_traceability",
        )
        if key in payload
    }
    if "entries" in projected:
        projected["entries"] = _compact_trace_entries(
            projected["entries"], label="source-trace.entries"
        )
    if "attribution_exclusions" in payload:
        projected["attribution_exclusions"] = _project_large_sequence(
            payload["attribution_exclusions"], label="source_trace.attribution_exclusions"
        )
    return {
        "ref": _artifact_prompt_ref(artifact.ref),
        "payload": projected,
        "reason": "Exact source-trace entries remain available for author attribution; repetitive exclusion indexes are represented by count/hash.",
        "basis": "source-trace-prompt-projection.v2",
    }


def _working_contract_prompt_dict(
    artifact: StructuredArtifact | None,
    *,
    include_elements: bool,
    include_source_trace: bool = True,
    include_review_subject: bool = True,
) -> dict[str, Any] | None:
    """Project the working contract while retaining exact mapping and omission receipts.

    The published working contract contains large eligibility exclusion lists and
    compiler-owned metadata. Source/model grounding needs the exact element
    mapping, but no stage needs every repeated exclusion string. The omitted
    sequences remain hash-addressed and available from the artifact path in the
    manifest, so this projection reduces context pressure without changing the
    input closure or silently changing a fact.
    """

    if artifact is None:
        return None
    payload = artifact.payload
    fixed_keys = (
        "artifact_role",
        "input_identity",
        "summary",
        "usage_gate",
        "inventory_digests",
    )
    if include_source_trace:
        fixed_keys += ("source_trace_base",)
    if include_review_subject:
        fixed_keys += ("review_subject",)
    projected: dict[str, Any] = {
        key: payload[key]
        for key in fixed_keys
        if key in payload
    }
    if isinstance(payload.get("ownership_policy"), dict):
        projected["ownership_policy"] = {
            key: payload["ownership_policy"][key]
            for key in ("agent_edit_policy", "compiler_member_policy", "origins")
            if key in payload["ownership_policy"]
        }
    if isinstance(payload.get("attribution_policy"), dict):
        projected["attribution_policy"] = {
            key: value
            for key, value in payload["attribution_policy"].items()
            if key != "policy_id"
        }
    for key in ("source_trace_base", "review_subject"):
        if key in projected:
            value = projected[key]
            if key == "source_trace_base" and isinstance(value, dict):
                projected[key] = {
                    subkey: value[subkey]
                    for subkey in (
                        "schema_version",
                        "trace_scope",
                        "relation_policy",
                        "notes",
                        "boundary_entries",
                        "entries",
                        "source_traceability",
                    )
                    if subkey in value
                }
                if "entries" in projected[key]:
                    projected[key]["entries"] = _compact_trace_entries(
                        projected[key]["entries"],
                        label="working-contract.source_trace_base.entries",
                    )
                if "attribution_exclusions" in value:
                    projected[key]["attribution_exclusions"] = _project_large_sequence(
                        value["attribution_exclusions"],
                        label="working_contract.source_trace_base.attribution_exclusions",
                    )
            elif key == "review_subject" and isinstance(value, dict):
                obligations = value.get("review_obligations", [])
                projected[key] = {
                    subkey: value[subkey]
                    for subkey in ("schema_version", "subject", "reason", "basis")
                    if subkey in value
                }
                projected[key]["review_obligations"] = [
                    {
                        subkey: row[subkey]
                        for subkey in (
                            "obligation_id",
                            "element_ids",
                            "source_refs",
                            "risk_tag",
                            "rationale",
                        )
                        if isinstance(row, dict) and subkey in row
                    }
                    for row in obligations
                    if isinstance(row, dict)
                ]
    if include_elements:
        elements = [
            item for item in payload.get("elements", []) if isinstance(item, dict)
        ]
        projected["elements"] = {
            "source_to_model": [
                {
                    "source_element": item.get("element_id"),
                    "model_refs": item.get("model_refs", []),
                }
                for item in elements
                if item.get("origin") == "source_owned"
            ],
            "compiler_owned": [
                {
                    "element_id": item.get("element_id"),
                    "kind": item.get("kind"),
                    "model_refs": item.get("model_refs", []),
                }
                for item in elements
                if item.get("origin") != "source_owned"
            ],
            "count": len(elements),
            "sha256": _artifact_hash_payload({"items": elements}),
            "source_ref_join": "Join source_element to exact_source_inventory.source_id/raw_ref; source refs are not repeated in this mapping table.",
        }
        projected["element_omitted_fields"] = {
            "fields": ["field_ownership", "metadata", "semantic_fields", "macro_ids", "edit_policy"],
            "count": len(elements),
            "sha256": _artifact_hash_payload(
                {
                    "items": [
                        {
                            "element_id": item.get("element_id"),
                            "field_ownership": item.get("field_ownership"),
                            "metadata": item.get("metadata"),
                            "semantic_fields": item.get("semantic_fields"),
                        }
                        for item in payload.get("elements", [])
                        if isinstance(item, dict)
                    ]
                }
            ),
            "reason": "Exact source/model refs are retained for binding; verbose compiler metadata remains available from the working-contract artifact hash.",
            "basis": "working-contract-prompt-projection.v6",
        }
    else:
        projected["elements"] = _project_large_sequence(payload.get("elements"), label="elements")
    if "macros" in payload:
        # Macro membership is useful as an audit identity, but the full member
        # lists duplicate the exact transition inventory and inflate every
        # grounding prompt.  Keep a deterministic count/hash projection here;
        # the complete macro payload remains in the hash-addressed artifact.
        projected["macros"] = _project_large_sequence(
            payload["macros"], label="macros"
        )

    eligibility: dict[str, Any] = {}
    raw_eligibility = payload.get("capability_eligibility", {})
    if isinstance(raw_eligibility, dict):
        for name, value in raw_eligibility.items():
            if not isinstance(value, dict):
                eligibility[name] = value
                continue
            eligibility[name] = {
                key: value[key]
                for key in ("claim_boundary", "status")
                if key in value
            }
    projected["capability_eligibility"] = eligibility
    projected["capability_eligibility_detail_receipt"] = {
        "capability_count": len(raw_eligibility) if isinstance(raw_eligibility, dict) else 0,
        "sha256": _artifact_hash_payload({"items": raw_eligibility}),
        "omitted_fields": [
            "reason_codes",
            "eligible_element_ids",
            "eligible_field_refs",
            "evidence_refs",
            "excluded_element_ids",
            "excluded_field_refs",
        ],
        "reason": "Capability status and claim boundaries remain visible; repeated eligibility ID lists remain in the complete working-contract artifact.",
        "basis": "working-contract-prompt-projection.v6",
    }
    for key in ("diagnostic_attribution", "confirm_gate", "repair_gate"):
        if key in payload:
            projected[f"{key}_receipt"] = {
                "sha256": _artifact_hash_payload({"value": payload[key]}),
                "reason": "This generation/review policy remains in the complete working-contract artifact and is not duplicated in discovery grounding.",
                "basis": "working-contract-prompt-projection.v5",
            }
    return {
        "ref": _artifact_prompt_ref(artifact.ref),
        "payload": projected,
        "reason": "The working contract projection preserves exact source/model mapping and hash-addresses omitted compiler and eligibility expansions.",
        "basis": "working-contract-prompt-projection.v5",
    }


def _prompt_base(pair: Any, stage: PromptStage) -> dict[str, Any]:
    """Build common stage context with every artifact receipt and source-role boundary."""

    if pair.context_manifest is None:
        raise ValueError("stage prompt requires a complete context manifest")
    manifest = pair.context_manifest
    return {
        "prompt_projection_version": "stage-context-projection.v7",
        "stage": stage,
        "context_manifest": {
            "schema_version": manifest.schema_version,
            "protocol_version": manifest.protocol_version,
            "pair_id": manifest.pair_id,
            "manifest_hash": manifest.manifest_hash,
            "artifact_count": len(manifest.artifacts),
            "sections": [item.model_dump(mode="json") for item in manifest.sections],
            "forbidden_inputs": list(manifest.forbidden_inputs),
            "reason": "The complete manifest is retained in the method receipt; this prompt identity is joined to the exact artifact refs below.",
            "basis": "context-manifest-prompt-projection.v2",
        },
        "artifact_refs": [
            {
                key: value
                for key, value in item.model_dump(mode="json").items()
                if key
                in {
                    "role",
                    "source_role",
                    "sha256",
                    "schema_version",
                    "algorithm_version",
                    "producer",
                    "prompt_included",
                }
            }
            for item in pair.context_manifest.artifacts
        ],
        "case_report": case_report_prompt_dict(pair.case_report),
        "source_roles": {
            "plantuml_source": "author_source_localization_only",
            "canonical_source_ir": "author_source_localization_only",
            "exact_source_inventory": "author_source_inventory",
            "fcstm_model": "closed_model_binding_and_execution",
            "working_contract": "mapping_and_eligibility_contract",
            "source_trace": "source_attribution_boundary",
            "reference_inspection_facts": "read_only_reference_deterministic_facts",
            "inspection_equivalent_facts": "owned_deterministic_inventory_and_diagnostics",
            "verify_facts": "owned_deterministic_finite_verification_summary",
            "smt_facts": "normalized_formal_inputs_not_solver_result",
        },
        "reason": "Stage context is role-scoped while the complete artifact closure remains identified by the manifest.",
        "basis": "context-manifest.v1 and stage-context-projection.v7",
    }


def prompt_context_payload(pair: Any, *, stage: PromptStage) -> dict[str, Any]:
    """Return the stage-specific prompt closure without duplicating unrelated raw artifacts.

    Every stage receives the complete manifest, hashes, versions, and role policy.
    The two complementary discovery lenses receive the same compact cross-view
    payload. Source and closed-model roles remain explicit inside that payload;
    neither lens receives a different semantic protocol or a silently incomplete
    half of the method input closure.
    """

    payload = _prompt_base(pair, stage)
    payload["input_hashes"] = dict(pair.hashes)
    if stage == "nl_contract_extraction":
        payload.update(
            {
                "numbered_nl": [
                    item.model_dump(mode="json")
                    for item in pair.nl_segments
                ],
                "working_contract": _working_contract_prompt_dict(
                    pair.working_contract,
                    include_elements=False,
                    include_source_trace=False,
                    include_review_subject=False,
                ),
                "source_trace_receipt": (
                    _artifact_prompt_ref(pair.source_trace.ref)
                    if pair.source_trace
                    else None
                ),
            }
        )
    elif stage == "discovery_grounding":
        payload.update(
            {
                "numbered_nl": [
                    item.model_dump(mode="json")
                    for item in pair.nl_segments
                ],
                "plantuml_source": {
                    "role": "author_source",
                    "sha256": pair.hashes.get("plantuml"),
                    "text": pair.plantuml_text,
                    "reason": "PlantUML is supplied for author-source localization only.",
                    "basis": "source-role separation contract",
                },
                "canonical_source_ir": _canonical_source_prompt_dict(pair.canonical_source_ir),
                "exact_source_inventory": _exact_source_inventory_prompt_dict(
                    pair.exact_source_inventory
                ),
                "working_contract": _working_contract_prompt_dict(
                    pair.working_contract,
                    include_elements=True,
                    include_source_trace=False,
                    include_review_subject=False,
                ),
                "source_trace": _source_trace_prompt_dict(pair.source_trace),
                "fcstm_model": {
                    "role": "closed_model",
                    "sha256": pair.hashes.get("fcstm"),
                    "text": pair.fcstm_text,
                    "model_ir": _owned_model_ir_prompt_dict(pair.model),
                    "reason": "FCSTM is the closed model evaluated by the new deterministic backends.",
                    "basis": pair.model.algorithm_version,
                },
                "reference_inspection_facts": (
                    reference_inspection_prompt_dict(pair.reference_inspection)
                    if pair.reference_inspection
                    else None
                ),
                "inspection_equivalent_facts": (
                    _inspection_equivalent_prompt_dict(pair.inspection_facts)
                ),
                "verify_facts": (
                    _verification_facts_prompt_dict(pair.verify_facts)
                ),
                "smt_facts": (
                    _smt_facts_prompt_dict(pair.smt_facts)
                ),
            }
        )
    elif stage == "d_adjudication":
        payload["dossier_input_policy"] = {
            "source_and_model_facts": "supplied in the obligation dossiers",
            "evaluation_ground_truth": "forbidden",
            "evaluation_scores": "forbidden",
            "reviewer_examples": "forbidden",
            "reason": "D receives exact candidate dossiers and closure identity, not a second copy of raw source artifacts.",
            "basis": "dossier-bound semantic adjudication boundary",
        }
    else:  # pragma: no cover - PromptStage is a closed literal
        raise ValueError(f"unsupported prompt stage: {stage}")
    return payload


def build_context_manifest(
    *,
    pair_id: str,
    artifacts: tuple[ArtifactRef, ...],
) -> ContextManifest:
    """Create a deterministic manifest and hash it after excluding its hash field."""

    sections = (
        PromptSection(
            section_id="nl-contract",
            artifact_roles=("natural_language", "working_contract", "source_trace"),
            purpose="Extract numbered source obligations without looking at model satisfaction or evaluation ground truth.",
            excluded_claims=("model_violation", "evaluation_score", "reviewer_match"),
            reason="The contract stage is source-first.",
            basis="frozen method information-flow boundary",
        ),
        PromptSection(
            section_id="source-grounding",
            artifact_roles=("plantuml_source", "canonical_source_ir", "source_inventory", "source_trace", "working_contract"),
            purpose="Locate author-source states, transitions, mappings, and source-scoped obligations.",
            excluded_claims=("fcstm_execution_verdict", "evaluation_ground_truth", "evaluation_score"),
            reason="PlantUML and canonical IR are author-source evidence only.",
            basis="source-role separation contract",
        ),
        PromptSection(
            section_id="model-grounding",
            artifact_roles=("fcstm_model", "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts"),
            purpose="Bind exact closed-model elements and plan deterministic predicate checks.",
            excluded_claims=("author_source_identity", "evaluation_ground_truth", "reviewer_example"),
            reason="FCSTM is the tested closed model; deterministic facts are context, not semantic verdicts.",
            basis="closed-model execution contract",
        ),
    )
    forbidden = (
        "evaluation ground truth and external labels",
        "evaluation scores or error classifications",
        "reviewer examples or outputs",
        "artifacts from other evaluation cases",
        "previously generated reports",
    )
    base = {
        "schema_version": "evidence-discovery.context-manifest.v1",
        "protocol_version": "typed-input-closure-plus-four-family-19.v3",
        "pair_id": pair_id,
        "artifacts": [item.model_dump(mode="json") for item in artifacts],
        "sections": [item.model_dump(mode="json") for item in sections],
        "forbidden_inputs": list(forbidden),
        "reason": "The method and grounding branches must receive the full source/model/fact closure while remaining independent of evaluation answers.",
        "basis": "frozen input artifacts plus owned evidence-discovery deterministic fact algorithms",
    }
    return ContextManifest(
        **base,
        manifest_hash=_artifact_hash_payload(base),
    )


def build_artifact_ref(
    *,
    role: ArtifactRole,
    source_role: SourceRole,
    path: Path,
    sha256: str,
    schema_version: str,
    algorithm_version: str,
    producer: str,
    prompt_included: bool = True,
    reason: str,
    basis: str,
) -> ArtifactRef:
    """Build a validated artifact reference for a file or generated payload."""

    return ArtifactRef(
        role=role,
        source_role=source_role,
        path=str(path.resolve()),
        sha256=sha256,
        schema_version=schema_version,
        algorithm_version=algorithm_version,
        producer=producer,
        prompt_included=prompt_included,
        reason=reason,
        basis=basis,
    )


def generated_artifact(
    *,
    role: ArtifactRole,
    source_role: SourceRole,
    path: Path,
    payload: BaseModel,
    schema_version: str,
    algorithm_version: str,
    producer: str,
    reason: str,
    basis: str,
) -> StructuredArtifact:
    """Wrap an owned generated fact model as a promptable structured artifact."""

    data = payload.model_dump(mode="json")
    return StructuredArtifact(
        ref=build_artifact_ref(
            role=role,
            source_role=source_role,
            path=path,
            sha256=_artifact_hash_payload(data),
            schema_version=schema_version,
            algorithm_version=algorithm_version,
            producer=producer,
            reason=reason,
            basis=basis,
        ),
        payload=data,
    )


def file_artifact(
    *,
    role: ArtifactRole,
    source_role: SourceRole,
    path: Path,
    payload: dict[str, Any],
    sha256: str,
    schema_version: str,
    algorithm_version: str,
    producer: str,
    reason: str,
    basis: str,
) -> StructuredArtifact:
    """Wrap a published JSON artifact after reading its exact bytes."""

    return StructuredArtifact(
        ref=build_artifact_ref(
            role=role,
            source_role=source_role,
            path=path,
            sha256=sha256,
            schema_version=schema_version,
            algorithm_version=algorithm_version,
            producer=producer,
            reason=reason,
            basis=basis,
        ),
        payload=payload,
    )


def context_payload(pair: Any) -> dict[str, Any]:
    """Return the complete method-visible closure with explicit source roles."""

    def artifact(value: StructuredArtifact | None) -> dict[str, Any] | None:
        return value.to_prompt_dict() if value is not None else None

    return {
        "context_manifest": pair.context_manifest.model_dump(mode="json"),
        "numbered_nl": [item.model_dump(mode="json") for item in pair.nl_segments],
        "plantuml_source": {
            "role": "author_source",
            "path": str(pair.pair_dir / "plantuml.puml"),
            "sha256": pair.hashes.get("plantuml"),
            "text": pair.plantuml_text,
            "reason": "PlantUML is supplied for author-source localization only.",
            "basis": "source-role separation contract",
        },
        "fcstm_model": {
            "role": "closed_model",
            "path": str(pair.pair_dir / "fcstm.fcstm"),
            "sha256": pair.hashes.get("fcstm"),
            "text": pair.fcstm_text,
            "model_ir": pair.model.to_dict(),
            "reason": "FCSTM is the closed model evaluated by the new deterministic backends.",
            "basis": pair.model.algorithm_version,
        },
        "canonical_source_ir": pair.canonical_source_ir.model_dump(mode="json") if pair.canonical_source_ir else None,
        "exact_source_inventory": pair.exact_source_inventory.model_dump(mode="json"),
        "working_contract": artifact(pair.working_contract),
        "source_trace": artifact(pair.source_trace),
        "case_report": case_report_prompt_dict(pair.case_report),
        "reference_inspection_facts": artifact(pair.reference_inspection),
        "inspection_equivalent_facts": pair.inspection_facts.model_dump(mode="json"),
        "verify_facts": pair.verify_facts.model_dump(mode="json"),
        "smt_facts": pair.smt_facts.model_dump(mode="json"),
        "reason": "All sections are method-visible context; no evaluation ground truth, scores, reviewer output, or prior generated report is included.",
        "basis": "context-manifest.v1 and frozen pair artifact closure",
    }
