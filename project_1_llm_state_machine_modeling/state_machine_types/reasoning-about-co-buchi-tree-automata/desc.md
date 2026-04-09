# 关于 co-Büchi 树自动机的推理 / Reasoning About Co-Büchi Tree Automata

## 基本信息

- 标题：Reasoning About Co-Büchi Tree Automata
- 中文标题：关于 co-Büchi 树自动机的推理
- 作者：Salvatore La Torre, Aniello Murano
- 发表：收录于 *Theoretical Aspects of Computing -- ICTAC 2004*, LNCS 3407, pp. 527-542, 2005
- DOI：`10.1007/978-3-540-31862-0_37`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/cobuchi.ps
- 形式主义：`Co-Büchi Tree Automata / Alternating Generalized Co-Büchi Tree Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 tree automaton tuple、generalized co-Büchi acceptance 和 alternating transition function。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 generalized co-Büchi acceptance、alternating boolean transition formulas 和 parity reduction。

## 简报

这篇论文把 `co-Büchi tree automata` 从一句“Büchi 的对偶”真正整理成了一条可挂树的分支：它同时考虑 ordinary / generalized / alternating 三种视角，说明 `AGCTA` 如何刻画 generalized Büchi tree languages 的补类，并给出 emptiness 的复杂度边界。对当前文库而言，这正好能把 `Alternating Tree Automata` 母线下的 `Co-Büchi` 子枝稳定命名化。

- 形式主义定位：`Infinite-Tree Automata` 上的 co-Büchi / alternating acceptance 分支。
- 构造方式简述：先给标准 tree automaton tuple，再换用 generalized co-Büchi acceptance；若走 alternating 线，则把转移关系提升为 `B^+(K\times Q)` 上的布尔公式。
- 基础设施与场景简述：原文是纯理论 work，但模型、复杂度和与 parity automata 的关系都写得非常清楚，足以作为 `Co-Büchi Tree Automata / AGCTA` 的代表条目。

```text
generalized Büchi tree languages -> complement class -> co-Büchi / generalized co-Büchi -> alternating generalized co-Büchi -> parity reduction
```

## 形式主义定义与核心对象

### 定义对象

论文先回顾 ordinary tree automaton，再把接受条件换成 generalized co-Büchi。随后，它再把同一 acceptance family 提升到 alternating tree automata 上，形成 `AGCTA`。

### 核心抽象

标准 finite automaton on infinite trees 的骨架写成：

$$
A = \langle \Sigma, Q, Q_0, \delta, F \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入字母表。
2. `Q` 是有限状态集。
3. `Q_0 \subseteq Q` 是初始状态集。
4. `\delta \subseteq Q \times \Sigma \times Q \times Q` 是树自动机的转移关系。
5. `F` 是接受条件家族。

若 `r` 是 automaton 在输入树上的一条 run，`π` 是 run 上的一条路径，则 generalized co-Büchi condition 写成：

$$
\forall \pi\ \exists F_i \in F,\ \mathrm{Inf}(r/\pi) \subseteq F_i
$$

这里：

1. `\mathrm{Inf}(r/\pi)` 是沿路径 `\pi` 无限次出现的状态集合。
2. `F=\{F_1,\ldots,F_k\}` 是 accepting-state families。
3. 含义是：每条路径最终都必须稳定落在某个 `F_i` 之内。

对 alternating 版本，原文把转移函数提升为：

$$
\delta : Q \times \Sigma \to B^+(K \times Q)
$$

其中 `K=\{0,1\}` 是树分支方向集合，`B^+(K\times Q)` 是由 `(d,q)` 生成的正布尔公式集合。

### 一个最小例子与通俗解释

可以把 co-Büchi 直观理解成“坏状态只能出现有限次”。例如，一个最小模型可以要求：在每条分支上，状态 `q_{\mathrm{bad}}` 最终必须消失，只允许 `q_{\mathrm{good}}` 反复出现。此时接受家族可以写成 `F=\{\{q_{\mathrm{good}}\}\}`。

通俗地说，Büchi 是“好状态要无限次回来”，co-Büchi 则是“坏状态只能有限次出现，之后系统要稳定下来”。在树对象上，这个稳定性要求要对每一条无限分支都成立。

### 运行 / 接受 / 转移语义

对于 alternating tree automaton，论文给出如下直观语义：若

$$
\delta(q_0,a) = ((0,q_1)\lor(0,q_2)) \land ((0,q_3)\lor(1,q_2))
$$

那么在根节点读到 `a` 时，run 在下一层必须同时满足两组义务：

1. 左孩子上至少要出现 `q_1` 或 `q_2` 之一。
2. 还必须出现一个 `(0,q_3)` 或 `(1,q_2)` 的分支副本。

这说明 alternating co-Büchi tree automaton 同时具备：

1. branching obligations 的布尔组合能力；
2. eventual-stability 的 co-Büchi 接受能力。

### 语义边界

相对 ordinary Büchi tree automata，这条路线处理的是其补语言方向；相对 parity / Rabin tree automata，它使用的 acceptance family 更轻，但并不自动享有所有 simulation / closure 优势。

### 关键性质与判定边界

论文的关键结论包括：

1. `AGCTA` 与 `ACTA` 多项式等价：

$$
T(A') = T(A)
$$

2. `AGCTA` 的 emptiness 是 `\mathrm{Exptime}`-complete。

3. 任一 `AGCTA` 可以先转成 `ACTA`，再转成只有两个 parity sets 的 parity tree automaton。

4. 对 deterministic generalized Büchi complement class，可经 `\exists`-acceptance + generalized co-Büchi word automata 得到二次时间 emptiness 判定。

因此，这篇论文不是单纯的算法文章，而是把 co-Büchi / generalized / alternating 这三层 acceptance-family 关系真正压成了稳定的模型谱系。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制。 |
| 事件 / 触发 | 不适用一般事件流 | 核心是树节点标签和 branching direction。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据守卫。 |
| 层次 | 强支持 | 输入对象是 infinite tree。 |
| 并发 / 同步 | 强支持 | alternating transition 使用布尔组合施加并行义务。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 infinite-tree acceptance。 |
| 可执行 / 可验证性 | 强理论支持 | parity reduction、emptiness complexity、与 generalized Büchi complement 的关系都明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| tree automaton 骨架 | `$A=\langle \Sigma,Q,Q_0,\delta,F\rangle$` | infinite-tree automaton 的基本模型。 |
| generalized co-Büchi | `$\forall \pi\ \exists F_i\in F,\ \mathrm{Inf}(r/\pi)\subseteq F_i$` | 每条路径最终稳定在某个 accepting family 内。 |
| alternating 转移 | `$\delta:Q\times\Sigma\to B^+(K\times Q)$` | 把树分支义务写成正布尔公式。 |
| polynomial equivalence | `$T(A')=T(A)$` | `AGCTA` 可压回 `ACTA`。 |
| complexity | `$\mathrm{Emptiness}(\mathrm{AGCTA})$ is Exptime-complete` | co-Büchi alternating 分支的判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入树字母表和状态集。
2. 若只需 ordinary co-Büchi，则保留常规树自动机转移关系。
3. 若需 alternating 义务，则把转移改写成 `B^+(K\times Q)` 上的布尔公式。
4. 用 generalized co-Büchi family 表达“最终稳定在何类状态集合内”。

### 机器可处理承载方式

机器可处理承载方式是 automaton tuple、acceptance family 和 alternating transition formulas，而不是工程 DSL。

### 交换与互操作

它直接连到：

1. generalized Büchi tree automata 的 complement class；
2. alternating tree automata；
3. parity tree automata；
4. weak alternating / weak Muller / Landweber 等 acceptance-family 支线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 acceptance families 和 alternating formulas。
- 仿真/执行支持：可按 run tree 展开，但主要服务于理论分析。
- 验证/分析支持：emptiness、duality、parity reduction 和 language-class comparison。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 co-Büchi tree-acceptance 和 generalized / alternating 结合处的经典理论节点。

## 适用场景与需求前提

### 适用场景

适合表达“每条分支最终稳定避免坏状态”的 branching-time 性质，以及 generalized Büchi complement 方向的语言类分析。

### 需求前提

1. 对象必须是 infinite tree。
2. 性质更接近 eventual stability / finite-badness，而不是 repeated-goodness。
3. 若需要 alternating 紧凑表达，必须接受布尔化分支义务。

### 不适用或高成本场景

若只处理 ordinary finite words 或普通工程状态机，这条分支过于理论化。

## 与相邻形式主义的关系

相对 `Büchi tree automata`，它走的是 complement / eventual-stability 路线；相对 [alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md](../alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md)，这里是 alternating parity 母线下的 co-Büchi specialized branch；相对 [weak-muller-acceptance-conditions-for-tree-automata/desc.md](../weak-muller-acceptance-conditions-for-tree-automata/desc.md)，后者探索的是另一组对 Muller condition 的弱化。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树里长期缺失的 `Co-Büchi Tree Automata / AGCTA` 子枝稳定补出，同时也为后续继续补 full parity / full alternating tree automata 提供近邻节点。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点与 branching-time 中间表示。

### 对需求到模型生成的启发

当需求是“坏模式最终必须消失”而不是“好模式必须反复发生”时，co-Büchi 家族比 Büchi 表述更直接。

### 现实限制

没有工程工具与交换格式，主要服务于 acceptance-family 谱系和复杂度边界分析。

## 重要的相关工作

### 奠基或前身工作

- [alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md](../alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md)
- [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)

### 同类型或同家族工作

- generalized Büchi tree automata
- parity tree automata

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合挂成 `Alternating Tree Automata / Parity Tree Automata -> Co-Büchi Tree Automata / AGCTA` 的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Co-Büchi Tree Automata / Alternating Generalized Co-Büchi Tree Automata`
- 论文角色：分支整理
- 核心功能：整理 co-Büchi tree automata 与 generalized / alternating paradigms 的关系，并给出 `AGCTA` 的复杂度边界。
- 关键特性：generalized co-Büchi、alternating boolean transitions、parity reduction、Exptime-complete emptiness。
- 构造方式：tree automaton tuple + generalized co-Büchi acceptance + `B^+(K\times Q)` transition formulas。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：eventual-stability branching properties、generalized Büchi complement 分析。
- 需求前提：对象是 infinite tree，且性质更像“坏状态只允许有限次出现”。
- 状态：🟢
