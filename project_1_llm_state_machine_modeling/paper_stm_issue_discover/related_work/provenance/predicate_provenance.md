# 当前谓词来源映射入口

旧的逐条来源表已归档到 [`archive/legacy_20260821/predicate_provenance.md`](archive/legacy_20260821/predicate_provenance.md)。
本文件不复制旧数字，避免读者误把旧分类或旧台账用量当成当前结论。

当前唯一有效映射是：

- 机器表：[`pipeline/evidence_discovery/predicate_registry.json`](../../pipeline/evidence_discovery/predicate_registry.json)；
- 人读表：[`pipeline/evidence_discovery/PREDICATE_REGISTRY.md`](../../pipeline/evidence_discovery/PREDICATE_REGISTRY.md)；
- 学术和变更契约：[`METHOD_PRINCIPLES.md`](../../pipeline/evidence_discovery/METHOD_PRINCIPLES.md)。

三类来源：`domain`（领域检查命题）、`formal`（形式定义和性质模式）、`technical`
（后端、算法和回执边界）。来源 ID 只是档案索引，不是普遍率分母；台账/v27 使用量
只是冻结设计的表达力映射。

当前严格来源准入仍未全部闭合，不能把注册表中登记的候选来源写成全部通过。没有足够
来源的命题保留 W1-only，问题仍然可以提出；除非通过独立来源、命题匹配、学术 review
和兼容性测试，否则不得新增谓词或修改定义。
