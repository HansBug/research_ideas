# da-silva-2011-six-years-slr：S1--S8 四分栏审计补充

## 总体统计池裁决

本文是后续主统计池候选：原文具备系统检索、纳排、QA、数据抽取、明确分母链与可统计字段；但当前证据链仍标记为 `not_verified / 待 A2a`，因此在 A2a 完成 PDF 版面、表图、页码和分母链精核前，只能作为文本级可用的 schema / pattern seed 与主统计池候选，不应写入最终定量结论。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文明确为 updated tertiary study；RQ1--RQ5 覆盖 SLR 数量、主题、活跃作者/机构、既有限制、质量改进。 | 对应任务层根节点：更新型三级研究，以已发表二级研究为样本单位，并整合 OS/FE + SE。 | 支持主统计池候选的任务边界；不是最终 finding。 | 核对 PDF 摘要、§3.1 RQ、OS/FE/SE 定义的页码与表述。 |
| S2 语料收集与筛选 | 自动检索 6 个库、手工检索 13 个源、参考文献回溯；154 unique papers → 77 → 排除 10 → 67，整合 OS/FE 后 N=120。 | 对应语料构造与分母链节点：search、selection、QA/data extraction、final SE set、integrated OS/FE+SE set。 | 强支持主统计池候选，但最终统计前需确认 67/77/120/1455 等分母。 | 核对 Fig.2、Table 1、Appendix A、结论中 1455 articles 与流程图分母是否一致。 |
| S3 原生维度树/样本编码对象 | 样本为 SLR/MS/MA 二级研究；抽取 Year、Quality Score、Review Type、Review Scope、Topic、citation、primary-study count、practitioner guideline、source type 等。 | 可复原为维度森林：抽取表 schema、QA rubric、主题/课程/SWEBOK 分类、作者/机构/国家关系、OS→FE→SE 更新关系。 | 支持主统计池候选的编码对象定义；具体叶子维度应等 A2a 后入正式字段表。 | 核对 Table 2、Table 3、Table 5、Table 6 以及 Appendix A 是否完整支撑所有叶子。 |
| S4 字段级证据 | §3.6 给出 QA1--QA4 与 Y/P/N 评分；§3.7 给出抽取字段；Table 2/3/5 等按 SE ID 展示样本级编码。 | 字段级证据较充分，可支撑抽取表与 QA rubric 两棵核心子树。 | 文本级可入候选字段池；最终字段统计需 A2a 表格视觉核验。 | 核对表格列名、SE01--SE77 ID、缺失/排除项、Table 2/3/5 的换行和 OCR 提取错误。 |
| S5 维度模式演化 | 原文说明沿用 FE protocol、调整 RQ4；QA2 标准有修改；结论提出 temporal update、search extension、both 三类更新。 | 可复原为“前序综述关系 / 更新类型”子树，但不是完整 codebook 演化日志。 | 只作为模式演化的中等强度候选，不宜进入最终统计为强证据。 | 核对 §3 方法继承、§6 QA2 咨询 OS/FE 作者、§7 三类 update 的原文精确表述。 |
| S6 统计分析 | 原文有主题频次、质量趋势、指南引用、practitioner guideline、primary-study QA、回归与相关分析等，含 N=67/N=120。 | 对应字段 → 频次/比例/趋势/回归的统计路径，可支撑统计观察层。 | 支持主统计池候选；A2a 前不得沉淀为最终跨论文定量结论。 | 核对 Table 4、6、10、11、12、13 及回归/相关分析的 N、p、系数。 |
| S7 候选 finding | 结论提出主题覆盖增加、研究者/组织更分散、MS 比例增加；也指出 primary QA 不足、综合方法薄弱、practitioner guideline 仍少。 | 对应统计观察 → candidate finding / limitation / recommendation 路径。 | 可作为 finding heuristic 候选；领域结论必须降级为 2004--2009 SE SLR 语境。 | 核对结论与 §5 discussion 是否由表格统计直接支撑，避免把作者解释外推为通用规律。 |
| S8 研究者/作者质疑与裁决 | 原文定义 DCP：双人评估、第三研究者裁决、全体共识；QA 与 data extraction 使用 DCP；§6 讨论 QA2/QA4 主观性和报告不足。 | 对应 human-in-the-loop 裁决子树：selection / QA / extraction 的 disagreement handling 与 limitation challenge。 | 支持研究者裁决模式入库；不直接增加统计分母。 | 核对 Fig.1 DCP、§3.3、§3.6、§6 中“至少两人”“第三方/共识”的完整性。 |

## 建议降级 / 修正

- 当前 `review.md` 的 S1、S2、S3、S4、S6、S8 标为“强”总体可以保留，但建议在四分栏中明确写成：文本级强证据；A2a 前不等于最终统计证据。
- S5 标为“中”合理：原文有更新关系与 QA2 修订，但没有完整 codebook 演化或冲突修订日志。
- S7 标为“中”合理：多项 finding 有统计支撑，但跨论文迁移和领域外推必须等 A2a/A2b 复核。
