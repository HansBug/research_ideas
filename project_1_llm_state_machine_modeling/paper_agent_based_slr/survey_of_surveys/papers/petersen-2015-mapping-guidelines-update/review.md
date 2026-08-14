# Guidelines for conducting systematic mapping studies in software engineering: An update

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Guidelines for conducting systematic mapping studies in software engineering: An update |
| 作者 | Kai Petersen; Sairam Vakkalanka; Ludwik Kuzniarz |
| 年份 | 2015 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 综述类型大类 | 🟦 SMS |
| 细分类型 / 原文自称 | mapping guideline update / systematic map of maps；52 篇 SMS |
| 本文角色 | 🔵 类SLR |
| 统计池资格 | 🟢 入池 |
| 证据成熟度 | 🟡 全文 |
| 样本单位 / 分母链 | 📚 综述 / 52 |
| 原生维度树类型 | 🔁 流程树 |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology；DOI 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 18 页；未做图表视觉级人工核对。 |
| 证据等级 | 全文文本级；复杂图表 / 附录矩阵待 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.1016/j.infsof.2015.03.007> |
| SE 子领域 | 软件工程 系统映射 方法学。 |
| A1 角色 | 从失败路径升级为全文级核心方法锚点：用于抽取 planning-conducting-reporting 流程、topic-independent dimensions、validity taxonomy、reporting structure、quality rubric。 |
| 是否目标证据池 | 否；它支撑综述方法学与 模式种子，不支撑某一目标 SE 主题的领域结论。 |
| 是否统计池 | 是，但仅限 A1 `survey_of_surveys/` 的方法学统计池；不能作为目标领域效果 / 因果统计证据。 |
| 一句话结论 | 这篇论文是 A1 中最关键的 SMS guideline update：它证明“维度模式”和“报告 / 效度 / 评价 rubric”本身可以从综述之综述中抽取、统计、回修。 |

## 2. 论文内容详读

### 2.1 研究目标与定位

本文的出发点是：2008 年的 系统映射 guideline 已经不足以覆盖后来软件工程 mapping studies 的真实做法，许多研究会组合多个 guideline，导致实践差异较大。因此作者通过对既有 mapping studies 做 系统映射，识别这些研究如何执行搜索、选择、分类、可视化、效度和报告，并据此更新 guideline。

这篇论文对 Paper2 的价值在于，它不仅说明“如何做 mapping”，还说明“如何从一批已有 mapping studies 中抽出方法 pattern，再反过来更新 guideline”。这与 A1/A2a 的定位完全一致：先从综述论文中抽模式，而不是直接写目标领域发现。

### 2.2 RQ 与方法流程

作者设置四个 RQ：

1. 哪些 guidelines 被用于 SE 系统映射 studies。
2. 这些 studies 覆盖哪些 SE topics。
3. 它们在哪里、何时发表。
4. 它们如何执行 系统映射 process，包括 study identification、分类方案和结果可视化。

方法上，作者使用 IEEE Xplore、ACM、Scopus、Inspec/Compendex；以 系统映射 相关词、software engineering、method / classification / guideline 等词构造检索式；用 EndNote 去重；先 title/abstract，再 full-text，再 backward snowballing；最终对纳入研究做 quality assessment 和数据抽取。

### 2.3 纳排、质量评价与抽取表

纳入标准包括：论文呈现 systematic 系统映射研究 的研究方法与结果、属于软件工程、发表在 2004--2012。排除标准包括 conference summary / editorial、guideline/template 本身、非 peer-reviewed、非英文、全文不可得、书籍 / 灰色文献、重复研究。

质量评价问题包括：mapping 动机是否清楚；mapping process 是否清楚定义；是否有该 mapping process 的 empirical evidence / 结果。数据抽取表覆盖 study ID、title、authors、year、SWEBOK area、venue、使用的 guidelines、search strategy、search type、classification scheme、visualization type。

这些字段可作为 A2a 对 SLR/SMS 文献的 extraction form 候选，仍需主线程裁决。

### 2.4 guideline update 与维度模式

本文把 mapping guideline 组织为三大阶段：planning、conducting、reporting。Planning 中包括 need identification / scoping、study identification、data extraction and classification、visualization、validity threats、evaluate the mapping。Conducting 强调执行搜索、筛选、抽取、分类和可视化；Reporting 强调标准化结构、可复用性和可比较性。

作者还抽出了可跨主题使用的 topic-independent dimensions，包括 research type、research method、study focus、venue；传统 contribution type 并不总是最通用。topic-specific classification 则可来自 emergent scheme 或既有知识体系，例如 SWEBOK / IEEE / ISO 标准。

对 Paper2 来说，这支持“维度 pattern 类似树结构”的判断：有横向通用维度，也有主题特化维度；两者需要由研究者裁决后组合，而不是由 LLM 自动一次性定死。

### 2.5 证据呈现、统计与评价 rubric

本文大量使用频数、比例、分布图、bubble plot、bar chart、pie diagram、Venn diagram、heatmap 和附录矩阵来呈现 mapping studies 的方法差异。作者还构建了用于评价 systematic map 质量的 action / rubric，并报告不同 studies 在 rubric 上的表现。

这说明 survey-of-surveys 不只是收摘要：它可以抽取“哪些维度被使用、哪些可视化被使用、哪些 validity 被报告、哪些 reporting 结构被采用”，并对这些方法维度做统计。这是 A1/A2b 后续大文库的统计目标候选。

### 2.6 效度威胁

作者在 §3.6 使用 descriptive validity、theoretical validity、generalizability、interpretive validity 等框架，讨论搜索漏检、单人筛选 / 抽取偏差、术语混淆、样本代表性和结论解释风险。其缓解方式包括 backward snowballing、reference set validation、抽取表、抽取回溯、纳排后的复查和明确 reporting。

这对 Paper2 有两个强启发：第一，agent 辅助抽取必须把单点自动判断升级为可回溯证据；第二，研究者裁决不是装饰，而是对 selection / extraction / interpretation bias 的核心缓解机制。

### 2.7 报告结构

本文建议 systematic map 报告结构尽量标准化，包括 Introduction、Related Work、Research Method、Results、Discussion / Conclusions 和 Appendix。Research Method 应包含 research question、search、study selection、data extraction、quality assessment、analysis and classification、validity evaluation。附录可保留纳入 / 排除边界论文与矩阵表。

这对 `survey_of_surveys/` 后续文库有直接价值：A2a/A2b 的单篇 review 和总账应显式记录 report structure pattern，而不能只写“这篇讲了什么”。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖 guideline 使用、SE topic、venue/year、mapping process execution。 | `paper_content.txt` §3.1。 | 可迁移为“方法实践如何被执行”的 survey-of-surveys RQ 模板。 | 不回答具体 SE 技术效果。 |
| dimension pattern | 抽出 topic-independent dimensions：research type、research method、study focus、venue；topic-specific classification 可来自 emergent / existing scheme。 | §5.1、Table 5、Appendix B。 | 高度可迁移为 A2a 初版维度模式库。 | 具体维度需与目标主题和研究者 meta-model 对齐。 |
| finding pattern | 从 mapping studies 的实践差异形成 guideline update、rubric 和改进建议。 | §5、§6。 | 可迁移为“统计方法实践 → guideline 修订”的 finding heuristic。 | finding 属方法学裁决，不是领域效果结论。 |
| evidence presentation pattern | 以流程图、频数表、分布图、可视化类型统计、quality rubric、附录矩阵呈现证据。 | Figure 1、Table 3、Table 8、Table 14、Appendix A/B。 | 可迁移到 A2b 的 pattern evidence dashboard。 | 图表和附录表格复杂，需 PDF 视觉核对。 |
| validity / threat pattern | 使用 descriptive/theoretical/generalizability/interpretive validity，记录单人筛选、漏检、分类误差和代表性风险。 | §3.6、§5.1.5、Table 13。 | 可迁移为 agent-assisted SLR 的 threat taxonomy。 | 需要补充 LLM/服务提供商漂移（provider drift）、prompt drift、schema revision bias 等现代风险。 |
| report structure pattern | 标准化 systematic map 报告结构，并建议纳入附录清单与排除边界。 | §5.3。 | 可迁移为 A2a/A2b 单篇 review 和最终论文 method/reporting 结构。 | Paper2 还要加入 human-in-the-loop、候选发现裁决和审计制品链。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 将研究目标定义为更新 mapping guideline，并明确为何单一 guideline 不足。 | A2a 可用“方法实践差异 → guideline update”作为综述之综述元模型。 | 不能把 guideline update 误写成领域事实。 |
| A1-M1 语料收集与纳排 | 数据库、检索式、时间窗、title/abstract/full-text、snowball、quality assessment 都有清楚记录。 | 可迁移为 A2b 完整文库检索和纳排总账模板。 | 单人筛选风险需要额外裁决 / double-check 记录。 |
| A1-M2 研究对象与主题语义 | 使用 SWEBOK area、topic categories、study focus 等定义研究对象语义。 | 可迁移为主题语义树和横向方法维度并存的字段设计。 | SWEBOK 与现代 LLM/agent 主题存在时代差异。 |
| A1-M3 方法 / 技术 / 干预 | 记录 search strategy、search type、classification scheme、visualization type、guideline adoption。 | 可迁移为“agent 做了哪些环节、人做了哪些环节、分类与可视化如何执行”的方法字段。 | 需扩展 LLM/agent role、prompting、工具链和交互日志字段。 |
| A1-M4 评价、证据与复现资产 | 有 data extraction form、validity schema、quality rubric、included studies appendix。 | 可迁移为字段证据、schema version、reviewer check、artifact completeness 的审计资产。 | 本文的开放制品要求不如 Paper2 高，不能降低审计标准。 |
| A1-M5 统计分析就绪 | 对 guideline、topic、venue、search、classification、visualization、rubric score 做计数与分布。 | 可迁移为 A2b 的方法学统计池。 | 只能做方法学频次 / 分布统计，不支持目标领域效果合成。 |
| A1-M6 research finding 形成与裁决 | 从方法实践统计形成更新 guideline 和质量评价建议。 | 可迁移为“统计观察 → 方法学 finding → researcher 裁决”的模板。 | 最终领域 finding 必须另由目标主题证据支持。 |

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **A1/A2a 本质上也是 guideline update 的前置工作**：我们不是为了堆论文，而是为了从 SE 综述实践中抽出适合 agentic SLR 的维度与证据规范。
2. **维度模式必须分通用层和主题层**：research type / venue / method 这类通用字段，与 LLM4STM / LLM4SE / MDE 等主题字段应分层组合。
3. **评价 rubric 可以成为方法贡献**：Paper2 可以为 agent-assisted SLR 提出审计制品完整性、字段证据完整性、finding 裁决完整性的 rubric。
4. **报告结构本身是可抽取对象**：后续写论文时，应把综述方法、字段表、统计观察、候选发现和裁决日志作为标准报告部件。
5. **效度威胁必须流程化**：每个阶段都要有风险与缓解，例如搜索、筛选、抽取、分类、统计、finding 形成、研究者裁决。

### 6.2 风险

1. 本文的数字链条和 Appendix B 很复杂，A2a 若要精确统计必须视觉核对，不能只依赖 `paper_content.txt`。
2. 2015 的 guideline update 仍未覆盖 LLM/agent/服务提供商漂移（provider drift）、prompt drift、schema drift 等新风险，Paper2 需要补充。
3. 该文以 mapping studies 为对象，不能直接告诉我们 LLM-assisted SLR 是否有效，只能告诉我们如何设计字段和审计方法。
4. 如果把本文纳入统计池，必须标注“方法学统计池”，避免与目标领域统计池混淆。

## 7. 待复核

1. 视觉核对 Figure 1（p.5）的 selection flow，特别是 7752 → 5082 → 60 → 43 → 54 → 44 → 52，并区分 +11、-10、+8 等边变化；不得继续写成旧式相加混合口径。
2. 视觉核对 Table 5（p.8--9）的 guideline comparison matrix。
3. 视觉核对 Figure 5--15（p.6--8）的分布 / 分类 / validity 图。
4. 视觉核对 Figure 16--19（p.9--13）中 search reflection、study selection、venue classification 和 research method classification。
5. 视觉核对 Table 8、Table 14、Figure 20--21（p.14--15）中的 rubric 与质量分布。
6. 若 A2a 要精确复用 Appendix B 的逐篇映射，需要人工检查 p.16--17 的 B.15--B.27 表格。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__codex.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__codex.md)、[../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__claude.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__claude.md)、[../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__deepseek.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `petersen-2015-mapping-guidelines-update` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；完整通读 1973 行（18 页全部，含 §1 引言至 §6 结论、Appendix A 包含/排除清单、Appendix B 表 B.15–B.27、References）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者元信息一致，DOI=10.1016/j.infsof.2015.03.007，IST 卷 64 (2015) pp. 1–18。 |
| 是否打开或核对 `paper.pdf` | 否（本轮以 `paper_content.txt` 全文为主，文本提取对所有 Table/Figure caption 和正文均可见；未做图表视觉级人工核对，复杂图(Fig.1 数字链、Fig.16 partition 图)留待 A2a）。 |
| 原文类型 | **SLR / SMS / 指南 混合**：系统映射研究 of 系统映射 studies (tertiary 性质) + 指南 update。 |
| 被编码样本单位 | **原始研究 = SE 领域已发表的 系统映射研究**（每个 研究 被作者按 Table 3 抽取表编码）。 |
| 样本数量 / 分母 | **52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (完整-text) → 54 (+11 snowball) → 44 (质量) → 52 (review of excluded 回补 8) 。 |
| 原生树类型 | **维度森林**（至少 4 棵互相独立的主干树：①抽取 form 树；②分类切面（分类 facet） 树；③指南 action / rubric 树；④效度 分类法 树）。 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**阅读范围**：完整通读 `paper_content.txt` 1–1973 行（18 页 + 18 页 References）；逐节核对 §1 Introduction、§2 Background and related work、§3 Method (含 §3.1 RQ, §3.2 Search, §3.3 Selection/QA, §3.4 数据抽取（数据抽取） Table 3, §3.5 Analysis, §3.6 Validity 5 子节)、§4 Results (含 4.1 频度、4.2 Topics SWEBOK、4.3 Venue、4.4 过程 含 4.4.1–4.4.6)、§5 Guideline updates (含 §5.1 计划（Planning） 5 子节、§5.2 执行（Conducting）、§5.3 报告（Reporting）、§5.4 Evaluate 含 Tables 8–14、§5.5 Dissemination)、§6 Conclusions、Appendix A、Appendix B (Tables B.15–B.27)、References 1–100。

**仅基于 text 的局限**：(a) Fig. 1 的数字流程链 `-10-17-5022-2666` 文本提取后顺序错乱，分母重建需 PDF 视觉核验；(b) Fig. 16 (Badampudi partition 圆 + snowball 三角) 是视觉示意，无法仅靠文本理解；(c) Fig. 3 / Fig. 4 / Fig. 5 / Fig. 7–15 的具体柱条数值只能从 Tables B.15–B.27 倒推（B 表给出 研究 list，可数得到，但需精核）；(d) Tables 9–13 的"bold 高亮分数"在文本中丢失，需 PDF 复核本研究自身的 rubric 评分位置。

**5–12 个最关键原文证据锚点**：

| # | 证据锚点 | 章节 / 表图 | 短引或释义 |
|---|---|---|---|
| E1 | RQ 1–4 全文表述 | §3.1 (line 217–229) | "RQ1: Which 指南 are followed... RQ2: Which SE topics are covered... RQ3: Where and when... RQ4: How was the 系统映射 流程 performed?" |
| E2 | Table 3 数据抽取表（12 字段）| §3.4 / Table 3 (line 392–408) | Study ID / Title / Author / Year (RQ3) / Area in SE = SWEBOK (RQ2) / Venue (RQ3) / Guidelines adopted (RQ1) / Search strategy (RQ4) / Search type {手工（manual）, 自动（automated）, 二者都有（both）} (RQ4) / 分类 schemes (RQ4) / Visualization type (RQ4)。 |
| E3 | 选择流程链 + 52 分母 | §3.3 / Fig. 1 / §3.6.2 | "57 原始研究"(snowball 后) → "52 mapping studies" (final, §3.6.2)；§4.4.3: "only 14 out of 52 studies"。 |
| E4 | Topic-independent facet 五元封闭枚举 | §4.4.4 / Fig. 12 / Table B.24 | 研究（Research） type, 研究（Research） 方法, Study focus, Contribution type, Venue。"Three new dimensions not highlighted by Petersen et al. [2] have been identified, namely venue, 研究 focus, and 研究方法（research method）." |
| E5 | 研究（Research） type 6 类封闭枚举 + 真值表 | Table 7 (line 1310–1326) + §4.4.4 | Evaluation research / Solution 提案 / Validation research / Philosophical / Opinion / Experience；R1–R6 真值表 6 conditions × 6 decisions（Used in practice, Novel solution, Empirical 评价, Conceptual 框架, Opinion about something, Authors' experience）。 |
| E6 | Search 子树（3+5+4+3 封闭枚举）| §4.4.2 / Figs 6–9 / Tables B.18–B.21 | 搜索策略: {数据库检索（database）, 滚雪球（snowballing）, 手工检索（manual）}；发展: {PICO, expert/librarian, iterative, keywords-from-known, standards}；评估: {test-set, expert eval, key authors' webpages, test–retest}；纳排: {objective criteria, additional reviewer + consensus, decision rules}。 |
| E7 | Visualization 6 类封闭枚举 | §4.4.5 / Fig. 14 / Table B.26 | {折线图（line）, 饼图（pie）, 柱状图（bar）, 气泡图（bubble）, Venn 图, 热力图（heatmap）}。 |
| E8 | Validity 5 类 分类法 | §3.6 / §5.1.5 | {Descriptive, Theoretical, Generalizability (内部/外部), Interpretive (≈ conclusion), Repeatability}。 |
| E9 | Table 5 指南 比较矩阵 | §5 / Table 5 (line 775–840) | 9 指南 × 30+ activities × {适用 ✓ / 不适用 ✗}；展示本研究合成的"完整 activity 全集"。 |
| E10 | Tables 8–13 rubric + Table 14 评分分布 | §5.4 / Tables 8–14 | 26 actions × 4 phases；4 rubrics(need / search strategy / search 评价 / 抽取-分类) 有序 scale {0,1,2,3}，1 rubric(效度) {0,1}；Table 14: 52 studies 在每个 rubric 上的频次分布。 |
| E11 | Tables B.15–B.27 逐研究关系边 | Appendix B (line 1559–1801) | 13 张关系表（topic, venue, 指南, search strategy, search dev, search eval, inc/excl, QA, 数据抽取, topic-indep, topic-related, visualization, 效度），全部分母=52。 |
| E12 | Validity 威胁 自评（§3.6.2 单人筛选）| §3.6.2 (line 432–438) | "The 研究 selection was conducted by an individual author, which is the main 威胁 to 效度"；缓解：first author 复审 + reference-set 验证。 |

### 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象**：52 篇 SE 系统映射 studies（含部分 tertiary studies），样本单位是"published SE 系统映射研究"。Appendix A 给出 included 与 excluded 完整 reference id 清单。
2. **是否有系统检索 / 纳排 / 数据抽取 / 编码方案**：**完全有**。Table 1 给出 4 个数据库的精确检索串；Table 2 给出每个 db 的命中数；Fig. 1 给出完整 PRISMA-like 流程链；§3.3 给出明确 inclusion / exclusion 标准（6+4 条）+ snowball；§3.3 给出 3 题 质量评价；Table 3 给出 12 字段 抽取 form；§3.5 给出"theme grouping then counting"分析方法。
3. **字段来源**：
   - **Extraction form**：Table 3 (Section 3.4)，每个字段直接绑定到一个 RQ。
   - **分类 模式**：双层 — (i) Section 4.4.4 + Fig. 12 + Table B.24 给出 topic-independent 切面（facets） 5 项；(ii) Section 4.4.4 + Fig. 13 + Table B.25 给出 topic-specific {emerging, existing scheme}；(iii) Table 7 给出 research type 真值决策表，是 Wieringa et al. [11] 的精化。
   - **Quality rubric**：Tables 8–13 + Table 14 (Section 5.4)，作者自行构造的 4+1 rubric。
   - **Validity 分类法**：来自 Petersen & Gencel [29]，5 类。
   - **报告（Reporting） structure**：§5.3 给出 6 部分推荐结构。
   - **Mapping table**：Table 5 (Section 5) 比较 9 个既有 指南 × 30+ 活动的覆盖度。
4. **RQ 与样本单位关系**：RQ 不是"树根"，而是 **抽取 form 字段的 owner**（Table 3 的 RQ 列把每个字段绑到 RQ1/2/3/4）。Section 4 按 RQ 组织结果。因此 RQ 在维度森林中扮演的是"字段 owner / 结果组织维度"，而非主树根。
5. **是否无系统样本库**：**有**。无需降级；本文具备完整 SMS 证据链，分母=52 稳定且可追溯到 Appendix B 各表。降级仅适用于:把它当 *Paper2 目标领域* 的统计源，而非把它本身当 SMS。

### 3. 原生样本编码维度森林

本文有 **4 棵互相独立的主干树**，每棵服务不同的作者目的。把它们合并为单树会破坏取值空间语义。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[森林根节点] Petersen 2015 系统映射指南更新（52 篇 软件工程系统映射研究）

== 树 1：数据抽取表单（Section 3.4 / Table 3；作者编码 52 篇研究所用） ==
├── 基本信息
│   ├── 研究编号：整数
│   ├── 文章标题：字符串
│   ├── 作者姓名：字符串集合
│   ├── 发表年份：2007..2012（RQ3）
│   ├── 软件工程领域：SWEBOK KA ∪ {教育（Education）、研究方法（Research Methods）}；RQ2；Table B.15
│   └── 发表源：字符串；RQ3
└── 映射研究过程字段
    ├── 采用的指南：10 个指南标签的多选；RQ1；Fig.5 / Table B.17
    ├── 检索策略：{数据库检索（database）, 滚雪球（snowballing）, 手工检索（manual）} 的多选；RQ4；Fig.6 / B.18
    ├── 检索类型：{手工（manual）, 自动（automated）, 二者都有（both）}；RQ4
    ├── 分类方案：字符串，细节见树 2；RQ4
    └── 可视化类型：6 个封闭标签的多选；RQ4；Fig.14 / B.26

== 树 2：分类切面树（Section 4.4.4；作者归纳出的 切面模式） ==
├── 主题无关切面（Fig.12 / B.24）
│   ├── 研究类型：{评价研究（评价）, 解决方案提案, 验证研究, 哲学性论文（philosophical）, 观点论文（opinion）, 经验论文（experience）}
│   │   └── 判定规则：Table 7 的 R1..R6 六条件真值表
│   ├── 研究方法：{调查（survey）, 案例研究（case study）, 受控实验（controlled experiment）, 行动研究（action research）, 民族志（ethnography）, 仿真（simulation）, 原型（prototyping）, 数学分析（mathematical analysis）} 多选
│   │   └── 与研究类型关系：验证集合（验证 set）∪ 评价集合（评价 set）∪ 二者都有（both）；Fig.19
│   ├── 研究焦点：{学术（academic）, 工业（industrial）, 政府（government）, 项目（project）, 组织（organization）}
│   ├── 贡献类型：{过程（process）, 方法, 模型, 工具, 指标}（Wieringa et al.）
│   └── 发表源分类：四层层级枚举（四层层级枚举），来自 芬兰教育部方案（芬兰教育部方案）；Fig.18
└── 主题相关切面（Fig.13 / B.25）
    ├── 新兴分类方案：通过 keywording 产生，类似开放编码
    └── 既有分类方案：{SWEBOK, IEEE 标准（IEEE std）, ISO/IEC 标准（ISO/IEC std）, ACM 词表（ACM Thesaurus）, ...}

== 树 3：映射研究流程活动 / 指南动作树（Section 5 / Table 5 / Table 8） ==
├── 规划阶段
│   ├── 研究必要性识别：说明动机（motivate）、定义目标（定义目标）、咨询受众（咨询受众）
│   ├── 研究识别
│   │   ├── 选择检索策略：{数据库检索（database）, 滚雪球（snowballing）, 手工检索（manual）}
│   │   ├── 开发检索式：{PICO(C), 咨询专家、迭代改进、从已知论文取关键词、标准 / 百科 / 词表（原字段标识保留于审计附录）}
│   │   ├── 评估检索式：{测试集（测试集）, 专家评价（专家评价）, 关键作者网页（关键作者网页）, 测试-复测（测试-复测）}
│   │   ├── 纳入 / 排除：{客观准则（客观准则）, 额外评审者 + 共识（额外评审者 + 共识）, 决策规则（决策规则）}
│   │   ├── 决策规则状态：Table 6 的 六格矩阵（6-cell matrix），R1×R2 ∈ {Inc, Unc, Exc}² → A..F
│   │   └── 是否做质量评估：布尔值
│   ├── 数据抽取与分类：见树 2
│   ├── 可视化：{折线图（line）, 饼图（pie）, 柱状图（bar）, 气泡图（bubble）, Venn 图, 热力图（heatmap）}
│   └── 有效性威胁：见树 4
├── 执行阶段：记录所有阶段（记录所有阶段）、迭代修订（迭代修订）、工具使用（工具使用）
└── 报告阶段：结构化模板，包含 引言（Intro）、相关工作（Related Work）、方法（Method）、结果（Results）、讨论 / 结论（Discussion/Conclusion）、附录（Appendix）

== 评分量规层（Tables 9–13；5 个独立量规） ==
├── R9 综述必要性：{0 无更新, 1 部分, 2 完整}
├── R10 检索策略选择：{0 无更新, 1 至少 2 种策略, 2 三种策略齐全}
├── R11 检索评估：0..3，组合 检索可靠性（search reliability）与纳排可靠性（inc/excl reliability）
├── R12 抽取与分类：0..3
└── R13 研究有效性：{0 未报告威胁（未报告威胁）, 1 描述了威胁（描述了威胁）}

== 树 4：有效性威胁分类法（Section 3.6 / 5.1.5） ==
├── 描述有效性：数据收集表（数据收集表）、可复查抽取（可复查抽取） 等缓解手段
├── 理论有效性：发表偏倚（发表偏倚）、研究者选择偏倚（研究者选择偏倚）、样本总体质量（样本总体质量）、术语混淆（术语混淆） 等子威胁
├── 可推广性：内部 / 外部
├── 解释有效性：近似 结论有效性（conclusion 效度）
└── 可重复性：详细报告（详细报告）、指南使用（指南使用）
```

> 注：每棵树都可独立产出统计。例如 Table B.18 给出 T1 中 search_strategy 字段在 52 篇上的逐研究映射；Table B.24 给出 T2 中 topic_independent facet 的逐研究映射；Table 14 给出 T3 rubric 的频数分布；§4.4.6 + Table B.27 给出 T4 是否被讨论的 52 分母二值统计。

### 4. 叶子维度表（精选 14 个有完整原文证据的叶子；非全集）

> 说明：仅列出**有原文封闭枚举 / 数值分母 / 真值表 / 有序 scale**的核心叶子；T1 的 研究_id/title/author 等 trivial general fields 省略。完整叶子全集 ≥30 项，留 A2a 精核。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 area_in_se | SWEBOK 知识域 | T1.general | Table 3 (RQ2) + Table B.15 | 系统映射研究 所属 SE 知识域 | 11 类: software_quality / 工具&方法 / 流程 / management / configuration / testing / construction / design / requirements / research_methods / education | 层级枚举 (SWEBOK + 2 新增) | 不可缺；52 全覆盖 | 主题分布频次 (52 分母, Table B.15) | 识别 SE 主题覆盖 缺口（gap） (e.g., education, config mgmt 弱) | E2, E11, §4.2 | SWEBOK 时代差异需注意；现代主题需扩展 |
| L02 指南_adopted | 所采用 指南 | T1.流程 | Table 3 (RQ1) + Fig.5 + Table B.17 | 该 研究 引用为方法依据的 指南 | 10 项封闭枚举: {Kitchenham2004, Kitchenham&Charters2007, Petersen2008, Budgen2008, Arksey&O'Malley2005, Dybå&Dingsøyr2008, Bailey2007, Petticrew&Roberts2006, Biolchini2005, Jorgensen&Shepperd2007, Durham_template} | 多选 封闭枚举 (集合并集) | 0 也是有效值 (无 指南) | 24/52 用 >1 指南 (§4.4.1) | 揭示 指南 不足 → motivate update | E2, E11, §4.4.1 | 仅限 SE SMS 内；不能迁移到 ML/NLP venues |
| L03 search_strategy | 搜索策略组合 | T1.流程 / T3.研究_identification | Table 3 (RQ4) + Fig.6 + Table B.18 | 研究 实际采用的 search 渠道 | {数据库检索（database）, 滚雪球（snowballing）, 手工检索（manual）} 任意子集 | 多选 封闭枚举 | 不可缺；至少 1 项 | 52 分母频次；最常见 = database (49/52 from B.18) | snowball-only / manual-only 极少 → 暴露过度依赖 db search 风险 | E2, E6, E11 | 适用 SMS；SLR 可能侧重不同 |
| L04 search_development | 搜索开发策略 | T3.研究_identification | §4.4.2 + Fig.7 + Table B.19 | 构造 search string 的方法 | {PICO(C), 专家 / 图书馆员, 迭代改进, 从已知论文提取关键词, 标准 / 百科 / 词表} 子集 | 多选 封闭枚举 | 可缺（部分 研究 未报告）| 频次见 B.19；PICO=11, keywords_from_known=11, standards=7 | 识别低使用率但有效的策略 (e.g., PICO 仅 11/52) | E6, §4.4.2, Table B.19 | -- |
| L05 search_evaluation | 搜索评估策略 | T3.研究_identification | §4.4.2 + Fig.8 + Table B.20 | 验证检索完整性的方法 | {测试集（测试集）_of_known_papers, 专家评价（专家评价）, key_authors_webpages, 测试-复测（测试-复测）} 子集 | 多选 封闭枚举 | 可缺；许多 研究 无评估 | 测试集（测试集）=8, expert=1, webpages=1, 测试-复测（测试-复测）=1 (B.20) | 暴露 search 不被验证的普遍问题 | E6, §4.4.2 | -- |
| L06 inc_excl_strategy | 纳排可靠性策略 | T3.研究_identification | §4.4.2 + Fig.9 + Table B.21 + Table 6 | 提高 inc/excl 可靠性的策略 | {识别客观准则, 额外评审者 + 共识, 决策规则（原字段标识保留于审计附录）} 子集 | 多选 封闭枚举 + Table 6 状态矩阵 | 可缺 | additional_reviewer 最常用 | 揭示 决策规则 仅 4/52 使用，但 Ali&Petersen 证明有效 | E6, Table 6, Table B.21 | -- |
| L07 quality_assessment | 是否做 QA | T3.研究_identification | §4.4.3 + Fig.10 + Table B.22 | 是否对 原始研究 做质量评估 | {yes, no} | 布尔 | 不可缺；52 全覆盖 | 14/52 yes; 38/52 no (§4.4.3) | "QA 在 SMS 中并不强制" 的直接证据 | E11, §4.4.3 | -- |
| L08 data_抽取_reliability | 抽取可靠性策略 | T3.data_抽取_分类 | §4.4.4 + Fig.11 + Table B.23 | 提高 抽取 可靠性的方法 | {识别客观准则, 额外评审者 + 共识, 测试-复测（原字段标识保留于审计附录）} 子集 | 多选 封闭枚举 | 可缺 | 频次见 B.23 | 与 inc/excl 模式相似但 N 更低，揭示薄弱环节 | §4.4.4, Table B.23 | -- |
| L09 topic_independent_切面（facets） | 主题无关分类 facet | T2.topic_independent | §4.4.4 + Fig.12 + Table B.24 | 该 研究 使用的横向分类维度 | {研究方法, 研究类型, 研究焦点, 贡献类型, 发表源} 子集 | 多选 封闭枚举 | 可缺 (一些 研究 无 facet) | venue=27, research_type=21, research_method=17, 研究_focus=11, contribution_type=6 | 揭示 venue/方法/type 是主流；contribution_type 边缘化 | E4, E11, §4.4.4 | -- |
| L10 research_type | 研究类型分类 | T2.topic_independent.research_type | Table 7 (§5.1.3) | 单个 原始研究 的研究类型 | {evaluation_research, solution_proposal, validation_research, philosophical_paper, opinion_paper, experience_paper} | 完整封闭枚举 (Wieringa et al. + Table 7 真值表) | 决策表必返回 ≥1 | 真值表精确判定 (T/F over 6 条件) | Table 7 真值表可作为候选迁移启发；后续必须经 A2a 证据核验和研究者裁决后再用于 Paper2 编码规则 | E5, Table 7 | research type 真值表对 LLM 智能体 抽取尤其有用 |
| L11 research_method | 研究方法 | T2.topic_independent.research_method | §5.1.3 + Fig.19 | 实证方法分类 | {调查（survey）, 案例研究（case_研究）, 受控实验（controlled_experiment）, 行动研究（action_research）, 民族志（ethnography）, 仿真（simulation）, 原型（prototyping）, 数学分析（mathematical_analysis）} | 封闭枚举 + Fig.19 双归属映射 (验证 vs 评价) | -- | 多分类 (一个 方法 可属两类) | Fig.19 给出 方法→research_type 关系边 → 可作完整性约束检查 | E4, Fig.19, §5.1.3 | -- |
| L12 visualization_types | 可视化类型 | T1.流程 / T3.planning.visualization | Table 3 (RQ4) + Fig.14 + Table B.26 | 研究 用的呈现方式 | {折线图（line）, 饼图（pie）, 柱状图（bar）, 气泡图（bubble）, Venn 图, 热力图（heatmap）} 子集 | 多选 封闭枚举 | 可缺 | bar=22, bubble=23, pie=12, line=2, Venn=3, heatmap=1 (B.26) | heatmap 严重低使用 (1/52) 是潜在 发现 | E7, E11 | -- |
| L13 validity_分类法 | 效度分类 | T4 | §3.6 + §5.1.5 | 研究 报告的 效度 维度 | {descriptive, theoretical, generalizability_internal, generalizability_external, interpretive, repeatability} | 封闭枚举 (5 类 + repeatability) | 可缺 | 45/52 报告 效度 (B.27) | 暴露 7/52 不报告 → 报告规范缺失 | E8, E11, §5.1.5 | 现代风险 (LLM/服务提供商漂移（provider drift）) 需另立 |
| L14 rubric_scores | 质量评分 (4+1 rubric) | T3 评分层 | Tables 9–13 + Table 14 | 该 研究 在每个 rubric 上的得分 | need∈{0,1,2}, search_strat∈{0,1,2}, search_eval∈{0,1,2,3}, extract_class∈{0,1,2,3}, 效度∈{0,1} | 5 独立 有序 scale | 全部强制评分 | Table 14 给出 52 篇分布；median ratio=33% (§5.4) | 这是首个 SMS 的 质量量规 实证分布，可作 baseline | E10, Tables 9–13, Table 14 | rubric 仅适合 SMS，不能直接套到 SLR / experimental |

### 5. 关系边表

本文 native 模式 富含**显式关系边**：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R01 研究↦指南 | 原始研究 | 采纳 | 已采纳指南集合 | 10 项 (L02) 子集 | 0=未声明 | Table B.17 | 频次 + 共现统计（52 篇中 24 篇使用超过 1 个指南） |
| R02 研究↦area | primary_study | covers | area_in_se | SWEBOK 11 类 (L01) | 必填 | Table B.15 | 主题分布；缺口（gap） 识别 |
| R03 研究↦venue | primary_study | published_in | venue_分类 | Fig.18 4 级层级 | 必填 | Tables 4, B.16 | venue 集中度；top-3 = IST(14), EASE(8), ESEM(4) |
| R04 研究↦search_strategy | primary_study | uses | search_strategy | L03 子集 | 必填 | Table B.18 | -- |
| R05 研究↦topic_indep_facet | primary_study | classified_by | topic_independent_切面（facets） | L09 子集 | 可空 | Table B.24 | facet 选择模式 |
| R06 research_method↦research_type | research_method | 归属 | {验证, 评价, both} | Fig.19 双向映射 | -- | Fig.19, §5.1.3 | **模式 内在约束**：可用作 Paper2 自动一致性检查 |
| R07 研究↦rubric_action | primary_study | applied | rubric_action (26 items) | 0/1 (Table 8 形态) | -- | Table 8 + Table 14 | 给出 质量 ratio |
| R08 指南↦activity | 指南 (10 项) | covers | activity (Table 5 中 30+ activities) | {✓, ✗} | -- | Table 5 | 指南 完整度对比矩阵 (本文核心贡献之一) |
| R09 inc/excl decision | reviewer pair (R1, R2) | combines_to | decision_state | {A, B, C, D, E, F} via Table 6 | -- | Table 6 | 决策规则代数 |
| R10 research_type decision | 研究 traits | maps_to | research_type | Table 7 R1..R6 真值表 | 真值表覆盖全部组合 | Table 7 | **完整布尔真值表 模式**, A2a 可作为候选复用 |

> 说明：R06、R08、R09、R10 是本文最有价值的**结构化关系**，远超普通 SMS 的字段平铺。Paper2 应优先借鉴这些"模式 内一致性约束"模式。

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 原文中由字段 / 统计表支持的统计观察（关键原文依据，分母明确；A2a 前仍为候选）

| 统计观察 | 证据 | 分母 |
|---|---|---|
| Kitchenham&Charters [1] 与 Petersen [2] 是最常用的两个 指南；24/52 研究 用 >1 指南 | §4.4.1, Fig.5, Table B.17 | 52 |
| 数据库检索是最常用搜索策略；snowball/manual 仅作补充 | Table B.18 | 52 |
| 仅 14/52 (27%) 研究 做了 质量评价 | §4.4.3, Fig.10, Table B.22 | 52 |
| topic_independent facet 中 venue 出现最频繁(27)；contribution_type 仅 6/52 | §4.4.4, Fig.12, Table B.24 | 52 |
| 多数 研究 用 emerging 分类 (open-coding-like) 而非 existing scheme | §4.4.4, Fig.13, Table B.25 | 52 |
| Visualization: bubble(23) ≈ bar(22) > pie(12) >> Venn(3) > line(2) > heatmap(1) | Table B.26 | 52 |
| 45/52 (87%) 研究 报告 效度 威胁 | Table B.27, Fig.15 | 52 |
| Rubric 质量 ratio 中位数 = 33%；25% 的 研究 ≥ 40% | §5.4, Fig.20, Table 14 | 52 |
| 期刊 的 rubric ratio 中位数 > 会议 | Fig.21, §5.5 | 52 |
| SE 主题覆盖：testing 最多；configuration mgmt 与 education 弱 | Table B.15, §4.2 | 52 |

#### 6.2 原文 discussion / 推荐 / 路线图 中提出的候选发现

| 候选发现 | 类型 | 强度 |
|---|---|---|
| 单一 指南 不足以指导完整 SMS → 需要 update | 推荐 | 强（由 R01 频次支持） |
| 应使用 venue, research_type, research_method 三个 facet 作为 topic-independent 分类 默认 | 推荐 | 中（基于 facet 频次） |
| 应避免对 SMS 设过严的 纳入标准 (e.g., 要求 评价) | 指南 | 中（理论论证） |
| Decision rules 在 inc/excl 中虽未被广泛采用，但实证有效 (Ali&Petersen 引文) | candidate_heuristic | 中（外部引文支持） |
| Snowball 单用 + good start set 可能达到 db search 完整度 (Wohlin 2014 引文) | candidate_heuristic | 中（外部引文） |
| SMS 不应追求"找到所有"，应追求"good sample" | methodological_seed | 强（多次重复，Wohlin 2013 引文+本文重申） |

#### 6.3 对 Paper2 可迁移的方法学启发

1. **数据抽取表绑定 RQ**（Table 3 列 `RQ`）——Paper2 的 LLM-智能体 抽取 form 也应让每个字段标注 owner RQ，便于回溯。
2. **真值决策表分类**（Table 7）——比简单 free-form prompt 更可靠；适合 LLM 智能体 + post-hoc rule check 二级验证。
3. **模式 内在关系约束**（R06: research_method↔research_type）——可作为 Paper2 自动一致性 guard。
4. **多 指南 比较矩阵**（Table 5）——审计同一 task 上不同 指南 的覆盖差异，是 模式种子（schema_seed） 反向产生新维度的方法学样板。
5. **Quality rubric 有序 scale**（Tables 9–13）——给出 0/1/2/3 的精确分级描述（"None / Min / Partial / Full"），可迁移作 LLM-judge 有序 rubric 模板。
6. **报告结构标准化**（§5.3）——Paper2 在 SUMMARY.md / desc.md 中应固定 sub-sections，便于跨论文比较。

#### 6.4 绝不能迁移的领域结论

1. SWEBOK 11 类不是普适分类法，仅适用 2012 前 SE。
2. "指南 X 比 指南 Y 更好"这种结论本文未做，Paper2 也不应外推。
3. rubric ratio 33% 是 2012 前 SE SMS 的实证基线，**不能**外推为"现代 LLM-assisted SLR 应达到 ≥33%"或类似规范性指标。
4. 效度 分类法 5 类未涵盖 LLM/服务提供商漂移（provider drift）、prompt drift、模式 revision bias 等现代风险。

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。

| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 强 | 本文以“对 SE 系统映射研究做系统映射并更新 mapping guideline”为任务，RQ 覆盖 guideline 使用、SE topic、venue/year 与 mapping process 执行。 | `review.md` §2.1、§2.2、维度树复原 E1；`evidence_chain.md` A.3 `clm-petersen-2015-mapping-guidelines-update-type` |
| S2 语料收集与筛选 | 强 | 有数据库、检索式、时间窗、去重、题摘、全文、snowballing、QA 和回补排除研究；57 是 QA 中间候选，52 是 final included mapping studies 分母。 | `paper_content.txt` §3.2--§3.3；Fig. 1；`review.md` 维度树 E3、S2 行 |
| S3 原生维度树/样本编码对象 | 强 | 被编码样本单位是 52 篇 SE 系统映射研究，原生结构是抽取表单树、分类切面树、guideline action/rubric 树和 validity taxonomy 树组成的维度森林。 | `review.md` 维度树复原 §0、§2、§3；`evidence_chain.md` A.2 `ev-petersen-2015-mapping-guidelines-update-unit`、`ev-petersen-2015-mapping-guidelines-update-tree` |
| S4 字段级证据 | 中 | Table 3 与 Appendix B 支撑字段级编码，但当前核心证据多为 not_verified / 待 A2a 图表核验；字段存在性强，逐样本表格数值仍待精核。 | `review.md` S4 行、叶子表；`evidence_chain.md` A.2 `ev-petersen-2015-mapping-guidelines-update-tree`、`ev-petersen-2015-mapping-guidelines-update-denom` |
| S5 维度模式演化 | 强 | 本文通过比较既有 guidelines 与实际 SMS 做法形成 guideline update；新识别维度包括 venue、study focus、research method，最终推荐通用 facets 为 venue、research type、research method。 | `review.md` §2.4、§3、维度树复原 §3、§6.2；E4、E9；`audits/a1-s1s8-19x1/adjudications/petersen-2015-mapping-guidelines-update.md` |
| S6 统计分析 | 强 | 对 guideline adoption、search、QA、classification、visualization、validity 和 rubric scores 有分母明确统计；A2a 前不作最终统计结论。 | `review.md` 维度树 §6.1、S6 行 |
| S7 候选 finding | 强 | 候选 finding 主要是方法学发现：单一 guideline 不足、需更新指南、topic-independent facets 可复用、SMS 应追求 good sample、rubric 可评价报告质量。 | `review.md` §3、§6.1、维度树复原 §6.2、§6.3 |
| S8 研究者/作者质疑与裁决 | 中 | 本文没有完整裁决日志，但讨论单人筛选/抽取偏差，并给出 first-author 复审、reference-set validation、additional reviewer + consensus、decision rules 等缓解机制。 | `review.md` §2.6、§4、维度树复原 E12、L06、R09 |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

**裁决：保留为 `survey_of_surveys` S1--S8 主统计池候选，但只进入方法学 / schema 统计池；A2a 页码、表图和 Appendix B 逐研究映射精核前，不进入最终定量发现。**

理由：本文不是纯 guideline 文本。摘要和 §3 明确说明作者执行了 **systematic mapping study of systematic maps**，最终样本单位是 **52 篇 SE 系统映射研究**，并用 Table 3 抽取表、§4 统计结果、Appendix B 逐研究关系表支撑 RQ1--RQ4；同时 §5 将这些统计与既有 SLR/SMS 指南比较后形成 **guideline update**。因此它可以统计“综述之综述如何抽取字段、形成维度、做方法学统计与修订指南”，但不能作为 Paper2 目标 SE 领域效果 / 因果结论的统计来源。分母口径应使用 final included **N=52 mapping studies**；57 只是 quality assessment 中间候选。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要写明目标是识别 systematic mapping process 如何执行并据此更新 guideline；§3.1 给出 RQ1--RQ4，覆盖采用哪些 guidelines、SE topics、发表时间地点、mapping process 如何执行。 | 顶层任务是“对 SE systematic maps 做 systematic map，并将统计结果转化为 mapping guideline update”；RQ 是字段 owner，不是单一树根。 | **强，合格候选**；可统计为 mapping-of-maps / guideline-update 型任务设定，但仅限方法学池。 | 核对摘要、§1 contribution、§3.1 RQ 的正式页码与原文排版；确认 DOI final 与本地 PDF 一致。 |
| S2 语料收集与筛选 | §3.2 给出 IEEE、ACM、Scopus、Inspec/Compendex 检索式和命中数；§3.3 给出纳排、title/abstract、full-text、backward snowballing、QA、first-author validation 与排除研究回查；Fig. 1 给出流程链。 | 检索漏斗树包括数据库检索、去重与时间窗、题摘筛选、全文筛选、滚雪球、质量评价、validation set 与 excluded review 回补。 | **强，合格候选**；可入“语料筛选流程 / 分母链”统计池；最终分母应为 52，不应把 57 写成 included studies。 | 视觉核对 Fig. 1 的 7752、5082、60、43、54、44、52 等数字链；复核 Table 1/2 和 Appendix A included/excluded 清单。 |
| S3 原生维度树/样本编码对象 | §3.4 Table 3 给出抽取表；§4 按 RQ 汇总；Appendix B Tables B.15--B.27 给出逐研究映射；`review.md` 已裁决样本单位为 52 篇 SE systematic mapping studies。 | 原生结构是维度森林：数据抽取表单树、classification facet 树、guideline action / rubric 树、validity taxonomy 树，共享“52 篇 mapping studies”样本单位。 | **强，合格候选**；可作为“同一样本单位上的多根维度森林”统计样本。 | 核对 Table 3 列名、RQ 绑定关系、Appendix B 全部表格是否均以同一 52 分母展开；检查表格跨页无漏项。 |
| S4 字段级证据 | Table 3 字段包括 study id、title、author、year、SWEBOK area、venue、guidelines、search strategy、search type、classification schemes、visualization type；Appendix B 给出 topic、venue、guideline、search、QA、facet、visualization、validity 等逐研究关系。 | 字段层可复原为 bibliographic fields、SE topic fields、process fields、classification fields、visualization fields、validity fields 和 rubric fields。 | **中到强，文本级候选**；字段存在性强，但逐样本取值和计数需 A2a 后才能进入最终统计。 | 精核 Tables B.15--B.27 每张表的行数、列名、缺失值语义和 OCR 残留；复核 Figure 3--15 与 Appendix B 倒推计数是否一致。 |
| S5 维度模式演化 | §4.4.4 识别 topic-independent facets，指出 Petersen 2008 未强调的新维度为 venue、study focus、research method；§5 与 Table 5 比较既有 guidelines，§5.1.3 最终鼓励使用 venue、research type、research method。 | 模式演化不是代码本迭代日志，而是“已有指南覆盖差异 + 实际 SMS 统计实践 → 更新后的通用 facet 与活动清单”。需区分新识别维度和最终推荐 facet。 | **强，合格候选**；可入“方法实践统计如何驱动 schema/guideline 修订”统计池。 | 复核 Table 5 guideline comparison matrix、Fig. 12、Table B.24、§5.1.3 相关段落；避免把 contribution type 或 study focus 误写为最终推荐三元组。 |
| S6 统计分析 | §3.5 明确 tabulate、visualize、theme grouping and counting；§4 对 guideline adoption、topics、venues、search、QA、classification、visualization、validity 做频数统计；§5.4 Table 14 与 Fig. 20--21 报告 rubric 分布。 | 统计从字段树派生：52 分母上的 guideline、topic、venue、search、QA、facet、visualization、validity 和 rubric ratio 等方法学统计。 | **强，合格候选**；可作为方法学统计池样本，A2a 前不得并入最终跨论文定量发现。 | 逐项核对 §4 图表、Table 14、Fig. 20--21 的数值；确认 median quality ratio、25% threshold、journal/conference 对比等表述。 |
| S7 候选 finding | §6 总结多指南并用、单一 guideline 不足、需要 updated guideline；§5.1.3 推荐通用 facets；§5.4 提出 evaluation rubric；§6 强调 good sample / representation 比单纯更多研究更重要。 | 候选 finding 链条是“字段统计观察 → 方法学解释 → guideline update / rubric / reporting 建议”，不是 SE 目标领域技术效果结论。 | **强但限界**；可入“统计观察转方法学 finding”模式池；不得迁移为 LLM4STM 或其他目标领域发现。 | 将每个 finding 回连到 RQ、图表或 Table 5/8/14；核对作者 discussion 与我们方法启发之间的边界。 |
| S8 研究者/作者质疑与裁决 | §3.3 承认 title/abstract 筛选由单一作者完成，是 reliability threat；随后用 first-author validation sets、回查排除研究缓解；§3.4 说明第二作者抽取、第一作者 trace-back review；§3.6 系统讨论 validity。 | 可复原为 threat-aware validation / checker 机制和 guideline-level consensus 建议；不是完整双人独立筛选、完整 coding adjudication 或 inter-rater 日志。 | **中，候选但需降级**；可统计为“有复核与效度缓解”，不能统计为“完整人工裁决日志”。 | 核对 §3.3、§3.4、§3.6、Fig. 17、Table 6；确认单人筛选风险与 first-author validation 的边界表述。 |

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
