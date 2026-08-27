# 协议自审清单

每次代码冻结、provider-free replay、15x1 与 54x3 前后均按本清单自审。

1. 注册表仍是 19 个冻结谓词，且 registry、typed schema、compiled form、backend 和文档的语义一致。
2. 所有 19 个谓词均具有 academic eligibility 与可执行 backend；来源 catalog 仅作 bibliography metadata，未参与运行时 W、D、publication、route 或 coverage。
3. W 只可能为 `W2/W1/W0`。`completed`/`true|false` 是 W2；失败通过 `execution_state`、`failure_kind`、retry/billing 审计后退 W1/W0，不得被解释为 violation。
4. S4 phase 严格为 entry/do/exit；S2 验 owner-local scope；S5/S6 使用 native transition AST/operation；native Event 必须保持 `event`/`trigger` 角色，不能作为 S5/V1 guard；结构判断不由 ModelIR 或字符串近似完成。
5. R 类输入包含真实 scenario、queue、schedule、macrostep、window 和终止边界；V 类经 `.fbmcq` compile/solve/witness/replay。FBMCQ 的 native load、prepare、core build、property compile、solve、decode、replay 均受父进程 wall-clock/RSS 隔离；V5 lower-bound pass 未被当作目标 horizon satisfaction，lower-bound counterexample 已 replay。未使用 Python `inspect`、手写有限求解或静态 trace。
6. 每个 W2 与退化记录都闭合 current-artifact attribution、typed inputs、program/hash、backend result、reason、basis、receipt/retry/cost。
7. method 未读取 ledger expected、L、Judge、答案、其他 pair 输出或 pair-ID 特判。Judge 保持独立冻结口径，不回流 candidate/W/D。
8. FULL expected 的 max-W2 分母、W2/全部 expected 分母、predicate execution 分母、hit 和 precision/FP 分别报告，不得混算。
9. run identity、source commit、prompt/schema/registry/input hash、cell terminal 状态、实际 worker 数与成本完整；provider error 只重试受影响调用或 cell。后续新 run 默认 `--workers 16`，不得为调整并发重启或覆盖已闭合/执行中的 run。
10. 任一系统性 W 误判、非法 typed W2、错误假 violation、来源 metadata 回流或 Judge 口径漂移都阻止进入下一阶段。
11. R1 只使用 exact event/carrier、唯一 native cold entry 与唯一 direct unguarded carrier；R4 只接受 requirement 明示的 `scenario=cold`、`window=cold_macrosteps=N`（`N <= 32`），或 exact retained state 的唯一最短 native cold-entry prefix 加一个 zero-event macrostep；V1 只接受完整 native same-choice guarded group、exact carrier 集与 requirement 独立有限 JSON `domain`。任何缺口保持 W1，不得补造 runtime/domain。
12. provider-free A/B 物理分离：route replay 只取保存的最终 `predicate_id=null` W1 evidence，frontier replay 只取保存 extraction/grounding 并复用 runner deterministic prefrontier chain，selected structural rebind 只取保存的 S2--S6 candidate。route 与 structural rebind 都必须在 route 前合并 immutable typed `frontier_batch` contract，与 production runner 的输入闭合一致。当前 predicate-null route 制品为 `479bb22f064ec72327b422b57cfbd0cb`：51 条 fixed cohort，3 条 W2（S2=2、R4=1）、48 条 W1，0 provider/Judge；不得混算各 cohort、把辅助 candidate 当 cohort，或呈报为 hit/Judge 指标。
13. FCSTM 的唯一语义源是 `pyfcstm` 原生 parser/AST/model/topology/runtime/`.fbmcq`。`ModelIR` 仅为 native compatibility projection；任何 state/event/transition/path/owner/forced/combo/guard/effect/lifecycle/choice/runtime 输入都由 native identity 解析。不得有 FCSTM regex、line parser、brace stack 或文本语义回退。每次冻结的 `fcstm_native_projection_audit` 必须为 60/60 source load、54/54 input closure、零 projection difference、零未批准文本处理。

14. provider-free replay 必须按固定输入 cohort 分开保存、分开统计：predicate-null `route_replay`、保存 frontier `frontier_replay`、已选择 S2--S6 `structural_rebind_replay`。任何 replay 都不得读 ledger expected、Judge、答案或其他 pair；不得调用 provider/Judge；不得发布 issue 或作为 hit/precision 统计。`structural_rebind_replay` 的已选候选必须重新经过 exact native binder，旧 projection ref 和 legacy guard/action 字段不能直接输入 backend；无法闭合只能 W1/W0 并保留 failure audit。当前 selected-structural 制品 `c9b461924c636ae6a92809b117934be9` 固定审计 108 条，其中 57 条 W2、16 条 route-unclosed、35 条 execution-degraded，0 provider/Judge。历史 frontier 中已被 soundness audit 删除的 `wrong_scope_route` 仅可在 replay 输入边界排除并逐项计数，生产 `FrontierBatch` 仍严格拒绝，不能为历史制品恢复该 kind。
15. 15-pair 的 planned execution 分母固定为 S1、S2、S3、S4、S5、S6、G1、G4、R1、R4、V1、V4。selection preflight 只能含通用 capability/schema、输入 hash 和 semantic-shape metadata；它不得含 ledger、expected、Judge、答案、D/L、hit、precision 或 pair-specific execution values，worker 只记录其 hash/reference。
16. 54x3 的 planned execution 分母固定为 S1--S6、G1--G4、R1、R2、R4、V1、V4（15 个）；完整 universe 自动使用 `full-scale-15`，任意后续代表子集必须显式声明该 scope，不得按 terminal predicate 集合缩小。
17. `backend_missing` 只表示 frozen predicate 没有 dispatch/backend；当前 19/19 backend 下应为 0。`invalid_input` 归入 `input_contract_missing`，已实现 backend 上的 fragment 缺口归入 `out_of_fragment`，原 `failure_kinds` 同时保留；不得从 `backend=none` 的未执行展示值反推 backend 不存在。
18. G2/G3/R2 route 只消费当前 pair 的 pyfcstm native identity/runtime。G2 composite source 必须经每层唯一 `State.init_transitions` 下降到 leaf；R2 的 identity 必须由 typed alternative、唯一 canonical carrier 与 native Event 闭合，prefix 搜索不接收 target state。不能用待验证 target truth、ledger、Judge 或答案选择 source leaf/scenario；不唯一、未消费或运行失败保持 W1。
19. evaluator compatibility projection 未修改 method/Judge 原件：eligible diagnostic reports 逐值保持，ineligible failed cells 为空发布面；原始/投影 hash、status、eligible、report count、reason/basis 全部闭合。恢复只补失败 `(round,pair)`，composite 保留所有失败尝试、retry、成本和固定 435 expected position。
