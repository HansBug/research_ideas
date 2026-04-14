# Wind Energy Conversion System under a Supervisor Deterministic Finite State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把并网风能转换系统的高层监督器明确写成 `Park / Start-up / Generating / Brake` 四态确定性 FSM，并用风速与发电机转速阈值管理并网、额定运行和停机。

## 条目 1: Four-state wind-turbine operational supervisor

- 控制对象：过程与环境控制领域的变速变桨 DFIG 风能转换系统运行状态监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个并网风能转换系统的高层运行模式监督器，用风速区间和发电机转速阈值在停机、启动、发电和制动之间切换。
- 判断：算。对象是真实能源转换控制系统；原文给出 FSM 模型、状态转移图、四个 operational states 的语义和状态相关执行效果，并用仿真比较 supervisor 开启前后的系统响应。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This paper presents a simulation of an onshore energy conversion system connected to the electric grid and under a strategy of a supervisor control based on deterministic version of a finite state machine. ... The supervisor is included at the higher level, having the objective of analyzing the operational states according to the wind speed.

#### 摘录 B

- 出处：第 1-2 页，Introduction
> The state of operation of a WECS can be classified according with the wind speed range into four regions of power operation. Region I: where the wind speed is less than the cut-in speed ... WT is in shut down. Region II ... maximize the capture of the kinetic energy from the wind. Region III ... operate at nominal generator speed, and pitch control is used ... Region IV ... the turbine is in shut down for safety purpose.

#### 摘录 C

- 出处：第 4 页，Section `B. Supervisor`
> The WECS supervisor is based on FSM also known by finite-state automaton or state machine. ... The supervisor deterministic version of a FSM used in this paper has the state transition diagram shown by Fig. 4. ... the operational states are park, start-up, generating and brake, typifying the regions of power operation.

#### 摘录 D

- 出处：第 4 页，Section `B. Supervisor`
> Park is a state on Region I where the WECS is in shutdown and the generator is disconnected from the electric grid. ... Start-up is a state on Region II ... The generator is connected to the electric grid ... This state can enter into the generating one or into the brake one according to the values for the wind speed and generator speed. ... Generating ... where the wind speed is not less than the rated wind speed and is lower than the cut-out speed. ... Brake state is a state in Region IV where the WECS is in shutdown and the generator is disconnected from the electric grid.

### 2. 基于原文整理后的自然语言描述

The WECS supervisor is a deterministic four-state FSM over `Park`, `Start-up`, `Generating`, and `Brake`, where the states map directly to wind-turbine operating regions. In `Park`, low wind keeps the turbine shut down and the generator disconnected; in `Start-up`, wind above cut-in starts the system and connects the generator while it is not yet necessarily at rated power. From `Start-up`, the supervisor can move to `Generating` or `Brake` according to wind-speed and generator-speed thresholds, and `Generating` represents rated-power Region III operation with nominal generator speed and pitch curtailment. When wind exceeds the cut-out region or the transition conditions leave the generating state, `Brake` shuts the WECS down and disconnects the generator, after which the supervisor can return to `Start-up` or `Park`. Although the low-level model is continuous and includes rotor speed, pitch and generator dynamics, the supervisory requirement is a compact FSM with explicit operational states, threshold guards and state-dependent grid-connection behavior.

### 3. 逐句溯源

1. 句子 1：The WECS supervisor is a deterministic four-state FSM over `Park`, `Start-up`, `Generating`, and `Brake`, where the states map directly to wind-turbine operating regions.
   对应摘录：B, C
2. 句子 2：In `Park`, low wind keeps the turbine shut down and the generator disconnected; in `Start-up`, wind above cut-in starts the system and connects the generator while it is not yet necessarily at rated power.
   对应摘录：B, D
3. 句子 3：From `Start-up`, the supervisor can move to `Generating` or `Brake` according to wind-speed and generator-speed thresholds, and `Generating` represents rated-power Region III operation with nominal generator speed and pitch curtailment.
   对应摘录：B, D
4. 句子 4：When wind exceeds the cut-out region or the transition conditions leave the generating state, `Brake` shuts the WECS down and disconnects the generator, after which the supervisor can return to `Start-up` or `Park`.
   对应摘录：B, D
5. 句子 5：Although the low-level model is continuous and includes rotor speed, pitch and generator dynamics, the supervisory requirement is a compact FSM with explicit operational states, threshold guards and state-dependent grid-connection behavior.
   对应摘录：A, B, C, D
