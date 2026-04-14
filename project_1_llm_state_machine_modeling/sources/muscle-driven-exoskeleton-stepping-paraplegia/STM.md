# A muscle-driven approach to restore stepping with an exoskeleton for individuals with paraplegia - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `sitting / sit-to-stand / standing / stepping / stand-to-sit` 顶层控制，加上 `double stance / early swing / late swing / weight acceptance` 步态子状态和 timeout 安全回退，可直接作为高质量下肢外骨骼 `HSM` 样本。

## 条目 1: Hierarchical HNP supervisor with stepping submachine and timeout recovery
- 控制对象：面向截瘫患者的肌肉驱动混合神经假体/外骨骼 (`HNP`) 步行监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把神经刺激、液压关节约束和 gait event detector 组合起来的分层外骨骼控制器，用顶层功能态和步态子状态共同驱动站起、步行和坐下。
- 判断：算。对象是真实下肢外骨骼/神经假体控制器，不是实验协议；原文明确写出顶层功能切换、步行子状态、阈值 guard、按钮触发和 timeout 回退机制。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Methods
> An onboard controller processed exoskeleton sensor signals, determined appropriate exoskeletal constraints and stimulation commands for a finite state machine (FSM), and transmitted data over Bluetooth to an off-board computer for real-time monitoring and data recording.
>
> The FSM coordinated stimulation and exoskeletal constraints to enable functions, selected with a wireless finger switch user interface, for standing up, standing, stepping, or sitting down.
>
> In the stepping function, the FSM used a sensor-based gait event detector to determine transitions between gait phases of double stance, early swing, late swing, and weight acceptance.

#### 摘录 B
- 出处：第 5-6 页，Section `Software control system`
> The closed-loop FSM controller used the information from the sensors to output the appropriate neural stimulation and set hydraulic joint constraints. High-level control of the FSM defined the functions of the hydraulic system and pre-programmed stimulation patterns for the sit-to-stand, standing, stepping, and stand-to-sit functions ...
>
> The high-level control transitioned between the different functions of sitting, sit-to-stand, standing, stepping, and stand-to-sit ... The transitions were initiated by pressing different buttons on the wireless finger switch.
>
> The sit-to-stand function was initiated by pressing the “go” button which uncoupled the hips, unlocked the knee joints, and maximally activated hip and knee extensor muscles ...
>
> The stand-to-sit function was activated by pressing the “stop” button that unlocked all joints and ramped down the stimulation to the hip and knee extensor muscles.

#### 摘录 C
- 出处：第 6-7 页，Section `Software control system` / Figure `5`
> After entering the stepping function, the controller alternated between left and right steps. A gait event detector (GED) identified appropriate transitions between phases in the stepping function of the FSM ...
>
> The GED determined transitions between double stance (before left swing), left early swing, left late swing, left weight acceptance, double stance (before right swing), right early swing, right late swing, and right weight acceptance phases of gait ...
>
> During left early swing phase, the right (contralateral) knee was locked and the left (ipsilateral) knee was unlocked, and vice versa during right early swing phase. Double stance phase was characterized by both ipsilateral and contralateral heels/forefoot being in contact with the ground.
>
> Transition between early swing and late swing occurred when the ipsilateral hip joint angle exceeded a predetermined hip flexion angle threshold ... Transition between late swing and weight acceptance occurred when the ipsilateral knee joint angle reached extension ... Before the user could initiate the next step, the ipsilateral heel FSR signal had to exceed the set weight acceptance threshold.

#### 摘录 D
- 出处：第 7 页，Section `Software control system`
> Timeout phases were incorporated into the FSM for safety. The FSM transitioned to the timeout phases if the hip or knee angle thresholds during swing were not achieved within a prescribed time determined by the lengths of the pre-programmed stepping stimulation pattern.
>
> In the timeout phase, the exoskeleton returned to default reciprocally coupled hips and locked knees while maximally activating the hip and knee extensor muscles.

### 2. 基于原文整理后的自然语言描述

The untethered HNP controller is organized hierarchically: a high-level FSM switches among `sitting`, `sit-to-stand`, `standing`, `stepping`, and `stand-to-sit`, while a stepping submachine coordinates the detailed gait phases. A wireless finger switch drives the top-level transitions, so `sit-to-stand` uncouples the hips, unlocks the knees, and maximally activates hip and knee extensors, whereas `stand-to-sit` unlocks all joints and ramps extensor stimulation down. Inside `stepping`, a gait event detector cycles through `double stance`, `early swing`, `late swing`, and `weight acceptance` for each leg, locking the contralateral knee during swing and using hip-angle, knee-extension, and heel-FSR thresholds to advance the phase sequence. The controller therefore alternates left and right steps through a threshold-gated substate machine rather than a fixed open-loop sequence. For safety, timeout states are built into the machine so that if swing thresholds are not achieved within the prescribed stimulation timing, the exoskeleton falls back to reciprocally coupled hips, locked knees, and maximal extensor stimulation.

### 3. 逐句溯源

1. 句子 1：The untethered HNP controller is organized hierarchically: a high-level FSM switches among `sitting`, `sit-to-stand`, `standing`, `stepping`, and `stand-to-sit`, while a stepping submachine coordinates the detailed gait phases.
   对应摘录：A, B
2. 句子 2：A wireless finger switch drives the top-level transitions, so `sit-to-stand` uncouples the hips, unlocks the knees, and maximally activates hip and knee extensors, whereas `stand-to-sit` unlocks all joints and ramps extensor stimulation down.
   对应摘录：B
3. 句子 3：Inside `stepping`, a gait event detector cycles through `double stance`, `early swing`, `late swing`, and `weight acceptance` for each leg, locking the contralateral knee during swing and using hip-angle, knee-extension, and heel-FSR thresholds to advance the phase sequence.
   对应摘录：A, C
4. 句子 4：The controller therefore alternates left and right steps through a threshold-gated substate machine rather than a fixed open-loop sequence.
   对应摘录：C
5. 句子 5：For safety, timeout states are built into the machine so that if swing thresholds are not achieved within the prescribed stimulation timing, the exoskeleton falls back to reciprocally coupled hips, locked knees, and maximal extensor stimulation.
   对应摘录：D
