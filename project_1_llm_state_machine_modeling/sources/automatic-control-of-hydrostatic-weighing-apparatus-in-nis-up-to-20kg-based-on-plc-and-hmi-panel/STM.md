# Automatic Control of Hydrostatic Weighing Apparatus in NIS Up to 20kg Based on PLC and HMI Panel - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `R-T-T-R` 校准序列、`P1/P2/P3/L1/L2` 传感链、三电机角色、稳定时间与水浴温控组织成一套自动计量流程，给 `⚙️` 方向补进了一条结构差异很强的双 A 样本。

## 条目 1: R-T-T-R hydrostatic weighing calibration supervisor

- 控制对象：通用控制与计量自动化领域的水静力称量装置自动校准监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC + HMI` 的水静力称量自动校准系统，使用三台电机、编码器、接近开关、限位开关和恒温水浴在空气/液体两种介质间执行标准砝码与被测砝码的自动称量序列。
- 判断：算。对象是实际自动计量装置，原文明确给出设备子系统、传感器与执行器、`R-T-T-R` 顺序、介质切换、稳定时间与人工/自动模式，不是单纯的实验平台介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`2. HWA-NIS Main Subsystems`，`paper_content.txt` 第 157-186 行
> The primary function of the HWA-NIS is to measure the solid density according to Archimedes principle... The system has five sub-systems: The main cabinet, balance pan, mass carrier, assembly elevating platform and the thermostatic water bath.
>
> ... Motor 1 (M1) loads and unloads the mass on the balance pan. Motor 2 (M2) selects which mass between the standard and test masses to weigh. Motor 3 (M3) is used to change the weighing medium to weigh both masses in two different mediums (air and distilled water).

#### 摘录 B

- 出处：第 3 页，`3. Circuit Diagram`，`paper_content.txt` 第 202-220 行
> The system has three motors that need to be controlled according to the sequence of operation. Each motor will operate in a forward and reverse direction.
>
> Three proximity switches are added. The first one is used for home position detection... The first motor (M1) must operate forward and reverse according to constant stroke. Therefore, two proximity switches are added. The first (P2) is used for the upper limit, while the other (P3) is used for a lower limit.
>
> ... Motor 3 (M3) is used for this operation. Therefore, two limit switches are added. The first is used for the upper limit (L1), while the second is for the lower limit (L2).

#### 摘录 C

- 出处：第 4 页，`4. System Control`，`paper_content.txt` 第 274-316 行
> The sequence is operated using the R-T-T-R sequence of operation in air and liquid. R refers to the weight of reference mass, while T refers to test mass. Firstly, the user should enter No. of cycles...
>
> ... the user enters the reference temperature value of 20℃. The water bath is controlled using a PID controller.
>
> Firstly, the PLC controller will check the home position before weighing. The home position is P1, L2, and P2 are ON. When P1 is ON, it will set the encoder angle to 0o. Then, the calibration process will start by weighing the standard mass... Then, (M2) will rotate 180o until the test mass will be concentric to the balance pan... Then, the process will be repeated until the No. of cycles.
>
> ... Then, (M3) will operate until the limit switch 1 (L1) is reached. Therefore, the masses are now immersed in the distilled water. Then, all previous sequences of weighing operation will be repeated in the distilled water using a sequence of operation R-T-T-R.

#### 摘录 D

- 出处：第 4-5 页，`5. PLC controlling the sequence of operation`，`paper_content.txt` 第 323-345, 356-377 行
> ... the user can enter No. of cycles, the delay between each weighing process and the delay time before starting the measurement. Finally, the process will start.
>
> The system can be controlled manually using the touch screen to test motors, manual calibration checks, or the presence of active sensors... An emergency switch is added for any fault.
>
> However, automatic control is used for the calibration process, and each operation takes more than three hours depending on the number of cycles, the delay time before starting the test and the delay time between each weighing process (stability time).
>
> For automatic calibration... Firstly, HWA-NIS checks that the home positions P1, P2, and L2 are ON. Then, the weighing process is ready to start. M1 operates in a forward direction till it reaches (P3). After that, stability time to let the balance be stable. Then, M2 rotates 180o ... M1 operates in a Reverse direction till it reaches (P2)... Then, the number of cycles will be checked... Else, M3 will be actuated till reaching (L1). Then, the weighing process will be repeated according to the number of cycles after the masses are immersed in the distilled water.

#### 摘录 E

- 出处：第 5-6 页，`6. Experimental Work`，`paper_content.txt` 第 412-418, 441-458 行
> The distance between P2 and P3 is 30mm... the time required to load or unload a mass is 90 sec... the time required to rotate masses 180o is 30 sec... the time required to change the medium from air to liquid is 285.7 sec.
>
> The touch screen is programmed with PLC to facilitate the weighing process... Users can check the active sensor and the angle of the encoder using channel (1)... the user can select the weighing sequence (R-T-R) or (R-T-T-R) and the weighing medium (air or liquid) using channel 2. No. Of cycles, centering stability time, No. of centering cycles, and No. Stability time can be selected using channel 3... The user can operate the system using the touch buttons shown in the last channel for manual work.

### 2. 基于原文整理后的自然语言描述

The HWA-NIS controller automates hydrostatic weighing over a main cabinet, balance pan, mass carrier, elevating platform, and thermostatic water bath, where `M1` loads or unloads a mass onto the balance pan, `M2` rotates the carrier between reference and test masses, and `M3` switches the weighing medium between air and distilled water. The control sequence is grounded on discrete sensor states: `P1` defines home position and resets the encoder to `0°`, `P2/P3` bound the vertical motion of the mass carrier, and `L1/L2` bound the elevating platform that immerses or removes the masses from the water bath. Automatic calibration follows the `R-T-T-R` cycle: the PLC first weighs the reference mass, rotates `180°` to the test mass, weighs the test mass twice, rotates back, repeats the reference weighing, and loops this pattern for the configured number of cycles before repeating the whole sequence in liquid. The same supervisor also maintains the water bath at `20℃` with PID control and inserts user-defined stability delays between weighing actions, so the measuring loop is governed by both motion states and timing constraints. Through the HMI, the operator can select `R-T-R` or `R-T-T-R`, choose air or liquid, set cycle counts and stability times, monitor sensor activity and encoder angle, or switch to manual testing and emergency interruption when needed.

### 3. 逐句溯源

1. 句子 1：The HWA-NIS controller automates hydrostatic weighing over a main cabinet, balance pan, mass carrier, elevating platform, and thermostatic water bath, where `M1` loads or unloads a mass onto the balance pan, `M2` rotates the carrier between reference and test masses, and `M3` switches the weighing medium between air and distilled water.
   对应摘录：A
2. 句子 2：The control sequence is grounded on discrete sensor states: `P1` defines home position and resets the encoder to `0°`, `P2/P3` bound the vertical motion of the mass carrier, and `L1/L2` bound the elevating platform that immerses or removes the masses from the water bath.
   对应摘录：B, C
3. 句子 3：Automatic calibration follows the `R-T-T-R` cycle: the PLC first weighs the reference mass, rotates `180°` to the test mass, weighs the test mass twice, rotates back, repeats the reference weighing, and loops this pattern for the configured number of cycles before repeating the whole sequence in liquid.
   对应摘录：C, D
4. 句子 4：The same supervisor also maintains the water bath at `20℃` with PID control and inserts user-defined stability delays between weighing actions, so the measuring loop is governed by both motion states and timing constraints.
   对应摘录：C, D, E
5. 句子 5：Through the HMI, the operator can select `R-T-R` or `R-T-T-R`, choose air or liquid, set cycle counts and stability times, monitor sensor activity and encoder angle, or switch to manual testing and emergency interruption when needed.
   对应摘录：D, E
