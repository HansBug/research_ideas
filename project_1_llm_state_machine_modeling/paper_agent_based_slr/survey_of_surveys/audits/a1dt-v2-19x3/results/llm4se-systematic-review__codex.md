### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm4se-systematic-review` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已按全文结构通读 79 页文本抽取内容，重点复核 Approach、RQ1--RQ4、Threats、Challenges/Roadmap、Appendix A--E。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；用于核对题名、作者、DOI、TOSEM 元信息、本地全文状态和 eligibility 字段。 |
| 是否打开或核对 `paper.pdf` | 是；使用 `pdfinfo` 确认 PDF 79 页，并用 `pdftotext -layout` 局部核对 Fig. 1、Table 2--5、Table 7--17、Appendix A--E 的版面与表头。未做逐页人工视觉截图核验。 |
| 原文类型 | SLR |
| 被编码样本单位 | LLM4SE primary study / research paper；最终纳入 395 篇，部分字段允许一篇论文有多个取值或任务实例。 |
| 样本数量 / 分母 | 395 篇总样本；质量评估后 382 篇 + snowballing 追加 13 篇。若字段缺失，作者使用局部分母，例如 dataset source 明示 374 篇、input form 明示 355 篇。 |
| 原生树类型 | 维度森林：RQ 驱动的多棵分类/统计树，核心为“LLM 模型—数据—优化/评价—SE 任务”，并辅以检索/质量门与 challenges/roadmap。 |
| 主统计池资格 | 局部可统计。可进入“系统综述如何构造字段树/统计表”的方法学统计池；不得作为 Paper2 目标领域 final finding 或 LLM4STM 领域事实池直接使用。 |
| 总体判定 | needs repair。论文原文本身证据充分；现有 `review.md` 仍混有通用六叶投影、v1 历史审计入口和过宽迁移表述，需要按本文原生字段森林重写。 |

### 1. 原文证据阅读说明

实际读取文件：

- `bibtex.bib`：确认正式题名、TOSEM、2024、DOI `10.1145/3695988`。
- `metadata.json`：确认 slug、PDF URL、摘要、全文状态、`eligible_for_schema_seed=true`、`eligible_for_statistical_synthesis=true`。
- `paper_content.txt`：全文 4152 行，覆盖摘要、Introduction、Approach、RQ1--RQ4、Threats、Challenges/Opportunities/Roadmap、Conclusion、References、Appendix A--E。
- `review.md`：全文 440 行，作为返修对象读取。
- `paper.pdf`：用 `pdfinfo` 和 `pdftotext -layout` 做有限版面核验；确认 79 页，核对 Fig. 1、Table 5、Appendix 表格存在并与文本抽取一致。

仍需 PDF 视觉核验的部分：复杂图形的精确布局、Fig. 4/5/10 的图中数值、最终 ACM 版本与本地 arXiv v6 的 DOI/页眉差异、Appendix 参考编号是否有排版错位。

关键原文证据锚点：

1. 摘要：作者称选择并分析 395 篇、回答四个 RQ，定义本文为 LLM4SE SLR。
2. Section 2.1：四个 RQ 分别对应 LLM、dataset、optimization/evaluation、SE task。
3. Fig. 1 / Section 2.2：QGS manual search、automated search、snowballing 与多阶段筛选链。
4. Table 3：纳入/排除标准，包括 full text、LLM used、SE task、非短文、非灰色文献等。
5. Table 4：10 个 QAC，前 3 个为相关性门，后 7 个为质量分。
6. Section 2.4：382 篇作为 snowballing 初始集，追加 13 篇，最终 395 篇。
7. Table 5：抽取字段与 RQ 的直接映射，是维度树根证据。
8. RQ1 / Fig. 4 / Table 6：LLM 架构三分法及其适合任务。
9. RQ2 / Table 7--8 / Appendix A--B：数据来源、数据类型、预处理、输入形式。
10. RQ3 / Fig. 9 / Table 9 / Appendix C--D：调优、prompt engineering、problem type 到 metric 的映射。
11. RQ4 / Fig. 10 / Table 10 / Appendix E：SDLC 六阶段、85 个 SE task、problem type 分布。
12. Section 7--8：threats、challenges、opportunities、roadmap，属于候选 finding 层，不是原始编码字段本体。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 LLM4SE research papers / primary studies。虽然 Table 1 比较了既有 surveys，但正式编码对象不是 secondary study，而是 395 篇 LLM 用于 SE 任务的研究论文。
2. 作者有系统检索、纳排、质量评估和数据抽取方案。检索采用 QGS：6 个顶级 SE venue 形成 51 篇种子，再派生关键词，覆盖 7 个数据库，最后用 snowballing 补充。纳排见 Table 3，质量评估见 Table 4，抽取字段见 Table 5。
3. 原文字段来源主要是 extraction form / classification schema / appendix mapping，而不是 discussion 自由总结。Table 5 是抽取字段总表；Fig. 4--10 与 Table 6--10 是结果统计表；Appendix A--E 将字段取值映射到 study references。
4. RQ 不是树根本身，而是字段用途和结果组织方式。真正根对象是 “included LLM4SE study”；RQ1--RQ4 分别驱动模型、数据、优化评价、SE 任务四棵子树。
5. 不需要降级为 roadmap/proposal。本文有系统样本库与可统计字段；但 Section 8 的 roadmap/challenges 只能作为候选 finding 或方法学启发，不能进入主编码树叶子统计。

### 3. 原生样本编码维度树 / 维度森林

```text
included_llm4se_study  395 篇 LLM4SE primary studies
├── study_selection_and_quality
│   ├── source_channel: manual_search | automated_database | snowballing
│   ├── venue_or_database: ICSE | ESEC/FSE | ASE | ISSTA | TOSEM | TSE | IEEE | ACM | ScienceDirect | WoS | Springer | arXiv | DBLP
│   ├── publication_year: 2020 | 2021 | 2022 | 2023 | Jan-2024
│   ├── publication_venue_type: peer_reviewed | arXiv
│   ├── inclusion_exclusion_status: included | excluded_by_short_page | duplicate | non_peer_review | workshop | grey | non_English | no_LLM_technique | SE4LLM_not_LLM4SE
│   └── QAC_score: relevance gates QAC1--QAC3 + quality score QAC4--QAC10
├── RQ1_llm_model
│   ├── llm_architecture: encoder-only | encoder-decoder | decoder-only
│   ├── llm_family_or_application: BERT | CodeBERT | T5 | CodeT5 | GPT-* | ChatGPT | Codex | LLaMA | StarCoder | ...
│   ├── parameter_size_declared: declared numeric/free text | not_declared
│   └── task_fit: understanding | understanding_and_generation | generation
├── RQ2_dataset_and_input
│   ├── dataset_source: open-source | collected | constructed | industrial | not_specified
│   ├── dataset_type_category: text-based | code-based | graph-based | software-repository-based | combined
│   ├── concrete_data_type: programming problems | prompts | bug reports | requirements docs | source code | patches | GUI images | issues/commits | ...
│   ├── text_preprocessing_step: extraction | initial segmentation | unqualified deletion | text preprocessing | duplicate deletion | tokenization | segmentation
│   ├── code_preprocessing_step: extraction | unqualified deletion | duplicate deletion | compilation | uncompilable deletion | representation | segmentation
│   └── input_form: token-based | tree/graph-based | pixel-based | hybrid
├── RQ3_optimization_and_evaluation
│   ├── tuning_technique: full fine-tuning | ICL | PEFT | RL | SFT | syntax fine-tuning | knowledge preservation fine-tuning | task-oriented fine-tuning
│   ├── PEFT_subtype: LoRA | prompt tuning | prefix tuning | adapter tuning
│   ├── prompt_engineering: few-shot | zero-shot | CoT | APE | CoC | Auto-CoT | MoT | SCoT | others
│   ├── problem_type: regression | classification | recommendation | generation
│   └── metric: MAE | Precision | Recall | F1 | Accuracy | AUC | MRR | MAP@k | BLEU | Pass@k | CodeBLEU | ROUGE | ...
├── RQ4_se_task
│   ├── se_activity: requirements engineering | software design | software development | software quality assurance | software maintenance | software management
│   ├── specific_se_task: 85 task labels, e.g. code generation, program repair, verification, specification formalization
│   ├── task_count_or_study_count: numeric # studies, often multi-label
│   └── developed_strategy_or_solution: free-text summary with exemplars for selected high-frequency tasks
└── synthesis_layer
    ├── statistical_observation: distribution/trend/frequency/cross-field observation
    ├── challenge: applicability | generalizability | evaluation | interpretability/trust/ethics
    ├── opportunity: code-specialized LLM | ChatGPT influence | task-specific training | collaborative LLMs | new input forms | under-explored SE phases | domain-specific data | evaluation framework
    └── roadmap_action: coding assistance | testing/analysis | programming knowledge | code review/QA | data mining | predictive analytics | software security | SE4LLM
```

缺失部分与 A2a 精核任务：完整叶子全集很大，尤其是 Fig. 4 的 70+ model labels、Appendix A 的全部 data type references、Appendix E 的 85 个任务 references。A2a 应逐表固化页码、表号、分母、是否多标签、是否允许同一论文重复计数。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 来源渠道 | study_selection_and_quality | Fig. 1 / Sec. 2.2--2.4 | 样本来自 manual、automated 或 snowballing。 | manual search、automated search、snowballing | 完整枚举 | 不适用；流程级字段 | 记录检索分母与来源闭环 | QGS 方法学启发 | Fig. 1 | 可迁移检索设计，不迁移 LLM4SE 结论 |
| L2 | 数据库/venue | study_selection_and_quality | Table 2 / Sec. 2.2.2 | manual venues 和 automated databases。 | 6 venues + 7 databases | 完整枚举 | 未命中则无记录 | 覆盖范围统计 | 识别检索覆盖风险 | Table 2, Sec. 2.2.2 | 需按目标领域重配 venue/database |
| L3 | 纳排状态 | study_selection_and_quality | Table 3 | 论文是否满足 inclusion/exclusion。 | 3 inclusion + 9 exclusion criteria | 完整枚举 | 无 full text 则排除 | 筛选审计 | 纳排偏差分析 | Table 3 | 可迁移 criteria 形式，不迁移阈值 |
| L4 | QAC 质量分 | study_selection_and_quality | Table 4 / Sec. 2.3.2 | 研究相关性与质量评分。 | QAC1--3: -1/0/1；QAC4--10: 0/1/2/3；阈值 80% | 数值/等级 | QAC1--3 为 -1 则直接排除 | 质量过滤 | 质量门设计 seed | Table 4 | QAC3 与 retained surveys 表述需复核 |
| L5 | 发表形态 | study_selection_and_quality | Fig. 2 / Sec. 2.5 | peer-reviewed venue 或 arXiv。 | peer-reviewed、arXiv | 完整枚举 | 不明确则待核验 | venue 分布 | arXiv 占比风险 | Fig. 2 | 不代表证据强度完全等价 |
| L6 | 年份 | study_selection_and_quality | Fig. 2 | 纳入研究年份分布。 | 2020, 2021, 2022, 2023, Jan 2024 | 数值/时间 | 检索窗外不纳入 | 趋势统计 | 时间漂移风险 | Fig. 2 | LLM 快速变化，必须标截止日 |
| L7 | LLM 架构 | RQ1_llm_model | Fig. 4 / Table 6 | 被研究 LLM 的架构类别。 | encoder-only、encoder-decoder、decoder-only | 完整枚举 | 未能归类则待核验 | 架构频次/趋势 | 模型选择模式 | Fig. 4, Table 6 | 具体模型时效性强 |
| L8 | LLM 家族/应用 | RQ1_llm_model | Fig. 4 / repo claim | 具体模型或 LLM-based application。 | BERT、CodeBERT、GPT-4、ChatGPT、Codex、LLaMA 等 70+ | 层级枚举 | 未声明则 not_declared | 模型使用频次 | 识别主流模型与长尾 | Fig. 4 | 需更新到当前模型生态 |
| L9 | 参数规模 | RQ1_llm_model | Sec. 3.1 / repo claim | 论文声明的模型参数规模。 | 数值/free text；not_declared | 数值或自由文本 | 未声明为 not_declared | 模型规模分析 | 部署成本/可复现风险 | Sec. 3.1 | 原文说 repo 包含参数，正文未完整列出 |
| L10 | 架构任务适配 | RQ1_llm_model | Table 6 | 架构与 SE task 类型的适配。 | understanding、understanding+generation、generation | 关系值 | 无任务映射则待核验 | 架构-任务关系 | 模型选择启发 | Table 6 | 不是因果效果证明 |
| L11 | 数据来源 | RQ2_dataset_and_input | Fig. 6 / Sec. 4.1 | training/evaluation dataset 的来源策略。 | open-source、collected、constructed、industrial、not_specified | 完整枚举 + 缺失类 | 未说明训练数据，尤其 hosted LLM，记 not_specified | 数据来源频次 | 工业数据缺口 | Fig. 6, RQ2 summary | 不可推出目标领域数据可得性 |
| L12 | 数据类型大类 | RQ2_dataset_and_input | Table 7 / Appendix A | dataset 内容类型。 | text-based、code-based、graph-based、software repository-based、combined | 完整枚举 | 未报告 dataset type 则待核验 | 数据类型统计 | multimodal/graph 缺口 | Table 7, Table 13 | 多标签计数需保留分母 |
| L13 | 具体数据类型 | RQ2_dataset_and_input | Table 7 / Table 13 | 细粒度 dataset artifact。 | programming problems、prompts、requirements docs、source code、patches、issues/commits 等 | 层级枚举 | 不明确则待核验 | 细粒度频次 | 目标领域 artifact seed | Table 13 | 代码中心偏置强 |
| L14 | 文本预处理步骤 | RQ2_dataset_and_input | Fig. 7 / Sec. 4.3 | text-based dataset preprocessing pipeline。 | extraction、initial segmentation、unqualified deletion、text preprocessing、duplicate deletion、tokenization、segmentation | 层级/流程枚举 | 顺序可变；未用文本数据则不适用 | 流程模式 | 数据清洗规范 seed | Fig. 7 | 不应当成所有任务必备顺序 |
| L15 | 代码预处理步骤 | RQ2_dataset_and_input | Fig. 8 / Sec. 4.3 | code-based dataset preprocessing pipeline。 | extraction、unqualified deletion、duplicate deletion、compilation、uncompilable deletion、representation、segmentation | 层级/流程枚举 | 未用代码数据则不适用 | 流程模式 | 代码数据审计 seed | Fig. 8 | 状态机/形式化模型需另设流程 |
| L16 | 输入形式 | RQ2_dataset_and_input | Table 8 / Appendix B | LLM input representation。 | token-based、tree/graph-based、pixel-based、hybrid | 完整枚举 | 仅 355 篇明示 input form；其他 not_reported | input form 分布 | 非 token 表示缺口 | Table 8, Table 14 | 保留局部分母 355 |
| L17 | 调优技术 | RQ3_optimization_and_evaluation | Sec. 5.1 | 提升 LLM 性能的调优方式。 | full fine-tuning、ICL、PEFT、RL、SFT、syntax fine-tuning、knowledge preservation、task-oriented | 层级枚举 | 无调优则 none/not_reported | 方法频次 | 低成本优化启发 | Sec. 5.1 | 效果强弱需回 primary study |
| L18 | PEFT 子类 | RQ3_optimization_and_evaluation | Sec. 5.1 | PEFT 的具体方式。 | LoRA、prompt tuning、prefix tuning、adapter tuning | 完整枚举 | 非 PEFT 则不适用 | PEFT 分类 | 轻量化调优 seed | Sec. 5.1 | 不可直接迁移性能结论 |
| L19 | Prompt 技术 | RQ3_optimization_and_evaluation | Fig. 9 / Appendix C | prompt engineering 分类。 | few-shot、zero-shot、CoT、APE、CoC、Auto-CoT、MoT、SCoT、Others | 完整枚举 + Others | 未显式命名但设计 prompt 归 Others | prompt 频次 | prompt taxonomy seed | Fig. 9, Table 15 | Others 需二级拆分 |
| L20 | 问题类型 | RQ3/RQ4 bridge | Fig. 10 / Table 9 | SE task 被归为哪类 prediction/generation problem。 | regression、classification、recommendation、generation | 完整枚举 | 不适用或不明确则待核验 | metric 选择分母 | metric 设计启发 | Fig. 10, Table 9 | 不是任务领域分类 |
| L21 | 评价指标 | RQ3_optimization_and_evaluation | Table 9 / Appendix D | 各 problem type 常用 metrics。 | MAE、Precision、Recall、F1、Accuracy、AUC、MRR、MAP@k、BLEU、Pass@k、CodeBLEU、ROUGE 等 | 层级枚举 | 未报告 metric 则 not_reported | metric 频次 | 综合评价框架缺口 | Table 9, Table 16 | 指标适用性需任务语义复核 |
| L22 | SE 活动 | RQ4_se_task | Fig. 10 / Table 10 | SDLC 六阶段。 | requirements engineering、software design、software development、software quality assurance、software maintenance、software management | 完整枚举 | 不属于六类则 Others/待核验 | 生命周期覆盖分布 | under-explored phase finding | Fig. 10, Table 10 | 只支撑 LLM4SE 覆盖格局 |
| L23 | 具体 SE 任务 | RQ4_se_task | Table 10 / Appendix E | 85 个具体任务标签。 | code generation、program repair、verification、specification formalization 等 85 项 | 层级枚举 | 未明确任务则待核验 | task 频次 | 目标任务候选 seed | Table 17 | 需保留多标签计数语义 |
| L24 | 策略/解决方案 | RQ4_se_task | Sections 6.2--6.7 / Tables 11--12 | 对部分任务的代表性模型、benchmark、metric、findings。 | 自由文本 + 表格字段 | 自由文本加理由/关系值 | 未展开任务只列 Others | 案例说明，不宜主统计 | 方法模式启发 | Tables 11--12, Sec. 6 | 不能代替 primary-study 证据 |
| L25 | Challenge 类别 | synthesis_layer | Sec. 8.1 | 作者从结果讨论出的挑战。 | applicability、generalizability、evaluation、interpretability/trust/ethics | 层级枚举 | 非编码字段，无缺失语义 | 不进入样本字段统计 | candidate finding | Sec. 8.1 | discussion 层，需降级 |
| L26 | Roadmap action | synthesis_layer | Sec. 8.3 | 作者给出的未来路线。 | automated coding、testing/analysis、programming knowledge、QA、data mining、predictive analytics、security、SE4LLM | 开放枚举 | 非系统编码字段 | 不进入 primary study 统计 | 方法学启发 | Sec. 8.3 | roadmap 不是已验证结论 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | RQ | drives_extraction | Data item | Table 5 的 8 个抽取项 | 无 RQ 绑定则不应作为正式抽取字段 | Table 5 | 建立字段服务 RQ 的合同 |
| E2 | included_study | has_llm_architecture | LLM 架构 | encoder-only / encoder-decoder / decoder-only | 未归类则待核验 | Fig. 4, Table 6 | 架构频次和趋势 |
| E3 | LLM 架构 | suitable_for | 任务能力类型 | understanding / understanding+generation / generation | 非效果证明 | Table 6 | 模型选择关系 seed |
| E4 | included_study | uses_dataset_source | 数据来源 | open-source / collected / constructed / industrial / not_specified | hosted LLM 或未说明记 not_specified | Fig. 6 | 数据来源统计 |
| E5 | dataset_type_category | has_concrete_data_type | 具体数据类型 | Appendix A 的细粒度类型 | 未报告 dataset type 则待核验 | Table 7, Table 13 | 数据 artifact 层级树 |
| E6 | data_type | requires_preprocessing_step | 预处理步骤 | text/code 两套七步流程 | 顺序可变；非该数据类型则不适用 | Fig. 7, Fig. 8 | 数据处理 schema seed |
| E7 | included_study | uses_input_form | 输入形式 | token / tree-graph / pixel / hybrid | 仅 355 篇明示，其他 not_reported | Table 8, Table 14 | 输入表示统计 |
| E8 | optimization_method | has_subtype | PEFT 子类 | LoRA / prompt tuning / prefix tuning / adapter tuning | 非 PEFT 则不适用 | Sec. 5.1 | 优化技术层级 |
| E9 | included_study | uses_prompt_technique | prompt 分类 | 8 类 + Others | 未显式名但有 prompt design 可归 Others | Fig. 9, Table 15 | prompt 统计 |
| E10 | SE task | mapped_to_problem_type | 问题类型 | regression / classification / recommendation / generation | 不明确则待核验 | Fig. 10, Table 9 | metric 选择前置分类 |
| E11 | problem_type | uses_metric | 评价指标 | Table 9/16 metrics | 未报告 metric 则 not_reported | Table 9, Table 16 | 指标分类与统计 |
| E12 | SE activity | contains | specific SE task | Appendix E 的 85 个任务 | 未归类任务需待核验 | Table 10, Table 17 | SDLC 任务树 |
| E13 | statistical_observation | motivates | challenge/opportunity | Section 8 类别 | discussion 层，非字段抽取 | Sec. 8 | 候选 finding 链 |
| E14 | challenge/opportunity | suggests | roadmap_action | Section 8.3 action labels | 作者观点，不代表已验证 | Sec. 8.3 | 迁移为写作启发 |

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段/统计表支持的统计观察：

- 最终纳入 395 篇，其中 382 篇来自质量评估后集合，13 篇来自 snowballing。
- 154 篇在 peer-reviewed venues，241 篇在 arXiv；2023 年样本显著增多，2024 年仅覆盖 1 月。
- RQ1：模型按 encoder-only、encoder-decoder、decoder-only 三类；decoder-only 在近年占主导。
- RQ2：dataset source 中 open-source 最多，industrial dataset 很少；dataset type 中 text/code 为主；input form 中 token-based 占绝大多数，但分母是 355 篇明示 input form 的研究。
- RQ3：PEFT 与 prompt engineering 被明确分类；evaluation metrics 按 regression/classification/recommendation/generation 组织。
- RQ4：SE 活动以 software development、maintenance、quality assurance 为主；requirements/design/management 覆盖低。具体任务中 code generation 和 program repair 是高频项。

原文 discussion / recommendation / roadmap 提出的候选 finding：

- LLM4SE 需要处理模型部署成本、数据依赖、代码生成歧义、泛化、评价、可解释性/可信/伦理。
- under-explored phases 包括 requirements engineering、software design、software management。
- 未来路线包括更综合的评价框架、更多输入形式、domain-specific datasets、formal analysis/formal verification 结合、SE4LLM。

对 Paper2 可迁移的方法学启发：

- 用 RQ 驱动 extraction form，而不是先套通用六叶模板。
- 用 QGS 构造检索种子，再派生关键词并 snowballing。
- 字段表应记录分母、局部分母、多标签语义和 reference anchors。
- Appendix 可以作为字段取值到 primary studies 的证据账本。
- final finding 应从“统计观察 → candidate finding → 反证/边界 → 研究者裁决”生成。

绝不能迁移的领域结论：

- 不能把 “decoder-only 主导 LLM4SE” 迁移成 LLM4STM 或控制系统状态机建模的模型选择结论。
- 不能把 “token-based input 占 97.75%” 迁移成形式化模型/状态机任务的最佳输入形式。
- 不能把 “industrial datasets 仅 6 篇” 迁移成目标领域工业数据结论，除非目标语料重复验证。
- 不能把 “requirements/design/verification 低覆盖” 直接写成 Paper2 目标领域缺口，只能作为重新检索的提示。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | `review.md` 仍保留“六个通用 leaf 是跨论文接口层”的大段内容，虽然有警告，但版面上仍容易被当作原文树。 | 将六叶接口整体移到“通用投影附录”，正文维度树只保留本文原生 `included_llm4se_study` 维度森林。 |
| C | “历史草稿”“v1-deprecated”“19×3 审计”混入单篇事实源，违反本任务 v2 不以旧 v1 审计作模板的口径。 | 删除或降级为返修来源说明；A.2/A.3 必须重新用本文原文证据填充。 |
| C | 原文主树目前仍是粗略 6 行，不足以复原 Table 5、Table 13--17 的叶子字段。 | 重写“维度树复原”，至少包含 selection/quality、RQ1 model、RQ2 dataset/input、RQ3 optimization/evaluation、RQ4 SE task、synthesis layer。 |
| I | `review.md` 把主统计池资格写得偏保守，容易混淆“不能进入目标领域 finding”与“不能统计原文 schema”。 | 修正为“局部可统计”：原文字段和统计可用于 survey schema pool；目标领域结论不可直接迁移。 |
| I | 当前 A.2 证据账本多为 `not_verified` 泛行，未指向具体 Table 5、Fig. 6、Table 13--17。 | 新增逐表证据：Table 5、Fig. 1、Table 3/4、Fig. 4/Table 6、Fig. 6/Table 7/8、Fig. 9/Table 9、Fig. 10/Table 10、Appendix A--E。 |
| I | 关系边只列 `method-evidence` 和 `taxonomy-finding`，过粗。 | 增加 RQ→data item、task→problem type→metric、SE activity→SE task、dataset type→concrete data type 等关系边。 |
| I | 对局部分母处理不足。 | 明确 395 总分母、374 dataset-source 分母、355 input-form 分母，并标注多标签计数可能导致 task totals 不等于 paper count。 |
| M | artifact URL 在 metadata 与 paper text 不一致。 | 在待复核中保留 URL 差异，正式引用前联网核验。 |
| M | `QAC3` 与 “retained systematic views/survey/review papers” 存在表述张力。 | 在 A.2 记录为证据限制；必要时查 replication package。 |
| M | SUMMARY 表字段建议修正。 | `样本单位=LLM4SE primary study/research paper`；`样本数量=395`；`原生树类型=维度森林/RQ-driven classification forest`；`统计池资格=局部可统计，目标领域 finding 禁用`。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | `paper_content.txt`, `paper.pdf` | Abstract | Page 1 摘要 | 选择并分析 395 篇，回答四个 RQ | 根对象/样本量 | strong | included_llm4se_study, sample_count | 否 | 只支撑本文 SLR 样本 |
| EV02 | `paper_content.txt`, `paper.pdf` | 2.1 Research Questions | RQ1--RQ4 | 四个 RQ 覆盖 LLM、dataset、optimization/evaluation、SE task | RQ 组织 | strong | RQ-driven forest | 否 | RQ 是字段用途，不是叶子全集 |
| EV03 | `paper_content.txt`, `paper.pdf` | 2.2 Search Strategy | Fig. 1 | QGS、automated search、snowballing、多阶段筛选 | 检索流程 | strong | study_selection_and_quality | 是 | 图中数据库命中数需最终版核对 |
| EV04 | `paper_content.txt`, `paper.pdf` | 2.2.1 / 2.3.1 | Table 2 / Table 3 | 6 个 manual venues；3 个 inclusion、9 个 exclusion | 范围与纳排 | strong | source_channel, venue, inclusion_exclusion | 否 | 不直接迁移为目标领域 venue 表 |
| EV05 | `paper_content.txt`, `paper.pdf` | 2.3.2 | Table 4 | QAC1--QAC10 与评分阈值 | 质量门 | medium | QAC_score | 否 | QAC3 表述需复核 |
| EV06 | `paper_content.txt`, `paper.pdf` | 2.4 / 2.5 | snowballing + Fig. 2 | 382 + 13 = 395；154 peer-reviewed，241 arXiv | 样本分母/发表分布 | strong | sample_count, venue_type, year | 是 | arXiv 不等于同行评审 |
| EV07 | `paper_content.txt`, `paper.pdf` | 2.5 | Table 5 | 抽取 data items 与 RQ 对齐 | extraction form | strong | all main branches | 否 | 当前最关键原生 schema 证据 |
| EV08 | `paper_content.txt`, `paper.pdf` | 3 / RQ1 | Fig. 4 / Table 6 | LLM 架构三分法与任务适配 | 模型分类 | strong | LLM architecture/family/task_fit | 是 | 模型列表时效性强 |
| EV09 | `paper_content.txt`, `paper.pdf` | 4 / RQ2 | Fig. 6 / Table 7 / Table 8 | 数据来源、类型、输入形式 | 数据字段 | strong | dataset_source/type/input_form | 是 | dataset/source 有局部分母 |
| EV10 | `paper_content.txt`, `paper.pdf` | 4.3 | Fig. 7 / Fig. 8 | text/code preprocessing steps | 流程字段 | medium | preprocessing steps | 是 | 顺序可变，不是必备流程 |
| EV11 | `paper_content.txt`, `paper.pdf` | 5 / RQ3 | Fig. 9 / Table 9 | prompt 技术与 metrics by problem type | 优化/评价字段 | strong | prompt, problem_type, metric | 是 | metric 适用性需按任务判断 |
| EV12 | `paper_content.txt`, `paper.pdf` | 6 / RQ4 | Fig. 10 / Table 10 | SDLC 六阶段、85 个 SE tasks | 任务分类 | strong | se_activity, specific_se_task | 是 | task totals 可能多标签 |
| EV13 | `paper_content.txt`, `paper.pdf` | Appendix A--E | Tables 13--17 | 字段取值、# Studies、References | reference mapping | strong | concrete leaves and anchors | 是 | 需 A2a 固化全部页码/编号 |
| EV14 | `paper_content.txt`, `paper.pdf` | 7 Threats | 三类 threat | search omission、selection bias、empirical knowledge bias | validity boundary | strong | migration boundary | 否 | 只支撑风险，不支撑字段频次 |
| EV15 | `paper_content.txt`, `paper.pdf` | 8 Challenges/Roadmap | 8.1--8.3 | challenges、opportunities、roadmap | candidate finding | medium | synthesis_layer | 否 | discussion 层，不能当 final finding |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是有系统样本库的 LLM4SE SLR，最终纳入 395 篇研究论文。 | paper_type/sample | included_llm4se_study | EV01, EV03, EV06 | strong | 审计结论卡片、SUMMARY 样本字段 | 本地 PDF 为 arXiv v6，正式 DOI 版需最终核对 |
| C02 | 本文原生维度结构是 RQ 驱动的维度森林，不是单一六叶模板。 | tree_type | RQ-driven forest | EV02, EV07 | strong | 重写 `review.md` 维度树 | 六叶接口只能作投影 |
| C03 | Table 5 是本文字段抽取合同的核心证据。 | schema_source | extraction form | EV07 | strong | A.2/A.3 与叶子表 | Table 5 是粗粒度字段，细叶需 Appendix |
| C04 | RQ1 的模型字段包括架构、模型家族/应用、参数规模声明和任务适配。 | leaf_definition | RQ1_llm_model | EV08 | medium | schema seed / 局部统计 | 参数规模主要在 repo 声称，正文未完整列出 |
| C05 | RQ2 的数据字段包括来源、类型、预处理流程和输入形式。 | leaf_definition | RQ2_dataset_and_input | EV09, EV10, EV13 | strong | schema seed / 局部统计 | input form 分母是 355，不是 395 |
| C06 | RQ3 把优化技术与评价指标分开，并通过 problem type 组织 metrics。 | relation/schema | RQ3_optimization_and_evaluation | EV11 | strong | evaluation schema seed | metrics 频次不等于指标质量 |
| C07 | RQ4 按 SDLC 六阶段组织 85 个 SE task。 | taxonomy | RQ4_se_task | EV12, EV13 | strong | task taxonomy seed | 多标签和 task-instance 语义需保留 |
| C08 | 本文可作为方法学/字段树统计池样本，但不能作为 Paper2 目标领域 final finding。 | migration_boundary | whole paper | EV14, EV15 | strong | SUMMARY 统计池资格 | LLM4SE 与 LLM4STM/状态机建模主题不同 |
| C09 | Section 8 的 challenges/opportunities/roadmap 应作为 candidate finding 或启发，而不是原始编码字段。 | finding_boundary | synthesis_layer | EV15 | medium | Paper2 写作启发 | 作者 discussion，非逐项 extraction form |
| C10 | 现有 `review.md` 需要返修，因为通用六叶和历史 v1 审计内容仍干扰原生树。 | repair_need | existing review.md | EV02, EV07, EV13 + review.md | strong | 返修计划 | 不表示已有 review 全部错误，只是事实源层级需重排 |

### 9. 技能使用与自我审查记录

已读取的技能/指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence workflow、证据门、reviewer gate。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer 视角，优先指出 soundness、reproducibility、claim support 风险。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 rejection-risk audit、claim/evidence gap、revision priority。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解研究上下文、再输出结构化计划/风险的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“不编造不明确细节、明确 UNCLEAR”的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化 schema、task/risk 字段化表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated completion 思路；本任务禁止启动 autoresearch 或任何 agent，因此只吸收“验证证据存在才算完成”的原则。

本输出最高风险 3 点：

1. Appendix A--E 叶子全集过大，本报告只列核心叶子和代表性取值。主线程合并时应逐表补全全部 85 个 SE task、全部 metric 和全部 data type。
2. PDF 核验是 `pdftotext -layout` 局部核验，不是逐页人工视觉核验。正式 `review.md` 若引用精确图中比例，应再用 PDF 视觉核对。
3. QAC3 与原文“retained systematic views/survey/review papers”存在潜在张力。合并时应查 replication package 或作者 artifact，确认 secondary study 是否最终进入 395。

blocked / timeout / 文件缺失：未出现 blocked、timeout 或指定文件缺失。未修改仓库文件，未 commit，未 push，未调用 subagent。