# Yakindu 状态图的形式化组合语义 / Formal Compositional Semantics for Yakindu Statecharts

## 基本信息

- 标题：Formal Compositional Semantics for Yakindu Statecharts
- 中文标题：Yakindu 状态图的形式化组合语义
- 作者：Bence Graics，Vince Molnár
- 发表：*Proceedings of the 24th PhD Mini-Symposium*，pp. 22-25，2017
- DOI：`10.5281/zenodo.291892`
- 链接：https://doi.org/10.5281/zenodo.291892
- 形式主义：`Yakindu Statecharts / compositional language`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：composition language + formal semantics for component-based Yakindu models
- 工具/实现获取方式：论文明确以 `Yakindu` 作为上游状态图编辑器，并计划基于该语义构建完整工具链；原文尚未给出现成公开实现仓库。
- 标准/格式获取方式：核心承载方式是论文定义的 system / component / interface / port / channel metamodel 与组合语义，不是独立国际标准。

## 简报

这篇论文的重点不是重新定义单个 statechart 的执行，而是补 `Yakindu` 一直缺的“组件化组合层”。作者把 `Yakindu` 单体状态图抽象成统一接口对象，再定义 ports、channels、system interface 和 step-wise 组合语义，使多个 statechart 可以像组件一样拼成一个 composite system。

- 形式主义定位：statechart composition language / infrastructure，而不是一般性验证算法。
- 构造方式简述：先把单个 `Yakindu` 状态图抽象为输入、输出、状态、初态和迁移的五元组，再把多个状态机组合为带 channel association 的系统四元组。
- 基础设施与场景简述：依托 `Yakindu` 编辑器和代码生成生态，服务复杂嵌入式 reactive systems 的组件化设计、代码生成和形式验证前端。

```text
Yakindu statechart components -> ports / interfaces / channels -> composite-system semantics -> code-generation / model-transformation framework
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 单个 `Yakindu` statechart 的抽象五元组。
2. component / instance / interface / port。
3. channel associations。
4. system input/output interface。
5. complete run 与单步组合语义。

### 核心抽象

论文直接把 `Yakindu` 状态图抽象成：

$$
S = \langle I, O, S, s_0, T \rangle
$$

并进一步说明：

$$
T \subseteq (2^I \times S) \times (S \times 2^O)
$$

上式中的符号逐项解释如下：

1. `I` 是输入事件集合。
2. `O` 是输出事件集合。
3. `S` 是状态集合，其中也吸收了变量取值与 state configuration。
4. `s_0` 是初始状态。
5. `T` 表示在一组输入事件作用下从某状态迁移到新状态并产生一组输出事件。

论文对组合系统给出的核心对象是：

$$
C = \langle SC, CA, IN, OUT \rangle
$$

上式中的符号逐项解释如下：

1. `SC` 是状态机组件集合。
2. `CA` 是 channel associations。
3. `IN` 是系统输入接口。
4. `OUT` 是系统输出接口。
5. 这四元组把多个 `Yakindu` 状态图提升成可组合系统。

论文还把系统运行定义为 step sequence：

$$
\rho = (\tau_1, \tau_2, \ldots), \qquad \tau_j = (s_j, i_j, s'_j, o_j)
$$

上式中的符号逐项解释如下：

1. `\rho` 是 complete run。
2. `\tau_j` 是第 `j` 步。
3. `s_j` 是各组件在步前的状态向量。
4. `i_j` 是该步输入事件集合。
5. `s'_j` 是步后的状态向量。
6. `o_j` 是本步产生的输出集合。

关于跨步传播，论文给出非常关键的约束：

$$
\mathrm{tgd}(o_j) \subseteq i_{j+1} \subseteq \mathrm{tgd}(o_j) \cup IN
$$

上式中的符号逐项解释如下：

1. `\mathrm{tgd}(o_j)` 表示由上一轮输出经 channels 触发到下一轮的输入。
2. 左侧包含关系表示 channel 传播来的输入不能丢。
3. 右侧包含关系表示环境还可以额外注入系统公开输入接口中的事件。
4. 这正是组合层“事件沿端口传播”的正式化表达。

### 一个最小例子与通俗解释

论文给的 coffee-machine / light-switch 例子已经非常清楚：

1. `CoffeeMachine` 组件有 `on / off / cappuchino` 输入和 `lightOn / lightOff` 输出。
2. `LightSwitch` 组件有 `on / off` 输入。
3. channel 把 `machine.lightOn` 接到 `light.on`，把 `machine.lightOff` 接到 `light.off`。
4. 于是咖啡机状态图一旦发出点亮/熄灭灯事件，灯的 statechart 会在下一步自动接到对应输入。

通俗地说，这就像给单体 `Yakindu` 状态图加了一层“组件接口插槽”。以前每个图自己跑，现在可以通过 ports 和 channels 拼成系统级状态机网络。

### 运行 / 接受 / 转移语义

论文继承 `Yakindu` 的 turn-based semantics，并指出每个 turn 包含 raising section 与 running section：

1. raising section 先把输入事件置为当前 turn 有效。
2. running section 再检查当前配置下哪些迁移被这些事件触发。
3. 多条迁移同时可触发时，仍按 `Yakindu` 的 transition priority 解决歧义。
4. 组合层只负责事件如何在组件间传播，不重写单个组件的本体语义。

### 语义边界

论文也明确给出边界：

1. 它只定义 event-based composition，不引入 message queues。
2. parameterized events 在无缓冲语义下可能互相覆盖。
3. 它主要面向 component-based reactive systems，而不是一般对象系统。
4. 这是形式语义与工具链前导工作，不是成熟工业标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单组件抽象 | `$S = \langle I, O, S, s_0, T \rangle$` | 把 `Yakindu` 单体 statechart 压成统一接口对象。 |
| 迁移关系 | `$T \subseteq (2^I \times S) \times (S \times 2^O)$` | 允许一组输入事件共同触发一次迁移并产出一组输出。 |
| 组合系统 | `$C = \langle SC, CA, IN, OUT \rangle$` | ports/channels/system interface 的最小语义骨架。 |
| 事件传播 | `$\mathrm{tgd}(o_j) \subseteq i_{j+1} \subseteq \mathrm{tgd}(o_j) \cup IN$` | 说明输出如何通过 channel 成为下一步输入。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 单组件仍是状态机，系统层是状态向量。 |
| 事件 / 触发 | 很强 | 整个组合语言都围绕事件端口传播构建。 |
| 守卫 / 数据 | 中等支持 | 单体 `Yakindu` 支持变量与 guards，但本文抽象层主要保留事件与配置。 |
| 层次 | 间接支持 | 底层 `Yakindu` statechart 支持 hierarchy；组合语言本身不再重写层次语义。 |
| 并发 / 同步 | 很强 | 多组件组合与 channel 传播正是论文主线。 |
| 时间约束 | 弱支持 | 本文不专门扩展 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 不在本文讨论范围。 |
| 可执行 / 可验证性 | 很强 | 组合语义就是为精确代码生成和形式分析服务。 |

### 形式化问题与性质

1. 论文真正补的是 `Yakindu` 从“单图可建模”走向“多图可组合”的基础设施缺口。
2. ports、system interface 和 channels 使系统边界与组件边界都变得显式。
3. 对 `project_1` 来说，这类组合语言比单体 statechart 更接近复杂控制系统的真实工程结构。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 先用 `Yakindu` 绘制单个 statechart。
2. 为组件声明 interface 和 ports。
3. 实例化多个 components。
4. 用 channels 和 system interface 连接它们。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `System / Component / Interface / Port / Channel` metamodel。
2. state machine 五元组抽象。
3. 组合系统四元组。
4. complete run / step sequence。

### 交换与互操作

互操作的重点很明确：

1. 底层仍复用 `Yakindu` 作为单图编辑与代码生成入口。
2. 组合层则引入独立 metamodel 表达组件连接。
3. 后续可把 composite system 进一步变换到形式验证后端。

## 配套基础设施

- 建模/编辑工具：`Yakindu Statechart Tools`。
- 解析/交换/元模型支持：论文明确给出组合语言 metamodel。
- 仿真/执行支持：组合语义与 `Yakindu` turn-based semantics 对齐。
- 验证/分析支持：作者明确以 formal analysis 和 model transformation 为目标。
- 代码生成/转换支持：论文把 precise code generation 列为主要动机之一。
- 标准化或社区生态：这是研究型组合语言，不是已标准化 profile。

## 适用场景与需求前提

### 适用场景

适合复杂嵌入式 reactive systems，尤其适合单个状态图已不足以表达模块化结构、需要按组件边界做代码生成与形式分析的场景。

### 需求前提

1. 上游行为已经适合用 `Yakindu` statechart 表达。
2. 系统交互主要是 event-based，而不是数据流或消息队列驱动。
3. 组件边界、端口方向和连接关系可以显式建模。
4. 团队希望后续能接代码生成与模型变换。

### 不适用或高成本场景

如果系统本质上是 message-buffer-heavy、dataflow-heavy 或需要复杂动态拓扑，这套 event-based composition 语义会显得过于克制。

## 与相邻形式主义的关系

相对 [mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md](../mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md)，这篇论文更早、更轻量，也更直接绑定 `Yakindu`；相对 [transforming-medical-best-practice-guidelines-to-executable-and-verifiable-statechart-models/desc.md](../transforming-medical-best-practice-guidelines-to-executable-and-verifiable-statechart-models/desc.md)，后者把 `Yakindu` 当单体状态图前端，而这里补的是其组合层；相对 [on-the-formal-semantics-of-visualstate-statecharts/desc.md](../on-the-formal-semantics-of-visualstate-statecharts/desc.md)，`VisualSTATE` 论文主要固定单图执行语义，而这里补的是组件连接语义。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 很关键，因为控制系统需求很少天然就是“一个大状态图”，更常见的是多个控制部件、接口和协同关系。若 LLM 只会生成单图而不会生成组合结构，离工程可用还差很远。

### 作为目标形式主义还是中间表示

很适合作为组件化 statechart 的工程目标方言，也可作为更强后端前的组合层中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应尽量保留组件边界、端口和事件流向。
2. 组合语义最好先独立于底层状态图细节建模，这样更利于后续替换单图方言。
3. 若希望闭环到验证和代码生成，接口层语义必须与单图语义同样正式。

### 现实限制

论文本身还是早期工作，未给出成熟工具链与大规模工业验证结果。

## 重要的相关工作

1. [mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md](../mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md)：后续更完整的 statechart composition framework。
2. [transforming-medical-best-practice-guidelines-to-executable-and-verifiable-statechart-models/desc.md](../transforming-medical-best-practice-guidelines-to-executable-and-verifiable-statechart-models/desc.md)：`Yakindu` 到验证后端的桥接工作。
3. [on-the-formal-semantics-of-visualstate-statecharts/desc.md](../on-the-formal-semantics-of-visualstate-statecharts/desc.md)：另一条 statechart 方言的正式语义固定化路线。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Yakindu Statecharts / compositional language`
- 论文角色：composition language + formal semantics for component-based Yakindu models
- 归类理由：论文主体是 `Yakindu` 组件化组合语言与接口基础设施，而不是单纯验证方法或案例应用。
