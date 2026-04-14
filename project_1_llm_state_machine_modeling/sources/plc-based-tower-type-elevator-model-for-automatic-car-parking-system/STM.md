# PLC Based Tower Type Elevator Model for Automatic Car Parking System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 tower-type 停车系统的 `parkingin / parkingout` 模式、空位检查和 token 分配流程都写得较清楚。

## 条目 1: Vacant-Slot Search and Token-Based Tower Parking
- 控制对象：塔式自动停车系统的 PLC 电梯与车位分配控制器
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是智慧停车领域的塔式停车控制器，用于检测停车区来车、搜索空车位、将车辆送往空位并按 slot 编号发放 token。
- 判断：算。对象是实际自动停车系统，原文明确给出了 parkingin、vacant-position search、slot sensor 检查和 token issuance 的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 20-28
> Car parking is proposed with three floors each floor can accommodate three cars the main components are PLC, sensors and elevator, BLDC motor and programming language is ladder diagram, software is TIA portal. Car is placed on the parking area sense by sensors and select the parkingin button it parks automatically in the vacant position and light the respected slot in the panel board followed by receiving a token number. For park out select the parkingout button and slot number the car automatically reaches to ground position.

#### 摘录 B
- 出处：第 3 页，Algorithm steps，行 170-182
> Step 2: check the main gate sensor, elevator sensor and any one sensor in slots are low then only open the main gate and car enter the elevator otherwise move to step 9. Step 3: then elevator sensor is high and check the first floor vacant or not, if vacant move to next step otherwise move to step 8. Step 4: if check the first slot sensor is low or not if it is low park the car in the first slot and get the token with respected slot number ... Step 7: the elevator moves to second floor check the vacant or not ... Step 8: the elevator moves to third floor check the vacant or not ... Step 9: if all the floors are full it shows parking area full. Step 10: if parking out enters the token then it senses slot number and floor number the elevator moves to that floor and taken out.

### 2. 基于原文整理后的自然语言描述

The tower-type parking controller first checks the main-gate sensor, the elevator sensor, and whether at least one slot sensor is free before allowing an incoming car to enter the elevator. In parking-in mode, the controller searches floor by floor and then slot by slot, moving from the first floor to the second and third floors only when the earlier positions are full, and it parks the car in the first available slot while lighting that slot on the panel and issuing the corresponding token number. If all floors are occupied, the system reports that the parking area is full. In parking-out mode, the controller reads the token, identifies the stored floor and slot, moves the elevator to that position, and brings the car back to ground level.

### 3. 逐句溯源

1. 句子 1：The tower-type parking controller first checks the main-gate sensor, the elevator sensor, and whether at least one slot sensor is free before allowing an incoming car to enter the elevator.
   对应摘录：B
2. 句子 2：In parking-in mode, the controller searches floor by floor and then slot by slot, moving from the first floor to the second and third floors only when the earlier positions are full, and it parks the car in the first available slot while lighting that slot on the panel and issuing the corresponding token number.
   对应摘录：A, B
3. 句子 3：If all floors are occupied, the system reports that the parking area is full.
   对应摘录：B
4. 句子 4：In parking-out mode, the controller reads the token, identifies the stored floor and slot, moves the elevator to that position, and brings the car back to ground level.
   对应摘录：A, B
