# 从 Petri 网综合异步硬件 / Synthesis of Asynchronous Hardware from Petri Nets

## 基本信息

- 标题：Synthesis of Asynchronous Hardware from Petri Nets
- 中文标题：从 Petri 网综合异步硬件
- 作者：Josep Carmona，Jordi Cortadella，Victor Khomenko，Alexandre Yakovlev
- 发表：*Lectures on Concurrency and Petri Nets: Advances in Petri Nets*，pp. 345-401，2004
- DOI：`10.1007/978-3-540-27755-2_9`
- 链接：https://doi.org/10.1007/978-3-540-27755-2_9
- 形式主义：`Petri Nets / Signal Transition Graphs / asynchronous hardware synthesis`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：Petri-net/STG-based logic-synthesis route for asynchronous control hardware
- 工具/实现获取方式：论文明确围绕 `Petrify`、`SAT` 求解器、`ILP` 和 Petri-net unfolding 组织综合流程；正文未给统一公开仓库，但多次以 `Petrify` 作为核心现有工具。
- 标准/格式获取方式：核心承载对象是 `HDL`、`Petri Net/STG`、unfolding prefix、`CSC/USC` 检查与 logic equations；它不是交换标准，而是异步硬件综合方法线。

## 简报

这篇论文的重要性在于：它把 `Petri Net/STG` 不再只当作“可以描述并发控制逻辑的模型”，而是系统性地当作异步硬件综合的中间表示，并且沿着 direct mapping、结构方法、`ILP`、unfolding 和 `SAT` 几条线把 state-space explosion 问题重新拆开。对文库来说，这不是某个单独工具的短文，而是异步控制器从 `HDL`/timing diagram 到逻辑电路的整条方法路线总述。

- 形式主义定位：`Petri Net/STG` 驱动的异步硬件综合方法路线，而不是新的网模型分支。
- 构造方式简述：`HDL/timing diagram -> Petri Net / STG -> CSC / USC analysis -> direct mapping or ILP or unfolding+SAT -> asynchronous circuit`。
- 基础设施与场景简述：依托 `STG`、`Petrify`、unfolding prefix、`SAT/ILP` 和状态编码分析，服务异步控制器与 `speed-independent` 电路综合。

```text
HDL or timing diagram -> Petri Net / STG -> state-coding analysis -> structural or unfolding-based synthesis -> asynchronous circuit
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 高层 `HDL` 或 timing diagram 规格；
2. `Signal Transition Graph (STG)`；
3. `Petrify` 状态空间式综合；
4. 结构化 `ILP` 方法；
5. unfolding + `SAT` 驱动的综合与编码冲突分析。

### 核心抽象

论文把异步控制器的关键前端形式化为 `STG`。文中给出的保守骨架可写成：

$$
G = (N, M_0, Z, \lambda)
$$

上式中的符号逐项解释如下：

1. `N` 是底层 Petri 网结构。
2. `M_0` 是初始标识。
3. `Z` 是信号集合，并区分输入、输出与内部信号。
4. `\lambda` 把迁移标记成某个信号的上升/下降事件。
5. `STG` 由此成为 timing diagram 和控制器逻辑之间的中间表示。

论文强调的方法总链可以保守压缩成：

$$
HDL \xrightarrow{\tau_1} STG \xrightarrow{\tau_2} Circuit
$$

上式中的符号逐项解释如下：

1. `\tau_1` 表示从 `HDL`、算法或 timing diagram 提炼控制部分并构造 `STG`。
2. `\tau_2` 表示后续的逻辑综合，可走 direct mapping、结构化方法或 unfolding+`SAT` 路线。
3. 论文重点正是如何让 `\tau_2` 不再完全受全状态空间限制。

对 unfolding 路线，论文进一步把分析对象转成有限完整展开前缀。可保守写成：

$$
\pi = \mathrm{Unf}(G)
$$

其中：

1. `\pi` 是 `STG` 的 finite complete unfolding prefix。
2. 它保留了偏序并发语义。
3. 论文用它承载 `CSC` 冲突检测、支持集求解与后续 `SAT` 编码。

### 一个最小例子与通俗解释

论文用两个非常典型的例子铺开整条综合链：

1. 一个简单 filter controller，从高层算法描述开始，提炼出控制器 `STG`。
2. 一个 `VME` bus controller，从 timing diagram 直接构造 `STG`。
3. 接着分析 `CSC/USC` 与状态编码问题。
4. 最后通过 `Petrify`、`ILP` 或 unfolding+`SAT` 生成逻辑实现。

通俗地说，这条路线像“先把异步控制器需求压成信号事件网，再决定是走传统状态空间式综合，还是走更结构化、更偏偏序语义的综合办法”。

### 运行 / 接受 / 转移语义

由于 `STG` 继承 Petri 网语义，论文的方法建立在标识迁移之上。可保守写成：

$$
M \xrightarrow{t} M'
$$

上式中的符号逐项解释如下：

1. `M` 和 `M'` 是前后两个标识。
2. `t` 是某个已使能的信号迁移。
3. 一次 firing 对应某个信号上升或下降事件的发生。

论文真正关心的是由这种并发事件网能否稳定导出电路实现，因此状态编码问题可概括为：

$$
STG \xrightarrow{\mathrm{CSC/USC}} Encoded\ STG \xrightarrow{} Circuit
$$

这并不是单一算法，而是一系列 direct mapping、`ILP`、unfolding 和 `SAT` 技术的共同目标。

### 语义边界

1. 论文聚焦异步控制器综合，不是一般 Petri 网分析大全。
2. 它特别关注 `CSC/USC` 和状态空间爆炸，因此大量方法都服务于规避全 reachability graph。
3. `STG` 非常适合信号级异步控制逻辑，但不等价于任意数据路径模型。
4. 文章是路线综述型长文，很多具体算法只给核心思想而非完整实现细节。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `STG` 骨架 | `$G = (N, M_0, Z, \lambda)$` | 异步控制器综合的核心中间表示。 |
| 综合总链 | `$HDL \xrightarrow{\tau_1} STG \xrightarrow{\tau_2} Circuit$` | 从高层行为到电路实现的主流程。 |
| unfolding 前缀 | `$\pi = \mathrm{Unf}(G)$` | 用偏序语义替代完整状态空间的关键对象。 |
| 标识推进 | `$M \xrightarrow{t} M'$` | `STG`/Petri 网的基本执行语义。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 主要通过标识和信号事件组合体现状态。 |
| 事件 / 触发 | 很强 | 上升/下降信号事件是核心。 |
| 守卫 / 数据 | 弱支持 | 重点是控制与握手，不是富数据语义。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 很强 | Petri 网偏序和并发因果是方法核心。 |
| 时间约束 | 弱支持 | 讨论的是异步实现与时序鲁棒性，不是显式时钟模型。 |
| 连续动态 / 随机性 | 不支持 | 纯离散控制硬件逻辑。 |
| 可执行 / 可验证性 | 很强 | 直接面向逻辑综合、编码检查和实现。 |

### 形式化问题与性质

1. 论文真正解决的是“Petri 网/STG 如何成为异步硬件综合的高价值中间表示”。
2. 它把 direct mapping、结构方法、`ILP`、unfolding 和 `SAT` 放在同一条问题链里看待，而不是割裂成独立技巧。
3. 对文库来说，这篇论文非常适合作为 `Petri/STG` 异步综合主线的路线型锚点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `HDL` 行为描述；
2. timing diagram；
3. 提炼出的 `Petri Net/STG`；
4. unfolding prefix；
5. `ILP/SAT` 编码；
6. 最终逻辑电路。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `STG`；
2. 信号事件与 handshake 关系；
3. 状态编码约束；
4. unfolding prefix；
5. `ILP/SAT` 问题实例；
6. 逻辑实现与支持集。

### 交换与互操作

这条路线的互操作重点在：

1. 高层 `HDL` 或 timing diagram 可以下沉到 `STG`；
2. `Petrify`、结构分析与 `SAT` 都共享 `STG` 或 unfolding 这一核心中间对象；
3. 逻辑综合的很多难点被转写为状态编码、支持集和冲突检测问题。

## 配套基础设施

- 建模/编辑工具：`HDL`、timing diagram 与 `STG` 规格。
- 解析/交换/元模型支持：`STG` 作为异步控制器综合的中心中间表示。
- 仿真/执行支持：重点不是仿真，而是电路综合与编码正确性。
- 验证/分析支持：`CSC/USC` 检查、冲突检测、support analysis、unfolding 与 `SAT/ILP` 求解。
- 代码生成/转换支持：从 `STG` 导出逻辑电路实现。
- 标准化或社区生态：依托 `Petrify` 和异步电路 `STG` 工具链生态。

## 适用场景与需求前提

### 适用场景

适合异步控制器、握手协议电路、`speed-independent` 设计以及任何能自然写成信号事件网的控制硬件综合任务。

### 需求前提

1. 控制逻辑能被提炼为 `STG` 或相邻 Petri 网表示。
2. 设计目标确实关心异步实现和状态编码问题。
3. 团队愿意接受 `STG` 作为中间表示，而不是直接从 `HDL` 黑箱综合。
4. 若规模较大，最好能利用 unfolding/结构方法而非完全依赖全状态空间。

### 不适用或高成本场景

如果问题主要是富数据路径优化而不是控制逻辑，单用 `STG` 路线的收益会有限。

## 与相邻形式主义的关系

相对 [petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md](../petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md)，那篇更偏工具基础设施，这篇更像把整条 `Petri/STG` 综合路线系统化梳理出来；相对 [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)，后者是带仲裁元件的现代 `Workcraft` 工作流，这篇覆盖更广的前端与综合方法版图；相对 [timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md](../timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md)，那篇把异步电路接到 timed-automata 后端，这篇则停留在 `Petri/STG` 驱动的电路综合主线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `Petri Net/STG` 不只是分析模型，也可以成为从需求到实现的重要中间表示。
2. 对博士研究中的“生成-验证-修复”闭环而言，这类条目能帮助区分“形式模型可验证”与“形式模型可综合”的差异。
3. 若后续研究要接触控制器自动实现，这条 `Petri/STG` 线是重要的横向参照。

### 作为目标形式主义还是中间表示

更像高价值中间表示与综合路线，而不是新的终局形式主义节点。

### 对需求到模型生成的启发

1. 对带握手和并发约束的控制逻辑，网模型往往比平面状态机更自然。
2. 形式模型若能同时支持验证和综合，研究价值会显著提高。
3. 复杂验证/综合问题可以通过偏序展开、结构分解等方式避开全局状态爆炸。

## 重要的相关工作

- [petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md](../petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md)：`Petrify` 工具基础设施条目。
- [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)：现代 `Workcraft`/`STG` 异步综合流。
- [timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md](../timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md)：异步电路与定时自动机验证后端的另一条桥接线。

## 文献分类总结

- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Petri Nets / Signal Transition Graphs / asynchronous hardware synthesis`
- 论文角色：Petri-net/STG-based logic-synthesis route for asynchronous control hardware
- 归类理由：论文主体是从 `Petri/STG` 出发系统梳理异步控制器综合方法，因此最适合作为 `Petri` 主类下的综合路线条目，而不是单纯工具基础设施。
