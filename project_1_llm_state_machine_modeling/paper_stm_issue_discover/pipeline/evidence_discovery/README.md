# 证据发现方法

本目录是当前 method 的唯一实现入口。冻结注册表为 `four-family-19-core.v1`：结构 6、拓扑 4、轨迹 4、有界验证 5，共 19 个谓词。不得新增、删除、改名或重定义谓词。

## 当前协议

19 个冻结谓词都已经完成学术资格审查。`related_work/provenance/current_source_catalog.json` 的 bibliography 记录只保存来源 ID、三类来源、引用和适用边界；它不参与运行时 W、backend 准入、publication 或 coverage 计算。

W 只有 `W2/W1/W0`：

- `W2`：冻结谓词以精确、合法、完整的 typed binding，在当前被检制品上由一致 backend 终止求值得到 `true` 或 `false`。`false` 是 violation，`true` 是 satisfaction receipt；只有前者可能随 D1/D2 发布。
- `W1`：语义和元素绑定精确，但没有一次合法完成的谓词求值。unsupported、invalid input、timeout、backend error 和 attribution failure 均在独立 execution audit 中记录，不构成 violation。
- `W0`：未形成精确可靠的语义/元素绑定；不参与 hit 或 FP。

运行回执必须分别保存 `execution_state`、`predicate_verdict`、`failure_kind`、`degraded_from`、`degradation_reason`、`attempt_count`、`retry_records`、`billable`、`independent_semantic_basis`、`reason` 与 `basis`。不存在第四个 W 等级。

## 原生执行边界

FCSTM DSL 只由 `pyfcstm` 原生 parser/AST/model class 解释。兼容入口 `parse_fcstm` 只做 native load，`ModelIR` 是原生对象的 Pydantic compatibility projection，服务于稳定 ref、binding、事实投影和归因，不能成为第二个 parser 或替代执行模型。每个冻结谓词均有真实、可终止、可返回布尔值的 backend：

- S1--S6 读取 `pyfcstm.model.StateMachine`、`State`、`Transition`、生命周期 action、guard AST 与 effect AST。
- G1--G4 使用 `pyfcstm.verify.topology` 的原生叶级拓扑投影，必要的全称/有界检查使用 `.fbmcq`。
- R1--R4 在 method-owned 的封闭 scenario、event queue、schedule、macrostep、window 与终止边界上调用 `pyfcstm.simulate.SimulationRuntime`。
- V1--V5 读取原生 FCSTM model class，并经 `.fbmcq` 的 compile/solve/witness/replay 流水线产生结果。

后端不得使用 Python `inspect`，不得从字符串手写图、守卫求值器、有限赋值枚举器或静态 source trace 伪造运行结论。

所有 FCSTM 语义处理均使用 native state/event/transition/AST identity：包含 hierarchy/path、pseudo-state、forced/combo authored carrier、trigger、guard/effect、lifecycle action、topology、runtime 和 `.fbmcq`。禁止用正则、`splitlines`、brace stack 或文本切片重新解析 FCSTM source。允许方法在 native identity 上构建 Pydantic facts、route、输入闭包和审计算法；PlantUML/canonical source 仍可由其专用 source parser 处理，但不是 FCSTM execution model。每次冻结使用 `inputs.native_projection_audit` 生成审计制品，要求 60/60 source、54/54 input closure、projection parity 和 static allowlist 全部通过。

`.fbmcq` 的 native load、query prepare、core build、property compile、solve、decode 和 replay 全部在可终止 worker 中运行。父进程执行全链路 wall-clock deadline 和 RSS 安全上限，默认分别为 15 秒与 2 GiB，可通过 `EVIDENCE_FBMCQ_WALL_CLOCK_TIMEOUT_MS`、`EVIDENCE_FBMCQ_MEMORY_LIMIT_BYTES` 显式配置；`timeout_ms` 仅是 solver 内部预算，绝不能代替前两者。回执保存每一阶段的开始/结束/耗时、query/model hash、bound、state/transition/variable 计数、失败阶段和资源终止原因。worker timeout、memory limit 或 backend exception 只生成 terminal failure receipt，并按精确 binding 退化 W1/W0，绝不产生 `false`、W2 或 issue。

V5 `state_invariant` 可从小 bound 递增检查：若较小 bound 得到可 replay 的 counterexample，该 trace 是请求 horizon 内的有效反例，可提前返回 W2 `false`；较小 bound 的 `true` 只是中间进展，必须继续到请求 horizon 或在共享全链路 deadline 后诚实退化。

## 主 route 与保存 A/B

主 route 依次执行 `typed contract -> compatible predicate set -> exact input binder -> compiler -> native backend`。它仅使用当前 pair 的 method 输入；ledger、Judge、答案、其他 pair 与 pair-ID 特判都不在输入边界内。

LLM 的预选 `predicate_id` 不构成 typed execution plan。S4/S6 即使已被模型标注，也必须回到 exact input binder：S4 需分别闭合 native state、`entry/do/exit` 和 action；S6 需闭合 native transition carrier 与 pyfcstm 可解析的单一 operation effect。无法闭合时删除 execution plan、保留精确 W1，不得把状态名、业务阶段、事件名或自然语言动作短语伪装为 FCSTM lifecycle/effect 输入。

- R1 需要 exact event/carrier、唯一 native cold entry 和唯一无 guard direct carrier，才能构造 cold-start event queue、schedule 和 macrostep。
- R4 需要 requirement 明示 `scenario=cold` 和 `window=cold_macrosteps=N`，其中 `N <= 32`；开放 prose 时间窗保持 W1。
- V1 需要 native same-choice guarded group、完整 exact carrier 集和 requirement 独立给出的有限 JSON `domain`；不得从 guard 或观察到的变量值补造 domain。

15-pair 的固定 planned 分母为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4。selection preflight 仅保存这 12 个谓词的通用能力、typed schema、语义形状和输入 hash，不包含 ledger、expected、Judge、答案、D/L 或评测字段；它只以 hash/reference 进入 run manifest，不进入 method worker 的 candidate、binding、route 或 backend 输入。未列入该分母的冻结谓词仍全部具有学术资格和 native backend。

当前正确的 provider-free A/B artifact ID 是 `f993bb21aa5c39e8a93f8ba1899c29e9`（`evidence-discovery-15x1-primary-route-replay-05699769`）。它只重放保存的最终 `predicate_id=null` W1 evidence（88 条），不使用较宽的辅助 `execute_batch` candidate 集，且 provider/Judge 调用均为 0；20 条候选已完成确定性路由，其中 17 条获得 W2。该 A/B 只报告 route、execution 和 W 的确定性变化，不能代替 hit、precision 或 Judge 评测。

## 隔离与审计

method 只读取当前 pair 的 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、working contracts 与封闭 ModelIR。它不读取台账 expected、L、Judge、答案、其他 pair 或未来结果。Judge 是独立 evaluation 层，冻结口径不参与 method 的 W/D/candidate。

每个 W2 的 `audit_bundle` 必须闭合：typed inputs、compiled program/hash、backend/algorithm version、真实 result、receipt hash、NL/PlantUML/canonical IR/FCSTM/facts/model 的当前制品归因、reason、basis 和 retry/billing。完整运行还保存 immutable run ID、source commit、prompt/schema/registry/input hash 与成本。

详细规则见 [METHOD_PRINCIPLES.md](METHOD_PRINCIPLES.md)、[PREDICATE_REGISTRY.md](PREDICATE_REGISTRY.md)、[REFACTOR_PLAN.md](REFACTOR_PLAN.md) 和 [POLICY_REVIEW.md](POLICY_REVIEW.md)。
