# Integrating Graphical and Natural Language Specifications to Support Analysis and Testing

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2016 |
| venue | conference / industrial MBT paper |
| URL / DOI | https://bura.brunel.ac.uk/bitstream/2438/15650/1/Fulltext.pdf |
| strict seed 结论 | `NN-D` |
| artifact 可用性 | `SA-3` |
| 当前角色 | boundary negative / NL-GN integration related work |

## 一句话总结

工业规格中将 statechart/block diagram 等 graphical notation 与 NL requirements 集成，用 GN 生成章节结构和测试模型；实际方向是 GN/statechart + NL -> structured spec/test，不是 NL -> STM。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 处理 NL requirements / atomic statements。 |
| P2_T0_STM_FAMILY | statechart/FSM-like GN 是已有或人工创建的输入；不是输出。 |
| P3_GENERATION_RELATION | 核心转换为 GN -> LDG/chapter structure/test model；未来才提 NL 自动派生结构。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；有 belt-warner statechart、LDG、industrial stats；无公开机器可读 artifact。 |

## 风险与 caveat

用于证明 NL 与 statechart 共现不等于 strict NL->STM seed。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
