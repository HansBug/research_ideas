# 围绕 Neco 编译器构建 Petri 网工具 / Building Petri Nets Tools around Neco Compiler

## 基本信息

- 标题：Building Petri Nets Tools around Neco Compiler
- 中文标题：围绕 Neco 编译器构建 Petri 网工具
- 作者：Lukasz Fronc，Franck Pommereau
- 发表：*PNSE 2013 / CEUR Workshop Proceedings Vol. 989*，2013
- DOI：原文未提供
- 链接：https://ceur-ws.org/Vol-989/paper01.pdf
- 形式主义：`High-Level Petri Nets / Neco compiler / exploration and LTL-checking toolchain`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：Petri-net compiler / state-space exploration / LTL-checking infrastructure
- 工具/实现获取方式：论文直接给出 `Neco` 下载与文档入口，原文地址是 `http://code.google.com/p/neco-net-compiler`；当前历史地址可能需要通过镜像或代码归档继续追踪。
- 标准/格式获取方式：原文明确指出输入可以是 `Python/SNAKES`、`ABCD` 或 `PNML`，输出是经 `Cython/C++` 编译后的 exploration library 以及配套检查模块。

## 简报

这篇论文的核心不是再定义一种新的 Petri 网，而是把“Petri 网模型 -> 专用探索引擎 -> LTL 检查组件”做成编译式基础设施。`Neco` 通过对高层 Petri 网做类型推断、标识优化和后端代码生成，把通常在解释器里做的 transition firing 和 state-space traversal 变成专门编译过的库，因此更像 Petri 网版本的 domain-specific compiler。

- 形式主义定位：围绕 high-level Petri nets 的编译式工具链，而不是新的网语义主干。
- 构造方式简述：输入 `SNAKES/ABCD/PNML` 模型，经 `neco-compile` 生成 marking structure、successor functions 和 compilation trace，再由 `neco-explore`、`neco-check`、`neco-spot` 组合完成探索和 `LTL` 模型检查。
- 基础设施与场景简述：依托 `Python/Cython/C++`、`SPOT` 和编译元数据，适合面向工具开发者的高性能显式状态空间探索。

```text
Petri net model -> neco-compile -> optimized exploration engine -> state-space exploration / atomic-proposition checker -> SPOT-based LTL model checking
```

## 形式主义定义与核心对象

### 定义对象

`Neco` 处理的核心对象不是单一数学元组，而是“模型 + 编译产物 + 检查产物”三层：

1. 高层 Petri 网模型本体。
2. 针对该模型编译出的 exploration engine。
3. 针对该模型标识结构再编译出的 atomic proposition checker。

### 核心抽象

结合论文对编译产物的描述，可把 `Neco` 针对单个 Petri 网生成的探索引擎保守写为：

$$
\mathcal{E}_{Neco} = (M, \mathrm{init}, \mathrm{succ}, \{\mathrm{succ}_{t}\}_{t \in T}, \mathrm{trace})
$$

上式中的符号逐项解释如下：

1. `M` 是编译后生成的 marking structure。
2. `\mathrm{init}` 是初始标识构造函数。
3. `\mathrm{succ}` 是全局 successor function。
4. `\mathrm{succ}_t` 是特定于某条迁移 `t` 的 successor function。
5. `\mathrm{trace}` 是 compilation trace，记录模型和标识结构元数据。
6. 这是依据原文 Figure 1 和 Section 2.1 的保守整理，不是论文显式统一元组。

论文把整体工具链列成四个命令，可进一步压成：

$$
\mathcal{T}_{Neco} = \{\texttt{neco-compile},\ \texttt{neco-explore},\ \texttt{neco-check},\ \texttt{neco-spot}\}
$$

上式中的符号逐项解释如下：

1. `\texttt{neco-compile}` 负责从模型生成 exploration engine。
2. `\texttt{neco-explore}` 用该引擎建立状态空间与 reachability graph。
3. `\texttt{neco-check}` 为给定 `LTL` 公式生成 atomic proposition checker。
4. `\texttt{neco-spot}` 把上两步产物接到 `SPOT` 上做 `LTL` 模型检查。

论文对 `LTL` 检查模块的核心接口也给得很清楚，可保守写为：

$$
\mathrm{check}(m, i) \to \{\mathrm{true}, \mathrm{false}\}
$$

上式中的符号逐项解释如下：

1. `m` 是某个具体标识状态。
2. `i` 是原子命题编号。
3. `\mathrm{check}` 返回该原子命题在该状态上的真假。
4. `i` 来自对原始 `LTL` 公式做 id-atom map 之后得到的标识。

### 一个最小例子与通俗解释

原文没有铺一个长的单独案例，而是通过工具链图解释最小用法：

1. 用 `SNAKES`、`ABCD` 或 `PNML` 写一个 Petri 网。
2. 运行 `neco-compile`，得到一个专门针对该网的探索库。
3. 运行 `neco-explore`，通过 `init` 和 `succ` 逐步扩展可达标识。
4. 若再给一条 `LTL` 公式，则用 `neco-check` 生出原子命题检查器，并由 `neco-spot` 输出 counterexample。

通俗地说，`Neco` 像“把一张 Petri 网先编译成一套专门服务它自己的状态空间 API，再把这个 API 提供给探索器和模型检查器”。它比传统通用 Petri 网解释器更进一步，因为它把很多结构信息内联进生成代码里了。

### 运行 / 接受 / 转移语义

`Neco` 自身不是新的 Petri 网语义，而是针对给定网生成高效执行产物。论文强调 exploration engine 的主要职责是：

$$
\mathrm{Reach}(N) = \mu Z.\ \{\mathrm{init}(N)\} \cup \mathrm{succ}(Z)
$$

上式中的符号逐项解释如下：

1. `N` 是输入 Petri 网。
2. `\mathrm{init}(N)` 是初始标识。
3. `\mathrm{succ}(Z)` 表示对已发现状态集合应用 successor expansion。
4. `\mu Z` 表示取最小不动点，也就是反复探索直到无新状态。
5. 这是依据论文“repeatedly calling successor functions”做的保守归纳。

对 `LTL` 检查部分，可压缩为：

$$
\text{Petri net} + \varphi_{LTL} \xrightarrow{\texttt{neco-check} + \texttt{neco-spot}} \text{counterexample or satisfaction result}
$$

上式中的符号逐项解释如下：

1. `\varphi_{LTL}` 是 Neco 兼容语法的 `LTL` 公式。
2. `neco-check` 先为原子命题生成模型专用检查函数。
3. `neco-spot` 再利用 `SPOT` 的算法执行模型检查。

### 语义边界

1. `Neco` 主要面向 explicit state-space exploration 和 `LTL` checking，不是通用数值分析平台。
2. 其性能依赖输入模型是否能被充分静态类型化；若嵌入 Python 对象过多，就会回退到解释器调用。
3. 论文明确区分 Python backend 与 Cython backend，部分特性只在某一后端可用。
4. 它强调的是 Petri 网编译和工具复用，不是新的 `PNML` 标准定义或新网类理论。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 探索引擎骨架 | `$\mathcal{E}_{Neco}=(M,\mathrm{init},\mathrm{succ},\{\mathrm{succ}_t\},\mathrm{trace})$` | 概括了编译后库的最关键组件。 |
| 工具链骨架 | `$\mathcal{T}_{Neco}=\{\texttt{neco-compile},\texttt{neco-explore},\texttt{neco-check},\texttt{neco-spot}\}$` | 说明 `Neco` 是一整条链，不只是单命令工具。 |
| 可达性计算 | `$\mathrm{Reach}(N)=\mu Z.\{\mathrm{init}(N)\}\cup\mathrm{succ}(Z)$` | 对应反复调用 successor functions 建立状态空间。 |
| AP 检查接口 | `$\mathrm{check}(m,i)\to\{\mathrm{true},\mathrm{false}\}$` | 说明 `LTL` 检查的模型专用接口形态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 主体对象是 Petri net 标识，不是状态图模式。 |
| 事件 / 触发 | 中等支持 | 通过迁移 firing 和 successor functions 实现。 |
| 守卫 / 数据 | 很强 | 支持 Python 表达式、高层 token、类型推断。 |
| 层次 | 不适用 | 论文重心不在层次状态机。 |
| 并发 / 同步 | 很强 | Petri 网本体就是并发建模对象。 |
| 时间约束 | 不支持 | 这篇条目不讨论 timed nets。 |
| 连续动态 / 随机性 | 不支持 | 主线是显式探索与 `LTL`。 |
| 可执行 / 可验证性 | 很强 | exploration、reachability graph 和 `LTL` checking 全部打通。 |

### 形式化问题与性质

1. `Neco` 的关键创新是“面向单模型编译”的 Petri 网工具链，而不是通用解释器。
2. compilation trace 是它的关键基础设施，因为不同工具都必须和优化后的 marking structure 对齐。
3. `SPOT` 的接入说明它不是孤立平台，而是主动把 Petri 网世界接到既有 automata / `LTL` 工具生态上。

## 构造方式与承载格式

### 建模入口

原文明确列出三个输入入口：

1. `Python + SNAKES`。
2. `ABCD` formalism。
3. `PNML`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 输入 Petri 网模型。
2. 编译后的 native Python shared library。
3. model-specific marking structure。
4. compilation trace 元数据。
5. `LTL` 公式文件与 atomic proposition checker module。

### 交换与互操作

1. 输入侧支持 `PNML`，这是与 Petri 网标准生态最直接的接口。
2. 探索引擎通过 Python module 和 `C++` library 双重形态暴露，便于被其他工具重用。
3. `LTL` 检查通过 `SPOT` 接口完成，说明它和 automata-based model checking 生态存在稳定互操作。

## 配套基础设施

- 建模/编辑工具：可由 `SNAKES`、`ABCD` 或其他 `PNML` 生成工具提供前端建模。
- 解析/交换/元模型支持：`PNML` 输入、类型推断、marking structure 生成和 compilation trace 是关键。
- 仿真/执行支持：`neco-explore` 负责状态空间探索；生成库也可被外部 client program 调用。
- 验证/分析支持：`neco-check` + `neco-spot` 提供 `LTL` 模型检查，依赖 `SPOT`。
- 代码生成/转换支持：`Cython` backend 会把可类型化部分翻译为高效 `C++`。
- 标准化或社区生态：论文把它定位成 free software，并明确面向工具开发者复用。

## 适用场景与需求前提

### 适用场景

适合需要把高层 Petri 网快速转成高性能探索器、显式状态空间分析器或 `LTL` 模型检查后端的场景，尤其适合研究型 Petri 网工具开发和 benchmark 分析。

### 需求前提

1. 系统本身更自然地建模为 Petri 网而不是状态机或 timed automata。
2. 需要显式状态空间、reachability graph 或 `LTL` 检查，而不是连续或随机数值分析。
3. 模型中的 token / 表达式最好能较多地被静态类型化，以吃到编译优化收益。

### 不适用或高成本场景

1. 若系统主体是 timed / stochastic / hybrid extensions，这篇论文覆盖不够。
2. 若模型 heavily 依赖复杂 Python 动态对象，`Cython` 优势会下降。
3. 若只想做普通仿真而不关心探索/检查，完整编译工具链的成本可能偏高。

## 与相邻形式主义的关系

1. 相比普通 Petri 网编辑器，`Neco` 更像编译器和后端基础设施。
2. 相比 `PIPE+ / TimeNET / GreatSPN / MARCIE` 这类整体验证平台，它更强调 explicit exploration engine 的可复用生成。
3. 与 `SPOT` 的耦合说明它把 Petri 网和 automata-based `LTL` checking 连接了起来。
4. 它与状态机家族不同，描述客体更偏 token / marking / 并发流，而不是层次控制模式。

## 与本研究的关系

### 对 Project 1 的价值

它对 `project_1` 的价值主要不在“作为目标状态机”，而在“如何把形式模型编译成可重复使用的分析基础设施”。这对后续做 LLM 生成模型后的自动验证后端很有启发。

### 作为目标形式主义还是中间表示

它不是 `project_1` 直接输出的理想目标形式主义，但非常适合作为中间验证承载或对照后端，尤其当生成对象偏并发资源流控制时。

### 对需求到模型生成的启发

1. 若 LLM 生成的是 Petri 网，最好同步生成结构化类型信息，以便后端编译优化。
2. compilation trace 这种中间元数据很关键，它能把“模型生成”和“验证工具调用”稳定衔接起来。
3. 模型检查工具最好面向单模型生成专用适配层，而不是完全依赖通用解释器。

### 现实限制

1. 这是研究型工具链，生态和维护稳定性不如主流工业平台。
2. 重点是显式探索和 `LTL`，覆盖面不如大型综合平台。
3. 历史下载入口已老化，后续获取实现可能需要额外追踪。

## 重要的相关工作

### 奠基或前身工作

1. `SNAKES` 是论文直接依赖的 Petri 网原型工具。
2. `SPOT` 是 `LTL` 后端的关键前身。

### 同类型或同家族工作

1. 其他 Petri 网工具如 `PIPE+`、`TimeNET`、`GreatSPN`、`TAPAAL` 都属于相邻基础设施。
2. 但它们多是完整平台，而 `Neco` 更强调 compiler-generated exploration engine。

### 标准 / 格式 / 工具链工作

1. `PNML` 是它的重要输入格式。
2. `ABCD` 则体现它还支持另一类高层 Petri 网前端。

### 与本研究关系最紧的工作

1. 对文库里的 Petri 网基础设施线，它和 `MARCIE`、`PIPE+`、`TimeNET` 互补。
2. 对“模型 -> 可执行分析后端”的思路，它和 `OpenNWA/WALi/PDAAAL` 这类编译式/库式后端更接近。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`High-Level Petri Nets / Neco compiler / exploration and LTL-checking toolchain`
- 论文角色：Petri-net compiler / state-space exploration / LTL-checking infrastructure
- 核心功能：把 Petri 网编译成模型专用 exploration engine，并进一步接到 `SPOT` 做 `LTL` 检查。
- 关键特性：类型推断、marking optimization、per-transition successor functions、compilation trace、`SPOT` 对接。
- 构造方式：`SNAKES/ABCD/PNML` 输入 -> `neco-compile` -> native module -> `neco-explore/neco-check/neco-spot`。
- 基础设施：Python/Cython/C++ backend、`SPOT`、模型专用标识结构与 AP checker。
- 适用场景：Petri 网显式状态空间探索、工具开发、`LTL` 检查后端构建。
- 需求前提：对象应更适合并发资源流建模，且希望把模型编译成高性能检查基础设施。
- 状态：🟢 直接可用
