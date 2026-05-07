# `ttool-ai` review extraction

> 本篇方法分析见 [baselines/ttool-ai/DESC.md](../../baselines/ttool-ai/DESC.md)。

## 1. 论文元信息

- **标题**：System Architects Are not Alone Anymore: Automatic System Modeling with AI
- **作者**：Ludovic Apvrille, Bastien Sultan
- **单位**：Télécom Paris, IP Paris
- **年份 / Venue**：MODELSWARD 2024
- **DOI / arXiv / URL**：[hal-04483279](https://telecom-paris.hal.science/hal-04483279v1)
- **本篇 review 数据用途**：当前 reviewer 系统 dataset 中 `summary_level_run_score` / `case_aggregate_stat` / `raw_score_row` / `summary` / `overall_aggregate_stat` 等多类 summary-level scored 共 116 行的来源；提供 SysML 状态机（含块图 / 内部块图）的 summary-level scored 数据。

## 2. review 数据获取方式

- **来源类型**：☑ 公开仓库（GitHub）
- **入口 URL**：[github.com/zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)
  - 含 3 个测试系统目录：`platooning / space-basedsystem / AutomatedBraking`
  - 含规范 `.desc` 文件、TTool-AI 生成的 `.xml` 模型、复现实验 README、`result.ods`
- **本地落盘路径**：`discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/baseline_double_green_human_review_records.parquet`（`paper_slug == "ttool-ai"`）
- **当前可访问性**：☑ 已下载 + 已 parquet 化
- **首次访问时间戳**：约 `2026-04-15 01:03:52`

## 3. reviewer 资质与人数

- **reviewer 总人数**：N 学生 + N 工程师（论文实验中提及 student 评分作为对照）
- **资质**：🟡 学生评分 + 🟢 系统工程师对照
  - 论文实验对比：TTool-AI 在块图生成上得分 81/100（学生 70/100），状态机生成得分 63/100（学生 58/100）
- **是否独立**：☑ 多人独立评分（学生组 vs 专家对照组）
- **是否报告 inter-rater agreement**：⚪ 论文未显式报告 Kappa，但有学生组 vs 专家组对照

## 4. review 数据 schema

### 4.1 单条 review 的字段

reviewer 系统的 parquet 中 `paper_slug == "ttool-ai"` 共 116 行，分布在多种 record_type：

| record_type | 行数 | 用途 |
|---|---:|---|
| `summary_level_run_score` | 30 | 单次运行的 summary 评分 |
| `case_aggregate_stat` | 36 | 案例级聚合统计 |
| `raw_score_row` | 30 | 原始评分行 |
| `summary` | 12 | 顶层 summary |
| `overall_aggregate_stat` | 8 | 整体聚合 |

字段：

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `review_record_id` | string | unique | |
| `case_id` | string | `platooning / space-basedsystem / AutomatedBraking` | 3 个测试系统 |
| `case_name` | string | e.g. `Platoon3`, `System5` | 单个 sub-case |
| `diagram_type` | string | `bd` / `smd` | block diagram / state machine diagram |
| `review_target` | string | `BD / SMD / Properties / UCD / All` | |
| `human_review_score` | float | 0-100（论文里的 100 分制） | |
| `human_review_score_unit` | string | `score_0_100` | |
| `pred_output_artifact_path` | string | TTool-AI 生成的 `.xml` 模型路径 | |

### 4.2 数据规模

- artifact 总数：3 个测试系统 × 多个 sub-cases × 2 diagram types = **116 行**
- reviewer 总数：学生组 + 工程师对照组（具体 N 未公开）
- review 总条数：**116 行**（已聚合）

### 4.3 评分聚合方式

- 论文是否提供原始评分表（每条独立）：☑ 是（GitHub 仓库的 `result.ods` 含每条 raw_score_row）
- 论文公开的是聚合后的（mean / median / vote）：☑ 是（同时提供 raw 与 aggregated）
- 当前 corpus 持有的是哪一种：☑ 两种都持有（30 条 raw_score_row + 30 条 summary_level_run_score + 各级聚合）

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| score 0-100 | `human_review_score`（0-100，单位 `score_0_100`） | 直接 |
| BD / SMD / UCD / Properties | `review_target` | 保留分类 |
| platooning / space-based / AutomatedBraking | `case_id` | 保留 |
| `diagram_type` (`bd` / `smd`) | `diagram_type` | 保留 |

## 6. 落盘与 parquet 化

- 本地数据路径：`discussions/.../baseline_double_green_human_review_records.parquet`
- parquet schema 是否对齐到 `baseline_double_green_human_review_records` schema：☑ 是
- parquet 行数：**116** 行（占总 820 行的 14.1%）
- 当前 reviewer benchmark 是否已能消费：☑ 是

## 7. 状态

🟢 直接可用

## 8. 后续动作

已完成：

- GitHub 公开数据已下载并 parquet 化
- reviewer benchmark 主路径已消费

待办：

- 若需要 reviewer-level 原始评分（每位学生 / 工程师独立），可以从 GitHub 仓库的 `result.ods` 进一步抽取（当前 raw_score_row 30 条已含按 reviewer 聚合的部分）
- 论文提到的"15.2x / 67.5x speedup"等运行时数据已在 baseline parquet 中保留

阻塞：

- 无

## 9. 更新日志

- `2026-05-06 13:54:54`：初版 review_extraction.md 入库；数据沿用现有 parquet（baseline 双绿 2026-04-15）
