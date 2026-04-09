# 面向 mCRL2 的可执行 UML 规格模型检验 / Towards model checking executable UML specifications in mCRL2

## 基本信息

- 标题：Towards model checking executable UML specifications in mCRL2
- 中文标题：面向 mCRL2 的可执行 UML 规格模型检验
- 作者：Helle Hvid Hansen，Jeroen Ketema，Bas Luttik，MohammadReza Mousavi，Jaco van de Pol
- 发表：*Innovations in Systems and Software Engineering*，6(1-2):83-90，2010
- DOI：`10.1007/s11334-009-0116-1`
- 链接：https://doi.org/10.1007/s11334-009-0116-1
- 形式主义：`Executable UML / xUML -> mCRL2`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`xUML` 到 `mCRL2/LTSmin` 的模型检验桥接路线
- 工具/实现获取方式：原文明确给出 `mCRL2` 工具集与 `LTSmin` 工具集入口；翻译原型本身是论文中的研究实现，未给独立公开仓库。
- 标准/格式获取方式：输入承载是 `Cassandra/xUML` 风格的 class diagram + state machine；输出承载是 `mCRL2` 进程代数规格；相关标准背景来自 `OMG UML` 规范。

## 简报

这篇论文补的是一条很实用的验证桥：把 railway interlocking 场景里实际使用的 `xUML` 子集翻译成 `mCRL2`，再交给 `mCRL2/LTSmin` 做显式或符号模型检查。它不打算重新定义一门新的状态机语言，而是把 `class diagram + state machine + event pool + run-to-completion` 这套可执行 `UML` 语义压成可分析的 process-algebra 模型。

- 形式主义定位：`xUML` 验证桥接方法，不是新的状态机族本体论文。
- 构造方式简述：`xUML` 类图与状态机先被展平、补事件池，再翻译成 `mCRL2` 进程，并交给 `mCRL2/LTSmin` 做 safety checking。
- 基础设施与场景简述：依托 `mCRL2`、`LTSmin`、`Cassandra/xUML` 与 railway interlocking toy model，服务可执行 `UML` 设计的安全属性验证。

```text
xUML class/state model -> flattening + event-pool semantics -> mCRL2 processes -> mCRL2/LTSmin -> safety result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `xUML` 的 class diagrams、class generalisations 与 associations。
2. 带 signal events 和 change events 的 UML state machines。
3. 每个状态机伴随的 event pool。
4. `mCRL2` 进程代数规格与 `LTSmin` 符号/显式模型检查。
5. local / atomic / global 三类 run-to-completion 假设。

### 核心抽象

结合论文的翻译流程，可把单个 `xUML` 类的编译结果保守整理为：

$$
\mathrm{Comp}(X) = P_{sm}(X) \parallel P_{buf}(X)
$$

上式中的符号逐项解释如下：

1. `X` 是某个 `xUML` 类实例对应的行为模型。
2. `P_{sm}(X)` 是表示状态机控制逻辑的 `mCRL2` 进程。
3. `P_{buf}(X)` 是表示该状态机 event pool 的缓冲进程。
4. 这组记号是依据论文“state machine part + buffer part”做的保守整理，不是原文直接给出的统一元组。

论文对状态机局部运行配置的描述可以保守写成：

$$
\sigma = (\mathrm{Conf}, Q)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Conf}` 是当前 active state configuration。
2. `Q` 是尚未处理的事件队列。
3. `\sigma` 表示 run-to-completion 语义下的局部离散配置。

论文还明确比较了三类 RTC 假设，其关系可直接压成：

$$
\mathrm{AtomicRTC} \Rightarrow \mathrm{LocalRTC}
$$

$$
\mathrm{GlobalRTC} \not\Rightarrow \mathrm{LocalRTC},\quad \mathrm{GlobalRTC} \not\Rightarrow \mathrm{AtomicRTC}
$$

上式中的符号逐项解释如下：

1. `LocalRTC` 表示同一状态机处理一个事件时，必须完成本地 run-to-completion 后才能取下一个事件。
2. `AtomicRTC` 表示某状态机执行本地 RTC 时，其他状态机也不能取事件。
3. `GlobalRTC` 表示只有当系统内部事件池都清空时，环境才能再注入外部事件。
4. 这些蕴含与非蕴含关系是论文正文直接给出的结论。

### 一个最小例子与通俗解释

论文用铁路联锁 toy example 说明这条路线：

1. 一个 route-setting 逻辑先在 `xUML` 中写成类图和状态机。
2. 轨道元件通过 signal events 异步通信。
3. change events 用于在条件从 false 变成 true 时向 event pool 插入事件。
4. 翻译后，每个类变成“状态机进程 + 队列进程”。

通俗地说，这像是把 `UML` 状态机的“图形面子”撕掉，露出里面真正会跑的“事件队列 + 状态配置 + 并发交错规则”，再交给 `mCRL2` 这类更擅长算状态空间的后端。

### 运行 / 接受 / 转移语义

论文强调 event pool 的核心处理规则可保守写成：

$$
(\mathrm{Conf}, Q) \xrightarrow{e} (\mathrm{Conf}', Q')
$$

其中：

1. `e` 是从 `Q` 中 dispatch 出来的当前事件。
2. 先在状态机里执行一轮对应的 local RTC。
3. 再得到新的 active configuration `\mathrm{Conf}'` 与新队列 `Q'`。

对 change events，论文明确说明 `when(cond)` 在 `cond` 从 false 变为 true 时向队列追加事件，而且即使之后条件又变回 false，该事件仍可保留在队列中等待分发。

### 语义边界

论文边界很清楚：

1. 只翻译 `xUML` 的一个子集，而不是完整 UML。
2. 子集主要覆盖 class generalisations、associations、signal events、change events 与 composite/concurrent states。
3. 翻译目标是 safety-property verification，不是代码生成。
4. 结果严重依赖 RTC 假设；同一模型在不同 RTC 语义下的状态空间和可观察 trace 会明显不同。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 类的翻译骨架 | `$\mathrm{Comp}(X) = P_{sm}(X) \parallel P_{buf}(X)$` | 每个类由状态机进程与事件池进程共同表示。 |
| 局部配置 | `$\sigma = (\mathrm{Conf}, Q)$` | active states 与 event queue 是关键运行状态。 |
| RTC 关系 | `$\mathrm{AtomicRTC} \Rightarrow \mathrm{LocalRTC}$` | 原文直接比较的并发语义层级。 |
| RTC 差异 | `$\mathrm{GlobalRTC} \not\Rightarrow \mathrm{LocalRTC}$` | 外部输入何时进入系统会改变可观察行为。 |
| change event 触发 | `$cond:false \to true \Rightarrow when(cond)\in Q$` | change event 由条件边沿触发，而不是持续条件本身。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 UML state machines 展开。 |
| 事件 / 触发 | 很强 | signal events 与 change events 是主线。 |
| 守卫 / 数据 | 中等支持 | 覆盖类属性、关联引用与 change 条件，但不是数据密集型语义论文。 |
| 层次 | 中等支持 | 支持 composite / concurrent states，但翻译时会展平。 |
| 并发 / 同步 | 强支持 | 重点就是多类实例并发与 RTC 交错。 |
| 时间约束 | 弱支持 | 这篇不做 timed UML，而是 executable UML 的离散验证桥。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围。 |
| 可执行 / 可验证性 | 很强 | 直接落到 `mCRL2/LTSmin` 做模型检查。 |

### 形式化问题与性质

1. 论文核心问题是“如何把 `xUML` 的可执行子集稳定翻成可验证的 `mCRL2` 模型”。
2. event pool 的显式建模是关键，因为 `UML` 的语义歧义很多都压在 dispatch 与 RTC 上。
3. 结果表明，对同一模型，RTC 假设本身就会成为重要的语义变量。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 `Cassandra/xUML` 风格写 class diagrams 与 state machines。
2. 把类继承层次展平。
3. 为每个状态机显式补 event pool 语义。
4. 翻译到 `mCRL2`，再交给 `mCRL2/LTSmin`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `xUML` 类图与状态机模型。
2. `mCRL2` 进程代数文本规格。
3. `LTSmin` 可消费的状态空间/模型检查后端格式。

### 交换与互操作

这篇论文的互操作重点在于：

1. `UML/xUML` 前端与 `mCRL2` 后端之间的语义桥接。
2. 用 `mCRL2` 明确化 `UML` 本来较模糊的执行语义。
3. 再由 `LTSmin` 负责规模更大的状态空间探索。

## 配套基础设施

- 建模/编辑工具：`Cassandra/xUML` 风格建模环境与一般 UML 类图/状态机编辑器。
- 解析/交换/元模型支持：类图、状态机、event pool 和关联引用会被翻成 `mCRL2` 数据类型与进程参数。
- 仿真/执行支持：论文重点不在仿真，而在把 `xUML` 运行语义交给 `mCRL2` 解释。
- 验证/分析支持：`mCRL2` toolset 与 `LTSmin`。
- 代码生成/转换支持：核心是 `xUML -> mCRL2` 翻译，而不是部署代码生成。
- 标准化或社区生态：`UML` 规范、`mCRL2`、`LTSmin` 构成主要生态；原文未给独立中立交换标准。

## 适用场景与需求前提

### 适用场景

适合已经采用可执行 `UML` 做软件/控制逻辑设计，并希望把 safety property 拉到 formal backend 上做验证的场景，尤其是铁路联锁、离散控制和事件驱动软件。

### 需求前提

1. 行为逻辑能落进论文支持的 `xUML` 子集。
2. 需求主要是 safety-style property，而不是复杂连续物理约束。
3. 团队能接受对 RTC 假设做明确选择，而不是继续保留语义模糊性。

### 不适用或高成本场景

如果模型高度依赖完整 UML 特性、复杂对象实例化模式或非离散物理动力学，这条路线会变得笨重或不适用。

## 与相邻形式主义的关系

相对 [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md)，它不走 timed collaboration + observer 路线，而是把 executable `UML` 的离散语义翻到 `mCRL2`；相对 [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)，它覆盖的 UML 子集更窄，但更强调后端模型检查链路；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，它是 verification bridge，而不是 runtime execution bridge。

## 与本研究的关系

### 对 Project 1 的价值

它说明 `UML` 这类工程前端并不一定只能停留在图形层，完全可以通过语义压缩与显式队列建模接到严格的 formal backend。

### 作为目标形式主义还是中间表示

更像中间表示桥接路线，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 若要让 LLM 生成的状态机能进 formal backend，事件池、dispatch 和 RTC 规则必须显式化。
2. 面向对象状态机的验证里，关联引用和 change events 常是语义难点。
3. 同一前端模型在不同执行假设下可能对应不同验证结论，这对后续“生成-验证-修复”闭环很重要。

### 现实限制

它证明的是一条可行桥，而不是“完整 UML 已被一次性形式化完毕”。

## 重要的相关工作

1. [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md)：另一条 `UML -> formal backend` 路线，但偏 timed collaboration。
2. [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)：更完整的 UML 状态机直接语义。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 形式化与自动验证路线的后续总览。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：主贡献是把 `xUML` 子集稳定翻译到 `mCRL2/LTSmin` 的验证链，而不是提出新的状态机本体。
