# `cross_paper/` — 跨论文统一汇总 parquet

## 用途

本目录的 4 个 parquet 不属于任何单篇论文，而是**跨 4 个数据集统一字段后的汇总视图**。下游 reviewer / judge benchmark 通常直接从这里取数据。

## 文件清单

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| [`dataset_catalog.parquet`](./dataset_catalog.parquet) | 4 | 8 | 4 个数据集元数据汇总（id / paper_slug / dataset_name / output_metamodel / sample_granularity / 规模 / notes） |
| [`human_review_availability.parquet`](./human_review_availability.parquet) | 4 | 9 | 4 篇人评公开可用性总表（input/ref/pred 是否可用 + 缺口说明） |
| [`human_review_protocols.parquet`](./human_review_protocols.parquet) | 4 | 15 | 4 篇人评方法复原（reviewer pool / 评审维度 / 执行步骤 / 匹配规则 + 论文原文摘录） |
| [`human_review_records.parquet`](./human_review_records.parquet) | 820 | 34 | 跨论文统一字段的人评记录总表（按 paper_slug + record_type + review_record_id 索引） |

## 关键字段（人评统一 schema）

`human_review_records.parquet` 字段含义：

- `paper_slug` —— 来自哪篇论文（与 baselines 目录名一致）
- `record_source` / `record_type` / `review_target` / `component` —— 切片维度
- `input_text` / `ref_output_text` / `pred_output_text` —— 三元组（部分论文 ref 或 pred 可能为空，详见 availability 表）
- `human_review_score` / `human_review_score_unit` / `human_review_summary` —— 评分
- `paper_method_verbatim_excerpt` —— 论文原文评审协议摘录
- `verbatim_extraction_verified` —— 摘录是否人工核验

## 用法示例

```python
import pandas as pd

# 读跨论文人评总表
df = pd.read_parquet("cross_paper/human_review_records.parquet")

# 切 llms_emp 的逐样本人评
llms_emp = df[df["paper_slug"] == "llms_emp"]

# 切 input + ref + pred 三者都齐的（用于训 reviewer）
triplet = df[df[["input_text", "ref_output_text", "pred_output_text"]].notna().all(axis=1)]

# 按论文统计分布
print(df["paper_slug"].value_counts())
```

## 不要在这里做什么

- ❌ 不要把单篇 parquet 复制到这里 —— 单篇 parquet 在 `../<paper>/` 子目录
- ❌ 不要把下游导出脚本的产物落到这里 —— 那应该写入 [`../datasets/`](../datasets/)
- ❌ 不要手工编辑这些 parquet —— 由 [`build_baseline_double_green_human_review_parquets.py`](../../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_human_review_parquets.py) 重生
