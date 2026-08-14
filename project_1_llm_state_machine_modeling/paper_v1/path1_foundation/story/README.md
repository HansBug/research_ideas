# story/：论文主线、术语与 claim 控制

本目录维护 Path-1 第一篇论文的 story 真源。S0a 后，它回答四个问题：这篇论文到底讲什么、哪些 claim 可以写、哪些术语必须弱化、哪些 claim 必须等实验完成后再写。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | S0a 后的 thesis、task boundary、gap、technical challenge、method insight、contributions、baseline-aware positioning 与 claims-to-avoid。 |
| [terminology_policy.md](./terminology_policy.md) | `fcstm` / `pyfcstm` 弱化策略、preferred wording、forbidden wording、允许出现位置、grep / 自检策略。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每条潜在论文 claim 的 status、baseline_coverage、marginal_claim、forbidden_softened_claims、required evidence 与 safe wording。 |
| [paper_outline.md](./paper_outline.md) | 在导师定调和九个 direct baseline 反证压力下，固定 Introduction / Related Work / Method / Experiment / Threats 逻辑、RQ 和证据门。 |
| [venue_readiness_gate.md](./venue_readiness_gate.md) | issue #67 的投稿 readiness 背景与 CCF-A 强度门禁；S0a 不冻结最终 venue，后续 S0b 再产出 [../target_venue_decision.md](../target_venue_decision.md)。 |

S0b 新产物位于上级目录，是本目录 story 真源的下游合同，而不是新的 story 真源：

| S0b 文件 | 与 story/ 的关系 |
|---|---|
| [../DIRECTION.md](../DIRECTION.md) | 消费 S0a story，冻结 direction / scope / 贡献边界，并约束后续 S1b/S2/S3/S4/S5。 |
| [../abstract_v0.md](../abstract_v0.md) | 把 S0a + S0b 口径压缩成无结果过度承诺的摘要草案；若摘要需要新 claim，必须先回到 [claim_evidence_map.md](./claim_evidence_map.md)。 |
| [../target_venue_decision.md](../target_venue_decision.md) | 在 [venue_readiness_gate.md](./venue_readiness_gate.md) 背景上冻结 fit-first 投稿路线；它是 venue 决策真源。 |
| [../ccf_a_readiness_checklist.md](../ccf_a_readiness_checklist.md) | 按 CCF-A 强度检查 S0a/S0b 后的 novelty、baseline、oracle、claim-evidence、artifact 与 threats。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认当前主线是 formal-executable representation -> deterministic diagnostics -> scenario-level simulation feedback -> structured repair decision -> baseline-aware evaluation。
2. 再读 [terminology_policy.md](./terminology_policy.md)，确认 title / abstract / contribution 中不得主打 `fcstm` / `pyfcstm` / `new DSL`。
3. 写任何 abstract / introduction / contribution 句子前，必须查 [claim_evidence_map.md](./claim_evidence_map.md)。
4. 再读 [paper_outline.md](./paper_outline.md)，确认 Related Work 第一节必须正面处理 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs。
5. 再读 [../DIRECTION.md](../DIRECTION.md)、[../abstract_v0.md](../abstract_v0.md)、[../target_venue_decision.md](../target_venue_decision.md)、[../ccf_a_readiness_checklist.md](../ccf_a_readiness_checklist.md)，确认 S0b 已把 story 转成 direction / venue / readiness contract。
6. 最后读 [venue_readiness_gate.md](./venue_readiness_gate.md)，只把它作为 S0b venue decision 的背景，不把它理解为最终投稿期刊真源。

## 与后续阶段的依赖

- **S0a story 真源**：本目录文件先定义 thesis、terminology、claim boundary 和 closest-work carve-out。
- **S0b direction / venue 决策**：上级 S0b 文件只能在 S0a 真源上冻结 direction、scope、abstract-v0、target venue 与 CCF-A readiness；不得把 S0b 写成实验结果、方法贡献或运行记录贡献。
- **S1b**：可与 S0b 前后衔接准备 related-work / baseline 材料，但所有最终 wording 必须服从 S0b 的 direction / venue 口径。
- **S2/S3/S4**：S2 sample / oracle 必须等待 S0b scope；S3/S4 经由 S2 继承该 scope。
- **S5**：manuscript v1 必须同时消费 S0a story、S0b direction / venue、S1b closest-work positioning、S2 sample / oracle 和 S4 实验结果。

## S0a 硬约束

- 不写 `first NL-to-STM`、`first feedback loop`、`prior work only draws diagrams` 或其柔化版本。
- 不把 `fcstm` / `pyfcstm`、过程性工程材料、LangGraph、Codex、Claude、prompt template 写成 contribution。
- 不把 E1/E2 写成 Hybrid 方法贡献；只能作为 orchestration condition / RQ dimension。
- 不把 parse / semantic / inspect / simulation 写成 complete formal verification。
- 不把 private GT、missing code、missing prompt 写成 prior work weakness。
- 不把 PR #9 historical selection / expansion / reference draft 写成当前 paper result。

## 边界

- `story/` 不保存实验数据和运行结果。
- 如果后续实验结果与当前 thesis 冲突，应先改本目录，再改 manuscript。
- 如果 S1b/S3 对 closest baseline 的可复现性判断改变，应同步更新 [claim_evidence_map.md](./claim_evidence_map.md)、[paper_outline.md](./paper_outline.md) 和 [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)。
