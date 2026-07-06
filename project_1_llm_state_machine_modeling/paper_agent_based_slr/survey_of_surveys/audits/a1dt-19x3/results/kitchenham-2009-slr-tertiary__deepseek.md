# kitchenham-2009-slr-tertiary · deepseek 全文审计报告

## 1. 审计身份与输入

| 字段 | 内容 |
|---|---|
| reviewer 身份 | deepseek（PR #135 学术 reviewer） |
| 是否读取 `$ai-research-writing-skill` | 是，路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` |
| 是否读取 `$research-planning` | 是，路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`，并读取 `references/planning-prompts.md` |
| 是否读取 `$oh-my-codex:autoresearch` | 是，路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` |
| 是否完整阅读 `paper_content.txt` | 是。完整阅读了全部 962 行（Page 1--9），覆盖：abstract、目录结构、Section 1 Introduction、Section 2 Method（2.1 RQ、2.2 Search process、2.3 Inclusion/exclusion criteria、2.4 Quality assessment / DARE QA1--QA4、2.5 Data collection / extraction form、2.6 Data analysis / tabulation plan、2.7 Deviations from protocol）、Section 3 Results（3.1 Search results / Table A1、3.2 Quality evaluation / Table 3、3.3 Quality factors / Table 4--5）、Section 4 Discussion（4.1--4.4 逐一回答 RQ1--RQ4）、Section 4.5 Limitations of this study、Section 5 Conclusions、Appendix Tables A1--A3、References [1]--[42] |
| 是否核对 `paper.pdf` | 否。`paper.pdf` 文件存在（150804 bytes），但本轮未进行视觉核对。原因：paper_content.txt 文本提取完整、可读，且该论文的 extraction form、QA schema、tabulation plan 和 RQ 结构在纯文本中已充分暴露；主要缺失项（表格精确数值、页码、版式布局）已在本报告中标注为需后续 A2a PDF 核验。 |
| 文库级规则与 story 读取 | 已读取 `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md` 和 `paper_agent_based_slr/story/paper_story.md` |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

论文标题：*Systematic literature reviews in software engineering – A systematic literature review*（Kitchenham et al., 2009, IST）。

论文性质：**tertiary study**（对 SE SLR 的 SLR），又称 tertiary-like SLR。目标：评估自 2004 年 ICSE04 提出 EBSE 以来，系统综述（SLR）对软件工程的影响。

明确写了 **4 个 RQ**（Section 2.1）：

1. **RQ1**：自 2004 年以来 EBSE 活动有多少？（How much EBSE activity?）
2. **RQ2**：正在研究哪些主题？（What research topics?）
3. **RQ3**：谁在领导 EBSE 研究？（Who is leading?）
4. **RQ4**：当前研究有哪些限制？（What are the limitations?），细分为 4 个子问题：
   - RQ4.1：主题覆盖是否有限？
   - RQ4.2：每个 SLR 用了多少 primary studies？
   - RQ4.3：SLR 质量如何？
   - RQ4.4：SLR 是否提供了面向实践者的指南？

### 2.2 原文方法流程

论文使用标准 SLR 方法，**manual search** 策略（非自动化数据库搜索）：

1. **检索（Section 2.2）**：手动搜索 10 种期刊 + 4 个会议论文集（Table 1），时间窗 2004-01-01 至 2007-06-30。
2. **纳排（Section 2.3）**：纳入有定义 RQ + 搜索过程 + 数据抽取的 SLR 和 meta-analysis；排除 informal literature surveys、方法论文、重复报告。
3. **数据抽取（Section 2.5）**：有**显式的 extraction form**，共 10 个字段（详见下文 §2.3）。
4. **质量评价（Section 2.4）**：使用 York University CRD DARE 标准，**4 个 QA 问题**（QA1--QA4），评分 Y=1, P=0.5, N=0, Unknown。
5. **数据分析（Section 2.6）**：按 8 种方式 tabulate 数据，分别对应各 RQ。
6. **人员分工**：单 extractor + 单 checker，与 Kitchenham 2004 guideline 建议的 double extraction 不一致（Section 2.7 已有 protocol deviation 说明）。

### 2.3 原文显式 Extraction Form、Classification Schema、Taxonomy、Coding Scheme

该论文有**非常显式的、逐字段定义的数据抽取表单和分类体系**，具体包括：

#### A. 数据抽取表单（Section 2.5，精确原文字段列表）

| 抽取字段 | 原文对应 | 操作化 |
|---|---|---|
| 来源 | The source (journal or conference) and full reference | 期刊/会议名 + 完整引用 |
| 研究类型 | Classification of the study Type (SLR, Meta-Analysis MA) | SLR 或 MA |
| 研究范围 | Scope (Research trends or specific technology evaluation question) | 研究趋势 / 技术评估 |
| 主主题 | Main topic area | 软件工程子领域（cost estimation / testing / experiments / ...） |
| 作者与机构 | The author(s) and their institution and the country where it is situated | 作者名、机构、国家 |
| 摘要含 RQ 与答案 | Summary of the study including the main research questions and the answers | 结构化的 RQ + 答案 |
| RQ/问题 | Research question/issue | 具体 RQ 文本 |
| 质量评价 | Quality evaluation | DARE QA1--QA4 的 Y/P/N 打分 |
| 引用 EBSE/SLR guideline | Whether the study referenced the EBSE papers [23,5] or the SLR Guidelines [22] | 布尔型 |
| 实践指南 | Whether the study proposed practitioner-based guidelines | 布尔型 |
| primary study 数量 | How many primary studies were used in the SLR | 数值 |

共计 **11 个显式字段**（原文列出 10 项，其中 "Summary, RQs and answers" 可进一步拆分为摘要、RQ、答案）。

#### B. 质量评价 schema（Section 2.4，DARE criteria）

| QA 编号 | 问题 | 评分标准 |
|---|---|---|
| QA1 | Are the review's inclusion and exclusion criteria described and appropriate? | Y/P/N |
| QA2 | Is the literature search likely to have covered all relevant studies? | Y=≥4 DL + extra strategies; P=3-4 DL or restricted journals; N=≤2 DL or extremely restricted |
| QA3 | Did the reviewers assess the quality/validity of the included studies? | Y=explicit quality criteria extracted; P=quality addressed; N=no explicit assessment |
| QA4 | Were the basic data/studies adequately described? | Y=info per study; P=summary only; N=not specified |

评分：Y=1, P=0.5, N=0, Unknown。这是**完整的 coding scheme**，带有明确的取值语义。

#### C. 分类体系（贯穿 Section 2.3、2.5、2.6）

- 研究类型：SLR / Meta-Analysis (MA)
- 研究范围：Research trends / Specific technology evaluation question
- 主题分类（实际 data 中识别）：Cost estimation / Testing / Software engineering experiments
- 出版 venue：10 journals + 4 conferences（Table 1）
- 是否引用 guideline / EBSE paper：是/否
- 是否提出 practitioner guideline：是/否

#### D. 数据 tabulation 方案（Section 2.6，显式对应各 RQ）

| 统计方式 | 对应 RQ |
|---|---|
| #SLRs published per year and source | RQ1 |
| Whether SLR referenced EBSE papers or SLR guidelines | RQ1 |
| #studies in each major category (research trends / technology questions) | RQ2, RQ4.1 |
| Topics studied and their scope | RQ2, RQ4.1 |
| Author affiliations and institutions | RQ3 |
| #primary studies in each SLR | RQ4.2 |
| Quality score for each SLR | RQ4.3 |
| Whether SLR proposed practitioner-oriented guidelines | RQ4.4 |

### 2.4 原文证据表

| Table | 内容 | 功能 |
|---|---|---|
| Table 1 | Selected journals and conference proceedings | 检索范围 |
| Table 2 | Summary of 20 included studies | 主证据表：作者、年份、标题、source、研究类型、scope、topic、primary studies、guidelines |
| Table 3 | Quality evaluation of SLRs (QA1--QA4 scores per study) | 质量证据主表 |
| Table 4 | Average quality scores by publication year | 质量趋势分析 |
| Table 5 | Average quality score by guideline usage | 质量与 guideline 关系 |
| Table A1 | Sources searched for years 2004--2007（每 venue 每年 total/relevant/selected） | 检索分母证据 |
| Table A2 | Candidate articles not selected（含排除理由） | 纳排透明度 |
| Table A3 | Author affiliation details | RQ3 证据 |

### 2.5 原文 Finding / Conclusion / Roadmap 形成方式

论文从统计表格和质性分析形成 finding，对应到 RQ 结构：

1. **RQ1 (EBSE activity)**：20 篇相关研究，19 SLR + 1 MA。12 篇 technology evaluation，8 篇 research trends。8 篇引用 guideline，2 篇引用 EBSE paper。IEEE SW/TSE 各 4 篇，JSS 3 篇，IST 2 篇。（统计 finding）
2. **RQ2 (Topics)**：7 篇 cost estimation，3 篇 experiments，3 篇 testing。Cost estimation 领域已形成证据链，有具体 RQ→答案。Testing 只有 3 篇。（主题分布 finding）
3. **RQ3 (Who is leading)**：European-dominated。Simula Research Laboratory（挪威）参与 8 篇，Jørgensen（5 篇）和 Sjøberg（3 篇）。仅 4 篇有北美作者。（机构分布 finding）
4. **RQ4.1 (Topic coverage)**：主题有限，主流 SE 主题覆盖不足；建议更多 mapping studies。（gap finding）
5. **RQ4.2 (Primary study count)**：Research trends 63--1485 篇 primary studies；Technology evaluation 6--54 篇。（规模统计）
6. **RQ4.3 (Quality)**：所有研究 ≥1 分 DARE，仅 3 篇 <2 分。Quality 随年份提升（Spearman r=0.51, p<0.023），但与 guideline 引用无显著关系（F=0.37, p=0.55）。（统计 + 推断）
7. **RQ4.4 (Practice contribution)**：12 篇 technology evaluation 中仅 4 篇 offer advice to practitioners。需要改进。（缺口 finding）
8. **Roadmap**：明确 future plan——扩展为 broader automated search、2009 年末重复此研究。

## 3. 当前 `review.md` 维度树审计

### 3.1 总判断

当前 `review.md` 的维度树存在一个**核心结构性问题**：它自己明确声明 6 个 `leaf-*` 节点是"**跨论文通用接口层**，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原"。换言之，`review.md` 的维度树主干**首先是一个跨论文的通用模板，其次才尝试向本文原文靠拢**。这产生了以下后果：

- 主树中 6 个叶子无法直接对应到原文的 11 个 extraction fields、4 DARE QA 维度、3 层分类体系（type × scope × topic）、或 8 种 tabulation plan。
- 原文显式的数据抽取 schema 被迫降级为 4 个 `[leaf-*-orig-*]` 候选叶子并标注 `not_verified`，而**这些候选叶子才是原文的真正结构**。
- 原文丰富的 classification schema（SLR/MA × research trend/technology × topic area）被简化为一个泛化的"主题与维度分类"叶子，丢失了原文的多层分类结构。
- RQ→discussion→finding 的显式映射链在树中不够清晰。
- 原文的 8 种 tabulation plan（Section 2.6）作为统计操作化的精确指令，在树中没有得到对应节点。

### 3.2 逐项审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-kitchenham-2009-slr-tertiary-root]` = "Systematic literature reviews in software engineering – A systematic literature"，准确抓住了本文研究对象（对 SE SLR 的 SLR）。 | 通过 |
| 主干分支是否覆盖原文 schema | **I** | 5 个主干分支（b1 综述范围与 RQ、b2 语料收集与纳排、b3 主题/对象分类、b4 方法/技术/干预、b5 评价/统计与候选发现）采用了跨论文通用六类结构，但**未能直接对应原文的核心 schema**：原文的 extraction form 有 11 个字段，DARE QA1--QA4 是独立的 4 维质量评价 schema，而 8 种 tabulation plan 精确映射到各 RQ。当前分支中最明显的缺失是：(a) 原文的质量评价维度（QA1--QA4）是一项独立于 general "评价/统计"的主干结构——它本身就是对每篇被审 SLR 的编码操作，且带有显式评分标准（Y=1/P=0.5/N=0/Unknown）；(b) 原文单篇 SLR 级别的分类（type × scope × topic × guideline-reference × practitioner-guideline）是一个**多层分类系统**，不是单一的"主题/对象分类"分支可以覆盖的。 | I |
| 叶子维度是否足够具体 | **I** | 6 个通用叶子（scope、corpus、taxonomy、method、evidence、finding）过于抽象，无法捕捉原文**已经具备的高度操作化的字段级 schema**。例如原文 extraction form 明确列出"source/journal、study type (SLR/MA)、scope (research trends/technology)、main topic area、author/institution/country、summary+RQ+answers、RQ/issue、quality evaluation、referenced EBSE/guidelines、practitioner guidelines、#primary studies"共 11 个字段——每一个都是可直接抽取、可统计的操作化字段。当前叶子表没有为任何一个原文字段提供独立的叶子节点。`review.md` 自己承认叶子是"跨论文通用接口层"，这一声明本身说明它不完全忠于本文原文 schema。 | I |
| 取值空间是否可执行 | **I** | 原文的取值空间非常清晰且可执行：(a) study type = {SLR, MA}；(b) scope = {research trends, technology evaluation}；(c) QA1--QA4 每个 = {Y, P, N, Unknown} 且 Y=1/P=0.5/N=0；(d) topic area = {cost estimation, testing, experiments, ...}（由 data 驱动）；(e) referenced guideline = {yes, no}；(f) practitioner guideline = {yes, no}；(g) #primary studies = integer。这些已具备统计就绪性。当前 review.md 的叶子取值空间均为泛化的"自由文本 + RQ / 贡献声明引用"、"完整枚举 / 层级枚举 / 自由文本加理由"等——没有还原原文已有的精确取值空间。对于本文而言，原文取值空间已经非常明确，不需要等待 A2a 才定义。 | I |
| 关系边是否缺失 | **I** | 原文存在明显的跨字段关系：RQ→tabulation plan、extraction field→statistical use、quality dimension→quality score→trend analysis、study type × scope × topic 的交叉分类关系、guideline reference→quality score 的 ANOVA 检验关系。当前 review.md 的关系边表中缺少这些原文中已显式存在的交叉统计和因果分析关系。特别是 Section 2.6 的 8 项 tabulation 明确指定了"用什么数据回答哪个 RQ"，这是一种精确的数据→RQ 映射关系，在维度树中未得到体现。 | I |
| 统计用途 / 分母是否正确 | **M** | review.md 正确标注了本文作为候选主统计池和 schema seed 的身份，也说明了 A1-DT 阶段不进入 SUMMARY 定量统计。但统计用途列的表述（"可进入描述统计 / 交叉统计，前提是分母和样本单位明确"）对本文而言过于保守——原文已经有非常明确的统计分母（20 篇 SLR，检索源 2506 篇论文）、统计方法（频次、均值、Spearman 相关、ANOVA）和统计结果。这些不代表当前 A1-DT 就应该直接进入 SUMMARY 定量统计（跨论文统计还是需要 A2a 精确锚定），但至少在本文内部维度树的"统计用途"描述中应该如实反映原文已有的统计操作，而不是全标"前提是…"。 | M |
| 候选 finding 路径是否完整 | **M** | review.md 的"原文模式候选叶子映射"列出了 4 个候选叶子（tertiary-corpus、quality-criteria、topic-distribution、impact-limit），但遗漏了原文中同样重要的：(a) 机构/国家分布（RQ3 的核心证据，Table A3）；(b) primary study count 分布（RQ4.2）；(c) practitioner guideline 覆盖率（RQ4.4）；(d) 排除研究及其理由（Table A2，纳排透明性的核心证据）；(e) guideline reference 与质量的 ANOVA 关系（Section 3.3 / Table 5）。此外，原文 finding 形成路径中，RQ→discussion subsection→evidence table→finding 的显式链路在 review.md 的 finding 链路中被简化为"统计结果 / discussion / roadmap action 邻近段落"。 | M |
| A.1--A.4 证据链是否足够 | **M** | A.1 文件来源完整。A.2 证据账本只有 4 条证据（root、taxonomy、stat、risk），且 4 条全部标记为 `not_verified`——这虽然符合 pattern-field-schema.md 中 A1-DT 阶段的降级规则，但对于本文这种 extraction form 极为清晰的论文，应当至少有部分字段级证据可以标记为 `medium`（如 Section 2.5 的 11 字段列表在原文字面上已可精确定位）。A.3 结论-证据映射与 A.2 一致。A.4 只记录了一条 structure check + needs_manual_check，缺少逐字段 PDF 核对项的 checklist。 | M |
| 是否存在可能误导 A2a 的强主张 | **通过** | review.md 在多个位置明确声明"当前维度树是 schema seed，不是正式统计证据"、"A2a 完成前不得升级"、"叶子是通用接口层，不是原文叶子全集"——这些声明有效防止了读者将当前树误读为完成型复原。`pattern-field-schema.md` 的 §8.6 临时降级规则也被正确引用。在"不误导"这一点上，review.md 是诚实的，但诚实本身不能替代 faithful restoration。 | 通过 |

### 3.3 核心问题总结

当前 review.md 的维度树存在一个**"两层结构"问题**：

- **Layer 1（主干）**：6 个通用接口叶子（scope/corpus/taxonomy/method/evidence/finding）——这是跨论文的标准化检查框架，并非本文 faithful restoration。
- **Layer 2（候选叶子）**：4 个 `[leaf-*-orig-*]` 候选叶子（tertiary-corpus/quality-criteria/topic-distribution/impact-limit）——这才是向原文靠拢的尝试，但目前仅 4 个、全标 `not_verified`、取值空间笼统。

问题在于：**Layer 1 主导了"维度树"的名义结构，Layer 2 只是候选附录**。对于本文这样 extraction form、quality rubric、classification schema 和 tabulation plan 均**已在原文字面上显式列出**的论文，faithful restoration 应该反过来——原文字段应当占据维度树主干的叶子层，而通用接口层可以作为跨论文汇总时的归纳维度。当前结构容易让 A2a 执行者误认为"原文 schema 已通过 6 个通用叶子覆盖"，从而漏掉原文中已精确可操作的 11 个 extraction fields + 4 QA dimensions + 3-tier classification + 8 tabulation mappings。

## 4. 建议维度树骨架

以下维度树更忠实于 Kitchenham 2009 的原文结构。区分两个层级：

- **Level A**：忠实于原文"这个特定 tertiary study 做了什么"的操作化 schema。
- **Level B**：该 schema 如何归纳到跨论文通用维度（用于 A2a 归纳时与其它论文对齐）。

### Level A：忠实于原文的单论文维度树

```
[dim-kit-2009-root] Systematic literature reviews in SE – A tertiary study (Kitchenham et al., 2009)
│
├── [dim-kit-2009-b1] 研究设计（Study Design）
│   ├── [leaf-kit-2009-rq-structure] RQ 结构
│   │   取值空间：{RQ1 EBSE 活动规模, RQ2 研究主题, RQ3 研究领导者, RQ4 当前限制}
│   │   子问题：RQ4.1 主题覆盖, RQ4.2 primary study 数量, RQ4.3 SLR 质量, RQ4.4 实践贡献
│   │   可统计：是（描述性，N/A 于统计合成）
│   │   证据：Section 2.1
│   │
│   ├── [leaf-kit-2009-search-strategy] 检索策略
│   │   取值空间：{manual search, automated search}
│   │   来源池：10 journals + 4 conferences（Table 1 完整枚举）
│   │   时间窗：2004-01-01 至 2007-06-30
│   │   总检索引擎量：2506 篇论文（Table A1）
│   │   可统计：是（分母明确）
│   │   证据：Section 2.2, Table 1, Table A1
│   │
│   ├── [leaf-kit-2009-inclusion-criteria] 纳入标准
│   │   取值空间：{SLR with RQ+search+extraction, MA with RQ+search+extraction}
│   │   可统计：是
│   │   证据：Section 2.3
│   │
│   ├── [leaf-kit-2009-exclusion-reasons] 排除理由
│   │   取值空间：{informal literature survey, no RQ/search/extraction, discussion of EBSE procedure, duplicate}
│   │   排除列表：Table A2（14 篇排除论文 + 逐条理由）
│   │   可统计：是
│   │   证据：Section 2.3, Table A2
│   │
│   └── [leaf-kit-2009-protocol-deviation] Protocol 偏离
│       取值空间：{single extractor+checker vs double extraction, manual vs automated search, ...}
│       可统计：否（质性描述）
│       证据：Section 2.7
│
├── [dim-kit-2009-b2] 数据抽取表单（Extraction Form）
│   ├── [leaf-kit-2009-ext-source] 来源（journal/conference + full reference）
│   │   取值空间：属于 Table 1 的 venue 列表
│   │   可统计：是（频次）
│   │
│   ├── [leaf-kit-2009-ext-study-type] 研究类型
│   │   取值空间：{SLR, Meta-Analysis}
│   │   统计结果：19 SLR + 1 MA
│   │   可统计：是（频次）
│   │
│   ├── [leaf-kit-2009-ext-scope] 研究范围
│   │   取值空间：{Research trends, Specific technology evaluation question}
│   │   统计结果：8 research trends + 12 technology evaluation
│   │   可统计：是（频次、交叉）
│   │
│   ├── [leaf-kit-2009-ext-topic] 主主题
│   │   取值空间：{Cost estimation, Testing, Software engineering experiments, ...}（from data）
│   │   统计结果：7 cost estimation, 3 testing, 3 experiments
│   │   可统计：是（频次、分布）
│   │
│   ├── [leaf-kit-2009-ext-authors] 作者与机构
│   │   取值空间：自由文本 → 可归入 {institution, country}
│   │   统计结果：European-dominated (14/20), Simula Lab involved in 8
│   │   可统计：是（频次、机构/国家分布）— Table A3
│   │
│   ├── [leaf-kit-2009-ext-rq-answers] 研究问题与答案
│   │   取值空间：自由文本（结构化 RQ + answer）
│   │   可统计：否（质性综合）
│   │
│   ├── [leaf-kit-2009-ext-quality-score] 质量评价分数
│   │   取值空间：{Y=1, P=0.5, N=0, Unknown} × 4 QA questions → Total Score ∈ [0,4]
│   │   统计结果：mean 2.08--3.0 per year; Spearman r=0.51 (p<0.023)
│   │   可统计：是（均值、标准差、相关、ANOVA）— Table 3, 4, 5
│   │
│   ├── [leaf-kit-2009-ext-guideline-ref] 是否引用 SLR guideline
│   │   取值空间：{Yes, No}
│   │   统计结果：8/20 referenced guidelines
│   │   可统计：是（频次、交叉 Table 5）
│   │
│   ├── [leaf-kit-2009-ext-practitioner-guideline] 是否提供实践指南
│   │   取值空间：{Yes, No}
│   │   统计结果：4/12 technology evaluation SLRs offered advice
│   │   可统计：是（频次）
│   │
│   └── [leaf-kit-2009-ext-primary-study-count] Primary study 数量
│       取值空间：整数；Range: 6--54 (technology eval), 63--1485 (research trends)
│       可统计：是（描述性统计）
│
└── [dim-kit-2009-b3] 数据分析与发现形成（Analysis & Finding Formation）
    ├── [leaf-kit-2009-tabulation-plan] Tabulation 方案
    │   原文 Section 2.6 列出 8 种 tabulation，每种对应特定 RQ
    │   可统计：是（作为方法透明性指标）
    │
    ├── [leaf-kit-2009-finding-per-rq] 逐 RQ 发现
    │   取值空间：每个 RQ→discussion subsection→finding（可以结构化）
    │   示例：RQ1→"20 篇 SLR, 19 SLR+1 MA, 12 technology eval, 8 research trends"
    │   可统计：否（作为质性综合）
    │
    ├── [leaf-kit-2009-gap-finding] 缺口 / 建议
    │   取值空间：{topic coverage limited, more mapping studies needed, practice impact insufficient, ...}
    │   可统计：否
    │
    ├── [leaf-kit-2009-roadmap] 未来路线图
    │   取值空间：{extend with broader automated search, repeat end of 2009, investigate manual vs automated search reliability, ...}
    │   可统计：否
    │
    └── [leaf-kit-2009-validity-threats] 效度威胁
        取值空间：{manual search restriction, single selector, protocol deviations, terminology history, ...}
        可统计：否
        证据：Section 4.5
```

### Level B：跨论文归纳映射

以上 Level A 中的每个原文叶子可以映射到 A1-M0--M6 元维度：

| 原文叶子（A） | A1-M 元维度 |
|---|---|
| `[leaf-kit-2009-rq-structure]` | A1-M0 研究意图与综述元模型 |
| `[leaf-kit-2009-search-strategy]`, `[leaf-kit-2009-inclusion-criteria]`, `[leaf-kit-2009-exclusion-reasons]` | A1-M1 语料收集与纳排 |
| `[leaf-kit-2009-ext-topic]`, `[leaf-kit-2009-ext-scope]`, `[leaf-kit-2009-ext-study-type]` | A1-M2 研究对象与主题语义 |
| `[leaf-kit-2009-ext-source]`, `[leaf-kit-2009-ext-quality-score]`（方法侧） | A1-M3 方法 / 技术 / 干预 |
| `[leaf-kit-2009-ext-quality-score]`（结果侧）、`[leaf-kit-2009-ext-guideline-ref]`、`[leaf-kit-2009-ext-primary-study-count]` | A1-M4 评价、证据与复现资产 |
| `[leaf-kit-2009-tabulation-plan]`、所有可统计叶子 | A1-M5 统计分析就绪 |
| `[leaf-kit-2009-finding-per-rq]`, `[leaf-kit-2009-gap-finding]`, `[leaf-kit-2009-roadmap]` | A1-M6 research finding 形成与裁决 |

### 与当前 review.md 的关系

当前 review.md 的**诚实度和降级纪律值得肯定**（所有证据标记 `not_verified`、所有结论标记 `schema_seed`、明确声明"通用接口层不是原文叶子全集"），但其维度树结构不足以直接支撑 A2a 的精确字段锚定任务。建议在当前 review.md 中**增加一个"§原文 schema 直接复原"子节**，把上文 Level A 的树作为补充（而保留当前 6 叶子通用接口层作为 Level B 归纳辅助），并至少对 Section 2.5 的 11 个 extraction fields 和 Section 2.4 的 DARE QA1--QA4 coding scheme 提供原文逐字段引用。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补充原文 extraction form 的逐字段复原 | review.md §维度树复原，新增"原文 extraction form 直接复原"子节 | 列出 Section 2.5 的 11 个字段，每个字段标注：(a) 原文精确措辞，(b) 取值空间（含原文已报告的统计分布），(c) 在原文表格中的位置（Table 2 / Table 3 / Table A3），(d) 是否可统计（大部分是）。这 11 个字段应成为维度树的一部分，而非仅作候选叶子。 | `paper_content.txt`, Section 2.5 (Page 3) | I |
| 补充 DARE QA1--QA4 coding scheme | review.md §维度树复原，作为独立的质量评价子维度 | 列出 QA1--QA4 的完整 scoring rubric（Y=1/P=0.5/N=0/Unknown），标注：(a) 每个 QA 在 Table 3 中的列，(b) 每个 QA 的精确判定标准，(c) 统计口径（均值/Spearman/ANOVA）。原文 quality evaluation 不是一个笼统的"评价叶子"，而是 4 维独立编码 + 总分合成 + 统计推断的完整 schema。 | `paper_content.txt`, Section 2.4 (Page 3), Table 3 (Page 5) | I |
| 补充原文 classification 的多层结构 | review.md §维度树复原的叶子维度表 | 原文的分类不是单层"主题分类"，而是三层：study type (SLR/MA) → scope (trends/technology) → topic area (cost est./testing/experiments/...)。应在 taxonomy 叶子中明确这三层结构及每层的取值空间。 | `paper_content.txt`, Sections 2.3/2.5/3.1/4.2 | I |
| 补充 RQ→tabulation→finding 的显式映射 | review.md §统计与候选发现链路 | 原文 Section 2.6 的 8 种 tabulation 是"数据→RQ→finding"的最精确映射指令。当前 review.md 的统计链路过于抽象。建议增加一个"原文 data→RQ 映射表"，列出 8 种 tabulation × 对应的 RQ × 证据表 × 统计方法。 | `paper_content.txt`, Section 2.6 (Page 3) | I |
| 补充遗漏的候选叶子 | review.md "原文模式候选叶子映射"表 | 增加至少以下候选叶子：(a) 机构/国家分布（RQ3, Table A3），(b) primary study count 分布（RQ4.2），(c) 实践指南覆盖率（RQ4.4），(d) 排除研究清单（Table A2），(e) guideline ref × quality 的 ANOVA（Table 5）。 | `paper_content.txt`, Sections 3/4, Tables A2/A3, Table 5 | M |
| 升级已有明确原文定位的证据强度 | review.md A.2 证据账本 | EV-kitchenham-2009-slr-tertiary-002 目前覆盖太广（支撑所有 5 个分支 + 多个叶子）。建议拆分：至少为 Section 2.5 extraction form 和 Section 2.4 DARE QA 单独建证据行，并将字段级原文引用升级为 `medium`（因为 Section 2.5 字段列表在原文字面上已精确可定位，不需要 PDF 视觉核对即可确定存在性）。 | `paper_content.txt`, Section 2.4 & 2.5 | M |
| 补充 A.4 逐字段 PDF 核对清单 | review.md A.4 | 当前 A.4 只有一条 `needs_manual_check`。建议增加按 Table 3、Table 4、Table 5、Table A1、Table A2、Table A3 逐表核对的 checklist 条目，每项标注：核对对象（表号/QA 列/统计值）、通过条件、当前状态。 | `paper.pdf` + pattern-field-schema.md §8.4 | M |

## 6. C/I/M 结论

### 6.1 C（Critical）— 直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

无。当前 review.md 的诚实度和降级纪律使本文维度树不会直接破坏证据链——所有证据标记 `not_verified`，所有结论标记 `schema_seed`，明确声明了"通用接口层不是原文叶子全集"。A2a 执行者如果阅读了这些声明，就不会将当前树误用为可统计证据。**没有发现 C 级问题。**

### 6.2 I（Important）— 会实质影响维度树可用性、原文 schema 复原、证据可审计性

4 项 I 级问题：

1. **I-1：维度树主干未覆盖原文 schema**（§3.2 第 2 行）：5 个跨论文通用分支无法直接对应原文的 extraction form（11 字段）、DARE QA schema（4 维）、多层 classification（type × scope × topic）、和 8 种 tabulation plan。对 A2a 执行者的直接影响：当 A2a 需要"按原文 extraction form 逐字段锚定证据"时，当前维度树无法提供字段级导航。

2. **I-2：叶子维度过于抽象，未还原原文已有操作化字段**（§3.2 第 3 行）：6 个通用叶子的取值空间描述过于泛化，而原文的 11 个 extraction fields、DARE QA1--QA4 的 Y/P/N/Unknown coding rule、和 type × scope × topic 的分类枚举已经在原文字面上高度操作化。当前叶子不能指导 A2a 执行者"该抽哪些字段、取值空间是什么"。

3. **I-3：取值空间未还原原文已有精确枚举**（§3.2 第 4 行）：原文 study type ∈ {SLR, MA}、scope ∈ {research trends, technology evaluation}、QA ∈ {Y, P, N, Unknown}、topic ∈ {cost estimation, testing, experiments} 等精确枚举在 review.md 中全部丢失，被替换为"自由文本"、"完整枚举/层级枚举/自由文本加理由"等泛化表述。

4. **I-4：原文的 RQ→tabulation→finding 映射关系和交叉统计关系缺失**（§3.2 第 5 行）：Section 2.6 的 8 种 tabulation 精确映射是原文"方法透明性"的核心资产，也是 Paper2 期望从 survey-of-surveys 中抽取的"综述方法学模式"的核心内容——这一关系边在维度树中完全缺失，对 A2a 的方法学模式抽取构成实质损失。

### 6.3 M（Moderate）— 不阻塞的清晰度或维护性建议

4 项 M 级问题：

1. **M-1：统计用途描述对本文过于保守**（§3.2 第 6 行）：原文已有非常精确的统计操作（均值/Spearman/ANOVA），但在单篇维度树的"统计用途"列中应如实反映这一既成事实。
2. **M-2：候选叶子覆盖不全**（§3.2 第 7 行）：遗漏了 RQ3 机构分布、RQ4.2 primary study count、RQ4.4 practitioner guideline、Table A2 排除清单、Table 5 ANOVA 关系等原文显著的数据维度。
3. **M-3：A.2 证据账本粒度不足**（§3.2 第 8 行）：4 条证据覆盖整个论文，导致每条证据的"原文页码/章节/段落"定位过于宽泛，且字段级的明确原文引用被标记为 `not_verified`。
4. **M-4：A.4 缺少逐表 PDF 核对清单**（§3.2 第 8 行）：需要按 Table 3/4/5/A1/A2/A3 分解的人工核对条目。

### 6.4 最终建议

**NEEDS FIX**（需要修正后可达 READY）。

理由：虽然不存在 C 级风险（review.md 的诚实声明保护了证据链不被误用），但 4 项 I 级问题意味着当前维度树无法有效支撑 A2a 的"按原文 extraction form 逐字段锚定证据"任务。修正不要求重写整个 review.md——可以通过以下最小修复方案解决 I 级问题：

1. 在 §维度树复原中增加一个"原文 schema 直接复原"子节，列出原文 extraction form 的 11 字段 + DARE QA1--QA4 + 三层 classification，每个字段标注原文精确措辞、取值空间和证据定位。
2. 在该子节中增加"R→tabulation→finding 映射表"，列出 Section 2.6 的 8 种 tabulation 与对应 RQ/evidence table/统计方法的映射。
3. 在 A.2 证据账本中为 Section 2.4 DARE QA 和 Section 2.5 extraction form 分别建立独立证据行，证据强度可标注为 `medium`（因为字段列表在原文字面上已精确可定位）。

修正后建议的最终状态：READY。

---

*审计日期：2026-06-29*
*审计范围：单篇 kitchenham-2009-slr-tertiary，全文文本级审计，未进行 PDF 视觉核对*
*审计标准：`survey_of_surveys/GUIDE.md` + `patterns/pattern-field-schema.md` + `paper_story.md` + reviewer mode references*
