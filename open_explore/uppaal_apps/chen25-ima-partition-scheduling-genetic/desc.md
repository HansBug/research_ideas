问题一句话：本文验证的是 `ARINC-653` 集成模块化航电系统的分区调度设计，核心问题是在满足所有任务 deadline 的前提下，分区 `period/budget` 参数能否被自动优化到更低的处理器占用率。
方法一句话：作者把 `IMA` 两层调度系统建成 `UPPAAL` 的 timed/stopwatch automata，并用并行遗传算法 `MBGA` 在集群上搜索候选参数，再用组合式模型检查独立验证各分区可调度性。
验证收获一句话：在简单基准上，`MBGA` 找到与 exhaustive search 相同的全局最优 `45.1%` 占用率；在 `5` 分区航电负载上，又把经验方案的 `100%` 占用率压到 `83%`，同时排除了 deadline miss。

## 基本信息

- 标题：Model-based partition scheduling of integrated modular avionics systems using genetic algorithm
- 中文标题：使用遗传算法的集成模块化航电系统分区调度模型驱动优化
- 作者：Jichen Chen、Zhengjun Zhai、Pujie Han、Min Huang
- 单位：Northwestern Polytechnical University
- 发表：Scientific Reports，2025
- DOI：`10.1038/s41598-025-16745-4`
- 链接：[DOI](https://doi.org/10.1038/s41598-025-16745-4)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🚀 航空航天与国防
- 被验证系统：`ARINC-653` 航电 `IMA` 平台中的全局分区调度与分区内任务调度
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供独立 `UPPAAL` 模型、集群脚本或 `MBGA` 实现仓库。
- 案例/数据获取方式：论文公开给出两个实验任务集、优化参数、集群配置和最终分区参数，可据正文重建。

## 简报

这篇论文的核心不是“设计一个更快的遗传算法”，而是让 `UPPAAL` 真正进入 `ARINC-653` 分区调度优化闭环。作者把“候选参数是否可调度”这件事仍交给模型检查来裁决，而不是用解析近似代替。

- 系统：`ARINC-653` 两层调度系统，外层 `TDM` 分区调度，内层分区内 `FP` 任务调度。
- 特点：同时支持单核/多核、strictly periodic 与 loosely periodic partitions、执行时间区间、核绑定和 context-switch overhead。
- 规模：简单实验为 `2` 分区 `8` 任务；复杂实验为 `5` 分区、`22` 个任务、`4` 个处理器核。
- 模型：`Partition Scheduler`、`Task Scheduler` 和 `Task Template` 三类 `UPPAAL` 模板，结合 stopwatch 表达任务执行区间。
- 性质：核心查询是所有任务都不能进入 `deadlineMissed`。
- 方法：并行遗传算法生成候选 `period/budget`，调度表生成器构造 `ARINC-653` schedule，再由分区级组合式模型检查判定可调度性。
- 结果：`MBGA` 在简单系统上达到全局最优，在复杂系统上显著优于经验方案。

`IMA 工作负载 -> 分区参数编码 -> 调度表生成 -> 分区级 UPPAAL 验证 -> fitness 回写 -> 输出低 occupancy 可调度方案`

## 论文定位

这是典型的 `⏱️ + 🚀` 条目。它虽然使用遗传算法，但论文真正想解决的是“复杂航电系统的分区调度可调度性如何在形式化约束下被联合优化”，因此仍属于强调验证边界的 schedulability 应用论文。

## 验证对象与问题背景

### 系统与场景

对象是 `ARINC-653` 标准下的 `IMA` 系统。多个应用以 temporal partition 的方式共享硬件平台，每个分区内部再运行自己的实时任务集。

### 系统组成与运行机制

1. 全局层
   - `TDM` scheduler 按 major time frame 周期性激活各 partition。
2. 局部层
   - 每个 partition 内部用 preemptive fixed-priority 调度任务。
3. 任务模型
   - 每个任务包含 period、initial offset、`BCET/WCET`、deadline、priority 和 core binding。

### 验证边界

论文验证的是分区调度与任务时序行为，不涉及航电功能算法本身，也不验证实际操作系统实现代码。

### 核心问题

1. 解析方法往往过于保守，浪费处理器时间。
2. `ARINC-653` 的两层调度、严格/宽松周期分区和多核绑定使参数空间高度非线性。
3. 传统参数综合工具在这种高维离散搜索上很难终止。

### 研究动机

作者希望让形式模型既保留 schedulability 判断精度，又能进入自动搜索流程，从而得到更可用的分区参数。

## 模型与形式化建模

### 抽象对象

作者把 `IMA` 系统抽象成：

1. partition scheduler
2. task scheduler
3. periodic task automata

每个 partition 都由自己的时间窗集合 `Wi` 驱动，并映射成独立可验证的 `UPPAAL` 实例模型。

### 建模形式

1. timed automata 负责调度逻辑。
2. stopwatch automata 负责表达任务执行区间和可暂停执行。
3. 调度表以数组结构输入 `UPPAAL` 模型。

### 关键抽象与取舍

1. 采用 compositional model checking，把系统拆成分区级验证，降低状态爆炸。
2. 只要 `UPPAAL` 返回 `Satisfied (unreachable)`，就把 `Unschedulable` error state 视为 definitively unreachable。
3. 参数空间不直接用 parametric synthesis，而是改用固定值候选的迭代搜索。

## 验证目标与性质

### 待验证问题

1. 给定调度表下每个 partition 是否 schedulable。
2. 是否能找到更低 processor occupancy 的全局参数。
3. 不同优化方法在简单/复杂航电任务集上谁更接近全局最优。

### 性质类型

- 可调度性
- deadline 安全
- 资源/处理器占用优化

### 查询表达

论文把 schedulability 写成“任何任务都不会进入 `deadlineMissed`”，对应 `UPPAAL` 查询：

1. `A[] not deadlineMissed`

### 判定边界与前提

stopwatch 模型在 `UPPAAL` 中依赖 over-approximate reachability。论文因此把“error state definitely unreachable”的正结论视为可靠，而把可能可达视作保守警报。

## 核心方法与验证流程

1. 用个体向量编码每个 partition 的 `period/budget`。
2. 通过 demand decoder 与调度表生成器构建候选 `ARINC-653` scheduling table。
3. 将每个 partition 独立实例化为 `UPPAAL` 模型。
4. 并行运行 `UPPAAL`，汇总各 partition 的 schedulability。
5. 用可调度分区数量和 processor occupancy 计算 fitness。
6. 在集群上执行 `selection/recombination/mutation`，输出最佳参数。

## 案例与结果

### 实验平台

优化器用 Python 实现，运行在 `4` 节点集群上，共 `128` 个核心，每节点 `512 GB` 内存，节点间 `40 Gbps InfiniBand` 互连。

### 实验 1：简单航电系统

系统包含 `2` 个 partitions、每个分区 `4` 个任务。结果如下：

1. Exhaustive Search 与 `MBGA` 都得到 `(1600,341,1600,341)`。
2. 最优 processor occupancy 为 `45.1%`。
3. `GA1`、`GA2` 只停在 `59.5%` 和 `47.5%` 的局部最优。
4. 几何规划法得到 `67.8%`，明显更保守。

### 实验 2：复杂航电系统

表 `4` 给出 `5` 个 partitions、`22` 个 tasks、`4` 个 cores 的 concrete avionics task set。结果如下：

1. 经验方案 `(25,4.8,25,4.8,25,4.8,25,4.8,25,4.8)` 占用率 `100%`，仍不可调度。
2. `UPPAAL` 返回反例，指出 `τ1_3` 在 `50.2 ms` 时 miss deadline。
3. `MBGA` 运行 `200` 代、总时长 `26 h 23 min`，找到 `(25,4.9,25,4.7,25,3.4,25,4.5,50,4.5)`。
4. 最终 processor occupancy 为 `83%`。

### 结果解释

论文表明：在复杂 `ARINC-653` 系统里，局部最优 partition 参数并不能自动拼成全局最优；形式验证必须直接嵌入全局搜索回路。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究中的“生成-验证-修复”闭环很接近，只不过它修的不是状态机结构，而是时间参数与资源配置。

### 可借鉴之处

1. 先用形式模型裁决 candidate，再把结论反馈给优化器。
2. 用组合式验证拆掉 monolithic model 的状态爆炸。
3. 用领域知识定制编码和遗传算子，而不是直接套通用 GA。

### 存在的不足与改进空间

1. 没有公开完整模型与优化实现。
2. 复杂实验耗时仍然很长。
3. 核心关注 schedulability，对消息交互和锁竞争的实际系统细节展开有限。

### 对本研究的启发

如果后续要让 `LLM` 自动给出时序参数或验证 profile，这篇论文说明“候选生成”与“形式验证裁决”应当显式分层，而不是把验证退化成纯启发式评分。

## 重要的相关工作

### 1. `ARINC-653` schedulability

- 论文直接延续了 `UPPAAL` 在航电层次化调度上的系列工作，但把目标推进到全局分区参数优化。

### 2. 参数综合工具

- 文中专门比较了 `IMITATOR` 路线，指出高维有理参数综合在该问题上计算上不可行。

### 3. 经典遗传算法与解析优化

- `GA1/GA2/GP` 在论文里都被作为对照，反过来凸显出“形式模型 + 定制算子”的必要性。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文和任务表公开，实验平台与最优参数也写得较细，但未公开独立 `UPPAAL` 模型、调度表生成器或 `MBGA` 代码。
- 获取方式/链接：[DOI](https://doi.org/10.1038/s41598-025-16745-4)
- 对后续复用的现实影响：适合作为航电分区调度优化的强样本，但要复跑仍需自行重建模型与搜索流程。
