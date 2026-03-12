# `project_1_llm_state_machine_modeling` README

## 1. 项目定位

`project_1_llm_state_machine_modeling/` 是本博士研究中“研究内容一”的主工作区，核心关注的问题是：

**如何基于自然语言的控制系统描述、系统设计说明或软件需求，利用大语言模型（LLM）自动生成状态机模型。**

这里的目标不是泛泛做“LLM 建模”，也不是只做一般 UML 生成，而是围绕以下主线展开：

1. 输入是自然语言控制系统描述、系统设计说明、功能需求或相近文本工件。
2. 输出是状态机、Statechart、SysML 行为模型或与之高度等价的状态行为模型。
3. 方法上强调 LLM 在“生成 - 反馈 - 修复 - 约束注入 - 可验证化”链路中的作用。
4. 研究对象优先面向控制系统、离散事件行为、模式切换逻辑、故障恢复逻辑和守卫条件。

换言之，本项目服务的是：

**从自然语言控制系统信息到形式化/半形式化状态机模型的自动化建模研究。**

## 2. 在整个博士研究中的角色

本项目是后续几个研究内容的前置基础：

1. 如果没有较高质量的状态机模型生成能力，后续验证场景生成、性质生成、验证剖面构造和模型修复都缺少稳定输入。
2. 因此，本项目负责先把“从非形式化描述到结构化状态机模型”的问题做扎实。
3. 后续 `project_2`、`project_3`、`project_4` 可以在这里生成或整理出的模型基础上继续做验证、剖面化和修复。

本目录重点关注以下问题：

1. 哪些自然语言输入适合直接生成状态机？
2. 哪些工作已经能形成可比较的 baseline？
3. 真实控制系统论文中有哪些可提取的状态机自然语言样本？
4. 当前方法在时间约束、安全约束、层次并发语义、可验证性方面还缺什么？

## 3. 当前目录构成

当前 `project_1` 目录主要由以下部分构成：

1. [baselines/](./baselines/)
   - baseline 论文集。
   - 收录和维护与本项目直接可比或紧密相关的 LLM 建模方法论文。
   - 这里重点沉淀“别人怎么做”的方法、输入、输出、数据集、实验和局限性。
2. [sources/](./sources/)
   - 样本来源论文集。
   - 收录真实控制系统论文，并从中提取可用于状态机建模的自然语言描述与控制逻辑证据。
   - 这里重点沉淀“可作为我们建模输入样本的数据源”。
3. [scripts/](./scripts/)
   - 项目辅助脚本目录。
   - 用于支持批量检索、批量处理或其他工程化整理动作。

因此，这个项目当前可以理解为两条主线并行：

1. **方法线**：看已有工作如何从自然语言或邻近工件生成状态机模型，对应 [baselines/](./baselines/)。
2. **数据线**：从真实控制系统论文中整理可用的描述样本和控制逻辑证据，对应 [sources/](./sources/)。

## 4. 各下属论文集分别是什么

### 4.1 `baselines/`

[baselines/](./baselines/) 是本项目的 baseline collection，负责维护：

1. 与“自然语言生成状态机模型”任务直接可比的 LLM 方法论文。
2. 与状态机精化、扩展、修复、多模态识别、邻近行为建模相关的论文。
3. 跨论文统一比较口径，例如输入类型、输出模型类型、所用 LLM、主要方法、数据集与 benchmark 可获取性。

它回答的核心问题是：

1. 当前有哪些工作能作为 `project_1` 的 baseline？
2. 它们的输入到底是纯自然语言、自然语言加约束、已有模型、图像还是别的工件？
3. 它们输出的是状态机、SysML、Umple、代码还是其他工件？
4. 哪些工作可直接比较，哪些只是邻近相关，哪些只适合作为背景资料？

进入该 collection 后，应先读：

1. [baselines/README.md](./baselines/README.md)
2. [baselines/GUIDE.md](./baselines/GUIDE.md)
3. [baselines/SUMMARY.md](./baselines/SUMMARY.md)
4. 若涉及单篇分析，再读 [baselines/DESC_GUIDE.md](./baselines/DESC_GUIDE.md)

### 4.2 `sources/`

[sources/](./sources/) 是本项目的 source collection，负责维护：

1. 真实控制系统样本文献。
2. 可直接支持状态机建模的自然语言控制逻辑描述。
3. 从论文中提取出的 `STM.md`，用于沉淀状态、事件、转换、守卫、时序与异常恢复等信息。

它回答的核心问题是：

1. 我们能从哪些真实控制系统论文中抽到可靠的状态机描述素材？
2. 哪些领域、对象和系统类型最适合成为自然语言到状态机建模的数据源？
3. 这些论文里有哪些模式切换、阶段推进、故障恢复和约束条件值得保留？

进入该 collection 后，应先读：

1. [sources/README.md](./sources/README.md)
2. [sources/GUIDE.md](./sources/GUIDE.md)
3. [sources/SUMMARY.md](./sources/SUMMARY.md)
4. 若涉及 `STM.md`，再读 [sources/STM_GUIDE.md](./sources/STM_GUIDE.md)

### 4.3 `scripts/`

[scripts/](./scripts/) 不是论文集，而是项目辅助目录。这里的文件主要用于：

1. 批量检索候选论文。
2. 批量生成或检查中间产物。
3. 支持 `baselines/` 和 `sources/` 的工程化整理流程。

它不承担 collection 总账功能，也不替代各 collection 的 `README.md / GUIDE.md / SUMMARY.md`。

## 5. 本项目整体工作流

围绕 `project_1` 工作时，默认应遵循以下逻辑：

1. 先明确你是在做“baseline 方法整理”，还是在做“控制系统样本整理”。
2. 如果是比较已有方法、寻找可对照论文、整理输入输出方法字段，进入 [baselines/](./baselines/)。
3. 如果是寻找真实控制系统语料、提取状态机描述样本、建设后续数据基础，进入 [sources/](./sources/)。
4. 先读对应 collection 的 `README.md`、再读 `GUIDE.md`、再读 `SUMMARY.md`。
5. 只有在明确 collection 边界和当前总账后，才进入具体单论文目录处理。

本项目默认的研究信息流可概括为：

`真实控制系统自然语言样本` + `已有 LLM baseline 方法` -> `面向控制系统的状态机自动建模方法设计`

## 6. 单论文与论文集的关系

本项目统一采用“论文集路径 + 单论文路径”两级结构。

当前已经明确的两类单论文派生物如下：

1. `baselines/` 下以 `DESC.md` 为核心。
   - 用于沉淀单篇 baseline 论文的方法、实验、相关工作和与本研究的关系。
2. `sources/` 下以 `STM.md` 为核心。
   - 用于沉淀单篇控制系统论文中的状态机自然语言描述与控制逻辑证据。

因此，不应在未看所属 collection 规范的情况下，擅自决定某篇论文该写什么派生文件。

## 7. 推荐阅读顺序

对人类读者和 AI，都推荐按以下顺序进入本项目：

1. 先读本文件 [README.md](./README.md)，理解 `project_1` 的总体目标与目录分工。
2. 判断当前任务属于 [baselines/](./baselines/) 还是 [sources/](./sources/)。
3. 进入对应 collection 后，先读其 `README.md`。
4. 再读其 `GUIDE.md`。
5. 再读其 `SUMMARY.md`。
6. 若任务涉及单篇派生文件，再读对应专项 GUIDE。
7. 最后才进入具体单论文目录，按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> 派生文件` 的顺序工作。

## 8. 后续维护时应优先做什么

优先做的事：

1. 保持 [baselines/](./baselines/) 和 [sources/](./sources/) 两条线的边界清晰，不混收。
2. 让 baseline 比较字段、数据集口径、单篇派生文件格式持续一致。
3. 优先补齐那些能直接服务“自然语言控制系统描述/设计/需求 -> 状态机模型”主线的问题材料。
4. 任何正式收录的论文，都应回写对应 collection 的 [SUMMARY.md](./baselines/SUMMARY.md) 或 [SUMMARY.md](./sources/SUMMARY.md) 总账。

应避免的事：

1. 把 `project_1` 变成泛泛的“LLM 建模论文堆放目录”。
2. 把控制系统样本论文和 baseline 方法论文混在一个 collection 里。
3. 只新增论文目录，不回写各自 collection 的总账。
4. 在项目级目录继续堆放临时 markdown，而不及时把内容收敛进对应论文集。
