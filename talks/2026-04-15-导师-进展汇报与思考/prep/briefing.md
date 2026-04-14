# 2026-04-15 与导师讨论准备稿：当前进展、文库解释与研究收束建议

本文服务于 `2026-04-15` 与导师的讨论，时间基线统一取截至 `2026-04-14` 晚。本文重点不是简单罗列事项，而是把下面几件事放到同一份材料里讲清楚：`project_1` 三条文库线各自服务什么问题、这些文库为什么不能被当成“领域自然分布”、`pyfcstm` 和 `pyudbm` 目前分别到了什么位置、以及我为什么现在更倾向于把本学期投稿主线明确收束到 `project_1`。[1][2][3][4][5]

## 1. 一页结论

截至 `2026-04-14`，我现在最核心的判断有六点。

1. 这学期第一优先级应该是先把 `project_1` 的会议论文发出去，而不是把 `project_3` 也一起拉到同一篇里硬做大一统。[1][2][15]
2. `project_1` 当前已经不缺材料，真正缺的是问题收束。最关键的问题不是“有没有状态机样本”，而是“我们这篇论文到底把什么叫作控制系统状态机”。[2][4][5][6]
3. 从现有 `sources/`、`state_machine_types/` 和 `project_1` 讨论稿综合来看，我更倾向把本阶段主问题收束为：**面向控制系统离散控制状态层的自然语言到可执行状态机建模**，也就是模式、阶段、互锁、异常恢复、局部定时这一层，而不是把连续/混成控制整体一起吞进去。[4][5][6][7]
4. `pyfcstm` 不应该只被说成“最近写得比较快的工具仓库”，而应该被说成 `project_1` 当前的**目标形式主义 / 可执行中间表示 / 闭环基础设施**。它的研究价值在于把“自然语言生成状态机”从“生成图”提升成“生成可执行形式模型”。[7][8]
5. `project_3_profile_based_verification/` 这个目录本身现在确实还很空，但 `project_3` 并不是“什么都没有”。大量 timed automata、UPPAAL、UTAP、UDBM 相关的基础设施与文献调研实际上集中在兄弟仓库 `HansBug/pyudbm` 里，当前已经做到“前端 + 符号核 + 文档 / query 互操作 + 文献基础”，只是还没有完整做到 `verifyta` 级搜索引擎。[9][10][11]
6. 我越来越相信，`LLM-based modeling` 的真正杀手锏不是把 prompt 玩得更花，而是给模型持续的**基础设施反馈**。这个判断已经能被现有 baseline 文献中的实证结果支撑，而不只是主观感觉。[12][13][14][16][17]

## 2. 站在博士研究和本学期投稿视角下，为什么现在必须先收束到 `project_1`

如果站在博士全局看，四个 project 当然都重要；但如果站在 `2026` 年春季学期必须先发出第一篇会议论文这个约束下看，当前最适合率先收束的是 `project_1`。原因很简单：它已经同时具备了问题定义、文库证据、可比 baseline、目标形式主义候选，以及一条正在成形的基础设施主线。[1][2][3][4][5][7]

| 方向 | 当前成熟度 | 现阶段最适合承担的角色 | 这学期是否适合作为主投稿 |
| --- | --- | --- | --- |
| `project_1` | 最高 | 先完成第一篇“问题定义 + 方法对象 + baseline + 数据证据 + 基础设施落点”论文 | 是 |
| `project_2` | 中等 | 继续作为接口层问题存在，为后续性质 / 剖面生成做准备 | 暂不宜单独先发 |
| `project_3` | 理论对象已清楚，但原型未成形 | 继续沉淀 timed / profile-guided verification 后端基础 | 暂不宜抢在前面 |
| `project_4` | 依赖前面几项更成熟 | 作为后续“生成-验证-修复”闭环延展 | 更不适合现在先发 |

我现在更倾向的说法是：**本学期这篇论文不应该追求把博士四个问题一次性都回答完，而应该先把“控制系统状态机自动建模”的目标对象、问题边界和方法落点说透。** 这反而更符合会议论文节奏。[1][2][15]

## 3. `project_1` 三条文库线到底分别在做什么

### 3.1 三条文库线在 `project_1` 里的位置

`project_1` 下面的三条线不是三个平行摆设，而是在回答三类不同但互相依赖的问题。[2][3][4][5]

| 文库 | 在 `project_1` 里的位置 | 直接服务的问题 | 当前规模 |
| --- | --- | --- | ---: |
| `baselines/` | 方法线 | 别人现在怎样做“需求 / 描述 -> 状态机”，我们该和谁比较、差距在哪里 | `62` 篇，`🟢 14 / 🟡 19 / 🟠 29` [3] |
| `sources/` | 数据线 | 真实控制系统设计里到底常见什么样的控制状态逻辑，未来数据集该从哪里来 | `787` 篇论文，`746` 条正例案例 [4] |
| `state_machine_types/` | 类型线 | “状态机”到底有哪些家族，我们最后该生成哪一种，为什么不是别的 | `669` 条普通条目，`10` 条综述 [5] |

换句话说：

1. `baselines/` 解决“别人怎么做”和“我们该怎么比”。
2. `sources/` 解决“真实控制系统设计文本长什么样”和“数据集从哪里来”。
3. `state_machine_types/` 解决“我们到底想生成哪一类状态机，而不是泛泛状态机”。

这也是为什么我现在认为 `project_1` 的论文不能只讲其中一条线。真正有说服力的写法，应该是三条线一起服务同一个结论：**控制系统状态机自动建模必须先把目标对象收束成一个清楚的 control-state 问题。**[2][6][7]

### 3.1.1 `baselines/` 里当前最值得拿出来讲的几篇 `🟢`

就明天汇报而言，我觉得 `baselines/` 里不需要铺太满，重点讲几篇最直接的绿色条目就够了。[3]

| 年份 | 条目 | 为什么值得讲 |
| --- | --- | --- |
| `2026` | [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](../../../project_1_llm_state_machine_modeling/baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) | 这是当前文库里最直接命中“自由文本 -> UML 状态机”的 direct baseline，说明主问题已经被正面回答，但 guard / action 仍明显薄弱 [12] |
| `2025` | [Generating SysML Behavior Models via Large Language Models: an Empirical Study](../../../project_1_llm_state_machine_modeling/baselines/llms_emp/DESC.md) | 这是“需求 -> 行为模型 + 模型检查反馈修复”的强证据，直接支撑“反馈闭环比纯 prompt 更重要” [13] |
| `2025` | [LLM-based Iterative Requirements Refinement in FSM with IEC 61499 code generation](../../../project_1_llm_state_machine_modeling/baselines/fsm-gen-iec-61499/DESC.md) | 说明工业控制语境里，状态机生成一旦能接仿真和代码生成，方法就不再只是文本生成 [17] |
| `2024` | [System Architects Are not Alone Anymore: Automatic System Modeling with AI](../../../project_1_llm_state_machine_modeling/baselines/ttool-ai/DESC.md) | 说明知识注入 + 自动反馈循环 + MBSE 工具链集成是能打出实证效果的，不是口头想法 [14] |

就这几篇合起来，我现在对 `baselines/` 的总体判断是：**direct baseline 已经出现了，但真正强的路线越来越不是“一次生成完”，而是“生成后立即接工具反馈”。**[3][12][13][14][17]

### 3.2 这三条文库都不是“均匀采样”的结果

这一点我觉得明天需要向导师说清楚，否则表面统计很容易被误读。

| 文库 | 不能怎样理解 | 更准确的理解 |
| --- | --- | --- |
| `baselines/` | 不能把它理解成“LLM + modeling 领域论文总体分布” | 它是围绕 `project_1` 的可比性刻意筛出来的比较集，优先保留 direct baseline 和任务邻近条目 [3] |
| `sources/` | 不能把当前类型 / 时间分布理解成“控制系统文献天然就以 `EFSM/HSM + T0/T1` 为主” | 早期是广撒网，后期已经明显转向数据集治理，优先收 `EFSM/HSM`、`T0/T1`、细节充实度高且不强趋同的条目 [4][6] |
| `state_machine_types/` | 不能把它理解成“状态机家族论文被均匀抽样后的学科分布” | 它本来就是奔着补全整个状态机家族谱系树去做的，当前阶段明确以“扩树、挂树、补定义与基础设施”为主 [5] |

因此，今天看到 `sources/` 里 `EFSM = 429`、`HSM = 157`、`T0 = 352`、`T1 = 367`，首先说明的是**当前数据集建设目标和收录策略**，其次才是领域现象本身。[4][6]

### 3.3 `sources/` 的标准口径必须讲清楚

`sources/` 现在其实已经不只是“论文样本库”，而是一个带有明确数据集治理口径的文库。它至少同时维护了五套标准。[4][6]

| 口径层次 | 固定字段 | 作用 |
| --- | --- | --- |
| 论文级可用性 | `🟢 / 🟡 / ⚪ / ⏳` | 判断单篇论文整体上是否能形成可靠样本 [4] |
| 案例级保留角色 | `💎 / 🧰 / 🪫` | 区分核心保留、清洗后保留、降采样保留 [4][6] |
| 细节充实度 | 原文细节、描述细节的 `A/B/C/D` 分级 | 判断这条样本是否足以支撑高质量建模与评测 [4][6] |
| 主类型 | `FSM / EFSM / HSM / Protocol / Resource-flow / Hybrid / N/A` | 回答“默认推荐用哪类状态机来理解它” [4][6] |
| 时间级别 | `T0 / T1 / T2 / T3 / N/A` | 回答时间语义到底只是局部工程定时，还是已经进入强实时 / 时钟组合问题 [4][6] |

此外还有一层结构标签，例如 `层次`、`并行`、`协议交互`、`资源互斥`、`显式时钟`、`连续耦合`，以及“强趋同簇”治理。这些东西的作用，不是把样本装饰得更漂亮，而是为了后续回答：哪些样本应该进主训练集，哪些样本应降采样，哪些样本虽然有价值但不能在分布上占太大权重。[4][6]

### 3.4 `sources/` 现在的统计结果到底应该怎么读

目前 `sources/` 的核心统计如下。[4]

先把不同维度拆开看，否则“标题 + 数字”很容易让统计失真。

#### 3.4.1 论文级总体统计

| 指标 | 定义 | 数量 |
| --- | --- | ---: |
| 论文总数 | 当前 `sources/` 已正式入账的论文目录总数 | `787` |
| 论文级 `🟢` | 单篇论文整体上可直接支持可靠样本抽取 | `715` |
| 论文级 `🟡` | 单篇论文仍有价值，但需要额外整理或局部补证 | `16` |
| 论文级 `⚪` | 单篇论文最终未形成可靠样本 | `56` |

#### 3.4.2 案例级保留角色统计

| 类别 | 定义 | 数量 |
| --- | --- | ---: |
| 正例案例总数 | 当前正式入账、可作为控制状态样本讨论的案例条目总数 | `746` |
| `💎 核心保留` | 细节和分布都足够好，适合进入主数据集主链 | `685` |
| `🧰 清洗后保留` | 有价值，但需要进一步清洗、补证或统一口径 | `20` |
| `🪫 降采样保留` | 本身可用，但因强趋同或分布控制原因不应过量进入主集 | `41` |

#### 3.4.3 主类型分布

| 主类型 | 定义 | 数量 |
| --- | --- | ---: |
| `FSM` | 普通离散阶段机，少量条件并入状态也不会明显失真 | `127` |
| `EFSM` | 离散状态仍是主体，但关键语义明显依赖变量、阈值、计数器、请求位等 guard / effect 数据面 | `429` |
| `HSM` | 高层模式和低层子状态 / 子机关系本身就是主要结构事实 | `157` |
| `Protocol` | 多角色请求、授权、确认、接管等交互顺序是核心语义 | `4` |
| `Resource-flow` | 正确性主要由资源占用、互斥、锁闭、释放等流转关系决定 | `13` |
| `Hybrid` | 连续动力学或连续控制律是模型语义不可删的一部分 | `16` |

#### 3.4.4 时间级别分布

| 时间级别 | 定义 | 数量 |
| --- | --- | ---: |
| `T0` | 无关键时间语义，时间不是控制逻辑主体 | `352` |
| `T1` | 只有工程定时 / 局部 timer / 延时保持等局部时间语义 | `367` |
| `T2` | deadline、最小 / 最大持续时间、refractory 等强实时窗口是核心 | `15` |
| `T3` | 连续时间演化与连续状态共同参与系统语义 | `12` |

#### 3.4.5 结构标签覆盖

| 结构标签 | 定义 | 数量 |
| --- | --- | ---: |
| `显式时钟` | 时钟、timer、time window、reset 语义应被显式建模 | `243` |
| `层次` | 超状态 / 子状态 / 任务层与执行层等层级关系必须保留 | `160` |
| `连续耦合` | 离散模式切换与连续量或连续控制律紧耦合 | `71` |

我对这组数字的解读是：

1. 从主类型表看，当前主集明显以离散控制状态层为主体，`FSM + EFSM + HSM = 713 / 746`。[4]
2. 从时间级别表看，当前主集主要集中在 `T0 / T1`，说明短期最稳的论文对象仍是“离散控制 + 局部工程定时”。[4]
3. 从结构标签表看，`显式时钟`、`层次` 都不是个别现象，这意味着即使论文先收束到离散控制状态层，也不能退回过于简单的扁平 `FSM` 设定。[4][6]
4. 但 `Hybrid`、`T2/T3`、`连续耦合` 也不是零星噪声，这说明真实控制系统里确实一直存在另一类更强时间 / 连续动力学耦合问题。[4][6]
5. 因此，**当前最合理的收束不是否认第二类问题，而是承认：本学期论文先解决第一类主问题。**

### 3.4.6 `sources/` 里几类最值得举出来的代表样本

为了让这条线不只是抽象统计，我觉得明天至少可以摘出几类代表案例来讲。[4][6]

| 类型 | 代表条目 | 为什么重要 |
| --- | --- | --- |
| 典型离散顺序控制 | [Automatic Washing Machine Control System Based on PLC](../../../project_1_llm_state_machine_modeling/sources/automatic-washing-machine-control-system-based-on-plc/STM.md) | 很典型的 `EFSM + T1` 样本，说明真实工业控制里“阶段链 + timer + guard”是高频对象 |
| 典型机电控制 / 门控 | [PLC Controlled Elevator System using XC1 PLC through Ladder Programming](../../../project_1_llm_state_machine_modeling/sources/plc-controlled-elevator-system-using-xc1-plc-through-ladder-programming/STM.md) | 电梯样本把请求队列、方向优先、门控时长、异常保护这类控制状态语义写得很清楚 |
| 资源互斥与联锁 | [Some Experiences on Formal Specification of Railway Interlocking Systems using Statecharts](../../../project_1_llm_state_machine_modeling/sources/some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts/STM.md) | 说明有些“状态机”本质上更像强 guard / 强资源约束系统，不只是简单顺序流程 |
| 分层任务控制 | [A Parallel Hierarchical Finite State Machine Approach to UAV Control for Search and Rescue Tasks](../../../project_1_llm_state_machine_modeling/sources/a-parallel-hierarchical-finite-state-machine-approach-to-uav-control-for-search-and-rescue-tasks/STM.md) | 这是 `HSM` 主线的代表，说明 mission supervisor 与子层任务控制是另一类高频对象 |
| 连续 / 混成耦合 | [Stair Ascent Phase-Variable Control of a Powered Knee-Ankle Prosthesis](../../../project_1_llm_state_machine_modeling/sources/stair-ascent-phase-variable-control-powered-knee-ankle-prosthesis/STM.md) | 说明确实存在“也叫状态机，但核心仍受连续相变量支配”的第二类问题 |

### 3.5 `state_machine_types/` 不是应用样本库，而是“族谱树”

`state_machine_types/` 目前普通条目 `669` 篇、综述条目 `10` 篇。它最重要的作用，不是告诉我们哪一类应用最多，而是帮助我们确认：状态机根本不是单一对象，而是一整族形式主义。[5]

主要主类统计如下。[5]

| 主类 | 定义 | 数量 |
| --- | --- | ---: |
| 经典离散状态机 | `FSM / EFSM / Statecharts` 一类离散状态建模主线 | `160` |
| 时间 / 时钟自动机 | 以显式时间约束、时钟或 timed transition semantics 为核心的家族 | `96` |
| 混成 / 随机扩展 | 连续动力学、概率、不确定性等增强语义主线 | `46` |
| Petri 网与并发网模型 | 以并发、资源流、token/marking 语义为核心的家族 | `28` |
| 接口 / 组合 / 契约模型 | 以交互、组合、契约和接口行为为核心的家族 | `31` |
| DSL / 专用建模语言 | 面向特定状态机 profile 或特定工程对象的语言 / DSL 主线 | `59` |
| 标准、交换格式、元模型与执行载体 | 承载状态机模型互操作、执行和工具链的标准与基础设施 | `264` |

我觉得这一块最有价值的结论是：**现代“状态机研究”越来越不是只在发明新形式主义，而是在发明 profile、DSL、元模型、交换格式、运行时和验证基础设施。** 这恰好也解释了为什么 `pyfcstm` 这种“目标形式主义 + 执行语义 + 工具链入口”会在学术上有位置。[5][7]

## 4. `project_1` 当前最需要收束的，其实是问题对象定义

我现在越来越不想把“控制系统状态机”当成一个不加区分的大口袋，因为 `sources/` 和 `state_machine_types/` 已经把问题揭露得很清楚：这个词至少同时罩着两类不同问题。[4][5][6]

| 维度 | 离散监督 / 顺序控制 / 模式管理 | 连续 / 混成控制中的模式切换 |
| --- | --- | --- |
| 典型系统 | PLC、电梯、铁路联锁、门控、任务控制、异常恢复链 | `ABS/BBW`、外骨骼步态、强时序医疗控制、动力学模式切换 |
| 状态的主要含义 | 模式、阶段、权限、流程位置、故障恢复位置 | 控制律区间、相变量阶段、连续动力学运行区间 |
| 核心建模难点 | guard、事件、互锁、局部 timer、异常链 | 时钟组合、连续变量、动力学耦合、hybrid semantics |
| 更自然的模型对象 | `FSM / EFSM / HSM / control-state DSL` | `Timed / Hybrid` 一类对象 |
| 更自然的反馈基础设施 | parser、simulator、代码生成、结构校验、可执行 trace | timed/hybrid verification、数值仿真、symbolic reachability |

这是我的归纳判断，不是任何一篇论文的原句。但它有直接证据基础：

1. `sources/` 里当前大多数条目都落在离散控制状态层，尤其是 `EFSM/HSM/T0/T1` 主链。[4]
2. `state_machine_types/` 明确把 `Timed Automata`、`Hybrid Automata`、`Petri Nets`、`Interface Automata` 等家族拉开了，不存在一个“天然统一”的单对象。[5]
3. `project_1` 讨论稿中也已经多次指出，更合理的做法不是重新发明“控制系统状态机”这个家族，而是把控制语义里真正重要的部分提升为一等对象，例如模式、守卫、互锁、恢复和局部时间约束。[6][7]

因此，我现在更倾向于把 `project_1` 论文的目标对象写成：

> **面向控制系统离散控制状态层的自然语言到可执行状态机建模。**

这里的“控制状态层”指的是：

1. 模式切换；
2. 顺序阶段推进；
3. 互锁与权限控制；
4. 故障与恢复链；
5. 局部工程定时。

这一定义一旦收束，`project_1` 的问题就会清楚很多，而不会在第一篇论文里同时背上 continuous control、timed automata、hybrid reachability 三类难题。[4][5][6][7]

## 5. `pyfcstm`：从 `2026-02` 底以来的进展，以及它在 `project_1` 里的学术位置

### 5.1 目前到底推进到了什么程度

本地 `pyfcstm` 仓库中，`main` 当前 `HEAD = dcf1f70`。从 `2026-02-28` 以来，`main` 上至少已经明确做出了下面几类能力推进。[8]

| 能力层 | `main` 上已可确认的推进 | 对 `project_1` 的意义 |
| --- | --- | --- |
| 多文件 / 模块化 | `import` 语法、模型组装、目录级入口、convenience loaders、import-aware editor support | 说明目标模型已不再是玩具单文件样例，而是在朝可维护工程对象走 |
| 执行与语义 | `if` 语句、运行时递归执行、symbolic if-block execution | 说明 DSL 正在补齐真正可执行的行为语义，而不是只做结构图 |
| 代码生成 | 内建 Python / C 模板、`c_poll` 路线、模板测试和 runtime 对齐 | 说明生成结果可以继续进代码侧基础设施 |
| 可视化与写作 | PlantUML 导出、文档与教程完善、VS Code 支持 | 说明模型不只是能被机器跑，也能被人类读、审、改 |
| 验证预备 | solver / verify 相关测试、符号搜索与可回放 witness 测试 | 说明它已经在向后续验证闭环预埋接口 |

所以，我现在不太想再把 `pyfcstm` 描述成“状态机 DSL 做了一些功能”，而更想描述成：

> **一条正在成形的 executable control-state infrastructure。**

### 5.2 它在 `project_1` 里不只是工具，而是研究答案的一部分

结合 `project_1` 的讨论稿，我现在认为 `pyfcstm` 的最准确定位是：[7]

> 一类面向控制逻辑的、以 sequential hierarchy 为结构骨架、以 `EFSM` 风格 guard / variable / effect 为数据面的 executable control-state DSL，并且把外部副作用隔离为 abstract action。

这一定义对 `project_1` 很重要，因为它实际上回答了五个学术问题。[7]

| 学术问题 | `pyfcstm` 给出的回答 |
| --- | --- |
| 我们到底让 LLM 生成什么 | 不是宽语义的 `UML/SCXML` 全集，而是语义收束的 control-state profile |
| 生成结果如何立刻可用 | 直接生成可解析、可执行、可仿真的 DSL，而不是只生成图形草图 |
| 怎样兼顾形式化与工程动作 | 把模型主体的 formal core 和外部行为挂点隔离开 |
| 后续验证 / 修复怎么接 | parser、runtime、solver、template generation 围绕同一模型对象组织 |
| 为什么它适合作为 LLM 的目标 | 因为它比宽语义目标形式主义更低熵、更可校验、更适合闭环反馈 |

### 5.3 如果要讲论文贡献点，我现在更愿意这样讲

如果 `project_1` 这篇会议论文要把 `pyfcstm` 纳入叙事，我目前更倾向把贡献点表述成下面六类，而不是泛泛说“实现了一个工具”。[7]

1. 提出一种面向控制系统自动建模的状态机 profile，而不是直接把 `UML/SCXML` 大全集当目标。
2. 给出该 profile 的可执行、较强确定性的执行语义。
3. 提出“形式化核心与外部行为隔离”的建模边界，使后续验证和修复更容易落地。
4. 把研究任务从“自然语言到状态图”提升为“自然语言到可执行形式模型”。
5. 为后续 `project_2 / project_3 / project_4` 提供统一模型基座。
6. 把“LLM 生成友好性”显式纳入目标形式主义设计，而不是事后再去迁就 LLM。

我觉得这几点正是 `project_1` 当前和纯 prompt-paper 的最大差异：我们不是只在问“能不能生成”，而是在问“该生成成什么、生成后如何进入闭环”。[7][8]

## 6. `project_3` 其实已经在 `pyudbm` 里推进了很多，只是还没长回 `research_ideas` 这个目录

### 6.1 先说结论

如果只看 `research_ideas/project_3_profile_based_verification/`，当前确实会让人感觉像“还没动”。但如果把工作范围放回实际研究推进，我觉得更准确的说法是：

> `project_3` 的 timed automata / UPPAAL / symbolic verification 后端准备，当前主要集中在兄弟仓库 `HansBug/pyudbm` 里，而不是集中在 `research_ideas/project_3_profile_based_verification/` 这个空目录里。[9][10][11]

本地已将 `pyudbm` clone 到 `~/oo-projects/pyudbm`，当前 `main` 的 `HEAD = a8d0649`。[9]

### 6.2 `pyudbm` 已经做出的部分

结合 `README`、路线文档、UTAP 集成计划、测试文件和 foundations 文档，我认为 `pyudbm` 现在至少已经把下面几层搭起来了。[9][10][11]

| 层次 | 当前状态 | 证据 |
| --- | --- | --- |
| 历史风格 `UDBM` Python API | 已恢复主线 | `Context / Clock / Federation / Valuation` 已公开导出 [9] |
| `UCDD` / mixed symbolic 方向 | 已纳入长期路线 | 路线文档明确把 `UCDD` 作为 mixed symbolic 核之一 [10] |
| `UTAP` 绑定与模型前端 | 已进入 public API 层 | 已有 `load_xml`、`load_xta`、`load_query`、`loads_query`、`parse_query` 等入口 [10][11] |
| 官方模型 / query 样本库 | 已有保留官方样本集 | `178` 个保留文件，来自 `216` 个原始抓取文件筛后留下 [11] |
| query / roundtrip 测试 | 已较扎实 | query API、roundtrip、feature summary、capability summary 都有测试 [10][11] |
| TA / UPPAAL 文献阅读地图 | 已系统化维护 | `papers/README.md` 不是随手笔记，而是阅读路径 [10] |
| foundations 文档 | 已明确讲清 query 和 symbolic semantics | docs 已直接解释 on-the-fly symbolic exploration [10] |

我觉得这意味着：`project_3` 现在不是“什么都没有”，而是**后端和文献基础已经在另一个仓库里做了很多，只是还没有组装成第一版 profile-guided verifier 原型。**

### 6.3 但为什么我仍然说它还没有真正起飞

原因也很明确。`pyudbm` 当前做得很深的，是：

1. `UDBM` 这一层；
2. `UCDD` 这一层；
3. `UTAP` 这一层；
4. 模型 / query / roundtrip / docs / sample corpus 这一层。

但它还没有做成的，是 `verifyta` 最核心的一层：[10][11]

| 能力 | 当前状态 |
| --- | --- |
| zone / federation 基础 | 已有 |
| query 解析与对象化 | 已有 |
| official model / query interop | 已有 |
| 完整 symbolic reachability 搜索 | 仍缺 |
| `A[] / E<> / A<> / E[]` 查询求值引擎 | 仍缺 |
| 诊断 trace / witness / counterexample 生成 | 仍缺 |
| `verifyta` 核心搜索算法 | 仍缺 |

所以，关于 `project_3`，我现在更诚实的表述是：

> 后端基础已经有实质推进，尤其是 `pyudbm`；但完整验证器仍然没有，下一步需要的不是再堆文献，而是做出最小可运行原型。[1][9][10][11]

## 7. 为什么我越来越相信“基础设施反馈”才是 `LLM-based modeling` 的真正杀手锏

我现在对这一点已经不是模糊感觉了，而是有一组相当一致的 baseline 证据。[3][12][13][14][16][17]

### 7.1 现有 baseline 给出的直接证据

| 文献 | 最关键结果 | 我对它的解释 |
| --- | --- | --- |
| *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models* (2026) | `Claude 3.5 Sonnet` 单提示整体 `F1 = 0.7029`，但 `actions = 0.1633`；`GPT-4o` 单提示 `F1 = 0.5431`，`Hybrid` 提升到 `0.6559` [12] | 纯 prompt 可以出骨架，但 guard / action / 复杂结构仍明显是痛点；流程设计和后续修补对弱模型尤其重要 |
| *Generating SysML Behavior Models via Large Language Models: an Empirical Study* (2025) | 引入模型检查反馈后，格式错误修复率 `94.6%`，语法错误 `88%`，但语义错误只有 `43.1%`，需求不一致只有 `37.3%`；代价是时间增加 `2.72-7.67` 倍 [13] | 反馈不是没用，而是说明“只有规则反馈还不够”，需要更强执行 / 仿真 / 反例环境 |
| *System Architects Are not Alone Anymore* (2024) | 状态机生成得分 `63/100`，高于学生 `58/100`，速度快 `15.2` 倍；块图是 `81/100` 对 `70/100`，速度快 `67.5` 倍 [14] | 一旦知识注入、自动反馈循环和工具链集成做起来，效果就不再只是 prompt 本身的能力 |
| *Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering* (2026) | 强调 section-wise decomposition、sanity checks、编译 / 静态分析、regression traceability，而不是一次性大 prompt [16] | 安全关键工程里真正被信任的是工作流闭环，不是 prompt 魔法 |
| *LLM-based iterative requirements refinement in FSM with IEC 61499 code generation* (2025) | 迭代精化、闭环仿真、IEC 61499 代码生成、部署测试被放在一个链里 [17] | 控制逻辑建模只要接上 simulator 和 code generation，方法论就已经变了 |

### 7.2 这意味着什么

我现在更愿意把我的观点写成下面这句话：

> `LLM-based modeling` 的真正优势，不在于让模型“单次思考得更聪明”，而在于让模型的每次输出都能被 parser、simulator、compiler、model checker、regression test 这些基础设施继续打分。

如果站在 `project_1` 视角下看，这个结论几乎正好落在 `pyfcstm` 上：[7][8]

1. 先把目标对象收束成一个 LLM 相对能稳定生成的 DSL；
2. 让它一生成就能被 parser 和 runtime 检；
3. 让它继续能接 solver、模板生成、后续 verification backend；
4. 这样生成过程就不是“写一段文本”，而是在往一个可执行对象空间里搜索。

我觉得这正是我们最值得强调的差异化：**不是说我们 prompt 比别人更漂亮，而是说我们给了模型更强的环境反馈。**[7][12][13][14][16][17]

## 8. 如果从本学期投稿倒推，`project_1` 论文到底该怎么收束

### 8.1 我现在最倾向的论文主张

如果必须收成一篇会议论文，我现在最倾向的主张是：

> 面向控制系统自然语言描述，不应一上来就把目标写成“任意状态机”或“所有控制系统状态机”；更稳妥、更有研究可操作性的做法，是先把目标收束为控制系统的离散控制状态层，并以一门可执行、可校验、可继续进入验证闭环的 control-state DSL 作为目标形式主义。

这条主线的好处是：

1. `baselines/` 能提供直接对比对象；
2. `sources/` 能提供大量真实控制样本与数据证据；
3. `state_machine_types/` 能证明为什么“状态机不是一个对象”，我们为什么要主动选型；
4. `pyfcstm` 能提供目标形式主义与基础设施落点；
5. `project_3` 与 `pyudbm` 则可以作为后续验证闭环的自然延伸，而不用现在就全部做完。

### 8.2 如果要讲“我们现在处在整个博士研究中的哪一段”，我更愿意这样讲

1. 博士研究的总目标仍然是“生成-验证-修复”闭环。[1]
2. 但当前阶段最先要解决的是 `project_1`：把输入对象、目标形式主义和评测口径立住。[2][3][4][5]
3. `pyfcstm` 正是这个阶段的关键研究产出，因为它提供了目标对象和基础设施骨架。[7][8]
4. `pyudbm` 则是在为后续 timed / symbolic verification 打地基。[9][10][11]

## 9. 从 `dev/frontier` 看投稿时间点：本学期还剩什么窗口

这一部分我只基于 `dev/frontier` 里现有整理来判断，不把它说成官方最终 `CFP`；真正投稿前仍需要回官方页面再核对。[15]

| venue | 与当前论文的关系 | `frontier` 中可见时间节奏 | 站在 `2026-04-14` 的判断 |
| --- | --- | --- | --- |
| `RE` | 需求工程 / 需求到模型 / 规约抽取很强相关 | 近年大多在 `3` 月上中旬摘要 / 投稿；`RE 2025` 是 `2025-03-03` 摘要、`2025-03-10` 投稿 [15] | `2026` 这一轮基本已过 |
| `MoDELS` | 模型驱动 / 状态机 / SysML / 形式化建模主场 | 近年大多在 `3` 月下旬到 `4` 月上旬；`2025` 是 `2025-03-27` 摘要、`2025-04-03` 投稿 [15] | `2026` 这一轮大概率刚过或已过 |
| `ASE` | 自动化软件工程 / `LLM for SE` / 建模-验证-修复最匹配 | `2024` 是 `2024-05-31` 摘要、`2024-06-07` 投稿；`2025` 是 `2025-05-30` 投稿 [15] | 这是本学期最值得盯的近端 A 类窗口 |
| `FM` | 形式化方法 / timed automata / verification 邻近 | 节奏不如 `RE/MoDELS/ASE` 稳定，但 `2024` 是 `2024-04-05` 摘要、`2024-04-12` 投稿；`frontier` 的 `2026` 推断周历把它放到 `4` 月下旬到 `5` 月上旬 [15] | 若论文更偏形式化目标形式主义，也可观察，但对 `project_1` 不是首选 |
| `SoSyM / STVR` | 建模与验证类期刊 | `frontier` 里按全年滚动处理 [15] | 若本学期 conference 赶不上，是稳定后手 |

因此，如果只谈“这学期还要发出去”，我现在的判断是：

1. 最近端最值得争取的是 `ASE` 这条线；
2. `RE` 和 `MoDELS` 更像下一轮周期的自然主场；
3. 如果 `ASE` 时间上来不及，就不要为了抢窗口把问题重新做散，宁愿老老实实把 `project_1` 的对象和实验打厚，再看下一轮 `RE / MoDELS` 或 rolling journal。[15]

## 10. 我明天最希望和导师讨论出结论的几个点

1. 本学期第一篇会议论文，是否就明确收束为 `project_1`，不再试图把 `project_3` 的完整验证器也塞进同一篇。
2. 论文中的“控制系统状态机”，是否就先明确限定为**离散控制状态层**，而把连续 / 混成控制整体作为后续延展方向。
3. `pyfcstm` 是否可以在学术叙事中明确作为目标形式主义 / 可执行中间表示 / 闭环基础设施来写，而不是只当一个实现细节。
4. `project_3` 下一步是否应当继续由 `pyudbm` 这条线沉淀 timed / symbolic 基础，但不打断本学期 `project_1` 投稿节奏。
5. 如果按本学期投稿节奏倒推，是否优先瞄准 `ASE` 风格的表达方式：自动化软件工程 + 可执行反馈基础设施 + 建模闭环，而不是把论文写得过于泛形式化。

## 参考文献

[1] 仓库总述与博士整体目标：[TARGET.md](../../../TARGET.md)  
[2] `project_1` 项目级说明：[project_1_llm_state_machine_modeling/README.md](../../../project_1_llm_state_machine_modeling/README.md)  
[3] `project_1 baselines` 文库与总账：[README.md](../../../project_1_llm_state_machine_modeling/baselines/README.md)，[SUMMARY.md](../../../project_1_llm_state_machine_modeling/baselines/SUMMARY.md)  
[4] `project_1 sources` 文库、总账与标准口径：[README.md](../../../project_1_llm_state_machine_modeling/sources/README.md)，[GUIDE.md](../../../project_1_llm_state_machine_modeling/sources/GUIDE.md)，[SUMMARY.md](../../../project_1_llm_state_machine_modeling/sources/SUMMARY.md)  
[5] `project_1 state_machine_types` 文库与总账：[README.md](../../../project_1_llm_state_machine_modeling/state_machine_types/README.md)，[GUIDE.md](../../../project_1_llm_state_machine_modeling/state_machine_types/GUIDE.md)，[SUMMARY.md](../../../project_1_llm_state_machine_modeling/state_machine_types/SUMMARY.md)  
[6] `sources` 数据集治理与 STM 可用性讨论：[2026-04-02-14-17-AI-讨论-sources文库STM数据集可用性与趋同问题系统分析.md](../../../project_1_llm_state_machine_modeling/discussions/2026-04-02-14-17-AI-讨论-sources文库STM数据集可用性与趋同问题系统分析.md)  
[7] `pyfcstm` 研究定位与贡献讨论：[2026-03-12-18-54-AI-讨论-控制系统状态机相对一般状态机的特性与pyfcstm落点.md](../../../project_1_llm_state_machine_modeling/discussions/2026-03-12-18-54-AI-讨论-控制系统状态机相对一般状态机的特性与pyfcstm落点.md)，[2026-04-05-22-39-29-AI-讨论-pyfcstm-形式化定位-差异化与工具链比较.md](../../../project_1_llm_state_machine_modeling/discussions/2026-04-05-22-39-29-AI-讨论-pyfcstm-形式化定位-差异化与工具链比较.md)  
[8] `pyfcstm` 仓库：<https://github.com/HansBug/pyfcstm>  
[9] `pyudbm` 仓库：<https://github.com/HansBug/pyudbm>  
[10] `pyudbm` 关键文档与路线图：<https://github.com/HansBug/pyudbm/blob/main/mds/UPPAAL_ECOSYSTEM_AND_PYUDBM_LONG_TERM_ROADMAP.md>，<https://github.com/HansBug/pyudbm/blob/main/mds/PR14_UTAP_PYBINDING_INTEGRATION_PLAN.md>，<https://github.com/HansBug/pyudbm/blob/main/papers/README.md>  
[11] `pyudbm` 关于 query、symbolic exploration 与官方样本集的文档：<https://github.com/HansBug/pyudbm/blob/main/docs/source/foundations/queries-and-properties/index.rst>，<https://github.com/HansBug/pyudbm/blob/main/test/testfile/official/README.md>  
[12] Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian, Boqi Chen, Gunter Mussbacher. *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*. arXiv, 2026. 公开链接：<https://arxiv.org/abs/2604.00275>；仓库分析稿：[DESC.md](../../../project_1_llm_state_machine_modeling/baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md)  
[13] Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, Chunming Hu. *Generating SysML Behavior Models via Large Language Models: an Empirical Study*. Internetware 2025. DOI: `10.1145/3755881.3755926`；仓库分析稿：[DESC.md](../../../project_1_llm_state_machine_modeling/baselines/llms_emp/DESC.md)  
[14] Ludovic Apvrille, Bastien Sultan. *System Architects Are not Alone Anymore: Automatic System Modeling with AI*. MODELSWARD 2024. 仓库分析稿：[DESC.md](../../../project_1_llm_state_machine_modeling/baselines/ttool-ai/DESC.md)  
[15] `dev/frontier` 投稿时间线资料：`frontier_index/ccf_history/SUBMISSION_TIMELINES.md`，以及相关 venue 页 `ASE / RE / MoDELS / FM`  
[16] Chih-Hong Cheng, Brian Hsuan-Cheng Liao, Adam Molin, Hasan Esen. *Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering*. arXiv, 2026. 公开链接：<https://arxiv.org/abs/2602.19614>；仓库分析稿：[DESC.md](../../../project_1_llm_state_machine_modeling/baselines/workflow-level-design-principles-trustworthy-genai-automotive/DESC.md)  
[17] Valeriy Vyatkin, Sandeep Patil, Dmitrii Drozdov, Anatoly Shalyto. *LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation*. INDIN 2025. 公开链接：<https://ieeexplore.ieee.org/abstract/document/11279575/>；仓库分析稿：[DESC.md](../../../project_1_llm_state_machine_modeling/baselines/fsm-gen-iec-61499/DESC.md)  
