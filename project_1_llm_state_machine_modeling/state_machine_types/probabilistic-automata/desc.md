# 概率自动机 / Probabilistic Automata

## 基本信息

- 标题：Probabilistic Automata
- 中文标题：概率自动机
- 作者：Michael O. Rabin
- 发表：Information and Control, 6(3):230-245, 1963
- DOI：`10.1016/S0019-9958(63)90290-0`
- 链接：https://perso.ens-lyon.fr/denis.kuperberg/CR18/probas.pdf
- 形式主义：Probabilistic Automata
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 transition probability table、stochastic matrices 与 cut-point acceptance。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `$A(\sigma)$` 随机矩阵、接受概率 `$p(x)$` 与 cut-point `$\\lambda$`。

## 简报

这篇论文把有限自动机从“布尔接受器”推广成“带随机转移的有限状态机”。给定输入词后，机器不会得到单一终态，而是得到一个到各个终态的概率分布；是否接受，由接受概率是否超过 cut-point 决定。Rabin 的核心结论非常经典：一般 cut-point 语义下，概率自动机可以超出 regular event；但如果 cut-point 是 isolated 的，那么整台机器又能归约回某个普通确定自动机。

- 形式主义定位：有限自动机主干上的随机/概率扩展分支。
- 构造方式简述：用 stochastic transition table 取代普通确定迁移，并用 `$T(\mathcal A, \lambda)$` 定义 cut-point 语言。
- 基础设施与场景简述：原文服务不可靠顺序电路和 stochastic matrix product 分析，没有工程工具，但为后来 probabilistic automata、cut-point language 与随机电路语义提供了最早骨架。

```text
输入词 -> stochastic matrices -> 接受概率 p(x) -> cut-point λ -> 语言 T(A, λ)
```

## 形式主义定义与核心对象

### 定义对象

论文把 `Probabilistic Automata` 描述成和普通有限自动机几乎一样的有限状态系统，只是每次读入符号后，不再确定地跳到某个单一状态，而是按一个概率分布跳转到若干可能状态。

### 核心抽象

原文 Definition 4 给出的模型可写成：

$$
\mathcal A = (S, M, s_0, F)
$$

其中：

$$
M : S \times \Sigma \to [0,1]^{n+1}
$$

并且对每个 `(s,\sigma)` 满足：

$$
\sum_{i=0}^{n} p_i(s,\sigma) = 1,\qquad p_i(s,\sigma)\ge 0
$$

上式中的符号逐项解释如下：

1. `S = \{s_0,\dots,s_n\}` 是有限状态集。
2. `\Sigma` 是输入字母表。
3. `M(s,\sigma)` 返回从状态 `s` 读入 `\sigma` 后，进入各个状态的概率向量。
4. `F \subseteq S` 是接受状态集。

原文随后把每个输入符号 `\sigma` 写成随机矩阵：

$$
A(\sigma) = [p_j(s_i,\sigma)]_{0\le i,j\le n}
$$

对词 `x = \sigma_1 \sigma_2 \cdots \sigma_m`，定义：

$$
A(x) = A(\sigma_1)A(\sigma_2)\cdots A(\sigma_m)
$$

若 `F = \{s_{i_0},\dots,s_{i_r}\}`，则接受概率为：

$$
p(x) = \sum_{i\in I} p_i(s_0, x)
$$

这里的符号逐项解释如下：

1. `A(x)` 是读完整个词后的总转移矩阵。
2. `p_i(s_0,x)` 是从初始状态 `s_0` 出发读入 `x` 后落在状态 `s_i` 的概率。
3. `I` 是接受状态对应的下标集合。
4. `p(x)` 是词 `x` 的总接受概率。

### 一个最小例子与通俗解释

一个最小例子可以取两个状态 `s_0`、`s_1`，其中 `s_1` 为接受态。假设读到输入 `a` 时，从 `s_0` 以 `1/2` 的概率留在 `s_0`，以 `1/2` 的概率转到 `s_1`；从 `s_1` 总是留在 `s_1`。这样输入越长，进入接受态的概率就越大。

通俗地说，`Probabilistic Automata` 像一个“会掷骰子”的有限状态机。普通 `FSM` 最终只会说“接收/拒绝”，而它会先算出一个接受概率，再由 cut-point 决定这个词属于语言还是不属于语言。

### 运行 / 接受 / 转移语义

原文 Definition 7 用 cut-point 定义语言：

$$
T(\mathcal A, \lambda) = \{x \in \Sigma^* \mid \lambda < p(x)\}
$$

也就是说，输入词 `x` 是否被接受，并不直接取决于某次具体随机运行，而是取决于接受概率是否超过阈值 `\lambda`。

论文进一步定义 isolated cut-point：

$$
\exists \delta > 0\ \forall x \in \Sigma^* \quad |p(x)-\lambda| \ge \delta
$$

若 `\lambda` 满足这条性质，就意味着所有词的接受概率都与 cut-point 保持一个统一正间隔。

### 语义边界

这个模型的语义边界不只看状态数，还高度依赖 cut-point 选择。一般 cut-point 下，它可以定义非 regular 语言；但一旦 cut-point isolated，概率语义又会塌缩回普通确定自动机可识别的范围。

### 关键性质与判定边界

原文最重要的三条结论是：

$$
\exists \mathcal A,\ \lambda \quad T(\mathcal A,\lambda) \notin \mathrm{REG}
$$

也就是概率自动机一般严格强于确定有限自动机。

但若 `\lambda` isolated，则有 Reduction Theorem：

$$
\lambda \text{ isolated } \implies \exists D\ \text{ deterministic automaton},\ T(\mathcal A,\lambda)=T(D)
$$

此外，论文还讨论了所谓 actual automata，并指出它们在语言定义能力上会进一步受限。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 仍是有限状态控制。 |
| 事件 / 触发 | 支持 | 输入字母触发概率迁移。 |
| 守卫 / 数据 | 不支持 | 无显式变量守卫。 |
| 层次 | 不支持 | 平坦有限状态机。 |
| 并发 / 同步 | 不支持 | 单串、单机语义。 |
| 时间约束 | 不支持 | 无时钟语义。 |
| 连续动态 / 随机性 | 强支持 | 转移是随机的，并通过 cut-point 定义语言。 |
| 可执行 / 可验证性 | 部分支持 | 可做矩阵分析与 isolated cut-point 归约，但一般 cut-point 语言更复杂。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$\mathcal A=(S,M,s_0,F)$` | 用有限状态和概率转移表定义机器。 |
| 随机矩阵 | `$A(x)=A(\sigma_1)\cdots A(\sigma_m)$` | 用矩阵乘积累计词的随机效应。 |
| 接受概率 | `$p(x)=\sum_{i\in I} p_i(s_0,x)$` | 输入词对应的总接受概率。 |
| cut-point 语言 | `$T(\mathcal A,\lambda)=\{x\mid \lambda < p(x)\}$` | 由阈值决定属于语言还是不属于语言。 |
| 隔离阈值 | `$\exists\delta>0\ \forall x,\ |p(x)-\lambda|\ge\delta$` | 这是归约回确定自动机的关键条件。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 有限状态集与接受状态集。
2. 每个输入字母对应的随机转移矩阵。
3. cut-point `\lambda`。

### 机器可处理承载方式

机器可处理的核心承载是 stochastic matrix family `\{A(\sigma)\}`、输入词矩阵积 `A(x)` 和接受概率函数 `p(x)`。

### 交换与互操作

原文没有工程交换标准，但它和随机矩阵乘积、数值近似、顺序电路可靠性分析之间的互操作关系非常明确。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是随机矩阵表示。
- 仿真/执行支持：可按随机迁移运行，也可按矩阵乘积求接受概率。
- 验证/分析支持：isolated cut-point 可归约到确定自动机；一般 cut-point 需做概率/矩阵分析。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：后续形成 probabilistic automata、stochastic language 与 cut-point language 的理论路线。

## 适用场景与需求前提

### 适用场景

适合处理输入是线性词、系统内部状态有限，但转移具有随机性、不可靠性或统计判定阈值的场景。

### 需求前提

1. 输入对象仍是离散符号串。
2. 随机性主要体现在有限状态转移上。
3. 语言语义允许通过 cut-point 由概率转成布尔判定。

### 不适用或高成本场景

若需求包含显式连续动力学、复杂并发交互或时钟约束，仅靠概率自动机并不足够。

## 与相邻形式主义的关系

相对普通 `Finite Automata`，它把确定/非确定转移推广成概率分布；相对 `Weighted Automata`，它的权值必须满足随机矩阵约束并通过 cut-point 解释为语言；相对后来的 `Stochastic Hybrid Automata`，它没有连续变量和混成动力学。

## 与本研究的关系

### 对 Project 1 的价值

它补全了演化树里“有限状态 -> 随机有限状态”这条经典 automata theory 支线，使后续概率扩展不再只挂在混成主干上。

### 作为目标形式主义还是中间表示

更适合作为特定随机需求的专用目标形式，而不是通用控制系统默认终点。

### 对需求到模型生成的启发

它提示我们：如果需求中的不确定性主要体现在“转移概率”和“阈值接受”上，就不必一开始就跳到混成/连续模型；有限状态的随机扩展已经足够形成独立分支。

### 现实限制

它对结构、时间和并发的表达都很弱，因此通常只覆盖某一类随机语义子问题。

## 重要的相关工作

### 奠基或前身工作

- Rabin 与 Scott 的 `Finite Automata`。

### 同类型或同家族工作

- cut-point language 与后续 probabilistic automata 研究。
- `Weighted Automata` 与数值语言模型。

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具链。

### 与本研究关系最紧的工作

- 这条分支为后续把“随机性”纳入状态机族谱系提供了最早、最经典的母节点。

## 文献分类总结

- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Probabilistic Automata
- 论文角色：模型提出
- 核心功能：用概率转移和 cut-point 语言定义随机有限状态机。
- 关键特性：stochastic matrices、接受概率、isolated cut-point、可归约到确定自动机。
- 构造方式：有限状态 + 概率转移表 + cut-point。
- 基础设施：矩阵表示清晰，但无工程标准或工具。
- 适用场景：随机顺序电路、概率词分类、有限状态随机语义建模。
- 需求前提：输入是线性词，随机性主要体现为有限状态转移概率。
- 状态：🟢
