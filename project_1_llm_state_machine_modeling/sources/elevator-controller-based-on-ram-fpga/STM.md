# Elevator controller based on implementing a random access memory in FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把两层电梯控制器写成 `10×7` 输入输出映射的 RAM/LUT，并给出 `20` 步地址-数据表和完整的地面层呼梯执行链，虽然不是传统命名状态图，但仍可稳定整理成系统级 EFSM 样本。

## 条目 1: Ten-Input Seven-Output Elevator LUT Controller

- 控制对象：楼宇机电与电梯控制领域的两层电梯 LUT/RAM 门控与行驶控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `FPGA + 10×7 RAM` 的两层电梯控制器，用楼层按钮、门按钮和门/楼层传感器输入驱动轿厢上行、下行、开门、关门与忙信号输出。
- 判断：算。虽然原文没有用传统状态名画出平面状态图，但它明确给出输入/输出编码、`20` 条控制步和一条完整的呼梯执行链，足以作为扩展状态机样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 19-33 行
> A look-up-table LUT ... represented a proposed relation between 10 and 7 lines, the states of the sensors and switches have been represented by the 10 input lines, and the commands for the motors of slide door and traction machine have been represented by the 7 output lines. The proposed LUT has been schematically realize by a (10×7) bits RAM.

#### 摘录 B

- 出处：第 3-4 页，Section 2 `Research Method`，`paper_content.txt` 第 147-187 行
> The LUT of the proposed elevator has been designed with 10 input and 7 output lines ... X0 ... car calling ... ground floor ... X4 ... close the slide door ... X8 ... reaching the ground floor ... X9 ... reaching the first floor ... Y0 move the car upward ... Y1 move the car downward ... Y2 slide door closing ... Y3 slide door opening ... Y5 busy signal generation.

#### 摘录 C

- 出处：第 4-5 页，Table 1 与测试说明，`paper_content.txt` 第 188-203、231-254 行
> Table 1 illustrates ... 20 steps of relation between address and data bits of the proposed schematic RAM.  
> For testing the proposed controller ... switch X0 of car calling by someone at ground floor, where the car in the first floor ... (0010010) commands the slide door motor to close the door ... after the slide door will be closed ... (0100010) ... command the traction motor to move the car in downward direction toward the ground floor ... when the car is reached to the ground floor ... (0001010) ... command the car to stop and then command the motor to open the slide door.

### 2. 基于原文整理后的自然语言描述

The proposed elevator controller is organized as a `10`-input, `7`-output lookup-based control machine rather than as a loose collection of relay rules. Its input side includes hall-call switches, in-car floor-selection switches, door open/close switches, door-position sensors and floor-position sensors, while its output side commands upward motion, downward motion, door closing, door opening, busy signalling and switch-reset actions. The paper then instantiates this control logic as a `10×7` RAM with `20` address-data rows, so each encoded sensor/switch situation maps directly to a motor-action pattern. In the worked execution chain, a ground-floor hall call causes the controller to close the door, drive the car downward from the first floor, stop at the ground floor, and open the slide door, which gives a complete elevator service sequence that can be modeled as an EFSM over encoded I/O states.

### 3. 逐句溯源

1. 句子 1：The proposed elevator controller is organized as a `10`-input, `7`-output lookup-based control machine rather than as a loose collection of relay rules.
   对应摘录：A, B
2. 句子 2：Its input side includes hall-call switches, in-car floor-selection switches, door open/close switches, door-position sensors and floor-position sensors, while its output side commands upward motion, downward motion, door closing, door opening, busy signalling and switch-reset actions.
   对应摘录：B
3. 句子 3：The paper then instantiates this control logic as a `10×7` RAM with `20` address-data rows, so each encoded sensor/switch situation maps directly to a motor-action pattern.
   对应摘录：A, C
4. 句子 4：In the worked execution chain, a ground-floor hall call causes the controller to close the door, drive the car downward from the first floor, stop at the ground floor, and open the slide door, which gives a complete elevator service sequence that can be modeled as an EFSM over encoded I/O states.
   对应摘录：C
