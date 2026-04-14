# SISTEM KERJA PENGENDALI OTOMATIS LAMPU TRAFFIC LIGHT PADA PERSIMPANGAN 4 (EMPAT) JALAN RAYA MENGGUNAKAN PROGRAMMABLE LOGIC CONTROLLER (PLC) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：FSM（普通离散状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口东西向/南北向交替放行、`05:00 s` 黄灯延时和 `07:00 s` 红灯保持链写得足够清楚，但与库内常规定时 PLC 交通灯簇存在较强同构。

## 条目 1: West-East / North-South Alternating Signal Cycle

- 控制对象：道路交通信号控制领域的四路口定时轮换交通灯控制器
- 状态机类型：FSM（普通离散状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（PLC 四路口定时轮换簇）

### 0. 条目识别与判定

- 一句话说明：这是一个四路口交通灯 PLC 控制器，用固定的启停触发和延时链条在东西向绿灯、黄灯过渡、南北向绿灯之间周期轮换。
- 判断：算。对象是实际交通灯控制系统，原文明确给出开机后的初始放行方向、`05:00 s` 与 `07:00 s` 两段延时，以及后续循环重复关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-25 行
> Pengaturan Traffic Light menggunakan PLC yang dilengkapi sistem bahasa Logic, Digital, Timmer, Delay, dan Relay ...
>
> Teknologi pengendali PLC bisa mengatur semua jalur Traffic Light sesuai dengan kebutuhan, sehingga kemacetan tidak terjadi pada jalur utama.

#### 摘录 B

- 出处：第 6 页，`Hasil`，`paper_content.txt` 第 436-460 行
> Apabila I1, ditekan pada posisi ON maka hijau barat (H-B) dan hijau timur (H-T) akan menyala, sementara merah utara (M-U) dan merah selatan (M-S) dalam kondisi menyala juga.
>
> Disaat hijau barat (H-B) dan hijau timur (H-T) menyalah, maka waktu On Delay yang telah diberi waktu yaitu 05:00 s ... maka lampu kuning barat (K-B) dan lampu kuning timur (K-T) menyala.
>
> Saat merah utara (M-U) dan merah selatan (M-S) menyala waktu On Delay selama 07:00s menghitung, sampai akhirnya lampu hijau utara (H-U) dan hijau selatan (H-S) menyalah ... kejadian ini terus berlangsung secara teratur dan berlanjut.

### 2. 基于原文整理后的自然语言描述

The PLC intersection controller starts from a fixed initial phase in which the west-east direction receives green while the north-south direction remains red. Once that west-east green phase becomes active, the controller launches an `On Delay` timer of `05:00 s`; after the timer expires, west-east green is replaced by west-east yellow while the opposite red phase is kept active. The controller then maintains the north-south red branch for `07:00 s` before switching to the opposite service phase, where north-south green turns on together with west-east red. This sequence repeats continuously until the operator stops the system, so the controller forms a simple cyclic FSM with explicit timed transition guards between the two directional phases.

### 3. 逐句溯源

1. 句子 1：The PLC intersection controller starts from a fixed initial phase in which the west-east direction receives green while the north-south direction remains red.
   对应摘录：B
2. 句子 2：Once that west-east green phase becomes active, the controller launches an `On Delay` timer of `05:00 s`; after the timer expires, west-east green is replaced by west-east yellow while the opposite red phase is kept active.
   对应摘录：B
3. 句子 3：The controller then maintains the north-south red branch for `07:00 s` before switching to the opposite service phase, where north-south green turns on together with west-east red.
   对应摘录：B
4. 句子 4：This sequence repeats continuously until the operator stops the system, so the controller forms a simple cyclic FSM with explicit timed transition guards between the two directional phases.
   对应摘录：A, B
