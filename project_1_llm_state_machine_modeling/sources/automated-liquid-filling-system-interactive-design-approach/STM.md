# Development of Automated Liquid Filling System Based on the Interactive Design Approach - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把激光定位、相机采图、模板匹配、液位判停和输送带放行写成了完整的视觉闭环灌装控制链，是一条明显区别于普通定时灌装的双 A 样本。

## 条目 1: Laser-Triggered Vision-Verified Liquid Filling Controller

- 控制对象：工业自动化与离散制造领域的激光定位、视觉液位匹配与输送放行灌装控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个低成本自动灌装控制器，使用激光传感器定位瓶子、相机连续采图、边缘检测与模板匹配判定液位，再由 `Arduino` 控制输送带和泵完成灌装放行。
- 判断：算。对象是实际自动灌装控制系统，不是单纯图像处理方法展示；原文把传感器、执行器、停止条件和放行条件都写得很具体。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 27-34 行、第 55-58 行
> The new proposed system consists of a conveyor subsystem, filling stations, and camera to detect the level of the liquid at any instant during the filling process ... Arduino board is used as the controller unit in the automatic operation of developed filling system.
>
> When the laser sensor detects the bottle at the predefined position, the motor of the conveyor will be stopped automatically.

#### 摘录 B

- 出处：第 2 页，`Introduction / Description and Performance`，`paper_content.txt` 第 89-107 行、第 112-123 行
> The bottle is stopping under the filling section by laser sensor, and the camera starts capturing many images to detect the level of the liquid. The developed design is based on the open-loop system which can control conveyor by laser sensor, and make sure that the bottle doesn’t overflow ...
>
> The Automated liquid filling system consists of the conveyor system, stepper motor, pump, Arduino board, power supply, camera and laser sensor ...

#### 摘录 C

- 出处：第 2 页，`Description and Performance`，`paper_content.txt` 第 124-136 行
> The conveyor belt moves the empty bottle to the fill section. Then, the laser sensor will stop the bottle at the specific point that is located under the fill pipe. After the bottle arrives at the filling site, the filling process begins, and the camera starts capturing images. Then immediately the image analysis is performed if the image matches the image template or not ... the camera continuously captures the images until the level of fluid reaches the required level in the bottle. After filling the bottle, the camera gives a signal to the Arduino board which in turn gives a signal to the conveyor belt to move on.

#### 摘录 D

- 出处：第 4-6 页，`Theoretical methodology / Results and Discussion`，`paper_content.txt` 第 204-220 行、第 398-410 行
> Each image will be processed by the edge detection method and then will be compared with the template image that saved earlier. Any captured image will be checked if matched with the template or not ... The optimal method that gave results with high accuracy is the Prewitt edge detection method.
>
> The Prewitt method is the most optimal method for such system. It succeeded to detect accurately the required level of water in the bottle ... When the edge detection is applied, the system is matching the base image with the image that is under processing. If the matching percentage is greater than 90%, the decision is to stop the filling process and move the conveyor belt to fill the next bottle.

### 2. 基于原文整理后的自然语言描述

The developed filling machine is an Arduino-based sequential controller for a conveyor, pump, laser sensor, camera, and image-analysis module rather than a simple timer-based filler. A laser sensor stops each incoming bottle at the fill position and triggers the camera to start capturing images while filling begins. The controller keeps processing the captured frames with edge detection and template matching, and the paper explicitly selects `Prewitt` as the preferred detector for this task. When the current image matches the stored template with a percentage greater than `90%`, the system decides that the required liquid level has been reached, stops filling, and commands the conveyor to move the next bottle into place. Because bottle spacing is handled by the laser sensor and the method is validated on different bottle volumes and transparent bottles, the core control chain is built around position detection, vision-validated fill completion, and conveyor release.

### 3. 逐句溯源

1. 句子 1：The developed filling machine is an Arduino-based sequential controller for a conveyor, pump, laser sensor, camera, and image-analysis module rather than a simple timer-based filler.
   对应摘录：A, B
2. 句子 2：A laser sensor stops each incoming bottle at the fill position and triggers the camera to start capturing images while filling begins.
   对应摘录：A, C
3. 句子 3：The controller keeps processing the captured frames with edge detection and template matching, and the paper explicitly selects `Prewitt` as the preferred detector for this task.
   对应摘录：C, D
4. 句子 4：When the current image matches the stored template with a percentage greater than `90%`, the system decides that the required liquid level has been reached, stops filling, and commands the conveyor to move the next bottle into place.
   对应摘录：C, D
5. 句子 5：Because bottle spacing is handled by the laser sensor and the method is validated on different bottle volumes and transparent bottles, the core control chain is built around position detection, vision-validated fill completion, and conveyor release.
   对应摘录：B, D
