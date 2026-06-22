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


def _copy_seed_library_subset(tmp_path: Path) -> Path:
    base = tmp_path / "seed_library"
    base.mkdir()
    shutil.copytree(SEED_LIBRARY / UNIFIED, base / UNIFIED)
    return base


def test_seed_asset_validator_accepts_unmodified_unified_trace(tmp_path: Path) -> None:
    base = _copy_seed_library_subset(tmp_path)
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

    base = _copy_seed_library_subset(tmp_path)
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
