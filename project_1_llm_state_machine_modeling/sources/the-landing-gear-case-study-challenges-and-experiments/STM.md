# The landing gear case study: challenges and experiments - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对起落架伸出/收回基本序列、飞行员手柄、指示灯和模拟开关行为都有清晰描述。

## 条目 1: Extend-retract sequencing and cockpit indication in the landing gear system
- 控制对象：飞机起落架及其数字控制软件
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G6 起落架 handle-门-起落架序列）

### 0. 条目识别与判定

- 一句话说明：这是航空起落架控制领域的 landing gear system，用于根据飞行员 Up/Down handle 指令协调门、起落架、液压与指示灯的伸放/回收过程。
- 判断：算。对象是实际飞机起落架控制系统，原文直接给出了 landing/retraction sequence、pilot interface、传感/灯光反馈以及模拟开关时序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，The landing gear case study: brief overview / Architecture of the system，对 basic sequence、手柄、灯光与 hydraulic control 的说明，行 87-149
> a basic landing sequence are: (1) open the doors of the landing gear boxes, (2) extend the landing gears and (3) close the doors. Similarly, after taking off, the corresponding basic retraction sequence to be performed are: (1) open the doors, (2) retract the landing gears and (3) close the doors. ... the pilot can interrupt each sequence at any time and at any point to start the opposite sequence as often as he/she wishes
>
> an Up/Down handle is provided to the pilot. When the handle is switched to “Up” the retracting landing gear sequence is executed, when the handle is switched to “Down” the extending landing gear sequence is executed.
>
> Three lights inform the pilot ... (1) one green light “gears are locked down”, (2) one orange light “gears manoeuvring”, (3) one red light “landing gear system failure”.
>
> The three doors (resp. gears) are controlled simultaneously by the same electro-valve. It is thus not possible to control the doors (resp. gears) separately.

#### 摘录 B
- 出处：第 4-5 页，Analogical switch / Electro-valves / Cylinders，对 analogical switch 与执行元件时间语义的说明，行 198-248
> The switch is closed each time the “Up/Down” handle is moved by the pilot, and it remains closed for 20 s. After this duration, the switch automatically becomes open.
>
> the transition from the two states closed and open takes a given amount of time: (1) 0.8 s from open to closed, and (2) 1.2 s from closed to open.
>
> when E rises from false to true ... the total duration of the transition phase is 1 s. In the same way, when E falls to false, the pressure goes down linearly from Hin to 0. The total duration of the pressure drop is 3.6 s.
>
> it is possible to stop and to inverse the motion of any cylinder at any time.

#### 摘录 C
- 出处：第 5 页，Expected scenarios in normal mode / Timing constraints，对 outgoing / retraction sequence 与 timing constraints 的说明，行 252-319
> When the gears are locked in retracted position, and the doors are locked in closed position, if the pilot sets the handle to “Down”, then the software should have the following sequence of actions:
> 1. stimulate the general electro-valve ...
> 2. stimulate the door opening electro-valve,
> 3. once the three doors are in the open position, stimulate the gear outgoing electro-valve,
> 4. once the three gears are locked down, stop the stimulation of the gear outgoing electro-valve,
> 5. stop the stimulation of the door opening electro-valve,
> 6. stimulate the door closure electro-valve,
> 7. once the three doors are locked in the closed position, stop the stimulation of the door closure electro-valve,
> 8. and finally stop stimulating the general electro-valve.
>
> When the gears are locked in down position, and the doors are locked in closed position, if the pilot sets the handle to “Up”, then the software should have the following sequence of actions ... once the three doors are in the open position, if the three shock absorbers are relaxed, then stimulate the gear retraction electro-valve ... else ... go to step 5
>
> The previous sequences can be interrupted by counter orders ... at any time. In that case, the scenario stops and restarts in the counter-sequence from the point where it was interrupted.
>
> First, stimulations of the general electro-valve and the manoeuvring electro-valve must be separated by at least 200 ms. Second, orders to stop the stimulation of the general electro-valve and the manoeuvring electro-valve must be separated by at least 1 s. And third, two contrary orders ... must be separated by at least 100 ms.

#### 摘录 D
- 出处：第 6 页，Requirements，对 monitoring constraints 的说明，行 354-386
> If one of the three doors is still seen locked in the closed (resp. open) position more than 7 s after stimulating the opening (resp. closure) electro-valve, then the red light “landing gear system failure” is on.
>
> If one of the three gears is not seen locked in the up (resp. down) position more than 10 s after stimulating the retraction (resp. outgoing) electro-valve, then the red light “landing gear system failure” is on.
>
> when the landing gear command handle has been DOWN (resp. UP) for 15 s, and if the gears are not locked down (resp. retracted) after 15 s, then the red light “landing gear system failure” is on.

### 2. 基于原文整理后的自然语言描述

The landing gear software executes two interruptible sequences. For a `Down` handle command with gears locked retracted and doors locked closed, it stimulates `general_EV`, opens the doors, stimulates gear outgoing once the three doors are open, stops gear outgoing once the three gears are locked down, stops door opening, closes the doors, stops door closure once all three doors are closed, and finally stops `general_EV`; the `Up` handle command mirrors this with gear retraction, except that retraction is allowed only if the three shock absorbers are relaxed. Either sequence may be interrupted at any time by the opposite handle order, and then the controller stops the current action and restarts the counter-sequence from the corresponding point, for example reopening the doors if an outgoing sequence is interrupted during door closure. The pilot observes green, orange, and red lights for locked-down, manoeuvring, and failure conditions, and every handle movement closes the analogical switch for 20 s, with 0.8 s open-to-closed and 1.2 s closed-to-open inertia, so the digital part can pass the order to the general electro-valve. The normal mode also imposes timing guards: `general_EV` and a manoeuvring electro-valve command must be at least 200 ms apart, stopping the manoeuvring and general electro-valves must be at least 1 s apart, contrary orders must be at least 100 ms apart, and prolonged door/gear mismatches or an unfinished sustained handle command raise the red failure light after the stated 7 s, 10 s, or 15 s thresholds.

### 3. 逐句溯源

1. 句子 1：The landing gear software executes two interruptible sequences. For a `Down` handle command with gears locked retracted and doors locked closed, it stimulates `general_EV`, opens the doors, stimulates gear outgoing once the three doors are open, stops gear outgoing once the three gears are locked down, stops door opening, closes the doors, stops door closure once all three doors are closed, and finally stops `general_EV`; the `Up` handle command mirrors this with gear retraction, except that retraction is allowed only if the three shock absorbers are relaxed.
   对应摘录：A, C
2. 句子 2：Either sequence may be interrupted at any time by the opposite handle order, and then the controller stops the current action and restarts the counter-sequence from the corresponding point, for example reopening the doors if an outgoing sequence is interrupted during door closure.
   对应摘录：A, C
3. 句子 3：The pilot observes green, orange, and red lights for locked-down, manoeuvring, and failure conditions, and every handle movement closes the analogical switch for 20 s, with 0.8 s open-to-closed and 1.2 s closed-to-open inertia, so the digital part can pass the order to the general electro-valve.
   对应摘录：A, B
4. 句子 4：The normal mode also imposes timing guards: `general_EV` and a manoeuvring electro-valve command must be at least 200 ms apart, stopping the manoeuvring and general electro-valves must be at least 1 s apart, contrary orders must be at least 100 ms apart, and prolonged door/gear mismatches or an unfinished sustained handle command raise the red failure light after the stated 7 s, 10 s, or 15 s thresholds.
   对应摘录：C, D
