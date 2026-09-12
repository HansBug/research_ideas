from __future__ import annotations

import json
import re
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from pipeline.semantic_judge.artifacts import stable_model_hash
from pipeline.semantic_judge.models import (
    AdapterAudit,
    AdapterIdMap,
    CandidateReport,
    CoreClaimTruth,
    MatchStrength,
    ReportValidity,
)
from pipeline.semantic_judge.protocol import (
    RELATION_SYSTEM_PROMPT,
    VALIDITY_SYSTEM_PROMPT,
)
from pipeline.semantic_judge.runner import (
    JudgeExecutionFailure,
    build_primary_prompt,
    build_validity_prompt,
    judge_pair,
)
from pipeline.semantic_judge.schema import (
    build_exact_relation_model,
    build_exact_validity_model,
    build_relation_input,
    build_validity_input,
    materialize_validity_certificate,
)

from .test_models_and_schema import minimal_input


class FakeRuntime:
    real_llm = False
    profile = "gpt-5.6-luna"

    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []
        self.config = SimpleNamespace(max_output_tokens=128_000)

    def call(self, **kwargs):
        self.calls.append(kwargs)
        payload = self.payloads.pop(0)
        recipe = getattr(kwargs["schema"], "__semantic_judge_recipe__", None)
        if recipe is not None and "batch_id" not in payload:
            report_count = len(recipe["input"]["reports"])
            items = [payload]
            items.extend(self.payloads.pop(0) for _ in range(report_count - 1))
            payload = {
                "schema_version": (
                    "semantic-judge.validity-batch-response.v1"
                    if recipe["kind"] == "validity_batch"
                    else "semantic-judge.relation-batch-response.v1"
                ),
                "batch_id": recipe["input"]["batch_id"],
                **{f"item{index}": item for index, item in enumerate(items)},
            }
        response = kwargs["schema"].model_validate(payload)
        return SimpleNamespace(
            succeeded=True,
            response=response,
            usage=[],
            attempts=[],
            cost={"total_usd": 0.0, "eligible": True},
            reason="Provider-free structured fixture succeeded.",
            basis="FakeRuntime exact Pydantic validation.",
        )


def adapter_audit(report_count: int, expected_count: int) -> AdapterAudit:
    return AdapterAudit(
        source_format="x1v2_record",
        source_path="/fixture/source.json",
        source_hash="sha256:" + "3" * 64,
        report_id_map=tuple(
            AdapterIdMap(
                anonymous_id=f"R{index:04d}",
                original_id=f"original-report-{index}",
            )
            for index in range(1, report_count + 1)
        ),
        expected_id_map=tuple(
            AdapterIdMap(
                anonymous_id=f"E{index:04d}",
                original_id=f"LEDGER-{index}",
            )
            for index in range(1, expected_count + 1)
        ),
        projected_field_names=("report_id", "claim", "reason"),
        excluded_field_names=("arm", "witness_level", "d_level"),
        reason="Fixture adapter projection.",
        basis="Provider-free fixture mapping.",
    )


def validity_payload(
    validity_input,
    *,
    refuted: set[tuple[str, str]] | None = None,
    cluster_key: str = "one actionable technical mechanism",
) -> dict:
    """Build one exact fixed-field validity response fixture."""

    refuted = refuted or set()

    def gate(status: str, subject: str) -> dict:
        return {
            "status": status,
            "reason": f"The complete common artifacts determine the {subject} gate.",
            "basis": f"The immutable report clauses and common artifacts establish the {subject} status.",
            "source_refs": ["artifact:natural_language"],
        }

    payload = {
        "schema_version": "semantic-judge.validity-response.v3",
        "report_id": validity_input.report.report_id,
        "root_cause_cluster_key": cluster_key,
        "minimum_evidence_gate": gate("SATISFIED", "minimum evidence"),
        "validity_reason": "Every immutable core clause was reviewed against the common artifacts.",
        "validity_basis": "The report source clauses and common artifacts determine every verdict.",
        "validity_source_refs": ["artifact:natural_language"],
    }
    for field_plan in validity_input.core_envelope.field_plans:
        payload[f"{field_plan.report_field.value}_audit"] = {
            f"item{index}": {
                "clause_id": clause.clause_id,
                "assertion": "This English assertion faithfully represents the complete immutable source clause.",
                "validity_role": (
                    "CORE_CLAIM"
                    if field_plan.report_field.value == "claim"
                    else "INDISPENSABLE_MECHANISM"
                    if field_plan.report_field.value == "reason"
                    else "AUXILIARY_CONTEXT"
                ),
                "verdict": (
                    "REFUTED"
                    if (field_plan.report_field.value, clause.clause_id) in refuted
                    else "SUPPORTED"
                ),
                "reason": (
                    "The common artifacts contradict a material premise in this complete clause."
                    if (field_plan.report_field.value, clause.clause_id) in refuted
                    else "The common artifacts support every material premise in this complete clause."
                ),
                "basis": "The authored source and deterministic artifact facts provide the direct evidence.",
                "source_refs": ["artifact:natural_language"],
            }
            for index, clause in enumerate(field_plan.clauses)
        }
    return payload


def relation_payload(relation_input, matches=None) -> dict:
    """Build one exact relation-only response fixture."""

    matches = matches or {}
    decisions = []
    for expected in relation_input.expected_issues:
        match = matches.get(expected.expected_id, MatchStrength.NO_MATCH)
        if match == MatchStrength.NO_MATCH:
            decisions.append(
                {
                    "expected_id": expected.expected_id,
                    "match": "NO_MATCH",
                    "reason": "This valid report concerns a different expected defect or obligation.",
                    "basis": "The report, expected issue, and common artifacts establish this explicit boundary.",
                    "source_refs": [
                        f"expected:{expected.expected_id}",
                        "artifact:natural_language",
                    ],
                }
            )
        else:
            decisions.append(
                {
                    "expected_id": expected.expected_id,
                    "match": match.value,
                    "report_field_refs": ["claim", "reason"],
                    "reason": "The valid report states this expected issue's actionable technical facet.",
                    "basis": "The frozen certificate, expected obligation, and common artifacts establish the relation.",
                    "source_refs": [
                        f"expected:{expected.expected_id}",
                        "artifact:natural_language",
                    ],
                }
            )
    return {
        "schema_version": "semantic-judge.relation-response.v2",
        "report_id": relation_input.report.report_id,
        "validity_certificate_hash": (
            relation_input.validity_certificate.certificate_hash
        ),
        "relation_decisions": decisions,
        "relation_reason": "Every exact expected position has one complete relation decision.",
        "relation_basis": "The immutable VALID certificate and common artifact closure were preserved.",
        "relation_source_refs": ["artifact:natural_language"],
    }


def certificate_from_payload(validity_input, payload):
    model = build_exact_validity_model(validity_input)
    return materialize_validity_certificate(
        model.model_validate(payload), validity_input
    )


def test_validity_prompt_physically_excludes_expected_and_experimental_metadata() -> (
    None
):
    judge_input = minimal_input(report_count=1, expected_count=2)
    validity_input = build_validity_input(judge_input, "R0001")
    prompt = build_validity_prompt(validity_input)
    compatibility_prompt = build_primary_prompt(judge_input)

    assert prompt == compatibility_prompt
    assert "expected_issues" not in prompt
    assert '"expected_id"' not in prompt
    serialized_input = prompt.split("<validity_input>\n", 1)[1].split(
        "\n</validity_input>", 1
    )[0]
    serialized_keys = json.dumps(json.loads(serialized_input), sort_keys=True)
    assert "expected_issues" not in serialized_keys
    assert "expected_id" not in serialized_keys
    assert "ledger" not in serialized_keys.lower()
    assert '"arm"' not in prompt
    assert '"witness_level"' not in prompt
    assert '"d_level"' not in prompt
    assert '"predicate_id"' not in prompt
    assert "FULL_MATCH" not in prompt
    assert "PARTIAL_MATCH" not in prompt


def test_expected_changes_do_not_change_validity_input_or_hash() -> None:
    first = minimal_input(report_count=1, expected_count=2)
    second = first.model_copy(
        update={
            "expected_issues": tuple(
                item.model_copy(
                    update={
                        "expected_id": f"E{3 - index:04d}",
                        "summary": f"decoy summary {index}",
                        "detail": f"decoy detail {index}",
                    }
                )
                for index, item in enumerate(reversed(first.expected_issues), start=1)
            )
        }
    )
    first_validity = build_validity_input(first, "R0001")
    second_validity = build_validity_input(second, "R0001")

    assert first_validity == second_validity
    assert stable_model_hash(first_validity) == stable_model_hash(second_validity)
    assert build_validity_prompt(first_validity) == build_validity_prompt(
        second_validity
    )


def test_fixed_validity_slots_reject_claim_or_clause_omission_and_where_injection() -> (
    None
):
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    schema = build_exact_validity_model(validity_input)
    payload = validity_payload(validity_input)

    provider_schema = schema.model_json_schema()
    assert "minimum_evidence_gate" in provider_schema["properties"]
    assert "core_claim_gate" not in provider_schema["properties"]
    assert "indispensable_mechanism_gate" not in provider_schema["properties"]
    claim_group_ref = provider_schema["properties"]["claim_audit"]["$ref"]
    claim_group = provider_schema["$defs"][claim_group_ref.rsplit("/", 1)[-1]]
    assert claim_group["type"] == "object"
    assert claim_group["required"] == ["item0"]
    assert claim_group["additionalProperties"] is False
    assert "prefixItems" not in claim_group

    missing_claim = dict(payload)
    missing_claim.pop("claim_audit")
    with pytest.raises(ValidationError, match="claim_audit"):
        schema.model_validate(missing_claim)

    missing_clause = json.loads(json.dumps(payload))
    missing_clause["reason_audit"].pop("item0")
    with pytest.raises(ValidationError, match="item0"):
        schema.model_validate(missing_clause)

    with_where = dict(payload)
    with_where["where_audit"] = payload["claim_audit"]
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        schema.model_validate(with_where)


def test_invalid_certificate_never_enters_relation_stage() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    refuted = {
        ("claim", validity_input.core_envelope.field_plans[0].clauses[0].clause_id)
    }
    invalid = validity_payload(validity_input, refuted=refuted)
    runtime = FakeRuntime((invalid, invalid))

    result = judge_pair(
        run_id="fixture-invalid",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="a" * 40,
    )

    assert len(runtime.calls) == 2
    assert all("validity" in item["kind"] for item in runtime.calls)
    assert result.metrics.invalid_count == 1
    assert result.final_reading.relations[0].match == MatchStrength.NO_MATCH
    assert result.relation_reading_1.backend_invalid_report_ids == ("R0001",)
    assert result.relation_reading_1.responses == ()


def test_valid_novel_and_concise_report_remain_valid_without_formal_witness() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    valid = validity_payload(validity_input)
    certificate = certificate_from_payload(validity_input, valid)
    relation_input = build_relation_input(judge_input, certificate)
    no_match = relation_payload(relation_input)
    runtime = FakeRuntime((valid, valid, no_match, no_match))

    result = judge_pair(
        run_id="fixture-novel",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="b" * 40,
    )

    assert result.metrics.valid_novel_count == 1
    assert result.metrics.invalid_count == 0
    assert result.report_outcomes[0].validity == ReportValidity.VALID_NOVEL
    assert len(result.call_receipts) == 4


def test_refuted_auxiliary_reason_wording_does_not_kill_supported_core() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    payload = validity_payload(validity_input)
    reason_row = payload["reason_audit"]["item0"]
    reason_row["validity_role"] = "AUXILIARY_CONTEXT"
    reason_row["verdict"] = "REFUTED"
    reason_row["reason"] = (
        "One incidental phrase is inaccurate but is not needed to sustain the bounded claim."
    )

    certificate = certificate_from_payload(validity_input, payload)

    assert certificate.core_truth == CoreClaimTruth.VALID
    assert [
        (item.report_field.value, item.clause_id)
        for item in certificate.auxiliary_warnings
    ] == [("reason", "C1")]


def test_refuted_indispensable_mechanism_invalidates_supported_conclusion() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    payload = validity_payload(validity_input, refuted={("reason", "C1")})

    certificate = certificate_from_payload(validity_input, payload)

    assert certificate.core_claim_gate.status.value == "SATISFIED"
    assert certificate.indispensable_mechanism_gate.status.value == "REFUTED"
    assert certificate.core_truth == CoreClaimTruth.INVALID


@pytest.mark.parametrize(
    ("refuted", "expected_validity"),
    [
        (set(), ReportValidity.VALID_NOVEL),
        ({("claim", "C1")}, ReportValidity.INVALID),
    ],
)
def test_empty_expected_denominator_runs_validity_only_and_closes_ownership(
    refuted: set[tuple[str, str]], expected_validity: ReportValidity
) -> None:
    judge_input = minimal_input(report_count=1, expected_count=0)
    validity_input = build_validity_input(judge_input, "R0001")
    response = validity_payload(validity_input, refuted=refuted)
    runtime = FakeRuntime((response, response))

    result = judge_pair(
        run_id="fixture-empty-expected",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 0),
        runtime=runtime,
        judge_code_commit="d" * 40,
    )

    assert len(runtime.calls) == 2
    assert all("validity" in item["kind"] for item in runtime.calls)
    assert result.relation_reading_1.responses == ()
    assert result.relation_reading_2.responses == ()
    assert result.final_reading.relations == ()
    assert result.final_reading.expected_assessments == ()
    assert result.report_outcomes[0].validity == expected_validity
    assert result.metrics.expected_count == 0
    assert result.metrics.report_count == 1
    assert result.metrics.valid_novel_count == (
        expected_validity == ReportValidity.VALID_NOVEL
    )
    assert result.metrics.invalid_count == (expected_validity == ReportValidity.INVALID)
    assert len(result.call_receipts) == 2


def test_validity_conflict_is_arbitrated_before_relation_visibility() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    valid = validity_payload(validity_input)
    refuted = {("claim", "C1")}
    invalid = validity_payload(validity_input, refuted=refuted)
    runtime = FakeRuntime((valid, invalid, invalid))

    result = judge_pair(
        run_id="fixture-validity-arbitration",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="c" * 40,
    )

    assert len(runtime.calls) == 3
    assert runtime.calls[2]["kind"] == "semantic-judge-validity-arbitration-batch"
    assert "expected_issues" not in runtime.calls[2]["prompt"]
    assert result.validity_arbitration_certificates[0].core_truth == (
        CoreClaimTruth.INVALID
    )
    assert result.metrics.invalid_count == 1


def test_relation_conflict_is_arbitrated_without_reopening_validity() -> None:
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    valid = validity_payload(validity_input)
    certificate = certificate_from_payload(validity_input, valid)
    relation_input = build_relation_input(judge_input, certificate)
    full = relation_payload(relation_input, {"E0001": MatchStrength.FULL_MATCH})
    partial = relation_payload(relation_input, {"E0001": MatchStrength.PARTIAL_MATCH})
    runtime = FakeRuntime((valid, valid, full, partial, full))

    result = judge_pair(
        run_id="fixture-relation-arbitration",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(1, 1),
        runtime=runtime,
        judge_code_commit="d" * 40,
    )

    assert len(runtime.calls) == 5
    assert runtime.calls[-1]["kind"] == "semantic-judge-relation-arbitration-batch"
    assert "field_audits" in runtime.calls[-1]["prompt"]
    assert result.final_reading.relations[0].match == MatchStrength.FULL_MATCH
    assert len(result.relation_arbitration_responses) == 1


def test_relation_schema_replays_and_eliminates_conditional_no_closure_failure() -> (
    None
):
    judge_input = minimal_input(expected_count=3)
    validity_input = build_validity_input(judge_input, "R0001")
    valid = validity_payload(validity_input)
    certificate = certificate_from_payload(validity_input, valid)
    relation_input = build_relation_input(judge_input, certificate)
    schema = build_exact_relation_model(relation_input)
    corrected = relation_payload(relation_input, {"E0003": MatchStrength.FULL_MATCH})
    old_failure = json.loads(json.dumps(corrected))
    for decision in old_failure["relation_decisions"]:
        if decision["match"] == "NO_MATCH":
            decision.pop("reason")
            decision.pop("basis")
            decision.pop("source_refs")
    old_failure["no_match_closure"] = None

    with pytest.raises(ValidationError) as caught:
        schema.model_validate(old_failure)
    error_text = str(caught.value)
    assert "reason" in error_text
    assert "basis" in error_text
    assert "source_refs" in error_text
    properties = schema.model_json_schema()["properties"]
    assert "no_match_closure" not in properties
    validated = schema.model_validate(corrected)
    assert [item.match for item in validated.relation_decisions] == [
        MatchStrength.NO_MATCH,
        MatchStrength.NO_MATCH,
        MatchStrength.FULL_MATCH,
    ]


def v19_0053_input():
    """Return the real three published reports from the preserved diagnostic run."""

    base = minimal_input(report_count=3, expected_count=3)
    reports = (
        CandidateReport(
            report_id="R0001",
            claim="PumpControl 内部被建模为三个并行区域（PumpRegion、WaterRegion、MethaneRegion），而不是一个包含三个可选择子状态的状态结构。",
            where="PumpControl 内的 state PumpRegion、state WaterRegion、state MethaneRegion 定义",
            reason="规范描述 PumpControl 下有三个主要子状态 PumpState、WaterState 和 MethaneState，系统从 PumpControl 可根据条件转移到不同子状态。这通常要求三者处于同一互斥状态层级；当前模型的三个区域各自拥有初始伪状态，PlantUML 语义上会同时激活三个区域，因此不能表示在三个子状态之间选择性转移。",
        ),
        CandidateReport(
            report_id="R0002",
            claim="模型没有表示从 PumpState 转移到 WaterState 或 MethaneState 的任何条件转移。",
            where="PumpControl 内部，仅存在各区域的默认初始进入关系",
            reason="规范明确说明系统从 PumpControl 可基于特定条件转移到 WaterState 和 MethaneState。模型只有各区域内部的默认初始进入关系，没有区域之间或三个子状态之间的事件或条件转移，因此无法表达这些转换。",
        ),
        CandidateReport(
            report_id="R0003",
            claim="模型没有确保系统首先进入 PumpState。",
            where="PumpControl 内三个区域分别从初始伪状态直接进入各自状态",
            reason="规范要求系统首先转换到 PumpState。由于三个并行区域会各自同时从初始伪状态进入 PumpState、WaterState 和 MethaneState，模型并非先进入 PumpState，而是同时进入三个状态。",
        ),
    )
    expected = tuple(
        item.model_copy(
            update={
                "summary": summary,
                "detail": detail,
            }
        )
        for item, summary, detail in zip(
            base.expected_issues,
            (
                "The sequential wrappers are mutually unreachable.",
                "The owner state has no default entry to the required first state.",
                "The named states have no operational outgoing transitions.",
            ),
            (
                "Missing conditional transitions are an actionable facet of the unreachable alternatives.",
                "This distinct issue concerns owner-level entry rather than inter-state behavior.",
                "The model is a zero-behavior stub because named-state transitions are absent.",
            ),
            strict=True,
        )
    )
    return base.model_copy(update={"reports": reports, "expected_issues": expected})


def _first_clause_containing(validity_input, field_name: str, text: str) -> str:
    field_plan = next(
        item
        for item in validity_input.core_envelope.field_plans
        if item.report_field.value == field_name
    )
    return next(
        item.clause_id for item in field_plan.clauses if text in item.exact_text
    )


def test_v19_replay_closes_0053_anchor_without_nearby_truth_rescue() -> None:
    judge_input = v19_0053_input()
    validity_inputs = {
        report.report_id: build_validity_input(judge_input, report.report_id)
        for report in judge_input.reports
    }
    r1_refuted = {
        (
            "claim",
            _first_clause_containing(validity_inputs["R0001"], "claim", "并行区域"),
        ),
        (
            "reason",
            _first_clause_containing(validity_inputs["R0001"], "reason", "同时激活"),
        ),
    }
    r3_refuted = {
        (
            "reason",
            _first_clause_containing(validity_inputs["R0003"], "reason", "并行区域"),
        )
    }
    validity_payloads = (
        validity_payload(
            validity_inputs["R0001"],
            refuted=r1_refuted,
            cluster_key="false concurrent-region mechanism",
        ),
        validity_payload(
            validity_inputs["R0002"],
            cluster_key="missing named-state conditional transitions",
        ),
        validity_payload(
            validity_inputs["R0003"],
            refuted=r3_refuted,
            cluster_key="false simultaneous-entry mechanism",
        ),
    )
    r2_certificate = certificate_from_payload(
        validity_inputs["R0002"], validity_payloads[1]
    )
    relation_input = build_relation_input(judge_input, r2_certificate)
    relation = relation_payload(
        relation_input,
        {
            "E0001": MatchStrength.FULL_MATCH,
            "E0003": MatchStrength.FULL_MATCH,
        },
    )
    runtime = FakeRuntime((*validity_payloads, *validity_payloads, relation, relation))

    result = judge_pair(
        run_id="v19-0053-provider-free-replay",
        round_no=1,
        judge_input=judge_input,
        adapter_audit=adapter_audit(3, 3),
        runtime=runtime,
        judge_code_commit="e" * 40,
    )

    assert [item.core_truth for item in result.validity_reading_1.certificates] == [
        CoreClaimTruth.INVALID,
        CoreClaimTruth.VALID,
        CoreClaimTruth.INVALID,
    ]
    assert [item.core_truth for item in result.validity_reading_2.certificates] == [
        CoreClaimTruth.INVALID,
        CoreClaimTruth.VALID,
        CoreClaimTruth.INVALID,
    ]
    assert result.validity_arbitration_certificates == ()
    assert [item.report_id for item in result.relation_reading_1.responses] == ["R0002"]
    matrix = {
        (item.report_id, item.expected_id): item.match
        for item in result.final_reading.relations
    }
    assert matrix == {
        ("R0001", "E0001"): MatchStrength.NO_MATCH,
        ("R0001", "E0002"): MatchStrength.NO_MATCH,
        ("R0001", "E0003"): MatchStrength.NO_MATCH,
        ("R0002", "E0001"): MatchStrength.FULL_MATCH,
        ("R0002", "E0002"): MatchStrength.NO_MATCH,
        ("R0002", "E0003"): MatchStrength.FULL_MATCH,
        ("R0003", "E0001"): MatchStrength.NO_MATCH,
        ("R0003", "E0002"): MatchStrength.NO_MATCH,
        ("R0003", "E0003"): MatchStrength.NO_MATCH,
    }
    assert result.metrics.full_hit_count == 2
    assert (
        result.metrics.valid_known_count,
        result.metrics.valid_novel_count,
        result.metrics.invalid_count,
    ) == (1, 0, 2)
    assert len(runtime.calls) == 4
    assert all("expected_issues" not in item["prompt"] for item in runtime.calls[:2])
    for certificate in result.validity_reading_1.certificates:
        for field_audit in certificate.field_audits:
            assert (
                "".join(item.exact_text for item in field_audit.clauses)
                == field_audit.exact_text
            )
            assert re.fullmatch(r"sha256:[0-9a-f]{64}", field_audit.exact_text_sha256)


def test_two_stage_semantics_are_invariant_to_report_and_expected_ids_and_order() -> (
    None
):
    first = minimal_input(report_count=2, expected_count=2)
    first_reports = (
        first.reports[0].model_copy(
            update={"claim": "artifact-supported report", "reason": "supported cause"}
        ),
        first.reports[1].model_copy(
            update={"claim": "artifact-refuted report", "reason": "refuted cause"}
        ),
    )
    first_expected = (
        first.expected_issues[0].model_copy(
            update={"summary": "directly matched obligation"}
        ),
        first.expected_issues[1].model_copy(
            update={"summary": "partially supported obligation"}
        ),
    )
    first = first.model_copy(
        update={"reports": first_reports, "expected_issues": first_expected}
    )
    second = first.model_copy(
        update={
            "reports": (
                first_reports[1].model_copy(update={"report_id": "R0042"}),
                first_reports[0].model_copy(update={"report_id": "R0017"}),
            ),
            "expected_issues": (
                first_expected[1].model_copy(
                    update={
                        "expected_id": "E0099",
                        "source_refs": ("expected:E0099",),
                    }
                ),
                first_expected[0].model_copy(
                    update={
                        "expected_id": "E0007",
                        "source_refs": ("expected:E0007",),
                    }
                ),
            ),
        }
    )

    def run(judge_input, run_id: str):
        validity_inputs = {
            report.report_id: build_validity_input(judge_input, report.report_id)
            for report in judge_input.reports
        }
        validity_by_report = {}
        for report in judge_input.reports:
            refuted = (
                {("claim", "C1")}
                if report.claim == "artifact-refuted report"
                else set()
            )
            validity_by_report[report.report_id] = validity_payload(
                validity_inputs[report.report_id], refuted=refuted
            )
        valid_report = next(
            report
            for report in judge_input.reports
            if report.claim == "artifact-supported report"
        )
        certificate = certificate_from_payload(
            validity_inputs[valid_report.report_id],
            validity_by_report[valid_report.report_id],
        )
        relation_input = build_relation_input(judge_input, certificate)
        matches = {
            expected.expected_id: (
                MatchStrength.FULL_MATCH
                if expected.summary == "directly matched obligation"
                else MatchStrength.PARTIAL_MATCH
            )
            for expected in judge_input.expected_issues
        }
        relation = relation_payload(relation_input, matches)
        ordered_validity = tuple(
            validity_by_report[report.report_id] for report in judge_input.reports
        )
        runtime = FakeRuntime(
            (*ordered_validity, *ordered_validity, relation, relation)
        )
        audit = AdapterAudit(
            source_format="x1v2_record",
            source_path=f"/fixture/{run_id}.json",
            source_hash="sha256:" + "6" * 64,
            report_id_map=tuple(
                AdapterIdMap(
                    anonymous_id=report.report_id,
                    original_id=report.claim,
                )
                for report in judge_input.reports
            ),
            expected_id_map=tuple(
                AdapterIdMap(
                    anonymous_id=expected.expected_id,
                    original_id=expected.summary,
                )
                for expected in judge_input.expected_issues
            ),
            projected_field_names=("report_id", "claim", "reason"),
            excluded_field_names=("arm", "witness_level", "d_level"),
            reason="Provider-free identity and ordering invariance fixture.",
            basis="The adapter mapping restores semantic fixture identities outside the provider.",
        )
        result = judge_pair(
            run_id=run_id,
            round_no=1,
            judge_input=judge_input,
            adapter_audit=audit,
            runtime=runtime,
            judge_code_commit="9" * 40,
        )
        normalized_relations = {
            (
                next(
                    report.claim
                    for report in judge_input.reports
                    if report.report_id == relation_row.report_id
                ),
                next(
                    expected.summary
                    for expected in judge_input.expected_issues
                    if expected.expected_id == relation_row.expected_id
                ),
            ): relation_row.match
            for relation_row in result.final_reading.relations
        }
        normalized_validity = {
            item.original_report_id: item.validity for item in result.report_outcomes
        }
        return result, normalized_relations, normalized_validity

    first_result, first_relations, first_validity = run(first, "invariance-first")
    second_result, second_relations, second_validity = run(
        second, "invariance-renamed-reordered"
    )

    assert first_relations == second_relations
    assert (
        first_validity
        == second_validity
        == {
            "artifact-supported report": ReportValidity.VALID_KNOWN,
            "artifact-refuted report": ReportValidity.INVALID,
        }
    )
    assert first_result.metrics == second_result.metrics
    assert (
        first_result.metrics.full_hit_count,
        first_result.metrics.supported_count,
        first_result.metrics.invalid_count,
    ) == (1, 2, 1)


def test_failed_validity_call_retains_billable_usage_and_cost() -> None:
    judge_input = minimal_input()

    class FailedRuntime:
        real_llm = True
        profile = "gpt-5.6-luna"
        config = SimpleNamespace(max_output_tokens=128_000)

        def call(self, **_kwargs):
            return SimpleNamespace(
                succeeded=False,
                response=None,
                usage=[
                    {
                        "model_call_id": "call-failed-schema",
                        "status": "success",
                        "model": "gpt-5.6-luna",
                        "input_tokens": 1000,
                        "output_tokens": 200,
                        "input_token_details": {
                            "cache_read": 800,
                            "cache_creation": 50,
                        },
                        "cost_counted": True,
                        "billing_disposition": "billable",
                    }
                ],
                attempts=[
                    {
                        "outer_attempt": 1,
                        "status": "failed",
                        "provider_error": False,
                        "billing_disposition": "billable",
                    }
                ],
                cost={"total_usd": 0.0125, "eligible": True},
                reason="Schema handling failed after a billable model response.",
                basis="Provider-free failure accounting fixture.",
            )

    with pytest.raises(JudgeExecutionFailure) as caught:
        judge_pair(
            run_id="fixture-failed-run",
            round_no=1,
            judge_input=judge_input,
            adapter_audit=adapter_audit(1, 1),
            runtime=FailedRuntime(),
            judge_code_commit="f" * 40,
        )
    receipt = caught.value.call_receipts[0]
    assert receipt.phase == "validity_primary_1"
    assert receipt.status == "failed"
    assert receipt.cost_usd == 0.0125
    assert receipt.usage[0].cache_read_input_tokens == 800
    assert receipt.usage[0].cache_write_input_tokens == 50


def test_prompts_and_generated_fixture_audit_language_are_english() -> None:
    non_ascii = re.compile(r"[^\x00-\x7f]")
    assert not non_ascii.search(VALIDITY_SYSTEM_PROMPT)
    assert not non_ascii.search(RELATION_SYSTEM_PROMPT)
    judge_input = minimal_input()
    validity_input = build_validity_input(judge_input, "R0001")
    payload = validity_payload(validity_input)
    generated_values = [
        payload["root_cause_cluster_key"],
        payload["validity_reason"],
        payload["validity_basis"],
    ] + [
        value
        for field_plan in validity_input.core_envelope.field_plans
        for row in payload[f"{field_plan.report_field.value}_audit"].values()
        for value in (row["assertion"], row["reason"], row["basis"])
    ]
    assert all(not non_ascii.search(value) for value in generated_values)


def test_prompts_state_general_typed_carrier_and_relation_scope_boundaries() -> None:
    normalized_validity = " ".join(VALIDITY_SYSTEM_PROMPT.split()).lower()
    normalized_relation = " ".join(RELATION_SYSTEM_PROMPT.split()).lower()

    assert "explicit region separator" in normalized_validity
    assert "child-local initial transitions do not establish sibling concurrency" in (
        normalized_validity
    )
    assert "independently actionable causal facet" in normalized_relation
    assert "need not also identify every coequal facet" in normalized_relation
    assert "never expand the report to a different defect" in normalized_relation
    assert (
        "initial transition inside a child composite is not a parent-level entry"
        in (normalized_relation)
    )
    assert (
        "unexpected reachable deadlock or no progress need not be stated verbatim"
        in (normalized_validity)
    )
    assert "without a typed predicate or formal witness can be valid" in (
        normalized_validity
    )
    forbidden_calibration_terms = {
        "pumpstate",
        "pumpcontrol",
        "r0001",
        "e0001",
        "0053",
    }
    assert forbidden_calibration_terms.isdisjoint(
        set(re.findall(r"[a-z0-9]+", normalized_validity + normalized_relation))
    )
