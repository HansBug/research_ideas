"""为 4 个论文子目录各生成一个格式统一的 simple.parquet。

字段固定 6 列（无论该论文实际数据形态如何）：

- ``id``：全数据集唯一 id
- ``input``：自然语言输入（必有）
- ``expected``：期望 STM 输出（论文中的 gold reference，nullable）
- ``predicted``：论文方法 LLM 实际输出（nullable）
- ``model``：predicted 对应的 LLM 名（nullable）
- ``notes``：备注，含 record_type / case_name / strategy 等切片信息

行数粒度（按论文最自然的"一行一个评估单元"）：

- llms_emp: 192（人评行）
- ttool_ai: 15（model variant）
- light_control_nimbus: 4（fragments）
- structure_event_driven: 512（人评行）
"""

from pathlib import Path

import pandas as pd

DATA = Path("project_1_llm_state_machine_modeling/data/baselines_double_green")

SCHEMA = ["id", "input", "expected", "predicted", "model", "notes"]


def _norm(value):
    """空字符串 / NaN 统一返回 None；其他原样转 str。"""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    s = str(value).strip()
    return s if s else None


# ============================================================================
# llms_emp
# ============================================================================

def build_llms_emp():
    df = pd.read_parquet(DATA / "llms_emp" / "human_review.parquet")
    out = []
    for _, r in df.iterrows():
        out.append({
            "id": f"llms_emp::{r['review_record_id']}",
            "input": _norm(r["input_text"]),
            "expected": _norm(r["ref_output_text"]),
            "predicted": _norm(r["pred_output_text"]),
            "model": _norm(r["llm_name"]),
            "notes": f"diagram_type={r.get('diagram_type', '')}; sheet={r.get('sheet_name', '')}; record_type={r.get('record_type', '')}",
        })
    return pd.DataFrame(out)[SCHEMA]


# ============================================================================
# ttool_ai
# ============================================================================

def build_ttool_ai():
    df = pd.read_parquet(DATA / "ttool_ai" / "models.parquet")
    out = []
    for _, r in df.iterrows():
        out.append({
            "id": f"ttool_ai::{r['case_name']}::{r['variant_name']}",
            "input": _norm(r["input_spec_text"]),
            "expected": None,  # 论文未公开 reference output
            "predicted": _norm(r["raw_xml"]),
            "model": "TTool-AI workflow (GPT-4)",  # 论文使用 GPT-4 作为后端
            "notes": f"case={r['case_name']}; variant={r['variant_name']}; modeling_type={r.get('modeling_type', '')}; states={int(r.get('state_count') or 0)}; transitions={int(r.get('transition_count') or 0)}",
        })
    return pd.DataFrame(out)[SCHEMA]


# ============================================================================
# light_control_nimbus
# ============================================================================

def build_light_control_nimbus():
    df = pd.read_parquet(DATA / "light_control_nimbus" / "fragments.parquet")
    out = []
    for _, r in df.iterrows():
        out.append({
            "id": f"light_control_nimbus::{r['case_id']}::{r['fragment_id']}",
            "input": _norm(r["input_requirement_text"]),
            "expected": _norm(r["output_fragment_excerpt"]),
            "predicted": None,  # 论文非 LLM 工作，无 prediction
            "model": None,
            "notes": f"case={r['case_id']}; fragment={r['fragment_id']}; abstraction={r.get('abstraction_level', '')}; sample_kind={r.get('sample_kind', '')}",
        })
    return pd.DataFrame(out)[SCHEMA]


# ============================================================================
# structure_event_driven
# ============================================================================

def build_structure_event_driven():
    df = pd.read_parquet(DATA / "structure_event_driven" / "human_review.parquet")
    out = []
    for _, r in df.iterrows():
        out.append({
            "id": f"structure_event_driven::{r['review_record_id']}",
            "input": _norm(r["input_text"]),
            "expected": _norm(r["ref_output_text"]),
            "predicted": _norm(r["pred_output_text"]),
            "model": _norm(r.get("llm_name")),
            "notes": f"case={r.get('case_name', '')}; strategy={r.get('strategy_name', '')}; component={r.get('component', '')}",
        })
    return pd.DataFrame(out)[SCHEMA]


# ============================================================================
# 主逻辑
# ============================================================================

BUILDERS = {
    "llms_emp": build_llms_emp,
    "ttool_ai": build_ttool_ai,
    "light_control_nimbus": build_light_control_nimbus,
    "structure_event_driven": build_structure_event_driven,
}


def main():
    for paper, fn in BUILDERS.items():
        df = fn()
        out_path = DATA / paper / "simple.parquet"
        df.to_parquet(out_path, index=False)
        coverage = {
            "rows": len(df),
            "input_present": df["input"].notna().sum(),
            "expected_present": df["expected"].notna().sum(),
            "predicted_present": df["predicted"].notna().sum(),
            "model_present": df["model"].notna().sum(),
        }
        print(f"▸ {paper}/simple.parquet: {coverage}")


if __name__ == "__main__":
    main()
