# 历史策略归档指针

旧的 `fused_event_policy` 属于 v25 迁移期策略复盘，曾讨论事件融合和假想的
`event_cardinality` 扩张。它不是当前方法政策，不能据此新增谓词或修改四族 19 行定义。

完整历史记录见
[`archive/legacy_20260821/fused_event_policy.md`](archive/legacy_20260821/fused_event_policy.md)。
当前有效规则以 [`method_provenance_policy.md`](./method_provenance_policy.md)、
[`pipeline/evidence_discovery/METHOD_PRINCIPLES.md`](../../../pipeline/evidence_discovery/METHOD_PRINCIPLES.md)
和 [`REFACTOR_PLAN.md`](../../../pipeline/evidence_discovery/REFACTOR_PLAN.md) 为准：
谓词是证据升级而非问题提出门槛；没有适用谓词时输出 W1 `semantic_hit`。
