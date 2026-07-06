# ml4se-tertiary-study：A1-S1S8 四分栏提取

## 总体统计池裁决

裁决：**后续主统计池候选，但当前仍按 `schema_seed` / 方法模式样本使用；A2a 完成 PDF 表图、supplementary / Zenodo 制品与字段级页码精核前，不进入最终跨论文定量统计。** 本文是 ML4SE tertiary study，原文最终分析对象是 **83 篇通过 DARE-4 QA≥2.0 的 secondary studies / reviews**；摘要和结果中的 **6,117 primary studies** 只能写作“非唯一 primary-study 覆盖计数 / coverage metric”，不是去重后的原始研究总数，也不是逐篇编码样本单位。可迁移的是三级综述的分母链、字段树、质量评价、统计与 implication 生成模式，不能迁移 ML4SE 领域频次和具体研究建议为本仓库目标领域 finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要称系统收集、质量评价、汇总并分类 83 篇 ML4SE reviews；§3.1 给出 RQ1 SE tasks、RQ2 underrepresented KAs、RQ3 ML techniques。 | 复原为“ML4SE 三级研究”的任务树：以 secondary studies 为综述对象，RQ1/2/3 分别驱动 SE task、SWEBOK KA coverage 与 ML technique 分类。 | **强 / 候选**：可作为 tertiary-review task 与 RQ-field contract 样本；只贡献方法模式。 | 核对 ACM final 与本地 arXiv 文本在标题、年份、RQ 表述和页码上的差异。 |
| S2 语料收集与筛选 | §3.2--§3.5：自动检索 IEEE/ACM/Scopus 得 1,897 条，DOI 去重为 1,566；manual search 补 1 条成 1,567；snowballing 后 140 篇进入 QA；57 篇 QA<2.0 排除，最终 83。 | 复原为多阶段漏斗：automated/manual search → DOI 去重 → IC/EC → backward/forward snowballing → DARE-4 QA → 83 quality-accepted reviews。 | **强 / 候选**：分母链清楚；但最终统计主分母只能用 83 reviews，不能用 1,567/140/6,117 替代。 | 视觉核验 Fig.1、§3.2 footnote CSV、backward/forward snowballing 数量、3 篇审稿建议补入研究是否进入 140。 |
| S3 原生维度树/样本编码对象 | §3.6 列出每篇 quality-accepted secondary study 的抽取字段；§4.1 声明最终 83 篇 reviews 覆盖 6,117 non-unique primary studies；Tables 3--4 给逐篇 review 台账。 | 复原为以 `secondary_study` 为根的共根维度森林：书目信息、研究设计、质量评价、primary 覆盖度、SWEBOK KA×subarea×SE task、ML 四轴、further research / implications、threats / replication。 | **强 / 候选**：样本编码对象明确；6,117 仅作覆盖度叶子字段，不作为样本根。 | 核验 Tables 3--4 的 Primary / Covered Years 列、是否存在重复 primary、以及 supplementary `knowledge_areas.csv` 等文件与正文一致性。 |
| S4 字段级证据 | §3.6 明列 title/source/year/venue/authors/institutions/countries/study type/research method/QA score/primary count/KAs/subareas/tasks/implications/ML techniques；Tables 3--7 与 Fig.6 展示字段结果。 | 复原为字段合同 → 表图统计 → supplementary CSV/MD 的证据链；字段包括封闭枚举、数值、自由文本和多对多关系边。 | **中到强 / 候选**：字段层次充分，但当前 evidence_chain 仍标为 text-level / not_verified，表图和补充材料未逐项精核。 | 逐字段核验 Table 3--7、Fig.3--6、footnote 中 Zenodo / CSV 文件名、字段缺失值和推断 primary 数规则。 |
| S5 维度模式演化 | §3.6：SWEBOK KA 和四轴 ML scheme 来自既有来源；SE tasks 用 open coding，随后讨论、泛化/特化并用 qualitative content analysis 分组；ML application task 在 Table 7 事后归类。 | 复原为“先验框架 + 开放编码 + 事后归纳”的混合演化模式；不是完整公开的 codebook 版本史或冲突日志。 | **中 / 可统计为有 schema construction 证据**；不宜升级为完整 schema-evolution audit。 | 查 supplementary 是否包含原始 codes、合并记录、冲突记录、coder agreement；若无，应保持 S5=中。 |
| S6 统计分析 | §4.1--§4.4、Tables 3--7、Fig.3--6 报告 83 reviews 的年度、venue、publisher、QA、study type、KA/subarea/task、ML 四轴、ML application task 等频次/比例/交叉分布。 | 复原为由字段树派生的统计层：83 reviews 是主分母；6,117 是非唯一 primary-study coverage sum；KA×ML axis 等为关系/交叉统计。 | **强 / 候选**：适合后续抽取“是否具备统计分析”与字段分布模式；A2a 前不得并入最终定量统计。 | 核对所有百分比、分母、四舍五入、Table 5 Sec./Prim. 列含义；特别标注 6,117 非唯一边界和部分 primary 数由 bibliography 推断。 |
| S7 候选 finding | §4.3.1 与 §5 给出 general recommendations 和 Implications 1--7：实证/工业验证、SE literature deficiencies、human-centered KA 数据、data pipeline、proprietary data、online/incremental、hybrid/cross-domain ML。 | 复原为“统计覆盖观察 → underrepresented KA / obstacle → implication / recommendation”的 finding 生成路径。 | **强但限界 / 方法模式候选**：可统计 finding 形成机制；ML4SE 领域结论不得进入目标领域 final finding。 | 检查每条 implication 与前文 RQ2/Table 5/Table 6 的支撑关系；区分作者建议、统计观察与本仓库可迁移方法启发。 |
| S8 研究者/作者质疑与裁决 | §3.4 用 Cohen's Kappa 校准 IC/EC；§3.5 QA 采用 extractor/checker 且 82% agreement；§3.6 多处说明冲突由讨论或最后作者解决；§6 分 Study Selection/Data/Research validity。 | 复原为质量控制与裁决树：选择一致性校准、DARE-4 QA、extractor/checker、conflict resolution、threat taxonomy；本地三路审计不算原文证据。 | **强 / 候选**：可统计为报告了 QA、inter-rater / agreement、冲突解决和 threats；但不是公开逐项裁决日志。 | 核验 `cohen_kappa_agreement.csv`、`dare_assessment.csv`、selection reviewer CSV、是否有逐项 disagreement log；若无，避免写成 full audit trail。 |

## 建议降级 / 修正

- 坚持分母边界：**83 reviews / secondary studies** 是编码与统计主样本；**6,117 primary studies** 是非唯一覆盖计数，且部分数值可能由 bibliography 推断，不能写成去重 primary-study 语料库。
- S4、S5 在 A2a 前不宜无条件升为“强”：字段合同强，但表图、supplementary 与 codebook 演化记录仍待核验；S5 最多写作“混合 schema construction”，不是完整 schema evolution。
- S7 只迁移“统计观察到 implication/recommendation 的生成模式”；不得把 supervised/offline/model-based 等 ML4SE 具体频次写入 Paper2 目标领域结论。
