# Path-1 Foundation Progress

## 当前阶段

- Branch：`paper/project1-path1-foundation`
- 目标：建立第一篇 Path-1 paper foundation，并开 PR 供后续 paper 工作承接。
- 状态：PR #93 已进入结构化 foundation 收口阶段；PR #9 详细样本筛选 / NL 扩充 / parquet / reference draft 资产已归档，当前正在进行分层 README、PR body 与最终复核。

## 已完成

- 使用 `$ai-research-writing-skill` / `$research-planning` / `$sub-agents` 约束任务。
- 读取并吸收导师讨论、PR #9、PR #31、PR #22、issue #67、baseline / method / eval 当前资料。
- 建立 `path1_foundation/` 工作区。
- 归档 PR #9 的 selection / expansion / parquet / ref-STM 原始资产，不将其写成 current result。
- 将 `path1_foundation/` 分层为 `story/`、`evidence/`、`dataset_selection/`、`experiment_design/` 与 `plan/`。

## 本 PR 产物

| 文件 | 作用 |
|---|---|
| [../README.md](../README.md) | foundation 入口 |
| [../story/README.md](../story/README.md) | story 分层入口 |
| [../story/paper_story.md](../story/paper_story.md) | thesis、gap、contributions、claims |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | claim gate |
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
| 2026-06-10 | PR #9 详细资产归档 | 已归档 387 个历史资产文件：323 个 selection review、30 个 expansion JSON、2 个 parquet、2 个 reference draft 目录，并生成 manifest / summary |
| 2026-06-10 | foundation 分层 README 收口 | 新增 story/evidence/dataset_selection/experiment_design/plan 及 legacy asset 子路径中文 README，修正 current overlay 旧路径 |

## Capability-use audit

- Required skills/scripts：`ai-research-writing-skill`、`research-planning`、`sub-agents`。
- Inputs consumed：PR #9 body/assets、PR #31 body、本地导师讨论、issue #67、method/eval/baselines docs。
- Inputs not used and why：已归档全部 323 review JSON，但当前 foundation 不重新解释每条 review；正式样本冻结阶段再逐条核验 eligibility / provenance。
- Artifacts produced：分层 foundation Markdown、PR #9 legacy assets、asset manifest / summary。
- Verification run：foundation markdown sanity、相对 Markdown 链接检查已通过；PR body 已创建并接受第一轮三路 review。
- Remaining risk：当前 foundation PR 无 C/I 阻塞；后续主实验仍需按 risk register 处理 baseline fairness、sample/reference bias、oracle weak 与 claim-evidence mismatch。
