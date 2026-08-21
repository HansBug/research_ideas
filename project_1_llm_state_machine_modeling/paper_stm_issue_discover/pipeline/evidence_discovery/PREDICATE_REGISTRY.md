# 四族 19 谓词注册表

**注册表版本：** `four-family-19-core.v1`  
**状态：** 冻结设计，代码迁移待完成  
**唯一机器可读来源：** [`predicate_registry.json`](predicate_registry.json)

本表是当前方法唯一的公开谓词表。谓词从领域分析、真实文献、标准/形式语义资料和
技术资料中按命题归纳；台账只用于冻结后的可表达性映射，不用于反向创造谓词。
每行的来源类型以机器注册表中的 `source_types` 为准：`domain` 表示领域来源，
`formal` 表示形式/标准来源，`technical` 表示后端或算法技术来源。当前登记不等于
严格准入全部通过。

## 1. 核心谓词

| ID | 谓词名 | 谓词族 | 简明语义 | 最小输入 | 预期台账条目 | 预期 v27 条目 | 来源类型与边界 |
|---|---|---|---|---|---:|---:|---|
| S1 | `element_exists` | 结构 | 指定种类的命名元素属于封闭声明清单。 | kind、element、scope | 14 | 0 | ST1/ST2/ST4；只证明模型内存在，不证明父子关系或数量。 |
| S2 | `transition_exists` | 结构 | 指定源和目标之间存在一条迁移。 | source、target、scope | 20 | 150 | ST1/ST2/ST4；只证明端点和迁移存在。 |
| S3 | `trigger_set_equals` | 结构 | 某条迁移解析后的触发集合等于需求集合。 | transition、triggers | 22 | 54 | ST1/ST2/ST5；不声称运行时消费。 |
| S4 | `state_action_attached` | 结构 | 指定动作挂在指定状态的指定生命周期阶段。 | state、phase、action | 10 | 193 | ST1/ST3/ST7；只判归属和阶段。 |
| S5 | `transition_guard_equals` | 结构 | 某条迁移解析后的守卫等于需求守卫。 | transition、guard | 3 | 30 | ST1/ST2/ST3；不判守卫可满足性。 |
| S6 | `transition_effect_attached` | 结构 | 指定效果属于指定迁移的效果集合。 | transition、effect | 3 | 0 | ST1/ST2/ST9；不判执行后的变量值。 |
| G1 | `may_reach` | 拓扑 | 从源集合到目标集合存在有限图路径。 | source、target | 16 | 93 | TP1/TP2/ST3；图可达不等于运行时可行。 |
| G2 | `must_reach` | 拓扑 | 在声明的图完备化下，源发出的每条路径最终访问目标。 | source、target | 1 | 30 | TP2/TP3/TP4；不等同于共可达。 |
| G3 | `route_avoids` | 拓扑 | 从源到目标的路径都不经过禁止节点或边集合。 | source、target、forbidden | 3 | 5 | TP3/TP3B/TP3C；禁止范围必须显式给出。 |
| G4 | `coaccessible_to` | 拓扑 | 从根可达的每个节点都能沿有限路径到达标记节点。 | roots、marked | 5 | 0 | TP6/G4-RP1/G4-RP2；不等同于无死锁或公平性。 |
| R1 | `event_consumed` | 轨迹仿真 | 精确的事件出现于声明的宏步中并被消费。 | scenario、event、step | 9 | 0 | TR1/TR2/ST8；回执记录实际消费者。 |
| R2 | `state_reached_after` | 轨迹仿真 | 在声明的轨迹窗口后段，目标状态处于激活状态。 | scenario、stimulus、state、window | 1 | 0 | TR1/TR2/ST3；单条轨迹只说明该调度。 |
| R3 | `behavior_occurs` | 轨迹仿真 | 指定行为在轨迹中指定的拥有者和槽位发生。 | scenario、behavior、window | 0 | 0 | TR1/TR2/ST8；不替代静态挂接检查。 |
| R4 | `state_retained` | 轨迹仿真 | 在封闭区间的每个记录点，目标状态都保持激活。 | scenario、state、interval | 3 | 0 | TR4/TR5/TR6；不声称终止或无死锁。 |
| V1 | `guards_disjoint` | 有界验证 | 同一选择组中任意两条守卫在声明域内不能同时满足。 | source、trigger、domain | 4 | 19 | BV4/BV5/BV6；限定为公式层且不使用优先级。 |
| V2 | `guards_complete` | 有界验证 | 同一选择组的守卫析取覆盖声明输入域。 | source、trigger、domain | 0 | 0 | BV4/BV5/BV6；不推出可达性。 |
| V3 | `response_within` | 有界验证 | 每次支持的 p 发生后，q 在声明界限和单位内发生。 | p、q、bound、unit、scope | 0 | 0 | TP1/BV7/TR1；规范界限不等于搜索视界。 |
| V4 | `deadlock_free` | 有界验证 | 每个可达的非终态稳定配置都存在模型进展。 | initial_scope | 4 | 29 | BV8/BV7/BV9；终止和活锁另行区分。 |
| V5 | `state_invariant` | 有界验证 | 每个可达配置都满足指定状态的预期占用值。 | state、expected、initial_scope | 0 | 0 | TP3/TP3B/TP3C；正向证明需闭包，有限反例搜索不自动构成证明。 |

族计数为：结构 6、拓扑 4、轨迹仿真 4、有界验证 5，共 19 个。

## 2. 派生宏（不增加谓词）

下列操作只能编译为已有原子谓词的组合：

- `initial_edge_to_required_target_exists`
- `initial_transition_triggerless`
- `required_transition_signature`
- `state_action_attached_in_any_lifecycle_phase`
- `termination_decomposition_may_reach_and_must_reach`

宏必须保留展开后的原子谓词、输入绑定和证据来源，不能以宏名逃避 soundness 审查。

## 3. W1-only 与退役核心候选

下列需求可以提出，但当前不作为核心 sound 谓词：

`requirement_relative_containment`、`typed_direct_member_cardinality`、
`initial_vertex_exists_each_required_owner`、`initial_vertex_outdegree_at_most_one`、
`event_consumer_exists_in_scope`、`event_consumer_may_reach`、
`orthogonal_runtime_configuration`、`hierarchical_transition_priority`、
`trace_variable_delta`。

它们需要外部需求参照、精确基数、并发运行时或额外轨迹语义；在没有独立且匹配的
领域证据与 sound 后端前，统一输出 W1 或 coverage gap，不能改名挂到现有谓词上。

## 4. 来源审查边界

来源 ID 的当前落点、命题和边界见 [`CURRENT_SOURCE_AUDIT.md`](../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)
及其机器目录 [`current_source_catalog.json`](../../related_work/provenance/current_source_catalog.json)。
三类来源分别用于说明：

1. 领域系统与状态机中的反复出现的检查命题；
2. UML/状态机形式语义、性质模式和模型检查中的正式命题；
3. 可复核的技术资料或工具语义，用于限定实现和回执边界。

当前来源审计明确区分 `partial_pass`、`candidate` 和 `w1_only_*`。其中 G4、V1、V3、V4
和 R3 当前不能宣称有 sound W2 来源门；它们仍可作为语义问题提出并输出 W1。来源数量不
构成普遍率，台账/v27 使用量不构成学术出处。特别是 UML 2.5.1 没有把同事件守卫互斥
列为状态机约束，不能把它误写成 UML 的普遍要求。

## 5. 变更门

除非有独立领域证据、明确命题匹配、完整学术审查、兼容性迁移和回归测试，否则不得
新增谓词或修改上述定义。覆盖率压力、单个案例、LLM 方便生成或旧 prototype 的实现
便利都不是变更理由。
