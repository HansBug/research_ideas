# Traffic Signal Control Using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文对车辆检测、行人过街触发和红灯联动闸门控制都有明确文字说明，适合直接收录。

## 条目 1: Vehicle and Pedestrian Aware Signal-and-Barrier Control
- 控制对象：路口交通灯与自动栏杆联动控制系统

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的 PLC 联动控制系统，用于依据车辆和行人传感输入控制信号灯与栏杆的开闭。
- 判断：算。对象是实际交通控制系统，原文给出了传感输入、红绿灯响应和栏杆联动逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 16-21 行
> This paper presents feasible approach of Programmable Logic Controller (PLC) for controlling traffic signal lights using eddy current displacement sensors and for traffic intersection a proportionate signaling is designed. In this system, piezoelectric material is used to generate power from load of vehicles when the vehicles is in idle situation in traffic signal junction and load of people who usually use pathways across traffic road.

#### 摘录 B
- 出处：第 3 页，系统布局说明，`paper_content.txt` 第 123-139 行
> At each rod 3 eddy current displacement sensors were used. ... For zebra crossing eddy current displacement sensor which senses the human was used in every road. After sensing 10 people all signals was red as this people can cross the road. At each road automatic barrier was used. When the signal was red the barrier was closed that means no vehicle can break the traffic rules and when the signal was green the barrier was open.

### 2. 基于原文整理后的自然语言描述

The PLC traffic controller uses eddy current displacement sensors to detect vehicles and apply proportionate signal timing at the intersection. It also monitors the zebra crossing sensor, and when ten pedestrians are detected it forces all traffic signals to red so that people can cross safely. Automatic barriers are coupled to the signal state, remaining closed on red and opening only when the corresponding signal turns green.

### 3. 逐句溯源

1. 句子 1：The PLC traffic controller uses eddy current displacement sensors to detect vehicles and apply proportionate signal timing at the intersection.
   对应摘录：A
2. 句子 2：It also monitors the zebra crossing sensor, and when ten pedestrians are detected it forces all traffic signals to red so that people can cross safely.
   对应摘录：B
3. 句子 3：Automatic barriers are coupled to the signal state, remaining closed on red and opening only when the corresponding signal turns green.
   对应摘录：B
