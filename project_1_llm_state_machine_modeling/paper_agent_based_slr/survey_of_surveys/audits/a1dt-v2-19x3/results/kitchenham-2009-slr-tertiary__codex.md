### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-2009-slr-tertiary` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；按全文 962 行阅读，重点核对 §1--§5、Table 1--5、Appendix Table A1--A3 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；核对 DOI、题名、年份、期刊、review type、当前本地状态 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 确认 9 页 PDF，并用 `pdftotext -layout` 核对 Table 2、Table 3、Table A1--A3 的版面列结构；未做截图级视觉核验 |
| 原文类型 | tertiary；文中明确称本研究为 tertiary literature review，方法上是系统文献综述（SLR） |
| 被编码样本单位 | 纳入的二级研究，即软件工程领域 SLR / meta-analysis 研究条目；Table 2 中为 S1--S20 |
| 样本数量 / 分母 | 检索分母：Table A1 统计 2506 篇源内文章、33 篇 relevant、19 篇 selected；去重后 18 个唯一研究，再加 2 个源外 peer-reviewed 研究，最终 20 个相关研究 |
| 原生树类型 | 维度森林：语料检索与筛选树 + 纳入研究数据抽取树 + DARE 质量评价树 + 作者/机构关系树 + 结果统计/局限树 |
| 主统计池资格 | 局部可统计；原文有系统检索、纳排、抽取字段、质量评分与统计表，适合作为 tertiary-study schema seed 和后续 A2a 主统计池候选；但 2004--2007 EBSE 领域结论不可直接迁移为 Paper2 final finding |
| 总体判定 | needs repair；原文证据充足，但现有 `review.md` 仍需把原生字段树置于主位，并拆分过粗证据账本 |

### 1. 原文证据阅读说明

实际读取文件：

- `bibtex.bib`：核对 Kitchenham et al. 2009、IST、DOI `10.1016/j.infsof.2008.09.009`。
- `metadata.json`：核对本地类型为 `tertiary-like SLR`，`eligible_for_schema_seed=true`，`eligible_for_statistical_synthesis=true`。
- `paper_content.txt`：阅读全文，重点读 §2 Method、§3 Results、§4 Discussion、§5 Conclusions、Table 1--5、Table A1--A3。
- `review.md`：阅读全文，确认其已有六叶通用接口、v1 历史审计警告、原文 schema seed 表、A.1--A.4。
- `paper.pdf`：用本地 PDF 工具核对页数和表格版面；Table 2/3/A1/A2/A3 的列结构比 `paper_content.txt` 清晰。仍建议 A2a 做人工 PDF 视觉核验以补精确页码和表号。

关键原文证据锚点：

1. 摘要：研究目标是评估 SLR 作为 EBSE 聚合证据方法的影响；方法为手工搜索指定期刊和会议。
2. §1 Introduction：作者说明本研究用 tertiary study 评估 2004 年以来 EBSE/SLR 状态，关注描述 SLR 的文章。
3. §2 Method：作者明确本研究按 SLR 指南执行，因对象是 secondary studies，所以归类为 tertiary review。
4. §2.1 Research questions：RQ1--RQ4 分别问 SLR 活动量、研究主题、主导研究者/机构、当前研究限制。
5. §2.2 Search process 与 Table 1：手工搜索指定期刊和会议，由一名研究者初筛，另一名研究者检查纳入/排除。
6. §2.3 Inclusion/exclusion：纳入 peer-reviewed SLR 和 meta-analysis；排除 informal survey、纯 EBSE/SLR procedure paper、重复报告。
7. §2.4 Quality assessment：使用 DARE 的 QA1--QA4，并将 Y/P/N/Unknown 映射为 1/0.5/0/Unknown。
8. §2.5 Data collection：逐项列出从每个研究抽取的字段，是本文原生维度树最核心证据。
9. §2.6 Data analysis：说明哪些字段被 tabulate，并逐项映射到 RQ1--RQ4。
10. §3.1 与 Table 2：最终 20 个研究条目，字段包含 ID、作者、年份、topic type、topic area、article type、refs、practice guideline、primary studies 数量。
11. Table 3--5：质量评价字段和统计结果，包括 QA1--QA4、total score、initial rater agreement、按年份/是否引用 guideline 的质量均值。
12. §4.5 Limitations：手工搜索、单人选择/抽取加检查、可能漏检和数据错误，是迁移边界的核心证据。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文主样本单位是“纳入的二级研究”，即软件工程领域的 SLR 或 meta-analysis。Table 2 的 S1--S20 是实际编码对象。Primary studies 不是本文主样本单位，而是每个纳入 SLR 的一个数值字段。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

有。作者定义了 RQ，手工搜索指定来源，给出纳排标准，记录候选与排除条目，抽取字段，使用 DARE 质量评价，并将抽取字段表格化以回答 RQ。流程不是 roadmap/vision，而是完成型 tertiary review。

3. 原文字段来自哪里？

主要来自四类原文结构：

- 数据抽取字段：§2.5 的 extraction list 与 Table 2 / A3。
- 质量 rubric：§2.4 的 DARE QA1--QA4 与 Table 3--5。
- 检索/筛选账本：§2.2--§2.3、Table 1、Table A1、Table A2。
- 结果组织与限制：§2.6、§3、§4、§5。

没有发现独立 replication package；文中指向技术报告 [24] 的 Appendix 作为更详细补充，但本任务只基于本地入库论文材料审计。

4. RQ 与样本单位是什么关系？

RQ 不是维度树根，也不是样本单位。RQ 是字段选择和统计组织的用途层：RQ1 选择 year/source/reference-to-EBSE/guideline；RQ2 选择 scope/topic；RQ3 选择 author/institution/country；RQ4 选择 topic limitation、primary-study count、quality score、practice guideline。维度树根仍是“纳入的 SLR/MA study”。

5. 若无系统样本库，如何降级？

本文不需要降级为无系统样本库。仅需局部降级：领域结论只能作为 2004--2007 早期 EBSE/SE SLR 状态观察，不可迁移为当前 LLM/agent survey 的最终领域发现。

### 3. 原生样本编码维度树 / 维度森林

```text
Root: Kitchenham 2009 tertiary review corpus
对象: 纳入的二级研究条目 S1--S20（SLR 或 MA）

├── F0. 检索来源与筛选账本
│   ├── source venue（Table 1/A1；完整枚举，期刊/会议来源）
│   ├── source acronym（完整枚举）
│   ├── publication year window（数值/区间：2004--2007-06-30）
│   ├── total articles per source-year（数值）
│   ├── relevant articles per source-year（数值）
│   ├── selected articles per source-year（数值）
│   ├── inclusion class: SLR / MA（完整枚举）
│   ├── exclusion reason（完整枚举/自由文本：informal survey、not SE topic、no described survey 等）
│   └── duplicate handling（关系值：conference version / journal version / most complete report）

├── F1. 纳入研究描述与抽取字段
│   ├── study ID S1--S20（标识符）
│   ├── author(s) / full reference（自由文本/引用）
│   ├── date（年份或年份组合）
│   ├── article type: SLR / MA（完整枚举）
│   ├── scope / topic type: research trends / technology evaluation（完整枚举）
│   ├── main topic area（自由文本受控化：cost estimation、testing、SE experiments 等）
│   ├── referenced EBSE papers or SLR guideline（布尔/枚举：Guideline TR、EBSE paper、No）
│   ├── proposed practitioner-based guidelines（布尔/边界脚注）
│   ├── number of primary studies（数值）
│   ├── summary including RQ and answers（自由文本）
│   └── research question / issue（自由文本）

├── F2. DARE 质量评价树
│   ├── QA1 inclusion/exclusion criteria described and appropriate（Y/P/N/Unknown）
│   ├── QA2 search coverage likely adequate（Y/P/N/Unknown）
│   ├── QA3 included-study quality/validity assessed（Y/P/N/Unknown）
│   ├── QA4 basic data/studies adequately described（Y/P/N/Unknown）
│   ├── score mapping（Y=1, P=0.5, N=0, Unknown=待补）
│   ├── total quality score（数值 0--4）
│   ├── initial rater agreement（数值 0--4）
│   └── author-contact reassignment marker（布尔/标记：asterisk）

├── F3. 作者、机构与国家关系树
│   ├── study ID -> author（关系值）
│   ├── author -> institution（关系值）
│   ├── institution -> country（关系值）
│   └── derived leadership counts（数值：欧洲、Simula、个人贡献次数等）

├── F4. RQ 映射与统计输出树
│   ├── RQ1 activity: studies per year/source/reference relation（数值/枚举）
│   ├── RQ2 topics: scope + topic area + concrete question-answer examples（枚举/自由文本）
│   ├── RQ3 leadership: author/institution/country aggregation（关系+数值）
│   ├── RQ4.1 topic limitation（统计观察+解释）
│   ├── RQ4.2 primary-study availability（数值范围）
│   ├── RQ4.3 quality appropriateness/improvement（质量分数+统计检验）
│   └── RQ4.4 practitioner guideline contribution（布尔计数）

└── F5. 协议偏离、局限与迁移边界
    ├── manual search rather than automated search（布尔/过程说明）
    ├── single researcher selected + checker（过程说明）
    ├── single extractor + checker（过程说明）
    ├── restricted venue scope（范围限制）
    ├── possible inclusion bias toward weakly systematic studies（风险说明）
    └── data extraction / DARE subjectivity risk（风险说明）
```

缺失部分与 A2a 精核任务：本文没有单独附录全文之外的 detailed summary 表；文中指向技术报告 [24] Appendix 3。A2a 若要冻结完整叶子，应补技术报告或人工 PDF 页码核验；否则 summary/RQ-answer 字段只能保留为自由文本加理由，不进入封闭枚举统计。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L0-source | 来源 venue | F0 | Table 1, Table A1 | 被手工搜索的期刊/会议来源 | IST、JSS、TSE、IEEE SW 等 | 完整枚举，需 A2a 核 venue 数 | 未列入即非本轮搜索范围 | 检索分母、来源覆盖 | 搜索范围局限 | §2.2, Table 1/A1 | 只迁移“来源账本”结构 |
| L0-year-window | 时间窗 | F0 | §2.3, Table A1 | 纳入出版时间范围 | 2004-01-01 至 2007-06-30 | 区间 | 窗外不纳入 | 分母边界 | 早期 EBSE 边界 | §2.3 | 不代表现代 SLR 状态 |
| L0-total-relevant-selected | 总量/相关/选中计数 | F0 | Table A1 | 每来源每年 total/relevant/selected 数 | 非负整数 | 数值 | n/a 表示无会议年度 | 搜索漏斗统计 | 检索充分性讨论 | Table A1 | 只可用于本文检索过程 |
| L0-exclusion-reason | 排除原因 | F0 | Table A2 | 候选文章未纳入原因 | informal survey、not SE topic、survey not described 等 | 枚举+自由文本 | 未进入 A2 即非候选排除表对象 | 纳排审计 | 定义“系统综述”边界 | §2.3, Table A2 | 不可泛化为所有排除原因 |
| L1-study-id | 研究 ID | F1 | Table 2 | 纳入研究编号 S1--S20 | S1--S20 | 完整枚举 | 无 ID 不在主样本表 | 主键 | 样本单位确认 | Table 2 | 必须区分文章与唯一研究 |
| L1-date | 发表年份 | F1 | Table 2 | 纳入研究出版年份 | 2004--2007，含重复报告年份组合 | 数值/区间 | 未报告则 not_reported | 年度趋势 | SLR 活动稳定性 | Table 2/4 | 早期时间窗限定 |
| L1-article-type | 文章类型 | F1 | §2.5, Table 2 | 纳入研究类型 | SLR、MA | 完整枚举 | 非 SLR/MA 不纳入 | 类型分布 | tertiary 语料边界 | §2.3, Table 2 | 只对应本文纳排定义 |
| L1-topic-type | 主题类型/范围 | F1 | §2.5, Table 2 | 研究趋势 vs 技术评价 | Research trends、Technology evaluation | 完整枚举 | 未判定则待核验 | RQ2/RQ4.1 分组 | 主题是否偏研究实践 | §2.1, §2.5, Table 2 | 不等同通用 SLR taxonomy |
| L1-topic-area | 主主题领域 | F1 | §2.5, Table 2 | 每个 SLR/MA 的软件工程主题 | cost estimation、unit testing、SE experiments 等 | 自由文本受控化 | 未报告则 not_reported | 主题频次 | 主题覆盖有限 | Table 2, §4.2 | 只保留本文原词或明确归并 |
| L1-ref-ebse-guideline | EBSE/guideline 引用状态 | F1 | §2.5, Table 2 | 是否引用 EBSE paper 或 SLR guideline | Guideline TR、EBSE paper、No | 枚举 | 未报告则 No/待核验需区分 | RQ1、质量因素 | EBSE 自定位程度 | §2.6, Table 2/5 | 不等于方法质量充分 |
| L1-practitioner-guideline | 是否提出实践指南 | F1 | §2.5, Table 2 | 是否给 practitioner-based guidelines | Yes、No、脚注边界 | 布尔+边界脚注 | 暗示建议但未明确定义应为 No/边界 | RQ4.4 | EBSE 对实践贡献不足 | Table 2, §4.4 | 不能外推到现代指南研究 |
| L1-num-primary | primary studies 数量 | F1 | §2.5, Table 2 | 每个纳入 SLR 使用的一手研究数量 | 非负整数 | 数值 | 未报告则 Unknown | RQ4.2 | 主题是否有足够一手证据 | Table 2, §4.4 | primary studies 不是本文样本单位 |
| L1-summary-rq-answer | 摘要/RQ/答案 | F1 | §2.5, [24] Appendix 3 指向 | 对纳入研究的问题与答案摘要 | 自由文本 | 自由文本加理由 | 本地论文未展开则 not_verified | 质性解释 | 候选 finding 背景 | §2.5, §3.1 | 未读技术报告前不可封闭编码 |
| L2-QA1 | QA1 纳排标准质量 | F2 | §2.4, Table 3 | 纳排标准是否描述且适当 | Y/P/N/Unknown | 完整枚举 | Unknown 可询问作者后重评 | 质量分数 | 报告质量缺口 | §2.4, Table 3 | DARE 特定口径 |
| L2-QA2 | QA2 检索覆盖质量 | F2 | §2.4, Table 3 | 检索是否可能覆盖相关研究 | Y/P/N/Unknown | 完整枚举 | Unknown 可询问作者后重评 | 质量分数 | 检索充分性 | §2.4, Table 3 | DARE 特定口径 |
| L2-QA3 | QA3 一手研究质量评价 | F2 | §2.4, Table 3 | 是否评价纳入 primary studies 质量/有效性 | Y/P/N/Unknown | 完整枚举 | Unknown 可询问作者后重评 | 质量分数 | 技术评价 SLR 风险 | §2.4, Table 3, §4.4 | 不适用于无 primary-study 的样本 |
| L2-QA4 | QA4 基础数据描述 | F2 | §2.4, Table 3 | 是否充分描述基本数据/研究 | Y/P/N/Unknown | 完整枚举 | Unknown 可询问作者后重评 | 质量分数 | 复现/可审计性 | §2.4, Table 3 | DARE 特定口径 |
| L2-total-score | 总质量分 | F2 | §2.4, Table 3 | QA1--QA4 按 Y/P/N 映射求和 | 0--4，0.5 步长 | 数值 | Unknown 未补则总分不稳 | 质量统计、趋势 | 质量是否改善 | Table 3--5 | 正式统计需保留评分规则 |
| L2-rater-agreement | 初始评分一致数 | F2 | Table 3 | 初始评价者一致的问题数 | 0--4 | 数值 | 未报告则 not_reported | 质量评价可靠性 | DARE 主观性边界 | Table 3, §3.2 | 不是 inter-rater coefficient |
| L3-author-inst-country | 作者-机构-国家 | F3 | §2.5, Table A3 | 每个研究作者及机构国家 | author、institution、country 关系 | 关系值 | 未报告则 not_reported | RQ3 聚合 | 研究主导者/地域 | Table A3, §4.3 | 不可迁移为当前地域格局 |
| L5-protocol-deviation | 协议偏离/局限 | F5 | §2.7, §4.5 | 与原 SLR 指南不同的过程选择 | manual search、single selector、single extractor 等 | 自由文本枚举 | 不适用则无偏离 | validity boundary | 搜索/抽取误差风险 | §2.7, §4.5 | 只迁移局限写法 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E-RQ-field-1 | RQ1 | drives-fields | year、source、EBSE/guideline reference | 数值/枚举 | 无字段则 RQ1 不可统计 | §2.1, §2.6 | 说明 RQ 是字段用途，不是样本单位 |
| E-RQ-field-2 | RQ2 | drives-fields | topic type、topic area、scope | 枚举/自由文本 | 无 topic 则待核验 | §2.1, §2.5--2.6 | 主题分布统计 |
| E-RQ-field-3 | RQ3 | drives-fields | author、institution、country | 关系值 | 未报告则 not_reported | §2.1, Table A3 | 主导研究者/机构分析 |
| E-RQ-field-4 | RQ4 | drives-fields | topic limitation、primary-study count、QA score、practice guideline | 数值/布尔/自由文本 | 字段缺失则 RQ4 分支降级 | §2.1, §2.6, §4.4 | 限制与实践贡献分析 |
| E-search-select | searched article | filtered-by | included study / excluded candidate | included、excluded、duplicate | 不在 Table A1/A2/Table2 则不可追踪 | §2.2--§3.1, Table A1/A2 | 检索漏斗审计 |
| E-duplicate | duplicate report | duplicate-of | most complete included study | 引用关系 | 未说明则待核验 | §2.3, §3.1 | 防止重复计数 |
| E-study-quality | included study | scored-by | QA1--QA4 | Y/P/N/Unknown | Unknown 可作者询问后重评 | §2.4, Table 3 | DARE 质量树 |
| E-QA-total | QA1--QA4 | summed-into | total quality score | 0--4 | Unknown 未补则总分不稳 | §2.4, Table 3 | 质量统计 |
| E-study-author | included study | authored-by | author | 自由文本实体 | 未列则 not_reported | Table A3 | RQ3 关系图 |
| E-author-institution | author | affiliated-with | institution/country | 关系值 | 未列则 not_reported | Table A3 | 机构与国家聚合 |
| E-study-primary-count | included study | contains-count-of | primary studies | 非负整数 | 未报告则 Unknown | §2.5, Table 2 | RQ4.2 证据充分性 |
| E-study-guideline | included study | proposes | practitioner-based guideline | Yes/No/脚注边界 | 暗示但不明确定义则边界 No | Table 2, §4.4 | 实践贡献判断 |

本文存在显式关系型 schema，尤其是 study-author-institution-country、study-QA-score、RQ-field-table 关系；因此“不适用”不成立。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段/统计表支持的统计观察：

- 最终纳入 20 个相关研究；其中 19 个 SLR、1 个 meta-analysis。
- 12 个研究面向 technology evaluation，8 个面向 research trends。
- 7 个研究涉及 cost estimation；提出实践指南的研究集中在 cost estimation。
- 8 个研究引用 SLR guideline，2 个引用 EBSE paper；约一半研究直接自定位到 EBSE。
- Table 3 显示所有研究 DARE 总分至少 1，只有 3 个低于 2。
- Table 4 显示 2004--2007 年数量相对稳定，平均质量分上升；文中报告 Spearman 相关为 0.51，p < 0.023。
- Table 5 显示引用 guideline 与否的质量均值差异不显著；文中报告 F=0.37，p=0.55。
- RQ3 统计显示欧洲研究者参与 14 个研究，Simula 参与 8 个研究。
- research trends study 的 primary-study 数量范围大于 technology evaluation study；原文给出 63--1485 vs 6--54。

原文 discussion / recommendation / roadmap 提出的候选 finding：

- 早期 SE SLR 主题覆盖有限，主流软件工程生命周期主题代表不足。
- 较多 SLR 服务研究实践而不是工程实践，EBSE 对 practitioner 的贡献仍需增强。
- 高质量 mapping study 可作为后续研究共同起点。
- 建立分类化 primary-study 数据库可能支撑连续的二级研究。
- 作者建议后续采用更宽的自动化检索，并在 2009 年后重复追踪 EBSE/SLR 进展。

对 Paper2 可迁移的方法学启发：

- 先判定样本单位，再建字段树；primary studies count 可以是字段，而不是本综述样本单位。
- 把 RQ 显式映射到抽取字段和结果表，避免 RQ 伪装成维度树。
- 保留 search denominator、relevant、selected、unique、external-added 的漏斗链。
- 对质量评价单独建 rubric 树，并保存评分规则、Unknown 处理、评分者一致性边界。
- 把 excluded candidate 和 rejection reason 当成范围控制证据，而不是丢掉。
- 将 statistical observation、discussion recommendation、final finding 分层。

绝不能迁移的领域结论：

- “Simula/欧洲主导 SLR”只适用于 2004--2007 早期 EBSE 样本。
- “cost estimation 是主要主题”不能外推到 LLM/agent/SE 综述。
- “SLR 质量正在提高”不能作为当前领域趋势，除非后续跨年样本复核。
- 具体 cost estimation 结论，如模型 vs expert judgment，不属于 Paper2 目标领域事实。

### 7. 对现有 `review.md` 的返修建议

C 级：

- 必须把“原文 schema 主树/维度森林”提升为 `维度树复原` 的主事实源；当前六个通用 leaf 即使有校准说明，仍占据主树位置，容易继续被误读为原文叶子全集。
- 必须修正根对象/样本单位表述：根对象应为 included secondary study（SLR/MA），不是 “primary study / secondary study” 混写；primary studies 是 Table 2 中的数值字段。
- 必须把 20 个 included studies 的分母链写清：2506 total articles、33 relevant、19 selected articles、18 unique studies、+2 external peer-reviewed studies、20 final studies。否则 “20 relevant studies” 的分母来源不透明。

I 级：

- A.2 证据账本需要拆分。当前 EV-002/EV-003 过粗，建议至少拆为 RQ、search process、inclusion/exclusion、DARE QA rubric、data collection、data analysis、Table 2、Table 3--5、Table A1、Table A2、Table A3、limitations。
- 叶子维度表应替换为原文字段：article type、topic type、topic area、Refs、practice guideline、number primary studies、QA1--QA4、total score、initial rater agreement、author-institution-country 等。
- 关系边表应新增 RQ→字段→表→观察、study→QA→score、study→author→institution→country、candidate→rejection reason、duplicate report→included study。
- `A.4` 中如果保留 “structure-check passed”，应补实际命令、日期或运行证据；否则在 v2 语境中改为 `not_rerun_in_v2` 更稳。

M 级：

- SUMMARY 当前 “样本单位 / 样本数量 / 原生树类型”基本方向正确，但建议把“主统计池资格”统一写为“局部可统计 / A2a 后可升级”，避免 `是` 被误读为已可进入最终定量统计。
- `review.md` 快速结论卡片里的“是否目标证据池：否”与 `metadata.json` 的 eligibility、SUMMARY 的候选资格不完全一致；建议改为“主统计池候选：局部可统计；当前用途 schema_seed”。
- PDF 版面核验状态可从 `needs_manual_check` 改成“已做 `pdftotext -layout` 核验；仍需人工视觉页码核验”。

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-K09-001 | `paper_content.txt`, `paper.pdf` | §1, §2 | Introduction 与 Method 开头 | 本研究用 tertiary review 评估 EBSE/SLR 状态 | 样本单位/原文类型 | strong | root、原文类型、sample unit | 否 | 只说明本文类型 |
| EV-K09-002 | `paper_content.txt` | §2.1 | RQ1--RQ4 | RQ 覆盖活动量、主题、主导者、限制 | RQ 到字段用途 | strong | F4、E-RQ-field-* | 否 | RQ 不是树根 |
| EV-K09-003 | `paper_content.txt`, `paper.pdf` | §2.2, Table 1 | selected journals/conferences | 手工搜索指定期刊会议，由一人初筛、一人检查 | 检索来源 | medium | F0, L0-source | 是；venue 数有抽取/摘要口径差异 | 不代表自动检索 |
| EV-K09-004 | `paper_content.txt` | §2.3 | inclusion/exclusion criteria | 纳入 peer-reviewed SLR/MA，排除 informal survey、procedure paper、duplicate | 纳排规则 | strong | F0, L0-exclusion-reason | 否 | 只适用本文定义 |
| EV-K09-005 | `paper_content.txt` | §2.4 | DARE QA1--QA4 | 使用 DARE 四个 QA 问题与 Y/P/N/Unknown 评分 | 质量 rubric | strong | F2, L2-QA1--QA4 | 否 | DARE 口径不等同所有质量评价 |
| EV-K09-006 | `paper_content.txt` | §2.5 | data extracted list | 抽取 source/ref、type/scope、topic、authors、summary、quality、guideline、primary studies count 等 | 数据抽取字段 | strong | F1, L1-* | 否 | summary 字段需技术报告补全 |
| EV-K09-007 | `paper_content.txt` | §2.6 | data tabulated list | 字段按 RQ1--RQ4 形成表格统计 | RQ→字段→统计 | strong | F4, relation edges | 否 | 不支撑跨领域结论 |
| EV-K09-008 | `paper_content.txt`, `paper.pdf` | §3.1, Table 2 | S1--S20 systematic review studies | 20 个研究条目及其 type/topic/guideline/primary count | 主样本表 | strong | Root, F1 | 已做 layout；建议人工页码核验 | 2004--2007 样本 |
| EV-K09-009 | `paper_content.txt`, `paper.pdf` | §3.2, Table 3 | Quality evaluation of SLRs | 每个研究 QA1--QA4、total score、initial agreement | 质量结果表 | strong | F2 | 已做 layout；建议人工页码核验 | 评分有主观性 |
| EV-K09-010 | `paper_content.txt`, `paper.pdf` | §3.3, Table 4--5 | quality by year / guideline use | 年份与是否引用 guideline 的质量均值比较 | 统计观察 | medium | F4 | 是 | 统计检验仅限本文样本 |
| EV-K09-011 | `paper_content.txt`, `paper.pdf` | Appendix Table A1 | sources searched | total/relevant/selected 漏斗计数 | 检索分母 | strong | F0 | 已做 layout；建议人工页码核验 | 源范围受限 |
| EV-K09-012 | `paper_content.txt`, `paper.pdf` | Appendix Table A2 | candidate articles not selected | 未纳入候选及排除原因 | 排除账本 | medium | L0-exclusion-reason | 已做 layout；建议人工页码核验 | 只含候选排除 |
| EV-K09-013 | `paper_content.txt`, `paper.pdf` | Appendix Table A3 | author affiliation details | study-author-institution-country 关系 | 关系边 | strong | F3, E-study-author | 已做 layout；建议人工页码核验 | 不代表当前地理格局 |
| EV-K09-014 | `paper_content.txt` | §4.5 | Limitations of this study | 手工搜索、单人选择/抽取加检查、范围限制 | 迁移边界 | strong | F5 | 否 | 只支撑边界，不支撑发现 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-K09-001 | 本文是完成型 tertiary review，主样本单位是纳入的 SLR/MA 二级研究，不是 primary studies | sample_unit | root | EV-K09-001, EV-K09-008 | strong | sample unit 判定、SUMMARY 修正 | primary studies 只作为 L1-num-primary 字段 |
| CLM-K09-002 | 本文有系统检索、纳排、数据抽取、质量评价和分析映射，可作为 schema seed 和局部统计候选 | pool_qualification | F0--F4 | EV-K09-003--EV-K09-011 | strong | 主统计池候选资格 | A2a 前不进入 final finding |
| CLM-K09-003 | 原生结构是维度森林，而不是六个通用 leaf 组成的单树 | tree_type | F0--F5 | EV-K09-005--EV-K09-014 | strong | 重写 `review.md` 维度树 | 六叶只能作跨论文投影 |
| CLM-K09-004 | §2.5 是原生叶子字段的核心来源，应优先于通用接口层 | leaf_source | F1 | EV-K09-006 | strong | 叶子表重写 | summary 字段需技术报告补证 |
| CLM-K09-005 | DARE QA1--QA4 构成独立质量评价树，取值空间为 Y/P/N/Unknown 并映射到 0--4 分 | quality_schema | F2 | EV-K09-005, EV-K09-009 | strong | 质量叶子、统计字段 | DARE 主观性见 §4.5 |
| CLM-K09-006 | RQ 在本文中是字段选择与结果组织的用途层，不是样本单位或树根 | rq_role | F4 | EV-K09-002, EV-K09-007 | strong | 防止 RQ 误建树 | RQ 可作为 relation edge 源节点 |
| CLM-K09-007 | 原文统计观察可用于方法学启发，但 2004--2007 EBSE 领域结论不可迁移为 Paper2 final finding | migration_boundary | F4/F5 | EV-K09-010, EV-K09-014 | strong | candidate finding 边界 | 需要跨论文与当前样本反证 |
| CLM-K09-008 | 现有 `review.md` 需要 repair：样本单位混写、证据账本过粗、六叶投影仍过显眼 | repair_needed | `review.md` | EV-K09-001--EV-K09-014 + 现有 review 结构 | strong | C/I/M 返修 | 不要求本任务直接修改文件 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering、unsupported claim 降级、review task 先列风险的原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 必须具体、可操作、证据绑定的原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 claim audit、evidence gap、revision priority 的 C/I/M 风险组织方式。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先读研究上下文、明确资源与风险、输出结构化 plan/schema 的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用不臆造细节、严格跟随原文 method/dataset/evaluation setup 的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用 structured schema、risk、task dependency 的组织方式，用于本报告的树/表/关系边。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated completion 思路；本任务不启动 autoresearch loop，只把“完成必须有可审计产物”作为输出纪律。

本输出最高风险 3 点：

1. Table 1 的“10 journals + 4 conference proceedings”与本地 PDF/text 表格可见来源行数存在轻微口径差异。合并时应人工打开 PDF 原版核对 Table 1 完整 venue 列。
2. Table 2/3/A1--A3 已用 `pdftotext -layout` 核验列结构，但未做截图级视觉核验。A2a 写入正式页码和表格数值前应人工复核 PDF。
3. `summary including RQ and answers` 字段在本文中指向技术报告 [24] Appendix 3，本地论文正文未完整展开。若要把该字段统计化，必须补技术报告；否则保持自由文本/weak。

blocked / timeout / 文件缺失：

- 未出现 blocked。
- 未出现 timeout。
- 指定必读文件均已读取。
- 本任务未修改仓库文件、未 commit、未 push、未发 gh comment、未启动 subagent。