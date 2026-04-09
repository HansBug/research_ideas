# 面向实时系统开发的时间自动机综述 / A Survey of Timed Automata for the Development of Real-Time Systems

## 基本信息

- 标题：A Survey of Timed Automata for the Development of Real-Time Systems
- 中文标题：面向实时系统开发的时间自动机综述
- 作者：Md Tawhid Bin Waez，Juergen Dingel，Karen Rudie
- 发表：`Computer Science Review`, Volume 9, 2013
- DOI：`10.1016/j.cosrev.2013.05.001`
- 链接：https://doi.org/10.1016/j.cosrev.2013.05.001
- 综述主题：`Timed Automata` 变体、分析技术、实现问题与工具生态
- 对象类型：🧱
- 覆盖时间范围：以 Alur-Dill 早期工作为起点，主体覆盖前两个十年左右的研究积累
- 覆盖主类：⏱️
- 补充材料/数据获取方式：原文本体即为大规模综述，包含变体分类、工具表和实现问题讨论
- 原文是否给出系统比较表：是，给出大量分类表、决策问题表、工具表和发展趋势图

## 综述范围与结论

这篇 survey 几乎可以看作时间自动机家族的“索引册”。原文不仅回顾经典 `Timed Automata` 的语法、语义、区域与 zone 技术，还进一步系统整理了 `80` 个变体、`12` 个类别、`40` 个工具，并单独讨论“模型如何真正落地为可运行实时系统”这一实现问题。

- 覆盖范围：经典时间自动机、参数化/概率/代价/博弈/更新型/递归型等变体、实现与代码生成问题、工具版图
- 主要比较轴：时钟约束、时钟更新、分析算法、判定问题、实现可行性、工具用途
- 对本 collection 的直接价值：它非常适合帮助 `project_1` 判断“什么时候应该选用时间自动机，以及该选哪个可判定/可实现的子类”

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| ⏱️ | Classical Timed Automata | 重点 | 定义对象 | 作为所有后续变体的基线 |
| ⏱️ | Parametric Timed Automata | 重点 | 扩展对象 | 适合复用组件和参数综合 |
| ⏱️ | Timed Automata with richer constraints/updates | 重点 | 扩展对象 | 用于提升表达力，但常牺牲可判定性 |
| ⏱️ | Priced / Probabilistic / Game Timed Automata | 重点 | 扩展对象 | 面向成本、随机性和控制综合 |
| ⏱️ | Task / Product Interval / Implementation-oriented automata | 一般 | 应用对象 | 面向调度、代码生成和平台落地 |

## 分类轴与比较框架

原文的比较框架非常完整，主要包含：

1. 语法轴：时钟约束、时钟更新、接受条件、是否允许参数/概率/递归等。
2. 分析轴：`region`、`zone`、`flattening` 三大分析路线。
3. 理论轴：闭包性质、可判定性、复杂度、reachability/emptiness/universality 等问题。
4. 工程轴：可实现性、鲁棒性、sampling、代码生成。
5. 工具轴：模型检验、控制综合、调度、测试、参数分析、概率分析等用途。

这意味着它既能回答“这个形式主义能不能表达”，也能回答“有没有工具”和“生成出来以后能不能跑”。原文实际上同时在做三层比较：**分析技术**、**变体家族**、**工具用途**；如果不把这三层拆开，survey 的信息密度就会被压扁。

| 分析路线 | 核心对象 | 理论性质 | 实践表现 | 原文结论 |
|---|---|---|---|---|
| Region graph | `clock regions` | 奠定可判定性基础，许多经典结果依赖它 | 状态数爆炸，实际很少直接用 | 是理论基石，不是今天最常用的工程实现 |
| Zone graph | `clock zones` + `DBM` | 保留 reachability 等关键性质 | 实践里明显更紧凑，主流工具普遍采用 | 是现代 timed automata 工具生态的主流基础设施 |
| Flattening / arithmetic encoding | 将时间问题改写到可判定算术理论 | 能表达部分 region/zone 难表达的问题，如某些二元延迟关系 | 不能覆盖全部常规验证需求 | 适合补充某些特殊性质，而不是取代主流分析路线 |

| 变体家族 | 主要增加的能力 | 理论代价 | 代表用途 | 原文中的位置 |
|---|---|---|---|---|
| Classical Timed Automata | clocks、guards、invariants、resets | 基线可判定性最好 | 实时验证基础模型 | 所有后续扩展的出发点 |
| Parametric Timed Automata | 约束参数化 | 一般情形很快变难；`L/U` 子类较稳 | 平台无关设计、参数综合 | 实际价值非常高的一支 |
| Richer constraints / updates | 加性约束、乘法、可更新时钟等 | 许多问题转为不可判定 | 提高表达力或简洁性 | 是“表达力与可判定性 tradeoff”的集中展示区 |
| Priced / Probabilistic / Game variants | 代价、概率、博弈、控制 | 增加分析复杂度，但工具支持逐步成熟 | 最优调度、控制综合、资源分析、随机实时系统 | 体现 timed automata 从验证走向综合与量化分析 |
| Implementation-oriented variants | sampling、robustness、code synthesis | 需要引入平台和部署假设 | 从模型到实现/代码 | 回答“模型能验”和“系统能跑”之间的裂缝 |

| 工具用途 | 代表工具线 | 主要任务 | 对 `project_1` 的意义 |
|---|---|---|---|
| 实时验证 | `UPPAAL`、`Kronos`、`RED`、`VerICS` | reachability、模型检验、仿真 | 是最稳的落点 |
| 参数分析 | `IMITATOR`、`HyTech`、`TReX` | 参数综合、参数化安全分析 | 非常适合需求到模型自动化的早期设计阶段 |
| 控制综合/博弈 | `UPPAAL TIGA`、`SynthKro`、`Synthia` | controller synthesis、timed games | 能把模型从“验”推进到“合成” |
| 量化/资源分析 | `UPPAAL CORA`、`PRISM`、`Fortuna`、`Priced-Timed Maude` | cost/probability analysis | 适合资源、性能与可靠性研究 |
| 实现/代码生成 | `TIMES`、`SAVE IDE`、`AITARTOS`、`TART` | schedulability、code synthesis、deployment | 直接对应“模型落地”问题 |

## 构造方式与表示格式版图

| 形式主义/路线 | 图形表示 | 文本/DSL | 机器可处理承载 | 标准/交换格式 | 原文体现出的关键事实 |
|---|---|---|---|---|---|
| Classical Timed Automata | 是 | 工具 DSL 常见 | locations + clocks + guards + invariants + resets | 无统一标准 | 语义核心很稳定，但交换载体高度工具化 |
| Parametric Timed Automata | 是 | 参数化约束 DSL | 在 clock constraints 中引入参数 | 无统一标准 | 非常适合早期设计，但承载通常绑定具体工具 |
| Priced / Probabilistic / Game variants | 是 | 各工具自有扩展 DSL | 在 automaton 上叠加 cost/probability/game 结构 | 无统一标准 | 扩展能力强，但互操作性主要靠工具族谱，不靠通用格式 |
| Tool-specific carriers | 弱 | `UPPAAL`、`Kronos`、`RED`、`HyTech`、`PRISM` 等输入语言 | 工具私有格式 | 否 | 这条线的强项是分析工具，不是统一交换标准 |

这篇 survey 并不提供一个统一的时间自动机交换格式路线；它更多告诉我们：时间自动机的强项在“分析技术与工具”，而不是“标准化机器交换格式”。

| 路线/子类 | 自动生成最关键的结构化信息 | 为什么这一信息是关键瓶颈 |
|---|---|---|
| Classical Timed Automata | 时钟集合、reset 点、guard、invariant | 这是进入 `UPPAAL/Kronos` 类工具的最小充分结构 |
| Parametric Timed Automata | 参数化时限、参数作用域 | 没有参数边界信息，后续综合空间会失控 |
| Priced / Probabilistic / Game variants | 代价、概率、控制者角色 | 这些不是“附加注释”，而是直接改变分析问题类型 |
| Implementation-oriented variants | sampling、clock drift、平台调度假设 | 若缺这些部署假设，验证通过也不等于实现可行 |

## 基础设施与生态版图

| 工具谱系 | 主要对象 | 支持能力 | 生态成熟度 | 原文中的关键观察 |
|---|---|---|---|---|
| `UPPAAL`、`Kronos`、`RED`、`VerICS` | Classical / general analysis | reachability、模型检验、仿真 | 高 | 原文明确指出这是最成熟的一层工具生态 |
| `IMITATOR`、`HyTech`、`TReX` | Parametric Timed Automata | 参数综合、可达性、参数化安全分析 | 高 | 参数线不是边缘分支，而是成熟分析方向 |
| `UPPAAL TIGA`、`SynthKro`、`Synthia` | Game / controller variants | 控制综合、timed games | 中高 | timed automata 已不止“验证”，还进入 synthesis |
| `UPPAAL CORA`、`PRISM`、`Fortuna`、`Priced-Timed Maude` | Priced / probabilistic variants | cost/probability analysis | 中高 | 量化分析工具已形成独立分支 |
| `TIMES`、`SAVE IDE`、`AITARTOS`、`TART` | Implementation-oriented lines | schedulability、代码生成、实现验证 | 中 | 原文专门讨论模型到实现的落地问题 |

| 比较维度 | 结果 |
|---|---|
| 分析底层 | zone-based 技术是主流工程实现基础，region 更多是理论基石 |
| 地域与维护 | 工具高度集中在欧洲，`UPPAAL` 系是最活跃、维护周期最长的一支 |

## 适用场景与需求映射

| 形式主义/路线 | 适用场景 | 需求前提 | 为什么适合 | 不适合的情况 |
|---|---|---|---|---|
| Classical Timed Automata | 实时协议、调度、定时控制、时序安全验证 | 需求可抽成有限位置 + clocks + guards/invariants | 可判定性和工具成熟度最好 | 需要连续物理动力学或复杂数据结构时 |
| Parametric Timed Automata | 早期设计、平台无关建模、参数综合 | 需求中的时限可参数化表达 | 能在实现前先探索“哪些参数范围可行” | 需要强确定实现但参数空间过大时 |
| Priced / Probabilistic variants | 资源约束、性能评估、随机实时系统 | 除时限外还要表达代价或概率 | 能把“时间”与“资源/不确定性”一起纳入分析 | 只需基础 reachability 时会引入不必要复杂性 |
| Game / controller variants | 需要策略合成、控制器生成 | 需求中存在控制者/环境对抗结构 | 可以直接把验证推进到 synthesis | 只是想做单纯时序安全验证时 |
| Implementation-oriented variants | 代码生成、平台映射、执行调度 | 必须处理 clock drift、sampling、非瞬时动作 | 回答“模型怎么部署成系统” | 希望直接把抽象模型原封不动部署到平台时 |

| 需求信号 | 更适合的 timed automata 路线 | 原因 |
|---|---|---|
| 只有明确时限和重置条件 | Classical Timed Automata | 最小而稳的建模选择 |
| 时限要延后再定或依平台变化 | Parametric Timed Automata | 可以把“未知但有范围”的时序要求保留下来 |
| 还要分析成本/功耗/可靠性 | Priced / Probabilistic variants | 经典 timed automata 不足以覆盖这些量化目标 |
| 最终目标是 controller 或代码 | Game / implementation-oriented routes | 验证只是中间步骤，最终要落地到策略或实现 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

如果需求中存在明确的时间上界、下界、时钟复位和实时调度约束，那么 `Timed Automata` 是本 collection 中最成熟的验证导向目标之一。相比一般层次状态机，它的语义和工具链都更稳定。

### 对中间表示设计的启发

若 `project_1` 要把需求自动映射到时间自动机，中间表示至少要显式承载：

1. 时钟集合与复位点。
2. 守卫与不变式。
3. 可观测动作与不可观测动作。
4. 平台实现容差、sampling 或鲁棒性假设。

否则模型检查通过也不等于部署可行。

### 对后续扩库方向的启发

后续优先应补三类单篇文献：

1. 基础理论：经典 `Timed Automata` 定义与语义。
2. 工具主线：`UPPAAL`、`Kronos`、`IMITATOR`。
3. 实现主线：robustness、sampling、code synthesis。

### 原文未覆盖但本研究仍需补的空白

原文对统一交换格式和标准化承载讨论较弱，也几乎不触及面向 LLM 自动生成的 DSL 设计问题。因此它更适合作为“验证与实现地图”，不直接给出“统一建模文件格式”答案。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1994 | Classical Timed Automata | Alur, Dill, `A Theory of Timed Automata` | 经典定义论文，后续所有变体都依赖它 | 优先补单篇 `desc.md` | 🔴 |
| 1998 | Timed Automata tutorial/tool line | Bengtsson, Yi, `Timed Automata: Semantics, Algorithms and Tools` | 适合作为理论到工具的桥梁性入口 | 优先补单篇 `desc.md` | 🟠 |
| 2004 | Verification tool line | Daws et al., `Kronos` tool paper | 代表早期成熟时间自动机验证工具 | 先找工具/方法论文 | 🟡 |
| 2005 | Controller synthesis | Altisen, Tripakis, `Tools for Controller Synthesis of Timed Systems` | 代表时间自动机走向控制综合的重要分支 | 先找原文并补 `desc.md` | 🟡 |
| 2009 | Parametric timed automata | Andre, `IMITATOR` tool line | 代表参数综合方向，和需求到模型自动化关系密切 | 优先补单篇 `desc.md` | 🟠 |
| 2011 | Tool ecosystem | Behrmann, David, Larsen, `A Tutorial on UPPAAL` | 最值得优先跟踪的主流工具线 | 优先补工具条目 | 🔴 |

## 文献分类总结

- 综述主题：时间自动机变体、实现与工具生态
- 对象类型：🧱
- 覆盖主类：⏱️
- 覆盖的形式主义：经典 `Timed Automata`、参数化、概率、代价、博弈、实现导向变体
- 是否覆盖构造方式/基础设施：是，但偏工具生态，统一交换格式覆盖弱
- 主要价值：一次性把 `Timed Automata` 的理论变体、实现问题与工具版图串起来，适合做选型总览
- 状态：🟢
