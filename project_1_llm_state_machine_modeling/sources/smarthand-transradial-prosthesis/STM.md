# The SmartHand transradial prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `HLHC -> LLMC` 的层次控制架构、`force control / position control / sleep mode` 多模式低层控制、双 FSM 并发驱动，以及 `preshaping -> grasping` 的自动抓握序列，可直接作为层次化假手控制样本。

## 条目 1: Hierarchical grasp-and-power supervisor for the SmartHand prosthesis
- 控制对象：`SmartHand` 经桡假手的高低层协同控制架构
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `HLHC` 调度两个 `LLMC`、并在低层为各电机运行双有限状态机以完成模式切换、抓握序列和电源管理的智能假手控制器。
- 判断：算。对象是真实假手控制系统，不是接口协议本身；原文明确给出层次控制分工、低层模式集合、模式切换触发、自动抓握阶段序列和功耗/错误管理职责，能够恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section describing the four-axis control architecture
> A modular hierarchical architecture ... based on a high-level hand controller (HLHC) and two low-level motor controllers (LLMCs) has been selected. Both LLMCs ... are associated to two actuators whilst the host HLHC is in charge of the general functionality of the prosthesis. The HLHC ... communicates through a fast serial peripheral interface (SPI) bus with the slave LLMCs ...

#### 摘录 B
- 出处：第 8 页，Section describing the internal software
> The main function of the internal software implemented in the LLMC is to provide all the necessary low-level motor control functions (i.e. force control, position control modes, sleep mode). Therefore the microcontroller acts as a double finite-state machine (one for each motor) where the transitions between the different modes are triggered by HLHC commands coming from the SPI2 bus. The HLHC is in charge of sequencing LLMC functions to obtain meaningful operation of the hand (i.e. grasps and gestures) ... to manage power modes and handle errors.

#### 摘录 C
- 出处：第 8 页，same section
> Commands are divided into three main types: motor commands (for driving fingers in position or force control), sensor readings and automatic grasps. ... Internal control loops ... update errors every 1 ms ... Automatic grasps are modelled on natural grasping. ... two different phases are sequenced by the HLHC: the preshaping and the grasping (closure) phase. After preshaping the desired finger tendon force is selected according to the grasping primitive. In the second phase, the prosthesis closes the involved fingers ... using tendon tension force control until the desired global tight force is reached.

### 2. 基于原文整理后的自然语言描述

The SmartHand prosthesis uses a hierarchical control architecture in which one `HLHC` supervises two `LLMC` boards, while each `LLMC` manages the local actuation behavior of its assigned motors. At the low level, each controller acts as a double finite-state machine, one FSM per motor, and the available modes explicitly include `force control`, `position control`, and `sleep mode`, with transitions triggered by `HLHC` commands over the `SPI2` bus. The high-level controller does not merely relay commands: it sequences low-level mode changes into meaningful hand behaviors such as grasps and gestures, manages power modes, and handles error conditions across the prosthesis. Automatic grasps are themselves structured as a two-phase sequence, with `preshaping` first selecting the posture and desired tendon force for the chosen grasp primitive, followed by `grasping` or closure under tendon-tension force control until the desired global tight force is reached. Because the architecture coordinates multiple low-level FSMs under one higher-level sequencer, it forms a hierarchical and parallel prosthetic-hand supervisor rather than a single flat motor controller.

### 3. 逐句溯源

1. 句子 1：The SmartHand prosthesis uses a hierarchical control architecture in which one `HLHC` supervises two `LLMC` boards, while each `LLMC` manages the local actuation behavior of its assigned motors.
   对应摘录：A
2. 句子 2：At the low level, each controller acts as a double finite-state machine, one FSM per motor, and the available modes explicitly include `force control`, `position control`, and `sleep mode`, with transitions triggered by `HLHC` commands over the `SPI2` bus.
   对应摘录：B
3. 句子 3：The high-level controller does not merely relay commands: it sequences low-level mode changes into meaningful hand behaviors such as grasps and gestures, manages power modes, and handles error conditions across the prosthesis.
   对应摘录：B
4. 句子 4：Automatic grasps are themselves structured as a two-phase sequence, with `preshaping` first selecting the posture and desired tendon force for the chosen grasp primitive, followed by `grasping` or closure under tendon-tension force control until the desired global tight force is reached.
   对应摘录：C
5. 句子 5：Because the architecture coordinates multiple low-level FSMs under one higher-level sequencer, it forms a hierarchical and parallel prosthetic-hand supervisor rather than a single flat motor controller.
   对应摘录：A, B, C
