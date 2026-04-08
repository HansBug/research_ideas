# 一个可模型检验的 UML 足球机器人 / A Model Checkable UML Soccer Player

## 基本信息

- 标题：A Model Checkable UML Soccer Player
- 中文标题：一个可模型检验的 UML 足球机器人
- 作者：Valentin Besnard，Ciprian Teodorov，Frédéric Jouault，Matthias Brun，Philippe Dhaussy
- 发表：*2019 ACM/IEEE 22nd International Conference on Model Driven Engineering Languages and Systems Companion (MODELS-C)*，pp. 211-220，2019
- DOI：`10.1109/MODELS-C.2019.00035`
- 链接：https://doi.org/10.1109/MODELS-C.2019.00035
- 形式主义：`UML State Machine / EMI / OBP2 / observer automata`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：EMI-based design-verify-execute workflow for executable UML models
- 工具/实现获取方式：论文明确给出 `EMI` 页面 `https://plug-obp.github.io/bare-metal-uml/`、`OBP2` 页面 `https://plug-obp.github.io/`，并给出挑战代码仓库 `https://github.com/ValentinBesnard/mdetools19-emi`。
- 标准/格式获取方式：核心承载对象是 `UML` 类图、复合结构图、状态机、`EMI` 解释器接口、`OBP2` 验证接口和 UML observer automata；它不是独立交换标准。

## 简报

这篇论文的关键点，是把一套具体的 `UML` 机器人控制模型放到“同一语义定义同时服务设计、验证和执行”这条路线里做完整闭环，而不是只演示其中某一段。作者用 `EMI` 解释器统一执行 `UML` 模型，再把 `OBP2` 接到同一运行语义上做 simulation 和 `LTL` model checking，同时把 observer automata 部署到实际执行阶段做 runtime monitoring，最后还通过真实 `TCP` 连接把模型接到足球仿真器。

- 形式主义定位：围绕 `EMI` 的 executable-`UML` 验证与执行方法路线，而不是新的 `UML` 语义母型。
- 构造方式简述：`UML model + abstract environment -> EMI operational semantics -> OBP2 simulation / LTL model checking -> observer automata runtime monitoring -> concrete TCP deployment`。
- 基础设施与场景简述：依托 `EMI`、`OBP2`、observer automata 和 `TCP` 接口，服务嵌入式或机器人控制类 UML 模型的设计期验证与执行期落地。

```text
UML design model -> EMI single semantics -> OBP2 simulation / LTL verification -> observer automata monitoring -> TCP-connected execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 可执行 `UML` 模型；
2. `EMI` 统一解释器；
3. `OBP2` model checker；
4. abstract environment 与 concrete environment；
5. UML observer automata。

### 核心抽象

论文使用的可执行 UML 模型仍然沿用类图、复合结构图与状态机的组合骨架，可保守写成：

$$
U = (CD, SM, CSD)
$$

上式中的符号逐项解释如下：

1. `CD` 是类图。
2. `SM` 是控制器、轨迹管理器、环境等对象的状态机集合。
3. `CSD` 是组件和连接关系的复合结构图。
4. 论文明确说明 `EMI` 支持的正是这套 UML 子集。

`EMI` 运行时维护的配置可保守整理为：

$$
\sigma = (C, P, A)
$$

上式中的符号逐项解释如下：

1. `C` 是各对象当前控制状态。
2. `P` 是消息、输入与事件池。
3. `A` 是属性和内部变量赋值。
4. 论文强调 simulation、model checking 和 execution 都共享这套 operational semantics。

论文中的一步执行可保守写成：

$$
(U, \sigma) \xrightarrow{t} (U, \sigma')
$$

上式中的符号逐项解释如下：

1. `t` 是当前某个可触发转移。
2. `\sigma` 是执行前配置。
3. `\sigma'` 是执行后的新配置。
4. `OBP2` 正是通过控制解释器、复用这套一步语义来做仿真与验证。

运行时监测则可以保守概括成 UML 观察者和主模型的同步运行：

$$
\gamma = (\sigma, q_O)
$$

上式中的符号逐项解释如下：

1. `\sigma` 是主模型当前配置。
2. `q_O` 是 observer automaton 当前状态。
3. 当 observer 进入 failure 状态时，就说明运行时检测到安全性质失效。

### 一个最小例子与通俗解释

论文围绕机器人足球 challenge 建模：

1. 一个状态机负责球员控制逻辑。
2. 一个状态机负责轨迹管理。
3. abstract environment 用于设计期验证。
4. concrete environment 用于通过真实 `TCP` 连接接入足球仿真器。
5. 若某些安全性质需要执行期守护，则额外设计 observer automata。

通俗地说，这条路线不像传统“先画 UML，再另写一份验证模型，再生成一份执行代码”，而是尽量让同一个 UML 模型贯穿设计、验证和执行三段流程。

### 运行 / 接受 / 转移语义

论文强调 `OBP2` 是通过 `EMI` 暴露的统一接口工作，可保守压成：

$$
\mathrm{GetFireableTransitions}(U, \sigma) = \{ t \mid enabled(t, \sigma) \}
$$

以及：

$$
\mathrm{FireTransition}(U, \sigma, t) = (U, \sigma')
$$

上式中的符号逐项解释如下：

1. `GetFireableTransitions` 让分析器查询当前可执行转移。
2. `FireTransition` 让分析器沿相同 operational semantics 前进一步。
3. 这正是“what is verified is what is executed”的基础。

运行时 observer 则可以保守写成：

$$
(\sigma, q_O) \xrightarrow{t} (\sigma', q_O')
$$

其中 `q_O'` 由当前事件、守卫结果与 observer 转移共同确定。

### 语义边界

1. 论文聚焦 `EMI` 支持的 UML 子集，不覆盖完整 UML 全语义。
2. `EMI` 不支持文中作者希望使用的一些特性，例如更丰富的层次状态或线程式 TCP 监听。
3. 案例重点是说明单一语义闭环可行，不是讨论最优机器人策略。
4. 时间约束不是这篇论文的核心主线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 可执行 UML 模型骨架 | `$U = (CD, SM, CSD)$` | `EMI` 解释器消费的 UML 结构。 |
| 运行时配置 | `$\sigma = (C, P, A)$` | 设计、验证、执行共享的核心运行时对象。 |
| 一步执行 | `$(U, \sigma) \xrightarrow{t} (U, \sigma')$` | `OBP2` 和实际执行复用同一 operational semantics。 |
| 观察者联合状态 | `$\gamma = (\sigma, q_O)$` | runtime monitoring 由 UML observer automata 与主模型联合推进。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 机器人控制逻辑直接以 UML 状态机表达。 |
| 事件 / 触发 | 很强 | referee/player 消息、仿真输入和内部事件都是核心。 |
| 守卫 / 数据 | 强支持 | 动作、守卫与变量都在解释执行语义中保留。 |
| 层次 | 中等支持 | 使用 UML 状态机，但受 `EMI` 子集约束。 |
| 并发 / 同步 | 中等支持 | 多组件协作通过结构图和事件交互组织。 |
| 时间约束 | 弱支持 | 本文主要不是 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 足球物理由外部模拟器承担，模型本身是离散控制逻辑。 |
| 可执行 / 可验证性 | 很强 | simulation、`LTL` checking、runtime monitoring 和实际执行都已打通。 |

### 形式化问题与性质

1. 这篇论文真正补的是“单一 operational semantics 支撑 design-verify-execute 闭环”的可操作证据。
2. observer automata 让一部分安全性质不只停在设计期模型检查，还能落到执行期守护。
3. 对 `state_machine_types` 文库而言，它比单纯的解释器论文更偏具体方法流程，因此更适合归到 `🛠️`。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 用 UML 建结构和状态机；
2. 针对验证目的建立 abstract environment；
3. 用 `OBP2` 复用 `EMI` 语义做仿真和 `LTL` 检查；
4. 用 observer automata 部署 runtime monitoring；
5. 用 concrete environment 和 `TCP` 接口连接真实仿真器或目标系统。

### 机器可处理承载方式

机器可处理承载方式包括：

1. UML 类图、复合结构图和状态机；
2. `EMI` 解释器 API；
3. `OBP2` 的仿真与显式状态探索；
4. `LTL` 性质；
5. UML observer automata；
6. `TCP` 连接适配层。

### 交换与互操作

这篇论文的互操作重点在：

1. `OBP2` 不重新解释 UML，而是复用 `EMI` 语义；
2. observer automata 在设计期和执行期都能复用；
3. 通过替换 abstract / concrete environment，可以在同一模型上切换验证和部署。

## 配套基础设施

- 建模/编辑工具：UML 建模环境与 `EMI`。
- 解析/交换/元模型支持：`EMI` 支持的 UML 子集、模型解释接口与环境替换机制。
- 仿真/执行支持：`EMI` 可在 host/embedded target 上执行模型。
- 验证/分析支持：`OBP2` simulation、显式状态模型检查、`LTL` 性质验证与 observer runtime monitoring。
- 代码生成/转换支持：论文重点不是代码生成，而是统一解释执行与外部接口连接。
- 标准化或社区生态：依附 `EMI`、`OBP2` 与 executable-`UML` 研究路线；原文未给中立交换标准。

## 适用场景与需求前提

### 适用场景

适合需要在设计期验证后继续执行同一 UML 模型的嵌入式控制、机器人逻辑和协议式反应系统。

### 需求前提

1. 模型能落到 `EMI` 支持的 UML 子集。
2. 团队认可解释执行而不是完全依赖代码生成。
3. 性质能表达成 `LTL` 或 observer automata。
4. 环境行为可以分别抽象成验证环境和执行环境。

### 不适用或高成本场景

若系统严重依赖完整 UML 高级特性、复杂并发运行时或高精度时间语义，这条路线会遇到 `EMI` 子集边界。

## 与相邻形式主义的关系

相对 [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)，本文更像该统一解释器思路在具体机器人控制 challenge 上的完整落地；相对 [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)，本文多了 `OBP2`、observer automata 和真实 `TCP` 接入这三段工程闭环；相对 [formal-verification-and-validation-of-run-to-completion-style-state-charts-using-event-b/desc.md](../formal-verification-and-validation-of-run-to-completion-style-state-charts-using-event-b/desc.md)，那篇是 `Event-B` 验证桥，这篇则是解释器级的执行-验证同语义路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为 `project_1` 提供了一个很直接的例子：生成出来的 UML 状态机若想进入高可信流程，最好同时准备设计期验证和执行期监测入口。
2. abstract environment / concrete environment 的拆分，对“生成-验证-修复”闭环尤其有启发。
3. 单一语义闭环能显著降低“验证的是不是最终要跑的东西”这类追溯风险。

### 作为目标形式主义还是中间表示

更像 executable-`UML` 的验证与执行工作流，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 生成状态机时应尽可能保留可解释执行的结构，而不是只追求静态图形好看。
2. 性质既可以写成离线验证公式，也可以编译成 observer automata 进入执行期。
3. 若未来接入 LLM 生成 UML 模型，统一解释语义会极大简化调试和修复闭环。

## 重要的相关工作

- [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)：统一解释器与 `LTL` 验证主线。
- [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)：统一设计与部署语义的更早期骨架。
- [practical-multiverse-debugging-through-user-defined-reductions-application-to-uml-models/desc.md](../practical-multiverse-debugging-through-user-defined-reductions-application-to-uml-models/desc.md)：同属 executable-`UML` 工具线，但更偏调试与搜索缩减。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / EMI / OBP2 / observer automata`
- 论文角色：EMI-based design-verify-execute workflow for executable UML models
- 归类理由：论文主体是利用 `EMI + OBP2 + observer automata` 把 UML 设计模型、形式验证和执行闭环打通，因此更适合作为 executable-`UML` 方法路线条目，而不是单纯的机器人应用案例。
