# Design of Control System for Automatic Bamboo Splitting Equipment Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把破竹设备的送料、选刀、对中、夹持和切割链写成了完整 PLC 自动化流程，并明确了传感器、阈值和安全替代人工的控制语义。

## 条目 1: Automatic Feeding, Tool Selection, Alignment, and Cutting
- 控制对象：自动破竹机的 PLC 送料、选刀、对中与切割控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是竹材加工领域的自动破竹机控制系统，用 PLC 协调输送带送料、刀盘选刀、抓取夹持、中心对准和最终切割，以替代人工视觉选刀和危险手工送料。
- 判断：算。对象是实际离散制造设备控制系统，原文把阶段划分、传感器测量、刀具选择依据、夹持阈值和切割完成链都写得比较完整。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`2.1 System Summary`，`paper_content.txt` 第 95-108 行
> The control system is mainly divided into the following several parts: bamboo tube feeding, blade choice, bamboo centering, bamboo cutting. Bamboo tube feeding namely bamboo timber transport to the designated cutting position, and choose system specified by the blade on the tool dish blade model, finally by a central system aim the bamboo center and the center of the blades, for cutting.
>
> Described BSE automatic switch cutter device can be mounted to the rest of 4 tool dish, tool plate can be installed on the number of the blade is 12 ~ 15. Bamboo diameter that can be processed in the range of 60 ~ 120 mm. The gripping device can grab the bamboo for 2 ~ 2.5 kg, the length of 1500 ~ 2500 mm.

#### 摘录 B
- 出处：第 4 页，`2.2 Bamboo Tube Feeding System`，`paper_content.txt` 第 109-125 行
> Bamboo tube feeding system performed by ladder type conveyor belt. Using PLC control motor speed and pause, bamboo was sent to cutting machine.
>
> ... it can use more simple control process will transfer bamboo timber to the specified location, to deliver goods, speed automatically according to the distance between the two items can transform to prevent collision between the articles; can realize fault alarm, status indication, the conveyor belt load soft start, etc.; to realize automatic and manual state switch, convenient maintenance. The system mainly uses the PLC, sensors, relays, inverter and other components, good automatic control performance by using PLC, to realize to control by no one in the process of assembly line conveyor belt transmission.

#### 摘录 C
- 出处：第 4-5 页，`2.3 Blade Selection System`，`paper_content.txt` 第 130-149 行
> Blade selection system is the most crucial part of the machine control system among the whole automatic BSE ... bamboo is often need to be processed into different size materials. Method is general by manual operation, namely estimate its diameter by staff visual bamboo, artificially turn the tool dish, then cut bamboo. This method is not only a waste of resources, easy to cause error, to threaten the safety of operating personnel importantly.
>
> This system adopted the control mode of automatic measurement of bamboo diameter and the choice of tool, in order to overcome this problem.
>
> From the above, we can see that there are 4 contact points between the bamboo grasp tool and bamboo, and the spatial position of the 4 contact points can be obtained by using the sensor ... get the fitting the diameter of the circle, as the parameter compared with 4 cutter diameter of cutter head on, to get the suitable cutting tool.

#### 摘录 D
- 出处：第 5-6 页，`2.4 Bamboo Tube Alignment System`，`paper_content.txt` 第 188-220 行
> The automatic centering device is a device which is used for positioning and clamping at the same time ... According to the uniform motion or rotation principle of the positioning and clamping elements, the system realizes the centering and clamping ... The clamping force directly affects the processing reliability, the clamping deformation, the positioning accuracy and the processing precision of bamboo. ... the force sensor on the grasping tool plays an important role.
>
> Because of the space fitting circle have been completed, can easily find the spatial coordinates of the bamboo tube fitting section circle cross, with constant speed movement principle of clamping device can realize automatic clamping action. Using the grab tool and the position sensor of the cutting table, the center of the bamboo and the center of the blade can be aligned. After the alignment is finished, the pressure sensor of the grab tool reaches the threshold. In the end, the bamboo is fed into the blade by the cutting table and the grasping tool, and the automatic cutting of the bamboo is finished.

### 2. 基于原文整理后的自然语言描述

The PLC-based bamboo-splitting controller organizes the machine into bamboo feeding, blade choice, bamboo centering, and bamboo cutting, where bamboo is transported to the designated cutting position, matched with a specified blade on the tool dish, centered against the blade, and then cut. The feeding subsystem uses a ladder conveyor whose PLC-controlled motor speed and pause move bamboo to the target position, adapt the speed according to the distance between articles to avoid collisions, raise fault alarms and status indications, and switch between automatic and manual states for maintenance. The blade-selection subsystem measures four contact points on the bamboo grasp tool, fits the bamboo cross-section to obtain an equivalent diameter, and compares that diameter with the four cutter diameters on the cutter head to choose the suitable cutting tool instead of manual visual selection. After the fitting circle is known, the clamping device performs automatic clamping, aligns the bamboo center with the blade center through the grab tool and position sensor, waits until the grab-tool pressure sensor reaches the threshold, and then feeds the bamboo into the blade to finish automatic cutting.

### 3. 逐句溯源

1. 句子 1：The PLC-based bamboo-splitting controller organizes the machine into bamboo feeding, blade choice, bamboo centering, and bamboo cutting, where bamboo is transported to the designated cutting position, matched with a specified blade on the tool dish, centered against the blade, and then cut.
   对应摘录：A
2. 句子 2：The feeding subsystem uses a ladder conveyor whose PLC-controlled motor speed and pause move bamboo to the target position, adapt the speed according to the distance between articles to avoid collisions, raise fault alarms and status indications, and switch between automatic and manual states for maintenance.
   对应摘录：B
3. 句子 3：The blade-selection subsystem measures four contact points on the bamboo grasp tool, fits the bamboo cross-section to obtain an equivalent diameter, and compares that diameter with the four cutter diameters on the cutter head to choose the suitable cutting tool instead of manual visual selection.
   对应摘录：C
4. 句子 4：After the fitting circle is known, the clamping device performs automatic clamping, aligns the bamboo center with the blade center through the grab tool and position sensor, waits until the grab-tool pressure sensor reaches the threshold, and then feeds the bamboo into the blade to finish automatic cutting.
   对应摘录：D
