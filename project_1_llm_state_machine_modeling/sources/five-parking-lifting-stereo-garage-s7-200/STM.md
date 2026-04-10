# Design of Five Parking Lifting Stereo Garage Based on S7-200 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把两层五车位立体车库的自动/手动模式、一层直接存取、二层让位降盘、复位以及故障报警写成了一条清楚的存取控制链，可稳定形成双 A 停车样本。

## 条目 1: Two-layer lift-sliding parking access controller

- 控制对象：智慧停车与车位管理领域的两层五车位升降横移立体车库存取控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `S7-200 PLC` 的升降横移立体车库控制器，用自动/手动模式、层间让位、限位/光电检测和故障报警来完成五个可用车位的存车与取车。
- 判断：算。对象是实际双层立体车库的主控制链，原文明确写出一层直进直出、二层先判下层空位、必要时先横移让位再降盘，以及异常时整机停机报警。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 7-11、23-26 行
> It takes two-layer and five-location of lift-sliding stereo garage for example ... It implements automatic access vehicle, operation monitoring and fault alarm for stereo garage.
>
> The up-down and translation stereo garage system ... total of six parking spaces, including a vacancy with the template the rise and fall of the channel, the other five spaces ... can be used for storage of vehicles. ... Second layer of parking spaces for parking or taking the car, should first determine the corresponding layer if the position is empty, if not empty to shift to a layer, until the bottom of the empty to were falling action reach a layer.

#### 摘录 B

- 出处：第 2 页，`2.1 control section`，`paper_content.txt` 第 39-48 行
> The main operating modes of the control system are divided into two types, automatic operation mode and manual operation mode.
>
> ... in the automatic operation mode, when the operator input and out of the garage password and parking number ... garage tray lifting and traversing action will automatically ...
>
> The so-called manual (or point) operation mode ... operated separately continuous or intermittent operation of a certain action, such as a car lift alone, alone shifting ...

#### 摘录 C

- 出处：第 3 页，`3.2 Composition of control system`，`paper_content.txt` 第 88-101 行
> The main control object of the control system is to traverse a small motor and lift a large motor ...
>
> Travel switch positioning is taken in order to ensure the car carrier dropping at the specified location. The photoelectric switch is used to determine whether there is a vehicle on the car carrier. Besides, anti-falling system with anti-falling electromagnet is used in the second floor parking space ... Safety hook system will be opened with power and locked without power.

#### 摘录 D

- 出处：第 4 页，`3.3 Design of control program`，`paper_content.txt` 第 112-124 行
> PLC control system is mainly aimed to complete the operation of storage and taking vehicles automatically. The control program is designed with modular structure, which is composed of initialization program, main control program and fault alarm program.
>
> ... if driver choose parking space in layer one the driver can directly drive the car into the parking space or out of the car carrier. While if driver choose the layer two, PLC control program can determine the parking space in layer one just below the chosen one whether is free. Then the car carrier will drop when it is free. Otherwise, the car carrier will be moved and free the space firstly. Once complete the car storage or car taking, system will reset automatically and wait for the next operation instructions.
>
> When the vehicle is too long or overweight, or there are some other security risks, the fault alarm program will be sent to the sound and light signal alarm, while the system will stop all actions, clear all ports and prompt troubleshooting.

### 2. 基于原文整理后的自然语言描述

The lift-sliding garage controller is a two-mode `S7-200 PLC` system that manages a two-layer structure with five usable parking positions plus one vacancy channel for lift movement. In automatic mode, the operator enters the parking number and command, and the controller drives the tray-lifting and traversing motions without manual intervention, while maintenance staff can still use pointwise manual mode to move only the lift or only the traversing mechanism. For a first-layer slot, the storage or retrieval cycle is direct because the driver can load or unload at ground level without rearranging other trays. For a second-layer slot, the PLC first checks whether the lower position is free; if it is free, the selected carrier drops to the ground level, and if it is not free the controller first shifts carriers to release the lower vacancy and only then executes the lowering action. Throughout the cycle, travel switches, photoelectric vehicle detection, anti-falling electromagnets, and the safety hook system qualify motion, and any overweight, overlength, or other safety risk diverts the machine into the fault-alarm branch and stops all actions until troubleshooting is completed.

### 3. 逐句溯源

1. 句子 1：The lift-sliding garage controller is a two-mode `S7-200 PLC` system that manages a two-layer structure with five usable parking positions plus one vacancy channel for lift movement.
   对应摘录：A, B
2. 句子 2：In automatic mode, the operator enters the parking number and command, and the controller drives the tray-lifting and traversing motions without manual intervention, while maintenance staff can still use pointwise manual mode to move only the lift or only the traversing mechanism.
   对应摘录：B
3. 句子 3：For a first-layer slot, the storage or retrieval cycle is direct because the driver can load or unload at ground level without rearranging other trays.
   对应摘录：A, D
4. 句子 4：For a second-layer slot, the PLC first checks whether the lower position is free; if it is free, the selected carrier drops to the ground level, and if it is not free the controller first shifts carriers to release the lower vacancy and only then executes the lowering action.
   对应摘录：A, D
5. 句子 5：Throughout the cycle, travel switches, photoelectric vehicle detection, anti-falling electromagnets, and the safety hook system qualify motion, and any overweight, overlength, or other safety risk diverts the machine into the fault-alarm branch and stops all actions until troubleshooting is completed.
   对应摘录：C, D
