# VUB-CYBERLEGs CYBATHLON 2016 Beta-Prosthesis: case study in control of an active two degree of freedom transfemoral prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `CYBATHLON` 义肢的任务级状态机选择、`idle` 安全态、基于陀螺/关节角/踝部力矩的转移信号，以及 `sit-to-stand / stair-climbing` 子状态机细节，可直接作为层次化义肢监督控制样本。

## 条目 1: Task-selectable hierarchical supervisor for the VUB-CYBERLEGs transfemoral prosthesis
- 控制对象：`VUB-CYBERLEGs` 主动双自由度股骨假肢的任务级监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个为主动膝踝假肢选择任务模式并在每个任务模式下运行子状态机的层次化监督控制器，用于 `sit-to-stand`、`stair climbing`、`slope walking` 等多任务切换。
- 判断：算。对象是真实下肢义肢控制器，不是赛事流程；原文明确给出顶层任务选择、`idle` 安全态、传感触发条件、子状态机输出轨迹和超时回退逻辑，适合作为层次状态机样本。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `Prosthesis attitude detection`
> The prosthesis was controlled by a finite state machine ... determined by inertial rate gyros found on the pilot’s thigh ... prosthesis kinematic values could be used to determine state transitions, such as knee angle or ankle angles ... ankle torque ... was used as a trigger for some of the states.

#### 摘录 B
- 出处：第 6 页，Figure 4 / Section `Events and control methods for the CYBATHLON`
> Each of these state machines consisted of trajectory generators for the KD, ankle actuator, and WA systems ... The five prosthesis functions ... correspond to the sit-to-stand, hurdles, slope walking, stair climbing, and normal walking states ... The green “Zzz” button can be pressed at any time to send the device to the Idle state.

#### 摘录 C
- 出处：第 7 页，Section `Sit to stand`
> Figure 6 shows the sit-to-stand mode of the state machine, showing that it contained two different torque profiles based on whether the pilot was standing or sitting ... The states were switched based on the knee angle.

#### 摘录 D
- 出处：第 8-9 页，Section `Stair climbing and descent`
> The stair climbing task required the pilot to climb and then descend a set of 6 standardized stairs ... The ankle angle was held neutral for stance and pushoff, while during swing it was changed to a 20 degree dorsiflexion ... the ankle was used as a torque sensing device to detect footfall and weight transfer ... if the device remains in any of the stair ascent states for longer than a timeout period (t), the device returns to the slope down state.

### 2. 基于原文整理后的自然语言描述

The VUB-CYBERLEGs transfemoral prosthesis is organized as a hierarchical supervisor in which the pilot selects one of several task-level state machines, including `sit-to-stand`, `hurdles`, `slope walking`, `stair climbing`, and `normal walking`, while an `Idle` state can be entered at any time as the safest locked configuration. Each task-level machine drives coordinated trajectories for the knee drive, ankle actuator, and weight-acceptance mechanism, with the trajectory amplitudes and switching thresholds tuned from human-task observations and experiments. Transitions are triggered by multiple sensed variables rather than a single gait phase clock: thigh gyros capture user intention, knee and ankle kinematics identify internal progress, and ankle torque estimates from compliance are used to detect loading events. In the `sit-to-stand` submachine, the controller alternates between standing and sitting torque profiles, shifts the ankle to a slightly plantarflexed seat-compatible posture, and switches states according to knee angle. In the `stair-climbing` submachine, the ankle stays neutral during `stance` and `pushoff`, changes to `20°` dorsiflexion during `swing`, uses ankle torque sensing to detect footfall and weight transfer onto the new stair, and falls back to a safe descent state if any ascent state exceeds the configured timeout.

### 3. 逐句溯源

1. 句子 1：The VUB-CYBERLEGs transfemoral prosthesis is organized as a hierarchical supervisor in which the pilot selects one of several task-level state machines, including `sit-to-stand`, `hurdles`, `slope walking`, `stair climbing`, and `normal walking`, while an `Idle` state can be entered at any time as the safest locked configuration.
   对应摘录：B
2. 句子 2：Each task-level machine drives coordinated trajectories for the knee drive, ankle actuator, and weight-acceptance mechanism, with the trajectory amplitudes and switching thresholds tuned from human-task observations and experiments.
   对应摘录：B
3. 句子 3：Transitions are triggered by multiple sensed variables rather than a single gait phase clock: thigh gyros capture user intention, knee and ankle kinematics identify internal progress, and ankle torque estimates from compliance are used to detect loading events.
   对应摘录：A
4. 句子 4：In the `sit-to-stand` submachine, the controller alternates between standing and sitting torque profiles, shifts the ankle to a slightly plantarflexed seat-compatible posture, and switches states according to knee angle.
   对应摘录：C
5. 句子 5：In the `stair-climbing` submachine, the ankle stays neutral during `stance` and `pushoff`, changes to `20°` dorsiflexion during `swing`, uses ankle torque sensing to detect footfall and weight transfer onto the new stair, and falls back to a safe descent state if any ascent state exceeds the configured timeout.
   对应摘录：D
