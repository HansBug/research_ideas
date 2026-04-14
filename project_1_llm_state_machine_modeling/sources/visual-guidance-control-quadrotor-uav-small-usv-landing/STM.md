# A Visual Guidance and Control Method for Autonomous Landing of a Quadrotor UAV on a Small USV - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `Idle / Approaching / Landing` 三阶段 landing FSM、event-triggered bounding-box yaw logic，以及 `marker lost > 0.3 s -> Hold` 的 failsafe 回退链，可直接作为高质量回收控制样本入账。

## 条目 1: Small-USV landing supervisor for a quadrotor UAV
- 控制对象：四旋翼 `UAV` 面向小型 `USV` 回收任务的高层自主降落监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `UAV` 在小型 `USV` 上回收的 landing supervisor，用于协调悬停待命、轨迹接近、视觉着陆和目标丢失后的安全保持。
- 判断：算。对象是真实 UAV 回收控制器，不是纯视觉流程；原文给出了顶层状态、进入条件、空间 guard 和短时失视恢复链，能够恢复完整高层控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section `2.3. Finite State Machine`
> The UAV flight process is divided into the following three stages, which the Finite-State Machine (FSM) uses to determining the UAV’s behavior:
>
> Idle ... The UAV hovers in the air, waiting for further commands.
>
> Approaching ... the UAV automatically computes an optimized trajectory ... When the UAV’s front-facing camera detects the fiducial marker ... the state automatically switches to the Landing stage.
>
> Landing ... When the relative pose error between the UAV and the ArUco fiducial marker falls below the threshold value, the motors are shut down and the UAV falls onto the landing platform, completing the landing.

#### 摘录 B
- 出处：第 13-14 页，Section `4.2. Event-Triggered Yaw Control`
> An event-triggered mechanism is introduced by establishing a virtual bounding box around the UAV’s target landing point.
>
> When the UAV is outside the bounding box, ψdes remains constant and the UAV primarily relies on translational motion to minimize position error ... When the UAV enters the bounding box, ψdes is adjusted based on rdev.
>
> The target landing point is located ... 75 cm in front of the ... marker ...
>
> the bounding box height was set to 60 cm ... The length and width were set to 50 cm and 25 cm, respectively.

#### 摘录 C
- 出处：第 17-18 页，Section `4.4. Failsafe Mechanism`
> If the fiducial marker becomes undetectable for more than 0.3 s, the system automatically switches the UAV’s flight mode in the PX4 flight stack from Offboard to Hold.
>
> In Hold mode, the UAV hovers at its current position, maintaining stability against wind and other external disturbances.
>
> When the marker is detected again, the system switches the flight mode back to Offboard, allowing the UAV to resume visual tracking.

#### 摘录 D
- 出处：第 18 页，Section `4.4. Failsafe Mechanism`
> At 54 s, the fiducial marker was occluded manually ... causing the flight mode to switch from Offboard to Hold. When the marker reappeared at 75 s, the UAV automatically resumed Offboard flight mode and continued visual tracking.

### 2. 基于原文整理后的自然语言描述

The quadrotor recovery controller is organized as a three-stage landing FSM with `Idle`, `Approaching`, and `Landing` states for autonomous docking on a small `USV`. From `Idle`, the UAV hovers and waits for a landing command; once commanded, it enters `Approaching`, computes an optimized waypoint-based trajectory, and follows it until the front-facing camera detects the platform marker, which triggers the switch to `Landing`. During `Landing`, visual guidance is refined by an event-triggered bounding-box guard: while the UAV is outside the box, heading is held constant so translation dominates, but once it enters the box, yaw is actively corrected toward a target landing point located `75 cm` in front of the marker, with box dimensions `60 cm × 50 cm × 25 cm`. The landing process terminates when the relative pose error falls below the prescribed threshold and the motors are shut down to settle onto the platform. To preserve safety under visual uncertainty, the supervisor switches PX4 from `Offboard` to `Hold` whenever the marker is lost for more than `0.3 s`, and returns to `Offboard` as soon as the marker is detected again.

### 3. 逐句溯源

1. 句子 1：The quadrotor recovery controller is organized as a three-stage landing FSM with `Idle`, `Approaching`, and `Landing` states for autonomous docking on a small `USV`.
   对应摘录：A
2. 句子 2：From `Idle`, the UAV hovers and waits for a landing command; once commanded, it enters `Approaching`, computes an optimized waypoint-based trajectory, and follows it until the front-facing camera detects the platform marker, which triggers the switch to `Landing`.
   对应摘录：A
3. 句子 3：During `Landing`, visual guidance is refined by an event-triggered bounding-box guard: while the UAV is outside the box, heading is held constant so translation dominates, but once it enters the box, yaw is actively corrected toward a target landing point located `75 cm` in front of the marker, with box dimensions `60 cm × 50 cm × 25 cm`.
   对应摘录：B
4. 句子 4：The landing process terminates when the relative pose error falls below the prescribed threshold and the motors are shut down to settle onto the platform.
   对应摘录：A
5. 句子 5：To preserve safety under visual uncertainty, the supervisor switches PX4 from `Offboard` to `Hold` whenever the marker is lost for more than `0.3 s`, and returns to `Offboard` as soon as the marker is detected again.
   对应摘录：C, D
