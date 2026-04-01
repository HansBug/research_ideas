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

这意味着它既能回答“这个形式主义能不能表达”，也能回答“有没有工具”和“生成出来以后能不能跑”。

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| Classical Timed Automata | 是 | 依工具而定 | 原文未系统比较统一格式 | 否 | 核心元素是 location、clock、guard、reset、invariant |
| Parametric Timed Automata | 是 | 依工具而定 | 原文未系统比较统一格式 | 否 | 在 clock constraints 中引入参数 |
| Priced / Probabilistic / Game variants | 是 | 依工具而定 | 原文未系统比较统一格式 | 否 | 扩展守卫、代价、概率或博弈结构 |
| Tool-specific carriers | 否 | `UPPAAL`、`Kronos`、`RED`、`HyTech` 等各自输入语言 | 有工具私有格式 | 否 | 原文重工具，不重统一交换标准 |

这篇 survey 并不提供一个统一的时间自动机交换格式路线；它更多告诉我们：时间自动机的强项在“分析技术与工具”，而不是“标准化机器交换格式”。

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| Timed Automata | `UPPAAL`、`Kronos`、`RED`、`VerICS` | reachability、模型检验、仿真 | 高 | 原文明确指出 `UPPAAL` 系长期最活跃 |
| Parametric Timed Automata | `IMITATOR`、`HyTech`、`RED`、`TReX` | 参数综合、可达性、参数化安全分析 | 高 | 适合平台/配置空间探索 |
| Controller / Game variants | `UPPAAL TIGA`、`SynthKro`、`Synthia` | 控制综合、博弈求解 | 中高 | 偏策略生成与调度 |
| Code synthesis / implementation | `TIMES`、`SAVE IDE`、`TART`、`AITARTOS` | 调度、代码生成、实现验证 | 中 | 原文专门讨论其实现挑战 |
| Probabilistic / priced variants | `PRISM`、`UPPAAL PRO`、`Fortuna`、`Priced-Timed Maude` | 概率分析、成本分析 | 中高 | 适合量化性能与资源问题 |

原文还观察到，绝大多数研究工具集中在欧洲，尤其是 `UPPAAL` 与 `Verimag` 两大阵营。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| Classical Timed Automata | 实时协议、调度、定时控制、时序安全验证 | 需求可抽成有限位置 + clocks + guards/invariants | 需要连续物理动力学或复杂数据结构时 |
| Parametric Timed Automata | 早期设计、平台无关建模、参数综合 | 需求中的时限可参数化表达 | 需要强确定实现但参数空间过大时 |
| Priced / Probabilistic variants | 资源约束、性能评估、随机实时系统 | 除时限外还要表达代价或概率 | 只需基础 reachability 时会引入不必要复杂性 |
| Implementation-oriented variants | 代码生成、平台映射、执行调度 | 必须处理 clock drift、sampling、非瞬时动作 | 希望直接把抽象模型原封不动部署到平台时 |

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
