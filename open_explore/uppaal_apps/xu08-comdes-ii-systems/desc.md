问题一句话：本文验证的是基于 COMDES-II 的嵌入式控制系统，核心问题是组件化模型在保持原语义的前提下能否被系统性翻译到 `UPPAAL`，并对调度与反应行为做正式验证。
方法一句话：作者把 COMDES-II 的 actor、scheduler、state machine function block 等语义锚定到 `UPPAAL` timed automata，并在 turntable control system 上验证该模型转换流程。
验证收获一句话：在 `6` 个 actor task 的转台控制案例上，`UPPAAL` 能在约 `7s` 内证明任务不会进入 `ERROR` 状态，说明所提转换流程足以支撑实际嵌入式控制案例验证。

## 基本信息

- 标题：Verification of COMDES-II Systems Using UPPAAL with Model Transformation
- 中文标题：通过模型转换使用 `UPPAAL` 验证 COMDES-II 系统
- 作者：Xu Ke、Paul Pettersson、Krzysztof Sierszecki、Christo Angelov
- 单位：University of Southern Denmark；Mälardalen University
- 发表：`RTCSA 2008`
- DOI：`10.1109/RTCSA.2008.32`
- 链接：[DOI](https://doi.org/10.1109/RTCSA.2008.32)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🏭 工业与基础设施
- 被验证系统：基于 COMDES-II 设计的 Turntable Control System
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：公开可得的是 [SDU 开放版本 PDF](https://findresearcher.sdu.dk/ws/portalfiles/portal/3637/Verification_of_COMDES-II_Systems_Using_UPPAAL_with_Model_Transformation_normalsize.pdf)；未见独立模型转换工具或案例模型包下载。
- 案例/数据获取方式：turntable case study 来自 COMDES-II 设计案例，无独立数据集。

## 简报

这篇论文的主线是“如何把组件化嵌入式控制模型可靠地搬到 `UPPAAL`”。不过它并没有停在纯方法层，而是用一个实际的 turntable control system 案例来证明这套转换真的能落地验证。

- 系统：COMDES-II 组件化嵌入式控制系统，以 turntable control system 为验证案例。
- 特点：显式区分 actor 调度、时间语义和功能块行为。
- 规模：案例中 `UPPAAL` 模型包含 `6` 个 actor tasks。
- 模型：actor、scheduler、state machine FB、通信语义分别锚定到 timed automata、共享变量和离散时间机制。
- 性质：任务不得进入 `ERROR` 状态，系统应满足 schedulability 与 reactive behavior 要求。
- 方法：语义锚定 + 模型转换 + `UPPAAL` 性质检查。
- 结果：turntable 案例验证通过，单条 schedulability 性质在 `7s` 内完成。

`COMDES-II 组件模型 -> 语义锚定到 timed automata -> Turntable 控制案例 -> schedulability/反应行为验证`

## 论文定位

这篇论文位于 `uppaal_apps/` 与 `uppaal_tech/` 的交界处。它确实包含较强的方法框架成分，但正文最终落脚在 turntable control system 的实际验证，因此仍可作为应用条目录入，只是状态更适合记为“案例可整理而非最强代表案例”。

从主轴看，真正被验证的是控制系统行为，所以仍归 `🎛️ 控制器与设备控制`；从次轴看，它服务的是真实嵌入式工业控制场景，因此归 `🏭 工业与基础设施`。

## 验证对象与问题背景

### 系统与场景

被验证对象是一个用 COMDES-II 设计的 turntable control system。COMDES-II 旨在支持具有硬实时约束的分布式控制系统开发，因此案例本身面向安全关键控制。

### 系统组成与运行机制

论文重点介绍的是 COMDES-II 的语义层次：

1. `Actor`
   主动组件，负责任务执行与 I/O。
2. `Scheduler`
   控制离散时间下 actor task 的释放、运行和完成。
3. `Function Blocks`
   包括 basic/composite/modal/state machine FB，用于表达功能和反应逻辑。
4. `Signal-based communication`
   actor 之间通过带标签的状态消息通信。

### 验证边界

本文验证的是**由 COMDES-II 模型转换得到的控制系统行为**，重点是 schedulability 和 reactive behavior 是否被保真带到 `UPPAAL`。论文对 turntable 具体工艺细节展开不多，因此这里需要明确：它更像“以真实案例验证转换框架”的论文，而非深描系统本体的案例论文。

### 核心问题

COMDES-II 已经定义了语法和静态语义，但组合后系统行为、任务调度和状态机逻辑如何做正式验证仍然困难。作者想解决的是“组件语义如何不失真地进入 `UPPAAL`”。

## 模型与形式化建模

论文把 COMDES-II 语义拆成四个映射层：

1. actor 映射为 `UPPAAL` 进程；
2. actor interaction 映射为共享变量和数据结构；
3. actor concurrency 映射为离散时间执行阶段；
4. scheduler 映射为独立 timed automaton。

此外，state machine function block 被转换为不带时间注解的自动机，priority-based transition ordering 则通过互斥守卫编码。

作者强调，这种 meta-level transformation 的目标不是“近似相似”，而是尽量保留 COMDES-II 原有的 deterministic task semantics 与 split-phase timing behavior。

## 验证目标与性质

### 待验证问题

1. 转换后的 `UPPAAL` 模型是否保留原系统调度语义。
2. actor task 是否会进入 `ERROR` 状态。
3. reactive behavior 是否满足需求。

### 性质类型

1. 调度性质：任务必须可调度。
2. 安全性质：任一 task 不得进入 `ERROR`。
3. 反应行为：state machine FB 的反应语义应与 COMDES-II 一致。

### 查询表达

论文明确给出了一条代表性查询：

`A[] forall(i : int[1,TASKS_NUM]) task[i].status != ERROR`

它对应的工程含义是：所有任务在所有可达状态中都不能进入错误执行状态。

## 核心方法与验证流程

1. 先定义 COMDES-II 和 `UPPAAL` 之间的语义映射。
2. 对 actor、scheduler 和 function blocks 做模型转换。
3. 把 turntable case study 从 COMDES-II 转为 `UPPAAL`。
4. 依据系统需求构造 schedulability 与 reactive queries。
5. 在 `UPPAAL` 中执行验证并评估开销。

## 案例与结果

1. 论文在 turntable control system 上验证了该转换框架。
2. 代表性 schedulability 性质在 `2.0 GHz Core Duo / 2 GB RAM` 机器上约 `7s` 完成。
3. 该次验证的内存占用约为 `18220 KB`。
4. 论文据此认为：在保留 COMDES-II 原语义的前提下，`UPPAAL` 足以承担动态行为验证。

## 与本研究的关系

### 相关性分析

该论文对博士研究最重要的价值，是它把“领域特定建模语言/组件框架 -> timed automata -> verification”这一链路做成了完整示例。

### 可借鉴之处

1. 用语义锚定控制模型转换保真。
2. 将调度语义和功能语义分层编码。
3. 用具体案例验证转换链条是否真的可用。

### 存在的不足与改进空间

turntable 系统本体展开较少，因此单篇系统分析深度不如纯案例论文；公开工件也不足。

### 对本研究的启发

它非常适合作为“从 DSL/组件模型到 `UPPAAL`”的参考文献，尤其对后续 pyfcstm 或其他领域语言如何进入验证链路有直接借鉴意义。

## 重要的相关工作

### 1. COMDES-II 框架

论文建立在 COMDES-II 的组件模型与状态机功能块之上。

### 2. timed automata 语义锚定

本文的核心贡献之一就是把控制框架语义稳定落到 timed automata。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：公开可得的是 [SDU 开放版本 PDF](https://findresearcher.sdu.dk/ws/portalfiles/portal/3637/Verification_of_COMDES-II_Systems_Using_UPPAAL_with_Model_Transformation_normalsize.pdf)；未见 turntable 案例的 `UPPAAL` 模型或转换工具下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.1109/RTCSA.2008.32)
- 对后续复用的现实影响：适合借鉴建模与转换思路，但若要复跑案例，需要基于论文与 COMDES-II 资料自行重建。
