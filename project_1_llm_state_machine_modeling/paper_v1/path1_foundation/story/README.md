# story/：论文主线、术语与 claim 控制

本目录维护 Path-1 第一篇论文的 story 真源。S0a 后，它回答四个问题：这篇论文到底讲什么、哪些 claim 可以写、哪些术语必须弱化、哪些 claim 必须等实验完成后再写。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | S0a 后的 thesis、task boundary、gap、technical challenge、method insight、contributions、baseline-aware positioning 与 claims-to-avoid。 |
| [terminology_policy.md](./terminology_policy.md) | `fcstm` / `pyfcstm` 弱化策略、preferred wording、forbidden wording、允许出现位置、grep / 自检策略。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每条潜在论文 claim 的 status、baseline_coverage、marginal_claim、forbidden_softened_claims、required evidence 与 safe wording。 |
| [paper_outline.md](./paper_outline.md) | 在导师定调和九个 direct baseline 反证压力下，固定 Introduction / Related Work / Method / Experiment / Threats 逻辑、RQ 和证据门。 |
| [venue_readiness_gate.md](./venue_readiness_gate.md) | issue #67 的投稿 readiness 背景与 CCF-A 强度门禁；S0a 不冻结最终 venue，后续 S0b 再产出 `target_venue_decision.md`。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认当前主线是 formal-executable representation -> deterministic diagnostics -> scenario-level simulation feedback -> structured repair decision -> baseline-aware evaluation。
2. 再读 [terminology_policy.md](./terminology_policy.md)，确认 title / abstract / contribution 中不得主打 `fcstm` / `pyfcstm` / `new DSL`。
3. 写任何 abstract / introduction / contribution 句子前，必须查 [claim_evidence_map.md](./claim_evidence_map.md)。
4. 再读 [paper_outline.md](./paper_outline.md)，确认 Related Work 第一节必须正面处理 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs。
5. 最后读 [venue_readiness_gate.md](./venue_readiness_gate.md)，只把它作为 S0b venue decision 的输入，不把它理解为 S0a 已经决定最终投稿期刊。

## S0a 硬约束

- 不写 `first NL-to-STM`、`first feedback loop`、`prior work only draws diagrams` 或其柔化版本。
- 不把 `fcstm` / `pyfcstm`、run record、LangGraph、Codex、Claude、prompt template 写成 contribution。
- 不把 E1/E2 写成 Hybrid 方法贡献；只能作为 orchestration condition / RQ dimension。
- 不把 parse / semantic / inspect / simulation 写成 complete formal verification。
- 不把 private GT、missing code、missing prompt 写成 prior work weakness。
- 不把 PR #9 historical selection / expansion / reference draft 写成当前 paper result。

## 边界

- `story/` 不保存实验数据和运行结果。
- 如果后续实验结果与当前 thesis 冲突，应先改本目录，再改 manuscript。
- 如果 S1b/S3 对 closest baseline 的可复现性判断改变，应同步更新 [claim_evidence_map.md](./claim_evidence_map.md)、[paper_outline.md](./paper_outline.md) 和 [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)。
