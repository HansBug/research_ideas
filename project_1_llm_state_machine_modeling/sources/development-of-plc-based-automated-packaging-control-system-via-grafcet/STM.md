# Development of PLC-based Automated Packaging Control System via Grafcet - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 24 罐装包装系统的三段式 `Grafcet` 顺序、计数器、气缸动作和后续梯形图/PLC 落地链写得很完整，可直接形成双 A 样本。

## 条目 1: Grafcet-Based 24-Can Packaging Sequence Controller

- 控制对象：工业自动化与离散制造领域的罐装包装顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC + Grafcet` 的自动包装控制器，用多个双作用气缸、计数器、限位/接近信号和输送带共同完成 `24` 个罐体的列生成、行生成与最终堆叠。
- 判断：算。对象是实际离散制造包装系统，原文明确给出三段式顺序 `[({[B+B-] x 4} + [A+A-]} x 3) x 2`、各段执行条件、计数器用途、执行器构成以及 PLC/梯形图实现。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页与第 29 页，`Abstract / 4.1 Simulation design`，`paper_content.txt` 第 91-95、752-764 行
> the project would be on improvising a system in packaging a batch of 24 canned food into a cardboard box for SMI production system. The system will be fully automatic and will be controlled using industrial controller, in this case a programmable logic controller (PLC). This project will be focusing on Grafcet programming method to develop the programming sequences for the actuators in the packaging system under study.
>
> The full sequence of this project is : [({[B+B-] x 4} + [A+A-]} x 3) x 2]
>
> As we can see, there are 3 parts in the sequence. The first part is cylinder B need to extend and retract 4 times, second part is cylinder A need to extend and retract after the first part process has completed for 3 times, and the last part is the 2 cycle combination of the first and second part.

#### 摘录 B

- 出处：第 29-34 页，`4.1.1 First part / 4.1.2 Second part / 4.1.3 Third part`，`paper_content.txt` 第 759-761、773-778、795-800、845-850 行
> From the diagram we can see that the first part of the sequence will create the 4 column of the canned food arrangement, the second part will create the 3 row arrangement and the last part is the stacking process of the canned food to create a 24 can arrangement.
>
> Cylinder B needs to extend and retract for 4 times. Thus a simple counter system is used to implement the sequence. A double acting cylinder will be used as the actuator which will be controlled by a 5/2 way solenoid valve. A proximity sensor will also be placed at both end of the double acting cylinder to be used as a signal for the program.
>
> For the second part, cylinder A needs to extend and retract for 3 times after the completion of each part one sequence. Thus, the program is implemented by using simultaneous exclusive action of Grafcet which is to allow only one step to be active at a time by using transition condition. Also a second counter system is added to the system.
>
> For the third and final part, the full sequence of the project will be implemented. Since actuator D only need to extend and retract once of the completion of both first and second part, no counter is needed.

#### 摘录 C

- 出处：第 35-44 页，`4.2 Simulation testing / 4.3.3 Testing and commissioning / 4.4 Discussion`，`paper_content.txt` 第 885-900、991-1009、1022-1028 行
> Steps will not proceed until the transition condition is met.
>
> For the hardware simulation, the actuator, solenoid valves and proximity switch is tested to make sure that it is following the right sequence tally with the Grafcet program.
>
> For the actuators, the demonstration unit will be using 3 double acting cylinders with 5/2 way spring returned solenoid valve.
>
> After the modification was done, the system run flawlessly. Also a conveyer system which was not previously available in the simulation was added to the system. The conveyer system is controlled by the proximity sensor, counter 1 and counter 2 of the system.
>
> It makes program troubleshooting easier as only one part of the program is active at a time. It reduces overall PLC program scan time by only scanning active program steps. Well suited method for systems that work in sequence.

### 2. 基于原文整理后的自然语言描述

The packaging controller is a PLC-based `Grafcet` sequence system that automatically arranges a batch of `24` canned products into a cardboard box rather than relying on a human operator to perform repetitive packing. Its overall sequence is written explicitly as `[({[B+B-] x 4} + [A+A-]} x 3) x 2]`, which the author decomposes into three coordinated parts: a first branch that makes four column-forming `B+ / B-` cycles, a second branch that makes three row-forming `A+ / A-` cycles after each completed part-one sequence, and a final branch in which actuator `D` executes the stacking action after the first two parts are complete. The implementation uses double-acting cylinders, `5/2` solenoid valves, proximity or limit signals, and at least two counters to guard progress through the sequence, while `Grafcet` transition conditions ensure that a later step cannot start until the current branch is complete. After conversion to ladder logic and hardware commissioning, the same controller is run on a PLC demonstration unit with three cylinders and an added conveyor path controlled by the proximity sensor and both counters. The resulting sample is therefore a concrete manufacturing EFSM in which counts, actuator strokes, and transition guards are all part of the control semantics.

### 3. 逐句溯源

1. 句子 1：The packaging controller is a PLC-based `Grafcet` sequence system that automatically arranges a batch of `24` canned products into a cardboard box rather than relying on a human operator to perform repetitive packing.
   对应摘录：A
2. 句子 2：Its overall sequence is written explicitly as `[({[B+B-] x 4} + [A+A-]} x 3) x 2]`, which the author decomposes into three coordinated parts: a first branch that makes four column-forming `B+ / B-` cycles, a second branch that makes three row-forming `A+ / A-` cycles after each completed part-one sequence, and a final branch in which actuator `D` executes the stacking action after the first two parts are complete.
   对应摘录：A, B
3. 句子 3：The implementation uses double-acting cylinders, `5/2` solenoid valves, proximity or limit signals, and at least two counters to guard progress through the sequence, while `Grafcet` transition conditions ensure that a later step cannot start until the current branch is complete.
   对应摘录：B, C
4. 句子 4：After conversion to ladder logic and hardware commissioning, the same controller is run on a PLC demonstration unit with three cylinders and an added conveyor path controlled by the proximity sensor and both counters.
   对应摘录：C
5. 句子 5：The resulting sample is therefore a concrete manufacturing EFSM in which counts, actuator strokes, and transition guards are all part of the control semantics.
   对应摘录：A, B, C
