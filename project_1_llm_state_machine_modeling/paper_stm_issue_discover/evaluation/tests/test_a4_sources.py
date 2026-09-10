"""A4 selects immutable Full populations, including the agreed Luna replacement."""

from pathlib import Path

import pytest

from paper_stm_evaluation.a4_sources import checked_json, contained, source_manifest


PAPER = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("model", ["sonnet", "luna", "qwen", "muse"])
def test_frozen_population_and_source_hashes(model):
    manifest = source_manifest(PAPER, model)
    assert len(manifest["cells"]) == 162
    if model == "luna":
        replacement = next(
            cell for cell in manifest["cells"]
            if (cell["pair"], cell["round"]) == ("0045", 1)
        )
        assert replacement["source"].endswith(
            "v61_current_fill0045/method/0045/round-1.json"
        )


def test_hash_drift_and_archive_escape_are_rejected(tmp_path):
    source = tmp_path / "source.json"
    source.write_text('{"value": 1}', encoding="utf-8")
    _, digest = checked_json(source)
    source.write_text('{"value": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        checked_json(source, digest)
    with pytest.raises(ValueError, match="escapes archive"):
        contained(tmp_path, "../elsewhere.json")
