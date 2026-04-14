# Design and Evaluation of Stand-to-Sit and Sit-to-Stand Control Protocols for a HIP-Knee-Ankle-Foot Prosthesis with a Motorized Hip Joint - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `idle posture detection -> sit-to-stand / stand-to-sit protocol -> phase impedance controller` 写成了完整层次控制链，并给出 `4 + 4` 相位、显式 guard、`5 s` idle 判定和 phase-specific assist/damping law，可直接作为 `HSM + T1` 样本。

## 条目 1: Hierarchical sit-stand protocol controller for the motorized HKAF Power Hip
- 控制对象：带 motorized hip joint 的 `HKAF` prosthesis 坐下/起立控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `Power Hip HKAF` prosthesis 的层次 sit/stand controller，它先根据 `hip angle + thigh IMU + axial force sensor` 判定 `idle sitting / idle standing`，再分别进入 `sit-to-stand` 或 `stand-to-sit` 的四阶段 impedance submachine，并在每一阶段切换不同的 assistive / damping torque law。
- 判断：算。对象是真实髋离断假肢控制器，不是实验流程；原文明确给出了顶层模式选择、双子协议、相位 guard、局部时间判据和 state-specific torque parameters。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `3. Control Strategy`
> the control strategy ... extends ... by developing two new sets of finite state machines to decompose sitting/standing activities into a series of shorter phases ... If the user is in idle sitting mode, the sit-to-stand control protocol is executed ... if the user is in idle standing mode, the stand-to-sit protocol is activated.

#### 摘录 B
- 出处：第 4-5 页，Section `3. Control Strategy`
> Regulation of Power Hip assistive and damping torques ... was performed by a finite-state-based impedance controller ... Sit-to-stand and stand-to-sit activities were divided into four distinct chronological phases. Progression between phases occurs only when predefined transition conditions are met.

#### 摘录 C
- 出处：第 6 页，Section `3.1`
> The transition from Phase 1 to Phase 2 ... ground reaction force ... must exceed `2%` of the body weight ... the hip angle must meet or exceed ... `θST_Phase1` ... The transition from Phase 2 to Phase 3 occurs when sufficient propulsion height is achieved ... using the thigh angle measured by the Power Hip IMU.

#### 摘录 D
- 出处：第 7 页，Section `3.1`
> Power Hip control locks in position when a downward COM displacement is detected (`ωHip > 0 deg/s`) ... High damping torque is applied ... `K > 100 N·m/deg` ... Phase 4 ... generates a high assistive hip extension torque ... simultaneously rotates the knee joint into full extension.

#### 摘录 E
- 出处：第 8-9 页，Section `3.2`
> During Phase 1 ... the participant uses their pelvis to perform rapid hip extension ... The transition condition is `ωHip < ωSI_Phase1 < 0 deg/s` ... The transition from Phase 2 to Phase 3 is completed once `θHip ≥ θSI_Phase2` ... The transition from Phase 3 to Phase 4 ... when the COM is a few centimetres above the seat.

### 2. 基于原文整理后的自然语言描述

The `Power Hip` controller is hierarchical: a top layer first detects whether the prosthesis is in `idle sitting` or `idle standing` from hip angle, thigh tilt, and axial loading, and then dispatches execution into either a `sit-to-stand` or a `stand-to-sit` phase machine. Each of those two activity protocols is itself a four-phase finite-state impedance controller, so the full structure is not a single flat sequence but a mode selector over two separate submachines. In the sit-to-stand branch, the controller moves from forward lean to chair push-off once force exceeds `2% BW` and hip extension crosses `θST_Phase1`, then uses IMU-derived thigh height to detect the transition into vertical displacement, and finally applies a high-assist recovery torque that drives the hip and prosthetic knee back to full extension. During vertical displacement it explicitly detects downward `COM` motion through `ωHip > 0 deg/s` and switches to a high-damping lock state to avoid falling back into the chair. In the stand-to-sit branch, the controller first reduces the knee extension moment with a rapid hip-extension kick, then triggers knee flexion, controlled descent, and final settling using explicit guards such as `ωHip < ωSI_Phase1`, `θHip ≥ θSI_Phase2`, and a seat-height threshold derived from thigh tilt, while a `5 s` posture hold is used in the top-level idle-state detection.

### 3. 逐句溯源

1. 句子 1：The `Power Hip` controller is hierarchical: a top layer first detects whether the prosthesis is in `idle sitting` or `idle standing` from hip angle, thigh tilt, and axial loading, and then dispatches execution into either a `sit-to-stand` or a `stand-to-sit` phase machine.
   对应摘录：A
2. 句子 2：Each of those two activity protocols is itself a four-phase finite-state impedance controller, so the full structure is not a single flat sequence but a mode selector over two separate submachines.
   对应摘录：B
3. 句子 3：In the sit-to-stand branch, the controller moves from forward lean to chair push-off once force exceeds `2% BW` and hip extension crosses `θST_Phase1`, then uses IMU-derived thigh height to detect the transition into vertical displacement, and finally applies a high-assist recovery torque that drives the hip and prosthetic knee back to full extension.
   对应摘录：C, D
4. 句子 4：During vertical displacement it explicitly detects downward `COM` motion through `ωHip > 0 deg/s` and switches to a high-damping lock state to avoid falling back into the chair.
   对应摘录：D
5. 句子 5：In the stand-to-sit branch, the controller first reduces the knee extension moment with a rapid hip-extension kick, then triggers knee flexion, controlled descent, and final settling using explicit guards such as `ωHip < ωSI_Phase1`, `θHip ≥ θSI_Phase2`, and a seat-height threshold derived from thigh tilt, while a `5 s` posture hold is used in the top-level idle-state detection.
   对应摘录：A, E
