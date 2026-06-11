# Path-1 第一篇论文奠基工作区

## 1. 定位

本目录是 `project_1_llm_state_machine_modeling` 第一篇论文的 **Path-1 paper foundation**。它接续历史 Path-1 sprint PR [#9](https://github.com/HansBug/research_ideas/pull/9)、导师讨论 PR [#31](https://github.com/HansBug/research_ideas/pull/31)、agent-loop 总线 PR [#22](https://github.com/HansBug/research_ideas/pull/22)、伞 PR [#93](https://github.com/HansBug/research_ideas/pull/93)、S1a baseline 专项盘点 PR [#94](https://github.com/HansBug/research_ideas/pull/94) 与 S0a story-reframe PR [#96](https://github.com/HansBug/research_ideas/pull/96)，用于把后续 paper 工作从“路线讨论和实验基础设施”收口到“可写、可审、可执行的论文计划”。

本目录不是论文集，不收录 PDF；它是论文写作与实验执行的 durable planning / evidence workspace。

## 2. 当前 S0a 结论

第一篇论文暂定走 **Path-1 baseline hard comparison**，但 S1a 九个 direct baseline 已经打穿旧的“首个 NL-to-STM / 首个反馈闭环”叙事。S0a 后，本文主线收敛为：

> 在自然语言控制系统需求到状态机模型生成任务中，研究可机检、可执行的状态机表示能否把 LLM 生成结果带入 deterministic diagnostics、scenario-level simulation feedback 和 structured repair decision 的闭环，并在 frozen sample、human adjudication、B0-B5 消融、EXT 外部近似对照与 baseline-aware protocol 下检验模型质量和修复稳定性是否产生可防守的边际变化。

当前必须同时遵守：

1. **不主打 `fcstm` / `pyfcstm`**：论文主文使用 formalized / executable / machine-checkable state-machine representation；内部 DSL 只作为 implementation / artifact。
2. **不把过程性工程材料写入论文贡献或方法主线**：论文主文只呈现样本、预算、oracle、统计口径等必要实验条件，不主动叙述过程性工程材料。
3. **不把 E1/E2 写成 Hybrid contribution**：E1/E2 只是 agent orchestration condition / RQ dimension。
4. **不写结果型 claim**：G3/G5 前不得写 “we improve quality / we show improvement / same benchmark win”。
5. **先过 S0a，再做 S0b**：旧 S0 的 `DIRECTION.md`、`abstract_v0.md`、`target_venue_decision.md` 必须后移到 S0b / PR-S0-Direction，在 S0a 新 story 后冻结。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文 thesis、gap、contribution 边界、terminology policy、target venue readiness 和 claim-evidence gate | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、baseline / related-work 对齐矩阵 | [evidence/README.md](./evidence/README.md) |
| [dataset_selection/](./dataset_selection/) | 样本选择、PR #9 历史资产归档、后续 frozen registry 入口 | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | RQ、实验合同、执行 gate、reviewer risk register | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前 PR 任务状态、review 记录和 task packet | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

后续 agent / 人类进入本目录时，必须先按 S0a gate 阅读，而不是从旧 venue-first 路线开始：

1. [story/paper_story.md](./story/paper_story.md)：S0a 后的新 thesis、gap、method insight、contributions、claims-to-avoid。
2. [story/terminology_policy.md](./story/terminology_policy.md)：`fcstm` / `pyfcstm` 弱化策略、preferred / forbidden wording。
3. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：每条 claim 的 status、baseline_coverage、marginal_claim、forbidden_softened_claims 与 safe wording。
4. [story/paper_outline.md](./story/paper_outline.md)：Introduction、Related Work、Method、Experiment、Threats 的 S0a 后章节逻辑。
5. [evidence/baseline_and_related_work_matrix.md](./evidence/baseline_and_related_work_matrix.md)：四个 mandatory closest works 与 strict / approximate / near / evidence-only 分层。
6. [experiment_design/experiment_inventory.md](./experiment_design/experiment_inventory.md)：RQ、B0-B5 条件、EXT 外部 baseline 分层、样本、oracle、metrics 与内部实验管理要求。
7. [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)：novelty、baseline fairness、oracle、formal overclaim、soft novelty、命名等 C/I/M 风险。
8. [experiment_design/execution_plan.md](./experiment_design/execution_plan.md)：S0a/S0b 拆分、Mermaid 依赖图、G0a/G0b gate 与 stop condition。
9. [story/venue_readiness_gate.md](./story/venue_readiness_gate.md)：仅作为 S0b 的 venue readiness 背景与 CCF-A 强度门禁，不代表 S0a 已冻结最终投稿期刊。
10. [dataset_selection/sample_assets.md](./dataset_selection/sample_assets.md)：PR #9 historical assets 与正式样本冻结前的复核要求。
11. [plan/progress.md](./plan/progress.md)：当前 PR / 后续 paper 工作进度与 review 记录。

## 5. 与历史 PR #9 的关系

PR #9 是 2026-05 Path-1 quick sprint 分支，提供了重要样本资产和 ref-STM 早期经验，但它不是当前论文主结果。当前目录已经把其中可长期复用的事实、索引和原始资产归档到 [dataset_selection/legacy_pr9_assets/](./dataset_selection/legacy_pr9_assets/)：

- `sources/` T0+🟢 候选池 323 sample 的筛选输入、323 个自动评审 JSON、Top-15 / Backup-15 报告和 `summary.csv`。
- 30 条 candidate / backup 的严格溯源 NL 扩充报告、30 个 expansion JSON 和 provenance。
- `sources_path1.parquet` / `sources_path1_backup.parquet` 历史数据快照。
- 2 个 early historical reference draft（CARA 低-V、CubeSat 高-V）、handover、prompt 和辅助脚本。
- 文件级 [asset_manifest.tsv](./dataset_selection/asset_manifest.tsv) 与数量摘要 [asset_summary.json](./dataset_selection/asset_summary.json)。

PR #9 中的自动评分、扩充 NL 和 historical early reference draft 仍需在正式 paper 实验前复核；不得把它们直接写成最终实验结果。

## 5.1 与 PR #92 / PR #94 baseline 增量的关系

PR [#92](https://github.com/HansBug/research_ideas/pull/92) 已补充 2025-2026 arXiv 的 LLM→STM-family direct baseline 与强近邻候选。PR [#94](https://github.com/HansBug/research_ideas/pull/94) 已在本 foundation 下完成 S1a 九个 direct baseline 专项盘点，当前总账是 [baselines/SUMMARY.md](./baselines/SUMMARY.md)，逐篇文件在 [baselines/papers/](./baselines/papers/)。

S1a 结论已改变第一篇 story：后续 S1b/S2/S3/S5 必须先通过 S0a 新 story gate，不能继续沿用“首个 NL-to-STM / 首个 feedback loop / prior work only draws diagrams”的旧 novelty。

## 6. 非目标

本目录当前不做：

1. 不运行四例真实 agent-loop、不运行主实验、不宣称已有最终 F1 / lift 数字。
2. 不写完整英文 manuscript。
3. 不把 E1/E2 写成 Hybrid 方法贡献。
4. 不把 `fcstm`、LangGraph、Codex、Claude 或某个工程实现写成论文主贡献。
5. 不把 LLM-as-Judge 当作主 oracle。
6. 不声称完成 BMC / LTL / 完整 model checking。
7. 不在 S0a 阶段冻结最终投稿期刊；S0b 才写 `target_venue_decision.md`。

## 7. 当前验收标准

当前 S0a / foundation ready 的最低标准：

- [x] PR body 与本目录文档能无歧义说明第一篇论文 story、边界、执行计划和验收 gate。
- [x] 已清楚标注 PR #9 资产的历史性质、可复用部分和不可直接当结果的部分。
- [x] 样本、baseline、oracle、human adjudication、claim-evidence、risk register 与实验管理均有入口文件。
- [x] 四个 mandatory closest works（Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs）已进入 story、claim map、outline、baseline matrix、risk 和 execution gate。
- [x] `fcstm` / `pyfcstm`、agent framework、E1/E2 均已降级为 implementation / evidence / condition；过程性工程材料不进入论文 contribution / Method。
- [x] S0a/S0b 已拆分；旧 “S0 先冻结 abstract / venue” 路线被 execution plan 与入口文档阻断。
- [x] S0a 不跑四例真实 agent-loop；真实运行留给样本、oracle、baseline budget 与 runtime 条件冻结后的 S3/S4。
- [ ] PR #96 实现后多智能体学术 review 无 C/I 级事实、学术、可执行性问题；M 级问题可进入 follow-up。
