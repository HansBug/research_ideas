# Large Language Models for Software Engineering: A Systematic Literature Review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Large Language Models for Software Engineering: A Systematic Literature Review |
| 作者 | Xinyi Hou; Yanjie Zhao; Yue Liu; Zhou Yang; Kailong Wang; Li Li; Xiapu Luo; David Lo; John Grundy; Haoyu Wang |
| 年份 / 出版日期 | 2024 / 2024-09-20；本地 PDF 为 arXiv v6 文本，页眉显示 2024-04-10 |
| DOI | <https://doi.org/10.1145/3695988> |
| 类型 | SLR |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [TOSEM](https://dl.acm.org/journal/tosem)；开放全文来自 arXiv PDF |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | A |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 阅读状态 | 已读 `bibtex.bib`、`metadata.json`、`paper_content.txt`；未逐页人工核对 `paper.pdf` 图表 |
| 证据等级 | 全文文本级；图表/表格精确数值、artifact 内容与最终 ACM 版本差异待复核 |
| 语料范围 | 2017 年至 2024-01-31；最终纳入 395 篇 LLM4SE 研究论文 |
| A1 角色 | 高相关 CCF-A LLM4SE SLR，用来抽取 SE SLR/SMS 的 field schema、artifacts、证据呈现与 threat pattern。 |
| 是否目标领域 evidence pool | 否。它只作为“软件工程二次研究如何建字段树和制品链”的模式样本，不能支撑 Paper2 目标领域 finding。 |
| 一句话结论 | 该文的核心价值不是某个 LLM4SE 结论，而是把 LLM4SE 拆成“模型类型—数据—优化/评价—SE 任务—挑战/路线图”的可审计字段树，并用 appendices/replication package 连接每个字段与 primary studies。 |

## 2. 全文内容详读

### 2.1 背景 / 问题设定

论文指出，已有 LLM4SE 相关综述要么只覆盖单一 SE 子任务（例如 testing、NL2Code、program repair），要么仍停留在 ML/DL for SE，不足以覆盖 ChatGPT、GPT-4、LLaMA 等新近 LLM 在 SE 中的扩散。作者因此按 Kitchenham 系统综述方法组织一篇覆盖 LLM、数据、优化/评价和 SE 应用任务的 SLR。

对 A1 来说，它最重要的 methodological signal 是：作者没有把 SLR 写成“论文列表”，而是预先定义了四个 RQ，每个 RQ 都对应一组可抽取字段，最后再把统计观察提升为 challenges、opportunities 和 roadmap。这正是 Paper2 的 A1-M0--M6 证据工程链条可借鉴的结构。

### 2.2 RQ1--RQ4

| RQ | 原文问题 | 抽取出的元维度 | 对 A1 的意义 |
|---|---|---|---|
| RQ1 | What LLMs have been employed to date to solve SE tasks? | LLM architecture、model family、parameter size、task fit、usage trend | 把“模型”从泛称拆成 encoder-only / encoder-decoder / decoder-only，并关联 SE 任务类型。 |
| RQ2 | How are SE-related datasets collected, preprocessed, and used in LLMs? | data source、data type、preprocessing、input representation | 把数据证据拆成 source/type/process/representation 四层，适合迁移为 Paper2 的字段树。 |
| RQ3 | What techniques are used to optimize and evaluate LLM4SE? | tuning、PEFT、prompt engineering、problem type、metrics | 同时抽取“优化策略”和“评价策略”，避免只统计模型性能。 |
| RQ4 | What SE tasks have been effectively addressed to date using LLM4SE? | SDLC activity、specific SE task、problem type、solution strategy | 用 SDLC 六阶段组织任务分布，并进一步按 generation/classification/recommendation/regression 分类。 |

### 2.3 语料范围：2017--2024

作者把检索起点设为 2017 年，理由是 Transformer 架构论文发表于 2017 年，是后续 LLM 的关键基础。截止日期为 2024-01-31。最终语料为 395 篇：质量评估后得到 382 篇，再经 forward/backward snowballing 补充 13 篇。

关键边界：该语料是 LLM4SE，而不是 SLR automation、agentic review、formal methods 或 LLM4STM。它可以作为“现代 SE SLR 如何构造分类轴”的样本，不能直接作为本仓库目标主题的证据池。

### 2.4 检索 / 筛选流程

作者使用 Quasi-Gold Standard（QGS）策略：

1. **Manual search**：选择 6 个顶级 SE venue：ICSE、ESEC/FSE、ASE、ISSTA、TOSEM、TSE；爬取 4,618 篇论文，人工确认 51 篇相关论文作为 QGS。
2. **Search string derivation**：从 QGS 和领域知识构造两组关键词：SE task keywords 与 LLM keywords。SE 关键词覆盖 code generation/search/completion/summarization、bug detection/localization、program repair、requirement extraction/traceability/validation、mining GitHub/SO/app 等；LLM 关键词覆盖 LLM、PLM、pre-trained、Transformer、BERT、Codex、GPT、T5、ChatGPT 等。
3. **Automated search**：在 IEEE Xplore、ACM Digital Library、ScienceDirect、Web of Science、Springer、arXiv、DBLP 七个数据库检索，初始获得 218,765 条候选。
4. **Filtering**：按少于 8 页、题名/摘要/关键词、venue 信息、去重、全文检查、workshop/doctoral symposium/grey literature 等条件逐级筛选。
5. **Quality assessment**：设置 10 个 QAC，覆盖 SE task relevance、LLM usage、是否二次研究、高声誉 venue、动机、技术描述、实验设置/数据、finding、贡献/限制、学术或工业贡献。正式出版论文按 21 分满分，arXiv 按 18 分满分，阈值均为 80%。
6. **Snowballing**：对 382 篇初始集合做 backward/forward snowballing，获得 3,964 + 9,610 条线索，去重后 5,152 条，再筛选补入 13 篇。

可迁移点：QGS 不只是检索技巧，也是一种 A1-M1 脚手架构造方式——先由高置信 venue 构造关键词与候选 schema，再扩展到数据库与 snowballing。

待注意：正文对 QAC3 “not a secondary study” 与“retained systematic views/survey/review papers for assessment”的表述存在潜在歧义；正式引用其筛选规则前应回 PDF/replication package 核对。

### 2.5 数据抽取

Table 5 将抽取字段直接绑定到 RQ：

- SE task category。
- LLM category。
- LLM characteristics and applicability。
- data handling techniques。
- weight training algorithms and optimizer。
- evaluation metrics。
- SE activity。
- developed strategies and solutions。

这是本文最适合 Paper2 复用的做法：每个字段都要说明服务哪个 RQ，而不是为“信息完整”机械抽取。

### 2.6 分类维度与主要结果

#### RQ1：LLM 类型与趋势

作者采用 encoder-only、encoder-decoder、decoder-only 三分法。encoder-only 主要服务理解类任务，如 code understanding、bug localization、vulnerability detection；encoder-decoder 同时服务理解与生成，如 code summarization、code translation、program repair；decoder-only 更适合生成类任务，如 code generation、code completion、test case generation。

主要发现：395 篇中出现 70+ 种 LLM；decoder-only 成为最常用架构。2020 年研究主要集中于 encoder-only；2021--2022 开始多样化；2023 年 decoder-only 显著占优；2024 年 1 月样本中 decoder-only 仍是中心，但 encoder-decoder 和 encoder-only 仍有探索空间。

#### RQ2：数据来源、类型、预处理与输入形式

作者把数据来源分成四类：

1. open-source datasets。
2. collected datasets。
3. constructed datasets。
4. industrial datasets。

其中 open-source datasets 最常见；显式说明 dataset 的 374 篇中约 62.83% 使用开源数据。industrial datasets 只有 6 篇，作者据此指出学术数据与工业真实场景之间可能错位。

数据类型分成五类：text-based、code-based、graph-based、software repository-based、combined。Table 7/Appendix A 进一步细到 programming tasks/problems、prompts、Stack Overflow posts、bug reports、requirements documentation、source code、buggy code、patches、test suites/cases、code repository、issues/commits、pull requests 等。

预处理方面，文本数据流程包括 data extraction、initial segmentation、unqualified data deletion、text preprocessing、duplicated instance deletion、tokenization、segmentation；代码数据流程包括 extraction、unqualified deletion、duplicate deletion、compilation、uncompilable deletion、code representation、segmentation。

输入形式分为 token-based、tree/graph-based、pixel-based、hybrid。token-based 占绝对多数：在 355 篇明确 input form 的研究中约 97.75% 使用 token-based input；tree/graph、pixel、hybrid 仍很少。

#### RQ3：优化与评价

优化策略包括 full fine-tuning、ICL、PEFT、prompt engineering 等。PEFT 进一步包括 LoRA、prompt tuning、prefix tuning、adapter tuning；此外还有 RL、SFT、syntax fine-tuning、knowledge preservation fine-tuning、task-oriented fine-tuning。

Prompt engineering 被整理为八类：few-shot、zero-shot、Chain-of-Thought、Automatic Prompt Engineer、Chain of Code、Automatic Chain-of-Thought、Modular-of-Thought、Structured Chain-of-Thought。另有 76 篇研究虽未落入上述名称，但仍进行了 prompt strategy / prompt design。

评价指标按 problem type 组织：

- regression：MAE。
- classification：Precision、Recall、F1、Accuracy、AUC、ROC、FPR、FNR、MCC。
- recommendation：MRR、Precision@k、MAP@k、F-score@k、Recall@k、Accuracy。
- generation：BLEU、Pass@k、Accuracy@k、Exact Match、CodeBLEU、ROUGE、METEOR、Edit Similarity 等。

这里的可迁移点是：评价字段不应直接绑定具体任务，而应先绑定 problem type，再允许 task-specific metric。

#### RQ4：SE 任务分布

作者按 SDLC 将 SE 任务分为六类：requirements engineering、software design、software development、software quality assurance、software maintenance、software management。研究分布高度不均：software development 约 56.65%，software maintenance 约 22.71%，software quality assurance 约 15.14%，requirements engineering 约 3.90%，software design 约 0.92%，software management 约 0.69%。按问题类型看，generation 约 70.97%，classification 约 21.61%，recommendation 约 6.77%，regression 约 0.65%。

Table 10/Appendix E 总结了 85 个具体 SE task。高频任务包括 code generation、program repair、code completion、code summarization、test generation、vulnerability detection 等；requirements engineering 中有 anaphoric ambiguity treatment、requirements classification、requirement analysis/evaluation、specification generation、traceability automation、specification formalization、use case generation；software quality assurance 中出现 verification，但数量很少。

对本仓库特别重要的观察：需求、设计、形式化规格、验证等与控制系统状态机建模更接近的环节，在这篇 LLM4SE SLR 中属于低占比区域。因此它可以支持“field schema 需要覆盖 under-explored phases”的模式判断，但不能支持“LLM4STM 已被充分研究”的结论。

### 2.7 Artifacts 做法

论文多次声明 replication package / artifacts 公开可得，并在正文给出 GitHub 链接。`paper_content.txt` 中摘要和 threats footnote 指向 `https://github.com/xinyi-hou/LLM4SE_SLR`；`metadata.json` 的 abstract 则记录 `https://github.com/security-pride/LLM4SE_SLR`。该 URL 差异需要后续联网核对。

就文本内容看，artifact 至少承载以下类型：

1. selected primary studies list。
2. 每篇研究使用的 LLM 与参数规模。
3. Appendix A--E 的字段到 primary-study references 映射：data types、input forms、prompt engineering、evaluation metrics、SE tasks。
4. 支撑复核的 replication package。

对 Paper2 的启发：appendix 不只是补充材料，而是 field schema 的 source-anchor 层。后续我们自己的字段树也应能从 summary table 跳到单篇论文和原文锚点。

### 2.8 Threats

作者报告三类 threats：

1. **Paper search omission**：关键词不完备可能遗漏相关论文；缓解方式是 manual search + automated search + backward/forward snowballing。
2. **Study selection bias**：BibTeX/metadata 不完整、自动筛选误判、人工判断主观性；缓解方式包括保留无法确定排除的论文进入人工阶段、邀请两名 SE/LLM 领域 reviewers 做 secondary review，并提供 replication package。
3. **Empirical knowledge bias**：395 篇论文需要人工理解和归类，作者经验可能影响 RQ 与分类；缓解方式是参考 DL4SE 等前序综述，并在回答每个 RQ 前先读相关文献预定义分类。

A1 额外风险判断：其 threat 报告比普通 survey 更规范，但仍没有完全暴露每个字段的 coder agreement、冲突解决日志、schema revision history。Paper2 若主打 audit-first，应在这些过程证据上比它更强。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 四个 RQ 按“对象模型—数据—优化/评价—应用任务”展开，形成完整 field schema。 | Section 2.1；RQ1--RQ4。 | 可迁移为 Paper2 的 A1-M0 综述元模型设计范式。 | RQ 内容是 LLM4SE 特有，不能迁移为目标领域结论。 |
| dimension pattern | 核心维度包括 LLM architecture、dataset source/type/preprocessing/input form、tuning/prompt/eval metric、SDLC activity、problem type、specific task。 | Table 5；Sections 3--6；Appendix A--E。 | 高度可迁移为字段树。 | 取值空间偏 code-centric，对状态机/形式化方法需重新扩展。 |
| finding pattern | 从频次与趋势推导出 decoder-only 占优、industrial data 缺口、token input 主导、RE/design/management 低覆盖、evaluation limitations。 | RQ summaries；Section 8。 | 可迁移为“统计观察 -> gap/challenge/opportunity”的 finding 生成方式。 | 这些 finding 属于 LLM4SE，不是 Paper2 目标领域 finding。 |
| evidence presentation pattern | 使用 QGS 流程图、筛选分母、QAC 表、RQ-field 表、分布图、分类表、appendix reference lists、replication package。 | Fig. 1--10；Table 2--17；Appendix A--E。 | 非常适合迁移为审计优先证据呈现模板。 | 本轮未 PDF 核对图表版式；精确数值引用需复核。 |
| validity / threat pattern | threats 分为 search omission、selection bias、empirical knowledge bias，并逐项写缓解措施。 | Section 7。 | 可迁移为 Paper2 的 threat skeleton。 | 对 coder agreement、schema drift、artifact rot 的显式处理不足。 |
| report structure pattern | Introduction / Approach / RQ1--RQ4 / Threats / Challenges & Opportunities / Roadmap / Conclusion；每个 RQ 末尾都有 summary。 | 全文目录与章节。 | 可迁移为“方法--RQ结果--威胁--路线图”的 SLR 报告结构。 | Paper2 是方法论文，不能照搬为纯领域 SLR 结构。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式 | 说明 |
|---|---|---|
| A1-M0 主题与综述元模型设定 | 用 RQ 明确综述对象、数据、优化/评价和任务边界。 | 证明高质量 SE SLR 会先设定可执行元模型，而不是边读边自由摘要。 |
| A1-M1 脚手架挖掘与种子探测 | QGS：顶级 venue manual search -> 51 篇种子 -> search strings。 | 可作为“从高置信种子构造初始 schema/keyword”的脚手架策略。 |
| A1-M2 维度模式准备与批准 | Table 5 将 data items 绑定到 RQ。 | 可迁移为字段合同：每个字段必须服务某个 RQ，并定义最低证据。 |
| A1-M3 论文收集与概览 | 218,765 初始候选 -> 多阶段筛选 -> 382 + 13 -> 395。 | 可迁移为检索分母、排除原因、全文状态、质量阈值的概览卡。 |
| A1-M4 字段级证据抽取与模式演化 | Appendix A--E 把字段取值与 primary-study references 连接。 | 可迁移为 source-anchor 表；但原文未充分暴露 schema revision trail。 |
| A1-M5 统计分析 | 按年份、venue、architecture、dataset、input form、prompt、metric、SE activity 做分布分析。 | 可迁移为字段表上的频次/趋势/交叉统计，而非直接生成结论。 |
| A1-M6 候选发现形成 | Section 8 将统计缺口组织成 challenges、opportunities、roadmap。 | 可迁移为 candidate finding ledger：统计观察先变成候选发现，再由研究者裁决。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

本字段树覆盖用户指定的 **LLM类型、SE任务、数据、优化/评价策略** 等核心维度；英文 ID 仅用于后续机器可读字段命名。

```text
review_record
├── bibliographic_source
│   ├── title / authors / year / venue / DOI
│   ├── publication_type / CCF_category / CCF_rank
│   └── fulltext_status / artifact_url / version_note
├── search_and_selection
│   ├── search_scope_start_end
│   ├── seed_venues / QGS_size
│   ├── databases / query_keyword_families
│   ├── inclusion_criteria / exclusion_criteria
│   ├── screening_counts_by_stage
│   └── quality_assessment_criteria / threshold / reviewer_check
├── LLM类型 llm_type
│   ├── architecture: encoder-only | encoder-decoder | decoder-only
│   ├── model_family: BERT | CodeBERT | T5 | CodeT5 | GPT | Codex | ChatGPT | LLaMA | ...
│   ├── parameter_size_declared
│   ├── general_vs_code_specialized
│   ├── hosted_vs_open_or_reproducible
│   └── task_fit: understanding | generation | understanding+generation
├── SE任务 se_task
│   ├── sdlc_activity: requirements | design | development | QA | maintenance | management
│   ├── specific_task: code_generation | program_repair | requirements_classification | verification | ...
│   ├── problem_type: generation | classification | recommendation | regression
│   ├── input_artifact_type
│   └── output_artifact_type
├── 数据 data
│   ├── source_category: open_source | collected | constructed | industrial
│   ├── data_type: text | code | graph | repository | combined
│   ├── concrete_artifact: source_code | bug_report | requirements_doc | tests | patch | prompt | ...
│   ├── preprocessing_steps
│   ├── representation: token | tree_graph | pixel | hybrid
│   ├── split_and_benchmark
│   └── privacy_or_industrial_constraints
├── 优化/评价策略 optimization_and_inference
│   ├── full_fine_tuning
│   ├── PEFT: LoRA | prompt_tuning | prefix_tuning | adapter_tuning
│   ├── prompt_strategy: zero_shot | few_shot | CoT | APE | CoC | Auto_CoT | MoT | SCoT | custom
│   ├── RL_or_SFT_or_task_specific_training
│   └── feedback_loop_or_tool_integration
├── evaluation
│   ├── benchmark_or_dataset
│   ├── baseline_models_or_tools
│   ├── metric_family_by_problem_type
│   ├── human_eval_or_manual_validation
│   ├── statistical_or_ablation_analysis
│   └── limitations_of_metrics
├── evidence_and_artifacts
│   ├── table_or_figure_anchor
│   ├── primary_study_reference_anchor
│   ├── replication_package_url
│   ├── appendix_mapping
│   └── extraction_uncertainty
└── finding_ledger
    ├── distribution_observation
    ├── trend_observation
    ├── gap_or_underexplored_area
    ├── challenge
    ├── opportunity
    └── roadmap_or_action_recommendation
```

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **字段树优先于摘要生成**：该文最强的做法是 Table 5 + Appendix A--E，把综述问题、抽取字段、取值表和 primary-study anchors 连成一条链。
2. **QGS 可作为 A1-M1 scaffold pattern**：先用高置信 venue 形成 QGS，再派生 query strings，比直接在数据库中堆关键词更适合审计。
3. **field schema 应服务 RQ**：每个字段都应解释它支撑哪个 RQ；Paper2 可用这一点约束 agent 不做无目的摘录。
4. **结果章节可按 RQ 分段，每段末尾保留 summary**：这有利于从统计观察过渡到候选 finding。
5. **appendix 是证据链，不是剩余材料**：后续 Paper2 的字段证据表、source anchors、artifact links 应像该文 appendices 一样成为可审计资产。
6. **under-explored phase 是重要 finding 类型**：本文通过 SDLC 分布识别 RE/design/management 低覆盖；Paper2 可借鉴这种“覆盖不均 -> 研究缺口”的候选发现模式。
7. **roadmap 要从统计缺口推出**：Section 8 的 challenges/opportunities/roadmap 可作为 A1-M6 candidate finding 的写法样本。

### 6.2 风险

1. **不能把它当目标领域 evidence pool**：它是 LLM4SE SLR，不是 LLM4STM、控制系统状态机、formal verification 或 agentic SLR 目标语料。
2. **时间漂移很强**：截止到 2024-01-31，且 LLM4SE 之后发展极快；任何“当前最新模型/任务格局”都必须重新核验。
3. **arXiv 占比高**：395 篇中大量是 arXiv，虽有质量评估，但不能简单等价为 peer-reviewed evidence。
4. **工业数据覆盖弱**：industrial datasets 仅少量出现，工业/安全关键系统外推需要降级。
5. **字段审计过程不足**：文章公开了 replication package，但正文未充分展示每个字段的双人编码、一致性、冲突解决和 schema drift 记录；Paper2 若主打 audit-first，应补强这部分。
6. **代码中心偏置**：分类轴高度围绕 code generation/repair/testing，对 requirements formalization、system design、state machine modeling、formal verification 的取值空间不足。
7. **artifact URL 有差异**：本地 metadata 与 paper text 的 GitHub 链接不同，不能在正式写作中不核验就引用。

## 7. 待复核

1. 人工打开 `paper.pdf` 核对 Fig. 1、Table 2--17、Appendix A--E 的版式和精确数值，尤其是数据库分项命中数与 task count 语义。
2. 核对 ACM final version 与 arXiv v6 的差异：本地 PDF 页眉 DOI 仍显示占位格式，但 `bibtex.bib` / `metadata.json` 已有正式 DOI。
3. 联网核验 replication package 的真实 URL、可访问性、license、文件结构，以及 `xinyi-hou/LLM4SE_SLR` 与 `security-pride/LLM4SE_SLR` 的关系。
4. 复核 QAC3 与二次研究纳排规则是否存在版本/表述歧义。
5. 若要在 Paper2 正文引用精确比例，应回到 PDF 或 artifact 表格确认分母：例如 374 篇显式说明 dataset、355 篇显式说明 input form、software development 的 paper count 与 task-instance count 差异。
6. A2a 若把该文纳入 `survey_of_surveys` 总账，应同步回填 `target_se_subfield=LLM4SE`、`challenge_action_pattern`、`artifact_anchor_pattern`，但不得改写为目标领域 finding。

## 维度树复原

### 一句话结论

本文的维度树主类型为“大规模 RQ 驱动分类树”，辅助类型为“LLM4SE task-method-evidence 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-llm4se-systematic-review-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-llm4se-systematic-review-source-schema-candidates]

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-llm4se-systematic-review-root] | Large Language Models for Software Engineering 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-llm4se-systematic-review-b1] 综述范围与研究问题；[dim-llm4se-systematic-review-b2] 语料收集与纳排；[dim-llm4se-systematic-review-b3] 主题 / 对象分类；[dim-llm4se-systematic-review-b4] 方法 / 技术 / 干预；[dim-llm4se-systematic-review-b5] 评价、统计与候选发现 | [ev-llm4se-systematic-review-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-llm4se-systematic-review-root] Large Language Models for Software Engineering
├── [dim-llm4se-systematic-review-b1] 综述范围与研究问题
│   └── [leaf-llm4se-systematic-review-scope] 研究范围与单位对象
├── [dim-llm4se-systematic-review-b2] 语料收集与纳排
│   └── [leaf-llm4se-systematic-review-corpus] 语料与纳排链条
├── [dim-llm4se-systematic-review-b3] 主题 / 对象分类
│   └── [leaf-llm4se-systematic-review-taxonomy] 主题与维度分类
├── [dim-llm4se-systematic-review-b4] 方法 / 技术 / 干预
│   └── [leaf-llm4se-systematic-review-method] 方法 / 技术 / 干预分类
└── [dim-llm4se-systematic-review-b5] 评价、统计与候选发现
    └── [leaf-llm4se-systematic-review-evidence] 评价、证据与复现资产
    └── [leaf-llm4se-systematic-review-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-llm4se-systematic-review-scope] | 研究范围与单位对象 | [dim-llm4se-systematic-review-b1] | 定义 LLM4SE 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-scope] |
| [leaf-llm4se-systematic-review-corpus] | 语料与纳排链条 | [dim-llm4se-systematic-review-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-corpus] |
| [leaf-llm4se-systematic-review-taxonomy] | 主题与维度分类 | [dim-llm4se-systematic-review-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-taxonomy] |
| [leaf-llm4se-systematic-review-method] | 方法 / 技术 / 干预分类 | [dim-llm4se-systematic-review-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-method] |
| [leaf-llm4se-systematic-review-evidence] | 评价、证据与复现资产 | [dim-llm4se-systematic-review-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-evidence] |
| [leaf-llm4se-systematic-review-finding] | 统计观察与候选发现 | [dim-llm4se-systematic-review-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm4se-systematic-review-leaf-finding] |

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-llm4se-systematic-review-orig-se-task] | [dim-llm4se-systematic-review-b1] | 软件工程任务 | 需求、设计、编码、测试、维护、项目管理、教育等 SE 生命周期任务。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-llm4se-systematic-review-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-llm4se-systematic-review-orig-llm-method] | [dim-llm4se-systematic-review-b2] | LLM 方法与模型 | 模型家族、prompting、fine-tuning、RAG、agent、tool use、workflow。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-llm4se-systematic-review-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-llm4se-systematic-review-orig-dataset-benchmark] | [dim-llm4se-systematic-review-b3] | 数据集与基准 | 任务数据、benchmark、评价集、开源状态和许可。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-llm4se-systematic-review-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-llm4se-systematic-review-orig-metric] | [dim-llm4se-systematic-review-b4] | 评价指标 | 正确性、效率、人工评价、安全、鲁棒性、可复现性等指标。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-llm4se-systematic-review-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-llm4se-systematic-review-orig-limitation-risk] | [dim-llm4se-systematic-review-b5] | 限制与风险 | 幻觉、泛化、数据泄漏、成本、隐私、伦理和工业可用性。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-llm4se-systematic-review-002, EV-llm4se-systematic-review-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/llm4se-systematic-review__codex.md)、[claude](../../audits/a1dt-19x3/results/llm4se-systematic-review__claude.md)、[deepseek](../../audits/a1dt-19x3/results/llm4se-systematic-review__deepseek.md)。 [clm-llm4se-systematic-review-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-llm4se-systematic-review-orig-rq1-model] | RQ1 模型与任务格局 | LLM 模型家族、参数规模、prompt/fine-tuning/RAG/agent/tool use | LLM4SE 方法 taxonomy seed | 快速漂移需标日期 | 核对 RQ1 表 |
| [dim-llm4se-systematic-review-orig-rq2-data] | RQ2 数据收集与预处理 | 数据源、dataset、benchmark、input/output form、preprocessing、license/open status | data/artifact schema seed | 数据集报告缺失单列 | 核对 RQ2 和 extracted items |
| [dim-llm4se-systematic-review-orig-rq3-optimization-eval] | RQ3 优化与评价 | prompting、fine-tuning、evaluation metric、baseline、human eval、robustness、cost | evaluation seed | 指标和任务分母分开 | 核对 RQ3 表 |
| [dim-llm4se-systematic-review-orig-rq4-se-task] | RQ4 软件工程任务 | requirements、design、coding、testing、maintenance、management、education 等任务树 | SE task taxonomy seed | 代码中心偏置需记录 | 核对 RQ4 taxonomy |
| [dim-llm4se-systematic-review-orig-extraction-qgs] | 抽取字段与质量门 | Table 5 extracted data items、QGS、QAC、纳排标准、二次研究排除 | 质量和字段合同 seed | QAC 分数需精核 | 核对 Table 5 和 quality criteria |
| [dim-llm4se-systematic-review-orig-artifact-trend] | 复现资产、限制与趋势 | replication package、arXiv 占比、工业数据、limitations、future trend | candidate finding 和风险 seed | 链接和版本需核验 | 核对 artifact 链接、discussion、threats |

#### 三路审计综合返修结论

| 审计共同问题 | 本轮返修动作 | 剩余风险 |
|---|---|---|
| 原先主树过度依赖六个通用接口叶子，容易把跨论文投影误读成原文 schema。 | 将原文 RQ、抽取字段、分类项、质量 rubric、关系边、统计表或 roadmap action 抬升为上表主干，并把通用接口降级为后文投影。 | 上表仍是 `schema_seed`，需 A2a 精确核对页码、表号、图号和附录。 |
| 原文显式取值空间未完全进入叶子层。 | 在“叶子 / 取值空间种子”中列出封闭枚举、层级枚举、数值分母、关系值或自由文本边界。 | 取值空间是否封闭、是否饱和、是否可统计，需要 A2a 逐项判定。 |
| 统计观察、候选发现和最终 finding 容易混层。 | 统计用途列显式保留 `schema_seed`、候选 finding 和不得进入当前 SUMMARY 定量统计的边界。 | final research finding 仍必须等跨论文证据、反证和研究者裁决。 |

#### 审计返修口径

- 本节吸收 `codex`、`claude`、`deepseek` 三路全文审计的共同结论：原文 schema 主树必须优先于跨论文通用接口层；通用接口只做投影，不再冒充原文叶子全集。
- 本节只完成 A1-DT 结构化返修；凡未补齐精确页码、表号、图号或 supplementary 定位的节点均保持 `schema_seed` / `not_verified`，并作为 A2a 精核入口。
- 若三路审计之间存在细节差异，后续 A2a 以原文 PDF、`paper_content.txt`、附录和复现实验包为准，并在 A.3 中新增替代结论或废弃旧结论。
#### 通用接口投影

下表只用于把原文 schema 主树投影到跨论文统一接口，不能替代上表成为原文事实源。

| 通用接口 | 在本文中的投影对象 | 使用边界 |
|---|---|---|
| 研究范围与单位对象 | `RQ landscape` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
| 语料与纳排链条 | 与检索、纳排、样本分母、方法流程相关的原文主干。 | 无系统检索的 roadmap / vision 需写不适用。 |
| 主题与维度分类 | 原文 taxonomy、classification schema、concept model 或 roadmap action 分类。 | 必须保留原文取值空间，不得压成泛词。 |
| 方法 / 技术 / 干预分类 | 原文 method / tool / intervention / agent role / guideline stage。 | 方法学 guideline 不得误写成目标领域方法效果。 |
| 评价、证据与复现资产 | 原文 quality、metric、artifact、replication、validity、evidence table。 | 弱证据或未核验链接不得进入统计。 |
| 统计观察与候选发现 | 原文 result / discussion / gap / recommendation / action point。 | 只能作 candidate finding，需研究者裁决。 |

#### 返修后仍需 A2a 精核

1. 将上表每个原文主干拆成更细叶子，并为每个叶子补具体页码、表号 / 图号、段落或附录定位。
2. 核对取值空间是否是原文封闭枚举、层级枚举、数值 / 分母、关系值，还是只能自由文本。
3. 若三路审计意见冲突，以原文证据为准，并在 A.3 新增替代结论或废弃旧结论。

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-llm4se-systematic-review-method-evidence] | [leaf-llm4se-systematic-review-method] | 支撑 / 度量 | [leaf-llm4se-systematic-review-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-llm4se-systematic-review-taxonomy] | [clm-llm4se-systematic-review-edge-method-evidence] |
| [edge-llm4se-systematic-review-taxonomy-finding] | [leaf-llm4se-systematic-review-taxonomy] | 导出候选发现 | [leaf-llm4se-systematic-review-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-llm4se-systematic-review-stat] | [clm-llm4se-systematic-review-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-llm4se-systematic-review-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-llm4se-systematic-review-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-llm4se-systematic-review-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-llm4se-systematic-review-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | LLM4SE 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-llm4se-systematic-review-transfer] |
| [leaf-llm4se-systematic-review-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-llm4se-systematic-review-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-llm4se-systematic-review-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-llm4se-systematic-review-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-llm4se-systematic-review-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-llm4se-systematic-review-001 | [ev-llm4se-systematic-review-root] | [src-llm4se-systematic-review-text], [src-llm4se-systematic-review-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-llm4se-systematic-review-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-llm4se-systematic-review-002 | [ev-llm4se-systematic-review-taxonomy] | [src-llm4se-systematic-review-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-llm4se-systematic-review-b1], [dim-llm4se-systematic-review-b2], [dim-llm4se-systematic-review-b3], [dim-llm4se-systematic-review-b4], [dim-llm4se-systematic-review-b5], [leaf-llm4se-systematic-review-taxonomy], [leaf-llm4se-systematic-review-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-llm4se-systematic-review-003 | [ev-llm4se-systematic-review-stat] | [src-llm4se-systematic-review-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-llm4se-systematic-review-evidence], [leaf-llm4se-systematic-review-finding], [leaf-llm4se-systematic-review-orig-se-task], [leaf-llm4se-systematic-review-orig-llm-method], [leaf-llm4se-systematic-review-orig-dataset-benchmark], [leaf-llm4se-systematic-review-orig-metric], [leaf-llm4se-systematic-review-orig-limitation-risk] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-llm4se-systematic-review-004 | [ev-llm4se-systematic-review-risk] | [src-llm4se-systematic-review-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-llm4se-systematic-review-root], [leaf-llm4se-systematic-review-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-llm4se-systematic-review-005 | [ev-llm4se-systematic-review-relation] | [src-llm4se-systematic-review-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边；本行在 A1-DT 仅作关系边 seed，待 A2a 精确页码 / 表图核验后才能升级。 | taxonomy | not_verified | [edge-llm4se-systematic-review-method-evidence], [edge-llm4se-systematic-review-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-llm4se-systematic-review-tree-type] | A1DT-llm4se-systematic-review-C01 | 本文的维度树主类型为“大规模 RQ 驱动分类树”，辅助类型为“LLM4SE task-method-evidence 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-llm4se-systematic-review-tree-type] | tree_type | [dim-llm4se-systematic-review-root] | EV-llm4se-systematic-review-001, EV-llm4se-systematic-review-004 | 树型判断仅限本文，不代表所有 LLM4SE 综述。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-scope] | A1DT-llm4se-systematic-review-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-scope] | EV-llm4se-systematic-review-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-corpus] | A1DT-llm4se-systematic-review-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-corpus] | EV-llm4se-systematic-review-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-taxonomy] | A1DT-llm4se-systematic-review-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-taxonomy] | EV-llm4se-systematic-review-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-method] | A1DT-llm4se-systematic-review-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-method] | EV-llm4se-systematic-review-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-evidence] | A1DT-llm4se-systematic-review-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-evidence] | EV-llm4se-systematic-review-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-leaf-finding] | A1DT-llm4se-systematic-review-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm4se-systematic-review-finding] | EV-llm4se-systematic-review-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-transfer] | A1DT-llm4se-systematic-review-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-llm4se-systematic-review-root] | EV-llm4se-systematic-review-002, EV-llm4se-systematic-review-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-finding-boundary] | A1DT-llm4se-systematic-review-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-llm4se-systematic-review-finding] | EV-llm4se-systematic-review-003, EV-llm4se-systematic-review-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |
| [clm-llm4se-systematic-review-edge-method-evidence] | A1DT-llm4se-systematic-review-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-llm4se-systematic-review-method-evidence] | EV-llm4se-systematic-review-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-edge-taxonomy-finding] | A1DT-llm4se-systematic-review-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-llm4se-systematic-review-taxonomy-finding] | EV-llm4se-systematic-review-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | weak | candidate_finding | false | -- |
| [clm-llm4se-systematic-review-source-schema-candidates] | A1DT-llm4se-systematic-review-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-llm4se-systematic-review-orig-se-task], [leaf-llm4se-systematic-review-orig-llm-method], [leaf-llm4se-systematic-review-orig-dataset-benchmark], [leaf-llm4se-systematic-review-orig-metric], [leaf-llm4se-systematic-review-orig-limitation-risk] | EV-llm4se-systematic-review-002, EV-llm4se-systematic-review-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-llm4se-systematic-review-a1dt-19x3-repair] | A1DT-llm4se-systematic-review-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-llm4se-systematic-review-root] | EV-llm4se-systematic-review-002, EV-llm4se-systematic-review-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-llm4se-systematic-review-structure-check] | [dim-llm4se-systematic-review-root], A1DT-llm4se-systematic-review-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-llm4se-systematic-review-visual-check] | EV-llm4se-systematic-review-002, EV-llm4se-systematic-review-003, EV-llm4se-systematic-review-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
