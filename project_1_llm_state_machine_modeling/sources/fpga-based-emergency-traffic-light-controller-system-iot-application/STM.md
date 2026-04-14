# FPGA - Based Emergency Traffic Light Controller System with IoT Application - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把路口 emergency-priority 交通灯实现成 “state machine + counter”，并给出了四种输入状态、黄灯 `3 s` 和红灯 `10 s` 的切换规则。

## 条目 1: Four-state emergency-priority TLC with IoT notification

- 控制对象：道路交通信号控制领域的 North-South / East-West 应急优先交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向救护车优先放行的双向路口交通灯控制器，用声音/图像传感器触发状态迁移，并用计数器实现黄灯和红灯延时后再把绿灯让给目标方向。
- 判断：算。对象是实际路口信号控制器，不是单纯 IoT 通知系统；原文明确给出了 state machine、counter、四种输入状态、NS/EW 输出编码以及应急放行后的恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，摘要与 `2. Background Study`，`paper_content.txt` 第 9-15、80-82 行
> This system was designed using FPGA with an IoT platform. Its give priority to emergency vehicles, especially ambulances at the traffic lights intersections ... Once the input is detected and the light turns green, the system will notify the ambulance driver using ESP8266 Wi-Fi Module ...
>
> The TLC involve two significant parts: (1) a state machine to maintain track of the present and next traffic state, (2) a counter to regulates transitions that occur from one vehicle state to another.

#### 摘录 B

- 出处：第 2-3 页，`3.2 Flow chart of the TLC system / Table 2`，`paper_content.txt` 第 82、90-92 行
> The process started when the two sensors placed at the traffic light intersection, which is audio (microphone) sensor and video (camera) sensor, detect an upcoming emergency vehicle at one of the junctions, either North to South or East to West.
>
> There are four states of possible input: (1) both input are at '0', (2) the video sensor is active '1', while the audio is not active '0', (3) the audio sensor is active '1', and the video sensor is '0' and (4) both sensors are detected as active '1'.
>
> ... the video sensor is at '1' and audio is at '0'. The traffics at NS will be GREEN while EW will be a delay at YELLOW ('010') for 3 seconds, then change to RED '100'. The delay sets for this project is 3 seconds for the YELLOW state and 10 seconds for the RED state.

#### 摘录 C

- 出处：第 4 页，`4.2 Hardware implementation with IoT / 5. Conclusion`，`paper_content.txt` 第 99-111 行
> Figure 9 shows C1 is at '0' and C2 at '1'. The LED on NS turns GREEN, and EW turns YELLOW for 3s delay, then turn to RED.
>
> ... Figure 11 shows the C1 is at '1' while C2 is also at '1'. The LED currently GREEN at NS and RED at EW.
>
> The traffic light becomes green until the ambulance passed by and subsequently recovers to its initial control flow.

### 2. 基于原文整理后的自然语言描述

The emergency-priority traffic light controller is implemented as a state machine plus counter architecture that supervises a two-way intersection with North-South and East-West directions. Its inputs are the video sensor `C1` and audio sensor `C2`, and the paper explicitly enumerates four sensor states: `00`, `01`, `10`, and `11`, which determine which direction should receive the emergency green corridor. In the no-emergency state `00`, the controller stays in its nominal signal pattern, while a detected emergency request causes the opposite direction to pass through a timed yellow handoff and then hold red so that the requested direction can turn green. The timed part is explicit: the yellow transition lasts about `3 s`, and the red hold is maintained for about `10 s` before the state machine settles into the emergency-priority pattern. When the ambulance has passed, the controller leaves the emergency state and returns to its initial traffic-light flow, while the current light state is simultaneously reported to the emergency driver through the IoT notification channel.

### 3. 逐句溯源

1. 句子 1：The emergency-priority traffic light controller is implemented as a state machine plus counter architecture that supervises a two-way intersection with North-South and East-West directions.
   对应摘录：A
2. 句子 2：Its inputs are the video sensor `C1` and audio sensor `C2`, and the paper explicitly enumerates four sensor states: `00`, `01`, `10`, and `11`, which determine which direction should receive the emergency green corridor.
   对应摘录：B
3. 句子 3：In the no-emergency state `00`, the controller stays in its nominal signal pattern, while a detected emergency request causes the opposite direction to pass through a timed yellow handoff and then hold red so that the requested direction can turn green.
   对应摘录：B, C
4. 句子 4：The timed part is explicit: the yellow transition lasts about `3 s`, and the red hold is maintained for about `10 s` before the state machine settles into the emergency-priority pattern.
   对应摘录：B, C
5. 句子 5：When the ambulance has passed, the controller leaves the emergency state and returns to its initial traffic-light flow, while the current light state is simultaneously reported to the emergency driver through the IoT notification channel.
   对应摘录：A, C
