# Development of Automatic Packaging System using PLC and SCADA for Industries - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文把包装线拆成 bottle filling、case erector、6 瓶装箱、自动贴带和称重剔除等多个顺序段，适合沉淀多个离散控制样本。

## 条目 1: Bottle Cleaning-Filling-Capping Line
- 控制对象：包装产线前端的瓶清洗、灌装与封盖控制段

### 0. 条目识别与判定
- 一句话说明：这是工业包装领域的前端灌装线控制器，用于驱动瓶子依次通过清洗、灌装、封盖并送往后续装箱工位。
- 判断：算。对象是实际包装产线控制段，原文明确写出了从主入口到 cleaner、main tank/valve、capping machine 和 exit gate 的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，4.1 Bottle Filling Process，行 149-157
> Each step which is included in bottle filling i.e. cleaning, washing, liquid filling and capping are made automatic and this wholesome process is showcased on a single screen as shown in Fig.9. As shown firstly the un-cleaned bottles come from the main entry gate; then this bottles pass through a cleaner where through a combined process of washer and cleaner these bottles gets cleaned. Now these cleaned bottles further move towards main tank and valve for filling these bottles with the desired liquid. After filling process, these bottles pass through a capping machine where capping of these bottles is done. Now these capped bottles pass through an exit gate to further pack these bottles in an erected box.

### 2. 基于原文整理后的自然语言描述

The automatic packaging line first brings uncleaned bottles through the main entry gate and sends them through a cleaner that performs washing and cleaning. The cleaned bottles then move to the main tank and valve so that they can be filled with the desired liquid. After filling, the bottles pass through the capping machine and then leave through the exit gate toward the erected-box packing section.

### 3. 逐句溯源

1. 句子 1：The automatic packaging line first brings uncleaned bottles through the main entry gate and sends them through a cleaner that performs washing and cleaning.
   对应摘录：A
2. 句子 2：The cleaned bottles then move to the main tank and valve so that they can be filled with the desired liquid.
   对应摘录：A
3. 句子 3：After filling, the bottles pass through the capping machine and then leave through the exit gate toward the erected-box packing section.
   对应摘录：A

## 条目 2: Six-Bottle Carton Packing and Quality Gate
- 控制对象：包装产线后端的装箱、封箱与称重放行/剔除控制段

### 0. 条目识别与判定
- 一句话说明：这是包装线后端的离散控制段，用于将 6 瓶成组装箱、自动贴带，并根据称重结果决定放行还是剔除。
- 判断：算。对象是实际包装产线控制系统，原文明确写出了 `count=6` 装箱门控、自动贴带以及 green/red/yellow 称重分流逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7 页，4.2 Case Erector / 4.3 Filling Section，行 166-179
> The conveyor combination keeps the flow of cases in-line ... Pressure is applied on the flat box which is moving on the conveyor and two pneumatic arms pulls the box through pressure and puts the box into the second conveyor for further filling of the bottles into these erected boxes ... Each carton is packed with the pack of 6 bottles through this automated process ... In this section the gate only gets opened when the bottle count=6 and further through an automatic counter and sensor operation a bunch of 6 bottles gets filled in the carton boxes to move ahead this box for further taping processes.

#### 摘录 B
- 出处：第 8 页，4.4 Taping Section / 4.5 Weighing Section，行 185-201
> In this section the filled boxes are taped to ensure the safety of the products inside the box. ... when the carton box moves through this machine, the boxes gets taped. The taping is done automatically through a PLC program ... The taped boxes pass through a weighing transmitter in which weighing of boxes is done. When the weight of box is correct ... then the LED flashes green and this box is accepted ... When the weight of box is incorrect ... then the LED flashes red and this box is reject and it is moved away from the conveyor through an setup of pushing pistons ... When the transmitter is empty, then the LED flashes yellow ...

### 2. 基于原文整理后的自然语言描述

The case-erector section keeps the box flow in line, uses pneumatic arms to erect the flat boxes, and transfers them to the next conveyor for bottle loading. In the filling section, the gate opens only when the bottle count reaches six, and an automatic counter together with sensors loads a group of six bottles into each carton. After loading, the cartons are taped automatically, and the weighing stage accepts correctly weighted boxes with a green indication while rejecting underweight boxes with a red indication and ejecting them from the conveyor.

### 3. 逐句溯源

1. 句子 1：The case-erector section keeps the box flow in line, uses pneumatic arms to erect the flat boxes, and transfers them to the next conveyor for bottle loading.
   对应摘录：A
2. 句子 2：In the filling section, the gate opens only when the bottle count reaches six, and an automatic counter together with sensors loads a group of six bottles into each carton.
   对应摘录：A
3. 句子 3：After loading, the cartons are taped automatically, and the weighing stage accepts correctly weighted boxes with a green indication while rejecting underweight boxes with a red indication and ejecting them from the conveyor.
   对应摘录：B
