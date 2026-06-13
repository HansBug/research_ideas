# Statistical Usage Testing Based on UML

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2003 |
| venue | SCI 2003 / workshop paper |
| URL / DOI | https://www.inf.uni-hamburg.de/en/inst/ab/swk/research/publications/pdf/2003-sci2003-paper.pdf |
| strict seed 结论 | `SS-B` |
| artifact 可用性 | `SA-3` |
| 当前角色 | manual-refinement conditional strict seed / paper-only main-candidate boundary |

## 一句话总结

UML textual/tabular use case + domain class model 经 template-guided refinement 自动转换为 UML state diagram / state machine，再转 usage graph / Markov usage model，用于 statistical usage testing。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 文本型 / 表格型 UML use case；论文说明标准 use case 主要是 textual description，示例为停车票售卖机用例。 |
| P2_T0_STM_FAMILY | 输出包含 UML state chart / state machine，规则包括 use-case step -> state、user-caused event -> transition、loop -> recurring transition，并有 guard / entry action。 |
| P3_GENERATION_RELATION | 流程图与步骤明确：textual use case description -> structured use case -> state transition/state diagram -> usage graph。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；论文内有示例 use case、refined text、statechart/usage graph；XML prototype 声明但未公开包。 |

## 风险与 caveat

依赖人工/工具辅助 refinement 和 domain class model，不是 raw NL 直接生成；SA-3 不计自动可复验主 seed。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
