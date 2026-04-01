问题一句话：本文验证的是 `ARINC-653` 航电分区调度系统，核心问题是在保证全局与局部可调度性的前提下，分区 `period/budget` 参数能否被自动优化到更低的处理器占用率。
方法一句话：作者把 `IMA` 两层调度系统建成 `UPPAAL` timed automata，并用 `EA4HS` 做参数搜索，同时结合 `UPPAAL SMC` 的快速统计筛查和经典 `UPPAAL` 的组合式验证。
验证收获一句话：在复杂航电工作负载上，经验性 `5 ms` 等长分区方案不可调度，而自动搜索得到的 `(25,4.9,25,4.7,25,3.4,25,4.5,50,4.5)` 方案把 processor occupancy 压到 `82.6%` 且通过验证。

## 基本信息

- 标题：Model-based optimization of ARINC-653 partition scheduling
- 中文标题：基于模型的 `ARINC-653` 分区调度优化
- 作者：Pujie Han、Zhengjun Zhai、Brian Nielsen、Ulrik Nyman
- 单位：Northwestern Polytechnical University；Aalborg University
- 发表：International Journal on Software Tools for Technology Transfer，2021
- DOI：`10.1007/s10009-020-00597-6`
- 链接：[DOI](https://doi.org/10.1007/s10009-020-00597-6)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🚀 航空航天与国防
- 被验证系统：`ARINC-653` 集成模块化航电系统中的分区调度参数配置
- UPPAAL线：`UPPAAL` + `UPPAAL SMC`
- 代码/模型/仓库获取方式：原文未提供独立 `UPPAAL` 模型、`EA4HS` 实现或参数搜索脚本的公开仓库。
- 案例/数据获取方式：论文给出了 `3` 组实验工作负载与任务表，尤其是 `5` 个分区、`18` 个 periodic tasks、`4` 个 sporadic tasks 的复杂案例，可据正文重建。

## 简报

这篇论文验证的不是单个控制器，而是航电 `IMA` 平台中“怎样给各分区分时”的设计问题。其重点在于：分区时间参数一旦定下，不只决定局部任务能否按时完成，也决定整机是否还有余量容纳更多应用。

- 系统：`ARINC-653` 两层调度系统，外层是 `TDM` 分区调度，内层是分区内 `FP` 任务调度。
- 特点：同时考虑全局时间片、局部任务 deadline、资源共享、sporadic task 与分区间消息通信。
- 规模：复杂实验包含 `5` 个 partitions、`18` 个 periodic tasks、`4` 个 sporadic tasks、`3` 个 locks 和 `4` 类 message types。
- 模型：每个 partition、local scheduler、task type 和通信/资源行为都被抽成 `UPPAAL` timed automata。
- 性质：既要满足 schedulability，又要最小化 processor occupancy。
- 方法：`EA4HS` 搜索候选参数；`UPPAAL SMC` 先快速 falsify；经典 `UPPAAL` 再对候选做严格验证。
- 结果：小规模实验可达到和 exhaustive search 相同的最优值；大规模案例中自动搜索优于工程经验配置。

`ARINC-653 任务集 -> timed automata 调度模型 -> SMC 快速筛查 -> 经典 MC 严格验证 -> 选出更低 occupancy 的 schedulable 参数`

## 论文定位

这是一篇很典型的 `⏱️ + 🚀` 条目。它虽然带优化器和进化算法，但核心仍是“用 `UPPAAL` 判断候选分区参数是否满足可调度性”，因此属于调度/资源验证应用，而不是纯优化算法论文。

## 验证对象与问题背景

### 系统与场景

论文场景是 `ARINC-653` 标准下的集成模块化航电系统。多个实时应用共享同一处理器，但通过时间分区实现隔离。

### 系统组成与运行机制

系统有两层关键结构：

1. 全局 `TDM` scheduler
   - 按 major frame 循环给各分区分配预算。
2. 分区内 local scheduler
   - 在本分区里按 preemptive fixed-priority 调度任务。
3. 任务与交互行为
   - 同时存在 periodic / sporadic tasks，以及锁和消息通信。

### 验证边界

本文验证的是**分区调度参数层**，不是整个航电应用功能逻辑，也不是真实操作系统内核实现。

### 核心问题

分区 `period/budget` 给少了会不可调度，给多了又会浪费 CPU 余量，降低后续集成空间。对复杂航电任务集，这个权衡已经超出简单解析式能可靠处理的范围。

### 研究动机

作者希望把“给定参数 -> 检查可调度”推进为“自动搜索参数 -> 快速否定坏候选 -> 严格确认好候选”的完整闭环。

## 模型与形式化建模

论文把分区调度系统抽成一组 `UPPAAL` timed automata：

1. `PartitionSupply` 类结构描述全局分区供给。
2. `PeriodicTask` 与 `SporadicTask` 模板描述任务释放和执行。
3. `LocalScheduler` 描述分区内 ready queue 与抢占规则。
4. 锁、消息通信和上下文切换开销进入 task chunk 抽象。

对复杂案例，论文显式保留了 task dependency、锁与 inter-partition message，而不是只用解析法里的简化任务模型。

## 验证目标与性质

### 待验证问题

1. 给定分区参数是否 schedulable；
2. 哪组参数能在 schedulable 前提下让 processor occupancy 最低；
3. 小规模最优解能否与 exhaustive search 对齐；
4. 大规模复杂系统里经验配置与模型驱动优化相比差多少。

### 性质类型

- 调度性质
- deadline 安全性质
- 资源与时间约束
- 统计快速筛查性质

### 判定边界与前提

`UPPAAL SMC` 在这里主要负责快速 falsification；真正的 schedulable 结论仍要回到经典 `UPPAAL` 做严格验证。

## 核心方法与验证流程

1. 将 `IMA` 工作负载翻译成 `UPPAAL` 执行模型。
2. 把分区 `period/budget` 作为参数搜索空间。
3. 用 `EA4HS` 生成候选参数组合。
4. 对每个候选先用 `UPPAAL SMC` 快速排除明显不可调度方案。
5. 通过 SMC 的候选再用组合式经典模型检查验证。
6. 以 processor occupancy 作为优化目标选择最终方案。

## 案例与结果

论文包含三组实验：

1. 实验 `1`
   - `2` 个 partitions，每个分区 `4` 个独立 periodic tasks，可与 exhaustive search 对照。
2. 实验 `2`
   - 扩大参数范围，用于比较不同进化算子组合。
3. 实验 `3`
   - `5` 个 partitions、`18` 个 periodic tasks、`4` 个 sporadic tasks 的真实复杂航电案例。

关键结果是：

1. 小规模案例中，`EA4HS` 能找到与 exhaustive search 相同的全局最优参数。
2. 大规模案例里，经验方案 `(25,4.8,25,4.8,25,4.8,25,4.8,25,4.8)` 不可调度，且 occupancy 达 `100%`。
3. 自动搜索得到 `(25,4.9,25,4.7,25,3.4,25,4.5,50,4.5)`，通过 `UPPAAL SMC` 和经典 `UPPAAL` 双重确认，occupancy 降为 `82.6%`。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究中的“状态机建模 + 验证 + 约束修复/优化”高度贴近，只不过它的对象是调度参数而不是控制状态图结构。

### 可借鉴之处

1. 用同一份 `UPPAAL` 模型同时服务 falsification 和严格验证。
2. 把复杂任务行为抽象为 chunk 序列，兼容锁和通信。
3. 先快速筛掉坏候选，再对少量好候选做昂贵验证。

### 存在的不足与改进空间

原文没有公开完整模型和优化器实现，因此复现仍需自行重建。

### 对本研究的启发

它说明“生成-验证-修复”闭环并不只适用于状态结构修复，也可以外推到时间参数、预算和资源配置的自动修补。

## 重要的相关工作

### 1. `ARINC-653` / `IMA` 调度分析

- 本文直接针对航电分区调度标准中的 `period/budget` 参数进行优化。

### 2. `UPPAAL SMC` 与经典 `UPPAAL` 结合

- 论文把统计快速筛查与严格模型检查串成一条工程化流程。

### 3. 进化搜索与形式化验证结合

- `EA4HS` 不是单独跑黑盒仿真，而是持续调用 `UPPAAL` 验证器反馈搜索方向。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文可公开获取，任务表和参数结果也较完整，但未提供独立 `UPPAAL` 模型、查询文件和 `EA4HS` 代码。
- 获取方式/链接：[DOI](https://doi.org/10.1007/s10009-020-00597-6)
- 对后续复用的现实影响：适合作为“航电分区调度参数如何通过模型检查做自动优化”的强样本，但若要复跑结果，仍需按正文重建模型与搜索流程。
