"""Contract tests for the evaluation-only predicate gold layer."""

from __future__ import annotations

import json
from pathlib import Path

from paper_stm_evaluation.predicate_gold import (
    ExactnessRelation,
    GoldStatus,
    JsonType,
    PredicateGoldDataset,
    SourceRef,
    TypedInput,
    build_inventory,
    canonical_sha256,
    sha256_path,
)
from paper_stm_evaluation.predicate_gold_arbitration import build_arbitration_batch
from paper_stm_evaluation.predicate_gold_assemble import assemble_dataset
from paper_stm_evaluation.predicate_gold_capability import PredicateCapabilityAudit
from paper_stm_evaluation.predicate_gold_composite import (
    CompositeExecutionRequest,
    execute_composite_request,
    replay_composite_request,
)
from paper_stm_evaluation.predicate_gold_docs import (
    DOC_FILENAMES,
    build_bundle,
    load_inputs,
    validate_bundle,
)
from paper_stm_evaluation.predicate_gold_execution import (
    ArtifactRole,
    PredicateExecutionRequest,
    PredicateGoldExecutionReceipt,
    RelationScope,
    execute_request,
    replay_request,
)
from paper_stm_evaluation.predicate_gold_finalize import finalize_batch
from paper_stm_evaluation.predicate_gold_oracle import (
    ArtifactRole as NativeArtifactRole,
)
from paper_stm_evaluation.predicate_gold_oracle import (
    NativeOracleRequest,
)
from paper_stm_evaluation.predicate_gold_oracle import (
    evaluate_request as evaluate_native_oracle_request,
)
from paper_stm_evaluation.predicate_gold_preflight import seal_preflight
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    RelationOracleReceipt,
    RelationOracleRequest,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    execute_request as execute_relation_oracle_request,
)
from paper_stm_evaluation.predicate_gold_relation_oracle import (
    replay_request as replay_relation_oracle_request,
)
from paper_stm_evaluation.predicate_gold_release import (
    ActiveReviewManifest,
    build_active_review_manifest,
    collect_release_paths,
)
from paper_stm_evaluation.predicate_gold_review import build_blind_packets
from paper_stm_evaluation.predicate_gold_static_oracle import (
    ArtifactRole as StaticArtifactRole,
)
from paper_stm_evaluation.predicate_gold_static_oracle import (
    StaticOracleId,
    StaticOracleRequest,
)
from paper_stm_evaluation.predicate_gold_static_oracle import (
    evaluate_request as evaluate_static_oracle_request,
)
from paper_stm_evaluation.predicate_gold_static_oracle import (
    execute_request as execute_static_oracle_request,
)
from paper_stm_evaluation.predicate_gold_static_oracle import (
    replay_request as replay_static_oracle_request,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
PAPER_ROOT = (
    REPO_ROOT / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover"
)


def test_inventory_closes_current_ledger_and_pair_artifacts() -> None:
    """Inventory all 145 ledger rows and 46 source pairs without missing bytes."""

    inventory = build_inventory(
        repo_root=REPO_ROOT,
        paper_root=PAPER_ROOT,
        generated_at="2026-08-31T00:00:00Z",
        source_commit="0" * 40,
    )
    assert inventory.ledger_count == 145
    assert inventory.pair_count == 46
    assert inventory.family_counts == {"DIFF": 8, "EIS": 90, "INS": 35, "VU": 12}
    assert inventory.d_tier_counts == {"D1": 47, "D2": 98}
    assert inventory.l_tier_counts == {"L0": 71, "L1": 35, "L2": 39}
    assert inventory.registry_predicate_count == 19
    assert (
        inventory.coverage_snapshot_status
        == "planned_mapping_not_new_method_measurement"
    )
    assert inventory.missing_paths == ()
    assert inventory.duplicate_ledger_ids == ()
    assert inventory.selected_fcstm_hash_mismatches == ()


def test_schema_describes_every_property_and_model_field() -> None:
    """Require Pydantic descriptions for every object and canonical field."""

    schema = PredicateGoldDataset.model_json_schema()
    assert schema["description"]
    pending = [schema]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            if node.get("type") == "object" or "properties" in node:
                assert node.get("description"), node.get("title")
                for field_name, field_schema in node.get("properties", {}).items():
                    assert field_schema.get("description"), field_name
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)


def test_final_schema_forbids_blocked_execution() -> None:
    """Keep BLOCKED_EXECUTION as a work status but out of final canonical rows."""

    assert GoldStatus.BLOCKED_EXECUTION.value == "BLOCKED_EXECUTION"


def test_method_tree_does_not_reference_gold_directory() -> None:
    """Prevent evaluation gold from entering method imports, prompts, or package data."""

    method_root = PAPER_ROOT / "method"
    forbidden = (
        "predicate_gold_v1",
        "predicate-gold.v1",
        "obligation-equivalent-predicate-gold",
    )
    offenders: list[str] = []
    for path in method_root.rglob("*"):
        if not path.is_file() or path.suffix not in {
            ".py",
            ".json",
            ".md",
            ".toml",
            ".yml",
            ".yaml",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert offenders == []


def test_current_ledger_has_no_embedded_gold_fields() -> None:
    """Keep the immutable ledger separate from the evaluation overlay."""

    ledger_path = PAPER_ROOT / "discover_matrix" / "ledger_v2" / "ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    forbidden = {"gold_property", "typed_inputs", "execution", "positive_control"}
    assert all(not forbidden.intersection(item) for item in ledger["items"].values())


def test_publication_docs_are_mechanical_canonical_views() -> None:
    """Require all human-facing gold files to match the provider-free renderer."""

    gold_root = (
        PAPER_ROOT
        / "discover_matrix"
        / "ledger_v2"
        / "predicate_gold_v1"
    )
    inputs = load_inputs(
        canonical=gold_root / "predicate_gold_v1.json",
        summary=gold_root / "summary.json",
        expected_actual=gold_root / "expected_vs_actual_v60.json",
    )
    bundle = build_bundle(inputs)
    assert tuple(bundle) == DOC_FILENAMES
    validate_bundle(inputs, gold_root)
    unsupported = json.loads(bundle["unsupported_exact.json"])
    assert unsupported["total"] == 98
    assert len({item["ledger_id"] for item in unsupported["items"]}) == 98
    assert all(item["capability_gap"] for item in unsupported["items"])


def test_active_review_manifest_selects_hash_bound_files(tmp_path: Path) -> None:
    """Keep retained failed attempts outside the explicit current review surface."""

    review_root = tmp_path / "review"
    current_paths = [
        review_root / track / "current.json"
        for track in (
            "track_a",
            "track_b",
            "track_c",
            "high_risk",
            "arbitration",
        )
    ]
    historical = review_root / "attempt_01_rejected" / "failed.json"
    for current in current_paths:
        current.parent.mkdir(parents=True)
        current.write_text("{}\n", encoding="utf-8")
    historical.parent.mkdir(parents=True)
    historical.write_text('{"verdict":"FAIL"}\n', encoding="utf-8")
    manifest = build_active_review_manifest(
        review_root=review_root,
        generated_at="2026-08-31T00:00:00Z",
        track_a_paths=[current_paths[0]],
        track_b_paths=[current_paths[1]],
        track_c_paths=[current_paths[2]],
        high_risk_paths=[current_paths[3]],
        arbitration_paths=[current_paths[4]],
        superseded_review_roots=["attempt_01_rejected"],
    )
    assert isinstance(manifest, ActiveReviewManifest)
    assert manifest.track_a[0].repository_path == "track_a/current.json"
    assert manifest.superseded_review_roots == ("attempt_01_rejected",)
    assert all("attempt_01_rejected" not in item.repository_path for item in (
        *manifest.track_a,
        *manifest.track_b,
        *manifest.track_c,
        *manifest.high_risk,
        *manifest.arbitration,
    ))


def test_release_path_collection_uses_canonical_and_active_surfaces() -> None:
    """Collect replayable current artifacts without sweeping rejected attempts."""

    gold_root = (
        PAPER_ROOT
        / "discover_matrix"
        / "ledger_v2"
        / "predicate_gold_v1"
    )
    selected = collect_release_paths(
        repo_root=REPO_ROOT,
        canonical_path=gold_root / "predicate_gold_v1.json",
        review_root=gold_root / "review",
        active_review_manifest_path=gold_root / "review" / "active_review_manifest.json",
        explicit_paths=[gold_root / "summary.json"],
        code_roots=[PAPER_ROOT / "evaluation" / "src" / "paper_stm_evaluation"],
    )
    relative = {path.relative_to(REPO_ROOT).as_posix() for path in selected}
    assert (gold_root / "predicate_gold_v1.json").relative_to(REPO_ROOT).as_posix() in relative
    assert (gold_root / "summary.json").relative_to(REPO_ROOT).as_posix() in relative
    assert any(path.endswith("receipts/EIS-0000-01/defective/request.json") for path in relative)
    assert any(path.endswith("predicate_gold_release.py") for path in relative)
    assert not any("attempt_01_rejected" in path for path in relative)


def test_blind_packets_cover_ledger_without_predicate_leakage() -> None:
    """Cover all ledger IDs while hiding planned, actual, peer, and execution data."""

    packets = build_blind_packets(repo_root=REPO_ROOT, paper_root=PAPER_ROOT)
    ledger_ids = [item.ledger_id for packet in packets for item in packet.ledger_items]
    assert len(packets) == 46
    assert len(ledger_ids) == 145
    assert len(set(ledger_ids)) == 145
    assert all(
        packet.visibility.planned_predicate_mapping_visible is False
        for packet in packets
    )
    assert all(
        packet.visibility.v60_actual_predicate_visible is False for packet in packets
    )
    assert all(
        packet.visibility.other_track_conclusions_visible is False for packet in packets
    )
    assert all(
        packet.visibility.execution_results_visible is False for packet in packets
    )
    payloads = [packet.model_dump(mode="json") for packet in packets]
    assert all("candidate_properties" not in payload for payload in payloads)
    assert all("execution" not in payload for payload in payloads)
    assert all("v60_actual_outputs" not in payload for payload in payloads)


def test_capability_schema_describes_all_fields() -> None:
    """Keep capability rows and findings machine-readable and documented."""

    schema = PredicateCapabilityAudit.model_json_schema()
    assert schema["description"]
    for definition in schema["$defs"].values():
        if "properties" not in definition:
            continue
        assert definition.get("description")
        assert all(
            field.get("description") for field in definition["properties"].values()
        )


def test_evaluation_runner_seals_completed_false_without_method_pipeline(
    tmp_path: Path,
) -> None:
    """Execute one mechanics-only S1 false query and retain a replayable receipt."""

    artifact = (
        PAPER_ROOT
        / "selected_seed_examples"
        / "llms_emp_feedback_final_0000"
        / "model.fcstm"
    )
    source = SourceRef(
        repository_path=artifact.relative_to(REPO_ROOT).as_posix(),
        sha256=sha256_path(artifact),
        json_pointer=None,
        line_start=1,
        line_end=1,
        model_element="llms_emp_feedback_final_0000",
        excerpt="state llms_emp_feedback_final_0000",
    )
    typed_inputs = (
        TypedInput(
            field_name="kind",
            json_type=JsonType.STRING,
            value="state",
            normalized_value="state",
            provenance_kind="FORMAL_SEMANTICS",
            source_ref=source,
            stable_object_id=None,
            alias_resolution=None,
            reason="Mechanics-only test asks for state membership.",
        ),
        TypedInput(
            field_name="element",
            json_type=JsonType.STRING,
            value="NoSuchState",
            normalized_value="NoSuchState",
            provenance_kind="DECLARED_EVALUATION_ASSUMPTION",
            source_ref=source,
            stable_object_id=None,
            alias_resolution=None,
            reason="A deliberately absent identifier exercises the false receipt path; it is not ledger gold.",
        ),
        TypedInput(
            field_name="scope",
            json_type=JsonType.STRING,
            value="closed_fcstm",
            normalized_value="closed_fcstm",
            provenance_kind="FORMAL_SEMANTICS",
            source_ref=source,
            stable_object_id=None,
            alias_resolution=None,
            reason="S1 source implementation accepts the closed native declaration inventory.",
        ),
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.execution-request.v1",
        "request_id": "contract-smoke-s1-false",
        "ledger_id": "TEST-NOT-GOLD",
        "property_id": "mechanics-only-s1",
        "property_proposal_sha256": "sha256:" + "1" * 64,
        "exactness_relation": ExactnessRelation.EQUIVALENT,
        "relation_scope": RelationScope.THIS_PROPERTY,
        "predicate_id": "S1",
        "artifact_role": ArtifactRole.DEFECTIVE,
        "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": ["mechanics-only contract test; not a semantic gold assignment"],
        "expected_boolean_for_acceptance": False,
        "created_at": "2026-08-31T00:00:00Z",
    }
    request = PredicateExecutionRequest(
        **unsigned, request_sha256=canonical_sha256(unsigned)
    )
    receipt = execute_request(
        request=request,
        repo_root=REPO_ROOT,
        receipt_root=tmp_path,
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-smoke",),
    )
    assert receipt.verdict is False
    assert receipt.acceptance_match is True
    assert receipt.state.value == "COMPLETED_BOOLEAN"
    assert (tmp_path / "query.json").is_file()
    assert (tmp_path / "raw_receipt.json").is_file()
    assert (tmp_path / "receipt.json").is_file()
    replay_root = tmp_path / "replay"
    audit = replay_request(
        request=request,
        original_receipt=PredicateGoldExecutionReceipt.model_validate_json(
            (tmp_path / "receipt.json").read_text()
        ),
        original_receipt_path=tmp_path / "receipt.json",
        repo_root=REPO_ROOT,
        replay_root=replay_root,
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-smoke-replay",),
    )
    assert audit.overall_match is True
    assert audit.original_projection_sha256 == audit.replay_projection_sha256


def test_composite_runner_executes_all_constituents_and_replays(tmp_path: Path) -> None:
    """Retain false and true S3/S5 constituents without short-circuiting."""

    artifact = (
        PAPER_ROOT
        / "selected_seed_examples"
        / "llms_emp_feedback_final_0000"
        / "model.fcstm"
    )
    source = SourceRef(
        repository_path=artifact.relative_to(REPO_ROOT).as_posix(),
        sha256=sha256_path(artifact),
        json_pointer=None,
        line_start=19,
        line_end=21,
        model_element="root initial carriers",
        excerpt=None,
    )
    proposal_sha256 = "sha256:" + "3" * 64

    def constituent(
        *,
        request_id: str,
        predicate_id: str,
        transition: str,
        expected: bool,
    ) -> PredicateExecutionRequest:
        value_name = "triggers" if predicate_id == "S3" else "guard"
        value = [] if predicate_id == "S3" else ""
        value_type = JsonType.ARRAY if predicate_id == "S3" else JsonType.STRING
        typed_inputs = (
            TypedInput(
                field_name="transition",
                json_type=JsonType.STRING,
                value=transition,
                normalized_value=transition,
                provenance_kind="AUTHOR_SOURCE",
                source_ref=source,
                stable_object_id=transition,
                alias_resolution=None,
                reason="Exact native carrier used by the mechanics-only composite test.",
            ),
            TypedInput(
                field_name=value_name,
                json_type=value_type,
                value=value,
                normalized_value=value,
                provenance_kind="FORMAL_SEMANTICS",
                source_ref=source,
                stable_object_id=None,
                alias_resolution=None,
                reason="S3 empty trigger set or S5 empty guard is deliberate, not missing.",
            ),
        )
        unsigned = {
            "schema_version": "paper1.predicate-gold.execution-request.v1",
            "request_id": request_id,
            "ledger_id": "TEST-NOT-GOLD",
            "property_id": "mechanics-only-root-initial-composite",
            "property_proposal_sha256": proposal_sha256,
            "exactness_relation": ExactnessRelation.EQUIVALENT,
            "relation_scope": RelationScope.PARENT_COMPOSITE,
            "predicate_id": predicate_id,
            "artifact_role": ArtifactRole.DEFECTIVE,
            "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
            "assumptions": [
                "mechanics-only composite test; not a semantic gold assignment"
            ],
            "expected_boolean_for_acceptance": expected,
            "created_at": "2026-08-31T00:00:00Z",
        }
        return PredicateExecutionRequest(
            **unsigned, request_sha256=canonical_sha256(unsigned)
        )

    constituents = (
        constituent(
            request_id="line19-s3",
            predicate_id="S3",
            transition="transition:line:19",
            expected=False,
        ),
        constituent(
            request_id="line19-s5",
            predicate_id="S5",
            transition="transition:line:19",
            expected=True,
        ),
        constituent(
            request_id="line21-s3",
            predicate_id="S3",
            transition="transition:line:21",
            expected=False,
        ),
        constituent(
            request_id="line21-s5",
            predicate_id="S5",
            transition="transition:line:21",
            expected=True,
        ),
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.composite-request.v1",
        "request_id": "contract-smoke-root-initial-composite",
        "ledger_id": "TEST-NOT-GOLD",
        "property_id": "mechanics-only-root-initial-composite",
        "property_proposal_sha256": proposal_sha256,
        "exactness_relation": ExactnessRelation.EQUIVALENT,
        "operator": "AND",
        "no_short_circuit": True,
        "artifact_role": ArtifactRole.DEFECTIVE,
        "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "constituents": [item.model_dump(mode="json") for item in constituents],
        "assumptions": [
            "The two line-bound carriers form the complete mechanics-only test inventory."
        ],
        "expected_boolean_for_acceptance": False,
        "created_at": "2026-08-31T00:00:00Z",
    }
    request = CompositeExecutionRequest(
        **unsigned, request_sha256=canonical_sha256(unsigned)
    )
    original_root = tmp_path / "original"
    receipt = execute_composite_request(
        request=request,
        repo_root=REPO_ROOT,
        receipt_root=original_root,
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-smoke-composite",),
    )
    assert receipt.verdict is False
    assert receipt.acceptance_match is True
    assert [item.verdict for item in receipt.constituents] == [False, True, False, True]
    assert all(item.acceptance_match for item in receipt.constituents)
    assert len(list((original_root / "constituents").glob("*/receipt.json"))) == 4

    replay_root = tmp_path / "replay"
    audit = replay_composite_request(
        request=request,
        original_receipt=receipt,
        original_receipt_path=original_root / "receipt.json",
        repo_root=REPO_ROOT,
        replay_root=replay_root,
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-smoke-composite-replay",),
    )
    assert audit.overall_match is True
    assert all(item.match for item in audit.constituents)


def test_unary_not_composite_inverts_s1_and_replays(tmp_path: Path) -> None:
    """Keep child and parent truth visible for a unary NOT source-static proxy."""

    defective = (
        PAPER_ROOT
        / "selected_seed_examples"
        / "llms_emp_feedback_final_0004"
        / "model.fcstm"
    )
    control = (
        PAPER_ROOT
        / "discover_matrix"
        / "ledger_v2"
        / "predicate_gold_v1"
        / "controls"
        / "EIS-0004-01"
        / "minimal_repair.fcstm"
    )
    source = SourceRef(
        repository_path=defective.relative_to(REPO_ROOT).as_posix(),
        sha256=sha256_path(defective),
        json_pointer=None,
        line_start=8,
        line_end=10,
        model_element="InvalidInitialtr_0002",
        excerpt=None,
    )
    typed_inputs = (
        TypedInput(
            field_name="kind",
            json_type=JsonType.STRING,
            value="state",
            normalized_value="state",
            provenance_kind="FORMAL_SEMANTICS",
            source_ref=source,
            stable_object_id=None,
            alias_resolution=None,
            reason="S1 checks the native state declaration inventory.",
        ),
        TypedInput(
            field_name="element",
            json_type=JsonType.STRING,
            value="InvalidInitialtr_0002",
            normalized_value="InvalidInitialtr_0002",
            provenance_kind="DECLARED_EVALUATION_ASSUMPTION",
            source_ref=source,
            stable_object_id="InvalidInitialtr_0002",
            alias_resolution=None,
            reason="Exact packet-attributed sentinel identity; no fuzzy matching.",
        ),
        TypedInput(
            field_name="scope",
            json_type=JsonType.STRING,
            value="closed_fcstm",
            normalized_value="closed_fcstm",
            provenance_kind="FORMAL_SEMANTICS",
            source_ref=source,
            stable_object_id=None,
            alias_resolution=None,
            reason="S1's complete native declaration scope.",
        ),
    )
    proposal_sha256 = "sha256:" + "4" * 64

    def parent_request(
        *,
        artifact: Path,
        role: ArtifactRole,
        child_expected: bool,
        parent_expected: bool,
    ) -> CompositeExecutionRequest:
        child_unsigned = {
            "schema_version": "paper1.predicate-gold.execution-request.v1",
            "request_id": f"not-s1-{role.value.lower()}-child",
            "ledger_id": "TEST-NOT-GOLD",
            "property_id": "mechanics-only-not-s1",
            "property_proposal_sha256": proposal_sha256,
            "exactness_relation": ExactnessRelation.O_IMPLIES_P,
            "relation_scope": RelationScope.PARENT_COMPOSITE,
            "predicate_id": "S1",
            "artifact_role": role,
            "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
            "assumptions": ["mechanics-only unary NOT contract test"],
            "expected_boolean_for_acceptance": child_expected,
            "created_at": "2026-08-31T00:00:00Z",
        }
        child = PredicateExecutionRequest(
            **child_unsigned, request_sha256=canonical_sha256(child_unsigned)
        )
        parent_unsigned = {
            "schema_version": "paper1.predicate-gold.composite-request.v1",
            "request_id": f"not-s1-{role.value.lower()}-parent",
            "ledger_id": "TEST-NOT-GOLD",
            "property_id": "mechanics-only-not-s1",
            "property_proposal_sha256": proposal_sha256,
            "exactness_relation": ExactnessRelation.O_IMPLIES_P,
            "operator": "NOT",
            "no_short_circuit": True,
            "artifact_role": role,
            "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "constituents": [child.model_dump(mode="json")],
            "assumptions": ["NOT contains exactly one fully receipted S1 child"],
            "expected_boolean_for_acceptance": parent_expected,
            "created_at": "2026-08-31T00:00:00Z",
        }
        return CompositeExecutionRequest(
            **parent_unsigned, request_sha256=canonical_sha256(parent_unsigned)
        )

    for label, request, parent_expected, child_expected in (
        (
            "defective",
            parent_request(
                artifact=defective,
                role=ArtifactRole.DEFECTIVE,
                child_expected=True,
                parent_expected=False,
            ),
            False,
            True,
        ),
        (
            "control",
            parent_request(
                artifact=control,
                role=ArtifactRole.POSITIVE_CONTROL,
                child_expected=False,
                parent_expected=True,
            ),
            True,
            False,
        ),
    ):
        original_root = tmp_path / label
        receipt = execute_composite_request(
            request=request,
            repo_root=REPO_ROOT,
            receipt_root=original_root,
            source_commit="0" * 40,
            pyfcstm_commit="1" * 40,
            command=("contract-smoke-not",),
        )
        assert receipt.verdict is parent_expected
        assert receipt.constituents[0].verdict is child_expected
        assert receipt.acceptance_match is True
        assert "logical negation" in receipt.reason
        assert "unary NOT truth function" in receipt.basis
        audit = replay_composite_request(
            request=request,
            original_receipt=receipt,
            original_receipt_path=original_root / "receipt.json",
            repo_root=REPO_ROOT,
            replay_root=original_root / "replay",
            source_commit="0" * 40,
            pyfcstm_commit="1" * 40,
            command=("contract-smoke-not-replay",),
        )
        assert audit.overall_match is True


def test_preflight_seal_correction_changes_only_digest_fields(tmp_path: Path) -> None:
    """Preserve review content while repairing row and batch canonical digests."""

    source = tmp_path / "submitted.json"
    output = tmp_path / "corrected.json"
    log_path = tmp_path / "correction.json"
    source.write_text(
        json.dumps(
            {
                "schema_version": "test.preflight.v1",
                "batch_id": "batch_test",
                "rows": [
                    {
                        "ledger_id": "EIS-TEST-01",
                        "decision": "UNSUPPORTED_EXACT",
                        "row_sha256": "sha256:" + "0" * 64,
                    }
                ],
                "batch_sha256": "sha256:" + "0" * 64,
            }
        ),
        encoding="utf-8",
    )
    log = seal_preflight(
        source_path=source, output_path=output, correction_log_path=log_path
    )
    submitted = json.loads(source.read_text(encoding="utf-8"))
    corrected = json.loads(output.read_text(encoding="utf-8"))
    assert submitted["rows"][0]["decision"] == corrected["rows"][0]["decision"]
    assert submitted["rows"][0]["row_sha256"] != corrected["rows"][0]["row_sha256"]
    assert submitted["batch_sha256"] != corrected["batch_sha256"]
    assert log["semantic_fields_changed"] is False


def test_native_initial_transition_oracle_uses_pyfcstm_objects_and_does_not_short_circuit() -> (
    None
):
    """Evaluate every initial-transition contract constituent after a cardinality failure."""

    artifact = (
        PAPER_ROOT
        / "selected_seed_examples"
        / "llms_emp_feedback_final_0000"
        / "model.fcstm"
    )
    source = SourceRef(
        repository_path=artifact.relative_to(REPO_ROOT).as_posix(),
        sha256=sha256_path(artifact),
        json_pointer=None,
        line_start=1,
        line_end=21,
        model_element="llms_emp_feedback_final_0000",
        excerpt=None,
    )
    values = {
        "owner_path": (["llms_emp_feedback_final_0000"], JsonType.ARRAY),
        "cardinality": ("EXACTLY_ONE", JsonType.STRING),
        "required_target_path": (
            ["llms_emp_feedback_final_0000", "HumanDrivingMode"],
            JsonType.ARRAY,
        ),
        "require_no_event": (True, JsonType.BOOLEAN),
        "require_no_guard": (True, JsonType.BOOLEAN),
    }
    typed_inputs = tuple(
        TypedInput(
            field_name=name,
            json_type=json_type,
            value=value,
            normalized_value=value,
            provenance_kind="AUTHOR_SOURCE"
            if name in {"owner_path", "required_target_path"}
            else "FORMAL_SEMANTICS",
            source_ref=source,
            stable_object_id="state:llms_emp_feedback_final_0000:line:2"
            if name == "owner_path"
            else None,
            alias_resolution=None,
            reason="Mechanics-only test binding for the native initial-transition contract.",
        )
        for name, (value, json_type) in values.items()
    )
    unsigned = {
        "schema_version": "paper1.predicate-gold.native-oracle-request.v1",
        "request_id": "contract-smoke-native-initial-false",
        "ledger_id": "TEST-NOT-GOLD",
        "property_id": "mechanics-only-native-initial",
        "property_proposal_sha256": "sha256:" + "2" * 64,
        "exactness_relation": ExactnessRelation.EQUIVALENT,
        "oracle_id": "NATIVE_INITIAL_TRANSITION_CONTRACT",
        "artifact_role": NativeArtifactRole.DEFECTIVE,
        "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
        "artifact_sha256": sha256_path(artifact),
        "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
        "assumptions": ["mechanics-only contract test; not a ledger-gold assignment"],
        "expected_boolean_for_acceptance": False,
        "created_at": "2026-08-31T00:00:00Z",
    }
    request = NativeOracleRequest(**unsigned, request_sha256=canonical_sha256(unsigned))
    owner_path, transitions, constituents = evaluate_native_oracle_request(
        request, repo_root=REPO_ROOT
    )
    assert owner_path == ("llms_emp_feedback_final_0000",)
    assert len(transitions) == 2
    assert [item.constituent_id for item in constituents] == [
        "cardinality",
        "target",
        "event",
        "guard",
    ]
    assert [item.verdict for item in constituents] == [False, False, False, True]


def test_source_static_proxy_oracles_false_true_and_replay(tmp_path: Path) -> None:
    """Run both pilot proxies on defective and independently repaired artifacts."""

    original = (
        PAPER_ROOT
        / "selected_seed_examples"
        / "llms_emp_feedback_final_0000"
        / "model.fcstm"
    )
    controls = (
        PAPER_ROOT / "discover_matrix" / "ledger_v2" / "predicate_gold_v1" / "controls"
    )
    cases = (
        (
            "EIS-0000-01",
            StaticOracleId.RUNNING_EVENT_ROOT_EXIT_CONSUMERS,
            {
                "event_path": "llms_emp_feedback_final_0000.Power_Off",
                "required_running_leaf_paths": [
                    "llms_emp_feedback_final_0000.HumanDrivingMode",
                    "llms_emp_feedback_final_0000.AutonomousMode.AutoNavigating",
                    "llms_emp_feedback_final_0000.AutonomousMode.AutoFinal",
                ],
                "required_exit_target": "[*]",
            },
            controls / "EIS-0000-01" / "minimal_repair.fcstm",
        ),
        (
            "EIS-0000-02",
            StaticOracleId.SEPARATED_CONDITION_TAKEOVER_CONSUMERS,
            {
                "required_event_tokens": ["Human_Steering_Cmd", "Brake_Pressed"],
                "state_condition": "llms_emp_feedback_final_0000.AutonomousMode.AutoFinal",
                "response_state": "llms_emp_feedback_final_0000.HumanDrivingMode",
            },
            controls / "EIS-0000-02" / "minimal_repair.fcstm",
        ),
    )

    def request_for(
        *,
        ledger_id: str,
        oracle_id: StaticOracleId,
        values: dict[str, object],
        artifact: Path,
        role: StaticArtifactRole,
    ) -> StaticOracleRequest:
        source = SourceRef(
            repository_path=artifact.relative_to(REPO_ROOT).as_posix(),
            sha256=sha256_path(artifact),
            json_pointer=None,
            line_start=1,
            line_end=len(artifact.read_text(encoding="utf-8").splitlines()),
            model_element=artifact.stem,
            excerpt=None,
        )
        typed_inputs = tuple(
            TypedInput(
                field_name=name,
                json_type=JsonType.ARRAY
                if isinstance(value, list)
                else JsonType.STRING,
                value=value,
                normalized_value=value,
                provenance_kind="DECLARED_EVALUATION_ASSUMPTION",
                source_ref=source,
                stable_object_id=None,
                alias_resolution=None,
                reason="Mechanics-only regression input mirrors the frozen pilot oracle contract.",
            )
            for name, value in values.items()
        )
        unsigned = {
            "schema_version": "paper1.predicate-gold.static-oracle-request.v1",
            "request_id": f"contract-{ledger_id.lower()}-{role.value.lower()}",
            "ledger_id": ledger_id,
            "property_id": f"contract-{oracle_id.value.lower()}",
            "property_proposal_sha256": "sha256:" + "4" * 64,
            "exactness_relation": ExactnessRelation.O_IMPLIES_P,
            "oracle_id": oracle_id,
            "artifact_role": role,
            "artifact_path": artifact.relative_to(REPO_ROOT).as_posix(),
            "artifact_sha256": sha256_path(artifact),
            "typed_inputs": [item.model_dump(mode="json") for item in typed_inputs],
            "assumptions": ["mechanics-only source-static proxy regression"],
            "expected_boolean_for_acceptance": role
            == StaticArtifactRole.POSITIVE_CONTROL,
            "created_at": "2026-08-31T00:00:00Z",
        }
        return StaticOracleRequest(
            **unsigned, request_sha256=canonical_sha256(unsigned)
        )

    for ledger_id, oracle_id, values, control in cases:
        defective_request = request_for(
            ledger_id=ledger_id,
            oracle_id=oracle_id,
            values=values,
            artifact=original,
            role=StaticArtifactRole.DEFECTIVE,
        )
        control_request = request_for(
            ledger_id=ledger_id,
            oracle_id=oracle_id,
            values=values,
            artifact=control,
            role=StaticArtifactRole.POSITIVE_CONTROL,
        )
        _, defective_constituents = evaluate_static_oracle_request(
            defective_request, repo_root=REPO_ROOT
        )
        _, control_constituents = evaluate_static_oracle_request(
            control_request, repo_root=REPO_ROOT
        )
        assert all(item.verdict for item in defective_constituents) is False
        assert all(item.verdict for item in control_constituents) is True

    first_id, first_oracle, first_values, _ = cases[0]
    replay_request = request_for(
        ledger_id=first_id,
        oracle_id=first_oracle,
        values=first_values,
        artifact=original,
        role=StaticArtifactRole.DEFECTIVE,
    )
    original_root = tmp_path / "static-original"
    receipt = execute_static_oracle_request(
        replay_request,
        repo_root=REPO_ROOT,
        receipt_root=original_root,
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-static",),
    )
    audit = replay_static_oracle_request(
        replay_request,
        original_receipt=receipt,
        original_receipt_path=original_root / "receipt.json",
        repo_root=REPO_ROOT,
        replay_root=tmp_path / "static-replay",
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
        command=("contract-static-replay",),
    )
    assert receipt.verdict is False
    assert audit.overall_match is True


def test_batch_02_relation_oracles_false_true_and_replay(tmp_path: Path) -> None:
    """Re-execute every batch-02 native relation property on both artifact roles."""

    gold_root = PAPER_ROOT / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    ledger_ids = (
        "EIS-0009-01",
        "EIS-0009-02",
        "EIS-0009-03",
        "EIS-0010-02",
        "EIS-0010-05",
        "VU-0010-01",
    )
    for ledger_id in ledger_ids:
        for role, expected in (("defective", False), ("positive_control", True)):
            request_path = gold_root / "receipts" / ledger_id / role / "request.json"
            request = RelationOracleRequest.model_validate_json(
                request_path.read_text(encoding="utf-8")
            )
            receipt_root = tmp_path / ledger_id / role
            receipt = execute_relation_oracle_request(
                request,
                repo_root=REPO_ROOT,
                receipt_root=receipt_root,
                source_commit="0" * 40,
                pyfcstm_commit="1" * 40,
                command=("contract-smoke-relation",),
            )
            assert receipt.state == "COMPLETED_BOOLEAN"
            assert receipt.verdict is expected
            assert receipt.acceptance_match is True
            audit = replay_relation_oracle_request(
                request,
                original_receipt=RelationOracleReceipt.model_validate_json(
                    (receipt_root / "receipt.json").read_text(encoding="utf-8")
                ),
                original_receipt_path=receipt_root / "receipt.json",
                repo_root=REPO_ROOT,
                replay_root=receipt_root / "replay",
                source_commit="0" * 40,
                pyfcstm_commit="1" * 40,
                command=("contract-smoke-relation-replay",),
            )
            assert audit.overall_match is True


def test_batch_02_receipt_manifest_closes_pre_registered_polarity() -> None:
    """Require every batch-02 executed row to retain false/true/replay closure."""

    gold_root = PAPER_ROOT / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    manifest = json.loads(
        (gold_root / "receipts" / "batch_02a_request_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(manifest["rows"]) == 9
    assert {row["final_pre_execution_relation"] for row in manifest["rows"]} == {
        "EQUIVALENT",
        "O_IMPLIES_P",
    }
    for row in manifest["rows"]:
        assert len(row["roles"]) == 2
        for role in row["roles"]:
            request_path = gold_root / role["request_path"]
            assert sha256_path(request_path) == role["request_file_sha256"]
            receipt = json.loads(
                (request_path.parent / "receipt.json").read_text(encoding="utf-8")
            )
            replay = json.loads(
                (request_path.parent / "replay" / "replay_audit.json").read_text(
                    encoding="utf-8"
                )
            )
            expected = receipt["artifact_role"] == "POSITIVE_CONTROL"
            assert receipt["state"] == "COMPLETED_BOOLEAN"
            assert receipt["verdict"] is expected
            assert receipt["acceptance_match"] is True
            assert replay["overall_match"] is True


def test_generic_arbitration_and_assembler_close_pilot(tmp_path: Path) -> None:
    """Project selected pilot A/B/C evidence without issue-specific build code."""

    gold_root = PAPER_ROOT / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    review_root = gold_root / "review"
    a_paths = [
        review_root / "pilot_independent" / "track_a_pair_0000.json",
        review_root / "track_a_independent" / "batch_01a.json",
        review_root / "track_a_independent" / "batch_02a.json",
        review_root / "track_a_independent" / "batch_04a.json",
    ]
    b_paths = [
        review_root / "pilot_independent" / "track_b_pair_0000.json",
        review_root / "track_b_independent" / "batch_01a.json",
        review_root / "track_b_independent" / "batch_02a.json",
        review_root / "track_b_independent" / "batch_04a.json",
    ]
    c_paths = [
        review_root / "track_c_independent" / "pilot_pair_0000_portable.json",
        review_root / "track_c_independent" / "batch_01a_portable.json",
        review_root / "track_c_independent" / "batch_02a_portable.json",
        review_root / "track_c_independent" / "batch_04a_portable.json",
    ]
    high_risk_paths = [
        review_root / "high_risk_independent" / "pilot_batch_01a_02a.json",
        review_root / "high_risk_independent" / "batch_04a.json",
    ]
    arbitration_paths = [
        review_root / "arbitration_drafts" / "pilot_batch_01a_02a.json",
        review_root / "arbitration_drafts" / "batch_04a.json",
    ]
    draft = build_arbitration_batch(
        repo_root=REPO_ROOT,
        gold_root=gold_root,
        batch_id="contract-pilot-arbitration",
        a_paths=a_paths,
        b_paths=b_paths,
        c_paths=c_paths,
        high_risk_paths=high_risk_paths,
        arbitrated_at="2026-08-31T00:00:00Z",
    )
    assert len(draft.rows) == 56
    assert all(row.arbitration.adjudicator_id == "pane5:manual-supervised-adjudicator" for row in draft.rows)

    manifest = build_active_review_manifest(
        review_root=review_root,
        generated_at="2026-08-31T00:00:00Z",
        track_a_paths=a_paths,
        track_b_paths=b_paths,
        track_c_paths=c_paths,
        high_risk_paths=high_risk_paths,
        arbitration_paths=arbitration_paths,
        superseded_review_roots=[],
    )
    manifest_path = tmp_path / "active_review_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    dataset = assemble_dataset(
        repo_root=REPO_ROOT,
        gold_root=gold_root,
        review_root=review_root,
        active_manifest_path=manifest_path,
        generated_at="2026-08-31T00:00:00Z",
        source_commit="0" * 40,
        pyfcstm_commit="1" * 40,
    )
    assert len(dataset.items) == 56
    assert dataset.items["INS-0000-04"].gold_status == GoldStatus.COMPOSITE_EXACT_FALSE
    assert dataset.items["INS-0000-04"].execution is not None
    assert dataset.items["INS-0000-04"].execution.verdict is False
    assert dataset.items["INS-0000-04"].positive_control is not None
    assert dataset.items["INS-0000-04"].positive_control.verdict is True
    assert dataset.items["DIFF-0019-05"].gold_status == GoldStatus.COMPOSITE_EXACT_FALSE
    assert dataset.items["DIFF-0019-05"].gold_property is not None
    assert dataset.items["DIFF-0019-05"].gold_property.property_id == "DIFF-0019-05-B-P3"


def test_pane5_finalizer_closes_fourth_review_disagreements() -> None:
    """Require explicit source-based overrides for every fourth-review split."""

    gold_root = PAPER_ROOT / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    review_root = gold_root / "review"
    final = finalize_batch(
        draft_path=review_root / "arbitration_drafts" / "pilot_batch_01a_02a.json",
        track_c_paths=[
            review_root / "track_c_independent" / "pilot_pair_0000_portable.json",
            review_root / "track_c_independent" / "batch_01a_portable.json",
            review_root / "track_c_independent" / "batch_02a_portable.json",
        ],
        high_risk_paths=[
            review_root / "high_risk_independent" / "pilot_batch_01a_02a.json"
        ],
        arbitrated_at="2026-08-31T11:00:00Z",
    )
    rows = {row.ledger_id: row for row in final.rows}
    assert len(rows) == 34
    assert rows["EIS-0007-01"].arbitration.final_status == GoldStatus.UNSUPPORTED_EXACT
    assert rows["EIS-0007-01"].arbitration.final_exactness_relation.value == "UNRELATED"
    assert rows["VU-0009-01"].arbitration.final_status == GoldStatus.UNSUPPORTED_EXACT
    assert all("Pane5 draft" not in row.arbitration.reason for row in final.rows)
