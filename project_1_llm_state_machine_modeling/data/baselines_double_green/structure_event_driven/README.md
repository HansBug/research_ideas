# `structure_event_driven/` — Structure- and Event-Driven Frameworks (2026)

## 论文与上游引用

- **论文**：Abdulkarim et al., *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*, **arXiv 2026**. DOI: [10.48550/arXiv.2604.00275](https://arxiv.org/abs/2604.00275)
- **baselines 单篇分析**：[`../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/`](../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/)
- **公开工件**：[匿名 4open.science](https://anonymous.4open.science/r/llm_state_machine_modeling/)
- **可获取性**：🟢（匿名工件公开）

## 任务

NL reactive system 描述 → UML 状态机（Umple 文本表示）。**论文已经做过 LLM benchmark**，公开了 `8 个 paper-eval case + 1 课堂练习 + 4 种 strategy × 多 LLM × 7 类组件 × TP/FP/FN/F1` 的完整评测矩阵。

## 文件清单

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| [`simple.parquet`](./simple.parquet) | 512 | 6 | **格式统一表（6 列：id / input / expected / predicted / model / notes）**；input 全有，expected 320/512（部分 case 仅图像无文本），predicted 8/512（4open 几乎无 prediction 文本） |
| [`cases.parquet`](./cases.parquet) | 9 | 18 | 9 个 case（8 paper-eval + 1 课堂；含 system_description + reference 图 + nshot 来源） |
| [`reference_solutions.parquet`](./reference_solutions.parquet) | 9 | 19 | 完整 Umple ref（5 paper-eval + 1 课堂 case 含完整文本，3 paper-eval 仅图像）+ 7 类组件计数 |
| [`metrics.parquet`](./metrics.parquet) | 512 | 14 | 逐组件 TP/FN/FP/precision/recall/f1（按 strategy × LLM × case × component） |
| [`human_review.parquet`](./human_review.parquet) | 512 | 30 | 统一字段人评（含原始 xlsx 评分行 + 论文评审规则摘录） |
| [`raw/`](./raw/) | — | — | 8 个 reference Umple txt + xlsx F1 表 + backend prompts + 1 个 prediction txt（已从 4open.science 下载） |

## 关键字段

`cases.parquet`：

- `case_id` / `case_name`（Printer / Spa Manager / Dishwasher / ...）
- `is_paper_evaluation_case`（True 表示进入论文 8 个评测 case）
- `system_description`（输入 NL 描述）
- `reference_prompt_text` / `reference_image_local_path`
- `has_full_reference_solution`（是否有 Umple 文本，否则只有图像 + 计数）

`reference_solutions.parquet` 含 7 类组件计数：

- `reference_states_count` / `reference_transitions_count` / `reference_guards_count`
- `reference_actions_count` / `reference_hierarchical_states_count`
- `reference_history_states_count` / `reference_parallel_regions_count`

`metrics.parquet`（512 行 = 4 strategy × 16 LLM × 8 case，按组件粒度展开）：

- `strategy_name`（Single-Prompt / Structure-Driven / Event-Driven / Hybrid）
- `llm_name` / `case_id` / `component`（7 类组件之一）
- `tp` / `fn` / `fp` / `precision` / `recall` / `f1_score`

## 真实样本（一条）

Printer case（6 状态 17 迁移 6 guards 3 actions 2 hierarchical）：

```
INPUT (system_description):
  The printer has a master switch which turns the printer on or off. Once the
  printer is turned on, a user needs to log in before being able to print or
  scan a document. To login, a user taps her/his printer card on the printer's
  card reader. ...

REF (reference_solution_text — Umple):
  class Printer{
   sm {
     Off { on -> On; }
     On {
       off -> Off;
       Idle { login(cardID) [idAuthorized(cardID)] / {action="none";} -> Ready; }
       Ready { ... start [action=="scan" && originalLoaded()] -> ScanAndEmail; ... }
   }}
  [counts: states=6 transitions=17 guards=6 actions=3 hierarchical=2 parallel=0]
```

## 原始资源现状（✅ 已下载，但有缺口）

`raw/` 已从 [匿名工件](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) 下载：

- `reference_solutions/<case>.txt` × 8 个 —— 8 个 case 的 reference Umple 文本
- `llm_state_machine_final_f1_scores.xlsx` —— 完整 F1 评测矩阵
- `Final_Single_Prompt/Claude Sonnet 3.5/SSC7_single_prompt_<hash>.txt` —— 唯一 1 个公开的 prediction 文本
- `backend_prompts/` —— 论文 backend 各 strategy 的 prompt 模板（event_driven_smf / simple_linear_smf）

**已知缺口**：

1. ⚠️ **prediction PNG 图像未公开**：4open.science zip 里没有任何 prediction 图像（论文当时可能只在 supplementary 提供 metrics + reference txt，prediction 文本用了原 png 截图但没上传）。`human_review.parquet` 中 `pred_output_artifact_path` 字段已统一置空（512 / 512 全空）。
2. ⚠️ **reference PNG 也未公开**：原计划 `extracted/Reference Solutions/<case>.png` 不存在；parquet 中相关字段已**改为指向 `.txt` 文件**（数据形态实际是 Umple 文本，更准确）。

parquet 中所有非空路径字段已迁移到本目录的相对路径（`./raw/...`），可逐字段验证存在。

## 复用性建议

- ✅ **最适合做组件级 TP/FP/FN/F1 benchmark**：512 行 metrics 已经按 strategy × LLM × case × component 展开
- ✅ **paper benchmark 完整复现可能**：cases + reference_solutions + metrics 三表 join 可以直接重现论文表
- ⚠️ 仅 5 个 paper-eval case 含完整 Umple 文本（其余只有图像 + 计数）；做"完整 ref 文本"实验时记得过滤 `has_full_reference_solution`
- ✅ Umple 元模型显式区分 hierarchical / parallel / history / guards / actions —— 跟时间状态机 + HSM 任务 surface area 高度重合
