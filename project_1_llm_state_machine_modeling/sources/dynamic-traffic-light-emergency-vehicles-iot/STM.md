# Dynamic Traffic Light System to Reduce The Waiting Time of Emergency Vehicles at Intersections within IoT Environment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `fixed cycle -> dynamic mode` 的应急优先交通灯写成了 `pure` 与 `hybrid` 两套带 `TR/TG` 时间公式的算法链，而不是只给简单抢占示意。

## 条目 1: Pure/Hybrid emergency-priority signal controller

- 控制对象：道路交通信号控制领域的 IoT 应急车辆优先交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向应急车辆的动态交通灯控制器，用 IoT 感知应急车辆到达并在 `pure operation mode` 与 `hybrid operation mode` 两套定时规则下改变当前 active light 和等待时间。
- 判断：算。对象是实际交通信号控制算法，原文直接给出了 detection、当前 active light、`TR/TG` 等时间参数和纯/混合两套切换场景，不是泛泛的 smart-city 介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`
> The new approach consists of two algorithms which are pure operation mode and hybrid operation mode. These operation modes aim to reduce the waiting time of emergency vehicles on traffic intersections. ... The smart infrastructure system switches traffic light operation from fixed cycle mode to dynamic mode.

#### 摘录 B

- 出处：第 5 页，`3.1 Pure Operation Mode`
> TR: Time of the Red Light
> TG: Time of the Green Light
>
> If the EV is detected and Traffic Light 1 is red, and another traffic light within the same intersection ... is green, switch it to red and switch Traffic Light (1) to green.
>
> The EV will wait a time equal to (3*TR+TG)*(# of Times Traffic Light 1 changed its status before the EV passes) ...

#### 摘录 C

- 出处：第 6-7 页，`Pure / Hybrid Operation Mode`
> The EV will wait a time within the interval [1 - TG] until Traffic Light 1 becomes green ...
>
> The EV will wait a time within the interval [(TR+1) - (TR+TG)] until Traffic Light 1 becomes green ...
>
> The EV will wait a time equal to (TR+TG)*(# of Times Traffic Light 1 changed its status before the EV passes) ...
>
> The EV will wait a time equal to (TR) until Traffic Light 1 becomes green, then passes the intersection after vehicles in front of it.

#### 摘录 D

- 出处：第 2 页，`Introduction`
> Based on the emergency vehicle's location and the current state of the traffic light, our dynamic model for traffic light system will adapt to reduce the waiting time for the emergency vehicles.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller switches from a fixed-cycle regime to a dynamic emergency-priority regime once the IoT infrastructure detects an approaching emergency vehicle and reports the current signal state. The paper defines two timed EFSM variants, `Pure operation mode` and `Hybrid operation mode`, both parameterized by `TR` and `TG` and both centered on the status of `Traffic Light 1`, which is the lane used by the incoming emergency vehicle. In the detected-emergency branch, if another light is currently active the controller forces that active light to red and immediately grants green to `Traffic Light 1`; in the undetected or partially aligned branches it computes bounded waiting times such as `[1-TG]`, `[(TR+1)-(TR+TG)]`, or repeated-cycle expressions like `(3*TR+TG) * k` and `(TR+TG) * k` before the emergency vehicle can pass. The distinction between the two modes lies in how aggressively the controller shortens the waiting path when the emergency vehicle is not immediately detected, which makes the case more informative than simple RF-triggered override papers.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller switches from a fixed-cycle regime to a dynamic emergency-priority regime once the IoT infrastructure detects an approaching emergency vehicle and reports the current signal state.
   对应摘录：A, D
2. 句子 2：The paper defines two timed EFSM variants, `Pure operation mode` and `Hybrid operation mode`, both parameterized by `TR` and `TG` and both centered on the status of `Traffic Light 1`, which is the lane used by the incoming emergency vehicle.
   对应摘录：A, B
3. 句子 3：In the detected-emergency branch, if another light is currently active the controller forces that active light to red and immediately grants green to `Traffic Light 1`; in the undetected or partially aligned branches it computes bounded waiting times such as `[1-TG]`, `[(TR+1)-(TR+TG)]`, or repeated-cycle expressions like `(3*TR+TG) * k` and `(TR+TG) * k` before the emergency vehicle can pass.
   对应摘录：B, C
4. 句子 4：The distinction between the two modes lies in how aggressively the controller shortens the waiting path when the emergency vehicle is not immediately detected, which makes the case more informative than simple RF-triggered override papers.
   对应摘录：A, B, C
