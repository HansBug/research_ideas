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
| 论文类型 | vision / roadmap / taxonomy-boundary anchor；不是 SLR、SMS、tertiary study 或 guideline |
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

### 2.4 Teammate.next

Teammate.next 是从 static / impersonal coding assistant 到 self-evolving personalized mentor 的转变。作者要求 AI teammate 具备对话智能、社交智能和 personification，能够长期学习项目约束、人类偏好、常见错误和交互历史；它不仅执行任务，还帮助开发者澄清意图、解释设计取舍、教授模式与框架，成为 one-on-one programming mentor。

可迁移点：该层为 Paper2 的“研究者 / agent 角色边界”提供一个反面提醒：即使强调 AI teammate，也必须区分“提出建议 / 候选”与“最终裁决 / 责任归属”。

证据锚点：`paper_content.txt` §3.2，Page 7--8。

### 2.5 IDE.next

IDE.next 是 intent-centric IDE。它以 human-AI alignment of intents 为入口，而不是以编辑源代码为中心。输入可以是非形式化功能描述、伪代码、UI sketch、示例数据等；AI 在意图对齐后驱动代码创建循环。代码默认被隐藏，只有在 low-level debugging mode 下才暴露给人类。论文还强调 conversations 将成为核心资产，需要版本控制和管理；这里的 code 被扩展为传统代码、机器学习模型、prompt 甚至数据。

可迁移点：对 Paper2 很重要的是“conversation / decision trail as asset”这一点，可类比为系统综述中的模式批准、证据抽取、质疑和裁决日志必须成为一等制品，而不能只留下最终综述文本。

证据锚点：`paper_content.txt` §3.3，Page 8。

### 2.6 Compiler.next

Compiler.next 被定义为把 intents 合成为 runnable software 的搜索式编译器。其核心机制包括：

1. 通过 code mutations 与 self-reflection 迭代开发解决方案；
2. 在 accuracy、latency、cost 等目标之间做 multi-objective optimization；
3. 使用 goal-tracking 机制把 intents 翻译为 tests，并在需求变化时适配测试，避免从现有代码反推测试的 AI4SE 陷阱；
4. 作者引用另一篇 Compiler.next work，称其 prototype 包含 architecture explorers、prompt rewriters、search optimizers、observability、semantic caching 与 distributed execution，并在 HumanEval-Plus 上提供初步 feasibility evidence。

可迁移点：对 Paper2 可迁移的是“goal / intent -> test / evidence obligation”的方向，即研究问题和综述元模型应下推为可检查字段与证据要求，而不是从生成文本反推结构。

证据锚点：`paper_content.txt` §3.4，Page 8--9。

### 2.7 Runtime.next

Runtime.next 面向 FMware 和 compound AI systems。作者认为未来许多软件系统会成为 FMware 或包含 FMware 模块，而 FMware 往往处于 data flywheel 驱动的持续演化状态，因此需要新的运行时。Runtime.next 的三项性质是：

1. **SLA-aware**：针对实时、批处理、内存密集等不同 SLA 要求进行 priority-based routing、observability、resource provisioning 和 cluster management；作者引用 companion work，称 DAG workflow、per-task slack、profiler、resource provisioner、router、cluster manager 在真实部署场景中降低 SLA violations 并改善硬件利用率。
2. **Uni-clusters**：统一训练、微调、服务和 agent self-evolution 等 FM-related activities，降低多套基础设施成本并提升资源使用效率。
3. **Edge-computing extension**：把简单请求路由到本地小模型，降低成本和延迟；如何路由被列为 OQ4。

可迁移点：Runtime.next 对 Paper2 的直接技术迁移有限，但其“运行时 observability + SLA / 成本 / latency 约束”的叙事可提醒 Paper2 过程证据应保留成本、耗时、失败和可复核性指标。

证据锚点：`paper_content.txt` §3.5，Page 9--11。

### 2.8 FM.next

FM.next 是 knowledge-driven efficient FM。作者主张通过 curriculum engineering 系统设计、维护和持续改进包含高质量领域知识的 curriculum，并用 synthetic data 扩展具体示例。SE curriculum 可借鉴 SWEBOK，覆盖 requirements reasoning、architecture design、implementation、testing、debugging、maintenance 等全生命周期能力。Curriculum 被视为可审查、可重组、可扩展、可版本化的知识资产，甚至可能比模型本身更接近 intellectual property。

本节还给出 curriculum 设计 recipe：定义目标与范围、识别 domain / subdomain、组织 hierarchical taxonomy、在叶节点放 examples / templates / evaluation rules、用 teacher FM 生成合成数据、进行 consistency testing、pilot testing、community contributions，并用 observability data / data flywheel 迭代修订。

可迁移点：这是与 Paper2 最贴近的一层。Paper2 的维度模式可被类比为 review-specific curriculum / schema：需要字段树、取值空间、例子、证据规则、缺失语义、版本、回填和观测数据驱动的修订；但不能把该文对 FM training 的设想直接等同于系统综述方法证据。

证据锚点：`paper_content.txt` §3.6，Page 11--13。

### 2.9 挑战路线图

论文 §4 把挑战统一组织为：Description、Affects、Open question、Our vision。这是本篇对 Paper2 最有迁移价值的报告结构。五组主要挑战如下：

| 挑战 | 影响组件 | Open question | Our vision 摘要 |
|---|---|---|---|
| Speeding up human-AI alignment | IDE.next, Teammate.next | OQ1：如何平衡澄清问题过多与过少？ | AI teammate 需要发展 sticky but adjustable 的 theory of mind，并提供 confidence / feedback 等 mutual ToM signal；需求工程活动仍关键。 |
| Improving efficiency of code synthesis | Compiler.next, Teammate.next | OQ2：如何提高 synthesis efficiency 且保持 / 提高 accuracy？ | 借鉴 SBSE，复用本地和 crowdsourced search data、semantic caching、self-reflection、历史启发式与用户个性化。 |
| Improving runtime performance | Runtime.next | OQ3：如何超过 Ray Serve 等 serving frameworks？OQ4：edge-extension routing 最佳算法是什么？ | 把 FMware workflow 编译为保留 intent 的 declarative graph；边缘路由应支持 continual learning 和 self-evolving，减少云端大模型请求。 |
| Improving FM understanding of code and SE | Compiler.next, Teammate.next | OQ5：如何让 FM 理解代码以及更广义 SE 原则？ | 引入 execution logic、变量状态、call stack、symbolic execution、data flow、SE curriculum 和模型内部表征研究。 |
| Eliminating prompt engineering | AI teammate 与 stack 中其他 FMware 层 | OQ6：如何避免人类做 prompt engineering？ | 让 AI 负责 prompt construction；结合 model training、Compiler.next、feedback-driven prompt examples、template database 和 question calibration。 |

§4.6 进一步列出 OQ7--OQ14，覆盖 SE 3.0 时代“好软件工程师”定义、教育、编程语言、IDE UI、benchmark、AI teammate IP 归属、就业影响、开放创新、accessibility / equity / fairness 等议题。

证据锚点：`paper_content.txt` §4.1--§4.6，Page 13--19。

### 2.10 证据 / 引用性质

这篇文章的证据构成是混合型，而不是系统综述证据链：

1. **叙事性论证**：以 SE 1.0 / 2.0 / 3.0 历史分期和技术栈迁移组织主线。
2. **快速变化工具 / 模型例子**：列举 GitHub Copilot、Claude Code、Codex CLI、Gemini Code Assist、Amazon Q Developer、Tabnine、Cline、Aider、Devin、SWE-agent、OpenHands、TRAE、Lovable、Replit、Bolt.new、Vercel v0 等；这些事实若进入论文正文必须另行按官方来源或固定快照核验。
3. **既有研究引用**：引用 productivity、AI coding assistants 接受率、prompt fragility、ToM、curriculum learning、SBSE、continual learning、code understanding 等相关研究，用于支撑局部风险或技术方向。
4. **作者组 companion works / under-review works**：Compiler.next、Runtime.next、FMware、conversational development environments、RAR、Watson / cognitive observability 等被用于支撑愿景的可行性线索，但存在作者自引用和未完全独立复现的风险。
5. **工业经验与社区讨论**：客户 / 内部团队 / OPEA / workshop / summit 被作为愿景来源，但没有可复核访谈 protocol、样本分布、编码过程或原始证据。

因此，本篇可以提供 roadmap/challenge 字段设计灵感，但不能作为“AI-native SE 已被系统证实”的证据。

### 2.11 局限

1. **非系统综述**：没有系统检索和纳排协议，不支持领域覆盖率、研究分布或统计性 finding。
2. **愿景强于证据**：核心贡献是 vision 和 roadmap，许多组件仍处于概念、prototype、companion work 或 open question 状态。
3. **自引用 / 生态偏置**：技术栈中的 Compiler.next、Runtime.next、FM.next、FMware、OPEA 等与作者团队研究和产业合作密切相关，外部独立证据有限。
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
| report structure pattern | 结构为 Introduction → critical analysis of current era → future vision and technology stack → challenges / open questions → conclusion；§4 每个挑战使用 Description / Affects / Open question / Our vision 模板。 | `paper_content.txt` 目录性 headings；§1--§5。 | 高度可迁移为 roadmap/challenge 文献的 review 模板，也可用于 Paper2 的 candidate finding / roadmap pattern。 | 不代表 SLR/SMS 报告结构；不能替代 Method / Results / Threats 的系统综述结构。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本篇可贡献的模式先验 | 可用方式 | 禁止升级 |
|---|---|---|---|
| A1-M0 主题 / 研究问题 / 范围 / 综述元模型设定 | 提供 AI-native SE / agentic SE 的边界词：SE 2.0、SE 3.0、AI-assisted、AI-native、intent-centric、conversation-oriented、FMware、AI teammate。 | 可作为未来 pilot topic 或相关工作背景的词表；帮助定义“AI-native SE roadmap 文献”与“系统综述证据文献”的边界。 | 不得把该文当作 Paper2 的目标领域综述结果。 |
| A1-M1 脚手架挖掘 / 种子探测 | 提供 vision/roadmap 样本的结构先验：era transition、technology stack、component transition、challenge、OQ、our vision。 | 可进入 A1-M1 候选字段和 report-structure pattern；后续需研究者采纳。 | 不能未经 G1 批准直接成为正式抽取 schema。 |
| A1-M2 维度模式准备与批准 | 暴露一组 roadmap 字段：problem source、affected component、open question、solution vision、evidence type、maturity、risk、follow-up obligation。 | 可作为 A3 schema 候选输入，尤其是 challenge_action_pattern 的扩展。 | 不能以单篇 vision paper 冻结字段取值空间。 |
| A1-M3 论文收集与概览 | 提醒概览卡必须记录 `review_type = vision / roadmap`、`not_SLR = true`、`evidence_level = narrative / prototype / industry_signal`。 | 可用于后续候选池分类和降级过滤。 | 不得与 SLR / SMS / tertiary 的全文文本级 evidence 混列为同等统计样本。 |
| A1-M4 字段级证据抽取与模式演化 | 适合抽取 section-level anchors，而非统计表；每个 claim 需要标注来自 §2 limitation、§3 stack vision 或 §4 OQ。 | 可练习“愿景 claim 的来源锚点 + 证据性质 + 快速漂移风险”字段。 | 不得把 citation density 或作者论述当作目标事实强证据。 |
| A1-M5 统计分析 | 本篇不能提供统计分析样本；最多作为“vision/roadmap 文献比例”统计中的一种类型。 | 若后续文库统计 review_type 分布，可计入 vision/roadmap 类型。 | 不能从单篇愿景文献推导领域趋势、频次或覆盖率。 |
| A1-M6 候选发现生成 | 可提供候选发现启发式：把 limitation -> stack component -> OQ -> roadmap action 连接起来；同时要求主张强度降级。 | 可启发 Paper2 的候选发现台账字段，例如 `finding_type = challenge / roadmap / open_question`。 | 候选发现不得跳过反向证据和研究者裁决成为最终领域发现。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

以下字段树只作为 A1-M1/A1-M2 候选，不是正式 schema：

```text
roadmap_item
├── bibliographic_context
│   ├── paper_type: vision / roadmap / taxonomy / SLR / SMS / tertiary / guideline
│   ├── evidence_level: narrative / systematic / prototype / benchmark / industry_signal / mixed
│   └── temporal_stability: stable_concept / fast_drifting_tool / fast_drifting_model / fast_drifting_benchmark
├── problem_framing
│   ├── current_era_or_baseline
│   ├── limitation_category
│   ├── affected_actor: human / AI / organization / runtime / ecosystem
│   └── failure_mode_or_pain_point
├── future_vision
│   ├── target_era_or_paradigm
│   ├── core_principle
│   ├── intended_actor_boundary
│   └── expected_benefit
├── technology_stack_component
│   ├── component_name
│   ├── from_state
│   ├── to_state
│   ├── required_capability
│   └── dependency_on_other_components
├── challenge
│   ├── challenge_title
│   ├── description
│   ├── affected_components
│   ├── open_question_id
│   ├── open_question_text
│   ├── proposed_vision_or_solution
│   ├── companion_evidence_or_reference
│   └── maturity: concept / prototype / empirical_initial / deployed_signal / open_question_only
├── evidence_and_risk
│   ├── evidence_anchor
│   ├── evidence_source_type
│   ├── independent_validation_status
│   ├── self_citation_or_author_ecosystem_risk
│   ├── missing_counterevidence
│   └── overclaim_guard
└── downstream_obligation
    ├── needs_official_fact_check
    ├── needs_pdf_figure_check
    ├── needs_systematic_review_evidence
    ├── needs_researcher_approval
    └── allowed_use: background / schema_candidate / candidate_finding / final_finding_forbidden
```

对本篇的最小实例化示例：

| 字段 | 示例值 |
|---|---|
| `paper_type` | vision / roadmap |
| `evidence_level` | mixed narrative：文献引用 + 作者经验 + companion prototypes + 工业 / 社区信号 |
| `problem_framing.limitation_category` | cognitive overload；inefficient model training；additive bias；autonomous SE benchmark limitation |
| `future_vision.core_principle` | intent-centric；conversation-oriented；AI-native；knowledge-driven |
| `technology_stack_component.component_name` | Teammate.next；IDE.next；Compiler.next；Runtime.next；FM.next |
| `challenge.open_question_id` | OQ1--OQ14 |
| `evidence_and_risk.overclaim_guard` | 不得写成 SLR evidence；不得写成 AI-native SE 已被系统验证 |

## 6. 对 Paper2 story / method 的启发

1. **roadmap/challenge 是可抽取对象，但必须降级**：本篇作为一个样例表明，vision / roadmap 文献可以启发 challenge_action_pattern 候选结构；但 Paper2 必须记录其证据等级，不能把它和 SLR / SMS 的统计 finding 混用。
2. **字段树应保留“证据性质”而不只保留“结论文本”**：同一句 roadmap claim 可能来自作者观点、companion prototype、工业经验、benchmark 或已发表研究；这些来源的可审计性不同。
3. **技术栈图可启发维度模式版本化**：SE 3.0 stack 把 Teammate / IDE / Compiler / Runtime / FM 分层，类似 Paper2 把综述元模型、维度模式、字段证据、统计分析、候选发现和裁决分层；每层都应有职责边界。
4. **conversation as asset 支持过程证据叙事**：IDE.next 强调 conversations version-controlled；Paper2 可借此强化“模式批准、质疑、裁决、回填日志是研究制品”的论点。
5. **curriculum engineering 可类比维度模式工程**：FM.next 把 curriculum 作为可维护知识资产；Paper2 可把维度模式视为面向单个综述任务的可维护知识资产，包含 taxonomy、examples、evaluation rules、missing semantics 与 observability-driven revision。
6. **goal tracking 启发证据义务**：Compiler.next 中 intents -> tests 的方向可迁移为 Paper2 中 research questions / review meta-model -> extraction fields / evidence requirements 的方向。
7. **OQ 模板可用于候选发现台账**：Description / Affects / Open question / Our vision 是较好的 roadmap report structure；Paper2 的 candidate finding ledger 可加入 affected_dimension、evidence_strength、open_issue、proposed_action 字段。

## 7. 对 Paper2 的风险

1. **过度升级风险**：最大风险是把该文的愿景性判断写成系统综述发现。必须在任何引用处标明“vision/roadmap，不是 SLR/SMS evidence”。
2. **快速事实漂移风险**：模型版本、工具、benchmark 排名、commercial platform 变化快；若用于背景，必须在正式写作前重新核验官方来源和日期。
3. **自引用 / 生态闭环风险**：多个关键支撑来自作者团队 companion works，可能放大同一研究生态的观点。Paper2 若抽取 roadmap evidence，应记录 independent validation status。
4. **反向证据不足**：论文欢迎 opposing views，但自身没有系统呈现反对观点、失败案例或替代路线。
5. **治理与安全关键不足**：OQ11--OQ14 承认 IP、就业、公平性等开放问题；对形式化验证、安全关键控制系统、合规认证没有深入路线，不能直接支撑 project_1 / 博士主线的形式化方法论断。
6. **方法可执行性不等于工具可用性**：Compiler.next / Runtime.next 的 prototype evidence 只是局部可行性线索，不证明完整 SE 3.0 stack 已可运行或可泛化。

## 历史草稿（已迁移，不作事实真源）：旧第 8 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

- 本篇触发一个明确字段需求：`roadmap_challenge_pattern` 或扩展现有 `challenge_action_pattern`，至少记录 `paper_type`、`evidence_level`、`affected_component`、`open_question`、`solution_vision`、`maturity`、`overclaim_guard`。
- 由于本轮任务只允许编辑本 `review.md`，不回修 [../../patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md) 或 [../../SUMMARY.md](../../SUMMARY.md)。后续 A2/A3 若决定采纳 vision/roadmap 样本，应再执行 schema 回修闭环。
- 对 SLR/SMS 六类 pattern 而言，本篇的 RQ、finding、validity/threat 均只能写为“不适用 / 降级适用”，不能以缺失字段方式误判为低质量 SLR。

## 9. 待复核

1. 需要人工打开 `paper.pdf` 核对 Fig. 1--7 的版式、组件命名和图中箭头 / 标签；本轮仅依据 `paper_content.txt` 文本抽取。
2. 若正式写入论文或投稿材料，仍建议在提交前按当轮 CCF 官方目录复核；本轮沿用本仓库 ccf_venues 缓存记录 TOSEM 为 A 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
3. 若引用模型、工具、benchmark 或 commercial platform 示例，需要在正式写作前按官方来源记录核验日期，避免使用已漂移事实。
4. 若把 Compiler.next、Runtime.next、FMware、RAR、Conversational Development Environments 等 companion works 作为证据，需要分别读取原文，区分已发表、预印本、under review、prototype 和真实部署证据。
5. 若后续把该文纳入 Paper2 的脚手架样本，应在总账中显式标为 `vision / roadmap`，并把“不得作为系统综述证据”写入候选池备注。

## 维度树复原

### 一句话结论

本文的维度树主类型为“roadmap / challenge 树”，辅助类型为“理论 / 元模型概念树”。不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 [clm-ai-native-se-roadmap-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-ai-native-se-roadmap-root] | Towards AI-Native Software Engineering (SE 3.0) 的研究目标 / RQ / 贡献声明 | roadmap action / guideline item / schema seed | [dim-ai-native-se-roadmap-b1] SE 3.0 愿景对象；[dim-ai-native-se-roadmap-b2] 技术栈层级；[dim-ai-native-se-roadmap-b3] AI-native challenge；[dim-ai-native-se-roadmap-b4] action roadmap；[dim-ai-native-se-roadmap-b5] boundary risk | [ev-ai-native-se-roadmap-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-ai-native-se-roadmap-root] Towards AI-Native Software Engineering (SE 3.0)
├── [dim-ai-native-se-roadmap-b1] SE 3.0 愿景对象
│   └── [leaf-ai-native-se-roadmap-scope] 研究范围与单位对象
├── [dim-ai-native-se-roadmap-b2] 技术栈层级
│   └── [leaf-ai-native-se-roadmap-corpus] 语料与纳排链条
├── [dim-ai-native-se-roadmap-b3] AI-native challenge
│   └── [leaf-ai-native-se-roadmap-taxonomy] 主题与维度分类
├── [dim-ai-native-se-roadmap-b4] action roadmap
│   └── [leaf-ai-native-se-roadmap-method] 方法 / 技术 / 干预分类
└── [dim-ai-native-se-roadmap-b5] boundary risk
    └── [leaf-ai-native-se-roadmap-evidence] 评价、证据与复现资产
    └── [leaf-ai-native-se-roadmap-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-ai-native-se-roadmap-scope] | 研究范围与单位对象 | [dim-ai-native-se-roadmap-b1] | 定义 AI-native SE roadmap 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-scope] |
| [leaf-ai-native-se-roadmap-corpus] | 语料与纳排链条 | [dim-ai-native-se-roadmap-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-corpus] |
| [leaf-ai-native-se-roadmap-taxonomy] | 主题与维度分类 | [dim-ai-native-se-roadmap-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-taxonomy] |
| [leaf-ai-native-se-roadmap-method] | 方法 / 技术 / 干预分类 | [dim-ai-native-se-roadmap-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-method] |
| [leaf-ai-native-se-roadmap-evidence] | 评价、证据与复现资产 | [dim-ai-native-se-roadmap-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-evidence] |
| [leaf-ai-native-se-roadmap-finding] | 统计观察与候选发现 | [dim-ai-native-se-roadmap-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ai-native-se-roadmap-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-ai-native-se-roadmap-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否 | 识别可迁移的维度模式类型 | 不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 |
| [leaf-ai-native-se-roadmap-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | not_applicable | 否 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-ai-native-se-roadmap-finding] | 候选发现台账，不直接作为 final finding | discussion / conclusion / roadmap action | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-ai-native-se-roadmap-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | AI-native SE roadmap 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-ai-native-se-roadmap-transfer] |
| [leaf-ai-native-se-roadmap-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-ai-native-se-roadmap-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-ai-native-se-roadmap-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-ai-native-se-roadmap-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-ai-native-se-roadmap-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-ai-native-se-roadmap-001 | [ev-ai-native-se-roadmap-root] | [src-ai-native-se-roadmap-text], [src-ai-native-se-roadmap-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-ai-native-se-roadmap-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-ai-native-se-roadmap-002 | [ev-ai-native-se-roadmap-taxonomy] | [src-ai-native-se-roadmap-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-ai-native-se-roadmap-b1], [dim-ai-native-se-roadmap-b2], [dim-ai-native-se-roadmap-b3], [dim-ai-native-se-roadmap-b4], [dim-ai-native-se-roadmap-b5], [leaf-ai-native-se-roadmap-taxonomy], [leaf-ai-native-se-roadmap-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-ai-native-se-roadmap-003 | [ev-ai-native-se-roadmap-stat] | [src-ai-native-se-roadmap-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作 boundary / candidate seed，待 A2a 精确页码 / 表图核验后才能升级。 | author_claim | not_verified | [leaf-ai-native-se-roadmap-evidence], [leaf-ai-native-se-roadmap-finding] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
| EV-ai-native-se-roadmap-004 | [ev-ai-native-se-roadmap-risk] | [src-ai-native-se-roadmap-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-ai-native-se-roadmap-root], [leaf-ai-native-se-roadmap-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-ai-native-se-roadmap-tree-type] | A1DT-ai-native-se-roadmap-C01 | 本文的维度树主类型为“roadmap / challenge 树”，辅助类型为“理论 / 元模型概念树”。不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 [clm-ai-native-se-roadmap-tree-type] | tree_type | [dim-ai-native-se-roadmap-root] | EV-ai-native-se-roadmap-001, EV-ai-native-se-roadmap-004 | 树型判断仅限本文，不代表所有 AI-native SE roadmap 综述。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-scope] | A1DT-ai-native-se-roadmap-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-scope] | EV-ai-native-se-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-corpus] | A1DT-ai-native-se-roadmap-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-corpus] | EV-ai-native-se-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-taxonomy] | A1DT-ai-native-se-roadmap-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-taxonomy] | EV-ai-native-se-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-method] | A1DT-ai-native-se-roadmap-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-method] | EV-ai-native-se-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-evidence] | A1DT-ai-native-se-roadmap-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-evidence] | EV-ai-native-se-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-leaf-finding] | A1DT-ai-native-se-roadmap-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ai-native-se-roadmap-finding] | EV-ai-native-se-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-ai-native-se-roadmap-transfer] | A1DT-ai-native-se-roadmap-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-ai-native-se-roadmap-root] | EV-ai-native-se-roadmap-002, EV-ai-native-se-roadmap-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-ai-native-se-roadmap-finding-boundary] | A1DT-ai-native-se-roadmap-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-ai-native-se-roadmap-finding] | EV-ai-native-se-roadmap-003, EV-ai-native-se-roadmap-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-ai-native-se-roadmap-structure-check] | [dim-ai-native-se-roadmap-root], A1DT-ai-native-se-roadmap-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-ai-native-se-roadmap-visual-check] | EV-ai-native-se-roadmap-002, EV-ai-native-se-roadmap-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
