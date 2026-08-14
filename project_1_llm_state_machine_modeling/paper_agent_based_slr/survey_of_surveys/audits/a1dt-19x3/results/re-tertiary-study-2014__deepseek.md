# re-tertiary-study-2014 · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是
  - 读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - 读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - 读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - 读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是
  - 读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - 读取 `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是
  - 读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是
  - 已阅读全部 966 行，覆盖摘要（Page 2）、引言（Page 2--3）、方法 / 搜索策略 / 质量评价（Page 3--5）、Table V 53 篇 SLR 分类总表（Page 5--6）、RQ2 QA 结果（Page 6）、Table VI Top 10 Cited（Page 6）、RQ3 gap 分析三类（Page 6--7）、Limitations Section IV（Page 7）、Discussion / Conclusion（Page 7）、Acknowledgments / References（Page 8）、Appendix A 全部 53 篇 SLR + 额外引用清单（Page 8--9）。
- **是否核对 `paper.pdf`**：否
  - `paper.pdf` 存在于本地路径，但本 reviewer 无视觉工具直接渲染 PDF；Table I（QA checklist）、Table V（53 篇 SLR 分类）、Table VI（Top 10 Cited）、Figure 1--4（趋势图）均通过 `paper_content.txt` 文本级推断。凡涉及页码 / 表号 / 图号精确核对处，均标注为 `not_verified` 并说明原因。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

Bano, Zowghi & Ikram (2014) 是一篇在 EmpiRE 2014 workshop 发表的 **Requirements Engineering 领域 tertiary study**。论文明确宣称"first tertiary study that aims to identify all the SLR published about RE related topics by following EBSE guidelines"（Paper Page 2）。

三个显式研究问题（RQ）：

- **RQ1**：What SLR have been published in RE?
  - 回答：53 篇 distinct SLR、64 篇 publication（某些 SLR 有多篇会议 + 期刊版本）、2006--2014 年跨度、按 RE 主题分类为 Table V 中的 **11 个主题大类**（Requirements Elicitation、Requirements Prioritization、Stakeholders and Users、Meta Modelling / Software Requirements Specifications、Requirements Verification/Validation/Evaluation、Requirements Traceability、Requirements Change Management、RE Education、Mobile Learning、Checklist for RE、Security Requirements 等）。
- **RQ2**：What is the quality of the published SLR in RE like?
  - 回答：通过 Table I 定义的 **4 条 QA 标准**（QA1 纳排标准是否描述与适当、QA2 搜索策略是否充分、QA3 是否评价纳入的一次研究质量、QA4 是否提供纳入一次研究概览/总结），对 51 篇可得全文的 SLR 评分（2 篇不可得）。42/51 得分 ≥ 2/4。关键 finding：**2009 年后平均质量下降**；超过半数 SLR 忽略 QA3 与 QA4。
- **RQ3**：What are the gaps in the coverage of RE research topics in the published SLR?
  - 回答以三类 gap 组织：(a) Anomalies——同一主题下不同 SLR 报告的一次研究数量不一致（如 S1 报告 8 篇 vs S4 报告 240 篇 prioritization）；(b) Lack of primary studies——某些 SLR 报告的一次研究极少（如 data quality requirements 和 causes of requirements change），可能因为检索不足或确实缺少实证文献；(c) Ignored RE areas——goal-oriented RE、RE in law、requirements modeling notations、conflict resolution、requirements negotiation、RE scaling、RE for self-management systems 等从未被 SLR 覆盖。

贡献声明（摘要末句与引言末段）：
- 首次为 RE 领域提供 SLR 的 comprehensive overview。
- 识别 RE SLR 的主题覆盖、质量和缺口。
- 作为 larger research plan 的第一步。

### 2.2 原文方法流程：检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

**检索**：
- 自动化搜索主要在线数据库：IEEE Xplore、ACM Digital Library、ISI Web of Science、Science Direct、Springer、Scopus、Google Scholar。
- 手工搜索 RE 和 SLR 相关会议 / 期刊（RE、REJ、REFSQ、IST、ESE、JSS 等）。
- 滚雪球（snowballing）：追踪引用和被引。
- 时间窗：2006--2014。

**纳排**（显式 inclusion/exclusion criteria，原文 method 段）：
- 纳入：English language、published empirical SLR with systematic protocol on RE topics。
- 排除：traditional reviews、non-empirical、non-RE、not SLR/SMS。

**数据抽取**：
- 从每篇纳入 SLR 抽取：SLR title、number of included primary studies、year of publication、RE topic classification、citation count（Google Scholar）、publication venue/channel。
- 作者对 53 篇 SLR 中的 51 篇可得全文，应用 Table I 的 4 条 QA 标准评分。

**分类 / taxonomy / coding scheme**：
- RE 主题分类采用自底向上的 emergent classification：作者从纳入 SLR 的实际主题聚类出 ~11 个 RE 大类（Table V），并标注与 Cheng & Atlee (2007) roadmap、Nuseibeh & Easterbrook (2000) 的对照关系。
- 这不是预先定义的外部 taxonomy，而是从样本中 emergent 的主题归类。

**统计**：
- 53 篇 SLR 按 RE 主题分布（频次）。
- 51 篇 QA 得分分布（频次直方图 Figure 2）。
- 按 QA 维度分布（柱状图 Figure 3）。
- 平均质量随年份变化（折线趋势图 Figure 4）。
- Top 10 高引用 SLR（Table VI，附 GS citation、venue、QA score）。

**Finding 形成**：
- RQ1 → descriptive listing + classification。
- RQ2 → QA 评分 → 趋势判断 "质量下降" + 原因推断（QA3/QA4 被忽略）。
- RQ3 → 三类 gap："anomalies"（跨 SLR 数量矛盾）、"lack of primary studies"（某些主题极少一次研究）、"ignored RE areas"（对比 roadmap 识别未覆盖主题）。
- 所有 finding 均回到纳入 SLR 的具体案例（S-ID 引用），并将 gap 判断与外部 roadmap 对照。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文包含以下显式信息结构，当前 `review.md` 的维度树应至少能容纳这些内容：

| 原文结构 | 内容 | 当前 review 是否覆盖 |
|---|---|---|
| **Table I：Quality Assessment Checklist** | 4 条 QA 标准（QA1/QA2/QA3/QA4），每题 0/0.5/1 评分 | 未在维度树中显式建模；`[leaf-re-tertiary-study-2014-orig-secondary-study-quality]` 只泛化为"二级研究质量字段"而未展开 QA 维度 |
| **Table V：SLR Classification by RE Topic** | 53 行，每行含 S-ID、SLR Title、# Primary Studies、Year、RE Topic Category，分属 ~11 个 RE 主题大类 | `[leaf-re-tertiary-study-2014-orig-re-topic]` 只提及"需求获取、建模、验证、管理、追踪、质量等子主题"但未枚举完整分类项 |
| **Table VI：Top 10 Highly Cited SLR** | S-ID、GS Citations、Pub Channel、QA Score | 未建模，citation / venue / QA 交叉分析缺失 |
| **Figure 1**：SLR publications over years | 时间序列 | 未建模 |
| **Figure 2**：QA score distribution | 51 篇直方图 | `[leaf-re-tertiary-study-2014-orig-secondary-study-quality]` 间接覆盖 |
| **Figure 3**：QA score per check | 4 条 QA 准则各自的柱状分布 | 同上，未展开到 QA 维度 |
| **Figure 4**：Average quality score by year | 趋势线 | 未建模时间维度 |
| **RQ1/RQ2/RQ3 结构** | 原文按 RQ 组织结果和 discussion | 维度树未按 RQ 组织；b1--b5 是跨论文通用分组 |
| **Gap 三类分析框架** | anomalies / lack of primary studies / ignored RE areas | `[leaf-re-tertiary-study-2014-orig-method-gap]` 只泛化为"方法缺口字段" |
| **Search strategy 信息** | 自动化 + 手工 + snowballing + 具体数据库列表 + 纳排标准 | `[leaf-re-tertiary-study-2014-corpus]` 可覆盖但过于泛化 |
| **Limitations / Threats** | Section IV 明确了搜索覆盖风险、单 reviewer 偏差、可复制性限制 | `EV-re-tertiary-study-2014-004` 有记录但未作为独立维度叶子 |
| **Appendix A：Complete SLR list** | 全部 53 篇 SLR 的完整引用 + citation count | 未建模 |
| **SLR 类型分类** | 原文在引言区分为 conventional SLR / systematic mapping / tertiary study | 未建模 |

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的 finding 形成链路高度明确：

1. **字段层**：Table V 的每条记录 = (S-ID, Topic, #Primary Studies, Year, Venue) + Table I QA score（可选，51/53 有）+ Google Scholar citations。
2. **统计层**：
   - 描述统计：53 SLR × topic 分布、51 SLR × QA score 分布。
   - 趋势分析：年度 SLR 数量增长 + 年度平均 QA 下降（Figure 1 + Figure 4 联合解读）。
   - 引用分析：Table VI Top 10 Cited 按 venue 和 QA 交叉。
3. **Finding 层**：
   - RQ2 finding："质量自 2009 年后下降"← Figure 4 趋势 + Figure 3 QA3/QA4 偏低。
   - RQ3 anomaly finding："S1 vs S4 在 prioritization 上报告一次研究数量矛盾"← Table V 具体 S-ID 对比。
   - RQ3 gap finding："goal-oriented RE、RE in law、modeling notations 未被 SLR 覆盖"← 对照 Cheng & Atlee 2007 roadmap 和 Nuseibeh & Easterbrook 2000。
4. **Recommendation 层**：
   - 强调需要 replicate S1 等低质量 SLR。
   - 呼吁社区关注 gap 区域。
   - 指出应强制要求 SLR 报告 QA3（primary study quality assessment）和 QA4（summary of included studies）。

## 3. 当前 `review.md` 维度树审计

### 3.1 审计总判断

当前 `review.md` 的维度树**诚实但不足**。它诚实地将 6 叶子标注为"跨论文通用接口层"，并补充 4 个 `not_verified` orig-* 候选叶子。但：

1. **6 叶子的通用接口层是对原文 schema 的投影而非复原**——树中每个 leaf 的取值空间、证据要求和定义都是跨论文通用的抽象描述，而非从原文中逐字段抽取的具体 schema。
2. **4 个 orig-* 候选叶子数量不足、归属分支有误差、且全部 `not_verified`**——当所有原文模式叶子都以 `not_verified` 状态出现时，A2a 无法区分"原文有但未核验"和"原文确实没有"。
3. **原文中大量明确、可操作的字段 / 分类 / 表格结构未被映射到任何叶子**——包括 QA rubric 的 4 条具体标准、RE 主题分类的 ~11 个类别、时间维度、引用维度、SLR 类型维度、gap 三类范式。

综合判断：**当前树不会向 A2a 传递足以指导原文 schema 精确字段抽取的可操作信息**。A2a 执行者拿到这个维度树后，仍需从头阅读 `paper_content.txt` 才能知道原文到底抽取了哪些字段、用了什么分类、怎么做的统计。这与 survey-of-surveys 脚手架的核心目的——从既有综述中提取可演化的维度模式先验——之间存在实质性张力。

### 3.2 逐项审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-re-tertiary-study-2014-root]` = "Systematic Reviews in Requirements Engineering"，与原文标题一致；根节点只复原本文内部 schema，不自称 Paper2 目标领域结论；审计口径正确。 | 通过 |
| 主干分支是否覆盖原文 schema | **I** | 5 条主干分支（b1--b5）是按 A1-M0--M6 脚手架元维度投影的**跨论文通用分组**，并非原文自身的章节 / RQ / 抽取结构。原文的 3 条 RQ 和对应的结果 / discussion 组织（RQ1→Table V listing、RQ2→QA 分析、RQ3→三类 gap）在树中不可见。原文 Introduction 中 SLR 三类区分（conventional SLR / mapping / tertiary）在树中不可见。**树形正确但语义空泛**：分支名称覆盖范围足够宽，但无法告知 A2a 原文内具体有哪些字段。 | I |
| 叶子维度是否足够具体 | **I** | 6 个 leaf-* 的取值空间全部是跨论文通用描述（如"自由文本加 RQ / 贡献声明引用"、"完整枚举 / 层级枚举 / 自由文本加理由"），未嵌入原文的具体分类项、具体 QA 标准、具体 gap 类型。`[leaf-re-tertiary-study-2014-taxonomy]` 定义说"复原原文中的 taxonomy、classification schema"，但叶子取值空间中未出现原文 Table V 的 ~11 个 RE 主题类别。一个接手 A2a 的人无法从这个叶子推断原文到底用了什么分类。 | I |
| 取值空间是否可执行 | **I** | 6 个通用 leaf 的取值空间对任意一篇 SLR/SMS 论文都适用——这正是问题所在。取值空间的可执行性来自"我能判断这一篇论文在这个字段上应该填什么"，而当前取值空间全部是类型级描述（"层级枚举、关系值或开放 action point"），不包含具体值的枚举。原文实际可执行字段——如 QA1--QA4 的 0/0.5/1 评分、Table V 的 ~11 个 RE 主题类别、SLR 类型三类——均未出现在叶子取值空间中。 | I |
| 关系边是否缺失 | **I** | 树中只建模了父子层级（dim → leaf），未建模叶子之间的交叉关系。原文中 QA score × citation count × venue × year × topic 的交叉是核心统计（Table VI 即为 QA × citation × venue 的交叉表；Figure 4 为 QA × year 的趋势），当前树无法表达这些交叉统计关系。`pattern-field-schema.md` §8.3 定义了关系边合同（源节点、关系类型、目标节点、目标取值空间），但本文 `review.md` 完全未使用。 | I |
| 统计用途 / 分母是否正确 | 通过 | `review.md` 正确声明当前仅作 `schema_seed`，不进入 SUMMARY 定量统计；分母标注（"当前 19 篇样本"）和降级理由（"A.2/A.3 多数证据仍待 A2a 精确锚定"）与 `pattern-field-schema.md` §8.6 的 A1-DT 临时降级规则一致。 | 通过 |
| 候选 finding 路径是否完整 | **I** | `[leaf-re-tertiary-study-2014-finding]` 定义的用途是"统计用途、候选发现、boundary anchor、risk_only"，但这实际上是用途分类而非 finding 路径。原文的 finding 路径非常具体：字段 → 统计 → (anomaly / gap / trend 类型) → 对照外部 roadmap → recommendation。当前树只覆盖了"字段→候选发现"这一段，缺失中间的类型学（anomaly/gap/trend/recommendation）和外参照（roadmap/guideline 对照）。 | I |
| A.1--A.4 证据链是否足够 | **I** | A.1 有 4 条来源记录（pdf、text、bib、meta），A.2 有 4 条证据条目（EV-001 到 EV-004），A.3 有 10 条结论映射，A.4 有 2 条复验命令。结构完整、回链正确。但核心问题在证据强度：**4 条 A.2 证据中有 3 条为 `not_verified`**（EV-001/002/003），且 EV-002 和 EV-003 都标注"需要原文版面核验=true"。这意味 A.3 中所有 leaf_definition 结论（C02--C07）都建立在 `not_verified` 的证据上，结论强度全部为 `weak`、用途全部为 `schema_seed`。这种"全部 weak + 全部 schema_seed"的状态虽然保守安全，但也意味着当前证据链对原文 schema 复原没有提供任何可靠的升级路径——因为连"哪个字段原文确实有"都还是 `not_verified`。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | `review.md` 在 §维度树复原 开头明确声明"六个 leaf-* 是跨论文通用接口层"、"不是对原文全部抽取字段、分类项或报告叶子的完成复原"，并在 4 个 orig-* 候选叶子中全部标注 `not_verified` 和 `schema_seed`。没有把通用接口误写为原文 schema 完成复原。审查通过。 | 通过 |

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树。该树在保留现有 5 条主干分支（作为跨论文可对照的通用层）的同时，将所有原文中实际存在的字段 / 分类 / 表格结构作为**原文叶子**就地展开，并标注具体取值空间和证据来源。

### 4.1 改进树结构

```text
[dim-re-tertiary-study-2014-root] Systematic Reviews in Requirements Engineering (2014)
│
├── [dim-re-tertiary-study-2014-b1] 综述目标与研究问题
│   ├── [leaf-re-tertiary-study-2014-scope] 研究范围与单位对象  ← 保留通用 leaf
│   ├── [leaf-re-tertiary-study-2014-orig-rq1] RQ1: What SLR published in RE?
│   │   └── 取值：53 distinct SLR, 64 publications, 2006--2014
│   ├── [leaf-re-tertiary-study-2014-orig-rq2] RQ2: Quality assessment of RE SLR
│   │   └── 取值：51/53 QA scored, 42/51 ≥ 2/4
│   ├── [leaf-re-tertiary-study-2014-orig-rq3] RQ3: Gaps in RE SLR coverage
│   │   └── 取值：三类 gap（anomalies / lack of primary studies / ignored RE areas）
│   └── [leaf-re-tertiary-study-2014-orig-slr-type-def] SLR 类型定义
│       └── 取值：conventional SLR / systematic mapping study / tertiary study
│
├── [dim-re-tertiary-study-2014-b2] 语料收集与纳排
│   ├── [leaf-re-tertiary-study-2014-corpus] 语料与纳排链条  ← 保留通用 leaf
│   ├── [leaf-re-tertiary-study-2014-orig-search-dbs] 搜索数据库
│   │   └── 取值：IEEE, ACM, ISI WoS, Science Direct, Springer, Scopus, Google Scholar
│   ├── [leaf-re-tertiary-study-2014-orig-search-method] 搜索方式
│   │   └── 取值：automated / manual / snowballing
│   ├── [leaf-re-tertiary-study-2014-orig-incl-excl] 纳排标准
│   │   └── 取值：English / empirical SLR with protocol / RE topic / not traditional review
│   ├── [leaf-re-tertiary-study-2014-orig-time-window] 时间窗
│   │   └── 取值：2006--2014
│   └── [leaf-re-tertiary-study-2014-orig-distinct-vs-pub] distinct SLR vs publications
│       └── 取值：53 distinct SLR / 64 publications；部分 SLR 有会议+期刊双版本
│
├── [dim-re-tertiary-study-2014-b3] 主题 / 对象分类
│   ├── [leaf-re-tertiary-study-2014-taxonomy] 主题与维度分类  ← 保留通用 leaf
│   ├── [leaf-re-tertiary-study-2014-orig-re-topic] RE 主题分类（Table V）
│   │   └── 取值：~11 个 emergent 类别（Elicitation / Prioritization / Stakeholders & Users /
│   │       Meta Modelling & Specifications / Verification-Validation-Evaluation /
│   │       Traceability / Change Management / RE Education / Mobile Learning /
│   │       Checklist for RE / Security Requirements 等）
│   ├── [leaf-re-tertiary-study-2014-orig-slr-type] SLR 类型（每条纳入记录的属性）
│   │   └── 取值：conventional SLR / systematic mapping / tertiary（按原文引言三类定义）
│   └── [leaf-re-tertiary-study-2014-orig-ext-ref] 外参照物
│       └── 取值：Cheng & Atlee 2007 RE roadmap / Nuseibeh & Easterbrook 2000
│
├── [dim-re-tertiary-study-2014-b4] 方法 / 技术 / 干预
│   ├── [leaf-re-tertiary-study-2014-method] 方法 / 技术 / 干预分类  ← 保留通用 leaf
│   └── [leaf-re-tertiary-study-2014-orig-reviewer] 数据抽取执行者
│       └── 取值：single reviewer（原文 Limitation 中明确报告）
│
└── [dim-re-tertiary-study-2014-b5] 评价、统计与候选发现
    ├── [leaf-re-tertiary-study-2014-evidence] 评价、证据与复现资产  ← 保留通用 leaf
    ├── [leaf-re-tertiary-study-2014-finding] 统计观察与候选发现  ← 保留通用 leaf
    ├── [leaf-re-tertiary-study-2014-orig-qa-rubric] QA rubric（Table I）
    │   └── 取值：QA1 纳排描述 / QA2 搜索充分 / QA3 一次研究质量评价 / QA4 一次研究概览
    │       评分：0 / 0.5 / 1 每项，总分 0--4
    ├── [leaf-re-tertiary-study-2014-orig-qa-score] QA score per SLR
    │   └── 取值：51/53 × 0--4 分；统计口径：42/51 ≥ 2，9/51 < 2
    ├── [leaf-re-tertiary-study-2014-orig-citation] Citation count
    │   └── 取值：Google Scholar citations per SLR；Table VI Top 10 范围 41--154
    ├── [leaf-re-tertiary-study-2014-orig-venue] Publication venue
    │   └── 取值：RE / IST / REJ / JS / ITSE / CSI / ESEM 等（Table VI 样例）
    ├── [leaf-re-tertiary-study-2014-orig-year] Publication year
    │   └── 取值：2006--2014，可统计（Figure 1 年度分布，Figure 4 QA×year 趋势）
    ├── [leaf-re-tertiary-study-2014-orig-gap-type] Gap 类型
    │   └── 取值：anomalies（跨 SLR 矛盾）/ lack of primary studies / ignored RE areas
    ├── [leaf-re-tertiary-study-2014-orig-recommendation] Recommendation type
    │   └── 取值：replicate low-quality SLR / fill gap areas / mandate QA3+QA4 in SLR
    └── [leaf-re-tertiary-study-2014-orig-limitation] Limitation / threat
        └── 取值：search coverage risk / single reviewer bias / replicability limits
```

### 4.2 关键改进说明

| 改进点 | 当前 review 状态 | 建议状态 | 理由 |
|---|---|---|---|
| 原文 RQ 结构 | 未建模 | 新增 3 个 RQ leaf + 1 个 SLR 类型 leaf | 原文按 RQ 组织全部结果和 discussion；SLR 类型是引言中明确区分的三类，影响后续纳排和分类 |
| Table I QA rubric | `orig-secondary-study-quality` 笼统覆盖 | 新增 `orig-qa-rubric`（4 标准枚举）+ `orig-qa-score`（每篇得分） | 原文的 QA 是 4 条有具体评分的标准，不是笼统的"二级研究质量字段"；可统计（频次、均值、趋势） |
| Table V RE 主题分类 | `orig-re-topic` 只列"需求获取、建模、验证..." | 补充完整的 ~11 个 emergent 类别枚举 | 原文的 RE 主题分类是核心 finding 载体（RQ1），取值空间在 Table V 中已有完整枚举 |
| Table VI Citation × Venue 交叉 | 未建模 | 新增 citation leaf + venue leaf | 原文用 citation 和 venue 分析 SLR 影响力和质量关联 |
| 时间维度 | 未建模 | 新增 year leaf | Figure 1（年度分布）、Figure 4（QA × year 趋势）是原文核心统计发现 |
| Gap 三类框架 | `orig-method-gap` 笼统覆盖 | 新增 `orig-gap-type`（三类枚举）+ `orig-recommendation` | 原文 RQ3 明确按三类 gap 组织：anomalies / lack of primary studies / ignored areas，并给出 recommendation |
| SLR 类型 | 未建模 | 新增 `orig-slr-type` | 原文引言明确区分 conventional SLR / mapping / tertiary，影响纳入标准的理解 |
| 外参照物 | 未建模 | 新增 `orig-ext-ref` | 原文用 Cheng & Atlee 2007 和 Nuseibeh & Easterbrook 2000 roadmaps 判断 gap，这不只是作者讨论，是方法论组成部分 |
| 纳排标准具体内容 | 笼统在 b2 覆盖 | 新增 `orig-incl-excl`、`orig-search-dbs`、`orig-search-method`、`orig-time-window` | 原文 method 段明确列出了这些信息；对 A2a 的字段设计有直接参考价值 |
| distinct-study vs publication | `review.md` §3 建议过但未建模 | 新增 `orig-distinct-vs-pub` | 原文明确区分 53 SLR / 64 publications，是 tertiary study 的常见陷阱 |
| Limitation / threat 独立建模 | 只在 A.2 记录为 EV-004 | 新增 `orig-limitation` leaf | 原文 Section IV 是全文 limitations，应作为独立叶子而非只在证据账本中出现 |

### 4.3 保留现有 6 通用 leaf 的理由

现有 6 个 leaf-*（scope, corpus, taxonomy, method, evidence, finding）作为跨论文对照层保留——它们提供了统一的分类框架，允许跨 19 篇 survey-of-surveys 论文做横向对比。但应将它们标注为 `[universal-interface]` 节点类型，与原文具体叶子 `[orig-*]` 明确区分，避免混淆。`pattern-field-schema.md` §8.2 已经允许这种双层结构：通用接口层 + 原文叶子全集层。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 维度树缺少原文 RQ 结构 | `review.md` §维度树 → b1 下新增叶子 | 新增 `[leaf-re-tertiary-study-2014-orig-rq1]`、`[leaf-re-tertiary-study-2014-orig-rq2]`、`[leaf-re-tertiary-study-2014-orig-rq3]`，取值空间为具体 RQ 文字和对应答案摘要 | `paper_content.txt` Page 2 & Page 5--7 | I |
| 维度树缺少 SLR 类型定义 | `review.md` §维度树 → b1 或 b3 下新增叶子 | 新增 `[leaf-re-tertiary-study-2014-orig-slr-type-def]`，取值 conventional SLR / systematic mapping / tertiary study | `paper_content.txt` Page 2 Introduction | I |
| Table I QA rubric 未展开 | `review.md` §原文模式候选叶子映射 | 将 `[leaf-re-tertiary-study-2014-orig-secondary-study-quality]` 拆分为 `orig-qa-rubric`（4 标准枚举 + 评分 0/0.5/1）和 `orig-qa-score`（每篇得分），或在其取值空间中明确写入 4 条 QA 标准 | `paper_content.txt` Page 3 Table I 描述 + Page 6 QA results | I |
| RE 主题分类未完整枚举 | `review.md` §原文模式候选叶子映射 → `orig-re-topic` | 在候选取值空间中列出 Table V 中实际出现的 ~11 个 RE 主题类别（Elicitation / Prioritization / Stakeholders / Specifications / V&V / Traceability / Change Management / Education / Mobile Learning / Checklist / Security Requirements 等），并标注"emergent classification"来源 | `paper_content.txt` Page 5--6 Table V | I |
| Citation / venue / year 维度完全缺失 | `review.md` §维度树 → b5 下新增叶子 | 新增 `orig-citation`（GS citation count）、`orig-venue`（publication venue）、`orig-year`（publication year），这些是 Table VI 和 Figure 1/4 的核心字段 | `paper_content.txt` Page 6 Table VI + Figures 1--4 | I |
| Gap 类型学未建模 | `review.md` §原文模式候选叶子映射 | 将 `[leaf-re-tertiary-study-2014-orig-method-gap]` 重新定位到 b5，改名为 `orig-gap-type`，取值空间写为 anomalies / lack of primary studies / ignored RE areas 三类 | `paper_content.txt` Page 6--7 RQ3 results | I |
| 外参照物缺失 | `review.md` §维度树 | 新增叶子记录原文的外部 roadmap 对照（Cheng & Atlee 2007、Nuseibeh & Easterbrook 2000），因为作者正是以此判断 gap，这不只是 background 引用 | `paper_content.txt` Page 7 对照段落 | I |
| Limitation 应作为独立叶子 | `review.md` §维度树 → b5 下新增叶子 | Section IV "Limitations of the Study" 包含 search coverage risk、single reviewer bias、replicability limits，应作为独立 `orig-limitation` 叶子而非只在 A.2 证据中出现 | `paper_content.txt` Page 7 Section IV | I |
| Search strategy 具体字段缺失 | `review.md` §维度树 → b2 下新增叶子 | 新增 `orig-search-dbs`（数据库列表）、`orig-search-method`（automated/manual/snowballing）、`orig-incl-excl`（纳排标准文本）、`orig-time-window`（2006--2014），这些字段是原文 method 段显式内容，对 A2a 设计搜索和纳排字段有直接参考价值 | `paper_content.txt` Page 3--4 Method | M |
| Distinct vs publication 区分缺失 | `review.md` §维度树 → b2 下新增叶子 | 新增 `orig-distinct-vs-pub`，取值（53, 64），这是 tertiary study 的核心操作细节，A2a 设计去重逻辑时应考虑 | `paper_content.txt` Page 2 Abstract + Page 3 | M |
| 4 个 orig-* 全部 not_verified 导致 A2a 入口模糊 | `review.md` §原文模式候选叶子映射 + A.2 证据账本 | 至少将那些在 `paper_content.txt` 中已有明确文本证据的字段（如 orig-re-topic 的 emergent 类别、orig-qa-rubric 的 4 条 QA 标准）从 `not_verified` 升级为 `weak`，并标注"全文文本级；图表待人工核对"；只对那些确实需要打开 PDF 核对的图表数值保留 `not_verified` | `paper_content.txt` 全文文本 + `pattern-field-schema.md` §4 证据等级枚举 | I |
| 关系边完全缺失 | `review.md` §维度树 | 至少补充 2 条跨叶子的关系边：(a) QA score × Year → 用于 Figure 4 趋势；(b) QA score × Citation × Venue → 用于 Table VI 交叉分析。按 `pattern-field-schema.md` §8.3 合同记录 | `paper_content.txt` Pages 5--7 | M |
| §2 六类 pattern 的 finding pattern 过于泛化 | `review.md` §2 | "finding pattern" 当前写"具体结论需进一步深读结果章节"——但原文已有完整 RQ2/RQ3 finding。应改为具体描述：原文按 RQ 组织 finding、三类 gap 类型学（anomaly / lack / ignored）、对照外部 roadmap 判断 gap | `paper_content.txt` Page 6--7 | I |

## 6. C/I/M 结论

### C（Critical）：破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

本审计**未发现 C 级问题**。

`review.md` 的维度树虽然过于泛化，但它诚实声明了 6 叶子是"通用接口层"、4 个 orig-* 是 `not_verified` 种子、所有结论强度为 `weak`、用途为 `schema_seed`。这种保守姿态防止了误导 A2a，不会直接破坏 Paper2 的证据链。最大风险是"信息不足导致 A2a 做无用功"，但这属于 I 级而非 C 级。

### I（Important）：实质影响维度树可用性、原文 schema 复原、证据可审计性

共 **8 项 I 级问题**：

| # | 问题 | 影响的学术目标 / 证据链 |
|---|---|---|
| I-1 | 6 叶子取值空间全部是跨论文通用描述，未嵌入原文具体字段 / 分类 / 标准 | A2a 无法从维度树推断原文 schema，必须回头重读 `paper_content.txt`，使脚手架失去"模式先验"的加速价值 |
| I-2 | 4 个 orig-* 全部 `not_verified`，但其中部分字段在 `paper_content.txt` 已有清晰文本证据（如 RE 主题 emergent 类别、4 条 QA 标准） | 把"原文确实有"和"确实需要 PDF 核对"混为一谈，A2a 无法判断优先级 |
| I-3 | 维度树缺少原文 RQ 结构（3 RQs）和 SLR 类型定义 | 原文的方法论骨架（问题→结果→finding）不可见，A2a 可能误解为笼统的描述统计 |
| I-4 | Table I QA rubric 未展开为具体 QA 标准枚举 | QA rubric 是原文的核心方法贡献（4 条标准 + 评分体系），当前只作为笼统"二级研究质量字段" |
| I-5 | Citation / venue / year 维度完全缺失 | 原文的 cross-tabulation 证据呈现模式（Table VI QA × citation × venue）对 A2a 设计交叉统计有重要参考价值 |
| I-6 | Gap 三类框架被压入 `orig-method-gap` 且挂在 b4（方法/技术/干预），语义不匹配 | Gap 分析是原文 RQ3 的核心 finding 模式，对 Paper2 的 candidate finding 形成有直接启发 |
| I-7 | A.3 所有结论建立在 `not_verified` 证据上，且全部 `weak` + `schema_seed` | 虽然保守安全，但证据链无法为原文 schema 复原提供任何可升级路径 |
| I-8 | §2 finding pattern 写"具体结论需进一步深读结果章节"，但原文已有完整 RQ2/RQ3 finding 在 `paper_content.txt` 中 | 降低 review 本身的可用性 |

### M（Minor）：不阻塞的清晰度或维护性建议

共 **3 项 M 级问题**：

| # | 问题 |
|---|---|
| M-1 | Search strategy 具体字段（数据库列表、纳排标准文本、时间窗）未独立建模，虽然 b2 分支语义覆盖，但缺少原文级细节 |
| M-2 | Distinct SLR (53) vs publications (64) 的区分虽在 §3 提到过但未在维度树中建模 |
| M-3 | 关系边完全缺失，按 `pattern-field-schema.md` §8.3 合同应至少补充 QA × year 和 QA × citation × venue 两条 |

### 最终建议

**NEEDS FIX**。

理由：当前维度树的"通用接口层 + not_verified 种子"结构虽然诚实，但实质信息含量不足以支撑 A2a 从本文中提取可操作的维度模式先验。建议按本报告 §4（建议维度树骨架）和 §5（修正清单）完成至少 I-1 到 I-7 的修复后重新审计。修复的最小可行范围：

1. 在 6 通用 leaf 之外，按 §4.1 的树结构补充原文具体叶子（orig-*），将每个叶子的取值空间填写为原文中实际出现的枚举值或文本描述（而非跨论文通用类型描述）。
2. 对 `paper_content.txt` 中已有明确文本证据的 orig-* 叶子（RE 主题类别、QA 4 标准、3 条 RQ、3 类 gap、citation/venue/year），将证据强度从 `not_verified` 升级为 `weak`（全文文本级；图表待人工核对），并在 A.2 中补充逐叶子的证据条目。
3. 修正 `orig-method-gap` 的分支归属（从 b4 移至 b5）和语义（从"方法缺口"改为"gap 类型"）。
4. 更新 §2 finding pattern 为原文实际内容。

### 能力使用审计（按 `ai-research-writing-skill` SKILL.md 要求）

```markdown
### Capability-use audit
- Required references/scripts: SKILL.md × 3, references × 6, 文库规则 × 5, paper 文件 × 5
- Inputs consumed: paper_content.txt (966 lines full), review.md (170 lines full), bibtex.bib, metadata.json, GUIDE/SUMMARY/README/pattern-field-schema/paper_story
- Inputs not used and why: paper.pdf（无视觉工具直接渲染，已标注）
- Artifacts produced: audits/a1dt-19x3/results/re-tertiary-study-2014__deepseek.md
- Verification run: 未运行命令，全文审计为人工审核
- Remaining risk: paper.pdf 的 Table I/Table V/Table VI/Figure 1--4 图表级精核需人工完成
```
