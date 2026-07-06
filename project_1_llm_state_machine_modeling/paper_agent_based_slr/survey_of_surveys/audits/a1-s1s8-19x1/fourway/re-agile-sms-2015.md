# re-agile-sms-2015：A1-S1S8 四分栏提取裁决

## 总体统计池裁决

裁决：**主统计池候选，但仅限 A1 schema_seed / mapping 字段统计；A2a 精核前不得进入最终定量统计或研究发现池**。理由是原文确为 2015 年 SEAA 短会议论文形式的 systematic mapping study，给出 Scopus 检索式、时间窗、纳排标准与 241→187→65→28 的分母链，并对 28 篇原始研究 S1--S28 做 venue、context、article type、benefit、problem / solution 分类；但样本量较小、单库 Scopus、表 I--V 版面/页码尚未 PDF 视觉核验，且未报告多研究者筛选/编码裁决、一致性或 QA 协议。因此可作为 S1--S7 的可统计模式种子，S8 只能弱证据记录限制与缺失裁决机制。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文标题、摘要和引言明确为 “mapping study”；提出 3 个 RQ：研究了什么、报告了哪些 agile RE benefits、有哪些 problems 及 corresponding solutions。 | 根对象复原为“敏捷软件开发中的需求工程原始研究（28 篇）”，RQ1--RQ3 分别锚定分布、benefit、problem+solution 三类字段用途。 | **可入候选池**：SMS 任务设定清晰，可作为 exploratory mapping RQ 样本；不支持效果评价型结论。 | 核对 PDF 中 RQ 段页码与 wording；确认会议短文未在附录补充更细 protocol。 |
| S2 语料收集与筛选 | Methodology 给出 Scopus、2014-09 检索、完整检索式、排除非 journal/conference、非英文、题摘排除和全文排除标准；分母为 241→187→65→28。 | 复原出“语料/纳排分母链”分支：数据库、检索式、时间窗、初筛、题摘筛选、全文筛选、排除原因。 | **可入候选池**：分母链足以支撑 mapping-study 筛选字段；但单库检索限制需随字段一起保留。 | PDF 视觉核验检索式脚注、排除标准编号、分母数字；检查 2003/2004--2014 年份跨度表述差异。 |
| S3 原生维度树/样本编码对象 | 方法段说明抽取 metadata、context、methods、results，并归入 definition、benefits、problems、solutions；结果表使用 S1--S28 原始研究编号。 | 复原为维度森林：语料分支 + venue/context/article-type 三个分布分支 + definition + B1--B6 benefit + P1--P6 problem / solution 关系边。 | **可入候选池**：样本单位为原始研究，树/森林结构清楚；problem→solution 是本地从 §IV.D 复原的关系 schema，不应写成原文 formal table。 | 核验 Table I--V 中 S 编号、合并单元格、B/P 枚举是否与文本提取一致；确认 solution set 的边界。 |
| S4 字段级证据 | Table I--III 给 venue、agile method context、article type；Table IV--V 给 benefit/problem 类目及 S 编号集合；§IV.D 逐项讨论 solution 或 no solutions。 | 叶子字段包括 Scopus/search string/分母链、venue type/name、context、article type、definition clarity、B/P code、study set、solution relation、single-database limitation。 | **有条件可入候选池**：字段丰富且多为封闭枚举/关系集合；当前证据等级为全文文本级，表格数值仍不宜 final。 | 必须对表 I--V 做 PDF 表格级核验；特别核验会议/期刊/杂志计数、B1--B6/P1--P6 的 S 集合与空 solution 断言。 |
| S5 维度模式演化 | 原文从 RQ 到 Results 再到 Discussion：RQ1 形成分布表，RQ2 形成 benefit taxonomy，RQ3 形成 problem taxonomy 与 solution/gap 讨论。 | 复原出 RQ→字段→统计观察/候选 finding 的演化链；“solution 集合为空”被视为一等缺口信号。 | **中等候选资格**：可作为 mapping 维度如何生成 finding 的模式种子；但演化过程多由本地审计重构，不能当作作者显式方法论贡献。 | 核验 §IV.D/V.C/VI 中 no-solution 与 future-work 句子，避免把审计者归纳过度写成作者 schema。 |
| S6 统计分析 | 原文给出 28 篇样本的描述统计：conference 15/28、journal 8/28、magazine 5/28；unspecified agile 20/28、Scrum 7、FDD 1；method proposal 8/28；经验/评价类约 17/28 等。 | 统计分支可复原为分布统计 + coverage 统计 + problem 无 solution 比例（P3/P4/P6 = 3/6）。 | **可入候选池但小样本降权**：适合 landscape / coverage 统计，不适合因果、效果、饱和性或全域趋势判断。 | 核验所有百分比四舍五入和表格单元格；短会论文 N=28、单库 Scopus 和稀疏 cell（如 FDD=1、tool eval=1）必须保留警告。 |
| S7 候选 finding | 摘要、Discussion 和 Conclusion 给出 agile RE 定义模糊、无主导 venue、user story 在复杂大型系统中不足、P3/P4/P6 无解决方案、方法提议缺少实证评价等发现。 | finding 由字段统计和主题归纳支持：definition clarity、venue dispersion、article type distribution、problem-solution gap、empirical evaluation gap。 | **可入候选 finding 池**：仅作为本文内部 mapping finding 或 Paper2 方法启发；不得迁移 Agile RE 领域结论。 | A2a 需逐条映射 finding→表格/段落证据；区分作者明说、审计归纳与后续研究启发。 |
| S8 研究者/作者质疑与裁决 | §V.D Limitations 仅说明 Scopus 单库和检索词范围限制；未见多研究者筛选、编码冲突裁决、inter-rater agreement 或 QA checklist。 | 复原为“限制声明存在，但研究者裁决机制缺失”的弱分支；可记录 negative evidence。 | **弱资格/不入强统计**：可统计“是否报告 limitations=是、是否报告裁决/一致性=否/未报告”，但不支撑高可信 QA 模式。 | PDF 全文检索/视觉核验是否存在遗漏的裁决、双人筛选、编码一致性或 quality assessment 描述；若仍缺失，应保持弱或缺失编码。 |

## 建议降级 / 修正

1. 将本文总体资格表述统一为：**A2a 主统计池候选 / A1 不进入最终定量统计**，避免 `eligible_for_statistical_synthesis=true` 被误读为当前已可 final synthesis。
2. S4、S6 的表格数值在 A2a 前保持“全文文本级；表格待核验”，不要升级为 PDF 图表级证据。
3. S8 建议维持“弱”：原文有 limitation，但缺少研究者裁决与一致性机制；不得因其是 SMS 而脑补 QA 协议。
