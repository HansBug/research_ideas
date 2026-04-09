# 通信层次状态机 / Communicating Hierarchical State Machines

## 基本信息

- 标题：Communicating Hierarchical State Machines
- 中文标题：通信层次状态机
- 作者：Rajeev Alur, Sampath Kannan, Mihalis Yannakakis
- 发表：*Automata, Languages and Programming*, pp. 169-178, 1999
- DOI：`10.1007/3-540-48523-6_14`
- 链接：https://doi.org/10.1007/3-540-48523-6_14
- 形式主义：`Communicating Hierarchical State Machines (CHSM / CHM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 并发扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `FSM`、product expression 与 hierarchy expression 三层递归定义，以及 associated flat `FSM` `[M]` 与语言 `L(M)`。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是递归 machine term、同步字母表和 flat-language semantics。

## 简报

这篇论文真正做的，是把“层次”和“并发”两个经典增强第一次放到同一个 automata-theory 骨架里，并且允许二者任意嵌套。它不再只是说“多个状态机并行跑”或“状态里还能装子状态机”，而是明确给出递归语法：一个 `CHM` 不是普通 `FSM`，就是若干 `CHM` 的 product，或者是一个 `FSM` 加上一组映射到下层 `CHM` 的 superstates。对层次状态机支线来说，这篇论文对应的是 `HSM` 之后最直接的并发子枝。

- 形式主义定位：`HSM` 的并发扩展，把 hierarchy 与 synchronous communication 统一成一个递归 machine family。
- 构造方式简述：模型递归地由 `base FSM`、`product expression`、`hierarchy expression` 三种构造子拼出来。
- 基础设施与场景简述：原文纯理论，但直接把 reachability、emptiness、universality、language inclusion / equivalence 与 succinctness 全部压到了一个统一分析框架里。

```text
多局部控制器 + 层次复用 -> product + hierarchy 递归组合 -> associated flat FSM -> language / equivalence / reachability analysis
```

## 形式主义定义与核心对象

### 定义对象

原文先从普通有限状态机出发，再把 concurrency 与 hierarchy 逐层叠上去。这里的 communication 不是共享变量，而是多个分量在相同字母上做同步迁移；hierarchy 则通过 superstate 展开。

### 核心抽象

原文的 base case 仍是 ordinary `FSM`：

$$
M = (Q,\Sigma,q_{in},q_f,\delta)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\Sigma` 是输入字母表。
3. `q_{in}` 是初始状态。
4. `q_f` 是终止 / 接受状态。
5. `\delta \subseteq Q \times \Sigma \times Q` 是迁移关系。

在此基础上，`CHM` 递归定义为三种形式之一：

1. base case：一个 ordinary `FSM`；
2. concurrency：

$$
M_1 \parallel M_2 \parallel \cdots \parallel M_r
$$

3. hierarchy：

$$
(N,\mathcal M,\mu)
$$

上式中的符号逐项解释如下：

1. `N` 是 top-level `FSM`。
2. `\mathcal M` 是一组下层 `CHM` 组件。
3. `\mu : Q_N \to \mathcal M` 把 top-level `FSM` 的每个状态映射到一个下层 `CHM`。

原文把没有 product expression 的子类称为 `HSM`。因此：

$$
\mathrm{HSM} \subset \mathrm{CHSM}
$$

### 一个最小例子与通俗解释

一个最小直觉例子可以是“双通道重发控制器”：

1. 顶层状态机有 `Idle`、`Try`、`Done` 三个状态。
2. `Try` 不是普通状态，而是一个层次节点，里面再展开成“发送器子机”和“确认子机”并行执行。
3. 两个子机在共享字母 `ack`、`timeout` 上同步。

通俗地说，`CHSM` 像“把多个层次状态机装进一个同步积木盒”。如果 `HSM` 只是“状态里再套一台状态机”，`CHSM` 则进一步允许“几个这样的层次盒子并排跑，并在共同事件上同时迈步”。

### 运行 / 接受 / 转移语义

原文通过 associated flat `FSM` `[M]` 来给出语义。其核心思想是：

1. 对 hierarchy expression，递归用对应组件替换 superstate。
2. 对 product expression，把局部分量做同步 product。
3. 最终得到一个 ordinary `FSM` `[M]`。

因此语言语义直接定义为：

$$
L(M) = L([M])
$$

这里的符号逐项解释如下：

1. `M` 是原始 `CHM`。
2. `[M]` 是把 hierarchy / concurrency 全部展开后的 flat `FSM`。
3. `L([M])` 是 ordinary `FSM` 接受的 regular language。

这一定义也说明：`CHSM` 本体不是为了超越 regular languages，而是为了在保持 regular-language semantics 的同时获得更紧凑的结构表达。

### 语义边界

`CHSM` 的边界很清楚：

1. 仍是纯离散、纯有限控制模型。
2. hierarchy 与 concurrency 都是结构增强，不引入栈、时间或连续变量。
3. communication 依赖同步字母，而不是共享变量。
4. 它强调 succinctness 与 complexity trade-off，而不是工程可执行语义细节。

### 关键性质与判定边界

原文关心的核心问题是：加入 hierarchy 与 concurrency 后，哪些问题会变得多难。代表性结论可以压成：

$$
\mathrm{Reachability}(\mathrm{HSM}) \text{ is } P\text{-complete}
$$

而对带并发的 `CHSM`：

$$
\mathrm{Reachability}(\mathrm{CHSM}) \text{ is } PSPACE\text{-complete}
$$

对语言问题，原文进一步表明：

$$
\mathrm{Universality}(\mathrm{HSM}),\ \mathrm{Inclusion}(\mathrm{HSM}),\ \mathrm{Equivalence}(\mathrm{HSM})
$$

都已经进入高复杂度区间，而对一般 `CHSM` 还会继续上升。也就是说，hierarchy 本身不一定“昂贵”，但 hierarchy 与 concurrency 叠加后，analysis cost 会显著变重。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | ordinary states + superstates 都是一等对象。 |
| 事件 / 触发 | 强支持 | 以同步字母为核心。 |
| 守卫 / 数据 | 不支持 | 原文仍是纯状态 / 字母模型。 |
| 层次 | 强支持 | hierarchy expression 是核心构造子。 |
| 并发 / 同步 | 强支持 | product expression 显式建模并发同步。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 直接面向 reachability、universality、equivalence、succinctness。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| base FSM | `$M=(Q,\Sigma,q_{in},q_f,\delta)$` | 普通母型。 |
| 并发组合 | `$M_1 \parallel \cdots \parallel M_r$` | communication branch 的核心构造。 |
| 层次组合 | `$(N,\mathcal M,\mu)$` | superstate expansion 的核心构造。 |
| flat semantics | `$L(M)=L([M])$` | 所有复杂结构都落到 associated flat `FSM`。 |
| 子类关系 | `$\mathrm{HSM}\subset\mathrm{CHSM}$` | sequential hierarchical line 是并发线的子类。 |

## 构造方式与承载格式

### 建模入口

1. 先决定局部控制器是 ordinary `FSM` 还是层次节点。
2. 若几个局部控制器需要在共享事件上同步，则用 product expression。
3. 若某个局部状态需要进一步细化，则用 hierarchy expression。
4. 最终递归组合出一个 `CHM` 项。

### 机器可处理承载方式

机器可处理承载方式主要就是：

1. ordinary `FSM`；
2. `\parallel` product；
3. hierarchy triple `(N,\mathcal M,\mu)`；
4. associated flat `FSM` `[M]`。

### 交换与互操作

这篇论文没有工程交换格式，但在谱系上很关键：

1. 它把 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 sequential hierarchy 推到 concurrency。
2. 它为后续“层次 + richer semantics”路线提供了可对照的 complexity baseline。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive machine syntax 与 associated flat expansion。
- 仿真/执行支持：可经 `[M]` 解释为 ordinary `FSM`。
- 验证/分析支持：reachability、emptiness、universality、equivalence、succinctness 全部覆盖。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：主要服务于层次 / 并发 state-machine theory，而不是工程标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 有多个局部控制器并行同步的离散系统。
2. 同时需要 hierarchy 与 concurrency 的 succinct formal model。
3. 关注 language / equivalence / complexity 的理论问题。

### 需求前提

1. 交互可压成有限同步字母表。
2. 并发分量数量有限。
3. 不需要共享变量、时间或连续语义。

### 不适用或高成本场景

如果需求核心是作用域变量、history、group transition 或黑盒 mode semantics，则 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md) 更合适；如果需求核心是 recursion / call-return，则 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 更贴切。

## 与相邻形式主义的关系

相对 `HSM`，`CHSM` 增加了并发同步 product；相对 `Statecharts`，它保留了 hierarchy / concurrency 两个经典增强，但把语义压成更干净的 automata-theory 骨架；相对 `HRM`，它没有变量作用域与 history 语义；相对 `RSM`，它没有递归调用栈。

## 与本研究的关系

### 对 Project 1 的价值

它说明“层次状态机”并不是只有 DSL 路线，也存在明确的 automata-theory 并发分支，这对后续演化树非常关键。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和理论中间表示，而不是控制系统直接交付工件。

### 对需求到模型生成的启发

当需求同时出现“层次子模式 + 多局部控制器同步”时，LLM 不应只在 flat `FSM` 或单机 `HSM` 之间选，而要意识到 `CHSM` 这类 product-based hierarchical family 的存在。

### 现实限制

语言问题复杂度很高，也缺少工程标准化载体，因此在工程上往往会被 UML / synchronous DSL / tool-specific language 替代。

## 重要的相关工作

### 奠基或前身工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)
- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)

### 同类型或同家族工作

- [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)：走 semantic mode / shared-variable 路线的层次模型。
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：走 recursion / call-return 路线的层次模型。

## 文献分类总结

- 这篇论文对应层次状态机支线里最经典的“并发扩展”节点。
- 它主体讨论的是模型家族与复杂度，不是 DSL、标准或应用案例。
- 在当前演化树里，它最适合作为 `HSM` 下面的 `CHSM` 子枝。
