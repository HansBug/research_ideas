# PENGEMBANGAN SISTEM TRAFFIC LIGHTS BERDASARKAN KEPADATAN KENDARAAN MENGGUNAKAN PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把车流密度感知、绿灯时长映射、黄灯前后双阶段和四路口顺序轮转写得很完整，是交通灯方向稳健的双 A `EFSM + T1` 样本。

## 条目 1: Three-Sensor Density-to-Green-Duration Traffic-Light Supervisor

- 控制对象：道路交通信号控制领域的基于车流密度的 PLC 路口交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个四路口交通灯控制器，用每条车道上的三个传感器判断密度等级，并据此决定绿灯持续时间与整条路口轮转顺序。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了传感器到密度状态的映射、`5/10/20/40` 秒绿灯时长、黄灯前后两段切换以及四条车道的串行服务约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，`3.2 Blok Diagram Dan Flow Chart`，`paper_content.txt` 第 176-185 行、第 202-207 行
> Gambar berikut adalah blok diagram secara umum rancangan sistem traffic light berdasarkan kepadatan kendaraan berbasis PLC pada satu jalur.
> Dalam menentukan kondisi kepadatan kendaraan, perancangan alat ini menggunakan tiga buah sensor untuk mewakili empat kondisi kepadatan pada masing-masing jalur. Satu sensor aktif menandakan kondisi sepi, dua sensor aktif menandakan kondisi normal, tiga sensor aktif untuk menandakan kondisi padat dan jika ketiga sensor tidak aktif menandakan kondisi tidak ada kendaraan (kosong) pada jalur tersebut. Kondisi ketiga sensor tersebut yang akan menentukan durasi waktu nyala lampu hijau.
> Pengaturan durasi waktu nyala masing-masing kondisi memanfaatkan internal timer yang ada pada PLC.

#### 摘录 B

- 出处：第 8 页，`Flowchart satu jalur perancangan traffic light`，`paper_content.txt` 第 217-223 行
> Pada flowchart terlihat lampu kuning akan menyala dua kali, sebelum dan sesudah lampu hijau menyala. Namun terdapat perbedaan nyala lampu kuning pada dua kondisi tersebut. Sebelum lampu hijau menyala, lampu kuning menyala bersama lampu merah. Sedangkan setelah lampu hijau, lampu kuning menyala duluan, kemudian disusul nyala lampu merah. Nyala lampu hijau tergantung kepada kondisi ketiga sensor yang menandakan kondisi kepadatan jalan.

#### 摘录 C

- 出处：第 10-11 页，`4.2 Data Durasi Lampu Hijau Menyala`，`paper_content.txt` 第 308-336 行
> Pada setiap jalur ditempatkan tiga buah sensor, kondisi setiap sensor mempengaruhi nyala lampu hijau pada jalur tersebut. Kondisi dari ketiga sensor tersebut yang akan menentukan kepadatan kendaraan.
>
> Tabel 2. Durasi nyala lampu hijau berdasarkan kondisi sensor
> Kosong off off off 5
> Sepi on off off 10
> Normal on on off 20
> Padat on on on 40
>
> Jika dilakukan pengujian pada keempat jalurnya, maka akan sangat berpengaruh kepada durasi nyala lampu merah pada setiap jalur. Karena ke empat jalur merupakan satu siklus yang saling berkaitan. Siklus nyala lampu jalur kedua akan mulai bekerja setelah siklus nyala lampu jalur pertama selesai. Kemudian siklus nyala lampu jalur ketiga juga akan mulai bekerja setelah siklus nyala lampu jalur kedua selesai, demikian seterusnya. Dengan kata lain, lampu jalur berikutnya tidak akan mulai bekerja, jika lampu jalur sebelumnya belum selesai.

#### 摘录 D

- 出处：第 11 页，`5.1 Kesimpulan`，`paper_content.txt` 第 342-352 行
> Sistem pengaturan lampu lalu lintas dapat dirancang lebih efektif dan bekerja berdasarkan kepadatan kendaraan ...
> Durasi nyala lampu lalu lintas dapat ditentukan dan disesuaikan dengan tingkat kepadatan kendaraan dengan cara, mengatur durasi nyala lampu lalu lintas berdasarkan timer menggunakan PLC Omron CPM1A. Kerja dari timer-timer yang terdapat pada PLC ini, ditentukan oleh kondisi sensor-sensor yang menjadi input dari PLC tersebut. Sehingga terdapat perbedaan pengaturan lampu lalu lintas berdasarkan keadaan sepi, normal ataupun padat kendaraan yang melintas pada suatu jalur persimpangan jalan raya.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller uses three sensors on each lane to encode four density conditions and then selects the green-light dwell time from that density state instead of using one fixed cycle for all traffic situations. The sensor patterns `off/off/off`, `on/off/off`, `on/on/off`, and `on/on/on` represent `Kosong`, `Sepi`, `Normal`, and `Padat`, and the PLC maps them to green durations of `5`, `10`, `20`, and `40` seconds through its internal timers. The single-lane flow chart inserts yellow twice in every cycle: before green it is combined with red as a preparatory warning, and after green it appears alone before the road turns red. Across the four-road junction, each lane is part of one serial cycle, so lane `n+1` cannot begin until lane `n` has fully completed its own red-yellow-green-yellow sequence and timer allocation.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller uses three sensors on each lane to encode four density conditions and then selects the green-light dwell time from that density state instead of using one fixed cycle for all traffic situations.
   对应摘录：A, C
2. 句子 2：The sensor patterns `off/off/off`, `on/off/off`, `on/on/off`, and `on/on/on` represent `Kosong`, `Sepi`, `Normal`, and `Padat`, and the PLC maps them to green durations of `5`, `10`, `20`, and `40` seconds through its internal timers.
   对应摘录：A, C, D
3. 句子 3：The single-lane flow chart inserts yellow twice in every cycle: before green it is combined with red as a preparatory warning, and after green it appears alone before the road turns red.
   对应摘录：B
4. 句子 4：Across the four-road junction, each lane is part of one serial cycle, so lane `n+1` cannot begin until lane `n` has fully completed its own red-yellow-green-yellow sequence and timer allocation.
   对应摘录：C
