# Embedded Device Berbasis PLC pada Miniatur Konveyor untuk Pengoperasian Simulator Rejection System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把瓶盖缺失/压盖不良的检测、等待对位、步进电机拒收、计数与急停链都写得很完整，是一条细节足够扎实的制造质检顺序控制样本。

## 条目 1: Bottle-Cap Defect Detection and Rejector-Arm Controller

- 控制对象：工业自动化与离散制造领域的瓶盖缺陷检测与拒收臂控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个安装在小型输送带上的拒收控制器，利用 `proximity #1/#2/#3` 和 `optical sensor` 检查瓶盖缺失或压盖不良，并在瓶子对齐时驱动步进电机带动 rejector 臂将缺陷瓶推出输送带。
- 判断：算。对象是论文主系统，原文明确给出传感器职责、步进电机动作、自动/手动模式、30 ms 右转脉冲和等待对位后再执行拒收的时序链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 19-31 行
> A PLC-based embedded device on a miniature conveyor machine for operating a rejection system has been designed and constructed.
>
> Programming based on ladder diagram carried out by determining algorithms, compiling the ladder diagram, addressing the input/output, and compiling and uploading the program from PC to PLC.
>
> observation and measurement of the processing time of the rejection arm.

#### 摘录 B

- 出处：第 4-5 页，`Simulator rejection system`，`paper_content.txt` 第 403-441 行
> #01: Proximity sensor #1 (tutup botol tidak baik, not okay)
> #02: Proximity sensor #2 (tidak ada tutup botol)
> #03: Optic sensor (posisi botol baik)
> #04: Motor stepper penggerak lengan rejection system
>
> motor stepper beroperasi setelah posisi botol tepat berada sejajar dengan lengan rejector dan counter dalam pengitungan setiap botol yang terdeteksi tidak tertutup sempurna di bagian tutup botol.

#### 摘录 C

- 出处：第 7 页，`Algoritma, penyusunan ladder, dan pemberian alamat`，`paper_content.txt` 第 652-666 行
> I005 Proximity sensor #1 pembaca keberadaan botol
> I006 Proximity sensor #2 tidak ada tutup
> I007 Proximity sensor #3 tutup tidak press
> I008 Optical Sensor untuk posisi botol, penggerakan posisi lengan rejector
> ...
> Q000 Pul +5 Driver
> Q001 Pul - Dir Driver
> Q002 Counter
> Q005 R1
> Q006 R2

#### 摘录 D

- 出处：第 8-10 页，`3.3 Kinerja ...`，`paper_content.txt` 第 709-787、855-905 行
> Saat rejection system dalam pilihan mode auto ... Sesaat setelah botol terdeteksi sensor proximity #1 pada belt conveyor dan ketiadaan tutup botol terdeteksi oleh sensor proximity #2, motor stepper berubah ke kondisi ON, berputar ke arah kanan selama 30 mili detik (ms), counter dengan kondisi ON, setelah motor stepper OFF.
>
> Sesaat setelah botol terdeteksi oleh sensor proximity #1 dan tutup botol tidak tertutup sempurna terdeteksi oleh sensor proximity #3, motor stepper berubah ke kondisi ON berputar ke arah kanan selama 30 ms ...
>
> saat kondisi pembaca tutup tidak sempurna sensor #03 dan #02 ON, kondisi lengan rejector masih diam ... sampai posisi botol sejajar dengan lengan rejector ... kemudian lengan rejector beroperasi, botol terdorong.
>
> saat sensor #2 dan #3 kondisi ON, maka motor stepper untuk penggerak lengan rejector dapat berfungsi dengan tepat dalam pendorongan terhadap botol dengan kondisi tutup tidak sempurna.

### 2. 基于原文整理后的自然语言描述

The rejection unit is a PLC-controlled defect-handling controller for a bottle-cap inspection conveyor rather than a generic inspection setup. In automatic mode, the conveyor runs while `proximity sensor #1` confirms bottle presence and `proximity sensor #2` or `#3` identifies either a missing cap or a cap that is present but not properly pressed. Once a defect condition is latched, the rejector does not fire immediately; instead, the controller waits until the optical position sensor confirms that the bottle is aligned with the rejector arm, which preserves a clear state progression from defect detection to geometric alignment. The PLC then drives the stepper motor to rotate right for `30 ms`, turns the counter on, and pushes the bottle out of the conveyor path before the arm returns and the line continues. The same implementation also exposes `manual` mode for direct conveyor and stepper actuation and an `emergency stop` path that forces the whole simulator into the OFF state, so the paper preserves both normal rejection and maintenance/safety branches in one coherent control chain.

### 3. 逐句溯源

1. 句子 1：The rejection unit is a PLC-controlled defect-handling controller for a bottle-cap inspection conveyor rather than a generic inspection setup.
   对应摘录：A, B
2. 句子 2：In automatic mode, the conveyor runs while `proximity sensor #1` confirms bottle presence and `proximity sensor #2` or `#3` identifies either a missing cap or a cap that is present but not properly pressed.
   对应摘录：B, C, D
3. 句子 3：Once a defect condition is latched, the rejector does not fire immediately; instead, the controller waits until the optical position sensor confirms that the bottle is aligned with the rejector arm, which preserves a clear state progression from defect detection to geometric alignment.
   对应摘录：B, D
4. 句子 4：The PLC then drives the stepper motor to rotate right for `30 ms`, turns the counter on, and pushes the bottle out of the conveyor path before the arm returns and the line continues.
   对应摘录：D
5. 句子 5：The same implementation also exposes `manual` mode for direct conveyor and stepper actuation and an `emergency stop` path that forces the whole simulator into the OFF state, so the paper preserves both normal rejection and maintenance/safety branches in one coherent control chain.
   对应摘录：C, D
