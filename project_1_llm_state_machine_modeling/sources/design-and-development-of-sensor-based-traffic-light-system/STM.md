# Design and Development of Sensor Based Traffic Light System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然篇幅不长，但把单灯三状态、双向同步、基于三只红外传感器的配时计算、`8/16/24 s` 绿灯倒计时与 `2 s + 1 s` 相位切换链写得足够完整。

## 条目 1: Queue-sensitive four-way traffic-light supervisor

- 控制对象：道路交通信号控制领域的四向路口传感交通灯监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个根据各车道传感器触发数量动态分配绿灯持续时间、并按顺时针轮转四个方向的交通灯相位监督器。
- 判断：算。对象是实际 traffic signal simulator/controller，不是单纯 GUI 或硬件连接说明；原文明确给出 `Red / Yellow / Green` 三状态、paired-output 组合、倒计时触发输入、三档传感配时和 `North -> East -> South -> West` 的相位顺序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Implementation，`paper_content.txt` 第 176-197 行
> A single 3-lamp traffic light is considered as a finite state machine. It has three states, Red, Yellow, and Green, which are also the outputs.
>
> This input is connected to the output of a countdown timer, which outputs a 1 when it reaches zero.
>
> ... one pair of lights was used to control traffic in the north-south direction, while the other pair controls the east-west direction.
>
> Thus there are 3 × 3 = 9 possible outputs. Each combined output describes the color of the north-south light along with the color of the east-west light.

#### 摘录 B

- 出处：第 3 页，queue-based timing model，`paper_content.txt` 第 198-225 行
> mathematical functions that can calculate the time needed for the green signal to illuminate based on the length of queue are developed.
>
> The length of queue is detected through the infrared object detectors by the presence of vehicles.
>
> ... z is a variable, which gives two values only: 0 when there is no sensor triggered and 1 if there is at least one sensor triggered ...
>
> t1 is the value of the first time delay in (s), tn equals to the number of sensors triggered, and t2 is the second time delay for each lane in (s).

#### 摘录 C

- 出处：第 3-4 页，implementation and phase switching，`paper_content.txt` 第 232-250 行
> In each lane, three infrared object detectors have been installed.
>
> The total number of sensors triggered will be used in the mathematical function to calculate the appropriate timing for the green signal to illuminate.
>
> After the green signal finishes the illumination timing, the yellow signal will illuminate for 2 seconds and then finally the red signal will illuminate. After that, the traffic signal will wait for 1 second before it goes to the next lane condition.

#### 摘录 D

- 出处：第 4 页，results and countdown cases，`paper_content.txt` 第 255-325 行
> The traffic signal operation will start by the traffic lights illuminating in red for 1 second in all directions. Then the traffic signals will start illuminating in the clockwise direction ... North lane, then East lane, then South lane, then West lane ...
>
> when one sensor is activated, Counter 1 will start counting down ... from 8 seconds to zero.
>
> If two sensors are triggered ... Counter 2 ... will start counting down from 16 seconds ...
>
> three sensors triggered by the vehicles ... will count down from 24 seconds to zero.
>
> If there are no vehicles on the road in all four directions, then the lights will change from green to yellow in 2 seconds and from yellow to red in another 2 seconds.

### 2. 基于原文整理后的自然语言描述

The sensor-based traffic controller starts from a simple three-state FSM for a single lamp with `Red`, `Yellow`, and `Green` outputs, triggered by a countdown-timer input that requests a state change when it reaches zero. At the intersection level, the controller synchronizes north-south and east-west lamp pairs and treats the combined signal as one of `3 × 3 = 9` possible paired outputs. Green duration is not fixed, because each lane has three infrared sensors and the controller computes queue-dependent green time from the number of triggered sensors and the inter-sensor motion model. After each green phase, the controller holds yellow for `2 s`, then red, and waits `1 s` before moving to the next lane in the clockwise sequence `North -> East -> South -> West`. In the implemented cases, one triggered sensor yields an `8 s` countdown, two sensors yield `16 s`, and three sensors yield `24 s`, while the no-vehicle case falls back to a short `2 s` green-to-yellow and another `2 s` yellow-to-red transition.

### 3. 逐句溯源

1. 句子 1：The sensor-based traffic controller starts from a simple three-state FSM for a single lamp with `Red`, `Yellow`, and `Green` outputs, triggered by a countdown-timer input that requests a state change when it reaches zero.
   对应摘录：A
2. 句子 2：At the intersection level, the controller synchronizes north-south and east-west lamp pairs and treats the combined signal as one of `3 × 3 = 9` possible paired outputs.
   对应摘录：A
3. 句子 3：Green duration is not fixed, because each lane has three infrared sensors and the controller computes queue-dependent green time from the number of triggered sensors and the inter-sensor motion model.
   对应摘录：B, C
4. 句子 4：After each green phase, the controller holds yellow for `2 s`, then red, and waits `1 s` before moving to the next lane in the clockwise sequence `North -> East -> South -> West`.
   对应摘录：C, D
5. 句子 5：In the implemented cases, one triggered sensor yields an `8 s` countdown, two sensors yield `16 s`, and three sensors yield `24 s`, while the no-vehicle case falls back to a short `2 s` green-to-yellow and another `2 s` yellow-to-red transition.
   对应摘录：D
