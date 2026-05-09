"""一次性迁移：把 21 parquet 中所有路径字段改成相对于 parquet 文件本身的相对路径。

迁移规则（按字段）：

- ``/tmp/baseline_double_green/raw/<X>``：根据 X 的子结构映射到对应论文的 raw/
- ``/home/.../research_ideas-2/.../baselines/<slug>/...``：改成相对仓库的相对路径
- ``/tmp/baseline_double_green/raw/structure_event/extracted/Reference Solutions/<case>.png``：改成 ``./raw/reference_solutions/<case>.txt``（实际数据形态是 Umple 文本，不是图像）
- 找不到对应文件的字段：改为空字符串 ``""``，并记录到 missing list

输入：仓库内 21 个 parquet
输出：覆盖原文件 + 打印迁移报告
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

REPO = Path("/home/zhangshaoang/oo-projects/research_ideas")
DATA = REPO / "project_1_llm_state_machine_modeling/data/baselines_double_green"
BASELINES = REPO / "project_1_llm_state_machine_modeling/baselines"

# 全局 missing/replaced 计数器
report = {"replaced": 0, "missing": 0, "missing_examples": []}


# ============================================================================
# 路径映射规则
# ============================================================================

def _map_tmp_path(value: str, parquet_file: Path) -> str:
    """把 /tmp/baseline_double_green/raw/<X> 映射到对应 raw/ 相对路径。"""
    s = value
    # 去除 /tmp 前缀
    PFX = "/tmp/baseline_double_green/raw/"
    if not s.startswith(PFX):
        return None
    rel = s[len(PFX):]

    # 分发到具体 paper：根据子目录前缀
    if rel.startswith("llms_emp_gmodel/"):
        target = DATA / "llms_emp" / "raw" / rel[len("llms_emp_gmodel/"):]
    elif rel.startswith("ttool-ai/"):
        target = DATA / "ttool_ai" / "raw" / rel[len("ttool-ai/"):]
    elif rel == "light-control-original-case-study.txt" or \
         rel == "light-case-jucs.txt" or \
         rel == "light-case-jucs.pdf":
        target = DATA / "light_control_nimbus" / "raw" / rel
    elif rel == "papers/Light Control Case Study.pdf" or rel == "papers/Light%20Control%20Case%20Study.pdf":
        target = DATA / "light_control_nimbus" / "raw" / "Light_Control_Case_Study.pdf"
    elif rel == "Thompson_J_M.html":
        # 这个 HTML 没下载（参考列表 helper），保持 missing
        return ""
    elif rel.startswith("structure_event/extracted/Reference Solutions/"):
        # png 引用 → 改为 reference_solutions/<case>.txt
        png_name = rel[len("structure_event/extracted/Reference Solutions/"):]
        txt_name = png_name.rsplit(".", 1)[0] + ".txt"
        target = DATA / "structure_event_driven" / "raw" / "reference_solutions" / txt_name
    elif rel.startswith("structure_event/reference_solutions/"):
        target = DATA / "structure_event_driven" / "raw" / "reference_solutions" / rel[len("structure_event/reference_solutions/"):]
    elif rel == "llm_state_machine_final_f1_scores.xlsx":
        target = DATA / "structure_event_driven" / "raw" / "llm_state_machine_final_f1_scores.xlsx"
    elif rel.startswith("llm_state_machine_modeling/Paper Experiment Resources/Final ") and rel.endswith(".png"):
        # 各种 strategy（Single Prompt / Structure-Driven / Event-Driven / Hybrid）的 prediction 图像 —— 4open 都没公开
        return ""
    elif rel.startswith("llm_state_machine_modeling/Paper Experiment Resources/Final ") and rel.endswith(".txt"):
        # 4open 仅公开 1 个 SSC7 prediction txt，其他都缺
        # 路径形式：'.../Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_<hash>.txt'
        sub = rel[len("llms_state_machine_modeling/Paper Experiment Resources/"):]
        # 直接尝试映射到 Final_Single_Prompt/<...>
        pieces = rel.split("/")
        if len(pieces) >= 5:
            target = DATA / "structure_event_driven" / "raw" / "Final_Single_Prompt" / "/".join(pieces[4:])
            if target.exists():
                return _relative(parquet_file, target)
        return ""
    elif rel == "llm_state_machine_modeling/Paper Experiment Resources/Final Detailed F1-Scores.xlsx":
        target = DATA / "structure_event_driven" / "raw" / "llm_state_machine_final_f1_scores.xlsx"
    else:
        return None  # 未识别，让上层报警

    if not target.exists():
        return ""
    return _relative(parquet_file, target)


def _relative(parquet_file: Path, target: Path) -> str:
    """计算 target 相对于 parquet_file 父目录的相对路径（兼容 Py3.10）。"""
    import os
    rel = os.path.relpath(target.resolve(), start=parquet_file.parent.resolve())
    # 同目录或子目录：加 ./ 前缀以明确"相对当前 parquet 同级"语义
    return "./" + rel if not rel.startswith("..") else rel


def _map_research_ideas2(value: str, parquet_file: Path) -> str:
    """把 /home/.../research_ideas[-2]/.../{baselines,reproduction}/... 映射到本仓库相对路径。"""
    # 优先匹配 reproduction/data/raw/...（structure_event 资源在另一个 worktree 的路径）
    m_repr = re.search(r"/research_ideas(?:-2)?/.*?/reproduction/data/raw/(.+)$", value)
    if m_repr:
        sub = m_repr.group(1)
        if sub.startswith("structure_event/extracted/Reference Solutions/"):
            png_name = sub[len("structure_event/extracted/Reference Solutions/"):]
            txt_name = png_name.rsplit(".", 1)[0] + ".txt"
            target = DATA / "structure_event_driven" / "raw" / "reference_solutions" / txt_name
        elif sub.startswith("structure_event/reference_solutions/"):
            target = DATA / "structure_event_driven" / "raw" / "reference_solutions" / sub[len("structure_event/reference_solutions/"):]
        else:
            return ""
        if not target.exists():
            return ""
        return _relative(parquet_file, target)

    # 再匹配 baselines/<slug>/...
    m = re.search(r"/research_ideas(?:-2)?/.*?/baselines/(.+)$", value)
    if m:
        slug_path = m.group(1)
        candidates = [
            BASELINES / slug_path,
            BASELINES / (slug_path + "/paper_content.txt"),
        ]
        for cand in candidates:
            if cand.exists():
                return _relative(parquet_file, cand)

    return None


def map_value(value, parquet_file: Path):
    """对单个字段值做路径映射。"""
    # 显式处理 numpy ndarray / list（部分字段是 JSON list 序列）
    if isinstance(value, (list, tuple)):
        return [_map_one(item, parquet_file) for item in value]
    try:
        import numpy as np
        if isinstance(value, np.ndarray):
            return np.array([_map_one(item, parquet_file) for item in value])
    except Exception:
        pass
    if value is None:
        return value
    try:
        if pd.isna(value):
            return value
    except (TypeError, ValueError):
        pass
    return _map_one(value, parquet_file)


def _map_one(value, parquet_file: Path):
    """对单个非容器值做路径映射。"""
    if value is None:
        return value
    s = str(value).strip()
    if not s or s.lower() == "none":
        return value
    # JSON-encoded list (如字符串 '["/tmp/...", "/tmp/..."]')
    if s.startswith("[") and s.endswith("]"):
        try:
            import json
            arr = json.loads(s)
            if isinstance(arr, list):
                mapped = [_map_one(x, parquet_file) for x in arr]
                return json.dumps(mapped, ensure_ascii=False)
        except Exception:
            pass

    # /tmp 路径
    if s.startswith("/tmp/baseline_double_green/raw/"):
        new = _map_tmp_path(s, parquet_file)
        if new is None:
            report["missing"] += 1
            if len(report["missing_examples"]) < 8:
                report["missing_examples"].append(("/tmp 未识别", s))
            return ""
        if new == "":
            report["missing"] += 1
        else:
            report["replaced"] += 1
        return new

    # research_ideas-2 绝对路径
    if "research_ideas-2" in s or "research_ideas/" in s:
        new = _map_research_ideas2(s, parquet_file)
        if new is None:
            report["missing"] += 1
            if len(report["missing_examples"]) < 8:
                report["missing_examples"].append(("research_ideas 未识别", s))
            return ""
        if new == "":
            report["missing"] += 1
        else:
            report["replaced"] += 1
        return new

    # 已经是相对路径或其他文本，原样保留
    return value


# ============================================================================
# 字段配置
# ============================================================================

PATH_COLS_BY_PARQUET = {
    "cross_paper/human_review_availability.parquet": ["raw_artifact_path"],
    "cross_paper/human_review_protocols.parquet": ["paper_local_path", "human_review_artifact"],
    "cross_paper/human_review_records.parquet": ["ref_output_artifact_path", "pred_output_artifact_path"],
    "light_control_nimbus/documents.parquet": ["local_path"],
    "llms_emp/human_review.parquet": ["ref_output_artifact_path", "pred_output_artifact_path"],
    "structure_event_driven/cases.parquet": ["reference_prompt_local_path", "reference_image_local_path"],
    "structure_event_driven/human_review.parquet": ["ref_output_artifact_path", "pred_output_artifact_path"],
    "structure_event_driven/reference_solutions.parquet": ["reference_prompt_local_path", "reference_image_local_path"],
    "ttool_ai/human_review.parquet": ["ref_output_artifact_path", "pred_output_artifact_path"],
    "ttool_ai/models.parquet": ["spec_path", "xml_path"],
}


# ============================================================================
# 主逻辑
# ============================================================================

def main():
    print("迁移开始\n" + "=" * 60)
    for rel_pq, cols in PATH_COLS_BY_PARQUET.items():
        pq = DATA / rel_pq
        df = pd.read_parquet(pq)
        before_examples = {}
        for col in cols:
            if col not in df.columns:
                continue
            before_examples[col] = df[col].dropna().astype(str).iloc[0] if df[col].notna().any() else "(empty)"
            df[col] = df[col].apply(lambda v: map_value(v, pq))
        df.to_parquet(pq, index=False)
        print(f"\n▸ {rel_pq}")
        for col, sample in before_examples.items():
            after_sample = df[col].dropna().astype(str)
            after_sample = after_sample[after_sample != ""].iloc[0] if (after_sample != "").any() else "(all empty)"
            print(f"  [{col}]")
            print(f"    旧 → {sample[:100]}")
            print(f"    新 → {after_sample[:100]}")

    print("\n" + "=" * 60)
    print(f"迁移结果：替换 {report['replaced']} 处，置空 {report['missing']} 处")
    if report["missing_examples"]:
        print("\n未识别示例（前 8 个）：")
        for kind, s in report["missing_examples"]:
            print(f"  [{kind}] {s[:100]}")


if __name__ == "__main__":
    main()
