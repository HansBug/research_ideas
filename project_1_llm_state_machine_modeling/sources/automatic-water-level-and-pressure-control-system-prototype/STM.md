# Automatic Water Level and Pressure Control System Prototype Design Using Programmable Logic Controller and Human Machine Interface - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：论文对液位阈值触发泵启停，以及高液位后延时排水再回到低液位重启的循环控制过程都给出了直接的 PLC 行为描述。

## 条目 1: Float-triggered pump start and stop
- 控制对象：PLC 水箱液位控制子系统中的泵启停逻辑

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的水箱液位控制器，用于根据低液位和高液位浮球信号自动启动或停止补水泵。
- 判断：算。对象是实际水位控制系统中的 PLC 控制逻辑，原文明确给出了低位启动、高位停止的触发条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`A. Block Diagram System / B. Placement of Sensors`，行 117-131
> The water tank will be filled by a pump. The pump will automatically turn on when the water level
> in the water tank reaches a low level, and it stops when the water level reaches a high level. While,
> the solenoid valve works based on air pressure, when low pressure the sensor detects a drop in
> pressure according to the set point, so the air compressor will work, and it will stop when the pressure
> reaches the high pressure.
> This study uses two types of sensors that are level sensors and pressure sensors. The level sensors
> are mounted and used to measure and to sense the level of water presence at the required level in the
> tank. While pressure sensors are mounted and used to measure and to sense high of air pressure at
> the required pressure on the solenoid valve. Level sensors come into the PLC input module and inlet
> water valve is connected to the PLC output module.

#### 摘录 B
- 出处：第 4 页，`1) Float for Water Level Sensor`，行 162-176
> Float level sensor is a sensor put in the water tank and used to
> detect water level. The float level sensor has two floats that both of which have a space to float,
> and the spaces have each space limit that it will send signals to the PLC. The lower float (LL)
> has a lower limit space and an upper limit space for the upper float (HL).
> The first Float is the lower float that will send signals to the PLC if the lower water level reach
> or push a float in space limit (LL) in the lower that sign that the water tank will empty so the
> PLC will process the signals given by float level sensor to run the motor (pump) to pump the
> water from the water container (the water resource) come up in the water tank.
> The second float is the upper float that will work if the upper limit space (HL) is pushed since
> the water pressure on the float to up. In the limit, float level sensor sends signals to the PLC to
> process so that the PLC switch off the motor to pump the water come up in the water tank.

### 2. 基于原文整理后的自然语言描述

The PLC-based water level controller uses two float level sensors to supervise the tank level. When the lower float LL is reached, the PLC interprets the tank as empty and starts the pump to transfer water from the source container into the tank. When the upper float HL is reached, the PLC stops the pump after receiving the high-level signal.

### 3. 逐句溯源

1. 句子 1：The PLC-based water level controller uses two float level sensors to supervise the tank level.
   对应摘录：A, B
2. 句子 2：When the lower float LL is reached, the PLC interprets the tank as empty and starts the pump to transfer water from the source container into the tank.
   对应摘录：B
3. 句子 3：When the upper float HL is reached, the PLC stops the pump after receiving the high-level signal.
   对应摘录：A, B

## 条目 2: Fill-delay-drain-repeat tank cycle
- 控制对象：PLC 水箱控制系统中的填充、延时、排水与循环复位逻辑

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的水箱顺序控制逻辑，用于在高液位后延时开启阀门排水，在回到低液位后关闭阀门并重新启动泵。
- 判断：算。对象仍然是实际水位控制系统，原文给出了带触发点、延时和重复循环的离散阶段推进过程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，`C. Ladder Diagram and Human Machine Interface`，行 262-272
> Fig. 10 below is ladder
> diagram to control the level water when must filling in (the pump run) and when must switch off so
> that the water in the tank is not overflow from the tank.
> The working principal of the ladder program in Fig. 10 below is that in the rung 0, the program runs
> by activating the program with an indication that the start light is on and immediately starts the pump
> in the rung 2 and fill the water from the water resource (the water container) into the water tank.
> After the water reach the upper setting value (high level), the water state stops for a moment
> according to the set value on the timer in the rung 3, and then the solenoid valve opens the valve, and
> the water falls into the water container (the water resource). So that the water reaches the lower
> setting value (low level) and immediately the solenoid valve closed, and the pump starts. This process
> continues be repeating until deactivating the program with the stop light indication turning on in the
> rung 1.

### 2. 基于原文整理后的自然语言描述

After the program is activated, the ladder controller immediately starts the pump and fills the tank from the water source. When the water reaches the high-level setting, the controller holds the state for a timer-defined delay and then opens the solenoid valve so that the water falls back to the source container. Once the water reaches the low-level setting again, the solenoid valve is closed, the pump restarts, and the cycle repeats until the program is deactivated.

### 3. 逐句溯源

1. 句子 1：After the program is activated, the ladder controller immediately starts the pump and fills the tank from the water source.
   对应摘录：A
2. 句子 2：When the water reaches the high-level setting, the controller holds the state for a timer-defined delay and then opens the solenoid valve so that the water falls back to the source container.
   对应摘录：A
3. 句子 3：Once the water reaches the low-level setting again, the solenoid valve is closed, the pump restarts, and the cycle repeats until the program is deactivated.
   对应摘录：A
