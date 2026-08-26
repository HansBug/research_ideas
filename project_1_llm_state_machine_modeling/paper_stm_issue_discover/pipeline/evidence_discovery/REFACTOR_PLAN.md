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

## 阶段 B：provider-free replay

对保存的 method artifact 重算 plan readiness、execution audit、W、D、publication、audit bundle 与 summary，不调用 provider、不修改 report semantic identity。回放必须证明：完成的 true/false 未降级、非法 typed input 无 W2、timeout/error 不是假 violation、每个 W2/退化记录归因闭合。已闭合 Judge relation 仅在 report identity 未变时复用。

## 阶段 C：route A/B 与 15-pair

route 使用 `typed contract -> compatible predicate set -> exact input binder`，只读取当前 pair 的方法输入。先在保存 extraction/grounding 输入上做 provider-free A/B，再以新 commit 和 immutable run identity 运行一次 15x1。固定 12 谓词分母为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4；R1/R4/V1 必须有 method-owned scenario/trace/domain 闭包，不能以 pass probe 代替 finding。

S4/S6 的 LLM 预选标签必须经过同一 binder 复核，不能绕过输入闭包：S4 的 phase 只允许 `entry/do/exit`；S6 的 effect 必须是 pyfcstm native operation grammar 可解析的单一操作并绑定到 exact carrier。失败时只退化执行计划和 W，不改 contract/candidate 语义，不产生 false、W2 或 publication。

R4 的 method-owned runtime closure 固定为受限 native cold-entry fragment：只有精确 retained state 的唯一最短 event prefix 加一轮 zero-event macrostep 才可执行；任何路径歧义、runtime failure 或 fragment 越界均退化 W1。不得从 source trace、台账或人工答案构造 schedule。

R1 的 cold-start execution 必须由 exact event/carrier、唯一 native cold entry 和唯一 direct unguarded carrier 闭合；R4 的显式 typed control 仅接受 requirement 明示的 `scenario=cold` 与 `window=cold_macrosteps=N`（`N <= 32`），但 generic prose window 只能保留语义限定，不能阻断独立的唯一 native cold-entry closure；V1 必须具有完整 native same-choice guarded group、exact carrier 集与 requirement 独立提供的有限 JSON `domain`。不满足时记录 `input_contract_missing`/`out_of_fragment` 并保留 W1，禁止从 prose、guard、fixture 或答案补造输入。

selection preflight 的 15x12 表只保存固定 12 谓词的通用 capability/schema、当前输入 hash 与 semantic-shape set cover，不读取或存储 ledger、expected issue、Judge、答案、D/L 或评测结果。run manifest 只保存经校验的 preflight hash/reference；method worker 不消费 preflight 内容。未计划使用不等于学术或 backend 边界，19 个冻结谓词仍全部保留 native backend 和 conformance coverage。

阶段 C 的基准 A/B 只能以保存的最终 `predicate_id=null` W1 evidence 为 cohort。当前有效 artifact ID 是 `f993bb21aa5c39e8a93f8ba1899c29e9`（`evidence-discovery-15x1-primary-route-replay-05699769`），包含 88 条 cohort、0 provider 调用、0 Judge 调用、20 条确定性路由和 17 条 W2；历史上使用 113 条辅助 `execute_batch` candidate 的制品不是本阶段指标依据。A/B 仅证明确定性 route 收益，不能取代新 15x1 的独立 method/Judge 验收。

15-pair 的检查包括 15/15 terminal、无 diagnostics、FULL expected 的 max-W2、W2/全部 expected、overall/L2 hit、precision/FP、12 分母 execution、W2 audit closure 和成本。Judge 在 method 完成后独立补齐，不能改 Judge 语义迁就 method。Judge 完成后必须在 evaluation artifact 写入 `expected_issue_witness_audit.json`：每个 expected 保留 `FULL/PARTIAL/NONE`、匹配 report 的 predicate/W/D、typed/backend/receipt 链、`max_W` 与 stage-loss；该制品只读不可变 method/Judge artifact，绝不反向进入 method。

## 阶段 D：54x3

新的 15-pair 协议稳定后冻结 current，启动一次并发 54 pair x3。每个 cell 保存 source commit、prompt/schema/registry/input hash、成本与 terminal receipt。报告 overall/L2 `hit@1`、`hit@3`、`hit@all`、precision、FP、FULL expected max-W2、W2/435、15 个 planned predicate execution 与 cost，并与冻结 baseline 和冻结全量参考结果公平对照。

若 54 pair 未达 soft gate，先完成 `contract extraction -> identity binding -> predicate route -> typed inputs -> backend -> W -> D -> publication -> Judge relation` stage-loss，选择 12--15 个代表 pair 做一次局部修复；同一版本不得重复抽样刷结果。
