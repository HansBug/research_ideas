# 单计数器语言识别札记 / A note on the recognition of one counter languages

## 基本信息

- 标题：A note on the recognition of one counter languages
- 中文标题：单计数器语言识别札记
- 作者：S. A. Greibach
- 发表：*Revue française d'automatique informatique recherche opérationnelle. Informatique théorique*, 9(2):5-12, 1975
- DOI：`10.1051/ita/197509r200051`
- 链接：https://www.numdam.org/article/ITA_1975__9_2_5_0.pdf
- 形式主义：`One-Counter Machines / One-Counter Languages`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论分析
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是单计数器机、on-line / off-line 输入头方式以及“empty counter + final state”接受纪律。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是单计数器机假设、复杂度上界和与 `PDA` / multi-head automata 的关系。

## 简报

这篇论文不是重新发明 `counter machine`，而是把 `k=1` 的单计数器分支单独拉出来，说明它在 recognition complexity 上明显比一般 `PDA` 或更高维计数器族更瘦、更好控。对当前文库来说，它正好把 [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md) 下面一直缺失的 `One-Counter` 节点补出来，也能解释为什么后来的 [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md) 要继续靠“受限相位切换”去换判定性。

- 形式主义定位：`Counter Machines` 母线下最经典、最瘦的单计数器子家族。
- 构造方式简述：保留有限控制和零测试，但把无界存储严格压成一只计数器，同时区分 on-line 与 off-line 输入头。
- 基础设施与场景简述：原文是纯理论工作，不过 acceptance convention、on-line / off-line 口径和 `n^2 / n^3 / n^2-space` 级别的识别上界都很清楚，足以作为树上的稳定分支节点。

```text
线性词输入 -> 有限控制 + 1 个计数器 -> empty-counter acceptance -> recognition complexity boundary
```

## 形式主义定义与核心对象

### 定义对象

论文没有重新给出一整套新 tuple，而是沿用既有 counter machine 定义，专门讨论“只有一只计数器”的情形，并明确补上三条工作约定：

1. 机器按 empty counter 与 final state 接受。
2. on-line 机器使用 one-way、left-to-right 输入带。
3. off-line 机器使用带两端端标记的 two-way read-only 输入带。

因此，这里的 `one-counter machine` 可以直接看成 [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md) 中 `k=1` 的特例。

### 核心抽象

若把上一条母线中的 `k` 取成 `1`，则单计数器机可保守写成：

$$
\mathcal O = (Q_p, Q_a, \Sigma, M, K, s_0, F)
$$

上式中的符号逐项解释如下：

1. `Q_p`、`Q_a`、`\Sigma`、`M`、`K`、`s_0`、`F` 的含义与一般 `Counter Machine` 相同。
2. 唯一差别是这里只有一个计数器，因此计数器值退化成单个整数 `c`。
3. 当前论文真正直接增加的是“输入头能否双向移动”和“接受必须同时满足空计数器与终态”这两层约束。

对当前论文而言，更直接、也更关键的形式化结论是复杂度上界。原文 Theorem 1 与 Theorem 3 可压成：

$$
L_{\mathrm{online\text{-}1C}} \subseteq \mathrm{DTIME}(n^2)
$$

$$
L_{\mathrm{offline\text{-}1C}} \subseteq \mathrm{TIME}(n^3) \cap \mathrm{SPACE}(n^2)
$$

上式中的符号逐项解释如下：

1. `L_{\mathrm{online\text{-}1C}}` 表示 on-line one-counter languages。
2. `L_{\mathrm{offline\text{-}1C}}` 表示 off-line one-counter languages。
3. `\mathrm{DTIME}(n^2)` 表示可由确定性 `TM` 在二次时间内识别。
4. `\mathrm{TIME}(n^3) \cap \mathrm{SPACE}(n^2)` 表示可由 `TM` 在三次时间、二次空间内接受。

### 一个最小例子与通俗解释

最典型的例子仍然是：

$$
L = \{ a^n b^n \mid n \ge 0 \}
$$

对一台 on-line one-counter machine 来说，它的工作方式可以理解成：

1. 沿输入带从左到右扫描。
2. 在 `a` 段不断加一。
3. 进入 `b` 段后不断减一。
4. 只有在计数器清空且到达接受状态时才接受。

通俗地说，`One-Counter Machine` 是“只能拿一只无界计数器的状态机”。它比普通 `FA` 强，因为它能记住任意大的差值；但它又比 `PDA` 弱，因为它只有一个高度而没有真正的栈字序列。

### 运行 / 接受 / 转移语义

当前论文最明确的接受约束是：

$$
\text{accept} \iff \text{empty counter} \land \text{final state}
$$

对 on-line 情形，这意味着机器一边向右扫描输入、一边维护计数器；对 off-line 情形，则允许输入头双向回看，但输入带本身仍是只读的。

论文第一个证明的核心，是把 on-line one-counter machine 的每一步配置，编码成确定性 `TM` 工作带上的一串集合：

$$
*E(S_0)* \cdots *E(S_i)* \cdots *E(S_{m_t})*
$$

这里的符号逐项解释如下：

1. `S_i` 编码“在读完前 `t` 个输入符号后、计数器值为 `i` 时可能处于哪些控制状态”。
2. `E` 是这些状态子集的编码。
3. 这使得单计数器的非确定性运行可以被确定性 `TM` 逐层更新出来。

### 语义边界

这个 family 的边界也很清楚：

1. 只有一只计数器，没有多计数器并行计数。
2. 接受纪律是 empty counter + final state，不是任意终止条件。
3. on-line 与 off-line 的差别只在输入头能力，不在存储结构本体。
4. 论文重点是 recognition complexity，而不是新的语义子类或工程承载格式。

### 关键性质与判定边界

原文给出的几个最值得保留的边界结论是：

1. every on-line one counter language can be accepted in time `n^2`。
2. deterministic on-line one-counter languages properly sit inside realtime `PDA` languages。
3. off-line nondeterministic one-counter machines admit `n^3` time and `n^2` space upper bounds。

可以再把其中一个包含关系压成：

$$
\mathrm{Det\text{-}online\text{-}1C} \subsetneq \mathrm{Realtime\ PDA}
$$

这说明单计数器虽然已经比普通有限自动机强，但仍然没有达到一般 `PDA` 的表达面。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然是有限控制。 |
| 事件 / 触发 | 强支持 | 由输入符号与计数器零测试驱动。 |
| 守卫 / 数据 | 部分支持 | 只有一个整数计数器，守卫主要是空 / 非空。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 不支持 | 单机串行识别模型。 |
| 时间约束 | 不支持 | 讨论的是识别复杂度，不是显式时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散计数模型。 |
| 可执行 / 可验证性 | 强理论支持 | 上界清晰，且与 `PDA` / multi-head family 的关系明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| family 定位 | `$\mathcal O = \mathcal C \text{ with } k=1$` | 说明它是 `Counter Machine` 的单计数器分支。 |
| 接受纪律 | `empty counter \land final state` | 论文明确固定了该 family 的接受口径。 |
| on-line 上界 | `$L_{\mathrm{online\text{-}1C}} \subseteq \mathrm{DTIME}(n^2)$` | 单计数器比一般 `CFL/PDA` 更容易识别。 |
| off-line 上界 | `$L_{\mathrm{offline\text{-}1C}} \subseteq \mathrm{TIME}(n^3)\cap \mathrm{SPACE}(n^2)$` | 双向输入头会提高复杂度，但仍可控。 |
| 与 `PDA` 关系 | `$\mathrm{Det\text{-}online\text{-}1C} \subsetneq \mathrm{Realtime\ PDA}$` | 说明 single-counter family 的表达边界。 |

## 构造方式与承载格式

### 建模入口

建模时需要先决定：

1. 这是不是一个“只需要一个无界计数”的问题。
2. 输入头只需 one-way，还是必须允许 two-way 回看。
3. 接受是否自然表达成“计数器清空 + 终态”。

### 机器可处理承载方式

原文的机器可处理承载方式仍然是机器元组、配置和状态集合编码，没有独立工程载体。

### 交换与互操作

它最自然地互操作到：

1. `Counter Machines` 的母线定义。
2. realtime / off-line `PDA` 复杂度比较。
3. multi-head finite state acceptor 与 `TM` 上界模拟。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是单计数器接受纪律与 complexity upper bound。
- 仿真/执行支持：可按单计数器配置转移直接执行。
- 验证/分析支持：与 `TM`、multi-head `FA`、`PDA` 的复杂度比较是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 classic automata theory 里从一般 `counter machine` 向 `PDA` 边界延展的经典细分节点。

## 适用场景与需求前提

### 适用场景

适用于只需要一个无界整数记忆、但希望保留非常瘦的自动机骨架的线性词识别场景。

### 需求前提

1. 结构记忆可压成单个计数差值，而不是一般栈串。
2. 需求中心是识别语言或分析复杂度，而不是图形化控制逻辑。
3. 若需要更强的嵌套结构，单计数器就不够。

### 不适用或高成本场景

如果需求需要多组无界计数同时演化，`multicounter` 更自然；如果需要完整调用/返回栈，`PDA` 更自然；如果需要树、网格或连续动态对象，它也不适合。

## 与相邻形式主义的关系

相对 [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)，它是最直接的 `k=1` 特例；相对 [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)，它只有计数高度、没有真正栈内容；相对 [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)，后者是朝“更多计数器但更强约束”方向走的另一条分支。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Counter Machines` 这条母线下面最基础的 `One-Counter` 子节点正式补入演化树，使 `counter -> one-counter -> reversal-bounded multicounter` 的局部结构更加完整。

### 作为目标形式主义还是中间表示

它更适合作为理论族谱中的分支节点，而不是控制系统建模的默认终点；不过对于“需求里只有单调计数差”的情形，它提供了比 `PDA` 更瘦、更容易分析的参照。

## 重要的相关工作

1. [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)：更一般的 `Counter Machines` 母节点。
2. [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)：在多计数器方向进一步靠限制反转次数换判定性。
3. [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)：与单计数器最邻近的更强存储增强自动机。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它稳定刻画了 `One-Counter` family 的接受口径与复杂度边界，而不是单纯某个算法技巧。
- 它应挂在 `Finite Automata -> Counter Machines` 之下，而不应再直接孤立地挂在 `reversal-bounded` 旁边。
- 它不是 DSL、工具或应用论文，也不是仅用 one-counter 做案例验证的 side paper。
