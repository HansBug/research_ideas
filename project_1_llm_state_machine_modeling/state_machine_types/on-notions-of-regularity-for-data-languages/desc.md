# 数据语言正则性概念 / On notions of regularity for data languages

## 基本信息

- 标题：On notions of regularity for data languages
- 中文标题：数据语言正则性概念
- 作者：Henrik Björklund，Thomas Schwentick
- 发表：*Theoretical Computer Science*, 411(4-5):702-715, 2010
- DOI：`10.1016/j.tcs.2009.10.009`
- 链接：https://doi.org/10.1016/j.tcs.2009.10.009
- 形式主义：`Class-Memory Automata (CMA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 等价整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CMA=(Q,\Sigma,\delta,q_I,F_L,F_G)` 元组、class-memory function 与到 `DA` / multicounter automata 的翻译。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 global state、per-data-value local state 和记忆更新语义。

## 简报

这篇论文的核心动作，是把上一代 `Data Automata` 重新整理成更直观的 `Class-Memory Automata`。`DA` 用“全局 transducer + 每个 class 单独 NFA”来讲语义，而 `CMA` 改成“有限控制状态 + 每个数据值记住上次所处状态”的写法。结果是表达力没变，但模型本体更清楚，也第一次获得了一个真正有意义的 deterministic notion。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上，`CMA` 是 `Data Automata` 的等价重述，也是 `weak / nested CMA`、`CRA`、`HRA` 等后继模型的直接母节点。
- 构造方式简述：自动机维护一个全局状态 `q` 和一个 class-memory function `f`；读到数据值 `d` 时，先查询 `f(d)`，再据此决定转移，并把 `f(d)` 覆盖为新状态。
- 基础设施与场景简述：原文纯理论，但系统给出了与 `DA` 的等价、对 `RA` 的严格超越，以及闭包与可判定性边界。

```text
data word -> query last-state of current data value -> update global state and class memory -> local/global acceptance
```

## 形式主义定义与核心对象

### 定义对象

`CMA` 处理的是 data strings：每个位置带一个有限标签和一个无限域数据值。模型关心的不是寄存器里当前存了哪些具体值，而是“当前这个数据值上一次出现时，自动机处在哪个状态”。

### 核心抽象

原文把 `Class-Memory Automaton` 定义为：

$$
C=(Q,\Sigma,\delta,q_I,F_L,F_G)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是有限输入字母表。
3. `q_I\in Q` 是初始状态。
4. `\delta:(Q\times\Sigma\times(Q\cup\{\bot\}))\to \mathcal P(Q)` 是转移函数。
5. `F_L\subseteq Q` 是局部接受状态集。
6. `F_G\subseteq Q` 是全局接受状态集，且原文要求 `F_G\subseteq F_L`。

`CMA` 的关键对象不是普通寄存器，而是 class-memory function：

$$
f:\Delta\to Q\cup\{\bot\}
$$

上式中的符号逐项解释如下：

1. `\Delta` 是无限数据值域。
2. `f(d)` 记录数据值 `d` 上一次出现后自动机停在什么状态。
3. `\bot` 表示数据值 `d` 之前从未出现过。
4. 只有有限多个 `d` 允许满足 `f(d)\neq\bot`。

### 一个最小例子与通俗解释

一个直观例子是“每个进程 ID 的事件流都必须遵守 `request -> wait -> grant` 这类局部协议”。`CMA` 的做法不是把若干活动 ID 塞进有限寄存器，而是为每个真正出现过的 ID 记一条“最近状态便签”：

1. 读到 `(request,d)` 时，如果 `f(d)=\bot`，就把它推到 waiting 相关状态。
2. 读到 `(grant,d)` 时，只有当 `f(d)` 表示“该 ID 上次已请求未完成”才允许转移。
3. 完成这一步后，再把 `f(d)` 覆盖成新的状态。

通俗地说，`CMA` 像“每个数据值都带一张最近一次状态卡片的有限自动机”。它没有显式保留数据值之间的数值关系，只保留“这个值上次停在哪里”。

### 运行 / 接受 / 转移语义

`CMA` 的 configuration 写成：

$$
(q,f)
$$

其中 `q\in Q` 是当前全局状态，`f` 是当前 class-memory function。

若当前输入为 `(a,d)\in\Sigma\times\Delta`，则一步转移满足：

$$
(q,f)\xrightarrow{(a,d)}(q',f[d\mapsto q']) \quad \text{iff} \quad q'\in\delta(q,a,f(d))
$$

上式中的符号逐项解释如下：

1. `f(d)` 是当前数据值 `d` 的 local state。
2. `f[d\mapsto q']` 表示仅把 `d` 的 class-memory 覆盖成 `q'`。
3. 其他数据值 `d'\neq d` 的记忆保持不变。

接受条件由两部分组成：

$$
q\in F_G
$$

以及

$$
\forall d\in\Delta,\ f(d)\in F_L\cup\{\bot\}
$$

这表示：最终全局状态要落在全局接受集里，而且所有真正出现过的数据值，其最后一次状态都必须落在局部接受集里。

### 语义边界

`CMA` 的增强点是“对每个数据值记住 last state”，而不是：

1. 在寄存器中做任意值重写；
2. 对数据值做算术；
3. 显式维护多层祖先结构；
4. 给输入加时钟或连续变量。

因此它比 `DA` 更操作式，比 `RA` 更适合“每个 ID 都要独立记一份局部控制状态”的语义，但还没到 nested-data 或 history/reset 那一级。

### 关键性质与判定边界

原文的关键边界可压成：

$$
\mathrm{CMA}\equiv \mathrm{DA}
$$

$$
\mathrm{RA}\subsetneq \mathrm{CMA}
$$

$$
\mathcal L(\mathrm{CMA}) \text{ 对 } \cup,\ \cap,\ \cdot \text{ 封闭}
$$

$$
\mathcal L(\mathrm{CMA}) \text{ 不对 } \mathrm{complement},\ {}^* \text{ 封闭}
$$

$$
\mathrm{emptiness}(\mathrm{CMA}) \text{ decidable}
$$

上面几式中的符号逐项解释如下：

1. `\equiv` 表示语言表达力等价。
2. `\cdot` 表示串连接。
3. `${}^*` 表示 Kleene star。
4. `\mathrm{emptiness}` 可由到 multicounter automata 的翻译支撑。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态控制骨架。 |
| 事件 / 触发 | 强支持 | 每个 data-word 位置都会触发一次 local-state lookup 与更新。 |
| 守卫 / 数据 | 强支持 | 核心就是“当前数据值上次处于什么状态”。 |
| 层次 | 不支持 | 原始 `CMA` 只处理线性 data strings。 |
| 并发 / 同步 | 不支持 | 无显式并发组合算子。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，且与 `DA` 等价。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$C=(Q,\Sigma,\delta,q_I,F_L,F_G)$` | `CMA` 的标准定义。 |
| class memory | `$f:\Delta\to Q\cup\{\bot\}$` | 记录每个数据值的最近状态。 |
| 单步转移 | `$q'\in\delta(q,a,f(d))$` | 转移取决于当前数据值的 last state。 |
| 接受条件 | `$q\in F_G \land \forall d,\ f(d)\in F_L\cup\{\bot\}$` | 同时包含 global 与 local acceptance。 |
| 谱系结论 | `$\mathrm{CMA}\equiv\mathrm{DA}$` | `CMA` 是 `DA` 的等价但更直观的母型。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否真的是 per-data-value last-state 语义。
2. 为每个有限控制状态定义它对当前标签和 local state 的响应。
3. 明确哪些状态允许作为局部结束状态，哪些状态允许作为全局结束状态。
4. 若需求只需要有限个活动值比较，优先退回 `RA`；若需要祖先链或 nested data，转向 `NDCMA`。

### 机器可处理承载方式

机器可处理承载方式就是：

1. `C=(Q,\Sigma,\delta,q_I,F_L,F_G)` 元组；
2. class-memory function `f`；
3. 基于 `(q,f)` 的配置演化语义。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它与 [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md) 的关系最直接：两者表达力等价，但 `CMA` 更像真正的自动机本体。它又直接通向 [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md) 与 [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 class-memory function 与 `(q,f)` 配置语义。
- 仿真/执行支持：可按每步 lookup/update 规则直接解释。
- 验证/分析支持：与 `DA` 的互译、到 multicounter automata 的 emptiness reduction、deterministic notion。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是后续 `weak CMA / NDCMA / CRA / HRA` 支线的标准理论母型。

## 适用场景与需求前提

### 适用场景

适合 per-ID protocol、进程 / 会话 / 资源编号的最近状态跟踪，以及“每个数据值都应独立遵守某条局部状态规律”的对象。

### 需求前提

1. 输入可压成 data string。
2. 关键约束是当前数据值的 last-state，而不是复杂算术。
3. 每个数据值最终都要落入某个局部可接受状态。

### 不适用或高成本场景

如果需求依赖 global freshness、history reset、nested data 或 timed constraints，`CMA` 就不够；此时更适合 `FRA`、`HRA`、`NDCMA` 或 timed family。

## 与相邻形式主义的关系

相对 [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md) 中的 `DA`，`CMA` 用 last-state memory 重写了同一表达力；相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它不再只记有限个活动值，而是给每个出现过的数据值都保留一个抽象状态；相对 [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)，它还没有 registers 和 local guessing。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里的 `Data Automata` 线补成了更稳定的 `DA -> CMA` 主枝，使 `weak / nested CMA`、`CRA` 与 `HRA` 的挂接都更清晰。

### 作为目标形式主义还是中间表示

更适合作为理论母型和中间表示，而不是控制系统交付语言。

### 对需求到模型生成的启发

当需求文本里不断出现“每个 ID 上次所处阶段”“同一会话下一步必须从最近阶段续接”时，LLM 应优先考虑 `CMA` 风格，而不是一味增加普通 `FSM` 状态数。

### 现实限制

它缺少工程标准和现成生态，强项是谱系、表达力和判定边界。

## 重要的相关工作

### 奠基或前身工作

- [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)
- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)
- [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)
- [history-register-automata/desc.md](../history-register-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补到当前演化树 `Data / Infinite-Alphabet` 支线的 `Class-Memory Automata` 母节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
