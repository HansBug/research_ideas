# task boundary：`<NL, STM_0> -> STM_k` 的方法范围

## 1. 任务定义

输入为自然语言需求 `NL` 与初始状态机 `STM_0`。输出为经过自动反馈驱动修正循环后的候选状态机 `STM_k`，以及每轮诊断、反馈、候选修正、接受 / 拒绝 / 回滚证据。

```text
Input:  <NL, STM_0>
Output: <STM_k, diagnostics ledger, scenario ledger, repair ledger, acceptance / rollback ledger>
```

## 2. 方法内范围

| 阶段 | 是否属于方法内 | 说明 |
|---|---:|---|
| 对 `STM_i` 做解析、语义、设计、场景诊断 | 是 | 产生结构化 feedback。 |
| 基于 feedback 生成 candidate repair | 是 | 可以由 LLM 或 deterministic repair policy 参与，但必须受冻结输入和检查门约束。 |
| 对 candidate 重新执行诊断、场景和回归检查 | 是 | 决定接受、拒绝或回滚。 |
| 记录 rejected repair、oscillation、non-convergence | 是 | 失败也是结果的一部分。 |
| 在 `max_iterations` 或停止条件内选择当前最佳候选 | 是 | 不允许人工临时介入修正 run。 |

## 3. 方法外范围

| 阶段 | 定位 | 后续记录要求 |
|---|---|---|
| `NL -> STM_0` prompt-based 生成 | seed construction | 记录 prompt、模型、配置和来源；不作为主贡献。 |
| prior work artifact 转换为内部表示 | converter / seed preparation | 必须记录转换损失、人工补全和归因；不计入 repair-loop 收益。 |
| 学生 / 人工初始建模 | seed source | 必须记录任务说明、参与者角色、允许工具与数据边界。 |
| reference / adjudication | evaluation audit | 人类可参与，但不属于 repair run 内方法。 |

## 4. 人类角色边界

| 人类活动 | 允许性 | 是否属于 repair run 内 no-human-in-the-loop |
|---|---:|---|
| 设计 benchmark / seed registry | 允许 | 不属于 run 内。 |
| 制作参考裁决 / 人工审计 | 允许 | 不属于 run 内。 |
| 在某轮修正失败后手工改 `STM_i` 再继续 | 不允许 | 会破坏无人化修正定义。 |
| 事后分析失败模式 | 允许 | 作为 evaluation / threats。 |

## 5. 停止、拒绝与回滚

候选修正不能只要“看起来更好”就接受。最低策略：

1. 若引入新的阻塞级诊断，拒绝 candidate。
2. 若冻结场景或回归检查退化，拒绝 candidate。
3. 若 NL-grounded adjudication 判定语义退化，拒绝 candidate。
4. 若多轮在同类候选间振荡，记录 oscillation 并停止或回滚到当前最佳。
5. 若超过 `max_iterations` 或预算，记录 non-convergence，不手工补救。

## 6. R0 不冻结的内容

R0 不冻结具体 `seed_id`、转换 schema、诊断代码枚举、场景 fixture、LLM prompt、模型 ID、统计阈值和主实验纳入规则。这些分别由 PR-R1 到 PR-R6 冻结。
