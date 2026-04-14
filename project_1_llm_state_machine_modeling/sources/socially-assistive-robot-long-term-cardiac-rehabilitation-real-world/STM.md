# A Socially Assistive Robot for Long-Term Cardiac Rehabilitation in the Real World - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 cardiac rehabilitation 机器人在一整次训练会话中的鼓励、监测、在线反馈和医护告警链写成明确 FSM，并给出 `5 min / 7 min / 3 min` 的局部定时与生理阈值 guard。

## 条目 1: Rehabilitation-session monitoring and intervention robot

- 控制对象：医疗设备与生命支持控制领域的心脏康复训练会话监督机器人
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于门诊心脏康复训练的 socially assistive robot session supervisor，会在训练过程中周期性鼓励、持续监测并按心率/用力等级/姿态状态触发不同反馈与医护告警。
- 判断：算。对象是真实 cardiac-rehabilitation robot 的 monitoring module，不是一般实验流程；原文明确给出三状态交互结构、`5 min / 7 min / 3 min` 定时、心率与 Borg scale 阈值，以及触发医护介入的告警逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section `3.2 Robot Module`，`paper_content.txt` 第 382-398 行
> The Robot Module focuses on interaction with the user. This interaction is divided into three states: (1) Motivational support, (2) Performance monitoring, and (3) Online feedback.
>
> A session with the robot starts with an initial greeting, where the robot makes an announcement of the intensity that will be performed during the session ...
>
> Motivational support occurs periodically every 5 min during the session.

#### 摘录 B

- 出处：第 6 页，Figure 4 and monitoring logic，`paper_content.txt` 第 404-421 行
> Finite state machine presenting the different transitions possible during the monitoring phase.
>
> the Borg scale was requested every 7 min to ensure that the exertion level remains within the acceptable range.
>
> During this monitoring state, sensory information is analyzed. Depending on the values given by each sensor, the current state can activate the online feedback state or remain in the same state.
>
> we added a cooldown period of 3 min after feedback was provided to prevent the robot from repeating the same feedback too often.

#### 摘录 C

- 出处：第 6 页，heart-rate feedback，`paper_content.txt` 第 423-444 行
> This feedback is given by the robot when the heart rate exceeds the warning or critical thresholds.
>
> The warning threshold corresponds to the maximum of the determined healthy range ...
>
> If the patient is not feeling well, the robot alerts the medical staff verbally and non-verbally.
>
> The critical threshold corresponds to the maximum heart rate allowed for the patient ... calculated by the medical staff using the Karvonen formula ...
>
> the robot directly alerts the medical staff without confirmation from the patient.

#### 摘录 D

- 出处：第 6 页，exertion and posture feedback，`paper_content.txt` 第 445-460 行
> according to the value of the perceived exertion level, three types of robot behaviors are activated ...
>
> (1) If the Borg scale is on a normal range, the robot thanks the patient,
> (2) if the patient enters a critical Borg scale (above 12), but the current heart rate is in a healthy range, the robot asks for a confirmation ...
> (3) when both the Borg scale and the heart rate are critical, the robot alerts the medical staff.
>
> This feedback is given by the robot when the patient is not looking straight ... In this case, the robot gives verbal feedback to the patient, asking to maintain a straight posture.

### 2. 基于原文整理后的自然语言描述

The cardiac-rehabilitation robot uses a monitoring FSM in which a session progresses through `Motivational support`, `Performance monitoring`, and `Online feedback` rather than through a single repetitive coaching loop. At session start the robot announces the treadmill intensity, then during exercise it provides encouragement every `5 min` and requests Borg-scale input every `7 min` while the monitoring state continuously evaluates sensor values. Depending on sensor events, the machine activates targeted online feedback for high or critical heart rate, high exertion level, or incorrect cervical posture, and then enforces a `3 min` cooldown to prevent repeated alerts. Heart-rate feedback distinguishes a warning threshold from a critical threshold computed via the Karvonen formula, asks the patient for confirmation at warning level, and immediately calls medical staff once the critical limit is exceeded. The same supervisor also branches on Borg-scale input and posture deviation, either thanking the patient, requesting confirmation, or issuing direct corrective or medical-alert behaviors according to the combined physiological state.

### 3. 逐句溯源

1. 句子 1：The cardiac-rehabilitation robot uses a monitoring FSM in which a session progresses through `Motivational support`, `Performance monitoring`, and `Online feedback` rather than through a single repetitive coaching loop.
   对应摘录：A, B
2. 句子 2：At session start the robot announces the treadmill intensity, then during exercise it provides encouragement every `5 min` and requests Borg-scale input every `7 min` while the monitoring state continuously evaluates sensor values.
   对应摘录：A, B
3. 句子 3：Depending on sensor events, the machine activates targeted online feedback for high or critical heart rate, high exertion level, or incorrect cervical posture, and then enforces a `3 min` cooldown to prevent repeated alerts.
   对应摘录：B, D
4. 句子 4：Heart-rate feedback distinguishes a warning threshold from a critical threshold computed via the Karvonen formula, asks the patient for confirmation at warning level, and immediately calls medical staff once the critical limit is exceeded.
   对应摘录：C
5. 句子 5：The same supervisor also branches on Borg-scale input and posture deviation, either thanking the patient, requesting confirmation, or issuing direct corrective or medical-alert behaviors according to the combined physiological state.
   对应摘录：D
