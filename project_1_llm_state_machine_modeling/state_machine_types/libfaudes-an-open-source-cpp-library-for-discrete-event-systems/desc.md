# libFAUDES：离散事件系统开源 C++ 库 / libFAUDES -- An Open Source C++ Library for Discrete Event Systems

## 基本信息

- 标题：libFAUDES -- An Open Source C++ Library for Discrete Event Systems
- 中文标题：libFAUDES：离散事件系统开源 C++ 库
- 作者：Thomas Moor，Klaus Schmidt，Sebastian Perk
- 发表：*2008 9th International Workshop on Discrete Event Systems*，pp. 125-130，2008
- DOI：`10.1109/WODES.2008.4605933`
- 链接：https://doi.org/10.1109/WODES.2008.4605933
- 形式主义：`DES generators / supervisory control / libFAUDES`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：监督控制与 DES 算法实现/扩展的开源 C++ 基础库
- 工具/实现获取方式：原文明确把 `libFAUDES` 作为开源 `C++` 软件库发布，并配套 `luaFAUDES` console、plugins 与 benchmark scripts。
- 标准/格式获取方式：承载方式是 `generator` 类、`.gen` human-readable files、Lua scripts、plugins，以及到 `IEC 61131-3` 的代码生成扩展。

## 简报

这篇论文的价值，不是提出新的 DES 理论，而是把 Ramadge/Wonham 风格监督控制、有限自动机操作、timed/I-O/hierarchical control 扩展和脚本化实验环境统一进一个可扩展开源库里。`libFAUDES` 的角色很像 DES 领域的“研究级中间件”：核心库给 automata 与 synthesis 算法，plugin 机制给分支扩展，`luaFAUDES` 给实验脚本入口。

- 形式主义定位：离散事件系统与监督控制算法的实现基础库，不是新的状态机本体。
- 构造方式简述：用 `generator` 类表示 automata，用 STL-based containers 承载状态/事件/迁移，再通过 core operations、`SupConNB`、plugins 与 Lua 脚本组织分析流程。
- 基础设施与场景简述：依托 `C++`、STL、attribute templates、plugin architecture、`luaFAUDES`、`.gen` 文件与 code generation 扩展，服务 DES 研究、监督控制实验和工业控制原型。

```text
generator automata + specifications -> library operations / SupConNB -> plugins / luaFAUDES scripts -> supervisors / benchmarks / PLC-oriented extensions
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `generator` 类表示的有限自动机。
2. core library 中的 automata/language 操作。
3. `SupConNB` 等监督控制综合例程。
4. `luaFAUDES` 脚本接口。
5. `timed`、`hiosys`、`schmidt` 等插件扩展。

### 核心抽象

结合原文对 `generator` 的描述，可保守把单个 automaton 写成：

$$
G = (Q, \Sigma, \delta, q_0, Q_m)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\Sigma` 是事件集合。
3. `\delta` 是转移关系。
4. `q_0` 是初始状态。
5. `Q_m` 是标记状态集合。
6. 这是对论文中 `generator class models finite automata` 的保守形式化整理。

论文给出的 locally modular control 关键公式是：

$$
H_i := \parallel_{j,\ \Sigma_{G_j} \cap \Sigma_{D_i} \ne \emptyset} G_j
$$

和

$$
R_i = \mathrm{SupConNB}(H_i, D_i)
$$

上式中的符号逐项解释如下：

1. `G_j` 是第 `j` 个子 plant。
2. `D_i` 是第 `i` 个局部 specification。
3. `H_i` 是与 `D_i` 共享事件的 modular plant。
4. `R_i` 是由 `SupConNB` 计算得到的 nonblocking local supervisor。
5. 这两条公式是论文直接给出的局部模块化控制实现骨架。

论文给出的 hierarchical/decentralized 公式还包括：

$$
R_i := \mathrm{SupConNB}(G_i, D_i)
$$

$$
R := R_{hi} \parallel R_1 \parallel \cdots \parallel R_s
$$

上式中的符号逐项解释如下：

1. `G_i` 是第 `i` 个局部 plant。
2. `D_i` 是第 `i` 个局部 specification。
3. `R_{hi}` 是高层 supervisor。
4. `R` 是并行组合后的整体 supervisor。

### 一个最小例子与通俗解释

论文直接给了一个 `luaFAUDES` 脚本：

1. 先从 `.gen` 文件读 `plant1/spec1`。
2. 再把 `plant2..4` 和 `spec2..4` 做并行组合。
3. 最后调用 `SupConNB(plant, spec, super)` 生成 nonblocking supervisor。

通俗地说，`libFAUDES` 像一个“把 DES 理论算法装进可编程积木”的库。你不需要每次重写 automaton container、并行组合或 supervisor synthesis，而是直接在库和脚本层拼装实验。

### 运行 / 接受 / 转移语义

论文主体不重新定义 DES 语义，而是强调：

1. `generator` 作为统一自动机数据结构。
2. 事件可带 controllable/observable 等 attribute。
3. core library 提供 union、intersection、Kleene closure、projection、minimal realization 等语言操作。
4. supervisor synthesis 则建立在这些统一数据结构之上。

### 语义边界

边界也很清楚：

1. `libFAUDES` 不是单一 IDE，而是研究型库 + console + plugins。
2. 主体聚焦 DES / supervisory control，不是通用程序模型检查平台。
3. timed、I/O、hierarchical control 是插件扩展，不是核心库唯一本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 生成器骨架 | `$G = (Q, \Sigma, \delta, q_0, Q_m)$` | `libFAUDES` 的核心数据对象是有限自动机生成器。 |
| 模块化 plant | `$H_i := \parallel_{j,\ \Sigma_{G_j} \cap \Sigma_{D_i} \ne \emptyset} G_j$` | 用共享事件关系切出 modular plants。 |
| 局部监督器 | `$R_i = \mathrm{SupConNB}(H_i, D_i)$` | 直接在模块上做 nonblocking supervisor synthesis。 |
| 总体监督器 | `$R := R_{hi} \parallel R_1 \parallel \cdots \parallel R_s$` | 层次控制最后回收到整体 supervisor。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象就是 finite-state generators。 |
| 事件 / 触发 | 很强 | 事件集、可控/可观属性是一等对象。 |
| 守卫 / 数据 | 弱支持 | 主线是 DES，复杂数据不在核心。 |
| 层次 | 中等支持 | 通过插件支持 hierarchical control。 |
| 并发 / 同步 | 很强 | 并行组合与 supervisor synthesis 是主体。 |
| 时间约束 | 中等支持 | 通过 `timed` plugin 扩展。 |
| 连续动态 / 随机性 | 不支持 | 不在核心范围。 |
| 可执行 / 可验证性 | 很强 | 开源库、Lua console、benchmarks、code generation 一体化。 |

### 形式化问题与性质

1. 它把 DES 理论算法从一次性实验代码提升成可复用库基础设施。
2. plugin 机制是区分 core library 与方法扩展的关键。
3. `luaFAUDES` 明显降低了批量 benchmark 和可重复实验的成本。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `generator` 类直接建模 automata。
2. `.gen` human-readable 文件。
3. `luaFAUDES` 脚本。
4. plugin-based specialized executables。

### 机器可处理承载方式

机器可处理承载方式包括：

1. STL-based containers for states/events/transitions。
2. 带 attribute template 的事件集与状态集。
3. `.gen` 文件格式。
4. Lua scripting interface。

### 交换与互操作

这条路线的互操作重点在于：

1. core library 与 plugins 的严格分离。
2. Lua console 与 C++ core 的桥接。
3. 向 `IEC 61131-3` 代码生成与硬件在环扩展。

## 配套基础设施

- 建模/编辑工具：`luaFAUDES` console、`.gen` 文件、Qt generator widget。
- 解析/交换/元模型支持：human-readable file I/O、attribute templates、plugin architecture。
- 仿真/执行支持：同步 timed generators simulator、interactive/stochastic execution。
- 验证/分析支持：automata operations、supervisor synthesis、locally modular control、hierarchical/decentralized control。
- 代码生成/转换支持：到 `IEC 61131-3` 的 code generator。
- 标准化或社区生态：采用 `LGPL` 开源许可，适合学术与工业扩展。

## 适用场景与需求前提

### 适用场景

适合 DES 理论算法实现、监督控制 benchmark、模块化控制原型、脚本化实验，以及需要把监督器进一步落到 PLC/工业软件链路的场景。

### 需求前提

1. 系统能用 finite automata / DES 方式建模。
2. 主要问题是 controllability、observability、nonblocking、modularity 等 supervisory-control 议题。
3. 用户接受 `C++`/Lua 风格的研究型工具环境。

### 不适用或高成本场景

如果系统高度依赖连续动力学、丰富数据语义或现代图形建模前端，`libFAUDES` 不会像 `Stateflow` 或 `BIP` 平台那样直接。

## 与相邻形式主义的关系

相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，`libFAUDES` 更像可编程基础库而不是完整 IDE；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，它更靠近 DES algorithm implementation，而不是完整 supervisory-control engineering pipeline；相对 [plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md](../plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md)，它提供的是更底层的库基础设施而非单一 PLC bridge。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续要把 LLM 生成的有限状态控制模型真正接到控制工程工具链，除了语言本体，还需要能批量做组合、综合和脚本实验的库层基础设施。

### 作为目标形式主义还是中间表示

更像验证/综合基础设施与实验平台，而不是最终目标语言。

### 对需求到模型生成的启发

1. 生成的状态机若保留 controllable/observable 事件属性，就更容易接 supervisory-control 工具。
2. 中间表示最好能稳定序列化到人类可读文件，再配脚本化批处理。
3. 模型工具链不一定非要重图形前端，库和脚本也可以非常有效。

### 现实限制

它对理论算法实验很强，但对现代工程 UI 和混成/概率扩展不是主打方向。

## 重要的相关工作

1. [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)：大规模 DES IDE。
2. [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)：监督控制工程链平台。
3. [plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md](../plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md)：监督器到 PLC 的落地桥接。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`DES generators / supervisory control / libFAUDES`
- 归类理由：论文主体是监督控制算法与 DES 建模的库级基础设施，而不是新的状态机母线。
