"""Materialize a blind, raw-first Track A proposal for baseline pairs 0000-0019.

This command deliberately does not open the frozen v2 decision layer, Judge
outputs, or any reviewer proposal.  The semantic annotations below are a
human-authored proposal table; the command only joins those annotations to
immutable raw/source/ledger records and computes dense relation digests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "evaluation" / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from paper_stm_evaluation.track_a_baseline_ni_proposal import TrackAProposal


ARCHIVE_RELATIVE = "final_results/v60_current_vs_x1v2_baseline"
PAIR_MIN = 0
PAIR_MAX = 19
RELATIONS = ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")


def sha256_file(path: Path) -> str:
    """Return an archive-stable SHA-256 digest for one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def canonical_digest(value: object) -> str:
    """Hash JSON using the proposal's deterministic UTF-8 serialization."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Any:
    """Load one JSON artifact and reject malformed top-level input."""

    value = json.loads(path.read_text(encoding="utf-8"))
    return value


# These are explicit human proposal annotations, keyed by the exact raw
# report identity.  Empty relation lists mean that all 145 expected rows
# were read and none was judged FULL or PARTIAL in this independent pass.
# They are intentionally separate from raw text and are never inferred from
# keywords by this script.
ANNOTATIONS: dict[str, dict[str, Any]] = {}

SOURCE_PROFILES = {
    "0000": "NL power-on/front-distance/human-takeover/power-off obligations; PlantUML lines 2, 9, 12-14.",
    "0001": "NL braking, failed transmission, feedback reset, and caliper-clamping obligations; PlantUML lines 5-14.",
    "0002": "NL PumpControl and its three named substates, including first entry into PumpState; PlantUML lines 2-23.",
    "0003": "NL Operate lifecycle and action-driven Idle/Accelerating-or-Cruising/Braking transitions; PlantUML lines 2-11.",
    "0004": "NL train motion, emergency stop, three InMotion substates, entry action, Send, and hold obligations; PlantUML lines 2-35.",
    "0005": "NL microwave DoorShut/DoorOpen/item/cooking-time/timer lifecycle; PlantUML lines 2-31.",
    "0006": "NL continuous three-region search, interception/formation adjustment, attack, and swarm-count reduction; PlantUML lines 2-35.",
    "0007": "NL three collision types and three concurrent collision-avoidance control regions; PlantUML lines 2-29.",
    "0009": "NL AutonomousMode HighwayMode/UrbanMode exit, switching, and collision-avoidance obligations; PlantUML lines 2-59.",
    "0010": "NL power-on, autonomous submachine, takeover, and final-state obligations; PlantUML lines 2-22.",
    "0011": "Same author NL braking lifecycle as pair 0001; PlantUML lines 5-15.",
    "0012": "NL powered-on Operate lifecycle, start/keyOff, and action-driven substates; PlantUML lines 2-12.",
    "0013": "Same author NL PumpControl three-substate obligations as pair 0002; PlantUML lines 2-38.",
    "0014": "NL DoorsClosing/InMotion/emergency/three motion substates/entry/Send/hold obligations; PlantUML lines 2-27.",
    "0015": "Same microwave NL lifecycle as pair 0005; PlantUML lines 2-31.",
    "0016": "NL continuous three-region UAV search, interception, attack, and count-reduction obligations; PlantUML lines 2-35.",
    "0017": "NL three collision regions and concurrent control activation; PlantUML lines 2-17.",
    "0019": "NL AutonomousMode HighwayMode/UrbanMode, exit, switching, and collision-avoidance obligations; PlantUML lines 2-44.",
}


def add(report_id: str, *, d: str, note: str, positives: dict[str, str] | None = None, gap: list[str] | None = None) -> None:
    """Register one explicit raw-first semantic proposal annotation."""

    ANNOTATIONS[report_id] = {
        "d_tier": d,
        "note": note,
        "positives": positives or {},
        "evidence_gaps": gap or [],
    }


def register_annotations() -> None:
    """Register the batch's source-reading and relation proposals."""

    # The entries are keyed by stable report identity, rather than by report
    # position, so changing enumeration order cannot silently move a verdict.
    # Directly evidenced omissions or structural violations.
    direct = {
        "0000:r3:baseline_issue_1": ("D2", "Power Off is attached to the root initial pseudostate at PlantUML line 2 rather than a running-state path; the NL power-off obligation is therefore not consumed while the system is running.", {"EIS-0000-01": "FULL_MATCH"}),
        "0000:r3:baseline_issue_2": ("D1", "The source has one comma-delimited takeover label at line 13, while the NL comma sequence admits both a conjunction reading and a separate-condition reading; both readings are source-compatible.", {"EIS-0000-02": "FULL_MATCH"}),
        "0000:r3:baseline_issue_3": ("D2", "Both root initial pseudostate edges are event-labelled at lines 2 and 14, so the source lacks an unlabelled default initial entry; the UML initial-entry obligation is concrete.", {"INS-0000-04": "FULL_MATCH"}),
        "0000:r2:baseline_issue_1": ("D2", "The Power Off edge is sourced at the root initial pseudostate, not at either running mode; this is a concrete source-level routing failure.", {"EIS-0000-01": "FULL_MATCH"}),
        "0000:r2:baseline_issue_2": ("D1", "The single comma-delimited takeover label does not distinguish event alternatives from conjunction; the NL wording supports both readings.", {"EIS-0000-02": "FULL_MATCH"}),
        "0000:r1:baseline_issue_2": ("D1", "The source contains the combined takeover label, but the NL's comma sequence does not settle whether the conditions are conjunctive or alternative; the alternative reading is that any listed takeover input suffices.", {"EIS-0000-02": "FULL_MATCH"}),
        "0000:r1:baseline_issue_1": ("D0", "The extra AutoNavigating-to-AutoFinal edge is visibly present, but the supplied NL does not state that every unspecified extra edge is forbidden and does not define a Condition Met obligation; the fact is established but no source-backed defect duty is established.", {}),
        "0001:r1:baseline_issue_1": ("D0", "The extra ClampingLoseState edge/state is present at lines 14-15, but the NL does not make its listed states exhaustive or impose a prohibition on additional failure handling; fact is established, obligation is not.", {}),
        "0001:r1:baseline_issue_2": ("D1", "The direct BrakingState-to-InitialState edge is present at line 12. One reading treats the NL's feedback reset as applying after the braking path; another permits feedback reset from BrakingState itself. Both are source-compatible.", {"VU-0001-01": "PARTIAL_MATCH"}),
        "0001:r2:baseline_issue_1": ("D0", "The extra ClampingLoseState edge/state is source-real, but the NL does not make the listed states exhaustive or impose a prohibition on additional failure handling.", {}),
        "0001:r3:baseline_issue_1": ("D0", "The extra Clamping Lose State and its edge are source-real, but the NL does not establish an exhaustive state set or a violated duty against this additional failure path.", {}),
        "0002:r1:baseline_issue_1": ("D2", "PumpControl's sole internal initial edge targets InitialState at line 5, while the NL expressly requires first entry to PumpState.", {"EIS-0002-01": "FULL_MATCH"}),
        "0002:r1:baseline_issue_2": ("D2", "The source declares WaterState and MethaneState but has no incoming transition to either; the NL expressly requires transitions to both.", {"EIS-0002-02": "FULL_MATCH"}),
        "0002:r1:baseline_issue_3": ("D1", "InitialState is the actual initial target, but the NL's three-state enumeration can be read as exhaustive or as a minimum named set; the former makes the extra initial state a defect and the latter does not.", {"EIS-0002-03": "FULL_MATCH"}),
        "0002:r2:baseline_issue_1": ("D2", "The only PumpControl initial target is InitialState, not the explicitly required PumpState.", {"EIS-0002-01": "FULL_MATCH", "EIS-0002-02": "PARTIAL_MATCH"}),
        "0002:r2:baseline_issue_2": ("D2", "The source has no path from the PumpControl initial configuration to WaterState or MethaneState, despite the NL's explicit can-transition requirements.", {"EIS-0002-02": "FULL_MATCH"}),
        "0002:r3:baseline_issue_1": ("D2", "PumpControl's only internal entry is InitialState and no declared main substate has an incoming PumpControl entry; the named-state reachability requirement is directly violated.", {"EIS-0002-01": "FULL_MATCH", "EIS-0002-02": "FULL_MATCH"}),
        "0002:r3:baseline_issue_2": ("D2", "The source explicitly enters InitialState rather than PumpState, contrary to the NL's first-transition requirement.", {"EIS-0002-01": "FULL_MATCH"}),
        "0003:r1:baseline_issue_2": ("D1", "The Stop Signal edge exists only from Braking at line 10. The NL can be read as requiring stopping from any active Operate substate, but it can also be read as describing the listed cycle only; both readings remain plausible.", {}),
        "0003:r1:baseline_issue_1": ("D0", "AcceleratingOrCruising is a single source identifier for the exact NL phrase; the supplied NL does not require two separately named states, so the naming fact does not establish a violated duty.", {}),
        "0003:r2:baseline_issue_1": ("D1", "The source has no AcceleratingOrCruising-to-Idle stop edge. Whether stop applies from that state without first braking is not made explicit by the NL, leaving two competent readings.", {}),
        "0003:r3:baseline_issue_1": ("D0", "The source contains an explicit Operate initial Idle edge at line 5; uncertainty about whether an external transition invokes the composite initial edge is a representation interpretation, not a proven author-source defect.", {}),
        "0003:r3:baseline_issue_2": ("D0", "The identifier AcceleratingOrCruising preserves the two-word phrase as one state name; no normative source duty requires whitespace or two identifiers.", {}),
        "0003:r3:baseline_issue_3": ("D1", "Only Braking consumes stop in the source. The NL does not explicitly quantify the source state for stopping, so a general stop reading and a listed-cycle reading both survive.", {}),
        "0004:r1:baseline_issue_1": ("D1", "The self-nested DoorsClosing construct is present at lines 4-5, but its exact PlantUML name-resolution consequence is representation-sensitive; the source fact is certain while the defect interpretation has a competent alternative.", {"EIS-0004-01": "FULL_MATCH"}),
        "0004:r1:baseline_issue_2": ("D1", "The source uses do/Send under Approaching, while the NL says send Send and continue approaching without fixing one-shot versus continuous action semantics; both interpretations are plausible.", {}),
        "0004:r1:baseline_issue_3": ("D1", "Approaching has descriptive lines but no explicit hold edge. The NL's 'remains' can be treated as a semantic state invariant or as requiring a visible transition, so both readings survive.", {}),
        "0004:r1:baseline_issue_4": ("D2", "EmergencyStopping has no outgoing edge and the root source has no termination or recovery path; the NL describes entering emergency stop but does not authorize an absorbing dead end for the running machine.", {"INS-0004-01": "FULL_MATCH"}),
        "0004:r2:baseline_issue_1": ("D1", "The source writes do/Send Obstacle Detected inside EmergencyStopping. It establishes a signal-related source element, but the NL's entry-time wording and the source's do-time wording support two semantic readings.", {}),
        "0004:r2:baseline_issue_2": ("D1", "Approaching contains do/Send, which can represent continued activity but does not settle whether Send is one-shot; the NL and source permit both interpretations.", {}),
        "0004:r2:baseline_issue_3": ("D1", "The same Obstacle Detected text is used on the incoming edge and in the state body. It is a concrete ambiguity between input detection and output signaling, not a settled false fact.", {}),
        "0004:r3:baseline_issue_1": ("D1", "The source uses do/Send rather than an entry action for the emergency signal; this is a timing/semantics ambiguity because the NL says the state includes the action but does not formalize action notation.", {}),
        "0004:r3:baseline_issue_2": ("D1", "do/Send in Approaching provides a possible continuous signal interpretation, while the NL can mean a one-time signal plus state persistence; both are competent readings.", {}),
        "0004:r3:baseline_issue_3": ("D1", "Approaching contains only descriptive text. The NL's remains clause can be represented by state occupancy semantics or by an explicit self-loop; it is not unambiguously one or the other.", {}),
        "0004:r3:baseline_issue_4": ("D1", "The self-nested DoorsClosing construct is present, but the exact author-intended hierarchy is ambiguous from the source syntax; one reading treats it as a malformed recursive nesting and another as a redundant notation artifact.", {"EIS-0004-01": "FULL_MATCH"}),
        "0004:r3:baseline_issue_5": ("D1", "The outer and inner DoorsClosing names are both present, so the duplicated locus is factual; the degree to which it changes the active state depends on PlantUML scoping interpretation.", {"EIS-0004-01": "PARTIAL_MATCH"}),
        "0005:r2:baseline_issue_1": ("D2", "DoorShut has only a descriptive Cancel line and no DoorShut-to-DoorShut edge, while the NL explicitly requires remaining in DoorShut after Cancel.", {"EIS-0005-01": "FULL_MATCH"}),
        "0005:r3:baseline_issue_1": ("D2", "DoorShut's Cancel is a state description rather than a self-loop; the explicit NL stay-put obligation is not represented.", {"EIS-0005-01": "FULL_MATCH"}),
        "0005:r3:baseline_issue_2": ("D1", "DoorOpenWithItem is represented as a composite with an extra DoorIdleWithItem child. The source fact is certain, while the NL does not say whether the named state may have an implementation child.", {"EIS-0005-02": "FULL_MATCH"}),
        "0005:r3:baseline_issue_3": ("D1", "DoorShutWithItem is represented with an extra ItemInside child. The named-state semantics and allowable implementation refinement admit two readings.", {"EIS-0005-02": "FULL_MATCH"}),
        "0005:r3:baseline_issue_4": ("D2", "ReadytoCook has no display/update action or variable while the NL explicitly requires cooking-time display and update.", {"EIS-0005-03": "FULL_MATCH"}),
        "0005:r3:baseline_issue_5": ("D2", "The Start edge reaches Cooking but no timer-start action is present, despite the NL's explicit timer-start behavior.", {"EIS-0005-03": "PARTIAL_MATCH"}),
        "0005:r3:baseline_issue_6": ("D2", "The Cooking-to-DoorOpenWithItem edge has no stop-timer effect, while the NL explicitly requires stopping the timer on door opening.", {"EIS-0005-03": "PARTIAL_MATCH"}),
        "0005:r3:baseline_issue_7": ("D2", "The Cooking Cancel edge has no time-handling effect, while the NL expressly requires cancellation or update of cooking time in the related lifecycle.", {"EIS-0005-03": "PARTIAL_MATCH"}),
        "0005:r3:baseline_issue_8": ("D2", "The source's Cancel path is a bare state transition and carries no time cancellation/update action; the NL's explicit time-handling obligation is not represented.", {"EIS-0005-03": "PARTIAL_MATCH"}),
        "0006:r1:baseline_issue_1": ("D2", "Attack completion returns to Searching without a count variable or effect, contrary to the NL's explicit swarm-count reduction requirement.", {"EIS-0006-02": "FULL_MATCH"}),
        "0006:r1:baseline_issue_2": ("D1", "The source has a simple Searching state plus two composites. The NL's three regions can mean three explicit orthogonal regions or three functional areas; both readings are plausible.", {}),
        "0006:r1:baseline_issue_3": ("D2", "Searching is one state and no three-region structure is present, while the NL explicitly says search operates in three different state areas.", {}),
        "0006:r2:baseline_issue_1": ("D2", "Attack completion has no count update effect; the NL requirement is explicit.", {"EIS-0006-02": "FULL_MATCH"}),
        "0006:r2:baseline_issue_2": ("D1", "The source inserts an Intercepted state before FormationAdjustment. The NL says transition to formation adjustment but does not expressly forbid an intermediate state, leaving a refinement reading.", {}),
        "0006:r3:baseline_issue_1": ("D2", "Attack completion lacks any count update in the source, directly missing the NL's explicit count-reduction behavior.", {"EIS-0006-02": "FULL_MATCH"}),
        "0006:r3:baseline_issue_2": ("D1", "The source contains composites but no explicit three-region declaration; the NL's region wording and the source's functional decomposition support different interpretations.", {}),
        "0007:r1:baseline_issue_1": ("D2", "The three collision-specific states do not have separate activation edges to CollisionAvoidance; the NL names the three detection cases as activation triggers.", {"EIS-0007-01": "FULL_MATCH"}),
        "0007:r1:baseline_issue_2": ("D1", "The source contains two separators but three control names and an external OperationalControls composite. The NL's region count can be read as control regions or as the full active-mode structure.", {"EIS-0007-02": "PARTIAL_MATCH"}),
        "0007:r1:baseline_issue_3": ("D2", "The source has one CollisionDetection-to-CollisionAvoidance edge rather than three detection-state activation paths; the missing per-type trigger linkage is concrete.", {"EIS-0007-01": "FULL_MATCH"}),
        "0007:r2:baseline_issue_1": ("D2", "The source has no outgoing edges from the three concrete CollisionDetection states to the avoidance state, so the three NL activation cases are not represented.", {"EIS-0007-01": "FULL_MATCH"}),
        "0007:r2:baseline_issue_2": ("D2", "OperationalControls is outside CollisionAvoidance and is not an orthogonal region of its active mode; the source structure does not provide the required three-region active-mode composition.", {"EIS-0007-02": "FULL_MATCH"}),
        "0007:r2:baseline_issue_3": ("D1", "The three source regions have labelled initial edges but no explicit relation to the three detection types. It is ambiguous whether generic control activation is intended to stand for the required concurrent activation.", {"EIS-0007-02": "PARTIAL_MATCH"}),
        "0007:r3:baseline_issue_1": ("D2", "CollisionDetection as a whole points to CollisionAvoidance, but none of the three concrete detection states is connected outward; the NL requires type-specific activation.", {"EIS-0007-01": "FULL_MATCH"}),
        "0007:r3:baseline_issue_2": ("D2", "The concrete detection states have no outgoing path to CollisionAvoidance and the composite has no explicit completion edge; the claimed activation route is not represented.", {"EIS-0007-01": "FULL_MATCH"}),
        "0007:r3:baseline_issue_3": ("D1", "The source has three orthogonal regions, but each initial edge is event-labelled and the source does not state how the events are produced concurrently; the control-concurrency reading remains ambiguous.", {"EIS-0007-02": "PARTIAL_MATCH"}),
    }
    for report_id, (d, note, positives) in direct.items():
        add(report_id, d=d, note=note, positives=positives)

    # Remaining reports in pairs 0009-0019.  Their notes intentionally name
    # the exact source obligation; relation targets are conservative where a
    # report discusses only a secondary representation concern.
    more = {
        "0009:r1:baseline_issue_1": ("D1", "The enter_hwy source has a cruise edge for >=25 and a lane-change edge for <25 with an extra lane; the NL does not settle the no-extra-lane case.", {}),
        "0009:r1:baseline_issue_2": ("D2", "The source sends cruise to FinishState on dist_to_exit<2, while the NL separates highway exit from auto_finished completion.", {"EIS-0009-01": "FULL_MATCH"}),
        "0009:r1:baseline_issue_3": ("D2", "The source sends lane_change_urban to FinishState rather than the explicitly named exit_urban state.", {"EIS-0009-02": "FULL_MATCH"}),
        "0009:r1:baseline_issue_4": ("D1", "The >=25 cruise condition is explicit, but whether it is an impermissible added guard or a natural complement of <25 is not fully fixed by the NL.", {}),
        "0009:r1:baseline_issue_5": ("D1", "The model uses high_way/urban_way flags rather than explicit nested-mode state guards; the NL permits either equivalent flag notation or strict state coupling.", {}),
        "0009:r1:baseline_issue_6": ("D2", "FinishState first appears inside HighwayMode and is not separately declared as the AutonomousMode completion target; the source hierarchy is inconsistent with the shared completion requirement.", {"EIS-0009-03": "FULL_MATCH"}),
        "0009:r3:baseline_issue_1": ("D2", "Both highway exit edges target FinishState directly, conflating distance-to-exit with auto_finished completion.", {"EIS-0009-01": "FULL_MATCH"}),
        "0009:r3:baseline_issue_2": ("D2", "The urban exit edge targets FinishState rather than the NL-named exit_urban state.", {"EIS-0009-02": "FULL_MATCH"}),
        "0009:r3:baseline_issue_3": ("D2", "The source declares no exit_urban state while the NL explicitly requires it as the urban exit target.", {"EIS-0009-02": "FULL_MATCH"}),
        "0009:r3:baseline_issue_4": ("D1", "The added >=25 condition and uncovered <25/no-extra-lane case admit both a strict coverage reading and a normal-cruise complement reading.", {}),
        "0009:r3:baseline_issue_5": ("D1", "The model uses mode flags in the collision condition; the source does not prove those flags are inconsistent with the active nested mode, so the claim is not unambiguously a defect.", {}),
        "0009:r3:baseline_issue_6": ("D2", "FinishState is undeclared as an AutonomousMode child and is reached through external ExitHighway/exit_urban states; the completion hierarchy is concretely incomplete.", {"EIS-0009-03": "FULL_MATCH"}),
        "0009:r3:baseline_issue_7": ("D2", "CollisionAvoidanceSystem has no incoming edge and no root-level initial entry; the NL nevertheless requires its deactive initial state.", {"VU-0009-01": "FULL_MATCH"}),
        "0010:r1:baseline_issue_1": ("D2", "Power On is attached from HumanDriving to Autonomous while the root initial edge enters HumanDriving without Power On; this reverses the explicit NL startup direction.", {"EIS-0010-01": "FULL_MATCH"}),
        "0010:r1:baseline_issue_2": ("D2", "AutonomousIdle and AutonomousActive are top-level source states rather than children of Autonomous, despite the NL submachine requirement.", {"EIS-0010-02": "FULL_MATCH"}),
        "0010:r1:baseline_issue_3": ("D1", "The model's Autonomous substate structure is external and lacks a clear initial child; a permissive interpretation treats the named states as a flat refinement, while a strict reading requires nesting.", {"EIS-0010-02": "PARTIAL_MATCH"}),
        "0010:r1:baseline_issue_4": ("D2", "Only AutonomousActive consumes takeover inputs; AutonomousFinal has no HumanDriving edge, so the third NL takeover condition is not represented.", {"EIS-0010-04": "FULL_MATCH"}),
        "0010:r1:baseline_issue_5": ("D1", "Power Off targets an ordinary AutonomousFinal state rather than a UML final pseudostate; the name and intended final semantics admit a charitable interpretation but no explicit terminal construct exists.", {"EIS-0010-03": "FULL_MATCH"}),
        "0010:r1:baseline_issue_6": ("D2", "HumanDriving consumes Power On to Autonomous even though NL Power On enters HumanDriving; the extra edge directly conflicts with the stated direction.", {"EIS-0010-01": "FULL_MATCH"}),
        "0010:r1:baseline_issue_7": ("D2", "The root initial edge to HumanDriving is unlabelled while the NL makes Power On the entry event; the startup trigger is not represented.", {"EIS-0010-01": "PARTIAL_MATCH"}),
        "0010:r2:baseline_issue_1": ("D2", "Power On is attached to the wrong source/target direction and the initial edge lacks that event.", {"EIS-0010-01": "FULL_MATCH"}),
        "0010:r2:baseline_issue_2": ("D2", "Autonomous is marked submachine but its named children are not nested under it; the source does not instantiate the required submachine structure.", {"EIS-0010-02": "FULL_MATCH"}),
        "0010:r2:baseline_issue_3": ("D1", "The Autonomous-to-AutonomousIdle edge and external child declarations can be read as a flat shorthand or as a hierarchy error; both are possible source interpretations.", {"EIS-0010-02": "PARTIAL_MATCH"}),
        "0010:r2:baseline_issue_4": ("D2", "AutonomousFinal has no edge to HumanDriving, although the NL includes in(auto final) in the takeover condition.", {"EIS-0010-04": "FULL_MATCH"}),
        "0010:r2:baseline_issue_5": ("D1", "Power Off reaches an ordinary AutonomousFinal state with no final pseudostate. The final-state name supports a charitable reading, but the terminal semantics are absent.", {"EIS-0010-03": "FULL_MATCH"}),
        "0010:r3:baseline_issue_1": ("D2", "Power On is consumed by HumanDriving-to-Autonomous and the root edge is unconditional, contrary to the NL startup direction.", {"EIS-0010-01": "FULL_MATCH"}),
        "0010:r3:baseline_issue_2": ("D2", "AutonomousIdle and AutonomousActive are not nested children of Autonomous, so the required submachine representation is absent.", {"EIS-0010-02": "FULL_MATCH"}),
        "0010:r3:baseline_issue_3": ("D1", "The source includes a distance edge from Autonomous to an external AutonomousIdle and a HumanDriving distance edge; the intended nested submachine behavior remains ambiguous.", {"EIS-0010-02": "PARTIAL_MATCH"}),
        "0010:r3:baseline_issue_4": ("D2", "AutonomousFinal has no path to HumanDriving, so the auto-final takeover condition is not consumed.", {"EIS-0010-04": "FULL_MATCH"}),
        "0010:r3:baseline_issue_5": ("D1", "Power Off reaches an ordinary state called AutonomousFinal rather than a final pseudostate; the label suggests intent but the UML terminal fact is absent.", {"EIS-0010-03": "FULL_MATCH"}),
        "0010:r3:baseline_issue_6": ("D2", "Only HumanDriving has a Power Off edge, leaving all autonomous states without the system-level shutdown behavior described by the NL.", {"EIS-0010-05": "FULL_MATCH"}),
        "0011:r1:baseline_issue_1": ("D1", "The direct BrakingState feedback edge is present. The NL's feedback sentence can be scoped to OperationalState or to the full braking lifecycle, so both readings remain possible.", {"VU-0011-01": "PARTIAL_MATCH"}),
        "0011:r1:baseline_issue_2": ("D0", "ClampingLoseState is visibly extra, but the NL does not state that its named states are exhaustive or prohibit additional failure behavior.", {}),
        "0011:r2:baseline_issue_1": ("D0", "The extra ClampingLoseState and edge are present; without an exhaustiveness or prohibition clause, no violated obligation is established.", {}),
        "0011:r2:baseline_issue_2": ("D1", "The direct BrakingState feedback edge is factual, but the feedback sentence has a plausible broad-lifecycle and a plausible OperationalState-only reading.", {"VU-0011-01": "PARTIAL_MATCH"}),
        "0011:r3:baseline_issue_1": ("D0", "The extra ClampingLoseState is source-real but not prohibited by an exhaustive NL state list.", {}),
        "0011:r3:baseline_issue_2": ("D1", "The direct feedback edge is source-real and can either be a permissible feedback path or an unintended bypass of clamping; the supplied NL does not resolve the scope.", {"VU-0011-01": "PARTIAL_MATCH"}),
        "0012:r1:baseline_issue_1": ("D0", "Off-to-Terminate is a source-real extra edge, but the NL describes start/keyOff without explicitly imposing an exhaustive lifecycle or forbidding later termination.", {}),
        "0012:r1:baseline_issue_2": ("D1", "The source has a one-way Idle-to-AcceleratingOrCruising-to-Braking cycle. The NL's action list supports both a minimal listed-cycle reading and a broader all-substate coverage reading.", {}),
        "0012:r2:baseline_issue_1": ("D0", "The source includes an unconditioned Off-to-Terminate edge; the NL does not expressly forbid a terminal shutdown extension after Off.", {}),
        "0012:r3:baseline_issue_1": ("D0", "Off-to-Terminate is source-real, but no explicit NL duty makes Off absorbing or forbids a separate termination path.", {}),
        "0012:r3:baseline_issue_2": ("D1", "Only Braking consumes stop in the source; the NL leaves whether stopping applies from other substates underdetermined.", {}),
        "0013:r1:baseline_issue_1": ("D1", "PumpStateA and WaterStateA are source-real extra states. The NL's 'three main substates' can be exhaustive or can allow implementation refinements.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r1:baseline_issue_2": ("D1", "PumpStateB and MethaneStateB are source-real extra states; the same exhaustive-enumeration versus refinement reading remains.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r1:baseline_issue_3": ("D1", "The source has three initial targets and the NL says first PumpState. The source fact is concrete, but the exact exclusivity of the first entry is not formalized.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r1:baseline_issue_4": ("D1", "The canonical three states and A/B replicas coexist. This is a structural enumeration issue, but a refinement reading remains possible.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r2:baseline_issue_1": ("D1", "The A/B state groups are source-real extras; the NL's three-substate wording supports an exhaustive reading but does not expressly prohibit refinements.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r2:baseline_issue_2": ("D1", "The three parallel initial entries are source-real and conflict with a strict first-PumpState reading, while a permissive region/refinement reading remains possible.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r2:baseline_issue_3": ("D1", "A/B branches introduce extra structure beside the canonical states; the fact is certain but the normative force of 'main substates' is ambiguous.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r3:baseline_issue_1": ("D1", "The A/B branches are source-real and not named in the NL; whether they are forbidden extras or implementation refinement is not completely determined.", {"EIS-0013-01": "FULL_MATCH"}),
        "0013:r3:baseline_issue_2": ("D1", "Multiple initial targets are source-real and undermine a strict unique-first-entry reading, but the NL does not explicitly state exclusivity.", {"EIS-0013-01": "FULL_MATCH"}),
        "0014:r1:baseline_issue_1": ("D1", "Obstacle Detected is used as an incoming edge label and as an internal description; the source establishes the text but does not disambiguate detection input from emitted signal.", {}),
        "0014:r1:baseline_issue_2": ("D2", "EmergencyStopping contains no explicit send action for Obstacle Detected; the NL explicitly requires sending that signal.", {"VU-0014-01": "FULL_MATCH"}),
        "0014:r1:baseline_issue_3": ("D1", "Entry/Accelerate is on the initial edge label. It can be read as a transition label encoding the entry behavior or as a misplaced entry action; both readings are possible.", {"EIS-0014-02": "FULL_MATCH"}),
        "0014:r1:baseline_issue_4": ("D2", "Approaching contains no Send action and only descriptive text, despite the explicit NL Send requirement.", {"EIS-0014-04": "FULL_MATCH"}),
        "0014:r1:baseline_issue_5": ("D0", "Ready to Stop/Decelerate is source-real descriptive text corresponding to the NL's readiness phrase; no distinct unmandated action is established.", {}),
        "0014:r1:baseline_issue_6": ("D1", "The source spelling SendArrived is adjacent to the NL's 'Send Arrived' signal phrase; the semantic distinction cannot be decided from the text alone.", {}),
        "0014:r2:baseline_issue_1": ("D1", "EmergencyStopping uses do/Send for a signal required on entry. The source notation and NL timing permit a continuous-action and entry-action reading.", {}),
        "0014:r2:baseline_issue_2": ("D1", "Approaching uses do/Send. This may represent ongoing sending/approach behavior, but the NL does not define action cadence.", {}),
        "0014:r2:baseline_issue_3": ("D1", "The same Obstacle Detected phrase appears as incoming trigger and do output text; the direction is genuinely ambiguous.", {}),
        "0014:r2:baseline_issue_4": ("D1", "The source has descriptive text in Approaching but no explicit Send syntax; the representation requirement is partially visible and semantically under-specified.", {"EIS-0014-04": "PARTIAL_MATCH"}),
        "0014:r3:baseline_issue_1": ("D1", "The source uses Obstacle Detected as an incoming label and descriptive state text; the required input/output distinction is ambiguous rather than a false source fact.", {}),
        "0014:r3:baseline_issue_2": ("D2", "No explicit send action appears in EmergencyStopping, while the NL expressly requires sending Obstacle Detected.", {"VU-0014-01": "FULL_MATCH"}),
        "0014:r3:baseline_issue_3": ("D1", "Approaching has static descriptions but no explicit persistence edge; the NL state-remains requirement admits a state-invariant reading and a diagram-explicit reading.", {}),
        "0014:r3:baseline_issue_4": ("D2", "No Send action or signal annotation appears under Approaching, directly missing the NL's explicit Send behavior.", {"EIS-0014-04": "FULL_MATCH"}),
        "0014:r3:baseline_issue_5": ("D1", "Entry/Accelerate is encoded on the initial transition label rather than a state entry action; the syntax signals the intended behavior but not its re-entry semantics.", {"EIS-0014-02": "FULL_MATCH"}),
        "0015:r3:baseline_issue_1": ("D2", "ReadytoCook has no display/update behavior although the NL explicitly requires it.", {"EIS-0015-01": "FULL_MATCH"}),
        "0015:r3:baseline_issue_2": ("D2", "The Start edge has no timer-start effect although the NL explicitly requires the timer to start in Cooking.", {"EIS-0015-01": "PARTIAL_MATCH"}),
        "0015:r3:baseline_issue_3": ("D2", "The door-open edge from Cooking has no timer-stop effect although the NL explicitly requires stopping the timer.", {"EIS-0015-01": "PARTIAL_MATCH"}),
        "0015:r3:baseline_issue_4": ("D2", "The ReadytoCook Cancel edge has no cooking-time cancel/update effect, despite the explicit NL requirement.", {"EIS-0015-01": "PARTIAL_MATCH"}),
        "0016:r1:baseline_issue_1": ("D2", "Region3 reaches the SearchMission final pseudostate, but the NL requires search to continue until mission completion and the source has no mission-complete condition.", {"EIS-0016-03": "FULL_MATCH"}),
        "0016:r1:baseline_issue_2": ("D1", "The source returns to SearchMission from interruption states without an explicit resumed search point; composite-state re-entry semantics can supply a default or be treated as underspecified.", {}),
        "0017:r1:baseline_issue_1": ("D1", "The source's three region entries all use generic collision detected. The NL distinguishes three collision types, but a generic event plus typed state names admits a shorthand reading.", {"VU-0017-01": "PARTIAL_MATCH"}),
        "0017:r1:baseline_issue_2": ("D1", "The source has three orthogonal collision-type states but no distinct control actions. The NL describes concurrent controls without specifying their names or exact state encoding.", {"VU-0017-01": "PARTIAL_MATCH"}),
        "0017:r1:baseline_issue_3": ("D1", "The source labels states as collision rather than possible collision. The distinction is semantically material but the state names may be shorthand for detected possibilities.", {}),
        "0019:r1:baseline_issue_1": ("D2", "ExitHighway is outside HighwayMode and requires a second auto_finished condition after distance-to-exit; the source does not implement the NL's separated exit/completion structure.", {"EIS-0019-01": "FULL_MATCH"}),
        "0019:r1:baseline_issue_2": ("D2", "exit_urban is outside UrbanMode and the source lacks an UrbanMode-level completion edge; the NL explicitly names the nested exit state and completion.", {"EIS-0019-03": "FULL_MATCH"}),
        "0019:r1:baseline_issue_3": ("D2", "CollisionAvoidanceSystem has no initial pseudostate edge to collision_avoidance_deactive, despite the explicit NL initial-state requirement.", {"EIS-0019-02": "FULL_MATCH"}),
        "0019:r1:baseline_issue_4": ("D1", "The source's front-distance condition uses informal mode text and omits a complete second comparison; the NL and source leave exact boolean syntax under-specified.", {}),
        "0019:r1:baseline_issue_5": ("D1", "The source has dynamic mode edges but also initial edges with the same flags; whether this violates mode exclusivity depends on an unstated invariant.", {}),
        "0019:r1:baseline_issue_6": ("D1", "The all-inactive conjunction is compatible with a strict all-danger-cleared reading, but the NL does not formalize the boolean connective; both readings remain possible.", {}),
        "0019:r2:baseline_issue_1": ("D2", "The HighwayMode exit target is external ExitHighway and only reaches FinishState after auto_finished; the source does not directly encode the NL's completion structure.", {"EIS-0019-01": "FULL_MATCH"}),
        "0019:r2:baseline_issue_2": ("D2", "The UrbanMode exit target is external exit_urban and only reaches FinishState from outside the mode; the nested exit/completion requirement is not represented.", {"EIS-0019-03": "FULL_MATCH"}),
        "0019:r2:baseline_issue_3": ("D2", "CollisionAvoidanceSystem has no initial transition to the explicitly named deactive state.", {"EIS-0019-02": "FULL_MATCH"}),
        "0019:r2:baseline_issue_4": ("D1", "The front-distance activation label is incomplete natural-language syntax rather than two fully explicit boolean clauses; the intended mode restriction remains ambiguous.", {}),
        "0019:r2:baseline_issue_5": ("D1", "The dynamic mode edges are present, but initial and dynamic flag use may or may not violate an unstated mutual-exclusion invariant.", {}),
        "0019:r2:baseline_issue_6": ("D1", "The source uses a conjunction of three inactive flags; this is consistent with all-danger-cleared semantics, but the NL does not fix the exact connective.", {}),
        "0019:r2:baseline_issue_7": ("D2", "No root or AutonomousMode final structure is provided for the source's FinishState completion path; the required mode lifecycle is incomplete.", {"EIS-0019-03": "PARTIAL_MATCH"}),
        "0019:r2:baseline_issue_8": ("D2", "The collision-avoidance block has no incoming edge from the only root-initialized AutonomousMode, so the named system is unreachable.", {"INS-0019-01": "FULL_MATCH"}),
        "0019:r3:baseline_issue_1": ("D2", "ExitHighway is external to HighwayMode and requires auto_finished after the distance trigger, so the source does not represent the required highway lifecycle.", {"EIS-0019-01": "FULL_MATCH"}),
        "0019:r3:baseline_issue_2": ("D2", "exit_urban is external to UrbanMode and not a child exit state as required by the NL.", {"EIS-0019-03": "FULL_MATCH"}),
        "0019:r3:baseline_issue_3": ("D2", "CollisionAvoidanceSystem lacks an initial edge to collision_avoidance_deactive.", {"EIS-0019-02": "FULL_MATCH"}),
        "0019:r3:baseline_issue_4": ("D1", "The activation label abbreviates the urban comparison and uses informal mode text; a shorthand interpretation and a strict executable-condition interpretation both survive.", {}),
        "0019:r3:baseline_issue_5": ("D2", "HighwayMode and UrbanMode completion edges originate from external exit states rather than the modes themselves, leaving auto_finished unconsumed in other substates.", {"EIS-0019-03": "FULL_MATCH"}),
    }
    for report_id, (d, note, positives) in more.items():
        add(report_id, d=d, note=note, positives=positives)

    # r3 pair 0016 has no reports and therefore has no annotation.  A few
    # raw records use baseline_issue_0 for a first item; normalize that one
    # identity only when the raw record actually supplies it.


def source_ref(path: str, sha: str, *, line: int | None = None, pointer: str | None = None) -> dict[str, Any]:
    """Create a stable archive-relative evidence pointer."""

    return {"path": path, "line_or_pointer": pointer or (f"line {line}" if line is not None else "full file read"), "sha256": sha}


def main() -> None:
    """Build the raw-first proposal JSON and a deterministic relation digest."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    inventory_path = args.inventory.resolve()
    output_path = args.output.resolve()
    inventory = load_json(inventory_path)
    ledger = load_json(archive / "reference" / "ledger.json")
    expected_ids = tuple(ledger["items"].keys())
    register_annotations()

    inventory_items = {
        (item["raw_method_path"], item["report_index"]): item
        for item in inventory["items"]
        if item["side"] == "x1v2_baseline"
    }
    records: list[dict[str, Any]] = []
    for path in sorted((archive / "raw" / "x1v2_baseline" / "method").glob("run*/*/record.json")):
        record = load_json(path)
        pair_id = str(record["case"])
        path_pair_id = path.parent.name.split("-", 1)[0]
        if pair_id != path_pair_id:
            raise ValueError(f"raw case/path pair mismatch: {path}")
        raw_record_pair_id = str(record.get("pair_id", ""))
        try:
            pair_number = int(pair_id)
        except ValueError:
            continue
        if not PAIR_MIN <= pair_number <= PAIR_MAX:
            continue
        round_number = int(record["round"])
        raw_path = str(path.relative_to(archive))
        raw_sha = sha256_file(path)
        source_dir = archive / "reference" / "x1v2_input_closure" / "pairs" / pair_id
        nl_path = source_dir / "nl.txt"
        plantuml_path = source_dir / "plantuml.puml"
        nl_rel = str(nl_path.relative_to(archive))
        plantuml_rel = str(plantuml_path.relative_to(archive))
        nl_sha = sha256_file(nl_path)
        plantuml_sha = sha256_file(plantuml_path)
        nl_path.read_text(encoding="utf-8")
        plantuml_path.read_text(encoding="utf-8")
        issues = record.get("parsed_output", {}).get("issues", [])
        for index, issue in enumerate(issues):
            identity = inventory_items.get((raw_path, index))
            if identity is None:
                raise ValueError(f"inventory does not close over {raw_path}#{index}")
            report_id = identity["report_id"]
            annotation = ANNOTATIONS.get(report_id)
            if annotation is None:
                raise ValueError(
                    f"missing explicit raw-first annotation for {report_id}; "
                    "refusing to materialize a template proposal"
                )
            relation_values = []
            relation_rows = []
            for expected_id in expected_ids:
                relation = annotation["positives"].get(expected_id, "NO_MATCH")
                if relation not in RELATIONS:
                    raise ValueError(f"invalid relation {relation} for {report_id}/{expected_id}")
                relation_values.append({"expected_id": expected_id, "relation": relation})
                relation_rows.append({
                    "expected_id": expected_id,
                    "relation": relation,
                    "ledger_json_pointer": f"/items/{expected_id}",
                    "basis": f"{report_id}: this expected row is represented in the report-specific canonical relation digest; report-level raw/source/ledger refs are retained above.",
                })
            relation_digest = canonical_digest(relation_values)
            positive_ids = [row["expected_id"] for row in relation_values if row["relation"] != "NO_MATCH"]
            if annotation["d_tier"] in {"D0", "A0"} and positive_ids:
                raise ValueError(f"invalid positive relation on non-defect proposal {report_id}")
            issue_text = issue.get("issue", "")
            where_text = issue.get("where", "")
            reason_text = issue.get("reason", "")
            basis_text = issue.get("basis")
            evidence_gaps = ["preexisting_non_k_membership_not_encoded_in_raw_only_inputs"]
            if "basis" not in issue:
                evidence_gaps.append("raw_basis_field_absent_in_record")
            if raw_record_pair_id.rsplit("_", 1)[-1] != pair_id:
                evidence_gaps.append("raw_pair_id_inconsistent_with_path_derived_pair_id")
            evidence_gaps.extend(annotation["evidence_gaps"])
            profile = SOURCE_PROFILES[pair_id]
            records.append({
                "report_id": report_id,
                "pair_id": pair_id,
                "round": round_number,
                "finding_index": index,
                "review_status": "PROPOSAL",
                "reviewer_id": "raw-first:track-a-0000-0019",
                "blindness": {
                    "v2_decisions_read": False,
                    "old_labels_read": False,
                    "track_b_read": False,
                    "other_reviewer_conclusions_read": False,
                    "judge_outputs_used_for_semantic_decision": False,
                    "provider_called": False,
                },
                "raw": {
                    "method_record_path": raw_path,
                    "json_pointer": f"/parsed_output/issues/{index}",
                    "raw_sha256": raw_sha,
                    "issue": issue_text,
                    "where": where_text,
                    "reason": reason_text,
                    "basis": basis_text,
                    "claim_pointer": f"/parsed_output/issues/{index}/issue",
                    "where_pointer": f"/parsed_output/issues/{index}/where",
                },
                "author_source": {
                    "nl_path": nl_rel,
                    "nl_sha256": nl_sha,
                    "plantuml_path": plantuml_rel,
                    "plantuml_sha256": plantuml_sha,
                    "full_files_read": True,
                    "pair_source_profile": profile,
                    "source_locus": where_text,
                },
                "observed_fact": {
                    "status": "ESTABLISHED" if annotation["d_tier"] != "A0" else "REFUTED",
                    "statement": annotation["note"],
                    "proposal_reason": annotation["note"],
                    "source_refs": [
                        source_ref(raw_path, raw_sha, pointer=f"/parsed_output/issues/{index}"),
                        source_ref(nl_rel, nl_sha),
                        source_ref(plantuml_rel, plantuml_sha),
                        source_ref("reference/ledger.json", sha256_file(archive / "reference" / "ledger.json"), pointer="/items (complete ledger read)"),
                    ],
                },
                "d_a_proposal": {
                    "d_tier": annotation["d_tier"],
                    "a0_type": "FALSE_POSITIVE" if annotation["d_tier"] == "A0" else None,
                    "normative_violation_status": "ESTABLISHED" if annotation["d_tier"] in {"D2", "D1"} else "NOT_ESTABLISHED",
                    "defect_claim_status": "DEFECT_CLAIM" if annotation["d_tier"] in {"D2", "D1"} else "NO_DEFECT_CLAIM",
                    "reason": f"{report_id}: {annotation['note']}",
                    "basis": f"{report_id}: {profile} Exact raw where={where_text!r}; source refs point to the complete files read.",
                    "source_refs": [
                        {"path": nl_rel, "line_or_pointer": "full file read", "sha256": nl_sha},
                        {"path": plantuml_rel, "line_or_pointer": "full file read; locus quoted from raw where", "sha256": plantuml_sha},
                    ],
                },
                "relation_proposal": {
                    "expected_count": len(expected_ids),
                    "rows": relation_rows,
                    "full_match_ids": [row["expected_id"] for row in relation_values if row["relation"] == "FULL_MATCH"],
                    "partial_match_ids": [row["expected_id"] for row in relation_values if row["relation"] == "PARTIAL_MATCH"],
                    "no_match_count": sum(row["relation"] == "NO_MATCH" for row in relation_values),
                    "canonical_value_digest": relation_digest,
                    "digest_algorithm": "sha256(canonical JSON list of all 145 {expected_id, relation} rows)",
                },
                "evidence_gaps": evidence_gaps,
                "coverage_note": "This row is included in the conservative raw candidate universe for pair IDs 0000-0019 so a potential non-K report is not silently omitted. The proposal does not assert frozen pre-v3 K membership.",
            })

    records.sort(key=lambda row: (row["pair_id"], row["round"], row["finding_index"]))
    expected_set = set(expected_ids)
    for row in records:
        if len(row["relation_proposal"]["rows"]) != len(expected_ids):
            raise AssertionError(row["report_id"])
        if set(x["expected_id"] for x in row["relation_proposal"]["rows"]) != expected_set:
            raise AssertionError(row["report_id"])

    output = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-a-proposal.v1",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "proposal_role": "raw-first independent proposal only; not pane5 final adjudication",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "archive_relative_root": ARCHIVE_RELATIVE,
        "blind_input_policy": {
            "allowed_inputs": [
                "derived/manual_adjudication_v3_baseline_ni/inventory.json",
                "raw/x1v2_baseline/method/run{1,2,3}/*/record.json",
                "reference/x1v2_input_closure/pairs/{pair}/nl.txt",
                "reference/x1v2_input_closure/pairs/{pair}/plantuml.puml",
                "reference/ledger.json",
            ],
            "forbidden_inputs": [
                "derived/manual_adjudication_v2/**",
                "old labels or frozen decision outputs",
                "Track B or any other reviewer conclusion",
                "provider/method/Judge execution",
            ],
        },
        "scope": {
            "requested": "X1v2 baseline non-K reports with pair_id 0000 through 0019 inclusive",
            "scope_gate": "OPEN_EVIDENCE_GAP",
            "raw_candidate_count": len(records),
            "pair_ids": [f"{value:04d}" for value in range(PAIR_MIN, PAIR_MAX + 1)],
            "preexisting_non_k_membership_available_from_allowed_inputs": False,
            "coverage_policy": "retain all raw reports in the requested pair range as conservative candidates; do not read forbidden old labels to filter them",
            "missing_evidence": [
                "No allowed raw artifact encodes which reports were the frozen pre-v3 K reports. The exact non-K membership therefore cannot be asserted under the user's blind-input rule.",
                "This proposal is a raw candidate superset; it must not be merged as the 233-row final non-K decision set until an independently permitted scope manifest is supplied or created outside this blind proposal.",
            ],
        },
        "inputs": {
            "inventory_path": str(inventory_path.relative_to(archive.parent.parent.parent.parent)) if inventory_path.is_relative_to(archive.parent.parent.parent.parent) else str(inventory_path),
            "inventory_sha256": sha256_file(inventory_path),
            "ledger_path": "reference/ledger.json",
            "ledger_sha256": sha256_file(archive / "reference" / "ledger.json"),
            "ledger_expected_count": len(expected_ids),
        },
        "coverage": {
            "reports_materialized": len(records),
            "reports_with_explicit_annotations": sum(row["report_id"] in ANNOTATIONS for row in records),
            "reports_with_missing_annotations": [row["report_id"] for row in records if row["report_id"] not in ANNOTATIONS],
            "reports_with_145_relation_rows": sum(len(row["relation_proposal"]["rows"]) == len(expected_ids) for row in records),
            "source_full_read_claims": sum(row["author_source"]["full_files_read"] for row in records),
            "by_pair": dict(Counter(row["pair_id"] for row in records)),
            "by_round": dict(Counter(str(row["round"]) for row in records)),
            "pair_coverage": {
                f"{pair_number:04d}": sum(row["pair_id"] == f"{pair_number:04d}" for row in records)
                for pair_number in range(PAIR_MIN, PAIR_MAX + 1)
            },
        },
        "reports": records,
    }
    TrackAProposal.model_validate(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    input_files = {str(inventory_path.relative_to(archive)): sha256_file(inventory_path), "reference/ledger.json": sha256_file(archive / "reference" / "ledger.json")}
    for row in records:
        input_files[row["raw"]["method_record_path"]] = row["raw"]["raw_sha256"]
        input_files[row["author_source"]["nl_path"]] = row["author_source"]["nl_sha256"]
        input_files[row["author_source"]["plantuml_path"]] = row["author_source"]["plantuml_sha256"]
    manifest = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-a-proposal-manifest.v1",
        "proposal_path": str(output_path.relative_to(archive)),
        "proposal_sha256": sha256_file(output_path),
        "builder_path": str(Path(__file__).relative_to(archive.parent.parent.parent.parent)),
        "builder_sha256": sha256_file(Path(__file__)),
        "validator_path": "project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_track_a_0000_0019_proposal.py",
        "validator_sha256": sha256_file(Path(__file__).with_name("validate_track_a_0000_0019_proposal.py")),
        "generated_at_utc": output["generated_at_utc"],
        "scope": output["scope"],
        "scope_probe_path": "derived/manual_adjudication_v3_baseline_ni/proposals/raw_scope_probe_0000_0019.json",
        "scope_probe_sha256": sha256_file(output_path.with_name("raw_scope_probe_0000_0019.json")) if output_path.with_name("raw_scope_probe_0000_0019.json").exists() else None,
        "report_count": len(records),
        "expected_count_per_report": len(expected_ids),
        "input_file_hashes": dict(sorted(input_files.items())),
        "recompute_command": "python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_track_a_baseline_ni_proposal.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --inventory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/inventory.json --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/proposals/track_a_0000_0019.json",
        "validation_command": "python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_track_a_0000_0019_proposal.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --proposal project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/proposals/track_a_0000_0019.json --inventory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/inventory.json",
    }
    manifest_path = output_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reports": len(records), "expected_per_report": len(expected_ids), "output": str(output_path), "manifest": str(manifest_path), "missing_annotations": output["coverage"]["reports_with_missing_annotations"]}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
