# NLP-Based Requirements Formalization for Automatic Test Case Generation

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2021 |
| venue | CS&P 2021 / CEUR Workshop Proceedings |
| URL / DOI | https://ceur-ws.org/Vol-2951/paper15.pdf |
| strict seed 结论 | `SS-B` |
| artifact 可用性 | `SA-3` |
| R1.7 priority | `P1` |
| 当前角色 | e-mobility NL requirements -> UML state machine 的 paper-only strict literature evidence / test-generation boundary |

## 一句话总结

论文提出 ReForm 半自动 NLP 流程，把自然语言功能需求抽取为 IRDL requirement model / sequence model，再用 ModGen 合成 UML state machine，最后生成测试用例；案例来自 e-mobility charging approval system。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 输入为 functional requirements / text documents，论文明确目标是从 natural language requirements 创建 requirement models。 |
| P2_T0_STM_FAMILY | toolchain 图和 §3.5/§4 明确生成 UML state machine；Fig. 4 给出 charging approval 的 UML state machine。 |
| P3_GENERATION_RELATION | §3.4 先从文本需求形成 IRDL relations / sequence diagram；§3.5 再把 sequence elements rule-based 转换为 UML state machine；§4 报告 14 个 requirement models 合成为 specification model。 |
| P4_EVIDENCE_POINTER | 本地 `paper_content.txt` lines around Fig. 1、§3.4、§3.5、§4；本地 PDF 已保存。 |

## 风险与 caveat

- 不是 raw NL 直接到 STM：存在 IRDL / sequence model intermediate，且用户需要 validate intermediate model。
- 目标是 automatic test case generation，state machine 是中间 specification model。
- 未发现公开 ReForm / ModGen code、requirement dataset 或生成 UML state machine 的机器可读输出，因此为 `SA-3`，不得计入 R1.7 主 / 条件主 seed 成功门。

## R1.7 使用建议

- 可作为工业 e-mobility 相关的 strong paper-only seed evidence，说明传统 NLP/MBT 中确有 `NL requirements -> UML state machine` 链路。
- 若 PR-R2 需要可运行 seed，不能直接使用本文；只能人工重建小例子或另找/联系 artifact，并单独登记 provenance。
