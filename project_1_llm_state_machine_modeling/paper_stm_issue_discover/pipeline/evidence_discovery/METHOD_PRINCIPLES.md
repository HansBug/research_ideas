# 方法原则

## 1. 冻结边界

`four-family-19-core.v1` 的 19 个谓词均已完成学术资格审查。注册表冻结的是定义、最小 typed contract、来源 metadata、soundness fragment 和 backend 实现义务，不是某次运行的结果。不得新增谓词或修改冻结定义；也不得以成本、台账覆盖率、单个 pair 或文献管理标签把无关语义挂到邻近谓词。

bibliography metadata 只解释“为什么该谓词在学术与领域叙事中成立”。运行时只回答“该谓词是否在当前制品上以合法输入真实执行”。两者正交；来源管理信息不得影响 W、backend、D 或 publication。

## 2. W 与执行审计

本方法使用 `W2/W1/W0` 三档确定性逻辑：

| 条件 | W | publication |
|---|---|---|
| 精确 binding、合法 typed inputs、冻结谓词、正确 backend、完整当前制品归因，且 `completed`/`false` | W2 | 仅 D2/D1 可发 issue |
| 同上但 `completed`/`true` | W2 | pass receipt，不发 issue |
| 精确 binding 但 timeout、backend error、invalid input、unsupported backend 或 attribution failure | W1 | 失败本身不能发 issue；仅独立 semantic basis 可支持 D2/D1 |
| binding 不精确 | W0 | D0，不进 hit/FP |

`execution_state` 是 `not_attempted`、`completed` 或 `failed`；`predicate_verdict` 仅为 `true`、`false` 或 null；`failure_kind` 单独保存。没有第四种 W。重试和计费也必须写入 receipt：provider error 原调用重试不计费，其他重试计费；deterministic timeout 最多一次同输入受控重试。

谓词不支持不是发 issue 的资格门。W1 可以是 `semantic_hit`；W0 是 coverage gap。D2/D1/D0 由 method 的确定性裁定，只有 D2 与 D1 可以发布。方法不生成、不裁定台账侧属性 `l_level`，Judge 也不能反向驱动 method。

## 3. Typed、native backend 与来源归因

所有 Pydantic model 都必须有 class docstring 和 Field description；所有结构化模型输出、失败、退化与未执行记录都必须有非空 `reason` 与 `basis`。S4 的 `phase` 只能是 `entry`、`do` 或 `exit`；S2 必须检验 owner-local scope；S5 比较原生 guard AST；S6 只检验 exact transition 的 effect membership。

结构事实必须从 `pyfcstm.model` 的原生 model class 读取，不能由 ModelIR 或字符串近似判断。轨迹必须由 `SimulationRuntime` 在 method-owned closed scenario 中运行。有界检查必须使用 `.fbmcq` compile/solve/witness/replay，不得手写守卫计算、图遍历替代 solver、赋值枚举或静态 trace。后端不得调用 Python `inspect`。

### FCSTM 单一语义源

FCSTM DSL 的唯一语义权威是 `pyfcstm` 的原生 parser、AST、`StateMachine`、`State`、`Event`、`Transition`、topology、`SimulationRuntime` 与 `.fbmcq`。兼容名称 `parse_fcstm` 只调用原生 loader；`ModelIR` 是原生对象的 Pydantic compatibility projection，不是第二套 grammar 或 execution model。它保留 canonical state/event path、owner/path、pseudo-state、lifecycle action、authored forced/combo carrier provenance、source span 与唯一 historical-ref compatibility mapping。

任何涉及 FCSTM 的 state、event、transition、scope、initial/final pseudo-state、trigger、guard、effect、lifecycle action、reachability、choice group、runtime scenario 或 typed carrier resolution，都必须消费上述原生对象或其 native-derived projection。禁止正则、`splitlines`、brace stack、字符串切片或手写 parser 重新解释 FCSTM source；不得用 ModelIR 图遍历替代 pyfcstm hierarchy、forced/combo、runtime 或 `.fbmcq` 真值。文本处理只允许用于非 FCSTM 的 run/ref/hint 格式、provider framing、PlantUML/source attribution；不得决定 FCSTM 语义。

每次冻结前运行 `python -m pipeline.evidence_discovery.inputs.native_projection_audit --report-root pipeline/representation/reports/llms_emp_r45_java_60 --output <immutable-run-artifact>/fcstm_native_projection_audit.json`。gate 要求 60/60 native source load、54/54 frozen input closure、逐项 projection parity 和零 unapproved text handling；source line 仅作 attribution，不能作为完整 carrier identity。

`.fbmcq` 的完整原生链 `native load -> query prepare -> core build -> property compile -> solve -> decode -> replay` 必须在可终止 worker 内运行。父进程的 wall-clock deadline 与 RSS 安全上限覆盖每个阶段；solver 的局部 `timeout_ms` 只覆盖 solve，不能被误写成全链路 timeout。默认上限为 15 秒、2 GiB，且只可通过 `EVIDENCE_FBMCQ_WALL_CLOCK_TIMEOUT_MS`、`EVIDENCE_FBMCQ_MEMORY_LIMIT_BYTES` 显式配置。每个 receipt 保存阶段 telemetry、query/model hash、bound、native state/transition/variable 计数、失败阶段、deadline、实际耗时和资源终止原因。worker 被终止、超时、内存超限或抛出 backend exception 时，父进程必须写出 terminal failure receipt；失败不是 `false`，不构成 W2、D1/D2 或 violation。

V5 的有限 invariant 允许 counterexample-first incremental execution。请求 horizon 为 `H` 时，任何 `h < H` 的 replayed `false` trace 都是 `H` 的有效反例，可记录 `requested_horizon`、`witness_horizon` 后提前结束；任何 `h < H` 的 `true` 都不能证明 `H`，必须继续到 `H` 或在共享全链路 deadline 后按 W1/W0 退化。不得把 V5 静默固定为 bound=1。

W2 的归因链至少包含当前 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、model hash、编译后的 assertion/formal program、program hash 与真实 receipt。bibliography 只作为冻结谓词的 academic provenance metadata 留在 registry 和 audit bundle。

## 3.1 主 route 的输入闭包与 A/B

主链固定为 `typed contract -> compatible predicate set -> exact input binder -> compiler -> native backend`。route 只可读取当前 pair 的 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、working contracts 与封闭 `ModelIR`；不得读取 ledger expected、Judge、答案、其他 pair 输出或 `pair_id` 特判。

- R1 只在一个 exact transition carrier、一个 exact event、唯一 native cold entry、唯一直接无 guard event carrier 都闭合时，构造 method-owned cold-start event queue、schedule 和 macrostep；不补造 guard valuation、并发调度或 event identity。
- R4 只接受 requirement 明示的 `scenario=cold` 与 `window=cold_macrosteps=N`（`N <= 32`）。自然语言中的 `until`、`while` 或开放时间短语不能被转换成 interval，必须以 `input_contract_missing` 或 `out_of_fragment` 留作 W1。
- V1 必须同时闭合一个 native same-source/same-event guarded choice group、与该 group 完全相等的 exact carrier 集，以及 requirement 独立声明的有限 JSON `domain`。domain 不得从 guard、变量观察值、fixture、台账或答案推断。

主 route 修改必须先在保存的 extraction/grounding/candidate 上做 provider-free A/B。当前有效 A/B 制品为 `evidence-discovery-15x1-primary-route-replay-05699769/f993bb21aa5c39e8a93f8ba1899c29e9`：cohort 固定为历史最终 `predicate_id=null` 的 88 条 W1 evidence，不是较宽的 `execute_batch` 辅助候选集；provider/Judge 调用均为 0，确定性结果为 20 条完成路由、其中 17 条 W2。它只度量 route/execution/W 的确定性变化，不是 hit、precision 或 Judge 指标。

## 4. 实验与评测隔离

route 只能基于当前 pair 的 typed contract、compatible predicate set、exact input binder 和封闭模型。它不读取 ledger expected、Judge relation、答案或 pair ID 特判。supporting pass probe 只用于审计，不能当作 finding、FULL hit 或 W2 violation。

Judge 在独立 evaluation 路径执行，保持冻结口径；method 与 Judge 的 artifact 物理分离。15-pair 与 54x3 运行均须保存 immutable run identity、source commit、prompt/schema/registry/input hash、完整成本与 terminal cell receipt。先做 provider-free replay，后做一次新 15x1；只有协议、typed/backend 和小规模 gate 稳定后才启动 54x3。

## 5. Public implementation language

Public implementation language: provider prompts、Pydantic class docstrings、Field descriptions、production class/function/variable names、registry text、generated explanations 与 deterministic audit prose must be English；本中文协议不进入 provider prompt。Exact source quotations 可保留原文。Provider-free tests 必须检查 W 状态、native backend、失败退化、归因闭合和无答案泄漏。
