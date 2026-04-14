# PLC Based Automatic Door Opening & Closing System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动滑门的感应开门、占用保持、延迟关门、防夹回开、手动/自动切换和报警复位都写进了 PLC 逻辑链，足以形成双 A 样本。

## 条目 1: Manual-Auto Sliding-Door Open-Hold-Close PLC Controller

- 控制对象：楼宇机电领域的自动滑门开闭与防夹控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向公共建筑出入口的 PLC 自动滑门控制器，用感应开门、红外防夹、限位停机、`8 s` 保持延时和手动/自动模式共同管理门体运行。
- 判断：算。对象是真实楼宇自动门控制系统，原文明确给出感应输入、门位限位、延迟关门、防夹回开、手动按钮、急停与报警复位逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / Introduction / System Design`，`paper_content.txt` 第 21-30、43-47、61-66 行
> The primary objective of this system is to automate the process of opening and closing doors in response to user input or environmental conditions.
>
> The main working principle of the automatic door is to sense whether there is an object passing through the sensing device at the top of the door and the auxiliary infrared sensing device on the side of the door frame, giving the door a switch signal and then programmable control. The frequency converter, the drive motor and the transmission control the movement of the door leaf to realize the function of opening and closing the door.
>
> The automatic sliding door uses the inductive switch and safety grating to realize automatic control. At the same time, the manual control is realized by using the operation buttons.

#### 摘录 B

- 出处：第 3-4 页，`1.3 System Software Design`，`paper_content.txt` 第 140-146、148-152、163-176 行
> Automatic control of closing and anti-clamping: The automatic door touches the door opener I0.4 and enters the 8s timing. During the three sensors I0.6, I0.7, I1.0, if an object is detected, the timer T37 retimed. After the automatic door detects no object for 8 s, the PLC’s Q0.1, M0, V0 action, pass to the inverter a motor reversal signal and low speed running signal, a total of 6s automatic door closing, if any object is closed when the automatic door is closed I1.0 detects that the automatic door stops closing and executes the automatic door opening procedure. In the automatic closing, the automatic door uses a safety grating with a delay of only 0.2 s to prevent the object from being clamped.
>
> There are two kinds of alarm conditions in the automatic door. The automatic door appears to be operated manually or automatically and closed. The door will judge by the program, the M0.1 action will stop the whole automatic door control system, the fault light Q1.1 will light up, and after checking no problem, press the abnormal reset button I1.3.
>
> The automatic door in the text is mainly composed of two control modes, manual control and automatic control of the opening and closing of the automatic door.

#### 摘录 C

- 出处：第 2-3 页，`1.1 System Design / 1.3 System Software Design`，`paper_content.txt` 第 74-82、90-96 行
> This paper adopts the photoelectric sensor to collect whether the object passes the signal to the PLC, and controls the opening and closing of the automatic door through the inverter, the driving motor and the transmission device in the PLC control actuator.
>
> The input signal device and the output control device are clearly designed, and the number of input and output points is estimated in combination with the requirements of the automatic door function design. Select the appropriate PLC type based on the number of I/O points.
>
> Draw a complete ladder diagram according to the curriculum design requirements and practical applications. Use software simulation to export the program to the specified format and run the simulation to see if the function is implemented.

### 2. 基于原文整理后的自然语言描述

The automatic sliding-door controller uses a PLC, an inductive presence switch, an auxiliary infrared safety grating, a frequency converter, and a motor-transmission chain to manage door opening and closing at a public entrance. In automatic mode, a trigger on the door-opener input starts an `8 s` hold period, and the controller keeps re-timing that hold window whenever any of the presence sensors still detects an object in the passage. Once the doorway remains clear long enough, the PLC issues a reverse motor command and a low-speed closing signal for a `6 s` closing branch. If an object is detected during that closing movement, the anti-clamping logic interrupts the close path and immediately switches back to the door-opening procedure, with a `0.2 s` safety-grating delay used for pinch prevention. On top of the nominal automatic path, the same controller supports manual and automatic operating modes, fault-stop detection, alarm-light output, and abnormal reset input, so the resulting sample is a full EFSM with both nominal and abnormal branches.

### 3. 逐句溯源

1. 句子 1：The automatic sliding-door controller uses a PLC, an inductive presence switch, an auxiliary infrared safety grating, a frequency converter, and a motor-transmission chain to manage door opening and closing at a public entrance.
   对应摘录：A, C
2. 句子 2：In automatic mode, a trigger on the door-opener input starts an `8 s` hold period, and the controller keeps re-timing that hold window whenever any of the presence sensors still detects an object in the passage.
   对应摘录：B
3. 句子 3：Once the doorway remains clear long enough, the PLC issues a reverse motor command and a low-speed closing signal for a `6 s` closing branch.
   对应摘录：B
4. 句子 4：If an object is detected during that closing movement, the anti-clamping logic interrupts the close path and immediately switches back to the door-opening procedure, with a `0.2 s` safety-grating delay used for pinch prevention.
   对应摘录：B
5. 句子 5：On top of the nominal automatic path, the same controller supports manual and automatic operating modes, fault-stop detection, alarm-light output, and abnormal reset input, so the resulting sample is a full EFSM with both nominal and abnormal branches.
   对应摘录：B, C
