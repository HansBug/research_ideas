# 混成系统的算法化分析 / The algorithmic analysis of hybrid systems

## 基本信息

- 标题：The algorithmic analysis of hybrid systems
- 中文标题：混成系统的算法化分析
- 作者：Rajeev Alur, Costas Courcoubetis, Nicolas Halbwachs, Thomas A. Henzinger, Pei-Hsin Ho, Xavier Nicollin, Alfredo Olivero, Joseph Sifakis, Sergio Yovine
- 发表：*Theoretical Computer Science*, 138(1):3-34, 1995
- DOI：`10.1016/0304-3975(94)00202-T`
- 链接：https://doi.org/10.1016/0304-3975(94)00202-T
- 形式主义：`Linear Hybrid Systems / Multirate Timed Systems`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未附独立工具下载；机器可处理入口是 `$H=(Loc,Var,Lab,Edg,Act,Inv)$`、linear guards/assignments、polyhedral state sets 与 symbolic reachability。
- 标准/格式获取方式：原文没有 DSL / XML 标准，核心承载方式是 location graph、activities、invariants 和 transition relations 的数学定义。

## 简报

这篇论文的重要性不只是“分析混成系统”，而是把 `Hybrid Systems`、`Linear Hybrid Systems`、`Multirate Timed Systems` 这些经典名字用同一自动机化骨架串起来了。它明确把混成系统写成“有限位置图 + 连续变量 + location activities + invariants + guarded assignments”，然后继续划出 linear、multirate、integrator 等子类，并给出一系列 sharp 的可判定/不可判定边界。对当前文库来说，这正是 `Hybrid Automata` 主干往下长出 `Linear Hybrid Systems / Multirate Timed Systems` 子节点的关键母文献。

- 形式主义定位：`Hybrid Automata` 主干上的 algorithmic / linear 子线母文献。
- 构造方式简述：位置负责离散模式，activities 负责连续流，invariants 和 transition relations 负责模式切换约束。
- 基础设施与场景简述：polyhedral reachability、symbolic model checking 和 minimization 都建立在这套统一定义之上。

```text
hybrid system -> linear hybrid system -> multirate timed system / integrator system -> symbolic reachability / decidability boundary
```

## 形式主义定义与核心对象

### 定义对象

论文把 hybrid system 明确视作一张图：边表示 discrete transitions，顶点表示 continuous activities。系统状态由“当前位置 + 连续变量取值”组成。

### 核心抽象

原文的统一模型是：

$$
H = (Loc,Var,Lab,Edg,Act,Inv)
$$

上式中的符号逐项解释如下：

1. `Loc` 是有限 location 集。
2. `Var` 是实值变量集。
3. `Lab` 是同步标签集。
4. `Edg` 是 transition 集；每条边都带源/目标位置、同步标签和 transition relation。
5. `Act` 给每个 location 指派一组连续 activities。
6. `Inv` 给每个 location 指派 invariant 集。

系统状态写成：

$$
(\ell,v)\in Loc\times V
$$

其中 `\ell` 是离散位置，`v` 是变量赋值。

### 一个最小例子与通俗解释

论文中的 thermostat 例子非常适合作为最小直觉模型。系统有两个位置：

1. `l_{off}`：加热器关闭，温度 `x` 按某条冷却曲线下降。
2. `l_{on}`：加热器开启，温度 `x` 按另一条曲线上升。

当温度降到下阈值就从 `l_{off}` 跳到 `l_{on}`，升到上阈值再跳回去。通俗地说，`Hybrid System` 就是“每个模式里有一套连续规律，模式之间靠 guard 切换”的状态机。

### 运行 / 接受 / 转移语义

系统可以通过两种方式改变状态：

1. 做一次离散瞬时 transition。
2. 让时间流逝一段，在当前 location 的 activity 下连续演化。

原文把连续步写成：若 `f\in Act(\ell)` 且 `f(0)=v`，并且在整个持续时间内都满足 invariant，那么可以发生时间步

$$
(\ell,v)\xrightarrow{t}(\ell,f(t))
$$

离散步则由边上的 transition relation 给出：

$$
(\ell,v)\xrightarrow{a}(\ell',v')
$$

要求存在 `e=(\ell,a,\mu,\ell')\in Edg` 且 `(v,v')\in\mu`。

### 语义边界

在此基础上，论文再定义 `Linear Hybrid Systems`：要求 activities、invariants 和 transition relations 都能由线性表达式给出。更进一步，`Multirate Timed Systems` 是其中一个重要子类，变量在各 location 里按固定整数速率演化。

### 关键性质与判定边界

这篇论文最有价值的就是把 several classic boundaries 明确写出来。正结果之一是：

$$
\text{Reachability is decidable for simple multirate timed systems}
$$

而负结果同样直接：

$$
\text{Reachability is undecidable for 2-rate timed systems}
$$

以及

$$
\text{Reachability is undecidable for simple integrator systems}
$$

因此，这篇论文不是泛泛“算法化分析”，而是真正把 `Linear / Multirate / Integrator` 这几条边界节点固定进谱系里。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 `Loc` 是离散控制骨架。 |
| 事件 / 触发 | 支持 | 边带同步标签和 guard。 |
| 守卫 / 数据 | 强支持 | transition relation、linear guards 和 assignments 都是一等对象。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 部分支持 | 通过 product composition 组合多个 hybrid systems。 |
| 时间约束 | 强支持 | 时间步和连续演化是模型基础。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 允许 location-wise continuous activities。 |
| 可执行 / 可验证性 | 强理论支持 | symbolic reachability 与 decidability boundary 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$H=(Loc,Var,Lab,Edg,Act,Inv)$` | 统一的 hybrid-system 自动机定义。 |
| 系统状态 | `$(\ell,v)\in Loc\times V$` | 离散位置加连续赋值。 |
| 连续步 | `$(\ell,v)\xrightarrow{t}(\ell,f(t))$` | 在 activity 下满足 invariant 的时间流逝。 |
| 正结论 | `$\mathrm{Reachability}$ decidable for simple multirate timed systems` | 给出可判定子类。 |
| 负结论 | `$\mathrm{Reachability}$ undecidable for 2-rate timed / simple integrator systems` | 划出 sharp boundary。 |

## 构造方式与承载格式

### 建模入口

1. 先列出 locations 和实值变量。
2. 为每个 location 指定 activities 和 invariants。
3. 为每条边指定 guard / assignment relation。
4. 若所有连续约束都能线性化，则进一步落到 `Linear Hybrid Systems`。

### 机器可处理承载方式

机器可处理承载方式是 location graph、线性公式和 polyhedral state sets，而不是工程交换格式。

### 交换与互操作

它和 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md) 的早期 `Hybrid Automata` 母线高度连续，也直接通向 [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md)、[the-theory-of-rectangular-hybrid-automata/desc.md](../the-theory-of-rectangular-hybrid-automata/desc.md) 和 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md) 这些子类边界工作。

## 配套基础设施

- 建模/编辑工具：原文未提供独立工具，但后续 `HyTech` 线可直接承接。
- 解析/交换/元模型支持：核心是线性公式、polyhedra 和 graph-based hybrid semantics。
- 仿真/执行支持：run semantics 清晰，可直接解释连续/离散交替行为。
- 验证/分析支持：symbolic model checking、minimization、polyhedral reachability。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 linear / multirate hybrid verification 线的经典母文献。

## 适用场景与需求前提

### 适用场景

适合 thermostat、gas burner、water-level monitor 这类模式切换和连续变量同样重要的系统，也适合研究 `multirate` / `integrator` 的理论边界。

### 需求前提

1. 需求必须同时含 finite modes 和 continuous variables。
2. 若想落到 linear 子类，flows、guards 和 assignments 最好都能线性化。
3. 若想保住可判定性，通常还需要进一步落到更受限的子类。

### 不适用或高成本场景

对强非线性、难以写成 location-wise 活动或线性约束的系统，这条路线会迅速变重。

## 与相邻形式主义的关系

相对 [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md)，它更像标准 automaton graph 形式；相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它把 clocks-only 实时模型推广成一般 continuous variables；相对 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，后者主要固定 decidable subclass，而这篇论文给的是这些 subclass 的上位定义母线。

## 与本研究的关系

### 对 Project 1 的价值

它能把演化树里的 `Linear Hybrid Systems / Multirate Timed Systems` 稳定命名并挂到 `Hybrid Automata` 主干下。

### 作为目标形式主义还是中间表示

既可以是最终理论模型，也很适合作为从一般混成需求往可判定子类压缩时的中间层。

### 对需求到模型生成的启发

LLM 在抽取这类模型时，应显式区分 location、continuous activity、invariant 和 jump relation；否则后续很难判断能否进一步收缩到 multirate 或 rectangular。

### 现实限制

虽然给出了统一框架，但一般 reachability 很快不可判定，自动建模后仍常常需要继续收缩到更窄的分支。

## 重要的相关工作

### 奠基或前身工作

- [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md)
- [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)

### 同类型或同家族工作

- [the-theory-of-rectangular-hybrid-automata/desc.md](../the-theory-of-rectangular-hybrid-automata/desc.md)
- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 后续 `HyTech` 和 polyhedral symbolic analysis 路线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Hybrid Automata -> Linear Hybrid Systems / Multirate Timed Systems` 的关键母文献。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Linear Hybrid Systems / Multirate Timed Systems`
- 论文角色：模型提出
- 核心功能：统一定义 hybrid / linear hybrid / multirate timed 几类模型，并给出经典可判定边界。
- 关键特性：locations、activities、invariants、linear guards、multirate、polyhedral symbolic analysis。
- 构造方式：`H=(Loc,Var,Lab,Edg,Act,Inv)` + linear constraints。
- 基础设施：polyhedra、symbolic reachability、model checking；无工程标准格式。
- 适用场景：模式切换 + 连续变量系统、hybrid decidability frontier、linear/multirate 建模。
- 需求前提：需求需可拆成 finite modes 与连续变量，且最好能线性化。
- 状态：🟢
