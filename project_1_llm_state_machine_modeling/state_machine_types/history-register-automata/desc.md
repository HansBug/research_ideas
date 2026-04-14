# 历史-寄存器自动机 / History-Register Automata

## 基本信息

- 标题：History-Register Automata
- 中文标题：历史-寄存器自动机
- 作者：Radu Grigore, Nikos Tzevelekos
- 发表：*Logical Methods in Computer Science*, 12(1:7):1-32, 2016
- DOI：`10.2168/LMCS-12(1:7)2016`
- 链接：https://arxiv.org/abs/1209.0680
- 形式主义：`History-Register Automata (HRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 histories / registers assignment、`(X,X')` 接受标签与 reset 标签。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `(m,n)`-HRA 元组、assignment 更新和 configuration graph。

## 简报

这篇论文把 infinite-alphabet automata 再往前推进了一步：不仅能像 register automata 那样保存少量名字，还能维护若干无界的 histories，并允许消费、删除和 reset。这样得到的 `HRA` 不再只是“记住一个名字以后比较”，而是能表达 fresh-name generation、name consumption、history reset 这些更贴近动态资源分配的模式。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上的强模型节点，位于 register / class-memory 一侧的上层母型。
- 构造方式简述：机器维护若干 histories 和 registers；标签 `(X,X')` 表示“读入一个恰好出现在 places `X` 中的名字，并把它重放到 `X'` 中”，标签 `X` 表示 reset。
- 基础设施与场景简述：原文是纯理论工作，但给出 closure、Ackermann / ExpSpace / PSpace 级空性复杂度，以及与 RA / FRA / CMA / data-automata 支线的清晰联系。

```text
无限名字序列 -> 有限控制 + histories / registers -> freshness / reuse / reset -> name-aware language analysis
```

## 形式主义定义与核心对象

### 定义对象

`HRA` 处理的是来自无限名字域 `\mathbb N` 的有限字符串。它假定输入字母本身就是名字，或可编码成名字，并且需求要显式区分 fresh、seen-before、consumed、reset 后再见等模式。

### 核心抽象

对固定的 histories 数 `m` 与 registers 数 `n`，原文先定义 assignment 集合：

$$
\mathrm{Asn} = \{ H : [m+n] \to \mathcal P_{\mathrm{fin}}(\mathbb N) \mid \forall i > m,\ |H(i)| \le 1 \}
$$

上式中的符号逐项解释如下：

1. `[m+n]` 是 places 的编号集合。
2. 前 `m` 个 places 是 histories，每个都可保存无界有限名字集。
3. 后 `n` 个 places 是 registers，每个至多保存一个名字。

在此基础上，`(m,n)`-HRA 被定义为：

$$
A = \langle Q, q_0, H_0, \delta, F \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_0 \in Q` 是初始状态。
3. `H_0 \in \mathrm{Asn}` 是初始 assignment。
4. `\delta \subseteq Q \times \mathrm{Lab} \times Q` 是转移关系。
5. `F \subseteq Q` 是终态集。

其中标签分两类：

1. `(X,X')`：读取一个恰好出现在 places `X` 中的名字，并把它更新到 `X'`。
2. `X`：执行 reset，把 `X` 中所有 places 清空。

### 一个最小例子与通俗解释

论文一开始就用“名字生成者 `P` 和名字消费者 `O`”来说明动机。可以把输入看成一串 `(P,a)` 或 `(O,a)` 事件；`HRA` 要求每个被 `O` 消费的名字都必须先被 `P` 产生过，而且同一个名字不能被反复消费。

通俗地说，`HRA` 像“有限状态机 + 有界便签槽 + 若干历史仓库”。register 负责精确保存少量名字，history 则像一个名字集合仓库；reset 相当于把某个仓库整批清空。

### 运行 / 接受 / 转移语义

给定 assignment `H` 和 place 集合 `X`，原文定义

$$
H@X = \bigcap_{i \in X} H(i) \setminus \bigcup_{i \notin X} H(i)
$$

它表示“恰好出现在 `X` 这些 places 中、而不出现在其他 places 中”的名字集合。

若名字 `a` 被接受并更新到 `X'`，则记作 `H[a \text{ in } X']`。因此 configuration graph 上的语义可压成：

$$
(q,H) \xrightarrow{a} (q',H')
$$

当且仅当存在 `q \xrightarrow{X,X'} q' \in \delta`，满足 `a \in H@X` 且 `H' = H[a \text{ in } X']`。

对应的 reset 语义是：

$$
(q,H) \xrightarrow{\varepsilon} (q', H[X \mapsto \varnothing])
$$

当且仅当存在 `q \xrightarrow{X} q' \in \delta`。

上式中的符号逐项解释如下：

1. `H[X \mapsto \varnothing]` 表示把 `X` 中所有 histories / registers 直接清空。
2. `\varepsilon` 转移来自 reset，不消耗输入名字。
3. 对 register 来说，“写入名字”会覆盖掉原有单个内容；对 history 来说则是集合更新。

### 语义边界

`HRA` 虽然比普通 register automata 强得多，但它仍是纯离散语言模型：没有 clocks、没有连续变量、没有概率。它的核心增强是名字历史与 reset，而不是数值约束。

### 关键性质与判定边界

原文给出的一条结构性结论是：

$$
\text{RA} \subseteq \text{HRA}, \qquad \text{FRA} \subseteq \text{HRA}
$$

并且一般 `HRA` 语言对下列运算封闭：

$$
\cup,\ \cap,\ \cdot,\ {}^*
$$

但不对补运算封闭：

$$
\mathrm{Lang}(\mathrm{HRA}) \text{ is not complement-closed}
$$

空性复杂度方面，原文给出三层非常清楚的边界：

$$
\mathrm{emptiness}(\mathrm{HRA}) \text{ is Ackermann-complete}
$$

$$
\mathrm{emptiness}(\mathrm{non\text{-}reset\ HRA}) \text{ is ExpSpace-complete}
$$

$$
\mathrm{emptiness}(\mathrm{unary\ HRA}) \text{ is PSpace-complete}
$$

上面几式中的符号逐项解释如下：

1. `non-reset HRA` 指没有 reset 标签的子类。
2. `unary HRA` 指只有单个 history 的受限版本。
3. 这组复杂度结果清楚说明：reset 是表达力与计算代价同时上升的关键来源。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然是有限状态控制。 |
| 事件 / 触发 | 强支持 | 每个输入名字或 reset 转移都触发状态更新。 |
| 守卫 / 数据 | 强支持 | 可判断 fresh / seen-before / precise-place-membership。 |
| 层次 | 不支持 | 不直接处理树层次，但可表达 history nesting 风格的信息流。 |
| 并发 / 同步 | 不支持 | 模型对象仍是线性名字串。 |
| 时间约束 | 不支持 | 无实时时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | closure 明确，空性复杂度分层清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| assignment | `$\mathrm{Asn}=\{H:[m+n]\to\mathcal P_{\mathrm{fin}}(\mathbb N)\mid \forall i>m,\ |H(i)|\le 1\}$` | histories / registers 的统一存储语义。 |
| 模型元组 | `$A=\langle Q,q_0,H_0,\delta,F\rangle$` | `HRA` 的标准定义。 |
| name guard | `$a \in H@X$` | 判断输入名字是否恰好出现在指定 places 中。 |
| update | `$H' = H[a \text{ in } X']$` | 接受后把名字重分配到新 places。 |
| 复杂度边界 | `Ackermann / ExpSpace / PSpace` | general、non-reset、unary 三类空性问题的主结果。 |

## 构造方式与承载格式

### 建模入口

1. 列出哪些 places 需要是 histories，哪些只需单格 registers。
2. 判断每类输入名字应在什么 precise-place pattern 下才允许被读入。
3. 决定读入后要把名字移动到哪些 places。
4. 只在确实需要“批量忘记历史”时引入 reset。

### 机器可处理承载方式

机器可处理承载方式就是 `(m,n)`-assignment、`(X,X')` / `X` 标签与 configuration graph，没有单独的文本 DSL。

### 交换与互操作

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，`HRA` 多了 histories、reset 与 precise-place-membership；相对 [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)，它更操作式、也更贴近 name consumption；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它更强调 freshness / history，不强调 alternation 与 data-tree。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 assignment、history / register 更新与 configuration graph。
- 仿真/执行支持：可直接按 labelled transition system 解释。
- 验证/分析支持：closure analysis、VASS-style 空性分析、与 RA / FRA / CMA 的翻译。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：与 automata over infinite alphabets、program analysis、name-generation semantics、data automata 理论密切相连。

## 适用场景与需求前提

### 适用场景

适合建模带无限名字域的生成、消费、重复使用和 reset 过程，例如 fresh resource creation、动态分配对象名、会话 / 引用 / 文件名的生命周期分析。

### 需求前提

1. 输入可以压成一串名字事件。
2. 核心约束依赖名字是否 fresh、是否曾出现、是否存于某类历史集合。
3. 系统行为最好能表述成有限种 history / register 更新模式。

### 不适用或高成本场景

如果需求需要算术、时钟、树导航或栈递归，`HRA` 不是合适终点；若根本不需要 reset / consumption，non-reset HRA、class-memory 或更轻的 FMA / register 支线通常更合适。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，`HRA` 明显更强，已经能表达 name generation / consumption / reset；相对 [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)，它与 non-reset / weak variants 存在直接等价桥梁；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，两者都在 infinite alphabet 上工作，但 `HRA` 的核心机制是 histories，而不是 alternation + register threads。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Data / Infinite-Alphabet` 这条支线从“能比较历史名字”推进到“能管理名字生命周期”，使演化树在 automata-theory 主干上更完整。

### 作为目标形式主义还是中间表示

更适合作为理论母型或中间表示，而不是控制系统常规建模语言。

### 对需求到模型生成的启发

当需求文本里出现“创建一个新标识符”“以后只能消费一次”“某次 reset 后名字视作忘记”这类模式时，LLM 可以考虑先生成 HRA 级别的中间模型，再判断是否需要向下退化或向上提升。

### 现实限制

虽然理论分支很强，但工程生态薄弱；原文不提供工具链，因此它主要服务于谱系和形式化表达边界，而不是直接落地。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)
- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补到当前演化树 `Finite Automata -> Data / Infinite-Alphabet` 的 `history / freshness / reset` 子枝。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`History-Register Automata (HRA)`
- 论文角色：模型提出
- 核心功能：用 histories / registers 管理无限名字域中的 freshness、reuse、consumption 与 reset。
- 关键特性：precise-place membership、reset、RA/FRA generalization、Ackermann / ExpSpace / PSpace 空性边界。
- 构造方式：`(Q,q_0,H_0,\delta,F)` 元组加 `(X,X')` / `X` 标签和 configuration graph。
- 基础设施：纯理论模型，无工程标准；核心是 assignment、history updates、VASS-style analysis 与 CMA bridge。
- 适用场景：动态资源名、fresh-value generation、引用/会话生命周期、name-aware verification。
- 需求前提：输入可压成名字事件串，且主要约束依赖名字历史与 reset。
- 状态：🟢
