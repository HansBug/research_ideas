# 正则函数与代价寄存器自动机 / Regular Functions and Cost Register Automata

## 基本信息

- 标题：Regular Functions and Cost Register Automata
- 中文标题：正则函数与代价寄存器自动机
- 作者：Rajeev Alur, Loris D'Antoni, Jyotirmoy Deshmukh, Mukund Raghothaman, Yifei Yuan
- 发表：*2013 28th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS 2013)*, pp. 13-22
- DOI：`10.1109/LICS.2013.65`
- 链接：https://www.cis.upenn.edu/~alur/Lics13reg.pdf
- 形式主义：`Cost Register Automata (CRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立实现；机器可处理入口是 cost grammar、register update table 与 final cost function。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `CRA` 元组、cost grammar 与 semiring-style register expressions。

## 简报

这篇论文给 quantitative automata 做了一件很关键的事：把“字符串到代价值”的 regular function 从 weighted automata 的 nondeterministic 传统里拉出来，给出一个 deterministic 的寄存器式机器模型 `CRA`。它因此成为 `Weighted Automata` 旁边那条 `cost-register` 子枝的母节点。

- 形式主义定位：`Finite Automata -> 加权 / 随机扩展` 支线里连接 `Weighted Automata` 与 `copyless CRA` 的关键母型。
- 构造方式简述：机器在有限状态控制下维护若干 write-only cost registers；每读一个输入符号，就按给定 cost grammar 对寄存器做并行更新。
- 基础设施与场景简述：原文把 CRA 与 regular cost functions、weighted automata、streaming tree transducer 和多种 min-cost / equivalence 算法系统接通。

```text
输入串 -> 有限状态 + cost registers -> semiring / cost-grammar update -> string-to-cost regular function
```

## 形式主义定义与核心对象

### 定义对象

`CRA` 处理的是 string-to-cost functions：输入是有限字符串，输出是某个 cost domain 上的值，例如加和、最小值、折扣值等。关键点在于：输出不再是字符串，而是代价。

### 核心抽象

原文先定义 cost grammar `G=(F,T)`，再在其上给出 cost register automaton：

$$
M = (\Sigma, Q, q_0, X, \delta, \rho, \mu)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入字母表。
2. `Q` 是有限状态集。
3. `q_0 \in Q` 是初始状态。
4. `X` 是有限个代价寄存器。
5. `\delta : Q \times \Sigma \to Q` 是状态转移函数。
6. `\rho : Q \times \Sigma \times X \to E(G,X)` 是寄存器更新函数。
7. `\mu : Q \to E(G,X)` 是 partial final cost function。

其中 `E(G,X)` 是把 cost grammar 里的叶子节点扩展为“常量或寄存器名”后得到的表达式集合。

### 一个最小例子与通俗解释

一个最小例子是“计算输入串里 `a` 的个数”。取一个寄存器 `x`，初始值为 `0`，然后：

$$
x := x + 1 \quad \text{on } a,\qquad x := x \quad \text{on } b
$$

最后输出 `x`。这就是最简单的 `CRA`。

通俗地说，`CRA` 像“只能写、不能测的代价记账机”。它不像 data automata 那样拿寄存器做比较，而是把寄存器当成若干代价表达式槽，不断累积和组合成本。

### 运行 / 接受 / 转移语义

给定 cost model `C=(G,D,\llbracket \cdot \rrbracket)`，`CRA` 的 configuration 是 `(q,\nu)`，其中 `q \in Q`，`\nu : X \to D` 给出每个寄存器当前的代价值。

读入符号 `a` 后，配置更新满足：

$$
(q,\nu) \xrightarrow{a} (\delta(q,a), \nu')
$$

其中 `\nu'` 由 `\rho(q,a,\cdot)` 的并行赋值决定。若对整个输入串 `w` 最终到达状态 `q`，则输出为：

$$
\llbracket M, C \rrbracket (w) = \llbracket \mu(q) \rrbracket_{\nu}
$$

上式中的符号逐项解释如下：

1. `\nu` 是终态时各寄存器的 valuation。
2. `\mu(q)` 指定在状态 `q` 下如何从寄存器表达式读出最终代价。
3. `\llbracket \cdot \rrbracket_{\nu}` 表示把表达式中出现的寄存器用 valuation 展开并在 cost domain 中求值。

### 语义边界

`CRA` 的寄存器是 write-only 的：它们用来构造代价，而不是做测试。这一点和 classic register automata 差异极大。它的核心边界则由 two things 决定：允许哪些 cost operations，以及是否加 copyless restriction。

### 关键性质与判定边界

对 additive cost functions，论文证明：

$$
F(D;+c) = F_c(D;+) = R(D;+c) = R(D;+)
$$

也就是说 regular additive cost functions 与相应的 CRA / copyless CRA 类在表达力上吻合。

对 semiring 情形，论文给出：

$$
F_c(D \times D, \oplus, \otimes c, [\cdot]) \equiv R(D,\oplus,\otimes d)
$$

并进一步证明 weighted automata 与不受 copyless 限制的 CRA 精确对应：

$$
F(D,\oplus,\otimes c) \equiv \text{Weighted Automata}
$$

对典型决策问题，原文还给出：

$$
\mathrm{min\text{-}cost}(\mathrm{CRA\ over}\ (\mathbb Q,+c)) \in \mathrm{PTIME}
$$

以及

$$
\mathrm{equivalence}(\mathrm{CRA\ over}\ (\mathbb Q,+)) \in \mathrm{PTIME}
$$

这说明 `CRA` 不是只“更 deterministic 更漂亮”，同时也保留了大量可分析性。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制仍是核心。 |
| 事件 / 触发 | 强支持 | 每个输入符号触发一次寄存器并行更新。 |
| 守卫 / 数据 | 部分支持 | 支持寄存器表达式更新，但寄存器不用于测试。 |
| 层次 | 不支持 | 输入对象仍是线性串。 |
| 并发 / 同步 | 不支持 | 非并发模型。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 部分支持 | 可表达定量/半环代价，但不是概率自动机。 |
| 可执行 / 可验证性 | 强理论支持 | min-cost、equivalence、weighted-automata correspondence 都很成熟。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=(\Sigma,Q,q_0,X,\delta,\rho,\mu)$` | `CRA` 的标准定义。 |
| configuration | `$(q,\nu)$` | 当前状态加寄存器 valuation。 |
| additive expressiveness | `$F(D;+c)=F_c(D;+)=R(D;+c)=R(D;+)$` | additive regular cost functions 与 CRA 族对齐。 |
| weighted bridge | `$F(D,\oplus,\otimes c)\equiv \text{Weighted Automata}$` | 非 copyless CRA 与 weighted automata 等价。 |
| min-cost / equivalence | `PTIME` | `CRA` 保留了关键算法可解性。 |

## 构造方式与承载格式

### 建模入口

1. 先确定 cost domain 与允许的 operations，例如 `+`、`min`、discount。
2. 再定义 cost grammar。
3. 选择有限状态控制与寄存器集合。
4. 为每个 `(state, input, register)` 指定更新表达式。
5. 最后用 `\mu` 指定终态输出表达式。

### 机器可处理承载方式

机器可处理承载方式是：

1. cost grammar。
2. register update table。
3. final cost expression。

没有统一 XML / JSON / DSL。

### 交换与互操作

相对 [weighted-logics-and-weighted-automata-survey/survey.md](../weighted-logics-and-weighted-automata-survey/survey.md) 覆盖的 weighted automata 主线，`CRA` 提供 deterministic register-based counterpart；相对 [copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md](../copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md)，这是更一般的母模型；相对 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)，它把“输出是字符串”改成“输出是 cost value”。

## 配套基础设施

- 建模/编辑工具：原文未提供独立工具。
- 解析/交换/元模型支持：核心是 cost grammar、register valuation、copyless / substitution discipline。
- 仿真/执行支持：天然支持单遍、确定性代价累积执行。
- 验证/分析支持：min-cost、equivalence、weighted-automata translation、semiring reasoning。
- 代码生成/转换支持：原文未讨论工程代码生成，但给出与 weighted automata / SSTT 的理论转换。
- 标准化或社区生态：是 regular cost functions、quantitative verification 和 copyless CRA 理论的母节点。

## 适用场景与需求前提

### 适用场景

适合 string-to-cost regular function、能耗 / 价格 / 惩罚累计、带 `min` 或折扣的有限状态 quantitative analysis。

### 需求前提

1. 输入是线性串。
2. 输出是某个 cost domain 上的值，而不是结构化对象。
3. 代价更新可由有限个寄存器和有限状态控制表达。

### 不适用或高成本场景

若需求要输出字符串 / 树而非 cost，应转向 `SST / STT`；若需要概率接受语义，则 `Probabilistic / Weighted` 支线更直接；若只关心 copyless 子类边界，则应进一步看 copyless CRA。

## 与相邻形式主义的关系

相对 `Weighted Automata`，`CRA` 是 deterministic register view；相对 [copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md](../copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md)，它是其母节点；相对 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)，两者都用寄存器和单遍更新，但一个输出字符串、一个输出代价。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Weighted Automata` 旁边的 quantitative 分支从 survey 级概念落成了正式树节点，并为已有的 copyless CRA 提供了直接父节点。

### 作为目标形式主义还是中间表示

更适合作为定量需求的中间表示或理论节点，不适合作为一般控制器的最终状态机语言。

### 对需求到模型生成的启发

如果需求描述里显式出现“累计代价”“最小成本”“折扣收益”“资源开销”等量化目标，LLM 可以考虑先抽成 CRA 风格模型，而不是只生成 Boolean 状态机。

### 现实限制

原文的强项在理论整合，不在工程生态；没有公开工具和标准格式，因此更适合做谱系与理论能力边界工作。

## 重要的相关工作

### 奠基或前身工作

- [on-the-definition-of-a-family-of-automata/desc.md](../on-the-definition-of-a-family-of-automata/desc.md)
- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 同类型或同家族工作

- [copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md](../copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或交换格式。

### 与本研究关系最紧的工作

- 它最适合挂到演化树 `Weighted Automata -> Cost Register Automata` 的母节点位置。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Cost Register Automata (CRA)`
- 论文角色：模型提出
- 核心功能：用有限状态与 write-only cost registers 计算 regular string-to-cost functions。
- 关键特性：cost grammars、copyless discipline、weighted-automata bridge、min-cost / equivalence analyzability。
- 构造方式：`(\Sigma,Q,q_0,X,\delta,\rho,\mu)` 元组加 cost grammar 和 register update table。
- 基础设施：纯理论模型，无工程标准；核心是与 weighted automata、SSTT 和 semiring algorithms 的连接。
- 适用场景：定量语言、资源 / 能耗 / 价格分析、string-to-cost functions。
- 需求前提：输入是线性串，输出是 cost domain 上的值，且更新规则可压成有限寄存器表达式。
- 状态：🟢
