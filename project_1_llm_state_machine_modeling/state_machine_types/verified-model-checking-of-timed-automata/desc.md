# 时间自动机的已验证模型检查 / Verified Model Checking of Timed Automata

## 基本信息

- 标题：Verified Model Checking of Timed Automata
- 中文标题：时间自动机的已验证模型检查
- 作者：Simon Wimmer，Peter Lammich
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 10805`，pp. 61-78，2018
- DOI：`10.1007/978-3-319-89960-2_4`
- 链接：https://doi.org/10.1007/978-3-319-89960-2_4
- 形式主义：`Timed Automata / Munta / Isabelle-HOL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：mechanically verified timed-automata model checker compatible with an Uppaal-bytecode subset
- 工具/实现获取方式：原文明确给出工具仓库 `https://github.com/wimmers/munta`。
- 标准/格式获取方式：主承载是 timed automata、zones/`DBM`、`Uppaal` bytecode 子集、Isabelle/HOL formalization 与导出的 `Standard ML` 实现；它不是交换标准。

## 简报

这篇论文补的是时间自动机验证里的“高可信参考实现”路线。作者不是再做一个更快的 `Uppaal` 替代品，而是把 timed-automata reachability / liveness checking、`DBM` 操作、subsumption-based search 和 `Uppaal` 风格输入都放进 `Isabelle/HOL` 的 stepwise refinement 流程里，最后导出可运行的 `Standard ML` model checker。

- 形式主义定位：`Timed Automata` 的参考验证后端，而不是新的 timed-automata 子类。
- 构造方式简述：从抽象 timed-automata formalization 出发，形式化 `DBM`、search with subsumption、`Uppaal` bytecode 子集和 on-the-fly product construction，再精化到 imperative data structures。
- 基础设施与场景简述：依托 `Isabelle/HOL`、IRF、Sepref、`DBM`、zone graph、`Uppaal` bytecode 和 `Standard ML`，服务中等规模实时系统 benchmark 的可信验证。

```text
Uppaal-style timed model -> verified product construction + DBM / zone algorithms -> Isabelle refinement chain -> Standard ML reference checker
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata；
2. clock valuations、zones 和 `DBM`；
3. abstract zone graph 与 closure-based soundness；
4. `Uppaal` bytecode 子集；
5. Isabelle/HOL 中的 refinement chain 与导出实现。

### 核心抽象

论文把 timed automaton 写成“transition set + invariants”的形式；可保守整理为：

$$
A = (L, \ell_0, C, E, Inv)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$\ell_0$` 是初始 location。
3. `$C$` 是 clocks 集合。
4. `$E$` 是边集合，每条边带 guard、action label 与 reset set。
5. `$Inv$` 是每个 location 上的 invariants。
6. 论文正文也把对象表述为 `(T,I)`；这里用更常见的元组写法做保守整理。

delay 与 action 两类基本步语义分别为：

$$
(\ell,u) \xrightarrow{d} (\ell, u \oplus d), \qquad (\ell,u) \xrightarrow{a} (\ell', [r \leftarrow 0]u)
$$

上式中的符号逐项解释如下：

1. `$u$` 是 clock valuation。
2. `$d \ge 0$` 是时间推进量。
3. `$u \oplus d$` 表示所有 clocks 同步增加 `$d$`。
4. `$r$` 是该边上要重置为 `0` 的 clocks 集合。
5. guard 与 invariant 都必须在执行时满足。

论文把两者组合成 timed-automaton 的整体一步：

$$
(\ell,u) \to_A (\ell',u') \iff \exists d \ge 0,\ a,\ u''.\ (\ell,u)\xrightarrow{d}(\ell,u'') \land (\ell,u'')\xrightarrow{a}(\ell',u')
$$

上式中的符号逐项解释如下：

1. `$u''$` 是 delay 之后、离散跳转之前的 valuation。
2. 一步总是“先 delay、后离散跳转”。
3. 这种合并对 liveness reasoning 很关键。

对抽象状态，论文强调用 zones 表示 valuation 集：

$$
Z \subseteq (C \to \mathbb{R}_{\ge 0})
$$

上式中的符号逐项解释如下：

1. `$Z$` 是一组 clock valuations。
2. 实现上用 `DBM` 对这类集合做矩阵式表示。
3. `DBM` 是 checker 工程可用性的核心。

### 一个最小例子与通俗解释

论文第一节就给出一个小例子：

1. 某 automaton 有两个 clocks。
2. location 上有限制，例如“停留时某时钟不能超过阈值”。
3. 当 guard 满足时，边被触发并重置部分 clocks。
4. checker 实际上不枚举每个实数时间，而是维护“这批 clock valuations 构成的 zone”。

通俗地说，这个工具像“一个被证明过的 `Uppaal` 风格参考裁判”。它不追求最强性能，而是追求：当它说某个 timed-automata 性质成立或给出反例时，这个结论的实现链条尽可能短且可机械校验。

### 运行 / 接受 / 转移语义

论文支持 `Uppaal` 常见的 `CTL` 片段，例如：

$$
A \Diamond \varphi,\quad A \Box \varphi,\quad E \Diamond \varphi,\quad E \Box \varphi
$$

上式中的符号逐项解释如下：

1. `$A$` 表示“所有 runs 上”。
2. `$E$` 表示“存在某条 run”。
3. `$\Diamond$` 表示 eventually。
4. `$\Box$` 表示 always。

其可达性检查本质上可以压成：

$$
A,s_0 \models E \Diamond \varphi \iff \exists s.\ s_0 \to_A^\ast s \land \varphi(s)
$$

上式中的符号逐项解释如下：

1. `$s_0$` 是初始状态。
2. `$\to_A^\ast$` 是 timed-automaton 一步关系的传递闭包。
3. `$\varphi(s)$` 表示目标状态性质。

论文还强调 subsumption-based search，可保守整理为：

$$
x \preceq x' \Rightarrow \mathrm{Succ}(x) \text{ 可由 } \mathrm{Succ}(x') \text{ 覆盖}
$$

上式中的符号逐项解释如下：

1. `$x \preceq x'$` 对 timed automata 对应“zone inclusion / coverage”类关系。
2. 若小状态已被更大抽象状态覆盖，则搜索可跳过重复分支。
3. 这是 checker 性能能够达到实用级的关键。

### 语义边界

1. 这是一篇 checker 基础设施论文，不重新定义时间自动机母理论。
2. 输入兼容目标是 `Uppaal` bytecode 的一个子集，而不是完整 `Uppaal` 前端语法。
3. 强项是可信实现与参考语义，不是大规模工业优化。
4. 时钟语义很强，但复杂程序分析只做了足以覆盖常见 benchmark 的保守子集。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$A = (L,\ell_0,C,E,Inv)$` | checker 的核心工作对象。 |
| delay / action 语义 | `$(\ell,u)\xrightarrow{d}(\ell,u\oplus d)$` 与 `$(\ell,u)\xrightarrow{a}(\ell',[r\leftarrow 0]u)$` | 时间推进与离散跳转的基础。 |
| 合成一步 | `$(\ell,u)\to_A(\ell',u')$` | liveness / reachability 的统一一步关系。 |
| zone 抽象 | `$Z \subseteq (C \to \mathbb{R}_{\ge 0})$` | 无穷 valuation space 的可计算抽象。 |
| subsumption | `$x \preceq x'$` | search with subsumption 的正确性核心。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 timed automata locations。 |
| 事件 / 触发 | 很强 | edges 带 guards、actions 和 resets。 |
| 守卫 / 数据 | 中等支持 | 支持 bounded integer shared state 和 `Uppaal` bytecode 子集。 |
| 层次 | 不支持 | 不是层次状态图前端。 |
| 并发 / 同步 | 很强 | 支持 network of automata 和 synchronization。 |
| 时间约束 | 很强 | clocks、zones、`DBM`、extrapolation 都是主轴。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic line。 |
| 可执行 / 可验证性 | 很强 | 机械化证明、精化和导出实现是全文重点。 |

### 形式化问题与性质

1. 论文解决的是“如何把时间自动机检查器本身做成可证明正确的程序”。
2. `DBM`、subsumption search 和 on-the-fly product construction 都不只是算法描述，而是被放进 refinement chain 中证明。
3. 对本论文集而言，它提供的是“timed-verification backend 的高可信锚点”，而不是新的 `TA` 分支节点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Uppaal`-style timed-automata models；
2. `Uppaal` bytecode 子集；
3. shared bounded integer variables；
4. network of automata with synchronization。

### 机器可处理承载方式

机器可处理承载方式包括：

1. zones 与 `DBM`；
2. abstract zone graph；
3. `Uppaal` bytecode instructions；
4. Isabelle/HOL specifications；
5. `Standard ML` extracted implementation。

### 交换与互操作

互操作重点在验证输入与参考实现之间：

1. 通过 reverse-engineered bytecode semantics 兼容 `Uppaal` 工具链输出。
2. 通过 product construction 把 automata network 规约到单 automaton。
3. checker 本身可作为其他 timed model checker 的 reference implementation。

## 配套基础设施

- 建模/编辑工具：主入口仍是 `Uppaal` 风格模型，而不是新图形前端。
- 解析/交换/元模型支持：bytecode parser、program analysis、network-to-single-automaton product construction。
- 仿真/执行支持：主线是 model checking，不是 runtime execution platform。
- 验证/分析支持：reachability、liveness、`CTL` fragment、zones、`DBM`、subsumption-based search。
- 代码生成/转换支持：重点是 formal refinement 到 imperative `Standard ML` implementation，而不是控制代码部署。
- 标准化或社区生态：`Isabelle/HOL`、IRF、Sepref、`Uppaal` benchmark 与 `Munta` 仓库构成其生态。

## 适用场景与需求前提

### 适用场景

适合需要可信 timed-automata reference checker 的场景，例如验证工具比对、教学型高可信后端、benchmark 交叉验证，以及中等规模实时系统性质核验。

### 需求前提

1. 系统能表达为 network of timed automata。
2. 关键数据状态最好限制在 checker 覆盖的 `Uppaal` bytecode 子集之内。
3. 团队关注的是“结果可信”而非“绝对最快”。
4. 性质主要落在 reachability / liveness / `CTL` fragment 上。

### 不适用或高成本场景

如果需求更偏巨大工业模型的极致性能、复杂用户界面建模或更丰富混成连续动力学，这条 verified-checker 路线就不是最直接选择。

## 与相邻形式主义的关系

相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，`KRONOS` 是早期高性能实时验证器，而本文强调“已验证实现”；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，本文不试图替代完整 `UPPAAL` 生态，而是尽量兼容其输入子集并作为参考后端；相对 [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)，后者优化 `SMT/BMC` 编码性能，而本文优化的是可信度与形式化精化链。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 timed-automata 不是只能“建模后交给黑盒工具”，工具本身的语义链也可以被形式化。
2. 对 `project_3` 的验证 profile 设计很有启发：如果后续要比较多个验证后端，参考实现类条目能提供语义基准。
3. 对 LLM 生成的 timed models 而言，`Uppaal`-style network + bytecode subset 也提示了一个可落地的 machine-consumable target。

### 作为目标形式主义还是中间表示

更像高可信验证后端，而不是最终的人类建模语言。

### 对需求到模型生成的启发

1. 若需求目标是实时验证，应尽早明确 clocks、guards、resets 和 invariants，而不是只写模糊时序要求。
2. 并发模板网络仍然是强而稳的 timed-model carrier，适合 LLM 输出结构化模型。
3. 如果未来要追求更高可信闭环，模型生成阶段最好直接对齐可证明语义的子集，而不是依赖不透明转换。

### 现实限制

本文强调参考实现和形式化可信性，因此对工程支持面的覆盖与性能都明显受控，不是“万能 timed platform”。

## 重要的相关工作

1. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：早期实时验证工具主线。
2. [uppaal-40/desc.md](../uppaal-40/desc.md)：经典 `Timed Automata` 平台与输入生态锚点。
3. [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)：时间自动机验证中的另一条 solver-facing 方法路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / Munta / Isabelle-HOL`
- 归类理由：主贡献是构造一个对 `Uppaal` 风格输入尽量兼容、且从语义到实现都可机械校验的 timed-automata reference checker。
