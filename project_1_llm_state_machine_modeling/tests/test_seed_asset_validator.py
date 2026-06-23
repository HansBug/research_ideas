from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_LIBRARY = REPO_ROOT / "project_1_llm_state_machine_modeling" / "paper_stm_repair" / "corpora" / "seed_library"
VALIDATOR = SEED_LIBRARY / "tools" / "validate_seed_assets.py"
UNIFIED = "unified-uml-multimodal-validation"
SEFM = "sefm-llm-state-machine"
LLMS_EMP = "llms-emp-stm-subset"
TTOOL_AI = "ttool-ai-smd-subset"


def _copy_seed_library_subset(tmp_path: Path, *seed_ids: str) -> Path:
    base = tmp_path / "seed_library"
    base.mkdir()
    # REGISTRY.md is the human-facing decision table.  Copy it into fixture
    # bases so validator tests also exercise markdown/JSON count consistency.
    shutil.copy2(SEED_LIBRARY / "REGISTRY.md", base / "REGISTRY.md")
    shutil.copytree(SEED_LIBRARY / "schemas", base / "schemas")
    for seed_id in seed_ids or (UNIFIED,):
        shutil.copytree(SEED_LIBRARY / seed_id, base / seed_id)
    return base


def test_seed_asset_validator_accepts_unmodified_unified_trace(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload == {
        "seed_id": UNIFIED,
        "pair_count": 999,
        "trace_verified_pair_count": 999,
        "eligible_generated_pair_count": 989,
    }


def test_seed_asset_validator_rejects_tampered_extracted_nl(tmp_path: Path) -> None:
    """A trace-verified pair must round-trip to committed raw, not only self-report hashes."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    pairs_path = base / UNIFIED / "assets" / "extracted" / "pairs.jsonl"
    rows = [json.loads(line) for line in pairs_path.read_text().splitlines() if line.strip()]
    rows[0]["nl_text"] = "BROKEN_TEXT_NOT_FROM_PARQUET"
    rows[0]["nl_sha256"] = "0" * 64
    pairs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "nl_text does not match raw parquet" in result.stderr
    assert "nl_sha256 mismatch" in result.stderr


def test_seed_asset_validator_rejects_tampered_validation_summary_counts(tmp_path: Path) -> None:
    """validation_summary.json must be derived from raw/pairs evidence, not trusted."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    summary_path = base / UNIFIED / "assets" / "extracted" / "validation_summary.json"
    summary = json.loads(summary_path.read_text())
    summary["raw_asset_count"] = 999
    summary["pair_count"] = 12345
    summary["hash_match_count"] = 12345
    summary["locator_resolved_count"] = 12345
    summary["text_or_hash_match_count"] = 12345
    summary["repo_or_external_reproducible_eligible_count"] = 12345
    summary["local_only_trace_count"] = 999
    summary["metadata_only_trace_count"] = 999
    summary["failed_pair_ids"] = ["fake_failure"]
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "validation_summary raw_asset_count mismatch" in result.stderr
    assert "validation_summary pair_count mismatch" in result.stderr
    assert "validation_summary hash_match_count mismatch" in result.stderr
    assert "validation_summary locator_resolved_count mismatch" in result.stderr
    assert "validation_summary text_or_hash_match_count mismatch" in result.stderr
    assert "validation_summary repo_or_external_reproducible_eligible_count mismatch" in result.stderr
    assert "validation_summary local_only_trace_count mismatch" in result.stderr
    assert "validation_summary metadata_only_trace_count mismatch" in result.stderr
    assert "validation_summary failed_pair_ids mismatch" in result.stderr


def test_seed_asset_validator_rejects_tampered_excluded_pair_ids(tmp_path: Path) -> None:
    """Excluded failure rows must stay auditable rather than disappearing from summaries."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    summary_path = base / UNIFIED / "assets" / "extracted" / "validation_summary.json"
    summary = json.loads(summary_path.read_text())
    summary["excluded_pair_ids"] = []
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "validation_summary excluded_pair_ids mismatch" in result.stderr


def test_seed_asset_validator_accepts_unmodified_llms_emp_xlsx_trace(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path, LLMS_EMP)
    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), LLMS_EMP],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload == {
        "seed_id": LLMS_EMP,
        "pair_count": 60,
        "trace_verified_pair_count": 60,
        "eligible_generated_pair_count": 60,
    }


def test_seed_asset_validator_rejects_tampered_llms_emp_metadata(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path, LLMS_EMP)
    pairs_path = base / LLMS_EMP / "assets" / "extracted" / "pairs.jsonl"
    rows = [json.loads(line) for line in pairs_path.read_text().splitlines() if line.strip()]
    rows[0]["llm"] = "BROKEN_LLM"
    rows[0]["model_source"] = "BROKEN_SOURCE"
    rows[0]["model_name"] = "BROKEN_NAME"
    rows[0]["reference_plantuml_sha256"] = "0" * 64
    pairs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), LLMS_EMP],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "llm does not match raw XLSX row" in result.stderr
    assert "model_source does not match raw XLSX row" in result.stderr
    assert "model_name does not match raw XLSX row" in result.stderr
    assert "reference_plantuml_sha256 mismatch" in result.stderr


def test_seed_asset_validator_rejects_tampered_llms_emp_xlsx_locator(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path, LLMS_EMP)
    pairs_path = base / LLMS_EMP / "assets" / "extracted" / "pairs.jsonl"
    rows = [json.loads(line) for line in pairs_path.read_text().splitlines() if line.strip()]
    rows[0]["source_locator"] = rows[0]["source_locator"].replace("row=0", "row=9999")
    pairs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), LLMS_EMP],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "XLSX row out of range" in result.stderr
    assert "claims trace_verified but raw trace validation failed" in result.stderr


def test_seed_asset_validator_accepts_unmodified_sefm_zip_trace(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path, SEFM)
    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload == {
        "seed_id": SEFM,
        "pair_count": 1,
        "trace_verified_pair_count": 1,
        "eligible_generated_pair_count": 1,
    }


def test_seed_asset_validator_rejects_tampered_sefm_locator(tmp_path: Path) -> None:
    """A ZIP-based pair must resolve the exact Python symbol and generated text member."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    pairs_path = base / SEFM / "assets" / "extracted" / "pairs.jsonl"
    row = json.loads(pairs_path.read_text().strip())
    row["source_locator"] = row["source_locator"].replace("SSC7_fall_2024", "MISSING_SYMBOL")
    pairs_path.write_text(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "cannot resolve ZIP locator" in result.stderr
    assert "claims trace_verified but raw trace validation failed" in result.stderr


def test_seed_asset_validator_accepts_unmodified_ttool_zip_member_pair_trace(tmp_path: Path) -> None:
    """TTool-AI conditional pairs must round-trip to explicit ZIP members."""

    base = _copy_seed_library_subset(tmp_path, TTOOL_AI)
    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), TTOOL_AI],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload == {
        "seed_id": TTOOL_AI,
        "pair_count": 6,
        "trace_verified_pair_count": 6,
        "eligible_generated_pair_count": 6,
    }


def test_seed_asset_validator_rejects_tampered_ttool_zip_member_locator(tmp_path: Path) -> None:
    """A ZIP member-pair row must resolve both NL and generated XML members."""

    base = _copy_seed_library_subset(tmp_path, TTOOL_AI)
    pairs_path = base / TTOOL_AI / "assets" / "extracted" / "pairs.jsonl"
    rows = [json.loads(line) for line in pairs_path.read_text().splitlines() if line.strip()]
    rows[0]["source_locator"] = rows[0]["source_locator"].replace("automatedbraking.md", "missing.md")
    pairs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), TTOOL_AI],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "cannot resolve ZIP member-pair locator" in result.stderr
    assert "claims trace_verified but raw trace validation failed" in result.stderr


def test_seed_asset_validator_rejects_pair_state_drift_from_registry(tmp_path: Path) -> None:
    """Eligible generated rows must not silently keep stale conditional state."""

    base = _copy_seed_library_subset(tmp_path, LLMS_EMP)
    pairs_path = base / LLMS_EMP / "assets" / "extracted" / "pairs.jsonl"
    rows = [json.loads(line) for line in pairs_path.read_text().splitlines() if line.strip()]
    rows[0]["eligibility_state"] = "conditional_final_pool"
    pairs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), LLMS_EMP],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "eligibility_state mismatch with pair set" in result.stderr


def test_seed_asset_validator_rejects_exclusion_reason_on_eligible_row(tmp_path: Path) -> None:
    """Non-blocking caveats belong in registry/docs, not eligible row exclusion_reason."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    pairs_path = base / SEFM / "assets" / "extracted" / "pairs.jsonl"
    row = json.loads(pairs_path.read_text().strip())
    row["exclusion_reason"] = "stale_license_blocker"
    pairs_path.write_text(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "eligible generated row must not carry exclusion_reason" in result.stderr


def test_seed_asset_validator_allows_unknown_redistribution_for_trace_ready_public_assets(tmp_path: Path) -> None:
    """Redistribution/license notes are not final_pool_ready blockers once trace evidence is complete."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    registry_path = base / SEFM / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    registry["asset_summary"]["redistribution_status"] = "unknown"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_seed_asset_validator_rejects_missing_pair_set_id_on_eligible_row(tmp_path: Path) -> None:
    """Eligible generated rows must be anchored to a registry pair_set."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    pairs_path = base / SEFM / "assets" / "extracted" / "pairs.jsonl"
    row = json.loads(pairs_path.read_text().strip())
    row.pop("pair_set_id", None)
    pairs_path.write_text(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "eligible generated row must carry pair_set_id" in result.stderr
    assert "eligible generated row must reference a known pair_set_id" in result.stderr


def test_seed_asset_validator_rejects_registry_markdown_count_drift(tmp_path: Path) -> None:
    """Human REGISTRY.md counts must not drift from structured registry facts."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    registry_md = base / "REGISTRY.md"
    text = registry_md.read_text()
    text = text.replace(
        "| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 🟢 | NL+STM一手 | 🔴未公开 | 🟢开权重可用 | ⚪不适用 | 已下载 | 999 / 999 | 989 | 999 | 0 | 10 / 10 |",
        "| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 🟢 | NL+STM一手 | 🔴未公开 | 🟢开权重可用 | ⚪不适用 | 已下载 | 3 / 3 | 989 | 999 | 0 | 10 / 10 |",
    )
    registry_md.write_text(text)

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "REGISTRY.md NL 数 mismatch" in result.stderr


def test_seed_asset_validator_rejects_registry_missing_assets_link(tmp_path: Path) -> None:
    """Rows with assets/README.md must link seed_id directly to that README."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    registry_md = base / "REGISTRY.md"
    text = registry_md.read_text()
    text = text.replace("[`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md)", "`sefm-llm-state-machine`")
    registry_md.write_text(text)

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "must link to ./sefm-llm-state-machine/assets/README.md" in result.stderr


def test_seed_asset_validator_rejects_missing_source_inventory(tmp_path: Path) -> None:
    """Registry entries must carry machine-readable NL inventory facts."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    registry_path = base / UNIFIED / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    registry.pop("source_inventory", None)
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "registry missing required field source_inventory" in result.stderr


def test_seed_asset_validator_rejects_source_inventory_count_drift(tmp_path: Path) -> None:
    """source_inventory counts must be derived from pairs/pair_sets, not trusted."""

    base = _copy_seed_library_subset(tmp_path, UNIFIED)
    registry_path = base / UNIFIED / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    inventory = registry["source_inventory"]
    inventory["raw_nl_count"] = 998
    inventory["unique_nl_count"] = 998
    inventory["nl_only_count"] = 9
    inventory["nl_only_unique_count"] = 9
    inventory["generated_pair_count"] = 123
    inventory["unique_generated_stm0_count"] = 123
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), UNIFIED],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "source_inventory raw_nl_count mismatch" in result.stderr
    assert "source_inventory unique_nl_count mismatch" in result.stderr
    assert "source_inventory nl_only_count mismatch" in result.stderr
    assert "source_inventory nl_only_unique_count mismatch" in result.stderr
    assert "source_inventory generated_pair_count mismatch" in result.stderr
    assert "source_inventory unique_generated_stm0_count mismatch" in result.stderr


def test_seed_asset_validator_rejects_source_inventory_pair_set_drift(tmp_path: Path) -> None:
    """SEFM has 9 NL descriptions even though pairs.jsonl currently has one row."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    registry_path = base / SEFM / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    registry["source_inventory"]["raw_nl_count"] = 1
    registry["source_inventory"]["unique_nl_count"] = 1
    registry["source_inventory"]["nl_only_count"] = 0
    registry["source_inventory"]["nl_only_unique_count"] = 0
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "source_inventory raw_nl_count mismatch" in result.stderr
    assert "source_inventory nl_only_count mismatch" in result.stderr




def test_seed_asset_validator_rejects_invalid_manifest_schema_enum(tmp_path: Path) -> None:
    """assets_manifest.schema.json must be enforced, not only documented."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    manifest_path = base / SEFM / "assets" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["assets"][0]["source_url_type"] = "stale_source_type"
    manifest["assets"][0]["download_status"] = "almost_downloaded"
    manifest["assets"][0]["storage_mode"] = "floating_cache"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "assets_manifest.schema.json validation error" in result.stderr
    assert "assets[0] unknown download_status" in result.stderr
    assert "assets[0] unknown storage_mode" in result.stderr

def test_seed_asset_validator_rejects_invalid_registry_schema_enum(tmp_path: Path) -> None:
    """The JSON Schema must be enforced, including license / redistribution enums."""

    base = _copy_seed_library_subset(tmp_path, SEFM)
    registry_path = base / SEFM / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    registry["asset_summary"]["license_status"] = "STALE_LICENSE_BLOCKER"
    registry["asset_summary"]["redistribution_status"] = "STALE_REDIS_BLOCKER"
    registry["downstream_selection"]["r2_smoke_recommendation"] = "strong"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), SEFM],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "seed_resource_registry.schema.json validation error" in result.stderr
    assert "unknown asset_summary license_status" in result.stderr
    assert "unknown asset_summary redistribution_status" in result.stderr
    assert "unknown r2_smoke_recommendation strong" in result.stderr

def test_seed_asset_validator_rejects_resource_profile_semantic_drift(tmp_path: Path) -> None:
    """LLM/code reproducibility profile must remain auditable and cannot upgrade pipeline-only to final pool."""

    base = _copy_seed_library_subset(tmp_path, "designing-fsm-gpt4")
    registry_path = base / "designing-fsm-gpt4" / "seed_resource_registry.json"
    registry = json.loads(registry_path.read_text())
    profile = registry["resource_profile"]
    profile["paper_llm_availability_checked_at"] = "2026/06/23"
    profile["paper_llm_availability_evidence_urls"] = []
    profile["code_reproducibility_evidence_paths"] = ["assets/extracted/missing.json"]
    profile["code_reproducibility_label"] = "⚪不适用"
    registry["recommended_role"] = "final_pool_ready"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    env = os.environ.copy()
    env["SEED_LIBRARY_BASE"] = str(base)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "designing-fsm-gpt4"],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode != 0
    assert "paper_llm_availability_checked_at must use yyyy-mm-dd" in result.stderr
    assert "paper_uses_llm=yes requires paper_llm_availability_evidence_urls" in result.stderr
    assert "code_reproducibility evidence path missing" in result.stderr
    assert "code_reproducibility_label mismatch" in result.stderr
    assert "nl_code_reproducible cannot be recommended_role final_pool_ready" in result.stderr
