# 协议自审清单

每次代码冻结、provider-free replay、15x1 与 54x3 前后均按本清单自审。

1. 注册表仍是 19 个冻结谓词，且 registry、typed schema、compiled form、backend 和文档的语义一致。
2. 所有 19 个谓词均具有 academic eligibility 与可执行 backend；来源 catalog 仅作 bibliography metadata，未参与运行时 W、D、publication、route 或 coverage。
3. W 只可能为 `W2/W1/W0`。`completed`/`true|false` 是 W2；失败通过 `execution_state`、`failure_kind`、retry/billing 审计后退 W1/W0，不得被解释为 violation。
4. S4 phase 严格为 entry/do/exit；S2 验 owner-local scope；S5/S6 使用 native transition AST/operation；结构判断不由 ModelIR 或字符串近似完成。
5. R 类输入包含真实 scenario、queue、schedule、macrostep、window 和终止边界；V 类经 `.fbmcq` compile/solve/witness/replay。FBMCQ 的 native load、prepare、core build、property compile、solve、decode、replay 均受父进程 wall-clock/RSS 隔离；V5 lower-bound pass 未被当作目标 horizon satisfaction，lower-bound counterexample 已 replay。未使用 Python `inspect`、手写有限求解或静态 trace。
6. 每个 W2 与退化记录都闭合 current-artifact attribution、typed inputs、program/hash、backend result、reason、basis、receipt/retry/cost。
7. method 未读取 ledger expected、L、Judge、答案、其他 pair 输出或 pair-ID 特判。Judge 保持独立冻结口径，不回流 candidate/W/D。
8. FULL expected 的 max-W2 分母、W2/全部 expected 分母、predicate execution 分母、hit 和 precision/FP 分别报告，不得混算。
9. run identity、source commit、prompt/schema/registry/input hash、cell terminal 状态与成本完整；provider error 只重试受影响调用或 cell。
10. 任一系统性 W 误判、非法 typed W2、错误假 violation、来源 metadata 回流或 Judge 口径漂移都阻止进入下一阶段。
11. R1 只使用 exact event/carrier、唯一 native cold entry 与唯一 direct unguarded carrier；R4 只接受显式 `scenario=cold`、`window=cold_macrosteps=N`（`N <= 32`）；V1 只接受完整 native same-choice guarded group、exact carrier 集与 requirement 独立有限 JSON `domain`。任何缺口保持 W1，不得补造 runtime/domain。
12. route A/B 的 cohort 必须是保存的最终 `predicate_id=null` W1 evidence。当前有效制品 `evidence-discovery-15x1-primary-route-replay-78506646/1bf7555fdbb9661008fc1e14b0ae16be` 为 88 条、0 provider/Judge 调用；辅助 `execute_batch` candidate 集不得代替该 cohort，A/B 不得被呈报为 hit 或 Judge 指标。
13. FCSTM 的唯一语义源是 `pyfcstm` 原生 parser/AST/model/topology/runtime/`.fbmcq`。`ModelIR` 仅为 native compatibility projection；任何 state/event/transition/path/owner/forced/combo/guard/effect/lifecycle/choice/runtime 输入都由 native identity 解析。不得有 FCSTM regex、line parser、brace stack 或文本语义回退。每次冻结的 `fcstm_native_projection_audit` 必须为 60/60 source load、54/54 input closure、零 projection difference、零未批准文本处理。
