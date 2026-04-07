# UML 状态机与协作图的模型检验和代码生成 / Model checking and code generation for UML state machines and collaborations

## 基本信息

- 标题：Model checking and code generation for UML state machines and collaborations
- 中文标题：UML 状态机与协作图的模型检验和代码生成
- 作者：Alexander Knapp，Stephan Merz
- 发表：*Proceedings of the 5th Workshop on Tools for System Design and Verification*，pp. 59-64，2002
- DOI：原文未提供
- 链接：https://opus.bibliothek.uni-augsburg.de/opus4/files/45281/45281.pdf
- 形式主义：`UML State Machines / UML Collaborations / HUGO / XMI-to-Java-PROMELA-UPPAAL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：early `HUGO` toolchain for UML state-machine verification and code generation
- 工具/实现获取方式：原文明确给出 `HUGO` 项目入口 `http://www.pst.informatik.uni-muenchen.de/projekte/hugo/`，并说明工具集包含 model-checking backend、code generation backend 与 `UPPAAL` timed-analysis backend；未给独立公开仓库。
- 标准/格式获取方式：输入承载是 off-the-shelf UML editor 导出的标准 `XMI`；输出承载包括 `Java` 运行时代码、`PROMELA/SPIN` 模型与 `UPPAAL` 模型。

## 简报

这篇论文补的是一条很早的 `UML -> backend/runtime` 集成工具线。它不是重新定义 UML 状态机，而是把同一个 UML 设计模型同时接到 model checking 和 code generation：一方面把 state machines 与 collaborations 编译到 `PROMELA/SPIN` 和 `UPPAAL`，另一方面把同一行为模型编译成 Java 运行时骨架。对文库来说，它是 `hugo/RT` 前史里的关键工具锚点。

- 形式主义定位：`UML State Machine` 的验证/执行工具链，而不是新的语言本体。
- 构造方式简述：`UML editor -> XMI -> HUGO -> Java runtime classes / PROMELA-SPIN / UPPAAL`。
- 基础设施与场景简述：依托 `XMI`、`HUGO`、generic Java runtime classes、observer automata、`SPIN` 与 `UPPAAL`，服务对象交互设计的一致性检查与可执行原型生成。

```text
UML state machines + collaborations -> XMI -> HUGO backends -> Java execution skeleton / SPIN checking / UPPAAL timed analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML State Machine`；
2. collaboration / sequence-style scenario；
3. active state configuration 与 event queue；
4. `HUGO` 生成的 Java runtime classes；
5. `PROMELA/SPIN` 与 `UPPAAL` backend。

### 核心抽象

论文把 UML 状态机当前配置描述成 active state configuration 加 event queue，可保守整理为：

$$
\sigma = (\mathrm{Conf}, Q)
$$

上式中的符号逐项解释如下：

1. `$\mathrm{Conf}$` 是当前 active state configuration。
2. `$Q$` 是该状态机尚未处理的事件队列。
3. `$\sigma$` 是 run-to-completion 语义下的离散运行状态。

围绕代码生成，原文强调 `HUGO` 提供一组通用 Java runtime classes，并为模型生成专用类。可保守写成：

$$
\mathrm{CodeGen}(U) = J_{rt} \cup J_U
$$

上式中的符号逐项解释如下：

1. `$U$` 是 UML 模型。
2. `$J_{rt}$` 是 `hugo.rt.java` 中的通用运行时类。
3. `$J_U$` 是为具体 UML 类、事件、guards 和 actions 生成的模型专用 Java 类。
4. 这说明 HUGO 的代码生成更像“运行时解释骨架 + 模型专用代码”。

围绕模型检验，论文描述的核心关系可压成：

$$
\mathrm{MC}(U,C) = M_{spin}(U) \parallel O(C)
$$

上式中的符号逐项解释如下：

1. `$U$` 是 UML state-machine view。
2. `$C$` 是 collaboration view。
3. `$M_{spin}(U)$` 是从 UML 状态机编译得到的 `PROMELA` / `SPIN` 模型。
4. `$O(C)$` 是由 collaboration 编译得到的 observer automaton。
5. 这是根据原文“state machine 当模型，collaboration 当属性”的描述做的保守整理。

### 一个最小例子与通俗解释

论文用 ATM 例子说明得很清楚：

1. `ATM` 和 `Bank` 都有 UML state machine。
2. collaboration 规定一条“输错 PIN 后重新输入”的期望交互，以及一条“不应在 abort 后仍接受 PIN”的错误交互。
3. `HUGO` 可以把状态机和 collaboration 同时编译出去，检查期望交互是否可实现、错误交互是否可达。
4. 同一个状态机模型也能生成 Java 代码骨架，作为 faithful prototype。

通俗地说，这条路线像“把 UML 图既当设计图，也当可检查、可跑的程序蓝图”，尽量避免设计语义和实现语义分裂成两套互不相认的东西。

### 运行 / 接受 / 转移语义

论文对 run-to-completion 步骤的描述可写成：

$$
(\mathrm{Conf}, Q) \xrightarrow{e} (\mathrm{Conf}', Q')
$$

其中：

1. `$e$` 是 dispatcher 从事件队列中取出的当前事件。
2. 先选择 maximal consistent set of enabled transitions。
3. 再执行 deactivation、actions 和 target-state activation。
4. 最后得到新的 active configuration `$\mathrm{Conf}'$` 与队列 `$Q'$`。

代码生成的运行语义还可进一步压成：

$$
\mathrm{Dispatch}(Q) \to \mathrm{Handle}_{top}(e) \to \mathrm{RTC\ completion}
$$

这不是原文正式公式，而是对其 Java runtime 结构的保守整理，强调：

1. 事件先被 event dispatcher 分发。
2. top state 递归向下处理事件。
3. completion events 优先于 ordinary events。

### 语义边界

1. 论文主体是早期工具原型，不是 UML 完整正式语义标准。
2. `HUGO` 的 code generation 偏 faithful interpretation，不追求 production-grade optimized code。
3. `SPIN` backend 和 `UPPAAL` backend 都只覆盖 UML 子集。
4. time 和 change events 在不同 backend 中的支持程度不一致。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| UML 运行配置 | `$\sigma = (\mathrm{Conf}, Q)$` | active states 和 event queue 是执行语义核心。 |
| Java 代码生成 | `$\mathrm{CodeGen}(U) = J_{rt} \cup J_U$` | `HUGO` 用通用运行时类加模型专用类承载 UML 行为。 |
| 模型检验关系 | `$\mathrm{MC}(U,C) = M_{spin}(U) \parallel O(C)$` | collaboration 被当作 property observer，state machine 被当作 model。 |
| RTC 步 | `$(\mathrm{Conf}, Q) \xrightarrow{e} (\mathrm{Conf}', Q')$` | 论文执行语义围绕 event queue 与 RTC。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 `UML State Machines`。 |
| 事件 / 触发 | 很强 | event queue、dispatch、completion event 都是主线。 |
| 守卫 / 数据 | 中等支持 | 支持 guards 和 Java-style actions，但主体更关注 control part。 |
| 层次 | 中等支持 | 处理 UML hierarchy、orthogonal regions 和 pseudo-states。 |
| 并发 / 同步 | 中等支持 | 对象交互与 orthogonal regions 都被纳入。 |
| 时间约束 | 中等支持 | 通过 `UPPAAL` backend 支持 time events 分析。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散对象行为。 |
| 可执行 / 可验证性 | 很强 | 同一模型可接 Java runtime、`SPIN` 与 `UPPAAL`。 |

### 形式化问题与性质

1. 论文补出的关键不是单个算法，而是“同一个 UML 模型如何同时连到验证和执行”。
2. collaboration 被编成 observer automata，这一点对后续场景/性质自动生成很有启发。
3. `XMI` 作为统一输入前端，使它具备了较早期的跨工具互操作味道。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. off-the-shelf UML editor 中建好的 class diagram、state machines 与 collaborations。
2. 导出的标准 `XMI`。
3. `HUGO` 对 `XMI` 的解析和后端生成。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XMI` 输入模型；
2. `Java` runtime classes；
3. `PROMELA` / `SPIN` 模型；
4. `UPPAAL` 模型；
5. counterexample 与 diagnostic trace。

### 交换与互操作

这篇论文的互操作重点非常清楚：

1. `XMI` 是统一前端。
2. 同一 UML 模型既能去 `SPIN` 也能去 `UPPAAL`。
3. 同一 UML 模型还能落成 Java prototype。

## 配套基础设施

- 建模/编辑工具：off-the-shelf UML editors。
- 解析/交换/元模型支持：标准 `XMI` 输入。
- 仿真/执行支持：`hugo.rt.java` 通用运行时类与模型专用 Java 类。
- 验证/分析支持：`PROMELA/SPIN` backend、observer automata、`UPPAAL` backend。
- 代码生成/转换支持：面向 Java 的 faithful code generation。
- 标准化或社区生态：依托 UML、`XMI`、`SPIN`、`UPPAAL` 的现成生态；`HUGO` 是其桥接工具。

## 适用场景与需求前提

### 适用场景

适合对象交互较强、已使用 UML 做设计、同时又希望把场景一致性检查和可执行原型都建立在同一模型上的软件建模流程。

### 需求前提

1. 行为逻辑已落成 `UML State Machine`。
2. 关键正确性要求能写成 collaboration / interaction 场景。
3. 团队接受 `XMI` 作为统一模型输入。
4. 所需特性必须落在 `HUGO` 支持的 UML 子集内。

### 不适用或高成本场景

若需求重在连续动力学、复杂多实例对象系统，或必须使用 UML 的大量高级特性，这条早期 `HUGO` 路线会很快变重。

## 与相邻形式主义的关系

相对 [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md)，那篇是 `hugo/RT` timed verification 分支，本文是更早的 `HUGO` 总体工具链；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，本文走的是 `XMI -> Java/SPIN/UPPAAL`，后者则是 `XMI -> interpreter runtime`；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，本文的特点是同时把 model checking 和 code generation 并到一个工具线里。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 UML 状态机在很早期就已经有“同一模型同时做验证和执行”的工具愿景。
2. 对后续 LLM 生成状态机而言，这意味着目标输出不一定非得是某个纯验证后端，也可以是更接近工程设计环境的统一前端。
3. collaboration 被当作 property/observer 的做法，对 `project_2` 的场景与性质生成也有启发。

### 局限

1. 这是早期 workshop tool paper，支持特性有限。
2. Java code generation 更像 faithful prototype，而不是工业级最终代码生成链。

## 重要的相关工作

1. [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md)：`hugo/RT` timed verification 分支。
2. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：更晚的 UML 解释执行路线。
3. [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：另一条 `UML -> verifier` 自动桥接路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machines / UML Collaborations / HUGO / XMI-to-Java-PROMELA-UPPAAL`
- 论文角色：early `HUGO` toolchain for UML state-machine verification and code generation
- 归类理由：论文主体是 `HUGO` 工具链、`XMI` 输入、backend bridge 和 runtime/code generation，不是在重讲 UML 语言本体，因此应归入基础设施条目。
