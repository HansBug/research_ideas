# 为 JGrafchart 增加 FMI 协同仿真支持 / On Extending JGrafchart with Support for FMI for Co-Simulation

## 基本信息

- 标题：On Extending JGrafchart with Support for FMI for Co-Simulation
- 中文标题：为 JGrafchart 增加 FMI 协同仿真支持
- 作者：Alfred Theorin, Charlotta Johnsson
- 发表：Proceedings of the 10th International Modelica Conference, 1257-1263, 2014
- DOI：`10.3384/ecp140961257`
- 链接：https://doi.org/10.3384/ecp140961257
- 形式主义：Grafchart / JGrafchart with `FMI` co-simulation
- 主类：📦
- 描述客体：🌡️
- 所属领域：🌡️
- 论文角色：工具扩展 / 协同仿真载体
- 工具/实现获取方式：原文明确依托 `JGrafchart`、`CustomIO`、`SocketIO` 和 `FMI` 相关 Java/C 包装器，讨论多种实现路径。
- 标准/格式获取方式：承载方式是 `Grafchart` 模型、`FMU`、`FMI` XML 元数据和 co-simulation master/slave API。

## 简报

这篇论文关注的是一个非常现实的落地问题：`JGrafchart` 很适合写顺控和规程逻辑，但如果要把它放进 `Modelica/FMU` 世界里，与连续物理模型联合仿真，应该怎样接入 `FMI for Co-Simulation`。作者没有停留在“理论上可以”，而是把 `JGrafchart` 的 scan-cycle 语义、可导出的状态、主从架构和三种集成方案都梳理清楚了。

- 形式主义定位：面向离散控制逻辑与连续物理模型联调的图形状态机载体。
- 构造方式简述：保留 `Grafchart` 的 steps/transitions/scan cycle，再把其 I/O 和执行状态映射到 `FMU`/communication step 接口。
- 基础设施与场景简述：依托 `JGrafchart`、`FMI`、`FMU`、`Modelica` 工具链，服务控制器与被控对象的协同验证。

```text
控制逻辑需求 -> Grafchart / JGrafchart 应用 -> FMI wrapper / FMU -> 与物理模型联合 co-simulation
```

## 形式主义定义与核心对象

### 定义对象

论文的关键对象不是单独的状态机，也不是单独的物理模型，而是“按 scan cycle 执行的离散控制器如何成为 co-simulation 里的一个 slave 或 FMU”。

### 核心抽象

结合论文中的 `FMI` 主从结构，可保守整理为：

$$
CS = (M, \mathcal{S}, h, \Sigma)
$$

上式中的符号逐项解释如下：

1. `M` 是 `FMI master`。
2. `\mathcal{S}` 是 slave 集合，其中之一可以是 `JGrafchart` 控制器。
3. `h` 是 communication step size。
4. `\Sigma` 是在 communication points 交换的输入输出接口。

论文还明确指出 `JGrafchart` 应用状态至少包含：

$$
State_{JG} = (V, S_a, T_a, C_p)
$$

其中：

1. `V` 是变量值集合。
2. `S_a` 是当前活跃的 steps 集合。
3. `T_a` 是活跃 steps 的持续时间属性，如 `t` 与 `s`。
4. `C_p` 是当前活跃的 procedure calls。

底层 `Grafchart` 切换仍保留基本语义：

$$
\mathrm{enabled}(t) \iff \bigwedge_{s \in pre(t)} active(s) \land cond_t
$$

$$
\mathrm{fire}(t) \Rightarrow deactivate(pre(t)) \land activate(post(t))
$$

### 一个最小例子与通俗解释

论文沿用了一个最简单的 Grafchart 片段来解释执行模型：

1. 上方 step 激活时执行 `S` 动作，把 `var` 设为 `7`。
2. 当 guard `cond == 4` 成立时，transition 触发。
3. 上方 step 失活，下方 step 激活，并把 `var` 设为 `12`。
4. 若把这个控制器放进 `FMI`，则 communication point 最理想地应落在每个 scan cycle 的前后。

通俗地说，论文关心的是：`JGrafchart` 像一个按拍子工作的离散控制器，而 `FMI` 像一个负责全局节拍协调的总导演，二者需要在 communication points 对上节奏。

### 运行 / 接受 / 转移语义

论文把 co-simulation 执行描述为逐个 communication step 推进：

$$
t_{k+1} = t_k + h_k
$$

其中：

1. `t_k` 是第 `k` 个 communication point。
2. `h_k` 是该步选择的 communication step size。
3. 每个 slave 在 `t_k` 到 `t_{k+1}` 之间独立推进。

与此同时，`JGrafchart` 本身仍按 scan cycle 周期执行：

$$
Cycle = ReadInputs \rightarrow Mark \rightarrow Fire \rightarrow Update \rightarrow Sleep
$$

其中：

1. `ReadInputs` 读取 I/O。
2. `Mark` 标记可触发迁移。
3. `Fire` 执行迁移。
4. `Update` 更新 step 属性和动作。
5. `Sleep` 等待下一个周期。

### 语义边界

这篇论文的边界也很明确：

1. 工作重点是 `JGrafchart` 接入 `FMI for Co-Simulation`，不是重新定义 `FMI`。
2. 文中方案仍是概念设计，尚未完全实现。
3. 为支持 redo communication steps，需要 `JGrafchart` 暴露和恢复内部执行状态。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| co-simulation 骨架 | `$CS = (M, \mathcal{S}, h, \Sigma)$` | `FMI master/slave` 和 communication step 是主线。 |
| 控制器状态 | `$State_{JG} = (V, S_a, T_a, C_p)$` | `JGrafchart` 的变量、活跃 steps 和过程调用都要能被 co-simulation 管理。 |
| communication step | `$t_{k+1} = t_k + h_k$` | 仿真按离散 communication points 推进。 |
| Grafchart 切换 | `$\mathrm{enabled}(t) \iff \bigwedge_{s \in pre(t)} active(s) \land cond_t$` | 控制器内部仍遵循 Grafchart 的 step-transition 语义。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 继承 `Grafchart/JGrafchart` 的 step/transition、过程和异常机制。 |
| 事件 / 触发 | 强支持 | guard 条件和通信点共同控制执行。 |
| 守卫 / 数据 | 强支持 | `JGrafchart` 变量和 FMU 输入输出直接相关。 |
| 层次 | 部分支持 | 保留 Grafchart 的层次和 procedure 结构。 |
| 并发 / 同步 | 部分支持 | co-simulation 层面由 master 协调，控制器内部仍是 scan-cycle 离散执行。 |
| 时间约束 | 强支持 | communication step、scan cycle 和 redo step 是全文重点。 |
| 连续动态 / 随机性 | 部分支持 | 连续动态由其他 FMU 表达，`JGrafchart` 负责离散控制侧。 |
| 可执行 / 可验证性 | 强支持 | 目标是把控制应用放进真实 co-simulation 流程中验证。 |

### 形式化问题与性质

1. 原文提出三条路线：hardware-in-the-loop、generic FMI wrapper、standalone FMU。
2. `JGrafchart` 的 I/O 类型与 `FMI` 基本数据类型有天然对应，这降低了接入成本。
3. 外部时钟、状态读写和 communication step redo 是能否真正成为 `FMU` 的关键能力。
4. 论文明确指出 `JGrafchart` 与 `Modelica state machines` 各有长短：前者 procedures/exception 强，后者 mutual hierarchy 强。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `Grafchart` 的 steps/transitions/actions。
2. `JGrafchart` 的 `CustomIO` 和 `SocketIO`。
3. `FMI` 的 `FMU`、`DefaultExperiment`、capabilities 和 XML 元数据。

### 机器可处理承载方式

机器可处理承载有三种：

1. 把 `JGrafchart` 作为 hardware-in-the-loop 外部控制器。
2. 用 generic wrapper 把 `JGrafchart` 接成一个通用 `FMU`。
3. 通过代码生成或打包导出 standalone `FMU`。

### 交换与互操作

这篇论文的互操作核心是 `FMI` 标准：`FMU` 的 XML 描述、master/slave API、communication step 能力声明以及 Java/C 包装器。

## 配套基础设施

- 建模/编辑工具：`JGrafchart`。
- 解析/交换/元模型支持：`FMI` XML、`FMU` 资源、`CustomIO/SocketIO`。
- 仿真/执行支持：`FMI master` 协调 co-simulation，各 FMU slave 独立推进。
- 验证/分析支持：主要是通过联合仿真做控制器行为验证，而非离散模型检查。
- 代码生成/转换支持：论文讨论 generic wrapper、embedded export 与 standalone FMU 三种路径。
- 标准化或社区生态：依托 `FMI`、`Modelica` 和相关 Java/Python wrapper 生态。

## 适用场景与需求前提

### 适用场景

适合自动化控制器需要和连续物理过程模型联调、在上线前验证控制逻辑对 plant 的作用、或把图形顺控逻辑接入 `Modelica/FMU` 生态的场景。

### 需求前提

1. 控制逻辑本质上是离散 scan-cycle 状态机。
2. 被控对象或环境可作为 `FMU` 提供。
3. 需要在 communication points 交换输入输出。
4. 愿意为外部时钟、状态恢复和 wrapper/导出能力改造 `JGrafchart`。

### 不适用或高成本场景

如果只需要本地顺控执行、不需要物理联仿，或者要求现成成熟实现而不是概念设计，这条路线会显得成本偏高。

## 与相邻形式主义的关系

相对普通 `JGrafchart`，它增加了对物理模型联合仿真的入口；相对 `Modelica state machines`，它更强于 procedures 和 exception handling；相对纯 `FMU` 组件，它保留了更友好的图形控制逻辑表示。

## 与本研究的关系

### 对 Project 1 的价值

它说明状态机生成并不应止于“生成图”。如果后续研究要做生成-验证-修复闭环，那么把控制状态机接入 plant co-simulation 是非常实际的一步。

### 作为目标形式主义还是中间表示

更适合作为面向仿真验证的目标载体或后端导出路径，而不是抽象需求侧中间表示。

### 对需求到模型生成的启发

当需求最终要落到“控制器 + 被控对象”联合验证时，生成状态机时就应考虑其 I/O 类型、scan cycle 和 future FMU export 能力。

### 现实限制

论文仍是概念评估；真正工业可用还需要补齐实现、状态回放和导出稳定性。

## 重要的相关工作

### 奠基或前身工作

- `Grafchart`
- `JGrafchart`
- `FMI / FMI for Co-Simulation`

### 同类型或同家族工作

- `Modelica State Machines`
- 控制器与 plant 的联合 co-simulation 路线

### 标准 / 格式 / 工具链工作

- `FMU`
- `CustomIO / SocketIO`
- `JFMI / PyFMI`

### 与本研究关系最紧的工作

- 它把图形状态机和物理模型验证链连起来，对后续“需求到可验证控制模型”的闭环非常关键。

## 文献分类总结

- 主类：📦
- 描述客体：🌡️
- 所属领域：🌡️
- 形式主义：Grafchart / JGrafchart with `FMI` co-simulation
- 论文角色：工具扩展 / 协同仿真载体
- 核心功能：把图形顺控状态机接入 `FMI` 协同仿真生态，与动态物理模型联合验证。
- 关键特性：communication step、wrapper/FM U 导出路线、scan-cycle 对齐、状态恢复需求。
- 构造方式：`JGrafchart` 应用 + `CustomIO/SocketIO` + `FMI/FMU` 元数据与包装器。
