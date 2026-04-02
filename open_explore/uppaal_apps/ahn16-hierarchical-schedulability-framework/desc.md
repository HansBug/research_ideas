问题一句话：本文验证的是层次化实时系统的可调度性，核心问题是当任务依赖、共享资源和虚拟化调度层级叠加时，系统还能否始终在 deadline 前完成。
方法一句话：作者提出一个基于 `UPPAAL` 的层次化 schedulability 分析框架，将根调度器、虚拟调度器、任务、共享资源和依赖关系直接编成统一模型，并用 `A[] not err` 检查 deadline miss。
验证收获一句话：论文展示了同一框架如何先证明一个目标系统可调度，再通过共享资源和预算更新构造出 priority inversion 与预算不足的反例，最后扩展到三层层次化系统。

## 基本信息

- 标题：Hierarchical System Schedulability Analysis Framework Using UPPAAL
- 中文标题：基于 `UPPAAL` 的层次化系统可调度性分析框架
- 作者：So Jin Ahn、Dae Yon Hwang、Miyoung Kang、Jin-Young Choi
- 单位：Korea University
- 发表：IEICE Transactions on Information and Systems，2016
- DOI：`10.1587/transinf.2016EDL8003`
- 链接：[DOI](https://doi.org/10.1587/transinf.2016EDL8003)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🏭 工业与基础设施
- 被验证系统：带虚拟调度层、共享资源和任务依赖的层次化实时系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供独立仓库；给出框架输入、状态结构和案例拓扑。
- 案例/数据获取方式：案例为论文内构造的层次化 target system，可根据表格与拓扑图重建。

## 简报

这篇论文关注的是一种非常工程化的对象：采用虚拟化技术的层次化实时系统。系统中既有根调度器，也有虚拟调度器和普通任务，另外还可能有共享资源与任务依赖。作者的目标是把这些对象全部放在一个 `UPPAAL` 模型中统一检查，而不是像 compositional analysis 那样切开后只看局部。

- 系统：多层调度器 + 虚拟资源 + 实时任务构成的层次化实时系统。
- 特点：多级调度、共享资源、任务依赖、preemption overhead。
- 规模：示例包括二层 target system，以及加入 `V2/T5/T6` 的三层扩展示例。
- 模型：根 `HS`、虚拟 `HS`、任务和资源模型的统一 `UPPAAL` 编码。
- 性质：系统是否始终 schedulable、共享资源是否引发 priority inversion、预算是否充足。
- 方法：以 `err` 变量汇总 deadline miss，再用 `A[] not err` 统一判断。
- 结果：基础 target system 满足，可通过修改共享资源和 budget 直接得到不可调度反例。

`层次化调度系统 -> 根/虚拟调度器 + 任务 + 资源建模 -> A[] not err -> 定位 priority inversion 与预算不足`

## 论文定位

本文是典型的 `⏱️` 主轴论文。它验证的不是某个控制器功能逻辑，而是层次化实时执行平台的调度正确性。因为案例本身较小且以框架展示为主，所以应标为 `🟡`，但其应用对象是真实的虚拟化实时系统而非纯理论模型。

## 验证对象与问题背景

### 系统与场景

对象是 hierarchical real-time system。虚拟化带来了隔离和易维护，但也让 schedulability 分析更复杂，因为调度器本身也形成了层次结构。

### 系统组成与运行机制

论文给出的基本定义是：

1. `RS = (W, R, S)`
2. `HS = (W_H, R, S)`

其中 workload `W` 可以包含普通任务，也可以包含下层 `HS`。根层调度器直接分配物理资源，其余层调度器则消费父层给定的 budget。

### 验证边界

论文验证的是**层次化调度语义**，不是具体应用软件功能。共享资源、依赖和 preemption overhead 都是为了更真实地表达调度行为。

### 核心问题

1. 纯组合式分析虽然高效，但不容易直观表达共享资源和优先级反转。
2. 全系统统一分析更准确，但容易爆炸。
3. 需要一个既能看全局行为、又能表达资源/依赖的正式模型。

## 模型与形式化建模

### 关键对象

框架输入包括：

1. 根层系统 `P = (W, R_P, S)`
2. 虚拟层系统 `V = (W, R_V, S)`
3. 任务 `T = (Pe, E, D, O, SR, Dep)`

### 关键建模点

1. 物理资源与虚拟资源区分对待。
2. 默认内置 `RM`、`EDF` 与 preemptive `FP` 调度。
3. 通过 preemption counts 计算新的执行时间：
   `$E_t = E'_t + (\Delta CXS + \Delta CMPD) * PRM_t$`

### 模型优势

作者强调该框架相比 partition-based compositional analysis 的优势在于：

1. 能直观加入共享资源和依赖关系。
2. 能显式统计 intra-scheduler / inter-scheduler preemption。
3. 能引入用户自定义调度策略。

## 验证目标与性质

### 待验证问题

1. 整个层次化系统是否 always schedulable。
2. 共享资源是否会造成 priority inversion。
3. 更新 preemption overhead 后给定 budget 是否仍足够。

### 性质类型

1. 调度安全性质。
2. 资源竞争相关性质。
3. deadline miss 可达性。

### 查询表达

案例统一使用的 `TCTL` 性质是：

`A[] not err`

其含义是：在任何执行路径上，变量 `err` 都不会变为真；而 `err` 一旦变真就表示某个任务错过 deadline。

## 核心方法与验证流程

1. 输入层次结构、任务参数、budget、资源和调度策略。
2. 建立统一 `UPPAAL` 模型。
3. 运行 `A[] not err` 检查整个系统是否 schedulable。
4. 若性质不满足，则读取 counter-example 分析是共享资源、预算还是依赖导致。
5. 若系统结构变化，再重复验证。

## 案例与结果

### 基础案例

论文先用表 1 中的 target system 演示：

1. 在没有共享资源的情况下，`A[] not err` 的验证结果为 `Satisfied`。

### 共享资源反例

随后作者加入共享资源 `SR0`：

1. 该案例得到 `Unsatisfied`。
2. 反例显示 `T1` 和 `T3` 共享资源会诱发 priority inversion。
3. 结果进一步导致 `T4` deadline miss。

### 预算与 overhead 更新

作者再利用表 2 的 preemption count 以及：

1. `CXS = 86.917 μs`
2. `CMPD = 139.12 μs`

更新执行时间后再次验证，结果仍为 `Unsatisfied`，原因是 `V0` 的 budget 不足以调度 `T1` 与 `T2`。

### 三层扩展

最后作者加入 `V2`、`T5`、`T6`，把系统扩展到三层层次结构。该扩展系统再次得到 `Satisfied`。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究的意义在于：它把多层调度器、任务和资源依赖都统一成了状态机级对象，为“系统级建模而不是局部拆分”提供了例子。

### 可借鉴之处

1. 用统一错误变量把复杂性质压缩成稳定查询。
2. 将资源竞争、preemption overhead 和层次结构放在一套模型里。
3. 用 counter-example 直接解释不可调度原因。

### 存在的不足与改进空间

1. 案例较小，更像框架验证样例。
2. 主要针对单核/单资源口径，作者自己也指出未来要扩到多核和共享资源协议。
3. 未公开工件。

### 对本研究的启发

对博士研究中的“验证剖面生成”来说，这篇论文说明：复杂执行平台的性质也可以被压缩成少数稳定的查询模板，如 `always no error`、budget sufficiency 和 resource-induced anomaly。

## 重要的相关工作

### 1. 组合式层次化分析

- 论文将自己的方法与 compositional analysis 做对比，强调统一全系统分析对共享资源更友好。

### 2. 航电应用

- 作者明确把未来目标指向航电系统，说明该框架面向的是严肃工业场景，而不是纯玩具例子。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未提供 `UPPAAL` 模型、表格输入文件或反例样例下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.1587/transinf.2016EDL8003)
- 对后续复用的现实影响：适合复用层次化调度建模框架，但要复跑需按正文重新编码。
