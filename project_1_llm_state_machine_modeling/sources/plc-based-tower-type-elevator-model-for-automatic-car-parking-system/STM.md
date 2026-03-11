# PLC Based Tower Type Elevator Model for Automatic Car Parking System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文把 tower-type 停车系统的 `parkingin / parkingout` 模式、空位检查和 token 分配流程都写得较清楚。

## 条目 1: Vacant-Slot Search and Token-Based Tower Parking
- 控制对象：塔式自动停车系统的 PLC 电梯与车位分配控制器

### 0. 条目识别与判定
- 一句话说明：这是智慧停车领域的塔式停车控制器，用于检测停车区来车、搜索空车位、将车辆送往空位并按 slot 编号发放 token。
- 判断：算。对象是实际自动停车系统，原文明确给出了 parkingin、vacant-position search、slot sensor 检查和 token issuance 的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 20-28
> Car parking is proposed with three floors each floor can accommodate three cars the main components are PLC, sensors and elevator, BLDC motor and programming language is ladder diagram, software is TIA portal. Car is placed on the parking area sense by sensors and select the parkingin button it parks automatically in the vacant position and light the respected slot in the panel board followed by receiving a token number. For park out select the parkingout button and slot number the car automatically reaches to ground position.

#### 摘录 B
- 出处：第 3 页，Algorithm steps，行 170-180
> Step 3: then elevator sensor is high and check the first floor vacant or not, if vacant move to next step otherwise move to step 8. Step 4: if check the first slot sensor is low or not if it is low park the car in the first slot and get the token with respected slot number ... Step 5: it checks the second slot high or low if it is Low Park the car and get the token with respected slot number ... Step 6: it checks the third slot high or low if it is Low Park the ...

### 2. 基于原文整理后的自然语言描述

The tower-type parking controller uses sensors and an elevator to park incoming cars automatically on one of three floors. When the driver selects the parking-in mode, the controller searches for a vacant position, lights the corresponding slot on the panel, and issues a token number for the parked car. During the search, the controller checks floor availability and then examines the slot sensors in sequence so that the car is placed into the first available slot and associated with the corresponding token.

### 3. 逐句溯源

1. 句子 1：The tower-type parking controller uses sensors and an elevator to park incoming cars automatically on one of three floors.
   对应摘录：A
2. 句子 2：When the driver selects the parking-in mode, the controller searches for a vacant position, lights the corresponding slot on the panel, and issues a token number for the parked car.
   对应摘录：A
3. 句子 3：During the search, the controller checks floor availability and then examines the slot sensors in sequence so that the car is placed into the first available slot and associated with the corresponding token.
   对应摘录：B
