# PLC Based Automatic Intelligent Car Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场监督控制直接写成 `ON / OFF / EMERGENCY` 三模式逻辑，并明确给出入口/出口 IR 触发、LDR 车位占用判断、满位拒绝和紧急全闭锁链，足以形成双 A 停车门禁样本。

## 条目 1: ON-OFF-EMERGENCY Parking Gate Supervisor

- 控制对象：停车场入口/出口门禁与车位占用监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 PLC 的停车场监督控制器，用三种模式管理入口/出口 gate、车位占用检测和异常全闭锁。
- 判断：算。对象是实际停车控制系统，而不是单一传感器或显示模块；原文明确写出 `ON`、`OFF`、`EMERGENCY` 模式、六个车位 LDR、入口/出口 IR 传感器及 gate 开闭条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 3-18 行
> The main purpose of this paper was to design and implement an intelligent car parking system. The proposed system works on three modes such as ON, OFF and EMERGENCY. The system developed is able to sense the presence of the vehicles standing at the main car parking gate through an IR sensor. ... there is a global shift towards the automatic car parking system to calculate accurate space available for car and revenue collection as a parking fee.

#### 摘录 B

- 出处：第 2-3 页，`III. Methodology`，`paper_content.txt` 第 100-132 行
> The intelligent car parking system works in three modes such as ON, OFF and EMERGENCY. The ON mode gets activated at the day time ... The OFF mode is used at night ... The EMERGENCY system gets activated whenever the parking authority staff presses the emergency push button ... In emergency mode the PLC directs to close all the gates and no car is allowed to enter or leave the car parking. ... If the data provided by the LDR shows the possibility of available space for car parking and also the IR sensor detects the presence of car waiting to get parked, then the PLC directs the main parking gate to open ... If the data provided by the LDR shows the possibility of fully occupied parking space, then the PLC stops the main gate from opening and directs the car to next parking ground.

#### 摘录 C

- 出处：第 3 页，`IV. Process Description`，`paper_content.txt` 第 169-204 行
> There are two sets of IR sensor. First IR sensor is placed at the entry gate to detect the presence of the vehicle at the entry gate. Second IR sensor is placed at the exit gate which helps in detecting the vehicle at the exit gate and directs the PLC to open the gate. There are six LDR sensors placed on each of the car parking ground ... The push button enables the security alarm and directs the PLC to shut down all the gates of the car parking system. ... Entry gate opens whenever the IR sensor detects a vehicle at the entry gate and a space is available for parking. The exit gate opens whenever the IR sensor detects the presence of a vehicle at the exit gate and also when the emergency mode is inactive.

### 2. 基于原文整理后的自然语言描述

The parking controller is organized around three PLC operating modes: `ON` for normal daytime service, `OFF` for low-use night operation, and `EMERGENCY` for security incidents that must lock the facility immediately. In normal service, six `LDR` sensors report whether each parking slot is occupied, while an entry `IR` sensor detects a waiting vehicle at the main gate and an exit `IR` sensor detects vehicles requesting departure. The PLC opens the entry gate only when a vehicle is present and the `LDR` inputs still indicate at least one vacant slot; if all spaces are occupied, the gate remains closed and the driver is redirected to the next parking ground instead of being admitted. The exit gate opens when a vehicle is sensed at the exit and the controller is not in `EMERGENCY`, so the outgoing path is also guarded by the global mode state. When a guard presses the emergency push button after observing suspicious activity, the system switches to `EMERGENCY`, raises the alarm, and forces all gates closed so no vehicle can enter or leave the car park.

### 3. 逐句溯源

1. 句子 1：The parking controller is organized around three PLC operating modes: `ON` for normal daytime service, `OFF` for low-use night operation, and `EMERGENCY` for security incidents that must lock the facility immediately.
   对应摘录：A, B
2. 句子 2：In normal service, six `LDR` sensors report whether each parking slot is occupied, while an entry `IR` sensor detects a waiting vehicle at the main gate and an exit `IR` sensor detects vehicles requesting departure.
   对应摘录：B, C
3. 句子 3：The PLC opens the entry gate only when a vehicle is present and the `LDR` inputs still indicate at least one vacant slot; if all spaces are occupied, the gate remains closed and the driver is redirected to the next parking ground instead of being admitted.
   对应摘录：B
4. 句子 4：The exit gate opens when a vehicle is sensed at the exit and the controller is not in `EMERGENCY`, so the outgoing path is also guarded by the global mode state.
   对应摘录：C
5. 句子 5：When a guard presses the emergency push button after observing suspicious activity, the system switches to `EMERGENCY`, raises the alarm, and forces all gates closed so no vehicle can enter or leave the car park.
   对应摘录：B, C
