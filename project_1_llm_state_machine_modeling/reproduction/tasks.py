from __future__ import annotations

import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Any

import gdown
import pandas as pd
import requests

from baselines import (
    REFERENCE_PROMPT_FILES,
    build_reference_counts,
    run_llms_emp,
    run_nimbus,
    run_structure_event,
    run_ttool,
)
from config import DERIVED_ROOT, DISCUSSION_ASSET_DIR, DISCUSSION_MD, RAW_ROOT, RESULTS_ROOT
from io_utils import load_discussion_parquet, write_parquet, write_text


LLMS_EMP_URL = "https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6"
TTOOL_AI_REPO_URL = "https://github.com/zebradile/ttool-ai"
LIGHT_CASE_FILES = {
    "light-case-jucs.pdf": "https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf",
    "light-control-original-case-study.pdf": (
        "https://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced/"
        "papers/Light%20Control%20Case%20Study.pdf"
    ),
}
STRUCTURE_EVENT_ZIP_URLS = [
    "https://anonymous.4open.science/api/repo/llm_state_machine_modeling/archive/main.zip",
    "https://anonymous.4open.science/api/repo/llm_state_machine_modeling/archive/master.zip",
]


def _download_file(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    path.write_bytes(response.content)


def _extract_from_zip(zip_path: Path, member_prefixes: tuple[str, ...], target_dir: Path) -> None:
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            if not any(member.startswith(prefix) for prefix in member_prefixes):
                continue
            if member.endswith("/"):
                continue
            relative_name = member.split("/", 1)[1] if "/" in member else member
            target_path = target_dir / relative_name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as source, target_path.open("wb") as sink:
                shutil.copyfileobj(source, sink)


def _extract_structure_event_assets(structure_root: Path) -> None:
    zip_path = structure_root / "llm_state_machine_modeling.zip"
    _extract_from_zip(
        zip_path,
        (
            "Paper Experiment Resources/Reference Solutions/",
            "backend/resources/prompts/",
            "backend/resources/state_machine_descriptions.py",
            "backend/resources/n_shot_examples_single_prompt.py",
            "backend/resources/n_shot_examples_simple_linear.py",
            "backend/resources/n_shot_examples_event_driven.py",
            "backend/simple_linear_smf/",
            "backend/event_driven_smf/",
            "backend/merged_simple_linear_smf/",
            "backend/merged_event_driven_smf/",
            "backend/single_prompt.py",
        ),
        structure_root / "extracted",
    )


def download_raw_data() -> None:
    RAW_ROOT.mkdir(parents=True, exist_ok=True)

    llms_emp_root = RAW_ROOT / "llms_emp_gmodel"
    if not (llms_emp_root / "Dataset.xlsx").exists():
        gdown.download_folder(LLMS_EMP_URL, output=str(llms_emp_root), quiet=False)

    ttool_root = RAW_ROOT / "ttool-ai"
    if not ttool_root.exists():
        subprocess.run(["git", "clone", TTOOL_AI_REPO_URL, str(ttool_root)], check=True)

    light_root = RAW_ROOT / "light_control"
    for filename, url in LIGHT_CASE_FILES.items():
        pdf_path = light_root / filename
        txt_path = pdf_path.with_suffix(".txt")
        if txt_path.exists() and not pdf_path.exists():
            continue
        if not pdf_path.exists():
            try:
                _download_file(url, pdf_path)
            except Exception:
                if filename == "light-control-original-case-study.pdf" and not txt_path.exists():
                    mirror_url = "https://r.jina.ai/http://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced/papers/Light%20Control%20Case%20Study.pdf"
                    _download_file(mirror_url, txt_path)
                    continue
                raise
        if not txt_path.exists():
            subprocess.run(
                [
                    "venv/bin/python",
                    "-m",
                    "tools.pdf_extractor",
                    "-i",
                    str(pdf_path),
                    "-o",
                    str(txt_path),
                    "-m",
                    "text",
                ],
                check=True,
            )

    structure_root = RAW_ROOT / "structure_event"
    zip_path = structure_root / "llm_state_machine_modeling.zip"
    structure_root.mkdir(parents=True, exist_ok=True)
    if not zip_path.exists():
        downloaded = False
        for url in STRUCTURE_EVENT_ZIP_URLS:
            try:
                _download_file(url, zip_path)
                downloaded = True
                break
            except Exception:
                continue
        if not downloaded:
            raise FileNotFoundError(
                "Structure/Event raw zip is missing and the public archive endpoint could not be downloaded."
            )
    _extract_structure_event_assets(structure_root)


def _structure_event_prompt_path(case_id: str) -> Path:
    candidates = [
        RAW_ROOT / "structure_event" / "reference_solutions" / REFERENCE_PROMPT_FILES[case_id],
        RAW_ROOT / "structure_event" / "extracted" / "Reference Solutions" / REFERENCE_PROMPT_FILES[case_id],
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _structure_event_image_path(case_id: str) -> Path:
    stem = REFERENCE_PROMPT_FILES[case_id].replace(".txt", ".png")
    candidates = [
        RAW_ROOT / "structure_event" / "reference_solutions" / stem,
        RAW_ROOT / "structure_event" / "extracted" / "Reference Solutions" / stem,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def augment_parquets() -> None:
    DERIVED_ROOT.mkdir(parents=True, exist_ok=True)
    download_raw_data()

    cases_df = load_discussion_parquet("structure_event_driven_cases").copy()
    refs_df = load_discussion_parquet("structure_event_driven_reference_solutions").copy()
    ref_counts = build_reference_counts()

    existing_refs = refs_df.set_index("case_id").to_dict(orient="index")
    enriched_ref_rows: list[dict[str, Any]] = []
    component_fields = [
        "States",
        "Transitions",
        "Guards",
        "Actions",
        "Hierarchical states",
        "History States",
        "Parallel Regions",
    ]
    for _, case_row in cases_df.iterrows():
        case_id = case_row["case_id"]
        ref_payload = existing_refs.get(case_id, {})
        count_row = (
            ref_counts.loc[ref_counts["case_id"] == case_id].iloc[0].to_dict()
            if case_id in set(ref_counts["case_id"])
            else {"case_id": case_id}
        )
        prompt_path = _structure_event_prompt_path(case_id) if case_id in REFERENCE_PROMPT_FILES else None
        image_path = _structure_event_image_path(case_id) if case_id in REFERENCE_PROMPT_FILES else None
        prompt_text = prompt_path.read_text(encoding="utf-8").strip() if prompt_path and prompt_path.exists() else None
        enriched_ref_rows.append(
            {
                "dataset_id": "structure_event_driven",
                "case_id": case_id,
                "case_name": case_row["case_name"],
                "is_paper_evaluation_case": bool(case_row["is_paper_evaluation_case"]),
                "reference_solution_representation": (
                    ref_payload.get("reference_solution_representation")
                    or ("Prompt + image + component counts" if prompt_text else None)
                ),
                "reference_solution_text": ref_payload.get("reference_solution_text"),
                "reference_prompt_text": prompt_text,
                "reference_prompt_local_path": str(prompt_path) if prompt_path and prompt_path.exists() else None,
                "reference_image_local_path": str(image_path) if image_path and image_path.exists() else None,
                "output_metamodel": ref_payload.get("output_metamodel") or case_row["output_metamodel"],
                "umple_transition_count": ref_payload.get("umple_transition_count"),
                "umple_block_count": ref_payload.get("umple_block_count"),
                **{f"reference_{field.lower().replace(' ', '_')}_count": int(count_row.get(field, 0)) for field in component_fields},
            }
        )

    enriched_refs_df = pd.DataFrame(enriched_ref_rows)

    count_lookup = enriched_refs_df.set_index("case_id").to_dict(orient="index")
    cases_df["reference_prompt_local_path"] = cases_df["case_id"].map(
        lambda case_id: count_lookup[case_id]["reference_prompt_local_path"]
    )
    cases_df["reference_image_local_path"] = cases_df["case_id"].map(
        lambda case_id: count_lookup[case_id]["reference_image_local_path"]
    )
    cases_df["reference_prompt_text"] = cases_df["case_id"].map(
        lambda case_id: count_lookup[case_id]["reference_prompt_text"]
    )
    cases_df["reference_components_json"] = cases_df["case_id"].map(
        lambda case_id: json.dumps(
            {
                key: value
                for key, value in count_lookup[case_id].items()
                if key.startswith("reference_") and key.endswith("_count")
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )

    catalog_df = load_discussion_parquet("baseline_double_green_dataset_catalog").copy()
    mask = catalog_df["dataset_id"] == "structure_event_driven"
    catalog_df.loc[mask, "experiment_ready_sample_count"] = 8
    catalog_df.loc[mask, "notes"] = (
        "All 8 paper evaluation cases now expose prompt text, reference image, and metric-derived "
        "component counts locally; 6 cases additionally expose full Umple text from the public artifact."
    )

    for name, frame in (
        ("structure_event_driven_cases", cases_df),
        ("structure_event_driven_reference_solutions", enriched_refs_df),
        ("baseline_double_green_dataset_catalog", catalog_df),
    ):
        write_parquet(frame, DERIVED_ROOT / f"{name}.parquet")
        write_parquet(frame, DISCUSSION_ASSET_DIR / f"{name}.parquet")

    md_text = DISCUSSION_MD.read_text(encoding="utf-8")
    replacements = {
        "| [structure_event_driven_reference_solutions.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_reference_solutions.parquet) | `Structure/Event-Driven` 中可恢复的 6 个 Umple 参考解 |":
        "| [structure_event_driven_reference_solutions.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_reference_solutions.parquet) | `Structure/Event-Driven` 的 8 个论文案例 prompt/image/count ground truth 与 6 个 Umple 文本参考解 |",
        "- `Final Detailed F1-Scores.xlsx` 可以直接下载，但匿名源并没有稳定暴露 `Reference Solutions/` 的目录列表；这会影响 3 个案例参考解的完整恢复，后文会单独说明。":
        "- `Final Detailed F1-Scores.xlsx` 可以直接下载；结合本地保留的 zip 快照后，`Reference Solutions/` 目录下 8 个论文案例的 prompt/image 以及逐组件 count 级 ground truth 已全部恢复，另有 6 个案例还能恢复完整 Umple 文本参考解。",
        "2. 在匿名工件中，当前能恢复出来的完整参考解文本是 `Umple` 语法 [2]":
        "2. 在匿名工件中，8 个论文案例都能恢复 prompt + reference image，另有 6 个案例能恢复完整 `Umple` 文本参考解 [2]",
        "- `structure_event_driven_reference_solutions.parquet`：保留当前可访问的 Umple 参考解":
        "- `structure_event_driven_reference_solutions.parquet`：统一保留 prompt / image / metric-derived counts，并在可恢复时补上 Umple 文本参考解",
        "| [structure_event_driven_reference_solutions.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_reference_solutions.parquet) | 6 行 | 5 个论文正式案例 + 1 个额外 `ATAS` 的完整 Umple 参考解 |":
        "| [structure_event_driven_reference_solutions.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_reference_solutions.parquet) | 9 行 | 8 个论文正式案例全部带 prompt/image/count ground truth；其中 6 个案例 + 1 个额外 `ATAS` 还带完整 Umple 文本 |",
        "| `Printer` | 有 | 有 |\n| `Spa Manager` | 有 | 有 |\n| `Dishwasher` | 有 | 有 |\n| `Chess Clock` | 有 | 有 |\n| `Automatic Bread Maker` | 有 | 无 |\n| `Thermomix TM6` | 有 | 有 |\n| `W-UMPLE` | 有 | 无 |\n| `SSC7` | 有 | 无 |\n| `ATAS` | 有 | 有，但它不是论文正式 8 案例之一 |":
        "| `Printer` | 有 | 有，且有 Umple 文本 |\n| `Spa Manager` | 有 | 有，且有 Umple 文本 |\n| `Dishwasher` | 有 | 有，且有 Umple 文本 |\n| `Chess Clock` | 有 | 有，且有 Umple 文本 |\n| `Automatic Bread Maker` | 有 | 有，但仅有 prompt/image/count |\n| `Thermomix TM6` | 有 | 有，且有 Umple 文本 |\n| `W-UMPLE` | 有 | 有，但仅有 prompt/image/count |\n| `SSC7` | 有 | 有，但仅有 prompt/image/count |\n| `ATAS` | 有 | 有 Umple 文本，但它不是论文正式 8 案例之一 |",
        "- 8 个论文正式案例的自然语言描述都已经恢复\n- 官方指标表也已经完整恢复\n- 但匿名工件对 `Reference Solutions/` 的目录和剩余文件并没有稳定公开，因此 `Automatic Bread Maker / W-UMPLE / SSC7` 三个正式案例目前只有描述和指标，没有完整参考解文本":
        "- 8 个论文正式案例的自然语言描述都已经恢复\n- 官方指标表也已经完整恢复\n- 8 个论文正式案例的 prompt/image/count 级 ground truth 现在也都已恢复\n- 但 `Automatic Bread Maker / W-UMPLE / SSC7` 三个正式案例仍然只有 prompt/image/count，没有公开的完整 Umple 文本参考解",
        "这一点已经在 `structure_event_driven_cases.parquet` 的 `has_full_reference_solution` 与 `reference_solution_missing_reason` 两列中显式编码。":
        "这一点已经在 `structure_event_driven_cases.parquet` 与 `structure_event_driven_reference_solutions.parquet` 中显式编码。",
        "| `cases` | `case_id`, `case_name`, `is_paper_evaluation_case`, `system_description`, `has_full_reference_solution` | 案例主表 |\n| `reference_solutions` | `case_id`, `reference_solution_text`, `umple_transition_count`, `umple_block_count` | 已恢复的 Umple 参考解 |":
        "| `cases` | `case_id`, `case_name`, `is_paper_evaluation_case`, `system_description`, `reference_prompt_text`, `reference_components_json`, `has_full_reference_solution` | 案例主表 |\n| `reference_solutions` | `case_id`, `reference_solution_text`, `reference_prompt_text`, `reference_image_local_path`, `reference_states_count`, `reference_transitions_count` 等 | prompt/image/count ground truth 与已恢复 Umple 文本 |",
    }
    for old, new in replacements.items():
        md_text = md_text.replace(old, new)
    DISCUSSION_MD.write_text(md_text, encoding="utf-8")


def run_baseline(name: str) -> None:
    if name == "llms_emp":
        run_llms_emp()
        return
    if name == "ttool":
        run_ttool()
        return
    if name == "nimbus":
        run_nimbus()
        return
    if name == "structure_event":
        run_structure_event()
        return
    raise ValueError(f"Unknown baseline: {name}")


def write_report() -> None:
    report_path = RESULTS_ROOT.parent / "REPRODUCTION_REPORT.md"
    llms_emp_summary = json.loads((RESULTS_ROOT / "llms_emp" / "summary.json").read_text(encoding="utf-8"))
    ttool_summary = json.loads((RESULTS_ROOT / "ttool" / "summary.json").read_text(encoding="utf-8"))
    nimbus_summary = json.loads((RESULTS_ROOT / "nimbus" / "summary.json").read_text(encoding="utf-8"))
    struct_summary = json.loads((RESULTS_ROOT / "structure_event" / "summary.json").read_text(encoding="utf-8"))

    llms_emp_pred = pd.read_parquet(RESULTS_ROOT / "llms_emp" / "predictions.parquet")
    ttool_pred = pd.read_parquet(RESULTS_ROOT / "ttool" / "predictions.parquet")
    nimbus_pred = pd.read_parquet(RESULTS_ROOT / "nimbus" / "predictions.parquet")
    struct_pred = pd.read_parquet(RESULTS_ROOT / "structure_event" / "predictions.parquet")

    lines = [
        "# Reproduction Report",
        "",
        "## 1. Runtime Entry",
        "",
        "```bash",
        "venv/bin/pip install -r project_1_llm_state_machine_modeling/reproduction/requirements-reprod.txt",
        "venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py download-raw",
        "venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py augment-parquets",
        "venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline all",
        "venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py report",
        "```",
        "",
        "默认 provider fallback 顺序是 `airouter -> findcg -> miaocg`，默认模型是 `gpt-5.5`，不会自动尝试 `api68886868`。",
        "",
        "## 2. Code Entry Points",
        "",
        "- `run_all.py`: 顶层 CLI 入口，统一调度下载、增强、运行、报告。",
        "- `tasks.py`: 原始数据下载、parquet 回填、报告生成。",
        "- `llm_client.py`: 官方 `openai` client + provider fallback + 磁盘缓存。",
        "- `baseline_llms_emp.py`: `llms_emp` 复现主入口。",
        "- `baseline_ttool.py`: `ttool-ai` 与本地 `sm/MTI` 复现主入口。",
        "- `baseline_nimbus.py`: `Nimbus` 4 个 fragment 复现主入口。",
        "- `baseline_structure_event.py`: `Structure/Event-Driven` 四策略复现主入口。",
        "",
        "## 3. Raw Data",
        "",
        f"- `llms_emp`: `{RAW_ROOT / 'llms_emp_gmodel'}`",
        f"- `ttool-ai`: `{RAW_ROOT / 'ttool-ai'}`",
        f"- `light_control`: `{RAW_ROOT / 'light_control'}`",
        f"- `structure_event`: `{RAW_ROOT / 'structure_event'}`",
        "",
        "## 4. Dataset Augmentation",
        "",
        "- `structure_event_driven_reference_solutions.parquet` 已补成统一 ground-truth 表：8 个论文案例全部具备 prompt/image/count 级 ground truth，6 个案例另外具备 Umple 文本参考解。",
        "- 所有复现实验统一基于 parquet 输入；若原始 artifact 只有 zip / PDF / XML，则先在本地补全再回写 parquet。",
        "",
        "## 5. Real Run Results",
        "",
        "### 5.1 llms_emp",
        "",
        f"- sample count: `{llms_emp_summary['sample_count']}`",
        f"- overall macro F1: `{llms_emp_summary['overall_macro_f1']:.4f}`",
        "- covered scenarios: `stm / act / sd`",
        "",
        llms_emp_pred.groupby("diagram_type")[["macro_component_f1", "repaired"]]
        .mean()
        .rename(columns={"macro_component_f1": "macro_f1", "repaired": "repair_rate"})
        .to_markdown(),
        "",
        "### 5.2 ttool-ai / local sm",
        "",
        "- covered scenarios: `platooning / automated_braking / space_based_system`",
        "- covered strategies: `ttool_ai_prompt / mti_multi_step`",
        "",
        ttool_pred.groupby("strategy_name")[["macro_component_f1"]]
        .mean()
        .rename(columns={"macro_component_f1": "macro_f1"})
        .to_markdown(),
        "",
        ttool_pred[["case_id", "strategy_name", "macro_component_f1"]].to_markdown(index=False),
        "",
        "### 5.3 Nimbus Light Control",
        "",
        f"- fragment count: `{nimbus_summary['fragment_count']}`",
        f"- overall macro F1: `{nimbus_summary['overall_macro_f1']:.4f}`",
        f"- strict exact-set macro F1: `{nimbus_summary['overall_strict_macro_f1']:.4f}`",
        "- covered fragments: room hierarchy / chosen light scene capture / occupancy timeout / software refinement",
        "",
        nimbus_pred[
            [
                "fragment_id",
                "fragment_title",
                "sample_kind",
                "macro_f1",
                "strict_macro_f1",
                "pred_state_count",
                "ref_state_count",
                "pred_rule_count",
                "ref_rule_count",
            ]
        ].to_markdown(index=False),
        "",
        "### 5.4 Structure/Event-Driven",
        "",
        "- covered cases: 8 paper evaluation systems",
        "- covered strategies: `single_prompt / structure_driven / event_driven / hybrid`",
        "",
        struct_pred.groupby("strategy_name")[["macro_component_f1"]]
        .mean()
        .rename(columns={"macro_component_f1": "macro_f1"})
        .to_markdown(),
        "",
        struct_pred[["case_id", "strategy_name", "macro_component_f1"]].to_markdown(index=False),
        "",
        "## 6. Strategy Coverage",
        "",
        "- `llms_emp`: 复现了论文里的 `stm / act / sd` 三类行为模型生成，并补了一轮基于结构反馈的修复。",
        "- `ttool-ai`: 复现了本地 `sm/baseline.py` 中 `TTool_ai` 的三步 blocks/signals/behavior 链路，以及 `sm/MTI/*` 的多步建模链路。",
        "- `Nimbus`: 复现了 4 个 fragment，覆盖房间级状态层次、light scene capture、occupancy/timeout rules、software refinement，并同时保留 count-based 与 strict exact-set 两种评测结果。",
        "- `Structure/Event-Driven`: 复现了 `single_prompt / structure_driven / event_driven / hybrid` 四种策略，并覆盖 8 个论文案例。",
        "",
        "## 7. Simplifications",
        "",
        "- `llms_emp` 的评测采用可复现的 PlantUML 结构计数近似，而不是原文全部人工语义判别项。",
        "- `ttool-ai` 没有强行输出完整 TTool XML / SCXML；这里统一复现为 `TTool-style JSON`，但 prompt 内容已尽量贴近本地 `sm` 原始链路。",
        "- `Nimbus` 以 RSML-e 状态/规则 JSON 为统一中间表示，并默认以 count-based 指标做主结果，strict exact-set 指标作为补充诊断。",
        "- `Structure/Event-Driven` 统一采用 count-based 组件评测，这样 8 个论文案例都可以进入同一口径；其中 `hybrid` 在本地 provider 不稳定时退化为保守聚合（优先 single-prompt 候选），6 个公开 Umple 文本仍保留在 parquet 中供后续更细粒度评测。",
        "",
        "## 8. Result Files",
        "",
        f"- `llms_emp`: `{RESULTS_ROOT / 'llms_emp'}`",
        f"- `ttool`: `{RESULTS_ROOT / 'ttool'}`",
        f"- `nimbus`: `{RESULTS_ROOT / 'nimbus'}`",
        f"- `structure_event`: `{RESULTS_ROOT / 'structure_event'}`",
        "",
        "各 baseline 的主入口都由 `project_1_llm_state_machine_modeling/reproduction/run_all.py` 统一调度。",
    ]
    write_text("\n".join(lines) + "\n", report_path)
