### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `mdse-modelling-assistants-mapping` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；全文 1798 行已分段通读，并用 `rg` 定位 RQ、表格、统计与 threats 证据 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；BibTeX 与 metadata 均已读取，用于核对标题、作者、年份、DOI、类型与本地 PDF 状态 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 确认 19 页 PDF，用 `pdftotext -layout` 核对 Table 2--5、Fig. 9--13 周边版式文本；未做逐像素/人工视觉核验 bubble chart 图形数值 |
| 原文类型 | SMS / systematic mapping；另含 practice documentation review，不是 tertiary review |
| 被编码样本单位 | 主单位：literature 中的 modelling assistance proposal；实践侧辅单位：GMQ 工具文档中的 documented modelling assistance proposal / feature |
| 样本数量 / 分母 | literature：3,176 screened records -> 58 included proposals；practice：17 GMQ low-code tools -> 7 tools with documentation -> 15 documented proposals |
| 原生树类型 | 维度森林：literature proposal 编码森林 + practice documentation proposal 编码森林 + quality rubric / cross-tab 关系层 |
| 主统计池资格 | 局部可统计：可统计原文 58 proposals 与 15 practice proposals 的原文维度；对 Paper2 只能作 schema_seed / boundary anchor，不能直接迁移领域结论 |
| 总体判定 | needs repair：现有 `review.md` 内容丰富，但维度树复原仍混入通用六叶、v1 审计入口与若干非原文字段 |

### 1. 原文证据阅读说明

已读取文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。已核对 PDF：`paper.pdf` 的元数据、页数，以及 pages 6--17 中 Table 2--5、Fig. 9--13 附近的版式文本。未做的核验：没有打开 PDF 图像逐项人工检查 Fig. 4--15 的气泡大小、颜色或视觉布局；Zenodo replication package 也未打开。

关键证据锚点：

| 锚点 | 原文位置 | 证据要点 |
|---|---|---|
| E1 | Abstract / Page 1 | 目标是系统梳理 MDSE / low-code / no-code modelling assistants；结果聚类字段包括 strategies、goals、limitations、metrics、target users |
| E2 | §1 Introduction | 定义 modelling assistance 为辅助人类在 MDSE 工具中完成软件建模任务的 strategy |
| E3 | §3.1 | MRQ 拆成 RQ1 strategy、RQ2 goals/limitations、RQ3 metrics/users；practice 侧后续引入 RQ4 |
| E4 | §3.2--3.3 | database search + snowballing；五个数据库；I1/I2 与 E1--E5 决定纳入 proposal |
| E5 | Table 1 / §3.4 | quality assessment rubric：proposal clarity、limitations/goals clarity、downloadability、case study、empirical evaluation、users、results、venue、citations |
| E6 | §3.5 | extraction form 明确按 RQ 抽取 strategy keywords、goals、limitations、evaluation metrics、target users；未报告则留空或标为 user-not-specified |
| E7 | §4.1 / Fig. 3 | 3,176 records -> 58 proposals；K-statistic 0.634 selection、0.651 clustering |
| E8 | Table 2 / §4.2 | RQ1 六类 strategy clusters：Tools、Guidelines、Techniques、Methods、Frameworks、Languages |
| E9 | Table 3 / §4.3 | RQ2 七类 goals、L1--L6 limitations、L-NS；正文称 five limitation clusters 但表中实际六类，需保留为口径风险 |
| E10 | Table 4 / §4.4 | RQ3 metrics: M1/M2/M3/NE；users: U1/U2/U3/U-NS |
| E11 | Table 5 / §5.2 | practice side 用 GMQ 工具文档 quote 映射到 S/G/L/M/U；17 tools、15 proposals |
| E12 | §7--§8 | validity threats 与 final gap：limitations、metrics、target users 信息稀疏，AI/LLM 论述是 future-facing，不是实证结论 |

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 modelling assistance proposal。literature 侧不是“论文综述本身”，而是 58 个面向 MDSE 工具用户建模任务的 proposals；practice 侧是 17 个 GMQ low-code tools 的公开文档中可识别的 15 个 modelling assistance proposals / features。

2. 作者有系统检索、纳排、质量评价、数据抽取和编码方案。检索采用五个数据库 + snowballing；纳排标准 I1/I2/E1--E5；质量评价是 10 项 3-point Likert rubric；数据抽取按 RQ1--RQ3 采集文本片段，再基于作者术语聚类。

3. 原文字段来源主要是 extraction form + classification schema + quality rubric + mapping/cross-tab figures + practice quote table。没有发现一个单独命名的 appendix schema，但原文说明 raw data 与 protocol 在 Zenodo；本次未核验 Zenodo。

4. RQ 不是树根模板本身，而是字段用途和结果组织方式。真正的样本编码字段是每个 proposal 的 strategy、goal、limitation、metric、target user，以及 quality assessment items；RQ4 将同一字段体系投影到 practice documentation quotes。

5. 本文不是 roadmap / vision / proposal，具备系统样本库；不需要降级为“无系统样本库”。但对 Paper2 迁移时必须降级为 schema_seed / methodological seed，因为 MDSE assistant 的领域统计不能直接当作 LLM4STM 领域 finding。

### 3. 原生样本编码维度树 / 维度森林

```text
mdse_modelling_assistance_mapping
├── literature_proposal_pool
│   ├── source_record_chain
│   │   ├── database_source: IEEE Xplore / ACM DL / Scopus / Springer Link / Web of Science
│   │   ├── search_strategy: database search / backward snowballing / forward snowballing / external reviewer suggestions
│   │   ├── screened_records: 3176
│   │   ├── possible_proposals: 77 before final review
│   │   └── included_proposals: 58
│   ├── selection_schema
│   │   ├── inclusion: I1 dedicated proposal; I2 assists MDSE-tool users during modelling
│   │   └── exclusion: not main contribution / non-SE / non-English / non-peer-reviewed / no full text
│   ├── quality_rubric
│   │   ├── subjective_items: clarity, limitations, goals, downloadable tool/source, case/example, empirical evaluation, users, results
│   │   └── objective_items: venue importance, citation count
│   ├── rq1_strategy
│   │   ├── strategy_cluster: Tools / Guidelines / Techniques / Methods / Frameworks / Languages
│   │   └── strategy_keywords: original author terminology grouped under each cluster
│   ├── rq2_goal_limitation
│   │   ├── goal_cluster: G1 change propagation / G2 consistency checking / G3 compatibility / G4 quality / G5 interaction / G6 evolution / G7 vulnerability
│   │   ├── limitation_cluster: L1 accuracy / L2 effort / L3 generality / L4 learnability / L5 scope / L6 usability
│   │   └── limitation_missingness: L-NS
│   ├── rq3_metric_user
│   │   ├── metric_cluster: M1 effectiveness / M2 efficiency / M3 user perception / NE
│   │   └── user_cluster: U1 designers-modellers / U2 domain experts / U3 software developers / U-NS
│   └── cross_analysis
│       ├── goal_x_limitation
│       ├── strategy_x_goal_limitation
│       └── goal_x_metric_user
└── practice_documentation_pool
    ├── tool_pool: 17 GMQ enterprise low-code tools
    ├── gmq_class: LE / C / V / NP
    ├── documentation_status: documented / not found
    ├── documented_proposal: 15 proposals from 7 tools
    ├── quote_mapping: S / G / L / M / U tags using literature clusters
    └── literature_vs_practice_comparison
```

缺失部分与 A2a 精核任务：需要回到 Zenodo raw data 确认每个 proposal 的字段 cardinality，尤其是 goal、limitation、user 是否严格单标签；需要人工核验 Fig. 4--15 的视觉统计；需要逐项核对 Table 5 的 vendor quote 原网页是否仍可访问。当前树对本地 `paper_content.txt` 与 PDF 表格文本是可核验的，但不是 replication package 级别复现。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 | 数据源 | source_record_chain | §3.2 | 检索数据库或补充来源 | 5 databases / snowballing / reviewer suggestions | 完整枚举 | 不适用 | 分母追踪 | 检索覆盖风险 | §3.2 | 只迁移检索记录方法 |
| L02 | 筛选分母 | source_record_chain | §4.1/Fig.3 | screened records 与 proposal 流程 | 2001, 1175, 3176, 77, 58 等数值 | 数值链条 | 不适用 | 可统计 | 样本可靠性 | §4.1 | 不迁移比例到 Paper2 |
| L03 | 纳入标准 | selection_schema | §3.3 | 是否专门提出辅助 MDSE 建模的 proposal | I1, I2 | 布尔/规则 | 不满足即排除 | 样本边界 | scope gate seed | §3.3 | 需改写为 LLM4STM scope |
| L04 | 排除标准 | selection_schema | §3.3 | 排除非主贡献、非 SE 等 | E1--E5 | 完整枚举 | 不适用 | 样本边界 | false positive 控制 | §3.3 | 只迁移规则形态 |
| L05 | QA subjective | quality_rubric | Table 1 | proposal 质量主观评分项 | 8 items, each Yes/Partially/No | 完整枚举+三值评分 | 未评分需 not_verified | quality seed / snowball seed | quality gate | Table 1 | 不能当作本文主发现 |
| L06 | QA objective | quality_rubric | Table 1 | venue 与 citation 评分 | venue rank, citation bucket | 完整枚举/区间 | 未索引/低引用 | seed selection | 证据质量 | Table 1 | 不等于研究质量绝对评价 |
| L07 | Strategy cluster | rq1_strategy | Table 2 | 建模辅助采用的 strategy | Tools, Guidelines, Techniques, Methods, Frameworks, Languages | 完整枚举 | 未发现未单列；需回 raw data | 核心统计 | assistant schema seed | Table 2/Fig.4 | LLM agent 系统需允许多标签 |
| L08 | Strategy keyword | rq1_strategy | Table 2 | 作者术语下的子型 | recommender, AI assistant, bot, plugin 等 | 层级枚举 | 术语不统一 | 子类统计 | 技术路线 seed | Table 2 | 术语受作者命名影响 |
| L09 | Goal cluster | rq2_goal_limitation | Table 3 | proposal 试图达成的建模辅助目标 | G1--G7 | 完整枚举 | 无显式 goal 时按原文留空；表内未给 G-NS | 核心统计 | 生命周期映射 | Table 3/Fig.5 | 不直接等同 STM 目标 |
| L10 | Limitation cluster | rq2_goal_limitation | Table 3 | 作者报告的限制类别 | L1--L6 | 完整枚举 | L-NS 表示未显式报告 | 核心统计 | 缺失报告 finding | Table 3/Fig.5 | 正文 five vs 表 six 需标风险 |
| L11 | Metric cluster | rq3_metric_user | Table 4 | evaluation metric 类型 | M1, M2, M3 | 完整枚举/可多值 | NE 表示 not evaluated | 核心统计 | evaluation gap | Table 4/Fig.6 | STM 需加 formal verification metrics |
| L12 | Target user cluster | rq3_metric_user | Table 4 | 被辅助的用户类型 | U1, U2, U3 | 完整枚举 | U-NS 表示 generic user/he/she | 核心统计 | user specificity gap | Table 4/Fig.6 | STM 需分 domain expert/verifier/modeller |
| L13 | GMQ class | practice_tool_pool | §5.1/Table 5 | 工具市场分类 | LE, C, V, NP | 完整枚举 | 不适用 | practice 分层 | 产业对照 | §5.1 | 只代表 GMQ 2023 |
| L14 | Documentation status | practice_tool_pool | §5.2/Fig.9 | 是否找到公开 modelling assistance 文档 | D / NF | 布尔/枚举 | NF 是未找到文档，不是能力不存在 | practice 统计 | evidence absence boundary | Fig.9 | 不可写成工具无功能 |
| L15 | Practice quote tag | quote_mapping | Table 5 | 文档 quote 被映射为 S/G/L/M/U | S, G, L, M, U with clusters | 关系值 | 未提及即 NF/not specified | practice 统计 | 文档透明度 gap | Table 5/Fig.10 | quote 未回网页复核 |
| L16 | Cross-analysis axis | cross_analysis | Fig.5/6/11/12/13 | 字段间交叉关系 | goal-limitation, metric-user, strategy-goal, literature-practice | 关系值 | not specified clusters 在部分图中移除 | 关系统计 | candidate finding | §6/Fig.11--13 | 不是因果关系 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R01 | screened record | selection_result | included proposal | included / excluded / possible | 不满足 I/E 即排除 | §3.3, §4.1, Fig.3 | 样本分母 |
| R02 | included literature proposal | classified_as | strategy cluster | Tools / Guidelines / Techniques / Methods / Frameworks / Languages | 未发现显式缺失类 | Table 2, Fig.4 | RQ1 统计 |
| R03 | included literature proposal | classified_as | goal cluster | G1--G7 | 原文未设置 G-NS；缺失需回 raw data | Table 3, Fig.5 | RQ2 统计 |
| R04 | included literature proposal | classified_as | limitation cluster | L1--L6 / L-NS | L-NS = 未显式报告 | Table 3, Fig.5 | limitation gap |
| R05 | included literature proposal | evaluated_by | metric cluster | M1/M2/M3/NE | NE = not evaluated / no metric | Table 4, Fig.6 | RQ3 统计 |
| R06 | included literature proposal | targets | target user cluster | U1/U2/U3/U-NS | U-NS = generic user/he/she | Table 4, Fig.6 | user gap |
| R07 | GMQ tool | contains_or_lacks | documented proposal | 15 proposals / NF | NF = not found in public docs | Table 5, Fig.9--10 | practice 统计 |
| R08 | documentation quote | mapped_to | S/G/L/M/U tag | same clusters as literature | 未提及即未记录 | Table 5 | literature-practice 对照 |
| R09 | strategy cluster | cross_tabulated_with | goal/limitation | Fig.11 axes | 部分稀疏关系不解释 | §6, Fig.11 | 关系观察 |
| R10 | goal cluster | cross_tabulated_with | metric/user | Fig.12 axes | 稀疏类降级 | §6, Fig.12 | 关系观察 |
| R11 | literature cluster set | compared_with | practice cluster set | Fig.13 axes | not specified often dominates | §6, Fig.13 | candidate finding |
| R12 | quality rubric score | selects_seed_for | snowballing initial set | top 12 / 80th percentile | 未入 top seed 不等于低质量 | §3.4, §4.1 | 方法复现 |

### 6. 统计观察、候选 finding 与 final finding 边界

| 层级 | 内容 | 证据状态 | 可迁移边界 |
|---|---|---|---|
| 统计观察 | Tools 是最常见 strategy；Frameworks、Techniques、Methods 次之 | Table 2/Fig.4 支持 | 可迁移为字段设计，不可迁移为 LLM4STM 事实 |
| 统计观察 | 31.0% proposals 创建模型；43.1% refinement；25.9% both | §4.3 支持 | 可启发 generation/verification/repair 生命周期字段 |
| 统计观察 | 50.0% literature proposals 明确 limitations；其余 L-NS | §4.3/Table 3 支持 | 可迁移缺失值编码 |
| 统计观察 | metrics 中 effectiveness 与 efficiency 多，user perception 少；NE 很高 | §4.4/Table 4 支持 | 可启发 Paper2 加人机指标 |
| 统计观察 | target users 中 developers 与 modellers 多，domain experts 少，U-NS 高 | §4.4/Table 4 支持 | 可启发 target user specificity |
| 统计观察 | practice 侧 17 tools 中 10 未找到文档；15 proposals 中 limitation/metric/user 披露不足 | §5.2/Fig.9--10 支持 | 可迁移 public-doc evidence boundary |
| 候选 finding | MDSE assistant 领域缺少清楚的 limitations、metrics、target users，妨碍客观比较 | §6/§8 支持 | 可作 Paper2 方法学启发，不可直接写成 LLM4STM 领域结论 |
| 候选 finding | AI/LLM 可能改变 modelling assistance strategy，需要 unified framework | §8 discussion 支持 | 只能标 future expectation / design implication |
| Paper2 方法学启发 | 把 not specified / not evaluated / not found 当作一等字段 | 多表共同支持 | 可直接迁移为 schema 规则 |
| 绝不能迁移 | GMQ leader tools 更常公开 assistant 能力、practice 全部 target developers 等 | 仅 MDSE low-code 2023 文档 | 不可外推到 UPPAAL、Simulink、STM generation 或控制系统 |

### 7. 对现有 `review.md` 的返修建议

| 级别 | 建议 | 理由 |
|---|---|---|
| C | 重写“维度树复原”主树，把 `literature_proposal_pool` 与 `practice_documentation_pool` 放在最前，通用六叶只保留为投影 | 当前虽有警告，但仍先给六个通用 leaf，容易再次被误读为原文树 |
| C | 删除或降级 `orig-rq2-language`、`orig-modeling-artifact`、`orig-tAM-user` 等非原生主干 | 原文 RQ2 是 goals/limitations，RQ3 是 metrics/users；TAM 只是 metric clustering 依据，不是独立样本编码主树 |
| C | 将样本单位从 “primary study / secondary study” 修正为 “modelling assistance proposal”；practice 侧补充 documented proposal / feature | 原文最终纳入对象是 proposals；不是 tertiary secondary studies |
| I | A.2 证据账本要从泛化 `not_verified` 改为具体锚点：§3.5 extraction、Table 2、Table 3、Table 4、Table 5、Fig.11--13、§7 threats | 现有 A.2 不能直接支撑字段级返修 |
| I | A.3 结论映射要拆成具体结论：样本单位、原生维度森林、五大字段、practice quote mapping、统计池资格、迁移边界 | 当前 C02--C07 仍是泛 leaf_definition |
| I | 关系边表需新增 proposal->strategy/goal/limitation/metric/user，GMQ tool->documented proposal，quote->S/G/L/M/U，cluster cross-tab | 当前只有 method-evidence、taxonomy-finding，太抽象 |
| I | SUMMARY 当前若记录“样本单位 / 样本数量 / 原生树类型 / 统计池资格”，应改为：样本单位=proposal；样本数量=58 literature + 15 practice proposals / 17 tools；原生树=维度森林；统计池=局部可统计 | 避免把 A1-DT schema seed 与原文统计资格混淆 |
| M | 保留 Table 3 “five limitations vs L1--L6” 口径风险 | 原文正文与表格不一致，正式统计前需人工裁决 |
| M | 补 PDF 核验记录：已用 `pdftotext -layout` 核对表格文本，但 Fig.4--15 视觉细节仍待人工核验 | 让证据等级清楚 |
| M | 保留 Zenodo replication package 未核验风险 | 原文 raw data 在 Zenodo，但本任务未读取，不可声称字段全集复现 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-A2-01 | `paper_content.txt`, `bibtex.bib`, `metadata.json` | Abstract / metadata | title, DOI, abstract | 系统映射 MDSE modelling assistants；58 proposals、17 tools | root_type | high | 原文类型、样本池 | 否 | 不支撑字段全集 |
| EV-A2-02 | `paper_content.txt` | §3.1 | MRQ/RQ1--RQ3 | MRQ 询问 literature/practice 中有哪些 modelling assistance proposals | rq_schema | high | RQ 与字段用途 | 否 | RQ 不是维度树本身 |
| EV-A2-03 | `paper_content.txt` | §3.2--3.3 | search strategy, I/E criteria | 五数据库 + snowballing；I1/I2/E1--E5 | selection_schema | high | source_record_chain, selection_schema | 否 | 不代表所有灰色文献 |
| EV-A2-04 | `paper_content.txt` | Table 1 / §3.4 | QA questionnaire | 10 项 3-point Likert quality assessment | quality_rubric | high | QA leaves | 已用 PDF 文本核对 | QA 只用于方法质量/seed |
| EV-A2-05 | `paper_content.txt` | §3.5 | Data extraction strategy | RQ1/RQ2/RQ3 分别抽 strategy、goals/limitations、metrics/users | extraction_form | high | 字段来源判定 | 否 | 未核验 Zenodo raw data |
| EV-A2-06 | `paper_content.txt`, `paper.pdf` | Table 2 / §4.2 | RQ1 clusters | Tools / Guidelines / Techniques / Methods / Frameworks / Languages | taxonomy | high | Strategy cluster | 已用 PDF 文本核对 | 单标签边界需 raw data |
| EV-A2-07 | `paper_content.txt`, `paper.pdf` | Table 3 / §4.3 | RQ2 clusters | G1--G7, L1--L6, L-NS | taxonomy | high | Goal/limitation leaves | 已用 PDF 文本核对 | five/six limitation 口径风险 |
| EV-A2-08 | `paper_content.txt`, `paper.pdf` | Table 4 / §4.4 | RQ3 clusters | M1/M2/M3/NE; U1/U2/U3/U-NS | taxonomy | high | Metric/user leaves | 已用 PDF 文本核对 | user cardinality 待 raw data |
| EV-A2-09 | `paper_content.txt`, `paper.pdf` | Table 5 / §5.2 | practice quote table | GMQ tool docs quote mapped to S/G/L/M/U | mapping_table | medium | Practice documentation pool | 已用 PDF 文本核对 | vendor 原网页未复核 |
| EV-A2-10 | `paper_content.txt`, `paper.pdf` | Fig. 5/6/11/12/13, §6 | cross analysis | strategy-goal-limitation, goal-metric-user, literature-practice | relation_edge | medium | 关系边与统计观察 | 是，图形视觉待核验 | 非因果关系 |
| EV-A2-11 | `paper_content.txt` | §7 | Threats to validity | selection、extraction、terminology、inter-rater、grey literature、language bias | limitation | high | 迁移边界 | 否 | 只支撑风险 |
| EV-A2-12 | `paper_content.txt` | §8 | Conclusions/future work | limitations/metrics/users 缺失；AI/LLM 是未来判断 | candidate_finding | medium | 候选 finding | 否 | 不可升级为 LLM4STM 事实 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CL-A3-01 | 本文是 systematic mapping + practice documentation review，不是 tertiary review 或 roadmap | paper_type | root | EV-A2-01, EV-A2-02 | high | 审计结论卡片 | practice review 不是完整灰色文献综述 |
| CL-A3-02 | 原生样本单位是 modelling assistance proposal；practice 侧是 documented proposal / feature | sample_unit | literature/practice pools | EV-A2-03, EV-A2-09 | high | SUMMARY 修正 | 记录层仍含 screened records 与 GMQ tools |
| CL-A3-03 | 原生维度树应复原为 proposal 编码维度森林，而不是六个通用接口 leaf | tree_type | native forest | EV-A2-05--EV-A2-10 | high | 重写 `review.md` 维度树 | 细粒度 cardinality 待 Zenodo |
| CL-A3-04 | RQ1 strategy 的封闭顶层枚举是六类 | leaf_definition | strategy cluster | EV-A2-06 | high | 叶子表 / schema seed | hybrid LLM systems 不宜强制单标签 |
| CL-A3-05 | RQ2 goal/limitation 是核心字段；limitations 缺失本身可统计 | leaf_definition | goal/limitation | EV-A2-07 | high | 叶子表 / candidate finding | Table 3 limitation 数量口径不一致 |
| CL-A3-06 | RQ3 metric/user 字段同时包含显式缺失码 NE 与 U-NS | leaf_definition | metric/user | EV-A2-08 | high | 缺失值语义 | metric 可多值，user cardinality 待复核 |
| CL-A3-07 | practice side 采用 quote-to-cluster mapping，可作为 documentation evidence pattern | mapping_pattern | practice pool | EV-A2-09 | medium | Paper2 evidence design | vendor 原始网页未复核 |
| CL-A3-08 | 原文统计观察可作 Paper2 schema_seed，但不可直接迁移为 LLM4STM 领域 finding | migration_boundary | all findings | EV-A2-10--EV-A2-12 | high | 迁移边界 | 需要跨论文证据与研究者裁决 |
| CL-A3-09 | 现有 `review.md` 需要返修，因为 v1/v2 口径、通用 leaf 与非原生主干仍混杂 | repair_needed | existing review | EV-A2-05--EV-A2-12 + `review.md` lines around 393--563 | high | 返修建议 | 不代表全文摘要部分都错误 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

| 文件 | 采用原则 |
|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | claim-evidence workflow；强结论必须有证据，缺证据则降级 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | reviewer-quality objection 要具体、可执行；关注 soundness、clarity、reproducibility |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | 用 needs evidence / weaken / remove 思路处理高风险结论 |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 先理解研究问题、方法、评价、风险，再结构化输出 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | 严格跟随原文方法与实验设置，不补造缺失细节 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | 用结构化 schema、task/risk 字段表达审计结果 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 完成标准必须 artifact/evidence-gated；不能因“看起来完成”停止 |

最高风险 3 点与复核方式：

1. 字段 cardinality 风险：goal、limitation、user 是否严格单标签，原文正文没有全部说清。合并时应读取 Zenodo raw data 或作者 supplementary。
2. PDF 图形风险：本次只用 `pdftotext -layout` 核对表格与图周边文字，未视觉核验 Fig. 4--15 的图形数值。合并时应人工打开 PDF。
3. Practice evidence 风险：Table 5 vendor quotes 未回原网页核验。合并时只能写“论文转录的公开文档证据”，不能写当前 vendor 状态。

blocked / timeout / 文件缺失：未出现 blocked；四个指定论文文件和七个技能文件均可读取；未修改仓库文件，未 commit，未 push，未调用 subagent。