# Presentation of Control Algorithm for Cooling System in Business Building - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把楼宇冷却系统的手动/自动模式、外温驱动的制冷单元切换、供水泵联锁和阀门定时动作写成了完整 PLC/SCADA 控制链，可稳定支撑双 A 样本。

## 条目 1: Auto-Manual Cooling Supervisor with Ambient-Temperature Handover and Timed Valve Sequencing

- 控制对象：楼宇机电领域的商用建筑双回路冷却系统 PLC 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 PLC、HMI 和 SCADA 的楼宇冷却系统监督控制器，负责在 air-cooled chiller 与 dry cooler 之间切换，并联动 flow pump、butterfly valves 和 three-way valve 完成安全冷却运行。
- 判断：算。对象是真实商用建筑冷却系统，原文明确给出了 manual/automatic 两种模式、外温阈值驱动的冷却单元切换、供水泵停启联锁、阀门开闭时序以及 memory bit / timer 级程序事实。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 35-35 行
> This paper presents an algorithm for controlling and monitoring a cooling system in a business building by using the human-machine interface (HMI). The computer program for automatic control was implemented by using the ©SIEMENS TIA portal computer program. Based on the previously created hydraulic schema of the system, a ladder diagram was created, which was stored in the PLC with the aim of further automatic system control. In addition, a SCADA system was implemented to monitor all the processes of the cooling system under consideration. The control system is designed as a remote-control system with the possibility of adjusting and monitoring the system from a remote location via a computer or mobile device.

#### 摘录 B

- 出处：第 2 页，`Literature review / contribution`，`paper_content.txt` 第 134-144 行
> The contribution of this paper is as follows:
> • The control system with a PLC controller and SCADA system has an implemented PID algorithm. It is controlled with electric actuators on the elements in the field (dampers and three-way valves). The parameters of the PID controller are set automatically via a separate subprogram in the system.
> • The control system has the option of switching the operating modes from the standard cooling method to the dry cooling method and vice versa. This can be done manually or automatically.
> • The system can be controlled with a remote control and monitored via a computer or mobile device from another location.

#### 摘录 C

- 出处：第 3 页，`Description of proposed automatic control system`，`paper_content.txt` 第 189-224 行
> The system is controlled by a programmable logic controller (PLC) via ethernet communication. The PLC collects all data from the entire system and, depending on it, controls the operation of the system and processes. A provided installation of eight temperature sensors and two pressure sensors in the system is ensured.
>
> The control system is carried out in such a way that the system control mode can be selected on the control screen, either manually or automatically. The manually selected mode means that the desired air-cooled chiller is selected, through which the system's cooling is to be switched on. In this case, it is either the dry cooler or an air-cooled chiller that is switched on by clicking the ON/OFF button on the screen. When the desired device is switched on, the cooling process begins. If everything goes well and without errors, the flow pump is also switched on, which starts automatically when one of the devices mentioned is in operation.
>
> If automatic control mode is selected, the ambient temperature detected by the temperature sensor is considered. If the ambient temperature is higher than zero, the system operates in summer mode, and the air-cooled chiller is switched on. If the temperature is below zero or falls below zero while cooling and the air-cooled chiller is switched on, the chiller is switched off, and the dry cooler is switched on. During this period of switching the other cooling unit off and on, the supply pump is switched off to prevent excessive pressure and possible damage caused by this pressure. When the second cooling device starts cooling, and if everything is in order and there are no faults in the system, the flow pump resumes its work.

#### 摘录 D

- 出处：第 5-6 页，`Dry cooler program / Butterfly valve program / Mode selection program`，`paper_content.txt` 第 357-395 行、第 420-426 行
> The control program for the dry cooler is shown below (Figure 5). The program for the air-cooled chiller and the flow pump was based on the same principle, so this paper does not show these parts of the program in detail.
>
> The block in Figure 5 serves to turn on the power supply to the dry cooler. It contains the memory bit M21.0, which turns the power on and off depending on its logic state. In addition, there is a MOVEJOG_DB data block (Figure 6), whose activation also uses the memory bit M21.1, which is a status bit from the MC_POWER data block and serves as a confirmation bit that the power is on and that the refrigerator compressor can start to work.
>
> In addition, there is a block for defining all conditions (Figure 7) so that the dry cooler functions correctly and safely. The logical values of the memory bits of individual states of the system define the current phase in which the system is in but also define the condition under which the further process runs when a new change occurs.
>
> This program line (Figure 8) shows the conditions required for the throttle valves to function properly. The program prompts you to open and close these dampers. ... You can choose between manual and automatic control modes in the control system.
>
> Therefore, each damper requires a certain amount of time to open and close, which is provided by the TON and TOF timers.
>
> The program (Figure 11) is used to select the cooling mode when the automatic control mode is selected. It takes place and is determined according to the value of the outside temperature. If the outside temperature is below zero, dry cooling is switched on; if the temperature is above zero, water cooling is switched on.

### 2. 基于原文整理后的自然语言描述

The building cooling supervisor is organized around manual and automatic HMI/SCADA modes for a dual-circuit plant that includes an air-cooled chiller, a dry cooler, a flow pump, butterfly valves, a three-way valve, and multiple temperature and pressure sensors connected to a PLC. In manual mode the operator explicitly selects whether the dry cooler or the air-cooled chiller is energized from the screen, and once the chosen cooling device starts without faults, the flow pump is allowed to run under differential-pressure supervision. In automatic mode the PLC evaluates the outside temperature, keeps the system in summer mode with the air-cooled chiller when ambient temperature stays above zero, and performs a handover to dry cooling whenever the outside temperature falls below zero during operation. During this cooling-unit handover the supply pump is switched off to avoid excessive pressure, and it resumes only after the second unit is cooling normally and the system reports no faults. The ladder program further encodes this supervisory sequence with dry-cooler power and confirmation bits `M21.0` and `M21.1`, phase-defining memory bits, and TON/TOF timer blocks that delay butterfly-valve opening and closing so media routing stays synchronized with the selected cooling mode.

### 3. 逐句溯源

1. 句子 1：The building cooling supervisor is organized around manual and automatic HMI/SCADA modes for a dual-circuit plant that includes an air-cooled chiller, a dry cooler, a flow pump, butterfly valves, a three-way valve, and multiple temperature and pressure sensors connected to a PLC.
   对应摘录：A, B, C
2. 句子 2：In manual mode the operator explicitly selects whether the dry cooler or the air-cooled chiller is energized from the screen, and once the chosen cooling device starts without faults, the flow pump is allowed to run under differential-pressure supervision.
   对应摘录：C
3. 句子 3：In automatic mode the PLC evaluates the outside temperature, keeps the system in summer mode with the air-cooled chiller when ambient temperature stays above zero, and performs a handover to dry cooling whenever the outside temperature falls below zero during operation.
   对应摘录：B, C, D
4. 句子 4：During this cooling-unit handover the supply pump is switched off to avoid excessive pressure, and it resumes only after the second unit is cooling normally and the system reports no faults.
   对应摘录：C
5. 句子 5：The ladder program further encodes this supervisory sequence with dry-cooler power and confirmation bits `M21.0` and `M21.1`, phase-defining memory bits, and TON/TOF timer blocks that delay butterfly-valve opening and closing so media routing stays synchronized with the selected cooling mode.
   对应摘录：D
