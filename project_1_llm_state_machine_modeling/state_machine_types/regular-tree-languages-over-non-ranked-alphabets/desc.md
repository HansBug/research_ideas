# 非定秩字母表上的正则树语言 / Regular tree languages over non-ranked alphabets

## 基本信息

- 标题：Regular tree languages over non-ranked alphabets
- 中文标题：非定秩字母表上的正则树语言
- 作者：Anne Brüggemann-Klein, Derick Wood
- 发表：版本 `0.3` 手稿，1998-04-19
- DOI：原文未提供
- 链接：https://www.coverpages.org/regTreeLanguages-ps.gz
- 形式主义：Unranked Tree Automata / Tree-Regular Languages over Non-Ranked Alphabets
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `2NTA / NATA / NDTA / DATA / DDTA` 的定义和 child-state regular language transitions。
- 标准/格式获取方式：没有工程标准，核心承载方式是 non-ranked tree terms、regular child-state languages 和 top congruence。

## 简报

这篇手稿是 unranked / non-ranked tree automata 方向上非常关键的一步：它不再要求每个标签有固定 arity，而是把“一个节点的孩子状态序列属于某个 regular language”作为转移条件，从而把 tree automata 从 ranked alphabets 推广到了 finite-but-unbounded branching 的对象上。对当前演化树来说，这正是 `Tree Automata -> unranked` 这条缺口上的母节点。

- 形式主义定位：普通 ranked tree automata 向 unranked trees 推广后的经典总纲。
- 构造方式简述：用 `2NTA` 统一描述双向、上行、下行树自动机，再把 tree-regular languages 固定到 `NATA` 识别类上。
- 基础设施与场景简述：原文纯理论，但直接面向 XML / derivation trees 这类“分支数无固定上界”的对象。

```text
unranked tree -> regular child-state string condition -> tree automaton run -> tree-regular language
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象是 non-ranked trees：节点标签来自有限字母表，但每个节点的孩子数不预先固定。也因此，转移不再是 ranked tree automata 里那种固定元数的局部规则，而是关于“孩子状态串”的 regular language 条件。

### 核心抽象

原文首先定义 two-way nondeterministic tree automaton：

$$
M = (Q,\delta,F)
$$

其中：

$$
\delta \subseteq \Sigma \times Q^* \times Q \times \{u,d,s\}
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是 non-ranked alphabet。
3. `Q^*` 表示节点所有孩子对应的状态串。
4. `u,d,s` 分别表示向上、向下、停留三类移动方向。
5. `F` 是接受状态集。

在此基础上，原文把 ascending tree automata 进一步收束为主干模型。对 nondeterministic ascending tree automaton (`NATA`)，一个转移可以理解为：在某个标签为 `a` 的节点，若其孩子根部状态序列落在某个 regular language 中，则该节点可以归约到状态 `q`。

论文把 tree-regular language 明确定义为：

$$
T \text{ is tree-regular } \iff T \text{ is recognizable by a tree automaton, i.e. a NATA}
$$

### 一个最小例子与通俗解释

一个最小例子是：识别“根为 `a`，所有孩子都是 `b`-leaf，且孩子个数任意”的树。对 unranked automaton 来说，不需要给 `a` 预先规定固定 arity，只要给出一个 regular child-state language，例如“若所有孩子都处在 `q_b`，则根可归到 `q_a`”，就能同时覆盖 `a(b)`, `a(bb)`, `a(bbb)` 等任意分支数情形。

通俗地说，普通 ranked tree automata 像“只会处理固定参数个数的函数符号”；这篇 paper 的 unranked 版本则更像“节点先把所有孩子状态排成串，再用一个字符串自动机检查这串状态是否合法”。

### 运行 / 接受 / 转移语义

对 `NATA` 而言，节点的局部接受由孩子状态串是否属于某个 regular language 决定。论文中与之对应的 deterministic ascending 结果可概括为：

$$
\text{ascending nondeterministic} \equiv \text{ascending deterministic}
$$

更具体地，Theorem B 给出：

$$
\text{Every tree-regular language is recognizable by an ascending deterministic tree automaton}
$$

同时，Theorem A 给出：

$$
\text{ascending nondeterministic} \equiv \text{descending nondeterministic}
$$

但对 deterministic top-down 路线，Theorem C 明确指出：

$$
\text{DDTA} \subsetneq \text{tree-regular languages}
$$

也就是说：

1. nondeterministic 上行 / 下行等价；
2. 上行 deterministic 仍然完整；
3. 下行 deterministic 更弱。

### 语义边界

相对 ranked tree automata，它的增强点是“无固定 arity”；相对 hedge automata，它仍主要在“树”而不是“森林 / hedge”层面给出 general theory；相对 XML schema 语言，它还停留在 automata 母型，不涉及具体 schema 语法。

### 关键性质与判定边界

论文最关键的结构性结论之一是 top congruence characterization：

$$
t_1 \equiv_T t_2
\iff
\forall t \in T_{\Sigma,X},\ t \cdot t_1 \in T \Leftrightarrow t \cdot t_2 \in T
$$

在 unranked setting 中，这还不够，作者又引入了水平方向的等价：

$$
t_1 \equiv^h_T t_2
\iff
\forall t \in T_\Sigma^a,\ t_1 \mathbin{\|} t \in T \Leftrightarrow t_2 \mathbin{\|} t \in T
$$

并借此证明 finite top index + local views 可刻画 tree-regularity。对演化树而言，这说明 unranked tree automata 不是 ranked 情况的简单拷贝，而是多了一层“horizontal language”结构。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态控制。 |
| 事件 / 触发 | 不适用 | 输入对象是树。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据守卫。 |
| 层次 | 强支持 | 层次来自 unranked tree 本体。 |
| 并发 / 同步 | 不支持 | 不是并发过程模型。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树语言。 |
| 可执行 / 可验证性 | 强支持 | recognizability、最小化、congruence characterization 都很完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 2NTA 骨架 | `$M=(Q,\delta,F)$` | non-ranked setting 下的最一般双向骨架。 |
| 转移表 | `$\delta \subseteq \Sigma \times Q^* \times Q \times \{u,d,s\}$` | 节点局部规则依赖孩子状态串。 |
| tree-regular 定义 | `$T$ recognizable by a NATA` | 语言类主定义。 |
| 上行确定化 | `$\text{NATA} \equiv \text{DATA}$` | Theorem B。 |
| 下行确定性更弱 | `$\text{DDTA} \subsetneq \text{tree-regular}$` | Theorem C。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先确定对象是 finite but unbounded branching tree；
2. 给出节点标签字母表；
3. 为每个标签定义关于孩子状态串的 regular condition；
4. 选择上行 / 下行、确定 / 非确定模型。

### 机器可处理承载方式

机器可处理承载方式是：

1. tree terms；
2. child-state regular languages；
3. congruence classes 和 local views。

### 交换与互操作

它直接连到：

1. ranked tree automata；
2. hedge / forest automata；
3. XML document trees；
4. derivation trees of grammars with regular right-hand sides。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程交换格式。
- 仿真/执行支持：可按 automaton run 定义，但主价值在 recognizability。
- 验证/分析支持：determinization、最小化、congruence characterization 很强。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：为后续 XML / hedge / deterministic-unranked 方向提供母体。

## 适用场景与需求前提

### 适用场景

适用于 derivation trees、XML-like 文档树、节点分支数不固定的层次对象以及任何需要 unranked tree regularity 的场景。

### 需求前提

1. 对象必须天然是树而不是线性序列。
2. 节点分支数有限但无固定上界。
3. 可用孩子状态串的 regular condition 描述局部约束。

### 不适用或高成本场景

若对象本质上是 hedge / forest 序列，或者需要 XML schema 的工程语法层，后续 `Hedge Automata` 更直接。

## 与相邻形式主义的关系

相对 [tree-automata/desc.md](../tree-automata/desc.md)，它把 ranked tree automata 推到了 non-ranked alphabets；相对 [hedge-automata-a-formal-model-for-xml-schemata/desc.md](../hedge-automata-a-formal-model-for-xml-schemata/desc.md)，它是更一般、更基础的 unranked tree 母型；相对 [deterministic-automata-on-unranked-trees/desc.md](../deterministic-automata-on-unranked-trees/desc.md)，后者进一步专门刻画 deterministic 子线。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata -> unranked` 这条树枝补成了真正可命名的主节点，而不是只靠 survey 或 XML 侧说明。

### 作为目标形式主义还是中间表示

更适合作为理论母型和树枝节点；当需求对象就是文档树或 derivation tree 时也可以直接作为目标家族。

### 对需求到模型生成的启发

它提示我们：若对象的结构天然是“孩子数无固定上界”，就不应该强行用 ranked tree 或线性自动机，而要直接切换到 unranked tree family。

### 现实限制

原文没有工程 DSL、schema 语法或工具链，更多提供母体定义和性质。

## 重要的相关工作

### 奠基或前身工作

- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- [hedge-automata-a-formal-model-for-xml-schemata/desc.md](../hedge-automata-a-formal-model-for-xml-schemata/desc.md)
- [deterministic-automata-on-unranked-trees/desc.md](../deterministic-automata-on-unranked-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文无工程标准，但明确把 unranked trees 与 XML/document trees 的模型需求接到自动机理论上。

### 与本研究关系最紧的工作

- 它是 `Tree Automata -> unranked` 支线最适合入树的经典母型条目之一。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Unranked Tree Automata / Tree-Regular Languages over Non-Ranked Alphabets
- 论文角色：分支整理
- 核心功能：把 tree automata 从 ranked alphabets 推到 unranked / non-ranked trees。
- 关键特性：`2NTA`、`NATA/DATA`、`NDTA/DDTA`、top congruence、horizontal local views。
- 构造方式：孩子状态串上的 regular language + 树自动机 run。
- 基础设施：无工程标准，但为后续 XML / hedge / deterministic-unranked 提供母体。
- 适用场景：unranked tree、文档树、derivation trees、XML-like structural validation。
- 需求前提：节点分支数有限但不固定，且局部约束可用 child-state regular languages 描述。
- 状态：🟢
