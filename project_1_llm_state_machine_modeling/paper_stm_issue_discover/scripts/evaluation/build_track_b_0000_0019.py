#!/usr/bin/env python3
"""Build the blind raw-first Track B proposal for baseline pairs 0000--0019.

The assessment table below is a human-entered evidence record.  The program
only joins it to exact raw findings, source files, and the 145 ledger rows;
it does not infer a D/A tier, relation, or K/N/I label from text.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ARCHIVE = Path(__file__).parents[2] / "final_results/v60_current_vs_x1v2_baseline"
RAW_ROOT = ARCHIVE / "raw/x1v2_baseline/method"
SOURCE_ROOT = ARCHIVE / "reference/x1v2_input_closure/pairs"
LEDGER_PATH = ARCHIVE / "reference/ledger.json"
OUT = ARCHIVE / "derived/manual_adjudication_v3_baseline_ni/proposals/track_b_0000_0019.json"
REVIEWER = "subagent:track-b-0000-0019"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path: Path, *, pointer: str | None = None, line: int | None = None) -> dict:
    return {
        "repository_path": path.relative_to(ARCHIVE).as_posix(),
        "json_pointer": pointer,
        "line": line,
        "sha256": sha256(path),
    }


# Each entry is a raw-first semantic adjudication written after reading the
# report, its complete author source, and the pair's ledger evidence.
ASSESSMENTS: dict[tuple[str, int, int], dict] = {
    ("0000", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:8-9"],
        "reason": "0000:r1:baseline_issue_1: AutoNavigating to AutoFinal exists, but the author NL does not prescribe an AutoFinal entry condition. The report identifies an unspecified design choice, not a demonstrated violation.",
        "basis": "0000:r1:baseline_issue_1: NL line 1 states only that autonomous mode has substates; PlantUML lines 8-9 contain the Condition Met transition. A named condition is not by itself a defect when no source obligation requires a particular condition.",
        "same_pair": "No ledger item establishes a defect for the unspecified AutoFinal entry condition; the three 0000 expected claims concern Power Off placement, the handover label, and a labeled root initial edge.",
    },
    ("0000", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:8-9"],
        "reason": "0000:r2:baseline_issue_2: The model has an AutoNavigating to AutoFinal transition with a generic condition, but the source requirement does not require a more specific AutoFinal completion condition. The claimed defect is therefore not established.",
        "basis": "0000:r2:baseline_issue_2: NL line 1 requires autonomous substates and separately lists the handover and Power Off behavior; PlantUML lines 8-9 show the disputed transition. No author-source obligation is violated by choosing the label Condition Met.",
        "same_pair": "No ledger item matches a generic AutoFinal entry-condition complaint.",
    },
    ("0000", 3, 2): {
        "d": "D1", "loci": ["plantuml.puml:7-10", "plantuml.puml:13"],
        "reason": "0000:r3:baseline_issue_3: AutoFinal is a named substate and is used in the handover label, but the NL does not state whether AutoFinal is a terminal state or merely a mode condition. Treating its name as an obligation is a live alternative reading, so the issue is a D1 novel interpretation concern rather than D2.",
        "basis": "0000:r3:baseline_issue_3: NL line 1 says in (auto final) and says Power Off reaches a final state, without declaring AutoFinal itself final. PlantUML lines 7-10 define AutoFinal as an ordinary substate with no final pseudostate; line 13 uses it as text in an outer transition.",
        "same_pair": "The ledger has no expected that asserts AutoFinal must itself be declared final; all 0000 expected rows concern other concrete defects.",
    },
    ("0000", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:14"],
        "reason": "0000:r3:baseline_issue_1: The report's Power Off claim is a known ledger issue and is not part of this non-K proposal; this entry is retained only in the raw census exclusion set.",
        "basis": "This entry is excluded from the proposal because its concrete Power Off source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded",
        "exclude": True,
    },
    ("0000", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:13"],
        "reason": "0000:r1:baseline_issue_2: The combined handover label is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete handover source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded",
        "exclude": True,
    },
    ("0000", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:14"],
        "reason": "0000:r2:baseline_issue_1: The Power Off source locus is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power Off source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded",
        "exclude": True,
    },
    ("0000", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:13"],
        "reason": "0000:r3:baseline_issue_2: The combined handover label is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete handover source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded",
        "exclude": True,
    },
    ("0001", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:12"],
        "reason": "0001:r1:baseline_issue_2: BrakingState to InitialState on Signal Feedback Sent is explicitly required by the NL. The reported transition is present and therefore does not establish a defect.",
        "basis": "0001:r1:baseline_issue_2: NL lines 1-3 require return to the initial state after signal feedback; PlantUML line 12 contains exactly BrakingState --> InitialState : Signal Feedback Sent.",
        "same_pair": "The report concerns the explicitly present required feedback edge, not either ledger defect: the extra dead ClampingLoseState or the ClampingState dead end.",
    },
    ("0001", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0001:r1:baseline_issue_1: The extra ClampingLoseState is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0001", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0001:r2:baseline_issue_1: The extra ClampingLoseState is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0001", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0001:r3:baseline_issue_1: The extra ClampingLoseState is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0003", 1, 0): {
        "d": "D1", "loci": ["plantuml.puml:4-8"],
        "reason": "0003:r1:baseline_issue_1: AcceleratingOrCruising is one declared state, while the NL phrase can be read either as one combined named state or as two conceptual phases. The structural fact is clear but the normative reading is genuinely ambiguous, so D1 and novel.",
        "basis": "0003:r1:baseline_issue_1: NL line 1 names Idle, Accelerating or Cruising, and Braking; PlantUML lines 4-8 declare one AcceleratingOrCruising state and its transitions. The source does not settle whether separate states are mandatory.",
        "same_pair": "The ledger contains no 0003 expected item; all 0003 expected relations are NO_MATCH.",
    },
    ("0003", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:6-8"],
        "reason": "0003:r1:baseline_issue_2: The report demands Stop Signal coverage from additional states, but the NL only requires action-dependent transitions and does not require a Stop Signal edge from every state. The existing Braking to Idle stop path is a reasonable design interpretation.",
        "basis": "0003:r1:baseline_issue_2: NL lines 1 and 3 describe transitions based on actions; PlantUML lines 6-8 provide the accelerate, brake, and stop chain. No text mandates direct stopping from AcceleratingOrCruising.",
        "same_pair": "The ledger contains no 0003 expected item; all 0003 expected relations are NO_MATCH.",
    },
    ("0003", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:6-8"],
        "reason": "0003:r2:baseline_issue_1: The report treats the absence of a direct AcceleratingOrCruising to Idle stop edge as a defect, but the author source supplies the sequential brake then stop path and does not require a direct edge.",
        "basis": "0003:r2:baseline_issue_1: NL line 3 says transitions depend on actions such as accelerating, braking, or stopping; PlantUML lines 6-8 route AcceleratingOrCruising to Braking on brake and Braking to Idle on stop.",
        "same_pair": "The ledger contains no 0003 expected item; all 0003 expected relations are NO_MATCH.",
    },
    ("0003", 3, 0): {
        "d": "A0", "loci": ["plantuml.puml:4-5", "plantuml.puml:11"],
        "reason": "0003:r3:baseline_issue_1: The report says entry into Idle is not guaranteed after power-on, but the author source has Operate's initial transition to Idle. The承重事实 is refuted by the source.",
        "basis": "0003:r3:baseline_issue_1: PlantUML lines 4-5 define Operate with [*] --> Idle, and line 11 enters Operate on start. The report's claimed absence is not present in the complete PlantUML.",
        "same_pair": "The ledger contains no 0003 expected item; A0 requires NO_MATCH for every expected.",
    },
    ("0003", 3, 1): {
        "d": "D1", "loci": ["plantuml.puml:4-8"],
        "reason": "0003:r3:baseline_issue_2: The declared combined AcceleratingOrCruising state can be read as a valid rendering of the source phrase or as a loss of two conceptual phases. That alternative reading survives, so the report is D1 novel.",
        "basis": "0003:r3:baseline_issue_2: NL line 1 uses the phrase Accelerating or Cruising without separate transition obligations; PlantUML lines 4-8 use one named state. The source supports both readings.",
        "same_pair": "The ledger contains no 0003 expected item; all 0003 expected relations are NO_MATCH.",
    },
    ("0003", 3, 2): {
        "d": "D0", "loci": ["plantuml.puml:6-8"],
        "reason": "0003:r3:baseline_issue_3: The report generalizes the stop requirement beyond what the NL states. The existing Braking to Idle stop transition is a source-consistent design and no additional obligation is established.",
        "basis": "0003:r3:baseline_issue_3: NL line 3 gives examples of action-dependent transitions; PlantUML lines 6-8 contain the complete Idle, AcceleratingOrCruising, Braking chain with Stop Signal.",
        "same_pair": "The ledger contains no 0003 expected item; all 0003 expected relations are NO_MATCH.",
    },
    ("0004", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:24-26"],
        "reason": "0004:r1:baseline_issue_2: Approaching has do/Send, which is a valid state action and satisfies the NL requirement to send Send while approaching. The report does not establish that the action must be entry-only.",
        "basis": "0004:r1:baseline_issue_2: NL lines 9-10 require sending Send and remaining in Approaching; PlantUML lines 24-26 declare Approaching with do/Send. State residence is implicit without an outgoing transition.",
        "same_pair": "The pair ledger covers the malformed DoorsClosing nesting and two dead-end states; it does not require Send to be an entry action.",
    },
    ("0004", 1, 2): {
        "d": "D0", "loci": ["plantuml.puml:24-26"],
        "reason": "0004:r1:baseline_issue_3: A state remains active until an outgoing transition fires; an explicit self-loop is not required to express continuous approach. The absence of a self-loop is therefore not a defect.",
        "basis": "0004:r1:baseline_issue_3: NL lines 9-10 explicitly say Approaching continues and remains; PlantUML lines 24-26 define the state and its do action, with no competing exit edge from Approaching.",
        "same_pair": "No 0004 ledger item asserts that a persistence statement must be encoded as a self-loop; all expected relations are NO_MATCH.",
    },
    ("0004", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:32-35"],
        "reason": "0004:r2:baseline_issue_1: EmergencyStopping's do/Send action is a valid action phase for the source requirement, which says the state includes the action but does not require entry timing. No violation is established.",
        "basis": "0004:r2:baseline_issue_1: NL line 3 requires Emergency Stop and sending Obstacle Detected in EmergencyStopping; PlantUML lines 32-35 provide entry/Emergency Stop and do/Send Obstacle Detected.",
        "same_pair": "The ledger's EmergencyStopping expected is the absence of an exit path, not a requirement that its send action use entry phase.",
    },
    ("0004", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:24-26"],
        "reason": "0004:r2:baseline_issue_2: The do/Send action is compatible with sending while the system is in Approaching, and the source does not require a particular action phase. The report is not a demonstrated defect.",
        "basis": "0004:r2:baseline_issue_2: NL lines 9-10 require Send and continued approach; PlantUML lines 24-26 provide do/Send and no exit from Approaching.",
        "same_pair": "No 0004 ledger item requires Send to be encoded with a particular entry/do phase.",
    },
    ("0004", 2, 2): {
        "d": "D1", "loci": ["plantuml.puml:29-34"],
        "reason": "0004:r2:baseline_issue_3: The same phrase Obstacle Detected is used as the transition trigger and as the EmergencyStopping output text. It can be read as an intentionally reused signal name or as a failure to distinguish input and output, so the semantic concern is D1 novel.",
        "basis": "0004:r2:baseline_issue_3: NL line 2 uses obstacle detection as the input condition and line 3 separately requires sending Obstacle Detected; PlantUML lines 29-34 show the input transition and state action text. The source is ambiguous about signal namespaces.",
        "same_pair": "The expected EmergencyStopping ledger row concerns a missing exit path; it does not subsume this input/output naming ambiguity.",
    },
    ("0004", 3, 0): {
        "d": "D1", "loci": ["plantuml.puml:29-34"],
        "reason": "0004:r3:baseline_issue_1: Reusing Obstacle Detected for the input trigger and output annotation may be a signal-role ambiguity, but the source does not define separate signal namespaces. Both a correct reuse and an under-specified output are competent readings.",
        "basis": "0004:r3:baseline_issue_1: NL lines 2-3 distinguish detection and sending only by sentence role; PlantUML lines 29-34 use the same text at the transition and do action. This supports D1, not an unambiguous D2.",
        "same_pair": "The expected EmergencyStopping row is the missing exit behavior and does not match this role-separation concern.",
    },
    ("0004", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:32-35"],
        "reason": "0004:r3:baseline_issue_2: EmergencyStopping has an explicit entry/Emergency Stop action and a do/Send Obstacle Detected action. The report's claim that the required action is absent is refuted by the complete state body.",
        "basis": "0004:r3:baseline_issue_2: NL line 3 requires both actions; PlantUML lines 32-35 contain EmergencyStopping: entry/Emergency Stop and EmergencyStopping: do/Send Obstacle Detected.",
        "same_pair": "The report does not concern the ledgered missing outgoing transition, and its asserted action absence is false.",
    },
    ("0004", 3, 2): {
        "d": "D0", "loci": ["plantuml.puml:24-26"],
        "reason": "0004:r3:baseline_issue_3: Approaching is a persistent state with do/Send and no outgoing transition; the report's demand for an explicit hold loop is not required by the source semantics.",
        "basis": "0004:r3:baseline_issue_3: NL lines 9-10 require continuous approach and remaining in Approaching; PlantUML lines 24-26 provide the state and its do action. Absence of a self-loop does not refute persistence.",
        "same_pair": "No 0004 ledger row requires an explicit self-loop for Approaching.",
    },
    ("0004", 3, 3): {
        "d": "D0", "loci": ["plantuml.puml:4-6"],
        "reason": "0004:r3:baseline_issue_4: The nested DoorsClosing construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete DoorsClosing source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0004", 3, 4): {
        "d": "D0", "loci": ["plantuml.puml:2-5"],
        "reason": "0004:r3:baseline_issue_5: The nested DoorsClosing construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete DoorsClosing source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0004", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:4-6"],
        "reason": "0004:r1:baseline_issue_1: The nested DoorsClosing construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete DoorsClosing source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0004", 1, 3): {
        "d": "D0", "loci": ["plantuml.puml:30-35"],
        "reason": "0004:r1:baseline_issue_4: The EmergencyStopping dead-end construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete EmergencyStopping source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0006", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:4-5, 7-8"],
        "reason": "0006:r1:baseline_issue_2: Searching is a state that persists while active, and the NL gives no explicit self-loop or separate completion event requirement. The report mistakes implicit state residence for a missing transition.",
        "basis": "0006:r1:baseline_issue_2: NL line 1 says search is continuous before mission completion; PlantUML lines 4-5 define Searching, while lines 7-8 provide its two event exits. No outgoing edge is needed merely to remain active.",
        "same_pair": "The sole 0006 ledger expected concerns UAV-count decrease after Attack Complete, not a Searching self-loop.",
    },
    ("0006", 1, 2): {
        "d": "D2", "loci": ["plantuml.puml:2-26"],
        "reason": "0006:r1:baseline_issue_3: The NL explicitly requires operation within three different state areas, while the author source has Searching, FormationAdjustment, and Attack as separate elements without three search regions. The fact and obligation are clear, so this is a valid novel defect.",
        "basis": "0006:r1:baseline_issue_3: NL line 2 requires three different state areas during continuous search; PlantUML lines 2-26 show one Searching state, one FormationAdjustment composite, and one Attack composite, with no three-region search structure.",
        "same_pair": "The sole 0006 ledger expected is the attack-count effect; a missing three-region search structure is NO_MATCH.",
    },
    ("0006", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:7-14, 22-23"],
        "reason": "0006:r2:baseline_issue_2: The source does provide an Intercepted element followed by FormationAdjustment. An intermediate named state is not prohibited, so the claim that the required interception behavior is missing is not established.",
        "basis": "0006:r2:baseline_issue_2: NL line 3 requires transition to formation adjustment after interception; PlantUML lines 7 and 22-23 route Searching to Intercepted and Intercepted to FormationAdjustment, whose body begins at lines 10-14.",
        "same_pair": "The sole 0006 expected item concerns attack-count decrease; this interception representation has NO_MATCH.",
    },
    ("0006", 3, 1): {
        "d": "D2", "loci": ["plantuml.puml:2-26"],
        "reason": "0006:r3:baseline_issue_2: The NL explicitly requires three different state areas during the continuous search period, but the complete PlantUML does not provide that structure. This is a valid novel defect.",
        "basis": "0006:r3:baseline_issue_2: NL line 2 states the three-area obligation; PlantUML lines 2-26 contain the full state machine and show no three-region search arrangement.",
        "same_pair": "The sole 0006 expected item concerns attack-count decrease; the three-area structure is NO_MATCH.",
    },
    ("0006", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:16-20"],
        "reason": "0006:r1:baseline_issue_1: The attack-count omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Attack Complete source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0006", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:16-20"],
        "reason": "0006:r2:baseline_issue_1: The attack-count omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Attack Complete source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0006", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:16-20"],
        "reason": "0006:r3:baseline_issue_1: The attack-count omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Attack Complete source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0007", 1, 1): {
        "d": "A0", "loci": ["plantuml.puml:11-23, 25-29"],
        "reason": "0007:r1:baseline_issue_2: The report says the CollisionAvoidance region count is inconsistent, but the complete source has three regions separated by two separators and separately declares OperationalControls. The claimed structural absence is refuted.",
        "basis": "0007:r1:baseline_issue_2: NL line 1 requires three regions; PlantUML lines 11-23 contain three CollisionAvoidance regions, and lines 25-29 contain a separate OperationalControls state. The source does not support the report's asserted count error.",
        "same_pair": "The ledger rows concern the dead InitialState, labeled region initial edges, and extra OperationalControls; this asserted region-count error is NO_MATCH.",
    },
    ("0007", 1, 2): {
        "d": "D2", "loci": ["plantuml.puml:4-9, 31"],
        "reason": "0007:r1:baseline_issue_3: The NL requires the collision-avoidance submachine to become active when one of three possible collision types is detected, but the source uses an unconditional Collision Mode Active edge from CollisionDetection. The violation is explicit and novel.",
        "basis": "0007:r1:baseline_issue_3: NL line 2 supplies the three detection-trigger alternatives; PlantUML lines 4-9 define those detections inside CollisionDetection, while line 31 enters CollisionAvoidance with the unrelated unconditional label Collision Mode Active.",
        "same_pair": "The ledger has no expected item for the missing detection guard on the CollisionDetection-to-CollisionAvoidance edge.",
    },
    ("0007", 2, 0): {
        "d": "D2", "loci": ["plantuml.puml:4-9, 31"],
        "reason": "0007:r2:baseline_issue_1: CollisionAvoidance is entered by an unconditional edge rather than by the three possible-collision detections required by the NL. The source fact and obligation are both clear.",
        "basis": "0007:r2:baseline_issue_1: NL line 2 lists frontend, rear-end, and pedestrian possible-collision triggers; PlantUML lines 4-9 define those internal detections but line 31 uses only Collision Mode Active without the required trigger relation.",
        "same_pair": "No 0007 ledger item covers this missing external activation condition.",
    },
    ("0007", 2, 2): {
        "d": "D2", "loci": ["plantuml.puml:11-23"],
        "reason": "0007:r2:baseline_issue_3: The source has three fixed control regions with labeled initial events, but it does not connect the three possible-collision detections to independently activatable controls as required. The report identifies a valid novel completeness defect.",
        "basis": "0007:r2:baseline_issue_3: NL lines 2-3 require activation of the active submachine and concurrent collision-avoidance controls; PlantUML lines 11-23 show three regions but no detection-specific activation link into them.",
        "same_pair": "The ledger's labeled-initial-edge item concerns UML initial pseudostate labels, not the missing detection-to-control activation mapping.",
    },
    ("0007", 3, 0): {
        "d": "D2", "loci": ["plantuml.puml:4-9, 31"],
        "reason": "0007:r3:baseline_issue_1: The three collision-detection states are internal to CollisionDetection, but the external activation edge still has only Collision Mode Active and does not express the required detection alternatives. This is a valid novel defect.",
        "basis": "0007:r3:baseline_issue_1: NL line 2 names three possible-collision conditions; PlantUML lines 4-9 show the conditions only inside CollisionDetection and line 31 shows the unguarded external edge.",
        "same_pair": "No 0007 ledger row matches the missing external detection trigger.",
    },
    ("0007", 3, 1): {
        "d": "D2", "loci": ["plantuml.puml:4-9, 31"],
        "reason": "0007:r3:baseline_issue_2: The required three detection outcomes are not represented as separate activation conditions on the edge that enters CollisionAvoidance. The report's fact is present and its normative requirement is explicit.",
        "basis": "0007:r3:baseline_issue_2: NL line 2 requires activation on any of three possible collisions; PlantUML lines 4-9 enumerate the internal states, while line 31 does not consume any of those outcomes.",
        "same_pair": "No 0007 ledger expected covers this incomplete trigger binding.",
    },
    ("0007", 3, 2): {
        "d": "D0", "loci": ["plantuml.puml:11-23"],
        "reason": "0007:r3:baseline_issue_3: The three `--`-separated regions are precisely the PlantUML representation of orthogonal regions, and the source has no competing evidence that concurrency is absent. The report's uncertainty is not a demonstrated violation.",
        "basis": "0007:r3:baseline_issue_3: NL line 3 requires concurrent activation; PlantUML lines 11-23 define three separated regions inside CollisionAvoidance. The source structure supports concurrent regions without an additional prose annotation.",
        "same_pair": "The ledger's region-related expected is the invalid labeled initial-edge construction, not a requirement for extra concurrency text.",
    },
    ("0007", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:2, 31-32"],
        "reason": "0007:r1:baseline_issue_1: The InitialState dead-end is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete InitialState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0007", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:25-29"],
        "reason": "0007:r2:baseline_issue_2: OperationalControls being a separate top-level state is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete OperationalControls source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0009", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:12-17"],
        "reason": "0009:r1:baseline_issue_1: The source supplies a cruise path for dist_to_front>=25 and a lane-change path for dist_to_front<25 with an extra lane. The NL does not require the report's proposed alternative partition, so no defect is established.",
        "basis": "0009:r1:baseline_issue_1: NL lines 3-5 describe distance and extra-lane-dependent HighwayMode behavior; PlantUML lines 12-17 provide both enter_hwy outcomes. The complement case is a defensible design choice.",
        "same_pair": "The ledger highway expected rows concern the FinishState/exit semantics, not this reasonable complement guard.",
    },
    ("0009", 1, 3): {
        "d": "D0", "loci": ["plantuml.puml:16-17"],
        "reason": "0009:r1:baseline_issue_4: The `dist_to_front>=25` cruise guard is a reasonable complement to the explicitly required `<25` lane-change case, and the source does not require an additional branch for extra_lane=false. The report identifies unspecified behavior, not a violation.",
        "basis": "0009:r1:baseline_issue_4: NL lines 3-5 specify the `<25` plus extra-lane lane-change behavior but do not forbid a complementary cruise guard; PlantUML lines 16-17 show the two explicit branches.",
        "same_pair": "No 0009 ledger expected asserts that the complement guard must be absent or that extra_lane=false needs another edge.",
    },
    ("0009", 1, 4): {
        "d": "A0", "loci": ["plantuml.puml:51-58"],
        "reason": "0009:r1:baseline_issue_5: The report alleges that the collision-avoidance distance conditions are malformed, but the complete source contains the highway `<15` and urban `<10` alternatives together with the pedestrian and rear-distance alternatives required by the NL.",
        "basis": "0009:r1:baseline_issue_5: NL line 12 gives the same four semantic alternatives; PlantUML lines 51-58 encode them in the activation guard. The claimed absence or wrong-mode binding is refuted by the source.",
        "same_pair": "The ledger collision-avoidance expected concerns unreachable CollisionAvoidanceSystem, not the present activation guard.",
    },
    ("0009", 3, 3): {
        "d": "D0", "loci": ["plantuml.puml:12-17"],
        "reason": "0009:r3:baseline_issue_4: The explicit `<25` lane-change branch is complemented by the source's `>=25` cruise branch. The NL leaves the complementary cruise partition open, so the report does not establish a defect.",
        "basis": "0009:r3:baseline_issue_4: NL lines 3-5 require the `<25` and extra-lane condition for lane change; PlantUML lines 12-17 show a coherent partition with cruise for the complement.",
        "same_pair": "No 0009 expected item covers the choice of a complementary cruise guard.",
    },
    ("0009", 3, 4): {
        "d": "A0", "loci": ["plantuml.puml:51-58"],
        "reason": "0009:r3:baseline_issue_5: The report's alleged mode-condition defect is not present: the source explicitly includes the highway and urban distance alternatives and the other required danger alternatives.",
        "basis": "0009:r3:baseline_issue_5: NL line 12 and PlantUML lines 51-58 agree on the semantic guard alternatives. The report's asserted missing or invalid condition is false against the complete author source.",
        "same_pair": "The ledger collision-avoidance expected is the unreachable system block, not this guard expression.",
    },
    ("0010", 2, 1): {
        "d": "A0", "loci": ["plantuml.puml:5, 9, 12, 18"],
        "reason": "0010:r2:baseline_issue_2: The report says the front-distance transition direction is wrong, but the author NL explicitly requires front_distance>10 to move to autonomous mode and the source has that HumanDriving to Autonomous edge. The asserted source fact is false.",
        "basis": "0010:r2:baseline_issue_2: NL line 1 states front_distance > 10 leads to autonomous; PlantUML lines 5, 9, 12, and 18 show the corresponding edges. The additional <=10 idle edge does not refute the required direction.",
        "same_pair": "No ledger item asserts a front-distance direction defect; the pair expected rows concern power-on, submachine structure, handover, and Power Off.",
    },
    ("0010", 3, 2): {
        "d": "A0", "loci": ["plantuml.puml:5, 9, 12, 18"],
        "reason": "0010:r3:baseline_issue_3: The report claims the front-distance transition is absent or misplaced, but the complete source contains HumanDriving to Autonomous on Front Distance > 10. The承重事实 is refuted.",
        "basis": "0010:r3:baseline_issue_3: NL line 1 requires front_distance > 10 to reach autonomous; PlantUML line 18 provides that transition, with lines 9 and 12 defining additional autonomous states.",
        "same_pair": "No 0010 expected item matches a complaint that the required front-distance edge is absent; the source contains it.",
    },
    ("0010", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:2, 5"],
        "reason": "0010:r1:baseline_issue_1: The Power On placement is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power On source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:5-13"],
        "reason": "0010:r1:baseline_issue_2: The autonomous submachine structure is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete autonomous-mode source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 2): {
        "d": "D0", "loci": ["plantuml.puml:6-13"],
        "reason": "0010:r1:baseline_issue_3: The autonomous submachine structure is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete autonomous-mode source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 3): {
        "d": "D0", "loci": ["plantuml.puml:15-16"],
        "reason": "0010:r1:baseline_issue_4: The handover coverage is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete handover source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 4): {
        "d": "D0", "loci": ["plantuml.puml:19-21"],
        "reason": "0010:r1:baseline_issue_5: The Power Off target is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power Off source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 5): {
        "d": "D0", "loci": ["plantuml.puml:5, 18"],
        "reason": "0010:r1:baseline_issue_6: The extra Power On edge is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power On source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 1, 6): {
        "d": "D0", "loci": ["plantuml.puml:2"],
        "reason": "0010:r1:baseline_issue_7: The initial Power On edge is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete initial source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:2, 5"],
        "reason": "0010:r2:baseline_issue_1: The Power On placement is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power On source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 2, 2): {
        "d": "D0", "loci": ["plantuml.puml:15-16"],
        "reason": "0010:r2:baseline_issue_3: The handover coverage is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete handover source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 2, 3): {
        "d": "D0", "loci": ["plantuml.puml:19-21"],
        "reason": "0010:r2:baseline_issue_4: The Auto Final Power Off construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Auto Final source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 2, 4): {
        "d": "D0", "loci": ["plantuml.puml:6-13"],
        "reason": "0010:r2:baseline_issue_5: The autonomous submachine construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete autonomous-mode source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:2, 5"],
        "reason": "0010:r3:baseline_issue_1: The Power On construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power On source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:6-13"],
        "reason": "0010:r3:baseline_issue_2: The autonomous submachine construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete autonomous-mode source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 3, 3): {
        "d": "D0", "loci": ["plantuml.puml:15-16, 21"],
        "reason": "0010:r3:baseline_issue_4: The Auto Final handover construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Auto Final handover source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 3, 4): {
        "d": "D0", "loci": ["plantuml.puml:19-21"],
        "reason": "0010:r3:baseline_issue_5: The Power Off target construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power Off source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0010", 3, 5): {
        "d": "D0", "loci": ["plantuml.puml:19"],
        "reason": "0010:r3:baseline_issue_6: The incomplete Power Off construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Power Off source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0011", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:12"],
        "reason": "0011:r1:baseline_issue_2: BrakingState to InitialState on Signal Feedback Sent is explicitly required by the NL, so the report's asserted defect is not established.",
        "basis": "0011:r1:baseline_issue_2: NL lines 1-3 require the feedback return; PlantUML line 12 contains the exact transition.",
        "same_pair": "The report does not match the ledgered extra ClampingLoseState or dead ClampingState claims.",
    },
    ("0011", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:12"],
        "reason": "0011:r2:baseline_issue_2: The feedback return edge is required by the author NL and is present exactly in the source. It is not a defect.",
        "basis": "0011:r2:baseline_issue_2: NL line 2 requires return to InitialState after signal feedback; PlantUML line 12 provides BrakingState --> InitialState : Signal Feedback Sent.",
        "same_pair": "No 0011 ledger item matches this present required transition.",
    },
    ("0011", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:12"],
        "reason": "0011:r3:baseline_issue_2: The report's asserted undesired BrakingState feedback path is explicitly required by the NL and present in the author source.",
        "basis": "0011:r3:baseline_issue_2: NL line 2 states that the device returns to the initial state after feedback; PlantUML line 12 contains that edge.",
        "same_pair": "No 0011 ledger expected concerns a required BrakingState feedback edge.",
    },
    ("0011", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0011:r1:baseline_issue_1: The extra ClampingLoseState construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0011", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0011:r2:baseline_issue_1: The extra ClampingLoseState construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0011", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:14-15"],
        "reason": "0011:r3:baseline_issue_1: The extra ClampingLoseState construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete ClampingLoseState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0012", 1, 1): {
        "d": "A0", "loci": ["plantuml.puml:4-9"],
        "reason": "0012:r1:baseline_issue_2: The report claims the Operate internal chain is incomplete, but the complete source includes Idle to AcceleratingOrCruising, AcceleratingOrCruising to Braking, and Braking to Idle. The claimed missing structure is false.",
        "basis": "0012:r1:baseline_issue_2: NL line 3 requires action-dependent transitions; PlantUML lines 4-9 contain all three named states and the accelerate, brake, and stop edges.",
        "same_pair": "The pair ledger concerns the unguarded Off-to-Terminate transition and fake termination notation; the complete internal chain is NO_MATCH.",
    },
    ("0012", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:4-9"],
        "reason": "0012:r3:baseline_issue_2: The report demands a direct Idle-to-Braking stop path, but the NL describes action-dependent progression and the source has the coherent Idle to AcceleratingOrCruising to Braking to Idle chain. No direct edge is required.",
        "basis": "0012:r3:baseline_issue_2: NL lines 1 and 3 do not require stopping from Idle; PlantUML lines 4-9 show the complete sequential path. The report's stronger direct-edge reading is not compelled.",
        "same_pair": "No 0012 ledger item requires a direct Idle-to-Braking transition.",
    },
    ("0012", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:11-12"],
        "reason": "0012:r1:baseline_issue_1: The Off-to-Terminate construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Off-to-Terminate source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0012", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:11-12"],
        "reason": "0012:r2:baseline_issue_1: The Off-to-Terminate construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Off-to-Terminate source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0012", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:11-12"],
        "reason": "0012:r3:baseline_issue_1: The Off-to-Terminate construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Off-to-Terminate source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:20-21"],
        "reason": "0014:r1:baseline_issue_1: Obstacle Detected is a valid trigger label on the InMotion-to-EmergencyStopping edge. The source requirement does not require a different lexical form for detecting the obstacle.",
        "basis": "0014:r1:baseline_issue_1: NL lines 2-3 require entry when an obstacle is detected and then sending a signal; PlantUML lines 20-21 provide the input transition. The report's claimed transition-label error is not established.",
        "same_pair": "The ledger signal expected concerns the missing output action inside EmergencyStopping, not the valid input trigger edge.",
    },
    ("0014", 1, 4): {
        "d": "D0", "loci": ["plantuml.puml:14-17"],
        "reason": "0014:r1:baseline_issue_5: Ready to Stop/Decelerate is descriptive state text inside Approaching. The NL says the system remains until ready to stop or decelerate, so this annotation is a compatible representation, not a forbidden extra behavior.",
        "basis": "0014:r1:baseline_issue_5: NL line 10 names readiness as the stopping boundary; PlantUML lines 14-17 define Approaching with Nearing Destination and Ready to Stop/Decelerate descriptions. No transition is required by the source for this phrase.",
        "same_pair": "No 0014 ledger item covers a descriptive readiness annotation inside Approaching.",
    },
    ("0014", 1, 5): {
        "d": "D0", "loci": ["plantuml.puml:20"],
        "reason": "0014:r1:baseline_issue_6: SendArrived is a lexical spelling variation in a free-text transition label; the transition also contains Arrived/Stop and its semantic target is Stopping. The source does not establish a distinct required identifier token.",
        "basis": "0014:r1:baseline_issue_6: NL line 2 writes Arrived/Stop, Send Arrived in prose; PlantUML line 20 writes Arrived/Stop, SendArrived on the InMotion-to-Stopping edge. The transition role and action words remain identifiable.",
        "same_pair": "No 0014 expected item treats this label-spacing variation as a distinct defect.",
    },
    ("0014", 2, 3): {
        "d": "D0", "loci": ["plantuml.puml:20"],
        "reason": "0014:r2:baseline_issue_4: SendArrived is a text spelling variation on the correct Arrived/Stop transition. No source obligation requires a machine-readable token with a space in this free-text label.",
        "basis": "0014:r2:baseline_issue_4: NL line 2 names the arrival action; PlantUML line 20 targets Stopping and includes Arrived/Stop, SendArrived. The claimed semantic omission is not supported.",
        "same_pair": "No 0014 ledger expected matches a label-spacing complaint.",
    },
    ("0014", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:20-21, 24-27"],
        "reason": "0014:r3:baseline_issue_1: The source contains both required InMotion exits and an EmergencyStopping body. Reusing the obstacle phrase as the input label does not by itself remove the required transition or action.",
        "basis": "0014:r3:baseline_issue_1: NL lines 2-3 require obstacle-triggered entry and actions; PlantUML lines 20-21 contain the transition and lines 24-27 contain the EmergencyStopping annotations. The alleged incomplete trigger/action binding is not established.",
        "same_pair": "The pair expected rows cover missing initial entry, misplaced Entry action, and missing output actions; this broad trigger-label complaint has NO_MATCH.",
    },
    ("0014", 3, 2): {
        "d": "D0", "loci": ["plantuml.puml:14-17"],
        "reason": "0014:r3:baseline_issue_3: Approaching is a state and therefore remains active absent an outgoing transition; its descriptive lines represent the approaching/readiness semantics. An explicit hold loop is not required.",
        "basis": "0014:r3:baseline_issue_3: NL lines 9-10 require sending Send and remaining while nearing; PlantUML lines 14-17 define the state and descriptions. The report's asserted missing persistence behavior is a false defect claim.",
        "same_pair": "No 0014 ledger item requires an explicit Approaching self-loop.",
    },
    ("0014", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:24-27"],
        "reason": "0014:r1:baseline_issue_2: The EmergencyStopping action omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete EmergencyStopping source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 1, 2): {
        "d": "D0", "loci": ["plantuml.puml:7"],
        "reason": "0014:r1:baseline_issue_3: The Entry/Accelerate placement is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Accelerating-entry source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 1, 3): {
        "d": "D0", "loci": ["plantuml.puml:14-17"],
        "reason": "0014:r1:baseline_issue_4: The Approaching Send omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Approaching source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:2"],
        "reason": "0014:r2:baseline_issue_1: The missing DoorsClosing initial edge is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete initial source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:14-17"],
        "reason": "0014:r2:baseline_issue_2: The Approaching Send omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Approaching source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 2, 2): {
        "d": "D0", "loci": ["plantuml.puml:21, 24-27"],
        "reason": "0014:r2:baseline_issue_3: The missing EmergencyStopping signal action is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete EmergencyStopping signal source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:24-27"],
        "reason": "0014:r3:baseline_issue_2: The EmergencyStopping signal action is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete EmergencyStopping signal source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 3, 3): {
        "d": "D0", "loci": ["plantuml.puml:14-17"],
        "reason": "0014:r3:baseline_issue_4: The Approaching Send omission is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Approaching source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0014", 3, 4): {
        "d": "D0", "loci": ["plantuml.puml:7"],
        "reason": "0014:r3:baseline_issue_5: The Entry/Accelerate placement is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Accelerating-entry source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0016", 1, 1): {
        "d": "A0", "loci": ["plantuml.puml:4-21, 23-28, 30-35"],
        "reason": "0016:r1:baseline_issue_2: The report says returning to SearchMission does not define a search entry, but SearchMission has an explicit initial transition to Region1 and the returning edges target SearchMission. The asserted absence is refuted by the source.",
        "basis": "0016:r1:baseline_issue_2: PlantUML lines 4-6 define SearchMission's [*] --> Region1 entry; lines 23 and 27, and lines 30 and 34, provide the return paths. Composite-state entry semantics therefore supplies the initial search region.",
        "same_pair": "The 0016 expected items concern region nesting, repeated Search identifiers, Region3 completion, and a labeled initial edge; this claimed absent re-entry target is NO_MATCH.",
    },
    ("0016", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:17-20"],
        "reason": "0016:r1:baseline_issue_1: The Region3 completion construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete Region3 source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0017", 1, 1): {
        "d": "D2", "loci": ["plantuml.puml:2-17"],
        "reason": "0017:r1:baseline_issue_2: The author source only defines three collision-type states and no collision-avoidance control actions, while the NL explicitly requires concurrent activation of different collision-avoidance controls. This is a clear novel defect.",
        "basis": "0017:r1:baseline_issue_2: NL lines 2-3 distinguish possible collisions from concurrently activated avoidance controls; PlantUML lines 2-17 contain only F, R, and P states with Collision avoided exits and no control actions.",
        "same_pair": "The ledger items cover labeled region initial edges and absent external activation of the compound state; missing control actions is NO_MATCH.",
    },
    ("0017", 1, 2): {
        "d": "D1", "loci": ["plantuml.puml:4-15"],
        "reason": "0017:r1:baseline_issue_3: The state aliases Frontend collision, Rear-end collision, and Collision with pedestrian can denote detected collision categories or possible-collision modes. The NL does not resolve that naming distinction, so D1 novel.",
        "basis": "0017:r1:baseline_issue_3: NL line 2 says possible collision, while PlantUML lines 4-15 name the three states without a possible qualifier. The state names are compatible with both a risk-mode and an occurred-collision reading.",
        "same_pair": "No 0017 ledger item treats the lexical possible-versus-detected state-name distinction as the expected defect.",
    },
    ("0017", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:4, 9, 14"],
        "reason": "0017:r1:baseline_issue_1: The labeled initial edges are a pair-specific expected claim and are excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete labeled initial-edge source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 1, 3): {
        "d": "A0", "loci": ["plantuml.puml:42"],
        "reason": "0019:r1:baseline_issue_4: The report calls the collision-avoidance activation guard incorrect, but the author NL uses the same highway and urban front-distance alternatives and the source includes them in the guard text.",
        "basis": "0019:r1:baseline_issue_4: NL line 12 gives front distance <15 in highway mode or <10 in urban mode; PlantUML line 42 contains that expression. The alleged source mismatch is false.",
        "same_pair": "The ledger collision-avoidance expected is the missing initial transition, not the matching distance guard.",
    },
    ("0019", 1, 4): {
        "d": "A0", "loci": ["plantuml.puml:43"],
        "reason": "0019:r1:baseline_issue_5: The source uses the conjunction front_inactive and rear_inactive and pedestrian_inactive, exactly matching the NL's three no-danger conditions. The report's claim that the condition is too strict is not an author-source defect.",
        "basis": "0019:r1:baseline_issue_5: NL line 13 lists all three inactive conditions; PlantUML line 43 has the same conjunction. The source provides no basis for treating the conjunction as erroneous.",
        "same_pair": "No 0019 expected item concerns replacing the explicitly stated all-inactive return condition.",
    },
    ("0019", 1, 5): {
        "d": "A0", "loci": ["plantuml.puml:37-38"],
        "reason": "0019:r1:baseline_issue_6: The dynamic mode transitions have the directions and guards required by the NL: HighwayMode to UrbanMode on urban_way=true and UrbanMode to HighwayMode on high_way=true. The report's asserted mismatch is refuted.",
        "basis": "0019:r1:baseline_issue_6: NL line 11 states the two directions and conditions; PlantUML lines 37-38 encode them exactly.",
        "same_pair": "No 0019 expected item concerns the dynamic mode-switch direction because the source satisfies it.",
    },
    ("0019", 2, 5): {
        "d": "D0", "loci": ["plantuml.puml:23-34"],
        "reason": "0019:r2:baseline_issue_6: The report demands behavior after entering intersection, but the NL only requires transitions into intersection and does not prescribe a subsequent transition. The absence is unspecified, not a proven violation.",
        "basis": "0019:r2:baseline_issue_6: NL lines 7-9 require enter_urban/straight to intersection; PlantUML lines 23-34 provide those incoming transitions. No author obligation defines the post-intersection behavior.",
        "same_pair": "The 0019 ledger expected rows concern highway guard ambiguity, collision-system initialization, and finish-condition scope; post-intersection behavior is NO_MATCH.",
    },
    ("0019", 2, 7): {
        "d": "D1", "loci": ["plantuml.puml:41-44"],
        "reason": "0019:r2:baseline_issue_8: The source writes the highway/urban mode qualifiers in informal text (`in hwy mode or <10 in urban mode`) rather than a fully explicit boolean expression. It can be read as a faithful shorthand or as an under-specified executable condition, so D1 novel.",
        "basis": "0019:r2:baseline_issue_8: NL line 12 defines the same mode-dependent threshold semantically; PlantUML line 42 uses an informal mixed expression. The source supports both a shorthand and a genuine formalization concern.",
        "same_pair": "The ledger's 0019 items do not assert this exact informal guard syntax as an expected issue; the expected initialization and finish rows are NO_MATCH.",
    },
    ("0019", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:10-21"],
        "reason": "0019:r1:baseline_issue_1: The highway exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete highway exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 1, 1): {
        "d": "D0", "loci": ["plantuml.puml:23-35"],
        "reason": "0019:r1:baseline_issue_2: The urban exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete urban exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 1, 2): {
        "d": "D0", "loci": ["plantuml.puml:41-43"],
        "reason": "0019:r1:baseline_issue_3: The missing collision-avoidance initial transition is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete collision-system source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 1, 0): {
        "d": "D0", "loci": ["plantuml.puml:10-21"],
        "reason": "0019:r1:baseline_issue_1: The highway exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete highway exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 0): {
        "d": "D0", "loci": ["plantuml.puml:12-13"],
        "reason": "0019:r2:baseline_issue_1: The identical HighwayMode guards are a pair-specific expected claim and are excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete enter_hwy source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 1): {
        "d": "D0", "loci": ["plantuml.puml:12-13"],
        "reason": "0019:r2:baseline_issue_2: The missing independent HighwayMode cruise condition is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete enter_hwy source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 2): {
        "d": "D0", "loci": ["plantuml.puml:16-21"],
        "reason": "0019:r2:baseline_issue_3: The highway exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete highway exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 3): {
        "d": "D0", "loci": ["plantuml.puml:30, 35"],
        "reason": "0019:r2:baseline_issue_4: The urban exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete urban exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 4): {
        "d": "D0", "loci": ["plantuml.puml:35"],
        "reason": "0019:r2:baseline_issue_5: The urban completion-source construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete urban completion source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 2, 6): {
        "d": "D0", "loci": ["plantuml.puml:41-43"],
        "reason": "0019:r2:baseline_issue_7: The missing collision-avoidance initial transition is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete collision-system source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 3, 0): {
        "d": "D0", "loci": ["plantuml.puml:10-21"],
        "reason": "0019:r3:baseline_issue_1: The highway exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete highway exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 3, 1): {
        "d": "D0", "loci": ["plantuml.puml:30, 35"],
        "reason": "0019:r3:baseline_issue_2: The urban exit construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete urban exit source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 3, 2): {
        "d": "D0", "loci": ["plantuml.puml:41-43"],
        "reason": "0019:r3:baseline_issue_3: The missing collision-avoidance initial transition is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete collision-system source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
    ("0019", 3, 3): {
        "d": "D1", "loci": ["plantuml.puml:42"],
        "reason": "0019:r3:baseline_issue_4: The source's mixed textual guard for highway/urban mode can be interpreted as shorthand for the NL condition or as insufficiently explicit for an executable model. Both readings remain source-compatible, so D1 novel.",
        "basis": "0019:r3:baseline_issue_4: NL line 12 supplies the semantic alternatives; PlantUML line 42 uses `dist_to_front<15 in hwy mode or <10 in urban mode` inside a larger text label. This is a real ambiguity, not a proven D2 failure.",
        "same_pair": "No 0019 expected row asserts this exact textual guard form; the pair's expected initialization and finish claims are NO_MATCH.",
    },
    ("0019", 3, 4): {
        "d": "D0", "loci": ["plantuml.puml:10-21, 23-35"],
        "reason": "0019:r3:baseline_issue_5: The HighwayMode and UrbanMode completion construction is a pair-specific expected claim and is excluded from this non-K proposal.",
        "basis": "This entry is excluded from the proposal because its concrete FinishState source locus has a positive pair-specific expected relation. No Track B decision is emitted for it.",
        "same_pair": "excluded", "exclude": True,
    },
}


# These raw identities were read during the same census but have a
# pair-specific positive relation and therefore are outside the requested
# non-K proposal.  Their identities and hashes remain in raw_census.
OMITTED_KEYS = {
    ("0002", 1, 0), ("0002", 1, 1), ("0002", 1, 2), ("0002", 2, 0),
    ("0002", 2, 1), ("0002", 3, 0), ("0002", 3, 1),
    ("0005", 2, 0), ("0005", 3, 0), ("0005", 3, 1), ("0005", 3, 2),
    ("0005", 3, 3), ("0005", 3, 4), ("0005", 3, 5), ("0005", 3, 6),
    ("0005", 3, 7),
    ("0009", 1, 1), ("0009", 1, 2), ("0009", 1, 5),
    ("0009", 3, 0), ("0009", 3, 1), ("0009", 3, 2), ("0009", 3, 5),
    ("0009", 3, 6),
    ("0013", 1, 0), ("0013", 1, 1), ("0013", 1, 2), ("0013", 1, 3),
    ("0013", 2, 0), ("0013", 2, 1), ("0013", 2, 2), ("0013", 3, 0),
    ("0013", 3, 1),
    ("0015", 3, 0), ("0015", 3, 1), ("0015", 3, 2), ("0015", 3, 3),
}


def all_raw_reports() -> list[dict]:
    rows = []
    for record in sorted(RAW_ROOT.glob("run*/[0-9][0-9][0-9][0-9]-luna/record.json")):
        pair = record.parent.name[:4]
        if not (0 <= int(pair) <= 19):
            continue
        payload = json.loads(record.read_text())
        source_pair = SOURCE_ROOT / pair
        if payload.get("inputs", {}).get("nl_sha256") != sha256(source_pair / "nl.txt").removeprefix("sha256:"):
            raise AssertionError(f"raw NL hash does not close to source closure: {record}")
        if payload.get("inputs", {}).get("plantuml_sha256") != sha256(source_pair / "plantuml.puml").removeprefix("sha256:"):
            raise AssertionError(f"raw PlantUML hash does not close to source closure: {record}")
        for index, issue in enumerate(payload.get("parsed_output", {}).get("issues", [])):
            rows.append({
                "pair_id": pair,
                "round": int(payload["round"]),
                "finding_index": index,
                "original_report_id": f"{pair}:r{payload['round']}:baseline_issue_{index + 1}",
                "raw_method_path": record.relative_to(ARCHIVE).as_posix(),
                "raw_json_pointer": f"/parsed_output/issues/{index}",
                "raw_sha256": sha256(record),
                "issue": issue,
                "record": record,
            })
    return rows


def build() -> dict:
    ledger = json.loads(LEDGER_PATH.read_text())
    ledger_items = ledger["items"]
    if len(ledger_items) != 145:
        raise AssertionError(f"expected 145 ledger items, found {len(ledger_items)}")
    raw_rows = all_raw_reports()
    raw_keys = {(r["pair_id"], r["round"], r["finding_index"]) for r in raw_rows}
    assessment_keys = set(ASSESSMENTS)
    if not assessment_keys <= raw_keys:
        raise AssertionError(f"assessment keys absent from raw: {sorted(assessment_keys - raw_keys)}")

    if set(OMITTED_KEYS) != raw_keys - assessment_keys:
        raise AssertionError("omitted raw scope is not exactly the unassessed raw set")
    included = [r for r in raw_rows if (r["pair_id"], r["round"], r["finding_index"]) in ASSESSMENTS and not ASSESSMENTS[(r["pair_id"], r["round"], r["finding_index"])].get("exclude")]
    missing = [(r["pair_id"], r["round"], r["finding_index"]) for r in included if (r["pair_id"], r["round"], r["finding_index"]) not in ASSESSMENTS]
    if missing:
        raise AssertionError(f"included raw reports without blind assessment: {missing}")

    proposals = []
    for raw in included:
        key = (raw["pair_id"], raw["round"], raw["finding_index"])
        audit = ASSESSMENTS[key]
        parsed_issue = raw["issue"]
        pair_source = SOURCE_ROOT / raw["pair_id"]
        d_tier = audit["d"]
        validity = "INVALID" if d_tier in {"D0", "A0"} else "VALID_NOVEL"
        kni = "I" if validity == "INVALID" else "N"
        source_refs = [
            ref(raw["record"], pointer=raw["raw_json_pointer"]),
            ref(pair_source / "nl.txt", line=1),
            ref(pair_source / "plantuml.puml"),
            ref(LEDGER_PATH),
        ]
        relation_rows = []
        full_ids = []
        partial_ids = []
        no_ids = []
        for expected_id, expected in sorted(ledger_items.items()):
            expected_pair = expected["pair"]
            if expected_pair != raw["pair_id"]:
                relation_reason = f"NO_MATCH for {raw['original_report_id']}: expected {expected_id} belongs to pair {expected_pair}; cross-pair matching is not admissible."
                relation_basis = "Mechanical pair boundary from the raw report identity and ledger item pair field; no semantic cross-pair relation is proposed."
            else:
                relation_reason = f"NO_MATCH for {raw['original_report_id']} against {expected_id}: {audit['same_pair']}"
                relation_basis = f"Manual raw-first comparison of the complete report and author source against ledger item {expected_id}; no FULL_MATCH or PARTIAL_MATCH is proposed."
            relation_rows.append({
                "expected_id": expected_id,
                "relation": "NO_MATCH",
                "reason": relation_reason,
                "basis": relation_basis,
                "source_refs": [
                    ref(raw["record"], pointer=raw["raw_json_pointer"]),
                    ref(LEDGER_PATH, pointer=f"/items/{expected_id}"),
                ],
                "report_owned_field_refs": [
                    f"{raw['raw_json_pointer']}/issue",
                    f"{raw['raw_json_pointer']}/where",
                    f"{raw['raw_json_pointer']}/reason",
                ],
            })
            no_ids.append(expected_id)
        proposal = {
            "review_status": "PROPOSAL",
            "reviewer_id": REVIEWER,
            "reference_visible": False,
            "primary_visible": False,
            "pair_id": raw["pair_id"],
            "round": raw["round"],
            "original_report_id": raw["original_report_id"],
            "finding_index": raw["finding_index"],
            "raw_method_path": raw["raw_method_path"],
            "raw_json_pointer": raw["raw_json_pointer"],
            "raw_sha256": raw["raw_sha256"],
            "source_hashes": {
                "nl_sha256": sha256(pair_source / "nl.txt"),
                "plantuml_sha256": sha256(pair_source / "plantuml.puml"),
            },
            "raw_finding": parsed_issue,
            "raw_text": {
                "issue": parsed_issue.get("issue", ""),
                "where": parsed_issue.get("where", ""),
                "reason": parsed_issue.get("reason", ""),
                "basis": parsed_issue.get("basis"),
            },
            "observed_source_fact_status": "REFUTED" if d_tier == "A0" else "ESTABLISHED",
            "normative_violation_status": "NOT_ESTABLISHED" if d_tier in {"D0", "A0"} else "ESTABLISHED",
            "defect_claim_status": "DEFECT_CLAIM",
            "d_tier": d_tier,
            "a0_type": "FALSE_POSITIVE" if d_tier == "A0" else None,
            "validity_proposal": validity,
            "corrected_kni_proposal": kni,
            "witness": {
                "level": "W1",
                "concrete_locations": audit["loci"],
                "executable_object": None,
                "receipt": None,
                "artifact_sha256": None,
                "terminal_result": None,
                "reason": "The raw finding points to concrete author-source locations, but no baseline executable witness receipt was used or upgraded in this blind proposal.",
                "basis": f"Raw report where field and author PlantUML source for {raw['original_report_id']}; W is kept separate from D/A and relation.",
            },
            "source_loci": audit["loci"],
            "reason": audit["reason"],
            "basis": audit["basis"],
            "source_refs": source_refs,
            "relations": relation_rows,
            "full_ledger_ids": full_ids,
            "partial_ledger_ids": partial_ids,
            "no_match_ledger_ids": no_ids,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "submission_basis": "Blind raw-first proposal; no v2 decision, old label, Track A file, or reviewer conclusion was read.",
        }
        proposals.append(proposal)

    census = [{
        "pair_id": r["pair_id"],
        "round": r["round"],
        "finding_index": r["finding_index"],
        "original_report_id": r["original_report_id"],
        "raw_method_path": r["raw_method_path"],
        "raw_json_pointer": r["raw_json_pointer"],
        "raw_sha256": r["raw_sha256"],
        "in_proposal": (r["pair_id"], r["round"], r["finding_index"]) in {(p["pair_id"], p["round"], p["finding_index"]) for p in proposals},
    } for r in raw_rows]
    proposal_ids = [p["original_report_id"] for p in proposals]
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-b-proposal",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "review_status": "PROPOSAL",
        "reviewer_id": REVIEWER,
        "blind_scope": {
            "pair_min": "0000",
            "pair_max": "0019",
            "side": "x1v2_baseline",
            "reference_visible": False,
            "primary_visible": False,
            "prohibited_inputs_read": [],
        },
        "input_files": {
            "ledger": {"path": LEDGER_PATH.relative_to(ARCHIVE).as_posix(), "sha256": sha256(LEDGER_PATH), "expected_count": 145},
            "source_root": SOURCE_ROOT.relative_to(ARCHIVE).as_posix(),
            "raw_method_root": RAW_ROOT.relative_to(ARCHIVE).as_posix(),
        },
        "raw_census": census,
        "coverage": {
            "raw_report_count_in_range": len(raw_rows),
            "proposal_report_count": len(proposals),
            "dense_relation_rows": len(proposals) * 145,
            "proposal_ids": proposal_ids,
            "raw_reports_not_emitted": len(raw_rows) - len(proposals),
            "not_emitted_basis": "Only raw-first reports with no positive pair-specific ledger relation were emitted; the census retains identity and hash coverage for the complete range.",
        },
        "proposals": proposals,
        "generation": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "script": "scripts/evaluation/build_track_b_0000_0019.py",
            "provider_calls": 0,
            "method_calls": 0,
            "judge_calls": 0,
        },
    }


if __name__ == "__main__":
    result = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "output": OUT.relative_to(ARCHIVE).as_posix(),
        "raw_report_count": result["coverage"]["raw_report_count_in_range"],
        "proposal_report_count": result["coverage"]["proposal_report_count"],
        "dense_relation_rows": result["coverage"]["dense_relation_rows"],
    }, ensure_ascii=False))
