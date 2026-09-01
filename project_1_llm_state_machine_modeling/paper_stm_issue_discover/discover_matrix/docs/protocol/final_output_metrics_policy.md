# 最终输出与指标政策

method、ledger 与 Judge 物理隔离。方法不得生成、裁定或在 release issue 中声称自己的 `l_level`；Judge 只在独立 evaluation artifact 中建立 FULL/PARTIAL/NONE/INVALID 关系。

每次正式运行报告：

- method cell terminal/diagnostics、run/source/prompt/schema/registry/input hashes 与成本；
- evidence `W2/W1/W0`、execution failure/retry/billing；
- FULL hit 的 max-W2 占比和 W2/全部 expected，分别使用各自固定分母；
- `hit@1`、`hit@3`、`hit@all`、L2、semantic precision、INVALID/FP；
- 19 backend conformance、固定 planned predicate execution 分母与逐项 input closure；
- W2 与退化记录的 audit closure。

completed true 是 W2 pass receipt 但不是 issue。completed false 只有 D2/D1 才可发布。timeout、backend error、invalid input、unsupported backend 与 attribution failure 不能制造 violation；它们依据 precise binding 退 W1 或 W0。

后端禁止调用 Python `inspect`。结构、拓扑、轨迹和有界结果必须来自 FCSTM 的 native model class、`pyfcstm.verify.topology`、`SimulationRuntime` 或 `.fbmcq` 的真实执行。Judge 不得为降低成本而改变冻结语义，method 不得读取台账答案或 Judge 结果。

FCSTM source 只由 `pyfcstm` 原生 parser/AST 解释；`ModelIR` 是 native compatibility projection，不是第二个 DSL parser。最终报告同时附带 `fcstm_native_projection_audit`：60/60 native source load、54/54 frozen input closure、零 projection parity difference、零未批准文本处理。该 audit 与 W2/全部 expected、FULL max-W2、hit 和 predicate execution 分母分别报告，不能相互替代。

route A/B 是独立的确定性诊断，不是最终评测。它的 cohort 必须为保存的最终 `predicate_id=null` W1 evidence；当前有效基准 artifact ID 是 `1bf7555fdbb9661008fc1e14b0ae16be`（`evidence-discovery-15x1-primary-route-replay-78506646`）的 88 条 cohort，provider/Judge 调用均为 0。A/B 只报告新增 route、terminal execution、W 和未闭合输入，不得把它混入 FULL hit、W2/全部 expected、precision、predicate execution 分母或 Judge 统计。
