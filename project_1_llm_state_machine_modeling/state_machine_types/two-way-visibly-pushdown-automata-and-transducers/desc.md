# 双向可见下推自动机与转换器 / Two-Way Visibly Pushdown Automata and Transducers

## 基本信息

- 标题：Two-Way Visibly Pushdown Automata and Transducers
- 中文标题：双向可见下推自动机与转换器
- 作者：Luc Dartois, Emmanuel Filiot, Pierre-Alain Reynier, Jean-Marc Talbot
- 发表：*Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science (LICS 2016)*, pp. 217-226, 2016
- DOI：`10.1145/2933575.2935315`
- 链接：https://doi.org/10.1145/2933575.2935315
- 形式主义：`Two-Way Visibly Pushdown Automata / Two-Way Visibly Pushdown Transducers (2VPA / 2VPT)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未给工程实现；机器可处理入口是 `2VPA` 的双向头位置、方向、visible stack 语义，以及 `2VPT` 的 rule-output morphism 与 single-use restriction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `2VPA=(Q,q_I,F,\Gamma,\delta)`、`2VPT=(A,O)`、look-around 与 `MSO` 对应。

## 简报

这篇论文把 `VPA/VPT` 的输入头从单向扫描推进到双向扫描，同时仍然保留可见下推纪律。结果是：在语言识别上，`2VPA` 并没有超出 `VPA` 的表达力；但在变换上，`D2VPT` 成了一个非常自然的 nested-word transduction 母型，既能描述比单向 `VPT` 更强的结构化变换，又能在 single-use 限制下精确对齐 `MSO` transductions。

- 形式主义定位：`Structured-word / nested-word` 支线从一向 `VPT` 迈向 `MSO`-级 transduction 的关键桥节点。
- 构造方式简述：读头允许左右移动，但每次遇到 call/return 时的 push/pop 仍由输入字母类型决定；在 transducer 版本里，每条规则再带一个输出词。
- 基础设施与场景简述：原文给出 `2VPA` 到 `VPA` 的等价、`D2VPT` 的 regular look-around 闭包、等价性可判定性，以及 `MSO [nw2w] = D2VPT_{su}` 的主结果。

```text
nested word -> 双向读头 + visible stack -> 结构化往返扫描 -> nested-word 到 word 的 MSO 级变换
```

## 形式主义定义与核心对象

### 定义对象

`2VPA/2VPT` 处理的仍是 nested words，只是读头可以在输入上左右移动。为了描述读头方向，原文引入方向集合：

$$
D=\{\leftarrow,\rightarrow\}
$$

此外，还在输入两端加入左右端标记，方便定义从边界返回和离开边界时的动作。

### 核心抽象

原文把 `2VPA` 定义为：

$$
A=(Q,q_I,F,\Gamma,\delta)
$$

其中 `\delta` 被拆成 `\delta_{\mathrm{push}}` 与 `\delta_{\mathrm{pop}}` 两部分，用来区分当前读取符号和方向共同决定的是 push 还是 pop。

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_I\in Q` 是初始状态。
3. `F\subseteq Q` 是接受状态集。
4. `\Gamma` 是栈字母表。
5. `\delta` 是考虑读头方向后的双向 visibly-pushdown 转移关系。

在此基础上，`2VPT` 定义为：

$$
T=(A,O)
$$

上式中的符号逐项解释如下：

1. `A` 是 underlying `2VPA`。
2. `O` 是从 `A` 的规则到输出字母表 `\Delta^*` 的 morphism。
3. 每次读头移动时都可追加一段输出词。

### 一个最小例子与通俗解释

一个很直观的例子是：对每个结构块的 opening tag，不是立刻按顺序输出，而是先向右走进这个块，找到块内部的标题，再回到 opening tag 位置决定输出什么。这类“需要进块里看一眼，再回到当前点作决定”的变换，对单向 `VPT` 很别扭，但对 `2VPT` 非常自然。

通俗地说，`2VPT` 像“会回头看上下文的 `VPT`”。普通 `VPT` 更像单遍流式处理器；`2VPT` 则像一个仍然受 visible stack 约束、但能前后往返查看局部层次结构的结构化扫描器。

### 运行 / 接受 / 转移语义

原文把 `2VPA` 的 configuration 写成：

$$
(q,i,d,\sigma)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `i` 是读头当前位于输入第 `i` 个位置之间的间隙。
3. `d\in D` 表示下一步向左读还是向右读。
4. `\sigma` 是当前栈内容。

接受运行从左端、空栈、向右开始，并在右端、空栈、向右结束。其关键点是：即使读头双向移动，栈动作仍然由“当前读取的是 call 还是 return”以及“当前方向是左还是右”共同决定，因此在同一输入位置上反复访问时，栈高度仍与 nested 结构同步。

对于 `2VPT`，若运行 `\rho` 是 `A` 在输入 `w` 上的一条接受运行，对应规则序列为 `t_1\cdots t_n`，则输出定义为：

$$
\mathrm{out}_w(\rho)=O(t_1)\cdots O(t_n)
$$

于是转导关系为：

$$
\llbracket T \rrbracket=\{(w,\mathrm{out}_w(\rho)) \mid \rho \text{ 是 } T \text{ 在 } w \text{ 上的接受运行}\}
$$

### 语义边界

`2VPA` 的重点不在于增加任意下推能力，而在于给 nested-word 模型加“双向局部回看”能力。它仍不是一般双向 `PDA`，因为栈纪律始终由输入字母类型固定。对语言识别来说，这个增强不会突破 `VPA`；但对 transduction 来说，它明显增强了表达力。

### 关键性质与判定边界

原文给出的主结论可压成：

$$
\mathcal L(2\mathrm{VPA})=\mathcal L(\mathrm{VPA})
$$

$$
\mathrm{equivalence}(D2\mathrm{VPT}) \text{ decidable}
$$

$$
D2\mathrm{VPT} \text{ 对 regular look-around 封闭}
$$

$$
\mathrm{MSO}[nw2w]=D2\mathrm{VPT}_{su}=D2\mathrm{VPTLA}_{su}
$$

上面几式中的符号逐项解释如下：

1. 第一式表示双向对 nested-word 语言识别不增加表达力。
2. `D2VPT` 是 deterministic `2VPT`。
3. `su` 表示 single-use restriction。
4. `VPTLA` 表示带 look-around 的版本。
5. 最后一式说明：加上 single-use 约束后，`D2VPT` 正好刻画 `MSO`-definable nested-word 到 word 变换。

原文还强调：未加 single-use 限制时，`D2VPT` 严格强于 `MSO` transductions，因为它可以实现指数级 size increase。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限控制骨架。 |
| 事件 / 触发 | 强支持 | 读取 call / return / internal 时均显式依赖方向。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据变量。 |
| 层次 | 强支持 | visible stack 直接绑定 nested-word 结构。 |
| 并发 / 同步 | 不支持 | 对象仍是单个 nested word。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散结构化变换模型。 |
| 可执行 / 可验证性 | 强支持 | 等价性可判定，look-around 可消除，`MSO` 对应明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| automaton 元组 | `$A=(Q,q_I,F,\Gamma,\delta)$` | `2VPA` 的标准定义。 |
| transducer 元组 | `$T=(A,O)$` | `2VPT` 在 `2VPA` 上附输出。 |
| configuration | `$(q,i,d,\sigma)$` | 状态、位置、方向、栈四元语义。 |
| `MSO` 对应 | `$\mathrm{MSO}[nw2w]=D2\mathrm{VPT}_{su}$` | single-use 版本正好对应 `MSO` transduction。 |
| 判定边界 | `equivalence(D2VPT) decidable` | 这是该模型非常有价值的性质。 |

## 构造方式与承载格式

### 建模入口

1. 先判断问题是否必须“回头看”块内或块后的上下文。
2. 若只是单向 streaming 即可完成，应优先使用一向 `VPT`。
3. 若确实需要双向回看，再决定哪些规则在回访同一位置时允许产生输出，是否需要 single-use。

### 机器可处理承载方式

机器可处理承载方式就是：

1. 带端标记的 nested-word 输入；
2. 方向化 configuration `(q,i,d,\sigma)`；
3. 双向 push/pop 规则；
4. 规则到输出词的映射 `O`；
5. 可选的 unambiguous look-around 与 single-use 限制。

### 交换与互操作

它直接连接 [visibly-pushdown-transducers/desc.md](../visibly-pushdown-transducers/desc.md) 与 `MSO`/tree-walking transducer 路线：向下能退化到单向 `VPT`，向上在 single-use 下与 `MSO` transduction 等价。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 traversal algebra、look-around 与 transducer-to-transducer 编译。
- 仿真/执行支持：deterministic 版本可按输入深度线性内存执行。
- 验证/分析支持：`2VPA` 到 `VPA` 转换、type checking、等价性判定、single-use 检查。
- 代码生成/转换支持：原文给出到 one-way / look-around / `MSO` 等价模型的系统性翻译。
- 标准化或社区生态：与 nested words、`MSO` transducers、streaming tree/string transducers 和 tree-walking transducers 关系紧密。

## 适用场景与需求前提

### 适用场景

适合需要在层次输入上前后回看局部上下文的结构化变换，例如 XML / unranked tree 的复杂重排、摘要提取、context-dependent output generation。

### 需求前提

1. 输入必须有稳定的 visible call/return 结构。
2. 输出逻辑确实需要双向回访，而非单向 streaming。
3. 若要落到 `MSO` 对应，最好还能满足 single-use。

### 不适用或高成本场景

若输入只是普通词，或变换可单向完成，用 `FST/VPT` 更轻；若需要任意数据运算或无 visible 栈纪律的递归程序模型，则 `2VPT` 也不是终点。

## 与相邻形式主义的关系

相对 [visibly-pushdown-transducers/desc.md](../visibly-pushdown-transducers/desc.md)，它把读头从单向推进到双向；相对 `MSO` transducers，它给出更操作化、机器式的实现骨架；相对 [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)，它依赖双向回看而不是单向寄存器更新。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `nested-word transduction` 主线从 `VPT` 正式延伸到 `MSO` 级别，避免演化树在 structured-word transducer 一侧断层。

### 作为目标形式主义还是中间表示

更适合作为理论母型和变换能力边界节点，而不是控制系统建模的最终交付语法。

### 对需求到模型生成的启发

当需求里存在“先到子结构里看一眼，再回到当前层决定输出”的模式时，LLM 应意识到这已经超出普通单向 `VPT` 的舒适区，更接近 `2VPT` 或 `MSO` transduction。

### 现实限制

虽然理论能力强，但工程生态不如一向模型直接；其价值主要在于补树和界定 transduction 支线的表达力上界。

## 重要的相关工作

### 奠基或前身工作

- [visibly-pushdown-transducers/desc.md](../visibly-pushdown-transducers/desc.md)
- [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)

### 同类型或同家族工作

- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准；look-around、`MSO` 与 tree-walking transducer 是其主要外部连接点。

### 与本研究关系最紧的工作

- 它最适合挂到 `Visibly Pushdown Transducers` 之下，作为继续追 `MSO`-级 nested-word / tree transformation 的关键节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Two-Way Visibly Pushdown Automata / Transducers (2VPA / 2VPT)`
- 论文角色：模型扩展
- 核心功能：在 visible stack discipline 下给 nested-word automata / transducer 增加双向读头，从而实现更强的结构化变换。
- 关键特性：双向读头、位置-方向-栈 configuration、look-around 闭包、single-use、与 `MSO` transduction 的精确对应。
- 构造方式：`2VPA=(Q,q_I,F,\Gamma,\delta)` 加 `2VPT=(A,O)`，并按规则序列拼接输出。
