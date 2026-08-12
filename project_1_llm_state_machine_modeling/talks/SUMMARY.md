# project_1 正式导师讨论总账

## 1. 总体状态

| 字段 | 当前状态 |
|---|---|
| 正式导师讨论记录数 | **5**（另收 **4** 篇非导师记录：**3** 篇实验结论 + **1** 篇调研结论，见 §2） |
| 最近更新时间 | 2026-08-13 01:20:00 |
| 当前第一篇论文主倾向 | **STM issue discover，单独成篇**（2026-08-08 导师定调）。repair 另立后续论文，本篇只在讨论一节捎带提及 |
| `NL -> STM` 定位 | seed construction / baseline source / related work，不再作为第一篇主贡献 |
| `fcstm` / `pyfcstm` 定位 | intermediate semantic representation / executable medium，只服务 diagnostics / simulation / verification / refinement，不作为 paper1 contribution |
| Better STM 定位 | R5.7 阶段性评价框架；active headline framework 已被覆盖，Better STM-facing 资产应全量归档 |
| Path-2 定位 | 可作为后续控制系统差异化论文继续展开；不压进第一篇主线 |
| E1/E2 定位 | 同一方法底座或工具链在不同 agent 编排形态下的实验条件，不主打 Hybrid story |
| 当前核心贡献口径 | ⚠️ **三条**【用户明确裁定 2026-08-11】：① **基于模型转换 + 模型形式化检查 / 仿真 / 验证的模型错误发现方法**（⭐ 本条独有的是**真值封存**：断言执行完但真值封存，审查者只看得到可执行性、看不到真假）；② **基于归纳后的谓词逻辑的断言体系**（⚠️ 这一条**就是元模型本身**，只是从「用于构建断言」的角度陈述）；③ **issue 证据链体系**。⛔ **此前本行写「两条」，是 2026-08-08 的旧口径，已被取代。** ⛔ 另删去了原文的「天然具备覆盖性」——现行写法是「**覆盖性的分母来自需求侧**」，⚠️ 「全覆盖」是交给 LLM 的指令、由另一个 LLM 审查，其完整性**未测量**，⛔ 分母来自需求侧不等于分母完整。真源：[paper_stm_issue_discover/story/paper_story.md](../paper_stm_issue_discover/story/paper_story.md) §7。 |
| 谓词词表由来的论文口径 | 从**领域分析、真实文献与技术资料调研**归纳，应用于 54 个案例，并据此指导 prompt 设计。⛔ 不表述为"从这批 pair 归纳" |
| 建模对象边界 | $M = (S, E, V, Tr, A)$，不含时钟与正交区。fork/join 那份需求在**问题定义阶段**即落在界外，一句话带过，**不单开 RQ、不做辩护** |
| 第二篇当前倾向 | 从 `sources` 文库综述 / corpus paper 转向带 human audit gates 的 agent-based SLR 方法学与 benchmark / evidence-package 评价框架 |

## 2. 记录列表

状态口径：🟢 = 当前有效；🟡 = 部分被后续记录覆盖但仍有可复用背景；⚪ = 历史背景。状态列只写 emoji。

| 日期 | 记录 | 核心结论 | 状态 |
|---|---|---|---|
| 2026-08-12 | [2026-08-12-实验-为什么主臂比朴素基线低15个点.md](./2026-08-12-实验-为什么主臂比朴素基线低15个点.md) | **实验根因调查（⭐ 已更新至 v2 基准）。** 九路独立调查 + 两路 codex 交叉验证。⭐ **现行基准**：X1-v2（已去臂身份泄漏、完整材料重判）`hit@1` = 448/588 = **76.2%**，主臂 355 = **60.4%**，**Δ = −15.82pp**。⛔ **去掉泄漏后 X1 反而更高（+5 位），但那是 83 次双向翻转的残差、小于判定噪声。** ⭐⭐ **三个改变结论的发现**：(1) **形式化规约有人类基线且比我们低**——Czepa（N=215）受训人类 + pattern 辅助只有 **47–50%**、不用 pattern 仅 28–31%；⛔ **不可与我们的 60.4% 直接相减**（任务/分母/人群/评分四项均不同，四条限定见 talk §10.5.1）；(2) **脚手架类型决定符号**——Huang（ICLR 2024）自我纠正使 Llama-2 **−27.5pp**、GPT-4 仅 −2.0pp，⭐ 而我们的 ROI 数据独立吻合（两个 reviewer 第 3–5 轮**恰好零位**、79% token 覆盖净变化≈0；`precheck_and_seal` 0 token 性价比最高）；(3) ⛔ **Stroebl 不可能性定理**（arXiv:2411.17501）——验证器不完美时弱模型的任何推理扩展都追不上强模型，⭐ 唯一出路是换 **sound oracle**。⭐ **v47 最小改动集 < 100 行、预计 +11~17pp 且成本降 19%**，其中最硬的两条：**schema 把结论排在理由前（75 条流式实测 25/25，禁掉了 CoT，+6.8~9.2pp）** 与 **splitter prompt 95,589 字符把任务埋在中间**。⛔ 台账正在全量人工重标（54 份工作单、33–49 人时），**在它完成前不要锁定选题**。 | 🟢 |
| 2026-08-12 | [2026-08-12-实验-X1朴素基线对照臂与八轮口径尝试.md](./2026-08-12-实验-X1朴素基线对照臂与八轮口径尝试.md) | **实验结论记录，非导师意见。** ⛔ **朴素基线（一次提示）在覆盖率与精度两侧都高于主臂**：`hit@1` 75.3% vs 60.4%（**Δ = −14.9pp**）、`hit@3` 81.6% vs 70.9%、`hit@all` 67.3% vs 48.5%；已认领率 59.6% vs 31.7%；**假阳性负担平手**（**0.052** vs 0.056；⚠️ 原记 0.051，⛔ 那用了复核前的 449 分母，⭐ 正确分母是 443）——而成本是主臂的 **1/212**。⭐ 逐位对拍排除「判定宽松」：仅主臂命中 86 位 / 仅 X1 命中 174 位，是**能力正交**而非一边放宽。随后**八轮**独立判据尝试（可断言性 98.4% vs 99.2%、下游就绪度组间跨度 26.4pp > 臂间差 17.3pp、形态对照设计错误、文献只能类比）**全部失败**，且⭐⭐ **八次失败收敛到同一机制**：任何「基线缺少 X」的静态判据，只要 X 是主臂的输出格式，方差就被**需求文本**与**缺陷类型**吃掉——而那两样对两臂共同。⚠️ 另查实**约 30% 主臂命中位建立在模型自造标识符上**（对主臂不利）。⭐ 建议：论文有效性主张整体转向**交付形态 + 成本**。⛔⛔ **本篇的「同判定链」「判定伪影 2.7–4.1pp」「98.2% 可断言」三条已被同日根因调查推翻，见上一行；其余内容仍有效。** | 🟡 |
| 2026-08-12 | [2026-08-12-调研-paper1相关工作版图与竞争定位.md](./2026-08-12-调研-paper1相关工作版图与竞争定位.md) | ⭐ **调研结论记录，非导师讨论。** L1 轨五问全部落档（覆盖 14467 条题录）。⭐⭐ **竞争者只有 1 篇（MCeT, MODELS 2025），⛔ 但它的任务形状与本文逐项对应、自称 first、且把本文要做的事点名为 future work。** ⭐ 差异化收窄为三条：**缺口挂在「需求 × 这份模型」那一格上**（⚠️ 既有工作也记缺口，⛔ 但挂的是规约语言能力）· 裁决在被判对象上求值 · 可重放。⛔ **C-① 新颖性上限「与既有工作不同」；C-③「有没有证据链」这个形状站不住。** ⚠️ 一条导师决策项：X1 复刻的恰好是 MCeT 已量过的弱臂 | 🟢 |
| 2026-08-12 | [2026-08-12-导师-谓词词表的出处根基与C3差异化.md](./2026-08-12-导师-谓词词表的出处根基与C3差异化.md) | ⭐ **汇报材料，非导师意见；自包含。** 回答「19 条谓词凭什么是这 19 条」。74 路检索 / 送审 782 条 / 裁定存活 418 条 → 按出版物去重 **360 独立来源**，**17/19 达 ≥6 源**，分类 **① 12 · ② 6 · ③ 1**（唯一的 ③ 是 `containment`）。⭐ 证据轴定为**普遍性而非符合性**；② 依据 **UML 抽象语法**且只豁免「名字是否悬空」那一层。⭐ C-③ 的 gap 陈述改为「**判据与追溯各自成熟，而 NL→判据这一跳在每个社区都是人的行为、从未被机器检查**」（六处独立自证）。⛔ **C-③ 定第三档「与既有工作不同」**——核实发现 SLDV 的 dead logic 已在 STM 空间做到 transition 粒度锚点 + 具名可重算判据。⛔ 七条局限，其中「词表由评测语料决定（transductive）」与「仅 3/19 有强形式普遍性」直接限定可主张范围。⚠️ 与同日 L1 记录并读：MCeT 的任务形状与本文对应，差异化须落到 L1 §5 那三条上。 | 🟢 |
| 2026-08-10 | [2026-08-10-实验-v46全量矩阵双侧结论.md](./2026-08-10-实验-v46全量矩阵双侧结论.md) | **实验结论记录，非导师意见。** 一次完整实验 324 格：覆盖侧 `hit@1` 355/588 = 60.4%（**必须标为上界**）、`hit@3` 70.9%、`hit@all` 48.5%；多报侧 288 条目 / 124 去重，**最大成分 46.5% 是 PlantUML → FCSTM 的编译损失而非模型缺陷**，相对台账净增量仅 2 条。两条机制性结论：合式性层比 NL 点名层低 22.4pp（流水线只有 NL 驱动一个入口）；命中格数向两端聚集（满格 37 / 近满格 13 / 不稳定 25 / 零命中 23 = 98；⛔ 不写「双峰」，局部极大实为 0/3/6 三个），`hit@3` 与 `hit@all` 差 22.4pp 说明瓶颈在稳定性。 | 🟢 |
| 2026-08-08 | [2026-08-08-导师-paper1收窄为issue-discover.md](./2026-08-08-导师-paper1收窄为issue-discover.md) | **本文库当前最高优先级依据。** 导师定调「**discover 部分单独成一篇文章**」「**repair 不会简单的，特别是要高质量 repair**」——paper1 收窄为 issue discover 单独成篇，repair 另立后续论文。contribution 改为谓词元模型 + 断言体系，外加「现有 detection 方法缺少错误上下文信息」这条差异化叙述。谓词由来按「从领域分析归纳、应用于 54 案例」表述。多 LLM 不追数量，围绕 motivation / contribution 定 RQ。 | 🟢 |
| 2026-07-07 | [2026-07-07-导师-paper1发现修正与BetterSTM归档.md](./2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | 第一篇不再以 Better STM / which STM is better 作为 active 评价框架，转向 source-level behavioral issue discovery and closure；`fcstm` 下沉为中间语义执行介质；R5.7 / Better STM-facing 资产应全量归档；baseline 按问题发现、已知问题修复 / 精化、黑盒端到端三层重排。⚠️ 其中 "and closure" 与 loop-as-contribution 已被 2026-08-08 记录覆盖；`fcstm` 定位与 Better STM 归档裁定仍有效。 | 🟡 |
| 2026-06-12 | [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇从 `NL -> STM` 生成转为 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正；`fcstm` / DSL 继续弱化为内部载体；baseline 转为 seed/source/converter/comparison；第二篇转向 agent-based SLR 方法学。其中 Better STM active framework 已被 2026-07-07 记录覆盖，但转向已有模型反馈修正、弱化 DSL、baseline 角色重排等背景仍有效。 | 🟡 |
| 2026-06-04 | [2026-06-04-导师-第一篇论文路线与E1E2定位.md](./2026-06-04-导师-第一篇论文路线与E1E2定位.md) | 第一篇更倾向 Path-1；Path-2 可拆成另一篇；E1/E2 是同一底座在自建 agent-loop 与成熟 agent 框架下的实验对照；弱化 `fcstm` 名称仍有效，但第一篇主任务边界已被 2026-06-12 和 2026-07-07 记录连续更新。 | 🟡 |

## 3. 当前高优先级约束

来源等级遵循 [GUIDE.md](./GUIDE.md) §3.1：导师直接表达 / 正式定调 > 用户明确决策 > 用户会后理解 / 待导师确认 > AI 执行建议。

| 约束 / 建议 | 来源等级 | 后续落点 |
|---|---|---|
| 第一篇论文优先推进并尽快进入可写作状态；一篇文章不能放太多内容，必须有明确 scope。 | 导师直接表达 / 正式定调 | paper1 R6/R7/R8 节奏、scope 与写作计划。 |
| ⛔ **已作废（2026-08-11）**：~~paper1 contribution 不是状态机表达、`fcstm`、`pyfcstm` 或 DSL，而是 loop + diagnostics / simulation / formal verification feedback。~~ ⚠️ 这条**曾被标为「导师直接表达 / 正式定调」，但它已被 2026-08-07 / 08-08 的收窄定调取代**，且现行 `paper_story.md` §13 的**禁语表**逐字列着「贡献是 feedback loop + verification feedback —— 已被 2026-08-07 / 08-08 定调取代」。⛔ 保留原文划删只为留痕，⛔ 不得再据此写 title / abstract / contribution。现行三条见本表「当前核心贡献口径」行。 | ⛔ 已被取代 | ⛔ 不再适用 |
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
