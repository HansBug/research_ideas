# 由 Fredkin 门构造可逆有限自动机的方法 / A Simple Construction Method of a Reversible Finite Automaton out of Fredkin Gates, and Its Related Problem

## 基本信息

- 标题：A Simple Construction Method of a Reversible Finite Automaton out of Fredkin Gates, and Its Related Problem
- 中文标题：由 Fredkin 门构造可逆有限自动机的方法及其相关问题
- 作者：Kenichi Morita
- 发表：*The Transactions of the IEICE*, E73(6):978-984, 1990
- DOI：原文未提供
- 链接：https://hiroshima.repo.nii.ac.jp/record/2008960/files/TransIEICE_E73-6_978.pdf
- 形式主义：`Reversible Finite Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文没有软件实现，但给出了由 `Fredkin` 门、unit wire、decoder、permutation 模块拼装 `RFA` 与 reversible `PCA` 的硬件化构造方法。
- 标准/格式获取方式：原文不涉及 DSL / XML / 交换格式；核心承载方式是 `RFA` 元组、injective move function 和 conservative logic 电路模块。

## 简报

这篇论文的亮点不只是“用可逆门电路实现一个 automaton”，更关键的是它把 `Reversible Finite Automaton` 作为一个明确的有限状态家族写成标准元组，并用 injective transition-output map 说明“可逆”在有限自动机层面到底是什么意思。对当前文库来说，它正好补出 `Finite Automata` 主干上的 `Reversible Finite Automata` 节点，同时又把该节点和 reversible `PCA`、conservative logic 之间的旁系联系交代清楚。

- 形式主义定位：有限自动机主干上的 computation-mode 约束分支，强调 backward determinism。
- 构造方式简述：把每一步读取符号和输出符号的状态更新做成 `Q \times S` 上的单射，再将该单射实现为组合的 permutation 电路。
- 基础设施与场景简述：原文没有软件工具链，但给出了从 `Fredkin` 门和 unit wire 构造 `RFA` 及 reversible `PCA` 的系统方法，足以说明该 family 的结构骨架。

```text
有限状态 + 输出 -> injective move function -> reversible finite automaton -> Fredkin-gate conservative circuit
```

## 形式主义定义与核心对象

### 定义对象

论文第 2 节把 `RFA` 定义为“可逆的确定性有限自动机”，其中“可逆”不是指语言接受条件换个名字，而是要求每一步状态-符号变换本身可逆。

### 核心抽象

原文把 deterministic reversible finite automaton 写成：

$$
M = (Q, S, f, q_0)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `S` 是有限符号集，同时作为输入字母表和输出字母表。
3. `f : Q \times S \to Q \times S` 是 move function。
4. `q_0 \in Q` 是初始状态。

核心约束是：

$$
f \text{ is injective}
$$

这意味着：

$$
f(q, s) = f(q', s') \Rightarrow (q, s) = (q', s')
$$

上式中的符号逐项解释如下：

1. `(q,s)` 与 `(q',s')` 是两个可能的“当前状态 + 当前读入符号”组合。
2. 若它们经 `f` 映到同一个“下一状态 + 输出符号”组合，则这两个输入组合必然相同。
3. 因而机器在给定逆序输出时可以唯一回溯其运行。

### 一个最小例子与通俗解释

考虑一个两状态、两符号的 `RFA`：

$$
Q = \{q_0, q_1\},\qquad S=\{0,1\}
$$

并定义：

$$
\begin{aligned}
f(q_0,0)&=(q_0,0)\\
f(q_0,1)&=(q_1,0)\\
f(q_1,0)&=(q_0,1)\\
f(q_1,1)&=(q_1,1)
\end{aligned}
$$

这是 `Q \times S` 上的一个置换。比如当前处于 `q_0` 且读入 `1`，则输出 `0` 并转到 `q_1`。反过来，如果事后知道某一步得到了 `(q_1,0)`，由于 `f` 是单射，就能唯一确定它只能来自 `(q_0,1)`。

通俗地说，普通有限自动机像“只管往前走”的状态机；`RFA` 则像“每一步都必须可倒带”的状态机。它不允许两个不同的局部情况合流成同一个后继局部情况。

### 运行 / 接受 / 转移语义

若输入串为 `s_1 s_2 \cdots s_n`，则一步步运行可写成：

$$
(q_i, o_i) = f(q_{i-1}, s_i),\qquad i=1,\ldots,n
$$

上式中的符号逐项解释如下：

1. `q_{i-1}` 是第 `i` 步前的状态。
2. `s_i` 是第 `i` 个输入符号。
3. `o_i` 是第 `i` 步输出的符号。
4. `q_i` 是第 `i` 步后的状态。

因此，`RFA` 更自然地看作 string transducer，而不是只谈接受/拒绝的识别器。论文也正是沿着这一点，把 `RFA` 实现成 conservative logic circuit。

### 语义边界

相对普通 deterministic finite automaton，`RFA` 多出来的不是栈、时间或随机性，而是“局部更新必须可逆”。这使它仍保持有限状态骨架，却落在完全不同的 computation discipline 上。

### 关键性质与判定边界

论文最核心的结构结论不是某个复杂度界，而是构造性定理：

$$
\text{For any RFA } M=(Q,S,f,q_0),\ \text{there exists a semi-closed conservative circuit realizing } M
$$

这就是原文的 Theorem 1。它说明 `RFA` 不是抽象玩具，而是能稳定落到 `Fredkin` 门和 unit wire 上的可逆实现对象。

论文还把这种可逆性推广到一维 partitioned cellular automaton。原文写成：

$$
P = (Z, L, C, R, f_P)
$$

其中：

$$
f_P : R \times C \times L \to L \times C \times R
$$

并证明：

$$
P \text{ globally reversible } \iff P \text{ locally reversible}
$$

这条 Proposition 1 说明 `RFA` 不是孤立节点，而是 reversible automata / reversible CA 家族之间的桥。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是标准有限状态骨架。 |
| 事件 / 触发 | 强支持 | 每步按当前输入符号驱动。 |
| 守卫 / 数据 | 不支持 | 原始模型无变量与守卫。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 不支持 | 单机串行模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、确定性、可逆。 |
| 可执行 / 可验证性 | 支持 | 本体可直接实现为 reversible conservative circuit。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| RFA 元组 | `$M=(Q,S,f,q_0)$` | 可逆有限自动机的标准定义。 |
| 可逆约束 | `$f:Q\times S \to Q\times S$` injective | backward determinism 的根本来源。 |
| 逐步语义 | `$(q_i,o_i)=f(q_{i-1},s_i)$` | 把模型视为有限状态转导器。 |
| PCA 元组 | `$P=(Z,L,C,R,f_P)$` | 说明 `RFA` 可自然嵌入 reversible `PCA` 单元。 |
| 局部/全局可逆 | `global reversible \iff local reversible` | 把有限自动机节点桥接到 reversible cellular automata。 |

## 构造方式与承载格式

### 建模入口

建模时首先要确定：

1. 状态集合 `Q` 与符号集合 `S`。
2. 哪些 `(q,s)` 组合映到哪些 `(q',s')`。
3. 该映射是否在 `Q \times S` 上是单射。

### 机器可处理承载方式

原文的机器可处理承载方式有两层：

1. 抽象层：`RFA` 元组和注入式转移函数。
2. 实现层：`DECODER`、`PERM` 等电路模块拼接出的 conservative logic circuit。

### 交换与互操作

它与以下对象互操作最紧：

1. reversible / conservative logic。
2. reversible `PCA`。
3. 更广义的 reversible computing 家族。

## 配套基础设施

- 建模/编辑工具：原文未提供软件工具。
- 解析/交换/元模型支持：核心是元组与 permutation-like move function。
- 仿真/执行支持：可直接按逐步输出语义运行，也可落到 `Fredkin` 门电路。
- 验证/分析支持：injectivity 检查是模型级关键条件。
- 代码生成/转换支持：原文给的是硬件门级构造，不是程序代码生成。
- 标准化或社区生态：属于 reversible computing 与 conservative logic 的经典理论支线。

## 适用场景与需求前提

### 适用场景

适用于需要显式 backward determinism、可逆执行或热力学可逆计算抽象的场景。

### 需求前提

1. 对象仍可压成有限状态。
2. 每一步局部变换必须避免信息丢失。
3. 输出符号与下一状态足以唯一回溯前驱。

### 不适用或高成本场景

如果需求本来就是普通识别问题，`RFA` 会比 `DFA` 更苛刻；多数工程控制器也不需要这种强可逆性约束。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，它保留有限状态骨架，但把局部转移从“一般函数”收紧为 `Q \times S` 上的单射；相对 [cellular-automata/desc.md](../cellular-automata/desc.md)，它是单元级有限状态可逆模型，而不是格点整体动力学；相对 [local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md)，这篇更靠近有限自动机本体，并把可逆性与 reversible `PCA` 明确连通。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Reversible Finite Automata` 这个很经典、但常被混入“reversible computing 总论”而缺少单独节点的 family。

### 作为目标形式主义还是中间表示

通常更适合作为理论谱系节点和结构约束模板，而不是控制系统需求建模的默认终态。

### 对需求到模型生成的启发

如果某类需求天然要求动作可回溯、局部更新不能丢信息，那么 LLM 在生成状态机时可以显式检查“转移是否 injective”，而不是只检查 reachability 或 determinism。

### 现实限制

它缺少直接工程 DSL，且可逆性约束非常强；多数控制系统不会直接采用这一 family 作为最终实现语言。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)
- reversible computing / conservative logic 基础工作

### 同类型或同家族工作

- reversible partitioned cellular automata
- reversible Turing machines

### 标准 / 格式 / 工具链工作

- 原文无工程标准；实现载体是 `Fredkin` 门与 unit wire。

### 与本研究关系最紧的工作

- 它最适合补出“有限自动机在 computation discipline 上的可逆化分支”。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Reversible Finite Automata`
- 论文角色：模型提出
- 核心功能：把有限自动机的每一步局部更新收紧为可逆映射，并给出 `Fredkin` 门实现。
- 关键特性：有限状态、输出伴随状态更新、injective move function、可回溯运行、与 reversible `PCA` 相连。
- 构造方式：`Q \times S` 上的单射 + decoder / permutation 电路模块。
- 基础设施：无软件标准，但有明确 conservative logic 实现路径。

