# Better STM：最小操作化定义

## 1. 公式

R0 采用如下 shorthand：

$$
Better(STM_k, STM_0 | NL, S, D, R)
$$

其中：

| 符号 | 含义 |
|---|---|
| `NL` | 自然语言需求。 |
| `STM_0` | 同一来源、同一转换流程下的规范化初始状态机。 |
| `STM_k` | 修正循环输出的候选状态机。 |
| `S` | 冻结的场景 / 回归套件。 |
| `D` | 解析、语义、设计和仿真诊断集合。 |
| `R` | 预注册人工 / 结构化评价量表。 |

## 2. 五条最低必要条件

只有同时满足以下条件，`STM_k` 才能计为相对 `STM_0` 的 Better STM：

1. **无新增阻塞级诊断**：`STM_k` 不得引入 `STM_0` 没有的 blocking parse / semantic / design issue。
2. **冻结场景和回归不退化**：在同一 `S` 上，关键 pass/fail、trace expectation 或 safety-relevant behavior 不得退化。
3. **至少一个预注册维度改进**：例如 blocking diagnostics 减少、semantic / executable validity 提升、场景通过率提升、组件级缺陷减少或 NL-grounded adjudication 更一致。
4. **NL-grounded adjudication 不判为语义退化**：诊断减少但需求语义偏离，不能算 Better STM。
5. **转换规范化收益与 repair-loop 收益分开统计**：格式转换、人工补全或 normalization 带来的改善不能计入 repair-loop 贡献。

## 3. 反例边界

| 情况 | 是否可算 Better STM | 原因 |
|---|---:|---|
| 诊断减少但行为更差。 | 否 | 违反场景 / 语义条件。 |
| 场景通过但 guard / action 偏离 `NL`。 | 否 | 违反 NL-grounded adjudication。 |
| 只因 converter 清洗格式导致诊断减少。 | 否 | 属于转换规范化收益。 |
| 为通过测试删除需求相关行为。 | 否 | 属于过修 / semantic drift。 |
| 修正后无新增 blocking issue，场景不退化，且预注册维度改善。 | 可能 | 仍需人工 / 结构化评价确认。 |

## 4. 三阶段归因

所有可进入 RQ4 统计的样例必须记录：

```text
原始种子 / 来源制品 -> 转换后规范化 STM_0 -> 修正后 STM_k
```

| 差值 | 含义 | 是否可计入 repair-loop 贡献 |
|---|---|---:|
| 原始种子到转换后 `STM_0` | converter / normalization 贡献或损失 | 否 |
| 转换后 `STM_0` 到 `STM_k` | repair-loop 贡献或退化 | 满足五条件时才可计入 |
| 人工补全导致的改善 | manual normalization | 默认否，除非单独实验条件报告 |

## 5. 与 RQ4 的关系

RQ4 的通过判定等价于五条最低必要条件全部满足。任一条件失败，该 run 不得计为 Better STM，只能进入失败、局限、不收敛或回归分析。
