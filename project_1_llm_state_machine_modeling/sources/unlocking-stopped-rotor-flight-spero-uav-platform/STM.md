# Unlocking Stopped-Rotor Flight: Development and Validation of SPERO, a Novel UAV Platform - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 SPERO stopped-rotor UAV 的安全、VTOL、固定翼、前向转换和后向转换控制模式写成 11 状态模式管理器，并给出 80 rad/s、10 m/s、4.2 s 与 3.8 s 等关键门控或验证时间，适合作为飞行器构型重配置 HSM 样本。

## 条目 1: SPERO Stopped-Rotor Bidirectional Transition Mode Manager

- 控制对象：SPERO stopped-rotor UAV 的飞行构型重配置与模式切换控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空航天领域 stopped-rotor UAV 的高层飞行状态机，用来协调 PX4 multicopter / fixed-wing controller、主旋翼、counterbalance、翼面翻转和 CoP 机构。
- 判断：算。对象是实际飞行平台的控制器，不是仿真流程；原文明确给出模式分组、状态顺序、速度/转速门控、构型动作和双向转换验证时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10 页，Section V
> "eleven discrete modes, grouped into five categories"

#### 摘录 B

- 出处：第 10 页，Section V-B
> "steady-state speed of 80 rad/s"

#### 摘录 C

- 出处：第 6 页，Table I
> "forward transition time 4.2 s"

### 2. 基于原文整理后的自然语言描述

The SPERO flight controller is a hierarchical mode manager with eleven discrete modes grouped into safety, VTOL, forward-flight, forward-transition, and backward-transition categories. The safety layer contains `disarmed`, `armed`, and globally reachable `kill`: on power-up the vehicle starts disarmed with motors disabled, the armed state enables motors at zero speed and readies the system, and `kill` immediately disables every motor regardless of the current flight mode. From rest, the VTOL branch enters `rotor spin-up`; the aircraft remains on the ground until the main rotor reaches 80 rad/s, after which it enters `VTOL` and controls translational velocity, altitude, and yaw with the multicopter controller. In forward flight, SPERO behaves as a fixed-wing aircraft with the main rotor locked as a lifting surface; below 10 m/s it uses a hybrid MC/FWC controller for altitude stability, and above 10 m/s it can rely on fixed-wing control. The forward-transition branch moves from `VTOL` to `deceleration preparation`, reverses the counterbalance orientation, enters `rotor deceleration` to slow the main rotor while counterbalances cancel torque, then enters `forward flight initiation` to flip the wing, rotate counterbalances forward, shift CoP aft, and finally transfer to `forward flight`. The backward-transition branch starts when forward speed drops below 10 m/s, moves through `VTOL initiation` to shift CoP forward and flip the wing back, then enters `rotor acceleration` where the rotor accelerates at a constant rate while the quadcopter holds position, roll, and pitch and yaw is controlled by counterbalances. Flight validation reports a measured forward-transition time of 4.2 s and backward-transition time of 3.8 s, so the machine has explicit engineering timing as well as continuous flight-regime coupling.

### 3. 逐句溯源

1. 句子 1：The SPERO flight controller is a hierarchical mode manager with eleven discrete modes grouped into safety, VTOL, forward-flight, forward-transition, and backward-transition categories.
   对应摘录：A；`paper_content.txt` 第 676-689 行。
2. 句子 2：The safety layer contains `disarmed`, `armed`, and globally reachable `kill`: on power-up the vehicle starts disarmed with motors disabled, the armed state enables motors at zero speed and readies the system, and `kill` immediately disables every motor regardless of the current flight mode.
   对应摘录：A；`paper_content.txt` 第 707-719 行。
3. 句子 3：From rest, the VTOL branch enters `rotor spin-up`; the aircraft remains on the ground until the main rotor reaches 80 rad/s, after which it enters `VTOL` and controls translational velocity, altitude, and yaw with the multicopter controller.
   对应摘录：B；`paper_content.txt` 第 720-726 行。
4. 句子 4：In forward flight, SPERO behaves as a fixed-wing aircraft with the main rotor locked as a lifting surface; below 10 m/s it uses a hybrid MC/FWC controller for altitude stability, and above 10 m/s it can rely on fixed-wing control.
   对应摘录：A；`paper_content.txt` 第 727-735 行。
5. 句子 5：The forward-transition branch moves from `VTOL` to `deceleration preparation`, reverses the counterbalance orientation, enters `rotor deceleration` to slow the main rotor while counterbalances cancel torque, then enters `forward flight initiation` to flip the wing, rotate counterbalances forward, shift CoP aft, and finally transfer to `forward flight`.
   对应摘录：A；`paper_content.txt` 第 740-759 行。
6. 句子 6：The backward-transition branch starts when forward speed drops below 10 m/s, moves through `VTOL initiation` to shift CoP forward and flip the wing back, then enters `rotor acceleration` where the rotor accelerates at a constant rate while the quadcopter holds position, roll, and pitch and yaw is controlled by counterbalances.
   对应摘录：A；`paper_content.txt` 第 760-772 行。
7. 句子 7：Flight validation reports a measured forward-transition time of 4.2 s and backward-transition time of 3.8 s, so the machine has explicit engineering timing as well as continuous flight-regime coupling.
   对应摘录：C；`paper_content.txt` 第 243-245 行。
