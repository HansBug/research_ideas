# R5 交接入口

本目录保存 R5 修正前准备度审计向后续阶段传递的稳定证据。这里不是 PR 动态流程台账，只记录可复用的研究交接材料。

## 文件职责

| 文件 | 作用 | 主要读者 |
|---|---|---|
| [r5_to_r6_repair_inputs.json](./r5_to_r6_repair_inputs.json) | R5 认为可进入 R6 修正循环候选池的机器记录 | R6 loop 实现与样本选择 |
| [r5_to_r7_seed_eligibility.json](./r5_to_r7_seed_eligibility.json) | 面向正式实验资格冻结的 converted / partial 样本证据 | R7 protocol / eligibility freeze |
| [r5_to_r8_negative_evidence.json](./r5_to_r8_negative_evidence.json) | blocked、not_applicable、needs_generation 等负证据 | R8 negative evidence / follow-up |
| [llms_emp_main_seed_handoff.md](./llms_emp_main_seed_handoff.md) | 基于 R5 全量摸排收敛出的 `llms-emp-stm-subset` 主实验优先路线 | R6/R7 规划与论文 story |

## 使用纪律

1. R5 不执行 repair loop，不生成 `STM_k`，不产生 Better STM 主结果。
2. `r5_to_r6_repair_inputs.json` 只是候选输入池，不等同于最终实验样本。
3. `partial` 不表示不可用，但必须在 R7 中按 loss / attribution 分层。
4. `llms-emp-stm-subset` 的 60 条必须按 10 个唯一 NL cluster 解读；不能把它们当成 60 个独立需求。
5. conversion / normalization / `.fcstm` lowering 只可作为前修正准备度证据，不能计入 repair gain。
