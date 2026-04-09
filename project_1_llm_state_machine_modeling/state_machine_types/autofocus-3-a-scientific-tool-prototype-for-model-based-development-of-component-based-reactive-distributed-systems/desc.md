# AutoFocus 3：面向组件化反应式分布式系统的模型驱动原型工具 / AutoFocus 3 - A Scientific Tool Prototype for Model-Based Development of Component-Based, Reactive, Distributed Systems

## 基本信息

- 标题：AutoFocus 3 - A Scientific Tool Prototype for Model-Based Development of Component-Based, Reactive, Distributed Systems
- 中文标题：AutoFocus 3：面向组件化反应式分布式系统的模型驱动原型工具
- 作者：Florian Hölzl，Martin Feilkas
- 发表：*Model-Based Engineering of Embedded Real-Time Systems*，pp. 317-322，2010
- DOI：`10.1007/978-3-642-16277-0_13`
- 链接：https://doi.org/10.1007/978-3-642-16277-0_13
- 形式主义：`Focus / AutoFocus 3`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：component-based model-based development workbench with logical architecture, topology, deployment and code generation
- 工具/实现获取方式：原文给出 `AutoFocus 3` 站点 `http://af3.in.tum.de`，并说明工具运行在 Eclipse 平台之上。
- 标准/格式获取方式：承载方式是 `AutoFocus 3` 的 component / port / channel / I/O automata / topology / deployment 建模语法及生成的 `C` 代码；原文未给独立中立交换标准。

## 简报

`AutoFocus 3` 的核心价值，不是单个验证算法，而是把组件化逻辑架构、执行平台拓扑、deployment 和代码生成收进同一套语义连续的模型驱动流程。它基于 `Focus` 的 streams/stream-processing semantics，但在工程上落成了一个明确面向 reactive distributed embedded systems 的 CASE 工具。对本论文集而言，它补的是“组件自动机 + 部署模型 + 工具链”这类 DSL/workbench 方向。

- 形式主义定位：以 `Focus` 为语义底座的 component-automata workbench，而不是单一验证后端。
- 构造方式简述：先建 logical architecture 中的 components/ports/channels 与 stateful/stateless behavior，再建 topology 和 deployment，最后生成面向目标执行平台的代码。
- 基础设施与场景简述：依托 Eclipse-based tool、I/O automata、global discrete time、ECU/bus topology、deployment model 与 code generation，服务 embedded reactive systems 的逐层建模。

```text
logical architecture -> I/O automata / tables -> topology -> deployment -> generated C code -> validation / verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. logical architecture 中的 communicating components。
2. typed input/output ports 与 channels。
3. strong / weak causal time-synchronous semantics。
4. stateful I/O automata 与 stateless tabular behavior。
5. topology architecture、deployment 与 code generation。

### 核心抽象

论文对 component interface 的描述非常明确。可把一个 stateful component 保守整理为：

$$
C = (P_{in}, P_{out}, S, V, T, s_0, \nu_0)
$$

上式中的符号逐项解释如下：

1. `P_{in}` 是输入端口集合。
2. `P_{out}` 是输出端口集合。
3. `S` 是 control states 集合。
4. `V` 是 data state variables 集合。
5. `T` 是状态转移函数或转移规则集合。
6. `s_0` 是初始控制状态。
7. `\nu_0` 是所有数据状态变量的初值。

论文对 stateful behavior 的口头定义可以进一步压成：

$$
T : S \times Val(P_{in}) \times Val(V) \rightarrow S \times Val(P_{out}) \times Val(V)
$$

上式中的符号逐项解释如下：

1. 左侧是当前 control state、当前输入值和当前数据变量值。
2. 右侧是下一 control state、当前时刻输出值和更新后的数据变量值。
3. 论文原文明确说：state transition function 由当前状态、当前输入和当前数据状态映到输出与后继状态变量值。

对组件网络，论文给出的核心对象是 component set 与 channel relation，因此可保守写成：

$$
N = (Comp, Ch)
$$

上式中的符号逐项解释如下：

1. `Comp` 是组件集合。
2. `Ch \subseteq P_{out} \times P_{in}` 是 channels。
3. 每个 channel 连接一个 output port 和一个 input port。
4. 从逻辑层看，channel 是瞬时传输的。

### 一个最小例子与通俗解释

论文直接给了一个 pedestrian traffic lights system：

1. 一个 `Controller` 组件负责应用行为。
2. 一个 `Merge` 组件合并两侧按钮请求。
3. 两者通过 typed ports 与 channels 连接。
4. `Controller` 是 strong causal，`Merge` 可以是 weak causal。

通俗地说，`AutoFocus 3` 把“系统逻辑长什么样”“它最后部署到哪些 ECU / bus 上”“代码怎样生成”放在同一模型家族里。你不是只画状态图，而是在画一套能逐步下钻到平台的 component architecture。

### 运行 / 接受 / 转移语义

论文把时间语义收束得很清楚：系统基于离散、全局同步的 logical ticks。因而网络执行可保守看成逐 tick 计算：

$$
N(t+1) = F(N(t), I(t))
$$

上式中的符号逐项解释如下：

1. `N(t)` 是时刻 `t` 所有组件的全局组合状态。
2. `I(t)` 是该 tick 的输入消息集合。
3. `F` 是由组件网络、因果类别和 channels 共同决定的同步更新函数。
4. 这正对应论文所说的 time-synchronous streams 和 globally synchronized clocks。

论文还区分了两类因果性：

1. strong causal component 的当前输出不能依赖当前输入。
2. weak causal component 的当前输出可以依赖当前输入，但网络中不能形成 weak-causal cycle。

### 语义边界

1. `AutoFocus 3` 的时间是离散全局 tick，不是 dense-time clocks。
2. 文章主体是 workbench 和建模层次，不是某个验证算法的完整理论。
3. topology / deployment 在文中已出现，但更精细的调度与资源细节仍留待后续扩展。
4. 它更像 component-automata CASE tool，而不是开放交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| stateful component | `$C = (P_{in}, P_{out}, S, V, T, s_0, \nu_0)$` | `AutoFocus 3` 组件的最小保守抽象。 |
| 状态更新 | `$T : S \times Val(P_{in}) \times Val(V) \rightarrow S \times Val(P_{out}) \times Val(V)$` | 论文对 state transition function 的口头定义可压成这一型。 |
| 组件网络 | `$N = (Comp, Ch)$` | logical architecture 由 components 与 channels 构成。 |
| tick 语义 | `$N(t+1) = F(N(t), I(t))$` | time-synchronous streams 的工程化理解。 |
| 因果约束 | `strong` / `weak` | `weak` component 不可形成 weak-causal cycle。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | stateful I/O automata 是核心行为建模手段。 |
| 事件 / 触发 | 强 | 端口和消息驱动通信是一等对象。 |
| 守卫 / 数据 | 中等支持 | 支持 data state variables、input patterns 与 preconditions。 |
| 层次 | 强 | 组件可层次化组织。 |
| 并发 / 同步 | 强 | 组件网络在全局 tick 上同步演化。 |
| 时间约束 | 中等支持 | 有离散全局时间与 strong/weak causality，但不是专用 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主体内。 |
| 可执行 / 可验证性 | 很强 | 支持 validation、verification、deployment 与代码生成。 |

### 形式化问题与性质

1. `AutoFocus 3` 不是只管状态机建模，而是把 architecture/topology/deployment 串成一条工程链。
2. 它把 component automata 放在 explicit deployment context 中，这一点和普通 DSL 条目明显不同。
3. 从状态机谱系看，它适合作为 component-automata CASE workbench 证据，而不是独立母型分支。

## 构造方式与承载格式

### 建模入口

主要入口有：

1. logical architecture。
2. component interfaces、ports、channels。
3. stateful I/O automata 或 stateless tabular behavior。
4. topology architecture。
5. deployment model。

### 机器可处理承载方式

机器可处理承载方式包括：

1. component graph。
2. automata/table behavior descriptions。
3. topology/deployment models。
4. generated `C` code。

### 交换与互操作

互操作重点在工具链内部：

1. Eclipse-based modeling infrastructure。
2. automotive lab extension。
3. code generation to execution platform。

## 配套基础设施

- 建模/编辑工具：Eclipse-based `AutoFocus 3`。
- 解析/交换/元模型支持：component model、topology model、deployment model。
- 仿真/执行支持：validation 和 generated-code execution。
- 验证/分析支持：automatic test-case generation、model checking hooks。
- 代码生成/转换支持：deployment-aware `C` code generation。
- 标准化或社区生态：`Focus` 语义基础、`AutoFocus 3` 工具平台和特定 execution-platform 扩展共同构成生态。

## 适用场景与需求前提

### 适用场景

适合 reactive distributed embedded systems、需要从 logical architecture 一路下钻到 deployment 的模型驱动开发场景。

### 需求前提

1. 系统需能拆成 communicating components。
2. 行为需可写成 I/O automata 或 tabular behavior。
3. 团队接受全局离散 tick 与 time-synchronous semantics。
4. 目标平台可显式建成 execution units、busses 和 deployment relation。

### 不适用或高成本场景

如果系统主要依赖 dense-time constraints、连续动力学或完全开放的异步消息时序，`AutoFocus 3` 这套 global-tick discipline 可能不自然。

## 与相邻形式主义的关系

相对 [user-friendly-model-checking-integration-in-model-based-development/desc.md](../user-friendly-model-checking-integration-in-model-based-development/desc.md)，本文是 `AutoFocus 3` 平台本体，后者是其 model-checking integration route；相对 [formal-system-level-design-space-exploration/desc.md](../formal-system-level-design-space-exploration/desc.md)，两者都在做 model-based embedded design，但 `DIPLODOCUS` 更强调 exploration/translation，`AutoFocus 3` 更强调 component automata + deployment；相对 [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)，`DesignBIP` 更偏交互架构和生成，本文更偏全流程 embedded CASE workbench。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提供了一个很好的例子：状态机建模不一定停留在逻辑层，还可以天然联到 topology、deployment 和 code generation。
2. 对 `project_1` 的 LLM 建模任务来说，若未来想生成“更可落地的状态机工程工件”，`AutoFocus 3` 这类 component-automata workbench 很值得参考。
3. strong/weak causality 的分流，也提醒需求抽取阶段要显式区分“当前输出是否可依赖当前输入”。

### 作为目标形式主义还是中间表示

它既可以作为目标 DSL/workbench，也适合作为从需求规约下钻到平台部署之间的工程中间表示。

## 重要的相关工作

- [user-friendly-model-checking-integration-in-model-based-development/desc.md](../user-friendly-model-checking-integration-in-model-based-development/desc.md)：`AutoFocus 3` 上层的验证集成路线。
- [formal-system-level-design-space-exploration/desc.md](../formal-system-level-design-space-exploration/desc.md)：另一条 embedded model-based design + verification bridge。
- [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)：组件化建模与生成工作台方向的对照条目。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 component-automata CASE workbench 条目，适合作为 `Focus/AutoFocus` 语义在嵌入式系统建模、deployment 和代码生成方向上的基础设施证据入账。
