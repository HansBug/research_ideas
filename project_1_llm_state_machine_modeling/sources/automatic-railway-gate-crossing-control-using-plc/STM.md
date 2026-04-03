# AUTOMATIC RAILWAY GATE CROSSING CONTROL USING PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（普通离散状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对列车接近、报警、落杆、倒计时显示、通过后复位和电机正反转关系描述都很直接，适合作为道口门控样本。

## 条目 1: Sensor-Triggered Gate Closing and Reopening
- 控制对象：铁路平交口自动栏杆门控系统
- 状态机类型：FSM（普通离散状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是铁路道口控制领域的 PLC 门控系统，用于根据列车接近和离开传感器控制报警、栏杆关闭与复位。
- 判断：算。对象是实际铁路平交口门控系统，原文明确给出了到达侧传感、离开侧传感以及栏杆动作顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 25-31, 47-77 行
> The sensors are used to sense the arrival of the train, fault detection and signal passing to the plc and other components. The indication lamp and buzzer are used to indication purpose. The LED are used to railway platform. the train comes to the platform the some LED light are ON through a controller for safety of passengers and train is passing through the platform the LED is off.
>
> In this project detect the train and warn the road users about the arrival of train. If is found a green signal is given for the train to pass, otherwise a red signal is given to slow down. After they are cleared, the gate is closed and train is passed. We will make sure that the train is passed and reopen the gate. ... In this system whole operation is based on the sensor and their input to the PLC which sends the signal to open or close operation of the railway gate operating DC motor. ... The timer is connected to LED display near the gate. The displays the time remaining for closing or opening of the gate according to the necessary situation.

#### 摘录 B
- 出处：第 1-2 页，Working / Conclusions，`paper_content.txt` 第 82-111, 116-121 行
> When any train is coming from any one side than the sensor situated on that track gets high and a high signal is generated from the sensor by which the PLC generate a beep sound for a while and close the barriers for the traffic and the traffic signal gets amber by which the train can cross the gate easily. And when the train passes out from the crossing than the end side sensor which is sensor2 gets high and give a signal to PLC by which the PLC opens the barriers and the signals comes in its normal positions (off position).
>
> We can see here in the system that a buzzer is connected by which the alert sound is generated before closing the barriers so that the accidents can be minimized and the security level can be increased. ... For the forward and reverse operation of the DC motor we reverse the voltage so here we have connected a combination of two relays to take a forward and reverse voltage for the desired operation and the movement of the barriers of the system.
>
> When the train arrives in a particular direction the sensor senses and generates appropriates signal, then at the same time the PLC provides certain output signal to the DC motor to function.

### 2. 基于原文整理后的自然语言描述

The railway gate controller uses track-side sensors to detect an approaching train, warn road users, and drive the gate motor through PLC outputs rather than manual operation. When the arrival-side sensor goes high, the PLC generates a buzzer alert, closes the barriers, changes the traffic indication to amber so the train can cross, and uses a timer-driven LED display near the gate to show the remaining closing or opening time. When the train clears the crossing and the exit-side `sensor2` goes high, the PLC reopens the barriers and returns the signals to their normal off position. The same controller also turns platform LEDs on while the train is at the platform and off after it passes, and it drives barrier motion by reversing the DC motor through a two-relay forward/reverse arrangement.

### 3. 逐句溯源

1. 句子 1：The railway gate controller uses track-side sensors to detect an approaching train, warn road users, and drive the gate motor through PLC outputs rather than manual operation.
   对应摘录：A, B
2. 句子 2：When the arrival-side sensor goes high, the PLC generates a buzzer alert, closes the barriers, changes the traffic indication to amber so the train can cross, and uses a timer-driven LED display near the gate to show the remaining closing or opening time.
   对应摘录：A, B
3. 句子 3：When the train clears the crossing and the exit-side `sensor2` goes high, the PLC reopens the barriers and returns the signals to their normal off position.
   对应摘录：B
4. 句子 4：The same controller also turns platform LEDs on while the train is at the platform and off after it passes, and it drives barrier motion by reversing the DC motor through a two-relay forward/reverse arrangement.
   对应摘录：A, B
