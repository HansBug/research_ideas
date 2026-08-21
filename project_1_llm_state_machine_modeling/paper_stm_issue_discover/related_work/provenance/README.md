# 谓词来源档案

本目录保存当前谓词注册表所引用的来源摘录、边界审计和复核工具。当前方法的唯一
政策入口是 [`pipeline/evidence_discovery/METHOD_PRINCIPLES.md`](../../pipeline/evidence_discovery/METHOD_PRINCIPLES.md)，
唯一公开谓词表是 [`pipeline/evidence_discovery/predicate_registry.json`](../../pipeline/evidence_discovery/predicate_registry.json)。

当前来源 ID 的逐条落点和审查状态以 [`CURRENT_SOURCE_AUDIT.md`](CURRENT_SOURCE_AUDIT.md)
为准，机器校验目录为 [`current_source_catalog.json`](current_source_catalog.json)。

## 当前有效口径

现行配置为 `four-family-19-core.v1`：结构 6、拓扑 4、轨迹仿真 4、有界验证 5，共 19
个原子谓词。W1 是精确绑定但没有 sound 后端的合法 `semantic_hit`；W2 是终止且带源
归因的可执行证据；W0 和 `UNKNOWN` 不能算违反或命中。

来源分三类：

1. 真实领域系统和工程文献，证明检查命题在领域中反复出现；
2. 形式语义、性质模式和模型检查资料，说明命题的学术定义；
3. 工具或算法技术资料，限定求值后端、输入假设和回执边界。

三类来源回答不同问题，不能把技术实现说明冒充领域普遍性，也不能把来源数量当总体
比例。台账/v27 出场量只用于冻结后的表达力映射，不是来源证据。

## 严格审查状态

当前来源档案已经登记命题、来源 ID 和边界，但严格 T0、非并发、命题匹配、多源和
领域多样性准入尚未对所有谓词闭合。现行文档必须把“候选依据已登记”和“严格来源门
已通过”分开写，不能使用旧文档中的来源总数直接宣称全部可靠。

如果一个命题暂时没有足够来源，它仍可以作为语义问题提出并输出 W1；不能为了覆盖率
新增谓词、扩大已有谓词含义或把 containment/cardinality 等换名包装成核心。

## 历史材料

旧的来源分组、覆盖审计和三类政策草案在 [`archive/legacy_20260821/`](archive/legacy_20260821/)
中保留。它们可用于追溯，但不属于当前运行路径。未移动的原始摘录也必须通过当前注册表
重新解释，不能直接恢复旧谓词。
