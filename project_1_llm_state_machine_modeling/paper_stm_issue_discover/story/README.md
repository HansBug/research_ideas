# story/README.md — 论文叙事入口（placeholder 版）

> ⚠️ **本目录当前是 placeholder。** 上一版七份文档已归档；本版只保留**论文的结构骨架** 与**已经确定的内容**，其余全部以显式 `TODO(后续PR)` 区块占位，细节交给后续 PR。
>
> 不要把本目录当成写作素材库读——它现在是一张**待填的施工图**。

## 1. 当前定位（paper1 = 只做 STM issue discover）

【导师原话】「**discover 部分单独成一篇文章**」「repair 不会简单的，特别是要高质量 repair」。

由此：paper1 收窄为 **状态机模型的 issue discover，单独成篇**；repair 另立后续论文，本文只在讨论一节**捎带提及一小段**，不展开、不承诺效果、不给数据。

正式记录：[../../talks/2026-08-08-导师-paper1收窄为issue-discover.md](../../talks/2026-08-08-导师-paper1收窄为issue-discover.md)

## 2. ⚠️ 依据强度标记：全目录通用

本目录每一条陈述都必须能看出它的依据强度。**六档标记在所有文件中统一使用**：

| 标记 | 含义 | 能不能直接写进论文 |
| :-- | :-- | :-- |
| 【导师原话】 | **逐字**引自正式导师讨论记录中加粗引号内的文字。⛔ 用它就必须能在记录里 grep 到原句 | 能，是硬依据 |
| 【导师原话背书】 | 判断本身是**我方措辞**，但有**一句导师逐字原话直接针对它**；引用时必须把那句原话一并列出 | 能，但**只能以「我方判断 + 导师某句原话支持」的形式写**，不得当成导师说的话 |
| 【v46 实测】 | 有 324 格全量实验数据支撑，数字须回报告核对 | 能，但须遵守该数字自带的口径约束 |
| 【仓库裁定】 | 已固化在 `discover_matrix/docs/protocol/` 或 `CLAUDE.md` 的研究规则 | 能，改它等于改研究规则 |
| 【AI 建议·待确认】 | 从上述几类推演出的设计提案，**尚未经人确认** | ⛔ 不能，须先裁定 |
| 【待定】 | 已知有多个候选方案，且哪个对尚不清楚 | ⛔ 不能 |

⚠️ **第二档的边界必须硬守：「导师未反对」不等于背书。** 背书要求**存在一句导师逐字原话，且那句话直接针对这个判断**；讨论记录里写成「我方提出（导师未反对）」的内容，一律不得标为背书，应标【AI 建议·待确认】或写成「我方提出 · 导师未反对」。判据是：**能不能把那句支撑用的导师原话逐字列出来**。列不出就不是背书。

⛔ **[blueprint_proposal.md](./blueprint_proposal.md) 里的绝大多数内容属【AI 建议·待确认】。** 九节骨架、四个 RQ、三条 contribution 的分法、T1/T2 分层、ref 翻转率实验、来源类映射表——**全部是 AI 建议**。[2026-08-08 导师讨论记录](../../talks/2026-08-08-导师-paper1收窄为issue-discover.md) 中逐字加粗的导师原话共 **10 处**（此前本页写「8 句」，系少计，已更正）：discover 单独成篇 / repair 不会简单 / 修复只捎带提及 / 业务建模的重要性 / 那条大逻辑 / 缺上下文信息那条差异化叙述 / 规则从领域分析归纳 / 归纳的规则指导 prompt 设计 / 不必跑那么多 LLM / fork-join 可做专门分析。⚠️ 其中最后一条**已被 2026-08-11 的处置取代**（不展开、不单开 RQ），见该记录 §5.2 与 [model_scope.md](./model_scope.md) §2。后续 PR 不得把【AI 建议·待确认】悄悄升格为【导师原话】。

## 3. 文件职责

| 顺序 | 文件 | 职责 | 当前完成度 |
| --: | :-- | :-- | :-- |
| 1 | [paper_story.md](./paper_story.md) | 叙事主干：问题 / 价值 / 现有方法的问题 / 方法洞察 / contribution（**三条 vs 两条未裁定**，见 `TODO-S1`；正文按三条排布只为让结构成立） / 任务边界 / 可说与不可说 | 骨架完整，contribution 形状待裁定 |
| 2 | [paper_outline.md](./paper_outline.md) | 九节章节骨架 + 4 个 RQ + T1/T2 实验分层 + 待补对照清单 | 骨架完整，RQ 与实验分层待裁定 |
| 3 | [claim_evidence_map.md](./claim_evidence_map.md) | claim → 证据映射、强度、允许 / 禁止写法 | v46 已有的已填，新增 claim 待补证据 |
| 4 | [model_scope.md](./model_scope.md) | 建模对象 $M = (S, E, V, Tr, A)$、表达力边界、fork/join 处置 | 基本完整 |
| 5 | [terminology_policy.md](./terminology_policy.md) | 术语中英口径、易混术语、指标写法、禁用词 | 基本完整 |
| 6 | [blueprint_proposal.md](./blueprint_proposal.md) | ⛔ **提案，不是依据**：九节骨架 / 四 RQ / T1-T2 / ref 翻转率 / 来源类映射的 AI 推演原料，另含导师 6 句原话 | 全篇【AI 建议·待确认】，引用须标档位 |

**推荐阅读顺序**：想理解论文说什么 → 1、2；想写某一节 → 2 找结构、3 核 claim、5 核措辞；**想核任何数字 → 直接去实验报告，不从本目录转抄**。

### 3.1 ⚠️ `task_boundary.md` 去哪了

上一版有第六份 `task_boundary.md`（任务定义 / 输入输出 / 方法内外 / 人类角色 / 失败状态）。本版**不再单列**，其内容按以下方式并入：

| 原 `task_boundary.md` 章节 | 现落点 |
| :-- | :-- |
| §1 任务定义、§2 输入、§3 产出 | [paper_story.md](./paper_story.md) §6.1–§6.3 |
| §4 方法内外 | [paper_story.md](./paper_story.md) §6.4 |
| §5 人类角色 | [paper_story.md](./paper_story.md) §6.5 |
| §6 失败与不确定状态（拒答 / 覆盖缺口 / 隔离 / 降级 / 不可判定） | [paper_story.md](./paper_story.md) §6.6 |
| 「参考模型不是输入」「台账不是输入」两条硬约束 | [paper_story.md](./paper_story.md) §6.2，并在 [terminology_policy.md](./terminology_policy.md) §2.1 的术语条目里重复钉住 |

合并理由：任务边界是**叙事的一部分**（论文 §1.4 与 §3 都要用它），单列会造成两处维护。⛔ 后续 PR 若发现该合并使叙事文件过长，可以再拆回，但**拆回时必须同步改本表**。

## 4. 上游事实源与优先级

冲突时按此顺序裁定：

| 级别 | 来源 | 用途 |
| --: | :-- | :-- |
| 1 | 用户 / 导师当前明确指令 | 一切之上 |
| 2 | [../../talks/2026-08-08-导师-paper1收窄为issue-discover.md](../../talks/2026-08-08-导师-paper1收窄为issue-discover.md) | 论文收窄、contribution 口径、RQ 设计原则、谓词由来口径、修复不展开 |
| 3 | [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) | **全部实验数字的唯一来源**，自包含 |
| 4 | [../discover_matrix/docs/protocol/](../discover_matrix/docs/protocol/) | 判定口径、方法出处口径、建模对象边界判据——改它们等于改研究规则 |
| 5 | [../README.md](../README.md)、[../GUIDE.md](../GUIDE.md)、[../STATUS.md](../STATUS.md) | 工作区口径、纪律与当前状态 |
| 6 | [blueprint_proposal.md](./blueprint_proposal.md) 一类的 AI 推演材料 | **只作提案**，不得作为依据陈述 |

⛔ **施工流程状态**（PR 进度、review 状态、CI）以 GitHub PR / issue 为准，本目录不维护。

## 5. 已知冲突：X1 已裁定，X2 / X3 仍待裁定

**在裁定之前，相关章节不得定稿。**

| # | 冲突 | 双方 | 落点 | 状态 |
| --: | :-- | :-- | :-- | :-- |
| **X1** | RQ2 的证据来源里出现「**留出集**」 | BLUEPRINT 的 RQ 表 **vs** [method_provenance_policy.md](../discover_matrix/docs/protocol/method_provenance_policy.md) 的不设留出集 | [paper_outline.md](./paper_outline.md) §5.1 | ✅ **已裁定 2026-08-11：永久不设留出集** |
| **X2** | T1/T2 两层实验的形态 | BLUEPRINT 的分层基于 **v35 时期**（当时想省成本、只跑子集）**vs** v46 已跑完 **324 格全量** | [paper_outline.md](./paper_outline.md) `TODO-O5` | ⚠️ 待裁定 |
| **X3** | contribution「现有 detection 方法**缺少错误的上下文信息**」按字面写会被反驳 | 导师原话 **vs** 模型检查的反例轨迹就是上下文、有文献把状态图改动反向映射回需求、有工作给 provenance | [paper_story.md](./paper_story.md) `TODO-S2` | ⚠️ 待裁定 |

**X1 的裁定内容**【用户明确裁定 2026-08-11】：谓词逻辑元模型**来自领域调研**（文献、标准、技术资料），不来自这批 pair；方法的由来既然与 pair 无关，就不存在「在训练样本上评测」这个问题，因此留出集**没有任何存在必要**。RQ2 的证据来源就是已有的 v46 全量 324 格。⛔ 论文里**一笔带过即可，不专门辩护**——「为什么不留出」在本方法的论证结构里根本不出现。口径见 [method_provenance_policy.md](../discover_matrix/docs/protocol/method_provenance_policy.md) §一.1。

## 6. TODO 索引

全部 TODO 区块的汇总。**每个 TODO 在其所在文件中有完整的三段说明**（缺什么 / 做完长什么样 / 材料在哪）。

| ID | 文件 | 一句话 | 阻塞什么 |
| :-- | :-- | :-- | :-- |
| `TODO-S1` | paper_story | contribution 定三条还是两条，以及三条之间的映射 | §1.4、§6 定稿 |
| `TODO-S2` | paper_story | **X3**：「缺上下文」claim 的可辩护收窄 | Intro motivation、C-III |
| `TODO-S3` | paper_story | 领域分析这条论证链的实际交付物（19 行映射表） | 整篇方法合法性 |
| `TODO-S4` | paper_story | Related Work 四条轴的实际文献填充 | §2 |
| `TODO-S5` | paper_story | 「裸给工具效果差」这条反面观察缺可引用证据 | §1.3 末、§7.2 |
| `TODO-O1` | paper_outline | §3 领域分析节的交付形态与验收判据 | §3（承重结构） |
| `TODO-O2` | paper_outline | 建模对象边界落 §1 还是 §3（九节无独立 Problem Formulation） | §1、§3 分工 |
| `TODO-O3` | paper_outline | 4 个 RQ 定稿（两套候选） | §5、§6 全章 |
| ~~`TODO-O4`~~ | paper_outline | ✅ **X1 已裁定 2026-08-11：永久不设留出集**，见 §5 | 不再阻塞 RQ2 |
| `TODO-O5` | paper_outline | **X2**：T1/T2 形态重做 | §5 实验设置 |
| `TODO-O6` | paper_outline | ref 翻转率实验的可行性实测（参考模型转换成功率） | RQ3 |
| `TODO-O7` | paper_outline | 判别效力 / 覆盖性指标的定义与工程 | RQ3 |
| `TODO-O8` | paper_outline | 待补对照与审计清单的执行（朴素基线第一优先） | §6、§8 |
| `TODO-O9` | paper_outline | 投稿 venue 与排期重做 | 全篇节奏 |
| `TODO-C1` | claim_evidence_map | contribution 定稿后回填 claim 编号与措辞 | C2/C3/C4 |
| `TODO-C2` | claim_evidence_map | 表达力边界 claim 缺证据（映射表未产出） | RQ1 |
| `TODO-C3` | claim_evidence_map | 判别效力 claim 缺数据（ref 翻转率未跑） | RQ3 |
| `TODO-C4` | claim_evidence_map | 无外部对照 → 一切相对性 claim 不可写 | §6、§8 |
| `TODO-M1` | model_scope | fork/join：不展开（当前定）与 BLUEPRINT 四层 finding 方案的取舍留档 | §3.1 一句话 |
| `TODO-M2` | model_scope | 19 个谓词逐条挂领域出处 | §3、§4.2 |
| `TODO-M3` | model_scope | `invariant` 谓词的处置（最自然用法出界） | §4.2、§8 |
| `TODO-T1` | terminology_policy | 三条 contribution 的英文措辞 | 全篇英文稿 |
| `TODO-T2` | terminology_policy | 领域分析相关新术语的中英口径 | §3 |

## 7. placeholder 阶段的退出判据

本目录可以摘掉 placeholder 标记，当且仅当：

1. `TODO-S1` / `TODO-S2` / `TODO-O3` / `TODO-O5` **四项**已裁定——它们决定**论文的形状**，其余 TODO 决定内容的丰俭。✅ 原第五项 `TODO-O4`（留出集）**已于 2026-08-11 裁定：永久不设留出集**，从退出判据中移除。
2. §3 领域分析的交付形态已确定（`TODO-O1`），哪怕表还没填满。
3. [claim_evidence_map.md](./claim_evidence_map.md) 中不存在「有 claim、无证据、无 TODO」的条目。

⛔ **不以「文档看起来完整」作为退出判据。** 上一版就是七份写得很完整、但 contribution 形状其实还没定的文档；那种完整度会让后续 agent 误以为可以直接照着写正文。
