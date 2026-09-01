# 运行审计清单

本目录的语义裁定制品是 `judge-luna/` 下五个 pair JSON，`metrics.json` 只做 exact-ID 计数和成本汇总，`ledger_method.md` 与 `ledger_baseline.md` 是物理分离的逐条台账对照。语义 hit/false positive 来自 Luna judge 的自然语言 reason 与 confidence；确定性部分只负责按 ledger ID、cell ID 和 emitted finding ID 连接已裁定结果。

方法原始记录位于 `runs/paper1/witness-search/v36-default-stream-x3-20260820/run{1,2,3}/{0004,0023,0029,0046,0053}-luna/record.json`。15 个 method 格均正常完成；每个 observation 的 `adapter` 为 `openai-responses`、`streaming` 为 `true`，没有把 D0 cluster 送进 judge。

X1v2 baseline 原始记录沿用 `runs/paper1/luna-full-x3-20260819-v1/baseline-v2/run{1,2,3}/{0002,0029,0034,0046,0053}-luna/record.json`，profile 同为 `gpt-5.6-luna`。baseline 只作为同一 pair、同一轮位置的对照，不与 v36 method raw record 混写。

本轮五格 method 生成成本为 `$0.63995292`，baseline 对应成本为 `$0.02260044`，子集比值为 `28.316x`；该值只用于诊断，不能替代全量成本 gate。judge 的 provider 调用不进入 method/baseline 倍率；judge JSON 保留每一条 relation 的 `reason`、`confidence` 和 `supporting_finding_ids`。

本轮结果不是 54-pair 正式 headline。正式结论仍需在当前 Responses + 默认 stream 基础设施上完成全量三轮 method，并用同口径 judge 与 X1v2 对照后再发布。
