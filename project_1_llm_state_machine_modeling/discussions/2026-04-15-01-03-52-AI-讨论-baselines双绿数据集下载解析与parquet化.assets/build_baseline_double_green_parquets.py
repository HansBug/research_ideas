#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import pandas as pd


RAW_ROOT_DEFAULT = Path("/tmp/baseline_double_green/raw")

LLMS_EMP_DATASET_URL = (
    "https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6"
)
TTOOL_AI_REPO_URL = "https://github.com/zebradile/ttool-ai"
LIGHT_CASE_ORIGINAL_URL = (
    "https://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced/"
    "papers/Light%20Control%20Case%20Study.pdf"
)
LIGHT_CASE_NIMBUS_URL = (
    "https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/"
    "light-case-jucs.pdf"
)
LIGHT_CASE_NIMBUS_HTML_URL = (
    "https://www.jucs.org/jucs_6_7/requirements_capture_and_evaluation/"
    "Thompson_J_M.html"
)
STRUCTURE_EVENT_DRIVEN_ARTIFACT_URL = (
    "https://anonymous.4open.science/r/llm_state_machine_modeling/"
)
STRUCTURE_EVENT_DRIVEN_DESCRIPTIONS_URL = (
    "https://anonymous.4open.science/api/repo/llm_state_machine_modeling/file/"
    "backend/resources/state_machine_descriptions.py"
)
STRUCTURE_EVENT_DRIVEN_NSHOT_URL = (
    "https://anonymous.4open.science/api/repo/llm_state_machine_modeling/file/"
    "backend/resources/n_shot_examples_single_prompt.py"
)


def json_compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value)
    if not text.strip():
        return None
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def extract_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1 : end]).strip()


def clean_jina_wrapper(text: str) -> str:
    marker = "Markdown Content:\n"
    if marker in text:
        return text.split(marker, 1)[1].strip()
    return text


def classify_llms_emp_plantuml(text: str | None) -> str:
    if not text:
        return "missing"
    lower = text.lower()
    if "participant " in lower or "actor " in lower or "autonumber" in lower:
        return "sd"
    if "[*]" in lower or "state " in lower or "-->" in lower:
        return "stm"
    if "start" in lower or "stop" in lower or "split" in lower or "fork" in lower:
        return "act"
    return "other"


def llms_emp_metamodel(diagram_type: str) -> str:
    return {
        "stm": "SysML v1.6 state machine expressed in PlantUML",
        "act": "SysML v1.6 activity diagram expressed in PlantUML",
        "sd": "SysML v1.6 sequence diagram expressed in PlantUML",
        "other": "Unclassified PlantUML behavior model",
        "missing": "Missing output model",
    }.get(diagram_type, "Unknown")


def parse_llms_emp_stm_features(text: str) -> dict[str, Any]:
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
        token = token.strip()
        token = token.split(":", 1)[0].strip()
        token = token.strip('"')
        if token in {"[*]", "*"}:
            return None
        return aliases.get(token, token) or None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("@"):
            continue
        if line.endswith("{") and line.startswith("state "):
            hierarchical_state_count += 1
        m = state_decl_re.match(line)
        if m:
            label = normalize_text(m.group("label"))
            alias = normalize_text(m.group("alias"))
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
        m = trans_re.match(line)
        if m and "participant" not in line and "actor" not in line:
            src = normalize_state_token(m.group("src"))
            dst = normalize_state_token(m.group("dst"))
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


def parse_llms_emp_sd_features(text: str) -> dict[str, Any]:
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


def parse_llms_emp_act_features(text: str) -> dict[str, Any]:
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
        if re.match(r"^(fork|split)", line, re.I):
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


def parse_llms_emp_features(text: str | None, diagram_type: str) -> dict[str, Any]:
    if not text:
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
    if diagram_type == "stm":
        return parse_llms_emp_stm_features(text)
    if diagram_type == "sd":
        return parse_llms_emp_sd_features(text)
    if diagram_type == "act":
        return parse_llms_emp_act_features(text)
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


def build_llms_emp(raw_root: Path) -> dict[str, pd.DataFrame]:
    path = raw_root / "llms_emp_gmodel" / "Dataset.xlsx"
    df = pd.read_excel(path)
    df = df.rename(
        columns={
            "Unnamed: 4": "selection_flag",
            "Unnamed: 5": "diagram_annotation",
        }
    )
    df.insert(0, "row_id", range(len(df)))
    df["model_name"] = df["Model Name"].map(normalize_text)
    df["model_source"] = df["Model Source"].map(normalize_text)
    df["requirements_description"] = df["Requirements Description"].map(normalize_text)
    df["plantuml_code"] = df["PlantUML"].map(normalize_text)
    df["selection_flag"] = df["selection_flag"].map(normalize_text)
    df["diagram_annotation"] = df["diagram_annotation"].map(normalize_text)
    df["dataset_id"] = "llms_emp"
    df["dataset_name"] = "G_Model SysML behavior model dataset"
    df["dataset_source_url"] = LLMS_EMP_DATASET_URL
    df["input_modality"] = "Natural-language requirements description"
    df["output_representation"] = "PlantUML"
    df["diagram_type"] = df["plantuml_code"].map(classify_llms_emp_plantuml)
    df["output_metamodel"] = df["diagram_type"].map(llms_emp_metamodel)
    df["is_placeholder"] = df["model_name"].fillna("").str.contains(
        "to be continue", case=False, regex=False
    )
    df["has_requirements"] = df["requirements_description"].notna()
    df["has_output_model"] = df["plantuml_code"].notna()
    df["is_complete_sample"] = (
        ~df["is_placeholder"] & df["has_requirements"] & df["has_output_model"]
    )
    df["selected_by_authors"] = (
        df["selection_flag"].fillna("").str.lower().eq("selected")
    )
    df["requirements_char_count"] = df["requirements_description"].map(
        lambda v: len(v) if v else 0
    )
    df["requirements_line_count"] = df["requirements_description"].map(
        lambda v: len(v.splitlines()) if v else 0
    )
    df["plantuml_char_count"] = df["plantuml_code"].map(lambda v: len(v) if v else 0)
    df["plantuml_line_count"] = df["plantuml_code"].map(
        lambda v: len(v.splitlines()) if v else 0
    )

    feature_rows = []
    for _, row in df.iterrows():
        feature_rows.append(parse_llms_emp_features(row["plantuml_code"], row["diagram_type"]))
    feature_df = pd.DataFrame(feature_rows)
    raw_df = pd.concat([df, feature_df], axis=1)
    raw_df = raw_df[
        [
            "dataset_id",
            "dataset_name",
            "dataset_source_url",
            "row_id",
            "model_name",
            "model_source",
            "input_modality",
            "requirements_description",
            "output_representation",
            "output_metamodel",
            "diagram_type",
            "plantuml_code",
            "selection_flag",
            "diagram_annotation",
            "selected_by_authors",
            "is_placeholder",
            "has_requirements",
            "has_output_model",
            "is_complete_sample",
            "requirements_char_count",
            "requirements_line_count",
            "plantuml_char_count",
            "plantuml_line_count",
            "basic_state_count",
            "basic_transition_count",
            "basic_action_annotation_count",
            "basic_hierarchical_state_count",
            "basic_participant_count",
            "basic_message_count",
            "basic_activity_action_count",
            "basic_decision_count",
            "basic_parallel_count",
        ]
    ]
    complete_df = raw_df.loc[raw_df["is_complete_sample"]].reset_index(drop=True)
    return {
        "llms_emp_raw_samples": raw_df.reset_index(drop=True),
        "llms_emp_complete_samples": complete_df,
    }


def panel_component_name(component: ET.Element) -> str | None:
    info = component.find("infoparam")
    if info is None:
        return None
    return normalize_text(info.attrib.get("value"))


def parse_avatar_state_machine_panel(
    case_id: str,
    case_name: str,
    spec_text: str,
    variant_name: str,
    panel: ET.Element,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    panel_name = panel.attrib["name"]
    panel_id = f"{case_id}::{variant_name}::{panel_name}"
    state_rows: list[dict[str, Any]] = []
    transition_rows: list[dict[str, Any]] = []
    point_to_component: dict[str, dict[str, Any]] = {}

    state_component_count = 0
    start_component_count = 0

    for component in panel.findall("COMPONENT"):
        component_type = component.attrib.get("type")
        node_type = {
            "5106": "state",
            "5100": "start_state",
        }.get(component_type, "other")
        component_name = panel_component_name(component)
        if node_type == "state":
            state_component_count += 1
        elif node_type == "start_state":
            start_component_count += 1
            component_name = component_name or "__start__"

        cdparam = component.find("cdparam")
        sizeparam = component.find("sizeparam")
        point_ids = [point.attrib.get("id") for point in component.findall("TGConnectingPoint")]
        record = {
            "dataset_id": "ttool_ai",
            "case_id": case_id,
            "case_name": case_name,
            "variant_name": variant_name,
            "panel_name": panel_name,
            "panel_id": panel_id,
            "node_id": component.attrib.get("id"),
            "node_uid": component.attrib.get("uid"),
            "node_type": node_type,
            "node_name": component_name,
            "component_type_code": component_type,
            "x": int(cdparam.attrib["x"]) if cdparam is not None else None,
            "y": int(cdparam.attrib["y"]) if cdparam is not None else None,
            "width": int(sizeparam.attrib["width"]) if sizeparam is not None else None,
            "height": int(sizeparam.attrib["height"]) if sizeparam is not None else None,
            "connecting_point_ids_json": json_compact(point_ids),
            "raw_component_xml": ET.tostring(component, encoding="unicode"),
        }
        state_rows.append(record)
        for point_id in point_ids:
            point_to_component[point_id] = record

    transition_meta: dict[str, dict[str, Any]] = {}
    for sub in panel.findall("SUBCOMPONENT"):
        father = sub.find("father")
        if father is None:
            continue
        extra = sub.find("extraparam")
        extra_values = {child.tag: normalize_text(child.attrib.get("value")) for child in extra} if extra is not None else {}
        transition_meta[father.attrib["id"]] = {
            "guard": extra_values.get("guard"),
            "after_min": extra_values.get("afterMin"),
            "after_max": extra_values.get("afterMax"),
            "extra_delay_1": extra_values.get("extraDelay1"),
            "extra_delay_2": extra_values.get("extraDelay2"),
            "delay_distribution_law": extra_values.get("delayDistributionLaw"),
            "compute_min": extra_values.get("computeMin"),
            "compute_max": extra_values.get("computeMax"),
            "probability": extra_values.get("probability"),
            "actions": extra_values.get("actions"),
            "raw_subcomponent_xml": ET.tostring(sub, encoding="unicode"),
        }

    nonempty_guard_count = 0
    nonempty_action_count = 0
    for connector in panel.findall("CONNECTOR"):
        connector_id = connector.attrib.get("id")
        p1 = connector.find("P1")
        p2 = connector.find("P2")
        source = point_to_component.get(p1.attrib.get("id") if p1 is not None else "")
        target = point_to_component.get(p2.attrib.get("id") if p2 is not None else "")
        meta = transition_meta.get(connector_id, {})
        guard = normalize_text(meta.get("guard"))
        actions = normalize_text(meta.get("actions"))
        if guard and guard not in {"[ ]", "[]"}:
            nonempty_guard_count += 1
        if actions:
            nonempty_action_count += 1
        transition_rows.append(
            {
                "dataset_id": "ttool_ai",
                "case_id": case_id,
                "case_name": case_name,
                "variant_name": variant_name,
                "panel_name": panel_name,
                "panel_id": panel_id,
                "transition_id": connector_id,
                "transition_uid": connector.attrib.get("uid"),
                "source_node_id": source["node_id"] if source else None,
                "source_node_name": source["node_name"] if source else None,
                "source_node_type": source["node_type"] if source else None,
                "target_node_id": target["node_id"] if target else None,
                "target_node_name": target["node_name"] if target else None,
                "target_node_type": target["node_type"] if target else None,
                "guard_or_trigger": None if guard in {None, "[ ]", "[]"} else guard,
                "actions": actions,
                "after_min": meta.get("after_min"),
                "after_max": meta.get("after_max"),
                "extra_delay_1": meta.get("extra_delay_1"),
                "extra_delay_2": meta.get("extra_delay_2"),
                "delay_distribution_law": meta.get("delay_distribution_law"),
                "compute_min": meta.get("compute_min"),
                "compute_max": meta.get("compute_max"),
                "probability": meta.get("probability"),
                "raw_connector_xml": ET.tostring(connector, encoding="unicode"),
                "raw_transition_meta_xml": meta.get("raw_subcomponent_xml"),
            }
        )

    panel_row = {
        "dataset_id": "ttool_ai",
        "case_id": case_id,
        "case_name": case_name,
        "variant_name": variant_name,
        "model_id": f"{case_id}::{variant_name}",
        "panel_id": panel_id,
        "panel_name": panel_name,
        "panel_type": "AVATARStateMachineDiagramPanel",
        "input_spec_text": spec_text,
        "state_count": state_component_count,
        "start_pseudostate_count": start_component_count,
        "transition_count": len(transition_rows),
        "nonempty_guard_count": nonempty_guard_count,
        "nonempty_action_count": nonempty_action_count,
        "raw_panel_xml": ET.tostring(panel, encoding="unicode"),
    }
    return panel_row, state_rows, transition_rows


def build_ttool_ai(raw_root: Path) -> dict[str, pd.DataFrame]:
    cases = [
        {
            "case_id": "platooning",
            "case_name": "Platooning",
            "spec_path": raw_root / "ttool-ai" / "platooning" / "platoonings.md",
            "xml_path": raw_root / "ttool-ai" / "platooning" / "platoonings.xml",
        },
        {
            "case_id": "automated_braking",
            "case_name": "Automated Braking",
            "spec_path": raw_root / "ttool-ai" / "AutomatedBraking" / "automatedbraking.md",
            "xml_path": raw_root / "ttool-ai" / "AutomatedBraking" / "automatedbraking.xml",
        },
        {
            "case_id": "space_based_system",
            "case_name": "Space-Based System",
            "spec_path": raw_root
            / "ttool-ai"
            / "incoherencies"
            / "specification_spacebasedsystem.md",
            "xml_path": raw_root / "ttool-ai" / "spacebasedsystem" / "spacebasedsystem.xml",
        },
    ]

    model_rows: list[dict[str, Any]] = []
    panel_rows: list[dict[str, Any]] = []
    state_rows: list[dict[str, Any]] = []
    transition_rows: list[dict[str, Any]] = []

    for case in cases:
        spec_text = case["spec_path"].read_text(encoding="utf-8").strip()
        xml_path = case["xml_path"]
        xml_text = xml_path.read_text(encoding="utf-8")
        root = ET.fromstring(xml_text)
        for modeling in root.findall("./Modeling"):
            block_panels = modeling.findall("./AVATARBlockDiagramPanel")
            sm_panels = modeling.findall("./AVATARStateMachineDiagramPanel")
            panel_state_total = 0
            panel_transition_total = 0
            panel_guard_total = 0
            panel_action_total = 0
            for panel in sm_panels:
                panel_row, panel_state_rows, panel_transition_rows = parse_avatar_state_machine_panel(
                    case_id=case["case_id"],
                    case_name=case["case_name"],
                    spec_text=spec_text,
                    variant_name=modeling.attrib["nameTab"],
                    panel=panel,
                )
                panel_rows.append(panel_row)
                state_rows.extend(panel_state_rows)
                transition_rows.extend(panel_transition_rows)
                panel_state_total += panel_row["state_count"]
                panel_transition_total += panel_row["transition_count"]
                panel_guard_total += panel_row["nonempty_guard_count"]
                panel_action_total += panel_row["nonempty_action_count"]

            model_rows.append(
                {
                    "dataset_id": "ttool_ai",
                    "dataset_name": "TTool-AI AVATAR design artifacts",
                    "dataset_source_url": TTOOL_AI_REPO_URL,
                    "case_id": case["case_id"],
                    "case_name": case["case_name"],
                    "model_id": f"{case['case_id']}::{modeling.attrib['nameTab']}",
                    "variant_name": modeling.attrib["nameTab"],
                    "modeling_type": modeling.attrib.get("type"),
                    "output_metamodel": (
                        "TTool AVATAR design model containing block diagrams and AVATAR "
                        "state machine diagrams"
                    ),
                    "input_spec_text": spec_text,
                    "spec_path": str(case["spec_path"]),
                    "xml_path": str(xml_path),
                    "raw_xml": xml_text,
                    "block_panel_names_json": json_compact(
                        [panel.attrib.get("name") for panel in block_panels]
                    ),
                    "state_machine_panel_names_json": json_compact(
                        [panel.attrib.get("name") for panel in sm_panels]
                    ),
                    "block_panel_count": len(block_panels),
                    "state_machine_panel_count": len(sm_panels),
                    "state_count": panel_state_total,
                    "transition_count": panel_transition_total,
                    "nonempty_guard_count": panel_guard_total,
                    "nonempty_action_count": panel_action_total,
                }
            )

    return {
        "ttool_ai_models": pd.DataFrame(model_rows),
        "ttool_ai_state_machine_panels": pd.DataFrame(panel_rows),
        "ttool_ai_states": pd.DataFrame(state_rows),
        "ttool_ai_transitions": pd.DataFrame(transition_rows),
    }


LIGHT_REQUIREMENTS = {
    "U1": "If a person occupies a room, the light has to be sufficient to move safely, if nothing else is desired by a chosen light scene.",
    "U2": "As long as the room is occupied, the actual chosen light scene has to be maintained.",
    "U3": "If the room is reoccupied within T1 minutes after the last person has left the room, the last chosen light scene has to be reestablished.",
    "U4": "If the room is reoccupied after more than T1 minutes since the last person has left the room, the standard light scene has to be established.",
    "U6": "The light scenes can be determined by using the control panel.",
    "U7": "For each room, the actual ambient light level can be set by the user using the control panel.",
    "U8": "For each room, a default light scene can be set (not by using the control panel).",
    "U9": "For each room, a default ambient light level can be set (not by using the control panel).",
    "U10": "The value T1 can be set for each room separately (not by using the control panel).",
    "U11": "If the outdoor light sensor or the motion detector of a room does not work correctly, the user has to be informed.",
    "U12": "The ceiling lights and the task light should be maintained by the control system depending on different light scenes.",
    "FM1": "Use daylight to achieve the desired light whenever possible.",
    "FM3": "If a room is unoccupied for more than T3 minutes, all lights must be switched off.",
    "FM5": "The value T3 can be set for each room separately.",
    "FM6": "The facility manager can turn off any light in a room or hallway section that is not occupied.",
    "FM7": "If a malfunction occurs, the facility manager has to be informed.",
    "FM8": "If a malfunction occurs, the control system supports the facility manager by finding the reason.",
}


LIGHT_VARIABLE_ROWS = [
    ("Light Level", "monitored", "0..10000 lux", "The amount of light in the room"),
    ("Occupied", "monitored", "Boolean", "TRUE if room is occupied"),
    ("Light Level Undetectable", "monitored", "Boolean", "Used for light sensor failure"),
    ("Occupied Undetectable", "monitored", "Boolean", "Used for motion or door sensor failure"),
    ("Window Light Bank Intensity", "monitored", "0..100", "Measured intensity of the window light bank"),
    ("Wall Light Bank Intensity", "monitored", "0..100", "Measured intensity of the wall light bank"),
    ("Chosen1", "operator_input", "Boolean", "Chooses or replaces light scene 1"),
    ("Chosen2", "operator_input", "Boolean", "Chooses or replaces light scene 2"),
    ("Chosen3", "operator_input", "Boolean", "Chooses or replaces light scene 3"),
    ("Default", "operator_input", "Boolean", "Chooses the default light scene"),
    ("Set", "operator_input", "Boolean", "Stores the current settings into a chosen scene"),
    ("T1", "operator_input", "1..1440 minutes", "Timeout to reestablish the default light scene"),
    ("T3", "operator_input", "1..1440 minutes", "Timeout to shut off lights in an empty room"),
    ("FacM Shutoff", "operator_input", "Message / Boolean", "Facility-manager shutoff command"),
    ("ConWindow Light Bank Intensity", "controlled", "0..100", "Commanded intensity of the window light bank"),
    ("ConWall Light Bank Intensity", "controlled", "0..100", "Commanded intensity of the wall light bank"),
    ("Failed", "controlled", "Boolean", "TRUE if the system detects component failure"),
]


LIGHT_STATE_ROWS = [
    ("room_state_hierarchy_req", "Light_Control_System_Room", None, 0),
    ("room_state_hierarchy_req", "Light_Maintenance_Modes", "Light_Control_System_Room", 1),
    ("room_state_hierarchy_req", "Room_Occupied", "Light_Maintenance_Modes", 2),
    ("room_state_hierarchy_req", "Room_Occupied_Eq", "Room_Occupied", 3),
    ("room_state_hierarchy_req", "Maintain_Light_Scene", "Room_Occupied_Eq", 4),
    ("room_state_hierarchy_req", "User_Set_Mode", "Room_Occupied_Eq", 4),
    ("room_state_hierarchy_req", "Room_Empty", "Light_Maintenance_Modes", 2),
    ("room_state_hierarchy_req", "Occupancy_Undetectable", "Light_Maintenance_Modes", 2),
    ("room_state_hierarchy_req", "Chosen_Light_Scene", "Light_Control_System_Room", 1),
    ("room_state_hierarchy_req", "Chosen1_LS", "Chosen_Light_Scene", 2),
    ("room_state_hierarchy_req", "Chosen2_LS", "Chosen_Light_Scene", 2),
    ("room_state_hierarchy_req", "Chosen3_LS", "Chosen_Light_Scene", 2),
    ("room_state_hierarchy_req", "Default_LS", "Chosen_Light_Scene", 2),
    ("room_state_hierarchy_req", "Failure_Modes", "Light_Control_System_Room", 1),
    ("room_state_hierarchy_req", "Ok", "Failure_Modes", 2),
    ("room_state_hierarchy_req", "Failed", "Failure_Modes", 2),
    ("occupied_in_soft_refinement", "Occupied_In", "Light_Control_System_Room", 1),
    ("occupied_in_soft_refinement", "Occupied", "Occupied_In", 2),
    ("occupied_in_soft_refinement", "Not_Occupied", "Occupied_In", 2),
    ("occupied_in_soft_refinement", "Not_Detectable", "Occupied_In", 2),
]


LIGHT_RULE_ROWS = [
    (
        "room_state_hierarchy_req",
        "Light_Maintenance_Modes",
        "Room_Occupied",
        "Occupied_InVar = TRUE && Occupied_Detectable_InVar = TRUE",
        "REQ",
    ),
    (
        "room_state_hierarchy_req",
        "Light_Maintenance_Modes",
        "Occupancy_Undetectable",
        "Occupied_Detectable_InVar = FALSE",
        "REQ",
    ),
    (
        "room_state_hierarchy_req",
        "Light_Maintenance_Modes",
        "Room_Empty",
        "Occupied_InVar = FALSE && Occupied_Detectable_InVar = TRUE",
        "REQ",
    ),
    (
        "chosen1_light_scene_capture_req",
        "Chosen1_LS_Light_Level",
        "Light_Level_InVar",
        "Chosen1_LS_Button_InVar = kPressed && Set_Light_Scene_Button_InVar = kPressed",
        "REQ",
    ),
    (
        "chosen1_light_scene_capture_req",
        "Chosen1_LS_Light_Level",
        "PREV_STEP(Chosen1_LS_Light_Level)",
        "Otherwise preserve the previous chosen-1 scene light level",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Light_Level_InVar",
        "..Room_Occupied_Eq IN_STATE User_Set_Mode",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Chosen1_LS_Light_Level",
        "Chosen1_LS_Button_InVar = kPressed && Set_Light_Scene_Button_InVar = kNotPressed",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Chosen2_LS_Light_Level",
        "Chosen2_LS_Button_InVar = kPressed && Set_Light_Scene_Button_InVar = kNotPressed",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Chosen3_LS_Light_Level",
        "Chosen3_LS_Button_InVar = kPressed && Set_Light_Scene_Button_InVar = kNotPressed",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Default_LS_Light_Level",
        "Default_LS_Button_InVar = kPressed && Set_Light_Scene_Button_InVar = kNotPressed",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "0",
        "..Light_Maintenance_Modes IN_STATE Room_Empty && "
        "(TIME >= TIME_ENTERED(Room_Empty) + T3_InVar || MESSAGE_AT(FacM_Shutoff))",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "Reoccupied_Light_Level()",
        "..Room_Occupied_Eq IN_STATE Maintain_Light_Scene && "
        "PREV_STEP(..Light_Maintenance_Modes IN_STATE Room_Occupied) = FALSE",
        "REQ",
    ),
    (
        "occupancy_and_timeout_req",
        "Current_LS_Light_Level",
        "PREV_STEP(Current_LS_Light_Level)",
        "..Room_Occupied_Eq IN_STATE Maintain_Light_Scene && "
        "PREV_STEP(..Light_Maintenance_Modes IN_STATE Room_Occupied) = TRUE",
        "REQ",
    ),
    (
        "occupied_in_soft_refinement",
        "Occupied_In",
        "Not_Occupied",
        "Motion_Detected_InVar = FALSE",
        "SOFT",
    ),
    (
        "occupied_in_soft_refinement",
        "Occupied_In",
        "Occupied",
        "PREV_STEP(DoorSensor_InVar = kClosed) && "
        "PREV_STEP(..Occupied_In IN_STATE Not_Occupied) = FALSE && "
        "Motion_Detected_InVar = TRUE",
        "SOFT",
    ),
    (
        "occupied_in_soft_refinement",
        "Occupied_In",
        "Not_Detectable",
        "PREV_STEP(DoorSensor_InVar = kClosed) && "
        "PREV_STEP(..Occupied_In IN_STATE Not_Occupied) = TRUE && "
        "Motion_Detected_InVar = TRUE && DoorSensor_InVar = kClosed",
        "SOFT",
    ),
]


def requirement_text(requirement_ids: list[str]) -> str:
    return "\n".join(f"{req_id}: {LIGHT_REQUIREMENTS[req_id]}" for req_id in requirement_ids)


def build_light_control(raw_root: Path) -> dict[str, pd.DataFrame]:
    original_txt = raw_root / "light-control-original-case-study.txt"
    nimbus_txt = raw_root / "light-case-jucs.txt"
    original_text = original_txt.read_text(encoding="utf-8")
    nimbus_text = nimbus_txt.read_text(encoding="utf-8")

    documents_df = pd.DataFrame(
        [
            {
                "dataset_id": "light_control_nimbus",
                "document_id": "dagstuhl_light_control_case_study",
                "title": "Dagstuhl Light Control System case study",
                "document_role": "Original informal requirements",
                "source_url": LIGHT_CASE_ORIGINAL_URL,
                "local_path": str(original_txt),
                "text": original_text,
            },
            {
                "dataset_id": "light_control_nimbus",
                "document_id": "nimbus_light_control_case_study",
                "title": "Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study",
                "document_role": "RSML-e reconstruction and evaluation paper",
                "source_url": LIGHT_CASE_NIMBUS_URL,
                "alternate_source_url": LIGHT_CASE_NIMBUS_HTML_URL,
                "local_path": str(nimbus_txt),
                "text": nimbus_text,
            },
        ]
    )

    variables_df = pd.DataFrame(
        [
            {
                "dataset_id": "light_control_nimbus",
                "case_id": "light_control_room",
                "variable_name": name,
                "variable_group": group,
                "range_or_type": range_or_type,
                "description": description,
                "output_metamodel": "RSML-e monitored / controlled variable dictionary",
            }
            for name, group, range_or_type, description in LIGHT_VARIABLE_ROWS
        ]
    )

    fragments = [
        {
            "fragment_id": "room_state_hierarchy_req",
            "fragment_title": "Room-level RSML-e state hierarchy",
            "abstraction_level": "REQ",
            "sample_kind": "state_hierarchy",
            "input_requirement_ids_json": json_compact(
                ["U1", "U2", "U3", "U4", "U11", "U12", "FM1", "FM3", "FM6", "FM7", "FM8"]
            ),
            "input_requirement_text": requirement_text(
                ["U1", "U2", "U3", "U4", "U11", "U12", "FM1", "FM3", "FM6", "FM7", "FM8"]
            ),
            "output_metamodel": "RSML-e hierarchical and parallel state variables",
            "output_fragment_excerpt": extract_lines(nimbus_txt, 295, 309),
            "source_line_refs_json": json_compact(
                {
                    "nimbus_case_study": [295, 309],
                }
            ),
        },
        {
            "fragment_id": "chosen1_light_scene_capture_req",
            "fragment_title": "Capturing the Chosen1 light-scene level",
            "abstraction_level": "REQ",
            "sample_kind": "state_variable_rule",
            "input_requirement_ids_json": json_compact(["U6", "U7", "U8", "U9", "U10", "U12"]),
            "input_requirement_text": requirement_text(["U6", "U7", "U8", "U9", "U10", "U12"]),
            "output_metamodel": "RSML-e state variable definition",
            "output_fragment_excerpt": extract_lines(nimbus_txt, 423, 437),
            "source_line_refs_json": json_compact(
                {
                    "nimbus_case_study": [423, 437],
                }
            ),
        },
        {
            "fragment_id": "occupancy_and_timeout_req",
            "fragment_title": "Occupancy, timeout, and reoccupation control rules",
            "abstraction_level": "REQ",
            "sample_kind": "state_variable_rule_set",
            "input_requirement_ids_json": json_compact(
                ["U1", "U2", "U3", "U4", "U10", "FM1", "FM3", "FM5", "FM6"]
            ),
            "input_requirement_text": requirement_text(
                ["U1", "U2", "U3", "U4", "U10", "FM1", "FM3", "FM5", "FM6"]
            ),
            "output_metamodel": "RSML-e state variable and output-variable rules",
            "output_fragment_excerpt": extract_lines(nimbus_txt, 464, 570),
            "source_line_refs_json": json_compact(
                {
                    "nimbus_case_study": [464, 570],
                }
            ),
        },
        {
            "fragment_id": "occupied_in_soft_refinement",
            "fragment_title": "Refined Occupied_In software-level state variable",
            "abstraction_level": "SOFT",
            "sample_kind": "refined_state_variable_rule_set",
            "input_requirement_ids_json": json_compact(["U11", "FM7", "FM8"]),
            "input_requirement_text": requirement_text(["U11", "FM7", "FM8"]),
            "output_metamodel": "RSML-e refined software state variable",
            "output_fragment_excerpt": extract_lines(nimbus_txt, 831, 846),
            "source_line_refs_json": json_compact(
                {
                    "nimbus_case_study": [831, 846],
                }
            ),
        },
    ]
    fragments_df = pd.DataFrame(fragments)
    fragments_df.insert(0, "dataset_id", "light_control_nimbus")
    fragments_df.insert(1, "case_id", "light_control_room")

    states_df = pd.DataFrame(
        [
            {
                "dataset_id": "light_control_nimbus",
                "case_id": "light_control_room",
                "fragment_id": fragment_id,
                "state_name": state_name,
                "parent_state_name": parent_state_name,
                "depth": depth,
                "output_metamodel": (
                    "RSML-e state hierarchy" if fragment_id == "room_state_hierarchy_req" else "RSML-e refined state variable"
                ),
            }
            for fragment_id, state_name, parent_state_name, depth in LIGHT_STATE_ROWS
        ]
    )

    rules_df = pd.DataFrame(
        [
            {
                "dataset_id": "light_control_nimbus",
                "case_id": "light_control_room",
                "fragment_id": fragment_id,
                "target_variable": target_variable,
                "assigned_value": assigned_value,
                "condition": condition,
                "abstraction_level": abstraction_level,
                "output_metamodel": "RSML-e assignment / transition rule",
            }
            for fragment_id, target_variable, assigned_value, condition, abstraction_level in LIGHT_RULE_ROWS
        ]
    )

    return {
        "light_control_nimbus_documents": documents_df,
        "light_control_nimbus_fragments": fragments_df,
        "light_control_nimbus_variables": variables_df,
        "light_control_nimbus_states": states_df,
        "light_control_nimbus_rules": rules_df,
    }


STRUCTURE_EVENT_CASE_NAME_MAP = {
    "printer_winter_2017": "Printer",
    "spa_manager_winter_2018": "Spa Manager",
    "dishwasher_winter_2019": "Dishwasher",
    "chess_clock_fall_2019": "Chess Clock",
    "automatic_bread_maker_fall_2020": "Automatic Bread Maker",
    "thermomix_fall_2021": "Thermomix TM6",
    "WUMPLE_fall_2023": "W-UMPLE",
    "SSC7_fall_2024": "SSC7",
    "ATAS_fall_2022": "ATAS",
}


STRUCTURE_EVENT_CASE_ID_BY_METRIC_NAME = {
    "printer": "printer_winter_2017",
    "spa manager": "spa_manager_winter_2018",
    "spa_manager": "spa_manager_winter_2018",
    "dishwasher": "dishwasher_winter_2019",
    "chessclock": "chess_clock_fall_2019",
    "chess clock": "chess_clock_fall_2019",
    "breadmaker": "automatic_bread_maker_fall_2020",
    "automatic bread maker": "automatic_bread_maker_fall_2020",
    "thermomix": "thermomix_fall_2021",
    "thermomix tm6": "thermomix_fall_2021",
    "w umple": "WUMPLE_fall_2023",
    "w-umple": "WUMPLE_fall_2023",
    "wumple": "WUMPLE_fall_2023",
    "ssc7": "SSC7_fall_2024",
    "atas": "ATAS_fall_2022",
}


def parse_state_machine_descriptions(text: str) -> dict[str, str]:
    body = clean_jina_wrapper(text)
    pattern = re.compile(r"(?P<name>[A-Za-z0-9_]+)\s*=\s*\"\"\"(?P<desc>.*?)\"\"\"", re.S)
    return {
        match.group("name"): normalize_text(match.group("desc")) or ""
        for match in pattern.finditer(body)
    }


def parse_n_shot_reference_solutions(text: str) -> dict[str, str]:
    body = clean_jina_wrapper(text)
    start_marker = "n_shot_examples = {"
    end_marker = "\ndef get_n_shot_examples"
    if start_marker in body and end_marker in body:
        body = body.split(start_marker, 1)[1].split(end_marker, 1)[0]
        body = "{\n" + body
    pattern = re.compile(
        r'"(?P<key>[^"]+)":\s*\{\s*"system_description":\s*(?P<descvar>[A-Za-z0-9_]+),\s*"umple_code_solution":\s*\'\'\'(?P<code>.*?)\'\'\'',
        re.S,
    )
    references: dict[str, str] = {}
    for match in pattern.finditer(body):
        key = match.group("key")
        descvar = match.group("descvar")
        code = normalize_text(match.group("code"))
        if "_" not in key:
            continue
        if code:
            references[descvar] = code
    return references


def normalize_metric_case_name(raw_name: Any) -> str | None:
    name = normalize_text(raw_name)
    if not name:
        return None
    name = name.replace("\n", " ").strip()
    name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    return name


def canonical_structure_event_case_id(name: str | None) -> str | None:
    if not name:
        return None
    norm = name.lower().replace("_", " ")
    norm = re.sub(r"\s+", " ", norm).strip()
    return STRUCTURE_EVENT_CASE_ID_BY_METRIC_NAME.get(norm)


def parse_metric_value(value: Any) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if value in {"", "-"}:
            return None
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None
    if float(number).is_integer():
        return int(number)
    return float(number)


def parse_structure_event_metrics(workbook_path: Path) -> pd.DataFrame:
    sheet_specs = {
        "SinglePrompt": ("single_prompt", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "StructureDriven": ("structure_driven", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "EventDriven": ("event_driven", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "Hybrid": ("hybrid", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
    }
    rows: list[dict[str, Any]] = []
    for sheet_name, (strategy_name, blocks) in sheet_specs.items():
        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None)
        for llm_name, col in blocks:
            header_row = None
            for idx in range(len(df)):
                if normalize_text(df.iat[idx, col]) == "System Name":
                    header_row = idx
                    break
            if header_row is None:
                continue
            current_system = None
            current_image_reference = None
            for row_idx in range(header_row + 1, len(df)):
                system_value = df.iat[row_idx, col]
                component_value = df.iat[row_idx, col + 1] if col + 1 < df.shape[1] else None
                if pd.isna(system_value) and pd.isna(component_value):
                    continue
                normalized_system = normalize_metric_case_name(system_value)
                if normalized_system:
                    current_system = normalized_system
                    current_image_reference = normalize_text(df.iat[row_idx, col + 8])
                if current_system is None:
                    continue
                component = normalize_text(component_value)
                if not component:
                    continue
                rows.append(
                    {
                        "dataset_id": "structure_event_driven",
                        "strategy_name": strategy_name,
                        "llm_name": llm_name,
                        "sheet_name": sheet_name,
                        "system_name": current_system,
                        "case_id": canonical_structure_event_case_id(current_system),
                        "component": component,
                        "tp": parse_metric_value(df.iat[row_idx, col + 2]),
                        "fn": parse_metric_value(df.iat[row_idx, col + 3]),
                        "fp": parse_metric_value(df.iat[row_idx, col + 4]),
                        "precision": parse_metric_value(df.iat[row_idx, col + 5]),
                        "recall": parse_metric_value(df.iat[row_idx, col + 6]),
                        "f1_score": parse_metric_value(df.iat[row_idx, col + 7]),
                        "image_reference": current_image_reference,
                    }
                )
    return pd.DataFrame(rows)


def simple_umple_stats(code: str) -> dict[str, Any]:
    transition_count = len(re.findall(r"->", code))
    state_names = set()
    block_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{", re.M)
    for match in block_re.finditer(code):
        name = match.group(1)
        if name not in {"class", "sm", "status"}:
            state_names.add(name)
    return {
        "umple_transition_count": transition_count,
        "umple_block_count": len(state_names),
    }


def build_structure_event_driven(raw_root: Path) -> dict[str, pd.DataFrame]:
    descriptions_text = (raw_root / "state_machine_descriptions.py").read_text(encoding="utf-8")
    nshot_text = (raw_root / "n_shot_examples_single_prompt.py").read_text(encoding="utf-8")
    metrics_path = raw_root / "llm_state_machine_final_f1_scores.xlsx"

    descriptions = parse_state_machine_descriptions(descriptions_text)
    references = parse_n_shot_reference_solutions(nshot_text)
    metrics_df = parse_structure_event_metrics(metrics_path)

    case_rows = []
    for case_id, description in descriptions.items():
        is_paper_case = case_id != "ATAS_fall_2022"
        case_rows.append(
            {
                "dataset_id": "structure_event_driven",
                "dataset_name": (
                    "State-machine generation benchmark from Structure- and "
                    "Event-Driven Frameworks for State Machine Modeling with LLMs"
                ),
                "dataset_source_url": STRUCTURE_EVENT_DRIVEN_ARTIFACT_URL,
                "descriptions_source_url": STRUCTURE_EVENT_DRIVEN_DESCRIPTIONS_URL,
                "nshot_source_url": STRUCTURE_EVENT_DRIVEN_NSHOT_URL,
                "case_id": case_id,
                "case_name": STRUCTURE_EVENT_CASE_NAME_MAP.get(case_id, case_id),
                "is_paper_evaluation_case": is_paper_case,
                "input_modality": "Non-structured natural-language reactive-system description",
                "output_metamodel": "UML state machine (single-prompt reference solutions expressed in Umple)",
                "system_description": description,
                "has_full_reference_solution": case_id in references,
                "reference_solution_representation": (
                    "Umple state machine" if case_id in references else None
                ),
                "reference_solution_missing_reason": (
                    None
                    if case_id in references
                    else "Public artifact snapshot exposes description and metrics, but no full reference solution text was retrievable for this case."
                ),
            }
        )
    cases_df = pd.DataFrame(case_rows)

    reference_rows = []
    for case_id, code in references.items():
        stats = simple_umple_stats(code)
        reference_rows.append(
            {
                "dataset_id": "structure_event_driven",
                "case_id": case_id,
                "case_name": STRUCTURE_EVENT_CASE_NAME_MAP.get(case_id, case_id),
                "is_paper_evaluation_case": case_id != "ATAS_fall_2022",
                "reference_solution_representation": "Umple state machine",
                "reference_solution_text": code,
                "output_metamodel": "UML state machine in Umple syntax",
                **stats,
            }
        )
    references_df = pd.DataFrame(reference_rows)

    return {
        "structure_event_driven_cases": cases_df,
        "structure_event_driven_reference_solutions": references_df,
        "structure_event_driven_metrics": metrics_df,
    }


def serialize_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in result.columns:
        if result[column].dtype == "object":
            result[column] = result[column].map(
                lambda value: json_compact(value)
                if isinstance(value, (dict, list, tuple, set))
                else value
            )
    return result


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialize_object_columns(df).to_parquet(path, index=False)


def build_catalog(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    llms_complete = len(frames["llms_emp_complete_samples"])
    llms_total = len(frames["llms_emp_raw_samples"])
    ttool_models = len(frames["ttool_ai_models"])
    ttool_panels = len(frames["ttool_ai_state_machine_panels"])
    light_fragments = len(frames["light_control_nimbus_fragments"])
    light_documents = len(frames["light_control_nimbus_documents"])
    se_cases = len(frames["structure_event_driven_cases"])
    se_reference_cases = (
        frames["structure_event_driven_reference_solutions"]["case_id"].nunique()
        if not frames["structure_event_driven_reference_solutions"].empty
        else 0
    )
    return pd.DataFrame(
        [
            {
                "dataset_id": "llms_emp",
                "paper_slug": "llms_emp",
                "dataset_name": "G_Model SysML behavior model dataset",
                "output_metamodel": "SysML STM / ACT / SD encoded in PlantUML",
                "sample_granularity": "one row per behavior model",
                "raw_sample_count": llms_total,
                "experiment_ready_sample_count": llms_complete,
                "notes": "Public ledger contains 107 rows; 98 rows have both requirements and PlantUML output.",
            },
            {
                "dataset_id": "ttool_ai",
                "paper_slug": "ttool-ai",
                "dataset_name": "TTool-AI AVATAR design artifacts",
                "output_metamodel": "TTool AVATAR design model with block diagrams and state machines",
                "sample_granularity": "one row per generated system variant",
                "raw_sample_count": ttool_models,
                "experiment_ready_sample_count": ttool_panels,
                "notes": "Fifteen AVATAR designs are exposed as XML; the panel-level parquet focuses on behavior diagrams.",
            },
            {
                "dataset_id": "light_control_nimbus",
                "paper_slug": "requirements-capture-and-evaluation-in-nimbus-light-control",
                "dataset_name": "Light Control System RSML-e reconstruction",
                "output_metamodel": "RSML-e requirements / software state model",
                "sample_granularity": "one row per reconstructed fragment",
                "raw_sample_count": light_documents,
                "experiment_ready_sample_count": light_fragments,
                "notes": "Single-case benchmark reconstructed into fragment-level samples with traceable source excerpts.",
            },
            {
                "dataset_id": "structure_event_driven",
                "paper_slug": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
                "dataset_name": "Reactive-system description benchmark with expert references",
                "output_metamodel": "UML state machine; accessible full references are in Umple",
                "sample_granularity": "one row per benchmark case",
                "raw_sample_count": se_cases,
                "experiment_ready_sample_count": se_reference_cases,
                "notes": "All descriptions and all published metrics were recovered; 5 paper cases plus 1 extra artifact case expose full Umple references in the public snapshot.",
            },
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=RAW_ROOT_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()

    raw_root = args.raw_root
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    frames: dict[str, pd.DataFrame] = {}
    for builder in (
        build_llms_emp,
        build_ttool_ai,
        build_light_control,
        build_structure_event_driven,
    ):
        frames.update(builder(raw_root))

    frames["baseline_double_green_dataset_catalog"] = build_catalog(frames)

    for name, frame in frames.items():
        write_parquet(frame, output_dir / f"{name}.parquet")

    summary = {
        name: {
            "rows": int(len(frame)),
            "columns": list(frame.columns),
        }
        for name, frame in frames.items()
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
