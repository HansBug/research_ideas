# 时间 Petri 网 / Time Petri Nets Part II: State Class based methods

## 基本信息

- 标题：Time Petri Nets Part II: State Class based methods
- 中文标题：时间 Petri 网（第二部分：基于状态类的方法）
- 作者：Bernard Berthomieu
- 发表：ATPN tutorial slides, 2008
- DOI：原文未提供
- 链接：https://projects.laas.fr/tina/papers/TPNII.pdf
- 形式主义：Time Petri Nets
- 主类：🕸️
- 描述客体：🏭
- 所属领域：⏱️
- 论文角色：教程讲义
- 工具/实现获取方式：文档来自 TINA 路线，且专门列有 application areas 和 tools。
- 标准/格式获取方式：原文仍是数学/讲义表达，不提供统一标准文件格式。

## 简报

这份讲义把 `Time Petri Nets` 的核心语义和 state class 分析线压得很清楚：基础 P/T 网骨架不变，但每个变迁附有静态时间区间，状态由 `(marking, interval function)` 描述，再通过 state class graph 把连续时间状态空间做抽象分析。

- 形式主义定位：给 Petri 网加入显式时间区间的实时并发模型。
- 构造方式简述：`(P,T,Pre,Post,m0,Is)`，其中 `Is` 是静态区间函数。
- 基础设施与场景简述：讲义明确覆盖 decidability、state classes、subclasses、extensions、application areas、tools，适合补足时间网的工具线与分析线。

```text
并发实时需求 -> P/T 网 + 变迁时间区间 -> 时间 Petri 网 -> 状态类图/可达性/定量分析
```

## 形式主义定义与核心对象

### 定义对象

该模型描述的是带时间窗口的并发资源流与事件触发过程。

### 核心抽象

讲义给出的核心定义是：

$$
(P, T, Pre, Post, m_0, Is)
$$

其中 `(P,T,Pre,Post,m_0)` 是基础 Petri 网，`Is` 是把每个变迁映射到时间区间的静态区间函数。状态由 `(m, I)` 构成，`m` 是 marking，`I` 是 enabled transitions 上的 firing interval。

### 语义边界

它比基础 Petri 网多了显式时间，但仍然没有一般连续动力学；时间表现为变迁何时最早/最晚可发生。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 部分支持 | 仍以 marking 为状态骨架。 |
| 事件 / 触发 | 支持 | 变迁触发。 |
| 守卫 / 数据 | 部分支持 | 核心是时间区间，不是复杂数据。 |
| 层次 | 不支持 | 非层次模型。 |
| 并发 / 同步 | 强支持 | 保留 Petri 网并发优势。 |
| 时间约束 | 强支持 | earliest/latest firing times 是核心。 |
| 连续动态 / 随机性 | 不支持 | 无连续微分；随机非本讲义重点。 |
| 可执行 / 可验证性 | 强支持 | state class graph、trace/state preserving 抽象是重点。 |

## 构造方式与承载格式

### 建模入口

先建立 P/T 网，再为变迁附加静态时间区间。

### 机器可处理承载方式

讲义没有定义统一 XML/DSL；机器处理入口来自数学结构和后续工具实现。

### 交换与互操作

原文未定义交换标准，但与 TINA 工具链关系紧密。

## 配套基础设施

- 建模/编辑工具：文档明确讨论 tools。
- 解析/交换/元模型支持：原文未定义标准交换格式。
- 仿真/执行支持：支持 firing schedules 与状态空间构造。
- 验证/分析支持：state class graph、trace preserving/state preserving/branching analyses。
- 代码生成/转换支持：原文未说明。
- 标准化或社区生态：依附时间网分析社区和 TINA 线。

## 适用场景与需求前提

### 适用场景

适用于需要同时表达并发资源流和时间窗口的系统，例如调度、实时通信、时间受限工作流。

### 需求前提

1. 需求本体更像并发网而不是单状态控制器。
2. 关键时序可以落到变迁最早/最晚发生时间。
3. 需要状态类抽象和实时可达性分析。

### 不适用或高成本场景

若系统主要是层次模式切换且时间约束围绕单组件时钟，更适合 `Timed Automata`。

## 与相邻形式主义的关系

相对基础 `Petri Nets`，它加入显式时间区间；相对 `Timed Automata`，它更擅长资源流并发；相对 `Coloured Petri Nets`，它强化时间而非高层数据。

## 与本研究的关系

### 对 Project 1 的价值

它提供了“并发 + 时间”同时存在时的关键候选形式主义。

### 作为目标形式主义还是中间表示

适合特定实时并发控制场景的目标形式主义。

### 对需求到模型生成的启发

当需求中既有资源同步，又有最早/最晚发生窗口时，时间 Petri 网比单体定时状态机更自然。

### 现实限制

标准化承载格式不如 UML/SCXML 明确，学习门槛也更高。

## 重要的相关工作

### 奠基或前身工作

- Merlin 1974 时间 Petri 网定义。

### 同类型或同家族工作

- State class graph 分析线。
- 时间网子类与扩展。

### 标准 / 格式 / 工具链工作

- TINA 工具线。

### 与本研究关系最紧的工作

- 并发实时控制需求的结构化建模与验证。

## 文献分类总结

- 主类：🕸️
- 描述客体：🏭
- 所属领域：⏱️
- 形式主义：Time Petri Nets
- 论文角色：教程讲义
- 核心功能：在 Petri 网上加入变迁时间区间并支持状态类分析。
- 关键特性：静态区间函数、state class graph、实时可达性分析。
- 构造方式：P/T 网 + 变迁 firing interval。
- 基础设施：TINA 线分析方法与工具，未给统一标准文件格式。
- 适用场景：实时并发流程、调度、时间受限资源流。
- 需求前提：需求既有并发资源关系又有时间窗口。
- 状态：🟢
