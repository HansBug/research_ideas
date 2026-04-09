# 交替树自动机、奇偶博弈与模态 μ-演算 / Alternating Tree Automata, Parity Games, and Modal $\mu$-Calculus

## 基本信息

- 标题：Alternating Tree Automata, Parity Games, and Modal $\mu$-Calculus
- 中文标题：交替树自动机、奇偶博弈与模态 μ-演算
- 作者：Thomas Wilke
- 发表：*Bulletin of the Belgian Mathematical Society - Simon Stevin*, 8(2):359-391, 2001
- DOI：`10.36045/bbms/1102714178`
- 链接：https://lat.inf.tu-dresden.de/teaching/ws2007-2008/seminar/wilke.pdf
- 形式主义：`Alternating Tree Automata / Alternating Parity Tree Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 alternating tree automaton 的四元组、transition conditions 和 parity priorities。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `A=(S,s_I,\delta,\Omega)`、run tree 和 parity-game reduction。

## 简报

这篇论文不是 alternating tree automata 的最早提出文献，但它给出了一个非常干净、适合继续扩树的 canonical model：状态、transition condition、priority function、run 以及 parity acceptance 都被整理得非常稳定。对当前文库而言，它最直接的价值是把 `Alternating Tree Automata / Alternating Parity Tree Automata` 这条 acceptance-family 主干明确挂出来，并为 `Weak Alternating`、`Co-Büchi` 与后续 full parity 分支提供统一母语。

- 形式主义定位：`Tree Automata -> Infinite-Tree Automata` 上的 alternating / parity 语义主线。
- 构造方式简述：状态不再只给单个后继，而是给出关于当前命题、后继状态和分支选择的 transition condition；接受由 priority function 在 run branch 上的奇偶条件决定。
- 基础设施与场景简述：原文虽以 modal `\mu`-calculus 为动机，但交替树自动机本体、acceptance、index 和 parity-game reduction 都整理得足够自洽，完全可以作为独立模型条目入树。

```text
branching transition systems / trees -> alternating tree automaton -> parity acceptance -> parity games -> model checking / satisfiability
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象是带命题标记的 branching structure。它并不把 automaton 固定在某种窄化的 ranked-tree 编码上，而是直接让模型在 pointed Kripke structure / tree 上运行，这也是它能自然处理任意 branching 的原因。

### 核心抽象

原文的 alternating tree automaton 定义为：

$$
A = (S, s_I, \delta, \Omega)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `s_I \in S` 是初始状态。
3. `\delta` 是 transition function，把每个状态映射到一个 transition condition。
4. `\Omega : S \to \mathbb N` 是 priority function，为每个状态分配奇偶优先级。

transition conditions 由下列语法生成：

$$
0,\ 1,\ q,\ \neg q,\ s,\ \Diamond s,\ \Box s,\ s \land s',\ s \lor s'
$$

这里：

1. `q` 与 `\neg q` 检查当前节点是否满足某个命题变量。
2. `s` 表示在当前节点继续用状态 `s` 检查。
3. `\Diamond s` 表示把一个副本发送到某个后继节点并转入状态 `s`。
4. `\Box s` 表示对所有后继节点都必须放一个状态 `s` 的副本。
5. `\land / \lor` 分别对应 universal / existential branching。

### 一个最小例子与通俗解释

一个极小例子是“从当前节点出发，沿某条分支最终能到达满足 `q_0` 的节点”。可以取一个状态 `s`，并定义：

$$
\delta(s) = q_0 \lor \Diamond s
$$

通俗地说，这个 automaton 每到一个节点就做两件事中的一件：

1. 要么立刻检查“这里是不是已经满足 `q_0`”；
2. 要么把自己发到某个子节点继续找。

如果把 `\lor` 换成 `\land`，模型就会从“存在一条可行分支”切换成“所有分支都要继续满足”。这正是 alternation 在树对象上的直观意义。

### 运行 / 接受 / 转移语义

原文把 run 定义为一个标记在原结构之上的 run tree：

$$
R = (V^R, E^R, \lambda^R)
$$

其中每个 run-node 的标签是一个二元组 `(w,s)`，表示“在原结构节点 `w` 上，以 automaton 状态 `s` 继续检查”。接受条件是：每一条无限 run-branch 都必须满足 parity condition。

若 `\pi` 是 run tree 的一条无限分支，则接受条件可写成：

$$
\sup(\Omega \circ \pi^1) \text{ is even}
$$

上式中的符号逐项解释如下：

1. `\pi^1` 表示从 branch `\pi` 中抽取状态分量。
2. `\Omega \circ \pi^1` 是沿该分支看到的 priority 序列。
3. `\sup` 表示其中“无限次出现的优先级里的最大值”。
4. 该最大值为偶数时，此分支接受。

### 语义边界

相对 nondeterministic tree automata，这个模型把 branching mode 推进到了真正的 alternating semantics；相对 Rabin / Muller 线，它强调的是“简单统一的 parity acceptance + game semantics”，而不是更重的 pair / family acceptance 结构。

### 关键性质与判定边界

原文给出的关键结构包括：

1. 和 modal `\mu`-calculus 的等价性：

$$
\llbracket \varphi \rrbracket = \llbracket A(\varphi) \rrbracket
$$

2. index 定义：

$$
\mathrm{ind}(A) = \max_C m_C^A
$$

其中 `m_C^A` 是某个 strongly connected component 中用到的 priority 数。

3. model checking / nonemptiness 都可以约化到 parity games。

这意味着 alternating tree automata 不只是“another tree automaton variant”，而是一个和 fixed-point logics 深度互通的核心模型。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制，外加 priority function。 |
| 事件 / 触发 | 部分支持 | 主要由当前节点命题标记和 branching relation 触发。 |
| 守卫 / 数据 | 不支持一般数据 | 命题检查是核心，但没有一般变量守卫。 |
| 层次 | 强支持 | 输入对象天然是树 / branching structure。 |
| 并发 / 同步 | 强支持 | `\land` / `\Box` 直接带来逻辑并行分支。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 branching model。 |
| 可执行 / 可验证性 | 强支持 | acceptance、nonemptiness、model checking 都可转成 parity-game 问题。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(S,s_I,\delta,\Omega)$` | alternating tree automaton 的标准骨架。 |
| transition condition | `$\delta(s)\in\{0,1,q,\neg q,s,\Diamond s,\Box s,\land,\lor\}$` | 当前节点上的局部检查和 branching 规则。 |
| run tree | `$R=(V^R,E^R,\lambda^R)$` | automaton 在 branching structure 上的展开。 |
| parity acceptance | `$\sup(\Omega\circ\pi^1)$ even` | 每条无限分支上的奇偶接受。 |
| 逻辑等价 | `$\llbracket \varphi \rrbracket=\llbracket A(\varphi)\rrbracket$` | 与 modal `\mu`-calculus 完全对齐。 |

## 构造方式与承载格式

### 建模入口

1. 先确定要检查的 branching structure / tree 上有哪些原子命题。
2. 列出 automaton 状态及其对应的局部检查任务。
3. 为每个状态写 transition condition。
4. 用 priority function 指定 fixed-point / acceptance 层级。

### 机器可处理承载方式

机器可处理承载方式是状态、transition conditions、priority function 和 run tree，而不是工程文件格式。

### 交换与互操作

它最直接互操作到：

1. modal `\mu`-calculus。
2. parity games。
3. weak / co-Büchi / parity 等接受条件子族。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 automaton tuple 与 parity-game reduction。
- 仿真/执行支持：可在 pointed Kripke structures 上展开 run tree。
- 验证/分析支持：model checking、satisfiability、acceptance、nonemptiness 都有标准 reduction。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 automata + games + modal fixed-point logics 三线汇合处的经典节点。

## 适用场景与需求前提

### 适用场景

适合 branching-time properties、fixed-point specifications、tree / transition-system satisfiability 和 parity-game style reasoning。

### 需求前提

1. 对象应当天然是 branching structure 或 tree unfolding。
2. 性质能写成局部命题检查与后继分支组合。
3. 能接受 parity 作为长期接受语义。

### 不适用或高成本场景

若对象只是普通有限词语言，或需求主要是工程执行状态机，则这类 alternating parity tree automaton 往往过重。

## 与相邻形式主义的关系

相对 [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)，这里给的是 full alternating / parity 母线；相对 [reasoning-about-co-buchi-tree-automata/desc.md](../reasoning-about-co-buchi-tree-automata/desc.md)，后者是在 co-Büchi 接受条件下的 specialized alternating branch；相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，这里更强调 alternating + parity + games，而不是 Rabin 的 pair-family acceptance。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata -> Infinite-Tree Automata` 上的 `Alternating Tree Automata / Parity Tree Automata` 节点稳定命名化，是当前 summary 演化树最需要补实的一段主干。

### 作为目标形式主义还是中间表示

更适合作为理论中间层和谱系节点，不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

当需求本质上是 branching-time / fixed-point 性质时，可以先生成 alternating / parity 样式的中间模型，再决定是否回落到更具体的 acceptance family。

### 现实限制

没有工程交换格式；更偏 verification logic 和 infinite-structure reasoning。

## 重要的相关工作

### 奠基或前身工作

- [alternation/desc.md](../alternation/desc.md)
- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)

### 同类型或同家族工作

- [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)
- [reasoning-about-co-buchi-tree-automata/desc.md](../reasoning-about-co-buchi-tree-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合挂成 `Tree Automata -> Infinite-Tree Automata -> Alternating Tree Automata / Alternating Parity Tree Automata` 的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Alternating Tree Automata / Alternating Parity Tree Automata`
- 论文角色：分支整理
- 核心功能：给出适配 branching structures 的 alternating tree automaton canonical model，并用 parity games 统一处理 acceptance / nonemptiness / model checking。
- 关键特性：transition conditions、run tree、priority function、parity acceptance、与 modal `\mu`-calculus 等价。
- 构造方式：`A=(S,s_I,\delta,\Omega)` + run tree `R=(V^R,E^R,\lambda^R)`。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：branching-time verification、modal fixed-point logic、parity-game reductions。
- 需求前提：对象是 branching structure / tree，性质能写成局部命题与后继分支的交替组合。
- 状态：🟢
