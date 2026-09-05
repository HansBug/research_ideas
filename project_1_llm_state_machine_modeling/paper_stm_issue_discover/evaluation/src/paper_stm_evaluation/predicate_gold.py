"""Evaluation-only contracts and inventory tooling for predicate gold v1."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

SCHEMA_VERSION = "paper1.predicate-gold.v1"
INVENTORY_SCHEMA_VERSION = "paper1.predicate-gold.inventory.v1"
PROTOCOL_VERSION = "paper1.obligation-equivalent-predicate-gold.v1"
ANNOTATION_BATCH_SCHEMA_VERSION = "paper1.predicate-gold.annotation-batch.v1"
SHA256_PATTERN = r"^sha256:[0-9a-f]{64}$"


class StrictModel(BaseModel):
    """Base class for immutable canonical records that reject unknown fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class ExactnessRelation(str, Enum):
    """Logical relationship between normalized obligation O and property P."""

    EQUIVALENT = "EQUIVALENT"
    O_IMPLIES_P = "O_IMPLIES_P"
    P_IMPLIES_O = "P_IMPLIES_O"
    UNRELATED = "UNRELATED"


class GoldStatus(str, Enum):
    """Final disposition of one ledger issue in predicate gold v1."""

    EXACT_FALSE = "EXACT_FALSE"
    COMPOSITE_EXACT_FALSE = "COMPOSITE_EXACT_FALSE"
    SOUND_FALSE_PROXY = "SOUND_FALSE_PROXY"
    UNSUPPORTED_EXACT = "UNSUPPORTED_EXACT"
    BLOCKED_EXECUTION = "BLOCKED_EXECUTION"


class GoldMode(str, Enum):
    """Implementation form of the selected reference property or disposition."""

    FROZEN_PREDICATE = "FROZEN_PREDICATE"
    COMPOSITE = "COMPOSITE"
    EVALUATION_ONLY_ORACLE = "EVALUATION_ONLY_ORACLE"
    PROXY_ONLY = "PROXY_ONLY"
    UNSUPPORTED = "UNSUPPORTED"


class ExecutionState(str, Enum):
    """Machine-observable state of one property evaluation."""

    COMPLETED_BOOLEAN = "COMPLETED_BOOLEAN"
    NOT_EXECUTED = "NOT_EXECUTED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


class PositiveControlStatus(str, Enum):
    """Disposition of the independent true-side control for an executable property."""

    COMPLETED_TRUE = "COMPLETED_TRUE"
    UNAVAILABLE_JUSTIFIED = "UNAVAILABLE_JUSTIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ReviewTrack(str, Enum):
    """Independent review responsibility used by the v1 annotation protocol."""

    A_OBLIGATION = "A_OBLIGATION"
    B_PROPERTY = "B_PROPERTY"
    C_EXECUTION = "C_EXECUTION"
    EXTRA_HIGH_RISK = "EXTRA_HIGH_RISK"


class Confidence(str, Enum):
    """Reviewer confidence reported without replacing evidence or arbitration."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class JsonType(str, Enum):
    """JSON type of one typed property input."""

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NULL = "null"
    ARRAY = "array"
    OBJECT = "object"


class SourceRef(StrictModel):
    """Stable repository reference used as annotation or execution evidence."""

    repository_path: str = Field(description="Repository-relative evidence path; never an absolute or temporary path.", min_length=1)
    sha256: str = Field(description="SHA-256 of the referenced file bytes.", pattern=SHA256_PATTERN)
    json_pointer: str | None = Field(description="RFC 6901 pointer when the referenced evidence is JSON; otherwise null.")
    line_start: int | None = Field(description="One-based first source line when the evidence is line-addressable; otherwise null.", ge=1)
    line_end: int | None = Field(description="One-based inclusive final source line when a range is cited; otherwise null.", ge=1)
    model_element: str | None = Field(description="Stable state, transition, action, variable, region, or configuration identity; otherwise null.")
    excerpt: str | None = Field(description="Short verbatim excerpt used for review; null when the pointer is sufficient.")

    @model_validator(mode="after")
    def validate_line_range(self) -> SourceRef:
        """Reject reversed or half-specified source line ranges."""

        if self.line_end is not None and self.line_start is None:
            raise ValueError("line_end requires line_start")
        if self.line_start is not None and self.line_end is not None and self.line_end < self.line_start:
            raise ValueError("line_end must be greater than or equal to line_start")
        return self


class AlternativeReading(StrictModel):
    """One source-compatible reading considered for a D1 or boundary obligation."""

    reading_id: str = Field(description="Stable annotation-local alternative-reading identifier.", min_length=1)
    reading: str = Field(description="Complete alternative interpretation, including changed obligation or attribution.", min_length=1)
    source_compatible: bool = Field(description="Whether the reviewer found this reading compatible with the author source.")
    disposition: Literal["ADOPTED", "RETAINED_SENSITIVITY", "REJECTED"] = Field(description="Final treatment of this reading after arbitration.")
    reason: str = Field(description="Evidence-specific reason for retaining, adopting, or rejecting the reading.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Source anchors used to assess this reading.", min_length=1)


class NormalizedObligation(StrictModel):
    """Source-first normalized normative obligation O for one ledger issue."""

    subject_component: str = Field(description="Component or state machine subject that bears the obligation.", min_length=1)
    source_artifact_role: str = Field(description="Role of the author artifact from which the obligation is recovered.", min_length=1)
    quantifier: str = Field(description="Existential, universal, uniqueness, or other explicit quantifier; missing information is stated verbatim.", min_length=1)
    cardinality: str = Field(description="Required cardinality or an explicit statement that the source does not define one.", min_length=1)
    trigger_stimulus: str = Field(description="Trigger or stimulus and its identity; explicitly records absence or missing source information.", min_length=1)
    preconditions: tuple[str, ...] = Field(description="Source-backed preconditions; an empty tuple means the obligation has none, not that review was skipped.")
    semantic_scope: str = Field(description="Global, before, after, between, state-local, region-local, or other normalized scope.", min_length=1)
    initial_configuration: str = Field(description="Required initial or reachable configuration, or an explicit source-backed absence statement.", min_length=1)
    required_response: str = Field(description="Required behavior, state, action, variable value, or termination outcome.", min_length=1)
    forbidden_behavior: str | None = Field(description="Forbidden behavior when O is prohibitive; null when the obligation is purely positive.")
    timing: str = Field(description="RTC, macrostep, next stable configuration, finite bound, eventual, or other timing semantics.", min_length=1)
    observation_window: str = Field(description="Closed observation window or an explicit statement that no finite window is specified.", min_length=1)
    bound: str = Field(description="Source-backed bound and unit or an explicit statement that no bound is specified.", min_length=1)
    rtc_semantics: str = Field(description="How run-to-completion, pseudostates, completion, and event consumption affect O.", min_length=1)
    observables: tuple[str, ...] = Field(description="States, actions, variables, transitions, configurations, or termination observed by O.", min_length=1)
    environment_assumptions: tuple[str, ...] = Field(description="Only assumptions independently supported by author source or formal semantics.")
    missing_information: tuple[str, ...] = Field(description="Obligation dimensions absent from source and therefore forbidden to fabricate.")
    adopted_ledger_reading: str = Field(description="The ledger reading selected after considering all source-compatible alternatives.", min_length=1)
    reason: str = Field(description="Issue-specific explanation of the normalized obligation and adjacent readings.", min_length=1)
    basis: str = Field(description="Issue-specific NL, author-source, ledger, and formal-semantics basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="NL, author source, ledger, and semantics anchors used to recover O.", min_length=2)


class TypedInput(StrictModel):
    """One typed and source-provenanced input bound before property execution."""

    field_name: str = Field(description="Exact predicate or oracle input field name.", min_length=1)
    json_type: JsonType = Field(description="JSON type of the persisted input value.")
    value: JsonValue = Field(description="Exact JSON value proposed before execution.")
    normalized_value: JsonValue = Field(description="Canonical JSON value used by the backend after documented normalization.")
    provenance_kind: Literal["AUTHOR_NL", "AUTHOR_SOURCE", "FORMAL_SEMANTICS", "DECLARED_EVALUATION_ASSUMPTION"] = Field(description="Permitted origin of this input; method output and reference models are excluded.")
    source_ref: SourceRef = Field(description="Stable source anchor from which the value was bound.")
    stable_object_id: str | None = Field(description="Stable native object or model-element identity; null for scalar bounds or domains without an object ID.")
    alias_resolution: str | None = Field(description="Documented alias-to-native-object resolution; null when no alias was used.")
    reason: str = Field(description="Why this exact value is required by O and does not narrow or strengthen it silently.", min_length=1)


class CandidateProperty(StrictModel):
    """One independently proposed executable candidate and its relation to O."""

    candidate_id: str = Field(description="Stable issue-local candidate identifier.", min_length=1)
    mode: GoldMode = Field(description="Frozen predicate, composite, evaluation-only oracle, proxy, or unsupported form.")
    predicate_ids: tuple[str, ...] = Field(description="Frozen predicate IDs used by this candidate; empty only for an evaluation-only oracle or unsupported candidate.")
    property_expression: str = Field(description="Complete human-readable property P including quantifier, scope, timing, and observables.", min_length=1)
    exactness_relation: ExactnessRelation = Field(description="Proven O/P implication direction for this candidate.")
    typed_inputs: tuple[TypedInput, ...] = Field(description="Inputs proposed before execution; empty only when the candidate is not executable.")
    assumptions: tuple[str, ...] = Field(description="Explicit candidate assumptions, including domains, bounds, initial scope, and artifact mapping.")
    semantic_gaps: tuple[str, ...] = Field(description="Dimensions where P differs from O; empty only for an equivalent candidate.")
    selected: bool = Field(description="Whether pane5 selected this candidate as exact gold or nearest proxy.")
    reason: str = Field(description="Candidate-specific O/P comparison, including why false would or would not establish O=false.", min_length=1)
    basis: str = Field(description="Source, formal semantics, backend code, and typed-input basis for this candidate.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Evidence used for this candidate comparison.", min_length=1)


class PropertyComposition(StrictModel):
    """Explicit non-short-circuit semantics for a composite reference property."""

    operator: Literal["AND", "OR", "NOT", "IMPLIES", "FOR_ALL"] = Field(description="Declared logical operator used to combine constituents.")
    constituent_ids: tuple[str, ...] = Field(description="Ordered candidate or property IDs evaluated without hidden conditions.", min_length=1)
    truth_definition: str = Field(description="Complete truth function and quantification used to derive the composite Boolean.", min_length=1)
    no_short_circuit: Literal[True] = Field(description="Confirms that every constituent is evaluated and receives a receipt.")


class ExecutableProperty(StrictModel):
    """Selected exact or proxy property whose proposal is hashed before execution."""

    property_id: str = Field(description="Stable selected property identifier.", min_length=1)
    mode: GoldMode = Field(description="Execution form of the selected property.")
    predicate_ids: tuple[str, ...] = Field(description="Frozen predicate IDs used by the property; empty only for an evaluation-only oracle.")
    expression: str = Field(description="Complete executable property expression with scope and timing.", min_length=1)
    typed_inputs: tuple[TypedInput, ...] = Field(description="All typed inputs frozen before execution.")
    assumptions: tuple[str, ...] = Field(description="All source-backed execution assumptions.")
    semantic_scope: str = Field(description="Exact execution scope corresponding to O.", min_length=1)
    timing: str = Field(description="Exact timing or boundedness semantics corresponding to O.", min_length=1)
    rtc_semantics: str = Field(description="Exact RTC/macrostep interpretation used during execution.", min_length=1)
    composition: PropertyComposition | None = Field(description="Composite semantics, or null for a single predicate/oracle.")
    proposal_sha256: str = Field(description="Hash of O, P, typed inputs, and assumptions saved before any execution result was observed.", pattern=SHA256_PATTERN)


class ExecutionRecord(StrictModel):
    """Reproducible backend execution record for a selected property."""

    state: ExecutionState = Field(description="Terminal Boolean, non-executed, error, timeout, or unknown execution state.")
    verdict: bool | None = Field(description="Boolean result only when state is COMPLETED_BOOLEAN; otherwise null.")
    query_path: str | None = Field(description="Gold-root-relative serialized query path; null only when not executed.")
    query_sha256: str | None = Field(description="Hash of the serialized query bytes; null only when not executed.", pattern=SHA256_PATTERN)
    command: tuple[str, ...] = Field(description="Exact argv used for provider-free replay; empty only when not executed.")
    backend_id: str | None = Field(description="Frozen predicate backend or evaluation-only oracle identity; null only when not executed.")
    backend_version: str | None = Field(description="Backend version or source commit used for execution; null only when not executed.")
    backend_code_sha256: str | None = Field(description="Hash of the relevant backend/oracle code bytes; null only when not executed.", pattern=SHA256_PATTERN)
    artifact_sha256: str = Field(description="Hash of the exact defective artifact evaluated.", pattern=SHA256_PATTERN)
    domain: JsonValue | None = Field(description="Closed execution domain, or null when the property has no domain input.")
    bound: JsonValue | None = Field(description="Closed execution bound, or null when the property is unbounded/static.")
    seed: int | None = Field(description="Execution seed when nondeterminism is supported; null for deterministic evaluation.")
    started_at: str | None = Field(description="UTC execution start time; null only when not executed.")
    completed_at: str | None = Field(description="UTC completion time; null only when not executed or incomplete.")
    receipt_refs: tuple[SourceRef, ...] = Field(description="Execution receipt references; empty only when not executed.")
    counterexample_refs: tuple[SourceRef, ...] = Field(description="Counterexample or trace references; empty for static checks without a trace or when not executed.")
    replay_status: Literal["REPLAY_MATCH", "NOT_REPLAYED", "REPLAY_MISMATCH"] = Field(description="Independent mechanical replay disposition.")
    reason: str = Field(description="Execution-state and verdict interpretation without treating errors as false.", min_length=1)

    @model_validator(mode="after")
    def validate_execution_state(self) -> ExecutionRecord:
        """Enforce the observable contract between terminal state and Boolean value."""

        if self.state == ExecutionState.COMPLETED_BOOLEAN:
            required = (self.verdict is not None, bool(self.query_path), bool(self.query_sha256), bool(self.command), bool(self.backend_id), bool(self.backend_version), bool(self.backend_code_sha256), bool(self.started_at), bool(self.completed_at), bool(self.receipt_refs))
            if not all(required):
                raise ValueError("completed Boolean execution requires query, command, backend, time, receipt, and verdict")
        elif self.verdict is not None:
            raise ValueError("only completed Boolean execution may persist a verdict")
        return self


class PositiveControl(StrictModel):
    """Independent true-side control used to detect wrong bindings and vacuity."""

    status: PositiveControlStatus = Field(description="Completed true, justified unavailable, or not applicable disposition.")
    control_kind: str = Field(description="Minimal repair, independent correct artifact, theorem-backed control, or explicit non-applicability.", min_length=1)
    artifact_path: str | None = Field(description="Repository-relative control artifact path, or null when unavailable/not applicable.")
    artifact_sha256: str | None = Field(description="Hash of the control artifact, or null when unavailable/not applicable.", pattern=SHA256_PATTERN)
    verdict: bool | None = Field(description="True only for a completed control; otherwise null.")
    receipt_refs: tuple[SourceRef, ...] = Field(description="Control execution receipt references; empty only when unavailable/not applicable.")
    contamination_check: str = Field(description="Check that the control was not selected or edited using the defective verdict.", min_length=1)
    vacuity_check: str = Field(description="Check for unreachable antecedents, empty domains, and other vacuous truth sources.", min_length=1)
    reason: str = Field(description="Evidence-specific explanation of control selection or justified absence.", min_length=1)

    @model_validator(mode="after")
    def validate_control(self) -> PositiveControl:
        """Require a true verdict and receipt only for completed controls."""

        if self.status == PositiveControlStatus.COMPLETED_TRUE:
            if self.verdict is not True or not self.artifact_path or not self.artifact_sha256 or not self.receipt_refs:
                raise ValueError("COMPLETED_TRUE requires a true verdict, artifact, hash, and receipt")
        elif self.verdict is not None or self.receipt_refs:
            raise ValueError("unavailable or inapplicable controls cannot persist an execution verdict or receipt")
        return self


class ReviewOpinion(StrictModel):
    """Hash-bound independent Track A, B, C, or high-risk review opinion."""

    opinion_id: str = Field(description="Stable review opinion identity.", min_length=1)
    reviewer_id: str = Field(description="Internal reviewer identity; it is not represented as an external human annotator.", min_length=1)
    track: ReviewTrack = Field(description="Independent review responsibility.")
    input_sha256: str = Field(description="Digest of all files and records visible to this opinion.", pattern=SHA256_PATTERN)
    normalized_obligation_sha256: str = Field(description="Digest of the proposed or reviewed normalized obligation.", pattern=SHA256_PATTERN)
    property_proposal_sha256: str | None = Field(description="Digest of the property proposal reviewed by Track B/C; null for a blind Track A obligation opinion.", pattern=SHA256_PATTERN)
    proposed_status: GoldStatus | None = Field(description="Proposed final status for Track B/C; null for blind Track A, which does not see a property.")
    proposed_exactness_relation: ExactnessRelation | None = Field(description="Proposed O/P relationship for Track B/C; null for blind Track A.")
    proposed_predicate_ids: tuple[str, ...] = Field(description="Predicate IDs proposed by this reviewer; empty for unsupported or evaluation-only cases.")
    reason: str = Field(description="Independent opinion-specific semantic or execution reason.", min_length=1)
    basis: str = Field(description="Independent opinion-specific source, backend, or receipt basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Evidence actually read by this reviewer.", min_length=1)
    other_tracks_visible: bool = Field(description="Whether another track's conclusion was visible before this opinion was frozen.")
    v60_actual_visible: bool = Field(description="Whether frozen v60 actual predicate/input output was visible before this opinion was frozen.")
    confidence: Confidence = Field(description="Reviewer's confidence, which does not replace evidence.")
    reviewed_at: str = Field(description="UTC opinion freeze time.", min_length=1)
    opinion_sha256: str = Field(description="Digest of the persisted opinion payload excluding this field.", pattern=SHA256_PATTERN)

    def expected_opinion_sha256(self) -> str:
        """Return the canonical digest expected for this persisted opinion."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"opinion_sha256"}))

    @model_validator(mode="after")
    def validate_opinion_provenance(self) -> ReviewOpinion:
        """Enforce opinion hash integrity and track visibility boundaries."""

        if self.opinion_sha256 != self.expected_opinion_sha256():
            raise ValueError("opinion_sha256 does not match opinion payload")
        if self.v60_actual_visible:
            raise ValueError("predicate-gold reviewers cannot see v60 actual predicate/input output")
        if self.track in {ReviewTrack.A_OBLIGATION, ReviewTrack.B_PROPERTY} and self.other_tracks_visible:
            raise ValueError("blind Track A/B opinions cannot see other-track conclusions")
        if self.track == ReviewTrack.A_OBLIGATION and self.property_proposal_sha256 is not None:
            raise ValueError("blind Track A cannot bind a property proposal")
        if self.track == ReviewTrack.A_OBLIGATION and (self.proposed_status is not None or self.proposed_exactness_relation is not None):
            raise ValueError("blind Track A cannot propose a property status or O/P relation")
        property_tracks = {
            ReviewTrack.B_PROPERTY,
            ReviewTrack.C_EXECUTION,
            ReviewTrack.EXTRA_HIGH_RISK,
        }
        if self.track in property_tracks and self.property_proposal_sha256 is None:
            raise ValueError("Track B/C/high-risk review must bind the reviewed property proposal")
        if self.track in property_tracks and (
            self.proposed_status is None or self.proposed_exactness_relation is None
        ):
            raise ValueError("Track B/C/high-risk review must propose a property status and O/P relation")
        return self


class ConflictRecord(StrictModel):
    """One disagreement between independent opinions requiring source-based arbitration."""

    conflict_id: str = Field(description="Stable issue-local conflict identifier.", min_length=1)
    opinion_ids: tuple[str, ...] = Field(description="Conflicting opinion identities.", min_length=2)
    disputed_fields: tuple[str, ...] = Field(description="Obligation, relation, input, status, or execution fields in dispute.", min_length=1)
    positions: tuple[str, ...] = Field(description="Complete competing positions retained without majority-vote collapse.", min_length=2)
    additional_evidence_refs: tuple[SourceRef, ...] = Field(description="Evidence read specifically to resolve the disagreement.", min_length=1)
    resolution: str = Field(description="Pane5 evidence-based resolution or retained sensitivity.", min_length=1)


class ArbitrationRecord(StrictModel):
    """Pane5 final adjudication after reading O, P, executions, and all opinions."""

    arbitration_id: str = Field(description="Stable arbitration identity.", min_length=1)
    adjudicator_id: Literal["pane5:manual-supervised-adjudicator"] = Field(description="Authorized pane5 adjudicator identity.")
    input_sha256: str = Field(description="Digest binding the arbitration to source, proposals, opinions, and receipts.", pattern=SHA256_PATTERN)
    final_status: GoldStatus = Field(description="Final status selected from evidence, not majority vote.")
    final_exactness_relation: ExactnessRelation = Field(description="Final logical relationship between O and selected P.")
    reason: str = Field(description="Issue-specific final decision and resolution of adjacent statuses.", min_length=1)
    basis: str = Field(description="Issue-specific source, semantics, backend, receipt, and review basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Evidence actually read during final arbitration.", min_length=2)
    sensitivity: tuple[str, ...] = Field(description="Retained D1, bound, domain, grouping, or semantic sensitivity statements.")
    arbitrated_at: str = Field(description="UTC arbitration completion time.", min_length=1)


class PredicateGoldAnnotation(StrictModel):
    """Final predicate-gold overlay for exactly one immutable ledger issue."""

    ledger_id: str = Field(description="Immutable current ledger identity.", pattern=r"^(EIS|INS|VU|DIFF)-[0-9]{4}-[0-9]{2}$")
    pair_id: str = Field(description="Four-digit source pair identity.", pattern=r"^[0-9]{4}$")
    family: Literal["EIS", "INS", "VU", "DIFF"] = Field(description="Ledger family derived from ledger_id.")
    ledger_sha256: str = Field(description="Hash of the complete current ledger.json bytes.", pattern=SHA256_PATTERN)
    nl_path: str = Field(description="Repository-relative author NL path.", min_length=1)
    nl_sha256: str = Field(description="Hash of the author NL bytes.", pattern=SHA256_PATTERN)
    artifact_path: str = Field(description="Repository-relative defective executable FCSTM artifact path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of the defective FCSTM artifact bytes.", pattern=SHA256_PATTERN)
    author_source_path: str = Field(description="Repository-relative author PlantUML source path.", min_length=1)
    author_source_sha256: str = Field(description="Hash of the author PlantUML bytes.", pattern=SHA256_PATTERN)
    d_tier: Literal["D2", "D1"] = Field(description="Immutable D tier copied from the current ledger.")
    l_tier: Literal["L2", "L1", "L0"] = Field(description="Immutable L tier copied from the current ledger.")
    normalized_obligation: NormalizedObligation = Field(description="Source-first normalized obligation O.")
    obligation_source_refs: tuple[SourceRef, ...] = Field(description="Mirrored top-level anchors for rapid obligation audit.", min_length=2)
    alternative_readings: tuple[AlternativeReading, ...] = Field(description="All source-compatible or explicitly rejected adjacent readings.")
    candidate_properties: tuple[CandidateProperty, ...] = Field(description="All semantically credible candidates and their O/P directions.", min_length=1)
    rejected_candidate_ids: tuple[str, ...] = Field(description="Candidate IDs rejected as non-equivalent exact gold.")
    exactness_relation: ExactnessRelation = Field(description="Final O/P relationship for the selected gold or nearest proxy.")
    gold_status: GoldStatus = Field(description="Final exact, proxy, unsupported, or working blocked disposition.")
    gold_mode: GoldMode = Field(description="Frozen predicate, composite, evaluation-only, proxy, or unsupported mode.")
    gold_property: ExecutableProperty | None = Field(description="Selected exact executable property; null for proxy-only or unsupported dispositions.")
    predicate_ids: tuple[str, ...] = Field(description="Predicate IDs used by exact gold; empty for evaluation-only or unsupported cases.")
    execution: ExecutionRecord | None = Field(description="Exact property execution; null when no exact executable property exists.")
    false_receipt_refs: tuple[SourceRef, ...] = Field(description="Completed false receipt references for exact gold; empty otherwise.")
    counterexample_refs: tuple[SourceRef, ...] = Field(description="Counterexample or trace references; empty for static facts or unsupported cases.")
    positive_control: PositiveControl | None = Field(description="True-side control for exact/proxy execution, or null when nothing was executed.")
    proxy_property: ExecutableProperty | None = Field(description="Nearest sound O-implied property; null when no sound proxy exists.")
    proxy_execution: ExecutionRecord | None = Field(description="Completed false execution of the nearest proxy; null when no proxy was executed.")
    unsupported_reason: str | None = Field(description="Why no obligation-equivalent executable property is available; null for exact dispositions.")
    capability_gap: tuple[str, ...] = Field(description="Specific missing semantic capabilities after checking frozen predicates, composites, and pyfcstm-native evaluation oracles.")
    reason: str = Field(description="Issue-specific final status and exact/proxy/unsupported boundary.", min_length=1)
    basis: str = Field(description="Issue-specific NL, source, ledger, semantics, query, receipt, and control evidence.", min_length=1)
    review_opinions: tuple[ReviewOpinion, ...] = Field(description="Independent Track A, Track B, Track C, and fourth high-risk opinions.", min_length=4)
    reviewer_ids: tuple[str, ...] = Field(description="Unique internal reviewer identities mirrored from all four review opinions.", min_length=4)
    conflicts: tuple[ConflictRecord, ...] = Field(description="All detected disagreements, including retained sensitivities.")
    arbitration: ArbitrationRecord = Field(description="Pane5 final source-based arbitration record.")
    confidence: Confidence = Field(description="Final confidence after review and arbitration.")
    created_at: str = Field(description="UTC canonical annotation freeze time.", min_length=1)
    schema_version: Literal[SCHEMA_VERSION] = Field(default=SCHEMA_VERSION, description="Predicate gold annotation schema version.")

    @model_validator(mode="after")
    def validate_final_closure(self) -> PredicateGoldAnnotation:
        """Enforce mechanically decidable status, execution, and review closure."""

        if self.family != self.ledger_id.split("-", 1)[0] or self.pair_id != self.ledger_id.split("-")[1]:
            raise ValueError("family and pair_id must match ledger_id")
        candidate_ids = [candidate.candidate_id for candidate in self.candidate_properties]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate property IDs must be unique within an annotation")
        if not set(self.rejected_candidate_ids).issubset(candidate_ids):
            raise ValueError("rejected_candidate_ids must reference persisted candidates")
        if self.d_tier == "D1" and not any(
            reading.source_compatible and reading.disposition in {"ADOPTED", "RETAINED_SENSITIVITY"}
            for reading in self.alternative_readings
        ):
            raise ValueError("D1 requires at least one retained source-compatible alternative reading")
        tracks = {opinion.track for opinion in self.review_opinions}
        required_tracks = {
            ReviewTrack.A_OBLIGATION,
            ReviewTrack.B_PROPERTY,
            ReviewTrack.C_EXECUTION,
            ReviewTrack.EXTRA_HIGH_RISK,
        }
        if tracks != required_tracks or len(self.review_opinions) != 4:
            raise ValueError(
                "every annotation requires exactly one Track A, B, C, and fourth opinion"
            )
        opinion_reviewers = {opinion.reviewer_id for opinion in self.review_opinions}
        if set(self.reviewer_ids) != opinion_reviewers or len(self.reviewer_ids) != 4:
            raise ValueError("reviewer_ids must mirror four distinct opinion reviewers")
        if self.arbitration.final_status != self.gold_status or self.arbitration.final_exactness_relation != self.exactness_relation:
            raise ValueError("arbitration and final status/exactness must agree")
        exact = self.gold_status in {GoldStatus.EXACT_FALSE, GoldStatus.COMPOSITE_EXACT_FALSE}
        if exact:
            if self.exactness_relation != ExactnessRelation.EQUIVALENT or self.gold_property is None or self.execution is None:
                raise ValueError("exact status requires equivalent gold_property and execution")
            if self.execution.state != ExecutionState.COMPLETED_BOOLEAN or self.execution.verdict is not False:
                raise ValueError("exact status requires completed Boolean false")
            if self.execution.replay_status != "REPLAY_MATCH":
                raise ValueError("exact status requires an independent matching replay")
            if self.execution.artifact_sha256 != self.artifact_sha256:
                raise ValueError("exact execution artifact hash must match the canonical defective artifact")
            if not self.false_receipt_refs or self.positive_control is None:
                raise ValueError("exact status requires false receipts and a positive-control disposition")
            if set(self.false_receipt_refs) != set(self.execution.receipt_refs):
                raise ValueError("top-level false receipt refs must mirror the exact execution receipts")
            if self.positive_control.status == PositiveControlStatus.NOT_APPLICABLE:
                raise ValueError("an executed exact property cannot mark its positive control not applicable")
            if self.predicate_ids != self.gold_property.predicate_ids:
                raise ValueError("top-level predicate_ids must mirror the selected exact property")
            if self.gold_status == GoldStatus.COMPOSITE_EXACT_FALSE:
                if self.gold_property.mode != GoldMode.COMPOSITE or self.gold_property.composition is None:
                    raise ValueError("composite exact status requires explicit composition semantics")
            elif self.gold_property.mode == GoldMode.COMPOSITE or self.gold_property.composition is not None:
                raise ValueError("single exact status cannot carry composite semantics")
        elif self.gold_property is not None or self.execution is not None or self.false_receipt_refs:
            raise ValueError("non-exact status cannot persist an exact gold property or false receipt")
        if self.gold_status == GoldStatus.SOUND_FALSE_PROXY:
            if self.exactness_relation != ExactnessRelation.O_IMPLIES_P or self.proxy_property is None or self.proxy_execution is None:
                raise ValueError("sound proxy requires O_IMPLIES_P, proxy property, and execution")
            if self.proxy_execution.state != ExecutionState.COMPLETED_BOOLEAN or self.proxy_execution.verdict is not False:
                raise ValueError("sound proxy requires completed Boolean false")
            if self.proxy_execution.replay_status != "REPLAY_MATCH":
                raise ValueError("sound proxy requires an independent matching replay")
            if self.proxy_execution.artifact_sha256 != self.artifact_sha256:
                raise ValueError("proxy execution artifact hash must match the canonical defective artifact")
            if self.positive_control is None or self.positive_control.status == PositiveControlStatus.NOT_APPLICABLE:
                raise ValueError("an executed sound proxy requires a positive-control disposition")
        if self.gold_status == GoldStatus.UNSUPPORTED_EXACT and (not self.unsupported_reason or not self.capability_gap):
            raise ValueError("unsupported exact requires a reason and concrete capability gap")
        if self.gold_status == GoldStatus.BLOCKED_EXECUTION:
            raise ValueError("BLOCKED_EXECUTION is forbidden in the final canonical dataset")
        return self


class PredicateGoldDataset(StrictModel):
    """Canonical overlay containing exactly one final annotation per ledger issue."""

    schema_version: Literal[SCHEMA_VERSION] = Field(default=SCHEMA_VERSION, description="Canonical dataset schema version.")
    protocol_version: Literal[PROTOCOL_VERSION] = Field(default=PROTOCOL_VERSION, description="Frozen exactness and annotation protocol version.")
    generated_at: str = Field(description="UTC dataset generation time.", min_length=1)
    source_commit: str = Field(description="Repository commit whose frozen inputs and evaluation code were used.", pattern=r"^[0-9a-f]{40}$")
    ledger_path: str = Field(description="Repository-relative current ledger path.", min_length=1)
    ledger_sha256: str = Field(description="Hash of the current ledger bytes.", pattern=SHA256_PATTERN)
    registry_path: str = Field(description="Repository-relative frozen 19-predicate registry path.", min_length=1)
    registry_sha256: str = Field(description="Hash of the frozen registry bytes.", pattern=SHA256_PATTERN)
    inventory_path: str = Field(description="Gold-root-relative frozen input inventory path.", min_length=1)
    inventory_sha256: str = Field(description="Hash of the frozen input inventory bytes.", pattern=SHA256_PATTERN)
    pyfcstm_commit: str = Field(description="Pinned pyfcstm submodule commit used for native parsing/execution.", pattern=r"^[0-9a-f]{40}$")
    items: dict[str, PredicateGoldAnnotation] = Field(description="Annotations keyed by immutable ledger ID; key must equal the embedded ledger_id.", min_length=1)
    provider_experiment_calls: Literal[0] = Field(description="No provider experiment calls are permitted for this evaluation-only gold.")
    method_reruns: Literal[0] = Field(description="No method reruns are permitted for this gold construction.")
    judge_reruns: Literal[0] = Field(description="No Judge reruns are permitted for this gold construction.")
    full_experiment_reruns: Literal[0] = Field(description="No 54x3 reruns are permitted for this gold construction.")

    @model_validator(mode="after")
    def validate_item_keys(self) -> PredicateGoldDataset:
        """Require key identity and final zero-blocked closure."""

        if any(key != item.ledger_id for key, item in self.items.items()):
            raise ValueError("every items key must equal its annotation ledger_id")
        if any(item.ledger_sha256 != self.ledger_sha256 for item in self.items.values()):
            raise ValueError("every annotation must bind the dataset ledger hash")
        return self


class PredicateGoldAnnotationBatch(StrictModel):
    """Hash-bound canonical annotation batch produced after pane5 arbitration."""

    schema_version: Literal[ANNOTATION_BATCH_SCHEMA_VERSION] = Field(
        default=ANNOTATION_BATCH_SCHEMA_VERSION,
        description="Canonical annotation batch schema version.",
    )
    batch_id: str = Field(description="Stable batch identity.", min_length=1)
    pair_ids: tuple[str, ...] = Field(description="Pair identities represented by the annotation rows.", min_length=1)
    rows: tuple[PredicateGoldAnnotation, ...] = Field(description="One fully closed canonical annotation per ledger issue.", min_length=1)
    created_at: str = Field(description="UTC canonical batch creation time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical digest expected for this annotation batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> PredicateGoldAnnotationBatch:
        """Require unique rows, matching pair IDs and a correct batch digest."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("annotation batch contains duplicate ledger IDs")
        if {ledger_id.split("-")[1] for ledger_id in ledger_ids} != set(self.pair_ids):
            raise ValueError("annotation pair_ids do not match row ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("batch_sha256 does not match annotation batch payload")
        return self


class PairInventoryRecord(StrictModel):
    """Frozen source and executable-artifact inventory for one ledger pair."""

    pair_id: str = Field(description="Four-digit pair identity.", pattern=r"^[0-9]{4}$")
    ledger_ids: tuple[str, ...] = Field(description="All current ledger IDs owned by this pair.", min_length=1)
    nl_path: str = Field(description="Repository-relative author NL path.", min_length=1)
    nl_sha256: str = Field(description="Hash of author NL bytes.", pattern=SHA256_PATTERN)
    nl_line_count: int = Field(description="Number of physical lines in the author NL file.", ge=1)
    plantuml_path: str = Field(description="Repository-relative author PlantUML path.", min_length=1)
    plantuml_sha256: str = Field(description="Hash of author PlantUML bytes.", pattern=SHA256_PATTERN)
    plantuml_line_count: int = Field(description="Number of physical lines in the PlantUML file.", ge=1)
    fcstm_path: str = Field(description="Repository-relative executable FCSTM snapshot path.", min_length=1)
    fcstm_sha256: str = Field(description="Hash of executable FCSTM bytes.", pattern=SHA256_PATTERN)
    source_meta_path: str = Field(description="Repository-relative source provenance metadata path.", min_length=1)
    source_meta_sha256: str = Field(description="Hash of source provenance metadata bytes.", pattern=SHA256_PATTERN)
    fcstm_meta_path: str = Field(description="Repository-relative FCSTM conversion metadata path.", min_length=1)
    fcstm_meta_sha256: str = Field(description="Hash of FCSTM conversion metadata bytes.", pattern=SHA256_PATTERN)
    source_pair_id: str = Field(description="Source pair identity declared by source_meta.json.", min_length=1)
    source_locator: str = Field(description="Stable original-source locator declared by source_meta.json.", min_length=1)
    fcstm_artifact_role: str = Field(description="Declared role of the executable FCSTM snapshot.", min_length=1)
    fcstm_parse_status: str = Field(description="Declared FCSTM parse status from frozen metadata.", min_length=1)
    source_static_eligible: bool = Field(description="Whether metadata permits attribution-scoped source-static use.")
    simulation_status: str = Field(description="Declared whole-model simulation eligibility/status; does not become a predicate verdict.", min_length=1)
    academic_eligible: bool = Field(description="Declared whole-artifact academic eligibility from FCSTM metadata.")
    academic_ineligibility_reason: str | None = Field(description="Frozen reason for whole-artifact ineligibility; null only when eligible.")
    selected_fcstm_hash_matches: bool = Field(description="Whether current model.fcstm bytes match the hash sealed in fcstm_meta.json.")


class PredicateGoldInventory(StrictModel):
    """Machine-recomputed inventory of all frozen inputs used by predicate gold v1."""

    schema_version: Literal[INVENTORY_SCHEMA_VERSION] = Field(default=INVENTORY_SCHEMA_VERSION, description="Inventory schema version.")
    generated_at: str = Field(description="UTC inventory generation time supplied by the caller.", min_length=1)
    source_commit: str = Field(description="Repository commit inventoried.", pattern=r"^[0-9a-f]{40}$")
    ledger_path: str = Field(description="Repository-relative current ledger path.", min_length=1)
    ledger_sha256: str = Field(description="Hash of current ledger bytes.", pattern=SHA256_PATTERN)
    registry_path: str = Field(description="Repository-relative frozen registry path.", min_length=1)
    registry_sha256: str = Field(description="Hash of frozen registry bytes.", pattern=SHA256_PATTERN)
    ledger_count: int = Field(description="Number of current ledger IDs.", ge=1)
    pair_count: int = Field(description="Number of distinct pairs represented by the ledger.", ge=1)
    family_counts: dict[str, int] = Field(description="Mechanically recomputed ledger family counts.")
    d_tier_counts: dict[str, int] = Field(description="Mechanically recomputed D-tier counts.")
    l_tier_counts: dict[str, int] = Field(description="Mechanically recomputed L-tier counts.")
    registry_predicate_ids: tuple[str, ...] = Field(description="Frozen registry predicate IDs in registry order.", min_length=1)
    registry_predicate_count: int = Field(description="Number of frozen public predicate IDs.", ge=1)
    registry_status: str = Field(description="Frozen registry status field.", min_length=1)
    coverage_snapshot_status: str = Field(description="Frozen coverage-snapshot status; it is not executable gold.", min_length=1)
    pairs: tuple[PairInventoryRecord, ...] = Field(description="One frozen input record per ledger pair.", min_length=1)
    missing_paths: tuple[str, ...] = Field(description="Missing required paths; empty is required for Gate A.")
    duplicate_ledger_ids: tuple[str, ...] = Field(description="Duplicate ledger IDs detected during enumeration; empty is required.")
    selected_fcstm_hash_mismatches: tuple[str, ...] = Field(description="Pairs whose current FCSTM bytes differ from metadata; empty is required.")
    notes: tuple[str, ...] = Field(description="Inventory explanations that do not alter frozen inputs or semantic labels.")


def sha256_path(path: Path) -> str:
    """Return a prefixed SHA-256 digest for one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    """Return a prefixed SHA-256 digest for canonical JSON data."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _repo_relative(repo_root: Path, path: Path) -> str:
    """Return a normalized repository-relative POSIX path."""

    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _registry_predicates(registry: dict[str, Any]) -> tuple[str, ...]:
    """Enumerate public predicate IDs from the registry's ordered families."""

    return tuple(predicate["id"] for family in registry["families"] for predicate in family["predicates"])


def build_inventory(*, repo_root: Path, paper_root: Path, generated_at: str, source_commit: str) -> PredicateGoldInventory:
    """Read frozen ledger, registry, and pair artifacts into a hash-closed inventory."""

    ledger_path = paper_root / "discover_matrix" / "ledger_v2" / "ledger.json"
    registry_path = paper_root / "related_work/provenance/archive/pre_p1_20260905/predicate_registry.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    items = ledger["items"]
    ids = tuple(items)
    pair_to_ids: dict[str, list[str]] = defaultdict(list)
    for ledger_id, item in items.items():
        pair_to_ids[item["pair"]].append(ledger_id)

    missing_paths: list[str] = []
    mismatches: list[str] = []
    pair_records: list[PairInventoryRecord] = []
    for pair_id in sorted(pair_to_ids):
        item = items[pair_to_ids[pair_id][0]]
        nl_path = (ledger_path.parent / item["pair_context"]["nl_file"]).resolve()
        plantuml_path = (ledger_path.parent / item["pair_context"]["stm0_file"]).resolve()
        pair_dir = nl_path.parent
        required = {
            "nl": nl_path,
            "plantuml": plantuml_path,
            "fcstm": pair_dir / "model.fcstm",
            "source_meta": pair_dir / "source_meta.json",
            "fcstm_meta": pair_dir / "fcstm_meta.json",
        }
        absent = [path for path in required.values() if not path.is_file()]
        if absent:
            missing_paths.extend(_repo_relative(repo_root, path) for path in absent)
            continue
        source_meta = json.loads(required["source_meta"].read_text(encoding="utf-8"))
        fcstm_meta = json.loads(required["fcstm_meta"].read_text(encoding="utf-8"))
        fcstm_hash = sha256_path(required["fcstm"])
        expected_fcstm_hash = "sha256:" + fcstm_meta["selected_fcstm_sha256"].removeprefix("sha256:")
        hash_matches = fcstm_hash == expected_fcstm_hash
        if not hash_matches:
            mismatches.append(pair_id)
        pair_records.append(
            PairInventoryRecord(
                pair_id=pair_id,
                ledger_ids=tuple(pair_to_ids[pair_id]),
                nl_path=_repo_relative(repo_root, required["nl"]),
                nl_sha256=sha256_path(required["nl"]),
                nl_line_count=len(required["nl"].read_text(encoding="utf-8").splitlines()),
                plantuml_path=_repo_relative(repo_root, required["plantuml"]),
                plantuml_sha256=sha256_path(required["plantuml"]),
                plantuml_line_count=len(required["plantuml"].read_text(encoding="utf-8").splitlines()),
                fcstm_path=_repo_relative(repo_root, required["fcstm"]),
                fcstm_sha256=fcstm_hash,
                source_meta_path=_repo_relative(repo_root, required["source_meta"]),
                source_meta_sha256=sha256_path(required["source_meta"]),
                fcstm_meta_path=_repo_relative(repo_root, required["fcstm_meta"]),
                fcstm_meta_sha256=sha256_path(required["fcstm_meta"]),
                source_pair_id=source_meta["source_pair_id"],
                source_locator=source_meta["source_locator"],
                fcstm_artifact_role=fcstm_meta["artifact_role"],
                fcstm_parse_status=fcstm_meta["parse_status"],
                source_static_eligible=fcstm_meta["source_static_discover_eligible"],
                simulation_status=fcstm_meta["simulation_status"],
                academic_eligible=fcstm_meta["academic_eligible"],
                academic_ineligibility_reason=fcstm_meta.get("academic_ineligibility_reason"),
                selected_fcstm_hash_matches=hash_matches,
            )
        )

    registry_ids = _registry_predicates(registry)
    duplicates = tuple(sorted(ledger_id for ledger_id, count in Counter(ids).items() if count > 1))
    return PredicateGoldInventory(
        generated_at=generated_at,
        source_commit=source_commit,
        ledger_path=_repo_relative(repo_root, ledger_path),
        ledger_sha256=sha256_path(ledger_path),
        registry_path=_repo_relative(repo_root, registry_path),
        registry_sha256=sha256_path(registry_path),
        ledger_count=len(ids),
        pair_count=len(pair_to_ids),
        family_counts=dict(sorted(Counter(ledger_id.split("-", 1)[0] for ledger_id in ids).items())),
        d_tier_counts=dict(sorted(Counter(item["D"] for item in items.values()).items())),
        l_tier_counts=dict(sorted(Counter(item["L"] for item in items.values()).items())),
        registry_predicate_ids=registry_ids,
        registry_predicate_count=len(registry_ids),
        registry_status=registry["status"],
        coverage_snapshot_status=registry["coverage_snapshot"]["status"],
        pairs=tuple(pair_records),
        missing_paths=tuple(sorted(missing_paths)),
        duplicate_ledger_ids=duplicates,
        selected_fcstm_hash_mismatches=tuple(sorted(mismatches)),
        notes=(
            "The registry 118/145 coverage snapshot is planned_mapping_not_new_method_measurement, not predicate gold.",
            "FCSTM eligibility fields are frozen conversion metadata and do not by themselves determine exactness or a predicate verdict.",
        ),
    )


def write_json(path: Path, payload: Any) -> None:
    """Write canonical UTF-8 JSON with a trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    """Build the provider-free predicate-gold command-line parser."""

    parser = argparse.ArgumentParser(description="Build and validate evaluation-only predicate gold artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory = subparsers.add_parser("inventory", help="Build the frozen-input inventory.")
    inventory.add_argument("--repo-root", type=Path, required=True)
    inventory.add_argument("--paper-root", type=Path, required=True)
    inventory.add_argument("--generated-at", required=True)
    inventory.add_argument("--source-commit", required=True)
    inventory.add_argument("--output", type=Path, required=True)
    schema = subparsers.add_parser("schema", help="Write the canonical predicate-gold JSON Schema.")
    schema.add_argument("--output", type=Path, required=True)
    validate = subparsers.add_parser("validate", help="Validate a completed canonical predicate-gold dataset.")
    validate.add_argument("--gold", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run provider-free inventory, schema, or canonical validation."""

    args = _build_parser().parse_args(argv)
    if args.command == "inventory":
        inventory = build_inventory(
            repo_root=args.repo_root,
            paper_root=args.paper_root,
            generated_at=args.generated_at,
            source_commit=args.source_commit,
        )
        write_json(args.output, inventory.model_dump(mode="json"))
        print(json.dumps({"output": str(args.output), "ledger_count": inventory.ledger_count, "pair_count": inventory.pair_count, "missing_paths": len(inventory.missing_paths), "hash_mismatches": len(inventory.selected_fcstm_hash_mismatches)}, sort_keys=True))
        return 0
    if args.command == "schema":
        write_json(args.output, PredicateGoldDataset.model_json_schema())
        print(json.dumps({"output": str(args.output), "schema_version": SCHEMA_VERSION}, sort_keys=True))
        return 0
    payload = json.loads(args.gold.read_text(encoding="utf-8"))
    dataset = PredicateGoldDataset.model_validate(payload)
    print(json.dumps({"gold": str(args.gold), "items": len(dataset.items), "schema_version": dataset.schema_version}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
