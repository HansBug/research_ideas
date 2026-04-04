# 名义集合中的自动机理论 / Automata theory in nominal sets

## 基本信息

- 标题：Automata theory in nominal sets
- 中文标题：名义集合中的自动机理论
- 作者：Mikolaj Bojanczyk, Bartek Klin, Slawomir Lasota
- 发表：*Logical Methods in Computer Science*, 10(3:4):1-44, 2014
- DOI：`10.2168/LMCS-10(3:4)2014`
- 链接：https://doi.org/10.2168/LMCS-10(3:4)2014
- 形式主义：`Nominal G-Automata / Orbit-Finite Nominal Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型系统化
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 data symmetry `(D,G)`、orbit-finite `G`-sets、equivariant transitions、nominal supports 与 orbit-finite representations。
- 标准/格式获取方式：原文没有 DSL 或交换格式，核心承载方式是 `G`-set 上的自动机元组、orbit-finiteness、support 表示与 `Myhill-Nerode` 商结构。

## 简报

这篇论文的表面标题是“automata theory in nominal sets”，但真正对当前文库有价值的不是泛泛理论背景，而是它把一整类“无限字母表上的有限状态机”统一整理成了稳定的模型口径：只要把字母上的可观察结构压成一个对称群 `G`，再把“有限”换成“orbit-finite”，就能得到 `G-automata` 与 nominal `G-automata`。这样一来，`FMA`、若干 register-style 模型和更一般的 symmetry-based automata 就有了共同母语。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上的抽象母节点，可把 equality、order 等不同无限字母表结构统一起来。
- 构造方式简述：输入字母表和状态空间都不再要求有限，而只要求 orbit-finite；转移、初态和终态则要求 equivariant。
- 基础设施与场景简述：原文给出 `G-automata`、nominal `G-automata`、orbit-finite `Myhill-Nerode` 定理，并证明在 equality symmetry 下与 `Finite-Memory Automata` 表达力等价。

```text
带对称性的无限字母表 -> orbit-finite nominal sets -> equivariant automata -> symmetry-aware regular language theory
```

## 形式主义定义与核心对象

### 定义对象

原文从 data symmetry `(D,G)` 出发，其中 `D` 是数据值域，`G` 是 `D` 上的自同构群。与普通“无限字母表 automata”不同，这里不直接硬编码字母，而是先声明“自动机能观察到哪些对称性不变量”。

名义集合的关键概念是 support。若 `X` 是 `G`-set，则元素 `x\in X` 的有限 support `C\subseteq D` 满足：

$$
\forall \pi\in G.\ \bigl(\forall c\in C,\ \pi(c)=c\bigr)\Rightarrow x\cdot \pi=x
$$

上式中的符号逐项解释如下：

1. `\pi` 是 `G` 中的一个对称变换。
2. `x\cdot \pi` 是 `\pi` 在集合 `X` 上对元素 `x` 的作用。
3. 该式表示：只要 `\pi` 固定了 support 里的数据值，`x` 就不会被改变。

### 核心抽象

原文把 nondeterministic `G`-automaton 定义为：

$$
\mathcal A=(A,Q,I,F,\delta)
$$

上式中的符号逐项解释如下：

1. `A` 是 orbit-finite `G`-set，作为输入字母表。
2. `Q` 是状态空间，也是 `G`-set。
3. `I,F\subseteq Q` 是 equivariant 的初态集与终态集。
4. `\delta\subseteq Q\times A\times Q` 是 equivariant 转移关系。

若是 deterministic 版本，则转移函数变成：

$$
\delta:Q\times A\to Q
$$

并且初态集退化为单个初始状态 `\{q_I\}`。

### 一个最小例子与通俗解释

一个最简单的 equality-symmetry 例子，是识别“相邻两个数据值不同”的数据词。普通有限自动机没法直接处理无限数据域，但 nominal automaton 可以只记住“前一个数据值”这个有限 support，再用 equivariant 方式判断当前值是否与之相同。

通俗地说，这类模型像“不会记住具体编号，只记住对称性不变结构的自动机”。它并不关心某个数据值叫 `17` 还是 `203`；它关心的是这个值是否与某个已支持的名字相同、是否满足同一对称类关系。

### 运行 / 接受 / 转移语义

接受语义与普通自动机相同，只是所有对象都搬到了 `G`-set 世界中。多步转移关系写作：

$$
\delta^*\subseteq Q\times A^*\times Q
$$

一个词 `w\in A^*` 被接受，当且仅当存在 `q_I\in I` 与 `q_F\in F` 使得：

$$
(q_I,w,q_F)\in \delta^*
$$

这里的关键不是接受条件本身，而是：

1. `A^*` 仍然带有 `G` 的自然作用；
2. `\delta^*` 仍然是 equivariant；
3. 因此识别出来的语言天然是 `G`-language。

### 语义边界

这个模型的增强点不在单个额外存储结构，而在“把 finite 替换成 orbit-finite，并用 symmetry 约束状态与迁移”。因此它比具体的 `FMA/RA/FRA` 更抽象，也更像共同母语。代价是：并不是所有经典有限自动机性质都能无损保留，例如 nondeterministic nominal automata 一般不能像普通 `NFA` 那样稳定 determinize。

### 关键性质与判定边界

原文最关键的结构性结果可压成：

$$
L \text{ 被 deterministic orbit-finite } G\text{-automaton 识别 } \iff A^*/{\equiv_L} \text{ orbit-finite}
$$

这就是 `G`-set 版本的 `Myhill-Nerode` 定理。

对 nominal `G`-sets，原文进一步写成：

$$
L \text{ 被 } G\text{-DFA 识别 } \iff A^*/{\equiv_L} \text{ orbit-finite}
$$

在 equality symmetry 下，它又和 `Finite-Memory Automata` 建立等价桥梁：

$$
\mathrm{G\text{-}NFA}\equiv \mathrm{FMA}
$$

并且在 deterministic 情形下有：

$$
\mathrm{G\text{-}DFA}\equiv \mathrm{deterministic\ FMA}
$$

但另一方面，原文也强调：

$$
\text{determinization of nominal } G\text{-NFA fails in general}
$$

上面几式中的符号逐项解释如下：

1. `\equiv_L` 是 `L` 的 `Myhill-Nerode` 等价关系。
2. `A^*/{\equiv_L}` 是语言的 syntactic quotient。
3. orbit-finite 表示该商结构只有有限多个 orbit。
4. 最后一式说明：不能机械照搬普通 `NFA` 的子集构造。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍有有限控制骨架，但“有限”升级为 orbit-finite。 |
| 事件 / 触发 | 强支持 | 输入来自带对称性的无限字母表。 |
| 守卫 / 数据 | 强支持 | 通过 symmetry / support 间接处理无限域数据。 |
| 层次 | 不支持 | 基本模型仍是词自动机。 |
| 并发 / 同步 | 不支持 | 不是并发交互模型。 |
| 时间约束 | 不支持 | 原始模型无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散无限字母表理论。 |
| 可执行 / 可验证性 | 强理论支持 | `Myhill-Nerode`、orbit quotient、FMA 等价性都很清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| support | `$\forall \pi\in G.\ (\forall c\in C,\pi(c)=c)\Rightarrow x\cdot\pi=x$` | nominal set 的核心定义。 |
| automaton 元组 | `$\mathcal A=(A,Q,I,F,\delta)$` | `G`-automaton 的标准形态。 |
| deterministic 版本 | `$\delta:Q\times A\to Q$` | orbit-finite `G`-DFA。 |
| `Myhill-Nerode` | `$A^*/{\equiv_L}$ orbit-finite` | 语言可识别性的抽象判据。 |
| FMA 等价 | `$\mathrm{G\text{-}NFA}\equiv \mathrm{FMA}$` | 抽象模型与已有 infinite-alphabet automata 的连接。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入数据域上的可观察结构，例如 equality、order 或更一般 symmetry。
2. 再把字母表和状态空间写成 orbit-finite `G`-sets。
3. 最后只允许使用 equivariant 的转移、初态和终态。

### 机器可处理承载方式

机器可处理承载方式就是：

1. data symmetry `(D,G)`；
2. orbit-finite alphabet `A`；
3. nominal/orbit-finite state space `Q`；
4. equivariant transition relation 或函数；
5. support / orbit 的有限表示。

### 交换与互操作

它与 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 的关系最强，因为原文明确证明在 equality symmetry 下与 `FMA` 等价；它也能为 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md) 和 [history-register-automata/desc.md](../history-register-automata/desc.md) 提供更高层的 infinite-alphabet 母语。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 nominal/orbit-finite representation、supports、equivariant functions。
- 仿真/执行支持：可按普通自动机方式执行，只是状态和字母带 symmetry 语义。
- 验证/分析支持：`Myhill-Nerode` 定理、最小化视角、与 `FMA` 的表达力桥接、orbit-finite quotient 分析。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：与 nominal sets、automata over infinite alphabets、register/finite-memory automata 和程序语义理论紧密耦合。

## 适用场景与需求前提

### 适用场景

适合给“无限字母表但只关心对称性不变量”的 automata family 找统一母语，尤其是 equality / order 数据词和 support-sensitive 语言。

### 需求前提

1. 输入值域上的可观察结构必须能抽成某个对称群 `G`。
2. 需求真正关心的是 symmetry-invariant 关系，而不是具体常数。
3. 状态空间应可压成 orbit-finite，而不是本质上无限维。

### 不适用或高成本场景

如果需求更适合具体寄存器、history、stack 或时钟操作式描述，直接使用 `FMA/FRA/HRA/VPA/TA` 等专门模型通常更自然；nominal automata 更适合作为上层统一口径。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它更抽象，强调 symmetry 与 orbit 而不是具体 windows；相对 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md) 与 [history-register-automata/desc.md](../history-register-automata/desc.md)，它不是针对 freshness/history 的专门机制，而是更高层的 infinite-alphabet automata 框架。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Data / Infinite-Alphabet` 支线上的多个离散分枝拉回到同一个母节点，特别适合用来完善演化树的“抽象总线”。

### 作为目标形式主义还是中间表示

更适合作为理论总线与分类母型，而不是面向需求工程的直接交付模型。

### 对需求到模型生成的启发

它提示我们：面对无限数据域时，不一定要直接选某个具体寄存器机；先判断问题是否只依赖 symmetry-invariant 结构，往往更能决定后续该落到 `FMA`、register、class-memory 还是其他分支。

### 现实限制

其价值主要在统一化与谱系整理，而不是工程落地；如果不需要抽象视角，只写具体 automaton 通常更直接。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)
- [history-register-automata/desc.md](../history-register-automata/desc.md)
- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或统一工具。

### 与本研究关系最紧的工作

- 它最适合挂到 `Finite Automata -> Data / Infinite-Alphabet` 的抽象母节点，用来统摄 `FMA / FRA / class-memory / HRA` 等具体模型。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Nominal G-Automata / Orbit-Finite Nominal Automata`
- 论文角色：模型系统化
- 核心功能：把无限字母表上的自动机统一写成 symmetry-aware、orbit-finite、equivariant 的 nominal automata。
- 关键特性：data symmetry、supports、orbit-finiteness、equivariant transitions、`Myhill-Nerode` 商结构、与 `FMA` 的等价桥接。
- 构造方式：`G`-set 上的 automaton 元组加 nominal support / orbit 表示。
