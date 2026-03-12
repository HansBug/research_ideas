# Automatic traffic light controller for emergency vehicle using peripheral interface controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：紧急车辆触发、绿灯延长和恢复正常模式的控制链路非常清楚。

## 条目 1: Emergency-priority traffic light operation
- 控制对象：路口 emergency-priority 交通灯控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通控制领域的 emergency-priority traffic light controller，用于在救护车等紧急车辆到达时改变信号灯并在通行结束后恢复正常运行。
- 判断：算。对象是实际交通灯控制系统，原文清楚给出了紧急触发、强制放行、绿灯延长和恢复正常等离散控制步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，对 emergency case 的总体描述，行 27-34
> Traffic Light Controller for Emergency Vehicle is designed and developed to 
> help emergency vehicle crossing the road at traffic light junction during 
> emergency situation. This project used Peripheral Interface Cont roller (PIC) 
> to program a priority -based traffic light controller for emergency vehicle. 
> During emergency cases, emergency vehicle like ambulance can trigger the 
> traffic light signal to change from red to green in order to make clearance for 
> its path autom atically. Using Radio Frequency (RF) the traffic light operation 
> will turn back to normal when the ambulance finishes crossing the road. Result

#### 摘录 B
- 出处：第 2 页，Section 1，对 priority-based controller 的说明，行 76-80
> light controller for emergency vehicle us ing PIC is a project to program a priority based traffic light controller 
> for emergency vehicle during emergency cases where it is able to trigger the traffic light to change from red to 
> green to make a path for its way. If the traffic light already shows green, time duration will be delayed until 
> the emergency vehicle finishes crossing the junction. This project uses Radio Frequency (RF) for wireless 
> signal transmission. The traffic light operation will turn back to normal when ambulance finishes crossing the

#### 摘录 C
- 出处：第 2 页，System flow，对 push button / signal change / return to normal 的说明，行 106-110
> designed for PIC compiler. The flowchart of this projec t is shown in F igure 2. Once the push button is pressed, 
> an RF signal will be transmitted to the RF receiver. This will activate the PIC to control and trigger the traffic 
> light to turn from red to green. Some delays will be introduced if the emergency veh icle still does not manage 
> to pass the traffic light junction where the time duration of the green light signal appearance will be longer. 
> The traffic light system will be back to normal when the emergency vehicle successfully crosses the traffic

### 2. 基于原文整理后的自然语言描述

During an emergency case, the controller allows an ambulance to trigger the traffic light so that the signal changes from red to green and clears a path through the junction. If the light is already green, the controller extends the green interval until the emergency vehicle has finished crossing. After the emergency vehicle has crossed successfully, the traffic light returns to normal operation.

### 3. 逐句溯源

1. 句子 1：During an emergency case, the controller allows an ambulance to trigger the traffic light so that the signal changes from red to green and clears a path through the junction.
   对应摘录：A, B
2. 句子 2：If the light is already green, the controller extends the green interval until the emergency vehicle has finished crossing.
   对应摘录：B, C
3. 句子 3：After the emergency vehicle has crossed successfully, the traffic light returns to normal operation.
   对应摘录：A, C
