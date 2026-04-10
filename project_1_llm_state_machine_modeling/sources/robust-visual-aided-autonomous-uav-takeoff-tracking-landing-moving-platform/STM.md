# Robust Visual-Aided Autonomous Takeoff, Tracking, and Landing of a Small UAV on a Moving Landing Platform for Life-Long Operation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把小型无人机在移动平台上的自主起飞、跟踪、降落与失败恢复明确组织成五状态有限状态机，并给出 `0.5 s / 0.25 m / 0.7 m / 4 m` 等工程阈值。

## 条目 1: Five-State UAV Takeoff-Track-Land Recovery FSM

- 控制对象：航空航天与飞行/空管控制领域的移动平台无人机自主起降与恢复监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在小型旋翼无人机上的高层任务状态机，用五个离散状态组织起飞、目标平台跟踪、降落以及平台丢失时的重定位恢复。
- 判断：算。对象是真实无人机监督控制器而不是纯视觉检测算法；原文明确给出五个状态、状态图、进入恢复模式的两条 guard 以及下降速度、跟踪高度和成功着陆判定条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section `3.1. State Machine`，行 192-224
> The autonomous takeoff-tracking-landing system proposed in this paper builds upon a finite state machine ... with five states: landed, taking off, tracking, landing, and re-localizing. ... Once the nominal height has been reached (set to 4 m in our experiments), the state automatically changes to tracking ... A land command ... will trigger the start of the landing maneuver and shift the state to landing. ... the system can enter into recovery mode for either of the following two reasons: (1) ... if more than 0.5 s pass without getting a new position, the state changes to re-localizing; (2) if the relative error ... is bigger than a threshold (0.25 m in our experiments) at the final landing stages ... the system will also enter recovery mode.

#### 摘录 B

- 出处：第 6 页，Section `3.1. State Machine`，行 228-233
> The intuition behind ascending vertically is that the viewed area by the UAV's downward-looking camera is gradually increased. When the landing platform is viewed again, the state is changed to tracking and maintained so until the nominal tracking altitude of 4 m is reached again. ... this re-localization strategy will prove to be key when the landing platform moves faster than the nominal velocity, keeping the system alive and preventing failed landings.

#### 摘录 C

- 出处：第 9 页，Section `3.3.1 Height-Adaptive PID Controller`，行 401-416
> The descent speed during landing remains at a constant value of 0.3 m s-1 when flying 0.7 m above the landing platform ... Below 0.7 m, the UAV increases its downward speed notably to 2.0 m s-1. ... to be certain that the UAV has actually landed on the moving platform and not on the ground, both conditions must be met, namely (1) the sonar measurement must be smaller than a threshold persistently and (2) the IMU must indicate a non-zero linear acceleration.

### 2. 基于原文整理后的自然语言描述

The UAV behavior supervisor is a five-state FSM with `landed`, `taking off`, `tracking`, `landing`, and `re-localizing` states. After receiving a takeoff command, the vehicle ascends while running detection and tracking, and once it reaches the nominal tracking altitude of `4 m` it switches from `taking off` to `tracking`. A landing command moves the system into `landing`, where the vehicle descends while a height-adaptive PID controller keeps the UAV aligned with the landing platform in the horizontal plane. The recovery logic is explicit and engineering-oriented: if the platform is not re-detected for more than `0.5 s`, or if the relative horizontal error exceeds `0.25 m` during the final landing stage, the controller enters `re-localizing`. In that recovery state, the UAV climbs vertically until the platform is seen again and returns to `tracking`, while successful touchdown in `landing` is finally checked through persistent low-sonar readings together with non-zero IMU acceleration, and the final descent speed is increased once the altitude falls below `0.7 m`.

### 3. 逐句溯源

1. 句子 1：The UAV behavior supervisor is a five-state FSM with `landed`, `taking off`, `tracking`, `landing`, and `re-localizing` states.
   对应摘录：A
2. 句子 2：After receiving a takeoff command, the vehicle ascends while running detection and tracking, and once it reaches the nominal tracking altitude of `4 m` it switches from `taking off` to `tracking`.
   对应摘录：A
3. 句子 3：A landing command moves the system into `landing`, where the vehicle descends while a height-adaptive PID controller keeps the UAV aligned with the landing platform in the horizontal plane.
   对应摘录：A, C
4. 句子 4：The recovery logic is explicit and engineering-oriented: if the platform is not re-detected for more than `0.5 s`, or if the relative horizontal error exceeds `0.25 m` during the final landing stage, the controller enters `re-localizing`.
   对应摘录：A
5. 句子 5：In that recovery state, the UAV climbs vertically until the platform is seen again and returns to `tracking`, while successful touchdown in `landing` is finally checked through persistent low-sonar readings together with non-zero IMU acceleration, and the final descent speed is increased once the altitude falls below `0.7 m`.
   对应摘录：B, C
