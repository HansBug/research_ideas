问题一句话：本文验证的是 `ROS`/`ROS 2` 机器人应用的端到端反应时间，核心问题是在执行时间非确定、相机负载概率化以及定时/事件触发任务并存时，系统还能否满足 deadline。
方法一句话：作者给 `ROS` 设计赋予 timed automata 与 stochastic timed automata 语义，用 `UPPAAL` / `UPPAAL SMC` 分别处理确定性与概率化场景，并在一个相机引导工业机器人案例上分析最大 reaction time。
验证收获一句话：论文不仅复现并扩展了已有 deterministic 结果，还显示在工业案例中，当 camera 数量和 load 提升后，`850` 时间单位的 deadline 会快速失守；同时 subscription-based fusion 未必更优，说明建模可以直接辅助架构选型。

## 基本信息

- 标题：Verifying ROS-Based Applications Using Timed and Stochastic Timed Automata
- 中文标题：使用 timed 与 stochastic timed automata 验证 `ROS` 应用
- 作者：Peter Backeman、Cristina Seceleanu
- 单位：Mälardalen University
- 发表：Rebeca for Actor Analysis in Action 2025
- DOI：`10.1007/978-3-031-85134-6_13`
- 链接：[DOI](https://doi.org/10.1007/978-3-031-85134-6_13)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：`ROS`/`ROS 2` 机器人应用的任务链与工业视觉反应链路
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文明确给出 [ptrbman/ros2-modeling](https://github.com/ptrbman/ros2-modeling/) 仓库。
- 案例/数据获取方式：案例来自工业相机引导机器人系统；论文给出参数化模型和代码仓库，但不附真实生产数据集。

## 简报

这篇论文验证的不是单个 callback，而是从传感器输入到控制动作输出的端到端 reaction time。其关键价值在于：它先给出确定性 timed automata 语义，再把执行时间和输入负载推广为概率化对象，使 `ROS` 设计可以在更接近真实负载的条件下被分析。

- 系统：`ROS`/`ROS 2` 任务链以及工业 camera-guided robotic system。
- 特点：同时考虑 periodic / event-triggered task、非确定执行时间和 probabilistic load。
- 规模：工业案例包含 cameras、object detection、fusion、managing/actuation；表 4 给出 `Camera WCET=20`、period `1000`，`Object Detection WCET=50`，`Fusion Timer WCET=90`、period `500`，`Managing/Actuation WCET=50`。
- 模型：timed automata + stochastic timed automata，配合 `UPPAAL` / `UPPAAL SMC`。
- 性质：最大 reaction time、deadline violation 概率、不同 fusion 架构的性能比较。
- 方法：先验证基础语义，再在工业案例上扫 camera 数量和负载概率。
- 结果：`>5` cameras 时，在 `10000` 步设置下就可能违反 `850` deadline；扩到 `100000` 步后，可接受负载更低；subscription-based fusion 对后续 camera 甚至更差。

`ROS 设计模式 -> TA / STA 语义 -> 最大 reaction time 查询 -> 工业相机机器人案例 -> 架构与负载敏感性分析`

## 论文定位

这是一篇很强的 `ROS` 性能与反应时间应用论文。虽然对象最终是机器人系统，但真正验证的是任务链端到端时延和 deadline 风险，因此放在 `⏱️` 主轴最合适。

## 验证对象与问题背景

### 系统与场景

被验证对象是 `ROS`/`ROS 2` 应用中的任务链。论文最终采用一个工业启发案例：机器人通过多个相机观测环境，经 object detection、fusion 和 managing/actuation 后对障碍物作出动作。

### 系统组成与运行机制

工业案例链路包括：

1. **Camera nodes**
   - 周期产生感知输入。
2. **Object Detection**
   - 对图像做处理。
3. **Fusion**
   - 合并多路结果，可做 timer-based 或 subscription-based 设计。
4. **Managing/Actuation**
   - 根据融合结果发出控制动作。

### 验证边界

论文验证的是**任务调度、执行时间与输入负载共同决定的端到端 reaction time**，不是完整运动控制或视觉算法精度。

### 核心问题

`ROS` 应用的难点在于：

1. 任务执行时间常是区间或随机变量；
2. 数据生成可能是概率性的；
3. 有些任务定时触发，有些事件触发；
4. 最大 reaction time 不能只靠单次仿真猜测。

### 研究动机

作者要回答的是：模型检查能否帮助在设计阶段就给出 reaction time 上界和 deadline 风险，而不是等到系统跑起来再做经验性测试。

## 模型与形式化建模

### 基础语义

论文首先为 `ROS` 设计赋予 timed automata 语义，用于精确描述：

1. task release；
2. scheduling；
3. task-chain 中数据沿各任务传播；
4. reaction time 的度量。

### 随机扩展

随后作者将其推广为 stochastic timed automata，以便表达：

1. 非确定执行时间；
2. probabilistic data generation；
3. 统计意义上的 deadline violation。

### Reaction time 定义

论文给出了 task-chain 和 maximum reaction time 的明确定义，并以 monitor 自动机跟踪任务链开始和结束之间的时间差。

## 验证目标与性质

### 待验证问题

1. 给定任务链的最大 reaction time 上界是多少；
2. 在一定时间窗口内，reaction time 超过阈值 `t` 的概率是否低于给定门限；
3. 架构替换是否改善 deadline 满足性。

### 性质类型

1. 有界响应；
2. 概率性质；
3. 架构比较与容量边界。

### 查询表达

论文既使用确定性查询寻找最坏 reaction time，也使用 `UPPAAL SMC` 查询估计：

1. 在 `10000` 或 `100000` 时间步内；
2. reaction time 超过 `850` 的概率是否低于 `5%`；
3. 置信度设为 `95%`。

## 核心方法与验证流程

1. 给 `ROS` 设计模式建立 TA 语义。
2. 先和已有 deterministic 结果对比，验证模型可信。
3. 再扩展为带非确定执行时间和概率负载的 STA 语义。
4. 将工业案例参数化为 camera 数、激活概率、fusion 架构与周期。
5. 通过 `UPPAAL SMC` 评估 deadline 风险。

这样，模型检查不只是“证性质”，也变成了设计空间探索工具。

## 案例与结果

### 基础工业案例

表 4 给出的默认参数已经足以构成一个较完整的视觉反应链。论文在此基础上分析不同 camera 数和 load。

### `10000` 步设置

表 5 表明：

1. 当 camera 数提升后，系统很快接近或超过 `850` 的 reaction time deadline；
2. 超过 `5` cameras 时，风险已经明显上升；
3. 对单个 camera 的监控结果在对称设置下可代表其他 camera。

### `100000` 步设置

表 6 进一步显示，运行时间窗口加长后，可接受负载更低：

1. `75%` load 下只剩 `2` cameras 仍安全；
2. `50%` load 下大约 `3` cameras 仍安全。

### 架构替换

将 fusion 从 timer-based 改为 subscription-based 后：

1. 第一条 camera 路径可能更快；
2. 但其他 cameras 的 reaction time 明显恶化；
3. 文中甚至指出观察 camera 3 时，连 `2` cameras 场景都可能不安全。

这使论文具备直接指导系统架构选择的价值。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的关系在于：它展示了如何把现实系统的任务链、调度和概率负载都纳入统一状态机语义。

### 可借鉴之处

1. 将端到端 reaction time 作为一类明确性质对象。
2. 用 deterministic + stochastic 双语义覆盖不同验证深度。
3. 让验证结果直接支持架构比较，而不只是“是否满足”。

### 存在的不足与改进空间

1. 案例依然是参数化工业启发模型，不是完整工厂部署。
2. 更多关注时序与负载，不涉及高层任务正确性。
3. 真实 workload 分布仍需更多经验校准。

### 对本研究的启发

它很适合作为“验证剖面如何扩展到概率和负载维度”的样例，也提醒本研究要把场景负载视为性质成立的前提之一。

## 重要的相关工作

### 1. `ROS` 实时分析

- 论文直接接续了 `ROS`/`ROS 2` 反应时间分析与调度理论工作。

### 2. `UPPAAL SMC`

- 本文是 `UPPAAL SMC` 用于概率化机器人任务链分析的强应用样例。

### 3. 工业机器人视觉链路

- 相机、object detection、fusion、actuation 组成的链路让论文具有很强工程感。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文明确给出 GitHub 仓库，当前仓库可访问。
- 获取方式/链接：[DOI](https://doi.org/10.1007/978-3-031-85134-6_13)；[GitHub 仓库](https://github.com/ptrbman/ros2-modeling/)
- 对后续复用的现实影响：这是当前文库里公开度很高的 `ROS` 反应时间分析案例，适合直接复跑并做架构参数对比。
