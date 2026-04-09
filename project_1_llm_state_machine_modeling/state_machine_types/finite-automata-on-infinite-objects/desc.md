# 无限对象上的有限自动机 / Finite automata on infinite objects

## 基本信息

- 标题：Finite automata on infinite objects
- 中文标题：无限对象上的有限自动机
- 作者：Takeshi Hayashi
- 发表：Mathematical Reports, 15(1):13-66, 1985；文中同时注明这是作者在 Kyushu University 的博士论文
- DOI：`10.15017/1449046`
- 链接：https://catalog.lib.kyushu-u.ac.jp/opac_download_md/1449046/15_1_p013.pdf
- 形式主义：Infinite-Object Automata / $\omega$-Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：专题整理
- 工具/实现获取方式：原文未提供实现；机器可处理入口是无限对象上的 automaton tuple、run 与六类 acceptance condition。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 automaton 定义、path-based acceptance 和对象类之间的比较。

## 简报

这篇论文不是只讲一种单一 automaton，而是围绕“无限对象上的有限自动机”建立统一接受框架：一类是 `\omega`-words 上的 alternating finite automata，一类是 infinite trees 上的 finite tree automata，一类是 two-sided infinite words 上的 finite biautomata。它用同一组 `C_1,\ldots,C_6` 接受条件把这些对象统一起来，因此非常适合作为 `Finite Automata` 向 `\omega`-words / infinite trees / bilateral words 扩展时的总母节点。

- 形式主义定位：有限自动机主干上的“无限对象 / `\omega`-对象”扩展总线。
- 构造方式简述：先给出无限对象上的 run，再沿每条 path 施加 `C_1,\ldots,C_6` 接受条件。
- 基础设施与场景简述：原文完全是理论整理，没有工程格式，但非常适合为 `Büchi / Rabin / alternating / infinite-tree` 一整条分支提供统一母语。

```text
无限词 / 无限树 / 双向无限词 -> run on infinite object -> path-wise acceptance conditions -> language class
```

## 形式主义定义与核心对象

### 定义对象

论文的核心不是再发明一个完全不同的状态机骨架，而是把“有限状态控制 + 无限对象输入 + 路径接受条件”组织成统一框架。对 `k` 叉无限树的情形，原文给出了非常清晰的 tuple。

### 核心抽象

原文第 3 章对 finite `k`-ary tree automaton 的定义可写成：

$$
M = \langle S, E, d, s_0, \mathcal F \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `E` 是树节点标签字母表。
3. `d` 是转移函数，`d : S \times E \to \mathcal P(S^k) \setminus \{\emptyset\}`。
4. `s_0` 是初始状态。
5. `\mathcal F` 是 final-set family，其中每个 `F \in \mathcal F` 都是一组 final states。

若 `t : T_k \to E` 是一棵 `k` 叉无限树，则其 run `r : T_k \to S` 满足：

$$
r(\varepsilon) = s_0
$$

并且对每个 `x \in T_k` 有：

$$
(r(x0), r(x1), \ldots, r(x(k-1))) \in d(r(x), t(x))
$$

这里的符号逐项解释如下：

1. `T_k` 是无限 `k` 叉树的位置集合。
2. `t(x)` 是节点 `x` 的标签。
3. `r(x)` 是 run 在节点 `x` 处的状态。
4. `x0,\ldots,x(k-1)` 是 `x` 的 `k` 个子节点。

对任一路径 `\pi \subseteq T_k`，原文定义：

$$
I(r \mid \pi) = \{ s \in S \mid s = r(x) \text{ for infinitely many } x \in \pi \}
$$

它表示在路径 `\pi` 上“无限次出现”的状态集合。

### 一个最小例子与通俗解释

可以把一元情形看成最简单的例子：`k=1` 时，`T_1 = \{0\}^*`，这就退化成 `\omega`-word 上的自动机。也就是说，这个统一框架把“无限词自动机”看成“无限树自动机”的一元特例。

通俗地说，这类模型像普通有限自动机的“无限版”：对象不再在有限步内读完，所以接受不再取决于最后停在哪个状态，而取决于“沿一条无限 path，哪些状态会反复出现、出现到什么程度”。

### 运行 / 接受 / 转移语义

原文用六类接受条件 `C_1,\ldots,C_6` 统一描述无限对象上的接受。对 infinite-tree automata，接受语义可写成：

$$
t \in L_i(M)
\iff
\exists r\ \forall \pi \subseteq T_k\ \exists F \in \mathcal F,\ \text{Cond}_{C_i}(r,\pi,F)
$$

其中原文列出的条件包括：

$$
C_1:\ I(r \mid \pi) \cap F \neq \emptyset
$$

$$
C_2:\ I(r \mid \pi) \subseteq F
$$

$$
C_5:\ I(r \mid \pi) = F
$$

等等。

上式中的符号逐项解释如下：

1. `L_i(M)` 是按接受条件 `C_i` 得到的语言类。
2. `r` 是 `M` 在对象 `t` 上的一条 run。
3. `\pi` 是对象中的一条无限 path。
4. `F \in \mathcal F` 是某个 final set。
5. `\text{Cond}_{C_i}` 代表原文定义的六种路径接受关系之一。

### 语义边界

这个框架最重要的边界是：接受不再由“最终状态”决定，而由“无限运行中反复出现的状态集”决定；同时对象不只是一维 `\omega`-word，也可以是 infinite tree 或 two-sided infinite word。

### 关键性质与判定边界

原文给出的代表性结论包括：

1. 统一比较 alternating finite automata on `\omega`-words、finite tree automata on infinite trees 和 finite biautomata on two-sided infinite words。
2. 对 tree automata，simple final-set 形式对 `C_1,\ldots,C_4` 足够。
3. 对 infinite-tree 分支，Muller / `C_5` 型条件给出最一般的语言类。

可把其中一个核心判断问题压缩为：

$$
\text{Given } M,\ i,\ \text{compare } L_i(M) \text{ with other acceptance classes}
$$

也就是说，论文的重点不是某个单一算法，而是系统梳理不同接受条件和对象种类对语言类表达力的影响。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 仍是有限状态控制。 |
| 事件 / 触发 | 不适用 | 更核心的是无限对象上的标签与 path。 |
| 守卫 / 数据 | 不支持 | 原始框架无一般数据守卫。 |
| 层次 | 强支持 | 对 infinite tree 分支，层次来自对象本体。 |
| 并发 / 同步 | 不支持 | 不是并发网；分支只是对象结构，不是同步进程。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散无限对象模型。 |
| 可执行 / 可验证性 | 强支持 | 接受条件、类之间的包含和比较构成主要理论内容。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| infinite-tree automaton | `$M=\langle S,E,d,s_0,\mathcal F\rangle$` | 有限状态控制 infinite tree 上的 run。 |
| run 约束 | `$(r(x0),\ldots,r(x(k-1)))\in d(r(x),t(x))$` | 父节点状态和标签决定对子节点状态的要求。 |
| 无限出现状态集 | `$I(r\mid\pi)$` | 接受由 path 上无限次出现的状态决定。 |
| 路径接受 | `$t\in L_i(M)$` | 六类接受条件统一刻画无限对象语言类。 |
| 一元退化 | `$k=1 \Rightarrow T_1=\{0\}^*$` | `\omega`-word 自动机是树框架的特例。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先确定对象类型：`\omega`-word、infinite tree 或 two-sided infinite word。
2. 定义有限状态集与对象标签字母表。
3. 选择接受条件家族 `C_1,\ldots,C_6`。

### 机器可处理承载方式

机器可处理承载方式是 automaton tuple、run relation 和 acceptance family，而不是工程 XML/JSON。

### 交换与互操作

它与 `Büchi`、`Rabin`、alternating automata、infinite tree logic 以及双向无限词理论天然互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 automaton tuple 与 acceptance family。
- 仿真/执行支持：可以定义对象上的 run，但更偏识别而非工程执行。
- 验证/分析支持：接受条件比较、表达力分析和类关系梳理是原文重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `\omega`-automata 与 infinite-tree automata 的经典理论母体。

## 适用场景与需求前提

### 适用场景

适用于需要表达无限执行、无限路径、长期重复行为或 infinite-tree 结构语言的场景。

### 需求前提

1. 对象必须天然是无限词、无限树或双向无限词。
2. 需求是长期接受条件，而不是有限前缀判定。
3. 可以接受“路径上无限次出现状态”这类语义。

### 不适用或高成本场景

如果需求只是有限长度控制逻辑或普通协议 trace，用普通 `FA/PDA/TA` 更自然。

## 与相邻形式主义的关系

相对普通 `Finite Automata`，它把输入对象扩展到无限对象；相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，它给出更系统的接受条件比较；相对 [tree-automata/desc.md](../tree-automata/desc.md)，它把“有限树语言识别”进一步推进到 infinite-tree / `\omega`-object 语义。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了“有限自动机如何走向 `\omega`-objects / infinite trees”这一条非常重要的桥接节点。

### 作为目标形式主义还是中间表示

通常更适合作为谱系节点和理论中间层，而不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

它提示我们：一旦需求本质上是“无限运行 / 长期接受”，传统 finite acceptance 就不够，必须转向 `\omega`-style acceptance。

### 现实限制

没有工程级标准和工具链，且对象是无限结构，所以更多服务于理论分析而不是直接执行。

## 重要的相关工作

### 奠基或前身工作

- `Büchi` 关于 `\omega`-words 的经典工作。
- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)

### 同类型或同家族工作

- alternating finite automata on `\omega`-words
- finite tree automata on infinite trees
- finite biautomata on two-sided infinite words

### 标准 / 格式 / 工具链工作

- 原文没有工程标准，重点在 acceptance family 与类关系。

### 与本研究关系最紧的工作

- 它为“无限对象 automata 总线”提供了非常适合扩树的统一整理节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Infinite-Object Automata / $\omega$-Automata
- 论文角色：专题整理
- 核心功能：用统一 acceptance framework 组织无限词、无限树和双向无限词上的有限自动机。
- 关键特性：path-wise acceptance、六类接受条件、无限出现状态集、对象类型统一比较。
- 构造方式：有限状态骨架 + 对象上的 run + `C_1,\ldots,C_6` 接受条件。
- 基础设施：理论互操作强，但无工程标准或公开工具。
- 适用场景：无限执行、长期接受、infinite-tree 语言与 `\omega`-对象分析。
- 需求前提：对象必须天然是无限结构，且接受语义依赖长期重复行为。
- 状态：🟢
