# NuSMV 2：开源符号模型检查工具 / NuSMV 2: An OpenSource Tool for Symbolic Model Checking

## 基本信息

- 标题：NuSMV 2: An OpenSource Tool for Symbolic Model Checking
- 中文标题：NuSMV 2：开源符号模型检查工具
- 作者：Alessandro Cimatti，Edmund Clarke，Enrico Giunchiglia，Fausto Giunchiglia，Marco Pistore，Marco Roveri，Roberto Sebastiani，Armando Tacchella
- 发表：*Computer Aided Verification (CAV 2002)*，pp. 359-364，2002
- DOI：`10.1007/3-540-45657-0_29`
- 链接：https://doi.org/10.1007/3-540-45657-0_29
- 形式主义：`Synchronous Transition Systems / SMV / NuSMV`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：open-source symbolic model checker with unified `BDD`/`SAT` backend architecture
- 工具/实现获取方式：原文明确给出 `NuSMV` 站点 `http://nusmv.irst.itc.it/`，并说明从 `NuSMV2` 开始按开源方式发布。
- 标准/格式获取方式：原文主体围绕 `SMV` 语言、内部 `RBC/CNF` 承载和 `DIMACS` 导出；它是验证工具链承载，不是中立交换标准。

## 简报

这篇论文的关键贡献，不是再造一种新的状态机，而是把 `SMV` 风格同步转移系统的验证平台重新组织成一个真正可扩展的开源内核。`NuSMV 2` 在保留 `BDD` 路线的同时，把 `SAT`-based bounded model checking 接入同一代码基，并把 parsing、flattening、boolean encoding、cone-of-influence、trace reconstruction 等公共前处理抽出来，形成了后续很多 symbolic backend 的典型架构。

- 形式主义定位：面向 `SMV` 同步/异步模块描述的 symbolic verification infrastructure。
- 构造方式简述：先把模块化 `SMV` 模型做 flattening 和 boolean encoding，再按性质选择 `BDD` 有限状态机或 `SAT` 有界编码。
- 基础设施与场景简述：依托 `BDD` package、`RBC` engine、内部/外部 `SAT` solver、`DIMACS` printer 与 trace/simulation 子系统，服务 `CTL/LTL` 验证、reachability 与技术转移场景。

```text
SMV modules/processes -> flattening -> boolean encoding -> COI reduction -> BDD FSM or RBC/CNF -> verification / counterexample / simulation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `SMV` 模块化模型与属性集合。
2. flattening 后的 flat model。
3. boolean encoding 后的 boolean model。
4. `BDD`-based finite-state machine。
5. `SAT`-based bounded model checking 编码。

### 核心抽象

论文直接把输入写成模型 `M` 与性质集合 `P_1,\ldots,P_n`。可保守整理为：

$$
M = (V, I(V), T(V,V'))
$$

上式中的符号逐项解释如下：

1. `V` 是模型变量集合。
2. `I(V)` 是初始条件。
3. `T(V,V')` 是当前状态到下一状态的同步转移关系。
4. 论文说明 `SMV` 文件经过模块实例化与变量布尔化后，最终都归约到这个 finite-state symbolic core。

论文还显式区分了前处理后的多个层级：

$$
M \rightarrow M_f \rightarrow M_{fb}
$$

上式中的符号逐项解释如下：

1. `M` 是原始模块化模型。
2. `M_f` 是 flattening 后的扁平模型，每个变量都获得绝对名。
3. `M_{fb}` 是 boolean encoding 后的布尔模型。
4. 这正是原文图 1 和正文里给出的处理流水线。

对 `SAT`-based bounded model checking，原文的工作形态可以整理为：

$$
I(s_0) \land \bigwedge_{0 \le i < k} T(s_i,s_{i+1}) \land \neg \varphi_k
$$

上式中的符号逐项解释如下：

1. `s_0,\ldots,s_k` 是长度为 `k` 的候选路径。
2. `I(s_0)` 要求路径起于初始状态。
3. `T(s_i,s_{i+1})` 约束每一步满足系统转移关系。
4. `\varphi_k` 是在第 `k` 步实例化后的性质条件。
5. 论文明确说明：若该公式可满足，则得到原模型检查问题的 counterexample。

### 一个最小例子与通俗解释

一个最小例子可以用论文里的处理流程来理解：

1. 用户写一个包含 `MODULE`、`process`、布尔或标量变量的 `SMV` 模型。
2. 再写一个 `CTL` 或 `LTL` 性质。
3. `NuSMV 2` 先展开模块、再把标量编码成布尔变量。
4. 如果选 `BDD` 路线，就构建有限状态机后做 reachability / `CTL` / `LTL`；如果选 `SAT` 路线，就把 bounded problem 编成 `CNF` 交给 solver。

通俗地说，`NuSMV 2` 像一个“验证编译器前端 + 多后端执行器”。你写的是模块化状态机和时序性质，工具把它压成不同的 symbolic backend 可吃的格式，再把结果和反例还原回模型层。

### 运行 / 接受 / 转移语义

对 `BDD` 路线，原文强调最终构造的是布尔有限状态机，因此一步执行可写成：

$$
s' \models T(s,s')
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态赋值。
2. `s'` 是下一状态赋值。
3. `T` 是由 `SMV` 的 `next` 语义和模块展开共同得到的布尔转移关系。
4. 一旦 `BDD` 有限状态机建好，就可在其上做 reachability、fair `CTL` 和 `LTL` 检查。

对 `LTL` bounded model checking，接受语义则退化为“是否存在某条长度受限的违例路径”，即上文的 `SAT` 公式是否可满足。

### 语义边界

1. `NuSMV 2` 的主体是验证平台，不是新的状态机母型。
2. 它主要服务 finite-state symbolic checking；本文尚未进入 `nuXmv` 那种完整 infinite-state `SMT` 扩展。
3. 模型表达以 `SMV` 文本语言和同步转移关系为核心，不是图形层次状态图工具。
4. `SAT` 路线当时主要覆盖 bounded `LTL` model checking，并不是所有性质都交给 `SAT` 求解。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$M = (V, I(V), T(V,V'))$` | `NuSMV 2` 最终处理的是 finite-state symbolic transition system。 |
| 前处理层级 | `$M \rightarrow M_f \rightarrow M_{fb}$` | 模块化模型依次经过 flattening 和 boolean encoding。 |
| 单步语义 | `$s' \models T(s,s')$` | `BDD` 路线上的核心状态机语义。 |
| BMC 编码 | `$I(s_0) \land \bigwedge_{i<k} T(s_i,s_{i+1}) \land \neg \varphi_k$` | `SAT` 路线通过 bounded encoding 找 counterexample。 |
| COI reduction | `$M_{fb}(P_i)$` | 每个性质只保留其相关的模型部分。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 finite-state symbolic transition systems。 |
| 事件 / 触发 | 中等支持 | 通过 `SMV` 模块和转移关系表达，不强调显式事件端口。 |
| 守卫 / 数据 | 中等支持 | 标量数据会先经过 boolean encoding。 |
| 层次 | 不支持 | 不是层次状态图工作台。 |
| 并发 / 同步 | 强 | `modules/processes` 支持同步与异步组合。 |
| 时间约束 | 弱支持 | 本文不是专用 timed-automata 平台。 |
| 连续动态 / 随机性 | 不支持 | 主对象仍是有限离散 symbolic verification。 |
| 可执行 / 可验证性 | 很强 | `BDD` 与 `SAT` 两路 symbolic engine 已工程化集成。 |

### 形式化问题与性质

1. 论文真正补的是“同一个 `SMV` 模型怎样被公共前处理层送入不同 symbolic engines”。
2. `flattening + boolean encoding + COI` 是它最重要的工程抽象。
3. 从状态机谱系看，它是 `SMV`/symbolic backend 基础设施线的典型锚点。

## 构造方式与承载格式

### 建模入口

论文给出的主要入口有：

1. `SMV` 语言文件。
2. `CTL/LTL` 性质集合。
3. batch 模式或交互式 shell。

### 机器可处理承载方式

机器可处理承载方式包括：

1. flattening 后的 flat model。
2. boolean encoding 后的 boolean model。
3. `BDD`-based FSM。
4. `RBC` 和 `CNF/DIMACS`。

### 交换与互操作

互操作重点不在中立标准，而在 symbolic backend 桥接：

1. `RBC -> CNF -> SAT solver`。
2. `DIMACS` 导出。
3. traces 的重建与仿真。

## 配套基础设施

- 建模/编辑工具：主体是 `SMV` 文本建模和交互式 shell。
- 解析/交换/元模型支持：parser、flattening、boolean encoding、`DIMACS` printer。
- 仿真/执行支持：trace manipulation 与 simulation 子系统。
- 验证/分析支持：reachability、fair `CTL`、`LTL`、bounded model checking、定量分析。
- 代码生成/转换支持：支持输出 `DIMACS`，并可接外部 `SAT` solver。
- 标准化或社区生态：`NuSMV` 开源项目、`BDD` package、内部 `SIM` 与外部 `SAT` solvers 共同构成生态。

## 适用场景与需求前提

### 适用场景

适合有限状态同步/异步控制逻辑、协议、嵌入式软件和需要 `CTL/LTL` symbolic checking 的模型。

### 需求前提

1. 模型需能写成 `SMV` 模块和有限状态更新。
2. 若使用 `SAT` 路线，关注点主要是 bounded `LTL` counterexample search。
3. 团队愿意接受文本建模与 symbolic verification 工作流。

### 不适用或高成本场景

如果需求主体是 rich real-time clocks、连续动力学或图形化 statechart authoring，`NuSMV 2` 就不是最自然的主入口。

## 与相邻形式主义的关系

相对 [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)，本文是更早的 `BDD/SAT` 双路 symbolic core 锚点；相对 [sal-2/desc.md](../sal-2/desc.md)，`SAL 2` 更强调多 analyzer 和 infinite-state extension，而 `NuSMV 2` 更聚焦 `SMV` symbolic kernel 重构；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`LTSmin` 是 language-independent backend，而本文是 `SMV`-centered backend 本体。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“先把状态机压成统一转移系统骨架，再对接多种 symbolic backend”是一条非常稳的工程路线。
2. 对后续 `project_1` 的生成-验证闭环来说，`flattening`、布尔化和 counterexample reconstruction 都很值得借鉴。
3. 如果生成目标不是图形 DSL，而是验证中间表示，那么 `SMV/NuSMV` 这条线有直接参考价值。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更适合作为 verification-oriented 中间表示或后端，而不是最终面向用户的状态机交付语言。

## 重要的相关工作

- [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)：`NuSMV -> nuXmv` 演化后的 modern symbolic backend。
- [sal-2/desc.md](../sal-2/desc.md)：另一条以 scriptable analyzers 为核心的 symbolic analysis line。
- [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)：language-independent backend 方向的对照条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇典型的 symbolic model-checking infrastructure 条目，适合作为 `SMV` 前端、`BDD/SAT` 双后端和 verification-oriented 中间表示流水线的基础证据入账。
