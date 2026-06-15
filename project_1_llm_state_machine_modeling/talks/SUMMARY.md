# project_1 正式导师讨论总账

## 1. 总体状态

| 字段 | 当前状态 |
|---|---|
| 正式导师讨论记录数 | 3 |
| 最近更新时间 | 2026-06-15 19:45:28 |
| 当前第一篇论文主倾向 | `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正 |
| `NL -> STM` 定位 | seed construction / baseline source / related work，不再作为第一篇主贡献 |
| Path-2 定位 | 可作为后续控制系统差异化论文继续展开；不压进第一篇主线 |
| E1/E2 定位 | 同一方法底座或工具链在不同 agent 编排形态下的实验条件，不主打 Hybrid story |
| 当前核心贡献口径 | 以 `<NL, STM_0> -> STM_k` 的无人化反馈驱动修正协议为核心；语义增强、可机检、可执行状态机表示仅作为承载 diagnostics / simulation / repair feedback 的必要实验载体 |
| 第二篇当前倾向 | researcher-guided、finding-oriented、auditable agentic SLR support workflow：使用者 researcher 基于 scaffold 实例化 review meta-model，agent 提出候选 research findings 并建立 evidence chain，researcher 通过 challenge loop 质疑、补证、降级或修正 finding |

## 2. 记录列表

状态口径：🟢 = 当前有效；🟡 = 部分被后续记录覆盖但仍有可复用背景；⚪ = 历史背景。

| 日期 | 记录 | 核心结论 | 状态 |
|---|---|---|---|
| 2026-06-15 | [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md) | 第二篇进一步从“agent-based SLR / evidence workflow”收敛为 researcher-guided、finding-oriented、auditable agentic SLR support workflow；meta-model 应由使用该方法的 researcher 基于 scaffold 实例化；SLR 产出 candidate research findings，并通过 evidence chain 与 researcher challenge loop 迭代审计。 | 🟢 |
| 2026-06-12 | [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇从 `NL -> STM` 生成转为 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正；`fcstm` / DSL 继续弱化为内部载体；baseline 转为 seed/source/converter/comparison；第二篇转向 agent-based SLR 方法学，该第二篇口径已被 2026-06-15 记录进一步细化。 | 🟢 |
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
| 第二篇转向 researcher-guided、finding-oriented、auditable agentic SLR support workflow；meta-model scaffold 由本文提供但 operative meta-model 由使用者 researcher 实例化和确认。 | 正式定调 / 用户会后确认 | PR-S0 story、outline、claim-evidence map。 |
| SLR 的输出不应只是文献整理或报告生成，还应形成 candidate research findings；LLM/agent 可在 finding pattern 约束下提出候选 finding，但最终强度由 evidence chain + researcher audit 决定。 | 正式定调 + AI 执行展开 | finding pattern scaffold、evaluation obligation。 |
| researcher challenge loop 是第二篇方法闭环的一部分，可先以 protocol + log schema + examples 落地，不必在 PR-S0 立即实现 UI。 | 正式定调 + AI 执行展开 | scaffold / method follow-up PR。 |
| 需要 survey-of-surveys 作为 meta-model scaffold 与 finding pattern scaffold 的经验来源；它是 planned design basis，不应被写成已完成 PRISMA 式综述。 | AI 衍生执行建议 | 后续 survey_of_surveys 子 PR。 |
| 正式导师讨论记录必须区分【正式定调】和【AI 衍生建议】，不得把 AI 补全写成导师原话。 | 维护纪律 | 后续 talks 文库更新。 |

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 19:45:28 | 新增 2026-06-15 PR #112 导师讨论记录，更新第二篇为 researcher-guided、finding-oriented、auditable agentic SLR support workflow，并补充 meta-model scaffold、finding pattern、researcher challenge loop 与 survey-of-surveys 约束。 |
| 2026-06-12 16:41:15 | 按三路 reviewer 的 I 级意见补充条目级来源等级、`Better STM` 最小操作化判定框架，并把 SUMMARY 当前约束改为带来源等级表格。 |
| 2026-06-12 16:20:42 | 新增 2026-06-12 导师讨论记录，更新第一篇为 `<NL, STM_0> -> STM_k / Better STM` 修正任务，并记录第二篇 agent-based SLR 转向；同步新增“正式定调 vs AI 衍生建议”维护纪律。 |
| 2026-06-04 15:04:00 | 根据三路 reviewer 的 M 级建议，补充单篇记录的 PR 状态说明、contribution 草案归属说明、关键上游 comment 深链与总账回填提示。 |
| 2026-06-04 14:45:00 | 初始化 project_1 正式导师讨论文库，新增 2026-06-04 讨论记录。 |

后续任何正式导师讨论的新增、更新或覆盖，均应在本更新日志首行插入新记录，并同步更新 §1 总体状态与 §2 记录列表。
