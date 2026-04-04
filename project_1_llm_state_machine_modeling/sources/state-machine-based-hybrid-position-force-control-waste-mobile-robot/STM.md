# State Machine-Based Hybrid Position/Force Control Architecture for a Waste Management Mobile Robot with 5DOF Manipulator - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了垃圾分拣 5DOF 机械臂的主状态机、homing/position/force 三个子状态机和从抓取到投放的完整任务链，足以直接恢复其监督控制逻辑。

## 条目 1: Pick-and-drop supervisor for the waste-selection manipulator
- 控制对象：垃圾分拣移动机器人 5DOF 机械臂的任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于垃圾分拣机械臂的高层状态机，用来调度 homing、位置控制对准、力控抓取、抬升移送和开爪投放。
- 判断：算。对象是真实移动机器人上的执行器监督控制器，不是纯控制理论流程；原文给出了状态名、子状态机、抓取/投放顺序以及 emergency stop 路径。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> To solve this problem, we propose a state machine-driven hybrid position/force control architecture (SmHPFC).
>
> The architecture acts both as a parameter update process and as a switching mechanism for the joints' decision S-matrix.

#### 摘录 B
- 出处：第 5 页，Figure 3 / Table 1 `State machine states list and descriptions`
> Figure 3. The main 5DOF robot state machine for waste selection.
>
> Si1 Main The initial state of the entire system.
>
> Si2 Main/Homing Initialization complete.
>
> Si3 All Homing done or motion complete.
>
> SC1 Main Positioning in XOY plane and rotate gripper.
>
> SC2 Main/Force Control Positioning on OZ axis ... and rotate around OZ for gripper orientation.
>
> SC3 Main/Force Control Ready to start force control (grip object).
>
> SC4 Main/Position Control/Force Control Stop force control ... open gripper.
>
> SC5 Position Control Doing position control for selected reference.
>
> SES Position Control/Force Control Emergency stop.

#### 摘录 C
- 出处：第 6 页，Figure 4 / Section 3 `Decision Algorithm`
> These are the homing state machine, the position control state machine, and the force control state machine.
>
> The homing process is started sequentially on all five DOFs ... When the homing process is complete, the 5DOF system transitions to the stable state Si3.

#### 摘录 D
- 出处：第 6-7 页，Section 3 `Decision Algorithm` / Algorithm 1
> When a new task is received (transition TC1), the system begins to complete it, starting with the first two translation joints for positioning on XOY plane.
>
> Then, the vertical motion and orientation begin (SC2) and on its completion, the force control takes over for the gripper joint by changing the control type for this degree of freedom within the S-matrix.
>
> Thus, by using force control, the gripper attempts to grab the target object using the reference force given as input to the control system.
>
> While the gripper force holds, the 4DOF positioning system lifts the object and position the gripper above the recycling tray.
>
> At this moment, the gripper force control ends by updating the S-matrix, and the object is dropped by opening the gripper's jaws using position control.

### 2. 基于原文整理后的自然语言描述

The waste-selection manipulator is supervised by a hierarchical state machine whose top-level states cover system initialization, homing, stable waiting, position-controlled alignment, force-controlled gripping, and emergency stop handling. After the system starts, all five axes execute the `Homing` submachine and the controller moves to the stable state `Si3`, from which every new recycling task is launched. On a new task, the supervisor first enters `SC1` to position the manipulator in the `XOY` plane and rotate the gripper, then advances to `SC2` to adjust the `OZ` axis and finalize gripper orientation. Once the target pose is ready, the controller switches the gripper DOF from position control to force control inside the `S-matrix`, enters `SC3`, and closes the jaws until the reference gripping force is achieved and held. While force control maintains the grasp, the remaining axes lift the object, move it above the recycling tray, and then the controller updates the `S-matrix` again to return to position control so that the jaws can open and drop the object before the system accepts the next task.

### 3. 逐句溯源

1. 句子 1：The waste-selection manipulator is supervised by a hierarchical state machine whose top-level states cover system initialization, homing, stable waiting, position-controlled alignment, force-controlled gripping, and emergency stop handling.
   对应摘录：A, B, C
2. 句子 2：After the system starts, all five axes execute the `Homing` submachine and the controller moves to the stable state `Si3`, from which every new recycling task is launched.
   对应摘录：B, C
3. 句子 3：On a new task, the supervisor first enters `SC1` to position the manipulator in the `XOY` plane and rotate the gripper, then advances to `SC2` to adjust the `OZ` axis and finalize gripper orientation.
   对应摘录：B, D
4. 句子 4：Once the target pose is ready, the controller switches the gripper DOF from position control to force control inside the `S-matrix`, enters `SC3`, and closes the jaws until the reference gripping force is achieved and held.
   对应摘录：A, B, D
5. 句子 5：While force control maintains the grasp, the remaining axes lift the object, move it above the recycling tray, and then the controller updates the `S-matrix` again to return to position control so that the jaws can open and drop the object before the system accepts the next task.
   对应摘录：D
