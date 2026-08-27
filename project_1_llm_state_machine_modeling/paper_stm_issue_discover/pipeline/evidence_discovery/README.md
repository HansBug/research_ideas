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

provider-free replay 也必须按输入 cohort 隔离。`route_replay`、`frontier_replay` 与 `structural_rebind_replay` 分别审计 predicate-null route、保存 frontier 与保存的 selected S2--S6 native rebind；它们不调用 provider/Judge，不读评估答案，也不报告 hit、precision 或 publication。不得合并这些 replay 的 evidence/W 数，或把某个 replay 的 W2 当作新的 method finding。`route_replay` 与 `structural_rebind_replay` 都必须在 route 前合并 immutable `execute_batch.frontier_batch` 中的 typed obligation contracts，严格复用 production runner 的输入闭包；只有无保存 extraction、grounding、frontier 或合法 replay-only contract 时才可记为 route-unclosed。`route_replay` 的 `route_telemetry.json` 是 contract 级覆盖汇总，只能说明同一 contract 是否存在至少一条可闭合候选；逐 evidence 判断必须读取 record 内与 source candidate index 对齐的 `route_telemetry`，并可在 `candidate_route_telemetry.json` 复核。禁止把同 contract 的另一候选 route/W2 归因给当前候选。历史保存 frontier 若含已移除的 `wrong_scope_route`，replay 只排除并在 summary 计数；生产 schema 继续拒绝该 kind，不能为兼容旧制品重新启用。selected structural probe 若未保存 contract，只能从 `source_refs` 和 `contract_id` 唯一闭合真实 `NL...` segment 后重建；跨段或不唯一 provenance 必须 `unavailable`，不得默认 `NL1`。最新 selected-structural replay 为 `c9b461924c636ae6a92809b117934be9`：108 条固定 cohort 中 57 条 W2 有 audit bundle，16 条 route/input 未闭合、35 条 execution-degraded，0 provider/Judge 调用；其完整 manifest、records、failure audit 与 W2 bundles 位于独立 immutable run artifact。

`.fbmcq` 的 native load、query prepare、core build、property compile、solve、decode 和 replay 全部在可终止 worker 中运行。父进程执行全链路 wall-clock deadline 和 RSS 安全上限，默认分别为 15 秒与 2 GiB，可通过 `EVIDENCE_FBMCQ_WALL_CLOCK_TIMEOUT_MS`、`EVIDENCE_FBMCQ_MEMORY_LIMIT_BYTES` 显式配置；`timeout_ms` 仅是 solver 内部预算，绝不能代替前两者。回执保存每一阶段的开始/结束/耗时、query/model hash、bound、state/transition/variable 计数、失败阶段和资源终止原因。worker timeout、memory limit 或 backend exception 只生成 terminal failure receipt，并按精确 binding 退化 W1/W0，绝不产生 `false`、W2 或 issue。

V5 `state_invariant` 可从小 bound 递增检查：若较小 bound 得到可 replay 的 counterexample，该 trace 是请求 horizon 内的有效反例，可提前返回 W2 `false`；较小 bound 的 `true` 只是中间进展，必须继续到请求 horizon 或在共享全链路 deadline 后诚实退化。

D 阶段使用 `dossier-prompt-projection.v4`：原始 FBMCQ/SMT 公式和 solver dump 只保存在不可变 backend receipt，prompt 仅保留 canonical hash、原始字段名/字符数、typed plan、真实 verdict、telemetry 与 witness/replay 事实。完整语义 dossier 不做文本截断，并按 `obligation_id` 与实际 prompt size 稳定分批；当前每批最多 40,000 estimated tokens，且还要服从 profile context 的 65% 减去 output/schema reserve。单条 dossier 超限或单批失败只使该批 ID 进入 `D_UNRESOLVED`，不能触发 issue、覆盖成功批次或让整个 cell 挂死；correction 也只处理对应未闭合 ID。`utils.agent` 的 compact fail-closed 保持不变，runner 必须在调用前完成预算控制。

## 主 route 与保存 A/B

主 route 依次执行 `typed contract -> compatible predicate set -> exact input binder -> compiler -> native backend`。它仅使用当前 pair 的 method 输入；ledger、Judge、答案、其他 pair 与 pair-ID 特判都不在输入边界内。

LLM 的预选 `predicate_id` 不构成 typed execution plan。S4/S6 即使已被模型标注，也必须回到 exact input binder：S4 需分别闭合 native state、`entry/do/exit` 和 action；S6 需闭合 native transition carrier 与 pyfcstm 可解析的单一 operation effect。无法闭合时删除 execution plan、保留精确 W1，不得把状态名、业务阶段、事件名或自然语言动作短语伪装为 FCSTM lifecycle/effect 输入。

R4 仅在 exact retained state 有唯一最短的 native cold-entry event prefix 时构造运行输入，并追加一个无注入事件的 macrostep；`SimulationRuntime` 负责重放完整 event queue/schedule/interval。路径不唯一、超出受限 fragment 或 runtime 不闭合均保留 W1，不能用 source trace 或任意 schedule 替代。

- R1 需要 exact event/carrier、唯一 native cold entry 和唯一无 guard direct carrier，才能构造 cold-start event queue、schedule 和 macrostep。
- R4 的显式 typed control 只能是 requirement 明示的 `scenario=cold` 和 `window=cold_macrosteps=N`（`N <= 32`）。开放 prose 时间窗不能自行产生 interval；它也不会阻断已由 exact retained state、唯一 native cold-entry prefix 和 zero-event macrostep 闭合的 method-owned 路径。两种闭包都失败时才保持 W1。
- V1 需要 native same-choice guarded group、完整 exact carrier 集和 requirement 独立给出的有限 JSON `domain`；不得从 guard 或观察到的变量值补造 domain。原生 Event 只能作为 `event`/`trigger`，不能把 Event selector 写成 guard 来构造 S5 或 V1；不能闭合真实 guard AST 时保持 W1。

15-pair 的固定 planned 分母为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4。selection preflight 仅保存这 12 个谓词的通用能力、typed schema、语义形状和输入 hash，不包含 ledger、expected、Judge、答案、D/L 或评测字段；它只以 hash/reference 进入 run manifest，不进入 method worker 的 candidate、binding、route 或 backend 输入。未列入该分母的冻结谓词仍全部具有学术资格和 native backend。

54x3 使用另一套冻结分母：S1、S2、S3、S4、S5、S6、G1、G2、G3、G4、R1、R2、R4、V1、V4，共 15 个。evaluation artifact 必须保存 `planned_predicate_scope` 和完整 ID 列表；全量或其后续代表子集均不得按“本轮实际执行了几个”缩小分母。G2、G3、R2 缺少 terminal receipt 时属于待解释的 route/input closure loss，不属于计划外谓词。

reporting 对可行性采用结构化失败口径：`failure_kinds` 保留原 receipt 分类，`input_contract_missing` 仅计 `invalid_input`，`out_of_fragment` 表示 backend 已实现但当前 typed/soundness fragment 未闭合，`backend_missing` 只表示冻结 ID 没有 dispatch 实现。当前 19/19 backend 均已实现，所以不能再根据 `backend=none` 的展示值把 V1 的非法 finite domain、S6 的 prose effect 或其他未执行计划误报为 backend 缺失。

G2/G3/R2 的 primary route 不靠文本图近似。G2 的 exact source 可以是 native leaf，或经每层恰好一条 `State.init_transitions` 唯一下降到 leaf 的 composite；多 initial、无 initial、循环或 owner/target 不闭合时不得任取 leaf。G3 的 source/target/forbidden 必须是 exact native leaf state。R2 先由 typed transition group、唯一 canonical source carrier 和 native Event 形成 event/target identity，再用 `SimulationRuntime` 搜索唯一最短、最多 3 个事件的 stimulus-consuming cold prefix并追加一个空观察步。搜索不接收或检查 target state，target 仅由 R2 backend 在真实 trace 上求值；任何歧义或运行失败保持 W1。

provider-free A/B 至少按 predicate-null route、保存 frontier 与已选 structural rebind 三个不可互换 cohort 落盘。当前 predicate-null route 制品为 `evidence-discovery-15x1-native-route-replay-3dec97be4/479bb22f064ec72327b422b57cfbd0cb`：它读取 source run `7140b9c7a4f1c8ee6902b600e47a60c3` 的最终 51 条 `predicate_id=null` W1 evidence，先合并 immutable typed frontier contracts，再以当前 native route/backend 得到 3 条 W2（S2=2、R4=1）与 48 条 W1，0 provider/Judge 调用，不重物化 frontier。`evidence-discovery-15x1-frontier-replay-current/0f9d383071b29a11eb0474d655553706` 只重放保存 extraction/grounding 与 runner 的 deterministic prefrontier chain：15/15 frontier 成功，旧 frontier error 从 1 降为 0，added=40、removed=0，新增 W2/W1=13/27。三者均不是 hit、precision 或 Judge 评测。

## 隔离与审计

method 只读取当前 pair 的 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、working contracts 与封闭 ModelIR。它不读取台账 expected、L、Judge、答案、其他 pair 或未来结果。Judge 是独立 evaluation 层，冻结口径不参与 method 的 W/D/candidate。

每个 W2 的 `audit_bundle` 必须闭合：typed inputs、compiled program/hash、backend/algorithm version、真实 result、receipt hash、NL/PlantUML/canonical IR/FCSTM/facts/model 的当前制品归因、reason、basis 和 retry/billing。完整运行还保存 immutable run ID、source commit、prompt/schema/registry/input hash、实际 worker 数与成本。后续新启动的 method、Judge 及可并行审计默认使用 `--workers 16`；已闭合或正在执行的 run 不得为调整并发而重启、覆盖或混入新版本。

method 制品冻结且外置 Judge 完成后，evaluation 路径必须生成 `expected_issue_witness_audit.json`、`judge_cost_audit.json` 和 `evaluation_summary.json`。前者逐条保留每个 expected issue 的 `FULL/PARTIAL/NONE`、匹配 report ID、每个匹配报告的 predicate/W/D、typed/backend/receipt 链、`max_W` 与未命中的 stage-loss；`judge_cost_audit.json` 保留每个 unpriced billable call、provider/non-provider retry 与 schema retry，禁止把缺失 provider usage 估计成精确成本；后者将 FULL hit、W2/全部 expected、每 pair hit/max-W/D/precision/INVALID/route-stage loss、19 谓词 feasibility、W2 closure 和成本分别汇总。它们只读取不可变 method/Judge artifact，不能进入 method prompt、binding、route、backend、W、D 或 publication。

冻结 Judge adapter 与 method terminal status 版本不一致时，只能生成独立的 evaluator-only compatibility projection：`completed_with_diagnostics + eligible=true` 可将状态规范化为 `completed`，但 published report payload 必须逐值不变；`failed_with_receipt + eligible=false` 只能投影为空发布面，使固定 expected 分母产生 `NONE`，原 cell 中的任何 cluster 都不得进入 Judge。未变 cell 使用 hash 相同的硬链接，全部投影保存原始/投影 hash、status、eligible、report count、reason 与 basis；原 method JSON、Judge 代码和 Judge 语义均不可修改。若只恢复一个 method pair/cell，先用 `python -m pipeline.evidence_discovery.reporting.method_composite` 生成 source-explicit 单一 method root；它只接受同 pair/round、同 input hash 的 replacement。若 recovery run 为了形成完整 sample 而包含同 pair 的其他 round，必须显式传入 `--replacement-key 0004:r3` 这类白名单，只替换诊断过的 key；未选的 recovery cell 不进入结果指标但仍计入 total-incurred cost。所有选中 cell 和所有原始 pair status 都以 source-run 分区硬链接，composite manifest 逐 pair 记录 round-to-source 映射，禁止伪造一个跨 source 的 pair status。保留 base/recovery source commit、retry/schema-repair 和 selected/superseded/total-incurred cost，不能把完整 cell 重跑写成 stage-only replay。Judge 分批恢复时再用 Judge composite 闭合每个结果。54x3 expected position 分母始终固定为 435。

详细规则见 [METHOD_PRINCIPLES.md](METHOD_PRINCIPLES.md)、[PREDICATE_REGISTRY.md](PREDICATE_REGISTRY.md)、[REFACTOR_PLAN.md](REFACTOR_PLAN.md) 和 [POLICY_REVIEW.md](POLICY_REVIEW.md)。
