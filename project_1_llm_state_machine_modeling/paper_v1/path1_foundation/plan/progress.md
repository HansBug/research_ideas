# Path-1 Foundation Progress

## 当前阶段

- Branch：`paper/project1-path1-s0a-story-reframe`
- 上游：PR #93 foundation；当前执行 PR #96 / S0a Story-Reframe。
- 目标：把 PR #94 / S1a baseline 反证、PR #31 导师口径、`fcstm` 弱化策略、run-record 降级策略和 S0a/S0b 分工落实到 story、claim map、outline、baseline matrix、experiment design、risk register、execution plan 与入口文档。
- 状态：S0a 文档实现已合流并通过本地文档检查；待提交推送和正式三路实现后 review。本 PR 不触碰 runtime、runner、样本冻结、oracle 冻结或真实实验链路。

## 已完成

- 使用 `$ai-research-writing-skill` / `$research-planning` / `$sub-agents` 约束任务。
- 读取并吸收导师讨论、PR #9、PR #31、PR #22、issue #67、baseline / method / eval 当前资料。
- 建立 `path1_foundation/` 工作区。
- 归档 PR #9 的 selection / expansion / parquet / ref-STM 原始资产，不将其写成 current result。
- 将 `path1_foundation/` 分层为 `story/`、`evidence/`、`dataset_selection/`、`experiment_design/` 与 `plan/`。
- PR #96 / S0a 本轮已读取 PR #96 body、PR #93 body 中 S0a/S0b 依赖信息、PR #94 / S1a baseline 总账 §11、PR #31 导师讨论记录，以及 foundation 根入口、story、evidence、experiment_design、plan 文件。
- S0a 入口文档已明确要求先读 [../story/paper_story.md](../story/paper_story.md)、[../story/terminology_policy.md](../story/terminology_policy.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/paper_outline.md](../story/paper_outline.md) 和 baseline carve-out，再进入 experiment / venue / progress。
- [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 已重定位为 S0b venue readiness 背景输入；最终 `target_venue_decision.md`、abstract v0 和投稿路线由 S0b 冻结。
- 已用 4 个 codex spawn subagents 并行处理 S0a 分片：story/claim/terminology、outline/baseline matrix、experiment/risk/execution、README/venue/progress；主 session 已合流。

## 本 PR 产物

| 文件 | 作用 |
|---|---|
| [../README.md](../README.md) | foundation 入口 |
| [../story/README.md](../story/README.md) | story 分层入口 |
| [../story/paper_story.md](../story/paper_story.md) | thesis、gap、contributions、claims |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | claim gate |
| [../story/terminology_policy.md](../story/terminology_policy.md) | S0a terminology gate；本轮入口文档已将其纳入必读依赖 |
| [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) | S0b venue readiness 背景输入 |
| [../evidence/README.md](../evidence/README.md) | evidence 分层入口 |
| [../evidence/project_inventory.md](../evidence/project_inventory.md) | repo evidence inventory |
| [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md) | closest prior works 与实验对齐计划 |
| [../dataset_selection/README.md](../dataset_selection/README.md) | dataset selection 分层入口 |
| [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md) | PR #9 样本/扩充/ref资产迁移说明 |
| [../dataset_selection/legacy_pr9_assets/README.md](../dataset_selection/legacy_pr9_assets/README.md) | PR #9 原始资产归档入口 |
| [../dataset_selection/asset_manifest.tsv](../dataset_selection/asset_manifest.tsv) | 归档资产文件级 SHA-256 清单 |
| [../dataset_selection/asset_summary.json](../dataset_selection/asset_summary.json) | 归档资产数量摘要 |
| [../experiment_design/README.md](../experiment_design/README.md) | experiment design 分层入口 |
| [../experiment_design/experiment_inventory.md](../experiment_design/experiment_inventory.md) | RQ、baseline、metrics、oracle、run record |
| [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) | C/I/M 风险台账 |
| [../experiment_design/execution_plan.md](../experiment_design/execution_plan.md) | gate-driven 执行计划 |
| [./README.md](./README.md) | plan 分层入口 |
| [./task-packets/foundation.md](./task-packets/foundation.md) | 本任务 packet |

## Validation / review log

| 时间 | 动作 | 结果 |
|---|---|---|
| 2026-06-09 | PR #9 asset extraction subagent review | 确认可迁移为 historical assets；C 风险是误写成 current paper result |
| 2026-06-09 | academic critic reviewer | C1：旧 eval protocol 与正式 oracle 透明度冲突；I1：claim gate 过强；I2：样本池口径需 reconciliation |
| 2026-06-09 | paper story reviewer | C1：Abstract gate 放行 planned experiment claim；I：缺 durable experiment / literature artifacts，progress 落后 |
| 2026-06-09 | execution verifier reviewer | I：`paper_v1/README.md` 历史 sprint 入口仍误导；review/progress 证据需同步 |
| 2026-06-09 | C/I 修复迭代 | 收紧 claim status、明确 formal paper protocol supersedes 旧 eval LLM-assistance 口径、补 candidate pools reconciliation、清理旧 README 入口、同步 progress 与 literature/citation artifact gate |
| 2026-06-09 | academic critic reviewer 二轮 | READY；确认旧 eval 口径已被 supersede、claim gate 已收紧、样本池 reconciliation 已补、无 Path-2/Hybrid/DSL/LangGraph/Codex 主线漂移 |
| 2026-06-09 | paper story reviewer 二轮 | READY；确认结果型 Abstract/Introduction 句式已降级为 Planned，literature/citation gate 已记录，progress 记录完整 |
| 2026-06-09 | execution verifier reviewer 二轮 | READY；确认 PR body 与文档一致、旧 sprint 入口误导已清理、sanity/link checks 可验收 |
| 2026-06-09 | 最终三路复核 | READY；C=0/I=0；仅发现 README ready checklist 呈现不一致等 M 级问题，并已修正 |
| 2026-06-10 | PR #9 详细资产归档 | 已归档并纳入 manifest 391 个历史资产 / 说明文件：323 个 selection review、30 个 expansion JSON、2 个 parquet、2 个 reference draft 目录及 legacy 子路径 README，并生成 manifest / summary |
| 2026-06-10 | foundation 分层 README 收口 | 新增 story/evidence/dataset_selection/experiment_design/plan 及 legacy asset 子路径中文 README，修正 current overlay 旧路径 |
| 2026-06-10 | 最终 execution verifier review | 发现 I：`asset_manifest.tsv` 中 `selection_screening/README.md` bytes/SHA 与当前文件不一致；已修复 manifest 与 summary，并将 manifest 覆盖范围扩大为整个 `legacy_pr9_assets/` 目录 391 个文件；深度 manifest 复算纳入检查 |
| 2026-06-10 | PR #92 baseline 增量吸收要求 | 根据用户要求，补充“baseline 现状再摸排 / 吸收 PR #92 近期 arXiv 增量”为后续 S1a 子任务，避免基于过期 baseline corpus 冻结 competitor |
| 2026-06-10 | PR body 中文化要求 | 根据用户要求，后续 PR body 尽量中文化，Mermaid 节点使用中文，英文只保留必要术语 / 论文候选句 |
| 2026-06-10 | 论文主线与 direct baseline 反证门补强 | 使用 `$ai-research-writing-skill` story / reviewer 规则与多智能体调研，吸收导师讨论和 9 个五绿 direct baseline 全文审查结论；新增 [paper_outline.md](../story/paper_outline.md)，并将 S1a 升级为 9 direct baseline blocking absorption gate |
| 2026-06-10 | CCF-A 标准 / CCF-B 目标期刊门禁（旧 foundation 口径） | 根据 issue #67 补充 [venue_readiness_gate.md](../story/venue_readiness_gate.md) 的 CCF-A reviewer 强度、候选 SoSyM / ASEJ / REJ 出口和 novelty、baseline、oracle、artifact、threats、writing gate；S0a 已将其重定位为 S0b 背景输入，不再把该文件视为最终 venue 决策。 |
| 2026-06-11 17:01:20 | PR #96 / S0a 多 subagent 文档实现 | 使用 `$ai-research-writing-skill` story / claim-evidence 规则，并启动 4 个 codex spawn subagents 并行覆盖 story/claim/terminology、outline/baseline matrix、experiment/risk/execution、README/venue/progress；主 session 合流到 S0a 文档实现。未跑四例 agent-loop / skill 真实例子，因为本轮不触碰 runtime、runner、样本冻结、oracle 冻结或实验链路。 |
| 2026-06-11 18:16:52 | 响应 PR #96 codex reviewer I-1 | 修正 [../baselines/SUMMARY.md](../baselines/SUMMARY.md) 中 S1a 旧 story wording：新增 S0a supersession note，并将 `DSL` / `质量提升` / contribution 表述改为可机检 / 可执行状态机表示、deterministic diagnostics、scenario-level feedback、structured repair decision 与待实验检验的边际作用；同时微调 [../story/paper_story.md](../story/paper_story.md) 的 S0b 标题时机和“四段方法链路 + 一段评测协议”表述。复验 `git diff --check` 与 forbidden wording contextual grep。 |
| 2026-06-11 17:22:00 | S0a 预提交一致性审计与 C/I 修复 | 启动 2 个 codex spawn sidecar 只读审计，发现并修复 Designing FSMs 层级混淆、B0-B5/EXT/E1/E2 口径混合、behavior-model checking 措辞和 G1/S1b 命名混淆；保留 S0a docs-only、不跑四例真实例子的边界。 |


## Capability-use audit

- Required skills/scripts：`ai-research-writing-skill`、`sub-agents`；S0a 实现阶段使用 4 个 codex spawn subagents 分工，分别覆盖 story/claim/terminology、outline/baseline matrix、experiment/risk/execution、README/venue/progress；正式 review 仍要求 codex spawn reviewer + `claude -p` + `codex-deepseek exec`。
- Inputs consumed：PR #9 body/assets、PR #31 body、本地导师讨论、issue #67、PR #92 body/comments、PR #94 / S1a baseline 总账与逐篇文件、PR #96 body/comments、method/eval/baselines docs，以及 9 个五绿 direct baseline 的 `paper_content.txt` / `DESC.md` / `ASSETS.md` 调研结论。
- Inputs not used and why：已归档全部 323 review JSON，但当前 S0a 不重新解释每条 review；正式样本冻结阶段再逐条核验 eligibility / provenance。S0a 不 source `.env`、不跑四例真实 agent-loop，因为它不触碰 runtime / 实验链路。
- Artifacts produced：S0a 更新后的 [paper_story.md](../story/paper_story.md)、[terminology_policy.md](../story/terminology_policy.md)、[claim_evidence_map.md](../story/claim_evidence_map.md)、[paper_outline.md](../story/paper_outline.md)、[baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)、[experiment_inventory.md](../experiment_design/experiment_inventory.md)、[reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)、[execution_plan.md](../experiment_design/execution_plan.md)、入口 README 与 venue readiness gate。
- Verification run：本地已运行 `git diff --check`、relative Markdown link check、markdown sanity、forbidden wording contextual audit；真实四例留给 S3/S4，因为 S0a 是 docs/story gate。CI / Codecov 状态待 push 后检查。
- Remaining risk：当前 S0a 仍需正式三路实现后 review；后续主实验仍需按 risk register 处理 baseline fairness、sample/reference bias、oracle weak、claim-evidence mismatch、CCF-A 标准 readiness，并在 S1b/S3 逐篇吸收 mandatory closest works，尤其 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs。
