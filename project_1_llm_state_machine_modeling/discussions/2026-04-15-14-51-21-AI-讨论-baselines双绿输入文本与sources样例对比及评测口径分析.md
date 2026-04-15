# `baselines` 双绿输入文本形态、`sources` 样例对比与评测口径分析

## 1. 任务与本文结论

这份 discussion 回答 4 个紧密相关的问题：

1. `project_1` 里目前已经真正加载进来的双绿 baseline 数据集到底有哪些。
2. 这些 baseline 的**输入自然语言文本**长什么样，风格差异有多大。
3. 我们自己的 [sources](../sources/README.md) 文库里，当前最直接可用的自然语言输入样例是什么样，它和 baseline 到底像不像。
4. 如果 `project_1` 真的要做论文级实验，`sources` 现在这批自然语言描述到底够不够，评测又应该怎么设计。

先给结论，再展开证据。

### 1.1 结论先行

1. `sources` **足够支撑一类很扎实的学术实验**：`控制器级自然语言描述 -> 状态机/EFSM/HSM/带局部时间约束模型`。
2. `sources` **还不够支撑** `ttool-ai` 那种“长篇系统规格 -> 多 block 架构 + 多状态机面板”的系统级 MBSE 生成实验。
3. `sources` 当前最直接可用的输入，不是“原始工业需求原文”，而是每篇 `STM.md` 第 2 节里**基于原文重建后的自然语言描述**。这对实验是优点也是限制：
   - 优点：控制语义更集中，适合训练和对比。
   - 限制：如果论文要声称“直接从原始需求到模型”，那目前证据链还不够原生态。
4. 从输入文本形态上看，`sources` 处在 `llms_emp`、`Nimbus`、`Structure/Event-Driven` 三者之间：
   - 比 `llms_emp` 更真实、更控制工程化；
   - 比 `Nimbus` 更连续叙述、没有被拆成原子 requirement 规则；
   - 和 `Structure/Event-Driven` 一样都能做“单系统/单控制器状态机生成”，但 `sources` 更工业、更脏、更少现成 ground truth。
5. 如果 `project_1` 要做可发表实验，最稳的路线不是硬套某一个 baseline，而是**组合三层评测**：
   - 结构/语法正确性；
   - 组件级语义对齐；
   - 小规模执行/仿真/专家复核。

## 2. 本次分析绑定的本地资产

本文不泛指一个模糊的“baseline 世界”，而是明确绑定到当前仓库里已经落到本地、并且已经被整理成 `parquet` 的双绿数据资产。总入口是：

- [双绿数据集下载解析与 parquet 化记录](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md)
- [baseline_double_green_dataset_catalog.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/baseline_double_green_dataset_catalog.parquet)

当前确实已经加载进来的 4 组数据如下。

| baseline | 本地已加载资产 | 当前可直接观察的输入粒度 | 目标输出/参考模型 |
| --- | --- | --- | --- |
| `llms_emp` | [llms_emp_complete_samples.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_complete_samples.parquet) | `98` 个完整样本，其中 `stm = 38` | `PlantUML` 编码的 `SysML` 行为模型 |
| `ttool-ai` | [ttool_ai_models.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/ttool_ai_models.parquet)、[ttool_ai_state_machine_panels.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/ttool_ai_state_machine_panels.parquet) | `15` 份完整系统规格，对应 `122` 个状态机面板 | `TTool AVATAR design` 多 block 设计模型 |
| `Nimbus Light Control` | [light_control_nimbus_fragments.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/light_control_nimbus_fragments.parquet)、[light_control_nimbus_rules.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/light_control_nimbus_rules.parquet) | `4` 个重建后的需求片段 | `REQ / SOFT` 层 `RSML-e` 状态变量、规则和层次状态树 |
| `Structure/Event-Driven` | [structure_event_driven_cases.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_cases.parquet)、[structure_event_driven_reference_solutions.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_reference_solutions.parquet) | `9` 个英文问题描述 | `Umple` 状态机参考解 |

这 4 组数据已经足够覆盖 4 种很不一样的“自然语言到状态机/行为模型”的输入形态：

1. 短篇、近似图说式的行为描述；
2. 长篇系统规格；
3. 编号化需求规则；
4. 单系统反应式题目描述。

## 3. 四个双绿 baseline 的输入文本到底长什么样

下面每个 baseline 我都至少放 2 个真实例子。重点不是“摘几句看起来像状态机的话”，而是看：**输入文本天然要求模型做什么建模动作**。

---

## 3.1 `llms_emp`：中短文本、强提示式、很多样本已经“半状态机化”

入口材料：

- [llms_emp/paper_content.txt](../baselines/llms_emp/paper_content.txt)
- [llms_emp/DESC.md](../baselines/llms_emp/DESC.md)
- [llms_emp_complete_samples.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_complete_samples.parquet)

### 例 1：基础制动装置状态机

来源：`row_id = 2`

```text
1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations.
2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state.
3 After entering the braking state, the system transitions to the brake caliper clamping state.
```

这个输入的特点非常鲜明：

1. 第一行就明说“`This state machine model represents...`”，等于直接告诉模型“你现在要画状态机”。
2. `initial state / braking state / operational state` 这些状态名几乎已经直接给出来了。
3. `When ... / If ... / Once ...` 的触发词很密，迁移边也几乎已经口头写好。
4. 这种样本更像“把已有图意改写成自然语言”，而不是原始需求在前、建模在后的真实工程材料。

### 例 2：列车控制状态机

来源：`row_id = 54`

```text
1. The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal.
2. In the InMotion state, the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected.
3. When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.
4. Within the InMotion state, the system operates in three substates: Accelerating, Cruising, and Approaching, which represent different phases of the train's motion.
5. The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal.
6. If the system is in the Accelerating substate and approaches its destination, it transitions to the Approaching substate upon receiving the "Approached/Decelerate" signal.
7. The system in the Cruising substate transitions to the Approaching substate when it approaches the destination, triggered by the "Approached/Decelerate" signal.
8. The system enters the Accelerating substate when motion begins, marked by the "Entry/Accelerate" action.
9. In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.
10. The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.
```

这个例子比前一个复杂，但风格仍然很“友好”：

1. 叙述是严格按状态图组织的，不是按业务背景组织的。
2. `DoorsClosing / InMotion / Stopping / EmergencyStopping` 这些状态标签已经是模型语言，不再是需求语言。
3. 层次结构也直接写出来了：`Within the InMotion state ... three substates`.
4. 模型的工作更像“把已经很像状态机的说明转成 PlantUML/SysML 语法”。

### 对 `llms_emp` 输入文本的整体判断

如果只看 `stm` 子集，`llms_emp` 的输入最典型的特征是：

1. **中短文本**。本地统计里 `stm` 子集 `n = 38`，平均长度约 `874.4` 字符。
2. **编号化明显**。约 `63.2%` 的样本有明显的编号/分条结构。
3. **迁移提示词密**。`if_ratio = 0.368`，`when_ratio = 0.342`。
4. **很多样本已经带状态命名**。不是“从零抽象状态”，而是“从半结构化文本恢复状态机”。
5. **对 project 1 的启示**：它很适合作为“中等难度、结构友好”的外部 baseline，但不能把它当成真实工业需求的代表。

---

## 3.2 `ttool-ai`：长篇系统规格，目标不是单状态机，而是系统级 AVATAR 设计

入口材料：

- [ttool-ai/paper_content.txt](../baselines/ttool-ai/paper_content.txt)
- [ttool-ai/DESC.md](../baselines/ttool-ai/DESC.md)
- [ttool_ai_models.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/ttool_ai_models.parquet)

### 例 1：`platooning`

这是完整系统规格的一段真实输入。

```text
Platooning is a transportation technique that consists in grouping trucks or vehicles together to reduce CO2 emissions. A platoon consists of one or several vehicles, the first one in the platoon playing the role of the platoon leader, the other ones playing the role of followers.

1. A vehicle can create a platoon: this vehicle is then the leader of this platoon. This vehicle informs neighbour cars about this platoon by sending a platoon information message (position, speed, acceleration) every second. Once followers have joined, it regularly informs every half second the followers of its current situation (speed, acceleration, direction, selected lane). Whenever there is an important modification of speed / acceleration / direction / lane, the leader immediately informs the followers.

2. A follower can join a platoon only at the last position, i.e. behind all other vehicles of the platoon. When it joins the platoon, it informs the leader about this. When a follower wishes to leave the platoon, it informs all other vehicles of the platoon (with a "leave" message) and then brakes or changes of lane.

3. Leaders and followers use front and back cameras to detect the lanes and the distance to other vehicles. The distance between vehicles within a platoon is considered to be between a min and a max distance. If there is less than the min distance between two vehicles, then the first vehicle detecting this situation broadcasts the information to all others and all vehicles of the platoon must perform an emergency braking. If the distance between two vehicles v1 and v2 with v1 before v2 gets over max, then v2 and all the vehicles behind v2 have to leave the platoon. v2 is assumed to send the "leave" message.

In a more advanced version of the platooning system, the platoon can split i.e. a given follower can decide to become the leader of all the followers behind it.

Use at least 2 blocks and at most 10 blocks.
```

这个输入和 `llms_emp` 完全不是一个难度层级：

1. 它不是“一个状态机描述”，而是**一个分布式系统规格**。
2. 里面同时有角色、消息、频率、距离约束、异常处置、拓扑变化。
3. 最后一句还给了建模约束：`Use at least 2 blocks and at most 10 blocks.` 这已经不是普通状态机任务，而是 MBSE 任务。
4. 模型必须先做架构分解，再决定每个 block 下挂哪些状态机。

### 例 2：`space_based_system`

```text
A ground station needs to regularly monitor the safety data of a space-based system: 3D position, temperature, battery level, fuel quantity. For this, a ground station can send, via radio-frequencies, a TC (TeleCommand) to the space-based system. Once received by the RF receiver, the software of the space-based system gets the request for information. Data of TCs are ciphered. Once the software has deciphered data, it stores data in an intermediate buffer, and a task to handle this request is triggered. This task builds the answer by reading requested values from sensors. Once the answer packet has been built, it is first enciphered and then sent via a TM (TeleMetry) to the ground station, using the RF transmitter.

To ensure that the system does not crash, a microcontroller of this system is dedicated to execute a software task that checks, every 10ms, that all other software tasks of the space-based embedded system are still responsive. For this, a signal is sent to each task. If some of the tasks have not responded to this signal, then the whole system is restarted, apart from the watchdog.

Sometimes, while the software system is computing a TM, another TC is received. To avoid redundancy, the TM under construction is canceled: a new TM corresponding to the latest TC is computed and sent.

Last but not least, space-based systems are not well protected against high-energy particles. Such a particle can provoke a bit flip from 0 to 1, or the opposite. The memory is the most sensitive elements of the platform. Therefore, for each block of data the software writes into memory, an error correction code (CRC) of this block has to be computed by the software and stored into memory along with the data block. When this block is read, the corresponding CRC must also be read and checked.
```

这个例子再一次说明 `ttool-ai` 的输入特点：

1. 它不是面向“状态抽象”的文本，而是面向“系统设计理解”的文本。
2. 一个输入段落里同时揉进了 `RF receiver`、`software task`、`watchdog`、`TM/TC`、`CRC`。
3. 你很难说“这段话对应一个单状态机”；更准确地说，它对应**多个 block 协同**，每个 block 只负责其中一段行为。
4. 对 project 1 来说，这类 baseline 是“更高目标”的参考，不是可以直接一一对齐的同层 benchmark。

### 对 `ttool-ai` 输入文本的整体判断

本地统计里，`ttool-ai` 的规格文本 `n = 15`，平均长度约 `2297.0` 字符，明显长于其他三类。它的输入有 4 个关键特征：

1. **系统级，而非控制器级**。
2. **多角色、多部件、多接口**。
3. **一个输入对应多份状态机面板**，状态机只是输出的一部分。
4. **任务天然包含架构分解**，因此对实验设计的要求远高于 `llms_emp` 和 `Structure/Event-Driven`。

---

## 3.3 `Nimbus`：编号化 requirement 片段，极适合规则/变量/定时条件抽取

入口材料：

- [requirements-capture-and-evaluation-in-nimbus-light-control/paper_content.txt](../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/paper_content.txt)
- [light_control_nimbus_fragments.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/light_control_nimbus_fragments.parquet)
- [light_control_nimbus_rules.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/light_control_nimbus_rules.parquet)

### 例 1：房间状态层次相关需求

```text
U1: If a person occupies a room, the light has to be sufficient to move safely, if nothing else is desired by a chosen light scene.
U2: As long as the room is occupied, the actual chosen light scene has to be maintained.
U3: If the room is reoccupied within T1 minutes after the last person has left the room, the last chosen light scene has to be reestablished.
U4: If the room is reoccupied after more than T1 minutes since the last person has left the room, the standard light scene has to be established.
U11: If the outdoor light sensor or the motion detector of a room does not work correctly, the user has to be informed.
U12: The ceiling lights and the task light should be maintained by the control system depending on different light scenes.
FM1: Use daylight to achieve the desired light whenever possible.
FM3: If a room is unoccupied for more than T3 minutes, all lights must be switched off.
FM6: The facility manager can turn off any light in a room or hallway section that is not occupied.
FM7: If a malfunction occurs, the facility manager has to be informed.
FM8: If a malfunction occurs, the control system supports the facility manager by finding the reason.
```

### 例 2：占用与超时规则片段

```text
U1: If a person occupies a room, the light has to be sufficient to move safely, if nothing else is desired by a chosen light scene.
U2: As long as the room is occupied, the actual chosen light scene has to be maintained.
U3: If the room is reoccupied within T1 minutes after the last person has left the room, the last chosen light scene has to be reestablished.
U4: If the room is reoccupied after more than T1 minutes since the last person has left the room, the standard light scene has to be established.
U10: The value T1 can be set for each room separately (not by using the control panel).
FM1: Use daylight to achieve the desired light whenever possible.
FM3: If a room is unoccupied for more than T3 minutes, all lights must be switched off.
FM5: The value T3 can be set for each room separately.
FM6: The facility manager can turn off any light in a room or hallway section that is not occupied.
```

这两段非常典型：

1. 文本不是叙事体，而是**规则账本**。
2. `U1/U2/U3/FM1/FM3` 这种编号天然支持 requirement traceability。
3. `T1`、`T3`、`reoccupied`、`malfunction` 这些词让状态变量划分和规则定义几乎成为主任务。
4. 它对“状态机生成”的帮助方式，不是直接给你状态名，而是逼你去构造：模式、变量、超时条件、规则优先级。

### 对 `Nimbus` 输入文本的整体判断

本地重建片段只有 `4` 个，但风格非常稳定：

1. **短而规则化**，平均长度约 `732.5` 字符。
2. **不是自由自然语言**，而是需求条款的拼接。
3. **时间条件很强**，`time_ratio = 0.75`。
4. **极适合 requirement-to-formal-rule**，但不太像“用户会直接给模型的说明文”。

---

## 3.4 `Structure/Event-Driven`：单系统反应式题目，天然适合组件级 F1 评测

入口材料：

- [structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt)
- [structure_event_driven_cases.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_cases.parquet)
- [structure_event_driven_metrics.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_metrics.parquet)

### 例 1：`Printer`

```text
The printer has a master switch which turns the printer on or off. Once the printer is turned on, a user needs to log in before being able to print or scan a document. To login, a user taps her/his printer card on the printer's card reader. Each printer card has a unique ID. If the printer card is authorized, the user can either choose "scan" or "print". If the printer card is not authorized, a login error message is shown.
For the "print" option, the user presses the start button to print the user's first document in the user's print queue. If there is no document in the print queue, an error message is shown instead of performing the printing task. For the "scan" option, the user presses the start button for the printer to scan an original document, which was placed by the user in the automatic page feeder. The scan is sent to the user's email inbox. If the printer does not detect an original document, an error message is shown instead of performing the scanning task. When the printer is done printing or scanning, the user can print or scan the next document. The user may also stop the printing/scanning task at any time by pressing the stop button. The user is allowed to logoff either before or after a printing/scanning task but not while the printer is in the middle of a printing/scanning task.
If there is a paper jam, the printer will suspend the printing/scanning task to allow the user to clear the paper jam. The user may then either cancel the printing/scanning task or resume it. In case the printer runs out of paper during a printing task, the printer suspends the printing task to allow the user to resupply paper. The user may then either cancel the printing task or resume it.
```

### 例 2：`Chess Clock`

```text
The digital chess clock has six buttons (each of which corresponds to one event): flip, minus, plus, startStop, select, onOff.
After turning on the chess clock, players can iterate through all the predefined timings using the plus and minus buttons, and finally select the designated timing by the select button. A timing option has a predefined base time and an increment. The game then starts when the startStop button is pressed.
At any time before the game is started, the players can set the clock to match the actual seating of White and Black players using the flip button.
When the game is started, White's clock starts counting down until the flip button is pressed. At this moment, White's clock stops and receives a bonus time defined by the increment, and Black's clock starts counting down. If the flip button is pressed again, then the same procedure is applied with reversed colors.
Both clocks can be stopped by pressing the startStop button, while the game can be continued by pressing the startStop button again. If the clock of the current player counts down to zero, then a flashing flag shall appear on the screen. The chess clock can be turned off at any time by pressing the onOff button.
```

这类输入和前两类 baseline 很不一样：

1. 它是自然、完整、单系统的反应式描述。
2. 范围通常比较干净，不会像 `ttool-ai` 那样一下子扩成多 block。
3. 按钮、事件、守卫、恢复路径、并行/层次结构都可能出现。
4. 很适合拿来做“状态、迁移、守卫、动作”这些组件级的精细评测。

### 对 `Structure/Event-Driven` 输入文本的整体判断

本地统计里，这组样本 `n = 9`，平均长度约 `2302.0` 字符，和 `ttool-ai` 一样都比较长，但目标不同：

1. 它依然是**单系统/单题目**。
2. `if_ratio = 0.889`、`when_ratio = 0.889`、`time_ratio = 0.889`，说明反应式和定时条件极密。
3. 它不像 `Nimbus` 那样被拆成编号规则，也不像 `llms_emp` 那样已经接近状态图说明。
4. 如果只谈“输入自然语言对状态机生成是否友好”，它比 `llms_emp` 更真实，比 `ttool-ai` 更可评测。

## 4. `sources` 当前最直接可用的输入样例是什么样

如果 `project_1` 现在就要做实验，最直接可用的输入不是原始 `paper_content.txt`，而是每篇 `STM.md` 第 2 节的“基于原文整理后的自然语言描述”。这是一层很重要的现实前提：

1. 它们已经做过原文抽取、选择和压缩。
2. 它们比 raw paper 更适合作为 benchmark 输入。
3. 但它们也不是“零预处理原始需求”。

下面至少放 6 个真实例子，覆盖短平快、EFSM、定时、层次、联锁和通信型样本。

### 例 1：[automatic-elevator-controller/STM.md](../sources/automatic-elevator-controller/STM.md)

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel. In the normal workflow, the system starts from an ideal state, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving. The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival, so transitions such as `F1 -> MU2 -> F2`, `F2 -> MU3 -> F3`, `F3 -> MD1 -> F1`, and `F3 -> MD2 -> F2` are explicitly defined in the paper. The `hbrg` output distinguishes upward drive, downward drive, and stop conditions, while the reset signal forces the controller back to floor `1` regardless of the outstanding request context. Although the implementation is described in VHDL/FPGA terms, the underlying control object is still a concrete three-floor elevator supervisor rather than a generic hardware demo.
```

这个例子很接近 `llms_emp` 里的友好型状态机输入，但有两个更强的地方：

1. 它保留了输入、输出和复位语义，不只是状态名。
2. 它来自真实论文控制对象，不是纯教学题。

### 例 2：[creating-programmable-logic-control-program-for-a-storing-station/STM.md](../sources/creating-programmable-logic-control-program-for-a-storing-station/STM.md)

```text
The storing-station controller begins its storing cycle after power and conveyor start are enabled, then uses `C0` and `C1` to move an incoming pallet from the initial conveyor point to the pick-up point and pause the conveyor there. Each activation of `C1` increments the counting word `M4`, copies that value into `M3`, and thereby selects the target rack position for the current item. The arm subsystem is then driven by `FC3` and `FC5`: motor `Y` moves downward until `K0` is active, the gripper closes, the arm rises back to the upper line, and the cylinder extends so the pallet can be placed at the rack slot indexed by `M3`. After a `2` second delay with `Z` set, the gripper is released and the cylinder retracts, completing the placement cycle before the next item is processed. Once the station is full and `LEA` is enabled, the controller switches to the leaving sequence, starts from stored position `20`, and empties the rack back toward position `1`, so the overall controller behaves as a FIFO storing system with an explicitly modelled reverse retrieval routine.
```

这类样本已经明显不是 `llms_emp` 的“轻状态机化描述”了，而是：

1. 传感器、寄存器、功能块、执行器齐全。
2. 既有阶段链，也有变量驱动。
3. 还带显式时间 `2 second delay`。

它更像我们真正希望 `project_1` 解决的控制系统建模任务。

### 例 3：[intelligent-traffic-congestion-control-using-machine-learning-wireless-network/STM.md](../sources/intelligent-traffic-congestion-control-using-machine-learning-wireless-network/STM.md)

```text
The intelligent traffic-light controller is organized as a server-and-microcontroller loop in which cameras continuously send live road images to a server, and the server uses `Yolov3` plus `OpenCV` to classify emergency vehicles and count normal cars in each lane. The server then notifies the `ESP32 Nodemcu` controller, which directly drives the current traffic-light hardware and also communicates with the next traffic light through the wireless network. The first decision branch is emergency preemption: if an ambulance is detected on one side, the controller changes that side from red to green and simultaneously commands the next neighbor traffic light to green so the emergency vehicle can pass across successive intersections. The second branch is congestion relief: if one side has more than `10` waiting cars while the other sides are empty, that crowded side is switched to green automatically. If neither condition is satisfied, the system keeps looping, acquiring new images and preserving the ordinary traffic-light operation until one of the two rule conditions becomes true.
```

这个例子说明 `sources` 并不只有传统 PLC 样本，它还能覆盖：

1. 服务器 + 控制器 + 邻接设备通信；
2. 阈值规则；
3. 优先级决策；
4. 连续循环控制。

### 例 4：[liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md](../sources/liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md)

```text
The liquid-distribution supervisor begins in auto mode after the operator chooses a transfer destination and enters the requested quantity on the SCADA screen. If all pre-check interlocks are satisfied, the controller opens the suction, dispensing, and destination valves and then starts the pump to move liquid from the source tank to the selected receiver. The transfer is allowed to continue only while source level is decreasing and the line flow sensor confirms that liquid is moving; otherwise the controller pauses automatically by closing the opened valves and stopping the pump. Additional pause triggers include pump trip or dry run, missing valve-open feedback, manual override of other valves, and low source-tank level, after which the user must correct the interlock and restart the process. When the flow totalizer reaches the requested transfer quantity, the supervisor turns the pump off, closes the valves, and ends the operation as a completed transfer.
```

这个例子对 project 1 很关键，因为它展示了真正的**过程控制 supervisor** 风格：

1. 有 pre-check；
2. 有 interlock；
3. 有 pause/restart；
4. 有完成条件；
5. 几乎天然对应 `EFSM`。

### 例 5：[four-ir-sensor-based-automatic-control-of-railway-gate-using-microcontroller/STM.md](../sources/four-ir-sensor-based-automatic-control-of-railway-gate-using-microcontroller/STM.md)

```text
The railway-gate controller is an Arduino-based EFSM whose normal-open condition is represented by all four IR sensors `HIGH`, green LEDs `HIGH`, red LEDs `LOW`, buzzer `LOW`, and both gate servos commanded to the open angle. For a train approaching from the left, the first IR sensor becoming active drives the warning/closure branch: the road-side red LEDs turn on, the buzzer is set `HIGH`, and after the one-second servo-delay pattern the two servo motors move to the gate-closed angle. When the same train reaches the second IR sensor, the controller opens the crossing again by turning green LEDs on, turning red LEDs and buzzer off, and writing the open angle to the two servos. For a train approaching from the right, the third sensor executes the same close-and-warn branch as the first sensor, and the fourth sensor executes the same open-and-clear branch as the second sensor.
```

这个例子很适合做“左右对称分支 + 显式局部定时”的实验，优点是：

1. 分支清楚；
2. 变量/执行动作清楚；
3. 计时行为明确；
4. 很适合和 `Nimbus` 或 `llms_emp` 的简单样本拉开难度层次。

### 例 6：[modular-hybrid-architecture-autonomous-urban-driving/STM.md](../sources/modular-hybrid-architecture-autonomous-urban-driving/STM.md)

```text
The Sting Racing urban-driving supervisor is modeled as a nested hybrid automaton whose highest mission layer switches among the six major modes `Follow Lanes`, `Overtake Static Obstacle`, `U-Turn`, `Handle Intersection`, `Park`, and `Unpark`. Inside `Follow Lanes`, the controller further refines behavior into `Follow Lane`, `Overtake`, `Blocked`, and `Blind`, and the `Blocked` state does not merely describe a condition: it explicitly transitions to `Overtake` after a parameterized dwell time if the obstruction persists. The hierarchy continues at intersection level, where the machine cycles through `Approach`, `Find Queue Position`, `Wait For Turn`, `Go`, and `Done`, and the formal NHA section later rewrites the same logic as nested automata with states such as `approach-intersection`, `establish-precedence`, `wait-for-precedence`, `wait-for-oncoming-traffic`, and `traverse-intersection`. The `traverse-intersection` node itself contains a deeper submachine including `go`, `follow-points`, and `follow-lanes-in-intersection`, so the design is not a flat FSM but a true layered HSM. Each discrete state is mapped onward to action selections for the behavior-arbitration block, which means the hierarchy is directly tied to continuous steering and velocity commands rather than being a stand-alone planner sketch.
```

这个例子说明 `sources` 并不只支持简单 `FSM/EFSM`，它还能覆盖：

1. 层次结构；
2. 子机；
3. 参数化定时；
4. 连续控制耦合。

也就是说，只要实验目标不是 `ttool-ai` 那种完整系统架构合成，`sources` 的上限其实不低。

## 5. baseline 与 `sources` 到底像不像

先用几个粗指标看整体差异，再做解释。

### 5.1 粗统计对比

这里的 `sources` 统计对象，是当前可直接做主实验集的 `STM.md` 第 2 节自然语言描述子集，尤其关注 `double-A` 且 `T0/T1` 的主流可用样本。

| 文本族 | 样本数 | 平均字符数 | 中位字符数 | 编号化占比 | `if` 占比 | `when` 占比 | 时间词占比 | 典型感觉 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `llms_emp_all` | `98` | `961.2` | `959` | `0.612` | `0.245` | `0.204` | `0.071` | 中短、分条、图意改写感强 |
| `llms_emp_stm` | `38` | `874.4` | `849` | `0.632` | `0.368` | `0.342` | `0.105` | 中短、显式状态迁移 |
| `ttool_ai_specs` | `15` | `2297.0` | `2132` | `0.333` | `0.667` | `1.000` | `0.667` | 长篇系统规格、多角色多部件 |
| `nimbus_fragments` | `4` | `732.5` | `730` | `0.000` | `0.750` | `0.000` | `0.750` | requirement 规则片段 |
| `structure_event_cases` | `9` | `2302.0` | `1964` | `0.000` | `0.889` | `0.889` | `0.889` | 单系统反应式题目 |
| `sources_double_A_T0_T1` | `660` | `1077.8` | `1080` | `-` | `0.312` | `0.589` | `0.311` | 工业控制导向的整理描述 |

### 5.2 `sources` 最像谁

如果问“`sources` 最像哪一种 baseline”，答案不是单选，而是分层次：

1. **长度和复杂度上**，`sources` 介于 `llms_emp` 和 `Structure/Event-Driven` 之间。
2. **控制语义密度上**，`sources` 比 `llms_emp` 更像真实控制器，尤其在传感器、执行器、联锁、异常恢复方面更强。
3. **规则化程度上**，`sources` 没有 `Nimbus` 那么原子化；它仍然是“压缩后的自然语言段落”，不是“编号 requirement 列表”。
4. **系统级分解需求上**，`sources` 明显弱于 `ttool-ai`，因为大多数条目针对的是单个 supervisor/controller，而不是多 block 体系。

### 5.3 和 `llms_emp` 的差别：`sources` 更真实，但也更难

拿 [automatic-elevator-controller/STM.md](../sources/automatic-elevator-controller/STM.md) 和 `llms_emp` 的制动装置例子比，能看出一个关键差别：

1. `llms_emp` 经常直接写“从某状态转到某状态”。
2. `sources` 更常写“控制器利用哪些输入、输出、模式和恢复逻辑来运作”。
3. 也就是说，`sources` 不是直接把图翻译成句子，而是保留了更多控制因果链。

这意味着：

1. 如果目标是做“文到图”的漂亮结果，`llms_emp` 更容易。
2. 如果目标是做“从真实控制描述抽象出状态机”，`sources` 更有研究价值。

### 5.4 和 `Nimbus` 的差别：`sources` 适合控制器生成，但不天然适合规则表重建

`Nimbus` 的优势不在“文本自然”，而在“条款可追踪”。例如 `U3/U4/FM3` 天生支持：

1. `T1/T3` 变量抽取；
2. 状态变量分解；
3. 条件表重建；
4. 规则优先级讨论。

而 `sources` 的第 2 节描述虽然也能保留这些信息，但通常已经被融合成连贯段落。比如：

1. [liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md](../sources/liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md) 非常适合生成 `EFSM`。
2. 但如果你要恢复成 `Nimbus` 式的 `target_variable / assigned_value / condition` 规则表，仍然需要额外拆句和归一化。

所以：

1. `sources` 更适合“控制器级模型生成”。
2. `Nimbus` 更适合“规则级 formalization”。

### 5.5 和 `Structure/Event-Driven` 的差别：`sources` 更工业，但 ground truth 更缺

`Structure/Event-Driven` 的 `Printer`、`Chess Clock`、`Thermomix` 这类例子有一个巨大优势：**每个题目都有干净的专家参考解**。这让它天然适合做：

1. 状态 F1；
2. 迁移 F1；
3. 守卫 F1；
4. 层次/并行/历史状态 F1。

而 `sources` 的现实情况是：

1. 输入文本其实已经足够 rich；
2. 但大量条目没有现成的 canonical ground truth 状态机；
3. 所以它现在更像“一个很好的实验原矿”，而不是“已经封装好的 benchmark”。

换句话说，`sources` 缺的主要不是输入文本，而是**统一金标准和统一评测层**。

### 5.6 和 `ttool-ai` 的差别：当前 `sources` 还不够系统级

这一点必须讲清楚，否则实验目标会飘：

1. `ttool-ai` 的输入经常要求模型先决定 block 划分，再在每个 block 里生状态机。
2. 我们 `sources` 里的主流条目，大多已经隐含“主控制器是谁”。
3. 因此拿 `sources` 去和 `ttool-ai` 的系统架构生成结果硬比，会天然吃亏，也不公平。

这不代表 `sources` 弱，而是代表它的研究目标更聚焦：

1. 它更适合做 controller-level 建模；
2. 不适合直接做 full MBSE architecture synthesis。

## 6. `sources` 是否足够支撑这样的学术实验

### 6.1 足够支撑的部分

如果你的论文目标是下面这类，`sources` 已经足够强：

1. **自然语言描述 -> `FSM/EFSM/HSM` 状态机生成**。
2. **自然语言描述 -> 守卫/动作/状态/时间约束抽取**。
3. **跨领域泛化实验**：电梯、交通灯、铁路道口、液体转运、自动驾驶、机械臂、包装线。
4. **按类型分层的 ablation**：`FSM`、`EFSM`、`HSM`、`T1`、协议交互、显式时钟。
5. **现实感更强的 benchmark**：比 `llms_emp` 更贴近控制工程，比 `Structure/Event-Driven` 更贴近工业对象。

### 6.2 目前还不够的部分

如果你的论文目标是下面这类，`sources` 还需要补层：

1. **原始需求直接建模**。
   现在最直接输入是 `STM.md` 第 2 节整理描述，不是原始需求全文。
2. **系统级多 block 架构生成**。
   当前 `sources` 大多不是 `ttool-ai` 那种系统规格。
3. **完全自动化 benchmark**。
   没有统一的 canonical reference model，就很难像 `Structure/Event-Driven` 那样直接算组件级 F1。
4. **REQ 规则表恢复型实验**。
   若要接近 `Nimbus`，还需要把当前连贯段落进一步拆成原子 requirement 或规则项。

### 6.3 我的判断：足以支撑一篇像样的 `project_1` 论文，但要把 claim 讲准

最稳妥的说法不是：

`我们从原始工业需求直接生成了高可信状态机`

而是：

`我们基于真实论文证据整理出控制器级自然语言描述语料，并在此基础上研究面向控制系统状态机的生成、验证与修复`

这个 claim 更稳，也更符合仓库现状。

### 6.4 对 `sources` 文库的具体治理建议

如果目标是让它真正变成论文级 benchmark，我建议立刻做 5 件事：

1. **建立核心金标准子集**。
   先从 `double-A` 条目里挑 `50-80` 个，给出统一目标模型。
2. **保留双层输入**。
   一层是当前 `STM.md` 第 2 节整理描述，另一层是更贴近原始 evidence 的 requirement/excerpt 层。
3. **按类型分桶**。
   至少按 `FSM / EFSM / HSM / T1 / T2 / 协议交互 / 显式时钟` 建立标签。
4. **明确实验主赛道**。
   当前最值得做的是 `controller-level NL -> pyfcstm/状态机`，不要一上来挑战 `ttool-ai` 式系统级任务。
5. **准备小规模手工评测集**。
   选 `15-20` 个高价值样本做人工专家评分和执行验证，形成论文里的强证据。

## 7. 重点双绿 baseline 是怎么评“生成质量”的

下面把四篇工作逐个拆开。重点回答 3 个问题：

1. 评什么。
2. 怎么评。
3. 是人工、自动，还是混合。

---

## 7.1 `llms_emp`：自动语法检查 + 手工语义检查 + 参考模型对齐 F1

证据入口：

- [llms_emp/paper_content.txt](../baselines/llms_emp/paper_content.txt)
- [llms_emp/DESC.md](../baselines/llms_emp/DESC.md)

### 评测对象

这篇工作评的是：`LLM 生成 SysML 行为模型的能力`。它不是只看状态机，还同时覆盖 `activity` 和 `sequence diagram`。

### 评测维度

论文里把评测拆成 4 类检查：

1. `PlantUML format checking`
2. `SysML grammar checking`
3. `SysML semantic checking`
4. `Requirements semantic checking`

其中报告的核心指标是 4 个：

1. `T_G`：生成时间
2. `Acc_P`：`PlantUML` 格式准确率
3. `Acc_S`：`SysML` 语法准确率
4. `F1-score`：生成模型与参考模型的语义一致性

### 自动化和人工分别在哪里

1. `PlantUML format checking` 是**自动**的，由 `PlantUML` 模型检查器给结果。
2. `SysML grammar checking` 是**人工**的，因为 `PlantUML` 没有 `SysML grammar checker`。
3. `SysML semantic checking` 也是**人工**的，论文里说是对照 `55` 条语义规则记录违例。
4. `Requirements semantic checking` 用参考模型对比，最终用 `F1-score` 量化。

### 这个 baseline 给我们的启示

它的价值在于提供了一套很完整的“**语法 + 语义 + 参考对齐**”思路，但它也有两个边界：

1. 它的很多输入文本已经比较“图友好”。
2. 语法/语义检查里人工成分不低，说明即便是这篇论文也没有完全自动评测。

---

## 7.2 `ttool-ai`：教师式综合评分，混合了可执行性、可读性和设计质量

证据入口：

- [ttool-ai/paper_content.txt](../baselines/ttool-ai/paper_content.txt)
- [ttool-ai/DESC.md](../baselines/ttool-ai/DESC.md)

### 评测对象

它评的不是“生成一个状态机对不对”，而是“**从长篇系统规格自动生成系统设计模型**”的整体质量。

### 怎么评

论文把同一批系统规格给了大约 `15` 名硕士生：

1. 他们先接受了 `21` 小时教学；
2. 然后有 `1.5` 小时完成建模；
3. `TTool-AI` 和学生都用**同一套打分标准**。

### 评分标准是什么

论文明确提到，评分遵循软件工程质量标准，至少包括：

1. 架构/行为是否符合规格；
2. 在 `TTool simulator` 里观察到的行为是否符合规格；
3. block 间交换数量是否合理；
4. 图是否可读；
5. block 数量、状态数量、命名是否一致；
6. 是否存在声明了但没在状态机里使用的属性；
7. `TTool syntax checker` 报出的错误和警告数量。

### 自动化和人工分别在哪里

1. `syntax checker` 和 `simulator` 提供了一部分**自动/半自动证据**。
2. 但整体评分本质上仍然是**人工 rubric 评分**，而且很像课程作业评分。
3. 它没有像 `Structure/Event-Driven` 那样细到“状态 F1、守卫 F1”。

### 这个 baseline 给我们的启示

1. 如果研究目标是系统级设计生成，单看状态机 F1 远远不够。
2. 但对 `project_1` 当前阶段来说，这套评法太重，也太偏系统架构。
3. 我们可以借它的**可执行性检查**和**命名/一致性检查**思路，但不必照搬它的整套目标。

---

## 7.3 `Nimbus`：不是 LLM benchmark，而是“执行、仿真、验证”型评估框架

证据入口：

- [requirements-capture-and-evaluation-in-nimbus-light-control/paper_content.txt](../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/paper_content.txt)

### 它评的其实不是“生成质量”

严格说，`Nimbus` 这篇不是在做 LLM 生成评测。它做的是：

1. 需求捕获；
2. 形式化建模；
3. 执行/仿真/验证。

### 它的评估思路

论文把验证和确认分成三类：

1. `manual inspections`
2. `formal verification`
3. `simulation and testing`

并明确说这三者必须联合使用。

### 论文重点强调的是什么

这篇文重点不在指标，而在**执行环境**：

1. `REQ` 关系可以直接执行；
2. 输入可以来自文本文件、用户交互、Excel 环境模型；
3. 可以做日志记录和回放；
4. 可以逐步把传感器模型、执行器模型、过程模型接进来；
5. 最后还能做 `hardware-in-the-loop`。

### 这意味着什么

1. 它几乎没有 `precision/recall/F1` 这种 benchmark 指标。
2. 它更像“模型质量通过仿真场景暴露问题”的范式。
3. 对 `project_1` 的价值不在于拿来直接对比分数，而在于提醒我们：**生成之后必须有执行/验证层**。

---

## 7.4 `Structure/Event-Driven`：人工组件匹配，按 7 类状态机组件算 `P/R/F1`

证据入口：

- [structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt)
- [structure_event_driven_metrics.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_metrics.parquet)

### 评测对象

这篇工作非常直接：比较不同生成策略生成的状态机，与专家给定的参考解有多接近。

### 怎么评

论文明确说，**没有可用的自动 evaluator**，所以采用人工评估。核心原因是：

1. 同一个自然语言题目，可能有多个等价状态机设计；
2. 名字不同，不代表行为不同；
3. 自动做语义等价判定非常难。

于是他们采用：

1. 单作者对某一种方法的输出进行评审；
2. 允许语义等价匹配，而不是死盯名字；
3. 把生成结果与专家 diagrammatic ground truth 对齐。

### 评哪些组件

一共 7 类：

1. `states`
2. `transitions`
3. `guards`
4. `actions`
5. `hierarchical states`
6. `parallel regions`
7. `history states`

### 指标怎么定义

每一类组件都统计：

1. `TP`
2. `FP`
3. `FN`

然后计算：

1. `Precision`
2. `Recall`
3. `F1-score`

最后再把全部组件汇总，算整体 `F1-score`。

### 这篇评测最大的优点

它把“生成质量”拆成了可解释的多个维度。你不会只看到一个总分，而会知道：

1. 状态是否对了；
2. 迁移是否对了；
3. 守卫是否对了；
4. 动作是不是特别差；
5. 层次/并行/历史状态有没有抓到。

### 从本地 `parquet` 可以直接看到什么

按我们已经加载的 [structure_event_driven_metrics.parquet](./2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/structure_event_driven_metrics.parquet) 汇总，整体 `F1` 大致如下：

| 模型与策略 | 整体 F1 |
| --- | ---: |
| `Claude 3.5 Sonnet + single_prompt` | `0.693` |
| `GPT-4o + structure_driven` | `0.652` |
| `GPT-4o + hybrid` | `0.638` |
| `Claude 3.5 Sonnet + hybrid` | `0.621` |
| `Claude 3.5 Sonnet + structure_driven` | `0.479` |
| `GPT-4o + single_prompt` | `0.452` |
| `GPT-4o + event_driven` | `0.318` |
| `Claude 3.5 Sonnet + event_driven` | `0.298` |

更有意思的是组件层面。比如 `single_prompt`：

| 组件 | `Claude 3.5 Sonnet` F1 | `GPT-4o` F1 |
| --- | ---: | ---: |
| `States` | `0.903` | `0.698` |
| `Transitions` | `0.744` | `0.478` |
| `Guards` | `0.565` | `0.277` |
| `Actions` | `0.216` | `0.000` |
| `Parallel regions` | `0.667` | `0.308` |
| `History states` | `0.400` | `0.545` |

这组数很有价值，因为它清楚告诉我们：

1. 状态通常比守卫和动作容易；
2. 动作是最难的；
3. 结构感强的组件未必稳定；
4. 所以实验不能只看“生成了几个状态”，一定要把守卫/动作/层次单独拉出来。

## 8. 对 `project_1` 的直接建议

### 8.1 实验主线建议

我建议把 `project_1` 的实验主线明确成：

`controller-level natural language description -> pyfcstm / state-machine model`

不要把主线直接抬到：

`system-level multi-block MBSE synthesis`

原因很简单：

1. 这更贴合 `sources` 现状；
2. 也更贴合你的博士题目“控制系统状态机建模与验证”；
3. 它能和 `llms_emp`、`Nimbus`、`Structure/Event-Driven` 三类 baseline 都建立可解释对照。

### 8.2 数据集组织建议

建议把 `sources` 实验集分成 4 个桶：

1. `FSM-basic`
2. `EFSM-interlock`
3. `Timed/T1`
4. `HSM/Layered`

这样做有 3 个好处：

1. 可解释；
2. 能做分桶结果表；
3. 方便说明模型到底是败在守卫、时间还是层次上。

### 8.3 评测栈建议

最建议采用三层评测：

1. **语法/结构层**：
   - 输出是否通过你自己的建模语法约束；
   - 是否存在明显坏边、悬空状态、非法时间表达。
2. **组件对齐层**：
   - 学 `Structure/Event-Driven`，给状态、迁移、守卫、动作、层次单独算分。
3. **执行/验证层**：
   - 学 `Nimbus`，挑一小批样本做仿真、性质检查或场景回放。

这样既不会像 `ttool-ai` 一样过重，也不会像只算 BLEU 那样没说服力。

### 8.4 论文写作口径建议

如果后面要写论文，我建议你明确区分 3 个概念：

1. **原始论文证据**：`paper_content.txt` 和引文。
2. **整理后自然语言输入**：`STM.md` 第 2 节。
3. **目标状态机模型**：你自己的 `pyfcstm` / 目标形式模型。

只要把这三层写清楚，审稿人就不太容易抓住“你这不是 raw requirements”这个点硬打。

### 8.5 最后一句判断

如果问题是：

`sources 文库里面提取出来的自然语言描述是否足够支撑这样的学术实验？`

我的答案是：

**足够。**

但它目前足够支撑的是：

`控制器级、状态机导向、可验证的自然语言建模实验`

而不是：

`完整系统级 MBSE 自动设计实验`

前者已经很强，也更适合 `project_1`。
