# A Digital Automatic Sliding Door with a Room Light Control System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把红外入/出传感、双单稳态定时、开门/关门继电器切换和房间人数计数链路写得很完整，可直接整理成带工程定时的自动门控制样本。

## 条目 1: Timed Beam-Break Open-Hold-Close Door Controller

- 控制对象：楼宇出入口场景中的自动滑门与房间照明联合控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向楼宇入口的自动滑门控制器，用红外对管、比较器、单稳态定时器、计数器、异或门和继电器来驱动开门、保持、反向关门与房间照明计数。
- 判断：算。对象是实际建筑机电控制系统，原文明确给出了输入传感、双定时量、门电机的开闭逻辑、传感器去重窗口以及房间人数计数链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5-6 页，`system principle`，`paper_content.txt` 第 200-221 行
> The system works on the principle of breaking an infrared beam ... The low output of the comparator is used to trigger a mono-stable multi-vibrator, which is connected to a D-flip-flop, AND gates, OR gates, up/down counter and the display.
>
> The output of the comparators also triggers two timers simultaneously, but both have different time constant. The first timer has a time constant of `5 s` while the second timer has a time constant of `10 s`. When the timers are triggered by breaking the beam, the first timer drives the transistor switch that controls the opening of the door. Hence, the door opens in `5 s`. ... after the first `5 s`, the output of the first timer is low, and the output of the second is still high ... so the EX-OR gate switches another relay that closes the door for `5 s`. The door is closed by reversing the polarity of the supply to the motor.

#### 摘录 B

- 出处：第 7-10 页，`Sensor Control Stage / Driver Control Stage`，`paper_content.txt` 第 302-365 行
> The mono-stable stage generates one shot of clocking pulse each time the sensor detects somebody entering the room. ... To deactivate the second sensor, the `10 seconds` mono-stable serves as an input to an OR gate ... then the second sensor is inactive for the ten seconds allowing someone to pass without affecting the count of the other up/down counter.
>
> This consists of a mono-stable multivibrator used to create a time constant which allows opening and closing of the door ... Two monostable stages are employed. The first opens the door, while the second closes the door. ... The `5 s` constant was fixed because it is estimated that it would take approximately `5 s` to walk through the door from the sensor in a worst case condition ... durations of `10 s` was chosen so that the remaining `5 s` would switch another relay which closes the door.

### 2. 基于原文整理后的自然语言描述

The sliding-door controller uses beam-break photodiode sensing to trigger a logic chain built from comparators, monostables, flip-flops, counters, logic gates, relays, and a DC motor driver. Once the infrared beam is broken, the controller starts two timers at the same time: a `5 s` timer that opens the door and a `10 s` timer that remains high long enough for an EX-OR gate to drive another relay and close the door for the next `5 s` by reversing motor polarity. The same design also disables the second sensor for `10 s` so that a single passage does not corrupt the up/down occupancy counter, and the room light stays on while the counter value is nonzero and turns off when the count returns to zero. The resulting control chain is a timed EFSM centered on `beam broken -> open for 5 s -> allow passage while second sensor is masked -> reverse polarity and close for 5 s`, with occupancy counting coupled to the same sensor events.

### 3. 逐句溯源

1. 句子 1：The sliding-door controller uses beam-break photodiode sensing to trigger a logic chain built from comparators, monostables, flip-flops, counters, logic gates, relays, and a DC motor driver.
   对应摘录：A
2. 句子 2：Once the infrared beam is broken, the controller starts two timers at the same time: a `5 s` timer that opens the door and a `10 s` timer that remains high long enough for an EX-OR gate to drive another relay and close the door for the next `5 s` by reversing motor polarity.
   对应摘录：A
3. 句子 3：The same design also disables the second sensor for `10 s` so that a single passage does not corrupt the up/down occupancy counter, and the room light stays on while the counter value is nonzero and turns off when the count returns to zero.
   对应摘录：A, B
4. 句子 4：The resulting control chain is a timed EFSM centered on `beam broken -> open for 5 s -> allow passage while second sensor is masked -> reverse polarity and close for 5 s`, with occupancy counting coupled to the same sensor events.
   对应摘录：A, B
