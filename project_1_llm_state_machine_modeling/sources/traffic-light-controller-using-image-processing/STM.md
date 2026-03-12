# Traffic Light Controller using Image Processing - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：图像匹配结果到红绿灯时长的映射规则明确可追溯。

## 条目 1: Image-based traffic signal timing allocation
- 控制对象：基于图像处理的交通灯时长分配控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通控制领域的 image-based traffic light controller，用于根据摄像图像估计交通密度并分配不同长度的绿灯或红灯时段。
- 判断：算。对象是实际交通灯控制器，原文给出了三色信号、图像比较后的时长分配规则以及具体阈值对应的控制输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction，对 red/yellow/green lights 的说明，行 69-71
> when effectively monitored can control the traffic on the road and avoid congestion. The traffic light on the road 
> comprises of 3 signals - red, ye llow and green. People are made to hold back for the green signal to further proceed. 
> Delay in the red signal cause longer waiting time because of congestion. CCTV cameras are installed at almost

#### 摘录 B
- 出处：第 4 页，Timing allocation，对 matching interval and signal duration 的映射规则，行 160-168
> 1) If the matching lies between 0 to 30% - green light is turned on for 90 seconds.  
> 2) If the matching lies between 30 to 50% - green light is turned on for 60 seconds.  
>
>
> --- Page 5 ---
> Traffic Light Controller using Image Processing  
> 409 3) If the matching lies betw een 50 to 70% - green light is turned on for 30 seconds.  
> 4) If the matching lies between 70 to 90% - green light is turned on for 20 seconds.  
> 5) If the matching lies between 90 to 100% - red light is turned on for 90 seconds.

### 2. 基于原文整理后的自然语言描述

The traffic signal uses red, yellow and green lights and changes them according to the traffic observed at the junction. After the captured image has been compared with the reference image, the controller assigns different green durations to different levels of traffic density. At the highest matching range, the controller keeps the red light on for a long interval instead of assigning a green phase.

### 3. 逐句溯源

1. 句子 1：The traffic signal uses red, yellow and green lights and changes them according to the traffic observed at the junction.
   对应摘录：A
2. 句子 2：After the captured image has been compared with the reference image, the controller assigns different green durations to different levels of traffic density.
   对应摘录：B
3. 句子 3：At the highest matching range, the controller keeps the red light on for a long interval instead of assigning a green phase.
   对应摘录：B
