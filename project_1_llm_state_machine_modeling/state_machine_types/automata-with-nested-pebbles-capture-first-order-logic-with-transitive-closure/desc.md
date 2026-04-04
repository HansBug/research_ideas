# 带嵌套卵石的自动机刻画带传递闭包的一阶逻辑 / Automata with Nested Pebbles Capture First-Order Logic with Transitive Closure

## 基本信息

- 标题：Automata with Nested Pebbles Capture First-Order Logic with Transitive Closure
- 中文标题：带嵌套卵石的自动机刻画带传递闭包的一阶逻辑
- 作者：Joost Engelfriet, Hendrik Jan Hoogeboom
- 发表：*Logical Methods in Computer Science*, 3(2:3):1-27, 2007
- DOI：`10.2168/LMCS-3(2:3)2007`
- 链接：https://lmcs.episciences.org/2220
- 形式主义：`Nested-Pebble Tree-Walking Automata / k-Head Tree-Walking Pebble Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：逻辑刻画
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 automaton 元组 `A=(Q,\Sigma,X,q_0,A,I)`、head positions、pebble stack 和 instruction semantics。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 ranked tree、测试/移动/pebble 指令和 configuration 语义。

## 简报

这篇论文把 `Tree-Walking Automata` 向前推进成“多头 + 嵌套卵石 + 可远程取回”的 sequential tree machine，并证明它与带 `k` 元 deterministic transitive closure 的一阶逻辑精确对应。它的价值不只是多了一个 pebble 技巧，而是把 `Tree-Walking` 支线从局部导航模型提升成了一个能稳定承接 descriptive complexity、XML/tree query 和后续 pebble/alternating 变体的母节点。

- 形式主义定位：`Tree-Walking Automata` 的 nested-pebble 增强版，是 sequential tree machine 与 `FO + DTC` 之间的桥节点。
- 构造方式简述：机器在 ranked tree 上移动 `k` 个 heads，可按 LIFO 方式 drop/retrieve pebbles，并用标签测试、child-number 测试和移动/pebble 指令组织计算。
- 基础设施与场景简述：原文是纯理论工作，但直接连到 `FO + DTC_k`、searchable graph families、XML/unranked tree walking 与 tree query 理论。

```text
有序树 / 图结构 -> 多头 tree-walking + nested pebbles -> configuration 语义 -> 逻辑刻画 / 表达力分析
```

## 形式主义定义与核心对象

### 定义对象

原文关注的是 ranked tree 上的顺序行走式自动机。与 bottom-up tree automata 不同，这类机器始终靠有限控制和当前位置来工作；与普通 `TWA` 相比，这里再加入了多头和嵌套 pebble，用来临时记住树中的关键节点。

### 核心抽象

原文把 `k-head tree-walking pebble automaton` 定义为：

$$
A = (Q,\Sigma,X,q_0,A,I)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是 ranked input alphabet。
3. `X` 是有限 pebble 集合。
4. `q_0 \in Q` 是初始状态。
5. `A \subseteq Q` 是接受状态集。
6. `I` 是有限 instruction 集合。

原文给出的 instruction 由状态、操作或测试共同组成，核心动作包括：

$$
\mathrm{up}_i,\ \mathrm{down}_{i,j},\ \mathrm{drop}_i(x),\ \mathrm{retrieve}(x)
$$

以及测试：

$$
\mathrm{lab}_{i,\sigma},\ \mathrm{peb}_i(x),\ \mathrm{chno}_{i,j}
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{up}_i` 表示第 `i` 个 head 向父节点移动。
2. `\mathrm{down}_{i,j}` 表示第 `i` 个 head 向第 `j` 个孩子移动。
3. `\mathrm{drop}_i(x)` 表示把 pebble `x` 丢在第 `i` 个 head 当前所在节点。
4. `\mathrm{retrieve}(x)` 表示取回最近一次丢下的 pebble `x`。
5. `\mathrm{lab}_{i,\sigma}` 测试第 `i` 个 head 所在节点标签是否为 `\sigma`。
6. `\mathrm{peb}_i(x)` 测试第 `i` 个 head 当前节点上是否可见 pebble `x`。
7. `\mathrm{chno}_{i,j}` 测试当前节点是不是其父节点的第 `j` 个孩子。

原文最关键的约束是 pebble 的 lifetime 必须 nested；也就是说只有最后 drop 的 pebble 才能先被 retrieve。不过这些 pebbles 不是“必须回到原位置才能拿起”的 physical marker，而是可远程取回的 abstract marker。

### 一个最小例子与通俗解释

原文给出的例子，是检查某类叶节点到根路径上 branching nodes 的奇偶性。机器先把第一个 pebble 放在一个 `a`-leaf 上，再沿路径向上走；为了判断某个祖先节点是否 branching，会暂时把第二个 pebble 放在该节点上，并遍历“另一棵子树”看看是否也有 `a`-leaf。

通俗地说，这类模型像“会在树上巡逻、还能在若干关键位置插书签的单人检查员”。普通 `TWA` 只能靠有限状态记住极少上下文；nested pebbles 则允许它把某些节点地址临时压栈保存，稍后再回来利用。

### 运行 / 接受 / 转移语义

原文把 configuration 写成：

$$
[p,u,\alpha]
$$

上式中的符号逐项解释如下：

1. `p \in Q` 是当前状态。
2. `u` 是 `k` 个 head 当前所在节点组成的元组。
3. `\alpha` 是当前已放下 pebble 的 stack，记录 pebble 名和节点位置。

在输入树 `t` 上，接受语义可写成：

$$
L(A) = \{ t \in T_\Sigma \mid [q_0,\mathrm{root},\epsilon] \vdash^*_{A,t} [p,\mathrm{root},\epsilon],\ p \in A \}
$$

上式中的符号逐项解释如下：

1. `T_\Sigma` 是 `\Sigma` 上的所有 ranked trees。
2. `\mathrm{root}` 表示所有 heads 都从树根出发并最终回到树根。
3. `\epsilon` 表示开始和结束时都没有遗留 pebble。
4. `\vdash^*_{A,t}` 是在树 `t` 上由 instruction 诱导的多步计算关系。

### 语义边界

相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)，这里多了多头和 nested pebbles；相对 unrestricted pebbles，它又刻意保留 LIFO 约束，避免直接膨胀到 `\mathrm{DSPACE}(\log n)` 级别；相对 bottom-up tree automata，它仍然是单条路径上的 sequential machine，而不是并行子树汇总器。

### 关键性质与判定边界

原文最核心的逻辑刻画结论是：

$$
\mathrm{DPW}_k\mathrm{A} = \mathrm{FO} + \mathrm{DTC}^k
$$

$$
\mathrm{NPW}_k\mathrm{A} = \mathrm{FO} + \mathrm{posTC}^k
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{DPW}_k\mathrm{A}` 是 deterministic `k`-head nested-pebble tree-walking automata 所定义的树语言类。
2. `\mathrm{NPW}_k\mathrm{A}` 是其 nondeterministic 版本。
3. `\mathrm{FO}` 是一阶逻辑。
4. `\mathrm{DTC}^k` 是 `k` 元 deterministic transitive closure。
5. `\mathrm{posTC}^k` 是只允许正出现的 `k` 元 transitive closure。

对当前文库尤其重要的是 `k=1` 的树情形，它把单头 nested-pebble `TWA` 精确放到了 `FO` 与更强树逻辑之间，为后续 `PATWA`、XML/unranked 方向和 searchable graph families 留出了稳定接口。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制仍是主骨架。 |
| 事件 / 触发 | 不适用 | 输入是静态树，不是事件流。 |
| 守卫 / 数据 | 部分支持 | 支持标签、child number 和 pebble 可见性测试。 |
| 层次 | 强支持 | 对象天然是树，层次结构是核心语义。 |
| 并发 / 同步 | 不支持 | 不是并发模型，但可用多头协调遍历。 |
| 时间约束 | 不支持 | 纯离散树机器。 |
| 连续动态 / 随机性 | 不支持 | 无连续演化或概率。 |
| 可执行 / 可验证性 | 强理论支持 | 有明确 configuration 语义和逻辑刻画。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,\Sigma,X,q_0,A,I)$` | nested-pebble tree-walking automaton 的标准骨架。 |
| 配置 | `$[p,u,\alpha]$` | 运行状态由控制状态、多头位置和 pebble stack 组成。 |
| 接受语义 | `$[q_0,\mathrm{root},\epsilon]\vdash^*_{A,t}[p,\mathrm{root},\epsilon]$` | 从根出发、回到根并清空 pebbles 后接受。 |
| 逻辑刻画 | `$\mathrm{DPW}_k\mathrm{A}=\mathrm{FO}+\mathrm{DTC}^k$` | 多头 nested pebbles 与 `k` 元 deterministic transitive closure 对齐。 |
| 非确定性版本 | `$\mathrm{NPW}_k\mathrm{A}=\mathrm{FO}+\mathrm{posTC}^k$` | nondeterminism 对应 positive transitive closure。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入对象是 ranked tree 或其等价图结构。
2. 再确定需要几个 heads，以及哪些节点必须用 pebbles 临时记住。
3. 为标签测试、child-number 测试、移动和 pebble 操作设计 instruction 集。
4. 最后为 configuration 和接受状态给出语义。

### 机器可处理承载方式

机器可处理承载方式本质上是状态机图、instruction 集和 configuration 语义，而不是 XML/JSON/DSL 文件。

### 交换与互操作

它与 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md) 的普通 `TWA` 直接相连，也与 [pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md](../pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md) 的 alternating pebble 变体、以及 [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md) 的 tree-walking machine 支线形成旁系关系。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 ranked tree、instruction set 和 configuration 语义。
- 仿真/执行支持：可按 instruction 对 tree configuration 直接解释执行。
- 验证/分析支持：逻辑刻画、表达力对比、tree/graph family 可搜索性分析是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 tree-walking / descriptive complexity / XML tree theory 的经典理论节点。

## 适用场景与需求前提

### 适用场景

适合树查询、XML/半结构化文档导航、顺序 tree processing 以及“有限控制 + 少量书签”足以表达的树语言理论分析。

### 需求前提

1. 对象必须天然是树，或至少是 searchable graph family。
2. 需求更像顺序导航加局部记忆，而不是 bottom-up 并行汇总。
3. 允许用少量 nested pebbles 记录关键节点位置。

### 不适用或高成本场景

若需求需要一般数据变量、时间约束、概率或并发资源流，这个模型就不合适；若需要工程交换格式，它也没有直接载体。

## 与相邻形式主义的关系

相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)，它增加了多头和 nested pebbles；相对 [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md) 的 `CT-PD`，它没有显式 pushdown 输出/存储机语义，而是更偏 recognizer / logic-characterization；相对 [pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md](../pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md)，它还没有 alternation。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Tree-Walking Automata` 下面的 nested-pebble 母节点正式补出来，使树行走分支不再只有“无 pebble”与“交替 pebble”两端，而有了中间的经典承接层。

### 作为目标形式主义还是中间表示

更适合作为谱系节点、理论参照或特定树结构需求的中间表示，而不是控制系统主线的最终输出形式。

### 对需求到模型生成的启发

如果需求文本本身就隐含“沿树导航并暂存若干关键位置”的处理逻辑，LLM 先生成 nested-pebble `TWA` 可能比直接生成更重的 tree transducer 或 bottom-up automaton 更自然。

### 现实限制

它几乎没有工程生态，核心价值仍然在理论谱系和表达力边界，不适合作为项目中的直接执行格式。

## 重要的相关工作

### 奠基或前身工作

- [tree-acceptors-and-some-of-their-applications/desc.md](../tree-acceptors-and-some-of-their-applications/desc.md)
- [tree-automata/desc.md](../tree-automata/desc.md)
- [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)

### 同类型或同家族工作

- [pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md](../pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md)
- [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里 `Tree-Walking Automata` 下的 `Nested-Pebble` 母节点，并为后续 `PATWA`、XML/tree query 和 graph-walking 方向留接口。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Nested-Pebble Tree-Walking Automata / k-Head Tree-Walking Pebble Automata`
- 论文角色：逻辑刻画
- 核心功能：用多头 tree-walking + nested pebbles 精确刻画 `FO + DTC` 的树语言能力。
- 关键特性：多头导航、nested pebbles、远程 retrieve、configuration 语义、`FO + DTC` 逻辑对应。
- 构造方式：`(Q,\Sigma,X,q_0,A,I)` 元组加 instruction 集与 pebble-stack 语义。
- 基础设施：纯理论模型，无工程标准或工具。
- 适用场景：树查询、XML/tree navigation 理论、sequential tree machine 表达力分析。
- 需求前提：对象是树或 searchable graph family，且需求可由顺序导航加少量位置书签表达。
- 状态：🟢
