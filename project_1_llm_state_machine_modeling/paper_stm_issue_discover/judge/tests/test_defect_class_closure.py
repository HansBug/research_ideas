"""Defect-class closure over one frozen v60 judge input.

These tests read a frozen input closure from ``final_results`` when the source
checkout carries it. The standalone release does not ship frozen results, so the
tests skip there; the pure-logic tests in ``test_judge_provider_free_fixture.py``
still run in that release. A skip here therefore never hides a protocol change in
the release package, it only means the source-tree closure fixture is absent.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from paper_stm_judge.models import (
    ConflictKind,
    CoreClaimTruth,
    DefectClass,
    UnifiedJudgeInput,
    ValidityGateStatus,
)
from paper_stm_judge.runner import detect_validity_disagreements
from paper_stm_judge.scale_audit import _validity_envelope
from paper_stm_judge.schema import (
    build_exact_validity_batch_model,
    build_validity_batch_input,
    materialize_validity_certificate,
    validity_batch_responses,
    validity_item_input,
)

_FROZEN_INPUT = (
    Path(__file__).resolve().parents[2]
    / "final_results"
    / "v60_current_vs_x1v2_baseline"
    / "raw"
    / "v60_current"
    / "judge"
    / "source_runs"
    / "77404499c3ac4511a218f0ad3f91c45b"
    / "inputs"
    / "0004.json"
)


@pytest.fixture(scope="module")
def frozen_batch():
    if not _FROZEN_INPUT.is_file():
        pytest.skip(f"frozen source-tree judge input is not shipped here: {_FROZEN_INPUT}")
    judge_input = UnifiedJudgeInput.model_validate(
        json.loads(_FROZEN_INPUT.read_text(encoding="utf-8"))
    )
    report_ids = tuple(item.report_id for item in judge_input.reports[:2])
    batch_input = build_validity_batch_input(judge_input, report_ids, batch_id="VB-test")
    model = build_exact_validity_batch_model(batch_input)
    return judge_input, batch_input, model


def _payload(batch_input, defect_class: str, *, refute_core: bool = False) -> dict:
    payload = {"schema_version": "semantic-judge.validity-batch-response.v1", "batch_id": batch_input.batch_id}
    for index, report in enumerate(batch_input.reports):
        item = _validity_envelope(validity_item_input(batch_input, index))
        item["defect_adjudication"]["defect_class"] = defect_class
        if refute_core:
            item["claim_audit"]["item0"]["verdict"] = "REFUTED"
        payload[f"item{index}"] = item
    return payload


def test_valid_class_with_refuted_core_clause_is_rejected_with_repair_direction(frozen_batch) -> None:
    _judge_input, batch_input, model = frozen_batch
    with pytest.raises(ValueError, match="reclassify a non-load-bearing explanatory error as AUXILIARY_CONTEXT or choose A0_FALSE_POSITIVE"):
        model.model_validate(_payload(batch_input, "D2", refute_core=True))


def test_false_positive_requires_a_refuted_hard_clause(frozen_batch) -> None:
    _judge_input, batch_input, model = frozen_batch
    with pytest.raises(ValueError, match="A0_FALSE_POSITIVE requires the false load-bearing premise"):
        model.model_validate(_payload(batch_input, "A0_FALSE_POSITIVE"))
    accepted = model.model_validate(_payload(batch_input, "A0_FALSE_POSITIVE", refute_core=True))
    assert accepted.batch_id == batch_input.batch_id


@pytest.mark.parametrize(
    ("defect_class", "gate", "truth"),
    [
        ("D2", ValidityGateStatus.SATISFIED, CoreClaimTruth.VALID),
        ("D1", ValidityGateStatus.SATISFIED, CoreClaimTruth.VALID),
        ("D0", ValidityGateStatus.REFUTED, CoreClaimTruth.INVALID),
        ("A0_NOT_A_DEFECT_CLAIM", ValidityGateStatus.REFUTED, CoreClaimTruth.INVALID),
    ],
)
def test_certificate_derives_minimum_evidence_gate_from_defect_class(frozen_batch, defect_class, gate, truth) -> None:
    _judge_input, batch_input, model = frozen_batch
    response = model.model_validate(_payload(batch_input, defect_class))
    rows = validity_batch_responses(response, batch_input)
    certificate = materialize_validity_certificate(rows[0], validity_item_input(batch_input, 0))
    assert certificate.defect_adjudication.defect_class == DefectClass(defect_class)
    assert certificate.minimum_evidence_gate.status == gate
    assert certificate.core_truth == truth
    assert certificate.schema_version == "semantic-judge.frozen-validity-certificate.v3"


def test_defect_class_disagreement_triggers_arbitration(frozen_batch) -> None:
    _judge_input, batch_input, model = frozen_batch
    first = validity_batch_responses(model.model_validate(_payload(batch_input, "D1")), batch_input)[0]
    second = validity_batch_responses(model.model_validate(_payload(batch_input, "D0")), batch_input)[0]
    item_input = validity_item_input(batch_input, 0)
    disagreements = detect_validity_disagreements(
        materialize_validity_certificate(first, item_input),
        materialize_validity_certificate(second, item_input),
    )
    kinds = {item.kind for item in disagreements}
    assert ConflictKind.DEFECT_CLASS in kinds
    assert ConflictKind.CORE_TRUTH in kinds
    class_conflict = next(item for item in disagreements if item.kind == ConflictKind.DEFECT_CLASS)
    assert class_conflict.object_ref.endswith("/defect_class")
    assert (class_conflict.reading_1_value, class_conflict.reading_2_value) == ("D1", "D0")
