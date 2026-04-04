# 陆空两栖垂直起降自主载具 TURVTOL / Terrestrial Unmanned Roving Vertical Take-off and Landing (TURVTOL)

## 基本信息

- **标题**：Terrestrial Unmanned Roving Vertical Take-off and Landing (TURVTOL)
- **中文标题**：陆空两栖垂直起降自主载具 TURVTOL
- **作者**：Bennett Bartel，Ryan Bonk，Terelle Cadd，Chad Hite，Hunter Huth，Songcheng Lin，Stewart Nelson，Jamie O'Brien，Hannah Oliver，Zachary Preston，Nicole Schneider，Catie Spivey，Carson Stebbins，Christopher Titus，Isaac Vliem
- **单位**：
  - NASA Langley Research Center（NASA Academy 团队）
  - Christopher Newport University
- **发表**：AIAA Scitech 2021 Forum，2021
- **DOI**：10.2514/6.2021-1520
- **链接**：https://doi.org/10.2514/6.2021-1520

### 代码/仓库获取方式

- 原文描述的软件实现基于 `ROS`、`SMACH`、`VINS-Fusion`、`OctoMap` 和自定义 path planner。
- 论文没有给出独立公开仓库，但已把 FSM、transition signals、路径规划与控制环组织方式写到可直接提取的程度。

### 数据集/案例获取方式

- 原文未提供单独数据集。
- 论文给出了多模态 rover/drone 的 mission FSM、terrain-aware takeoff/landing 决策和 traction-loss 恢复链，适合作为复杂自主控制系统单案例 source paper。

## 简报

这篇论文解决的是**一个既能地面行驶又能短时飞跃障碍的自主载具如何在无 GPS 条件下完成 driving/flying/landing/charging 任务切换**的问题。输入是 path planner、battery、terrain safety、VIO、destination、slip/stuck/flip 信号，方法是设计一个 `SMACH` 层次状态机来调度 drive/fly/landing/traction-loss/dormant 多层子状态机，输出是多模态任务执行和异常恢复控制链。

- **输入**：path planner result、battery level、safe takeoff/landing flag、destination、slip/stuck/flipped indicators。
- **方法**：基于 `ROS/SMACH` 的 hierarchical FSM，联动 path planner、control loop、localization 与 terrain assessment。
- **输出**：`drive / takeoff / hover / search_for_landing / return_to_launch / charging / sleeping` 多模态任务控制链。
- **一句话评价**：这是高质量的 `HSM + T0` 自主平台控制样本，层次结构、状态表和 transition signal 都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是 `TURVTOL` 多模态自主载具的软件监督器。它负责决定车辆何时保持地面驱动、何时切换飞行、何时寻找安全着陆点、何时返航以及何时进入充电或休眠。

### 状态机组织方式

原文把高层控制明确写成 `hierarchical state machine`。顶层含：

1. `FLY_OPERATE`
2. `DRIVE_OPERATE`

同时又嵌入：

1. `LANDING` 子状态机
2. `TRACTION_LOSS` 子状态机
3. `DORMANT` 子状态机

最低层状态表则进一步展开为 `CHARGING / DRIVE_NO_FLY / FLIPPED / FLY / HOVER / LAND / NORM_DRIVE / RETURN_TO_LAUNCH / SEARCH_FOR_LANDING / SLEEPING / SLIPPING / STAND_STILL / STUCK / TAKEOFF`。

### 关键控制链

论文给出的控制链包含几个关键事实：

- 正常行驶时在 `NORM_DRIVE`，若 terrain 或风况使起飞不安全，就切到 `DRIVE_NO_FLY`。
- 需要飞越障碍时进入 `TAKEOFF -> FLY -> HOVER` 等飞行操作链。
- 需要着陆时，若周围能找到安全落点，则走 `SEARCH_FOR_LANDING -> LAND`；若找不到则进入 `RETURN_TO_LAUNCH`。
- 车辆打滑、卡住或翻覆时，会进入 `TRACTION_LOSS` 相关恢复链。
- 电量过低或无任务时，则由 `DORMANT` 子状态机管理 `CHARGING` 与 `SLEEPING`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实自主平台的任务监督逻辑**，而不是抽象多机器人方法论文。
- 原文已经明确写出层次状态组织、低层状态表和 transition signals，适合直接转成高质量自然语言状态机样本。
- 对“多模态平台在地面-飞行之间切换”的建模尤其有价值，能补充当前 `sources` 中较少的 drive/fly mixed mission 样本。

### 可直接借鉴之处

- 可以直接借鉴 drive/fly 两大主模式加 landing/traction-loss/dormant 子状态机的层次化组织。
- 可以直接借鉴 `safe_takeoff / safe_landing / return_to_safe / low_battery / stuck / slipping` 这类 transition signals 写法。
- 可以直接借鉴 `NORM_DRIVE -> DRIVE_NO_FLY` 这种由环境安全条件触发的模式约束逻辑。

### 局限性

- 论文是 design paper，部分低层 state method 仍处在持续集成阶段。
- 许多算法实现细节落在路径规划和定位模块，不能全部当成 FSM 事实直接吸收。
- 时间语义主要依靠任务顺序和安全信号，不是显式时钟约束。

## 文献分类总结

- **文献类型**：真实多模态自主平台控制案例论文
- **控制对象**：TURVTOL 多模态 rover/drone 监督控制器
- **状态机画像**：`HSM + T0`
- **证据强度**：层次结构、低层状态表和 transition signal 表都完整，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充 drive/fly 模式切换、异常恢复和落点搜索类自主控制样本
