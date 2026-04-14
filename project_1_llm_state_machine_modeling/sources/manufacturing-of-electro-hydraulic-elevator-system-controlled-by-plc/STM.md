# Manufacturing of Electro-hydraulic Elevator System Controlled by PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电液电梯的呼梯输入、编码器楼层定位、比例阀上下行、门开闭限位与定时关门链写得足够具体，能够稳定落成 `EFSM + T1` 的双 A 样本。

## 条目 1: Three-Floor Electro-Hydraulic Elevator Call-and-Door Cycle Controller

- 控制对象：楼宇机电与电梯控制领域的三层电液电梯呼梯、行驶与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC、比例阀、编码器和门限位开关驱动的三层电液电梯原型控制器，负责呼梯、上下行、到层停靠与自动关门。
- 判断：算。论文主体就是 elevator prototype 的控制实现，不只是液压建模；原文明确给出了输入来源、楼层边界识别、门状态反馈、自动关门定时与上下行执行链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This model consists of hydraulic parts (double-acting hydraulic cylinders, pump, valves, pipeline and filter) and electronic parts (PLC, push-bottoms, relays and encoder). It is built with three floors ... and controlled by a PLC controller of (DELTA DVP-ES32) with 16 inputs and 16 outputs.
>
> The PLC receives input signals as orders from the operator as well as sensors and encoders. The PLC is programmed ... to basically calling the elevator cabin through three locations and enabling its arrival at the desired floor.

#### 摘录 B

- 出处：第 4 页，Section 3.1(c)
> The proportional valve in this system has two functions, controlling the direction of oil in order to control the movement of the cabin likewise controlling the size of the oil ... in order to obtain a smooth and jerk-less cabin movement especially at the starting and stopping.
>
> The proportional valve is controlled by PLC ...

#### 摘录 C

- 出处：第 5-6 页，Section 3.3
> To solve this problem, the encoder utilized to recognize those stories borders for each floor.
>
> Three limit switches were used in the electro-hydraulic elevator system ... (LS1) was placed at the top end of the frame. (LS2) and (LS3) switches were placed in the DC cabin door. When the cabin reaches any floor, the door will open and during that the door touches the (LS2) which in turn sends a signal to the PLC that the door opened.
>
> After passing four seconds, the door will close and touch the (LS3) to send a signal to the PLC that the door closed.

#### 摘录 D

- 出处：第 7 页，Section 4
> The floor level pattern is proposed as (Ground→ floor 3→ floor 2→ Ground→ floor 1) ...
>
> In the case of 30 kg, the floors sequence is different ... (Ground→ floor 2→ Ground→ floor 3→ floor 1) ...
>
> It is worth mentioning that the door of the cabin was closed by using the automatic mode (the timer closed the door after passing 3 sec).

### 2. 基于原文整理后的自然语言描述

The electro-hydraulic elevator controller supervises a three-floor prototype using operator call orders together with sensor, encoder, and limit-switch feedback. The PLC drives a proportional valve to select the cabin's motion direction and oil flow so the hydraulic cylinder can lift or lower the cabin toward the requested floor. Floor-border recognition is handled by the encoder, while `LS2` and `LS3` report whether the DC cabin door has fully opened or fully closed after the cabin reaches a floor. The door cycle is timed rather than purely combinational: the design description states that the door closes after four seconds, and the loaded automatic run reports a three-second timer-based close in sequences such as `Ground→2→Ground→3→1`.

### 3. 逐句溯源

1. 句子 1：The electro-hydraulic elevator controller supervises a three-floor prototype using operator call orders together with sensor, encoder, and limit-switch feedback.
   对应摘录：A, C
2. 句子 2：The PLC drives a proportional valve to select the cabin's motion direction and oil flow so the hydraulic cylinder can lift or lower the cabin toward the requested floor.
   对应摘录：A, B
3. 句子 3：Floor-border recognition is handled by the encoder, while `LS2` and `LS3` report whether the DC cabin door has fully opened or fully closed after the cabin reaches a floor.
   对应摘录：C
4. 句子 4：The door cycle is timed rather than purely combinational: the design description states that the door closes after four seconds, and the loaded automatic run reports a three-second timer-based close in sequences such as `Ground→2→Ground→3→1`.
   对应摘录：C, D
