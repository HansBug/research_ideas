"""Regression gates for the pyfcstm-only FCSTM semantic projection."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from pipeline.evidence_discovery.inputs import parse_fcstm
from pipeline.evidence_discovery.inputs.fcstm_native_projection import (
    NativeTransitionCarrier,
    all_transition_carriers,
    load_native_document,
)
from pipeline.evidence_discovery.inputs.native_projection_audit import (
    build_native_projection_audit,
)
from pipeline.evidence_discovery.semantics.binding import resolve_state_ref


REPORT_ROOT = (
    Path(__file__).resolve().parents[2]
    / "representation"
    / "reports"
    / "llms_emp_r45_java_60"
)


def test_native_parser_accepts_semicolon_terminated_state_and_event_declarations() -> None:
    """Legal FCSTM declarations are accepted by pyfcstm, not a local regex grammar."""

    model = parse_fcstm(
        """
            state Root {
                state Disjoint;
                event Signal;
                [*] -> Disjoint;
        }
        """
    )

    assert model.state("Root.Disjoint") is not None
    assert model.event("Root.Signal") is not None
    models_source = (
        Path(__file__).parents[5] / "utils/stm_artifacts/models.py"
    ).read_text(encoding="utf-8")
    assert all(
        marker not in models_source
        for marker in (
            "_STATE_RE",
            "_EVENT_RE",
            "_TRANSITION_RE",
            "_ACTION_RE",
            "_GUARD_RE",
            "_EFFECT_RE",
        )
    )


def test_native_authored_carrier_is_an_immutable_pydantic_projection() -> None:
    """Native carrier adapters retain typed fields without serializing live objects."""

    document = load_native_document(
        "state Root {\nstate A;\nstate B;\nevent Go;\n[*] -> A;\nA -> B : Go;\n}\n"
    )
    carrier = next(item for item in all_transition_carriers(document) if item.source == "A")

    assert isinstance(carrier, BaseModel)
    assert isinstance(carrier, NativeTransitionCarrier)
    assert all(field.description for field in NativeTransitionCarrier.model_fields.values())
    assert "native_transitions" not in carrier.model_dump(mode="json")
    assert "events" not in carrier.model_dump(mode="json")


def test_native_projection_audit_covers_all_real_sources_and_known_regressions() -> None:
    """The 60-source/54-closure audit preserves every previously lost native feature."""

    audit = build_native_projection_audit(REPORT_ROOT)
    rows = {row.pair_id: row for row in audit.pair_audits}

    assert audit.source_pair_count == 60
    assert audit.frozen_input_closure_pair_count == 54
    assert audit.all_native_loads_succeeded
    assert audit.all_projection_parity_succeeded
    assert audit.all_frozen_input_closures_succeeded
    assert not audit.unapproved_text_handling
    assert sum(rows[pair_id].pseudo_state_count for pair_id in ("0018", "0038")) == 13
    assert sum(
        rows[pair_id].effect_only_transition_count
        for pair_id in ("0008", "0048")
    ) >= 26
    assert sum(
        rows[pair_id].lifecycle_action_count
        for pair_id in ("0004", "0034", "0044")
    ) == 12
    assert sum(
        len(rows[pair_id].forced_carrier_refs)
        for pair_id in ("0004", "0033")
    ) == 4
    assert all(not rows[pair_id].differences for pair_id in rows)


def test_only_native_projection_can_split_fcstm_source_for_attribution() -> None:
    """Semantic modules must not recover carriers from FCSTM source lines."""

    evidence_root = Path(__file__).parents[5] / "utils/stm_artifacts"
    direct_source_reads = []
    for path in evidence_root.rglob("*.py"):
        if "tests" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if ".source_text.splitlines()" in text or ".fcstm_text.splitlines()" in text:
            direct_source_reads.append(path.relative_to(evidence_root).as_posix())
    assert direct_source_reads == ["fcstm_native_projection.py"]


def test_duplicate_native_local_names_require_canonical_path_or_unique_legacy_ref() -> None:
    """Nested same-name states cannot be bound by a guessed local display name."""

    source = (
        REPORT_ROOT / "pairs" / "0029" / "fcstm.fcstm"
    ).read_text(encoding="utf-8")
    model = parse_fcstm(source)
    duplicates = [state for state in model.states if state.name == "UnspecifiedInitial"]

    assert len(duplicates) == 2
    assert len({state.canonical_path for state in duplicates}) == 2
    assert resolve_state_ref("UnspecifiedInitial", model) is None
    for state in duplicates:
        assert resolve_state_ref(state.canonical_path, model) == state.ref
        assert model.normalize_ref(state.legacy_refs[0]) == state.ref
