# Design of an Automated Secure Garage System Using License Plate Recognition Technique - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以 LPR 为入口，但对授权判定后的车库门禁控制链写得很完整，包括前后两块重量感应板、横杆与滑门联动、授权放行和离开后自动关门。

## 条目 1: LPR-authorized garage gate and sliding-door controller

- 控制对象：楼宇机电与电梯控制领域的授权车库门禁与滑门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个将车牌识别结果接入车库门禁控制的系统，控制对象是横杆与双侧滑门的自动开闭链。
- 判断：算。虽然论文包含大量 OCR 说明，但门禁控制部分提供了足够完整的输入、判定、执行机构和闭门反馈逻辑，适合提取为 EFSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Systematically process of the system
> As soon as the car appears in the front gate, it will activate a sensor which will be liked with a central control system. The system grabs a picture of the license plate and analyses the reference cars’ license plate number. After a successful match, the garage opens automatically allowing the car to get in.

#### 摘录 B

- 出处：第 2 页，Figure 1 steps
> Step1 The car approaches in front of the garage and the wheel touches a plate. ... Step4 Image form references are taken and then converted into text. Then the both texts are compared. If the image matches, it gives logic 1 to step 5. Step5 If step 4 gives logic 1, then the motor interfaced by PC rotates and the sliding and cross bar gates open.

#### 摘录 C

- 出处：第 2 页，Figure 1 steps
> Step6 When the car passes the gate, it touches another plate twice (for the front wheel and the back wheel). This sends two simultaneous signals to the PC. Step7 Then the motor rotates back to close both the doors.

#### 摘录 D

- 出处：第 2-3 页，Overview of the Mechanical Part
> The driveway has two sensors at two different places, one before approaching the gate and another just after the gate. ... The gate has two parts. One crossing bar which is in front of the gate and horizontally siding doors that are next to the crossing bar. ... The sliding doors have rack attached with it on the top. This rack meshes with a pinion that is coupled with two stepper motors. The crossing bar also has a motor coupled, which is used to move the crossing bar up and down.

#### 摘录 E

- 出处：第 3 页，Comparison of the license plate
> After comparing the two texts in MATLAB, we defined a variable, which will get logic 1, and we will run a loop in the three motors to open the garage doors and pulley using smart controlling features.

#### 摘录 F

- 出处：第 6 页，Performance Analysis
> When we bring a car having a number plate of CTG 253, it senses the number and passes the car by opening the gate. After it passes the second plate, the gates get closed.

### 2. 基于原文整理后的自然语言描述

The secure garage controller begins when an approaching car presses the first weight plate in front of the gate. That input triggers image capture and OCR processing, and the recognized plate text is compared with the authorized reference list. If the comparison returns logic `1`, the controller drives three motors so that the crossing bar rises and the two sliding doors open to create the passage. The car then moves through the garage entrance and activates the second plate after the gate, which is expected to be contacted twice by the front and rear wheels. Those exit-plate signals cause the motors to rotate in the opposite direction and close both the sliding doors and the barrier, returning the gate to its original secured state.

### 3. 逐句溯源

1. 句子 1：The secure garage controller begins when an approaching car presses the first weight plate in front of the gate.
   对应摘录：A, B, D
2. 句子 2：That input triggers image capture and OCR processing, and the recognized plate text is compared with the authorized reference list.
   对应摘录：A, B, E
3. 句子 3：If the comparison returns logic `1`, the controller drives three motors so that the crossing bar rises and the two sliding doors open to create the passage.
   对应摘录：B, D, E
4. 句子 4：The car then moves through the garage entrance and activates the second plate after the gate, which is expected to be contacted twice by the front and rear wheels.
   对应摘录：C, D
5. 句子 5：Those exit-plate signals cause the motors to rotate in the opposite direction and close both the sliding doors and the barrier, returning the gate to its original secured state.
   对应摘录：C, F
