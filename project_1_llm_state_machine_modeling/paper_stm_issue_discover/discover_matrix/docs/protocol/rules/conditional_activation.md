# 历史规则归档指针

旧的「条件激活」规则绑定了迁移前的 `event_consumed(source, trigger)` 接口和旧台账
动机，不能作为当前四族注册表的语义定义或运行规则。

历史文件保留在
[`archive/legacy_20260821/rules/conditional_activation.md`](../archive/legacy_20260821/rules/conditional_activation.md)。
当前的公开语义以 [`pipeline/evidence_discovery/predicate_registry.json`](../../../../pipeline/evidence_discovery/predicate_registry.json)
和 [`METHOD_PRINCIPLES.md`](../../../../pipeline/evidence_discovery/METHOD_PRINCIPLES.md) 为准；没有
适用谓词时仍输出 W1 `semantic_hit`。
