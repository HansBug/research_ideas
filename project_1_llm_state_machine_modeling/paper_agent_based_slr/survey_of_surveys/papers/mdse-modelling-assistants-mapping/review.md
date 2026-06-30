# Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping

## 0. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping |
| 作者 | David Mosquera; Marcela Ruiz; Óscar Pastor; Jürgen Spielberger |
| 年份 / 日期 | 2024；在线发表 2024-05-21；卷期为 IST 173:107492 |
| 类型 | systematic mapping；同时包含 literature mapping + practice documentation review |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| DOI | <https://doi.org/10.1016/j.infsof.2024.107492> |
| 本地核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 阅读状态 | 已读全文文本-paper_content核验；用 `pdftotext` 从 [paper.pdf](./paper.pdf) 局部核对 Table 2/3/4 的版式文本；图形数值仍待人工视觉核对 |
| 证据等级 | 全文文本级；关键表格为 PDF 文本核对级；bubble chart / Fig. 4--15 的视觉细节仍待 PDF 人工核对 |
| 研究对象 | 面向 MDSE / low-code / no-code 工具中“辅助人类完成软件建模任务”的 proposals；不局限特定技术、策略或领域 |
| 文献分母 | 3,176 条 screened records；最终纳入 58 个研究 proposals |
| 实践分母 | Gartner Magic Quadrant 2023 中 17 个 enterprise low-code application platform；7 个工具文档中找到 15 个 modelling assistance proposals |
| 核心产物 | strategy / goal / limitation / metric / target user 五棵维度树，外加 literature-vs-practice 对照 |
| 对 Project1 的价值 | 与 LLM4Modeling / STM generation 高度贴近：可直接迁移为“状态机建模 assistant”维度骨架，尤其适合抽取 assistant strategy、goal、limitation、metric、target user 字段 |
| 对 Paper2 的价值 | 是 A1-M1 脚手架强样本：展示如何从系统映射中形成可执行字段树、如何把统计观察转成候选 finding，以及为什么 limitation / metric / user 缺失本身应成为 evidence field |
| 主要风险 | 原文依赖作者术语聚类；tool/method/framework 等边界主观；实践侧只看公开文档和 GMQ；对 AI/LLM 的论述主要是未来判断，不是实证结果；Table 3 中 limitation 数量口径存在“五类/六类”不一致，需复核 |

**一句话结论**：这篇 IST 2024 mapping 是当前 `survey_of_surveys` 中最贴近 Project1 LLM4Modeling / STM generation 的脚手架样本；最值得迁移的不是具体比例，而是“strategy--goal--limitation--metric--user”的树状元维度，以及把 `not specified / not evaluated / not found` 当成一等字段而非空值的报告方式。

## 1. 全文内容详读

### 1.1 背景与问题定位

原文把 MDSE、model-driven development、model-based development、low-code 和 no-code 工具共同视为“以模型而非代码作为主要输入来生成软件”的工具族。它们承诺提升软件开发团队生产率、降低 time-to-market，并因为“建模”降低了非 IT 专家参与软件生产的门槛。但现实中，MDSE 工具仍要求团队投入大量精力创建、维护、调试模型，因此 modelling assistance 成为 MDSE 采用和可用性提升的关键问题。

原文采用的核心定义是：**modelling assistance 是任何旨在辅助人类在 MDSE 工具中完成软件建模任务的 strategy，包括 method、technique、framework、guideline 等**。这个定义对 Project1 很重要：LLM4STM / STM generation 不应只被描述为“生成器”，更可以被放进“辅助人类建模”的 assistant 框架中，进一步分析它辅助的是建模创建、模型一致性、修复、验证、解释还是用户交互。

相关工作部分把既有 review 分为两类：

1. **面向开发 MDE 工具的 modelling assistance review**：关注辅助 model-driven engineers 创建 MDSE 工具或语言，偏 meta-modelling，不是普通 MDSE 工具用户的建模活动。
2. **面向 MDSE 工具用户、但限制特定 strategy 的 review**：例如 recommender systems、elicitation techniques、collaborative MDSE 等，能够说明局部策略，但缺乏跨策略全景。

因此本文的缺口是：缺少一个同时覆盖 literature 和 practice、且不按具体技术 / strategy / domain 预先收窄的 MDSE modelling assistance mapping。

### 1.2 研究问题设计

原文先提出主研究问题：

- **MRQ**：literature 和 practice 中有哪些 proposals 用于辅助人类在 MDSE 工具中完成 modelling tasks？

随后将 MRQ 拆成 literature 侧三个 RQ，并在 practice 侧补充 RQ4：

| RQ | 内容 | 预期抽取对象 |
|---|---|---|
| RQ1 | How is software modelling assisted? | modelling assistance strategies：tool / method / technique / framework / guideline / language 等 |
| RQ2 | What goals and limitations do existing modelling assistance proposals report? | goals 与 limitations，含未报告情况 |
| RQ3 | Which evaluation metrics and target users do existing modelling assistance proposals consider? | empirical evaluation metrics 与 target users，含 not evaluated / not specified |
| RQ4 | What is the state of the practice on modelling assistance? | 从 Gartner Magic Quadrant 中的 MDSE / low-code 工具公开文档抽取 strategy、goal、limitation、metric、user |

值得注意的是，RQ 设计不是只问“有哪些工具”，而是同时问 **goals、limitations、metrics、target users**。这正是后续 Project1 / Paper2 应迁移的树状字段：LLM4STM assistant 的价值不能只由“能不能生成状态机”判断，还必须说明目标用户、适用范围、限制、评价指标和交互定位。

### 1.3 检索、筛选、质量评价与数据抽取

检索策略采用 database search + snowballing 双路径：

1. 数据库：IEEE Xplore、ACM Digital Library、Scopus、Springer Link、Web of Science。
2. 关键词构造：基于 PICO；population 是 MDSE / MDE / MDD / MDA / MBSE / low-code / no-code，intervention 是 assist / support / help / ease / facilitate / user / developer / tester / architect / assistant 等。
3. 时间范围：1985--2024。
4. snowballing：先用数据库结果按 inclusion/exclusion 选出候选，再取质量评价 top 12 作为 backward / forward snowballing 初始集，直到没有新记录。

纳排标准重点是“某篇论文是否专门提出一个 proposal 来辅助 MDSE 工具用户完成 modelling tasks”。排除包括：不是以 modelling assistance 为主要贡献、非 SE、非英文、非同行评审、全文不可得。这里对 Project1 有一个重要启发：若后续做 LLM4STM seed corpus，不能把所有“模型生成 / 代码生成 / diagram 工具”都收入，必须区分是否真正辅助目标建模任务。

质量评价采用 3-point Likert questionnaire，混合 subjective 与 objective 项：subjective 包括 proposal 是否清晰、limitations/goals 是否清晰、工具/源码是否可下载、是否有案例、是否经验评价、用户是否清楚、结果是否清楚；objective 包括 venue 重要性和 citation 数。该 QA 不只是评分，也服务于 snowballing 初始集选择。

执行结果：

- database search 得到 1,996 条记录，并加入 5 条外部 reviewer 建议记录，共 2,001 条初筛；
- 初筛得到 51 个 possible proposals；
- 选取质量评价 top 12 进入 snowballing；
- 4 轮 snowballing 新 review 1,175 条记录；
- 总共 screened 3,176 条 records，得到 77 个 possible proposals；
- 经过 R3/R4 复核与讨论，最终纳入 58 个 proposals；
- inclusion agreement 的 K-statistic 为 0.634；clustering 复核后的 K-statistic 为 0.651，均按 Landis and Koch 解释为 substantial agreement。

数据抽取规则是按 RQ 抽取原文片段：RQ1 抽 strategy keywords；RQ2 抽 goals 与 limitations；RQ3 抽 evaluation metrics 与 target users；若作者未报告就留空。之后再基于作者术语进行 clustering。这个过程的优点是可追溯到原文文本，风险是 cluster ontology 受作者术语与研究者解释影响。

### 1.4 研究侧 proposals 与实践侧工具

研究侧纳入 58 个 proposals，原文按 strategy、goal、limitation、metric、user 建立 cluster 并做分布分析。实践侧不是从论文检索，而是从 Gartner Magic Quadrant 2023 for enterprise low-code application platforms 中抽取 17 个工具：leaders、challengers、visionaries、niche players 四类。作者查阅每个工具的 documentation / website / user guide，寻找 modelling assistance 相关描述，并将文档 quote 映射到与 RQ1--RQ3 相同的 cluster 体系。

实践侧关键观察：

- 17 个 GMQ 工具中，10 个没有找到 modelling assistance 文档；7 个工具有相关文档；
- 7 个工具中发现 15 个 practice proposals；
- practice 中 strategy 主要表现为 tool，例如 AI capability、template、scanner、recommender、model inspector、AI assistant、intelligent wizard；
- practice 文档通常会写 goals，但很少清楚写 limitations、evaluation metrics 和 target users；
- 文档常使用第二人称 “you”，导致 target user 被隐藏。

这对 Project1 很关键：如果后续对比工业 modelling assistant，公开文档缺失不能被解释成“工具没有该能力”，只能写成“未发现公开文档证据”。

### 1.5 建模辅助策略：RQ1

原文从 58 个研究 proposals 中抽出六类 strategy clusters：

| strategy cluster | 原文定义 / 直观含义 | 典型子类 |
|---|---|---|
| Tools | 执行建模辅助任务的软件实现 | recommender systems、AI software assistants、bots、plugins、view managers、testing tools、transformation-based tools、collaboration tools |
| Guidelines | 建议何时、何处、如何辅助建模的步骤或规则 | ISO-based standardisation、flexible workflow、refactoring process、multi-modelling architecture |
| Techniques | 将预定义 guideline 与工具结合起来完成辅助任务 | model development、model validation、model repair techniques |
| Methods | 将 people、processes、techniques 组织成一组建模辅助指令 | consistency validation、model repair、task-driven reuse、MDE model alignment methods |
| Frameworks | 描述一组 elements 及其关系的黑盒式辅助框架，可带工具支持 | change propagation、testing、collaborative modelling、co-evolution、formal frameworks |
| Languages | 修改或包含 modelling language 以辅助建模 | mega-modelling language、UML extension、modelling template |

分布上，Tools 最常见，占 39.7%；Frameworks 19.0%；Techniques 15.5%；Methods 13.8%；Guidelines 6.9%；Languages 5.2%。作者进一步指出 93.1% proposals 使用完全或部分 software implementation 来辅助建模，非软件 guideline 较少。

对 LLM4STM 的直接映射：LLM-based state machine generation assistant 很可能同时有 Tool、Method、Framework 属性，但原文为了统计将每个 proposal 放入一个 cluster。Project1 不能照搬单标签做法；更适合采用主 strategy + 辅助 strategy + evidence anchor 的多值字段，否则 LLM agent loop / prompt protocol / DSL checker / repair loop 这类混合系统会被过度压扁。

### 1.6 目标与限制：RQ2

原文提出七类 goals：

| goal cluster | 含义 | 对 STM generation 的映射 |
|---|---|---|
| G1 addressing change propagation | 理解、追踪、检测、修复模型变化影响 | 状态机变更后的迁移 / guard / invariant 影响追踪 |
| G2 enhancing consistency checking | 模型内部、模型间、模型与代码/需求之间一致性检查 | 需求--状态--迁移--变量--事件一致性；DSL semantic diagnostics |
| G3 ensuring model compatibility | 与组件化软件或运行环境兼容 | 生成模型是否符合 pyfcstm / UPPAAL / DSL 目标格式 |
| G4 improving model quality | 同时覆盖验证、确认、探索等多个质量方面 | correctness、completeness、traceability、verifiability 综合质量 |
| G5 improving user interaction | 降低认知负担、增强交互、解释差异、指导建模 | 交互式澄清、生成解释、repair suggestion、human gate |
| G6 easing model evolution | 自动生成模型、支持 co-evolution / reuse / element suggestion | 从需求生成状态机、迭代补全模型、修复已有模型 |
| G7 supporting vulnerability detection | 检测安全/隐私相关弱点 | 控制系统安全约束、危险状态、违反 safety requirement 的路径检测 |

结果上，31.0% proposals 主要帮助创建模型（G6），43.1% 帮助 refinement（G1/G2/G3/G4/G7），25.9% 同时帮助创建和 refinement（G5）。这与 Project1 的 “generation--verification--repair” 生命周期高度吻合：STM generation 不只是 G6，还天然连接 G2/G4/G5/G1。

limitations 方面，正文概述称有 five limitation clusters，但 Table 3 实际列出 L1--L6，需作为待复核口径记录：

| limitation cluster | 含义 | 对 STM generation 的风险映射 |
|---|---|---|
| L1 accuracy | 自动抽取、建议、修复结果不准确 | LLM 生成错误状态、错误 guard、错误 transition、hallucinated event |
| L2 effort | 引入额外维护、标准化或人工任务 | prompt 准备、需求整理、人工审查、repair loop 成本 |
| L3 generality | 受 domain、refactoring type、training data、scenario 限制 | 只适用于某些控制系统、需求格式、DSL 子集或模型规模 |
| L4 learnability | 用户需学习额外语言、技术或决策方式 | 研究者/工程师需理解 DSL、反馈格式、formal diagnostics |
| L5 scope | 缺少特定约束、组件、功能、模型类型支持 | 不支持层次状态、时间约束、并发、复杂变量、异常路径 |
| L6 usability | 可用性功能不足或尚未评估 | 交互流程、错误解释、IDE/CLI 体验、human gate 可用性不足 |
| L-NS | 作者未显式报告 limitations | prior work / baseline 的限制缺失本身应作为字段记录 |

作者发现只有一半 proposals 明确报告 limitations。对 Paper2 来说，这说明“缺失字段”不是简单空白，而是重要发现来源：如果 LLM4STM 文献不报告 target users、limitations 或 metrics，那么 Paper2 的 evidence table 应明确计数并把它纳入 candidate finding，而不是在叙述里隐去。

### 1.7 评价指标与目标用户：RQ3

metrics 方面，原文参考 Technology Acceptance Model，将评价指标聚为三类：

| metric cluster | 含义 | 典型原文指标 | 对 STM generation 的可迁移指标 |
|---|---|---|---|
| M1 effectiveness | proposal 达成目标的程度 | detected faults、F-measure、accuracy、recall、precision、accepted suggestions | parse/semantic pass rate、requirement coverage、transition correctness、repair success、property violation detection |
| M2 efficiency | 应用 proposal 所需 effort | modelling time、completion time、execution time、recommendation time、performance | token/cost、wall-clock time、人工审查时间、repair iterations、model completion time |
| M3 user perception | perceived usefulness / ease of use / adoption intention | perceived usefulness、industrial adoption perception | domain expert trust、modeller perceived control、debuggability、explanation usefulness |
| NE | 未评价或未给指标 | -- | 必须保留为 `not evaluated`，不能当作 0 或未知混写 |

研究侧 47.2% metrics 是 effectiveness / efficiency；user perception 只有 4.2%；48.6% proposals 没有评价指标或未评价。这个结果对 LLM4STM 非常警示：只报告自动指标（如 pass rate）会复制既有 MDSE assistant 的评价缺口；应至少设计用户感知、解释可用性、审计成本等人机协同指标。

users 方面，原文聚为三类：

| user cluster | 含义 | 对 STM generation 的映射 |
|---|---|---|
| U1 designers/modellers | 直接指定模型或设计的人 | 状态机 modeller、requirements-to-model analyst、MDE engineer |
| U2 domain experts | 熟悉业务领域但未必懂建模的人 | 控制系统领域专家、安全需求专家、工业工程师 |
| U3 software developers | 开发人员或相关 SE 角色 | 实现状态机代码、维护 DSL / verification pipeline 的开发者 |
| U-NS | 只写 generic user 或 he/she，没有具体角色 | 必须作为 user specificity 风险记录 |

软件开发者是最常见 target user（29.3%），designers/modellers 27.6%，domain experts 13.8%，还有 29.3% 未指定 target user。实践侧更偏 software developers，domain experts 和 designers/modellers 很少被明确提及。这对 Project1 的影响是：LLM4STM 如果希望服务“非形式化需求到形式化状态机”，应明确 target user 是领域专家、建模专家还是验证工程师；不同用户决定 prompt、解释、审计门和评价指标。

### 1.8 综合结果与 future work

比较 literature 与 practice 后，原文给出几类主要 finding：

1. literature 与 practice 都重视 modelling assistance，且 practice 中 leader low-code tools 更常公开记录 assistant 能力。
2. literature 和 practice 都常见 G6 easing model evolution；practice 尤其偏向 AI assistant、template、scanner、recommender 等 tool strategy。
3. literature 更常讨论 G1 change propagation、G5 user interaction；practice 较少公开这些维度。
4. 两侧都缺少 limitations、evaluation metrics、target users 的明确报告；practice 缺失更严重。
5. practice target users 多偏 developers，domain experts / designers / modellers 被隐藏或不明确。
6. AI / LLM / GPT 的出现可能改变 modelling assistance strategy 与 goal，需要统一框架支持未来 assistant 设计。

future work 部分提出将本文 clusters 与既有 Intelligent Modelling Assistants framework、requirements elicitation framework 结合，并建设一个 public repository，用 strategy、goal、limitation、metric、user 等 clusters 来可视化新 assistant 与既有工作之间的关系。对 Paper2 来说，这相当于一个“维度 schema + evidence repository + similarity map”的雏形，可直接启发后续 candidate finding ledger 和 pattern library。

### 1.9 威胁与限制

原文 threats 结构较完整，分为 internal / construct / external validity：

| threat 类别 | 原文威胁 | 缓解 | 仍保留的限制 |
|---|---|---|---|
| Internal validity | selection bias | I/E criteria；多 reviewer；GMQ 作为实践工具入口 | GMQ 与 reviewer 判断仍可能遗漏相关工具 / studies |
| Internal validity | data extraction bias | 要求尽量多抽取 RQ 相关文本；第一/二作者复查 | human error 不可避免；practice 文档不完整；未文档化能力不可见 |
| Internal validity | subjective interpretation / cluster ontology | 基于作者术语；triangulation；报告 K-statistic；公开 raw data | tool / technique / method / framework 边界仍主观 |
| Internal validity | inter-rater reliability | 三位 reviewer；K-statistic 0.634 / 0.651 | 数据抽取阶段因文本为主未计算 K-statistic；reviewer fatigue |
| Construct validity | grey literature bias | 增加 GMQ practice review | 只看 GMQ 和公开文档，未纳入 reports / white papers 等其它灰色文献 |
| Construct validity | search bias | 五个数据库 + snowballing；top 12 quality seed | 数据库选择、snowballing 初始集和 GMQ 选择仍带偏差 |
| External validity | language bias | 只纳入英文 | 非英文 SE / MDSE proposals underrepresented |

对 Paper2 的元启发：validity threat 不能只放在论文末尾，而应转成方法设计要求，例如术语不稳定要有字段定义与冲突裁决，实践文档缺失要记录 `not found`，数据抽取主观性要有 source anchor、复核、agreement 或 adjudication log。

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 以 MRQ 统领 literature + practice，再拆成 strategy、goal/limitation、metric/user、practice state 四类 RQ；RQ 直接对应后续字段树。 | `paper_content.txt` §1、§3.1、§5；Page 1 abstract。 | 高度可迁移到 Paper2：先问“有哪些 assistant / studies”，再问维度、限制、指标、用户和实践状态。 | RQ 面向 MDSE assistant，不直接等同 LLM4STM 或 agent-based SLR；需重写目标对象与边界。 |
| dimension pattern | 核心字段树为 `strategy -> goals -> limitations -> metrics -> target users`，并保留 `not specified / not evaluated / not found`。 | `paper_content.txt` Table 2/3/4/5；§4.2--§5.2。 | 极强可迁移：适合 Project1 LLM4Modeling / STM generation，也适合 Paper2 的 dimension 模式种子。 | 原文多为单标签 cluster，混合型 LLM/agent 系统需多标签或主/辅标签；不能照搬所有取值。 |
| finding pattern | finding 从分布统计上升为缺口：software-based strategy 占主导、limitations/metrics/users 缺失、practice 文档不足、AI 将推动新 assistant 框架需求。 | `paper_content.txt` §4.2--§4.4、§5.2、§6、§8。 | 可迁移为 Paper2 的“统计观察 -> candidate finding -> 设计义务”模式。 | 这些 finding 是 MDSE assistant 领域事实，不是 LLM4STM 领域事实；只能作为启发或待验证假设。 |
| evidence presentation pattern | 使用 PRISMA-like flow、quality assessment、cluster tables、bubble charts、literature-vs-practice comparison、documentation quotes。 | `paper_content.txt` Fig. 2/3、Table 1--5、Fig. 4--13。 | 可迁移为 Paper2 证据呈现：分母、筛选流、字段表、交叉图、quote-to-cluster 映射。 | 图表视觉细节本轮未逐一人工核对；Table 5 的 practice quote 需后续回到网页 / 文档复核。 |
| validity / threat pattern | 明确报告 selection、extraction、subjective clustering、inter-rater、grey literature、search、language bias，并说明缓解与残余限制。 | `paper_content.txt` §7.1--§7.3。 | 可迁移为 Paper2 validity checklist；尤其是 terminology bias、not documented != not exist、cluster subjectivity。 | 原文没有把每个 cluster 的证据锚点做到 field-level ledger；Paper2 应比它更强。 |
| report structure pattern | 结构为 Introduction / Related Work / SMS design / SMS results / Practice review / Comparative analysis / Threats / Conclusions。 | `paper_content.txt` 目录与 §1--§8。 | 很适合写 Paper2 的 scaffold sample review：先系统方法，后结果，再 practice / comparative / threats。 | 该结构是 mapping 论文，不是方法论文；Paper2 还需突出审计优先 evidence engineering 方法与 evaluation。 |

## 3. A1-M0--M6 脚手架元维度贡献

> 说明：本节的 A1-M0--M6 指本 `survey_of_surveys/` 文库内部“脚手架元维度”，不是 S0 方法流程阶段，也不是原文 Table 3 中 L1--L6 limitation clusters。原文 limitation clusters 已在 §1.6 单独整理。

| A1-M 脚手架元维度 | 该论文提供的脚手架元维度贡献 | 可迁移字段 / 机制 | 对 LLM4STM / Paper2 的具体启发 |
|---|---|---|---|
| A1-M0：主题与综述元模型设定 | 原文清楚定义 “modelling assistance” 并排除 generic drawing tools、meta-modelling / MDSE tool development。 | `scope_definition`、`target_task`、`excluded_task`、`target_user_boundary`。 | LLM4STM 也要先定义是辅助“状态机建模任务”，不是泛 UML 画图、代码生成或模型检查工具。 |
| A1-M1：脚手架挖掘与种子探测 | Related work 分两组说明已有 review 的边界，并用专家咨询修订 RQ。 | `predecessor_review_group`、`gap_type`、`expert_consultation`。 | Paper2 可把此文作为脚手架样本：从既有 review 得到候选维度，再由研究者批准是否迁移。 |
| A1-M2：维度模式批准 | strategy / goal / limitation / metric / user 构成可执行抽取 schema，并定义每类 cluster。 | `assistant_strategy`、`goal_cluster`、`limitation_cluster`、`metric_cluster`、`target_user_cluster`、`missingness_code`。 | LLM4STM 的 extraction schema 不应只收“模型是否生成成功”，还要收目标、限制、指标、用户和缺失原因。 |
| A1-M3：论文收集与概览 | 记录数据库、PICO、search string、snowballing、I/E criteria、QA、最终 58 proposals；practice 侧记录 GMQ 17 tools。 | `search_source`、`screened_records`、`included_records`、`practice_tool_pool`、`documentation_status`。 | Paper2 可要求每个候选池都保留分母、筛选理由、practice/public-doc 状态，避免样本漂移。 |
| A1-M4：字段级证据抽取与模式演化 | 原文要求抽取原文片段，再基于文本聚类；practice 侧 Table 5 用 documentation quote 映射 cluster。 | `raw_text_fragment`、`quote_to_cluster`、`terminology_basis`、`cluster_decision`。 | Project1 应保留 requirement span / model span / diagnostic span 到字段值的证据链；不要只保留最终标签。 |
| A1-M5：统计分析 | 用比例、bubble chart、cluster cross-analysis 比较 strategy-goal-limitation、goal-metric-user、literature-vs-practice。 | `distribution_table`、`cross_tab`、`bubble_chart`、`comparison_axis`、`not_specified_rate`。 | Paper2 的统计观察可先形成 candidate signal，例如“目标用户未报告率高”，但不能直接写成领域结论。 |
| A1-M6：候选发现形成 | 从统计观察提出设计框架需求：limitations/metrics/users 缺失阻碍比较，AI disruption 需要 unified framework。 | `candidate_finding`、`supporting_statistic`、`design_implication`、`future_framework_need`。 | Paper2 可学习“统计 -> gap -> design implication”的写法，但要增加反向证据、主张强度和研究者裁决。 |

## 历史草稿（已迁移，不作事实真源）：旧第 4 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

以下字段树建议作为 Project1 LLM4Modeling / STM generation 方向的维度 pattern seed。字段名以英文为主，便于后续 schema 化；取值与说明用中文维护。

```text
modelling_assistant_review
├── study_metadata
│   ├── title / authors / year / venue / doi
│   ├── publication_type / venue_short_link / ccf_category / ccf_rank
│   ├── review_type = SMS / SLR / tertiary / practice review / mixed
│   └── evidence_level = title-abstract / fulltext / pdf-table / artifact
├── scope_definition
│   ├── target_domain = MDSE / LLM4Modeling / LLM4STM / low-code / no-code
│   ├── target_task = modelling / model repair / model validation / model tracing / model debugging / model evolution
│   ├── included_tool_family = MDSE tool / DSL tool / formal modelling tool / low-code platform
│   ├── excluded_scope = generic diagramming / meta-modelling / code-only generation / non-SE
│   └── practice_source = GMQ / vendor docs / tool docs / repository / none
├── search_and_selection
│   ├── search_strategy = database / snowballing / grey-literature / manual seed
│   ├── screened_records / included_records / candidate_records
│   ├── inclusion_criteria / exclusion_criteria
│   ├── quality_assessment_items
│   └── agreement_or_adjudication = kappa / discussion / single-reviewer / not reported
├── assistant_strategy
│   ├── primary_strategy = tool / guideline / technique / method / framework / language
│   ├── secondary_strategy[] = tool-supported method / agent workflow / prompt protocol / checker / repair loop
│   ├── software_based = yes / partial / no / unclear
│   ├── ai_based = no / rule-based / ML / LLM / agent / hybrid / unclear
│   ├── modelling_subtask
│   │   ├── suggest_elements
│   │   ├── create_models
│   │   ├── validate_or_check_consistency
│   │   ├── repair_or_refactor
│   │   ├── trace_changes
│   │   ├── visualize_or_explain
│   │   └── synchronize_or_collaborate
│   └── source_anchor = paper quote / table row / documentation quote / artifact link
├── goals
│   ├── G1_change_propagation
│   ├── G2_consistency_checking
│   ├── G3_model_compatibility
│   ├── G4_model_quality
│   ├── G5_user_interaction
│   ├── G6_model_evolution_or_generation
│   ├── G7_vulnerability_or_safety_detection
│   ├── create_refine_role = create / refine / both
│   └── goal_not_specified = true / false
├── limitations
│   ├── limitation_reporting_status = specified / not_specified / not_applicable
│   ├── L1_accuracy
│   ├── L2_effort
│   ├── L3_generality
│   ├── L4_learnability
│   ├── L5_scope
│   ├── L6_usability
│   ├── domain_specificity = domain-specific / cross-domain / unclear
│   ├── model_type_scope = state_machine / UML / DSL / process model / low-code app / unclear
│   └── residual_risk_note
├── evaluation_metrics
│   ├── evaluation_status = empirically_evaluated / not_evaluated / unclear
│   ├── M1_effectiveness
│   │   ├── parse_or_validity_rate
│   │   ├── semantic_correctness
│   │   ├── requirement_coverage
│   │   ├── precision_recall_f1
│   │   └── accepted_suggestions
│   ├── M2_efficiency
│   │   ├── modelling_time
│   │   ├── execution_time
│   │   ├── repair_iterations
│   │   ├── token_or_cost
│   │   └── human_review_time
│   ├── M3_user_perception
│   │   ├── perceived_usefulness
│   │   ├── perceived_control
│   │   ├── trust
│   │   ├── explanation_helpfulness
│   │   └── adoption_intention
│   └── metric_limitations
├── target_users
│   ├── user_reporting_status = specified / generic_user / not_specified
│   ├── U1_designers_or_modellers
│   ├── U2_domain_experts
│   ├── U3_software_developers
│   ├── verification_engineers
│   ├── safety_engineers
│   ├── novice_vs_expert = novice / junior / expert / mixed / unclear
│   └── user_role_evidence = direct quote / inferred / absent
├── practice_comparison
│   ├── market_tool_name
│   ├── documentation_found = found / not_found / access_failed
│   ├── documented_assistance_feature
│   ├── vendor_claim_type = speed / quality / security / productivity / education
│   ├── limitation_disclosed = yes / no
│   ├── metric_disclosed = yes / no
│   └── target_user_disclosed = yes / no / hidden_by_second_person
└── synthesis_outputs
    ├── distribution_observation
    ├── cross_axis_observation
    ├── candidate_gap
    ├── design_implication
    ├── threat_to_validity
    └── paper2_action_item
```

对 LLM4STM 的最小迁移版本建议先冻结 5 个强制字段组：`assistant_strategy`、`goals`、`limitations`、`evaluation_metrics`、`target_users`。如果一篇论文没有报告 limitations、metrics 或 users，应填 `not_specified` 并记录证据锚点，而不是空置。

## 5. 对 Project1 / Paper2 的启发与风险

### 5.1 对 Project1 LLM4Modeling / STM generation 的启发

1. **将 STM generation 重新表述为 modelling assistance，而不是孤立生成任务**：状态机生成可以是 G6 model evolution / generation，但如果引入 parser、semantic diagnostics、repair loop 和人类反馈，它同时涉及 G2 consistency checking、G4 model quality、G5 user interaction 和 G1 change propagation。
2. **目标用户必须前置**：面向 domain expert 的 LLM4STM assistant 与面向 modeller / developer 的 assistant 评价完全不同。前者强调自然语言解释、认知负担和可理解性；后者强调 DSL correctness、debugging、traceability、repair efficiency。
3. **metrics 不能只做自动正确率**：原文显示 MDSE assistance 领域已经偏向 effectiveness / efficiency，user perception 很少。Project1 若只报告 pass rate / transition accuracy，会延续该缺口；可补 user trust、perceived control、explanation usefulness、human review time。
4. **limitations 应成为主字段**：LLM4STM 常见风险可直接映射到 L1 accuracy、L3 generality、L5 scope、L2 effort、L6 usability。主动报告这些限制反而能增强论文可信度。
5. **practice vs literature 对照可作为额外视角**：若后续要讨论 low-code / modelling tools 中的 AI assistant，可借鉴本文 GMQ + documentation quote 方式，但必须标注公开文档的缺失边界。
6. **树状维度适合 STM 论文集抽取**：assistant strategy / goals / limitations / metrics / users 是天然的 `desc.md` 或 `review.md` 字段树，适合从多篇 LLM4Modeling 文献抽取对比矩阵。

### 5.2 对 Paper2 审计优先证据工程的启发

1. **A1-M1 脚手架价值很高**：本文展示了一个可以直接迁移到 Paper2 的维度 seed：研究对象、strategy、goal、limitation、metric、user、practice documentation。
2. **缺失值语义应显式化**：`not specified`、`not evaluated`、`not found` 在本文中参与统计和 finding 形成。Paper2 应将缺失语义写进 schema，而不是用空单元格。
3. **统计观察与 candidate finding 要分层**：本文从比例和分布推出“需要 unified framework”。Paper2 可以学习这种路线，但要更强地记录 supporting evidence、反向证据、主张强度、研究者裁决。
4. **terminology bias 是 schema 风险**：原文承认 tool / method / technique / framework 术语不统一。Paper2 需要在 schema 中记录 `terminology_basis = author_keyword / reviewer_interpretation / adjudicated`。
5. **practice evidence 需要 access / documentation 状态**：GMQ 工具中未找到文档不等于没有 assistant；Paper2 若处理工具、artifact、dataset 或 API，也应区分 `not documented`、`not accessible`、`not present`。
6. **source anchor 粒度可以进一步加强**：本文公开 raw data，但论文正文中的 cluster 多是表格和汇总。Paper2 若主张“审计优先”，应比本文更强，提供 field-level source span / page / table / quote anchor。

### 5.3 主要风险

1. **不能把本文结论直接当作 LLM4STM 领域 finding**：它覆盖 MDSE modelling assistance broadly，不是专门 LLM / state machine / control system。
2. **单标签 cluster 会压扁 hybrid LLM agent systems**：LLM4STM 往往同时是 tool、method、framework 和 guideline；后续 schema 应允许多标签或主/辅标签。
3. **实践侧 GMQ 只代表 enterprise low-code 市场的一种视角**：不覆盖 UPPAAL、Simulink/Stateflow、UML/SysML 工具、工业安全建模工具，也不覆盖开源 DSL 工具。
4. **AI disruption 论述是前瞻，不是已验证结果**：原文提到 LLM/GPT 会改变 modelling assistance，但它的纳入研究和 practice 文档不等于系统评估 LLM4Modeling。
5. **limitations cluster 口径需复核**：正文说 five limitation clusters，Table 3 列出 L1--L6，其中 L6 usability 只有一个 proposal；正式引用时要避免写错。
6. **metrics 与 formal verification 指标仍需扩展**：M1/M2/M3 对 STM generation 有帮助，但还不够覆盖 timed automata、model checking property satisfaction、counterexample usefulness 等 formal-method 指标。

## 历史草稿（已迁移，不作事实真源）：旧第 6 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

本轮只允许编辑单篇 [review.md](./review.md)，不回修全局 schema；但该文暴露出以下候选字段，建议后续 A2a/A2b 评估是否加入 [patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md)：

| 候选字段 | 触发原因 | 建议语义 |
|---|---|---|
| `assistant_strategy_tree` | 原文 strategy cluster 足够稳定，且与 LLM4STM 强相关 | 记录 primary / secondary strategy、software-based、AI-based、subtask |
| `goal_limitation_cross_axis` | 原文 Fig. 5 / Fig. 11 做 goal-limitation cross-analysis | 支持从二维关系而非单列分布生成 candidate finding |
| `metric_user_cross_axis` | 原文 Fig. 6 / Fig. 12 做 goal-metric-user cross-analysis | 记录目标用户是否被相应指标评价覆盖 |
| `missingness_code` | limitations、metrics、users 大量未报告 | 区分 not specified / not evaluated / not found / hidden by wording |
| `terminology_basis` | 原文承认 tool/method/framework 等术语不统一 | 标记 cluster 来自作者关键词还是 reviewer 归类 |
| `practice_documentation_status` | 17 个 GMQ 工具中 10 个未找到文档 | 避免把公开文档缺失误写为能力不存在 |
| `ai_disruption_claim_status` | 原文对 AI/LLM 是 future-facing 讨论 | 区分 empirical finding / future expectation / design implication |
| `target_user_specificity` | practice 文档常用 “you” 隐藏用户 | 记录 direct role、generic user、second-person-hidden、not specified |

## 7. 待复核

1. **PDF 视觉核对**：本轮已读 [paper_content.txt](./paper_content.txt)，并用 `pdftotext` 局部核对 Table 2/3/4；但 Fig. 4--15 的 bubble chart、flow chart 和 visual distribution 仍需人工打开 PDF 核对。
2. **Table 3 limitation 数量口径**：正文概述提到 five limitation clusters，但 Table 3 列出 L1 accuracy、L2 effort、L3 generality、L4 learnability、L5 scope、L6 usability；正式写作前需核对作者是否在其它位置解释 L6。
3. **Zenodo replication package**：原文给出 Zenodo 10262145；本轮未打开核验 raw extraction / clustering 数据，不能声称已复现实验数据。
4. **Practice 文档来源**：Table 5 中 Mendix、OutSystems、Power Apps、Salesforce、Appian、Oracle APEX、Retool 等 vendor quotes 本轮只读论文转录，未回到原始网页 / user guide 核对当前状态。
5. **GMQ 2023 来源与许可**：本轮没有核对 Gartner Magic Quadrant 原始报告，只能按论文叙述记录 17 个工具分母。
6. **CCF 信息**：metadata 已给出 IST / CCF B；正式文稿若引用 CCF 等级，仍建议回到 CCF 官方目录做一次日期化核验。
7. **OA 状态差异**：原文首页显示 Elsevier open access article under CC BY；metadata 中 `oa_status` 写 hybrid，正式总账可区分“期刊 hybrid / 该文 OA”。
8. **LLM4STM 迁移边界**：本文是 MDSE modelling assistance mapping；迁移到状态机生成时，需要补充 state machine-specific fields，如 state / event / variable / transition / guard / timing constraints / verification properties。
9. **相关 frameworks [81][103]**：原文 future work 提到 modelling assistant requirements framework 和 Intelligent Modelling Assistants framework，本轮未追踪原文；若 Paper2 使用 unified framework 论述，应补读这两篇。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 leaf / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生 schema。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__codex.md](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__codex.md)、[../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__claude.md](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__claude.md)、[../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__deepseek.md](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md](../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修 / needs repair”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 supplementary 精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `mdse-modelling-assistants-mapping` |
| agent | `claude`（Opus 4.7 [1m]，本会话由本进程直接执行） |
| 是否已读 `paper_content.txt` | 是；分段阅读 §1–§8（Page 1–18）及 References 起始部分；Table 1–5 文本核验 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；DOI 10.1016/j.infsof.2024.107492、IST 2024、CCF B、`evidence_role=systematic_mapping_dimension_pattern` 已记录 |
| 是否打开或核对 `paper.pdf` | 否（本审计只基于本地 `paper_content.txt` 文本与 `bibtex.bib` / `metadata.json`，未单独打开 PDF 视觉核验；图 4–15 的 bubble chart、PRISMA flow、Research Agenda 图等仍需 A2a 视觉核验） |
| 原文类型 | SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） |
| 被编码样本单位 | (a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） |
| 样本数量 / 分母 | 文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals |
| 原生树类型 | **维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） |
| 主统计池资格 | 局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 needs repair；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、supplementary 风险进入 A2a。 |

### 1. 原文证据阅读说明

本轮实际读取的本地文件与章节：

- `bibtex.bib`（全文 12 行）：确认标题、作者、DOI、IST 2024 元信息。
- `metadata.json`（全文 35 行）：确认 `evidence_role=systematic_mapping_dimension_pattern`、`eligible_for_statistical_synthesis=true`、`systematic_evidence_status=systematic_mapping`、CCF B / IST / hybrid OA。
- `paper_content.txt`：分段阅读 §1 Introduction（Page 1–2）、§2 Related work（Page 2–3）、§3 Systematic mapping study design 含 §3.1–§3.5（Page 3–5）、§4 Results 含 §4.1–§4.4（Page 5–10）、§5 State of the practice 含 §5.1–§5.2（Page 10–13）、§6 Comparative analysis（Page 13–14）、§7 Threats（Page 15）、§8 Conclusions（Page 15–17）、References 开头（Page 17–18）。Table 1（QA questionnaire）、Table 2（RQ1 clusters）、Table 3（RQ2 goals/limitations）、Table 4（RQ3 metrics/users）、Table 5（RQ4 practice quotes）的文本部分均已通读。
- `review.md`（既有 v1+19×3 返修版）：通读全文 564 行；当前 A1-DT v2 主干仍是六叶通用接口（`scope/corpus/taxonomy/method/evidence/finding`），原文真正编码 schema 被压在“原文模式候选叶子映射（A1 种子）”与“19×3 审计后返修”两个二级表中。

仅基于 text 文件做的判断，**仍需 PDF 视觉核验**的内容：

1. Fig. 4 RQ1 distribution、Fig. 5 G–L bubble、Fig. 6 M–U bubble、Fig. 11 S–G–L bubble、Fig. 12 G–M–U bubble、Fig. 13 lit-vs-practice 的具体数值与气泡半径口径；
2. Fig. 1（Research overview）、Fig. 2（SMS design overview）、Fig. 3（PRISMA flow）、Fig. 7（GMQ review overview）、Fig. 9/10（practice distributions）、Fig. 14（repository visualisation）、Fig. 15（research agenda）的精确节点与文字；
3. §4.3 文中“five limitation clusters”与 Table 3 中 L1–L6 的口径差异：是否在版式中存在 L6 的脚注 / inline 解释；
4. Zenodo replication package `10262145` 的 raw extraction 与 cluster CSV。

关键原文证据锚点（5–12 条，短引或释义）：

| # | 章节定位（page / 行近似） | 角色 | 简要释义或短引 |
|---|---|---|---|
| E1 | §1, Page 1, abstract & “Modelling assistance is the strategy—i.e., any method, technique, framework, or guideline—that aims to assist humans during software modelling tasks in MDSE tools.” | scope definition | 给出 modelling assistance 定义，并明确 unit = MDSE-tool-user-facing proposals |
| E2 | §1, Page 2, MRQ：“What proposals exist in the literature and practice to assist humans during modelling tasks in MDSE tools?” | RQ root | MRQ + 拆解为 RQ1/RQ2/RQ3 + 实践侧 RQ4 |
| E3 | §3.1, Page 3–4, RQ1/RQ2/RQ3 的精确措辞与“we expect to gather a set of tools, methods, techniques, and frameworks…” | 树根 → 主干字段 | 显式说明 extraction 字段：strategy / goals / limitations / metrics / target users |
| E4 | §3.5, Page 4–5：“RQ1: Extract the keywords the proposals’ authors use…; RQ2: …leave the field blank…; RQ3: …Leave the field blank if the authors do not state something…or if the authors use ‘user’ to refer to their target users.” | 抽取规则 + 缺失语义 | 原文显式定义“留空”=作者未报告；后续转为 L-NS / NE / U-NS 编码 |
| E5 | §3.5, Page 5 脚注 5：“we recognise that…definitions of method, framework, technique, and tool are still not unified…we rely on the keywords adopted by the proposals’ authors and our definition to each cluster.” | terminology bias | 作者承认 cluster 边界依赖作者术语 |
| E6 | §4.1, Page 5–6 与 Fig. 3：1,996 + 5 = 2,001 → 51 possible → top 12 seeds → 4 rounds snowballing → 1,175 records → total 3,176 screened → 77 possible → 58 included；K=0.634 / 0.651 | corpus pipeline | 系统检索分母与 inter-rater 数据 |
| E7 | §4.2, Table 2 + Fig. 4：Tools 39.7 %、Frameworks 19.0 %、Techniques 15.5 %、Methods 13.8 %、Guidelines 6.9 %、Languages 5.2 %；“93.1 % … totally or partially software implementations” | strategy taxonomy | 6-cluster 完整枚举 + 比例 |
| E8 | §4.3, Page 7：“we propose seven clusters about proposals’ goals and five clusters about proposals’ limitations.”，但 Table 3 列出 L1–L6（含 L6 usability 仅 [65]） + L-NS | **原文内部口径不一致** | 必须按 not_verified 保留，A2a 须做 PDF/Zenodo 复核 |
| E9 | §4.3, Page 8：分布 “G6 31.0 %（18）……G1/G2/G3/G4/G7 合 43.1 %（25）……G5 25.9 %（15）……50.0 % proposals 明确报告 limitations” | goal × create/refine 三分法 + limitation reporting rate | 直接量化 missingness |
| E10 | §4.4, Table 4 + Page 9：M1 effectiveness 23.6 %、M2 efficiency 23.6 %、M3 user perception 4.2 %、NE 48.6 %；U1 27.6 %、U2 13.8 %、U3 29.3 %、U-NS 29.3 % | metric / user 频次 | 量化 evaluation gap 与 user gap |
| E11 | §5.2, Table 5 + Fig. 9/10：17 GMQ tools → 10 NF + 7 D → 15 proposals；practice strategy=80 % Tool、goal=100 % 报告、limitation 报告 20 %、metric NF 73.3 %、user NF 73.3 % | practice projection | 与 literature 同一 schema 投影 + “you” 隐藏 target user |
| E12 | §6, Fig. 11/12/13；§7.1 terminology / subjective interpretation / inter-rater；§7.2 grey literature & search bias；§7.3 language bias | cross-axis + threats | 关系边与 validity 边界的证据来源 |

### 2. 样本单位与字段来源判定

1. **原文纳入与逐项描述的对象是什么？**
   - 主样本单位 = **primary study proposals**（n=58，每个 proposal 一行编码，引用 [20]–[77]）。
   - 辅样本单位 = **MDSE tools**（n=17 GMQ tools，作为 grey-literature carriers）与 **practice proposals**（n=15 documented assistance proposals inside 7 tools）。
   - 不是“按 RQ 列 finding”，也不是“按章节列工具”，而是“每条 proposal 一条记录、字段化编码、再聚类”。

2. **作者有没有系统检索 / 纳排 / 抽取 / 编码方案？**
   - 有完整系统流程：PICO 检索式（5 数据库）+ snowballing（4 轮，top-12 seeds 来自 QA）+ I/E criteria（I1–I2、E1–E5）+ 3-point Likert QA（Table 1）+ data extraction schema（RQ1 keywords / RQ2 goals & limitations / RQ3 metrics & users）+ 三 reviewer + K-statistic 报告。
   - 实践侧不是新数据库检索，而是 GMQ 2023 报告 → 17 tool 列表 → 公开文档 quote 抽取 → 同 schema 投影。

3. **原文字段来自哪里？**
   - 主 schema 来自 **§3.5 data extraction strategy + §4.2/§4.3/§4.4 cluster definitions + Table 2/3/4**。这是“extraction form + post-hoc cluster ontology”混合：先抽 author keywords，再由 R1 cluster、R4 复核、K-statistic 量化 agreement。
   - 缺失语义来自 §3.5 与 §4.3/§4.4 显式编码：`L-NS`（limitation not specified）、`NE`（not evaluated）、`U-NS`（generic “user” 或 “he/she” 隐藏的 target user）；practice 侧加 `NF`（documentation not found）。
   - replication package = Zenodo `10262145`，含 raw + clustered data（本审计未访问）。

4. **RQ 与样本单位的关系：**
   - RQ1–RQ3 = **样本字段定义**（按 RQ 提取并 cluster），不是结果分章。
   - RQ4 = **实践侧 schema 投影 + GMQ 分类辅助维度**。
   - MRQ 是树根问题；RQ 是“样本单位 → 字段树各主干”的桥。

5. **是否需要降级？**
   - **不降级**：本文确有系统样本库（58 + 15）、显式纳排、QA、K-statistic、replication package。可作为 schema-seed + 局部统计候选。
   - 但 **单标签 cluster**（§4.2 末尾：“we cluster each proposal in one cluster even if some overlap”）与 **作者术语 cluster**（§3.5 / §7.1 terminology bias）这两条边界必须与统计一起迁移；混合型 LLM/agent assistant 不能机械套用单标签。

### 3. 原生样本编码维度树（维度森林）

下面是按本文 §3.5 + §4.2/§4.3/§4.4 + Table 2/3/4 + §5 实际还原的**原生编码 schema**（替代 review.md 当前那六叶通用接口主树）：

```text
[ROOT] MDSE modelling assistance landscape (Mosquera et al. 2024)
│
├── [B-meta] Study & corpus metadata (per-proposal record key)
│   ├── proposal_id            // [20]..[77]; 1 row per proposal
│   ├── source_track           // database_search | snowballing | external_reviewer_suggestion
│   ├── inclusion_criteria_pass // I1, I2 (boolean each)
│   ├── exclusion_criteria_trigger // E1..E5 (one or more)
│   ├── quality_score           // 3-point Likert × 10 items (Table 1)
│   ├── selected_as_snowball_seed // true if in top-12
│   └── kappa_basis             // for inclusion (0.634) and clustering (0.651)
│
├── [B-RQ1] Modelling assistance strategy (RQ1)
│   ├── strategy_cluster        // ENUM = {Tools, Guidelines, Techniques, Methods, Frameworks, Languages}  (single-label, §4.2)
│   ├── strategy_subtype        // free-text but author-keyword grounded
│   │   ├── Tools.subtype       // recommender_system | AI_software_assistant | bot | plugin | view_manager | modelling_env | VR_env | reactive_system | testing_tool | transformation_tool | collab_tool
│   │   ├── Guidelines.subtype  // ISO_standardisation | flexible_workflow | refactoring_process | multi_modelling_arch
│   │   ├── Techniques.subtype  // model_development | model_validation | model_repair
│   │   ├── Methods.subtype     // consistency_validation | model_repair | task_driven_reuse | MDE_alignment
│   │   ├── Frameworks.subtype  // change_propagation | testing | collaborative_modelling | co_evolution | formal | modelling_framework
│   │   └── Languages.subtype   // mega_modelling | UML_extension | modelling_template
│   ├── software_based_ratio    // {totally, partially, no}  (§4.2 末 93.1 % vs 6.9 %)
│   └── author_keyword_evidence // raw text fragment (per §3.5)
│
├── [B-RQ2-G] Goals (RQ2-G)
│   ├── goal_cluster            // ENUM = {G1 change propagation, G2 consistency checking, G3 model compatibility, G4 model quality, G5 user interaction, G6 model evolution, G7 vulnerability detection}
│   ├── create_refine_role      // ENUM = {create_only(G6), refine_only(G1/G2/G3/G4/G7), both(G5)}   (§4.3 三分)
│   └── goal_evidence_quote     // raw fragment
│
├── [B-RQ2-L] Limitations (RQ2-L)
│   ├── limitation_reporting_status // {specified, not_specified=L-NS}  (§4.3：50.0 % 报告)
│   ├── limitation_cluster      // ENUM = {L1 accuracy, L2 effort, L3 generality, L4 learnability, L5 scope, L6 usability}  ← **Table 3 列 6 类，§4.3 prose 写 “five clusters”，待复核**
│   └── limitation_evidence_quote
│
├── [B-RQ3-M] Evaluation metrics (RQ3-M)
│   ├── evaluation_status       // {empirically_evaluated, not_evaluated=NE}
│   ├── metric_cluster          // ENUM = {M1 effectiveness, M2 efficiency, M3 user perception}  (TAM-based, §4.4)
│   ├── metric_subtype          // M1: faults | F-measure | accuracy | recall | precision | success_score | accepted_suggestions | compression_factor | feasibility | stakeholder_participation | trace_collection | inconsistency_coverage | effectiveness
│   │                           // M2: modelling_time | completion_time | testing_gen_time | repair_gen_time | performance | computational_effort | recommendation_time | preprocessing_time | resource_import | execution_count_reduction | execution_time
│   │                           // M3: industrial_adoption_perception | perceived_usefulness
│   └── metric_evidence_quote
│
├── [B-RQ3-U] Target users (RQ3-U)
│   ├── user_reporting_status   // {specified, generic_user_hidden=U-NS}  (§4.4 explicit)
│   ├── user_cluster            // ENUM = {U1 designers/modellers, U2 domain experts, U3 software developers}
│   ├── user_subtype            // U1: software_designer | model_developer | engineer_with_design_exp | UML_developer | MDE_developer | student/novice_modeller
│   │                           // U2: business_analyst | end_user | domain_user | domain_expert | domain_engineer | business_user
│   │                           // U3: developer | software_developer | SE_student | software_maintainer
│   └── user_evidence_quote
│
├── [B-RQ4-practice] Practice-side projection (RQ4)
│   ├── tool_id                 // 17 GMQ tools
│   ├── gmq_class               // ENUM = {LE Leaders, C Challengers, V Visionaries, NP Niche Players}
│   ├── documentation_status    // ENUM = {D documented, NF not_found}   (10 NF / 7 D)
│   ├── practice_proposal_id    // 15 sub-proposals inside 7 D tools
│   ├── practice_strategy       // projected to RQ1 schema (predominantly Tools)
│   ├── practice_goal           // projected to RQ2-G (G6 most common)
│   ├── practice_limitation     // projected to RQ2-L (mostly NF, only L1/L3/L5 surfaced)
│   ├── practice_metric         // projected to RQ3-M (mostly NF, M3 absent)
│   ├── practice_user           // projected to RQ3-U (mostly U3, U1/U2 absent)
│   ├── second_person_hidden    // boolean: doc uses “you” to hide target user
│   └── doc_quote_anchor        // URL / user-guide section / whitepaper id (Table 5)
│
├── [B-cross] Cross-axis derivations (§6, Fig. 5/6/11/12/13)
│   ├── strategy × goal × limitation   // Fig. 11
│   ├── goal × metric × user           // Fig. 6 / Fig. 12
│   └── literature × practice          // Fig. 13
│
└── [B-validity] Validity threats (§7)
    ├── internal: selection_bias | extraction_bias | subjective_clustering | inter_rater (K=0.634/0.651) | reviewer_fatigue
    ├── construct: grey_literature_bias | search_bias
    └── external: language_bias (English only)
```

**取值空间类型速查：**

| 主干 | 树结构 | 取值空间类型 |
|---|---|---|
| B-meta | 每 proposal 一行 | 标识符 / 数值 / 布尔 |
| B-RQ1 strategy_cluster | 单标签 ENUM | 完整封闭枚举（6 类） |
| B-RQ1 strategy_subtype | 层级子枚举 | 层级枚举 + 自由文本 anchor |
| B-RQ2-G goal_cluster | 单标签 ENUM | 完整封闭枚举（7 类） |
| B-RQ2-G create_refine_role | 派生 ENUM | 3 类 |
| B-RQ2-L limitation_cluster | 单/多标签 ENUM | 封闭枚举（6 类，**与 prose 中“five”冲突，待核**）+ NS |
| B-RQ3-M metric_cluster | 单/多标签 ENUM | 封闭枚举（3 类） + NE |
| B-RQ3-M metric_subtype | 自由文本 grounded | 自由文本加 TAM 类型 |
| B-RQ3-U user_cluster | 单标签 ENUM | 封闭枚举（3 类）+ U-NS |
| B-RQ4 gmq_class | 单标签 ENUM | 封闭枚举（4 类） |
| B-RQ4 documentation_status | 布尔 ENUM | {D, NF} |
| B-cross | 关系值 | 二维 / 三维 bubble |
| B-validity | 自由文本加理由 | 分类 + 缓解 + 残余 |

**与 A1-DT v2 通用六叶接口的对应（仅作投影层，不是原文结构）：**

- `scope` → B-meta + §1 modelling assistance 定义；
- `corpus` → §3.2/§3.3/§3.4 + Fig. 3 + B-RQ4 GMQ 池；
- `taxonomy` → B-RQ1 / B-RQ2-G / B-RQ2-L / B-RQ3-M / B-RQ3-U（这是本文真正的 taxonomy 主体）；
- `method` → B-RQ1（strategy 是 method/tool/framework/language 的并集）；
- `evidence` → B-meta 的 QA、K-statistic、Zenodo replication、Table 5 quotes；
- `finding` → B-cross + §8 discussion 的“documentation gap” + “AI/LLM disruption” 候选。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-strategy-cluster | 建模辅助策略 cluster | B-RQ1 | §3.5 RQ1 抽取规则 + §4.2 + Table 2 + Fig. 4 | 把每个 proposal 单标签归入 6 类作者术语 cluster 之一 | {Tools, Guidelines, Techniques, Methods, Frameworks, Languages} | 完整封闭枚举 | 不允许空；overlap 强制单标签（§4.2 末） | 频次 39.7/19.0/15.5/13.8/6.9/5.2 % | software-based 93.1 % 是候选 finding；混合系统外推风险 | E3, E7 | 单标签外推到 hybrid LLM/agent 系统须降级 |
| leaf-strategy-subtype | 策略子型 | leaf-strategy-cluster | §4.2 段落子列表 + Table 2 keywords | 在 cluster 内的作者术语子型 | 层级枚举（Tools 11+ 子型；其余每 cluster 3–6 子型） | 层级枚举 + 自由文本 | 子型未明时仅留 cluster | 子型分布尚未给出数字 | recommender / AI assistant 子型可对接 LLM4STM | E7 | 子型词表非饱和，A2a 待 Zenodo 核 |
| leaf-software-based | 软件实现程度 | B-RQ1 | §4.2 末 “93.1 %…software implementations” | 该 proposal 是否使用软件实现 | {totally_software, partially_software, no_software} | 派生 ENUM | 不允许空 | 93.1 % vs 6.9 % | 提示 guideline-only 占少数 | E7 | 直接迁移 |
| leaf-goal-cluster | 目标 cluster | B-RQ2-G | §3.5 + §4.3 + Table 3 + Fig. 5 | 单标签归入 7 类目标 | {G1, G2, G3, G4, G5, G6, G7} | 完整封闭枚举 | 不允许空 | G6=31.0 %、G1+G2+G3+G4+G7=43.1 %、G5=25.9 % | G6 对接 STM generation；G2/G5 对接 verification & repair | E3, E9 | G3/G7 单 proposal，统计稀疏 |
| leaf-create-refine-role | 创建/精化角色 | leaf-goal-cluster | §4.3 三分 | 派生：G6=create / G1-G4-G7=refine / G5=both | {create, refine, both} | 派生 ENUM（3 类） | 不允许空 | 31.0 / 43.1 / 25.9 % | 显示 refinement 主导，gap=纯创建少 | E9 | 直接迁移 |
| leaf-limitation-reporting | 限制是否报告 | B-RQ2-L | §3.5 “leave blank” + §4.3 L-NS | 50.0 % 明确报告 limitations | {specified, L-NS} | 布尔 | L-NS 即 not-reported（不是 not_applicable） | 50.0 % vs 50.0 % | missingness 本身=候选 finding | E9 | 直接迁移 |
| leaf-limitation-cluster | 限制 cluster | B-RQ2-L | Table 3 + §4.3 L1–L6 | 6 类限制（**§4.3 prose 写 “five”，待核**） | {L1 accuracy, L2 effort, L3 generality, L4 learnability, L5 scope, L6 usability} ∪ {L-NS} | 封闭枚举（带口径冲突待核） | L-NS=作者未声明 | 仅给出 L 子集的列表；具体每类频次未在 §4.3 完整给出 | L1/L3/L5 是 LLM4STM 主风险 | **E8 待复核** | 不允许把 “five” 直接当作权威；A2a 须复核 |
| leaf-evaluation-status | 是否经验评价 | B-RQ3-M | §4.4 NE 定义 | proposal 是否被经验评价 | {empirically_evaluated, NE} | 布尔 | NE=未评价 | NE=48.6 % | 评价缺口本身=候选 finding | E10 | 直接迁移 |
| leaf-metric-cluster | 指标 cluster | B-RQ3-M | Table 4 + §4.4 + TAM | 把指标按 TAM 分类 | {M1 effectiveness, M2 efficiency, M3 user perception} ∪ {NE} | 封闭枚举 | NE=未评价 | M1=23.6 %、M2=23.6 %、M3=4.2 %、NE=48.6 % | M3=4.2 % 是强 gap | E10 | 一 proposal 可有多 metric，注意多标签 |
| leaf-metric-subtype | 指标子型 | leaf-metric-cluster | Table 4 keywords | 在 cluster 内的具体指标项 | M1/M2/M3 子型枚举（见 §3） | 层级枚举 + 自由文本 | 缺则填 NE | 子型分布未数字化 | 直接对接 STM generation 评价 | E10 | 子型词表非饱和 |
| leaf-user-cluster | 目标用户 cluster | B-RQ3-U | §4.4 + Table 4 | 3 类 + 隐藏未报告 | {U1 designers/modellers, U2 domain experts, U3 software developers} ∪ {U-NS} | 封闭枚举 | U-NS=作者用 “user” / “he/she” 泛化或 second-person 隐藏 | U1=27.6 %、U2=13.8 %、U3=29.3 %、U-NS=29.3 % | U2 占比低是 LLM4STM domain expert 命题的起点 | E10, E11 | 直接迁移；practice 侧 U-NS 高度由 “you” 触发 |
| leaf-doc-status | 实践文档状态 | B-RQ4 | §5.2 + Fig. 9 | GMQ tool 是否有可访问的 modelling assistance documentation | {D documented, NF not_found} | 布尔 | NF≠工具缺失能力 | 10 NF / 7 D（58.8 % NF） | not-documented ≠ not-exists 是关键边界 | E11 | 直接迁移 |
| leaf-gmq-class | GMQ 分类 | B-RQ4 | §5.1 + Fig. 8 | Gartner Magic Quadrant 2023 分类 | {LE, C, V, NP} | 完整封闭枚举（4 类） | 不允许空 | LE=5, C=1, V=3, NP=8 | LE 更常公开 assistant 文档 | E11 | 仅代表 enterprise low-code 视角 |
| leaf-second-person-hidden | 第二人称隐藏用户 | leaf-doc-status | §5.2 末 “write using ‘you’… hides the actor” | 文档是否用 you 掩盖 target user | {true, false} | 布尔 | 不允许空 | 未数字化但 §5.2 显式声明常见 | LLM4STM 文档警示 | E11 | 直接迁移 |
| leaf-replication-link | 复现资料链接 | B-meta | §3.5 脚注 4 + §4.1 脚注 + §8 | Zenodo 10262145 | URL + 内容描述 | 链接 + 自由文本 | 不允许空 | n/a | 提升透明度证据 | E6 | 本审计未实际核验 |
| leaf-kappa-inclusion | 纳入 K-statistic | B-meta | §4.1 | 三 reviewer inter-rater | 数值 0–1 | 数值 | 不允许空 | K=0.634 | 处于 Landis-Koch substantial | E6 | 直接迁移 |
| leaf-kappa-clustering | 聚类 K-statistic | B-meta | §4.1 + §7.1 | 聚类 inter-rater | 数值 0–1 | 数值 | 不允许空 | K=0.651 | 同上 | E6 | 数据抽取阶段未算 K（§7.1） |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-strategy-goal | leaf-strategy-cluster | 编码关联（per-proposal）| leaf-goal-cluster | 单标签 × 单标签 | 不允许空 | Fig. 5 + Fig. 11 + §6 | Tools↔G5/G6；Methods↔G2；Frameworks↔G1；用于 cross-axis 统计 |
| edge-strategy-limitation | leaf-strategy-cluster | 编码关联 | leaf-limitation-cluster | 单 × 单/多 + L-NS | L-NS 显式 | Fig. 5 + Fig. 11 | Tools↔L1/L5/L3；Frameworks↔L5；候选 finding 来源 |
| edge-goal-metric | leaf-goal-cluster | 编码关联 | leaf-metric-cluster | 单 × 单/多 + NE | NE 显式 | Fig. 6 + Fig. 12 | G6↔M1+M2；G5↔M2；G2↔M1 |
| edge-goal-user | leaf-goal-cluster | 编码关联 | leaf-user-cluster | 单 × 单 + U-NS | U-NS 显式 | Fig. 6 + Fig. 12 | G6↔U1+U3；G5↔U1；G1↔U3+U2；显示 domain expert 命题缺口 |
| edge-literature-practice | B-RQ1/2/3 (lit-side) | 投影关系（同 schema） | B-RQ4 (practice-side) | 同左 cluster × 同左 cluster | NF（practice 一侧专属） | Fig. 13 + §6 | 显示 practice 中 L2/L4/L5 缺失、U1/U2 缺失、M3 缺失 |
| edge-tool-proposal | leaf-gmq-class + tool_id | 包含 | practice_proposal_id | 1 tool → 0..n proposals | NF=0 | §5.2 + Table 5 | 7 tools 包含 15 proposals |
| edge-doc-strategy | leaf-doc-status | 仅在 D 下展开 | leaf-strategy-cluster (practice 投影) | 同 RQ1 ENUM | NF 直接终止链 | §5.2 “80 % strategies are tools” | not-documented 阻断后续编码 |
| edge-quality-snowball | leaf-quality-score | 选种关系 | leaf-replication-link / snowball seeds | top-12 阈值 | n/a | §3.4 + §4.1 | 显示 corpus 入口偏置 |

### 6. 统计观察、候选 finding 与 final finding 边界

**A. 由字段 / 表支持的统计观察（可统计、可作 schema-seed 主统计池候选）：**

1. 纳入分母：3,176 screened → 77 possible → 58 included；K(inclusion)=0.634；K(clustering)=0.651。（E6）
2. RQ1 strategy 分布：Tools 39.7 %、Frameworks 19.0 %、Techniques 15.5 %、Methods 13.8 %、Guidelines 6.9 %、Languages 5.2 %；software-based 93.1 %。（E7）
3. RQ2-G create/refine 三分：G6 create=31.0 %（18）、refine(G1+G2+G3+G4+G7)=43.1 %（25）、G5 both=25.9 %（15）。（E9）
4. RQ2-L reporting rate：50.0 % proposals 明确报告 limitations；L-NS=50.0 %。（E9）
5. RQ3-M：M1=23.6 %、M2=23.6 %、M3=4.2 %、NE=48.6 %。（E10）
6. RQ3-U：U1=27.6 %、U2=13.8 %、U3=29.3 %、U-NS=29.3 %。（E10）
7. RQ4 documentation status：NF=10/17=58.8 %、D=7/17=41.2 %；7 D 包含 15 practice proposals；practice strategy 80 % tool、goal 100 % 报告、limitation 报告 20 %、metric NF 73.3 %、user NF 73.3 %。（E11）
8. Cross-axis（Fig. 5/6/11/12/13）支持的成对关联：Tools↔G5/G6/L1/L3/L5；Methods↔G2；Frameworks↔G1/L5；G6↔U1+U3；G5↔U1；practice 中 L2/L4/L5、M3、U1/U2 缺失。（E7, E9, E10, E11, E12）

**B. 原文 discussion / conclusion / future work 中的候选 finding（不是字段统计的直接结论，必须作 candidate 处理）：**

1. “documentation about MDSE assistants’ limitations, evaluation metrics, and target users is scarce or non-existent”（abstract & §8）—— 由 #4–#7 支撑但仍是 author claim，迁移时需保留分母。
2. “software-based strategies dominate”（§4.2）—— 93.1 % 数值支撑，相对稳健。
3. “practice tools 中 not-documented ≠ not-exists”（§5.2 + §7.1）—— 是方法论级别 caveat，不是领域 finding。
4. “AI/LLM/GPT 将带来 disruptive 变化，需要 unified framework”（§8）—— **不是字段统计结论**，是 future expectation；在 review.md 与 SUMMARY 中只能写成 candidate，不能写成已验证。
5. “designers/modellers (U1) 与 domain experts (U2) 在 practice 中几乎缺席”（§6 / Fig. 13）—— 由 practice 73.3 % U-NS + “you” 隐藏支撑。
6. “user-perception metrics (M3) 4.2 %”是 evaluation 维度的强 gap（§4.4 + Fig. 13）。
7. proposed unified framework 应连接 IMA [103] 与 elicitation framework [81]（§8 future work）—— 仅 design implication，不进入领域 final finding。

**C. 对 Paper2 可迁移的方法学启发（不依赖 MDSE 领域真值）：**

1. 字段树 = RQ-extraction-schema-as-tree：把 RQ 直接当作主干、把抽取规则当作叶子；
2. 显式缺失语义（L-NS / NE / U-NS / NF）是一等字段，不是空值；
3. 单标签 cluster 风险 + 作者术语依赖（terminology bias）必须随 schema 一起迁移；
4. literature × practice 同一 schema 双投影 + “not-documented ≠ not-exists”；
5. inter-rater 在 inclusion + clustering 两个环节分别报告 K（数据抽取阶段未算 K，是已声明限制）；
6. cross-axis bubble chart 是“多字段联合”候选 finding 的图形化载体；
7. replication package（Zenodo）作为字段证据的最终源。

**D. 绝不能迁移的领域结论：**

1. 任何 RQ1–RQ4 中 MDSE 领域具体百分比、cluster 名、proposal id 不能直接外推到 LLM4STM / 控制系统状态机领域；
2. “Tools 39.7 %”等比例只在 MDSE-assistant 普通研究池成立；
3. “M3 4.2 %”不能直接用作 LLM4STM 的 evaluation gap 论据，只能作为方法学警示；
4. AI/LLM disruption 论述是 future work，不是已验证结果。

### 7. 对旧版 `review.md` 的返修来源（C/I/M）

**C（critical，影响 A1-DT v2 事实源与统计池可信度）：**

- **C1**：当前 `review.md` 主结构（第 4 节“维度树复原 → 叶子维度表”那 6 行 `leaf-*-scope/corpus/taxonomy/method/evidence/finding`）把跨论文通用接口当成原文叶子全集，与本文真实 schema（strategy/goal/limitation/metric/user × 5 字段 × 6+7+6+3+3+NS/NE/NF cluster）严重不符。**返修**：把 §3 给出的 [B-RQ1] / [B-RQ2-G] / [B-RQ2-L] / [B-RQ3-M] / [B-RQ3-U] / [B-RQ4-practice] / [B-cross] / [B-validity] 抬升为正式主干叶子，把现有六叶降级为 §维度树复原 末尾的 “通用接口投影”小节（这部分目前虽然存在，但被压在 19×3 v1 旧框下，不是 v2 主结构）。
- **C2**：当前“原文模式候选叶子映射（A1 种子）”表只列了 5 个高粒度种子（strategy / goal / artifact / metric-user / limitation），且全部 `not_verified`；但原文 Table 2/3/4 已经显式给出**完整封闭枚举 + 频次**，应直接升级为已核验枚举（仅 `leaf-limitation-cluster` 因 §4.3 prose “five” vs Table 3 “L1–L6” 冲突保留 `not_verified`），不能继续整体停留在 `schema_seed`。
- **C3**：当前 SUMMARY 或 A.3 中“样本单位 / 样本数量 / 原生树类型 / 统计池资格”应改为：原生树类型=**维度森林**、样本单位=**proposal + tool**（双层）、样本数=58 + 17/15、主统计池资格=**局部可统计 schema-seed**（不是当前的 `否（A1-DT 阶段仅作 schema seed）`，因为 Table 2–4 已给出原文 closed-enum + 比例 + K）。

**I（important，影响证据链可读性与下游 schema 迁移）：**

- **I1**：§4.3 文中 “five limitation clusters” 与 Table 3 “L1–L6” 的口径冲突应在 A.2 中作为单独 evidence 行登记（建议 `EV-mdse-modelling-assistants-mapping-006`），强度=`not_verified`，并列入 A2a 必须 PDF + Zenodo 复核任务。
- **I2**：当前 A.2 把 5 条 evidence 全部标 `not_verified`，但 §3.5 / §4.1 / §4.2 / §4.4 / §5.2 文本级证据强度应至少升级为 `text_verified`（仅图表数字、bubble 半径与 §4.3 limitation count 保持 `not_verified`）。否则 A.3 推不出任何 `schema_seed` 以上的结论。
- **I3**：缺失语义编码 `L-NS / NE / U-NS / NF` 是本文一等字段，应在叶子维度表中单独列出，而非合并在叶子定义里；当前 review.md 把它们隐入 `not_specified` 自由文本，下游 schema 迁移容易丢。
- **I4**：当前 A.2 / A.3 没有为 [B-cross]（Fig. 5/6/11/12/13）建独立证据行；§6 cross-axis 是本文 finding 的主要来源，必须有专属 evidence + 关系边 claim。
- **I5**：当前 SUMMARY 表“样本数量 / 分母 = 58 proposals / 3,176 records / 17 tools”应改为“proposals=58 / practice_tools=17（D=7 / NF=10）/ practice_proposals=15 / records_screened=3,176 / K_inclusion=0.634 / K_clustering=0.651”，把 K 一并显化。
- **I6**：当前“可迁移与不可迁移边界”表把“具体领域结论”整体禁止迁移是对的，但应额外明确禁止把 `M3=4.2 %` 类指标直接当 LLM4STM gap 论据，只允许作方法学警示。

**M（minor，可后续顺手清理）：**

- **M1**：当前“历史草稿（已迁移，不作事实真源）”两节占 80+ 行，建议折叠到附录或文末 history 区，避免新 reviewer 误读为当前事实。
- **M2**：emoji 列（如 `🟢` 等口径）不出现在本 review.md，但 `[clm-*]` 引用键格式偶有空格不一致，建议统一。
- **M3**：将 Zenodo `10262145` 与 GMQ 2023 URL 在 A.1 中作为独立 src 行登记，便于 A2a 自动化抓取。
- **M4**：CCF 等级、IST OA 状态、`paper.pdf` 视觉核验是否完成，建议在 0 卡片末单独列“尚未做的最小动作清单”，避免 reviewer 误以为已完成。

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案（中文表头）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-mma-001 | paper_content.txt, bibtex.bib | §1 Introduction（Page 1）+ Abstract | abstract; “Modelling assistance is the strategy…that aims to assist humans during software modelling tasks in MDSE tools.” | 给出 modelling assistance 定义和 MDSE/低代码边界 | scope_definition | text_verified | B-meta, ROOT, leaf-strategy-cluster | 否 | 仅本文 scope；不外推 LLM4STM 领域 |
| EV-mma-002 | paper_content.txt | §3.1 RQ1/RQ2/RQ3（Page 3–4） + §3.5 extraction rules（Page 4–5） | RQ 表述与“Extract the keywords…leave the field blank…” | RQ 即字段树主干；缺失语义=显式留空 | rq_and_extraction_schema | text_verified | B-RQ1, B-RQ2-G, B-RQ2-L, B-RQ3-M, B-RQ3-U, leaf-limitation-reporting, leaf-evaluation-status, leaf-user-reporting | 否（仅 Zenodo raw form 待核） | 直接迁移结构，不迁移领域结论 |
| EV-mma-003 | paper_content.txt | §3.2/§3.3/§3.4/§4.1 + Fig. 3 PRISMA（Page 3–6） | 1,996+5 → 51 → top12 seeds → 1,175 snowball → 3,176 → 77 → 58；K=0.634/0.651 | corpus pipeline + inter-rater | corpus_pipeline | text_verified（图 3 视觉待核） | leaf-quality-score, leaf-kappa-inclusion, leaf-kappa-clustering, leaf-replication-link, B-meta | true（Fig. 3 视觉） | 仅本文样本池 |
| EV-mma-004 | paper_content.txt | §4.2 + Table 2 + Fig. 4（Page 6–7） | 6 cluster + 比例 + 93.1 % software-based | taxonomy_with_distribution | text_verified（图 4 数字待核） | leaf-strategy-cluster, leaf-strategy-subtype, leaf-software-based | true（Fig. 4 视觉） | 单标签 cluster 风险 |
| EV-mma-005 | paper_content.txt | §4.3 + Table 3 + Fig. 5（Page 7–9） | 7 G clusters + “five limitation clusters”（prose）/ Table 3 列 L1–L6 + L-NS | taxonomy + 口径冲突 | text_verified_with_internal_conflict | leaf-goal-cluster, leaf-create-refine-role, leaf-limitation-reporting, leaf-limitation-cluster | true（§4.3 prose vs Table 3） | **A2a 必须复核 PDF / Zenodo**，否则 L 总数不可信 |
| EV-mma-006 | paper_content.txt | §4.4 + Table 4 + Fig. 6（Page 9–10） | 3 M + 3 U + NE/U-NS + 频次 | taxonomy + missingness | text_verified（图 6 数字待核） | leaf-evaluation-status, leaf-metric-cluster, leaf-metric-subtype, leaf-user-cluster | true（Fig. 6 视觉） | 一 proposal 可多 metric，注意多标签 |
| EV-mma-007 | paper_content.txt | §5.1/§5.2 + Table 5 + Fig. 8/9/10（Page 10–13） | 17 GMQ tools → 10 NF + 7 D → 15 proposals；“you” 隐藏 user | practice_projection + missingness | text_verified（Fig. 9/10 视觉与 vendor URL 待核） | B-RQ4-practice, leaf-doc-status, leaf-gmq-class, leaf-second-person-hidden | true | grey-literature 局限于 GMQ；vendor URL 当前状态未复核 |
| EV-mma-008 | paper_content.txt | §6 + Fig. 11/12/13（Page 13–14） | strategy×goal×limitation；goal×metric×user；lit vs practice | cross_axis_relations | text_verified（bubble 视觉待核） | edge-strategy-goal, edge-strategy-limitation, edge-goal-metric, edge-goal-user, edge-literature-practice | true | bubble 半径 = 计数，单 proposal 单 cluster |
| EV-mma-009 | paper_content.txt | §7.1–§7.3（Page 15） | selection / extraction / subjective interpretation / inter-rater / grey literature / search / language bias | validity_threats | text_verified | B-validity, terminology_basis | 否 | 缓解 ≠ 消除；data extraction K 未算 |
| EV-mma-010 | paper_content.txt | §8（Page 15–17） + Fig. 14/15 | future framework + AI/LLM disruption + Zenodo 10262145 | future_work_candidate_finding | text_verified（视觉待核） | candidate findings (B/C/D) | true | AI/LLM disruption=expectation，不是结果 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-mma-01 | 本文真正的 A1-DT 维度森林由 5 字段树（strategy / goal / limitation / metric / user）+ practice 投影 + cross-axis 关系 + validity 组成；不是六叶通用接口。 | tree_type | ROOT, B-RQ1..4, B-cross, B-validity | EV-mma-002, 004, 005, 006, 007, 008 | strong（schema 级） | review.md 主结构、SUMMARY 行 | 单标签 cluster + 作者术语 cluster 必须随用 |
| C-mma-02 | 样本单位是 proposal（n=58）+ tool（n=17，含 15 practice proposals）的双层 schema；分母与 K 都已显化。 | sampling_unit | B-meta, B-RQ4 | EV-mma-003, 007 | strong | SUMMARY、统计池资格 | grey-literature 仅限 GMQ |
| C-mma-03 | RQ1 strategy 是完整封闭 6-cluster 单标签编码；93.1 % software-based。 | closed_enum + distribution | leaf-strategy-cluster, leaf-software-based | EV-mma-004 | strong | 可作 schema-seed 统计 | 单标签压扁混合系统 |
| C-mma-04 | RQ2-G 是完整封闭 7-cluster 单标签编码；可派生 create/refine 三分（31.0/43.1/25.9 %）。 | closed_enum + derived | leaf-goal-cluster, leaf-create-refine-role | EV-mma-005 | strong | 可作 schema-seed 统计 | G3/G7 单 proposal 稀疏 |
| C-mma-05 | RQ2-L cluster 总数在原文内部存在 “five (§4.3 prose)” vs “L1–L6 (Table 3)” 冲突，必须保留 `not_verified` 直到 A2a 复核。 | internal_inconsistency | leaf-limitation-cluster | EV-mma-005 | weak | 候选 finding 不可作 final | 必须 A2a PDF + Zenodo 复核 |
| C-mma-06 | RQ3-M cluster 是 3-cluster TAM-based 单/多标签；M3=4.2 %、NE=48.6 % 是显式 evaluation gap。 | closed_enum + missingness | leaf-evaluation-status, leaf-metric-cluster | EV-mma-006 | strong | 可作 schema-seed 统计；可作方法学警示 | 不可直接外推 LLM4STM gap 数字 |
| C-mma-07 | RQ3-U cluster 是 3-cluster 单标签 + U-NS；U-NS=29.3 %、practice 73.3 %；practice U-NS 由 “you” 触发是 §5.2 显式机制。 | closed_enum + missingness + mechanism | leaf-user-cluster, leaf-user-reporting, leaf-second-person-hidden | EV-mma-006, 007 | strong | 可作 schema-seed 统计 | 不外推领域比例 |
| C-mma-08 | not-documented ≠ not-exists（GMQ 中 10/17 NF 不能等同“工具没有 assistant”）。 | methodological_caveat | leaf-doc-status, B-validity | EV-mma-007, 009 | strong | 直接迁移到 Paper2 / Project1 | grey-literature 局限 |
| C-mma-09 | AI/LLM disruption 与 unified framework 论述是 future expectation，不是字段统计的 final finding。 | candidate_finding | §8 论述 | EV-mma-010 | weak | review.md / SUMMARY 只能写 candidate | 与原文 RQ 抽取数据不直接挂钩 |
| C-mma-10 | cross-axis（strategy×goal×limitation；goal×metric×user；lit vs practice）是本文 finding 的主要候选来源，但需 PDF 复核 bubble 半径数字。 | relation_finding | edge-* | EV-mma-008 | medium | 可作 candidate finding | bubble 数字 PDF 待核 |
| C-mma-11 | terminology bias + subjective clustering + data extraction K 未算 + grey literature limited to GMQ + English-only：5 条 validity 边界必须随 schema 一起迁移。 | migration_boundary | B-validity | EV-mma-009 | strong | review.md 迁移边界 + Paper2 启发 | 缓解不等于消除 |

### 9. 技能使用与自我审查记录

**已读技能 / 指南文件与采纳原则：**

1. `ai-research-writing-skill/SKILL.md` —— 采纳 “claim-evidence-engineering” + “evidence gate / story gate / citation gate”：每个 leaf / claim 必须挂证据锚点（EV-mma-001..010），不写无证据的强 finding；§4.3 内部冲突 → 显式标 `not_verified`，不脑补。
2. `ai-research-writing-skill/references/reviewer-guidelines.md` —— 采纳“constructive specificity”：返修建议 C/I/M 每条指定文件位置（review.md 哪一节、哪一表）+ 期望行为 + 实际行为差异。
3. `ai-research-writing-skill/references/reviewer-self-review.md` —— 采纳“Five-Dimension Review + Reviewer-Review Simulation”，并把它转成本审计末尾的“最高风险 3 点”。
4. `research-planning/SKILL.md` —— 采纳“先理解上下文 → 再生成 plan”的步骤约束，先读 schema 三件套再读论文。
5. `research-planning/references/planning-prompts.md` —— Paper2Code 4-turn 模板让我先做“overall scope 判定 → architecture（维度树） → logic（叶子+关系边） → configuration（取值空间/缺失/统计）”而不是一次性堆。
6. `research-planning/references/output-schemas.md` —— JSON schema 提示我把维度树以可序列化方式列出（叶子表 + 关系边表）。
7. `autoresearch/SKILL.md` —— 提醒本任务是 artifact-gated 单步审计，不进入 stateful loop；本输出本身即为完成 artifact，无需 nudge。

**Reviewer 自审：本输出最高风险的 3 点 + 主线程合并复核办法：**

1. **§4.3 limitation 口径冲突可能让下游错把 6 当作权威**。主线程合并 review.md 时，必须把 `leaf-limitation-cluster` 与 EV-mma-005 同时标 `not_verified`，并在 SUMMARY 中给 “limitations cluster 数 5 或 6 待核” 留显式 risk 条目；A2a 必须打开 PDF Table 3 + Zenodo raw CSV 双源核对。
2. **图表数字（Fig. 4/5/6/11/12/13）未做 PDF 视觉核验**。所有 cross-axis edge claim（C-mma-10）目前都基于 §6 文本叙述，bubble 半径未复核；合并时应保留 `needs_visual_check`，不要把 §6 中 “Tools↔G5/G6”、“Frameworks↔L5”、“G6↔U1+U3” 等关系直接升级为 strong。
3. **旧版 review.md 历史草稿与 19×3 旧表与本 v2 审计存在叙事冲突**。合并时必须显式把旧 v1 主树 + 旧 19×3 主树降级为“历史草稿（已迁移）”小节，把本审计 §3 的维度森林作为唯一事实源；否则下游 paper2 reviewer 会同时看到三套相互矛盾的“原文 schema”。

**blocked / timeout / 文件缺失：**

- 无 `blocked`：所有要求阅读的技能文件、bibtex.bib、metadata.json、paper_content.txt、review.md 均成功本地读取。
- 未访问：`paper.pdf` 未在本审计中打开（按硬约束 5 仅“必要时”才核对，且不允许 subagent；图表视觉核验留 A2a）；Zenodo `10262145` replication package 未访问（不在硬约束允许的本地材料范围内）。
- 无 timeout。

---

报告结束。本审计为自包含完整报告；A1-DT v2 维度森林、叶子表、关系边表、证据账本草案与结论映射草案均已落到本回答正文，主线程可直接据此重写 `review.md` 的“维度树复原 / 叶子维度表 / 关系边表 / A.1–A.4 审计附录”节，无需再回到上一条消息或工具调用结果。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md](../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-mdse-modelling-assistants-mapping-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-mdse-modelling-assistants-mapping-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-mdse-modelling-assistants-mapping-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-mdse-modelling-assistants-mapping-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/mdse-modelling-assistants-mapping__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-mdse-modelling-assistants-mapping-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/mdse-modelling-assistants-mapping.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-mdse-modelling-assistants-mapping-type | clm-mdse-modelling-assistants-mapping-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） | paper_type | text_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-mdse-modelling-assistants-mapping-unit | clm-mdse-modelling-assistants-mapping-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：(a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） | sample_unit | text_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-mdse-modelling-assistants-mapping-denom | clm-mdse-modelling-assistants-mapping-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals | denominator | text_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-mdse-modelling-assistants-mapping-tree | clm-mdse-modelling-assistants-mapping-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） | schema | text_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-mdse-modelling-assistants-mapping-pool | clm-mdse-modelling-assistants-mapping-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 final finding |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-mdse-modelling-assistants-mapping-type | A1DT-mdse-modelling-assistants-mapping-C01 | 本文原文类型为：SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） | paper_type | type | ev-mdse-modelling-assistants-mapping-type | 正式写作前需核对出版页和 PDF 版式 | text_verified | schema_seed / 背景方法样本描述 | 否 | -- |
| clm-mdse-modelling-assistants-mapping-unit | A1DT-mdse-modelling-assistants-mapping-C02 | 本文被编码样本单位为：(a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） | sample_unit | sample_unit | ev-mdse-modelling-assistants-mapping-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | text_verified | schema_seed / A2a 抽取表设计 | 否 | -- |
| clm-mdse-modelling-assistants-mapping-tree | A1DT-mdse-modelling-assistants-mapping-C03 | 本文原生维度树 / 维度森林为：**维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） | tree_type | native_tree | ev-mdse-modelling-assistants-mapping-tree | 不代表跨论文通用模板 | text_verified | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-mdse-modelling-assistants-mapping-pool | A1DT-mdse-modelling-assistants-mapping-C04 | 本文统计池资格为：局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 | eligibility | statistical_pool | ev-mdse-modelling-assistants-mapping-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-mdse-modelling-assistants-mapping-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-mdse-modelling-assistants-mapping-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-mdse-modelling-assistants-mapping-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
