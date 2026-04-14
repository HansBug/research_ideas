# Application of Industrial IoT in Developing a Sustainable and Automatic Liquid Filling Plant - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多规格瓶子的检测、对应阀位灌装和末端颜色分拣写成一条完整 PLC 控制链，并给出 `20 s / 30 s / 50 s / 10 s` 定时。

## 条目 1: Multi-Height Bottle Detection and Timed Filling-Sorting

- 控制对象：工业自动化领域的多规格瓶装灌装与颜色分拣控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个瓶装液体灌装与分拣控制器，用于根据瓶高识别结果选择对应阀位、定时灌装并在末端输出对应颜色分拣信号。
- 判断：算。对象是实际工业灌装产线控制系统，原文不仅给出高度检测和阀门动作，还给出时序、位锁存和末端分拣逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`Abstract / III. MATERIALS AND METHODS`
> The system is designed to automatically fill and sort bottles based on their height ... The proposed solution involves filling three differently sized bottles simultaneously through a detection mechanism ... To differentiate between small, medium, and large bottles, the IR sensors are configured to activate based on specific heights ... The PLC interprets these signals and latches another bit, indicating the presence of a medium-sized bottle ... By utilizing this detection mechanism, the PLC can accurately determine the height of each bottle passing through the sensor tower.

#### 摘录 B

- 出处：第 7-8 页，`IV. PROPOSED SYSTEM AND ALGORITHM / 4.3 DEVELOPMENT OF PLANT`
> if all three IR sensors detect the presence of the bottle ... start that specific timer (say T4:1) ... else if two IR sensors detect the presence of the bottle ... start that specific timer (say T4:2) ... else only one IR sensor detect the presence of the bottle ... start that specific timer (say T4:3) ... if bottle reaches the fourth IR sensor: open the solenoid valve (red) ... Height of the bottle: Small Sized Bottle, Red Liquid for 20 sec; Medium sized bottle, Green Liquid for 30 sec; Large sized bottle, Blue Liquid for 50 sec ... the last IR sensor detects the presence of a bottle ... an indicator light of a corresponding color is illuminated for a duration of 10 seconds ... Afterward, the conveyor belt restarts, and the entire process repeats for the subsequent bottles.

### 2. 基于原文整理后的自然语言描述

The plant starts by moving bottles along the conveyor and classifying each bottle height through a tower of three IR sensors whose activation pattern is latched into PLC bits. Depending on whether one, two, or three sensors are active, the controller starts a corresponding timer and routes the bottle to the matching filling position. When the bottle reaches the target valve sensor, the PLC opens the red, green, or blue solenoid valve and keeps it open for a preset duration of about twenty, thirty, or fifty seconds according to bottle size. After filling, the final IR sensor uses the earlier latched height bits to illuminate the matching sorting indicator for ten seconds, and then the conveyor resumes so the same cycle can be repeated for the next bottle.

### 3. 逐句溯源

1. 句子 1：The plant starts by moving bottles along the conveyor and classifying each bottle height through a tower of three IR sensors whose activation pattern is latched into PLC bits.
   对应摘录：A, B
2. 句子 2：Depending on whether one, two, or three sensors are active, the controller starts a corresponding timer and routes the bottle to the matching filling position.
   对应摘录：A, B
3. 句子 3：When the bottle reaches the target valve sensor, the PLC opens the red, green, or blue solenoid valve and keeps it open for a preset duration of about twenty, thirty, or fifty seconds according to bottle size.
   对应摘录：B
4. 句子 4：After filling, the final IR sensor uses the earlier latched height bits to illuminate the matching sorting indicator for ten seconds, and then the conveyor resumes so the same cycle can be repeated for the next bottle.
   对应摘录：B
