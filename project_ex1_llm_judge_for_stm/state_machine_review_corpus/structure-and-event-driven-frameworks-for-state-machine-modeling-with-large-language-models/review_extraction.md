# `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` review extraction

> 本篇方法分析见 [baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md)。

## 1. 论文元信息

- **标题**：Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models
- **作者**：Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian, Boqi Chen, Gunter Mussbacher
- **单位**：McGill University, Department of Electrical and Computer Engineering
- **年份 / Venue**：arXiv 预印本 2026-03-31（cs.SE）
- **DOI / arXiv / URL**：[arXiv:2604.00275](https://arxiv.org/abs/2604.00275) / DOI 10.48550/arXiv.2604.00275
- **本篇 review 数据用途**：当前 reviewer 系统 dataset 中 `component_level_review` 类全部 512 行的来源；覆盖 7 类状态机要素（states / transitions / guards / actions / hierarchical states / parallel regions / history states）的 component-level human review。

## 2. review 数据获取方式

- **来源类型**：☑ 论文 supplementary / artifact + ☑ 论文 tables 抽取
- **入口 URL**：
  - 匿名 artifact：[anonymous.4open.science/r/llm_state_machine_modeling](https://anonymous.4open.science/r/llm_state_machine_modeling/)
  - 论文正文表格中给出每个组件的 TP/FP/FN 与 macro-F1 数据
- **本地落盘路径**：现有 dataset 路径 `project_1_llm_state_machine_modeling/discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/baseline_double_green_human_review_records.parquet`（`paper_slug == "structure-and-event-driven-frameworks-..."`）
- **当前可访问性**：☑ 已下载 + 已 parquet 化
- **首次访问时间戳**：约 `2026-04-15 01:03:52`（baseline 双绿 parquet 化时）

## 3. reviewer 资质与人数

- **reviewer 总人数**：121 名 CS / SE 学生（来自美国 3 所大学的 senior / graduate level 课程）
- **资质**：🟡 学生（高年级 + 经过任务训练）—— 论文方法细节里说明每位 reviewer 接受了 PlantUML 渲染的状态机图与 ground-truth 对照训练后再独立打分
- **是否独立**：☑ 是（学生 reviewer，不是论文作者）
- **是否报告 inter-rater agreement**：⚪ 论文未显式报告 Cohen Kappa；但因为评估口径是 component-level TP/FP/FN（参考 ground truth），单点评分判定较客观，agreement 风险较小

## 4. review 数据 schema

### 4.1 单条 review 的字段（已对齐到 reviewer parquet schema）

reviewer 系统的 `baseline_double_green_human_review_records.parquet` 中 `record_type == "component_level_review"` 的 512 行携带的关键字段：

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `review_record_id` | string | unique | 单条 review 标识 |
| `case_id` / `case_name` | string | e.g. `SSC7_fall_2024` | 8 个非结构化 reactive-system 之一 |
| `diagram_type` | string | "stm" 等 | UML state machine |
| `strategy_name` | string | `Single-Prompt / Structure-Driven SMF / Event-Driven SMF / Hybrid` | 论文 4 条路线之一 |
| `llm_name` | string | e.g. `Claude 3.5 Sonnet / GPT-4 / Gemini` | 评估对象 |
| `review_target` | categorical | `States / Transitions / Guards / Actions / Hierarchical states / Parallel Regions / History States / All` | 7 类组件 + All |
| `human_review_score` | float | TP/FP/FN 推导的 component F1 / 单点判定 0/1 | 单组件 review |
| `human_review_score_unit` | string | `component_f1` 或 `pass_fail` | |
| `pred_output_text` / `ref_output_text` | string | UML state machine 文本 | LLM 输出 + ground truth |

### 4.2 数据规模

- artifact 总数：**8** 个 reactive-system descriptions × 多个 LLM × 4 strategies × 7+1 review_target = **512 component-level review 条目**
- reviewer 总数：121 学生
- 每个 artifact 平均被几位 reviewer 评：未公开（因为评分被聚合为 TP/FP/FN）
- review 总条数：**512 行**（已聚合为单条 review_record_id）

### 4.3 评分聚合方式

- 论文是否提供原始评分表（每条独立）：⚪ 否（仅聚合 TP/FP/FN/F1）
- 论文公开的是聚合后的（mean / median / vote）：☑ 是（component-level F1）
- 当前 corpus 持有的是哪一种：聚合后（已 parquet 化为 512 行 `component_level_review`）

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| component-level F1 | `human_review_score`（连续 0-1） | 直接 = component F1 |
| review_target（7 类） | `review_target` | 直接保留分类标签 |
| LLM strategy name | `strategy_name` | 保留 |
| 8 个 reactive-system | `case_id` / `case_name` | 保留 |

## 6. 落盘与 parquet 化

- 本地数据路径：`discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/baseline_double_green_human_review_records.parquet`
- parquet schema 是否对齐到 `baseline_double_green_human_review_records` schema：☑ 是
- parquet 行数：**512** 行（占总 820 行的 62.4%）
- 当前 reviewer benchmark 是否已能消费：☑ 是（现已是 reviewer dataset 的最大组成部分）

## 7. 状态

🟢 直接可用

## 8. 后续动作

已完成：

- 数据已抽取并 parquet 化
- reviewer benchmark 主路径已消费

待办：

- 若匿名 4open.science artifact 失效，需要联系 McGill 团队（Mussbacher）拿 artifact 镜像
- 若有需要，可联系作者拿 reviewer-level 原始评分表（当前持有的是聚合 F1）

阻塞：

- 无（当前 dataset 已 parquet 化）

## 9. 更新日志

- `2026-05-06 13:54:54`：初版 review_extraction.md 入库；数据沿用现有 parquet（baseline 双绿 2026-04-15）
