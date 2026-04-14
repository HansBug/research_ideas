# Design and Implementation of Car Parking System on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把停车系统入口检查、身份识别、车位判定和整合仿真写成 ASMD/FSM 工作流，原文与实现细节都足够支撑双 A 条目。

## 条目 1: Availability-Identification-Slot-Allotment Parking FSM

- 控制对象：停车场入口门禁与车位分配控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个停车场管理控制器，用 FPGA 状态机把入口空间检查、车主身份识别、车位状态判定和最终车位分配串成一条离散控制链。
- 判断：算。对象是实际停车场控制系统，原文明确指出系统由状态机建模，并给出 ASMD 流程、身份识别模块、车位检查模块、车位状态类别和整合后的 RTL/仿真结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，`3.2 Finite state machine / 4.1 Designing of parking system with State Machine Diagram`，`paper_content.txt` 第 202-226 行
> In order to implement parking system a state diagram is constructed. ... the proposed system performs space availability, motor rotation for door opening, identification and slot availability information. The system includes: `Identification` and `Slot Selection`.
>
> `ASMD` chart is Algorithm State Machine Diagram. ... At the entrance of parking area, LCD displays the status of parking system. If space is available then LCD displays space available else LCD displays no space exit. According to space status motor rotates in clockwise direction. After that identification unit identifies the person. For new member temporary card is allotted. After identification, slot status is checked. Status can be `filled`, `empty` or `reserved`. RF sensors are used in this process.

#### 摘录 B

- 出处：第 6-8 页，`4.2 Results`，`paper_content.txt` 第 238-298 行
> After space checking door will open with the help of stepper motor. ... When door opened, identification process starts. ... `Current_state` and `next_state` describes visitor is identified or a new member has come. ... Following simulation shows identification process.
>
> After that slot checking procedure starts. ... `Led_slotallot` and `slotallot` are output signals. When reset signal goes high-to-low, system comes out from idle state. According to input signals ... `slot 15` is available. ... Now identification and slot allotment modules are integrated. ... `Identified`, `new_member`, `led`, `led_filled`, `led_reserv`, `cout` are output signals. ... Figure above shows the `32 slot` involving RTL view parking system.

### 2. 基于原文整理后的自然语言描述

The FPGA parking controller is organized as a state-machine workflow that first evaluates parking-space availability at the entrance, then opens the gate, identifies the arriving user, and finally allocates a slot. Its ASMD chart combines two major subfunctions, `Identification` and `Slot Selection`, so the controller can distinguish known visitors from new members, issue a temporary card to a new member, and then classify candidate slot status as `filled`, `empty`, or `reserved`. After the space check succeeds, the system drives a stepper motor to open the entrance door and then starts the identification process, where current and next states encode whether the visitor has been identified or is a new member. The integrated implementation exposes slot-allotment outputs, reports that `slot 15` is available in the example simulation, and scales the same logic to a `32-slot` RTL parking-management view with LED outputs for slot, filled, and reserved status.

### 3. 逐句溯源

1. 句子 1：The FPGA parking controller is organized as a state-machine workflow that first evaluates parking-space availability at the entrance, then opens the gate, identifies the arriving user, and finally allocates a slot.
   对应摘录：A, B
2. 句子 2：Its ASMD chart combines two major subfunctions, `Identification` and `Slot Selection`, so the controller can distinguish known visitors from new members, issue a temporary card to a new member, and then classify candidate slot status as `filled`, `empty`, or `reserved`.
   对应摘录：A
3. 句子 3：After the space check succeeds, the system drives a stepper motor to open the entrance door and then starts the identification process, where current and next states encode whether the visitor has been identified or is a new member.
   对应摘录：B
4. 句子 4：The integrated implementation exposes slot-allotment outputs, reports that `slot 15` is available in the example simulation, and scales the same logic to a `32-slot` RTL parking-management view with LED outputs for slot, filled, and reserved status.
   对应摘录：B
