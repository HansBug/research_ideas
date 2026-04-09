# 矩形混成自动机理论 / The Theory of Rectangular Hybrid Automata

## 基本信息

- 标题：The Theory of Rectangular Hybrid Automata
- 中文标题：矩形混成自动机理论
- 作者：Peter W. Kopke
- 发表：Cornell University Computer Science Technical Report `TR96-1601`, 1996-08
- DOI：原文未提供
- 链接：https://hdl.handle.net/1813/7256
- 形式主义：`Rectangular Hybrid Automata (RHA)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论专著
- 工具/实现获取方式：原文未附统一实现；机器可处理入口是 `RHA` tuple、rectangular zones、edge/time-step semantics 与 quotient constructions。
- 标准/格式获取方式：原文没有 DSL / 交换标准，核心承载方式是 `inv/act/init/preguard/update/postguard` 这组矩形标注与相应状态空间语义。

## 简报

这份技术报告把 `Rectangular Hybrid Automata` 从一个“被提过的子类”提升成一整套系统理论。它不仅给出 `RHA` 的标准定义，还系统研究 reachability、temporal-logic model checking、controller synthesis，以及 bisimilarity / similarity / language equivalence 这几种 quotient 结构。对当前文库最关键的是：它把 `Hybrid Systems with Rectangular Differential Inclusions (1994)` 和 `Initialized Rectangular Automata (1998)` 之间缺失的那层“矩形混成自动机母节点”正式补出来了。

- 形式主义定位：`Hybrid Automata` 主干上矩形可判定边界分支的核心母文献。
- 构造方式简述：每个 vertex 用 invariant、activity rectangle 和 initial condition 标注；每条 edge 用 preguard、update、postguard 和 event 标注。
- 基础设施与场景简述：核心基础设施是 rectangular zone、timed-automata translation、finite quotient 与复杂度分析，而不是工程建模 DSL。

```text
hybrid automaton -> rectangular hybrid automaton -> initialized / positive / bounded-nondeterministic subclasses -> reachability / model checking / controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

`RHA` 是有限 automaton 与连续变量系统的组合，但所有连续约束都被限制成按坐标解耦的 rectangles。这使它既比一般 `Linear Hybrid Automata` 弱，又比纯 clocks-only 模型强。

### 核心抽象

原文把一个矩形自动机写成：

$$
A = (V,E,inv,act,init,preguard,update,postguard,\Sigma,event)
$$

上式中的符号逐项解释如下：

1. `V,E` 是有限 control graph。
2. `inv:V\to B^n` 给每个 vertex 指派 invariant rectangle。
3. `act:V\to B^n` 给每个 vertex 指派 activity rectangle，即导数区间。
4. `init:V\to B^n` 给出初始连续状态区域。
5. `preguard:E\to B^n` 是离散跳转前必须满足的矩形条件。
6. `update:E\to 2^{\{1,\ldots,n\}}` 指定哪些坐标允许在该 edge 上被重赋值。
7. `postguard:E\to B^n` 给出跳转后的目标矩形区间。
8. `\Sigma` 是事件字母表，`event:E\to\Sigma` 给每条边打事件标签。

状态写成：

$$
(v,x)\in V\times \mathbb{R}^n,\quad x\in inv(v)
$$

### 一个最小例子与通俗解释

一个最小直觉例子是“带 bounded drift 的本地时钟”。设位置 `Run` 中时钟 `x` 的导数满足 `\dot{x}\in[1-\rho,1+\rho]`；当 `x` 进入某个 preguard 时，系统沿一条边跳到 `Reset`，并把 `x` 重置到 postguard 指定的某个区间。这样：

1. 在一个位置里，`x` 不是固定速率，而是在一个矩形斜率盒子里变化。
2. 跳边时，一部分变量保持不变，另一部分变量按 postguard 重新取值。

通俗地说，`RHA` 就是“每个模式里每个连续变量都只允许在一个区间速率里走”的混成自动机。

### 运行 / 接受 / 转移语义

edge-step 语义可保守写成：

$$
(v,x)\xrightarrow{e}(w,y)
$$

当且仅当 `e=(v,w)`，`x\in preguard(e)`，`y\in postguard(e)`，并且所有不在 `update(e)` 中的坐标满足 `y_i=x_i`。

连续 time-step 语义则要求：当控制停在 `v` 时，连续状态沿某条可微轨迹演化，并始终保持

$$
x(t)\in inv(v),\qquad \dot{x}(t)\in act(v)
$$

这正是“rectangular”这个名字的来源：不变式和导数约束都来自 rectangles。

### 语义边界

它比 [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md) 更一般，因为显式保留了 control graph、preguard、postguard 与 update；但它又比一般 `Linear Hybrid Automata` 更受限，因为连续约束必须按坐标分解成矩形。

### 关键性质与判定边界

这份专著最核心的是把多个经典结论集中整理成一条线。可以保守浓缩为：

$$
\text{Reachability(initialized RHA) is decidable}
$$

同时，原文还强调：

$$
\text{if rectangularity or initialization is relaxed, reachability becomes undecidable}
$$

此外，对 initialized RHA with bounded nondeterminism，在 time-divergence 语义下，`CTL^*` / `LTL` model checking 也有明确复杂度分析，属于这一家族“可判定但不轻量”的代表结果。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 control graph 是离散骨架。 |
| 事件 / 触发 | 支持 | 每条 edge 带 event label。 |
| 守卫 / 数据 | 强支持 | `preguard/postguard/update` 显式建模离散跳转。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 非重点 | 核心是单体语义和可判定边界。 |
| 时间约束 | 强支持 | 连续时间通过 time-step 语义进入。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每维导数处于区间盒子 `act(v)` 中。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、temporal logic 和 control 都被系统研究。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$A=(V,E,inv,act,init,preguard,update,postguard,\Sigma,event)$` | `RHA` 的标准 tuple。 |
| 系统状态 | `$(v,x)\in V\times\mathbb{R}^n$` with `$x\in inv(v)$` | 离散位置加连续状态。 |
| 连续约束 | `$x(t)\in inv(v),\ \dot{x}(t)\in act(v)$` | time-step 期间必须满足的矩形限制。 |
| 正结论 | `$\text{Reachability(initialized RHA) is decidable}$` | 保住可判定性的经典子类。 |
| 负结论 | `$\neg rectangular \lor \neg initialized \Rightarrow$ undecidable in general` | 说明这条边界为什么重要。 |

## 构造方式与承载格式

### 建模入口

1. 先给出 finite control graph。
2. 为每个 vertex 补 `inv/act/init`。
3. 为每条 edge 补 `preguard/update/postguard/event`。
4. 若需要可判定性，继续检查是否满足 initialized、bounded-nondeterministic 或 positive 等子类条件。

### 机器可处理承载方式

机器可处理承载方式是 rectangular zones、edge/time-step relations 和相应 quotient / translation，而不是工程文件格式。

### 交换与互操作

它位于 [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md) 和 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md) 之间：前者给出更早的矩形微分包含母型，后者进一步钉住 initialized rectangular 的最大可判定边界。

## 配套基础设施

- 建模/编辑工具：原文未附统一实现。
- 解析/交换/元模型支持：核心是 rectangular zone 表示与相关等价关系。
- 仿真/执行支持：edge/time-step semantics 清晰，可直接解释执行。
- 验证/分析支持：reachability、`CTL^*` / `LTL` model checking、controller synthesis、bisimilarity / similarity / language equivalence quotient。
- 代码生成/转换支持：原文不讨论工程代码生成，但大量使用到 timed-automata translation。
- 标准化或社区生态：是 `RHA` 作为独立命名家族的经典专著级条目。

## 适用场景与需求前提

### 适用场景

适合 bounded-drift 协议、本地时钟漂移、矩形近似的物理系统，以及希望把一般混成系统保守收缩到可分析子类的场景。

### 需求前提

1. 连续变量约束必须能按坐标分解成矩形区间。
2. guard / reset 也最好能表示成 rectangles。
3. 若要保住经典正结果，通常还要满足 initialization 等附加纪律。

### 不适用或高成本场景

对于强耦合线性或非线性流、复杂跨维约束系统，矩形近似可能过于保守。

## 与相邻形式主义的关系

相对 [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md)，`RHA` 是更受限、更贴 decidable frontier 的子类；相对 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，这份文献本身更像“完整理论母书”，而后者是在其上继续强调 initialized boundary；相对 [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)，`RHA` 属于更典型的 hybrid 线，而不是从 `TA` 向上长出的 `0/1` 导数线。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树中 `Rectangular Hybrid Automata` 这层长期缺失的母节点补齐，让 `1994 rectangular differential inclusion -> 1996 RHA -> 1998 initialized rectangular` 这条链条闭合。

### 作为目标形式主义还是中间表示

更适合作为理论目标或中间抽象层；工程上常作为一般混成模型的保守逼近。

### 对需求到模型生成的启发

当需求里出现“每个模式里变量变化率只在某个区间内波动、切换时只重置部分变量”时，`RHA` 是非常自然的抽取目标。

### 现实限制

一旦离开 rectangular 或 initialization discipline，可判定性会很快失去；因此自动生成后通常还需要严格检查建模纪律。

## 重要的相关工作

### 奠基或前身工作

- [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md)

### 同类型或同家族工作

- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)
- [o-minimal-hybrid-systems/desc.md](../o-minimal-hybrid-systems/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有标准格式；与之最紧的工具/理论基础设施是 timed-automata translation 和 quotient-based verification。

### 与本研究关系最紧的工作

- 它最适合挂成 `Hybrid Automata -> Hybrid Systems with Rectangular Differential Inclusions -> Rectangular Hybrid Automata -> Initialized Rectangular Automata` 这条链条里的中间母节点。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Rectangular Hybrid Automata (RHA)`
- 论文角色：理论专著
- 核心功能：把 `RHA` 固定为独立家族，并系统研究其 reachability、model checking 和 control 边界。
- 关键特性：rectangular zones、`inv/act/init/preguard/update/postguard`、initialized / positive subclasses、time divergence、finite quotients。
- 构造方式：graph + rectangular labels + edge/time-step semantics。
- 基础设施：timed-automata translation、quotient analysis、复杂度理论；无工程标准格式。
- 适用场景：bounded-drift 协议、矩形近似的连续控制系统、decidable hybrid 建模预筛。
- 需求前提：连续约束和离散更新需可矩形化，且最好满足 initialization 等纪律。
- 状态：🟢
