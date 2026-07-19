from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

from paper_stm_repair_conversion.adapters.plantuml_source import parse_plantuml_source
from paper_stm_repair_representation.plantuml_source_audit import audit_lowered_artifact
from paper_stm_repair_representation.plantuml_source_lowering import (
    lower_plantuml_source,
)
from paper_stm_repair_representation.plantuml_working_bundle import (
    WorkingBundleError,
    load_attribution_safe_working_bundle,
)
from paper_stm_repair_representation.plantuml_working_contract import (
    bind_inspect_diagnostics,
    build_review_obligations,
)
from pyfcstm.diagnostics.inspect import inspect_model
from pyfcstm.model.load import load_state_machine_from_text


SOURCE = """@startuml
[*] --> Locked
state Locked
state Unlocked
state Alarm
Locked --> Unlocked : unlock [pin_ok] / alarm=false
Locked --> Alarm : unlock [pin_ok] / alarm=true
@enduml
"""


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REAL_REPO = _repo_root()
PAPER_REL = Path("project_1_llm_state_machine_modeling/paper_stm_repair")
PAIR_ID = "llms_emp_feedback_final_0000"
FORMAL_EVIDENCE = (
    REAL_REPO / PAPER_REL / "pipeline/representation/reports/llms_emp_r45_java_60"
)


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_text(value: str) -> str:
    return _sha_bytes(value.encode("utf-8"))


def _sha_json(value: object) -> str:
    return _sha_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bundle_fixture(
    tmp_path: Path, *, evidence_eligible: bool = True
) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    evidence = repo / PAPER_REL / "pipeline/representation/reports/fixture"
    schema_dir = repo / PAPER_REL / "pipeline/representation/schemas"
    evaluation_schema_dir = repo / PAPER_REL / "pipeline/evaluation/schemas"
    schema_dir.mkdir(parents=True)
    evaluation_schema_dir.mkdir(parents=True)
    shutil.copy2(
        REAL_REPO
        / PAPER_REL
        / "pipeline/representation/schemas/working_fcstm_contract.schema.json",
        schema_dir / "working_fcstm_contract.schema.json",
    )
    shutil.copy2(
        REAL_REPO
        / PAPER_REL
        / "pipeline/evaluation/schemas/source_issue_ledger.schema.json",
        evaluation_schema_dir / "source_issue_ledger.schema.json",
    )

    nl_text = (
        "Unlocking with the same valid PIN must not both disable and enable the alarm."
    )
    pair_path = repo / PAPER_REL / "corpora/fixture_pairs.jsonl"
    pair_path.parent.mkdir(parents=True)
    pair_row = {
        "pair_id": PAIR_ID,
        "nl_text": nl_text,
        "nl_sha256": _sha_text(nl_text),
        "stm0_text": SOURCE,
        "stm0_sha256": _sha_text(SOURCE),
        "selected_stage": "phase_ii_semantic",
        "selected_stage_cell": "AE2",
    }
    pair_path.write_text(json.dumps(pair_row, sort_keys=True) + "\n", encoding="utf-8")

    canonical = parse_plantuml_source(SOURCE, example_id=PAIR_ID)
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    inspect_report = inspect_model(model).to_json()
    ast_audit = audit_lowered_artifact(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        model=model,
        inspect_report=inspect_report,
    )
    paths = {
        "canonical": evidence / "canonical" / f"{PAIR_ID}.json",
        "fcstm": evidence / "fcstm" / f"{PAIR_ID}.fcstm",
        "inspect": evidence / "parse_inspect" / f"{PAIR_ID}.json",
        "contract": evidence / "working_contracts" / f"{PAIR_ID}.json",
        "trace": evidence / "source_traces" / f"{PAIR_ID}.json",
        "case_report": evidence / "case_reports" / f"{PAIR_ID}.json",
    }
    _write_json(paths["canonical"], canonical)
    paths["fcstm"].parent.mkdir(parents=True)
    paths["fcstm"].write_text(lowered["fcstm"], encoding="utf-8")
    _write_json(paths["inspect"], inspect_report)
    _write_json(paths["trace"], lowered["source_trace_base"])

    contract = bind_inspect_diagnostics(
        fcstm=lowered["fcstm"],
        inspect_report=inspect_report,
        contract=lowered["working_contract"],
    )

    def rel(path: Path) -> str:
        return path.relative_to(repo).as_posix()

    contract["artifact_bindings"] = {
        "canonical_path": rel(paths["canonical"]),
        "fcstm_path": rel(paths["fcstm"]),
        "parse_inspect_path": rel(paths["inspect"]),
        "source_trace_path": rel(paths["trace"]),
        "canonical_file_sha256": _sha_bytes(paths["canonical"].read_bytes()),
        "fcstm_file_sha256": _sha_bytes(paths["fcstm"].read_bytes()),
        "parse_inspect_file_sha256": _sha_bytes(paths["inspect"].read_bytes()),
        "source_trace_file_sha256": _sha_bytes(paths["trace"].read_bytes()),
        "comparison_sha256": _sha_json(lowered["comparison"]),
        "ast_audit_sha256": _sha_json(ast_audit),
    }
    obligations = build_review_obligations(
        comparison=lowered["comparison"],
        official_identity=canonical["metadata"]["official_identity_reconciliation"],
        contract=contract,
    )
    artifact_hashes = contract["artifact_bindings"]
    review_subject_sha256 = _sha_json(
        {
            "nl_sha256": pair_row["nl_sha256"],
            "source_sha256": pair_row["stm0_sha256"],
            **{
                key: artifact_hashes[key]
                for key in (
                    "canonical_file_sha256",
                    "fcstm_file_sha256",
                    "parse_inspect_file_sha256",
                    "source_trace_file_sha256",
                    "comparison_sha256",
                    "ast_audit_sha256",
                )
            },
            "element_set_sha256": contract["inventory_digests"]["element_set_sha256"],
            "macro_set_sha256": contract["inventory_digests"]["macro_set_sha256"],
        }
    )
    contract["review_subject"] = {
        "review_subject_sha256": review_subject_sha256,
        "risk_tags": sorted({item["risk_tag"] for item in obligations}),
        "review_obligations": obligations,
        "second_pass_required": bool(obligations),
    }
    _write_json(paths["contract"], contract)
    case_report = {
        "schema_version": "r4_5.llms_emp_java_case_report.v5",
        "pair_id": PAIR_ID,
        "case_id": "0000",
        "source_sha256": pair_row["stm0_sha256"],
        "canonical_sha256": artifact_hashes["canonical_file_sha256"],
        "fcstm_sha256": artifact_hashes["fcstm_file_sha256"],
        "parse_inspect_sha256": artifact_hashes["parse_inspect_file_sha256"],
        "source_trace_sha256": artifact_hashes["source_trace_file_sha256"],
        "working_contract_sha256": _sha_bytes(paths["contract"].read_bytes()),
        "review_subject_sha256": review_subject_sha256,
        "comparison": lowered["comparison"],
        "ast_audit": ast_audit,
    }
    _write_json(paths["case_report"], case_report)
    comparison_path = evidence / "comparison.jsonl"
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    comparison_path.write_text(
        json.dumps(
            {
                "case_id": "0000",
                "pair_id": PAIR_ID,
                "case_report_sha256": _sha_bytes(paths["case_report"].read_bytes()),
                "working_contract_sha256": _sha_bytes(paths["contract"].read_bytes()),
                "review_subject_sha256": review_subject_sha256,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    artifact_paths = [*paths.values(), comparison_path]
    inventory = [
        {
            "path": path.relative_to(evidence).as_posix(),
            "sha256": _sha_bytes(path.read_bytes()),
        }
        for path in sorted(artifact_paths)
    ]
    manifest = {
        "schema_version": "r4_5.llms_emp_java_batch.v5",
        "evidence_eligible": evidence_eligible,
        "output_dir": rel(evidence),
        "pairs_path": rel(pair_path),
        "pairs_sha256": _sha_bytes(pair_path.read_bytes()),
        "artifact_inventory": inventory,
        "artifact_set_sha256": _sha_json(inventory),
    }
    _write_json(evidence / "manifest.json", manifest)
    return repo, evidence


def _confirmed_ledger(bundle) -> dict:
    transition_ids = [
        item["element_id"]
        for item in bundle.working_contract["elements"]
        if item["origin"] == "source_owned" and item["kind"] == "transition_macro_root"
    ][-2:]
    source_refs = [
        {
            "element_id": element_id,
            "element_type": "transition",
            "reference": element_id,
            "summary": "Conflicting source transition.",
        }
        for element_id in transition_ids
    ]
    source_evidence = [
        {
            "evidence_id": f"SRC{index}",
            "evidence_type": "source_stm_fragment",
            "reference": element_id,
            "summary": "Source transition participating in the conflict.",
        }
        for index, element_id in enumerate(transition_ids, start=1)
    ]
    return {
        "schema_version": "source_issue_ledger.v0",
        "ledger_id": "fixture.bundle.0000",
        "case_id": "0000",
        "source_model_id": PAIR_ID,
        "ledger_scope": "formal_experiment_candidate",
        "nl_reference": {
            "reference_type": "synthetic_inline",
            "reference": "fixture NL",
            "summary": "Fixture requirement.",
        },
        "source_artifact_reference": {
            "reference_type": "synthetic_inline",
            "reference": "fixture PlantUML",
            "summary": "Fixture source state machine.",
        },
        "issues": [
            {
                "issue_id": "ISSUE.INTERNAL.001",
                "issue_level": "confirmed",
                "issue_family": "raw_internal_inconsistency",
                "confirmation_status": "confirmed",
                "confirmation_evidence_path": "raw_internal_inconsistency",
                "candidate_description": "Two source transitions conflict.",
                "source_element_refs": source_refs,
                "nl_evidence": [],
                "source_stm_evidence": source_evidence,
                "behavior_evidence": [
                    {
                        "evidence_id": "BEH1",
                        "evidence_type": "source_internal_consistency_check",
                        "reference": "same state/event/guard, conflicting effect",
                        "summary": "Source-static conflict check.",
                    }
                ],
                "confirmation_rationale": (
                    "The source artifact is internally contradictory; NL evidence is not "
                    "required for this v0 path."
                ),
                "attribution_boundary": {
                    "source_level_claim_allowed": True,
                    "conversion_or_lowering_related": False,
                    "representation_related": False,
                    "rationale": "The conflict is present in the raw PlantUML transitions.",
                },
                "rejection_reason": "",
                "downstream_repair_allowed": True,
                "required_future_trace": True,
                "reviewer_notes": "Fixture confirmed source issue.",
            }
        ],
        "notes": "Attribution-safe working-bundle fixture.",
    }


def test_loader_exposes_only_capability_filtered_source_fields(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    view = bundle.discover_view()

    assert view["pair_id"] == PAIR_ID
    assert view["source_plantuml"] == SOURCE
    assert view["protected_compiler_element_ids"]
    assert view["attribution_rules"]["confirmed_conversion_artifact_limit"] == 0
    assert all(
        item["element_id"].startswith("source:") for item in view["source_facts"]
    )
    assert all(
        set(item["semantic_fields"]).issubset(
            {
                field_ref.split("#field:", 1)[1]
                for field_ref in view["capability_eligibility"][
                    "source_static_discovery"
                ]["eligible_field_refs"]
                if field_ref.startswith(f"{item['element_id']}#field:")
            }
        )
        for item in view["source_facts"]
    )
    detached_contract = bundle.working_contract
    detached_contract["capability_eligibility"]["source_static_discovery"]["status"] = (
        "ineligible"
    )
    assert bundle.discover_view()["source_facts"] == view["source_facts"]
    with pytest.raises(WorkingBundleError, match="cannot authorize Confirm"):
        bundle.validate_confirm_acceptance({})


def test_loader_rejects_development_or_tampered_evidence(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path, evidence_eligible=False)
    with pytest.raises(WorkingBundleError, match="development-only"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)

    repo, evidence = _write_bundle_fixture(tmp_path / "tampered")
    fcstm = evidence / "fcstm" / f"{PAIR_ID}.fcstm"
    fcstm.write_text(fcstm.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(WorkingBundleError, match="artifact hash drift"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_confirmed_issue_binding_requires_positive_source_owned_roots(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    ledger = _confirmed_ledger(bundle)
    bindings = bundle.bind_confirmed_issues(ledger)

    assert len(bindings) == 1
    assert bindings[0].repair_authorized is False
    assert all(item.startswith("source:") for item in bindings[0].source_element_ids)
    assert bindings[0].positive_identity_trace_ids
    assert bindings[0].eligible_field_refs

    compiler_id = next(
        item["element_id"]
        for item in bundle.working_contract["elements"]
        if item["origin"] == "compiler_owned"
    )
    tampered = copy.deepcopy(ledger)
    tampered["issues"][0]["source_element_refs"][0]["element_id"] = compiler_id
    with pytest.raises(WorkingBundleError, match="eligible positive source root"):
        bundle.bind_confirmed_issues(tampered)


def test_confirmed_issue_binding_rejects_conversion_or_ineligible_evidence(
    tmp_path: Path,
):
    repo, evidence = _write_bundle_fixture(tmp_path)
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    ledger = _confirmed_ledger(bundle)
    ledger["issues"][0]["attribution_boundary"]["conversion_or_lowering_related"] = True
    with pytest.raises(WorkingBundleError, match="attribution contract"):
        bundle.bind_confirmed_issues(ledger)

    ledger = _confirmed_ledger(bundle)
    issue = ledger["issues"][0]
    issue["issue_family"] = "guard_condition_mismatch"
    issue["confirmation_evidence_path"] = "nl_grounded_behavioral_issue"
    issue["nl_evidence"] = [
        {
            "evidence_id": "NL1",
            "evidence_type": "nl_requirement",
            "reference": "valid PIN must not enable alarm",
            "summary": "Requirement evidence.",
        }
    ]
    issue["behavior_evidence"] = [
        {
            "evidence_id": "BEH1",
            "evidence_type": "inspect_diagnostic",
            "reference": "inspect:fixture",
            "summary": "Baseline inspect diagnostic is attribution-ineligible.",
        }
    ]
    issue["confirmation_rationale"] = "NL and source appear inconsistent."
    with pytest.raises(WorkingBundleError, match="capability-eligible typed evidence"):
        bundle.bind_confirmed_issues(ledger)


def test_committed_60_cases_are_loadable_only_through_attribution_safe_view():
    manifest = _read_json_fixture(FORMAL_EVIDENCE / "manifest.json")
    if manifest.get("schema_version") != "r4_5.llms_emp_java_batch.v5":
        pytest.skip("formal v5 evidence has not been replayed yet")
    assert manifest["evidence_eligible"] is True

    for index in range(60):
        bundle = load_attribution_safe_working_bundle(
            FORMAL_EVIDENCE,
            f"{index:04d}",
            repo_root=REAL_REPO,
        )
        view = bundle.discover_view()
        assert view["source_facts"]
        assert view["attribution_rules"]["main_result_conversion_artifact_limit"] == 0
        assert (
            view["capability_eligibility"]["repair"]["status"]
            == view["capability_eligibility"]["confirm"]["status"]
            == "not_run"
        )


def _read_json_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
