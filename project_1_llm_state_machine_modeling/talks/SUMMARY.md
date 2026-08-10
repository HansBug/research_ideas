# project_1 正式导师讨论总账

## 1. 总体状态

| 字段 | 当前状态 |
|---|---|
| 正式导师讨论记录数 | 4（另收 1 篇实验结论记录，见 §2） |
| 最近更新时间 | 2026-08-11 03:05:00 |
| 当前第一篇论文主倾向 | **STM issue discover，单独成篇**（2026-08-08 导师定调）。repair 另立后续论文，本篇只在讨论一节捎带提及 |
| `NL -> STM` 定位 | seed construction / baseline source / related work，不再作为第一篇主贡献 |
| `fcstm` / `pyfcstm` 定位 | intermediate semantic representation / executable medium，只服务 diagnostics / simulation / verification / refinement，不作为 paper1 contribution |
| Better STM 定位 | R5.7 阶段性评价框架；active headline framework 已被覆盖，Better STM-facing 资产应全量归档 |
| Path-2 定位 | 可作为后续控制系统差异化论文继续展开；不压进第一篇主线 |
| E1/E2 定位 | 同一方法底座或工具链在不同 agent 编排形态下的实验条件，不主打 Hybrid story |
| 当前核心贡献口径 | 两条：① **谓词逻辑元模型与断言体系本身**（不是"发现了多少问题"），断言由 NL 全覆盖需求条目转换而来、天然具备覆盖性，为真的部分构成回归防护；② 导师点名的差异化叙述——现有 detection 方法**缺少错误的上下文信息**，导致人工复核繁重且无法做修复后回归确认。⛔ issue closure / regression audit / discover-and-refine loop **不再是主贡献** |
| 谓词词表由来的论文口径 | 从**领域分析、真实文献与技术资料调研**归纳，应用于 54 个案例，并据此指导 prompt 设计。⛔ 不表述为"从这批 pair 归纳" |
| 建模对象边界 | $M = (S, E, V, Tr, A)$，不含时钟与正交区。fork/join 那份需求在**问题定义阶段**即落在界外，一句话带过，**不单开 RQ、不做辩护** |
| 第二篇当前倾向 | 从 `sources` 文库综述 / corpus paper 转向带 human audit gates 的 agent-based SLR 方法学与 benchmark / evidence-package 评价框架 |

## 2. 记录列表

状态口径：🟢 = 当前有效；🟡 = 部分被后续记录覆盖但仍有可复用背景；⚪ = 历史背景。状态列只写 emoji。

| 日期 | 记录 | 核心结论 | 状态 |
|---|---|---|---|
| 2026-08-10 | [2026-08-10-实验-v46全量矩阵双侧结论.md](./2026-08-10-实验-v46全量矩阵双侧结论.md) | **实验结论记录，非导师意见。** 一次完整实验 324 格：覆盖侧 `hit@1` 355/588 = 60.4%（**必须标为上界**）、`hit@3` 70.9%、`hit@all` 48.5%；多报侧 288 条目 / 124 去重，**最大成分 46.5% 是 PlantUML → FCSTM 的编译损失而非模型缺陷**，相对台账净增量仅 2 条。两条机制性结论：合式性层比 NL 点名层低 22.4pp（流水线只有 NL 驱动一个入口）；命中呈双峰分布（37 满格 / 23 零命中），`hit@3` 与 `hit@all` 差 22.4pp 说明瓶颈在稳定性。 | 🟢 |
| 2026-08-08 | [2026-08-08-导师-paper1收窄为issue-discover.md](./2026-08-08-导师-paper1收窄为issue-discover.md) | **本文库当前最高优先级依据。** 导师定调「**discover 部分单独成一篇文章**」「**repair 不会简单的，特别是要高质量 repair**」——paper1 收窄为 issue discover 单独成篇，repair 另立后续论文。contribution 改为谓词元模型 + 断言体系，外加「现有 detection 方法缺少错误上下文信息」这条差异化叙述。谓词由来按「从领域分析归纳、应用于 54 案例」表述。多 LLM 不追数量，围绕 motivation / contribution 定 RQ。 | 🟢 |
| 2026-07-07 | [2026-07-07-导师-paper1发现修正与BetterSTM归档.md](./2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | 第一篇不再以 Better STM / which STM is better 作为 active 评价框架，转向 source-level behavioral issue discovery and closure；`fcstm` 下沉为中间语义执行介质；R5.7 / Better STM-facing 资产应全量归档；baseline 按问题发现、已知问题修复 / 精化、黑盒端到端三层重排。⚠️ 其中 "and closure" 与 loop-as-contribution 已被 2026-08-08 记录覆盖；`fcstm` 定位与 Better STM 归档裁定仍有效。 | 🟡 |
| 2026-06-12 | [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇从 `NL -> STM` 生成转为 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正；`fcstm` / DSL 继续弱化为内部载体；baseline 转为 seed/source/converter/comparison；第二篇转向 agent-based SLR 方法学。其中 Better STM active framework 已被 2026-07-07 记录覆盖，但转向已有模型反馈修正、弱化 DSL、baseline 角色重排等背景仍有效。 | 🟡 |
| 2026-06-04 | [2026-06-04-导师-第一篇论文路线与E1E2定位.md](./2026-06-04-导师-第一篇论文路线与E1E2定位.md) | 第一篇更倾向 Path-1；Path-2 可拆成另一篇；E1/E2 是同一底座在自建 agent-loop 与成熟 agent 框架下的实验对照；弱化 `fcstm` 名称仍有效，但第一篇主任务边界已被 2026-06-12 和 2026-07-07 记录连续更新。 | 🟡 |

## 3. 当前高优先级约束

来源等级遵循 [GUIDE.md](./GUIDE.md) §3.1：导师直接表达 / 正式定调 > 用户明确决策 > 用户会后理解 / 待导师确认 > AI 执行建议。

| 约束 / 建议 | 来源等级 | 后续落点 |
|---|---|---|
| 第一篇论文优先推进并尽快进入可写作状态；一篇文章不能放太多内容，必须有明确 scope。 | 导师直接表达 / 正式定调 | paper1 R6/R7/R8 节奏、scope 与写作计划。 |
| paper1 contribution 不是状态机表达、`fcstm`、`pyfcstm` 或 DSL，而是 loop + diagnostics / simulation / formal verification feedback。 | 导师直接表达 / 正式定调 | title、abstract、contribution、method framing。 |
| 必须列举当前能仿真 / 验证的行为表达，并论证这些表达对控制系统行为和功能质量的重要性。 | 导师直接表达 / 正式定调 | model scope、motivation、method boundary、threats。 |
| 当前 active 主问题改为 source-level behavioral issue discovery and closure，不再问抽象的 “which STM is better”。 | 用户会后理解 / 待导师确认 | story、RQ、metric、baseline、experiment protocol。 |
| `fcstm` 只作为 intermediate semantic representation / executable medium；最终评价必须回到 raw/source issue、patch/projection/explanation。 | 导师直接表达 + 用户会后理解 | method boundary、run record、trace map、source-level projection。 |
| R5.7 / Better STM-facing 资产应全量迁入 `archive/r5_7_better_stm_snapshot/`，主路径不保留 Better STM 命名资产。 | 用户明确决策 | R6 前 archive 实施 PR；active 主路径清理。 |
| fold / ugly expression / guard-action-effect folded into event 不自动算 confirmed issue，只能作为 expression debt / semantic opacity / candidate trigger。 | 用户会后理解 + AI 执行建议 | reference issue ledger、issue taxonomy、baseline fairness。 |
| confirmed source-level issue 必须由 `NL + raw STM_0 + behavior evidence` 或 raw-internal inconsistency 支撑，不能由 `fcstm STM_k` 反向定义。 | AI 执行建议 / 待导师确认 | R7 reference ledger 构造协议。 |
| baseline 建议分三层：问题发现能力、已知问题下的修复 / 精化能力、完全黑盒端到端能力。 | 用户会后理解 + AI 执行建议 / 待导师确认 | R7 baseline matrix；R8 formal experiment。 |
| R6 应从 hot-start repair 改为 discover-and-refine pilot，至少补 issue ledger、trace map、source-level patch/projection、closure ledger、regression ledger。 | AI 执行建议 / 待导师确认 | R6 issue [#145](https://github.com/HansBug/research_ideas/issues/145) 与 agent-loop 实现。 |
| 第二篇转向带 human audit gates 的 agent-based SLR；需要调研 ASReview / RobotReviewer / SLR automation 等既有工作。 | 导师直接表达 + AI 执行建议 | 第二篇 planning issue / PR。 |
| 正式导师讨论记录必须区分【正式定调】、【用户会后理解】、【AI 衍生建议】和【待导师确认】，不得把 AI 补全写成导师原话。 | 维护纪律 | 后续 talks 文库更新。 |

## 4. 接下来建议动作

| 优先级 | 动作 | 说明 |
|---|---|---|
| P0 | 将 2026-07-07 记录发给导师或用于导师确认 | 重点确认 Better STM 是否归档、fcstm 是否只作中间介质、baseline 三层是否合理。 |
| P0 | 开 archive 实施 PR | 将 R5.7 Better STM-facing 资产全量迁入 archive snapshot，并保留 index / path mapping。 |
| P0 | 更新 R6 issue [#145](https://github.com/HansBug/research_ideas/issues/145) | 从 hot-start repair 改为 source-level discover-and-refine pilot。 |
| P1 | 重建 active issue / closure / regression-audit 文档 | 包括 source-level issue taxonomy、closure metrics、regression audit、source-level projection protocol。 |
| P1 | R7 前冻结 reference confirmed issue ledger 构造协议 | 必须盲态、冻结、可审计，避免 ours 结果反向污染 reference。 |
| P1 | R7 前冻结 baseline 三层协议 | 明确输入可见性、输出格式、评价分母、fairness 与 leakage 防护。 |

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 15:34:57 | 根据 multiagent review 修复来源等级口径：扩展 [GUIDE.md](./GUIDE.md) §3.1 为导师直接表达 / 用户明确决策 / 用户会后理解 / AI 执行建议四级，并同步本总账来源等级说明。 |
| 2026-07-07 15:17:40 | 新增 2026-07-07 导师讨论记录，更新第一篇主倾向为 source-level behavioral issue discovery and closure；将 2026-06-12 Better STM active framework 标记为被覆盖；新增 R5.7 Better STM-facing 资产全量归档、`fcstm` 中间介质、baseline 三层、confirmed issue 纪律和 R6/R7/R8 TODO。 |
| 2026-06-12 16:41:15 | 按三路 reviewer 的 I 级意见补充条目级来源等级、`Better STM` 最小操作化判定框架，并把 SUMMARY 当前约束改为带来源等级表格。 |
| 2026-06-12 16:20:42 | 新增 2026-06-12 导师讨论记录，更新第一篇为 `<NL, STM_0> -> STM_k / Better STM` 修正任务，并记录第二篇 agent-based SLR 转向；同步新增“正式定调 vs AI 衍生建议”维护纪律。 |
| 2026-06-04 15:04:00 | 根据三路 reviewer 的 M 级建议，补充单篇记录的 PR 状态说明、contribution 草案归属说明、关键上游 comment 深链与总账回填提示。 |
| 2026-06-04 14:45:00 | 初始化 project_1 正式导师讨论文库，新增 2026-06-04 讨论记录。 |

后续任何正式导师讨论的新增、更新或覆盖，均应在本更新日志首行插入新记录，并同步更新 §1 总体状态与 §2 记录列表。
