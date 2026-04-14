# Smart Sensors Applications for a New Paradigm of a Production Line - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然面向 smart production line 场景，但对协作机械臂的 `Monitoring / Manual Guidance / Collision Reaction / Waiting` 四态监督器给出了完整状态图、进入/退出条件、阈值和定时反应链，能稳定支撑双 A。

## 条目 1: Manual-guidance and collision-reaction supervisor for collaborative robot station

- 控制对象：工业自动化与离散制造领域的协作机械臂人工引导与碰撞反应安全监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是生产线协作机器人在正常监测、人工拖动引导、碰撞反应和等待恢复之间切换的安全监督控制器。
- 判断：算。对象是实际机器人控制器的状态监督层，不是泛化 smart factory 架构；原文明确给出四个状态、`mg_enter / mg_exit / cr_enter / cr_exit` 条件、阈值公式、`40 ms + 160 ms + 1 s` 时间链和实验验证。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5-6 页，`Basic state diagram for the state machine`，`paper_content.txt` 第 220-247 行
> The finite state machine shown in Figure 3 manages all the phases of the developed procedure; it is composed of the following four states: Monitoring, Manual Guidance, Collision Reaction, Waiting.
> The algorithm starts from the Monitoring state ...
> When an MG interaction is detected ... the system moves to the Manual Guidance state ... At this point, the system moves to the Waiting state, where a 1-s delay is imposed before returning to the Monitoring state.
> Whenever condition cr_enter is met, the system moves to the Collision Reaction state ... before returning to the Monitoring state when condition cr_exit is satisfied.

#### 摘录 B

- 出处：第 7-9 页，`Condition mg_enter / cr_enter`，`paper_content.txt` 第 273-319、331-360 行
> Condition mg_enter is achieved by comparing ... the estimated Cartesian forces applied on the end-effector Fmg(t) with a pair of varying threshold vectors Th1H(t) and Th1L(t) and ... the estimated Cartesian forces slopes with a constant threshold vector Th1s.
> Condition mg_enter is satisfied when force amplitudes cross the adaptive thresholds and the force slopes exceed the threshold.
> Condition cr_enter is obtained by comparing the vector of filtered residual currents Icd(t) with a varying threshold vector Thcd(t) ... Thcd(j)(t)=kcdc(j)+kcdv(j)|qdot|/qdotmax+kcda(j)|qddot|/qddotmax.

#### 摘录 C

- 出处：第 10-11 页，`Collision Reaction State / Waiting State`，`paper_content.txt` 第 444-500 行
> In this state, the system imposes a proper reaction strategy in order to move the TCP back ...
> The peak after an impact is attained in the subsequent 40 ms ...
> Phase 2: A constant-speed is applied for a predefined time interval (160 ms was chosen for our implementation) ...
> 2.2.4. Waiting State: The system imposes a 1-s wait before returning to the Monitoring state.

### 2. 基于原文整理后的自然语言描述

The collaborative-robot supervisor runs as a four-state EFSM with `Monitoring` as the default mode, `Manual Guidance` for intentional human dragging, `Collision Reaction` for unintended impacts, and `Waiting` for post-interaction stabilization. In `Monitoring`, the controller continuously estimates residual currents, Cartesian forces, and force slopes, and it enters `Manual Guidance` only when the filtered force magnitudes cross adaptive thresholds and their slopes exceed the configured bound, while `Collision Reaction` is triggered by high-pass residual-current thresholds that depend on joint velocity and acceleration. Once inside `Manual Guidance`, the robot remains compliant until the forces fall back within adaptive exit bands and the mean slope becomes flat; once inside `Collision Reaction`, it executes a three-phase retreat strategy built around a `40 ms` impact-peak capture window, a `160 ms` constant-speed escape segment, and a controlled stop profile. After either interaction branch, the machine enters `Waiting` for `1 s` before returning to `Monitoring`, so the whole controller is a timed safety supervisor rather than a single reaction heuristic.

### 3. 逐句溯源

1. 句子 1：The collaborative-robot supervisor runs as a four-state EFSM with `Monitoring` as the default mode, `Manual Guidance` for intentional human dragging, `Collision Reaction` for unintended impacts, and `Waiting` for post-interaction stabilization.
   对应摘录：A
2. 句子 2：In `Monitoring`, the controller continuously estimates residual currents, Cartesian forces, and force slopes, and it enters `Manual Guidance` only when the filtered force magnitudes cross adaptive thresholds and their slopes exceed the configured bound, while `Collision Reaction` is triggered by high-pass residual-current thresholds that depend on joint velocity and acceleration.
   对应摘录：A, B
3. 句子 3：Once inside `Manual Guidance`, the robot remains compliant until the forces fall back within adaptive exit bands and the mean slope becomes flat; once inside `Collision Reaction`, it executes a three-phase retreat strategy built around a `40 ms` impact-peak capture window, a `160 ms` constant-speed escape segment, and a controlled stop profile.
   对应摘录：B, C
4. 句子 4：After either interaction branch, the machine enters `Waiting` for `1 s` before returning to `Monitoring`, so the whole controller is a timed safety supervisor rather than a single reaction heuristic.
   对应摘录：A, C
