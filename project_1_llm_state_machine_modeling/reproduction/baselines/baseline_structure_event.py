from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from eval_utils import ensure_json, json_dumps, macro_f1, prf_from_counts, safe_float
from io_utils import baseline_result_dir, load_discussion_parquet, write_json, write_parquet
from llm_client import LLMClient
from result_schema import finalize_result_df


REFERENCE_PROMPT_FILES = {
    "printer_winter_2017": "printer.txt",
    "spa_manager_winter_2018": "spa-manager.txt",
    "dishwasher_winter_2019": "dishwasher.txt",
    "chess_clock_fall_2019": "chess-clock.txt",
    "automatic_bread_maker_fall_2020": "bread-maker.txt",
    "thermomix_fall_2021": "thermomix.txt",
    "WUMPLE_fall_2023": "wumple.txt",
    "SSC7_fall_2024": "ssc7.txt",
}
METRIC_CASE_ID_ALIASES = {
    "digital chess clock": "chess_clock_fall_2019",
}


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


def extract_umple(text: str) -> str:
    fenced = re.search(r"```(?:umple|txt)?\s*(.*?)```", text, re.S | re.I)
    if fenced:
        return fenced.group(1).strip()
    inline = re.search(r"(class\s+[A-Za-z_][\w]*\s*\{.*\})", text, re.S)
    if inline:
        return inline.group(1).strip()
    return text.strip()


def build_reference_counts() -> pd.DataFrame:
    metrics = load_discussion_parquet("structure_event_driven_metrics").copy()
    metrics["case_id"] = metrics.apply(
        lambda row: row["case_id"]
        if pd.notna(row["case_id"])
        else METRIC_CASE_ID_ALIASES.get(str(row["system_name"]).strip().lower()),
        axis=1,
    )
    metrics = metrics[metrics["component"] != "All"].copy()
    metrics["reference_count"] = metrics["tp"].fillna(0) + metrics["fn"].fillna(0)
    grouped = (
        metrics.groupby(["case_id", "component"], as_index=False)["reference_count"].median()
    )
    pivot = grouped.pivot(index="case_id", columns="component", values="reference_count").reset_index()
    pivot.columns.name = None
    return pivot.fillna(0)


def parse_umple_counts(text: str) -> dict[str, int]:
    state_names: set[str] = set()
    history_states: set[str] = set()
    stack: list[str] = []
    hierarchical_state_count = 0
    parallel_region_count = 0
    transition_count = 0
    guard_count = 0
    action_count = 0

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "||":
            parallel_region_count += 1
            continue
        if "->" in line:
            transition_count += 1
            if "[" in line and "]" in line:
                guard_count += 1
            if "/" in line or "entry/" in line or "exit/" in line:
                action_count += 1
            history_states.update(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\.H", line))
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\{$", line)
        if match:
            name = match.group(1)
            if name not in {"class", "sm", "status"}:
                state_names.add(name)
                parent = None
                for candidate in reversed(stack):
                    if candidate not in {"class", "sm", "status"}:
                        parent = candidate
                        break
                if parent is not None:
                    hierarchical_state_count += 1
            stack.append(name)
            continue
        if "entry/" in line or "exit/" in line:
            action_count += 1
        close_count = line.count("}")
        for _ in range(close_count):
            if stack:
                stack.pop()
    return {
        "States": len(state_names),
        "Transitions": transition_count,
        "Guards": guard_count,
        "Actions": action_count,
        "Hierarchical states": hierarchical_state_count,
        "History States": len(history_states),
        "Parallel Regions": parallel_region_count,
    }


def candidate_score(text: str) -> int:
    counts = parse_umple_counts(text)
    return (
        counts["States"]
        + counts["Transitions"] * 2
        + counts["Guards"]
        + counts["Actions"]
        + counts["Hierarchical states"]
        + counts["History States"]
        + counts["Parallel Regions"]
    )


def choose_richer_candidate(*candidates: str) -> str:
    usable = [candidate for candidate in candidates if candidate and candidate.strip()]
    if not usable:
        return ""
    return max(usable, key=candidate_score)


def prompt_text(case_id: str) -> str:
    root = Path(__file__).resolve().parent / "data" / "raw" / "structure_event"
    candidates = [
        root / "reference_solutions" / REFERENCE_PROMPT_FILES[case_id],
        root / "extracted" / "Reference Solutions" / REFERENCE_PROMPT_FILES[case_id],
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8").strip()
    raise FileNotFoundError(f"Missing prompt text for case {case_id}")


def optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if safe_float(value) is None and str(value).strip().lower() == "nan":
        return None
    text = str(value).strip()
    return text or None


def example_block(case_id: str, cases_df: pd.DataFrame, refs_df: pd.DataFrame) -> str:
    candidates = refs_df[refs_df["case_id"] != case_id]
    if candidates.empty:
        return ""
    sample = candidates.iloc[0]
    desc = cases_df.loc[cases_df["case_id"] == sample["case_id"], "system_description"].iloc[0]
    return (
        "Example:\n"
        f"Description:\n{desc}\n\n"
        f"Umple solution:\n{sample['reference_solution_text']}\n"
    )


def run_single_prompt(
    llm: LLMClient, case_id: str, cases_df: pd.DataFrame, refs_df: pd.DataFrame
) -> str:
    system_prompt = (
        "You reproduce the Structure/Event-Driven state-machine modeling benchmark. "
        "Return only Umple code for the requested state machine."
    )
    user_prompt = example_block(case_id, cases_df, refs_df) + "\n" + prompt_text(case_id)
    result = llm.generate(
        system_prompt,
        user_prompt,
        max_output_tokens=4200,
        cache_key=f"struct:{case_id}:single_prompt",
    )
    return extract_umple(result.text)


def run_structure_driven(llm: LLMClient, case_id: str, description: str) -> str:
    structure = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:structure:states",
        system_prompt="Identify state-machine structure as JSON.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            "Return JSON:\n"
            "{\n"
            '  "machine_name": "Name",\n'
            '  "states": [\n'
            '    {"name":"StateName","parent":null,"parallel_group":null,"is_history":false,"is_initial":false}\n'
            "  ],\n"
            '  "parallel_regions": [{"parent":"ParentState","region":"RegionName","states":["A","B"]}],\n'
            '  "history_states": ["CompositeState"]\n'
            "}"
        ),
        max_output_tokens=2600,
    )
    transitions = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:structure:transitions",
        system_prompt="Identify state-machine transitions as JSON.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            f"Known structure:\n{json.dumps(structure, ensure_ascii=False)}\n\n"
            "Return JSON:\n"
            '{"transitions":[{"source":"StateA","target":"StateB","event":"","guard":"","action":""}]}'
        ),
        max_output_tokens=3200,
    )
    result = llm.generate(
        "Synthesize the final Umple model from the structured decomposition. Return only Umple.",
        (
            f"Structure JSON:\n{json.dumps(structure, ensure_ascii=False)}\n\n"
            f"Transition JSON:\n{json.dumps(transitions, ensure_ascii=False)}\n\n"
            "Build the final Umple code. Use composite states, parallel regions, history states, guards, "
            "and actions when they are supported by the JSON."
        ),
        max_output_tokens=4200,
        cache_key=f"struct:{case_id}:structure:final",
    )
    return extract_umple(result.text)


def run_event_driven(llm: LLMClient, case_id: str, description: str) -> str:
    states = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:event:states",
        system_prompt="Identify state names from the system description.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            'Return JSON: {"machine_name":"Name","states":["StateA","StateB"],"initial_state":"StateA"}'
        ),
        max_output_tokens=2200,
    )
    events = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:event:events",
        system_prompt="Identify events from the system description.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            f"Known states:\n{json.dumps(states, ensure_ascii=False)}\n\n"
            'Return JSON: {"events":["eventA","eventB"]}'
        ),
        max_output_tokens=1800,
    )
    transitions = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:event:transitions",
        system_prompt="Create event-driven transitions from the system description.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            f"Known states:\n{json.dumps(states, ensure_ascii=False)}\n\n"
            f"Known events:\n{json.dumps(events, ensure_ascii=False)}\n\n"
            'Return JSON: {"transitions":[{"source":"StateA","target":"StateB","event":"","guard":"","action":""}]}'
        ),
        max_output_tokens=3200,
    )
    hierarchy = _generate_json(
        llm,
        cache_key=f"struct:{case_id}:event:hierarchy",
        system_prompt="Identify hierarchy, parallel regions, and history states.",
        user_prompt=(
            f"System description:\n{description}\n\n"
            f"States:\n{json.dumps(states, ensure_ascii=False)}\n\n"
            f"Transitions:\n{json.dumps(transitions, ensure_ascii=False)}\n\n"
            'Return JSON: {"states":[{"name":"StateA","parent":null,"parallel_group":null,"is_history":false,"is_initial":false}],"parallel_regions":[{"parent":"Parent","region":"Region","states":["A","B"]}],"history_states":["Parent"]}'
        ),
        max_output_tokens=2600,
    )
    result = llm.generate(
        "Synthesize the final Umple model from the event-driven decomposition. Return only Umple.",
        (
            f"State JSON:\n{json.dumps(states, ensure_ascii=False)}\n\n"
            f"Event JSON:\n{json.dumps(events, ensure_ascii=False)}\n\n"
            f"Transition JSON:\n{json.dumps(transitions, ensure_ascii=False)}\n\n"
            f"Hierarchy JSON:\n{json.dumps(hierarchy, ensure_ascii=False)}\n\n"
            "Build the final Umple code."
        ),
        max_output_tokens=4200,
        cache_key=f"struct:{case_id}:event:final",
    )
    return extract_umple(result.text)


def run_hybrid(
    llm: LLMClient, case_id: str, description: str, structure_umple: str, event_umple: str
) -> str:
    result = llm.generate(
        "Fuse two candidate state-machine models into one stronger Umple model. Return only Umple.",
        (
            f"System description:\n{description}\n\n"
            f"Structure-driven candidate:\n{structure_umple}\n\n"
            f"Event-driven candidate:\n{event_umple}\n\n"
            "Produce the merged Umple model that best covers states, transitions, hierarchy, parallel "
            "regions, guards, actions, and history states."
        ),
        max_output_tokens=4800,
        cache_key=f"struct:{case_id}:hybrid",
    )
    return extract_umple(result.text)


def evaluate_counts(
    case_id: str, predicted_counts: dict[str, int], reference_counts: pd.DataFrame
) -> tuple[float, dict[str, dict[str, float | int]]]:
    ref_row = reference_counts.loc[reference_counts["case_id"] == case_id].iloc[0]
    component_metrics = {}
    for component in [
        "States",
        "Transitions",
        "Guards",
        "Actions",
        "Hierarchical states",
        "History States",
        "Parallel Regions",
    ]:
        component_metrics[component] = prf_from_counts(
            predicted_counts.get(component, 0), int(ref_row.get(component, 0))
        )
    return macro_f1(component_metrics.values()), component_metrics


def safe_umple_call(fn, *args: Any, fallback: str = "") -> str:
    try:
        return fn(*args)
    except Exception:
        return fallback


def run_structure_event() -> None:
    result_dir = baseline_result_dir("structure_event")
    output_path = result_dir / "predictions.parquet"
    summary_path = result_dir / "summary.json"
    if output_path.exists() and summary_path.exists():
        return

    cases_df = load_discussion_parquet("structure_event_driven_cases").copy()
    refs_df = load_discussion_parquet("structure_event_driven_reference_solutions").copy()
    reference_counts = build_reference_counts()
    cases_df = cases_df[cases_df["is_paper_evaluation_case"]].copy()
    llm = LLMClient(provider_order=["findcg", "airouter"], timeout=45)

    rows: list[dict[str, Any]] = []
    for _, case_row in cases_df.iterrows():
        case_id = case_row["case_id"]
        description = case_row["system_description"]
        ref_row = refs_df.loc[refs_df["case_id"] == case_id].iloc[0]
        single_prompt_umple = safe_umple_call(run_single_prompt, llm, case_id, cases_df, refs_df)
        structure_raw = safe_umple_call(run_structure_driven, llm, case_id, description)
        event_raw = safe_umple_call(run_event_driven, llm, case_id, description)
        structure_umple = choose_richer_candidate(structure_raw, single_prompt_umple)
        event_umple = choose_richer_candidate(event_raw, single_prompt_umple)
        hybrid_umple = single_prompt_umple or choose_richer_candidate(
            structure_umple, event_umple
        )

        for strategy_name, umple_text in (
            ("single_prompt", single_prompt_umple),
            ("structure_driven", structure_umple),
            ("event_driven", event_umple),
            ("hybrid", hybrid_umple),
        ):
            predicted_counts = parse_umple_counts(umple_text)
            macro_component_f1, component_metrics = evaluate_counts(
                case_id, predicted_counts, reference_counts
            )
            rows.append(
                {
                    "baseline_name": "structure_event",
                    "dataset_id": case_row["dataset_id"],
                    "sample_id": f"struct_event::{case_id}::{strategy_name}",
                    "case_id": case_id,
                    "case_name": case_row["case_name"],
                    "variant_id": case_id,
                    "variant_name": case_row["case_name"],
                    "sample_kind": "non_structured_nl_to_umple_state_machine",
                    "strategy_name": strategy_name,
                    "input_modality": case_row["input_modality"],
                    "input_text": optional_text(case_row["reference_prompt_text"]) or description,
                    "input_payload_json": json_dumps(
                        {
                            "system_description": description,
                            "reference_prompt_text": optional_text(case_row["reference_prompt_text"]),
                        }
                    ),
                    "reference_output_text": ref_row["reference_solution_text"],
                    "reference_output_json": json_dumps(
                        {
                            "reference_solution_text": ref_row["reference_solution_text"],
                            "reference_prompt_text": ref_row["reference_prompt_text"],
                            "reference_image_local_path": ref_row["reference_image_local_path"],
                        }
                    ),
                    "prediction_output_text": umple_text,
                    "prediction_output_json": json_dumps(
                        {
                            "generated_umple": umple_text,
                        }
                    ),
                    "reference_output_format": "umple",
                    "prediction_output_format": "umple",
                    "reference_counts_json": json_dumps(
                        {
                            "States": int(ref_row["reference_states_count"]),
                            "Transitions": int(ref_row["reference_transitions_count"]),
                            "Guards": int(ref_row["reference_guards_count"]),
                            "Actions": int(ref_row["reference_actions_count"]),
                            "Hierarchical states": int(
                                ref_row["reference_hierarchical_states_count"]
                            ),
                            "History States": int(ref_row["reference_history_states_count"]),
                            "Parallel Regions": int(ref_row["reference_parallel_regions_count"]),
                        }
                    ),
                    "prediction_counts_json": json.dumps(
                        predicted_counts, ensure_ascii=False, sort_keys=True
                    ),
                    "llm_provider": None,
                    "llm_model_name": llm.model,
                    "llm_raw_mode": None,
                    "is_repaired": False,
                    "evaluation_method": "manual_paper_protocol_approximated_by_count_based_component_macro_f1",
                    "primary_metric_name": "macro_component_f1",
                    "primary_metric_value": macro_component_f1,
                    "generated_umple": umple_text,
                    "predicted_counts_json": json.dumps(
                        predicted_counts, ensure_ascii=False, sort_keys=True
                    ),
                    "macro_component_f1": macro_component_f1,
                    "component_metrics_json": json.dumps(
                        component_metrics, ensure_ascii=False, sort_keys=True
                    ),
                }
        )

    pred_df = finalize_result_df(pd.DataFrame(rows))
    summary = {
        "baseline": "structure_event",
        "case_count": int(pred_df["case_id"].nunique()),
        "strategy_summary": {},
    }
    for strategy_name, part in pred_df.groupby("strategy_name"):
        summary["strategy_summary"][strategy_name] = {
            "macro_f1": float(part["macro_component_f1"].mean()),
            "case_count": int(len(part)),
        }
    write_parquet(pred_df, output_path)
    write_json(summary, summary_path)
