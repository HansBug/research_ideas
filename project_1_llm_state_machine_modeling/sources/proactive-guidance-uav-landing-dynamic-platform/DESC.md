# 面向动态平台精确降落的 UAV 主动引导方法 / Proactive Guidance for Accurate UAV Landing on a Dynamic Platform: A Visual–Inertial Approach

## 基本信息

- **标题**：Proactive Guidance for Accurate UAV Landing on a Dynamic Platform: A Visual–Inertial Approach
- **中文标题**：面向动态平台精确降落的 UAV 主动引导方法
- **作者**：Ching-Wei Chang，Li-Yu Lo，Hiu Ching Cheung，Yurong Feng，An-Shik Yang，Chih-Yung Wen，Weifeng Zhou
- **单位**：
  - Department of Mechanical Engineering, The Hong Kong Polytechnic University
  - Department of Aeronautical and Aviation Engineering, The Hong Kong Polytechnic University
  - Department of Energy and Refrigerating Air-Conditioning Engineering, National Taipei University of Technology
  - School of Professional Education and Executive Development, The Hong Kong Polytechnic University
- **发表**：Sensors，2022
- **DOI**：10.3390/s22010404
- **链接**：https://doi.org/10.3390/s22010404

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文明确说明系统基于 `ROS`、视觉定位、Kalman filter 与 finite state machine 组成，但未开放完整实现。
- 原文给出了四阶段 landing FSM、位置域阈值、回退条件和关机距离，可直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集。
- 论文给出了室内外动态平台降落实验和完整 landing control chain，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**小型四旋翼如何在移动地面/海上平台上安全、平滑地完成自主降落**的问题。输入是 GPS、视觉定位、IMU/Kalman filter 状态估计、平台相对位置误差和高度信息，方法是用一个四阶段有限状态机调度 GPS 跟随、视觉位置跟随、无地效接近轨迹和最后关机，输出是 `GPS following -> vision position following -> ground-effect free trajectory -> shutdown` 的完整降落监督控制链。

- **输入**：GPS 跟随位置、视觉定位结果、`KF` 融合状态、相对位置误差、平台可见性、剩余高度。
- **方法**：视觉-惯导定位 + optimized trajectory planner + four-stage landing FSM。
- **输出**：动态平台入视野、视觉接管、无地效滑翔接近、触地前电机关断的完整 landing supervisor。
- **一句话评价**：这是高质量的 `EFSM + T0` 航空航天控制样本，阶段定义、空间阈值和失败回退都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是四旋翼 UAV 的高层 landing supervisor。它负责判断何时由 GPS 跟随切换到视觉接管、何时进入接近轨迹、何时因失视或越界回退，以及何时在接近平台后关闭电机。

### 状态机组织方式

原文把该控制器明确写成 `finite state machine`，包含四个阶段：

1. `GPS following`
2. `Vision position following`
3. `Ground-effect free trajectory following`
4. `Shutdown`

### 关键控制链

论文写清了降落主链和回退逻辑：

- `GPS following` 先把 UAV 带到平台视场附近。
- 一旦定位估计收敛，转入 `Vision position following`，利用视觉与融合定位维持相对位置。
- 当 UAV 进入以 `(1.1 m behind, 0.7 m above)` 为中心、半径 `0.1 m` 的期望域时，转入 `Ground-effect free trajectory following`。
- 在第三阶段中，若位置偏离期望轨迹、剩余高度不足或相对平台 overshoot 超界，则立刻回退到第二阶段并拉开安全距离。
- 当 UAV 到达着陆位置并距平台小于 `5 cm` 时，系统进入 `Shutdown`，快速降低电机油门并完成着陆。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实 UAV 降落监督控制器**，不是单纯视觉检测或路径优化论文。
- 原文同时保留了 FSM 阶段、切换条件、空间 guard 和 failsafe 回退逻辑，适合直接提取成高质量自然语言状态机描述。
- 对“移动平台回收、视觉接管、接近轨迹和 shutdown chain”这一类空地协同控制样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `GPS -> vision -> approach -> shutdown` 的分阶段接管模板。
- 可以直接借鉴以空间位置域和高度条件定义状态切换的 guard 写法。
- 可以直接借鉴在 approach 阶段设置越界即回退的安全控制口径。

### 局限性

- 论文中的低层位置估计与轨迹规划篇幅较多，需要与高层 FSM 主链分开整理。
- 时间语义主要体现在顺序阶段和空间条件，而非显式 timer。
- 失效恢复主要是回退到前一阶段，没有更复杂的异常模式网。

## 文献分类总结

- **文献类型**：真实 UAV 动态平台降落控制案例论文
- **控制对象**：四旋翼 UAV 的动态平台自主降落监督控制器
- **状态机画像**：`EFSM + T0`
- **证据强度**：四阶段 FSM、空间阈值、回退条件和 shutdown 条件明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充多阶段回收控制、视觉接管和安全回退样本
