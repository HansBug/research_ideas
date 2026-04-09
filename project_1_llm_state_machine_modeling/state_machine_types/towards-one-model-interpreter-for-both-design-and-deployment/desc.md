# 面向设计与部署统一语义的模型解释器 / Towards One Model Interpreter for Both Design and Deployment

## 基本信息

- 标题：Towards One Model Interpreter for Both Design and Deployment
- 中文标题：面向设计与部署统一语义的模型解释器
- 作者：Valentin Besnard，Matthias Brun，Philippe Dhaussy，Frédéric Jouault，David Olivier，Ciprian Teodorov
- 发表：*Proceedings of the EXE 2017 Workshop*，pp. 102-108，2017
- DOI：原文未提供
- 链接：https://ceur-ws.org/Vol-2019/exe_4.pdf
- 形式主义：`tUML / UML State Machine / bare-metal model interpreter`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：design-deployment unified model interpreter / remote diagnosis interface
- 工具/实现获取方式：原文说明解释器以 `C` 实现，可部署在 PC、`at91sam7s` 与 `stm32` bare-metal 目标上，并通过远程接口接入模拟器与诊断工具；正文未给独立公开仓库。
- 标准/格式获取方式：原文明确强调 `tUML` 模型、`XMI` 导出、`C struct initializers` 序列化与解释器通信 API；它不是独立标准语言，而是 `tUML/UML` 的执行载体。

## 简报

这篇论文的关键动作，是试图消掉“设计模型一套语义、验证模型一套语义、部署代码又一套语义”这三重语义鸿沟。作者提出一个 bare-metal UML 解释器，让同一份 `tUML` 模型在设计阶段和部署阶段都由同一执行核心解释，并通过远程 API 把运行时 configuration 暴露给 simulator、debugger 或 model checker。

- 形式主义定位：`UML State Machine` 与 `tUML` 的执行载体，不是新的状态机母型。
- 构造方式简述：`tUML` 的类图、状态机和 composite structure model 被序列化到 `C` 静态数据，再由解释器在 PC 或微控制器上运行。
- 基础设施与场景简述：依托 bare-metal interpreter、配置读写接口和可触发转移接口，服务设计期仿真、运行期诊断和部署后一致语义执行。

```text
tUML model -> XMI / serialized C data -> unified interpreter -> configuration API -> simulation / debugging / deployment
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织解释执行链：

1. `tUML` 模型。
2. class diagram、state machines、composite structure diagram 三视图。
3. 解释器中的 `ActiveObject`、`EventPool`、`Store` 和 `GuardEval`。
4. current configuration 与 fireable transitions。
5. 远程通信 API。

### 核心抽象

论文明确说明可执行模型由三种 UML 视图共同定义。可保守写成：

$$
U = (CD, SM, CSD)
$$

上式中的符号逐项解释如下：

1. `CD` 是 class diagram。
2. `SM` 是各 active objects 的 state machines。
3. `CSD` 是 composite structure diagram。
4. 论文说明这三者共同构成 `tUML` 的可执行模型骨架。

解释器运行时维护的 configuration 可整理为：

$$
\sigma = (C, P, A)
$$

上式中的符号逐项解释如下：

1. `C` 是各 `ActiveObject` 当前所处状态。
2. `P` 是事件池内容。
3. `A` 是属性存储区中的当前值。
4. 这是论文对 current state、event pool 和 store 的直接抽象。

解释器的状态迁移可保守写成：

$$
(U,\sigma) \xrightarrow{t} (U,\sigma')
$$

其中：

1. `t` 是某个 `ActiveObject` 上当前可触发的 transition。
2. 触发 `t` 时会消费 trigger event、更新当前状态并执行 effect。
3. `\sigma'` 是执行后的新 configuration。

### 一个最小例子与通俗解释

论文用铁路平交道口系统举例：

1. `Controller`、`Train`、`TrackCircuit`、`Gate` 和 `RoadSign` 都是 active objects。
2. 每个对象都有自己的状态机。
3. 解释器在运行时维护每个对象当前状态、事件池和属性值。
4. 远程工具可以读取 configuration、列出当前 fireable transitions，甚至回退到旧 configuration。

通俗地说，这套方案像“把 UML 模型本身当作程序来跑”，而不是先把它翻译成另一套难以映射回 UML 元素的代码。

### 运行 / 接受 / 转移语义

论文给出的远程接口可以压成四个基本操作：

$$
\mathrm{GetConfiguration}(U,\sigma) = \sigma
$$

$$
\mathrm{SetConfiguration}(U,\sigma,\hat{\sigma}) = (U,\hat{\sigma})
$$

$$
\mathrm{GetFireableTransitions}(U,\sigma) = \{ t \mid enabled(t,\sigma) \}
$$

$$
\mathrm{FireTransition}(U,\sigma,t) = (U,\sigma')
$$

上式中的符号逐项解释如下：

1. `GetConfiguration` 读取当前运行时快照。
2. `SetConfiguration` 支持把解释器放回任意配置，用于回退或探索。
3. `GetFireableTransitions` 返回当前可触发的转移集合。
4. `FireTransition` 触发指定转移并更新配置。

论文强调 back-in-time execution 的关键就在于 `SetConfiguration` 的存在。这意味着：

$$
\exists\ \sigma_i,\sigma_j \quad \mathrm{s.t.}\quad \sigma_j \to \sigma_i
$$

这里的含义是：

1. 运行时不只是单向前进。
2. 通过重新装载旧 configuration，可以回到先前状态。
3. 这为 debugging 和 state-space exploration 提供了直接支撑。

### 语义边界

这篇论文的边界主要有：

1. 它依赖 `tUML` 这个 UML 子集，而不是完整 UML 所有特性。
2. guards/effects 当前仍通过简化版 `ABCD` 语言与 `C` 实现承载。
3. 论文展示的是 prototype 级解释器，不是工业强度完整运行时。
4. 重点是统一语义与诊断接口，不是高性能代码生成。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 可执行模型骨架 | `$U = (CD, SM, CSD)$` | `tUML` 可执行模型由三视图共同定义。 |
| 运行时配置 | `$\sigma = (C, P, A)$` | 当前状态、事件池与属性值是一等运行时数据。 |
| 解释执行步 | `$(U,\sigma) \xrightarrow{t} (U,\sigma')$` | 统一解释器在单一语义下推进模型。 |
| 远程诊断接口 | `$\mathrm{GetConfiguration}$`、`$\mathrm{SetConfiguration}$`、`$\mathrm{GetFireableTransitions}$`、`$\mathrm{FireTransition}$` | simulator/debugger/model checker 接入的核心协议。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 UML state machines 运行。 |
| 事件 / 触发 | 很强 | 事件池和 trigger 是执行核心。 |
| 守卫 / 数据 | 强支持 | 通过 `Store` 与 guard/effect 解释执行。 |
| 层次 | 中等支持 | 依赖 UML 状态机子集，但论文重点不在扩展层次语义。 |
| 并发 / 同步 | 中等支持 | 多个 `ActiveObject` 通过事件交互。 |
| 时间约束 | 弱支持 | 主线不是 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 聚焦离散 UML 行为执行。 |
| 可执行 / 可验证性 | 很强 | 设计期和部署期共用解释器语义，且能接入诊断工具。 |

### 形式化问题与性质

1. 论文真正解决的是“单一语义定义如何同时服务设计与部署”。
2. 远程 configuration API 让 diagnosis tools 可以共享解释器语义，而不是重复实现一份近似语义。
3. 这比单纯代码生成更贴近“模型始终可被追踪和操控”的目标。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 `tUML` 建 class diagram。
2. 为 active objects 编写 state machines。
3. 用 composite structure diagram 组织对象连接关系。
4. 将模型序列化为 `C` 数据并交给解释器。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `tUML` 模型；
2. `XMI` 导出；
3. `C struct initializers` 形式的静态模型；
4. configuration 消息与远程控制接口。

### 交换与互操作

这篇论文的互操作重点在于：

1. 设计模型与部署模型不再通过语义改写式转换桥接。
2. 诊断工具通过统一 API 而不是各自单独解释模型。
3. 这为后续接入 simulator、debugger、model checker 留出稳定接口。

## 配套基础设施

- 建模/编辑工具：`tUML` / UML 建模环境。
- 解析/交换/元模型支持：`XMI` 导出与 `C` 序列化加载。
- 仿真/执行支持：PC 与 bare-metal 微控制器上的统一解释执行。
- 验证/分析支持：配置读取、可触发转移查询、回退式执行与外部诊断工具对接。
- 代码生成/转换支持：重点不是代码生成，而是模型序列化与解释运行。
- 标准化或社区生态：依托 UML/tUML 生态与 TCP/串口远程连接机制。

## 适用场景与需求前提

### 适用场景

适合希望在设计阶段和部署阶段保持统一语义，并且希望在运行中仍以模型元素为诊断对象的嵌入式建模场景。

### 需求前提

1. 行为逻辑已经稳定落到 `tUML/UML` 状态机子集。
2. 团队接受解释执行而非纯代码生成。
3. 目标平台允许承载 interpreter 的资源开销。
4. 诊断、回退和运行时可追踪性被视为重要需求。

### 不适用或高成本场景

如果目标是极致性能优化、复杂连续控制或完整 UML 全语义执行，这条 bare-metal interpreter 路线会比较受限。

## 与相邻形式主义的关系

相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，本文更早、更偏统一语义与配置 API 母线；相对 [enhanced-code-generation-from-uml-composite-state-machines/desc.md](../enhanced-code-generation-from-uml-composite-state-machines/desc.md)，后者走代码生成路线，而本文坚持解释执行；相对 [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)，两者都在补 UML 执行链，但本文强调 design/deployment 共用同一解释器。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明“状态机模型可直接进入部署阶段”并非只能靠代码生成。
2. 如果 `project_1` 未来想做生成后的在线调试、回放或修复，configuration 级 API 很值得借鉴。
3. 统一语义对闭环研究尤其关键，因为它减少了“生成模型”和“运行时工件”之间的语义漂移。

### 作为目标形式主义还是中间表示

它更像 `UML/tUML` 的执行载体和部署桥梁，而不是新的前端形式主义。

## 重要的相关工作

- [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：这一条线的后续嵌入式执行扩展。
- [enhanced-code-generation-from-uml-composite-state-machines/desc.md](../enhanced-code-generation-from-uml-composite-state-machines/desc.md)：统一模型执行与代码生成路线的对照条目。
- [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)：另一条 UML 执行/验证后端。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`tUML / UML State Machine / bare-metal model interpreter`
- 论文角色：design-deployment unified model interpreter / remote diagnosis interface
- 核心功能：以统一解释器语义贯通设计期仿真与部署期执行
- 关键特性：configuration API、fireable-transition API、back-in-time execution、bare-metal deployment
- 构造方式：`tUML` 三视图模型 -> 序列化 `C` 数据 -> unified interpreter
- 基础设施：interpreter、event pool、store、guard/effect evaluation、remote diagnosis protocol
- 适用场景：需要统一设计与部署语义的嵌入式 UML 执行链
- 需求前提：模型需落在 `tUML/UML` 可执行子集且目标平台可承载解释器
- 状态：🟢
