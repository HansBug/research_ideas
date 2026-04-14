# 一类稳健的数据语言及其学习应用 / A Robust Class of Data Languages and an Application to Learning

## 基本信息

- 标题：A Robust Class of Data Languages and an Application to Learning
- 中文标题：一类稳健的数据语言及其学习应用
- 作者：Benedikt Bollig，Peter Habermehl，Martin Leucker，Benjamin Monmege
- 发表：*Logical Methods in Computer Science*, 10(4:19):1-23, 2014
- DOI：`10.2168/LMCS-10(4:19)2014`
- 链接：https://doi.org/10.2168/LMCS-10(4:19)2014
- 形式主义：`Session Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 规范化与学习框架
- 工具/实现获取方式：原文未提供现成仓库；机器可处理入口是 session automaton tuple、symbolic normal form、canonical session automaton 与 membership/equivalence-query 学习流程。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 fresh-register automaton 的受限标签系统、`k`-bounded symbolic words 与 canonical automaton。

## 简报

这篇论文提出的 `Session Automata`，可以看成是 `Fresh-Register Automata` 的一个“稳健化”子类。它保留 global freshness，但丢掉 local freshness，于是语言类虽然变弱，却换来了 canonical form、`k`-bounded symbolic representation、resource-sensitive complement 以及 inclusion/equivalence 可判定这些对工程分析特别关键的性质。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上，`Session Automata` 是 `Fresh-Register Automata` 的一个经典子枝。
- 构造方式简述：自动机只允许两类动作，要么把“全局从未出现过”的数据值写入某个寄存器，要么读取当前寄存器里已有的数据值。
- 基础设施与场景简述：原文不仅给出模型本体，还给出了 symbolic normal form、canonical session automaton、逻辑刻画和主动学习算法，因此它比一般 infinite-alphabet automata 更接近“可操作的理论对象”。

```text
data word -> session/freshness discipline -> symbolic normal form -> canonical session automaton -> inclusion / learning
```

## 形式主义定义与核心对象

### 定义对象

`Session Automata` 处理的是 data words：每个位置由有限标签和无限数据值组成。它假设一个数据值的意义更像“一个会话 / session 在时间轴上的生命周期”，因此特别强调：

1. 某个值是否是全局 fresh；
2. 某个已打开的 session 是否仍在寄存器里可被重用；
3. 同时活跃的 session 数是否有界。

### 核心抽象

原文先把基础模型写成 fresh-register automaton：

$$
A=(S,R,\iota,F,\to)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `R` 是有限寄存器集。
3. `\iota` 是初始状态。
4. `F` 是终态集。
5. `\to` 是带标签的转移关系。

`Session Automata` 是它的一个语法受限子类：转移标签只能来自“读寄存器中的旧值”或“写入全局 fresh 值”。若用原文记号，可理解为：

$$
\text{label}\in \Sigma\times(R^{\mathsf{fresh}}\cup R^{\mathsf{read}})
$$

其中：

1. `r^{\mathsf{fresh}}` 表示读取一个此前在整条运行历史中从未出现过的数据值，并把它写入寄存器 `r`。
2. `r^{\mathsf{read}}` 表示当前数据值必须等于寄存器 `r` 中已保存的值。

### 一个最小例子与通俗解释

原文的 request / ack 例子很直观：若系统要求“每个进程 ID 最多发起一次 request，之后只能收到自己的 ack”，那么可令：

1. `req` 边使用 fresh-write，把第一次出现的进程 ID 写进寄存器。
2. `ack` 边使用 read，要求 ack 的 ID 就是之前寄存器里的值。
3. 因为 request 只能走 fresh-write，所以同一个 ID 无法第二次发起 request。

通俗地说，`Session Automata` 像“只会打开新会话和继续旧会话的寄存器自动机”。它故意不支持“当前寄存器里没有，但以前出现过也可以重新引入”的 local freshness，因此换来了更规整的语言理论。

### 运行 / 接受 / 转移语义

原文使用 configuration：

$$
(s,\tau,U)
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `\tau:R\rightharpoonup D` 是当前寄存器赋值。
3. `U\subseteq D` 是到目前为止在整条运行历史中见过的数据值集合。

若读入 `(a,d)`，则 fresh-write 语义可写成：

$$
(s,\tau,U)\xrightarrow{(a,d)}(s',\tau[r\mapsto d],U\cup\{d\})\quad \text{if } d\notin U
$$

而 read 语义可写成：

$$
(s,\tau,U)\xrightarrow{(a,d)}(s',\tau,U\cup\{d\})\quad \text{if } \tau(r)=d
$$

上面两式中的符号逐项解释如下：

1. 第一式体现 global freshness：`d` 必须从未在历史 `U` 中出现。
2. 第二式体现 session continuation：当前数据值必须等于寄存器里已存的值。
3. `\tau[r\mapsto d]` 表示把寄存器 `r` 更新为 `d`。

### 语义边界

`Session Automata` 的限制非常刻意：它保留 global freshness，但去掉 local freshness 和 reset 风格能力。因此它：

1. 比 `RA` 更擅长 session / nonce / fresh-ID 语言；
2. 比 `FRA` 更弱，但也更稳健；
3. 不处理栈、树、时钟和连续变量。

### 关键性质与判定边界

原文的关键结果可压成：

$$
\mathrm{RA}\ \text{与}\ \mathrm{SA}\ \text{表达力不可比},\qquad \mathrm{RA},\mathrm{SA}\subsetneq \mathrm{FRA}
$$

$$
L(A)\subseteq DW_k\quad \text{if }A\text{ uses }k\text{ registers}
$$

$$
\mathrm{snf}(L(A))\ \text{is regular over a finite alphabet}
$$

$$
\mathcal L(\mathrm{SA})\ \text{对}\ \cup,\ \cap\ \text{以及 }k\text{-bounded complement 封闭}
$$

上面几式中的符号逐项解释如下：

1. `SA` 表示 `Session Automata`。
2. `DW_k` 是所有 `k`-bounded data words；`k` 反映同时重叠的 session 数上界。
3. `\mathrm{snf}` 是 symbolic normal form，把 data word 规范化成有限字母表上的 symbolic word。
4. `k`-bounded complement 是 resource-sensitive complement，不是对全部 data words 的普通补集。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保持有限状态自动机骨架。 |
| 事件 / 触发 | 强支持 | 每个 data-word 位置触发一次 fresh-write 或 read。 |
| 守卫 / 数据 | 强支持 | 核心是 global freshness 与寄存器相等测试。 |
| 层次 | 不支持 | 对象仍是线性 data word。 |
| 并发 / 同步 | 不支持 | 无显式并发算子，但可表达多 session 交错。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | canonical form、inclusion/equivalence、logical characterization 与 learning 全部可做。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(S,R,\iota,F,\to)$` | 继承 fresh-register automata 骨架。 |
| fresh-write | `$d\notin U$` | 只能打开全局新 session。 |
| `k`-bounded | `$L(A)\subseteq DW_k$` | 使用 `k` 个寄存器就只能识别 `k`-bounded 语言。 |
| symbolic 规整化 | `$\mathrm{snf}(L(A))$ regular` | 这是 canonical automaton 的基础。 |
| 理论收益 | inclusion/equivalence decidable | 相比一般 `RA/FRA` 更稳健。 |

## 构造方式与承载格式

### 建模入口

1. 先判断对象是否天然具有“打开 session / 继续 session / 结束 session”的生命周期语义。
2. 再估计同时活跃的 session 数能否压成小的 `k`。
3. 用 fresh-write 边表示创建新会话，用 read 边表示继续旧会话。
4. 若需求依赖 local freshness 或任意旧值重引入，应转向 `RA/FRA`。

### 机器可处理承载方式

机器可处理承载方式就是：

1. `Session Automaton` 本体；
2. `k`-bounded symbolic words；
3. symbolic normal form `snf`；
4. canonical session automaton。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它与 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md) 的关系最直接：`Session Automata` 就是 `FRA` 的经典子类；它也与 [variable-automata-over-infinite-alphabets/desc.md](../variable-automata-over-infinite-alphabets/desc.md) 一样试图改善 infinite-alphabet automata 的“可用性”，但路径不同，前者靠 bounded symbolic normalization，后者靠 pattern syntax。

## 配套基础设施

- 建模/编辑工具：原文未提供成品工具。
- 解析/交换/元模型支持：核心是 `snf`、well-formed symbolic words 与 canonical automaton。
- 仿真/执行支持：可直接按 fresh-write / read 语义执行。
- 验证/分析支持：union、intersection、resource-sensitive complement、inclusion/equivalence 判定。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：在 data-word learning、logic characterization 与 robust infinite-alphabet automata 方向上非常关键。

## 适用场景与需求前提

### 适用场景

适合 security protocol nonce、会话标识、一次性 process ID、连接建立与释放等“数据值天然表示 session”的语言。

### 需求前提

1. 输入可写成 data word。
2. 数据值最重要的性质是“是不是全局第一次出现”以及“之后是否还会被继续引用”。
3. 同时活跃 session 数有现实上界，或至少在模型中可被压成小常数。

### 不适用或高成本场景

如果需求要求 local freshness、寄存器 reset、复杂 class-memory、nested data 或时序/连续语义，`Session Automata` 就不够；这时应使用 `RA/FRA`、`CMA/CRA`、`HRA` 或 timed family。

## 与相邻形式主义的关系

相对 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)，它删掉了 local freshness，因此更弱但更稳健；相对传统 `RA`，它能表达 global fresh session，但又放弃了局部 fresh 那条路，所以二者不可比；相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的 `CMA`，它处理的是“fresh/open session”而不是“每个数据值最近状态”。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里的 freshness 分支从 `Fresh-Register Automata` 继续推进到一个具备 canonical form 和学习算法的经典子类，使 `Data / Infinite-Alphabet` 主线更完整。

### 作为目标形式主义还是中间表示

更适合作为理论节点、规范化中间表示和学习对象，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求文本明确区分“新建一个此前从未见过的 ID”与“继续使用已有会话 ID”时，LLM 应优先考虑 `Session Automata` 风格，而不是把所有 data-word 问题都硬塞到普通 `FSM` 或更重的 `FRA`。

### 现实限制

它的优势依赖 bounded-session 假设；如果真实对象需要大量历史重引入或无界并发 session，模型会迅速变得不自然。

## 重要的相关工作

### 奠基或前身工作

- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)
- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [variable-automata-over-infinite-alphabets/desc.md](../variable-automata-over-infinite-alphabets/desc.md)
- `register automata` 早期母文献
- data-word learning / logical characterization 路线

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或统一工具。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树 `Finite Automata -> Data / Infinite-Alphabet -> Fresh-Register Automata` 之后的 `Session Automata` 子枝。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
