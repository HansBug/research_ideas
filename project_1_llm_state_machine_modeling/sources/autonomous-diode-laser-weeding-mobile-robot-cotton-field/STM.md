# Autonomous diode laser weeding mobile robot in cotton field using deep learning, visual servoing and finite state machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了棉田激光除草机器人的 `8` 状态任务级 `FSM`、图像/坐标 guard、`6 cm` 末端定位条件和带定义时长的激光打击循环，可直接作为高质量农业机器人监督控制样本。

## 条目 1: Laser-weeding task supervisor for the cotton-field mobile robot
- 控制对象：棉田自主激光除草移动机器人的任务级监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个围绕取像、检测、坐标估计、接近、对准、激光打击和回位循环来组织棉田除草作业的移动机器人任务监督器。
- 判断：算。对象是真实农业机器人控制器，不是纯感知流程；原文明确给出状态数量、进入条件、坐标/距离 guard、激光作用阶段和回位闭环，足以恢复完整控制序列。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，Section `2.4 Overall robot control with finite state machine`
> To model the order of task execution and the flow of information between the robot controllers, the master controller ... utilized ... SMACH to create a Finite State Machine (FSM) ... accepting input and producing output.

#### 摘录 B
- 出处：第 8 页，Section `2.4 Overall robot control with finite state machine`
> We modeled the autonomous weeding robot tasks into eight states (actions), with eight transitions from one state to another ... The system begins at the entry state (“get image”), if the system fails to obtain an image ... it exits.

#### 摘录 C
- 出处：第 8 页，Section `2.4 Overall robot control with finite state machine`
> Otherwise, the weed detection model searches for weeds in the image. If no weed is detected, the system continues navigating between the rows ... When a weed is detected, the system obtains the 3D coordinates (x, y, z) ... calculates the forward distance ... as well as the lateral distance ...

#### 摘录 D
- 出处：第 9 页，Section `2.4 Overall robot control with finite state machine`
> The rover then moves to the weed and orients the arm ... Subsequently, the arm moves laterally to within 6 cm from the weed. At this point, the system emits a laser beam for a defined duration while the servos oscillate ...

#### 摘录 E
- 出处：第 9 页，Section `2.4 Overall robot control with finite state machine`
> The arm then returns to its initial position to avoid colliding with cotton in the rows during movement. Then FSM transitions back to the beginning state to start all over.

### 2. 基于原文整理后的自然语言描述

The cotton-field laser weeding robot is coordinated by an eight-state task-level FSM implemented in `SMACH` on the embedded master controller so that sensing, navigation, arm motion, and laser firing proceed in a fixed supervisory order. The mission starts in `get image`; if the camera fails the system exits, otherwise the detector searches for weeds and, when none are found, the rover keeps navigating between rows while repeatedly reacquiring images. Once a weed is detected, the supervisor computes its `3D` position together with forward and lateral offsets, then commands the rover to move toward the target and orient the arm toward the weed. The next guard requires the arm to move laterally until the laser head is within `6 cm` of the weed, after which the controller fires the laser for a defined duration while oscillating the servos to enlarge the contact area on the stem. After the strike, the arm returns to its initial position to avoid collision with cotton plants and the FSM loops back to the beginning state for the next weed.

### 3. 逐句溯源

1. 句子 1：The cotton-field laser weeding robot is coordinated by an eight-state task-level FSM implemented in `SMACH` on the embedded master controller so that sensing, navigation, arm motion, and laser firing proceed in a fixed supervisory order.
   对应摘录：A, B
2. 句子 2：The mission starts in `get image`; if the camera fails the system exits, otherwise the detector searches for weeds and, when none are found, the rover keeps navigating between rows while repeatedly reacquiring images.
   对应摘录：B, C
3. 句子 3：Once a weed is detected, the supervisor computes its `3D` position together with forward and lateral offsets, then commands the rover to move toward the target and orient the arm toward the weed.
   对应摘录：C, D
4. 句子 4：The next guard requires the arm to move laterally until the laser head is within `6 cm` of the weed, after which the controller fires the laser for a defined duration while oscillating the servos to enlarge the contact area on the stem.
   对应摘录：D
5. 句子 5：After the strike, the arm returns to its initial position to avoid collision with cotton plants and the FSM loops back to the beginning state for the next weed.
   对应摘录：E
