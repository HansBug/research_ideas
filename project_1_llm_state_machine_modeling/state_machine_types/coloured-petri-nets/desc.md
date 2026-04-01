# 着色 Petri 网 / Coloured Petri Nets

## 基本信息

- 标题：Coloured Petri Nets
- 中文标题：着色 Petri 网
- 作者：Kurt Jensen
- 发表：Tutorial slide set, University of Aarhus, 2005
- DOI：原文未提供
- 链接：https://users.cis.fiu.edu/~hex/CEN6075-11/PetriNets/CPN-Jensen.pdf
- 形式主义：Coloured Petri Nets
- 主类：🕸️
- 描述客体：🏭
- 所属领域：💻
- 论文角色：教程讲义
- 工具/实现获取方式：讲义直接以 tools 为重要主题，并给出相关下载页面线索。
- 标准/格式获取方式：原文没有给出统一标准文件格式。

## 简报

Coloured Petri Nets 的核心思想是把基础 Petri 网与编程语言式数据类型结合起来：控制、同步和资源共享仍由网结构表达，数据和值操作则由颜色集与函数式表达处理。这样可以用更少的结构表达更大的状态空间，同时保持仿真和状态空间验证能力。

- 形式主义定位：面向复杂数据驱动并发系统的高层 Petri 网。
- 构造方式简述：places/ transitions 保留，同时引入 colour sets、arc inscriptions、typed tokens 和函数式数据操作。
- 基础设施与场景简述：讲义明确把 tools、simulation、verification、analysis、practical use 放在主结构里，说明该形式主义高度依赖工具生态。

```text
并发数据流需求 -> 高层 Petri 网 + 颜色集 -> CPN 模型 -> 仿真/状态空间/不变量分析
```

## 形式主义定义与核心对象

### 定义对象

CPN 描述的是既有并发控制，又有显式数据对象和资源共享的系统。

### 核心抽象

基础网结构不变，但 token 不再是匿名黑点，而是带类型和值的 coloured tokens；弧和变迁可以带表达式、模式匹配和数据操作。

### 语义边界

它比基础 `P/T Net` 更适合数据丰富的系统，但也更依赖工具支持和类型系统。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 部分支持 | 仍以 marking 为状态，但 token 带类型和值。 |
| 事件 / 触发 | 支持 | 变迁触发。 |
| 守卫 / 数据 | 强支持 | colour sets、arc inscriptions、数据表达式是核心。 |
| 层次 | 部分支持 | 讲义涵盖 modules 扩展。 |
| 并发 / 同步 | 强支持 | 保留 Petri 网并发优势。 |
| 时间约束 | 部分支持 | 讲义指出可扩展到 time。 |
| 连续动态 / 随机性 | 不支持 | 非连续模型。 |
| 可执行 / 可验证性 | 强支持 | simulation、state spaces、place invariants 明确。 |

## 构造方式与承载格式

### 建模入口

先定义 colour sets 和 token 类型，再用网结构描述控制与资源流。

### 机器可处理承载方式

讲义展示的是工具驱动建模，不是统一标准 XML；机器可处理性主要来自 CPN 工具环境。

### 交换与互操作

原文未定义统一交换标准，生态更依赖专用工具链。

## 配套基础设施

- 建模/编辑工具：讲义明确列出 editing。
- 解析/交换/元模型支持：原文未说明统一标准交换格式。
- 仿真/执行支持：simulation 是核心能力。
- 验证/分析支持：state spaces、symmetries、equivalence classes、sweep-line、place invariants。
- 代码生成/转换支持：讲义提到 implementation，但未细化标准流程。
- 标准化或社区生态：Aarhus/CPN Tools 线是核心基础设施。

## 适用场景与需求前提

### 适用场景

适用于通信协议、分布式软件、资源共享系统和带显式数据对象的并发流程。

### 需求前提

1. 需求同时包含并发控制和结构化数据。
2. 需要通过 typed token 压缩模型规模。
3. 依赖仿真与状态空间分析工具。

### 不适用或高成本场景

若需求基本不含数据，仅是简单同步/资源关系，基础 P/T 网更轻量。

## 与相邻形式主义的关系

相对 `Petri Nets`，它显著增强数据表达；相对 `Time Petri Nets`，它更偏高层数据而非时间区间；相对 `UML/SCXML`，它更适合并发资源流而非通用对象建模标准。

## 与本研究的关系

### 对 Project 1 的价值

它表明当需求同时需要并发与数据操作时，单纯 `FSM` 或基础网模型都可能过弱。

### 作为目标形式主义还是中间表示

可作为高层并发数据模型的目标形式主义，也可作为复杂系统补充视图。

### 对需求到模型生成的启发

如果需求中有“消息载荷、资源类型、参数化对象”这类内容，生成带数据的高层网比匿名 token 网更合适。

### 现实限制

其工具链集中，标准化交换格式和跨工具互操作性不如 UML/SCXML。

## 重要的相关工作

### 奠基或前身工作

- 基础 Petri 网。

### 同类型或同家族工作

- Time extensions。
- Modules / hierarchy extensions。

### 标准 / 格式 / 工具链工作

- CPN Tools 生态。

### 与本研究关系最紧的工作

- 并发数据流系统的可执行建模与验证。

## 文献分类总结

- 主类：🕸️
- 描述客体：🏭
- 所属领域：💻
- 形式主义：Coloured Petri Nets
- 论文角色：教程讲义
- 核心功能：在 Petri 网中加入 typed token 与数据表达，建模数据丰富的并发系统。
- 关键特性：colour sets、arc inscriptions、simulation、state spaces、invariants。
- 构造方式：网结构 + 颜色集/数据表达式 + 专用工具环境。
- 基础设施：工具生态成熟，但缺统一交换标准。
- 适用场景：协议、分布式软件、资源共享与数据驱动并发流程。
- 需求前提：需求含显式数据对象与并发资源流。
- 状态：🟢
