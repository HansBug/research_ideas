# 组合电路时序分析 / On Timing Analysis of Combinational Circuits

## 基本信息

- 标题：On Timing Analysis of Combinational Circuits
- 中文标题：组合电路时序分析
- 作者：Ramzi Ben Salah，Marius Bozga，Oded Maler
- 发表：*Formal Modeling and Analysis of Timed Systems*，pp. 204-218，2004
- DOI：`10.1007/978-3-540-40903-8_17`
- 链接：https://doi.org/10.1007/978-3-540-40903-8_17
- 形式主义：`Timed Boolean Circuits / acyclic Timed Automata / IF-Kronos-Aldebaran`
- 主类：⏱️ 时间 / 时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：组合电路最大稳定时间分析 / `IF-Kronos-Aldebaran` 抽象验证路线
- 工具/实现获取方式：原文明确说明工具链由 `IF`、`Kronos` 与 `Aldebaran` 组成，其中电路首先被自动翻译成 `IF` 格式的 interacting timed automata。
- 标准/格式获取方式：输入是带 delay 区间的布尔电路方程；中间承载是 `IF` timed automata network 与 reachability graph；输出是抽象 automaton 与最大稳定时间估计。

## 简报

这篇论文的重点，不是重新定义 timed automata，而是把“组合电路最大稳定时间”这类硬件 timing 问题拉到 `acyclic timed automata` 上解决，并用分而治之的子电路抽象缓解状态爆炸。它同时补了一个对 `state_machine_types` 很有价值的点：timed-automata 工具并不只服务软件时序协议，也能作为数字电路 timing analysis 的统一符号后端。

- 形式主义定位：`acyclic timed automata` 驱动的组合电路 timing-analysis 方法路线。
- 构造方式简述：`Boolean equations + delay intervals -> timed Boolean circuit -> interacting timed automata -> reachability graph -> abstract sub-circuit automaton`。
- 基础设施与场景简述：依托 `IF`、`Kronos`、`Aldebaran` 与 reachability-graph minimization，服务 worst-case propagation delay / false-path aware timing analysis。

```text
timed circuit -> acyclic timed automata network -> reachability graph -> abstract sub-circuit automaton -> maximal stabilization time
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. Boolean circuit。
2. timed Boolean circuit。
3. bi-bounded inertial delay operator。
4. acyclic timed automata network。
5. 基于 reachability graph 的子电路抽象 automaton。

### 核心抽象

论文给出的 timed circuit 骨架是：

$$
C = (V, \prec, F, I)
$$

上式中的符号逐项解释如下：

1. `$V$` 是节点集合。
2. `$\prec$` 是无环的直接影响关系。
3. `$F$` 为每个非输入节点指定布尔函数。
4. `$I$` 为每个非输入节点指定 delay 区间 `$I_v=[l_v,u_v]$`。

延迟元件被建成一个非确定性算子：

$$
D_I : A \times S(A) \to 2^{S(A)}
$$

上式中的符号逐项解释如下：

1. `$A$` 是离散值域。
2. `$S(A)$` 是取值于 `$A$` 的信号集合。
3. `$I=[l,u]$` 给出传播延迟的上下界。
4. 输出信号必须满足“变化早于 `$l$` 不传播、持续到 `$u$` 必须传播”的 bi-bounded inertial 语义。

组合电路稳定时间问题则被定义为：

$$
\theta(C,x,x') = \max \{ \theta(\beta) : \beta \in L(C,x,x') \}
$$

$$
\theta(C) = \max \{ \theta(C,x,x') : x,x' \in X \}
$$

上式中的符号逐项解释如下：

1. `$x$` 是前一周期输入，对应初始稳定状态。
2. `$x'$` 是当前周期新输入。
3. `$L(C,x,x')$` 是在该输入切换下所有可能输出信号的集合。
4. `$\theta(\beta)$` 是输出信号 `$\beta$` 的稳定时间。
5. `$\theta(C)$` 是整个电路的最大稳定时间。

论文再把电路编成 timed automaton：

$$
A = (Q, C, I, \Delta)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是离散状态集合。
2. `$C$` 是 clocks 集合。
3. `$I$` 是 location invariants。
4. `$\Delta$` 是带 guard 和 reset 的迁移关系。

### 一个最小例子与通俗解释

论文里最直观的最小例子是带两个输入和若干 gate delay 的无环组合电路：

1. 输入在一个周期内只变化一次。
2. 每个 gate 的输出不再被看作“瞬时算完”，而是先进入不稳定状态，再在 delay 区间内稳定到新值。
3. 如果只做 static timing analysis，通常会沿最长路径累加延迟，得到偏保守的上界。
4. timed automata 模型则能识别某些逻辑上根本无法同时触发的 false paths，因此给出更紧的最大稳定时间。

通俗地说，这条路线就是“把门电路都换成会拖延、会后悔、会稳定的状态机”，然后让 `Kronos` 去找“最晚什么时候整个电路真的稳定下来”。

### 运行 / 接受 / 转移语义

论文把一个 delay 元件建成四状态 timed automaton：`0, 0', 1, 1'`。其中：

1. `0 / 1` 是稳定状态。
2. `0' / 1'` 是输入变化后的不稳定状态。
3. `excite`、`stabilize`、`regret` 三类迁移分别表示被激发、完成传播、提前取消传播。

论文使用的 symbolic state 与 reachability graph 是：

$$
(q, Z)
$$

以及

$$
S = (N, \rightarrow)
$$

其中：

1. `$q$` 是离散 automaton state。
2. `$Z$` 是 zone。
3. `$S$` 是从初始状态出发生成的 reachability graph。

为了把 timing problem 直接变成 reachability problem，论文再加入一个永不 reset 的辅助时钟：

$$
T
$$

此时所有不稳定状态上 `$T$` 的最大可达值就是最大稳定时间。也就是说，最大稳定时间问题被压成“在所有 unstable symbolic states 上取辅助时钟 `$T$` 的最大值”。

### 语义边界

1. 论文只处理无环组合电路，不处理一般时序反馈网络。
2. 输入被假定为在有限时间内至多变化一次。
3. delay model 采用 bi-bounded inertial delay，不覆盖所有电路延迟模型。
4. 抽象 automaton 是 over-approximation，因此目标是保守上界而不是精确最小值。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed circuit 骨架 | `$C=(V,\prec,F,I)$` | 带 delay 区间的布尔电路。 |
| delay 算子 | `$D_I:A\times S(A)\to 2^{S(A)}$` | 传播延迟的非确定性语义。 |
| 最大稳定时间 | `$\theta(C)=\max\{\theta(C,x,x'):x,x'\in X\}$` | 目标分析问题。 |
| timed automaton | `$A=(Q,C,I,\Delta)$` | 电路后端模型。 |
| reachability graph | `$S=(N,\rightarrow)$` | 提取可行 timing 行为。 |
| 子电路抽象 | `$L(\hat A)$` over-approximates projected `$L(A)$` | 以更小模型保守替换子电路。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | gate 的稳定 / 不稳定模式都显式建模。 |
| 事件 / 触发 | 中等支持 | 关键是输入翻转与输出稳定，不是消息交互。 |
| 守卫 / 数据 | 弱支持 | 主体是 clocks 与布尔逻辑，不是富数据。 |
| 层次 | 不适用 | 不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 各 gate automata 交互组成并发网络。 |
| 时间约束 | 很强 | 全部贡献都围绕 delay 区间与稳定时间。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 已落到 `IF/Kronos/Aldebaran` 工具链。 |

### 形式化问题与性质

1. 论文的关键不是“如何验证功能正确性”，而是“如何在保守前提下求最大稳定时间”。
2. timed automata 的优势体现在它能结合逻辑结构排除 static longest-path 中的 false paths。
3. 为了扩到更大电路，作者引入了基于 reachability graph 的子电路 over-approximation 和 minimization。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 给出布尔电路方程与每个 gate 的 delay 区间。
2. 自动生成 interacting timed automata。
3. 对子电路生成 reachability graph。
4. 从 graph 中提炼更小的抽象 automaton，再拼回整体分析链。

### 机器可处理承载方式

机器可处理承载方式包括：

1. Boolean equations with delays。
2. `IF` timed automata format。
3. reachability graph / symbolic states / zones。
4. minimization 后的 abstract automaton。

### 交换与互操作

1. 电路首先被翻译成 `IF`。
2. reachability 分析依托 `Kronos`。
3. 最后用 `Aldebaran` 做带可见 / 不可见迁移的 minimization。

## 配套基础设施

- 建模/编辑工具：电路方程输入与自动 timed-automata 生成器。
- 解析/交换/元模型支持：`IF` 作为中间承载格式。
- 仿真/执行支持：主体不是仿真，而是符号 reachability。
- 验证/分析支持：`Kronos`、`Aldebaran`、reachability graph、abstract automaton minimization。
- 代码生成/转换支持：不面向代码生成，重点是 timing analysis。
- 标准化或社区生态：嵌入的是早期 timed-automata / verification 工具链，而不是硬件行业通用 STA 格式。

## 适用场景与需求前提

### 适用场景

适合需要保守估计组合电路最大传播延迟、并且静态最长路径分析过于悲观的场景。

### 需求前提

1. 电路应是 acyclic combinational circuit。
2. 输入变化模式需要可限制为“每个输入在一轮内至多变化一次”。
3. gate delay 必须能写成上下界区间。
4. 团队接受以 timed automata 作为 timing-analysis 后端。

### 不适用或高成本场景

若电路包含复杂反馈、无限制输入振荡或需要精确的模拟级连续行为，这条路线就不合适。

## 与相邻形式主义的关系

它和普通 static timing analysis 的关键差异，是前者只算路径累积延迟，而本文把逻辑可达性也纳入 timing 判断。相对 timed Petri net 路线，它更直接落在 `Kronos` 这类 timed-automata 验证器上；相对后来的异步电路 timed-analysis 论文，它更像一个“把子电路抽象自动化”的早期工具型地基。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明 timed automata 的方法路线并不局限于软件控制器，还能覆盖硬件时序分析，因此有助于拓宽 `project_1` 对 timed-state-machine family 工具边界的理解。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，组合电路本身不是目标输出，但 `acyclic timed automata` 非常适合作为 timing-analysis 中间表示。

### 对需求到模型生成的启发

1. 若后续面对“逻辑结构 + 时间传播”的系统，单纯最长路径并不够，形式模型能提供更紧上界。
2. 子系统抽象成更小 automaton 后再回灌整体，是控制 timed-state explosion 的有效套路。
3. 工具链层面的 `IF -> Kronos -> Aldebaran` 说明“先统一到可分析自动机，再做后端优化”是可复用思路。

### 现实限制

论文自己也承认当前瓶颈是 reachability graph 的内存消耗，因此这更像方法证明与原型，而不是现成的工业规模 STA 替代品。

## 重要的相关工作

1. 论文明确把 timed automata 电路分析与 industry static timing analysis 做比较，突出 false-path 感知的优势。
2. 它与后来的异步电路 / timed Petri net timing-analysis 论文共享一条“硬件 timing -> symbolic model”路线。
3. `IF`、`Kronos`、`Aldebaran` 在这里共同构成了一个典型的早期 timed-verification 工具栈。

## 文献分类总结

- 这篇论文应归入：⏱️ 时间 / 时钟自动机
- 这篇论文应归入：🛠️ 方法路线
- 这篇论文应归入：🎛️ 控制 / 反应式逻辑
- 这篇论文应归入：⏱️ 实时与嵌入式系统
- 作为 `state_machine_types` 条目，它补的是 timed-automata 在电路 timing-analysis 上的硬件支线与 `Kronos` 异步 / 时序分析挂接口径。
