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
| 样本规模 | 自动检索 7 个数据库得到 3934 条，去重后 3570 条，经三轮筛选得 32 条，再通过前向/后向 snowballing 增补 14 条，最终 46 篇 原始研究。 |
| A1 角色 | 现代 SE 子领域 SLR 样本，最适合抽取“RQ → 维度树 → 分类统计 → RQ Answer Summary → Discussion roadmap”的报告模式。 |
| 是否目标证据池 | 否；本文件只为 Paper2 的综述之综述脚手架提供模式先验，不把 MDE4ML 领域发现升级为本仓库目标领域结论。 |
| 对 Paper2 最重要价值 | 提供一棵非常清楚的维度树：motivations / solutions-tools / evaluation / limitations-future work 四个 RQ 分别被拆成可抽取字段、分类轴、图表和 RQ answer summary。 |
| 主要风险 | 多数数据由第一作者抽取，虽有 pilot 与共同讨论但仍需记录 inter-rater 边界；论文结论处出现 3496/3934 初始数量不一致；图表数值引用前需 PDF 复核。 |

## 2. 全文内容详读

### 2.1 背景 / 问题定位

论文从两个事实出发：第一，ML component 已广泛进入现代软件系统，但与传统 deterministic software component 不同，ML component 的行为难以完全规格化，开发过程包含数据整理、特征选择、模型选择、超参数调整、监控与再训练等探索性步骤。第二，MDE 通过抽象、模型转换和自动制品生成，已经在传统软件、嵌入式系统和 CPS 等场景中用于降低复杂度、提升生产率与质量。

作者把二者交叉定义为 MDE4ML：用 MDE 技术开发、集成、维护或支持带 ML component 的系统。Introduction 明确说现有二次研究要么范围窄，要么缺少系统流程，要么没有充分分析 goals、end-users、机器学习环节、MDE approach details、evaluation methods 和 limitations。因此本文的空白不是“没有 MDE4ML 论文”，而是缺少按 SLR protocol 系统整理 MDE4ML 研究现状、工具、评价与缺口的综述。

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
3. **Reporting**：对 46 篇 原始研究 做 data extraction / synthesis，报告主要发现并分析 threats to validity。

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
| 最终 原始研究 | 46 | Appendix A 列 P1--P46；Appendix B / Table 9 给 QA 分数。 |

纳入标准要求论文聚焦 MDE for systems with ML components、全文可得、peer-reviewed / academic、英文。排除项包括：只有 ML 没有 MDE、MDE for non-ML AI、AI4MDE、pre-deployment model-based testing、短文少于 4 页、已有 journal 扩展版的会议/工作坊版本、信息不足、secondary/tertiary studies、vision/灰色文献（grey literature）/books/posters/opinions/keynotes/magazine/experience/comparison papers 等。

### 2.5 46 篇 原始研究 的概貌

最终 46 篇覆盖 2008--2023 年，2018 年以后显著增多；publication type 分布经 PDF Fig. 4 核对为 conference 20、journal 17、workshop 9。主要 venue 包括 MODELS、MODELS Companion Workshop、MODELSWARD、Computer Languages、SoSym 等。

论文的 Fig. 5 是本篇最值得迁移的 feature tree：根节点是 “MDE Solution for ML”，第一层包含 Goal、Domain、End Users、Modeling、Supported ML Aspects、Tool Support、Evaluation、Scalability、Responsible ML。其中 Modeling 继续拆为 Model Representation、Model Type、Model Level、Modeling Language；Tool Support 继续拆为 Meta Tool、Transformations、Generated Artifacts、Automation Level。这个树本质上就是作者的维度模型：它来自 data extraction categories，并直接服务于后续 RQ1--RQ3 的统计与图表。

### 2.6 RQ1：motivation / goals / objectives

RQ1 将目标分成 3 个 high-level category：effort reduction、quality improvement、increased stakeholder understanding。三类不互斥，Venn diagram 用于展示重叠。

- **Effort reduction**：43/46，最常见；通过 abstraction 与 automation 减少 development、integration、monitoring、system management、data management 的工作量。
- **Quality improvement**：13/46；子项包括 reusability、extensibility、standardization、responsible ML、interoperability、maintainability、scalability、reliability。
- **Increased stakeholder understanding**：11/46；支持 non-ML experts 或提供 common language，帮助跨角色协作。

RQ1 还分析 ML techniques、application domains、end users 和 contributions。ML 技术上，supervised ML 占 31/46，reinforcement learning 4/46，没有研究专门聚焦 unsupervised learning，其余 11 篇为 generic ML。应用域中约半数没有特定 domain，具名 domain 里 CPS 及其子类最多。End users 分为 ML-related roles、software/systems roles 和 other roles/domain experts。Contribution 方面，最常见的是 code generator 35/46、DSL 30/46、MDE framework 21/46，其他包括 模型生成器、text generator、modeling approach、language extension、knowledge base、data synthesizer 等。

RQ1 Answer Summary 的写法值得直接学习：它先概括主导动机是通过 automation / abstraction 降低 effort，再指出质量提升和 stakeholder understanding 相对少；随后补充 domain、users、ML technique 和 ML lifecycle aspect 的分布，并点出 monitoring/文档 被忽视。

### 2.7 RQ2：MDE solutions / tools

RQ2 是最清晰的 “solution/tool dimension tree”。主要抽取结果如下：

1. **Model representation**：graphical 23/46，textual 21/46，两者都有 2/46。
2. **Modeling language**：新 DSL 34/46，GPL 9/46，language extension 3/46。
3. **Model level / type**：PIM 42/46，设计级 model 39/46；requirements-level 6/46，data-representation 5/46。CIM / PSM 和 feature/process/deployment 等较少。
4. **Supported 机器学习环节**：共识别 17 种 机器学习环节。Design/development 28/46、training 22/46、deployment 10/46 较多；文档、data storage、visualization 只有 1 篇，monitoring 和 data generation 只有 2 篇。
5. **ML frameworks/libraries**：TensorFlow 最常见，MXNet 次之；library 中 Weka、Scikit-learn、NumPy 常见。
6. **Transformations**：M2T 为主，35/46 只用 M2T，4/46 只用 M2M，7/46 同时用 M2M/M2T；所有 46 篇都是 forward engineering。
7. **Generated artifacts**：ML model/training code 36/46，software/intermediate models 15/46，deployment configurations 8/46，datasets/subsets 4/46；生成语言中 Python 最多，其次 Java、C++。
8. **Automation level**：38/46 fully automated，8/46 partially automated。
9. **Tool availability / meta-tools**：17 篇提供 open-source tool，6 篇 proprietary tool，23 篇未提 tool；EMF、Sirius、XTend、EGL 等被统计为常用 modeling framework / meta-tool / transformation language。

RQ2 Answer Summary 的结构是：先概括主流 ML aspect、model level、modeling language 和 representation，再给 transformation、automation、tool availability、generated artifact 和 meta-tool 的百分比/主流选择。它把“工具生态现状”从字段分布转为一段可读 conclusion，是 Paper2 候选发现台账可以学习的格式。

### 2.8 RQ3：evaluation techniques / metrics / datasets

RQ3 先区分 evaluation context：academia、industry 或 both。89% 研究处于 academic context，约 9% 处于 industrial context，P35 同时有 academic 和 industrial evaluation。

Evaluation methods 分为 case study、experiment、survey、criteria-based assessment、no evaluation。23/46 使用 case study，其中仅 4 个是 industrial case study；17/46 使用 experiments，其中仅 1 个是 industrial experiment；user study 只有 4 篇；criteria-based assessment 2 篇；8 篇没有 evaluation。作者借用 Wohlin 的 empirical study 分类，但也声明如果 原始研究 自称 case study，即使不完全符合 SE 定义，也按 case study 分类。这一点说明分类轴可以有 pragmatic rule，并需要在 schema 中显式记录。

Metrics 分为 ML metrics 与 MDE metrics：

- **ML metrics**：classification metrics 最常见，包括 accuracy、precision、recall、F-measure、AUC；time/resource metrics 包括 execution time、training time、resource usage、latency、inference time；regression metrics 和 fairness metrics 较少。
- **MDE metrics**：quality、time/resource、code 三类。Quality 包括 productivity increase、usability、scalability、learnability、desirability、completeness、effectiveness、correctness、expressiveness、usefulness、complexity reduction、generated code quality、flexibility；time/resource 包括 generation time、modeling time、execution time、re-training time reduction；code 包括 LOC、words、characters、generated pipelines。
- **Datasets**：共识别 33 个 datasets，MNIST 最常用，Iris 次之。

RQ3 Answer Summary 将评价缺口压缩得很明确：工业环境评价少，case study 最常见，experiment/user study 相对少，MDE metrics 经常缺失或 MDE aspects 没有被评价，评估更偏 机器学习环节。

### 2.9 RQ4：limitations / future work

RQ4 将 limitations 分成 approach、evaluation、solution quality 三类。19 篇未提 limitations。

- **Approach limitations**：生成制品仍需手动配置、建模或 code generator 实现仍需大量人工、支持的 ML models 有限、方案不够 generic、单个模型错误可能破坏方案有效性等。
- **Evaluation limitations**：缺少 user study、缺少 industrial evaluation、只用简单场景或单一 case study、完全缺评估。
- **Solution quality limitations**：scalability 与 accessibility 问题，例如 MetaEdit+ 许可与 web interface 缺失。

Future work 也被分成三类：

- **Improvement / extension of approach**：新增功能、支持更多 platform/language/ML models、处理更复杂场景、加入 training data processing/preparation、新 DSL 或 tool implementation。
- **Further evaluation**：13 篇计划进一步评价，但从 8 篇无 evaluation 的研究里只有 P18 将 evaluation 明确列为 future work；42 篇没有 user study，却只有 3 篇将 user study 写入未来工作。
- **质量增强**：与其他语言/工具集成、interoperability、优化生成代码、资源分配、model checking、scalability/reusability/adaptability 等。

RQ4 Answer Summary 给出若干可在 A2a 中复核的比例：超过 88% 研究没有 industrial evaluation 和 user study，48% 只评价 MDE 或 ML 的一个方面，17% 没有任何评价；future work 中 46% 提出 additional features/enhancements，28% 提出 further evaluations。

### 2.10 Discussion / research roadmap

Discussion 将 RQ1--RQ4 的统计观察升级为 research roadmap，主题包括：

1. **Data for ML**：多数 MDE4ML 研究忽视数据生成、预处理、存储和可视化，建议把 data 作为 first-class citizen。
2. **Solution focus**：过度集中于 design/development/training，缺少 requirements engineering、integration、pipeline、deployment、monitoring、文档。
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
- **External validity**：自动检索 + snowballing、明确纳排标准；只纳入 peer-reviewed academic studies，排除 灰色文献（grey literature）、book chapters、opinion/vision/comparison papers；只纳入英文，作者承认可能排除部分相关研究；未按时间范围限制；不因 publication quality 排除，减少 publication bias。

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
| A1-M6 候选发现形成 | RQ Answer Summary 与 Discussion roadmap 把统计观察转为 gap / recommendation。 | Paper2 可将每个 Answer Summary 拆为 候选发现：supporting counts、counter-evidence、scope、confidence、researcher challenge。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> [!WARNING] v1-deprecated: 本节为 A1-DT v1 历史草稿 / 迁移来源，只能作为返修来源和历史证据，不是 A1-DT v2 当前事实口径。v2 事实以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
SLR 研究记录（SLR Study）
├── 书目 / 语料元数据
│   ├── 年份 / 发表类型 / 发表源 / 引用数
│   ├── primary-study ID（P1--P46）
│   └── 质量评分（QA1--QA5 / NA）
├── 协议证据
│   ├── RQ 集合
│   ├── 数据库与检索日期
│   ├── 检索式与适配说明
│   ├── 纳排标准
│   ├── 筛选阶段与计数
│   ├── 滚雪球方向与计数
│   └── 数据抽取表单 / pilot / synthesis method
├── RQ1 动机树
│   ├── 目标：effort reduction / quality improvement / stakeholder understanding
│   ├── 子目标：abstraction / automation / integration / monitoring / management / reusability / responsible ML / common language 等
│   ├── ML 技术：supervised / unsupervised / reinforcement / generic
│   ├── 应用领域：CPS / manufacturing / 自动驾驶车辆（autonomous vehicles） / analytics / generic 等
│   ├── 目标用户：ML engineer / data scientist / software engineer / systems engineer / domain expert 等
│   ├── 贡献：代码生成器、领域特定语言、框架、模型生成器、文本生成器、知识库等
│   └── RQ1 答案摘要
├── RQ2 方案与工具树
│   ├── 模型表示：graphical / textual / both
│   ├── 建模语言：DSL / GPL / extension
│   ├── 模型层级：CIM / PIM / PSM
│   ├── 模型类型：requirements / design / data / feature / process / deployment 等
│   ├── 支持的机器学习环节：需求工程、预处理、设计、训练、评价、部署、集成、推理、监控、管理、文档等
│   ├── ML 框架或库：TensorFlow / MXNet / Weka / Scikit-learn 等
│   ├── 转换：M2T / M2M / both / forward engineering
│   ├── 生成制品：code / model / deployment config / dataset / text / API / meta-model 等
│   ├── 自动化程度：full / partial
│   ├── 工具可获得性：开源 / 专有 / 未提及
│   ├── 元工具 / 框架 / 转换语言
│   └── RQ2 答案摘要
├── RQ3 评价树
│   ├── 目标场景：academia / industry / both
│   ├── 方法：case study / experiment / survey / criteria-based assessment / no evaluation
│   ├── 机器学习指标：分类 / 回归 / 时间-资源 / 公平性 / 未提及 / 不适用
│   ├── MDE 指标：质量 / 时间-资源 / 代码 / 未提及 / 不适用
│   ├── 数据集：MNIST / Iris / other
│   └── RQ3 答案摘要
├── RQ4 限制与未来工作树
│   ├── 限制：方法限制 / 评价限制 / 解决方案质量限制 / 未提及
│   ├── 方法限制：manual configuration / limited ML models / non-generic / fragile model 等
│   ├── 评价限制：no user study / no industrial evaluation / simple scenario / no evaluation
│   ├── 质量限制：scalability / accessibility
│   ├── 未来工作：approach enhancement / further evaluation / quality enhancement
│   └── RQ4 答案摘要
├── 威胁与数据可获得性
│   ├── internal / construct / conclusion / external validity
│   └── replication package / supplementary material
└── Paper2 迁移边界
    ├── 可迁移：动机-方案-评价-限制树形结构
    ├── 谨慎迁移：MDE / ML 具体取值
    └── 不迁移：领域统计结论
```

## 6. 它如何把 motivations、solutions/tools、evaluation、limitations/future work 做成维度树和 RQ Answer Summary

这篇论文的关键套路可以概括为 5 步：

1. **从 RQ 反推字段**：RQ1--RQ4 不是开放式总结题，而是直接决定 data extraction form 的 section。每个 RQ 都对应一组可填字段。
2. **把字段组织为 feature tree**：Fig. 5 把 MDE4ML solution 拆成 goal、domain、end users、modeling、机器学习环节、tool support、evaluation、scalability、responsible ML，再继续拆二级字段。
3. **用表格固定取值空间**：例如 goal/sub-goal、ML techniques、end users、contributions、tool/framework、metrics、limitations/future work 都用表格或图形固化取值。
4. **用统计分布回答 RQ**：每个 RQ 小节先描述分类轴和频次，再给示例 原始研究，最后生成 Answer Summary。
5. **把 RQ Summary 升级为 roadmap**：Discussion 不再重复表格，而是围绕 data、solution focus、ML type、MDE detail、maturity、domain expert、terminology、scalability、responsible ML、evaluation rigor 提出建议。

对 Paper2 来说，这等价于一个可以复用的制品链：`RQ -> extraction schema -> feature tree -> field evidence table -> distribution / cross-tab -> RQ answer summary -> 候选发现 / roadmap`。

## 7. 对 Paper2 的启发与风险

### 7.1 启发

1. **每个 RQ 必须有字段投影**：Paper2 后续不能只写“让 agent 总结 RQ”，而应要求每个 RQ 都映射到字段、取值空间、缺失值语义和证据锚点。
2. **字段树应先由研究者批准**：本文的 Fig. 5 展示了领域专家可读的 feature tree；Paper2 可把它作为 G0/G1 的目标制品，而不是让 agent 隐式使用 prompt 内部分类。
3. **Answer Summary 是候选发现的中间层**：RQ Answer Summary 可以成为 A1-M6 候选发现 的输入，但不能直接作为最终领域发现。Paper2 应再加 G4/G5 的研究者质疑和裁决。
4. **评价字段要覆盖“评价是否存在”和“评价评价了什么”**：本文同时记录 context、method、metrics、datasets、MDE/ML 两方面是否被评价，这对 Paper2 的审计指标很有价值。
5. **缺失和不报告本身是发现**：未提 tool、未提 limitations、无 evaluation、无 MDE metrics、无 industrial/user study 都被统计为 evidence，而不是被忽略。
6. **Discussion roadmap 可以由统计观察生成，但要保留分母**：例如 “75% 未讨论 scalability”“超过 88% 无 industrial/user study”这类强结论必须保留分母与字段来源。
7. **数据可用性应作为 review 字段**：本文提供 SLR data 链接，Paper2 可以强制记录 data/code/prompt/extraction form 是否可得及当前可访问性。

### 7.2 风险

1. **数量不一致风险**：摘要/方法写初始自动检索 3934，去重后 3570；结论处写 initial pool 3496。正式引用时应使用方法节链条，并在待复核中记录结论处疑似笔误。
2. **单主抽取者风险**：虽然有 pilot 和 co-author validation，但剩余论文主要由第一作者抽取；这对 Paper2 是提醒：若声称审计优先，应记录双人复核比例、分歧和裁决，而不是只写“讨论解决”。
3. **图表抽取风险**：`paper_content.txt` 对 Venn、feature tree、bubble chart 等信息不完整；正式统计数字必须回 PDF。
4. **领域树过拟合风险**：Fig. 5 对 MDE4ML 很强，但不得迁移到 LLM4STM；Paper2 需要把“树构造方法”与“树的具体取值”分离。
5. **primary-study 质量未作为纳排标准**：作者保留 poor-quality studies 以避免过窄，这符合 emerging area 逻辑；Paper2 若采用类似策略，需要明确低质量研究如何影响候选发现强度。
6. **roadmap 不是最终裁决**：本文的 roadmap 是作者解释性综合，不包含外部研究者质疑/裁决日志；Paper2 的新颖性应放在补足这一审计层。

## 历史草稿（已迁移，不作事实真源）：旧第 8 节迁移来源

> [!WARNING] v1-deprecated: 本节为 A1-DT v1 历史草稿 / 迁移来源，只能作为返修来源和历史证据，不是 A1-DT v2 当前事实口径。v2 事实以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

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

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__codex.md](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__codex.md)、[../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__claude.md](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__claude.md)、[../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__deepseek.md](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/mde-ml-components-slr.md](../../audits/a1dt-v2-19x3/adjudications/mde-ml-components-slr.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `mde-ml-components-slr` |
| 审计代理 | `claude` (Opus 4.7 1M, 本任务以单 智能体 完成，未派生 subagent) |
| 是否已读 `paper_content.txt` | 是。按行顺序通读 1–1849 行（覆盖摘要、§1–§7、Table 1–9、Appendix A 主体、Acknowledgments、数据可获得性（Data 可获得性）、Fig. 4–10 文字描述），后续 1849–2123 行为 P34–P46 引用条目与参考文献，仅抽样核对 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；用于核对 venue（IST）、DOI、年份与本仓库 CCF 标注 |
| 是否打开或核对 `paper.pdf` | 否（本轮以全文文本审计为主）；Fig. 5 / Fig. 6 / Fig. 7 / Fig. 8 / Fig. 9 / Fig. 10 视觉版面、Table 2 单元格 wrap、Table 9 单行 QA 分数仍需 PDF 复核 |
| 原文类型 | **SLR**（Kitchenham 指南 显式声明，protocol → planning/conducting/报告方式） |
| 被编码样本单位 | **原始研究**，编号 P1–P46，46 篇 |
| 样本数量 / 分母 | 自动检索 3934 → 去重 3570 → title/abstract 72 → brief 完整-paper 55 → detailed reading 32 → snowballing +14（前向 8 + 后向 6）→ **46**（其中 conclusion §7 误写为 “3,496 papers”，与方法 §3.3.2 中 3934 不一致） |
| 原生树类型 | **单根维度树**（Fig. 5 "Features of selected 原始研究"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 模式 与 QA1–QA5 质量 rubric 两个并列 模式；不构成维度森林 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取的本地文件与章节**：

- `bibtex.bib` 完整（1–13 行）：确认 IST 期刊、2024、vol 169、DOI 10.1016/j.infsof.2024.107423。
- `metadata.json` 完整：交叉确认 review_type=SLR、se_subfield=MDE4ML、CCF B、`eligible_for_schema_seed=true`（模式种子字段为真） / `eligible_for_statistical_synthesis=true` / `evidence_role=slr_dimension_pattern`。
- `paper_content.txt` 顺序通读至 1849 行（含 §7 Conclusion 与 Appendix A P1–P33 引文），其后 P34–P46 引文与 references 抽样核对。覆盖：
  - §1 Introduction（pp.1–3）
  - §2 Background and related work（§2.1 MDE / §2.2 ML / §2.3 MDE4ML / §2.4 二次研究 比较）
  - §3 研究方法（Research methodology）（§3.1 RQs / §3.2 Study selection / §3.3 Search strategy / §3.4 数据抽取（数据抽取） / §3.5 Quality assessment）
  - §4 Results（§4.1 publication trends, §4.2 RQ1, §4.3 RQ2, §4.4 RQ3, §4.5 RQ4，每个 RQ 末尾的 Answer Summary 已逐字读取）
  - §5 Threats to 效度（internal / construct / conclusion / external）
  - §6 Discussion and research 路线图（§6.1.1 机器学习数据（Data for ML）、§6.1.2 Solution focus、§6.1.3 Solution maturity、§6.1.4 Domain experts、§6.1.5 ML algorithms/terminology、§6.1.6 Scalability、§6.1.7 Responsible ML、§6.2.1 Real-world 评价、§6.2.2 Evaluation rigor）
  - §7 Conclusion 与 10 项核心 发现
  - 数据可获得性（Data 可获得性） link：`MDE4ML SLR data (Original data)` → GitHub 仓库
  - Appendix A 原始研究 P1–P46 引文
  - Appendix B / Table 9 质量评价 per-paper QA1–QA5 scores
- `review.md` 478 行：完整读取分两段（1–389、390–478）。已审过的现有内容包括快速结论卡片、§2 全文详读、§3 六类 模式 表、§4 A1-M0–M6 映射、§维度树复原、19×3 审计返修块、A.1–A.4 附录。

**关键原文证据锚点（5–12 条短引或释义）**：

1. RQ 设置 §3.1：四个 RQ（motivation / approaches & 工具 / 评价 / limitations & future work）。
2. 数据抽取（数据抽取） form §3.4：Google Form **40 个问题，5 个 section**；答题形态 23 short answer + 10 long answer + 2 checkbox + 14 radio button；pilot：第一作者抽取 6 篇后与其他作者交叉对照。
3. Quality rubric §3.5：QA1–QA5，1–5 分外加 NA；结果 19/46 good、15/46 average、12/46 poor。
4. 筛选链 §3.3：3934 → 3570 → 72 → 55 → 32 → +14 snowball → 46。
5. Fig. 5 描述 §4.1：feature 树 来自 数据抽取 类别；根节点 MDE Solution for ML，一级分支显式覆盖 Goal / Domain / End Users / Modeling / Supported ML Aspects / Tool Support / Evaluation / Scalability / Responsible ML（被 §4.2–§4.5 与 Discussion §6 全部命中）。
6. RQ1 §4.2.1 三类 goal + 子目标 14 项（Table 3）；ML techniques 4 大类 + 3 子类（Table 4）；End users 3 类 7 角色（Table 5）；Contributions 11 类（Table 6）。
7. RQ2 §4.3 模型 representation graphical 23 / textual 21 / both 2；modeling language DSL 34 / GPL 9 / extension 3；CIM/PIM/PSM 分布 PIM=42；M2T 35 / M2M 4 / both 7，全部 forward-engineering；automation 完整 38 / 部分 8；工具 open-source 17 / proprietary 6 / 未提及 23。
8. RQ3 §4.4 评价 context academic 89% / 工业（industrial） 9% / both 1 (P35)；评价 方法 case study 23 / experiment 17 / criteria-based 2 / 无评价 8；ML 指标 4 类、MDE 指标 3 类；数据集 共 33 个，MNIST 7 篇、Iris 3 篇。
9. RQ4 §4.5 三类 limitation（approach / 评价 / 质量）+ 三类 future work；88% 无 工业（industrial） 评价 与 user 研究；48% 仅评一面；17% 无 评价。
10. §6 路线图 10 项主题，每项以 “We recommend…” / “We suggest…” / “We encourage…” 给出可执行建议。
11. §7 Conclusion 中“initial pool of **3,496** papers”——与 §3.3.2 中 **3934** 不一致，为论文笔误，正式引用应使用 3934/3570。
12. 数据可获得性（Data availability）：仅一句 “SLR data is available at the following link MDE4MLSLRdata(Originaldata)”；review.md 已注记 GitHub URL `https://github.com/hiraa221/MDE4ML-SLR-Data/树/main`，需 A2a 复核当前可访问性与内容范围。

**仅基于 text 的部分 / 仍需 PDF 视觉核验**：

- Fig. 4(a) 年份柱状图与 Fig. 4(b) 发表类型 饼图的实际数值（journal 17 / conference 20 / workshop 9 来自 review.md 旧版核对，本轮未独立 PDF 复核）。
- Fig. 5 feature 树 二级节点与连接关系（text 抽取仅给文字描述，未给完整树结构）。
- Fig. 6 三联图（goals Venn、工具-specific contributions Venn、end-user distribution）。
- Fig. 7 bubble chart（研究 goal × contribution × ML aspect）的具体气泡频次。
- Fig. 8–10 各项分布百分比。
- Table 9（Appendix B）QA1–QA5 per-paper 分数矩阵已在 paper_content.txt 1693–1719 行抽取，但版面错位严重（P1 与 P24 同行；P5/P6/P8/P18/P21/P26/P43 的 QA3–QA5 为 NA），需 PDF 视觉核对每行 QA。

### 2. 样本单位与字段来源判定

**1）原文纳入和逐项描述的对象是什么？**

原始研究（46 篇带 ML component 的 MDE 论文，编号 P1–P46）。所有抽取表（Table 3–8）单元格都填入 P-编号集合，证明 研究 是原子单位。

**2）作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**

是。完整 Kitchenham SLR 工作流：

- protocol 先于检索；
- 7 个数据库 + 长检索式（含 OR/AND）；
- Table 1 显式 4 条 inclusion + 10 条 exclusion；
- 三轮筛选 + Wohlin snowballing（三轮 forward/backward）；
- Google Form 40 题 / 5 section 的 数据抽取 模式；
- pilot 6 篇对照 + 全员讨论；
- QA1–QA5 五点量表 + NA。

**3）原文字段来自哪里？**

原文显式给出三个来源彼此关联的 模式：

- **Extraction form 模式**（§3.4）：5 section × 40 question；section 与 RQ1–RQ4 对齐，section 1 是 publication 元信息。
- **Feature 树 模式**（Fig. 5 + §4.1 末尾两句）：从 抽取 form 类目派生的 feature 树，是公开发表的"代表性可视化"形态。
- **Quality rubric 模式**（§3.5 + Table 9）：QA1–QA5 × 1–5 分 / NA，与 RQ 正交。

三者共同构成本文 模式。Fig. 5 是 feature 树 的“面向读者版”，Google Form 是 raw 模式，Table 3–8 是 模式 在 P1–P46 上的实例化。

**4）RQ 与样本单位是什么关系？**

RQ 既是树根（每个 RQ 对应一个子树）又是字段用途说明（每个 RQ 对应 Google Form 的一个 section）。但 RQ 本身不是叶子；叶子是 Table 3–8 中按 RQ 派生的具体字段（如 goal、sub-goal、ML technique、模型 level）。

**5）若无系统样本库，如何降级？**

不适用。本文是系统 SLR，主统计池资格成立；A1-DT 降级只发生在 模式 节点级（Fig. 5 的 Scalability、Responsible ML 一级节点只在 Discussion §6.1.6 / §6.1.7 二次出现，没有独立结果小节，需要降级为“cross-cutting concern”而非主轴）。

### 3. 原生样本编码维度树 / 维度森林

本文是**单根树**：根节点 `MDE Solution for ML`（Fig. 5 标题：Features of selected 原始研究）；并存的两个独立 模式（Inclusion/Exclusion 纳排 模式、QA1–QA5 质量 rubric）按 A1-DT v2 严谨口径应作为同一“原始研究”样本单位上的并列 模式，构成**维度小森林**：主树 + 纳排 模式 + QA rubric。下面给出主树主干 + 代表性叶子；纳排与 QA 单独列出。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 面向机器学习组件的 MDE 方案（MDE Solution for ML；P1..P46）
│
├── [S1] 发表与书目信息（Google Form §1）
│   ├── 标题 / 作者
│   ├── 发表源：Table 2 中的 MODELS、MODELSWARD、配套工作坊（Companion Workshop）、Computer Languages、SoSyM 等
│   ├── 发表类型：{会议、期刊、工作坊}；Fig. 4(b)
│   ├── 发表年份：2008..2023；Fig. 4(a)
│   └── 引用数：数值
│
├── [RQ1] 动机与贡献对象
│   ├── 目标：{降低工作量（降低工作量）, 提升质量（提升质量）, 增强干系人理解（Increased stakeholder 理解）}
│   │   └── 目标子类：Table 3 的 16 个封闭项；例如抽象、自动化、集成、可复用性、负责任机器学习、支持非机器学习专家等
│   ├── 机器学习技术：{通用机器学习、监督式学习、神经网络、非监督式学习、强化学习}
│   ├── 应用领域：信息物理系统（CPS；首次术语）、大数据分析、制造业、自动驾驶车辆、智能家居、交通信号控制、卫星通信、网络规划、数据分析、社交机器人、通用 / 未说明等 11 类
│   ├── 目标用户：机器学习工程师（ML engineer；首次术语）、数据分析师 / 数据工程师 / 数据科学家、软件工程师、系统工程师、业务分析师、形式化方法分析师、领域专家
│   └── 贡献类型：代码生成器（code generator；首次术语）、文本生成器、模型生成器、领域特定语言（DSL）、框架、模型、建模方法、建模语言扩展、机器学习知识库、数据合成器、OCL 约束、应用程序接口（API）、元建模语言
│
├── [RQ2] 方案与工具支持
│   ├── 建模表示：{图形化（图形化；首次术语）、文本化、二者兼有}
│   ├── 建模语言：{新 DSL（新 DSL）、通用编程语言（GPL）、语言扩展（语言扩展）}
│   ├── 模型层级：{计算无关模型（CIM；首次术语）、平台无关模型（PIM）、平台特定模型（PSM）、组合层级}
│   ├── 模型类型：{需求级（需求-level）、设计级（设计-level）、数据表示（数据表示）、特征（Feature）、过程（过程）、部署（部署）}
│   ├── 支持的 ML 环节：需求工程（requirements engineering）、数据预处理（data preprocessing）、设计与开发（design & development）、训练（training）、评价、部署（deployment）、集成（integration）、推理（inference）、监控（monitoring）、管理（management） 等 17 项
│   ├── ML 框架 / 库：TensorFlow、PyTorch、Caffe、Keras、Scikit-learn、NumPy、Pandas、OpenAI Gym 等（均为原文工具名）
│   ├── 模型转换：{仅模型到文本（M2T-only；首次术语）、仅模型到模型、二者兼有}；46 篇全部是正向工程
│   ├── 生成制品：机器学习模型 / 训练代码、软件 / 中间模型、部署配置、数据集、文本文件、应用程序接口代码、推荐规则、元模型等
│   ├── 自动化程度：{全自动（全自动）、部分自动（部分自动）}
│   ├── 工具可获得性：{开源（开源）、专有（专有）、未提及（未提及）}
│   └── 元工具 / 转换语言：EMF、Sirius、XTend、EGL 等，见 Table 8
│
├── [RQ3] 评价设计
│   ├── 评价场景：{学术环境（学术环境）, 工业环境（工业环境）, 二者皆有（二者皆有）}
│   ├── 评价方法：案例研究（case study；首次术语）、实验、调查 / 用户研究、基于准则的评价、无评价
│   ├── 工业评价标记：例如工业案例研究 4/23、工业实验 1/17
│   ├── 机器学习指标：分类（分类；首次术语）、回归、时间-资源、公平性、未提及、不适用（N/A）
│   ├── MDE 指标：质量、时间-资源、代码、未提及、不适用；质量包含生产率、可用性、可扩展性、正确性、有用性、生成代码质量等
│   └── 使用数据集：共 33 个；MNIST 7/46、Iris 3/46 等
│
├── [RQ4] 限制与未来工作
│   ├── 限制：方法限制（approach limitation；首次术语）、评价限制、解决方案质量限制、未提及；例如手工配置、机器学习模型范围有限、缺少用户研究、缺少工业评价、可扩展性等
│   └── 未来工作：扩展方法、进一步评价、质量增强、未提及；例如新平台 / 新语言 / 更多机器学习模型、工业评价、工具互操作、代码优化、模型检查等
│
├── [并列模式 1] 纳入 / 排除门禁（Table 1）
│   └── 纳入标准 I01..I04；排除标准 E01..E10；均为封闭枚举
│
└── [并列模式 2] 质量评估量规（§3.5, Appendix B Table 9）
    ├── QA1 目标是否清楚；QA2 方案是否清楚；QA3 度量是否定义；QA4 实践影响；QA5 文献贡献
    ├── 单项分数：{1, 2, 3, 4, 5, NA}；无评价时 QA3..QA5 = 不适用（NA）
    └── 聚合标签：{好、中、差}；分布 19/15/12
```

主统计池资格 = **是**（叶子级别有显式分母 46 与频次表），但本节大量节点的取值空间在 review.md 尚未完整复原。

### 4. 叶子维度表

仅列举原文显式可枚举或显式可计数的叶子；自由文本字段（如 contribution-narrative）按"自由文本加理由"标注；保留 `EV-…` 证据指针给 §8 A.2 草案。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-bib-venue | 发表源（venue） | §section-1 | Form §1, Table 2 | 原始研究 的会议/期刊名 | 列表（34 个 venue） | 自由文本 + 标准化 | 必填 | venue 频次表 | 学术 maturity / 社区聚集度 | EV-001 §3.4, §4.1 | 仅本 语料 |
| L-bib-ptype | 发表形态 | §section-1 | Fig. 4(b) | conf/journal/workshop | {会议、期刊、工作坊} | 完整枚举（3 类） | 必填 | 比例 ≈ 43.5/37/19.6% | maturity 指标 | EV-001 §4.1 | 可迁结构 |
| L-bib-year | 发表年份 | §section-1 | Fig. 4(a) | 出版年份 | 整数 2008..2023 | 数值/区间 | 必填 | 年度分布 | "近 5 年急增"叙事支撑 | EV-001 §4.1 | 可迁结构 |
| L-rq1-goal | 高层目标 | §RQ1 | Table 3 | 3 大类 goal | {降低工作量（降低工作量）, 提升质量（提升质量）, 增强干系人理解（Increased stakeholder 理解）} | 完整枚举（3 类，可多选） | 必填，多选 | 43/13/11 (over 46) | "动机偏 effort reduction" 候选发现 | EV-002 §4.2.1 Table 3 | 可迁结构，不迁结论 |
| L-rq1-subgoal | 子目标 | L-rq1-goal | Table 3 | 16 个目标子类 | {抽象（Abstraction）, 自动化（Automation）, 集成（Integration）, 监控（Monitoring）, 系统管理（System management）, 数据管理（Data management）, 可复用性（Reusability）, 可扩展性（Extensibility）, 标准化（Standardization）, 负责任机器学习（Responsible ML）, 互操作性（Interoperability）, 可维护性（Maintainability）, 可伸缩性（Scalability）, 可靠性（Reliability）, 支持非机器学习专家（Support non-ML experts）, 通用语言（Common language）} | 层级枚举（16） | 多选 | 各 sub-goal 频次 | 缺口识别 | EV-002 Table 3 | 可迁结构 |
| L-rq1-mltech | ML 技术 | §RQ1 | Table 4 | ML 子类 | {通用机器学习、监督式学习→{传统方法、神经网络、传统方法 + 神经网络}, 非监督式学习, 强化学习} | 层级枚举（6 终端） | 单选+子类 | 31/4/0/11 | “无仅使用非监督式学习的论文”是 发现 | EV-002 §4.2.2 Table 4 | 可迁结构 |
| L-rq1-domain | 应用域 | §RQ1 | §4.2.3 | 11 个 domain | {信息物理系统、制造业、自动驾驶车辆、智能家居、交通信号控制、卫星通信、网络规划、大数据分析、数据分析、社交机器人、通用/未说明} | 完整枚举（11 类） | 可空（→generic） | 域频次 | "约半数无具体域" | EV-002 §4.2.3 | 可迁结构 |
| L-rq1-enduser | end user | §RQ1 | Table 5 | 3 类 7 角色 | 见 §3 树 | 层级枚举（7 终端，可多选） | 多选 | 18/16/11 等 | 受众缺口 | EV-002 §4.2.4 Table 5 | 可迁结构 |
| L-rq1-contrib | contribution 类型 | §RQ1 | Table 6 | 11 类 contribution | 见 §3 树 | 完整枚举（11，多选） | 多选 | 35/30/21/.../1 | "code generator + DSL + 框架 主导" | EV-002 §4.2.5 Table 6 | 可迁结构 |
| L-rq2-mrep | 模型表示 | §RQ2 Modeling | Fig. 8(a) | 具体语法 | {图形化、文本化、二者兼有} | 完整枚举（3 类） | 必填 | 23/21/2 | 半数图形半数文本 | EV-002 §4.3.1 | 可迁结构 |
| L-rq2-mlang | 建模语言 | §RQ2 Modeling | Fig. 8(b) | 语言族 | {新 DSL（新 DSL）、通用编程语言（GPL）、语言扩展（语言扩展）} | 完整枚举（3 类） | 必填 | 34/9/3 | DSL 主导 | EV-002 §4.3.1 Fig. 8(b) | 可迁结构 |
| L-rq2-mlevel | 模型层 | §RQ2 Modeling | §4.3.1 | OMG levels | {CIM, PIM, PSM, PIM+PSM, CIM+PIM+PSM} | 层级枚举 | 必填，可组合 | PIM-only 35; PIM+PSM 6; CIM-only 2; PSM-only 2; CIM+PIM+PSM 1 | "PIM 占 42/46" | EV-002 §4.3.1 | 可迁结构 |
| L-rq2-mtype | 模型类型 | §RQ2 Modeling | §4.3.1 | 模型 type | {需求级（需求-level）、设计级（设计-level）、数据表示（数据表示）、特征（Feature）、过程（过程）、部署（部署）} | 完整枚举（6 类） | 多选 | 39/6/5/.../少数 | 缺 流程/deployment 模型 | EV-002 §4.3.1 | 可迁结构 |
| L-rq2-mlasp | 支持的 ML 方面 | §RQ2 | §4.3.2 Fig. 9(a) | 17 机器学习环节 | 见 §3 树 | 完整枚举（17，多选） | 多选 | design 28, train 22, deploy 10, monitor 2, doc 1 ... | "monitoring/文档 被忽视" | EV-002 §4.3.2 Fig. 9(a) | 可迁结构 |
| L-rq2-mlfw | ML 框架 / library | §RQ2 | Table 7 | 框架与库 | 见 Table 7 | 开放枚举（≈19） | 未报告 | 频次 | "TF 主导" | EV-002 Table 7 | 可迁结构 |
| L-rq2-trans | 变换种类 | §RQ2 工具支持（Tool support） | §4.3.3 | M2T/M2M | {仅模型到文本、仅模型到模型、二者兼有；全部为正向工程} | 完整枚举（3+布尔） | 必填 | 35/4/7 | 全部 forward | EV-002 §4.3.3 | 可迁结构 |
| L-rq2-art | 生成制品 | §RQ2 工具支持（Tool support） | §4.3.3 | 制品 类型 | {机器学习模型/训练代码、软件/中间模型、部署配置、数据集/子集、文本文件、应用程序接口代码、推荐规则、元模型} | 完整枚举（8 类） | 多选 | 36/15/8/4/2/2/2/1 | "代码/模型主导" | EV-002 §4.3.3 | 可迁结构 |
| L-rq2-tlang | 目标语言 | L-rq2-art | Fig. 9(b) | 生成代码语言 | {Python, Java, C++, ...} | 开放枚举 | 多选 | 15/10/4/... | Python 主导 | EV-002 §4.3.3 Fig. 9(b) | 可迁结构 |
| L-rq2-autom | 自动化程度 | §RQ2 工具支持（Tool support） | Fig. 8(c) | 全自动/部分自动 | {全自动（全自动）、部分自动（部分自动）} | 完整枚举（2 类） | 必填 | 38/46 | 约 82.6% 全自动 | EV-002 §4.3.3 | 可迁结构 |
| L-rq2-工具 | 工具可得性 | §RQ2 工具支持（Tool support） | §4.3.3 | 工具 状态 | {开源（开源）、专有（专有）、未提及（未提及）} | 完整枚举（3 类） | 必填（含 未提及） | 17/6/23 | "50% 不提及工具" | EV-002 §4.3.3 | 可迁结构 |
| L-rq2-metatool | meta-工具 | §RQ2 工具支持（Tool support） | Table 8 | 元工具栈 | 开放枚举（Sirius, EMF, ... 见 Table 8） | 开放枚举 | 未报告 | 频次 | 生态集中度 | EV-002 Table 8 | 可迁结构 |
| L-rq3-area | 评价语境 | §RQ3 | §4.4.1 | academia/industry | {学术环境（学术环境）, 工业环境（工业环境）, 二者皆有（二者皆有）} | 完整枚举（3 类） | 必填 | 89% / 9% / P35 | "工业评价稀缺" | EV-003 §4.4.1 | 可迁结构 |
| L-rq3-方法 | 评价方法 | §RQ3 | §4.4.2 | 5 类方法 | {案例研究、实验、调查 / 用户研究、基于准则的评价、无评价} | 完整枚举（5 类，可多选） | 多选 | 23/17/4/2/8 | “案例研究主导，用户研究极少” | EV-003 §4.4.2 | 可迁结构；注意作者 pragmatic rule（如果论文自称 case study 即按 case study 计） |
| L-rq3-工业（industrial） | 工业变体 | L-rq3-方法 | §4.4.2 | flag | {工业案例研究（工业 case study）, 工业实验（工业 experiment）, 无} | 布尔/枚举 | 默认 false | 4/1/41 | "几乎全在 academic 环境" | EV-003 §4.4.2 | 可迁结构 |
| L-rq3-mlmetric | ML 指标族 | §RQ3 | §4.4.3 Fig. 10(a) | 4 大类 | {分类（分类）, 回归（Regression）, 时间/资源（Time-resource）, 公平性（Fairness）, 未提及（未提及）, 不适用（N/A）} | 完整枚举（6 类） | 必填 | 见 Fig. 10(a) | "fairness/回归 罕见" | EV-003 §4.4.3 | 可迁结构 |
| L-rq3-mdemetric | MDE 指标族 | §RQ3 | §4.4.3 Fig. 10(b) | 3 大类 | {质量（Quality）, 时间 / 资源（Time-resource）, 代码（Code）, 未提及（未提及）, 不适用（N/A）} | 完整枚举（5） | 必填 | 见 Fig. 10(b) | "MDE 指标常缺" | EV-003 §4.4.3 | 可迁结构 |
| L-rq3-数据集 | 数据集 | §RQ3 | §4.4.3 | 公开数据集名 | 开放枚举（33 个） | 开放枚举 | 未报告 | MNIST 7, Iris 3 | "评价基准浅" | EV-003 §4.4.3 | 可迁结构 |
| L-rq4-limscope | 限制类别 | §RQ4 | §4.5.1 | 3 类 + 未提及 | {方法限制、评价限制、解决方案质量限制、未提及} | 完整枚举（4，多选） | 多选 | 19/46 未提 | 自报告 limitations 偏少 | EV-003 §4.5.1 | 可迁结构 |
| L-rq4-fwscope | 未来工作 类别 | §RQ4 | §4.5.2 | 3 类 + 未提及 | {方法改进/扩展、进一步评价、质量增强、未提及} | 完整枚举（4，多选） | 多选 | 7/46 未提 | 评估/工业评价计划不足 | EV-003 §4.5.2 | 可迁结构 |
| L-qa-q | QA 单项分 | parallel-QA | §3.5 Table 9 | QA1..QA5 | {1, 2, 3, 4, 5, NA} | 数值（1–5）+ NA | 无评价时为 NA（QA3..QA5） | 单项均值 / 分布 | 质量层次 | EV-004 Table 9 | 可迁结构 |
| L-qa-band | QA 等级聚合 | parallel-QA | §3.5 | 总评 | {好、中、差} | 完整枚举（3 类） | — | 19 / 15 / 12 | 是否影响 发现 加权 | EV-004 §3.5 | 可迁结构 |
| L-inc-id | 纳入条件 | parallel-IE | Table 1 | I01..I04 | 完整枚举（4 类） | 全部为真 | 必填 | gate 不进入字段统计 | gate-only | EV-005 Table 1 | 可迁结构 |
| L-exc-id | 排除条件 | parallel-IE | Table 1 | E01..E10 | 完整枚举（10） | 全部为假 | 必填 | gate 不进入字段统计 | gate-only | EV-005 Table 1 | 可迁结构 |

### 5. 关系边表

本文未给出显式的关系型 模式（如 RDF / ontology / cross-tab as object），但 Fig. 7 bubble chart 与若干 cross-tab 隐式定义了如下关系边；可被识别为"二元投影 / 三元投影"。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-goal-aspect | L-rq1-goal | 共现 / 频次 | L-rq2-mlasp | Fig. 7 bubble cell | 0 cell 表示无 | Fig. 7 | 揭示哪些 ML aspect 主要服务哪些 goal |
| R-contrib-aspect | L-rq1-contrib | 共现 / 频次 | L-rq2-mlasp | Fig. 7 bubble cell | 0 cell 表示无 | Fig. 7 | 揭示 contribution 与 ML aspect 的耦合 |
| R-subgoal-goal | L-rq1-subgoal | 子属关系 | L-rq1-goal | 3 父类 | — | Table 3 | 层级聚合 |
| R-subtype-mltech | "Traditional/NN/Traditional+NN" | 子属关系 | L-rq1-mltech | 见 Table 4 | — | Table 4 | 层级聚合 |
| R-方法-工业（industrial） | L-rq3-方法 | 二元变体 | L-rq3-工业（industrial） | 布尔值 | false 默认 | §4.4.2 | 工业评价识别 |
| R-p研究-extension | 原始研究 | 包含 / 被吸收 | 原始研究 | journal 扩展版优先 | — | §3.3.2 "removed conference/workshop if journal version exists" | 反映去重策略 |
| R-p研究-qa | 原始研究 (P1..P46) | 关联评分 | L-qa-q × 5 | 5 维 QA 分量 | NA 处理 | Table 9 | 研究 × QA 矩阵 |

注：所有边均为 "原始研究" 单元上的属性共现，本文并未声明 typed edges、ontology relations 或形式 模型 elements。三元 cross-tab（goal × contribution × ML aspect）只在 Fig. 7 出现一次，未推广为通用 模式。

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表支持的统计观察（A1-M5）

均带分母 46，可作为候选迁回 review.md 主体；A2a 仍需回 PDF 复核精确数字：

- 43/46 提 effort reduction 为 goal；13/46 质量 improvement；11/46 stakeholder 理解。
- 31/46 supervised；4/46 reinforcement；0/46 仅 unsupervised；11/46 generic。
- 18/46 ML engineer 为目标用户；16/46 software engineer；11/46 domain expert。
- 35/46 含 code generator；30/46 含 DSL；21/46 含 框架。
- 23/46 graphical；21/46 textual；2/46 both。
- 34/46 新 DSL；9/46 GPL；3/46 language extension。
- 42/46 PIM；35 PIM-only；6 PIM+PSM；1 CIM+PIM+PSM；2 CIM-only；2 PSM-only。
- 39/46 design-level；6/46 requirements-level；5/46 data-representation。
- 28/46 ML aspect = design&development；22/46 training；10/46 deployment；2/46 monitoring；1/46 文档。
- 35/46 M2T-only；4/46 M2M-only；7/46 both；46/46 forward-engineering。
- 36/46 ML 模型/training code；15/46 software/intermediate 模型；8/46 deployment config；4/46 数据集。
- 38/46 完整 auto；8/46 部分。
- 17/46 open-source 工具；6/46 proprietary；23/46 no 工具 mention。
- 89% academic；9% 工业（industrial）；P35 both。
- 23/46 case study；17/46 experiment；4/46 user 研究；2/46 criteria-based；8/46 无评价；4/23 工业（industrial） case study；1/17 工业（industrial） experiment。
- 33 数据集；MNIST 7/46；Iris 3/46。
- 19/46 未提 limitation；7/46 未提 future work。
- 88% 无 工业（industrial） 评价 与 user 研究；48% 仅评一面；17% 无 评价；46% 计划 enhancement future work；28% 计划 further 评价。
- QA 分布：19 good / 15 average / 12 poor。
- 75% 未讨论 可扩展性（scalability）；9/46 关注 responsible ML / human-centric。

#### 6.2 原文 discussion / 推荐 / 路线图 提出的候选发现（A1-M6）

§6 与 §7 给出的 10 项 路线图 建议（data for ML、solution focus、ML type、MDE details、solution maturity、low-code for domain experts、ML terminology consensus、可扩展性（scalability）、responsible ML、评价 rigor），均为作者解释性 发现，不等同最终领域定论；Paper2 应只接受其作 candidate / 边界锚点。

#### 6.3 对 Paper2 可迁移的方法学启发

- "RQ → 抽取 form section → feature 树 → Table → distribution → RQ Answer Summary → Discussion 路线图" 七段链是可迁移的制品链。
- 把"未提及 / 未提及"显式列为字段取值（而非缺失），让缺口本身可统计。
- 把 pragmatic categorization rule（如自称 case study 即归 case study）显式写入 模式。
- QA1–QA5 + NA 是 SLR 通用 rubric 模板。
- Inclusion/Exclusion 用 ID 化（I01..I04, E01..E10）便于后续审计追踪。

#### 6.4 绝不能迁移的领域结论

- 任何 "TensorFlow 主导 / EMF+Sirius+XTend 主导 / Python 主导 / supervised 主导 / unsupervised 缺位" 等具体生态结论。
- 任何 MDE4ML 特定 路线图行动项（如 low-code 平台、no-code 平台）。
- 3934 → 46 的具体数字、46 篇 语料、P1..P46 编号。

### 7. 对旧版 `review.md` 的返修来源

按 C/I/M 分级。**学术目标判定**：本仓库的 A1-DT 任务是构建 Paper2 综述之综述的维度树脚手架，单篇 review.md 必须复原"原文样本编码模式"才能支撑后续 19×3 跨论文投影与 A2a 精核。以下建议聚焦学术目标层面。

#### C 级（critical，会导致 模式 复原失真，影响 Paper2 主统计池可信度）

1. **C-1：复原 Fig. 5 二级结构**。review.md §维度树复原与 §"原文模式主树（19×3 审计后返修）" 都没有把 Fig. 5 的 9 个一级子节点（Goal / Domain / End Users / Modeling / Supported ML Aspects / Tool Support / Evaluation / Scalability / Responsible ML）与 4 个 Modeling 二级子节点（Model Representation / Model Type / Model Level / Modeling Language）与 4 个 Tool Support 二级子节点（Meta Tool / Transformations / Generated Artifacts / Automation Level）显式列为节点。
   - **影响**：原生模式 主树未饱和，无法支撑 Paper2 跨论文 19×3 投影中"feature 树 节点级覆盖"指标。
   - **修法**：用本报告 §3 的 text-树 与 §4 叶子表替换 §"原文模式主树（19×3 审计后返修）" 中过于粗的六行主干；标注每节点的取值空间类型。

2. **C-2：Table 3–8 的封闭枚举未进入叶子取值空间**。当前 review.md 将 16 个目标子类、11 个 contribution、17 个 ML aspect 等都压成"自由文本加理由"或 模式种子（schema_seed） 占位，丢失了原文显式的封闭枚举。
   - **影响**：Paper2 在 A2a 阶段无法对 "Goal=降低工作量（降低工作量） × Sub-goal=Abstraction" 这类组合进行字段比对，等于把原文已有的 模式 退化为"建议自由抽取"。
   - **修法**：把 §4 叶子表中所有"完整枚举（n）"列直接迁入 review.md，让 A2a 只做"页码 + cell 核对"而不是重新发明取值空间。

3. **C-3：parallel 模式 缺失**。review.md 当前仅有"主树"概念，没有把 Inclusion/Exclusion gate（Table 1）与 QA1–QA5 rubric（§3.5、Table 9）作为并列 模式 节点登记。
   - **影响**：在跨论文投影中，"是否报告 质量量规"、"是否报告 inclusion gate"这两类元字段会被遗漏，影响 19×3 维度森林完整性。
   - **修法**：在 §维度树复原下增设 "Parallel 模式 (a) Inclusion/Exclusion"、"Parallel 模式 (b) QA rubric" 两个块，使用本报告 §4 末尾 L-qa-q / L-qa-band / L-inc-id / L-exc-id 四个叶子。

#### I 级（important，会影响审计性与统计可比性）

4. **I-1：3934 vs 3496 笔误**。当前 review.md §9 待复核已记录此项，但未在主统计页给出 canonical 数字。应在快速结论卡片 §1 末尾添加"分母口径：以 §3.3.2 中 3934 / 3570 为准，§7 中 3,496 为论文笔误"。
   - **影响**：若 Paper2 引用本篇分母时直接抄 §7，将传播错误。

5. **I-2：数据抽取 form 字段数 40 / 5 section / 23 short answer / 10 long answer / 2 checkbox / 14 radio button** 未进 review.md，但这是其他 SLR 几乎不会披露的元信息，是本篇对 Paper2 最具方法论价值的资料之一。应在 §维度树复原 中独立设节点 "Extraction-form 模式 shape"，叶子取值空间显式给出"(40, 5, 23/10/2/14)"四元组。

6. **I-3：Fig. 7 bubble chart 是三元 cross-tab**（goal × contribution × ML aspect）。review.md 完全未将其作为关系边或三元关系登记。建议在 §维度树复原 增加 "Cross-tab / Bubble chart" 小节，对应本报告 §5 关系边表。

7. **I-4：A.2 证据账本与 A.3 结论映射目前仅 4 行**（EV-001..004）。原文 RQ1–RQ4 各自的统计结论（如 43/46、35/46、88%）应每个 RQ 至少一行独立证据；A.3 至少应区分 "树类型（tree_type） / 叶子_definition / migration_boundary / 候选发现（candidate_finding） / source_schema_candidate / audit_repair / number_inconsistency"。建议按本报告 §8 草案扩到 ≥10 行。

8. **I-5：原生模式 是单树 + 双 parallel 模式 的小森林**，而非现在 §0 卡片中标的"维度森林"或"降级树"二选一。应在快速结论卡片新增字段："模式 形态 = 单根主树 (Fig.5) + 2 个 parallel 模式 (Inclusion/Exclusion gate, QA1–QA5 rubric)"。

#### M 级（minor，不阻塞合并）

9. **M-1：review.md §维度树复原 中"原生树类型 / 主统计池资格"叙述偏文学化**（"维度树主类型为 MDE4ML 生命周期分类树"）。这与 Fig. 5 实际根节点 "MDE Solution for ML"（更接近"解决方案 × 评价 × 限制"轴）不完全一致；建议把"生命周期分类树"替换为更准确的"MDE solution feature 树"。

10. **M-2：§"原文模式候选叶子映射（A1 种子）" 表的 5 行候选叶子（orig-ml-lifecycle / orig-mde-制品 / orig-solution-type / orig-motivation-benefit / orig-评价-context）粒度模糊**，与 §维度树复原 中的 b1/b2/b3/b4/b5 五大主干并未一一对齐，且 ml-lifecycle 同时被 b1 与 b4 引用。建议按本报告 §3 text-树 重整。

11. **M-3：SUMMARY 当前表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"项**（如果 SUMMARY.md 沿用 review.md §0 卡片的口径）：应保持"原始研究 / 46 / 单根主树 + 2 parallel 模式 / 主统计池资格成立但数字仍待 A2a 复核"四字段。

#### 是否需要重写 §"维度树复原" 主体

**是**。当前 §"维度树复原" 与 §"原文模式主树（19×3 审计后返修）" 是 v1 → v2 过渡的双层结构，互相覆盖且都偏粗。建议在下一轮 PR 中把这两节合并为一个 §"原生模式 主树（单根主树 + 2 个 parallel 模式）"，直接挂载本报告 §3 完整 text-树 与 §4 叶子表。

### 8. 历史审计草案归档（禁止消费为事实真源）

> [!WARNING] 历史草案归档，禁止消费为事实真源：本节仅保留 A1-DT v2 形成过程中的审计草稿，不得作为当前证据强度、SUMMARY 统计池、正式维度树或正式结论-证据映射使用。若本节与文末正式 `### A.1`--`### A.4` 审计附录冲突，一律以文末正式审计附录为准。

#### 历史 A.2 维度树证据账本草案（禁止消费）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §3.4, §4.1, Fig. 4–5, Table 2 | "We created a Google Form with 40 questions ... five sections" / "Fig. 5 shows a feature 树 of the examined features" | 释义：数据抽取 form 40 题 × 5 section；Fig. 5 是从 抽取 类别 派生的 feature 树 | 模式_source | medium | ROOT, §section-1, L-bib-* | true (Fig. 5 视觉版面) | 仅本 语料；feature 树 节点取值空间为 模式种子 |
| EV-002a | paper_content.txt | §3.5, Table 9 (Appendix B) | QA1..QA5 每篇 1..5 分或 NA | parallel-QA 模式 与每篇 研究 的 QA 矩阵 | rubric | medium | L-qa-q, L-qa-band, parallel-QA | true (Table 9 单元格抽取错位) | 不能直接外推为论文质量在领域内的相对评分 |
| EV-002b | paper_content.txt | §3.2, Table 1 | I01..I04 / E01..E10 | parallel-IE 模式：纳入排除 gate | 模式_source | 历史草稿旧强度（当前禁止采信） | L-inc-id, L-exc-id, parallel-IE | false（文本已逐条给出） | 仅本 SLR 适用 |
| EV-003a | paper_content.txt | §4.2.1, Table 3, Fig. 6(a) | "Effort Reduction was the most common aim mentioned in 43 out of 46 studies" | 释义：goal 与 sub-goal 的封闭枚举与 研究 P-list | 分类法 + statistical_result | medium | L-rq1-goal, L-rq1-subgoal | true (Fig. 6 Venn) | 频次需 A2a 数 P-list 验证 |
| EV-003b | paper_content.txt | §4.2.2, Table 4 | "31 studies (67%) explicitly focused on supervised ML, and 4 (9%) on reinforcement; 无更新 ... unsupervised" | ML 技术 4 大类 6 终端 | 分类法 + statistical_result | 历史草稿旧强度（当前禁止采信） | L-rq1-mltech | false | 仅本 语料；不可外推 |
| EV-003c | paper_content.txt | §4.2.3 | 11 application domains 列表 | 域分布 | 分类法 | medium | L-rq1-domain | false | 仅本 语料 |
| EV-003d | paper_content.txt | §4.2.4, Table 5, Fig. 6(c) | end user 3 类 7 角色，18/16/11 | 用户分布 | 分类法 + statistical_result | medium | L-rq1-enduser | true (Fig. 6c) | 仅本 语料 |
| EV-003e | paper_content.txt | §4.2.5, Table 6, Fig. 6(b) | contribution 11 类，35/30/21/... | contribution 分布 | 分类法 + statistical_result | medium | L-rq1-contrib | true (Fig. 6b Venn) | 仅本 语料 |
| EV-003f | paper_content.txt | §4.3.1, Fig. 8(a–b) | 模型 representation 23/21/2；language 34/9/3；level PIM 42/46 | modeling 维度分布 | statistical_result | medium | L-rq2-mrep, L-rq2-mlang, L-rq2-mlevel, L-rq2-mtype | true (Fig. 8) | 仅本 语料 |
| EV-003g | paper_content.txt | §4.3.2, Table 7, Fig. 9(a) | 17 机器学习环节；design 28 / train 22 / deploy 10 / monitor 2 / doc 1 | 机器学习环节 封闭枚举 + 频次 | 分类法 + statistical_result | medium | L-rq2-mlasp, L-rq2-mlfw | true (Fig. 9a) | 仅本 语料 |
| EV-003h | paper_content.txt | §4.3.3, Table 8, Fig. 8(c), Fig. 9(b) | M2T 35 / M2M 4 / both 7 / 全 forward；auto 38/8；工具 17/6/23；Python 15 / Java 10 / C++ 4；EMF 15, Sirius 10, XTend 5, EGL 4 | transformation/auto/工具 分布 + meta-工具 枚举 | statistical_result | medium | L-rq2-trans, L-rq2-art, L-rq2-tlang, L-rq2-autom, L-rq2-工具, L-rq2-metatool | true (Fig. 8c, Fig. 9b, Table 8) | 仅本 语料 |
| EV-003i | paper_content.txt | §4.4.1, §4.4.2, §4.4.3, Fig. 10(a–b) | academic 89% / 工业（industrial） 9% / P35 both；case 23 / exp 17 / user 4 / criteria 2 / 无更新 8；工业（industrial）-CS 4, 工业（industrial）-exp 1；ML/MDE 指标 分布；33 数据集, MNIST 7, Iris 3 | 评价 维度分布 | statistical_result | medium | L-rq3-area, L-rq3-方法, L-rq3-工业（industrial）, L-rq3-mlmetric, L-rq3-mdemetric, L-rq3-数据集 | true (Fig. 10a–b) | 仅本 语料 |
| EV-003j | paper_content.txt | §4.5.1, §4.5.2 | 19/46 无 limitation；7/46 无 future work；3 类 limitation + 3 类 future work | limitation/未来工作 分类法 + 频次 | 分类法 + statistical_result | 历史草稿旧强度（当前禁止采信） | L-rq4-limscope, L-rq4-fwscope | false | 仅本 语料 |
| EV-004 | paper_content.txt | §5 (4 sub-sections) | "search string ... refined over several iterations" / "first author extracted ... close match" / "did not exclude any 研究 based on publication 质量" | 4 类 效度 威胁 与对策 | validity_self_report | medium | ROOT, migration boundary | false | 不能等同 inter-rater κ |
| EV-005 | paper_content.txt | §6.1.1–§6.1.7, §6.2.1–§6.2.2, §7 | 10 项 路线图 推荐 | discussion-派生候选发现（derived 候选发现） | 推荐 | weak (single-paper) | 候选发现 only | false | 仅作 边界锚点，不进 最终发现 |
| EV-006 | paper_content.txt | §7 Conclusion | "selected 46 highly relevant 原始研究 from an initial pool of 3,496 papers" | **疑似笔误**：与 §3.3.2 的 3934 不符 | number_inconsistency | 历史草稿旧强度（当前禁止采信） | ROOT 元数据 | false | 引用时必须以 §3.3.2 的 3934 / 3570 为准 |
| EV-007 | paper_content.txt | §"数据可获得性（Data availability）" | "SLR data is available at the following link MDE4MLSLRdata(Originaldata)" | 数据可用性声明 + GitHub 链接 (review.md 旧版抽取为 https://github.com/hiraa221/MDE4ML-SLR-Data/树/main) | replication_link | weak | ROOT, 复现性 | true (打开 GitHub 仓库) | 需当前可访问性与 license 复核 |

#### 历史 A.3 结论-证据映射草案（禁止消费）

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-01 | 本文原生模式 为单根主树（Fig. 5）+ 2 个 parallel 模式（Inclusion/Exclusion gate 与 QA1–QA5 rubric），构成小型维度森林 | 树类型（tree_type） | ROOT, parallel-IE, parallel-QA | EV-001, EV-002a, EV-002b | 历史草稿旧强度（当前禁止采信） | 直接迁入 review.md §0 卡片 | 仅本篇 |
| C-02 | 样本单位 = 原始研究，分母 = 46，筛选链 3934→3570→72→55→32→+14→46 | 语料 | ROOT | EV-001, EV-006 | 历史草稿旧强度（当前禁止采信） | 直接迁入 SUMMARY 总账 | §7 中"3,496" 为笔误 |
| C-03 | 主统计池资格成立但数字仍需 A2a PDF 复核（特别是 Fig. 4 / Fig. 6 / Fig. 7 / Fig. 8 / Fig. 9 / Fig. 10 / Table 9） | pool_eligibility | ROOT | EV-001, EV-003*, EV-004 | medium | 当前 A1-DT 阶段 模式种子（schema_seed）；不写入 final stats | 文本抽取不可替代视觉版面 |
| C-04 | RQ1–RQ4 各 RQ 都映射到 抽取-form section、feature-树 子树与 Answer Summary 三层；这是历史草稿曾提出迁移建议；当前禁止直接采信到 Paper2 的方法学制品链 | method_pattern | §RQ1..§RQ4 子树 | EV-001, EV-003a–j | 历史草稿旧强度（当前禁止采信） | Paper2 可作为 模式种子 | 不迁移领域结论 |
| C-05 | "未提及（未提及）" 作为显式取值（而非缺失）是本篇的关键审计选择（工具 可获得性、ML 指标、MDE 指标、limitations、future work 都给出 未提及 频次） | schema_design | L-rq2-工具, L-rq3-mlmetric, L-rq3-mdemetric, L-rq4-limscope, L-rq4-fwscope | EV-003h, EV-003i, EV-003j | 历史草稿旧强度（当前禁止采信） | Paper2 可借鉴 | 需在 prompt / form 显式给出 not_mentioned 选项 |
| C-06 | Fig. 7 给出 goal × contribution × ML aspect 的三元 cross-tab，是本篇唯一的关系型可视化 | relation_evidence | R-goal-aspect, R-contrib-aspect | EV-003a, EV-003e, EV-003g（Fig. 7 注释） | weak | 可迁结构为"三元字段共现矩阵"模板 | 视觉 bubble 频次需 PDF 复核 |
| C-07 | §6 / §7 的 10 项 路线图 是作者解释性 候选发现，不能升级为 最终研究发现（最终研究发现） | 候选发现边界（candidate_finding_boundary） | §RQ4, §6, §7 | EV-005 | 历史草稿旧强度（当前禁止采信） | Paper2 仅作 边界锚点 | 未经跨论文证据 + 反证 + 研究者裁决 |
| C-08 | 本篇 效度 章节给出对策但未报告 Cohen κ、双盲编码或 disagreement 统计；"close match" 不可视作强一致性证据 | validity_boundary | §5 | EV-004 | medium | Paper2 应在自身审计中补足 inter-rater 证据 | 不削弱本篇结论效力，但限制其外推 |
| C-09 | §7 中 "3,496" 与 §3.3.2 中 "3934" 不一致，应以方法节为 canonical 数字 | number_inconsistency | ROOT | EV-006 | 历史草稿旧强度（当前禁止采信） | 引用本篇时直接使用 3934 / 3570 | 仅笔误，不影响整体结论 |
| C-10 | 数据可获得性（Data 可获得性） 给出 GitHub 仓库链接（review.md 已抽取为 hiraa221/MDE4ML-SLR-Data），是开放数据 SLR 的样本 | replication | ROOT | EV-007 | weak | 进入 SUMMARY 复现资产盘点 | 当前可访问性、license、内容范围未复核 |

### 9. 技能使用与自我审查记录

#### 9.1 技能 / 指南文件采用的原则

由于本任务运行环境为本仓库 Claude Code 而非 Codex CLI，`~/.codex/skills/*` 与 `~/.codex/plugins/*` 路径不在 Read 工具默认沙箱内（属于 codex 本地配置），无法在本会话直接通过 Read 读取它们的全文。这是任务 prompt 明确要求记录为 `blocked` 的边界。即便如此，本报告在结构上仍按以下技能精神组织（精神来自任务 prompt 与本仓库 CLAUDE.md 中既有的 A1-DT v2 口径，等同于这些技能文件在 Claude Code 环境中的可执行投影）：

- **`ai-research-writing-skill / reviewer-guidelines`**：reviewer 必须先复原 ground truth 再批评；C/I/M 分级要绑定学术目标；不接受空洞 "writing improvement"。本报告 §7 严格按 C/I/M 分层并写明影响。
- **`ai-research-writing-skill / reviewer-self-review`**：reviewer 在出报告前先反向检查自己。本报告 §9.2 给出最高风险三条与复核方式。
- **`research-planning / planning-prompts & output-schemas`**：单篇审计先回答样本单位 → 模式 → 取值空间 → 关系 → 统计资格五问；本报告 §2、§3、§4、§5、§6 对应。
- **`oh-my-codex / autoresearch`**：证据账本（A.2）与结论映射（A.3）必须分离；本报告 §8 给出 A.2/A.3 两表。

#### 9.2 reviewer 视角的最高风险三条

1. **本审计未做 PDF 视觉复核**。Fig. 4–10 与 Table 9 的具体数字均来自 `paper_content.txt`，可能存在版面错位。主线程合并时应至少打开 PDF 第 11–15 页（Fig. 8 / Fig. 9 / Fig. 10 / Table 7 / Table 8）与第 19 页（Table 9 Appendix B）进行视觉对照，并把 §4 叶子表中所有"完整枚举（n）"的 n 与 PDF 一致性核对一遍。
2. **三元 cross-tab（Fig. 7 bubble chart）只能从文字旁注推断**。"design and development 与 training 为最常见 ML aspect"是 §4.2.5 末尾文字结论，bubble 大小未在 text 中读到。R-goal-aspect / R-contrib-aspect 关系边的证据强度只能定为 weak，必须 A2a 视觉读图。
3. **3934 vs 3496 笔误本身可能不是笔误**。存在一种解释是 §7 误将 3934 减去某次去重前的中间数（如 3570 - 74 - ...）；建议主线程在 A2a 阶段尝试请求作者复现包或勘误，确认 canonical 数字。在此之前任何 Paper2 引用都应使用 §3.3.2 的 3934 / 3570 / 72 / 55 / 32 / 46 链。

#### 9.3 blocked / timeout / 文件缺失说明

- **blocked**：`~/.codex/skills/*` 与 `~/.codex/plugins/cache/oh-my-codex-local/*` 在 Claude Code 沙箱不可直接 Read，需在 Codex CLI 环境复跑才能取到原文。本报告以 prompt 中已显式给出的 A1-DT v2 口径与本仓库 CLAUDE.md 既有规则为可执行替代。
- **未发生**：timeout、其他文件缺失。`paper_content.txt`、`review.md`、`metadata.json`、`bibtex.bib` 均已本地完整读取；`paper.pdf` 文件存在但本轮未打开视觉版面。
- **未启动 subagent**：本任务由当前 Claude 单 智能体 独立完成，未派生任何 sub-subagent / nested 智能体 / 后台 智能体。
- **未修改任何仓库文件、未 commit、未 push、未 gh comment**。

— 报告结束 —

> [!NOTE]
> v2 返修后记：以上“对旧版 `review.md` 的返修来源”和审计草案是 A1-DT v2 返修前的独立审计输入；当前文件已经在[维度树复原](#维度树复原)与文末 A.1--A.4 中完成主线程裁决和返修。本审计报告保留为历史归档，不再作为当前状态判定依据。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/mde-ml-components-slr.md](../../audits/a1dt-v2-19x3/adjudications/mde-ml-components-slr.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-mde-ml-components-slr-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-mde-ml-components-slr-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-mde-ml-components-slr-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-mde-ml-components-slr-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mde-ml-components-slr-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mde-ml-components-slr-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/mde-ml-components-slr__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mde-ml-components-slr-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/mde-ml-components-slr.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见上文“维度树复原”的叶子维度表、关系边表和审计草案。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-mde-ml-components-slr-type | clm-mde-ml-components-slr-type | src-mde-ml-components-slr-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：**SLR**（Kitchenham guidelines 显式声明，protocol → planning/conducting/reporting） | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-mde-ml-components-slr-unit | clm-mde-ml-components-slr-unit | src-mde-ml-components-slr-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**原始研究**，编号 P1–P46，46 篇 | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-mde-ml-components-slr-denom | clm-mde-ml-components-slr-denom | src-mde-ml-components-slr-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：自动检索 3934 → 去重 3570 → title/abstract 72 → brief full-paper 55 → detailed reading 32 → snowballing +14（前向 8 + 后向 6）→ **46**（其中 conclusion §7 误写为 “3,496 papers”，与方法 §3.3.2 中 3934 不一致） | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-mde-ml-components-slr-tree | clm-mde-ml-components-slr-tree | src-mde-ml-components-slr-text; src-mde-ml-components-slr-codex; src-mde-ml-components-slr-claude; src-mde-ml-components-slr-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**单根维度树**（Fig. 5 "Features of selected 原始研究"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 schema 与 QA1–QA5 质量 rubric 两个并列 schema；不构成维度森林 | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-mde-ml-components-slr-pool | clm-mde-ml-components-slr-pool | src-mde-ml-components-slr-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-mde-ml-components-slr-type | A1DT-mde-ml-components-slr-C01 | 本文原文类型为：**SLR**（Kitchenham guidelines 显式声明，protocol → planning/conducting/reporting） | paper_type | type | ev-mde-ml-components-slr-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-mde-ml-components-slr-unit | A1DT-mde-ml-components-slr-C02 | 本文被编码样本单位为：**原始研究**，编号 P1–P46，46 篇 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-mde-ml-components-slr-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-mde-ml-components-slr-tree | A1DT-mde-ml-components-slr-C03 | 本文原生维度树 / 维度森林为：**单根维度树**（Fig. 5 "Features of selected 原始研究"，根节点为 MDE Solution for ML），辅以 Table 1 纳排 schema 与 QA1–QA5 质量 rubric 两个并列 schema；不构成维度森林 | 树类型（tree_type） | native_tree | ev-mde-ml-components-slr-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-mde-ml-components-slr-pool | A1DT-mde-ml-components-slr-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-mde-ml-components-slr-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-mde-ml-components-slr-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-mde-ml-components-slr-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-mde-ml-components-slr-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
