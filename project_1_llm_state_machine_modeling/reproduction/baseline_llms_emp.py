from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from eval_utils import json_dumps, macro_f1, prf_from_counts
from io_utils import baseline_result_dir, load_discussion_parquet, write_json, write_parquet
from llm_client import LLMClient, LLMResult
from result_schema import finalize_result_df


COMPONENTS_BY_DIAGRAM_TYPE = {
    "stm": [
        ("basic_state_count", "States"),
        ("basic_transition_count", "Transitions"),
        ("basic_action_annotation_count", "Actions"),
        ("basic_hierarchical_state_count", "Hierarchical states"),
    ],
    "sd": [
        ("basic_participant_count", "Participants"),
        ("basic_message_count", "Messages"),
        ("basic_action_annotation_count", "Interaction fragments"),
    ],
    "act": [
        ("basic_activity_action_count", "Actions"),
        ("basic_decision_count", "Decisions"),
        ("basic_parallel_count", "Parallel regions"),
    ],
}


@dataclass
class GenerationRecord:
    row_id: int
    diagram_type: str
    provider: str
    raw_mode: str
    repaired: bool
    generated_plantuml: str
    pred_diagram_type: str
    pred_basic_state_count: int | None
    pred_basic_transition_count: int | None
    pred_basic_action_annotation_count: int | None
    pred_basic_hierarchical_state_count: int | None
    pred_basic_participant_count: int | None
    pred_basic_message_count: int | None
    pred_basic_activity_action_count: int | None
    pred_basic_decision_count: int | None
    pred_basic_parallel_count: int | None
    macro_component_f1: float
    component_metrics_json: str


def classify_plantuml(text: str | None) -> str:
    if not text:
        return "missing"
    lower = text.lower()
    if "participant " in lower or "actor " in lower or "autonumber" in lower:
        return "sd"
    if "[*]" in lower or ("state " in lower and "-->" in lower):
        return "stm"
    if "start" in lower or "stop" in lower or "split" in lower or "fork" in lower:
        return "act"
    return "other"


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text or None


def extract_plantuml(text: str) -> str:
    fenced = re.search(r"```(?:plantuml|puml)?\s*(.*?)```", text, re.S | re.I)
    if fenced:
        body = fenced.group(1).strip()
        if "@startuml" in body and "@enduml" in body:
            return body
    inline = re.search(r"(@startuml.*?@enduml)", text, re.S | re.I)
    if inline:
        return inline.group(1).strip()
    return text.strip()


def parse_stm_features(text: str) -> dict[str, int | None]:
    aliases: dict[str, str] = {}
    state_names: set[str] = set()
    transition_count = 0
    action_line_count = 0
    hierarchical_state_count = 0

    state_decl_re = re.compile(
        r'^\s*state\s+"?(?P<label>[^"{]+?)"?(\s+as\s+(?P<alias>[A-Za-z_][\w]*))?\s*\{?\s*$'
    )
    trans_re = re.compile(r"^\s*(?P<src>.+?)\s*[-.]*->+\s*(?P<dst>.+?)(\s*:\s*(?P<label>.*))?$")

    def normalize_state_token(token: str) -> str | None:
        token = token.strip().split(":", 1)[0].strip().strip('"')
        if token in {"[*]", "*"}:
            return None
        return aliases.get(token, token) or None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("@"):
            continue
        if line.endswith("{") and line.startswith("state "):
            hierarchical_state_count += 1
        match = state_decl_re.match(line)
        if match:
            label = normalize_text(match.group("label"))
            alias = normalize_text(match.group("alias"))
            if label:
                state_names.add(label)
                if alias:
                    aliases[alias] = label
            continue
        if "entry/" in line or "exit/" in line or "do/" in line:
            action_line_count += 1
            state_name = normalize_state_token(line.split(":", 1)[0])
            if state_name:
                state_names.add(state_name)
            continue
        match = trans_re.match(line)
        if match and "participant" not in line and "actor" not in line:
            src = normalize_state_token(match.group("src"))
            dst = normalize_state_token(match.group("dst"))
            if src:
                state_names.add(src)
            if dst:
                state_names.add(dst)
            transition_count += 1
    return {
        "basic_state_count": len(state_names),
        "basic_transition_count": transition_count,
        "basic_action_annotation_count": action_line_count,
        "basic_hierarchical_state_count": hierarchical_state_count,
        "basic_participant_count": None,
        "basic_message_count": None,
        "basic_activity_action_count": None,
        "basic_decision_count": None,
        "basic_parallel_count": None,
    }


def parse_sd_features(text: str) -> dict[str, int | None]:
    participant_count = 0
    message_count = 0
    fragment_count = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("@"):
            continue
        if re.match(r"^(participant|actor)\b", line, re.I):
            participant_count += 1
        if re.search(r"-+>+|<+-+", line):
            message_count += 1
        if re.match(r"^(alt|opt|loop|par|break|critical|group)\b", line, re.I):
            fragment_count += 1
    return {
        "basic_state_count": None,
        "basic_transition_count": None,
        "basic_action_annotation_count": fragment_count,
        "basic_hierarchical_state_count": None,
        "basic_participant_count": participant_count,
        "basic_message_count": message_count,
        "basic_activity_action_count": None,
        "basic_decision_count": None,
        "basic_parallel_count": None,
    }


def parse_act_features(text: str) -> dict[str, int | None]:
    action_count = 0
    decision_count = 0
    parallel_count = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("@"):
            continue
        if line.startswith(":") or line.startswith('"'):
            action_count += 1
        if re.match(r"^(if|elseif|else)\b", line, re.I):
            decision_count += 1
        if re.match(r"^(fork|split)\b", line, re.I):
            parallel_count += 1
    return {
        "basic_state_count": None,
        "basic_transition_count": None,
        "basic_action_annotation_count": None,
        "basic_hierarchical_state_count": None,
        "basic_participant_count": None,
        "basic_message_count": None,
        "basic_activity_action_count": action_count,
        "basic_decision_count": decision_count,
        "basic_parallel_count": parallel_count,
    }


def parse_features(text: str, diagram_type: str) -> dict[str, int | None]:
    if diagram_type == "stm":
        return parse_stm_features(text)
    if diagram_type == "sd":
        return parse_sd_features(text)
    if diagram_type == "act":
        return parse_act_features(text)
    return {
        "basic_state_count": None,
        "basic_transition_count": None,
        "basic_action_annotation_count": None,
        "basic_hierarchical_state_count": None,
        "basic_participant_count": None,
        "basic_message_count": None,
        "basic_activity_action_count": None,
        "basic_decision_count": None,
        "basic_parallel_count": None,
    }


def safe_int(value: Any) -> int:
    if value is None or pd.isna(value):
        return 0
    return int(value)


def build_generation_prompt(row: pd.Series) -> tuple[str, str]:
    diagram_name = {
        "stm": "SysML state machine",
        "act": "SysML activity diagram",
        "sd": "SysML sequence diagram",
    }[row["diagram_type"]]
    system_prompt = (
        "You reproduce the llms_emp baseline. Generate only valid PlantUML for the requested "
        "SysML behavior model. Keep the output concise and deterministic."
    )
    user_prompt = (
        f"Target diagram type: {diagram_name}\n"
        "Requirements:\n"
        f"{row['requirements_description']}\n\n"
        "Return only a PlantUML block from @startuml to @enduml."
    )
    return system_prompt, user_prompt


def build_repair_prompt(row: pd.Series, broken_output: str, feedback: str) -> tuple[str, str]:
    system_prompt = (
        "You are repairing a PlantUML behavior model for the llms_emp reproduction. "
        "Return only corrected PlantUML."
    )
    user_prompt = (
        f"Target diagram type: {row['diagram_type']}\n"
        "Requirements:\n"
        f"{row['requirements_description']}\n\n"
        "Previous output:\n"
        f"{broken_output}\n\n"
        "Problems to fix:\n"
        f"{feedback}\n\n"
        "Return only a corrected PlantUML block."
    )
    return system_prompt, user_prompt


def evaluate_prediction(row: pd.Series, features: dict[str, int | None]) -> tuple[float, dict[str, dict[str, float | int]]]:
    component_metrics: dict[str, dict[str, float | int]] = {}
    for field_name, label in COMPONENTS_BY_DIAGRAM_TYPE[row["diagram_type"]]:
        metric = prf_from_counts(safe_int(features.get(field_name)), safe_int(row[field_name]))
        component_metrics[label] = metric
    return macro_f1(component_metrics.values()), component_metrics


def _generate_one(llm: LLMClient, row: pd.Series) -> tuple[LLMResult, str, bool]:
    system_prompt, user_prompt = build_generation_prompt(row)
    initial = llm.generate(
        system_prompt,
        user_prompt,
        max_output_tokens=1600,
        cache_key=f"llms_emp:{row['row_id']}:initial",
    )
    candidate = extract_plantuml(initial.text)
    pred_type = classify_plantuml(candidate)
    pred_features = parse_features(candidate, row["diagram_type"])

    feedback: list[str] = []
    if "@startuml" not in candidate or "@enduml" not in candidate:
        feedback.append("Missing complete PlantUML delimiters.")
    if pred_type != row["diagram_type"]:
        feedback.append(
            f"Predicted diagram type looks like {pred_type}, but the target type is {row['diagram_type']}."
        )
    if all(safe_int(pred_features.get(field)) == 0 for field, _ in COMPONENTS_BY_DIAGRAM_TYPE[row["diagram_type"]]):
        feedback.append("The diagram contains almost no recognizable structural elements.")

    if not feedback:
        return initial, candidate, False

    repair_system_prompt, repair_user_prompt = build_repair_prompt(row, candidate, "\n".join(feedback))
    repaired = llm.generate(
        repair_system_prompt,
        repair_user_prompt,
        max_output_tokens=1800,
        cache_key=f"llms_emp:{row['row_id']}:repair",
    )
    return repaired, extract_plantuml(repaired.text), True


def run_llms_emp() -> None:
    result_dir = baseline_result_dir("llms_emp")
    output_path = result_dir / "predictions.parquet"
    summary_path = result_dir / "summary.json"
    if output_path.exists() and summary_path.exists():
        return

    df = load_discussion_parquet("llms_emp_complete_samples").copy()
    llm = LLMClient()
    rows: list[GenerationRecord] = []
    for _, row in df.iterrows():
        result, plantuml, repaired = _generate_one(llm, row)
        pred_diagram_type = classify_plantuml(plantuml)
        pred_features = parse_features(plantuml, row["diagram_type"])
        macro_component_f1, component_metrics = evaluate_prediction(row, pred_features)
        rows.append(
            GenerationRecord(
                row_id=int(row["row_id"]),
                diagram_type=row["diagram_type"],
                provider=result.provider,
                raw_mode=result.raw_mode,
                repaired=repaired,
                generated_plantuml=plantuml,
                pred_diagram_type=pred_diagram_type,
                pred_basic_state_count=pred_features["basic_state_count"],
                pred_basic_transition_count=pred_features["basic_transition_count"],
                pred_basic_action_annotation_count=pred_features["basic_action_annotation_count"],
                pred_basic_hierarchical_state_count=pred_features["basic_hierarchical_state_count"],
                pred_basic_participant_count=pred_features["basic_participant_count"],
                pred_basic_message_count=pred_features["basic_message_count"],
                pred_basic_activity_action_count=pred_features["basic_activity_action_count"],
                pred_basic_decision_count=pred_features["basic_decision_count"],
                pred_basic_parallel_count=pred_features["basic_parallel_count"],
                macro_component_f1=macro_component_f1,
                component_metrics_json=json.dumps(component_metrics, ensure_ascii=False, sort_keys=True),
            )
        )

    pred_df = pd.DataFrame(asdict(record) for record in rows)
    merged = df.merge(pred_df, on=["row_id", "diagram_type"], how="left")
    merged["baseline_name"] = "llms_emp"
    merged["sample_id"] = merged["row_id"].map(lambda value: f"llms_emp::{int(value)}")
    merged["case_id"] = merged["sample_id"]
    merged["case_name"] = merged["model_name"]
    merged["variant_id"] = merged["diagram_type"]
    merged["variant_name"] = merged["diagram_type"]
    merged["sample_kind"] = merged["diagram_type"]
    merged["strategy_name"] = "single_prompt_with_optional_repair"
    merged["input_text"] = merged["requirements_description"]
    merged["input_payload_json"] = merged.apply(
        lambda row: json_dumps(
            {
                "diagram_type": row["diagram_type"],
                "requirements_description": row["requirements_description"],
            }
        ),
        axis=1,
    )
    merged["reference_output_text"] = merged["plantuml_code"]
    merged["reference_output_json"] = merged.apply(
        lambda row: json_dumps(
            {
                "diagram_type": row["diagram_type"],
                "plantuml_code": row["plantuml_code"],
            }
        ),
        axis=1,
    )
    merged["prediction_output_text"] = merged["generated_plantuml"]
    merged["prediction_output_json"] = merged.apply(
        lambda row: json_dumps(
            {
                "diagram_type": row["pred_diagram_type"],
                "plantuml_code": row["generated_plantuml"],
            }
        ),
        axis=1,
    )
    merged["reference_output_format"] = "plantuml"
    merged["prediction_output_format"] = "plantuml"
    merged["reference_counts_json"] = merged.apply(
        lambda row: json_dumps(
            {
                field_name: safe_int(row[field_name])
                for field_name, _ in COMPONENTS_BY_DIAGRAM_TYPE[row["diagram_type"]]
            }
        ),
        axis=1,
    )
    merged["prediction_counts_json"] = merged.apply(
        lambda row: json_dumps(
            {
                field_name: safe_int(row[f"pred_{field_name}"])
                for field_name, _ in COMPONENTS_BY_DIAGRAM_TYPE[row["diagram_type"]]
            }
        ),
        axis=1,
    )
    merged["llm_provider"] = merged["provider"]
    merged["llm_model_name"] = llm.model
    merged["llm_raw_mode"] = merged["raw_mode"]
    merged["is_repaired"] = merged["repaired"]
    merged["evaluation_method"] = (
        "count_based_component_macro_f1_over_reference_plantuml_features"
    )
    merged["primary_metric_name"] = "macro_component_f1"
    merged["primary_metric_value"] = merged["macro_component_f1"]
    merged = finalize_result_df(merged)
    summary = {
        "baseline": "llms_emp",
        "sample_count": int(len(merged)),
        "overall_macro_f1": float(merged["macro_component_f1"].mean()),
        "diagram_type_summary": {},
    }
    for diagram_type, part in merged.groupby("diagram_type"):
        summary["diagram_type_summary"][diagram_type] = {
            "sample_count": int(len(part)),
            "macro_f1": float(part["macro_component_f1"].mean()),
            "repair_rate": float(part["repaired"].mean()),
            "provider_counts": part["provider"].value_counts().to_dict(),
        }
    write_parquet(merged, output_path)
    write_json(summary, summary_path)
