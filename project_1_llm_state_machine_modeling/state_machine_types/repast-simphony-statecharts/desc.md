# Repast Simphony 状态图 / Repast Simphony Statecharts

## 基本信息

- 标题：Repast Simphony Statecharts
- 中文标题：Repast Simphony 状态图
- 作者：Jonathan Ozik，Nicholson Collier，Todd Combs，Charles M. Macal，Michael North
- 发表：*Journal of Artificial Societies and Social Simulation*，18(3)，2015
- DOI：`10.18564/jasss.2840`
- 链接：https://doi.org/10.18564/jasss.2840
- 形式主义：`Statecharts / Repast Simphony`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：statechart editor / code-generation / runtime-visualization framework
- 工具/实现获取方式：原文说明状态图能力作为 `Repast Simphony` 的一部分随发行包提供，源码位于其开源分发中。
- 标准/格式获取方式：承载方式是 `Eclipse` 插件、`GMF/EMF` metamodel、statechart diagram serialization、`Xpand` code generation 与 runtime interaction panel；无中立交换标准。

## 简报

这篇论文的核心贡献，是把 agent-based social simulation 里常见的“自己手写状态逻辑”替换成一套图形化 statecharts 框架，并把 metamodel、editor、代码生成、runtime visualization 和手动交互全部接入 `Repast Simphony`。它不是在 statechart 理论上再前进一步，而是把一个 `Harel statecharts` 子集做成 agent-based modeling 语境下可直接使用的基础设施。

- 形式主义定位：statechart-based agent behavior infrastructure，而不是新的状态机家族。
- 构造方式简述：用户在 Eclipse editor 中编辑 statechart diagram，底层 `GMF/EMF` 维护 metamodel 实例，再由 `Xpand` 生成 Java builder code，最终创建运行时 statechart。
- 基础设施与场景简述：依托图形 editor、code editor、metamodel serialization、code generation 和 runtime panel，为 `Repast Simphony` / `ReLogo` 中的 agent 提供显式状态逻辑。

```text
statechart diagram -> EMF/GMF metamodel instance -> Xpand builder code -> runtime statechart -> simulation-time visualisation and interaction
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象定义 `Repast Simphony statecharts`：

1. state、composite state、final state。
2. entry/initial/deep history/shallow history/branching pseudo-states。
3. transitions 与多种 trigger types。
4. `StateMachine` 根对象及其 metamodel。
5. `Xpand` 生成的 builder code 与 runtime panel。

### 核心抽象

结合论文给出的 metamodel，可把其 statechart 骨架保守整理为：

$$
\mathcal{S}_{RS} = (Q, P, T, \Theta, B)
$$

上式中的符号逐项解释如下：

1. `Q` 是普通 states 集合。
2. `P` 是 pseudo-states 集合。
3. `T` 是 transitions 集合。
4. `\Theta` 是 transition triggers 集合。
5. `B` 是 state entry/exit/on-transition code blocks 与相关行为片段。

论文明确说明 metamodel 的根对象是：

$$
StateMachine \supseteq \{ AbstractState, Transition \}
$$

上式中的符号逐项解释如下：

1. `StateMachine` 是 diagram/model 的根对象。
2. `AbstractState` 是普通状态与复合状态等的抽象基类。
3. `Transition` 连接 states/pseudo-states，并持有 trigger 与 behavior 信息。

代码生成链可保守写成：

$$
\mathrm{Gen}_{Xpand} : Inst(MetaModel) \to JavaBuilder
$$

上式中的符号逐项解释如下：

1. `Inst(MetaModel)` 是用户在 editor 中创建的 metamodel 实例。
2. `JavaBuilder` 是生成出来、用于构造 runtime statechart 的 Java builder source。
3. 论文强调生成结果不是 runtime statechart 本体，而是创建 runtime statechart 的 builder code。

### 一个最小例子与通俗解释

论文的 CA-MRSA 案例很适合做直觉说明：

1. 模型里有一个 global activities statechart 协调 daily schedule。
2. 每个 agent 还有自己的 disease progression statechart。
3. 某些转移用 timed trigger，某些用 condition 或 message trigger。
4. 模型运行时，用户可以直接在 panel 上看到当前 active states，甚至手动激活状态或强制 transition。

通俗地说，`Repast Simphony Statecharts` 像“给 agent-based model 装了一套可视化状态机 IDE”，既能画图，又能生成代码，还能在仿真跑着的时候直接看和点。

### 运行 / 接受 / 转移语义

论文列出的 triggers 可保守抽象为：

$$
\Theta = \{ always, timed, probability, condition, decay, message \}
$$

上式中的符号逐项解释如下：

1. `always` 表示总是可触发。
2. `timed` 表示到时触发。
3. `probability` 表示按给定概率触发。
4. `condition` 表示条件表达式为真时触发。
5. `decay` 表示按指数衰减率触发。
6. `message` 表示满足消息条件时触发。

在运行时，某个 transition 的使能可保守写成：

$$
enabled(t,\alpha,\mu,\tau) \iff source(t)\subseteq \alpha \land trig_t(\mu,\tau)=true
$$

上式中的符号逐项解释如下：

1. `\alpha` 是当前 active-state configuration。
2. `\mu` 是可用消息或环境输入。
3. `\tau` 是当前仿真时间或相关时间上下文。
4. `trig_t` 对应 transition `t` 的 trigger 逻辑。

若从工具链角度描述运行时生成，可写成：

$$
\mathrm{Run}(JavaBuilder, agent) \to Statechart_{runtime}
$$

其中：

1. `JavaBuilder` 由 `Xpand` 生成。
2. 每个 agent 在运行时可实例化自己的 statechart。
3. runtime panel 再把 `Statechart_{runtime}` 的 active states 投影回图上。

### 语义边界

这篇论文的边界也非常清楚：

1. 它只实现 `Harel statecharts` 的一个子集。
2. 强能力高度依赖 `Repast Simphony` / Java / Eclipse 生态。
3. 工具关注 agent behavior engineering，不是通用形式验证平台。
4. 图形 editor、builder code 和 runtime engine 之间的一致性由工具链维护，而不是由独立标准规定。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| statechart 骨架 | `$\mathcal{S}_{RS} = (Q, P, T, \Theta, B)$` | 描述了状态、伪状态、迁移、触发器和代码块的整体结构。 |
| metamodel 根对象 | `$StateMachine \supseteq \{ AbstractState, Transition \}$` | 图形 editor 与持久化都围绕这个 metamodel 根对象展开。 |
| trigger 集合 | `$\Theta = \{ always, timed, probability, condition, decay, message \}$` | 说明其运行时不是只支持单一 event trigger。 |
| transition 使能 | `$enabled(t,\alpha,\mu,\tau) \iff source(t)\subseteq \alpha \land trig_t(\mu,\tau)=true$` | 当前活动状态和 trigger 条件共同决定转移。 |
| 代码生成 | `$\mathrm{Gen}_{Xpand} : Inst(MetaModel) \to JavaBuilder$` | 图形模型可被自动转为可运行 builder code。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | simple/composite/final states 与多种 pseudo-states 都支持。 |
| 事件 / 触发 | 很强 | timed、probability、condition、message 等 trigger 类型很丰富。 |
| 守卫 / 数据 | 强支持 | 通过 condition code、on-transition code 和 state code 承载。 |
| 层次 | 很强 | composite state、deep/shallow history 明确支持。 |
| 并发 / 同步 | 弱到中 | 重点在 agent state logic，而非复杂并发同步代数。 |
| 时间约束 | 中等支持 | timed triggers 明确存在，但主体不是 timed-automata 理论。 |
| 连续动态 / 随机性 | 部分支持 | probability / decay triggers 可表达部分随机化逻辑，但无连续动力学。 |
| 可执行 / 可验证性 | 很强 | 代码生成、运行时高亮、手动激活和强制转移都已打通。 |

### 形式化问题与性质

1. `Repast Simphony Statecharts` 的亮点，是把 diagram、code 和 runtime observation 绑定到一起。
2. `GMF/EMF + Xpand` 的链路说明它是一套真正的 metamodel-driven infrastructure，而不是简单的画图插件。
3. runtime panel 能直接操控 statechart，是它区别于很多“只生成代码不回显运行态”的工具的关键点。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 在 Eclipse 内的 graphical editor 中创建 statechart diagram。
2. 通过 properties/code editor 编写状态和转移逻辑。
3. 保存 diagram，序列化 metamodel 实例。
4. 由 `Xpand` 生成 Java builder code，并编译进模型运行环境。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `GMF/EMF` metamodel instances。
2. `StateMachine`、`AbstractState`、`Transition` 等持久化对象。
3. `Xpand` 生成的 Java builder source。
4. runtime statechart engine 与 panel snapshot/image。

### 交换与互操作

这篇论文的互操作重点在 `Repast Simphony` 内部：

1. statecharts 可与 Java、Groovy、`ReLogo` 行为定义并存。
2. `ReLogo` 的 `Patch/Link/Observer/Turtle` 都可拥有 statecharts-mediated behaviours。
3. 图形 editor、生成代码与 runtime panel 共用同一 metamodel。

## 配套基础设施

- 建模/编辑工具：Eclipse plugin、graphical editor、code editor、validation code。
- 解析/交换/元模型支持：`GMF/EMF` metamodel 与 serialization。
- 仿真/执行支持：runtime statechart engine、active-state visualisation、manual activation/forced transitions。
- 验证/分析支持：coherence checking、warnings/errors、runtime probing；不是通用 model checker。
- 代码生成/转换支持：`Xpand` 生成 Java builder code，并编译进 `Repast Simphony`。
- 标准化或社区生态：`Repast Simphony` 开源分发、`ReLogo` 集成和 Eclipse/Java 生态。

## 适用场景与需求前提

### 适用场景

适合 agent-based social simulation、agent-oriented建模教学，以及需要显式状态逻辑和运行时可视化的 `Repast Simphony` 模型开发。

### 需求前提

1. agent behavior 适合被拆成显式状态和转移。
2. 团队接受 `Repast Simphony` / Java / Eclipse 工具链。
3. 需要图形化建模、代码生成和 runtime visualization 一体化。
4. 可以接受实现的是 `Harel statecharts` 的子集，而不是全部语义。

### 不适用或高成本场景

如果目标是通用工业控制、独立验证后端或脱离 `Repast` 生态的可交换状态机模型，这套基础设施就偏窄。

## 与相邻形式主义的关系

相对 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)，本文是具体 statechart 子集的工具落地；相对 [mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md](../mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md)，它更偏 ABM 场景而不是组件化 reactive systems；相对 [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)，它偏工程执行与可视化，不强调 formal verification semantics。

## 与本研究的关系

### 对 Project 1 的价值

它补了一条“statechart 图 -> metamodel -> 代码 -> runtime panel”完整可执行基础设施证据，说明状态机文库不只需要理论节点，也需要这种可落地载体。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像某类 `Statecharts` 工具生态的目标运行载体，而不是通用中间表示。

### 对需求到模型生成的启发

1. 如果后续要让 LLM 生成 statecharts，除了状态和边，还应考虑 metamodel 字段、trigger 类型和代码块承载。
2. 可视化 runtime panel 说明“生成之后怎么被人调试和操控”同样值得提前设计。
3. 对教学或行为解释性要求高的场景，statechart 的图形可观察性本身就是重要价值。

### 现实限制

论文路线高度绑定 `Repast Simphony`；若研究目标是跨平台标准化或高强度形式验证，仍需转向更中立或更正式的载体。

## 重要的相关工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)：statecharts 的理论母线。
- [mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md](../mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md)：组件化 statechart framework 工具线。
- [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)：另一条更强调 formal semantics 的 statechart/robot DSL 工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Statecharts / Repast Simphony`
- 论文角色：statechart editor / code-generation / runtime-visualization framework
