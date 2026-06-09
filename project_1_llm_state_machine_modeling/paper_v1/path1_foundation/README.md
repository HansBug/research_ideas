# Path-1 第一篇论文奠基工作区

## 1. 定位

本目录是 `project_1_llm_state_machine_modeling` 第一篇论文的 **Path-1 paper foundation**。它接续历史 Path-1 sprint PR [#9](https://github.com/HansBug/research_ideas/pull/9)、导师讨论 PR [#31](https://github.com/HansBug/research_ideas/pull/31)、agent-loop 总线 PR [#22](https://github.com/HansBug/research_ideas/pull/22) 与投稿计划 issue [#67](https://github.com/HansBug/research_ideas/issues/67)，用于把后续 paper 工作从“路线讨论和实验基础设施”收口到“可写、可审、可执行的论文计划”。

本目录不是论文集，不收录 PDF；它是论文写作与实验执行的 durable planning / evidence workspace。

## 2. 当前结论

第一篇论文暂定走 **Path-1 baseline hard comparison**：研究自然语言控制系统需求到形式化状态机模型的 LLM 建模问题，重点证明形式化状态机表示、确定性检查反馈、可执行仿真反馈与 LLM agent 修复闭环能比近期 LLM-for-modeling / state-machine-generation baseline 提供更丰富、更可审计、更可执行的状态机建模结果。

一句话 thesis：

> We study whether executable formal feedback can improve LLM-based state-machine modeling from natural-language control-system requirements. We introduce a formalized state-machine representation and an agentic generate-check-simulate-repair loop, and evaluate its contribution through a frozen control-system benchmark, adapted component-level human adjudication, ablations, and comparisons with recent LLM-based modeling baselines.

中文口径：

> 本文研究可执行形式化反馈是否能提升 LLM 从自然语言控制系统需求生成状态机模型的质量。我们提出一种形式化状态机表示和 generate-check-simulate-repair agent loop，并通过冻结的控制系统 benchmark、改造的组件级人工评审、消融实验和近期 baseline 对比来评估其贡献。

## 3. 推荐阅读顺序

1. [paper_story.md](./paper_story.md)：论文 thesis、gap、贡献、claim 边界。
2. [project_inventory.md](./project_inventory.md)：当前仓库中与论文有关的证据、代码、baseline、run record 与缺口。
3. [sample_assets.md](./sample_assets.md)：从历史 PR #9 压缩迁移来的样本池、Top-15 / Backup-15、30 条扩充 NL 与 golden reference STM 信息。
4. [baseline_and_related_work_matrix.md](./baseline_and_related_work_matrix.md)：最近 baseline / related work 的实验定位与对齐方式。
5. [experiment_inventory.md](./experiment_inventory.md)：RQ、样本、baseline、metrics、oracle 与 run record 计划。
6. [claim_evidence_map.md](./claim_evidence_map.md)：强 claim、谨慎 claim、禁用 claim 与证据状态。
7. [reviewer_risk_register.md](./reviewer_risk_register.md)：按 C/I/M 维护的审稿风险与修复动作。
8. [execution_plan.md](./execution_plan.md)：从 foundation 到投稿冲刺的 gate-driven 执行方案。
9. [plan/progress.md](./plan/progress.md)：当前 PR / 后续 paper 工作进度与 review 记录。

## 4. 与历史 PR #9 的关系

PR #9 是 2026-05 Path-1 quick sprint 分支，提供了重要样本资产和 ref-STM 早期经验，但它不是当前论文主结果。当前目录只迁移其中可长期复用的事实与索引：

- `sources/` T0+🟢 候选池 323 sample 的筛选统计。
- Top-15 / Backup-15 样本表。
- 30 条 candidate / backup 的严格溯源 NL 扩充结果摘要。
- `sources_path1.parquet` / backup parquet 的历史位置与用途。
- 2 个 early golden reference STM（CARA 低-V、CubeSat 高-V）的经验与风险。

PR #9 中的自动评分、扩充 NL 和 golden reference 仍需在正式 paper 实验前复核；不得把它们直接写成最终实验结果。

## 5. 非目标

本 PR / 本目录当前不做：

1. 不运行主实验、不宣称已有最终 F1 / lift 数字。
2. 不写完整英文 manuscript。
3. 不把 E1/E2 写成 Hybrid 方法贡献。
4. 不把 `fcstm`、LangGraph、Codex、Claude 或某个工程实现写成论文主贡献。
5. 不把 LLM-as-Judge 当作主 oracle。
6. 不声称完成 BMC / LTL / 完整 model checking。

## 6. 当前验收标准

本 foundation PR ready 的最低标准：

- [ ] PR body 与本目录文档能无歧义说明第一篇论文 story、边界、执行计划和验收 gate。
- [ ] 已清楚标注 PR #9 资产的历史性质、可复用部分和不可直接当结果的部分。
- [ ] 样本、baseline、oracle、human adjudication、run record、claim-evidence、risk register 均有入口文件。
- [ ] 多智能体学术 review 后无 C/I 级事实、学术、可执行性问题；M 级问题可进入 follow-up。
- [ ] [paper_v1/README.md](../README.md) 已标注当前 overlay，避免新 session 误读 2026-05 sprint 旧口径。
