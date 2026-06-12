# project_1 正式导师讨论总账

## 1. 总体状态

| 字段 | 当前状态 |
|---|---|
| 正式导师讨论记录数 | 2 |
| 最近更新时间 | 2026-06-12 16:41:15 |
| 当前第一篇论文主倾向 | `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正 |
| `NL -> STM` 定位 | seed construction / baseline source / related work，不再作为第一篇主贡献 |
| Path-2 定位 | 可作为后续控制系统差异化论文继续展开；不压进第一篇主线 |
| E1/E2 定位 | 同一方法底座或工具链在不同 agent 编排形态下的实验条件，不主打 Hybrid story |
| 当前核心贡献口径 | 以 `<NL, STM_0> -> STM_k` 的无人化反馈驱动修正协议为核心；语义增强、可机检、可执行状态机表示仅作为承载 diagnostics / simulation / repair feedback 的必要实验载体 |
| 第二篇当前倾向 | 从 `sources` 文库综述 / corpus paper 转向带 human audit gates 的 agent-based SLR 方法学与 benchmark / evidence-package 评价框架 |

## 2. 记录列表

状态口径：🟢 = 当前有效；🟡 = 部分被后续记录覆盖但仍有可复用背景；⚪ = 历史背景。

| 日期 | 记录 | 核心结论 | 状态 |
|---|---|---|---|
| 2026-06-12 | [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇从 `NL -> STM` 生成转为 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正；`fcstm` / DSL 继续弱化为内部载体；baseline 转为 seed/source/converter/comparison；第二篇转向 agent-based SLR 方法学。 | 🟢 |
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
| 第二篇转向带 human audit gates 的 agent-based SLR；需要调研 ASReview / RobotReviewer / SLR automation 等既有工作。 | 正式定调 + AI 方法学补证建议 | 第二篇 planning issue / PR。 |
| 正式导师讨论记录必须区分【正式定调】和【AI 衍生建议】，不得把 AI 补全写成导师原话。 | 维护纪律 | 后续 talks 文库更新。 |

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-12 16:41:15 | 按三路 reviewer 的 I 级意见补充条目级来源等级、`Better STM` 最小操作化判定框架，并把 SUMMARY 当前约束改为带来源等级表格。 |
| 2026-06-12 16:20:42 | 新增 2026-06-12 导师讨论记录，更新第一篇为 `<NL, STM_0> -> STM_k / Better STM` 修正任务，并记录第二篇 agent-based SLR 转向；同步新增“正式定调 vs AI 衍生建议”维护纪律。 |
| 2026-06-04 15:04:00 | 根据三路 reviewer 的 M 级建议，补充单篇记录的 PR 状态说明、contribution 草案归属说明、关键上游 comment 深链与总账回填提示。 |
| 2026-06-04 14:45:00 | 初始化 project_1 正式导师讨论文库，新增 2026-06-04 讨论记录。 |

后续任何正式导师讨论的新增、更新或覆盖，均应在本更新日志首行插入新记录，并同步更新 §1 总体状态与 §2 记录列表。
