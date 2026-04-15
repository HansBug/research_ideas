from __future__ import annotations

import json
from typing import Any

import pandas as pd
from pathlib import Path

import sys

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from canonical_model import count_machine_components, normalize_machine
from eval_utils import ensure_json, json_dumps, macro_f1, prf_from_counts
from io_utils import baseline_result_dir, load_discussion_parquet, write_json, write_parquet
from llm_client import LLMClient
from result_schema import finalize_result_df


def local_system_prompt(
    task_description: str,
    requirements: str,
    *,
    state_list: dict[str, Any] | None = None,
    event_list: dict[str, Any] | None = None,
    variable_list: dict[str, Any] | None = None,
    transition_list: dict[str, Any] | None = None,
    action_list: dict[str, Any] | None = None,
) -> str:
    prompt = f"Task description:\n{task_description}\n\nRequirements:\n{requirements}\n\n"
    if state_list is not None:
        prompt += f"State List:\n{json.dumps(state_list, ensure_ascii=False)}\n\n"
    if event_list is not None:
        prompt += f"Event List:\n{json.dumps(event_list, ensure_ascii=False)}\n\n"
    if variable_list is not None:
        prompt += f"Variable List:\n{json.dumps(variable_list, ensure_ascii=False)}\n\n"
    if transition_list is not None:
        prompt += f"Transition List:\n{json.dumps(transition_list, ensure_ascii=False)}\n\n"
    if action_list is not None:
        prompt += f"Action List:\n{json.dumps(action_list, ensure_ascii=False)}\n\n"
    return prompt


def local_user_prompt(
    specific_task_description: str,
    *,
    domain_knowledge: str | None = None,
    format_description: str | None = None,
    constraint: str | None = None,
    suffix: str | None = None,
) -> str:
    prompt = specific_task_description.strip() + "\n"
    if domain_knowledge:
        prompt += "\n" + domain_knowledge.strip() + "\n"
    if format_description:
        prompt += f"\nFormat Description:\n{format_description.strip()}\n"
    if constraint:
        prompt += f"\nConstraint:\n{constraint.strip()}\n"
    if suffix:
        prompt += "\n" + suffix.strip() + "\n"
    return prompt


def _generate_json(
    llm: LLMClient,
    *,
    cache_key: str,
    system_prompt: str,
    user_prompt: str,
    max_output_tokens: int,
) -> dict[str, Any]:
    result = llm.generate(
        system_prompt,
        user_prompt,
        max_output_tokens=max_output_tokens,
        cache_key=cache_key,
    )
    try:
        return ensure_json(result.text)
    except Exception:
        repair_result = llm.generate(
            "Convert the previous answer into strict JSON only.",
            f"Previous answer:\n{result.text}\n\nReturn only fixed JSON.",
            max_output_tokens=max_output_tokens,
            cache_key=f"{cache_key}:repair",
        )
        return ensure_json(repair_result.text)


def build_reference_table() -> pd.DataFrame:
    models = load_discussion_parquet("ttool_ai_models").copy()
    reference = (
        models.groupby(["case_id", "case_name", "input_spec_text"], as_index=False)[
            [
                "state_machine_panel_count",
                "state_count",
                "transition_count",
                "nonempty_guard_count",
                "nonempty_action_count",
            ]
        ]
        .median()
        .rename(
            columns={
                "nonempty_guard_count": "guard_count",
                "nonempty_action_count": "action_count",
            }
        )
    )
    return reference


def build_reference_outputs() -> pd.DataFrame:
    models = load_discussion_parquet("ttool_ai_models").copy()
    rows: list[dict[str, Any]] = []
    for (case_id, case_name, input_spec_text), part in models.groupby(
        ["case_id", "case_name", "input_spec_text"], as_index=False
    ):
        rows.append(
            {
                "case_id": case_id,
                "case_name": case_name,
                "input_spec_text": input_spec_text,
                "reference_model_count": int(len(part)),
                "reference_xml_examples_json": json_dumps(
                    [
                        {"variant_name": row["variant_name"], "raw_xml": row["raw_xml"]}
                        for _, row in part[["variant_name", "raw_xml"]].iterrows()
                    ]
                ),
                "reference_variant_names_json": json_dumps(list(part["variant_name"])),
            }
        )
    return pd.DataFrame(rows)


def run_ttool_prompt(llm: LLMClient, case_id: str, spec_text: str) -> dict[str, Any]:
    system_prompt = (
        "You reproduce the TTool-AI baseline from the local sm/baseline.py workflow. "
        "Keep identifiers concise with underscores and return strict JSON only."
    )
    question_1 = """
When you are asked to identify SysML blocks, return them as a JSON specification formatted as follows:
```json
{
    "blocks": [
        {
            "name": "Name_of_block",
            "attributes": [
                {"name": "name_of_attribute", "type": "int|bool"}
            ]
        }
    ]
}
```

# Respect: each attribute must be of type "int" or "bool" only
# Respect: Any identifier (block, attribute, etc.) must not contain any space. Use "_" instead.

From the following system specification, using the specified JSON format, identify the typical system blocks and their attributes.
Do respect the JSON format, and provide only JSON (no explanation before or after).
"""
    answer_1 = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:blocks",
        system_prompt=system_prompt + "\nSystem specification:\n" + spec_text,
        user_prompt=question_1,
        max_output_tokens=2000,
    )
    question_2 = """
From the previous JSON and system specification, update this JSON with the signals you have to identify.
If necessary, you can add new blocks and new attributes. Connect the signals accordingly to constraints to be respected.

# Respect: Two signals with the same name are assumed to be connected: this is the only way to connect signals.
# Respect: Two connected signals must have the same list of attributes, even if they are defined in two different blocks.
One of them must be output, the other one must be input.
# Respect: all input signals must have exactly one corresponding output signal, i.e., an output signal with the same name

Return JSON only:
{
  "blocks": [...],
  "signals": [
    {
      "name": "signal_name",
      "source_block": "BlockA",
      "target_block": "BlockB",
      "payload": ["field1", "field2"]
    }
  ]
}
"""
    answer_2 = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:signals",
        system_prompt=(
            system_prompt
            + "\nSystem specification:\n"
            + spec_text
            + "\nExisting block design:\n"
            + json.dumps(answer_1, ensure_ascii=False)
        ),
        user_prompt=question_2,
        max_output_tokens=2500,
    )
    question_3 = """
From the system specification, and from the definition of blocks and their connections, identify the state machine of block.
# Respect: in actions, use only attributes and signals already defined in the corresponding block
# Respect: at least one state must be called "Start", which is the start state
# Respect: if a guard, an action, or an after is empty, use an empty string "", do not use "null"
# Respect: an action contains either a variable affectation, e.g. "x = x + 1" or a signal send/receive

For this reproduction workspace, convert the final model into strict JSON:
{
  "machine_name": "SystemName",
  "blocks": [
    {
      "name": "BlockName",
      "attributes": [...],
      "signals": [{"name": "signal", "direction": "in|out"}],
      "states": [
        {"name": "StateName", "parent": null, "parallel_group": null, "is_history": false, "is_initial": true}
      ],
      "transitions": [
        {"source": "StateA", "target": "StateB", "event": "event", "guard": "", "action": ""}
      ]
    }
  ],
  "signals": [...]
}
"""
    return _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:final",
        system_prompt=(
            system_prompt
            + "\nSystem specification:\n"
            + spec_text
            + "\nCurrent architecture:\n"
            + json.dumps(answer_2, ensure_ascii=False)
        ),
        user_prompt=question_3,
        max_output_tokens=4500,
    )


def run_mti_prompt(llm: LLMClient, case_id: str, spec_text: str) -> dict[str, Any]:
    task_description = """
You are a control systems domain expert and are assigned with the task of state machine modeling.
Your objective is to build a state machine model following the given program description.
There are many steps involved in the process. Follow the instruction for your current step.
""".strip()
    state_list = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:states",
        system_prompt=local_system_prompt(task_description, spec_text),
        user_prompt=local_user_prompt(
            """
Please read and understand the whole <Requirements>, analyze the running logic of the system
and define all the possible states of the system state machine and output <State list>.
(States can contain nested or parallel relationships)
""",
            domain_knowledge="""
Parallel states, also known as concurrent states, are states within a state machine that can be active simultaneously.
Nested states refer to a hierarchical relationship between states in a state machine.
""",
            format_description="""
```json
{
  "states": [
    {
      "name": "StateName",
      "description": "Description of the state",
      "sub_states": [
        {"name": "SubStateName", "description": "Description", "sub_states": []}
      ]
    }
  ]
}
```
""",
            suffix="Identified State List:",
        ),
        max_output_tokens=2500,
    )
    event_list = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:events",
        system_prompt=local_system_prompt(task_description, spec_text),
        user_prompt=local_user_prompt(
            """
According to the the <Requirements> and the <Definition of events>, please identify the external and internal events of the state machine.
""",
            domain_knowledge="""
Definition of events:
- External events: stimuli that originate from outside the system.
- Internal events: incentives generated inside the system to trigger a transition.
""",
            format_description="""
```json
{
  "events": [
    {"name": "EventName", "description": "Description", "type": "Internal|External"}
  ]
}
```
""",
            suffix="Identified Event List:",
        ),
        max_output_tokens=1800,
    )
    variable_list = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:variables",
        system_prompt=local_system_prompt(
            task_description,
            spec_text,
            state_list=state_list,
        ),
        user_prompt=local_user_prompt(
            """
According to the <Requirements>, please identify the variables of the state machine and output the <Variables list>.
""",
            domain_knowledge="""
In a state machine, variables capture and represent information relevant to the system's behavior.
Input variables are used to receive external stimuli.
Output variables are used to produce the results of the state machine's operations.
""",
            format_description="""
```json
{
  "variables": [
    {"name": "VariableName", "description": "Description", "type": "boolean|int"}
  ]
}
```
""",
            suffix="Identified Variable List:",
        ),
        max_output_tokens=1800,
    )
    transition_list = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:transitions",
        system_prompt=local_system_prompt(
            task_description,
            spec_text,
            state_list=state_list,
            event_list=event_list,
            variable_list=variable_list,
        ),
        user_prompt=local_user_prompt(
            """
According to the <Requirements>, please identify all the transitions of each state in <State list>.
""",
            domain_knowledge="""
The transition situations between the states include four types:
1. Direct Transition
2. Transition with Trigger Event
3. Transition with Guard Condition
4. Transition with Trigger Event and Guard Condition
""",
            format_description="""
```json
{
  "transitions": [
    {"source": "StateName", "target": "AnotherStateName", "event": "EventName", "guard": "condition"}
  ]
}
```
""",
            constraint="""
1. "source" and "target" should be the object in the <State list>
2. "event" should be the object in the <Event list>
3. "guard" should be the judgement expression of the object in the <Variable list> or the time delay constraint.
""",
            suffix="Identified Transition List:",
        ),
        max_output_tokens=3000,
    )
    action_list = _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:actions",
        system_prompt=local_system_prompt(
            task_description,
            spec_text,
            state_list=state_list,
            event_list=event_list,
            variable_list=variable_list,
            transition_list=transition_list,
        ),
        user_prompt=local_user_prompt(
            """
According to the model information, analyze the operations for variables and events, and decide when the operations happen(on entry of state, on exit of state, on transition of state).
""",
            domain_knowledge="""
On Entry: action immediately executed when a state machine enters a specific state.
On Exit: operation executed when the state machine is about to leave a certain state.
Transition Action: action executed during the process of the state machine transitioning from one state to another.
""",
            format_description="""
```json
{
  "actions": [
    {"action_position": ["StateName", "on entry"], "content": "expression or raise(EventName)"},
    {"action_position": ["StateName", "on transition", "AnotherStateName"], "content": "expression or raise(EventName)"}
  ]
}
```
""",
            constraint="""
1. State names should come from the <State list>
2. Event names should come from the <Event list>
3. Variables should come from the <Variable list>
""",
            suffix="Identified Action List:",
        ),
        max_output_tokens=2000,
    )
    return _generate_json(
        llm,
        cache_key=f"ttool:{case_id}:mti:final",
        system_prompt=local_system_prompt(
            task_description,
            spec_text,
            state_list=state_list,
            event_list=event_list,
            variable_list=variable_list,
            transition_list=transition_list,
            action_list=action_list,
        ),
        user_prompt=local_user_prompt(
            """
According to <Requirements>, build the state machine model by the following steps:
1. Build the structure of the state machine according to <State list>
2. Add the transition information to each state according to <Transition list>
3. Add the action information to proper position according to <Action list>
4. Add the data definition to the state machine according to <Variable list>
""",
            format_description="""
For this reproduction workspace, return strict JSON in the following format:
{
  "machine_name": "SystemName",
  "blocks": [
    {
      "name": "BlockName",
      "attributes": [{"name":"attr","type":"int|bool|string"}],
      "signals": [{"name":"sig","direction":"in|out"}],
      "states": [{"name":"StateName","parent":null,"parallel_group":null,"is_history":false,"is_initial":false}],
      "transitions": [{"source":"StateA","target":"StateB","event":"","guard":"","action":""}]
    }
  ]
}
""",
            suffix="Final state machine model JSON:",
        ),
        max_output_tokens=5000,
    )


def evaluate_case(
    payload: dict[str, Any], reference_row: pd.Series
) -> tuple[dict[str, int], float, dict[str, dict[str, float | int]]]:
    counts = count_machine_components(payload)
    reference_pairs = {
        "State machine panels": (
            counts["state_machine_panel_count"],
            int(reference_row["state_machine_panel_count"]),
        ),
        "States": (counts["state_count"], int(reference_row["state_count"])),
        "Transitions": (counts["transition_count"], int(reference_row["transition_count"])),
        "Guards": (counts["guard_count"], int(reference_row["guard_count"])),
        "Actions": (counts["action_count"], int(reference_row["action_count"])),
    }
    component_metrics = {
        label: prf_from_counts(predicted, reference)
        for label, (predicted, reference) in reference_pairs.items()
    }
    return counts, macro_f1(component_metrics.values()), component_metrics


def run_ttool() -> None:
    result_dir = baseline_result_dir("ttool")
    output_path = result_dir / "predictions.parquet"
    summary_path = result_dir / "summary.json"
    if output_path.exists() and summary_path.exists():
        return

    reference = build_reference_table()
    reference_outputs = build_reference_outputs()
    reference = reference.merge(
        reference_outputs, on=["case_id", "case_name", "input_spec_text"], how="left"
    )
    llm = LLMClient()
    rows: list[dict[str, Any]] = []
    for _, ref_row in reference.iterrows():
        case_id = ref_row["case_id"]
        spec_text = ref_row["input_spec_text"]
        for strategy_name, fn in (
            ("ttool_ai_prompt", run_ttool_prompt),
            ("mti_multi_step", run_mti_prompt),
        ):
            payload = normalize_machine(fn(llm, case_id, spec_text))
            counts, macro_component_f1, component_metrics = evaluate_case(payload, ref_row)
            rows.append(
                {
                    "baseline_name": "ttool",
                    "dataset_id": "ttool_ai",
                    "sample_id": f"ttool::{case_id}::{strategy_name}",
                    "case_id": case_id,
                    "case_name": ref_row["case_name"],
                    "variant_id": case_id,
                    "variant_name": ref_row["case_name"],
                    "sample_kind": "system_specification_to_avatar_design",
                    "strategy_name": strategy_name,
                    "input_modality": "Natural-language system specification",
                    "input_text": spec_text,
                    "input_payload_json": json_dumps(
                        {
                            "case_id": case_id,
                            "input_spec_text": spec_text,
                        }
                    ),
                    "reference_output_text": ref_row["reference_xml_examples_json"],
                    "reference_output_json": json_dumps(
                        {
                            "reference_model_count": int(ref_row["reference_model_count"]),
                            "reference_variant_names": json.loads(
                                ref_row["reference_variant_names_json"]
                            ),
                            "reference_xml_examples": json.loads(
                                ref_row["reference_xml_examples_json"]
                            ),
                        }
                    ),
                    "prediction_output_text": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                    "prediction_output_json": json.dumps(
                        payload, ensure_ascii=False, sort_keys=True
                    ),
                    "reference_output_format": "ttool_avatar_xml_aggregate",
                    "prediction_output_format": "canonical_json",
                    "reference_counts_json": json_dumps(
                        {
                            "state_machine_panel_count": int(ref_row["state_machine_panel_count"]),
                            "state_count": int(ref_row["state_count"]),
                            "transition_count": int(ref_row["transition_count"]),
                            "guard_count": int(ref_row["guard_count"]),
                            "action_count": int(ref_row["action_count"]),
                        }
                    ),
                    "prediction_counts_json": json_dumps(counts),
                    "llm_provider": None,
                    "llm_model_name": llm.model,
                    "llm_raw_mode": None,
                    "is_repaired": False,
                    "evaluation_method": "count_based_component_macro_f1_against_case_level_reference_medians",
                    "primary_metric_name": "macro_component_f1",
                    "primary_metric_value": macro_component_f1,
                    "prediction_json": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                    "pred_state_machine_panel_count": counts["state_machine_panel_count"],
                    "pred_state_count": counts["state_count"],
                    "pred_transition_count": counts["transition_count"],
                    "pred_guard_count": counts["guard_count"],
                    "pred_action_count": counts["action_count"],
                    "ref_state_machine_panel_count": int(ref_row["state_machine_panel_count"]),
                    "ref_state_count": int(ref_row["state_count"]),
                    "ref_transition_count": int(ref_row["transition_count"]),
                    "ref_guard_count": int(ref_row["guard_count"]),
                    "ref_action_count": int(ref_row["action_count"]),
                    "macro_component_f1": macro_component_f1,
                    "component_metrics_json": json.dumps(
                        component_metrics, ensure_ascii=False, sort_keys=True
                    ),
                }
            )

    pred_df = finalize_result_df(pd.DataFrame(rows))
    summary = {
        "baseline": "ttool",
        "scenario_count": int(pred_df["case_id"].nunique()),
        "strategy_summary": {},
    }
    for strategy_name, part in pred_df.groupby("strategy_name"):
        summary["strategy_summary"][strategy_name] = {
            "case_count": int(len(part)),
            "macro_f1": float(part["macro_component_f1"].mean()),
        }
    write_parquet(pred_df, output_path)
    write_json(summary, summary_path)
