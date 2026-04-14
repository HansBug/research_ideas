# Fuzzy Logic Control of Autonomous Vehicles for Parallel Parking Maneuver - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把并联泊车划分成三步，并说明每一步都配置独立模糊控制器，结构非常适合顺序控制样本。

## 条目 1: Three-Step Parallel Parking Process
- 控制对象：智慧停车领域的自主车辆并联泊车控制器
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个自主车辆并联泊车控制器，用于扫描停车位、执行倒车入位并在末段前进微调位置。
- 判断：算。对象是实际自动泊车控制器，原文明确写出了停车过程的分步结构和每一步的目标。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Automated Parking Process，行 83-98
> the parking process was divided into three steps and a fuzzy controller was designed for each of the steps. The three steps are: 1) parking space scanning while reaching a ready to reverse position, 2) reversing the vehicle into the parking space, and 3) adjusting the vehicle forward inside the parking space. In the ﬁrst step, the vehicle is navigated forward to reach a ready-to-reverse position with the vehicle’s orientation parallel to the available space. The parking space is also scanned using either image sensors or ultrasonic sensors ... The ready-to-reverse position for the center of the vehicle is chosen as (lp + 0.5l, hp + 0.65b) ... this step is divided into two substeps.

#### 摘录 B
- 出处：第 5-9 页，Fuzzy Logic Controllers，行 120-147
> In the second step of parallel parking, the vehicle is ﬁrst backed up into the parking space with an increasing θ until its right rear wheel is at a certain distance from the boundary SE of the space. Then the vehicle is backed up with decreasing θ until one of the rear wheels is very close to the boundary BK of the space. In the third step the vehicle is moved forward to adjust its position inside the space. The second and third steps can be repeated several times until the desired ﬁnal position is reached with some tolerance. ... The fuzzy logic controller has three inputs, xa1, yd1 and the orientation angle θ. The output of the fuzzy controller is the steering rate θ˙ ... there are a total of 18 rules.

#### 摘录 C
- 出处：第 5-10 页，goal-seeking / simulation，行 103-119, 205-213
> The task of the ﬁrst substep is to have the vehicle reach an intermediate position ((0.9lp, hp + 0.65b) for the vehicle’s center) without considering the orientation angle of the vehicle ... In the second substep, the orientation angle is adjusted while the vehicle moves forward to reach the desired x position. ... Figures 7 to 10 show the whole parking process ... It was seen that the vehicle moves back and forth twice within the parking space to reach the desired position.

### 2. 基于原文整理后的自然语言描述

The parking controller divides the whole parallel-parking process into three steps, and a dedicated fuzzy controller is designed for each step. In step 1, the vehicle scans the candidate parking space with image or ultrasonic sensors while moving to the ready-to-reverse position `(lp + 0.5l, hp + 0.65b)`, and this step is itself split into a goal-seeking substep that reaches the intermediate position `(0.9lp, hp + 0.65b)` and an orientation-adjustment substep that makes the heading nearly parallel to the space. In step 2, the reverse controller uses the relative-position variables `xa1` and `yd1` together with the orientation angle `θ` to back the vehicle into the space, first increasing `θ` until the right rear wheel reaches the desired distance from boundary `SE`, and then decreasing `θ` until one rear wheel is very close to boundary `BK`. In step 3, the vehicle moves forward to adjust its position inside the space, and steps 2 and 3 may be repeated until the final position is centered in the parking space and parallel to it within the required tolerance.

### 3. 逐句溯源

1. 句子 1：The parking controller divides the whole parallel-parking process into three steps, and a dedicated fuzzy controller is designed for each step.
   对应摘录：A
2. 句子 2：In step 1, the vehicle scans the candidate parking space with image or ultrasonic sensors while moving to the ready-to-reverse position `(lp + 0.5l, hp + 0.65b)`, and this step is itself split into a goal-seeking substep that reaches the intermediate position `(0.9lp, hp + 0.65b)` and an orientation-adjustment substep that makes the heading nearly parallel to the space.
   对应摘录：A, C
3. 句子 3：In step 2, the reverse controller uses the relative-position variables `xa1` and `yd1` together with the orientation angle `θ` to back the vehicle into the space, first increasing `θ` until the right rear wheel reaches the desired distance from boundary `SE`, and then decreasing `θ` until one rear wheel is very close to boundary `BK`.
   对应摘录：B
4. 句子 4：In step 3, the vehicle moves forward to adjust its position inside the space, and steps 2 and 3 may be repeated until the final position is centered in the parking space and parallel to it within the required tolerance.
   对应摘录：B, C
