# kitchenham-2009-slr-tertiary：A1-S1S8 四分栏提取

## 总体统计池裁决

裁决：本文是可保留的后续主统计池候选和 schema_seed，样本单位为 20 篇二次研究（19 篇 SLR + 1 篇 MA），分母链应写为 `2506 total records/articles → 33 relevant articles → 19 selected articles → 18 unique studies → +2 externally located peer-reviewed studies → N=20 studies`。但当前证据链仍是 text-level / not_verified，页码、表图、QA 数值与附录表需 A2a 视觉精核；A2a 前不得把本文数值并入最终定量统计。S5 建议保持弱；S8 保持中，不能夸大为完整双人独立筛选/抽取裁决。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | `paper_content.txt` §2 明确本文按 SLR 方法评估 SLR，归类为 tertiary literature review；§2.1 给出 RQ1--RQ4，覆盖活动量、主题、主导者和限制；证据链见 `ev-kitchenham-2009-slr-tertiary-type`。 | 根任务是对 2004--2007.6 SE SLR/MA 的三级综述；RQ 树驱动后续字段与分析项。 | 强；可作为“tertiary review task / RQ tree”统计池候选，但仅限方法模式与样本描述。 | 核对 PDF 中 §2/§2.1 页码、RQ 原文排版和 “tertiary” 表述。 |
| S2 语料收集与筛选 | §2.2--§2.3 描述手工检索 10 期刊 + 4 会议、Travassos/Jørgensen 补检索、显式纳排；§3.1 与 Table A1 给出 `2506→33→19→18+2→20`；证据链见 `ev-kitchenham-2009-slr-tertiary-denom`。 | 检索漏斗子树为来源×年份的 Total / Relevant / Selected；纳排对象为 peer-reviewed SLR/MA，排除非正式综述、流程讨论文和重复报告。 | 强；可作为“筛选漏斗 / 分母链”候选，但中间分母不得冒充最终 N。 | 复核 Table 1、Table A1、Table A2 的列数、总数、会议/期刊枚举和 `+2 external` 来源。 |
| S3 原生维度树/样本编码对象 | §2.5 列出 10 项数据抽取字段；Table 2 展示 S1--S20 编码表；§2.4/Table 3 展示 DARE QA；证据链见 `ev-kitchenham-2009-slr-tertiary-tree`。 | 原生结构为“单树为主 + 并列子树”：主树是 20 篇二次研究抽取编码表；并列 DARE 质量评价子树与检索漏斗子树。 | 强；可作为原生维度树/维度森林统计池候选。 | 核对 Table 2、Table 3、附录表是否完整映射到当前叶子表；确认 PDF 表格跨页无漏列。 |
| S4 字段级证据 | §2.5 字段清单、Table 2、Table 3、Table A1--A3 支撑来源、年份、类型、主题、作者/机构/国家、EBSE 引用、实践者指南、一级研究数、QA 和漏斗字段。 | 叶子层已复原为书目信息、研究分类、作者机构、内容摘要、DARE QA、EBSE/指南引用、实践影响、一级研究数、漏斗与排除原因。 | 强；可作为字段级 schema 候选；具体数值只在 A2a 后进入正式统计。 | 逐字段核对 Table 2/3/A1/A2/A3 的列名、取值空间、脚注和 OCR 残留。 |
| S5 维度模式演化 | §2.7 只记录 protocol deviations；§2.6 说明 RQ 到数据分析项的映射；原文没有 schema/codebook 迭代或维度演化机制。 | 可复原的只是 RQ 驱动字段设计、DARE rubric 采用和 protocol deviation 记录，不是维度树演化。 | 弱；不建议进入主统计池，只作“无显式演化机制/方法边界”质性提示。 | 确认 §2.7 与 Supplementary Appendix 相关表述；避免把 protocol deviation 误写成 schema evolution。 |
| S6 统计分析 | §2.6 列出 8 个分析项；§3--§4、Table 4/5 报告数量、主题、机构国家、质量得分、Spearman 相关、ANOVA 和实践者指南计数。 | 统计从字段树派生：类型/主题/地区/质量/引用/实践者指南/漏斗均有明确字段来源。 | 强；可作为“字段→统计观察”候选；A2a 前不并入最终跨论文定量池。 | 复核 Table 4/5 数值、Spearman `ρ=0.51, p<0.023`、ANOVA `F=0.37, p=0.55` 和所有计数。 |
| S7 候选 finding | §4 Discussion 和 §5 Conclusions 将统计观察转为主题覆盖有限、Simula 策略、美国参与不足、实践者指南不足、抽取-核对风险等候选发现。 | 维度树复原中应区分 OBS 统计观察、作者 discussion 候选发现和不可迁移的历史领域结论。 | 强但限界；可作为“统计观察→候选 finding”模式候选，不能迁移 2009 年领域状态结论。 | 核对 §4.1--§4.5、§5 中每个 finding 的证据边界；标出历史窗口限制。 |
| S8 研究者/作者质疑与裁决 | §2.4 质量评价由 Kitchenham + 其他作者独立评分并讨论分歧；§2.5 数据抽取是一人抽取一人检查；§4.5 承认单人筛选/抽取偏离指南。 | 可复原为 QA 双人独立评分与 disagreement resolution，加上筛选/抽取的 extractor-checker 机制；不是完整双人独立筛选/抽取裁决日志。 | 中；可作为复核机制候选，但需降级表述，不能按“完整双人独立 coding/adjudication”统计。 | 核对 §2.4、§2.5、§4.5 关于 disagreement、checker、independent QA 的原文；确认 Table 3 agreement 列。 |

## 建议降级 / 修正

- S5 保持“弱”：原文有 protocol deviation 与 RQ-analysis alignment，但没有维度模式演化。
- S8 保持“中”：QA 评分较强，但筛选和抽取不是完整双人独立流程。
- 总体统计池口径保持“候选 / A2a 前不进最终定量统计”；所有表格数值、页码和附录证据需在 A2a 精核后再升级。
