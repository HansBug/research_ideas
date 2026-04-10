# A Novel Approach to Automated Tracking Control of Hybrid Tilting Rotor UAVs Using LQG Controller and State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 tilt-rotor UAV 的 hover / transition / fixed-wing 控制切换写成基于状态机的 LQG gain-scheduling 监督器，并给出 90°→0° 倾转、`0 → -2 → -4 → -2 → 0` 垂向参考和 `K1-K9` 切换过程，细节达到双 A。

## 条目 1: LQG Gain-Switching Supervisor for Hybrid Tilting-Rotor UAV

- 控制对象：hybrid tilting-rotor UAV 的纵向飞行状态切换与 LQG controller supervisor
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 tilt-rotor UAV 的状态机监督控制器，用当前飞行状态触发 Kalman filter 参数和 LQ gain 的切换，并在 hover、transition、fixed-wing 之间完成自动模式过渡。
- 判断：算。对象是具体 UAV 的控制器而不是一般增益调度方法；原文明确给出状态机职责、切换信号、倾转角门槛、速度参考序列和 `K1-K9` 过渡过程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10 页，Section 3.2
> "finite state machine (FSM)"

#### 摘录 B

- 出处：第 11 页，Section 4.1
> "from 0 to -2 and then to -4"

#### 摘录 C

- 出处：第 12 页，Section 4.2
> "within 32 seconds"

### 2. 基于原文整理后的自然语言描述

The hybrid tilt-rotor controller uses a finite-state supervisory layer to switch both Kalman-filter parameters and LQ gain matrices according to the current operational state of the aircraft. In the hover takeoff phase, the state machine keeps the forward-speed reference at zero and commands the vertical-speed reference through the sequence `0 -> -2 -> -4 -> -2 -> 0`, while the controller compensates pitch to keep the vehicle climbing vertically. During the transition phase, the rotor tilts from `90°` to `0°`; because the thrust vector then produces coupled forward and downward acceleration, the state machine disables the outer loop by setting `Kouter` to zero and concentrates control on pitch angle and pitch rate. Once the tilting angle reaches `0°`, the outer loop is re-enabled and the rear rotor is disabled so the pitching moment is generated only through the elevator in fixed-wing mode. The gain-scheduling part of the controller is also state-driven: the aircraft starts in hover gains `K1` to `K3`, moves to `K4` as transition begins, and eventually reaches `K9` after the fixed-wing mode is fully established. The reported nonlinear simulation completes the stable transition within 32 seconds with 289.3 m horizontal and 50.6 m vertical displacement, so the machine is not only mode-based but also explicitly tied to engineering timing and continuous flight dynamics.

### 3. 逐句溯源

1. 句子 1：The hybrid tilt-rotor controller uses a finite-state supervisory layer to switch both Kalman-filter parameters and LQ gain matrices according to the current operational state of the aircraft.
   对应摘录：A；`paper_content.txt` 第 462-478 行。
2. 句子 2：In the hover takeoff phase, the state machine keeps the forward-speed reference at zero and commands the vertical-speed reference through the sequence `0 -> -2 -> -4 -> -2 -> 0`, while the controller compensates pitch to keep the vehicle climbing vertically.
   对应摘录：B；`paper_content.txt` 第 491-498 行。
3. 句子 3：During the transition phase, the rotor tilts from `90°` to `0°`; because the thrust vector then produces coupled forward and downward acceleration, the state machine disables the outer loop by setting `Kouter` to zero and concentrates control on pitch angle and pitch rate.
   对应摘录：A, B；`paper_content.txt` 第 499-503 行。
4. 句子 4：Once the tilting angle reaches `0°`, the outer loop is re-enabled and the rear rotor is disabled so the pitching moment is generated only through the elevator in fixed-wing mode.
   对应摘录：B；`paper_content.txt` 第 503-506 行。
5. 句子 5：The gain-scheduling part of the controller is also state-driven: the aircraft starts in hover gains `K1` to `K3`, moves to `K4` as transition begins, and eventually reaches `K9` after the fixed-wing mode is fully established.
   对应摘录：B；`paper_content.txt` 第 523-532 行。
6. 句子 6：The reported nonlinear simulation completes the stable transition within 32 seconds with 289.3 m horizontal and 50.6 m vertical displacement, so the machine is not only mode-based but also explicitly tied to engineering timing and continuous flight dynamics.
   对应摘录：C；`paper_content.txt` 第 18-21 行，523-532 行。
