# Grafchart：面向操作规程支持任务的图形程序处理语言 / GRAFCHART FOR PROCEDURAL OPERATOR SUPPORT TASKS

## 基本信息

- 标题：GRAFCHART FOR PROCEDURAL OPERATOR SUPPORT TASKS
- 中文标题：Grafchart：面向操作规程支持任务的图形程序处理语言
- 作者：Karl-Erik Arzen, Rasmus Olsson, Johan Akesson
- 发表：IFAC Proceedings Volumes, 35(1):85-90, 2002
- DOI：`10.3182/20020721-6-ES-1901.00920`
- 链接：https://doi.org/10.3182/20020721-6-ES-1901.00920
- 形式主义：Grafchart / JGrafchart
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：图形语言 / 工具载体
- 工具/实现获取方式：原文明确给出 `Grafchart` 工具箱与新的 Java 版本 `JGrafchart`，并说明可在线连接本地 I/O 或在 simulated mode 下运行。
- 标准/格式获取方式：承载方式是 `Grafchart` 图形 chart、`G2` 规则与 `JGrafchart` 运行时；原文未给出独立交换标准。

## 简报

这篇论文把 `Grafchart` 放在一个很务实的位置上：它不是拿来讲抽象自动机理论，而是拿来支撑化工与批处理工厂中的操作规程、状态迁移支持和 operator assistance。它以 `Grafcet / SFC` 为骨架，吸收 `Petri net` 和面向对象程序设计思想，在步骤、宏步骤、过程步骤、异常转移和高层 token 机制上补出了一套适合工业顺控和程序处理的图形载体。

- 形式主义定位：面向工业顺控与程序处理的图形状态机/过程图语言。
- 构造方式简述：由 `step`、`transition`、`macro step`、`procedure step`、`exception transition` 和高层 token/receptivity 组成。
- 基础设施与场景简述：依托 `Grafchart` 工具箱、`G2` 集成和 `JGrafchart` 运行时，直接服务 batch control、operator support 与 decision support。

```text
操作规程需求 -> Grafchart steps / procedures / exception transitions -> Grafchart / JGrafchart runtime -> operator support / batch control
```

## 形式主义定义与核心对象

### 定义对象

论文关心的不是一般“状态转换”，而是工业操作程序如何被稳定地表示、执行、可视化，并在出现异常时可恢复、可中止、可复用。

### 核心抽象

结合论文中的基础 `Grafchart` 与 `High-Level Grafchart`，可保守整理为：

$$
G = (Q, T, M, P, X, A)
$$

上式中的符号逐项解释如下：

1. `Q` 是普通 `step` 集合。
2. `T` 是 `transition` 集合。
3. `M` 是 `macro step` 集合，内部可再包含子图。
4. `P` 是 `procedure step`/procedure 集合，用于复用和过程调用。
5. `X` 是 token 或 token class 集合，高层 Grafchart 用其携带对象属性。
6. `A` 是与步骤和转移相关联的 actions/receptivities。

最基本的 firing 条件可写成：

$$
\mathrm{enabled}(t) \iff \bigwedge_{q \in pre(t)} active(q) \land cond_t
$$

其中：

1. `pre(t)` 是转移 `t` 的前驱步骤集合。
2. `active(q)` 表示步骤 `q` 当前为活动状态。
3. `cond_t` 是转移条件或事件。

触发后的核心效果是：

$$
\mathrm{fire}(t) \Rightarrow deactivate(pre(t)) \land activate(post(t))
$$

这里：

1. `post(t)` 是后继步骤集合。
2. 对高层 token 版本，还会把 token 从前驱步骤移动到后继步骤，或按 receptivity 动作创建/删除 token。

### 一个最小例子与通俗解释

论文最直观的对象是 procedure handling：

1. 一个 `procedure step` 调用某个操作规程，例如 `reactor-charge`。
2. 当宏步骤或过程步骤在执行时，若异常条件变真，则 `exception transition` 立即可用。
3. 被异常中止的过程会保留执行状态，后续允许 resume。

通俗地说，`Grafchart` 像“给工业操作规程做的可执行流程状态机”，并且它比普通流程图更强，因为它原生支持子过程、异常中断和对象化 token。

### 运行 / 接受 / 转移语义

论文没有把它抽成纯数学自动机理论，而是给了稳定的执行直觉。可保守写成：

$$
State_{k+1} = Exec(State_k, Inputs_k, Procedures_k)
$$

其中：

1. `State_k` 包含当前活动步骤、宏步骤/过程步骤执行位置以及 token 分布。
2. `Inputs_k` 是过程条件、事件、操作员输入或外部信号。
3. `Procedures_k` 表示当前可调用或正在执行的过程体。
4. `Exec` 依据 enabled transitions、异常转移、过程调用与 G2 规则产生下一状态。

对高层 Grafchart，receptivity 的直觉可以写成：

$$
\mathrm{enabled}(r) \iff token\_class(x) \in pre(r) \land cond_r(x)
$$

也就是：

1. 某个 token 类实例必须已在前驱步骤中出现。
2. 其属性满足 receptivity 条件。
3. 之后可执行 token 移动、删除、创建或任意 `G2` 动作。

### 语义边界

这个形式主义的边界非常工程化：

1. 它强在程序处理和顺序控制，而不是可判定性边界分析。
2. 它依赖工具运行时和对象系统，而不是开放数学核心。
3. 它的“时间”更多是过程推进和事件响应，不是显式时钟约束。

### 关键性质与判定边界

论文强调的关键性质包括：

1. `macro step` 与 `procedure step` 支持层次与可复用程序块。
2. `exception transition` 支持过程执行中的异步中止。
3. 高层 Grafchart 用 token attributes 处理对象化批处理与资源分配。
4. `JGrafchart` 支持在线 I/O、仿真、动画和 token tracing，利于操作员可视化。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `step`、`macro step`、`procedure step` 都是核心控制状态。 |
| 事件 / 触发 | 强支持 | 转移可由条件或事件触发，异常转移在执行中始终有效。 |
| 守卫 / 数据 | 强支持 | `G2` 规则、receptivity、token attributes 都显式进入语义。 |
| 层次 | 强支持 | 宏步骤和过程步骤提供层次化图结构。 |
| 并发 / 同步 | 部分支持 | 来源于 `Grafcet/SFC` 与 `Petri net` 的并发直觉，但论文重心在顺控程序。 |
| 时间约束 | 部分支持 | 面向程序推进与在线执行，不是显式时钟模型。 |
| 连续动态 / 随机性 | 不支持 | 主要描述离散过程规程。 |
| 可执行 / 可验证性 | 强支持 | 工具箱、`G2` 集成和 `JGrafchart` runtime 直接可执行。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$G = (Q, T, M, P, X, A)$` | `Grafchart` 由步骤、转移、宏步骤、过程步骤、token 与动作构成。 |
| 转移启用 | `$\mathrm{enabled}(t) \iff \bigwedge_{q \in pre(t)} active(q) \land cond_t$` | 所有前驱步骤都激活且条件满足时，转移才可触发。 |
| 触发效果 | `$\mathrm{fire}(t) \Rightarrow deactivate(pre(t)) \land activate(post(t))$` | 触发后前驱停用、后继启用。 |
| 高层 token 语义 | `$\mathrm{enabled}(r) \iff token\_class(x) \in pre(r) \land cond_r(x)$` | 高层 Grafchart 用 token 属性控制对象化程序流。 |

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 基础 `step / transition` 图。
2. `macro step` 与 `procedure step`。
3. `exception transition`。
4. 高层 token class 与 receptivity。

### 机器可处理承载方式

机器可处理承载有两条线：

1. 早期 `Grafchart` 与 `G2` 规则系统集成。
2. Java 化的 `JGrafchart` 编辑器与运行时。

### 交换与互操作

论文重点在执行与操作支持，不在开放交换。它更像一个工程工具载体，而不是行业中立格式。

## 配套基础设施

- 建模/编辑工具：`Grafchart` toolbox、`JGrafchart` graphical editor。
- 解析/交换/元模型支持：依托 `G2` 对象系统和 Java 运行时，支持 procedures、methods 和 token classes。
- 仿真/执行支持：`JGrafchart` 可在线连接本地 I/O，也可在 simulated mode 下运行。
- 验证/分析支持：论文更强调操作支持和结构化建模，而非独立模型检查器。
- 代码生成/转换支持：以运行时执行和程序处理为主，未强调独立代码生成标准。
- 标准化或社区生态：研究和工业原型生态清晰，但无通用开放标准。

## 适用场景与需求前提

### 适用场景

适合化工/流程工业的启动、停机、配方执行、批处理、故障辅助和 operator support。

### 需求前提

1. 需求核心是顺序化程序或操作规程。
2. 需要宏步骤、过程复用和异常中止。
3. 希望操作员看到当前活动步骤与历史执行轨迹。
4. 需要把过程逻辑与对象属性或设备方法关联起来。

### 不适用或高成本场景

若重点是开放模型交换、精确定时验证或复杂连续控制律，`Grafchart` 不是最优第一选择。

## 与相邻形式主义的关系

相对 `Grafcet/SFC`，它加入过程、宏步骤、异常转移与对象方法；相对 `Petri net`，它更图形化、更贴近工业顺控；相对 `StateGraph`，它更直接服务 operator support 与程序处理。

## 与本研究的关系

### 对 Project 1 的价值

它提供了一个“规程型状态机载体”的成熟实例，说明状态机不一定只服务控制器执行，也能直接服务操作支持。

### 作为目标形式主义还是中间表示

在程序处理/批处理场景下，它可以直接作为目标形式主义；在通用研究链中，也适合作为面向工业操作规程的后端载体。

### 对需求到模型生成的启发

如果需求里充满“步骤、操作规程、异常中断、可恢复过程”这类词，生成 `Grafchart` 比生成普通平面状态图更贴近真实使用语境。

### 现实限制

它对 `G2/JGrafchart` 运行时依赖较强，跨生态共享能力弱于标准化载体。

## 重要的相关工作

### 奠基或前身工作

- `Grafcet / Sequential Function Charts`
- `Petri Nets`

### 同类型或同家族工作

- `JGrafchart`
- `High-Level Grafchart`
- `StateGraph`

### 标准 / 格式 / 工具链工作

- `G2` 规则与对象系统
- 批处理 `S88` 相关建模实践

### 与本研究关系最紧的工作

- 它展示了状态机在工业操作支持、程序规程和批处理上的专用落点。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 形式主义：Grafchart / JGrafchart
- 论文角色：图形语言 / 工具载体
- 核心功能：把工业操作规程、过程调用和异常中止统一进一个可执行图形状态机载体。
