# 混成自动机：面向混成系统规约与验证的算法化方法 / Hybrid Automata: An Algorithmic Approach to the Specification and Verification of Hybrid Systems

## 基本信息

- 标题：Hybrid Automata: An Algorithmic Approach to the Specification and Verification of Hybrid Systems
- 中文标题：混成自动机：面向混成系统规约与验证的算法化方法
- 作者：Rajeev Alur, Costas Courcoubetis, Thomas A. Henzinger, Pei-Hsin Ho
- 发表：Cornell University Technical Report TR 93-1343, 1993；对应精简会议版本发表于 *Hybrid Systems*, LNCS 736, pp. 209-229
- DOI：对应会议版本 DOI 为 `10.1007/3-540-57318-6_30`；当前入库 PDF 为 Cornell 技术报告版本，原报告未单列 DOI
- 链接：https://ecommons.cornell.edu/server/api/core/bitstreams/4acee44b-8ef7-4ff4-8c08-8a3e3e6c2301/content
- 形式主义：`Hybrid Automata / Linear Hybrid Systems`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具下载；机器可处理入口是 hybrid system tuple、linear guards/assignments、run/trace semantics 和 product。
- 标准/格式获取方式：原文没有 DSL/XML 标准，核心承载方式是控制位置图、活动集合、异常/不变式和跳转关系的数学定义。

## 简报

这篇技术报告是 `Hybrid Automata` 主干非常早的一版算法化定义：它把 hybrid system 写成有限控制位置 + 连续活动 + 异常/不变式 + 跳转关系，并把 timed systems、multirate timed systems、integrator systems 和 parameterized variants 都放进同一条谱系。虽然一般 reachability 很快不可判定，但论文仍给出面向 piecewise-linear hybrid automata 的两类半判定验证过程。对演化树而言，它比后来的 1996 技术报告更适合把 `Hybrid Automata` 根节点往前推回 1993。

- 形式主义定位：有限状态机向“离散控制 + 连续物理流”扩展后的混成状态机母型，并显式包含 timed / multirate / integrator 子类。
- 构造方式简述：每个 location 带 activity、exception/invariant；每条 transition 带 guard 和 assignments；运行由时间流逝步与瞬时跳转步交替组成。
- 基础设施与场景简述：原文不提供工程 DSL，但给出 product composition、Muller acceptance、linear subclass 和 safety verification semidecision procedures，后续 `HyTech` 线可直接承接。

```text
离散程序模式 + 连续物理变量 -> Hybrid Automaton / Linear Hybrid System -> run / product / safety semidecision
```

## 形式主义定义与核心对象

### 定义对象

论文面向的是“离散程序嵌在连续环境里”的 hybrid systems。状态由一个有限 control location 和一组实值 data variables 的取值共同组成。

### 核心抽象

按原文 Section 2.2，可把 hybrid system 写成：

$$
A = (V_P, Q, \mu_1, \mu_2, \mu_3)
$$

上式中的符号逐项解释如下：

1. `V_P` 是有限个实值 data variables。
2. `Q` 是有限个 control locations。
3. `\mu_1` 给每个 location 指派一组允许的连续 activities。
4. `\mu_2` 给每个 location 指派 exception set；其补集可理解为 invariant。
5. `\mu_3` 给每对 locations 指派离散 transition relation / guarded assignments。

系统状态可写成：

$$
(\ell,\sigma)\in Q\times X_P
$$

其中 `\ell` 是离散位置，`\sigma` 是 `V_P` 上的变量赋值，`X_P` 是所有 data states 的集合。

### 一个最小例子与通俗解释

论文 Figure 1 就给了一个单变量 `x` 的两位置线性混成例子：在位置 `\ell_1` 里 `x` 以速率 `-1` 下降；当 `x<6` 时可跳到 `\ell_2`，并执行 `x:=x-1`；在 `\ell_2` 里 `x` 以速率 `2` 上升，且一旦 `x=10` 就必须切回 `\ell_1`，因为 `\ell_2` 的 invariant 是 `x<10`。

通俗地说，`Hybrid Automata` 就像“每个离散模式里都挂着一段连续动力学规则的状态机”。普通 `FSM` 只知道在哪个模式；`Hybrid Automata` 还要同时追踪温度、水位、位置这类连续变量怎样随时间演化，以及何时因 guard/invariant 触发跳转。

### 运行 / 接受 / 转移语义

一条 run 是离散跳转和连续活动交替组成的序列：

$$
\rho = (\ell_0,\sigma_0,J_0,f_0)(\ell_1,\sigma_1,J_1,f_1)\cdots
$$

其中 `J_i` 是第 `i` 段时间区间，`f_i\in\mu_1(\ell_i)` 是该段连续 activity。离散跳转需满足 successor relation：

$$
(\sigma_i,\sigma_{i+1})\in \mu_3(\ell_i,\ell_{i+1})
$$

连续演化则要求 `f_i(0)=\sigma_i`，且在 `J_i` 内始终不触发 `\mu_2(\ell_i)` 给出的 exception。

若把 hybrid system 加上初始条件 `\mu_4` 和 Muller 接受族 `F`，则得到 hybrid Muller automaton `(A,\mu_4,F)`；接受要求初态满足 `\mu_4`，且有限 run 的终止 location 或无限 run 的 `P_\infty` 落入 `F`。

### 语义边界

当每个变量在每个 location 都以固定线性速率变化、guards/assignments 都是线性公式时，得到 linear hybrid systems；若变量都只是 propositions 和 clocks，就退化为 timed systems。也就是说：

$$
\text{Timed Systems} \subseteq \text{Linear Hybrid Systems} \subseteq \text{Hybrid Systems}
$$

### 关键性质与判定边界

论文一方面强调一般 hybrid verification 的困难性：

$$
\text{Emptiness is undecidable for 2-rate timed systems and simple integrator systems}
$$

另一方面，它对 piecewise-linear hybrid automata 给出 fixpoint-based 和 minimization-based 两类 safety 半判定过程，并证明：

$$
\text{if a procedure terminates, then its answer is correct}
$$

这使该论文既是模型本体定义文献，也是后续可判定子类和符号验证算法的起点之一。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 control locations 是离散骨架。 |
| 事件 / 触发 | 支持 | 跳转由 guard、exception 和 transition relation 触发。 |
| 守卫 / 数据 | 强支持 | 允许实值变量、线性公式和重置/赋值。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 部分支持 | 通过 product composition 组合多个 hybrid systems。 |
| 时间约束 | 强支持 | 时间通过 continuous activities 和 interval sequence 进入。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每个 location 可挂 piecewise-smooth 或 linear continuous dynamics。 |
| 可执行 / 可验证性 | 部分支持 | 语义可执行，但一般 reachability 不可判定；linear 子类有半判定过程。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$A=(V_P,Q,\mu_1,\mu_2,\mu_3)$` | hybrid system 的早期自动机化定义。 |
| 系统状态 | `$(\ell,\sigma)\in Q\times X_P$` | 离散位置 + 连续数据状态。 |
| 离散跳转 | `$(\sigma_i,\sigma_{i+1})\in\mu_3(\ell_i,\ell_{i+1})$` | successor relation / guarded assignments。 |
| 子类包含 | `$\text{Timed}\subseteq\text{Linear Hybrid}\subseteq\text{Hybrid}$` | `TA` 是 `HA` 的受限特例。 |
| 不可判定性 | `$\text{Emptiness}$ undecidable for 2-rate timed / simple integrator` | 解释为什么必须研究可判定子类。 |

## 构造方式与承载格式

### 建模入口

1. 先列出有限 control locations 和实值变量 `V_P`。
2. 为每个 location 指定 continuous activities 和 exception/invariant。
3. 为每条离散边指定 guard 与 assignments / successor relation。
4. 如需系统级组合，用 product operation 合成 component hybrid automata。

### 机器可处理承载方式

机器可处理承载方式是位置图、线性公式、赋值集合、run/trace semantics 和 product composition；原文没有独立 DSL。

### 交换与互操作

它和 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 timed automata 母线、[the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md) 的后续理论总结，以及 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md) 的 decidability boundary 线直接相连。

## 配套基础设施

- 建模/编辑工具：原文未提供独立工具下载。
- 解析/交换/元模型支持：无 DSL/标准格式，核心是数学 tuple 与 guard/assignment 公式。
- 仿真/执行支持：run / trace semantics 可直接解释连续演化和瞬时跳转。
- 验证/分析支持：fixpoint / minimization 两类半判定过程面向 safety properties。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是后续 `HyTech`、linear hybrid verification 与 decidable hybrid subclasses 的早期理论源头。

## 适用场景与需求前提

### 适用场景

适合 water-level monitor、thermostat、gas burner、real-time mutual exclusion 等既有离散模式切换又有连续变量变化的 hybrid/CPS 基线建模。

### 需求前提

1. 需求必须同时包含有限离散模式和连续变量。
2. 每个模式下的连续行为可写成 differential equations / linear rates。
3. 跳转条件和重置关系可写成 guard/assignment。

### 不适用或高成本场景

若系统只是纯离散控制或纯实时 clock 约束，普通 `FSM` / `Timed Automata` 更经济；若连续动力学强非线性且不可保守线性化，算法分析会迅速变重。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文把 unit-rate clocks 推广成一般 location-dependent continuous activities；相对 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)，本文更早，且更强调 linear 子类、product 和半判定算法；相对 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，本文是上位模型定义源，后者专门划可判定边界。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Hybrid Automata` 主干的代表条目从 1996 回推到 1993，并明确补出 `Linear Hybrid / Timed / Integrator` 子类脉络，适合直接用于演化树扩充。

### 作为目标形式主义还是中间表示

当需求真的涉及模式切换 + 连续物理变量时，它可以作为目标形式主义；在更工程化流程里也可作为从自然语言需求到 `UPPAAL/HyTech` 可分析子类之间的中间语义层。

### 对需求到模型生成的启发

需求抽取时应显式区分“哪些是 location/mode”“哪些是 continuous state”“哪些是不变式/异常触发”“哪些是 jump assignments”，否则很难从自然语言直接落到 hybrid tuple。

### 现实限制

原文没有标准化文件格式或现成 DSL，而且一般混成可达性不可判定，自动生成后往往还要继续收缩到 rectangular/timed 等子类。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)
- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)

### 标准 / 格式 / 工具链工作

- `HyTech` 后续工具线。

### 与本研究关系最紧的工作

- 它是当前 `Hybrid Automata` 主干最适合向前补年份和子类谱系的经典定义文献之一。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Hybrid Automata / Linear Hybrid Systems`
- 论文角色：模型提出
- 核心功能：把 hybrid systems 统一写成有限位置 + 连续活动 + 异常/不变式 + 跳转关系，并给出 linear/timed/integrator 子类和安全半判定分析。
- 关键特性：hybrid traces、linear guards/assignments、Muller acceptance、product composition、timed-system special case、undecidability boundary。
- 构造方式：`A=(V_P,Q,\mu_1,\mu_2,\mu_3)` + activities/exceptions/transitions + run semantics。
- 基础设施：理论算法清晰，后续可接 `HyTech`，但原文无 DSL/标准文件格式。
- 适用场景：CPS / hybrid control 基线模型、water-level / thermostat / gas-burner 等离散-连续混合对象。
- 需求前提：需求同时含有限模式与连续变量，并能为每个模式/跳转给出 flow、invariant/exception 和 guard/reset。
- 状态：🟢
