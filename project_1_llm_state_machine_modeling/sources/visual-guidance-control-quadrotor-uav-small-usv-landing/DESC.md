# 小型 USV 上四旋翼 UAV 自主降落的视觉引导与控制方法 / A Visual Guidance and Control Method for Autonomous Landing of a Quadrotor UAV on a Small USV

## 基本信息

- **标题**：A Visual Guidance and Control Method for Autonomous Landing of a Quadrotor UAV on a Small USV
- **中文标题**：小型 USV 上四旋翼 UAV 自主降落的视觉引导与控制方法
- **作者**：Ziqing Guo，Jianhua Wang，Xiang Zheng，Yuhang Zhou，Jiaqing Zhang
- **单位**：
  - Key Laboratory of Transport Industry of Marine Technology and Control Engineering, Shanghai Maritime University
- **发表**：Drones，2025
- **DOI**：10.3390/drones9050364
- **链接**：https://doi.org/10.3390/drones9050364

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文明确给出 `FSM` 三阶段、trajectory generation、event-triggered yaw control、bounding box 约束和 `0.3 s` marker-loss failsafe，可直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集。
- 论文给出了小型 `USV` 上的 `UAV` 自主降落系统、室内外实验和完整 landing control chain，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**四旋翼 UAV 如何在小型 USV 上完成自主接近、视觉接管与最终降落，并在目标丢失时安全悬停**的问题。输入是 GNSS、视觉 marker 检测、相对位姿误差、yaw 偏差和 marker 可见性，方法是用三阶段 `FSM` 组织 `Idle -> Approaching -> Landing`，再在 Landing 内引入 event-triggered yaw control、bounding box guard 和 marker-loss failsafe，输出是完整的海上回收监督控制链。

- **输入**：landing command、GNSS 位置、ArUco marker 检测、相对位姿误差、yaw 偏差、marker visibility。
- **方法**：trajectory generation + three-stage `FSM` + event-triggered yaw/position `PID` control + `Hold` failsafe。
- **输出**：`hover waiting -> optimized approach -> visual landing -> motor shutdown / hold recovery` 的完整降落控制流程。
- **一句话评价**：这是高质量的 `EFSM + T1` 航空航天控制样本，阶段定义、空间 guard 和短时失视恢复链都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是四旋翼 `UAV` 在小型 `USV` 上回收任务的高层 landing supervisor。它负责接收降落命令、管理接近轨迹、在视觉锁定后切换到 landing，并在 marker 丢失时切到安全悬停。

### 状态机组织方式

原文明确把飞行过程写成三阶段 `FSM`：

1. `Idle`
2. `Approaching`
3. `Landing`

此外，在视觉跟踪阶段还引入了 `Offboard <-> Hold` 的 failsafe 模式切换，用于处理 fiducial marker 短时失视。

### 关键控制链

论文的高层控制链很清楚：

- `Idle` 下，`UAV` 悬停等待地面站命令；收到 landing command 后进入 `Approaching`。
- `Approaching` 下，系统根据给定 waypoints 生成优化轨迹并执行跟踪；前视相机检测到着陆平台 marker 后自动切到 `Landing`。
- `Landing` 下，系统使用视觉引导接近平台，并在进入虚拟 bounding box 后才允许更积极的 yaw 调整，以避免平移和转向互相干扰。
- 目标 landing point 设置在 marker 前方 `75 cm`，bounding box 尺寸根据平台和 UAV 机体约束为 `60 cm` 高、`50 cm` 长、`25 cm` 宽。
- 若 marker 在视觉阶段连续不可见超过 `0.3 s`，系统把 PX4 flight mode 从 `Offboard` 切到 `Hold`；marker 恢复后再回到 `Offboard` 继续 visual tracking。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 这是**真实 UAV-USV 回收控制器**，不是单纯视觉检测或轨迹优化论文。
- 原文同时保留了阶段状态、进入条件、空间 guard、event-triggered control 和 recovery chain，适合直接提取为高质量自然语言状态机描述。
- 对“vision takeover + landing supervisor + marker-loss recovery”这一类空海协同控制样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `Idle -> Approaching -> Landing` 的分阶段 supervisor 模板。
- 可以直接借鉴用空间 bounding box 决定何时放开 yaw 调整的 guard 写法。
- 可以直接借鉴 `marker lost for 0.3 s -> Hold -> re-detect -> Offboard` 的短时失视恢复链。

### 局限性

- 论文大量篇幅用于 trajectory planning 和视觉定位算法，需要与高层 `FSM` 主链拆开整理。
- 顶层状态数较少，但每个阶段内部的空间约束和模式回退比较关键。
- 时间语义主要体现在短时失视超时，而不是复杂的多定时器网络。

## 文献分类总结

- **文献类型**：真实 UAV-USV 回收控制案例论文
- **控制对象**：四旋翼 `UAV` 的小型 `USV` 自主降落监督控制器
- **状态机画像**：`EFSM + T1`
- **证据强度**：三阶段 `FSM`、bounding box、`75 cm` target point 和 `0.3 s` failsafe 都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充移动平台回收、视觉接管和安全悬停恢复样本
