# The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study |
| 作者 | Amr Mohamed; Maram Assi; Mariam Guizani |
| 年份 / 正式发布日期 | 2026 / 2026-04-27 |
| DOI | https://doi.org/10.1145/3809494 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [TOSEM](https://dl.acm.org/journal/tosem)；开放全文来自 arXiv PDF |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | A |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 综述类型 | SLR + SMS；39 篇 peer-reviewed primary studies，时间范围 2014--2024 |
| SE 子领域 | LLM assistants / developer productivity / LLM4SE empirical studies |
| 阅读状态 | 已读 [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)；未回 PDF 逐页核对图表 |
| 证据等级 | 全文文本级；图表/表格精确版式与页码待人工原文核对 |
| artifacts | 原文声明所有制品公开于 Zenodo replication package：https://zenodo.org/records/18489222 |
| A1 角色 | 高相关、现代、CCF-A 的 SLR+SMS 样本；用于学习如何把 `landscape -> method -> benefit/risk -> productivity dimensions -> implications/threats` 组织为 RQ 和结果表。 |
| 是否目标领域证据池 | 否。本文只能作为 Paper2 的 scaffold / pattern prior，不能把其 LLM-assistant productivity findings 直接当成我们目标领域发现。 |
| 核心可借鉴点 | RQ0--RQ3 层级清晰：先给研究景观，再给方法与工具，再给 benefit/risk，最后用外部框架映射 productivity dimensions；每个 RQ 末尾都有短 summary，把分布数字、主导类别、争议点和下一步 gap 压成可引用结论。 |
| 主要风险 | 其领域结论受 2024 年爆发式文献和快速模型漂移影响；primary studies 多为 formative / lab / self-report，适合学习报告结构，但不适合作为强领域事实迁移。 |

## 2. 全文内容详读

### 2.1 背景与问题定位

本文的问题不是泛泛讨论 LLM 是否“有用”，而是把 **LLM-assistants 对软件开发者生产力的影响**定义为一个需要系统综合的证据问题。背景部分先说明 LLM-assistants 已覆盖代码生成、翻译、调试、维护、文档和设计等任务，并把这种使用方式放到 AI pair programming 的实践背景中。随后，作者强调 developer productivity 本身是多维构念，不能只靠 LOC、velocity 或 task completion time 这类单指标解释；它同时包含效率、质量、满意度、认知负荷、协作和组织因素。

这篇文章的叙事结构很适合作为 Paper2 scaffold：先承认工具生态变化很快，再说明既有研究碎片化，最后引入一个外部概念框架（SPACE）作为综合镜头。它不是直接用 “LLM improves productivity” 作主张，而是问：已有 peer-reviewed empirical studies 是怎么研究这个问题、报告了哪些 benefit/risk、又覆盖了哪些 productivity dimensions。

### 2.2 RQ0--RQ3 的组织逻辑

| RQ | 原文问题焦点 | 实际承载的综述层级 | 对 Paper2 的结构启发 |
|---|---|---|---|
| RQ0 | 研究 LLM-assistants 与 developer productivity 的 peer-reviewed studies 有什么特征？ | landscape：年份、venue、作者分布、工具分布。 | 可迁移为“领域景观 RQ”：先给语料时间线、来源、研究社区和对象分布，不急着下领域结论。 |
| RQ1 | 这些研究使用了哪些 methodological strategies、procedures、instruments？ | method：研究策略、实验/调查/访谈等 procedures、评价工具、指标、数据来源。 | 可迁移为“方法与评价实践 RQ”：把研究设计本身作为综述对象，方便后续识别证据强弱和可比性。 |
| RQ2 | LLM-assistants 对 developer productivity 有什么影响？ | benefit/risk synthesis：主题分析，把 effects 拆成正负两组主题。 | 可迁移为“finding ledger RQ”：不要只列 benefit，还要同时组织 risk 和 contested finding。 |
| RQ3 | 哪些 productivity dimensions 被研究，如何映射到 SPACE？ | dimension mapping：用外部框架整合测量维度和覆盖缺口。 | 可迁移为“维度覆盖 RQ”：用研究者批准的元模型或框架映射字段，统计覆盖和缺口。 |

整体上，RQ0 给“景观”，RQ1 给“研究方式”，RQ2 给“结果主题”，RQ3 给“概念维度”。这使得论文避免把所有发现堆在一个结果章节里，也便于每个 RQ 对应一组表格 / 图 / summary。

### 2.3 方法：pre-review mapping、控制论文与检索策略

作者声称遵循 Kitchenham & Charters 的 SE SLR 指南。方法章节先做 pre-review mapping：定义 RQ、纳排标准、控制论文和搜索式迭代。控制论文的作用非常明确：作者先人工检索、标题摘要筛选、做一轮 backward / forward snowballing，得到 17 篇 control papers，再用它们验证搜索式是否能召回已知相关论文。

检索覆盖六个数据库：ACM、IEEE Xplore、ScienceDirect、Web of Science、Scopus、Springer。最终初始检索量为 9,756，其中 ACM 4,044、IEEE 491、ScienceDirect 3,734、Web of Science 271、Scopus 836、Springer 380。搜索式由三段组成：AI/LLM 技术词、developer/SE actor 词、productivity 概念词；IEEE、Web of Science 和 Scopus 使用 proximity operator 提高上下文相关性。作者还解释了 broad query 与 narrow query 的 trade-off：前者 false positives 多，后者可能漏文献，因此经过五轮 query iterations，并由全体作者开会达成最终搜索式。

对 Paper2 的启发是：检索策略不是只给字符串，还要说明字符串如何被控制论文校验、如何在 precision/recall 之间折中、哪些数据库因为语法不同需要调整。

### 2.4 检索、纳入 / 排除与筛选流程

纳入标准很短：研究 AI 或 LLMs 对 software developer productivity 的影响；英文；2014 年及以后发表且全文可访问。排除标准包括：不关注 SE 或不研究 productivity impact、只顺带提及而非研究主题、secondary studies / WIP / extended abstracts / posters / tool demos / editorials / grey literature / book / thesis / workshop 等不符合正式 peer review 口径的出版类型、少于 4 页、全文不可访问。

筛选流程的分母链条很完整：初始 9,756 条，去重 803 后剩 8,953 条做标题摘要筛选；标题摘要阶段排除 8,725 条，剩 228 条全文筛选；全文阶段排除 189 条；对入选研究做 backward / forward snowballing 额外加入 5 条；44 条进入质量评价；质量评价排除 5 条；最终纳入 39 条。作者使用 Rayyan 标注排除理由，并说明标题摘要筛选由第一作者完成、第二和第三作者验证 excluded papers，遇到不确定时保守进入全文阶段。

这里可迁移的是“分母链 + 排除原因 + 工具 + 人工验证角色”的组合。Paper2 若要做类 PRISMA 透明材料，可以学习这种粒度，但不能声称 PRISMA 合规，除非后续完整满足透明报告要求。

### 2.5 质量评价

质量评价采用 Lenarduzzi 等人的 empirical SE study QA 策略，包含 11 个 QA criteria：研究是否基于 research、目标是否清晰、上下文是否充分、研究设计是否适当、招募策略、控制组、数据收集、数据分析严谨性、研究者与参与者关系、finding 清晰性、研究/实践价值。每项按 0--4 的 Likert scale 打分，并使用 50% 平均分阈值排除低质量研究；最后 5 篇因质量评价被排除，39 篇进入最终综合。

对 Paper2 的重要启发：质量评价不是为了形式上打分，而是连接到“哪些 primary studies 可以进入结果综合”。如果我们后续使用 agent 抽取字段，quality / eligibility 必须成为字段证据表的一等字段，否则后续统计会混入低质量或不合格条目。

### 2.6 数据抽取与综合

数据抽取与综合持续三个月。作者先做初始 thematic analysis，抽取 study goals、tools、empirical strategy/design、tasks、settings、key results，并为每篇 study 写 descriptive summary；然后做多轮 targeted thematic analysis：一轮针对 RQ1 的方法细节，一轮针对 RQ2 的 benefits/risks，一轮针对 RQ3 的 SPACE mapping。主题合并后，第一作者和最后一位作者共同回查 citation against original text，以保证 traceability。

这对 Paper2 非常关键：它把“单篇摘要 -> 多轮主题编码 -> RQ-specific synthesis -> citation cross-check”写成了可审计流程。我们的方法可以把这一步转译成字段级内容证据表、模式修订日志和候选发现台账，而不是只让 LLM 直接生成综合段落。

### 2.7 RQ0 主要结果：landscape

RQ0 的结果包含四个景观维度：发表年份、作者分布、venue 分布、LLM tools 分布。时间上，2014--2022 只有 4 篇，ChatGPT 发布后研究急剧增长，2024 年占 77%。作者层面，154 位作者中 147 位只有 1 篇，少数作者有 2 篇或更多，说明该方向仍在形成中。Venue 层面，46% 来自 Software Engineering / Computer Science venues，包括 PACMSE、TOSEM、ICSE、FSE、PLDI、ASE、EASE 等；18% 来自 HCI venues，包括 CHI、IUI、CSCW、TOCHI；其余分散到 information systems、human-aspects、AI for software、SE education 等。工具层面，ChatGPT 15 篇、GitHub Copilot 14 篇最常见，Tabnine、GPT-4、CodeWhisperer 各 3 篇，GPT-3.5 2 篇，Claude、Codex、Gemini 等只出现 1 篇。

RQ0 的写法不是“背景介绍”，而是把语料本身当作对象，说明领域何时爆发、由哪些社区贡献、研究了哪些工具。这种 landscape layer 很适合 Paper2 的综述之综述脚手架：先把 corpus 的可解释边界讲清楚，再谈后续 finding。

### 2.8 RQ1 主要结果：method / procedure / instrument

RQ1 先用 Stol & Fitzgerald 的 empirical SE strategy taxonomy 分类研究策略。Laboratory experiment 最多，15/39，占 38%；field study 9/39，占 23%；sample study 6/39，占 15%；experimental simulation 5/39，占 13%；field experiment 和 judgment study 各 2/39，占 5%。这组结果支撑了作者后续 threat：当前证据很多来自 controlled / exploratory setting，生态效度有限。

随后作者用更细的 procedure taxonomy 分类研究方法：survey 32/39，占 82%；user experiment 16/39，占 41%；case study 12/39，占 31%；interview 10/39，占 26%；concept implementation 4/39，占 10%。69% 的研究采用 mixed-methods，常见组合是 user experiment + survey，以同时捕捉 measured performance 和 self-reported perception。研究目标上，59% 是 formative，41% 是 summative；数据分析上，67% 同时使用 quantitative + qualitative，21% 仅 qualitative，13% 仅 quantitative。

评价工具与指标部分，作者把 data source / instrument origin 组织成表：self-reported methods 很多由作者自设；validated instruments 包括 NASA-TLX、SPACE-based surveys、TAM、self-efficacy questionnaire、AAR/AI、emotion affect questionnaire；behavioral/performance metrics 包括 task completion/correctness、suggestion acceptance rate、interaction logs、time to completion、code quality metrics、productivity gain；还有 TCQ、RBV 等 econometric frameworks。关键结果包括：time to completion 是最常用 performance metric，12/39，占 31%；acceptance rate 常见但不宜单独优化；cognitive load 用 NASA-TLX 的 6 篇研究结果不一致，有改善、无差异和 frustration 增加等不同方向。

RQ1 的价值在于把“研究怎么做”拆成 strategy、procedure、objective、analysis type、instrument、metric，而不是只说“多数为实验研究”。这可直接迁移为 Paper2 字段树。

### 2.9 RQ2 主要结果：benefits 与 risks

RQ2 使用 thematic analysis 组织 benefits 和 risks，并用 radar plot + summary tables 呈现。Benefits 分为八类：

1. Accelerate software development：self-report 与部分 quantitative studies 都报告开发加速，案例中出现 effort 大幅下降、controlled experiments 中有 21%--45% 的效率增益。
2. Minimize online code search：LLM-assistants 减少 Stack Overflow / Google / Bing 等传统搜索，帮助保持 flow，但不同工具和任务结果有差异。
3. Automate trivial / repetitive tasks：生成 boilerplate、减少 keystrokes、支持 test generation 和 CI/CD automation。
4. Support knowledge acquisition：作为 expert consult、学习新框架、降低新任务进入门槛。
5. Support code-adjacent tasks：ideation、requirements specification、documentation、QA、emails、meeting minutes、onboarding、issue documentation。
6. Reduce task initiation overhead：生成初始 scaffolding、proof-of-concept、结构化想法，帮助开发者从空白开始。
7. Improve code quality：部分研究报告 code smells、defects、coverage、translation error rate 等改善。
8. Support debugging / troubleshooting：解释错误、建议 fix、帮助 early defect detection。

Risks 分为五类：

1. Fail to meet requirements：输出不满足功能/非功能需求、缺上下文、过度输出、正确率有限。
2. Promote over-reliance and cognitive offloading：新手和学生可能削弱 critical thinking，专业开发者也可能 automation complacency。
3. Limit code quality：错误代码、漏洞、幻觉、上下文不足、项目规范不一致；部分研究发现 quality 不改善甚至更差。
4. Disrupt the flow：不想要的建议、界面切换、verbose answers、多工具竞争、验证和 prompt crafting 时间占比高。
5. Reduce team collaboration：开发者转向 chatbot 而不是同事，传统 help channel 变少，organic conversation 和 synergy 受损。

最值得借鉴的是 code quality 的处理方式：它既出现在 benefits，也出现在 risks。作者没有强行调和为单向结论，而是指出不同 task、context、metric 和 study design 导致结果矛盾。这种“contested theme”写法对 Paper2 很重要：统计观察或频次不能直接升级为 finding，必须记录反向证据和主张强度。

### 2.10 RQ3 主要结果：SPACE 生产力维度

RQ3 以 SPACE 作为 productivity lens：Satisfaction and well-being、Performance、Activity、Communication and collaboration、Efficiency and flow。作者选择 SPACE 的理由是它能同时覆盖 objective outcomes（如 quality、activity、efficiency）与 human-centered constructs（如 satisfaction、collaboration），并允许根据 empirical context 调整 sub-dimensions。

作者进一步把 SPACE 细化为 sub-dimensions：

- Satisfaction：developer experience、self-efficacy、trust、cognitive load；well-being 没有 primary study 直接研究。
- Performance：quality、impact。
- Activity：action/task counts，例如 acceptance rate、suggestions shown、tasks completed。
- Communication：human-LLM collaboration、human-human collaboration；其中 human-human collaboration 只有很少研究覆盖。
- Efficiency：temporal efficiency、automation、interruptions and flow。

主要覆盖结果：90% 的研究至少覆盖两个 SPACE dimensions，44% 覆盖三个或更多，只有 15% 覆盖四个或更多；Satisfaction 最常见，30/39，占 77%；Performance 25/39，占 64%；Efficiency 23/39，占 59%；Activity 12/39，占 31%；Communication 10/39，占 26%。最常见组合是 Satisfaction-Performance-Efficiency。RQ3 因此给出一个很清楚的 gap：已有研究已经从单指标转向多维，但仍很少完整覆盖 communication、activity、well-being、team dynamics 等维度。

### 2.11 Discussion / implications

Discussion 先用 McLuhan’s Tetrad 做 in-depth synthesis，把 SPACE 的 measurement lens 拓展为 socio-technical interpretation lens：

- Enhance：LLM-assistants 强化开发速度、task initiation、knowledge acquisition、debugging/troubleshooting，尤其适合 boilerplate、syntax recall、initial scaffolding、exploratory prototyping。
- Reverse：过度信任会导致 cognitive offloading、automation complacency、弱化 reflective practice、影响 code quality 和 collaboration。
- Obsolesce：传统 online search、Q&A platform、独立验证习惯可能被削弱；作者建议把 LLM 当 complement 而非 replacement。
- Retrieve：文档、requirements elicitation、legacy modernization 等过去常被 deprioritized 的实践可能被重新带回 workflow。

随后作者面向 practitioners 给出五类建议：校准信任；从 coder 转向 reviewer，重视 prompt、evaluation、refinement；调整个人与团队 workflow，保留 pair programming、code review、architecture discussion；组织层面建立 adoption strategy、QA 和高风险模块审查；专业伦理层面要求 disclosure、accountability、traceability、bias testing。

面向 researchers，作者提出三个方向：使用 shared evaluation frameworks 和 validated instruments，开展 longitudinal / field / team-based studies；继续推进 multidimensional evaluation，补 Communication、Collaboration、well-being、team dynamics；系统报告 confounding variables，包括 developer expertise、task complexity、domain/organizational context，并做 replication。

### 2.12 Threats to validity

Threats 分两组。

第一组是 review methodology threats：

- Study selection bias：纳排标准可能漏掉相关研究，特别是排除 short paper、non-peer-reviewed 和不可访问全文；作者通过共同制定 criteria、控制论文验证搜索式、snowballing 缓解。
- Human-centered study identification 难：LLM4SE 领域大量“performance/efficiency”其实指模型性能，不是 developer productivity；作者通过 control papers 和 query refinement 缓解。
- Bias and repeatability：RQ 开放，selection/extraction 有主观性；初筛和抽取由第一作者主导，但其余作者参与 protocol design、selection validation，并进行 9 个月 weekly meetings。
- Classification rigor：SPACE 原本不是为 human-LLM collaboration 设计，映射 sub-dimensions 有解释性判断；作者用既有定义并通过团队讨论缓解。

第二组是 primary evidence base limitations：

- Formative and controlled studies 比例高：59% formative、38% lab experiments，内部效度较好但生态效度有限。
- Methodological diversity：code quality、cognitive load 等指标多样，阻碍跨研究比较，但也提供多源 triangulation。
- Temporal relevance：GenAI 变化快，检索和抽取截至 2024 年底，且 77% 纳入研究集中在 2024；作者建议透明协议和周期性更新。

### 2.13 Artifacts / replication package

摘要、贡献列表、方法和结论均声明公开 replication package，Zenodo 记录包括 study data、selection decisions、exclusion rationales，以及 supplemental appendix 中的 control papers、query refinement、QA scores 等。对 Paper2 来说，这一点不是附属材料，而是现代 SLR 的审计性核心：研究发现之外，过程分母、筛选理由、质量分数、字段表和排除台账都要能被复核。

## 3. 每个 RQ 末尾 Summary 的写法

| RQ summary | 写作结构 | 具体写法观察 | 可迁移模板 |
|---|---|---|---|
| RQ0 Summary | 时间爆发点 + 作者集中度/分散度 + venue 社区分布 | 先给 ChatGPT 后 35/39、2024 年峰值这类时间判断，再给 147/154 作者单篇和 SE/CS、HCI venue 分布。 | “Most studies appear after X; authorship is fragmented/concentrated; venues cluster in A and B communities.” |
| RQ1 Summary | 主导研究策略 + 方法组合 + 核心指标 + caveat | 先报 lab experiment 38%、mixed-methods 69%，再报 time to completion 31%、acceptance rate caution、NASA-TLX cognitive load mixed。 | “The evidence base is methodologically dominated by A; B is common; C is the most used metric, but D should not be interpreted alone; contested construct E remains mixed.” |
| RQ2 Summary | mixed findings + top benefits + top risks + contested theme + future need | 明确 benefits 和 risks 并存；列 accelerated development / code search / trivial tasks；列 requirements failure / over-reliance / flow disruption；强调 code quality 同时改善和恶化。 | “Studies report both benefits and risks. The most frequent benefits are ...; key risks are ...; X remains contested, so future work must identify boundary conditions and safeguards.” |
| RQ3 Summary | 框架 lens + multidimensional adoption + coverage gap | 先声明 SPACE 框架；再给 90% 多维、15% 四维以上；最后排序 S/P/E 最常见，A/C 最少。 | “Using framework F, most studies cover multiple dimensions, but few cover the full space; dimensions A/B/C dominate, while D/E remain underexplored.” |

这四个 summary 都不是普通段落总结，而是“结果压缩器”：每段都含 2--4 个可复核数字、一个主导模式、一个限制或 gap。Paper2 后续写 results 时应学习这种 summary style，但要把数字绑定到字段证据表和统计分析表，避免 LLM 直接写成无来源概括。

## 4. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 四层 RQ：RQ0 landscape、RQ1 methodology/instruments、RQ2 impact benefit/risk、RQ3 dimension/framework mapping。 | `paper_content.txt` §3 RQ 列表；§4--§7 各 RQ 结果；各 RQ summary。 | 高度可迁移为 Paper2 的 RQ scaffold：先语料景观，再方法实践，再 finding synthesis，再维度覆盖。 | 具体主题是 LLM-assistants productivity，不能迁移为我们目标领域 finding。 |
| dimension pattern | 维度树包含 publication year、venue focus、authors、tools、strategy、procedure、objective、analysis type、instrument、metric、benefit、risk、SPACE dimension/sub-dimension、recommendation、threat。 | RQ0 表 3/4；RQ1 表 5--7；RQ2 表 8/9；RQ3 表 10/11。 | 可迁移为 A2a/A3 字段树种子，尤其是“框架维度 + emergent sub-dimensions”的做法。 | SPACE 是 productivity framework；不能直接替代 Paper2 的综述元模型，除非目标主题确实是 productivity。 |
| finding pattern | 从统计分布生成 findings，但同时保留 contested findings 和 boundary conditions；code quality 被明确写成 benefit/risk 双重主题。 | RQ2 §6.1--§6.2；RQ2 summary；Discussion research gaps。 | 可迁移为候选发现台账：每个 candidate finding 应包含支持证据、反向证据、适用上下文、主张强度。 | 不能把“LLM improves productivity”等主题结论搬到我们的目标领域。 |
| evidence presentation pattern | 使用 PRISMA-style flow、数据库检索分母、QA criteria 表、strategy/procedure/instrument 表、benefit/risk summary 表、SPACE mapping 表、quality metrics 表、framework diagram。 | Fig. 1；Table 1--11；Fig. 2--9；Zenodo package。 | 可迁移为 Paper2 审计制品链：分母链、排除理由、字段表、质量表、主题表、维度映射表、复现包。 | 图表精确页码和最终 ACM 版格式待 PDF/ACM 核验；当前只读文本提取版。 |
| validity / threat pattern | Threats 同时覆盖 review process 与 primary evidence base：selection/search bias、repeatability、classification rigor、formative/lab evidence、method diversity、temporal relevance。 | `paper_content.txt` §9.1--§9.2。 | 可迁移为 Paper2 risk register：区分“我们方法导致的威胁”和“语料/primary evidence 本身的威胁”。 | 其 mitigation 建立在人工 review 团队上；Paper2 若引入 agent，需要额外加入 prompt/model drift、字段错误、证据断链、human gate fatigue 等威胁。 |
| report structure pattern | Introduction/Background/Method 后，结果按 RQ0--RQ3 独立成章，每章内部先分类/表格，再解释，再 summary；Discussion 先跨 RQ 综合，再给 practitioners/researchers recommendations，最后 threats/conclusion。 | `paper_content.txt` §1--§10。 | 高度可迁移为现代 SLR/SMS 报告模板，尤其是“RQ-by-RQ results + end-of-RQ summary + discussion lens”。 | Paper2 是方法论文，不应完全照搬领域 SLR 的章节比例；需要把方法对象、审计制品和评价单独突出。 |

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本文提供的 scaffold prior | 对后续方法设计的意义 |
|---|---|---|
| A1-M0 主题与综述元模型设定 | 明确把主题拆为对象（LLM-assistants）、影响对象（developer productivity）、证据对象（peer-reviewed empirical studies）、解释框架（SPACE）。 | 说明 A1-M0 不只是写题目，而要定义研究对象、目标构念、证据范围和解释框架。 |
| A1-M1 脚手架挖掘与种子探测 | 使用既有 SLR guideline、control papers 和 pre-review mapping 先测试 RQ/纳排/搜索式。 | 支持 Paper2 的“脚手架 + 种子探测”主线：用少量高相关样本压力测试模式，不直接冻结完整 schema。 |
| A1-M2 维度模式批准 | RQ1/RQ3 的字段体系显示 schema 可以由外部 taxonomy（Stol & Fitzgerald、Glass/Vessey/Ramesh、SPACE）与 emergent sub-dimensions 共同构成。 | 维度模式应允许“预设框架字段 + 数据中浮现字段”并存，且需研究者批准后进入正式抽取。 |
| A1-M3 论文收集与概览 | 给出数据库、搜索式、去重、筛选、排除理由、snowballing、质量评价前后分母。 | 可作为概览卡和筛选台账字段种子：source、query、dedup、screening status、exclusion code、fulltext status、snowball source。 |
| A1-M4 字段级证据抽取与模式演化 | 数据抽取包含 study goals、tools、strategy/design、tasks、settings、key results；RQ-specific thematic iterations 体现字段/主题会分轮细化。 | 支持把 A1-M4 设计为可迭代字段抽取，而不是一次性“读完全文生成摘要”；每轮抽取应记录字段版本和 evidence anchors。 |
| A1-M5 统计分析 | RQ0--RQ3 都把字段表转成频次、比例、分布、overlap 和组合分析。 | 支持 Paper2 将统计分析表作为独立产物：统计观察必须绑定字段版本、样本分母和限制。 |
| A1-M6 候选发现形成 | Discussion 将统计观察升级为 lessons learned、recommendations 和 research gaps，同时保留 contested findings。 | 支持候选发现台账：agent 可以提出 candidate finding，但必须标注支持/反向证据、contested status、boundary conditions，最后交研究者裁决。 |

## 6. 可迁移字段树

以下字段树只作为 Paper2 A2a/A3 的候选 scaffold，不是目标领域 schema 定稿。

```text
review_record
├── bibliographic_metadata
│   ├── title / authors / year / DOI / venue / publication_type / CCF_category / CCF_rank
│   ├── review_type: SLR / SMS / tertiary / guideline / hybrid
│   └── open_artifacts: replication_package_url / supplemental_material / dataset_status
├── scope_and_protocol
│   ├── topic_object
│   ├── impact_object_or_construct
│   ├── time_window
│   ├── databases
│   ├── search_string_segments
│   ├── control_papers
│   ├── query_iterations
│   ├── inclusion_criteria
│   └── exclusion_criteria
├── selection_flow
│   ├── initial_records_by_database
│   ├── duplicates_removed
│   ├── title_abstract_screened
│   ├── full_text_screened
│   ├── snowballing_added
│   ├── quality_assessed
│   ├── final_included
│   └── exclusion_reason_counts
├── quality_assessment
│   ├── qa_framework
│   ├── qa_criteria
│   ├── scoring_scale
│   ├── threshold
│   ├── excluded_by_quality
│   └── score_distribution
├── extraction_and_synthesis
│   ├── extracted_fields: goals / tools / strategy / design / tasks / settings / key_results
│   ├── descriptive_summary_per_study
│   ├── thematic_iterations
│   ├── citation_cross_check
│   └── traceability_mechanism
├── landscape_dimensions
│   ├── publication_year
│   ├── author_distribution
│   ├── venue_focus
│   └── studied_tools_or_artifacts
├── method_dimensions
│   ├── empirical_strategy
│   ├── procedure
│   ├── objective: formative / summative
│   ├── analysis_type: qualitative / quantitative / mixed
│   ├── data_source
│   ├── instrument_origin: author_designed / validated_framework
│   └── metric_type
├── effect_synthesis
│   ├── benefits
│   │   ├── accelerate_development
│   │   ├── minimize_search
│   │   ├── automate_repetitive_tasks
│   │   ├── support_knowledge_acquisition
│   │   ├── support_code_adjacent_tasks
│   │   ├── reduce_task_initiation_overhead
│   │   ├── improve_quality
│   │   └── support_debugging
│   ├── risks
│   │   ├── fail_requirements
│   │   ├── over_reliance_cognitive_offloading
│   │   ├── limit_quality
│   │   ├── disrupt_flow
│   │   └── reduce_collaboration
│   └── contested_themes: theme / support_evidence / counter_evidence / boundary_condition
├── framework_mapping
│   ├── framework_name
│   ├── predefined_dimensions
│   ├── emergent_subdimensions
│   ├── study_to_dimension_matrix
│   ├── dimension_overlap
│   └── underexplored_dimensions
├── implications_and_recommendations
│   ├── synthesis_lens: e.g., tetrad / socio_technical_lens
│   ├── lessons_learned
│   ├── practitioner_recommendations
│   ├── researcher_recommendations
│   └── ethical_or_professional_considerations
└── validity_and_update_risks
    ├── search_selection_bias
    ├── repeatability_bias
    ├── classification_rigor
    ├── evidence_base_limitations
    ├── methodological_diversity
    ├── temporal_relevance
    └── update_requirement
```

## 7. 对 Paper2 story / method 的启发与风险

### 7.1 启发

1. **RQ 层级可以显式绑定证据产物**：RQ0 对应 landscape table，RQ1 对应 method/instrument table，RQ2 对应 benefit/risk table，RQ3 对应 framework mapping table。Paper2 后续也应让每个 RQ 对应明确的审计制品，而不是泛泛“我们分析了论文”。
2. **字段树需要同时包含研究对象字段与方法字段**：本文把 primary studies 的 method strategy、procedure、instrument、metric 当作结果对象，这对我们很重要；Paper2 也应把 target papers 的研究设计、数据、评价、制品作为字段，而不只抽取领域主题。
3. **外部框架 + emergent coding 的组合可迁移**：SPACE 提供初始五维，但作者又添加 sub-dimensions。Paper2 的维度模式也应允许研究者定义元模型后，在抽取失败或新类型出现时版本化扩展。
4. **contested finding 的写法值得直接学习**：code quality 同时出现在 benefit 和 risk，并由作者解释为 context/metric/task 差异。Paper2 的候选发现台账应内置“矛盾证据/反向证据”字段。
5. **summary 段落是结果章节的审计压缩层**：每个 RQ 末尾 summary 都包含数字、排序和 gap，适合后续 paper writing；但这些 summary 应由统计表生成或至少可回溯。
6. **Discussion 可用第二框架做解释，而不是重复结果**：SPACE 负责 measurement，Tetrad 负责 socio-technical interpretation。这提示 Paper2 可以区分“字段统计框架”和“候选发现解释框架”。
7. **Artifacts 是现代 SLR 可信度的一部分**：本文显式发布 selection decisions 和 exclusion rationales。Paper2 的方法贡献必须把过程证据、字段证据、统计表、候选发现台账和裁决日志作为导出物。

### 7.2 风险

1. **不要把这篇的 LLM productivity findings 当成我们的领域 finding**：accelerated development、reduced search、over-reliance 等只能作为 benefit/risk synthesis pattern，不能支撑 LLM4STM 或系统综述自动化的结论。
2. **不要复制 SPACE 作为默认元模型**：SPACE 适合 developer productivity；Paper2 若目标是系统综述证据工程，元模型应围绕 review protocol、field evidence、statistics、candidate findings、human gates，而不是 productivity。
3. **不要忽视 primary evidence base limitation**：本文自己承认证据多为 formative、lab、self-report、短期研究。我们若借鉴其结果表风格，也必须在自己的语料中保留证据强度字段。
4. **不要声称 PRISMA 合规**：本文使用 PRISMA flow chart，但 Paper2 当前边界是类 PRISMA 透明材料；除非后续完整执行，否则只能说受启发的透明制品。
5. **不要把人工验证成本隐藏掉**：本文有 47 天标题摘要筛选、10 周全文筛选、3 个月综合、9 个月会议讨论。Paper2 若引入 agent，需要诚实记录人机协作成本，而不是暗示自动化免费替代。
6. **快速漂移风险很高**：本文截至 2024 年底，正式出版在 2026 年；LLM tools 和 developer workflow 变化快。Paper2 若做活领域，也要有 update policy 或 temporal cutoff。

## 8. 待复核

1. 当前只读 `paper_content.txt`，未打开 `paper.pdf` 逐页核对；Table 1--11、Fig. 1--9 的页码、版式和最终 ACM 版本需人工 PDF / ACM 页面复核。
2. `metadata.json` 记录正式 TOSEM 2026 DOI，`paper_content.txt` 开头仍有 arXiv / manuscript submitted / placeholder DOI 痕迹；正式引用前需确认 ACM final version 与 arXiv v2 差异。
3. Zenodo replication package 未下载核验；这里只记录原文声明的 artifact 入口，未核验 package 内部文件完整性。
4. CCF-A 字段本轮沿用本仓库 ccf_venues 缓存记录 TOSEM 为 A 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
5. RQ2 benefit/risk 的主题频次来自文本提取和表格说明，雷达图精确数值需 PDF 图核对后才能进入跨论文统计。
6. 若 A2a/A3 采纳本文字段树，应新增或确认字段：`control_papers`、`query_iterations`、`instrument_origin`、`contested_theme`、`framework_mapping`、`summary_style`、`temporal_relevance_threat`。

## 维度树复原

### 一句话结论

本文的维度树主类型为“RQ 驱动分类树”，辅助类型为“生产力 benefit-risk 评价树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-llm-assistants-developer-productivity-tree-type]

旧有“可迁移字段树 / 字段树 / schema 缺口”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-llm-assistants-developer-productivity-root] | The Impact of LLM-Assistants on Software Developer Productivity 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-llm-assistants-developer-productivity-b1] 综述范围与研究问题；[dim-llm-assistants-developer-productivity-b2] 语料收集与纳排；[dim-llm-assistants-developer-productivity-b3] 主题 / 对象分类；[dim-llm-assistants-developer-productivity-b4] 方法 / 技术 / 干预；[dim-llm-assistants-developer-productivity-b5] 评价、统计与候选发现 | [ev-llm-assistants-developer-productivity-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-llm-assistants-developer-productivity-root] The Impact of LLM-Assistants on Software Developer Productivity
├── [dim-llm-assistants-developer-productivity-b1] 综述范围与研究问题
│   └── [leaf-llm-assistants-developer-productivity-scope] 研究范围与单位对象
├── [dim-llm-assistants-developer-productivity-b2] 语料收集与纳排
│   └── [leaf-llm-assistants-developer-productivity-corpus] 语料与纳排链条
├── [dim-llm-assistants-developer-productivity-b3] 主题 / 对象分类
│   └── [leaf-llm-assistants-developer-productivity-taxonomy] 主题与维度分类
├── [dim-llm-assistants-developer-productivity-b4] 方法 / 技术 / 干预
│   └── [leaf-llm-assistants-developer-productivity-method] 方法 / 技术 / 干预分类
└── [dim-llm-assistants-developer-productivity-b5] 评价、统计与候选发现
    └── [leaf-llm-assistants-developer-productivity-evidence] 评价、证据与复现资产
    └── [leaf-llm-assistants-developer-productivity-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-llm-assistants-developer-productivity-scope] | 研究范围与单位对象 | [dim-llm-assistants-developer-productivity-b1] | 定义 LLM assistants / developer productivity 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-scope] |
| [leaf-llm-assistants-developer-productivity-corpus] | 语料与纳排链条 | [dim-llm-assistants-developer-productivity-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-corpus] |
| [leaf-llm-assistants-developer-productivity-taxonomy] | 主题与维度分类 | [dim-llm-assistants-developer-productivity-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-taxonomy] |
| [leaf-llm-assistants-developer-productivity-method] | 方法 / 技术 / 干预分类 | [dim-llm-assistants-developer-productivity-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-method] |
| [leaf-llm-assistants-developer-productivity-evidence] | 评价、证据与复现资产 | [dim-llm-assistants-developer-productivity-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-evidence] |
| [leaf-llm-assistants-developer-productivity-finding] | 统计观察与候选发现 | [dim-llm-assistants-developer-productivity-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-llm-assistants-developer-productivity-leaf-finding] |

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-llm-assistants-developer-productivity-method-evidence] | [leaf-llm-assistants-developer-productivity-method] | 支撑 / 度量 | [leaf-llm-assistants-developer-productivity-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-llm-assistants-developer-productivity-taxonomy] | [clm-llm-assistants-developer-productivity-edge-method-evidence] |
| [edge-llm-assistants-developer-productivity-taxonomy-finding] | [leaf-llm-assistants-developer-productivity-taxonomy] | 导出候选发现 | [leaf-llm-assistants-developer-productivity-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-llm-assistants-developer-productivity-stat] | [clm-llm-assistants-developer-productivity-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-llm-assistants-developer-productivity-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 是 | 识别可迁移的维度模式类型 | 可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 |
| [leaf-llm-assistants-developer-productivity-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 是 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-llm-assistants-developer-productivity-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-llm-assistants-developer-productivity-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | LLM assistants / developer productivity 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-llm-assistants-developer-productivity-transfer] |
| [leaf-llm-assistants-developer-productivity-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-llm-assistants-developer-productivity-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-llm-assistants-developer-productivity-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-llm-assistants-developer-productivity-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-llm-assistants-developer-productivity-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-llm-assistants-developer-productivity-001 | [ev-llm-assistants-developer-productivity-root] | [src-llm-assistants-developer-productivity-text], [src-llm-assistants-developer-productivity-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | strong | [dim-llm-assistants-developer-productivity-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-llm-assistants-developer-productivity-002 | [ev-llm-assistants-developer-productivity-taxonomy] | [src-llm-assistants-developer-productivity-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度。 | taxonomy | medium | [dim-llm-assistants-developer-productivity-b1], [dim-llm-assistants-developer-productivity-b2], [dim-llm-assistants-developer-productivity-b3], [dim-llm-assistants-developer-productivity-b4], [dim-llm-assistants-developer-productivity-b5], [leaf-llm-assistants-developer-productivity-taxonomy], [leaf-llm-assistants-developer-productivity-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-llm-assistants-developer-productivity-003 | [ev-llm-assistants-developer-productivity-stat] | [src-llm-assistants-developer-productivity-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | statistical_result | medium | [leaf-llm-assistants-developer-productivity-evidence], [leaf-llm-assistants-developer-productivity-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-llm-assistants-developer-productivity-004 | [ev-llm-assistants-developer-productivity-risk] | [src-llm-assistants-developer-productivity-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | medium | [dim-llm-assistants-developer-productivity-root], [leaf-llm-assistants-developer-productivity-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-llm-assistants-developer-productivity-005 | [ev-llm-assistants-developer-productivity-relation] | [src-llm-assistants-developer-productivity-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边。 | taxonomy | medium | [edge-llm-assistants-developer-productivity-method-evidence], [edge-llm-assistants-developer-productivity-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-llm-assistants-developer-productivity-tree-type] | A1DT-llm-assistants-developer-productivity-C01 | 本文的维度树主类型为“RQ 驱动分类树”，辅助类型为“生产力 benefit-risk 评价树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-llm-assistants-developer-productivity-tree-type] | tree_type | [dim-llm-assistants-developer-productivity-root] | EV-llm-assistants-developer-productivity-001, EV-llm-assistants-developer-productivity-004 | 树型判断仅限本文，不代表所有 LLM assistants / developer productivity 综述。 | strong | statistical_synthesis | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-scope] | A1DT-llm-assistants-developer-productivity-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-scope] | EV-llm-assistants-developer-productivity-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-corpus] | A1DT-llm-assistants-developer-productivity-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-corpus] | EV-llm-assistants-developer-productivity-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-taxonomy] | A1DT-llm-assistants-developer-productivity-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-taxonomy] | EV-llm-assistants-developer-productivity-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-method] | A1DT-llm-assistants-developer-productivity-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-method] | EV-llm-assistants-developer-productivity-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-evidence] | A1DT-llm-assistants-developer-productivity-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-evidence] | EV-llm-assistants-developer-productivity-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-llm-assistants-developer-productivity-leaf-finding] | A1DT-llm-assistants-developer-productivity-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-llm-assistants-developer-productivity-finding] | EV-llm-assistants-developer-productivity-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-llm-assistants-developer-productivity-transfer] | A1DT-llm-assistants-developer-productivity-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-llm-assistants-developer-productivity-root] | EV-llm-assistants-developer-productivity-002, EV-llm-assistants-developer-productivity-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | medium | schema_seed | false | -- |
| [clm-llm-assistants-developer-productivity-finding-boundary] | A1DT-llm-assistants-developer-productivity-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-llm-assistants-developer-productivity-finding] | EV-llm-assistants-developer-productivity-003, EV-llm-assistants-developer-productivity-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | medium | candidate_finding | false | -- |
| [clm-llm-assistants-developer-productivity-edge-method-evidence] | A1DT-llm-assistants-developer-productivity-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-llm-assistants-developer-productivity-method-evidence] | EV-llm-assistants-developer-productivity-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | medium | schema_seed | false | -- |
| [clm-llm-assistants-developer-productivity-edge-taxonomy-finding] | A1DT-llm-assistants-developer-productivity-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-llm-assistants-developer-productivity-taxonomy-finding] | EV-llm-assistants-developer-productivity-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | medium | candidate_finding | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-llm-assistants-developer-productivity-structure-check] | [dim-llm-assistants-developer-productivity-root], A1DT-llm-assistants-developer-productivity-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-llm-assistants-developer-productivity-visual-check] | EV-llm-assistants-developer-productivity-002, EV-llm-assistants-developer-productivity-003, EV-llm-assistants-developer-productivity-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
