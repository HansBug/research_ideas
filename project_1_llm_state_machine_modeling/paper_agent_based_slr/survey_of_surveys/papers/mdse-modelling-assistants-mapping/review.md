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

### 一句话结论

本文的维度树主类型为“systematic mapping 分类树”，辅助类型为“assistant strategy-goal-metric-user 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-mdse-modelling-assistants-mapping-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-mdse-modelling-assistants-mapping-root] | Understanding the landscape of software modelling assistants for MDSE tools 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-mdse-modelling-assistants-mapping-b1] 综述范围与研究问题；[dim-mdse-modelling-assistants-mapping-b2] 语料收集与纳排；[dim-mdse-modelling-assistants-mapping-b3] 主题 / 对象分类；[dim-mdse-modelling-assistants-mapping-b4] 方法 / 技术 / 干预；[dim-mdse-modelling-assistants-mapping-b5] 评价、统计与候选发现 | [ev-mdse-modelling-assistants-mapping-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-mdse-modelling-assistants-mapping-root] Understanding the landscape of software modelling assistants for MDSE tools
├── [dim-mdse-modelling-assistants-mapping-b1] 综述范围与研究问题
│   └── [leaf-mdse-modelling-assistants-mapping-scope] 研究范围与单位对象
├── [dim-mdse-modelling-assistants-mapping-b2] 语料收集与纳排
│   └── [leaf-mdse-modelling-assistants-mapping-corpus] 语料与纳排链条
├── [dim-mdse-modelling-assistants-mapping-b3] 主题 / 对象分类
│   └── [leaf-mdse-modelling-assistants-mapping-taxonomy] 主题与维度分类
├── [dim-mdse-modelling-assistants-mapping-b4] 方法 / 技术 / 干预
│   └── [leaf-mdse-modelling-assistants-mapping-method] 方法 / 技术 / 干预分类
└── [dim-mdse-modelling-assistants-mapping-b5] 评价、统计与候选发现
    └── [leaf-mdse-modelling-assistants-mapping-evidence] 评价、证据与复现资产
    └── [leaf-mdse-modelling-assistants-mapping-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-mdse-modelling-assistants-mapping-scope] | 研究范围与单位对象 | [dim-mdse-modelling-assistants-mapping-b1] | 定义 MDSE modelling assistants 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-scope] |
| [leaf-mdse-modelling-assistants-mapping-corpus] | 语料与纳排链条 | [dim-mdse-modelling-assistants-mapping-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-corpus] |
| [leaf-mdse-modelling-assistants-mapping-taxonomy] | 主题与维度分类 | [dim-mdse-modelling-assistants-mapping-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-taxonomy] |
| [leaf-mdse-modelling-assistants-mapping-method] | 方法 / 技术 / 干预分类 | [dim-mdse-modelling-assistants-mapping-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-method] |
| [leaf-mdse-modelling-assistants-mapping-evidence] | 评价、证据与复现资产 | [dim-mdse-modelling-assistants-mapping-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-evidence] |
| [leaf-mdse-modelling-assistants-mapping-finding] | 统计观察与候选发现 | [dim-mdse-modelling-assistants-mapping-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-mdse-modelling-assistants-mapping-leaf-finding] |

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-mdse-modelling-assistants-mapping-method-evidence] | [leaf-mdse-modelling-assistants-mapping-method] | 支撑 / 度量 | [leaf-mdse-modelling-assistants-mapping-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-mdse-modelling-assistants-mapping-taxonomy] | [clm-mdse-modelling-assistants-mapping-edge-method-evidence] |
| [edge-mdse-modelling-assistants-mapping-taxonomy-finding] | [leaf-mdse-modelling-assistants-mapping-taxonomy] | 导出候选发现 | [leaf-mdse-modelling-assistants-mapping-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-mdse-modelling-assistants-mapping-stat] | [clm-mdse-modelling-assistants-mapping-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-mdse-modelling-assistants-mapping-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-mdse-modelling-assistants-mapping-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-mdse-modelling-assistants-mapping-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-mdse-modelling-assistants-mapping-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | MDSE modelling assistants 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-mdse-modelling-assistants-mapping-transfer] |
| [leaf-mdse-modelling-assistants-mapping-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-mdse-modelling-assistants-mapping-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-mdse-modelling-assistants-mapping-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-mdse-modelling-assistants-mapping-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-mdse-modelling-assistants-mapping-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-mdse-modelling-assistants-mapping-001 | [ev-mdse-modelling-assistants-mapping-root] | [src-mdse-modelling-assistants-mapping-text], [src-mdse-modelling-assistants-mapping-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-mdse-modelling-assistants-mapping-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-mdse-modelling-assistants-mapping-002 | [ev-mdse-modelling-assistants-mapping-taxonomy] | [src-mdse-modelling-assistants-mapping-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-mdse-modelling-assistants-mapping-b1], [dim-mdse-modelling-assistants-mapping-b2], [dim-mdse-modelling-assistants-mapping-b3], [dim-mdse-modelling-assistants-mapping-b4], [dim-mdse-modelling-assistants-mapping-b5], [leaf-mdse-modelling-assistants-mapping-taxonomy], [leaf-mdse-modelling-assistants-mapping-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-mdse-modelling-assistants-mapping-003 | [ev-mdse-modelling-assistants-mapping-stat] | [src-mdse-modelling-assistants-mapping-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-mdse-modelling-assistants-mapping-evidence], [leaf-mdse-modelling-assistants-mapping-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-mdse-modelling-assistants-mapping-004 | [ev-mdse-modelling-assistants-mapping-risk] | [src-mdse-modelling-assistants-mapping-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-mdse-modelling-assistants-mapping-root], [leaf-mdse-modelling-assistants-mapping-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-mdse-modelling-assistants-mapping-005 | [ev-mdse-modelling-assistants-mapping-relation] | [src-mdse-modelling-assistants-mapping-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边；本行在 A1-DT 仅作关系边 seed，待 A2a 精确页码 / 表图核验后才能升级。 | taxonomy | not_verified | [edge-mdse-modelling-assistants-mapping-method-evidence], [edge-mdse-modelling-assistants-mapping-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-mdse-modelling-assistants-mapping-tree-type] | A1DT-mdse-modelling-assistants-mapping-C01 | 本文的维度树主类型为“systematic mapping 分类树”，辅助类型为“assistant strategy-goal-metric-user 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-mdse-modelling-assistants-mapping-tree-type] | tree_type | [dim-mdse-modelling-assistants-mapping-root] | EV-mdse-modelling-assistants-mapping-001, EV-mdse-modelling-assistants-mapping-004 | 树型判断仅限本文，不代表所有 MDSE modelling assistants 综述。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-scope] | A1DT-mdse-modelling-assistants-mapping-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-scope] | EV-mdse-modelling-assistants-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-corpus] | A1DT-mdse-modelling-assistants-mapping-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-corpus] | EV-mdse-modelling-assistants-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-taxonomy] | A1DT-mdse-modelling-assistants-mapping-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-taxonomy] | EV-mdse-modelling-assistants-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-method] | A1DT-mdse-modelling-assistants-mapping-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-method] | EV-mdse-modelling-assistants-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-evidence] | A1DT-mdse-modelling-assistants-mapping-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-evidence] | EV-mdse-modelling-assistants-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-leaf-finding] | A1DT-mdse-modelling-assistants-mapping-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-mdse-modelling-assistants-mapping-finding] | EV-mdse-modelling-assistants-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-transfer] | A1DT-mdse-modelling-assistants-mapping-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-mdse-modelling-assistants-mapping-root] | EV-mdse-modelling-assistants-mapping-002, EV-mdse-modelling-assistants-mapping-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-finding-boundary] | A1DT-mdse-modelling-assistants-mapping-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-mdse-modelling-assistants-mapping-finding] | EV-mdse-modelling-assistants-mapping-003, EV-mdse-modelling-assistants-mapping-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |
| [clm-mdse-modelling-assistants-mapping-edge-method-evidence] | A1DT-mdse-modelling-assistants-mapping-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-mdse-modelling-assistants-mapping-method-evidence] | EV-mdse-modelling-assistants-mapping-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | weak | schema_seed | false | -- |
| [clm-mdse-modelling-assistants-mapping-edge-taxonomy-finding] | A1DT-mdse-modelling-assistants-mapping-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-mdse-modelling-assistants-mapping-taxonomy-finding] | EV-mdse-modelling-assistants-mapping-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | weak | candidate_finding | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-mdse-modelling-assistants-mapping-structure-check] | [dim-mdse-modelling-assistants-mapping-root], A1DT-mdse-modelling-assistants-mapping-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-mdse-modelling-assistants-mapping-visual-check] | EV-mdse-modelling-assistants-mapping-002, EV-mdse-modelling-assistants-mapping-003, EV-mdse-modelling-assistants-mapping-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
