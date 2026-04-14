# A Simulation Framework for Developing Autonomous Drone Navigation Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了基于 Stateflow 的无人机自主导航层次状态机，写清了 superstate 划分、接近/对准/穿框/着陆链条以及 `20 Hz`、`4 s`、`2 s` 等工程时间参数，是高质量无人机导航监督器样本。

## 条目 1: Frame-navigation autopilot supervisor

- 控制对象：无人机竞赛场景中的自主导航与穿框任务监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是无人机自主导航系统中的高层任务监督器，用层次 Stateflow 状态机组织起飞、穿越不同颜色框架和返航着陆。
- 判断：算。对象是具体无人机导航控制器，原文把 superstate、子状态、对准条件、持续时间和着陆条件都写得非常明确，不是只有一张概念架构图。

### 1. 原文摘录

#### 摘录 A

- 出处：Section 3，`paper_content.txt` 第 430-447 行
> Figure 7 shows the contents of the autopilot Stateflow block ... This state machine is run every 0.05 s, so the navigation system runs at 20Hz. ... the state machine contains five superstates ... The navigation system starts in the TakeOff superstate ... Later, the system switches to the RedFrame state ... The GreenFrame and BlueFrame states define similar behaviors ... After going through all the frames, the system shifts to the Landing state.

#### 摘录 B

- 出处：TakeOff superstate，`paper_content.txt` 第 533-550 行
> After the activation of the motors, the state machine switches directly to the SetBase state. ... this assignment cannot be made in the Start state ... From the SetBase state the machine will pass to the End state ... the navigation system requests that the drone rise ... to a height of exactly 1m. ... When there are less than 10cm left to reach the desired height ... the system changes from the TakeOff superstate to the RedFrame superstate.

#### 摘录 C

- 出处：RedFrame state，`paper_content.txt` 第 708-727 行
> the drone tries to approach to within 40cm of it ... If for any reason the drone should lose sight of the frame, then the navigation system returns to the Go2Center state ... After that, the state machine transitions to the FrameClose state. ... The system records the current angle and changes to the ShiftLeft state. ... If the shift to the left makes the tilt angle increase ... transitioning to the ShiftRight state ... when the angle is less than 3°, the drone is sufficiently aligned with the frame to be able to pass through it, transitioning to the Crossing state.

#### 摘录 D

- 出处：Crossing and Landing，`paper_content.txt` 第 736-749 行
> In the Crossing state ... after 4 s the quadcopter should have passed through the frame. ... After crossing, the drone rises for 2 s ... The superstate then changes to the End state, and the navigation system moves to the Landing superstate. ... When the drone is less than 5 cm from its destination, the navigation system stops the engines so that the drone falls onto the base.

### 2. 基于原文整理后的自然语言描述

The example autopilot is a `20 Hz` Stateflow navigation supervisor organized as five superstates: `TakeOff`, `RedFrame`, `GreenFrame`, `BlueFrame`, and `Landing`. Inside `TakeOff`, the machine activates the motors, stores the base position in `SetBase`, climbs to `1 m`, and leaves the superstate only when the remaining distance falls below `10 cm`. In each frame-handling superstate, the drone first approaches the target frame, then enters `FrameClose` and lateral shift states to reduce misalignment until the tilt angle is below `3°`, at which point it transitions into `Crossing`. The `Crossing` state keeps the drone advancing for `4 s`, raises it for another `2 s`, and then hands control to `Landing`, where the vehicle returns to base and cuts the motors when it is within `5 cm` of the destination.

### 3. 逐句溯源

1. 句子 1：The example autopilot is a `20 Hz` Stateflow navigation supervisor organized as five superstates: `TakeOff`, `RedFrame`, `GreenFrame`, `BlueFrame`, and `Landing`.
   对应摘录：A
2. 句子 2：Inside `TakeOff`, the machine activates the motors, stores the base position in `SetBase`, climbs to `1 m`, and leaves the superstate only when the remaining distance falls below `10 cm`.
   对应摘录：B
3. 句子 3：In each frame-handling superstate, the drone first approaches the target frame, then enters `FrameClose` and lateral shift states to reduce misalignment until the tilt angle is below `3°`, at which point it transitions into `Crossing`.
   对应摘录：C
4. 句子 4：The `Crossing` state keeps the drone advancing for `4 s`, raises it for another `2 s`, and then hands control to `Landing`, where the vehicle returns to base and cuts the motors when it is within `5 cm` of the destination.
   对应摘录：D
