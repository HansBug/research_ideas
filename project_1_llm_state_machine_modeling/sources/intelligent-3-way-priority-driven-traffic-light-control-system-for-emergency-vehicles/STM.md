# Intelligent 3-Way Priority-Driven Traffic Light Control System for Emergency Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了 RFID 检测、优先判定、放行绿灯和恢复常规灯序的完整应急优先控制链。

## 条目 1: RFID-Based Emergency Priority Sequence
- 控制对象：道路交通信号领域的三路口应急车辆优先控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G2 应急车辆交通灯优先）

### 0. 条目识别与判定
- 一句话说明：这是一个基于 RFID 的三路口交通灯控制器，用于在检测到应急车辆接近时为其分配优先级、开放绿灯并在车辆通过后恢复常规时序。
- 判断：算。对象是实际交通灯控制系统，原文直接给出了检测、赋权、绿灯放行和恢复正常序列的控制链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 27-38
> The purpose of the system was to facilitate the operation of a 3-way traffic control light and provide priority to emergency vehicles using a Radio Frequency Identification (RFID) sensor ... The implemented prototype utilizes RFID transmission, operates in conjunction with the sequential mode of traffic lights to alter the traffic light sequence accordingly and reverts the traffic lights back to their normal sequence after the emergency vehicle has passed the traffic lights.

#### 摘录 B
- 出处：第 3-4 页，system overview, 行 150-176
> Each emergency vehicle is equipped with an RFID tag that transmits a unique identifier. It provides the capability for priority detection when an emergency vehicle approaches an intersection. The RFID reader at the traffic light detects the RFID tag and identifies the vehicle as an emergency vehicle requiring priority access ... ensuring that the vehicle receives a green signal at the traffic light, allowing it to pass through the intersection without delay. ... The traffic light control unit modifies the signal timings and sequences in accordance with the priority-driven determinations made by the microcontroller. The system grants priority access to identified emergency vehicles by proactively altering the traffic light signals in their favor.

#### 摘录 C
- 出处：第 13-15 页，Phases of Simulation，行 290-307
> First Phase: Here, the normal system passed the two lanes of traffic to go and holds the other lane ... Second Phase: Here, the normal system passes one lane of traffic to go and holds two of the other lanes at ready state ... Third Phase: Here, the traffic light system stopped vehicles moving on one traffic lane and permitted two lanes to move ... Fourth Phase: Here, the RFID tag is placed at the front of the RFID reader to be able to change the normal traffic system through the ATMEGA324 microcontroller to an emergency system for a specific time ... Upon activation and pressing of the button, the LED lights undergo a transition to red, thereby halting the movement of all vehicles.

### 2. 基于原文整理后的自然语言描述

The three-way traffic-light controller cycles through normal traffic phases in which either two lanes pass and one is stopped, or one lane passes while the other lanes remain in ready/stop states. Each emergency vehicle carries an RFID tag, and when the tag is brought in front of the reader the microcontroller identifies the vehicle and switches from the normal sequence to an emergency mode for a specific time. In that emergency mode the controller halts regular traffic by driving the ordinary traffic LEDs to red so that the emergency route is cleared. After the emergency vehicle has passed, the controller returns the lights to their normal sequential mode.

### 3. 逐句溯源

1. 句子 1：The three-way traffic-light controller cycles through normal traffic phases in which either two lanes pass and one is stopped, or one lane passes while the other lanes remain in ready/stop states.
   对应摘录：C
2. 句子 2：Each emergency vehicle carries an RFID tag, and when the tag is brought in front of the reader the microcontroller identifies the vehicle and switches from the normal sequence to an emergency mode for a specific time.
   对应摘录：A, B, C
3. 句子 3：In that emergency mode the controller halts regular traffic by driving the ordinary traffic LEDs to red so that the emergency route is cleared.
   对应摘录：C
4. 句子 4：After the emergency vehicle has passed, the controller returns the lights to their normal sequential mode.
   对应摘录：A
