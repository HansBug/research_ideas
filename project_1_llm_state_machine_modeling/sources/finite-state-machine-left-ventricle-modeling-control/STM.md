# Finite state machine implementation for left ventricle modeling and control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把左心室压容环模拟控制明确写成 `Mealy` 型有限状态机，并给出四个压容相位、可变输入集、输出力以及 `1024 Hz` 固定采样执行方式，可直接作为 `EFSM + T1` 医疗控制样本。

## 条目 1: Four-phase left-ventricle PV-loop Mealy controller

- 控制对象：左心室压容环模拟与执行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把左心室压力-容积循环分成四个心动周期相位，并用固定步长 `FSM` 去驱动液压 mock circulatory system 的执行控制器。
- 判断：算。对象是真实医疗实验系统中的左心室执行/模拟控制器，不是单纯生理建模背景；原文给出了相位定义、状态转移图、输入变量、输出力和执行采样率。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 6-14 行
> Producing a finite-state machine governance of a left ventricle model would enable a broad range of applications ... This approach uses a logic-based conditional finite state machine based on the four pressure-volume phases that describe left ventricular function. This was executed with a physical system hydraulic model using MathWorks' Simulink and Stateflow tools.

#### 摘录 B

- 出处：第 4 页，Figure `1` 说明，`paper_content.txt` 第 176-177 行
> In Phase I ... ventricular filling occurs with only a small increase in pressure and a large increase in volume ... Phase II constitutes the first segment of systole called isovolumetric contraction. Phase III begins with the opening of the aortic valve; ejection initiates ... Isovolumetric relaxation begins after the closure of the aortic valve constituting Phase IV.

#### 摘录 C

- 出处：第 10-11 页，Section `PV loop modeling utilizing a state machine control architecture approach`，`paper_content.txt` 第 372-410 行
> Utilizing Simulink Stateflow, a sequential decision-based control logic represented in Mealy machine structure form was developed to control the transition between LV-PV phases. ... The Inputs are parameters that can change with time and are LVESP, LVESV, LVEDV, LVEIRP, time (t), simulated pressure (P), and simulated volume (V). The Output ... is Force (F) applied to the piston in Newtons ... The FSM operates at a sampling rate of 1024 Hz.

#### 摘录 D

- 出处：第 13 页，Figure `4` 说明，`paper_content.txt` 第 547-549 行
> The Inputs, parameters that can change with time, are LVESP, LVESV, LVEDV, LVEIRP, simulated pressure [mmHg], and simulated volume [mL]. The output variable of the model, is Force (F) applied to the piston in Newtons. ... The oval shapes are the five states of the model. ... The sample rate is 1024 Hz.

### 2. 基于原文整理后的自然语言描述

The left-ventricle controller is implemented as a Mealy-type finite state machine that reproduces the four pressure-volume phases of the cardiac cycle: filling, isovolumetric contraction, ejection, and isovolumetric relaxation. Clinical or simulated inputs such as `LVESP`, `LVESV`, `LVEDV`, `LVEIRP`, current time, pressure, and volume determine the phase transitions, while the output is the piston force driving a hydraulic mock-circulation model. The state transition diagram is executed in Stateflow at `1024 Hz`, so every phase change and force update occurs in a deterministic fixed-step loop suitable for hardware deployment. Because preload, afterload, and contractility can be changed over time, the discrete phase machine is tightly coupled to continuous pressure-volume variables rather than being a purely symbolic sequence. The sample therefore preserves both the explicit mode backbone of the cardiac cycle and the engineering timing needed to run the controller on a real experimental left-ventricle platform.

### 3. 逐句溯源

1. 句子 1：The left-ventricle controller is implemented as a Mealy-type finite state machine that reproduces the four pressure-volume phases of the cardiac cycle: filling, isovolumetric contraction, ejection, and isovolumetric relaxation.
   对应摘录：A, B, C
2. 句子 2：Clinical or simulated inputs such as `LVESP`, `LVESV`, `LVEDV`, `LVEIRP`, current time, pressure, and volume determine the phase transitions, while the output is the piston force driving a hydraulic mock-circulation model.
   对应摘录：C, D
3. 句子 3：The state transition diagram is executed in Stateflow at `1024 Hz`, so every phase change and force update occurs in a deterministic fixed-step loop suitable for hardware deployment.
   对应摘录：C, D
4. 句子 4：Because preload, afterload, and contractility can be changed over time, the discrete phase machine is tightly coupled to continuous pressure-volume variables rather than being a purely symbolic sequence.
   对应摘录：A, C
5. 句子 5：The sample therefore preserves both the explicit mode backbone of the cardiac cycle and the engineering timing needed to run the controller on a real experimental left-ventricle platform.
   对应摘录：A, B, C, D
