# Simultaneous Obstacles Avoidance and Robust Autonomous Landing of a UAV on a Moving Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 moving-vehicle landing supervisor 明确写成 `hovering / tracking and avoiding obstacles / landing / disarmed` 四状态 FSM，并把视觉引导、避障轨迹和 `0.5 m` 终端切换条件连在一起，是一条完整的飞行控制样本。

## 条目 1: Four-state moving-vehicle landing supervisor

- 控制对象：航空航天与飞行/空管控制领域的无人机移动载具避障着陆监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于四旋翼在带未知障碍环境中降落到移动地面车辆上的高层监督控制器，用四状态 FSM 组织悬停、避障跟踪、最终着陆和停桨结束。
- 判断：算。对象是实际 UAV landing supervisor，而不是单纯视觉感知或轨迹规划模块；原文明确给出了状态集合、切换条件和视觉/GPS/避障在各状态中的角色。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 3-8、33-41 行
> Simultaneous Obstacles Avoidance and Robust Autonomous Landing of a UAV on a Moving Vehicle.
>
> ... we propose a systematic autonomous landing scheme that enables the robust autonomous landing performance of a quadrotor UAV. The proposed scheme integrates target detection, state estimation, trajectory planning, and landing control. ... The trajectory planner of the quadrotor updates continuously to avoid obstacles via real-time sensing and re-planning. A finite state machine is used to label the current flight status and triggers the control laws correspondingly.

#### 摘录 B

- 出处：第 4 页，`2.2. Finite State Machine`，`paper_content.txt` 第 241-246、268-286 行
> For the smooth implementation of the landing scheme, we designed a finite state machine (FSM) to determine the action of the quadrotor in a three-dimensional environment with unknown obstacles. FSM contains four states: hovering, tracking and avoiding obstacles, landing, and disarmed. The states and the respective transitions are depicted in Figure 2.
>
> Hovering: The hovering state includes the takeoff and loitering of the drone. At this stage, the quadrotor waits to receive the position of the landing pad and then transitions to the next state.
>
> Tracking and avoiding obstacles: After receiving the position of the landing pad, a collision-free trajectory from the quadrotor to the UGV is planned to avoid the obstacles, and the drone begins to approach the UGV.

#### 摘录 C

- 出处：第 4-5 页，`2.2. Finite State Machine / 3. Detection Method and Landing Pad`，`paper_content.txt` 第 280-289、303-309 行
> Landing: After the horizontal distance between the UAV and the mobile UGV is less than 0.5 m, we believe that the UAV then enters a safe area without obstacles. At this stage, the UAV will be guided by a visual system.
>
> Disarmed: After the drone lands on the moving UGV, the blades of the drone will stop rotating, and the landing mission is complete.
>
> ... simulated GPS is used to guide the drone, and the motion state of the mobile UGV is updated by the EKF.

### 2. 基于原文整理后的自然语言描述

The landing controller is a four-state FSM for a quadrotor that must land on a moving ground vehicle while avoiding unknown obstacles. In `hovering`, the UAV takes off, loiters, and waits until the landing-pad position is available. It then enters `tracking and avoiding obstacles`, where a collision-free trajectory toward the UGV is generated and continuously updated through real-time sensing and replanning. Once the horizontal distance between the UAV and the mobile vehicle drops below `0.5 m`, the machine switches to `landing`, which assumes the terminal area is obstacle-free and hands over to the visual landing loop. After touchdown, the controller enters `disarmed`, where the propellers stop and the mission terminates. The paper also states that GPS and EKF are used before close-range visual guidance, so the discrete flight-status machine is explicitly tied to continuous state estimation and obstacle-avoidance control rather than floating above the dynamics.

### 3. 逐句溯源

1. 句子 1：The landing controller is a four-state FSM for a quadrotor that must land on a moving ground vehicle while avoiding unknown obstacles.
   对应摘录：A, B
2. 句子 2：In `hovering`, the UAV takes off, loiters, and waits until the landing-pad position is available.
   对应摘录：B
3. 句子 3：It then enters `tracking and avoiding obstacles`, where a collision-free trajectory toward the UGV is generated and continuously updated through real-time sensing and replanning.
   对应摘录：A, B
4. 句子 4：Once the horizontal distance between the UAV and the mobile vehicle drops below `0.5 m`, the machine switches to `landing`, which assumes the terminal area is obstacle-free and hands over to the visual landing loop.
   对应摘录：C
5. 句子 5：After touchdown, the controller enters `disarmed`, where the propellers stop and the mission terminates.
   对应摘录：C
6. 句子 6：The paper also states that GPS and EKF are used before close-range visual guidance, so the discrete flight-status machine is explicitly tied to continuous state estimation and obstacle-avoidance control rather than floating above the dynamics.
   对应摘录：A, C
