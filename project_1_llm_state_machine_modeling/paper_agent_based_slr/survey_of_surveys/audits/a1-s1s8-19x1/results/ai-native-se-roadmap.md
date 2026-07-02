# ai-native-se-roadmap：S1--S8 独立审计报告

## 审计结论（未修改文件）

### 0. 术语与本体判定

- **真实类型**：本文是 **vision / challenge roadmap / proposal**，不是 SLR、SMS、tertiary study，也不是 survey-of-surveys。
- **样本单位**：没有系统综述意义上的“论文样本”。可抽取的原生对象是：3 个 SE 时代、5 个 SE 3.0 技术栈组件、5 个主挑战、OQ1–OQ14。
- **主统计池候选**：**否**。可作为 `schema_seed` / `roadmap_boundary_anchor`，不可进入后续主统计池或系统综述 finding 统计。

**本体审计**：若把本文当作“综述论文”或“tertiary/survey-of-surveys 样本”进入主统计池，是**范畴错误**。反例：原文明确说其挑战列表来自 practical experience and discussion，且 “not meant to be extensive”，没有检索式、纳排、筛选分母、QA、编码一致性或 synthesis protocol。

## 1. S1–S8 建议等级

| Schema | 建议等级 | 理由 |
|---|---|---|
| S1 综述问题与范围建模 | 弱 | 有清晰愿景问题：SE 2.0 局限 → SE 3.0；但不是 RQ-driven review。 |
| S2 检索纳排与语料构造 | 弱 / 近不适用 | 只声明 academic/gray literature surveys、workshop、客户讨论、OPEA 等来源；无系统语料链。 |
| S3 样本编码 / 维度树 | 中 | 可复原 era tree、stack tree、challenge/OQ tree；但这些不是文献样本编码树。 |
| S4 证据抽取与质量控制 | 弱 | 有 roadmap 字段模板，但没有 extraction form、QA rubric、coder agreement、quality control。当前 `中` 偏高。 |
| S5 统计分析设计 | 不适用 / 弱 | 只有封闭枚举和内部计数，不构成统计分析设计。 |
| S6 research finding / 启发式 | 中 | 可迁移 challenge → affected component → OQ → vision 的启发式；领域结论必须降级为 vision claim。 |
| S7 人类裁决 / 迭代 | 弱 | 有讨论来源和社区互动，但无正式裁决协议、分歧处理或迭代日志。 |
| S8 可复现性 / 威胁 | 弱 | 有若干自我限制和 “only time will tell”，但无 threats section、protocol、replication package。 |

## 2. 关键问题（C/I/M）

| 等级 | 位置 | 问题 | 为什么重要 | 建议 |
|---|---|---|---|---|
| I | `evidence_chain.md` A.2/A.3 | 写成“6 个主 challenge”。原文是 **5 key challenges**，§4.6 是 other open questions。 | 直接影响样本单位与分母，可能污染 SUMMARY 总账。 | 改为“5 个主挑战 + OQ1–OQ14；§4.6 为 OQ7–OQ14 附加开放问题”。 |
| I | `SUMMARY.md` S1–S4 行 | “不是第 5 个主挑战 + §4.6...” 表达错误，应为“不是第 6 个主挑战”。 | 中文表达与事实相冲突，读者会误解 challenge 数量。 | 统一为“§4.6 不是第 6 个主挑战”。 |
| I | `review.md` §6.1 | “5 个主挑战 + §4.6 附加开放问题 + 14 个 OQ，分母=20”有过度量化和重复计数风险。 | 会把 roadmap 枚举误写成统计分母。 | 改为“结构枚举：5 个主挑战；14 个 OQ，其中 OQ7–OQ14 属 §4.6 附加开放问题；不构成统计分母”。 |
| I | `review.md` S4/S6 | S4 标为“中”、S6 标为“弱”仍容易让人以为存在证据抽取和统计分析。 | Paper2 主线需要严格区分“字段模板”与“系统综述方法”。 | S4 改“弱”；S6 改“不适用/弱”，说明仅有内部枚举。 |
| M | `review.md` 快速卡片 | “taxonomy-边界锚点”措辞偏强。原文主要是 roadmap/stack/challenge，不是 taxonomy paper。 | 表述可能误导，但不影响核心结论。 | 改为“roadmap / stack-vision 边界锚点”。 |

## 3. 修改建议

### `review.md`

1. 保留“非 SLR / 不进统计池”的核心判断。
2. 修正 §6.1 的内部计数：不要写 `分母=20`。
3. S1–S8 表中建议：
   - S4：`中` → `弱`
   - S6：`弱` → `不适用 / 弱`
4. 把 “taxonomy-边界锚点” 改成 “roadmap / stack-vision 边界锚点”。

### `evidence_chain.md`

1. 所有 “6 个主 challenge” 改成 “5 个主挑战 + OQ1–OQ14”。
2. `ev-ai-native-se-roadmap-denom` 中去掉“6 个主 challenge”。
3. 增加限制语：这些是 roadmap structural units，不是 synthesis denominator。

### 顶层 `SUMMARY.md`

1. 修正 ai-native-se-roadmap 的 S3 描述：
   - “不是第 5 个主挑战...” → “不是第 6 个主挑战...”
2. S4/S6 等级与 `review.md` 保持一致。
3. 保持 `否；roadmap 降级`，不要把它列入主统计池候选。

## 4. 原文证据锚点

| 用途 | 锚点 | 短引 |
|---|---|---|
| 类型：vision/roadmap | Page 1, lines 10–20 | “We propose a shift towards Software Engineering 3.0” |
| 技术栈而非综述 | Page 1, lines 14–19 | “We outline the key components” |
| 来源非系统协议 | Page 2, lines 61–69 | “surveys of academic and gray literature” |
| 来源含工业讨论 | Page 2, lines 65–69 | “meetings with our customers” |
| 五个主挑战 | Page 2, lines 70–72 | “Section 4 discusses five key challenges” |
| 愿景性而非实现 | Page 7, lines 303–306 | “we focus on its desired attributes” |
| 挑战模板 | Page 13, lines 580–582 | “description, what parts… it affects” |
| 非穷尽列表 | Page 13, lines 584–586 | “not meant to be extensive” |
| §4.6 降级 | Page 18, lines 798–800 | “not yet developed a thorough vision yet” |
| 未被验证 | Page 20, lines 849–853 | “only time will tell” |
