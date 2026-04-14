# Desain Sistem Biodiesel Berbasis PLC Berdasarkan Diagram Keadaan - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把生物柴油批处理系统直接建成 `Kondisi 1-13` 的状态图，并显式列出 `T0-T30` 转移方程、`TIM1-TIM3` 定时和阀/加热/搅拌输出，是过程控制领域非常扎实的 timed EFSM 样本。

## 条目 1: Timed biodiesel batch-sequence controller

- 控制对象：过程与环境控制领域的生物柴油批处理阀门、加热与搅拌顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把多储罐生物柴油生产流程编码成状态图与梯形图的 PLC 顺序控制器，控制多个阀门、三套加热/搅拌单元和最终成品出料。
- 判断：算。对象是真实批处理过程控制系统，原文明确给出各状态、传感器条件、定时器和停止逻辑，并把它们正式写成状态和转移方程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> Biodiesel system is a sequential system that can be controlled with a programmable logic controller (PLC) device. Sequential system problems can be solved by making a state diagram that represents the conditions and transitions of the system. Biodiesel system is represented in a state diagram then converted into a ladder diagram as one of the programming languages of a PLC.

#### 摘录 B

- 出处：第 5 页，Cara kerja sistem biodiesel
> Kondisi 1-3: Sistem diawali dengan tombol “Sistem ON” yang ditekan untuk mengaktifkan seluruh sistem dengan ditandai lampu indikator sistem menyala.
>
> Kondisi 4: Valve 1-3 akan aktif ketika tombol “Mulai” ditekan, sehingga cairan dari tangki penyimpanan akan dialirkan pada ketiga tangki ukur yang dilengkapi sensor atas (SA1-SA3) dan sensor bawah (SB1-SB3).
>
> Kondisi 5: Ketika SA1 dan SB1 tangki 1 mendeteksi cairan maka valve 1 akan mati kemudian pemanas 1 dan pengaduk 1 akan aktif selama beberapa waktu (TIM1).
>
> Kondisi 6: Ketika SA2 dan SB2 tangki 2 aktif maka valve 2 akan mati dan valve 5 hidup untuk mengalirkan cairan ke tangki pencampuran 4.
>
> Kondisi 7: Ketika SA3 dan SB3 tangki 3 aktif maka valve 3 akan mati dan valve 6 hidup untuk mengalirkan cairan ke tangki pencampuran 4.
>
> Kondisi 8: Setelah cairan pada tangki 1 dipanaskan dan diaduk maka valve 4 akan aktif untuk mengalirkan cairan ke tangki pencampuran 5.
>
> Kondisi 9: Ketika SA4 dan SB4 mendeteksi cairan pada tangki pencampuran 4, cairan akan dipanaskan dan diaduk selama beberapa waktu (TIM2).
>
> Kondisi 10: Setelah cairan pada tangki pencampuran 4 dipanaskan dan diaduk, valve 7 akan aktif dan mengalirkan cairan ke tangki pencampuran 5.
>
> Kondisi 11: Ketika SA5 dan SB5 pada tangki pencampuran 5 mendeteksi ada cairan, pemanas dan pengaduk akan aktif selama beberapa waktu (TIM3).
>
> Kondisi 12: Setelah cairan diaduk dan dipanaskan, valve 8 akan aktif untuk mengalirkan cairan ke bak penampung akhir biodiesel dan sistem akan kembali dimulai dari awal.
>
> Kondisi 13: Jika tombol “Berhenti” ditekan maka seluruh sistem akan mati.

#### 摘录 C

- 出处：第 5 页，Gambar 6
> Kondisi 5 Valve 1 OFF Pemanas 1 ON Pengaduk 1 ON ... T7 = TIM1
>
> Kondisi 9 Valve 2 OFF Valve 3 OFF Pemanas 2 ON Pengaduk 2 ON ... T11 = TIM2
>
> Kondisi 11 Valve 7 OFF Valve 4 OFF Pemanas 3 ON Pengaduk 3 ON
>
> Kondisi 12 Valve 8 ON Pemanas 3 OFF Pengaduk 3 OFF TIM3

#### 摘录 D

- 出处：第 6 页，Persamaan transisi dan persamaan keadaan
> T0 = Sistem ON
> T1 = Mulai . Kondisi 1
> T4 = SA1 . SB1 . Kondisi 2
> T7 = TIM1 . Kondisi 5
> T11 = TIM2 . Kondisi 9
> T13 = TIM3 . Kondisi 11
> ...
> Kondisi 9 = (Kondisi 9 + T8 + T9). T11̅ . T23̅
> Kondisi 10 = (Kondisi 10 + T11). T12̅ . T25̅
> Kondisi 11 = (Kondisi 11 + T10 + T12). T23̅ . T13̅
> Kondisi 12 = (Kondisi 12 + T13). T14̅ . T15̅ . T27̅ . T16̅
> Kondisi 13 = (Kondisi 13 + T17 + T18 + ... + T27). T28̅ . T29̅ . T30̅

### 2. 基于原文整理后的自然语言描述

The biodiesel controller is a batch-sequence EFSM that begins when `Sistem ON` and `Mulai` activate the process and then runs multiple tanks, valves, heaters, and mixers in parallel branches before converging to final discharge. In the early stage, `Kondisi 2-4` open `Valve 1-3` to fill the three measuring tanks, and when the paired upper/lower sensors `SA1/SB1`, `SA2/SB2`, and `SA3/SB3` confirm liquid presence, the controller switches to `Kondisi 5-7` to stop those inlet valves and start heating or transfer actions. The first branch heats and stirs tank 1 under `TIM1`, while the second and third branches route liquids through `Valve 5` and `Valve 6` into mixing tank 4; once tank 4 is confirmed full, `Kondisi 9` applies heating and stirring under `TIM2`, then `Kondisi 10` pushes the batch toward mixing tank 5 through `Valve 7`. After `SA5` and `SB5` confirm liquid in tank 5, `Kondisi 11` heats and stirs under `TIM3`, and `Kondisi 12` opens `Valve 8` to send the finished biodiesel to final storage before the system returns to the initial cycle. The paper also enumerates explicit transition equations `T0-T30` and state equations `Kondisi 1-13`, including stop-triggered exits from every active condition, so the controller is a richly specified timed sequential-process sample rather than a vague PLC flowchart.

### 3. 逐句溯源

1. 句子 1：The biodiesel controller is a batch-sequence EFSM that begins when `Sistem ON` and `Mulai` activate the process and then runs multiple tanks, valves, heaters, and mixers in parallel branches before converging to final discharge.
   对应摘录：A, B, D
2. 句子 2：In the early stage, `Kondisi 2-4` open `Valve 1-3` to fill the three measuring tanks, and when the paired upper/lower sensors `SA1/SB1`, `SA2/SB2`, and `SA3/SB3` confirm liquid presence, the controller switches to `Kondisi 5-7` to stop those inlet valves and start heating or transfer actions.
   对应摘录：B, D
3. 句子 3：The first branch heats and stirs tank 1 under `TIM1`, while the second and third branches route liquids through `Valve 5` and `Valve 6` into mixing tank 4; once tank 4 is confirmed full, `Kondisi 9` applies heating and stirring under `TIM2`, then `Kondisi 10` pushes the batch toward mixing tank 5 through `Valve 7`.
   对应摘录：B, C, D
4. 句子 4：After `SA5` and `SB5` confirm liquid in tank 5, `Kondisi 11` heats and stirs under `TIM3`, and `Kondisi 12` opens `Valve 8` to send the finished biodiesel to final storage before the system returns to the initial cycle.
   对应摘录：B, C, D
5. 句子 5：The paper also enumerates explicit transition equations `T0-T30` and state equations `Kondisi 1-13`, including stop-triggered exits from every active condition, so the controller is a richly specified timed sequential-process sample rather than a vague PLC flowchart.
   对应摘录：A, D
