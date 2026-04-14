# 在时间自动机上检验 MITL 公式：一种基于逻辑的方法 / Model Checking MITL Formulae on Timed Automata: a Logic-Based Approach

## 基本信息

- 标题：Model Checking MITL Formulae on Timed Automata: a Logic-Based Approach
- 中文标题：在时间自动机上检验 MITL 公式：一种基于逻辑的方法
- 作者：Claudio Menghi，Marcello M. Bersani，Matteo Rossi，Pierluigi San Pietro
- 发表：*ACM Transactions on Computational Logic*，Vol. 21 No. 3，pp. 1-44，2020
- DOI：`10.1145/3383687`
- 链接：https://doi.org/10.1145/3383687
- 形式主义：`Timed Automata / MITL / CLTLoc / TACK`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：logic-based `TA + MITL -> CLTLoc` model-checking route with configurable semantics
- 工具/实现获取方式：原文明确给出 `TACK` 仓库 `https://github.com/claudiomenghi/TACK`、`QTLSolver` 仓库 `https://github.com/fm-polimi/qtlsolver`，并说明后端调用 `Zot`。
- 标准/格式获取方式：输入是与 `Uppaal` 兼容的 `Timed Automata` 网络和 `MITL` 公式；中间承载是 `CLTLoc` 公式，不是独立交换标准。

## 简报

这篇论文补的是 `Timed Automata` 验证里一条很有代表性的“逻辑中间层”路线。作者不再沿用“`MITL` 先翻成 timed automata，再和系统 automata 做乘积，然后做空性检查”的传统思路，而是把系统模型和性质公式都统一翻到 `CLTLoc`，再用 solver 决定可满足性。这样做的好处非常明确：可以切换不同 solver，可以替换不同 signal / synchronization / liveness semantics，也更容易加入新构造。

- 形式主义定位：围绕 `Timed Automata + MITL` 的验证方法路线，而不是新的时间自动机子类。
- 构造方式简述：`TA network` 与 `MITL` 性质分别翻译成 `CLTLoc`，再检查 `\Phi_{sig} \land \Phi_{\neg \psi}` 是否可满足。
- 基础设施与场景简述：依托 `TACK`、`QTLSolver`、`Zot`、signal-based semantics、`CLTLoc` 和 `Uppaal`-compatible front-end，服务可配置 timed verification。

```text
Timed Automata network + MITL property -> CLTLoc encoding -> solver -> satisfiable / unsatisfiable -> verification result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Timed Automata` 与带整数变量的扩展。
2. network of timed automata。
3. `MITL` on signals。
4. `CLTLoc` 中间逻辑。
5. `TACK` 工具链与可配置语义。

### 核心抽象

论文直接给出 `Timed Automaton` 定义：

$$
A = \langle AP, X, Act_\tau, Q, q_0, Inv, L, T \rangle
$$

上式中的符号逐项解释如下：

1. `$AP$` 是原子命题集合。
2. `$X$` 是 clocks 集合。
3. `$Act_\tau$` 是动作与空动作集合。
4. `$Q$` 是控制状态集合，`$q_0$` 是初始状态。
5. `$Inv$` 是 location invariants，`$L$` 是状态标注函数，`$T$` 是迁移集合。

论文进一步给出 network of timed automata：

$$
N = \{A_1, \ldots, A_K\}
$$

上式中的符号逐项解释如下：

1. `$A_1,\ldots,A_K$` 是多个 timed automata。
2. 它们共享原子命题、动作、变量与 clocks 语义背景。
3. 论文重点讨论网络级 signal semantics 和 synchronization。

`MITL` 语法在文中直接写成：

$$
\varphi ::= \alpha \mid \varphi \land \varphi \mid \neg \varphi \mid \varphi U_I \varphi
$$

上式中的符号逐项解释如下：

1. `$\alpha$` 是 atomic formula，可是原子命题或整数比较。
2. `$U_I$` 是带时间区间 `$I$` 的 until。
3. `$I$` 是非负实时间区间。
4. 这也是 timed requirements 的前端表达层。

### 一个最小例子与通俗解释

论文在背景部分给了一个很小的 timed automaton：

1. `q1` 带 invariant `x \le 5`。
2. 从 `q2` 回到 `q0` 的迁移要求 `x = 10`，并重置 `x`。
3. 若再加一个整数变量 `n`，不同迁移还可更新 `n := 0/1/2`。
4. `TACK` 不直接在这个模型上做传统 zone fixpoint，而是把位置、变量、时钟和 signal edges 都编码到 `CLTLoc`。

通俗地说，这套方法像“把时间自动机和时间逻辑都翻成同一种可求解逻辑语言”。这样一来，前端是 timed automata 还是稍微扩展过的 timed automata，后端是某个具体 solver 还是另一个 solver，二者都不再强绑定。

### 运行 / 接受 / 转移语义

论文给出的目标不是单台 automaton 的语言接受，而是 network 满足 `MITL` 性质。其最终验证判据可直接写成：

$$
N \models_T \psi
\iff
\Phi_{sig} \land \Phi_{\neg \psi}
\text{ 不可满足}
$$

上式中的符号逐项解释如下：

1. `$N$` 是 timed-automata 网络。
2. `$\psi$` 是 `MITL` 性质。
3. `$T$` 是由 liveness、synchronization 和 edge restrictions 组成的选择准则。
4. `$\Phi_{sig}$` 是系统 traces 映到 signals 后得到的 `CLTLoc` 表达。
5. `$\Phi_{\neg \psi}$` 是性质否定的 `CLTLoc` 编码。

论文还明确给出：

$$
\Phi_{sig} := \Phi_N \land \varphi_{sig}
$$

更完整地，在文中展开为：

$$
\Phi_{sig} := \varphi_N \land \varphi_l \land \varphi_s \land \varphi_{ef} \land \varphi_{sig}
$$

上式中的符号逐项解释如下：

1. `$\varphi_N$` 编码 automata 网络本身。
2. `$\varphi_l$` 编码 liveness conditions。
3. `$\varphi_s$` 编码 synchronization semantics。
4. `$\varphi_{ef}$` 编码 edge restrictions。
5. `$\varphi_{sig}$` 把 traces 绑定到 signals。

### 语义边界

1. 论文聚焦的是 `Timed Automata` 与 `MITL` 的 logic-based verification，而不是一般 hybrid systems。
2. 它强调 signal-based semantics，而不是仅沿用 timed words。
3. 主创新在中间逻辑与可配置语义，不是新的 timed-logic 本体。
4. 工具实现是 `TACK + Zot` 路线，不是经典 `KRONOS/UPPAAL` 的 zone fixpoint 路线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 元组 | `$A = \langle AP, X, Act_\tau, Q, q_0, Inv, L, T \rangle$` | 论文直接给出的 timed automaton 定义。 |
| automata 网络 | `$N = \{A_1, \ldots, A_K\}$` | 系统模型的基本单位。 |
| `MITL` 语法 | `$\varphi ::= \alpha \mid \varphi \land \varphi \mid \neg \varphi \mid \varphi U_I \varphi$` | timed requirements 前端。 |
| 系统信号公式 | `$\Phi_{sig} := \varphi_N \land \varphi_l \land \varphi_s \land \varphi_{ef} \land \varphi_{sig}$` | 把 traces / semantics 压成中间逻辑。 |
| 验证判据 | `$N \models_T \psi \Leftrightarrow \Phi_{sig} \land \Phi_{\neg \psi}$ 不可满足` | logic-based model checking 的最终判定。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 network of timed automata。 |
| 事件 / 触发 | 很强 | 支持多种 synchronization primitives。 |
| 守卫 / 数据 | 很强 | 支持整数变量与相关比较表达式。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 很强 | network semantics 和 synchronization encoding 是主轴之一。 |
| 时间约束 | 很强 | `MITL`、signal semantics、`CLTLoc` clocks 全是核心。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic line。 |
| 可执行 / 可验证性 | 很强 | `TACK` 已落成 Java 工具，且后端 solver 可替换。 |

### 形式化问题与性质

1. 这篇论文真正补的是“中间逻辑层”而不是单一 solver。
2. 可配置 semantics 很重要，因为实际 timed verification 往往不止一种同步 / 边界解释。
3. 它为 `TACK` 这条 timed-logic compiler / verifier 路线提供了很稳定的挂钩。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Uppaal` 兼容语法的 timed-automata 网络。
2. `MITL` 公式。
3. liveness / synchronization / edge 语义选择。
4. `TACK` front-end 与 `CLTLoc` backend。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `CLTLoc` 公式。
2. atomic propositions 与 integer predicates 的 signal atoms。
3. `TACK` 生成的 solver 输入。
4. `Zot` / `QTLSolver` 消费的逻辑约束。

### 交换与互操作

互操作重点在“中间层解耦”：

1. 前端 timed automata 可保持 `Uppaal` 兼容语法。
2. 中间层统一到 `CLTLoc`。
3. 后端 solver 可根据需要替换，而不必重写前端建模语言。

## 配套基础设施

- 建模/编辑工具：`TACK` 提供 timed-automata 网络和 `MITL` 性质的 front-end。
- 解析/交换/元模型支持：`Uppaal`-compatible syntax、`CLTLoc` 中间层、signal predicates。
- 仿真/执行支持：主线不是 simulation，而是 automated satisfiability-based verification。
- 验证/分析支持：`MITL` model checking、signal semantics、多种同步和 liveness 配置。
- 代码生成/转换支持：重点是 `TA + MITL -> CLTLoc -> solver language` 的逻辑转换。
- 标准化或社区生态：`TACK`、`QTLSolver`、`Zot`、`Uppaal` 和 timed-logic verification 社区。

## 适用场景与需求前提

### 适用场景

适合需要 `MITL` 级实时时序性质、希望调整信号语义 / 同步语义、或者希望将 timed verification 解耦到不同 solver 的场景。

### 需求前提

1. 系统需能表示成 finite network of timed automata。
2. 性质需能写成 `MITL` 或近似 `MITL`。
3. 团队接受 signal-based semantics 与 solver-based verification。
4. 若要扩展新构造，最好能把它们编码成额外 `CLTLoc` 公式。

### 不适用或高成本场景

如果目标只是最标准的 `Uppaal` reachability，且不需要 `MITL`、可配置 semantics 或 solver decoupling，这条路线可能显得过重。

## 与相邻形式主义的关系

相对 [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)，后者是在 `TACK` 里继续把 `TA` 侧编码直接改成 `SMT`，本文则是更早、更通用的 `TA + MITL -> CLTLoc` 路线；相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，`KRONOS` 是 zone / fixpoint 型 verifier，本文是 logic-based verifier；相对 [mightyppl-verification-of-mitl-with-past-and-pnueli-modalities/desc.md](../mightyppl-verification-of-mitl-with-past-and-pnueli-modalities/desc.md)，`MightyPPL` 更偏 stronger timed logic 到 timed automata 的编译器，而本文把系统和性质一起压到 `CLTLoc`。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常适合作为 `project_3` 乃至 `project_1` 的验证后端参考，因为它清楚展示了“模型 + 性质 + 语义开关”三者如何系统化编码。
2. 也提示我们：若未来由 LLM 生成 timed models，最好同步生成结构化 timed properties，而不是只生成 reachability queries。
3. `CLTLoc` 这种中间层思路对“生成 - 验证 - 修复”闭环尤其有启发。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Timed Automata` 可以是目标形式主义，而 `MITL / CLTLoc / TACK` 更像验证侧的中间表示与方法后端。

### 对需求到模型生成的启发

1. 自然语言中的 deadline、within、until、always eventually 等时序词非常适合抽成 `MITL`。
2. 生成模型时就要考虑同步语义和边界语义，否则验证阶段很难自动接轨。
3. 若工具链允许更换 solver，后续修模实验会更灵活。

## 重要的相关工作

1. [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)：`TACK` 后续的 `TA2SMT` 改进路线。
2. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：经典 timed symbolic checker。
3. [mightyppl-verification-of-mitl-with-past-and-pnueli-modalities/desc.md](../mightyppl-verification-of-mitl-with-past-and-pnueli-modalities/desc.md)：timed logic 到 timed automata 的另一条前端路线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / MITL / CLTLoc / TACK`
- 论文角色：logic-based `TA + MITL -> CLTLoc` model-checking route with configurable semantics
- 核心功能：把 timed-automata 网络和 `MITL` 性质统一压到 `CLTLoc` 并用 solver 完成验证
- 关键特性：signal semantics、`CLTLoc` 中间层、solver decoupling、可配置同步 / liveness / edge 语义
- 构造方式：`TA network + MITL -> CLTLoc -> satisfiability check`
- 基础设施：`TACK`、`QTLSolver`、`Zot`、`Uppaal`-compatible front-end
- 适用场景：需要 `MITL`、可配置语义或 solver 可替换的实时系统验证
- 需求前提：系统需落成 finite `TA` network，性质可写成 `MITL`
- 状态：🟢
