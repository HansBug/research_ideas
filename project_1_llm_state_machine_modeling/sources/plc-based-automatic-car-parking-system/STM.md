# PLC Based Automatic Car Parking System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文给出了车位状态盘点、入口处门禁控制以及开门后自动复位的完整顺序说明。

## 条目 1: Slot-Guided Entry Gate Control
- 控制对象：多层停车场的 PLC 入口门禁与车位引导控制系统

### 0. 条目识别与判定
- 一句话说明：这是智慧停车领域的停车场入口控制器，用于统计空位、向 HMI 发布车位状态，并根据入口车辆检测驱动道闸开闭。
- 判断：算。对象是实际停车控制系统，原文明确写出了 slot sensors、PLC/HMI 计数和入口门开闭时序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，How it works?，行 120-123
> There are proximity sensors connected at each parking spot which will detect the car and give the signal to PLC. After receiving the signal PLC will count the number of car and give the status to HMI which will fixed at the outside of parking which shows the current condition of each slots in the parking.

#### 摘录 B
- 出处：第 2 页，Working of Arduino，行 133-143
> When the car arrives at the entry point there is a proximity sensor which will detect the car. Also there is a LED light which will indicate the current condition (turn on – stop signal and turn off – go inside the parking). When the car arrives at the entry point light is glowing and it will detect by the sensor (Fig. a). After the detection of car the door will open and light goes off (Fig. b). When the car goes door will open for prescribed time and light remains off (Fig. c). After prescribed time door will be back to its normal position.

### 2. 基于原文整理后的自然语言描述

The parking controller uses proximity sensors at each parking slot to detect whether the slots are occupied and then updates the HMI with the current slot status and vehicle count. At the entry point, another proximity sensor detects the arriving car while the LED indicates whether the car must stop or may proceed. Once the arriving car is detected, the door opens, the light goes off, and after a prescribed time the door returns to its normal position for the next vehicle.

### 3. 逐句溯源

1. 句子 1：The parking controller uses proximity sensors at each parking slot to detect whether the slots are occupied and then updates the HMI with the current slot status and vehicle count.
   对应摘录：A
2. 句子 2：At the entry point, another proximity sensor detects the arriving car while the LED indicates whether the car must stop or may proceed.
   对应摘录：B
3. 句子 3：Once the arriving car is detected, the door opens, the light goes off, and after a prescribed time the door returns to its normal position for the next vehicle.
   对应摘录：B
