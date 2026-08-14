# 2026-06-15 导师讨论：PR #112 发现导向 SLR 与 meta-model 边界定调

## 1. 执行摘要

本记录沉淀 2026-06-15 与导师围绕 PR [#112](https://github.com/HansBug/research_ideas/pull/112) 的正式讨论结果。讨论前，PR #112 已经把第二篇论文从 `sources` 文库综述 / corpus paper 转向 **SE review meta-model 驱动的证据工作流**；本次导师反馈进一步把主线收敛为：

> **researcher-guided, finding-oriented, auditable agentic SLR support workflow**。

一句话概括最新方向：

> 这篇工作不应把 SLR 机械化为“自动整理文献”，而应让 researcher 先定义 / 裁剪 / 实例化 review meta-model scaffold，再让 LLM / agent 在该框架下提出候选 research findings、建立证据链，并允许 researcher 围绕 finding 继续质疑、补证、找反例和修正。

本记录将导师意见分成两层：

- **【正式定调】**：导师明确表达、且已经被用户会后确认的内容，后续 project_1 story、方法和实验边界应优先遵守。
- **【AI 衍生建议】**：主 session / reviewer 基于导师反馈推导出的执行建议、术语边界和 PR-S0 拆分方案；可以作为后续工作默认起点，但不得伪装成导师原话。

## 2. 讨论背景与上游材料

本次讨论发生在 PR [#112](https://github.com/HansBug/research_ideas/pull/112) 已经整理出完整会前材料、并在 PR comment 中补充了导师反馈消化与决策记录之后。当前讨论的目标，不是继续扩大 scope，而是把“meta-model 是起点 / SLR 要产出 finding / researcher 可以挑战 finding”这三点真正操作化为后续 PR-S0 计划。

相关上游材料如下：

| 类型 | 链接 | 作用 |
|---|---|---|
| 导师讨论 PR / body | [#112](https://github.com/HansBug/research_ideas/pull/112) | 本次讨论的主入口；PR body / comments 已沉淀现状、story、Q 和 follow-up；后续重写 story / outline / claim-evidence map 时也应回看 PR body。 |
| PR #112 长 comment | [#112 comment](https://github.com/HansBug/research_ideas/pull/112#issuecomment-4706323481) | 本记录的直接来源之一，记录“researcher-guided, finding-oriented, auditable agentic SLR support workflow”主线。 |
| project_1 正式导师讨论库 | [README.md](./README.md) | 本记录的归档入口；后续 project_1 路线优先按这里的正式记录读取。 |
| 既有正式导师讨论记录 | [2026-06-12 记录](./2026-06-12-导师-两篇论文转向与模型修正定调.md)；[2026-06-04 记录](./2026-06-04-导师-第一篇论文路线与E1E2定位.md) | 作为 project_1 讨论文库的既有上下文，帮助理解第一篇 / 第二篇路线已经如何演化。 |
| baselines 文库 | [../paper_agent_based_slr/baselines/](../paper_agent_based_slr/baselines/) | 第二篇路线的强近邻与差异化基础。 |

### 2.1 来源边界与约束等级 ledger

本记录同样区分导师明确意见、用户会后确认和我方工作性转译。后续使用时应按下表理解：

| 条目 | 约束等级 | 来源证据 | 后续处理 |
|---|---|---|---|
| meta-model 是起点，应由使用该 work 的 researcher 基于 scaffold 设定、裁剪并实例化 | 【正式定调 / 用户会后确认】 | 用户会后转述的导师原意；#112 comment 及后续确认 | 作为第二篇 story 的硬约束；不预设作者替所有人固定一套 universal SE ontology。 |
| SLR 不只是文献整理，还应形成 research findings | 【正式定调 / 用户会后确认】 | 用户会后对导师批示的整理 | 这次讨论的核心升维点。 |
| 需要 finding pattern 来约束 LLM / agent | 【正式定调 / 用户会后确认】 | 用户会后整理 + #112 comment | 作为方法设计的一部分，但仍需操作化。 |
| researcher 可以围绕 finding 质疑证据、要求补证、找反例 | 【正式定调 / 用户会后确认】 | 用户会后整理 + #112 comment | 引入 challenge / refinement loop。 |
| survey-of-surveys / meta-review 是 scaffold 的经验来源 | 【AI 衍生建议】 | 主 session 与 reviewer 推导 | 可作为 PR-S0 follow-up，不应写成已完成。 |
| challenge loop 需要最小 protocol（input / operation / output / stop） | 【AI 衍生建议】 | reviewer 建议 | 用于后续 PR-S0 方案冻结。 |
| evaluation 应围绕 finding 的 relevance / evidence-groundedness / revision，而不是只看 novelty | 【AI 衍生建议】 | reviewer 建议 | 用于后续 experiment obligation 改写。 |

## 3. 关键定义与术语

| 术语 | 定义类型 | 本文口径 | rationale / 与邻近概念的区别 |
|---|---|---|---|
| meta-model scaffold | 本研究新造工作口径 | 帮助 researcher 显式声明综述对象、关系、证据字段和 finding 类型的可配置协议 / 模板。 | 不是 MDE/UML 意义上的完整 metamodel，也不是 universal SE review ontology；它是让 researcher 在具体综述里先把问题框架写清楚。 |
| topic-specific review meta-model | 本研究新造工作口径 | researcher 针对某个具体 SLR/SMS 主题裁剪和确认后的工作模型。 | 它由 researcher 设定，不由 LLM 自动最终决定。 |
| researcher-approved executable schema | 本研究新造工作口径 | 由系统辅助生成、经 researcher 确认后供 agent 执行的字段和任务约束。 | 这里的“转换”不是自动化万能编译，而是系统辅助 + researcher 确认。 |
| finding pattern scaffold | 本研究新造工作口径 | 用于指导 agent 提出候选 research findings 的模式集合。 | 它不保证 finding 真实性，只规定候选发现的类型和组织方式。 |
| candidate finding | 本研究新造工作口径 | agent 基于 evidence objects 和 finding pattern 提出的候选研究发现，默认状态为 `candidate`。 | 只有经过 evidence chain + researcher audit 才能升级为 final finding；否则应保留为 tentative / unresolved / downgraded。 |
| final finding | 本研究新造工作口径 | researcher 接受其 claim strength、supporting / counter evidence 已被审计且 scope 已限定的研究发现，默认状态为 `accepted`。 | final 不是 LLM 直接生成状态，而是 candidate finding 经证据审计后的结果。 |
| evidence object | 本研究新造工作口径 | 从论文中抽取出的可追踪证据单元。 | 不是普通摘要；必须能回到 source anchor 或明确缺口。 |
| researcher challenge loop | 本研究新造工作口径 | researcher 围绕 candidate finding 发起质疑，系统补证、找反例、修订 finding 的协议。 | 不等于必须立即实现交互式 UI；PR-S0 只冻结其 story 角色、最小术语与 follow-up gate，完整 protocol / log schema / examples 由后续 scaffold 子 PR 落地。 |
| claim strength | 本研究新造工作口径 | finding / claim 的强弱等级。 | 不能只由 LLM confidence 决定，最终要由 researcher + evidence 共同确认。 |

## 4. 新 story：研究者引导、面向发现、可审计的 agentic SLR 支持方法

### 4.1 一句话 story

> 我们提出一种用于 SE SLR/SMS 的 **researcher-guided, finding-oriented, auditable agentic SLR support workflow**：researcher 基于 scaffold 实例化 review meta-model，agent 在该框架和 finding patterns 约束下提出有证据支撑的候选 findings，researcher 再通过 evidence challenge / refinement loop 对这些 findings 进行质疑、修正或降级。

### 4.2 这次讨论后 story 的核心变化

与 PR #112 之前的“SE review meta-model → agent workflow → auditable evidence chain”相比，最新方向的关键变化是：

1. **中心对象从 workflow 转到 finding**：SLR 的研究价值不只是整理文献，而是形成 research findings。
2. **meta-model 从“作者定义通用模型”降级为 scaffold + researcher instantiation**：研究者要先把自己的综述问题框架写清楚。
3. **evidence chain 从静态 trace 升级为 finding 审计结构**：它用来支撑、反驳、降级或修正 finding。
4. **researcher interaction 从附加功能变成方法闭环**：researcher 的质疑、补证和找反例是 finding 形成过程的一部分，而不是事后说明。

### 4.3 与宽泛自动化 SLR 的区别

本次讨论明确把工作从“自动化 SLR / 自动生成综述”收缩到“研究者引导的证据构建与发现生成支持”。这意味着：

- 不能把这篇工作写成完整自动化 SLR；
- 不能把 LLM 说成自动定义 meta-model；
- 不能把 candidate finding 直接当作最终 finding；
- 不能把 challenge loop 误写成必须先有完整 UI 才能成立。

---

## 5. 方法主线：从 meta-model 到 finding 再到 challenge

> 状态：`[正式定调 + AI 衍生建议]`

### 5.1 方法阶段

1. **Researcher instantiates the review meta-model**
   - 输入：综述主题、初始 RQ、seed papers、领域知识、研究者关注点。
   - 输出：topic-specific review meta-model。
   - 约束：LLM 可建议字段，但 researcher 必须确认；未确认版本不能进入正式 run。

2. **System-assisted executable schema preparation**
   - 输入：topic-specific review meta-model。
   - 输出：researcher-approved executable schema。
   - 约束：可通过 schema 完整性检查验证输入是否齐备；具体实现方式（deterministic / hybrid / human-audited）待 PR-S0 确定。

3. **Evidence extraction and coding**
   - agent 从论文中抽取 evidence objects：topic、method、artifact、dataset、metric、result、claim、threat、code/data/prompt availability、source anchor 等。

4. **Candidate finding proposal**
   - candidate-finding agent 根据 finding patterns 从 evidence objects 中提出候选 findings。
   - 这些候选 findings 只代表“值得进一步审计的发现”，不是最终结论。

5. **Evidence-chain construction**
   - 每个 candidate finding 建立 supporting / counter papers、source anchors、decision log、confidence / uncertainty 和 revision history。

6. **Researcher challenge and refinement protocol**
   - researcher 对 finding 发起质疑，系统补证、找反例、重抽取、重编码、提出降级版本或新 finding。
   - stop condition 可以是 researcher accept、mark unresolved、或触发新 review iteration。

### 5.2 最小 challenge protocol

> **来源等级说明**：导师正式定调到“researcher 可以围绕 finding 质疑、补证、找反例”这一闭环方向；下表中的 input / operation / output / stop 只是本记录给出的 AI 衍生操作化方案。

| 环节 | 内容 |
|---|---|
| Challenge input | 证据不足、反例要求、scope 过宽、claim strength 过强、检索偏差、coding 错误、finding 模糊 |
| System operation | 补检索、找 counter-evidence、重抽取、重编码、重算 finding support、提出降级版本 |
| Output | revised finding、downgraded claim、counter-evidence list、unresolved uncertainty、challenge log |
| Stop condition | researcher accept、标记 unresolved、或触发新 review iteration |

PR-S0 阶段只需明确 challenge protocol 在 story / outline / claim-evidence map 中的角色、最小术语与 follow-up gate；完整规则、日志 schema 和 examples 应由后续 scaffold 子 PR 落地，不必在 PR-S0 完成，也不必立即实现交互式 UI。

**Candidate-to-final 最小转移规则（候选）**：candidate finding 只有同时满足 `supporting evidence 已回链到 source anchors`、`counter-evidence / uncertainty 已被显式检查或标记缺口`、`scope 与 claim strength 已经 researcher 确认` 三个条件，才可转为 final finding；否则必须继续保留为 `candidate / tentative / unresolved / downgraded` 之一。该规则是 PR-S0 的最小术语门槛，不等价于完整 finding artifact schema。

---

## 6. Finding pattern scaffold：不只找 gap，也找结构与趋势

> 状态：`[候选设计；PR-S0 只需冻结初版，不应写成已验证结果]`
>
> **来源等级说明**：导师正式定调到“需要 finding pattern 来约束 LLM / agent”这一抽象层级；下表 11 项为本记录提出的候选实例，后续应在 survey-of-surveys 中校验保留、删减或合并。

导师强调 SLR 的 research finding 功能后，finding pattern 不应只剩“找不足清单”。当前候选 pattern 包括：

| Finding pattern | 说明 | 典型输出 |
|---|---|---|
| Topic gap | 某些主题、子问题或应用场景缺少关注 | “LLM4Modeling 中 X 类场景研究较少。” |
| Method gap | 现有方法集中在浅层 prompt、demo 或单阶段处理 | “多数方法未形成验证反馈闭环。” |
| Evidence gap | 缺少真实系统、工业案例、大规模数据、benchmark 或长期实验 | “现有结果主要来自小样本案例。” |
| Evaluation weakness | 指标单一、缺少 ablation、缺少人工一致性或失败分类 | “多数论文只报告生成质量，缺少错误类型分析。” |
| Reproducibility gap | 缺代码、缺数据、缺 prompt、缺模型版本或 run record | “缺少可复查的 prompt / raw output / model usage。” |
| Contradiction / tension | 不同论文对同一问题给出冲突结论或不同假设 | “部分研究支持 LLM screening，另一些显示 temperature=0 仍不稳定。” |
| Trend finding | 某主题随年份、venue、方法路线出现变化 | “2024 后 agent-based review workflow 快速增多。” |
| Consensus finding | 多数论文在某一点形成一致判断 | “人工审计仍被认为是降低 hallucination 风险的必要环节。” |
| Taxonomy finding | 从文献中归纳出方法 / 任务 / 证据对象分类 | “现有方法可分为 screening、extraction、survey generation、evidence synthesis 等。” |
| Maturity finding | 某方向处于概念、原型、小样本验证或较成熟 benchmark 阶段 | “SE LLM-SLR 目前更多集中在 screening 与方法学风险。” |
| Transferability gap | 方法在某领域有效，但缺少跨主题 / 跨领域迁移证据 | “医学 / 金融系统不直接证明适用于 SE SLR finding audit。” |

这里的关键不再只是 gap，而是要把 SLR 产出的 findings 组织成更丰富的结构化类型。

---

## 7. 候选贡献与 outline

> 状态：`[候选；PR-S0 需进一步压缩和验证]`

### 7.1 候选贡献

1. **Researcher-instantiated meta-model scaffolding**
   - 提供一套可配置 scaffold 和实例化协议，让 researcher 在 SLR 开始前显式声明研究问题、证据对象、关系和 finding 类型。

2. **Finding pattern scaffold for SLR research findings**
   - 把 SLR 的 research findings 方法化，提供 gap、trend、consensus、taxonomy、maturity、contradiction、transferability 等候选 patterns。

3. **Meta-model-guided agent support workflow**
   - 设计一个由 researcher-approved meta-model 约束的 agent 支持流程，使检索、筛选、抽取、编码、candidate finding proposal 和 evidence linking 围绕同一 schema 协作。

4. **Evidence-backed researcher challenge loop**
   - 引入 challenge / refinement protocol，使 researcher 能对 candidate finding 发起证据质疑，系统补证、找反例、降级或修正 finding，并保留 evidence chain 与 revision history。

### 7.2 候选 outline

1. Introduction
2. Background and Related Work
3. Planned Design Basis: Survey-of-surveys
4. Method
5. System / Implementation
6. Evaluation
7. Discussion and Limitations

其中，**Survey-of-surveys** 目前只是 planned design basis，不是已完成综述。

### 7.3 survey-of-surveys 最低 protocol（候选）

| 项 | 候选要求 |
|---|---|
| Source pool | 近年 SE / AI4SE / MDE / LLM4SE 的 SLR、SMS、survey；优先 CCF A/B/C 与高质量期刊/会议 |
| Inclusion criteria | 明确包含 SLR/SMS/survey，且报告 RQ、taxonomy、extraction、finding、gap/challenge/future work 中至少若干项 |
| Extraction fields | RQ 类型、taxonomy 维度、evidence table 字段、finding 类型、gap 写法、threat to validity、artifact / replication package |
| Coding procedure | 至少双人或 agent+human audit 的编码检查；保留 disagreement / uncertainty |
| Output boundary | 只作为 scaffold design basis，不主张系统覆盖全部 SE surveys，不作为正式 PRISMA 式综述 |

---

## 8. Evaluation obligation：围绕 candidate finding 与证据过程评价，不预设正收益

> 状态：`[AI 衍生建议；PR-S0 可写入 evaluation obligation，但不能写成结果]`
>
> **来源等级说明**：导师确认的是“candidate finding 需要 evidence chain + researcher audit 才能升级”为 final finding；RQ / 指标 / ablation 的具体形态为本记录衍生方案。

以下是候选评测设计，不代表已有结果，也不应被写成已完成实验：

| RQ | 问题 | 候选指标 / 人工评估维度 |
|---|---|---|
| RQ1 | researcher-instantiated meta-model 是否提高抽取 / 编码结构化程度？ | extraction correctness、schema coverage、coding consistency |
| RQ2 | finding patterns 是否帮助产生更有用、更可审计的 candidate findings？ | relevance、actionability、evidence-groundedness、non-triviality judged by domain researchers、finding type coverage |
| RQ3 | evidence chain 是否降低 unsupported / overclaimed findings？ | 无证据支撑 finding 比例、claim-to-source accuracy、counter-evidence coverage |
| RQ4 | researcher challenge loop 对 finding 修订有什么影响？ | challenge resolution / unresolved rate、claim downgrade / revision count、new evidence found、audit time；这些是过程指标，不天然代表正收益 |
| RQ5 | 相比 generic agentic SLR workflow，meta-model + finding pattern scaffold 的影响与代价是什么？ | ablation：without scaffold / without finding patterns / without challenge protocol；成本、错误类型变化 |

**最小接收门槛建议**：candidate finding 只有在 evidence chain 能支撑、counter-evidence 已检查、且 researcher 明确接受其强度时，才可升级为 final finding；否则应保留为 tentative / unresolved / downgraded。

---

## 9. 当前与强近邻 baseline 的差异化

> 状态：`[差异化假设；后续写 Related Work 前仍需回到 baselines 文库核验]`

| Baseline 类型 / 代表方向 | 已有能力 | 本文拟强调的差异 |
|---|---|---|
| LatteReview / agentic SLR workflow | 多 agent screening / extraction / reviewer workflow | 不主打“多 agent SLR workflow 首创”，而主打 researcher-defined meta-model、finding patterns、finding-level evidence chain 和 challenge protocol |
| LR-Robot / human-in-the-loop taxonomy classification | expert taxonomy + LLM 批量分类 + 下游知识库 / 网络分析 | 不只是分类或 bibliometric analysis，而是围绕 candidate research findings 生成、证据支撑、反证和迭代修正 |
| Closed-loop scientific literature summarization | agent + human audit + extraction + report loop | 聚焦 SE SLR/SMS 的 researcher-instantiated meta-model 与 finding-oriented audit，而非通用科学数值抽取 / 报告 |
| Beyond Accuracy / SE SLR screening | SE 语境下 LLM screening 变异性、人工复核和治理问题 | 将 screening 风险纳入更宽的 finding、evidence chain 和 challenge protocol 设计；不声称已覆盖或优于该工作 |
| Survey generation / automated literature review | 自动生成综述文本、引用、survey 结构 | 不把流畅报告作为核心结果，而把 evidence-backed candidate finding 与 researcher challenge 作为核心对象 |

---

## 10. Claims to make / be careful / avoid

> 状态：`[PR-S0 必须写入 claim_evidence_map / claims-to-avoid]`

### 可以尝试主张

- SLR 中的 research findings 需要 researcher-defined conceptual frame，而不是 LLM 自由生成。
- Meta-model scaffold 与 finding patterns 可以把 researcher 的问题意识转成 agent 可执行的 evidence workflow。
- Evidence chain 与 researcher challenge protocol 可以让 candidate findings 更可审计、更容易修正。

### 需要谨慎主张

- “提高 finding quality”：需要人工评价和清晰指标支持。
- “降低 unsupported findings”：需要 claim-to-source / counter-evidence 评测支持。
- “适用于 SE SLR/SMS”：如果实验只覆盖 LLM4Modeling / MDE，必须限定 scope。
- “challenge loop 有收益”：需要用过程指标和人工评价说明，不可预设必然正收益。

### 禁止或应避免的主张

- 首次 LLM / agent 自动化 SLR。
- 完整自动化 SLR 全生命周期。
- LLM 自动定义可靠 meta-model。
- 本文定义了一套适用于所有 SE 主题的完整通用 meta-model。
- PRISMA 合规。
- 替代人工专家或优于人工 SLR。

---

## 11. 后续任务：文件级落点与验收标准

> 状态：`[后续执行建议；PR-S0 只做 story 级冻结，不做完整实现]`
>
> **PR-S0 硬门槛**：只冻结 story / outline / claim-evidence map / 最小 schema；不做完整 survey-of-surveys，不做 runtime，不产实验结果，不把 candidate finding 写成 final finding。

| 任务 | 建议落点 | 产物 | 验收标准 | PR-S0 不做事项 |
|---|---|---|---|---|
| Task A：重写 story | [paper_story.md](../paper_agent_based_slr/story/paper_story.md)、[story/README.md](../paper_agent_based_slr/story/README.md) | 新 thesis、gap、method insight、claims-to-avoid | 明确 researcher-guided / finding-oriented / auditable；删除“自动化 SLR 首创”风险 | 不写最终 abstract；不声称实验已完成 |
| Task B：更新 outline | [paper_outline.md](../paper_agent_based_slr/story/paper_outline.md) | 新章节结构和 RQ | 标出 survey-of-surveys、finding patterns、challenge protocol、evaluation obligation 的章节位置与 follow-up gate | 不冻结最终实验数字；不展开完整 protocol / schema |
| Task C：更新 claim-evidence map | [claim_evidence_map.md](../paper_agent_based_slr/story/claim_evidence_map.md) | claims-to-make / careful / avoid | 禁用完整自动化、PRISMA、通用 meta-model、替代专家等强 claim | 不把候选 contribution 写成已验证结果 |
| Task D：新增 survey-of-surveys 子 PR | 可在 `paper_agent_based_slr/survey_of_surveys/` 或类似路径 | README/GUIDE/SUMMARY + 初筛协议 | 有 source pool、inclusion criteria、extraction fields、coding/audit procedure、更新日志 | PR-S0 不直接完成完整 survey-of-surveys |
| Task E：新增 scaffold 设计子 PR | `paper_agent_based_slr/scaffolds/` 或 paper2 专属 method 子目录 | meta-model scaffold、finding pattern scaffold、challenge log schema 草案 | 明确 scaffold 可配置、researcher-approved、非 universal ontology | PR-S0 不创建该目录；目录创建与总账同步由独立子 PR 负责；不实现完整 agent runtime |
| Task F：重新定义 evaluation obligation | [paper_outline.md](../paper_agent_based_slr/story/paper_outline.md) / [claim_evidence_map.md](../paper_agent_based_slr/story/claim_evidence_map.md) | RQ、指标、ablation、人工评估维度 | 指标围绕 finding usefulness、evidence-groundedness、unsupported rate、challenge revision | 不承诺已有结果，不虚构数据 |

## 12. 当前总判断

> **说明**：本节为综合判断，具体子句的来源等级以 §2.1 ledger 为准。

这次导师反馈把 paper2 的中心进一步收紧：

> 不是让 LLM/agent 替人机械完成 SLR，而是让 researcher 通过 meta-model scaffold 表达综述问题，让 agent 在 finding pattern 和 evidence chain 约束下帮助形成、支撑、质疑和修正 candidate research findings。

这一路线比“agent 自动化 SLR pipeline”更稳，因为它把 novelty 从流程自动化转向：

1. researcher 如何显式化 review frame；
2. LLM 如何在 finding patterns 下提出候选 findings；
3. evidence chain 如何支撑 / 反驳 / 降级 findings；
4. researcher challenge 如何驱动迭代。

后续 PR-S0 应围绕这条线重写 story、outline、claim-evidence map 和实验义务；同时把 survey-of-surveys、scaffold 设计和 challenge protocol 拆成明确 follow-up PR，避免在 PR-S0 中 scope creep。
