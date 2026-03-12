# Intelligent elevator control and safety monitoring system - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：门感应、语音选层和超时关闭前的语音控制逻辑较明确。

## 条目 1: Door induction and speech-control sequence
- 控制对象：智能电梯的人机交互与门控子系统

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的 intelligent elevator interaction controller，用于自动开门、在关门后触发语音选层，并在限定条件下结束语音录入。
- 判断：算，但属于上层交互控制样本。对象是实际电梯控制系统的子系统，原文给出了感应开门、关门后触发语音控制及其结束条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 2.1，对 automatic induction of elevator doors 与 speech control 的描述，行 55-60
> The elevator control system can achieve the following three objectives. 
> 2.1.1. Automatic induction of elevator doors. Using infrared induction technology, users can only 
> make a stop at the automatic sensing area in front of the elevator, and the doors of the elevator can be 
> opened automatically without manual manipulation.  
> 2.1.2. Speech control. After the user enters the elevator, the elevator door shut down automatically 
> triggers the elevator speech control system, voice guide users to select floor, according to user's voice

#### 摘录 B
- 出处：第 3 页，Section 2.2.2，对 speech control system workflow 的描述，行 108-110
> 2.2.2. Speech control system.At the moment when the elevator door is closed, can trigger the elevator 
> floor voice control system began to work, until you receive the two effective signal or close the door 
> after more than 20 seconds (mainly first come), elevator floor voice control system to stop working.

### 2. 基于原文整理后的自然语言描述

When a user reaches the automatic sensing area in front of the elevator, the doors open automatically without manual manipulation. After the elevator door has closed, the speech control system is triggered so that the user can select the destination floor by voice. The speech control continues until two effective signals are received or until more than twenty seconds have passed after door closure.

### 3. 逐句溯源

1. 句子 1：When a user reaches the automatic sensing area in front of the elevator, the doors open automatically without manual manipulation.
   对应摘录：A
2. 句子 2：After the elevator door has closed, the speech control system is triggered so that the user can select the destination floor by voice.
   对应摘录：A, B
3. 句子 3：The speech control continues until two effective signals are received or until more than twenty seconds have passed after door closure.
   对应摘录：B
