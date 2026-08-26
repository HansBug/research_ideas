# Reference Implementation Alignment

当前 method 的 FCSTM 唯一语义真源是 `pyfcstm` 的 parser、AST、`pyfcstm.model.StateMachine` 及其公开 verification、simulation 与 `.fbmcq` API。`ModelIR` 是从同一 native document 投影出的兼容 Pydantic 接口，保留 canonical path、owner、pseudo-state、lifecycle action、forced/combo provenance 与 span；PlantUML、canonical source IR 和 inspect-equivalent facts 是输入绑定与归因层，不是 predicate truth 或第二 FCSTM parser。

| 谓词族 | 实现对齐 |
|---|---|
| Structure | 原生 `State`、`Transition`、event、lifecycle action、guard/effect AST 与 owner scope |
| Topology | `pyfcstm.verify.topology` 的 native leaf-level macro projection；有界全称性质走 `.fbmcq` |
| Trajectory | `SimulationRuntime` 执行 method-owned closed scenario，不读取静态 trace 作为结果 |
| Bounded verification | 原生 state/transition/guard objects 加 `.fbmcq` compile/solve/witness/replay |

所有 backend 必须报告 native algorithm version、FCSTM source hash、typed inputs、compiled code/hash 与真实 terminal result。任何 malformed model、invalid input、unsupported fragment、timeout 或 backend failure 都是 execution audit 事实，不能被变形成 true/false 或 W2。

实现禁止 Python `inspect`、手写 ModelIR 图算法作为后端真值、手写 guard evaluator、手写有限 assignment enumeration 和 pair-specific result branch。unit tests 通过 native positive/negative/invalid/out-of-fragment/failure fixture 固定这些边界。

生产代码不得以正则、`splitlines`、brace stack 或字符串切片重新解释 FCSTM source。方法可以在 pyfcstm 原生 object/path 上实现 Pydantic projection、集合算法、route、输入闭包与审计；这些二次算法不能改变 native hierarchy、forced/combo、runtime 或 `.fbmcq` 的语义。`fcstm_native_projection_audit` 与静态 allowlist 是防止双模型回退的验收证据。

route 同样受 native 边界约束。G2 对 composite source 的唯一执行投影只能递归读取 `State.init_transitions`，每层恰有一条才能下降到 leaf；不得用 ModelIR reachability 任取后代。R2 的 event/target obligation 只能由 typed transition alternative、唯一 canonical author-source carrier 和 exact native Event 联结形成，scenario 只能由 target-independent `SimulationRuntime` prefix 搜索形成。provider-free 验收必须把 saved-candidate route replay 与 saved-extraction/grounding frontier replay 分开落盘、分开解释。

D prompt 不是 execution receipt 的第二份副本。原始 `.fbmcq`/SMT formula 与 solver payload 必须完整留在 backend/audit receipt，D 通过 canonical hash、size、typed plan、terminal result、telemetry 和 replay witness 引用它们。语义 dossier 按 obligation ID 稳定、按实际序列化预算分批且不截断；某批失败只退化该批 D，不得改变 backend truth、W、其他批次或 Judge。
