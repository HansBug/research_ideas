# 15-pair Provider-Free W Replay

本目录是独立、不可变的 W 状态机重放制品。它只读取源 method cell 已保存的 candidate、binding、typed inputs、compiled program、RawReceipt、reason/basis 和 semantic D facts；不调用 LLM、不重跑 backend、不读取 ledger，也不调用 Judge。

- source run: `{source_run_id}`
- source commit: `{source_commit}`
- replay id: `{replay_id}`
- registry: `{registry_version}` / `{registry_hash}`
- W before: `{historical_witness_levels}`
- W after: `{witness_levels}`
- completed Boolean W1 -> W2: `{completed_boolean_recoveries}`
- invalid typed Boolean rejected: `{invalid_typed_input_rejections}`

W2 同时要求冻结 predicate 的受支持片段、精确 binding、合法 typed input、pair/obligation/plan/model/program/receipt 的精确身份链、制品归因闭合、显式谓词/极性发表资格和 terminal `true`/`false`。来源归因不完整只将 W2 降为 W1，已经完成的 `completed`、`executed` 和 `true`/`false` 保留为执行审计事实。`completed/true` 不能发布 issue；`completed/false` 才可能在 D1/D2 下发布。timeout、backend error、invalid input 和 unsupported backend 记录在 execution audit，按 binding 精度退化为 W1/W0，绝不成为 violation。

全部 19 个冻结谓词均已完成学术资格审查，并具有 typed contract、compiled form 与 native backend。学术 provenance 继续留在 registry 和 source catalog，但不参与任何单次运行的 W 或 backend 准入。

`replay_evidence.json` 保存逐 record 的新 W/D/publication、typed execution audit 和 W2 bundle；`audit_bundles/` 仅保存 W2 bundle；`summary.json` 包含机器验收；`replay_manifest.json` 绑定源制品、registry 和 replay 实现哈希。

W-state replay、saved-candidate route replay 与 saved-extraction/grounding frontier replay 是三类不同制品。W-state replay 不重跑 backend；route replay 只对源 run 最终 predicate-null evidence 尝试当前 route/backend；frontier replay 先复用 runner deterministic prefrontier chain，再重物化 frontier并只执行新增 obligation。三者必须分别保存 cohort、实现 hash、provider/Judge 调用数和能力边界，不得合并统计或冒充 method/Judge hit。
