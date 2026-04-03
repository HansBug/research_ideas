# Traffic Light Controller using Image Processing - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：图像匹配结果到红绿灯时长的映射规则明确可追溯。

## 条目 1: Image-based traffic signal timing allocation
- 控制对象：基于图像处理的交通灯时长分配控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

The controller uses the standard red, yellow, and green traffic lights together with CCTV images of the junction to choose the signal duration. After comparing the captured image with the reference image, it maps a matching level of 0-30% to 90 seconds of green, 30-50% to 60 seconds of green, 50-70% to 30 seconds of green, and 70-90% to 20 seconds of green. If the matching rises to 90-100%, the controller does not allocate a green phase for that case and instead keeps the red light on for 90 seconds.

### 3. 逐句溯源

1. 句子 1：The controller uses the standard red, yellow, and green traffic lights together with CCTV images of the junction to choose the signal duration.
   对应摘录：A
2. 句子 2：After comparing the captured image with the reference image, it maps a matching level of 0-30% to 90 seconds of green, 30-50% to 60 seconds of green, 50-70% to 30 seconds of green, and 70-90% to 20 seconds of green.
   对应摘录：B
3. 句子 3：If the matching rises to 90-100%, the controller does not allocate a green phase for that case and instead keeps the red light on for 90 seconds.
   对应摘录：B
