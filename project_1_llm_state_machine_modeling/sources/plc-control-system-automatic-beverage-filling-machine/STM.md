# Analysis and Design of PLC-based Control System for Automatic Beverage Filling Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把空瓶确认、定量灌装、封盖和输送接续写成一条由传感器、称重确认、伺服泵和 HMI 参数共同驱动的 PLC 顺序控制链，足以稳定形成双 A 灌装产线样本。

## 条目 1: Empty-Bottle Confirm to Fill-Cap Handoff Controller

- 控制对象：自动饮料灌装机的空瓶确认、定量灌装、封盖与输送协同控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的灌装产线控制器，负责在空瓶到位后执行称重确认、灌装、封盖、输送和参数化速度协调。
- 判断：算。对象是真实灌装机 PLC 控制系统，原文明确给出空瓶检测、称重确认、伺服计量泵动作、自动/手动子程序和灌装完成后的移交流程，而不是泛泛介绍 PLC 优势。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Principle of automatic filling system / Hardware design`，`paper_content.txt` 第 45-74 行
> Automatic filling system is mainly composed of bottle sending system, liquid injection filling system and capping system.
>
> The empty bottles are sent into filling area ... after online weighing and empty bottles confirm, the injection filling system started to fill in the filling position. After the empty bottles being fully filled and confirmed by the online weighing system, they are covered with caps and sent out.
>
> ... bottle sending system, filling liquid injection system and the capping system are all within the core of PLC controller, various types of sensors are as motion control input, servo motor and stepping motor are as the driving assembly ...

#### 摘录 B

- 出处：第 2 页，`The functions of each part`，`paper_content.txt` 第 128-150 行
> Sensors: Include bottle coming sensors, weighing sensors, capping sensors, encoder, etc. As detecting elements of the control system, according to the state of each sensor, PLC output the corresponding action logic.
>
> Online weighing ... is real-time transmitted to the PLC, as confirmation signal for un-fill and filled.
>
> Servo filling mechanism: Servo motor drives the screw to control precision metering pump and filling capacity and the speed are set by the system parameters.
>
> Capping mechanism: After completely filled and confirmed by the online weighing system, bottles are capped.

#### 摘录 C

- 出处：第 3-4 页，`Software block diagram / Flow of filling program`，`paper_content.txt` 第 272-301 行
> Automatic/manual control subroutine: Complete automatic filling system to start, stop, reset and other functions and according to the actual condition of manual or automatic mode of operation.
>
> Drive control subroutine ... according to the filling speed adjust conveyor speed ...
>
> Filling servo control subroutine ... drive servo drives, control precision filling pump lotion, liquid filling and filling speed.
>
> The flow of filling program: When an empty bottle is sent into the filling area and confirmed by the online weighing system, the position detection sensor confirms the empty bottle is on the proper position. According to the different filling amount, the measurement parameters are set by the operator through human-machine interface ... After the filling head injecting, the full-filled bottle is sent to capping area by transmission system and filling head stop filling and then return and began to absorb liquid.

### 2. 基于原文整理后的自然语言描述

The beverage filling machine is controlled as a PLC-driven production sequence that moves bottles through arrival confirmation, metered filling, capping, and output transfer. The cycle starts when an empty bottle is guided into the filling area, and online weighing plus position detection confirm that the bottle is correctly placed for injection. At that point the PLC uses bottle, weighing, capping, and encoder sensors to choose the proper action logic, while a servo-driven precision metering pump fills the configured amount according to system parameters set through the HMI. The control program is partitioned into automatic/manual, drive, filling-servo, and capping subroutines, so conveyor speed can be coordinated with filling speed and the line can be started, stopped, reset, or switched between modes. Once injection completes, the filled bottle is transferred to the capping area, the filling head stops and returns to suction, and the sequence is ready to accept the next bottle.

### 3. 逐句溯源

1. 句子 1：The beverage filling machine is controlled as a PLC-driven production sequence that moves bottles through arrival confirmation, metered filling, capping, and output transfer.
   对应摘录：A
2. 句子 2：The cycle starts when an empty bottle is guided into the filling area, and online weighing plus position detection confirm that the bottle is correctly placed for injection.
   对应摘录：A, C
3. 句子 3：At that point the PLC uses bottle, weighing, capping, and encoder sensors to choose the proper action logic, while a servo-driven precision metering pump fills the configured amount according to system parameters set through the HMI.
   对应摘录：B, C
4. 句子 4：The control program is partitioned into automatic/manual, drive, filling-servo, and capping subroutines, so conveyor speed can be coordinated with filling speed and the line can be started, stopped, reset, or switched between modes.
   对应摘录：C
5. 句子 5：Once injection completes, the filled bottle is transferred to the capping area, the filling head stops and returns to suction, and the sequence is ready to accept the next bottle.
   对应摘录：A, C
