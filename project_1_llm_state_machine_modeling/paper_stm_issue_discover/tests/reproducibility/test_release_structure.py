"""Provider-free regression tests for the paper1 release boundary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


REPOSITORY = Path(__file__).resolve().parents[4]
SCRIPT = REPOSITORY / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/validate_release_structure.py"


def _module():
    """Load the release validator by path without invoking its CLI."""

    specification = importlib.util.spec_from_file_location("release_structure_validator", SCRIPT)
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def test_release_validator_preserves_frozen_archive_nodes_resources_and_boundaries() -> None:
    """The committed release structure retains frozen bytes and the approved test universe."""

    result = _module().validate(REPOSITORY, REPOSITORY / "venv/bin/python")
    assert result.frozen_archive_files_checked == 2671
    assert result.documented_archive_change_paths == (
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/archive_manifest.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/recomputed_summary.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/provenance_path_mapping.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/publication_manifest.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/archive_manifest.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/archive_manifest.json",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md",
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reviews/01_numeric_recomputation_review.md",
    )
    assert (result.baseline_node_count, result.current_node_count) == (465, 475)
    assert result.resource_hashes["registry"] == "sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca"
    assert result.resource_hashes["judge_protocol"] == "sha256:d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210"
    assert result.boundary_violations == ()
    assert result.provider_call_count == result.billable_call_count == 0


def test_judge_scale_audit_hashes_packaged_neutral_dependencies() -> None:
    """Judge scale auditing uses installed neutral modules rather than the method tree."""

    from paper_stm_judge.scale_audit import _algorithm_source_hash

    digest = _algorithm_source_hash()
    assert digest.startswith("sha256:")
    assert len(digest) == len("sha256:") + 64


def test_release_builder_refuses_to_write_inside_the_source_checkout() -> None:
    """The byte-copy builder never creates a release directory in the repository."""

    builder_path = REPOSITORY / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/build_method_release.py"
    specification = importlib.util.spec_from_file_location("method_release_builder", builder_path)
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)

    with pytest.raises(ValueError, match="outside the source checkout"):
        module._validate_output_path(REPOSITORY, REPOSITORY / "release-output")


def test_judge_release_allowlist_excludes_method_and_evaluation() -> None:
    """The independent Judge release keeps only Judge and neutral utility sources."""

    import json

    allowlist = json.loads(
        (
            REPOSITORY
            / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/release_allowlist.json"
        ).read_text(encoding="utf-8")
    )
    sources = {entry["source"] for entry in allowlist["entries"]}
    assert all(not source.startswith(("method/", "evaluation/")) for source in sources)
    assert "utils/stm_artifacts" in sources


def test_release_manifest_supports_distinct_method_and_judge_namespaces() -> None:
    """The shared byte-copy builder does not label a Judge release as method material."""

    builder_path = REPOSITORY / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/build_method_release.py"
    specification = importlib.util.spec_from_file_location("method_release_schema", builder_path)
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)

    manifest = module.ReleaseManifest(
        schema_version="paper-stm-judge.release-manifest.v1",
        source_commit="a" * 40,
        allowlist_sha256="sha256:" + "b" * 64,
        files=(
            module.ReleaseFile(
                source="judge/src/paper_stm_judge/__init__.py",
                destination="src/paper_stm_judge/__init__.py",
                sha256="sha256:" + "c" * 64,
                byte_count=1,
                purpose="Judge package marker.",
            ),
        ),
        file_count=1,
        total_bytes=1,
        provider_call_count=0,
        billable_call_count=0,
        reason="Provider-free byte copy.",
        basis="Test fixture.",
    )
    assert manifest.schema_version == "paper-stm-judge.release-manifest.v1"


def test_installed_evaluator_can_receive_an_explicit_repository_root(tmp_path: Path) -> None:
    """Archive link validation supports an evaluator installed outside the checkout."""

    from paper_stm_evaluation.final_results_archive import _parser

    archive = tmp_path / "archive"
    repository = tmp_path / "repository"
    args = _parser().parse_args(
        [
            "validate",
            "--archive-root",
            str(archive),
            "--repository-root",
            str(repository),
        ]
    )
    assert args.archive_root == archive
    assert args.repository_root == repository


def test_release_validation_planned_usage_excludes_extra_terminal_predicates() -> None:
    """The fixed 12-predicate denominator cannot be inflated by extra receipts."""

    from paper_stm_evaluation.release_validation import _planned_terminal_distinct_count

    legacy_usage = {
        "planned_predicates": ["S1", "S2", "S3", "S4", "S5", "S6", "G1", "G4", "R1", "R4", "V1", "V4"],
        "terminal_distinct_predicates": ["S1", "S2", "S3", "S4", "S5", "G1", "G4", "R1", "R4", "V4", "R2"],
    }
    assert _planned_terminal_distinct_count(legacy_usage) == 10


def test_release_validation_subset_input_hash_is_canonical() -> None:
    """Subset input contracts use the same stable JSON hash form as the runner."""

    from paper_stm_evaluation.release_validation import _canonical_hash

    assert _canonical_hash({"pair_input_hashes": {"0002": "sha256:b", "0001": "sha256:a"}}) == _canonical_hash(
        {"pair_input_hashes": {"0001": "sha256:a", "0002": "sha256:b"}}
    )
