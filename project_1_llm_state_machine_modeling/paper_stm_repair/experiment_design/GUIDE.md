# experiment_design/GUIDE.md — 实验设计维护规范

## 1. 总原则

实验设计必须先于真实修正结果冻结。任何新增 scope、eligibility、protocol 或 metric 都必须标明状态：`草案`、`评价门 v0`、`正式协议候选` 或 `已冻结`。当前除 Better STM 五条件外，不得把职责 README 写成已冻结协议。

## 2. 子路径维护规则

| 子路径 | 可以写什么 | 禁止写什么 |
|---|---|---|
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

## 4. 质量门

1. 只有满足 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 五条件，才可把 `STM_k` 计为相对 `STM_0` 的 Better STM。
2. 任一条件为 `unknown`、`not_applicable` 或 `fail`，都不能支持 Better STM 主张。
3. converter / normalization 收益必须与 repair-loop 收益分开记录。

## 5. 更新流程

1. 新增协议前先在对应子路径 README 中说明职责与状态。
2. 协议从草案升级为冻结前，应补可复验字段、输入输出、failure handling、run record 要求和验收命令。
3. 每次移动或新增文件后同步更新 [README.md](./README.md) 与 [SUMMARY.md](./SUMMARY.md)。
4. 不在本目录记录动态 PR 进度；PR comment 中的长期结论应抽象为稳定规则后再落盘。
