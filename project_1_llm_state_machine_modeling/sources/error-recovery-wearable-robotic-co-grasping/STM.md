# Error recovery in wearable robotic Co-Grasping: the role of human-led correction - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 wearable co-grasping gripper 的开合、保持、可靠抓取、抓取错误与人为纠错链明确实现为 device state machine，状态和 guard 都足够完整。

## 条目 1: Human-led error-recovery co-grasp controller

- 控制对象：医疗设备与生命支持控制领域的 wearable robotic co-grasping gripper controller
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个控制可穿戴协同抓握器开合、保持、抓取成功/失败与人工接管恢复的抓握状态机。
- 判断：算。对象是真实 wearable robotic gripper 的 device controller，不是实验流程；原文明确给出 `Maintain Aperture`、`Automated Open`、`Automated Close`、`Reliable Grasp`、`Grasp Error` 和 `Transfer` 等状态及其事件/条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Section `2.1.1 Control and actuation`，`paper_content.txt` 第 300-325 行
> The implemented finite state machine (FSM) ... represents the software used to control the robotic agent throughout the study.
>
> participants primarily interacted with the system via voice commands, using the key words “open” and “close” to indicate to the robot which actions to perform.
>
> transitioned the device control to the Maintain Aperture state ... the robot tracked their wrist position ... to maintain the gripper’s current aperture.

#### 摘录 B

- 出处：第 4-5 页，open/close transitions，`paper_content.txt` 第 326-337 行
> the participant said “open” and the researcher pressed the open button to transition the system to the Automated Open state ...
>
> Once β reached βopengoal, measured to be 95°, the system automatically returned to the Maintain Aperture state ...
>
> the user ... said “close” to initiate the grasp ... the researcher then pressed the close button once to transition the device into the Automated Close state ...

#### 摘录 C

- 出处：第 5 页，Figure 3 and reliable-grasp branch，`paper_content.txt` 第 342-358 行
> Device state machine (A) overview and (B) detailed grasping logic.
>
> When the switch is down in (B), the probability of Grasp Error is 44% and Reliable Grasp is 56%.
>
> When the control switch was up, the system facilitated a Reliable Grasp ... halting motor movement only when ... β=βclosegoal, which was approximately 65° ... Upon this observation ... transitioning to the Transfer state.

#### 摘录 D

- 出处：第 6 页，error-recovery branch，`paper_content.txt` 第 363-376 行
> γclosegoal was pseudorandomly defined as a motor contribution angle varying between 6–18°, or 20%–60% of the γ needed to securely grasp the test object, resulting in insufficient gripper closure (β>βclosegoal).
>
> Despite this unsuccessful grasp, the system automatically entered the Transfer state after prematurely stopping robot motion.
>
> Completing grasps successfully after a Grasp Error required the participant to move their wrist (+Δα) to actuate the device and finish closing the gripper (β=βclosegoal).
>
> In the Transfer state, the robot no longer moved the motor (Δγ=0) until the user said “open” again ...

### 2. 基于原文整理后的自然语言描述

The wearable Co-Grasping device is controlled by an explicit finite-state machine centered on `Maintain Aperture`, `Automated Open`, `Automated Close`, `Reliable Grasp`, `Grasp Error`, and `Transfer`. After a calibration step, the controller enters `Maintain Aperture`, where wrist motion and motor motion satisfy `Δγ = -Δα` so that the current gripper aperture is preserved while the user repositions the wrist. On the `open` command, the machine transitions to `Automated Open`, drives the motor until `β` reaches `βopengoal = 95°`, and then returns to `Maintain Aperture`; on the `close` command, it enters `Automated Close`. A control switch then selects either a `Reliable Grasp`, where closure continues until the observed target `βclosegoal ≈ 65°` secures the object, or a pseudo-random `Grasp Error`, which occurs `44%` of the time. In the error branch the motor contribution is limited to `6-18°`, or only `20%-60%` of the required closing contribution, the machine still enters `Transfer`, and the human must use wrist actuation to complete closure before the next `open` command restarts the cycle.

### 3. 逐句溯源

1. 句子 1：The wearable Co-Grasping device is controlled by an explicit finite-state machine centered on `Maintain Aperture`, `Automated Open`, `Automated Close`, `Reliable Grasp`, `Grasp Error`, and `Transfer`.
   对应摘录：A, C
2. 句子 2：After a calibration step, the controller enters `Maintain Aperture`, where wrist motion and motor motion satisfy `Δγ = -Δα` so that the current gripper aperture is preserved while the user repositions the wrist.
   对应摘录：A
3. 句子 3：On the `open` command, the machine transitions to `Automated Open`, drives the motor until `β` reaches `βopengoal = 95°`, and then returns to `Maintain Aperture`; on the `close` command, it enters `Automated Close`.
   对应摘录：B
4. 句子 4：A control switch then selects either a `Reliable Grasp`, where closure continues until the observed target `βclosegoal ≈ 65°` secures the object, or a pseudo-random `Grasp Error`, which occurs `44%` of the time.
   对应摘录：C
5. 句子 5：In the error branch the motor contribution is limited to `6-18°`, or only `20%-60%` of the required closing contribution, the machine still enters `Transfer`, and the human must use wrist actuation to complete closure before the next `open` command restarts the cycle.
   对应摘录：D
