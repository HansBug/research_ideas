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
        "read_task",
        "inspect_model",
        "register_coverage_plan",
        "eval_assert",
        "revise_assertion",
        "review_discovery_coverage",
        "query_model",
        "observe_trace",
        "lookup_source_trace",
        "read_fbmcq_guide",
    ]
    flat = _flat(PROMPT_ZH)
    assert "peer business tool, at the same level as `eval_assert`" in flat
    assert "There is no shell, arbitrary Python" in flat
    assert "hidden reference/gold" in flat


def test_non_formal_prompt_matches_hidden_formal_capability():
    prompt = system_prompt("en-US", formal_profile=False)
    line = next(
        item
        for item in prompt.splitlines()
        if "only Agent-callable tools are exactly" in item
    )
    assert "`read_fbmcq_guide`" not in line
    assert "read_fbmcq_guide and fbmcq are unavailable" in prompt
    assert "Do not compose, register, or recommend formal assertions" in prompt


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
    assert "SourceFact inventory is a frozen evidence pool" in flat
    assert "not a requirement to create one assertion per model fact" in flat
    assert "not a claim of 100% coverage" in flat
    assert "context_only" in PROMPT_ZH
    assert "representation_boundary" in PROMPT_ZH


def test_prompt_orders_review_gated_workflow():
    _ordered(
        PROMPT_ZH,
        [
            "1. **Read once.",
            "2. **Plan from the frozen task.",
            "3. **Register or perform targeted pre-plan investigation.",
            "4. **Evaluate.",
            "5. **Repair evidence only when needed.",
            "6. **Review.",
            "7. **Attribute contradictions.",
            "8. **Submit.",
        ],
    )
    flat = _flat(PROMPT_ZH)
    assert "Continue through the complete finite registered worklist" in flat
    assert "Evaluate each remaining missing expression exactly once first" in flat
    assert "after every registered latest assertion has received its first evaluation" in flat
    assert "does not authorize open-ended exploration" in flat
    assert "read every `required_action`" in flat
    assert "complete every listed `recommended_step`" in flat
    assert "before calling the review tool again" in flat
    assert "Only after Controller closure and current review pass" in flat


def test_prompt_orders_inconclusive_recovery_without_repeating_eval():
    flat = _flat(PROMPT_ZH)
    assert "do not repeat or revise that expression yet" in flat
    assert "the returned action names the exact next missing expression" in flat
    assert "then revise the incomplete assertion" in flat


def test_prompt_requires_sequential_single_tool_turns():
    flat = _flat(PROMPT_ZH)
    assert "Emit exactly one business tool call in each model response" in flat
    assert "Wait for that tool's result" in flat
    assert "Never batch, parallelize, or emit multiple tool calls" in flat
    assert "one-call turns, not one parallel tool-call batch" in flat
    assert "Never batch multiple `eval_assert` calls" in flat


def test_prompt_requires_same_strength_positive_assertions():
    flat = _flat(PROMPT_ZH)
    assert "`True` means the model satisfies the Root" in flat
    assert "`False` means it contradicts the Root" in flat
    assert "Preserve source, trigger, guard/condition, target, quantity" in flat
    assert "parenthesized state qualifier fixes the Root's source scope" in flat
    assert "Never lift it to an ancestor composite" in flat
    assert "not an NL obligation unless the NL itself supplies" in flat
    assert "Event existence alone cannot prove a destination" in flat
    assert "Do not strengthen" in flat
    assert "do not weaken it to `bool(effects(...))`" in flat
    assert "at least two distinct initialized progressing simulations" in flat
    assert "One invariant or existential `exists_always` path" in flat
    assert "exact `assert` string -> chain/Root/Unit map" in flat
    assert "semantically distinct direct predicates" in flat
    assert "Never evade uniqueness with whitespace" in flat
    assert "minimum sufficient evidence route" in flat
    assert "All evidence families are first-class capabilities" in flat
    assert "Do not follow a fixed tool order" in flat
    assert "First identify what the proposition quantifies over" in flat
    assert "Use simulation for one explicit initialized state" in flat
    assert "Use FBMCQ/formal evidence when the proposition ranges over" in flat
    assert "An explicit NL bound is not required" in flat
    assert "requirement_bound" in flat
    assert "analysis_bound" in flat


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
    assert "A cold simulation from model entry must make initialization explicit" in flat
    assert "using a leading empty cycle `[]`" in flat
    assert "literal `initial_vars` may override only the named subset" in flat
    assert "omitted variables retain their declaration initializers" in flat
    assert "A hot-start simulation with both an exact `initial_state` and complete `initial_vars`" in flat
    assert "does not require a leading `[]`" in flat
    assert "Do not use a hot-start result as proof of cold reachability" in flat
    assert "entry obligations, or default initialization behavior" in flat
    assert "Reusing an event in a later cycle is legal" in flat
    assert "consumed-event accounting is not a one-use rule" in flat
    assert "may appear more than once in one cycle's `consumed_events`" in flat
    assert "Never require `consumed_events.count(E) == 1`" in flat
    assert "duplicate labels alone" in flat
    assert 'For a local "while in S, event E leads to T" proposition' in flat
    assert "put E in the first caller cycle" in flat
    assert "E is consumed rather than unconsumed" in flat
    assert "completion/event-free transition leave S before E" in flat
    assert "a matching final state alone does not establish" in flat
    assert "`simulate(...).final.is_ended is True`" in flat
    assert "do not call `is_active` after the terminating event" in flat
    assert "call `read_fbmcq_guide`" in flat
    assert "replay-mismatched results are inconclusive" in flat


def test_prompt_preserves_inherited_forced_transition_semantics():
    flat = _flat(PROMPT_ZH)
    assert "`forced_expansion_role=inherited_exit_relay`" in flat
    assert "local hierarchical exit relay" in flat
    assert "not the authored business target or top-level termination" in flat
    assert "`forced_declaration_source` and `forced_declaration_target`" in flat
    assert "verify both the exact descendant relay and the declaring forced edge" in flat
    assert "Never join the relay `[*]` and the NL target with `or`" in flat
    assert "runtime result takes precedence" in flat


def test_prompt_prefers_simulation_for_runtime_behavior_outcomes():
    flat = _flat(PROMPT_ZH)

    assert "structure, relation, effect, simulation, formal, mapping" in flat
    assert "Use simulation for one explicit initialized state" in flat
    assert "a valid concrete counterexample may refute a universal requirement" in flat
    assert "a passing trace does not establish all-path correctness" in flat
    assert "A static transition relation cannot by itself prove event-causal runtime behavior" in flat
    assert "must not be weakened to edge existence" in flat
    assert "Use source mapping only for attribution" in flat


def test_prompt_makes_review_pass_current_and_actionable():
    flat = _flat(PROMPT_ZH)
    assert "current `review_discovery_coverage` result with `passed=true`" in flat
    assert "mandatory again after any subsequent revision/evaluation" in flat
    assert "required_actions" in PROMPT_ZH
    assert "related IDs, risk, recommended tools, concrete changes" in flat
    assert "independently reviews every Segment, Requirement, behavior SourceFact" in flat
    assert "reviewed_state_fingerprint" in PROMPT_ZH
    assert "There is no Agent-declared partial-success path" in flat


def test_prompt_treats_passing_review_as_a_stop_condition():
    flat = _flat(PROMPT_ZH)
    assert "submission is the mandatory next response" in flat
    assert "optional enhancements mentioned only in `coverage_analysis` are non-blocking" in flat
    assert "never execute them after a passing review" in flat
    assert "passing review with no remaining attribution work is a stop condition" in flat
    assert "do not call another business tool before submitting" in flat


def test_prompt_requires_feedback_driven_progress_without_external_takeover():
    flat = _flat(PROMPT_ZH)
    assert "No external controller will invent" in flat
    assert "Never repeat the same tool with semantically unchanged arguments" in flat
    assert "For `mandatory_tool_rejected`, call the returned `required_tool`" in flat
    assert "Do not disguise repetition with whitespace" in flat
    assert "close every item" in flat
    assert "`submit_discovery` schema validation returns `field_mismatches`" in flat
    assert "never respond by shortening the outcome" in flat
    assert "corrective workflow feedback, not as semantic evidence" in flat
    assert "intentional failure, budget probe" in flat


def test_prompt_converges_exploration_into_the_registered_plan():
    flat = _flat(PROMPT_ZH)
    assert "not a checklist for enumerating or corroborating" in flat
    assert "targeted pre-plan" in flat
    assert "inconclusive latest evaluation or failed review" in flat
    assert "Use the exact registered or provisional Root ID" in flat
    assert "never mint suffix variants, borrow another Root's identity or budget" in flat
    assert "These tools are never a parallel truth path around `eval_assert`" in flat
    assert "Keep the payload complete but concise" in flat
    assert "cite only SourceFacts actually consumed by assertions" in flat
    assert "use one-sentence rationales" in flat


def test_prompt_separates_plan_registration_from_truth_evaluation():
    flat = _flat(PROMPT_ZH)
    assert "default and preferred next business call after required reads" in flat
    assert "Registration commits what will be checked" in flat
    assert "it is not a truth verdict" in flat
    assert "does not require knowing whether any assertion will evaluate" in flat
    assert "truth is determined only after registration by `eval_assert`" in flat
    assert "There is exactly one successfully registered initial plan" in flat
    assert "A rejected attempt is not a registered plan" in flat


def test_prompt_forbids_preplan_probing_and_speculative_attribution():
    flat = _flat(PROMPT_ZH)
    for marker in (
        "Never intentionally make a call expected to fail",
        "Do not probe budgets, quotas, limits, duplicate detection",
        "do not repeat an already complete inventory query",
        "do not add or rename Root IDs",
        "do not make confidence-only corroboration calls",
        "forbidden before that evaluated contradiction",
        "one required guide read is owned by profile wiring",
    ):
        assert marker in flat
    assert "Before the first successful plan registration" in flat
    assert "`lookup_source_trace` remains forbidden" in flat
    assert "targeted pre-plan `query_model` or `observe_trace` call is allowed" in flat
    assert "after that answer, register the plan" in flat
    assert "do not explore to pre-prove truth" in flat
    assert "Never reread any guide or task resource" in flat
    assert "Do not call `read_fbmcq_guide` to decide whether FBMCQ is needed" in flat
    assert "to confirm it is unnecessary, just in case" in flat
    assert "Choose FBMCQ by semantic fit" in flat


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



def test_prompt_makes_all_evidence_families_first_class_and_allows_targeted_preplan():
    flat = _flat(PROMPT_ZH)
    assert "All evidence families are first-class capabilities" in flat
    assert "profile-exposed topology or inspect facts" in flat
    assert "inspect facts only as diagnostics and hypothesis leads" in flat
    assert "targeted pre-plan" in flat
    assert "one concrete object/initialization/event-sequence question" in flat
    assert "After that single call, the runtime requires `register_coverage_plan`" in flat
    assert "An explicit NL bound is not required" in flat
    assert "formal-profile syntax/capability guide" in flat
    assert "never implies that FBMCQ must be used" in flat


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
    assert "complete frozen planning inventory" in text
    assert "default next business call is register_coverage_plan" in text
    assert "does not require knowing assertion truth in advance" in text
    assert "A targeted pre-plan query_model or observe_trace call is allowed" in text
    assert "Do not call lookup_source_trace before an evaluated contradiction" in text
    assert "Do not reread any guide/task resource" in text
    assert "read the FBMCQ guide merely to decide whether it is needed" in text
    assert "Emit exactly one business tool call per model response" in text
    assert "wait for its result before the next call" in text
    assert "review_discovery_coverage after its prerequisites are closed" in text
    assert "Follow its finite actionable findings until it passes" in text
    assert "ignore optional enhancements and return submit_discovery next" in text
    assert "returning submit_discovery" in text
