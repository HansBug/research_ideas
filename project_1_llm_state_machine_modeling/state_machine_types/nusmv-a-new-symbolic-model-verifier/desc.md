# NuSMV：新一代符号模型验证器 / NuSMV: A New Symbolic Model Verifier

## 基本信息

- 标题：NuSMV: A New Symbolic Model Verifier
- 中文标题：NuSMV：新一代符号模型验证器
- 作者：Alessandro Cimatti，Edmund Clarke，Fausto Giunchiglia，Marco Roveri
- 发表：*Computer Aided Verification (CAV 1999)*，LNCS 1633，pp. 495-499，1999
- DOI：`10.1007/3-540-48683-6_44`
- 链接：https://doi.org/10.1007/3-540-48683-6_44
- 形式主义：`Synchronous Transition Systems / SMV / NuSMV`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：reengineered `SMV` symbolic model-checking platform
- 工具/实现获取方式：原文明确给出历史入口 `http://nusmv.irst.itc.it/`，并说明该平台由 CMU 与 IRST 联合开发，定位为开放、可维护、可技术转移的符号模型检查器。
- 标准/格式获取方式：主体承载是 `SMV` 文本语言、flattening 后的 flat model、布尔编码后的 transition relation 与 `BDD` backend；它不是中立交换标准。

## 简报

这篇论文的重点，不是重新定义状态机，而是把经典 `SMV` 验证器重构成一个更开放、可扩展、可交互的 symbolic verification platform。相对老版本 `SMV`，`NuSMV` 在 1999 这篇工具论文里已经明确补出三条工程主线：交互式 shell 与 GUI、改进的模型分区与 `BDD` 内核、以及基于 tableau 的 `LTL` model checking。

- 形式主义定位：面向 `SMV` 同步/异步模块模型的 symbolic verification infrastructure。
- 构造方式简述：`SMV` 输入先解析、flatten、布尔化，再构造 `BDD`-based finite-state machine 并执行 reachability、`CTL`、`LTL` 等检查。
- 基础设施与场景简述：依托 `SMV` 语言、交互式 shell、GUI、外部 `BDD` package 与 counterexample/simulation 子系统，服务协议、控制逻辑和嵌入式软件验证。

```text
SMV modules/processes -> flattening -> boolean encoding -> BDD FSM -> CTL/LTL checking -> counterexample / simulation / GUI inspection
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `SMV` 模块化模型。
2. flattening 后的 flat model。
3. boolean encoding 后的 symbolic transition system。
4. `BDD`-based finite-state machine。
5. `CTL/LTL` model-checking 与 counterexample 设施。

### 核心抽象

原文虽然是工具论文，但其核心对象仍可保守整理成有限状态转移系统：

$$
M = (V, I(V), T(V,V'))
$$

上式中的符号逐项解释如下：

1. `V` 是状态变量集合。
2. `I(V)` 是初始条件。
3. `T(V,V')` 是当前状态到下一状态的转移关系。
4. 论文说明 `SMV` 模块在 flattening 与布尔化之后，最终都会被压到这个 symbolic core。

论文还显式给出前处理流水线，可整理为：

$$
M \rightarrow M_f \rightarrow M_{fb}
$$

上式中的符号逐项解释如下：

1. `M` 是原始模块化模型。
2. `M_f` 是 flattening 后、变量带绝对名的扁平模型。
3. `M_{fb}` 是 boolean encoding 后的布尔模型。
4. 这正是原文将 parser、flattening 与 boolean encoding 分离成独立模块的工程骨架。

对 `LTL` 检查，论文说明它采用 tableau construction 与 `CTL` checking 结合的路线，可保守压成：

$$
M \models \varphi_{LTL} \iff \mathcal{P}(M,\neg \varphi_{LTL}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `\varphi_{LTL}` 是待验证的 `LTL` 性质。
2. `\mathcal{P}(M,\neg \varphi_{LTL})` 表示把系统与性质反式 tableau 组合后的违例搜索对象。
3. 若其空，则原模型满足该性质。
4. 这是对原文“tableau constructor + standard CTL model checking”描述的保守整理。

### 一个最小例子与通俗解释

一个最小例子可以按论文主流程理解：

1. 用户写一个 `SMV` 文件，里面定义若干布尔/枚举变量和 `next` 更新规则。
2. 工具先把模块结构展开，再把枚举变量布尔化。
3. 然后用 `BDD` 表示可达状态集与转移关系。
4. 若某条 `CTL` 或 `LTL` 性质失败，工具给出反例并允许在 shell 或 GUI 中回看。

通俗地说，`NuSMV` 像“把文本状态机语言编译成 `BDD` 可吃的状态图内核，再把 model checking 包在一套交互式工作台里”。它比旧 `SMV` 更像工程平台，而不只是一次性求解器。

### 运行 / 接受 / 转移语义

在 `BDD` 路线下，一步语义可写成：

$$
s' \models T(s,s')
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态赋值。
2. `s'` 是下一状态赋值。
3. `T` 是由 `SMV` 的赋值语句、同步/异步进程与 fairness 约束共同决定的转移关系。
4. 工具的 reachability 与 `CTL/LTL` 检查都建立在这套 symbolic transition relation 上。

论文也强调了 partitioning 对 symbolic execution 的重要性，可保守写成：

$$
T = \bigwedge_{i=1}^{n} T_i
$$

其中：

1. `T_i` 是某个模块或赋值片段导出的局部 transition cluster。
2. 改进的 model partitioning 旨在降低 `BDD` 操作代价。
3. 这也是 `NuSMV` 相对旧 `SMV` 的关键工程增强之一。

### 语义边界

1. 这篇条目是 1999 年的 `NuSMV` 起点论文，不包含后来的 `SAT`-based BMC 和 `SMT` 扩展。
2. 主对象是有限状态 symbolic verification，不是 timed / probabilistic / hybrid family。
3. 建模入口仍是 `SMV` 文本语言，而不是图形 statechart。
4. 文章篇幅较短，重点是平台结构与增量功能，不是完整理论手册。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| symbolic 模型骨架 | `$M = (V, I(V), T(V,V'))$` | `NuSMV` 最终处理的是有限状态 symbolic transition system。 |
| 前处理层级 | `$M \rightarrow M_f \rightarrow M_{fb}$` | 模块化模型先扁平化，再布尔化。 |
| 单步语义 | `$s' \models T(s,s')$` | `BDD` backend 上的基本状态转移条件。 |
| `LTL` 违例检查 | `$M \models \varphi_{LTL} \iff \mathcal{P}(M,\neg \varphi_{LTL}) = \emptyset$` | `LTL` 支持通过 tableau + symbolic checking 实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 finite-state symbolic transition systems。 |
| 事件 / 触发 | 中等支持 | 主要经 `SMV` 更新语句与进程执行体现。 |
| 守卫 / 数据 | 中等支持 | 标量会布尔化，复杂数据并非主线。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 强支持 | `SMV` 模块与 processes 提供组合表达。 |
| 时间约束 | 不支持 | 非 timed platform。 |
| 连续动态 / 随机性 | 不支持 | 主线是离散 symbolic checking。 |
| 可执行 / 可验证性 | 很强 | reachability、`CTL`、`LTL`、反例与交互式检查都已打通。 |

### 形式化问题与性质

1. 论文真正补的是“开放、模块化的 `SMV` symbolic verification platform”。
2. `flattening + boolean encoding + BDD partitioning` 是它最重要的工程骨架。
3. 它是文库中 `SMV/NuSMV/nuXmv` symbolic backend 母线的更早锚点。

## 构造方式与承载格式

### 建模入口

论文中的主要建模入口是：

1. `SMV` 文本模型。
2. `CTL/LTL` 性质。
3. batch 命令行、交互式 shell 与 GUI。

### 机器可处理承载方式

机器可处理承载方式包括：

1. flat model。
2. boolean model。
3. `BDD`-based finite-state machine。
4. trace / counterexample objects。

### 交换与互操作

互操作重点不在中立交换格式，而在平台内模块解耦：

1. parser、flattening、boolean encoding、checking 相互解耦。
2. `BDD` package 被外部化进系统内核。
3. GUI 与 shell 共用同一 symbolic backend。

## 配套基础设施

- 建模/编辑工具：`SMV` 文本建模、交互式 shell 与 GUI。
- 解析/交换/元模型支持：parser、flattening、boolean encoding 与 model partitioning。
- 仿真/执行支持：counterexample browsing、simulation 与交互式参数调优。
- 验证/分析支持：reachability、fair `CTL`、`LTL` checking 与定量特征计算。
- 代码生成/转换支持：主体不是代码生成；重点是 symbolic internal representation。
- 标准化或社区生态：历史站点、开放结构、外部 `BDD` package 与后续 `NuSMV 2/nuXmv` 生态共同构成延续。

## 适用场景与需求前提

### 适用场景

适合有限状态控制逻辑、协议与反应式软件的 symbolic verification，尤其适合已经有 `SMV` 文本建模习惯、并需要 `CTL/LTL` 反例与交互式分析的团队。

### 需求前提

1. 模型需能写成 `SMV` 有限状态模块或进程。
2. 关键性质以 `CTL/LTL` 为主，而不是实时时钟或概率代价。
3. 团队愿意接受文本化 symbolic verification workflow。

### 不适用或高成本场景

如果需求主体是显式时钟、连续动力学、图形状态图或概率实时分析，这篇条目的直接收益会明显下降。

## 与相邻形式主义的关系

相对 [nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md](../nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md)，本文是更早的起点版本，重点仍在 `BDD` symbolic kernel、GUI 与 `LTL` 增量；相对 [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)，它还没有进入 `SMT/infinite-state` 时代；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`NuSMV` 是 `SMV`-centered 平台，而 `LTSmin` 是 language-independent backend。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“先把状态机压成统一 symbolic transition system，再挂多个分析器”是一条很早就被验证过的稳定工程路线。
2. 对 `project_1` 的生成-验证闭环来说，`flattening`、布尔化和反例回放都很有参考价值。
3. 若未来要把 LLM 生成结果送入验证后端，`SMV/NuSMV` 这条线是很直接的中间表示候选。

### 作为目标形式主义还是中间表示

更像 verification-oriented 中间表示与后端平台，而不是最终交付给领域工程师的前端状态机语言。

### 对需求到模型生成的启发

1. 若需求主要是布尔控制与时序性质，可以优先考虑压成 `SMV` 风格结构，而不必强行上图形 DSL。
2. 把“可解释的前处理层”单独做出来，比直接把一切硬编码进验证器更利于闭环修复。

### 现实限制

这篇文章篇幅较短，更多展示平台骨架与工程重构目标；若需要完整语义细节，仍需结合后续 `NuSMV 2` 和 `nuXmv` 条目一起阅读。

## 重要的相关工作

1. [nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md](../nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md)：`NuSMV` 的后续开源平台化版本。
2. [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)：`NuSMV` 向更现代 symbolic / `SMT` backend 的演化。
3. [sal-2/desc.md](../sal-2/desc.md)：与 `NuSMV` 相邻的 symbolic verification platform。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
