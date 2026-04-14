# Improving bimanual interaction with a prosthesis using semi-autonomous control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `idle -> movement classification -> UNI / BI-SYNC / BI-ASYNC -> grasp -> manual manipulation -> idle` 的半自主双手交互控制回路，并补足 `500 ms` movement buffer、方向规则、自动握型切换、接触后停用自治控制等关键件，可直接作为 `HSM + T1` 样本。

## 条目 1: Semi-autonomous bimanual coordination controller for Michelangelo hand interactions
- 控制对象：Michelangelo 多功能假手在双手协作任务中的 semi-autonomous bimanual coordination controller
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向上肢假手双手协作任务的层次化半自主控制器，用 IMU 与编码器判断交互类型，再在 `UNI / BI-SYNC / BI-ASYNC` 三类模式下自动调整 wrist orientation 与 grip type，同时保留用户肌电覆盖权。
- 判断：算。对象是真实假手控制系统，不是仅做交互评估；原文完整给出 idle/classification/automatic-control 主流程、三类双手交互模式、`500 ms` 缓冲规则、触发信号、接触停用自治控制和模式内动作。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，BPC system overview，行 233-252
> The BPC system consists of 1) an autonomous controller, which determines the prosthesis orientation and grip-type based on sensor data from Michelangelo hand prosthesis (force and position encoders) and IMU sensors ... 2) myoelectric interface for manual control, and 3) tactile feedback communicating the state of the system to the subject.
>
> The autonomous controller is active only when the prosthesis is not actively operated by myocontrol.
>
> The myocontrol has the priority over the autonomous controller, which means that the user can always override the autonomous decisions using myocontrol; hence, the overall control scheme is semi-autonomous.
>
> The control loop is closed by means of vibrotactile feedback that communicates the state of the autonomous system back to the user.

#### 摘录 B
- 出处：第 4 页，System operation，行 253-274
> In the idle state, the system waits for the subject to start the movement.
>
> When the movement is detected, the system classifies the movement into three interaction classes: unimanual prosthesis movement (UNI), bimanual synchronous movement (BI-SYNC) and bimanual asynchronous movement (BI-ASYNC).
>
> The outcome of the movement classification determines the response of the autonomous control system. Each movement type activates a specific automatic control strategy coordinating the movement of the prosthesis to that of the contralateral hand.
>
> The automatic controller continuously adjusts the orientation of the prosthesis and its grasp type. When ready for grasping, the subject closes the hand using myoelectric control, and when the contact is detected, the automatic control is deactivated ... after the object is released, the system transits back to the initial state.

#### 摘录 C
- 出处：第 4-5 页，Movement detection and classification，行 291-336
> The magnitude of acceleration and its direction are used to detect the motion of the prosthesis and the sound hand, and to distinguish between the three types of movement.
>
> While in the idle state, the system continuously monitors the acceleration to detect when the hand and the prosthesis start moving.
>
> If only the sound hand moves, the algorithm makes no decision, buffers the hand movement for 500 ms and waits for further input.
>
> This approach establishes a maximal time window in which the movement of the two hands needs to occur in order to be considered as a potential bimanual interaction.
>
> If the prosthesis moves, while the sound hand is not moving ... the movement is classified as unilateral (UNI).
>
> However, if the sound hand has moved in the last 500 ms, and the prosthesis and hand are now moving towards each other ... the movement is classified as BI-ASYNC.

#### 摘录 D
- 出处：第 6 页，Automatic control，行 351-389
> During BI-ASYNC movements, the autonomous controller expects that the user will transfer an object from the sound hand to the prosthesis. In order to facilitate this interaction, it automatically adjusts the prosthesis rotation to match the rotation of the sound limb so that the palms always face opposite directions.
>
> During BI-SYNC movements, the autonomous controller assumes that the user would grasp an object using both hands and therefore, it automatically adjusts the prosthesis rotation to match the rotation of the sound limb so that the wrists move symmetrically.
>
> Furthermore, the controller also automatically switches between the palmar and lateral grip type, depending on the orientation of the sound hand.
>
> If the hand is rotated downwards or to the side, the prosthesis assumes palmar preshape ... However, if the sound hand is rotated upwards, then the prosthesis automatically changes the preshape to the neutral (lateral fully open) ...
>
> After the object has been grasped, the control is switched to manual.

### 2. 基于原文整理后的自然语言描述

The BPC controller is a hierarchical semi-autonomous supervisor in which a manual myoelectric layer, an autonomous coordination layer, and a tactile-feedback layer are combined, with manual myocontrol always taking priority over autonomy. Its top-level state flow is `idle -> movement detection/classification -> UNI / BI-SYNC / BI-ASYNC -> grasp-ready coordination -> manual manipulation -> idle`, and contact detection explicitly disables autonomous action until the object is released. Classification is driven by prosthesis-hand acceleration magnitude and direction, and the controller keeps a `500 ms` hand-movement buffer so that sequential sound-hand then prosthesis motion can still be interpreted as a bimanual transfer rather than as two unrelated unilateral motions. In `BI-ASYNC`, the prosthesis rotates so that the palms face opposite directions for hand-to-prosthesis transfer, whereas in `BI-SYNC` it mirrors the sound limb, switches automatically between palmar and lateral preshapes, and keeps regulating wrist rotation even after grasp to support bimanual manipulation. Because the paper preserves both the discrete interaction classes and the mode-specific automatic actions, it provides an `HSM + T1` coordination sample rather than only a human-subject evaluation protocol.

### 3. 逐句溯源

1. 句子 1：The BPC controller is a hierarchical semi-autonomous supervisor in which a manual myoelectric layer, an autonomous coordination layer, and a tactile-feedback layer are combined, with manual myocontrol always taking priority over autonomy.
   对应摘录：A
2. 句子 2：Its top-level state flow is `idle -> movement detection/classification -> UNI / BI-SYNC / BI-ASYNC -> grasp-ready coordination -> manual manipulation -> idle`, and contact detection explicitly disables autonomous action until the object is released.
   对应摘录：B
3. 句子 3：Classification is driven by prosthesis-hand acceleration magnitude and direction, and the controller keeps a `500 ms` hand-movement buffer so that sequential sound-hand then prosthesis motion can still be interpreted as a bimanual transfer rather than as two unrelated unilateral motions.
   对应摘录：C
4. 句子 4：In `BI-ASYNC`, the prosthesis rotates so that the palms face opposite directions for hand-to-prosthesis transfer, whereas in `BI-SYNC` it mirrors the sound limb, switches automatically between palmar and lateral preshapes, and keeps regulating wrist rotation even after grasp to support bimanual manipulation.
   对应摘录：D
5. 句子 5：Because the paper preserves both the discrete interaction classes and the mode-specific automatic actions, it provides an `HSM + T1` coordination sample rather than only a human-subject evaluation protocol.
   对应摘录：A, B, C, D
