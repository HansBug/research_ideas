# 实施与收敛计划

## 固定协议

实现维持 `four-family-19-core.v1`、冻结 Judge 与独立 evaluation。19/19 谓词 backend 必须真实可调用、可终止并返回 `true` 或 `false`；某次 pair 无法闭合输入只能形成 W1/W0 execution audit，不能改变谓词资格或缩小 planned 分母。`utils.agent`、`utils.llm`、既有 LangGraph、缓存和成本基础设施继续作为唯一调用路径。当前真实运行 profile 为 `gpt-5.6-luna`。

## 阶段 A：确定性协议与 conformance

1. 使用三档 W 状态机和正交 execution audit；bibliography 不进入任何运行时分支。
2. 为 19 个谓词维护 positive、negative、invalid-input、out-of-fragment、timeout/error fixture，并验证 backend dispatch。
3. S1--S6 使用 FCSTM model class；G 类使用 native topology/FBMCQ；R 类使用 `SimulationRuntime`；V 类使用 `.fbmcq` compile/solve/witness/replay。FBMCQ 的 native load、prepare、core build、property compile、solve、decode 和 replay 均在可终止 worker 内运行；父进程执行 wall-clock/RSS 边界并生成 terminal failure receipt。V5 仅能以 replayed lower-bound counterexample 提前返回，不得把 lower-bound pass 当成目标 horizon satisfaction。
4. 每次 W2 写入 typed input、编译后的 assertion/formal program、code/hash、真实 result、backend version、artifact attribution、reason、basis 与 receipt hash 到 `audit_bundle`。
5. provider error 原调用重试且不计费；schema、解析、业务和其他 retry 均计费并修复根因。禁止 Python `inspect`。
6. FCSTM 只允许 `pyfcstm` 原生 parser/AST/StateMachine 作为语义源。`parse_fcstm`/`ModelIR` 必须是 native compatibility projection，保留 canonical path、pseudo-state、owner、lifecycle action、forced/combo provenance、span 与唯一 legacy-ref mapping；禁止恢复或扩展 FCSTM regex/line parser。`native_projection_audit` 必须达到 60/60 source load、54/54 frozen input closure、零 parity difference、零未批准文本处理后才解释 replay 数据。
7. D adjudication 使用 receipt-only raw payload 边界：完整 FBMCQ/SMT 公式留在 execution/audit artifact，D semantic dossier 只携带 hash、size、typed plan、verdict、telemetry 与 witness/replay。dossier 按 obligation ID 和序列化预算稳定分批，不截断单条义务；超预算/失败批次仅退 `D_UNRESOLVED`，其他批次保持，targeted correction 只补对应 ID。不得削弱 `utils.agent` compact fail-closed，也不得用增加 context/retry 掩盖 prompt 投影 bug。

## 阶段 B：provider-free replay

对保存的 method artifact 重算 plan readiness、execution audit、W、D、publication、audit bundle 与 summary，不调用 provider、不修改 report semantic identity。回放必须证明：完成的 true/false 未降级、非法 typed input 无 W2、timeout/error 不是假 violation、每个 W2/退化记录归因闭合。已闭合 Judge relation 仅在 report identity 未变时复用。

## 阶段 C：route A/B 与 15-pair

route 使用 `typed contract -> compatible predicate set -> exact input binder`，只读取当前 pair 的方法输入。先在保存 extraction/grounding 输入上做 provider-free A/B，再以新 commit 和 immutable run identity 运行一次 15x1。固定 12 谓词分母为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4；R1/R4/V1 必须有 method-owned scenario/trace/domain 闭包，不能以 pass probe 代替 finding。

S4/S6 的 LLM 预选标签必须经过同一 binder 复核，不能绕过输入闭包：S4 的 phase 只允许 `entry/do/exit`；S6 的 effect 必须是 pyfcstm native operation grammar 可解析的单一操作并绑定到 exact carrier。S5/V1 也必须先区分 native Event selector 与 guard AST：可解析为 Event 的 requirement value 只能是 `event`/`trigger`，不能借 guard 字段进入错误谓词。失败时只退化执行计划和 W，不改 contract/candidate 语义，不产生 false、W2 或 publication。

R4 的 method-owned runtime closure 固定为受限 native cold-entry fragment：只有精确 retained state 的唯一最短 event prefix 加一轮 zero-event macrostep 才可执行；任何路径歧义、runtime failure 或 fragment 越界均退化 W1。不得从 source trace、台账或人工答案构造 schedule。

R1 的 cold-start execution 必须由 exact event/carrier、唯一 native cold entry 和唯一 direct unguarded carrier 闭合；R4 的显式 typed control 仅接受 requirement 明示的 `scenario=cold` 与 `window=cold_macrosteps=N`（`N <= 32`），但 generic prose window 只能保留语义限定，不能阻断独立的唯一 native cold-entry closure；V1 必须具有完整 native same-choice guarded group、exact carrier 集与 requirement 独立提供的有限 JSON `domain`。不满足时记录 `input_contract_missing`/`out_of_fragment` 并保留 W1，禁止从 prose、guard、fixture 或答案补造输入。

保存数据的 deterministic A/B 不是一次完整 method run。predicate-null route、frontier 和已选择 structural candidate 分别使用 `route_replay`、`frontier_replay`、`structural_rebind_replay`；三种 artifact 的 W/receipt 只能说明各自固定 cohort 在当前实现下的合法性，禁止混算为 hit、precision、execution coverage 或新 finding。已选择 S2--S6 的 replay 必须强制 current exact native rebind；历史 `state:<name>:line:<N>`、carrier ref 或 legacy `expected_guard` 不能跳过 typed binder。保存 frontier 里已被 soundness audit 删除的 `wrong_scope_route` 只能在 replay 读取时显式排除并计数，不能放宽当前 schema 或重启该规则。当前 `eb5820b1151c4271ffd287032da55128` 是该 structural 安全门的已闭合制品，随后仍须以一次新的 15x1 才能验证完整 native context/frontier/routing 链。

selection preflight 的 15x12 表只保存固定 12 谓词的通用 capability/schema、当前输入 hash 与 semantic-shape set cover，不读取或存储 ledger、expected issue、Judge、答案、D/L 或评测结果。run manifest 只保存经校验的 preflight hash/reference；method worker 不消费 preflight 内容。未计划使用不等于学术或 backend 边界，19 个冻结谓词仍全部保留 native backend 和 conformance coverage。

阶段 C 使用两条分离的 A/B。保存 candidate route cohort 只能取最终 `predicate_id=null` W1 evidence；当前代表集 route artifact `280a6ec53b61fb28c775a365247a402b` 含 76 条、0 provider/Judge 调用，当前 4 条 W2，相对源 commit 基线净增 2 条 G2 completed/false。保存 extraction/grounding 的 frontier artifact `0f9d383071b29a11eb0474d655553706` 必须复用 runner prefrontier deterministic chain，当前 15/15 frontier 成功、旧 error 1->0、added=40、removed=0、新增 W2/W1=13/27。前者不重生成 frontier，后者不重建完整 runner；二者均不能取代新 15x1 的独立 method/Judge 验收。

15-pair 的检查包括 15/15 terminal、无 diagnostics、FULL expected 的 max-W2、W2/全部 expected、overall/L2 hit、precision/FP、12 分母 execution、W2 audit closure 和成本。Judge 在 method 完成后独立补齐，不能改 Judge 语义迁就 method。Judge 完成后必须在 evaluation artifact 写入 `expected_issue_witness_audit.json` 和 `evaluation_summary.json`：前者逐 expected 保留 `FULL/PARTIAL/NONE`、匹配 report 的 predicate/W/D、typed/backend/receipt 链、`max_W` 与 stage-loss，后者分别汇总每 pair hit/max-W/D/precision/INVALID/route-stage loss、19 谓词 feasibility、W2 closure 和成本；两者只读不可变 method/Judge artifact，绝不反向进入 method。

## 阶段 D：54x3

新的 15-pair 协议稳定后冻结 current，启动一次并发 54 pair x3。新的 live method/Judge run 默认目标为 `--workers 16`；run manifest 必须固定实际 worker 数、provider 限流与重试策略。provider error 只原地重试受影响调用/cell，修复后只重跑失败 cell，禁止为了局部失败串行化、重启或覆盖其他已闭合 artifact。每个 cell 保存 source commit、prompt/schema/registry/input hash、成本与 terminal receipt。报告 overall/L2 `hit@1`、`hit@3`、`hit@all`、precision、FP、FULL expected max-W2、W2/435、15 个 planned predicate execution 与 cost，并与冻结 baseline 和冻结全量参考结果公平对照。

全量 planned 分母固定为 S1、S2、S3、S4、S5、S6、G1、G2、G3、G4、R1、R2、R4、V1、V4，共 15 个；目标至少 13/15 有真实 terminal receipt。reporting 自动将完整 54-pair universe 解析为 `full-scale-15`，其他代表子集必须显式指定该 scope。不得把 15-pair 的 `diagnostic-12`、候选中出现的 ID、preflight row 或实际执行集合代替全量分母；G2/G3/R2 的零执行必须进入 stage-loss 和输入闭包结论。

full-scale stage-loss 必须区分实现可用性与实例闭包：`backend_missing` 只在 frozen predicate 没有 dispatch/backend 时成立，当前 19/19 实现下应为 0；`invalid_input` 进入 `input_contract_missing`，backend 已实现但 soundness fragment 不满足进入 `out_of_fragment`，并另外保留原始 `failure_kinds`。禁止再用 `backend=none` 这个未执行展示值推断 V1/S6 或其他谓词没有 backend。

G2/G3/R2 的局部 route 修复不改谓词定义和 Judge。G2 只路由 exact source/target；source 已是 leaf 时直接使用，composite 仅在每层恰有一条 native initial transition 并最终唯一下降到 leaf 时执行，绝不任取 leaf。G3 要求 exact leaf source/target/forbidden。R2 要求 typed alternative、唯一 canonical source carrier、exact native event/target，并由 `SimulationRuntime` 在不读取 target truth 的前提下搜索唯一最短、最多 3 个事件的 stimulus-consuming cold prefix，追加一个空 observation step后交给 backend 判断 target。保存输出先做两类分离的 provider-free A/B；未形成这些闭包时继续 W1，不能制造 scenario 或缩小分母。

method terminal schema 与冻结 Judge adapter 的状态词表不一致时，不修改任一原制品。pair-local method 恢复先经 `reporting.method_composite` 建立单一 evaluator root：只替换同 pair/round 且 input hash 相等的完整新 cell。若完整 recovery sample 带有其他 round，必须显式列出 replacement-key，未选 recovery cell 不进入 selected result 但保留在 total-incurred cost；其他选中 method/W2 audit 及按 source-run 分区的 pair status 均保持硬链接字节身份，manifest 记录每个 pair 各 round 的来源，禁止合成跨 source status。source commit、selected/superseded/total-incurred cost、provider retry 与 schema repair 分开闭合；不得把完整重跑描述成原 cell 的 stage-only 重算。之后 evaluation 才建立独立 Pydantic Judge compatibility projection：eligible diagnostic cell 只规范化 adapter status 且 report payload 逐值不变；ineligible failed cell 只提供空发布面，保留固定 expected 分母并产生 `NONE`。Judge 恢复结果另用 Judge composite 对全部 result/source hash、失败、retry 和成本闭合。

若 54 pair 未达 soft gate，先完成 `contract extraction -> identity binding -> predicate route -> typed inputs -> backend -> W -> D -> publication -> Judge relation` stage-loss，选择 12--15 个代表 pair 做一次局部修复；同一版本不得重复抽样刷结果。
