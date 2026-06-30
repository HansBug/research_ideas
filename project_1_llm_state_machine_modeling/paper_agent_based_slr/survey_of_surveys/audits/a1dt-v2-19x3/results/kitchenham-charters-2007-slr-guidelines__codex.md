### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-charters-2007-slr-guidelines` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已按全文顺序阅读 3091 行，覆盖正文、表 1--9、附录 1--3 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；BibTeX 确认为 2007 EBSE 技术报告，metadata 已标为 `guideline`、不进入统计池 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 确认 65 页，并用 `pdftotext -layout` 核对表 2、表 5/6、Appendix 2、Appendix 3 的版面结构 |
| 原文类型 | guideline |
| 被编码样本单位 | 主体是 guideline item / protocol component / checklist item / extraction-form field；Appendix 2 局部列出 SE SLR 条目；Appendix 3 是 tertiary protocol，不是已执行结果 |
| 样本数量 / 分母 | 主体无系统样本库；Appendix 2 可数 SE SLR 条目 `n=15`，但候选总量 / 检索分母未在本报告中给出 |
| 原生树类型 | 降级树 / 维度森林 |
| 主统计池资格 | 否；只能作 methodological seed / boundary anchor。Appendix 2 的 `n=15` 不足以把整篇报告升级为统计型 tertiary study |
| 总体判定 | needs repair |

### 1. 原文证据阅读说明

实际读取文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。PDF 已做轻量版面核验，重点核对复杂表格和附录协议；未逐格人工校验全部表 5/7 的每个单元格，因此细粒度数值仍建议 A2a 再核。

关键证据锚点：

1. Executive Summary：报告目标是提出 SE 系统文献综述指南，来源于医学指南、社科书籍和专家讨论。
2. §1.1：指南来源材料包括 Cochrane、NHMRC、CRD、Petticrew & Roberts、Fink、专家会议和 EBSE 项目经验。
3. §1.2：构建过程是作者起草、内部 EBSE review、外部专家 review 后修订；不是系统检索后的主研究结果。
4. §4：综述流程被划分为 planning、conducting、reporting 三阶段。
5. §5.3：研究问题驱动 search、data extraction、data analysis。
6. §5.4：protocol 字段包括 background、RQ、search strategy、selection、quality、extraction、synthesis、dissemination、timetable。
7. 表 2：search process documentation 给出数据源到记录字段的映射。
8. 表 5 / 表 6：分别给出定量研究和定性研究 quality checklist。
9. 表 7：给出一个已填写 data collection form 示例，字段来自 cost-estimation SLR。
10. 表 8：给出 systematic review report 的 section / subsection / scope / comments。
11. Appendix 2：列出 2004--2007、DARE 分数 ≥2 的 SE SLR，字段含 author、date、topic type、topic area、quality score。
12. Appendix 3：给出 tertiary study protocol，含 RQ、search sources、inclusion/exclusion、DARE scoring、data collection、data analysis。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象不是一组完整执行后的 primary studies，而是“如何执行 SLR/SMS/tertiary review”的方法学对象：protocol component、search documentation item、quality checklist item、data extraction field、report section。
2. 作者有 guideline construction process，但不是本文主体的系统检索 / 纳排 / 数据抽取 / 编码方案。Appendix 2 背后提到曾作为 recent SE SLR review 的一部分识别和评分，但本报告只给结果清单和 Appendix 3 protocol，未给完整执行分母。
3. 字段来源主要来自 guideline item、quality rubric、data extraction form、reporting table、appendix protocol。Appendix 2 是局部 mapping table；Appendix 3 是 protocol seed。
4. RQ 不是本文维度树根；本文自身没有执行型 RQ。RQ 在原文中是被指南规定的 protocol 字段，并驱动 search / extraction / synthesis。
5. 降级方式：整篇作为 methodological seed / schema seed；Appendix 2 可记录 `n=15` 的局部表格事实，但不得作为主统计池样本库。

### 3. 原生样本编码维度树 / 维度森林

```text
Root: SLR guideline artifact
├── Planning / Protocol
│   ├── need for review / existing review appraisal
│   ├── RQ type and PICOC
│   ├── protocol components
│   └── protocol evaluation consistency checks
├── Identification / Search Documentation
│   ├── search source type
│   ├── database / venue / website / contacted researcher
│   ├── search date, years covered, URL, conditions
│   └── search rationale
├── Study Selection
│   ├── inclusion / exclusion criteria
│   ├── practical screening criteria
│   ├── multistage screening
│   └── reliability / disagreement resolution
├── Quality Assessment
│   ├── quality concepts: bias, internal validity, external validity
│   ├── bias types: selection, performance, measurement, attrition
│   ├── quantitative checklist: stage × study type × question
│   └── qualitative checklist: 18 questions
├── Data Extraction
│   ├── standard form metadata
│   ├── topic-specific extraction fields, as in Table 7
│   ├── extractor / checker / arbitration
│   └── duplicate, missing, manipulated data handling
├── Data Synthesis
│   ├── narrative tabulation dimensions
│   ├── quantitative effect measures and plots
│   ├── qualitative synthesis modes
│   ├── mixed synthesis
│   └── sensitivity / publication bias checks
├── Reporting
│   ├── dissemination channels
│   ├── report structure table
│   ├── report evaluation
│   └── protocol deviations / appendices
└── Appendices as Local Seeds
    ├── Appendix 2: SE SLR list fields, n=15, denominator missing
    └── Appendix 3: tertiary protocol fields, not executed in this report
```

取值空间多为 guideline enumeration、checklist question、free-text-with-rationale、boolean / Y-P-N score、numeric score、relation field。缺失部分：表 5 和表 7 很大，本审计只恢复核心主干和代表性叶子；A2a 应逐格核对所有 checklist / extraction form leaf。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 指南来源材料 | Root | §1.1 | 构成指南的来源 | 医学指南、社科书、专家讨论、EBSE 经验 | 层级枚举 | 未列来源不可脑补 | 不统计 | 来源等级判断 | §1.1 | 只作来源说明 |
| L2 | SLR 阶段 | Review Process | §4 | SLR 生命周期阶段 | planning / conducting / reporting | 完整枚举 | 不适用 | schema seed | 流程骨架 | §4 | 非样本分类结果 |
| L3 | RQ 结构 | Planning | §5.3 | 问题如何组织 | PICOC + study design | 外部分类法引用 | 未结构化可记自由文本 | 字段依赖 | 设计启发 | §5.3.2 | 不代表本文 RQ |
| L4 | Protocol 组件 | Planning | §5.4 | 协议必须记录内容 | background、RQ、search、selection、quality、extraction、synthesis、dissemination、timetable | 完整枚举 | 未报告即 protocol gap | 可作 checklist | run-record 启发 | §5.4 | 只迁移方法字段 |
| L5 | Search documentation | Search | 表 2 | 每类搜索源的记录字段 | 数据库、检索式、日期、年份、URL、联系人等 | 层级枚举 | 缺失表示不可复核 | 可统计完整性 | evidence-chain 启发 | 表 2 | 不给主题结论 |
| L6 | Selection criteria | Study Selection | §6.2 | 纳入 / 排除与筛选过程 | inclusion、exclusion、practical criteria、excluded-list reason | 自由文本加理由 | 未报告即弱证据 | 可作审计字段 | scope gate | §6.2 | 不迁移具体 criteria |
| L7 | Inclusion reliability | Study Selection | §6.2.3 | 纳排一致性 | Cohen Kappa、consensus、advisor/expert check、test-retest | 数值 / 关系值 | 单人研究需替代核验 | 可作质量指标 | reviewer risk | §6.2.3 | 不强制所有 SLR |
| L8 | Quality concepts | Quality | 表 3 | 质量概念定义 | bias、internal validity、external validity | 完整枚举 | 不适用 | 质量口径 | validity seed | 表 3 | 定义可迁移 |
| L9 | Bias types | Quality | 表 4 | 偏差类型和防护机制 | selection、performance、measurement、attrition | 完整枚举 | 未评估即质量缺口 | 质量统计 | threat model | 表 4 | 防护机制需按领域改写 |
| L10 | Quantitative checklist | Quality | 表 5 | 定量研究质量问题 | design / conduct / analysis / conclusions × study type | 层级枚举 | 未逐格核验 | A2a 可统计 | quality rubric seed | 表 5 | 本轮不冻结全叶子 |
| L11 | Qualitative checklist | Quality | 表 6 | 定性研究质量问题 | 18 个问题 | 完整枚举 | 未逐项回答即弱 | A2a 可统计 | qualitative audit | 表 6 | 需适配目标研究 |
| L12 | Data form metadata | Data Extraction | §6.4.2 | 抽取表通用字段 | reviewer、date、title、authors、publication details、notes | 完整枚举 | 未填即审计缺口 | 可统计完整性 | run record seed | §6.4.2 | 可迁移结构 |
| L13 | Topic extraction fields | Data Extraction | 表 7 | 单篇 primary study 的主题字段 | domain、database、project counts、metrics、models、accuracy、tests、summary | 层级枚举 / 数值 | 主题外不适用 | 示例字段，不主统计 | extraction-form seed | 表 7 | cost-estimation 专属字段不可直接迁移 |
| L14 | Synthesis metrics | Data Synthesis | §6.5 | 综合所需指标 | sample size、effect size、SE、mean difference、CI、units、OR/RR/ARR/WMD/SMD | 数值 / 完整枚举 | 不可比则降级 narrative | 统计方法 seed | evidence grading | §6.5.2 | 不代表本文实测结果 |
| L15 | Report structure | Reporting | 表 8 | SLR 报告结构 | title、abstract、background、methods、results、discussion、conclusions、appendices 等 | 层级枚举 | 未报告即透明性缺口 | 报告审计 | Paper2 写作约束 | 表 8 | 结构可迁移 |
| L16 | Appendix 2 SLR fields | Appendix 2 | Appendix 2 表 | 高质量 SE SLR 清单字段 | author、date、title、reference、topic type、topic area、quality score | 表格字段 / 数值 | denominator missing | 局部可数 `n=15` | boundary anchor | Appendix 2 | 不进入主统计池 |
| L17 | Appendix 3 protocol data fields | Appendix 3 | Data Collection | tertiary protocol 计划抽取字段 | source、year、type、scope、topic、authors、affiliation、RQ、EBSE reference、guideline reference、practitioner guideline、# primary studies、summary、quality score | 层级枚举 / 布尔 / 数值 | protocol 未执行 | schema seed | tertiary design seed | Appendix 3 | 不能冒充已执行结果 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | Research question | drives | Search process | search terms / sources | RQ 不清则 search 不可审计 | §5.3 | protocol consistency |
| E2 | Research question | drives | Data extraction | data items | 抽取字段无法回答 RQ 则设计失败 | §5.3 | schema validation |
| E3 | Research question | drives | Data analysis | synthesis strategy | 分析不能回答 RQ 则降级 | §5.3 | finding boundary |
| E4 | PICOC | derives | Search terms | population / intervention / comparison / outcome / context synonyms | 未结构化则需自由文本说明 | §5.3.2、§6.1.1 | 检索复核 |
| E5 | Study type | selects | Quality instrument | quantitative / qualitative / design-specific checklist | 混合研究需多个 checklist | §6.3.3 | quality audit |
| E6 | Quality score | informs | Selection or synthesis | inclusion/exclusion / subgroup / sensitivity | 未说明用途则质量分不可解释 | §6.3.3 | evidence weighting |
| E7 | Extracted data | feeds | Synthesis | narrative / quantitative / qualitative / mixed | 数据不可比则不能 meta-analysis | §6.5 | statistical readiness |
| E8 | Protocol | constrains | Report | report changes / deviations | 偏离未报告即透明性风险 | §7.4、表 8 | report audit |
| E9 | Appendix 3 data fields | answer | Appendix 3 RQs | activity、topics、leaders、limitations | 协议未执行，无结果强度 | Appendix 3 | tertiary seed only |

### 6. 统计观察、候选 finding 与 final finding 边界

字段 / 表支持的统计观察：

- 表 1 给出 SE 与其他学科研究实践相似度评分；这是背景论证，不是本文样本库统计。
- Appendix 2 局部列出 `n=15` 个 DARE ≥2 的 SE SLR 条目，字段包括 topic type、topic area、quality score；但缺少候选总量和检索分母。
- Appendix 3 计划按 year/source 统计 papers、candidate papers、selected papers，但这只是 protocol。

Discussion / recommendation 候选 finding：

- SE SLR 应使用可审计 protocol、search log、selection criteria、quality instrument、data extraction form。
- SE 中 meta-analysis 可能受限，因为报告协议差异大，很多综述更可能是 descriptive synthesis。
- 单人 PhD 版 SLR 需要替代性一致性检查，如 supervisor check 或 test-retest。

对 Paper2 可迁移的方法学启发：

- 把 RQ、search、selection、quality、extraction、synthesis、reporting 作为证据链字段。
- 把 “统计观察 → 候选 finding → final finding” 分层，避免 guideline recommendation 冒充实证结论。
- 对 LLM / agent 综述可借鉴 protocol-first、extraction-form-first、quality-rubric-first。

绝不能迁移的领域结论：

- 表 7 中 cost-estimation 字段不能直接迁移为 LLM-state-machine 领域 taxonomy。
- Appendix 2 的 topic distribution 不能代表 2007 之后 SE SLR 全局分布。
- “SE 更像 social sciences”只能作为作者背景论证，不可作为 Paper2 的实证发现。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 建议 | 理由 |
|---|---|---|
| C | 重写“维度树复原”的主树，使原文 guideline forest 放在前面，六个通用 leaf 只能放在“跨论文投影”后段 | 现有文件仍先给六叶接口，容易违反 A1-DT v2 口径 |
| C | 明确总体树型为“降级树 / 维度森林”，不是普通 SLR/SMS/tertiary 原生树 | 本文主体无执行型样本库 |
| I | 在样本字段中加入：主体 N/A；Appendix 2 `n=15`，分母缺失；Appendix 3 是 protocol 未执行 | 当前 review 对 Appendix 2/3 的局部分母边界不够清楚 |
| I | 叶子表应直接列表 2、表 5、表 6、表 7、表 8、Appendix 2、Appendix 3 字段 | 这些才是原文可见字段来源 |
| I | A.2 证据账本应把 `not_verified` 升级为 text/PDF verified 的表号级锚点；逐格未核验的表 5/7 再标 A2a | 本轮已完成 PDF 版面核验，旧证据强度过低 |
| I | SUMMARY 中“样本单位 / 样本数量 / 原生树类型 / 统计池资格”应改为：guideline item / protocol field；main N/A, appendix n=15 local only；降级维度森林；否 | 避免统计池误入 |
| M | 保留技术报告非 peer-reviewed venue 风险，但不要因此否定其方法学基准价值 | metadata 已正确标为技术报告 |
| M | 修正 Appendix 3 中 CRD/DARE 的拼写口径，避免 `CDR` 误写 | 原文部分有 OCR/拼写噪声，review 应统一为 CRD |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV1 | `paper_content.txt` / `paper.pdf` | Executive Summary | 目标段 | 提出 SE SLR 指南 | 类型判定 | strong | guideline root | 否 | 不等于执行型 SLR |
| EV2 | `paper_content.txt` | §1.1 | Source Material | 来源于既有指南、书籍、专家、EBSE 经验 | 来源链 | strong | L1 | 否 | 非系统样本库 |
| EV3 | `paper_content.txt` | §4 | Review Process | 三阶段：planning / conducting / reporting | 主干树 | strong | L2 | 否 | 流程字段，不是结果分类 |
| EV4 | `paper_content.txt` | §5.3 | RQ drives methodology | RQ 驱动 search / extraction / analysis | 关系边 | strong | E1--E3 | 否 | RQ 是 protocol 字段 |
| EV5 | `paper_content.txt` / PDF layout | 表 2 | Search process documentation | 数据源与记录字段映射 | 字段表 | strong | L5 | 已核验 | 不给实际搜索分母 |
| EV6 | `paper_content.txt` / PDF layout | 表 5、表 6 | Quality checklist | 定量 / 定性质量问题清单 | rubric | medium | L10、L11 | 表 5 逐格需 A2a | 不应全量手抄为最终叶子 |
| EV7 | `paper_content.txt` | 表 7 | Data collection form | 已填写 extraction form 示例 | extraction seed | medium | L13 | 逐格需 A2a | cost-estimation 专属 |
| EV8 | `paper_content.txt` / PDF layout | 表 8 | Report structure | SLR 报告结构字段 | reporting schema | strong | L15 | 已核验 | 结构可迁移，内容不可迁移 |
| EV9 | `paper_content.txt` / PDF layout | Appendix 2 | SE SLR table | DARE ≥2 的 15 条 SE SLR | local table | strong | L16 | 已核验 | denominator missing |
| EV10 | `paper_content.txt` / PDF layout | Appendix 3 | Protocol | tertiary study RQ / search / data fields | protocol seed | strong | L17、E9 | 已核验 | 未执行，不能统计结果 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C1 | 本文是方法学 guideline，不是执行后的 SLR/SMS/tertiary study | type | root | EV1、EV2 | strong | metadata / review card | Appendix 2 有局部表，但不改变主体类型 |
| C2 | 原生结构应恢复为 guideline item / protocol component / checklist / form 的降级维度森林 | tree_type | root | EV3--EV8 | strong | review.md 维度树 | 细叶仍需 A2a |
| C3 | 本文主体无系统样本库，主统计池资格为否 | pool | root | EV1、EV2、EV10 | strong | SUMMARY | Appendix 2 局部 n=15 不能入主池 |
| C4 | Appendix 2 可记录 15 个 SE SLR 条目，但候选分母缺失 | local_stat | L16 | EV9 | strong | boundary note | 不能推断整体分布 |
| C5 | Appendix 3 是 tertiary protocol seed，非执行结果 | protocol_seed | L17 | EV10 | strong | schema seed | 不能写成已完成 tertiary |
| C6 | 现有 review.md 的六叶接口必须降级为投影层 | repair | review.md | EV3--EV8 | strong | 返修建议 | 保留投影可以，但不得冒充原文树 |
| C7 | 可迁移内容是 protocol-first 与 evidence-chain 纪律，不是 cost-estimation 或 EBSE 领域结论 | migration | Paper2 seed | EV5--EV8 | medium | methodology seed | 需由目标语料重新验证 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence discipline、evidence gate、unsupported claim 降级。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection、具体证据锚点、风险优先。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 rejection-risk audit、claim-evidence gap、最高风险自审。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先读上下文、明确 ambiguity、不脑补。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用 “DO NOT FABRICATE DETAILS” 原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化 schema / risk 表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 validator-gated / artifact-gated 完成观；未运行 autoresearch workflow，因任务禁止 subagent / 后台 agent。

最高风险 3 点：

1. 表 5 和表 7 很大，本审计只恢复主干与代表性叶子；合并时应逐格核对。
2. Appendix 2 的 `n=15` 是我按表格条目计数；主线程应复核是否存在跨页漏行。
3. “Appendix 2 局部可数但主池不合格”的边界容易被误读；SUMMARY 应明确 main sample `N/A`、appendix local `n=15`。

blocked / timeout / 文件缺失：未出现。任务全程只读，未修改文件、未 commit、未 push、未启动 subagent。