# 方法谓词与出处政策

**状态：** 当前有效  
**适用范围：** paper1 的证据发现流水线、评测记录和论文叙事  
**唯一注册表：** [`pipeline/evidence_discovery/predicate_registry.json`](../../../pipeline/evidence_discovery/predicate_registry.json)

## 1. 当前方法口径

当前正式配置是 `four-family-19-core.v1`，公开原子谓词共 19 个：结构 6、拓扑 4、
轨迹仿真 4、有界验证 5。四族按证据产生方式划分，不是按 benchmark 类别切分。
完整命题、最小输入、来源 ID 和 W1-only 清单以注册表和
[`METHOD_PRINCIPLES.md`](../../../pipeline/evidence_discovery/METHOD_PRINCIPLES.md) 为准。

谓词是证据升级，不是问题提出门槛。需求先做语义绑定和裁决：

- W2：终止、可执行且带源归因的回执在声明 soundness fragment 内证明命题；
- W1：绑定精确到可复现位置，但没有适用的 sound 谓词或后端。W1 是合法的
  `semantic_hit`，必须计入命中统计；
- W0：无法精确绑定，不算命中，记录为 coverage gap；
- `UNKNOWN`：永远不能改写为 violation。

因此，缺少谓词不能抑制问题提出；只能降低证据等级。表达力快照 118/145（81.4%）、
L2 35/39（89.7%）和 v27 603/741（81.4%）是冻结设计映射，不是新实现的 W2 实测结果。

## 2. 三类学术来源

来源审查要区分“命题为什么值得检查”和“后端如何正确求值”：

1. **领域来源**：真实控制系统、状态机工程和需求分析中反复出现的检查命题；
2. **形式来源**：状态机语义、性质模式、模型检查或标准资料中对相关命题的正式讨论；
3. **技术来源**：工具/算法语义和实现资料，只用于限定输入、求值和回执边界。

来源 ID 必须能够回到 `related_work/provenance/` 的原始摘录或档案，并说明命题匹配、
模型边界以及是否含 timed、parallel 或 hybrid 语义。来源数量表示存在性和来源多样性，
不表示总体普遍率；台账或 v27 使用量不构成学术出处。

当前逐条审计见 [`related_work/provenance/CURRENT_SOURCE_AUDIT.md`](../../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)，
机器目录见 [`related_work/provenance/current_source_catalog.json`](../../../related_work/provenance/current_source_catalog.json)。

当前来源集合仍有部分未完成项目规定的 T0、非并发、多源和命题匹配严格准入。因此现阶段
只能说候选依据已登记，不能声称 19 个谓词的来源门全部通过。来源不足的命题保持
W1-only，不得通过改名或扩大语义来补覆盖。

## 3. 变更门

除非同时具备独立于本台账的命题匹配来源、清晰的最小输入和 soundness 边界、完整学术
叙事审查、兼容性迁移说明，以及注册表/来源/W1-W2/后端/mutation/prose non-interference
测试，否则禁止新增谓词或修改现有谓词定义。覆盖率目标、单个案例、LLM 生成便利和旧
实现结构都不是变更理由。低频边角需求可以合法地输出 W1。

containment、exact cardinality、initial existence/outdegree、consumer scope、
orthogonal runtime、hierarchy priority、trace variable delta 等命题目前只走 W1，
不是核心谓词。派生宏必须展开为现有原子，不增加公开 ID。

## 4. 归档纪律

`pipeline/archive/witness_search_prototype_legacy_20260821/` 和本目录下的
`archive/legacy_20260821/` 只保存历史代码、旧设计和旧出处审计。它们不在运行路径，
不得作为当前方法名、当前谓词表或新结果证据。任何引用旧材料的现行报告都必须明确
标注历史版本，并回链当前注册表。
