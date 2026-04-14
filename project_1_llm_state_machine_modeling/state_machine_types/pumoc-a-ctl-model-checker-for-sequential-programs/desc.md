# PuMoC：面向顺序程序的 CTL 模型检查器 / PuMoC: A CTL Model-Checker for Sequential Programs

## 基本信息

- 标题：PuMoC: A CTL Model-Checker for Sequential Programs
- 中文标题：PuMoC：面向顺序程序的 `CTL` 模型检查器
- 作者：Fu Song，Tayssir Touili
- 发表：*Proceedings of the 27th IEEE/ACM International Conference on Automated Software Engineering*，pp. 346-349，2012
- DOI：`10.1145/2351676.2351743`
- 链接：https://doi.org/10.1145/2351676.2351743
- 形式主义：`Pushdown Systems / ABPDS / CTL / PuMoC`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：💻 软件建模与程序行为
- 论文角色：`CTL` pushdown model-checking toolchain for `PDS` and sequential programs
- 工具/实现获取方式：原文明确给出下载入口 `http://www.liafa.jussieu.fr/~song/PuMoC`，并说明其与 `Moped` 集成；正文未给出稳定公开仓库 URL。
- 标准/格式获取方式：主承载是 `PDS`、`ABPDS`、`Moped/PDSolver` 语法、`Satabs` 输出的 boolean programs、`JimpleToPDSolver` 生成的 `PDS`；它不是中立交换标准。

## 简报

这篇论文补的是 pushdown-based software verification 的基础设施线。`PuMoC` 的关键价值不是重新定义 `PDS`，而是把“`CTL` 公式 + simple/regular valuations + `PDS`/顺序程序”真正做成一个可运行工具链：前端能吃 `PDS`、boolean programs、部分 `C/C++` 和 `Java`，核心把 `CTL` model checking 约化成 `ABPDS` 空性检查，后端再产出满足公式的 regular configuration sets。

- 形式主义定位：`PDS` 上的 `CTL` 模型检查基础设施，而不是新的 pushdown-state-machine 子类。
- 构造方式简述：`program / PDS + CTL -> ABPDS -> multi-automaton of satisfying configurations`。
- 基础设施与场景简述：依托 `Satabs`、`JimpleToPDSolver`、`Moped`、multi-automata 与 regular predicates，服务递归顺序程序、Windows driver、Java data-flow analysis。

```text
sequential program / PDS -> CTL + regular predicates -> ABPDS emptiness reduction -> accepted configuration set
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `PDS`，即 pushdown systems；
2. `ABPDS`，即 alternating Büchi pushdown systems；
3. `CTL` 及其 simple / regular valuations；
4. multi-automata，用于表示满足公式的无限配置集合；
5. `PuMoC`，即把这些对象串成工具链的实现。

### 核心抽象

论文把 pushdown system 写成：

$$
P = (P, \Gamma, \Delta)
$$

上式中的符号逐项解释如下：

1. 第一个 `$P$` 是 control locations 集合。
2. `$\Gamma$` 是 stack alphabet。
3. `$\Delta \subseteq (P \times \Gamma) \times (P \times \Gamma^\ast)$` 是规则集合。

配置写成：

$$
\langle p, \omega \rangle
$$

上式中的符号逐项解释如下：

1. `$p \in P$` 是当前控制位置。
2. `$\omega \in \Gamma^\ast$` 是当前栈内容。

一步 pushdown 转移满足：

$$
(p,\gamma,q,\omega) \in \Delta \Rightarrow \langle p,\gamma \omega' \rangle \leadsto_P \langle q,\omega \omega' \rangle
$$

上式中的符号逐项解释如下：

1. `$\gamma$` 是当前栈顶符号。
2. `$\omega'$` 是原有剩余栈内容。
3. `$\omega$` 是规则把栈顶替换出的新串。
4. 该规则体现了 `PDS` 的有限控制 + 栈顶重写语义。

为完成 `CTL` 检查，论文构造：

$$
BP = (P,\Gamma,\Delta,F)
$$

上式中的符号逐项解释如下：

1. `$BP$` 是 alternating Büchi pushdown system。
2. `$\Delta \subseteq (P \times \Gamma) \times 2^{P \times \Gamma^\ast}$` 现在变成 alternating 规则。
3. `$F$` 是 Büchi accepting control locations 集合。

### 一个最小例子与通俗解释

可以把 `PuMoC` 理解成“给递归程序装上 `CTL` 检查器”：

1. 假设某个程序点 `p` 表示“进入递归函数”，栈顶符号 `A` 表示当前调用上下文。
2. 若有规则把 `A` 改写成 `BA`，就相当于又压入了一层调用。
3. 如果我们要检查“从所有可达调用栈出发，最终总能回到某个安全返回点”，这就不是普通有限状态机能直接表达的。
4. `PuMoC` 通过 `ABPDS` 和 multi-automata 把这类带递归栈的 `CTL` 问题做成了工具。

通俗地说，`PDS` 像“带调用栈的有限状态机”；`PuMoC` 则是这个家族上的 `CTL` 检查器。

### 运行 / 接受 / 转移语义

论文给出 `CTL` 文法：

$$
\varphi ::= a \mid \neg a \mid \varphi \land \varphi \mid \varphi \lor \varphi \mid AX\varphi \mid EX\varphi \mid A[\varphi U \varphi] \mid E[\varphi U \varphi] \mid A[\varphi R \varphi] \mid E[\varphi R \varphi]
$$

上式中的符号逐项解释如下：

1. `$a$` 是 atomic proposition。
2. `$AX, EX$` 是一步后全称/存在时序算子。
3. `$U, R$` 分别是 until 与 release。

工具的核心约化可保守整理成：

$$
P \models \varphi \iff BP_{\varphi,P} \text{ has an accepting run}
$$

上式中的符号逐项解释如下：

1. `$P$` 是待验证的 pushdown system。
2. `$\varphi$` 是 `CTL` 公式。
3. `$BP_{\varphi,P}$` 是由公式与系统构造出的 `ABPDS`。
4. 该式说明 `CTL` 检查被规约成 `ABPDS` 的接受性 / 空性问题。

对 regular valuations，原子命题可依赖整个栈：

$$
\lambda_r : AP \to 2^{P \times \Gamma^\ast}
$$

上式中的符号逐项解释如下：

1. `$AP$` 是 atomic propositions 集合。
2. `$\lambda_r(a)$` 给出满足原子命题 `$a$` 的配置集合。
3. 这让命题不仅能看控制位置，也能看栈内容正则性质。

### 语义边界

1. 论文聚焦顺序程序与 `PDS`，不处理并发程序主线。
2. 时间约束、概率语义和连续动态都不在其问题范围内。
3. `PuMoC` 的优势在 branching-time `CTL`；`Moped` 负责 reachability / `LTL` 线。
4. regular valuations 很强，但仍然依赖可正则表示的栈性质。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PDS` 骨架 | `$P=(P,\Gamma,\Delta)$` | 工具的基本工作对象。 |
| 配置转移 | `$\langle p,\gamma\omega' \rangle \leadsto_P \langle q,\omega\omega' \rangle$` | 递归调用栈的基本动态。 |
| `ABPDS` 骨架 | `$BP=(P,\Gamma,\Delta,F)$` | `CTL` 检查的约化目标。 |
| regular valuations | `$\lambda_r : AP \to 2^{P \times \Gamma^\ast}$` | 允许原子命题依赖栈内容。 |
| 检查约化 | `$P \models \varphi \iff BP_{\varphi,P}\ \mathrm{has\ an\ accepting\ run}$` | 把 `CTL` model checking 变成 automata emptiness。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | control locations + unbounded stack 是核心。 |
| 事件 / 触发 | 中等支持 | 以规则触发为主，而非显式事件接口建模。 |
| 守卫 / 数据 | 中等支持 | 主要通过 regular predicates 与 program abstraction 表达。 |
| 层次 | 很强 | 调用-返回层次由栈天然提供。 |
| 并发 / 同步 | 不支持 | 面向顺序程序，不是并发 pushdown 系统平台。 |
| 时间约束 | 不支持 | 不是 timed pushdown line。 |
| 连续动态 / 随机性 | 不支持 | 纯离散递归程序验证。 |
| 可执行 / 可验证性 | 很强 | `CTL`、regular valuations、drivers / Java / data flow 都已工具化。 |

### 形式化问题与性质

1. 这篇论文的重要点是把 `CTL` 真正打进了 `PDS` 工具链，而不只停留在 `μ`-calculus 间接路线。
2. regular valuations 让命题能看“控制点 + 栈正则模式”，明显比只看控制位置更实用。
3. 与 `Moped` 的互补关系很明确：一边补 `CTL`，一边保留原有 `LTL` / reachability 能力。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 手写 `PDS`；
2. `Satabs` 生成的 boolean programs；
3. `JimpleToPDSolver` 从 `Java` 提取的 `PDS`；
4. `CTL` 公式和 regular predicates。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Moped/PDSolver` 风格的 `PDS` 语法；
2. `CTL` 公式；
3. regular expressions / multi-automata；
4. `ABPDS` 中间表示。

### 交换与互操作

1. `BP2PDS` 把 boolean programs 翻成 `PDS`。
2. `Regular Predicates Extractor` 处理栈上的正则谓词。
3. `PDS·CTL2ABPDS` 构造产品 `ABPDS`。
4. `MA Constructor` 生成满足公式的 multi-automaton。

## 配套基础设施

- 建模/编辑工具：前端支持 `Satabs`、`JimpleToPDSolver` 与手写 `PDS`。
- 解析/交换/元模型支持：`PDS` 语法、regular predicate 提取、multi-automata 构造。
- 仿真/执行支持：主线是模型检查，不是运行时执行器。
- 验证/分析支持：`CTL` 检查、regular valuations、Windows driver 批量检查、Java data-flow analysis。
- 代码生成/转换支持：支持从 boolean program / Java 中抽 `PDS`，但不负责部署代码生成。
- 标准化或社区生态：与 `Moped` 集成，并与 `PDSolver` 构成直接性能对照。

## 适用场景与需求前提

### 适用场景

适合递归顺序程序、驱动程序、函数调用明显且可抽成 pushdown 控制流的软件验证问题，以及需要把数据流分析写成 `CTL` 性质的场景。

### 需求前提

1. 目标系统应能抽象为 `PDS`。
2. 关键性质应能写成 `CTL`，必要时允许原子命题依赖栈的正则性质。
3. 程序应基本保持顺序控制流，而非大规模并发交互。
4. 若来自 `C/C++/Java`，前置抽象链路要可用。

### 不适用或高成本场景

1. 并发线程、实时约束或概率行为不是本文主线。
2. 若程序语义高度依赖复杂堆对象且难以抽象成 `PDS`，前处理成本会很高。
3. 若只需要 reachability / `LTL`，直接用 `Moped` 类工具可能更轻。

## 与相邻形式主义的关系

相对 `Moped` 这类偏 reachability / `LTL` 的 pushdown 工具，`PuMoC` 直接补上了 branching-time `CTL`；相对文库中的 `PDAAAL`，它不做 weighted reachability，而是做程序性质验证；相对 `OpenNWA` / nested-word 基础设施，它更贴近软件模型检查前线而不是 automata 算法库本身。

## 与本研究的关系

### 对 Project 1 的价值

它提供了一个重要提醒：若未来 `project_1` 需要处理带递归调用、子状态机嵌套或过程化控制逻辑，仅靠平面 `FSM` 可能不够，pushdown / recursive backend 是实际可用的验证落点之一。

### 可复用启发

1. 若需求文本里存在明显的 call-return / 子过程进入退出结构，可考虑输出递归状态机或 pushdown 近似而不是平面机。
2. `CTL + regular valuations` 说明性质端也可以依赖“栈模式”，不必只看当前状态名。
3. 递归控制流的验证后端不一定非要转 `μ`-calculus；`ABPDS` 约化是一条更贴近 automata 的实现路线。

## 重要的相关工作

1. `Moped`：提供 `PDS` 上的 reachability / `LTL` 能力，是 `PuMoC` 的直接补位对象。
2. `PDSolver`：`μ`-calculus 路线的对照基线。
3. `JimpleToPDSolver`：把 `Java` 程序抽成 `PDS` 的前端桥接。
4. `Satabs`：boolean program 前端，支撑 `C/C++` 进入本工具链。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：💻 软件建模与程序行为
- 结论：这篇论文最适合作为“pushdown 软件验证基础设施”条目保留。它不扩张新的状态机母型，但为递归控制逻辑提供了很清楚的 `CTL` backend 与工具落点。
