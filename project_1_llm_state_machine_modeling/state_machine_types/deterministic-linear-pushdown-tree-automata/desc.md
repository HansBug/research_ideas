# 由确定性线性下推树自动机线性时间可识别的树语言类 / Linear-Time Recognizable Classes of Tree Languages by Deterministic Linear Pushdown Tree Automata

## 基本信息

- 标题：Linear-Time Recognizable Classes of Tree Languages by Deterministic Linear Pushdown Tree Automata
- 中文标题：由确定性线性下推树自动机线性时间可识别的树语言类
- 作者：Akio Fujiyoshi
- 发表：*IEICE Transactions on Information and Systems* E92-D(2):248-254, 2009
- DOI：`10.1587/transinf.E92.D.248`
- 链接：https://doi.org/10.1587/transinf.E92.D.248
- 形式主义：`Linear Pushdown Tree Automata (L-PDTA) / deterministic L-PDTA`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理 / 线性时间确定化变体
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `L-PDTA` 元组、linearity restriction、deterministic / real-time / regular-look-ahead 定义与 complexity / hierarchy theorems。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `L-PDTA` rewrite rules、look-ahead bottom-up automaton 与 `LM-CFTG` 对应。

## 简报

这篇论文并不是重新提出 `PDTA`，而是抓住其中最适合“可识别但还要高效”的一条分支：禁止 stack duplication 的 linear `PDTA`。在这条分支上，作者系统整理了 real-time deterministic、deterministic 和 deterministic with regular look-ahead 三个层次，证明它们都能线性时间识别输入树，同时在 tree language 级别形成严格层级，而在 yield language 级别又全部 weakly equivalent。

- 形式主义定位：`Pushdown Tree Automata` 下的 deterministic / linear-time 支线，也是 `tree language` 与 `yield language` 两种比较口径的重要整理节点。
- 构造方式简述：从一般 `PDTA` 出发，加入“不允许复制当前 stack suffix”的 linearity restriction；再进一步区分 deterministic、real-time 与 regular look-ahead。
- 基础设施与场景简述：原文纯理论，但它把 `L-PDTA` 和 `LM-CFTG`、recognizable tree languages、linear-time recognizability 之间的关系压得很清楚，是 pushdown-tree 家族里少见兼顾表达力和复杂度的节点。

```text
tree pushdown -> linear stack discipline -> deterministic / look-ahead variants -> linear-time tree recognition
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 ranked trees 上的 linear pushdown tree automata。与一般 `PDTA` 的主要差别不在输入对象，而在 stack 更新：某一步中当前 stack suffix 最多只能传给一个孩子，不能被复制到多个孩子上。

### 核心抽象

一般 `L-PDTA` 继承 `PDTA` 的元组：

$$
M = (Q,\Sigma,\Gamma,q_0,Z_0,R)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是输入树字母表。
3. `\Gamma` 是 pushdown alphabet。
4. `q_0` 是初始状态。
5. `Z_0` 是初始 pushdown 符号。
6. `R` 是 read / `\varepsilon` rules。

其接受语言定义为：

$$
T(M) = \{ \alpha \in T_\Sigma \mid q_0(\alpha,Z_0) \vdash_M^* \alpha \}
$$

线性限制的核心写法是：对 type-(iv) rule

$$
q(b(x_1,\ldots,x_n),B) \to b(q_1(x_1,\pi_1),\ldots,q_n(x_n,\pi_n))
$$

要求：

$$
|\{ i \mid 1 \le i \le n,\ \pi_i \in \Gamma_1^* \}| = 1
$$

上式中的符号逐项解释如下：

1. `\pi_i \in \Gamma_1^*` 表示第 `i` 个孩子继承了当前 stack suffix。
2. 这个基数条件要求这样的孩子至多恰有一个。
3. 因而当前 stack 不会在一次分支中被复制给多个子树。

### 一个最小例子与通俗解释

论文的 Example 1 给了一个很好的最小例子：一个 `L-PDTA` 识别某类树，使其 yield language 为

$$
L_{ww} = \{ ww \mid w \in \{a,b\}^+ \}
$$

该 automaton 在树的前半段沿右脊 push 出一串 `A/B` 标记，随后在第二阶段把这些标记依次取回，强制第二半段与第一半段逐字符对应。

通俗地说，`L-PDTA` 像“树上的单分支栈记忆机器”。它仍有 pushdown 能力，但每次分叉时只能把那份真正的栈上下文继续交给一个孩子，因此比一般 `PDTA` 更轻，也更适合高效识别。

### 运行 / 接受 / 转移语义

其 instantaneous description 与一般 `PDTA` 相同，形式为状态、当前输入子树和当前 stack 内容。move relation 记作：

$$
c \vdash_M c'
$$

若某个 node `d` 上有可应用规则，就把对应 ID 改写成新的 ID-tree。接受语义仍然是从 `q_0(\alpha,Z_0)` 出发规约到输入树本身。

本文进一步定义三种确定化变体：

1. real-time deterministic `L-PDTA`
2. deterministic `L-PDTA`
3. deterministic `L-PDTA` with regular look-ahead

其中 regular look-ahead 版本扩成八元组：

$$
M = (P,Q,\Sigma,\Gamma,q_0,Z_0,\delta,R)
$$

这里 `P` 是 look-ahead states，`\delta` 由 deterministic bottom-up tree automaton 实现，用于先给每个节点分配 look-ahead 状态。

### 语义边界

相对 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)，`L-PDTA` 是更受限但更高效的子类；相对 deterministic top-down tree automata，它因为保留了 linear pushdown，能处理更多 context-free 样式树语言；相对 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)，它不是走更强 branching expressiveness，而是走 deterministic linear-time recognizability。

### 关键性质与判定边界

本文首先给出复杂度结果：

$$
\text{real-time deterministic L-PDTA, deterministic L-PDTA, deterministic L-PDTA with regular look-ahead}
$$

都能在线性时间内识别输入树，即：

$$
\mathrm{time}(M,\alpha) = O(|\alpha|)
$$

对 tree languages，三类 deterministic family 和 nondeterministic family 形成严格层级：

$$
\mathrm{RtDet} \subsetneq \mathrm{Det} \subsetneq \mathrm{DetRla} \subsetneq \mathrm{Nondet}
$$

但对 yield languages，又有：

$$
y\mathrm{RtDet} = y\mathrm{Det} = y\mathrm{DetRla} = y\mathrm{Nondet}
$$

更进一步，论文证明任意 `L-PDTA` 都能转成 weakly equivalent 的 real-time deterministic `L-PDTA`：

$$
\forall M \in \mathrm{L\mbox{-}PDTA},\ \exists M' \in \mathrm{RtDet}\ \text{such that}\ \mathrm{yield}(T(M'))=\mathrm{yield}(T(M))
$$

这说明 linear restriction 把“tree recognition 的表达力差异”和“yield language 的表达力差异”清楚地分离了出来。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留有限控制。 |
| 事件 / 触发 | 不适用 | 输入是树。 |
| 守卫 / 数据 | 不支持 | 原始模型不引入变量守卫。 |
| 层次 | 强支持 | 输入是树，且具有线性 pushdown 记忆。 |
| 并发 / 同步 | 弱支持 | 分支存在，但真实 stack suffix 只能给一个孩子。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | linear-time recognition、strict hierarchy 与 weak equivalence 结果明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| L-PDTA 元组 | `$M=(Q,\Sigma,\Gamma,q_0,Z_0,R)$` | linear pushdown family 的基本对象。 |
| 接受语言 | `$T(M)=\{\alpha\mid q_0(\alpha,Z_0)\vdash_M^* \alpha\}$` | tree-language 接受定义。 |
| 线性限制 | `$|\{i\mid \pi_i\in\Gamma_1^*\}|=1$` | 禁止 stack duplication。 |
| tree-language hierarchy | `$\mathrm{RtDet}\subsetneq\mathrm{Det}\subsetneq\mathrm{DetRla}\subsetneq\mathrm{Nondet}$` | 三类 deterministic family 的严格层级。 |
| yield weak equivalence | `$y\mathrm{RtDet}=y\mathrm{Det}=y\mathrm{DetRla}=y\mathrm{Nondet}$` | yield 级别又重新汇合。 |

## 构造方式与承载格式

### 建模入口

1. 先判断一般 `PDTA` 是否真的需要 stack duplication。
2. 若不需要，就尽量落到 `L-PDTA`。
3. 若 deterministic top-down 能力不够，但又希望保持线性时间，可再加 regular look-ahead。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `L-PDTA` rewrite rules；
2. linearity restriction；
3. deterministic bottom-up look-ahead automaton；
4. `LM-CFTG` 与 `L-PDTA` 的等价转换。

### 交换与互操作

它和 `LM-CFTG`、deterministic bottom-up tree automata 以及 yield language 分析之间互操作很强，但没有工程 DSL 或 schema。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `L-PDTA` rule system 与 look-ahead automaton。
- 仿真/执行支持：deterministic 变体可在线性时间执行识别。
- 验证/分析支持：strict hierarchy、weak equivalence 与 linear-time theorem 完整。
- 代码生成/转换支持：与 `LM-CFTG` 之间转换明确，但原文未讨论工程代码生成。
- 标准化或社区生态：是 pushdown-tree 家族中少见兼顾效率与表达力比较的稳定分支。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要超过 regular tree language、但又希望线性时间识别的树语言。
2. 需要比较 tree language 与 yield language 两种口径时的模型基线。
3. 作为 `PDTA` 家族中 deterministic / efficient 支线的代表条目。

### 需求前提

1. 输入必须是树。
2. 非正则性主要来自单支 continuation 和记忆，而不是多支 stack duplication。
3. 若要求最强 deterministic 能力，通常需要 regular look-ahead。

### 不适用或高成本场景

若需求本身就需要把 stack 上下文复制给多个子树，一旦越过 linearity，`L-PDTA` 就不够了；此时应回到 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md) 或转向更强的 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)。

## 与相邻形式主义的关系

相对 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)，它是禁止 stack duplication 的线性子类；相对 deterministic top-down tree automata，它通过 linear pushdown 恢复了部分 context-free 样式表达力；相对 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)，它走的是 deterministic efficiency 分支，而不是 matching-pop branching 分支。

## 与本研究的关系

### 对 Project 1 的价值

它把新补出的 `Pushdown Tree Automata` 母枝继续细化成“线性时间确定化”分支，使 pushdown-tree family 的树结构不只剩下“更强”这一种展开方向。

### 作为目标形式主义还是中间表示

更适合作为谱系中的效率型理论节点与中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求对象是树，且需要比 regular tree language 更强的结构依赖，但又希望保线性时间识别，那么 LLM 应优先考虑 `L-PDTA + look-ahead`，而不是直接跳到一般 `PDTA`。

### 现实限制

没有工程生态，且线性限制让它无法覆盖所有 `PDTA` 语言，因此它在本研究中的主要价值仍是补家族分层与复杂度边界。

## 重要的相关工作

### 奠基或前身工作

- [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)
- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为 `Pushdown Tree Automata` 下的 deterministic / linear-time 子节点，与 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md) 形成清晰的“母节点 -> 效率型子类”关系。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Linear Pushdown Tree Automata (L-PDTA) / deterministic L-PDTA`
- 论文角色：分支整理 / 线性时间确定化变体
- 核心功能：在线性 stack discipline 下系统整理 deterministic `L-PDTA` 的复杂度、层级与 yield-language 等价性。
- 关键特性：linearity restriction、real-time / deterministic / regular-look-ahead 三类变体、linear-time recognition、strict hierarchy、yield weak equivalence。
- 构造方式：`L-PDTA` 元组加 linearity condition 与 look-ahead bottom-up automaton。
- 基础设施：纯理论模型，无工程标准或工具；核心基础设施是 `LM-CFTG` correspondence 和 linear-time recognition theorem。
- 适用场景：高效 tree-language recognition、pushdown-tree 家族分层、tree/yield 双口径比较。
- 需求前提：对象必须是树，且 stack duplication 最好可以被禁止或由 look-ahead 替代。
- 状态：🟢
