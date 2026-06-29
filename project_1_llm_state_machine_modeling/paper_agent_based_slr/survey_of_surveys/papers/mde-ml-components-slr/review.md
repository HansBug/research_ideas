# Model driven engineering for machine learning components: A systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Model driven engineering for machine learning components: A systematic literature review |
| 年份 | 2024 |
| 类型 | SLR |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| DOI | <https://doi.org/10.1016/j.infsof.2024.107423> |
| 阅读状态 | 已读全文文本-paper_content核验；已回原文核对 Fig. 5 / Fig. 6 与 Data availability 链接；其余图表数值仍需正式引用前逐表复核。 |
| 证据等级 | 全文文本级；关键图示局部 原文图表级；正式统计数字待二次 PDF 核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述对象 | Model-driven Engineering for Machine Learning components，即 MDE4ML。 |
| 样本规模 | 自动检索 7 个数据库得到 3934 条，去重后 3570 条，经三轮筛选得 32 条，再通过前向/后向 snowballing 增补 14 条，最终 46 篇 primary studies。 |
| A1 角色 | 现代 SE 子领域 SLR 样本，最适合抽取“RQ → 维度树 → 分类统计 → RQ Answer Summary → Discussion roadmap”的报告模式。 |
| 是否目标证据池 | 否；本文件只为 Paper2 的综述之综述脚手架提供模式先验，不把 MDE4ML 领域发现升级为本仓库目标领域结论。 |
| 对 Paper2 最重要价值 | 提供一棵非常清楚的维度树：motivations / solutions-tools / evaluation / limitations-future work 四个 RQ 分别被拆成可抽取字段、分类轴、图表和 RQ answer summary。 |
| 主要风险 | 多数数据由第一作者抽取，虽有 pilot 与共同讨论但仍需记录 inter-rater 边界；论文结论处出现 3496/3934 初始数量不一致；图表数值引用前需 PDF 复核。 |

## 2. 全文内容详读

### 2.1 背景 / 问题定位

论文从两个事实出发：第一，ML component 已广泛进入现代软件系统，但与传统 deterministic software component 不同，ML component 的行为难以完全规格化，开发过程包含数据整理、特征选择、模型选择、超参数调整、监控与再训练等探索性步骤。第二，MDE 通过抽象、模型转换和自动制品生成，已经在传统软件、嵌入式系统和 CPS 等场景中用于降低复杂度、提升生产率与质量。

作者把二者交叉定义为 MDE4ML：用 MDE 技术开发、集成、维护或支持带 ML component 的系统。Introduction 明确说现有二次研究要么范围窄，要么缺少系统流程，要么没有充分分析 goals、end-users、ML aspects、MDE approach details、evaluation methods 和 limitations。因此本文的空白不是“没有 MDE4ML 论文”，而是缺少按 SLR protocol 系统整理 MDE4ML 研究现状、工具、评价与缺口的综述。

### 2.2 Research Questions：四个 RQ 直接对应四棵结果子树

原文设置 4 个 RQ，每个 RQ 都有明确的数据抽取范围：

| RQ | 原文问题焦点 | 对应维度树 |
|---|---|---|
| RQ1 | 为什么将 MDE 用于带 ML component 的系统？ | motivation / goal、ML technique、application domain、end users、contribution、ML aspect。 |
| RQ2 | 文献中有哪些 MDE approaches 与 tools？ | model representation、modeling language、model level/type、ML aspect、ML framework/library、transformation、generated artifact、automation level、tool availability、meta-tool/framework/transformation language。 |
| RQ3 | 现有 MDE4ML 研究如何评价？ | evaluation context、evaluation method、ML metrics、MDE metrics、datasets。 |
| RQ4 | 现有研究的 limitations 与 future work 是什么？ | limitation: approach / evaluation / solution quality；future work: approach enhancement / further evaluation / quality enhancement。 |

这组 RQ 的方法学价值很高：它不是单纯问“有哪些论文”，而是把目标领域对象拆成 motivations、solutions/tools、evaluation、limitations/future work 四个审计面，并在每个 RQ 末尾给出 “RQ Answer Summary”。Paper2 可以借鉴这种结构，把每个研究问题都要求映射到字段树和回答摘要，而不是只输出自然语言总结。

### 2.3 Kitchenham protocol 与执行流程

作者声明遵循 Kitchenham 等人的 SE SLR guidelines。流程被分为 planning、conducting、reporting 三阶段，并用 Fig. 2 表示：

1. **Planning**：识别 SLR 需求，制定 RQ，定义 SLR protocol。
2. **Conducting**：所有作者协作形成 search string 与数据库选择；第一作者执行检索、去重和初筛；多轮筛选中使用 predefined criteria；其他作者 cross-validation，歧义通过讨论解决；再使用 Wohlin snowballing 补充遗漏研究。
3. **Reporting**：对 46 篇 primary studies 做 data extraction / synthesis，报告主要发现并分析 threats to validity。

数据抽取方面，作者建立了包含 40 个问题的 Google Form，问题直接对应 4 个 RQ。Form 分为 5 个 section：general information/publication trends、motivations/goals/application domain/users、MDE approaches、evaluation techniques/tools、limitations/future challenges。答案形式包含 short answer、long answer、checkbox、radio button。质量控制上，第一作者先抽取 6 篇并与其他作者对同一批论文的抽取结果比较，发现 close match 后由第一作者抽取剩余论文；数据综合使用图、表和统计分布，并由其他作者指导。

质量评价方面，论文设置 QA1--QA5：aims 是否清楚、solution 是否清楚、measures 是否定义、是否有 practice implication、是否说明对文献的贡献。评分 1--5，结果为 19/46 good、15/46 average、12/46 poor。由于 MDE4ML 是 emerging area，作者没有因质量评分低而排除论文，以减少 publication bias。

### 2.4 数据库、检索与筛选

自动检索在 2023 年 3 月完成，使用 7 个数据库：IEEE Xplore、ACM Digital Library、Springer、Wiley、Scopus、Web of Science、ScienceDirect。检索词把大量 ML 术语与 MDE / model transformation / low-code/no-code 相关术语组合；作者也说明 model-based software engineering 与 low code/no code 不严格等同于 MDE，但因文献中常混用而纳入检索式。

筛选链条如下：

| 阶段 | 数量 / 处理 | 说明 |
|---|---:|---|
| 初始自动检索 | 3934 | 7 个数据库，无时间范围限制；以 academic article 为主。 |
| 去重后 | 3570 | Python 脚本去重，并在发现同题同作者 journal 扩展版时移除 conference/workshop 版本。 |
| title / abstract 筛选 | 72 | 大幅下降原因包括 AI4MDE 噪声、Springer 返回大量无关项、全文检索命中但语境不符。 |
| brief full-paper screening | 55 | 按 inclusion/exclusion criteria 继续过滤。 |
| detailed reading / data extraction 筛选 | 32 | 因信息不足或细读后不相关继续排除。 |
| snowballing | +14 | 32 篇与 related work 做三轮 forward/backward snowballing，前向 8 篇，后向 6 篇。 |
| 最终 primary studies | 46 | Appendix A 列 P1--P46；Appendix B / Table 9 给 QA 分数。 |

纳入标准要求论文聚焦 MDE for systems with ML components、全文可得、peer-reviewed / academic、英文。排除项包括：只有 ML 没有 MDE、MDE for non-ML AI、AI4MDE、pre-deployment model-based testing、短文少于 4 页、已有 journal 扩展版的会议/工作坊版本、信息不足、secondary/tertiary studies、vision/grey literature/books/posters/opinions/keynotes/magazine/experience/comparison papers 等。

### 2.5 46 篇 primary studies 的概貌

最终 46 篇覆盖 2008--2023 年，2018 年以后显著增多；publication type 分布经 PDF Fig. 4 核对为 conference 20、journal 17、workshop 9。主要 venue 包括 MODELS、MODELS Companion Workshop、MODELSWARD、Computer Languages、SoSym 等。

论文的 Fig. 5 是本篇最值得迁移的 feature tree：根节点是 “MDE Solution for ML”，第一层包含 Goal、Domain、End Users、Modeling、Supported ML Aspects、Tool Support、Evaluation、Scalability、Responsible ML。其中 Modeling 继续拆为 Model Representation、Model Type、Model Level、Modeling Language；Tool Support 继续拆为 Meta Tool、Transformations、Generated Artifacts、Automation Level。这个树本质上就是作者的维度模型：它来自 data extraction categories，并直接服务于后续 RQ1--RQ3 的统计与图表。

### 2.6 RQ1：motivation / goals / objectives

RQ1 将目标分成 3 个 high-level category：effort reduction、quality improvement、increased stakeholder understanding。三类不互斥，Venn diagram 用于展示重叠。

- **Effort reduction**：43/46，最常见；通过 abstraction 与 automation 减少 development、integration、monitoring、system management、data management 的工作量。
- **Quality improvement**：13/46；子项包括 reusability、extensibility、standardization、responsible ML、interoperability、maintainability、scalability、reliability。
- **Increased stakeholder understanding**：11/46；支持 non-ML experts 或提供 common language，帮助跨角色协作。

RQ1 还分析 ML techniques、application domains、end users 和 contributions。ML 技术上，supervised ML 占 31/46，reinforcement learning 4/46，没有研究专门聚焦 unsupervised learning，其余 11 篇为 generic ML。应用域中约半数没有特定 domain，具名 domain 里 CPS 及其子类最多。End users 分为 ML-related roles、software/systems roles 和 other roles/domain experts。Contribution 方面，最常见的是 code generator 35/46、DSL 30/46、MDE framework 21/46，其他包括 model generator、text generator、modeling approach、language extension、knowledge base、data synthesizer 等。

RQ1 Answer Summary 的写法值得直接学习：它先概括主导动机是通过 automation / abstraction 降低 effort，再指出质量提升和 stakeholder understanding 相对少；随后补充 domain、users、ML technique 和 ML lifecycle aspect 的分布，并点出 monitoring/documentation 被忽视。

### 2.7 RQ2：MDE solutions / tools

RQ2 是最清晰的 “solution/tool dimension tree”。主要抽取结果如下：

1. **Model representation**：graphical 23/46，textual 21/46，两者都有 2/46。
2. **Modeling language**：新 DSL 34/46，GPL 9/46，language extension 3/46。
3. **Model level / type**：PIM 42/46，设计级 model 39/46；requirements-level 6/46，data-representation 5/46。CIM / PSM 和 feature/process/deployment 等较少。
4. **Supported ML aspects**：共识别 17 种 ML aspects。Design/development 28/46、training 22/46、deployment 10/46 较多；documentation、data storage、visualization 只有 1 篇，monitoring 和 data generation 只有 2 篇。
5. **ML frameworks/libraries**：TensorFlow 最常见，MXNet 次之；library 中 Weka、Scikit-learn、NumPy 常见。
6. **Transformations**：M2T 为主，35/46 只用 M2T，4/46 只用 M2M，7/46 同时用 M2M/M2T；所有 46 篇都是 forward engineering。
7. **Generated artifacts**：ML model/training code 36/46，software/intermediate models 15/46，deployment configurations 8/46，datasets/subsets 4/46；生成语言中 Python 最多，其次 Java、C++。
8. **Automation level**：38/46 fully automated，8/46 partially automated。
9. **Tool availability / meta-tools**：17 篇提供 open-source tool，6 篇 proprietary tool，23 篇未提 tool；EMF、Sirius、XTend、EGL 等被统计为常用 modeling framework / meta-tool / transformation language。

RQ2 Answer Summary 的结构是：先概括主流 ML aspect、model level、modeling language 和 representation，再给 transformation、automation、tool availability、generated artifact 和 meta-tool 的百分比/主流选择。它把“工具生态现状”从字段分布转为一段可读 conclusion，是 Paper2 候选发现台账可以学习的格式。

### 2.8 RQ3：evaluation techniques / metrics / datasets

RQ3 先区分 evaluation context：academia、industry 或 both。89% 研究处于 academic context，约 9% 处于 industrial context，P35 同时有 academic 和 industrial evaluation。

Evaluation methods 分为 case study、experiment、survey、criteria-based assessment、no evaluation。23/46 使用 case study，其中仅 4 个是 industrial case study；17/46 使用 experiments，其中仅 1 个是 industrial experiment；user study 只有 4 篇；criteria-based assessment 2 篇；8 篇没有 evaluation。作者借用 Wohlin 的 empirical study 分类，但也声明如果 primary study 自称 case study，即使不完全符合 SE 定义，也按 case study 分类。这一点说明分类轴可以有 pragmatic rule，并需要在 schema 中显式记录。

Metrics 分为 ML metrics 与 MDE metrics：

- **ML metrics**：classification metrics 最常见，包括 accuracy、precision、recall、F-measure、AUC；time/resource metrics 包括 execution time、training time、resource usage、latency、inference time；regression metrics 和 fairness metrics 较少。
- **MDE metrics**：quality、time/resource、code 三类。Quality 包括 productivity increase、usability、scalability、learnability、desirability、completeness、effectiveness、correctness、expressiveness、usefulness、complexity reduction、generated code quality、flexibility；time/resource 包括 generation time、modeling time、execution time、re-training time reduction；code 包括 LOC、words、characters、generated pipelines。
- **Datasets**：共识别 33 个 datasets，MNIST 最常用，Iris 次之。

RQ3 Answer Summary 将评价缺口压缩得很明确：工业环境评价少，case study 最常见，experiment/user study 相对少，MDE metrics 经常缺失或 MDE aspects 没有被评价，评估更偏 ML aspects。

### 2.9 RQ4：limitations / future work

RQ4 将 limitations 分成 approach、evaluation、solution quality 三类。19 篇未提 limitations。

- **Approach limitations**：生成制品仍需手动配置、建模或 code generator 实现仍需大量人工、支持的 ML models 有限、方案不够 generic、单个模型错误可能破坏方案有效性等。
- **Evaluation limitations**：缺少 user study、缺少 industrial evaluation、只用简单场景或单一 case study、完全缺评估。
- **Solution quality limitations**：scalability 与 accessibility 问题，例如 MetaEdit+ 许可与 web interface 缺失。

Future work 也被分成三类：

- **Improvement / extension of approach**：新增功能、支持更多 platform/language/ML models、处理更复杂场景、加入 training data processing/preparation、新 DSL 或 tool implementation。
- **Further evaluation**：13 篇计划进一步评价，但从 8 篇无 evaluation 的研究里只有 P18 将 evaluation 明确列为 future work；42 篇没有 user study，却只有 3 篇将 user study 写入未来工作。
- **Quality enhancement**：与其他语言/工具集成、interoperability、优化生成代码、资源分配、model checking、scalability/reusability/adaptability 等。

RQ4 Answer Summary 给出若干可直接复核的比例：超过 88% 研究没有 industrial evaluation 和 user study，48% 只评价 MDE 或 ML 的一个方面，17% 没有任何评价；future work 中 46% 提出 additional features/enhancements，28% 提出 further evaluations。

### 2.10 Discussion / research roadmap

Discussion 将 RQ1--RQ4 的统计观察升级为 research roadmap，主题包括：

1. **Data for ML**：多数 MDE4ML 研究忽视数据生成、预处理、存储和可视化，建议把 data 作为 first-class citizen。
2. **Solution focus**：过度集中于 design/development/training，缺少 requirements engineering、integration、pipeline、deployment、monitoring、documentation。
3. **ML type**：supervised/deep learning 偏多，unsupervised 与 reinforcement learning 不足。
4. **MDE details**：部分 ML venue 研究数学/ML 细节多但 MDE 元模型和转换细节不足；部分 MDE venue 研究也缺 MDE 细节。
5. **Solution maturity**：工具成熟度、开放性、复杂场景支持、端到端 ML lifecycle 支持不足。
6. **Domain experts / low-code**：面向 domain experts 的低代码/无代码 MDE4ML 方案不足。
7. **Terminology**：ML algorithm / technique 粒度和术语不一致，影响综述编码和比较。
8. **Scalability**：约 75% 未讨论 scalability。
9. **Responsible ML**：只有 9/46 关注 human-centric 或 responsible ML。
10. **Evaluation rigor**：工业评价、user study 和同时覆盖 MDE/ML 两方面的严格评价不足。

这部分对 Paper2 很关键：作者没有停留在频次统计，而是把每个统计缺口转换成 future research recommendation。也就是说，RQ Answer Summary 是 A1-M5 统计观察，Discussion roadmap 是 A1-M6 候选发现 / 行动建议的样板。

### 2.11 Data availability

论文首页标注 Dataset link，Data availability 章节写明 SLR data is available。`paper_content.txt` 的链接文本被抽取为 `MDE4MLSLRdata(Originaldata)`，PDF 内 URI 可解析为：<https://github.com/hiraa221/MDE4ML-SLR-Data/tree/main>。正式引用数据可用性时应回 PDF 或在线仓库复核当前可访问性、内容范围、license 和是否包含 40-question extraction form / raw coding。

### 2.12 Threats to validity

论文按 internal、construct、conclusion、external validity 报告 threats：

- **Internal validity**：先制定 protocol 并由其他作者 review；search string 多次修改，在多个数据库执行；ScienceDirect 因长检索式限制拆成多个小检索式；多轮筛选，第一作者筛选、其他作者 validate；最终数据抽取前先 pilot。
- **Construct validity**：使用 7 个数据库和 automated/manual 两种搜索策略；纳排标准多轮讨论；ML 术语不一致被视为潜在威胁，通过第二、第三作者讨论达成共识。
- **Conclusion validity**：数据抽取表与 RQ 对齐；第一作者和其他作者对小样本抽取进行比较，close match 后继续；数据分析和分类经过多轮作者讨论。
- **External validity**：自动检索 + snowballing、明确纳排标准；只纳入 peer-reviewed academic studies，排除 grey literature、book chapters、opinion/vision/comparison papers；只纳入英文，作者承认可能排除部分相关研究；未按时间范围限制；不因 publication quality 排除，减少 publication bias。

需要注意：这些 threats 说明过程有交叉检查，但并未给出 Cohen $\kappa$、双人独立编码比例或完整 disagreement 统计。因此对 Paper2 而言，若要主张更强审计性，不能只写“作者讨论解决歧义”，而应记录每次模式修订、字段冲突、回填和裁决证据。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 四个 RQ 分别围绕 motivation、MDE solutions/tools、evaluation、limitations/future work；每个 RQ 都能落到字段树和 Answer Summary。 | `paper_content.txt` §3.1、§4.2--§4.5；RQ Answer Summary 分别在 RQ1--RQ4 末尾。 | 可迁移为 Paper2 的“每个 RQ 必须绑定抽取字段与回答摘要”规则。 | MDE4ML 的四类 RQ 不应原样迁移到 LLM4STM；只能迁移结构。 |
| dimension pattern | Fig. 5 给出 feature tree；Google Form 40 个问题按 5 个 section 对应 RQ；结果字段覆盖 goal/domain/users/modeling/tool/evaluation/scalability/responsible ML 等。 | `paper_content.txt` §3.4、§4.1；PDF Fig. 5 已核对。 | 高度可迁移为维度登记表和字段树构造样例。 | 该树服务 MDE4ML；目标领域需要研究者 G0/G1 重新批准。 |
| finding pattern | 从频次/分布统计形成 Answer Summary，再在 Discussion 中升级为 roadmap/recommendations，如 data first-class、evaluation rigor、responsible ML、scalability 等。 | `paper_content.txt` §4 各 RQ Answer Summary、§6 Discussion。 | 可迁移为“统计观察 → 候选发现 → 行动建议”的 A1-M5/A1-M6 分层。 | 原文没有显式区分候选发现与最终研究者裁决；Paper2 需补上 G4/G5。 |
| evidence presentation pattern | 使用 Fig. 2/3 protocol 与 search process，Table 1 纳排标准，Fig. 5 feature tree，Fig. 6 Venn，Fig. 7 bubble chart，Fig. 8--10 分布，Table 3--8 字段表，Table 9 QA。 | `paper_content.txt` 全文图表标题；PDF 局部核对 Fig. 5/6。 | 可迁移为 evidence package：搜索分母、筛选链、字段树、分布图、质量表、RQ summary。 | 图表数值正式引用前必须逐个回原文核对；`paper_content.txt` 对图形内容抽取有限。 |
| validity / threat pattern | threats 分 internal / construct / conclusion / external；强调 protocol、数据库、snowballing、多轮筛选、pilot extraction、作者讨论、英文和 publication bias 边界。 | `paper_content.txt` §5。 | 可迁移为 review.md 必备 threats 字段。 | 缺少详细 inter-rater 统计；不能把“close match”写成强一致性证明。 |
| report structure pattern | Abstract 按 Context/Object/Method/Results/Conclusion；正文为 Introduction → Background/Related Work → Methodology → Results by RQ → Threats → Discussion/Roadmap → Conclusion → Data availability/Appendix。 | `paper_content.txt` Page 1、§1--§7、Appendix A/B。 | 可迁移为现代 IST SLR 报告结构：每个 RQ 一节，每节末尾 Answer Summary。 | Paper2 是方法论文，不应完全照搬领域 SLR 结构；应抽取为制品链和审计链结构。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 / 启发 | 具体落点 |
|---|---|---|
| A1-M0 主题与综述元模型设定 | 先定义核心对象与关系：ML component、MDE approach、goal、artifact、evaluation、limitation。 | Paper2 可要求研究者在 G0 明确目标对象、制品类型、评价对象、缺陷/限制对象，而不是让 agent 自由归纳。 |
| A1-M1 脚手架挖掘与种子探测 | Fig. 5 feature tree 是从少量先验/RQ 导出的候选维度树样板。 | A2a 可把本篇作为 MDE 子领域样本，抽取“RQ 直接投影成 feature tree”的 scaffold pattern。 |
| A1-M2 维度模式批准 | Google Form 的 40 个问题、5 个 section、取值形态和 QA 字段展示了可执行 schema。 | Paper2 的字段合同应包含字段定义、取值空间、缺失值语义、证据要求、是否单选/多选/长文本。 |
| A1-M3 论文收集与概览 | 7 数据库、search string refinement、去重、三轮筛选、snowballing、纳排标准与筛选分母。 | Paper2 的检索/筛选台账需要保留每轮分母、排除理由、全文状态、snowball 来源和异常来源。 |
| A1-M4 字段级证据抽取与模式演化 | 数据抽取表与 RQ 对齐，pilot 后更新表单；分类时遇到术语不一致需讨论。 | Paper2 应记录“字段表变更原因、受影响论文、回填状态”；ML terminology 不一致是模式演化触发器样例。 |
| A1-M5 统计分析 | 用 Venn、bubble chart、feature distribution、频次表和 QA 表把字段表转成统计观察。 | Paper2 统计协议可要求频次、交叉表、覆盖率代理、缺失率、质量/评价分布，并注明分母。 |
| A1-M6 候选发现形成 | RQ Answer Summary 与 Discussion roadmap 把统计观察转为 gap / recommendation。 | Paper2 可将每个 Answer Summary 拆为 candidate finding：supporting counts、counter-evidence、scope、confidence、researcher challenge。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
SLR Study
├── Bibliographic / corpus metadata
│   ├── year / publication type / venue / citation count
│   ├── primary-study ID (P1--P46)
│   └── quality score (QA1--QA5 / NA)
├── Protocol evidence
│   ├── RQ set
│   ├── databases and search date
│   ├── search string and adaptation notes
│   ├── inclusion / exclusion criteria
│   ├── screening stages and counts
│   ├── snowballing direction and counts
│   └── data extraction form / pilot / synthesis method
├── RQ1 Motivation tree
│   ├── goal: effort reduction / quality improvement / stakeholder understanding
│   ├── sub-goal: abstraction / automation / integration / monitoring / management / reusability / responsible ML / common language ...
│   ├── ML technique: supervised / unsupervised / reinforcement / generic
│   ├── application domain: CPS / manufacturing / autonomous vehicles / analytics / generic ...
│   ├── end user: ML engineer / data scientist / software engineer / systems engineer / domain expert ...
│   ├── contribution: code generator / DSL / framework / model generator / text generator / knowledge base ...
│   └── RQ1 answer summary
├── RQ2 Solution and tool tree
│   ├── model representation: graphical / textual / both
│   ├── modeling language: DSL / GPL / extension
│   ├── model level: CIM / PIM / PSM
│   ├── model type: requirements / design / data / feature / process / deployment ...
│   ├── supported ML aspects: requirements / preprocessing / design / training / evaluation / deployment / integration / inference / monitoring / management / documentation ...
│   ├── ML framework or library: TensorFlow / MXNet / Weka / Scikit-learn ...
│   ├── transformation: M2T / M2M / both / forward engineering
│   ├── generated artifact: code / model / deployment config / dataset / text / API / meta-model ...
│   ├── automation level: full / partial
│   ├── tool availability: open-source / proprietary / not mentioned
│   ├── meta-tool / framework / transformation language
│   └── RQ2 answer summary
├── RQ3 Evaluation tree
│   ├── target area: academia / industry / both
│   ├── method: case study / experiment / survey / criteria-based assessment / no evaluation
│   ├── ML metric: classification / regression / time-resource / fairness / not mentioned / N-A
│   ├── MDE metric: quality / time-resource / code / not mentioned / N-A
│   ├── dataset: MNIST / Iris / other
│   └── RQ3 answer summary
├── RQ4 Limitation and future-work tree
│   ├── limitations: approach / evaluation / solution quality / not mentioned
│   ├── approach limits: manual configuration / limited ML models / non-generic / fragile model ...
│   ├── evaluation limits: no user study / no industrial evaluation / simple scenario / no evaluation
│   ├── quality limits: scalability / accessibility
│   ├── future work: approach enhancement / further evaluation / quality enhancement
│   └── RQ4 answer summary
├── Threats and data availability
│   ├── internal / construct / conclusion / external validity
│   ├── data repository link and current accessibility
│   └── residual risks / pending checks
└── Discussion roadmap
    ├── statistical observation
    ├── gap / limitation
    ├── recommendation
    └── candidate finding strength
```

## 6. 它如何把 motivations、solutions/tools、evaluation、limitations/future work 做成维度树和 RQ Answer Summary

这篇论文的关键套路可以概括为 5 步：

1. **从 RQ 反推字段**：RQ1--RQ4 不是开放式总结题，而是直接决定 data extraction form 的 section。每个 RQ 都对应一组可填字段。
2. **把字段组织为 feature tree**：Fig. 5 把 MDE4ML solution 拆成 goal、domain、end users、modeling、ML aspects、tool support、evaluation、scalability、responsible ML，再继续拆二级字段。
3. **用表格固定取值空间**：例如 goal/sub-goal、ML techniques、end users、contributions、tool/framework、metrics、limitations/future work 都用表格或图形固化取值。
4. **用统计分布回答 RQ**：每个 RQ 小节先描述分类轴和频次，再给示例 primary studies，最后生成 Answer Summary。
5. **把 RQ Summary 升级为 roadmap**：Discussion 不再重复表格，而是围绕 data、solution focus、ML type、MDE detail、maturity、domain expert、terminology、scalability、responsible ML、evaluation rigor 提出建议。

对 Paper2 来说，这等价于一个可以复用的制品链：`RQ -> extraction schema -> feature tree -> field evidence table -> distribution / cross-tab -> RQ answer summary -> candidate finding / roadmap`。

## 7. 对 Paper2 的启发与风险

### 7.1 启发

1. **每个 RQ 必须有字段投影**：Paper2 后续不能只写“让 agent 总结 RQ”，而应要求每个 RQ 都映射到字段、取值空间、缺失值语义和证据锚点。
2. **字段树应先由研究者批准**：本文的 Fig. 5 展示了领域专家可读的 feature tree；Paper2 可把它作为 G0/G1 的目标制品，而不是让 agent 隐式使用 prompt 内部分类。
3. **Answer Summary 是候选发现的中间层**：RQ Answer Summary 可以成为 A1-M6 candidate finding 的输入，但不能直接作为最终领域发现。Paper2 应再加 G4/G5 的研究者质疑和裁决。
4. **评价字段要覆盖“评价是否存在”和“评价评价了什么”**：本文同时记录 context、method、metrics、datasets、MDE/ML 两方面是否被评价，这对 Paper2 的审计指标很有价值。
5. **缺失和不报告本身是发现**：未提 tool、未提 limitations、无 evaluation、无 MDE metrics、无 industrial/user study 都被统计为 evidence，而不是被忽略。
6. **Discussion roadmap 可以由统计观察生成，但要保留分母**：例如 “75% 未讨论 scalability”“超过 88% 无 industrial/user study”这类强结论必须保留分母与字段来源。
7. **数据可用性应作为 review 字段**：本文提供 SLR data 链接，Paper2 可以强制记录 data/code/prompt/extraction form 是否可得及当前可访问性。

### 7.2 风险

1. **数量不一致风险**：摘要/方法写初始自动检索 3934，去重后 3570；结论处写 initial pool 3496。正式引用时应使用方法节链条，并在待复核中记录结论处疑似笔误。
2. **单主抽取者风险**：虽然有 pilot 和 co-author validation，但剩余论文主要由第一作者抽取；这对 Paper2 是提醒：若声称审计优先，应记录双人复核比例、分歧和裁决，而不是只写“讨论解决”。
3. **图表抽取风险**：`paper_content.txt` 对 Venn、feature tree、bubble chart 等信息不完整；正式统计数字必须回 PDF。
4. **领域树过拟合风险**：Fig. 5 对 MDE4ML 很强，但不能直接迁移到 LLM4STM；Paper2 需要把“树构造方法”与“树的具体取值”分离。
5. **primary-study 质量未作为纳排标准**：作者保留 poor-quality studies 以避免过窄，这符合 emerging area 逻辑；Paper2 若采用类似策略，需要明确低质量研究如何影响候选发现强度。
6. **roadmap 不是最终裁决**：本文的 roadmap 是作者解释性综合，不包含外部研究者质疑/裁决日志；Paper2 的新颖性应放在补足这一审计层。

## 历史草稿（已迁移，不作事实真源）：旧第 8 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

在不修改共享 schema 的前提下，本篇 review 暴露 4 个可在 A2a 考虑的候选字段：

1. `rq_answer_summary_pattern`：记录每个 RQ 是否有独立 Answer Summary，以及 summary 是否绑定统计分母。
2. `feature_tree_pattern`：记录综述是否提供显式维度树 / taxonomy tree / feature model，以及该树与 RQ 和抽取表的关系。
3. `extraction_form_shape`：记录数据抽取表的问题数、section、题型、pilot 方式、是否公开。
4. `roadmap_from_summary_pattern`：记录 Discussion 是否将 RQ summary 转为 research roadmap / recommendation，并区分统计观察、解释性建议和最终主张。

本任务只允许编辑本文件，因此上述字段只登记为单篇 schema 历史观察，不回修 [../../patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md)。

## 9. 待复核

- [ ] 回 PDF 逐项核对 Fig. 4--10、Table 2--9 的所有数值，尤其是百分比与分母。
- [ ] 复核 GitHub 数据仓库 <https://github.com/hiraa221/MDE4ML-SLR-Data/tree/main> 当前是否仍可访问，是否包含原始 Google Form / coding sheet / extraction data / scripts / license。
- [ ] 复核结论处 “initial pool of 3,496 papers” 与摘要/方法节 “3934 papers” 的不一致，正式写作时避免引用错误数字。
- [ ] 若进入 A2a 总表，建议补 `feature_tree_pattern`、`rq_answer_summary_pattern`、`data_availability_url`、`extraction_form_shape`。
- [ ] 若要引用 QA 结果，需回 PDF Table 9 核对每个 P1--P46 的 QA1--QA5 分数和 NA 处理。
- [ ] 若要把本篇作为“开放数据 SLR”样本，需检查仓库数据是否有版本、commit、license 与长期可用性。

## 维度树复原

### 一句话结论

本文的维度树主类型为“MDE4ML 生命周期分类树”，辅助类型为“解决方案 / 动机 / 评价树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-mde-ml-components-slr-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-mde-ml-components-slr-root] | Model driven engineering for machine learning components 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-mde-ml-components-slr-b1] 综述范围与研究问题；[dim-mde-ml-components-slr-b2] 语料收集与纳排；[dim-mde-ml-components-slr-b3] 主题 / 对象分类；[dim-mde-ml-components-slr-b4] 方法 / 技术 / 干预；[dim-mde-ml-components-slr-b5] 评价、统计与候选发现 | [ev-mde-ml-components-slr-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-mde-ml-components-slr-root] Model driven engineering for machine learning components
├── [dim-mde-ml-components-slr-b1] 综述范围与研究问题
│   └── [leaf-mde-ml-components-slr-scope] 研究范围与单位对象
├── [dim-mde-ml-components-slr-b2] 语料收集与纳排
│   └── [leaf-mde-ml-components-slr-corpus] 语料与纳排链条
├── [dim-mde-ml-components-slr-b3] 主题 / 对象分类
│   └── [leaf-mde-ml-components-slr-taxonomy] 主题与维度分类
├── [dim-mde-ml-components-slr-b4] 方法 / 技术 / 干预
│   └── [leaf-mde-ml-components-slr-method] 方法 / 技术 / 干预分类
└── [dim-mde-ml-components-slr-b5] 评价、统计与候选发现
    └── [leaf-mde-ml-components-slr-evidence] 评价、证据与复现资产
    └── [leaf-mde-ml-components-slr-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-mde-ml-components-slr-scope] | 研究范围与单位对象 | [dim-mde-ml-components-slr-b1] | 定义 MDE4ML 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-scope] |
| [leaf-mde-ml-components-slr-corpus] | 语料与纳排链条 | [dim-mde-ml-components-slr-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-corpus] |
| [leaf-mde-ml-components-slr-taxonomy] | 主题与维度分类 | [dim-mde-ml-components-slr-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-taxonomy] |
| [leaf-mde-ml-components-slr-method] | 方法 / 技术 / 干预分类 | [dim-mde-ml-components-slr-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-method] |
| [leaf-mde-ml-components-slr-evidence] | 评价、证据与复现资产 | [dim-mde-ml-components-slr-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-evidence] |
| [leaf-mde-ml-components-slr-finding] | 统计观察与候选发现 | [dim-mde-ml-components-slr-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mde-ml-components-slr-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-mde-ml-components-slr-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-mde-ml-components-slr-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-mde-ml-components-slr-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-mde-ml-components-slr-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | MDE4ML 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-mde-ml-components-slr-transfer] |
| [leaf-mde-ml-components-slr-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-mde-ml-components-slr-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-mde-ml-components-slr-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-mde-ml-components-slr-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-mde-ml-components-slr-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-mde-ml-components-slr-001 | [ev-mde-ml-components-slr-root] | [src-mde-ml-components-slr-text], [src-mde-ml-components-slr-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-mde-ml-components-slr-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-mde-ml-components-slr-002 | [ev-mde-ml-components-slr-taxonomy] | [src-mde-ml-components-slr-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-mde-ml-components-slr-b1], [dim-mde-ml-components-slr-b2], [dim-mde-ml-components-slr-b3], [dim-mde-ml-components-slr-b4], [dim-mde-ml-components-slr-b5], [leaf-mde-ml-components-slr-taxonomy], [leaf-mde-ml-components-slr-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-mde-ml-components-slr-003 | [ev-mde-ml-components-slr-stat] | [src-mde-ml-components-slr-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-mde-ml-components-slr-evidence], [leaf-mde-ml-components-slr-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-mde-ml-components-slr-004 | [ev-mde-ml-components-slr-risk] | [src-mde-ml-components-slr-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-mde-ml-components-slr-root], [leaf-mde-ml-components-slr-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-mde-ml-components-slr-tree-type] | A1DT-mde-ml-components-slr-C01 | 本文的维度树主类型为“MDE4ML 生命周期分类树”，辅助类型为“解决方案 / 动机 / 评价树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-mde-ml-components-slr-tree-type] | tree_type | [dim-mde-ml-components-slr-root] | EV-mde-ml-components-slr-001, EV-mde-ml-components-slr-004 | 树型判断仅限本文，不代表所有 MDE4ML 综述。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-scope] | A1DT-mde-ml-components-slr-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-scope] | EV-mde-ml-components-slr-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-corpus] | A1DT-mde-ml-components-slr-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-corpus] | EV-mde-ml-components-slr-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-taxonomy] | A1DT-mde-ml-components-slr-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-taxonomy] | EV-mde-ml-components-slr-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-method] | A1DT-mde-ml-components-slr-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-method] | EV-mde-ml-components-slr-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-evidence] | A1DT-mde-ml-components-slr-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-evidence] | EV-mde-ml-components-slr-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-leaf-finding] | A1DT-mde-ml-components-slr-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mde-ml-components-slr-finding] | EV-mde-ml-components-slr-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-transfer] | A1DT-mde-ml-components-slr-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-mde-ml-components-slr-root] | EV-mde-ml-components-slr-002, EV-mde-ml-components-slr-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-mde-ml-components-slr-finding-boundary] | A1DT-mde-ml-components-slr-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-mde-ml-components-slr-finding] | EV-mde-ml-components-slr-003, EV-mde-ml-components-slr-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-mde-ml-components-slr-structure-check] | [dim-mde-ml-components-slr-root], A1DT-mde-ml-components-slr-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-mde-ml-components-slr-visual-check] | EV-mde-ml-components-slr-002, EV-mde-ml-components-slr-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
