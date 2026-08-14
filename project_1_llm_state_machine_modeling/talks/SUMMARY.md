# project_1 正式导师讨论总账

## 1. 总体状态

| 字段 | 当前状态 |
|---|---|
| 正式导师讨论记录数 | 4 |
| 最近更新时间 | 2026-06-26 13:53:19 |
| 当前第一篇论文主倾向 | `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正 |
| `NL -> STM` 定位 | seed construction / baseline source / related work，不再作为第一篇主贡献 |
| Path-2 定位 | 可作为后续控制系统差异化论文继续展开；不压进第一篇主线 |
| E1/E2 定位 | 同一方法底座或工具链在不同 agent 编排形态下的实验条件，不主打 Hybrid story |
| 当前核心贡献口径 | 以 `<NL, STM_0> -> STM_k` 的无人化反馈驱动修正协议为核心；语义增强、可机检、可执行状态机表示仅作为承载 diagnostics / simulation / repair feedback 的必要实验载体 |
| 第二篇当前倾向 | researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach：researcher 定义 topic / RQ / scope / meta-model，agent 在 researcher-approved dimension schema 下抽取 field-level content evidence、生成 statistical analysis 与 candidate finding signals，researcher 通过 challenge / counter-evidence / adjudication 将部分候选升级为 final target-domain findings；计划中的 pilot 与后续硕士生 process data 将用于 method-evaluation findings |

## 2. 记录列表

状态口径：🟢 = 当前有效；🟡 = 部分被后续记录覆盖但仍有可复用背景；⚪ = 历史背景。

| 日期 | 记录 | 核心结论 | 状态 |
|---|---|---|---|
| 2026-06-26 | [2026-06-26-导师-三阶段SLR与human-in-the-loop-finding.md](./2026-06-26-导师-三阶段SLR与human-in-the-loop-finding.md) | 第二篇进一步将真实 SLR 拆成收集论文、维度 pattern 驱动的论文分析、统计分析与 research finding 形成；明确 statistical analysis 与 target-domain research finding 分层，survey-of-surveys 只是 scaffold mining，human-in-the-loop 是贯穿 meta-model / pattern / evidence / analysis / finding / process logging 的 approach，后续需先 pilot 再收集硕士生 human-LLM interaction process data。 | 🟢 |
| 2026-06-15 | [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md) | 第二篇进一步从“agent-based SLR / evidence workflow”收敛为 researcher-guided、finding-oriented、auditable agentic SLR support workflow；meta-model 应由使用该方法的 researcher 基于 scaffold 实例化；SLR 产出 candidate research findings，并通过 evidence chain 与 researcher challenge loop 迭代审计。该口径已被 2026-06-26 记录细化为 pattern-evolving / evidence-backed / statistical-analysis-vs-finding 分层方法。 | 🟢 |
| 2026-06-12 | [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇从 `NL -> STM` 生成转为 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正；`fcstm` / DSL 继续弱化为内部载体；baseline 转为 seed/source/converter/comparison；第二篇转向 agent-based SLR 方法学，该第二篇口径已被 2026-06-15 记录进一步更新为 researcher-guided、finding-oriented、auditable agentic SLR support workflow。 | 🟢 |
| 2026-06-04 | [2026-06-04-导师-第一篇论文路线与E1E2定位.md](./2026-06-04-导师-第一篇论文路线与E1E2定位.md) | 第一篇更倾向 Path-1；Path-2 可拆成另一篇；E1/E2 是同一底座在自建 agent-loop 与成熟 agent 框架下的实验对照；弱化 `fcstm` 名称仍有效，但第一篇主任务边界已被 2026-06-12 记录更新。 | 🟡 |

## 3. 当前高优先级约束

| 约束 / 建议 | 来源等级 | 后续落点 |
|---|---|---|
| 第一篇论文主任务改为 `<NL, STM_0> -> STM_k / Better STM` 的自动反馈驱动修正，不再主打 `NL -> STM` 生成。 | 正式定调 / 用户会后确认 | 第一篇 story、abstract、outline、RQ。 |
| `NL -> STM_0` 只作为 seed construction / baseline source / related work。 | 正式定调 / 用户会后确认 | task definition 与 experiment protocol。 |
| “无人化”限定为单次 repair run 内 no human-in-the-loop；人类可参与 benchmark、seed 构造、reference / adjudication 和最终审计。 | 正式定调 / 用户会后确认 | method boundary 与 threats。 |
| 继续弱化 `fcstm` / `pyfcstm` / DSL 名称；语义增强、可机检、可执行表示只是 feedback loop 的必要载体。 | 正式定调 / 延续早期导师意见 | terminology policy 与 contribution。 |
| prior baseline 不作废，应重排为 seed artifact、输入来源、转换目标、错误类型来源、related work 和必要 comparison / ablation。 | 正式定调 + AI 执行展开 | baseline matrix / related work。 |
| 规划面向 benchmark seed 的最小多格式转换层，不声称通用多格式状态机转换器。 | 正式定调 + AI 执行展开 | converter planning；具体范围后续 PR 冻结。 |
| repair-loop evaluation 覆盖 `STM_0` vs `STM_k`、structured feedback ablation、repair acceptance / rollback、rejected repair、oscillation / non-convergence。 | AI 衍生执行建议 | experiment design；可按 pilot 结果调整。 |
| 第二篇应以真实 SLR 的三层实践为基础：收集论文只是苦力层；论文分析层以可演化 dimension pattern 和 field-level content evidence 为中心；synthesis 层必须拆分 statistical analysis 与 target-domain research finding construction。 | 正式定调 / 用户会后确认 | PR-S0 / S0B story、method figure、artifact schema。 |
| human-in-the-loop 是 paper2 approach 的核心，researcher 不是末端审核者，而是在 topic / meta-model、dimension schema、field evidence、analysis protocol、candidate finding challenge、final adjudication 和 process logging 中持续拥有裁决权。 | 正式定调 / 导师原话 | method figure、gate contract、evaluation protocol。 |
| survey-of-surveys 可放宽范围、低成本识别 dimension pattern。 | 正式定调 / 导师原话 | scaffold mining 的直接动机。 |
| survey-of-surveys 的输出可扩展为 finding / evidence-presentation pattern library，但不进入目标 SLR findings evidence pool，也不得写成 PRISMA 式 tertiary review。 | AI 衍生执行建议 | survey-of-surveys 子 PR 的边界。 |
| pilot run 是下一步硬动作：先选定一个主题跑一遍方法看效果。 | 正式定调 / 导师原话 | pilot PR 的直接动机。 |
| pilot run 的执行化闭环应覆盖 meta-model、dimension schema、field evidence、statistical analysis、candidate finding signals、challenge / adjudication 和 process evidence；不声称跨主题泛化。 | AI 衍生执行建议 | pilot run record、artifact schema。 |
| 后续让硕士生使用这套方法做实验，并收集实验过程数据，特别是 human-LLM interaction data。 | 正式定调 / 导师原话 | multi-user evaluation protocol 的直接动机。 |
| 硕士生实验数据应作为 method-evaluation process data，记录 human-LLM interaction logs、人工修改、拒绝建议、决策理由和时间成本；需提前定义 consent、匿名化、日志脱敏和教学关系隔离。 | AI 衍生执行建议 | ethics/data boundary、process-data schema。 |
| 第二篇转向 researcher-guided、finding-oriented、auditable agentic SLR support workflow；operative meta-model 必须由使用者 researcher 针对 topic / RQ / scope 实例化和确认。 | 正式定调 / 用户会后确认 | PR-S0 story、outline、claim-evidence map。 |
| 本文可提供 generic meta-model template、dimension / finding pattern library 与 gate scaffold；但这些 scaffold 不得被写成 researcher-specific operative meta-model，也不得替代 executable dimension schema 的人工确认与版本化。 | AI 衍生执行建议 | scaffold / schema / gate 子 PR。 |
| SLR 的输出不应只是文献整理或报告生成，还应形成 research findings；最终 finding 强度必须由 evidence chain + researcher audit 决定。 | 正式定调 / 用户会后确认 | paper story、claim-evidence map。 |
| LLM/agent 可在 finding pattern 约束下提出 candidate finding signals；这些信号只有经 evidence audit、counter-evidence search、claim strength 降级和 researcher adjudication 后，才可转为 candidate / final target-domain findings。 | AI 衍生执行建议 | finding pattern scaffold、evaluation obligation。 |
| researcher challenge loop 是第二篇方法闭环的一部分：researcher 可以围绕 finding 质疑证据、要求补证、找反例、降级或修正 finding。 | 正式定调 / 用户会后确认 | PR-S0 story / claim-evidence map。 |
| PR-S0 只冻结 challenge 的 story 角色、最小术语和 follow-up gate；完整 protocol / log schema / examples 由后续 scaffold 子 PR 落地。 | AI 衍生执行建议 | scaffold follow-up PR。 |
| evaluation 应围绕 finding 的 usefulness / evidence-groundedness / 无证据支撑比例 / challenge-revision，不只看 novelty 或报告质量。 | AI 衍生执行建议 | experiment design、review rubric、后续 PR-S0 指标冻结。 |
| 需要 survey-of-surveys 作为 dimension / finding pattern scaffold 的经验来源；它是 planned design basis，不应被写成已完成 PRISMA 式综述，也不应称为 operative meta-model 的来源。 | AI 衍生执行建议 | 后续 survey_of_surveys 子 PR。 |
| 正式导师讨论记录必须区分【正式定调】和【AI 衍生建议】，不得把 AI 补全写成导师原话。 | 维护纪律 | 后续 talks 文库更新。 |

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-26 13:53:19 | 新增 2026-06-24/26 PR #123 三阶段 SLR 与 human-in-the-loop finding 形成导师讨论记录；更新第二篇当前倾向为 researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach，并补充 statistical analysis / target-domain finding / method-evaluation finding、content/process evidence、survey-of-surveys scaffold、planned pilot run 与后续硕士生 process data 约束。 |
| 2026-06-15 20:02:59 | 根据三路 reviewer 的 I 级意见，收紧第二篇记录中的来源等级、PR-S0 scope、candidate finding / final finding 边界、evaluation obligation 与上游链接口径。 |
| 2026-06-15 19:45:28 | 新增 2026-06-15 PR #112 导师讨论记录，更新第二篇为 researcher-guided、finding-oriented、auditable agentic SLR support workflow，并补充 meta-model scaffold、finding pattern、researcher challenge loop 与 survey-of-surveys 约束。 |
| 2026-06-12 16:41:15 | 按三路 reviewer 的 I 级意见补充条目级来源等级、`Better STM` 最小操作化判定框架，并把 SUMMARY 当前约束改为带来源等级表格。 |
| 2026-06-12 16:20:42 | 新增 2026-06-12 导师讨论记录，更新第一篇为 `<NL, STM_0> -> STM_k / Better STM` 修正任务，并记录第二篇 agent-based SLR 转向；同步新增“正式定调 vs AI 衍生建议”维护纪律。 |
| 2026-06-04 15:04:00 | 根据三路 reviewer 的 M 级建议，补充单篇记录的 PR 状态说明、contribution 草案归属说明、关键上游 comment 深链与总账回填提示。 |
| 2026-06-04 14:45:00 | 初始化 project_1 正式导师讨论文库，新增 2026-06-04 讨论记录。 |

后续任何正式导师讨论的新增、更新或覆盖，均应在本更新日志首行插入新记录，并同步更新 §1 总体状态与 §2 记录列表。
