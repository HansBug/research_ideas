"""Build the Track B raw-first proposal for baseline pairs 0040--0059.

The decision table in this file is a human-authored proposal table.  The
script only joins it with exact raw report text, author-source hashes, and
the ordered reference ledger identifiers.  It does not read any decision,
proposal, judge, or pane5 artifact.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


REPO = Path("/home/zhangshaoang/oo-projects/research_ideas")
ARCHIVE = (
    REPO
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    / "final_results/v60_current_vs_x1v2_baseline"
)
RAW_ROOT = ARCHIVE / "raw/x1v2_baseline/method"
SOURCE_ROOT = ARCHIVE / "reference/x1v2_input_closure/pairs"
LEDGER_PATH = ARCHIVE / "reference/ledger.json"
OUT = ARCHIVE / "derived/manual_adjudication_v3_baseline_ni/proposals/track_b_0040_0059.json"

TargetTier = Literal["D2", "D1", "D0", "A0"]
Relation = Literal["FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"]


class SourceRef(BaseModel):
    """A stable archive-relative author-source location used by one proposal."""

    path: str = Field(description="Archive-relative NL or PlantUML source path.")
    sha256: str = Field(description="SHA-256 of the exact source file bytes.")
    lines: str = Field(description="1-based source line or line range supporting the opinion.")


class ManualOpinion(BaseModel):
    """One raw-first semantic opinion for one raw report candidate."""

    observed_fact: str = Field(description="What the report claims and what the author source actually shows.")
    observed_fact_status: Literal["SUPPORTED", "REFUTED"] = Field(description="Whether the report's material fact is supported by author source.")
    normative_violation_status: Literal["SUPPORTED", "AMBIGUOUS", "NOT_ESTABLISHED"] = Field(description="Status of the claimed violated obligation after reading NL and model.")
    defect_claim_status: Literal["AUTHOR_SOURCE_DEFECT", "NO_DEFECT_ESTABLISHED"] = Field(description="Whether the report establishes an author-source defect claim.")
    d_tier: TargetTier = Field(description="Track B proposed D/A tier under the frozen baseline protocol.")
    proposed_validity: Literal["VALID_KNOWN", "VALID_NOVEL", "INVALID"] = Field(description="Mechanical proposal validity derived from D/A and the dense ledger relations; not a final adjudication label.")
    a0_reason: Optional[Literal["FALSE_POSITIVE"]] = Field(default=None, description="Baseline A0 subtype; null unless the source refutes the material fact.")
    reason: str = Field(description="Dedicated Track B reason for this report, grounded in source lines.")
    basis: str = Field(description="Dedicated evidence basis, including the surviving alternative reading where relevant.")
    source_refs: List[SourceRef] = Field(description="Author NL and PlantUML pointers supporting the opinion.")
    relation_overrides: Dict[str, Relation] = Field(description="Manual relation overrides; all other ledger IDs are NO_MATCH.")


class RawReportProposal(BaseModel):
    """A complete raw report plus its independent Track B proposal."""

    reviewer_id: str = Field(description="Independent Track B reviewer identity copied from the artifact metadata.")
    review_status: Literal["PROPOSAL"] = Field(description="This record is a proposal and is not a final adjudication.")
    reference_visible: Literal[False] = Field(description="Frozen labels were not visible before this blind proposal was submitted.")
    primary_visible: Literal[False] = Field(description="Another primary decision was not visible before this blind proposal was submitted.")
    pair_id: str = Field(description="Numeric four-digit pair identifier.")
    raw_pair_id: str = Field(description="Exact pair_id stored in the raw record.")
    round: int = Field(description="Raw report round number.")
    finding_index: int = Field(description="Zero-based index in parsed_output.issues.")
    original_report_id: str = Field(description="Stable raw report identifier, or the explicit fallback identifier when absent.")
    raw_method_record_path: str = Field(description="Archive-relative raw record path.")
    raw_json_pointer: str = Field(description="JSON pointer to the exact raw issue object.")
    raw_record_sha256: str = Field(description="SHA-256 of the exact raw record bytes.")
    raw_fields: Dict[str, Any] = Field(description="Exact issue, where, reason, and basis values from the raw issue object.")
    author_source: Dict[str, Any] = Field(description="Archive-relative NL/PlantUML paths and exact file hashes.")
    proposal: ManualOpinion = Field(description="Independent Track B raw-first opinion.")
    all_expected_relations: Dict[str, Relation] = Field(description="Dense relation map over every ordered ledger ID.")
    relation_digest_sha256: str = Field(description="SHA-256 of canonical ordered (expected_id, relation) pairs.")


class ProposalArtifact(BaseModel):
    """Versioned Track B proposal artifact with coverage and evidence-gap metadata."""

    artifact_schema_version: str = Field(description="Schema version for this proposal artifact.")
    protocol_version: str = Field(description="Protocol identifier used for the Track B semantic reading.")
    reviewer_id: str = Field(description="Independent Track B proposal reviewer identifier.")
    generated_at_utc: str = Field(description="UTC generation timestamp for this proposal artifact.")
    input_scope: Dict[str, Any] = Field(description="Requested pair interval and allowed input roots.")
    non_k_membership_evidence_gap: Dict[str, Any] = Field(description="Selector limitation preventing a claim that every raw candidate is confirmed current non-K.")
    coverage: Dict[str, Any] = Field(description="Raw candidate, source, and relation coverage counts.")
    ordered_expected_ids: List[str] = Field(description="All 145 expected IDs in reference-ledger order.")
    reports: List[RawReportProposal] = Field(description="One dedicated proposal for each raw report candidate in the interval.")
    forbidden_inputs_read: List[str] = Field(description="Explicitly prohibited input classes not read by the builder.")
    execution_boundary: Dict[str, Any] = Field(description="Provider/method/Judge execution boundary for this proposal.")


def sha256_file(path: Path) -> str:
    """Hash exact bytes without normalizing line endings."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source_metadata(path: Path) -> Dict[str, Any]:
    """Read a complete author source and retain a replayable read receipt."""
    text = path.read_text(encoding="utf-8")
    byte_digest = sha256_file(path)
    text_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if byte_digest != text_digest:
        raise AssertionError(f"source text/byte digest mismatch: {path}")
    return {
        "sha256": byte_digest,
        "full_text_sha256": text_digest,
        "line_count": len(text.splitlines()),
        "read_mode": "full_file_text_before_opinion",
    }


def pair_number(raw_pair_id: str) -> str:
    """Extract the four-digit pair suffix from the raw identifier."""
    suffix = raw_pair_id.rsplit("_", 1)[-1]
    if len(suffix) != 4 or not suffix.isdigit():
        raise ValueError(f"unexpected raw pair_id: {raw_pair_id}")
    return suffix


def source_ref(pair: str, kind: str, sha256: str, lines: str) -> SourceRef:
    """Create a source pointer relative to the archive root."""
    return SourceRef(path=f"reference/x1v2_input_closure/pairs/{pair}/{kind}", sha256=sha256, lines=lines)


# Explicit per-report decision codes.  The source-line and prose expansions
# below are keyed by these codes; no report label is inferred from words in a
# report.  This table has one entry for every raw issue candidate in scope.
DECISION_CODES: Dict[str, str] = {
    # 0040
    "0040:r1:i0": "power_off_missing",
    "0040:r2:i0": "auto_final_extra",
    "0040:r2:i1": "auto_final_condition",
    "0040:r2:i2": "power_off_missing",
    "0040:r3:i0": "auto_process_extra",
    "0040:r3:i1": "auto_final_condition",
    # 0041
    "0041:r1:i0": "brake_extra_edges",
    "0041:r1:i1": "clamping_feedback_scope",
    "0041:r2:i0": "brake_extra_edges",
    "0041:r2:i1": "brake_extra_edges",
    "0041:r2:i2": "braking_feedback_bypass",
    "0041:r3:i0": "brake_extra_edges",
    "0041:r3:i1": "brake_extra_edges",
    "0041:r3:i2": "braking_feedback_bypass",
    # 0042
    "0042:r1:i0": "keyoff_initial",
    "0042:r1:i1": "keyoff_initial",
    "0042:r2:i0": "keyoff_initial",
    "0042:r2:i1": "idle_brake",
    # 0043
    "0043:r1:i0": "pump_extra_region",
    "0043:r1:i1": "pump_extra_region",
    "0043:r1:i2": "pump_direct_entry",
    "0043:r2:i0": "pump_extra_region",
    "0043:r2:i1": "pump_extra_region",
    "0043:r3:i0": "pump_extra_region",
    "0043:r3:i1": "pump_first_state",
    # 0044
    "0044:r1:i0": "emergency_action_text",
    "0044:r2:i0": "inmotion_initial",
    "0044:r3:i0": "inmotion_initial",
    "0044:r3:i1": "approaching_hold",
    # 0045
    "0045:r2:i0": "cook_time_display_0045",
    "0045:r2:i1": "timer_start",
    "0045:r2:i2": "timer_stop",
    "0045:r3:i0": "cook_time_display_0045",
    "0045:r3:i1": "cook_cancel_update_0045",
    "0045:r3:i2": "timer_start_stop",
    # 0046
    "0046:r1:i0": "mission_extra_region",
    "0046:r1:i1": "mission_parallel_misread",
    "0046:r1:i2": "search_idle_scope",
    "0046:r1:i3": "uav_count_action",
    "0046:r2:i0": "search_continuity",
    "0046:r2:i1": "search_region_count",
    "0046:r2:i2": "mission_extra_region",
    "0046:r2:i3": "uav_count_action",
    "0046:r3:i0": "mission_parallel_misread",
    "0046:r3:i1": "mission_extra_region",
    "0046:r3:i2": "mission_sync",
    "0046:r3:i3": "flight_scope",
    "0046:r3:i4": "uav_count_action",
    # 0047
    "0047:r1:i0": "collision_no_orthogonal",
    "0047:r1:i1": "collision_activation",
    "0047:r1:i2": "collision_generic_event",
    "0047:r1:i3": "collision_exit_scope",
    "0047:r2:i0": "collision_no_orthogonal",
    "0047:r2:i1": "collision_activation",
    "0047:r2:i2": "collision_exit_scope",
    "0047:r3:i0": "collision_no_orthogonal",
    "0047:r3:i1": "collision_activation",
    "0047:r3:i2": "collision_generic_event",
    "0047:r3:i3": "collision_exit_scope",
    # 0049
    "0049:r1:i0": "highway_finish_exit",
    "0049:r1:i1": "urban_exit_hang",
    "0049:r1:i2": "intersection_lane_change",
    "0049:r1:i3": "highway_finish_scope",
    "0049:r1:i4": "highway_finish_scope",
    "0049:r1:i5": "urban_finish_scope",
    "0049:r1:i6": "collision_unreachable_0049",
    "0049:r2:i0": "highway_finish_exit",
    "0049:r2:i1": "urban_exit_hang",
    "0049:r2:i2": "composite_finish_transition",
    "0049:r2:i3": "composite_finish_transition",
    "0049:r2:i4": "composite_mode_transition",
    "0049:r2:i5": "collision_unreachable_0049",
    "0049:r3:i0": "highway_finish_exit",
    "0049:r3:i1": "urban_exit_hang",
    "0049:r3:i2": "urban_guard_overlap",
    "0049:r3:i3": "composite_mode_transition",
    "0049:r3:i4": "highway_false_case",
    "0049:r3:i5": "collision_unreachable_0049",
    # 0050--0059
    "0050:r3:i0": "auto_final_text",
    "0051:r1:i0": "braking_feedback_bypass",
    "0051:r1:i1": "braking_extra_completion",
    "0051:r2:i0": "braking_feedback_bypass",
    "0051:r2:i1": "braking_extra_completion",
    "0051:r3:i0": "braking_feedback_bypass",
    "0051:r3:i1": "braking_extra_completion",
    "0052:r2:i0": "operate_initial_ambiguity",
    "0052:r2:i1": "idle_brake",
    "0052:r3:i0": "shutdown_extra",
    "0052:r3:i1": "state_name_alias",
    "0053:r1:i0": "pump_parallel_misread",
    "0053:r1:i1": "pump_cross_transition",
    "0053:r1:i2": "pump_parallel_misread",
    "0053:r2:i0": "pump_wrapper_level",
    "0053:r2:i1": "pump_cross_transition",
    "0053:r2:i2": "pump_initial_level",
    "0053:r3:i0": "pump_parallel_misread",
    "0053:r3:i1": "pump_cross_transition",
    "0054:r2:i0": "obstacle_guard_trigger",
    "0054:r2:i1": "emergency_do_entry",
    "0054:r2:i2": "approaching_send",
    "0054:r2:i3": "approaching_exit",
    "0054:r2:i4": "arrived_action_text",
    "0054:r3:i0": "obstacle_guard_trigger",
    "0054:r3:i1": "emergency_do_entry",
    "0054:r3:i2": "closed_action_text",
    "0054:r3:i3": "arrived_action_text",
    "0055:r2:i0": "door_opened_name",
    "0055:r2:i1": "cook_time_display_0055",
    "0055:r2:i2": "cook_cancel_update_0055",
    "0055:r2:i3": "timer_start",
    "0055:r2:i4": "timer_stop",
    "0055:r2:i5": "timer_expired",
    "0055:r3:i0": "cook_time_display_0055",
    "0055:r3:i1": "cook_cancel_update_0055",
    "0056:r1:i0": "intercept_conflict",
    "0056:r1:i1": "uav_count_guard",
    "0056:r1:i2": "mission_exit_priority",
    "0056:r2:i0": "intercept_conflict",
    "0056:r2:i1": "uav_count_guard",
    "0056:r2:i2": "task_assignment_scope",
    "0056:r3:i0": "area_zero_time",
    "0056:r3:i1": "intercept_conflict",
    "0056:r3:i2": "attack_failure_scope",
    "0056:r3:i3": "uav_count_guard",
    "0057:r1:i0": "collision_no_orthogonal",
    "0057:r1:i1": "collision_activation_partial",
    "0057:r2:i0": "collision_no_orthogonal",
    "0057:r2:i1": "collision_activation_partial",
    "0057:r3:i0": "collision_activation_partial",
    "0057:r3:i1": "collision_no_orthogonal",
    "0059:r1:i0": "highway_lane_change",
    "0059:r1:i1": "urban_exit_hang",
    "0059:r1:i2": "urban_guard_overlap",
    "0059:r1:i3": "highway_finish_scope",
    "0059:r1:i4": "composite_mode_transition",
    "0059:r1:i5": "highway_exit_hang",
    "0059:r1:i6": "urban_exit_hang",
    "0059:r1:i7": "collision_guard_brackets",
    "0059:r1:i8": "collision_mode_names",
    "0059:r1:i9": "collision_and_release",
    "0059:r2:i0": "highway_lane_change",
    "0059:r2:i1": "highway_false_case",
    "0059:r2:i2": "composite_finish_transition",
    "0059:r2:i3": "urban_exit_hang",
    "0059:r2:i4": "urban_guard_overlap",
    "0059:r2:i5": "collision_mode_names",
    "0059:r3:i0": "highway_lane_change",
    "0059:r3:i1": "finish_implicit_state",
    "0059:r3:i2": "urban_exit_hang",
    "0059:r3:i3": "highway_exit_hang",
    "0059:r3:i4": "collision_unreachable_0059",
    "0059:r3:i5": "collision_mode_names",
}


# Code -> (tier, fact status, normative status, claim status, source lines,
# relation overrides, concise independent reasoning).  The raw issue text is
# copied separately for every report, so repeated semantic codes still have
# report-specific evidence and pointers in the resulting JSON.
DECISIONS: Dict[str, Dict[str, Any]] = {
    "power_off_missing": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "1-13", {"EIS-0040-01": "FULL_MATCH"}, "The NL makes Power Off a system-level response, while the source consumes it only from HumanDriving; Autonomous has no such edge. Returning to HumanDriving first would require a different event sequence and does not answer the current Power Off event."),
    "auto_final_extra": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "6-9", {}, "AutoInitial and a named AutoFinal state are present, but the NL does not forbid an intermediate state or require a UML final pseudostate. The report turns a representational preference into a defect."),
    "auto_final_condition": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "6-12", {}, "AutoFinal is a named state and is referenced by the transition. The source does not prove that the phrase in the NL must mean a final pseudostate rather than this named state."),
    "auto_process_extra": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "7-9", {}, "The source contains an Auto Process Complete edge, but the NL does not prohibit an explicit completion event. Extra behavior alone is not a violated author obligation here."),
    "brake_extra_edges": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "8-12", {}, "The alleged extra edge is present, but the NL neither states that these events are impossible nor defines the complete post-clamping lifecycle. A strict absence-of-extra-behavior reading is not established."),
    "clamping_feedback_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "8-15", {}, "The NL says feedback returns to InitialState without naming a source state, supporting a global reading; a competing reading limits it to the explicitly described feedback paths. Both readings fit the source, so this remains D1 and novel."),
    "braking_feedback_bypass": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "8,13", {}, "The source permits BrakingState to go directly to InitialState on feedback, while NL sentence 3 explicitly requires entering ClampingState after entering BrakingState. The direct edge creates a path that bypasses that stated step."),
    "keyoff_initial": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "2-4", {"EIS-0042-01": "FULL_MATCH"}, "The only root edge is guarded/labeled keyOff, although NL assigns keyOff to turning off and says power-on enters Operate. The source therefore places the off event on the initial path and lacks the required cold-start interpretation."),
    "idle_brake": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "6-12", {}, "Idle has no brake edge, but the NL does not explicitly say whether braking is valid from Idle or only from AcceleratingOrCruising. The missing edge is a supported possible defect with a competent narrower-scope reading."),
    "pump_extra_region": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "4-17", {"EIS-0043-01": "FULL_MATCH"}, "The author source adds Region2 with Idle/Active and activation events not named in the five-line NL, while the required three names are placed under Region1. This changes the stated PumpControl decomposition."),
    "pump_direct_entry": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "4-10", {}, "PumpState has explicit conditional edges to WaterState and MethaneState inside the PumpControl structure. The NL does not require those edges to originate syntactically at the PumpControl boundary."),
    "pump_first_state": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "4-17", {"EIS-0043-02": "PARTIAL_MATCH"}, "PumpControl is split into orthogonal regions whose nested initial edges enter PumpState and Idle at once; the report's simultaneous-state wording is imprecise, but the source does not provide a single PumpControl-level first entry as required by NL sentence 3."),
    "emergency_action_text": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "20", {}, "The state annotation contains both Emergency Stop and send Obstacle Detected text. The report assumes a parser/action decomposition that the author source itself does not disprove; this is not enough for a defect claim."),
    "inmotion_initial": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "7-15", {"EIS-0044-01": "FULL_MATCH"}, "InMotion contains Accelerating, Cruising, and Approaching but no internal initial edge. NL requires the motion phase to begin in Accelerating, so entry into InMotion has no specified required child."),
    "approaching_hold": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "7-18", {}, "Approaching has do/Send and outer InMotion transitions to Stopping and EmergencyStopping. The source need not duplicate those external transitions inside Approaching to establish a separate hold defect."),
    "cook_time_display_0045": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-31", {"EIS-0045-01": "FULL_MATCH"}, "The NL explicitly requires cooking time to be displayed and updated, while the source has no variable, action, or effect for that data. A model-level state interpretation could be intended, so the evidence supports D1 rather than D2."),
    "cook_time_display_0055": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-24", {"EIS-0055-01": "FULL_MATCH"}, "The NL explicitly requires cooking time to be displayed and updated, while the source has no variable, action, or effect for that data. A model-level state interpretation could be intended, so the evidence supports D1 rather than D2."),
    "cook_cancel_update_0045": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "18-27", {"EIS-0045-01": "PARTIAL_MATCH"}, "The Cancel transition exists, but no effect states that cooking time is cancelled or updated. The target DoorShutWithItem could be read as an implicit cancellation, leaving two competent readings."),
    "cook_cancel_update_0055": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "18-24", {"EIS-0055-01": "PARTIAL_MATCH"}, "The Cancel transition exists, but no effect states that cooking time is cancelled or updated. The target DoorShutWithItem could be read as an implicit cancellation, leaving two competent readings."),
    "timer_start": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "27", {}, "The source has ReadytoCook -> Cooking : Start but no explicit timer action. Cooking can itself be read as the timer-running state, while the literal NL asks for timer start; both readings remain plausible."),
    "timer_stop": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "29", {}, "The source leaves Cooking on Door Opened but has no stop effect. Leaving the timer state can imply stopping, yet the NL states the stop action explicitly; this is D1, not an automatic invalidity."),
    "timer_start_stop": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "27,29", {}, "Start and stop are represented by state changes without explicit timer effects. State-entry/exit semantics and literal action semantics are both coherent readings."),
    "timer_expired": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "30", {}, "Timer Expired is named as an event, but the source does not define its clock origin. It can be an environment event or a missing model timer, so the normative failure is genuinely ambiguous."),
    "mission_extra_region": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "2-28", {}, "MissionRegion and its lifecycle edges are present, but the NL does not expressly forbid additional lifecycle states after mission completion. The report treats unspecified behavior as prohibited without a source obligation."),
    "mission_parallel_misread": ("A0", "REFUTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "2-25", {}, "The source has no -- separator between SearchRegion and MissionRegion, so they are not two parallel regions. The report's material simultaneous-parallel-state fact is refuted; the separate missing outer default issue is not silently substituted."),
    "search_idle_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "3-8", {}, "The source begins SearchRegion in Idle and requires Start Mission before Searching, whereas NL says search is continuous before completion. Idle can be pre-mission setup or an uncovered active state; both readings are source-compatible."),
    "uav_count_action": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "16", {}, "The slash label names UAV Count Decreased as an effect-like action, but no quantity variable or arithmetic is present. The textual action may be the intended abstraction; executable update semantics would support the report."),
    "search_continuity": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "2-28", {}, "The source has a SearchRegion and a MissionRegion with no clear task-start/completion synchronization. It can be read as an underspecified lifecycle or as an intentional abstract mission wrapper; D1 records both."),
    "search_region_count": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "2-25", {}, "Only two named composite states are present and no -- separator creates three regions. Whether NL's 'three state areas' means UML regions or broader logical areas is an evidence-backed ambiguity."),
    "mission_sync": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "22,27", {}, "Mission Completed is consumed both inside MissionRegion and by an outer SearchRegion edge, with no synchronization rule. A hierarchical event interpretation and a split-lifecycle interpretation both fit the source."),
    "flight_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "8-10", {}, "Searching consumes Task Assignment Received without a flight marker. Searching may be the intended flight state, but the NL's 'during flight' qualifier is not explicitly represented."),
    "collision_no_orthogonal": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "2-23", {}, "The three control blocks are placed in one composite body without a -- region separator. NL explicitly requires concurrent activation, so ordinary nested-state structure does not establish orthogonality."),
    "collision_activation": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "25-26", {"EIS-0047-03": "FULL_MATCH"}, "The root enters CollisionAvoidance unconditionally, while NL requires activation after one of three possible-collision detections. The source contains no trigger or guard for those conditions."),
    "collision_generic_event": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5,12,19", {}, "All three control blocks consume the same generic Collision Detected event, so the source does not preserve the NL distinction between frontend, rear-end, and pedestrian detection."),
    "collision_exit_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "23-26", {}, "The source has one composite exit event and no per-control completion relation. NL requires concurrent controls but does not say whether one or all controls end the submachine; the concern is a real ambiguity."),
    "highway_finish_exit": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "13-16", {"EIS-0049-01": "FULL_MATCH"}, "The source sends dist_to_exit<2 directly to FinishState, while NL reserves FinishState for auto_finished=true and separately says exit the highway. The source conflates highway exit with overall completion."),
    "urban_exit_hang": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "19-31", {}, "The source reaches exit_urban but never declares it or gives it a successor. NL explicitly requires the transition into exit_urban, so the reachable path is left semantically incomplete."),
    "intersection_lane_change": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "26-30", {}, "The source gives intersection only road_clear and auto_finished exits. NL explicitly gives the lane-change condition for straight, not intersection; applying it to every urban substate is possible but not compelled."),
    "highway_finish_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "8-16", {}, "The source omits auto_finished edges inside enter_hwy/lane_change, but an outer HighwayMode/AutonomousMode transition can cover descendants under composite semantics. The report's local-edge requirement and hierarchical reading both survive."),
    "urban_finish_scope": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "19-30", {}, "The source has completion behavior at a composite level only in some variants/paths. Applying the NL completion condition to every UrbanMode child is plausible, but the required scope is not explicit enough for D2."),
    "collision_unreachable_0049": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "2,37-41", {"VU-0049-01": "FULL_MATCH"}, "The root initial edge enters AutonomousMode and no edge enters the separate CollisionAvoidance block. Its internal initial edge cannot activate a parent that is never entered, contradicting the NL initial-state requirement."),
    "collision_unreachable_0059": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "3,37-41", {"VU-0059-03": "FULL_MATCH"}, "The root initial edge enters AutonomousMode and no edge enters the separate CollisionAvoidanceSystem block. Its internal initial edge cannot activate a parent that is never entered, contradicting the NL initial-state requirement."),
    "composite_finish_transition": ("A0", "REFUTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "8-17,19-35,43", {}, "The report claims no completion path from a nested child, but the source has a transition from the enclosing AutonomousMode; the source-level absence asserted by the report is therefore not established under composite-state semantics."),
    "composite_mode_transition": ("A0", "REFUTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "8-35", {}, "The source explicitly provides HighwayMode/UrbanMode composite transitions and each target has an initial child. The report treats lack of duplicated child edges as absence of behavior, which is not a supported material fact."),
    "urban_guard_overlap": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "21-27", {}, "The listed urban guards can overlap and have no priority. NL enumerates alternatives without requiring mutual exclusion, so nondeterministic choice is a live concern but not an unambiguous D2 defect."),
    "highway_false_case": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "10-14", {}, "The source lacks a transition for one input combination, but NL does not state what must happen when the front distance is below 25 and no extra lane exists. Missing unspecified behavior is not by itself a defect."),
    "auto_final_text": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "8-17", {"EIS-0050-01": "FULL_MATCH"}, "The return label is one free-text event label containing three alternatives, while NL gives three independently meaningful conditions. PlantUML label semantics and human-readable OR semantics support different readings."),
    "braking_extra_completion": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "9-15", {}, "Braking Complete is an added edge, but the NL does not prohibit a completion event after clamping. The report supplies no violated obligation beyond omission of that event from the prose."),
    "operate_initial_ambiguity": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "3-4", {}, "The source starts at Off and reaches Operate only on start, while NL says power-on enters Operate and separately assigns start to turning on. The two NL sentences support competing cold-start readings."),
    "shutdown_extra": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "14-15", {}, "The source adds shutdown from Off, but the NL does not state that no terminal shutdown event may exist. Extra unspecified behavior is not enough for invalidity."),
    "state_name_alias": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "6-11", {}, "Underscore spelling is a legal identifier representation for the displayed phrase and does not change the transition semantics. No explicit source obligation requires literal whitespace-preserving names."),
    "pump_parallel_misread": ("A0", "REFUTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "5-20", {}, "The source contains no -- separator; the three wrappers are not declared as parallel regions. The report's claimed simultaneous parallel activation is therefore false as stated."),
    "pump_cross_transition": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-19", {}, "The only edges in the source are three nested initial edges; no edge connects PumpState to WaterState or MethaneState. NL explicitly requires those conditional substate transitions."),
    "pump_wrapper_level": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "5-19", {}, "The required states are nested below wrapper states rather than directly declared under PumpControl. This is a concrete structural difference, but the NL does not define whether wrapper depth is semantically material."),
    "pump_initial_level": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-19", {"EIS-0053-01": "FULL_MATCH"}, "PumpControl has no level-local default edge; its three nested initial edges are inside wrapper states. The source therefore does not establish the required first PumpState entry at the PumpControl level."),
    "obstacle_guard_trigger": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "13-18", {"VU-0054-01": "FULL_MATCH"}, "The source writes [obstacle detected] as a guard with no trigger. Strict UML completion semantics and a common PlantUML condition reading produce different behavior, and NL itself uses condition wording without a signal name."),
    "emergency_do_entry": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "17-18", {}, "do actions occur while EmergencyStopping is active and can include the requested effects; an entry-action reading would require immediate one-shot semantics. The source supports both interpretations."),
    "approaching_send": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "10", {}, "do/Send is an activity annotation and is not explicitly typed as a signal send. It may nevertheless be the author's representation of the NL Send behavior, so this is D1."),
    "approaching_exit": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "4-15", {}, "The outer InMotion transitions can be taken while a descendant is active, and the NL supplies no named separate Approaching exit event. Lack of a duplicated child edge is not a defect."),
    "arrived_action_text": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "13-14", {}, "The transition label contains the exact Arrived/Stop, Send Arrived text from NL. The report's demand for a particular comma/action parser is not independently established as an author-source violation."),
    "closed_action_text": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "13", {}, "Closed/SendDeparted is the exact NL event/action spelling and can be read as that event followed by the action. No source fact shows a semantic mismatch."),
    "door_opened_name": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "12", {}, "Door Opened is the same phrase used by the NL for the DoorShut transition. The report itself acknowledges semantic consistency, so no defect is established."),
    "intercept_conflict": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-20", {"EIS-0056-01": "FULL_MATCH"}, "Intercepted is consumed by the internal NoIntercept edge and also by the outer SearchState edge with no distinguishing guard. The same event has competing destinations in one active configuration."),
    "uav_count_guard": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "20", {"EIS-0056-02": "FULL_MATCH"}, "Decrease UAV Count is inside brackets, the guard position, rather than after a slash as an effect. The source therefore does not unambiguously perform the required count decrease."),
    "mission_exit_priority": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "16,22", {}, "Mission Complete is an unconditional outer exit while other SearchState events can also be enabled. NL says search continues before completion but does not define event priority, leaving a real completion race interpretation."),
    "task_assignment_scope": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "5-19", {}, "A transition whose source is the composite SearchState is enabled while that composite is active, including descendants. The report's demand for one duplicate edge per area is not a source-level requirement."),
    "area_zero_time": ("D1", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "5-9", {"INS-0056-01": "PARTIAL_MATCH"}, "Area1, Area2, and Area3 form a label-free cycle. The report's fixed-order concern is supported, and the same edges also create a plausible zero-time completion-cycle defect; the relation is partial because the report does not state the full execution consequence."),
    "attack_failure_scope": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "19-20", {}, "The NL requires the completed-attack path and does not require failure or cancellation paths. A single specified completion edge is not evidence that omitted failure behavior is forbidden."),
    "collision_activation_partial": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "22", {"INS-0057-01": "PARTIAL_MATCH"}, "The root edge carries one broad collision label rather than the three NL detection conditions, and it is attached to the initial pseudostate. The report supports the activation mismatch; its focus is narrower than the full initial-edge language issue."),
    "highway_lane_change": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "10-14", {"EIS-0059-01": "FULL_MATCH"}, "enter_hwy has only an edge to cruise and no direct lane_change edge, although NL sentence 3 requires both alternatives based on distance and lane availability."),
    "highway_exit_hang": ("D2", "SUPPORTED", "SUPPORTED", "AUTHOR_SOURCE_DEFECT", "13-17", {}, "The source targets exit_hwy from highway children but never declares or exits that state. NL requires exiting the highway, so the source leaves that required path without a modeled continuation."),
    "collision_guard_brackets": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "37-40", {}, "The source wraps each disjunct in separate brackets rather than presenting one clearly grouped guard. A permissive parser may accept it, but the intended single OR guard is not unambiguously represented."),
    "collision_mode_names": ("D1", "SUPPORTED", "AMBIGUOUS", "AUTHOR_SOURCE_DEFECT", "37-40", {}, "The source uses in_highway/in_urban rather than an explicit state-context expression and defines no relation between those names and the current mode. Self-descriptive variable reading and strict binding reading both remain possible."),
    "collision_and_release": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "39-40", {}, "AND over three inactive indicators is a coherent reading of no active danger. The NL does not require an OR release rule, so the report does not establish a defect."),
    "finish_implicit_state": ("D0", "SUPPORTED", "NOT_ESTABLISHED", "NO_DEFECT_ESTABLISHED", "28-34", {}, "PlantUML permits a target state to be introduced by a transition, and the enclosing completion transitions are present. The report's demand for a separate declaration is a style/clarity preference, not a proven behavior failure."),
}


def code_decision(code: str) -> Dict[str, Any]:
    """Return a checked copy of one human-authored decision tuple."""
    tier, fact, normative, claim, lines, overrides, rationale = DECISIONS[code]
    if tier == "A0" and fact != "REFUTED":
        raise AssertionError(f"A0 requires a refuted fact: {code}")
    if tier != "A0" and fact != "SUPPORTED":
        raise AssertionError(f"non-A0 requires supported fact: {code}")
    if tier == "A0" and claim != "NO_DEFECT_ESTABLISHED":
        raise AssertionError(f"A0 cannot establish a defect: {code}")
    return {
        "d_tier": tier,
        "observed_fact_status": fact,
        "normative_violation_status": normative,
        "defect_claim_status": claim,
        "lines": lines,
        "relation_overrides": overrides,
        "rationale": rationale,
    }


def canonical_relation_digest(relations: Dict[str, Relation], ordered_ids: List[str]) -> str:
    """Hash the ordered dense relation vector."""
    payload = [[expected_id, relations[expected_id]] for expected_id in ordered_ids]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def main() -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ordered_ids = list(ledger["items"].keys())
    if len(ordered_ids) != 145:
        raise AssertionError(f"reference ledger expected 145 items, found {len(ordered_ids)}")

    source_meta: Dict[str, Dict[str, Any]] = {}
    for pair in sorted({key.split(":", 1)[0] for key in DECISION_CODES}):
        nl = SOURCE_ROOT / pair / "nl.txt"
        uml = SOURCE_ROOT / pair / "plantuml.puml"
        if not nl.is_file() or not uml.is_file():
            raise FileNotFoundError(f"missing author source for {pair}")
        nl_meta = read_source_metadata(nl)
        plantuml_meta = read_source_metadata(uml)
        source_meta[pair] = {
            "nl_path": f"reference/x1v2_input_closure/pairs/{pair}/nl.txt",
            "nl_sha256": nl_meta["sha256"],
            "nl_full_text_sha256": nl_meta["full_text_sha256"],
            "nl_line_count": nl_meta["line_count"],
            "plantuml_path": f"reference/x1v2_input_closure/pairs/{pair}/plantuml.puml",
            "plantuml_sha256": plantuml_meta["sha256"],
            "plantuml_full_text_sha256": plantuml_meta["full_text_sha256"],
            "plantuml_line_count": plantuml_meta["line_count"],
            "read_mode": "full_file_text_before_opinion",
        }

    reports: List[RawReportProposal] = []
    seen_keys = set()
    for raw_path in sorted(RAW_ROOT.glob("run*/**/record.json")):
        record = json.loads(raw_path.read_text(encoding="utf-8"))
        raw_pair_id = record["pair_id"]
        pair = pair_number(raw_pair_id)
        if not ("0040" <= pair <= "0059"):
            continue
        issues = record.get("parsed_output", {}).get("issues", [])
        if not isinstance(issues, list):
            raise AssertionError(f"non-list issues at {raw_path}")
        for index, issue in enumerate(issues):
            key = f"{pair}:r{record['round']}:i{index}"
            if key not in DECISION_CODES:
                raise AssertionError(f"missing explicit decision code for {key}")
            if key in seen_keys:
                raise AssertionError(f"duplicate raw report key {key}")
            seen_keys.add(key)
            code = DECISION_CODES[key]
            decision = code_decision(code)
            relations: Dict[str, Relation] = {expected_id: "NO_MATCH" for expected_id in ordered_ids}
            for expected_id, relation in decision["relation_overrides"].items():
                if expected_id not in relations:
                    raise AssertionError(f"relation override outside ledger: {expected_id}")
                relations[expected_id] = relation
            raw_record_relative = raw_path.relative_to(ARCHIVE).as_posix()
            local_report_id = issue.get("report_id") or issue.get("id") or f"baseline_issue_{index + 1}"
            raw_report_id = str(local_report_id)
            if ":" not in raw_report_id:
                raw_report_id = f"{pair}:r{record['round']}:{raw_report_id}"
            refs = [
                source_ref(pair, "nl.txt", source_meta[pair]["nl_sha256"], "1"),
                source_ref(pair, "plantuml.puml", source_meta[pair]["plantuml_sha256"], decision["lines"]),
            ]
            d_tier: TargetTier = decision["d_tier"]
            has_match = any(relation != "NO_MATCH" for relation in relations.values())
            proposed_validity = "INVALID" if d_tier in {"D0", "A0"} else ("VALID_KNOWN" if has_match else "VALID_NOVEL")
            opinion = ManualOpinion(
                observed_fact=(
                    f"Raw report {raw_report_id} at {key} claims: {issue.get('issue', '')}. "
                    f"Track B source reading: {decision['rationale']}"
                ),
                observed_fact_status=decision["observed_fact_status"],
                normative_violation_status=decision["normative_violation_status"],
                defect_claim_status=decision["defect_claim_status"],
                d_tier=d_tier,
                proposed_validity=proposed_validity,
                a0_reason="FALSE_POSITIVE" if d_tier == "A0" else None,
                reason=(
                    f"Independent Track B decision for raw pair {pair}, round {record['round']}, finding {index}: "
                    f"{decision['rationale']}"
                ),
                basis=(
                    f"Author-source basis is {refs[0].path}:{refs[0].lines} and "
                    f"{refs[1].path}:{refs[1].lines}; the exact raw report text is retained in raw_fields. "
                    f"The relation decision is made only after the fact/obligation reading: "
                    f"{decision['normative_violation_status']}."
                ),
                source_refs=refs,
                relation_overrides=decision["relation_overrides"],
            )
            report = RawReportProposal(
                reviewer_id="subagent:track-b-0040-0059",
                review_status="PROPOSAL",
                reference_visible=False,
                primary_visible=False,
                pair_id=pair,
                raw_pair_id=raw_pair_id,
                round=record["round"],
                finding_index=index,
                original_report_id=str(raw_report_id),
                raw_method_record_path=raw_record_relative,
                raw_json_pointer=f"/parsed_output/issues/{index}",
                raw_record_sha256=sha256_file(raw_path),
                raw_fields={
                    "issue": issue.get("issue"),
                    "where": issue.get("where"),
                    "reason": issue.get("reason"),
                    "basis": issue.get("basis") if "basis" in issue else None,
                    "basis_field_present": "basis" in issue,
                },
                author_source=source_meta[pair],
                proposal=opinion,
                all_expected_relations=relations,
                relation_digest_sha256=canonical_relation_digest(relations, ordered_ids),
            )
            reports.append(report)

    if len(reports) != len(DECISION_CODES):
        missing = sorted(set(DECISION_CODES) - seen_keys)
        extra = sorted(seen_keys - set(DECISION_CODES))
        raise AssertionError(f"coverage mismatch: reports={len(reports)} expected={len(DECISION_CODES)}, missing={missing}, extra={extra}")

    reports.sort(key=lambda report: (report.pair_id, report.round, report.finding_index))
    pair_counts = {pair: sum(report.pair_id == pair for report in reports) for pair in sorted(source_meta)}
    tier_counts: Dict[str, int] = {tier: 0 for tier in ("D2", "D1", "D0", "A0")}
    validity_counts = {"VALID_KNOWN": 0, "VALID_NOVEL": 0, "INVALID": 0}
    for report in reports:
        tier_counts[report.proposal.d_tier] += 1
        has_match = any(relation != "NO_MATCH" for relation in report.all_expected_relations.values())
        validity = "INVALID" if report.proposal.d_tier in {"D0", "A0"} else ("VALID_KNOWN" if has_match else "VALID_NOVEL")
        validity_counts[validity] += 1

    artifact = ProposalArtifact(
        artifact_schema_version="manual-adjudication-v3-baseline-ni/track-b-proposal-1",
        protocol_version="issue-189-195-baseline-ni-v3/raw-first-track-b",
            reviewer_id="subagent:track-b-0040-0059",
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        input_scope={
            "pair_min": "0040",
            "pair_max": "0059",
            "allowed_roots": [
                "raw/x1v2_baseline/method/run{1,2,3}/*/record.json",
                "reference/x1v2_input_closure/pairs/{0040..0059}/{nl.txt,plantuml.puml}",
                "reference/ledger.json",
            ],
            "source_pair_dirs_with_files": sorted(source_meta),
            "source_pair_dirs_without_files_or_reports": ["0048", "0058"],
        },
        non_k_membership_evidence_gap={
            "status": "OPEN_SELECTOR_GAP",
            "current_non_k_count": None,
            "statement": "The allowed raw/source/ledger inputs do not expose a frozen current-N/K selector. The 152 entries below are raw report candidates in the requested pair interval, not a claim that all 152 are confirmed current non-K.",
            "raw_candidate_coverage": "152/152",
            "no_silent_exclusion": True,
        },
        coverage={
            "raw_candidate_reports": len(reports),
            "proposal_reports": len(reports),
            "pair_counts": pair_counts,
            "expected_ids": len(ordered_ids),
            "dense_relations_per_report": len(ordered_ids),
            "dense_relation_cells": len(reports) * len(ordered_ids),
            "d_tier_counts": tier_counts,
            "proposed_validity_counts": validity_counts,
            "source_hash_coverage": f"{len(reports)}/{len(reports)}",
            "missing_evidence": [
                "Frozen current non-K membership selector is unavailable in the allowed inputs.",
                "No evidence outside author NL/PlantUML was used to promote an issue to W2; W is not decided here.",
            ],
        },
        ordered_expected_ids=ordered_ids,
        reports=reports,
        forbidden_inputs_read=[
            "v2 decisions or derived/manual_adjudication_v2",
            "v3 decisions and any other proposal JSON",
            "pane5 decision register",
            "Judge labels, Judge outputs, and Judge source-run summaries",
            "Track A/B/C reviewer conclusions",
        ],
        execution_boundary={
            "provider_calls": 0,
            "method_calls": 0,
            "judge_calls": 0,
            "raw_modified": False,
            "source_modified": False,
            "reference_modified": False,
            "proposal_is_final_human_adjudication": False,
        },
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact.model_dump(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT), "reports": len(reports), "expected_per_report": len(ordered_ids), "tiers": tier_counts, "validity": validity_counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
