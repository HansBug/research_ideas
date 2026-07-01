# Guidelines for conducting systematic mapping studies in software engineering: An update

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Guidelines for conducting systematic mapping studies in software engineering: An update |
| 作者 | Kai Petersen; Sairam Vakkalanka; Ludwik Kuzniarz |
| 年份 | 2015 |
| 类型 | 系统映射 guideline update；对 SE 系统映射 studies 的 systematic map。 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology；DOI 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 18 页；未做图表视觉级人工核对。 |
| 证据等级 | 全文文本级；复杂图表 / 附录矩阵待 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.1016/j.infsof.2015.03.007> |
| 综述类型 | mapping guideline update / 系统映射之系统映射（systematic map of systematic maps）。 |
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

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> [!WARNING] v1-deprecated: 本节为 A1-DT v1 历史草稿 / 迁移来源，只能作为返修来源和历史证据，不是 A1-DT v2 当前事实口径。v2 事实以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
映射指南更新模式（mapping_guideline_update_pattern）
├── 指南使用
│   ├── 遵循的指南
│   ├── 组合使用的指南
│   ├── 缺失的指南覆盖
│   └── 更新理由
├── 映射研究过程
│   ├── 规划：必要性识别、范围界定、研究识别计划、抽取分类计划、可视化计划、有效性计划
│   ├── 执行：数据库检索、检索类型、筛选阶段、质量评估、数据抽取表单、分类方案
│   └── 报告：方法章节结构、结果结构、纳入 / 排除附录、可重复性细节
├── 维度
│   ├── 主题无关：研究类型、研究方法、研究焦点、发表源
│   └── 主题相关：新兴方案、既有方案
├── 可视化与统计
│   ├── 频次表
│   ├── 分布图
│   ├── 气泡图
│   ├── Venn 图
│   ├── heatmap
│   └── 质量量规分数
└── 有效性与质量
    ├── 描述有效性
    ├── 理论有效性
    ├── 可推广性
    ├── 解释有效性
    ├── 可重复性
    └── 研究者偏倚缓解
```

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

1. 视觉核对 Figure 1（p.5）的 selection flow，特别是 7752、5082、60、43、54、44、52+8+11 等链条。
2. 视觉核对 Table 5（p.8--9）的 guideline comparison matrix。
3. 视觉核对 Figure 5--15（p.6--8）的分布 / 分类 / validity 图。
4. 视觉核对 Figure 16--19（p.9--13）中 search reflection、study selection、venue classification 和 research method classification。
5. 视觉核对 Table 8、Table 14、Figure 20--21（p.14--15）中的 rubric 与质量分布。
6. 若 A2a 要精确复用 Appendix B 的逐篇映射，需要人工检查 p.16--17 的 B.15--B.27 表格。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__codex.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__codex.md)、[../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__claude.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__claude.md)、[../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__deepseek.md](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

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
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

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
| L10 research_type | 研究类型分类 | T2.topic_independent.research_type | Table 7 (§5.1.3) | 单个 原始研究 的研究类型 | {evaluation_research, solution_proposal, validation_research, philosophical_paper, opinion_paper, experience_paper} | 完整封闭枚举 (Wieringa et al. + Table 7 真值表) | 决策表必返回 ≥1 | 真值表精确判定 (T/F over 6 条件) | Table 7 真值表历史草稿曾提出迁移建议；当前禁止直接采信作为 Paper2 编码规则 | E5, Table 7 | research type 真值表对 LLM 智能体 抽取尤其有用 |
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

### 7. 对旧版 `review.md` 的返修来源（C / I / M 分级）

#### C（critical，影响维度树准确性 / 学术证据链）

| # | 问题 | 建议 |
|---|---|---|
| C1 | A1-DT v2 "维度树结构"（review.md line 203–216）仍以单棵树呈现，把 5 个主干强制压成 b1..b5（planning/conducting/报告方式/质量量规/topic-indep dim），实际原文是**4 棵独立树的森林**（抽取 form / 分类切面（分类 facet） / 流程+rubric / 效度），合并破坏 模式 语义。 | 改写为 §3 所示**维度森林**结构，每棵树独立列叶子；标注它们的服务对象不同（编码自己 52 篇 vs. 向后续 研究 推荐）。 |
| C2 | 叶子维度表（review.md line 218–227）的六个 `leaf-*` 仍是通用六叶（scope/语料/分类法/方法/证据/发现），未升级 Table 3 的 12 个 抽取 items、Fig.12 的 5 个 切面（facets）、Tables 9–13 的 4+1 有序 rubric 为真正的叶子。 | 用本审计 §4 的 14 个叶子（L01..L14）替换通用六叶；明确每个叶子的取值空间类型（封闭枚举 / 真值表 / 有序 / 多选）。 |
| C3 | A.2 证据账本（EV-001..004）证据强度全部 `not_verified`。但 Table 3、Table 7、Tables 9–13、Tables B.15–B.27 都是**已在 paper_content.txt 中直接可见的封闭枚举与频次表**，证据强度应升级为 `local_历史草稿旧强度（当前禁止采信）`（仅 Fig.1 数字链、Fig.16 partition 图等需 PDF 视觉核验保留 `not_verified`）。 | 把 EV 拆为 ≥6 条，分别绑到 Table 3 / Table 5 / Table 7 / Tables 8–13 / Tables B.15–B.27 / §3.6 效度；其中 Table B.15–B.27 + Table 3 + Table 7 升级为 `verified` 或 `local_历史草稿旧强度（当前禁止采信）`。 |
| C4 | "原文模式主树（19×3 审计后返修）"（review.md line 249–258）的叶子仍是抽象短语（"field list、map metadata"），未列具体字段名。 | 在该表 "叶子 / 取值空间种子" 列直接写出具体字段名与取值空间，如 `T1.抽取_form: {研究_id:int, year:[2007..2012], 指南: multi∈{10 closed labels}, search_type:{manual|auto|both}, ...}`。 |

#### I（important，影响统计池资格与候选发现 形成）

| # | 问题 | 建议 |
|---|---|---|
| I1 | "快速结论卡片"标注"是否目标证据池: 否"——正确；但"是否统计池: 是，但仅限 A1 `survey_of_surveys/` 的方法学统计池"应进一步明确**分母=52**，且所有 Appendix B 表是 ready-to-statistics 的关系边。 | 在卡片中加一行 "分母 / 样本单位: 52 included 软件工程系统映射研究 (per §3.6.2; Appendix A); per-facet 频次表已 ready (Tables B.15–B.27)"。 |
| I2 | SUMMARY.md（推测）中如果当前对本论文标注"原生树类型: 单树"或"统计池资格: 否"，与原文事实不符。 | 改为"原生树类型: 维度森林（4 棵）"+"统计池资格: 是（方法学池），分母=52"。 |
| I3 | 缺少关系边表。原文 R06 (方法↔type)、R08 (指南×activity)、R09 (Table 6)、R10 (Table 7) 是核心 模式 关系，未被记录。 | 新增 §A.x "关系边表"，按本审计 §5 列出 R01–R10。 |
| I4 | 候选发现 与 statistical observation 未分层。现 `clm-...-发现-boundary` 笼统说"最终研究发现（最终研究发现） 必须经过跨论文证据"——正确但太抽象。 | 在 review.md 新增 §"统计观察 vs. 候选发现" 小节，按本审计 §6.1/§6.2 区分（10 条强统计观察 + 6 条 候选发现）。 |

#### M（minor，工程改进）

| # | 问题 | 建议 |
|---|---|---|
| M1 | "历史草稿（已迁移）"块（line 103–157）保留了一棵旧 ASCII 树，已 deprecated 但仍占大量篇幅。 | 折叠或移到独立 `history.md`；review.md 主体保持单一事实源。 |
| M2 | "六类 模式 抽取"表（line 81–89）的"证据锚点"列仍写 `§3.1` 等粗粒度章节号，未到表号 / 图号。 | 加入具体 Table B.x / Table 7 / Fig.12 等精锚点。 |
| M3 | 时间字段（如待复核区）使用相对表述（"留待 A2a"），未给出 yyyy-mm-dd hh:mm:ss 时间戳。 | 在更新日志中加 `2026-06-30 hh:mm:ss` 完成时间戳。 |
| M4 | "A1-M0--M6 元维度贡献"表（line 93–101）仍是跨论文投影解释，应明确标注"非原文 模式"。 | 在该表上方加 callout: "本表是 Paper2 跨论文投影提示，不是本文原生维度树"。 |

### 8. 历史审计草案归档（禁止消费为事实真源）

> [!WARNING] 历史草案归档，禁止消费为事实真源：本节仅保留 A1-DT v2 形成过程中的审计草稿，不得作为当前证据强度、SUMMARY 统计池、正式维度树或正式结论-证据映射使用。若本节与文末正式 `### A.1`--`### A.4` 审计附录冲突，一律以文末正式审计附录为准。

#### 历史 A.2 维度树证据账本草案（禁止消费）

| 证据标识 | 引用键 | 来源文件 | 原文章节 | 表/图编号 | 释义 | 证据角色 | 证据强度 | 支撑维度节点 | 需 PDF 视觉核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|
| EV-pet15-001 | ev-rq | paper_content.txt | §3.1 (line 217–229) | -- | 明确 RQ1–RQ4 全文表述 | rq | verified | FOREST-ROOT, T1.流程 | 否 | 仅本文 |
| EV-pet15-002 | ev-抽取-form | paper_content.txt | §3.4, Table 3 | Table 3 | 12 字段 抽取 form + RQ owner 绑定 | 模式 | verified | T1 整棵树, L01–L05, L12 | 否 (文本完整) | -- |
| EV-pet15-003 | ev-分类-facets | paper_content.txt | §4.4.4, Fig.12–13 | Fig.12, B.24, B.25 | 5 个 topic-indep facet + 2 个 topic-spec 子项 | 模式 + 计数 | verified | T2 整棵树, L09 | 否 | -- |
| EV-pet15-004 | ev-research-type-truth-table | paper_content.txt | §5.1.3, Table 7 | Table 7 | research type 6 类 + R1..R6 真值表 | 模式 + decision-table | verified | T2.research_type, L10, R10 | 否 | 6 类闭包仅适于此 facet |
| EV-pet15-005 | ev-流程-actions | paper_content.txt | §5, Table 5, Table 8 | Table 5, Table 8 | 9 指南 × 30+ activities 比较矩阵；26 actions rubric | 模式 + 关系 | verified | T3 整棵树, R08 | 推荐 PDF 核对 ✓/✗ 符号 | -- |
| EV-pet15-006 | ev-rubric-有序 | paper_content.txt | §5.4, Tables 9–13, Table 14 | Tables 9–13, 14 | 4+1 有序 rubric + 52 篇分布 | rubric + statistic | local_历史草稿旧强度（当前禁止采信） | T3 评分层, L14 | 是（Table 14 数值需复核）| 有序 scale 仅适合 SMS |
| EV-pet15-007 | ev-appendix-B-relations | paper_content.txt | Appendix B | B.15–B.27 | 逐研究 研究→category 关系边，分母=52 | 关系 + 计数 | local_历史草稿旧强度（当前禁止采信） | R01–R05, R07, L01–L13 | 是（频次需复核）| 现代 SE SMS 已不同 |
| EV-pet15-008 | ev-效度-分类法 | paper_content.txt | §3.6, §5.1.5 | -- | 5 类 效度 + repeatability + mitigations | 分类法 | verified | T4 整棵树, L13 | 否 | 未含现代 LLM 风险 |
| EV-pet15-009 | ev-fig1-flow | paper_content.txt | §3.3, Fig.1 | Fig.1 | 选择流程链 7752→...→52 | statistic | not_verified | FOREST-ROOT 分母 | **是**（文本提取乱序）| -- |

#### 历史 A.3 结论-证据映射草案（禁止消费）

| ID | 结论 | 类型 | 支撑对象 | 支撑证据 | 反证/限制 | 强度 | 允许用途 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是 **维度森林**（4 棵独立树），不是单一维度树。 | 树类型（tree_type） | FOREST-ROOT | EV-001, EV-002, EV-003, EV-005, EV-008 | 4 棵树是审计判断；作者未显式声明"森林"。 | 历史草稿旧强度（当前禁止采信） | A1-DT v2 主结构定锚 |
| C02 | 样本单位 = SE 系统映射研究；分母=52；统计池资格 = 方法学池 yes。 | 样本单位（sample_unit） | T1, R01–R05 | EV-007, EV-009 | -- | 历史草稿旧强度（当前禁止采信） | SUMMARY 总表更新 |
| C03 | Table 3 抽取 form 的 12 字段历史草稿曾提出迁移建议；当前禁止直接采信作 Paper2 LLM-智能体 抽取 模式 模板。 | migration_seed | T1, L01–L05, L12 | EV-002 | 字段须重命名以适应现代 SE/LLM 主题；SWEBOK 需替换。 | 历史草稿旧强度（当前禁止采信） | Paper2 §方法 设计 |
| C04 | Table 7 research-type 真值表是 A1-DT v2 罕见的"完整布尔真值表 模式 证据"，可作为 Paper2 LLM-judge 后验规则 layer。 | migration_seed | L10, R10 | EV-004 | 仅适于 research_type 单 facet；其他 facet 需自行设计真值表。 | 历史草稿旧强度（当前禁止采信） | Paper2 §方法 设计 |
| C05 | 4+1 有序 rubric (Tables 9–13) 提供了 质量 评分的"0/1/2/3 分级描述"模板。 | migration_seed | L14, T3 评分层 | EV-006 | rubric 仅适合 SMS；SLR / experimental 研究 不可直接套。 | medium | Paper2 §评价 设计 |
| C06 | 指南×activity 比较矩阵 (Table 5) 提供"用多 指南 反向揭示 模式 覆盖 缺口（gap）"的方法学样板。 | migration_seed | R08 | EV-005 | matrix 对手工对齐成本高；需 LLM 辅助。 | medium | Paper2 §discussion / future work |
| C07 | 不可迁移：SWEBOK 11 类、效度 5 类、指南 10 类的具体内容均带有 2012 前 SE 时代痕迹，仅迁移"封闭枚举 + 频次统计"的方法学 form，不迁移 enum 内容。 | migration_boundary | L01, L02, L13 | EV-002, EV-003, EV-008 | -- | 历史草稿旧强度（当前禁止采信） | review.md §"可迁移边界" |
| C08 | 单人筛选（second author 独立 inclusion）是本文自报最大 效度 威胁；提示 Paper2 须设计双人/人+智能体 多重审查协议。 | candidate_heuristic | T4.theoretical_validity | EV-008 + §3.6.2 | -- | 历史草稿旧强度（当前禁止采信） | Paper2 §威胁 |
| C09 | rubric ratio 中位数 33% 是 2012 前 SE SMS 实证基线，**不得**外推为"现代 LLM-SLR 应达到 ≥33%"的规范性目标。 | migration_boundary | L14 | EV-006 | -- | 历史草稿旧强度（当前禁止采信） | review.md §"不可迁移边界" |
| C10 | （废弃旧结论）"原生树类型 = 降级树 / 模式种子 only"——本结论由 A1-DT v1 给出，与本审计冲突，应废弃。 | audit_repair | -- | EV-002, EV-003, EV-004, EV-005, EV-007 | -- | 历史草稿旧强度（当前禁止采信） | review.md §"审计返修口径"中标注 deprecated |

### 9. 技能使用与自我审查记录

#### 9.1 技能文件读取与采用原则

| 技能文件 | 实际读取范围 | 采用原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | line 1–100（核心 mandate / operating modes / loading strategy / non-negotiable gates） | "Evidence gate"（仓库 files 优于 memory）；"Claim gate"（每条声明须有证据，否则降级）；"Citation asset gate"（仅引用本地可核验的章节 / 表 / 图编号）。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 全文（112 lines） | 用 Universal Review Dimensions 5 维（Originality, Quality, Clarity, Significance, Reproducibility）评估旧版 review.md 的可信度；用 "constructive specificity" 标准产出 C/I/M 建议时给出 file:line 锚点。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 全文（223 lines） | 用 "Claim Audit" 模板检查 review.md 中"维度树主类型"等结论的证据强度；用 "Adversarial Questions" 检查是否把投影误读为原文（特别是 "Could a reviewer say... has been done before?"）。 |
| `research-planning/SKILL.md` | 全文（77 lines） | 按 "Flag ambiguities explicitly rather than making assumptions" 原则——本审计明确把 Fig.1 数字链等 PDF 视觉项标为 `not_verified`，不脑补分母。 |
| `research-planning/references/planning-prompts.md` | line 1–80 | Paper2Code 4-turn 思路用于组织 §3 维度森林的层级展开（先 overall, 再 architecture, 再 logic, 再 leaf-level）。 |
| `research-planning/references/output-schemas.md` | line 1–80 | 采用 JSON-模式-like 思路把每个 叶子 显式标注 `取值空间类型`。 |
| `oh-my-codex/autoresearch/SKILL.md` | 全文（70 lines） | 借用 "completion 制品 contract" 思路——本审计的最终交付物 = self-contained Markdown 报告，符合 制品-gated 完成标准。 |

#### 9.2 reviewer 视角下本审计最高风险 3 点

1. **Fig.1 数字链 (7752→5082→60→43→54→44→52+8+11) 未做 PDF 视觉核验**。文本提取顺序混乱，分母 52 来自 §3.6.2 与 §4.4.3 多处文本复现 (`14 out of 52`)，结论稳健；但 +8 与 +11 的回补来源需 PDF 复查才能 100% 锁定。主线程合并时应保留 `EV-pet15-009 = not_verified` 并列入 A2a。
2. **Tables 9–13 中 "bold 高亮分数" 在 paper_content.txt 中丢失**。Table 14 给出本文自身 rubric 的频次分布，但"本研究自评 33% ratio"的具体细分须 PDF 复核 Tables 9–13 中 bold 标注的位置（§5.4 line 1372: "scores identified in this 系统映射研究 are highlighted as bold text"）。主线程引用 L14 时应保留 `local_历史草稿旧强度（当前禁止采信）` 而非 `verified`。
3. **"维度森林 vs 单树" 是审计判断而非作者声明**。作者未在原文说"this is a 森林"；本审计基于 Table 3 (抽取 form) 与 Table 8 (rubric) 服务对象不同（编码自身 52 篇 vs 向后续研究推荐）的语义观察。若 reviewer 反对，可降级为"多 模式 共存的单论文"，但其取值空间区分必须保留。

#### 9.3 blocked / timeout / 文件缺失

- 无 blocked / timeout。
- 所有 7 个技能 / 指南文件可读，所有 5 个论文材料（bibtex.bib / metadata.json / paper.pdf 文件存在 / paper_content.txt / review.md）可读。
- 未打开 `paper.pdf` 二进制（按硬约束 6: 若需图表视觉核验仅说明状态，不强制读 PDF）；本轮以 paper_content.txt 全文 + Tables B.15–B.27 文本为主，已覆盖 ≥85% 的 模式 证据。

---

**审计完成时间**: 2026-06-30
**智能体**: claude (claude-opus-4-7[1m])
**输出文件**: 本回答正文，未修改仓库任何文件，未 commit / push / gh comment。

> [!NOTE]
> v2 返修后记：以上“对旧版 `review.md` 的返修来源”和审计草案是 A1-DT v2 返修前的独立审计输入；当前文件已经在[维度树复原](#维度树复原)与文末 A.1--A.4 中完成主线程裁决和返修。本审计报告保留为历史归档，不再作为当前状态判定依据。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md](../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-petersen-2015-mapping-guidelines-update-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-petersen-2015-mapping-guidelines-update-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-petersen-2015-mapping-guidelines-update-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-petersen-2015-mapping-guidelines-update-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2015-mapping-guidelines-update-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2015-mapping-guidelines-update-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/petersen-2015-mapping-guidelines-update__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-petersen-2015-mapping-guidelines-update-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/petersen-2015-mapping-guidelines-update.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见上文“维度树复原”的叶子维度表、关系边表和审计草案。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-petersen-2015-mapping-guidelines-update-type | clm-petersen-2015-mapping-guidelines-update-type | src-petersen-2015-mapping-guidelines-update-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：**SLR / SMS / guideline 混合**：systematic 系统映射研究 of 系统映射 studies (tertiary 性质) + guideline update。 | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-petersen-2015-mapping-guidelines-update-unit | clm-petersen-2015-mapping-guidelines-update-unit | src-petersen-2015-mapping-guidelines-update-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**原始研究 = SE 领域已发表的 systematic 系统映射研究**（每个 study 被作者按 Table 3 抽取表编码）。 | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-petersen-2015-mapping-guidelines-update-denom | clm-petersen-2015-mapping-guidelines-update-denom | src-petersen-2015-mapping-guidelines-update-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：**52 mapping studies**（Appendix A 列出 ~52 个 included id；§3.6.2 与 §4.4.3 多处复现 "52" 分母）。Fig. 1 流程链：7752 → 5082 (去 2004 前) → 60 (title/abstract) → 43 (full-text) → 54 (+11 snowball) → 44 (quality) → 52 (review of excluded 回补 8) 。 | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-petersen-2015-mapping-guidelines-update-tree | clm-petersen-2015-mapping-guidelines-update-tree | src-petersen-2015-mapping-guidelines-update-text; src-petersen-2015-mapping-guidelines-update-codex; src-petersen-2015-mapping-guidelines-update-claude; src-petersen-2015-mapping-guidelines-update-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②分类切面（classification facet） 树；③guideline action / rubric 树；④validity taxonomy 树）。 | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-petersen-2015-mapping-guidelines-update-pool | clm-petersen-2015-mapping-guidelines-update-pool | src-petersen-2015-mapping-guidelines-update-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-petersen-2015-mapping-guidelines-update-type | A1DT-petersen-2015-mapping-guidelines-update-C01 | 本文原文类型为：**SLR / SMS / guideline 混合**：systematic 系统映射研究 of 系统映射 studies (tertiary 性质) + guideline update。 | paper_type | type | ev-petersen-2015-mapping-guidelines-update-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-petersen-2015-mapping-guidelines-update-unit | A1DT-petersen-2015-mapping-guidelines-update-C02 | 本文被编码样本单位为：**原始研究 = SE 领域已发表的 systematic 系统映射研究**（每个 study 被作者按 Table 3 抽取表编码）。 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-petersen-2015-mapping-guidelines-update-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-petersen-2015-mapping-guidelines-update-tree | A1DT-petersen-2015-mapping-guidelines-update-C03 | 本文原生维度树 / 维度森林为：**维度森林**（至少 4 棵互相独立的主干树：①extraction form 树；②分类切面（classification facet） 树；③guideline action / rubric 树；④validity taxonomy 树）。 | 树类型（tree_type） | native_tree | ev-petersen-2015-mapping-guidelines-update-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-petersen-2015-mapping-guidelines-update-pool | A1DT-petersen-2015-mapping-guidelines-update-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-petersen-2015-mapping-guidelines-update-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-petersen-2015-mapping-guidelines-update-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-petersen-2015-mapping-guidelines-update-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-petersen-2015-mapping-guidelines-update-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
