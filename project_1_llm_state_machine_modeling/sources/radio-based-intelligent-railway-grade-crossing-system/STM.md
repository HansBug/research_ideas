# A Radio Based Intelligent Railway Grade Crossing System to Avoid Collision - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多轨道口控制器写成“传感器接收头/尾报文-CPU 判定-路信号/道口栏杆切换”的消息驱动流程，细节足够形成高质量铁路门控样本。

## 条目 1: Radio-Packet Multi-Track Grade-Crossing Gate Cycle

- 控制对象：多轨铁路道口的无线报文驱动门控与信号控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向多轨铁路平交道口的控制器，用列车头/尾无线报文、两侧传感器、CPU、道路/列车信号和半栏杆门协同完成道口关门与放行。
- 判断：算。对象是真实道口控制系统，不是纯通信方案；原文明确写出发包字段、传感器位置、CPU 内部变量、街道/列车信号状态和 gate open/close 逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 28-30 行
> This paper describes an intelligent railway crossing control system for multiple tracks that features a controller which receives messages from incoming and outgoing trains by sensors. These messages contain detail information including the direction and identity of a train. Depending on those messages the controller device decides whenever the railroad crossing gate will close or open.

#### 摘录 B

- 出处：第 2-3 页，`2. Design Pattern / 3. System Block`，`paper_content.txt` 第 56-68 行
> This automatic railway crossing gate uses radio link for identification, information of approaching and outgoing trains. The train has two transmitters at the beginning ... and end ... which transmit an identical packet that can be identified by the sensor. This packet transmitted through a radio link and received by sensor. Then the sensor sends the information of the packet to cpu ... where the controlling procedure is processed.
>
> ... After receiving the packet the cpu changes the signal & gate status from the packet type & algorithm stored in the cpu.
>
> ... When there is a train in the system it shuts the gate and opens it after leaving the system.

#### 摘录 C

- 出处：第 3-4 页，`4. Working Flow Diagram`，`paper_content.txt` 第 103-113 行
> The processing unit takes decision according to its own algorithm. ... sg_st and sg_tr mention street and train signal status respectively. Both street signal and train signal have two situations {g,r} ... g_s is the gate status and g_s in {o,c} for closing the gate it is c and for opening o.
>
> The packet has two information; train id (tr_id) and phase (d) of the train. Here, d in {h,t} it is h if the packet generate from head of the train otherwise it is t. Variable s indicates at which sensor the signal is acquired from.

### 2. 基于原文整理后的自然语言描述

The grade-crossing controller is organized as a message-driven EFSM in which each train carries two radio transmitters, one at the head and one at the tail, and each transmitted packet encodes both `train id` and `phase` information. Sensors placed on both sides of the crossing receive those packets and forward them to a central CPU, where the control procedure updates street-signal status, rail-signal status, gate status, and internal memory according to the packet type and the sensing side. When a train is recognized as being inside the protected crossing region, the controller shuts the half-barrier gate and changes the signal configuration so road traffic is blocked while rail traffic is allowed. When the tail packet indicates that the train has left the system, the same algorithm reopens the gate and restores the safe post-passage signal state. Because the logic explicitly distinguishes `g/r` signal states, `o/c` gate states, and `h/t` packet phases, the control chain is much richer than a simple fixed warning-time barrier.

### 3. 逐句溯源

1. 句子 1：The grade-crossing controller is organized as a message-driven EFSM in which each train carries two radio transmitters, one at the head and one at the tail, and each transmitted packet encodes both `train id` and `phase` information.
   对应摘录：A, B, C
2. 句子 2：Sensors placed on both sides of the crossing receive those packets and forward them to a central CPU, where the control procedure updates street-signal status, rail-signal status, gate status, and internal memory according to the packet type and the sensing side.
   对应摘录：B, C
3. 句子 3：When a train is recognized as being inside the protected crossing region, the controller shuts the half-barrier gate and changes the signal configuration so road traffic is blocked while rail traffic is allowed.
   对应摘录：B, C
4. 句子 4：When the tail packet indicates that the train has left the system, the same algorithm reopens the gate and restores the safe post-passage signal state.
   对应摘录：B, C
5. 句子 5：Because the logic explicitly distinguishes `g/r` signal states, `o/c` gate states, and `h/t` packet phases, the control chain is much richer than a simple fixed warning-time barrier.
   对应摘录：C
