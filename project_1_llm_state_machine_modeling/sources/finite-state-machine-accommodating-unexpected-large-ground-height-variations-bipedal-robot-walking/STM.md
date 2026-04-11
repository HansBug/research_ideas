# A Finite-State Machine for Accommodating Unexpected Large Ground-Height Variations in Bipedal Robot Walking - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `MABEL` 双足机器人的未知地形应对控制明确组织为 `RW / SD / SU / TR` 四相 FSM，并给出接触开关、高度估计和绊倒反射的转移条件。

## 条目 1: Blind terrain-transition FSM for the MABEL biped

- 控制对象：通用控制与机器人任务领域的 `MABEL` 双足机器人未知台阶/绊倒应对监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于 `MABEL` 双足机器人在未知地面升降、台阶和绊倒场景中切换反馈控制器的高层有限状态机。
- 判断：算。对象是真实机器人行走控制器，不是离线分析流程；原文明确给出四个控制相位、接触开关输入、由机器人关节几何估计的高度变化、绊倒早晚判定和状态相关控制动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> A finite-state machine is designed that manages transitions among controllers for flat-ground walking, stepping-up and down, and a trip reflex. If the robot completes a step, the depth of a step-down or height of a step-up can be immediately estimated at impact from the lengths of the legs and the angles of the robot's joints. ... if the swing leg impacts an obstacle during a step, or has a premature impact with the ground, a trip reflex is triggered on the basis of specially designed contact switches on the robot's shins, contact switches on the end of each leg, and the current configuration of the robot.

#### 摘录 B

- 出处：第 9 页，Section `V. Finite-State Machine`
> This section presents a finite-state machine to manage transitions among controllers for flat-ground walking, stepping-down, stepping-up, and a trip-reflex. ... four types of stance phase ... regular-walking phase (RW), step-down phase (SD), step-up phase (SU), and tripping phase (TR) ... W := {RW, SD, SU, TR}.

#### 摘录 C

- 出处：第 9 页，Section `V. Finite-State Machine`
> A decision to transition from one phase to another will be made on the basis of the values of the contact switches at the front and end of each leg, as well as a detected change in walking surface height ... Firstly, the transition to RW takes place ... when the impact with the ground occurs close to the end of the gait ... and ... the height of the swing toe ... is less than Delta H. The transition to SD or SU occurs ... along with the height of the swing toe ... being less than -Delta H, or larger than Delta H, respectively. ... the transition to TR arises when the swing leg trips over obstacles or touches the ground prematurely.

#### 摘录 D

- 出处：第 5-6 页，Section `IV. Control Design for Step-down, Step-up, and Tripping`
> In response to late tripping, the rapid-lowering (RL) strategy of the swing leg is applied. ... In response to early tripping, the rapid-elevation (RE) strategy of the swing leg is activated. Rapid-elevation of the swing leg is accomplished by rapidly bending the swing knee ... Once the swing foot is on top of the obstacle, the robot can continue walking by applying the step-up controller at the ensuing step.

### 2. 基于原文整理后的自然语言描述

The MABEL terrain supervisor is a four-state FSM that selects among `regular walking`, `step-down`, `step-up`, and `tripping-reflex` controllers while the robot walks without prior knowledge of where the ground height changes. At normal impact near the end of the gait cycle, the controller estimates swing-toe height from leg lengths and joint angles: small height error returns the machine to `RW`, negative height below the threshold selects `SD`, and positive height above the threshold selects `SU`. If the shin or toe contact switches report obstacle contact or premature ground contact, the machine enters `TR` rather than treating the event as a normal impact. Inside the tripping response, late tripping keeps the gait controller until contact and then applies a recovery step, while early tripping triggers rapid knee elevation to clear the obstacle and then routes the next step through step-up or recovery logic. The discrete FSM is therefore coupled to continuous robot configuration and contact sensing, but its main modeling skeleton is a clear flat set of behavior states with explicit disturbance-dependent transitions.

### 3. 逐句溯源

1. 句子 1：The MABEL terrain supervisor is a four-state FSM that selects among `regular walking`, `step-down`, `step-up`, and `tripping-reflex` controllers while the robot walks without prior knowledge of where the ground height changes.
   对应摘录：A, B
2. 句子 2：At normal impact near the end of the gait cycle, the controller estimates swing-toe height from leg lengths and joint angles: small height error returns the machine to `RW`, negative height below the threshold selects `SD`, and positive height above the threshold selects `SU`.
   对应摘录：A, C
3. 句子 3：If the shin or toe contact switches report obstacle contact or premature ground contact, the machine enters `TR` rather than treating the event as a normal impact.
   对应摘录：A, C
4. 句子 4：Inside the tripping response, late tripping keeps the gait controller until contact and then applies a recovery step, while early tripping triggers rapid knee elevation to clear the obstacle and then routes the next step through step-up or recovery logic.
   对应摘录：D
5. 句子 5：The discrete FSM is therefore coupled to continuous robot configuration and contact sensing, but its main modeling skeleton is a clear flat set of behavior states with explicit disturbance-dependent transitions.
   对应摘录：A, B, C, D
