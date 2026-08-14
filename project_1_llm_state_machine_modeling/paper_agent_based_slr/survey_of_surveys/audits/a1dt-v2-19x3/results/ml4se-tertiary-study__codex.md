### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `ml4se-tertiary-study` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；完整读取 1774 行全文文本，覆盖摘要、方法、结果、讨论、威胁和参考文献入口 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；已核对题名、作者、年份、DOI、venue、review 类型和本地元数据 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 核对 37 页 PDF，并用 `pdftotext -layout` 核对 PDF pp.5-12、13-16、23-29 的 Fig. 1、Tables 1-7、Implications、Threats、Conclusion |
| 原文类型 | 三级研究（tertiary study） |
| 被编码样本单位 | 质量通过的二级研究（secondary study / review）；主研究（primary study）只作为覆盖分母与追溯对象 |
| 样本数量 / 分母 | 搜索链：1897 条记录、1566 去重、1567 加手工检索；140 篇二级研究进入质量评估；83 篇质量通过；覆盖 6117 篇非唯一主研究 |
| 原生树类型 | 维度森林（dimension forest）：二级研究抽取字段 + DARE-4 质量 rubric + SWEBOK KA/subarea taxonomy + SE task open coding + 四轴 ML 分类 + ML application-task grouping + implication/action recommendation |
| 主统计池资格 | 是，但限于“完成型 tertiary study 的 schema / statistical-pool candidate”；ML4SE 领域结论不能直接迁移到 Paper2 |
| 总体判定 | needs repair：原文证据充分，现有 `review.md` 仍需按 A1-DT v2 重写/压实原生维度森林 |

### 1. 原文证据阅读说明

已读取本地文件：

- `bibtex.bib`：确认 ACM Computing Surveys 文章、2023、DOI `10.1145/3572905`。
- `metadata.json`：确认本地记录为 tertiary study、ML4SE、`eligible_for_statistical_synthesis: true`。
- `paper_content.txt`：完整阅读全文文本。
- `review.md`：完整读取现有单篇 review，用作返修对象。
- `paper.pdf`：做了 PDF layout 级核验；未做截图式视觉审查，复杂图形精确布局仍可在 A2a 中人工复核。

关键证据锚点：

1. 摘要 / PDF p.1：作者称系统收集、质量评估、总结并分类 83 篇 reviews，覆盖 6117 篇 primary studies。
2. §3 / PDF p.5：研究遵循 Kitchenham 与 Charters 指南，按 planning / conducting / reporting 组织，并有 formal protocol。
3. Fig. 1 / PDF p.5：完整 review method flow，含 automated/manual search、IC/EC、DARE、snowballing。
4. §3.1 / `paper_content.txt:217`：三条 RQ，分别对应 SE tasks、欠覆盖 KA、ML techniques。
5. §3.2 + Table 1 / PDF pp.6-7：检索策略为 automated、manual、backward、forward snowballing；关键词按 SE、ML、secondary studies 三组。
6. §3.3-3.4 / PDF pp.8-9：纳排对象限定为有系统方法的二级研究；140 篇 distinct secondary studies 进入 QA。
7. §3.5 + Table 2 / PDF pp.9-10：DARE-4 四项质量评价，Y/P/N 计分，阈值为总分至少 2。
8. §3.6 / `paper_content.txt:419`：显式列出每篇 quality-accepted secondary study 的抽取字段。
9. §3.6 RQ1 / PDF pp.10-11：每篇研究映射到 SWEBOK KA/subarea，并 open-code 1 到 3 个 SE tasks。
10. §3.6 RQ3 + Table 6 / PDF pp.11, 23：四轴 ML 分类为 AI role、supervision、incrementality、generalizability。
11. Table 5 / PDF p.15：按 SWEBOK KA/subarea 汇总 secondary study 数量、比例、references、primary count。
12. §5-7 / PDF pp.24-29：Implications 1-7、Threats、Conclusion 给出统计观察到 action recommendations 的边界。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文逐项编码的核心对象是质量通过的二级研究，即 SLR、systematic mapping study、meta-analysis、taxonomy 等二级研究。最终统计主体是 83 篇 quality-accepted secondary studies。6117 篇 primary studies 是这些二级研究覆盖的非唯一主研究总量，用于覆盖规模和间接证据，不是本文主要逐项编码单位。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

有。原文有四阶段检索、IC/EC、Cohen’s Kappa 选择一致性、DARE-4 质量评估、data extraction and data checking、SWEBOK 映射、open coding、Qualitative Content Analysis、四轴 ML 分类。该论文具备系统样本库，不需要降级为 roadmap / guideline seed。

3. 原文字段来自哪里？

主要来自 §3.6 的 data extraction form 式字段清单，以及下列 schema：

- DARE-4 quality rubric：Table 2。
- SWEBOK KA/subarea taxonomy：Table 5 与 §3.6 RQ1。
- SE task open coding：§3.6 RQ1。
- 四轴 ML classification scheme：§3.6 RQ3 与 Table 6。
- ML application-task grouping：Table 7。
- implications / comments / issues：§3.6 RQ2 与 §4.3、§5。
- replication / protocol package：正文脚注提到 Zenodo 和若干 CSV / protocol 文件；本审计未读取外部 replication package。

4. RQ 与样本单位是什么关系？

RQ 不是树根本身，也不是样本单位。树根应是“quality-accepted secondary study”。RQ 是字段用途和结果组织方式：RQ1 使用 KA/subarea/task 字段，RQ2 使用 coverage gap 与 implication/comment 字段，RQ3 使用四轴 ML 分类与 technique 字段。

5. 若无系统样本库，如何降级？

不适用。本文有系统样本库。只需对 discussion 中的 implication/action recommendation 降级为候选发现（candidate finding），不能把它们直接作为 Paper2 final finding。

### 3. 原生样本编码维度树 / 维度森林

```text
根对象：quality-accepted secondary study / review, n=83
├── A. 检索、纳排与质量门控上下文
│   ├── 检索阶段：automated / manual / backward snowballing / forward snowballing
│   ├── 检索来源：IEEE Xplore / ACM Digital Library / Scopus
│   ├── 检索关键词三元组：SE keyword × ML keyword × secondary-study keyword
│   ├── inclusion / exclusion criteria
│   ├── selection agreement：Cohen’s Kappa >= 0.8 gate
│   └── DARE-4 quality score：QA1--QA4, total score, threshold >= 2
├── B. 二级研究身份与书目信息
│   ├── title and source
│   ├── publication year
│   ├── publication venue / publisher
│   ├── author names / institutions / countries
│   ├── study type
│   ├── research method / guideline
│   ├── number of primary studies
│   └── covered years of primary studies
├── C. SE 领域与任务分类（RQ1 / RQ2）
│   ├── SWEBOK KA
│   ├── SWEBOK subarea
│   ├── most prominent KA/subarea rule
│   ├── SE task codes：每篇 1--3 个
│   ├── under-covered KA / subarea observation
│   └── further research implications / comments / issues
├── D. ML 技术分类（RQ3）
│   ├── role of AI in SE：3 类
│   ├── supervision type：4 类
│   ├── incrementality type：2 类
│   ├── generalizability type：2 类
│   ├── employed ML techniques
│   └── ML application task groups：Table 7 的 8 类
├── E. 汇总统计输出
│   ├── Tables 3--4：每篇二级研究 overview
│   ├── Fig. 3--4：year/publisher 与 QA trend
│   ├── Table 5：SWEBOK KA/subarea × secondary count × primary count
│   ├── Fig. 5：KA yearly distribution
│   ├── Table 6：ML axes distribution
│   ├── Fig. 6：KA × ML axes percentage relation
│   └── Table 7：ML techniques grouped by application task
└── F. 威胁、复现与行动建议
    ├── study selection validity
    ├── data validity
    ├── research validity
    ├── open data / protocol references
    ├── Implications 1--7
    └── recommendations for researchers / practitioners
```

缺失部分和 A2a 精核任务：Table 7 的算法列表非常长，本审计只把其上位 application-task categories 纳入维度树；若后续要统计算法层级，需要在 A2a 从 Table 7 和 `ml_techniques.csv` 逐项拆分。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 | 检索阶段 | 检索上下文 | §3.2, Fig. 1 | 候选研究进入样本池的检索来源阶段 | automated / manual / backward / forward | 完整枚举 | 未出现不等于无关，可能由其他阶段发现 | 复现检索链 | 方法学启发 | PDF p.5-8 | 不作为最终样本字段直接统计 |
| L02 | 检索关键词组 | 检索上下文 | Table 1 | 生成 query 的 SE/ML/secondary-study 三组关键词 | Table 1 三组关键词 | 层级枚举 | 未在表中则非本轮检索词 | 检索覆盖分析 | 构建 Paper2 检索策略 | PDF p.7 | 不迁移 ML4SE 具体词表为目标词表 |
| L03 | 纳排状态 | 检索上下文 | §3.3-3.4 | 候选二级研究是否满足 IC/EC | included / excluded + reason class | 布尔 + 自由文本理由 | 缺失需回到 selection CSV | 记录样本筛选 | 纳排边界模板 | PDF pp.8-9 | 只迁移纳排结构 |
| L04 | DARE-4 QA 分项 | 质量门控 | Table 2 | QA1--QA4 四项质量评分 | Y=1, P=0.5, N=0 | 完整枚举 + 数值 | 未评分则不能进入 accepted set | 质量门控与分层 | 质量证据模板 | PDF p.10 | DARE-4 不一定适配所有 Paper2 论文 |
| L05 | QA 总分 | 质量门控 | §3.5, Tables 3-4 | 四项 DARE 分数之和 | 0--4，0.5 步长；accepted >=2 | 数值区间 | 缺失则无法判断 quality-accepted | 质量分布统计 | 低质量排除风险 | PDF pp.10,13-14 | 仅代表作者 rubric |
| L06 | 标题与来源 | 研究身份 | §3.6 | 每篇 secondary study 的 title/source | 自由文本；source type | 自由文本 + 枚举 | 缺失需查原文或 package | overview table | 无 | §3.6, Tables 3-4 | 书目信息可迁移，具体条目不可迁移 |
| L07 | 年份 / venue / publisher | 研究身份 | §3.6, Tables 3-4 | 二级研究发表年、venue、publisher | 年份数值；venue/publisher 文本 | 数值 + 自由文本 | 缺失需外部书目核验 | 年度趋势、publisher 分布 | 领域热度 | PDF pp.13-14 | 不代表目标领域趋势 |
| L08 | 作者 / 机构 / 国家 | 研究身份 | §3.6, §4.1 | 贡献作者与机构国家 | 自由文本 | 自由文本 | 缺失不等于无作者信息 | top authors/institutions | 社群结构启发 | `paper_content.txt:419`, §4.1 | Paper2 未必需要 |
| L09 | 研究类型 | 研究身份 | §3.6, §4.1 | secondary study 的类型 | SLR / systematic mapping / survey / taxonomy；可有 meta-analysis second type | 完整枚举 + 少量组合 | 未报告需作者推断 | 研究类型分布 | 识别证据层级 | §4.1 | “survey”需区分是否系统性 |
| L10 | 研究方法 / guideline | 研究身份 | §3.6, §4.1 | 采用的 review guideline 或 method | Kitchenham, Petersen, Hall, snowballing 等 | 外部分类法引用 + 自由文本 | 未引用时作者可能按结构推断 | 方法规范统计 | 指南选择启发 | §4.1, Threats | 推断值需标记 inferred |
| L11 | 主研究数量 | 覆盖规模 | §3.6, Tables 3-4 | 每篇 secondary study 覆盖 primary studies 数量 | 非负整数 | 数值 | 未报告时作者可能从 bibliography 推断 | 覆盖规模加权 | 证据规模判断 | PDF pp.13-14, Threats | primary count 不是编码单位 |
| L12 | 覆盖年份 | 覆盖规模 | Tables 3-4 | secondary study 覆盖 primary-study 年份范围 | 年份区间 | 数值或区间 | 缺失需原文/参考文献推断 | 时段覆盖 | 历史演化 | PDF pp.13-14 | 只描述被综述研究 |
| L13 | SWEBOK KA | SE 分类 | §3.6 RQ1, Table 5 | 每篇研究映射到最 prominent KA | Table 5 覆盖 11 个 KA；源自 SWEBOK | 外部分类法引用 | 多 KA 时保留最 prominent，丢失次要 KA | KA 分布统计 | 欠覆盖 KA 候选 | PDF pp.10-11,15 | 不迁移具体 KA 频次 |
| L14 | SWEBOK subarea | SE 分类 | Table 5 | KA 下的 subarea | Table 5 子领域 | 层级枚举 | 未映射说明粒度不足 | subarea 分布 | 欠覆盖 subarea | PDF p.15 | 依赖 SWEBOK 版本 |
| L15 | SE task code | SE 分类 | §3.6 RQ1, §4.2 | open coding 得到的 SE tasks | 每篇 1--3 个；开放编码后合并 | 自由文本加理由 / 半结构枚举 | 无 task 不应默认，应查 coding sheet | task 频次与主题 | 任务覆盖发现 | PDF pp.10-11,15-19 | 任务词表需 A2a 固化 |
| L16 | further research implication/comment | RQ2 | §3.6 RQ2, §4.3 | 从二级研究中抽取的研究机会、问题、障碍 | 自由文本，按 KA/task 汇总 | 自由文本加理由 | 未提及不代表无问题 | gap synthesis | 候选 finding | PDF pp.19-23 | 只能作 candidate finding |
| L17 | role of AI in SE | ML 分类 | §3.6 RQ3, Table 6 | ML/AI 在 SE 中的角色 | SBSE；fuzzy/probabilistic；classification/learning/prediction | 完整枚举 | 多类时取 most prominent | ML role 分布 | 技术路线启发 | PDF pp.11,23 | 该轴来自 AI，非纯 ML，作者也列为威胁 |
| L18 | supervision type | ML 分类 | §3.6 RQ3, Table 6 | 学习监督类型 | supervised / unsupervised / semi-supervised / reinforcement | 完整枚举 | 多类取 prominent | 技术分布 | 数据标注需求 | PDF pp.11,23 | 不能直接评价优劣 |
| L19 | incrementality type | ML 分类 | §3.6 RQ3, Table 6 | 模型是否在线增量学习 | batch/offline / online/incremental | 完整枚举 | 未报告时需谨慎，不等于 offline | 技术分布 | online ML research gap | PDF pp.11-12,23 | “offline 占优”限 ML4SE |
| L20 | generalizability type | ML 分类 | §3.6 RQ3, Table 6 | instance-based 或 model-based | instance-based / model-based | 完整枚举 | 未报告需原文确认 | 技术分布 | 泛化讨论 | PDF pp.12,23 | 分类适配性需保留威胁 |
| L21 | employed ML techniques | ML 技术 | §3.6 RQ3, Table 7 | secondary studies 报告的 primary-study ML techniques | 算法名称集合 | 层级枚举 / 大集合 | 只在 reported when available 时抽取 | 技术 inventory | 技术候选 | PDF p.24 | 表 7 很大，需 A2a 逐项拆分 |
| L22 | ML application task group | ML 技术 | Table 7 | ML technique 按 application task 分组 | classification/clustering/regression; pattern discovery; dimensionality reduction; information retrieval; stochastic search; generation; hybrid; miscellaneous | 完整枚举 | 未分组算法需人工分类 | 技术族统计 | Paper2 技术 schema 启发 | PDF p.24 | 不迁移具体算法热度 |
| L23 | validity threat type | 威胁 | §6 | 作者对本 tertiary study 的威胁分类 | study selection / data / research validity | 完整枚举 | 未列不代表无威胁 | 证据风险说明 | 审计边界 | PDF pp.27-28 | 不作为样本单位字段 |
| L24 | implication / recommendation | action finding | §5, §7 | 由统计与讨论推出的行动建议 | Implications 1--7；researcher/practitioner recommendations | 完整枚举 + 自由文本 | 非统计字段，缺失不影响样本编码 | 不进主统计；可建候选 ledger | candidate finding | PDF pp.24-29 | 不能直接作为 Paper2 final finding |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R01 | SE keyword / ML keyword / secondary-study keyword | 组合生成 | search query | 三元组 | 不在 Table 1 不代表无关，只是不在本检索式 | Table 1 | 复现检索策略 |
| R02 | candidate study record | 去重依据 | unique study | DOI 最新 occurrence | 无 DOI 去重规则需 package 核验 | §3.2.1 | 样本流追踪 |
| R03 | selected secondary study | 被评分 | DARE-4 criteria | QA1--QA4 | 未评分则不能判断 quality gate | Table 2 | 质量门控 |
| R04 | DARE-4 total score | 阈值判断 | accepted / rejected | >=2 accepted, <2 rejected | 缺失则 blocked | §3.5 | 确定最终 83 样本 |
| R05 | accepted secondary study | covers | primary studies | count + covered years | 未报告时作者可能 bibliography inference | Tables 3-4, §6 | 覆盖规模 |
| R06 | accepted secondary study | mapped_to | SWEBOK KA/subarea | Table 5 hierarchy | 多 KA 时作者取 most prominent，次要关系丢失 | §3.6 RQ1, Table 5 | RQ1/RQ2 |
| R07 | accepted secondary study | open-coded_as | SE task(s) | 1--3 task codes | 未见 task 需查 coding sheet | §3.6 RQ1 | task taxonomy |
| R08 | SE task | may_associate_with | multiple KAs | KA set | 原文明确 task 可关联多个 KA | §3.6 RQ1 | 避免误读为单树 |
| R09 | accepted secondary study | classified_by_axis | ML role / supervision / incrementality / generalizability | Table 6 categories | 多类取 prominent，弱化多标签信息 | §3.6 RQ3, Table 6 | RQ3 |
| R10 | employed ML technique | grouped_by | ML application task | Table 7 categories | 未报告 technique 不等于技术不存在 | §3.6 RQ3, Table 7 | 技术族 inventory |
| R11 | KA/subarea | aggregated_to | Sec %, references, primary count | 数值 + reference list | aggregate 不是每篇原始字段 | Table 5 | coverage/gap 统计 |
| R12 | KA × ML axis | cross-tabulated_as | percentage distribution | Fig. 6 values | 视觉图需 PDF 核验；本轮已 layout 核对 | Fig. 6 | 交叉观察 |
| R13 | further-research comment | synthesized_into | Implications 1--7 | action recommendation | discussion synthesis，不是原始样本字段 | §4.3, §5 | candidate finding |

本文有显式关系型 schema，尤其是“secondary study → SWEBOK KA/subarea/task”和“secondary study → ML 四轴分类”。因此不能只写单层字段表。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段 / 统计表支持的统计观察：

- 83 篇 quality-accepted secondary studies 覆盖 6117 篇非唯一 primary studies。
- 140 篇 selected secondary studies 中 57 篇因 DARE score < 2 被排除。
- 研究类型分布：53 篇 SLR、16 篇 systematic mapping、13 篇 survey、1 篇 taxonomy；部分有第二类型如 meta-analysis。
- Table 5 支持 KA 覆盖观察：Software Quality、Software Testing、SE Process、SE Management 是主要覆盖区域。
- Table 6 支持 ML 分类观察：classification/learning/prediction、supervised、batch/offline、model-based 占主导。
- Table 7 支持技术 inventory：算法层面横跨 classification/clustering/regression、information retrieval、stochastic search、generation 等 application-task groups。

原文 discussion / recommendation 提出的候选 finding：

- ML4SE 工业采纳有限，需更多 empirical validation、comparative analysis、industrial trial。
- 某些 SE 基础概念与方法定义不足会影响 ML 模型构建与选择。
- human-centered KA 相比 technical KA 更少被 ML 覆盖，可能与主观评价和数据收集困难有关。
- 数据 pipeline 文档化与自动化是训练数据可信度问题。
- proprietary / industrial data 缺乏影响工业相关性、可扩展性和性能。
- online / incremental ML 在 SE 中明显不足，可作为未来方向。
- hybrid、probabilistic、search-based、cross-domain ML 方法值得进一步研究。

对 Paper2 可迁移的方法学启发：

- 先明确样本单位，再设计字段树。
- RQ 作为字段用途，不应替代样本单位。
- 外部 taxonomy、质量 rubric、open coding、关系边应分层表示。
- 统计观察、discussion implication、final finding 必须分开。
- 主研究数量可以作为覆盖分母，但不能混成逐项编码对象。

绝不能迁移的领域结论：

- 不能把 “Software Quality / Testing 最多” 迁移到 LLM/STM 或 Paper2。
- 不能把 65%/78%/99%/87% 等 ML4SE 技术分布当作目标领域事实。
- 不能把 DARE-4 直接规定为所有后续 review 的唯一质量 rubric。
- 不能把 Implications 1--7 直接写成 Paper2 final finding；只能作为候选发现模板。

### 7. 对现有 `review.md` 的返修建议

C 级：

| 等级 | 问题 | 最小返修 |
|---|---|---|
| C | `review.md` 仍先给出六个通用 leaf 的“维度树结构”，再补“原文 schema 主树”；这会让读者把跨论文接口误认为原文树 | 将“原文 schema 主树”提升为唯一主树；六叶接口改名为“通用接口投影”，放在主树之后 |
| C | 样本单位写成 `primary study / secondary study`，混淆编码单位与覆盖分母 | 改为“编码单位 = quality-accepted secondary study；primary studies = covered denominator” |
| C | A.2 证据账本大量 `not_verified`、`待 A2a`、`表 / 图待核验` 已与本轮 PDF layout 核验不一致 | 更新证据强度：Fig. 1、Tables 1-7、§5-7 可标为本地 PDF layout verified；外部 replication package 仍 `not_verified` |

I 级：

| 等级 | 问题 | 最小返修 |
|---|---|---|
| I | “原文模式候选叶子”中的 `data_source / benchmark` 不是 §3.6 明确逐项抽取字段，更多来自 discussion / implication | 降级为 RQ2 candidate implication leaf，除非 A2a 读取 `further_research.csv` 或 package 证实逐项编码 |
| I | `ML technique` 叶子混合了四轴分类、deep learning/NLP、Table 7 application-task groups | 拆成 `role_of_AI_in_SE`、`supervision`、`incrementality`、`generalizability`、`employed_ML_technique`、`application_task_group` |
| I | `review.md` line 22 写“是否目标证据池：否”，与 `metadata.json` 和 SUMMARY 的 `eligible_for_statistical_synthesis: true` / “是”不一致 | 改为“主统计池资格：是，但仅作为 schema/statistical-pool candidate；领域结论不可迁移” |
| I | A.3 结论仍多为弱泛化结论，缺少字段级结论 | 增加结论：样本单位、DARE threshold、SWEBOK mapping、SE task open coding、四轴 ML classification、Table 7 grouping |

M 级：

| 等级 | 问题 | 最小返修 |
|---|---|---|
| M | 早期“待复核”段落说 threats 未定位、表格待核对，已过时 | 删除或改成“本轮已定位；外部 package 待核验” |
| M | “tertiary 主题 / 挑战树”过窄 | SUMMARY 原生树类型改为“维度森林：secondary-study extraction + DARE-4 + SWEBOK + ML 四轴 + open-coded tasks + implications” |
| M | A.4 visual check 当前为 `needs_manual_check` | 改为“PDF layout key tables checked；full visual screenshot optional” |

SUMMARY 当前表建议修正：

| 字段 | 当前值倾向 | 建议值 |
|---|---|---|
| 样本单位 | `reviews + traced primary studies` | `quality-accepted secondary studies/reviews；primary studies as coverage denominator` |
| 样本数量 / 分母 | `83 reviews / 6117 primary studies` | 保留，但补 `140 QA-assessed; 57 excluded; 6117 non-unique primary studies` |
| 原生树类型 | `tertiary 主题 / 挑战 / action recommendation 树` | `维度森林：extraction fields + DARE-4 + SWEBOK KA/subarea + SE task open coding + four-axis ML classification + Table 7 technique grouping + implications` |
| 统计池资格 | `是` | 保留“是”，但备注 `schema/statistical-pool candidate; domain conclusions not transferable` |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-ML4SE-01 | `bibtex.bib`, `metadata.json` | 元数据 | DOI / title / venue | ACM CSUR tertiary study, 2023 | metadata | strong | 原文类型、slug、venue | 否 | 不支撑字段树 |
| EV-ML4SE-02 | `paper_content.txt`, `paper.pdf` | 摘要 | PDF p.1 | 83 reviews, 6117 primary studies | sample_denominator | strong | 样本单位与分母 | 否；已 PDF layout 核验 | primary studies 非编码单位 |
| EV-ML4SE-03 | `paper_content.txt`, `paper.pdf` | §3 Review Methods | Fig. 1, PDF p.5 | tertiary review uses SLR phases and flow | method_flow | strong | 检索/纳排/QA 上下文 | 否；已核验 | 不提供每篇字段值 |
| EV-ML4SE-04 | `paper_content.txt`, `paper.pdf` | §3.1 | RQ1--RQ3 | RQ 对应 SE task、under-covered KA、ML techniques | rq_to_field_use | strong | RQ 与字段用途 | 否 | RQ 不是树根 |
| EV-ML4SE-05 | `paper_content.txt`, `paper.pdf` | §3.2 + Table 1 | PDF pp.6-7 | 三组关键词与四阶段检索 | search_schema | strong | 检索字段 | 否；已核验 | 不迁移具体关键词 |
| EV-ML4SE-06 | `paper_content.txt`, `paper.pdf` | §3.3-3.4 | PDF pp.8-9 | IC/EC、Kappa、140 selected studies | eligibility_schema | strong | 纳排与候选流 | 否 | 140 不是最终编码分母 |
| EV-ML4SE-07 | `paper_content.txt`, `paper.pdf` | §3.5 + Table 2 | PDF p.10 | DARE-4, score >= 2 | quality_rubric | strong | QA leaf, accepted/rejected relation | 否；已核验 | DARE-4 是作者选择 |
| EV-ML4SE-08 | `paper_content.txt` | §3.6 | Data Extraction list | title/source/year/venue/authors/type/method/QA/primary count/KA/task/implication/ML technique | extraction_form | strong | 原生叶子字段 | 否 | 字段值需 package 精核 |
| EV-ML4SE-09 | `paper_content.txt`, `paper.pdf` | §3.6 RQ1 | PDF pp.10-11 | SWEBOK KA/subarea, SE task open coding | taxonomy_and_coding | strong | SE 分类分支 | 否 | open-code 词表需 A2a 固化 |
| EV-ML4SE-10 | `paper_content.txt`, `paper.pdf` | §3.6 RQ3 + Table 6 | PDF pp.11,23 | four axes: AI role, supervision, incrementality, generalizability | ml_classification | strong | ML 四轴分类 | 否；已核验 | AI role axis 有 validity caveat |
| EV-ML4SE-11 | `paper_content.txt`, `paper.pdf` | Tables 3-5 | PDF pp.13-15 | overview and KA/subarea counts | aggregate_statistics | strong | 统计观察 | 否；已核验 | 不迁移 ML4SE 领域分布 |
| EV-ML4SE-12 | `paper_content.txt`, `paper.pdf` | Table 7 | PDF p.24 | ML techniques grouped by application task | technique_grouping | medium | 技术族 leaf | 否；已核验 | 算法细项过大，需 A2a 拆分 |
| EV-ML4SE-13 | `paper_content.txt`, `paper.pdf` | §5 | Implications 1--7 | statistics to action recommendations | candidate_finding | strong | 候选 finding | 否；已核验 | 不能升级为 Paper2 final finding |
| EV-ML4SE-14 | `paper_content.txt`, `paper.pdf` | §6 | Threats to Validity | study selection, data, research validity | limitation | strong | 迁移边界 | 否；已核验 | 不否定样本资格 |
| EV-ML4SE-15 | `paper_content.txt` | footnotes / §3 | Zenodo and CSV/protocol file names | protocol/data package exists | replication_asset | medium | 复现资产 | 是；需读取外部 package | 本轮未核验 package 内容 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-ML4SE-01 | 本文是有系统样本库的三级研究，不应降级为 roadmap/guideline seed | paper_type | 原文类型 | EV-ML4SE-02, EV-ML4SE-03, EV-ML4SE-06 | strong | 主统计池候选判断 | 外部 package 未核验不影响论文文本判定 |
| C-ML4SE-02 | 原生编码单位是 quality-accepted secondary study，n=83；primary studies 是覆盖分母 | sample_unit | 样本单位 | EV-ML4SE-02, EV-ML4SE-08, EV-ML4SE-11 | strong | SUMMARY 样本单位修正 | 6117 是 non-unique primary studies |
| C-ML4SE-03 | RQ 是字段用途和结果组织方式，不是维度树根 | rq_boundary | RQ 与树关系 | EV-ML4SE-04, EV-ML4SE-08 | strong | review.md 重写 | 无 |
| C-ML4SE-04 | 本文原生结构是维度森林，而非单一六叶通用树 | tree_type | 维度森林 | EV-ML4SE-07, EV-ML4SE-08, EV-ML4SE-09, EV-ML4SE-10, EV-ML4SE-12 | strong | A1-DT v2 主树 | 六叶接口只能作投影 |
| C-ML4SE-05 | DARE-4 rubric 是质量门控字段，score >= 2 决定 accepted set | quality_gate | QA 分支 | EV-ML4SE-07 | strong | 质量字段复原 | DARE-4 不一定迁移到所有后续研究 |
| C-ML4SE-06 | SWEBOK KA/subarea 与 SE task open coding 是 RQ1/RQ2 的核心字段 | taxonomy_leaf | SE 分类分支 | EV-ML4SE-09, EV-ML4SE-11 | strong | 叶子表与关系边 | 多 KA 时取 prominent，会损失多标签信息 |
| C-ML4SE-07 | 四轴 ML 分类和 Table 7 application-task grouping 应拆开表示 | ml_schema | ML 分类分支 | EV-ML4SE-10, EV-ML4SE-12 | strong | review.md 返修 | Table 7 算法细项需 A2a 拆分 |
| C-ML4SE-08 | Implications 1--7 是候选 finding / action recommendation，不是可直接迁移的领域结论 | finding_boundary | 候选 finding | EV-ML4SE-13, EV-ML4SE-14 | strong | candidate finding ledger | 需要跨论文反证和研究者裁决 |
| C-ML4SE-09 | 现有 `review.md` 需要返修，因为它仍把通用接口置于原生树之前，并保留过时待核验说明 | repair_needed | review.md | EV-ML4SE-08, EV-ML4SE-10, EV-ML4SE-11, EV-ML4SE-13 | strong | 单篇 review 返修 | 本任务未修改文件 |
| C-ML4SE-10 | `data_source / benchmark` 目前不能作为强原生逐项抽取字段，只能弱化为 discussion/implication seed | evidence_downgrade | 可疑叶子 | EV-ML4SE-08, EV-ML4SE-13 | medium | 防止过度复原 | 读取外部 `further_research.csv` 后可重新评估 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering、unsupported claim 降级原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 必须具体、可操作的原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用风险分级、claim audit、revision plan 输出方式。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先读资源、明确 ambiguity、不编造计划细节的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用 “DO NOT FABRICATE DETAILS” 和 unclear 明示原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化 schema、risk 字段和依赖关系表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 的完成纪律；本任务未启动 autoresearch loop。

最高风险 3 点与合并复核方式：

1. 外部 replication package 未读取：本审计基于本地 PDF/text 复原 schema，未核对 Zenodo CSV 的逐项字段值。合并时若要冻结字段全集，应读取 `review-protocol.md`、`knowledge_areas.csv`、`ml_techniques.csv`、`further_research.csv`。
2. PDF 核验是 layout text 级，不是截图级：关键表图内容已核对，但 Fig. 6 等视觉热图若需精确数值，建议 A2a 用 PDF 视觉或原始数据复核。
3. Table 7 算法清单很大：本报告只复原到 application-task group 与代表性边界，未穷尽每个算法 leaf。若后续做算法统计，必须专门拆表。

blocked / timeout / 文件缺失情况：

- 未出现 blocked。
- 未出现 timeout。
- 指定的技能文件与论文文件均可读取。
- 未启动 subagent、未修改文件、未 commit、未 push、未 gh comment。