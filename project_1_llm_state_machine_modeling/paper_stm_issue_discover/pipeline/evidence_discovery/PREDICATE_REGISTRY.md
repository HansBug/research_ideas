# 四族 19 谓词注册表

**版本：** `four-family-19-core.v1`。机器真源为 [predicate_registry.json](predicate_registry.json)。19 个谓词均已完成学术资格审查，并且均有与冻结语义一致的 typed contract、compiled form 和 native backend。来源 ID、类型和边界可审计，但不构成运行时准入门。

| ID | 语义 | 原生执行 |
|---|---|---|
| S1 | `element_exists` | `StateMachine` 声明对象 |
| S2 | `transition_exists` | `Transition` 的 owner-local endpoint |
| S3 | `trigger_set_equals` | `Transition.event` |
| S4 | `state_action_attached` | `State` 的 entry/do/exit action |
| S5 | `transition_guard_equals` | `Transition.guard` AST |
| S6 | `transition_effect_attached` | `Transition.effects` AST |
| G1 | `may_reach` | native leaf topology |
| G2 | `must_reach` | `.fbmcq must_reach` |
| G3 | `route_avoids` | native topology route fragment |
| G4 | `coaccessible_to` | native topology coaccessibility |
| R1 | `event_consumed` | `SimulationRuntime` macrostep |
| R2 | `state_reached_after` | `SimulationRuntime` window |
| R3 | `behavior_occurs` | runtime/lifecycle observation |
| R4 | `state_retained` | `SimulationRuntime` interval |
| V1 | `guards_disjoint` | `.fbmcq forbid` |
| V2 | `guards_complete` | `.fbmcq forbid` |
| V3 | `response_within` | `.fbmcq response` |
| V4 | `deadlock_free` | native stable leaves + `.fbmcq reach` |
| V5 | `state_invariant` | `.fbmcq invariant` |

`ModelIR` 是从 `pyfcstm` 原生 parser/AST/model 对象投影出的 compatibility binding/attribution 接口；它不重新解析 FCSTM DSL，也不得用于替代上表的 truth evaluation。state/event/transition 的 canonical path、owner、pseudo-state、forced/combo provenance 和 native carrier ref 是唯一精确身份；局部 display name 只用于展示，不能在同名层次中猜测绑定。若具体输入不满足 frozen soundness fragment，仍应记录精确 W1 和 `input_contract_missing`/`out_of_fragment` 证据，而不是修改 registry 或缩小分母。

实验分母不改变 registry 资格。固定 15-pair 诊断分母为 S1--S6、G1、G4、R1、R4、V1、V4（12 个）；固定 54x3 分母为 S1--S6、G1--G4、R1、R2、R4、V1、V4（15 个）。后者正好对应机器 registry 的非零 planned mapping，G2、G3、R2 即使未形成真实输入也必须保留在分母并报告 stage-loss。R3、V2、V3、V5 在该实验的 planned count 为零，只表示本协议不制造实验输入，不影响它们的学术资格、typed contract、compiled form、native backend 或 conformance 义务。

registry/backend 与单次输入可行性是两个字段轴。19 个冻结 ID 当前全部 `backend_implemented=true`；单次 `invalid_input`、soundness fragment 不满足或 scenario/domain/carrier 未闭合，只能分别报告 `input_contract_missing`/`out_of_fragment` 和 W1/W0，不能写成 `backend_missing`。receipt 中的 `backend=none` 只表示该计划没有进入 backend，不能推翻 19/19 backend conformance。

下列语义边界不是谓词：requirement-relative containment、direct-member cardinality、initial vertex count、宽泛 event consumer coverage、orthogonal concurrency、hierarchy priority、trace variable delta。它们不得伪装为 S1--V5；精确语义问题可作为 W1 保留。
