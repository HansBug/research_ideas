# 树自动机的弱 Muller 接受条件 / Weak Muller Acceptance Conditions for Tree Automata

## 基本信息

- 标题：Weak Muller Acceptance Conditions for Tree Automata
- 中文标题：树自动机的弱 Muller 接受条件
- 作者：Salvatore La Torre, Aniello Murano, Margherita Napoli
- 发表：*Theoretical Computer Science*, 332(1-3):233-250, 2005
- DOI：`10.1016/j.tcs.2004.10.027`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/wmjournal.pdf
- 形式主义：`Landweber Tree Automata / Muller-Superset Tree Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是标准 tree automaton tuple 加两种新的 weak Muller acceptance conditions。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `TA` tuple、`Inf(r/\pi)` 与 Landweber / Muller-Superset 接受语义。

## 简报

这篇论文的关键动作是把 Muller acceptance 里的“等于某个 accepting set”拆成两个更弱的方向：

1. `Landweber`：路径上无限次出现的状态集合被某个 accepting set 包住。
2. `Muller-Superset`：某个 accepting set 被路径上无限次出现的状态集合包住。

这样一来，`Muller`、`Büchi`、`Landweber`、`Muller-Superset` 之间的关系就被系统地拉开了。对当前文库而言，它非常适合挂成 `Infinite-Tree Automata` 下 acceptance-family refinement 的稳定节点。

- 形式主义定位：`Infinite-Tree Automata` 上对 `Muller` 接受条件的两条弱化支线。
- 构造方式简述：保留标准 tree automaton 骨架，只替换路径接受谓词。
- 基础设施与场景简述：原文是纯理论模型，但 closure、size bound、emptiness 复杂度都讲得很清楚，足以直接支撑谱系节点建立。

```text
Muller equality condition -> subset relaxation / superset relaxation -> Landweber tree automata / Muller-Superset tree automata
```

## 形式主义定义与核心对象

### 定义对象

论文处理的底层骨架仍是 standard finite automata on infinite trees，只是把“路径上无限次出现的状态集合”与 accepting family 的关系从 equality 改成了 inclusion。

### 核心抽象

基本 tree automaton 仍写成：

$$
A = \langle Q, \Sigma, \delta, Q_0, F \rangle
$$

其中：

1. `Q` 是有限状态集。
2. `\Sigma` 是输入字母表。
3. `\delta` 是树自动机转移关系。
4. `Q_0` 是初始状态集。
5. `F=\{F_1,\ldots,F_m\}` 是 acceptance-family。

若 `r` 是 automaton 在树 `t` 上的一条 run，`\pi` 是 `r` 的一条路径，则两类新接受条件分别写成：

$$
\text{Landweber: }\forall \pi\ \exists F_i \in F,\ \mathrm{Inf}(r/\pi) \subseteq F_i
$$

$$
\text{Muller-Superset: }\forall \pi\ \exists F_i \in F,\ F_i \subseteq \mathrm{Inf}(r/\pi)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Inf}(r/\pi)` 是沿路径 `\pi` 无限次出现的状态集合。
2. `\subseteq` 的方向决定了“弱化”朝哪边发生。
3. Landweber 表示路径最终不会跑出某个 accepting family。
4. Muller-Superset 表示路径最终至少会反复访问某个 accepting family 的全部状态。

### 一个最小例子与通俗解释

论文中给出的 `T_2` 是一个很好的最小例子：

$$
T_2 = \{\, t \mid \forall \pi,\ a \notin \mathrm{Inf}(t/\pi)\ \lor\ b \notin \mathrm{Inf}(t/\pi) \,\}
$$

它要求每条分支最终只能“稳定偏向一边”：要么后面不再反复见到 `a`，要么后面不再反复见到 `b`。Landweber tree automaton 很自然地表达这种“最终稳定在某类状态集合里”的性质。

通俗地说，`Muller` 是“无限出现集合必须刚好等于某个模板”；`Landweber` 是“无限出现集合最后别跑出模板”；`Muller-Superset` 是“无限出现集合至少要覆盖某个模板”。

### 运行 / 接受 / 转移语义

这两条 acceptance line 的重点都不在新 run 结构，而在 `Inf(r/\pi)` 的判定方式。也就是说，automaton 仍按 ordinary tree run 展开，但在接受时改问：

1. 这条路径最后是不是被某个 accepting set 包住？
2. 或者，这条路径最后是不是至少完整覆盖了某个 accepting set？

因此它们天然适合作为 `Muller / Büchi / Rabin` 之间的 acceptance-family refinement，而不是一个全新树自动机骨架。

### 语义边界

相对 `Muller`，这两个模型更弱；相对 `Büchi`，`Muller-Superset` 与之同类但有时更 succinct；`Landweber` 则走出了与 `Büchi` 不可比的一条新路线。

### 关键性质与判定边界

论文给出的核心结论包括：

1. `BTA = STA`，也就是 Büchi tree automata 与 Muller-Superset tree automata 接受同一类语言。

2. 大小界：

$$
\mathrm{Size}_{STA}(T) \le \mathrm{Size}_{BTA}(T) \le (\mathrm{Size}_{STA}(T))^3
$$

3. 对 deterministic 情形，还有：

$$
\mathrm{Size}_{DSTA}(T) \le \mathrm{Size}_{DBTA}(T) \le 2^{O(\mathrm{Size}_{DSTA}(T))}
$$

4. `DLTA \subset LTA`，即 nondeterminism 严格增强 Landweber 模型的表达力。

5. `LTA` 的 emptiness 可在多项式时间内判定。

这些结果使它成为 acceptance-family 分支里非常“值得挂树”的节点：既有新模型，也有清晰的语言类关系和复杂度边界。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保持标准 finite-state tree automaton 骨架。 |
| 事件 / 触发 | 不适用一般事件流 | 输入是树标签和路径。 |
| 守卫 / 数据 | 不支持 | 原始模型不带一般变量守卫。 |
| 层次 | 强支持 | 对象是 infinite tree。 |
| 并发 / 同步 | 部分支持 | 多分支来自树对象本身，而不是进程同步。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 acceptance-family 模型。 |
| 可执行 / 可验证性 | 强理论支持 | size bounds、closure 和 polynomial emptiness 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle Q,\Sigma,\delta,Q_0,F\rangle$` | 仍沿用标准 tree automaton 骨架。 |
| Landweber 条件 | `$\forall \pi\ \exists F_i,\ \mathrm{Inf}(r/\pi)\subseteq F_i$` | 路径最终稳定在某个 accepting family 内。 |
| Muller-Superset 条件 | `$\forall \pi\ \exists F_i,\ F_i\subseteq \mathrm{Inf}(r/\pi)$` | 路径最终至少完整覆盖某个 accepting family。 |
| 语言类关系 | `$BTA = STA$` | Muller-Superset 与 Büchi 同类。 |
| nondeterminism gap | `$DLTA \subset LTA$` | Landweber 线上 nondeterminism 严格增 expressive power。 |
| emptiness | `$\mathrm{Emptiness}(LTA)\in \mathrm{Ptime}$` | Landweber acceptance 的主要算法优势。 |

## 构造方式与承载格式

### 建模入口

1. 先写标准 infinite-tree automaton 的状态与转移。
2. 明确要表达的是“被 accepting family 包住”还是“覆盖 accepting family”。
3. 若是前者，选 Landweber；若是后者，选 Muller-Superset。
4. 再根据需要选择 deterministic 还是 nondeterministic 分支。

### 机器可处理承载方式

机器可处理承载方式是 tree automaton tuple 和 `Inf(r/\pi)` 上的 acceptance predicate，而不是工程文件格式。

### 交换与互操作

它最直接连接：

1. Büchi tree automata。
2. Muller tree automata。
3. Landweber / generalized co-Büchi / co-Büchi acceptance 讨论。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是路径无限出现集合与 accepting families。
- 仿真/执行支持：可按 ordinary tree run 展开，但重点不是工程执行。
- 验证/分析支持：emptiness、closure、language-class comparison 和 succinctness bounds。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 infinite-tree acceptance-family 细分中的关键理论节点。

## 适用场景与需求前提

### 适用场景

适合 infinite-tree languages 中那些更接近“最终稳定”或“最终覆盖某组重复状态”的长期性质。

### 需求前提

1. 对象必须是 infinite tree。
2. 需求要关注路径上“无限次出现状态集合”的包含关系。
3. 若关心 tractable emptiness，Landweber 线尤其值得优先考虑。

### 不适用或高成本场景

若需求只需普通 Büchi 或更强的 full Muller / Rabin 条件，弱 Muller 线可能既不必要也不最自然。

## 与相邻形式主义的关系

相对 `Muller tree automata`，它是明确的 subset / superset relaxation；相对 `Büchi tree automata`，`Muller-Superset` 与其同类但可更 succinct；相对 [reasoning-about-co-buchi-tree-automata/desc.md](../reasoning-about-co-buchi-tree-automata/desc.md)，后者走的是 co-Büchi / generalized complement 线，而这篇走的是从 `Muller` 向两侧弱化的 acceptance-family 细分。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Infinite-Tree Automata` 下的 acceptance-family 细分从 `Rabin / Weak Alternating` 继续补到 `Landweber / Muller-Superset`，让 summary 里的 tree 分支不再只停在几类最常见条件。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和 acceptance-family 中间层。

### 对需求到模型生成的启发

当需求的长期行为更像“最终稳定在某类重复模式里”，弱 Muller 类接受条件可能比直接上 full Muller / Rabin 更贴切。

### 现实限制

没有工程工具线；主要服务于 infinite-tree acceptance 边界分析。

## 重要的相关工作

### 奠基或前身工作

- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)
- [finite-tree-automata-on-infinite-trees/desc.md](../finite-tree-automata-on-infinite-trees/desc.md)

### 同类型或同家族工作

- [reasoning-about-co-buchi-tree-automata/desc.md](../reasoning-about-co-buchi-tree-automata/desc.md)
- [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合挂成 `Infinite-Tree Automata` 下的 `Weak Muller / Muller-Superset / Landweber` acceptance-family 代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Landweber Tree Automata / Muller-Superset Tree Automata`
- 论文角色：模型提出
- 核心功能：把 Muller 接受条件拆成 Landweber 与 Muller-Superset 两条弱化支线，并给出语言类与复杂度关系。
- 关键特性：subset / superset acceptance、`BTA=STA`、`DLTA \subset LTA`、succinctness bounds、polynomial emptiness。
- 构造方式：标准 tree automaton tuple + `Inf(r/\pi)` 的包含型 acceptance predicate。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：infinite-tree acceptance-family 分析、eventual stability、tractable emptiness 场景。
- 需求前提：对象是 infinite tree，且长期性质可归约为 `Inf(r/\pi)` 与 accepting family 的包含关系。
- 状态：🟢
