# Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap

## 1. 快速结论卡片

| 字段 | 结论 |
|---|---|
| 标题 | Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap |
| 作者 | Ahmed E. Hassan; Gustavo A. Oliva; Dayi Lin; Boyuan Chen; Zhen Ming (Jack) Jiang |
| 年份 / 正式发表 | 2026；`metadata.json` 记录正式发布日期为 2026-04-09 |
| 出版形态 | 期刊；arXiv PDF 作为开放全文来源 |
| 期刊/会议/预印本 | [TOSEM](https://dl.acm.org/journal/tosem)；DOI: <https://doi.org/10.1145/3807901>；开放 PDF: <https://arxiv.org/pdf/2410.06107> |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | A |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 本轮阅读状态 | `已读全文文本-paper_content核验`：已读 `bibtex.bib`、`metadata.json` 与 `paper_content.txt` 全文；未人工打开 `paper.pdf` 核对图表版式 |
| 证据等级 | 全文文本级；图表待人工核对 |
| 论文类型 | vision / roadmap / taxonomy-边界锚点；不是 SLR、SMS、tertiary study 或 guideline |
| 对本库定位 | 可作为 AI-native SE / agentic SE 的“愿景—技术栈—挑战路线图”边界锚点，提供 roadmap / challenge / stack-component 字段候选；不得升级为系统综述证据或目标领域统计证据 |
| 一句话结论 | 该文通过“SE 2.0 局限 → SE 3.0 愿景 → 五层技术栈 → 开放挑战”的叙事组织 AI-native SE 路线图；价值在于结构化愿景和挑战字段树，不在于系统性证据综合。 |

## 2. 全文内容详读

### 2.1 背景 / 问题设定

论文把当前由 Foundation Models 和 AI coding assistants 支撑的软件工程称为 Software Engineering 2.0，即 AI-assisted SE。其核心判断是：AI coding assistants 已经广泛进入 IDE、终端和日常开发流程，但现有流程仍然是 task-driven、code-centric，并且人类开发者仍处于代码创建循环中心。作者由此提出需要从“AI 辅助传统 SE 活动”转向“AI-native SE”，即 Software Engineering 3.0。

证据锚点：`paper_content.txt` Page 1--2 的摘要与 Introduction；Page 2 明确说明该愿景来自学术与灰色文献 surveys、多个社区活动和 workshop、客户与内部团队讨论、作者对 FMware 与 SE 3.0 stack 的研发经验，以及 OPEA alliance 中 40+ 工业伙伴互动。

需要注意：这里的“surveys of academic and gray literature”不是系统综述协议。原文没有给出检索式、数据库、纳排流程、筛选分母、质量评价、抽取表或可复核合成协议，因此不能把它当作 SLR / SMS 证据源。

### 2.2 SE 2.0 限制

论文把 SE 2.0 的限制组织为三类主问题，并额外讨论 autonomous software engineers 的边界：

1. **人类认知过载**：在 SE 2.0 中，人类仍需拆解问题、提示 assistant、评估建议、调试失败并迭代修复。AI 补全片段代码提高局部速度，但没有改变人类驱动代码循环的本质。作者用典型编程会话说明这种局部补全—运行测试—发现遗漏—再提示—再修复的链条会让开发者陷入 debugging rabbit holes。
2. **模型训练低效且理解不足**：作者批评 frontier FMs 依赖大规模非结构化互联网数据，计算和环境成本高，训练过程处理大量噪声，难以获取深层 SE 知识和可维护的推理能力，并且需要持续重训 / 微调。
3. **代码质量与 additive bias**：AI coding assistants 倾向于添加代码而非提醒重构、抽象或删除复杂度；短期速度收益可能被长期复杂度、静态分析 warning、CI / lint 噪声和信任下降抵消。原文还指出 AI 生成代码进入未来训练数据可能造成质量反馈回路。
4. **autonomous software engineers 尚不能替代愿景**：Devin、SWE-agent、OpenHands、TRAE 等 autonomous software engineers 被视为重要趋势，但作者认为它们仍缺少 human-AI intent alignment，依赖 off-the-shelf FMs，且 SWE-Bench Verified 等 benchmark 的项目和语言覆盖有限，真实世界表现仍不明确。

证据锚点：`paper_content.txt` §2.2.1--§2.2.3，Page 3--5；§2.3，Page 5--6。

### 2.3 SE 3.0 愿景

SE 3.0 被定义为 AI-native SE：AI 不再只是传统活动的辅助工具，而是软件工程过程的内生组成部分。其核心从 code-centric 转为 intent-centric 和 conversation-oriented：人类表达目标、约束、示例、草图或数据；AI teammate 通过对话帮助澄清意图，然后驱动代码创建循环，把意图合成为可运行软件。作者把“code is just a means to an end”作为愿景底层立场。

该愿景包含三条关键原则：

1. **人机互补**：人类保留业务需求、目标反思和最终满意度判断；AI 负责高速搜索、合成、探索候选实现和处理低层实现细节。
2. **对话式意图对齐**：开发过程从写代码改为围绕意图反复澄清、原型反馈和重新合成。
3. **知识驱动模型**：从大规模 data-driven training 转向 curriculum-engineered / knowledge-driven FMs，以获取更深 SE 知识和更高推理效率。

证据锚点：`paper_content.txt` §3.1，Page 6--7。

### 2.4 Teammate.next（队友下一代形态）

Teammate.next（队友下一代形态） 是从 static / impersonal coding assistant 到 self-evolving personalized mentor 的转变。作者要求 AI teammate 具备对话智能、社交智能和 personification，能够长期学习项目约束、人类偏好、常见错误和交互历史；它不仅执行任务，还帮助开发者澄清意图、解释设计取舍、教授模式与框架，成为 one-on-one programming mentor。

可迁移点：该层为 Paper2 的“研究者 / agent 角色边界”提供一个反面提醒：即使强调 AI teammate，也必须区分“提出建议 / 候选”与“最终裁决 / 责任归属”。

证据锚点：`paper_content.txt` §3.2，Page 7--8。

### 2.5 IDE.next（集成开发环境下一代形态）

IDE.next（集成开发环境下一代形态） 是 intent-centric IDE。它以 人机对齐（human-AI alignment） of intents 为入口，而不是以编辑源代码为中心。输入可以是非形式化功能描述、伪代码、UI sketch、示例数据等；AI 在意图对齐后驱动代码创建循环。代码默认被隐藏，只有在低层调试模式（low-level debugging mode）下才暴露给人类。论文还强调 对话（conversations）将成为核心资产，需要版本控制和管理；这里的 code 被扩展为传统代码、机器学习模型、提示词（prompt）甚至数据。

可迁移点：对 Paper2 很重要的是“conversation / decision trail as asset”这一点，可类比为系统综述中的模式批准、证据抽取、质疑和裁决日志必须成为一等制品，而不能只留下最终综述文本。

证据锚点：`paper_content.txt` §3.3，Page 8。

### 2.6 Compiler.next（编译器下一代形态）

Compiler.next（编译器下一代形态） 被定义为把 intents 合成为 runnable software 的搜索式编译器。其核心机制包括：

1. 通过 code mutations 与 self-reflection 迭代开发解决方案；
2. 在 accuracy、latency、cost 等目标之间做 multi-objective optimization；
3. 使用 goal-tracking 机制把 intents 翻译为 tests，并在需求变化时适配测试，避免从现有代码反推测试的 AI4SE 陷阱；
4. 作者引用另一篇 Compiler.next（编译器下一代形态） work，称其 prototype 包含 architecture explorers、prompt rewriters、search optimizers、observability、semantic caching 与 distributed execution，并在 HumanEval-Plus 基准 上提供初步 feasibility evidence。

可迁移点：对 Paper2 可迁移的是“goal / intent -> test / evidence obligation”的方向，即研究问题和综述元模型应下推为可检查字段与证据要求，而不是从生成文本反推结构。

证据锚点：`paper_content.txt` §3.4，Page 8--9。

### 2.7 Runtime.next（运行时下一代形态）

Runtime.next（运行时下一代形态） 面向 FMware 和 compound AI systems。作者认为未来许多软件系统会成为 FMware 或包含 FMware 模块，而 FMware 往往处于 data flywheel 驱动的持续演化状态，因此需要新的运行时。Runtime.next（运行时下一代形态） 的三项性质是：

1. **SLA-aware**：针对实时、批处理、内存密集等不同 SLA 要求进行 priority-based routing、observability、resource provisioning 和 cluster management；作者引用 companion work，称 DAG workflow、per-task slack、profiler、resource provisioner、router、cluster manager 在真实部署场景中降低 SLA violations 并改善硬件利用率。
2. **Uni-clusters**：统一训练、微调、服务和 agent self-evolution 等 FM-related activities，降低多套基础设施成本并提升资源使用效率。
3. **Edge-computing extension**：把简单请求路由到本地小模型，降低成本和延迟；如何路由被列为 OQ4。

可迁移点：Runtime.next（运行时下一代形态） 对 Paper2 的直接技术迁移有限，但其“运行时 observability + SLA / 成本 / latency 约束”的叙事可提醒 Paper2 过程证据应保留成本、耗时、失败和可复核性指标。

证据锚点：`paper_content.txt` §3.5，Page 9--11。

### 2.8 FM.next（基础模型下一代形态）

FM.next（基础模型下一代形态） 是 knowledge-driven efficient FM。作者主张通过 curriculum engineering 系统设计、维护和持续改进包含高质量领域知识的 curriculum，并用 synthetic data 扩展具体示例。SE curriculum 可借鉴 SWEBOK，覆盖 requirements reasoning、architecture design、implementation、testing、debugging、maintenance 等全生命周期能力。Curriculum 被视为可审查、可重组、可扩展、可版本化的知识资产，甚至可能比模型本身更接近 intellectual property。

本节还给出 curriculum 设计 recipe：定义目标与范围、识别 domain / subdomain、组织 hierarchical taxonomy、在叶节点放 examples / templates / evaluation rules、用 teacher FM 生成合成数据、进行 consistency testing、pilot testing、community contributions，并用 observability data / data flywheel 迭代修订。

可迁移点：这是与 Paper2 最贴近的一层。Paper2 的维度模式可被类比为 review-specific curriculum / schema：需要字段树、取值空间、例子、证据规则、缺失语义、版本、回填和观测数据驱动的修订；但不能把该文对 FM training 的设想直接等同于系统综述方法证据。

证据锚点：`paper_content.txt` §3.6，Page 11--13。

### 2.9 挑战路线图

论文 §4 把挑战统一组织为：描述、影响范围、开放问题、我们的愿景。这是本篇对 Paper2 最有迁移价值的报告结构。五组主要挑战如下：

| 挑战 | 影响组件 | 开放问题 | 我们的愿景 摘要 |
|---|---|---|---|
| Speeding up 人机对齐（human-AI alignment） | IDE.next（集成开发环境下一代形态）, Teammate.next（队友下一代形态） | OQ1：如何平衡澄清问题过多与过少？ | AI teammate 需要发展 可保持但可调整的心智理论（sticky but adjustable theory of mind），并提供 置信度 / 反馈等双向心智理论信号（mutual ToM signal）；需求工程活动仍关键。 |
| Improving efficiency of code synthesis | Compiler.next（编译器下一代形态）, Teammate.next（队友下一代形态） | OQ2：如何提高 合成效率（synthesis efficiency）且保持 / 提高准确率（accuracy）？ | 借鉴 SBSE，复用本地和 众包搜索数据（crowdsourced search data）、语义缓存（semantic caching）、自反思（self-reflection）、历史启发式与用户个性化。 |
| Improving 运行时性能（runtime performance） | Runtime.next（运行时下一代形态） | OQ3：如何超过 Ray Serve 等 服务框架（serving frameworks）？OQ4：edge-extension routing 最佳算法是什么？ | 把 FMware 工作流（FMware workflow） 编译为保留 intent 的 declarative graph；边缘路由应支持 持续学习（continual learning）和自演化（self-evolving），减少云端大模型请求。 |
| Improving 基础模型理解（FM understanding） of code and SE | Compiler.next（编译器下一代形态）, Teammate.next（队友下一代形态） | OQ5：如何让 FM 理解代码以及更广义 SE 原则？ | 引入 执行逻辑（execution logic）、变量状态、调用栈（call stack）、符号执行（symbolic execution）、数据流（data flow）、软件工程课程（SE curriculum） 和模型内部表征研究。 |
| Eliminating prompt engineering | AI teammate 与 stack 中其他 FMware 层 | OQ6：如何避免人类做 prompt engineering？ | 让 AI 负责 prompt construction；结合 model training、Compiler.next（编译器下一代形态）、feedback-driven prompt examples、template database 和 question calibration。 |

§4.6 进一步列出 OQ7--OQ14，覆盖 SE 3.0 时代“好软件工程师”定义、教育、编程语言、IDE UI、benchmark、AI teammate IP 归属、就业影响、开放创新、可访问性 / 公平机会 / 公正性（accessibility / equity / fairness） 等议题。

证据锚点：`paper_content.txt` §4.1--§4.6，Page 13--19。

### 2.10 证据 / 引用性质

这篇文章的证据构成是混合型，而不是系统综述证据链：

1. **叙事性论证**：以 SE 1.0 / 2.0 / 3.0 历史分期和技术栈迁移组织主线。
2. **快速变化工具 / 模型例子**：列举 GitHub Copilot、Claude Code、Codex CLI、Gemini Code Assist、Amazon Q Developer、Tabnine、Cline、Aider、Devin、SWE-agent、OpenHands、TRAE、Lovable、Replit、Bolt.new、Vercel v0 等；这些事实若进入论文正文必须另行按官方来源或固定快照核验。
3. **既有研究引用**：引用 productivity、AI coding assistants 接受率、prompt fragility、ToM、curriculum learning、SBSE、continual learning、code understanding 等相关研究，用于支撑局部风险或技术方向。
4. **作者组 companion works / under-review works**：Compiler.next（编译器下一代形态）、Runtime.next（运行时下一代形态）、FMware、conversational development environments、RAR、Watson / cognitive observability 等被用于支撑愿景的可行性线索，但存在作者自引用和未完全独立复现的风险。
5. **工业经验与社区讨论**：客户 / 内部团队 / OPEA / workshop / summit 被作为愿景来源，但没有可复核访谈 protocol、样本分布、编码过程或原始证据。

因此，本篇可以提供 roadmap/challenge 字段设计灵感，但不能作为“AI-native SE 已被系统证实”的证据。

### 2.11 局限

1. **非系统综述**：没有系统检索和纳排协议，不支持领域覆盖率、研究分布或统计性 finding。
2. **愿景强于证据**：核心贡献是 vision 和 roadmap，许多组件仍处于概念、prototype、companion work 或 open question 状态。
3. **自引用 / 生态偏置**：技术栈中的 Compiler.next（编译器下一代形态）、Runtime.next（运行时下一代形态）、FM.next（基础模型下一代形态）、FMware、OPEA 等与作者团队研究和产业合作密切相关，外部独立证据有限。
4. **快速漂移风险**：模型名、benchmark 排名、商业工具、vibe coding 平台和开放权重模型状态变化快；用于 Paper2 正文时必须记录核验日期和来源。
5. **用户 / 组织 / 治理证据不足**：IP、就业、教育、公平性、可访问性等 OQ 被列出，但尚未形成充分解决方案。
6. **对安全关键 / 形式化方法覆盖不足**：虽然提到 SE knowledge、tests、goal tracking 和 runtime observability，但没有针对控制系统、状态机、形式化验证或高可信软件给出专门路线。

## 3. 六类 pattern 抽取

> 重要边界：本篇不是 SLR / SMS / tertiary study，因此以下 pattern 只能作为 vision/roadmap 样本的候选结构；不能进入“已采纳系统综述证据模式”，也不能用于目标领域统计结论。

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 不适用为标准 SLR/SMS RQ。原文没有 research questions，而是以愿景问题和 OQ1--OQ14 组织 roadmap；可抽象为“挑战 -> open question -> our vision”的 roadmap question pattern。 | `paper_content.txt` §4.1--§4.6，Page 13--19。 | 可迁移到 Paper2 的候选发现 / 未来方向组织：每个 challenge 显式记录 affected component、open question、solution vision、证据类型。 | 不能替代系统综述 RQ；没有 population / intervention / outcome / context 或 mapping taxonomy 的完整协议。 |
| dimension pattern | 主要维度是 SE era、SE 2.0 limitation、SE 3.0 principle、stack component、component transition、challenge、affected stack、open question、vision / solution、evidence source。 | `paper_content.txt` Fig. 1/3、§2、§3、§4。 | 可迁移为 Paper2 的 roadmap/challenge 字段树和 A1-M1 脚手架字段候选。 | 维度来自作者愿景，不是从论文集合归纳出的分类轴；不能当成目标文献抽取 schema 的最终字段。 |
| finding pattern | 不适用为系统综述 finding。可抽取的只是 vision claims：SE 2.0 的 code-centric / cognitive-overload / model-inefficiency / additive-bias 问题，以及 SE 3.0 的 intent-centric / AI-native / knowledge-driven 方向。 | `paper_content.txt` 摘要、§2.2、§3.1、§5。 | 可迁移为“统计观察不能直接变最终发现”的反面样例：愿景性 claim 必须标注证据等级和主张强度。 | 不能把这些 claim 写成领域共识或系统证据；缺少系统纳排、质量评价、反向证据综合。 |
| evidence presentation pattern | 使用历史分期图、技术栈图、流程图、挑战表述、引用支持、companion work 和社区 / 工业经验描述来呈现证据。 | `paper_content.txt` Page 2 证据来源说明；Fig. 1--7；§3.4、§3.5、§4。 | 可迁移为 Paper2 报告结构：愿景 / roadmap 需要区分 conceptual diagram、evidence anchor、open question、prototype evidence、unverified industry signal。 | 没有 PRISMA-style flow、筛选分母、质量表、抽取表或统计汇总表；证据呈现不可等同于 SLR evidence table。 |
| validity / threat pattern | 原文没有独立 threats to validity section；局限主要散落在对 autonomous SE、ToM 非银弹、routing 未解决、OQ7--OQ14 和结论中的“only time will tell / welcome responses”。 | `paper_content.txt` §2.3、§4.1、§4.6、§5。 | 可迁移为“vision paper 局限需显式补齐”的审计要求：Paper2 若使用 roadmap 文献，必须单独记录其非系统证据、快速漂移、自引用和愿景强主张风险。 | 不适用为正式 SLR threat pattern；原文没有搜索偏倚、筛选可靠性、quality assessment 或 protocol deviation。 |
| report structure pattern | 结构为 Introduction → critical analysis of current era → future vision and technology stack → challenges / open questions → conclusion；§4 每个挑战使用 描述 / 影响范围 / 开放问题 / 我们的愿景 模板。 | `paper_content.txt` 目录性 headings；§1--§5。 | 高度可迁移为 roadmap/challenge 文献的 review 模板，也可用于 Paper2 的 候选发现 / roadmap pattern。 | 不代表 SLR/SMS 报告结构；不能替代 Method / Results / Threats 的系统综述结构。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本篇可贡献的模式先验 | 可用方式 | 禁止升级 |
|---|---|---|---|
| A1-M0 主题 / 研究问题 / 范围 / 综述元模型设定 | 提供 AI-native SE / agentic SE 的边界词：SE 2.0、SE 3.0、AI-assisted、AI-native、intent-centric、conversation-oriented、FMware、AI teammate。 | 可作为未来 pilot topic 或相关工作背景的词表；帮助定义“AI-native SE roadmap 文献”与“系统综述证据文献”的边界。 | 不得把该文当作 Paper2 的目标领域综述结果。 |
| A1-M1 脚手架挖掘 / 种子探测 | 提供 vision/roadmap 样本的结构先验：era transition、technology stack、component transition、challenge、OQ、our vision。 | 可进入 A1-M1 候选字段和 report-structure pattern；后续需研究者采纳。 | 不能未经 G1 批准直接成为正式抽取 schema。 |
| A1-M2 维度模式准备与批准 | 暴露一组 roadmap 字段：problem source、affected component、open question、solution vision、evidence type、maturity、risk、follow-up obligation。 | 可作为 A3 schema 候选输入，尤其是 challenge_action_pattern 的扩展。 | 不能以单篇 vision paper 冻结字段取值空间。 |
| A1-M3 论文收集与概览 | 提醒概览卡必须记录 `review_type = vision / roadmap`、`not_SLR = true`、`evidence_level = narrative / prototype / industry_signal`。 | 可用于后续候选池分类和降级过滤。 | 不得与 SLR / SMS / tertiary 的全文文本级 evidence 混列为同等统计样本。 |
| A1-M4 字段级证据抽取与模式演化 | 适合抽取 section-level anchors，而非统计表；每个 claim 需要标注来自 §2 limitation、§3 stack vision 或 §4 OQ。 | 可练习“愿景 claim 的来源锚点 + 证据性质 + 快速漂移风险”字段。 | 不得把 citation density 或作者论述当作已最终核验的目标事实依据。 |
| A1-M5 统计分析 | 本篇不能提供统计分析样本；最多作为“vision/roadmap 文献比例”统计中的一种类型。 | 若后续文库统计 review_type 分布，可计入 vision/roadmap 类型。 | 不能从单篇愿景文献推导领域趋势、频次或覆盖率。 |
| A1-M6 候选发现生成 | 可提供候选发现启发式：把 limitation -> stack component -> OQ -> 路线图行动项 连接起来；同时要求主张强度降级。 | 可启发 Paper2 的候选发现台账字段，例如 `finding_type = challenge / roadmap / open_question`。 | 候选发现不得跳过反向证据和研究者裁决成为最终领域发现。 |

## 6. 对 Paper2 story / method 的启发

1. **roadmap/challenge 是可抽取对象，但必须降级**：本篇作为一个样例表明，vision / roadmap 文献可以启发 challenge_action_pattern 候选结构；但 Paper2 必须记录其证据等级，不能把它和 SLR / SMS 的统计 finding 混用。
2. **字段树应保留“证据性质”而不只保留“结论文本”**：同一句 roadmap claim 可能来自作者观点、companion prototype、工业经验、benchmark 或已发表研究；这些来源的可审计性不同。
3. **技术栈图可启发维度模式版本化**：SE 3.0 stack 把 Teammate / IDE / Compiler / Runtime / FM 分层，类似 Paper2 把综述元模型、维度模式、字段证据、统计分析、候选发现和裁决分层；每层都应有职责边界。
4. **conversation as asset 支持过程证据叙事**：IDE.next（集成开发环境下一代形态） 强调 conversations version-controlled；Paper2 可借此强化“模式批准、质疑、裁决、回填日志是研究制品”的论点。
5. **curriculum engineering 可类比维度模式工程**：FM.next（基础模型下一代形态） 把 curriculum 作为可维护知识资产；Paper2 可把维度模式视为面向单个综述任务的可维护知识资产，包含 taxonomy、examples、evaluation rules、missing semantics 与 observability-driven revision。
6. **goal tracking 启发证据义务**：Compiler.next（编译器下一代形态） 中 intents -> tests 的方向可迁移为 Paper2 中 research questions / review meta-model -> extraction fields / evidence requirements 的方向。
7. **OQ 模板可用于候选发现台账**：描述 / 影响范围 / 开放问题 / 我们的愿景 是较好的 roadmap report structure；Paper2 的 候选发现 ledger 可加入 affected_dimension、evidence_strength、open_issue、proposed_action 字段。

## 7. 对 Paper2 的风险

1. **过度升级风险**：最大风险是把该文的愿景性判断写成系统综述发现。必须在任何引用处标明“vision/roadmap，不是 SLR/SMS evidence”。
2. **快速事实漂移风险**：模型版本、工具、benchmark 排名、commercial platform 变化快；若用于背景，必须在正式写作前重新核验官方来源和日期。
3. **自引用 / 生态闭环风险**：多个关键支撑来自作者团队 companion works，可能放大同一研究生态的观点。Paper2 若抽取 roadmap evidence，应记录 independent validation status。
4. **反向证据不足**：论文欢迎 opposing views，但自身没有系统呈现反对观点、失败案例或替代路线。
5. **治理与安全关键不足**：OQ11--OQ14 承认 IP、就业、公平性等开放问题；对形式化验证、安全关键控制系统、合规认证没有深入路线，不能直接支撑 project_1 / 博士主线的形式化方法论断。
6. **方法可执行性不等于工具可用性**：Compiler.next（编译器下一代形态） / Runtime.next（运行时下一代形态） 的 prototype evidence 只是局部可行性线索，不证明完整 SE 3.0 stack 已可运行或可泛化。

## 9. 待复核

1. 需要人工打开 `paper.pdf` 核对 Fig. 1--7 的版式、组件命名和图中箭头 / 标签；本轮仅依据 `paper_content.txt` 文本抽取。
2. 若正式写入论文或投稿材料，仍建议在提交前按当轮 CCF 官方目录复核；本轮沿用本仓库 ccf_venues 缓存记录 TOSEM 为 A 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
3. 若引用模型、工具、benchmark 或 commercial platform 示例，需要在正式写作前按官方来源记录核验日期，避免使用已漂移事实。
4. 若把 Compiler.next（编译器下一代形态）、Runtime.next（运行时下一代形态）、FMware、RAR、Conversational Development Environments 等 companion works 作为证据，需要分别读取原文，区分已发表、预印本、under review、prototype 和真实部署证据。
5. 若后续把该文纳入 Paper2 的脚手架样本，应在总账中显式标为 `vision / roadmap`，并把“不得作为系统综述证据”写入候选池备注。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__codex.md](../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__codex.md)、[../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__claude.md](../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__claude.md)、[../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__deepseek.md](../../audits/a1dt-v2-19x3/results/ai-native-se-roadmap__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/ai-native-se-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/ai-native-se-roadmap.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `ai-native-se-roadmap` |
| 审计代理 | `claude`（claude-opus-4-7[1m]，本地直接读取，无 subagent / 后台 智能体） |
| 是否已读 `paper_content.txt` | 是；分两页读取 1–707、708–1146，覆盖摘要、§1–§5、参考文献 [1]–[117] |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；与本地引文键 `Hassan_2026` 与 DOI `10.1145/3807901`、`publication_date 2026-04-09` 交叉核对一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅文本审计，Fig. 1/2/3/4/5/6/7 未做版面核验，留 A2a |
| 原文类型 | **愿景 / 路线图 / 提案**（自我定位）；不是 SLR、SMS、tertiary、MLR、指南 检索研究 |
| 被编码样本单位 | 不存在系统样本库；原生编码对象是 **{SE 1.0/2.0/3.0 三时代 baseline}**、**{队友下一代形态（Teammate.next） / 集成开发环境下一代形态（IDE.next） / 编译器下一代形态（Compiler.next） / 运行时下一代形态（Runtime.next） / 基础模型下一代形态（FM.next） 五层技术栈组件}** 和 **{6 个主 挑战 + OQ1–OQ14 共 14 个 开放问题}** |
| 样本数量 / 分母 | 不适用为统计分母；可记录的"原生项数"：3 个时代、5 个 技术栈组件、6 个主 挑战、14 个 OQ；引用 [1]–[117] 共 117 条，但作者未声明任何检索 / 纳排，因此 117 不是 SLR 分母 |
| 原生树类型 | **降级树（路线图/挑战 树）+ 辅助"时代基线（era baseline）对照树"**；不是 SLR 维度森林 |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取的文件与范围**：

- `bibtex.bib`：第 1–10 行，确认 `Hassan_2026` / TOSEM / 2026 / DOI `10.1145/3807901`。
- `metadata.json`：第 1–35 行，确认 `review_type=vision/roadmap`、`eligible_for_schema_seed=true`（模式种子字段为真）、`eligible_for_statistical_synthesis=false`、`evidence_role=roadmap_boundary_anchor`、CCF=A、TOSEM 期刊、arXiv `2410.06107` 作为开放全文来源。
- `paper_content.txt`：1–1146 行全文文本（分两页读取），包含摘要、§1 Introduction、§2 critical analysis of SE 2.0、§3 Vision of SE 3.0（含 §3.1–§3.6 五个 技术栈组件）、§4 Challenges（§4.1–§4.5 五条主 挑战 + §4.6 OQ7–OQ14）、§5 Conclusion 与 [1]–[117] 全部参考文献。
- `review.md`：1–428 行全文，含维度树复原；证据链已迁至 evidence_chain.md。
- `paper.pdf`：未打开，因此 Fig. 1–7 的版面 / 箭头 / 标签 / Figure 6（NIPS 2015 Sculley 改图）未做版面核验，仅依赖文本里的 Figure 引用句。

**仅基于 text 的局限**：所有 Figure 的视觉布局、表内分类（如 Fig. 1 的 SE 1.0/2.0/3.0 三栏对照、Fig. 3 stack 图的箭头与命名一致性、Fig. 5/Fig. 7 截图取自 GitHub Copilot / OpenAI docs 的具体内容、Fig. 6 中"FM Code" vs "AIware / Compute / Curriculum Engineering" 等组件的精确命名）都需要 A2a 打开 PDF 复核。

**关键原文证据锚点（按出现顺序）**：

1. **摘要 / 自我定位**（Page 1, 行 8–25）："We propose a shift towards SE 3.0 ... We outline the key components ... We also present a 路线图 of 挑战 that must be overcome to realize our 愿景."
2. **愿景来源声明**（Page 2, 行 61–69）：愿景 基于 "(i) surveys of academic and gray literature, (ii) in-depth discussions ..., (iii) meetings with our customers and our own internal development teams ..., (iv) our practical experience with the research and development of FMware, and (v) our close interactions with several industry partners (40+ leading companies, including Intel, AMD, RedHat, HuggingFace, and SAP) as part of the Open Platform for Enterprise AI (OPEA) alliance"——这是非系统综述声明。
3. **三时代 baseline 对照**（§1 与 Fig. 1, Page 2–3, 行 100–131）：SE 1.0 (code-centric / program analysis) → SE 2.0 (code-centric AI4SE / data-driven FMs) → SE 3.0 (intent-centric / AI-native / knowledge-driven)。
4. **SE 2.0 三类 limitation + 1 类 boundary**（§2.2–§2.3, Page 3–5）：(2.2.1) cognitive overload；(2.2.2) inefficient 模型 training；(2.2.3) suboptimal code 质量 / additive bias；(2.3) autonomous SE benchmark limitation (SWE-Bench Verified, TRAE 75.2%, 仅 Python、12 项目，~70% 任务来自 3 个项目)。
5. **五层技术栈定义**（§3.2–§3.6 + Fig. 3, Page 7–13）：队友下一代形态（Teammate.next） / 集成开发环境下一代形态（IDE.next） / 编译器下一代形态（Compiler.next） / 运行时下一代形态（Runtime.next） / 基础模型下一代形态（FM.next），每层都自带 `from_state → to_state` 转换、所需 capability 与 companion paper 引用。
6. **Challenge 原文 4 字段 模式**（§4 引言段, Page 13, 行 580–586）："For each 挑战, we include a description, what parts of the SE 3.0 stack it affects (Figure 3), one or more 开放问题, and our 愿景 regarding the solution to those questions." — 这就是 `描述 / 影响范围 / 开放问题 / 我们的愿景` 四字段模板。
7. **OQ1–OQ6 主 挑战**（§4.1–§4.5, Page 13–18）：OQ1 ToM 平衡；OQ2 合成效率（synthesis efficiency）；OQ3 runtime > Ray Serve；OQ4 关系边 routing；OQ5 FM 理解 SE；OQ6 提示词工程（prompt engineering）消除。
8. **OQ7–OQ14 其他开放问题**（§4.6, Page 18, 行 800–823）：教育 / 编程语言 / IDE UI / Compiler benchmark / IP / 就业 / 开放创新 / accessibility & equity & fairness。
9. **Companion / under-review 自引用证据矩阵**（§3.4、§3.5、§4.1、§4.2、§4.3, [28]/[44]/[45]/[85]/[98]/[114]）：编译器下一代形态（Compiler.next） [28] 仍在 TOSEM 审稿；FMware [45] preprint；Watson [85]、SPICE [70]、RAR [98] 已被会议接收但仍是 self-citation 生态。
10. **运行时下一代形态（Runtime.next） 经验声明**（§4.3, Page 16, 行 696–697）："Preliminary results show a latency improvement in the order of 30% compared to Ray Serve."
11. **RAR 路由经验**（§4.3, Page 17, 行 716–718）："on different subsets of the popular MMLU benchmark [47], our approach routes 50% fewer requests to computationally expensive 模型 while maintaining around 90% of the general response 质量."
12. **结论 + 商业 vibe-coding 平台清单**（§5, Page 19–20, 行 851–853）：Lovable / Base44 / Replit / Bolt.new / V0 by Vercel 被列为"很早期的 SE 3.0 苗头"。

### 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象是什么？**
   - 不是一组论文 / 工具 / 制品 / 数据集样本，而是一个 **paradigm（SE 3.0）**及其内部的 **5 个 技术栈组件** + **3 个 era baseline 对照** + **14 个 开放问题 / 挑战**。每一层 component 是一个抽象架构对象；每一个 OQ 是一个 路线图 行动项。

2. **作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**
   - **没有**。§1 (Page 2, 行 61–69) 显式承认愿景来自 "surveys of academic and gray literature + 行业 workshop + 客户讨论 + 作者研发经验 + OPEA 工业互动"，但没有给出搜索数据库、检索式、纳入分母、排除标准、质量评价 rubric、抽取表或数据综合协议。§4 引言段也明确说 "The list of 挑战 that we present is not meant to be extensive"（Page 13, 行 584）。

3. **原文字段来自哪里？**
   - **stack-component 模板**：来自 Fig. 3 的"SE 2.0 vs SE 3.0"对照（每个 component 都有 `from_state` 子弹列表 + `to_state` 子弹列表），文中再用 §3.2–§3.6 展开。
   - **挑战 4 字段模板**：作者在 §4 引言段（Page 13, 行 580–586）显式给出 `描述 / 影响范围 / 开放问题 / 我们的愿景`，并在 §4.1–§4.5 严格执行。
   - **Open Question 编号**：作者显式编号 OQ1–OQ14，每个 OQ 都有自然语言文本与（前 6 个） "我们的愿景" 段落。
   - **没有 抽取 form / 分类方案（classification scheme；首次术语） / 分类法 table / 质量量规 / mapping table / appendix / 复现包**。

4. **RQ 与样本单位是什么关系？**
   - 本文没有 RQ；最接近 RQ 的对象是 §4 的 6 个主 挑战 + 14 个 OQ。这些 OQ 是"路线图行动项"，不是"用于编码样本的研究问题"。

5. **若无系统样本库，如何降级？**
   - 按 A1-DT v2 规则，本篇必须降级为 **边界锚点 + 方法学种子 + candidate heuristic**，不进入主统计池。`metadata.json` 已正确标注。

### 3. 原生样本编码维度树 / 维度森林

> 中文化导读：本维度树复原的是一篇路线图论文如何组织“AI 原生软件工程”的历史阶段、未来形态、挑战与研究议程。它不是传统 SLR 的样本编码表，因此树中保留了编译器、集成开发环境、基础模型、意图中心、代码中心、个性化、对话式等原文术语。阅读时应把中文层级关系放在第一位：先看软件工程范式演化，再看下一代环境组件，再看开放问题与影响范围。可迁移到 Paper2 的是“路线图也能形成维度森林，并且需要明确字段缺失和愿景性证据边界”，不是该文对 AI 原生软件工程未来形态的具体判断。

本篇的原生结构是 **"时代基线（era baseline）对照树 + 5 层技术栈（stack）树 + 挑战 / 开放问题（挑战/OQ）树"** 三棵子树构成的**维度森林**，而不是一棵 SLR 编码树。


> 进一步说明：这篇论文不是传统意义上的系统综述，所以不能用“样本论文—抽取字段—统计发现”的单一路径来读。它更像一个路线图型证据源：作者先给出软件工程范式演化，再提出下一代开发环境组件，最后把开放问题映射到组件和愿景。后续 Paper2 如果借用它，应该借用“路线图如何构造维度森林”的写法：一层是历史阶段，一层是系统组件，一层是开放问题，一层是影响范围和证据边界。不能把该文的未来判断直接当作已验证 finding。这里保留的英文，多数是原文组件名、工具名、基础模型缩写或代码生态名；它们不承担中文叙事主干。中文叙事主干是：路线图论文也能产生可复用的维度 pattern，但每个 pattern 都要标明它来自愿景、经验观察、作者立场还是可复验样本。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[论文根节点] 面向 AI 原生软件工程（Towards AI-Native SE, SE 3.0）— 愿景 + 路线图

├── [树-A] 软件工程时代基线 对照树 （Fig. 1, §1, §2.1, §3.1）
│   ├── 时代编号              取值 ∈ {SE 1.0, SE 2.0, SE 3.0}     // 完整枚举（封闭，3）
│   ├── 时代时间锚 取值 ∈ {1968 年以来（NATO 会议；since 1968） ;
│   │                          2000 年代中期以来（MSR、GitHub 2008、Stack Overflow 2008、深度学习 2010 年代中期） ;
│   │                          2020 年代末到 2030 年代初（late 2020–early 2030）}        // 自由文本 + 时间锚
│   ├── 代码取向    取值 ∈ {以代码为中心（code-centric）, 代码中心 + AI4SE, 以意图为中心（intent-centric）}   // 封闭，3
│   ├── 工具引擎      取值 ∈ {程序分析（program analysis）, 数据驱动且低效的基础模型（data-driven inefficient FMs）, 知识驱动且高效的基础模型（knowledge-driven efficient FMs）}  // 封闭，3
│   └── 人类角色          取值 ∈ {人类中心（human-central）, 人在环且有副驾驶（human-in-loop with copilots）, 人机共生且 AI 驱动代码循环（human-AI symbiosis / AI drives code-loop）}  // 封闭，3
│
├── [树-B] SE 3.0 五层技术栈树 （Fig. 3, §3.2–§3.6）
│   ├── [B1] 队友下一代形态（Teammate.next）            // 角色：个性化 AI 伙伴（personalized AI partner）
│   │     ├── 起始状态 取值 ∈ {静态且非个性化的编码助手（static, impersonal coding assistant）}
│   │     ├── 目标状态   取值 ∈ {自演化的个性化导师（self-evolving, personalized mentor）}
│   │     ├── 所需特征 取值子集 ⊆ {对话智能（conversational intelligence）, 社会智能（social intelligence）, 人格化（personification）,
│   │     │                       自主自反思（autonomous self-reflection）, 循环上下文学习（recurrent-context learning）, 导师角色（mentor role）}
│   │     ├── 依赖于 至少包含 ⊇ {编译器下一代形态（Compiler.next） (§3.4)}
│   │     └── 配套证据 取值 ∈ {[24] Chaves 与 Gerosa 综述（survey）, [36] Gallaba 等心智理论多智能体（ToM multi-智能体）}
│   ├── [B2] 集成开发环境下一代形态（IDE.next）                 // 角色：以意图为中心的 IDE（intent-centric IDE）
│   │     ├── 起始状态 取值 ∈ {以代码为中心（code-centric）, 编辑（editing）}
│   │     ├── 目标状态   取值 ∈ {以意图为中心（intent-centric）, 对话式（conversational）}
│   │     ├── 输入模态 取值子集 ⊆ {非正式自然语言描述（informal NL description）, 伪代码（pseudocode）, UI 草图（UI sketch）, 示例数据（example data）}
│   │     ├── 代码可见性 取值 ∈ {默认隐藏（hidden by default）, 低层调试模式（low-level debugging mode）}
│   │     ├── 对话作为资产 取值 ∈ {版本化（versioned）, 归档（archived）}
│   │     ├── 代码定义范围 至少包含 ⊇ {Python 代码（Python code）, 机器学习模型（ML 模型）, 提示词（prompts）, 数据（data）}
│   │     └── 启发来源 取值 ∈ {TDD [19,20]}
│   ├── [B3] 编译器下一代形态（Compiler.next）            // 角色：基于搜索的意图合成器（search-based intent synthesizer）
│   │     ├── 起始状态 取值 ∈ {逻辑规则实现（logic-rule realization）}
│   │     ├── 目标状态   取值 ∈ {搜索空间探索（search-space exploration）/ 多目标优化（multi-objective optimization）}
│   │     ├── 核心机制 取值子集 ⊆ {代码变异（code mutation）, 自反思（self-reflection）, 语义缓存（semantic caching）,
│   │     │                       分布式执行（distributed execution）, 多目标优化（multi-objective optimization）,
│   │     │                       目标追踪（goal tracking；intent→test）, 迭代合成（iterative synthesis）}
│   │     ├── 目标 取值子集 ⊆ {准确率（accuracy）, 延迟（latency）, 成本（cost）}
│   │     ├── 使用的基准 取值 ∈ {HumanEval-Plus 基准 [61]}
│   │     └── 配套证据 取值 ∈ {[28] Cogo 编译器下一代形态（Compiler.next）（TOSEM 在审稿 / under-review）, [68] Autogen}
│   ├── [B4] 运行时下一代形态（Runtime.next）             // 角色：服务等级协议感知的统一集群运行时与边缘扩展（SLA-aware unified cluster runtime + edge computing）
│   │     ├── 起始状态 取值 ∈ {服务模型（serving 模型）}
│   │     ├── 目标状态   取值 ∈ {服务复合应用（serving compound apps / AIware）}
│   │     ├── 质量属性  至少包含 ⊇ {服务等级协议感知（SLA-aware）, 统一集群（unified cluster）, 边缘计算扩展（edge-computing extension）}
│   │     ├── 服务等级协议工作负载类型（SLA workload types）取值子集 ⊆ {实时（real-time）/ 批处理（batch）/ 内存密集（memory-intensive）}
│   │     ├── 运行时组件 取值子集 ⊆ {剖析器（profiler）, 资源提供器（resource provider）, 路由器（router）, 集群管理器（cluster manager）,
│   │     │                          单任务余量（per-task slack）, 有向无环图工作流（DAG workflow）}
│   │     ├── 报告指标 取值 ∈ {相对 Ray Serve 延迟降低 30%（30% latency improvement） [114]}
│   │     ├── 边缘路由指标 取值 ∈ {RAR [98]: 昂贵请求减少 50%（50% fewer expensive requests）, MMLU 上约 90% 质量（~90% 质量） [47]}
│   │     └── 配套证据 取值 ∈ {[45] FMware 预印本（preprint）, [114] FMArts/Fusion, [98] RAR}
│   └── [B5] 基础模型下一代形态（FM.next）                  // 角色：课程工程化的知识驱动基础模型（curriculum-engineered knowledge-driven FM）
│         ├── 起始状态 取值 ∈ {数据驱动且低效的基础模型（data-driven inefficient FMs）}
│         ├── 目标状态   取值 ∈ {课程工程化的知识驱动高效基础模型（curriculum-engineered knowledge-driven efficient FMs）}
│         ├── 课程配方（curriculum recipe）取值子集 ⊆ {定义范围（define scope）, 识别领域 / 子领域（identify domain/subdomain）,
│         │                         层级分类法（hierarchical 分类法）, 示例 / 模板 / 评价规则（examples/templates/评价规则）,
│         │                         教师基础模型合成数据（teacher-FM synthetic data）, 内部一致性测试（internal consistency testing）,
│         │                         试点测试（pilot testing）, 社区贡献（community contribution）, 数据飞轮精化（data-flywheel refinement）}
│         ├── 课程根分支（curriculum 根节点 branches；原文术语）取值 ∈ {知识（knowledge）/ 基础技能（foundational skills）/ 组合技能（composition skills）} (InstructLab)
│         ├── 参考课程（reference curriculum）取值 ∈ {SWEBOK [106]}
│         ├── 软件工程能力轴（SE competence axes）取值子集 ⊆ {需求推理（requirements reasoning）, 架构设计（architectural design）,
│         │                          实现（implementation）, 测试（testing）, 调试（debugging）, 维护（maintenance）}
│         ├── 可观测性轴（observability axis）取值 ∈ {认知可观测性（cognitive observability）[85]}
│         └── 配套证据 取值 ∈ {[51,91] InstructLab, [104] 课程学习综述（curriculum learning survey）, [15] phi 模型族（phi family）, [85] Watson}
│
└── [树-C] 挑战 × 开放问题（OQ）路线图树（§4.1–§4.6，含每个挑战的 4 字段模式）
    ├── 挑战模板（作者在 §4 引言段显式声明）
    │     ├── 描述           : 自由文本
    │     ├── 影响范围               : 多选，取值子集 ⊆ {队友下一代形态（Teammate.next）、集成开发环境下一代形态（IDE.next）、编译器下一代形态（Compiler.next）、运行时下一代形态（Runtime.next）、基础模型下一代形态（FM.next）}
    │     ├── 开放问题（Open Question, OQ#）   : 自由文本 + 整数 id
    │     └── 我们的愿景            : 自由文本 + 配套论文引用（companion-paper references）
    │
    ├── [C1] §4.1 人机对齐（human-AI alignment）   → 影响范围（affects）= {集成开发环境下一代形态（IDE.next）, 队友下一代形态（Teammate.next）}   → OQ1
    ├── [C2] §4.2 合成效率（synthesis efficiency） → 影响范围（affects）= {编译器下一代形态（Compiler.next）, 队友下一代形态（Teammate.next）} → OQ2
    ├── [C3] §4.3 运行时性能（runtime performance）  → 影响范围（affects）= {运行时下一代形态（Runtime.next）}              → OQ3, OQ4
    ├── [C4] §4.4 基础模型理解（FM 理解）     → 影响范围（affects）= {编译器下一代形态（Compiler.next）, 队友下一代形态（Teammate.next）} → OQ5
    ├── [C5] §4.5 提示词工程（prompt engineering）   → 影响范围（affects）= {队友下一代形态（Teammate.next） 与所有 FMware 层} → OQ6
    └── [C6] §4.6 其他开放问题（OQ；无影响范围 / 愿景字段）
          ├── OQ7  SE 3.0 中的良好软件工程 / 下一代软件工程训练 / 计算机科学课程（SE 3.0 中的良好软件工程 / 下一代软件工程训练 / 计算机科学课程）
          ├── OQ8  面向 AI 智能体的编程语言 / token 高效编程语言（面向 AI 智能体的编程语言 / 词元高效编程语言） [114]
          ├── OQ9  集成开发环境下一代形态（IDE.next） 用户界面 / 插件与智能体 / 智能体式 IDE（集成开发环境下一代形态（IDE.next） UI / plugin vs 智能体 / agentic IDE） [44]
          ├── OQ10 编译器下一代形态（Compiler.next） 基准与可解释性（基准与可解释性） [75]
          ├── OQ11 开发者离职后 AI 队友知识产权归属（AI teammate IP ownership upon developer leaving）
          ├── OQ12 SE 3.0 对岗位的影响（岗位影响）
          ├── OQ13 开放创新与跨孤岛协作（开放创新 / 跨孤岛协作）
          └── OQ14 可访问性 / 公平机会 / 公正性（可访问性 / 公平机会 / 公正性） [96]
```

**说明**：

- **取值空间封闭性**：树-A 的 era_id（3 个值）与 树-B 的 5 个 技术栈组件 是**已封闭枚举**；树-C 的 14 个 OQ 是**作者声明的当前枚举**，但作者也写明 "not meant to be extensive"，因此 OQ 集合是**开放枚举（snapshot）**。
- **关系边**：树-B 与 树-C 之间存在显式 `影响范围` 关系（多对多），是本篇里**唯一可机械化的关系型字段**（详见 §5 关系边表）。
- 与 review.md "维度树复原"中六叶通用接口的对比：本树是**原文真实结构**；六叶接口是**跨论文投影层**，二者必须分层维护。

### 4. 叶子维度表

仅列**最关键的叶子字段**（取值空间和证据锚点都来自原文；未观察到原文取值的字段标 `待核验`）。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `era.id` | SE 时代标识 | 树-A | Fig. 1 三栏标题 | 软件工程演化时代 | {SE 1.0, SE 2.0, SE 3.0} | 完整枚举（封闭，3） | 不适用 | 模式种子（schema_seed） | 可作"era-baseline 对照模板"启发 | Fig. 1 / §1 / §2.1 / §3.1 (行 27, 91–94, 280–289) | 仅迁移结构，不迁移"SE 3.0 已成立"的领域结论 |
| `era.code_orientation` | 代码取向 | 树-A | Fig. 1 第一行 bullet | 时代主导开发取向 | {code-centric, code-centric+AI4SE, intent-centric} | 完整枚举（封闭，3） | 不适用 | 模式种子（schema_seed） | 启发 paper2 的 paradigm 对照轴 | Fig. 1 / §3.1 (行 280–302) | 迁移轴名 |
| `era.tooling_engine` | 工具引擎 | 树-A | Fig. 1 第三行 bullet | 时代主导技术引擎 | {program analysis, data-driven FMs, knowledge-driven FMs} | 完整枚举（封闭，3） | 不适用 | 模式种子（schema_seed） | 启发"baseline 模型类型"轴 | Fig. 1 (行 100–124) | 迁移结构 |
| `stack.component_name` | 技术栈组件名 | 树-B | Fig. 3 / §3.2–§3.6 标题 | SE 3.0 stack 的组件 | {队友下一代形态（Teammate.next）, 集成开发环境下一代形态（IDE.next）, 编译器下一代形态（Compiler.next）, 运行时下一代形态（Runtime.next）, 基础模型下一代形态（FM.next）} | 完整枚举（封闭，5） | 不适用（作者明确 5 个） | 模式种子（schema_seed）；可作 5 项分布的"内部计数" | 候选 layered-architecture 模式启发 | Fig. 3 / §3.2–§3.6 (行 250–278, 307–520) | 仅迁移"分层 愿景 stack"结构，不迁移层名 |
| `stack.from_state` / `stack.to_state` | 转换前/后状态 | 树-B | Fig. 3 SE2.0/SE3.0 两栏 + §3 各小节 | 每层 component 的转换 | 自由文本，但每个 component 都有 1–N 条 bullet | 自由文本 + 半结构 bullet | 缺失视为非显式宣称 | 模式种子（schema_seed） | 启发"component transition 模式" | Fig. 3 (行 258–278) | 迁移结构 |
| `stack.required_traits` | 所需能力子集 | 树-B | §3.2–§3.6 段落正文 | 该层为实现 to_state 需要的能力 | 各层不同的开放集合（见 §3 树） | 层级枚举（开放） | 缺失视为"作者未声明" | 模式种子（schema_seed） | 候选 capability/property axis 启发 | §3.2 (行 313–337), §3.3 (行 343–374), §3.4 (行 375–417), §3.5 (行 418–476), §3.6 (行 477–578) | 迁移结构 |
| `挑战.template_field` | 挑战 模板字段 | 树-C | §4 引言段 (行 580–586) 显式声明 | 挑战 的 4 字段 模式 | {描述, 影响范围, 开放问题, 我们的愿景} | 完整枚举（封闭，4） | 缺失视为 unstructured 挑战 | 模式种子（schema_seed）；可作"4-tuple 路线图 entry"模板 | **高迁移价值**：Paper2 候选发现台账可作为候选采纳 | §4 引言 (行 580–586) | 完全可迁移结构 |
| `挑战.id` | 挑战 编号 | 树-C | §4.1–§4.5 小节标题 + §4.6 列表 | 主 挑战 与附加 OQ | C1–C5 + OQ7–OQ14（OQ1–OQ6 嵌入 C1–C5） | 层级枚举（半开放） | 作者明确 "not exhaustive" | 模式种子（schema_seed） | 候选 路线图-completeness baseline | §4.1–§4.6 (行 587–823) | 迁移编号体系 |
| `挑战.affects` | 影响的 stack 层 | 树-C × 树-B | §4.1–§4.5 每节的 `影响范围:` 行 | 挑战 → 技术栈组件 的多对多关系 | ⊆ {队友下一代形态（Teammate.next）, 集成开发环境下一代形态（IDE.next）, 编译器下一代形态（Compiler.next）, 运行时下一代形态（Runtime.next）, 基础模型下一代形态（FM.next）}；§4.6 OQ7–OQ14 未填 | 关系值（多选） | §4.6 未填默认 unknown | 模式种子（schema_seed）；可作"挑战 → component 覆盖率"内部计数 | **关键关系字段**：可形成 5×6 影响矩阵 | §4.1 行 594 / §4.2 行 645 / §4.3 行 681 / §4.4 行 728 / §4.5 行 761 | 迁移关系建模方式 |
| `挑战.open_question` | OQ 文本 | 树-C | OQ# 框 | OQ 自然语言 | 自由文本 + 整数 id | 自由文本 + id | -- | 模式种子（schema_seed） | 候选 RQ-style 发现 启发 | §4.1–§4.5 OQ 框 / §4.6 列表 | 迁移结构 |
| `挑战.our_vision.companion_evidence` | 愿景配套引用 | 树-C | §4.1–§4.5 段尾"complementary work" | 支撑 愿景 的 companion paper | 取值为 {[28], [36], [44], [45], [85], [98], [114]} 等作者团队工作 | 引用集合 | 缺失视为 愿景-only | 模式种子（schema_seed） | **风险字段**：可标记 self-citation 生态 | §4.1 (行 632–636), §4.2 (行 672–676), §4.3 (行 695–697, 714–718) | 迁移"愿景—证据—独立性"链路 |
| `evidence.source_type` | 证据来源类型 | 跨树 | §1 行 61–69 自我声明 | 愿景与 挑战 的证据来源 | {非正式文献调研（informal literature survey）, 灰色文献（gray literature）, 工作坊/峰会（workshop/summit）, 客户讨论（customer discussion）, 内部团队经验（internal team experience）, OPEA 工业互动（OPEA 工业 interaction）, 配套论文（companion paper）, 同行评审既有工作（peer-reviewed prior work）} | 层级枚举（开放） | -- | 模式种子（schema_seed） | **关键降级字段**：用于区分 愿景 claim vs prototype 证据 vs peer-reviewed 证据 | §1 (行 61–69), §3.4 (行 405–417), §4.3 (行 696–697, 714–718) | 迁移"来源类型 → 主张强度"映射 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel.affects` | 树-C 中的 挑战（C1–C5） | `影响范围:`（多对多） | 树-B 中的 技术栈组件 | ⊆ {队友下一代形态（Teammate.next）, 集成开发环境下一代形态（IDE.next）, 编译器下一代形态（Compiler.next）, 运行时下一代形态（Runtime.next）, 基础模型下一代形态（FM.next）} | §4.6 OQ7–OQ14 未填，记为 unknown | §4.1 行 594；§4.2 行 645；§4.3 行 681；§4.4 行 728；§4.5 行 761 | 形成 挑战 × component 覆盖矩阵；可量化"哪个 stack 层被最多 挑战 关联" |
| `rel.depends_on` | 树-B 中的 技术栈组件 | 依赖 / 接口连接（depends on / interfaces with） | 同 树-B 其他 component 或 FMware | 各层不同 | 缺失视为未声明依赖 | §3.2 (Teammate→Compiler, 行 311–312)；§3.3 (IDE→Compiler+Teammate, 行 361–362)；§3.4 (Compiler→基础模型下一代形态（FM.next）, 行 381)；§3.5 (Runtime→FMware, 行 437)；§3.6 (基础模型下一代形态（FM.next）→编译器下一代形态（Compiler.next）, 行 495–496) + 结论段 (行 848: "集成开发环境下一代形态（IDE.next） largely depends on all other components") | 候选"stack 依赖拓扑"启发 |
| `rel.inspired_by` | 树-B / 树-C 的设计选择 | 受启发 / 类比自（draws inspiration from / draws analogy） | 外部理论或既有研究 | {TDD [19,20], ToM [17,103], Bloom [21], SBSE [39], continual learning [101], Voyager [100], Sculley [87], InstructLab [51,91], phi 模型族（phi family） [15], SWEBOK [106]} | 缺失视为纯作者构造 | §3.3 (行 372–374 TDD)；§4.1 (行 599–603 ToM)；§3.2 (行 332–335 Bloom)；§4.2 (行 653 SBSE)；§4.3 (行 708–710 continual learning, Voyager)；§3.6 (行 547–548 Sculley)；§3.6 (行 524 InstructLab)；§3.6 (行 493–494 phi 模型族（phi family）)；§3.6 (行 495–496 SWEBOK) | 候选"愿景 anchored to 既有理论"链路 |
| `rel.exemplified_by` | 树-C / 树-B | 举例体现（examples / early glimpses） | 外部商业 / 开源工具 | 树-C: GitHub Copilot [67], Claude Code [11], Codex CLI [74], Gemini Code Assist [3], Q Developer [1], Tabnine [6], Cline [26], Aider [8], Devin [27], SWE-智能体 [112], OpenHands [105], TRAE [93];  §5: Lovable [62], Base44 [18], Replit [84], Bolt.new [90], V0 [99] | 缺失视为无举例 | §1 行 33–34；§2.3 行 222–225；§5 行 851–853 | **快速漂移风险字段**：必须按官方来源记日期 |

`★ Insight ─────────────────────────────────────`
- `影响范围:` 这条关系边是本篇 模式 里**唯一可严格机械化**的关系字段——作者在 §4 引言段已经把它写成模板的第二个字段，而每个 §4.1–§4.5 都严格遵守。这是 Paper2 维度模式可以直接借用的"显式关系字段先例"。
- 反过来，§4.6 的 OQ7–OQ14 故意省略了 `影响范围:` 与 `我们的愿景:`——这本身就是一个"作者降级"信号：尚未成熟的 OQ 不强行填全表。这对 Paper2 的 候选发现 台账也是好启发：未成熟项允许字段缺失，但缺失语义必须显式（这里是"作者尚未发展完整 愿景"）。
`─────────────────────────────────────────────────`

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 原文中由字段 / 统计表支持的"内部统计观察"（极少）

- **5 个 技术栈组件**（封闭枚举，分母=5）
- **6 个主 挑战 + 14 个 OQ**（作者声明的 snapshot，分母=20，但 "not exhaustive"，分母不严格）
- **挑战 × component 覆盖矩阵**：C1→{IDE,Teammate}，C2→{Compiler,Teammate}，C3→{Runtime}，C4→{Compiler,Teammate}，C5→{Teammate+all FMware}。队友下一代形态（Teammate.next） 被 4/5 主 挑战 影响（明显高频）；运行时下一代形态（Runtime.next） 被 1/5。
- **作者引用 [1]–[117]**：共 117 条，其中作者团队 / 同生态 self-citation 至少含 [28]、[36]、[40]、[41]、[42]、[43]、[44]、[45]、[70]、[85]、[92]、[98]、[114]（≈12+/117 ≈ 10%+，**待 A2a 复核**）；这是"愿景—证据生态闭环"的潜在量化信号。

#### 6.2 原文 discussion / 推荐 / 路线图 提出的"候选发现"（仅作启发）

- "AI 应主导 code-creation loop，人类聚焦 intent"（§3.1, §3.3）—— 愿景 claim，不是 发现。
- "synthesis 应被建模为 SBSE 风格搜索 + semantic caching + self-reflection"（§3.4, §4.2）—— 愿景 claim + 1 篇 HumanEval-Plus 基准 初步可行性证据 [28]，不是 SLR 发现。
- "curriculum > 大规模 unstructured pretraining"（§3.6）—— 愿景 claim + 类比 InstructLab/phi，**没有直接证据**。
- "ToM-enhanced multi-智能体 显著提升 intent clarification"（§4.1, 行 632–636，引 [36]）—— 单篇 companion 经验研究（empirical） 研究 (150 scenarios)，**不是综述证据**。
- "运行时下一代形态（Runtime.next） vs Ray Serve 30% latency improvement"（§4.3，引 [114]）—— 单篇 companion prototype 经验，**不可外推**。
- "RAR 在 MMLU 子集上减少 50% 高成本请求 / 保持 ~90% 质量"（§4.3，引 [98]）—— 同上。

#### 6.3 对 Paper2 可迁移的方法学启发（**可迁移**）

1. **4-tuple 挑战 entry 模板**：`{描述, 影响范围, 开放问题, 我们的愿景}` 可作为候选迁移启发；后续必须经 A2a 证据核验和研究者裁决后采纳为 Paper2 候选发现 / 路线图条目台账的字段。
2. **`影响范围:` 关系字段**：把候选发现显式挂到维度模式层（component / dimension），形成可量化的覆盖矩阵。
3. **三时代 baseline 对照**：把"被审计对象 vs 替代方案"显式拆成 from_state / to_state，并附"工具引擎 / 角色 / 取向"三轴对照——这对 Paper2 比较综述方法学时是好脚手架。
4. **OQ7–OQ14 字段缺失模式**：未成熟的候选条目允许字段缺失，但缺失必须显式（"作者未发展完整 愿景"），不可静默 NULL。
5. **companion-证据 显式标签**：每条 愿景 必须标注配套证据强度（经验研究（empirical） / prototype / industry signal / 愿景-only / peer-reviewed prior work）。
6. **curriculum-as-asset 类比**：基础模型下一代形态（FM.next） 把 curriculum 视为可版本化、可观测、可迭代的知识资产——这与 Paper2 把"维度模式"视为可维护资产的论点高度同构。

#### 6.4 绝不能迁移的领域结论

1. ❌ "SE 3.0 已被验证为可行" —— 作者明确说 "only time will tell"（§5 行 853）。
2. ❌ "队友下一代形态（Teammate.next） / 集成开发环境下一代形态（IDE.next） / 编译器下一代形态（Compiler.next） / 运行时下一代形态（Runtime.next） / 基础模型下一代形态（FM.next） 5 层 stack 是 AI-native SE 的标准划分" —— 是单一作者团队的 愿景，未被独立社区共识。
3. ❌ "RAR / 编译器下一代形态（Compiler.next） prototype 数据可作为综述证据" —— companion paper、self-citation、prototype 规模。
4. ❌ "TRAE 75.2% SWE-Bench Verified 表示 autonomous SE 已实用" —— 作者本人在 §2.3 已显式降级。
5. ❌ "117 条参考文献是 SLR 分母" —— 没有检索 / 纳排协议。

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
