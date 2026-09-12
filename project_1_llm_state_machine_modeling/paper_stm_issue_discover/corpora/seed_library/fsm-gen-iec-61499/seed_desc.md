# LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation

## R1.6 strict seed 全文核验结论

| 字段 | 结论 |
|---|---|
| bibliographic_id | IEEE INDIN 2025，IEEE document `11279575` |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-4` |
| 是否计入主 seed | 不计入。任务贴近控制系统，但核心工具、案例数据、状态机输出和代码 artifact 未公开。 |

## P1/P2/P3/P4 核验

| 谓词 | 判定 | 证据 |
|---|---|---|
| `P1_NL_INPUT` | 通过 | 论文和本地 DESC 描述输入为自然语言控制需求和 I/O 接口规范。 |
| `P2_T0_STM_FAMILY` | 通过 / extended | 输出包含 FSM 与 IEC 61499 ECC / function block code；当前按控制软件 FSM/ECC extended seed 处理。 |
| `P3_GENERATION_RELATION` | 通过 | fbAssistant 使用 LLM 生成初始状态机，并通过仿真 / 用户反馈迭代 refined FSM。 |
| `P4_EVIDENCE_POINTER` | 论文级通过 / artifact 不足 | 本地 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 可核全文；但无公开代码、数据、输出包。 |

## SS / SA 解释

- `SS-B`：自然语言控制需求到 FSM 的生成链路清楚，且控制系统相关性强；但流程包含 I/O 接口、RAG、用户/工具迭代精化与 IEC 61499 代码生成，initial `NL -> STM_0` 是否可干净隔离仍需人工裁决。
- `SA-4`：原文未提供公开代码仓库或数据集下载；只能作为 related work / task motivation / private-tool boundary。

## R2 使用建议

不计四例下限。可作为“工业控制 + LLM + FSM + simulation/feedback”的强 related work，帮助论证本论文转向 `NL + raw/source STM_0 -> source-level issue discovery / repair / closure` 的合理性，但不应声称可以复现其 seed。
