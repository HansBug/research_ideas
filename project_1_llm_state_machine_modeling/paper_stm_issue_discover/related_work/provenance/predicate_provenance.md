# R1 的 19 个谓词来源与边界审计

本表是 R1 唯一的逐条谓词 citation/boundary 审计。语义文本来自冻结 [registry](../../method/src/paper_stm_method/resources/predicate_registry.json)，不是重新定义 registry。`domain`、`formal` 和 `technical` 在此表中只表示外部来源应承担的不同职责；冻结来源标识目录尚缺与 `D1--F7/T1--T2` 的完整可机读交叉映射，因此这些角色仍待逐条复核，不能被视为运行时注册表字段。每一次 W2 还必须满足精确 typed binding、闭合 FCSTM hash 归因、声明 fragment、编译对象 hash、原生终止布尔回执和完整 receipt；本表不产生任何回执。

状态含义：`条件可写` 指可在表中列出的 fragment 内描述；`语义不匹配` 指 registry 文字不能直接等同于现有后端所检验的命题；`TODO-CITATION` 指缺少外部可引用的 FCSTM 执行语义或需求域依据。后两类不应承重为无界、通用或全面正确性主张。

| ID | 精确语义与需求义务 | 来源职责 | 后端、W2 范围与 soundness boundary | citation 状态与不能推出的结论 |
| --- | --- | --- | --- | --- |
| S1 | `element_exists`：指定类型和名称属于闭合声明表；义务是需求明示元素存在。 | domain：D1 控制系统元素；formal：F1 UML 元模型；technical：本地 declaration inventory。 | 仅闭合根或明确 scope 的原生声明表。 | 条件可写；不推出 containment、基数、可达或运行活动。 |
| S2 | `transition_exists`：精确 source/target 间存在迁移；义务是需求明示转换。 | D1；F1；本地 endpoint resolution。 | 精确端点，闭合或明确 owner scope。 | 条件可写；不推出 enabledness、可达、trigger 或 effect。 |
| S3 | `trigger_set_equals`：指定迁移的解析 trigger 集等于要求集；义务是精确 trigger 归属。 | D1；F1；本地 token-set binding。 | 精确 carrier 和无序 token 集。 | `TODO-CITATION`：FCSTM token 相等语义；不推出 event path identity 或事件被消费。 |
| S4 | `state_action_attached`：动作挂在指定状态的 entry/do/exit 槽；义务是生命周期动作归属。 | D1；F1；本地 lifecycle slot。 | 精确 state、phase 和 action identity。 | 条件可写；attachment 不推出动作执行或后状态保证。 |
| S5 | `transition_guard_equals`：迁移 guard 的解析 AST 等于要求 guard；义务是 guard 文本结构。 | D1；F1；T1 辅助 AST/SMT 边界。 | 精确 carrier 的 FCSTM guard-AST。 | `TODO-CITATION`：AST equality 的 FCSTM 语义；不推出逻辑等价、可满足性或业务等价。 |
| S6 | `transition_effect_attached`：effect 属于指定迁移的 effect 集；义务是 effect 挂接。 | D1；F1；本地 effect operation carrier。 | 精确 carrier 上一个可解析 effect。 | 条件可写；不推出执行、输出或变量变化。 |
| G1 | `may_reach`：有限图存在从 source 到 target 的路径；义务是可达路径。 | D1；F4；T2 图查询语义。 | 原生 leaf-level macro graph 的精确 source/target。 | 条件可写；不推出 guard、数据、优先级或调度下可执行。 |
| G2 | `must_reach`：registry 写为每条路径最终经过 target；义务是必达。 | D1；F4/F5；本地 `.fbmcq must_reach`。 | 后端实际检查 `must_reach <= H`，`H` 为声明状态数。 | 语义不匹配；不得把有限界结果写为 `AF`、无界活性或完整 configuration-space 证明。 |
| G3 | `route_avoids`：从 source 到 target 的路径避开禁止集合；义务是显式避开路径。 | D1；F4/F5；本地 topology。 | 仅精确 leaf states；当前不支持 forbidden edges。 | 语义不匹配；无 source-target 路径时会有空真值，不能推出存在安全路径。 |
| G4 | `coaccessible_to`：每个 root-reachable 节点可到达 marked 节点；义务是声明图上的共可达。 | D1；F6；T2 图查询。 | 已声明 root、marked 集和闭合图。 | 条件可写；不推出全路径终止、deadlock-free、公平性或运行进展。 |
| R1 | `event_consumed`：精确事件在声明 macrostep 发生并被消费；义务是封闭场景事件响应。 | D1；F2；本地 `SimulationRuntime`。 | 一个 cold scenario、精确 event/carrier、前后 trace。 | `TODO-CITATION`：FCSTM consumed/macrostep 语义；单条 schedule 不推出所有事件或所有调度。 |
| R2 | `state_reached_after`：目标状态在刺激后的 trace window 尾部 active；义务是场景结果。 | D1；F2/F4；本地 `SimulationRuntime`。 | 一个封闭 stimulus 场景和有限 trailing window。 | 条件可写；不推出因果或全调度可达。 |
| R3 | `behavior_occurs`：指定行为在 trace 的 owner/slot 发生；义务是抽象生命周期行为发生。 | D1；F1/F2；本地 `.fbmcq called()`。 | 固定 schedule/window 的具名抽象 lifecycle action。 | `TODO-CITATION`：`called()` 和 replay fidelity；不推出具体操作或输出执行。 |
| R4 | `state_retained`：目标状态在封闭 interval 的所有记录点 active；义务是有限场景内保持。 | D1；F2/F4；本地 `SimulationRuntime`。 | 精确 state、closed macrostep interval。 | 条件可写；不推出连续时间保持、全局不变式或开放的 until。 |
| V1 | `guards_disjoint`：同一选择组 guard 在声明 domain 内两两不可同时满足；义务是该 domain 内无重叠选择。 | D1；F3；T1；本地 `.fbmcq forbid`。 | 完整 same-source/same-event 组和独立声明的有限 domain。 | `TODO-CITATION`：domain 的需求来源；有限 domain 结果不推出全输入互斥，UML 也不将此设为默认义务。 |
| V2 | `guards_complete`：同一选择组 guard 析取覆盖声明 domain；义务是该 domain 内输入覆盖。 | D1；F3；T1；本地 `.fbmcq forbid`。 | 完整选择组和有限声明 domain。 | `TODO-CITATION`：domain authority；不推出全环境输入覆盖或 deadlock freedom。 |
| V3 | `response_within`：在给定 bound/unit/scope 内，p 后 q 发生；义务是有界响应。 | D1；F4/F5/F7；T2；本地 `.fbmcq response`。 | 当前执行器只接受 `unit=steps` 的有限 bound。 | 语义不匹配；不得写为 physical time、无界 response 或无需 BMC completeness 的证明。 |
| V4 | `deadlock_free`：registry 写为每个可达稳定非终止 configuration 可进展。 | D1；F5；T2；本地 per-leaf reach probes。 | 后端遍历 topology-reachable stable leaves，检查存在一步进展。 | 语义不匹配；不得写为全 valuation/configuration、fairness 或并发 deadlock-freedom。 |
| V5 | `state_invariant`：registry 写为每个可达 configuration 具有期待 occupancy。 | D1；F4/F5/F7；本地 bounded encoding。 | 检查至 `H = declared-state count` 的有限 horizon。 | 语义不匹配；`true` receipt 不推出无界 invariant 或所有数据状态。 |

## 可用于正文的族级表述

- **结构：** 在闭合模型 inventory 与精确 carrier 上检查元素、迁移、trigger、动作、guard 和 effect 的归属。静态挂接不等于执行。
- **拓扑：** 在声明的有限图和 scope 内处理存在路径、有限界必达、避开和共可达。图性质不等于 guard/data/scheduling 下的运行性质。
- **轨迹仿真：** 对闭合场景中的 event、状态和生命周期观察保存一次 trace evidence。单条 trace 不是 all-traces 证明。
- **有界验证：** 在明确 domain、scope 和 finite horizon 内检查 guard、响应、进展和 occupancy。有限界 `true` 不自动升级为无界性质证明。

这些是本项目对外部概念的保守操作化，不把 D1--F7 中的任何来源写成项目 L/W/D、K/N/I 或 grouping 的原始定义。完整外部书目和全文定位仍需按本表的 `TODO-CITATION` 补齐；在此之前，正文不使用“19 个谓词均有完整学术资格”或等价表述。
