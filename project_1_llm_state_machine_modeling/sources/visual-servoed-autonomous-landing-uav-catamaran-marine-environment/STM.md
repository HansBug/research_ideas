# Visual Servoed Autonomous Landing of an UAV on a Catamaran in a Marine Environment - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把海上平台回收任务写成 `8` 状态 landing FSM，并给出 searching 圆轨迹、`timeout`、`>1 s` 失视悬停、`0.1 m` 高度步进和最终着陆阈值，是一条完整的双 A 飞行监督控制样本。

## 条目 1: Eight-State Catamaran Landing FSM
- 控制对象：航空航天与飞行控制领域的海上平台 UAV 自主降落监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于四旋翼在海上 catamaran 平台上自主回收的 landing FSM，用初始化、搜索、跟踪、悬停、升降、补偿和着陆阶段协调视觉与超声传感。
- 判断：算。对象是真实 UAV 降落监督控制器，不是单独视觉算法；原文给出完整状态图、各状态职责、时间触发条件和安全着陆 guard。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7 页，Section `3.4. Finite State Machine`
> The landing phase is described by a series of connected states, whose transitions are handled by a finite state machine. The behavior of the quadrotor is described by eight states: initialization, searching, tracking, hovering, descending, ascending, compensation, and landing; Figure 4 describes how the states are linked. The transitions among them are triggered by boolean algebra operations.
>
> ... Platform not Visible ... Aligned with Platform ... Vision Data not Valid ... After a Timeout ... Comp Ready ... Ready To Land.

#### 摘录 B
- 出处：第 8-9 页，Section `3.4.2. Searching`
> If the quadrotor has no visual information about the position of the landing platform, it enters a state where it searches for it. To this end, the quadrotor reaches a predefined altitude and flies in circles increasing in radius.
>
> The searching continues until the following condition is verified:
> (t-t0) < 2πR / vs.
>
> When this condition is no longer true, the parameters are updated: R is increased by 0.5 m ... t0 is set to the current value of t ... the quadrotor starts a new circle, but with an increased radius.

#### 摘录 C
- 出处：第 9-10 页，Sections `3.4.4-3.4.8`
> This state handles the case when the vision data coming from the camera have not been updated for more than a second. In that case, the quadrotor is asked to keep its position for a certain period until the vision system is back online ...
>
> The altitude waypoints are autonomously adjusted by being decreased by 0.1 m at each iteration.
>
> The altitude waypoints are autonomously adjusted by being increased by 0.1 m at each iteration.
>
> When the quadrotor is sufficiently close to the platform and the relative velocity between the two agents is under a certain threshold, the finite state machine enters the landing state, where the motors of the quadrotors are shut down ...

### 2. 基于原文整理后的自然语言描述

The catamaran-recovery controller is a flat eight-state landing FSM with `initialization`, `searching`, `tracking`, `hovering`, `descending`, `ascending`, `compensation`, and `landing` states. After rendezvous by GNSS, `initialization` positions the UAV in front of the landing platform; if the platform is not visible, the FSM enters `searching`, where the quadrotor flies circles around the search start point and starts a new circle whenever `(t-t0)` exceeds `2πR/vs`, increasing the radius by `0.5 m` each time. Once the platform is reacquired, the machine returns to initialization and then to `tracking`, where horizontal and vertical errors are reduced until the vehicle is aligned for the lower-altitude phases. If vision data are missing for more than `1 s`, the FSM switches to `hovering`; if tracking is valid but the vehicle is too high it goes to `descending`, and if visual contact is lost while flying too low it goes to `ascending`, with both states updating altitude waypoints in `0.1 m` steps. When the UAV is centered, close enough to the platform, and moving with sufficiently low relative velocity, the machine enters `compensation` and then `landing`, where the motors are shut down so the aircraft can settle onto the catamaran.

### 3. 逐句溯源

1. 句子 1：The catamaran-recovery controller is a flat eight-state landing FSM with `initialization`, `searching`, `tracking`, `hovering`, `descending`, `ascending`, `compensation`, and `landing` states.
   对应摘录：A
2. 句子 2：After rendezvous by GNSS, `initialization` positions the UAV in front of the landing platform; if the platform is not visible, the FSM enters `searching`, where the quadrotor flies circles around the search start point and starts a new circle whenever `(t-t0)` exceeds `2πR/vs`, increasing the radius by `0.5 m` each time.
   对应摘录：A, B
3. 句子 3：Once the platform is reacquired, the machine returns to initialization and then to `tracking`, where horizontal and vertical errors are reduced until the vehicle is aligned for the lower-altitude phases.
   对应摘录：A, B
4. 句子 4：If vision data are missing for more than `1 s`, the FSM switches to `hovering`; if tracking is valid but the vehicle is too high it goes to `descending`, and if visual contact is lost while flying too low it goes to `ascending`, with both states updating altitude waypoints in `0.1 m` steps.
   对应摘录：C
5. 句子 5：When the UAV is centered, close enough to the platform, and moving with sufficiently low relative velocity, the machine enters `compensation` and then `landing`, where the motors are shut down so the aircraft can settle onto the catamaran.
   对应摘录：A, C
