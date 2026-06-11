# Path-1 第一篇论文奠基工作区

## 1. 定位

本目录是 `project_1_llm_state_machine_modeling` 第一篇论文的 **Path-1 paper foundation**。它接续历史 Path-1 sprint PR [#9](https://github.com/HansBug/research_ideas/pull/9)、导师讨论 PR [#31](https://github.com/HansBug/research_ideas/pull/31)、agent-loop 总线 PR [#22](https://github.com/HansBug/research_ideas/pull/22) 与投稿计划 issue [#67](https://github.com/HansBug/research_ideas/issues/67)，用于把后续 paper 工作从“路线讨论和实验基础设施”收口到“可写、可审、可执行的论文计划”。

本目录不是论文集，不收录 PDF；它是论文写作与实验执行的 durable planning / evidence workspace。

## 2. 当前结论

第一篇论文暂定走 **Path-1 baseline hard comparison**：研究自然语言控制系统需求到形式化状态机模型的 LLM 建模问题，重点检验形式化状态机表示、确定性检查反馈、可执行仿真反馈与 LLM agent 修复闭环是否能相对近期 LLM-for-modeling / state-machine-generation baseline 提供更完整、更可执行、更高质量的状态机建模结果；run record 只作为实验复核、打假和排障支撑，不列为学术贡献。

一句话中文口径：

> 本文研究可执行形式化反馈是否能提升 LLM 从自然语言控制系统需求生成状态机模型的质量。本 foundation PR 只规划形式化状态机表示、生成-检查-仿真-修复 agent loop，以及后续在冻结 benchmark、组件级人工评审、消融实验和近期 baseline 对比中必须补齐的证据；在这些证据完成前，不提前声明结果型结论。

投稿策略按 issue [#67](https://github.com/HansBug/research_ideas/issues/67) 固定为：**按 CCF-A 论文标准打磨，2026 夏季优先投 CCF-B 期刊**。默认主投 SoSyM regular rolling，ASE Journal / Requirements Engineering Journal regular rolling 作备投；具体质量门禁见 [story/venue_readiness_gate.md](./story/venue_readiness_gate.md)。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文 thesis、gap、贡献边界、target venue/readiness 和 claim-evidence gate | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、baseline / related-work 对齐矩阵 | [evidence/README.md](./evidence/README.md) |
| [dataset_selection/](./dataset_selection/) | 样本选择、PR #9 历史资产归档、后续 frozen registry 入口 | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | RQ、实验合同、执行 gate、reviewer risk register | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前 PR 任务状态、review 记录和 task packet | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

1. [story/paper_story.md](./story/paper_story.md)：论文 thesis、gap、贡献、claim 边界。
2. [story/paper_outline.md](./story/paper_outline.md)：章节大纲、RQ、9 个五绿 direct baseline 反证门和投稿前证据门。
3. [story/venue_readiness_gate.md](./story/venue_readiness_gate.md)：按 CCF-A 标准打磨、优先投 CCF-B 期刊的目标出口与质量门禁。
4. [evidence/project_inventory.md](./evidence/project_inventory.md)：当前仓库中与论文有关的证据、代码、baseline、run record 与缺口。
5. [dataset_selection/sample_assets.md](./dataset_selection/sample_assets.md)：从历史 PR #9 迁移来的样本池、Top-15 / Backup-15、30 条扩充 NL 与 historical early reference draft 信息。
6. [dataset_selection/legacy_pr9_assets/README.md](./dataset_selection/legacy_pr9_assets/README.md)：PR #9 详细原始资产归档入口。
7. [evidence/baseline_and_related_work_matrix.md](./evidence/baseline_and_related_work_matrix.md)：最近 baseline / related work 的实验定位与对齐方式。
8. [experiment_design/experiment_inventory.md](./experiment_design/experiment_inventory.md)：RQ、样本、baseline、metrics、oracle 与 run record 计划。
9. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：强 claim、谨慎 claim、禁用 claim 与证据状态。
10. [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)：按 C/I/M 维护的审稿风险与修复动作。
11. [experiment_design/execution_plan.md](./experiment_design/execution_plan.md)：从 foundation 到投稿冲刺的 gate-driven 执行方案。
12. [plan/progress.md](./plan/progress.md)：当前 PR / 后续 paper 工作进度与 review 记录。

## 5. 与历史 PR #9 的关系

PR #9 是 2026-05 Path-1 quick sprint 分支，提供了重要样本资产和 ref-STM 早期经验，但它不是当前论文主结果。当前目录已经把其中可长期复用的事实、索引和原始资产归档到 [dataset_selection/legacy_pr9_assets/](./dataset_selection/legacy_pr9_assets/)：

- `sources/` T0+🟢 候选池 323 sample 的筛选输入、323 个自动评审 JSON、Top-15 / Backup-15 报告和 `summary.csv`。
- 30 条 candidate / backup 的严格溯源 NL 扩充报告、30 个 expansion JSON 和 provenance。
- `sources_path1.parquet` / `sources_path1_backup.parquet` 历史数据快照。
- 2 个 early historical reference draft（CARA 低-V、CubeSat 高-V）、handover、prompt 和辅助脚本。
- 文件级 [asset_manifest.tsv](./dataset_selection/asset_manifest.tsv) 与数量摘要 [asset_summary.json](./dataset_selection/asset_summary.json)。

PR #9 中的自动评分、扩充 NL 和 historical early reference draft 仍需在正式 paper 实验前复核；不得把它们直接写成最终实验结果。

## 5.1 与 PR #92 baseline 增量的关系

PR [#92](https://github.com/HansBug/research_ideas/pull/92) 已于 2026-06-10 合入 `main`，并补充 2025-2026 arXiv 的 LLM→STM-family direct baseline 与强近邻候选。本 PR 不复制 PR #92 的完整 baseline 文库内容，但后续 S1 baseline / related-work 冻结前必须直接读取 `main` 中最新 [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md)、[../../baselines/arxiv-census-2025-2026-stm-candidates.md](../../baselines/arxiv-census-2025-2026-stm-candidates.md) 和 9 个五绿 direct baseline 的单篇 `paper_content.txt` / `DESC.md` / `ASSETS.md`。S1a 是 **blocking absorption gate**：不能只看总账摘要，必须逐篇写清输入、输出、方法、反馈/验证、数据/复现性和能力上限，再决定 strict executable / approximate / evidence-only 分类。这样可以避免第一篇论文基于过期或过浅 baseline corpus 设计 competitor。

## 6. 非目标

本 PR / 本目录当前不做：

1. 不运行主实验、不宣称已有最终 F1 / lift 数字。
2. 不写完整英文 manuscript。
3. 不把 E1/E2 写成 Hybrid 方法贡献。
4. 不把 `fcstm`、LangGraph、Codex、Claude 或某个工程实现写成论文主贡献。
5. 不把 LLM-as-Judge 当作主 oracle。
6. 不声称完成 BMC / LTL / 完整 model checking。

## 7. 当前验收标准

本 foundation PR ready 的最低标准：

- [x] PR body 与本目录文档能无歧义说明第一篇论文 story、边界、执行计划和验收 gate。
- [x] 已清楚标注 PR #9 资产的历史性质、可复用部分和不可直接当结果的部分。
- [x] 样本、baseline、oracle、human adjudication、run record、claim-evidence、risk register 均有入口文件。
- [x] 目标投稿策略已固化为“按 CCF-A 标准打磨，优先投 CCF-B 期刊”，并将 SoSyM / ASEJ / REJ readiness gate 写入后续执行约束。
- [x] 多智能体学术 review 后无 C/I 级事实、学术、可执行性问题；M 级问题可进入 follow-up。
- [x] [paper_v1/README.md](../README.md) 已标注当前 overlay，避免新 session 误读 2026-05 sprint 旧口径。
