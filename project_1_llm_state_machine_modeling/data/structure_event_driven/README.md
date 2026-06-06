# `structure_event_driven/` — Structure- and Event-Driven Frameworks (2026)

## 论文与上游引用

- **论文**：Abdulkarim et al., *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*, **arXiv 2026**. DOI: [10.48550/arXiv.2604.00275](https://arxiv.org/abs/2604.00275)
- **baselines 单篇分析**：[`../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/`](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/)
- **公开工件**：[匿名 4open.science](https://anonymous.4open.science/r/llm_state_machine_modeling/)
- **可获取性**：🟢（匿名工件公开）

## 任务

NL reactive system 描述 → UML 状态机（Umple 文本表示）。**论文已经做过 LLM benchmark**，公开了 `8 个 paper-eval case + 1 课堂练习 + 4 种 strategy × 多 LLM × 7 类组件 × TP/FP/FN/F1` 的完整评测矩阵。

## 文件总览

| 文件 | 行数 × 列数 | 简介 |
|------|------------|------|
| [`simple.parquet`](./simple.parquet) | 512 × 6 | **格式统一表**（与其他 3 个 paper 同 schema） |
| [`cases.parquet`](./cases.parquet) | 9 × 18 | 9 个 case（8 paper-eval + 1 课堂；含 system_description + nshot 来源） |
| [`reference_solutions.parquet`](./reference_solutions.parquet) | 9 × 19 | 9 行 Umple ref + 7 类组件计数 |
| [`metrics.parquet`](./metrics.parquet) | 512 × 14 | 逐组件 TP/FN/FP/precision/recall/f1（按 strategy × LLM × case × component） |
| [`human_review.parquet`](./human_review.parquet) | 512 × 30 | 统一字段人评（含原始 xlsx 评分行 + 论文评审规则摘录） |
| [`raw/`](./raw/) | — | 8 reference Umple txt + xlsx F1 表 + backend prompts + 1 prediction txt |

---

## `simple.parquet`（512 行 × 6 列）

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `id` | str | 全数据集唯一 id（含 strategy:LLM:case:component:idx） | `structure_event_driven::single_prompt:GPT-4o:dishwasher_winter_2019:States:0` |
| `input` | str | NL 系统描述 | `A dishwasher comes with various programs that govern how the dishwasher cleans dishes ...` |
| `expected` | str / None | 期望 Umple 输出（5 paper-eval + 1 课堂 case 含完整文本，3 paper-eval 仅图像 = 空） | `class Dishwasher { status { state0 { ... } } }` |
| `predicted` | str / None | LLM 输出（4open 几乎全空：仅 1 个 SSC7 prediction txt 公开） | _None_（512 中 8 行非空） |
| `model` | str | LLM 名（`GPT-4o` / `Claude 3.5 Sonnet`） | `GPT-4o` |
| `notes` | str | 切片信息：case / strategy / component | `case=Dishwasher; strategy=single_prompt; component=States` |

---

## `cases.parquet`（9 行 × 18 列）

9 个评测 case 元信息（一行一个 case）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `structure_event_driven` |
| `dataset_name` | str | 数据集名 | `State-machine generation benchmark from Structure- and Event-Driven Frameworks for State Machine Modeling with LLMs` |
| `dataset_source_url` | str | 工件主入口 | `https://anonymous.4open.science/r/llm_state_machine_modeling/` |
| `descriptions_source_url` | str | 系统描述来源 URL（backend/resources/state_machine_descriptions） | `https://anonymous.4open.science/api/repo/.../state_machine_descriptions/...` |
| `nshot_source_url` | str | n-shot 示例来源 URL（backend/resources/n_shot_examples） | `https://anonymous.4open.science/api/repo/.../n_shot_examples/...` |
| `case_id` | str | case id（含 cohort：`<name>_<season>_<year>`） | `printer_winter_2017` |
| `case_name` | str | case 名（人类可读） | `Printer` |
| `is_paper_evaluation_case` | bool | 是否进入论文 8 个 paper-eval case（True = 是） | `True` |
| `input_modality` | str | 输入模态分类 | `Non-structured natural-language reactive-system description` |
| `output_metamodel` | str | 输出元模型描述 | `UML state machine (single-prompt reference solutions expressed in Umple)` |
| `system_description` | str | NL 系统描述（输入文本） | `The printer has a master switch which turns the printer on or off. ...` |
| `has_full_reference_solution` | bool | 是否有完整 Umple ref 文本（False = 仅图像 + 计数） | `True` |
| `reference_solution_representation` | str | reference 输出形式（`Umple state machine` / `Umple state machine (image only)` 等） | `Umple state machine` |
| `reference_solution_missing_reason` | str | 若 ref 缺失，给出原因说明 | `Public artifact snapshot exposes description and metrics, but no full reference solution text was retrievable.`（仅当缺失时） |
| `reference_prompt_local_path` | str | reference 文本本地路径（相对当前 parquet） | `./raw/reference_solutions/printer.txt` |
| `reference_image_local_path` | str | reference 图像本地路径（4open 没公开 png，已替代为同 .txt） | `./raw/reference_solutions/printer.txt` |
| `reference_prompt_text` | str | 给 LLM 的完整 prompt 模板 | `Given the problem description below, specify the state machine for the printer with integrated scanner ...` |
| `reference_components_json` | str (JSON dict) | 7 类组件 ground truth 计数 | `{"reference_actions_count": 3, "reference_guards_count": 6, "reference_hierarchical_states_count": 2, ...}` |

---

## `reference_solutions.parquet`（9 行 × 19 列）

完整 Umple reference 文本 + 7 类组件计数（一行一个 case）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `structure_event_driven` |
| `case_id` | str | case id | `printer_winter_2017` |
| `case_name` | str | case 名 | `Printer` |
| `is_paper_evaluation_case` | bool | 是否 paper-eval case | `True` |
| `reference_solution_representation` | str | reference 形式 | `Umple state machine` |
| `reference_solution_text` | str | 完整 Umple ref 文本（5 paper-eval + 1 课堂 case 含；3 paper-eval 缺） | `class Printer{ sm { Off {on -> On;} On{ off -> Off; Idle { ... } } } }` |
| `reference_prompt_text` | str | 给 LLM 的 prompt | `Given the problem description below, specify the state machine for the printer ...` |
| `reference_prompt_local_path` | str | prompt 本地相对路径 | `./raw/reference_solutions/printer.txt` |
| `reference_image_local_path` | str | reference 图像本地相对路径 | `./raw/reference_solutions/printer.txt` |
| `output_metamodel` | str | 输出元模型 | `UML state machine in Umple syntax` |
| `umple_transition_count` | float (nullable) | Umple 文本中 `->` 计数（自动从文本数出来的） | `17.0` |
| `umple_block_count` | float (nullable) | Umple 文本中 `{}` 块数 | `8.0` |
| `reference_states_count` | int | 论文给出的 ref 状态数 | `6` |
| `reference_transitions_count` | int | 论文给出的 ref 迁移数 | `17` |
| `reference_guards_count` | int | 论文给出的 ref guard 数 | `6` |
| `reference_actions_count` | int | 论文给出的 ref action 数 | `3` |
| `reference_hierarchical_states_count` | int | 论文给出的 ref 层次状态数 | `2` |
| `reference_history_states_count` | int | 论文给出的 ref 历史状态数 | `1` |
| `reference_parallel_regions_count` | int | 论文给出的 ref 平行区域数 | `0` |

---

## `metrics.parquet`（512 行 × 14 列）

逐组件评测矩阵（512 = 4 strategy × 16 LLM-runs × 8 case 的展开）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `structure_event_driven` |
| `strategy_name` | str | 4 种 strategy 之一（`single_prompt` / `structure_driven` / `event_driven` / `hybrid`） | `single_prompt` |
| `llm_name` | str | LLM 名 | `GPT-4o` |
| `sheet_name` | str | xlsx 中的 sheet 名 | `SinglePrompt` |
| `system_name` | str | case 名（驼峰，与 case_name 一致） | `Dishwasher` |
| `case_id` | str | case id | `dishwasher_winter_2019` |
| `component` | str | 评测组件类（`States` / `Transitions` / `Guards` / `Actions` / `HierarchicalStates` / `HistoryStates` / `ParallelRegions`） | `States` |
| `tp` | float | True Positive | `6.0` |
| `fn` | float | False Negative | `3.0` |
| `fp` | float | False Positive | `0.0` |
| `precision` | float | precision = tp / (tp + fp) | `1.0` |
| `recall` | float | recall = tp / (tp + fn) | `0.6666666666666666` |
| `f1_score` | float | F1 score | `0.8` |
| `image_reference` | str | 该 (strategy × LLM × case) 对应的 prediction 图像文件名（**4open 没公开 png**，仅作元信息保留） | `Dishwasher_single_prompt_001_3d861c05....png` |

---

## `human_review.parquet`（512 行 × 30 列）

每行对应一个 (strategy × LLM × case × component) 的人评记录。**字段大体与 `cross_paper/human_review_records.parquet` 同 schema**，参见顶层 [`README.md`](../README.md)。

本数据集特有差异：

- 含 `strategy_name` 列（4 种 strategy）
- 含 `component` 列（7 类组件之一）
- `pred_output_text` 几乎全空（4open 未公开 prediction Umple 文本）
- `pred_output_artifact_path` 全空（4open 未公开 prediction png）

---

## `raw/` 原始资源（✅ 已下载，但有缺口）

| 文件 / 目录 | 说明 |
|------|------|
| `reference_solutions/<case>.txt` × 8 | 8 个 case 的 reference Umple 文本 |
| `llm_state_machine_final_f1_scores.xlsx` | 完整 F1 评测矩阵（被 `metrics.parquet` 覆盖） |
| `Final_Single_Prompt/Claude Sonnet 3.5/SSC7_*.txt` | 唯一 1 个公开的 prediction 文本 |
| `backend_prompts/event_driven_smf/` × N | event-driven strategy 的 prompt 模板 |
| `backend_prompts/simple_linear_smf/` × N | structure-driven (simple linear) strategy 的 prompt 模板 |

**已知缺口**：

1. ⚠️ **prediction PNG 图像未公开**：4open.science zip 里没有任何 prediction 图像（`metrics.parquet.image_reference` 字段记录的文件名都对应空文件）
2. ⚠️ **reference PNG 也未公开**：原 `extracted/Reference Solutions/<case>.png` 不存在；`cases.parquet.reference_image_local_path` 与 `reference_solutions.parquet.reference_image_local_path` 已重指向同 `.txt` 文件

## 复用性建议

- ✅ **最适合做组件级 TP/FP/FN/F1 benchmark**：512 行 metrics 已经按 strategy × LLM × case × component 展开
- ✅ **paper benchmark 完整复现可能**：cases + reference_solutions + metrics 三表 join 可以直接重现论文表
- ⚠️ 仅 5 个 paper-eval case 含完整 Umple 文本（其余只有图像 + 计数）；做"完整 ref 文本"实验时记得过滤 `has_full_reference_solution`
- ✅ Umple 元模型显式区分 hierarchical / parallel / history / guards / actions —— 跟时间状态机 + HSM 任务 surface area 高度重合
