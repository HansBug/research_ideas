# 交替 / Alternation

## 基本信息

- 标题：Alternation
- 中文标题：交替
- 作者：Ashok K. Chandra, Dexter C. Kozen, Larry J. Stockmeyer
- 发表：*Journal of the ACM*, 28(1):114-133, 1981
- DOI：`10.1145/322234.322243`
- 链接：https://doi.org/10.1145/322234.322243
- 形式主义：`Alternating Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 alternating finite automaton 的五元组和布尔转移函数。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是状态集、布尔转移函数和递归接受函数。

## 简报

这篇论文的核心贡献不是再给 `FA/PDA/TM` 换一个名字，而是把“存在分支”的 nondeterminism 推广成“存在分支 + 全称分支”共同出现的 alternation。对 `project_1` 的演化树而言，它最重要的价值是把 `Alternating Automata` 固定成一个可以继续长出 `Alternating Tree Automata`、`Weak Alternating Tree Automata` 等后继节点的母节点。

- 形式主义定位：`Finite Automata` 主干上的 computation-mode 扩展节点。
- 构造方式简述：每个状态在读入一个符号后，不再只挑一个后继状态，而是对所有后继状态的真假值做布尔组合。
- 基础设施与场景简述：原文是纯理论工作，但它同时给出了 `AFA`、`APDA` 和 `ATM` 三层视角，足以稳定回答 alternation 是什么、能带来什么、在哪些模型上只增 succinctness、在哪些模型上真的增 expressive power。

```text
nondeterminism -> existential/universal branching -> alternating automata -> tree / pushdown / complexity branches
```

## 形式主义定义与核心对象

### 定义对象

论文第 5 节给出的 alternating finite automaton 是一个针对有限词的交替状态机。它仍然保留有限状态骨架，但把“下一个状态集合”换成了“关于所有状态真假值的布尔函数”。

### 核心抽象

原文 Definition 5.1 可写成：

$$
P = (Q,\Sigma,q_1,F,g)
$$

上式中的符号逐项解释如下：

1. `Q=\{q_1,\ldots,q_k\}` 是有限状态集。
2. `\Sigma` 是有限输入字母表。
3. `q_1` 是初始状态。
4. `F \subseteq Q` 是终止接受状态集。
5. `g` 把每个状态映射为一个布尔转移函数，决定读入一个符号后如何根据各后继状态的真假值组合出当前状态的真假值。

若把 `g(q_i)` 简写为 `g_i`，则：

$$
g_i : \Sigma \times B^k \to B
$$

其中 `B=\{0,1\}` 是布尔值集合，`B^k` 记录 `k` 个状态在剩余输入上的接受真假。

### 一个最小例子与通俗解释

一个很直观的例子是“这个词里既出现过 `a`，也出现过 `b`”。普通 nondeterministic automaton 更像“猜一个 witness”；alternating automaton 可以在初始状态一次性分成两条检查线：

1. 一条分支只负责确认“某处存在 `a`”。
2. 另一条分支只负责确认“某处存在 `b`”。

然后初始状态对这两条分支取合取。通俗地说，alternation 就像一个会“拆成多条并行检查任务”的状态机，其中有的分支在问“至少有一条成立吗”，有的分支在问“是不是全部都成立”。

### 运行 / 接受 / 转移语义

令 `f` 是接受状态集 `F` 的特征向量，原文先递归定义：

$$
H_i(\lambda) = \pi_i
$$

$$
H_i(ax)(u) = g_i(a, H_1(x)(u), \ldots, H_k(x)(u))
$$

上式中的符号逐项解释如下：

1. `\lambda` 是空串。
2. `\pi_i` 是对 `B^k` 的第 `i` 个投影。
3. `a \in \Sigma` 是当前读入符号。
4. `x \in \Sigma^*` 是剩余后缀。
5. `u \in B^k` 是各状态在后缀上的真假值向量。
6. `H_i(x)(u)` 表示“在状态 `q_i` 读取串 `x` 时的接受真假值”。

接受语义写成：

$$
P \text{ accepts } x \iff H_1(x)(f) = 1
$$

这意味着：从初始状态开始，把接受状态集的真值向量 `f` 代入递归布尔计算，最终若得到真，则输入词被接受。

### 语义边界

这篇论文最关键的边界结论是：

1. 在 finite automata 层面，alternation 增强的是表达的紧凑性，而不是词语言类本身。
2. 在 pushdown automata 层面，alternation 会真正规模性地增强表达能力。
3. 在 Turing-machine 层面，alternation 直接改写了时间/空间复杂度版图。

### 关键性质与判定边界

原文对 finite-state 情形给出的关键结论可压缩为：

$$
L(P)\ \text{is regular}
$$

以及：

$$
\text{a }k\text{-state AFA can require }2^{2^k}\text{ states under DFA simulation}
$$

这说明 alternating finite automata 并不离开 regular languages，但能比确定自动机紧凑得多。

对 machine complexity 线，论文的标志性结论是：

$$
\mathrm{APTIME} = \mathrm{PSPACE}
$$

这虽不是本文库要直接挂树的重点，却进一步说明 alternation 不是小修补，而是一种稳定的计算模型扩展。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态骨架。 |
| 事件 / 触发 | 强支持 | 每步按当前输入符号驱动。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般变量和守卫。 |
| 层次 | 不支持 | 本体不是层次状态机。 |
| 并发 / 同步 | 以逻辑并行方式支持 | 通过 existential / universal branching 同时展开多条检查分支。 |
| 时间约束 | 不支持 | 无时钟与时间语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散自动机。 |
| 可执行 / 可验证性 | 强理论支持 | regularity、determinization blow-up、complexity characterization 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$P=(Q,\Sigma,q_1,F,g)$` | alternating finite automaton 的基本骨架。 |
| 布尔转移 | `$g_i : \Sigma \times B^k \to B$` | 当前状态对所有后继真假值做布尔组合。 |
| 递归接受 | `$H_i(ax)(u)=g_i(a,H_1(x)(u),\ldots,H_k(x)(u))$` | alternating acceptance 的核心递归定义。 |
| 初始接受 | `$P$ accepts $x \iff H_1(x)(f)=1$` | 从初始状态计算整体真假值。 |
| 有限词边界 | `$L(P)$ regular` | AFA 不超出 regular languages。 |
| 状态爆炸 | `$2^{2^k}$` | DFA 模拟 AFA 的最坏状态代价。 |

## 构造方式与承载格式

### 建模入口

1. 先确定有限状态集与输入字母表。
2. 为每个状态定义一个布尔转移函数 `g_i`。
3. 指定哪些状态在空串上为接受状态。
4. 用 `H_i` 递归解释每个状态对任意后缀的真假值。

### 机器可处理承载方式

机器可处理承载方式是五元组和布尔函数，而不是图形 DSL 或交换文件。

### 交换与互操作

它最自然地互操作到：

1. 确定化自动机分析。
2. pushdown / tree automata 的 alternating 扩展。
3. complexity classes 的 alternating characterization。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是布尔转移函数和状态真值向量。
- 仿真/执行支持：可按递归真假值或 computation tree 展开。
- 验证/分析支持：determinization、regularity 和 complexity bounds 是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是后续 alternating word/tree automata 与 alternating complexity 理论的基础入口。

## 适用场景与需求前提

### 适用场景

适合表达“同一输入上需要同时满足若干分支检查”的词语言性质，也适合做更强 automata 家族的谱系母节点。

### 需求前提

1. 对象是离散符号串。
2. 需求可以写成对多个后继判断结果的布尔组合。
3. 更关注表达紧凑性和理论能力边界，而不是工程执行格式。

### 不适用或高成本场景

若需求主要是带数据守卫、时间或连续动力学的控制建模，则应转向 `EFSM`、`Timed Automata` 或 `Hybrid Automata`。

## 与相邻形式主义的关系

相对普通 nondeterministic finite automata，它把“存在一个后继可接受”推广成“存在 / 全称分支都可以出现”；相对 [alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md](../alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md)，这篇是更早的 computation-mode 母节点；相对 [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)，后者则是在 tree / infinite-tree 上的专门 acceptance 子类。

## 与本研究的关系

### 对 Project 1 的价值

它让 `Finite Automata` 主干上可以稳定补出 `Alternating Automata` 节点，为后续 tree 分支中的 `alternating / parity / co-Büchi` 口径提供母语。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和中间模型，而不是面向控制系统需求的默认最终交付形式。

### 对需求到模型生成的启发

当需求天然带有“同时检查多个分支义务”的结构时，LLM 生成模型时未必要只想 nondeterministic guessing，也可以考虑 alternating 风格的布尔后继语义。

### 现实限制

缺少工程格式和直接工具生态；控制系统侧通常还需要落到更具体的 automata / tree / timed 变体。

## 重要的相关工作

### 奠基或前身工作

- 经典 `Finite Automata` / nondeterministic automata 理论。

### 同类型或同家族工作

- [alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md](../alternating-tree-automata-parity-games-and-modal-mu-calculus/desc.md)
- [weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md](../weak-alternating-automata-the-weak-monadic-theory-of-the-tree-and-its-complexity/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合挂成 `Finite Automata` 主干下的 `Alternating Automata` 代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Alternating Automata`
- 论文角色：模型提出
- 核心功能：把 nondeterminism 推广为 existential / universal branching 并给出统一 alternating machine 语义。
- 关键特性：布尔后继组合、finite-case regularity、`2^{2^k}` 确定化代价、pushdown expressiveness gain、complexity characterization。
- 构造方式：`P=(Q,\Sigma,q_1,F,g)` + 递归接受函数 `H_i`。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：词语言分支检查、succinct specification、后续 alternating tree / pushdown 谱系节点。
- 需求前提：对象是离散符号串，且性质可写成对后继真假值的布尔组合。
- 状态：🟢
