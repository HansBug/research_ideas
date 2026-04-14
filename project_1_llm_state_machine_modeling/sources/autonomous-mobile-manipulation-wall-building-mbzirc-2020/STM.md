# Autonomous, Mobile Manipulation in a Wall-building Scenario: Team LARICS at MBZIRC 2020 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 MBZIRC 砌墙挑战中的 UGV 高层控制写成显式 state machine，并展开了 Load/Unload、Two-Stage Approach 和 Brick Pickup 的层次化阶段划分。

## 条目 1: Brick-load/unload mobile-manipulation challenge supervisor

- 控制对象：工业自动化与机器人施工领域的砖块抓取、运输与放置移动操作监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 MBZIRC 2020 砌墙挑战中 UGV 的高层挑战控制器，用状态机组织 brick stack 搜索、对齐、抓取、运输和在墙面 footprint 上的精准放置。
- 判断：算。对象是真实移动操作机器人控制系统，不是单纯任务说明；原文明确给出了 high-level state machine，以及 `Load Bricks / Unload Bricks / Two-Stage Approach / Brick Pickup / Brick Drop` 等子状态结构与各阶段职责。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，行 11-18
> Our control approach is based on a state machine that dictates which controllers are active at each stage of the Challenge.
> ... the second stage consists of detecting the object's global pose ... and calculating an alignment goal within a global map.
> Visual servo algorithms guide the vehicle in local object-approach movement and the arm in manipulating bricks.

#### 摘录 B

- 出处：第 5-7 页，Section `4 High-level control`，行 196-205
> A challenge-specific state machine has been designed that dictates which controllers are used at each stage of the Challenge.
> In certain states, both the UGV and the manipulator arm must collaborate, while in other states either UGV or manipulator is controlled while the other remains idle.
> The mission planner ... specifies which bricks to load and unload.

#### 摘录 C

- 出处：第 6-7 页，Section `4.0.2 Collaborative control`，行 212-239
> Operations in which the platform and the robot arm collaborate are Load Bricks and Unload Bricks.
> ... the platform is controlled by Two-Stage Approach, whose objective is to guide the UGV to a pose where the desired object is within reach of the robot arm.
> Both Load Bricks and Unload Bricks include Initial Approach and Final Approach states ...
> Initial Approach is used to get close enough to the desired object to detect its pose ... The Alignment is conducted with a navigation planner ...

#### 摘录 D

- 出处：第 9 页与第 13-14 页，Section `5 Detection of objects of interest` / `6.3 Visual Servo Brick Pickup`，行 300-305 与 463-490
> For Local Object Approach, a visual servo algorithm is used to keep observing an object while approaching it.
> ... For the Two-Stage Approach, the global pose of the approached object in map frame LM must be estimated ...
> The brick pickup motion is divided into four different stages: x and Pitch Visual Servo, y Visual Servo, yaw Visual Servo and z Approach ...
> This stage of the visual servo pickup is completed when the camera pitch angle reaches π/2 and the image coordinate ... is sufficiently close to zero.

### 2. 基于原文整理后的自然语言描述

The MBZIRC UGV controller is organized as a challenge-specific hierarchical state machine that decides when only the base moves, when only the manipulator acts, and when both subsystems must cooperate. At the top level, the mission alternates between navigating to a brick stack, loading the desired bricks, navigating to the wall pattern, and unloading those bricks until the planner reports completion. The collaborative core of both `Load Bricks` and `Unload Bricks` is a `Two-Stage Approach` in which the UGV first executes an `Initial Approach` to get close enough for pose estimation, then computes an aligned goal pose, performs `Alignment` with the navigation planner, and finally runs a `Final Approach` that preserves the acquired orientation while visually servoing into reach. Once the base is aligned to a brick, `Brick Pickup` takes over and decomposes the grasping process into `x-and-pitch`, `y`, `yaw`, and `z-approach` visual-servo stages so that pose alignment and contact establishment are handled sequentially in the robot frame. The resulting HSM therefore combines global mission repetition, local base alignment, and staged end-effector servoing into one coherent wall-building supervisor.

### 3. 逐句溯源

1. 句子 1：The MBZIRC UGV controller is organized as a challenge-specific hierarchical state machine that decides when only the base moves, when only the manipulator acts, and when both subsystems must cooperate.
   对应摘录：A, B
2. 句子 2：At the top level, the mission alternates between navigating to a brick stack, loading the desired bricks, navigating to the wall pattern, and unloading those bricks until the planner reports completion.
   对应摘录：B
3. 句子 3：The collaborative core of both `Load Bricks` and `Unload Bricks` is a `Two-Stage Approach` in which the UGV first executes an `Initial Approach` to get close enough for pose estimation, then computes an aligned goal pose, performs `Alignment` with the navigation planner, and finally runs a `Final Approach` that preserves the acquired orientation while visually servoing into reach.
   对应摘录：C, D
4. 句子 4：Once the base is aligned to a brick, `Brick Pickup` takes over and decomposes the grasping process into `x-and-pitch`, `y`, `yaw`, and `z-approach` visual-servo stages so that pose alignment and contact establishment are handled sequentially in the robot frame.
   对应摘录：D
5. 句子 5：The resulting HSM therefore combines global mission repetition, local base alignment, and staged end-effector servoing into one coherent wall-building supervisor.
   对应摘录：A, B, C, D
