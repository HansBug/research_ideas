# MightyPPL：带过去与 Pnueli 模态的 MITL 验证 / MightyPPL: Verification of MITL with Past and Pnueli Modalities

## 基本信息

- 标题：MightyPPL: Verification of MITL with Past and Pnueli Modalities
- 中文标题：MightyPPL：带过去与 `Pnueli` 模态的 `MITL` 验证
- 作者：Hsi-Ming Ho，Shankara Narayanan Krishna，Khushraj Madnani，Rupak Majumdar，Paritosh Pandya
- 发表：arXiv 预印本，2025
- DOI：原文未提供
- 链接：https://arxiv.org/abs/2510.01490
- 形式主义：`MITPPL / timed automata / MightyPPL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`MITPPL -> timed automata` translator / backend bridge
- 工具/实现获取方式：原文明确给出仓库入口 `https://github.com/hsimho/MightyPPL`，并说明可独立使用，也可接入 `Uppaal / TChecker / LTSmin / MoniTAal / PARDIBAAL`。
- 标准/格式获取方式：主承载是 `MITPPL` 输入、`Uppaal` / `TChecker` 输出的标准 timed automata、以及工具内部的 component/product `TA`；它不是新的行业交换标准。

## 简报

这篇论文补的是 timed-logic 到 timed-automata 的基础设施线。它的关键点不是再做一个只支持未来算子的 `MITL` translator，而是把带过去算子和 `Pnueli` 模态的 `MITPPL` 直接翻成语言等价的 timed automata，并且兼容多个后端。更重要的是，它没有沿用 `MightyL` 那种重度重叠 obligation 编码，而是通过“非重叠 obligation + sequentialisation + symbolic letters”把状态爆炸压下去。

- 形式主义定位：`MITPPL` 到 timed automata 的验证基础设施，而不是新的 timed-automata 母型。
- 构造方式简述：`MITPPL formula -> tester/component automata -> product or flattened TA -> Uppaal/TChecker/LTSmin`。
- 基础设施与场景简述：依托 `MightyPPL`、`tester automata`、symbolic synchronization、`TChecker`、`Uppaal`、`LTSmin`，服务实时时序逻辑 satisfiability 与 model checking。

```text
MITPPL formula -> triggered tester automata -> obligation handling / sequentialisation -> standard timed automata -> backend verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `MITPPL`，即带过去与 `Pnueli` 模态的 `MITL`；
2. tester automata / component automata；
3. timed automata 同步乘积；
4. `MightyPPL` 命令行工具链。

### 核心抽象

论文把 `MTLPPL` / `MITPPL` 公式写成：

$$
\phi ::= \top \mid p \mid \neg \phi \mid \phi_1 \land \phi_2 \mid \phi_1 U_I \phi_2 \mid \phi_1 S_I \phi_2 \mid Pn_J(\phi_1,\dots,\phi_k) \mid \overleftarrow{Pn}_J(\phi_1,\dots,\phi_k)
$$

上式中的符号逐项解释如下：

1. `$p$` 是 atomic proposition。
2. `$U_I$` 是带时间区间 `$I$` 的 until。
3. `$S_I$` 是带时间区间 `$I$` 的 since。
4. `$Pn_J$` 与 `$\overleftarrow{Pn}_J$` 分别是未来和过去的 `Pnueli` 模态。

论文对 timed automata 使用如下骨架：

$$
A = \langle \Sigma, S, s_0, X, \Delta, F \rangle
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是字母表。
2. `$S$` 是 location 集合。
3. `$s_0$` 是初始位置。
4. `$X$` 是时钟集合。
5. `$\Delta \subseteq S \times \Sigma \times G(X) \times 2^X \times S$` 是边关系。
6. `$F$` 是广义 `Büchi` 接受条件。

定时词上的 `Pnueli` 语义写成：

$$
\rho, j \models Pn_J(\phi_1,\dots,\phi_k) \iff \exists i_k > \cdots > i_1 > j,\ \forall 1 \le n \le k,\ \tau_{i_n} - \tau_j \in J \land \rho,i_n \models \phi_n
$$

上式中的符号逐项解释如下：

1. `$\rho$` 是 timed word。
2. `$j$` 是当前位置。
3. `$J$` 是时间区间。
4. 该式要求未来存在一串按顺序出现的事件点，分别满足 `$\phi_1,\dots,\phi_k$`。

### 一个最小例子与通俗解释

论文的直觉例子非常清楚：

1. `req => ◇_[0,5] ack` 这类需求是普通 `MITL`。
2. “未来 10 个时间单位内依次发生 `lock1, lock2, lock3`”则更适合 `Pnueli` 模态。
3. `MightyPPL` 先把这些子公式拆成带 trigger 的 tester automata。
4. 再把多个 obligation 顺序化，最终输出标准 timed automata 给后端工具。

通俗地说，`MightyPPL` 就像“高级实时逻辑到 timed automata 的编译器”，把人更容易写的 `MITPPL` 规格翻成现有验证器更容易跑的 automata。

### 运行 / 接受 / 转移语义

论文给 timed automaton 的同步乘积：

$$
A_1 \times A_2 = \langle \Sigma, S_1 \times S_2, (s_0^1,s_0^2), X_1 \cup X_2, \Delta, F \rangle
$$

上式中的符号逐项解释如下：

1. `$A_1,A_2$` 是两个 timed automata。
2. 其 product 位置是二者位置对。
3. 时钟集合并集后共同演化。
4. `$J A_1 \times A_2 K = J A_1 K \cap J A_2 K$`。

论文的核心翻译目标可概括为：

$$
J \phi K = J C_\phi K
$$

上式中的符号逐项解释如下：

1. `$\phi$` 是待翻译的 `MITPPL` 公式。
2. `$C_\phi$` 是由 tester automata 同步积得到的最终 timed automaton。
3. 该式表示 automaton 与原公式在 timed words 上语言等价。

### 语义边界

1. 论文面向 pointwise / event-based timed-word semantics，不是 signal semantics。
2. 主线是 satisfiability 与 model checking，不是监控或 falsification。
3. 它支持 past 与 `Pnueli`，但仍然建立在 decidable `MITPPL` 片段上。
4. 最终输出是标准 timed automata，而不是 generalized/silent TA 的私有格式。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `MITPPL` 文法 | `$\phi ::= \top \mid p \mid \cdots \mid Pn_J(\cdot) \mid \overleftarrow{Pn}_J(\cdot)$` | 给出支持 past 与 `Pnueli` 的逻辑骨架。 |
| `Pnueli` 语义 | `$\rho,j \models Pn_J(\phi_1,\dots,\phi_k)$` | 说明顺序事件约束如何落到 timed words。 |
| `TA` 骨架 | `$A=\langle \Sigma,S,s_0,X,\Delta,F\rangle$` | 后端统一工作对象。 |
| 语言等价翻译 | `$J\phi K = J C_\phi K$` | 工具输出 automaton 与原逻辑规格等价。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 输出直接是标准 timed automata。 |
| 事件 / 触发 | 很强 | timed word 事件点与 trigger propositions 是核心。 |
| 守卫 / 数据 | 中等支持 | 侧重时钟约束与逻辑子公式，而非富数据更新。 |
| 层次 | 弱支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 通过 product automata 组合多个 tester / component automata。 |
| 时间约束 | 很强 | 支持一般区间、past、`Pnueli` 与 counting-like 模式。 |
| 连续动态 / 随机性 | 不支持 | 纯 timed-word / timed-automata 语义。 |
| 可执行 / 可验证性 | 很强 | 直接输出 `Uppaal` / `TChecker` 兼容模型。 |

### 形式化问题与性质

1. 它解决的是“更强实时逻辑如何落到现有 timed automata 验证生态”的问题。
2. 论文的关键优化是把 obligations 做成 bounded、identical、sequentialised component automata。
3. symbolic letters 与只构造 forward/backward reachable product 部分，是工程上非常关键的减爆点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `MITPPL` 公式；
2. finite / infinite-word 选择；
3. optional model `TA`（用于 model checking）；
4. 输出目标后端格式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `MITPPL` textual spec；
2. component tester automata；
3. flattened monolithic `TA`；
4. `Uppaal` / `TChecker` 格式输出。

### 交换与互操作

1. 工具既可输出 component mode，也可输出 flat mode。
2. `Uppaal` 输出可进一步接到 `LTSmin` 做多核检查。
3. 工具内部还可接 `MoniTAal` / `PARDIBAAL` fixpoint `DBM` 路线。

## 配套基础设施

- 建模/编辑工具：`MightyPPL` 命令行工具。
- 解析/交换/元模型支持：`MITPPL` parser、component/product `TA` 模板。
- 仿真/执行支持：主体依赖外部 `Uppaal / TChecker / LTSmin` 后端。
- 验证/分析支持：finite/infinite satisfiability、model checking、multi-core timed verification。
- 代码生成/转换支持：逻辑到标准 timed automata 的自动翻译。
- 标准化或社区生态：兼容 `Uppaal`、`TChecker`、`LTSmin`，仓库公开在 GitHub。

## 适用场景与需求前提

### 适用场景

适合那些自然语言需求里明显包含“过去条件”“计数型顺序约束”“未来若干步必须依次发生某串事件”的实时系统规格，以及希望继续复用现有 timed-automata backends 的场景。

### 需求前提

1. 需求应采用 pointwise timed-word 语义。
2. 系统或环境模型能最终与 timed automata 后端对接。
3. 使用者接受先做逻辑编译，再交给 `TA` 工具链完成验证。
4. 若做 model checking，需要把待验系统落成 `TA` 模型。

### 不适用或高成本场景

1. 信号语义、连续采样语义或非 `TA` 后端不在主支持范围内。
2. 若需求 heavily 依赖富数据变量更新，`MITPPL` 不是最自然的入口。
3. 若只需普通 `MITL`/unilateral fragment，使用更轻的工具可能成本更低。

## 与相邻形式主义的关系

相对 `MightyL`，本文补了 past 与 `Pnueli`，并改进了 obligation handling；相对 `TChecker` / `Uppaal`，它不是新的验证器，而是给它们喂更强逻辑规格的前端；相对文库中的 `KRONOS / UPPAAL 4.0 / Synthia / compRTMC`，它更像 timed-logic compiler，而不是 timed model checker 本体。

## 与本研究的关系

### 对 Project 1 的价值

它非常契合“需求到验证性质生成”这条主线。很多控制系统需求天然带过去约束、计数型顺序约束和复杂时间窗口，`MightyPPL` 说明这些性质不必手工压平到简单 `LTL/TCTL`，而可以先保留较高层逻辑，再自动翻成 timed automata 监视器。

### 可复用启发

1. 可把自然语言时序需求先抽成 `MITPPL` 风格模板，再统一编译成 observer `TA`。
2. obligation sequentialisation 的思想对“多子约束并行触发”的 monitor 构造很有参考价值。
3. 说明性质生成与系统建模可以分离：先产 property automata，再接现有 timed backend。

## 重要的相关工作

1. `MightyL`：本文最直接的前代工具与性能对照。
2. `Uppaal`、`TChecker`、`LTSmin`：本文的主要 verification backends。
3. `MITL / MTL / Q2MLO / unilateral TPTL`：构成其逻辑 expressiveness 背景。
4. tester automata 与 stratification 传统：构成本文 compositional translation 的方法前史。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这篇论文最适合作为“高级实时逻辑到 timed automata 的前端编译器与验证桥接”条目保留。它不引入新的 timed-automata 母型，但为复杂时序需求生成和 timed backend 复用提供了很强的基础设施证据。
