# Towards Automatic Model Completion: from Requirements to SysML State Machines

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2022 |
| venue | arXiv preprint |
| URL / DOI | https://arxiv.org/abs/2210.03388 / https://doi.org/10.48550/arXiv.2210.03388 |
| strict seed 结论 | `NN-D` |
| artifact 可用性 | `SA-3` |
| R1.7 priority | `P2` |
| 当前角色 | model completion / repair-only boundary |

## 一句话总结

论文从 partial SysML model 与 Given-When-Then requirements 出发，补全 SysML state machine transitions / fragments；它不是从 NL requirements 初始生成完整 `STM_0`，而是典型 partial-model completion。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 输入包含 GWT requirements。 |
| P2_T0_STM_FAMILY | 输出包含 SysML state machine fragments / completed SMD。 |
| P3_GENERATION_RELATION | 不满足 strict initial-generation：摘要和方法反复说明起点是 partial SysML model / partial SMD，并用 requirements 完成模型。 |
| P4_EVIDENCE_POINTER | 本地 `paper_content.txt`：摘要提到 partial SysML model；§III 提到 partial State Machine Diagram；Fig. 1/2 展示 incomplete/complete SMD。 |

## 排除理由

触发 `X_REPAIR_ONLY`：输入不是只有 NL，且任务目标是补全已有 partial model；可保留为修正/补全 related work，但不能作为 R1.7 strict literature seed 或 PR-R2 主 seed。

## R1.7 使用建议

- 从 manual download queue 的 pending 中移出，记录为 `downloaded / excluded`。
- 放入 exclusion ledger，作为后续 reviewer 防止把 model completion 当初始 seed 的 sentinel。
