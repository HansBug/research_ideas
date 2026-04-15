from __future__ import annotations

import json
from typing import Any

import pandas as pd

from eval_utils import ensure_json, macro_f1, normalize_id, prf_from_counts, prf_from_sets
from io_utils import baseline_result_dir, load_discussion_parquet, write_json, write_parquet
from llm_client import LLMClient


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


def build_reference_sets(
    fragment_id: str, states_df: pd.DataFrame, rules_df: pd.DataFrame
) -> tuple[set[str], set[str]]:
    state_set = {
        f"{normalize_id(row.state_name)}|{normalize_id(row.parent_state_name)}"
        for row in states_df[states_df["fragment_id"] == fragment_id].itertuples()
    }
    rule_set = {
        f"{normalize_id(row.target_variable)}|{normalize_id(row.assigned_value)}|{normalize_id(row.condition)}"
        for row in rules_df[rules_df["fragment_id"] == fragment_id].itertuples()
    }
    return state_set, rule_set


def build_prediction_sets(payload: dict[str, Any]) -> tuple[set[str], set[str]]:
    state_set = {
        f"{normalize_id(state.get('name'))}|{normalize_id(state.get('parent'))}"
        for state in payload.get("states", []) or []
        if isinstance(state, dict) and state.get("name")
    }
    rule_set = {
        f"{normalize_id(rule.get('target_variable'))}|"
        f"{normalize_id(rule.get('assigned_value'))}|"
        f"{normalize_id(rule.get('condition'))}"
        for rule in payload.get("rules", []) or []
        if isinstance(rule, dict) and rule.get("target_variable")
    }
    return state_set, rule_set


def run_nimbus() -> None:
    result_dir = baseline_result_dir("nimbus")
    output_path = result_dir / "predictions.parquet"
    summary_path = result_dir / "summary.json"
    if output_path.exists() and summary_path.exists():
        return

    fragments = load_discussion_parquet("light_control_nimbus_fragments").copy()
    states_df = load_discussion_parquet("light_control_nimbus_states")
    rules_df = load_discussion_parquet("light_control_nimbus_rules")
    llm = LLMClient()

    rows: list[dict[str, Any]] = []
    for _, fragment in fragments.iterrows():
        reference_states, reference_rules = build_reference_sets(
            fragment["fragment_id"], states_df, rules_df
        )
        system_prompt = (
            "You reproduce the Nimbus Light Control case. Convert the requirement fragment into "
            "a concise RSML-e inspired JSON representation."
        )
        user_prompt = (
            f"Fragment title: {fragment['fragment_title']}\n"
            f"Sample kind: {fragment['sample_kind']}\n"
            f"Abstraction level: {fragment['abstraction_level']}\n"
            "Requirement fragment:\n"
            f"{fragment['input_requirement_text']}\n\n"
            "Return JSON only:\n"
            "{\n"
            '  "states": [\n'
            '    {"name": "StateName", "parent": null}\n'
            "  ],\n"
            '  "rules": [\n'
            '    {"target_variable": "Variable", "assigned_value": "Value", "condition": "Condition"}\n'
            "  ]\n"
            "}\n"
            "Use exact RSML-e style identifiers where the paper fragment already implies them."
        )
        payload = _generate_json(
            llm,
            cache_key=f"nimbus:{fragment['fragment_id']}",
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_output_tokens=2600,
        )
        predicted_states, predicted_rules = build_prediction_sets(payload)
        metrics = {
            "states": prf_from_counts(len(predicted_states), len(reference_states)),
            "rules": prf_from_counts(len(predicted_rules), len(reference_rules)),
        }
        strict_metrics = {}
        if reference_states:
            strict_metrics["states"] = prf_from_sets(predicted_states, reference_states)
        if reference_rules:
            strict_metrics["rules"] = prf_from_sets(predicted_rules, reference_rules)
        rows.append(
            {
                "fragment_id": fragment["fragment_id"],
                "fragment_title": fragment["fragment_title"],
                "sample_kind": fragment["sample_kind"],
                "prediction_json": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                "pred_state_count": len(predicted_states),
                "ref_state_count": len(reference_states),
                "pred_rule_count": len(predicted_rules),
                "ref_rule_count": len(reference_rules),
                "macro_f1": macro_f1(metrics.values()),
                "strict_macro_f1": macro_f1(strict_metrics.values()),
                "metrics_json": json.dumps(metrics, ensure_ascii=False, sort_keys=True),
                "strict_metrics_json": json.dumps(
                    strict_metrics, ensure_ascii=False, sort_keys=True
                ),
            }
        )

    pred_df = pd.DataFrame(rows)
    summary = {
        "baseline": "nimbus",
        "fragment_count": int(len(pred_df)),
        "overall_macro_f1": float(pred_df["macro_f1"].mean()),
        "overall_strict_macro_f1": float(pred_df["strict_macro_f1"].mean()),
        "fragment_summary": {
            row["fragment_id"]: {
                "title": row["fragment_title"],
                "macro_f1": float(row["macro_f1"]),
                "strict_macro_f1": float(row["strict_macro_f1"]),
            }
            for _, row in pred_df.iterrows()
        },
    }
    write_parquet(pred_df, output_path)
    write_json(summary, summary_path)
