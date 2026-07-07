# 2026-07-07 导师讨论：paper1 从 Better STM 转向 source-level 问题发现与闭合

## 1. 执行摘要

本记录沉淀 2026-07-07 前后围绕 paper1 最新导师讨论转录与会后复盘形成的路线校准。它覆盖 [2026-06-12 导师记录](./2026-06-12-导师-两篇论文转向与模型修正定调.md) 中把第一篇主任务表述为 `<NL, STM_0> -> STM_k / Better STM` 的 active evaluation 框架，但不否定该记录中关于“弱化 `fcstm` / DSL 名头”“从 `NL -> STM` 生成转向已有模型修正”“baseline 角色重排”“反馈循环是核心”的背景判断。

本次更新的核心结论是：

1. **【正式定调 / 按用户转录的导师直接表达】paper1 要尽快推进和撰写，不能把一篇文章塞进过多内容；应明确列举当前能做仿真 / 形式化验证的行为表达，并论证这些表达对控制系统行为质量的重要性。**
2. **【正式定调 / 按用户转录的导师直接表达】paper1 的 contribution 不是状态机建模语言、不是 `fcstm` / `pyfcstm` / DSL，而是 loop + diagnostics / simulation / formal verification feedback。**
3. **【用户会后理解 / 明确决策】`fcstm` 应进一步下沉为中间语义执行介质：它帮助把 raw/source 状态机 lifting 到可检查、可执行、可验证的中间表示；最终评价必须回到 raw/source 状态机层，说明发现并修复了哪些原模型行为问题。**
4. **【用户明确决策】Better STM 不再作为 paper1 active headline evaluation framework；R5.7 / Better STM-facing 资产应全量迁入 archive snapshot，主路径不保留 Better STM 命名资产。**
5. **【执行建议 / 待导师确认】新的 active framework 应从“which STM is better”转为“source-level behavioral issue discovery and closure”：给定 `NL + raw STM_0`，方法能否发现 raw `STM_0` 中可确认的行为问题，并在不引入关键回归的前提下闭合这些问题。**

一句话概括新的 paper1 主线：

> 给定自然语言需求与已有 raw/source 状态机，paper1 研究一个基于语义中间表示、确定性诊断、仿真和轻量形式化验证反馈的 agent loop，能否发现原模型中的 source-level 行为问题，生成可追溯的修正，并回到原模型表达层证明这些问题被闭合且没有引入关键回归。

本记录是后续 R6 / R7 / R8 的高优先级约束：若它与 R5.7 Better STM 文档、旧 PR body、旧 issue 计划或内部讨论冲突，默认以本记录为准；若后续导师再次明确更新，则以更晚导师记录覆盖。

---

## 2. 讨论背景与上游入口

### 2.1 当前 paper1 状态

讨论发生时，paper1 已完成以下阶段性工作：

1. 已从 `NL -> STM` 生成主线转到给定 `<NL, STM_0>` 后的反馈驱动修正主线。
2. 已围绕 `llms-emp-stm-subset` 建立 10 个唯一 NL cluster × 6 个 LLM-generated STM 输出 = 60 raw pairs 的主池画像。
3. 已完成 raw / canonical / `.fcstm` 表示桥、转换 readiness、R5.7 Better STM 评价逻辑、constructed `STM_k` cases 和 blind adjudication dry-run。
4. 正准备进入 R6，计划复用既有 agent loop，但需要从旧 `NL -> STM` 生成链路调整为已有模型上的 discovery + refinement 链路。

### 2.2 关键上游链接

| 类型 | 链接 | 用途 |
|---|---|---|
| 当前伞 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) | paper1 新主线 staged umbrella，总施工入口。 |
| 本轮战略校准 subPR | [#146](https://github.com/HansBug/research_ideas/pull/146) | 本记录落库前的自包含战略理解稿与 review 入口。 |
| R6 planning issue | [#145](https://github.com/HansBug/research_ideas/issues/145) | 后续应按本记录改写为 source-level discover-and-refine pilot。 |
| R5.7 上游 PR | [#138](https://github.com/HansBug/research_ideas/pull/138) | Better STM / repair target 合同历史入口；后续应全量 archive。 |
| R5.7.5 dry-run PR | [#143](https://github.com/HansBug/research_ideas/pull/143) | constructed `STM_k` + blind adjudication dry-run 资产历史入口。 |
| archive-first 口径 comment | [#146 comment](https://github.com/HansBug/research_ideas/pull/146#issuecomment-4900393564) | 明确 R5.7 / Better STM-facing 资产全量归档、主路径清理。 |
| 独立 reviewer archive check | [#146 comment](https://github.com/HansBug/research_ideas/pull/146#issuecomment-4900384221) | 上下文独立核查 archive-first 口径是否清晰。 |
| 上一条正式导师记录 | [2026-06-12 记录](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | 被本记录部分覆盖；仍保留第一篇从 `NL -> STM` 转向反馈修正的背景价值。 |

---

## 3. 信息来源与确认等级

本记录基于用户在当前会话中粘贴的导师讨论转录、用户会后理解、随后围绕 #146 的内部复盘和 multiagent review 整理而成。它不是逐字录音稿，因此必须显式区分不同来源等级。

| 信息 | 来源等级 | 本记录中的处理 |
|---|---|---|
| paper1 优先推进、尽快出东西和撰写。 | 【正式定调 / 按用户转录的导师直接表达】 | 作为 R6/R7/R8 节奏约束：不再无限发散评价体系。 |
| 一篇文章不能放太多内容，要有范围设定。 | 【正式定调 / 按用户转录的导师直接表达】 | paper1 只覆盖当前可仿真 / 可验证的行为表达；其他行为表达留 future work。 |
| 列举当前能做仿真 / 形式化验证的行为表达，并论证其重要性。 | 【正式定调 / 按用户转录的导师直接表达】 | R6/R7 需要把支持的 guard/action/effect/target/trace 等行为表达列入 scope 与 motivation。 |
| paper1 contribution 不是状态机模型表达，而是 loop + simulation + formal verification / diagnostics。 | 【正式定调 / 按用户转录的导师直接表达】 | `fcstm` 不进 contribution 位；方法贡献写 feedback loop。 |
| 最终要回到 raw/source 模型层说明 `STM_k` 相对 `STM_0` 解决了什么问题。 | 【正式定调 + 用户会后理解】 | 需要 source-level issue ledger、trace map、patch/projection/explanation 与 closure ledger。 |
| Better STM 主框架应归档。 | 【用户明确决策】 | 本记录将 R5.7 Better STM-facing 资产定位为 archive snapshot，不作为 active framework。 |
| baseline 三层策略。 | 【用户复盘 + AI 执行建议】 | 作为 R7 protocol 默认起点，仍建议导师确认。 |
| 新框架命名与指标细节。 | 【AI 衍生建议 / 待导师确认】 | 只能作为后续 PR 起点，不能写成导师已确认。 |

写作纪律：后续向导师汇报时，应表述为“这是我对讨论内容和后续执行路径的理解，请老师确认是否正确”，不得写成“导师已经批准全部细节”。

---

## 4. 对 2026-06-12 主线的覆盖关系

[2026-06-12 导师记录](./2026-06-12-导师-两篇论文转向与模型修正定调.md) 的核心作用是把第一篇从 `NL -> STM` 生成转到 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正。当时为了让评价对象可操作，使用了 “Better STM” 作为阶段性抽象。

本次讨论后的覆盖关系如下：

| 2026-06-12 口径 | 本次处理 | 原因 |
|---|---|---|
| 第一篇不再主打 `NL -> STM` 生成。 | 保留 | 仍是当前主线基础。 |
| 给定 `NL + STM_0` 后做反馈驱动修正。 | 保留并改写为 source-level discovery + closure | 仍研究已有模型的改进，但评价不再问抽象的“哪个 STM 更好”。 |
| Better STM 是主评价框架。 | 覆盖 / 归档 | “better” 太抽象，容易滑向建模语言质量或 specification quality 论文。 |
| 弱化 `fcstm` / DSL 名头。 | 加强 | 不只是“不提 `fcstm`”，而是把它明确定位为中间语义执行介质。 |
| baseline 转为 seed/source/converter/comparison。 | 保留并细化 | 需要进一步分成 issue discovery、known issue repair/refinement、black-box end-to-end 三层。 |
| repair-loop evaluation 覆盖 `STM_0` vs `STM_k`。 | 改写 | 不直接比较“哪个更好”，而是统计 confirmed issues 的发现、闭合与回归。 |

因此，2026-06-12 记录当前状态应视为 **部分有效**：它仍提供转向已有模型修正的背景，但其 Better STM active framework 已被本记录覆盖。

---

## 5. 为什么 Better STM 不再适合作为 active framework

### 5.1 阶段性价值

R5.7 的 Better STM 框架不是无效工作。它迫使我们明确了以下重要纪律：

1. candidate validity 与 method effectiveness 要分开。
2. conversion readiness、parse/semantic validity、diagnostics 减少不能自动等价于语义改进。
3. 构造 `STM_k` dry-run 只能校准 adjudication protocol，不能当作真实 repair-loop 输出。
4. no-regression、scope gate、attribution boundary、anti-gaming cases 对后续仍有启发。

### 5.2 审稿风险

但如果继续把 Better STM 作为 paper1 主问题，会产生强审稿风险：

1. **概念过抽象**：reviewer 会追问 “better” 是语义更好、表达更细、可执行性更强，还是只是 `fcstm` 表达力更强。
2. **容易变成 modeling language 论文**：当我们强调 guard/action/effect 从 event label 中展开时，问题会滑向“哪种建模语言更合适”，而不是“方法是否发现并修复原模型行为问题”。
3. **混淆 expression debt 与 model issue**：把 guard folded into event 直接算作模型问题，会被质疑只是表达介质差异。
4. **评价对象错位**：如果最终 judge 只比较 `fcstm STM_0` 与 `fcstm STM_k`，就没有回到 raw/source 模型层证明原模型哪里错、怎么被修。
5. **论文 scope 失控**：定义“什么是更好的 specification”本身太大，容易偏离导师要求的 loop + simulation + formal verification feedback 贡献。

### 5.3 本轮决策

**【用户明确决策】**：Better STM 不再作为 paper1 active headline evaluation framework；R5.7 / Better STM-facing 资产应全量归档，主路径保持干净。

建议归档路径：

```text
project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/
```

归档原则：

1. R5.7 definition、taxonomy、metrics、adjudication protocol、dry-run examples、blind prompts、reports、handoff、anti-gaming cases 等 Better STM-facing 资产全部迁入 archive snapshot。
2. active 主路径不保留 `better_stm_*` 命名资产。
3. 仍有价值的纪律只能重新提炼、重命名，写入新的 source-level issue discovery / closure / regression-audit 文档。
4. archive 不是垃圾桶；需要保留 README / index / 原路径映射 / 迁移说明，以便审计 R5.7 为什么被 superseded。

---

## 6. 新 active framework：source-level behavioral issue discovery and closure

### 6.1 新主问题

旧问题：

```text
Which is better: STM_0 or STM_k?
```

新问题：

```text
What confirmed source-level behavioral issues exist in raw STM_0?
Can the method discover them?
Can the method close them without introducing critical regressions?
```

### 6.2 输入、方法与输出

```text
Input:
  NL + raw STM_0

Method:
  raw STM_0
    -> semantic lift / fcstm-like intermediate representation
    -> deterministic diagnostics / inspect
    -> scenario simulation / trace feedback
    -> lightweight formal verification feedback where available
    -> issue discovery
    -> candidate refinement / repair
    -> regression check and acceptance / rollback
    -> source-level patch / projection / explanation

Output:
  source-level issue ledger
  raw-to-intermediate trace map
  intermediate change ledger
  source-level patch / projection / explanation
  issue closure ledger
  regression ledger
  auditable run record
```

核心变化是：`fcstm STM_k` 不再是最终评价对象。它只是中间制品；最终必须解释 raw/source `STM_0` 中哪个元素出了什么行为问题、方法如何发现、修改如何投影回 raw/source 层、该问题是否闭合、是否引入新问题。

### 6.3 关键 ledger

| 产物 | 最低内容 | 作用 |
|---|---|---|
| source-level issue ledger | `issue_id`、raw element、NL span、issue type、evidence、severity、status | 冻结“原模型有什么问题”。 |
| raw-to-intermediate trace map | raw transition/state/event 与中间表示元素映射 | 防止中间表示变化无法回到原模型。 |
| intermediate change ledger | loop 在中间表示中增加、删除、调整了什么 | 记录方法真实动作。 |
| source-level patch / projection / explanation | 回到 raw/source 层说明应如何改 | 支撑与 baseline、公平评价和导师沟通。 |
| closure ledger | 每个 confirmed issue 是否 closed / partially closed / not closed / over-repaired | 替代 Better STM verdict。 |
| regression ledger | 新引入问题、关键回归、不支持语义、过修 | 防止只报成功闭合。 |

---

## 7. 什么才算 source-level confirmed issue

### 7.1 关键纪律

**fold / ugly expression 不自动算 confirmed issue。**

例如，raw PlantUML 或 SysML-like 状态机把本应是 guard/action/effect 的内容折成 plain event label，这可能说明表达不优雅、语义不透明、转换需要更谨慎，但它本身不等于模型语义错误。

可以使用以下区分：

| 情况 | 是否计入 confirmed issue | 说明 |
|---|---|---|
| `A -> B : Event("x should gt 0")`，但 NL 没有足够证据说明行为错误。 | 否 | 只能算 expression debt / semantic opacity。 |
| NL 明确要求只有 `x > 0` 才能迁移，但 raw 模型允许无条件迁移。 | 是 | raw 行为允许了需求禁止的路径。 |
| raw 中 guard 条件方向与 NL 相反。 | 是 | 可由 NL + raw element 直接确认。 |
| raw 内部存在互斥 guard、不可达状态、死迁移等。 | 是 | 即使不依赖完整 NL，也可由模型内部一致性确认。 |
| 中间 `fcstm` 展开后更结构化、更可执行。 | 否 | 这是 representation gain，不自动是 source-level issue closure。 |

### 7.2 confirmed issue 判定原则

一个条目升级为 confirmed source-level issue，至少应满足以下之一：

1. **NL-grounded mismatch**：NL 明确要求某行为，但 raw `STM_0` 缺失、反向表达或错误表达。
2. **raw-internal inconsistency**：raw `STM_0` 内部存在不可达、死 guard、冲突迁移、错误目标、缺失终止路径等结构 / 行为矛盾。
3. **safety / control obligation violation**：raw 行为会违反控制系统关键功能、安全义务或故障处理约束。
4. **human-adjudicated source issue**：经独立标注 / 裁决，确认不是表达债，而是原模型行为问题。

### 7.3 举例

| issue 类型 | NL / raw 示例 | 为什么是真问题 |
|---|---|---|
| 缺少 guard | NL：微波炉只有门关闭才可开始加热；raw：`Idle -> Cooking : Start` | raw 允许门开时开始加热，违反安全约束。 |
| guard 方向错误 | NL：`distance < 10` 时刹车；raw：`Cruise -> Brake : distance > 10` | 条件方向与需求相反。 |
| 缺少 effect | NL：支付成功后打印票据；raw：`Payment -> Done : PaymentSuccess`，无 print action / printed state | 缺失需求要求的系统输出。 |
| 错误目标状态 | NL：EmergencyStop 进入 SafeStop；raw：`Moving -> Idle : EmergencyStop` | 若 Idle 非 SafeStop，则紧急停止语义错误。 |
| 内部不一致 | raw：`A -> B : go [x > 5 && x < 3]` | guard 不可满足，迁移死掉。 |
| 折叠表达但未证实错误 | raw：`A -> B : Event("door closed start")` | 可能只是表达粗糙；不能自动计入 confirmed issue。 |

---

## 8. baseline 三层对比策略

本节为 **【用户复盘 + AI 执行建议】**，建议在 R7 前向导师确认并冻结。

### 8.1 层次 1：问题发现能力

目标：比较谁更能发现 raw `STM_0` 中真实存在的 source-level behavioral issues。

```text
Baseline:
  Input: NL + raw STM_0
  Method: 直接让 LLM / reviewer 在 raw STM_0 上找问题
  Output: discovered issue list

Ours:
  Input: NL + raw STM_0
  Method: raw -> intermediate -> diagnostics / simulation / verification feedback -> issue discovery
  Output: discovered issue list + evidence
```

评价：以冻结的 reference confirmed issue ledger 为准，计算 issue precision / recall / F1、spurious issue rate、issue type coverage。该层证明的是“语义中间表示 + 工具反馈是否让问题发现更有效”。

### 8.2 层次 2：已知问题下的修复 / 精化能力

目标：在问题已知的情况下，比较谁更能闭合问题且不引入关键回归。

```text
Baseline:
  Input: NL + raw STM_0 + known confirmed issues
  Method: 直接让 LLM / baseline 在 raw STM_0 上修
  Output: raw-level patch / revised raw STM / explanation

Ours:
  Input: NL + raw STM_0 + same known confirmed issues
  Method: semantic lift -> feedback-guided refinement -> source-level projection
  Output: source-level patch / projection / explanation + closure ledger
```

评价：issue closure rate、partial closure rate、over-repair rate、critical regression rate、source patch traceability。该层变量较少、可控性强，可能最适合作为主 baseline。

### 8.3 层次 3：黑盒端到端能力

目标：比较完整流程解决问题的能力。

```text
Baseline:
  Input: NL + raw STM_0
  Method: 直接发现并修复 raw STM_0
  Output: revised raw artifact + explanation

Ours:
  Input: NL + raw STM_0
  Method: discover-and-refine loop
  Output: issue ledger + source-level patch/projection + closure/regression ledger
```

评价：discovered-and-closed confirmed issues、regression-free closure rate、invalid output rate、cost、retry、rollback、non-convergence。该层最贴近最终 claim，但变量最多，建议作为 R8 主实验或补充实验，而不是 R6 首轮就强行完全跑通。

### 8.4 baseline 纪律

1. baseline 必须在 raw/source `STM_0` 层操作；ours 可以使用 `fcstm` 作为中间语义执行介质。
2. 如果 ours 的输出只停留在 `fcstm STM_k`，没有 source-level projection，就不能与 raw baseline 公平比较。
3. reference issue ledger 必须在正式实验前冻结，不能让 ours 的发现结果反向定义 reference。
4. known issue repair baseline 必须给 baseline 与 ours 相同的 known issues，避免 ours 因先发现问题而在修复阶段占信息优势。
5. conversion / lowering / normalization gain 不得计入 repair / closure gain。

---

## 9. 对 R6 / R7 / R8 的影响

### 9.1 R6：从 hot-start repair 改为 discover-and-refine pilot

R6 不应只产出 `fcstm STM_k`，而应至少验证以下骨架：

1. `raw STM_0 -> intermediate representation` 带 trace binding。
2. source-level issue ledger schema。
3. issue discovery output schema。
4. source-level patch / projection / explanation schema。
5. issue closure ledger schema。
6. regression ledger schema。
7. run record 中记录 raw hash、intermediate hash、candidate hash、trace map、patch path、closure status、regression status。

R6 是 feasibility / pilot，不应报告正式主结果。

### 9.2 R7：冻结评价协议与 baseline

R7 应从旧 Better STM protocol 改为冻结：

1. reference confirmed issue ledger 构建协议。
2. issue discovery metrics。
3. issue closure metrics。
4. regression audit metrics。
5. baseline 三层协议与公平性控制。
6. source-level projection / patch / explanation 验收标准。
7. T0 / T0.5 / T1 scope 与 supported behavior expression 边界。

### 9.3 R8：正式实验

R8 才执行正式实验：

1. LLMS-EMP 60 cases 中的 eligible subset。
2. 自有 NL + 复现 / 直接运行 NL2STM 生成的 additional cases。
3. direct raw baseline 与 ours 的 issue discovery / known issue repair / black-box end-to-end 对比。
4. failure、partial、unresolved、regression、over-repair 全部入账。

---

## 10. 接下来大致 TODO

### 10.1 立即要做

1. **落库本导师讨论记录**：新增本文，并同步 [README.md](./README.md) 与 [SUMMARY.md](./SUMMARY.md)。
2. **更新 #146**：把 #146 从“仅 PR body contract”推进为“正式导师 talks 记录落库 PR”，列出新增 / 更新文件和验收标准。
3. **同步 #100**：在伞 PR 中说明 #146 已开始长期文档落库，后续 R6/R7/R8 以本记录为优先约束。
4. **multiagent review**：要求 reviewer 独立检查本文是否自包含、是否区分导师意见 / 用户理解 / AI 建议、是否把 Better STM 全量归档口径讲清楚。

### 10.2 R6 前必须做

1. 开 archive 实施 PR：将 R5.7 Better STM-facing 资产全量迁入 `archive/r5_7_better_stm_snapshot/`，保留 README / index / 原路径映射。
2. 清理 active 主路径：不再保留 Better STM 命名资产。
3. 重建 active source-level 文档：source-level issue taxonomy、closure metrics、regression audit、source-level projection protocol。
4. 更新 R6 planning issue [#145](https://github.com/HansBug/research_ideas/issues/145)：从 hot-start repair 改为 discover-and-refine pilot。
5. 调整 agent loop 接口：确保输出 issue ledger、patch/projection、closure ledger、regression ledger，而不是只输出 `fcstm STM_k`。

### 10.3 R7 / R8 前必须做

1. 盲态构建 reference confirmed issue ledger：构建者只能看 `NL + raw STM_0 + raw source metadata`，不得看 ours 的诊断、修复、`STM_k`。
2. 冻结 baseline 三层协议：至少明确层次 1、层次 2、层次 3 的输入可见性、输出格式、裁决方式和指标。
3. 冻结 source-level patch/projection 验收标准。
4. 冻结 supported behavior expression scope：当前能仿真 / 验证哪些行为表达，哪些留 future work。
5. 设计 failure reporting：未发现、误报、未闭合、过修、回归、不收敛都要入账。

### 10.4 需要导师确认的问题

1. 是否同意 paper1 正式放弃 Better STM / which STM is better 作为 active headline evaluation framework？
2. 是否同意新的主问题写成 source-level behavioral issue discovery and closure？
3. 是否同意 `fcstm` 只作为 intermediate semantic representation / executable medium，最终评价回到 raw/source issue 与 patch/explanation？
4. 是否同意 baseline 三层：问题发现、已知问题修复 / 精化、黑盒端到端？
5. 是否同意 R6 先做 discover-and-refine pilot，而不是直接跑正式实验？
6. 是否同意 R5.7 Better STM-facing 资产全量归档，主路径只保留新框架资产？
7. paper 标题 / 方法命名应更偏向 “behavioral issue discovery and refinement” 还是 “semantic-feedback-guided refinement”？

---

## 11. 可直接复用的 paper story 草案

### 11.1 保守 thesis

> Existing LLM-based modeling workflows can produce state-machine artifacts, but these artifacts often contain source-level behavioral issues that are hard to diagnose and repair from textual labels alone. We study a feedback-driven discover-and-refine loop that lifts raw state-machine artifacts into an executable semantic intermediate representation, uses deterministic diagnostics, simulation, and lightweight verification feedback to discover behavioral issues, and projects repairs back to the source level with closure and regression evidence.

### 11.2 中文贡献边界

本文不是提出一个新状态机建模语言，也不是证明 `fcstm` 比 PlantUML / SysML 更好。本文贡献在于：

1. 定义并研究已有状态机制品上的 source-level behavioral issue discovery and closure 任务。
2. 设计一个借助中间语义执行表示、diagnostics、simulation、formal verification feedback 的 discover-and-refine loop。
3. 建立 source-level issue ledger、closure ledger、regression ledger 和 source-level patch/projection 证据链。
4. 通过 raw baseline 与 ours 的问题发现 / 已知问题修复 / 黑盒端到端对比，证明工具反馈和语义执行介质对发现与闭合行为问题的价值。

### 11.3 必须避免的 claim

1. 避免说“我们提出 fcstm / pyfcstm 作为新 DSL”。
2. 避免说“我们的 STM 一定更好”而不解释 better 的证据。
3. 避免把 folded guard/action label 直接算成 confirmed issue。
4. 避免把 conversion / normalization 的收益算成 repair-loop 贡献。
5. 避免把 R5.7 constructed `STM_k` blind dry-run 写成真实 method effectiveness。

---

## 12. 维护说明

本记录进入 `project_1_llm_state_machine_modeling/talks/` 后，应作为 project_1 第一篇最新高优先级路线记录使用。后续若导师对本记录中“待确认”的 baseline、命名、R6/R7/R8 执行顺序或 archive-first 口径提出修正，应新增一条更晚的导师记录或更新 [SUMMARY.md](./SUMMARY.md) 中的覆盖关系，不应只留在 PR comment 中。
