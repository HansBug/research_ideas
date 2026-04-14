# Intelligent Traffic Light Controller using Fuzzy Logic and Image Processing - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：该条目已经能保住输入车流、摄像/传感感知链、六路信号输出、道路容量与实例化配时结果，可进主样本。

## 条目 1: Fuzzy traffic-light timing based on road congestion
- 控制对象：基于模糊逻辑的交通灯相位控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通控制领域的 fuzzy-logic traffic light controller，用于依据各路口车流和信号时长输入来同时调整多路红黄绿信号。
- 判断：算，但属于相位控制逻辑的可整理样本。对象是实际交通灯控制器，原文给出了输入量、输出信号和依据拥堵程度动态分配时隙的控制描述。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，对 fuzzy logic controller inputs/outputs 的说明，行 17-24
> smart traffic light controller was designed using fuzzy logic and
> image processing with MATLAB, to control movement in two
> ways, aided by a camera and auto sensors. The Fuzzy logic has
> two inputs and six outputs designed, th e console input is the
> number of cars on each road  and the time of the assumed red,
> yellow and green signal according to the vehicles congestion. The
> simulation result is similar to the proposed control unit, as it
> deals with the lights simultaneously acco rding to the number of

#### 摘录 B
- 出处：第 2 页，Section II，对 sensors/cameras 与 dynamic timing 的说明，行 132-140, 176-184
> system (artificial intelligent control)  is fuzzy logic controller
> with multiple sensors and cams distributed around the traffic
> signal at each direction. The function of each sensor is to sense
> if there is a car or not and if any car entered the target zone, in
> which case the sensor activates the ca mera to capture a photo,
> and the photo is processed and the number of cars on the photo
> are calculated. The same mechanism is applied to each road,
> and the signal time for the road is not fixed.
> The number  of cars  on
> road one can be calculated  by fixing  a sensor 30m from the
> signal . Road one is assumed with  three sub roads with full
> capacity of 24 cars, and road two is assumed with two sub
> roads with  maximum capacity of 16  cars as represented  of
> fuzzy logic  input .

#### 摘录 C
- 出处：第 3 页，Rule viewer，对 six outputs 的实例结果说明，行 231-263
> Fig. 4.  Rules Viewer for  the Fuzzy  Logic with Two Inputs  ( Cars on RO1
> and RO2) and  Six Output are  the Timing of  the Traffic  Signal ( R1,  G1, Y1,
> R2, G2 and Y2). Each Time of  the Signal  can be Determined by  Fuzzy  Logic
> Controller and  its Function  of the Number  of Cars at each Roads.
> Fig. 6.  Rules Viewer Representing  the Input and Output  of each Roads, if
> they are 24 Cars on  RO1 and  15 Cars on Road Two then G1=R2= 45.9 sec,
> Y1=Y2=4 sec and G2=R1=27.6 sec.

### 2. 基于原文整理后的自然语言描述

The controller uses two fuzzy-logic inputs, the numbers of cars on roads RO1 and RO2, and produces six traffic-signal outputs `R1`, `G1`, `Y1`, `R2`, `G2`, and `Y2`. Sensors and cameras on each road detect whether a car has entered the target zone, trigger image capture, and use the processed images to calculate the actual number of cars, after which the controller assigns signal times dynamically instead of keeping a fixed timing plan. In the model, road one is assumed to have a capacity of 24 cars and road two a capacity of 16 cars, and the fuzzy rule base maps the pair of road occupancies to the corresponding red/yellow/green durations. For example, when RO1 has 24 cars and RO2 has 15 cars, the controller sets `G1 = R2 = 45.9 s`, `Y1 = Y2 = 4 s`, and `G2 = R1 = 27.6 s`.

### 3. 逐句溯源

1. 句子 1：The controller uses two fuzzy-logic inputs, the numbers of cars on roads RO1 and RO2, and produces six traffic-signal outputs `R1`, `G1`, `Y1`, `R2`, `G2`, and `Y2`.
   对应摘录：A, C
2. 句子 2：Sensors and cameras on each road detect whether a car has entered the target zone, trigger image capture, and use the processed images to calculate the actual number of cars, after which the controller assigns signal times dynamically instead of keeping a fixed timing plan.
   对应摘录：A, B
3. 句子 3：In the model, road one is assumed to have a capacity of 24 cars and road two a capacity of 16 cars, and the fuzzy rule base maps the pair of road occupancies to the corresponding red/yellow/green durations.
   对应摘录：B, C
4. 句子 4：For example, when RO1 has 24 cars and RO2 has 15 cars, the controller sets `G1 = R2 = 45.9 s`, `Y1 = Y2 = 4 s`, and `G2 = R1 = 27.6 s`.
   对应摘录：C
