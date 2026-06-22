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


def _copy_seed_library_subset(tmp_path: Path, *seed_ids: str) -> Path:
    base = tmp_path / "seed_library"
    base.mkdir()
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
        "pair_count": 3,
        "trace_verified_pair_count": 3,
        "eligible_generated_pair_count": 3,
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
    summary["pair_count"] = 999
    summary["hash_match_count"] = 999
    summary["locator_resolved_count"] = 999
    summary["text_or_hash_match_count"] = 999
    summary["repo_or_external_reproducible_eligible_count"] = 999
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
