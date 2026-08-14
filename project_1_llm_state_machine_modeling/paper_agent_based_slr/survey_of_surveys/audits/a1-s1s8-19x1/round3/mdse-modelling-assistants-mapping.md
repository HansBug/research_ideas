# mdse-modelling-assistants-mapping：A1 S1--S8 round3 单篇维度抽取审计

## 0. 审计边界与阅读状态

- **处理对象**：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/mdse-modelling-assistants-mapping`。
- **本轮角色**：A1 survey-of-surveys 单篇维度抽取 subagent；未开启 sub-subagent。
- **输出边界**：本文件只写入 `audits/a1-s1s8-19x1/round3/mdse-modelling-assistants-mapping.md`，不直接修改 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`。
- **使用限制**：本文件是 A1 文本级独立审计结果，只能作为后续主线程裁决 / A2a 精核输入，**不得直接写成 Paper2 final quantitative finding**。
- **总体判定**：该文是系统映射（systematic mapping）+ 实践侧公开文档审查。文献侧 RQ1--RQ3 以 58 个研究提案为样本单位，实践侧 RQ4 以 17 个 GMQ 工具、7 个有文档工具、15 个文档中提案 / quote 为分层样本单位。可作为 `schema_seed / statistical_pool_candidate`，但 A2a 页码、表图、Zenodo、vendor 文档来源精核前不得进入最终定量发现。

| 材料 | 阅读状态 | 依据 |
|---|---|---|
| `bibtex.bib` | 已读全文 | 12 行；确认 `Mosquera_2024`、IST 173:107492、2024、DOI `10.1016/j.infsof.2024.107492`。 |
| `metadata.json` | 已读全文 | 35 行；确认本地标注 `review_type=systematic mapping`、`eligible_for_schema_seed=true`、`eligible_for_statistical_synthesis=true`、`evidence_role=systematic_mapping_dimension_pattern`。该 eligibility 只说明后续候选资格，不替代 A2a 精核。 |
| `paper_content.txt` | 已读全文 | 1798 行；覆盖摘要 / §1--§8 / References。关键锚点：摘要 16--29 行；MRQ 与 RQ1--RQ4 75--87、210--247、893--906 行；检索与纳排 248--338 行；QA 与抽取 339--399 行；执行与 Kappa 401--449 行；Table 2 / RQ1 455--567 行；Table 3 / RQ2 568--763 行；Table 4 / RQ3 764--892 行；Table 5 / RQ4 893--1145 行；比较分析 1146--1216 行；威胁 1228--1334 行；结论与 future work 1335--1445 行。 |
| `review.md` | 已读全文 | 568 行；重点核对“全文内容详读”“维度树复原”“survey_of_surveys 自身 schema 抽取”。现有主结论总体正确，但 SUMMARY 的 S5/S8 等级同步仍有问题。 |
| `evidence_chain.md` | 已读全文 | 50 行；A.1--A.4 均已读。现有证据链为 A1-DT v2 树级最小 claim map，多数 A.2 证据仍是 `not_verified` / 待 A2a。 |
| `paper.pdf` | 局部核验 | `pdfinfo` 显示 19 页；用 `pdftotext -layout -f 6 -l 13` 局部核对 Table 2--5 与 Table 3 “five limitation clusters” vs `L1--L6` 冲突。未人工视觉核验 Fig. 4--15 的气泡图、半径、图例和页码。 |

## 1. 原文样本单位与 RQ / 表格结构审计

### 1.1 文献侧：RQ1--RQ3 的研究提案样本单位

文献侧不是以“工具”或“论文综述章节”为直接统计单位，而是以 **assisting users during modelling tasks in MDSE tools 的研究提案 / primary proposal** 为主样本单位：

1. §3.1 将 MRQ 拆成 RQ1--RQ3：RQ1 问如何辅助建模，RQ2 问目标和限制，RQ3 问评价指标和目标用户（`paper_content.txt` 210--247 行）。
2. §3.2--§3.4 定义五个数据库、PICO 检索式、1985--2024 时间窗、滚雪球、I/E 标准和 QA（248--354 行）。
3. §3.5 明确逐 RQ 抽取文本片段：RQ1 抽 strategy keywords；RQ2 抽 goals / limitations，未报告则留空；RQ3 抽 evaluation metrics / target users，泛称 `user` 或 `he/she` 时留空 / 后续 U-NS（355--399 行）。
4. §4.1 给出分母链：1,996 + 5 → 2,001 初筛记录，4 轮滚雪球新增 1,175，总计 3,176 screened records，77 possible proposals，最终 58 included proposals；纳入 K=0.634，聚类 K=0.651（401--449 行）。
5. Table 2--4 分别把 RQ1 / RQ2 / RQ3 的抽取字段聚类成策略、目标 / 限制、指标 / 用户三组取值空间（455--892 行）。

**审计裁决**：文献侧样本单位应写为 `research proposal / included proposal (n=58)`。RQ1--RQ3 是字段定义来源，不是三个独立样本池；Table 2--4 是文献侧 proposal-level 编码树的核心证据。

### 1.2 实践侧：RQ4 的工具文档与文档中提案 / quote 样本单位

实践侧 RQ4 不是从学术数据库检索 primary studies，而是从 Gartner Magic Quadrant 2023 中的 enterprise low-code application platform 工具开始：

1. §5 明确 RQ4：从实践中收集 MDSE tools 的 modelling assistance 描述，字段仍包括 strategies、goals、limitations、target users、evaluation metrics（893--906 行）。
2. §5.1 把 GMQ 工具分为 17 个：leaders 5、challenger 1、visionaries 3、niche players 8（1054--1080 行）。
3. §5.2 抽取 documentation / websites / user guides 中的 quote，并把 quote 分类到 RQ1--RQ3 同样的 S/G/L/M/U 聚类（1081--1107 行）。
4. Table 5 是实践侧文档 quote 表：每行由 `MDSE Tool`、`Modelling assistance keyword`、documentation quote 和分类标签组成；这些 quote 不是独立学术提案的原始论文记录（921--1047 行）。
5. 实践侧分母链为 17 tools → 10 NF + 7 documented tools → 15 proposals inside documentation；其中 12/15 说明 strategy、15/15 说明 goal、3/15 说明 limitation、4/15 说明 metric、4/15 说明 user，且作者指出第二人称 “you” 会隐藏目标用户（1108--1143 行）。

**审计裁决**：实践侧必须写成分层样本单位：`GMQ tool (n=17)` → `documented tool (n=7)` → `practice proposal / documentation quote (n=15)`。不得把实践侧 15 个文档提案与文献侧 58 个研究提案简单相加成同一统计分母；也不得把 `NF` 解释成工具没有 assistant，只能解释成“公开文档未找到”。

## 2. S1--S8 五分栏证据拆分

> 说明：下表等级只表示该维度对 `survey_of_surveys/` 二级 schema 的可用程度；统计池资格列只给 A1/A2a 候选资格，不给最终定量结论。凡涉及数字、图表或字段级关系，A2a 前均保持 `not_verified / candidate`。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（强） | 摘要说明本文系统阐明 software modelling assistants，并回答 RQ1--RQ3；§1 提出 MRQ：文献和实践中有哪些 proposal 用于辅助人类在 MDSE tools 中完成 modelling tasks；§5 增加 RQ4（16--29、75--87、210--247、893--906 行）。 | 根对象为“MDSE 工具中的建模辅助”。文献侧树由 RQ1--RQ3 定义字段：策略、目标/限制、指标/目标用户；实践侧 RQ4 把公开文档投影到同一字段。 | 可进入 S1 任务设定候选池；强文本证据，但不产生最终经验发现。 | 核对 PDF 页码、ScienceDirect final 版式和 MRQ/RQ 原文；确认 online-first 与卷期年份口径。 |
| S2 语料收集与筛选（强） | 五数据库、PICO search string、1985--2024、滚雪球、I/E、QA top-12 seeds；执行链为 3,176 screened records → 77 possible proposals → 58 included；实践侧为 GMQ 2023 工具文档审查（248--354、401--449、907--914、1054--1080 行）。 | 文献侧分母链：record → possible proposal → included proposal；实践侧分母链：GMQ tool → documented / NF tool → documentation proposal / quote。 | 可进入 S2 分母与筛选流程候选池；文献侧和实践侧必须分池记录。 | 精核 Fig. 3 PRISMA flow、QA top-12 阈值、Zenodo protocol；核对 GMQ 原始报告和 17 工具清单来源。 |
| S3 原生维度树 / 样本编码对象（强） | §3.5 定义 RQ1/RQ2/RQ3 literal text extraction；Table 2 给策略聚类，Table 3 给目标/限制聚类，Table 4 给指标/用户聚类，Table 5 给实践 quote 映射（355--399、455--567、568--763、764--892、921--1145 行）。 | 原生结构是维度森林：A 树 = 文献侧 proposal-level 编码树；B 树 = 实践侧 tool/documentation/proposal quote 投影树；二者共享策略、目标、限制、指标、目标用户字段，但分母和样本单位不同。 | 可进入 S3 原生树候选池；必须保留 “58 research proposals” 与 “17 tools / 7 documented tools / 15 practice quotes” 分层。 | 精核 Table 2--5 的完整取值、表号页码、practice quote 与工具 / 文档 URL 的对应；不要把 Table 5 quote 当成学术 primary study。 |
| S4 字段级证据（中） | 原文要求抽取 text fragments；Table 2--4 给聚类关键词，Table 5 给 vendor documentation quotes；但论文正文多为汇总表 / quote，没有逐 proposal sample ID 的完整 raw table（355--399、921--1047、1228--1282 行）。 | 字段级对象存在：strategy_keyword、goal_fragment、limitation_fragment、metric_fragment、target_user_fragment、documentation_quote。但当前本地 `evidence_chain.md` 仍是树级锚点，不是逐字段 sample-level 账本。 | 只能作为 S4 schema seed；A2a 前不进入字段级最终统计。 | 打开 Zenodo `10262145` 核对 raw extraction / clustered data；补逐 proposal / quote 的 sample ID、页码、表格行、vendor URL 与访问日期。 |
| S5 维度模式演化（强，但缺完整 codebook） | §3.1 用 9 位 SE experts 咨询 RQ；§3.5 先 literal extraction，再按作者术语聚类；§4.1 R1 聚类、R4 review extracted data and proposed clusters，并报告聚类 K=0.651；§7.1 承认 terminology / subjective interpretation 威胁（221--228、394--399、432--449、1263--1282 行）。 | 演化链为：MRQ/RQ 草案 → 专家咨询 → RQ-driven extraction fields → author-terminology clustering → R4 triangulation / disagreement review → Kappa 报告 → threats/future validation。 | 可进入 S5 模式演化候选池；强在有过程和 Kappa，弱点是无正文级版本化 codebook / 完整裁决日志。 | 精核 Zenodo 是否包含 codebook、triangulation details、R4 disagreement log；核对 Kappa 对象是 first clustering vs final clustering，而非 data extraction。 |
| S6 统计分析（强，但 A2a 前 not_verified） | 原文报告策略比例、软件实现比例、目标 create/refine 三分、limitation reported 50.0%、M1/M2/M3/NE、U1/U2/U3/U-NS、实践侧 NF/D 和 15 文档提案字段分布；§6 做 bubble / comparative analysis（519--567、749--763、875--892、1108--1145、1146--1216 行）。 | 可统计叶子包括 `strategy_cluster`、`software_implementation`、`goal_cluster`、`create_refine_role`、`limitation_reported/cluster`、`metric_cluster`、`user_cluster`、`documentation_status`、`gmq_class` 及若干交叉关系边。 | 可进入 S6 候选统计池，但 A1 只记录文本级候选；不得把这些数字写成 final quantitative finding。 | 人工核验 Fig. 4--13、百分比四舍五入、分母口径、bubble chart 删除 NS/NE 的影响；重点复核 Table 3 “five limitation clusters” vs `L1--L6`。 |
| S7 候选 finding（强 / 部分降级） | 摘要和 §8 主张 limitations、evaluation metrics、target users 文档稀缺；§6 比较文献与实践；§8 对 AI/LLM/GPT 的 disruptive change 是 future expectation，不是已验证实证发现（27--29、1146--1216、1335--1445 行）。 | 候选 finding 分两类：统计支撑型（限制/指标/用户缺失、software-based 主导、实践文档 NF）与未来愿景型（AI/LLM 改变 modelling assistance、需要 unified framework）。 | 统计支撑型可进入 candidate finding 池；AI/LLM 未来愿景只能作弱启发 / design implication，不进入最终领域发现。 | 为每条 finding 绑定具体分母、字段、图表和反证；future work 类句子必须标注为 author expectation。 |
| S8 研究者 / 作者质疑与裁决（强，但 data extraction 无 Kappa） | §4.1 有 R1/R2/R3/R4 分工、R3/R4 复核 77 proposals、K=0.634 inclusion、K=0.651 clustering；§7 讨论 selection bias、data extraction bias、subjective interpretation、inter-rater reliability、grey literature、search、language bias，并说明 data extraction 阶段未算 Kappa（401--449、1228--1334 行）。 | 裁决树包含 multi-reviewer selection、QA、R4 cluster review、Kappa、triangulation、threats/residual limitations。缺口是 data extraction 主要为文本，未测 Kappa，完整裁决日志需回 Zenodo。 | 可进入 S8 质量控制候选池；必须保留 “data extraction no Kappa / reviewer fatigue / terminology bias” 限制。 | 精核 §7 threat 分类与 mitigation；打开 Zenodo 查是否有更细的 disagreement / triangulation material。 |

## 3. 原生维度树 / 维度森林复原

> 说明：下列结构是本篇原文自己的样本编码结构复原，不是跨论文 pattern 模板。`strategy/goal/limitation/metric/user` 等英文保留为原文术语；中文标签说明其在本地审计中的含义。

```text
[根节点] MDSE 建模辅助图景（Mosquera et al. 2024）
样本单位 = 文献侧 research proposal / 实践侧 GMQ tool + documentation proposal/quote
统计池资格 = A2a 前仅为 schema_seed / statistical_pool_candidate

├── [树 A] 文献侧系统映射编码树（RQ1--RQ3；primary proposal n=58）
│   ├── A0 语料与筛选元数据
│   │   ├── 记录来源 = {database search, external reviewer suggestion, backward/forward snowballing}
│   │   ├── 数据库 = {IEEE Xplore, ACM Digital Library, Scopus, Springer Link, Web of Science}
│   │   ├── 时间窗 = 1985--2024
│   │   ├── 纳排 = I1/I2 + E1--E5
│   │   ├── 质量评价 = 3-point Likert × 10 questions（Table 1）
│   │   ├── 分母链 = 3176 screened records → 77 possible proposals → 58 included proposals
│   │   └── 研究者裁决 = R1/R2/R3/R4 + K(inclusion)=0.634 + K(clustering)=0.651
│   │
│   ├── A1 建模辅助策略（RQ1；Table 2）
│   │   ├── 叶子 strategy_cluster = {tools, guidelines, techniques, methods, frameworks, languages}
│   │   ├── 叶子 strategy_keyword = 作者原文关键词 / 子型，例如 recommender systems、AI software assistants、bots、plugins、model testing tools、ISO-based standardisations、model repair techniques、consistency validation methods、formal frameworks、UML extensions 等
│   │   ├── 叶子 software_implementation = {totally/partially software-based, non-software guideline}
│   │   └── 风险 = 原文单标签聚类，且 tool / method / technique / framework 边界由作者术语和研究者定义共同决定
│   │
│   ├── A2 目标（RQ2-G；Table 3）
│   │   ├── goal_cluster = {G1 change propagation, G2 consistency checking, G3 model compatibility, G4 model quality, G5 user interaction, G6 model evolution, G7 vulnerability detection}
│   │   ├── create_refine_role = {create = G6, refine = G1/G2/G3/G4/G7, both = G5}
│   │   └── evidence = extracted goal text fragment
│   │
│   ├── A3 限制（RQ2-L；Table 3）
│   │   ├── limitation_reported = {specified, L-NS}
│   │   ├── limitation_cluster = {L1 accuracy, L2 effort, L3 generality, L4 learnability, L5 scope, L6 usability, L-NS}
│   │   ├── conflict_flag = true when citing limitation count
│   │   └── 冲突说明 = §4.3 prose 写 “five clusters about limitations”，但 Table 3 与后续定义列出 L1--L6；A2a 前不得把 limitation_cluster 写成 final quantitative finding
│   │
│   ├── A4 评价指标（RQ3-M；Table 4；TAM-based）
│   │   ├── evaluation_status = {evaluated / metric specified, NE}
│   │   ├── metric_cluster = {M1 effectiveness, M2 efficiency, M3 user perception, NE}
│   │   ├── metric_subtype = {faults, F-measure, accuracy, recall, precision, modelling time, completion time, performance, perceived usefulness, industrial adoption perception, ...}
│   │   └── 多值性 = 一个 proposal 可有多个 metric；NE 是显式缺失语义
│   │
│   ├── A5 目标用户（RQ3-U；Table 4）
│   │   ├── user_cluster = {U1 designers/modellers, U2 domain experts, U3 software developers, U-NS}
│   │   ├── user_subtype = {software designers, model developers, modellers, business analysts, end-users, domain experts, developers, maintainers, ...}
│   │   └── 缺失语义 = generic “user” / “he/she” 不算明确目标用户，进入 U-NS
│   │
│   └── A6 文献侧关系边
│       ├── edge.strategy_goal = strategy_cluster → goal_cluster
│       ├── edge.strategy_limitation = strategy_cluster → limitation_cluster / L-NS
│       ├── edge.goal_metric = goal_cluster → metric_cluster / NE
│       ├── edge.goal_user = goal_cluster → user_cluster / U-NS
│       └── edge.goal_create_refine = goal_cluster → create_refine_role
│
├── [树 B] 实践侧公开文档投影树（RQ4；GMQ tools n=17）
│   ├── B0 工具层元数据
│   │   ├── gmq_class = {LE leaders, C challengers, V visionaries, NP niche players}
│   │   ├── tool_id = {OutSystems, Mendix, Microsoft Power Apps, Salesforce, ServiceNow, Oracle APEX, Appian, Zoho Creator, PegaSystems, Retool, NewgenONE, Unqork, Huawei Astro Zero, Creatio ONE, YiDA, Kintone, Quickbase}
│   │   └── documentation_status = {D documented, NF not found}
│   │
│   ├── B1 文档中提案 / quote 层（documented tools n=7; practice proposals n=15）
│   │   ├── practice_proposal_keyword = 文档中的 assistant 名称或能力名，例如 MXAssist Logic Bot、AI Code Mentor、Copilot、Developer Co-Pilot、Intelligent Wizard、Retool AI Features 等
│   │   ├── documentation_quote = websites / user guides / technical documentation 中原文 quote
│   │   ├── projected_strategy = 映射到 RQ1；实践侧主要为 Tool
│   │   ├── projected_goal = 映射到 RQ2-G
│   │   ├── projected_limitation = 映射到 RQ2-L 或 NF / not specified
│   │   ├── projected_metric = 映射到 RQ3-M 或 NF / not specified
│   │   ├── projected_user = 映射到 RQ3-U 或 NF / hidden user
│   │   └── second_person_hidden_user = 文档以 “you” 写作导致目标用户隐藏
│   │
│   └── B2 实践侧关系边
│       ├── edge.tool_documentation = tool_id → documentation_status
│       ├── edge.tool_practice_proposal = documented tool → 0..n documentation proposals / quotes
│       ├── edge.practice_quote_projection = documentation_quote → {S/G/L/M/U cluster}
│       └── edge.not_documented_boundary = NF → stop coding, but not evidence of absence
│
└── [树 C] 研究者质疑与效度边界（§7）
    ├── internal_validity = {selection bias, data extraction bias, subjective interpretation, inter-rater reliability, reviewer fatigue}
    ├── construct_validity = {grey literature bias, search bias}
    ├── external_validity = {language bias / English-only}
    ├── terminology_bias = author terminology + reviewer cluster definitions
    ├── data_extraction_limit = no Kappa during data extraction because data were mainly text
    └── practice_limit = publicly documented proposal only; undocumented tool capability remains invisible
```

### 3.1 关键叶子与取值空间审计

| 叶子 | 样本单位 | 取值空间 | 证据锚点 | A1 裁决 |
|---|---|---|---|---|
| `strategy_cluster` | 文献侧 proposal | `{tools, guidelines, techniques, methods, frameworks, languages}` | Table 2；455--567 行 | 可作 schema seed；单标签风险需保留。 |
| `goal_cluster` | 文献侧 proposal | `{G1, G2, G3, G4, G5, G6, G7}` | Table 3；568--763 行 | 可作候选统计叶子；G3/G7 稀疏。 |
| `limitation_cluster` | 文献侧 proposal | `{L1, L2, L3, L4, L5, L6, L-NS}` | Table 3；568--763 行 | **待核验冲突叶子**：正文称 five，表中为 L1--L6；不得最终统计。 |
| `metric_cluster` | 文献侧 proposal | `{M1, M2, M3, NE}` | Table 4；764--892 行 | 可作候选统计叶子；一 proposal 可多指标。 |
| `user_cluster` | 文献侧 proposal | `{U1, U2, U3, U-NS}` | Table 4；764--892 行 | 可作候选统计叶子；U-NS 是显式缺失语义。 |
| `documentation_status` | 实践侧 GMQ tool | `{D, NF}` | §5.2 / Fig. 9；1108--1115 行 | 仅表示公开文档是否找到，不等价于能力是否存在。 |
| `practice_proposal_quote` | 文档中 proposal / quote | 自由文本 quote + S/G/L/M/U 标签 | Table 5；921--1047 行 | 可作字段级 evidence seed；需 vendor source A2a。 |
| `second_person_hidden_user` | 文档中 quote / 工具文档 | `{true, false / not reported}` | §5.2；1138--1143 行 | 高价值缺失语义；A2a 需回原文档复核。 |
| `kappa_inclusion` | 筛选流程 | 数值，0.634 | §4.1；426--431 行 | 支撑 S8 inclusion 裁决。 |
| `kappa_clustering` | 聚类流程 | 数值，0.651 | §4.1；432--438 行 | 支撑 S5/S8 clustering 裁决；不是 data extraction Kappa。 |

### 3.2 关系边审计

| 关系边 | 源 → 目标 | 原文位置 | 缺失语义 | A1 用途 |
|---|---|---|---|---|
| `edge.strategy_goal` | `strategy_cluster` → `goal_cluster` | Fig. 11 / §6；1146--1171 行 | NS/NE 从 bubble chart 移除，需保留图形过滤说明 | 候选交叉统计；A2a 前不最终。 |
| `edge.strategy_limitation` | `strategy_cluster` → `limitation_cluster` | Fig. 11 / §6；1156--1171 行 | L-NS 是有意义缺失，不应作为噪声删除 | 候选 gap 分析；受 L1--L6 冲突影响。 |
| `edge.goal_metric` | `goal_cluster` → `metric_cluster` | Fig. 6 / Fig. 12；1172--1190 行 | NE 从部分比较图中移除 | 候选评价模式分析。 |
| `edge.goal_user` | `goal_cluster` → `user_cluster` | Fig. 6 / Fig. 12；1172--1190 行 | U-NS / 第二人称隐藏用户需保留 | 候选 user targeting 分析。 |
| `edge.literature_practice_projection` | 文献侧 S/G/L/M/U → 实践侧 S/G/L/M/U | Fig. 13 / §6；1191--1208 行 | 实践侧 NF / sparse data 不等于反证 | 文献 / 实践对照候选。 |
| `edge.tool_documentation` | GMQ tool → D/NF | Fig. 9 / §5.2；1108--1115 行 | NF = no documentation found | 实践侧样本单位边界。 |
| `edge.tool_quote_projection` | vendor quote → S/G/L/M/U label | Table 5；921--1047 行 | quote 若无 L/M/U 则 not specified，不补猜 | 字段级 evidence seed。 |

## 4. 统计池资格与 A2a 接力

- **主统计池候选**：是，但仅限 A2a 后可升级的 systematic mapping / documentation-review 维度；A1 当前只给 `schema_seed / statistical_pool_candidate`。
- **不得进入最终定量发现的内容**：所有 Table 2--5 比例、Fig. 4--13 bubble / distribution 关系、Table 3 limitation 类数、vendor 文档 quote 当前都不得作为 Paper2 final quantitative finding。
- **分母纪律**：文献侧 `58 research proposals` 与实践侧 `17 tools / 7 documented tools / 15 documentation proposals` 必须分池；比较时只能说“同一字段体系下的投影对照”，不得直接合并计数。
- **缺失值纪律**：`L-NS`、`NE`、`U-NS`、`NF` 都是一等字段值；其中 `NF` 只表示公开文档未找到，不表示工具没有相应能力。
- **A2a 接力项**：
  1. PDF 视觉核验 Fig. 3--13，尤其是 PRISMA flow、bubble chart 半径、NS/NE 删除策略和百分比四舍五入。
  2. 精核 Table 3：§4.3 文本写 five limitation clusters，但 Table 3 / 后续段落列出 L1--L6；确认是否作者勘误、版式问题或 prose 错误。
  3. 打开 Zenodo `10262145`，核对 raw extraction、clustered data、proposal IDs、R4 triangulation / disagreement 材料和 practice-source 证据。
  4. 回到 Table 5 中 vendor 文档 URL / 用户指南 / technical documentation，核对 quote 的当前可访问性、访问日期和上下文。
  5. 若 SUMMARY 要使用 S5/S8 “强”或 S6 数字，必须同步标注 A2a 前 `not_verified`，避免被误读为 final empirical result。

## 5. 对 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

| 等级 | 文件 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| C | -- | 未发现需要立即阻断 A1 的 critical 问题。 | 当前单篇已正确识别为 systematic mapping + practice documentation review，并已记录 Table 3 冲突与 A2a 限制。 | -- |
| I | `SUMMARY.md` | S5 / S8 覆盖矩阵仍写作“中”，而 `review.md` 与既有 adjudication 已采纳 S5/S8 可升强；其中 S5 有 RQ 咨询、literal extraction、author-terminology clustering、R4 review、Kappa=0.651，S8 有 multi-reviewer selection、Kappa、threats。 | 会使跨 19 篇 S1--S8 覆盖矩阵低估该文在“维度演化”和“研究者裁决”上的方法学证据，也可能影响后续 A2a 优先级。 | 将 SUMMARY 中该文 S5/S8 调整为“强，但缺完整 codebook / data extraction Kappa，A2a 待精核”。 |
| I | `SUMMARY.md` | S2/S3/S6 的一句话摘要虽提到实践侧，但没有在所有相关格内稳定写清 `17 tools → 7 documented tools → 15 practice proposals/quotes` 与 `58 research proposals` 的分母分离。 | 后续合并统计时可能把文献侧 58 个研究提案与实践侧 15 个文档提案误当同一类样本单位。 | 在 SUMMARY 对应行补充“文献侧 proposal-level；实践侧 tool/documentation/quote-level，分母不得合并”。 |
| I | `evidence_chain.md` | A.2/A.3 目前是树级 claim map，S1--S8 相关证据多数仍靠 `review.md` 的章节说明和“短引见 review.md”，没有逐 Table 2--5 字段 / practice quote 的证据标识。 | A1 可接受，但如果直接用于 SUMMARY 定量或 A2b 模式归纳，会缺少字段级回链，尤其影响 S4/S6/S7。 | A2a 增补字段级 evidence：Table 2--5 每个关键叶子、Fig. 4--13 统计关系、Table 5 vendor quote、Zenodo raw data 均应有独立 `ev-*`。 |
| M | `review.md` | 快速结论卡片写“核心产物：策略 / 目标 / 限制 / 指标 / 目标用户 五棵维度树，外加文献侧与实践侧对照”；这容易让读者忽视实践侧是 tool→quote 的分层样本单位，而非简单第六棵同质树。 | 不影响 A1 主结论，但可能降低后续读者对 sample unit 边界的敏感性。 | 改为“文献侧 proposal-level 五主干编码树 + 实践侧 tool/documentation/quote 投影子树”。 |
| M | `review.md` | §1.8 使用“主要 finding”总结原文领域结论，虽后文已有候选 / 最终发现边界，但单独摘录时仍可能被误解为 Paper2 finding。 | 轻微传播风险；尤其是 AI/LLM disruptive change 只是 future expectation。 | 在 §1.8 首句或表后追加“以下是原文 MDSE 领域 finding / future expectation，不是本库最终定量 finding”。 |
| M | `evidence_chain.md` | A.4 的结构门禁命令仍指向 A1-DT v2 19×3 目录与 57 个 result/log，和本 round3 S1--S8 独立审计目录不是同一批次。 | 不影响当前 A1-DT 证据链，但对后续 round3 读者可能造成路径混淆。 | 后续若回填 S1--S8 evidence_chain，可另列 round3 审计文件路径和 TASKS.tsv 状态。 |
| M | `review.md` / `SUMMARY.md` | `eligible_for_statistical_synthesis=true` 容易被误读为“当前可最终统计”。 | 已有若干地方写 A2a 前 not_verified，但仍建议更一致。 | 统一写作“后续主统计池候选；A2a 精核前不进入 SUMMARY 定量统计或 final research finding”。 |

## 6. 审计结论

本篇是 `survey_of_surveys/` 中非常强的脚手架样本：它完整展示了如何从 RQ 驱动的数据抽取形成 **文献侧 proposal-level 编码树**，并把同一套字段投影到 **实践侧工具文档 quote**。最关键的 A1 结果不是任何百分比，而是以下方法学结构：

1. RQ1--RQ3 直接定义 `strategy / goal / limitation / metric / user` 五主干；RQ4 是实践文档投影，不是同质研究提案池。
2. `L-NS / NE / U-NS / NF` 是显式缺失值，不是空白；尤其 `NF` 不等于工具没有相应能力。
3. Table 3 limitation 子类存在 prose “five” 与表中 `L1--L6` 冲突，A2a 前不得进入最终统计。
4. 原文有 S5/S8 的强证据链（专家 RQ 咨询、作者术语聚类、R4 review、Kappa、threats），但缺完整 codebook / data-extraction Kappa，应写“强但有限制”。
5. 所有当前数字、图表关系和 vendor quote 都只是 A1 文本级候选，不得写成 Paper2 final quantitative finding。
