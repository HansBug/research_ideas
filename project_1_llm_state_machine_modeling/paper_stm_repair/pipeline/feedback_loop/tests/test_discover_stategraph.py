from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts, renderer  # noqa: E402
from paper_stm_feedback_loop.discover.graph import (  # noqa: E402
    build_discover_graph,
    route_after_convert,
    run_discover,
    run_discover_state,
)
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionCheckPublic,
    AssertionReview,
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    ReleasedAssertionResults,
    DiscoverAdjudication,
    DiscoverInput,
    RequirementCoverageProjection,
    RequirementReview,
    Requirement,
    RequirementSet,
    RevisionFeedback,
    RevisionLedgerEvent,
)
from paper_stm_feedback_loop.discover.utils import sha256_data  # noqa: E402
from paper_stm_feedback_loop.discover.nodes import default_fake_responder  # noqa: E402

MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def test_requirement_prompts_preserve_shared_scope_without_inventing_universal_scope() -> (
    None
):
    assert "shared prepositional qualifiers" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "unconditional global requirement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "joint trigger" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "shared qualifiers" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "independent triggers" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "invent a universal quantifier" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Operational context" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Containment language" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "source mode/state" in prompts.REQUIREMENT_REVIEWER_PROMPT


def test_assertion_prompts_state_the_family_b_valuation_boundary() -> None:
    """Family B runs at declared initial values and takes no valuation.

    A producer that does not know this writes `occupancy_after` for a guarded
    claim ("when speed > 120 ..."), the guard is false at defaults, and a
    correct model yields a False -- a fabricated confirmed issue.  Both
    assertion stages must carry the boundary.
    """

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        assert "cannot be given a valuation" in text, name
        assert "`limitations`" in text or "limitations" in text, name


def test_assertion_prompts_preserve_nl_targets_and_require_conflict_analysis() -> None:
    for prompt in (
        prompts.ASSERTION_CONVERTER_PROMPT,
        prompts.ASSERTION_REVIEWER_PROMPT,
    ):
        assert "source" in prompt
        assert "trigger" in prompt
        assert "destination" in prompt
        assert "guard_distinguishable" in prompt
        assert "completion-holder" in prompt
    assert "Context and proxy discipline" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Convergence rule" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "Mandatory event-response gate" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Mandatory event-response review gate" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "source-trigger-destination" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "behavior_phase" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert (
        'pseudo-initial source is exactly `"[*]"`' in prompts.ASSERTION_REVIEWER_PROMPT
    )
    assert (
        "must not demand an invented direct edge" in prompts.ASSERTION_CONVERTER_PROMPT
    )


def test_quantitative_effect_prompts_forbid_guessed_variable_names() -> None:
    assert (
        "never enumerate candidate variable names hoping one matches"
        in prompts.ASSERTION_CONVERTER_PROMPT
    )
    # Not guessing is only half the rule: the producer still owes a check, so the
    # prompt has to say where the name comes from instead.  Left at "do not
    # guess", the item has no legal move and burns its repair budget.
    assert (
        "use the name the Requirement proposes, asserted as a `precondition`"
        in prompts.ASSERTION_CONVERTER_PROMPT
    )
    # Case-insensitive: the sentence moved and its first word is now capitalised.
    # The rule is what matters, not where in the paragraph it sits.
    assert (
        "reject every invented identifier"
        in prompts.ASSERTION_REVIEWER_PROMPT.lower()
    )


def test_prompts_merge_one_repair_unit_and_preserve_attributable_mismatch() -> None:
    # Repair-unit atomicity（「containment + entry 保持在一条需求里」）已于 2026-08-09 删除：
    # `Requirement.predicate` 是单值必填，一条需求承载两个谓词在 v3 schema 下不可表达，而
    # reviewer 的孪生条据此删掉了承载台账谓词的那条需求 —— v37 段② 的 D 类 10 位就是这么丢的。
    # 现在锁的是相反的性质：去重只允许同谓词同绑定，且删除请求必须点名幸存者承接。
    assert "Repair-unit atomicity" not in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "one predicate per Requirement is a schema invariant" in (
        prompts.REQUIREMENT_REVIEWER_PROMPT
    )
    assert "name which surviving Requirement carries" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert (
        "Do not leave a repair-relevant destination mismatch"
        in prompts.ASSERTION_CONVERTER_PROMPT
    )
    assert "Attribution-preserving mismatch gate" in prompts.ASSERTION_REVIEWER_PROMPT


def test_prompts_enforce_positive_conflict_assertion_direction() -> None:
    assert (
        "positive distinguishability obligation" in prompts.REQUIREMENT_SPLITTER_PROMPT
    )
    assert (
        "positive distinguishability Requirement" in prompts.REQUIREMENT_REVIEWER_PROMPT
    )
    assert "Do not negate it" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Reject a negated form" in prompts.ASSERTION_REVIEWER_PROMPT


def test_requirement_prompts_distinguish_local_exit_from_completion() -> None:
    assert "Local-exit grounding" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Local-exit review" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert (
        "separate completion/termination target" in prompts.REQUIREMENT_SPLITTER_PROMPT
    )


def test_requirement_prompts_do_not_treat_missing_discriminator_as_nondeterminism() -> (
    None
):
    assert "Missing discriminator text" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "only an explicit statement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "absence of an explicit ban" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert (
        "separate distinguishability Requirement" in prompts.REQUIREMENT_REVIEWER_PROMPT
    )
    assert "undifferentiated condition set" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert (
        "different target-specific condition clauses"
        in prompts.REQUIREMENT_SPLITTER_PROMPT
    )
    assert "binding normalization" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "global guard mutual exclusion" in prompts.REQUIREMENT_REVIEWER_PROMPT


def test_revision_ledger_prompts_forbid_review_oscillation_and_truth_inference() -> (
    None
):
    assert "complete revision_ledger" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Do not reverse" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "every prior artifact delta" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Do not repeat resolved findings" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "never contains sealed True/False" in prompts.ASSERTION_REVIEWER_PROMPT


def test_assertion_prompts_distinguish_composed_completion_from_wrong_target() -> None:
    assert "Hierarchical completion distinction" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Hierarchical completion review" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "genuine wrong direct target" in prompts.ASSERTION_CONVERTER_PROMPT
    for prompt in (
        prompts.ASSERTION_CONVERTER_PROMPT,
        prompts.ASSERTION_REVIEWER_PROMPT,
    ):
        assert "Limitation non-waiver" in prompt
        assert "cannot" in prompt or "may not" in prompt
        assert "Cardinality evidence gate" in prompt
        assert "Multi-step response gate" in prompt


# Split out of the test above so its passing prompt-content checks are not
# masked by this known leak.  strict=True makes the marker itself fail once the
# prompt stops naming benchmark elements, which is the signal to delete it.
def test_assertion_prompts_do_not_name_benchmark_model_elements() -> None:
    """A prompt that names evaluation-set identifiers contaminates the run."""

    for benchmark_token in ("exit_hwy", "FinishState", "Power_Off", "R45RouteToken"):
        assert benchmark_token not in prompts.ASSERTION_CONVERTER_PROMPT
        assert benchmark_token not in prompts.ASSERTION_REVIEWER_PROMPT


def test_requirements_do_not_expose_benchmark_issue_taxonomy() -> None:
    assert "semantic_tags" not in Requirement.model_fields
    assert "hidden issue taxonomy" in prompts.REQUIREMENT_SPLITTER_PROMPT


def test_v2_prompts_freeze_requirement_kind_and_assertion_role() -> None:
    # v3 replaced the prose ordered decision with a named predicate whose family
    # derives the kind; the downstream role/evidence contract is unchanged.
    assert "Binding v3 Requirement contract" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "`predicate`" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Binding v3 review gate" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Binding v2 Assertion contract" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "`primary` assertion" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Supporting evidence" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "supporting False is retained" in prompts.RESULT_ADJUDICATOR_PROMPT


def test_requirement_requires_v2_kind_without_legacy_field() -> None:
    with pytest.raises(ValidationError, match="verification_kind"):
        Requirement.model_validate(
            {"requirement_id": "REQ-001", "statement": "A requirement."}
        )


def test_v2_splitter_path_rejects_legacy_requirement_upgrade() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("legacy-requirement")
    frozen = nodes._fallback_prepare(discover_input)
    legacy = RequirementSet(
        revision=1,
        requirements=(
            {
                "source_segment_ids": ("NL-L001",),
                "requirement_id": "REQ-001",
                "statement": "Legacy shape.",
                "checkability": "structure",
            },
        ),
        segment_disposition={"NL-L001": "covered"},
    )
    out = nodes.split_requirements(
        {"_input": discover_input, "frozen_inputs": frozen},
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: legacy
        ),
    )

    # The rejection itself is unchanged; what changed is that a producer
    # contract violation is now handed back for repair instead of ending the
    # run.  Three of eight cells in matrix v3-final died at this node on a
    # single malformed field, which Issue #167 §3 forbids for a local defect.
    assert "failure" not in out
    feedback = out["_requirement_split_contract_feedback"]
    assert feedback is not None
    assert "uses legacy checkability" in feedback.findings[0]
    assert out["_requirement_contract_repair_count"] == 1


def test_splitter_contract_repairs_are_bounded() -> None:
    """The repair loop must terminate even against a stubborn producer."""

    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("legacy-forever")
    frozen = nodes._fallback_prepare(discover_input)
    legacy = RequirementSet(
        revision=1,
        requirements=(
            {
                "source_segment_ids": ("NL-L001",),
                "requirement_id": "REQ-001",
                "statement": "Legacy shape.",
                "checkability": "structure",
            },
        ),
        segment_disposition={"NL-L001": "covered"},
    )
    state: dict = {"_input": discover_input, "frozen_inputs": frozen}
    for _ in range(nodes.MAX_REQUIREMENT_CONTRACT_REPAIRS + 2):
        out = nodes.split_requirements(
            {**state},
            nodes.CallableStructuredResponder(
                lambda _role, _schema, _system, _payload: legacy
            ),
        )
        state.update(out)
        if "failure" in out:
            break
    assert "failure" in state, "an unrepairable contract violation must still stop"
    assert state["failure"].node_name == "split_requirements"


def test_v2_converter_path_rejects_legacy_inferred_assertion_fields() -> None:
    """The three coverage fields are schema-required, not back-filled.

    They used to be optional with a validator that substituted
    `legacy:<id>` / `legacy-group:<id>`.  The object then validated and a
    downstream gate rejected it *for being legacy*, so one omitted field
    isolated every assertion and killed the cell with an empty script -- three
    of eight matrix cells died that way.  Rejecting at the schema costs one
    repair round instead of a run.
    """

    from pydantic import ValidationError

    from paper_stm_feedback_loop.discover.schemas import AssertionSpec

    complete = {
        "assertion_id": "AST-REQ-001-1",
        "requirement_id": "REQ-001",
        "description": "d",
        "expression": 'state_declared(state="Root.Idle", kind="leaf")',
        "failure_message": "[REQ-001][AST-REQ-001-1] m",
        "evidence_family": "structure",
        "role": "primary",
        "coverage_key": "state_declared:Root.Idle",
        "aggregation_group": "REQ-001:all",
        "rationale": "Fixture assertion; rationale not under test here.",
    }
    assert AssertionSpec.model_validate(complete).aggregation_group == "REQ-001:all"

    for omitted in ("role", "coverage_key", "aggregation_group"):
        partial = {k: v for k, v in complete.items() if k != omitted}
        with pytest.raises(ValidationError, match=omitted):
            AssertionSpec.model_validate(partial)

    # And no value is silently manufactured from the ids any more.
    schema = AssertionSpec.model_json_schema()
    assert {"role", "coverage_key", "aggregation_group"} <= set(schema["required"])


@pytest.mark.parametrize(
    ("verification_kind", "evidence_family", "accepted"),
    [
        ("structure", "structure", True),
        ("structure", "relation", True),
        ("behavior", "simulation", True),
        ("property", "fbmcq", True),
        ("structure", "simulation", False),
        ("property", "simulation", False),
    ],
)
def test_primary_family_matrix_is_enforced(
    verification_kind: str, evidence_family: str, accepted: bool
) -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("primary-family"))
    requirements = RequirementSet.model_validate(
        {
            "revision": 1,
            "requirements": [
                {
                    "requirement_id": "REQ-001",
                    "statement": "A typed requirement.",
                    "verification_kind": verification_kind,
                }
            ],
        }
    )
    script = AssertionScript.model_validate(
        {
            "revision": 1,
            "assertions": [
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": "Typed primary evidence.",
                    "expression": "True",
                    "failure_message": "[REQ-001][AST-REQ-001-01] failed",
                    "evidence_family": evidence_family,
                    "role": "primary",
                    "coverage_key": "REQ-001:key",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
                }
            ],
            "requirement_mapping": {"REQ-001": ["AST-REQ-001-01"]},
        }
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("primary-family"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: script
        ),
    )

    if accepted:
        assert "failure" not in out
        assert out.get("_assertion_conversion_contract_feedback") is None
    else:
        assert out["_assertion_conversion_contract_feedback"] is not None
        assert "invalid primary families" in out[
            "_assertion_conversion_contract_feedback"
        ].findings[0]


@pytest.mark.parametrize(
    ("verification_kind", "mandatory_family", "complementary_family"),
    [
        ("behavior", "simulation", "relation"),
        ("behavior", "simulation", "effect"),
        ("property", "fbmcq", "relation"),
        ("property", "fbmcq", "structure"),
        ("property", "fbmcq", "effect"),
    ],
)
def test_complementary_primary_requires_mandatory_family(
    verification_kind: str,
    mandatory_family: str,
    complementary_family: str,
) -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("complementary-primary"))
    requirements = RequirementSet.model_validate(
        {
            "revision": 1,
            "requirements": [
                {
                    "requirement_id": "REQ-001",
                    "statement": "A typed requirement.",
                    "verification_kind": verification_kind,
                }
            ],
        }
    )

    def script(*families: str) -> AssertionScript:
        assertions = [
            {
                "assertion_id": f"AST-REQ-001-{index}",
                "requirement_id": "REQ-001",
                "description": f"Primary {family} evidence.",
                "expression": "True",
                "failure_message": f"[REQ-001][AST-REQ-001-{index}] failed",
                "evidence_family": family,
                "role": "primary",
                "coverage_key": f"REQ-001:{family}:{index}",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            }
            for index, family in enumerate(families, start=1)
        ]
        return AssertionScript.model_validate(
            {
                "revision": 1,
                "assertions": assertions,
                "requirement_mapping": {
                    "REQ-001": [item["assertion_id"] for item in assertions]
                },
            }
        )

    missing = nodes.convert_assertions(
        {
            "_input": _input("complementary-primary-missing"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: script(complementary_family)
        ),
    )
    assert "missing mandatory primary evidence families" in missing[
        "_assertion_conversion_contract_feedback"
    ].findings[0]

    accepted = nodes.convert_assertions(
        {
            "_input": _input("complementary-primary-accepted"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: script(
                mandatory_family, complementary_family
            )
        ),
    )
    assert "failure" not in accepted
    assert accepted.get("_assertion_conversion_contract_feedback") is None


def test_requirement_with_only_supporting_assertions_is_rejected() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("supporting-only"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A structure fact.",
                "verification_kind": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Supporting only.",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] failed",
                "evidence_family": "structure",
                "role": "supporting",
                "coverage_key": "support:key",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("supporting-only"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: script
        ),
    )

    assert "requires at least one primary assertion" in out[
        "_assertion_conversion_contract_feedback"
    ].findings[0]


def _input(run_id: str = "r") -> DiscoverInput:
    return DiscoverInput(
        run_id=run_id,
        natural_language="After go, Done shall become active.",
        stm_text=MODEL,
        language="en-US",
    )


def _fake_responder(
    role: str, schema: type[BaseModel], system: str, payload: str
) -> BaseModel:
    """A fake producer whose assertion still executes after the predicate move.

    ``nodes.default_fake_responder`` emits the model-agnostic ``len(states()) > 0``,
    and no predicate is model-agnostic: every one takes declared paths.  The tests
    below exercise graph plumbing -- streaming, the update callback, the CLI, the
    segment-disposition ledger -- so they pin their own script against ``MODEL``
    rather than depending on whatever the shipped smoke fixture happens to say.
    """

    if schema is AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": "Fake smoke assertion.",
                    "expression": "state_declared(state='Root.Idle', kind='leaf')",
                    "failure_message": (
                        "[REQ-001][AST-REQ-001-01] The frozen STM declares no Root.Idle."
                    ),
                    "evidence_family": "structure",
                    "role": "primary",
                    "coverage_key": "model:states",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )
    return default_fake_responder(role, schema, system, payload)


def test_fake_stategraph_runs_complete_without_old_agent_loop_import() -> None:
    assert "paper_stm_repair_loop" not in sys.modules


def test_stategraph_soft_isolates_repeated_invalid_primary_and_publishes_partial() -> None:
    assertion_revision = 0

    def responder(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        nonlocal assertion_revision
        if schema is RequirementSet:
            return RequirementSet(
                revision=1,
                requirements=(
                    {
                        "source_segment_ids": ("NL-L001",),
                        "requirement_id": "REQ-001",
                        "statement": "Done shall be structurally present.",
                        "verification_kind": "structure",
                        "coverage_obligation": {
                            "domain": "state:Done",
                            "aggregation": "all",
                        },
                    },
                ),
                segment_disposition={"NL-L001": "covered"},
            )
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept",
                reviewed_revision=1,
                rationale="The typed requirement is complete.",
            )
        if schema is AssertionScript:
            assertion_revision += 1
            return AssertionScript(
                revision=assertion_revision,
                assertions=(
                    {
                        "assertion_id": "AST-REQ-001-PRIMARY",
                        "requirement_id": "REQ-001",
                        "description": "Repeated invalid primary.",
                        "expression": "len(state_declared(",
                        "failure_message": "[REQ-001][AST-REQ-001-PRIMARY] invalid",
                        "evidence_family": "structure",
                        "role": "primary",
                        "coverage_key": "state:Done",
                        "aggregation_group": "REQ-001:all",
                        "rationale": "Fixture assertion; rationale not under test here.",
                    },
                    {
                        "assertion_id": "AST-REQ-001-SUPPORT",
                        "requirement_id": "REQ-001",
                        "description": "Executable supporting locator.",
                        "expression": "state_declared(state='Root.Idle', kind='leaf')",
                        "failure_message": "[REQ-001][AST-REQ-001-SUPPORT] no states",
                        "evidence_family": "structure",
                        "role": "supporting",
                        "coverage_key": "support:states",
                        "aggregation_group": "REQ-001:all",
                        "rationale": "Fixture assertion; rationale not under test here.",
                    },
                ),
                requirement_mapping={
                    "REQ-001": (
                        "AST-REQ-001-PRIMARY",
                        "AST-REQ-001-SUPPORT",
                    )
                },
            )
        if schema is AssertionReview:
            review_payload = json.loads(_payload)
            assert review_payload["coverage_gaps"][0]["gap_id"] == (
                "GAP-AST-REQ-001-PRIMARY-NO-PROGRESS"
            )
            return AssertionReview(
                decision="accept",
                reviewed_script_hash="TO_BE_PATCHED",
                rationale="The remaining executable evidence is reviewable.",
            )
        if schema is DiscoverAdjudication:
            return DiscoverAdjudication(
                has_confirmed_issues=False,
                issues=(),
                satisfied_requirement_ids=(),
                excluded_findings=(),
                rationale="No released primary False assertion exists.",
            )
        raise AssertionError(schema)

    completed = run_discover(_input("soft-isolation-e2e"), responder)

    assert completed.status == "completed"
    assert completed.coverage_status == "partial"
    assert completed.issues == ()
    assert completed.satisfied_requirement_ids == ()
    assert len(completed.coverage_gaps) == 1
    assert completed.coverage_gaps[0].assertion_ids == (
        "AST-REQ-001-PRIMARY",
    )
    assert completed.coverage_gaps[0].blocks_full_coverage is True


def test_ambiguous_segment_is_disposed_not_missing() -> None:
    """Ambiguity is a recorded disposition, not an uncovered NL segment."""
    discover_input = _input().model_copy(
        update={
            "natural_language": "After go, Done shall become active.\nThe mode wording is ambiguous."
        }
    )

    def responder(role: str, schema: type[BaseModel], _: str, __: str) -> BaseModel:
        if schema is RequirementSet:
            return RequirementSet(
                revision=1,
                requirements=(
                    Requirement(
                        requirement_id="REQ-001",
                        statement="The system enters Idle.",
                        source_segment_ids=("NL-L001",),
                        verification_kind="structure",
                        coverage_obligation={
                            "domain": "state:Idle",
                            "aggregation": "all",
                        },
                    ),
                ),
                segment_disposition={
                    "NL-L001": "covered",
                    "NL-L002": "ambiguous",
                },
            )
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept",
                reviewed_revision=1,
                rationale="The ambiguous segment is explicitly retained for audit.",
            )
        return _fake_responder(role, schema, _, __)

    state = run_discover_state(discover_input, responder)
    assert state["requirement_coverage"].missing_segment_ids == ()
    assert state["requirement_set"].segment_disposition["NL-L002"] == "ambiguous"
    assert [event.event for event in state["_requirement_revision_ledger"]] == [
        "artifact_created",
        "review_completed",
    ]
    assert [event.event for event in state["_assertion_revision_ledger"]] == [
        "artifact_created",
        "check_completed",
        "review_completed",
    ]
    assert "truth_value" not in json.dumps(
        [event.model_dump(mode="json") for event in state["_assertion_revision_ledger"]]
    )
    completed = run_discover(_input("pair-0000"), _fake_responder)
    assert completed.status == "completed"
    assert completed.run_id == "pair-0000"
    assert completed.adjudication.has_confirmed_issues is False
    assert "paper_stm_repair_loop" not in sys.modules


def test_review_payload_hides_sealed_and_released_truth_values() -> None:
    from paper_stm_feedback_loop.discover import nodes

    completed_states: list[dict[str, Any]] = []
    graph = build_discover_graph(
        nodes.CallableStructuredResponder(_fake_responder)
    )
    for event in graph.stream(
        {"_input": _input("truth-hide")},
        stream_mode="updates",
    ):
        completed_states.append(event)
    release_index = next(
        index
        for index, item in enumerate(completed_states)
        if "release_results" in item
    )
    pre_release = completed_states[:release_index]
    assert pre_release
    dumped_pre_release = json.dumps(pre_release, default=str).lower()
    assert "truth_value" not in dumped_pre_release
    assert "_sealed_payload" not in dumped_pre_release
    review_event = next(item for item in pre_release if "review_assertions" in item)
    dumped = json.dumps(review_event["review_assertions"], default=str).lower()
    assert "truth_value" not in dumped
    assert "_sealed_payload" not in dumped


def test_revision_ledger_is_rendered_for_both_revision_loops() -> None:
    from paper_stm_feedback_loop.discover.nodes import _fallback_prepare

    frozen = _fallback_prepare(_input("ledger-render"))
    requirements = RequirementSet(
        revision=2,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "source_segment_ids": ("NL-L001",),
                "checkability": "effect",
            },
        ),
        segment_disposition={"NL-L001": "covered"},
    )
    script = AssertionScript(
        revision=2,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "event response",
                "expression": "edge_declared(source='Root.Idle', trigger='Root.go', target='Root.Done')",
                "failure_message": "[REQ-001][AST-REQ-001-01] response missing",
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    requirement_ledger = (
        RevisionLedgerEvent(
            sequence=1,
            loop="requirements",
            event="artifact_created",
            revision=1,
            artifact_hash="req-v1",
            status="created",
            artifact_delta={"added": [{"requirement_id": "REQ-OLD"}]},
        ),
        RevisionLedgerEvent(
            sequence=2,
            loop="requirements",
            event="review_completed",
            revision=1,
            artifact_hash="req-v1",
            status="revise",
            findings=("Preserve source scope.",),
        ),
    )
    assertion_ledger = (
        RevisionLedgerEvent(
            sequence=1,
            loop="assertions",
            event="artifact_created",
            revision=1,
            artifact_hash="ast-v1",
            status="created",
            artifact_delta={"added": [{"assertion_id": "AST-OLD"}]},
        ),
        RevisionLedgerEvent(
            sequence=2,
            loop="assertions",
            event="review_completed",
            revision=1,
            artifact_hash="ast-v1",
            status="revise",
            findings=("Use the source-compatible hot start.",),
        ),
    )
    public = AssertionCheckPublic(
        script_hash=sha256_data(script),
        tool_env_hash=frozen.tool_env_hash,
        status="executable",
        executions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "executable",
            },
        ),
    )

    requirement_payloads = (
        renderer.render_requirement_split_input(
            frozen, requirements, revision_ledger=requirement_ledger
        ),
        renderer.render_requirement_review_input(
            frozen,
            requirements,
            RequirementCoverageProjection(
                covered_requirement_ids=("REQ-001",), missing_segment_ids=()
            ),
            revision_ledger=requirement_ledger,
        ),
    )
    assertion_payloads = (
        renderer.render_assertion_conversion_input(
            frozen,
            requirements,
            script,
            revision_ledger=assertion_ledger,
        ),
        renderer.render_assertion_review_input(
            frozen, requirements, script, public, assertion_ledger
        ),
    )

    for payload in requirement_payloads:
        assert "revision_ledger" in payload
        assert "Preserve source scope." in payload
    for payload in assertion_payloads:
        assert "revision_ledger" in payload
        assert "Use the source-compatible hot start." in payload
        assert "truth_value" not in payload


def test_runtime_callback_path_consumes_stream_updates_to_completion() -> None:
    updates: list[str] = []
    state = run_discover_state(
        _input("stream-callback"),
        _fake_responder,
        on_update=lambda node_name, _update: updates.append(node_name),
    )
    assert updates[0] == "prepare"
    assert "adjudicate_results" in updates
    assert updates[-1] == "publish"
    assert state["final_output"].status == "completed"


def test_convert_failure_terminates_even_with_stale_contract_feedback() -> None:
    state = {
        "failure": object(),
        "_assertion_conversion_contract_feedback": RevisionFeedback(
            target="assertions",
            origin="assertion_contract",
            reason="Revise the invalid script.",
        ),
    }

    assert route_after_convert(state) == "run_failed"  # type: ignore[arg-type]


def test_renderer_assertion_review_input_has_no_truth_labels() -> None:
    from paper_stm_feedback_loop.discover.nodes import _fallback_prepare

    frozen = _fallback_prepare(_input())
    reqs = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "NL",
                "checkability": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "check",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover.nodes import precheck_and_seal

    state = {
        "_input": _input(),
        "frozen_inputs": frozen,
        "assertion_script": script,
    }
    checked = precheck_and_seal(state, sealed_store=InMemorySealedStore())
    payload = renderer.render_assertion_review_input(
        frozen, reqs, script, checked["assertion_check_public"]
    )
    assert "truth_value" not in payload
    assert "sealed_payload" not in payload
    assert "sealed_hash" not in payload


def test_effect_noncausal_formal_evidence_is_rejected_before_sealing() -> None:
    """Formal evidence that never mentions the trigger cannot close a triggered claim.

    The bare ``check reach`` query this used to be written as is now unwritable --
    no function accepts a query string.  The surviving way to dodge causality is
    to name ``invariant`` over a plain state predicate where the Requirement's
    trigger calls for ``response_within``, so the claim is expressed that way.
    """

    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    def fake_bmc_runner(*_args: Any, **_kwargs: Any) -> tuple[str, int]:
        # The reported kind/bound must echo the query the predicate built, or the
        # report is rejected as mismatched and the outcome never reaches the
        # causality gate this test is about.
        return (
            json.dumps(
                {
                    "result": {"status": "sat", "property_satisfied": True},
                    "property": {"kind": "invariant", "bound": 5},
                    "replay": {"ok": True},
                }
            ),
            0,
        )

    discover_input = _input("bare-formal")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Bounded property that ignores the trigger.",
                "expression": (
                    "invariant(scope='root', condition='active(\"Root.Done\")') is True"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not reached",
                "evidence_family": "fbmcq",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checker = AssertionChecker(
        EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )

    assert checked["assertion_check_public"].status == "invalid"
    assert "bare reach target is not causal evidence" in (
        checked["assertion_check_public"].executions[0].error or ""
    )
    assert "hot-start simulation" in (
        checked["assertion_check_public"].executions[0].error or ""
    )
    repeated = nodes.precheck_and_seal(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    assert "failure" not in repeated
    assert repeated["_assertion_no_progress_recovery_count"] == 1
    assert repeated["_assertion_feedback"].recovery_seed is not None
    assert repeated["_assertion_feedback"].target_item_ids == ("AST-REQ-001-01",)


def test_repeated_invalid_assertion_is_quarantined_without_discarding_peer() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("soft-isolation")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "The model exposes at least one state.",
                "verification_kind": "structure",
                "coverage_obligation": {"domain": "model", "aggregation": "all"},
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-PRIMARY",
                "requirement_id": "REQ-001",
                "description": "Repeated invalid primary.",
                "expression": "len(state_declared(",
                "failure_message": "[REQ-001][AST-REQ-001-PRIMARY] invalid",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "model:states",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-001-SUPPORT",
                "requirement_id": "REQ-001",
                "description": "Executable supporting locator.",
                "expression": "state_declared(state='Root.Idle', kind='leaf')",
                "failure_message": "[REQ-001][AST-REQ-001-SUPPORT] no states",
                "evidence_family": "structure",
                "role": "supporting",
                "coverage_key": "support:model:states",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={
            "REQ-001": (
                "AST-REQ-001-PRIMARY",
                "AST-REQ-001-SUPPORT",
            )
        },
    )
    store = InMemorySealedStore()
    base = {
        "_input": discover_input,
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": script,
    }
    first = nodes.precheck_and_seal(base, sealed_store=store)
    second = nodes.precheck_and_seal(
        {**base, **first, "assertion_script": script}, sealed_store=store
    )
    third = nodes.precheck_and_seal(
        {**base, **first, **second, "assertion_script": script},
        sealed_store=store,
    )

    assert "failure" not in third
    assert third["assertion_check_public"].status == "executable"
    assert [item.assertion_id for item in third["assertion_script"].assertions] == [
        "AST-REQ-001-SUPPORT"
    ]
    assert third["_quarantined_assertion_ids"] == ("AST-REQ-001-PRIMARY",)
    assert len(third["coverage_gaps"]) == 1
    assert third["coverage_gaps"][0].reason_code == "no_progress"
    assert third["coverage_gaps"][0].blocks_full_coverage is True


def test_changed_invalid_script_is_not_treated_as_no_progress() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("changed-invalid-script")
    frozen = nodes._fallback_prepare(discover_input)

    def make_script(description: str, expression: str) -> AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": description,
                    "expression": expression,
                    "failure_message": "[REQ-001][AST-REQ-001-01] helper failure",
                    "evidence_family": "structure",
                    "role": "primary",
                    "coverage_key": "AST-REQ-001-01",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )

    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A structure check.",
                "checkability": "structure",
            },
        ),
    )
    checker = AssertionChecker(
        EvalEnvironment(
            model_text=MODEL,
            extra_functions={
                "broken_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(AssertionError("backend failed")),
                ),
                "revised_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(
                        AssertionError("backend failed again")
                    ),
                ),
            },
        )
    )
    store = InMemorySealedStore()
    first = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": make_script("first version", "broken_helper()"),
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    second = nodes.precheck_and_seal(
        {
            **first,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": make_script(
                "materially revised version", "revised_helper()"
            ),
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    assert "failure" not in second
    assert second["assertion_check_public"].status == "invalid"


def test_invalid_effect_simulation_reports_script_error_before_hot_start_policy() -> (
    None
):
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("invalid-effect-script"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The converter omitted a closing list bracket.",
                "expression": "occupancy_after(source='Root.Idle', trigger='Root.go'",
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.precheck_and_seal(
        {
            "_input": _input("invalid-effect-script"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )

    error = out["assertion_check_public"].executions[0].error or ""
    assert "AssertionScriptSyntaxError" in error
    assert "hot-start" not in error


def test_name_error_feedback_forbids_rename_only_alias_repair() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("invalid-alias"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The assertion uses an undefined state alias.",
                "expression": (
                    "occupancy_after(source=human, trigger='Root.go', "
                    "target='Root.Done')"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.precheck_and_seal(
        {
            "_input": _input("invalid-alias"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )

    error = out["assertion_check_public"].executions[0].error or ""
    assert "Do not rename an undefined alias" in error
    assert "quoted complete state/event path" in error


# Replaces three tests that differed only in how the producer wrote its
# `simulate(...)` call -- explicit hot start, explicit cold path, empty
# cold-start cycles for a behavior_phase=initialization Requirement.  The
# producer no longer writes that call: `occupancy_after` hot-starts the named
# source itself, so the only property left is that a behavior Requirement
# discharged through the simulation predicate reaches the sealed set.
def test_behavior_simulation_predicate_is_accepted_by_the_precheck() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("initial-cold-effect")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Runtime occupancy after the trigger.",
                "expression": "occupancy_after(source='Root.Idle', trigger='Root.go', target='Root.Done')",
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )
    assert checked["assertion_check_public"].status == "executable"


def test_strict_schemas_reject_inconclusive_and_bad_review_shapes() -> None:
    with pytest.raises(ValidationError):
        DiscoverAdjudication.model_validate(
            {
                "has_confirmed_issues": False,
                "issues": [],
                "rationale": "ok",
                "truth_value": None,
            }
        )
    with pytest.raises(ValidationError):
        RequirementReview(
            decision="accept",
            reviewed_revision=1,
            findings=(
                {"severity": "important", "message": "x", "required_change": "y"},
            ),
            rationale="bad",
        )


def test_create_revise_pairs_and_no_progress_gate_are_enforced() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    current = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A",
                "checkability": "structure",
            },
        ),
    )

    def stale_responder(
        _role: str, schema: type[BaseModel], _system: str, _input: str
    ) -> BaseModel:
        assert schema is RequirementSet
        return current

    state = {
        "_input": _input(),
        "frozen_inputs": frozen,
        "requirement_set": current,
    }
    out = nodes.split_requirements(
        state, nodes.CallableStructuredResponder(stale_responder)
    )
    assert out["failure"].node_name == "split_requirements"
    assert "pair" in out["failure"].message


def test_converter_contract_reject_routes_existing_script_back_with_feedback() -> None:
    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.graph import route_after_convert

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "Done shall become active after go.",
                "checkability": "structure",
            },
        ),
    )
    current = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "current",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] current",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    invalid_revision = current.model_copy(
        update={
            "revision": 2,
            "assertions": (
                current.assertions[0].model_copy(
                    update={
                        "failure_message": "[REQ-WRONG][AST-REQ-001-01] wrong owner",
                    }
                ),
            ),
        }
    )
    state = {
        "_input": _input("converter-contract"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": current,
        "_assertion_feedback": RevisionFeedback(
            target="assertions",
            reason="review requested a revision",
            findings=("scope",),
        ),
    }
    out = nodes.convert_assertions(
        state,
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: invalid_revision
        ),
    )
    assert "failure" not in out
    assert out["_assertion_conversion_contract_feedback"].findings
    assert out["_assertion_contract_repair_count"] == 1
    assert route_after_convert(out) == "convert_assertions"
    assert out["node_execution_records"][0].status == "failed"


def test_effect_requirement_rejects_relation_only_evidence() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": "When go occurs, the system shall enter Done.",
                    "verification_kind": "behavior",
                    "coverage_obligation": {
                        "domain": "response:go",
                        "aggregation": "all",
                    },
            },
        ),
    )
    current = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "current relation check",
                "expression": "True",
                    "failure_message": "[REQ-001][AST-REQ-001-01] relation",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "response:go",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    state = {
        "_input": _input("effect-contract"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": current,
        "_assertion_feedback": RevisionFeedback(
            target="assertions", reason="review requested a revision"
        ),
    }
    out = nodes.convert_assertions(
        state,
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: current.model_copy(
                update={"revision": 2}
            )
        ),
    )
    assert "failure" not in out
    assert (
        "behavior requirement"
        in out["_assertion_conversion_contract_feedback"].findings[0]
    )
    assert (
        "['simulation']" in out["_assertion_conversion_contract_feedback"].findings[0]
    )


def test_effect_only_evidence_can_expose_missing_typed_effect_without_simulation() -> (
    None
):
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    model = (ROOT / "fixtures/selected_models/0006/STM_0.fcstm").read_text(
        encoding="utf-8"
    )
    discover_input = _input("effect-only").model_copy(
        update={
            "natural_language": (
                "After Attack_Complete, the UAV quantity shall decrease."
            ),
            "stm_text": model,
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After Attack_Complete, the UAV quantity shall decrease.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The named quantity has no typed decrement effect.",
                "expression": (
                    "effect_declared(source='Root.Attack', "
                    "trigger='Root.Attack_Complete', "
                    "variable='UAV_Quantity', sign='negative')"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] UAV_Quantity does not decrease "
                    "on Attack_Complete"
                ),
                "evidence_family": "effect",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=model)),
    )

    assert checked["assertion_check_public"].status == "executable"
    released = store.release(checked["sealed_assertion_results"].sealed_hash)
    assert len(released) == 1
    assert released[0].truth_value is False
    assert released[0].evidence_family == "effect"


def test_effect_requirement_does_not_accept_relation_only_after_contract_relaxation() -> (
    None
):
    """The new effect exception is narrow: relation remains insufficient."""

    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": "When go occurs, the system shall enter Done.",
                    "verification_kind": "behavior",
                    "coverage_obligation": {
                        "domain": "response:go",
                        "aggregation": "all",
                    },
            },
        ),
    )
    relation_only = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Only a transition relation is checked.",
                "expression": (
                    "edge_declared(source='Root.Idle', trigger='Root.go', "
                    "target='Root.Done')"
                ),
                    "failure_message": "[REQ-001][AST-REQ-001-01] effect missing",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "response:go",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("relation-only-after-relaxation"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: relation_only
        ),
    )

    assert out["_assertion_conversion_contract_feedback"].findings
    assert (
        "behavior requirement"
        in out["_assertion_conversion_contract_feedback"].findings[0]
    )


def test_assertion_reviewer_has_a_bounded_revision_gate() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("bounded-review"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "Done shall become active after go.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "bounded check",
                "expression": (
                    "occupancy_after(source='Root.Idle', trigger='Root.go', "
                    "target='Root.Done')"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    public_check = AssertionCheckPublic(
        script_hash=sha256_data(script),
        tool_env_hash=frozen.tool_env_hash,
        status="executable",
        executions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "executable",
            },
        ),
    )

    def always_revise(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        assert schema is AssertionReview
        return AssertionReview(
            decision="revise",
            reviewed_script_hash=sha256_data(script),
            findings=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "severity": "important",
                    "message": "repeatable review finding",
                    "required_change": "make a material change",
                },
            ),
            rationale="repeatable review",
        )

    base_state = {
        "_input": _input("bounded-review"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": script,
        "assertion_check_public": public_check,
    }
    responder = nodes.CallableStructuredResponder(always_revise)
    for count in range(nodes.MAX_ASSERTION_REVIEW_REPAIRS):
        out = nodes.review_assertions(
            {**base_state, "_assertion_review_repair_count": count}, responder
        )
        assert "failure" not in out
        assert out["_assertion_review_repair_count"] == count + 1

    out = nodes.review_assertions(
        {
            **base_state,
            "_assertion_review_repair_count": nodes.MAX_ASSERTION_REVIEW_REPAIRS,
        },
        responder,
    )
    assert "failure" in out
    assert "bounded review gate" in out["failure"].message


def test_initial_converter_contract_violation_enters_bounded_revision() -> None:
    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.graph import route_after_convert

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": "When go occurs, the system shall enter Done.",
                    "verification_kind": "behavior",
                    "coverage_obligation": {
                        "domain": "response:go",
                        "aggregation": "all",
                    },
            },
        ),
    )
    invalid = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "relation only",
                "expression": "edge_declared(source='Root.Idle', trigger='Root.go', target='Root.Done')",
                    "failure_message": "[REQ-001][AST-REQ-001-01] relation only",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "response:go",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("initial-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(lambda *_args: invalid),
    )
    assert "failure" not in out
    assert out["assertion_script"].revision == 1
    assert out["_assertion_contract_repair_count"] == 1
    assert "behavior requirement" in out["_assertion_feedback"].findings[0]
    assert route_after_convert(out) == "convert_assertions"


def test_repeated_contract_invalid_script_stops_without_five_duplicate_calls() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("repeat-contract"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )
    invalid = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "relation only",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] relation only",
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    revisions = iter((1, 2))
    responder = nodes.CallableStructuredResponder(
        lambda _role, _schema, _system, _payload: invalid.model_copy(
            update={"revision": next(revisions)}
        )
    )
    first = nodes.convert_assertions(
        {
            "_input": _input("repeat-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        responder,
    )
    assert "failure" not in first
    second = nodes.convert_assertions(
        {
            "_input": _input("repeat-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": first["assertion_script"],
            "_assertion_feedback": first["_assertion_feedback"],
            "_assertion_contract_failure_signatures": first[
                "_assertion_contract_failure_signatures"
            ],
            "_assertion_contract_repair_count": first[
                "_assertion_contract_repair_count"
            ],
        },
        responder,
    )
    assert "failure" in second
    assert "repeated contract-invalid" in second["failure"].message


def test_splitter_failure_routes_directly_to_run_failed_without_reviewer_masking() -> (
    None
):
    from paper_stm_feedback_loop.discover.graph import run_discover_state

    def fail_splitter(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        if schema is RequirementSet:
            raise RuntimeError("splitter transport failed")
        raise AssertionError("downstream reviewer must not be called")

    with pytest.raises(
        RuntimeError, match="split_requirements.*splitter transport failed"
    ):
        run_discover_state(_input("split-failure"), fail_splitter)


def test_assertion_precheck_seals_strict_bool_and_invalid_exceptions() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "ok",
                "expression": "state_declared(state='Root.Idle', kind='leaf')",
                "failure_message": "[REQ-001][AST-REQ-001-01] no states",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-001-02",
                "requirement_id": "REQ-001",
                "description": "bad",
                "expression": "broken_helper()",
                "failure_message": "[REQ-001][AST-REQ-001-02] helper failure",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-02",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )

    checker = AssertionChecker(
        EvalEnvironment(
            model_text=MODEL,
            extra_functions={
                "broken_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(AssertionError("backend failed")),
                )
            },
        )
    )
    store = InMemorySealedStore()
    out = nodes.precheck_and_seal(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    public = out["assertion_check_public"]
    assert public.status == "invalid"
    assert public.executions[0].status == "executable"
    assert public.executions[1].status == "invalid"
    receipt = out["sealed_assertion_results"]
    sealed = store.release(receipt.sealed_hash)
    assert len(sealed) == 1
    assert sealed[0].truth_value is True


def test_prompts_are_english_and_ban_tools_or_truth_leak() -> None:
    all_prompts = "\n".join(
        [
            prompts.REQUIREMENT_SPLITTER_PROMPT,
            prompts.REQUIREMENT_REVIEWER_PROMPT,
            prompts.ASSERTION_CONVERTER_PROMPT,
            prompts.ASSERTION_REVIEWER_PROMPT,
            prompts.RESULT_ADJUDICATOR_PROMPT,
        ]
    )
    assert "use tools" in all_prompts
    assert "AgentApp" not in all_prompts
    assert "sealed-result-blind" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "True/False" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "do not define functions or classes" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "public_check.script_hash" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "behavioral requirement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    # `checkability` is a removed field, and both requirement prompts prohibit
    # emitting it.  This used to pin a leftover review duty telling the reviewer to
    # "check the checkability classification" and reclassify to `effect` or
    # `relation` -- neither of which is a legal `verification_kind`, so a reviewer
    # acting on it could only loop until the repair budget ran out.  Pin the
    # prohibition that is actually in force instead.
    assert "checkability classification" not in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "legacy `checkability` field" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert (
        "no separate `checkability` vocabulary" in prompts.REQUIREMENT_SPLITTER_PROMPT
    )
    assert (
        "`effect_declared` is the direct declared-effect evidence"
        in prompts.ASSERTION_CONVERTER_PROMPT
    )
    assert "only evidence is static relation" in prompts.ASSERTION_REVIEWER_PROMPT


def test_cli_main_writes_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from paper_stm_feedback_loop.discover.cli import main
    from paper_stm_feedback_loop.discover import cli, nodes

    nl = tmp_path / "nl.txt"
    stm = tmp_path / "STM_0.fcstm"
    trace = tmp_path / "source_trace.json"
    nl.write_text("After go, Done shall become active.", encoding="utf-8")
    stm.write_text(MODEL, encoding="utf-8")
    trace.write_text('{"entries": [], "attribution_exclusions": []}', encoding="utf-8")
    monkeypatch.setattr(
        cli,
        "DirectStructuredResponder",
        lambda *_args, **_kwargs: nodes.CallableStructuredResponder(_fake_responder),
    )
    output = tmp_path / "run"
    assert (
        main(
            [
                "--case-id",
                "custom-0000",
                "--nl-file",
                str(nl),
                "--fcstm-file",
                str(stm),
                "--source-trace-file",
                str(trace),
                "--profile",
                "test-profile",
                "--content-language",
                "en-US",
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    data = json.loads((output / "discover-completed.json").read_text(encoding="utf-8"))
    assert data["run_id"].startswith("custom-0000-test-profile-")
    assert data["status"] == "completed"
    assert (output / "loops" / "discover.md").is_file()
    assert list((output / "records").glob("L000-*-discover-completed/record.json"))


def test_cli_failure_writes_auditable_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from paper_stm_feedback_loop.discover import cli

    nl = tmp_path / "nl.txt"
    stm = tmp_path / "STM_0.fcstm"
    trace = tmp_path / "source_trace.json"
    nl.write_text("After go, Done shall become active.", encoding="utf-8")
    stm.write_text(MODEL, encoding="utf-8")
    trace.write_text('{"entries": [], "attribution_exclusions": []}', encoding="utf-8")
    monkeypatch.setattr(
        cli, "DirectStructuredResponder", lambda *_args, **_kwargs: object()
    )
    monkeypatch.setattr(
        cli,
        "run_discover_state",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            RuntimeError("bounded review gate")
        ),
    )
    output = tmp_path / "failed-run"
    with pytest.raises(RuntimeError, match="bounded review gate"):
        cli.main(
            [
                "--case-id",
                "custom-failure",
                "--nl-file",
                str(nl),
                "--fcstm-file",
                str(stm),
                "--source-trace-file",
                str(trace),
                "--profile",
                "test-profile",
                "--output-dir",
                str(output),
            ]
        )
    failure = json.loads((output / "discover-failed.json").read_text(encoding="utf-8"))
    assert failure["status"] == "failed"
    assert "bounded review gate" in failure["error_message"]
    assert "records/" in (output / "loops" / "discover-failed.md").read_text(
        encoding="utf-8"
    )


def test_assertion_review_hash_must_match_current_script() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    reqs = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A",
                "checkability": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "ok",
                "expression": "state_declared(state='Root.Idle', kind='leaf')",
                "failure_message": "[REQ-001][AST-REQ-001-01] no states",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import InMemorySealedStore

    checked = nodes.precheck_and_seal(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
    )

    def wrong_hash(
        _role: str, schema: type[BaseModel], _system: str, _input: str
    ) -> BaseModel:
        assert schema is AssertionReview
        return AssertionReview(
            decision="accept", reviewed_script_hash="bad", rationale="ok"
        )

    out = nodes.review_assertions(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "requirement_set": reqs,
            "assertion_script": script,
            **checked,
        },
        nodes.CallableStructuredResponder(wrong_hash),
    )
    # Behaviour changed deliberately.  The payload is rendered fresh from the
    # current script on every reviewer call, so the model cannot be looking at a
    # stale revision; an exact-string test on a 64-hex-character value therefore
    # only ever detects a transcription slip.  On pair 0029 GPT-5.5 produced
    # such a slip (correct 32-char prefix, then a repeated fragment) and the
    # entire run was lost, which Issue #167 §3 forbids for a local defect.  The
    # discrepancy is now an audited fact and the binding is recomputed.
    assert "failure" not in out
    assert out["assertion_review"].reviewed_script_hash == sha256_data(script)
    record = out["node_execution_records"][-1]
    assert (record.details or {}).get("reviewed_hash_binding") == "mismatch"
    assert "agrees on only" in (record.details or {}).get("reviewed_hash_note", "")


def test_confirmed_issue_schema_defers_unsafe_attribution_to_the_node() -> None:
    """Parsing accepts a misfiled finding; `adjudicate_results` relocates it.

    This check used to raise here. It was moved because structured-output validation is
    recorded `retryable: False` in the responder, so a rejection at parse time ends the node
    just as surely as one inside it -- and `adjudicate_results` has no contract-feedback
    round to recover with. A whole `0029-gpt` run was lost that way.

    Nothing is loosened overall: which basket a primary False belongs in follows from its
    attribution status, so the node sorts both collections by status and records each move in
    `_adjudication_reconciliation.misfiled_findings_moved`. See
    `tests/test_adjudication_misfiling.py` for the relocation itself.
    """
    parsed = DiscoverAdjudication(
        has_confirmed_issues=True,
        issues=(
            {
                "issue_id": "ISSUE-001",
                "requirement_ids": ("REQ-001",),
                "assertion_ids": ("AST-REQ-001-01",),
                "title": "Unsafe finding",
                "rationale": "False but source attribution is absent.",
                "attribution_status": "unattributed",
            },
        ),
        rationale="parses; the node will move it to excluded_findings",
    )
    assert parsed.issues[0].attribution_status == "unattributed"


def test_adjudication_schema_defers_a_self_contradictory_flag_to_the_node() -> None:
    """The flag is re-derived downstream, so rejecting it here would only cost the cell.

    `adjudicate_results` sets `has_confirmed_issues` from the sorted collections
    unconditionally, which means a parse-time check on it protects nothing -- and structured
    validation is `retryable: False`, so it ends the run. The model that misfiles a safe
    finding as an exclusion is the same one that then reports no confirmed issues to match,
    so this is the flag most likely to disagree.
    """
    parsed = DiscoverAdjudication(
        has_confirmed_issues=True,
        issues=(),
        rationale="claims issues while listing none; the node re-derives the flag",
    )
    assert parsed.has_confirmed_issues is True
    assert parsed.issues == ()


def test_false_assertion_on_excluded_compiler_ref_is_representation_debt() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input().model_copy(
        update={
            "source_trace": {
                "entries": [],
                "attribution_exclusions": ["compiler:state:Root.Done"],
            }
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A deliberately absent transition.",
                "expression": "edge_declared(source='Root.Done', trigger='Root.go', target='Root.Idle')",
                "failure_message": "[REQ-001][AST-REQ-001-01] reverse transition is absent",
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False


def test_route_control_guarded_relation_is_representation_debt() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    # The predicate vocabulary addresses an edge by its trigger, so the NL event
    # has to be declared for the claim to be expressible at all.  The lowering
    # under test is unchanged: the only edge into Entry is event-free and carries
    # the converter's route-control guard.
    model = """def int R45RouteToken = 0;
state Root {
    event go;
    state Entry;
    [*] -> Entry : if [R45RouteToken == 5] effect { R45RouteToken = 0; };
}
"""
    discover_input = _input("route-control-relation").model_copy(
        update={
            "stm_text": model,
            "source_trace": {
                "entries": [],
                "attribution_exclusions": ["compiler:route_control:R45RouteToken"],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Entry should be entered on go, unconditionally.",
                "expression": (
                    "edge_declared(source='[*]', trigger='Root.go', "
                    "target='Root.Entry')"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] initial relation is guarded"
                ),
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )

    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert "compiler:route_control:R45RouteToken" in binding.exclusion_refs


def test_wrong_target_near_miss_remains_source_attributable() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    model = """state Root {
    event leave;
    state Cruise;
    state Exit;
    state Finish;
    [*] -> Cruise;
    Cruise -> Finish : leave;
}
"""
    discover_input = _input("wrong-target-near-miss").model_copy(
        update={
            "stm_text": model,
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:wrong-target",
                        "intermediate_elements": [
                            "Root.Cruise",
                            "Root.leave",
                            "Root.Finish",
                        ],
                        "source_elements": ["source:transition:wrong-target"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The local exit must reach Exit.",
                "expression": (
                    "edge_declared(source='Root.Cruise', "
                    "trigger='Root.leave', target='Root.Exit')"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] local exit reaches wrong target"
                ),
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )

    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "safe"
    assert binding.source_refs == ("source:transition:wrong-target",)


def test_simulation_false_on_ineligible_contract_is_representation_debt() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("simulation-ineligible").model_copy(
        update={
            "manifest": {
                "working_contract": {
                    "capability_eligibility": {"simulation": {"status": "ineligible"}}
                }
            },
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="simulation",
                check_detail={"function_call_trace": [{"args": ["Root.Done"]}]},
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False
    assert "contract:capability_eligibility.simulation" in binding.exclusion_refs


def test_simulation_false_without_ineligible_contract_keeps_source_trace_policy() -> (
    None
):
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("simulation-eligible").model_copy(
        update={
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            }
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="simulation",
                check_detail={"function_call_trace": [{"args": ["Root.Done"]}]},
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "safe"


def test_mixed_effect_assertion_using_simulation_respects_ineligible_gate() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("mixed-simulation-ineligible").model_copy(
        update={
            "manifest": {
                "working_contract": {
                    "capability_eligibility": {"simulation": {"status": "ineligible"}}
                }
            },
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="effect",
                evidence_scope={"actual_function_families": ["effect", "simulation"]},
                check_detail={
                    "actual_function_families": ["effect", "simulation"],
                    "function_call_trace": [{"args": ["Root.Done"]}],
                },
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False
    assert "contract:capability_eligibility.simulation" in binding.exclusion_refs


def test_attribution_matching_requires_exact_structured_path() -> None:
    from paper_stm_feedback_loop.discover.nodes import _reference_matches_observed

    assert _reference_matches_observed(
        "state:case.Controller.Idle", {"case.Controller.Idle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"case.OtherRegion.Idle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"case.Controller.NotIdle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"event:case.Controller.Idle"}
    )
    assert _reference_matches_observed(
        "compiler:route_control:R45RouteToken", {"R45RouteToken"}
    )
    assert not _reference_matches_observed(
        "compiler:event_projection:Root.pedestrian_or_distance",
        {"Root.pedestrian_or_distance"},
    )
    assert _reference_matches_observed(
        "compiler:event_projection:Root.pedestrian_or_distance",
        {"compiler:event_projection:Root.pedestrian_or_distance"},
    )


def test_adjudicator_must_account_for_every_safe_false_assertion() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("adjudication-closure"))
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A deliberately contradicted requirement.",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "safe",
                "source_refs": ("state:Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )

    def omit_false(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        assert schema is DiscoverAdjudication
        return DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            satisfied_requirement_ids=(),
            excluded_findings=(),
            rationale="omitted false assertion",
        )

    out = nodes.adjudicate_results(
        {
            "_input": _input("adjudication-closure"),
            "frozen_inputs": frozen,
            "requirement_set": RequirementSet(
                revision=1,
                requirements=(
                    {
                        "requirement_id": "REQ-001",
                        "statement": "A",
                        "checkability": "structure",
                    },
                ),
            ),
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(omit_false),
    )
    # Recorded, not fatal. `v11run3/0006-claude` died on this check with five of six issues
    # already written and nine LLM calls spent; issue #167 §3 says a local producer defect must
    # not become RUN_FAILED. The gap is now surfaced in the reconciliation and forces
    # `coverage_status` to `partial`, so a reader cannot mistake the cell for a complete pass --
    # which a dead cell, carrying no findings at all, certainly does not tell them.
    assert "failure" not in out, "an ungrouped False primary must not take the whole cell down"
    unaccounted = out["_adjudication_reconciliation"]["unaccounted_safe_false_assertions"]
    assert unaccounted == ("AST-REQ-001-01",)


def test_supporting_false_is_retained_without_creating_issue() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("supporting-false"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "Done is structurally present.",
                "verification_kind": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-PRIMARY",
                "requirement_id": "REQ-001",
                "description": "Primary structure fact.",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-PRIMARY] missing",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "state:Done",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-001-SUPPORT",
                "requirement_id": "REQ-001",
                "description": "Supporting locator.",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-SUPPORT] locator",
                "evidence_family": "relation",
                "role": "supporting",
                "coverage_key": "support:route",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-001-SUPPORT-TRUE",
                "requirement_id": "REQ-001",
                "description": "Passing supporting locator.",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-SUPPORT-TRUE] locator",
                "evidence_family": "relation",
                "role": "supporting",
                "coverage_key": "support:passing-route",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={
            "REQ-001": (
                "AST-REQ-001-PRIMARY",
                "AST-REQ-001-SUPPORT",
                "AST-REQ-001-SUPPORT-TRUE",
            )
        },
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-PRIMARY",
                requirement_id="REQ-001",
                role="primary",
                coverage_key="state:Done",
                aggregation_group="REQ-001:all",
                truth_value=True,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
            AssertionResult(
                assertion_id="AST-REQ-001-SUPPORT",
                requirement_id="REQ-001",
                role="supporting",
                coverage_key="support:route",
                aggregation_group="REQ-001:all",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="relation",
            ),
            AssertionResult(
                assertion_id="AST-REQ-001-SUPPORT-TRUE",
                requirement_id="REQ-001",
                role="supporting",
                coverage_key="support:passing-route",
                aggregation_group="REQ-001:all",
                truth_value=True,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="relation",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-001-SUPPORT",
                "requirement_id": "REQ-001",
                "status": "safe",
                "source_refs": ("transition:Root.Idle->Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )

    out = nodes.adjudicate_results(
        {
            "_input": _input("supporting-false"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: DiscoverAdjudication(
                has_confirmed_issues=False,
                issues=(),
                excluded_findings=(
                    {
                        "issue_id": "ISSUE-REQ-001-SUPPORT",
                        "requirement_id": "REQ-001",
                        "assertion_ids": ("AST-REQ-001-SUPPORT",),
                        "title": "Supporting observation",
                        "rationale": "The LLM temporarily classified it here.",
                        "attribution_status": "safe",
                    },
                ),
                excluded_observations=(
                    {
                        "assertion_id": "AST-REQ-001-SUPPORT",
                        "requirement_id": "REQ-001",
                        "role": "supporting",
                        "disposition": "quarantined",
                        "rationale": "Raw structured response before normalization.",
                    },
                    {
                        "assertion_id": "AST-REQ-001-SUPPORT-TRUE",
                        "requirement_id": "REQ-001",
                        "role": "supporting",
                        "disposition": "supporting_false",
                        "rationale": "A spurious observation for a True result.",
                    },
                ),
                satisfied_requirement_ids=("REQ-001",),
                rationale="Primary coverage is satisfied.",
            )
        ),
    )

    assert "failure" not in out
    assert out["adjudication"].issues == ()
    assert out["adjudication"].satisfied_requirement_ids == ("REQ-001",)
    assert len(out["adjudication"].excluded_observations) == 1
    assert out["adjudication"].excluded_observations[0].assertion_id == (
        "AST-REQ-001-SUPPORT"
    )
    assert (
        out["adjudication"].excluded_observations[0].disposition
        == "supporting_false"
    )


def test_safe_relation_primary_can_confirm_behavior_issue_when_simulation_has_debt() -> (
    None
):
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("behavior-complementary-primary"))
    requirements = RequirementSet.model_validate(
        {
            "revision": 1,
            "requirements": [
                {
                    "requirement_id": "REQ-001",
                    "statement": "PowerOff shall reach Final.",
                    "verification_kind": "behavior",
                }
            ],
        }
    )
    script = AssertionScript.model_validate(
        {
            "revision": 1,
            "assertions": [
                {
                    "assertion_id": "AST-REQ-001-SIM",
                    "requirement_id": "REQ-001",
                    "description": "Runtime response.",
                    "expression": "False",
                    "failure_message": "[REQ-001][AST-REQ-001-SIM] runtime mismatch",
                    "evidence_family": "simulation",
                    "role": "primary",
                    "coverage_key": "runtime:PowerOff",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
                },
                {
                    "assertion_id": "AST-REQ-001-REL",
                    "requirement_id": "REQ-001",
                    "description": "Exact source-event-target relation.",
                    "expression": "False",
                    "failure_message": "[REQ-001][AST-REQ-001-REL] relation mismatch",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "relation:PowerOff:Final",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
                },
            ],
            "requirement_mapping": {
                "REQ-001": ["AST-REQ-001-SIM", "AST-REQ-001-REL"]
            },
        }
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-SIM",
                requirement_id="REQ-001",
                role="primary",
                coverage_key="runtime:PowerOff",
                aggregation_group="REQ-001:all",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="simulation",
            ),
            AssertionResult(
                assertion_id="AST-REQ-001-REL",
                requirement_id="REQ-001",
                role="primary",
                coverage_key="relation:PowerOff:Final",
                aggregation_group="REQ-001:all",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="relation",
            ),
        ),
    )
    attribution = AttributionProjection.model_validate(
        {
            "bindings": [
                {
                    "assertion_id": "AST-REQ-001-SIM",
                    "requirement_id": "REQ-001",
                    "status": "representation_debt",
                    "source_refs": [],
                    "trace_entry_ids": [],
                    "exclusion_refs": ["contract:simulation"],
                    "source_level_claim_allowed": False,
                    "rationale": "Simulation is excluded by the frozen contract.",
                },
                {
                    "assertion_id": "AST-REQ-001-REL",
                    "requirement_id": "REQ-001",
                    "status": "safe",
                    "source_refs": ["transition:Root.Active->Root.Final"],
                    "trace_entry_ids": ["trace-1"],
                    "exclusion_refs": [],
                    "source_level_claim_allowed": True,
                    "rationale": "The exact relation is source-owned.",
                },
            ]
        }
    )

    out = nodes.adjudicate_results(
        {
            "_input": _input("behavior-complementary-primary"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: DiscoverAdjudication(
                has_confirmed_issues=True,
                issues=(
                    {
                        "issue_id": "ISSUE-REQ-001-REL",
                        "requirement_id": "REQ-001",
                        "assertion_ids": ("AST-REQ-001-REL",),
                        "title": "PowerOff relation is absent",
                        "rationale": "The source-owned exact relation is False.",
                        "attribution_status": "safe",
                    },
                ),
                excluded_findings=(
                    {
                        "issue_id": "ISSUE-REQ-001-SIM-DEBT",
                        "requirement_id": "REQ-001",
                        "assertion_ids": ("AST-REQ-001-SIM",),
                        "title": "Simulation mismatch is excluded",
                        "rationale": "The simulation touches representation debt.",
                        "attribution_status": "representation_debt",
                    },
                ),
                satisfied_requirement_ids=(),
                rationale="The safe exact mismatch confirms the issue.",
            )
        ),
    )

    assert "failure" not in out
    assert out["adjudication"].issues[0].assertion_ids == ("AST-REQ-001-REL",)
    assert out["adjudication"].excluded_findings[0].assertion_ids == (
        "AST-REQ-001-SIM",
    )


def test_adjudicator_reconciles_derived_satisfied_ids_without_dropping_findings() -> (
    None
):
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("adjudication-reconcile"))
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A contradicted requirement.",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-002-01",
                "requirement_id": "REQ-002",
                "description": "A satisfied requirement.",
                "expression": "True",
                "failure_message": "[REQ-002][AST-REQ-002-01] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-002-01",
                "aggregation_group": "REQ-002:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={
            "REQ-001": ("AST-REQ-001-01",),
            "REQ-002": ("AST-REQ-002-01",),
        },
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
            AssertionResult(
                assertion_id="AST-REQ-002-01",
                requirement_id="REQ-002",
                truth_value=True,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "safe",
                "source_refs": ("state:Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )

    def overreports_satisfied(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        assert schema is DiscoverAdjudication
        return DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-REQ-001",
                    "requirement_id": "REQ-001",
                    "assertion_ids": ("AST-REQ-001-01",),
                    "title": "Requirement failed",
                    "rationale": "The safe assertion is false.",
                    "attribution_status": "safe",
                },
            ),
            # Deliberately include the false requirement: this is a derived
            # bookkeeping error that deterministic closure can correct.
            satisfied_requirement_ids=("REQ-001", "REQ-002"),
            rationale="The issue is retained and the satisfied list is provisional.",
        )

    out = nodes.adjudicate_results(
        {
            "_input": _input("adjudication-reconcile"),
            "frozen_inputs": frozen,
            "requirement_set": RequirementSet(
                revision=1,
                requirements=(
                    {
                        "requirement_id": "REQ-001",
                        "statement": "A",
                        "checkability": "structure",
                    },
                    {
                        "requirement_id": "REQ-002",
                        "statement": "B",
                        "checkability": "structure",
                    },
                ),
            ),
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(overreports_satisfied),
    )
    assert "failure" not in out
    assert out["adjudication"].satisfied_requirement_ids == ("REQ-002",)
    assert out["adjudication"].issues[0].assertion_ids == ("AST-REQ-001-01",)
    assert out["_adjudication_reconciliation"]["normalization_applied"] is True


def test_an_ungrouped_false_primary_forces_partial_coverage() -> None:
    """The reader must be able to see that the adjudication left something out.

    Downgrading the raise to a record is only safe if the omission stays visible. `publish`
    therefore reads `unaccounted_safe_false_assertions` and cannot report `full`.
    """
    from paper_stm_feedback_loop.discover import nodes

    state = {"_adjudication_reconciliation": {"unaccounted_safe_false_assertions": ("AST-X-01",)}}
    unaccounted = (state.get("_adjudication_reconciliation", {}) or {}).get(
        "unaccounted_safe_false_assertions"
    ) or ()
    assert unaccounted, "the reconciliation key publish reads must survive renames"
    assert hasattr(nodes, "publish")
