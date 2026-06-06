# `llms_emp/` — Generating SysML Behavior Models via LLMs (2025)

## 论文与上游引用

- **论文**：Wang et al., *Generating SysML Behavior Models via Large Language Models: an Empirical Study*, **Internetware 2025**, pp. 366-377. DOI: [10.1145/3755881.3755926](https://dl.acm.org/doi/10.1145/3755881.3755926)
- **baselines 单篇分析**：[`../../baselines/llms_emp/`](../../baselines/llms_emp/)
- **数据集公开入口**：[Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)
- **可获取性**：🟢（直接公开）

## 任务

NL 需求 → PlantUML SysML 行为模型（STM / ACT / SD 三类）。

## 文件总览

| 文件 | 行数 × 列数 | 简介 |
|------|------------|------|
| [`simple.parquet`](./simple.parquet) | 192 × 6 | **格式统一表**（与其他 3 个 paper 同 schema） |
| [`raw_samples.parquet`](./raw_samples.parquet) | 107 × 32 | 公开账本原始 107 行（含未筛选样本） |
| [`complete_samples.parquet`](./complete_samples.parquet) | 98 × 32 | 完整实验样本（同时含 input + output：38 STM / 21 ACT / 39 SD） |
| [`human_review.parquet`](./human_review.parquet) | 192 × 31 | 公开逐样本人评（input + ref + pred + 评分 + 论文摘录） |
| [`raw/`](./raw/) | — | 原始 xlsx + Google Drive README |

---

## `simple.parquet`（192 行 × 6 列）

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `id` | str | 全数据集唯一 id，格式 `llms_emp::<sheet_name>:<idx>` | `llms_emp::STM Results:0` |
| `input` | str | 自然语言需求（输入） | `1 The human driving mode is represented by a simple state. 2 The autonomous mode ...` |
| `expected` | str | 期望 PlantUML 输出（论文 gold reference） | `@startuml [*] --> human_mode : power_on  autonomous_mode --> ...` |
| `predicted` | str | LLM 实际输出 | `@startuml [*] --> HumanDriving  state HumanDriving { [*] --> ... }` |
| `model` | str | LLM 名（6 个之一：GPT-4 / GPT-4o / Claude / Kimi / Llama / DeepSeek） | `GPT-4o` |
| `notes` | str | 切片信息：diagram_type / sheet / record_type | `diagram_type=stm; sheet=STM Results; record_type=sample_level_review` |

---

## `raw_samples.parquet`（107 行 × 32 列）

公开账本（Dataset.xlsx）原始 107 行；含未筛选样本（占位、缺失输出等）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id（固定 `llms_emp`） | `llms_emp` |
| `dataset_name` | str | 数据集名 | `G_Model SysML behavior model dataset` |
| `dataset_source_url` | str | 公开 URL | `https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6` |
| `row_id` | int | 在 Dataset.xlsx 中的行号（0-based） | `0` |
| `model_name` | str | 该 sample 对应的模型/制品标题 | `Activity diagram of rectification adjustment` |
| `model_source` | str | 该 sample 来源缩写（如 `EMUTC` 表示来自某出处） | `EMUTC` |
| `input_modality` | str | 输入模态分类 | `Natural-language requirements description` |
| `requirements_description` | str | 自然语言需求文本 | `1.The system should be able to switch the incoming AC 25 kV current ...` |
| `output_representation` | str | 输出形式（如 PlantUML） | `PlantUML` |
| `output_metamodel` | str | 输出元模型（具体 SysML 子类型） | `SysML v1.6 activity diagram expressed in PlantUML` |
| `diagram_type` | str | 图类型（`stm` / `act` / `sd`） | `act` |
| `plantuml_code` | str | 完整 PlantUML 输出代码 | `@startuml |start |...` |
| `selection_flag` | str | 论文是否在最终实验中选中此样本（`A` 选中 / 空 不选 等） | `A` |
| `diagram_annotation` | str | 论文给的图注释 / 标签 | _None_（多数为空） |
| `selected_by_authors` | bool | 是否被论文作者选入实验集 | `True` |
| `is_placeholder` | bool | 是否为占位行（未真正提交模型） | `False` |
| `has_requirements` | bool | 是否有需求文本 | `True` |
| `has_output_model` | bool | 是否有输出模型 | `True` |
| `is_complete_sample` | bool | 是否同时具备 requirements + output（实验有效样本） | `True` |
| `requirements_char_count` | int | 需求文本字符数 | `1234` |
| `requirements_line_count` | int | 需求文本行数 | `15` |
| `plantuml_char_count` | int | PlantUML 代码字符数 | `2345` |
| `plantuml_line_count` | int | PlantUML 代码行数 | `46` |
| `basic_state_count` | int (nullable) | 基本状态计数（仅 STM 有意义；ACT/SD 为 NaN） | `5` |
| `basic_transition_count` | int (nullable) | 基本迁移计数 | `7` |
| `basic_action_annotation_count` | int (nullable) | 动作注释计数 | `2` |
| `basic_hierarchical_state_count` | int (nullable) | 层次状态计数（嵌套状态数） | `0` |
| `basic_participant_count` | int (nullable) | （SD 专用）参与者数 | _NaN_ |
| `basic_message_count` | int (nullable) | （SD 专用）消息数 | _NaN_ |
| `basic_activity_action_count` | int (nullable) | （ACT 专用）动作节点数 | _NaN_ |
| `basic_decision_count` | int (nullable) | （ACT 专用）判定节点数 | _NaN_ |
| `basic_parallel_count` | int (nullable) | （ACT 专用）fork/join 节点数 | _NaN_ |

---

## `complete_samples.parquet`（98 行 × 32 列）

`raw_samples.parquet` 的子集：仅保留 `is_complete_sample=True` 的 98 行（38 STM / 21 ACT / 39 SD）。**字段与 `raw_samples.parquet` 完全一致**，不再重复列。

---

## `human_review.parquet`（192 行 × 31 列）

公开逐样本人评结果（来自 Experiment Results.xlsx）；每行一个 (sample × LLM) 配对。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `paper_slug` | str | 论文 slug | `llms_emp` |
| `paper_title` | str | 论文标题 | `Generating SysML Behavior Models via Large Language Models: an Empirical Study` |
| `record_source` | str | 记录来源工件路径（原始 xlsx 行） | `./raw/Experiment Results.xlsx` |
| `sheet_name` | str | xlsx 中的 sheet 名（`STM Results` / `ACT Results` / `SD Results`） | `STM Results` |
| `diagram_type` | str | 图类型 | `stm` |
| `record_type` | str | 记录类型（`sample_level_review` 表示逐样本评） | `sample_level_review` |
| `review_record_id` | str | 在该 sheet 中的行号（同 sheet 内唯一） | `STM Results:0` |
| `model_source` | str | sample 来源 | `EMUTC` |
| `model_name` | str | sample 标题 | `State Machine of Basic Braking Device` |
| `llm_name` | str | LLM 名（GPT-4 / GPT-4o / Claude / Kimi / Llama / DeepSeek） | `GPT-4o` |
| `prompt_text` | str | 给 LLM 的完整 prompt | `You are a SysML expert. Generate a state machine ...` |
| `input_text` | str | 自然语言输入（与 prompt 中的需求部分一致） | `1 The human driving mode is represented ...` |
| `ref_output_text` | str | 期望 PlantUML 输出 | `@startuml [*] --> human_mode : power_on ...` |
| `ref_output_format` | str | 期望输出格式 | `PlantUML / SysML behavior model` |
| `ref_output_artifact_path` | str | 期望输出来源工件相对路径 | `./raw/Dataset.xlsx` |
| `pred_output_text` | str | LLM 实际输出 | `@startuml [*] --> HumanDriving ...` |
| `pred_output_format` | str | LLM 输出格式 | `PlantUML / SysML behavior model` |
| `pred_output_artifact_path` | str | LLM 输出来源工件相对路径 | `./raw/Experiment Results.xlsx` |
| `review_target` | str | 评审对象（`generated_behavior_model` 等） | `generated_behavior_model` |
| `review_index` | float | 在该样本里的评审序号（如同一样本多轮，`1.0`/`2.0`...） | `1.0` |
| `human_review_score` | float | 人评分数（数值） | `0.4166666667` |
| `human_review_score_unit` | str | 分数单位 / 含义（如 `semantic_f1`） | `semantic_f1` |
| `human_review_summary` | str | 评审摘要（一句话） | `Manual grammar + semantic review with reference-model TP/FP/FN accounting.` |
| `human_review_details_json` | str (JSON) | 详细评审结果（含 grammar_hallucinations / semantic 漏检 等） | `{"initial": {...}, "after": {...}}` |
| `human_review_source_record_json` | str (JSON) | xlsx 原始行（保留所有列原貌） | `{"F1 Score": 0.4166666667, "False Negative": 6, ...}` |
| `human_review_original_text` | str | 评审者原始备注文本（自由文本） | `[grammar_hallucinations] transition does not connect two state` |
| `human_review_original_text_json` | str (JSON) | 评审者原始备注的结构化版（含来源列名） | `[{"column_name": "SysML Grammar Hallucinations", ...}]` |
| `paper_method_verbatim_excerpt` | str | 论文中 §Method 的相关原文摘录 | `[reviewer_pool] We have two groups: G_Search ...` |
| `paper_method_verbatim_excerpt_json` | str (JSON) | 上一字段的结构化版（含 source_path / line numbers） | `[{"end_line": 347, "label": "reviewer_pool", ...}]` |
| `verbatim_extraction_verified` | bool | 上一字段的摘录是否经过人工核对 | `True` |
| `review_rubric_text` | str | 评审 rubric 一段话描述 | `Grammar: manual comparison against SysML v1.6 grammar points. ...` |
| `public_artifact_limitations` | str | 公开工件已知缺口的说明 | `Workbook公开了逐样本结果，但人工审查日志只以汇总列形式保留在结果表中。` |

---

## `raw/` 原始资源（✅ 已下载）

| 文件 | 大小 | 来源 |
|------|------|------|
| `Dataset.xlsx` | 36K | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6) — 数据集主账本（NL + PlantUML） |
| `Experiment Results.xlsx` | 11M | 同上 — 6 个 LLM 的逐样本评审结果 |
| `ESE Expriment Results.xlsx` | 2.0M | 同上 — ESE 期刊扩展版的人评（增量样本） |
| `README.md` | 1.2K | Google Drive 上的数据集发布说明 |

`human_review.parquet` 与 `raw_samples.parquet` 中的 `*_artifact_path` 字段已指向上述 xlsx（相对当前 parquet 同级 `./raw/...`）。

## 复用性建议

- ✅ **最适合做主样本级 NL→STM benchmark**：唯一一个 input/ref/pred/score 都齐的数据集（192/192 全有）
- ✅ 192 行人评直接可用于训练 / 评测 reviewer / LLM-as-judge
- ⚠️ PlantUML 元模型偏 SysML v1.6，跟时间自动机有 gap，需要做格式转换
- ⚠️ 缺时间约束语义（`after`/`every` 等都没编入）
