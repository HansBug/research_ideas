# OpenNWA：嵌套词自动机库 / OpenNWA: A Nested-Word Automaton Library

## 基本信息

- 标题：OpenNWA: A Nested-Word Automaton Library
- 中文标题：OpenNWA：嵌套词自动机库
- 作者：Evan Driscoll，Aditya Thakur，Thomas Reps
- 发表：*Computer Aided Verification*，`LNCS 7358`，pp. 665-671，2012
- DOI：`10.1007/978-3-642-31424-7_47`
- 链接：https://doi.org/10.1007/978-3-642-31424-7_47
- 形式主义：`Nested-Word Automata / OpenNWA / WALi`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：nested-word automata algorithm library and WALi/WPDS interoperability infrastructure
- 工具/实现获取方式：原文给出 `OpenNWA` 文档入口 `http://research.cs.wisc.edu/wpis/OpenNWA`，并说明它作为 `C++` `NWA` class packaged with `WALi` 提供。
- 标准/格式获取方式：主承载是 `C++` API、`NWA` class、call/internal/return transitions、client information、`WALi` weighted pushdown system conversion；它不是行业交换标准。

## 简报

这篇论文补的是 `Nested-Word Automata` 的工程化算法库。`OpenNWA` 的价值不在于重新定义 `NWA`，而在于把 call / internal / return transitions、闭包运算、determinization、complement、emptiness、example-word generation、client information 和到 `WALi` weighted pushdown systems 的转换做成一套可复用 `C++` 基础设施。

- 形式主义定位：`NWA` / nested words 的工具基础设施，而不是新的嵌套词自动机子类。
- 构造方式简述：用户通过 `NWA` class 构造嵌套词自动机，再调用 union、intersection、Kleene star、reversal、determinization、complement、emptiness 和 example generation 等操作。
- 基础设施与场景简述：依托 `WALi`、`WPDS` conversion、client-information callbacks 和 example-word extraction，服务 interprocedural program analysis、XML / structured data analysis 与 nested trace reasoning。

```text
nested word / ICFG structure -> OpenNWA NWA object -> automata operations + WALi WPDS conversion -> emptiness / example word / program-analysis queries
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. nested word，即线性词加不交叉 nesting relation。
2. call、return 与 internal positions。
3. `NWA` 的 call/internal/return transitions。
4. `OpenNWA` 的 `C++` `NWA` class 与 automata-theoretic operations。
5. `WALi` weighted pushdown system interoperability。

### 核心抽象

嵌套词可保守整理为：

$$
nw = (a_1\cdots a_n, \nu)
$$

上式中的符号逐项解释如下：

1. `$a_1\cdots a_n$` 是普通线性输入词。
2. `$\nu$` 是 positions 之间的不交叉 nesting relation。
3. `$\nu(i,j)$` 表示位置 `$i$` 是 call position，位置 `$j$` 是与之匹配的 return position。
4. 不在 nesting edge 两端的位置是 internal position；未在词内匹配的位置可以是 pending call 或 pending return。

`NWA` 可保守写成：

$$
A = (Q, Q_0, F, \delta_c, \delta_i, \delta_r)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是状态集合。
2. `$Q_0 \subseteq Q$` 是初始状态集合。
3. `$F \subseteq Q$` 是接受状态集合。
4. `$\delta_c$` 是 call transitions。
5. `$\delta_i$` 是 internal transitions。
6. `$\delta_r$` 是 return transitions。
7. 论文强调 return transition 还会读取 call-predecessor state，这是 `NWA` 相对普通 `FA` 的关键差异。

return transition 的关键语义可写成：

$$
(q_{lin}, q_{call}, a, q') \in \delta_r
$$

上式中的符号逐项解释如下：

1. `$q_{lin}$` 是 return 位置前一条线性边上的状态。
2. `$q_{call}$` 是对应 call nesting edge 上保存的 call-predecessor state。
3. `$a$` 是当前位置输入符号。
4. `$q'$` 是 return transition 后的线性后继状态。

### 一个最小例子与通俗解释

一个最小例子可以是嵌套词 `call f`、`internal stmt`、`return f`：

1. 读到 `call f` 时，`NWA` 像普通自动机一样换到下一状态，同时把离开 call 位置时的状态写到 nesting edge 上。
2. 读到 `internal stmt` 时，只按普通线性状态转移。
3. 读到 `return f` 时，不只看前一个线性状态，还要看 matching call edge 上保存的状态。
4. 如果二者匹配到某条 return transition，就进入下一状态。

通俗地说，`OpenNWA` 里的 `NWA` 像“会记住调用入口的有限状态机”。它比普通 `FA` 多了一条嵌套边记忆，因此能区分函数调用/返回、XML 标签配对或括号结构是否匹配。

### 运行 / 接受 / 转移语义

论文对 `NWA` 运行的直觉说明可压成：

$$
Run_A(nw) \subseteq Q^{n+1} \times Q^{Calls}
$$

上式中的符号逐项解释如下：

1. `$Run_A(nw)$` 是 `A` 在 nested word `$nw$` 上的可能运行集合。
2. `$Q^{n+1}$` 表示每条线性边都被标上一个状态。
3. `$Q^{Calls}$` 表示 call nesting edges 也携带状态标签。
4. 当扫描到 return position 时，运行必须同时满足线性状态和 nesting-edge 状态约束。

`OpenNWA` 支持的语言空性与反例词生成可写成：

$$
L(A) = \emptyset \quad \text{or} \quad w \in L(A)
$$

上式中的符号逐项解释如下：

1. `$L(A)$` 是 `NWA` 接受的 nested-word language。
2. 若 `$L(A) \neq \emptyset$`，`OpenNWA` 可以返回某个 accepted example word。
3. 论文说明该能力通过把 `NWA` 转换到 `WPDS` 后执行 `post^*` 查询实现。

### 语义边界

1. `OpenNWA` 面向 nested-word automata，不是一般 pushdown automata 工具箱。
2. `NWA` 本身不带 weights；weights 主要通过转换到 `WALi` `WPDS` 时由用户提供的 `WeightGen` 产生。
3. 它适合 call-return / XML / structured word 这类显式 nesting 关系，不适合完全任意的无结构上下文无关语言。
4. 论文重心是 library operations 与 interoperability，不重新证明 `NWA` 理论全貌。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| nested word | `$nw=(a_1\cdots a_n,\nu)$` | 输入同时有线性顺序与不交叉嵌套关系。 |
| `NWA` 骨架 | `$A=(Q,Q_0,F,\delta_c,\delta_i,\delta_r)$` | `OpenNWA` 的核心工作对象。 |
| return transition | `$(q_{lin},q_{call},a,q')\in\delta_r$` | return 位置同时读取线性状态和 call-predecessor state。 |
| 运行结构 | `$Run_A(nw)\subseteq Q^{n+1}\times Q^{Calls}$` | 运行不仅标线性边，也标 nesting edges。 |
| 空性 / 示例词 | `$L(A)=\emptyset$` 或 `$w\in L(A)$` | `OpenNWA` 通过 `WPDS` 查询支持 emptiness 与 example generation。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接表示 `NWA` states 与 transitions。 |
| 事件 / 触发 | 很强 | 输入符号分为 call、internal、return 三类位置。 |
| 守卫 / 数据 | 弱支持 | 主线不是 data automata，但 client information 可附加状态元数据。 |
| 层次 | 很强 | nesting relation 是模型核心。 |
| 并发 / 同步 | 间接支持 | 可用于 interprocedural control-flow 分析，但不是并发同步语言。 |
| 时间约束 | 不支持 | 不属于 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 nested-word language infrastructure。 |
| 可执行 / 可验证性 | 很强 | 提供 automata operations、emptiness、example generation 与 `WALi` interoperability。 |

### 形式化问题与性质

1. `OpenNWA` 的核心价值是把 `NWA` 理论闭包与判定操作做成可复用库。
2. `WPDS` interoperability 让 `NWA` 不只是孤立语言模型，也能直接服务程序分析查询。
3. client-information 机制说明库设计考虑了上层分析工具给状态附加语义信息的需求。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 手工或程序化构造的 `NWA`。
2. interprocedural control-flow graph (`ICFG`) 到 `NWA` 的编码。
3. XML / nested structure 对象的 nested-word 编码。
4. `WALi` / `WPDS` 查询工作流。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `C++` `NWA` class。
2. call/internal/return transition sets。
3. epsilon internal transitions 与 wild transitions。
4. client-information callbacks。
5. `NWA -> WALi WPDS` conversion。

### 交换与互操作

互操作重点是与 `WALi` 生态的深度连接：

1. `OpenNWA` 可把 `NWA` 转成 `WALi` `WPDS`。
2. `WPDS` stack 对应尚未匹配的 nesting edges 上的状态。
3. emptiness 与 example-word generation 可以借助 `WPDS post^*` 与 witness tracing 实现。

## 配套基础设施

- 建模/编辑工具：主体是 `C++` library，而不是图形编辑器。
- 解析/交换/元模型支持：`NWA` class、transition API、client information、documentation。
- 仿真/执行支持：支持 example word generation，可用于向分析工具用户展示违反性质的结构化路径。
- 验证/分析支持：intersection、union、Kleene star、reversal、concatenation、determinization、complement、emptiness checking、shortest accepted word 等。
- 代码生成/转换支持：支持 `NWA -> WPDS` conversion；不主打部署代码生成。
- 标准化或社区生态：依托 `WALi` / `WPDS` / Wisconsin program-analysis infrastructure。

## 适用场景与需求前提

### 适用场景

适合程序调用/返回轨迹分析、interprocedural data-flow pruning、XML / HTML / nested document validation、CEGAR counterexample extraction 和结构化事件流分析。

### 需求前提

1. 输入对象需同时有线性顺序与不交叉嵌套匹配。
2. call、internal 与 return 位置应能明确区分。
3. 若要借助 `WPDS` 查询，需要接受 `WALi` 的 weighted pushdown system 接口。
4. 若要附加程序分析信息，需要把状态级元数据放到 client-information 机制里。

### 不适用或高成本场景

如果对象只是普通 flat trace，`FA` 库可能更轻；如果对象是 arbitrary pushdown behavior 但没有 visible nesting discipline，`OpenNWA` 也不是最自然的直接工具。

## 与相邻形式主义的关系

相对 [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)，那篇是 `Nested Word Automata` 模型本体条目，`OpenNWA` 是其算法库和工程基础设施；相对 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)，`VPA` 从输入字母分区角度刻画同类结构化语言，`OpenNWA` 则采用 nested-word 表示与 `WALi` 接口；相对 [vata-a-library-for-efficient-manipulation-of-non-deterministic-tree-automata/desc.md](../vata-a-library-for-efficient-manipulation-of-non-deterministic-tree-automata/desc.md)，二者都服务结构化对象自动机，但 `VATA` 面向 tree automata，`OpenNWA` 面向 nested words。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示状态机建模不必只接受 flat event trace；有调用/返回或文档嵌套结构时，嵌套词对象更合适。
2. `NWA -> WPDS` 的接口说明一种形式主义可以通过转换接入另一类成熟分析后端。
3. example-word generation 对“验证 - 修复”闭环很重要，因为它能把空性失败转化成具体结构化反例。

### 作为目标形式主义还是中间表示

更适合作为结构化 trace / nested document / interprocedural analysis 的中间表示与算法后端，而不是控制工程师直接手写的前端状态机语言。

### 对需求到模型生成的启发

1. 若需求中存在“进入子流程后必须正确返回”这类匹配关系，生成器应考虑显式 nested relation。
2. 反例不应只是一条平面事件串，还可以保留 call-return 嵌套证据。
3. 后端基础设施可以通过 client information 把原需求片段、程序位置或状态机节点挂回自动机状态。

## 重要的相关工作

1. [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)：`Nested Word Automata` 本体与 nested-word theory。
2. [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)：visible-stack discipline 与 `VPA` 语言类。
3. [vata-a-library-for-efficient-manipulation-of-non-deterministic-tree-automata/desc.md](../vata-a-library-for-efficient-manipulation-of-non-deterministic-tree-automata/desc.md)：结构化对象自动机库的 tree-automata 对照。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Nested-Word Automata / OpenNWA / WALi`
- 论文角色：nested-word automata algorithm library and WALi/WPDS interoperability infrastructure
- 核心功能：把 `NWA` 的标准操作、空性、示例词生成与 `WALi` `WPDS` 查询做成可复用 `C++` 库
- 关键特性：call/internal/return transitions、call-predecessor state、client information、`NWA -> WPDS` conversion、example-word generation
- 构造方式：nested word / ICFG -> `OpenNWA` `NWA` object -> automata operations / `WPDS` query
- 基础设施：`OpenNWA`、`WALi`、`WPDS`、`C++` API、documentation
- 适用场景：程序调用返回分析、XML / nested document、结构化 trace 与 CEGAR example generation
- 需求前提：对象需有可见 call/internal/return 或等价不交叉 nesting relation
- 状态：🟢
