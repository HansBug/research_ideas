# 机器映射的刻画 / A Characterization of Machine Mappings

## 基本信息

- 标题：A Characterization of Machine Mappings
- 中文标题：机器映射的刻画
- 作者：Seymour Ginsburg, Gene F. Rose
- 发表：Canadian Journal of Mathematics, 18:381-388, 1966
- DOI：`10.4153/CJM-1966-040-3`
- 链接：https://www.cambridge.org/core/services/aop-cambridge-core/content/view/9BBE438C4AADDEDA0D4B3006DB8F87C5/S0008414X00040360a.pdf/div-class-title-a-characterization-of-machine-mappings-div.pdf
- 形式主义：Generalized Sequential Machines / Machine Mappings
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型刻画
- 工具/实现获取方式：原文只给出形式模型与 regular-set characterization；无独立实现或代码。
- 标准/格式获取方式：原文没有 XML/JSON 标准，机器可处理入口是 `gsm` 的状态集合、输入字母表、输出字母表、状态转移函数与输出函数。

## 简报

这篇论文的重要性不在“又提出一个顺序机名字”，而在于它把 `generalized sequential machine (gsm)` 作为稳定的 string-to-string transducer 母型明确写成标准 tuple，并给出 machine mapping 的结构性刻画。对当前演化树来说，它正好把 `Mealy / Moore / LSM` 之间尚未清晰命名的“顺序机 / 转导器”主干补成 `GSM` 节点。

- 形式主义定位：有限状态骨架上的经典单遍字符串转导模型，是后续 transducer / rational relation 支线的稳定母节点之一。
- 构造方式简述：输入词逐符号推进状态，同时按当前状态和输入字母输出一个词片段。
- 基础设施与场景简述：原文完全是理论刻画，没有工程标准；但它把 `gsm` 与 regular-language closure 之间的关系讲得非常清楚。

```text
输入字符串 -> 有限控制 + 输出函数 -> machine mapping -> regular-set characterization
```

## 形式主义定义与核心对象

### 定义对象

原文开篇就把 generalized sequential machine 定义成一个把输入词映射到输出词的有限状态转导器。它不是只识别语言，而是直接实现从 `\Sigma^*` 到 `\Delta^*` 的函数。

### 核心抽象

原文给出的 `gsm` 骨架可写成：

$$
S = (K, \Sigma, \Delta, \delta, \lambda, p_1)
$$

上式中的符号逐项解释如下：

1. `K` 是有限状态集。
2. `\Sigma` 是输入字母表。
3. `\Delta` 是输出字母表。
4. `\delta : K \times \Sigma \to K` 是 next-state function。
5. `\lambda : K \times \Sigma \to \Delta^*` 是 output function。
6. `p_1 \in K` 是起始状态。

原文再把这两个函数扩展到整个输入词：

$$
\delta(p, \epsilon) = p, \qquad \lambda(p, \epsilon) = \epsilon
$$

$$
\delta(p, xa) = \delta(\delta(p, x), a), \qquad \lambda(p, xa) = \lambda(p, x)\lambda(\delta(p, x), a)
$$

上式中的符号逐项解释如下：

1. `p` 是当前状态。
2. `x \in \Sigma^*` 是已经读过的前缀。
3. `a \in \Sigma` 是当前读入字母。
4. `\epsilon` 是空词。
5. 第二个式子表达“输出按前缀累计拼接”，这正是 `gsm` 区别于纯 acceptor 的核心。

于是 machine mapping 可写成：

$$
f(x) = \lambda(p_1, x)
$$

这说明 `gsm` 的本体就是“有限状态 + 增量输出”的字符串函数实现器。

### 一个最小例子与通俗解释

一个最小例子是“遇到 `a` 输出 `0`，遇到 `b` 输出 `10`，并在某些字母上切换状态”的编码器。机器从 `p_1` 出发，每读一个输入字母，一方面更新状态，另一方面立刻吐出一个输出片段；最后把沿路所有片段拼起来就是最终输出词。

通俗地说，`gsm` 像一个“边走边写”的有限状态翻译器。普通 `FA` 只回答“接不接受”，而 `gsm` 会在每一步顺手写出一段输出，因此它天然是 transducer，而不是 acceptor。

### 运行 / 接受 / 转移语义

`gsm` 没有 accept/reject 作为主语义，主语义就是输出函数的累计拼接。对任意输入词 `$x = a_1 \cdots a_n$`，其输出由逐步展开决定：

$$
f(x) = \lambda(p_1, a_1)\lambda(\delta(p_1, a_1), a_2)\cdots\lambda(\delta(p_1, a_1\cdots a_{n-1}), a_n)
$$

这条式子说明：

1. 当前输出片段取决于“当前状态 + 当前输入字母”。
2. 最终输出是所有局部片段的串联。
3. 因而该模型天然适合描述单遍、有限记忆、输出可增量产生的 transduction。

### 语义边界

相对 `Mealy` / `Moore`，`gsm` 把单符号输出推广成一般词输出，因此更适合描述真正的 string transduction；相对 [infinite-linear-sequential-machines/desc.md](../infinite-linear-sequential-machines/desc.md)，它仍是纯有限离散字母表模型，没有线性状态空间结构。

### 关键性质与判定边界

原文的核心贡献是 machine mapping characterization。它证明函数 `$f : \Sigma^* \to \Delta^*$` 可由某个 `gsm` 实现，当且仅当满足一组结构性条件。可压缩写成：

$$
f \text{ is a gsm mapping } \iff
\begin{cases}
f(\epsilon) = \epsilon, \\
f \text{ preserves initial subwords}, \\
f \text{ has bounded output growth}, \\
f^{-1}(Y) \text{ is regular for every regular } Y \subseteq \Delta^*
\end{cases}
$$

其中“bounded output growth”在原文中写成：

$$
|\!f(ua)\!| - |\!f(u)\!| < M
$$

上式中的符号逐项解释如下：

1. `u \in \Sigma^*` 是任意输入前缀。
2. `a \in \Sigma` 是单个输入字母。
3. `M` 是与具体输入无关的统一上界。
4. 这条界说明每一步新增加的输出长度是有全局上界的。

这组条件非常适合拿来解释为什么 `gsm` 是“正则语言友好”的 transducer 母型。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制是核心骨架。 |
| 事件 / 触发 | 强支持 | 每个输入字母触发一次状态更新和输出追加。 |
| 守卫 / 数据 | 不支持 | 原始模型没有显式变量或守卫。 |
| 层次 | 不支持 | 输入对象是线性词而非树。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无显式时钟或延迟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散有限状态。 |
| 可执行 / 可验证性 | 强支持 | 与 regular-set inverse image 和结构刻画紧密绑定。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$S=(K,\Sigma,\Delta,\delta,\lambda,p_1)$` | `gsm` 的标准有限状态转导器骨架。 |
| 词级输出语义 | `$f(x)=\lambda(p_1,x)$` | 输出不是终态标签，而是逐步累计产生。 |
| 增量输出界 | `$|f(ua)|-|f(u)|<M$` | 每步输出长度有统一上界。 |
| regular inverse image | `$f^{-1}(Y)$ regular | $\forall Y \in \mathrm{REG}$` | `gsm` 与 regular-language 理论的核心接口。 |
| 结构刻画 | `gsm mapping iff four conditions` | 直接回答“什么函数才是 machine mapping”。 |

## 构造方式与承载格式

### 建模入口

建模时需要：

1. 选定输入与输出字母表。
2. 设计有限状态集。
3. 为每个“状态 + 输入字母”给出下一状态和输出词片段。

### 机器可处理承载方式

原文的承载方式就是函数表：

1. `\delta : K \times \Sigma \to K`
2. `\lambda : K \times \Sigma \to \Delta^*`

没有单独 DSL，也没有图形标准。

### 交换与互操作

它和 regular languages、sequential functions、inverse-image characterization 以及后来的 transducer / rational relation 路线直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程化交换格式，只有数学函数表。
- 仿真/执行支持：按输入字母单遍推进即可执行。
- 验证/分析支持：regular inverse image、bounded output growth 等理论性质清晰。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是后续 string transducer / sequential machine 理论的重要母节点之一。

## 适用场景与需求前提

### 适用场景

适合有限记忆、单遍扫描、输出可逐步生成的字符串变换问题，例如编码、协议符号重写、词法级翻译和简单串关系实现。

### 需求前提

1. 输入对象必须是线性词。
2. 需要的是有限记忆 transduction，而不是无界栈或树结构处理。
3. 每步输出增量应有统一上界。

### 不适用或高成本场景

若需求需要回看任意远前缀、复制未界定的中间结果、显式树结构或无限运行接受条件，`gsm` 就不再是合适母型。

## 与相邻形式主义的关系

相对 [a-method-for-synthesizing-sequential-circuits/desc.md](../a-method-for-synthesizing-sequential-circuits/desc.md) 和 [gedanken-experiments-on-sequential-machines/desc.md](../gedanken-experiments-on-sequential-machines/desc.md)，`gsm` 把顺序机从“单步输出逻辑”推进到“词到词转导”；相对 [infinite-linear-sequential-machines/desc.md](../infinite-linear-sequential-machines/desc.md)，它是更基础、更经典的有限字母表 transducer 母型；相对后来的 streaming transducer，它没有变量更新和 copyless 约束，只保留最朴素的有限控制 + 输出片段结构。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树中“顺序机 / 转导器支线”补成了一个明确可命名的 `Generalized Sequential Machines` 节点，便于后续继续向 rational relations、streaming string transducers 和 tree/string transducer 路线延伸。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示或演化树母节点，而不是控制系统最终建模语言。

### 对需求到模型生成的启发

它提醒我们：当需求本质上是“有限上下文决定的字串到字串映射”时，没必要一上来引入栈、树或时间结构，`gsm` 级别就足够。

### 现实限制

工程侧没有现成标准格式或主流工具生态，实际更多承担谱系定位和表达力边界说明的作用。

## 重要的相关工作

### 奠基或前身工作

- [a-method-for-synthesizing-sequential-circuits/desc.md](../a-method-for-synthesizing-sequential-circuits/desc.md)
- [gedanken-experiments-on-sequential-machines/desc.md](../gedanken-experiments-on-sequential-machines/desc.md)

### 同类型或同家族工作

- [infinite-linear-sequential-machines/desc.md](../infinite-linear-sequential-machines/desc.md)
- [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供标准或工具线。

### 与本研究关系最紧的工作

- 它最适合充当当前文库里 `Finite Automata -> 顺序机 / 转导器` 的经典母节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Generalized Sequential Machines / Machine Mappings
- 论文角色：模型刻画
- 核心功能：用有限状态与增量输出函数实现字符串到字符串的单遍 machine mapping。
- 关键特性：有限状态、逐步输出、bounded output growth、regular inverse-image characterization。
- 构造方式：`(K,\Sigma,\Delta,\delta,\lambda,p_1)` 六元组与词级扩展语义。
- 基础设施：纯理论模型，无工程标准与工具。
- 适用场景：有限记忆字串变换、编码与 classical transducer 理论主干。
- 需求前提：输入是线性词，输出可按步增量产生，且每步输出长度有统一上界。
- 状态：🟢
