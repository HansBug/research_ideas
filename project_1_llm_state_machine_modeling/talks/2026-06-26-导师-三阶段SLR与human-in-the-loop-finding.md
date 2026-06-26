# 2026-06-24/26 导师讨论：三阶段 SLR、维度 pattern 与 human-in-the-loop finding 形成

## 1. 执行摘要

本记录沉淀 2026-06-24 至 2026-06-26 围绕第二篇论文 paper2 / agentic-SLR 的正式导师讨论、PR [#123](https://github.com/HansBug/research_ideas/pull/123) body、PR comment 与会后消化结果。它在 2026-06-15 记录 [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md) 的基础上进一步明确：第二篇论文不应写成“LLM/agent 自动完成 SLR”，而应聚焦 **researcher-guided、pattern-evolving、evidence-backed、finding-oriented** 的 agentic SLR 支持方法。

本轮讨论把真实 SLR 实践拆成三个相互迭代的层次：

1. **论文收集与初步处理**：检索、去重、初筛、全文状态记录、overview card 等高劳动量、低创造性的工作。
2. **维度 pattern 驱动的论文分析**：由 researcher 基于研究主题和 meta-model 设定可执行维度 pattern，再由 agent 辅助抽取字段级证据，形成可比较、可统计、可审计的文献信息表。
3. **统计分析与 research finding 形成**：先基于字段表做统计分析，再在 finding pattern / heuristics 引导下提出 candidate finding signals，最终由 researcher 通过 evidence chain、反例搜索、claim strength 降级和 challenge / adjudication 做最终裁决。

最新一句话 story 建议为：

> 第二篇论文研究一种面向 SE SLR/SMS 的 **researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach**：researcher 定义研究主题、RQ、scope 与 meta-model，LLM/agent 从 survey-of-surveys scaffold 与 seed papers 中提出候选 dimension / finding patterns，在 researcher-approved schema 下抽取字段级内容证据、生成统计视图和 candidate finding signals；final target-domain findings 必须经过 researcher challenge、反例搜索、补证、必要降级和最终裁决，同时保留 process evidence / audit trail 以支持方法评估。

本记录严格区分两类来源：

- **【正式定调 / 高置信导师意见理解】**：导师明确表达或用户会后确认的方向，后续 paper2 story、method、outline、evaluation 应优先遵守。
- **【AI 衍生建议 / 执行化推导 / 待确认】**：主 session 与 reviewer 基于导师意见、PR #123 body/comment 与 baseline 调研推导出的执行路径，可作为后续 PR 默认起点，但不得伪装成导师原话。

---

## 2. 讨论背景与上游材料

### 2.1 上游上下文

PR [#101](https://github.com/HansBug/research_ideas/pull/101) 是 paper2 的伞 PR；PR [#105](https://github.com/HansBug/research_ideas/pull/105) 的 baseline 调研表明，LLM / agent 辅助 SLR、自动综述生成、evidence synthesis、HITL provenance 等方向已有大量近邻，因此 paper2 不能继续使用“first LLM SLR / first agentic SLR / 自动化完整 SLR”之类叙事。PR [#112](https://github.com/HansBug/research_ideas/pull/112) 已经确认 meta-model 应由使用者 researcher 基于 scaffold 实例化，agent 只提出 candidate finding signals，final findings 需要 evidence chain + researcher audit。PR [#114](https://github.com/HansBug/research_ideas/pull/114) 进一步将 schema approval gate、candidate/final finding 边界、researcher challenge loop 与“透明审计材料不等于自动写论文”写入 S0 story 草案。

在上述基础上，PR [#123](https://github.com/HansBug/research_ideas/pull/123) 作为 S0B 导师讨论材料 subPR，进一步把 paper2 的方法主线从“发现导向 SLR”落到真实 SLR 工作过程：**收集论文 → 分析论文 → 统计分析与形成 research findings**，并在 PR comment [#123 comment 4806613777](https://github.com/HansBug/research_ideas/pull/123#issuecomment-4806613777) 中补充了最新导师意见消化。

### 2.2 关键上游材料

| 类型 | 链接 | 用途 |
|---|---|---|
| paper2 伞 PR | [PR #101](https://github.com/HansBug/research_ideas/pull/101) | 第二篇论文总控入口。 |
| baseline 调研 PR | [PR #105](https://github.com/HansBug/research_ideas/pull/105) | 证明已有近邻很多，不能主打“自动化 SLR firstness”。 |
| S0-pre 导师讨论材料 | [PR #112](https://github.com/HansBug/research_ideas/pull/112) | 确认 meta-model 由 researcher 设定、agent 只产出 candidate finding signals、final finding 需要 evidence chain + researcher audit。 |
| S0 story 草案 | [PR #114](https://github.com/HansBug/research_ideas/pull/114) | 已把 schema approval gate、candidate/final finding、challenge loop 等写入 S0 story；本记录与其互相校准。 |
| S0B 三阶段 SLR 讨论 PR | [PR #123](https://github.com/HansBug/research_ideas/pull/123) | 本记录主要归档对象，PR body 是发给导师过目的自包含材料。 |
| PR #123 最新长 comment | [#123 comment 4806613777](https://github.com/HansBug/research_ideas/pull/123#issuecomment-4806613777) | 记录最新导师意见消化与执行化理解。 |
| project_1 正式导师讨论库 | [README.md](./README.md) / [GUIDE.md](./GUIDE.md) / [SUMMARY.md](./SUMMARY.md) | 本记录归档入口与维护规则。 |
| 2026-06-15 正式导师讨论记录 | [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md) | 本轮讨论的直接前置记录。 |
| agentic-SLR baseline 文库 | [../paper_agent_based_slr/baselines/SUMMARY.md](../paper_agent_based_slr/baselines/SUMMARY.md) | 后续差异化与 related work 的主要证据入口。 |

### 2.3 与 SE SLR/SMS 基础方法的关系

本轮讨论并不否定 SE 二级研究中的既有基本规范。Kitchenham 与 Charters 的 SE SLR 指南强调，系统综述通常包括 planning、conducting、reporting 等阶段，并以可审计方法识别、分析和解释研究问题相关证据 [1]；Petersen 等关于 systematic mapping studies 的工作强调通过分类 scheme、keywording、data extraction 和 mapping 来获得研究领域结构化图景 [2]。本轮导师讨论的“收集论文 → 分析论文 → 统计与 finding”并不是替代这些经典过程，而是把 agentic 支持方法要处理的关键认知与证据问题重新显式化：**谁定义研究问题和 schema，如何演化维度 pattern，如何让字段级证据和 finding 级证据可审计，以及 researcher 如何参与最终裁决**。

---

## 3. 原话记录与来源等级 ledger

### 3.1 2026-06-24 前后关于三阶段 SLR 的原话整理

> 关于 paper2 的 agentic-SLR 这边，我和导师讨论了一下，目前有这些思考：
>
> 1. 实际上我们一般来做 SLR 的时候，基本上是三步走：
>    1. 第一阶段，收集论文，要的就是大量搜集到论文 + 初步处理 + 初步阅读把概要等一些信息抽取出来；这一阶段纯粹的苦力活，没啥技术含量。
>    2. 第二阶段，分析论文，要的是建立一些特定的维度 pattern，然后针对这些维度来一个一个论文提取这些定向的信息，然后整理成一个足够 reasonable 的文献信息表格。
>       1. 维度 pattern，以 LLM STM generation 为例，就包括输入、输出、所使用的方法、agent 使用程度、所用的 LLM、输入的 NL 类型，输出的 NL 类型，甚至可以包含是否公开了数据集、是否公开了源码这些信息。
>       2. pattern 很多时候在 SLR 初建立的时候是很难建立得很周全的，一般都得随着所阅读文献的越来越多，对这个领域的理解越深入，不断完善并且最终形成一套真正全面的 pattern 出来。
>       3. 但是对于一个特定的领域而言，pattern 也总归是有迹可循的，因此应当去建立 survey of surveys，就去看软工领域近年的 survey 论文来摸透一般的规律。
>       4. 这部分也有个问题，就是对于每一篇论文提取出来的上述信息，如何证明这个信息是可靠的？难不成靠人去挨个 review 吗？如果真要那样的话就毫无意义了，还不如直接人工。因此正确做法是在提取这些信息的时候就保存充分的经得起审计的证据链条，之前所说的证据链思路也就体现在这里。
>    3. 第三阶段，基于第二阶段的这部分数据，进行统计分析，然后针对这个分析结果来归纳现状，乃至发现新的学术问题。这也是真正最厉害最灵魂性的地方，是真正最大的重点所在。
> 2. 因此 agentic SLR 也得立足于这几点。
> 3. 还有一个很重要的点在于，这部分不应该追求随意地无人化，而是应当让人类在这一系列环节中扮演重要角色且让 AI 真的能帮助到人，这也才是 LLM 辅助研究的重点所在，而不是让人类直接缺位。
> 4. 维度 pattern 基于 LLM 自动生成也是个不错的思路，可以考虑这样多个方向。

### 3.2 2026-06-26 最新导师意见原话整理

> 感觉把统计分析与 research finding 分开更好理解，因为统计分析基本属于按照规定的分析方法，在抽取的字段级证据中形成归纳性质的观察；而 research finding 强调具有开放性的洞察分析，可以给定一些启发（heuristics）。
>
> 至于 survey-of-surveys，我倒是觉得可以范围放宽一些，从中识别和提取 dimension pattern 是个低复杂度工作。
>
> 建议给出整个方法的流程图，强调 human in the loop，人与 LLM 协同，在流程图中要体现出来，这就是 approach。
>
> 然后你自己先设定一个主题，跑一遍方法看看效果。
>
> 后续让硕士生都是用这套方法来做实验，收集实验过程数据，特别是人与 LLM 的交互数据。

### 3.3 来源等级 ledger

| 条目 | 来源等级 | 本记录处理方式 |
|---|---|---|
| SLR 可按“收集论文 / 分析论文 / 统计与 finding”理解；agentic SLR 应立足这些真实环节。 | 【正式定调 / 用户会后确认】 | 作为 S0B 方法 story 的基础结构。 |
| 第二阶段核心不是摘要，而是建立并演化 dimension pattern，把论文读成可比较表格。 | 【正式定调 / 用户会后确认】 | 写入方法 L2：dimension pattern evolution + field-level evidence extraction。 |
| dimension pattern 初期不完整，应随阅读和理解深化持续修订。 | 【正式定调 / 用户会后确认】 | 写入 pattern lifecycle、schema version、backfill 与 stability 条件。 |
| 抽取字段必须保存经得起审计的证据链，否则人工复核成本会抵消 agentic SLR 意义。 | 【正式定调 / 用户会后确认】 | 写入 content evidence / field-level evidence 默认产物。 |
| 统计分析与 research finding 要分开。 | 【正式定调 / 导师原话】 | 写入 L3 的两个 sub-stage，并区分 statistical analysis、target-domain finding、method-evaluation finding。 |
| research finding 可由 finding pattern / heuristics 引导。 | 【正式定调 / 导师原话】 | 写入 finding pattern scaffold；LLM 只产出 candidate finding signals。 |
| survey-of-surveys 范围可放宽，用于识别 dimension pattern，是低复杂度工作。 | 【正式定调 / 导师原话】 | 作为 scaffold mining 的直接动机。 |
| survey-of-surveys 的输出可扩展为 finding pattern / evidence-presentation pattern library，但不进入目标 SLR findings evidence pool，也不得写成 PRISMA 式 tertiary review。 | 【AI 衍生建议 / 执行化推导】 | 作为 survey-of-surveys 子 PR 的边界。 |
| 方法流程图要体现 human-in-the-loop 与人-LLM 协同，这就是 approach。 | 【正式定调 / 导师原话】 | 后续 S0 / method figure 必须在多个 gate 呈现 researcher decision。 |
| 自己先设定主题跑一遍方法看效果。 | 【正式定调 / 导师原话】 | 作为 pilot run 的直接来源。 |
| 后续让硕士生使用方法，收集实验过程数据，尤其是人-LLM 交互数据。 | 【正式定调 / 导师原话】 | 作为后续 multi-user method evaluation 的直接动机。 |
| 硕士生过程数据应被定位为 method-evaluation process data，并提前处理 consent、匿名化、prompt/raw log 脱敏、教学关系隔离和数据使用范围。 | 【AI 衍生建议 / 风险控制】 | 作为后续 evaluation protocol 与 ethics/data boundary 的设计要求。 |
| 四层 L0--L3 方法结构、两类 evidence、三类 finding、gate contract。 | 【AI 衍生建议 / 执行化推导】 | 作为后续 S0 / method PR 的默认起点，仍可按导师后续反馈调整。 |

---

## 4. 关键定义与术语

| 术语 | 定义类型 | 本记录口径 | 与相邻概念的区别 |
|---|---|---|---|
| SLR / Systematic Literature Review / 系统文献综述 | 领域已有定义 [1] | 围绕明确研究问题，以系统、可审计方式识别、分析、综合相关研究证据的二级研究方法。 | 本文不重新定义 SLR，只研究 LLM/agent 如何支持其中的 pattern、evidence 和 finding 形成过程。 |
| SMS / Systematic Mapping Study / 系统映射研究 | 领域已有定义 [2] | 通过分类 scheme / mapping process 获得领域结构、主题分布和研究空白的二级研究方法。 | 更强调广度、分类和 map；本 work 可覆盖 SLR/SMS 场景，但正式实验 scope 需限定。 |
| researcher-defined meta-model | 本研究工作口径 | 由使用该 work 的 researcher 基于 RQ、scope 和领域关注点定义的研究对象、关系、证据类型与字段语义。 | 不是由 LLM、survey-of-surveys 或 seed papers 自动决定；也不是作者预先固定的一套 universal SE ontology。 |
| dimension schema / extraction dimension pattern | 本研究工作口径 | meta-model 在单篇论文抽取任务上的可执行字段化投影，包括字段、取值空间、证据要求、缺失值处理和修订历史。 | 它是 L2 论文分析层中心制品，不是全方法唯一中心；必须经 researcher approval。 |
| survey-of-surveys scaffold | 本研究工作口径 | 从既有 SE survey / SLR / SMS 中低成本提取常见 dimension pattern、finding pattern 和证据呈现方式，形成 pattern prior / scaffold。 | 不进入目标 SLR 的 findings evidence pool；不得声称完成 PRISMA 式 tertiary review 或覆盖全部 SE surveys。 |
| seed papers | 本研究工作口径 | 用于 schema feasibility probing / stress test 的少量种子论文。 | 不代表完整 corpus 结论，也不自动决定 meta-model。 |
| content evidence / field-level evidence | 本研究工作口径 | 来自目标论文原文的证据，例如 source anchor、表格/图、section/page、引用片段、artifact URL、缺失原因和不确定说明。 | 支撑字段值、统计分析和 target-domain findings；不同于 process evidence。 |
| process evidence / audit trail | 本研究工作口径 | 来自 schema revision、人机交互、challenge、adjudication、backfill 的过程记录。 | 支撑方法可审计性与 method-evaluation findings，不能替代目标领域文献证据。 |
| statistical analysis | 本研究工作口径 | 基于字段表形成的描述性/归纳性分析，如频次、分布、交叉表、趋势、覆盖率。 | 不能直接等同于 research finding；若作为 claim 必须转写为有解释边界和证据链的主张。 |
| target-domain research finding | 本研究工作口径 | 基于目标论文 corpus 的字段级内容证据、统计分析、反例和 researcher 解释形成的研究主张。 | 与 method-evaluation finding 区分；前者回答目标领域状态与问题。 |
| method-evaluation finding | 本研究工作口径 | 基于 pilot run 和 student process data 形成的关于方法本身可用性、审计性、人机协同成本和失败模式的发现。 | 不能作为目标领域 SLR finding 的文献证据。 |
| candidate finding signal | 本研究工作口径 | LLM/agent 基于 statistical analysis 与 finding heuristics 提出的候选 finding 线索。 | 不是 final finding；必须经 researcher challenge / evidence audit / adjudication。 |
| final finding | 本研究工作口径 | 经过 researcher 接受其 claim strength、scope、supporting evidence 与 counter-evidence 检查后的 finding。 | 不能由 LLM 直接生成；必须留有 evidence chain 与裁决记录。 |
| human gate / auditable decision point | 本研究工作口径 | 带 input artifact、decision type、rationale、versioned change、impact scope、downstream action 的人工决策点。 | 不是简单 sign-off；包括 approve / revise / reject / downgrade 等动作。 |

---

## 5. 从 PR #123 body 到最新 story 的自然演化

### 5.1 PR #123 body 的核心内容

PR #123 body 已经形成以下主线：

1. 论文收集层是必要基础，但不是 paper2 的主要学术 novelty；已有 LLM workflow 很容易覆盖检索、初筛、摘要等任务。
2. 论文分析层的中心是 **维度 pattern**，不是普通摘要；它应表现为树状、带类型、可修订的 schema / taxonomy tree。
3. 以 LLM-based state-machine generation / LLM4Modeling 为 running example，维度 pattern 可以覆盖输入材料类型、输出 STM 谱系、方法与 LLM/agent 使用方式、评价与证据、复现资产、失败模式和 evidence anchor 等。
4. 第三阶段需要从结构化字段表中生成统计、趋势、矛盾、gap、maturity 等研究线索。
5. paper2 应避开 “first / automated SLR / auto survey writing” claim，转向 researcher-guided、pattern-evolving、evidence-backed、finding-oriented 口径。

### 5.2 树状 LLM4STM 维度 pattern 的意义

PR #123 中新增的 `LLM4STM generation extraction dimension pattern` 示例非常重要，因为它把“维度 pattern”从平铺字段表升级为可维护的 typed schema。其主要结构包括：

| 子树 | 代表字段 | 作用 |
|---|---|---|
| 研究任务与输入 | 输入材料类型、输入 NL 谱系、输入结构化程度、领域与系统类型 | 区分不同 LLM4Modeling / LLM4STM 问题设置。 |
| 输出 STM 谱系 | UML/SysML/DSL/timed automata/FSA/statechart/code-level state machine，flat/hierarchical/concurrent，state/transition/event/guard/action/variable/invariant/clock 等 | 避免把所有“状态机输出”混成一个类别。 |
| 方法与 LLM/agent 使用方式 | LLM 类型、调用策略、agent 组织程度、外部工具、运行配置 | 区分 prompt-only、RAG、tool-augmented、verifier-guided、planner-executor、critic-reviewer、多 agent 协作等。 |
| 评价与证据 | gold reference、语法/语义/完整性/guard/action/timing/trace/human judgement、parser/simulation/model checking、dataset/code/prompt/raw output | 支撑后续 finding 对“评价成熟度 / 复现性 / evidence weakness”的分析。 |
| 横切证据与结论字段 | 适用范围、失败模式、evidence anchor、missing / uncertainty | 把字段抽取与证据链、缺失值、不确定性绑定。 |

【正式定调】这类维度 pattern 应随着阅读更多论文而演化，不应假定初始版本一次性覆盖完整领域。

【AI 衍生建议】后续可把该 running example 用作 pilot run 的候选主题，检查 pattern versioning、backfill、evidence anchor 和 finding generation 是否能闭环。

### 5.3 最新 comment 对 PR body 的补充

PR #123 最新 comment 将 body 中“三阶段 SLR”进一步操作化为四层闭环：

| 层次 | 作用 | 关键 gate |
|---|---|---|
| L0 研究主题与 meta-model 设定 | researcher 定义 topic、RQ、scope、核心概念和证据规则 | meta-model approval |
| L1 文献收集与初步处理 | agent 支持检索、去重、初筛、全文状态、overview card | screening audit |
| L2 维度 pattern 演化与字段级证据抽取 | researcher 批准 dimension schema，agent 抽取 field-level content evidence | pattern approval + field evidence audit |
| L3 统计分析与 research finding 形成 | agent 生成统计视图与 candidate finding signals，researcher challenge / adjudicate | analysis protocol check + finding adjudication |

这四层不是线性流水线，而是 logical layers；L2 schema revision 可以回流触发 L1 补检索或 L2 backfill。

---

## 6. 最新方法主线：四层闭环与 human-in-the-loop

### 6.1 方法洞察

【正式定调】这篇工作不应追求 end-to-end autonomous SLR，而应强调 human-in-the-loop，让 researcher 在一系列关键环节中扮演重要角色，LLM / agent 的价值是帮助 researcher 而不是替代 researcher。

【AI 衍生建议】因此，真正需要 agentic 化的不是“让 AI 从头到尾自动写综述”，而是：

> 把 researcher 在 SLR 中反复做的关键判断显式化、结构化、可审计化：哪些论文进入池子，哪些 dimension pattern 能描述这个领域，每个字段的证据是否可靠，哪些统计现象足以升级为 target-domain research finding，以及 researcher 如何围绕 finding 质疑、补证、找反例和裁决。

### 6.2 四层方法表

| 层次 | 主要问题 | researcher 角色 | LLM / agent 角色 | 关键产物 | 关键 gate |
|---|---|---|---|---|---|
| L0 研究主题与 meta-model 设定 | 这篇 SLR/SMS 要回答什么领域问题？哪些对象、关系、证据类型重要？ | 定义 topic、RQ、scope、核心概念、证据要求 | 提供候选拆解、术语归纳、近邻线索 | researcher-defined meta-model、scope、RQ、初始证据规则 | meta-model approval |
| L1 文献收集与初步处理 | 候选论文池是否足够系统、可追溯？ | 批准检索协议、抽查筛选质量 | 检索、去重、初筛、全文状态记录、overview card | search log、screening table、paper pool、overview cards | screening audit |
| L2 维度 pattern 演化与字段级证据抽取 | 如何把论文读成可比较表格？每个字段是否有内容证据？ | 选择 / 修订 dimension pattern，裁决字段定义和高风险字段 | 从 scaffold 与 seed papers 提出候选维度；按 approved schema 抽取字段并保存 anchors | dimension registry、paper-by-dimension table、field-level evidence objects、schema version log、revision/backfill audit trail | pattern approval + field evidence audit |
| L3 统计分析与 research finding 形成 | 结构化表格中有什么分布？哪些现象能变成研究洞察？ | 确认分析口径，challenge candidate target-domain findings，裁决 final target-domain findings | 生成统计视图，基于 finding heuristics 提出 candidate finding signals，协助补证和反例搜索 | statistical analysis table、candidate finding signal ledger、claim-evidence map、challenge/adjudication audit trail、final target-domain findings | analysis protocol check + finding adjudication |

### 6.3 流程图文本草案

后续 S0 / method PR 应将以下结构转成正式 Mermaid / figure，并进行视觉可读性 review：

```text
Researcher topic / RQ / scope / meta-model
        ↓  human approval
Survey-of-surveys scaffold + seed-paper feasibility probing
        ↓  LLM proposes pattern candidates only; does not define the operative meta-model
Researcher selects / revises / approves executable dimension schema
        ↓
LLM extracts field-level content evidence for each paper
        ↕  human audit / correction / schema revision / backfill
Structured dimension table
        ↓
Statistical analysis: distribution / frequency / cross-tab / coverage
        ↓
LLM proposes candidate finding signals using finding heuristics
        ↕  researcher challenge / counter-evidence search / claim downgrade
Final target-domain findings + evidence chain
        ↓
[Cross-cutting process evidence across all human gates:
 human edits, rejected suggestions, prompts, interaction logs, time cost]
```

### 6.4 Human-in-the-loop 的最低 gate contract

【正式定调】human-in-the-loop 必须体现在流程图和 approach 中，不是最后一个人工审核节点。

【AI 衍生建议】每个 human gate 至少应包含：

| 要素 | 说明 |
|---|---|
| Input artifact | researcher 审核的对象，例如 meta-model、dimension schema、field evidence table、candidate finding signal ledger。 |
| Decision type | approve / revise / reject / downgrade / mark unresolved。 |
| Rationale | 决策理由，尤其是为什么接受或拒绝某个 field / finding。 |
| Versioned change | schema / finding / evidence table 的版本变更。 |
| Impact scope | 哪些论文、字段、统计表或 findings 受影响。 |
| Downstream action | backfill、counter-evidence search、claim revision、补检索或停止。 |
| Gate ID / actor / timestamp | 记录哪个 researcher 在何时对哪个 artifact 做出裁决。 |
| Eligibility consequence | 若必需 gate 缺失，对应 field / analysis / finding 只能标为 tentative / unresolved，不能进入 final finding。 |

---

## 7. 统计分析、target-domain finding 与 method-evaluation finding 的区分

### 7.1 三类输出

| 类型 | 关注点 | 例子 | 如何进入论文 claim |
|---|---|---|---|
| Statistical analysis / 统计分析 | 字段表中的描述性归纳：频次、分布、交叉关系、年份趋势、覆盖率 | “2022--2026 年各年份 agentic-SLR 论文数量分别为 n1/n2/n3；agent workflow 相关字段在 2024 年后占比上升。” | 只是 finding 的证据基础；若要作为 claim，必须转写为有解释边界、证据链和 threat discussion 的主张。 |
| Target-domain research finding / 目标领域研究发现 | 基于目标论文 corpus 的字段级内容证据、统计分析、反例和解释形成的研究主张 | “在当前样本中，agentic workflow 的数量增长快于其评价协议成熟度；多数工作仍缺少 claim-to-source audit、反例检查或过程日志，因此该方向呈现 workflow proliferation 与 evaluation immaturity 的张力。” | 可以作为 candidate finding，但必须经过 challenge、counter-evidence search 与 evidence audit 才能成为 final finding。 |
| Method-evaluation finding / 方法评估发现 | 基于 pilot run 和 student process data 形成的关于方法本身的发现 | “某类字段需要最多人工修订”“某类 LLM suggestion 经常被拒绝”“evidence anchor 降低了复核成本但增加了日志开销”。 | 只能支撑 paper2 对自身方法可用性、审计性、人机协同过程的分析，不能作为目标领域 SLR 的文献证据。 |

### 7.2 Candidate-to-final 最小转移规则

【AI 衍生建议】candidate finding 只有同时满足以下条件，才可转为 final target-domain finding：

1. supporting evidence 已回链到 source anchors；
2. counter-evidence / uncertainty 已被显式检查或标记缺口；
3. scope 与 claim strength 已经 researcher 确认；
4. challenge / adjudication 过程有记录；
5. 如果字段或 pattern 曾经修订，相关论文已完成必要 backfill 或显式标记未完成风险。

否则 finding 必须保留为 `candidate / tentative / unresolved / downgraded` 之一。

---

## 8. 两类 evidence：content evidence 与 process evidence

| Evidence 类型 | 来源 | 支撑什么 | 不能支撑什么 |
|---|---|---|---|
| content evidence / field-level evidence | 目标论文原文、表格、图、artifact URL、source anchor、缺失原因、不确定说明 | 字段值、统计分析、target-domain findings | 方法可用性、人机协同成本、学生使用过程结论 |
| process evidence / audit trail | schema revision、人机交互、prompt/response、人工编辑、challenge、adjudication、backfill、时间成本 | 方法可审计性、method-evaluation findings、human-LLM collaboration 分析 | 目标领域 SLR 的文献证据 |

【正式定调】每篇论文抽取信息必须保存充分证据链，否则需要人工逐篇 review 会抵消 agentic SLR 的意义。

【AI 衍生建议】后续 schema / run record 至少应让每个字段保留 source anchor、抽取 rationale、missing/uncertainty、model output、human correction 与 version 信息；每个 finding 需要 claim-evidence map、support/counter-evidence、challenge/adjudication audit trail。

---

## 9. survey-of-surveys 的新定位

### 9.1 为什么需要 survey-of-surveys

【正式定调】对于一个具体领域，dimension pattern 虽然不可能在 SLR 初期一次性周全设计，但也不是完全无迹可循。可以从近年 SE survey / SLR / SMS 中识别常见 dimension pattern。

【AI 衍生建议】survey-of-surveys 的输出应进入 scaffold / pattern library，而不是目标 SLR 的 findings evidence pool。它的目标是降低 dimension / finding pattern 的冷启动成本，避免 prompt 临场生成或作者拍脑袋固定字段。

### 9.2 可提取内容

| 要归纳的对象 | 示例 | 对 paper2 的作用 |
|---|---|---|
| 常见 RQ 类型 | topic distribution、method taxonomy、evaluation practice、artifact availability、industrial relevance | 帮助设计 finding pattern scaffold。 |
| 常见抽取维度 | input/output、method、dataset、metric、tool、artifact、threats、replicability | 帮助设计 dimension pattern registry。 |
| 表格组织方式 | paper-by-feature matrix、taxonomy table、timeline table、evidence strength table | 帮助定义 paper-by-dimension table。 |
| finding 写法 | gap、trend、consensus、contradiction、maturity、future direction | 帮助定义 candidate finding template。 |
| 证据呈现方式 | source citation、table cell、count、example papers、qualitative quote、threat discussion | 帮助定义 field-level evidence chain 和 finding-level claim-evidence chain。 |

### 9.3 硬边界

1. survey-of-surveys 不是重型 tertiary review；不声称覆盖全部 SE surveys。
2. survey-of-surveys 不进入目标 SLR findings evidence pool。
3. survey-of-surveys 不自动决定 researcher-defined meta-model。
4. 若后续要写成正式方法依据，应记录检索范围、纳入标准、抽取字段和人工审计方式，但规模可先轻量。

---

## 10. 后续验证路线：pilot run 与硕士生过程数据

### 10.1 Pilot run

【正式定调】先由我们自己设定一个主题，跑一遍方法看看效果。

【AI 衍生建议】pilot 的执行化落点是检查 meta-model、dimension schema、field evidence、statistical analysis、candidate finding signals、challenge / adjudication 和 process evidence 是否能形成闭环；这些是执行方案，不是导师原话。

候选主题：

1. **LLM-based state-machine generation / LLM4Modeling**：与 project_1 高度相关，已有 Path-1 / baseline 文库和维度经验；适合检验 input/output/method/agent/evaluation/artifact 等字段。
2. **agentic / LLM-assisted SLR baseline corpus**：B0 已积累一批近邻论文，适合检验 finding pattern 是否能从“近邻压力”中形成清晰差异化判断。

pilot 目标不是立刻产出可投稿 SLR，也不验证跨主题泛化，而是验证：

1. researcher-defined meta-model 是否能写成可执行 schema；
2. survey-of-surveys scaffold 是否真的帮助补充 dimension / finding patterns；
3. LLM 抽取字段级 content evidence 是否可审计、可纠错；
4. pattern evolution 是否记录 version、来源、accept/reject/merge、backfill 范围、修改理由和稳定条件；
5. statistical analysis 与 candidate finding signals 是否能分层输出；
6. challenge / adjudication log 是否支持 claim 降级、补证和找反例；
7. process evidence 是否足够复盘 human-LLM collaboration。

### 10.2 硕士生使用实验

【正式定调】后续让硕士生使用这套方法做实验，收集实验过程数据，特别是人与 LLM 的交互数据。

【AI 衍生建议】这部分数据应被定位为 method-evaluation process data，而不是目标领域文献证据。consent、匿名化、日志脱敏和教学关系隔离等属于风险控制建议，不是导师原话。可收集：

- researcher 如何定义或修改 meta-model；
- 哪些 LLM 建议的 dimension pattern 被接受、拒绝、合并；
- 哪些字段抽取最容易错，如何通过 evidence anchor 纠正；
- 哪些 candidate target-domain findings 被接受、降级或拒绝，理由是什么；
- prompt / response、人工编辑、交互轮次、时间成本、决策理由；
- 不同使用者对同一方法的理解差异；
- 方法文档 / 工具是否足以稳定引导。

### 10.3 伦理与数据边界

若后续收集学生使用数据，应提前定义：

1. consent / 知情同意；
2. 匿名化与身份隔离；
3. prompt / raw log 脱敏；
4. 学生评分 / 教学关系隔离；
5. 数据使用范围与可公开程度；
6. 数据保存位置和访问权限。

---

## 11. 对 paper story、method、outline、evaluation 的影响

### 11.1 Story 影响

【正式定调】paper2 的核心不再是“agent 替人做 SLR”，而是：

> 在 researcher 主导下，把 SLR 中维度模式演化、字段级证据抽取、统计归纳、研究发现形成和人机交互过程都变成显式、可审计、可迭代的研究制品。

### 11.2 候选贡献

> 状态：AI 衍生建议；需后续 S0 / method PR 压缩验证。

1. **Researcher-guided meta-model and dimension pattern scaffolding**：帮助 researcher 将主题、RQ、scope、对象关系和证据要求转化为可执行 schema。
2. **Pattern-evolving paper analysis workflow**：支持 dimension pattern 随阅读演化、版本化、backfill 与稳定化。
3. **Field-level content evidence and finding-level claim-evidence chain**：将字段抽取、统计分析、candidate finding 和 final finding 都绑定到可追溯证据。
4. **Human-in-the-loop challenge / adjudication protocol**：将 researcher 的质疑、补证、找反例、降级和裁决纳入方法闭环。
5. **Method-evaluation process data**：通过 pilot 与多使用者实验分析 human-LLM collaboration 的成本、收益、失败模式和审计性。

### 11.3 候选 outline

1. Introduction
2. Background and Related Work
3. Baseline Pressure and Design Requirements
4. Method: Researcher-guided Pattern-evolving Agentic SLR
5. Implementation / Artifact Schema
6. Pilot Study
7. Multi-user Process Evaluation
8. Discussion and Limitations

### 11.4 Evaluation obligation

| RQ | 问题 | 候选指标 / 人工评估维度 |
|---|---|---|
| RQ1 | researcher-defined meta-model / dimension schema 是否可操作？ | schema completeness、field ambiguity、researcher revision count、backfill burden |
| RQ2 | field-level evidence chain 是否提升抽取可审计性？ | claim-to-source accuracy、unsupported field rate、human correction rate、audit time |
| RQ3 | finding pattern 是否帮助产生有用 candidate finding signals？ | relevance、actionability、evidence-groundedness、non-triviality、finding type coverage |
| RQ4 | challenge / adjudication 如何改变 findings？ | accepted/downgraded/rejected/unresolved rate、counter-evidence found、claim strength changes |
| RQ5 | 多使用者使用过程揭示了哪些方法成本与失败模式？ | interaction turns、time cost、prompt/edit ratio、disagreement、privacy/logging burden |

### 11.5 Claims to make / be careful / avoid

| 类型 | 内容 |
|---|---|
| 可以尝试主张 | researcher-defined meta-model 与 dimension pattern 可以把 SLR 关注点转成 agent 可执行 schema；field-level evidence 与 challenge log 可以提高 finding 形成过程的可审计性。 |
| 谨慎主张 | 方法是否降低重复劳动、提高 finding quality、提升审计性，需要 pilot / process data 支持，不得预设正收益。 |
| 必须避免 | first LLM/agent SLR、完整自动化 SLR、LLM 自动定义可靠 meta-model、PRISMA 合规、替代人工专家、自动产出 final findings。 |

---

## 12. 对后续工作的约束

### 12.1 应做

1. 在后续 S0 / method PR 中补正式方法流程图，突出 human-in-the-loop 与人-LLM 协同。
2. 将 L3 synthesis 拆成 statistical analysis 与 target-domain research finding construction。
3. 建立最小 dimension registry / finding ledger / evidence object / audit trail schema。
4. 设计 lightweight survey-of-surveys / scaffold mining 子任务。
5. 选择一个 pilot 主题跑通方法闭环。
6. 规划硕士生使用实验与 process data 收集协议。
7. 更新 claim-evidence map，明确哪些 claim 需要 pilot / multi-user data 支撑。

### 12.2 暂缓或待确认

1. 不急于实现完整交互式 UI；先冻结 schema、gate、artifact 和最小流程。
2. survey-of-surveys 规模、是否阻塞后续 S0、是否 sampling-based，需后续与导师确认。
3. pilot 主题选 LLM4STM / LLM4Modeling 还是 agentic-SLR baseline corpus，需结合数据可用性和导师偏好决定。
4. 硕士生实验涉及伦理与数据边界，不能只按普通内部实验处理。

### 12.3 不要做

1. 不要把 paper2 写成 end-to-end autonomous SLR。
2. 不要把 LLM 生成的 candidate finding 写成 final finding。
3. 不要把 survey-of-surveys 写成已经完成的 PRISMA 式 tertiary review。
4. 不要把 student process data 当成目标领域文献证据。
5. 不要用“human-in-the-loop”作为末端人工 review 的空泛标签；必须落到多个可审计 gate。

---

## 13. 后续 AI 工作入口

后续 agent 处理 paper2 时应优先读取：

1. 本记录；
2. [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md)；
3. PR [#123](https://github.com/HansBug/research_ideas/pull/123) body 与最新 comment [#123 comment 4806613777](https://github.com/HansBug/research_ideas/pull/123#issuecomment-4806613777)；
4. baseline 文库 [../paper_agent_based_slr/baselines/SUMMARY.md](../paper_agent_based_slr/baselines/SUMMARY.md)；
5. 后续 S0 / method / survey-of-surveys 子 PR。

使用本记录时务必遵守来源等级：**正式定调优先；AI 衍生建议可作为默认起点但可被后续导师意见覆盖；任何候选实验结果都不得写成已完成事实。**

---

## 参考文献

[1] Barbara A. Kitchenham and Stuart Charters. 2007. *Guidelines for Performing Systematic Literature Reviews in Software Engineering*. EBSE Technical Report EBSE-2007-01. URL: https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf

[2] Kai Petersen, Robert Feldt, Shahid Mujtaba, and Michael Mattsson. 2008. *Systematic Mapping Studies in Software Engineering*. Proceedings of the 12th International Conference on Evaluation and Assessment in Software Engineering (EASE 2008), 68--77. DOI: https://dl.acm.org/doi/10.5555/2227115.2227123
