# Cognitive vision system for control of dexterous prosthetic hands: Experimental evaluation - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出 `user EMG -> CVS high-level controller -> CyberHand low-level controller` 的完整层次链，同时明确 `open / close` 主状态、`9` 种 grasp modality、固定阈值规则、`2 kHz` 采样、`100 ms` EMG 窗口与 `3 s` 回 idle 延迟，是非常完整的 `HSM + T1` 假手控制样本。

## 条目 1: Hierarchical vision-guided prehension controller for the CyberHand prosthesis
- 控制对象：CyberHand 多指假手的 vision-guided prehension 监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向多指 dexterous prosthetic hand 的层次控制器，用 EMG 触发主状态流，再由视觉规则自动选择抓型与开口，最后由嵌入式低层位置/力控制执行 preshape 与 grasp。
- 判断：算。对象是真实假手控制系统；原文同时给出层次结构、主状态序列、视觉规则阈值、抓型集合、低层执行接口和延迟语义，不是单纯的图像识别或实验流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Control system architecture，行 120-136，201-212
> It is a hierarchical structure, in which the overall control task is shared between the user, a high-level controller and a low-level embedded controller.
>
> The user issues commands for hand opening and closing via a simple EMG interface and also controls the orientation of the hand during grasping and manipulation.
>
> The high-level controller comprises: 1) the CVS estimating object properties (size, shape) and automatically selecting grasp type and aperture size appropriate for grasping the object; and 2) a hand controller translating the selected grasp into a set of desired finger positions (for hand preshaping) and forces (for hand grasping) that are sent to a low-level controller.
>
> The low-level controller embedded into the CyberHand prototype implements closed-loop position and force control during hand preshaping and grasping, respectively.
>
> It includes commands for setting the finger positions in the range from 0 (fully open) to 100% (fully flexed) and tendon forces in the range from 0 (no force) to 100% (maximal force ~140 N).

#### 摘录 B
- 出处：第 4-6 页，CVS algorithm and rule set，行 243-249，269-283，344-347
> The PC runs a control application implementing a finite state machine that triggers the following modules: the myoelectric control module, the CVS algorithm and the hand control module.
>
> The CVS algorithm estimates the size of the target object and uses a set of simple IF-THEN rules to select the grasp type and aperture size appropriate to grasp the object.
>
> These rules are constructed so that four different grasp types can be chosen: palmar, lateral, 3-digit and 2-digit (pinch) grasps.
>
> Palmar and lateral grasps are available in three different aperture sizes (small, medium, and large) while the 3-digit grasp has two available sizes. Therefore, there are nine possible grasp modalities in total.
>
> The thresholds are defined relative to the hand size and the size of the maximal aperture when the hand is preshaped according to a given grasp type. For example, TLARGE = 90% PW, TTHIN = 70% MLA, TWIDE = 50% MPA, and TVERYWIDE = 65% MPA.

#### 摘录 C
- 出处：第 6-7 页，Hand control and myoelectric interface，行 319-345，357-365
> The task of this module is to send the proper HLHC commands to the hand in order to preshape or close the hand according to the output of the CVS.
>
> A lookup table with the preshaping positions and tendon force values (for stable grasps) that should be assumed by each finger in each grasp was built.
>
> The myoelectric control module simply thresholds the EMG inputs in the following manner: raw EMG signals are sampled at 2 kHz, and the mean absolute value (MAV) is calculated over 100-ms overlapping time windows.
>
> The MAVs of both channels are then thresholded using individually adjustable levels, and a two-bit binary code is generated. The binary code is input for the application's state machine.

#### 摘录 D
- 出处：第 7 页，Finite state machine sequence，行 357-375
> 1) The starting, idle state is where the robotic hand is in a neutral posture (i.e., all fingers 60% flexed).
>
> 2) ... activate his/her finger extensor muscles. The recognized EMG activity that is larger than the preset threshold starts the CVS algorithm for the estimation of the pointed object size and selection of the appropriate grasp type and aperture size.
>
> 3) Once the size and grasp type are selected, the hand control module commands finger extension, thereby providing preshaping.
>
> 4) ... commanding its closure by activating his/her finger flexors. The artificial hand grasps the object by using force control to flex the involved fingers.
>
> 5) The object is held until the subject contracts his/her finger extensor muscles, thereby triggering the opening of the hand and releasing of the object.
>
> 6) The final phase is the return to the idle state (after a three-second delay).

### 2. 基于原文整理后的自然语言描述

The CyberHand controller is a hierarchical state machine in which the user only triggers the high-level sequence with flexor and extensor EMG, while the vision module and the embedded hand controller refine that sequence into object-specific preshaping and grasp execution. At the high level, the PC runs an FSM whose EMG-driven main flow is `idle -> vision-based grasp selection -> preshaping -> force-controlled closure -> hold -> release -> idle`, and the hand returns to idle only after a `3 s` delay. Inside that flow, the CVS computes object size from camera and distance-sensor measurements, aggregates ten consecutive estimates with a median, and applies fixed IF-THEN thresholds such as `TLARGE = 90% PW`, `TTHIN = 70% MLA`, `TWIDE = 50% MPA`, and `TVERYWIDE = 65% MPA` to choose one of `9` grasp modalities spanning palmar, lateral, 3-digit and 2-digit pinch families. The selected grasp is converted by the hand control module into finger position and tendon-force commands, while the embedded HLHC/LLMC layer closes the loop with position control for preshaping and force control for final grasping, over interfaces that span `0-100%` finger position and `0-140 N` tendon-force scaling. Because the paper preserves both the top-level discrete sequence and the lower-level execution interface, it is a rich `HSM + T1` sample rather than a generic vision-for-grasping article.

### 3. 逐句溯源

1. 句子 1：The CyberHand controller is a hierarchical state machine in which the user only triggers the high-level sequence with flexor and extensor EMG, while the vision module and the embedded hand controller refine that sequence into object-specific preshaping and grasp execution.
   对应摘录：A, B, C
2. 句子 2：At the high level, the PC runs an FSM whose EMG-driven main flow is `idle -> vision-based grasp selection -> preshaping -> force-controlled closure -> hold -> release -> idle`, and the hand returns to idle only after a `3 s` delay.
   对应摘录：D
3. 句子 3：Inside that flow, the CVS computes object size from camera and distance-sensor measurements, aggregates ten consecutive estimates with a median, and applies fixed IF-THEN thresholds such as `TLARGE = 90% PW`, `TTHIN = 70% MLA`, `TWIDE = 50% MPA`, and `TVERYWIDE = 65% MPA` to choose one of `9` grasp modalities spanning palmar, lateral, 3-digit and 2-digit pinch families.
   对应摘录：B
4. 句子 4：The selected grasp is converted by the hand control module into finger position and tendon-force commands, while the embedded HLHC/LLMC layer closes the loop with position control for preshaping and force control for final grasping, over interfaces that span `0-100%` finger position and `0-140 N` tendon-force scaling.
   对应摘录：A, C
5. 句子 5：Because the paper preserves both the top-level discrete sequence and the lower-level execution interface, it is a rich `HSM + T1` sample rather than a generic vision-for-grasping article.
   对应摘录：A, B, D
