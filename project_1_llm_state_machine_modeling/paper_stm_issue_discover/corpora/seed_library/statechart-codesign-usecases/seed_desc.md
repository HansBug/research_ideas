# From Use Cases to System Implementation: Statechart Based Co-design

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2003 |
| venue | MEMOCODE |
| URL / DOI | https://doi.org/10.1109/MEMCOD.2003.1210083 |
| strict seed 结论 | `SS-B` |
| artifact 可用性 | `SA-3` |
| 当前角色 | embedded co-design paper-only boundary |

## 一句话总结

方法从 use cases 捕获系统功能，然后可直接把每个 use case 翻译为 statechart 或经 sequence diagram 再合成为 statechart，用于硬软协同实现。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 输入为 use cases / use case diagram；功能以 informal way 捕获。 |
| P2_T0_STM_FAMILY | 输出 statechart / set of sub-statecharts / top-level statechart model。 |
| P3_GENERATION_RELATION | 论文明确给出两种 route：directly translate each use case into a statechart；或 use case -> sequence diagram -> statechart。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；给出 image acquisition system case 和 figures；无公开 artifact。 |

## 风险与 caveat

偏 co-design/implementation，转换可能人工执行；sequence-diagram route 需排除，direct route 可作 weak strict evidence。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
