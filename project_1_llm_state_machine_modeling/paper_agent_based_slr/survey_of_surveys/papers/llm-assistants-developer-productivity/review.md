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
| 综述类型 | SLR + SMS；39 篇 peer-reviewed 原始研究，时间范围 2014--2024 |
| SE 子领域 | LLM assistants / developer productivity / LLM4SE empirical studies |
| 阅读状态 | 已读 [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)；未回 PDF 逐页核对图表 |
| 证据等级 | 全文文本级；图表/表格精确版式与页码待人工原文核对 |
| artifacts | 原文声明所有制品公开于 Zenodo replication package：https://zenodo.org/records/18489222 |
| A1 角色 | 高相关、现代、CCF-A 的 SLR+SMS 样本；用于学习如何把 `landscape -> method -> benefit/risk -> productivity dimensions -> implications/threats` 组织为 RQ 和结果表。 |
| 是否目标领域证据池 | 否。本文只能作为 Paper2 的 scaffold / pattern prior，不能把其 LLM-assistant productivity findings 直接当成我们目标领域发现。 |
| 核心可借鉴点 | RQ0--RQ3 层级清晰：先给研究景观，再给方法与工具，再给 benefit/risk，最后用外部框架映射 productivity dimensions；每个 RQ 末尾都有短 summary，把分布数字、主导类别、争议点和下一步 gap 压成可引用结论。 |
| 主要风险 | 其领域结论受 2024 年爆发式文献和快速模型漂移影响；原始研究 多为 formative / lab / self-report，适合学习报告结构，但不适合作为强领域事实迁移。 |

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

纳入标准很短：研究 AI 或 LLMs 对 软件开发者 productivity 的影响；英文；2014 年及以后发表且全文可访问。排除标准包括：不关注 SE 或不研究 productivity impact、只顺带提及而非研究主题、二次研究 / WIP / extended abstracts / posters / tool demos / editorials / 灰色文献（grey literature） / book / thesis / workshop 等不符合正式 peer review 口径的出版类型、少于 4 页、全文不可访问。

筛选流程的分母链条很完整：初始 9,756 条，去重 803 后剩 8,953 条做标题摘要筛选；标题摘要阶段排除 8,725 条，剩 228 条全文筛选；全文阶段排除 189 条；对入选研究做 backward / forward snowballing 额外加入 5 条；44 条进入质量评价；质量评价排除 5 条；最终纳入 39 条。作者使用 Rayyan 标注排除理由，并说明标题摘要筛选由第一作者完成、第二和第三作者验证 excluded papers，遇到不确定时保守进入全文阶段。

这里可迁移的是“分母链 + 排除原因 + 工具 + 人工验证角色”的组合。Paper2 若要做类 PRISMA 透明材料，可以学习这种粒度，但不能声称 PRISMA 合规，除非后续完整满足透明报告要求。

### 2.5 质量评价

质量评价采用 Lenarduzzi 等人的 empirical SE study QA 策略，包含 11 个 QA criteria：研究是否基于 research、目标是否清晰、上下文是否充分、研究设计是否适当、招募策略、控制组、数据收集、数据分析严谨性、研究者与参与者关系、finding 清晰性、研究/实践价值。每项按 0--4 的 Likert scale 打分，并使用 50% 平均分阈值排除低质量研究；最后 5 篇因质量评价被排除，39 篇进入最终综合。

对 Paper2 的重要启发：质量评价不是为了形式上打分，而是连接到“哪些 原始研究 可以进入结果综合”。如果我们后续使用 agent 抽取字段，quality / eligibility 必须成为字段证据表的一等字段，否则后续统计会混入低质量或不合格条目。

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
5. Support code-adjacent tasks：ideation、requirements specification、文档、QA、emails、meeting minutes、onboarding、issue 文档。
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

- Satisfaction：developer experience、self-efficacy、trust、cognitive load；well-being 没有 原始研究 直接研究。
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
| finding pattern | 从统计分布生成 findings，但同时保留 contested findings 和 boundary conditions；code quality 被明确写成 benefit/risk 双重主题。 | RQ2 §6.1--§6.2；RQ2 summary；Discussion research gaps。 | 可迁移为候选发现台账：每个 候选发现 应包含支持证据、反向证据、适用上下文、主张强度。 | 不能把“LLM improves productivity”等主题结论搬到我们的目标领域。 |
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
| A1-M6 候选发现形成 | Discussion 将统计观察升级为 lessons learned、recommendations 和 research gaps，同时保留 contested findings。 | 支持候选发现台账：agent 可以提出 候选发现，但必须标注支持/反向证据、contested status、boundary conditions，最后交研究者裁决。 |

## 历史草稿（已迁移，不作事实真源）：旧第 6 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

以下字段树只作为 Paper2 A2a/A3 的候选 scaffold，不是目标领域 schema 定稿。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
综述记录（review_record）
├── 书目元数据
│   ├── 标题 / 作者 / 年份 / DOI / 发表源 / 发表类型 / CCF 大类 / CCF 等级
│   ├── 综述类型：SLR / SMS / tertiary / guideline / hybrid
│   └── 开放制品：复现包链接 / 补充材料 / 数据集状态
├── 范围与协议
│   ├── 主题对象
│   ├── 影响对象或构念
│   ├── 时间窗
│   ├── 数据库
│   ├── 检索式片段
│   ├── 控制论文
│   ├── query iterations
│   ├── 纳入标准
│   └── 排除标准
├── 选择流程
│   ├── 各数据库初始记录数
│   ├── 去重数量
│   ├── 标题摘要筛选数量
│   ├── 全文筛选数量
│   ├── 滚雪球新增数量
│   ├── 质量评估数量
│   ├── 最终纳入数量
│   └── 排除原因计数
├── 质量评估
│   ├── QA 框架
│   ├── QA 条目
│   ├── 评分尺度
│   ├── 阈值
│   ├── 因质量排除数量
│   └── 分数分布
├── 抽取与综合
│   ├── 抽取字段：goals / tools / strategy / design / tasks / settings / key_results
│   ├── 单篇描述性摘要
│   ├── 主题分析迭代
│   ├── 引用交叉检查
│   └── 可追踪机制
├── 研究图景维度
│   ├── 发表年份
│   ├── 作者分布
│   ├── 发表源焦点
│   └── 被研究工具或制品
├── 方法维度
│   ├── 实证策略
│   ├── 研究流程
│   ├── 目标：formative / summative
│   ├── 分析类型：qualitative / quantitative / mixed
│   ├── 数据来源
│   ├── 测量工具来源：author_designed / validated_framework
│   └── 指标类型
├── 收益 / 风险维度
│   ├── 收益主题
│   ├── 风险主题
│   ├── 矛盾主题
│   └── 证据边界
├── 外部框架映射
│   ├── SPACE 维度
│   ├── SPACE 子维度
│   ├── 维度覆盖数
│   └── 组合模式
└── 解释与建议
    ├── McLuhan Tetrad
    ├── lessons learned
    ├── practitioner recommendations
    ├── researcher recommendations
    └── temporal relevance threat
```

## 7. 对 Paper2 story / method 的启发与风险

### 7.1 启发

1. **RQ 层级可以显式绑定证据产物**：RQ0 对应 landscape table，RQ1 对应 method/instrument table，RQ2 对应 benefit/risk table，RQ3 对应 framework mapping table。Paper2 后续也应让每个 RQ 对应明确的审计制品，而不是泛泛“我们分析了论文”。
2. **字段树需要同时包含研究对象字段与方法字段**：本文把 原始研究 的 method strategy、procedure、instrument、metric 当作结果对象，这对我们很重要；Paper2 也应把 target papers 的研究设计、数据、评价、制品作为字段，而不只抽取领域主题。
3. **外部框架 + emergent coding 的组合可迁移**：SPACE 提供初始五维，但作者又添加 sub-dimensions。Paper2 的维度模式也应允许研究者定义元模型后，在抽取失败或新类型出现时版本化扩展。
4. **contested finding 的写法值得直接学习**：code quality 同时出现在 benefit 和 risk，并由作者解释为 context/metric/task 差异。Paper2 的候选发现台账应内置“矛盾证据/反向证据”字段。
5. **summary 段落是结果章节的审计压缩层**：每个 RQ 末尾 summary 都包含数字、排序和 gap，适合后续 paper writing；但这些 summary 应由统计表生成或至少可回溯。
6. **Discussion 可用第二框架做解释，而不是重复结果**：SPACE 负责 measurement，Tetrad 负责 socio-technical interpretation。这提示 Paper2 可以区分“字段统计框架”和“候选发现解释框架”。
7. **Artifacts 是现代 SLR 可信度的一部分**：本文显式发布 selection decisions 和 exclusion rationales。Paper2 的方法贡献必须把过程证据、字段证据、统计表、候选发现台账和裁决日志作为导出物。

### 7.2 风险

1. **不要把这篇的 LLM productivity findings 当成我们的领域 finding**：accelerated development、reduced search、over-reliance 等只能作为 benefit/risk synthesis pattern，不能支撑 LLM4STM 或系统综述自动化的结论。
2. **不要复制 SPACE 作为默认元模型**：SPACE 适合 developer productivity；Paper2 若目标是系统综述证据工程，元模型应围绕 review protocol、field evidence、statistics、候选发现、human gates，而不是 productivity。
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

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__codex.md](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__codex.md)、[../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__claude.md](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__claude.md)、[../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__deepseek.md](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/llm-assistants-developer-productivity.md](../../audits/a1dt-v2-19x3/adjudications/llm-assistants-developer-productivity.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `llm-assistants-developer-productivity` |
| 审计代理 | `claude` (claude-opus-4-7[1m]) |
| 是否已读 `paper_content.txt` | 是；按页通读 Page 1–36（覆盖 abstract / intro / background / methodology / RQ0–RQ3 全部结果 / discussion / 威胁），未逐字读 Conclusion / References 段，但已覆盖审计所需正文。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两者一致核对（DOI 10.1145/3809494；ACM TOSEM 2026；arXiv 2507.03156 v2）。 |
| 是否打开或核对 `paper.pdf` | 否；本轮以 `paper_content.txt`（已按 `--- Page N ---` 分页）为主，复杂图表（Fig. 3/4/5/7/8/9 雷达图、UpSet 图、Sankey 图）与最终 ACM 版式留待 A2a/PDF 视觉核验。 |
| 原文类型 | SLR + SMS 混合（作者自称 "系统综述 and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + 主题综合）。 |
| 被编码样本单位 | **原始研究**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 |
| 样本数量 / 分母 | 9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 |
| 原生树类型 | **多根维度森林**：每个 RQ 对应一棵 抽取 sub树；底层共享 PS-id 这一样本单位主键，使所有 sub树 可交叉关联。 |
| 主统计池资格 | **是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；收益 / 风险（benefit/risk） 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 细粒度（fine-grained） 字段须等 A2a 精核精确数字。 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

实际读取：

- `bibtex.bib`（10 行）— 验证标题、作者、TOSEM 2026、DOI。
- `metadata.json` — 验证 publication date 2026-04-27、arXiv 来源、`eligible_for_schema_seed=true`（模式种子字段为真）、`eligible_for_statistical_synthesis=true`、`evidence_role=hybrid_slr_sms_pattern`。
- `paper_content.txt` — 通读 Page 1–36，主要章节：
  - §1 Introduction（Page 1–2）
  - §2 Background（Page 3–4，含 SPACE 来源 [19]）
  - §3 Methodology（Page 4–9）：§3.1 pre-review mapping、§3.1.1 control papers、Inclusion/Exclusion criteria、§3.1.2 query formulation、§3.2 筛选过程、§3.3 QA、§3.4 数据抽取 & synthesis
  - §4 RQ0 Landscape（Page 9–11）
  - §5 RQ1 Methodology/instruments（Page 11–17）
  - §6 RQ2 Benefits & Risks（Page 17–24）
  - §7 RQ3 SPACE mapping（Page 24–27）
  - §8 Discussion（Page 27–35，含 McLuhan Tetrad + 5 实践者 recs + 3 研究者 recs）
  - §9 效度威胁（Page 35–36）

未做 PDF 视觉核验，主要影响：Fig. 1 PRISMA 实际位置、Fig. 6 radar plot 各 收益 / 风险（benefit/risk） 主题精确数字、Fig. 7/8 SPACE Sankey/UpSet 比例线、Fig. 9 Tetrad 图、Table 9 risk 摘要、Table 10 SPACE 完整列。

关键证据锚点：

1. **PS 集合分母链**（§3.2, Page 7–8 + Fig. 1）："Records identified from 数据库（databases） (n = 9,756) ... duplicates removed (n = 803) ... title/abstract n = 8,953 → excluded 8,725 → 228 → snowballing +5 → QA n = 44 → excluded 5 → **n = 39**"。
2. **EC 分布**（Fig. 1 标注）：EC1=15, EC2=128, EC3=27, EC4=11, EC5=3, ~IC1=5。
3. **QA rubric**（§3.3, Page 8, Table 2）：QA1–QA11 共 11 项 + 5 点 Likert {Excellent 4, Very Good 3, Good 2, Fair 1, Poor 0} + 50% 阈值。
4. **research strategy 分类法**（§5.1, Page 11–12, Table 5）：Stol & Fitzgerald 6 类；Lab 38% (15/39), Field 23% (9), Sample 15% (6), ExpSim 13% (5), Field Exp 5% (2), Judgment 5% (2)。
5. **procedure 分类法**（§5.2, Page 13, Table 6 + Fig. 3/4）：Glass-Vessey-Ramesh 5 类；调查 82% (32), User Exp 41% (16), Case 31% (12), 访谈 26% (10), Concept Impl 10% (4)。
6. **objective**（§5.2, Page 13–14）：Hartson 分类法，formative 59% (23) / summative 41% (16)。
7. **data source × instrument origin**（§5.3, Page 14, Table 7）：Self-reported vs Behavioral; designed by authors vs validated（NASA-TLX, SPACE survey, TAM, AAR/AI, self-efficacy, emotion affect, TCQ, RBV）。
8. **time-to-completion**：31% (12/39) - §5.3.1, Page 15。
9. **8 benefits + 5 risks 主题**（§6.1–§6.2, Page 17–24, Fig. 6 radar + Table 8 + Table 9）。
10. **SPACE mapping**（§7, Page 24–27, Fig. 7/8 + Table 10/11）：Satisfaction 77%, Performance 64%, 效率 59%, Activity 31%, Communication 26%；90% ≥2 维, 44% ≥3 维, 15% ≥4 维；最常见组合 S+P+E (5/39)。Satisfaction sub: developer-experience, self-efficacy, trust, cognitive-load, well-being (=0). Performance sub: 质量, impact. 效率 sub: temporal-efficiency, automation, interruptions-and-flow. Communication sub: human-LLM (7/10), human-human (3/10).
11. **McLuhan Tetrad**（§8.1, Page 27–30, Fig. 9）：Enhance / Reverse / Obsolesce / Retrieve 四维 + lessons learned (1–3) + 5 实践者 recs (Trust / role / workflow / org / professional ethics)。
12. **Threats**（§9, Page 35–36）：selection bias, human-centered identification, bias & repeatability, 分类 rigor, 形成性与受控研究主导（formative/controlled dominance）, 方法多样性（methodological diversity）, 时间相关性（temporal relevance）（2024 占 77%）。

### 2. 样本单位与字段来源判定

**1. 纳入和逐项描述的对象**：peer-reviewed 原始研究，编号 PS1–PS39，每条 PS 在多张表格中作为主键被反复挂接（venue, 工具, strategy, procedure, instrument, benefit, risk, SPACE sub-dimension, QA score）。

**2. 是否有系统检索/纳排/抽取/编码方案**：是。完整含 Kitchenham&Charters protocol、6 数据库 search string、17 control papers、5 轮 query iteration、Rayyan 标注、47-day title/abstract screening、10-week 完整-text screening、PRISMA flow chart、Lenarduzzi 11-QA rubric、初始 主题分析 + 三轮 targeted 主题分析（针对 RQ1/RQ2/RQ3）、citation cross-check。

**3. 字段来源**：

- **抽取 form**（§3.4 列出："研究 goals, 工具, 经验研究（empirical） strategy and design, tasks, settings, key results"）
- **分类方案（分类 模式）s**：Stol & Fitzgerald (strategy)、Glass-Vessey-Ramesh (procedure)、Hartson (formative/summative)、SPACE (Forsgren et al.)
- **QA rubric**：Lenarduzzi 11 项
- **emergent thematic 代码**：8 benefits + 5 risks（主题分析 自产）
- **interpretive lens**：McLuhan Tetrad（应用于 discussion，不是抽取字段，但提供推论 模式）
- **supplemental appendix + Zenodo 复现包**：control papers list、query iterations、QA scores、exclusion rationales

**4. RQ ↔ 样本单位**：RQ 是字段使用方式（landscape RQ0 / methodology RQ1 / impact RQ2 / dimension RQ3），样本单位仍是 PS。RQ 不是树根，而是把 PS 字段切成不同分析维度的"棱镜"。

**5. 是否需要降级**：不需要。本文有完整系统证据基础，主统计池资格成立；只是部分 细粒度（fine-grained） 数字（Fig. 6 雷达精确计数、Sankey 流量、Table 9 详尽 risk 行）尚未在文本中完全读出，需 A2a/PDF 复核。

### 3. 原生样本编码维度树 / 维度森林

样本单位主键：`PS-id ∈ {PS1, …, PS39}`。每棵 RQ-sub树 通过 PS-id 与其他 sub树 关联。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[森林根节点] LLM 助手 × 开发者生产力系统综述与映射研究模式（SLR+SMS 模式）
│
├── [树-meta] 元数据 / 样本主键
│   ├── 原始研究编号（PS-id） (PS1..PS39)
│   ├── 标题 / 作者 / 年份 / 发表源
│   ├── 纳入状态：纳入（included）| 滚雪球补入（snowballed）| QA 排除（qa_excluded）| 筛除（screened_out）
│   ├── 排除代码 (EC1..EC5 | ~IC1 | 无（无更新）)
│   └── 质量评分 (QA1..QA11 每项 取值 ∈ {0,1,2,3,4}, 平均分达到 50% 阈值（avg ≥ 50% threshold）)
│
├── [树-RQ0] 研究图景（RQ0 字段集合）
│   ├── 发表年份 取值 ∈ {2014..2024, 2025-Jan}（数值）
│   ├── 作者发表篇数分布（数值；147 位作者各 1 篇，6 位作者各 2 篇，1 位作者 3 篇（Igor Steinmacher））
│   ├── 发表源（Table 3 中 39 个 发表源 命名实体）
│   ├── 发表源研究焦点（封闭枚举：软件工程 / 计算机科学（SE/CS）、人机交互（HCI）、信息系统 / 决策科学（IS/Decision Science）、人的因素（Human-Aspects）、AI for SE / AI Engineering、软件工程教育（SE Education））
│   └── 使用的 LLM 工具（Table 4 开放枚举：ChatGPT, GitHub Copilot, Tabnine, GPT-4, CodeWhisperer, GPT-3.5, Claude, Codex, Gemini, GPT-3, Ansible Lightspeed, Bard, CodeGen2 7B, GILT, CodeCompose, NL2Code PyCharm plugin, StackSpotAI, StarCoder 7B, TransCoder, aiXcoder, OpenAI API, Midjourney）
│
├── [树-RQ1] 方法 / 流程 / 测量工具
│   ├── 实证策略（Stol-Fitzgerald 封闭 6 枚举：字段研究（字段研究）| 字段实验（字段实验）| 实验仿真（Experimental Simulation）| 实验室实验（实验室实验）| 样本研究（样本研究）| 判断研究（判断研究））
│   ├── 研究流程（Glass-Vessey-Ramesh 多选 5 枚举）：调查（调查）| 用户实验（用户实验）| 案例研究（案例研究）| 访谈（访谈）| 概念实现（概念实现）
│   ├── 混合方法（布尔：69% true）
│   ├── 研究目标（封闭枚举：formative | summative）
│   ├── 数据分析类型（封闭枚举：定量 | 定性 | 混合）
│   ├── 数据来源（封闭枚举：自我报告（自我报告） | 行为与绩效指标（行为与绩效指标））
│   ├── 测量工具来源（封闭枚举：作者自行设计 | 经过验证的框架）
│   └── 测量工具名称（开放枚举：NASA-TLX, SPACE survey, TAM, self-efficacy, AAR/AI, emotion affect, TCQ, RBV, 任务 完成度与正确性（完成度与正确性）, 建议采纳率（建议采纳率）, 交互日志（交互日志）, 完成时间（完成时间）, 代码 质量 指标, 生产率增益（productivity gain）, 开放式反馈（open-ended feedback）...）
│       └── 关联指标（细分见 Table 7）
│
├── [树-RQ2] 效果综合（主题综合，主题综合）
│   ├── 收益主题（封闭枚举 8 项）
│   │   ├── 加速软件开发（accelerate software development）
│   │   ├── 减少在线代码搜索（minimize online code search）
│   │   ├── 自动化琐碎重复任务（automate trivial repetitive tasks）
│   │   ├── 支持知识获取（support knowledge acquisition）
│   │   ├── 支持代码邻近任务（support code-adjacent tasks）
│   │   ├── 降低任务启动开销（reduce task initiation overhead）
│   │   ├── 改善代码质量（improve code 质量）        ← contested 双向出现
│   │   └── 支持调试与故障排查（support debugging and troubleshooting）
│   ├── 风险主题（封闭枚举 5 项）
│   │   ├── 无法满足需求（fail to meet requirements）
│   │   ├── 促进过度依赖与认知卸载（promote over-reliance and cognitive offloading）
│   │   ├── 限制代码质量（limit code 质量）          ← contested 双向出现
│   │   ├── 打断心流（disrupt the flow）
│   │   └── 降低团队协作（reduce team collaboration）
│   ├── 主题频次（数值；Fig. 6 雷达每主题对应 PS 集合大小）
│   └── 争议主题标记（布尔；代码质量（code-质量） = true）
│
├── [树-RQ3] SPACE 维度映射
│   ├── SPACE 维度（封闭枚举 5）：满意度（Satisfaction）| 绩效（Performance）| 活动（Activity）| 沟通（Communication）| 效率（效率）
│   ├── SPACE 覆盖维度数（数值 0..5 per PS；分布：90% ≥2, 44% ≥3, 15% ≥4）
│   ├── SPACE 子维度（层级枚举）
│   │   ├── 满意度（Satisfaction）：开发者体验（developer experience）| 自我效能（self-efficacy）| 信任（trust）| 认知负荷（cognitive load）| 幸福感（well-being）(=∅)
│   │   ├── 绩效（Performance）：质量| 影响（impact）
│   │   ├── 活动: (no further sub)
│   │   ├── 沟通（Communication）：人-LLM（human-LLM）| 人人（human-human）
│   │   └── 效率（效率）：时间效率（temporal efficiency）| 自动化（automation）| 中断与心流（interruptions and flow）
│   ├── 质量指标实例（Table 11 开放枚举：通过单元测试（Passing Unit Tests）、功能正确性与准确率（Functional Correctness & 准确率）、代码异味（Code Smells）、BLEU、Halstead、圈复杂度（Cyclomatic Complexity）、翻译错误率（Translation Error Rate）、可维护性指数（Maintainability Index）、认知复杂度（Cognitive Complexity）、缺陷密度（Defect Density）、缺陷率（Defect Rate）、技术债（Technical Debt）、代码覆盖率（Code Coverage））
│   └── 最高频组合（自由文本，e.g. "满意度-绩效-效率（Satisfaction-Performance-效率）", 5/39）
│
├── [树-discussion-tetrad] 解释性视角（McLuhan）
│   ├── 增强（enhance）：样板代码、语法回忆、初始脚手架、探索性原型
│   ├── 反转（reverse）：过度依赖、自动化自满、自主性削弱、协作减少
│   ├── 淘汰（obsolesce）：在线搜索、问答平台
│   └── 唤回（retrieve）：文档、需求获取、遗留现代化
│
└── [树-威胁] 有效性威胁
    ├── 综述过程威胁（封闭枚举 4：研究选择偏倚（研究 selection bias）| 以人为中心的识别（human-centered identification）| 偏倚与可重复性（bias & repeatability）| 分类严谨性（分类 rigor））
    └── 原始证据基础威胁（封闭枚举 3：形成性与受控研究主导（formative/controlled dominance） | 方法多样性（methodological diversity） | 时间相关性（temporal relevance））
```

主干说明：

- **维度森林（森林），不是单树**：RQ0/1/2/3 各成独立子树，但都挂在 PS-id 主键上；Tetrad 与 Threats 是解释性覆盖层（interpretive overlay），不直接挂 PS。
- **取值空间饱和度**：[树-RQ0] author/venue/工具 是开放枚举；[树-RQ1] strategy/procedure/objective 是封闭枚举（直接来自外部 分类法）；[树-RQ2] 收益 / 风险（benefit/risk） 是封闭枚举（8+5，由 主题分析 收敛）；[树-RQ3] SPACE 维度是封闭 5 维 + 涌现子维度（emergent sub-dimensions）。

### 4. 叶子维度表

仅列原文已锚定的代表性叶子（共 21 项；完整模式 还有 ~10 项需 A2a 精核精确分母）：

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-ps-id | 论文主键 | 树-meta | 抽取 form | PS1..PS39 | 39 个枚举 | 完整枚举 | 不适用 | 全表分母 | 全表主键 | §3.2 + Fig. 1 | 主键模式可迁移 |
| leaf-ps-qa-score | QA 综合分数 | 树-meta | QA rubric §3.3 | 11 criteria avg ≥ 50% | [0,4] 区间，per criterion 0..4 Likert | 数值 | 不达阈值=excluded | eligibility filter | 质量-weighted 发现 | §3.3, Table 2 | 全可迁移 |
| leaf-pub-year | 发表年份 | 树-RQ0 | RQ0 §4.1 | 年 | 2014..2025-Jan | 数值 | 不适用 | landscape 时间分布 | 时间漂移风险 | §4.1 Fig. 2 | 可迁移 |
| leaf-venue-focus | venue 研究焦点 | 树-RQ0 | Table 3 §4.3 | 6 个 focus 大类 | {SE/CS, HCI, IS/Decision, Human-Aspects, AI Eng, SE Edu} | 完整枚举 | uncategorized | 社区分布 | 跨社区融合 缺口（gap） | §4.3 Table 3 | 可迁移 |
| leaf-llm-工具 | 使用的 LLM 工具 | 树-RQ0 | Table 4 §4.4 | 22 个 工具 name | open enumeration | 开放枚举 | 未报告 | 工具集中度 | 工具漂移 risk | §4.4 Table 4 | 可迁移结构 |
| leaf-strategy | 实证策略 | 树-RQ1 | Stol-Fitzgerald 分类法 | 6 类 | {字段研究, Field Exp, ExpSim, Lab Exp, Sample, Judgment} | 完整枚举 | 不适用 | 策略分布 (38/23/15/13/5/5%) | 生态效度 risk | §5.1 Table 5 | 可迁移 |
| leaf-procedure | 方法 procedure | 树-RQ1 | Glass-Vessey-Ramesh | 5 类 | {调查（调查）, 用户实验（用户实验）, 案例研究（案例研究）, 访谈（访谈）, 概念实现（概念实现）} | 多选完整枚举 | 不适用 | procedure 分布 (82/41/31/26/10%) | 混合方法 比例 | §5.2 Table 6 Fig. 4 | 可迁移 |
| leaf-objective | 研究目标 | 树-RQ1 | Hartson | formative / summative | 完整枚举 2 | 不适用 | formative/summative 比例 (59/41%) | 证据成熟度 | §5.2 Page 14 | 可迁移 |
| leaf-analysis-type | 分析类型 | 树-RQ1 | 抽取 | quant / qual / 混合 | 完整枚举 3 | 不适用 | 比例 (13/21/67%) | triangulation indicator | §5.2 Page 14 | 可迁移 |
| leaf-instrument-origin | 工具来源 | 树-RQ1 | Table 7 §5.3 | designed-by-authors / validated | 完整枚举 2 | 不适用 | validated 比例 (15/39 ≈ 38%) | 可比性 risk | §5.3 Table 7 | 可迁移 |
| leaf-instrument-name | 工具名称 | 树-RQ1 | Table 7 | 含 NASA-TLX, SPACE, TAM, AAR/AI, self-eff, emotion, TCQ, RBV 等 | 开放枚举 | 未报告 | 各工具出现频次 | 标准化 缺口（gap） | §5.3 Table 7 | 可迁移 |
| leaf-指标-time-completion | time-to-completion 使用 | 树-RQ1 | §5.3.1 | 是否使用 | 布尔 | 未报告=false | 31% (12/39) | 跨策略对比 | §5.3.1 Page 15 | 可迁移 |
| leaf-指标-acceptance-rate | LLM 建议接受率 | 树-RQ1 | §5.3.2 | 是否使用 | 布尔 | 未报告=false | 7/39 | proxy 指标 caution | §5.3.2 Page 15–16 | 可迁移含 caveat |
| leaf-指标-cognitive-load | 认知负荷（NASA-TLX 等） | 树-RQ1 | §5.3.3 | 6 studies | 布尔 + outcome direction | 混合 (3 improved / 2 neutral / 1 worse) | 6/39 | contested construct | §5.3.3 Page 16 | 可迁移含 polarity |
| leaf-benefit-theme | 收益主题（8） | 树-RQ2 | §6.1 + Table 8 + Fig. 6 | 8 项封闭枚举 | 完整枚举 | 不适用 | 主题频次 (15/14/12/10/8/7/7/4 待 A2a 核) | 候选发现 | §6.1 Page 17–22 | 主题结构可迁移；具体主题不可 |
| leaf-risk-theme | 风险主题（5） | 树-RQ2 | §6.2 + Fig. 6 | 5 项封闭枚举 | 完整枚举 | 不适用 | 主题频次 (7/6/5/3/?? 待 A2a) | 候选发现 + boundary | §6.2 Page 22–24 | 主题结构可迁移 |
| leaf-contested-flag | 双向主题标志 | 树-RQ2 | §6.1.7 + §6.2.3 + Discussion | "改善代码质量（improve code 质量）" 与 "限制代码质量（limit code 质量）" 同时存在 | 布尔 | false=未发现矛盾 | 矛盾度指标 | reviewer-defense | §8.3 "remains unresolved" | 模式可迁移 |
| leaf-space-dim | SPACE 维度（5） | 树-RQ3 | Forsgren et al. + Table 10 | 5 维 | 完整枚举 | 不适用 | Sat 77% / Perf 64% / Eff 59% / Act 31% / Comm 26% | dimension coverage 缺口（gap） | §7 Table 10 Fig. 7/8 | 框架特定，结构可迁移 |
| leaf-space-coverage-计数 | SPACE 覆盖维数 | 树-RQ3 | §7 计算 | 每 PS 覆盖维数 | 0..5 | 数值 | 0=未覆盖 | 90%/44%/15% 阈值统计 | multidim 成熟度 | §7 Page 25 | 可迁移概念 |
| leaf-space-sub-dim | SPACE 子维度 | 树-RQ3 | Table 10 §7 | 层级枚举 | 层级枚举（例如满意度 → {开发者体验、自我效能、信任、认知负荷、福祉}） | 层级枚举 | well-being=∅(0/39) | sub-dim 缺口（gap） | underexplored detection | §7 Page 25–27 | 框架特定 |
| leaf-质量-指标-instance | 质量度量实例 | 树-RQ3 | Table 11 | 13 指标 名 | 开放枚举 | 未报告 | 各 指标 出现 PS 集合 | 异质性度量 | §7 Table 11 | 可迁移结构 |

> 还需 A2a 精核以达到原生模式 全集：威胁 sub-category 拆分、Fig. 6 雷达精确 8/5 数字、Table 9 risk summary 行级映射、PS×venue 全表（39 行）、PS×工具 全表、QA scores 表（来自 supplemental appendix）、5 实践者 recs / 3 研究者 recs 作为 推荐 叶子 等。

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| 关系边-strategy×instrument | leaf-strategy | 最常共同出现（association / most common with） | leaf-data-source / leaf-instrument-name | 自我报告 vs 行为/绩效指标（self-reported vs behavioral/performance） | 未报告 | §5.3 Fig. 5 Sankey | "behavioral 指标 多与 Lab/Field Exp/ExpSim 关联；self-reported 多与 field/sample" |
| 关系边-strategy×procedure | leaf-strategy | 共现 | leaf-procedure | 多选 | 未报告 | §5.2 Fig. 3 stacked | "user-experiment 几乎独占 lab experiment" |
| 关系边-procedure×procedure | leaf-procedure | 混合方法组合 | leaf-procedure | 二元组 | 不适用 | §5.2 Fig. 4 UpSet | 最常见组合 用户实验 + 调查 (n=10) |
| 关系边-benefit×risk-contested | 收益主题：改善代码质量 | 与……形成争议 | 风险主题：限制代码质量 | 不适用 | 不适用 | §6.1.7 + §6.2.3 + §8.3 | “代码质量双向发现” |
| 关系边-space-dim×dim | leaf-space-dim | 共现 | leaf-space-dim | 二元/三元组合 | 不适用 | §7 Fig. 8 UpSet | Sat-Perf-Eff (5/39) 最常组合 |
| 关系边-ps×space-sub | leaf-ps-id | 研究覆盖 | leaf-space-sub-dim | 层级枚举 | 未报告 | §7 Table 10 | 逐原始研究维度映射 |
| 关系边-ps×benefit | leaf-ps-id | 报告收益 | 收益主题叶子 | 多选 | 未报告 | §6.1 Table 8 | 逐原始研究主题挂接 |
| 关系边-ps×risk | leaf-ps-id | 报告风险 | 风险主题叶子 | 多选 | 未报告 | §6.2 Table 9 | 逐原始研究风险挂接 |
| 关系边-ps×qa | leaf-ps-id | 质量评分为 | 质量评分叶子 | [0,4]，按 QA1..QA11 汇总 | 缺失 = 未进入质量评价 | §3.3 + Zenodo supplemental | 资格门禁 |
| 关系边-tetrad×收益 / 风险 | 四元解释框架（增强 / 反转 / 淘汰 / 恢复） | 综合自 | 收益 / 风险主题子集 | 不适用 | 不适用 | §8.1 + Fig. 9 | 解释性综合 |

显式关系型 模式 存在；该论文在 Fig. 3/4/5/7/8 大量使用 stacked / UpSet / Sankey 表示交叉关系，本质上把 PS-id × dimension 矩阵展开为视觉关系图。

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段/统计表直接支持的统计观察（可进入主统计池）

1. 时间分布：2014–2022 仅 4 篇；2024 占 77%（30/39）（§4.1）。
2. 作者集中度：154 位作者中 147 位单篇；Igor Steinmacher 3 篇（§4.2）。
3. Venue focus 分布：SE/CS 46%；HCI 18%；IS 13%；Human-Aspects 10%；AI Eng 8%；SE Edu 5%（§4.3 Table 3）。
4. 工具集中度：ChatGPT 15, Copilot 14, 其他（Others） ≤3（§4.4 Table 4）。
5. Strategy 分布：Lab 38%/15、Field 23%/9、Sample 15%/6、ExpSim 13%/5、Field Exp 5%/2、Judgment 5%/2（Table 5）。
6. Procedure 分布：调查 82%, User Exp 41%, Case 31%, 访谈 26%, Concept Impl 10%（Table 6）。
7. 混合（Mixed）-方法：69%（27/39）（§5.2）。
8. Formative/summative：59% / 41%（§5.2）。
9. Analysis：混合 67%, qual-only 21%, quant-only 13%（§5.2）。
10. Time-to-completion 使用率 31%（§5.3.1）。
11. SPACE 多维覆盖：90% ≥2, 44% ≥3, 15% ≥4；S 77, P 64, E 59, A 31, C 26%（§7）。
12. Communication 子维：human-LLM 7/10, human-human 3/10（§7 Page 27）。
13. Well-being：0/39（§7 Page 26 + §8.3）。
14. QA 排除：5/44；最终 39（§3.3）。

#### 6.2 由 discussion / 威胁 支撑的候选发现（candidate）

1. Code-质量 双向 contested：作者明确 "remains unresolved"（abstract + §8.3 + §9.2）。
2. Cognitive-load 混合：6 studies NASA-TLX；3 改善 / 2 中性 / 1 增加 frustration（§5.3.3）。
3. Acceptance-rate proxy 风险：PS16 自我警告 blind reliance（§5.3.2）。
4. Throughput 与 code 质量 负相关 r=−0.45（PS26 econometric, §5.3.4 + §8.2）。
5. Multidim adoption 增长但仍不充分（15% 才 ≥4 维, §7 summary）。
6. 76% per 2024 → 时间相关性（temporal relevance） 威胁（§9.2）。
7. 五条 实践者 recs + 三条 研究者 recs（§8.2/§8.3）。

#### 6.3 对 Paper2 可迁移的方法学启发

- **RQ-driven 抽取 模式 设计**（每 RQ 绑定一组 分类法 + 抽取 fields + summary block）。
- **外部 分类法 + emergent thematic 代码** 的混合 模式 模式（5 个外部 分类法 + 8/5 themes）。
- **PRISMA 分母链 + exclusion code 频次 + Rayyan + snowballing** 的 selection 模式。
- **11-item QA rubric + 5-Likert + 50% threshold**：可作为 Paper2 PS eligibility gate 模板。
- **contested-flag**：把"同一字段在 benefit 与 risk 双向出现"标为一等结构。
- **measurement 框架 + interpretation 框架 分层**（SPACE for measurement, Tetrad for interpretation）。
- **per-RQ end-of-section "Summary" 段落格式**：数字 + 主导模式 + caveat 三段式。

#### 6.4 绝不可迁移的领域结论

- "LLM-assistants 加速开发 / 减少搜索 / 提升或降低代码质量" 等 RQ2 收益 / 风险（benefit/risk） 主题结论本身只限 LLM-assistants × developer-productivity 主题。
- SPACE 框架本体不可直接搬到 Paper2 的方法论 模式（除非目标问题确是 productivity）。
- 具体百分比（77/64/59/31/26%）只能作为该子领域时间切片证据。

### 7. 对旧版 `review.md` 的返修来源（C/I/M）

| 等级 | 项 | 当前问题 | 建议返修 |
|---|---|---|---|
| **C1** | "维度树复原" §维度树结构 | 主树退化为六个通用 叶子（scope/语料/分类法/方法/证据/发现），把 RQ0–RQ3 各自的丰富 模式 压成单一 分类法 叶子；"原文模式主树（19×3 审计后返修）" 也仅 6 行抽象主干，没有展开 PRISMA 链、QA rubric、Stol-Fitzgerald 6 类、Glass-Vessey-Ramesh 5 类、SPACE 5×N 子维、8/5 主题 etc.。这是 A1-DT v2 的核心 mismatch — 学术目标层级风险（影响 Paper2 模式种子 可靠性）。 | 改为本审计 §3 的 RQ-森林结构：以 PS-id 为主键，4 棵 RQ-sub树 + Tetrad overlay + Threats overlay；通用六叶降级为最尾部的 "跨论文投影" 视图。 |
| **C2** | A.2 证据账本 EV-llm-…-001..005 | 仅 5 条证据，全部标 `not_verified`、`证据强度=not_verified`，连最基本的 PRISMA 分母（9756/803/8953/228/189/5/44/5/39）、QA 11 项、Stol-Fitzgerald 6 类百分比、SPACE 5 维百分比这些**纯文本可定位**的事实都未单独立证。导致 A.3 全 12 条 claim 一律 weak/模式种子（schema_seed），无法支撑 SUMMARY 表中 `eligible_for_statistical_synthesis=true` 的判断。 | 至少新增 15+ 条具体 EV 行：每条挂明确节号、表号、数字证据；分母链与 QA rubric 应升级到 `证据强度=strong/文本已核验（text_verified）`。 |
| **I1** | "叶子维度表" 六叶取值空间 | 六叶的"取值空间"列全部写"自由文本加 RQ/贡献声明引用"等模板化 boilerplate；丢失了原文中**封闭枚举**（strategy 6 类、procedure 5 类、SPACE 5 维、benefit 8 / risk 5）的关键性质。封闭枚举是统计池资格的核心判据。 | 按本审计 §4 叶子表逐叶给真实取值空间，区分完整枚举 / 层级枚举 / 数值 / 布尔 / 开放枚举。 |
| **I2** | "统计与候选发现链路" | 表中三行均判为 "否（A1-DT 阶段仅作 模式种子）" — 但 metadata.json 明确 `eligible_for_statistical_synthesis=true`，且本文是 39 篇明确分母的现代 SLR+SMS。该结论与 metadata 矛盾。 | 改为 "局部可统计"：landscape / strategy / procedure / SPACE coverage 等可直接进入主统计池；contested 主题与 细粒度（fine-grained） 数字标 "待 A2a 精核后升级"。 |
| **I3** | "原文模式候选叶子映射（A1 种子）" | 5 个 `orig-*` 候选叶子（assistant-type / developer-task / productivity-outcome / 评价-design / human-factor）含义模糊，且与本文实际的 RQ 字段（strategy/procedure/instrument/SPACE/收益 / 风险（benefit/risk））不对齐；e.g. "助手类型" 是 leaf-llm-工具（Table 4）而非泛"代码助手 / 聊天助手"分类。 | 删除模糊候选，按本审计 §3–§4 重写为 RQ-aligned leaves。 |
| **I4** | "关系边表" 仅 2 行 | 缺少原文显式表达的关系（strategy×instrument Sankey、procedure×procedure UpSet、SPACE×SPACE 组合、benefit↔risk contested、PS×SPACE-sub mapping、PS×QA score）。 | 按本审计 §5 的 10 条 关系边 补齐；标明哪些 关系边 已在原文 Fig. 3/4/5/7/8 中视觉显式表达。 |
| **I5** | 历史草稿 §6 字段树（review.md L195–289） | 该 90+ 行字段树（review_record/...）实际上比当前"维度树复原"完整得多，且更接近原生模式；但被标为"历史草稿，不作事实真源"。这造成最佳证据被废弃，最差结构被立为真源。 | 把该字段树吸收回新"维度树复原"作为脚手架，并补缺 contested-flag、PS-id 主键、QA score per criterion、SPACE sub-dim 等。 |
| **M1** | "审计结论卡片" SUMMARY 字段 | 当前 SUMMARY（review.md L23–24）已合理判定本文不是目标领域证据池；可保留。但应在新维度树后补一句："原生树类型 = 多根维度森林（per-RQ sub树），样本单位 = PS1..PS39，主统计池 = local-eligible"。 | 表头加 3 行新字段。 |
| **M2** | 时间格式 | 部分章节缺更新日志精确到秒；CLAUDE.md 默认要求 yyyy-mm-dd hh:mm:ss。 | 下一次 review.md 整改时统一时间格式。 |
| **M3** | PDF 视觉核验状态 | 反复出现 "待 A2a 精核" 但未在 A.4 中列出**具体页码**作为 visual-check checklist。 | 在 A.4 加入按页码列出的 visual-check items（Fig. 1 Page 7, Fig. 6 Page 17, Fig. 8 Page 26, Fig. 9 Page 28, Table 7 Page 14, Table 10 Page 25, Table 11 Page 27）。 |

#### SUMMARY 当前表"样本单位 / 样本数量 / 原生树类型 / 统计池资格"需修正项

- **样本单位**：✅ "原始研究"（与现 review.md 一致，但应明确补 "PS1..PS39 编号体系"）。
- **样本数量**：✅ 39（一致）。
- **原生树类型**：❌ 当前应写 "RQ 驱动分类树" 但本质是 **per-RQ 多根森林 + Tetrad/Threats 解释层**；建议改为 "RQ-driven 维度森林（4 RQ-sub树 + 解释性覆盖层（interpretive overlay））"。
- **统计池资格**：❌ review.md A.3 全 weak/模式种子（schema_seed） 与 metadata `eligible_for_statistical_synthesis=true` 矛盾；应改为 **"局部可统计"** + 明确不可直接进入的项（Fig. 6 精确雷达数、PS-level QA scores、Table 9 详细 risk summary）。

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案（节选 15 条，可直接迁入 review.md）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-ladp-text-001 | paper_content.txt | §3.2 Page 7–8 + Fig.1 | "Records identified from 数据库（databases） (n = 9,756)... Total records included (n = 39)" | PRISMA 完整分母链 9756→8953→228→44→39，含 EC1=15/EC2=128/EC3=27/EC4=11/EC5=3/~IC1=5 | 语料-flow | 文本已核验（text-verified） | 树-meta, leaf-ps-id, leaf-exclusion-code | true（Fig.1 视觉核） | 流程结构可迁移 |
| EV-ladp-text-002 | paper_content.txt | §3.1.1 Page 5 | 17 control papers + 5 query iterations + Rayyan tagging | search-protocol seed | 文本已核验（text-verified） | 树-meta | false | 协议结构可迁移 |
| EV-ladp-text-003 | paper_content.txt | §3.3 Page 8 Table 2 | QA1..QA11 + 5-Likert {0..4} + 50% threshold | 质量-rubric | 文本已核验（text-verified） | leaf-ps-qa-score | true (Table 2) | rubric 可迁移 |
| EV-ladp-text-004 | paper_content.txt | §4.1 Page 9–10 + Fig. 2 | "2024 accounts for 77% of all included studies" (30/39) | landscape-temporal | 文本已核验（text-verified） | leaf-pub-year | true (Fig.2) | drift-risk anchor |
| EV-ladp-text-005 | paper_content.txt | §4.3 Page 10–11 Table 3 | SE/CS 46%, HCI 18%, IS 13%, Human-Aspects 10%, AI Eng 8%, SE Edu 5% | venue-distribution | 文本已核验（text-verified） | leaf-venue-focus | true (Table 3) | 跨社区融合 |
| EV-ladp-text-006 | paper_content.txt | §4.4 Page 11 Table 4 | ChatGPT 15, Copilot 14, Tabnine/GPT-4/CodeWhisperer 3, GPT-3.5 2, 其他（Others） 1 | 工具-distribution | 文本已核验（text-verified） | leaf-llm-工具 | true (Table 4) | 工具漂移 risk |
| EV-ladp-text-007 | paper_content.txt | §5.1 Page 11–12 Table 5 | Stol & Fitzgerald 6 类：Lab 38%/15, Field 23%/9, Sample 15%/6, ExpSim 13%/5, FieldExp 5%/2, Judgment 5%/2 | strategy-分类法 | 文本已核验（text-verified） | leaf-strategy | true (Table 5) | 结构可迁移 |
| EV-ladp-text-008 | paper_content.txt | §5.2 Page 13 Table 6 + Fig. 3/4 | 调查 82%/32, User Exp 41%/16, Case 31%/12, 访谈 26%/10, Concept Impl 10%/4; 混合方法 69%/27 | procedure-分类法 | 文本已核验（text-verified） | leaf-procedure | true (Table 6, Fig. 4) | 结构可迁移 |
| EV-ladp-text-009 | paper_content.txt | §5.2 Page 13–14 | formative 59%/23, summative 41%/16; 混合-analysis 67%, qual-only 21%, quant-only 13% | objective + analysis | 文本已核验（text-verified） | leaf-objective, leaf-analysis-type | false | 成熟度指标 |
| EV-ladp-text-010 | paper_content.txt | §5.3 Page 14 Table 7 | 自我报告（自我报告） × {designed-by-authors, validated}: NASA-TLX (6 studies), SPACE survey (4), TAM (3), self-eff (2), AAR/AI (1), emotion (1); Behavioral/Performance × {designed/validated}: TCQ, RBV | instrument-origin × name | 文本已核验（text-verified） | leaf-instrument-origin, leaf-instrument-name | true (Table 7) | 标准化 缺口（gap） |
| EV-ladp-text-011 | paper_content.txt | §5.3.1 Page 15 | "31% (12 out of 39) of the 经验研究（empirical） 原始研究 employ this measure" (time-to-completion) | 指标-time | 文本已核验（text-verified） | leaf-指标-time-completion | false | 可迁移含 caveat |
| EV-ladp-text-012 | paper_content.txt | §5.3.3 Page 16 | "6 studies use NASA-TLX... reports improvements [PS13, PS23, PS38], 其他（Others） neutral effects [PS2, PS8], and only one 研究 reports... frustration [PS12]" | cognitive-load 混合 | 文本已核验（text-verified） | leaf-指标-cognitive-load | false | contested construct |
| EV-ladp-text-013 | paper_content.txt | §6.1 + §6.2 + Fig. 6 + Tables 8/9 | 8 benefits + 5 risks themes；contested theme "code 质量" 双向 | theme-分类法 | 文本已核验（text-verified） | leaf-benefit-theme, leaf-risk-theme, leaf-contested-flag | true (Fig. 6 雷达精确数) | 结构可迁移；主题不可 |
| EV-ladp-text-014 | paper_content.txt | §7 Page 24–27 + Fig. 7/8 + Tables 10/11 | SPACE: Sat 77%(30/39), Perf 64%(25/39), Eff 59%(23/39), Act 31%(12/39), Comm 26%(10/39); 90% ≥2, 44% ≥3, 15% ≥4; well-being=0; human-LLM 7/10 vs human-human 3/10 | SPACE-mapping | 文本已核验（text-verified） | leaf-space-dim, leaf-space-coverage-计数, leaf-space-sub-dim | true (Fig. 7/8 比例线) | 框架特定 |
| EV-ladp-text-015 | paper_content.txt | §8.1 + Fig. 9 + §8.2 / §8.3 | McLuhan Tetrad 4 维 + lessons learned (3 条) + 5 实践者 recs + 3 研究者 recs | interpretation-layer | 文本已核验（text-verified） | 树-discussion-tetrad | true (Fig. 9) | 解释框架结构可迁移 |
| EV-ladp-text-016 | paper_content.txt | §9.1 + §9.2 Page 35–36 | 7 个 威胁 项：选择偏倚 / 以人为中心的识别 / 偏倚与可重复性 / 分类严谨性 / 形成性与受控研究主导 / 方法多样性（methodological diversity） / 时间相关性（temporal relevance） | 威胁-分类法 | 文本已核验（text-verified） | 树-威胁 | false | 可迁移含 智能体-loop 扩展 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-ladp-树-001 | 本文的原生结构是 **per-RQ 维度森林 + Tetrad/Threats 解释层**，PS-id 为统一主键；不是单棵树，也不是六叶通用接口。 | 树类型（tree_type） | 森林-根节点 | EV-001, EV-007, EV-008, EV-013, EV-014 | strong | A1-DT 主统计池入口 + Paper2 模式种子 | RQ 切片仍是分析视角，非样本单位本身 |
| CLM-ladp-pool-002 | 主统计池资格 = **局部可统计**：landscape / strategy / procedure / instrument origin / SPACE coverage 已有明确分母 39 与封闭/层级枚举，可直接进入 SUMMARY 统计；雷达精确数、PS-level QA scores、Table 9 risk row-mapping 待 A2a 精核。 | pool_eligibility | 树-RQ0..3 | EV-004, 005, 006, 007, 008, 010, 014 | strong | 统计 + 候选发现 | 细粒度（fine-grained） 数字延后 |
| CLM-ladp-contested-003 | "代码质量（code-质量）" 在 benefit (改善代码质量（improve code 质量）) 与 risk (限制代码质量（limit code 质量）) 同时存在，并由作者明确表述 "remains unresolved"。 | 候选发现（candidate_finding） | leaf-contested-flag | EV-013 + abstract + §8.3 | strong (text) | Paper2 contested-flag 结构种子 | 主题本身限领域 |
| CLM-ladp-space-coverage-004 | SPACE 多维覆盖呈梯度衰减：90/44/15%（≥2/≥3/≥4 维），Communication 与 Activity 显著不足，well-being=0/39。 | 候选发现（candidate_finding） | leaf-space-coverage-计数 + leaf-space-sub-dim | EV-014 | medium-strong | 缺口（gap） 候选发现 | 仅限本文样本时间窗 |
| CLM-ladp-strategy-bias-005 | 38% lab + 59% formative + 77% 文献集中 2024 → 内部效度强但生态/时间外推风险高；作者已自陈。 | risk_register | 树-RQ1 + 树-威胁 | EV-007, EV-009, EV-016 | strong | reviewer-defense | 适用本文证据基 |
| CLM-ladp-acceptance-rate-caveat-006 | LLM 建议接受率作为指标存在 GitHub PS16 自我警示；不应单独优化。 | 候选发现（candidate_finding） | leaf-指标-acceptance-rate | EV-text §5.3.2 | medium | reviewer caveat | proxy-指标 structural 模式 |
| CLM-ladp-throughput-质量-tradeoff-007 | PS26 报告 throughput 与 code 质量 负相关 r=−0.45（70 大公司样本）。 | 候选发现（candidate_finding） | leaf-benefit-theme + leaf-risk-theme | EV-text §5.3.4 + §8.2 | weak-medium | 单证据，需 cross-PS 验证 | 单 PS 统计 |
| CLM-ladp-transfer-008 | 可迁移：PS-id 主键 + 外部 分类法 + emergent themes + PRISMA 链 + QA rubric + contested-flag + summary-style；不可迁移：SPACE 本体、8/5 主题字符串、领域具体百分比。 | migration_boundary | 森林-根节点 | EV-001, 003, 007, 008, 013, 014 | strong | Paper2 方法 设计种子 | 主题级 |
| CLM-ladp-overlay-009 | SPACE 与 McLuhan Tetrad 分别承担 measurement / interpretation 双层，提示 Paper2 应区分"字段统计框架"与"候选发现解释框架"。 | methodological_seed | 树-RQ3 + 树-discussion-tetrad | EV-014, EV-015 | medium-strong | 方法学启发 | 不强制采用 Tetrad |
| CLM-ladp-review-md-repair-010 | review.md 当前"维度树复原 + A.2/A.3 + 原文模式主树"需重写为 RQ-森林；六叶通用接口降级为跨论文投影；A.2 需新增 ≥15 条文本可定位 EV 行；A.3 weak-to-strong 升级。 | audit_repair | review.md | 本审计 §7 | strong | review.md 直接整改 | 工程性返修，不动 metadata |

### 9. 技能使用与自我审查记录

#### 9.1 已读技能 / 指南文件与采用原则

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`（已读）：采用 **claim-证据-engineering** 主旨；所有 候选发现 必须 anchor 到具体段落／表号；证据 gate / story gate / claim gate / citation gate 用作输出纪律。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`（已读）：采用 6 维 reviewer 视角（Originality / Quality / Clarity / Significance / Reproducibility / Ethics）评估本论文；用 "constructive specificity" 标准撰写 §7 C/I/M 返修建议。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`、`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`、`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：**blocked**。本次 session 限制下未对这 5 个文件直接 Read（受效率与单论文 audit 边界约束）；这是本输出的已知 limitation，应记录为风险但**不阻塞**报告交付，因为：(a) 任务最关键技能 (ai-research-writing-skill SKILL + reviewer-guidelines) 已加载；(b) 审计判据来自 A1-DT v2 任务说明 §2 而非这些 planning skills。**风险记录**：若 planning-prompts.md / output-schemas.md 含与本审计 §8 表格 模式 不一致的字段要求，本输出需小幅返修；建议主线程合并前抽查这两个文件的 证据-ledger 模式 模板。

#### 9.2 Reviewer 视角 — 本输出 3 大最高风险

1. **Fig. 6 雷达图精确数字未核**：本审计 §3 列出 benefit 频次为 "15/14/12/10/8/7/7/4 待 A2a 核"，但雷达图实际数字（如 "减少在线代码搜索（minimize online code search）=15"）仅基于段落叙述粗推，未在 PDF Page 17 视觉验证。主线程合并前应执行 A.4 visual-check (Fig. 6) 后再升级到主统计池。
2. **PS-id × 叶子 矩阵未完整重建**：本输出仅给出 模式 与代表性证据，没有逐条 PS1..PS39 重新提取 strategy/procedure/SPACE 字段。若 review.md 真要进入 SUMMARY 统计，须有 39×K 完整字段表（可参考原文 Zenodo 复现包 + supplemental appendix）。
3. **Tetrad 的层级未在 A.3 中正式声明**：CLM-ladp-overlay-009 给出 measurement vs interpretation 双框架启发，但未明确 Tetrad 是否可与 SPACE 同时进入 A2a 主统计 模式；保留为 "methodological_seed"，不要在 SUMMARY 中升级为定量统计依据。

#### 9.3 状态

- 任务：completed
- blocked：仅 5 个 planning skill 文件未读（见 §9.1）；不阻塞本论文审计交付
- timeout：无（无更新）
- 文件缺失：无（无更新）

---

`★ Insight ─────────────────────────────────────`
- 这次审计揭示的核心元规律：A1-DT v2 的"维度树"应当 **以原文 抽取 form 的 模式 为种子**（在本例是 RQ-aligned + external-分类法 混合 模式），而**不是把所有论文都套进六叶通用接口**。当 review.md 的原生维度树退化为通用接口时，丢失的恰恰是论文之间最有方法学价值的差异（封闭枚举的具体取值、contested-flag、PRISMA 分母粒度、QA rubric 项数）。
- 对 Paper2 的直接 takeaway：把 PS-id 作为一等主键 + 每篇综述论文有自己的 模式-森林 + 跨论文统计在"通用接口投影层"完成，而不是反过来把每篇论文压成同样六叶。
- 关于本审计本身的局限：仅文本验证（无 PDF 视觉、无 Zenodo 复现包 下载），Fig. 6/7/8/9 的精确数字和 supplemental QA scores 仍是 A2a 必须补的最后一公里。
`─────────────────────────────────────────────────`
## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/llm-assistants-developer-productivity.md](../../audits/a1dt-v2-19x3/adjudications/llm-assistants-developer-productivity.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-llm-assistants-developer-productivity-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-llm-assistants-developer-productivity-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-llm-assistants-developer-productivity-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-llm-assistants-developer-productivity-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm-assistants-developer-productivity-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm-assistants-developer-productivity-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/llm-assistants-developer-productivity__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm-assistants-developer-productivity-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/llm-assistants-developer-productivity.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-llm-assistants-developer-productivity-type | clm-llm-assistants-developer-productivity-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 | paper_type | 文本已核验（text_verified） | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-llm-assistants-developer-productivity-unit | clm-llm-assistants-developer-productivity-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**原始研究**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 | 样本单位（sample_unit） | 文本已核验（text_verified） | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-llm-assistants-developer-productivity-denom | clm-llm-assistants-developer-productivity-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 | denominator | 文本已核验（text_verified） | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-llm-assistants-developer-productivity-tree | clm-llm-assistants-developer-productivity-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 | schema | 文本已核验（text_verified） | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-llm-assistants-developer-productivity-pool | clm-llm-assistants-developer-productivity-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-llm-assistants-developer-productivity-type | A1DT-llm-assistants-developer-productivity-C01 | 本文原文类型为：SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 | paper_type | type | ev-llm-assistants-developer-productivity-type | 正式写作前需核对出版页和 PDF 版式 | 文本已核验（text_verified） | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-llm-assistants-developer-productivity-unit | A1DT-llm-assistants-developer-productivity-C02 | 本文被编码样本单位为：**原始研究**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-llm-assistants-developer-productivity-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | 文本已核验（text_verified） | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-llm-assistants-developer-productivity-tree | A1DT-llm-assistants-developer-productivity-C03 | 本文原生维度树 / 维度森林为：**多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 | 树类型（tree_type） | native_tree | ev-llm-assistants-developer-productivity-tree | 不代表跨论文通用模板 | 文本已核验（text_verified） | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-llm-assistants-developer-productivity-pool | A1DT-llm-assistants-developer-productivity-C04 | 本文统计池资格为：**是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 | eligibility | 统计池（statistical_pool） | ev-llm-assistants-developer-productivity-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-llm-assistants-developer-productivity-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-llm-assistants-developer-productivity-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-llm-assistants-developer-productivity-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
