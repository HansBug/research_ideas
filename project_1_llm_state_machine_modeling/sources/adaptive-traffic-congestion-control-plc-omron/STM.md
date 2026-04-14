# DESAIN SISTEM KONTROL PENANGGULANGAN KEMACETAN LALU LINTAS ADAPTIF BERBASIS PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了基于 `LDR + PLC Omron` 的四路口自适应相位链，并把 `5 detik / 3 detik / 10 detik` 的常规与拥堵分支明确写进了主程序和子程序说明里，是一条很稳定的双 A `EFSM + T1` 样本。

## 条目 1: LDR-Based Adaptive Four-Way Signal Cycle

- 控制对象：道路交通信号领域的 `LDR` 拥堵感知四向相位控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 `PLC Omron` 和每车道 `LDR` 传感器驱动的自适应交通灯控制器，会根据拥堵检测把绿灯时长从正常值扩展到拥堵值。
- 判断：算。对象是实际路口交通灯控制系统，原文明确给出了子程序、各车道相位关系、拥堵触发条件以及 `5 detik / 10 detik / 3 detik` 的工程时序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`ABSTRACT / ABSTRAK`，`paper_content.txt` 第 21-31 行、第 43-49 行
> an adaptive traffic light control system based on Programmable Logic Controller was built. ... the amber and green lights are set to about 3 and 5 seconds, respectively. During crowded situations, the duration of the green light is ... 10 seconds.
>
> durasi lampu kuning dan hijau diatur sekitar 3 detik dan 5 detik. Sedangkan pada saat kondisi padat, maka durasi lampu hijau diatur menjadi 10 detik.

#### 摘录 B

- 出处：第 2 页，`Diagram Alur Sistem`，`paper_content.txt` 第 137-166 行
> Gambar 3 adalah merupakan diagram alur sistem kontrol traffic light di dalam penelitian ini.
>
> S3 Padat? ... TL 1,2,6 Hijau 5 Detik ... TL 3,4,2 Hijau 10 Detik ... S2 Padat? ... TL 5,6,4 Hijau 10 Detik ... S1 Padat? ... TL 1,2,6 Hijau 10 Detik

#### 摘录 C

- 出处：第 4-5 页，`Pengujian sub rutin Jalur 1/2/3/4`，`paper_content.txt` 第 291-310 行、第 316-324 行、第 351-361 行
> TM1 menjadi aktif dan mulai menghitung selama 5 detik.
>
> TM3 juga akan aktif dan mulai menghitung selama 5 detik ... merupakan lama nyala LH3 dan LH2.
>
> TM5 aktif dan mulai menghitung selama 5 detik ... merupakan lama nyala lampu hijau pada jalur 3.
>
> TM6 aktif dan mulai menghitung selama 5 detik ... merupakan lama nyala lampu hijau pada jalur 4.

#### 摘录 D

- 出处：第 5-6 页，`Pengujian Sub rutin Sensor / Pengujian Lampu Traffic Light / Kesimpulan`，`paper_content.txt` 第 336-348 行、第 367-403 行、第 411-419 行
> ketika kontak NO S1 aktif ... TSPJ1 akan mulai menghitung selama 5 detik, kemudian dilanjutkan perhitungan oleh TM1 selama 5 detik. ... selama 10 detik. Waktu tersebut merupakan lama nyala lampu hijau saat terjadi kepadatan.
>
> Saat kondisi hijau ... lampu traffic 2, 3, 4 merah ... Saat kondisi merah ... lampu traffic 2, 3, 4 hijau.
>
> Ketika terjadi kemacetan, lampu hijau menyala sekitar 10 detik ... Sedangkan ketika normal, lampu hijau menyala sekitar 5 menit.

### 2. 基于原文整理后的自然语言描述

The PLC controller runs a four-way traffic sequence in which each active approach normally receives a `5 s` green phase and a `3 s` yellow phase while the conflicting approaches stay red. Its flowchart explicitly branches on congestion sensors `S1`, `S2`, and `S3`, so the machine can decide whether the next served approach keeps the normal duration or switches into a dense-traffic variant. In the dense branch, the corresponding `LDR` sensor triggers an extra timing segment and extends the green hold from the normal `5 s` to `10 s`, which the paper describes as a combined `5 s + 5 s` computation inside the sensor subroutine. The controller also specifies the per-lane mutual exclusion relation, meaning the green or yellow state of one traffic light is always paired with red on the other three approaches before the sequence moves to the next lane.

### 3. 逐句溯源

1. 句子 1：The PLC controller runs a four-way traffic sequence in which each active approach normally receives a `5 s` green phase and a `3 s` yellow phase while the conflicting approaches stay red.
   对应摘录：A, B, C, D
2. 句子 2：Its flowchart explicitly branches on congestion sensors `S1`, `S2`, and `S3`, so the machine can decide whether the next served approach keeps the normal duration or switches into a dense-traffic variant.
   对应摘录：B
3. 句子 3：In the dense branch, the corresponding `LDR` sensor triggers an extra timing segment and extends the green hold from the normal `5 s` to `10 s`, which the paper describes as a combined `5 s + 5 s` computation inside the sensor subroutine.
   对应摘录：A, D
4. 句子 4：The controller also specifies the per-lane mutual exclusion relation, meaning the green or yellow state of one traffic light is always paired with red on the other three approaches before the sequence moves to the next lane.
   对应摘录：B, D
