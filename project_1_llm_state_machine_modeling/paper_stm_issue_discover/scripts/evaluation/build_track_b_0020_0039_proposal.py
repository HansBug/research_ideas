#!/usr/bin/env python3
"""Build the independent Track-B raw-first proposal for pairs 0020--0039.

The only semantic inputs allowed here are the frozen baseline method records,
the pair NL/PlantUML closure, the frozen reference ledger, and the protocol
documents named in the task.  The review table below is an explicit human
proposal table keyed by raw report identity.  This program only copies raw
text, computes hashes, expands the 145-position relation vector, and validates
that no report was silently omitted.

This is deliberately not a final adjudication and it does not select the
current non-K subset: raw records do not carry that membership, while v2/v3
decisions and other proposals are forbidden inputs for this track.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


PAPER = Path(__file__).resolve().parents[2]
ARCHIVE = PAPER / "final_results" / "v60_current_vs_x1v2_baseline"
RAW_ROOT = ARCHIVE / "raw" / "x1v2_baseline" / "method"
SOURCE_ROOT = ARCHIVE / "reference" / "x1v2_input_closure" / "pairs"
LEDGER_PATH = ARCHIVE / "reference" / "ledger.json"
OUT = ARCHIVE / "derived" / "manual_adjudication_v3_baseline_ni" / "proposals" / "track_b_0020_0039.json"

SCHEMA = "paper1.manual-adjudication.v3-baseline-ni.track-b-proposal.v1"
PROTOCOL = "issue-189-195-baseline-ni-v3"
REVIEWER = "track-b:raw-first-independent-0020-0039"


class RawText(BaseModel):
    """Verbatim four-field text copied from one frozen raw finding."""

    model_config = ConfigDict(extra="forbid")

    issue: str = Field(description="Verbatim raw issue text.")
    where: str = Field(description="Verbatim raw where text.")
    reason: str = Field(description="Verbatim raw reason text.")
    basis: str | None = Field(description="Verbatim raw basis text, or null when absent.")


class SourceRef(BaseModel):
    """Archive-relative source pointer and byte hash used by this proposal."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(description="Archive-relative path of an allowed evidence artifact.")
    json_pointer: str | None = Field(description="RFC 6901 pointer when the source is JSON, otherwise null.")
    line: int | None = Field(description="One-based source line when a stable line locus is used, otherwise null.", ge=1)
    sha256: str = Field(description="SHA-256 of the referenced artifact bytes.", pattern=r"^sha256:[0-9a-f]{64}$")


class RelationRow(BaseModel):
    """One explicit expected-specific relation in the dense 145-row vector."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="Expected ledger ID in frozen ledger order.")
    relation: Literal["FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"] = Field(description="Independent Track-B relation proposal.")


class PositiveRelation(BaseModel):
    """Evidence explanation for one proposed FULL or PARTIAL relation."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="Expected ledger ID for this positive relation.")
    relation: Literal["FULL_MATCH", "PARTIAL_MATCH"] = Field(description="Positive relation strength.")
    reason: str = Field(description="Report-specific semantic reason for this positive relation.", min_length=1)
    basis: str = Field(description="Source and expected-item basis for this positive relation.", min_length=1)


class TrackBReport(BaseModel):
    """One independent raw-first semantic proposal for one raw report."""

    model_config = ConfigDict(extra="forbid")

    side: Literal["x1v2_baseline"] = Field(description="Baseline side reviewed by Track B.")
    pair_id: str = Field(description="Four-digit pair ID from raw.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen method round.", ge=1, le=3)
    original_report_id: str = Field(description="Stable report identity constructed from pair, round, and finding index.")
    finding_index: int = Field(description="Zero-based index in parsed_output.issues.", ge=0)
    raw_method_path: str = Field(description="Archive-relative exact record.json path.")
    raw_json_pointer: str = Field(description="Pointer to exact raw finding object.")
    raw_sha256: str = Field(description="SHA-256 of exact raw record.", pattern=r"^sha256:[0-9a-f]{64}$")
    raw_text: RawText = Field(description="Verbatim raw issue/where/reason/basis.")
    observed_source_fact_status: Literal["ESTABLISHED", "REFUTED"] = Field(description="Track-B observation of the author-source fact.")
    observed_fact: str = Field(description="Report-specific source fact statement.", min_length=1)
    normative_violation_status: Literal["ESTABLISHED", "NOT_ESTABLISHED"] = Field(description="Track-B observation of a violated obligation.")
    d_tier: Literal["D2", "D1", "D0", "A0"] = Field(description="Track-B proposed D/A tier.")
    a0_type: Literal["FALSE_POSITIVE"] | None = Field(description="Baseline A0 subtype; null for non-A0 proposals.")
    validity_proposal: Literal["VALID_KNOWN", "VALID_NOVEL", "INVALID"] = Field(description="Provider-free closure proposal, not a frozen membership label.")
    relation_rows: tuple[RelationRow, ...] = Field(description="All 145 expected relations in ledger order.", min_length=145, max_length=145)
    relation_digest_sha256: str = Field(description="SHA-256 of canonical relation rows.", pattern=r"^sha256:[0-9a-f]{64}$")
    positive_relations: tuple[PositiveRelation, ...] = Field(description="Evidence for every positive relation row.")
    source_loci: tuple[str, ...] = Field(description="Source loci read for the report, including the raw where text.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Raw pointer, NL, PlantUML, and ledger evidence refs.", min_length=4)
    reason: str = Field(description="Dedicated Track-B report-level semantic reason.", min_length=1)
    basis: str = Field(description="Dedicated Track-B evidence basis naming exact source closure.", min_length=1)
    reviewer_id: Literal["track-b:raw-first-independent-0020-0039"] = Field(description="Independent Track-B reviewer identity.")
    review_status: Literal["PROPOSAL_ONLY"] = Field(description="Proposal only; cannot serve as final human adjudication.")
    v2_decisions_read: Literal[False] = Field(description="False: forbidden v2 decisions were not read.")
    v3_decisions_read: Literal[False] = Field(description="False: forbidden v3 decisions were not read.")
    other_proposals_read: Literal[False] = Field(description="False: other proposals and reviewer conclusions were not read.")
    provider_calls: Literal[0] = Field(description="Provider calls made for this proposal.")

    @model_validator(mode="after")
    def close_local_semantics(self) -> "TrackBReport":
        relations = {row.expected_id: row.relation for row in self.relation_rows}
        if len(relations) != 145:
            raise ValueError("each report must contain 145 unique relation IDs")
        positives = {row.expected_id: row.relation for row in self.positive_relations}
        if set(positives) != {key for key, value in relations.items() if value != "NO_MATCH"}:
            raise ValueError("positive relation evidence does not match dense rows")
        if self.d_tier == "A0":
            if self.observed_source_fact_status != "REFUTED" or self.a0_type != "FALSE_POSITIVE":
                raise ValueError("baseline A0 must be FALSE_POSITIVE with refuted fact")
        elif self.observed_source_fact_status != "ESTABLISHED" or self.a0_type is not None:
            raise ValueError("non-A0 must have established fact and no A0 subtype")
        expected_validity = "INVALID" if self.d_tier == "D0" or self.d_tier == "A0" else ("VALID_KNOWN" if positives else "VALID_NOVEL")
        if self.validity_proposal != expected_validity:
            raise ValueError("validity proposal is not closed from D/A and relation")
        if self.d_tier in {"D0", "A0"} and positives:
            raise ValueError("invalid proposal cannot have a positive relation")
        return self


class TrackBDocument(BaseModel):
    """Blind Track-B proposal envelope with explicit raw-coverage gaps."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal["paper1.manual-adjudication.v3-baseline-ni.track-b-proposal.v1"] = Field(description="Versioned Track-B proposal schema.")
    protocol_version: str = Field(description="D/A and relation protocol identifier.")
    proposal_status: Literal["PROPOSAL_ONLY"] = Field(description="This document is not final adjudication data.")
    reviewer_id: Literal["track-b:raw-first-independent-0020-0039"] = Field(description="Independent reviewer identity.")
    blindness: dict[str, object] = Field(description="Forbidden-input and zero-call assertions.")
    scope: dict[str, object] = Field(description="Raw range, present/missing pairs, and unresolved non-K membership.")
    allowed_inputs: tuple[str, ...] = Field(description="Only allowed raw/source/ledger/protocol input classes.", min_length=1)
    forbidden_inputs_not_read: tuple[str, ...] = Field(description="Forbidden artifact classes explicitly not read.", min_length=1)
    protocol_refs: tuple[SourceRef, ...] = Field(description="Protocol artifacts read for this independent review.", min_length=1)
    ledger: dict[str, object] = Field(description="Frozen ledger path/hash/count/order hash.")
    coverage: dict[str, object] = Field(description="Machine-checkable raw and evidence coverage.")
    reports: tuple[TrackBReport, ...] = Field(description="All raw reports actually reviewed in the requested range.", min_length=1)
    generation: dict[str, object] = Field(description="Provider-free generation metadata.")

    @model_validator(mode="after")
    def validate_document(self) -> "TrackBDocument":
        ids = [report.original_report_id for report in self.reports]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate report identity")
        if self.blindness.get("provider_calls") != 0:
            raise ValueError("provider call count must be zero")
        if self.forbidden_inputs_not_read == ():
            raise ValueError("forbidden-input declaration must be explicit")
        return self


def sha256(path: Path) -> str:
    """Return a prefixed SHA-256 digest for one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    """Hash canonical JSON using the archive's stable UTF-8 serialization."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def source_ref(path: Path, pointer: str | None = None) -> dict[str, Any]:
    """Create an archive-relative evidence pointer without copying secrets."""

    try:
        repository_path = path.relative_to(ARCHIVE).as_posix()
    except ValueError:
        repository_path = path.relative_to(PAPER).as_posix()
    return {"repository_path": repository_path, "json_pointer": pointer, "line": None, "sha256": sha256(path)}


def n(tier: str, reason: str, relations: dict[str, str] | None = None, basis: str | None = None) -> tuple[str, str, dict[str, str], str]:
    """Declare one explicit manual note; this helper performs no semantic inference."""

    return tier, reason, relations or {}, basis or reason


# Explicit Track-B reading table.  The index is the one-based issue position
# in the exact raw record.  Every enumerated report must have one entry; a
# missing entry is a hard build error rather than a generated default.
NOTES: dict[tuple[str, int, int], tuple[str, str, dict[str, str], str]] = {
    # 0020: takeover-condition ambiguity, extra event, and composite exit scope.
    ("0020", 1, 1): n("D1", "The source has the AutoFinalState-to-human edge, but the comma-separated label does not settle whether auto-final is an independent trigger or a source-state qualifier; EIS-0020-02 is the same condition ambiguity.", {"EIS-0020-02": "FULL_MATCH"}, "NL line 4 and PlantUML AutoFinalState -> HumanDrivingMode line are mutually readable as the two interpretations; exact raw pointer is retained.") ,
    ("0020", 1, 2): n("D1", "The source fact is the extra Signal Transmission Succeeds gate between the autonomous initial and operational states. The NL does not say whether this intermediate success event is required, so the omission/extra-gate claim remains a real but ambiguous obligation reading.", basis="NL lists entry into autonomous mode but does not define this extra gate; PlantUML explicitly contains AutoInitialState -> AutoOperationalState: Signal Transmission Succeeds.") ,
    ("0020", 1, 3): n("D0", "The parent-level AutonomousMode -> final Power Off edge is a source fact, but UML composite-state exit semantics can cover active descendants; no independent violated obligation remains after that closure check.", basis="PlantUML has the parent exit edge and no source evidence requiring one duplicated child edge per substate.") ,
    ("0020", 2, 1): n("D1", "The two takeover labels are source-real, but the wording permits both a conjunctive label and a reading in which the auto-final qualifier is carried by the source state; the ambiguity is substantive and matches EIS-0020-02.", {"EIS-0020-02": "FULL_MATCH"}, "The exact two edges and NL takeover sentence were compared; no old classification was used.") ,
    ("0020", 2, 2): n("D0", "The report treats an internal-to-external edge as lacking exit semantics, but the complete author source already gives explicit child-to-human transitions and a composite parent; the asserted defect is not compelled.") ,
    ("0020", 2, 3): n("D0", "Signal Transmission Succeeds is an additional source event, but the NL does not prohibit an implementation-level initialization event; its existence alone does not establish a violated obligation.") ,
    ("0020", 2, 4): n("D0", "Mission Completed and AutoFinalState are source-real refinements. The short NL mentions auto-final but does not forbid a named completion event, so this extra-event claim is not a demonstrated defect.") ,
    ("0020", 2, 5): n("D1", "The source uses one composite takeover label for steering and braking. Whether comma punctuation denotes conjunction or separate triggers is unresolved by the authored text, while the report identifies the same condition defect as EIS-0020-02.", {"EIS-0020-02": "FULL_MATCH"}, "NL takeover sentence and both exact transition labels were read together.") ,
    ("0020", 3, 1): n("D1", "AutoFinalState exists and the edge is present, but the label leaves the independent auto-final trigger versus source-state-qualifier reading unresolved; this is the EIS-0020-02 condition issue.", {"EIS-0020-02": "FULL_MATCH"}) ,
    ("0020", 3, 2): n("D1", "The source fact is the same comma-compressed takeover condition on both autonomous substates. The NL supports an independent-trigger reading, while the source syntax also supports a conjunctive reading; EIS-0020-02 is directly implicated.", {"EIS-0020-02": "FULL_MATCH"}) ,
    ("0020", 3, 3): n("D1", "The AutoFinalState completion edge is present but its handoff is still represented only by the ambiguous human steering/brake label. The report identifies the same auto-final takeover obligation as EIS-0020-02.", {"EIS-0020-02": "FULL_MATCH"}) ,

    # 0021: extra release edges and the ambiguous scope of feedback return.
    ("0021", 1, 1): n("D0", "Clamping Released is an explicit extra edge, but the author source contains no prohibition on a release recovery path; an unmentioned behavior is not by itself a violated obligation.") ,
    ("0021", 1, 2): n("D1", "BrakingState -> InitialState on Signal Feedback Sent is source-real and can bypass the required clamping path. The feedback sentence can also be read as a general return rule, so the scope of the violation is genuinely ambiguous.") ,
    ("0021", 2, 1): n("D0", "The extra Clamping Released recovery edge is confirmed in PlantUML, but the NL does not state that clamping release is forbidden; no source-backed defect obligation is established.") ,
    ("0021", 2, 2): n("D1", "The direct BrakingState feedback edge is present. Reading the NL feedback sentence as applying only to the failure/operational branch makes the bypass a defect, while a general feedback-return reading remains competent.") ,
    ("0021", 3, 1): n("D0", "Clamping Released is an unrequired but source-real recovery behavior. The specification is silent about that event and therefore does not establish a defect merely from its presence.") ,

    # 0022: PoweredOn/start scope and stopping wording.
    ("0022", 1, 1): n("D1", "The source inserts PoweredOn before Operate and gates it with start. NL sentence 1 says powered-on enters Operate while sentence 2 gives start as an on signal, leaving the two-event scope genuinely ambiguous.") ,
    ("0022", 1, 2): n("D1", "The source has accelerating/cruising, braking, and idle transitions but no literal stopping event. The NL may use stopping as the action that leads to idle, yet it does not define that equivalence explicitly.") ,
    ("0022", 2, 1): n("D1", "PoweredOn -> Operate: start is explicit in the source, but the NL separately says powered-on enters Operate and also names start as the on signal; the report exposes a real scope ambiguity rather than a false fact.") ,
    ("0022", 2, 2): n("D1", "The source omits a named stopping transition. `user idle` may represent stopping, but the authored NL distinguishes stopping from other actions only weakly, so both a defect and an abstraction reading survive.") ,
    ("0022", 3, 1): n("D1", "The same PoweredOn/start intermediate path is present. It conflicts with a literal powered-on-immediately-enters-Operate reading but can be reconciled with the separate start-signal sentence.") ,
    ("0022", 3, 2): n("D1", "The start edge is the only modeled turn-on path and is attached to PoweredOn. The report's claim about misplaced start semantics is supported structurally, but the NL leaves its relationship to power-on underspecified.") ,
    ("0022", 3, 3): n("D1", "No explicit stopping label exists in the Operate transitions. Treating user idle as stopping is possible, but not stated, so the omission remains a D1 proposal.") ,

    # 0023: initial-region interpretation and the three concrete dead ends.
    ("0023", 1, 1): n("D1", "The three -- separated initial branches are source-real and do not guarantee PumpState is first. The structure could be intended as concurrent regions or as three alternatives, so the ordering defect is D1 and does not itself identify the dead-end expected items.") ,
    ("0023", 1, 2): n("D2", "All three concrete substates are entered by initial edges and none has an outgoing transition; the parent and root also have no recovery edge. This is one source-level dead-end fact covering INS-0023-01, INS-0023-02, and INS-0023-03.", {"INS-0023-01": "FULL_MATCH", "INS-0023-02": "FULL_MATCH", "INS-0023-03": "FULL_MATCH"}) ,
    ("0023", 2, 1): n("D1", "The three initial branches remain source-real, but their `--` separators permit an orthogonal-region reading as well as an alternative-entry reading. The report is therefore a valid novel structural ambiguity, not one of the dead-end rows.") ,
    ("0023", 2, 2): n("D2", "The source has no transition between PumpState, WaterState, and MethaneState after their initial entry edges. The resulting three reachable states are all dead ends, directly covering the three expected dead-end findings.", {"INS-0023-01": "FULL_MATCH", "INS-0023-02": "FULL_MATCH", "INS-0023-03": "FULL_MATCH"}) ,
    ("0023", 2, 3): n("D1", "The `--` separators create a competent concurrent-region reading, while the NL describes selectable substates under one PumpControl. The source fact is real but the intended structural scope is ambiguous, so this remains novel.") ,

    # 0024: train-control action placement, exits, and the stopping dead end.
    ("0024", 1, 1): n("D2", "Obstacle Detected is used as the entry trigger and the required output is placed only on the EmergencyStopping exit edge; the authored source therefore does not represent the required entry-time signal. This is EIS-0024-04.", {"EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 1, 2): n("D2", "Emergency Stop is only a state description and the same source also adds an automatic EmergencyStopping exit carrying the output text. The misplaced output is EIS-0024-04 and the extra recovery edge is DIFF-0024-04.", {"EIS-0024-04": "FULL_MATCH", "DIFF-0024-04": "FULL_MATCH"}) ,
    ("0024", 1, 3): n("D2", "Approaching exits to InMotion with an exit action, although the NL requires remaining there while approaching. The edge both relocates Send and resets the motion phase, covering EIS-0024-02 and EIS-0024-03.", {"EIS-0024-02": "FULL_MATCH", "EIS-0024-03": "FULL_MATCH"}) ,
    ("0024", 1, 4): n("D2", "Send is carried only by the Approaching exit label, not by an action in the Approaching behavior. The output/trigger inversion is exactly EIS-0024-02.", {"EIS-0024-02": "FULL_MATCH"}) ,
    ("0024", 1, 5): n("D2", "The source contains no Entry/Accelerate action on entry to Accelerating; the only relevant text is a state description. This directly covers EIS-0024-01.", {"EIS-0024-01": "FULL_MATCH"}) ,
    ("0024", 1, 6): n("D2", "The same `Obstacle Detected` label is used as an input while the NL requires that phrase as an output after entering EmergencyStopping. The action/trigger inversion is EIS-0024-04.", {"EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 2, 1): n("D2", "The InMotion-to-EmergencyStopping label does not distinguish detection input from the required output signal. The source therefore misses the entry-time output, EIS-0024-04.", {"EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 2, 2): n("D2", "The source writes Emergency Stop as a state description rather than an entry or executable action. The claimed missing action is source-supported, but it is not the ledger's separate Send placement issue, so no expected relation is assigned.") ,
    ("0024", 2, 3): n("D2", "The EmergencyStopping -> InMotion exit edge is extra and carries the required output text in the wrong phase. It is the DIFF-0024-04 extra edge and EIS-0024-04 output-placement defect.", {"DIFF-0024-04": "FULL_MATCH", "EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 2, 4): n("D2", "Approaching is sent back to InMotion and the Send text is attached to the exit edge. This violates the remain behavior and reverses the output, covering EIS-0024-03 and EIS-0024-02.", {"EIS-0024-02": "FULL_MATCH", "EIS-0024-03": "FULL_MATCH"}) ,
    ("0024", 2, 5): n("D1", "The only Approaching exit is `exit/Send`; the source does not state a ready-to-stop or decelerate condition. The report's remain-until concern is directly tied to EIS-0024-03, but its exact lifecycle reading is weaker than a fully specified transition defect.", {"EIS-0024-03": "FULL_MATCH"}) ,
    ("0024", 2, 6): n("D2", "The source lacks Entry/Accelerate on the initial Accelerating entry, directly violating the explicit action placement in the NL. This is EIS-0024-01.", {"EIS-0024-01": "FULL_MATCH"}) ,
    ("0024", 2, 7): n("D2", "The only Send occurrence is an exit label from Approaching, so it cannot establish the required in-state output timing. This is EIS-0024-02.", {"EIS-0024-02": "FULL_MATCH"}) ,
    ("0024", 3, 1): n("D2", "Approaching -> InMotion: exit/Send both leaves the required persistent phase and places Send on the wrong side of the transition. It covers EIS-0024-03 and EIS-0024-02.", {"EIS-0024-02": "FULL_MATCH", "EIS-0024-03": "FULL_MATCH"}) ,
    ("0024", 3, 2): n("D2", "The obstacle detection edge uses the required output name as its trigger and provides no output action on entry. This is EIS-0024-04.", {"EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 3, 3): n("D2", "EmergencyStopping exits automatically and carries Obstacle Detected on the exit label, so the required signal is delayed/misclassified. The extra edge is DIFF-0024-04 and the output issue is EIS-0024-04.", {"DIFF-0024-04": "FULL_MATCH", "EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 3, 4): n("D1", "Both exit labels use action-like text in locations not authorized by the NL. The source fact supports the Send/output placement concerns, but the broad claim about all exit pseudo-state syntax is an interpretation-level extension.", {"EIS-0024-02": "FULL_MATCH", "EIS-0024-04": "FULL_MATCH"}) ,
    ("0024", 3, 5): n("D2", "The explicit Entry/Accelerate action is absent from the Accelerating entry and instead appears nowhere in the model. This is EIS-0024-01.", {"EIS-0024-01": "FULL_MATCH"}) ,

    # 0025: zero-time branch, cooking-time representation, and timer claims.
    ("0025", 1, 1): n("D1", "Door Closed has no zero-time guard, but the NL's `if` may be a sufficient condition and the state names may encode time status. The claim is the same guard relation as EIS-0025-01, with a surviving competent alternative reading.", {"EIS-0025-01": "FULL_MATCH"}) ,
    ("0025", 1, 2): n("D1", "The ReadytoCook branch has no explicit value/branch exclusion for zero time. It is materially related to the zero-time split in EIS-0025-01, but the NL does not fully specify whether zero is a valid Cooking Time Entered event.", {"EIS-0025-01": "PARTIAL_MATCH"}) ,
    ("0025", 1, 3): n("D1", "ReadytoCook -> DoorShutWithItem: Cancel carries no cancellation/update effect, while the NL requires cooking-time cancellation or update. This is the same represented cooking-time behavior as EIS-0025-02.", {"EIS-0025-02": "FULL_MATCH"}) ,
    ("0025", 1, 4): n("D1", "The source has a Cooking -> DoorOpenWithItem edge but no timer-stop action. The timer semantics are not represented in this state-only PlantUML, yet the protocol does not let missing backend support decide the validity; the precise timer claim is novel here.") ,
    ("0025", 1, 5): n("D0", "Timer Expired is already the transition trigger, and the NL does not separately require a completion effect on that edge. The source fact does not establish an additional violated obligation.") ,
    ("0025", 1, 6): n("D1", "The two DoorOpenWithItem branches do not show the zero-time distinction needed to disambiguate their destinations. This is a direct guard/branch relation to EIS-0025-01.", {"EIS-0025-01": "FULL_MATCH"}) ,
    ("0025", 2, 1): n("D1", "Door Closed is unguarded although the NL names zero time as the condition for DoorShutWithItem. The relation to EIS-0025-01 is direct.", {"EIS-0025-01": "FULL_MATCH"}) ,
    ("0025", 2, 2): n("D1", "Cooking Time Entered is not distinguished from the zero-time branch. It is related to the expected zero-time split, but the exact exclusion is not fully stated, so PARTIAL is appropriate.", {"EIS-0025-01": "PARTIAL_MATCH"}) ,
    ("0025", 3, 1): n("D1", "The Door Closed edge lacks the explicit zero-time condition, allowing the wrong branch when a nonzero time was entered. This directly matches EIS-0025-01.", {"EIS-0025-01": "FULL_MATCH"}) ,
    ("0025", 3, 2): n("D1", "The ReadytoCook edge does not make its time-value/branch relationship explicit. It is only partially attributable to EIS-0025-01 because the source may permit time entry while open.", {"EIS-0025-01": "PARTIAL_MATCH"}) ,
    ("0025", 3, 3): n("D1", "No variable, display, or update action carries cooking time in the source. The missing authored representation is EIS-0025-02.", {"EIS-0025-02": "FULL_MATCH"}) ,
    ("0025", 3, 4): n("D1", "The Cancel return edge has no cooking-time cancellation/update effect. This is a direct manifestation of EIS-0025-02.", {"EIS-0025-02": "FULL_MATCH"}) ,
    ("0025", 3, 5): n("D1", "Opening during Cooking has no timer-stop effect. The source supports a timer-side omission, but no ledger item in this pair identifies that exact timer action, so it remains novel.") ,
    ("0025", 3, 6): n("D1", "The source enters Cooking on Start but does not represent starting the timer. This is a specific timer-effect claim distinct from the ledger's cooking-time display/update item, so it remains novel.") ,

    # 0026: search regions, attack count, and formation-adjustment dead end.
    ("0026", 1, 1): n("D2", "SearchingState contains TargetSearchingState, FormationAdjustmentState, and AttackState as ordinary children, not three state areas. This directly covers EIS-0026-01.", {"EIS-0026-01": "FULL_MATCH"}) ,
    ("0026", 1, 2): n("D2", "AttackState -> TargetSearchingState has no count variable or update effect, despite the explicit NL requirement that UAV count decreases. This is EIS-0026-02.", {"EIS-0026-02": "FULL_MATCH"}) ,
    ("0026", 2, 1): n("D2", "FormationAdjustmentState is reachable from TargetSearchingState but has no outgoing transition, so interception permanently breaks the required continuing mission loop. This is EIS-0026-03.", {"EIS-0026-03": "FULL_MATCH"}) ,
    ("0026", 2, 2): n("D2", "The attack completion edge has no UAV-count update, directly covering EIS-0026-02.", {"EIS-0026-02": "FULL_MATCH"}) ,
    ("0026", 2, 3): n("D1", "The source has a Mission Completed edge, but the model does not explain the continuous-search boundary or count update. Those concerns are related to the region/count ledger items without uniquely identifying either one, so both relations are partial.", {"EIS-0026-01": "PARTIAL_MATCH", "EIS-0026-02": "PARTIAL_MATCH"}) ,
    ("0026", 3, 1): n("D2", "Attack completion returns to search without any count state or effect. This directly matches EIS-0026-02.", {"EIS-0026-02": "FULL_MATCH"}) ,
    ("0026", 3, 2): n("D2", "The source has only one search composite and leaves FormationAdjustmentState outside the continuing path with no return edge. It directly covers the three-region problem and the formation dead end, EIS-0026-01 and EIS-0026-03.", {"EIS-0026-01": "FULL_MATCH", "EIS-0026-03": "FULL_MATCH"}) ,

    # 0027: collision-control activation, completion lifecycle, and junctions.
    ("0027", 1, 1): n("D2", "The three control states immediately lead to undefined junctions and ActiveState has no complete exit lifecycle. This makes the activated submachine unusable and also instantiates the no-event junction transitions, covering EIS-0027-01 and INS-0027-04.", {"EIS-0027-01": "FULL_MATCH", "INS-0027-04": "FULL_MATCH"}) ,
    ("0027", 1, 2): n("D2", "`InitialState` is referenced as a target but is not declared in the author PlantUML. That is a real malformed-target defect, but it is distinct from the ledger's active-state lifecycle and no-event junction findings, so it remains novel.") ,
    ("0027", 2, 1): n("D1", "The source has an ActiveState with three separated regions, but its entry path does not explicitly connect the triggering event to each region. PlantUML implicit composite entry admits another reading, so this is a novel structural ambiguity.") ,
    ("0027", 2, 2): n("D1", "The three controls flow to undefined or incomplete junction targets, and the source does not define how an active control completes. This is materially the same lifecycle and no-event transition problem as EIS-0027-01 and INS-0027-04.", {"EIS-0027-01": "FULL_MATCH", "INS-0027-04": "FULL_MATCH"}) ,
    ("0027", 2, 3): n("D1", "The event label attaches `detected` only to the final collision phrase, while the NL speaks of detected possible collisions. The wording mismatch is source-real but not one of the two ledger defects, so it remains novel.") ,
    ("0027", 3, 1): n("D1", "The trigger text omits the NL's possible-collision qualification. This is a real semantic narrowing, but it is not the expected active-state lifecycle or junction row.") ,
    ("0027", 3, 2): n("D1", "The regions have initial arrows but no complete activation/exit semantics and their control targets are not wired into a finished lifecycle. It partially overlaps the expected active-state lifecycle issue without proving the exact same dead-end claim.", {"EIS-0027-01": "PARTIAL_MATCH"}) ,
    ("0027", 3, 3): n("D1", "The three controls are selected through a common Inactive state and each returns to that outer state, preventing concurrent activation. The source supports the core active-state lifecycle defect, EIS-0027-01.", {"EIS-0027-01": "FULL_MATCH"}) ,
    ("0027", 3, 4): n("D2", "The SensorControl path targets an undeclared InitialState, so the source does not provide a valid continuation. This is a malformed-target claim distinct from the expected lifecycle and no-event junction rows.") ,

    # 0029: highway/urban scopes, completion targets, and collision subsystem.
    ("0029", 1, 1): n("D1", "The two enter_hwy edges have identical guards, so the source cannot distinguish cruise from lane_change. The ambiguity directly matches EIS-0029-02.", {"EIS-0029-02": "FULL_MATCH"}) ,
    ("0029", 1, 2): n("D2", "The cruise edge uses dist_to_exit<2 to enter FinishState, while the NL reserves FinishState for auto_finished and otherwise says exit highway. This is EIS-0029-03.", {"EIS-0029-03": "FULL_MATCH"}) ,
    ("0029", 1, 3): n("D2", "The lane-change exit_hwy target has no declaration or continuation. The source defect is real, but the frozen expected rows in this pair cover a different cruise completion edge, entry guards, hierarchy, and collision reachability; it remains novel.") ,
    ("0029", 1, 4): n("D2", "The exit_urban target is undeclared and has no continuation. This is a distinct incomplete urban-exit path not represented by the listed ledger relations, so it remains novel.") ,
    ("0029", 1, 5): n("D1", "The source puts mode-switch edges on composite boundaries without naming internal source/target substates. The report identifies a real dynamic-switch scope ambiguity, but not the expected identical-guard or hierarchy defects.") ,
    ("0029", 1, 6): n("D2", "CollisionAvoidance is a top-level block with no incoming edge from the sole root initial path, so its required deactive/active behavior is unreachable. This directly covers INS-0029-01.", {"INS-0029-01": "FULL_MATCH"}) ,
    ("0029", 1, 7): n("D1", "The all-inactive guard is source-real, but the NL says no active danger and does not settle whether all three independent signals must be true. The conjunction claim is a valid novel ambiguity, not a ledger match.") ,
    ("0029", 2, 1): n("D1", "The identical enter_hwy guards create an unresolved choice between cruise and lane_change. This is the exact EIS-0029-02 relation.", {"EIS-0029-02": "FULL_MATCH"}) ,
    ("0029", 2, 2): n("D2", "The cruise-to-FinishState edge uses the exit-distance condition instead of auto_finished. This directly matches EIS-0029-03.", {"EIS-0029-03": "FULL_MATCH"}) ,
    ("0029", 2, 3): n("D2", "The declared exit_hwy target lacks a continuation, but the expected ledger does not contain this exact exit-path omission. It remains a valid novel source defect.") ,
    ("0029", 2, 4): n("D2", "The exit_urban target lacks a continuation, which is source-real but distinct from the frozen expected relations. It remains novel.") ,
    ("0029", 2, 5): n("D2", "The collision-avoidance composite is unreachable from the root, so the required initial deactive state cannot participate in execution. This is INS-0029-01.", {"INS-0029-01": "FULL_MATCH"}) ,
    ("0029", 3, 1): n("D2", "The cruise edge turns the highway-exit condition into global FinishState entry, contrary to the separate auto_finished completion condition. This is EIS-0029-03.", {"EIS-0029-03": "FULL_MATCH"}) ,
    ("0029", 3, 2): n("D2", "The exit_hwy state is declared but has no follow-up path. The omission is real but not one of the frozen expected relation identities.") ,
    ("0029", 3, 3): n("D2", "The exit_urban state is declared but has no follow-up path. It remains a valid novel incomplete-exit claim.") ,
    ("0029", 3, 4): n("D1", "InitialState is source-real but is a top-level sibling of AutonomousMode rather than its nested child. The hierarchy claim is a concrete ambiguity/defect, and it directly matches EIS-0029-01.", {"EIS-0029-01": "FULL_MATCH"}) ,
    ("0029", 3, 5): n("D2", "CollisionAvoidance has no reachable top-level entry or explicit parallel carrier, so its required active/deactive lifecycle is absent from the running model. This is INS-0029-01.", {"INS-0029-01": "FULL_MATCH"}) ,
    ("0029", 3, 6): n("D1", "The three inactive signals are conjoined in the source, but the NL does not define their aggregation as an all-of condition. This is a novel semantic ambiguity, not a frozen expected relation.") ,

    # 0030: autonomous final state, power-off coverage, and compressed takeover label.
    ("0030", 1, 1): n("D2", "Power Off is consumed only by HumanDriving; Autonomous and its children have no such edge. The global power-off requirement is EIS-0030-02.", {"EIS-0030-02": "FULL_MATCH"}) ,
    ("0030", 1, 2): n("D1", "The source compresses steering, brake, and `[*]` into one label and has no actual auto-final target. The label ambiguity is EIS-0030-03; the missing final carrier is separate.", {"EIS-0030-03": "FULL_MATCH"}) ,
    ("0030", 1, 3): n("D2", "Autonomous contains only Navigating and Parking and no final child or completion edge. The required auto-final carrier is absent, directly matching EIS-0030-01.", {"EIS-0030-01": "FULL_MATCH"}) ,
    ("0030", 2, 1): n("D2", "Only HumanDriving responds to Power Off, so the autonomous branch cannot reach final state on that event. This is EIS-0030-02.", {"EIS-0030-02": "FULL_MATCH"}) ,
    ("0030", 2, 2): n("D1", "The autonomous handoff conditions are one free-text label, not separate triggers. This is the same compressed-takeover relation as EIS-0030-03.", {"EIS-0030-03": "FULL_MATCH"}) ,
    ("0030", 2, 3): n("D2", "The only autonomous children are Navigating and Parking; the `[*]` in a label is not an authored final state. This directly covers EIS-0030-01.", {"EIS-0030-01": "FULL_MATCH"}) ,
    ("0030", 2, 4): n("D1", "The composite Autonomous has an external exit label but no explicit child-level final carrier. The claim is directly related to the missing auto-final expected issue, though the exact exit-scope interpretation is ambiguous.", {"EIS-0030-01": "FULL_MATCH"}) ,
    ("0030", 3, 1): n("D1", "The takeover label contains all three conditions as one free-text label, leaving independent trigger semantics unresolved. This is EIS-0030-03.", {"EIS-0030-03": "FULL_MATCH"}) ,
    ("0030", 3, 2): n("D2", "No autonomous final state exists; the nested initial `[*]` cannot serve as an auto-final condition. This is EIS-0030-01.", {"EIS-0030-01": "FULL_MATCH"}) ,
    ("0030", 3, 3): n("D2", "The autonomous block has no completion state or path at all. This is the same absent auto-final carrier as EIS-0030-01.", {"EIS-0030-01": "FULL_MATCH"}) ,

    # 0031: brake feedback scope and an explicit no-issue report.
    ("0031", 1, 1): n("D2", "The source permits BrakingState to return directly on feedback, bypassing the explicitly required transition to ClampingState. The report identifies a real control-flow violation.") ,
    ("0031", 1, 2): n("D0", "Transition Missing Feedback is an extra source edge, but the NL does not prohibit an additional recovery condition. Its presence alone does not establish a violated obligation.") ,
    ("0031", 2, 1): n("D0", "The same extra Transition Missing Feedback edge is source-real but not forbidden by the supplied NL. It is therefore D0, not A0.") ,
    ("0031", 2, 2): n("D2", "ClampingState returns only on the source's opposite `Transition Missing Feedback` label and has no Signal Feedback Sent return. The report's omission claim is supported by the authored feedback requirement.") ,
    ("0031", 3, 1): n("D0", "The report itself confirms that the Brake Signal Received edge has the required source and target. No violated obligation remains for this claim.") ,
    ("0031", 3, 2): n("D2", "The direct BrakingState -> InitialState feedback edge bypasses the mandatory ClampingState transition. The source and NL establish the control-flow defect.") ,
    ("0031", 3, 3): n("D2", "Transition Missing Feedback is not the NL's Signal Feedback Sent condition and is attached to the clamping return edge. The condition is semantically reversed.") ,
    ("0031", 3, 4): n("D2", "The clamping return uses the wrong feedback condition and therefore does not implement the stated feedback-to-initial behavior. The source fact and obligation are both explicit.") ,

    # 0032: nested regions and the Accelerating/Cruising split.
    ("0032", 1, 1): n("D1", "The NL names Accelerating or Cruising as one state phrase while the source splits it into two states and adds Reach Speed at region level. This directly matches DIFF-0032-03.", {"DIFF-0032-03": "FULL_MATCH"}) ,
    ("0032", 1, 2): n("D1", "The source has no Braking-to-accelerating path, but the NL gives only a general action-driven transition statement and does not require every reverse edge. The claim is a novel under-specification.") ,
    ("0032", 1, 3): n("D1", "Stop is only modeled from BrakeRegion, not from idle or acceleration. The source supports incomplete action scope, but the NL does not fix all stopping source states, so it remains novel.") ,
    ("0032", 2, 1): n("D1", "The source uses start from OffState while NL separately says powered-on enters Operate. The same two-sentence scope ambiguity remains a valid novel claim.") ,
    ("0032", 2, 2): n("D1", "The source places Reach Speed at AccelerateRegion level and has no AcceleratingState edge. This is the same split/refinement issue as DIFF-0032-03.", {"DIFF-0032-03": "FULL_MATCH"}) ,
    ("0032", 2, 3): n("D1", "No Cruising-to-Accelerating edge is authored, but the NL does not explicitly demand a reverse acceleration path. This is a valid novel omission claim, not a ledger match.") ,
    ("0032", 2, 4): n("D1", "The region-level Stop edge could be interpreted as applying to BrakingState through composite semantics, but the source does not make that carrier explicit. The claim is a novel clarity issue.") ,
    ("0032", 3, 1): n("D1", "OperateState contains three nested regions without default entries and AcceleratingState has no incoming edge. The missing-entry/source hierarchy issue directly matches EIS-0032-01.", {"EIS-0032-01": "FULL_MATCH"}) ,
    ("0032", 3, 2): n("D1", "IdleRegion leads to an AccelerateRegion with no initial or direct edge to AcceleratingState; the concrete Accelerating state cannot be reached. This is EIS-0032-01.", {"EIS-0032-01": "FULL_MATCH"}) ,
    ("0032", 3, 3): n("D1", "Stop is modeled only at BrakeRegion level, leaving its applicability to the other action states unresolved. The source supports a novel action-scope ambiguity.") ,

    # 0033: repeated PumpControl blocks and unmodeled in-parent transitions.
    ("0033", 1, 1): n("D2", "PumpControl is opened three times and the named substates are not reliably contained in one parent. This covers the hierarchy and repeated-block defects EIS-0033-01 and EIS-0033-02.", {"EIS-0033-01": "FULL_MATCH", "EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 1, 2): n("D2", "The source uses top-level PumpControl-to-child edges while also repeating child declarations inside PumpControl blocks. This is the same parent/child hierarchy failure as EIS-0033-01 and EIS-0033-02.", {"EIS-0033-01": "FULL_MATCH", "EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 1, 3): n("D2", "Three repeated parents each have a different initial target, so the source cannot guarantee first entry to PumpState. This directly covers EIS-0033-02.", {"EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 1, 4): n("D1", "The three exit-to-final edges are source-real extra terminal behaviors, but the NL does not expressly prohibit termination after stabilization/deactivation. The claim remains novel under a conservative obligation reading.") ,
    ("0033", 2, 1): n("D2", "The repeated PumpControl blocks prevent one parent from containing the three required substates. This directly covers EIS-0033-01 and EIS-0033-02.", {"EIS-0033-01": "FULL_MATCH", "EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 2, 2): n("D2", "The source has three initial declarations under repeated PumpControl blocks rather than one first PumpState entry. This is EIS-0033-02.", {"EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 2, 3): n("D2", "WaterState and MethaneState are initialized in separate repeated parents, not reached as alternatives inside one PumpControl. This covers EIS-0033-01.", {"EIS-0033-01": "FULL_MATCH"}) ,
    ("0033", 2, 4): n("D1", "The exit transitions are extra and have no corresponding parent-level return logic. Because the NL does not explicitly forbid a terminal stabilization behavior, this is a novel conservative claim.") ,
    ("0033", 3, 1): n("D2", "PumpControl is declared three times, each with a different initial child. The required single parent hierarchy and unique initial entry are both broken, covering EIS-0033-01 and EIS-0033-02.", {"EIS-0033-01": "FULL_MATCH", "EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 3, 2): n("D2", "External parent-to-child edges duplicate the separate repeated internal declarations, so the source cannot represent one coherent PumpControl hierarchy. This covers EIS-0033-01 and EIS-0033-02.", {"EIS-0033-01": "FULL_MATCH", "EIS-0033-02": "FULL_MATCH"}) ,
    ("0033", 3, 3): n("D2", "No transition connects PumpState to WaterState or MethaneState in the repeated-parent source. The required substate navigation is absent, but this is distinct from the ledger's hierarchy rows and remains novel.") ,

    # 0034: train-control action placement and termination claims.
    ("0034", 1, 1): n("D2", "DoorsClosing carries entry/Accelerate even though the NL assigns Entry/Accelerate to entering Accelerating. This directly matches EIS-0034-03.", {"EIS-0034-03": "FULL_MATCH"}) ,
    ("0034", 1, 2): n("D2", "The obstacle edge uses the output name as a trigger and does not send it on EmergencyStopping entry. This is EIS-0034-05.", {"EIS-0034-05": "FULL_MATCH"}) ,
    ("0034", 1, 3): n("D1", "Obstacle Cleared terminates EmergencyStopping, but the NL is silent about recovery/termination after an obstacle. The extra edge is a valid novel conservative claim.") ,
    ("0034", 1, 4): n("D2", "Accelerating is a top-level sibling rather than an InMotion child and is entered without the required motion-begins carrier. This covers EIS-0034-01 and EIS-0034-02.", {"EIS-0034-01": "FULL_MATCH", "EIS-0034-02": "FULL_MATCH"}) ,
    ("0034", 1, 5): n("D2", "InMotion has untriggered direct edges to Cruising and Approaching, allowing both to bypass the specified Accelerating path. This is EIS-0034-02.", {"EIS-0034-02": "FULL_MATCH"}) ,
    ("0034", 1, 6): n("D0", "Cruise appears as an entry action on Cruising, but the NL does not forbid an additional entry action corresponding to the transition signal. The fact is present without a compelled violation.") ,
    ("0034", 1, 7): n("D2", "Approaching uses entry/Decelerate and has no Send behavior. The misplaced entry action and missing output are EIS-0034-04.", {"EIS-0034-04": "FULL_MATCH"}) ,
    ("0034", 1, 8): n("D2", "Approaching -> Stopping uses Ready to Stop instead of the specified arrival transition and signal. The stopping edge is a dead-end path as well, covering INS-0034-01.", {"INS-0034-01": "FULL_MATCH"}) ,
    ("0034", 1, 9): n("D2", "Destination Missed exits Approaching before the specified ready-to-stop/decelerate boundary. This directly matches EIS-0034-06.", {"EIS-0034-06": "FULL_MATCH"}) ,
    ("0034", 1, 10): n("D2", "Approaching has no Send action and its exits do not express remaining until the specified boundary. The missing Send/action placement is EIS-0034-04.", {"EIS-0034-04": "FULL_MATCH"}) ,
    ("0034", 2, 1): n("D2", "DoorsClosing has the wrong entry action; the NL assigns Accelerate to entering Accelerating. This is EIS-0034-03.", {"EIS-0034-03": "FULL_MATCH"}) ,
    ("0034", 2, 2): n("D2", "Obstacle Detected is modeled as the input label while the required same-named signal is absent from EmergencyStopping behavior. This is EIS-0034-05.", {"EIS-0034-05": "FULL_MATCH"}) ,
    ("0034", 2, 3): n("D2", "Accelerating, Cruising, and Approaching are top-level states rather than children of an InMotion composite. This is EIS-0034-01.", {"EIS-0034-01": "FULL_MATCH"}) ,
    ("0034", 2, 4): n("D2", "Three untriggered InMotion edges permit direct entry to all phases and do not encode the motion-begins condition. This is EIS-0034-02.", {"EIS-0034-02": "FULL_MATCH"}) ,
    ("0034", 2, 5): n("D0", "Cruise is an entry action in the source, but the NL's signal/action notation does not explicitly prohibit repeating it on entry. No violated obligation is compelled.") ,
    ("0034", 2, 6): n("D2", "Approaching entry uses Decelerate and the source has no Send signal. This directly covers EIS-0034-04.", {"EIS-0034-04": "FULL_MATCH"}) ,
    ("0034", 2, 7): n("D0", "Ready to Stop is an additional transition label, but the NL says the system remains until ready to stop without prescribing whether that readiness is an event. The extra label alone is not a proven defect.") ,
    ("0034", 2, 8): n("D2", "Destination Missed terminates the model from Approaching before the specified stopping/deceleration boundary. This is EIS-0034-06.", {"EIS-0034-06": "FULL_MATCH"}) ,
    ("0034", 2, 9): n("D1", "Obstacle Cleared directly terminates EmergencyStopping, but the supplied NL does not define the post-clear behavior. The claim is a source-real novel concern, not an expected match.") ,
    ("0034", 2, 10): n("D2", "EmergencyStopping has only entry/Emergency Stop and never sends Obstacle Detected. This is EIS-0034-05.", {"EIS-0034-05": "FULL_MATCH"}) ,
    ("0034", 3, 1): n("D2", "DoorsClosing carries entry/Accelerate, which belongs to the Accelerating entry according to the NL. This is EIS-0034-03.", {"EIS-0034-03": "FULL_MATCH"}) ,
    ("0034", 3, 2): n("D2", "The obstacle edge uses the output signal name as its trigger and does not encode sending it on entry. This is EIS-0034-05.", {"EIS-0034-05": "FULL_MATCH"}) ,
    ("0034", 3, 3): n("D2", "EmergencyStopping only has entry/Emergency Stop; the required Obstacle Detected output is absent. This is EIS-0034-05.", {"EIS-0034-05": "FULL_MATCH"}) ,
    ("0034", 3, 4): n("D2", "The three phase states are outside an InMotion composite, so the required substate hierarchy is absent. This is EIS-0034-01.", {"EIS-0034-01": "FULL_MATCH"}) ,
    ("0034", 3, 5): n("D2", "The edge into Accelerating has no motion-begins/Entry carrier and the state is not nested under InMotion. It covers EIS-0034-02.", {"EIS-0034-02": "FULL_MATCH"}) ,
    ("0034", 3, 6): n("D2", "Approaching entry performs Decelerate while the NL requires Send during Approaching and does not assign Decelerate as an entry action. This is EIS-0034-04.", {"EIS-0034-04": "FULL_MATCH"}) ,
    ("0034", 3, 7): n("D0", "Ready to Stop is an authored extra event, but the NL's wording permits a readiness boundary without prescribing the exact label or transition. The claim does not establish a defect by itself.") ,
    ("0034", 3, 8): n("D2", "Destination Missed terminates Approaching without the NL's ready-to-stop/decelerate condition. This is EIS-0034-06.", {"EIS-0034-06": "FULL_MATCH"}) ,
    ("0034", 3, 9): n("D1", "Obstacle Cleared terminates the state machine, but the author source does not state whether a cleared obstacle should recover or end. It remains a valid novel concern under conservative semantics.") ,

    # 0035: frozen initial/door path, cooking-time representation, and timer extras.
    ("0035", 1, 1): n("D1", "The Door Closed edge lacks zero-time qualification, but the source's state naming and the NL's conditional wording leave a competent alternative reading. The claim matches EIS-0035-03.", {"EIS-0035-03": "FULL_MATCH"}) ,
    ("0035", 1, 2): n("D1", "ReadytoCook contains no authored cooking-time display/update carrier. This directly matches EIS-0035-04.", {"EIS-0035-04": "FULL_MATCH"}) ,
    ("0035", 1, 3): n("D1", "Cancel returns to DoorShutWithItem without a cooking-time cancellation/update action. This is the same data-action omission as EIS-0035-04.", {"EIS-0035-04": "FULL_MATCH"}) ,
    ("0035", 1, 4): n("D1", "Start enters Cooking but the source has no timer-start effect. This exact timer claim is distinct from the frozen display/update expected item and remains novel.") ,
    ("0035", 1, 5): n("D1", "Opening while Cooking has no timer-stop effect. This is a real timer-side omission, but no expected item in this pair identifies that exact operation, so it remains novel.") ,
    ("0035", 1, 6): n("D0", "The DoorOpen self-loop on Item Removed is an extra source edge, but the NL does not explicitly prohibit a no-op event in an already empty state. No violated obligation is established.") ,
    ("0035", 2, 1): n("D0", "The raw report confirms the Cancel self-loop agrees with the NL. The claimed subject is therefore not a defect.") ,
    ("0035", 2, 2): n("D2", "DoorOpen has no Door Closed -> DoorShut edge although the NL explicitly requires it. This is EIS-0035-02.", {"EIS-0035-02": "FULL_MATCH"}) ,
    ("0035", 2, 3): n("D1", "The Door Closed edge lacks the explicit zero-time condition and is directly related to EIS-0035-03.", {"EIS-0035-03": "FULL_MATCH"}) ,
    ("0035", 3, 1): n("D0", "Item Removed self-loops in DoorOpen, where the source already represents no item. The extra no-op is not prohibited by the supplied NL, so it is D0 rather than A0.") ,
    ("0035", 3, 2): n("D1", "Door Closed is unguarded despite the explicit zero-time condition for DoorShutWithItem. This is EIS-0035-03.", {"EIS-0035-03": "FULL_MATCH"}) ,

    # 0036: no pair-specific frozen expected rows; all claims are assessed as novel/invalid.
    ("0036", 1, 1): n("D2", "Region1 and Region2 are separate source composites with no connection from search to attack. The report establishes a real broken mission flow, but this pair has no ledger expected item for it.") ,
    ("0036", 1, 2): n("D2", "Only Region1 and Region2 are declared, while the NL explicitly asks for three state areas. This is a source-level novel defect.") ,
    ("0036", 1, 3): n("D2", "InitialState has no outgoing edge to either region, so the source's operational states are unreachable from the root. This is a novel reachability defect.") ,
    ("0036", 1, 4): n("D2", "There is no mission-completion boundary or continuous-search lifecycle connecting the source regions. The claim is source-supported and novel.") ,
    ("0036", 1, 5): n("D2", "FormationAdjustment returns only to TargetSearch inside Region1 and is not connected to the attack region. The report identifies a real end-to-end flow break, novel for this pair.") ,
    ("0036", 1, 6): n("D2", "The attack completion label mentions UAV Count Decreased but the source has no count variable or update effect. This is a valid novel data-action defect.") ,
    ("0036", 1, 7): n("D2", "AttackReady is only reachable as the initial child of the disconnected Region2 and has no source link from flight/search. The report's context defect is source-supported and novel.") ,
    ("0036", 2, 1): n("D2", "Only two regions are authored against the explicit three-region requirement. This is a novel structural defect.") ,
    ("0036", 2, 2): n("D2", "TargetSearch is isolated in Region1 and the root InitialState does not enter either region; the required pre-completion search lifecycle is absent. This is novel.") ,
    ("0036", 2, 3): n("D2", "The interception loop is local to Region1 and cannot be reached from the root or connected to attack. The report identifies a real novel lifecycle defect.") ,
    ("0036", 2, 4): n("D2", "Task Assignment Received is modeled only inside AttackReady, without any authored flight context. This is a source-level novel applicability defect.") ,
    ("0036", 2, 5): n("D2", "The count decrease is only label text on Attack -> AttackReady; there is no data carrier or update operation. This is novel.") ,
    ("0036", 2, 6): n("D2", "The source separates search and attack into unconnected top-level composites, so the described same-swarm workflow cannot be followed. This is novel.") ,
    ("0036", 3, 1): n("D2", "The source has two regions, not the three explicitly required. This is a novel structural defect.") ,
    ("0036", 3, 2): n("D2", "AttackReady is disconnected from TargetSearch and no flight state is represented. The report's broken task-assignment context is source-supported and novel.") ,
    ("0036", 3, 3): n("D2", "InitialState has no continuation into the two regions, and no connected lifecycle guarantees continuing search. This is novel.") ,
    ("0036", 3, 4): n("D2", "No task-completion state, event, or exit is authored. The report identifies a real novel lifecycle omission.") ,

    # 0037: collision regions are sequential children, not orthogonal controls.
    ("0037", 1, 1): n("D2", "The three collision regions are entered as alternatives from one Inactive state rather than as orthogonal concurrent regions. The resulting inability to run controls concurrently is EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 1, 2): n("D1", "The source labels confirmed Collision Detected rather than possible collision detected. This is a real trigger-scope issue, but distinct from the expected unreachable-control lifecycle.") ,
    ("0037", 1, 3): n("D2", "ActiveState first enters Inactive and only then chooses one collision branch; it does not carry the detected type into concurrent control regions. This is the expected broken activation behavior, EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 1, 4): n("D2", "Each control returns to the same outer Inactive state, so one control completion cannot preserve other concurrent controls. This is EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 2, 1): n("D2", "The three named regions are ordinary nested states selected from Inactive, not orthogonal active-mode regions. This directly covers EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 2, 2): n("D1", "The source uses one generic Collision Detected entry and then three mutually exclusive typed entries, omitting the possible-collision qualification. The trigger issue is real but distinct from EIS-0037-01.") ,
    ("0037", 2, 3): n("D2", "Control completion targets outer Inactive and destroys any possibility of independent concurrent lifecycles. This is EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 3, 1): n("D2", "The three control containers are nested ordinary states and selected sequentially from Inactive; the source lacks orthogonal region semantics. This is EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 3, 2): n("D2", "ActiveState is entered through a generic event and then chooses one branch, so the three possible collision types are not carried into concurrent controls. This is EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,
    ("0037", 3, 3): n("D2", "The three Inactive-to-collision edges form an alternative choice and each control returns to the common Inactive state. That source structure directly prevents concurrent activation, EIS-0037-01.", {"EIS-0037-01": "FULL_MATCH"}) ,

    # 0039: dynamic switch claim, duplicate root initial edges, and guard syntax.
    ("0039", 1, 1): n("D1", "The source has no HighwayMode-to-UrbanMode or reverse edge; the only mode edges originate at AutonomousMode. The absence is real, but it is not the expected parent-boundary reentry issue, so it remains novel.") ,
    ("0039", 2, 1): n("D2", "Two top-level initial pseudo-state edges share the same root without an orthogonal carrier, giving the model competing global starts. This is DIFF-0039-04.", {"DIFF-0039-04": "FULL_MATCH"}) ,
    ("0039", 3, 1): n("D1", "The source still lacks direct HighwayMode/UrbanMode dynamic transitions. The report's missing-switch claim is real, but it does not match the expected edge-reentry relation.") ,
    ("0039", 3, 2): n("D1", "exit_urban is declared as an internal target but has no continuation. The source supports an incomplete exit lifecycle, distinct from the frozen expected rows.") ,
    ("0039", 3, 3): n("D1", "The mode-qualified front-distance expression is free-text PlantUML syntax rather than an explicit Boolean carrier. The claim is an independent semantic ambiguity and not one of the expected rows.") ,
}


def load_json(path: Path) -> Any:
    """Load JSON from an allowed frozen artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict[str, Any]:
    """Enumerate raw reports and materialize the explicit Track-B notes."""

    ledger_doc = load_json(LEDGER_PATH)
    ledger_ids = list(ledger_doc["items"])
    if len(ledger_ids) != 145:
        raise AssertionError(f"expected 145 ledger IDs, got {len(ledger_ids)}")
    ledger_sha = sha256(LEDGER_PATH)
    reports: list[dict[str, Any]] = []
    present_pairs: list[str] = []
    missing_pairs: list[str] = []
    raw_paths: list[str] = []

    for pair_int in range(20, 40):
        pair = f"{pair_int:04d}"
        record_paths = sorted(RAW_ROOT.glob(f"run*/{pair}-*/record.json"))
        if not record_paths:
            missing_pairs.append(pair)
            continue
        present_pairs.append(pair)
        nl_path = SOURCE_ROOT / pair / "nl.txt"
        puml_path = SOURCE_ROOT / pair / "plantuml.puml"
        if not nl_path.exists() or not puml_path.exists():
            raise AssertionError(f"source closure unexpectedly missing for present raw pair {pair}")
        for record_path in record_paths:
            raw_paths.append(record_path.relative_to(ARCHIVE).as_posix())
            record = load_json(record_path)
            round_no = int(record["round"])
            for finding_index, raw_issue in enumerate(record["parsed_output"]["issues"]):
                issue_no = finding_index + 1
                key = (pair, round_no, issue_no)
                if key not in NOTES:
                    raise AssertionError(f"missing explicit Track-B note for {pair}:r{round_no}:baseline_issue_{issue_no}")
                tier, review_reason, positive_map, review_basis = NOTES[key]
                report_id = f"{pair}:r{round_no}:baseline_issue_{issue_no}"
                raw_rel = record_path.relative_to(ARCHIVE).as_posix()
                rows = [{"expected_id": expected_id, "relation": positive_map.get(expected_id, "NO_MATCH")} for expected_id in ledger_ids]
                positives = [
                    {
                        "expected_id": expected_id,
                        "relation": relation,
                        "reason": f"{report_id}: the source-located claim is materially related to {expected_id} under the independent Track-B reading; this is {relation}.",
                        "basis": f"{review_basis} Expected item {expected_id} was read from reference/ledger.json; raw pointer {raw_rel}#/parsed_output/issues/{finding_index}; NL {nl_path.relative_to(ARCHIVE).as_posix()}; PlantUML {puml_path.relative_to(ARCHIVE).as_posix()}.",
                    }
                    for expected_id, relation in positive_map.items()
                ]
                observed_established = tier != "A0"
                validity = "INVALID" if tier in {"D0", "A0"} else ("VALID_KNOWN" if positive_map else "VALID_NOVEL")
                source_refs = [
                    source_ref(record_path, f"/parsed_output/issues/{finding_index}"),
                    source_ref(record_path, f"/parsed_output/issues/{finding_index}/issue"),
                    source_ref(record_path, f"/parsed_output/issues/{finding_index}/where"),
                    source_ref(nl_path),
                    source_ref(puml_path),
                    source_ref(LEDGER_PATH),
                ]
                reports.append(
                    {
                        "side": "x1v2_baseline",
                        "pair_id": pair,
                        "round": round_no,
                        "original_report_id": report_id,
                        "finding_index": finding_index,
                        "raw_method_path": raw_rel,
                        "raw_json_pointer": f"/parsed_output/issues/{finding_index}",
                        "raw_sha256": sha256(record_path),
                        "raw_text": {
                            "issue": raw_issue.get("issue", ""),
                            "where": raw_issue.get("where", ""),
                            "reason": raw_issue.get("reason", ""),
                            "basis": raw_issue.get("basis"),
                        },
                        "observed_source_fact_status": "ESTABLISHED" if observed_established else "REFUTED",
                        "observed_fact": f"{report_id}: {review_reason}",
                        "normative_violation_status": "NOT_ESTABLISHED" if tier in {"D0", "A0"} else "ESTABLISHED",
                        "d_tier": tier,
                        "a0_type": "FALSE_POSITIVE" if tier == "A0" else None,
                        "validity_proposal": validity,
                        "relation_rows": rows,
                        "relation_digest_sha256": canonical_sha(rows),
                        "positive_relations": positives,
                        "source_loci": [str(raw_issue.get("where", "")), review_basis],
                        "source_refs": source_refs,
                        "reason": f"{report_id}: {review_reason}",
                        "basis": f"{report_id}: {review_basis} Exact source closure: NL={nl_path.relative_to(ARCHIVE).as_posix()} sha256={sha256(nl_path)}; PlantUML={puml_path.relative_to(ARCHIVE).as_posix()} sha256={sha256(puml_path)}; raw={raw_rel} sha256={sha256(record_path)}; ledger={LEDGER_PATH.relative_to(ARCHIVE).as_posix()} sha256={ledger_sha}.",
                        "reviewer_id": REVIEWER,
                        "review_status": "PROPOSAL_ONLY",
                        "v2_decisions_read": False,
                        "v3_decisions_read": False,
                        "other_proposals_read": False,
                        "provider_calls": 0,
                    }
                )

    expected_keys = set(NOTES)
    actual_keys = {(item["pair_id"], item["round"], int(item["original_report_id"].rsplit("_", 1)[1])) for item in reports}
    if expected_keys != actual_keys:
        raise AssertionError(f"explicit notes and raw inventory differ: notes-only={sorted(expected_keys-actual_keys)} raw-only={sorted(actual_keys-expected_keys)}")
    ordered_protocol = [
        "discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md",
        "discover_matrix/docs/protocol/dtier_triage.md",
        "discover_matrix/docs/protocol/defect_taxonomy.md",
        "discover_matrix/docs/protocol/verdict_methodology.md",
    ]
    protocol_refs = [source_ref(PAPER / path) for path in ordered_protocol]
    doc = {
        "schema": SCHEMA,
        "protocol_version": PROTOCOL,
        "proposal_status": "PROPOSAL_ONLY",
        "reviewer_id": REVIEWER,
        "blindness": {
            "raw_first": True,
            "v2_decisions_read": False,
            "v3_decisions_read": False,
            "track_a_read": False,
            "other_reviewer_conclusions_read": False,
            "judge_labels_read": False,
            "provider_calls": 0,
            "method_reruns": 0,
            "judge_reruns": 0,
        },
        "scope": {
            "requested_pair_range": ["0020", "0039"],
            "requested_pair_ids": [f"{i:04d}" for i in range(20, 40)],
            "present_pair_ids": present_pairs,
            "missing_pair_ids": missing_pairs,
            "raw_report_count": len(reports),
            "raw_report_coverage": "205/205 enumerated reports with readable pair source closure",
            "current_non_k_membership": "UNRESOLVED_BLIND_SCOPE",
            "current_non_k_coverage": "NOT_ASSERTED",
            "coverage_gap": "Allowed raw records do not encode frozen current K/N/I membership. Selecting only current non-K would require forbidden v2/v3 decisions or labels; this Track-B artifact therefore reports all raw reports in the requested pair range and does not claim that all are current non-K.",
        },
        "allowed_inputs": (
            "raw/x1v2_baseline/method/run*/record.json",
            "reference/x1v2_input_closure/pairs/<pair>/nl.txt",
            "reference/x1v2_input_closure/pairs/<pair>/plantuml.puml",
            "reference/ledger.json",
            "discover_matrix/docs/protocol/*.md",
        ),
        "forbidden_inputs_not_read": (
            "derived/manual_adjudication_v2/**",
            "derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json",
            "derived/manual_adjudication_v3_baseline_ni/proposals/track_a_0020_0039.json",
            "derived/manual_adjudication_v3_baseline_ni/proposals/track_b_0000_0019.json",
            "pane5_decision_register.json",
            "raw/x1v2_baseline/judge/**",
            "other reviewer conclusions or labels",
        ),
        "protocol_refs": protocol_refs,
        "ledger": {
            "repository_path": LEDGER_PATH.relative_to(ARCHIVE).as_posix(),
            "sha256": ledger_sha,
            "expected_count": len(ledger_ids),
            "ordered_expected_ids_sha256": canonical_sha(ledger_ids),
            "ordered_expected_ids": ledger_ids,
        },
        "coverage": {
            "reports_enumerated": len(reports),
            "reports_with_dedicated_opinion": len(reports),
            "reports_with_145_relation_rows": len(reports),
            "source_pairs_read": len(present_pairs),
            "source_pairs_missing": missing_pairs,
            "raw_fields_read_per_report": ["issue", "where", "reason", "basis"],
            "raw_pointer_hash_closure": True,
            "nl_plantuml_hash_closure": True,
            "explicit_notes_only": True,
            "a0_reports": sum(item["d_tier"] == "A0" for item in reports),
            "d2_reports": sum(item["d_tier"] == "D2" for item in reports),
            "d1_reports": sum(item["d_tier"] == "D1" for item in reports),
            "d0_reports": sum(item["d_tier"] == "D0" for item in reports),
            "positive_relation_reports": sum(bool(item["positive_relations"]) for item in reports),
        },
        "reports": reports,
        "generation": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "generator": "scripts/evaluation/build_track_b_0020_0039_proposal.py",
            "provider_calls": 0,
            "method_reruns": 0,
            "judge_reruns": 0,
            "semantic_decisions_source": "explicit Track-B raw-first review table in this script; no heuristic classifier",
        },
    }
    return TrackBDocument.model_validate(doc).model_dump(mode="json")


def main() -> None:
    """Build and write the provider-free Track-B proposal artifact."""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    document = build()
    OUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "path": OUT.relative_to(ARCHIVE).as_posix(), "reports": len(document["reports"]), "expected_rows_per_report": 145, "provider_calls": 0, "missing_pairs": document["scope"]["missing_pair_ids"]}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
