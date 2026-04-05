# Four Junction Traffic Light Controller using PLC (S7-200) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口直行/转向灯组的完整相位循环、每段驻留时间、启动/停止输入和灯组输出映射写成了标准的定时状态序列。

## 条目 1: Timed Four-Junction Straight-and-Turn Phase Cycle
- 控制对象：道路交通信号控制领域的四路口 PLC 直行/转向相位控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 S7-200 PLC 实现的四路口交通灯控制器，用于按照固定时序轮转主路、侧路以及转向相位。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了启动/停止按钮、灯组输出、相位顺序和各阶段的定时持续时间。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Schematic Diagram / Software Implementation，`paper_content.txt` 第 185-200、239-244 行
> The start and stop buttons are connected in input of the PLC and pilots’ light. Main road and side road, are output of PLC.
>
> When the program is started, main road is green and the side road is red about 15s. After this, the yellow light is turn on 5s. And the side road is green and main road is red about 15s. After side is yellow about 5s, it changes to red. At that time the main road turn is green and side road turn is red about 10s. After 10s, the side road is green and the main road is green.

#### 摘录 B
- 出处：第 6 页，Figure 7 The Flow Chart of Operation of Traffic Light System，`paper_content.txt` 第 252-268 行
> Start -> Gm, Rs, Rt1, Rt2 -> 15Sec -> Ym, Rs, Rt1, Rt2 -> 5Sec -> Rm, Gs, Rt1, Rt2 -> 15Sec -> Rm, Ys, Rt1, Rt2 -> 5Sec -> Rm, Rs, Gt1, Rt2 -> 10Sec -> Rm, Rs, Rt1, Gt2 -> 10Sec -> End

#### 摘录 C
- 出处：第 7-8 页，Results and Discussion，`paper_content.txt` 第 279-315 行
> The main road has red, yellow, green, turn green and turn red. The side road has also the same ... The side road is red and the main road is green ... After 15 second, the side road is red but the main road yellow light is turn on.
>
> After the main road and side road are red, the main turn is green and the side turn is red ... After 5s green of the main turn on, it goes to red. And the side turn is green.

### 2. 基于原文整理后的自然语言描述

After the start button is pressed, the four-junction PLC controller enters a fixed traffic cycle beginning with main-road green and side-road red. It then switches the main road to yellow for `5 seconds`, transfers the right-of-way to the side road for `15 seconds`, and follows with a `5 seconds` side-road yellow phase. Once both straight directions are red, the controller activates the main turn phase for `10 seconds` and then the side turn phase for `10 seconds` before returning to the start of the cycle. The stop button breaks the loop and the lamp outputs are implemented directly on the PLC outputs for the main-road and side-road green, yellow, red, turn-green, and turn-red lamps.

### 3. 逐句溯源

1. 句子 1：After the start button is pressed, the four-junction PLC controller enters a fixed traffic cycle beginning with main-road green and side-road red.
   对应摘录：A, B
2. 句子 2：It then switches the main road to yellow for `5 seconds`, transfers the right-of-way to the side road for `15 seconds`, and follows with a `5 seconds` side-road yellow phase.
   对应摘录：A, B, C
3. 句子 3：Once both straight directions are red, the controller activates the main turn phase for `10 seconds` and then the side turn phase for `10 seconds` before returning to the start of the cycle.
   对应摘录：A, B, C
4. 句子 4：The stop button breaks the loop and the lamp outputs are implemented directly on the PLC outputs for the main-road and side-road green, yellow, red, turn-green, and turn-red lamps.
   对应摘录：A, C
