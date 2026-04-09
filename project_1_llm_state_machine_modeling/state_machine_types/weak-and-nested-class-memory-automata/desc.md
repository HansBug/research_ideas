# 弱与嵌套类记忆自动机 / Weak and Nested Class Memory Automata

## 基本信息

- 标题：Weak and Nested Class Memory Automata
- 中文标题：弱与嵌套类记忆自动机
- 作者：Conrad Cotton-Barratt, Andrzej S. Murawski, C.-H. Luke Ong
- 发表：*Language and Automata Theory and Applications*, pp. 188-199, 2015
- DOI：`10.1007/978-3-319-15579-1_14`
- 链接：https://www.cs.ox.ac.uk/andrzej.murawski/papers/lata15.pdf
- 形式主义：`Weak / Nested Class-Memory Automata (weak CMA / weak NDCMA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 class memory function、weak acceptance 条件和 nested-data transition map。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `CMA / NDCMA` 元组、data word / nested data set 和 class memory update 语义。

## 简报

这篇论文做了两件都很关键的事。第一，它把 `Class Memory Automata` 的 local acceptance 去掉，得到 `weak CMA`，并证明它与 locally prefix-closed `Data Automata`、`Class Counting Automata`、non-reset `HRA` 是同一类语言。第二，它把类记忆思想推进到 nested data，得到 `NDCMA`，然后证明“一般嵌套版不可判定，但加 weakness 后又回到可判定”。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上 `class-memory` 方向的重要分叉节点。
- 构造方式简述：每个数据值都关联一个“上次见到它时自动机处于什么状态”的 class memory；嵌套版则对一个数据值及其所有祖先同时做这种记录。
- 基础设施与场景简述：原文纯理论，但把 `weak CMA` 直接桥接到 `pDA / CCA / non-reset HRA`，并把 nested version 接到 `NDA / HOMCA` 复杂度链条上。

```text
data word / nested data -> class memory update -> weak acceptance or nested ancestors -> infinite-alphabet language analysis
```

## 形式主义定义与核心对象

### 定义对象

`CMA` 处理的是 data words：每个位置除了有限字母表标签，还携带一个来自无限域的数据值。论文进一步引入 nested data set，使数据值之间带有父子层次，适合建模进程生成、层次命名和多级上下文。

### 核心抽象

原文回顾的 `Class Memory Automaton` 可写成：

$$
A = \langle Q, \Sigma, q_I, \delta, F_L, F_G \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是有限输入字母表。
3. `q_I \in Q` 是初始状态。
4. `\delta : Q \times \Sigma \times Q_? \to \mathcal P(Q)` 是转移函数。
5. `F_L \subseteq Q` 是 locally accepting states。
6. `F_G \subseteq Q` 是 globally accepting states。

其中 `Q_? = Q \cup \{?\}`，`?` 表示某个数据值此前从未见过。类记忆函数是

$$
f : D \to Q_?
$$

且只有有限多个数据值 `d` 满足 `f(d) \ne ?`。

对 `weak CMA`，论文采用的关键限制是：去掉 local acceptance 条件，只保留全局终态条件。因此它保留“记住每个数据值最近一次所处状态”的能力，但不再要求每个数据值最终停在某个 locally accepting state。

### 一个最小例子与通俗解释

一个直观例子是“每个进程 ID 对应一串事件交错出现，但我们想记住这个 ID 最近处于哪个控制状态”。`weak CMA` 每次读到某个 ID，就先查询“上次这个 ID 出现时最后处在哪个状态”，再决定当前怎么转移，并把该 ID 的 memory 覆盖成新状态。

通俗地说，`weak CMA` 像“对每个数据值都挂了一条最近状态便签的有限自动机”；而 `weak NDCMA` 则像“对一个数据值及其祖先链都挂便签”。

### 运行 / 接受 / 转移语义

`CMA` 的 configuration 写成：

$$
(q,f)
$$

其中 `q \in Q` 是当前控制状态，`f : D \to Q_?` 是当前 class memory function。

若当前输入为 `(a,d) \in \Sigma \times D`，则一步转移满足：

$$
(q,f) \xrightarrow{(a,d)} (q', f[d \mapsto q'])
$$

当且仅当

$$
q' \in \delta(q, a, f(d))
$$

上式中的符号逐项解释如下：

1. `f(d)` 是自动机上次见到数据值 `d` 时记录的状态，或 `?`。
2. `f[d \mapsto q']` 表示把数据值 `d` 的 memory 覆盖成新状态 `q'`。
3. 对 weak 版本，接受只需最终 `q' \in F_G`，不再检查所有数据值的局部接受性。

对 level-`l` 的 nested data，论文给出的 `NDCMA` transition map 是：

$$
\delta = \bigcup_{1 \le i \le l} \delta_i,\qquad
\delta_i : Q \times \Sigma \times (\{i\} \times (Q_?)^i) \to \mathcal P(Q)
$$

这表示：若当前数据值处于第 `i` 层，则自动机不仅能看到它自己的记忆，还能同时看到它所有祖先的记忆。

### 语义边界

`weak CMA` 相比完整 `CMA` 更易判定，但表达力更弱；`NDCMA` 引入嵌套数据后表达力很强，一般空性不可判定。weakness 在这里不是小修小补，而是“重新把系统拉回可判定区”的结构约束。

### 关键性质与判定边界

原文第一条关键结论是：

$$
\text{weak CMA} \equiv \text{locally prefix-closed DA} \equiv \text{CCA} \equiv \text{non-reset HRA}
$$

并且这种等价是 `PTime`-equivalent。

对 deterministic weak CMA，论文进一步证明：

$$
\text{deterministic weak CMA are closed under all Boolean operations}
$$

于是：

$$
\mathrm{containment}(\mathrm{det\ weak\ CMA}),\ \mathrm{equivalence}(\mathrm{det\ weak\ CMA})
$$

都是 `ExpSpace`-complete。

对嵌套版，论文给出的主结论是：

$$
\mathrm{emptiness}(\mathrm{NDCMA}) \text{ is undecidable}
$$

但

$$
\mathrm{weak\ NDCMA} \equiv \mathrm{pNDA}
$$

并恢复空性可判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态仍是主骨架。 |
| 事件 / 触发 | 强支持 | 每个 data word 位置触发一次 class-memory lookup/update。 |
| 守卫 / 数据 | 强支持 | 核心就是对无限数据值最近状态的记忆。 |
| 层次 | 部分支持 | `weak NDCMA` 支持 nested data 的祖先链记忆。 |
| 并发 / 同步 | 不支持 | 输入对象仍是线性数据词。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 与 pDA / CCA / non-reset HRA 等价，且 deterministic weak 版本有完整布尔闭包。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| baseline tuple | `$A=\langle Q,\Sigma,q_I,\delta,F_L,F_G\rangle$` | `CMA` / `weak CMA` 的标准骨架。 |
| class memory | `$f:D\to Q_?$` | 为每个数据值记录“最近一次处于哪个状态”。 |
| 单步转移 | `$q' \in \delta(q,a,f(d))$` | 转移依赖当前数据值的 memory。 |
| 等价桥梁 | `$\text{weak CMA} \equiv \text{pDA} \equiv \text{CCA} \equiv \text{non-reset HRA}$` | 该论文最重要的谱系结论。 |
| nested boundary | `$\mathrm{emptiness}(\mathrm{NDCMA})$ undecidable, $\mathrm{weak\ NDCMA}$ decidable` | weakness 是恢复可判定性的关键。 |

## 构造方式与承载格式

### 建模入口

1. 先判断输入是否天然是 data word。
2. 若只需跟踪每个数据值最近状态，用 `weak CMA`。
3. 若数据值有父子层次、并需要祖先上下文，则升级到 `weak NDCMA`。
4. 只有当确实需要“每个数据值自身也必须落在局部可接受状态”时才回到完整 `CMA`。

### 机器可处理承载方式

机器可处理承载方式是 automaton tuple 加 class memory function / nested-data ancestor lookup，没有固定 DSL。

### 交换与互操作

相对 [history-register-automata/desc.md](../history-register-automata/desc.md)，它更抽象地保存“最近状态”，而不是显式 histories / reset；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它更偏 per-data-value memory，而不是 one-register thread 与 alternation；相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它已经进入更成熟的数据词自动机阶段。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 class memory function、nested data set 与 ancestor-aware transition map。
- 仿真/执行支持：可直接按配置 `(q,f)` 演化。
- 验证/分析支持：`pDA / CCA / non-reset HRA / NDA / HOMCA` 等价翻译与复杂度结果。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 data automata、nested-data logic、程序验证和数据库理论中的标准理论节点。

## 适用场景与需求前提

### 适用场景

适合 per-identifier protocol、并发进程交错行为、嵌套命名、spawned subprocess 这类“无限数据值 + 最近状态记忆”问题。

### 需求前提

1. 输入能写成 data words。
2. 核心约束是“这个数据值上次出现时处于什么状态”。
3. 若使用嵌套版，数据值之间确实存在稳定的祖先结构。

### 不适用或高成本场景

如果需求依赖显式 reset / history consumption，`HRA` 更自然；如果需求是 data tree 上的导航和 alternation，`ARA / ATRA` 更自然；如果不需要 infinite-alphabet，普通 `FA` 就够。

## 与相邻形式主义的关系

相对 [history-register-automata/desc.md](../history-register-automata/desc.md)，weak CMA 与 non-reset HRA 在语言层面等价，但操作直觉不同；相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它已经不是“有限个 windows 记住少量真实符号”，而是给每个数据值都保留一个抽象 last-state；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，两者都在 data words 上工作，但这里的 memory 颗粒度是“每个数据值一条最近状态”。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里的 `class-memory` 支线补成稳定节点，同时把 `HRA`、`pDA`、`CCA`、nested data 这些旁支连成一条连续的谱系。

### 作为目标形式主义还是中间表示

更适合作为理论节点与中间表示，而不是最终控制系统建模语言。

### 对需求到模型生成的启发

若需求文本里充满“某个 ID 最近处于什么阶段”“每个子任务都要独立满足某个本地条件”“新子任务继承父任务上下文”这类模式，LLM 可优先考虑 class-memory 风格抽象。

### 现实限制

原文没有工程工具和标准格式；它主要提供的是谱系、判定边界和与其他模型的翻译关系。

## 重要的相关工作

### 奠基或前身工作

- `CMA / DA` 原始工作
- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [history-register-automata/desc.md](../history-register-automata/desc.md)
- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补到当前演化树 `Data / Infinite-Alphabet` 的 `class-memory / nested-data` 分支。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Weak / Nested Class-Memory Automata (weak CMA / weak NDCMA)`
- 论文角色：模型扩展
- 核心功能：把 class-memory automata 推到 weak 与 nested 两条子线，并恢复/分析对应判定边界。
- 关键特性：per-data last-state memory、deterministic Boolean closure、nested data、与 `pDA / CCA / non-reset HRA` 等价。
- 构造方式：`(Q,\Sigma,q_I,\delta,F_L,F_G)` 元组加 class memory function；nested 版再加 ancestor-aware transition map。
- 基础设施：纯理论模型，无工程标准；核心是与 `DA / HRA / NDA / HOMCA` 的翻译关系。
- 适用场景：data words、并发 ID 行为、层次命名、spawn / subprocess 结构。
- 需求前提：输入带无限数据值，且核心逻辑可压成“最近状态记忆”或祖先链记忆。
- 状态：🟢
