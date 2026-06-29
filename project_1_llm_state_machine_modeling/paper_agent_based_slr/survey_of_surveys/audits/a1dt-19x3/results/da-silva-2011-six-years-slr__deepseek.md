# da-silva-2011-six-years-slr · deepseek 全文审计报告

## 1. 审计身份与输入

| 项目 | 内容 |
|---|---|
| reviewer 身份 | deepseek |
| 审计日期 | 2026-06-29 |
| 审计目标 | 判断 `review.md` 中维度树复原是否完整、准确、可追溯；尤其检查树是否过小、是否把通用 6 个 leaf 接口误当成原文 schema、是否遗漏原文 RQ / extraction form / taxonomy / coding scheme / roadmap figure / evidence table / finding path / quality / validity / artifact 字段 |
| 是否读取 `$ai-research-writing-skill` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` |
| 是否读取 `paper-story.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md` |
| 是否读取 `reviewer-guidelines.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` |
| 是否读取 `reviewer-self-review.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` |
| 是否读取 `$research-planning` | 是；路径 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 和 `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` |
| 是否读取 `$oh-my-codex:autoresearch` | 是；路径 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` |
| 是否完整阅读 `paper_content.txt` | 是；已从头至尾阅读全部 1625 行，覆盖：Abstract、§1 Introduction、§2 Previous studies（OS 2009, FE 2010）、§3 Method（§3.1 RQs、§3.2 Research team、§3.3 Decision procedure、§3.4 Search process、§3.5 Study selection、§3.6 Quality assessment + DARE criteria QA1--QA4、§3.7 Data extraction process + 10 字段抽取表）、§4 Data extraction results（Table 2 全部 67 篇 SLR 汇总、Figure 2 PRISMA-style 流程图、Table 3 质量分 quartile 表）、§5 Discussion of RQs（§5.1 RQ1 数量增长趋势 Table 4、§5.2 RQ2 主题覆盖 + Table 5 SE Curriculum/SWEBOK 教育/实践映射 + Table 6 SWEBOK 分布、§5.3 RQ3 作者/机构/国家分布 Table 7--8、§5.4 RQ4 与前序研究对比：§5.4.1 主题与证据范围、§5.4.2 面向实践、§5.4.3 质量评价 Table 9--11、§5.4.4 指南使用 Table 12、§5.5 RQ5 质量趋势 Table 13）、§6 Limitations、§7 Conclusions、Appendix A 全部 67 篇参考文献 |
| 是否核对 `paper.pdf` | 否；无法在当前环境下进行视觉 PDF 页面核对。复杂表图（Table 2 完整 67 行、Table 3 quartile 分表、Table 5 SWEBOK 映射的完整版本、Figure 2 PRISMA 流程图）的版面细节、页码精确定位和列偏移仍需人工 PDF 核对。本报告基于 `paper_content.txt` 的全文文本级证据，所有来自表图的精确数值均标注"文本提取级；待 PDF 版面核对" |
| 是否读取文库级规则 | 是；已读 `README.md`、`GUIDE.md`、`SUMMARY.md`、`pattern-field-schema.md`、`paper_story.md` |
| 是否读取 BibTeX / metadata | 是；已读 `bibtex.bib`、`metadata.json` |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文是一篇发表在 Information and Software Technology（IST，CCF-B）上的 **updated tertiary study**，整合并扩展了 Kitchenham et al. 之前的两项 tertiary study（OS 2009, FE 2010），将时间窗口从 2004-01-01 至 2008-06-30 扩展至 2004-01-01 至 2009-12-31。

**目标声明**（Abstract）：扩展和更新两项已有 tertiary study，覆盖 2008-07-01 至 2009-12-31 的时间段，分析已发表 SE SLR 的质量、主题覆盖和潜在的教育/实践影响。

**贡献声明**（Abstract + §7 Conclusions）：
1. 发现 67 篇新 SLR，覆盖 24 个 SE 主题
2. SE SLR 数量在增长、质量在改善、研究者群体在扩大和全球化
3. 然而大多数 SLR 仍未评价 primary study 的质量，且缺乏面向实践者的指南

**五个显式 RQ**（§3.1，等价于 FE 的 RQ）：

| RQ | 原文表述 | 对应结果节 |
|---|---|---|
| RQ1 | How many SLRs were published between 1st January 2004 and 31st December 2009? | §5.1 |
| RQ2 | What research topics are being addressed? | §5.2 |
| RQ3 | Which individuals and organisations are most active in SLR-based research? | §5.3 |
| RQ4 | Are the limitations of SLRs, as observed in the two previous studies, FE and OS, still an issue? | §5.4（含 4 个子节） |
| RQ5 | Is the quality of the SLRs improving?（等价于 FE 的 RQ4） | §5.5 |

**特点**：原文 RQ 是从 FE 直接继承而非重新设计，但将 FE 的原 RQ4（limitations）拆分为现在的 RQ4，原 RQ3（quality）重新编号为 RQ5。RQ 的"更新"性质体现在每个 RQ 下均包含 OS/FE 数据与 SE 新数据的对比和合并。

### 2.2 原文方法流程

完整流程见 Figure 2（PRISMA-style flow diagram）：

1. **Automated Search**：在 ACM、IEEEXplore、CiteSeerX、ScienceDirect、ISI、Scopus 六库执行自动检索 → 1389 条结果
2. **First Filter**：读 title/abstract 排除明显无关 → 157 篇
3. **Manual Search**：对 Table 1 所列 20+ 本 SE 期刊/会议逐卷/逐期手工检索 → 166 篇
4. **Merge + Remove Duplicates**：合并自动和手工结果，去重 69 篇 → 154 篇
5. **Selection**：对全文应用 inclusion/exclusion criteria → 排除 79 篇 → 75 篇
6. **Reference Search**：对 75 篇做 backward reference search → 新增 2 篇 → 77 篇
7. **Final Exclusion**：Quality Assessment + Data Extraction 后排除 10 篇（4 非 SE、3 为已有 FE study 的报告、1 超出时间范围、1 为重复发表、1 质量分为 0） → **最终包含 67 篇**

检索起点为 2004-01-01，终点为 2009-12-31。

### 2.3 原文显式 extraction form — 这是最关键的部分

原文 §3.7 显式定义了 **10 个数据抽取字段**：

| # | 字段 | 取值空间 | 用于回答的 RQ |
|---|---|---|---|
| 1 | Year of publication | 2004--2009 | RQ1 |
| 2 | Quality Score | 0--4（4 个 DARE QA 问题各得 0/0.5/1 分） | RQ4, RQ5 |
| 3 | Review Type | SLR / MA / MS（mapping study） | RQ2, RQ4 |
| 4 | Review Scope | RQ（detailed technical question）/ SERT（SE trends）/ RT（research methods in SE） | RQ2 |
| 5 | Topic Area | 24 个 SE 主题（Requirements Engineering, Distributed Software Development, Software Product Line, Software Testing, Empirical Research Methods 等） | RQ2 |
| 6 | Cited EBSE papers | Y/N（是否引用 [14,8,20]） | RQ1, RQ4 |
| 7 | Cited Guidelines | Y/N（是否引用 [15,16]） | RQ1, RQ4 |
| 8 | Number of Primary Studies | 整数（如 36, 68, 97, 237...） | RQ4 |
| 9 | Included Practitioners Guidelines | Y/N（论文是否有可识别的实践指南 section/table 等） | RQ2, RQ4 |
| 10 | Source Type | J（Journal）/ C（Conference）/ WS（Workshop）/ BS（Book Series） | RQ2 |

**这 10 个字段是原文最明确、可直接操作的 schema**，而非任何抽象 meta-dimension。它们构成了 Table 2（67 行 × 10+ 列主数据表）的基础。

### 2.4 原文显式 quality rubric — DARE 标准

原文 §3.6 完整定义四问 DARE 质量评价标准：

| 编号 | 问题 | 评分规则 |
|---|---|---|
| QA1 | Are the review's inclusion and exclusion criteria described? | Y（显式定义）=1, P（隐式）=0.5, N（未定义）=0 |
| QA2 | Is the literature search likely to have covered all relevant studies? | Y（≥4 个数字图书馆 + 补充策略）=1, P=0.5, N=0 |
| QA3 | Did the reviewers assess the quality/validity of the included studies? | Y（显式定义质量准则并用于评估）=1, P（质量问题是 RQ 的一部分且被讨论）=0.5, N（无）=0 |
| QA4 | Were the basic data/studies adequately described? | Y（每篇 primary study 可追溯）=1, P（仅分组汇总）=0.5, N（未引用 individual study）=0 |

最终 Quality Score = QA1 + QA2 + QA3 + QA4，范围 0--4。Table 3 将所有 67 篇按总分分成四个 quartile。

### 2.5 原文显式 classification schema / taxonomy

原文有两套相互交叉的分类体系：

**A. Review Type × Review Scope**（每个 SLR 同时属于一个 type 和一个 scope）：
- Review Type: SLR / MA / MS
- Review Scope: RQ / SERT / RT

**B. Topic Area**（原文 Table 2 + §5.2）：
- 原文列出 24 个不同 SE topic areas
- 最频繁的 6 个：Requirements Engineering (8), Distributed Software Development (8), Software Product Line (7), Software Testing (6), Empirical Research Methods (5), Agile Software Development (4) + Software Maintenance and Evaluation (4)
- 与 OS/FE 相比新增 14 个 topic

**C. Education/Practice Impact Classification**（原文 Table 5）：
- 每个 SLR 被评为 "Useful for education"（Yes/Possibly/No）和 "Useful for practitioner"（Yes/Possibly/No）
- 每条评估附带 "Why?" 理由（例如"aimed at practitioners rather than undergraduates"）
- 同时映射到 SE Curriculum 和 SWEBOK section
- 原文 Table 6 汇总了 SWEBOK 章节分布

**D. Source Type**：J / C / WS / BS（四类，已在 extraction form 中）

### 2.6 原文 evidence tables 与图形

| 编号 | 内容 | 类型 |
|---|---|---|
| Figure 2 | Identification of included SLRs（PRISMA-style 筛选流程图） | 流程/路线图 |
| Table 2 | 67 篇 SLR 完整数据摘要（10 字段 × 67 行） | 主数据表 |
| Table 3 | Quality scores for each assessment question（67 行 × QA1--QA4 + Final Score + Quartile） | 质量评价表 |
| Table 4 | Number of SLRs per year（2004--2009；OS/FE vs SE vs Total；EBSE positioned vs not） | 趋势表 |
| Table 5 | Relationships between SLRs and SE undergraduate Curriculum and SWEBOK（逐篇列出 usefulness for education/practitioner + Why + SE Curriculum + SWEBOK mapping） | 教育/实践影响映射表 |
| Table 6 | Distribution of SLRs over 2004 SE Curriculum and SWEBOK sections（OS/FE vs SE vs Total） | 覆盖度表 |
| Table 7 | Researchers that co-authored three or more SLRs（21 位研究者名单） | 研究者活跃度表 |
| Table 8 | Countries contributing to SLRs | 国家分布表 |
| Table 9 | Evolution of the types of research questions（OS/FE vs SE vs Total；Exploration/Description/Explanation） | 对比趋势表 |
| Table 10 | Evolution of review scope vs review type（OS/FE vs SE vs Total） | 对比趋势表 |
| Table 11 | Evolution of quality evaluation of primary studies（Yes/No；OS/FE vs SE vs Total） | 对比趋势表 |
| Table 12 | Use of guidelines（OS/FE vs SE vs Total；cited EBSE/Cited Guidelines） | 对比趋势表 |
| Table 13 | Distribution of quality scores per year（Quality Score 每年 min/mean/max/std dev） | 质量趋势表 |
| Appendix A | List of 67 SLRs（完整参考文献列表，含 study ref ID、citation、review type） | 语料清单 |

### 2.7 原文 finding 形成路径

原文的 finding 形成遵循"逐 RQ 统计 → 与 OS/FE 对比 → 解释 → 综合结论"的模式：

1. **RQ1（数量）**：统计 67 新 + 53 旧 = 120 总 → 发现数量增长（2009 年占 43%） → EBSE 定位率从早期 17% 升至 80%
2. **RQ2（主题）**：对 67 篇按 Topic Area 分类计数 → 发现 24 个 topic → 新增 14 个 → 但仍有 6 个 topic 占 55% → 教育/实践相关性逐篇评估 → 15 篇对教育有用、40 篇对实践有用、26 篇主要面向研究者 → SWEBOK 覆盖仅 33%（15/46 sections）
3. **RQ3（研究者）**：统计作者/机构/国家频次 → 发现 159 位研究者（较 OS/FE 增 50%） → 90 个机构 → 25 个国家 → 欧洲主导但亚洲开始出现
4. **RQ4（limitations）**：分四个子维度与 OS/FE 对比 → 主题集中度降低但仍有 55% 集中于 6 个 topic → 大多数面向研究者而非实践者 → 仅 21% 评价了 primary study 质量 → 指南使用增加但与质量无显著统计相关
5. **RQ5（质量）**：质量分逐年趋势 → 均值从 2004 的 2.38 升至 2009 的 2.90（12.5% 提升） → 但 QA3/Q4 仍是薄弱环节 → 质量与 primary study 数量负相关（r=−0.204, p=0.05）

**最终结论形成**（§7）：三条正面变化 + 三条 persistent limitations → 正面与负面形成平衡判断。

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树结构概述

当前 `review.md` 的维度树包含：
- **根节点**：`[dim-da-silva-2011-six-years-slr-root]`
- **6 个 pattern 分支**（RP/DP/FP/EP/VP/SP）：对应 RQ pattern、dimension pattern、finding pattern、evidence presentation pattern、validity threat pattern、report structure pattern 六类通用模式抽取
- **约 7 个叶子维度**（A1DT C01--C07）：`leaf-scope`、`leaf-corpus`、`leaf-taxonomy`、`leaf-method`、`leaf-evidence`、`leaf-finding`、`leaf-transfer`
- **C12 候选叶子映射**：`leaf-orig-secondary-study-profile`、`leaf-orig-quality-assessment`、`leaf-orig-topic-taxonomy`、`leaf-orig-practice-impact`
- **2 条关系边**：`method→evidence`（支撑/度量）、`taxonomy→finding`（导出候选发现）

### 3.2 逐项审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | **命名准确但语义信息不足** | 根节点标识为 `[dim-da-silva-2011-six-years-slr-root]`，定位正确。但标识只含 slug，未体现"updated tertiary study + 扩展 time window + 整合两项前序研究"的核心性质。根节点描述中缺少原文三个核心动作词：extend、update、integrate。不影响功能但降低可读性。 | M |
| 主干分支是否覆盖原文 schema | **严重不足——当前树用 6 个通用 pattern 分支替代原文真实 schema** | 原文有多层显式 schema：① 10 个数据抽取字段（§3.7）是原文最直接的操作化 schema；② 4 个 DARE 质量评价问题（QA1--QA4）；③ Review Type × Review Scope 分类；④ 教育/实践影响三级分类 + SWEBOK 映射；⑤ 与前序研究对比的 4 个子维度（topic extent、practice orientation、quality evaluation、guidelines usage）。当前维度树的主干分支按 pattern-field-schema.md 的 6 类通用接口组织（RQ/dimension/finding/evidence/validity/report structure），这是 **综述之综述的脚手架元分类**，不是 **本篇论文自身的 schema**。它混淆了"我们如何分类这篇论文的模式贡献"和"这篇论文用了什么 schema"。6 个 pattern 分支下挂的 7 个 leaf 本质上是对原文进行了一次 meta-reflection（"这篇论文有 RQ 模式、有 dimension 模式、有 finding 模式……"），但这不是对原文抽取字段和分类体系的复原。C12 中确实列出了 4 个候选原文叶子（`leaf-orig-*`），但这些候选叶子并未作为主树干的分支展开——它们只是被声明为"A2a 精核入口"，却未融入当前维度树的主结构。读者无法从当前树中看到：① 原文有 10 个抽取字段、② 原文有 4 个 DARE 评估问题、③ 原文的分类编码体系是 Review Type × Review Scope × Topic Area、④ 原文有教育/实践影响映射逻辑。这导致 A2a 若仅依赖当前维度树，将完全丢失原文的操作化 schema 结构。 | C |
| 叶子维度是否足够具体 | **不足——7 个叶子是通用接口，不是论文特化叶子** | `leaf-scope` 的实际内容是"研究范围与 context 锚定"，对应 pattern-field-schema.md 的通用定义。论文实际的 scope 信息（time window 2004-01-01 至 2009-12-31、搜索六库+手工 20+ 源、纳排后 67 篇）被压缩进一个抽象槽位。`leaf-taxonomy` 的实际内容是"主题与维度分类"，原文的三种分类体系（Review Type、Review Scope、Topic Area 24 类）被压缩为一个通用标签。`leaf-method` 实际内容是"方法/技术/干预分类"，但原文是 tertiary study，其"方法"是 SLR/SMS 本身的方法学——当前 leaf 没有区分原文自身方法和原文分析对象（primary SLR）的方法。`leaf-finding` 将原文 5 个 RQ 下的 15+ 条具体 finding（§5.1--§5.5 各子节 + §7 Conclusions 三正三负）压缩为一个通用槽位，每个 finding 的独立可追溯性丢失。`leaf-corpus` 的实际内容是"语料与纳排链条"，但原文有 Figure 2 的 PRISMA 流程图 + Table 2 的 67 篇完整语料清单，当前都没有作为该 leaf 的子维度展开。 | I |
| 取值空间是否可执行 | **部分可执行，但对原文特化 schema 无效** | 7 个通用 leaf 的取值空间为"自由文本 + 受控标签"或"完整枚举 / 层级枚举 / 自由文本"——这对 A1-DT 的 schema seed 阶段是可接受的。但问题在于：这些取值空间是对 pattern-field-schema.md 合同的重述，而非对原文字段取值的枚举。例如原文 Review Type 可取 `{SLR, MA, MS}`，这是一个简单、可统计的三值枚举——但当前维度树中没有任何 leaf 显式记录这个取值空间。原文 24 个 Topic Area 的完整列表在 §5.2 明确给出——但 `leaf-taxonomy` 没有收录。如果 A2a 仅依赖当前维度树做字段抽取，它必须回到 `paper_content.txt` 逐字段查找取值空间，维度树本身没有提供可直接操作的枚举。 | I |
| 关系边是否缺失 | **严重缺失** | 当前仅定义两条关系边：`method→evidence` 和 `taxonomy→finding`。原文至少有如下关键关系未被捕获：① **Time → OS/FE → SE comparison**：原文的核心贡献是"更新"，每个 RQ 下都有 OS/FE vs SE vs OS/FE+SE 的三栏对比，这是一条跨时域的比较关系边。② **Extraction Fields → RQs**：10 个抽取字段与 5 个 RQ 之间的映射（例如 Quality Score 服务于 RQ4 和 RQ5，Topic Area 服务于 RQ2）——这是原文 schema 的骨架关系。③ **Quality Assessment → Data Extraction**：质量评价结果用于排除低质量论文，即 QA score 影响哪些条目进入最终统计。④ **Topic Area → Education/Practice Impact**：原文 Table 5 显式将每个 topic 的每条 SLR 映射到教育和实践有用性。⑤ **Search/Selection → Final Corpus**：Figure 2 的流程关系，从 1389 到 67 的每一步纳排都有明确分母。这些关系边的缺失意味着 A2a 无法从维度树中获知原文的数据流和比较逻辑。 | I |
| 统计用途 / 分母是否正确 | **正确但过于保守，且未定位到原文** | 当前所有 leaf 的统计用途标注为"不进入主统计池（仅作 schema seed）"——这符合 A1-DT 的降级纪律。但"可统计方式"列中，`leaf-taxonomy` 写为"分类项频次/交叉表/主题分布"，而原文的实际统计方式（例如 Table 6 SWEBOK 分布统计、Table 10 Review Scope × Review Type 交叉统计、Table 12 指南使用与质量的相关性检验）并未显式链接到原文表号。分母信息（67 篇新 SLR / 120 篇总计 / 1455 篇初始检索）也未在维度树中显式记录。 | M |
| 候选 finding 路径是否完整 | **不完整——原文 15+ 条具体 finding 被压缩为 1 个通用槽位** | 原文通过 5 个 RQ 形成了 5 条 finding 路径，每条路径下有 2--5 条具体的 finding 陈述。例如 §5.4 下有 4 个子节各产生独立 finding（topic concentration 降低但仍存在、most SLRs researcher-oriented、仅 21% 评价 primary study 质量、指南使用增加但与质量无显著相关）。当前 `leaf-finding` 将这些压缩为一个通用节点，A2a 无法从中获知每条 finding 对应的统计证据和对比维度。C09 虽然标注了"本文可为候选发现提供启发"，但未逐条 listing 原文 finding 及其支撑 RQ 和表格。 | I |
| A.1--A.4 证据链是否足够 | **结构合规，但证据强度普遍为 not_verified，且缺少原文 schema 的直接证据锚点** | A.1 来源标识完整（bibtex、paper_content.txt、paper.pdf、metadata.json、review.md）。A.2 证据账本有 6 条证据（EV-001 至 EV-006），但所有证据均为 `weak` 强度且标注为"待 A2a 精确页码复核"。这符合 pattern-field-schema.md 的降级规则，但问题是：当前 6 条证据主要锚定在 pattern 层面的抽象结构（"原文有 RQ 模式""原文有 dimension 模式"），而不是锚定在原文的具体字段和分类上（"原文 §3.7 定义 10 个抽取字段""原文 §3.6 定义 4 个 DARE 问题""原文 Table 2 有 67 行 10 列"）。A.3 结论-证据映射有 14 条结论（C00--C13），但 C03--C07 这 5 个 leaf_definition 结论的支撑证据都是 EV-002/EV-003 的泛定位引用（"原文的 RQ/方法/分类/评价/讨论结构"），这不是字段级的证据锚点。A.4 复验清单有 2 项，其中 `needs_manual_check` 的视觉核对项覆盖了 EV-002/EV-003，但具体应核对的表格/图编号和页码未在 A.4 中逐项列出。最关键的是：**没有任何一条 A.2 证据直接锚定到原文 §3.7 的 10 个 extraction fields、§3.6 的 4 个 DARE QA 问题、或 Table 5 的教育/实践影响映射**——这三者是原文最核心的 schema 元素，但证据链中完全没有出现过。 | I |
| 是否存在可能误导 A2a 的强主张 | **存在但已有部分缓解** | C12（source schema candidates）和 C08（migration boundary）的声明明确区分了"候选叶子"和"已核验 schema"，且 C09 明确标注"单篇 discussion 不能直接升级为最终发现"。这是防御性声明，部分缓解了风险。但仍存在以下潜在误导：① 6 个通用 pattern 分支被命名后，没有显式声明"这是脚手架元分类，不是原文 schema"，A2a reader 可能误以为这就是原文的维度结构。② C03--C07 命名使用了 `leaf-corpus`、`leaf-taxonomy` 这类自然语言标签，暗示它们就是原文的叶子维度。③ 原文最核心的 10 字段 extraction form 只在 C12 中以 `leaf-orig-secondary-study-profile` 的模糊标签出现，没有标出具体 10 字段名。如果 A2a 基于当前维度树执行字段抽取，会产生系统性偏差：它用的字段是脚手架元维度（corpus/taxonomy/method/evidence/finding），而不是原文的实际字段（Year/Quality Score/Review Type/Review Scope/Topic Area/Cited EBSE/Cited Guidelines/Number of Primary Studies/Practitioners Guidelines/Source Type）。 | I |

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树。该树遵循两个原则：
1. **以原文 RQ 为主干**——因为原文的 findings 和统计均按 RQ 组织
2. **以原文 10 字段 extraction form + 4 条 DARE QA + 教育/实践映射为叶子**——尽可能使用原文术语

### 4.1 建议树结构

```text
[dim-root] Six years of SLRs in SE: updated tertiary study extending OS(2009)+FE(2010) to cover 2004--2009
│
├── [dim-protocol] 研究协议与方法
│   ├── [dim-protocol-search] 检索策略
│   │   ├── [leaf-search-automated] 自动检索源 → 取值: {ACM, IEEEXplore, CiteSeerX, ScienceDirect, ISI, Scopus} (6个); 证据: §3.4, Fig.2
│   │   ├── [leaf-search-manual] 手工检索源 → 取值: Table 1 中的 20+ 期刊/会议名; 证据: §3.4, Table 1
│   │   └── [leaf-search-reference] 后向引用检索 → 取值: Y/N/不适用; 证据: §3.5
│   ├── [dim-protocol-selection] 纳排
│   │   ├── [leaf-inclusion-criteria] 纳入标准 → 取值: 自由文本(原文定义); 证据: §3.5
│   │   ├── [leaf-exclusion-criteria] 排除标准 → 取值: 自由文本(原文定义); 证据: §3.5
│   │   └── [leaf-screening-flow] 筛选流程 → 取值: 分母{1389→157→154→75→77→67}; 证据: Fig.2
│   ├── [dim-protocol-quality] 质量评价
│   │   ├── [leaf-qa1] QA1: 纳排标准是否描述 → 取值: {Y(1), P(0.5), N(0)}; 证据: §3.6, Table 3
│   │   ├── [leaf-qa2] QA2: 文献检索是否充分 → 取值: {Y(1), P(0.5), N(0)}; 证据: §3.6, Table 3
│   │   ├── [leaf-qa3] QA3: primary study 质量是否评价 → 取值: {Y(1), P(0.5), N(0)}; 证据: §3.6, Table 3
│   │   ├── [leaf-qa4] QA4: primary study 数据是否充分描述 → 取值: {Y(1), P(0.5), N(0)}; 证据: §3.6, Table 3
│   │   └── [leaf-quality-total] 质量总分 → 取值: 0--4; 可统计: 均值/趋势/quartile; 证据: Table 3
│   └── [dim-protocol-extraction] 数据抽取
│       ├── [leaf-ext-year] 发表年份 → 取值: {2004,2005,...,2009}; 可统计: 频次/趋势; 证据: §3.7, Table 2, Table 4
│       ├── [leaf-ext-quality-score] 质量分 → 同上 [leaf-quality-total]; 证据: §3.7, Table 2, Table 3
│       ├── [leaf-ext-review-type] Review Type → 取值: {SLR, MA, MS}; 可统计: 频次/交叉表; 证据: §3.7, Table 2, Table 10
│       ├── [leaf-ext-review-scope] Review Scope → 取值: {RQ, SERT, RT}; 可统计: 频次/交叉表; 证据: §3.7, Table 2, Table 10
│       ├── [leaf-ext-topic-area] Topic Area → 取值: 24 个 SE 主题(开放列表,原文 §5.2 枚举); 可统计: 频次/分布; 证据: §3.7, Table 2, §5.2
│       ├── [leaf-ext-cited-ebse] Cited EBSE papers → 取值: {Y, N}; 可统计: 频次/%; 证据: §3.7, Table 2, Table 4
│       ├── [leaf-ext-cited-guidelines] Cited Guidelines → 取值: {Y, N}; 可统计: 频次/%; 证据: §3.7, Table 2, Table 12
│       ├── [leaf-ext-num-primary] Number of Primary Studies → 取值: 正整数; 可统计: 均值/范围/与质量相关; 证据: §3.7, Table 2
│       ├── [leaf-ext-practitioner-guidelines] Included Practitioners Guidelines → 取值: {Y, N}; 可统计: 频次/%; 证据: §3.7, Table 2
│       └── [leaf-ext-source-type] Source Type → 取值: {J, C, WS, BS}; 可统计: 频次/分布; 证据: §3.7, Table 2
│
├── [dim-rq1] RQ1: 数量和增长（→ §5.1）
│   ├── [leaf-rq1-count-by-year] 每年 SLR 数量 → 取值: 频次(整数); 可统计: 趋势; 证据: Table 4
│   ├── [leaf-rq1-ebse-positioned] EBSE 定位比例 → 取值: {每年 Y/N 计数, %}; 可统计: 趋势; 证据: Table 4
│   └── [leaf-rq1-os-fe-comparison] 与 OS/FE 的数量对比 → 取值: {53(OS/FE,4.5年), 67(SE,1.5年), 120(总计)}; 统计: 对比增长率; 证据: Table 4
│
├── [dim-rq2] RQ2: 主题覆盖、教育和实践影响（→ §5.2）
│   ├── [leaf-rq2-topic-distribution] 各 topic 的 SLR 频次 → 取值: 24 个 topic × 频次; 可统计: 分布/集中度; 证据: §5.2, Table 2
│   ├── [leaf-rq2-new-topics] 与 OS/FE 相比新增 topic → 取值: 14 个新增 topic 名; 证据: §5.2
│   ├── [leaf-rq2-education-usefulness] 对教育的有用性 → 取值: {Yes, Possibly, No}; 可统计: 频次; 证据: Table 5
│   ├── [leaf-rq2-practitioner-usefulness] 对实践的有用性 → 取值: {Yes, Possibly, No}; 可统计: 频次; 证据: Table 5
│   ├── [leaf-rq2-usefulness-reason] 有用性理由 → 取值: 自由文本(逐篇); 证据: Table 5 "Why?" 列
│   ├── [leaf-rq2-se-curriculum] SE Curriculum 映射 → 取值: SE Curriculum section 名; 可统计: 覆盖频次; 证据: Table 5, Table 6
│   ├── [leaf-rq2-swebok] SWEBOK 映射 → 取值: SWEBOK chapter/section 名; 可统计: 覆盖频次; 证据: Table 5, Table 6
│   └── [leaf-rq2-swebok-coverage] SWEBOK 覆盖率 → 取值: {15/46 sections, 33%}; 证据: §7
│
├── [dim-rq3] RQ3: 研究者和机构分布（→ §5.3）
│   ├── [leaf-rq3-researcher-count] 研究者数量 → 取值: 整数(159, OS/FE vs SE); 可统计: 增长率; 证据: Table 7
│   ├── [leaf-rq3-multi-study-researchers] 多篇研究者 → 取值: 姓名列表 + 篇数; 证据: Table 7 (21 位 ≥3 篇)
│   ├── [leaf-rq3-org-count] 机构数量 → 取值: 整数(90, OS/FE+SE); 证据: §5.3
│   ├── [leaf-rq3-country-distribution] 国家分布 → 取值: 25 个国家 × 频次; 可统计: 分布; 证据: Table 8
│   └── [leaf-rq3-region-trend] 地区趋势 → 取值: 欧洲/北美/亚洲/南美/其他; 证据: §5.3
│
├── [dim-rq4] RQ4: 历史 limitations 是否仍存在（→ §5.4）
│   ├── [leaf-rq4-topic-concentration] 主题集中度 → 取值: {55% 集中于 6 个 topic}; 证据: §5.4.1
│   ├── [leaf-rq4-practice-orientation] 面向实践的程度 → 取值: {most researcher-oriented, 40/67 对实践有用}; 证据: §5.4.2, Table 5
│   ├── [leaf-rq4-quality-eval-rate] primary study 质量评价率 → 取值: {21% (14/67)}; 可统计: 与 OS/FE 对比; 证据: §5.4.3, Table 11
│   ├── [leaf-rq4-quality-eval-reasons] 不评价质量的原因 → 取值: {混淆质量评价与纳排标准/相信peer-review保证/primary study太少}; 证据: §5.4.3
│   ├── [leaf-rq4-guidelines-usage] 指南使用率 → 取值: Y/N %; 可统计: 与 OS/FE 对比; 证据: §5.4.4, Table 12
│   └── [leaf-rq4-guidelines-quality-correlation] 指南使用与质量相关性 → 取值: {not statistically significant for all 120 SLRs}; 证据: §5.4.4
│
├── [dim-rq5] RQ5: 质量趋势（→ §5.5）
│   ├── [leaf-rq5-mean-quality-by-year] 每年平均质量分 → 取值: 数值列表(2004:2.38→2009:2.90); 可统计: 趋势; 证据: Table 13
│   ├── [leaf-rq5-quality-improvement] 质量提升幅度 → 取值: {12.5% over 6 years}; 证据: §5.5
│   ├── [leaf-rq5-qa12-vs-qa34] QA1/QA2 vs QA3/QA4 表现差异 → 取值: {QA1/QA2 普遍较好, QA3/QA4 仍是瓶颈}; 证据: §5.5, Table 3
│   └── [leaf-rq5-quality-vs-num-primary] 质量与 primary study 数量的相关性 → 取值: {r=−0.204, p=0.05, N=120}; 可统计; 证据: §5.5
│
├── [dim-comparison] 跨时域对比框架
│   ├── [leaf-comp-os-data] OS (2009) 基准数据 → 取值: 各类统计值(53 SLRs); 证据: §2, 各对比表
│   ├── [leaf-comp-fe-data] FE (2010) 基准数据 → 取值: 各类统计值(扩展自 OS); 证据: §2, 各对比表
│   ├── [leaf-comp-se-data] SE (本论文) 新数据 → 取值: 各类统计值(67 SLRs); 证据: 各 RQ 节
│   └── [leaf-comp-merged-data] OS/FE+SE 合并数据 → 取值: 各类统计值(120 SLRs); 证据: 各 RQ 节
│
├── [dim-validity] 效度威胁与本研究的 limitation（→ §6）
│   ├── [leaf-validity-search-coverage] 检索覆盖度 → 取值: 自由文本; 证据: §6
│   ├── [leaf-validity-quality-subjectivity] 质量评价主观性 → 取值: {QA4 过于主观, QA2 不一致已解决}; 证据: §6
│   ├── [leaf-validity-extraction-difficulty] 数据抽取困难 → 取值: {多数 SLR 报告不充分, 信息需推断}; 证据: §6
│   └── [leaf-validity-multi-evaluator] 多评估者程序 → 取值: {至少 2 人评估, 冲突由第 3 人或共识解决}; 证据: §6
│
└── [dim-artifact] 制品与可复现性
    ├── [leaf-artifact-appendix] Appendix A 完整语料清单 → 取值: 67 篇 SLR 参考文献; 证据: Appendix A
    ├── [leaf-artifact-dcp] Data Collection Protocol (DCP) → 取值: {存在, 用于数据抽取和质量评价}; 证据: §3.7
    └── [leaf-artifact-supplementary] 补充材料 → 取值: {未明确提及, 待人工 PDF 核对}; 证据: 待核验
```

### 4.2 树设计理由

| 设计决策 | 理由 | 与当前树的关键差异 |
|---|---|---|
| 用 RQ 作为主干分支 | 原文的 finding 和统计均按 RQ 组织；RQ 是 reader navigating 原文的自然路径 | 当前树用 6 个 pattern 类型作为主干，这是一次元分类反射，不是原文自身结构 |
| 将 10 个 extraction fields 展开为叶子 | 这 10 个字段是原文最明确、可直接操作化、可统计的 schema，且 Table 2 所有 67 行均按这些字段编码 | 当前树 C03--C07 将原文字段压缩为 5 个通用 leaf，丢失了字段级别的可操作性 |
| 将 4 个 DARE QA 单独展开 | DARE 是原文的质量 rubric 核心，原文用它为 67 篇 SLR 逐一打分并分成 quartile，这 4 个 QA 需要独立的叶子维度来承载统计 | 当前树没有独立的 QA leaf |
| 展开教育/实践影响叶子 | Table 5 是原文的大型分类映射表（67 行 × usefulness for education + usefulness for practitioner + Why + SE Curriculum + SWEBOK），是一个独立的分析维度 | 当前树没有 education/practice 维度；仅在 "dimension pattern" 中作为文字提及 |
| 添加跨时域对比框架分支 | updated tertiary study 的核心贡献是"OS/FE vs SE vs Merged"的三栏对比设计，原文 14 张表格中有多张使用此框架 | 当前树没有体现这种对比框架 |
| 添加 artifact 分支 | 原文有完整的 Appendix A（67 篇 SLR 列表）和 DCP，是重要的可复现资产 | 当前树仅通过证据链间接提及，未作为独立维度 |

### 4.3 取值空间可操作性评估

| 叶子 | 取值空间 | 统计能力 | 缺失值语义 | 证据定位 |
|---|---|---|---|---|
| `leaf-ext-review-type` | {SLR, MA, MS} | 频次、与 Scope 交叉表（Table 10） | not_reported（原文 67 篇均填写，OS/FE 的 53 篇可能不区分 MA） | §3.7, Table 2 |
| `leaf-ext-review-scope` | {RQ, SERT, RT} | 频次、与 Type 交叉表（Table 10） | not_reported | §3.7, Table 2 |
| `leaf-ext-topic-area` | 24 个 SE 主题（开放枚举，可能跨论文扩展） | 频次、集中度分析 | not_reported | §5.2 |
| `leaf-ext-cited-ebse` | {Y, N} | 频次、% per year（Table 4） | not_reported | §3.7, Table 2 |
| `leaf-ext-num-primary` | 正整数 | 均值、中位数、范围、与 QA 的相关性 | not_reported | §3.7, Table 2 |
| `leaf-ext-practitioner-guidelines` | {Y, N} | 频次、% | not_reported | §3.7, Table 2 |
| `leaf-ext-source-type` | {J, C, WS, BS} | 频次分布 | not_reported | §3.7, Table 2 |
| `leaf-qa1`--`leaf-qa4` | {Y(1), P(0.5), N(0)} | 每题的 Y/P/N 分布（Table 3）、与年份趋势的交叉 | not_applicable（部分论文 QA3 因研究设计不需要质量评价） | §3.6, Table 3 |
| `leaf-rq2-education-usefulness` | {Yes, Possibly, No} | 频次 | not_reported | Table 5 |
| `leaf-rq2-practitioner-usefulness` | {Yes, Possibly, No} | 频次 | not_reported | Table 5 |

**说明**：上述取值空间均来自原文显式定义，不是 reviewer 臆造。`leaf-ext-topic-area` 的 24 个主题是开放枚举——原文本身也是通过频次统计形成的主题列表，因此这个枚举在跨论文扩展时可能增长。

## 5. 必须补充 / 修正清单

| # | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|---|
| 1 | 主干分支从"6 个 pattern 类型"改为"原文 RQ 驱动 + 方法协议分支" | `review.md` §A.1/A.2 维度树定义区域 | 将 [dim-pattern-rq]、[dim-pattern-dimension] 等 6 个 pattern 分支重构为 [dim-rq1]--[dim-rq5] 五个 RQ 分支、[dim-protocol] 方法协议分支、[dim-comparison] 跨时域对比分支、[dim-validity] 效度威胁分支和 [dim-artifact] 制品分支。保留 6 个 pattern 分支作为该树的 meta-annotation 而非主结构。 | 原文 §3.1 RQ 定义、§3.4--3.7 方法流程、§5.1--§5.5 RQ 讨论 | C |
| 2 | 展开原文 10 字段 extraction form 为独立叶子维度 | `review.md` 叶子维度表 | 在 [dim-protocol-extraction] 下新建叶子 `[leaf-ext-year]`、`[leaf-ext-review-type]`、`[leaf-ext-review-scope]`、`[leaf-ext-topic-area]`、`[leaf-ext-cited-ebse]`、`[leaf-ext-cited-guidelines]`、`[leaf-ext-num-primary]`、`[leaf-ext-practitioner-guidelines]`、`[leaf-ext-source-type]`、`[leaf-ext-quality-score]`（quality score 与 QA leaf 共享），每个叶子附带取值空间、统计用途和证据定位 | 原文 §3.7, Table 2 | C |
| 3 | 展开 4 个 DARE QA 为独立叶子维度 | `review.md` 叶子维度表 | 在 [dim-protocol-quality] 下新建 `[leaf-qa1]`--`[leaf-qa4]`，附 DARE 评分规则（Y=1, P=0.5, N=0）和原文 Table 3 定位 | 原文 §3.6, Table 3 | I |
| 4 | 展开教育/实践影响维度 | `review.md` 叶子维度表 | 在 [dim-rq2] 下新建 `[leaf-rq2-education-usefulness]`、`[leaf-rq2-practitioner-usefulness]`、`[leaf-rq2-se-curriculum]`、`[leaf-rq2-swebok]`，附取值空间 {Yes, Possibly, No} 和 Table 5/6 证据定位 | 原文 Table 5, Table 6, §5.2 | I |
| 5 | 添加跨时域对比框架分支 | `review.md` 叶子维度表 | 新建 [dim-comparison] 分支，含 `[leaf-comp-os-data]`、`[leaf-comp-fe-data]`、`[leaf-comp-se-data]`、`[leaf-comp-merged-data]`，反映 updated tertiary study 的核心对比设计 | 原文各 RQ 讨论节中的三栏对比表（Table 4/6/9/10/11/12 等） | I |
| 6 | 补充关系边：extraction fields → RQs 映射 | `review.md` 关系边表 | 添加关系边：`[edge-ext-fields-to-rqs]`，源节点 [dim-protocol-extraction]，目标节点 [dim-rq1]--[dim-rq5]，关系类型为"输入/服务于" | 原文 §3.7 vs §5.1--§5.5 | I |
| 7 | 补充关系边：OS/FE → SE → Merged 时域对比 | `review.md` 关系边表 | 添加关系边：`[edge-temporal-comparison]`，源节点为各 OS/FE 基准数据，目标节点为 SE 新数据，关系类型为"扩展/比较" | 原文各对比表（Table 4/9/10/11/12） | I |
| 8 | 补充 A.2 证据锚点到原文具体字段 | `review.md` A.2 证据账本 | 新增至少 5 条证据条目：EV-007（原文 §3.7 10 字段 extraction form）、EV-008（原文 §3.6 DARE QA1--QA4）、EV-009（原文 Table 5 教育/实践影响映射）、EV-010（原文 Table 4/9/10/11/12 的 OS/FE vs SE 对比结构）、EV-011（原文 Figure 2 PRISMA 流程图 + 分母数据）。每条证据附页码、表/图编号和原文段落定位。 | 原文 §3.6, §3.7, Table 2/3/4/5, Figure 2 | I |
| 9 | 在 A.4 复验清单中逐项列出需核对的表/图编号 | `review.md` A.4 [cmd-da-silva-2011-six-years-slr-visual-check] | 在通过条件中明确列出：Table 2（67 行 × 10+ 列完整性）、Table 3（67 行 QA 分 + quartile）、Table 5（逐篇 SWEBOK 映射准确性）、Figure 2（各步骤分母是否与文本一致）、Table 9--13 的数值准确性。标注"此清单为文本提取级确认；若与 PDF 版面不一致，需降级对应证据强度"。 | 原文各表/图 | M |
| 10 | 显式声明"当前 6 个 pattern 分支是脚手架元分类，不是原文 schema" | `review.md` A.2 或维度树定义头部 | 在维度树定义的开头或 A.2 证据账本头部添加一条 declaration：`[decl-meta-vs-source-schema]`，声明"当前树的 6 个 pattern 分支（RP/DP/FP/EP/VP/SP）是对原文的模式进行 meta-reflection 的脚手架分类，**不是**原文自身的 extraction form、QA rubric 或 taxonomy。原文的 schema 应以 §3.6 DARE、§3.7 10 字段、Table 5 教育/实践映射和 RQ-driven 讨论结构为准。A2a 在执行前必须回到原文核对这些 schema。"" | pattern-field-schema.md §4 与原文 §3.6--§3.7 的对照 | I |

## 6. C/I/M 结论

### 6.1 问题严重度定义参照

| 级别 | 定义 | 对 Paper2 的影响 |
|---|---|---|
| C | 直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性 | 如果 A2a 基于有问题的维度树执行字段抽取和统计分析，整条证据链会偏离原文真实 schema，后续 candidate finding 和 researcher adoption 的可靠性被系统性破坏 |
| I | 会实质影响维度树可用性、原文 schema 复原、证据可审计性 | A2a 即使不产生系统性错误，也需要大量返工才能补回缺失的维度、关系边和证据锚点 |
| M | 不阻塞的清晰度或维护性建议 | 影响可读性和维护效率，但不直接威胁学术目标 |

### 6.2 逐条判定

| # | 问题 | 严重度 | 理由 |
|---|---|---|---|
| 1 | 主干分支用 6 个通用 pattern 替代原文 RQ-driven 结构 | **C** | 原文的 evidence-finding 路径是按 RQ 组织的，不是按 pattern 类型组织的。如果 A2a 以 pattern 分类为主干做字段抽取，会错位：例如原文的"质量评价"信息分布在 §3.6（方法）、§3.7（抽取字段之一）、§5.4.3（RQ4 子维度）、§5.5（RQ5）和 Table 3/11/13 等多处；如果按 pattern 分类操作，会丢失这些跨节信息的 RQ-关联和对比语境。这直接影响 A2a 能否正确理解原文的证据链。 |
| 2 | 10 字段 extraction form 未作为主叶子 | **C** | 这 10 个字段是原文最直接的数据 schema，Table 2 的 67 行完全按它编码。当前维度树没有展开这 10 个字段，意味着 A2a 若按当前树执行字段抽取，将使用不同的字段集合（如"语料链""方法分类"这些抽象维度），抽取结果与原文 schema 不兼容。这是系统性偏差，直接影响 A2b 的统计分析可靠性。 |
| 3 | 4 个 DARE QA 未作为叶子 | **I** | QA1--QA4 是原文质量 rubric 的核心，原文用这 4 个维度打分了 67 篇 SLR。缺失意味着 A2a 无法从维度树中获知原文的质量评价维度结构，必须自行重新发现。 |
| 4 | 教育/实践影响维度缺失 | **I** | Table 5 是原文最大的非数值分类表之一（67 行 × usefulness + Why + SE Curriculum + SWEBOK），是 §5.2 RQ2 的核心证据。缺失导致 A2a 无法将"实践/教育影响"作为可抽取维度，而这恰好是 paper_story.md 中强调的"实践指导发现"相关维度。 |
| 5 | 跨时域对比框架缺失 | **I** | Updated tertiary study 的核心贡献就是 OS/FE vs SE vs Merged 的三栏对比。缺失此框架意味着 A2a 无法理解原文为什么每个 RQ 下都有历史对比，也无法在跨论文扩展 schema 时保留这种 longitudinal 对比结构。 |
| 6 | Extraction fields → RQs 映射关系边缺失 | **I** | 原文 §3.7 明确定义每个字段用于回答哪些 RQ。缺失此边导致 A2a 无法追踪原文的数据流。 |
| 7 | 时域对比关系边缺失 | **I** | 同上，但是跨时间的比较维度。 |
| 8 | A.2 证据缺少对原文核心 schema 元素的直接锚点 | **I** | 当前 A.2 的 6 条证据都在描述 pattern 层面的特征，没有一条直接锚定在原文的字段名、QA 编号、表号或页码上。对 A2a 的审计性来说是实质性缺失。 |
| 9 | A.4 复验清单缺少逐表/图编号 | **M** | 不直接影响 schema 复原，但降低了视觉核对的可操作性。 |
| 10 | 缺少"当前树是元分类不是原文 schema"的显式声明 | **I** | 当前 review.md 没有在任何位置明确区分"我们对这篇论文做的模式分类"和"这篇论文自身的 schema"。这是引起"通用接口 vs 原文 schema"混淆的根源。A2a 可能因此对维度树的性质产生误解。 |

### 6.3 最终判定

**最终建议：NEEDS FIX。**

当前维度树的根本问题是：它用一套跨论文通用的 pattern 分类框架（即 pattern-field-schema.md 定义的 6 类接口）来描述论文，而非复原论文自身的 schema。这两者之间的 gap 是实质性的：6 类 pattern 回答的是"这篇论文在综述方法学中充当了什么角色"，而原文的 extraction form、DARE criteria 和 RQ-driven 结构回答的是"这篇论文使用了什么 schema 来分析它的 67 篇 primary SLRs"。

对 Paper2 的影响路径如下：
- **A2a** 若基于当前维度树执行字段抽取，将使用抽象元维度（如"taxonomy""method""finding"）而非原文的实际字段（如"Review Type""Quality Score""Topic Area"），导致抽取结果与原文证据不兼容
- **A2b** 的跨论文统计分析如果混用了 meta-schema 和 source-schema，将产生类别错误
- **Paper2 的证据链**可能在一开始就建立在"综述之综述的维度模式"而非"目标综述的真实 schema"上，违反了 paper_story.md 中"维度模式必须投影自具体综述"的核心设计原则

修复优先级：问题 1 和 2（C 级）必须优先修复，因为它们直接决定了维度树是否还原的是原文的真实 schema。问题 3--10（I 级和 M 级）可以在解决 C 级问题后批量修复。建议采用上述 §4 建议的维度树骨架作为重构起点，将当前 6 个 pattern 分支降级为树的 meta-annotation 层（例如作为每个 RQ 分支的补充标签），而非主结构。
