问题一句话：本文验证的是 `ROS 2` 应用中的 callback latency 和 buffer overflow，核心问题是如何用可复用的 pattern-based 模型模板，把 `ExV1/ExV2` 执行器、topic/service 通信和节点执行整体纳入 `UPPAAL` 分析。
方法一句话：作者提出三类 callback 模板、executor 模板和 communication topic 模板，支持 individual-node 与 holistic 两种建模方式，并在 `SC1-SC3` 三个场景上比较 `ExV1/ExV2`、输入/输出缓冲区和延迟抖动行为。
验证收获一句话：论文显示 pattern-based 建模既能精确复现实验轨迹，也能发现现实运行中未必恰好出现的潜在高延迟路径与 buffer overflow；其中 `SC2` 抓住了 `ExV2` 下 timer callback 实例丢失，`SC3` 还揭示了“更低 latency 可能只是因为 overflow 导致消息丢了”的反直觉现象。

## 基本信息

- 标题：Pattern-based verification of ROS 2 applications using UPPAAL
- 中文标题：基于模式的 `ROS 2` 应用 `UPPAAL` 验证
- 作者：Lukas Dust、Rong Gu、Cristina Seceleanu、Mikael Ekström、Saad Mubeen
- 单位：Mälardalen University
- 发表：International Journal on Software Tools for Technology Transfer 2025
- DOI：`10.1007/s10009-025-00802-4`
- 链接：[DOI](https://doi.org/10.1007/s10009-025-00802-4)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：`ROS 2` 节点、executor、callback 和通信链路组成的分布式机器人应用
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文明确给出完整模型页面 [pbvros2nodes](https://sites.google.com/view/pbvros2nodes)。
- 案例/数据获取方式：论文给出可复用模板与实验场景模型；未附真实工业数据集，但模型工件公开。

## 简报

这篇论文关注的是 `ROS 2` 执行语义本身，尤其是 callback latency 和 buffer overflow。它的强项不只是建一个案例，而是把建模过程模板化，使后续 `ROS 2` 节点、executor 和通信链路都能按 pattern 复用。

- 系统：`ROS 2` 节点中的 callbacks、executors、topics / services 和处理链。
- 特点：同时支持 `ExV1` 与 `ExV2`，支持 holistic 与 individual 两种建模方式。
- 规模：核心实验包含 `SC1`、`SC2`、`SC3` 三个场景，覆盖 sporadic callbacks、periodic callbacks、input/output buffer overflow。
- 模型：三类 callback 模板（data / sporadic / periodic）+ executor 模板 + topic 模板。
- 性质：callback latency、输入/输出缓冲区溢出、调度轨迹一致性。
- 方法：先和真实 `ROS 2` 轨迹对比，再用模型检查搜索潜在坏路径。
- 结果：`SC1` 的 latency 与真实执行对齐；`SC2` 抓到 `ExV2` 下 timer callback 实例丢失；`SC3` 证明更低 latency 可能是 overflow 的假象。

`ROS 2 执行语义 -> pattern-based UTA 模板 -> individual / holistic 建模 -> latency / overflow 查询 -> 对比真实轨迹并发掘潜在坏路径`

## 论文定位

这是非常强的 `ROS 2` 执行与缓存行为应用论文。虽然也有方法贡献，但落点始终是具体 `ROS 2` 应用的 callback 执行与通信链验证，因此仍应算作 `uppaal_apps` 中的机器人应用案例。

## 验证对象与问题背景

### 系统与场景

被验证对象是 `ROS 2` 应用中 callback、executor 和 communication channel 组成的执行链。作者特别关注 `ExV1` 与 `ExV2` 两个单线程 executor 版本的行为差异。

### 系统组成与运行机制

论文显式建模了：

1. **四类 communication patterns**
   - publisher-subscriber、service-client 等。
2. **三类 callback templates**
   - `Data Callback`、`Sporadic Callback`、`Periodic Callback`。
3. **Executor template**
   - 调度 ready set 中的 callbacks。
4. **Topic template**
   - 负责数据传播、delay、jitter 和 output buffer。

### 验证边界

本文验证的是**`ROS 2` 执行语义、callback 调度和通信缓冲行为**，不是机器人任务逻辑本身。

### 核心问题

`ROS 2` 的困难在于：

1. timer callbacks 与 data callbacks 释放机制不同；
2. `ExV1` 和 `ExV2` 对 timers 的处理顺序不同；
3. 缓冲区溢出会导致 callback instance miss；
4. 仅靠实验往往看不到全部潜在执行路径。

### 研究动机

作者要解决的是：怎样用可复用模板降低形式化建模成本，让 `ROS 2` 应用的 latency 和 overflow 检查成为可重复工作流。

## 模型与形式化建模

### 模板体系

论文提出三类 callback 模板：

1. `Data Callback`
2. `Sporadic Callback`
3. `Periodic Callback`

每个 callback 模板都统一包含：

1. `Waiting`
2. `Released`
3. `InReadySet`
4. `Execution`

并使用 buffer utilization、release times 和 latency clocks 跟踪执行。

### 两种建模方式

1. **Individual approach**
   - 把节点单独建模，通信抽象成 release times。
2. **Holistic approach**
   - 将通信链路一并建模，topics 真实触发 data callbacks。

### `ExV1 / ExV2`

论文特别指出两种 executor 的差别：

1. `ExV1` 中 timer callbacks 被持续优先考虑；
2. `ExV2` 中 timers 只有在 polling point 才被纳入 ready set。

这直接影响 latency 和 overflow。

## 验证目标与性质

### 待验证问题

1. callback 最大 latency 是多少；
2. 输入缓冲区是否会 overflow；
3. 输出缓冲区是否会 overflow；
4. 不同 executor 版本是否导致实例丢失；
5. holistic 与 individual 建模结果有何差别。

### 性质类型

1. 有界响应；
2. 资源/缓冲区安全；
3. 调度与执行轨迹一致性。

### 查询表达

论文围绕：

1. buffer overflow eventual reachability；
2. `sup` 型 latency 计算；
3. 生成 counterexample traces

来完成分析。

## 核心方法与验证流程

1. 用模板快速拼出场景模型。
2. 先在真实 `ROS 2` 系统中录制执行轨迹。
3. 再用 `UPPAAL` 生成模拟轨迹，与真实轨迹核对。
4. 对 latency 和 overflow 运行 model-checking 查询。
5. 当模型找到更坏路径时，分析其是否为理论可达而未在实验中显现的执行。

作者特别强调：模型检查可以找到“真实系统未来某次可能出现，但这次实验没碰上的坏路径”。

## 案例与结果

### `SC1`

`SC1` 关注 sporadic callbacks。表 1 显示，无论 `ExV1` 还是 `ExV2`，real trace、individual 和 holistic 三者得到的多组 latency 基本一致，例如 `H/M/L/SH/SM/SL` 等 callbacks 的 latency 与真实执行对齐。

### `SC2`

`SC2` 用 periodic timer + 消息序列触发复杂争用。论文指出：

1. 在 `ExV2` 中，timer `T0` 虽被释放 `6` 次，却只执行 `4` 次；
2. 原因是 input buffer overflow 导致 instance miss；
3. `UPPAAL` 的结果和真实执行吻合。

### `SC3`

`SC3` 专门研究 output buffer。表 4 给出：

1. buffer size 为 `3` 时，在 `delay=0/1` 或 `jitter=1` 下均无 overflow；
2. buffer size 为 `2` 时三种设置都可能 overflow；
3. 更反直觉的是：某些情况下 latency 反而更低，但那是因为 overflow 让一部分数据直接丢了，不是系统更好。

### 工程意义

因此，这篇论文的价值不仅是“计算 latency”，还在于提醒工程师不能把低 latency 直接等同于好配置。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的关系在于：它展示了如何通过模式化抽象，把复杂中间件执行语义转换为一组可复用状态机模板。

### 可借鉴之处

1. 用模板化方式降低单篇建模成本。
2. 把 executor 版本差异显式建成模型元素。
3. 用真实轨迹和模型轨迹双向校验模型可信度。

### 存在的不足与改进空间

1. 聚焦执行语义，不涉及更高层机器人行为正确性。
2. 结果仍依赖对 release 假设和 abstraction level 的选择。
3. 更复杂分布式部署和多线程 executor 还可继续扩展。

### 对本研究的启发

它很适合用来思考“状态机模板库”如何服务后续自动建模，也说明验证结果必须结合“overflow 是否导致语义损失”来解释。

## 重要的相关工作

### 1. `ROS 2` executor 语义

- 论文把 `ExV1` / `ExV2` 的行为差异转成形式模型，是其关键贡献之一。

### 2. Pattern-based modeling

- 模板复用不是附带技巧，而是全文方法主轴。

### 3. `UPPAAL`

- `UPPAAL` 在这里同时用于轨迹复现、latency 计算和 overflow 搜索。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文明确给出完整模型站点，当前可访问。
- 获取方式/链接：[DOI](https://doi.org/10.1007/s10009-025-00802-4)；[完整模型页面](https://sites.google.com/view/pbvros2nodes)
- 对后续复用的现实影响：这是当前文库里公开度很高的 `ROS 2` 执行语义案例，适合作为模板化建模和 callback 性质验证的直接参考。
