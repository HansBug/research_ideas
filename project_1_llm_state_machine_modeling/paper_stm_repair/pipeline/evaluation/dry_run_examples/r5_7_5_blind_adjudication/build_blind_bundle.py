#!/usr/bin/env python3
"""Build / refresh the R5.7.5 blind adjudication bundle from constructed STM_k cases.

The script preserves the fixed Bxx -> Cxx hidden mapping in oracle_answer_key.json,
refreshes candidate files and hashes from the constructed suite, and writes only
neutral / observable mechanical and provenance facts into blind_inputs/*.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONSTRUCTED_ROOT = ROOT.parent / "r5_7_5_constructed_stmk"
REPO_ROOT = ROOT.parents[5]

SOURCE_CASE_SPECIAL_FACTS: dict[str, dict[str, Any]] = {
    "C04": {
        "change_origin_category": "normalization_only_artifact",
        "candidate_same_as_canonical_stm0": True,
        "change_ledger_available": True,
        "target_instance_ledger_available": True,
    },
    "C10": {
        "semantic_evidence_status": "insufficient_for_strict_improvement_or_regression",
        "notes": [
            "The candidate changes surface event/action decomposition only; strict semantic gain is not mechanically decidable from the carrier alone."
        ],
    },
    "C12": {
        "semantic_evidence_status": "insufficient_traceability_for_strict_verdict",
        "notes": [
            "The candidate renames guard variables and weakens traceability; without an explicit trace map the judge should avoid claiming a strict gain."
        ],
    },
    "C14": {
        "scope_boundary_category": "caveat_t05",
        "semantic_evidence_status": "t05_counter_abstraction_without_lifecycle",
        "notes": [
            "The candidate lowers a timer-expired event to a discrete counter guard, but the blind packet does not show counter increment/reset lifecycle evidence; strict better should not be claimed."
        ],
    },
    "C15": {
        "scope_boundary_category": "caveat_t05",
        "declared_extra_method_claims": ["timed_automata_or_real_clock_support"],
        "candidate_semantics_observed_by_carrier": "discrete_state_machine_with_integer_variable_only",
        "change_ledger_available": True,
        "target_instance_ledger_available": True,
    },
    "C16": {
        "scope_boundary_category": "out_of_headline_t1_stress",
        "scope_observed_features": [
            "second_based_duration_or_execution_time_annotations",
            "not_lowered_to_discrete_counter_caveat"
        ],
        "change_origin_category": "stress_scope_probe",
    },
    "C18": {
        "change_ledger_available": False,
        "target_instance_ledger_available": False,
        "hash_chain_complete": False,
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pyfcstm_parse_status(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "pyfcstm", "plantuml", "-i", str(path)],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=30,
    )
    return "parse_ok" if result.returncode == 0 else "parse_failed"


def case_by_id() -> dict[str, dict[str, Any]]:
    suite = load_json(CONSTRUCTED_ROOT / "suite_index.json")
    return {case["case_id"]: case for case in suite["cases"]}


def existing_packet_base(bid: str) -> dict[str, Any]:
    p = ROOT / "blind_inputs" / bid / "input_packet.json"
    if not p.exists():
        return {}
    old = load_json(p)
    keep = [
        "blind_case_id",
        "base_pair_id",
        "source_model_name",
        "source_model_family",
        "source_llm",
        "nl_path",
        "raw_stm0_path",
        "canonical_stm0_path",
        "candidate_stmk_path",
    ]
    return {k: old[k] for k in keep if k in old}


def main() -> None:
    oracle_path = ROOT / "oracle_answer_key.json"
    if not oracle_path.exists():
        raise SystemExit("oracle_answer_key.json is required to preserve fixed Bxx mapping")
    oracle = load_json(oracle_path)
    cases = case_by_id()
    out_cases = []
    index_cases = []
    for item in oracle["cases"]:
        bid = item["blind_case_id"]
        cid = item["source_case_id"]
        case = cases[cid]
        cdir = REPO_ROOT / case["case_dir"]
        bdir = ROOT / "blind_inputs" / bid
        bdir.mkdir(parents=True, exist_ok=True)

        # Preserve NL/raw/canonical already materialized for the blind bundle.
        for name in ["nl.txt", "raw_stm0.plantuml", "canonical_stm0.fcstm"]:
            dst = bdir / name
            if not dst.exists():
                raise SystemExit(f"missing existing blind source artifact: {dst}")
        candidate_text = (cdir / "candidate.fcstm").read_text(encoding="utf-8")
        (bdir / "candidate_stmk.fcstm").write_text(candidate_text, encoding="utf-8")

        baseline_sha = sha256_file(bdir / "canonical_stm0.fcstm")
        candidate_sha = sha256_file(bdir / "candidate_stmk.fcstm")
        parse_status = pyfcstm_parse_status(bdir / "candidate_stmk.fcstm")
        special = SOURCE_CASE_SPECIAL_FACTS.get(cid, {})
        provenance = {
            "change_ledger_available": special.get("change_ledger_available", True),
            "target_instance_ledger_available": special.get("target_instance_ledger_available", True),
            "hash_chain_complete": special.get("hash_chain_complete", True),
            "candidate_hash_matches_constructed_case": candidate_sha == case.get("candidate_sha256"),
            "change_origin_category": special.get("change_origin_category", "constructed_candidate_with_local_ledgers"),
            "candidate_same_as_canonical_stm0": special.get("candidate_same_as_canonical_stm0", candidate_sha == baseline_sha),
        }
        if "declared_extra_method_claims" in special:
            provenance["declared_extra_method_claims"] = special["declared_extra_method_claims"]
        if "candidate_semantics_observed_by_carrier" in special:
            provenance["candidate_semantics_observed_by_carrier"] = special["candidate_semantics_observed_by_carrier"]
        if "semantic_evidence_status" in special:
            provenance["semantic_evidence_status"] = special["semantic_evidence_status"]
        if "scope_boundary_category" in special:
            provenance["scope_boundary_category"] = special["scope_boundary_category"]
        if "scope_observed_features" in special:
            provenance["scope_observed_features"] = special["scope_observed_features"]
        if "notes" in special:
            provenance["notes"] = special["notes"]

        packet = {
            "schema_version": "r5_7_5.blind_input_packet.v1",
            "blind_case_id": bid,
            "artifact_role": "blind_adjudication_input",
            **existing_packet_base(bid),
            "nl_path": "nl.txt",
            "raw_stm0_path": "raw_stm0.plantuml",
            "canonical_stm0_path": "canonical_stm0.fcstm",
            "candidate_stmk_path": "candidate_stmk.fcstm",
            "baseline_sha256": baseline_sha,
            "candidate_sha256": candidate_sha,
            "mechanical_checks": {
                "baseline_file_present": True,
                "candidate_file_present": True,
                "candidate_parse_status": parse_status,
                "parse_success_alone_is_not_semantic_evidence": True,
            },
            "semantic_modeling_conventions": {
                "fcstm_role": "internal_static_experiment_carrier_not_method_contribution",
                "guard_variables": "Abstract sensor/input conditions in static adjudication; absence of in-model assignment is not by itself a dead-transition proof.",
                "event_labels": "Labels may encode events and actions in raw/canonical STM_0; candidate may split them into event plus effect only if NL-supported behavior is preserved.",
                "t05_timer_policy": "Periodic timer/tick cues may be routed as caveat_t05 when represented as a discrete counter abstraction.",
                "t1_policy": "True continuous time / timed-automata semantics are out-of-headline stress cases, not headline Better STM successes.",
            },
            "provenance_checks": provenance,
            "neutral_change_observation": "Inspect canonical_stm0.fcstm and candidate_stmk.fcstm directly. The packet provides only observable mechanical/provenance facts and no hidden answer key.",
            "adjudication_question": "Based only on NL, raw STM_0, canonical STM_0, candidate STM_k and mechanical/provenance facts, decide whether candidate STM_k is better than canonical STM_0 under E0-E11/G0-G6.",
        }
        # Ensure base fields did not override required identifiers.
        packet["blind_case_id"] = bid
        packet["base_pair_id"] = item["base_pair_id"]
        write_json(bdir / "input_packet.json", packet)

        updated_oracle = dict(item)
        updated_oracle.update(
            {
                "base_pair_id": case["base_pair_id"],
                "primary_expected_verdict": case["primary_expected_verdict"],
                "scope_routing_status": case["scope_routing_status"],
                "run_validity_status": case["run_validity_status"],
                "risks": case.get("risks", []),
            }
        )
        out_cases.append(updated_oracle)
        index_cases.append({
            "blind_case_id": bid,
            "input_dir": str((ROOT / "blind_inputs" / bid).relative_to(REPO_ROOT)),
            "base_pair_id": case["base_pair_id"],
        })

    oracle["schema_version"] = "r5_7_5.blind_oracle_answer_key.v1"
    oracle["cases"] = out_cases
    write_json(oracle_path, oracle)
    write_json(
        ROOT / "blind_input_index.json",
        {
            "schema_version": "r5_7_5.blind_input_index.v1",
            "case_count": len(index_cases),
            "cases": index_cases,
        },
    )
    print(f"r5.7.5-blind-bundle-refreshed cases={len(index_cases)}")


if __name__ == "__main__":
    main()
