问题一句话：本文验证的是多电池使用调度，核心问题是在给定负载下，如何利用电池 recovery effect 找到比顺序放电更优的切换策略。
方法一句话：作者用 `KiBaM` 建模电池行为，再将离散化后的模型表示为 linearly priced timed automata，并在 `UPPAAL CORA` 中求使系统寿命最大的 battery schedule。
验证收获一句话：论文表明顺序放电明显次优，而 `TA-KiBaM` 最优策略在两块 `5 Ah` 电池的随机负载实验中平均可比 sequential scheme 提升约 `70%` 的系统寿命。

## 基本信息

- 标题：Computing Optimal Schedules of Battery Usage in Embedded Systems
- 中文标题：嵌入式系统中电池使用最优调度的计算
- 作者：Marijn Jongerden、Alexandru Mereacre、Henrik Bohnenkamp、Boudewijn Haverkort、Joost-Pieter Katoen
- 单位：University of Twente；RWTH Aachen University；Embedded Systems Institute
- 发表：IEEE Transactions on Industrial Informatics，2010
- DOI：`10.1109/TII.2010.2051813`
- 链接：[DOI](https://doi.org/10.1109/TII.2010.2051813)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🔋 能源与采能计算
- 被验证系统：含多电池/多电芯的嵌入式供电调度系统
- UPPAAL线：`UPPAAL CORA`
- 代码/模型/仓库获取方式：原文未提供独立 `UPPAAL CORA` 工程或脚本仓库。
- 案例/数据获取方式：论文给出 `KiBaM` 参数、随机负载生成方式和多种调度基线，可据正文重建实验。

## 简报

这篇论文的验证对象不是控制器状态机，而是“什么时候切换到哪块电池”这一资源调度问题。它把电池的 rate-capacity effect 与 recovery effect 都显式纳入模型，所以目标不只是平均分配，而是最大化整体可用寿命。

- 系统：多电池或 smart battery pack 供电的嵌入式设备。
- 特点：rate-capacity effect、recovery effect、切换时机与切换对象共同决定寿命。
- 规模：代表性实验包含两块 `5 Ah` 电池和 `500` 条随机负载轨迹。
- 模型：基于 `KiBaM` 的离散化 `LPTA` 模型，代价变量对应剩余电量/寿命损失。
- 性质：最大化 system lifetime，同时比较 sequential、round-robin、best-first 和最优策略。
- 方法：用 `UPPAAL CORA` 做 minimum-cost reachability，导出最优切换路径。
- 结果：顺序放电最差，最优策略在随机负载下显著拉开与基线的差距。

`KiBaM 电池模型 -> LPTA / cost 变量 -> UPPAAL CORA 最优路径 -> 最长寿命 schedule`

## 论文定位

这是典型的 `⏱️ + 🔋` 条目。尽管论文也给出解析法对照，但 `UPPAAL CORA` 路线本身已经构成一个明确的资源优化验证应用。

## 验证对象与问题背景

### 系统与场景

面向的系统是依赖电池供电的移动设备或嵌入式装置，尤其是可外挂电池或由多个 cells 组成的智能电池包。

### 系统组成与运行机制

关键对象包括：

1. batteries / cells
   - 各自具有可恢复的电荷状态。
2. load profile
   - 决定不同时间段的放电电流。
3. scheduler
   - 决定何时切换电池、切到哪块电池。

### 验证边界

本文验证的是**供电调度层**，不是电化学底层机理的高保真连续仿真，也不是具体嵌入式任务功能。

### 核心问题

简单顺序放电忽略了 recovery effect，可能把本可恢复的电量浪费掉，因此并不一定是寿命最优策略。

## 模型与形式化建模

论文先用 `KiBaM` 表示 available-charge well 与 bound-charge well，再离散化成 `dKiBaM`，最终建成 `LPTA`：

1. `Discharge automaton`
   - 描述当前被选中电池的放电。
2. `Recovery automaton`
   - 描述未被使用时的恢复过程。
3. `cost` 变量
   - 累积寿命损失或剩余电量代价。

这样 `UPPAAL CORA` 就可以把“求最优 schedule”转成 cost-optimal reachability。

## 验证目标与性质

### 待验证问题

1. 在给定负载下，哪些切换策略寿命更长；
2. 最优策略与顺序放电、round-robin、best-first 相差多少；
3. 调度决定和允许的 switching points 对寿命的影响有多大。

### 性质类型

- 成本/寿命最优性
- 资源调度性质
- 定量性能比较

### 查询表达

论文把问题落在 `UPPAAL CORA` 的 minimum-cost reachability 上，即寻找使总剩余损失最小、系统寿命最长的路径。

## 核心方法与验证流程

1. 用 `KiBaM` 建立电池充放电与恢复模型。
2. 离散化为 `dKiBaM`。
3. 构造 `LPTA` 自动机网络。
4. 将调度选择留为 nondeterministic。
5. 用 `UPPAAL CORA` 搜索 cost-optimal schedule。
6. 与 sequential、round-robin、best-first 和解析法对照。

## 案例与结果

论文的关键结果包括：

1. `TA-KiBaM` 生成的调度显著优于 sequential discharge。
2. 对两块 `5 Ah` 电池和 `500` 条随机负载轨迹，平均寿命相较 sequential 提升约 `70%`。
3. round-robin 与 best-first 有时接近最优，但在若干场景下仍明显落后。
4. 解析法还揭示：允许更多 switching points 往往比“选哪块电池”本身更关键。

## 与本研究的关系

### 相关性分析

这篇论文体现了如何把“资源恢复效应”编进状态机模型，并用形式化最优路径搜索回答工程调度问题。

### 可借鉴之处

1. 把连续物理对象抽象成适合 timed automata 的双井模型。
2. 让 nondeterministic choices 代表待综合的调度动作。
3. 用 cost-optimal reachability 把验证和优化连在一起。

### 存在的不足与改进空间

原文未公开完整模型，且电池模型依然是离散化抽象，不是电化学高精度仿真。

### 对本研究的启发

它说明博士研究中的“性质”完全可以是寿命、代价、资源占用这类定量目标，而不必局限于纯布尔安全/活性性质。

## 重要的相关工作

### 1. `KiBaM`

- 论文把 recovery-aware 电池模型直接嵌进形式化验证流程。

### 2. `UPPAAL CORA`

- 其关键价值在于把 schedule synthesis 转成 cost-optimal path 搜索。

### 3. 解析法对照

- 论文不是只给出工具结果，还用解析法解释为什么更多切换点会更优。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未见独立 `UPPAAL CORA` 模型、查询文件和负载脚本仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1109/TII.2010.2051813)
- 对后续复用的现实影响：很适合作为“资源调度 + 恢复效应 + 最优路径”案例，但若要复现论文数值仍需自行实现离散化模型。
