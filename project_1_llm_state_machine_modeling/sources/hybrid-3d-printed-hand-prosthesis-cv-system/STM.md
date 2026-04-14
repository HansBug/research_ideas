# A Hybrid 3D Printed Hand Prosthesis Prototype Based on sEMG and a Fully Embedded Computer Vision System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `sEMG pulse -> laser/camera -> CNN grasp suggestion -> accept/restart -> movement -> release` 的离散交互链和 `100 ms / 350 ms / <250 ms / 600 ms / 1.4 s` 定时细节写得很清楚，可直接作为 `EFSM + T1` 假手控制样本。

## 条目 1: sEMG-triggered visual grasp-selection controller for a hybrid prosthetic hand
- 控制对象：带 embedded computer vision 的 hybrid 3D printed hand prosthesis 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 3D printed transradial prosthetic hand 的离散交互控制器，用 sEMG threshold pulse 触发拍照和 grasp-class proposal，再由用户 accept/restart 并最终 command movement 与 release。
- 判断：算。对象是真实 prosthetic hand controller，不是纯图像分类流程；原文同时保住了 grasp mode 集合、控制链、用户确认分支、release 返回链和局部定时。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-4 页，Sections `2.1 System Design` 与 `2.2 Control System`，行 159-199
> A new intelligent hybrid prosthesis model is proposed, commanded by a simple sEMG system aided by a fully embedded CV system. ... The system offers five modes: palmar grasp with the wrist in a neutral position and with the wrist pronated, tripod pinch, key grasp, and the index finger extension gesture.
>
> The Arduino system commands the start of image processing, opening, and closing of the prosthesis using servo motors, based on the user’s intention detected by the sEMG system and a finite state machine. The CV system is responsible for capturing the image of the object the user wants to grasp, and a CNN, running on the RPI3, classifies it according to the five hand posture patterns.

#### 摘录 B
- 出处：第 4 页，Section `2.2 Control System`，行 212-222
> The control system is expressed by a finite state machine ... For each suprathreshold muscle contraction, the control system receives an input pulse. A muscle contraction activates the laser point, so the user visually confirms the object to be picked up, photographs it, and starts the classification process by the CNN. The pattern chosen by the neural network is displayed on the LEDs on the back of the prosthesis. The user has two options: reject and restart the process or accept and command the movement. In the latter, another muscle contraction defines the object release, and the prosthesis returns to its initial condition.

#### 摘录 C
- 出处：第 4 页，Section `2.2 Control System`，行 223-229
> The total estimated time for this state machine to grasp the object since rest is `1.4 s`, excluding the time the user takes to accept the suggested grasp pattern. The estimated time for each sEMG pulse is `100 ms`, the laser point takes `350 ms`, the classification time since camera activation was less than `250 ms`, and the time for motor activation and movement was approximately `600 ms`.

#### 摘录 D
- 出处：第 4 页，Section `2.2 Control System`，行 208-211
> The Arduino Nano board, which makes the analog/digital conversion, has a sampling rate of `9,600` samples per second and `10` bits of resolution.

### 2. 基于原文整理后的自然语言描述

The hybrid 3D printed hand prosthesis uses an extended state-machine interaction loop in which an sEMG-driven Arduino front-end, an embedded camera-plus-CNN module, and the hand actuators are chained through discrete user-confirmed events rather than through continuous proportional grasp blending. At the mode level, the controller chooses among five output classes: `palmar grasp with neutral wrist`, `palmar grasp with pronated wrist`, `tripod pinch`, `key grasp`, and `index finger extension`. Every suprathreshold muscle pulse acts as an event trigger: the first pulse activates the laser pointer and image capture, the CNN classifies the target object and displays the suggested class on back LEDs, and the user then either rejects the proposal and restarts the sequence or accepts it and commands the prosthetic movement. After execution, a further muscle contraction explicitly commands object release and returns the prosthesis to its initial condition, so the interaction loop itself is part of the control semantics rather than a separate interface wrapper. The controller also preserves clear local timing semantics, with `9,600 Hz` and `10-bit` A/D acquisition, `100 ms` sEMG pulse handling, `350 ms` laser activation, `<250 ms` CNN classification, `~600 ms` motor movement, and an end-to-end rest-to-grasp time of `1.4 s`.

### 3. 逐句溯源

1. 句子 1：The hybrid 3D printed hand prosthesis uses an extended state-machine interaction loop in which an sEMG-driven Arduino front-end, an embedded camera-plus-CNN module, and the hand actuators are chained through discrete user-confirmed events rather than through continuous proportional grasp blending.
   对应摘录：A, B
2. 句子 2：At the mode level, the controller chooses among five output classes: `palmar grasp with neutral wrist`, `palmar grasp with pronated wrist`, `tripod pinch`, `key grasp`, and `index finger extension`.
   对应摘录：A
3. 句子 3：Every suprathreshold muscle pulse acts as an event trigger: the first pulse activates the laser pointer and image capture, the CNN classifies the target object and displays the suggested class on back LEDs, and the user then either rejects the proposal and restarts the sequence or accepts it and commands the prosthetic movement.
   对应摘录：B
4. 句子 4：After execution, a further muscle contraction explicitly commands object release and returns the prosthesis to its initial condition, so the interaction loop itself is part of the control semantics rather than a separate interface wrapper.
   对应摘录：B
5. 句子 5：The controller also preserves clear local timing semantics, with `9,600 Hz` and `10-bit` A/D acquisition, `100 ms` sEMG pulse handling, `350 ms` laser activation, `<250 ms` CNN classification, `~600 ms` motor movement, and an end-to-end rest-to-grasp time of `1.4 s`.
   对应摘录：C, D
