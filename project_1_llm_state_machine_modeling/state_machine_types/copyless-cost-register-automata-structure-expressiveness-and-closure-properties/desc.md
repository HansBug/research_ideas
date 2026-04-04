# 无复制代价寄存器自动机：结构、表达力与闭包性质 / Copyless Cost-Register Automata: Structure, Expressiveness, and Closure Properties

## 基本信息

- 标题：Copyless Cost-Register Automata: Structure, Expressiveness, and Closure Properties
- 中文标题：无复制代价寄存器自动机：结构、表达力与闭包性质
- 作者：Filip Mazowiecki, Cristian Riveros
- 发表：*33rd Symposium on Theoretical Aspects of Computer Science (STACS 2016)*, LIPIcs 47, Article 53, pp. 53:1-53:13, 2016
- DOI：`10.4230/LIPIcs.STACS.2016.53`
- 链接：https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2016.53
- 形式主义：`Copyless Cost-Register Automata (copyless CRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：能力边界
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `CRA` 元组、semiring expressions/substitutions、copyless updates 和 output expression。
- 标准/格式获取方式：原文没有工程 DSL 或交换标准，核心承载方式是 deterministic state graph、register substitution 表和 semiring 语义。

## 简报

这篇论文研究 `Cost Register Automata` 的 copyless 子类：每次更新或输出时，每个旧寄存器值在右侧最多用一次。它一方面给出 copyless `CRA` 的 normal form、stable registers 和结构分析工具，另一方面证明 copyless `CRA` 严格弱于 `Weighted Automata`，且对 reverse 不闭包，从而把 `Weighted Automata` 附近那条“寄存器式定量自动机”分支的边界画得很清楚。

- 形式主义定位：`Weighted Automata` 旁边的 deterministic register-based quantitative automata 子枝，用 semiring registers 计算字符串到代价/权值的函数。
- 构造方式简述：有限状态机每读一个输入符号，就用一个 semiring substitution 并行更新所有寄存器；copyless 约束禁止同一旧寄存器在一次更新中被重复复制。
- 基础设施与场景简述：原文是纯理论模型，但给出 normal form、稳定寄存器分析、与 `WA` 的严格表达力分离，以及 `BAC` 子类的闭包结果。

```text
输入字符串 -> DFA-like control + semiring registers + copyless substitution -> 输出代价 / 权值函数
```

## 形式主义定义与核心对象

### 定义对象

`copyless CRA` 处理的是从字符串到 semiring 值的函数 `f:\Sigma^* \to S`。它不是布尔语言接受器，而是一个 deterministic finite-state skeleton 上叠加 semiring registers 的定量函数机。

### 核心抽象

原文先定义 `CRA`：

$$
A = (Q,\Sigma,X,\delta,q_0,\nu_0,\mu)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集。
2. `\Sigma` 是输入字母表。
3. `X` 是寄存器集合。
4. `\delta:Q\times\Sigma\to Q\times\mathrm{Subs}(X)` 是转移函数。
5. `q_0` 是初始状态。
6. `\nu_0:X\to S` 是初始 valuation。
7. `\mu:Q\to\mathrm{Expr}(X)` 是 final output expression。

在固定 semiring

$$
S=(S,\oplus,\odot,0,1)
$$

上式中的符号逐项解释如下：

1. `S` 是值域集合。
2. `\oplus` 是分支/项聚合运算。
3. `\odot` 是项内组合运算。
4. `0` 和 `1` 是对应单位元。

copyless 限制要求：每个表达式里同一变量最多出现一次；并且一个 substitution `\sigma` 中，不同目标寄存器右侧使用的变量集合两两不交。

### 一个最小例子与通俗解释

原文的 Example 1 在 `\mathbb N_{-\infty}(\max,+)` 上计算“输入串中最长连续 `b` 段长度”。机器用寄存器 `x` 记录当前 `b` 后缀长度，用 `y` 记录目前见过的最大 `b` 段长度；读到 `b` 时做 `x:=x+1, y:=y`，读到 `a` 时做 `x:=0, y:=\max\{x,y\}`，最终输出 `\max\{x,y\}`。这些更新都是 copyless 的，因为每个旧寄存器值不会在一次 substitution 里被重复复制。

通俗地说，copyless `CRA` 像“边扫字符串边维护几个数值槽位的确定性状态机”，但它不允许把同一个旧槽位值在一次更新里到处复制，因此比一般 `CRA` 更规整，也比 `WA` 更容易暴露结构边界。

### 运行 / 接受 / 转移语义

对输入串 `w=a_1\cdots a_n`，原文把 run 写成：

$$
(q_0,\nu_0)\xrightarrow{a_1}(q_1,\nu_1)\xrightarrow{a_2}\cdots\xrightarrow{a_n}(q_n,\nu_n)
$$

并要求若 `\delta(q_{i-1},a_i)=(q_i,\sigma_i)`，则：

$$
\nu_i(x)=\llbracket \nu_{i-1}\circ\sigma_i(x)\rrbracket
$$

最终输出语义是：

$$
\llbracket A \rrbracket(w)=\llbracket \nu_n\circ\mu(q_n)\rrbracket
$$

上面三式中的符号逐项解释如下：

1. `\sigma_i` 是读入第 `i` 个符号时选择的寄存器 substitution。
2. `\nu_i` 是第 `i` 步后的 valuation。
3. `\llbracket \cdot \rrbracket` 是把 ground expression 按 semiring 解释成具体值。
4. `\mu(q_n)` 是终态对应的输出表达式。

### 语义边界

相对 [on-the-definition-of-a-family-of-automata/desc.md](../on-the-definition-of-a-family-of-automata/desc.md) 的 `Weighted Automata`，copyless `CRA` 用寄存器 substitution 替代路径权值累积，因此更像 deterministic program-style accumulation；但 copyless 限制又让它严格弱于 `WA`。相对 `SST/STT` 的 copyless variables，这里输出不是字符串/树，而是 semiring 值。

### 关键性质与判定边界

原文首先证明每个 copyless `CRA` 都可化到 normal form，并据此识别 stable registers。更重要的表达力边界是：

$$
\mathrm{copyless\ CRA} \subsetneq \mathrm{WA}
$$

并且：

$$
\mathrm{copyless\ CRA} \text{ is not closed under reverse.}
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{copyless\ CRA}` 是满足 copyless substitution/output 限制的 `CRA` 函数类。
2. `\mathrm{WA}` 是 weighted automata 定义的字符串到 semiring 值函数类。
3. reverse 闭包指：对任意 `f(w)`，是否总能在同类中定义 `f^r(w^r)=f(w)`。

论文随后指出 bounded alternation copyless `CRA` (`BAC`) 比一般 copyless `CRA` 更 robust，并对 unambiguous nondeterminism、regular look-ahead 和 reverse 保持闭包。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制直接决定采用哪个 substitution。 |
| 事件 / 触发 | 强支持 | 每个输入符号触发一次寄存器并行更新。 |
| 守卫 / 数据 | 强支持 | semiring registers 和 copyless expressions 是核心。 |
| 层次 | 不支持 | 输入对象是线性串。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 部分支持 | 可表达定量/代价语义，但不是连续动力学或概率转移模型。 |
| 可执行 / 可验证性 | 强理论支持 | 有 normal form、stable-register 分析和表达力/闭包边界。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,\Sigma,X,\delta,q_0,\nu_0,\mu)$` | `CRA` / copyless `CRA` 的 deterministic register skeleton。 |
| 单步 valuation 更新 | `$\nu_i(x)=\llbracket\nu_{i-1}\circ\sigma_i(x)\rrbracket$` | 每步按 substitution 并行更新寄存器值。 |
| 输出语义 | `$\llbracket A \rrbracket(w)=\llbracket\nu_n\circ\mu(q_n)\rrbracket$` | 读完整个串后由终态输出表达式产生 semiring 值。 |
| 表达力边界 | `$\mathrm{copyless\ CRA}\subsetneq\mathrm{WA}$` | copyless 限制使模型严格弱于 weighted automata。 |
| 非 reverse 闭包 | `$\mathrm{copyless\ CRA}$ not reverse-closed` | 该类函数对输入反向不稳定。 |

## 构造方式与承载格式

### 建模入口

1. 先选定 semiring 和目标函数 `f:\Sigma^*\to S`。
2. 设计状态集、寄存器集合和初始 valuation。
3. 为每个“状态 + 输入符号”写出 copyless substitution。
4. 为每个终态写出 copyless output expression。
5. 若要做理论分析，再把机器化到 normal form 并识别 stable registers。

### 机器可处理承载方式

机器可处理承载方式是 deterministic transition graph、register substitutions、output expressions 和 semiring 解释函数；原文没有专用文件格式。

### 交换与互操作

它与 [on-the-definition-of-a-family-of-automata/desc.md](../on-the-definition-of-a-family-of-automata/desc.md) 的 `Weighted Automata` 直接形成父子/边界关系，也与 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md) 和 [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md) 的 copyless-variable 思路有明显旁系联系。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 semiring expressions、substitutions、valuations 和 normal-form transformation。
- 仿真/执行支持：可按 DFA-like run 和寄存器 substitution 直接解释执行。
- 验证/分析支持：normal form、stable register、inexpressibility、closure analysis 和 `BAC` 子类比较是重点。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 weighted automata / cost-register automata / regular cost functions 理论线。

## 适用场景与需求前提

### 适用场景

适合字符串到代价/分数/长度/最大值等 semiring 函数的理论建模，尤其是希望保留 deterministic state skeleton 且寄存器更新能写成 copyless expressions 的场景。

### 需求前提

1. 输入对象是线性字符串。
2. 目标输出是 semiring 值，而不是布尔接受或结构化树输出。
3. 每步旧寄存器值的复用方式可以满足 copyless 限制。

### 不适用或高成本场景

如果函数本身依赖 reverse-robust behavior、需要 `WA` 级别的完整表达力，或输出是字符串/树结构，那么一般 copyless `CRA` 就不是最合适模型。

## 与相邻形式主义的关系

相对 [on-the-definition-of-a-family-of-automata/desc.md](../on-the-definition-of-a-family-of-automata/desc.md) 的 `Weighted Automata`，copyless `CRA` 更像 deterministic register program，但表达力更弱；相对 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)，它们都用 copyless 更新，但输出域从字符串变成 semiring；相对一般 `CRA`，这里用 copyless 限制换来更清楚的结构理论，同时也暴露出非 reverse 闭包。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Weighted Automata` 下的 cost-register 子枝补出来，让演化树在“布尔接受 -> 权值累计 -> 寄存器式代价计算”这条线更完整。

### 作为目标形式主义还是中间表示

更适合作为含代价/打分需求的中间表示或理论旁支节点，而不是控制系统主线的默认输出形式主义。

### 对需求到模型生成的启发

如果需求文本不只是“某 trace 是否可接受”，而是“每条 trace 要计算一个最大代价、累计分数或最优值”，那么可以考虑让 LLM 先生成 copyless `CRA` 风格的寄存器更新式定量模型，再决定是否需要退回 `WA` 或升级到更强 cost model。

### 现实限制

copyless `CRA` 严格弱于 `WA` 且不 reverse-closed，说明它并不是一个万能定量母型；若任务强依赖双向扫描或反向稳定性，优先考虑 `BAC` 或其他 weighted/transducer 模型。

## 重要的相关工作

### 奠基或前身工作

- [on-the-definition-of-a-family-of-automata/desc.md](../on-the-definition-of-a-family-of-automata/desc.md)
- [weighted-automata-algorithms/desc.md](../weighted-automata-algorithms/desc.md)

### 同类型或同家族工作

- [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)
- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或公共工具线。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树的 `Weighted Automata` 下，形成 `Copyless Cost-Register Automata` 子枝，并为后续继续追一般 `CRA / BAC / regular cost functions` 留入口。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Copyless Cost-Register Automata (copyless CRA)`
- 论文角色：能力边界
- 核心功能：用 copyless semiring-register updates 计算字符串到代价函数，并刻画其相对 `WA` 的结构和闭包边界。
- 关键特性：copyless substitutions、normal form、stable registers、`copyless CRA \subsetneq WA`、非 reverse 闭包、`BAC` robust 子类。
- 构造方式：`A=(Q,\Sigma,X,\delta,q_0,\nu_0,\mu)` + copyless substitution/output expressions + semiring valuation semantics。
- 基础设施：纯理论模型，无工程标准或工具。
- 适用场景：字符串到代价/权值函数建模、weighted automata 子类比较、deterministic quantitative register updates。
- 需求前提：输入是线性串，输出是 semiring 值，且每步寄存器更新可满足 copyless 限制。
- 状态：🟢
