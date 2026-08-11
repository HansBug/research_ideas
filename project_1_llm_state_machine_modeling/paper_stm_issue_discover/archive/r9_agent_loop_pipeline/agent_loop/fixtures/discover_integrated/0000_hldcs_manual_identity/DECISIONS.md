# 0000 人工 canonicalization 说明

## 使用边界

该模型只用于解除 `PR-discover` 的 smoke 阻塞，不属于自动 PlantUML -> FCSTM 转换结果，不进入 paper1 正式效果统计，也不能作为 reference repair。加载的 source pair 固定为 `llms_emp_feedback_final_0000`；run source 仍采用 `fcstm_identity`，因此 `stm0.puml` 只负责保存 feedback-final source provenance。人工建模过程中实际参考过的 phase-I Generation PlantUML 另存为 [phase_i_generation_provenance.puml](./phase_i_generation_provenance.puml)，只作为 derivation provenance，不得替代 selected source hash。

## 人工裁决

| 原输入冲突或歧义 | 本次裁决 | 理由 |
| --- | --- | --- |
| NL 说 `HumanDriving` 是 simple state，raw PlantUML 却写成 composite | 将 `HumanDriving` 建为 leaf | 遵循明确 NL 类型声明；不保留错误的转换嵌套 |
| NL 说 `Autonomous` 是 submachine，raw 在顶层声明它，但又从 `HumanDriving` 作用域引用 | 将 `Autonomous` 建为与 `HumanDriving` 同级的 composite | 保留模式切换语义，避免把自动模式嵌入人工模式 |
| 两个作用域均使用 `InitialState/FinalState` | 改为唯一的 `AutoInitial/AutoFinal` | 避免短名冲突；名称变化被记录，不宣称字面 identity |
| feedback-final PlantUML 把 `Front Distance > 10` 写在 transition label 中；phase-I derivation 也曾包含同类表达 | 保留为 `Front_Distance_10 named "Front Distance > 10"` event | A 阶段只保留 source 已表达的行为，不借助 NL 把 condition-like label 恢复为变量或 guard；官方 SCXML 与既有 R4.5 lowering 也采用该口径 |
| `Human Steering Cmd or Brake Pressed` 是一个组合文本 | 拆成 `HumanSteeringCommand` 与 `BrakePressed` 两条迁移 | NL 明确表达两个替代触发条件 |
| NL 表示进入 autonomous final 后返回人工模式 | `AutoFinal -> [*]`，完成后由 parent completion 返回 `HumanDriving` | 使用 FCSTM composite completion 语义，不做祖先重入改写 |
| power on 进入人工模式 | 增加隐式 `PoweredOff` carrier，随后由 `PowerOn` 进入 `HumanDriving` | FCSTM composite 需要无条件稳定初态；该 carrier 只操作化 NL 已隐含的上电前状态 |
| steering/brake 需要从 autonomous 任意子状态退出 | 使用 `!Autonomous -> HumanDriving` forced transition | pyfcstm 将其精确展开到 composite 及全部 descendants，避免普通 parent edge 在 active child 下不可触发 |
| raw 只从 `HumanDriving` 表达 power off | 暂仅保留 `HumanDriving -> [*] : PowerOff` | 不擅自增加 autonomous 下的 power-off 行为；该缺口可由 Discover 判断 |

## 仍然保留的 source-level 风险

1. NL 的 power-off 是否应当在 autonomous 模式同样生效，原文没有给出明确作用域。
2. `Front Distance > 10` 仍是 source 中的 condition-like opaque event；它属于 expression debt / semantic opacity 候选，不能仅因没有被恢复为 guard 就算 confirmed issue。
3. phase-I PlantUML 自身的层级与 NL 冲突已经通过人工裁决消解，并仅作为 derivation provenance 保留；正式 loaded source pair 是 feedback-final `AE2`。因此该模型只能作为 conversion-safe pilot，不能用于测量方法发现该层级问题的能力。
