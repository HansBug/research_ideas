# Path-1 Foundation Progress

## 当前阶段

- Branch：`paper/project1-path1-foundation`
- 目标：建立第一篇 Path-1 paper foundation，并开 PR 供后续 paper 工作承接。
- 状态：foundation 初稿已提交至 PR #93；第一轮 C/I 已完成文档修复；二轮三路本地学术 review 均 READY，当前 PR body / foundation 文档已达到 body-ready。

## 已完成

- 使用 `$ai-research-writing-skill` / `$research-planning` / `$sub-agents` 约束任务。
- 读取并吸收导师讨论、PR #9、PR #31、PR #22、issue #67、baseline / method / eval 当前资料。
- 建立 `path1_foundation/` 工作区。
- 压缩迁移 PR #9 的 selection / expansion / ref-STM 资产，不将其写成 current result。

## 本 PR 产物

| 文件 | 作用 |
|---|---|
| [../README.md](../README.md) | foundation 入口 |
| [../paper_story.md](../paper_story.md) | thesis、gap、contributions、claims |
| [../project_inventory.md](../project_inventory.md) | repo evidence inventory |
| [../sample_assets.md](../sample_assets.md) | PR #9 样本/扩充/ref资产迁移 |
| [../experiment_inventory.md](../experiment_inventory.md) | RQ、baseline、metrics、oracle、run record |
| [../baseline_and_related_work_matrix.md](../baseline_and_related_work_matrix.md) | closest prior works 与实验对齐计划 |
| [../claim_evidence_map.md](../claim_evidence_map.md) | claim gate |
| [../reviewer_risk_register.md](../reviewer_risk_register.md) | C/I/M 风险台账 |
| [../execution_plan.md](../execution_plan.md) | gate-driven 执行计划 |
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

## Capability-use audit

- Required skills/scripts：`ai-research-writing-skill`、`research-planning`、`sub-agents`。
- Inputs consumed：PR #9 body/assets、PR #31 body、本地导师讨论、issue #67、method/eval/baselines docs。
- Inputs not used and why：未读取全部 323 review JSON，当前 foundation 只需压缩资产索引；正式样本冻结阶段再全量核验。
- Artifacts produced：本目录所有 foundation Markdown。
- Verification run：foundation markdown sanity、相对 Markdown 链接检查已通过；PR body 已创建并接受第一轮三路 review。
- Remaining risk：当前 foundation PR 无 C/I 阻塞；后续主实验仍需按 risk register 处理 baseline fairness、sample/reference bias、oracle weak 与 claim-evidence mismatch。
