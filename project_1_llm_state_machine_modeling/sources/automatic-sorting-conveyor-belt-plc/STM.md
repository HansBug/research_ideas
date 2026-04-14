# Development of Automatic Sorting Conveyor Belt Using PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把输送、检测、放行/剔除、启停和正反转控制链写成了可追溯的 PLC 输入输出逻辑。

## 条目 1: Photoelectric height-sorting conveyor PLC supervisor
- 控制对象：基于 PLC 的按高度分拣输送带与气缸剔除控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的 PLC conveyor sorter，用 photo-electric sensor 判断工件高度，再驱动气缸决定放行还是剔除。
- 判断：算。对象是实际分拣控制系统，原文给出了启动/停止、正反转、阈值判定、传感器输入、执行器输出和循环运行条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract 与 Introduction，对控制目标的说明，行 17-28、63-74
> The automatic sorting process is used to differentiate the products manufactured in an industry to further direct it towards packaging according to height.
> ...
> the system based on conveyor belt model to sort the objects which are of ideal selected height is described.
> ...
> A precise value of the height parameter is set which is used as a condition to either allow the objects to pass through to next step on the conveyor or be discarded in a different space.
> ...
> the photo-electric sensor senses the height of the object and gives its signal to the PLC which takes a decision based on that and further controls the actuator to either reject the object by the push of piston or allow it to go further.

#### 摘录 B
- 出处：第 2 页，Section 2，对工作流程的说明，行 83-90
> As soon as the green start button is pressed, the conveyor belt should start moving in the forward direction ... towards the photoelectric sensor which gives the signal if the object is not of suitable height.
> The output is processed in the PLC program which controls the actuator to either allow the object to pass through it or discard it with the piston push.
> This process should run in a repetitive cycle until the stop red push button is pressed to stop the conveyor belt.

#### 摘录 C
- 出处：第 8-9 页，Section 4-5，对实现结果和 I/O 的说明，行 199-205、214-221、238-241
> the hardware has been tested for the relay connections for motor rotation to run the conveyor belt forward and backward.
> ...
> Two Double Pole Double Throw Relays switched using green and red push buttons for start and stop respectively such that at one time only one relay operates which is activated by another mode selector switch for direction forward or reverse.
> ...
> the setup is able to sort objects of height 6cm and discards all the other objects with the piston.
> ...
> the conveyor doesn’t sort objects in the reverse direction while only runs in the forward direction when the Start green push button is pressed.
> ...
> I/P I0.2 as a toggle switch, I0.3 as a start push button (green), I0.4 as a stop push button (red), I0.5 as the sensor I/P and Q0.6 as the actuator O/P.

### 2. 基于原文整理后的自然语言描述

The PLC sorting system runs a conveyor that moves workpieces toward a photo-electric sensor and uses a configured height threshold to decide whether each object should continue downstream or be discarded. When the green start button is pressed, the conveyor runs in the forward direction, the sensor checks whether the current object has a suitable height, and the PLC drives the pneumatic actuator either to let the object pass or to reject it with a piston push. This decision loop repeats continuously until the red stop button is pressed. The implementation also supports forward and reverse conveyor motion through relay logic and a mode selector, but the paper states that sorting is performed only in forward mode. In the realized I/O mapping, `I0.2` is the direction toggle, `I0.3` is start, `I0.4` is stop, `I0.5` is the sensor input, and `Q0.6` is the actuator output, and the tested setup accepts `6 cm` objects while discarding the others.

### 3. 逐句溯源

1. 句子 1：The PLC sorting system runs a conveyor that moves workpieces toward a photo-electric sensor and uses a configured height threshold to decide whether each object should continue downstream or be discarded.
   对应摘录：A
2. 句子 2：When the green start button is pressed, the conveyor runs in the forward direction, the sensor checks whether the current object has a suitable height, and the PLC drives the pneumatic actuator either to let the object pass or to reject it with a piston push.
   对应摘录：A, B
3. 句子 3：This decision loop repeats continuously until the red stop button is pressed.
   对应摘录：B
4. 句子 4：The implementation also supports forward and reverse conveyor motion through relay logic and a mode selector, but the paper states that sorting is performed only in forward mode.
   对应摘录：C
5. 句子 5：In the realized I/O mapping, `I0.2` is the direction toggle, `I0.3` is start, `I0.4` is stop, `I0.5` is the sensor input, and `Q0.6` is the actuator output, and the tested setup accepts `6 cm` objects while discarding the others.
   对应摘录：C
