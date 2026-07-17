from __future__ import annotations

import re

import pytest

from paper_stm_repair_loop.prompts.discover import system_prompt, user_prompt


PROMPT_ZH = system_prompt("zh-CN")
PROMPT_EN = system_prompt("en-US")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _index_all(prompt: str, needles: list[str]) -> list[int]:
    positions = []
    for needle in needles:
        pos = prompt.find(needle)
        assert pos >= 0, f"missing prompt marker: {needle}"
        positions.append(pos)
    return positions


def test_prompt_is_executable_protocol_not_toolbox_and_orders_the_workflow():
    markers = [
        "## Mandatory working protocol and completion conditions",
        "1. **Freeze orientation.",
        "2. **Construct one complete check-draft batch.",
        "3. **Evaluate the whole batch.",
        "4. **Investigate named evidence gaps, then adjudicate conservatively.",
        "5. **Run batch coverage and zero-root self-check.",
        "6. **Submit once.",
    ]
    assert _index_all(PROMPT_ZH, markers) == sorted(_index_all(PROMPT_ZH, markers))
    assert "Completion condition:" in PROMPT_ZH
    assert "immutable run identity" in PROMPT_ZH
    assert "Controller has already prepared only" in PROMPT_ZH
    assert "This protocol is the work to perform" in _flat(PROMPT_ZH)
    assert "complete all six reasoning and coverage steps even when no optional tool call is needed" in _flat(PROMPT_ZH)
    assert "Optional tool use never replaces comparison, adjudication, coverage, or submission" in _flat(PROMPT_ZH)


def test_prompt_requires_attempt_frozen_six_field_context_and_single_agent_run():
    assert "one and only `AgentApp.run`" in PROMPT_ZH
    assert "No other Agent or producer has generated checks or verdicts" in _flat(PROMPT_ZH)
    assert "You are the only LLM Agent in B-discover" in _flat(PROMPT_ZH)
    assert "attempt-frozen six-field working set" in PROMPT_ZH
    for field in ["`stage`", "`loop_no`", "`model`", "`targets`", "`current_records`", "`readable_history`"]:
        assert field in PROMPT_ZH
    assert "never reads a newer mutable state" in _flat(PROMPT_ZH)
    assert "targets=[]" in PROMPT_ZH
    assert "readable_history=[]" in PROMPT_ZH


def test_prompt_tool_whitelist_has_four_investigation_tools_plus_mandatory_evaluation():
    whitelist_line = next(line for line in PROMPT_ZH.splitlines() if "only Agent-callable tools are exactly" in line)
    tools = re.findall(r"`([a-z_]+)`", whitelist_line)
    assert tools == ["read_task", "query_model", "observe_trace", "lookup_source_trace", "evaluate_checks"]
    assert "is optional" in PROMPT_ZH
    assert "only when an evaluated proposition has a concrete missing structural" in _flat(PROMPT_ZH)
    assert "`evaluate_checks(checks)` is mandatory for the final batch" in PROMPT_ZH
    assert "gate.eligible=true" in PROMPT_ZH
    assert "No other capability is part of your tool surface" in PROMPT_ZH


def test_prompt_does_not_require_controller_tools_or_tool_call_termination():
    forbidden_required_phrases = [
        "Call `check_fcstm`",
        "call `check_fcstm`",
        "Call `run_scenarios`",
        "call `run_scenarios`",
        "Call `verify_properties`",
        "call `verify_properties`",
        "require_tool_call",
        "required tool call",
        "fifth business tool",
        "extra tool call",
    ]
    for phrase in forbidden_required_phrases:
        assert phrase not in PROMPT_ZH
    for forbidden_tool in ["`check_fcstm`", "`run_scenarios`", "`verify_properties`", "`validate_discovery_checks`", "`verify_static_consistency`"]:
        assert forbidden_tool not in PROMPT_ZH


def test_prompt_defines_confirmed_candidate_rejected_boundaries_and_zero_root_batch_coverage():
    for marker in ["`confirmed`", "`candidate_only`", "`rejected`"]:
        assert marker in PROMPT_ZH
    assert "all final checks were considered" in _flat(PROMPT_ZH)
    assert "zero roots" in PROMPT_ZH
    assert "no_issue_found=true" in PROMPT_ZH
    assert "non-empty reason" in PROMPT_ZH
    assert "all-or-nothing" in PROMPT_ZH
    flattened = _flat(PROMPT_ZH)
    assert "all confirmed roots cite current-run valid checks/records" in flattened
    assert "exact one-to-one grounding" in flattened
    assert "merely existing in inspect or a check binding is not source attribution" in flattened
    assert "no defensible confirmed or candidate root remains" in flattened
    assert "Publish confirmed/candidate propositions as `root_nodes`" in _flat(PROMPT_ZH)
    assert "`rejected_propositions`" in PROMPT_ZH
    assert "union of root `required_check_ids` and rejected `considered_check_ids`" in _flat(PROMPT_ZH)


def test_prompt_forbids_model_mutation_repair_future_confirm_and_source_closure_claims():
    for text in [
        "do not edit `STM_0`",
        "do not propose Repair actions",
        "do not make Confirm or source-closure claims",
        "do not modify or restate `STM_0` as a patch",
        "not source closure",
        "future Repair/Confirm",
        "Never claim model completeness",
        "scientific success",
    ]:
        assert text in _flat(PROMPT_ZH)


def test_prompt_rejects_representation_artifacts_bounded_overclaiming_and_duplicate_roots():
    flat = _flat(PROMPT_ZH)
    assert "source-to-fcstm structural difference" in flat
    assert "conversion artifact is not a source behavioral issue" in flat
    assert "Reject representation-only propositions explicitly" in flat
    assert "bounded `unsat`, `not_observed_within_bound`" in flat
    assert "cannot independently establish unbounded unreachability" in flat
    assert "one underlying source-model defect should cite one root" in flat
    assert "Do not inflate the issue count" in flat


def test_prompt_requires_single_structured_output_not_prose_or_split_batches():
    assert "one provider-native/Pydantic structured output" in PROMPT_ZH
    assert "semantic name" in PROMPT_ZH and "`submit_discovery`" in PROMPT_ZH
    assert "Submit once" in PROMPT_ZH
    assert "Return exactly one complete `submit_discovery` structured" in PROMPT_ZH
    assert "do not publish partial batches" in PROMPT_ZH
    assert "do not add prose alternatives" in _flat(PROMPT_ZH)


def test_prompt_language_policy_keeps_schema_english_and_free_text_in_requested_language():
    assert "Run content language: `zh-CN`" in PROMPT_ZH
    assert "in `zh-CN` only" in PROMPT_ZH
    assert "Run content language: `en-US`" in PROMPT_EN
    assert "in `en-US` only" in PROMPT_EN
    for prompt in [PROMPT_ZH, PROMPT_EN]:
        assert "Keep every schema key, enum, identifier" in prompt
        assert "in English" in prompt


def test_system_prompt_rejects_unknown_language():
    with pytest.raises(ValueError, match="unsupported Discover content language"):
        system_prompt("fr-FR")


def test_user_prompt_is_read_only_and_requests_one_structured_result():
    text = user_prompt({"b": 2, "a": "中文"})
    assert "Discover task snapshot (read-only)" in text
    assert '"a": "中文"' in text
    assert text.find('"a"') < text.find('"b"')
    assert "return one structured submit_discovery result" in text
