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
- 出处：第 1 页，Introduction，对 image-processing pipeline 与 1-second capture 的说明，行 37-40
> Under image processing, we use sub techniques like RGB to Gray conversion, Image resizing, Image Enhancement, Edge
> detection, Image matching, and Timing allocation. A real -time image is captured for every 1 second. After edge detection
> procedure for both reference and real -time images, these images are compared using SURF Algorithm. Then the amount of
> traffic is d etected and the details are stored in the server.

#### 摘录 B
 - 出处：第 3-4 页，System architecture，对 reference image / actual image / processing chain 的说明，行 118-135
> The system that we put forward consists of a CCTV camera that is used to capture the reference image and
> the a ctual image. These images are stored in a database. It is later retrieved from database and Image process
> techniques are applied and are feed into Aurdino.
> In our proposed system, the reference image of an empty road is taken and the real -time traffic on a road is
> captured as an actual image. They are stored in the database and the data is extracted using data extraction tools .
> Image processing techniques like RGB to Grayscale conversion, Image resizing, Image enhancement, Edge
> detection are used and applied to both the images. Image matching for both the images is done and the percentage
> of matching is done using the SURF algo rithm.

#### 摘录 C
- 出处：第 4-5 页，Timing allocation，对 matching interval and signal duration 的映射规则，行 160-168
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

The controller captures a real-time road image every 1 second and compares the actual image with a reference image of an empty road. Both images are processed through RGB-to-grayscale conversion, resizing, enhancement, edge detection, and SURF-based image matching, and the matching percentage is then used for timing allocation. The controller maps a matching level of 0-30% to 90 seconds of green, 30-50% to 60 seconds of green, 50-70% to 30 seconds of green, and 70-90% to 20 seconds of green. If the matching lies between 90 and 100%, the controller keeps the red light on for 90 seconds instead of allocating a green interval.

### 3. 逐句溯源

1. 句子 1：The controller captures a real-time road image every 1 second and compares the actual image with a reference image of an empty road.
   对应摘录：A, B
2. 句子 2：Both images are processed through RGB-to-grayscale conversion, resizing, enhancement, edge detection, and SURF-based image matching, and the matching percentage is then used for timing allocation.
   对应摘录：A, B
3. 句子 3：The controller maps a matching level of 0-30% to 90 seconds of green, 30-50% to 60 seconds of green, 50-70% to 30 seconds of green, and 70-90% to 20 seconds of green.
   对应摘录：C
4. 句子 4：If the matching lies between 90 and 100%, the controller keeps the red light on for 90 seconds instead of allocating a green interval.
   对应摘录：C
