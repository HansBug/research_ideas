"""Version-aware labels never mutate or re-evaluate frozen evidence."""

import hashlib
import json
from pathlib import Path

import pytest

from paper_stm_evaluation.predicate_id_mapping import (
    CURRENT_IDS, CURRENT_REGISTRY, PRE_P1_REGISTRY, PRE_P1_TO_CURRENT,
    build_predicate_id_view, current_predicate_id, main,
)
from paper_stm_evaluation.stage_loss import (
    _predicate_feasibility, _resolve_planned_predicate_scope,
)

PAPER_ROOT = Path(__file__).resolve().parents[2]


def test_versioned_mapping_covers_all_ids_and_rejects_ambiguous_inputs() -> None:
    assert len(PRE_P1_TO_CURRENT) == 19
    assert len(CURRENT_IDS) == 12
    for old, new in PRE_P1_TO_CURRENT.items():
        assert current_predicate_id(PRE_P1_REGISTRY, old) == new
    for value in CURRENT_IDS:
        assert current_predicate_id(CURRENT_REGISTRY, value) == value
    for collision in ("G3", "R3", "V1"):
        assert current_predicate_id(PRE_P1_REGISTRY, collision) is None
        assert current_predicate_id(CURRENT_REGISTRY, collision) == collision
    for version, value in (("unknown", None), (CURRENT_REGISTRY, "G4"), (PRE_P1_REGISTRY, "S7")):
        with pytest.raises(ValueError):
            current_predicate_id(version, value)


def test_view_preserves_retired_and_unbound_receipts_and_source_bytes(tmp_path: Path) -> None:
    run = tmp_path / "source"
    cell_dir = run / "method/0000"
    cell_dir.mkdir(parents=True)
    manifest = run / "run_manifest.json"
    manifest.write_text(json.dumps({"run_id": "a" * 32, "registry_version": PRE_P1_REGISTRY, "registry_hash": "original-hash"}))
    cell = cell_dir / "round-1.json"
    cell.write_text(json.dumps({"run_id": "a" * 32, "predicate_execution_receipts": [
        {"predicate_id": old, "terminal_state": "completed", "predicate_verdict": "false"}
        for old in ("G3", "G4", "R3", "R4", "V1", "V4", "S6", None)
    ]}))
    before = {path: path.read_bytes() for path in (manifest, cell)}
    view = build_predicate_id_view(run)
    assert view["receipt_count"] == 8
    assert sum(row["terminal_count"] for row in view["rows"]) == 8
    rows = {row["original_predicate_id"]: row for row in view["rows"]}
    assert rows["G3"]["mapping_status"] == "retired"
    assert rows["G4"]["current_predicate_id"] == "G3"
    assert rows[None]["mapping_status"] == "unbound"
    output = tmp_path / "view.json"
    assert main(["--run-root", str(run), "--output", str(output)]) == 0
    with pytest.raises(FileExistsError):
        main(["--run-root", str(run), "--output", str(output)])
    for target in (run / "view.json", tmp_path / "final_results/view.json"):
        with pytest.raises(SystemExit):
            main(["--run-root", str(run), "--output", str(target)])
    assert all(path.read_bytes() == data for path, data in before.items())


def test_retained_predicate_definitions_are_unchanged_apart_from_ids_and_sources() -> None:
    paths = [PAPER_ROOT / "related_work/provenance/archive/pre_p1_20260905/predicate_registry.json",
             PAPER_ROOT / "method/src/paper_stm_method/resources/predicate_registry.json"]
    old, current = [{p["id"]: p for family in json.loads(path.read_text())["families"] for p in family["predicates"]} for path in paths]
    for old_id, new_id in PRE_P1_TO_CURRENT.items():
        if new_id is not None:
            for field in ("name", "semantics", "inputs", "source_types"):
                assert old[old_id][field] == current[new_id][field], (old_id, field)


def test_stage_loss_uses_the_runs_registry_not_current_backend_availability() -> None:
    scope, predicates = _resolve_planned_predicate_scope(
        pair_ids=("0000",), requested_scope=None, applicability=None,
        registry_version=CURRENT_REGISTRY,
    )
    assert scope == "current-12" and set(predicates) == CURRENT_IDS
    for version, requested in ((PRE_P1_REGISTRY, "current-12"), (CURRENT_REGISTRY, "full-scale-15")):
        with pytest.raises(ValueError):
            _resolve_planned_predicate_scope(pair_ids=("0000",), requested_scope=requested,
                                            applicability=None, registry_version=version)
    old = _predicate_feasibility(method_indexes={}, applicability=None, planned_predicates=(), registry_version=PRE_P1_REGISTRY)
    current = _predicate_feasibility(method_indexes={}, applicability=None, planned_predicates=predicates, registry_version=CURRENT_REGISTRY)
    assert old["S6"]["backend_implemented"] is True
    assert set(current) == CURRENT_IDS


def test_v61_selected_receipt_counts_are_conserved_without_touching_frozen_files() -> None:
    archive = PAPER_ROOT / "final_results/v61_source_divergence_vs_x1v2_baseline/raw"
    roots = (archive / "v61_current/method", archive / "v61_current_fill0045")
    views = [build_predicate_id_view(root) for root in roots]
    # The published selection replaces this failed cell with the stored fill run.
    failed = json.loads((roots[0] / "method/0045/round-1.json").read_text())
    assert failed["predicate_execution_receipts"] == []
    assert len(views[0]["source_cells"]) == 162 and len(views[1]["source_cells"]) == 1
    rows = [row for view in views for row in view["rows"]]
    assert sum(row["terminal_count"] for row in rows) == 1114
    assert sum(row["true"] for row in rows) == 573
    assert sum(row["false"] for row in rows) == 541
    for root, view in zip(roots, views):
        for source in view["source_cells"]:
            assert hashlib.sha256((root / source["path"]).read_bytes()).hexdigest() == source["sha256"]
