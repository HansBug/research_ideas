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

下列语义边界不是谓词：requirement-relative containment、direct-member cardinality、initial vertex count、宽泛 event consumer coverage、orthogonal concurrency、hierarchy priority、trace variable delta。它们不得伪装为 S1--V5；精确语义问题可作为 W1 保留。
