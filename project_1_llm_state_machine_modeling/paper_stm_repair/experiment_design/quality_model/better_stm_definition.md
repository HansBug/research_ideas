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

## 2. 核心判据：可解析 / 可执行不是 Better STM

Better STM 是相对于同一个规范化 `STM_0` 的语义保真修正目标，不是格式可用性标签。R5.6 采用如下状态机抽象作为判定锚点：

$$
M = (S, s_0, E, V, T, H, A, \tau)
$$

迁移写作：

$$
t = (s, e, g, a, s')
$$

其中 $e$ 是 trigger / event，$g$ 是离散、可追溯的 guard 谓词，$a$ 是 action / effect，$\tau$ 是模型元素到 `NL` 片段的 traceability。由此得到三条硬判据：

1. **parse ok 不等于 Better STM**：语法可解析只是进入诊断、场景和裁决流程的最低前置条件；不能单独支持质量提升主张。
2. **executable 不等于 Better STM**：模型能运行或能被仿真，只说明存在可执行语义载体；若状态、事件、guard、action、层级或 traceability 相对 `NL` 退化，仍不得计为 Better。
3. **guard / action / event 不得语义折叠**：若 `NL` 明示条件、触发或效果，而 `STM_k` 把 guard/action 全部揉进 event label，或为通过检查删除需求相关行为，即使诊断减少或场景通过，也必须进入 semantic-drift / over-repair 审查，不能直接计为 Better STM。

因此，Better STM 的正向证据必须同时满足：同一 `STM_0` 起点、预注册维度至少一项改善、冻结场景与回归不退化、`NL` grounding 不判语义退化，并且 conversion / normalization / lowering 收益与 repair-loop 收益分开归因。

## 3. 五条最低必要条件

只有同时满足以下条件，`STM_k` 才能计为相对 `STM_0` 的 Better STM：

1. **无新增阻塞级诊断**：`STM_k` 不得引入 `STM_0` 没有的 blocking parse / semantic / design issue。
2. **冻结场景和回归不退化**：在同一 `S` 上，关键 pass/fail、trace expectation 或 safety-relevant behavior 不得退化。
3. **至少一个预注册维度改进**：例如 blocking diagnostics 减少、semantic / executable validity 提升、场景通过率提升、组件级缺陷减少或 NL-grounded adjudication 更一致。
4. **NL-grounded adjudication 不判为语义退化**：诊断减少但需求语义偏离，不能算 Better STM。
5. **转换规范化收益与 repair-loop 收益分开统计**：格式转换、人工补全或 normalization 带来的改善不能计入 repair-loop 贡献。

## 4. 反例边界

| 情况 | 是否可算 Better STM | 原因 |
|---|---:|---|
| 诊断减少但行为更差。 | 否 | 违反场景 / 语义条件。 |
| 场景通过但 guard / action 偏离 `NL`。 | 否 | 违反 NL-grounded adjudication。 |
| 只因 converter 清洗格式导致诊断减少。 | 否 | 属于转换规范化收益。 |
| 为通过测试删除需求相关行为。 | 否 | 属于过修 / semantic drift。 |
| 修正后无新增 blocking issue，场景不退化，且预注册维度改善。 | 可能 | 仍需人工 / 结构化评价确认。 |

## 5. 三阶段归因

所有可进入 RQ4 统计的样例必须记录：

```text
原始种子 / 来源制品 -> 转换后规范化 STM_0 -> 修正后 STM_k
```

| 差值 | 含义 | 是否可计入 repair-loop 贡献 |
|---|---|---:|
| 原始种子到转换后 `STM_0` | converter / normalization 贡献或损失 | 否 |
| 转换后 `STM_0` 到 `STM_k` | repair-loop 贡献或退化 | 满足五条件时才可计入 |
| 人工补全导致的改善 | manual normalization | 默认否，除非单独实验条件报告 |

## 6. 与 RQ4 的关系

RQ4 的通过判定等价于五条最低必要条件全部满足。任一条件失败，该 run 不得计为 Better STM，只能进入失败、局限、不收敛或回归分析。
