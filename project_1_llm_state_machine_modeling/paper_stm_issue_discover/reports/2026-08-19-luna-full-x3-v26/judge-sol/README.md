# Sol 54-pair 独立语义评审结果

本目录保存 `gpt-5.6-sol` 对冻结 v26 method 与 X1v2 输出的完整 54-pair semantic judgement。每个 `NNNN.json` 同时包含该 pair 的冻结 ledger 输入、六个 release-output cell、逐台账 hit/miss、支持 finding ID、逐 emission matched-ledger/FP、自然语言 reason 与 confidence；全部 54 份均为真实 `status=ok`，没有用 Luna 标签混填，也没有把失败写成全 miss。

`audit-manifests/` 保存完整 Sol judge 历史调用审计，是 `$12.284775` 成本、103 次 LLM call、110 个 attempt 和 7 次 provider retry exemption 的复算来源。`retry-manifests/0009.json`、`0013.json`、`0056.json` 另提供三次最终补判的直接入口：`0009` 的 4 个前序失败、`0013` 的 2 个前序失败、`0056` 的 1 个前序失败均为 provider/upstream error，并在同一进程内重发；这些前序 attempt 标为 `provider_error_retry_exempt`，随后成功 attempt 正常计费。汇总指标与两臂物理分表位于上一级 `metrics.json`、`ledger_method.md`、`ledger_baseline.md`。

评审输入边界、同处同性质判据、D0 排除、FP 定义、provider retry 与原子 LLM fallback 合同见 [final_output_metrics_policy.md](../../../discover_matrix/docs/protocol/final_output_metrics_policy.md)。
