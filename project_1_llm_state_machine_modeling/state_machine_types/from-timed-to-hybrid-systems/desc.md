# 从定时系统到混成系统 / From Timed to Hybrid Systems

## 基本信息

- 标题：From Timed to Hybrid Systems
- 中文标题：从定时系统到混成系统
- 作者：Oded Maler, Zohar Manna, Amir Pnueli
- 发表：收录于 *Real-Time: Theory in Practice*, LNCS 600, pp. 447-484, 1992
- DOI：`10.1007/BFb0032003`
- 链接：https://www-verimag.imag.fr/PEOPLE/Oded.Maler/Papers/mmp.pdf
- 形式主义：`Timed Transition Systems / Phase Transition Systems`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具；机器可处理入口是 `Timed Transition System` 的 `$S=(V,\Theta,T,l,u)$` 与 `Phase Transition System` 的 `$\Phi=(V,\Theta,T,A,l,u)$`。
- 标准/格式获取方式：原文没有 XML / DSL 标准，核心承载方式是 transition-system tuple、age-based temporal logic、以及带微分方程标注的 hybrid statecharts。

## 简报

这篇论文的地位在于，它把“实时状态机”从普通离散 transition-system 语义一路推进到能容纳连续演化的 `Phase Transition Systems`。它不是后来的 `Timed Automata` 路线，也不是再晚一点的 `Hybrid Automata` 图式，而是一条更偏 transition-system / temporal-logic 的母线：先给出 `Timed Transition Systems`，再把它们推广到 `hybrid traces`、`activities` 和 `phase transition systems`。对当前文库来说，这正好补上了“时间 / 连续主干”里长期缺失的 `Timed Transition Systems` 与 `Phase Transition Systems` 命名母节点。

- 形式主义定位：`Timed Transition Systems` 到 `Phase Transition Systems` 的桥接型母文献。
- 构造方式简述：用带上下界的离散 transition 建模 timed behavior，再把连续演化写成 activities，把 hybrid behavior 写成 phases 的交替序列。
- 基础设施与场景简述：核心不是工程文件格式，而是 age-based temporal logic、hybrid traces 与 hybrid statecharts 这组语义/规约工具。

```text
discrete transition system -> timed transition system -> hybrid trace / activity -> phase transition system -> hybrid statechart / temporal verification
```

## 形式主义定义与核心对象

### 定义对象

论文先讨论 timed systems，再把同一套语义骨架推广到 hybrid systems。它关心的是“系统行为如何被定义与验证”，而不是某个具体求解器输入格式。

### 核心抽象

定时部分的核心模型是：

$$
S = (V,\Theta,T,l,u)
$$

上式中的符号逐项解释如下：

1. `V` 是状态变量集合。
2. `\Theta` 是初始条件。
3. `T` 是有限 transition 集，每个 transition 都有自己的 transition relation。
4. `l` 给每个 transition 指定最小等待时间。
5. `u` 给每个 transition 指定最大等待时间。

推广到混成域后，论文定义：

$$
\Phi = (V,\Theta,T,A,l,u)
$$

这里新增的符号只有 `A`，表示 activities 集。每个 activity 都带一个 activation condition 和一组微分约束，用来描述连续变量在一个 phase 内如何演化。对 `\Phi` 还要求 `V = V_c \cup V_d`，其中 `V_c` 是连续变量，`V_d` 是离散变量。

### 一个最小例子与通俗解释

论文中给了一个非常小的 `PTS` 例子：连续变量 `x` 在 activity 的作用下按 `\dot{x}=1` 持续增长；当 `x` 变到某个阈值时，一个立即 transition 被触发，把离散变量 `y` 从 `0` 改成 `1`。于是系统的运行轨迹自然分成两段：

1. 先是一段正时间长度的连续 phase，`x` 连续增长。
2. 到阈值时发生一个零时间的离散跳转，`y` 被瞬时更新。

通俗地说，`PTS` 就是在普通状态机上再加一种“状态内部连续流动”的能力。普通状态机只有“跳”；`PTS` 既有“跳”，也有“流”。

### 运行 / 接受 / 转移语义

论文把 hybrid behavior 写成 hybrid trace。离散部分满足离散后继关系；连续部分则要求所有连续变量在一个闭区间内满足相应 activities 的微分约束。对 `PTS` 中的一条 activity，原文写法可压成：

$$
a \to \dot{y} = r
$$

这里 `a` 是 activation condition，`\dot{y}=r` 是对连续变量 `y` 的演化规则。

对 `PTS` 的 computation，关键要求之一是：如果在某个离散采样点发生 transition `\tau`，那么必须满足

$$
\sigma(i+1,t_i) \in \tau(\sigma(i,t_i))
$$

而在连续 phase 内，所有 `y \in V_c` 都要满足当前 operational activities 给出的微分方程。

### 语义边界

这条路线非常强调 transition-system 语义和 temporal verification。它比纯 clocks-only 的实时模型更宽，因为允许一般 continuous activities；但它又比后来的 `Hybrid Automata` 更偏“语义母型”，而不是固定的 automaton graph + invariant/flow/jump 标注格式。

### 关键性质与判定边界

论文的重点不在某个 reachability complexity，而在“形式主义能否统一承载 timed / hybrid semantics”。两条最关键的结构结论可以保守写成：

$$
\text{Timed semantics} \leadsto S=(V,\Theta,T,l,u)
$$

以及

$$
\text{Hybrid semantics} \leadsto \Phi=(V,\Theta,T,A,l,u)
$$

也就是说，混成扩展并没有推翻 timed-transition 的骨架，只是把连续 activities 加了进去。对当前文库的演化树而言，这正是它的节点价值。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `TTS/PTS` 都有明确的离散 transition 骨架。 |
| 事件 / 触发 | 支持 | 离散 transition 由 enabling 条件与上下界共同约束。 |
| 守卫 / 数据 | 强支持 | transition relation 和初始条件都可显式引用状态变量。 |
| 层次 | 核心模型不支持、规约层支持 | `PTS` 本体不是层次自动机，但论文同时给出 hybrid statecharts 作为规格层。 |
| 并发 / 同步 | 非重点 | 重点是 timed / hybrid semantics，而不是并发组合代数。 |
| 时间约束 | 强支持 | `l/u` 上下界与 age-based references 是核心。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 通过 activities 和微分方程引入连续演化。 |
| 可执行 / 可验证性 | 强理论支持 | 论文同时给出 temporal specification 与 invariance 证明思路。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed 模型骨架 | `$S=(V,\Theta,T,l,u)$` | `Timed Transition Systems` 的核心 tuple。 |
| hybrid 模型骨架 | `$\Phi=(V,\Theta,T,A,l,u)$` | 在 `TTS` 上加入 activities。 |
| activity 约束 | `$a \to \dot{y}=r$` | 连续 phase 内的微分演化规则。 |
| 离散后继 | `$\sigma(i+1,t_i)\in\tau(\sigma(i,t_i))$` | 采样点上的 transition 语义。 |
| 结构增量 | `$\Phi = S + A$` | `PTS` 可看作 `TTS` 的连续活动扩展。 |

## 构造方式与承载格式

### 建模入口

1. 先列出状态变量、初始条件和离散 transitions。
2. 若系统只含 timing discipline，可停在 `TTS`。
3. 若系统还包含连续变量演化，则为连续变量补 activities 与微分约束，形成 `PTS`。
4. 若需要图形化规格，可再把 `PTS` 写成带微分方程标注的 hybrid statecharts。

### 机器可处理承载方式

机器可处理承载方式是 timed / hybrid tuples、transition relations、activities 和 temporal formulas，而不是交换文件标准。

### 交换与互操作

它和 [verification-of-clocked-and-hybrid-systems/desc.md](../verification-of-clocked-and-hybrid-systems/desc.md) 的 `CTS/PTS` 线直接相连，也和 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md) 的 `Hybrid Automata` 母型构成两条并行但可对照的早期 hybrid 主线。

## 配套基础设施

- 建模/编辑工具：原文未提供独立工具。
- 解析/交换/元模型支持：核心是 tuples、age functions 和 hybrid statecharts，不是标准化交换格式。
- 仿真/执行支持：通过 timed traces / hybrid traces 给出明确运行语义。
- 验证/分析支持：提供 age-based temporal specification，以及针对 invariance 的 proof rule。
- 代码生成/转换支持：原文未讨论工程级代码生成。
- 标准化或社区生态：是 transition-system 风格 timed / hybrid semantics 的经典源头之一。

## 适用场景与需求前提

### 适用场景

适合需要先从语义层面讲清“系统何时跳、何时连续流动”的场景，尤其适合作为 timed / hybrid 母线的理论入口。

### 需求前提

1. 需求必须能区分离散 transition 与连续 activity。
2. 若要落到 `PTS`，至少有一部分状态变量需要满足显式微分约束。
3. 如果需求本身就偏 temporal-logic specification，这条路线会比纯图形状态机更自然。

### 不适用或高成本场景

若目标是直接交给现代 model checker 的工业输入格式，这篇论文给出的主要还是语义骨架，不是现成 DSL。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它不是 region / automata-theoretic 线，而是 transition-system / temporal-logic 线；相对 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)，它更早地把“离散 + 连续”用 phase 和 activity 讲清；相对 [verification-of-clocked-and-hybrid-systems/desc.md](../verification-of-clocked-and-hybrid-systems/desc.md)，后者可看作对 `TTS` 线的再整理和 proof-oriented 强化。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树中长期空缺的 `Timed Transition Systems` 与 `Phase Transition Systems` 节点一次性补齐，避免时间/连续主干直接从 `Timed Automata` 和 `Hybrid Automata` 开始。

### 作为目标形式主义还是中间表示

更适合作为高层语义母型和中间表示，而不是最终工程交付格式。

### 对需求到模型生成的启发

如果 LLM 先把需求拆成“离散跳转规则 + 连续活动规则”，再决定后续落到 `CTS`、`TA` 还是 `HA`，会比一开始就硬选具体模型更稳。

### 现实限制

缺少现代工具输入标准；很多后续自动验证仍要继续收缩成 `Timed Automata`、`Linear Hybrid` 或 `Rectangular` 之类的子类。

## 重要的相关工作

### 奠基或前身工作

- 论文本身就是 timed / hybrid transition semantics 的早期奠基条目。

### 同类型或同家族工作

- [verification-of-clocked-and-hybrid-systems/desc.md](../verification-of-clocked-and-hybrid-systems/desc.md)
- [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准；其规格层上的关键承载是 hybrid statecharts。

### 与本研究关系最紧的工作

- 它最适合挂成“时间 / 连续主干”里 `Timed Transition Systems -> Phase Transition Systems` 的母节点文献。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Timed Transition Systems / Phase Transition Systems`
- 论文角色：模型提出
- 核心功能：把 timed transition semantics 推进到含 continuous activities 的 phase-transition semantics。
- 关键特性：`l/u` 上下界、age functions、activities、hybrid traces、hybrid statecharts。
- 构造方式：`S=(V,\Theta,T,l,u)` / `\Phi=(V,\Theta,T,A,l,u)` + temporal specification。
- 基础设施：纯理论语义框架，无工程标准/工具。
- 适用场景：timed / hybrid semantics 建模、transition-system 风格需求规约与验证。
- 需求前提：需求需能拆成离散 transitions、时间界和连续 activities。
- 状态：🟢
