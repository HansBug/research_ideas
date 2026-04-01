# `state_machine_types/` 论文集 README

## 1. 论文集定位

`project_1_llm_state_machine_modeling/state_machine_types/` 是 `project_1` 下专门维护“状态机类型谱系 / 行为形式主义谱系”的论文集工作区。

它服务的核心问题不是：

1. “别人怎样用 LLM 生成状态机”；
2. “真实控制系统论文里有哪些可抽取的状态机描述样本”；

而是：

1. 当前主流的状态机族形式主义到底有哪些。
2. 它们各自能表达什么，不能表达什么。
3. 它们分别依赖什么构造方式、交换格式、DSL 或标准载体。
4. 它们的工具链、验证器、编辑器、运行时与生态成熟度如何。
5. 面对不同类型的控制系统需求，应优先考虑哪一类形式主义。

因此，这个 collection 是 `project_1` 的“形式主义地图”工作区，重点沉淀：

1. `FSM / EFSM / Statechart / UML State Machine / SCXML`
2. `Timed Automata / Timed Transition Systems / Timed Statecharts`
3. `Hybrid Automata / Probabilistic or Stochastic Automata`
4. `Petri Nets / Colored Petri Nets / Timed Petri Nets`
5. `Interface / I-O / Contract / Compositional Automata`
6. 与这些形式主义直接相关的标准、交换格式、建模 DSL 与基础设施论文

## 2. 设立宗旨与期望收获

单独建立本论文集，主要为了固定以下几类后续会反复使用的材料：

1. 主流状态机类型的定义型、奠基型、语义澄清型、教程型和工具型论文。
2. 各类形式主义的“功能 - 特性 - 构造方式 - 基础设施 - 场景 - 需求前提”统一比较口径。
3. 综述/调查/系统映射文献中对多个状态机族形式主义的分类框架、比较轴和研究缺口。

本论文集最终希望回答以下问题：

1. 对 `project_1` 而言，哪些形式主义最适合作为目标输出。
2. 哪些形式主义更适合作为中间表示，而不是最终交付工件。
3. 如果未来要做“生成 - 验证 - 修复”闭环，哪些形式主义已经具备成熟工具链。
4. 哪些形式主义虽然表达力强，但对需求质量、建模前提或工具成本要求较高。

## 3. 收录范围

本论文集优先收录以下论文：

1. 明确定义、提出、澄清或系统说明某一主流状态机族形式主义的论文。
2. 直接解释某一形式主义语义、构造方式、文本/图形表示、交换格式、元模型或 DSL 的论文。
3. 直接面向某一形式主义的基础设施论文，例如编辑器、解释器、执行器、模型检查器、转换器、交换标准。
4. 综述、survey、review、mapping study、taxonomy、tutorial、retrospective 等能系统比较多个状态机族形式主义的论文。
5. 对仓库后续“需求到状态机自动建模”任务有明显选型价值的标准或规范材料。

原则上不应作为本论文集重点收录的论文：

1. 纯应用论文。若正文主要在讲某个控制系统案例，而不是形式主义本身，应优先进入 `sources/` 或其他专题。
2. 纯验证算法论文。若论文主要讨论算法复杂度或求解器优化，但几乎不解释对应形式主义的对象、语义和构造方式，则不应在这里扩张。
3. 只有“state machine”字样，但正文把它当成比喻、内部实现细节或泛流程控制术语的论文。
4. 极其冷门、一次性、缺少配套生态的变体论文；除非它位于某条关键演化分支上。
5. 无法稳定整理出 `desc.md` 或 `survey.md` 的论文。

## 4. 纳入与排除判定标准

后续判断一篇论文是否进入 `state_machine_types/` 时，至少从以下维度执行：

1. 研究对象
   - 纳入：状态机族形式主义本身，或直接支撑其建模与交换的标准/DSL/工具链。
   - 排除：只把形式主义当应用承载物，正文不解释该形式主义本身。
2. 任务类型
   - 纳入：定义、语义说明、分类比较、标准化、工具化、跨形式主义比较。
   - 降优先级：只是在更大框架里顺带出现一种形式主义。
3. 证据形态
   - 纳入：原文能稳定提取形式主义功能、关键特性、构造方式、工具/基础设施和适用场景。
   - 排除：只有摘要级概述，无法支撑可靠比较。
4. 可提取性
   - 纳入：PDF 可获取，`paper_content.txt` 质量可用。
   - 排除：无法获得可用 PDF，或文本提取后仍不足以支持分析。
5. 与本研究相关性
   - 纳入：能直接服务 `project_1` 的目标形式主义选型、中间表示设计、约束表达设计或后续验证衔接。
   - 排除：虽然属于一般形式化方法背景，但无法形成状态机类型选型依据。

## 5. 本论文集下文件说明

本论文集默认包含以下核心文件：

1. [README.md](./README.md)
   - 入口说明文件。
   - 负责解释本论文集的定位、边界与使用顺序。
2. [GUIDE.md](./GUIDE.md)
   - AI 工作操作规范。
   - 负责规定检索、筛选、目录维护、`SUMMARY.md` 回填和一致性检查。
3. [SUMMARY.md](./SUMMARY.md)
   - 论文集总账。
   - 负责维护普通类型论文表、综述论文表、统计、关键词簇和更新日志。
4. [DESC_GUIDE.md](./DESC_GUIDE.md)
   - 单篇 `desc.md` 的专项规范。
   - 只用于“聚焦单一形式主义或单一标准/工具线”的条目。
5. [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)
   - 单篇 `survey.md` 的专项规范。
   - 只用于“跨多个形式主义做综述/调查/比较”的条目。
   - 同时要求把综述中的代表原始文献和后续应追踪方向转成可继续扩库的线索。

AI 推荐阅读顺序如下：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. [DESC_GUIDE.md](./DESC_GUIDE.md) 或 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)
5. 目标论文目录下的 `bibtex.bib`
6. 目标论文目录下的 `paper_content.txt`
7. 必要时回到 `paper.pdf`

## 6. 单论文路径约束

本论文集下每个单论文目录默认至少应包含：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`
4. `desc.md` 或 `survey.md`

其中：

1. `paper_content.txt` 必须优先使用 `tools/pdf_extractor.py` 生成。
2. 普通类型论文默认使用 `desc.md`，且必须遵循 [DESC_GUIDE.md](./DESC_GUIDE.md)。
3. 综述/调查/系统映射论文默认使用 `survey.md`，且必须遵循 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
4. 同一条目默认只保留一个核心派生文件，不要同时写 `desc.md` 和 `survey.md`。

本论文集对派生文件名作如下 collection 级 override：

1. 单篇普通论文统一使用小写 `desc.md`。
2. 单篇综述论文统一使用小写 `survey.md`。
3. 后续 AI 不得沿用 `baselines/` 中的大写 `DESC.md` 口径到本论文集。

## 7. AI 工作入口提示

进入本论文集时，默认按以下方式工作：

1. 先读 [README.md](./README.md)，确认本 collection 研究的是“形式主义类型”，不是 baseline 或应用样本。
2. 再读 [GUIDE.md](./GUIDE.md)，确认当前分类口径、双表结构和条目完成标准。
3. 再读 [SUMMARY.md](./SUMMARY.md)，确认当前已收录范围、空白类型和待补综述方向。
4. 若任务涉及单篇普通条目，继续读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
5. 若任务涉及综述条目，继续读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
6. 进入单论文目录后，严格按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> desc.md/survey.md` 的顺序处理。
7. 完成后必须回写 [SUMMARY.md](./SUMMARY.md)，不能只在论文目录里留下未入账条目。

## 8. 后续 AI 应优先做什么、避免做什么

优先做的事：

1. 优先补齐最常被 `project_1` 用来比较的主流形式主义，例如 `Statechart`、`Timed Automata`、`Petri Nets`、`SCXML`。
2. 每收一类形式主义，都同步补它的“构造方式 + 基础设施 + 适用场景 + 需求前提”。
3. 综述类论文与定义型论文并行推进，避免只积累碎片化单篇。
4. 让综述条目承担“后续扩库导航”职责，把其中发现的新形式主义、代表原始文献和缺口持续回写到 [SUMMARY.md](./SUMMARY.md)。
5. 用 [SUMMARY.md](./SUMMARY.md) 固定分类口径和待补类型，减少后续重复检索成本。

应避免的事：

1. 把本论文集写成泛形式化方法大杂烩。
2. 把控制系统应用论文误当成“形式主义类型论文”。
3. 只记录“某类型存在”，却不整理其构造方式和工具生态。
4. 把 survey 只写成背景摘要，却不抽出后续要追的原始文献和补库入口。
5. 新增论文目录而不更新 [SUMMARY.md](./SUMMARY.md)。
