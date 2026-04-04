# 新鲜寄存器自动机 / Fresh-register automata

## 基本信息

- 标题：Fresh-register automata
- 中文标题：新鲜寄存器自动机
- 作者：Nikos Tzevelekos
- 发表：*Proceedings of the 38th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2011)*, pp. 295-306, 2011
- DOI：`10.1145/1926385.1926420`
- 链接：https://doi.org/10.1145/1926385.1926420
- 形式主义：`Fresh-Register Automata (FRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是寄存器赋值 `\sigma`、history `H`、known / locally-fresh / globally-fresh 三类标签与 symbolic bisimulation。
- 标准/格式获取方式：原文没有 DSL 或交换格式，核心承载方式是 `A=(Q,q_0,\sigma_0,\delta,F)` 元组、configuration 语义与 typed-span 级 symbolic simulation。

## 简报

这篇论文把 `Finite-Memory Automata` 的“有限寄存器 + 局部 fresh”能力进一步推进到“全局 fresh-name generation”。换句话说，`FRA` 不只会问“当前输入是不是某个寄存器里没出现过”，还会问“这个名字是不是在整条运行历史里从未出现过”。这一步非常关键，因为很多名字生成、引用分配、`pi`-calculus 式通信语义，真正依赖的是 run-level freshness，而不是仅仅当前寄存器里的局部新鲜。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线里，从 `FMA/RA` 迈向 freshness-aware 名字自动机的关键中间节点。
- 构造方式简述：自动机维护有限个寄存器和一份历史集合；标签 `i` 表示匹配第 `i` 个寄存器，`i•` 表示局部 fresh 写入第 `i` 个寄存器，`i⊛` 表示全局 fresh 写入第 `i` 个寄存器。
- 基础设施与场景简述：原文是纯理论工作，但系统给出闭包性质、空性/普遍性边界、symbolic bisimulation 判定，以及与 `FMA/RA` 和 `π`-calculus 的关系。

```text
无限名字串 -> 有限控制 + 有界寄存器 + 运行历史 -> known / local-fresh / global-fresh 转移 -> freshness-aware language
```

## 形式主义定义与核心对象

### 定义对象

`FRA` 处理的是来自无限名字域 `A` 的有限串。它假定模型关心的是名字是否等于已存名字、是否是当前寄存器里的新名字，以及是否在整条运行历史里从未出现。

### 核心抽象

原文先定义 `n` 个寄存器的赋值集合：

$$
\mathrm{Reg}_n=\{\sigma:[n]\to A\cup\{\sharp\}\mid i\neq j \Rightarrow \sigma(i)=\sigma(j)=\sharp \text{ or } \sigma(i)\neq \sigma(j)\}
$$

上式中的符号逐项解释如下：

1. `[n]=\{1,\ldots,n\}` 是寄存器编号集合。
2. `\sigma(i)` 是第 `i` 个寄存器当前保存的名字。
3. `\sharp` 表示空寄存器。
4. 约束要求真实名字不会同时出现在两个不同寄存器里。

在此基础上，`n` 寄存器 `FRA` 被定义为：

$$
A=(Q,q_0,\sigma_0,\delta,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_0\in Q` 是初始状态。
3. `\sigma_0\in \mathrm{Reg}_n` 是初始寄存器赋值。
4. `\delta\subseteq Q\times L_n\times Q` 是转移关系。
5. `F\subseteq Q` 是接受状态集。

其中 `L_n` 里的关键标签有三类：

1. `i`：匹配寄存器 `i` 中已经存着的名字。
2. `i•`：接受一个对当前寄存器赋值局部 fresh 的名字，并把它写入寄存器 `i`。
3. `i⊛`：接受一个对整条运行历史全局 fresh 的名字，并把它写入寄存器 `i`。

### 一个最小例子与通俗解释

最小例子可以取“所有位置名字都两两不同”的语言：

$$
L_{\mathrm{fresh}}=\{a_1\cdots a_k\in A^* \mid \forall i\neq j,\ a_i\neq a_j\}
$$

一个只带一个寄存器、单个自环状态的 `FRA` 就能识别这个语言：每次都走 `1⊛` 转移，把新读到的全局 fresh 名字写入唯一寄存器，再继续循环。

通俗地说，`FRA` 像“带一份历史账本的寄存器自动机”。普通 `RA/FMA` 只盯着当前几个格子里放了什么；`FRA` 还额外记住“以前整条运行里出现过哪些名字”，因此能表达“这次确实是新创建出来的名字”。

### 运行 / 接受 / 转移语义

原文把 configuration 定义为：

$$
(q,\sigma,H)\in \hat Q=Q\times \mathrm{Reg}_n\times \mathcal P_{\mathrm{fin}}(A)
$$

上式中的符号逐项解释如下：

1. `q` 是当前控制状态。
2. `\sigma` 是当前寄存器赋值。
3. `H` 是到目前为止出现过的名字历史。
4. `\mathcal P_{\mathrm{fin}}(A)` 是 `A` 上所有有限子集。

若当前输入名为 `a`，则关键转移语义可压成：

$$
(q,\sigma,H)\xrightarrow{a}(q',\sigma,H\cup\{a\}) \quad \text{if } (q,i,q')\in\delta \land \sigma(i)=a
$$

$$
(q,\sigma,H)\xrightarrow{a}(q',\sigma[i\mapsto a],H\cup\{a\}) \quad \text{if } (q,i•,q')\in\delta \land a\notin \mathrm{img}(\sigma)
$$

$$
(q,\sigma,H)\xrightarrow{a}(q',\sigma[i\mapsto a],H\cup\{a\}) \quad \text{if } (q,i⊛,q')\in\delta \land a\notin H\cup \mathrm{img}(\sigma_0)
$$

上式中的符号逐项解释如下：

1. `\mathrm{img}(\sigma)` 是当前寄存器里已经存着的名字集合。
2. `\sigma[i\mapsto a]` 表示把寄存器 `i` 更新为 `a`。
3. 第二式只要求 `a` 当前不在寄存器里，因此是局部 fresh。
4. 第三式要求 `a` 没在历史里出现过，因此是全局 fresh。

接受语言定义为：

$$
L(A)=\{w\in (A\cup C)^* \mid (q_0,\sigma_0,\varnothing)\xrightarrow{w *}(q,\sigma,H)\land q\in F\}
$$

这里的 `\xrightarrow{w *}` 表示按输入串 `w` 的逐步转移闭包。

### 语义边界

`FRA` 的核心增强点只有 freshness，而不是一般数据运算。它没有算术、没有时钟、没有树结构、没有并发组件。它比 `FMA/RA` 强在可区分 global fresh 与 local fresh，但仍保持有限控制和有限寄存器骨架。

### 关键性质与判定边界

原文给出的关键边界可以压成：

$$
\mathrm{RA}\subsetneq \mathrm{FRA}
$$

$$
\mathcal L(\mathrm{FRA}) \text{ 对 } \cup,\ \cap \text{ 封闭}
$$

$$
\mathcal L(\mathrm{FRA}) \text{ 不对 } \cdot,\ {}^*,\ \mathrm{complement} \text{ 封闭}
$$

$$
\mathrm{emptiness}(\mathrm{FRA}) \text{ decidable},\qquad \mathrm{universality}(\mathrm{FRA}) \text{ undecidable}
$$

$$
\mathrm{bisimilarity}(\mathrm{FRA}) \text{ decidable}
$$

上面几式中的符号逐项解释如下：

1. `\cdot` 表示串连接。
2. `${}^*` 表示 Kleene star。
3. `\mathrm{emptiness}` 是判断语言是否为空。
4. `\mathrm{universality}` 是判断是否接受全部输入串。
5. bisimilarity 的可判定性来自原文的 symbolic typed-span 构造。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保持有限状态控制骨架。 |
| 事件 / 触发 | 强支持 | 每个输入名字触发 known / local-fresh / global-fresh 三类判断。 |
| 守卫 / 数据 | 强支持 | 支持 equality、局部 fresh、全局 fresh。 |
| 层次 | 不支持 | 不处理树、栈或层次区域。 |
| 并发 / 同步 | 不支持 | 对象仍是单串。 |
| 时间约束 | 不支持 | 无时钟与实时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性与 bisimulation 可判定，闭包边界清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,q_0,\sigma_0,\delta,F)$` | `FRA` 的标准定义。 |
| configuration | `$(q,\sigma,H)$` | 把控制状态、寄存器赋值和历史绑定到一起。 |
| 局部 fresh | `$a\notin \mathrm{img}(\sigma)$` | 只要求当前寄存器里没出现。 |
| 全局 fresh | `$a\notin H\cup \mathrm{img}(\sigma_0)$` | 要求整条运行历史里都没出现。 |
| 判定边界 | `emptiness decidable / universality undecidable / bisimilarity decidable` | 理论上最关键的可判定性组合。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否真的依赖“全局新名字”而不是一般 equality。
2. 再决定哪些状态下需要 known、local-fresh、global-fresh 三类转移。
3. 为少量关键名字分配寄存器，并明确何时覆写。
4. 若只需局部 fresh 而不需全局 history，应优先退回 `RA/FMA`。

### 机器可处理承载方式

机器可处理承载方式就是：

1. 有限状态集 `Q`。
2. 初始寄存器赋值 `\sigma_0`。
3. 带 `i / i• / i⊛` 标签的转移关系 `\delta`。
4. configuration graph 与 symbolic bisimulation 环境。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它与 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 的关系最直接：`FRA` 是在 `FMA/RA` 的寄存器框架上加入 global freshness。它也和 [history-register-automata/desc.md](../history-register-automata/desc.md) 的名字生成路线相邻，但 `HRA` 更强，能够维护 histories 和 reset。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是寄存器赋值、history 和 typed-span symbolic relation。
- 仿真/执行支持：可直接按 configuration 语义运行。
- 验证/分析支持：空性判定、symbolic bisimulation、与 `FMA/RA` 的互译。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：与 automata over names、nominal techniques、`π`-calculus 和 infinite-alphabet automata 理论紧密相连。

## 适用场景与需求前提

### 适用场景

适合表达 fresh name generation、动态引用创建、一次性标识符发放、session/channel 新建等“名字必须是从未出现过”的模式。

### 需求前提

1. 输入对象最好能压成线性名字串。
2. 关键语义集中在 equality 与 freshness，而不是算术或时序。
3. 真正需要记住的活动名字数量可以压成常数个寄存器。

### 不适用或高成本场景

如果需求需要 history reset、无界历史仓库、多层嵌套数据、树导航或实时间语义，则 `FRA` 往往不够；此时更合适的是 `HRA`、class-memory、tree/data automata 或 timed family。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，`FRA` 多了全局 fresh 判断；相对 [history-register-automata/desc.md](../history-register-automata/desc.md)，它还没有 histories / reset，只是在有限寄存器上加入 history-aware freshness；相对 [automata-theory-in-nominal-sets/desc.md](../automata-theory-in-nominal-sets/desc.md)，它更具体、更操作式，而 nominal automata 提供的是更抽象的对称性框架。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Data / Infinite-Alphabet` 支线从“只会记住几个旧名字”推进到“显式识别新名字生成”，这是完善演化树时很关键的一层。

### 作为目标形式主义还是中间表示

更适合作为理论母型或中间表示，而不是控制系统常规交付语言。

### 对需求到模型生成的启发

如果需求文本里不断出现“创建一个新编号”“后续不得与历史任何编号重复”“新会话必须唯一”这类语义，LLM 应优先想到 `FRA` 级别的 freshness-aware 中间模型，而不是直接退回普通 `FSM`。

### 现实限制

它的强项是形式化表达力和理论边界，而不是工程生态；原文没有给出现成工具链，因此主要服务于谱系建设与模型选择。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [history-register-automata/desc.md](../history-register-automata/desc.md)
- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)
- [automata-theory-in-nominal-sets/desc.md](../automata-theory-in-nominal-sets/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或交换格式。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树 `Finite Automata -> Data / Infinite-Alphabet` 的 freshness 子枝，并作为继续追 `register / nominal / history` 系模型的中间节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Fresh-Register Automata (FRA)`
- 论文角色：模型提出
- 核心功能：在有限寄存器自动机中显式区分 known、local-fresh 和 global-fresh 名字，从而表达 fresh-name generation。
- 关键特性：寄存器赋值、history-sensitive freshness、空性可判定、bisimilarity 可判定、非连接/非星闭包。
- 构造方式：`(Q,q_0,\sigma_0,\delta,F)` 元组加 configuration `(\sigma,H)` 语义与 symbolic typed-span 分析。
