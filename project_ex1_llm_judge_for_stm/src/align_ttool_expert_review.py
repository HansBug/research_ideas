from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from config import RAW_ROOT, RESULTS_ROOT
from expert_review import ExpertReviewAgent, ExpertReviewRequest, result_to_flat_row
from expert_review.schema import to_dict
from io_utils import load_discussion_parquet, write_json, write_parquet


TTOOL_RESULTS_ODS = RAW_ROOT / "ttool-ai" / "results.ods"
ALIGNMENT_ROOT = RESULTS_ROOT / "ttool" / "expert_alignment"

CASE_FILE_ROWS = [
    {
        "case_id": "platooning",
        "case_name": "Platooning",
        "xml_path": RAW_ROOT / "ttool-ai" / "platooning" / "platoonings.xml",
    },
    {
        "case_id": "automated_braking",
        "case_name": "Automated Braking",
        "xml_path": RAW_ROOT / "ttool-ai" / "AutomatedBraking" / "automatedbraking.xml",
    },
    {
        "case_id": "space_based_system",
        "case_name": "Space-Based System",
        "xml_path": RAW_ROOT / "ttool-ai" / "spacebasedsystem" / "spacebasedsystem.xml",
    },
]

SHEET_TO_CASE = {
    "Platooning": ("platooning", "Platooning"),
    "Automated braking": ("automated_braking", "Automated Braking"),
    "Space-based system": ("space_based_system", "Space-Based System"),
}

PROMPT_VARIANTS: dict[str, dict[str, str]] = {
    "paper_rubric_v1": {
        "bd": (
            "You are grading a TTool AVATAR Block Diagram using the same style of expert human grading described in the TTool-AI paper. "
            "Return all scores normalized to the range 0.0 to 1.0, where 1.0 corresponds to 100/100. "
            "Review only the block diagram, not the internal state-machine behavior. "
            "Focus on: adequacy of the architecture to the specification, whether the chosen blocks capture the required system actors or subsystems, "
            "whether exchanges between blocks are reasonable and sufficient, readability, naming consistency, reasonableness of the number of blocks, "
            "and declared attributes or interfaces that look pointless, inconsistent, or unsupported. "
            "Use the full score range. A model with major missing participants or implausible communication should score low, even if it looks tidy. "
            "A model with a coherent decomposition and sensible exchanges should receive high credit even if its decomposition differs from another valid design."
        ),
        "smd": (
            "You are grading a TTool AVATAR State Machine Diagram set using the same style of expert human grading described in the TTool-AI paper. "
            "Return all scores normalized to the range 0.0 to 1.0, where 1.0 corresponds to 100/100. "
            "Review only the state-machine behavior, not the block-diagram decomposition by itself. "
            "Focus on: adequacy of the state-machine behavior to the specification, whether the behavior looks simulator-plausible and executable, "
            "whether key events, control paths, safety or fault paths, and reaction logic are represented, readability, naming consistency, "
            "reasonableness of state counts, declared attributes or signals that appear unused or unjustified, and obvious syntax or well-formedness problems. "
            "Use the full score range. Missing core behaviors, implausible transitions, or poorly grounded state logic should score low."
        ),
    },
    "paper_rubric_v2": {
        "bd": (
            "You are grading a high-level architecture or block diagram using a strict human expert style. "
            "Return all scores normalized to 0.0 to 1.0. Review only the architecture-level block diagram, not the detailed internal behavior. "
            "Judge it at the abstraction level of a block diagram: reward a coherent decomposition, the main actors/subsystems, and a sensible end-to-end communication chain. "
            "Do not heavily penalize the model merely because nonfunctional, timing, privacy, or fault-tolerance requirements are not each mapped to separate blocks, unless the architecture clearly contradicts them or omits a critical participant. "
            "Do penalize missing major participants, implausible communication paths, block counts that violate stated limits, duplicated or unsupported data-holder blocks, and obviously pointless attributes or interfaces. "
            "Human score calibration: 0.85+ means the architecture is largely specification-adequate despite imperfections; around 0.60 means partially adequate with important weaknesses; below 0.45 means the structural solution is seriously mismatched."
        ),
        "smd": (
            "You are grading a set of state-machine diagrams using a strict human expert style. "
            "Return all scores normalized to 0.0 to 1.0. Review only the behavioral state-machine logic. "
            "Focus on whether the operational control logic, fault handling, reaction paths, and communication-triggered behavior are actually modeled in a requirement-grounded way. "
            "Do not reward generic or placeholder behavior such as broad Idle/Processing loops, shallow state skeletons, duplicated transitions, or signal names with little semantic justification. "
            "High scores require that most core control paths and safety-relevant reactions are explicitly represented and behaviorally plausible. "
            "Human score calibration: 0.80+ means behavior is strong and fairly complete; 0.55 to 0.75 means partially adequate but with notable omissions; 0.30 to 0.50 means weak or generic behavior even if the model is parseable."
        ),
    },
    "paper_rubric_v3": {
        "bd": (
            "Act as a conservative human architecture reviewer. Score only the block diagram on a 0.0 to 1.0 scale. "
            "Use the specification primarily to check whether the main structural story is preserved: who detects danger, who assesses it, who sends commands, who communicates outward, and whether the declared exchanges support that story. "
            "Treat extra cosmetic or data-centric detail as a readability problem, not automatically as a catastrophic failure. "
            "Reserve very low scores for cases with broken architectural flow, missing core participants, or almost no justified exchanges."
        ),
        "smd": (
            "Act as a conservative human behavioral reviewer. Score only the state-machine behavior on a 0.0 to 1.0 scale. "
            "Look for real control logic rather than mere state names: triggers, guards, causal ordering, fault reactions, recovery, and communication behavior grounded in the specification. "
            "If many panels look generic, placeholder-like, or disconnected from the described behavior, score the model low even when the notation is parseable. "
            "Reserve high scores for behavior that is both specification-grounded and operationally plausible across the important scenarios."
        ),
    },
    "paper_rubric_v4": {
        "bd": (
            "You are simulating a practical human expert review of a high-level architecture/block diagram. Score on 0.0 to 1.0. "
            "Judge the model at architecture level, not at full behavioral or detailed safety-case level. "
            "Give substantial credit when the main structural narrative is present: the right major actors/subsystems appear, their responsibilities are sensible, and the communication chain roughly follows the specification. "
            "Treat extra message/data-holder blocks, overly detailed attributes, or modest abstraction mismatches as moderate clarity deductions rather than severe semantic failures, unless they break the core architecture. "
            "Only score very low when the main structural flow is wrong, major participants are absent, or exchanges are implausible or almost missing."
        ),
        "smd": (
            "You are simulating a practical human expert review of state-machine behavior models. Score on 0.0 to 1.0. "
            "Judge the model at the abstraction level of hand-built state machines from a textual requirement: reward domain-specific states, role-specific control flows, and the main causal behavior story even if not every edge case, timing detail, or quantitative constraint is encoded explicitly. "
            "The normalized summary may contain [initial] pseudostates and [action] nodes for send/receive/action constructs; do not treat those conventions as syntax errors by themselves. "
            "Penalize heavily only when the behavior is mostly generic skeleton logic, core causal reactions are missing, or the modeled roles and transitions are weakly grounded in the specification. "
            "A model can still deserve a high score when the main operational scenarios are present and recognizable, even if some detailed constraints remain implicit."
        ),
    },
    "paper_rubric_v5": {
        "bd": (
            "You are simulating a practical human review of a high-level architecture/block diagram. Score on 0.0 to 1.0. "
            "Use generous but disciplined credit for architecture-level adequacy: if the main actors/subsystems are present and the end-to-end interaction story is recognizable, the model can still deserve roughly 0.75 to 0.90 even when some detailed constraints, data abstractions, or supporting mechanisms are imperfect or implicit. "
            "Subtract moderately for extra data-holder blocks, noisy attributes, duplicated interfaces, or exceeding the requested block count. "
            "Subtract heavily only when the main architectural flow is broken, key participants are absent, or exchanges are implausible."
        ),
        "smd": (
            "You are simulating a practical human review of state-machine behavior models. Score on 0.0 to 1.0. "
            "At this abstraction level, give strong credit when the main operational scenarios are recognizable through domain-specific states and transitions across the important roles, even if some timing details, quantitative constraints, or secondary edge cases are only implicit. "
            "A model with clear role-specific behavior such as coordination, join/leave, braking, warning, or recovery can still deserve roughly 0.75 to 0.90 if those main scenarios are present and behaviorally plausible. "
            "The normalized summary may contain [initial] pseudostates and [action] nodes; do not count those conventions as syntax problems by themselves. "
            "Score below 0.50 mainly when the behavior collapses into generic placeholder loops, the major scenarios are not recognizable, or the causal chain is seriously under-modeled."
        ),
    },
}


@dataclass(slots=True)
class AlignmentJob:
    case_id: str
    case_name: str
    variant_name: str
    artifact_type: str
    prompt_variant: str
    prompt: str
    input_text: str
    pred_output: str
    human_score_100: float


def _compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _normalize_signal_value(value: str | None) -> tuple[str, str]:
    text = (value or "").strip()
    if text.startswith("in "):
        return text[3:].strip(), "in"
    if text.startswith("out "):
        return text[4:].strip(), "out"
    return text, ""


def _sheet_variant_name(case_id: str, test_no: int) -> str:
    if case_id == "platooning":
        return f"Platoon{test_no}"
    return f"System{test_no}"


def load_ttool_human_scores() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    workbook = pd.ExcelFile(TTOOL_RESULTS_ODS, engine="odf")
    for sheet_name, (case_id, case_name) in SHEET_TO_CASE.items():
        if sheet_name not in workbook.sheet_names:
            continue
        sheet = pd.read_excel(TTOOL_RESULTS_ODS, sheet_name=sheet_name, engine="odf")
        for _, row in sheet.iterrows():
            test_value = row.get("Unnamed: 1")
            if pd.isna(test_value):
                continue
            try:
                test_no = int(test_value)
            except Exception:
                continue
            rows.append(
                {
                    "case_id": case_id,
                    "case_name": case_name,
                    "variant_name": _sheet_variant_name(case_id, test_no),
                    "test_no": test_no,
                    "human_bd_score_100": float(row["Unnamed: 3"]),
                    "human_smd_score_100": float(row["Unnamed: 5"]),
                }
            )
    return pd.DataFrame(rows).sort_values(["case_id", "test_no"]).reset_index(drop=True)


def _block_point_map(block_panel: ET.Element) -> dict[str, str]:
    point_to_block: dict[str, str] = {}
    for component in block_panel.findall("./COMPONENT"):
        info = component.find("infoparam")
        if info is None or info.attrib.get("name") != "Block":
            continue
        block_name = info.attrib.get("value", "").strip()
        for point in component.findall("TGConnectingPoint"):
            point_id = point.attrib.get("id")
            if point_id:
                point_to_block[point_id] = block_name
    return point_to_block


def _parse_block_component(component: ET.Element) -> dict[str, Any]:
    info = component.find("infoparam")
    block_name = info.attrib.get("value", "").strip() if info is not None else ""
    extra = component.find("extraparam")
    attributes: list[dict[str, Any]] = []
    signals: list[dict[str, Any]] = []
    if extra is not None:
        for child in extra:
            if child.tag == "Attribute":
                attributes.append(
                    {
                        "name": child.attrib.get("id", "").strip(),
                        "type": child.attrib.get("typeOther") or child.attrib.get("type", "").strip(),
                    }
                )
            elif child.tag == "Signal":
                signal_name, direction = _normalize_signal_value(child.attrib.get("value"))
                if signal_name:
                    signals.append(
                        {
                            "name": signal_name,
                            "direction": direction,
                        }
                    )
    return {
        "name": block_name,
        "attributes": attributes,
        "signals": signals,
        "states": [],
        "transitions": [],
    }


def parse_block_diagram_summary(modeling: ET.Element, case_id: str, variant_name: str) -> dict[str, Any]:
    block_panel = modeling.find("./AVATARBlockDiagramPanel")
    if block_panel is None:
        return {
            "artifact_type": "ttool_avatar_block_diagram",
            "machine_name": f"{case_id}_{variant_name}_bd",
            "blocks": [],
            "signals": [],
            "counts": {},
            "notes": ["No AVATARBlockDiagramPanel found."],
        }

    point_to_block = _block_point_map(block_panel)
    blocks = [
        _parse_block_component(component)
        for component in block_panel.findall("./COMPONENT")
        if component.find("infoparam") is not None
        and component.find("infoparam").attrib.get("name") == "Block"
    ]
    exchanges: list[dict[str, Any]] = []
    unresolved_exchange_count = 0
    for connector in block_panel.findall("./CONNECTOR"):
        extra = connector.find("extraparam")
        p1 = connector.find("P1")
        p2 = connector.find("P2")
        source_block = point_to_block.get(p1.attrib.get("id", "") if p1 is not None else "", "")
        target_block = point_to_block.get(p2.attrib.get("id", "") if p2 is not None else "", "")
        if not source_block or not target_block:
            unresolved_exchange_count += 1
        extra_values = {child.tag: child.attrib.get("value", "") for child in list(extra) if extra is not None}
        source_signal, _ = _normalize_signal_value(extra_values.get("oso"))
        target_signal, _ = _normalize_signal_value(extra_values.get("isd"))
        signal_name = source_signal or target_signal or "unnamed_exchange"
        exchanges.append(
            {
                "name": signal_name,
                "direction": "out",
                "source_block": source_block,
                "target_block": target_block,
                "payload": [],
                "source_signal": source_signal,
                "target_signal": target_signal,
            }
        )

    declared_attributes = sum(len(block["attributes"]) for block in blocks)
    declared_signals = sum(len(block["signals"]) for block in blocks)
    return {
        "artifact_type": "ttool_avatar_block_diagram",
        "machine_name": f"{case_id}_{variant_name}_bd",
        "blocks": blocks,
        "signals": exchanges,
        "counts": {
            "block_count": len(blocks),
            "exchange_count": len(exchanges),
            "declared_attribute_count": declared_attributes,
            "declared_signal_count": declared_signals,
            "unresolved_exchange_count": unresolved_exchange_count,
        },
        "notes": [
            "This summary is intended for block-diagram grading only.",
            "Signals at top level represent block-to-block exchanges resolved from connector endpoints.",
        ],
    }


def _string_token_set(values: list[str]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", value):
            tokens.add(token.lower())
    return tokens


def _label_smd_node(name: str | None, node_type: str | None) -> str:
    clean = str(name or "").strip()
    if node_type == "start_state":
        return "[initial]"
    if node_type == "other":
        return f"[action] {clean}" if clean else "[action]"
    return clean or "[unnamed]"


def build_smd_summary(
    case_id: str,
    variant_name: str,
    block_summary: dict[str, Any],
    panel_df: pd.DataFrame,
    state_df: pd.DataFrame,
    transition_df: pd.DataFrame,
) -> dict[str, Any]:
    variant_panels = (
        panel_df[(panel_df["case_id"] == case_id) & (panel_df["variant_name"] == variant_name)]
        .copy()
        .sort_values("panel_name")
    )
    variant_states = state_df[(state_df["case_id"] == case_id) & (state_df["variant_name"] == variant_name)].copy()
    variant_transitions = transition_df[
        (transition_df["case_id"] == case_id) & (transition_df["variant_name"] == variant_name)
    ].copy()

    block_by_name = {block["name"]: block for block in block_summary.get("blocks", [])}
    blocks: list[dict[str, Any]] = []
    panel_rows: list[dict[str, Any]] = []
    model_strings: list[str] = []

    for _, panel in variant_panels.iterrows():
        panel_name = str(panel["panel_name"])
        panel_states = variant_states[variant_states["panel_name"] == panel_name].copy()
        panel_transitions = variant_transitions[variant_transitions["panel_name"] == panel_name].copy()
        node_type_map = {
            str(row["node_name"]): str(row["node_type"])
            for _, row in panel_states[["node_name", "node_type"]].dropna().iterrows()
            if str(row["node_name"]).strip()
        }

        state_names = [
            str(name)
            for name in panel_states.loc[panel_states["node_type"] == "state", "node_name"].dropna().tolist()
            if str(name).strip()
        ]
        other_nodes = [
            str(name)
            for name in panel_states.loc[panel_states["node_type"] != "state", "node_name"].dropna().tolist()
            if str(name).strip() and str(name).strip().lower() != "null"
        ]

        transitions = []
        initial_transition_count = 0
        action_node_transition_count = 0
        state_to_state_transition_count = 0
        for _, trans in panel_transitions.iterrows():
            source_name = str(trans.get("source_node_name") or "").strip()
            target_name = str(trans.get("target_node_name") or "").strip()
            source_type = str(trans.get("source_node_type") or node_type_map.get(source_name) or "").strip()
            target_type = str(trans.get("target_node_type") or node_type_map.get(target_name) or "").strip()
            transition_payload = {
                "source": _label_smd_node(source_name, source_type),
                "target": _label_smd_node(target_name, target_type),
                "source_kind": source_type or "unknown",
                "target_kind": target_type or "unknown",
                "event": str(trans.get("guard_or_trigger") or "").strip(),
                "guard": str(trans.get("guard_or_trigger") or "").strip(),
                "action": str(trans.get("actions") or "").strip(),
            }
            if transition_payload["source"] or transition_payload["target"]:
                transitions.append(transition_payload)
                if source_type == "start_state" or target_type == "start_state":
                    initial_transition_count += 1
                if source_type == "other" or target_type == "other":
                    action_node_transition_count += 1
                if source_type == "state" and target_type == "state":
                    state_to_state_transition_count += 1
                model_strings.extend(
                    [
                        transition_payload["source"],
                        transition_payload["target"],
                        transition_payload["event"],
                        transition_payload["guard"],
                        transition_payload["action"],
                    ]
                )

        model_strings.extend(state_names)
        model_strings.extend(other_nodes)
        declared_block = block_by_name.get(panel_name, {"attributes": [], "signals": []})
        block_attributes = list(declared_block.get("attributes", []))
        block_signals = list(declared_block.get("signals", []))

        blocks.append(
            {
                "name": panel_name,
                "attributes": block_attributes,
                "signals": block_signals,
                "states": [
                    {
                        "name": name,
                        "parent": None,
                        "parallel_group": None,
                        "is_history": False,
                        "is_initial": name.lower() == "start",
                    }
                    for name in sorted(set(state_names))
                ],
                "transitions": transitions,
            }
        )
        panel_rows.append(
            {
                "panel_name": panel_name,
                "start_pseudostate_count": int(panel.get("start_pseudostate_count") or 0),
                "state_count": int(panel.get("state_count") or 0),
                "transition_count": int(panel.get("transition_count") or 0),
                "nonempty_guard_count": int(panel.get("nonempty_guard_count") or 0),
                "nonempty_action_count": int(panel.get("nonempty_action_count") or 0),
                "initial_transition_count": initial_transition_count,
                "action_node_transition_count": action_node_transition_count,
                "state_to_state_transition_count": state_to_state_transition_count,
                "state_names": sorted(set(state_names)),
                "other_nodes": sorted(set(other_nodes)),
            }
        )

    used_tokens = _string_token_set(model_strings)
    unused_attribute_candidates: list[dict[str, Any]] = []
    for block in blocks:
        unused = []
        for attribute in block["attributes"]:
            name = str(attribute.get("name") or "").strip()
            if name and name.lower() not in used_tokens:
                unused.append(name)
        if unused:
            unused_attribute_candidates.append({"block": block["name"], "attributes": unused})

    return {
        "artifact_type": "ttool_avatar_state_machine_diagrams",
        "machine_name": f"{case_id}_{variant_name}_smd",
        "blocks": blocks,
        "panels": panel_rows,
        "counts": {
            "panel_count": int(len(panel_rows)),
            "state_count": int(variant_states[variant_states["node_type"] == "state"].shape[0]),
            "transition_count": int(variant_transitions.shape[0]),
            "send_signal_node_count": int(
                variant_states[variant_states["component_type_code"] == "5103"].shape[0]
            ),
            "initial_pseudostate_count": int(
                variant_states[variant_states["node_type"] == "start_state"].shape[0]
            ),
            "action_node_count": int(variant_states[variant_states["node_type"] == "other"].shape[0]),
            "state_to_state_transition_count": int(
                variant_transitions[
                    (variant_transitions["source_node_type"] == "state")
                    & (variant_transitions["target_node_type"] == "state")
                ].shape[0]
            ),
        },
        "unused_attribute_candidates": unused_attribute_candidates,
        "notes": [
            "This summary is intended for state-machine grading only.",
            "unused_attribute_candidates are heuristic lexical findings, not ground truth.",
            "[initial] denotes a start pseudostate. [action] X denotes a non-state action/signal node rather than a normal state.",
        ],
    }


def build_ttool_artifact_jobs(prompt_variant: str) -> list[AlignmentJob]:
    if prompt_variant not in PROMPT_VARIANTS:
        raise KeyError(f"Unknown prompt variant: {prompt_variant}")

    models = load_discussion_parquet("ttool_ai_models").copy()
    panels = load_discussion_parquet("ttool_ai_state_machine_panels").copy()
    states = load_discussion_parquet("ttool_ai_states").copy()
    transitions = load_discussion_parquet("ttool_ai_transitions").copy()
    human = load_ttool_human_scores()
    merged = models.merge(human, on=["case_id", "case_name", "variant_name"], how="inner")

    modeling_map: dict[tuple[str, str], ET.Element] = {}
    for case in CASE_FILE_ROWS:
        root = ET.parse(case["xml_path"]).getroot()
        for modeling in root.findall("./Modeling"):
            modeling_map[(case["case_id"], modeling.attrib["nameTab"])] = modeling

    jobs: list[AlignmentJob] = []
    for _, row in merged.sort_values(["case_id", "variant_name"]).iterrows():
        case_id = str(row["case_id"])
        case_name = str(row["case_name"])
        variant_name = str(row["variant_name"])
        modeling = modeling_map[(case_id, variant_name)]
        block_summary = parse_block_diagram_summary(modeling, case_id, variant_name)
        smd_summary = build_smd_summary(case_id, variant_name, block_summary, panels, states, transitions)
        prompt_cfg = PROMPT_VARIANTS[prompt_variant]
        jobs.append(
            AlignmentJob(
                case_id=case_id,
                case_name=case_name,
                variant_name=variant_name,
                artifact_type="bd",
                prompt_variant=prompt_variant,
                prompt=prompt_cfg["bd"],
                input_text=str(row["input_spec_text"]),
                pred_output=_compact_json(block_summary),
                human_score_100=float(row["human_bd_score_100"]),
            )
        )
        jobs.append(
            AlignmentJob(
                case_id=case_id,
                case_name=case_name,
                variant_name=variant_name,
                artifact_type="smd",
                prompt_variant=prompt_variant,
                prompt=prompt_cfg["smd"],
                input_text=str(row["input_spec_text"]),
                pred_output=_compact_json(smd_summary),
                human_score_100=float(row["human_smd_score_100"]),
            )
        )
    return jobs


def _cache_file(prompt_variant: str, case_id: str, variant_name: str, artifact_type: str) -> Path:
    return ALIGNMENT_ROOT / prompt_variant / "cache" / f"{case_id}__{variant_name}__{artifact_type}.json"


def review_job(agent: ExpertReviewAgent, job: AlignmentJob, force: bool = False) -> dict[str, Any]:
    cache_path = _cache_file(job.prompt_variant, job.case_id, job.variant_name, job.artifact_type)
    if cache_path.exists() and not force:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        return cached

    request = ExpertReviewRequest(
        prompt=job.prompt,
        input_text=job.input_text,
        pred_output=job.pred_output,
        ref_output=None,
    )
    result = agent.review(request)
    payload = {
        "case_id": job.case_id,
        "case_name": job.case_name,
        "variant_name": job.variant_name,
        "artifact_type": job.artifact_type,
        "prompt_variant": job.prompt_variant,
        "human_score_100": job.human_score_100,
        "predicted_score_100": float(result.overall_score) * 100.0,
        "absolute_error": abs(float(result.overall_score) * 100.0 - job.human_score_100),
        "request": {
            "prompt": job.prompt,
            "input_text": job.input_text,
            "pred_output": job.pred_output,
            "ref_output": None,
        },
        "review_result": to_dict(result),
        "flat_row": {
            "case_id": job.case_id,
            "case_name": job.case_name,
            "variant_name": job.variant_name,
            "artifact_type": job.artifact_type,
            "prompt_variant": job.prompt_variant,
            "human_score_100": job.human_score_100,
            "predicted_score_100": float(result.overall_score) * 100.0,
            "absolute_error": abs(float(result.overall_score) * 100.0 - job.human_score_100),
            **result_to_flat_row(result),
        },
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def _safe_corr(series_a: pd.Series, series_b: pd.Series, method: str) -> float | None:
    if len(series_a) < 2:
        return None
    if method == "spearman":
        value = series_a.rank(method="average").corr(series_b.rank(method="average"), method="pearson")
    else:
        value = series_a.corr(series_b, method=method)
    if pd.isna(value):
        return None
    return float(value)


def compute_alignment_metrics(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {"review_count": 0}
    abs_error = (df["predicted_score_100"] - df["human_score_100"]).abs()
    sq_error = (df["predicted_score_100"] - df["human_score_100"]) ** 2
    return {
        "review_count": int(len(df)),
        "human_score_mean": float(df["human_score_100"].mean()),
        "predicted_score_mean": float(df["predicted_score_100"].mean()),
        "mae": float(abs_error.mean()),
        "rmse": float(math.sqrt(float(sq_error.mean()))),
        "pearson": _safe_corr(df["predicted_score_100"], df["human_score_100"], "pearson"),
        "spearman": _safe_corr(df["predicted_score_100"], df["human_score_100"], "spearman"),
        "within_5": float((abs_error <= 5).mean()),
        "within_10": float((abs_error <= 10).mean()),
        "within_15": float((abs_error <= 15).mean()),
    }


def run_alignment(prompt_variant: str, force: bool = False, limit: int | None = None) -> dict[str, Any]:
    jobs = build_ttool_artifact_jobs(prompt_variant)
    if limit is not None:
        jobs = jobs[:limit]
    agent = ExpertReviewAgent(timeout=240)
    payloads = [review_job(agent, job, force=force) for job in jobs]
    rows = [item["flat_row"] for item in payloads]
    df = pd.DataFrame(rows)

    summary = {
        "prompt_variant": prompt_variant,
        "overall_metrics": compute_alignment_metrics(df),
        "by_artifact_type": {
            artifact_type: compute_alignment_metrics(part.copy())
            for artifact_type, part in df.groupby("artifact_type")
        },
        "by_case": {
            case_id: compute_alignment_metrics(part.copy())
            for case_id, part in df.groupby("case_id")
        },
    }

    result_root = ALIGNMENT_ROOT / prompt_variant
    write_parquet(df, result_root / "alignment_reviews.parquet")
    write_json(summary, result_root / "alignment_summary.json")
    write_json(payloads, result_root / "alignment_payloads.json")
    return {
        "summary": summary,
        "dataframe": df,
        "result_root": result_root,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-variant", default="paper_rubric_v1", choices=sorted(PROMPT_VARIANTS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    result = run_alignment(args.prompt_variant, force=args.force, limit=args.limit)
    print(
        json.dumps(
            {
                "prompt_variant": args.prompt_variant,
                "result_root": str(result["result_root"]),
                "overall_metrics": result["summary"]["overall_metrics"],
                "by_artifact_type": result["summary"]["by_artifact_type"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
