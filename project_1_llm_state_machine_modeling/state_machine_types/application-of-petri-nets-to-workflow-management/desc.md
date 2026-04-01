# Petri 网在工作流管理中的应用 / The Application of Petri Nets to Workflow Management

## 基本信息

- 标题：The Application of Petri Nets to Workflow Management
- 中文标题：Petri 网在工作流管理中的应用
- 作者：Wil M. P. van der Aalst
- 发表：Journal of Circuits, Systems, and Computers, 8(1):21-66, 1998
- DOI：`10.1142/S0218126698000043`
- 链接：https://doi.org/10.1142/S0218126698000043
- 形式主义：WorkFlow net (WF-net)
- 主类：🕸️
- 描述客体：🏭
- 所属领域：💻
- 论文角色：领域特化
- 工具/实现获取方式：论文列举了 `ExSpect`、`COSA`、`INCOME`、`Woflan` 等 Petri-net-based workflow tools，但不提供统一下载入口。
- 标准/格式获取方式：本文使用经典/高阶 `Petri Net` 语义定义工作流网，尚未给出后来 `PNML` 式标准交换载体。

## 简报

这篇论文的价值不只是“Petri 网可用于工作流”，而是明确把单 case 的流程生命周期压成一种专门子类 `WF-net`，再把 soundness、free-choice、well-structured、S-coverable 等可分析结构直接绑定到工作流质量上。它把工作流从“软件系统里的流程脚本”提升成“可验证的网模型”。

- 形式主义定位：面向工作流过程生命周期的 `Petri Net` 特化子类。
- 构造方式简述：用 place 表示条件、transition 表示任务、token 表示 case 的当前工作流状态。
- 基础设施与场景简述：依托 Petri net 分析理论，可直接问流程是否 sound、是否 safe、是否有 dead task，并能挂接工作流工具。

```text
业务流程与路由规则 -> WF-net -> marking / soundness / structural analysis -> workflow design / verification / enactment
```

## 形式主义定义与核心对象

### 定义对象

原文关心的是“一个 case 在工作流中的生命周期如何被建模和验证”。因此模型对象不是一般并发系统，而是带有开始条件、结束条件、路由分支和任务执行约束的流程网。

### 核心抽象

论文先使用经典 Petri 网：

$$
PN = (P, T, F)
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合，对应条件或状态片段。
2. `T` 是 transition 集合，对应任务或控制路由动作。
3. `F \subseteq (P \times T) \cup (T \times P)` 是弧集合。

标识由 marking 给出：

$$
M : P \to \mathbb{N}
$$

其中 `M(p)` 表示 place `p` 中 token 的数量。

在此基础上，论文定义工作流网：

$$
WF = (P, T, F, i, o)
$$

其中：

1. `i` 是唯一输入 place，表示一个新 case 的开始条件。
2. `o` 是唯一输出 place，表示 case 完成后的结束条件。
3. 若加入额外 transition `t^*`，使 `o \to t^* \to i`，则扩展后的网必须强连通。

### 一个最小例子与通俗解释

最小例子是“任务 `A` 做完后再做任务 `B`”：

1. `c1` 放一个 token，表示 case 已启动。
2. 触发 transition `A` 后，token 从 `c1` 走到 `c2`。
3. 只有 `c2` 中有 token 时，`B` 才能触发。
4. `B` 完成后 token 到达 `o`。

通俗解释是：`WF-net` 像把流程图改写成“token 在条件节点里流动”的系统。任务能不能做，不靠人脑去读箭头，而靠 token 是否到位来决定。

### 运行 / 接受 / 转移语义

论文沿用经典 Petri 网 firing 语义。若 `t \in T`，则：

$$
M \xrightarrow{t} M'
$$

当且仅当 `t` 在 `M` 下使能，并在 firing 后得到 `M'`。

对经典网，`t` 的使能条件可写为：

$$
\forall p \in {}^\bullet t,\quad M(p) \ge 1
$$

触发后：

$$
M'(p) = M(p) - 1 \ \text{for } p \in {}^\bullet t,\qquad
M'(p) = M(p) + 1 \ \text{for } p \in t^\bullet
$$

工作流语境下，初始 marking 通常是：

$$
M_i = [i]
$$

而目标终止状态是：

$$
M_o = [o]
$$

这里的符号逐项解释如下：

1. `${}^\bullet t` 是 transition `t` 的输入 place 集合。
2. `t^\bullet` 是 transition `t` 的输出 place 集合。
3. `[i]` 表示只有输入 place `i` 上有一个 token。
4. `[o]` 表示只有输出 place `o` 上有一个 token。

### 语义边界

`WF-net` 是 `Petri Net` 的领域化子类，因此它保留并发、同步和资源流表达力，但把工作流的基本结构约束收紧到：

1. 一个入口 place。
2. 一个出口 place。
3. 所有节点都必须服务于从入口到出口的 case 处理。

它不直接处理完整应用数据，工作流属性需要靠高层网的 color 或额外条件补充。

### 关键性质与判定边界

这篇论文最重要的性质是 soundness。原文定义如下：

$$
\forall M,\ ( [i] \xrightarrow{*} M ) \Rightarrow ( M \xrightarrow{*} [o] )
$$

$$
\forall M,\ ( [i] \xrightarrow{*} M \land M \ge [o] ) \Rightarrow M = [o]
$$

$$
\forall t \in T,\ \exists M, M'.\ [i] \xrightarrow{*} M \xrightarrow{t} M'
$$

上面三条分别对应：

1. 从任一可达状态都仍然能走到正确终止。
2. 一旦结束 place 中出现 token，其他地方就不应再残留 token。
3. 不允许 dead transition，也就是任何任务都必须在某条合法路径上可执行。

论文进一步给出一个非常实用的等价转化。对 short-circuited 扩展网 `\overline{PN}`：

$$
\overline{PN} = (P, T \cup \{t^*\}, F \cup \{(o,t^*),(t^*,i)\})
$$

有：

$$
WF\text{-net sound} \iff (\overline{PN}, [i]) \text{ is live and bounded}
$$

这使得工作流验证可以直接复用标准 Petri net analysis。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 以 place / marking 显式表示流程条件。 |
| 事件 / 触发 | 部分支持 | 任务触发依赖使能，而不是事件标签中心语义。 |
| 守卫 / 数据 | 部分支持 | 经典 `WF-net` 不带数据，高层网可补颜色与属性。 |
| 层次 | 部分支持 | 原文把 hierarchy 视作可扩展方向，不是核心定义。 |
| 并发 / 同步 | 强支持 | `AND-split` / `AND-join` 是工作流路由核心。 |
| 时间约束 | 部分支持 | 论文明确说时间需依赖 timed Petri net 扩展。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 token 流。 |
| 可执行 / 可验证性 | 强支持 | soundness、liveness、boundedness、safeness 都可分析。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础网 | `$PN=(P,T,F)$` | place / transition / arc 的经典 Petri 网骨架。 |
| 工作流网 | `$WF=(P,T,F,i,o)$` | 一个入口、一个出口、无悬空节点的流程网。 |
| 触发语义 | `$M \xrightarrow{t} M'$` | 某任务在 marking `M` 下被执行。 |
| 正确终止 | `$\forall M,\ [i]\xrightarrow{*}M \Rightarrow M\xrightarrow{*}[o]$` | 任一可达流程状态都不应陷入死局。 |
| Proper termination | `$([i]\xrightarrow{*}M \land M \ge [o]) \Rightarrow M=[o]$` | 到达结束条件时不能遗留脏 token。 |
| 无死任务 | `$\forall t\in T,\ \exists M,M'.\ [i]\xrightarrow{*}M\xrightarrow{t}M'$` | 每个任务都必须真有机会执行。 |
| 验证等价 | `$WF\text{-net sound} \iff (\overline{PN},[i])$ live and bounded` | 可把流程正确性翻译成标准网性质。 |

## 构造方式与承载格式

### 建模入口

建模入口很清晰：任务画成 transition，条件画成 place，case 画成 token；随后把顺序、并行、条件分支、迭代路由映射成固定网结构。

### 机器可处理承载方式

原文使用的是经典 `Petri Net` 及其高层扩展，而不是专门的工作流 XML。机器可处理层面主要依赖：

1. 网结构 `P/T/F`。
2. marking。
3. `WF-net` 的入口/出口与结构约束。

### 交换与互操作

本文发表于 `PNML` 之前，因此没有给出统一交换标准。它的互操作优势主要来自“工作流可先落在 vendor-independent Petri net 上”，再由不同工具消费。

## 配套基础设施

- 建模/编辑工具：论文列举 `ExSpect`、`COSA`、`INCOME`、`Protos` 等工作流/网工具。
- 解析/交换/元模型支持：当时尚无统一 XML 标准，主要依靠 Petri net 抽象作为共同中间层。
- 仿真/执行支持：可作为 workflow enactment 的过程骨架。
- 验证/分析支持：`Woflan` 被明确作为 workflow analyzer，检查 soundness、free-choice、well-structuredness、S-coverability 等。
- 代码生成/转换支持：原文重点不在代码生成。
- 标准化或社区生态：工作流管理系统与 Petri net 工具生态之间形成了较清晰的桥接。

## 适用场景与需求前提

### 适用场景

适合业务流程、审批流程、服务过程、文档流转，以及任何“任务路由 + 并发分支 + 同步汇合 + 正确终止”比数据运算本身更关键的系统。

### 需求前提

1. 需求中存在清晰的任务、前后置条件和 case 流转。
2. 重点是流程路由正确性，而不是复杂数值计算。
3. 需要验证流程是否会死锁、是否会残留脏状态、是否存在永远执行不到的任务。

### 不适用或高成本场景

若系统核心不是流程路由，而是复杂数据守卫、连续控制律或细粒度接口协商，纯 `WF-net` 就会不够，需要 colored/timed/hierarchical 扩展，甚至转向 `EFSM` 或 `Statechart`。

## 与相邻形式主义的关系

相对一般 `Petri Net`，`WF-net` 是带入口/出口和流程完结语义的领域化子类；相对 `Statechart`，它更适合表达并发路由和同步汇合；相对 `CFSM`，它弱在消息协议语义，强在流程结构和 soundness 分析。

## 与本研究的关系

### 对 Project 1 的价值

它提供了一个非常典型的“应用领域反推形式主义”的样本：论文不是先讲抽象理论再找例子，而是从 workflow management 反推出一种稳定、可验证的专门网模型。

### 作为目标形式主义还是中间表示

更适合作为特定流程子系统的目标模型，或作为需求到形式化流程模型的候选输出；对整个控制系统来说，它通常是局部视图而非唯一统一视图。

### 对需求到模型生成的启发

当需求文字里充满“先做 A，再并行做 B/C，汇合后做 D，若条件 X 则转 E”这种 routing 描述时，直接生成 `WF-net` 往往比强行生成层次状态机更自然。

### 现实限制

它对流程正确性很强，但对复杂数据与外部对象生命周期表达较弱，因此自动化建模时常要和高层网或其他状态机类型协同。

## 重要的相关工作

### 奠基或前身工作

- 经典 `Petri Net` 本体与 liveness / boundedness / safeness 理论。

### 同类型或同家族工作

- high-level / colored / timed / hierarchical Petri net 扩展。
- workflow-specific subclasses，如 free-choice、well-structured、S-coverable `WF-net`。

### 标准 / 格式 / 工具链工作

- `Woflan` 是文中最直接的 workflow verification 工具线。
- 论文写作时间早于 `PNML` 标准化成熟期。

### 与本研究关系最紧的工作

- 与 `project_1` 最相关的是“特定应用领域如何催生专门状态机/网模型”这条经验。

## 文献分类总结

- 主类：🕸️
- 描述客体：🏭
- 所属领域：💻
- 形式主义：WorkFlow net (WF-net)
- 论文角色：领域特化
- 核心功能：把单 case 工作流生命周期压成可分析的 Petri 网子类。
- 关键特性：单入口/单出口、soundness、proper termination、dead transition 分析。
- 构造方式：任务映射为 transition，条件映射为 place，case 映射为 token。
