# An Approach to Building Object Models with UML in Embedded Systems

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2004 |
| venue | Journal of Computing and Information Technology |
| URL / DOI | https://hrcak.srce.hr/file/69340 |
| strict seed 结论 | `SS-B` |
| artifact 可用性 | `SA-3` |
| 当前角色 | embedded use-case-to-statechart paper-only related seed |

## 一句话总结

嵌入式系统对象建模方法，首先把 use case 转换为 statechart，再从 statechart 识别对象；示例含 elevator request。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 输入为 use case textual description，use case 由 name/actor/pre/postconditions/normal steps/exceptional steps 构成。 |
| P2_T0_STM_FAMILY | 输出为 UML statechart/extended statechart，states/events/transitions/guards 描述 controlled parts。 |
| P3_GENERATION_RELATION | 论文明确“converting the use case into a statechart”以及“derive the statechart”后再识别对象。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；elevator example 与 figures；无公开 artifact。 |

## 风险与 caveat

目标是 object model，不是 seed dataset；转换步骤偏人工/方法论。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
