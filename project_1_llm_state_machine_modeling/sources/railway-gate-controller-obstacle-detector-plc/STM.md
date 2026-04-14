# PLC Based Automatic Railway Gate Controller and Obstacle Detector - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路平交口 arrival / obstacle / departure 触发、闸门开闭与列车停车联锁写成了完整 PLC 事件链，并给出输入输出地址。

## 条目 1: Arrival-obstacle-departure crossing controller with train-stop interlock

- 控制对象：铁路与轨道交通设备控制领域的平交口闸门与障碍物联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Allen-Bradley PLC 的铁路道口门控控制器，使用列车位置开关和障碍物检测开关协调列车运行、闸门关闭、闸门重新开启和列车停车/恢复。
- 判断：算。对象是具体铁路道口控制器，原文直接给出列车到达、闸门关闭、障碍停车、离站后延时抬杆以及输入输出地址，不是抽象 signalling 介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 41-50 行
> This paper provides an automatic railway crossing gate replacing the gates operated by the workers. In this work, an automatic railway crossing gate control system has been developed using a Programmable Logic Controller (PLC). Signaling light models are implemented using several red, green and yellow Light Emitting Diodes (LEDs); and railway gates are opened using DC motors with gear trains that are connected to the output ports of the PLC.

#### 摘录 B

- 出处：第 2-3 页，Figure 2 说明，`paper_content.txt` 第 76-79、114-123 行
> This energizes the motor in the forward direction which is coupled to the gate assembly and closes the gate without manual control.
>
> The obstacle detector senses any obstacle present on the level crossing and gives the signal to PLC. If any obstacle is present on the track then PLC will send stop command to geared DC motors which are used as wheels of the train. Once the obstacle is removed from the track then PLC will send run command to geared DC motors.
>
> If the train is closer to the level crossing, PLC activates its output and sends the close command through a relay to DC motors which are coupled to the railway gate assembly. Once the train crosses the leveler, PLC activates its output to open the gate automatically after some delay.

#### 摘录 C

- 出处：第 3-4 页，Hardware Specifications / Table 2，`paper_content.txt` 第 153-158、175-193 行
> Limit switches are used to detect the obstacle and position of the train. These switches work as the system input to inform the programmable logic controller (PLC) regarding the current situation of the system (train position).
>
> When the train reaches at position switch 5, the switch gets pressed. The signal goes to the PLC and according to the PLC programming gates closed. When the train reaches at position switch 1, the switch gets pressed, in step with the PLC programming gates opened.
>
> Train Motor (Forward) O:0/1; Train Motor (Reverse) O:0/2; Gate Assembly Motor (Closing) O:0/3; Gate Assembly Motor (Opening) O:0/4.

#### 摘录 D

- 出处：第 7 页，Conclusion，`paper_content.txt` 第 223-230 行
> Whenever the train arrives from a specific direction the proximity sensor provides the signal to PLC and it generates an acceptable signal for the operation of DC motor to close/open the gate. PLC sends operating signal to the dc motors according to the output signal of sensors to open/close the railway crossing gate. In our project, we used obstacle detector switch which saves the life of obstacle.

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller uses train-position switches and obstacle-detection switches as PLC inputs and coordinates both the barrier motor and the train-drive motors. When an approaching train reaches the closing-side position switch, the PLC energizes the gate-closing output so the barrier motor lowers the gate, and the crossing stays in the protected state while the train passes. During this protected phase, obstacle switches are still monitored; if an obstacle is detected on the crossing, the PLC sends a stop command to the geared DC motors that move the train, and only restores the run command after the obstacle is cleared. When the train later reaches the departure-side switch, the PLC issues the opening command and reopens the barrier after a short delay, completing an arrival-close-monitor-depart-open control loop. Table 2 makes the EFSM interface explicit by listing separate addresses for train-position inputs, obstacle inputs, train forward/reverse outputs, and gate closing/opening outputs.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller uses train-position switches and obstacle-detection switches as PLC inputs and coordinates both the barrier motor and the train-drive motors.
   对应摘录：A, B, C
2. 句子 2：When an approaching train reaches the closing-side position switch, the PLC energizes the gate-closing output so the barrier motor lowers the gate, and the crossing stays in the protected state while the train passes.
   对应摘录：B, C
3. 句子 3：During this protected phase, obstacle switches are still monitored; if an obstacle is detected on the crossing, the PLC sends a stop command to the geared DC motors that move the train, and only restores the run command after the obstacle is cleared.
   对应摘录：B
4. 句子 4：When the train later reaches the departure-side switch, the PLC issues the opening command and reopens the barrier after a short delay, completing an arrival-close-monitor-depart-open control loop.
   对应摘录：B, C, D
5. 句子 5：Table 2 makes the EFSM interface explicit by listing separate addresses for train-position inputs, obstacle inputs, train forward/reverse outputs, and gate closing/opening outputs.
   对应摘录：C
