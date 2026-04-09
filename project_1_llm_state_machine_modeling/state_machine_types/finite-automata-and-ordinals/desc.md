# 有限自动机与序数 / Finite automata and ordinals

## 基本信息

- 标题：Finite automata and ordinals
- 中文标题：有限自动机与序数
- 作者：Nicolas Bedon
- 发表：*Theoretical Computer Science*, 156(1):119-144, 1996
- DOI：`10.1016/0304-3975(95)00006-2`
- 链接：https://dpt-info-sciences.univ-rouen.fr/~bedonnic/Recherche/Biblio/finite_automata_and_ordinals.php
- 形式主义：`Automata on Ordinals / Choueka-Wojciechowski Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论统一
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 ordinal-indexed words、successor / limit ordinal transition 语义，以及 Choueka / Wojciechowski 两套 automaton 定义。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `n`-automaton / `W`-automaton tuple、continuous run、cofinality、正则表达式刻画与 determinization construction。

## 简报

这篇论文的关键价值，不是再讲一遍 `\omega`-word automata，而是把“序数索引词上的自动机”这条支线整理成稳定母节点：它统一解释 Choueka automata 与 Wojciechowski automata 的关系，证明受限域上的等价性，并补出 complement closure 与 determinization。对当前文库来说，它正好填上了 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md) 与 [automata-on-linear-orderings/desc.md](../automata-on-linear-orderings/desc.md) 之间长期缺的一层“ordinal-word”中间节点。

- 形式主义定位：`Infinite-Object Automata / \omega-Automata` 主干下的 ordinal-word 分支母节点。
- 构造方式简述：把普通有限自动机的 successor transition 保留下来，再为 limit ordinals 单独定义“由此前共尾出现状态决定”的 limit transition 语义。
- 基础设施与场景简述：原文是纯理论工作，但 tuple、continuous run、cofinality、正则表达式刻画、complement closure 与 determinization 都非常完整，足以直接挂树。

```text
ordinal-indexed word -> successor / limit transitions -> continuous run -> accepted ordinal language
```

## 形式主义定义与核心对象

### 定义对象

论文聚焦的是“以序数为长度的词”上的有限自动机。和普通 `FA` 相比，它的难点不在 successor position，而在 limit ordinal：运行到 `\omega`、`\omega^2` 这类位置时，自动机不能只看“前一个状态”，而要看此前某个状态集合是否共尾地反复出现。

### 核心抽象

论文先统一记号，再把 Choueka 的 `n`-automaton 写成：

$$
A = \langle S, M, s_0, F, \Sigma \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是有限基础状态集。
2. `M` 是转移关系。
3. `s_0` 是初始状态。
4. `F` 是接受状态集。
5. `\Sigma` 是输入字母表。

Choueka 路线的一个关键点，是 limit level 不再只落在 `S` 中，而会落到迭代幂集层上。原文用到的记号可压成：

$$
[S]^0_n = \bigcup_{i=0}^n [S]^i,\quad [S]^0 = S,\quad [S]^{i+1} = \mathcal P([S]^i)
$$

这表示：对长度小于 `\omega^n + 1` 的词，run 在不同 limit 层级上可能进入 `S` 的迭代幂集。

论文对 Wojciechowski 路线给出的 continuous run 在 limit ordinal `\beta` 处满足：

$$
\phi(\beta) = \{ s \in S \mid \{\gamma < \beta \mid \phi(\gamma) = s\}\ \text{is cofinal with}\ \beta \}
$$

上式中的符号逐项解释如下：

1. `\phi` 是 run。
2. `\beta \in Lim` 是某个 limit ordinal。
3. `cofinal with \beta` 表示状态 `s` 在 `\beta` 之前共尾地反复出现，而不是只出现有限多次。

这条式子就是 ordinal-word automata 与 ordinary `\omega`-automata 真正分家的地方。

### 一个最小例子与通俗解释

一个最容易理解的例子，是长度为 `\omega + 1` 的词。设自动机在前 `\omega` 个位置不断读取 `a`，最后一个位置读取 `b`。那么在位置 `\omega`，run 不会简单地看“第 `\omega-1` 步状态”，而是会汇总：

$$
\phi(\omega) = \{ s \in S \mid s \text{ appears infinitely often before } \omega \}
$$

然后再用 `\phi(\omega)` 与字母 `b` 决定最后一步转移。

通俗地说，这类模型像“会在无穷长前缀末端做一次极限汇总”的有限自动机。它比 `Büchi` 只处理 `\omega`-words 更进一步，因为这里的输入长度可以是 `\omega+1`、`\omega^2`、甚至更高的可数序数。

### 运行 / 接受 / 转移语义

对输入词 `u \in \Sigma^\alpha`，接受语义可压成：

$$
u \in L(A) \iff \exists \phi\ \text{continuous on}\ \alpha+1,\ \phi(0)=s_0,\ \phi(\alpha)\in F
$$

上式中的符号逐项解释如下：

1. `\phi` 是 run。
2. `continuous` 表示 successor 与 limit 位置都遵守对应的转移语义。
3. `\phi(\alpha)\in F` 表示在输入末端落到接受态或接受层元素。

对 Choueka 路线，输入长度受限于 `< \omega^n + 1`；对 Wojciechowski 路线，输入长度可以更广，但 limit transition 的定义更直接建立在共尾性上。

### 语义边界

这条支线的边界主要有三点：

1. 对象仍然是线性序列，不是树或一般图。
2. 输入长度可以是 transfinite ordinal，而不再只是 `\omega`。
3. limit transition 是本体的一部分，不是外接逻辑解释。

### 关键性质与判定边界

论文最核心的结果，是在把 Wojciechowski automata 的定义域限制到 Choueka 的范围后，二者可定义同一类语言。可把这一点压成：

$$
L_{\mathrm{Choueka}} = L_{\mathrm{Wojciechowski}} \cap \Sigma^{<\omega^n+1}
$$

上式中的符号逐项解释如下：

1. `L_{\mathrm{Choueka}}` 是 Choueka `n`-automata 定义的语言类。
2. `L_{\mathrm{Wojciechowski}}` 是 Wojciechowski automata 定义的语言类。
3. `\Sigma^{<\omega^n+1}` 把输入域限制在 Choueka 可处理的长度范围内。

在这个等价基础上，论文进一步得到：

1. Wojciechowski-definable languages 对 complement 封闭。
2. Wojciechowski automata 可 determinize。
3. 序数词正则表达式视角与 automata 视角能稳定互通。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然保留有限基础状态集。 |
| 事件 / 触发 | 强支持 | successor 位置按当前字母转移，limit 位置按共尾状态集合转移。 |
| 守卫 / 数据 | 不支持 | 没有一般变量守卫，增强点完全在输入长度与 limit semantics。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 不支持 | 单机串行识别模型。 |
| 时间约束 | 不支持 | 这里的“序数”是输入索引，不是时钟时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、纯符号序列模型。 |
| 可执行 / 可验证性 | 强理论支持 | 等价性、补封闭与确定化结论都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `n`-automaton 骨架 | `$A=\langle S,M,s_0,F,\Sigma \rangle$` | 给序数词自动机一个稳定 tuple。 |
| limit 语义 | `$\phi(\beta)=\{s\in S\mid \{\gamma<\beta\mid \phi(\gamma)=s\}\text{ cofinal with }\beta\}$` | 说明 ordinal-word automata 真正新增了什么。 |
| 接受语义 | `$u\in L(A)\iff \exists \phi,\ \phi(0)=s_0,\ \phi(\alpha)\in F$` | 序数长度输入仍以 run 末态接受为核心。 |
| 两路线等价 | `$L_{\mathrm{Choueka}} = L_{\mathrm{Wojciechowski}} \cap \Sigma^{<\omega^n+1}$` | 给树上新增节点提供稳定理论母语。 |
| 闭包与确定化 | complement / determinization | 说明这不是孤立定义，而是一个成熟 family。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 输入对象是否确实是 ordinal-indexed word。
2. limit ordinal 处的语义是否需要依赖共尾反复出现的状态集合。
3. 是采用 Choueka 的有界层级版本，还是采用更一般的 Wojciechowski 版本。

### 机器可处理承载方式

原文的承载方式是 automaton tuple、ordinal-word、continuous run 与正则表达式刻画，没有工程文件格式。

### 交换与互操作

它最自然地互操作到：

1. `Büchi` / `Muller` 风格的 `\omega`-word automata。
2. `Finite automata on infinite objects` 的统一 infinite-object 框架。
3. 后来的 `Automata on Linear Orderings` 一般化路线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 ordinal-word automaton tuple、cofinality 与 regular-expression characterization。
- 仿真/执行支持：可按 successor / limit 语义定义运行，但更偏识别理论而非工程执行。
- 验证/分析支持：等价性、补封闭、确定化与可定义语言类比较是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `\omega`-automata 向更长 transfinite sequence 扩张时的经典分支。

## 适用场景与需求前提

### 适用场景

适用于确实需要处理 ordinal-indexed words、可数序数长度输入或 transfinite run 语义的场景。

### 需求前提

1. 对象必须天然是线性序列，且长度超出普通有限词和 `\omega`-词。
2. 需求需要在 limit 位置做“此前无限 / 共尾出现状态”的汇总。
3. 关注点是表达力、闭包性与逻辑对应，而不是工程落地工具链。

### 不适用或高成本场景

如果需求只是有限词、普通 `\omega`-word 或树结构，用已有 `FA` / `Büchi` / tree automata 更自然；如果需求落在一般线性序或 scattered ordering，则后来的 `Automata on Linear Orderings` 更贴切。

## 与相邻形式主义的关系

相对 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)，它从“统一 infinite-object 框架”进一步收束到序数词这一条具体支线；相对 [on-a-decision-method-in-restricted-second-order-arithmetic/desc.md](../on-a-decision-method-in-restricted-second-order-arithmetic/desc.md)，它已经不只停在 `\omega`-输入，而是进入更一般的 transfinite words；相对 [automata-on-linear-orderings/desc.md](../automata-on-linear-orderings/desc.md)，后者可以看作把这里的 ordinal branch 进一步推广到更一般线性序的一步。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Infinite-Object Automata / \omega-Automata -> Automata on Ordinals` 这层长期缺失的中间节点，也让 `Automata on Linear Orderings` 有了更合理的前序来源。

### 作为目标形式主义还是中间表示

它更适合作为谱系节点和理论边界参照，而不是控制系统需求建模的直接目标；但它很适合文库里的“状态机族演化树”建设。

## 重要的相关工作

1. [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)：更高一层的 infinite-object 总母节点。
2. [on-a-decision-method-in-restricted-second-order-arithmetic/desc.md](../on-a-decision-method-in-restricted-second-order-arithmetic/desc.md)：`\omega`-word 接受主线的更早奠基点。
3. [automata-on-linear-orderings/desc.md](../automata-on-linear-orderings/desc.md)：把 ordinal branch 推广到更一般线性序的后继条目。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它给出了清晰的 automaton 骨架、limit 语义和 family-level closure / determinization 结果。
- 它应挂在 `Infinite-Object Automata / \omega-Automata` 之下，并作为 `Automata on Linear Orderings` 的直接前序节点。
- 它不是 DSL、工具或应用论文，也不是只借序数词做某个逻辑证明的 side paper。
