# 广义有限自动机定义的关系 / On Relations Defined by Generalized Finite Automata

## 基本信息

- 标题：On Relations Defined by Generalized Finite Automata
- 中文标题：广义有限自动机定义的关系
- 作者：Calvin C. Elgot, Jorge E. Mezei
- 发表：*IBM Journal of Research and Development*, 9(1):47-68, 1965
- DOI：`10.1147/RD.91.0047`
- 链接：https://doi.org/10.1147/RD.91.0047
- 形式主义：`Generalized Finite Automata / Transductions`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `n` 元 `NDA`、路径标签元组、`FAD` 与 sequential relation。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是有限有向图上的多分量词标签与 relation semantics。

## 简报

这篇论文的核心不是再定义一个一元 acceptor，而是把“有限图上按路径拼接标签得到的 `n` 元词关系”稳定命名为 `transduction`，并系统说明它和 `FAD`、sequential relations、multi-tape one-way automata 以及函数型 transducer 的关系。对当前演化树来说，它正好补上 `Finite Automata -> 顺序机 / 转导器` 支线里的“关系型 transduction / rational relation 母节点”。

- 形式主义定位：有限状态骨架上的 `n` 元词关系 / transduction 模型，是从 acceptor 走向 transducer 与 relation automata 的经典母型。
- 构造方式简述：用带初态、终态和元组词标签边的有限有向图生成路径语言，再按分量拼接得到 `n` 元 relation。
- 基础设施与场景简述：原文是纯理论工作，没有 DSL 或工具标准，但它把 transduction、FAD、sequential relation 和 closure / decomposition 讲得非常完整。

```text
多分量词关系需求 -> 有限图 + 元组边标签 -> 路径分量拼接 -> transduction / sequential relation / closure analysis
```

## 形式主义定义与核心对象

### 定义对象

论文关注的是 `R \subseteq (\Sigma^*)^n` 这类 `n` 元词关系，而不是单个语言。它允许 relation 是函数，也允许一对多 / 多对多的非确定性 transduction。

### 核心抽象

对一个 `n` 元 nondeterministic automaton，可保守整理成如下骨架：

$$
\mathcal A = (S, v, s_0, D)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `s_0 \in S` 是初始状态。
3. `D \subseteq S` 是 designated states。
4. `v \subseteq S \times (\Sigma^*)^n \times S` 是带 `n` 元词标签的边关系；原文把它画成有限有向标号图。

`n` 元 transduction 的定义可写成：

$$
R \text{ is a transduction } \iff \exists \mathcal A,\ R = T(\mathcal A)
$$

其中 `T(\mathcal A)` 是所有从 `s_0` 出发并到达 `D` 的路径标签按分量拼接后得到的 `n` 元词集合。

### 一个最小例子与通俗解释

可以取论文里反复提到的二元关系原型：

$$
R = \{(0,00)\}^* = \{(0^m,0^{2m}) \mid m \ge 0\}
$$

这个 relation 只需要一个循环边，边标签写成 `(0,00)`，每走一圈就在第一分量追加一个 `0`，在第二分量追加两个 `0`。

通俗地说，这类模型像“多条纸带一起写的有限状态路径机”：一条路径不是只产出一个词，而是同时产出 `n` 个词分量，因此天然描述的是词关系而不是普通语言。

### 运行 / 接受 / 转移语义

若路径依次经过边标签 `u_1,\ldots,u_m \in (\Sigma^*)^n`，则该路径产出的整体标签是分量式拼接：

$$
u = u_1u_2\cdots u_m
$$

其中对 `n` 元组 `u_i=(u_i^1,\ldots,u_i^n)`，拼接按分量执行：

$$
u_1u_2 = (u_1^1u_2^1,\ldots,u_1^n u_2^n)
$$

于是接受语义可以写成：

$$
u \in T(\mathcal A) \iff \exists s_1,\ldots,s_{m+1},\ s_1=s_0,\ s_{m+1}\in D,\ (s_i,u_i,s_{i+1})\in v,\ u=u_1\cdots u_m
$$

上式中的 `s_i` 是路径上的状态序列，`u_i` 是每条边上的 `n` 元标签。

### 语义边界

当 `n=1` 时，transductions 正好退化为有限自动机可识别语言；但当 `n>1` 时，multi-tape automata 定义的 `FAD` 只是 transductions 的真子类，论文明确给出 `{(0,00)\}^*` 这类“是 transduction 但不是 `FAD`”的例子。

### 关键性质与判定边界

论文最核心的结构定理之一是：

$$
\mathsf{Trans}_n(\Sigma) = \mathrm{Kleene}(\mathrm{FinRel}_n(\Sigma))
$$

这里 `\mathrm{FinRel}_n(\Sigma)` 是有限 `n` 元词关系类，`\mathrm{Kleene}(\cdot)` 表示对并、拼接和 Kleene 星闭包生成的最小类。也就是说，`n` 元 transductions 正好是“从有限关系出发做正则式闭包”得到的 relation family。

论文还证明二元 transductions 在 Pierce product / relation composition 下封闭，并把 `LP`、locally finite、`S`-transductions 等子类放进统一分解框架。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态图是唯一控制骨架。 |
| 事件 / 触发 | 支持 | 边标签由词元组承载，沿路径离散推进。 |
| 守卫 / 数据 | 不支持 | 原始模型没有变量守卫或算术数据。 |
| 层次 | 不支持 | 输入输出对象是线性词元组，不是树。 |
| 并发 / 同步 | 不支持 | 多分量是 relation 维度，不是并发进程语义。 |
| 时间约束 | 不支持 | 无时钟或 deadline。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 relation automata。 |
| 可执行 / 可验证性 | 强支持 | closure、decomposition、`FAD` 边界和 sequential relation 条件都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| transduction 定义 | `$R=T(\mathcal A)$` | 用有限图路径定义 `n` 元词关系。 |
| 分量拼接 | `$u_1u_2=(u_1^1u_2^1,\ldots,u_1^n u_2^n)$` | 路径标签按每个分量分别累积。 |
| 一元退化 | `$n=1 \Rightarrow \mathsf{Trans}_1=\mathrm{REG}$` | 普通有限自动机是特例。 |
| 非 `FAD` 例子 | `$\{(0,00)\}^* \notin \mathrm{FAD}$` | `n>1` 时 transduction 严格强于多带 `FAD`。 |
| Kleene 刻画 | `$\mathsf{Trans}_n=\mathrm{Kleene}(\mathrm{FinRel}_n)$` | 给出 relation automata 的正则式闭包刻画。 |

## 构造方式与承载格式

### 建模入口

1. 先确定 relation 的 arity `n` 和每个分量的字母表。
2. 把每类局部 relation step 写成边上的 `n` 元词标签。
3. 指定初态、终态，并通过路径拼接生成全局 relation。

### 机器可处理承载方式

机器可处理承载方式就是有限有向图 + 元组词标签 + designated states；如果限制成函数型并加入 prefix-closed / `FAD` 条件，则可进一步落到 sequential machine / sequential function。

### 交换与互操作

它和 [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md) 的 `GSM` 线、[closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md](../closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md) 的 multi-tape relation 线，以及后续 rational relations / transducer 理论都直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程标准，核心是有限图与 relation closure 语义。
- 仿真/执行支持：可按路径枚举或按边关系推进，但原文不是工程执行框架。
- 验证/分析支持：重点是 closure、子类分解、`FAD` 边界和 sequential relation characterization。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 rational relations / transducer theory 的经典母体之一。

## 适用场景与需求前提

### 适用场景

适合多串关系、编码/解码关系、有限状态转导、路径标号 relation 建模，以及需要区分“函数型 sequential transduction”和“一般 `n` 元 relation”的理论场景。

### 需求前提

1. 对象可写成有限个线性词分量之间的关系。
2. relation 的局部生成机制可由有限状态图和有限标签模式表达。
3. 不需要栈、树、时间或连续变量。

### 不适用或高成本场景

若需求需要显式层次树结构、无界嵌套记忆或物理时间/连续动态，就应转向 tree automata、pushdown 或 timed/hybrid 分支。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，它把“接受一个词”推广成“定义 `n` 个词之间的关系”；相对 [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md)，本文更一般，允许非函数型 `n` 元 transduction；相对 [closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md](../closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md)，它明确指出多带 `FAD` 只是 transductions 的受限子类。

## 与本研究的关系

### 对 Project 1 的价值

它把演化树里“顺序机 / 转导器”支线从 `GSM / SST` 进一步上提到更早、更一般的 relation 母节点，方便后续继续补 rational relations、multi-tape transductions 与 subsequential families。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和中间表示，不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

如果需求描述的不是“控制器 trace 是否合法”，而是“多个 trace / 字符串之间应满足什么有限状态关系”，那么应考虑 relation automata / transduction，而不是只输出单一 acceptor。

### 现实限制

原文没有 DSL、标准格式或工具生态，工程落地需要另选载体。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)

### 同类型或同家族工作

- [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md)
- [closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md](../closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md)
- [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Finite Automata -> 顺序机 / 转导器 -> Transductions / Generalized Finite Automata` 这一层的经典母节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Generalized Finite Automata / Transductions`
- 论文角色：模型提出
- 核心功能：用有限图路径上的 `n` 元词标签定义 transduction，并系统整理它和 `FAD`、sequential relations、composition closure 的关系。
- 关键特性：`n` 元 relation、分量拼接语义、Kleene 闭包刻画、Pierce product、sequential / locally finite 子类。
- 构造方式：`(S,v,s_0,D)` 有限图 + 元组词标签 + designated states。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：rational relations、多串 transduction、有限状态 relation theory。
- 需求前提：对象是有限个线性词之间的关系，且局部 relation step 可由有限图边标签表达。
- 状态：🟢
