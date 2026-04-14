# Mobile robot with failure inspection system for ferromagnetic structures using magnetic memory method - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁磁结构巡检机器人沿板面行进、避障、回退与转向的 5 态 FSM 写得很完整，还给出了 100 ms 的电机等待时序与实测巡检能力。

## 条目 1: Five-State Ferromagnetic Inspection Path Controller

- 控制对象：铁磁结构缺陷巡检移动机器人的路径跟随与避障控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个安装了磁记忆检测装置的移动巡检机器人控制器，用 5 个离散状态管理直线巡检、左右转向与后退恢复。
- 判断：算。对象是实际移动机器人运动控制链，原文明确写出 `START / FOLLOW / LEFT TURN / RIGHT TURN / BACKWARD` 状态集合、左右障碍触发、100 ms 电机等待，以及与巡检任务绑定的速度、续航和测量能力。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section 2.1 / Figure 5，行 226-260
> A Finite State Machine (FSM) shows the robot's behavior path in five states. The FSM always starts in `START` state, waiting for 100 ms time required for setting registers and assigning variables, after this, FSM changes to `FOLLOW` state, activating both motors and following a straight line. If at some point the robot detects an obstacle in the right side, then it stops and waits for 100 ms before a spin change and, after, goes into `LEFT TURN`. When it is in `LEFT TURN` state and detects presence of an object on the left side, the robot stops 100 ms and changes to `BACKWARD` state. On the other hand, if the robot is in `FOLLOW` state and senses an obstacle on the left side, it stops 100 ms and switches to `RIGHT TURN` state. Finally, if robot is in `FOLLOW` state and is fully blocking its path, then it will change to `BACKWARD` state, being able to change from this state to `RIGHT TURN` if there is no obstacle on the left side or to `LEFT TURN` if there is no obstacle on the right side.

#### 摘录 B

- 出处：第 5-8 页，Section 3 Results / Section 5 Conclusions，行 294-299, 317-321, 369-380
> The complete system is powered by four 1.5 V batteries, which has an autonomy of 45 min and a power consumption of approximately 2 W. Additionally, the microsensor has a resolution of 0.1 µT. The mobile robot uses a proportional integral derivative (PID) controller, which was designed to stabilize the speed, and the infrared sensors are used to handle the turning left, right and the moving forward, backward and reverse. In this paper a mobile robot was used to inspect rectangular defects in a ASTM A-27 ferromagnetic plate. The proposed prototype is capable of measuring small variations of the magnetic field due to defects of the order of millimeters at a travel speed of 2.15 cm/s.

### 2. 基于原文整理后的自然语言描述

The inspection robot executes a five-state FSM consisting of `START`, `FOLLOW`, `LEFT TURN`, `RIGHT TURN`, and `BACKWARD`, and it begins by spending 100 ms in `START` to initialize registers and variables before enabling both motors for straight-line inspection in `FOLLOW`. While following the ferromagnetic plate, right-side obstacles trigger a 100 ms stop followed by a transition to `LEFT TURN`, left-side obstacles trigger a 100 ms stop followed by `RIGHT TURN`, and a fully blocked path triggers `BACKWARD`, from which the robot chooses a new turn direction according to which side becomes free. The controller therefore embeds both nominal inspection motion and explicit recovery branches for side blockage and full blockage instead of relying on a single open-loop path. In the implemented prototype, this FSM-based motion layer is paired with PID speed stabilization and infrared sensing, enabling defect inspection at 2.15 cm/s with 45 minutes of autonomy and 0.1 µT sensing resolution.

### 3. 逐句溯源

1. 句子 1：The inspection robot executes a five-state FSM consisting of `START`, `FOLLOW`, `LEFT TURN`, `RIGHT TURN`, and `BACKWARD`, and it begins by spending 100 ms in `START` to initialize registers and variables before enabling both motors for straight-line inspection in `FOLLOW`.
   对应摘录：A
2. 句子 2：While following the ferromagnetic plate, right-side obstacles trigger a 100 ms stop followed by a transition to `LEFT TURN`, left-side obstacles trigger a 100 ms stop followed by `RIGHT TURN`, and a fully blocked path triggers `BACKWARD`, from which the robot chooses a new turn direction according to which side becomes free.
   对应摘录：A
3. 句子 3：The controller therefore embeds both nominal inspection motion and explicit recovery branches for side blockage and full blockage instead of relying on a single open-loop path.
   对应摘录：A
4. 句子 4：In the implemented prototype, this FSM-based motion layer is paired with PID speed stabilization and infrared sensing, enabling defect inspection at 2.15 cm/s with 45 minutes of autonomy and 0.1 µT sensing resolution.
   对应摘录：B
