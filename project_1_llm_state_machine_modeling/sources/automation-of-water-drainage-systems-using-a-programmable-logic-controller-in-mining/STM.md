# Automation of Water Drainage Systems Using a Programmable Logic Controller in Mining - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把矿井排水系统写成一条八步 PLC 监督控制算法，完整覆盖启动、自检、阈值启泵、阀门顺序、运行调节、紧急停机、正常停机和 SCADA 手自动切换。

## 条目 1: Eight-step mine drainage pump supervisor

- 控制对象：过程与环境控制领域的矿井排水泵站 PLC 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个矿井中央排水系统的 PLC 监督控制器，依据液位、压力、流量、振动、冷却水和阀位信号来决定泵的启停、调速、切换和报警停机。
- 判断：算。对象是实际排水泵站控制系统，不是单纯工艺综述；原文直接给出了八步 operational algorithm，并明确列出了启泵条件、阀门顺序、正常停机和 emergency shutdown 条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 9-19、36-39 行
> The presented solution enables automatic control of pumps based on parameters such as current water level, pipeline pressure, actuator positions, and the presence of a cooling water flow.
>
> ... The article describes the system’s operational algorithm and its ability to respond in real time to variations in the hydrogeological environment.

#### 摘录 B

- 出处：第 4 页，`Figure 3: Drainage System Control Algorithm`，`paper_content.txt` 第 308-354 行
> 1. System startup
> ▪ Check for power supply and PLC/SCADA readiness.
> ▪ Self-diagnosis of sensors and actuators (valves, contactors, frequency converters).
> 2. Monitoring input data
> ▪ Reading the water level in the water tank ...
> 3. Pump start condition
> ▪ If level ≥ upper threshold → activate pump start sequence.
> ▪ If level ≤ lower threshold → stop pump ...
> 4. Pump start-up sequence
> ▪ Opening the suction valve.
> ▪ Checking for the presence of cooling water.
> ▪ Starting the electric motor ...
> ▪ Smoothly increasing the speed ...
> ▪ Opening the discharge valve.
> 5. Operating mode
> ▪ Automatic switching between operating pumps in case of load or failure.
> 6. Emergency shutdown condition
> ▪ Overheating ... Lack of flow rate ... Vibrations above permissible limits ... Overflow ... Failure of a critical sensor or communication.
> 7. Pump stop (normal)
> ▪ Closing the discharge valve ... Stopping the electric motor ... Closing the suction valve.
> 8. SCADA Integration
> ▪ The operator can choose: Automatic mode ... Manual mode ...

#### 摘录 C

- 出处：第 4-5 页，`IV. Result and Discussion`，`paper_content.txt` 第 357-379 行
> The proposed algorithm ensures stable operation of the pumping system during pump operation while simultaneously reducing energy consumption ...
>
> intelligent pump switching,
>
> real-time monitoring, and flexible control based on dynamic conditions in the drainage network.

### 2. 基于原文整理后的自然语言描述

The drainage controller is an eight-step PLC supervisory algorithm for a mine pumping station, and it begins with system startup checks for power, PLC/SCADA readiness, and self-diagnosis of sensors and actuators. In normal operation, it continuously monitors tank level, pipeline flow and pressure, and motor or bearing condition, and it compares the water level with lower and upper thresholds to decide whether the pump should stay off or enter the start sequence. Once the upper threshold is reached, the controller executes an ordered start-up chain: open the suction valve, verify cooling-water availability, start the electric motor, ramp speed through the frequency converter, and then open the discharge valve. During the operating mode it maintains flow and pressure, automatically switches between pumps under load or fault conditions, and keeps regulating speed against current drainage demand. If overheating, missing flow, excessive vibration, overflow alarm, or critical sensor or communication failure occurs, the controller enters emergency shutdown; otherwise a normal stop closes the discharge valve, ramps down and stops the motor, and finally closes the suction valve, while SCADA allows the operator to select either automatic or manual mode.

### 3. 逐句溯源

1. 句子 1：The drainage controller is an eight-step PLC supervisory algorithm for a mine pumping station, and it begins with system startup checks for power, PLC/SCADA readiness, and self-diagnosis of sensors and actuators.
   对应摘录：A, B
2. 句子 2：In normal operation, it continuously monitors tank level, pipeline flow and pressure, and motor or bearing condition, and it compares the water level with lower and upper thresholds to decide whether the pump should stay off or enter the start sequence.
   对应摘录：A, B
3. 句子 3：Once the upper threshold is reached, the controller executes an ordered start-up chain: open the suction valve, verify cooling-water availability, start the electric motor, ramp speed through the frequency converter, and then open the discharge valve.
   对应摘录：B
4. 句子 4：During the operating mode it maintains flow and pressure, automatically switches between pumps under load or fault conditions, and keeps regulating speed against current drainage demand.
   对应摘录：B, C
5. 句子 5：If overheating, missing flow, excessive vibration, overflow alarm, or critical sensor or communication failure occurs, the controller enters emergency shutdown; otherwise a normal stop closes the discharge valve, ramps down and stops the motor, and finally closes the suction valve, while SCADA allows the operator to select either automatic or manual mode.
   对应摘录：B, C
