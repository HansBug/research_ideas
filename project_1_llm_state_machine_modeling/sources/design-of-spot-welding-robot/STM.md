# Design of Spot Welding Robot - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出点焊机器人 `manual / automatic` 两层模式、自动模式下 `single-step / single-cycle / continuous` 三个子模式，以及完整的动作顺序和 `2.4` 秒焊接周期，属于高质量层次状态机样本。

## 条目 1: Manual/automatic spot-welding robot sequence supervisor

- 控制对象：工业自动化与离散制造领域的点焊机器人多模式顺序控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 PLC 控制的三自由度点焊机器人，顶层分为手动与自动，自动模式下再细分为单步、单循环和连续循环。
- 判断：算。原文明确给出模式层级、动作顺序、限位开关、启动停止按钮和焊接时间控制，能稳定支撑 HSM 抽取。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The hardware design includes two parts: manual mode and automatic mode. Manual mode is generally used for the robot system installation, commissioning and troubleshooting, and the major modules are controlled by the start of the corresponding button; automatic mode is mainly used for production stage.

#### 摘录 B

- 出处：第 2 页，Mechanical Systems Design Scheme
> The robot is controlled through the PLC to complete the movements of arm telescoping, rotation and waist rotation. ... the welding efficiency is 22 points/min and welding cycle time is 2.4 seconds.

#### 摘录 C

- 出处：第 4-5 页，The Workflow
> The initial position of the welding clamp is in situ, after pressing the start button, and the robot will complete movements in sequence: dextral → backspin → elongation → welding → contraction → topspin → sinistral. The rotation and movements conversion of welding clamp is controlled by limit switches, and the welding time is controlled by the time relay.

#### 摘录 D

- 出处：第 4-5 页，The Workflow
> To meet the production requirements, the control modes have manual mode and automatic mode, and the automatic mode have single-step, single-cycle and continuous operation mode.

#### 摘录 E

- 出处：第 4-5 页，The Workflow
> Single-step mode: starting from the situ, according to the automatic cycle process, per-click the Start button, the arm completes a step action and then stops automatically. Single-cycle mode: Press the start button, the arm will automatically complete a cycle action from the origin, and then stops in situ. Continuous operation mode: when the arm is in situ, press the start button, the arm will automatically and continuously execute cycle action.

#### 摘录 F

- 出处：第 5 页，PLC Programming
> When chose automatic mode (Single-step, single circle, continuous), I1.2, I1.3, I1.4 is turned on respectively, the system perform automatic procedure.

### 2. 基于原文整理后的自然语言描述

The spot-welding robot controller is organized hierarchically with a top-level split between manual mode and automatic mode. In manual mode, dedicated buttons directly command dextral, sinistral, topspin, backspin, elongation, contraction, and welding actions for installation or troubleshooting. In automatic mode, the robot always starts from the in-situ state and executes the fixed process sequence `dextral -> backspin -> elongation -> welding -> contraction -> topspin -> sinistral`, with limit switches controlling the motion transitions and a time relay controlling the welding duration. The automatic layer is further divided into single-step, single-cycle, and continuous submodes. Single-step advances one action per start press, single-cycle completes one full welding cycle and returns to the origin, and continuous mode repeats the cycle until a stop command is issued.

### 3. 逐句溯源

1. 句子 1：The spot-welding robot controller is organized hierarchically with a top-level split between manual mode and automatic mode.
   对应摘录：A, D
2. 句子 2：In manual mode, dedicated buttons directly command dextral, sinistral, topspin, backspin, elongation, contraction, and welding actions for installation or troubleshooting.
   对应摘录：A
3. 句子 3：In automatic mode, the robot always starts from the in-situ state and executes the fixed process sequence `dextral -> backspin -> elongation -> welding -> contraction -> topspin -> sinistral`, with limit switches controlling the motion transitions and a time relay controlling the welding duration.
   对应摘录：B, C
4. 句子 4：The automatic layer is further divided into single-step, single-cycle, and continuous submodes.
   对应摘录：D, F
5. 句子 5：Single-step advances one action per start press, single-cycle completes one full welding cycle and returns to the origin, and continuous mode repeats the cycle until a stop command is issued.
   对应摘录：E
