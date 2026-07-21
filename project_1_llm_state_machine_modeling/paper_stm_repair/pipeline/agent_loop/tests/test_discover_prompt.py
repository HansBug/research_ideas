from __future__ import annotations

import re

import pytest

from paper_stm_repair_loop.prompts.discover import system_prompt, user_prompt


PROMPT_ZH = system_prompt("zh-CN")
PROMPT_EN = system_prompt("en-US")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _ordered(prompt: str, markers: list[str]) -> None:
    positions = [prompt.find(marker) for marker in markers]
    assert min(positions) >= 0, [m for m, p in zip(markers, positions) if p < 0]
    assert positions == sorted(positions)


def test_prompt_keeps_one_top_level_agent_and_controller_issue_agnostic():
    flat = _flat(PROMPT_ZH)
    assert "only top-level LLM Agent" in flat
    assert "one `AgentApp.run`" in flat
    assert "Controller never predicts an issue" in flat
    assert "never supplies a fixed defect taxonomy" in flat
    assert "never edits `STM_0`" in flat
    assert "loop stays on FCSTM" in flat
    assert "Issue categories are open-world" in flat
    assert "Do not invent, require, or organize the run around D01-D12" in flat


def test_prompt_exposes_review_as_peer_tool_and_forbids_hidden_surfaces():
    line = next(
        line
        for line in PROMPT_ZH.splitlines()
        if "only Agent-callable tools are exactly" in line
    )
    tools = re.findall(r"`([a-z_]+)`", line)
    assert tools == [
        "read_fcstm_guide",
        "read_fbmcq_guide",
        "read_task",
        "register_coverage_plan",
        "revise_assertion",
        "query_model",
        "eval_assert",
        "observe_trace",
        "lookup_source_trace",
        "review_discovery_coverage",
    ]
    flat = _flat(PROMPT_ZH)
    assert "peer business tool, at the same level as `eval_assert`" in flat
    assert "There is no shell, arbitrary Python" in flat
    assert "hidden reference/gold" in flat


def test_prompt_separates_controller_worklist_units_roots_and_assertions():
    flat = _flat(PROMPT_ZH)
    for marker in (
        "`InputSegment` is a deterministic NL slice",
        "`CoverageRequirement` is a hard positive obligation",
        "Create exactly one atomic NL `CoverageUnit`",
        "exactly one positive `PropositionRootNode`",
        "one or more required `LogicalAssertion` chains",
    ):
        assert marker in flat
    assert "SourceFact inventory is an exploration pool" in flat
    assert "not a requirement to create one assertion per model fact" in flat
    assert "not a claim of 100% coverage" in flat
    assert "context_only" in PROMPT_ZH
    assert "representation_boundary" in PROMPT_ZH


def test_prompt_orders_review_gated_workflow():
    _ordered(
        PROMPT_ZH,
        [
            "1. **Read semantics and frozen task.",
            "2. **Explore the major behavior surface.",
            "3. **Build the complete atomic plan.",
            "4. **Register the plan.",
            "5. **Execute all latest assertions.",
            "6. **Revise inconclusive or weak assertions.",
            "7. **Run the independent coverage review.",
            "8. **Inspect final projection and attribution.",
            "9. **Submit exactly once.",
        ],
    )
    flat = _flat(PROMPT_ZH)
    assert "Do not stop after finding the first issue" in flat
    assert "read every `required_action`" in flat
    assert "complete every listed `recommended_step`" in flat
    assert "before calling the review tool again" in flat
    assert "Only after Controller closure and current review pass" in flat


def test_prompt_requires_same_strength_positive_assertions():
    flat = _flat(PROMPT_ZH)
    assert "`True` means the model satisfies the Root" in flat
    assert "`False` means it contradicts the Root" in flat
    assert "Preserve source, trigger, guard/condition, target, quantity" in flat
    assert "Event existence alone cannot prove a destination" in flat
    assert "Do not strengthen" in flat
    assert "do not weaken it to `bool(effects(...))`" in flat
    assert "at least two distinct initialized progressing simulations" in flat
    assert "One invariant or existential `exists_always` path" in flat
    assert "exact `assert` string -> chain/Root/Unit map" in flat
    assert "semantically distinct direct predicates" in flat
    assert "Never evade uniqueness with whitespace" in flat
    assert "minimum sufficient evidence route" in flat
    assert "More tool families do not automatically make a claim stronger" in flat
    assert "Use FBMCQ only when a bounded temporal property is necessary" in flat
    assert "Do not add formal or simulation assertions merely to decorate" in flat


def test_prompt_forbids_deterministic_anti_gaming_patterns():
    flat = _flat(PROMPT_ZH)
    assert "complete stable model-definition scope" in flat
    assert "filtering or enumerating exactly N known names" in flat
    assert "literal lists, or membership predicates" in flat
    assert "sentinel/probe/dummy/nonexistent/future-model/only-for-test" in flat
    assert "open-ended `effect_deltas(...)` route" in flat
    assert "Natural-language rationales must not smuggle in anti-evidence" in flat
    assert "filtered-cardinality" in flat


def test_prompt_preserves_cycle_and_fbmcq_semantics():
    flat = _flat(PROMPT_ZH)
    assert "Every literal `simulate(cycles=...)` begins with `[]`" in flat
    assert "Reusing an event in a later cycle is legal" in flat
    assert "consumed-event accounting is not a one-use rule" in flat
    assert "`simulate(...).final.is_ended is True`" in flat
    assert "do not call `is_active` after the terminating event" in flat
    assert "call `read_fbmcq_guide`" in flat
    assert "replay-mismatched results are inconclusive" in flat


def test_prompt_makes_review_pass_current_and_actionable():
    flat = _flat(PROMPT_ZH)
    assert "current `review_discovery_coverage` result with `passed=true`" in flat
    assert "mandatory again after any subsequent revision/evaluation" in flat
    assert "required_actions" in PROMPT_ZH
    assert "related IDs, risk, recommended tools, concrete changes" in flat
    assert "independently reviews every Segment, Requirement, behavior SourceFact" in flat
    assert "reviewed_state_fingerprint" in PROMPT_ZH
    assert "There is no Agent-declared partial-success path" in flat


def test_prompt_requires_feedback_driven_progress_without_external_takeover():
    flat = _flat(PROMPT_ZH)
    assert "No external controller will invent" in flat
    assert "Never repeat the same tool with semantically unchanged arguments" in flat
    assert "For `mandatory_tool_rejected`, call the returned `required_tool`" in flat
    assert "Do not disguise repetition with whitespace" in flat
    assert "close every item" in flat
    assert "`submit_discovery` schema validation returns `field_mismatches`" in flat
    assert "never respond by shortening the outcome" in flat


def test_prompt_converges_exploration_into_the_registered_plan():
    flat = _flat(PROMPT_ZH)
    assert "not a checklist for enumerating the inventory" in flat
    assert "one stable provisional Root ID" in flat
    assert "never mint suffix variants or new IDs" in flat
    assert "do not run a model-wide pre-plan trace sweep" in flat
    assert "the next semantic step for that proposition is to incorporate" in flat
    assert "one distinct unresolved condition" in flat
    assert "Keep the payload complete but concise" in flat
    assert "cite only SourceFacts actually consumed by assertions" in flat
    assert "use one-sentence rationales" in flat


def test_prompt_language_policy_and_unknown_language():
    assert "Run content language is `zh-CN`" in _flat(PROMPT_ZH)
    assert "in `zh-CN`" in _flat(PROMPT_ZH)
    assert "Run content language is `en-US`" in _flat(PROMPT_EN)
    assert "in `en-US`" in _flat(PROMPT_EN)
    for prompt in (PROMPT_ZH, PROMPT_EN):
        assert "Keep schema keys, enum values, IDs" in _flat(prompt)
        assert "in English" in _flat(prompt)
    with pytest.raises(ValueError, match="unsupported Discover content language"):
        system_prompt("fr-FR")


def test_user_prompt_withholds_content_and_requires_review_pass():
    text = user_prompt(
        {
            "stage": "B-discover",
            "loop_no": 0,
            "model": {
                "model_id": "STM_0",
                "content": "secret fcstm",
                "model_sha256": "abc",
            },
            "current_records": {"nl": {"content": "secret nl"}},
        }
    )
    assert "task content withheld" in text
    assert "secret fcstm" not in text
    assert "secret nl" not in text
    assert "read_fcstm_guide first, then read_task" in text
    assert "review_discovery_coverage after its prerequisites are closed" in text
    assert "Follow actionable findings until it passes" in text
    assert "returning submit_discovery" in text
