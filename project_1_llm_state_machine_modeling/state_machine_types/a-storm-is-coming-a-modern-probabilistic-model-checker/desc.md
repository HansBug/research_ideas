# Storm：现代概率模型检查器 / A Storm is Coming: A Modern Probabilistic Model Checker

## 基本信息

- 标题：A Storm is Coming: A Modern Probabilistic Model Checker
- 中文标题：Storm：现代概率模型检查器
- 作者：Christian Dehnert，Sebastian Junges，Joost-Pieter Katoen，Matthias Volk
- 发表：*Computer Aided Verification*，pp. 592-600，2017
- DOI：`10.1007/978-3-319-63390-9_31`
- 链接：https://doi.org/10.1007/978-3-319-63390-9_31
- 形式主义：`probabilistic models / Storm`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：面向概率模型检查的多引擎、多输入格式与多求解器平台
- 工具/实现获取方式：原文明确把 `Storm` 作为公开发布的 probabilistic model checker，并描述 command-line、C++ API 与 Python API 三种接口。
- 标准/格式获取方式：核心承载是 `Prism` 输入、`JANI`、显式转移格式、GSPN、DFT 与 pGCL 前端，以及 sparse/MTBDD engines 与 solver interfaces。

## 简报

这篇论文的关键贡献，不是提出一个新的概率自动机家族，而是把概率模型检查做成一个真正模块化的平台。`Storm` 在同一套基础设施里统一了 `DTMC/CTMC/MDP/MA`、`Prism/JANI/GSPN/DFT/pGCL` 多种前端、sparse 与 MTBDD 多种引擎、线性方程 / Bellman / MILP / SMT 多种求解器，以及 command-line / C++ / Python 三层接口。

- 形式主义定位：概率模型检查平台与工具基础设施，不是新的单体状态机语言。
- 构造方式简述：先从 `Prism/JANI/GSPN/DFT/pGCL` 等输入建模，再按目标任务选择 sparse、`dd`、`hybrid` 或 abstraction-refinement engine，并调度合适 solver。
- 基础设施与场景简述：依托多输入格式、可插拔 engines/solvers、counterexample/permissive scheduler/parametric backend 与 Python API，服务概率验证、反例生成、参数分析和 benchmark workflow。

```text
Prism / JANI / GSPN / DFT / pGCL -> model builder / engines -> linear or Bellman or MILP or SMT solvers -> probabilities / rewards / counterexamples / schedulers
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 支持的概率模型族。
2. 输入建模语言与显式模型格式。
3. sparse / decision-diagram / abstraction-refinement engines。
4. 线性方程、Bellman、MILP、SMT 等 solver interfaces。
5. 命令行、C++ API 与 Python API。

### 核心抽象

按论文架构，`Storm` 可保守压成：

$$
\mathrm{Storm} = (\mathcal{M}, \mathcal{L}, \mathcal{E}, \mathcal{S}, \mathcal{A})
$$

上式中的符号逐项解释如下：

1. `\mathcal{M}` 是支持的模型类型集合。
2. `\mathcal{L}` 是输入语言与格式集合。
3. `\mathcal{E}` 是 engines 集合。
4. `\mathcal{S}` 是 solver interfaces 与其实现集合。
5. `\mathcal{A}` 是面向用户和开发者的接口集合。
6. 这是基于论文工具架构做的保守整理，不是原文显式统一元组。

论文对模型族支持范围可直接整理为：

$$
\mathcal{M} = \{\mathrm{DTMC}, \mathrm{CTMC}, \mathrm{MDP}, \mathrm{MA}\}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间马尔可夫链。
2. `CTMC` 是连续时间马尔可夫链。
3. `MDP` 是马尔可夫决策过程。
4. `MA` 是 Markov automata，也是文中最丰富的模型类。

论文对输入族也给得很清楚：

$$
\mathcal{L} = \{\mathrm{Prism}, \mathrm{JANI}, \mathrm{GSPN}, \mathrm{DFT}, \mathrm{pGCL}, \mathrm{Explicit}\}
$$

上式中的符号逐项解释如下：

1. `Prism` 是经典概率建模语言。
2. `JANI` 是中立交换格式。
3. `GSPN`、`DFT`、`pGCL` 是 Storm 提供专门建模支持的几类前端。
4. `Explicit` 指显式枚举转移的输入格式。

引擎层则可压成：

$$
\mathcal{E} = \{\mathrm{sparse}, \mathrm{exploration}, \mathrm{dd}, \mathrm{hybrid}, \mathrm{abstraction\mbox{-}refinement}\}
$$

上式中的符号逐项解释如下：

1. `sparse` 是稀疏矩阵引擎。
2. `exploration` 是带学习式 state-space exploration 的稀疏引擎。
3. `dd` 纯用 decision diagrams。
4. `hybrid` 混用 MTBDD 与 sparse matrices。
5. `abstraction-refinement` 把离散时间模型抽象成 stochastic games 再自动细化。

### 一个最小例子与通俗解释

一个最小直觉例子可以是：

1. 用 `Prism` 或 `JANI` 写一个带奖励的 `DTMC/MDP`。
2. `Storm` 读取模型后，挑一套合适的 engine 与 solver。
3. 用户问的是 reachability probability、expected reward 或 counterexample。
4. 工具返回的不只是概率值，还可能是高层反例、permissive scheduler 或 exact result。

通俗地说，`Storm` 像一个“概率模型检查操作系统”。同一个前端模型，可以换不同引擎、不同求解器、不同 API，而不需要每次重写一套工具。

### 运行 / 接受 / 转移语义

论文的语义重点不是再定义单个模型的转移规则，而是工具如何承载这些模型：

1. sparse 引擎偏向标准显式数值解法。
2. `dd/hybrid` 引擎偏向 MTBDD 驱动的符号化表示。
3. abstraction-refinement 引擎把可能无限的离散时间模型抽象成 stochastic games。
4. solver 层把线性方程、Bellman、MILP、SMT 等任务统一接口化。

### 语义边界

边界也很明确：

1. `Storm` 是概率模型检查平台，不是统一的单一 DSL。
2. 2017 版并不覆盖 `Prism` 的全部能力，例如 probabilistic timed automata、multi-objective checking 等。
3. 强项在模块化基础设施和性能，不在单一建模语法创新。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 平台骨架 | `$\mathrm{Storm} = (\mathcal{M}, \mathcal{L}, \mathcal{E}, \mathcal{S}, \mathcal{A})$` | 工具的核心是模型、语言、引擎、求解器、接口五层。 |
| 模型族 | `$\mathcal{M} = \{\mathrm{DTMC}, \mathrm{CTMC}, \mathrm{MDP}, \mathrm{MA}\}$` | 覆盖离散、连续与非确定性概率模型。 |
| 输入族 | `$\mathcal{L} = \{\mathrm{Prism}, \mathrm{JANI}, \mathrm{GSPN}, \mathrm{DFT}, \mathrm{pGCL}, \mathrm{Explicit}\}$` | 多种前端可统一进入同一平台。 |
| 引擎族 | `$\mathcal{E} = \{\mathrm{sparse}, \mathrm{exploration}, \mathrm{dd}, \mathrm{hybrid}, \mathrm{abstraction\mbox{-}refinement}\}$` | 不同 engine 对应不同状态空间与算术结构。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 支持多种概率状态模型。 |
| 事件 / 触发 | 中等支持 | 依赖具体输入语言，如 `Prism/JANI/GSPN`。 |
| 守卫 / 数据 | 很强 | `Prism`、`JANI`、`pGCL` 都保留变量和更新。 |
| 层次 | 弱支持 | 平台主体不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 通过 `Prism/JANI` 自动机网络或 GSPN/DFT 等前端体现。 |
| 时间约束 | 中等支持 | 2017 版不支持 `PTA`，但支持 `CTMC/MA` 等定量时间模型。 |
| 连续动态 / 随机性 | 很强 | 主体就是概率/随机模型检查。 |
| 可执行 / 可验证性 | 很强 | 提供数值、符号、精确算术、反例与参数分析。 |

### 形式化问题与性质

1. 平台的关键优势在“同一架构里装下多引擎和多求解器”，而不是某一个特定算法。
2. `Storm` 通过 solver abstraction 让外部高性能库可插拔，避免把工具锁死在单一路线。
3. 它已经明显从“单工具”演进成“概率验证工作台”。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Prism` 模型。
2. `JANI` 模型。
3. `GSPN`、`DFT`、`pGCL` 专用前端。
4. 显式转移格式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. sparse matrices。
2. MTBDD。
3. rational functions for parametric models。
4. solver-level task interfaces。

### 交换与互操作

这篇论文的互操作重点在于：

1. `Prism` 与 `JANI` 双入口。
2. 多输入族共享同一 engine/solver infrastructure。
3. command-line、C++ API、Python API 三层接口共存。

## 配套基础设施

- 建模/编辑工具：原文主要讨论建模输入与 parser，本体不是图形编辑器。
- 解析/交换/元模型支持：原生支持 `Prism`、`JANI`、`GSPN`、`DFT`、`pGCL` 与显式格式。
- 仿真/执行支持：论文明确说明 `Storm` 不做 statistical model checking；主线是数值与符号分析。
- 验证/分析支持：PCTL/CSL、rewards、conditional probabilities/rewards、exact arithmetic、parametric analysis、counterexamples、permissive schedulers。
- 代码生成/转换支持：重点是 model building 与 analysis，不是部署代码生成。
- 标准化或社区生态：通过 `JANI`、`Prism` 与 solver abstraction 接入更广 quantitative ecosystem。

## 适用场景与需求前提

### 适用场景

适合概率模型检查、奖励分析、反例生成、参数化概率分析，以及需要在不同状态空间表示和不同 solver 之间切换的研究型与工程型 workflow。

### 需求前提

1. 模型能落成 `DTMC/CTMC/MDP/MA` 或相邻 quantitative family。
2. 用户关心的是概率、奖励、条件概率或参数分析。
3. 工具链需要多输入语言与多 solver 的可插拔结构。

### 不适用或高成本场景

如果目标是 `PTA`、multi-objective 或统计模型检查，这篇 2017 论文中的 `Storm` 版本并不是最直接入口。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`Storm` 更强调平台模块化与多求解器架构，而 `PRISM` 更像长期主流单平台；相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，`JANI` 是交换层，`Storm` 是实际分析后端；相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，`Momba` 更偏 Python workflow，而 `Storm` 是底层求解与模型检查引擎。

## 与本研究的关系

### 对 Project 1 的价值

它说明一旦状态机输出走向概率/随机扩展，单一语言并不够，最好同时规划后端 engine、solver 和 API 层。

### 作为目标形式主义还是中间表示

更像验证基础设施与后端工作台，而不是 LLM 生成的最终状态机交付格式。

### 对需求到模型生成的启发

1. 前端生成若能对接 `Prism/JANI`，后端就能复用 `Storm`。
2. 复杂验证 workflow 往往不是一个算法，而是 `parser + engine + solver + counterexample` 组合。
3. 多接口设计对后续自动化实验和批量闭环特别重要。

### 现实限制

论文强调的是平台架构与性能，不会直接替你决定模型该怎么抽象成概率状态机。

## 重要的相关工作

1. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：经典概率实时 model checker。
2. [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：跨工具交换层。
3. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：另一条 integrated quantitative environment 路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`probabilistic models / Storm`
- 归类理由：主贡献是概率模型检查平台的 engine/solver/API 基础设施，而不是新的概率自动机本体。
