# Perencanaan Control Valve Pada Head Tank PLTA Tulungagung Menggunakan PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了头水箱液位阈值到阀门动作的明确 PLC 控制逻辑，并包含 auto/manual 与传感器改造信息。

## 条目 1: Head-Tank Elevation Valve Control
- 控制对象：过程控制领域的水电站头水箱 PLC 控制阀系统

### 0. 条目识别与判定
- 一句话说明：这是 PLTA 头水箱液位控制器，用于根据超声波测得的水位高度自动驱动电动阀/电磁阀维持冷却水系统所需水位。
- 判断：算。对象是实际冷却系统控制子系统，原文明确给出了液位阈值和阀门开关条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 17-24
> Head Tank ... still has a manual control valve which consists of a gate valve and a pair of float valves. ... In this research, there would build a plan of the automatic control valve of the Tulungagung HEPP. PLC Siemens Simatic Step 7 was used as a control base on a SCADA software Wonderware Intouch version 10.0.0. In this modification plan, a pair of float valve changed over solenoid valve and manual gate valve change over motorized valve. For the water level that would be ultrasonic sensor SICK UM 30 ...

#### 摘录 B
- 出处：第 3 页，control logic summary, 行 140-146
> 1. Jika elevasi head tank ≤ 41.60 mdpl maka sinyal elevasi head tank low terkirim di ruang CCR, dan float valve 1 + float valve 2 = ON
>
> 2. Jika elevasi head tank ≤ 41.80 mdpl, maka float valve 1 + float valve 2 = ON hingga elevasi head tank mencapai 42.00 mdpl.
>
> 3. Jika 41.80 mdpl ≤ elevasi head tank ≤ 42.00 mdpl, maka float ...

### 2. 基于原文整理后的自然语言描述

The modified head-tank controller replaces the original manual gate valve and float-valve arrangement with a PLC-based automatic valve system using a motorized valve, solenoid valves, and an ultrasonic water-level sensor. When the head-tank elevation drops to 41.60 mdpl or below, a low-level signal is sent to the control room and both control valves are turned on. When the elevation is 41.80 mdpl or below, the valves remain on until the water level reaches 42.00 mdpl.

### 3. 逐句溯源

1. 句子 1：The modified head-tank controller replaces the original manual gate valve and float-valve arrangement with a PLC-based automatic valve system using a motorized valve, solenoid valves, and an ultrasonic water-level sensor.
   对应摘录：A
2. 句子 2：When the head-tank elevation drops to 41.60 mdpl or below, a low-level signal is sent to the control room and both control valves are turned on.
   对应摘录：B
3. 句子 3：When the elevation is 41.80 mdpl or below, the valves remain on until the water level reaches 42.00 mdpl.
   对应摘录：B
