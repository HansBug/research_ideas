# Automatic Traffic Using Image Processing - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了“图像采集/车辆计数/按车流分配绿灯时间”的控制闭环，但相位细节主要停留在算法控制层。

## 条目 1: Density-Based Signal Timing
- 控制对象：道路交通信号领域的图像驱动交通灯控制器

### 0. 条目识别与判定
- 一句话说明：这是一个基于相机图像的交通灯控制器，用于统计各方向车辆数并按密度为信号灯分配通行时间。
- 判断：算，但属于控制策略级样本。对象是实际交通信号控制器，不过正文更强调计数与时间分配，而非完整相位状态机。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 19-31
> The paper suggests implementing a smart traffic controller using real-time image processing. The sequence of the camera is analyzed using different edge detection algorithms and object counting methods. The camera will be installed along with traffic light. It will capture the image sequence. To set an image of an empty road as a reference image, the captured images are sequentially matched using image matching; but in my paper, we used filtering method, which filtered the image and released all waste objects and only showed the cars, and after it showed the number of cars in image. My paper is software that takes a picture or video. It has been customized to be used in the future to control the traffic light sign by giving each sign sufficient time, depending on the number of cars on each direction.

#### 摘录 B
- 出处：第 5 页，Vehicle counting stage, 行 242-247
> In my paper we use also from Foreground Detector Blob Analysis function. This function detects the vehicles and then from bounding box we get the size of the detected vehicles. ... It’s considered as the last stage in my paper, it gives the number of cars according to the number of boxes detected around the cars.

### 2. 基于原文整理后的自然语言描述

The controller captures image sequences from cameras mounted with the traffic light and filters the scene to isolate vehicles while removing irrelevant objects. It counts detected cars from bounding boxes and uses the resulting density of each direction to assign sufficient signal time for that approach.

### 3. 逐句溯源

1. 句子 1：The controller captures image sequences from cameras mounted with the traffic light and filters the scene to isolate vehicles while removing irrelevant objects.
   对应摘录：A
2. 句子 2：It counts detected cars from bounding boxes and uses the resulting density of each direction to assign sufficient signal time for that approach.
   对应摘录：A, B
