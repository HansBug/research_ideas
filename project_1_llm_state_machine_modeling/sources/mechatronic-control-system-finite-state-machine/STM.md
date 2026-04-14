# Mechatronic Control System on a Finite-State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动滑门控制器明确写成带多级子状态的 FSM，既给出了 `init / positive / negative / stop` 主状态，也给出了运动扇区子状态、输入输出接口和阻塞恢复逻辑，足以形成双 A 的层次化门控样本。

## 备注

- 首页标题和作者处有少量版式噪声，但第 `2`、`6-8`、`10` 页关于 automatic sliding-door FSM 的控制主链清晰可核对，不影响提取。

## 条目 1: Hierarchical Sliding-Door Motion FSM with Blockade Recovery

- 控制对象：楼宇机电与自动门控制领域的自动滑门运动与阻塞恢复控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向自动滑门的多层 FSM 控制器，由门管理 FSM 向运动生成 FSM 下达命令，再由运动 FSM 产生位置、速度、加速度参考并处理阻塞恢复。
- 判断：算。对象是实际 mechatronic automatic sliding-door controller，不是单纯的软件方法展示；原文直接写出了控制输入/输出、主状态、子状态层级和障碍打断后的恢复规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 10-20 行
> This paper describes design using state-transition methodology. The current operational function of the system is described as the current state of the system using state-transition programming. The state transition diagram or table describes the current state and the conditions for transition. ... The presented application of an automatic sliding-door illustrates the feasibility of this approach. This paper presents the MFSM (Modular Finite-State Machine) ...

#### 摘录 B

- 出处：第 2 页，Section `2 SYSTEM DESCRIPTION`，`paper_content.txt` 第 123-142 行
> This is a system where the control system controls the application of automatic doors. The control system receives certain information (inputs) from the application, and generates actions (outputs) that affect it. ... The outputs represent the control system's states (open, closed, locked etc.). Each previous state is stored within a variable. The new state depends on the previous state and the input conditions. A switching algorithm between states with input and state conditions is the core of the FSM.

#### 摘录 C

- 出处：第 6-8 页，Section `4 MOTION BASED ON FSM`，`paper_content.txt` 第 344-414 行
> The FSM door motion was designed in Matlab/Simulink-StateFlow. ... The FSM motion-generator has 14 different inputs. The input PROMACHINE_IN is connected to the door management FSM, which gives commands to the FSM motion-generator. ... The FSM motion-generator with 5 outputs represents 3 pieces of reference data (acceleration, velocity, and position). ... The states (init., positive, negative, and stop) have two sub-levels. Let's take the state-positive for example. The first sub-level contains positive motion profile sector-switching (sectors I to VIII ...). The positive motion consists of 8 first sub-states ... The states at the first sub-level have states in the second sub-level.

#### 摘录 D

- 出处：第 10 页，Section `5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR`，`paper_content.txt` 第 501-505 行
> The door during normal operation goes into blockade detection when the motion is forcefully interrupted (obstacle collision or any other movement prevention). In this case the door changes movement direction or stops with an error indicator after three subsequent attempts.

### 2. 基于原文整理后的自然语言描述

The paper models the automatic sliding-door controller as a hierarchical FSM rather than a flat IF-THEN ladder. A door-management FSM sends the command input `PROMACHINE_IN` to the motion-generator FSM, while the motion layer also reads actuator position and velocity related inputs and outputs reference acceleration, velocity, position, status, and diagnostic toggle information back to the rest of the controller. At the main level, the motion generator is organized around `init`, `positive`, `negative`, and `stop`, and the motion states are then refined into sub-levels instead of being kept flat. In the `positive` direction, the first sub-level switches across eight motion-profile sectors, and the second sub-level finishes the detailed motion equations for states such as `S20`, so the paper preserves both the high-level travel mode and the lower-level sector computation chain. During normal operation, if the door motion is forcefully interrupted by an obstacle or another movement-prevention condition, the FSM enters blockade detection, reverses direction when possible, and finally stops with an error indication after three consecutive failed attempts.

### 3. 逐句溯源

1. 句子 1：The paper models the automatic sliding-door controller as a hierarchical FSM rather than a flat IF-THEN ladder.
   对应摘录：A, B, C
2. 句子 2：A door-management FSM sends the command input `PROMACHINE_IN` to the motion-generator FSM, while the motion layer also reads actuator position and velocity related inputs and outputs reference acceleration, velocity, position, status, and diagnostic toggle information back to the rest of the controller.
   对应摘录：C
3. 句子 3：At the main level, the motion generator is organized around `init`, `positive`, `negative`, and `stop`, and the motion states are then refined into sub-levels instead of being kept flat.
   对应摘录：C
4. 句子 4：In the `positive` direction, the first sub-level switches across eight motion-profile sectors, and the second sub-level finishes the detailed motion equations for states such as `S20`, so the paper preserves both the high-level travel mode and the lower-level sector computation chain.
   对应摘录：C
5. 句子 5：During normal operation, if the door motion is forcefully interrupted by an obstacle or another movement-prevention condition, the FSM enters blockade detection, reverses direction when possible, and finally stops with an error indication after three consecutive failed attempts.
   对应摘录：D
