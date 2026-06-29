# task boundary：`<NL, STM_0> -> STM_k` 的方法范围

## 0. 来源与当前性

| 字段 | 值 |
|---|---|
| 原始来源 | R0 `task_boundary.md`，后在 R5 简化时折叠进 [README.md](./README.md) |
| 本轮恢复目的 | 恢复独立任务边界入口，避免方法内外、人类角色、停止/回滚策略被 README 隐藏 |
| 当前证据入口 | [../reports/2026-06-28-22-54-39-model-scope-handoff.md](../reports/2026-06-28-22-54-39-model-scope-handoff.md)、[../experiment_design/README.md](../experiment_design/README.md)、[../STATUS.md](../STATUS.md) |
| 当前性 | 本文件冻结 story-level 边界；正式 model scope / eligibility / protocol 仍应在 `experiment_design/` 后续文件中冻结 |

## 1. 任务定义

输入为自然语言需求 `NL` 与初始状态机 `STM_0`。输出为经过自动反馈驱动修正循环后的候选状态机 `STM_k`，以及每轮诊断、反馈、候选修正、接受 / 拒绝 / 回滚证据。

```text
Input:  <NL, STM_0>
Output: <STM_k, diagnostics ledger, scenario ledger, repair ledger, acceptance / rollback ledger>
```

`STM_0` 可以来自一手 LLM-generated STM、prior artifact、学生/人工初始模型或其他可审计 seed source；但 seed construction 不属于 repair run 内贡献。`STM_k` 必须由同一个 frozen `<NL, STM_0>` 出发，不能在 run 中手工替换初始模型。

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
| selected smoke 例子整理 | engineering smoke input | 只用于链路冒烟，不作为最终实验集合。 |
| 学生 / 人工初始建模 | seed source | 必须记录任务说明、参与者角色、允许工具与数据边界。 |
| reference / adjudication | evaluation audit | 人类可参与，但不属于 repair run 内方法。 |
| paper writing / post-hoc failure analysis | reporting / threats | 可有人类参与，不能回写到 run 内形成 hidden intervention。 |

## 4. 人类角色边界

| 人类活动 | 允许性 | 是否属于 repair run 内 no-human-in-the-loop |
|---|---:|---|
| 设计 benchmark / seed registry | 允许 | 不属于 run 内。 |
| 制作参考裁决 / 人工审计 | 允许 | 不属于 run 内。 |
| 冻结 eligibility、scope、metrics | 允许 | 不属于 run 内。 |
| 在某轮修正失败后手工改 `STM_i` 再继续 | 不允许 | 会破坏无人化修正定义。 |
| 事后分析失败模式 | 允许 | 作为 evaluation / threats。 |

## 5. 停止、拒绝与回滚

候选修正不能只要“看起来更好”就接受。最低策略：

1. 若引入新的阻塞级诊断，拒绝 candidate。
2. 若冻结场景或回归检查退化，拒绝 candidate。
3. 若 NL-grounded adjudication 判定语义退化，拒绝 candidate。
4. 若多轮在同类候选间振荡，记录 oscillation 并停止或回滚到当前最佳。
5. 若超过 `max_iterations` 或预算，记录 non-convergence，不手工补救。

## 6. conversion attribution 边界

必须区分三层：

| 层 | 说明 | 能否计为 repair-loop 收益 |
|---|---|---:|
| 原始制品 | 一手 `STM_0` 原始 PlantUML / Umple / 其他格式。 | 否 |
| 规范化 `STM_0` | 经过 parser / converter / representation bridge 得到的内部可机检表示。 | 否，除非只报告为 normalization effect。 |
| 修正后 `STM_k` | repair loop 在同一 frozen `STM_0` 上产生并通过接受门的候选。 | 可以，但必须有回归和裁决证据。 |

如果某个改进来自 pre-repair conversion / recovery / hand normalization，则必须归因给 conversion / seed preparation，不能计入 repair-loop gain。

## 7. R5.5 后的 model scope 暂定边界

R5.5 画像建议后续主实验优先围绕 `llms-emp-stm-subset`：10 个唯一 NL × 6 个 LLM 输出。当前 story-level 暂定为：

| 层级 | 暂定角色 | 证据入口 | 说明 |
|---|---|---|---|
| T0 / T0.5 离散 FSM/HSM/statechart | 主线候选 | [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | 更适合当前 repair loop 先跑通。 |
| Digital Camera / T1-ish stress | supplementary stress | [../reports/2026-06-28-22-54-39-model-scope-handoff.md](../reports/2026-06-28-22-54-39-model-scope-handoff.md) | 不支撑 T0 主 claim，只作压力/负证据。 |
| data-rich EFSM / timed automata / full verification | 暂不作为主线 | 后续 scope 决策 | 当前证据和工具链不足以支撑强 claim。 |

正式冻结仍应落到 [../experiment_design/scope/](../experiment_design/scope/)；本节只是 story handoff，不是最终协议。

## 8. R0 不冻结的内容

R0/R5.5 story 不冻结具体 `seed_id` 纳入、转换 schema、诊断代码枚举、场景 fixture、LLM prompt、模型 ID、统计阈值和主实验纳入规则。这些分别由 R5.6、R5.7、R6/R8 或后续协议冻结。
