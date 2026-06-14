# Specification-based Verification of Embedded Systems by Automated Test Case Generation

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2008 |
| venue | DIPES / IFIP |
| URL / DOI | https://dl.ifip.org/db/conf/ifip10-3/dipes2008/KirchsteigerTSWP08.pdf |
| strict seed 结论 | `NN-D` |
| artifact 可用性 | `SA-3` |
| 当前角色 | seed-adjacent related work / testbench boundary |

## 一句话总结

半形式化文本 use case specification 自动生成 SystemC verification testbench 与测试用例；内部 verification state machine 是测试执行机制，不是目标系统 STM seed。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 半形式化 textual use cases，包含 actor、pre/postcondition、trigger、main success scenario、extensions。 |
| P2_T0_STM_FAMILY | 有 verification state machine，但属于 SystemC testbench 执行线程；不是目标系统 FSM/HSM/EFSM/statechart。 |
| P3_GENERATION_RELATION | XML use case spec -> parser/semantic analyzer -> SystemC testbench/test cases，方向是 test generation。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；RFID case 报告 53 scenarios、131 SystemC test cases、coverage 与 faults。 |

## 风险与 caveat

RFID use cases还由 controller state diagram 派生，存在方向反转风险；不计 strict seed。

## R1.7 使用建议

- 若为 `SS-A/SS-B + SA-3`：可作为 strict seed 文献证据、manual reconstruction 线索或 related work，但不得计入 R1.7 主 / 条件主 seed 成功门。
- 若为 `NN-D`：保留为边界负例，防止把 testbench / GN-driven / co-exist-only 工作误收为 strict seed。
