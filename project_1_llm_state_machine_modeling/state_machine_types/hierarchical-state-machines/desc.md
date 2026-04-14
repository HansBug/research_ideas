# 层次状态机 / Hierarchical State Machines

## 基本信息

- 标题：Hierarchical State Machines
- 中文标题：层次状态机
- 作者：Mihalis Yannakakis
- 发表：*Theoretical Computer Science: Exploring New Frontiers of Theoretical Informatics*, pp. 315-330, 2000
- DOI：`10.1007/3-540-44929-9_24`
- 链接：https://doi.org/10.1007/3-540-44929-9_24
- 形式主义：`Hierarchical State Machines (HSM)`，并系统回顾其并发扩展 `CHM / CHSM`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：家族综述 / 主干梳理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 base `FSM`、层次三元组 `(N,\mathcal M,\mu)`、flattening 规则、`CHM` 的 product / hierarchy 递归构造，以及 emptiness / universality / equivalence / model checking 等标准判定问题。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 rooted-DAG 层次表示、associated flat `FSM` 与 temporal-logic / automata-theoretic 语义。

## 简报

这篇文章不是再发明一个新 DSL，而是把 `Statecharts` 之后已经分化出的 classic hierarchical-state-machine 理论线做了一次很干净的总梳理。作者把 `HSM` 视为“状态本身还能展开成其他状态机”的有限状态机家族，围绕它回答了三类最关键的问题：它和普通 `FSM` 相比到底增益了什么；determinism / nondeterminism、single-entry / multiple-entry、single-exit / multiple-exit 这些变体如何改变复杂度；以及 hierarchy 和 concurrency 叠加后为何会自然长出 `CHM` 这条分支。

- 形式主义定位：`Statecharts` 理论化之后的层次状态机母线综述条目，用于把 `HSM -> CHM` 的主干结构说清楚。
- 构造方式简述：先从 ordinary `FSM` 出发，再递归定义 `HSM=(N,\mathcal M,\mu)`；若再加入并发组合子 `M_1 \parallel \cdots \parallel M_r`，则得到 `CHM`。
- 基础设施与场景简述：纯理论论文，没有工程标准，但非常适合作为状态机族演化树里 `HSM` 支线的“挂接说明”来源，因为它集中讨论了 hierarchy、共享子机、succinctness 与 model-checking 边界。

```text
Statecharts 风格层次控制 -> HSM 递归定义 / flatten 语义 -> 复杂度与表达力边界 -> HSM / CHM 家族分支
```

## 形式主义定义与核心对象

### 定义对象

原文把 `HSM` 直接定义成“状态可以展开成其他状态机的有限状态机”，并明确区分：

1. 纯层次的 sequential `HSM`；
2. 叠加并发后的 `CHM / CHSM`；
3. 单入口/单出口与多入口/多出口两类接口骨架。

### 核心抽象

文中先从 ordinary `FSM` 出发：

$$
M = (Q,\Sigma,q_0,F,E)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\Sigma` 是输入字母表。
3. `q_0 \in Q` 是初始状态。
4. `F \subseteq Q` 是终止或接受状态集合。
5. `E \subseteq Q \times \Sigma \times Q` 是迁移关系。

在 single-entry / single-exit 情况下，原文把 `HSM` 递归写成：

$$
H = (N,\mathcal M,\mu)
$$

上式中的符号逐项解释如下：

1. `N` 是 top-level `FSM`。
2. `\mathcal M` 是一组先前已经定义好的 `HSM` 子机。
3. `\mu : Q_N \to \mathcal M` 把 `N` 的某个状态映射到一个下层 `HSM`，表示该状态会展开成子机。

并发扩展 `CHM` 则在此基础上加入：

$$
M_1 \parallel M_2 \parallel \cdots \parallel M_r
$$

这里的 `\parallel` 表示多个分量在共享字母上同步推进的 product expression。

### 一个最小例子与通俗解释

原文反复使用的直觉例子是 digital clock。顶层只放 `24` 个“小时”盒子；每个小时盒子复用同一个“分钟循环”子机；分钟子机再复用同一个“秒循环”子机。这样：

1. 大结构只描述“小时 -> 分钟 -> 秒”三层模式。
2. 不需要把 `24 × 60 × 60` 个平铺状态全部逐个写出来。
3. 多个上层状态还可以共享同一个下层子机定义。

通俗地说，`HSM` 就像“一个状态里还能装下一本子流程手册的状态机”。普通 `FSM` 只能把所有控制点平铺成一张大图；`HSM` 允许你说“进入这个大状态后，再按另一台局部状态机继续跑”。这不会改变它识别 regular language 的本质，但会极大压缩表示体积。

### 运行 / 接受 / 转移语义

原文把 `HSM` 的语义统一落到对应的 flat machine `flat(H)`。可以写成：

$$
L(H) = L(\mathrm{flat}(H))
$$

上式中的符号逐项解释如下：

1. `H` 是原始层次状态机。
2. `\mathrm{flat}(H)` 是把所有层次结构递归展开后的 ordinary `FSM`。
3. `L(\cdot)` 表示该机器接受的语言。

对 `CHM`，语言语义同样是：

$$
L(H) = L(\mathrm{flat}(H))
$$

但这里的 `\mathrm{flat}(H)` 还需要同时展开 hierarchy 与 concurrency。

### 语义边界

这篇文章对家族边界讲得很清楚：

1. `HSM` 不增加语言表达力，仍然只对应 regular languages。
2. hierarchy 带来的主要收益是 succinctness，而不是超出 regular 的识别能力。
3. 一旦允许 recursion，就会走向 `RSM / pushdown` 线，这已经超出本文主线。
4. 一旦把 hierarchy 与 concurrency 任意交错，就会形成 `CHM`，复杂度明显上升。

### 关键性质与判定边界

文中的几个代表性结论非常适合写进演化树说明：

$$
\mathrm{Emptiness}(\mathrm{HSM}) \in P,\quad \mathrm{Universality}(\mathrm{HSM}) \text{ is EXPSPACE-complete}
$$

这说明 hierarchy 对 emptiness 很“便宜”，但对 universality 非常“昂贵”。

对 deterministic / nondeterministic 的 succinctness，原文强调：

$$
\text{nondeterministic HSM} \to \text{deterministic HSM}
$$

在最坏情况下会产生 doubly exponential blow-up。

对 `LTL/CTL`，文中给出保层次分析结论：

$$
\mathrm{MC}_{LTL}(H,\varphi) = O(|H| \cdot 4^{|\varphi|})
$$

以及

$$
\mathrm{MC}_{CTL}(H,\varphi) = O(|H| \cdot 2^{|\varphi| d})
$$

上式中的 `d` 是每个子机允许的出口数上界。它说明 single-exit 情况明显更友好，而 multiple-exit 会把 `CTL` 复杂度推高。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 普通状态与 superstate / box 是核心。 |
| 事件 / 触发 | 支持 | 通过字母标注迁移表达。 |
| 守卫 / 数据 | 不支持 | 本文主线不引入变量。 |
| 层次 | 强支持 | `HSM` 的定义中心。 |
| 并发 / 同步 | 部分支持 | 通过 `CHM` 分支支持。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | emptiness、universality、equivalence、`LTL/CTL` 全部讨论。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| ordinary `FSM` | `$M=(Q,\Sigma,q_0,F,E)$` | 层次扩展之前的母型。 |
| `HSM` 递归三元组 | `$H=(N,\mathcal M,\mu)$` | sequential hierarchy 的基本骨架。 |
| 并发组合 | `$M_1 \parallel \cdots \parallel M_r$` | `CHM` 的并发构造子。 |
| flat 语义 | `$L(H)=L(\mathrm{flat}(H))$` | 层次结构最终回落到 ordinary `FSM` 语义。 |
| `CTL` 复杂度 | `$\mathrm{MC}_{CTL}(H,\varphi)=O(|H|\cdot 2^{|\varphi|d})$` | 多出口直接影响复杂度上界。 |

## 构造方式与承载格式

### 建模入口

1. 先写一个 top-level `FSM`。
2. 再识别哪些状态应折叠成可复用子机。
3. 需要并发时，再把若干子机用同步 product 组合成 `CHM`。
4. 最后由 flatten 规则给出统一语义。

### 机器可处理承载方式

原文中的可处理对象主要是：

1. rooted DAG 的层次表示；
2. `FSM` + `HSM` 递归三元组；
3. `CHM` 的 product / hierarchy expression；
4. associated flat machine 与 language semantics。

### 交换与互操作

原文没有工程交换格式，但在谱系上非常关键：

1. 它把 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的奠基结果整理成稳定母线。
2. 它把 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md) 明确成 `HSM` 的并发分支。
3. 它为后续 `HRM`、`RSM`、`CDHSM/SHSM` 等子线提供统一上位语境。

## 配套基础设施

- 建模/编辑工具：原文只列举 `Statecharts`、`STATEMATE`、`UML` 等背景语境，未提供实现。
- 解析/交换/元模型支持：核心是 rooted-DAG 层次表示与 flatten 语义。
- 仿真/执行支持：可通过 associated flat `FSM` 执行。
- 验证/分析支持：emptiness、universality、intersection、equivalence、`LTL/CTL`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：这是一篇理论梳理文，不是标准条目，但对文库里的层次状态机主干命名具有“校准口径”的作用。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要把大控制器压成层次化局部子机的离散系统。
2. 需要分析 hierarchy 带来的 succinctness 与复杂度边界。
3. 需要给 `Statecharts` 之后的理论谱系找一个清晰母节点。

### 需求前提

1. 系统本质仍是有限离散控制。
2. hierarchy 主要体现为子机复用与结构压缩。
3. 若走 `CHM` 路线，并发交互需可压成共享字母同步。

### 不适用或高成本场景

如果需求已经出现无界递归调用，应转向 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)；如果核心是变量作用域、history 与 mode black-box 语义，则 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md) 更贴切。

## 与相邻形式主义的关系

相对 plain `FSM`，`HSM` 增加 hierarchy；相对 `CHSM`，`HSM` 没有并发同步；相对 `RSM`，`HSM` 没有无界 call-return 递归；相对 `HRM`，`HSM` 没有变量作用域、history 与 group-transition 语义。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合作为当前文库“状态机族演化树”里 `Statecharts` 之后层次状态机理论母线的挂接说明，因为它集中给出哪些节点是同一家族、哪些只是后续分支扩展。

### 作为目标形式主义还是中间表示

更适合作为谱系锚点与理论母线，而不是最终工程目标语言。

### 对需求到模型生成的启发

如果需求文本里已经出现“局部流程复用”“状态里再套子流程”“同一子流程在多个上下文复现”等结构信号，LLM 至少应把目标族从 flat `FSM` 提升到 `HSM` 视角，而不是直接平铺成大图。

### 现实限制

这篇条目主要贡献在理论整理，不直接给公共工具或工程标准；真正做工程落地时，还要继续落到 `UML/SCXML/HRM` 或其他具体载体。

## 重要的相关工作

### 奠基或前身工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)
- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)

### 同类型或同家族工作

- [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)
- [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)

## 文献分类总结

- 这篇论文虽然是 chapter-style summary，但主体始终围绕单一 `HSM/CHM` 家族本体，而不是跨多个无关形式主义做 survey。
- 它严格服务于当前文库“扩树优先”的目标，因为它把层次状态机理论支线的主干节点和分支方向都说清楚了。
- 在演化树中，它更适合作为 `HSM` 主枝的说明性代表条目，而不是一个完全独立的新节点。
