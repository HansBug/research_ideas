# 第一篇论文工作区：状态机模型的问题发现（STM Issue Discover）

> **入口页。** 本目录承载 paper1 的全部内容：方法实现、语料、缺陷台账、实验、报告。先读本页，再按第 6 节导航进入子目录。
>
> ⚠️ **本工作区曾名 `paper_stm_repair/`。** 2026-08-11 按导师定调更名—— paper1 已收窄为 issue discover，repair 另立后续论文。历史文档中出现的旧名指的就是这里。

## 1. 这篇论文做什么

给定一份自然语言需求 `NL` 与一份由 LLM 从该需求生成的状态机模型 `STM_0`，**自动发现该模型不符合需求之处**，并把每一条发现落成**可机械求值的断言**。

```text
输入：<NL, STM_0>
产出：<已发布的 issue 清单、支撑每条 issue 的可执行断言、
       一条可回溯到 NL 原句与模型元素的证据链>
```

方法把过程拆成若干阶段，每阶段配一个审查者，不合格就带**定向反馈**打回重写；断言只能取自一份**先验定义的闭合谓词词表**——19 个谓词，按求值机制分结构（10）/ 仿真（6）/ 有界模型检查（3）三族。

## 2. Contribution 口径（2026-08-07 与 08-08 导师讨论定）

⚠️ **paper1 收窄到 issue discover，单独成篇。** 导师原话：「discover 部分单独成一篇文章」「repair 不会简单的，特别是要高质量 repair」。repair 另立后续论文，本文只在讨论一节**捎带提及**可用于修复，不展开。

⚠️ **本节已于 2026-08-11 整体更新（PR [#180](https://github.com/HansBug/research_ideas/pull/180)）。** 此前写「可写成贡献的两条」，且把「中间表示与转换桥」列为不可成条——两处都已过期，⛔ 不要按旧版读。真源是 [story/paper_story.md](./story/paper_story.md) §7「Contributions」。

可写成贡献的**三条**【用户明确裁定 2026-08-11】：

1. **基于模型转换 + 模型形式化检查 / 仿真 / 验证的模型错误发现方法**——立的是**整条发现链路**。⭐ 本条独有的是**真值封存**：断言在执行阶段已按依赖拓扑序跑完但真值被封存，审查阶段只看得到可执行性、看不到真假，校验脚本与工具环境哈希后才解封。
2. **基于归纳后的谓词逻辑的断言体系**——⚠️ **这一条就是元模型本身**，只是从「用于构建断言」的角度陈述。⛔ 不要读成「元模型与断言体系是两条」。
3. **issue 证据链体系**——每条发现带着 issue → 断言 → 需求条目 → NL 原句 / PlantUML 元素的四段链接。

⚠️ **两种强度分开记**：**新颖性强度**待 L1/L2 文献调研；**有效性强度**受限于目前没有任何外部对照（属 R2 导师议题）。⛔ 三条一律不得写「首个 / 显著优于 / 据我们所知未见」。

⛔ **一处措辞纪律**：断言由需求拆分转换而来，因而**覆盖性的分母来自需求侧**（不是模型的可疑点集）——⛔ **不得写成「天然具备覆盖性」**。⚠️ 「全覆盖」是交给 LLM 的一条**指令**、由另一个 LLM 审查，其完整性本轮**未测量**；分母来自需求侧 ⛔ 不等于分母是完整的。

不能写成主贡献的（属方法支撑或评价纪律）：run record 与证据簿记、台账与判定口径、closure / regression 审计。⚠️ **此处原有的「中间表示与转换桥」已删除**——那条纪律说的是**实验分析层面**「转换环节引入的模型变化不得记到修复的账上」，被误当成**贡献层面**的禁令；且其前提（存在修复环节）在本文已不存在。详见 [story/paper_story.md](./story/paper_story.md) §7 的两层对照表。

**谓词词表的由来必须按这个口径表述**：从**领域分析、真实文献与技术资料调研**归纳而来，应用于 54 个案例，并据此指导 prompt 设计。⛔ 不表述为"从这批 pair 归纳"。见 [discover_matrix/docs/protocol/method_provenance_policy.md](./discover_matrix/docs/protocol/method_provenance_policy.md)。

## 3. 建模对象的边界（属于问题定义，不是样本取舍）

本研究锚定的状态机形式为

$$ M = (S, E, V, Tr, A) $$

即状态、事件、变量、迁移、动作五元组。它**不含时钟变量，也不含正交区并发语义**。

这条边界在**问题定义阶段**就要讲清。语料里有一份需求要求 fork / join 并发结构与秒级时间约束，其忠实模型在 $M$ 中无法表达，因此该需求派生的 6 个 pair 自然落在研究对象之外、不进入实验。判据只读需求文本，与任何运行结果无关。见 [discover_matrix/docs/protocol/nl_scope_rule.md](./discover_matrix/docs/protocol/nl_scope_rule.md)。

⚠️ 这条边界必须在论文里如实写明，且**不得反过来说"这些模型没有并发问题"**——上游论文记录的最大一类语义问题恰恰是缺正交区。我们排除的是**我们无法判断的那部分**，不是不存在的那部分。

## 4. 语料

来自一篇已发表的实证研究：**10 份**真实控制系统需求，每份交由 **6 个不同的 LLM**（GPT-4o / GPT-4 / Claude / DeepSeek / Kimi / Llama）各生成一份 PlantUML 状态机，合计 **60 个 pair**；上游论文作者还为每份需求人工撰写了参考模型。扣除上述越界的那份需求后，**54 个 pair** 构成本实验语料。

⚠️ 全文有两条容易混淆的模型轴：**生成方**（写出被评审模型的 6 个 LLM，属语料，我们不控制）与**执行方**（跑本方法的 LLM）。

## 5. 当前进展

⭐⭐ **2026-08-17 台账换代。** 当前唯一有效的台账是 [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/) 的 **145 条**（`D2` 98 + `D1` 47，每条逐条落定 `L0`/`L1`/`L2`）。它由 321 条三方 D 档判读 + 人工逐条 meta review + 人工逐条裁决产出。

⭐ 当前有结果的基线臂只有一条：**X1v2**（朴素基线，单次提示、无循环、无工具）。它在新台账上的精确命中为 `hit@1` **59.8%** · `hit@3` **70.3%** · `hit@all` **47.9%**（145 × 6 = 870 位），逐档拆分与全部限制见 [discover_matrix/ledger_v2/X1V2_RESULTS.md](./discover_matrix/ledger_v2/X1V2_RESULTS.md)。

⛔ **主臂 v46 已整体归档**（[archive/r10_ledger_v1_and_v46/](./archive/r10_ledger_v1_and_v46/)），其全量实验 **54 pair × 2 执行模型 × 3 轮 = 324 格** 与那份自包含报告 [../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) ⚠️ **是历史记录，其数字建立在第一版台账上，⛔ 不是当前口径**。

⚠️ **已知欠账**：主臂尚未在新台账上重测，故目前无法给出两臂在同一台账上的对照。

## 6. 目录导航

| 目录 | 是什么 | 什么时候进去 |
| :-- | :-- | :-- |
| [pipeline/](./pipeline/) | **方法实现**。当前活的是 `feedback_loop/`（Requirement-to-Assertion 发现流水线）；`conversion/` 与 `representation/` 是输入准备与表示桥；`readiness_audit/` 是语料准入检查；`agent_loop/` 是上一版单 Agent 实现，已不在运行路径上 | 改方法、改谓词、改提示词 |
| [discover_matrix/](./discover_matrix/) | **实验与评测**。缺陷台账、判定表、代次记录、判定口径文档、分析脚本全在这里 | 看结果、复算数字、查判定口径 |
| [selected_seed_examples/](./selected_seed_examples/) | **60 个 pair 的人读镜像**，每个目录含 `nl.txt`、`stm0.puml` 与溯源元数据。⚠️ 它**不是**流水线的运行时输入根——真实输入是 `pipeline/representation/reports/llms_emp_r45_java_60/pairs/`，两者逐字节相同 | 查某个 pair 的原文 |
| [corpora/](./corpora/) | 更广的语料库与候选集。⚠️ 其中 `nl_segmentation/overrides.json` **在运行路径上**（被 `feedback_loop/common/nl_segmentation.py` 运行时读取），不是纯资料 | 扩充语料、改分句覆盖 |
| [evidence/](./evidence/) | 证据链：台账、审计、追溯矩阵 | 追溯某条结论的来源 |
| [experiment_design/](./experiment_design/) | 实验设计：issue 生命周期、指标口径、来源追踪 | 设计新实验 |
| [reports/](./reports/) | 阶段性报告（按日期命名） | 回顾历史结论 |
| [story/](./story/) | 论文叙事：outline、claim-evidence 映射、术语口径 | 写论文 |
| [archive/](./archive/) | 本工作区**内部**的历史快照（R1.5–R1.7 种子语料、R5.7 Better STM） | 考古 |

其它入口：[**TODO.md**](./TODO.md)（**本论文所有待办的唯一清单**，带复选框）、[GUIDE.md](./GUIDE.md)（工作纪律）、[SUMMARY.md](./SUMMARY.md)（总账）、[STATUS.md](./STATUS.md)（当前状态）。

⚠️ **`story/` 与 `experiment_design/` 目前是 placeholder**——结构在、细节缺，每一处待补都写成了显式 `TODO(后续PR)` 区块。上一版（内容不差，是赶工版）归档在 [archive/r8_story_pre_rebuild/](./archive/r8_story_pre_rebuild/) 与 [archive/r7_issue_lifecycle_scaffold/](./archive/r7_issue_lifecycle_scaffold/)，各配复活导引。

## 7. 推荐阅读顺序

1. **想理解这篇论文做什么**：读本页 → 读上面那份实验报告。两份读完即可完整理解方法与结果。
2. **想复算某个数字**：进 [discover_matrix/](./discover_matrix/)，先读它的 `README.md` 导航页。
3. **想改方法**：先读 [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/) 下的判定口径（改它们等于改研究规则），再动 [pipeline/feedback_loop/](./pipeline/feedback_loop/)。
4. **想写论文**：读 [story/](./story/)，并以 [../talks/](../talks/) 的导师讨论为最高优先级。

## 8. 与仓库其它位置的关系

- **已停用的旧路线**在 [../archive/](../archive/)：旧 agent loop 基础设施、Path-1 评测链、Path-1/Path-2 指南。它们**完整保留、可复活**（各配复活导引），但不参与本文任何结论。⚠️ 注意与本目录内部的 [archive/](./archive/) 区分：后者是本工作区自己的历史快照。
- **正式导师讨论**在 [../talks/](../talks/)，优先级高于本目录的任何推演。
- **归属纪律**：project_1 顶层只放跨论文公共资产；与本论文直接绑定的一切都在本目录内。见仓库根 `CLAUDE.md` §9.5。
- **施工流程状态**（PR 进度、review 状态、CI）以 GitHub PR / issue 为准，本目录不维护。
