# Smart and adaptive traffic light system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 normal / pedestrian / busy / priority / maintenance 五类运行分支、按方向成对放行的基础循环、显式定时器、优先车辆抢占和恢复逻辑都写得很细，是道路交通信号方向很完整的双 A `HSM + T1` 样本。

## 条目 1: Adaptive Traffic-Light Mode and Priority Supervisor

- 控制对象：道路交通信号控制领域的自适应路口交通灯分层监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 Siemens CPU 1516-3 PN/DP 实现的四路口自适应交通灯控制器，上层在 normal、pedestrian、busy、priority 和 maintenance 分支间切换，下层按定时器推进具体灯色相位。
- 判断：算。对象是实际交通灯控制器，原文明确给出输入按钮/开关、相位时长、优先抢占、行人请求、密度扩时、停止后黄闪维护和恢复条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 23-25 页，`4.2 System description and programming / 4.3 Input data`，`paper_content.txt` 第 841-852 行、第 889-918 行
> In this system, a four-ways intersection with pedestrian crossing is taken into consideration. The system consists of a “start” operation push button, “stop” push button, and “pedestrian request” buttons. In addition, there are four switches for controlling the priority vehicle pass on each side of the junction, and another four switches for the vehicle density option.
>
> The inputs of the program while operating consist of: 1. Default signal time 2. Signal 1 to 4 busy cycle time 3. Pedestrian request 1 to 4 time 4. Yellow delay timer 5. Red delay timer.
>
> The four primary functions of this system include: normal flow, high-density flow, priority pass, and pedestrian crossing.

#### 摘录 B

- 出处：第 26-29 页，`4.4 Program functions`，`paper_content.txt` 第 944-998 行、第 1015-1059 行
> During normal flow, signal 1 and signal 3 prompts red lights to turn on for 3 seconds, 3 seconds for yellow lights ... and finally the green lights start for the time entered. ... The cycle then repeats itself in case of no interrupts such as pedestrian, busy mode or priority.
>
> At the end of the 6 seconds of yellow and red lights delay signaling the end of Signals 1 and 3, the pedestrian green light will set on for 10 seconds then change to red. Signals 2 and 4 can begin parallel with the pedestrian green light.
>
> If there is a busy traffic flow associated with Signal 1 ... vehicles can pass the intersection a little longer, i.e., in 15 seconds instead of 8 seconds.
>
> Since a vehicle with a priority pass is allowed to pass the intersection at any moment ... the yellow light should be on for one second in all directions followed by a green light in the direction of the oncoming priority vehicle, but red lights for all the other routes.
>
> As the traffic lights work continuously, the lights are featured with a maintenance option as the blinking yellow lights occurs. The yellow lights blink at a 1 second rate.

#### 摘录 C

- 出处：第 30-37 页，`5 SOFTWARE IMPLEMENTATION / 6 HMI VISUALIZATION AND SIMULATION`，`paper_content.txt` 第 1077-1121 行、第 1137-1171 行、第 1189-1252 行
> Since the normal traffic flow cycle is a series of events whereby the next outputs begin at the end of a preceding output cycle, the operation is controlled by the TON timer ... 12 timers are used (T1-T12) due to presence of 12 timer events.
>
> The pedestrian requests are only activated when the start condition is on and the priority mode is off. ... There will be a 3 seconds delay between the phase of red light turning green. After the request is done, the normal cycle will start after all the conditions in PED request 1 has been turned off.
>
> Presence of a busy traffic prompts an increase of the green light timer from e.g. 8 to 15 seconds ... if the vehicle count is zero, it means that no vehicles are coming from that direction and so the amount of time allocated to the green light equals 0 seconds.
>
> Assuming that the priority pass signal is originating from the Signal 1 direction, the yellow lights in all directions will flash for 1 second. ... Presence of a priority on any direction, prompts the program from normal cycle execution and jumps to the priority network with a predefined label Priority mode.
>
> The system initiates and starts working by pressing the start push button and stops in the blinking state when the stop push button is pressed.

### 2. 基于原文整理后的自然语言描述

The controller is a hierarchical traffic-signal supervisor whose normal state is a paired-lane signal cycle and whose interrupt branches handle pedestrian crossing, busy-traffic extension, priority-vehicle passage, and maintenance blinking. The PLC takes `START`, `STOP`, four pedestrian requests, four priority switches, and four density inputs, and it drives the full set of vehicle and pedestrian red, yellow, and green outputs for a four-way junction. In the normal cycle, signals `1` and `3` run together and then hand over to `2` and `4`, with `3 s` red and yellow delays, an `8 s` laboratory green interval, and a conflict-free overlap before the next branch becomes active. Pedestrian requests are only admitted when the system is started and priority mode is off, they wait until the current road cycle completes, and then give the selected crossing a timed green interval before normal execution resumes; busy mode extends green time from the normal cycle to `15 s` or higher according to density, while zero-count lanes can remain red. When a priority request arrives the PLC suspends normal and pedestrian operation, flashes all yellow lights for `1 s`, grants green only to the requesting direction, and resumes the paused cycle after the priority vehicle passes; when `STOP` is pressed the system falls back to maintenance mode with blinking yellow at a `1 s` rate.

### 3. 逐句溯源

1. 句子 1：The controller is a hierarchical traffic-signal supervisor whose normal state is a paired-lane signal cycle and whose interrupt branches handle pedestrian crossing, busy-traffic extension, priority-vehicle passage, and maintenance blinking.
   对应摘录：A, B
2. 句子 2：The PLC takes `START`, `STOP`, four pedestrian requests, four priority switches, and four density inputs, and it drives the full set of vehicle and pedestrian red, yellow, and green outputs for a four-way junction.
   对应摘录：A
3. 句子 3：In the normal cycle, signals `1` and `3` run together and then hand over to `2` and `4`, with `3 s` red and yellow delays, an `8 s` laboratory green interval, and a conflict-free overlap before the next branch becomes active.
   对应摘录：B
4. 句子 4：Pedestrian requests are only admitted when the system is started and priority mode is off, they wait until the current road cycle completes, and then give the selected crossing a timed green interval before normal execution resumes; busy mode extends green time from the normal cycle to `15 s` or higher according to density, while zero-count lanes can remain red.
   对应摘录：B, C
5. 句子 5：When a priority request arrives the PLC suspends normal and pedestrian operation, flashes all yellow lights for `1 s`, grants green only to the requesting direction, and resumes the paused cycle after the priority vehicle passes; when `STOP` is pressed the system falls back to maintenance mode with blinking yellow at a `1 s` rate.
   对应摘录：B, C
