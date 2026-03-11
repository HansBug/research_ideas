# Intelligent Traffic Light Controller using Fuzzy Logic and Image Processing - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：用车流量与红黄绿时间共同决定六个信号输出，具备明确的相位控制含义。

## 条目 1: Fuzzy traffic-light timing based on road congestion
- 控制对象：基于模糊逻辑的交通灯相位控制器

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
- 出处：第 1 页，Introduction，对 dynamic time slots 的说明，行 80-80
> infrared sensors and achieves dynamic time slots at different

#### 摘录 C
- 出处：第 2 页，System description，对 six traffic signals 的说明，行 174-175
> Fig. 1, with six traffic signals  (green  one, green  two, red one , 
> red two , yellow one and yellow two). The number  of cars  on

### 2. 基于原文整理后的自然语言描述

The fuzzy traffic light controller uses the number of cars on each road together with the assumed red, yellow and green times to regulate the intersection. It assigns dynamic time slots at different roads according to the measured congestion. The system controls six traffic signals corresponding to the red, yellow and green outputs of the two directions.

### 3. 逐句溯源

1. 句子 1：The fuzzy traffic light controller uses the number of cars on each road together with the assumed red, yellow and green times to regulate the intersection.
   对应摘录：A
2. 句子 2：It assigns dynamic time slots at different roads according to the measured congestion.
   对应摘录：B
3. 句子 3：The system controls six traffic signals corresponding to the red, yellow and green outputs of the two directions.
   对应摘录：C
