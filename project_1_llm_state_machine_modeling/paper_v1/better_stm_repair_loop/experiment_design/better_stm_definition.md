# Better STM Definition

## 1. 最小判定框架

R0 使用以下 shorthand 表示相对更优状态机候选：$Better(STM_k, STM_0 \mid NL, S, D, R)$。

其中：

- $NL$：自然语言需求；
- $STM_0$：同一来源下的初始状态机，原则上指转换后、修正前的规范化 baseline；
- $STM_k$：修正循环输出的候选模型；
- $S$：冻结的场景 / 回归套件；
- $D$：解析、语义、设计、仿真诊断集合；
- $R$：预注册人工 / 结构化评价量表。

## 2. 五条最低必要条件

`STM_k` 只有同时满足以下条件，才能在 RQ4 中计为相对更优：

1. **无新增阻塞级诊断**：`STM_k` 不得引入 `STM_0` 没有的 blocking parse / semantic / design issue。
2. **冻结场景不关键回归**：在同一 $S$ 上不得出现 safety-relevant 或 task-critical regression。
3. **至少一个预注册维度改进**：例如 blocking diagnostics 减少、场景通过率提升、组件级缺陷减少或 NL-grounded consistency 更好。
4. **NL-grounded adjudication 不判为语义退化**：若模型偏离需求，即使 diagnostics 减少，也不能称为更优。
5. **转换收益与修正收益分开统计**：格式转换、人工规范化或 seed 清洗带来的改善不得计入 repair-loop contribution。

## 3. 三阶段归因台账

后续 R3/R6 必须至少记录：

```text
原始种子 / 来源制品 -> 转换后规范化 STM_0 -> 修正后 STM_k
```

| 计数阶段 | 目的 | 是否可计入 repair-loop 贡献 |
|---|---|---:|
| 转换前 | 识别原始 artifact / 格式问题。 | 否 |
| 转换后 / 修正前 | repair-loop 的真实 baseline。 | 否，作为比较起点 |
| 修正后 | 观察自动修正后的变化。 | 仅在五条件满足时可计入 |

## 4. 反例边界

以下情况不能直接称为 `Better STM`：

1. diagnostics 变少但 guard / action 偏离 `NL`；
2. scenario 通过但删除了需求相关行为；
3. 仅 converter 清洗让模型更规范；
4. 人工临时补字段或手动改语义后才通过；
5. 某一维度提升但新增 critical regression；
6. run 超时、振荡或不收敛后只保留成功片段。

## 5. 与 R4/R6 的关系

本文件是 R0 的最小定义。R4 需要冻结诊断代码、场景套件、评价量表草案、主结果纳入规则和统计表结构；R6 需要冻结主实验阈值、对照矩阵、人工裁决和降级写法。R4/R6 可以细化本定义，但不得降低五条最低必要条件。
