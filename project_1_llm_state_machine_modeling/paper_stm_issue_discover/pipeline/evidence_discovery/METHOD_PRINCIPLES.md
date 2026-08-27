# 方法原则

## 1. 冻结边界

`four-family-19-core.v1` 的 19 个谓词均已完成学术资格审查。注册表冻结的是定义、最小 typed contract、来源 metadata、soundness fragment 和 backend 实现义务，不是某次运行的结果。不得新增谓词或修改冻结定义；也不得以成本、台账覆盖率、单个 pair 或文献管理标签把无关语义挂到邻近谓词。

bibliography metadata 只解释“为什么该谓词在学术与领域叙事中成立”。运行时只回答“该谓词是否在当前制品上以合法输入真实执行”。两者正交；来源管理信息不得影响 W、backend、D 或 publication。

## Provider-Free Probe Replay

`execution_probe_replay` 是独立的第四个 provider-free cohort：它只使用保存的 extraction/grounding 重建当前 production deterministic chain，并审计本次新物化的 `DomainInvariantContract`/transition-group execution probe。每条记录必须标明该 contract ID 是否已经存在于 source `execute_batch.candidates`。新增 `false` 只证明当前 native route/backend/audit 已闭合，不能倒写为历史 candidate、publication、hit 或 precision，也不能与 route/frontier/structural/W-state replay 的 W 或 receipt 相加。

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

所有 Pydantic model 都必须有 class docstring 和 Field description；所有结构化模型输出、失败、退化与未执行记录都必须有非空 `reason` 与 `basis`。S4 的 `phase` 只能是 `entry`、`do` 或 `exit`；S2 必须检验 owner-local scope；S5 比较原生 guard AST；S6 只检验 exact transition 的 effect membership。S5 的 `guard=""` 是“要求 absence of guard”的合法显式 typed 值，`guard=null` 才是未绑定输入。pyfcstm 可解析为 Event 的条件必须以 `event`/`trigger` 绑定，绝不能作为 S5/V1 的 `guard`；角色无法由当前原生 carrier 闭合时保留 W1。

结构事实必须从 `pyfcstm.model` 的原生 model class 读取，不能由 ModelIR 或字符串近似判断。轨迹必须由 `SimulationRuntime` 在 method-owned closed scenario 中运行。有界检查必须使用 `.fbmcq` compile/solve/witness/replay，不得手写守卫计算、图遍历替代 solver、赋值枚举或静态 trace。后端不得调用 Python `inspect`。

### FCSTM 单一语义源

FCSTM DSL 的唯一语义权威是 `pyfcstm` 的原生 parser、AST、`StateMachine`、`State`、`Event`、`Transition`、topology、`SimulationRuntime` 与 `.fbmcq`。兼容名称 `parse_fcstm` 只调用原生 loader；`ModelIR` 是原生对象的 Pydantic compatibility projection，不是第二套 grammar 或 execution model。它保留 canonical state/event path、owner/path、pseudo-state、lifecycle action、authored forced/combo carrier provenance、source span 与唯一 historical-ref compatibility mapping。

任何涉及 FCSTM 的 state、event、transition、scope、initial/final pseudo-state、trigger、guard、effect、lifecycle action、reachability、choice group、runtime scenario 或 typed carrier resolution，都必须消费上述原生对象或其 native-derived projection。禁止正则、`splitlines`、brace stack、字符串切片或手写 parser 重新解释 FCSTM source；不得用 ModelIR 图遍历替代 pyfcstm hierarchy、forced/combo、runtime 或 `.fbmcq` 真值。文本处理只允许用于非 FCSTM 的 run/ref/hint 格式、provider framing、PlantUML/source attribution；不得决定 FCSTM 语义。

每次冻结前运行 `python -m pipeline.evidence_discovery.inputs.native_projection_audit --report-root pipeline/representation/reports/llms_emp_r45_java_60 --output <immutable-run-artifact>/fcstm_native_projection_audit.json`。gate 要求 60/60 native source load、54/54 frozen input closure、逐项 projection parity 和零 unapproved text handling；source line 仅作 attribution，不能作为完整 carrier identity。

`.fbmcq` 的完整原生链 `native load -> query prepare -> core build -> property compile -> solve -> decode -> replay` 必须在可终止 worker 内运行。父进程的 wall-clock deadline 与 RSS 安全上限覆盖每个阶段；solver 的局部 `timeout_ms` 只覆盖 solve，不能被误写成全链路 timeout。默认上限为 15 秒、2 GiB，且只可通过 `EVIDENCE_FBMCQ_WALL_CLOCK_TIMEOUT_MS`、`EVIDENCE_FBMCQ_MEMORY_LIMIT_BYTES` 显式配置。每个 receipt 保存阶段 telemetry、query/model hash、bound、native state/transition/variable 计数、失败阶段、deadline、实际耗时和资源终止原因。worker 被终止、超时、内存超限或抛出 backend exception 时，父进程必须写出 terminal failure receipt；失败不是 `false`，不构成 W2、D1/D2 或 violation。

V5 的有限 invariant 允许 counterexample-first incremental execution。请求 horizon 为 `H` 时，任何 `h < H` 的 replayed `false` trace 都是 `H` 的有效反例，可记录 `requested_horizon`、`witness_horizon` 后提前结束；任何 `h < H` 的 `true` 都不能证明 `H`，必须继续到 `H` 或在共享全链路 deadline 后按 W1/W0 退化。不得把 V5 静默固定为 bound=1。

D adjudication 不得把 backend receipt 的原始大对象重复送入模型。完整 `.fbmcq` 公式、solver dump 与其他 raw execution payload 永久保留在不可变 execution/audit receipt；D 的 semantic dossier 只携带 typed candidate/binding/plan、terminal verdict、replay witness/trace、算法与阶段 telemetry，以及 raw payload 的 canonical hash、字段名和字符数。这里的“完整 dossier”指每条义务的语义判定事实完整且不被截断，不表示把可由 hash 回指的原始 SMT 文本复制进 prompt。

D dossier 按 `obligation_id` 稳定排序，并按实际序列化字符数在 provider 调用前装入有限批次。单批上限最多按 40,000 estimated tokens 计算，同时受当前 profile context window 的 65% 减去 output/schema reserve 约束；禁止依赖运行时 compact 挽救超预算输入，禁止静默裁剪或拆开单条 dossier。某一完整 dossier 单独仍超预算，或某一批 provider/schema 调用失败时，只将该批 obligation 明确退为 `D_UNRESOLVED`，保留 batch ID、prompt size、budget、call/failure receipt、reason 和 basis；其他成功批次的 D 结果不得被覆盖或重跑。targeted correction 的唯一输入集合为 `repair_ids = missing_ids ∪ duplicate_ids ∪ invalid_decision_ids`，每个 `repair_id` 必须恰好返回一次，不得把“missing IDs”误写为整个修复集合，并遵守相同预算与稳定合并规则。

`SemanticAdjudication` 的 `defeater_evidence_refs` 是存活 alternative 的强制证据链。每个 D dossier 都给出只属于当前 obligation 的 exact catalog（candidate/binding 的 native model ref 与 source ref）。`undercutting` 或 `rebutting` 标为 `survives` 时必须至少引用一个 catalog token；没有具体、可绑定、与当前 closed facts 兼容的替代实现，不能以“或许有隐藏机制”压制 candidate。`none` 不能携带该引用。缺引用、重复引用或引用 catalog 外 ID 都进入既有 targeted D correction；仍不能修复时只退 `D_UNRESOLVED`，绝不把自由文本当成 rebuttal。

W2 的归因链至少包含当前 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、model hash、编译后的 assertion/formal program、program hash 与真实 receipt。bibliography 只作为冻结谓词的 academic provenance metadata 留在 registry 和 audit bundle。

## 3.1 主 route 的输入闭包与 A/B

主链固定为 `typed contract -> compatible predicate set -> exact input binder -> compiler -> native backend`。route 只可读取当前 pair 的 NL、PlantUML、canonical source IR、FCSTM、inspect-equivalent facts、working contracts 与封闭 `ModelIR`；不得读取 ledger expected、Judge、答案、其他 pair 输出或 `pair_id` 特判。

每次 successful live primary contract extraction 都只执行一次 in-node `contract_completion` property-coverage pass。contract 数与 numbered-NL segment 数之间的关系不是属性覆盖证明：同一段可以同时建立 cardinality/member-set、owner/local entry、source/target、event、guard、effect/output、lifecycle、coverage、transition-group、progress 或 termination 等彼此独立的义务。correction 只可追加当前 NL 独立建立的 `NLContract` 或完整 `NLTransitionGroup`；runner 以完整 typed semantic key 去重并生成 canonical ID，既有 primary contract/group 永不被重写、删除或以同义文字覆盖。正常的 admitted 或 semantic duplicate 只作为 merge audit，不使 cell 产生 diagnostics；未知 segment 或 canonical-ID collision 才是诊断。correction 失败只保留 primary plan 与 failure receipt，不补造合同。该阶段不读台账、Judge、答案、旧 report 或其他 pair，且其新增 contract 必须经过正常 grounding、route、W/D/publication 链，不能直接算 hit。

已带 predicate label 的候选不享有绕过权：S2--S6 一律由同一 exact input binder 重建 native state path、owner scope、authored transition carrier、lifecycle slot 与 guard/effect AST 输入。`state:<name>:line:<N>` 等 projection ref 只用于 binding/audit attribution，绝不是 pyfcstm backend 的 state argument；旧字段（例如 `expected_guard`）也不得直接进入执行。重绑不能闭合时清除执行计划，保留精确 W1 和完整 route reason/basis，禁止把历史输入、timeout 或 parser 兼容猜测伪造成 `false`/W2。

保存制品重放按 cohort 物理隔离：`route_replay` 只审计最终 predicate-null W1 的当前主 route；`frontier_replay` 只审计保存的 frontier 输入；`structural_rebind_replay` 只审计已选择 S2--S6 在当前 native binder 下是否仍具备合法输入。三者都不得读取 ledger expected、Judge、答案或其他 pair，均不产生 hit、precision、publication 或 Judge 结论，W 分布也不得互相相加。`route_replay` 与 `structural_rebind_replay` 都必须在 route 前合并 immutable `execute_batch.frontier_batch` 中的 typed obligation contracts，这与 production runner 的输入顺序一致；不得把这类已保存、可验证的契约误记为 contract absent。历史制品若含已因 soundness audit 移除的 frontier kind（当前为 `wrong_scope_route`），replay 只可显式排除并计数，不能放宽生产 `FrontierBatch` schema、重写原制品或把它恢复为当前 frontier。对没有保存 extraction/frontier contract 的 selected structural probe，replay 只可在候选 `source_refs` 与 `contract_id` 合并后唯一解析出同一个真实 `NL...` segment 时，从其完整保存 typed input 重建 replay-only contract；跨段、冲突或缺失 segment 一律标为 `unavailable` 并退化，禁止默认写成 `NL1`。`initial_entry` 重建为 `must_enter`，`transition_endpoints` 为 `must_exist`，`trigger_set`/`guard` 为 `must_equal`，`state_action`/`effect` 为 `must_occur`。当前 structural-rebind 制品 `c9b461924c636ae6a92809b117934be9` 固定审计 108 条保存的 selected-structural candidates：57 条具备 W2 audit bundle，16 条 route/input 未闭合、35 条 execution-degraded，合计 51 条退化为 W1；provider/Judge 调用均为 0，历史 `wrong_scope_route` 显式排除 4 条。这是历史输入的 typed-safety 对拍，不是一次新的 method 效果。

inspection-equivalent、verify、SMT 与 native topology 只提供当前制品的观察事实，不能自行创造 source-side 的 NL 规范义务。唯一受控例外是预先冻结、带 authority 的 `DomainInvariantContract`：它的规范义务来自领域规则，native fact 只将该规则绑定到当前精确 carrier。当前冻结的 `uml_initial_pseudostate_outgoing_unconditional` 可把原生 `INITIAL_ENTRY_CONDITIONAL` 投影为 exact-carrier S3（要求 `triggers=[]`）或 S5（要求 `guard=""`）候选；同一 carrier 的 S2 endpoint satisfaction 既不能否定也不能抑制该 trigger/guard issue。每一个唯一闭合到 native carrier 的 transition-group event alternative 都须独立执行 S3；仅完全相同的 `(transition_ref, required_trigger_set)` 可以去重，任一 completed/true receipt 仅审计自身，不能中止或抑制其他 alternative。除该类显式冻结领域不变量外，`INITIAL_ENTRY_CONDITIONAL` 仍须有同属性 NL contract 才可形成 NL initial-entry finding；containment、cardinality、state action 或泛 scope contract 只能作为审计上下文。相同地，同 event/guard 多目标事实只有在 NL 已明确 `guard_disjointness` contract 时才可形成 V1/guard-disjointness frontier；不得从任意 scope、事件消费或 action contract 推出互斥义务。未被同属性 contract 或冻结领域不变量规范化的 native fact 必须保留 audit，而不是发布候选。

termination 的 source/owner 与 explicit target 是两个独立 typed role。`HighwayMode -> FinishState` 一类合同允许 `FinishState` 位于 owner 的外层、同层或其他明确 scope；target ancestry 不能自行制造 `route_avoidance`/wrong-scope candidate，也不能把完成目标改写为 owner-local state。只有合同自身声明的 endpoint、termination 或其他冻结可表达属性才可进入后续 route。

LLM 已填写的 `predicate_id` 也不是执行准入。尤其 S4 与 S6 必须由同一 exact input binder 重建：S4 只能闭合为独立的 native state、`entry/do/exit` lifecycle slot 和 action；S6 必须闭合为 exact native transition carrier 与可由 pyfcstm operation grammar 解析的单一 effect。任一项未闭合时清除该执行计划，保留原精确语义候选为 W1；不得把自然语言动作、事件名、状态名或业务阶段当作 action/effect/phase 执行。

R4 的默认 method-owned fragment 也不得伪造 trace：它只接受精确 retained state 的唯一最短 native cold-entry event prefix，再追加一个零事件 macrostep；全部 event queue、schedule、interval 与实际 active state 均由 pyfcstm `SimulationRuntime` 重放。多个同长路径、guard/运行失败、超出小型 event vocabulary/bound 或未到达目标时不选择方便样本，保留 W1。显式 `scenario=cold` 与 `window=cold_macrosteps=N` 仍按其原样闭合。

- R1 只在一个 exact transition carrier、一个 exact event、唯一 native cold entry、唯一直接无 guard event carrier 都闭合时，构造 method-owned cold-start event queue、schedule 和 macrostep；不补造 guard valuation、并发调度或 event identity。
- R4 有两条彼此独立的合法闭包：requirement 明示 `scenario=cold` 与 `window=cold_macrosteps=N`（`N <= 32`）时，按该严格 typed control 构造 cold window；否则只可尝试精确 retained state 的唯一最短 native cold-entry prefix 加一个零事件 macrostep。自然语言中的 `until`、`while` 或开放时间短语只是语义限定，不能自行转换成 interval，也不能阻断后一条已由 native runtime 唯一闭合的路径。若两条均不能闭合，才以 `input_contract_missing` 或 `out_of_fragment` 保留 W1。
- V1 必须同时闭合一个 native same-source/same-event guarded choice group、与该 group 完全相等的 exact carrier 集，以及 requirement 独立声明的有限 JSON `domain`。domain 不得从 guard、变量观察值、fixture、台账或答案推断。

15-pair 的固定 planned 分母仅为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4。selection preflight 只记录这 12 个冻结谓词的通用 typed contract、当前输入 hash 和预注册语义形状；它不含 ledger、expected issue、Judge、答案、D/L、hit 或 precision 字段，且 worker 只将其 hash/reference 写入 immutable manifest，绝不读取它来生成 candidate、绑定值、route 或 backend 输入。其余 7 个冻结谓词未进入本次 planned 分母不影响其学术资格或 19/19 backend 义务。

54x3 的固定 planned 分母是 S1、S2、S3、S4、S5、S6、G1、G2、G3、G4、R1、R2、R4、V1、V4，共 15 个，与冻结 registry 中非零 planned mapping 一致。该分母与 15-pair 的诊断 12 分母分别记录；不得用实际 terminal execution 集合反向缩小。特别是 G2、G3、R2 没有执行时必须报告 route/typed-input stage-loss，不能写成“不在全量计划内”。任意 54-pair 后续修复子集都必须显式沿用 `full-scale-15`，不得因子集规模为 12--15 pair 自动退回 `diagnostic-12`。

`backend_missing` 只表示冻结谓词没有真实 dispatch/backend 实现；当前 19 个冻结谓词均有 backend，因此该值应为 0。某个 receipt 的 `failure_kind=invalid_input` 必须计入 `input_contract_missing`；backend 已实现但输入落在 soundness fragment 外时计入 `out_of_fragment`，同时原样保留 receipt 的 `failure_kind` 分布。不得再因为 receipt 的展示 backend 为 `none`，就把 V1/S6 的非法 domain/effect 或其他输入闭包失败写成 backend 缺失。

全量主 route 对新增计划项采用保守 native 闭包：G2 只接受 exact source/target；source 可以已经是 pyfcstm leaf，也可以是每一层都恰有一条 `State.init_transitions`、最终唯一下降到 leaf 的 composite。多 initial、无 initial、循环或目标不属于当前 owner 时不得任取 leaf，继续 W1。G3 只接受 exact leaf source、target、forbidden。R2 只接受 typed transition alternative、唯一 canonical author-source carrier、exact native event 和 exact target 同时闭合的输入；其 method-owned schedule 从 cold `SimulationRuntime` 枚举至多 3 个事件的唯一最短 stimulus-consuming prefix，再追加一个空 observation macrostep。前缀选择函数不接收 target state，target truth 只由 R2 backend 在真实 trace 上判断。非唯一、未消费、并发或运行失败均保留 W1，不制造 schedule 或 verdict。

主 route 修改必须先对每个固定输入 cohort 做彼此独立的 provider-free A/B，不得混算。保存 candidate replay 的 cohort 固定为源 run 最终 `predicate_id=null` W1 evidence；当前制品 `evidence-discovery-15x1-native-route-replay-3dec97be4/479bb22f064ec72327b422b57cfbd0cb` 读取 source run `7140b9c7a4f1c8ee6902b600e47a60c3` 的 51 条该类 evidence，0 provider/Judge 调用，当前 route 合法完成 3 条 W2（S2=2、R4=1），其余 48 条保持 W1。它先合并保存的 typed frontier contracts、但不重物化 frontier，也不是 hit、precision 或 Judge 指标。

`route_replay` 同时保存两种不可混用的 route telemetry：`route_telemetry.json` 是 contract 级 coverage 汇总，回答“该 contract 是否至少有一条候选闭合”；每个 replay record 的 `route_telemetry` 与 `candidate_route_telemetry.json` 是 source candidate index 对齐的逐候选决策，回答“这一条候选实际是否闭合”。逐 evidence 的 W、stage-loss、execution 或 publication 审计只能使用候选级记录；contract 级成功绝不能为同 contract 的另一条未闭合候选生成 predicate、receipt 或 W2。

保存 extraction/grounding 的 deterministic frontier replay 使用独立制品 `evidence-discovery-15x1-frontier-replay-current/0f9d383071b29a11eb0474d655553706`。它复用 runner 在 frontier 前的确定性归一化链，15/15 pair 当前 frontier 成功，保存运行中的 1 个 frontier error 清零，typed identity 为 added=40、removed=0；新增结果为 W2=13、W1=27，0 provider/Judge 调用。22 条 `state_after_stimulus` 中 10 条形成 R2 completed/true satisfaction receipt；0039 恢复的 guard frontier 仅 1 条 S5 completed/false，其余非法输入退 W1。该制品只证明 frontier/route/backend 的确定性变化，不重建 publication、D、Judge 或 FULL hit。

## 4. 实验与评测隔离

route 只能基于当前 pair 的 typed contract、compatible predicate set、exact input binder 和封闭模型。它不读取 ledger expected、Judge relation、答案或 pair ID 特判。supporting pass probe 只用于审计，不能当作 finding、FULL hit 或 W2 violation。

当前优化主指标是外置 Judge 的 exact FULL hit 与 report claim 完整性，而不是单纯增加 pass receipt、W2 数量或 predicate usage。15-pair 固定 planned 分母仍为 12；已达到 12/15 即为稳定合格，后续不得为了追逐低频 13--15/15 而扩大 unsafe route、堆 supporting pass probe、牺牲 exact binding 或延后 hit 修复。发布报告必须保留 violated obligation、exact carrier/locus、完整 member set/count、owner/source/target、event/guard/effect/action role、repair delta、reason 与 basis；粗粒度 predicate 的 `true` 只证明它自身命题，不能删除不同 property/role/scope 的精确 candidate。

Judge 在独立 evaluation 路径执行，保持冻结口径；method 与 Judge 的 artifact 物理分离。15-pair 与 54x3 运行均须保存 immutable run identity、source commit、prompt/schema/registry/input hash、完整成本与 terminal cell receipt。新的 live run 默认以 `--workers 16` 启动，并在 manifest 固定实际并发、限流和 retry policy；provider error 只就地重试受影响调用/cell，修复后只重跑该 cell，绝不通过串行化或重启整个 run 处理局部错误。先做 provider-free replay，后做一次新 15x1；只有协议、typed/backend 和小规模 gate 稳定后才启动 54x3。

外置 Judge 终结后，evaluation 侧使用 `python -m pipeline.evidence_discovery.reporting.expected_issue_witness` 生成 `expected_issue_witness_audit.json`，使用 `python -m pipeline.evidence_discovery.reporting.judge_cost_audit` 生成 `judge_cost_audit.json`，再使用 `python -m pipeline.evidence_discovery.reporting.evaluation_summary` 生成 `evaluation_summary.json`。前者逐 expected issue 保存 `FULL/PARTIAL/NONE`、匹配 report 的 predicate/W/D、完整 typed/backend/receipt 链、`max_W` 和 `contract extraction -> identity binding -> predicate route -> typed inputs -> backend -> W -> D -> publication -> Judge relation` 的 stage-loss；成本审计逐个保留 unpriced billable call、provider/non-provider retry 和 schema retry，严禁把 provider 缺失 usage 估算为精确成本或伪装成语义失败；后者将 FULL hit、W2/全部 expected、每 pair hit/max-W/D/precision/INVALID/route-stage loss、predicate feasibility、W2 closure 和成本分母分别固定。三者输入只能是不可变 method/Judge artifact，不能作为 prompt、binding、route、execution、W、D、publication 或 preflight 的任何条件。

若冻结 Judge adapter 只接受 `completed + eligible=true`，而 method terminal schema 允许 eligible diagnostic 或 ineligible failure，evaluation 只能建立独立 compatibility projection。eligible diagnostic 的 published report payload 必须保持不变；ineligible failure 必须变为空发布面并保留固定 expected 分母，不能评估其 cluster。投影必须用 Pydantic audit 记录原始/投影 hash、status、eligible、report count、reason 和 basis；原 method artifact 与 Judge 代码均不可改。pair-local 恢复产生新 method sample 时，必须先用 `reporting.method_composite` 建立 source-explicit 单一 method root：replacement 必须保持同一 pair/round 与 input hash。若 recovery sample 包含同 pair 的非失败 round，composite 必须使用显式 replacement-key 白名单，未替换 cell 和 W2 bundle 逐字节硬链接，未选 recovery cell 仅计入 total-incurred cost；每个 source pair status 也必须按 source-run 分区硬链接，并由 manifest 的 round-to-source 映射审计，禁止合成或冒充一个跨 source pair status。分别报告 selected、superseded、total-incurred cost 以及 retry/schema-repair；不得把新 sample 伪称为旧 candidate 的 stage-only replay。随后才可做 Judge compatibility projection。若 Judge 本身分批恢复，再由独立 Judge composite 闭合每个 result/source hash、失败、retry 和成本。

## 5. Public implementation language

Public implementation language: provider prompts、Pydantic class docstrings、Field descriptions、production class/function/variable names、registry text、generated explanations 与 deterministic audit prose must be English；本中文协议不进入 provider prompt。Exact source quotations 可保留原文。Provider-free tests 必须检查 W 状态、native backend、失败退化、归因闭合和无答案泄漏。
