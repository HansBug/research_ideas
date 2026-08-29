#!/usr/bin/env python3
"""Apply explicit pane5 semantic reread corrections to manual-input rows.

The correction table below is authored from a raw-first reread in the
authorized pane5 session.  It is deliberately an explicit data table: this
command does not infer D/A, relation, validity, or K/N/I from text, legacy
labels, IDs, or similarity.  The confirmation and recomputation commands
perform the remaining closure checks and regenerate all derived artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ARCHIVE_RELATIVE = "final_results/v60_current_vs_x1v2_baseline"
INPUT_NAME = "pane5_manual_input_v2.json"


def _relation(row: dict[str, Any], expected_id: str, value: str, reason: str, basis: str) -> None:
    """Update one explicitly adjudicated dense relation row."""
    for item in row["relation_rows"]:
        if item["expected_id"] == expected_id:
            item["relation"] = value
            item["reason"] = reason
            item["basis"] = basis
            return
    raise ValueError(f"missing expected relation {expected_id} for {row['report_id']}")


def _clear_relations(row: dict[str, Any]) -> None:
    """Close an invalid report's dense relation matrix to NO_MATCH."""
    for item in row["relation_rows"]:
        item["relation"] = "NO_MATCH"


def _set_review_text(row: dict[str, Any], reason: str, basis: str, arbitration_reason: str, arbitration_basis: str) -> None:
    """Persist report-specific primary and final reread attestations."""
    report_id = row["report_id"]
    row["reason"] = f"{report_id}: {reason}"
    row["basis"] = f"{report_id}: {basis}"
    row["primary_reason"] = f"{report_id}: pane5 raw-first reread: {reason}"
    row["primary_basis"] = f"{report_id}: {basis}"
    row["arbitration_reason"] = f"{report_id}: {arbitration_reason}"
    row["arbitration_basis"] = f"{report_id}: {arbitration_basis}"
    row["confirmation_basis"] = (
        f"{row['report_id']}: pane5 reread the exact raw target, author NL, author PlantUML, "
        "and the complete expected-ledger closure before confirming the corrected fields."
    )
    row["attestation"] = (
        f"{row['report_id']}: authorized pane5 session reread and confirmed this targeted correction "
        "after the independent raw-first proposal was unblinded."
    )
    row["disagreement"] = (
        f"{row['report_id']}: independent proposal and prior pane5 input differed; targeted reread and "
        "arbitration resolved the difference from raw/source evidence."
    )


def corrections() -> dict[str, dict[str, Any]]:
    """Return the manually authored correction table."""
    return {
        "0014:r3:issue:1": {
            "fact_status": "REFUTED", "strict_da": "A0", "a0_type": "NOT_A_DEFECT_CLAIM", "canonical_group_key": None,
            "reason": "The raw finding reports that the current analysis has no supplied executable retention trace. The author NL explicitly states that Approaching continues until readiness to stop or decelerate, while the PlantUML carries the Approaching state and its descriptive text. The unresolved/deferred lack of a native retention trace is a limitation of this method's evidence closure, not an author-source defect. The final classification is A0/NOT_A_DEFECT_CLAIM and therefore INVALID/I; W remains W1 because the state locus is precise but no terminal executable receipt exists.",
            "basis": "Pane5 reread raw/v60_current/method/method/0014/round-3.json#/report_issue_clusters/1, reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0014/nl.txt:9-10, and reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0014/plantuml.puml:14-17. The raw observation is an analysis-evidence gap; no author-source retention violation is established. The independent proposal was compared only after this reread.",
            "relations": {},
            "arbitration_reason": "The author source supplies the retention statement; the report only establishes that this method did not obtain a native retention receipt. That is current-only representation/analysis debt, so A0/NOT_A_DEFECT_CLAIM with all relations NO_MATCH.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0014:r3:issue:1; W1 is retained independently of the invalid closure.",
        },
        "0023:r1:issue:0": {
            "fact_status": "ESTABLISHED", "strict_da": "D1", "a0_type": None, "canonical_group_key": None,
            "reason": "The report correctly locates PumpState and the absence of a lifecycle action carrier, but two competent readings remain. Under the strict executable-model reading, the body text Pump Activated is not an action slot. Under the author-facing reading, the NL phrase where the pump is activated or controlled and the PlantUML body text can document the intended behavior without specifying a lifecycle phase. The fact is established with D1, and its relation to the ledger's PumpState continuation defect is only PARTIAL because adding an outgoing transition is not identical to adding an action.",
            "basis": "Pane5 reread raw/v60_current/method/method/0023/round-1.json#/report_issue_clusters/0, reference/x1v2_input_closure/pairs/0023/nl.txt:3-4, reference/x1v2_input_closure/pairs/0023/plantuml.puml:4,9, and reference/ledger.json#/items/INS-0023-01. The two readings are tied to the exact author syntax and NL wording, not lexical similarity or a legacy label.",
            "relations": {"INS-0023-01": ("PARTIAL_MATCH", "The report identifies a real PumpState behavior/continuation facet related to INS-0023-01, but the report's missing action carrier and the expected missing outgoing transition are not the same defect identity or repair overlap.", "Raw/source and expected evidence were reread for 0023:r1:issue:0; the expected item is reference/ledger.json#/items/INS-0023-01. The relation is PARTIAL, not a primary hit." )},
            "arbitration_reason": "D1 is retained because the body description and the executable action-slot reading both survive. The expected relation is PARTIAL only, preserving the distinction between action absence and transition absence.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0023:r1:issue:0; canonical K/N/I is derived after this explicit input.",
        },
        "0029:r1:issue:9": {
            "fact_status": "ESTABLISHED", "strict_da": "D1", "a0_type": None, "canonical_group_key": None,
            "reason": "The report establishes a termination-related source fact: FinishState is not an explicit final sink and the author source also contains continuing mode transitions. Two competent readings survive: the NL's word ends may designate the shared FinishState as a semantic completion boundary, or the literal source structure may require an explicit final sink and disallow further continuation. The report therefore remains D1, with the direct scope/target issue EIS-0029-05 as PARTIAL rather than asserting the distinct no-terminal-sink issue as a second full match.",
            "basis": "Pane5 reread raw/v60_current/method/method/0029/round-1.json#/report_issue_clusters/6, reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0029/nl.txt:6,10, and reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0029/plantuml.puml:15-17,37-44. Expected evidence was reread at reference/ledger.json#/items/EIS-0029-05 and INS-0029-05.",
            "relations": {"EIS-0029-05": ("PARTIAL_MATCH", "The report is genuinely related to the expected FinishState scope/termination facet, but the surviving semantic readings prevent an identity-level FULL_MATCH.", "Raw/source and expected evidence were reread for 0029:r1:issue:9; EIS-0029-05 is the directly related scope item and the distinct INS-0029-05 relation is NO_MATCH for this final row." )},
            "arbitration_reason": "The source supports a real termination concern but does not defeat the alternative semantic reading. D1 and PARTIAL are the conservative final closure.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0029:r1:issue:9; relation closure is regenerated deterministically.",
        },
        "0049:r2:issue:30": {
            "fact_status": "REFUTED", "strict_da": "A0", "a0_type": "FALSE_POSITIVE", "canonical_group_key": None,
            "reason": "The report's exact named-edge claim is refuted as an author-defect attribution. The PlantUML author source contains a nested AutonomousMode initial pseudostate with [*] --> InitialState, which supplies the required initial relation even though the closed representation does not expose it as a named AutonomousMode --> InitialState edge. The report mistakes a representation shape for an author-source omission, so it is A0/FALSE_POSITIVE and INVALID/I. The exact terminal receipt remains independently eligible for W2.",
            "basis": "Pane5 reread raw/v60_current/method/method/0049/round-2.json#/report_issue_clusters/21, reference/x1v2_input_closure/pairs/0049/nl.txt:1-2, reference/x1v2_input_closure/pairs/0049/plantuml.puml:2-6, and the original S2 receipt at raw/v60_current/method/method/0049/round-2.json#/report_issue_clusters/21/receipt. The receipt proves the closed-model named-edge query, not an author-source defect.",
            "relations": {},
            "arbitration_reason": "The nested initial pseudostate is the author-source initialization construct; absence of the queried named edge is not a defect. A0/FALSE_POSITIVE closes all expected relations to NO_MATCH while W2 remains an independent evidence axis.",
            "arbitration_basis": "Author PlantUML and the exact terminal receipt were reread and their hashes are preserved in the evidence-read row for 0049:r2:issue:30.",
        },
        "0053:r1:issue:0": {
            "fact_status": "ESTABLISHED", "strict_da": "D2", "a0_type": None, "canonical_group_key": None,
            "reason": "The report identifies the PumpControl-owned initial edge to UnspecifiedInitial and the separate PumpRegion-scoped entry to PumpState. The NL explicitly requires the system first to enter PumpState, so the author-source owner/target obligation is violated. The report is a direct match to EIS-0053-01. DIFF-0053-01 concerns the separate wrapper-region/separator semantics and is not a second relation for this initial-entry claim.",
            "basis": "Pane5 reread raw/v60_current/method/method/0053/round-1.json#/report_issue_clusters/0, reference/x1v2_input_closure/pairs/0053/nl.txt:1-3, reference/x1v2_input_closure/pairs/0053/plantuml.puml:3-18, and reference/ledger.json#/items/EIS-0053-01 and DIFF-0053-01. The two expected properties were separated by author-source locus and repair obligation.",
            "relations": {"EIS-0053-01": ("FULL_MATCH", "The report's PumpControl initial-entry locus, required first PumpState target, and repair obligation are the same as EIS-0053-01.", "Raw/source and expected evidence were reread for 0053:r1:issue:0; DIFF-0053-01 is a separate wrapper-region property and remains NO_MATCH." )},
            "arbitration_reason": "The initial-entry defect is a direct EIS-0053-01 match; the wrapper-region issue is not double-counted.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0053:r1:issue:0; dense relation rows are regenerated from this explicit table.",
        },
        "0014:r1:baseline_issue_1": {
            "fact_status": "ESTABLISHED", "strict_da": "D1", "a0_type": None, "canonical_group_key": None,
            "reason": "The finding correctly sees Obstacle Detected on the incoming transition and the separate EmergencyStopping body text. Two readings remain: the transition label can be read as the obstacle trigger, while the state text may document the signal; or the source lacks an explicit output-action carrier required by NL3. The report therefore establishes an ambiguous signal-role defect at D1 and is only PARTIAL to VU-0014-01.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0014-luna/record.json#/parsed_output/issues/0, reference/x1v2_input_closure/pairs/0014/nl.txt:2-3, reference/x1v2_input_closure/pairs/0014/plantuml.puml:20-26, and reference/ledger.json#/items/VU-0014-01. The output-action finding is kept distinct from the transition-label wording.",
            "relations": {"VU-0014-01": ("PARTIAL_MATCH", "The finding exposes the same obstacle-signal facet as VU-0014-01, but its broader trigger/label claim leaves a surviving role interpretation and cannot be a FULL identity match.", "Raw/source and expected evidence were reread for 0014:r1:baseline_issue_1; the relation is PARTIAL and does not create a primary hit." )},
            "arbitration_reason": "The transition-label and output-action readings are not interchangeable; D1/PARTIAL preserves that distinction.",
            "arbitration_basis": "Author NL/PlantUML and the raw finding were reread in the pane5 session; evidence hashes remain in the canonical evidence-read row.",
        },
        "0023:r1:baseline_issue_1": {
            "fact_status": "ESTABLISHED", "strict_da": "D1", "a0_type": None, "canonical_group_key": None,
            "reason": "The source has three PumpControl initial edges while NL3 says the system first transitions to PumpState. The initial-entry fact is established, but the expected ledger item INS-0023-01 is the separate PumpState no-outgoing-transition defect. The two issues share the PumpControl/PumpState operating facet without sharing the same defect identity or repair; therefore D1/PARTIAL is the final conservative relation closure.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0023-luna/record.json#/parsed_output/issues/0, reference/x1v2_input_closure/pairs/0023/nl.txt:1-5, reference/x1v2_input_closure/pairs/0023/plantuml.puml:2-12, and reference/ledger.json#/items/INS-0023-01. The direct initial-entry error is not relabeled as the distinct dead-end issue.",
            "relations": {"INS-0023-01": ("PARTIAL_MATCH", "The report is a real related PumpState/PumpControl operating facet, but the expected item concerns the missing outgoing transition from PumpState; the identities and repairs are not the same.", "Raw/source and expected evidence were reread for 0023:r1:baseline_issue_1; relation is PARTIAL, so it is supported coverage but not a primary hit." )},
            "arbitration_reason": "The initial-entry and no-outgoing-transition claims are distinct; the source supports a related facet only. D1/PARTIAL prevents an overclaimed FULL hit.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0023:r1:baseline_issue_1; K/N/I is derived after relation closure.",
        },
        "0029:r1:baseline_issue_2": {
            "fact_status": "ESTABLISHED", "strict_da": "D2", "a0_type": None, "canonical_group_key": None,
            "reason": "The raw finding claims that cruise goes directly to FinishState under dist_to_exit<2. The author PlantUML contains exactly that edge and also contains lane_change --> exit_hwy under the same condition, while NL4-6 distinguish highway exit from auto_finished completion. The fact and violated obligation are explicit and unambiguous, so this is D2/K with a FULL match to EIS-0029-03.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/1, reference/x1v2_input_closure/pairs/0029/nl.txt:4-6, reference/x1v2_input_closure/pairs/0029/plantuml.puml:14-17, and reference/ledger.json#/items/EIS-0029-03. The exact source edge and condition were checked before unblinding.",
            "relations": {"EIS-0029-03": ("FULL_MATCH", "The report names the same cruise source, dist_to_exit<2 condition, FinishState target conflict, and repair-relevant obligation as EIS-0029-03.", "Raw/source and expected evidence were reread for 0029:r1:baseline_issue_2; the exact source edge is at PlantUML line 15 and the companion exit_hwy edge at line 17." )},
            "arbitration_reason": "The author source explicitly separates highway exit from auto_finished completion; the finding is a direct known defect.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0029:r1:baseline_issue_2; corrected K/FULL closure is deterministic.",
        },
        "0029:r1:baseline_issue_3": {
            "fact_status": "ESTABLISHED", "strict_da": "D1", "a0_type": None, "canonical_group_key": None,
            "reason": "The source names exit_hwy as the target of the highway-exit transition but does not give it an explicit state block or continuation. One reading treats that name as an implicit exit marker in the author notation; the other treats an undeclared target with no continuation as an incomplete state-machine carrier. The fact is established with D1, and the relation to EIS-0029-03 is PARTIAL because the missing declaration/continuation is related to, but not identical with, the expected same-condition target conflict.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/2, reference/x1v2_input_closure/pairs/0029/nl.txt:4-5, reference/x1v2_input_closure/pairs/0029/plantuml.puml:16-17, and reference/ledger.json#/items/EIS-0029-03. No text similarity or old label was used for the relation.",
            "relations": {"EIS-0029-03": ("PARTIAL_MATCH", "The undefined exit_hwy target is a real related exit-semantics facet, but it is not the same defect identity as the expected cruise/FinishState target conflict.", "Raw/source and expected evidence were reread for 0029:r1:baseline_issue_3; PARTIAL is supported coverage and is excluded from primary hit and FP calculations." )},
            "arbitration_reason": "The target declaration has a surviving implicit-marker reading, so D1 is retained; its ledger relation is related but only PARTIAL.",
            "arbitration_basis": "Author NL/PlantUML and raw finding were reread in pane5; evidence hashes remain in the canonical evidence-read row.",
        },
        "0029:r1:baseline_issue_7": {
            "fact_status": "ESTABLISHED", "strict_da": "D0", "a0_type": None, "canonical_group_key": "0029:I:0029:r1:baseline_issue_7",
            "reason": "The source fact is true: the recovery edge uses front_inactive, rear_inactive, and pedestrian_inactive conjunctively. However, NL13 says the system returns when there is no active danger and then lists those three inactive conditions; it does not establish that any single inactive condition should suffice or that the conjunction is wrong. The report therefore has no surviving violated obligation and is D0/INVALID/I, not a valid novel defect.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/6, reference/x1v2_input_closure/pairs/0029/nl.txt:12-13, and reference/x1v2_input_closure/pairs/0029/plantuml.puml:31-34. The explicit conjunctive reading is preserved; no scope or A0 classification is used.",
            "relations": {},
            "arbitration_reason": "The source and NL are compatible with the conjunction; fact成立但义务未成立 is D0, which deterministically closes to INVALID/I with all NO_MATCH.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0029:r1:baseline_issue_7; invalid closure is checked by the Pydantic validator.",
        },
        "0053:r1:baseline_issue_1": {
            "fact_status": "ESTABLISHED", "strict_da": "D0", "a0_type": None, "canonical_group_key": "0053:I:0053:r1:baseline_issue_1",
            "reason": "The author source does contain three wrapper states PumpRegion, WaterRegion, and MethaneRegion, so the structural fact is established. But the NL requires three main substates and operating alternatives without explicitly prohibiting wrapper regions or prescribing mutual exclusion. The report has no established violated author obligation; this is D0/INVALID/I rather than A0/FALSE_POSITIVE.",
            "basis": "Pane5 reread raw/x1v2_baseline/method/run1/0053-luna/record.json#/parsed_output/issues/0, reference/x1v2_input_closure/pairs/0053/nl.txt:1-5, and reference/x1v2_input_closure/pairs/0053/plantuml.puml:5-20. The true wrapper fact is kept separate from the unproven obligation.",
            "relations": {},
            "arbitration_reason": "The wrapper structure is present in the author source; the evidence does not establish that wrappers violate the stated NL. D0/INVALID/I is the conservative final label.",
            "arbitration_basis": "Raw/source pointers and hashes are preserved in pane5_evidence_reads.json for 0053:r1:baseline_issue_1; no A0 subtype is introduced.",
        },
    }


def main() -> None:
    """Apply the explicit targeted reread table and preserve a correction log."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    path = archive / "derived" / "manual_adjudication_v2" / INPUT_NAME
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("rows")
    if not isinstance(rows, list):
        raise ValueError("pane5 manual input has no rows")
    by_id = {str(row["report_id"]): row for row in rows}
    table = corrections()
    missing = sorted(set(table) - set(by_id))
    if missing:
        raise ValueError(f"targeted correction IDs missing from pane5 input: {missing}")
    for report_id, correction in table.items():
        row = by_id[report_id]
        row["fact_status"] = correction["fact_status"]
        row["strict_da"] = correction["strict_da"]
        row["a0_type"] = correction["a0_type"]
        row["canonical_group_key"] = correction["canonical_group_key"]
        # A reread correction replaces the report's complete dense relation
        # judgment.  Clear old proposal/primary positives before applying the
        # explicit relation table, including for valid D1/D2 rows.
        _clear_relations(row)
        for expected_id, (value, reason, basis) in correction["relations"].items():
            _relation(row, expected_id, value, reason, basis)
        _set_review_text(row, correction["reason"], correction["basis"], correction["arbitration_reason"], correction["arbitration_basis"])
        row["review_status"] = "ARBITRATED"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    correction_log = archive / "derived" / "manual_adjudication_v2" / "pane5_targeted_re_review.json"
    existing = json.loads(correction_log.read_text(encoding="utf-8")) if correction_log.is_file() else {"schema": "paper1.manual-adjudication.targeted-rereview.v1", "rows": []}
    existing["schema"] = "paper1.manual-adjudication.targeted-rereview.v1"
    existing["rows"] = [
        {
            "report_id": report_id,
            "status": "ARBITRATED",
            "primary_reviewer_id": "human:pane5-supervised-adjudicator",
            "independent_reviewer_id": "subagent:semantic-raw-first-independent-proposal",
            "final_adjudicator_id": "human:pane5-supervised-adjudicator",
            "human_confirmation": True,
            "human_supervised_session": True,
            "reason": correction["reason"],
            "basis": correction["basis"],
            "disposition": "canonical pane5 input corrected; full canonical recomputation required",
            "source_refs": by_id[report_id]["source_refs"],
        }
        for report_id, correction in sorted(table.items())
    ]
    correction_log.write_text(json.dumps(existing, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "TARGETED_PANE5_CORRECTIONS", "rows": len(table), "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
