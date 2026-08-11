# R8 论文叙事快照（cold archive）

> **Cold archive / 冻结的一版叙事骨架 / 内容仍然可用。**
> 本目录保存 2026-08-11 凌晨那一版 `story/`——七份论文叙事文件，
> 已经按「paper1 只做 issue discover」的口径整体重写过。
>
> ⚠️ **它不是 repair 期遗物，不要按「过时资产」读。** 归档理由见 §2。

## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原路径 | `paper_stm_issue_discover/story/` |
| 内容冻结时间 | 2026-08-11 凌晨（七份文件的 §「相对上一版改了什么」记录了那次重写的逐条动机） |
| 归档时间 | 2026-08-11 |
| 归档动作 | `git mv story archive/r8_discover_repair_story/story`，7 个文件全部为 rename，内容未改；只机械调整了相对链接深度（详见 §6） |
| 内容口径 | 已是 discover-only 口径；2026-08-07 / 08-08 导师定调已吸收 |

## 1. 这是什么

paper1 的论文叙事真源：thesis、两条 contribution、章节骨架与 RQ、claim–证据对照、
任务边界、建模对象 $M = (S, E, V, Tr, A)$、术语与禁用词。七份：

| 文件 | 行数 | 一句话 |
| :-- | --: | :-- |
| [story/README.md](./story/README.md) | 99 | 叙事入口、文件职责表、上游事实源五级优先级 |
| [story/paper_story.md](./story/paper_story.md) | 279 | 叙事主干：问题 / 价值 / 现有方法的三条 gap / 核心洞察 / 两条 contribution / 可说与不可说的话 / 审稿人风险 |
| [story/paper_outline.md](./story/paper_outline.md) | 344 | §1–§10 章节结构，含四个 RQ 与每节验收判据 |
| [story/claim_evidence_map.md](./story/claim_evidence_map.md) | 220 | C1–C15 逐条 claim 的证据、强度档、允许 / 禁止写法 |
| [story/task_boundary.md](./story/task_boundary.md) | 120 | 输入输出、方法内八阶段、人类角色、五种失败与不确定状态 |
| [story/model_scope.md](./story/model_scope.md) | 115 | 建模对象五元组、硬边界、可断言的行为表达、禁止外推 |
| [story/terminology_policy.md](./story/terminology_policy.md) | 157 | 四组易混术语、指标写法、禁用词、中英一致性 |

## 2. 为什么归档

**不是因为内容过时，也不是因为它属于 repair 期。** 这一版是 2026-08-11 凌晨在时间压力下
一次性赶出来的：口径对、密度高，但骨架是那一夜按当时手头的材料现搭的，没有经过
「先定框架、再逐节填」的过程。新一轮论文写作要**重新搭一次骨架**，所以把这一版整体冻结，
让新的 `story/` 从空目录起步，避免在旧骨架上做增量修补而把当时的临时取舍带进去。

⛔ **不要把归档理由写成「repair 期资产」或「口径已作废」——两条都不成立。**
这七份文件里的 discover 口径、两条 contribution、四组易混术语、C1–C15 的强度分档
都与当前口径一致。

## 3. ⭐ 里面哪些内容仍然有价值、什么时候该取回来

**这一节是本归档最重要的部分。** 后续写新 `story/` placeholder 或正式论文时，
应当先读这里、再动笔——下面每一项都给了精确路径。

### 3.1 应当直接继承、不要重新发明的

| 内容 | 精确路径 | 为什么值得继承 |
| :-- | :-- | :-- |
| 导师那条大逻辑与它到章节的映射表 | [story/paper_outline.md](./story/paper_outline.md) §0 | 「解决什么问题 == 为什么有价值 == 现有方法的问题 == 你的方法 == 验证扣住 contribution == 结果回到问题」这条链已经逐环映射到章节，并附了「每节自问服务哪一环」的验收判据 |
| 四个 RQ 及其「验证哪条 contribution / 扣住 §1 哪条」两列 | [story/paper_outline.md](./story/paper_outline.md) §5.1 | 无归属的 RQ 是最常见的返工点；这张表已经把归属钉死，并记录了「回归防护面有多大」为什么被排除为 RQ |
| 现有方法的三条 gap（G1 判据不可复算 / G2 缺定位归因 / G3 无法回归） | [story/paper_story.md](./story/paper_story.md) §4 | 直接由导师原话拆出，是 Intro motivation 与 §Related Work 差异化落点的共同锚 |
| 核心洞察「受限谓词词表本身就是一次建模」 | [story/paper_story.md](./story/paper_story.md) §5.1 | 含三族划分、19 谓词全表，以及两个可直接写进论文的领域出处挂钩示例（`stays_in` ← UML 2.5.1 run-to-completion；`persists_until` ← until 的标准定义） |
| 「把形式化工具裸给自主 agent 效果很差」这条反面立论 | [story/paper_story.md](./story/paper_story.md) §4 末、§5.1 | 它是 §5.1 洞察的反面证据，也是回答「这不就是让 LLM 报缺陷吗」的主要弹药 |
| C1–C15 的强度分档（`实测-强/中/弱`、`方法性质-未测`、`推论`） | [story/claim_evidence_map.md](./story/claim_evidence_map.md) §1–§2 | 五档口径能表达「有实测但只是上界」「有数据但对口径敏感」两种最常见情形，重搭时不必重造 |
| 12 条 forbidden claims 与其理由、替代写法 | [story/claim_evidence_map.md](./story/claim_evidence_map.md) §3 | 每条对应一次真实的措辞回流风险，删掉会重犯 |
| 九条 reviewer challenge 对照 | [story/claim_evidence_map.md](./story/claim_evidence_map.md) §4；[story/paper_story.md](./story/paper_story.md) §13 | 覆盖「60.4% 相对什么」「分母是你们自己标的」「多报这么多 precision 呢」等必被问到的问题 |
| 四组易混术语 | [story/terminology_policy.md](./story/terminology_policy.md) §1 | 「作者」（生成模型的 LLM）vs 上游论文作者；生成方 6 vs 执行方 2；`over_specification`（模型多写）vs 过度规定（断言多要）；条目 / 去重 / 逐格三层计数。这四组每一组混用都会让读者得出与数据相反的结论 |
| 指标写法的三条硬约束 | [story/terminology_policy.md](./story/terminology_policy.md) §3 | `hit@1` 必带 $\le$、三口径同报、覆盖率与算力同报 |
| 建模对象边界「只在问题定义出现一次、一句话带过、不展开辩护」 | [story/model_scope.md](./story/model_scope.md) §2 | 用户明确要求的写法；同时写清了不许反过来声称「这些模型没有并发 / 时间问题」 |
| 任务边界里的两条实验公平性硬约束 | [story/task_boundary.md](./story/task_boundary.md) §2 | 「参考模型不是输入」「缺陷台账不是输入」——审稿人第一个会问的问题 |
| 五种失败与不确定状态（拒答 / 覆盖缺口 / 隔离项 / 降级 / 不可判定） | [story/task_boundary.md](./story/task_boundary.md) §6 | 与仓库根 §10「只有两种情况允许整格崩」是同一条纪律的本地落法 |

### 3.2 取回时必须一并复核的三件事

1. **所有数字都不要从这里转抄。** 这七份文件里出现的 `hit@1 ≤ 60.4%`、`hit@3 70.9%`、
   表示债务 46.5%、288 簇 / 124 去重组等等，**唯一事实源**是自包含实验报告
   [../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md)。
   归档只保证「当时抄对了」，不保证「现在仍是最新」。
2. **判定口径以 [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/) 为准。**
   本目录只管论文措辞；两者冲突时后者赢（[story/terminology_policy.md](./story/terminology_policy.md) 开头已写明这条优先级）。
3. **导师依据的引用方式要更新。** 这七份文件写作时，2026-08-07 / 08-08 定调还是口头的，
   文中多处写「口头，尚未落成正式 talks 记录」。该记录现已存在：
   [../../../talks/2026-08-08-导师-paper1收窄为issue-discover.md](../../../talks/2026-08-08-导师-paper1收窄为issue-discover.md)。
   新版应直接引它，不要照抄「尚未落成正式记录」这句。

### 3.3 什么时候该取回来

- **写新 `story/` placeholder 时**：先读 §3.1 表，决定哪些条目直接进新骨架、哪些重写。
- **写论文任一节时**：先在 [story/paper_outline.md](./story/paper_outline.md) 找该节的验收判据，
  再到 [story/claim_evidence_map.md](./story/claim_evidence_map.md) 核 claim 强度与禁止写法。
- **回答审稿意见时**：[story/claim_evidence_map.md](./story/claim_evidence_map.md) §4 与
  [story/paper_story.md](./story/paper_story.md) §13 是两张现成的对照表。

## 4. 哪些内容已被取代

| 本目录里的内容 | 被谁取代 | 精确路径 |
| :-- | :-- | :-- |
| 一切实验数字 | 自包含实验报告（唯一事实源） | [../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) |
| 命中判定、方法出处、建模对象边界判据 | 判定口径文档（改它们等于改研究规则） | [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/) |
| 「2026-08-07 / 08-08 定调尚未落成正式 talks 记录」 | 已落库的导师记录 | [../../../talks/2026-08-08-导师-paper1收窄为issue-discover.md](../../../talks/2026-08-08-导师-paper1收窄为issue-discover.md) |
| [story/README.md](./story/README.md) §5 「repair 期资产虽在但不得引用，文件仍在原地」 | 那批资产已于同日归档 | [../r7_issue_lifecycle_scaffold/](../r7_issue_lifecycle_scaffold/) |
| 工作区口径、纪律与当前状态 | 工作区入口三件套（由另一路 PR 维护） | [../../README.md](../../README.md)、[../../GUIDE.md](../../GUIDE.md)、[../../STATUS.md](../../STATUS.md) |

⚠️ **没有一份新文件「取代」了本目录的叙事内容本身**——新 `story/` 目前是空的，等待重搭骨架。
在新骨架落地之前，本目录仍是叙事口径最完整的一份材料，只是不再是 active 事实源。

## 5. 原路径 → 新路径映射

| 原路径 | 新路径 |
| :-- | :-- |
| `story/README.md` | [story/README.md](./story/README.md) |
| `story/paper_story.md` | [story/paper_story.md](./story/paper_story.md) |
| `story/paper_outline.md` | [story/paper_outline.md](./story/paper_outline.md) |
| `story/claim_evidence_map.md` | [story/claim_evidence_map.md](./story/claim_evidence_map.md) |
| `story/task_boundary.md` | [story/task_boundary.md](./story/task_boundary.md) |
| `story/model_scope.md` | [story/model_scope.md](./story/model_scope.md) |
| `story/terminology_policy.md` | [story/terminology_policy.md](./story/terminology_policy.md) |

## 6. 归档时对内容做了什么 / 没做什么

**做了**：把七份文件里的相对链接按新的目录深度机械重算，使它们仍能点开
（例如 `../README.md` → `../../../README.md`，`../experiment_design/issue_lifecycle/` →
`../../r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/`）。这是纯路径变换，
不改变任何链接的目标对象。

**没做**：不改结论、不改数字、不改措辞、不删「相对上一版改了什么」这一节。
因此文中若干「当前 / 现在」的时态表述停留在 2026-08-11 凌晨的语境，属正常历史留痕。

## 7. 禁止外推

1. 不得把本目录当作 active 叙事事实源引用；新 `story/` 落地后一律以新目录为准。
2. 不得从本目录转抄任何实验数字（见 §3.2 第 1 条）。
3. 不得因为本目录在 `archive/` 下就认为其中的口径已作废——作废的是「这一版骨架」，不是口径。
4. 不得把本目录内的相对链接当作 active 入口；先回本 README 与 §5 映射表。
