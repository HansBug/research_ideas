# 终将时间自动机 / Eventual Timed Automata

## 基本信息

- 标题：Eventual Timed Automata
- 中文标题：终将时间自动机
- 作者：Deepak D'Souza、Raj Mohan M
- 发表：*FSTTCS 2005: Foundations of Software Technology and Theoretical Computer Science*, pp. 322-334, 2005
- DOI：`10.1007/11590156_26`
- 链接：https://www.csa.iisc.ac.in/~deepakd/papers/eta.ps
- 形式主义：`Eventual Timed Automata (ETA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `O_a / O_B` 这类 input-determined operators、recursive ETA 的分层定义，以及到 non-recursive `ETA` / 1-clock alternating timed automata 的归约。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `A = (Q,s,\delta,F)` 结构、operator guards 和 recursive floating automata。

## 简报

这篇论文把 `Input-Determined Timed Automata` 主线再往前推进了一条很重要的语义支线：不再用自由 reset 的 clocks，而是直接用“未来某类事件会在多远处出现”这样的 operator 作为 guards。`ETA` 的核心不是更复杂的控制状态，而是 `O_a` 和 `O_B` 这类**由输入 timed word 自身决定**的 future-distance operators。论文证明，这个 family 虽然比普通 `TA` 更偏规格语言，但仍然可判定，而且 recursive 版本可以通过 flattening + 1-clock alternating timed automata 化归。

- 形式主义定位：`Input-Determined Timed Automata` 下面的 future-distance / eventuality 支线。
- 构造方式简述：用 `O_a` 表示“未来某个 `a` 距当前有多远”，再允许用 floating automata 递归定义 `O_B`。
- 基础设施与场景简述：核心基础设施是 flattening、1-clock ATA reduction、`MTL` 关联和 expressive incomparability analysis。

```text
input-determined operators -> future-distance guard O_a -> recursive operator O_B -> ETA -> flattening -> 1-clock alternating timed automata
```

## 形式主义定义与核心对象

### 定义对象

`ETA` 面向的是 timed words 上的 eventuality-style specification。它关心的不是“自动机何时 reset 一只 clock”，而是“在当前时刻往未来看，多远处会出现某类事件或某个被 automaton 识别的情形”。

### 核心抽象

基础 `ETA` 写成：

$$
A = (Q,s,\delta,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `s \in Q` 是起始状态。
3. `\delta \subseteq Q \times \Sigma \times G(\Sigma) \times Q` 是带 guards 的迁移关系。
4. `F \subseteq Q` 是接受状态集。

它最关键的原子 operator 是 `O_a`，其语义可以保守写成：

$$
[O_a](\sigma,i) = \{\tau(j)-\tau(i) \mid j \ge i,\ w(j)=a\}
$$

上式中的符号逐项解释如下：

1. `\sigma = (w,\tau)` 是 timed word。
2. `i` 是当前观察位置。
3. `w(j)=a` 表示未来位置 `j` 上的事件标签是 `a`。
4. `\tau(j)-\tau(i)` 是从当前位置到未来这个 `a` 的时间距离。

若 guard 写成 `O_a \in I`，含义就是“存在某个未来 `a`，其时间距离落在区间 `I` 内”。

### 一个最小例子与通俗解释

论文一开始给出的直觉例子是：所有 `a` 组成的 timed word 中，不允许出现两次 `a` 的时间差恰好为 `1`。这时只需要一个状态，并在读到每个 `a` 时检查：

$$
\neg (O_a \in [1,1])
$$

通俗地说，`ETA` 像“把 eventually 谓词直接做成时间自动机边上的原子观察器”。普通 `TA` 需要自己设计 reset 和比较；`ETA` 则直接问“未来某种事会不会在某个时间窗内发生”。

### 运行 / 接受 / 转移语义

若输入 timed word 是

$$
\sigma = (a_0,t_0)\cdots(a_n,t_n)
$$

则一条 run 是状态序列

$$
q_0 q_1 \cdots q_{n+1}
$$

并满足：

$$
q_0 = s
$$

且对每个位置 `i` 都存在 guard `g_i` 使得

$$
(q_i,a_i,g_i,q_{i+1}) \in \delta,\qquad \sigma,i \models g_i
$$

最终接受条件是：

$$
q_{n+1} \in F
$$

### 语义边界

相对 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md) 的一般 `IDA`，`ETA` 是以 eventuality operator 为核心的特化 family；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它不再把 future constraint 编成固定 event clocks，而是直接用 operator 读未来距离集合。

### 关键性质与判定边界

递归版本通过 floating automata 定义 `O_B`：

$$
[O_B](\sigma,i) = \{\tau(j)-\tau(i) \mid j \ge i,\ (\sigma,j) \in L^f(B)\}
$$

论文的主结论是：recursive `ETA` 可先 flatten 成 non-recursive `ETA`，再归约到 1-clock alternating timed automata，因此 emptiness 可判。可压缩为：

$$
\text{Recursive ETA emptiness is decidable}
$$

此外，原文还给出两个很重要的语义边界：

$$
\text{Recursive ETA and Alur-Dill timed automata are incomparable in expressive power}
$$

以及：

$$
\text{the dual eventuality operator alone is decidable, but combining both duals becomes undecidable}
$$

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍保留有限状态骨架。 |
| 事件 / 触发 | 强支持 | 迁移由输入事件驱动，并结合 future-distance guards。 |
| 守卫 / 数据 | 强支持时间守卫 | 守卫来自 `O_a / O_B` 这类 input-determined operators。 |
| 层次 | 部分支持 | 不是 Harel 层次，但 recursive ETA 有 operator-level 分层。 |
| 并发 / 同步 | 不支持 | 原始模型针对单条 timed word 语言。 |
| 时间约束 | 强支持 | future eventuality 就是模型核心。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | flattening、1-clock ATA reduction 和 expressive-boundary 都明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础模型 | `$A=(Q,s,\delta,F)$` | `ETA` 的有限状态骨架。 |
| 基础 operator | `$[O_a](\sigma,i)=\{\tau(j)-\tau(i)\mid j\ge i,\ w(j)=a\}$` | future-event distance 的语义核心。 |
| 递归 operator | `$[O_B](\sigma,i)=\{\tau(j)-\tau(i)\mid (\sigma,j)\in L^f(B)\}$` | 允许用 automata 自己定义更高阶 eventuality。 |
| 可判定性 | `recursive ETA -> flattening -> 1-clock ATA` | 说明 recursive family 仍可做 emptiness decision。 |
| 表达边界 | `ETA \nsubseteq TA` 且 `TA \nsubseteq ETA` | 不是简单的 TA 子类或父类。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. 需求里哪些 future-time constraints 最核心。
2. 这些约束能否直接用 `O_a` 表示，还是要引入 floating automata 定义 `O_B`。
3. 需要的是 pointwise eventuality，还是更一般的 recursive operator。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. 带 operator guards 的有限自动机。
2. floating timed words / floating automata。
3. flattening 后的扩展字母表与 1-clock ATA reduction。

### 交换与互操作

它与 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md) 的 `IDA` 母线、[counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md) 的逻辑片段子类，以及 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md) 的可确定化 timed specification 分支都有直接关系。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 operator semantics、floating automata 和 flattening construction。
- 仿真/执行支持：可按 timed word 逐位置解释 guards。
- 验证/分析支持：decidable emptiness、flattening、1-clock ATA reduction、expressiveness comparison。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 input-determined timed-specification family 的经典语义分支。

## 适用场景与需求前提

### 适用场景

适合那些直接以“未来某类事件将在若干时间单位内/外出现”来陈述的 timed specification，以及 `MTL` / timed logic 与 automata 之间的桥接研究。

### 需求前提

1. 时间约束最好来自输入 timed word 本身，而非自由 reset 的局部程序时钟。
2. 需求更像语言规格或逻辑性质，而不是工程执行控制器。
3. 若要使用 recursive ETA，需接受 floating automata 作为 operator 定义载体。

### 不适用或高成本场景

若需求主要是工程化实时控制、复杂同步网络或一般 reset-based local timing，普通 `TA` 更自然。

## 与相邻形式主义的关系

相对 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)，这是一条更具体的 eventuality operator 子线；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它更偏 operator semantics 而非固定 event clocks；相对 [on-continuous-timed-automata-with-input-determined-guards/desc.md](../on-continuous-timed-automata-with-input-determined-guards/desc.md)，它还是 pointwise 事件点语义，不是 continuous branch。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Input-Determined Timed Automata` 补成一条此前明确待补的 `eventual` 语义支线，让演化树不再只停留在 pointwise / continuous / counter-free 这几个已有节点。

### 作为目标形式主义还是中间表示

更适合作为逻辑规格导向的目标形式主义或中间表示，而不是直接执行的控制器模型。

### 对需求到模型生成的启发

当自然语言需求反复出现“最终在某个时间窗内会发生某事”时，LLM 先生成 `ETA` 式 operator guards，往往比直接选一般 `TA` 更贴近原始语义。

### 现实限制

它更偏 timed-language / logic family，工程工具链远不如 `UPPAAL` 生态成熟。

## 重要的相关工作

### 奠基或前身工作

- [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)

### 同类型或同家族工作

- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)
- [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)
- [on-continuous-timed-automata-with-input-determined-guards/desc.md](../on-continuous-timed-automata-with-input-determined-guards/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”是 flattening 和 1-clock ATA reduction。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Input-Determined Timed Automata -> Eventual Timed Automata`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Eventual Timed Automata (ETA)`
- 论文角色：模型提出
- 核心功能：用 future-distance operators 直接表达 timed-word 上的 eventuality specification。
- 关键特性：`O_a / O_B` operators、recursive floating automata、flattening、1-clock ATA reduction、与 `TA` 表达力不可比。
- 构造方式：`A=(Q,s,\delta,F)` + operator guards。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：future-time specification、`MTL` 关联、timed logic 到 automata 的落点分析。
- 需求前提：约束主要由输入 timed word 自身决定，且目标偏规格而非执行。
- 状态：🟢
