# PLC Based Water Level Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了基于多浮球阈值的水泵启停逻辑，非常适合做简单阈值驱动控制样本。

## 条目 1: Float-Triggered Pump On-Off Cycle
- 控制对象：过程控制领域的 PLC 水位控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个双水箱液位控制器，用于通过上、下罐浮球开关检测水位，并在达到预定阈值时启停抽水电机。
- 判断：算。对象是实际液位控制系统，原文明确写出了阈值触发、泵启停和满罐停止逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 14-18
> I have used Siemens plc for water level control system. In this type plc is a very simple programming language so that this project used a four float switch sensor. Two float switch sensor is used a upper tank and two float switch sensor is used bottom tank.

#### 摘录 B
- 出处：第 1 页，Abstract, 行 28-32
> effort has been made to construct a water controller that is capable of controlling the electric water pumping motor operation in regard switching on or off at predetermined level of water in the storage tanks or reservoirs. This project also gives the clarity of advantage of using an automatic method of controlling level over human or manual control method.

#### 摘录 C
- 出处：第 1 页，Related Work, 行 54-67
> Automatic tank filling in-home helps you automate your motor and fill the tank whenever it reaches the threshold level and turns off the motor after the tank is full. ... Whenever the water level reaches threshold Bolt gives a signal to the relay to turn on the motor ... when the tank is full Bolt sends a signal to turn off the motor.

### 2. 基于原文整理后的自然语言描述

The PLC water-level controller uses four float-switch sensors, with two assigned to the upper tank and two assigned to the lower tank. It automatically switches the pumping motor on or off at predetermined tank levels instead of relying on manual operation. When the water level reaches the threshold, the relay starts the motor, and when the tank becomes full, the controller turns the motor off.

### 3. 逐句溯源

1. 句子 1：The PLC water-level controller uses four float-switch sensors, with two assigned to the upper tank and two assigned to the lower tank.
   对应摘录：A
2. 句子 2：It automatically switches the pumping motor on or off at predetermined tank levels instead of relying on manual operation.
   对应摘录：B
3. 句子 3：When the water level reaches the threshold, the relay starts the motor, and when the tank becomes full, the controller turns the motor off.
   对应摘录：C
