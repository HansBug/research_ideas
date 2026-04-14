# A Prosthetic Hand Body Area Controller Based on Efficient Pattern Recognition Control Strategies - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不只给了 gesture classifier，还把 prosthetic hand 的 reset-based FSM、`100 ms` spike filter、`20` 次投票窗口和 motor-current feedback actuation 写成了完整控制闭环。

## 条目 1: Reset-based gesture execution controller for the prosthetic hand
- 控制对象：多指假手的实时手势识别与执行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个假手控制器，它把 `ADC acquisition -> spike removal -> SVM voting -> gesture config -> decontraction retrigger` 组织成一个带 reset 位置约束的有限状态控制链。
- 判断：算。对象是真实 prosthetic hand controller，不是单纯离线分类算法；原文明确给出控制状态、触发阈值、局部时间窗口和状态相关执行动作。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section `3`
> The proposed solution integrates sample-level SVM classification with a high-level Finite State Machine (FSM) to produce accurate and robust control of the prosthesis. For mechanical constraints, the prosthetic hands start every gesture from a reset position, i.e., open hand ... during the onset of a gesture, the output of the sample-level recognition is analyzed with a majority voting approach to limit the errors due to the signal transitions and to converge to a decision within a specified time window.

#### 摘录 B
- 出处：第 9-10 页，Section `3.5 Control Strategy`
> Prosthetic hands execute the various grasps and movements starting always from a reset state ... The Spike Removal block acts as a time trigger ... spikes ... for less than 100 ms are filtered ... a natural interaction with the device requires response times below 300 ms ... our system applies the majority voting on 20 consecutive SVM classifications to select the most likely gesture being performed.

#### 摘录 C
- 出处：第 10 页，Section `3.5 Control Strategy`
> In the power grasp all the motors receive the command to rotate closing the fingers, while in the precision grasp only index and thumb fingers receive the closing command. The MCU stops the motors exploiting the H-bridge current feedback ... Once a gesture is decoded and actuated, the EMG contraction level is acquired again, waiting for a muscular decontraction, that retriggers the FSM controller.

### 2. 基于原文整理后的自然语言描述

The prosthetic hand controller is built around a reset-based finite-state control loop in which every new gesture starts from the known `open hand` configuration. Incoming EMG samples are first stabilized by a spike-removal stage that suppresses contraction bursts shorter than `100 ms`, after which the embedded classifier performs majority voting over `20` consecutive SVM decisions so the hand can respond within a sub-`300 ms` interaction window while still rejecting transient onset errors. Once a gesture is accepted, the gesture-configuration state sends state-specific motor commands: a `power grasp` closes all fingers, whereas a `precision grasp` closes only the thumb and index. Finger motion stops through motor-current feedback from the H-bridge rather than through external position sensors, so the controller can infer when a finger has reached the intended position or encountered an object. After actuation, the FSM waits for muscular decontraction, uses that event to retrigger the controller, and routes the hand back through the reset/open-hand transition before permitting the next gesture.

### 3. 逐句溯源

1. 句子 1：The prosthetic hand controller is built around a reset-based finite-state control loop in which every new gesture starts from the known `open hand` configuration.
   对应摘录：A, B
2. 句子 2：Incoming EMG samples are first stabilized by a spike-removal stage that suppresses contraction bursts shorter than `100 ms`, after which the embedded classifier performs majority voting over `20` consecutive SVM decisions so the hand can respond within a sub-`300 ms` interaction window while still rejecting transient onset errors.
   对应摘录：B
3. 句子 3：Once a gesture is accepted, the gesture-configuration state sends state-specific motor commands: a `power grasp` closes all fingers, whereas a `precision grasp` closes only the thumb and index.
   对应摘录：C
4. 句子 4：Finger motion stops through motor-current feedback from the H-bridge rather than through external position sensors, so the controller can infer when a finger has reached the intended position or encountered an object.
   对应摘录：C
5. 句子 5：After actuation, the FSM waits for muscular decontraction, uses that event to retrigger the controller, and routes the hand back through the reset/open-hand transition before permitting the next gesture.
   对应摘录：A, C
