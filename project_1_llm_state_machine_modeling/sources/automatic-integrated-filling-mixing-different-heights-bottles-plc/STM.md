# Automatic Integrated Filling and Mixing of Different Heights of Bottles using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多高度瓶检测、三种模式选择、双阀互锁和混合流程都写成了可直接整理的 PLC 顺序控制链，是比较有代表性的灌装/混合复合样本。

## 条目 1: Mode-Selected Bottle Filling and Two-Station Mixing Supervisor

- 控制对象：不同瓶高瓶装灌装与双站混合一体线的模式控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的灌装/混合模式控制器，用两级 IR 传感器、模式选择器和双阀互锁组织不同瓶高灌装与双产品混合。
- 判断：算。对象是实际生产线控制系统，原文明确给出了 `Mode 1 / Mode 2 / Mode 3`、小瓶/大瓶判定、阀门开启时长、混合站顺序以及紧急停机回 idle/reset 的条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / `III. System Description`，`paper_content.txt` 第 20-31 行、第 91-103 行
> This paper proposes an integrated bottle filling and mixing system of different height of bottles for two different types of products using Sensors and PLC ... Here sensors acts as the input device. PLC acts as the real time decision maker ...
>
> This system has two filling stations and three Modes. For filling of bottles Mode 1 and Mode 2 are used and Mode 3 is used for Mixing. During filling process, by interlock these two products; one product is used at a time.

#### 摘录 B

- 出处：第 2 页，`IV. Working / V. System Inputs / Outputs`，`paper_content.txt` 第 144-156 行、第 172-186 行
> A program is created for various heights of bottles and varying time for opening of valve must be fixed for corresponding bottles heights. Filling and mixing process is based on timing and this is preprogrammed. ... mode selector switch is placed to select the mode (Filling or Mixing). When one mode is selected ... sensors and valves in another product won’t get energized i.e. they are interlocked with each other ...
>
> The input module comprises IR sensors, Mode selector switch, and Start/Stop pushbuttons. ... One push button is used to start the process and another push button is used to stop the process or act as emergency switch. ... Motor is used to drive the conveyors, solenoid valve is used to open and close the valve of the tank containing liquids to be filled.

#### 摘录 C

- 出处：第 3 页，`VIII. Sequence of Operations`，`paper_content.txt` 第 233-261 行
> Press the START push button to start the entire system. Select any one mode by mode selector switch ...
>
> For Mode 1 or Mode 2, if lower IR sensor only gets ON (i.e. small size bottle comes on the conveyor) then conveyor stops and valve 1 in the tank will open for preset time.
>
> If both lower and upper IR sensors gets ON (i.e. large size bottle comes on the conveyor) then conveyor stops and valve 2 will open for preset time. After the respective time period valve will automatically get closed.
>
> For Mode 3, If IR sensor near the filling station 1 senses object then conveyor stops and valve 1 will open for some period of time after that conveyor starts moving and bottles are stopped near the filling station 2 by the IR sensors. The valve 2 will open for some time through these two products will get mixed.
>
> ... If STOP or Emergency button is pressed then the system goes to the idle state and all outputs will go to the Reset condition.

### 2. 基于原文整理后的自然语言描述

The integrated controller supervises a single conveyor line that can run in two filling modes and one mixing mode, and the active mode is selected by a mode-selector switch after the operator starts the system. In filling mode, bottle height is inferred from two vertically separated IR sensors: if only the lower sensor is active the conveyor stops and one valve opens for its preset fill time, whereas if both lower and upper sensors are active the conveyor stops and the other valve opens for a different preset interval. The two product lines are interlocked during filling so that selecting one mode prevents the sensors and valve set of the other product from energizing. In mixing mode, bottles are first stopped at filling station 1 for one timed valve-opening step, then advanced to filling station 2 for a second timed valve-opening step so the two products are combined, and any stop or emergency command sends the system back to idle/reset.

### 3. 逐句溯源

1. 句子 1：The integrated controller supervises a single conveyor line that can run in two filling modes and one mixing mode, and the active mode is selected by a mode-selector switch after the operator starts the system.
   对应摘录：A, B, C
2. 句子 2：In filling mode, bottle height is inferred from two vertically separated IR sensors: if only the lower sensor is active the conveyor stops and one valve opens for its preset fill time, whereas if both lower and upper sensors are active the conveyor stops and the other valve opens for a different preset interval.
   对应摘录：B, C
3. 句子 3：The two product lines are interlocked during filling so that selecting one mode prevents the sensors and valve set of the other product from energizing.
   对应摘录：A, B
4. 句子 4：In mixing mode, bottles are first stopped at filling station 1 for one timed valve-opening step, then advanced to filling station 2 for a second timed valve-opening step so the two products are combined, and any stop or emergency command sends the system back to idle/reset.
   对应摘录：C
