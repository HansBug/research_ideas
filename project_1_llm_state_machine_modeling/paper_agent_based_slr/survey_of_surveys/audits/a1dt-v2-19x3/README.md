# A1-DT v2 19×3 原生维度树审计批次

本目录是 PR #135 A1-DT v2 的独立审计入口。v1 目录 [../a1dt-19x3/](../a1dt-19x3/) 只作为历史归档；v2 的 prompt、结果、日志和裁决不得写入 v1 目录。

## 目标

v2 审计检查 19 篇 `review.md` 是否真正复原了单篇论文的**原生维度树 / 维度森林**，而不是把 A1-M0--M6 或通用接口反向写成原文 schema。每篇论文由 `codex`、`claude`、`deepseek` 三路审计，共 57 个任务。

审计重点：

1. 原文 RQ、贡献声明、样本单位、抽取表、分类 schema、统计表、roadmap / guideline stage 与 finding path 是否进入单篇原生树。
2. A1-M0--M6 是否只作为跨论文投影矩阵，而不是单篇原生树。
3. roadmap、vision、proposal、guideline、theory-roadmap 等无系统样本库论文是否已降级，且不进入主统计池。
4. v2 结果是否保留 `schema_seed`、`not_verified`、`needs_manual_check` 等 A2a 前降级状态。

## 当前状态

- 批次创建日期：2026-06-30
- 当前状态：57/57 三路 CLI 审计完成；19/19 主线程裁决完成；19/19 `review.md` 已按 v2 口径重写；结构门禁已通过。
- 任务数：19 篇 × 3 agent = 57
- 任务清单：[TASKS.tsv](./TASKS.tsv)
- prompts：[prompts/](./prompts/)
- results：[results/](./results/)
- logs：[logs/](./logs/)
- adjudications：[adjudications/](./adjudications/)
- 结构门禁：从仓库根运行 `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict`；从本目录运行 `python check_structure.py --strict`

## 产物边界

本目录保存 A1-DT v2 的完整审计证据链：原始 prompt、三路 raw result、运行 log、主线程 adjudication、结构门禁脚本和复验命令。A1-DT v2 已完成“原生维度树 / 维度森林”重写，但仍不承担 A2a 的页码 / 表号 / 图号 / supplementary 精核；所有定量统计和 final research finding 仍需后续阶段升级证据强度后再使用。
