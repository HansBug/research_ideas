# Team RoboSimian: Semi-autonomous Mobile Manipulation at the 2015 DARPA Robotics Challenge Finals - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RoboSimian 在 DRC 操作任务中的低层 behavior 明确写成接触触发的层次状态机，并补出对象相对起始位姿、力/距离阈值、timeout 与 success/failure 分支，足以形成高质量机器人任务监督样本。

## 条目 1: Contact-Triggered Behavior Supervisor for DRC Mobile Manipulation

- 控制对象：通用控制与机器人任务领域的 RoboSimian 接触触发 manipulation/mobility behavior supervisor
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 RoboSimian 在 DARPA Robotics Challenge 中执行开门、拧阀、抓钻和接触推进等 manipulation 行为时使用的上层 behavior supervisor。
- 判断：算。对象是实际移动操作机器人控制系统，而不是泛流程架构；原文明确写出 behavior 是异步、接触触发、层次状态机，每个状态都带动作、结束条件、事件迁移和失败恢复分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> We use the term “behaviors” to conceptualize this low-level adaptability. Each behavior is a contact-triggered state machine that enables execution of short order manipulation and mobility tasks autonomously.

#### 摘录 B

- 出处：第 11 页，Section `5.1 Behaviors`
> Behaviors consist of asynchronous, contact-triggered, hierarchical state machines that interface to this control system at its highest loop.
>
> Behaviors specify Cartesian-space motion objectives at the end effector and are data-driven hierarchical state machines. Force control set points and open-loop Cartesian moves are examples of the types of objectives that can be associated with a given behavior. Each state consists of a parameterized action, an associated set of end condition checks for monitoring action completion, and logic for transitioning. Example end condition checks are motion request complete, time reached, and measured force/torque at a certain value. Transitions are event-based and occur when an action completes or fails.

#### 摘录 C

- 出处：第 11-12 页，Section `5.1 Behaviors` / Figure `7`
> For object manipulation behaviors (e.g. Door Open, Valve Turn, Drill Grab), part of the behavior definition is the starting pose of the end effector in the object frame. When a planner receives a behavior request from the OCU, it first plans a trajectory to this end effector pose based on the location of the object in the 3D world. It then sends the trajectory, behavior type, and behavior parameters to the control server to handle execution.
>
> Figure 7: A subset of the behaviors (contact-triggered state machines) used in the competition. Most behaviors were parameterized by force/distance thresholds and timeouts (the parameters are shown in blue; best viewed in color).

#### 摘录 D

- 出处：第 21-22 页，Section `8` manipulation tasks
> The following end effector behaviors were explored to open the door: finger grasping and handle turning, hooking the handle with the fingers, and preloading the door and moving the wrist to hook the handle. ... The state machine for the final door behavior is illustrated in the bottom left region of Figure 7.
>
> The following end effector behaviors were explored to turn the valve: grasping at the perimeter and turning, grasping the center or the perimeter of the valve and turning (for smaller valves), and hooking the center of the valve and turning. ... The state machine for the final valve turn behavior is illustrated in the bottom middle region of Figure 7.
>
> The wall task was sequenced into three discrete objectives: pick up the drill, align the bit with the wall, and cut the hole. ... the following set of behaviors were stored in the drill and wall fits: 1) ‘drill grab’ ... 2) ‘push drill’ ... 3) ‘drive to contact’ ... and 4) ‘cut a circle given a wall normal.’

### 2. 基于原文整理后的自然语言描述

The RoboSimian manipulation layer is organized as an asynchronous contact-triggered hierarchical state machine that sits above the cascaded limb control loops and dispatches reusable end-effector behaviors. Each behavior is defined in Cartesian/object space and every state carries a parameterized action together with event-based completion or failure checks, including motion completion, timeout, and force/torque thresholds. For competition tasks such as `Door Open`, `Valve Turn`, and `Drill Grab`, the planner first drives the limb to a behavior-specific start pose in the object frame and then invokes the corresponding contact behavior with the required parameters. Figure 7 shows that these behaviors are internally decomposed into smaller substeps such as moving to contact, waiting at a face-sensor stage, advancing by force-controlled increments, or ending on success/failure branches, while most transitions are guarded by force/distance thresholds and timeouts. At the task level, the wall operation is explicitly sequenced as `drill grab -> push drill -> drive to contact -> cut a circle`, so the supervisor combines high-level repeatable task scripts with low-level local adaptation through force sensing.

### 3. 逐句溯源

1. 句子 1：The RoboSimian manipulation layer is organized as an asynchronous contact-triggered hierarchical state machine that sits above the cascaded limb control loops and dispatches reusable end-effector behaviors.
   对应摘录：A, B
2. 句子 2：Each behavior is defined in Cartesian/object space and every state carries a parameterized action together with event-based completion or failure checks, including motion completion, timeout, and force/torque thresholds.
   对应摘录：B, C
3. 句子 3：For competition tasks such as `Door Open`, `Valve Turn`, and `Drill Grab`, the planner first drives the limb to a behavior-specific start pose in the object frame and then invokes the corresponding contact behavior with the required parameters.
   对应摘录：C, D
4. 句子 4：Figure 7 shows that these behaviors are internally decomposed into smaller substeps such as moving to contact, waiting at a face-sensor stage, advancing by force-controlled increments, or ending on success/failure branches, while most transitions are guarded by force/distance thresholds and timeouts.
   对应摘录：B, C, D
5. 句子 5：At the task level, the wall operation is explicitly sequenced as `drill grab -> push drill -> drive to contact -> cut a circle`, so the supervisor combines high-level repeatable task scripts with low-level local adaptation through force sensing.
   对应摘录：A, D
