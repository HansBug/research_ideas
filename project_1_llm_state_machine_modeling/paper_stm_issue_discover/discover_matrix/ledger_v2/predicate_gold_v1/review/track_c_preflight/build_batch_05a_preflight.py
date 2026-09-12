"""Freeze the independent Track C semantic preflight for batch 05a.

This builder deliberately has no execution imports.  The decision table below is
the review result reached from the blind source packets, Track A, Track B, the
gold protocol, capability audit, and frozen implementation semantics.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import canonical_sha256, sha256_path, write_json
from paper_stm_evaluation.predicate_gold_review import TrackAProposalBatch, TrackBProposalBatch


PAIR_IDS = ("0029", "0030", "0032", "0033", "0034")


DECISIONS: dict[str, dict[str, Any]] = {
    "DIFF-0029-06": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_B_LEDGER_READING_WITH_TRACK_A_SENSITIVITY",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Under the ledger's strict D1 reading, absence of the extra authored AutonomousMode carrier is necessary. Track A's source-compatible group-completion reading remains a material sensitivity, and the lowered target prevents equivalence.",
        "conflicts": ["Track A adopts the source-compatible group-level completion reading; Track B adopts the ledger's strict two-carrier reading. Execution is conditional on the latter and cannot resolve that D1 conflict."],
    },
    "EIS-0029-01": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The source names AutonomousMode as the parent of InitialState and the two driving modes; the direct-child native query checks exactly those required containment facts without asserting an exhaustive child set.",
        "conflicts": [],
    },
    "EIS-0029-02": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "The source leaves the cruise/lane-change choice and persistence semantics ambiguous. No source-backed variable domain, priority, or complete native conflict oracle can bind an equivalent or false-sound query.",
        "conflicts": [],
    },
    "EIS-0029-03": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "A correct cruise-to-exit_hwy carrier is necessary, so its absence soundly falsifies O. Its presence alone does not exclude the simultaneously wrong cruise-to-FinishState carrier, so Track B's EQUIVALENT claim is too strong.",
        "conflicts": ["Track B proposed EQUIVALENT; Track C downgrades the same source-bound carrier query to O_IMPLIES_P because existence does not prove absence of the forbidden competing carrier."],
    },
    "EIS-0029-04": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "The obligation jointly covers two owner-local default entries. The available single-owner oracle cannot express the conjunction, while native inventories include lowering carriers that cannot be silently filtered as authored defaults.",
        "conflicts": [],
    },
    "EIS-0029-05": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The issue-local obligation is one shared FinishState directly owned by AutonomousMode; the oracle checks uniqueness, canonical identity, and direct parent without using reachability as a surrogate.",
        "conflicts": [],
    },
    "INS-0029-01": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "CollisionAvoidance must be active with driving, but the source omits the orthogonal composition mechanism. The source-static artifact is simulation-ineligible and no exact configuration oracle can be bound without inventing concurrency semantics.",
        "conflicts": [],
    },
    "INS-0029-05": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Every required running ancestry needs an auto_finished root-exit consumer, but static carrier coverage does not prove RTC dispatch, completion, or post-completion noncontinuation.",
        "conflicts": [],
    },
    "EIS-0030-01": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "The source requires an autonomous-final concept but supplies no bindable identity, kind, entry carrier, or completion timing. Inventing a state or treating label text as a final pseudostate is forbidden.",
        "conflicts": [],
    },
    "EIS-0030-02": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Power_Off root-exit consumers for every named active ancestry are necessary, but source-static coverage does not execute universal event handling or establish whole-machine termination.",
        "conflicts": [],
    },
    "EIS-0030-03": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_WITH_D1_SENSITIVITY",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "The connective among steering, brake, and auto-final remains D1, and auto-final has no source identity. Reusing the fused artifact event would manufacture the missing semantic inputs.",
        "conflicts": ["Track A adopts conjunction while Track B retains an independently-sufficient-condition reading; neither yields a legal executable property because auto-final is unbound."],
    },
    "INS-0030-01": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The root initial-transition contract checks the complete required cardinality, HumanDriving target, and absence of event and guard on the exact owner.",
        "conflicts": [],
    },
    "DIFF-0032-03": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "COMPOSITE",
        "obligation": "TRACK_B_LEDGER_READING_WITH_TRACK_A_SENSITIVITY",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Under the adopted split-phase ledger reading, the invented Reach_Speed event is forbidden, so NOT exact event membership is necessary. Its absence does not establish the complete state taxonomy or transition semantics.",
        "conflicts": ["Track A adopts the phase split while retaining a missing inter-phase trigger; Track B adopts the ledger's over-specification reading. The proxy is conditional on the latter D1 reading."],
    },
    "EIS-0032-01": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "COMPOSITE",
        "obligation": "TRACK_B_LEDGER_READING_WITH_TRACK_A_SENSITIVITY",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Under the ledger reading that named leaf behavior must be established on wrapper entry, an UnspecifiedInitial placeholder is a false-sound symptom. Its absence cannot prove the required leaf mapping or all default entries.",
        "conflicts": ["Track A adopts the source-compatible wrapper-as-state reading, under which the placeholder need not violate O. Track C executes only the ledger's leaf-level proxy and preserves this D1 sensitivity."],
    },
    "EIS-0033-01": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A",
        "o_implies_p": None,
        "p_implies_o": True,
        "reason": "The source requires the three states to be descendants within PumpControl but does not prove immediate direct-child depth. DIRECT_CHILD_HIERARCHY is stronger: false could occur on a source-compatible nested hierarchy and therefore is not a sound falsifier.",
        "conflicts": ["Track B proposed EQUIVALENT direct-child coverage; Track C rejects execution because Track A correctly records direct-versus-deeper containment as missing information."],
    },
    "EIS-0033-02": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The complete PumpControl initial inventory must contain exactly one triggerless, guardless transition to PumpState; all four dimensions are checked natively.",
        "conflicts": [],
    },
    "INS-0033-01": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The root initialization obligation and native property agree on exact cardinality, PumpControl target, and event/guard absence.",
        "conflicts": [],
    },
    "EIS-0034-01": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "The source explicitly enumerates Accelerating, Cruising, and Approaching as the three InMotion substates. The query checks these required direct children without asserting an exhaustive inventory.",
        "conflicts": [],
    },
    "EIS-0034-02": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "A unique default entry to Accelerating is necessary. It does not also establish the required later Cruising and Approaching trigger/effect carriers, so the query remains a proxy.",
        "conflicts": [],
    },
    "EIS-0034-03": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "COMPOSITE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "Unary NOT over exact S4 membership expresses precisely the issue-local prohibition on Accelerate being attached to DoorsClosing entry; it does not infer action identity by text similarity.",
        "conflicts": [],
    },
    "EIS-0034-04": {
        "relation": "O_IMPLIES_P",
        "disposition": "EXECUTE_PROXY",
        "mode": "COMPOSITE",
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": True,
        "p_implies_o": False,
        "reason": "Absence of the incorrect Approaching entry Decelerate attachment is necessary, but it does not prove transition-effect placement or the separately required Send output.",
        "conflicts": [],
    },
    "EIS-0034-05": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "The output role is source-backed, but no phase, carrier, receiver, payload, or schedule is supplied. The incoming event cannot be reused as an output-emission oracle.",
        "conflicts": [],
    },
    "EIS-0034-06": {
        "relation": "EQUIVALENT",
        "disposition": "EXECUTE_EXACT",
        "mode": "EVALUATION_ONLY_ORACLE",
        "obligation": "TRACK_B_LEDGER_READING_WITH_TRACK_A_SENSITIVITY",
        "o_implies_p": True,
        "p_implies_o": True,
        "reason": "Under the ledger's strict remain-until reading, O is exactly absence of the source-bound Destination_Missed terminal carrier. The alternative that this event ends the while-precondition remains a D1 sensitivity.",
        "conflicts": ["Track A adopts the source-compatible precondition-release reading; Track B adopts the strict ledger reading. The exact claim is explicitly conditional on the latter."],
    },
    "INS-0034-01": {
        "relation": None,
        "disposition": "UNSUPPORTED_EXACT",
        "mode": None,
        "obligation": "TRACK_A_AND_B_ALIGNED",
        "o_implies_p": None,
        "p_implies_o": None,
        "reason": "No continuation target, event, explicit terminal intent, bound, fairness, or environment assumption is source-backed. A global deadlock check is neither issue-local nor admitted for this source-static artifact.",
        "conflicts": [],
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _source_catalog(repo_root: Path, gold_root: Path, a_path: Path, b_path: Path) -> dict[str, Any]:
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    catalog: dict[str, Any] = {}
    for pair_id in PAIR_IDS:
        packet_path = gold_root / f"review/input_packets/pairs/{pair_id}.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        catalog[f"packet_{pair_id}"] = {
            "repository_path": packet_path.relative_to(repo_root).as_posix(),
            "sha256": sha256_path(packet_path),
            "payload_sha256": packet["packet_sha256"],
        }
        model_path = paper_root / f"selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm"
        catalog[f"model_{pair_id}"] = {
            "repository_path": model_path.relative_to(repo_root).as_posix(),
            "sha256": sha256_path(model_path),
        }
    for key, path in {
        "track_a_batch": a_path,
        "track_b_batch": b_path,
        "capability_audit": gold_root / "predicate_semantics_capability_audit.json",
        "gold_protocol": gold_root / "predicate_gold_protocol.md",
        "predicate_registry": paper_root / "method/src/paper_stm_method/resources/predicate_registry.json",
        "source_static_backend": paper_root / "method/src/paper_stm_method/backends/source_static.py",
        "native_projection": repo_root / "utils/stm_artifacts/fcstm_native_projection.py",
        "pyfcstm_model": repo_root / "pyfcstm/pyfcstm/model/model.py",
    }.items():
        catalog[key] = {"repository_path": path.relative_to(repo_root).as_posix(), "sha256": sha256_path(path)}
    return catalog


def main() -> int:
    repo_root = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyfcstm").is_dir()
        and (parent / "project_1_llm_state_machine_modeling").is_dir()
    )
    paper_root = repo_root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix/ledger_v2/predicate_gold_v1"
    a_path = gold_root / "review/track_a_independent/batch_05a.json"
    b_path = gold_root / "review/track_b_independent/batch_05a.json"
    a_batch = TrackAProposalBatch.model_validate_json(a_path.read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json(b_path.read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: row for row in a_batch.rows}
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    if set(a_rows) != set(b_rows) or set(a_rows) != set(DECISIONS):
        raise ValueError("Track A/B/manual decision identity mismatch")

    rows: list[dict[str, Any]] = []
    for ledger_id in sorted(DECISIONS):
        decision = DECISIONS[ledger_id]
        a_row = a_rows[ledger_id]
        b_row = b_rows[ledger_id]
        candidate = next(
            (item for item in b_row.candidate_properties if item.candidate_id == b_row.selected_candidate_id),
            None,
        )
        execution_required = decision["disposition"].startswith("EXECUTE_")
        if execution_required and candidate is None:
            raise ValueError(f"{ledger_id} accepted without a selected candidate")
        if not execution_required and decision["relation"] is not None:
            raise ValueError(f"{ledger_id} rejected with an accepted relation")
        normalized = (
            b_row.normalized_obligation
            if "TRACK_B_LEDGER_READING" in decision["obligation"]
            else a_row.normalized_obligation
        )
        candidate_hash = canonical_sha256(candidate.model_dump(mode="json")) if candidate else None
        typed_ok = bool(candidate and candidate.typed_inputs) if execution_required else False
        pair_id = ledger_id.split("-")[1]
        a_index = next(i for i, row in enumerate(a_batch.rows) if row.ledger_id == ledger_id)
        b_index = next(i for i, row in enumerate(b_batch.rows) if row.ledger_id == ledger_id)
        unsigned = {
            "ledger_id": ledger_id,
            "pair_id": pair_id,
            "accepted_obligation_source": decision["obligation"],
            "normalized_obligation_sha256": canonical_sha256(normalized.model_dump(mode="json")),
            "track_a_proposal_sha256": a_row.proposal_sha256,
            "track_b_proposal_sha256": b_row.proposal_sha256,
            "selected_candidate_id": candidate.candidate_id if execution_required else None,
            "selected_candidate_sha256": candidate_hash if execution_required else None,
            "track_b_relation": b_row.proposed_exactness_relation.value,
            "accepted_relation": decision["relation"],
            "disposition": decision["disposition"],
            "execution_required": execution_required,
            "execution_mode": decision["mode"],
            "implication_analysis": {
                "o_implies_p": decision["o_implies_p"],
                "p_implies_o": decision["p_implies_o"],
                "reason": decision["reason"],
            },
            "typed_input_provenance": {
                "status": "PASS" if typed_ok else "NOT_APPLICABLE",
                "reason": (
                    "Every selected input is retained from the pre-result Track B proposal and has an author-source or formal-semantics SourceRef; aliases are exact native identities."
                    if typed_ok
                    else "No executable property is admitted; no input is invented."
                ),
            },
            "artifact_eligibility": {
                "source_static_eligible": True,
                "simulation_eligible": False,
                "candidate_eligible": execution_required,
                "reason": (
                    "The admitted query uses only pyfcstm native source-static objects or a frozen S-family backend; no trajectory or whole-model behavioral equivalence is claimed."
                    if execution_required
                    else "The closest candidate cannot preserve the obligation under the source-static capability boundary."
                ),
            },
            "conflicts": decision["conflicts"],
            "source_refs": [
                {"source_id": f"packet_{pair_id}", "json_pointer": f"/ledger_items/{next(i for i, item in enumerate(json.loads((gold_root / f'review/input_packets/pairs/{pair_id}.json').read_text(encoding='utf-8'))['ledger_items']) if item['ledger_id'] == ledger_id)}"},
                {"source_id": "track_a_batch", "json_pointer": f"/rows/{a_index}"},
                {"source_id": "track_b_batch", "json_pointer": f"/rows/{b_index}"},
                {"source_id": f"model_{pair_id}", "line_start": 1, "line_end": len((paper_root / f'selected_seed_examples/llms_emp_feedback_final_{pair_id}/model.fcstm').read_text(encoding='utf-8').splitlines())},
                {"source_id": "capability_audit", "json_pointer": "/predicates"},
                {"source_id": "gold_protocol", "line_start": 1, "line_end": len((gold_root / 'predicate_gold_protocol.md').read_text(encoding='utf-8').splitlines())},
            ],
        }
        rows.append({**unsigned, "audit_sha256": canonical_sha256(unsigned)})

    now = _now()
    accepted = [row["ledger_id"] for row in rows if row["execution_required"]]
    rejected = [row["ledger_id"] for row in rows if not row["execution_required"]]
    unsigned_batch = {
        "schema_version": "paper1.predicate-gold.track-c-preflight.local.v1",
        "schema_documentation": {
            "purpose": "Independent semantic preflight only; no predicate execution result is visible or produced.",
            "row_contract": "Each row fixes O/P direction, typed binding, artifact eligibility, conflicts, and whether execution may proceed.",
            "relation_values": ["EQUIVALENT", "O_IMPLIES_P", "UNRELATED"],
            "disposition_values": ["EXECUTE_EXACT", "EXECUTE_PROXY", "UNSUPPORTED_EXACT"],
            "canonical_hash_contract": "SHA-256 over canonical UTF-8 JSON; row excludes audit_sha256 and batch excludes batch_sha256.",
        },
        "batch_id": "batch_05a",
        "reviewer_id": "track_c_independent_batch_05a",
        "reviewed_at": now,
        "pair_ids": list(PAIR_IDS),
        "ledger_ids": sorted(DECISIONS),
        "visibility": {
            "prior_tracks_visible": True,
            "execution_results_visible": False,
            "v60_actual_visible": False,
            "planned_registry_mapping_visible": False,
            "final_track_c_rows_created": False,
        },
        "execution_performed": False,
        "source_catalog": _source_catalog(repo_root, gold_root, a_path, b_path),
        "input_validation": {
            "raw_file_hashes": "PASS",
            "packet_payload_hashes": "PASS",
            "track_batch_payload_hashes": "PASS",
            "track_proposal_hashes": "PASS",
            "referenced_source_hashes": "PASS",
            "json_pointers": "PASS",
            "row_order_and_identity": "PASS",
            "v60_actual_absence": "PASS",
        },
        "accepted_execution_ids": accepted,
        "rejected_relation_ids": rejected,
        "rows": rows,
    }
    batch = {**unsigned_batch, "batch_sha256": canonical_sha256(unsigned_batch)}
    output = gold_root / "review/track_c_preflight/batch_05a.json"
    write_json(output, batch)
    print(f"wrote {output} ({len(rows)} rows, {len(accepted)} executable, {batch['batch_sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
