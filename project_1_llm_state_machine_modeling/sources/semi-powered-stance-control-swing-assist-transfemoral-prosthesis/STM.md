# Design of a Semi-Powered Stance-Control Swing-Assist Transfemoral Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `Stance / Pre-Swing / Swing Flexion / Swing Extension` 四态 walking controller、`IMU + knee angle + load cell` guard，以及 state-specific hydraulic valve 与 cadence-adaptive spline control，可直接作为 `EFSM + T0` 样本。

## 条目 1: Four-state walking controller for the semi-powered SCSA knee
- 控制对象：semi-powered stance-control swing-assist transfemoral knee 的 walking controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `SCSA` transfemoral knee 的四态 gait supervisor，它在 `Stance / Pre-Swing / Swing Flexion / Swing Extension` 之间切换，并据此调度 hydraulic spool valve、cadence-adaptive swing trajectory 与 PD motor tracking。
- 判断：算。对象是真实主动膝假肢的 walking controller；原文给出了显式状态集合、传感器 guard、状态相关执行策略和具体 transition table。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，Section `V. WALKING CONTROLLER`，行 374-380
> A finite-state walking controller was developed for the SCSA knee ... four states: 1) Stance (ST); 2) Pre-swing (PS); 3) Swing flexion (SF); and 4) Swing extension (SE). ... moving between sequential states ... based on real-time measurements provided by the IMU, knee angle sensing, and/or the load cell.

#### 摘录 B
- 出处：第 9 页，Section `V. WALKING CONTROLLER`，行 381-392
> In the ST state, the rotary spool valve ... is closed ... In the PS state, the rotary spool valve is opened ... As the controller switches into the SF state, a cadence-adaptive spline-based swing-phase trajectory is generated ... and a PD controller is employed ... When the controller switches into the SE state ... the hydraulic spool valve is moved to the closed position.

#### 摘录 C
- 出处：第 30 页，Table `II`
> `ST to PS` Thigh angle < −5 deg
> `PS to SF` Thigh angular velocity > 0 or Force < 50 N
> `SF to SE` Knee angular velocity < −5 rad/s
> `SE to ST` Knee angle < 0 or Force > 50 N

### 2. 基于原文整理后的自然语言描述

The semi-powered `SCSA` transfemoral knee uses a four-state extended gait controller with `Stance`, `Pre-Swing`, `Swing Flexion`, and `Swing Extension` as its explicit supervisory phases. State progression is guarded by real-time sensing from the `IMU`, knee-angle channel, and axial load cell rather than by a fixed cadence script. In `Stance`, the hydraulic spool valve is closed so knee flexion is blocked and the motor remains inactive, while `Pre-Swing` opens the valve to let the user initiate unloading. Once the controller enters `Swing Flexion`, it generates a cadence-adaptive spline reference and tracks that reference through a `PD` motor controller; in `Swing Extension`, the motor keeps tracking while the hydraulic valve is closed again to prepare stable terminal extension. The transition table is fully explicit, using `thigh angle < -5 deg`, `thigh angular velocity > 0 or Force < 50 N`, `knee angular velocity < -5 rad/s`, and `knee angle < 0 or Force > 50 N` to close the full walking loop.

### 3. 逐句溯源

1. 句子 1：The semi-powered `SCSA` transfemoral knee uses a four-state extended gait controller with `Stance`, `Pre-Swing`, `Swing Flexion`, and `Swing Extension` as its explicit supervisory phases.
   对应摘录：A
2. 句子 2：State progression is guarded by real-time sensing from the `IMU`, knee-angle channel, and axial load cell rather than by a fixed cadence script.
   对应摘录：A, C
3. 句子 3：In `Stance`, the hydraulic spool valve is closed so knee flexion is blocked and the motor remains inactive, while `Pre-Swing` opens the valve to let the user initiate unloading.
   对应摘录：B
4. 句子 4：Once the controller enters `Swing Flexion`, it generates a cadence-adaptive spline reference and tracks that reference through a `PD` motor controller; in `Swing Extension`, the motor keeps tracking while the hydraulic valve is closed again to prepare stable terminal extension.
   对应摘录：B
5. 句子 5：The transition table is fully explicit, using `thigh angle < -5 deg`, `thigh angular velocity > 0 or Force < 50 N`, `knee angular velocity < -5 rad/s`, and `knee angle < 0 or Force > 50 N` to close the full walking loop.
   对应摘录：C
