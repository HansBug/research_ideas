# Rancang Bangun Mesin Pengecat Dinding Otomatis Berbasis PLC CP1E-NA20DR-A - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文完整给出自动涂墙机的状态图、四个运动状态、三个限位/停止条件以及编码器脉冲阈值 `D100=1380 ppr`、`D200=5520 ppr`，是典型的工业顺序控制样本。

## 条目 1: Wall-painting machine lift-traverse sequence controller

- 控制对象：工业自动化与离散制造领域的自动墙面喷涂机升降横移顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `Omron CP1E-NA20DR-A` PLC 驱动的二维墙面喷涂设备，使用垂直与水平两个电机、限位开关和编码器脉冲计数完成往复喷涂。
- 判断：算。原文不仅明确说明设备对象和输入输出，还给出了 `Keadaan 1-4 + Stop` 的状态图、状态切换条件和脉冲阈值，足以直接整理成工业顺序 EFSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The components used in this study are the PG28 DC motor, encoder sensor, limit switch sensor and PLC Omron CP1E-NA20DR-A. This tool moves based on the x and y axis that is moving up-down and right-left, then for painting using a paint roll. Every movement of tools in the program is using ladder diagram in the CX-Programmer software. In making ladder diagram programs researchers use the state diagram method because this method can arrange ladder programs well.

#### 摘录 B

- 出处：第 5-6 页，Desain Algoritma Program
> Kondisi-kondisi tersebut adalah sebagai berikut.
> 1. Sistem menyala,
> 2. Keadaan 1 motor vertikal berputar searah jarum jam atau pengecat bergerak ke atas,
> 3. Keadaan 2 motor vertikal berputar berlawanan arah jarum jam atau pengecat bergerak ke bawah,
> 4. Keadaan 3 motor horizontal berputar searah jarum jam atau pengecat bergerak ke kiri,
> 5. Keadaan 4 motor horizontal berputar berlawanan jarum jam atau pengecat bergerak ke kanan,
> 6. Stop.

#### 摘录 C

- 出处：第 6 页，Gambar 7 menjelaskan cara kerja dari mesin pengecat
> Gambar 7 menjelaskan cara kerja dari mesin pengecat yang bermula ketika push button start ditekan maka akan mengaktifkan sistem pada PLC dengan mengaktifkan Keadaan 1, ketika Keadaan 1 bergerak ke atas dan ketika rangka verikal mengenai limit switch 1 maka akan mengaktifkan limit switch 1 dan Keadaan 2 akan aktif bergerak ke bawah kemudian mengaktifkan limit switch vertikal 2. Sistem akan berulang dari Keadaan 1 dan Keadaan 2 on hingga counter dari limit switch 2 telah aktif sebanyak 2 kali. Setelah itu counter akan mengaktifkan Keadaan 3 hingga D100 bernilai 1380 ppr on setelah itu maka Keadaan 3 akan off dan sistem kembali ke Keadaan 1 on. Sistem terus berulang hingga D100 aktif sebanyak 4 kali dalam counter. Kemudian counter mengaktifkan Keadaan 4 sampai D200 mencapai nilai 5520 ppr maka mesin off. Jika Keadaan 4 mengenai limit switch 3 atau PB stop ditekan maka seluruh sistem akan off.

#### 摘录 D

- 出处：第 1 页 / 第 11 页，Abstract / Pengujian
> reads 1380 pulses per 10 cm by the encoder sensor. A distance of 10 cm refers to the width of the paint roll used.
>
> Didapat jarak 10 cm dengan nilai pulsa sebesar 1380 ppr.

### 2. 基于原文整理后的自然语言描述

The wall-painting machine is controlled by a PLC EFSM that starts from an idle origin, then alternates vertical up and down strokes before shifting horizontally and eventually returning to the start point. Pressing `start` activates `Keadaan 1`, which drives the vertical motor upward until `limit switch 1` fires, after which `Keadaan 2` drives the same axis downward until `limit switch 2` is reached. This up-down loop repeats until the `limit switch 2` counter has been hit twice, then `Keadaan 3` moves the horizontal axis left until register `D100` reaches `1380 ppr`, equivalent to a `10 cm` painting width. The machine then re-enters the vertical painting pass and keeps iterating until the horizontal counter has been accumulated four times; after that `Keadaan 4` drives the axis right until `D200` reaches `5520 ppr`, where the machine stops. A stop pushbutton or `limit switch 3` can shut the whole system down early, so the controller is not just a fixed path generator but a sensor- and counter-gated painting sequencer.

### 3. 逐句溯源

1. 句子 1：The wall-painting machine is controlled by a PLC EFSM that starts from an idle origin, then alternates vertical up and down strokes before shifting horizontally and eventually returning to the start point.
   对应摘录：A, B, C
2. 句子 2：Pressing `start` activates `Keadaan 1`, which drives the vertical motor upward until `limit switch 1` fires, after which `Keadaan 2` drives the same axis downward until `limit switch 2` is reached.
   对应摘录：B, C
3. 句子 3：This up-down loop repeats until the `limit switch 2` counter has been hit twice, then `Keadaan 3` moves the horizontal axis left until register `D100` reaches `1380 ppr`, equivalent to a `10 cm` painting width.
   对应摘录：C, D
4. 句子 4：The machine then re-enters the vertical painting pass and keeps iterating until the horizontal counter has been accumulated four times; after that `Keadaan 4` drives the axis right until `D200` reaches `5520 ppr`, where the machine stops.
   对应摘录：C
5. 句子 5：A stop pushbutton or `limit switch 3` can shut the whole system down early, so the controller is not just a fixed path generator but a sensor- and counter-gated painting sequencer.
   对应摘录：C
