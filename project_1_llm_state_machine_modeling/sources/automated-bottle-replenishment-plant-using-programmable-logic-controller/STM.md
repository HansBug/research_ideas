# Automated Bottle Replenishment Plant using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把瓶体检测、大小瓶分支、缺陷剔除、定量灌装、封盖和末端分流写成了多支路 `PLC` 顺序控制链，细节密度明显高于普通短流程灌装稿。

## 条目 1: Bottle-Size-Aware Filling-Capping and Defect-Rejection Controller

- 控制对象：工业自动化与离散制造领域的瓶型判别、灌装封盖与缺陷剔除控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个多输送带瓶装生产单元控制器，围绕 `IR` 传感器、大小瓶开关、质量检测、灌装泵、封盖执行器、缺陷瓶 crusher 和末端分拣完成整线顺序控制。
- 判断：算。对象是实际瓶装/封盖离散制造控制系统，原文不仅给出了主流程，还明确写出了多类传感器、储液 tank 级联、定时灌装和缺陷剔除分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Introduction`，`paper_content.txt` 第 32-43 行
> The aim of this project is to design PLC Based automatic bottle filling system that sense the presence of bottle and level of liquid in it and then fills it accordingly up to a fixed level ... Our paper aims at filling and capping bottles simultaneously. The filling and capping operation takes place in a synchronized manner. It also includes a user-defined volume selection menu through which the user can input the desired volume to be filled in the bottles.

#### 摘录 B

- 出处：第 2 页，`Methodology / Process Description`，`paper_content.txt` 第 61-76 行
> Bottles are kept in position over a conveyor belt. An IR sensor is used to detect their presence. Next is a switch which will be in OFF condition when a large bottle will come then the switch will be in ON condition. Then there is a sensor which controls the quality of the bottles. Depending on the output of the switch the corresponding pumps switch on and filling operation takes place i.e. for large and small bottles. If the particular bottle is defective then the both pumps are off and the bottle is rejected and the bottle is thrown away from the main conveyor and pushed to the crusher situated below.
>
> Once the box is filled the level sensor is ON and the conveyor moves and next empty box came. Now the filled bottle is sealed by cap. Next is an sensor which detects the size of the bottle, if it large it will be bring down to the third conveyor and the small one will move forward on the same conveyor for further packaging.

#### 摘录 C

- 出处：第 2-3 页，`Input Module / Series of Operations / User-Defined Volume`，`paper_content.txt` 第 83-91 行、第 142-165 行
> There are four pairs of IR sensors ... three pairs ... used to detect the bottles at the input and one more is used to sense the bottles for filling and capping operations ... Two level sensors are used in tank 1 ... two sensors are used in tank 2 ... Three level sensors are used in the process tank ...
>
> Once the bottles are detected in the input side the conveyor motor switches ON ... The bottles then reach the desired position for filling and the conveyor stops. The corresponding pumps in process tank switch ON ... When the liquid in the process tank reaches below low level (LLS) pumps in tank 1 and tank 2 switches on ... When the level of liquid reaches high level (HLS) the pumps in tank 1 and 2 switch off.
>
> The filling is done using timing operations. Thus the pump remains on for the preset value of the timer and switches off once time is out.

#### 摘录 D

- 出处：第 4 页，`Capping Operation`，`paper_content.txt` 第 178-188 行
> The bottles are transported to the capping arrangement. IR sensors are kept to stop the bottles in the desired position for capping to take place. Once the bottles reach the position the conveyor motor switches OFF. The capping of bottles is done using actuator arrangement. Three actuators which move in forward and reverse directions are used to cap the bottles ... Similar to filling, if a particular bottle is not present it does not get capped. Thus the capping is done and the conveyor starts moving again. When the capping operation for one batch is done simultaneously the filling operation for another batch takes place.

### 2. 基于原文整理后的自然语言描述

The bottle-replenishment plant is a PLC-driven production-line controller that synchronizes bottle detection, size discrimination, defect rejection, filling, capping, and final routing instead of only implementing a short fill cycle. At the front end, an `IR` sensor confirms bottle presence, a size switch distinguishes large and small bottles, and a quality sensor can divert defective bottles away from the main conveyor to a crusher and box-collection branch. For valid bottles, the conveyor stops at the filling position, the selected process pump runs, and the process tank is automatically replenished from the concentrate and water tanks when `LLS` is reached and stopped again at `HLS`. The actual fill quantity is governed by a user-selected volume and a preset timer, so the pump turns off when the timer expires and the conveyor restarts. Downstream `IR` stop sensing and three actuators perform capping only for present bottles, and a final size sensor routes large bottles to the third conveyor while small bottles continue on the main line for packaging.

### 3. 逐句溯源

1. 句子 1：The bottle-replenishment plant is a PLC-driven production-line controller that synchronizes bottle detection, size discrimination, defect rejection, filling, capping, and final routing instead of only implementing a short fill cycle.
   对应摘录：A, B
2. 句子 2：At the front end, an `IR` sensor confirms bottle presence, a size switch distinguishes large and small bottles, and a quality sensor can divert defective bottles away from the main conveyor to a crusher and box-collection branch.
   对应摘录：B
3. 句子 3：For valid bottles, the conveyor stops at the filling position, the selected process pump runs, and the process tank is automatically replenished from the concentrate and water tanks when `LLS` is reached and stopped again at `HLS`.
   对应摘录：C
4. 句子 4：The actual fill quantity is governed by a user-selected volume and a preset timer, so the pump turns off when the timer expires and the conveyor restarts.
   对应摘录：A, C
5. 句子 5：Downstream `IR` stop sensing and three actuators perform capping only for present bottles, and a final size sensor routes large bottles to the third conveyor while small bottles continue on the main line for packaging.
   对应摘录：B, D
