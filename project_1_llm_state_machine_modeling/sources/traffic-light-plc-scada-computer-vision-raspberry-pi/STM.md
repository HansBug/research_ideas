# Prototipe lampu lalu lintas menggunakan PLC dan SCADA berbasis computer vision dengan raspberry pi 4B - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `computer vision + Raspberry Pi + PLC + SCADA` 融成了一个可执行的两优先模式交通灯监督器，既给出了 `>3 kendaraan` 的阈值判断，又给出了 `10 -> 15 detik` 与 `10 -> 5 detik` 的时长重配置，是交通信号方向强度很高的双 A `EFSM + T1` 样本。

## 条目 1: Camera-Driven Priority-Mode Traffic Supervisor

- 控制对象：道路交通信号领域的视觉检测优先模式交通灯监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把 `SSD` 车辆计数、`Raspberry Pi 4B`、`PLC Omron` 和 `SCADA CX-Supervisor` 结合起来的交通灯控制器，会在两种优先模式之间切换并动态重配绿灯时长。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了优先模式、阈值条件、寄存器映射、具体计时变化和 SCADA 侧的应急/待机控制项。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`ABSTRAK / Introduction`，`paper_content.txt` 第 22-38 行、第 164-180 行
> dikembangkan sistem lampu lalu lintas cerdas berbasis Programmable Logic Controller (PLC) yang dikombinasikan dengan Raspberry Pi 4B ... pengaturan durasi lampu berdasarkan analisis data lalu lintas secara real-time.
>
> terdapat 2 kondisi, yaitu padat dan sepi. Padat merupakan kondisi dimana terdapat lebih dari 3 kendaraan di persimpangan dan sepi merupakan kondisi terdapat kurang dari 3 mobil di persimpangan.

#### 摘录 B

- 出处：第 7 页，`2.6 Prinsip Kerja Sistem Traffic Light`，`paper_content.txt` 第 347-368 行
> dua kamera dipasang pada jalur-jalur prioritas, yaitu jalur Timur-Selatan dan Selatan-Barat. Fungsi dari kamera ini adalah mendeteksi kepadatan lalu lintas di setiap jalur dan mengirimkan data jumlah kendaraan ke PLC melalui komunikasi serial RS232.
>
> Sistem Smart Traffic Light ini menerapkan dua mode prioritas, yaitu: a. Prioritas 1: Jalur Timur-Selatan b. Prioritas 2: Jalur Selatan-Barat.
>
> jalur Timur akan mendapatkan lampu hijau lebih lama ketika terdeteksi jumlah kendaraan melebihi 3 unit (padat) ... jika jalur Selatan terdeteksi padat (lebih dari 3 kendaraan), durasi lampu hijau dipercepat.

#### 摘录 C

- 出处：第 8-9 页，`PLC menerima data / komunikasi Raspberry Pi ke PLC`，`paper_content.txt` 第 436-442 行、第 463-469 行、第 476-508 行
> Data jumlah kendaraan pada tiap simpang tersebut kemudian dikirim ke PLC Omron CP1-E N40 melalui komunikasi serial RS232. Data jumlah kendaraan pada simpang selatan dikirim ke memori D42 dan pada simpang barat dikirim ke memori D43.
>
> D42 CHANNEL ... 0003 ... Selatan ; D43 CHANNEL ... 0004 ... Barat.
>
> Raspberry Pi-4B mengirimkan data jumlah kendaraan dalam bentuk command block ... menulis data di memori D0 / D1 / D42 / D43.

#### 摘录 D

- 出处：第 10-12 页，`Prioritas 1 / Prioritas 2 / CX-Supervisor`，`paper_content.txt` 第 548-552 行、第 580-584 行、第 595-599 行、第 615-618 行
> Dalam kondisi normal, lampu hijau menyala selama 10 detik. ... pada mode prioritas 1, durasi penyalaan lampu hijau ... diperpanjang sebesar 5 detik, sehingga total durasinya menjadi 15 detik.
>
> Dalam kondisi normal, lampu hijau menyala selama 10 detik, tetapi pada mode prioritas 2, durasinya berkurang 5 detik menjadi 5 detik.
>
> Pengujian ini mencakup pengujian berbagai fitur kontrol, seperti Emergency Lamp, Emergency Button, Push Button ON, dan lampu indikator operasi (ON/Standby Lamp).

### 2. 基于原文整理后的自然语言描述

The smart-traffic controller uses two camera streams and a Raspberry Pi to classify each monitored approach as dense or sparse, then writes the resulting vehicle counts into PLC memory through an `RS232 / Modbus` link. Because only two cameras are used, the controller alternates between two exclusive operating modes: `Priority 1` for the `East-South` pair and `Priority 2` for the `South-West` pair. In `Priority 1`, when the east approach exceeds the `>3 vehicles` threshold while the south approach stays sparse, the PLC extends the east green timer from `10 s` to `15 s`; in `Priority 2`, when the west approach is dense and the south approach is sparse, the current south green is shortened from `10 s` to `5 s` so the controller can hand over sooner to the congested west side. On top of the automatic priority logic, the SCADA layer keeps explicit supervisory controls for `Emergency Lamp`, `Emergency Button`, and `ON/Standby`, so the traffic sequence can still be monitored and overridden from the control interface.

### 3. 逐句溯源

1. 句子 1：The smart-traffic controller uses two camera streams and a Raspberry Pi to classify each monitored approach as dense or sparse, then writes the resulting vehicle counts into PLC memory through an `RS232 / Modbus` link.
   对应摘录：A, B, C
2. 句子 2：Because only two cameras are used, the controller alternates between two exclusive operating modes: `Priority 1` for the `East-South` pair and `Priority 2` for the `South-West` pair.
   对应摘录：B
3. 句子 3：In `Priority 1`, when the east approach exceeds the `>3 vehicles` threshold while the south approach stays sparse, the PLC extends the east green timer from `10 s` to `15 s`; in `Priority 2`, when the west approach is dense and the south approach is sparse, the current south green is shortened from `10 s` to `5 s` so the controller can hand over sooner to the congested west side.
   对应摘录：A, B, D
4. 句子 4：On top of the automatic priority logic, the SCADA layer keeps explicit supervisory controls for `Emergency Lamp`, `Emergency Button`, and `ON/Standby`, so the traffic sequence can still be monitored and overridden from the control interface.
   对应摘录：D
