# UPPAAL：现状与进展 / UPPAAL: Status & Developments

## 基本信息

- 标题：UPPAAL: Status & Developments
- 中文标题：UPPAAL：现状与进展
- 作者：Kim G. Larsen，Paul Pettersson，Wang Yi
- 发表：*Computer Aided Verification*，`LNCS 1254`，pp. 456-459，1997
- DOI：`10.1007/3-540-63166-6_47`
- 链接：https://doi.org/10.1007/3-540-63166-6_47
- 形式主义：`Timed Automata / UPPAAL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：early `UPPAAL` platform overview / timed-automata simulator and verifier workbench
- 工具/实现获取方式：原文明确说明 `UPPAAL` 已作为 toolbox 发布，含 description language、simulator 与 verifier，并给出当时的安装与文档入口；本文重点就是报告这一平台状态与新增能力。
- 标准/格式获取方式：承载方式是 `UPPAAL` 的 timed-automata description language、graphical editor、textual notation、symbolic state representation 与 query-driven verifier；不是独立于工具的中立交换标准。

## 简报

这篇论文的价值，不是重新介绍 timed automata 理论，而是把早期 `UPPAAL` 明确报告成一个已经具备**语言、仿真器、验证器、优化后端和 GUI** 的完整平台。它把 `UPPAAL` 从“一个基于约束求解的验证原型”推进到“既能做早期 validation，又能做 exhaustive verification”的工作台。

- 形式主义定位：timed-automata 工具平台综述，而不是 timed automata 母模型奠基论文。
- 构造方式简述：用 network of timed automata 建模系统，再通过 simulator 观察符号执行路径，通过 verifier 做 forward on-the-fly reachability analysis。
- 基础设施与场景简述：依托 description language、graphical interface、simulator、DBM-based symbolic engine、control-structure analysis 与 compact constraint representation，服务实时控制器与实时通信协议验证。

```text
timed automata network -> UPPAAL description language / graphical editor -> symbolic states with clock constraints -> simulation / diagnostic traces / reachability checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. networks of timed automata；
2. description language；
3. graphical simulator；
4. model checker；
5. symbolic states 与约束优化技术。

### 核心抽象

虽然本文重点是平台状态，但其核心建模对象仍可保守整理为：

$$
A = (L, \ell_0, C, V, E, Inv)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `\ell_0` 是初始 location。
3. `C` 是 clocks。
4. `V` 是离散数据变量。
5. `E` 是边集合，边上带有 guard、synchronization 和 update。
6. `Inv` 是 location invariants。

全局验证对象则写成：

$$
N = A_1 \parallel A_2 \parallel \cdots \parallel A_n
$$

上式中的符号逐项解释如下：

1. `A_i` 是单个 timed automaton。
2. `\parallel` 表示 network composition。
3. `N` 是 `UPPAAL` 真正探索的整体系统。

论文反复强调符号状态而不是显式时钟赋值枚举，因此可保守写成：

$$
s = (\ell, Z)
$$

上式中的符号逐项解释如下：

1. `\ell` 是离散位置向量。
2. `Z` 是 clocks 与离散变量上的约束集合。
3. `Z` 在实现上由 `DBM` 一类差分约束结构承载。
4. simulator 与 verifier 都围绕这类符号状态工作。

### 一个最小例子与通俗解释

一个最小 `UPPAAL` 式系统可以这样理解：

1. 每个 component 是一个带 clocks 的有限状态机。
2. 位置上可以有限时停留，边上可以要求 `x <= 5` 这类 guard。
3. 多个 automata 通过 channels 和 shared variables 同步。
4. 工具既能让你手动/自动跑一条可能执行，也能穷尽性检查某个可达性或不变式。

通俗地说，`UPPAAL` 把“画一个带时钟的状态机网络”和“真正把它拿去跑、拿去证”接成了一条线；而这篇论文就是那条线早期成熟的状态报告。

### 运行 / 接受 / 转移语义

timed automata 的两类基本步骤可保守写成：

$$
(\ell, \nu) \xrightarrow{d} (\ell, \nu + d)
$$

$$
(\ell, \nu) \xrightarrow{a} (\ell', \nu')
$$

上式中的符号逐项解释如下：

1. `\ell`、`\ell'` 是离散位置。
2. `\nu`、`\nu'` 是时钟赋值。
3. `d` 是非负延时，且延时过程中要保持 invariants。
4. `a` 是同步动作或内部动作。
5. 动作步要求 guard 成立，并执行必要的 reset / variable update。

本文强调当前实现采用 forward on-the-fly reachability，因此可把核心验证问题保守压成：

$$
\mathrm{Reach}(N, Goal)
$$

或更具体地写成：

$$
\exists s \in \mathrm{Post}^\ast(s_0).\ s \models Goal
$$

上式中的符号逐项解释如下：

1. `s_0` 是初始符号状态。
2. `\mathrm{Post}^\ast` 表示反复应用 delay / action successors 得到的可达符号状态集合。
3. `Goal` 是用户关心的可达性或不变式相关条件。
4. 论文同时指出 bounded liveness 往往通过 testing automata 或 decorated systems 间接处理。

### 语义边界

1. 论文时代的 `UPPAAL` 主打 invariant / reachability 一类性质，而不是通用时序逻辑全覆盖。
2. 数据类型支持仍较受限，重点还是 clocks 与有限控制。
3. 这是平台论文，因此不重讲 timed automata 理论完备细节。
4. 其优势主要来自高效约束求解和工程化前端，而不是更强的模型表达力。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单个 automaton 骨架 | `$A = (L, \ell_0, C, V, E, Inv)$` | `UPPAAL` 的基本建模单元。 |
| 网络组合 | `$N = A_1 \parallel \cdots \parallel A_n$` | 平台验证对象是 timed-automata 网络。 |
| 符号状态 | `$s = (\ell, Z)$` | 工具不枚举所有时钟值，而是操作约束区。 |
| reachability | `$\exists s \in \mathrm{Post}^\ast(s_0).\ s \models Goal$` | forward on-the-fly model checking 的核心任务。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | timed automata locations / network 是核心。 |
| 事件 / 触发 | 很强 | channels 与 shared variables 是标准配套。 |
| 守卫 / 数据 | 中等支持 | guards、clocks 与有限数据类型可用，但数据仍较受限。 |
| 层次 | 不支持 | 不是层次状态机平台。 |
| 并发 / 同步 | 很强 | network composition 是基本假设。 |
| 时间约束 | 很强 | 整个平台围绕 clocks 与约束求解建立。 |
| 连续动态 / 随机性 | 不支持 | 不面向 hybrid / probabilistic semantics。 |
| 可执行 / 可验证性 | 很强 | simulator、diagnostic traces 与 verifier 已成体系。 |

### 形式化问题与性质

1. 论文真正要说明的是：`UPPAAL` 已经不只是 checker，而是 validation + verification 一体化平台。
2. forward analysis、control-structure reduction 与 compact constraints 共同决定了它为何能跑得更大。
3. simulator 的加入也很关键，因为它把“看到一条真实可执行 trace”变成了早期建模纠错手段。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口有：

1. graphical interface 中画 timed automata；
2. textual notation 直接写模型；
3. channels、shared variables 与 clocks 的声明；
4. query-driven verification 与 diagnostic trace inspection。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed-automata description language；
2. symbolic states 与 `DBM` constraint structures；
3. diagnostic traces；
4. simulator / verifier 共享的内部状态表示。

### 交换与互操作

互操作重点在统一平台内部：

1. graph editor 会自动转成 textual format。
2. simulator 可直接回放 verifier 生成的 diagnostic traces。
3. verifier 与 simulator 共享同一模型骨架和符号状态视图。

## 配套基础设施

- 建模/编辑工具：graphical user interfaces 与 textual notation。
- 解析/交换/元模型支持：description language、editor-to-text transformation 与 trace replay。
- 仿真/执行支持：interactive / automatic simulator，可记录与回放 traces。
- 验证/分析支持：forward on-the-fly reachability、breadth-first / depth-first exploration、diagnostic trace generation。
- 代码生成/转换支持：原文不强调代码生成；重点是建模、仿真与验证。
- 标准化或社区生态：作为 `UPPAAL` 早期平台总览，是后续 `UPPAAL 4.0`、`UPPAAL-Tiga`、`UPPAAL-SMC` 等路线的基础锚点。

## 适用场景与需求前提

### 适用场景

适合实时控制器、嵌入式调度问题和时序敏感通信协议，尤其是那些能自然压成 network of timed automata 的系统。

### 需求前提

1. 系统的时间行为能由有限 clocks 与 guard / invariant 表达。
2. 并发交互可通过同步 channels 与共享变量描述。
3. 核心验证目标主要是 reachability / safety 一类问题。

### 不适用或高成本场景

如果需求依赖概率、连续动力学、复杂层次结构或富数据状态，那么 1997 年这版 `UPPAAL` 还不是直接答案。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，教程文更像系统手册，而本文更像平台状态汇报；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，`UPPAAL 4.0` 展示的是更成熟的语言和库演化，本文则记录更早期的“simulator + forward engine + GUI”基线；相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，后者是在这条平台主线上增加 timed-game synthesis，而本文仍是经典 timed-automata validation / verification 主核。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明如果 `project_1` 最终目标语言选到 timed automata，成熟工具链是明确存在的，而且从一开始就重视“可视化执行 + 形式验证”的双入口。
2. 对需求到模型自动建模而言，这篇论文提示目标语言不只要看表达力，还要看是否有 simulator、diagnostics 和可复用后端。
3. `UPPAAL` 这种语言-工具-后端一体化设计，对后续闭环验证平台很有参考价值。

### 局限

1. 论文是工具状态汇报，不负责给出 timed automata 最原始、最完整的形式化理论。
2. 其数据与性质支持都还较早期，不能直接代表后来的整个 `UPPAAL` 生态上限。

## 重要的相关工作

1. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：更系统的 `UPPAAL` 语言与使用教程。
2. [uppaal-40/desc.md](../uppaal-40/desc.md)：后续核心平台升级锚点。
3. [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：`UPPAAL` 生态中的 timed-game synthesis 路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 `🏗️` 基础设施条目，核心价值在于把 `UPPAAL` 早期平台的语言、仿真、验证与约束后端一次性钉成文库里的 timed-automata 主干锚点。
