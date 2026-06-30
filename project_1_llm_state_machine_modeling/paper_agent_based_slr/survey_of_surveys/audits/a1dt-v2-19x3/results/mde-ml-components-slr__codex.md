### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `mde-ml-components-slr` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是。已按全文顺序分块阅读 2123 行，并用 `rg`/`nl` 回查关键证据锚点。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib` 确认为 Naveed et al., IST 2024；`metadata.json` 确认为 DOI、PDF URL、SLR 类型与本地全文状态。 |
| 是否打开或核对 `paper.pdf` | 是。用 `pdfinfo` 确认 PDF 22 页，并渲染/视觉核对第 7 页，重点核对 Fig. 5 特征树与 Fig. 6 分布；未逐表核验全部图表数值。 |
| 原文类型 | SLR |
| 被编码样本单位 | 46 篇 primary studies，编号 P1--P46。 |
| 样本数量 / 分母 | 自动检索 3934 条，去重后 3570 条，三轮筛选到 32 篇，snowballing 增补 14 篇，最终 46 篇；结论节另写 3496，疑似与方法节不一致，需保留为风险。 |
| 原生树类型 | 维度森林：以 Fig. 5 “MDE Solution for ML” 特征树为核心，外加 Google Form 5 个 section / 40 个问题驱动的 RQ1--RQ4 字段森林。 |
| 主统计池资格 | 局部可统计。原文自身可对 46 篇 primary studies 做字段统计；迁移到 Paper2 时只能作为 schema/method pattern，MDE4ML 领域结论不得进入主统计池。 |
| 总体判定 | needs repair。原文证据足够，但现有 `review.md` 仍混入六叶通用接口和 v1 历史审计痕迹，需要重写原生维度树与 A.2/A.3。 |

### 1. 原文证据阅读说明

已读取本地 `bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。PDF 层面做了局部版面核验：确认 PDF 页数，并打开第 7 页核对 Fig. 5 特征树、Fig. 6 Venn 图和 Table 2 周边；没有逐页核验 Fig. 7--10、Table 3--9 的所有数值，因此涉及全量数值表时仍需 A2a PDF 精核。

关键证据锚点：

1. 摘要 Method：作者按 Kitchenham 指南做 SLR，7 个数据库检索得到 3934 papers，最终 46 篇进入 data extraction / synthesis。
2. §3 Research methodology：流程分 planning / conducting / reporting；第一作者执行检索和筛选，其他作者 cross-validation，最终 46 篇 primary studies。
3. §3.1 RQ1--RQ4：四个 RQ 分别面向 motivation、MDE approaches/tools、evaluation、limitations/future work。
4. §3.2 Table 1：纳排标准排除了 AI4MDE、secondary/tertiary studies、vision、grey literature、opinion、comparison papers 等。
5. §3.3.2--3.3.4：3934 → 3570 → 72 → 55 → 32，再 snowballing +14。
6. §3.4 Data extraction：Google Form 有 40 questions，分 5 sections，题型包括 short answer、long answer、checkbox、radio button。
7. §3.5 Quality assessment：QA1--QA5，1--5 分；QA3--QA5 对无 evaluation 的论文标 NA；19/46 good、15/46 average、12/46 poor。
8. §4.1 / PDF Fig. 5：特征树来自 RQ-based data extraction categories；根为 “MDE Solution for ML”。
9. §4.2 Table 3--6：RQ1 的 goals、ML techniques、end users、contributions 是逐 primary study 编码字段。
10. §4.3 Fig. 8--9 / Table 7--8：RQ2 编码 modeling、ML aspects、tool support、transformation、generated artifacts 等。
11. §4.4 Fig. 10：RQ3 编码 evaluation context/method、ML/MDE metrics、datasets，并区分 not mentioned 与 N/A。
12. §4.5 / §6：RQ4 的 limitations/future work 进入统计，Discussion 再升级为 roadmap/recommendations。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 primary study，不是 tool、dataset、claim 或 roadmap action。每个样本以 P1--P46 标识，Appendix A 给出完整引用，Appendix B 给出 QA 分数。

2. 作者有系统检索、纳排、数据抽取和编码方案。证据包括 7 个数据库、明确 search string、Table 1 纳排标准、三轮筛选、snowballing、40 问 Google Form、QA1--QA5 与 threats to validity。

3. 字段来源主要是 extraction form 与 Fig. 5 feature tree。可观察字段来自：Google Form 5 sections、Fig. 5、Table 3--8、Fig. 6--10、Appendix B。质量字段来自 QA rubric。Discussion roadmap 不是原始抽取表，但由统计观察解释生成。

4. RQ 不是维度树根本身，而是字段用途和结果组织方式。RQ 驱动 extraction form sections；Fig. 5 才是显式特征树；RQ Answer Summary 是统计综合输出。

5. 本文不是无系统样本库，不需要降级为 roadmap/proposal。但迁移到 Paper2 时必须降级 MDE4ML 领域结论：只能迁移“如何构造字段树、统计观察和候选 finding”的方法学启发。

### 3. 原生样本编码维度树 / 维度森林

原文没有完整公开 40 个问题清单，因此以下为“核心主干 + 可从正文/表图确认的代表性叶子”。缺失的完整问题文本、字段题型细节、原始 coding sheet 需 A2a 检查数据仓库。

```text
Primary Study Record: P1--P46
├── General information / publication trends
│   ├── title / authors / venue / citation count [自由文本 / 数值；Google Form section 1]
│   ├── publication year [数值；Fig. 4]
│   ├── publication type: conference / journal / workshop [完整枚举；Fig. 4]
│   └── QA1--QA5 score: 1--5 / NA [数值枚举；Appendix B]
├── RQ1 Motivation / goal / context / outcome
│   ├── goal: effort reduction / quality improvement / stakeholder understanding [层级多选；Table 3]
│   ├── sub-goal: abstraction, automation, integration, monitoring, system management, data management, reusability, etc. [层级枚举；Table 3]
│   ├── ML technique: generic / supervised / unsupervised / reinforcement; supervised 下分 traditional / neural networks / both [层级枚举；Table 4]
│   ├── application domain: CPS, manufacturing, autonomous vehicles, analytics, social bots, generic, etc. [自由文本归类；§4.2.3]
│   ├── end user: ML-related roles / software & systems roles / other roles [层级多选；Table 5]
│   └── contribution: code generator, text generator, model generator, DSL, framework, model, modeling approach, extension, etc. [层级多选；Table 6]
├── RQ2 MDE solution and tool support
│   ├── model representation: textual / graphical / both [完整枚举；Fig. 5/Fig. 8]
│   ├── modeling language: GPL / DSL / language extension [完整枚举；Fig. 5/Fig. 8]
│   ├── model level: CIM / PIM / PSM [多选枚举；§4.3.1]
│   ├── model type: requirements / design / data-representation / feature / process / deployment [层级枚举；§4.3.1]
│   ├── supported ML aspects: requirements, preprocessing, design/development, training, evaluation, deployment, integration, inference, monitoring, management, data generation/storage/visualization, documentation, pipeline, knowledge base [层级多选；§4.3.2]
│   ├── ML framework/library: TensorFlow, MXNet, PyTorch, Weka, Scikit-learn, etc. [开放受控列表；Table 7]
│   ├── transformation: M2T / M2M / both; forward engineering [完整枚举 + 布尔事实；§4.3.3]
│   ├── generated artifact: ML/training code, models, deployment config, dataset/subset, text, API, rules, meta-model [层级多选；§4.3.3]
│   ├── generated language: Python / Java / C++ / other [开放受控列表；Fig. 9]
│   ├── automation level: full / partial [完整枚举；Fig. 5/Fig. 8]
│   └── tool/meta-tool availability: open-source / proprietary / no tool mentioned; EMF, Sirius, XTend, etc. [枚举 + 外部工具名；§4.3.3/Table 8]
├── RQ3 Evaluation
│   ├── evaluation context: academia / industry / both [完整枚举；§4.4.1]
│   ├── evaluation method: case study / experiment / survey / criteria-based assessment / no evaluation [多选枚举；§4.4.2]
│   ├── ML metrics: classification / regression / time-resource / fairness / not mentioned / N/A [层级枚举；Fig. 10]
│   ├── MDE metrics: quality / time-resource / code / not mentioned / N/A [层级枚举；Fig. 10]
│   └── dataset: MNIST, Iris, other named datasets [开放列表；§4.4.3]
└── RQ4 Limitations and future work
    ├── limitation category: approach / evaluation / solution quality / not mentioned [多选枚举 + 缺失值语义；§4.5.1]
    ├── limitation subtype: manual configuration, limited ML models, non-generic, no user study, no industrial evaluation, simple case, scalability, accessibility, etc. [自由文本归类；§4.5.1]
    ├── future-work category: approach enhancement / further evaluation / quality enhancement / not mentioned [多选枚举；§4.5.2]
    └── future-work subtype: new features, more platforms/languages/models, complex scenarios, data processing, DSL/tool implementation, user/industrial evaluation, interoperability, model checking, scalability, etc. [自由文本归类；§4.5.2]
```

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L0 | 基本文献元数据 | General | Google Form section 1 | 每篇 primary study 的题名、作者、venue、citation count | 文本/数值 | 自由文本 + 数值 | 未说明则待核验 | publication trends | 无直接 finding | §3.4, §4.1 | 只迁移字段要求 |
| L1 | 发表年份/类型 | General | Fig. 4, Table 2 | 发表时间和 venue 类型 | year; conference/journal/workshop | 数值 + 完整枚举 | 不应缺失 | 趋势统计 | 研究兴趣变化 | §4.1 | 不迁移 MDE4ML 趋势 |
| L2 | 质量评分 | Quality | QA1--QA5, Appendix B | 对 primary study 质量打分 | 1--5; QA3--QA5 可 NA | 数值枚举 | 无 evaluation 时 NA | 质量分布 | 低质量证据降权 | §3.5, Table 9 | 可迁移 QA rubric 思路 |
| L3 | 目标/动机 | RQ1 | Table 3 | 使用 MDE4ML 的目标 | effort reduction / quality improvement / stakeholder understanding | 层级多选 | 未提不等于无，需编码规则 | 频次/Venn | 动机缺口 | §4.2.1 | 不迁移领域比例 |
| L4 | 目标子类 | RQ1 | Table 3 | 目标的细化原因 | abstraction, automation, integration, monitoring, etc. | 层级枚举 | 未出现在表中为未编码 | 频次 | 哪些目标被忽略 | Table 3 | 只迁移分层方式 |
| L5 | ML 技术类型 | RQ1 | Table 4 | 方案支持的 ML 类型 | generic, supervised, unsupervised, reinforcement; supervised 子类 | 层级枚举 | 未明确则 generic/需理由 | 覆盖率 | 技术覆盖缺口 | §4.2.2 | 不迁移技术结论 |
| L6 | 应用域 | RQ1 | §4.2.3 | primary study 的应用领域 | CPS, manufacturing, AV, analytics, social bots, generic 等 | 自由文本归类 | 无特定域则 generic | 领域分布 | 应用域偏置 | §4.2.3 | 分类口径可迁移 |
| L7 | 目标用户 | RQ1 | Table 5 | 方案面向角色 | ML engineer, data scientist, software engineer, domain expert, etc. | 层级多选 | 未提需 not_reported | 角色分布 | domain expert 缺口 | Table 5 | 可迁移“用户角色”字段 |
| L8 | 贡献类型 | RQ1 | Table 6, Fig. 6(b) | 研究产物类别 | code/text/model generator, DSL, framework, model, etc. | 层级多选 | 未归类需待核验 | 产物分布 | 工具/产物成熟度 | §4.2.5 | 可迁移产物编码思路 |
| L9 | 模型表示 | RQ2 | Fig. 5, Fig. 8(a) | 模型 concrete syntax | graphical / textual / both | 完整枚举 | 不明则 not_reported | 表示分布 | DSL 形态观察 | §4.3.1 | 可迁移字段，不迁移比例 |
| L10 | 建模语言类型 | RQ2 | Fig. 5, Fig. 8(b) | GPL、DSL 或扩展 | GPL / DSL / extension | 完整枚举 | 不明则 not_reported | 语言策略统计 | DSL 主导性候选 | §4.3.1 | 可迁移字段 |
| L11 | 模型层级/类型 | RQ2 | §4.3.1 | MDE 抽象层和模型种类 | CIM/PIM/PSM; requirements/design/data/etc. | 多选枚举 | 未提需 not_reported | MDE 细节统计 | PIM/design 偏向 | §4.3.1 | 可迁移字段 |
| L12 | 支持的 ML aspect | RQ2 | Fig. 9(a), §4.3.2 | 覆盖的 ML 生命周期/相关方面 | 17 类 aspect | 层级多选 | 未覆盖不等于未提，需按论文编码 | 覆盖率 | 被忽视阶段 | §4.3.2 | 仅迁移生命周期编码法 |
| L13 | ML 框架/库 | RQ2 | Table 7 | 使用的框架/库 | TensorFlow, MXNet, PyTorch, Weka, etc. | 开放受控列表 | 未提则 absent/not_reported | 工具生态 | 依赖集中度 | Table 7 | 只作字段种子 |
| L14 | 转换类型 | RQ2 | Fig. 5, §4.3.3 | MDE transformation 类型 | M2T / M2M / both; forward engineering | 完整枚举 + 布尔 | 未提需待核验 | 方法分布 | 自动生成偏向 | §4.3.3 | 可迁移 |
| L15 | 生成制品 | RQ2 | §4.3.3 | 从模型生成的 artifact | code, model, deployment config, dataset, text, API, rules, meta-model | 层级多选 | 无生成物需 not_applicable/待核验 | artifact 分布 | 产物覆盖缺口 | §4.3.3 | 可迁移字段 |
| L16 | 自动化程度 | RQ2 | Fig. 5, Fig. 8(c) | 转换是否需要人工 | fully / partially automated | 完整枚举 | 未提需 not_reported | 自动化统计 | 成熟度候选 | §4.3.3 | 可迁移 |
| L17 | 工具可用性/meta-tool | RQ2 | §4.3.3, Table 8 | 工具是否可用及底层工具 | open-source / proprietary / no tool; EMF/Sirius/XTend 等 | 枚举 + 外部名 | no tool mentioned 是显式缺失 | 可复现/成熟度 | 开源不足 | §4.3.3 | 可迁移 |
| L18 | 评价上下文/方法 | RQ3 | §4.4.1--4.4.2 | evaluation setting 和 method | academia/industry/both; case/experiment/survey/criteria/no evaluation | 多选枚举 | no evaluation 是显式值 | 评价强度 | 工业/user study 缺口 | §4.4 | 可迁移 |
| L19 | 指标与数据集 | RQ3 | Fig. 10, §4.4.3 | ML/MDE metrics 与 datasets | metric categories; MNIST/Iris/other | 层级枚举 + 开放列表 | not mentioned 与 N/A 分开 | 指标覆盖 | 评价偏 ML | §4.4.3 | 可迁移缺失语义 |
| L20 | limitations | RQ4 | §4.5.1 | primary study 自报/作者归类限制 | approach/evaluation/quality/not mentioned + subtype | 多选 + 自由文本归类 | not mentioned 是统计值 | 限制分布 | gap 候选 | §4.5.1 | 不直接外推 |
| L21 | future work | RQ4 | §4.5.2 | primary study 建议未来工作 | approach enhancement/further evaluation/quality enhancement/not mentioned + subtype | 多选 + 自由文本归类 | not mentioned 是统计值 | future work 分布 | roadmap seed | §4.5.2 | 不直接外推 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | Primary study | has_goal | Goal/sub-goal | Table 3 三大 goal 与子类 | 未列入表不代表无目标，需抽取表核验 | Table 3 | RQ1 频次/Venn |
| E2 | Primary study | targets | ML technique | generic/supervised/unsupervised/reinforcement | 未明确时归 generic 的规则需保留 | Table 4 | 技术覆盖统计 |
| E3 | Primary study | intended_for | End user | ML roles / software-system roles / domain expert | 未提需 not_reported | Table 5 | 用户角色分布 |
| E4 | Primary study | contributes | Contribution | generator/DSL/framework/model/etc. | 可多值 | Table 6 | 产物统计 |
| E5 | Goal/Contribution | cross-tabbed_with | ML aspect | Fig. 7 的 ML aspects | 只支撑图中交叉，非逐字段因果 | Fig. 7 | 发现 design/training 偏重 |
| E6 | MDE solution | has_modeling_feature | Representation/language/level/type | Fig. 5/Fig. 8/§4.3.1 | 未提需 not_reported | Fig. 5, Fig. 8 | RQ2 分类树 |
| E7 | MDE solution | transforms_to | Generated artifact | code/model/config/dataset/text/API/etc. | 无生成物或未提需区分 | §4.3.3 | artifact 生态 |
| E8 | MDE solution | uses_tooling | Framework/meta-tool/transformation language | EMF/Sirius/XTend 等 | absent from table = not mentioned | Table 8 | 工具链统计 |
| E9 | Primary study | evaluated_by | Context/method | academia/industry/both; case/experiment/survey/criteria/no eval | no evaluation 是显式值 | §4.4.1--4.4.2 | 评价强度统计 |
| E10 | Evaluation | measured_by | ML/MDE metrics | metric category and named metric | not mentioned 与 N/A 分开 | Fig. 10, §4.4.3 | 指标缺失统计 |
| E11 | Evaluation | uses_dataset | Dataset | named dataset list | 无 dataset 或不适用需分开 | §4.4.3 | 数据集集中度 |
| E12 | Primary study | has_quality_score | QA1--QA5 | 1--5 / NA | QA3--QA5 对无 evaluation 可 NA | Appendix B | 证据降权 |
| E13 | Primary study | reports_limitation | Limitation category/subtype | approach/evaluation/quality/not mentioned | not mentioned 是统计值 | §4.5.1 | RQ4 gap |
| E14 | Primary study | reports_future_work | Future-work category/subtype | enhancement/evaluation/quality/not mentioned | not mentioned 是统计值 | §4.5.2 | roadmap seed |

未发现作者公开完整实体关系模型或因果 schema；上述关系边是从 Fig. 5 feature tree、RQ 统计表和交叉图可直接复原的编码/统计关系，不应解释为因果关系。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段/统计表支持的统计观察包括：43/46 研究以 effort reduction 为目标；31/46 明确聚焦 supervised ML，4/46 聚焦 reinforcement learning，0 篇专门聚焦 unsupervised；35/46 有 code generator，30/46 有 DSL；23/46 case study，17/46 experiment，8/46 no evaluation；17 篇 open-source tool，23 篇 no tool mentioned；19 篇未提 limitations。此类观察可作为“原文内部统计”，但若用于 Paper2，只能作为方法样例。

Discussion/recommendation 提出的候选 finding 包括：data 应作为 first-class citizen；应扩展到 requirements、integration、deployment、monitoring、documentation；需要更成熟和开放的工具；需要面向 domain experts 的低代码方案；需要统一 ML terminology；需要 scalability、responsible ML、industrial evaluation 和 user study。这些是作者解释性综合，不是 Paper2 的 final finding。

对 Paper2 可迁移的方法学启发：RQ 必须投影到 extraction fields；缺失值本身可统计；`not mentioned` 与 `N/A` 要分开；统计观察、RQ Answer Summary、Discussion roadmap 应分层；字段树最好以图/表显式发布；质量评价不必作为纳排门槛，但必须影响结论强度。

绝不能迁移的领域结论：MDE4ML 中 TensorFlow、EMF、DSL、PIM、M2T、MNIST、supervised learning 等具体比例，不能外推到 LLM 状态机建模或 Paper2 目标领域。

### 7. 对现有 `review.md` 的返修建议

| 级别 | 建议 | 理由 |
|---|---|---|
| C | 重写“维度树复原”，以 P1--P46 primary study record 为根对象，使用 Google Form 5 sections + Fig. 5 + Tables/Figs 作为原生 schema；六个通用 leaf 只能放到“跨论文投影”小节。 | 现有 `review.md` 明确保留六叶接口和 v1 历史返修，容易违反 A1-DT v2 “原生树优先”口径。 |
| C | 将原生树类型改为“维度森林 / Fig.5 核心特征树 + RQ 字段森林”，不要写成“MDE4ML 生命周期分类树”或单纯“解决方案树”。 | 原文同时编码 bibliographic/QA、motivation、solution/tool、evaluation、limitation/future work。 |
| C | 主统计池资格建议写“局部可统计”：46 篇 primary studies 的字段统计可用；MDE4ML 领域发现不得迁移到 Paper2 主统计池。 | 现有 review 中“否/A1-DT 仅 schema seed”和 metadata 中 `eligible_for_statistical_synthesis: true` 容易冲突。 |
| I | 补 A.2 证据账本与 A.3 结论映射，使用具体章节、表图、分母、缺失值语义，替换当前泛化 `EV-002`/`not_verified` 行。 | 当前证据表过粗，无法直接支撑叶子字段。 |
| I | 增加“3496 vs 3934”分母不一致风险。正式统计采用摘要/方法节 3934，但记录结论节 3496 为疑似错误。 | 避免后续 SUMMARY 或论文写作引用错误分母。 |
| I | 明确 PDF 核验边界：Fig. 5 已核对；Fig. 7--10、Table 3--9 全量数字仍需逐表核验。 | `paper_content.txt` 对图形抽取有限。 |
| M | 检查 Data availability 的 GitHub 仓库是否包含原始 Google Form/coding sheet/license，并把可访问性作为待复核项。 | 可能帮助补全 40 questions 的完整叶子。 |
| M | SUMMARY 当前表若记录“样本单位/样本数量/原生树类型/统计池资格”，建议值为：`primary studies`、`46 / initial 3934`、`维度森林`、`局部可统计`。 | 我未读取 SUMMARY；这是基于本单篇审计的建议值。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | `paper_content.txt` | Abstract / §3 | Method + Research methodology | 7 个数据库，3934 到 46 篇 | 样本库/SLR 类型 | strong | 样本单位、分母 | 否 | 结论节 3496 需记录为冲突 |
| EV02 | `paper_content.txt` | §3.1 | RQ1--RQ4 | motivation / solutions / evaluation / limitations | RQ 到字段用途 | strong | 维度森林主干 | 否 | RQ 不是树根本身 |
| EV03 | `paper_content.txt` | §3.2 / Table 1 | inclusion/exclusion criteria | 排除 AI4MDE、secondary/tertiary、vision 等 | 纳排边界 | strong | 主统计池资格 | 表格可 PDF 复核 | 不代表领域外对象 |
| EV04 | `paper_content.txt` | §3.3 | search/filter/snowball | 3934→3570→72→55→32，snowball +14 | 分母链 | strong | 样本数量 | 否 | 结论节数字冲突 |
| EV05 | `paper_content.txt` | §3.4 | Data extraction | 40 questions / 5 sections / answer types | 字段来源 | strong | 原生 schema | 是，需数据仓库补全 | 未公开完整问题文本 |
| EV06 | `paper.pdf` + `paper_content.txt` | §4.1 / Fig. 5 | PDF 第 7 页 | `MDE Solution for ML` 特征树 | 显式维度树 | strong | RQ2/核心树 | 已局部核验 | 只核 Fig.5，不含全表 |
| EV07 | `paper_content.txt` | §4.2 / Tables 3--6 | goals, ML techniques, users, contributions | RQ1 字段表 | 叶子字段 | strong | L3--L8 | 是，数值需逐表核验 | 不迁移比例 |
| EV08 | `paper_content.txt` | §4.3 / Figs. 8--9 / Tables 7--8 | modeling, aspects, tools | RQ2 solution/tool 字段 | 叶子字段 | strong | L9--L17 | 是 | 不迁移 MDE4ML 结论 |
| EV09 | `paper_content.txt` | §4.4 / Fig. 10 | evaluation methods/metrics/datasets | not mentioned 与 N/A 区分 | 缺失值语义 | strong | L18--L19 | 是 | 指标名需全表核验 |
| EV10 | `paper_content.txt` | §4.5 | limitations/future work | approach/evaluation/quality 分类 | RQ4 字段 | strong | L20--L21 | 否 | discussion 不能直接 final |
| EV11 | `paper_content.txt` | §5 | validity threats | first author extraction + close match | 证据质量边界 | medium | 结论强度 | 否 | 无 kappa/完整分歧统计 |
| EV12 | `paper_content.txt` | §6--§7 | roadmap/conclusion | recommendations 与 3496 冲突 | candidate finding + risk | medium | finding 边界 | 否 | roadmap 是作者解释性综合 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是系统性 SLR，样本单位为 46 篇 primary studies。 | 样本判定 | 样本单位 | EV01, EV04 | strong | SUMMARY / review 卡片 | 结论节 3496 数字冲突不影响最终 46 |
| C02 | 原文字段来自 40 问 Google Form、5 个 section、Fig. 5 和结果表图。 | 字段来源 | 原生 schema | EV05, EV06 | strong | 维度树复原 | 40 个问题全文未在正文列出 |
| C03 | RQ 是字段组织和结果回答方式，不应当直接作为原生树根。 | schema 解释 | RQ/schema | EV02, EV05 | strong | 修复 review | RQ 可作为主干标签 |
| C04 | 原生树类型应写为维度森林，Fig. 5 是核心显式特征树。 | tree_type | 维度树 | EV06--EV10 | strong | review / SUMMARY | 需 A2a 补全全部叶子 |
| C05 | 本文可局部进入统计：只统计原文 46 篇 primary studies 的编码字段。 | statistical_pool | 主统计池资格 | EV04, EV07--EV10 | medium | SUMMARY 字段 | 不迁移 MDE4ML 领域比例 |
| C06 | `not mentioned`、`N/A`、`no evaluation` 是原文重要缺失值语义。 | missing_semantics | 评价/限制字段 | EV09, EV10 | strong | Paper2 schema seed | 需保持字段级定义 |
| C07 | Discussion roadmap 只能作为 candidate finding，不是 Paper2 final finding。 | finding_boundary | 候选 finding | EV10, EV12 | strong | A1-M6 启发 | 单篇领域建议不可外推 |
| C08 | 现有 `review.md` 需要返修，因为通用六叶接口仍像原生树。 | repair | review.md | EV02--EV10 + 已读 review | strong | 返修任务 | 不需要改原文材料 |
| C09 | 全量数值引用前需 PDF 精核，尤其 Fig. 7--10、Table 3--9。 | evidence_risk | 证据强度 | EV06--EV10 | medium | A2a checklist | 本轮只视觉核验 Fig.5/Fig.6 周边 |
| C10 | 结论节 3496 与摘要/方法节 3934 不一致，应作为分母风险。 | counterevidence | 分母链 | EV01, EV04, EV12 | strong | 待复核/风险 | 不应用 3496 替代方法节链条 |

### 9. 技能使用与自我审查记录

已读取并采用以下技能/指南文件：

| 文件 | 采用原则 |
|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | claim-evidence-engineering；无证据则弱化或标注 gap。 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | reviewer-quality objection 要具体、可执行、绑定证据。 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | 输出需列最高风险、证据状态和修订优先级。 |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 先理解研究上下文，再给结构化、可执行计划/字段。 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | 严格贴合原文方法、数据、实验/评价设置，不编造细节。 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | 用 schema 化字段、风险、任务依赖组织输出。 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 完成必须由验证证据支撑，不能因“已读完”自称完成；本任务未启动 autoresearch loop。 |

最高风险与主线程复核建议：

1. 完整 40-question Google Form 未在正文公开。本报告只能复原核心字段，主线程应核查 Data availability 仓库是否含原始表单/coding sheet。
2. 本轮 PDF 仅局部视觉核验 Fig. 5/Fig. 6 周边，未逐表核验全部数值。进入正式统计前应逐项核对 Fig. 7--10、Table 3--9。
3. 分母存在 3934 vs 3496 冲突。主线程应采用摘要/方法节链条作为主分母，并把结论节 3496 记录为疑似笔误或待作者原文核验项。

本任务未出现 blocked、timeout 或指定文件缺失；未修改仓库文件，未 commit、未 push、未调用 subagent。