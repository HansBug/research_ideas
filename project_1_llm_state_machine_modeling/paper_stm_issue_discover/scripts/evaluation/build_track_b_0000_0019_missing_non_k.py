"""Build the missing raw-first Track-B coverage for baseline pairs 0000--0019.

This is a coverage supplement for the already submitted blind Track-B batch.
It reads only frozen raw records, the complete author-source closure, the
ledger, and protocol files.  The semantic table is explicit per report; the
program only joins it to exact source bytes and expands the 145-row relation
vector.  It does not read or import v2/v3 decisions, Judge output, or another
reviewer's proposal.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARCHIVE = Path(__file__).parents[2] / "final_results/v60_current_vs_x1v2_baseline"
RAW_ROOT = ARCHIVE / "raw/x1v2_baseline/method"
SOURCE_ROOT = ARCHIVE / "reference/x1v2_input_closure/pairs"
LEDGER_PATH = ARCHIVE / "reference/ledger.json"
OUT = ARCHIVE / "derived/manual_adjudication_v3_baseline_ni/proposals/track_b_0000_0019_missing_non_k.json"
REVIEWER = "subagent:track-b-0000-0019-coverage-supplement"


REPORTS = {
    "0000:r1:baseline_issue_2": {"d": "D1", "loci": ["plantuml.puml:13"], "positive": {"EIS-0000-02": "FULL_MATCH"}, "reason": "The reported comma-separated handover label is present in the author PlantUML. The NL lists human steering, braking, and being in AutoFinal without resolving whether these are alternative triggers, a conjunction, or a state qualifier; the concrete alternative readings survive, so this is D1 rather than an unambiguous D2.", "basis": "Pair 0000 NL line 4 lists the three handover conditions; PlantUML line 13 stores them as one free-text transition label. EIS-0000-02 describes this same loss of condition structure. The relation is selected only after reading the source and the expected item.", "alternative": "A competent reader can interpret the comma list as a conjunction with AutoFinal as a state qualifier, while another can interpret it as alternatives. That live reading does not erase the source fact but prevents D2."},
    "0002:r1:baseline_issue_3": {"d": "D2", "loci": ["plantuml.puml:4-5"], "positive": {"EIS-0002-01": "FULL_MATCH"}, "reason": "PumpControl's internal initial edge targets InitialState instead of the PumpState required as the first substate. The report's source fact and the violated first-entry obligation are both explicit.", "basis": "Pair 0002 NL lines 2-3 name PumpState as the first substate and PlantUML line 5 targets InitialState. EIS-0002-01 identifies the same wrong initial target.", "alternative": "InitialState could be treated as an informal alias for PumpState, but the author source separately names PumpState and never defines InitialState; that reading is not supported by the complete source."},
    "0002:r2:baseline_issue_1": {"d": "D2", "loci": ["plantuml.puml:5", "plantuml.puml:7-24"], "positive": {"EIS-0002-01": "FULL_MATCH"}, "reason": "The report correctly identifies that PumpControl's initial path goes to an undeclared InitialState rather than the required PumpState. This is a direct source-backed violation, not merely a missing ledger match.", "basis": "Pair 0002 NL line 3 requires the first transition to PumpState; PlantUML line 5 is the only PumpControl initial edge and points to InitialState. EIS-0002-01 is the same concrete wrong-entry defect.", "alternative": "The initial edge might be read as a placeholder for a later choice, but no later edge leaves InitialState and no source text defines that placeholder, so the alternative does not preserve the stated first-entry behavior."},
    "0002:r3:baseline_issue_1": {"d": "D2", "loci": ["plantuml.puml:5", "plantuml.puml:7-24"], "positive": {"EIS-0002-02": "FULL_MATCH"}, "reason": "The report identifies the absence of any PumpControl initial or subsequent path to PumpState, WaterState, or MethaneState. All three named main substates are structurally unreachable from the only internal initial edge.", "basis": "Pair 0002 NL line 2 names the three main substates and lines 3-5 require access to them; PlantUML line 5 targets only InitialState, with no edge from it to any named substate. EIS-0002-02 is the exact all-three-unreachable claim.", "alternative": "The three nested blocks could be treated as declarations sufficient for reachability, but declaration alone does not supply an incoming transition; the source contains no such path."},
    "0002:r3:baseline_issue_2": {"d": "D2", "loci": ["plantuml.puml:5", "plantuml.puml:7-9"], "positive": {"EIS-0002-01": "FULL_MATCH"}, "reason": "The report's claim that the first PumpControl transition does not enter PumpState is true. The only internal initial edge enters InitialState, so the explicit first-entry requirement is not encoded.", "basis": "Pair 0002 NL line 3 says the system first transitions to PumpState; PlantUML line 5 says [*] --> InitialState. EIS-0002-01 is the same source-level mismatch.", "alternative": "InitialState could be an intended staging state, but it is neither defined nor connected to PumpState, and the NL gives no staging step; that interpretation cannot satisfy the first-entry sentence."},
    "0004:r3:baseline_issue_5": {"d": "D2", "loci": ["plantuml.puml:2", "plantuml.puml:4-6"], "positive": {"EIS-0004-01": "FULL_MATCH"}, "reason": "The model has a top-level DoorsClosing and an inner initial edge that targets the same name from within the DoorsClosing block. The resulting self/out-of-scope initial construction is the concrete hierarchy defect reported.", "basis": "Pair 0004 NL line 1 requires a single initial DoorsClosing state; PlantUML lines 2 and 4-5 contain the outer and inner same-name construction. EIS-0004-01 records this exact malformed inner initial target.", "alternative": "A reader could regard both names as an intentional alias, but the inner initial edge still lacks a distinct child target and does not define a valid internal entry; the source does not document aliasing."},
    "0005:r3:baseline_issue_2": {"d": "D1", "loci": ["plantuml.puml:10-16"], "positive": {"EIS-0005-02": "FULL_MATCH"}, "reason": "DoorOpenWithItem is explicitly made composite with an extra DoorIdleWithItem child, while the NL describes the named DoorOpenWithItem state as the carrier of remove, close, and cooking-time actions. The structural fact is clear, but whether the extra representation is an impermissible loss of direct state semantics has a competent alternative reading, so D1.", "basis": "Pair 0005 NL lines 3-4 describe actions from DoorOpenWithItem; PlantUML lines 10-15 enter DoorIdleWithItem and place the actions there. EIS-0005-02 concerns the same forward-reference/composite hierarchy distortion.", "alternative": "The child can be read as an implementation refinement of the named state, with its outgoing edges preserving the three externally observable actions. That reading keeps the fact but leaves a real hierarchy/semantic ambiguity."},
    "0005:r3:baseline_issue_3": {"d": "D1", "loci": ["plantuml.puml:18-23"], "positive": {}, "reason": "DoorShutWithItem is represented as a composite state whose active child is ItemInside, although the NL describes DoorShutWithItem as the state receiving open-door and cooking-time events. The extra child is real, but the same behavior can be read as a valid implementation refinement, so this remains D1 novel rather than an automatic invalidity or known match.", "basis": "Pair 0005 NL lines 4-5 name DoorShutWithItem as the behavioral state; PlantUML lines 18-22 introduce ItemInside and preserve both named outgoing actions. No ledger item exactly covers this distinct child-state representation.", "alternative": "A competent reader can treat ItemInside as the internal active substate of DoorShutWithItem while preserving the parent state's external contract. The report's concern remains a live representation ambiguity, not an unambiguous violated obligation."},
    "0005:r3:baseline_issue_8": {"d": "D2", "loci": ["plantuml.puml:33-39"], "positive": {"EIS-0005-03": "FULL_MATCH"}, "reason": "The report correctly observes that Cooking's Cancel transition has no timer or cooking-time handling, while the source explicitly requires time-related behavior. The author source contains no variable, effect, or entry/exit action that supplies that behavior.", "basis": "Pair 0005 NL lines 5-8 require cooking time to be displayed/updated and describe timer behavior; PlantUML lines 33-39 contain only state transitions and no timer effect. EIS-0005-03 is the corresponding absent data/action semantics.", "alternative": "A state named Cooking could be assumed to imply a timer, but the source gives no such convention and the required update/cancel behavior is not encoded by a bare Cancel edge; this does not defeat the explicit obligation."},
    "0007:r1:baseline_issue_1": {"d": "D2", "loci": ["plantuml.puml:4-9", "plantuml.puml:31-32"], "positive": {}, "reason": "The three detection outcomes lead only among CollisionDetection substates, while the sole CollisionDetection-to-CollisionAvoidance edge is a generic outer edge labeled Collision Mode Active. The source does not connect the required frontend, rear-end, or pedestrian detections to activation of the avoidance submachine.", "basis": "Pair 0007 NL lines 2-3 require activation on any of three detected collision possibilities; PlantUML lines 6-8 terminate those detections inside CollisionDetection and line 31 supplies no detection-specific activation edge. The pair ledger items concern a dead initial state, labeled inner initials, and an extra OperationalControls tree, not this activation omission.", "alternative": "The outer transition could be treated as an implicit completion transition from the composite CollisionDetection, but no trigger or completion rule connects it to the three detection states, so it cannot establish the required event-conditioned activation."},
    "0009:r1:baseline_issue_6": {"d": "D0", "loci": ["plantuml.puml:21", "plantuml.puml:25", "plantuml.puml:45-46"], "positive": {}, "reason": "The report accurately notes that FinishState has no separate state declaration, but PlantUML permits a state to be introduced by a transition and the first reference establishes its containing scope. The observation therefore does not establish a defect by itself.", "basis": "Pair 0009 PlantUML first references FinishState on line 21 inside HighwayMode and reuses it on lines 25 and 45-46; the source language does not require a separate state declaration. The real hierarchy/exit consequences are distinct claims and are not silently assigned to this report.", "alternative": "A strict style reading could require an explicit declaration for clarity, but that is a representation preference rather than a source-backed defect obligation here; the fact is retained and the normative defect is D0."},
    "0012:r3:baseline_issue_1": {"d": "D2", "loci": ["plantuml.puml:10-12"], "positive": {"EIS-0012-01": "FULL_MATCH", "INS-0012-01": "FULL_MATCH"}, "reason": "The source adds an untriggered Off-to-Terminate transition and models Terminate as an ordinary state with a final annotation, so Off cannot remain waiting for start and no actual terminal pseudostate is supplied. Both reported consequences are source-backed.", "basis": "Pair 0012 NL line 2 defines start/keyOff signals and does not authorize automatic Off completion; PlantUML lines 10-12 contain Off --> Terminate and Terminate : final. EIS-0012-01 covers the unconditional completion edge and INS-0012-01 covers the ordinary-state terminal construction.", "alternative": "The final annotation might be read as informal documentation, but it does not create UML termination semantics and does not justify an automatic transition out of Off; that reading cannot remove either explicit mismatch."},
    "0015:r3:baseline_issue_2": {"d": "D2", "loci": ["plantuml.puml:25-30"], "positive": {}, "reason": "The NL explicitly states that Start enters Cooking where the timer starts, but the corresponding transition contains only a Start trigger and no timer-start effect or state action. The omission is a source-backed defect and is not represented by the sole pair ledger item.", "basis": "Pair 0015 NL line 7 requires timer start after Start; PlantUML line 26 is only ReadytoCook -> Cooking : Start, and the complete file has no timer variable or effect. This is a distinct novel timer-start claim, not an inference from ledger absence alone.", "alternative": "A reader could treat entering a state named Cooking as implicitly starting its timer, but the source does not define that convention and separately describes timer start as a required behavior; the alternative does not eliminate the omission."},
    "0015:r3:baseline_issue_3": {"d": "D2", "loci": ["plantuml.puml:28-30"], "positive": {}, "reason": "The NL explicitly requires opening the door during Cooking to stop the timer before entering DoorOpenWithItem, while the source has only the state transition and no stop-timer effect or action. The reported author-source omission is established.", "basis": "Pair 0015 NL line 8 says opening the door stops the timer; PlantUML line 28 contains only Cooking -> DoorOpenWithItem : Door Opened, and the full source contains no timer-stop effect. This is a separate novel side-effect claim from the ledgered display/update omission.", "alternative": "One might infer timer stopping from leaving Cooking, but the source does not specify that invariant and the NL calls out the stop behavior explicitly; an inference cannot replace the absent effect in this audit."},
    "0019:r1:baseline_issue_2": {"d": "D1", "loci": ["plantuml.puml:23-35", "plantuml.puml:37-38"], "positive": {"EIS-0019-03": "PARTIAL_MATCH"}, "reason": "The report identifies an UrbanMode exit path whose exit_urban node is outside the UrbanMode block and whose FinishState transition is outside the mode. This is part of the ledgered completion-source narrowing family, but this report is limited to the urban side and leaves a live scope interpretation, so PARTIAL and D1 are appropriate.", "basis": "Pair 0019 NL lines 8-10 describe exit_urban inside the urban flow and UrbanMode completion on auto_finished; PlantUML lines 23-35 close UrbanMode before defining exit_urban's FinishState edge. EIS-0019-03 covers the broader source-narrowing completion obligation; this row is not treated as a full duplicate of the two-sided expected statement.", "alternative": "A reader could treat exit_urban as an AutonomousMode-level handoff state reached from UrbanMode, with the outer edge implementing the same observable exit. That reading preserves a real hierarchy concern and supports D1 rather than D2."},
    "0019:r1:baseline_issue_3": {"d": "D2", "loci": ["plantuml.puml:41-44"], "positive": {"EIS-0019-02": "FULL_MATCH"}, "reason": "CollisionAvoidanceSystem has no internal initial edge to collision_avoidance_deactive, despite the NL's explicit initial-state requirement. The two ordinary state-to-state edges do not establish an initial substate.", "basis": "Pair 0019 NL line 12 names collision_avoidance_deactive as the initial state; PlantUML lines 41-44 contain the composite block and two transitions but no [*] initial edge. EIS-0019-02 is the exact missing-initial-edge claim.", "alternative": "The first state named in a composite block could be assumed to be initial, but this source uses explicit [*] initial edges elsewhere and does not define declaration order as an initial-state convention."},
    "0019:r2:baseline_issue_4": {"d": "D1", "loci": ["plantuml.puml:23-35"], "positive": {"EIS-0019-03": "PARTIAL_MATCH"}, "reason": "The source places exit_urban outside the UrbanMode braces even though the report's cited urban exit semantics describe it as part of that mode. The hierarchy fact is established, but an outer handoff interpretation remains possible, so the normative classification is D1 with a partial relation to the broader completion-source expected.", "basis": "Pair 0019 NL lines 8-10 and PlantUML lines 23-35 were read in full; the UrbanMode block closes at line 34, while exit_urban is used at line 30 and defined by the outer line 35. EIS-0019-03 addresses the related completion-source narrowing, not a strict identical instance.", "alternative": "exit_urban may be an intentional mode-exit handoff state at AutonomousMode scope. That is a competent alternative reading but does not remove the mismatch with the NL's stated urban substate flow."},
    "0019:r3:baseline_issue_1": {"d": "D1", "loci": ["plantuml.puml:10-21", "plantuml.puml:37-38"], "positive": {"EIS-0019-03": "PARTIAL_MATCH"}, "reason": "The report correctly observes that HighwayMode's exit path leaves to an outer ExitHighway state and requires a second auto_finished transition, rather than expressing the completion at the mode boundary. The requirement/source relation is real, but the exact source scope admits a mode-exit handoff interpretation, so D1 and PARTIAL.", "basis": "Pair 0019 NL lines 4-6 describe exit and completion; PlantUML lines 10-21 close HighwayMode before ExitHighway -> FinishState and lines 37-38 define mode switching. EIS-0019-03 is the broader ledgered completion-source narrowing family; only the highway instance is covered here.", "alternative": "ExitHighway can be read as an intentional intermediate handoff owned by AutonomousMode, with auto_finished completing it later. That reading leaves an obligation ambiguity and prevents an unqualified D2/FULL label."},
    "0019:r3:baseline_issue_2": {"d": "D1", "loci": ["plantuml.puml:23-35"], "positive": {"EIS-0019-03": "PARTIAL_MATCH"}, "reason": "The report identifies the same outer exit_urban construction and missing direct UrbanMode completion behavior as the r1 urban claim. The source fact is clear, but the outer handoff interpretation remains competent; the relation is partial to the two-sided ledger expectation.", "basis": "Pair 0019 NL lines 8-10 require the urban exit flow and auto_finished completion; PlantUML lines 23-35 place the exit state and completion edge outside UrbanMode. EIS-0019-03 covers the associated narrowing of the auto_finished source.", "alternative": "The outer exit_urban state can be treated as the enclosing mode's handoff representation. That does not fully satisfy the natural reading of the NL, but it is a live interpretation, hence D1."},
    "0019:r3:baseline_issue_5": {"d": "D1", "loci": ["plantuml.puml:10-38"], "positive": {"EIS-0019-03": "FULL_MATCH"}, "reason": "The report covers both HighwayMode and UrbanMode and correctly identifies that auto_finished is consumed only after the outer ExitHighway/exit_urban handoffs, not at the two mode boundaries as the NL states. The completion-source fact is established, but the handoff reading remains a concrete alternative, so D1.", "basis": "Pair 0019 NL lines 6 and 10 require each mode to exit to FinishState on auto_finished; PlantUML lines 21 and 35 put those edges after the exit states and lines 10-34 close the modes. EIS-0019-03 is the exact two-sided completion-source narrowing expected.", "alternative": "A competent reader can interpret ExitHighway and exit_urban as intentional intermediate states in AutonomousMode, with the mode-level wording describing the overall flow rather than the literal transition source. This survives as a D1 alternative but does not erase the source mismatch."},
}


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def source_ref(path: Path, *, pointer: str | None = None, line: int | None = None) -> dict[str, Any]:
    return {"repository_path": path.relative_to(ARCHIVE).as_posix(), "json_pointer": pointer, "line": line, "sha256": sha256(path)}


def find_raw(pair: str, round_number: int) -> Path:
    matches = sorted(RAW_ROOT.glob(f"run{round_number}/{pair}-*/record.json"))
    if len(matches) != 1:
        raise ValueError(f"expected one raw record for {pair}/r{round_number}, found {len(matches)}")
    return matches[0]


def report_id(pair: str, round_number: int, index: int) -> str:
    return f"{pair}:r{round_number}:baseline_issue_{index + 1}"


def load_ledger() -> tuple[dict[str, Any], tuple[str, ...]]:
    document = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    items = document.get("items")
    if not isinstance(items, dict) or len(items) != 145:
        raise ValueError("ledger is not the frozen 145-item input")
    return items, tuple(sorted(items))


def build() -> dict[str, Any]:
    ledger, expected_ids = load_ledger()
    records: list[dict[str, Any]] = []
    source_pairs: dict[str, dict[str, Any]] = {}
    for rid, assessment in REPORTS.items():
        pair, round_token, issue_token = rid.split(":")
        round_number = int(round_token[1:])
        index = int(issue_token.rsplit("_", 1)[1]) - 1
        raw_path = find_raw(pair, round_number)
        raw_document = json.loads(raw_path.read_text(encoding="utf-8"))
        raw_report = raw_document["parsed_output"]["issues"][index]
        nl_path = SOURCE_ROOT / pair / "nl.txt"
        puml_path = SOURCE_ROOT / pair / "plantuml.puml"
        if not nl_path.is_file() or not puml_path.is_file():
            raise FileNotFoundError(f"missing author source closure for pair {pair}")
        nl_text = nl_path.read_text(encoding="utf-8")
        puml_text = puml_path.read_text(encoding="utf-8")
        source_pairs[pair] = {"nl": source_ref(nl_path, line=None), "plantuml": source_ref(puml_path, line=None), "nl_bytes_read": len(nl_text.encode()), "plantuml_bytes_read": len(puml_text.encode())}
        tier = assessment["d"]
        positive = assessment["positive"]
        if tier in {"D0", "A0"} and positive:
            raise ValueError(f"invalid positive relation on {rid}")
        validity = "INVALID" if tier in {"D0", "A0"} else ("VALID_KNOWN" if positive else "VALID_NOVEL")
        kni = "I" if validity == "INVALID" else ("K" if positive else "N")
        raw_ref = source_ref(raw_path, pointer=f"/parsed_output/issues/{index}")
        nl_ref = source_ref(nl_path)
        puml_ref = source_ref(puml_path)
        ledger_ref = source_ref(LEDGER_PATH)
        relations = [{"expected_id": expected_id, "relation": positive.get(expected_id, "NO_MATCH")} for expected_id in expected_ids]
        vector = "".join({"FULL_MATCH": "F", "PARTIAL_MATCH": "P", "NO_MATCH": "N"}[row["relation"]] for row in relations)
        records.append({
            "side": "x1v2_baseline",
            "pair_id": pair,
            "round": round_number,
            "original_report_id": rid,
            "finding_index": index,
            "raw_method_path": raw_path.relative_to(ARCHIVE).as_posix(),
            "raw_json_pointer": f"/parsed_output/issues/{index}",
            "raw_sha256": sha256(raw_path),
            "raw_text": {"issue": raw_report.get("issue", ""), "where": raw_report.get("where", ""), "reason": raw_report.get("reason", ""), "basis": raw_report.get("basis")},
            "observed_source_fact_status": "REFUTED" if tier == "A0" else "ESTABLISHED",
            "normative_violation_status": "NOT_ESTABLISHED" if tier in {"D0", "A0"} else "ESTABLISHED",
            "defect_claim_status": "NO_DEFECT_CLAIM" if tier in {"D0", "A0"} else "DEFECT_CLAIM",
            "d_tier": tier,
            "a0_type": "FALSE_POSITIVE" if tier == "A0" else None,
            "validity_proposal": validity,
            "corrected_kni_proposal": kni,
            "source_loci": assessment["loci"],
            "reason": assessment["reason"],
            "basis": assessment["basis"],
            "alternative_reading": assessment["alternative"],
            "source_refs": [raw_ref, nl_ref, puml_ref, ledger_ref],
            "relation_encoding": {"ledger_item_count": 145, "ledger_order": list(expected_ids), "default_relation_for_unlisted_ids": "NO_MATCH", "overrides": positive, "dense_rows_sha256": canonical_sha(relations)},
            "relation_vector": vector,
            "relation_digest_sha256": canonical_sha({"ledger_order": list(expected_ids), "relations": relations}),
            "relations": relations,
            "reviewer_id": REVIEWER,
            "review_status": "PROPOSAL",
            "reference_visible": False,
            "other_reviewers_visible": False,
        })
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-b-proposal-supplement",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "review_status": "PROPOSAL",
        "reviewer_id": REVIEWER,
        "blind_scope": {"side": "x1v2_baseline", "pair_min": "0000", "pair_max": "0019", "reference_visible": False, "other_reviewers_visible": False},
        "allowed_inputs": ["raw/x1v2_baseline/method/**/record.json", "reference/x1v2_input_closure/pairs/{0000..0019}/nl.txt", "reference/x1v2_input_closure/pairs/{0000..0019}/plantuml.puml", "reference/ledger.json", "discover_matrix/docs/protocol/*.md"],
        "forbidden_inputs_read": ["v2/v3 decisions", "pane5 register", "Judge labels/output", "Track A or other reviewer conclusions"],
        "selection_evidence_gap": "The existing blind Track-B batch omitted these 20 records. This supplement is emitted from an explicit coverage list supplied by the main audit session; the semantic fields below were reread from raw/source/ledger, and no old label is copied into any proposal field.",
        "source_pairs": source_pairs,
        "coverage": {"requested_pair_range": ["0000", "0019"], "proposal_records_written": len(records), "raw_reports_read": len(records), "source_pairs_read": len(source_pairs), "ledger_items_read": 145, "raw_fields_read": ["issue", "where", "reason", "basis"], "all_145_relations": True, "missing_evidence": ["A blind frozen non-K selector was not available inside the raw/source/ledger allowlist; this supplement therefore records its selection boundary explicitly."], "provider_calls": 0, "method_calls": 0, "judge_calls": 0},
        "reports": records,
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "provenance_statement": "Raw-first proposal supplement only. Every emitted record preserves exact raw text and raw/source hashes, carries an explicit per-report D/A reason and basis, and expands all 145 ledger IDs. No final human confirmation or pane5 adjudication is asserted.",
    }


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    value = build()
    OUT.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(value["reports"]), "source_pairs": len(value["source_pairs"]), "ledger_items": 145, "provider_calls": 0}, ensure_ascii=False))
