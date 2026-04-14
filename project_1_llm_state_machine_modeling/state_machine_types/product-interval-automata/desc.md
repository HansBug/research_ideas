# 乘积区间自动机 / Product Interval Automata

## 基本信息

- 标题：Product Interval Automata
- 中文标题：乘积区间自动机
- 作者：Deepak D'Souza、P. S. Thiagarajan
- 发表：*Sadhana*, 27(2):181-208, 2002
- DOI：`10.1007/BF02717183`
- 链接：https://www.csa.iisc.ac.in/~deepakd/papers/sadhana.ps
- 形式主义：`Product Interval Automata (PIA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 distributed alphabet、每 agent 一只 clock 的局部 interval automaton，以及全局 run 的前缀语义。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `({A_i}_{i \in P}, Q_{in})` 结构、局部区间迁移和由共享动作分布决定的 clock read/reset discipline。

## 简报

这篇论文在 `Timed Automata` 主干里切出了一条很“克制但好用”的分支：不再让全局自动机自由读写任意 clocks，而是把系统拆成一组 timed agents，并规定**每个 agent 只有一只 clock**，且某个共享动作只允许读取和重置参与该动作的那些 agent 的 clocks。这个约束让模型比一般 `TA` 弱，但换来了布尔闭包、逻辑刻画和更清晰的分布式结构，非常适合拿来扩演化树中的“结构化 timed-network”支线。

- 形式主义定位：`Timed Automata` 的分布式、单局部时钟、结构化子类。
- 构造方式简述：把全局 timed behavior 写成若干 interval automata 的乘积；动作分布 `\Sigma = \{\Sigma_i\}` 决定哪些局部 clock 会被读写。
- 基础设施与场景简述：核心基础设施是 language-theoretic closure、`TMSO/TLTL` 式逻辑刻画和 asynchronous circuit 建模能力，而不是工程执行器。

```text
distributed timed agents -> one clock per agent -> shared-action-determined clock usage -> product interval automaton -> boolean closure / logic characterization
```

## 形式主义定义与核心对象

### 定义对象

原文把对象看成“若干 timed agents 在共享动作上同步”的 timed behavior。和普通 `TA` 相比，它不是一张全局图随意读写 clocks，而是先给出分布式 alphabet，再由 alphabet 的分布规则约束每只 clock 的使用方式。

### 核心抽象

`PIA` 的正式定义是：

$$
A = (\{A_i\}_{i \in P}, Q_{in})
$$

上式中的符号逐项解释如下：

1. `P` 是 agents 的索引集。
2. `A_i` 是第 `i` 个局部 interval automaton。
3. `Q_{in} \subseteq Q_1 \times \cdots \times Q_{|P|}` 是全局初始状态集合。

每个局部 automaton 写成：

$$
A_i = (Q_i, \to_i, F_i, G_i)
$$

上式中的符号逐项解释如下：

1. `Q_i` 是第 `i` 个 agent 的有限状态集。
2. `\to_i \subseteq Q_i \times (\Sigma_i \times \mathcal I_{\mathbb R}) \times Q_i` 是带区间标注的局部迁移关系。
3. `F_i`、`G_i` 分别是有限运行和无限运行下的接受状态集合。

这里最关键的 collection 级约束是：每个 agent 只有一只局部 clock，而某个共享动作 `a` 只读取、重置那些满足 `a \in \Sigma_i` 的 clocks。

### 一个最小例子与通俗解释

最小直觉例子是两个 agent：

1. `A_1` 参与动作 `a` 和 `b`。
2. `A_2` 只参与动作 `b`。

于是：

1. 执行 `a` 时，只会检查和重置 `A_1` 的 clock。
2. 执行共享动作 `b` 时，会同时检查和重置 `A_1`、`A_2` 的 clocks。

通俗地说，`PIA` 像“带显式局部计时器的同步产品”。普通 `TA` 像一块能随意碰所有 clocks 的总控面板；`PIA` 则先把系统拆成模块，再规定“哪个动作能碰哪些时钟”完全由参与者集合决定。

### 运行 / 接受 / 转移语义

对 timed word `\sigma`，原文把 run 定义成前缀到全局状态的映射：

$$
p : \mathrm{prf}(\sigma) \to Q
$$

并要求：

$$
p(\varepsilon) \in Q_{in}
$$

若当前前缀为 `r`，下一步事件是 `(a,t)`，则对每个参与者 `i \in loc(a)` 必须存在局部迁移

$$
p(r)[i] \xrightarrow{(a,I_i)} p(r(a,t))[i]
$$

且满足：

$$
t - time_i(r) \in I_i
$$

对每个不参与 `a` 的 agent `i \notin loc(a)`，则保持：

$$
p(r)[i] = p(r(a,t))[i]
$$

这正是 `PIA` 的核心语义边界：shared action 决定哪些局部 clock 被真正访问。

### 语义边界

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的一般 `Timed Automata`，`PIA` 更弱，因为它禁止任意 clock read/reset；但也正因如此，它保住了更稳的语言论性质和更清晰的模块化结构。

### 关键性质与判定边界

论文的核心结论之一可压缩成：

$$
L \text{ is accepted by a PIA } \iff L \text{ is a regular product interval language}
$$

同时，作者给出了布尔闭包结果：

$$
\text{regular product interval languages are closed under } \cup,\ \cap,\ \complement
$$

并进一步证明 `PIA` 具有 `TMSO` / `TLTL` 风格的逻辑刻画，还能表达 asynchronous digital circuits 的 timed behavior。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个 agent 有局部有限状态，系统是它们的同步乘积。 |
| 事件 / 触发 | 强支持 | 共享动作是同步点，局部动作只影响相关 agent。 |
| 守卫 / 数据 | 支持时间守卫 | 守卫体现为动作上的实数区间约束。 |
| 层次 | 不支持 | 原始模型不是层次状态机。 |
| 并发 / 同步 | 强支持 | 分布式 agent 同步正是模型核心。 |
| 时间约束 | 强支持 | 每个 agent 有局部 clock，动作约束由时间区间表达。 |
| 连续动态 / 随机性 | 不支持 | 没有 ODE、概率或一般 hybrid flow。 |
| 可执行 / 可验证性 | 强理论支持 | 布尔闭包、逻辑刻画和 language inclusion 均稳定。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 顶层模型 | `$A = (\{A_i\}_{i \in P}, Q_{in})$` | `PIA` 的分布式 timed skeleton。 |
| 局部模型 | `$A_i = (Q_i,\to_i,F_i,G_i)$` | 每个 agent 只有自己的状态与区间边。 |
| run 语义 | `$p : \mathrm{prf}(\sigma) \to Q$` | 用 timed-word 前缀驱动全局同步运行。 |
| 参与动作约束 | `$t - time_i(r) \in I_i$` | 只有参与动作的局部 clocks 会被检查。 |
| 核心结论 | `PIA \iff regular product interval languages` | 说明该 family 不是 ad hoc 子类，而是稳定语言类。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. 系统可以拆成哪些 timed agents。
2. 每个 agent 的局部动作集 `\Sigma_i` 是什么。
3. 哪些动作需要同步共享，哪些是纯局部动作。
4. 每个共享动作应该约束哪些 agent 的局部等待时间。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. 分布式 alphabet。
2. 局部 interval automata。
3. 全局初始状态集合 `Q_{in}`。

### 交换与互操作

它与 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 `Timed Automata` 母线直接相关，也与 timed CSP / timed Petri-style distributed semantics 有自然邻接，但本文真正稳定给出的主骨架仍是“distributed timed-agent product”。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是局部 automata 乘积、distributed alphabet 和 logical characterization。
- 仿真/执行支持：可直接按 timed word 的前缀语义执行。
- 验证/分析支持：布尔闭包、language inclusion、`TMSO/TLTL` 风格逻辑刻画。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `Timed Automata` 家族中偏 language-theoretic 的结构化分布式支线。

## 适用场景与需求前提

### 适用场景

适合异步数字电路、分布式 timed agents、共享动作同步系统，以及那些希望用模块化方式表达局部等待约束的 timed specification。

### 需求前提

1. 系统应能自然拆成少量局部 agent。
2. 每个 agent 的时间记忆最好可以压缩成“一只局部 clock”。
3. 动作参与者集合必须是稳定、可显式枚举的。

### 不适用或高成本场景

若需求需要任意 clocks 的交叉读取、复杂 reset 模式或一般 dense-time 程序控制流，普通 `TA` 更自然。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`PIA` 牺牲了自由时钟操作，换来分布式结构化和布尔闭包；相对一般 timed circuit / application 条目，它不是案例建模，而是一个明确命名、可逻辑刻画的 timed family。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Timed Automata` 主干补成一条此前还比较空的“结构化分布式 timed family”支线，不再只是在 event-clock / pushdown / parametric 这些语义方向长枝。

### 作为目标形式主义还是中间表示

更适合作为理论选型节点或某些模块化实时控制需求的中间表示，而不是通用工程交付格式。

### 对需求到模型生成的启发

如果需求文本本身已经按“若干 agent + 共享动作 + 局部等待时间”组织，LLM 生成 `PIA` 会比直接生成扁平 `TA` 更自然，也更利于后续做结构化验证。

### 现实限制

它的 clock discipline 很强，表达力明显弱于一般 `TA`；只有在模块边界和同步参与者确实稳定时才值得使用。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- 论文中明确将其看作一般 `Timed Automata` 的受限子类，而不是独立脱离 timed-automata 主线的新总线。

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”是 product-language 和 logical-characterization 结果。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Timed Automata -> Product Interval Automata` 的结构化 timed-network 节点。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Product Interval Automata (PIA)`
- 论文角色：模型提出
- 核心功能：把分布式 timed agents 压成“一 agent 一只 clock、共享动作决定时钟使用”的结构化时间自动机子类。
- 关键特性：distributed alphabet、one clock per agent、boolean closure、logical characterization、asynchronous-circuit expressiveness。
- 构造方式：`A = (\{A_i\}_{i \in P}, Q_{in})` + 局部 interval automata。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：异步数字电路、分布式 timed agents、模块化实时规格。
- 需求前提：系统可按 agents 拆分，且动作参与者集合稳定可枚举。
- 状态：🟢
