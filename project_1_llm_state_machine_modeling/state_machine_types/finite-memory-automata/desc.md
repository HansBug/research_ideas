# 有限记忆自动机 / Finite-memory automata

## 基本信息

- 标题：Finite-memory automata
- 中文标题：有限记忆自动机
- 作者：Michael Kaminski, Nissim Francez
- 发表：*Theoretical Computer Science*, 134(2):329-363, 1994
- DOI：`10.1016/0304-3975(94)90242-9`
- 链接：https://archive.org/details/memory-automata
- 形式主义：`Finite-Memory Automata (FMA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是有限状态、初始 assignment、window reassignment 与 transition relation。
- 标准/格式获取方式：原文没有 DSL 或交换格式，核心承载方式是 window assignment、configuration semantics 与 quasi-regular language 定义。

## 简报

这篇论文把“有限状态骨架如何处理无限字母表”这个老问题压成了一个很克制的模型：自动机仍然只有有限个控制状态，但额外挂一组只能复制和比较、不能算术加工的 windows。这样得到的 `FMA` 既比普通 `Finite Automata` 强，能记住有限个先前见过的无限域符号；又没有强到退化成任意无限状态程序。

- 形式主义定位：`Finite Automata` 主干下 `Data / Infinite-Alphabet` 支线的早期母节点。
- 构造方式简述：每步只允许判断当前输入是否已经在某个 window 中；若没有，就把它写入指定 window，再按该 window 的编号转移。
- 基础设施与场景简述：原文是纯理论工作，但稳定给出 quasi-regular 语言、空性可判定、布尔/连接闭包边界，以及 deterministic / two-way 变体。

```text
无限字母表输入 -> 有限控制 + 有界 windows -> substitution / equality pattern -> quasi-regular language
```

## 形式主义定义与核心对象

### 定义对象

`FMA` 处理的是来自无限字母表 `\Sigma` 的有限字符串。它不假设字母上有额外算术结构，自动机真正能观察到的只是“这个符号是否等于某个之前存过的符号”。

### 核心抽象

原文把一个 `r`-window 的有限记忆自动机写成：

$$
A = (S, q_0, u, \rho, \mu, F)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `q_0 \in S` 是初始状态。
3. `u \in (\Sigma \cup \{\#\})^r` 是初始 assignment；`u_i = \#` 表示第 `i` 个 window 为空。
4. `\rho : S \rightharpoonup \{1,\ldots,r\}` 是 partial reassignment function，规定在“新符号”出现时把它写入哪个 window。
5. `\mu \subseteq S \times \{1,\ldots,r\} \times S` 是转移关系。
6. `F \subseteq S` 是终态集。

原文还要求 assignment 中任意真实输入符号在所有 windows 里最多出现一次。也就是说，对

$$
w = w_1 w_2 \cdots w_r \in (\Sigma \cup \{\#\})^r
$$

如果 `w_i = w_j` 且 `i \ne j`，那么只能有 `w_i = w_j = \#`。

### 一个最小例子与通俗解释

一个最小例子是识别

$$
L = \{ aa \mid a \in \Sigma \}
$$

的两步机器。它先在初态把第一个输入符号写入唯一 window，再读取第二个符号时要求它等于该 window 的内容后接受。

通俗地说，`FMA` 像“只有几个便签槽的有限自动机”。普通有限自动机只能分辨有限字母；`FMA` 还能把少量“见过的真实符号”塞进便签槽里，之后再问“现在这个是不是刚才那个”。

### 运行 / 接受 / 转移语义

原文的 configuration 是状态与 assignment 的二元组：

$$
(s, w) \in S \times (\Sigma \cup \{\#\})^r
$$

若当前读到输入符号 `\sigma`，则 induced configuration transition relation `\mu_C` 可以保守压成两种情况：

$$
((s,w), \sigma, (t,v)) \in \mu_C
$$

当且仅当满足下面之一：

1. `\sigma` 已经等于某个 window `k` 的内容，且 `(s,k,t) \in \mu`，此时 `v = w`。
2. `\sigma \notin [w]`，并且 `\rho(s) = k` 已定义且 `(s,k,t) \in \mu`，此时把 `\sigma` 写入第 `k` 个 window，得到新 assignment `v`。

上式中的符号逐项解释如下：

1. `[w]` 表示当前 assignment 中非空窗口所包含的真实输入符号集合。
2. 第一种情况对应“旧符号比较成功”。
3. 第二种情况对应“新符号出现并触发 substitution / copy”。

### 语义边界

`FMA` 只能复制和比较有限个已见符号，不能计数、不能对无限域做算术、也不能把同一真实符号无限复制到不同寄存单元。因此它更像“有限自动机加有限记忆槽”，而不是通用数据程序。

### 关键性质与判定边界

原文最关键的正结果之一是：当字母表退化成有限集时，`FMA` 与普通有限自动机等价。可压成

$$
\Sigma \text{ finite} \implies \mathrm{FMA} \equiv \mathrm{FA}
$$

对无限字母表，论文把可识别语言称为 quasi-regular languages，并证明：

$$
\mathrm{QuasiRegular} \text{ 对 } \cup,\ \cap,\ \cdot,\ {}^* \text{ 封闭}
$$

同时，

$$
\mathrm{emptiness}(\mathrm{FMA}) \text{ is decidable}
$$

但一般并不满足：

$$
\mathrm{QuasiRegular} \text{ is closed under complement}
$$

上面几式中的符号逐项解释如下：

1. `\cdot` 表示串连接。
2. `${}^*` 表示 Kleene star。
3. `\mathrm{emptiness}(\mathrm{FMA})` 指“给定一台 `FMA`，判断其语言是否为空”的判定问题。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限控制状态仍是主骨架。 |
| 事件 / 触发 | 强支持 | 每个输入符号触发一次 equality / substitution 决策。 |
| 守卫 / 数据 | 强支持 | 支持无限字母表上的 equality pattern，但只限有限个 windows。 |
| 层次 | 不支持 | 没有树层次或栈结构。 |
| 并发 / 同步 | 不支持 | 单串、单控制流模型。 |
| 时间约束 | 不支持 | 无 clocks、无密集时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，且有清楚的 closure / non-closure 边界。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(S,q_0,u,\rho,\mu,F)$` | `FMA` 的标准定义。 |
| configuration | `$(s,w)$` | 运行状态由有限控制与当前 window assignment 组成。 |
| 新符号写入 | `$\sigma \notin [w] \land \rho(s)=k$` | 当输入是 fresh symbol 时执行 substitution。 |
| 空性可判定 | `$\mathrm{emptiness}(\mathrm{FMA})$ decidable` | 仍保留了 regular-style 的核心判定性。 |
| 非补闭包 | `$\mathrm{QuasiRegular}$ not complement-closed` | 无限字母表上代价最明显的边界。 |

## 构造方式与承载格式

### 建模入口

1. 确定输入对象是否真的是“无限字母表上的有限串”。
2. 识别需求里哪些约束只依赖“是否等于某个先前出现的符号”。
3. 分配有限个 windows，决定哪些状态下需要把 fresh symbol 写入哪个 window。
4. 再补终态与允许的 equality-based transitions。

### 机器可处理承载方式

机器可处理承载方式就是：

1. 初始 assignment `u`。
2. reassignment function `\rho`。
3. transition relation `\mu`。
4. configuration semantics `\mu_C`。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

`FMA` 与 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md) 的差别，在于输入字母表不再有限；与 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md) 相比，它没有显式寄存器线程、alternation 和 data-tree 结构。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 assignment、window、configuration 与 induced transition relation。
- 仿真/执行支持：可直接按 configuration relation 解释运行。
- 验证/分析支持：空性判定、closure analysis、deterministic / two-way variants。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：后续 infinite-alphabet / data automata、register-family 与 XML/data-language 理论经常把它视作早期参照。

## 适用场景与需求前提

### 适用场景

适合处理“事件标签来自无限域，但控制逻辑只关心有限次记忆与相等比较”的语言问题，例如 ID 重复、简单 fresh / repeat pattern、有限资源名流。

### 需求前提

1. 输入是线性序列，不是树、图或带时间的轨迹。
2. 对无限域值的操作最好只限 equality / disequality 模式。
3. 需求里真正需要记住的历史数据个数可以压成常数个 windows。

### 不适用或高成本场景

若需求需要多寄存器布尔组合、层次树结构、显式栈、概率、时间或算术关系，那么 `FMA` 很快就不够；这时更合适的是 register / class-memory / timed / pushdown 等后续分支。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，`FMA` 是对有限自动机在 infinite alphabet 上的克制推广；相对 [history-register-automata/desc.md](../history-register-automata/desc.md)，它没有 histories / reset / freshness-consumption 机制；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它更早、更弱，也没有 alternation 与 data tree。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树里 `Finite Automata -> Data / Infinite-Alphabet` 这条支线的最早稳定母节点补出来，使后续 `ARA`、`class-memory`、`HRA` 等条目不再悬空。

### 作为目标形式主义还是中间表示

更适合作为理论母型和谱系节点，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求文本里只是反复出现“同一个编号是否又出现了”“某个新名字后来是否被再次引用”这类模式，那么 LLM 不必立刻上更重的 register / data logic 模型，可以先判断 `FMA` 级别是否已足够。

### 现实限制

它的表达力来自有限 equality memory，而不是工程生态；原文也没有给出现成工具链，因此更适合做演化树与理论边界工作。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)

### 同类型或同家族工作

- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)
- [history-register-automata/desc.md](../history-register-automata/desc.md)
- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或文件格式。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树 `Finite Automata -> Data / Infinite-Alphabet` 的最早母节点位置。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Finite-Memory Automata (FMA)`
- 论文角色：模型提出
- 核心功能：用有限个 windows 在无限字母表上实现有限记忆的 substitution / equality pattern 识别。
- 关键特性：finite control、bounded windows、quasi-regular languages、空性可判定、非补闭包。
- 构造方式：`(S,q_0,u,\rho,\mu,F)` 元组加 assignment / configuration semantics。
- 基础设施：纯理论模型，无工程标准；核心是 windows、substitution、closure analysis 与 deterministic / two-way variants。
- 适用场景：infinite alphabet 上的简单数据重复/首次出现模式、有限记忆数据语言。
- 需求前提：输入是线性串，数据约束主要依赖有限个已见符号的 equality pattern。
- 状态：🟢
