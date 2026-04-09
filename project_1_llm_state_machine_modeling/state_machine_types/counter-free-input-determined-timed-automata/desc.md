# 无计数器带输入决定时间自动机 / Counter-Free Input-Determined Timed Automata

## 基本信息

- 标题：Counter-Free Input-Determined Timed Automata
- 中文标题：无计数器带输入决定时间自动机
- 作者：Fabrice Chevalier、Deepak D'Souza、Pavithra Prabhakar
- 发表：*Formal Modeling and Analysis of Timed Systems* (FORMATS 2007), pp. 82-97, 2007
- DOI：`10.1007/978-3-540-75454-1_8`
- 链接：https://www.labri.fr/perso/weil/frindien/publications/2007FormatsFChDDSPP.pdf
- 形式主义：`Counter-Free Input-Determined Timed Automata (CFCIDA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 continuous timed semantics、input-determined operators、proper symbolic alphabets、`ST-NFA` 与 counter-free 限制。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `CIDA`、proper `CIDA`、`ST-NFA`、`TFOc` 与 `rec-TFOc`。

## 简报

这篇论文的重要性在于：它不是简单说“`IDA` 很像某个 timed temporal logic”，而是把 `IDA` 中真正对应 timed first-order logic 的那一层精确切出来，并命名为 `Counter-Free Input-Determined Timed Automata`。对当前文库来说，这让 `Input-Determined Timed Automata` 不再只是一个抽象母线，而是有了一个能稳定承接 `MTL` / `MITL` / `EventClockTL` 等逻辑的清晰子节点。

- 形式主义定位：`Input-Determined Timed Automata` 母线下，对应 timed first-order / temporal logics 的 counter-free 规格子类。
- 构造方式简述：从 `CIDA` 先走到 fully canonical proper `CIDA`，再要求其底层 `ST-NFA` 是 counter-free。
- 基础设施与场景简述：原文是纯理论工作，但它把 `TFOc`、`FOc`、`ST-NFA` 和 `CFCIDA` 串成一条完整 characterisation pipeline。

```text
timed temporal / first-order logic -> TFOc -> FOc on symbolic alphabet -> counter-free ST-NFA -> CFCIDA
```

## 形式主义定义与核心对象

### 定义对象

论文以 continuous timed semantics 为主，处理的是有限 timed words 上的 input-determined automata。与上一条 `IDA` 母线相比，当前论文最关键的新增对象有三层：

1. `Continuous Input Determined Automata (CIDA)`。
2. proper / fully canonical `CIDA`。
3. 底层 `ST-NFA` 无 counter 的 `CFCIDA`。

### 核心抽象

论文首先把 `CIDA` 定义成 symbolic alphabet 上的 `ST-NFA`。可保守写成：

$$
A = (Q, s, \delta, F, \ell)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `s` 是初始状态。
3. `\delta` 是 transition relation。
4. `F` 是接受状态集。
5. `\ell` 是 state-label function；因此这里不是普通 `NFA`，而是 state-transition-labeled finite automaton。

在 timed side，论文关心的是 `CIDA` 接受的 timed language：

$$
L(A) = tw(F(A))
$$

上式中的符号逐项解释如下：

1. `F(A)` 是底层 `ST-NFA` 生成的 finitely varying functions language。
2. `tw` 把函数语言翻译成 timed-word language。

真正的 family 节点 `CFCIDA` 则是：

$$
\mathrm{CFCIDA}(\Sigma,\mathrm{Op}) = \{\, A \mid A \text{ is a fully canonical proper CIDA and its underlying ST-NFA is counter-free} \,\}
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是 timed word 字母表。
2. `\mathrm{Op}` 是 input-determined operator 集。
3. `fully canonical proper CIDA` 保证 timed side 的字母串表示是唯一且规范的。
4. `counter-free` 的限制对应 classical McNaughton-Papert 风格的 first-order fragment。

### 一个最小例子与通俗解释

论文直接给了一个很小的 `CFCIDA` 例子：在字母表 `\Sigma=\{a\}`、operator 集只有 eventual operator `\Diamond_a` 的情况下，接受“恰好一个 `a` 出现在 `[1,2]` 区间内”的 timed words。其直觉性规格可写成：

$$
\exists t \in [1,2] : a \text{ occurs at } t \quad \land \quad \text{no other } a \text{ occurs}
$$

通俗地说，`CFCIDA` 像是“把 input-determined timed automata 再收紧成没有 classical counter behavior 的那一层”。它比一般 `IDA` 更瘦，但正是这层瘦身，才让它和 first-order / temporal logic 精确对齐。

### 运行 / 接受 / 转移语义

论文的运行语义是两步式的：

1. `ST-NFA` 先接受 alternating symbolic/function representation。
2. 再由 `tw` 把它翻译成 timed words。

因此 `CFCIDA` 的 timed language 仍可写成：

$$
L(A) = tw(F(A))
$$

但其底层 symbolic machine 已经被 fully canonical + counter-free 双重限制收紧。

### 语义边界

这条 family 的边界很明确：

1. 仍然建立在 input-determined operators 之上，不退回普通 resettable `TA`。
2. 采用 counter-free 而不是 arbitrary `ST-NFA`，因此它故意只覆盖 timed first-order / temporal logic 那部分表达力。
3. 论文主要处理 continuous semantics，并顺带说明 pointwise semantics 也成立。

### 关键性质与判定边界

论文的主定理是 `TFOc` 与 `CFCIDA` 的精确对应：

$$
L \subseteq T_\Sigma^* \text{ is definable by a } \mathrm{TFO}^c(\Sigma,\mathrm{Op}) \text{ sentence} \iff L \text{ is definable by a CFCIDA over } (\Sigma,\mathrm{Op})
$$

这说明 `CFCIDA` 正是 timed first-order definable timed languages 的 automata 版本。

在证明链上，论文还先给出了一个更底层的 classical-looking 结论：

$$
\text{FOc-definable alternating finitely varying functions} \iff \text{counter-free ST-NFA-definable functions}
$$

而在递归扩展上，论文进一步说明：

$$
\text{rec-TFOc-definable timed languages} \iff \text{rec-CFCIDA-definable timed languages}
$$

所以这篇论文不只是补一个 family name，而是把 `IDA -> logic` 这条路线真正封闭起来。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍有有限控制骨架，但底层是 `ST-NFA`。 |
| 事件 / 触发 | 强支持 | 处理 timed words 上的离散动作点和间隙区间。 |
| 守卫 / 数据 | 支持时间守卫、不支持一般数据 | 仍围绕 input-determined operators。 |
| 层次 | 不支持 | 原始 family 不是层次状态机。 |
| 并发 / 同步 | 不支持 | 重点是 timed-word language 与 logic，对并发组合不展开。 |
| 时间约束 | 强支持 | continuous / pointwise 两类 timed semantics 都覆盖。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 ODE 或概率。 |
| 可执行 / 可验证性 | 强理论支持 | 与 `TFOc`、`FOc`、`MTL/MITL` 的 characterisation 是核心。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `ST-NFA` 骨架 | `$A=(Q,s,\delta,F,\ell)$` | 说明 timed side 的 automaton 实际建立在 state-transition-labeled finite automata 上。 |
| timed language | `$L(A)=tw(F(A))$` | 明确 timed language 和底层函数语言的接口。 |
| family 定义 | `$\mathrm{CFCIDA}(\Sigma,\mathrm{Op})$` | 把 fully canonical proper `CIDA` 的 counter-free 子类稳定命名。 |
| 主刻画定理 | `$\mathrm{TFO}^c \iff \mathrm{CFCIDA}$` | timed first-order logic 的 automata 等价物。 |
| 底层桥梁 | `$\mathrm{FOc} \iff \text{counter-free ST-NFA}$` | 连接 McNaughton-Papert 风格的 classical counter-free 理论。 |

## 构造方式与承载格式

### 建模入口

建模时通常遵循：

1. 先选择 input-determined operators。
2. 再构造 proper symbolic alphabet。
3. 然后将需求降到 `TFOc` 或对应 timed temporal logic。
4. 最后落成 counter-free `ST-NFA` / `CFCIDA`。

### 机器可处理承载方式

原文的承载方式是 symbolic alphabet、finitely varying functions、`ST-NFA` 和 timed first-order logic，而不是 XML / DSL。

### 交换与互操作

它与以下条目最直接互操作：

1. [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)：作为 `IDA` 母线。
2. [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)：作为被 `IDA/CFCIDA` 吸收的早期特例。
3. `MTL / MITL / EventClockTL`：论文明确把这几类 logic 拉到 `CFCIDA` 刻画下。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `ST-NFA`、symbolic alphabets、`FOc/TFOc` 翻译链。
- 仿真/执行支持：可先在 symbolic/function side 运行，再映回 timed words。
- 验证/分析支持：first-order characterisation、counter-free closure 和 periodic-word stability。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 timed automata 理论里连接 `IDA` 与 timed logics 的精细分支。

## 适用场景与需求前提

### 适用场景

适合那些需求主要以 timed temporal / first-order logic 写成，并希望得到与之精确等价的 automata family 的场景。

### 需求前提

1. 时间约束需要建立在 input-determined operators 上。
2. 目标是逻辑表达力边界，而不是一般 `TA` 工程建模。
3. 若要享受 counter-free characterization，需求应落在 first-order / counter-free 这一层。

### 不适用或高成本场景

若需求本质上依赖 general `IDA` 的更强 operator 组合、普通 `TA` 的 reset 程序化能力，或复杂并发网络，则 `CFCIDA` 过于收紧。

## 与相邻形式主义的关系

相对 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)，`CFCIDA` 是逻辑精确刻画层，而不是 `IDA` 全体；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它属于更一般 `IDA` 母线下的 logic-centered 子类；相对普通 `Timed Automata`，它牺牲了自由 reset 和一般路径依赖，换来 first-order characterisation。

## 与本研究的关系

### 对 Project 1 的价值

它让 `Input-Determined Timed Automata` 这条新支线不只停在概念抽象，而是进一步拥有一个能稳定承接 `MTL` / `MITL` / `EventClockTL` 的子节点。

### 作为目标形式主义还是中间表示

它更像 timed-specification / logic equivalence 层的中间表示，而不是最终控制器执行模型。

### 对需求到模型生成的启发

如果需求首先被抽成某种带过去/未来窗口的 timed temporal logic，那么 `CFCIDA` 提供了一个比一般 `TA` 更直接、更规范的 automata 落点。

## 重要的相关工作

1. [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)：母线 `IDA`。
2. [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)：可被纳入 `IDA/CFCIDA` 框架的早期 timed family。
3. `MTL`、`MITL`、`EventClockTL`：论文明确给出这些逻辑的 automata characterisation。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它稳定定义了 `CFCIDA` family，并给出与 `TFOc` 的精确等价。
- 它应挂在 `Input-Determined Timed Automata` 之下，作为 timed logic / first-order fragment 的规范子类。
- 它不是 DSL、工具或应用论文；其核心贡献是 family definition 与 logic-automata bridge。
