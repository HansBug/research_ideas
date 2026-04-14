# Human-in-the-loop layered architecture for control of a wearable ankle-foot robot - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把踝足可穿戴机器人写成高层识别 + 中层 FSM + 低层 PID 的分层控制架构，给出了 `assistive / hold / release` 三模、事件触发切换与实时功率/位置反馈，是完整的辅助行走控制样本。

## 条目 1: Gait-synchronized ankle-foot assist controller

- 控制对象：基于步态事件识别的踝足可穿戴辅助机器人中层控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是步态辅助机器人中的中层离散控制器，用 `toe-off / hold / heel-contact` 状态驱动脚部抬升、保持和释放。
- 判断：算。对象是真实可穿戴机器人里的控制核心，原文不仅说明用了 FSM，还把状态、输出值、切换逻辑、提前打断规则和实时实验反馈都写清楚了。

### 1. 原文摘录

#### 摘录 A

- 出处：Abstract，`paper_content.txt` 第 26-38 行
> The proposed control architecture is composed of high-, mid- and low-level computational and control layers ... The mid-level layer implements a Finite State Machine (FSM) ... The low-level layer is responsible for the precise control ... The assistance is applied lifting up the human foot when the toe-off event is detected ... and the assistance is removed ... when the heel-contact event is detected.

#### 摘录 B

- 出处：Section 3.4，`paper_content.txt` 第 390-434 行
> the wearable robot need[s] to be in ‘assistive’, ‘hold’ or ‘release’ mode ... The transition ... is controlled by the ‘toe-off’, ‘hold’ and ‘heel-contact’ states in a FSM ... The output ... takes one of three values: -1, 0 and 1 ... When the toe-off event is recognised ... the FSM enters the ‘toe-off’ state ... Then, the FSM enters the ‘hold’ state ... Once the high-level layer predicts the heel-contact event ... sends a negative speed signal ... This causes a downward movement ... The state machine does not simply follow a predefined procedure ... if the current robot state is ‘release’ ... and the high-level layer detects the toe-off event before the loose position is reached, then ... immediately enter[s] the ‘toe-off’ state.

#### 摘录 C

- 出处：Real-time validation，`paper_content.txt` 第 648-665 行，第 711-720 行
> The output signal is used to set the control parameters and next state ... The signals from the mid-level layer are -1, 0 and 1, which represent the ‘release’, ‘hold’ and ‘assistive’ states ... These signals prepare the robot to lift up ... and move downwards ... the robot keeps the foot up ... before the heel contact event is detected ... When the toe-off event was detected, the wearable robot entered the ‘assistive’ mode ... Once the foot is at the target upper position, there was a short period of time where the foot was steady (‘hold’ mode) ... When the heel contact was detected, the robot entered to the ‘release’ mode.

### 2. 基于原文整理后的自然语言描述

The wearable ankle-foot robot is controlled by a human-in-the-loop layered architecture in which a high-level gait recognizer feeds a mid-level finite-state machine and a low-level cascade PID controller. The mid-level FSM decides whether the robot should be in `assistive`, `hold`, or `release` mode by entering the `toe-off`, `hold`, and `heel-contact` states, and it converts those states into `1`, `0`, and `-1` speed commands for the motors. When toe-off is recognized, the controller lifts the foot until the target position is reached and then holds it; when heel contact is recognized, it commands a negative speed to release the foot toward a loose position, while still allowing immediate early switching if the recognized gait event contradicts the current robot state. Real-time experiments show the corresponding `assist / hold / release` command sequence, motor-angle feedback, and power peaks while the robot repeatedly lifts and lowers the user's foot during walking.

### 3. 逐句溯源

1. 句子 1：The wearable ankle-foot robot is controlled by a human-in-the-loop layered architecture in which a high-level gait recognizer feeds a mid-level finite-state machine and a low-level cascade PID controller.
   对应摘录：A
2. 句子 2：The mid-level FSM decides whether the robot should be in `assistive`, `hold`, or `release` mode by entering the `toe-off`, `hold`, and `heel-contact` states, and it converts those states into `1`, `0`, and `-1` speed commands for the motors.
   对应摘录：B
3. 句子 3：When toe-off is recognized, the controller lifts the foot until the target position is reached and then holds it; when heel contact is recognized, it commands a negative speed to release the foot toward a loose position, while still allowing immediate early switching if the recognized gait event contradicts the current robot state.
   对应摘录：B
4. 句子 4：Real-time experiments show the corresponding `assist / hold / release` command sequence, motor-angle feedback, and power peaks while the robot repeatedly lifts and lowers the user's foot during walking.
   对应摘录：C
