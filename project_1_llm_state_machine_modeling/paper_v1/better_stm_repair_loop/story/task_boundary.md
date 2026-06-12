# Task Boundary：`<NL, STM_0> -> STM_k`

## 1. 任务定义

R0 冻结的第一篇任务是：给定自然语言需求 `NL` 和一个初始状态机 `STM_0`，系统在无人化修正运行中使用结构化反馈生成候选修复，并输出相对 `STM_0` 更优或明确失败的 `STM_k` / run outcome。

```text
Input:  <NL, STM_0>
Loop:   diagnostics / feedback / simulation -> repair -> regression checks
Output: STM_k or rejected / rollback / non-converged outcome
```

## 2. 方法内范围

| 范围 | 说明 |
|---|---|
| diagnostics | 解析、语义、设计、轻量形式化 / 静态检查和后续 R4 冻结的诊断集合。 |
| scenario / simulation feedback | 基于需求相关场景执行状态机制品，形成 pass/fail、trace mismatch 或行为证据。 |
| repair candidate generation | LLM 或修正组件基于结构化反馈提出候选修改。 |
| accept / reject / rollback | 候选模型必须经过回归和评价门；失败时拒绝或回滚，不由人工临时干预放行。 |
| non-convergence handling | 超时、振荡或语义退化必须记录为失败 / 局限 / 不收敛。 |

## 3. 方法外范围

| 外部环节 | R0 口径 |
|---|---|
| `NL -> STM_0` | 只作为 seed construction / baseline source / related work；不作为主贡献。 |
| 多格式转换器 | R3 才定义最小转换合同；R0 只说明需要转换归因。 |
| 样本选择 | R2 才冻结 seed registry 和四例样本；R0 不抽样。 |
| 评价量表终稿 | R4/R6 冻结；R0 只定义原则。 |
| 论文正文 | R7 才写 manuscript skeleton；R0 只写 outline。 |

## 4. 人类角色

本任务中的“无人化”只限定 repair run 内部：在冻结 `NL`、`STM_0`、检查器、场景、停止条件和接受规则后，修正循环不依赖人在中途逐轮决策。

允许人类参与：

1. benchmark 和 seed 的构造；
2. reference model、rubric 或 adjudication 的准备；
3. 运行结果的最终审计；
4. 失败原因和局限性分析。

禁止把上述人类评测准备写成 repair loop 内部的 human-in-the-loop 方法贡献。

## 5. 停止和回滚边界

| 情况 | R0 原则 |
|---|---|
| 新增阻塞诊断 | 默认拒绝候选或回滚。 |
| 冻结场景关键回归 | 默认拒绝候选或回滚。 |
| 语义偏离 `NL` | 即使诊断减少，也不能称为 `Better STM`。 |
| 振荡 / 超时 / 不收敛 | 记录为失败模式，不临时人工修补后算成功。 |
| 仅 converter 清洗带来改善 | 不计入 repair-loop 贡献。 |

## 6. 与后续 PR 的接口

| 后续 PR | 从 R0 继承什么 |
|---|---|
| R1 | baseline / prior artifact 的新角色与资产盘点字段。 |
| R2 | seed 来源类型和四例样本必须在 R1 后冻结。 |
| R3 | 转换收益与修正收益必须分开记录。 |
| R4 | 评价门必须在真实修正预演前冻结。 |
| R5 | 自动修正循环必须包含接受、拒绝、回滚和不收敛记录。 |
| R6 | 主实验和对照不能新增/删除/替换 R4 已冻结的核心指标。 |
| R7 | 论文骨架必须遵守本任务边界与禁止 claim。 |
