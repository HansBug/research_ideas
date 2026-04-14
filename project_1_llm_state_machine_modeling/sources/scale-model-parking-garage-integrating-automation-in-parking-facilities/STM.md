# Scale Model Parking Garage: Integrating Automation in Parking Facilities - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束 / 以事件推进为主）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `MAIN / AUTO_MODE / MAN_MODE` 的顶层程序组织、停车/取车顺序、HMI 模式切换、急停与故障停机逻辑、以及整套验证流程都写得很完整，可作为停车设施领域的双 A `HSM + T0` 样本。

## 条目 1: Circular Parking Garage Auto/Manual Supervisor

- 控制对象：智慧停车与车位管理领域的环形车库自动/手动分层控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束 / 以事件推进为主）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Beckhoff PLC、TwinCAT、HMI、伺服轴和步进轴的环形立体车库控制器，上层在自动停车/取车与手动调试之间切换，下层负责楼层定位、旋转与安全停机。
- 判断：算。对象是真实停车装置控制系统，原文明确给出程序层级、操作模式、按钮与变量、故障/急停响应，以及整条停车/取车顺序的验证结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 22-24 页，`5 Software implementation / 5.1 PLC project structure and task configuration / 5.2 Input output configuration`，`paper_content.txt` 第 527-556 行、第 563-581 行
> Figure 12 shows, the main Program Organization Units (POUs) structure for the project. Each POU has a specific purpose in the control system: MAIN (PRG) ... AUTO_MODE (PRG): Controls the automatic parking and retrieval sequence. MAN_MODE (PRG): Allows manual operation for troubleshooting, testing, or calibration. ... The PLC program uses a cyclic task that runs the main logic at a fixed interval to ensure reliable and smooth operation.
>
> System states and user commands are represented by the variables ‘AutoMode’, ‘ExitBtn’, ‘EntryBtn’, ‘ManualMode’, and ‘ResetButton’. ... Figure 15 shows how these button inputs are logically assigned to different control functions, such as reset, manual/auto mode selection, and motor control actions (stop, up, forward, open, down, reverse, and close).

#### 摘录 B

- 出处：第 28-30 页，`6 HMI implementation / 6.2 System design and navigation`，`paper_content.txt` 第 642-699 行、第 703-716 行
> The HMI directly allows operator commands and reads and writes PLC variables, such as retrieval, start, stop, and parking commands ... feedback, including slot availability and motor status, are displayed to the user.
>
> The Manual Mode section allows individual mechanical movements ... vertical movement, horizontal or rotational movement, door control ... An ‘emergency stop’ button is prominently placed within the manual control area for immediate shutdown.
>
> The ‘Automatic Mode’ section is designed for normal automatic parking and retrieval ... a numeric input field for entering the desired parking slot number ... Entry and Exit command buttons to initiate parking or retrieval sequences ... Once a slot number is entered, the PLC executes a predefined control sequence that manages parking slot positioning, rotation and the vehicle movement automatically.
>
> Interlocking logic plays a vital role within the PLC to confirm that only one mode can be active at a time.

#### 摘录 C

- 出处：第 31-35 页，`7 Safety system implementation / 8 Testing and validation / 8.4 Parking and retrieval sequence testing / 8.5 Safety system testing`，`paper_content.txt` 第 724-749 行、第 811-857 行
> When the emergency stop button is pressed, it immediately deactivates all drives of the motors and halts system operation. ... If any fault detects during operation the system disables further motion commands and immediately stops the affected motor.
>
> Parking and retrieval sequence testing ... covers all major stages of the control logic such as including vehicle entry detection, slot number evaluation, platform rotation direction selection, vertical floor level positioning, and vehicle retrieval execution.
>
> The PLC controller first determines the target floor position based on the selected slot number. Slots are grouped into ranges. Each range corresponds to predefined vertical target position ... Figure 19 shows, the rotation direction of the platform was dynamically selected according to the slot number. Specific slots are activated by reverse rotation or skip rotation command and remaining slots are activated by forward rotation.
>
> Fault scenarios, such as incomplete motion and incorrect positioning signals are introduced to verify that the controller responded safely and halted the sequence when required. ... the whole system restarts only possible after the fault is cleared and safety conditions are restored.

### 2. 基于原文整理后的自然语言描述

The Beckhoff TwinCAT controller is organized as a hierarchical parking-garage supervisor with `MAIN` at the top, `AUTO_MODE` and `MAN_MODE` as mutually exclusive operating branches, and dedicated function blocks for the servo and stepper axes. In automatic mode the operator enters a parking slot number and issues `Entry` or `Exit`, after which the PLC executes a predefined sequence for floor positioning, platform rotation, and vehicle handling; in manual mode the same mechanical axes and door functions can be driven individually for setup or troubleshooting. Global variables such as `AutoMode`, `ManualMode`, `EntryBtn`, `ExitBtn`, and `ResetButton` together with speed-selection parameters govern mode switching, command initiation, and motion tuning. The controller also couples emergency-stop and motor-fault signals into the motion supervisor so any unsafe condition overrides commands, disables motor outputs, and forces the system into a safe state. During validation the thesis explicitly checks floor-range selection, slot-based rotation direction, repeatability, wrong-position fault scenarios, and restart-after-fault behaviour, so the parking and retrieval control chain is recoverable and operationally concrete rather than just an HMI mock-up.

### 3. 逐句溯源

1. 句子 1：The Beckhoff TwinCAT controller is organized as a hierarchical parking-garage supervisor with `MAIN` at the top, `AUTO_MODE` and `MAN_MODE` as mutually exclusive operating branches, and dedicated function blocks for the servo and stepper axes.
   对应摘录：A
2. 句子 2：In automatic mode the operator enters a parking slot number and issues `Entry` or `Exit`, after which the PLC executes a predefined sequence for floor positioning, platform rotation, and vehicle handling; in manual mode the same mechanical axes and door functions can be driven individually for setup or troubleshooting.
   对应摘录：B
3. 句子 3：Global variables such as `AutoMode`, `ManualMode`, `EntryBtn`, `ExitBtn`, and `ResetButton` together with speed-selection parameters govern mode switching, command initiation, and motion tuning.
   对应摘录：A, B
4. 句子 4：The controller also couples emergency-stop and motor-fault signals into the motion supervisor so any unsafe condition overrides commands, disables motor outputs, and forces the system into a safe state.
   对应摘录：C
5. 句子 5：During validation the thesis explicitly checks floor-range selection, slot-based rotation direction, repeatability, wrong-position fault scenarios, and restart-after-fault behaviour, so the parking and retrieval control chain is recoverable and operationally concrete rather than just an HMI mock-up.
   对应摘录：C
