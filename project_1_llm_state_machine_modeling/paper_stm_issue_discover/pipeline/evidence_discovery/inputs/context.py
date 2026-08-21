"""Typed input closure and deterministic inspection-equivalent facts.

This module is deliberately independent from ``pyfcstm`` and from the legacy
feedback-loop inspection helpers.  It reads already published representation
artifacts as facts, and computes the small closed-world inventory needed by the
new evidence method with algorithms owned by this package.
"""

from __future__ import annotations

import hashlib
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
    "source_grounding",
    "model_grounding",
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


class StructuredArtifact(BaseModel):
    """JSON artifact together with its immutable provenance reference."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    ref: ArtifactRef = Field(description="Versioned provenance reference for the JSON artifact.")
    payload: dict[str, Any] = Field(description="Parsed JSON object supplied as structured context; it is never treated as an execution result by itself.")

    def to_prompt_dict(self) -> dict[str, Any]:
        """Return the complete structured payload while retaining its receipt reference."""

        return {"ref": self.ref.model_dump(mode="json"), "payload": self.payload}


_CASE_REPORT_PROMPT_FIELDS = (
    "schema_version",
    "case_id",
    "pair_id",
    "pair_index",
    "canonical_sha256",
    "fcstm_sha256",
    "parse_inspect_sha256",
    "source_trace_sha256",
    "working_contract_sha256",
    "source_sha256",
    "selected_stage",
    "official_raw_status",
    "official_validation_status",
    "is_phase_i_fallback",
    "phase_i_changed",
)


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
        key: artifact.payload[key]
        for key in _CASE_REPORT_PROMPT_FIELDS
        if key in artifact.payload
    }
    return {
        "ref": artifact.ref.model_dump(mode="json"),
        "payload": payload,
        "reason": "Only case identity and artifact status are prompt-visible; historical run outputs are receipt-only.",
        "basis": "case-report prompt projection v1",
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


class CanonicalModel(BaseModel):
    """Typed source model portion of the canonical PlantUML IR."""

    model_config = ConfigDict(extra="allow", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Canonical source model name.")
    hierarchy_level: str = Field(default="unknown", description="Canonical hierarchy classification.")
    timing_level: str = Field(default="unknown", description="Canonical timing classification; unknown is preserved rather than inferred.")
    initial_states: tuple[str, ...] = Field(default_factory=tuple, description="Canonical initial state identities.")
    final_states: tuple[str, ...] = Field(default_factory=tuple, description="Canonical explicit final state identities.")
    concurrent_regions: tuple[dict[str, Any], ...] = Field(default_factory=tuple, description="Canonical concurrent-region facts, if any.")
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
    reason: str = Field(min_length=1, description="Why this is a deterministic inventory fact.")
    basis: str = Field(min_length=1, description="Owned FCSTM parser fields used for this row.")


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
    metrics: dict[str, int | float] = Field(default_factory=dict, description="Deterministic inventory metrics such as state and transition counts.")
    reason: str = Field(min_length=1, description="Why these facts are supplied to method/grounding.")
    basis: str = Field(min_length=1, description="Owned parser and inspection-equivalent algorithm basis.")


class VerificationCheck(BaseModel):
    """One finite closed-model verification fact."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    check_id: str = Field(min_length=1, description="Stable deterministic verification check identifier.")
    kind: Literal["reachability", "initial_entry", "deadlock", "guard_inventory"] = Field(description="Verification fact family.")
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
    forbidden_inputs: tuple[str, ...] = Field(min_length=1, description="Data classes excluded from method generation, including ledger answers, baseline hits, and judge examples.")
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
            concurrent_regions=tuple(value for value in model_payload.get("concurrent_regions", ()) if isinstance(value, dict)),
            variables=tuple(value for value in model_payload.get("variables", ()) if isinstance(value, dict)),
            states=tuple(CanonicalState.model_validate(value) for value in model_payload.get("states", ()) if isinstance(value, dict)),
            transitions=tuple(CanonicalTransition.model_validate(value) for value in model_payload.get("transitions", ()) if isinstance(value, dict)),
        ),
        metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {},
    )


def build_numbered_nl_segments(text: str) -> tuple[NumberedNLSegment, ...]:
    """Split numbered NL even when the legacy artifact contains no newlines.

    The splitter recognizes a one-or-more digit marker only when it is followed
    by a period, whitespace, or the ``when`` clause marker.  Thus the numeric
    literal in ``front_distance > 10`` is not treated as a segment boundary.
    """

    marker = re.compile(r"(?<![A-Za-z0-9_.])(?P<number>[1-9]\d*)(?:(?P<dot>\.)(?=\s)|(?=\s)|(?=when\b))")
    matches = list(marker.finditer(text))
    segments: list[NumberedNLSegment] = []
    seen: dict[int, int] = {}
    for index, match in enumerate(matches):
        number = int(match.group("number"))
        if number > 99:
            continue
        start = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
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
                raw_start=match.start(),
                raw_end=end,
                reason="A numbered source marker was followed by a clause boundary and the next marker bounds this segment.",
                basis="nl-segmentation.v1; period/whitespace/when marker rule",
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
                basis="nl-segmentation.v1 fallback; exact artifact preservation",
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


def _graph_facts(model: ModelIR) -> tuple[dict[str, tuple[str, ...]], dict[str, tuple[str, ...]]]:
    graph: dict[str, list[str]] = {}
    for item in model.states:
        graph.setdefault(item.name, [])
    for item in model.transitions:
        graph.setdefault(item.source, []).append(item.target)
        graph.setdefault(item.target, [])
    normalized = {key: tuple(value) for key, value in graph.items()}
    roots = {item.target for item in model.transitions if item.source in {"[*]", "[* ]"}}
    reachable: set[str] = set(roots)
    frontier = list(roots)
    while frontier:
        node = frontier.pop(0)
        for target in normalized.get(node, ()):
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)
    return normalized, {"[*]": tuple(sorted(reachable))}


def build_inspection_equivalent_facts(model: ModelIR, fcstm_hash: str) -> InspectionEquivalentFacts:
    """Compute deterministic inventory, diagnostics, and finite graph facts."""

    outgoing: dict[str, list[str]] = {state.name: [] for state in model.states}
    transitions: list[InspectionTransitionFact] = []
    diagnostics: list[InspectionDiagnostic] = []
    for item in model.transitions:
        transitions.append(
            InspectionTransitionFact(
                transition_ref=item.ref,
                source=item.source,
                target=item.target,
                triggers=item.triggers,
                guard=item.guard,
                effects=item.effects,
                line=item.line,
                reason="The row is copied from the owned FCSTM parser's normalized transition fields.",
                basis=model.algorithm_version,
            )
        )
        if item.source in outgoing:
            outgoing[item.source].append(item.ref)
        if item.source not in {"[*]", "[* ]"} and item.source not in model.state_names:
            diagnostics.append(
                InspectionDiagnostic(
                    code="FCSTM_SOURCE_UNRESOLVED",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message=f"Transition source {item.source!r} is not a declared FCSTM state.",
                    reason="The normalized transition endpoint is absent from the owned state inventory.",
                    basis="fcstm-line-parser.v1 endpoint membership",
                )
            )
        if item.target not in model.state_names and item.target not in {"[*]", "[* ]"}:
            diagnostics.append(
                InspectionDiagnostic(
                    code="FCSTM_TARGET_UNRESOLVED",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message=f"Transition target {item.target!r} is not a declared FCSTM state.",
                    reason="The normalized transition endpoint is absent from the owned state inventory.",
                    basis="fcstm-line-parser.v1 endpoint membership",
                )
            )
        if item.source in {"[*]", "[* ]"} and (item.triggers or item.guard):
            diagnostics.append(
                InspectionDiagnostic(
                    code="INITIAL_ENTRY_CONDITIONAL",
                    severity="warning",
                    refs=(item.ref,),
                    line=item.line,
                    message="An initial pseudostate transition carries a trigger or guard.",
                    reason="Initial-entry conditionality is a deterministic structural fact.",
                    basis="inspection-equivalent.initial-entry.v1",
                )
            )
    for state in model.states:
        if not outgoing.get(state.name):
            diagnostics.append(
                InspectionDiagnostic(
                    code="LEAF_WITHOUT_OUTGOING",
                    severity="warning",
                    refs=(state.ref,),
                    line=state.line,
                    message=f"State {state.name!r} has no outgoing FCSTM transition.",
                    reason="The state has no outgoing transition in the closed FCSTM inventory.",
                    basis="inspection-equivalent.deadlock-frontier.v1",
                )
            )
    graph, reachability = _graph_facts(model)
    state_facts = tuple(
        InspectionStateFact(
            state_ref=state.ref,
            name=state.name,
            parent=state.parent,
            line=state.line,
            is_composite=any(item.parent == state.name for item in model.states),
            outgoing_transition_refs=tuple(outgoing.get(state.name, ())),
            reason="The row is computed from owned-parser state declarations and transition endpoints.",
            basis="fcstm-line-parser.v1 plus inspection-equivalent inventory.v1",
        )
        for state in model.states
    )
    metrics: dict[str, int | float] = {
        "state_count": len(model.states),
        "event_count": len(model.events),
        "transition_count": len(model.transitions),
        "diagnostic_count": len(diagnostics),
        "reachable_node_count": len(reachability.get("[*]", ())),
        "guarded_transition_count": sum(1 for item in model.transitions if item.guard),
    }
    return InspectionEquivalentFacts(
        schema_version="evidence-discovery.inspection-equivalent.v1",
        algorithm_version="inspection-equivalent.fcstm-graph.v1",
        fcstm_hash=fcstm_hash,
        states=state_facts,
        transitions=tuple(transitions),
        events=tuple(item.name for item in model.events),
        diagnostics=tuple(diagnostics),
        reachability={key: value for key, value in reachability.items()},
        metrics=metrics,
        reason="The method receives deterministic inventory and diagnostics without invoking Python inspect, pyfcstm.inspect, or legacy inspect backends.",
        basis="owned FCSTM line parser, endpoint checks, initial-entry checks, leaf frontier, and finite graph traversal",
    )


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_FORMULA_KEYWORDS = {"and", "or", "not", "true", "false", "if", "else"}


def build_verification_facts(model: ModelIR, inspection: InspectionEquivalentFacts) -> VerificationFacts:
    """Summarize finite verification facts without claiming an external solver run."""

    checks: list[VerificationCheck] = []
    reachable = set(inspection.reachability.get("[*]", ()))
    for state in inspection.states:
        status = "proved" if state.name in reachable else "unknown"
        checks.append(
            VerificationCheck(
                check_id=f"reachability:{state.name}",
                kind="reachability",
                status=status,
                subject_refs=(state.state_ref,),
                details={"state": state.name, "reachable_from_initial": state.name in reachable},
                reason="Finite graph traversal found the state from the FCSTM initial pseudostate roots." if state.name in reachable else "No finite initial-root path was found; this is not a semantic violation claim.",
                basis=inspection.algorithm_version,
            )
        )
    for transition in model.transitions:
        if transition.source in {"[*]", "[* ]"}:
            checks.append(
                VerificationCheck(
                    check_id=f"initial-entry:{transition.ref}",
                    kind="initial_entry",
                    status="refuted" if transition.triggers or transition.guard else "proved",
                    subject_refs=(transition.ref,),
                    details={"has_trigger": bool(transition.triggers), "has_guard": bool(transition.guard)},
                    reason="Initial-entry conditionality is directly determined from normalized transition fields.",
                    basis=inspection.algorithm_version,
                )
            )
    for state in inspection.states:
        if not state.outgoing_transition_refs:
            checks.append(
                VerificationCheck(
                    check_id=f"deadlock:{state.name}",
                    kind="deadlock",
                    status="refuted",
                    subject_refs=(state.state_ref,),
                    details={"outgoing_count": 0},
                    reason="The state is a finite leaf frontier with no outgoing transition in the closed model.",
                    basis=inspection.algorithm_version,
                )
            )
    return VerificationFacts(
        schema_version="evidence-discovery.verify-facts.v1",
        algorithm_version="verify-equivalent.finite-graph.v1",
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
                basis="fcstm-line-parser.v1 guard normalization",
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
    """Keep a deterministic receipt for a large contract sequence without expanding it in prompts."""

    if not isinstance(value, list):
        return {"count": 0, "sha256": _artifact_hash_payload({"items": []}), "label": label}
    return {
        "count": len(value),
        "sha256": _artifact_hash_payload({"items": value}),
        "label": label,
    }


def _working_contract_prompt_dict(
    artifact: StructuredArtifact | None,
    *,
    include_elements: bool,
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
        "schema_version",
        "artifact_role",
        "example_id",
        "input_identity",
        "summary",
        "ownership_policy",
        "usage_gate",
        "inventory_digests",
        "attribution_policy",
        "diagnostic_attribution",
        "artifact_bindings",
        "source_trace_base",
        "review_subject",
        "confirm_gate",
        "repair_gate",
    )
    projected: dict[str, Any] = {
        key: payload[key]
        for key in fixed_keys
        if key in payload
    }
    if include_elements:
        projected["elements"] = [
            {
                key: item[key]
                for key in (
                    "element_id",
                    "kind",
                    "origin",
                    "model_refs",
                    "source_refs",
                    "macro_ids",
                    "edit_policy",
                    "metadata",
                    "semantic_fields",
                )
                if isinstance(item, dict) and key in item
            }
            for item in payload.get("elements", [])
            if isinstance(item, dict)
        ]
    else:
        projected["elements"] = _project_large_sequence(payload.get("elements"), label="elements")
    if "macros" in payload:
        projected["macros"] = (
            payload["macros"]
            if include_elements
            else _project_large_sequence(payload["macros"], label="macros")
        )

    eligibility: dict[str, Any] = {}
    raw_eligibility = payload.get("capability_eligibility", {})
    if isinstance(raw_eligibility, dict):
        for name, value in raw_eligibility.items():
            if not isinstance(value, dict):
                eligibility[name] = value
                continue
            row = {
                key: value[key]
                for key in (
                    "claim_boundary",
                    "eligible_element_ids",
                    "eligible_field_refs",
                    "evidence_refs",
                )
                if key in value
            }
            for key in ("excluded_element_ids", "excluded_field_refs"):
                if key in value:
                    row[key] = _project_large_sequence(
                        value[key],
                        label=f"{name}.{key}",
                    )
            eligibility[name] = row
    projected["capability_eligibility"] = eligibility
    return {
        "ref": artifact.ref.model_dump(mode="json"),
        "payload": projected,
        "reason": "The working contract projection preserves exact source/model mapping and hashes omitted repetitive eligibility sequences.",
        "basis": "working-contract-prompt-projection.v1",
    }


def _prompt_base(pair: Any, stage: PromptStage) -> dict[str, Any]:
    """Build common stage context with every artifact receipt and source-role boundary."""

    if pair.context_manifest is None:
        raise ValueError("stage prompt requires a complete context manifest")
    return {
        "prompt_projection_version": "stage-context-projection.v1",
        "stage": stage,
        "context_manifest": pair.context_manifest.model_dump(mode="json"),
        "artifact_refs": [
            item.model_dump(mode="json")
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
            "reference_inspection_facts": "read_only_v27_deterministic_facts",
            "inspection_equivalent_facts": "owned_deterministic_inventory_and_diagnostics",
            "verify_facts": "owned_deterministic_finite_verification_summary",
            "smt_facts": "normalized_formal_inputs_not_solver_result",
        },
        "reason": "Stage context is role-scoped while the complete artifact closure remains identified by the manifest.",
        "basis": "context-manifest.v1 and stage-context-projection.v1",
    }


def prompt_context_payload(pair: Any, *, stage: PromptStage) -> dict[str, Any]:
    """Return the stage-specific prompt closure without duplicating unrelated raw artifacts.

    Every stage receives the complete manifest, hashes, versions, and role policy.
    The source and model branches additionally receive the exact payloads owned by
    their authority. This preserves v27 information flow and prevents a large
    mapping or inspection report from being repeated into every LLM call.
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
                ),
                "source_trace_receipt": (
                    pair.source_trace.ref.model_dump(mode="json")
                    if pair.source_trace
                    else None
                ),
            }
        )
    elif stage == "source_grounding":
        payload.update(
            {
                "numbered_nl": [
                    item.model_dump(mode="json")
                    for item in pair.nl_segments
                ],
                "plantuml_source": {
                    "role": "author_source",
                    "path": str(pair.pair_dir / "plantuml.puml"),
                    "sha256": pair.hashes.get("plantuml"),
                    "text": pair.plantuml_text,
                    "reason": "PlantUML is supplied for author-source localization only.",
                    "basis": "source-role separation contract",
                },
                "canonical_source_ir": (
                    pair.canonical_source_ir.model_dump(mode="json")
                    if pair.canonical_source_ir
                    else None
                ),
                "exact_source_inventory": (
                    pair.exact_source_inventory.model_dump(mode="json")
                    if pair.exact_source_inventory
                    else None
                ),
                "working_contract": _working_contract_prompt_dict(
                    pair.working_contract,
                    include_elements=True,
                ),
                "source_trace": (
                    pair.source_trace.to_prompt_dict()
                    if pair.source_trace
                    else None
                ),
            }
        )
    elif stage == "model_grounding":
        payload.update(
            {
                "numbered_nl": [
                    item.model_dump(mode="json")
                    for item in pair.nl_segments
                ],
                "fcstm_model": {
                    "role": "closed_model",
                    "path": str(pair.pair_dir / "fcstm.fcstm"),
                    "sha256": pair.hashes.get("fcstm"),
                    "text": pair.fcstm_text,
                    "model_ir": pair.model.to_dict(),
                    "reason": "FCSTM is the closed model evaluated by the new deterministic backends.",
                    "basis": pair.model.algorithm_version,
                },
                "working_contract": _working_contract_prompt_dict(
                    pair.working_contract,
                    include_elements=True,
                ),
                "reference_inspection_facts": (
                    pair.reference_inspection.to_prompt_dict()
                    if pair.reference_inspection
                    else None
                ),
                "inspection_equivalent_facts": (
                    pair.inspection_facts.model_dump(mode="json")
                    if pair.inspection_facts
                    else None
                ),
                "verify_facts": (
                    pair.verify_facts.model_dump(mode="json")
                    if pair.verify_facts
                    else None
                ),
                "smt_facts": (
                    pair.smt_facts.model_dump(mode="json")
                    if pair.smt_facts
                    else None
                ),
            }
        )
    elif stage == "d_adjudication":
        payload["dossier_input_policy"] = {
            "source_and_model_facts": "supplied in the obligation dossiers",
            "ledger": "forbidden",
            "baseline": "forbidden",
            "judge_examples": "forbidden",
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
            purpose="Extract numbered source obligations without looking at model satisfaction or ledger answers.",
            excluded_claims=("model_violation", "baseline_hit", "judge_match"),
            reason="The v27 contract stage is source-first.",
            basis="frozen method information-flow boundary",
        ),
        PromptSection(
            section_id="source-grounding",
            artifact_roles=("plantuml_source", "canonical_source_ir", "source_inventory", "source_trace", "working_contract"),
            purpose="Locate author-source states, transitions, mappings, and source-scoped obligations.",
            excluded_claims=("fcstm_execution_verdict", "ledger_answer", "baseline_result"),
            reason="PlantUML and canonical IR are author-source evidence only.",
            basis="source-role separation contract",
        ),
        PromptSection(
            section_id="model-grounding",
            artifact_roles=("fcstm_model", "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts"),
            purpose="Bind exact closed-model elements and plan deterministic predicate checks.",
            excluded_claims=("author_source_identity", "ledger_answer", "judge_example"),
            reason="FCSTM is the tested closed model; deterministic facts are context, not semantic verdicts.",
            basis="closed-model execution contract",
        ),
    )
    forbidden = (
        "frozen ledger answers and D/L labels",
        "baseline hit/false-positive results",
        "independent judge examples or outputs",
        "other pair payloads",
        "historical method release outputs",
    )
    base = {
        "schema_version": "evidence-discovery.context-manifest.v1",
        "protocol_version": "v27-input-closure-plus-four-family-19.v1",
        "pair_id": pair_id,
        "artifacts": [item.model_dump(mode="json") for item in artifacts],
        "sections": [item.model_dump(mode="json") for item in sections],
        "forbidden_inputs": list(forbidden),
        "reason": "The method and grounding branches must receive the full source/model/fact closure while remaining independent of evaluation answers.",
        "basis": "v27 frozen artifacts plus owned evidence_discovery deterministic fact algorithms",
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
        "reason": "All sections are method-visible context; no ledger, baseline, judge, or historical release data is included.",
        "basis": "context-manifest.v1 and frozen pair artifact closure",
    }
