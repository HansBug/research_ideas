# experiment_design/GUIDE.md — 实验设计维护规范

## 1. 总原则

实验设计必须先于真实修正结果冻结。任何新增 scope、eligibility、protocol 或 metric 都必须标明状态：`草案`、`评价门 v0`、`正式协议候选` 或 `已冻结`。当前已冻结的上游合同包括 [evaluation_logic.md](./evaluation_logic.md) 的 R5.7.1 评价逻辑链与 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 的 Better STM 五条件；除此之外，不得把职责 README 写成已冻结协议。

## 2. 子路径维护规则

| 子路径 | 可以写什么 | 禁止写什么 |
|---|---|---|
| [evaluation_logic.md](./evaluation_logic.md) | R5.7.1 评价逻辑链、claim 类型、分母纪律、A 层、归因边界、指标位置、失败报告纪律、下游接口。 | Better STM 判定细则、最终指标阈值、真实 repair 效果、`STM_k` 结果。 |
| [scope/](./scope/) | RQ 版本、样本范围、T0/T0.5/T1 边界、story / scope 分工。 | 论文叙事正文、已跑结果、最终 claim。 |
| [quality_model/](./quality_model/) | Better STM 定义、质量维度、判定反例、归因边界。 | 因结果好坏临时改五条件。 |
| [eligibility/](./eligibility/) | run / sample / conversion / provider failure 纳入排除草案。 | 未验证就宣称 eligibility 已冻结。 |
| [protocols/](./protocols/) | 修正循环、对照、人工裁决、回滚和审计协议草案。 | 真实运行流水账或结果统计。 |
| [metrics/](./metrics/) | 指标字段、统计表骨架、报告口径草案。 | 看结果后倒推阈值或删改不利指标。 |

## 3. story vs scope 分工

[../story/](../story/) 是论文叙事与 claim gate 真源；[scope/](./scope/) 是实验对象、RQ 和边界真源。若二者冲突：

1. claim / wording / paper outline 以 story 为准。
2. sample envelope / RQ eligibility / experiment boundary 以 experiment_design 为准。
3. 若导师或 PR body 更新导致边界变化，必须同时检查 story 和 scope，但不要把一边复制成另一边。
4. R5.6 之后，任何 repair target taxonomy、eligibility 或 protocol 草案都必须先对照 [../story/model_scope.md](../story/model_scope.md) 与 [scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md)：不得把 T0.5/T1、timed/hybrid/arbitrary UML/protocol FSM 或 conversion/normalization/lowering 误写成 main repair claim。
5. R5.7.1 之后，任何涉及方法有效性、评价分母、客观指标或 failure reporting 的写法，都必须先对照 [evaluation_logic.md](./evaluation_logic.md)：不得把 readiness claim、protocol claim 或 limitation claim 升级为 repair effectiveness claim。

## 4. 质量门

1. 只有同时满足 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 的核心判据与五条最低必要条件，才可把 `STM_k` 计为相对 `STM_0` 的 Better STM；parse ok、executable 或 `.fcstm` lowering 本身都不是 Better STM 证据。
2. 任一条件为 `unknown`、`not_applicable` 或 `fail`，都不能支持 Better STM 主张。
3. converter / normalization 收益必须与 repair-loop 收益分开记录。

## 5. 评价逻辑链维护纪律

后续新增或修改 R5.7 / R6 / R7 / R8 评价相关文件时，必须为每条核心 claim 明确以下字段或等价说明：

| 字段 | 最低要求 |
|---|---|
| `claim_type` | 至少区分 `task_scope`、`readiness`、`protocol_evaluation`、`repair_effectiveness`、`limitation_negative_evidence`。 |
| `evidence_type` | 说明来自 machine artifact、report、run record、change ledger、semantic adjudication、human rubric 还是 PR 决策。 |
| `denominator` | 明确是 pre-registered pool、scope pool、evaluation-eligible pool，还是 success / failure / unknown 分母。 |
| `attribution_boundary` | 说明该证据属于 raw -> canonical readiness，还是 canonical `STM_0` -> `STM_k` repair-loop gain。 |
| `forbidden_extrapolation` | 明确不能由该证据推出什么，例如不能由 parse ok 推出 Better STM。 |
| `failure_handling` | 说明 A-fail、partial、unknown、out-of-scope、rollback、不收敛如何入 ledger。 |

禁止事项：

1. 不得用 parse ok、inspect ok、conversion success、diagnostics fewer、F1 更高、场景通过率更高、文本相似度更高或低 token cost 单独支持 Better STM。
2. 不得把 `T0 headline main = 8 clusters / 48 pairs` 写成最终 eligible / success denominator。
3. 不得把 `partial` 静默丢弃或直接等同失败；它是带 caveat 的可评价候选，需后续 A 层与语义裁决。
4. 不得在真实 repair loop 运行前报告 repair effectiveness、Better STM 成功率或强泛化主张。

## 6. 更新流程

1. 新增协议前先在对应子路径 README 中说明职责与状态。
2. 协议从草案升级为冻结前，应补可复验字段、输入输出、failure handling、run record 要求和验收命令。
3. 每次移动或新增文件后同步更新 [README.md](./README.md) 与 [SUMMARY.md](./SUMMARY.md)。
4. 不在本目录记录动态 PR 进度；PR comment 中的长期结论应抽象为稳定规则后再落盘。
