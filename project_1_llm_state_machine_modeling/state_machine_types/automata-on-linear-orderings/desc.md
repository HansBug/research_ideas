# 线性序上的自动机 / Automata on linear orderings

## 基本信息

- 标题：Automata on linear orderings
- 中文标题：线性序上的自动机
- 作者：Veronique Bruyere, Olivier Carton
- 发表：*Journal of Computer and System Sciences*, 73(1):1-24, 2007
- DOI：`10.1016/j.jcss.2006.10.009`
- 链接：https://www.irif.fr/~carton/Publications/Linear/Kleene/Scattered/jcss.pdf
- 形式主义：`Automata on Linear Orderings`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 automaton 四元组、cut-indexed path、left/right limit transitions 和 countable scattered linear orderings。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 automaton tuple、cut 结构和 rational operations。

## 简报

这篇论文的意义不只是“再讲一次 ordinal automata”，而是把 finite、`\omega`、双向无限、ordinal 以及更一般的 countable scattered linear orderings 放进同一套 automaton 语义里。对当前文库来说，它非常适合作为 `Infinite-Object Automata / \omega-Automata` 主线上的统一扩张节点，因为它把 `Buchi`、`biautomata`、ordinal words` 等分散分支重新压回到“线性序上的自动机”这个更高层母语里。

- 形式主义定位：`Infinite-Object Automata` 主干上的“任意可数散线性序”统一扩展。
- 构造方式简述：状态不再贴在单词位置上，而是贴在线性序的 `cuts` 上；除了普通 successor transition 外，还增加 left limit 和 right limit transition。
- 基础设施与场景简述：原文完全是理论工作，但定义、示例、rational operations 和 `Kleene` 型等价定理都很完整，适合作为扩树节点而不是零散旁证。

```text
finite / omega / bi-infinite / ordinal words -> cuts of linear ordering -> successor + limit transitions -> unified automaton semantics
```

## 形式主义定义与核心对象

### 定义对象

论文研究的是“由任意 countable scattered linear ordering 索引的词”。与传统 automaton 的区别不在字母表，而在底层索引对象：输入不再只是一条自然数序列，而可以是任意可数散线性序。

### 核心抽象

原文把 automaton 写成：

$$
\mathcal A = (Q, E, I, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `E` 是转移集合。
3. `I \subseteq Q` 是初始状态集。
4. `F \subseteq Q` 是终止状态集。

转移分三类：

$$
E \subseteq (Q \times A \times Q) \cup (\mathcal P(Q) \times Q) \cup (Q \times \mathcal P(Q))
$$

它们分别表示：

1. successor transition `(p,a,q)`，记作 `$p \xrightarrow{a} q$`。
2. left limit transition `(P,q)`，记作 `$P \to q$`。
3. right limit transition `(q,P)`，记作 `$q \to P$`。

这里最关键的对象不是输入位置本身，而是线性序 `J` 的 cuts 组成的序 `\hat J`。若词是：

$$
x = (a_j)_{j \in J}
$$

则路径写成：

$$
\gamma = (q_c)_{c \in \hat J}
$$

也就是说，状态序列的索引不是 `J`，而是 `\hat J`。

### 一个最小例子与通俗解释

一个直观例子是“识别所有长度为 ordinal 的词”。论文里的简单 automaton 只保留 ordinary successor transition 和 left limit transition，而不放任何 right limit transition。

直觉上：

1. 若一个 cut 没有前驱，那么路径必须靠 left limit transition 接上。
2. 若某个 cut 没有后继，却又不是最后一个 cut，就需要 right limit transition。
3. 因为 automaton 里没有 right limit transition，所以可接受的底层线性序只能是“除了最后一个 cut 之外，每个 cut 都有后继”的情形，也就是 ordinal。

通俗地说，这类 automaton 像是在“单词缝隙”上布状态，而不是在字母上布状态；当线性序有极限点时，它不是停下来，而是用 left/right limit transitions 跨过这些极限切口。

### 运行 / 接受 / 转移语义

论文定义了 path 的左右极限状态集。对任一 cut `c \in \hat J`，左极限集可写成：

$$
\lim_{c^-}\gamma = \{ q \in Q \mid \forall k < c,\ \exists i,\ k < i < c \text{ and } q_i = q \}
$$

右极限集对称地写成：

$$
\lim_{c^+}\gamma = \{ q \in Q \mid \forall k > c,\ \exists i,\ c < i < k \text{ and } q_i = q \}
$$

上式中的符号逐项解释如下：

1. `c` 是一个 cut。
2. `q_i` 是路径在某个 cut 上的状态。
3. 左极限集收集“在 `c` 左侧无限接近 `c` 时反复出现的状态”。
4. 右极限集收集右侧对应的状态。

路径需要满足：

1. 对每个相邻 cut `c_j^- < c_j^+`，都有 successor transition：

$$
q_{c_j^-} \xrightarrow{a_j} q_{c_j^+}
$$

2. 若某个 cut 没有前驱且不是第一个 cut，则必须有：

$$
\lim_{c^-}\gamma \to q_c
$$

3. 若某个 cut 没有后继且不是最后一个 cut，则必须有：

$$
q_c \to \lim_{c^+}\gamma
$$

成功路径要求其首状态在 `I` 中、末状态在 `F` 中。

### 语义边界

这个模型的关键边界在于它统一处理的是 `countable scattered linear orderings`。它不是针对任意 dense order，也不是只针对 `\omega` 或 ordinal；其主语义支点是 cuts 与 limit transitions。

### 关键性质与判定边界

论文主定理 Theorem 20 可压成：

$$
\text{A set of words on countable scattered linear orderings is rational } \iff \text{ it is recognizable}
$$

这就是该 family 的 `Kleene` 型定理。换言之：

1. 论文不仅给出 automaton。
2. 还同时给出 rational expressions。
3. 并证明二者在 countable scattered linear orderings 上完全对齐。

这使它成为一个非常稳定的模型节点，而不是零散的变体说明。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态骨架。 |
| 事件 / 触发 | 强支持 | successor transition 仍由当前字母触发。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般变量守卫。 |
| 层次 | 不支持 | 对象仍是线性序，而不是树。 |
| 并发 / 同步 | 不支持 | 单条线性序上的路径模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散线性序。 |
| 可执行 / 可验证性 | 强理论支持 | rational / automaton 等价、limit transitions 语义清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| automaton 元组 | `$\mathcal A=(Q,E,I,F)$` | 统一 finite / infinite / ordinal / bi-infinite 的骨架。 |
| 转移类型 | `$(Q\times A\times Q)\cup(\mathcal P(Q)\times Q)\cup(Q\times \mathcal P(Q))$` | successor + left limit + right limit。 |
| 路径索引 | `$\gamma=(q_c)_{c\in\hat J}$` | 状态贴在 cuts 上，而不是字母位置上。 |
| 左右极限 | `$\lim_{c^-}\gamma,\ \lim_{c^+}\gamma$` | 处理极限 cut 的核心语义对象。 |
| 主定理 | `rational \iff recognizable` | 线性序 automata 的 Kleene 定理。 |

## 构造方式与承载格式

### 建模入口

建模时要先确定：

1. 输入词由哪类线性序索引。
2. 是否需要处理极限 cut。
3. 哪些状态集合可作为 left / right limit transition 的端点。

### 机器可处理承载方式

机器可处理承载方式是 automaton 四元组、cuts 和 rational expressions，而不是工程交换格式。

### 交换与互操作

它与以下家族互操作最紧：

1. `Buchi` automata。
2. bi-infinite word automata。
3. ordinal automata。
4. rational expressions over countable scattered orderings。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 cut-based path 与 rational operations。
- 仿真/执行支持：理论上可沿 cuts 构造 path。
- 验证/分析支持：`Kleene` 型等价与 limit-transition 语义是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 infinite-word / ordinal-word / bi-infinite-word 理论的统一化分支。

## 适用场景与需求前提

### 适用场景

适用于输入对象天然不是普通有限词，而是 countable scattered linear ordering 上的序列，例如 ordinal words、bi-infinite words 及其统一分析。

### 需求前提

1. 对象仍是线性序，而不是树或网格。
2. 需要显式处理极限点左右两侧的无限逼近行为。
3. 可以接受状态建在 cuts 上，而不是建在元素上。

### 不适用或高成本场景

若需求只是 finite words 或普通 `\omega`-words，用更专门的 automata 往往更轻量；若对象是 dense orderings，则这篇的主结果也不直接适用。

## 与相邻形式主义的关系

相对 [on-a-decision-method-in-restricted-second-order-arithmetic/desc.md](../on-a-decision-method-in-restricted-second-order-arithmetic/desc.md)，它不再只处理 one-sided `\omega`-words；相对 [ensembles-reconnaissables-de-mots-biinfinis/desc.md](../ensembles-reconnaissables-de-mots-biinfinis/desc.md)，它把 bi-infinite words 作为统一线性序框架中的一个特例；相对 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)，它更明确地给出了“线性序 + cuts + 双侧极限转移”的 automaton 本体。

## 与本研究的关系

### 对 Project 1 的价值

它为 `Infinite-Object Automata` 主线补出了“线性序统一框架”这一节点，让 `Buchi / biautomata / ordinal` 不再只是松散并列。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和无限对象中间模型，而不是控制系统需求建模的默认最终形式。

### 对需求到模型生成的启发

当需求对象本身带有“有穷、无穷、双向无穷、ordinal 段落混合”的线性序结构时，生成模型时不应只想 `\omega`-automata，而要显式问清底层 ordering 类型。

### 现实限制

没有工程化工具链，且 cut-based 语义对一般控制工程师不直观；因此更适合谱系建设与能力分析。

## 重要的相关工作

### 奠基或前身工作

- [on-a-decision-method-in-restricted-second-order-arithmetic/desc.md](../on-a-decision-method-in-restricted-second-order-arithmetic/desc.md)
- ordinal-word / bi-infinite-word automata 传统

### 同类型或同家族工作

- [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)
- [ensembles-reconnaissables-de-mots-biinfinis/desc.md](../ensembles-reconnaissables-de-mots-biinfinis/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为 `Infinite-Object` 主线上“统一 linear-ordering 语义”的补树节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Automata on Linear Orderings`
- 论文角色：模型提出
- 核心功能：在 countable scattered linear orderings 上统一 finite / infinite / bi-infinite / ordinal words 的 automaton 语义。
- 关键特性：cut-indexed path、left/right limit transitions、rational expressions、Kleene 型等价。
- 构造方式：`(Q,E,I,F)` 元组 + successor / left-limit / right-limit transitions。
- 基础设施：纯理论承载，无工程标准，但统一性极强。
