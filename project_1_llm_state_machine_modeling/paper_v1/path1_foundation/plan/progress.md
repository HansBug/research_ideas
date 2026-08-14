# Path-1 Foundation Progress

## 当前阶段

- Branch：`paper/project1-path1-s0-direction-venue-freeze`
- 上游：PR #93 foundation；当前执行 PR #98 / S0b Direction + Venue Freeze。
- 目标：在已合入的 PR #96 / S0a story gate 基础上，冻结第一篇论文的 direction、venue route、abstract v0、CCF-A readiness checklist 与后续 S1b/S2/S3/S4/S5 的 scope 约束；继续坚持 `fcstm` / `pyfcstm` 仅作为 implementation / artifact 层内部载体，不作为论文新概念、新 DSL 或 novelty。
- 状态：S0b 为 docs / direction / venue gate，不触碰 runtime、runner、样本冻结、oracle 冻结或真实实验链路；不 source `.env`、不跑四例真实 agent-loop。过程性工程材料只保留在本 `plan/progress.md` 审计记录中，不写入 manuscript 的 Method / Contribution 主线。

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
- PR #96 / S0a 已合入 PR #93 upstream，S0b 直接基于新 story 继续推进，不回到 `first NL-to-STM`、新 DSL 或结果提升 claim。
- PR #98 / S0b 计划阶段三路 review 已完成并迭代到 READY：`claude -p` reviewer READY；codex reviewer 首轮给出 I=3 后，PR body 已修复 mandatory closest works、venue 单一真源、本地 `execution_plan.md` 依赖图同步等问题并二轮 READY；`codex-deepseek exec` reviewer 针对 I/M 问题二轮复核后 READY。
- PR #98 body 已明确 S0b 不跑四例真实 agent-loop：本轮是 docs / direction / venue gate，不触碰真实 LLM、runtime、runner、样本冻结、oracle 冻结或主实验链路。

## 本 PR 产物

| 文件 | 作用 |
|---|---|
| [../README.md](../README.md) | foundation 入口 |
| [../DIRECTION.md](../DIRECTION.md) | S0b direction / scope / contribution boundary 冻结 |
| [../abstract_v0.md](../abstract_v0.md) | pre-result / direction-freeze abstract v0 |
| [../target_venue_decision.md](../target_venue_decision.md) | S0b target venue route 决策产物 |
| [../ccf_a_readiness_checklist.md](../ccf_a_readiness_checklist.md) | CCF-A reviewer 强度派生 checklist |
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
| [../experiment_design/experiment_inventory.md](../experiment_design/experiment_inventory.md) | RQ、baseline、metrics、oracle、内部运行边界 |
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
| 2026-06-11 19:00:25 | 用户跟进修订：移除工程留痕方法化残留并中文化大纲 | 按用户要求清理非 legacy 路径中把过程记录写成 Method、RQ、贡献或结果可信度依据的表述，统一改为样本 / 运行纳入排除规则、必要实验披露或内部执行边界；`paper_outline.md` §4 保持英文 section heading，下方大纲尽量中文化。启动 codex spawn sidecar 复审，结论为 C=0/I=0，仅有不阻塞 M 级措辞建议。 |
| 2026-06-11 | PR #98 / S0b 计划阶段三路 review | `claude -p` reviewer 判断 READY；codex reviewer 首轮指出 I=3：mandatory closest works 未显式验收、venue/readiness 单一真源未冻结、本地 `execution_plan.md` 依赖图同步未进入验收；修复 PR body 后 codex 二轮 READY；`codex-deepseek exec` reviewer 对 I/M 问题二轮复核后 READY。 |
| 2026-06-11 | PR #98 / S0b progress + checklist dry audit | 本 worker 仅更新 [progress.md](./progress.md)，记录当前阶段、计划 review 闭环和 capability-use audit；不修改 manuscript 方法/贡献，不 source `.env`，不跑四例 agent-loop。 |
| 2026-06-11 | PR #98 / S0b 文档实现与主 session 合流检查 | 新增 [../DIRECTION.md](../DIRECTION.md)、[../abstract_v0.md](../abstract_v0.md)、[../target_venue_decision.md](../target_venue_decision.md)、[../ccf_a_readiness_checklist.md](../ccf_a_readiness_checklist.md)，并同步入口 README、story README、execution plan 依赖图和本 progress；主 session 运行 Markdown 相对链接检查、forbidden wording 上下文 grep、mandatory closest works grep、`git diff --check` 与 pytest smoke：`432 passed, 6 warnings in 88.75s`。 |


## Capability-use audit

- Required skills/scripts：本 PR #98 / S0b 使用 `$ai-research-writing-skill` 的 story / claim-evidence / reviewer gate 约束 direction 与 venue 冻结；使用 `$sub-agents` 工作流要求完成计划阶段三路 review；计划与 review 记录涉及 codex spawn reviewer、`claude -p` reviewer、`codex-deepseek exec` reviewer。当前 worker D 按用户约束禁止启动 sub-subagent，仅直接编辑本 `progress.md`。
- Inputs consumed：PR #93 upstream body / 依赖图口径、PR #96 / S0a 已合入 story gate、PR #98 body 与计划阶段 review comment、S1a baseline 总账与 mandatory closest works 约束、导师关于淡化 `fcstm` / 不引入新 DSL 名头的口径，以及本地 [../experiment_design/execution_plan.md](../experiment_design/execution_plan.md)、[../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 的现有分工。
- Inputs not used and why：本 worker 不读取或执行 `.env`，不调用真实 LLM，不跑四例真实 agent-loop；S0b 是 docs / direction / venue gate，不触碰 runtime、runner、样本冻结、oracle 冻结或主实验链路。四例真实运行留给后续 S3/S4 或 upstream 明确要求的关键实验节点。
- Artifacts produced / updated：当前 worker 仅更新 [progress.md](./progress.md)，记录 PR #98 / S0b 当前阶段、计划阶段三路 review 闭环、S0b 不跑四例的依据，以及过程性工程材料只能作为 plan/progress 审计记录、不得进入 manuscript Method / Contribution 主线的边界。
- Verification run：主 session 已运行 `git diff --check`、8 个 S0b 相关 Markdown 文件相对链接存在性检查、forbidden wording 上下文 grep、mandatory closest works grep，以及 `PYTHONPATH=project_1_llm_state_machine_modeling pytest -q project_1_llm_state_machine_modeling/tests project_1_llm_state_machine_modeling/method/tests`；结果为 `432 passed, 6 warnings in 88.75s`。本轮不 source `.env`、不跑四例真实 agent-loop。
- Remaining risk：实现阶段已把 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 写入 S0b 产物并同步本地 `execution_plan.md` 依赖图；剩余风险转为后续 S1b/S2/S3/S5 是否严格消费 S0b 冻结口径，尤其是 related-work wording、sample/oracle scope、external approximate baseline 与 manuscript result claim 不得回潮。
