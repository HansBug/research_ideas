# Prototipe Sistem Parkir Gantung Berputar Ke Atas berbasis Programmable Logic Control Dilengkapi Human Machine Interface - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把六车位旋转停车系统的 PIN 认证、空槽搜索、目标槽召回和满位计数联锁写得足够细，是停车方向可靠的双 A 样本。

## 条目 1: PIN-Gated Empty-Slot Search and Slot-Recall Parking Controller

- 控制对象：智慧停车与车位管理领域的旋转式多车位停车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个六车位悬挂旋转停车系统，用 HMI 上的 `PIN`、停车/取车命令、限位开关和红外检测来驱动 DC 电机寻找空槽或召回目标车位。
- 判断：算。对象是真实停车控制系统，原文明确写出了空槽判断逻辑 `1:0 / 1:1`、停车与取车梯形图地址、计数比较器以及满位/空位指示的输出行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`Blok diagram prototipe`，`paper_content.txt` 第 133-149 行
> Prototipe tersebut menggunakan PLC, HMI, catu daya 220 VAC dan 12-24 VDC, sensor infrared, motor DC, dan limit switch. Pada saat akan parkir, PLC akan menerima perintah dari HMI untuk menggeser mobil yang telah diparkir kemudian menyiapkan slot tempat parkir selanjutnya yang masih kosong dengan bantuan limit switch ke 7 dan sensor infrared. Jika logika 1:0 artinya slot selanjutnya kosong, jika limit switch ke 7 dan sensor infrared dapat logika 1:1 artinya ada mobil di slot tersebut dan slot parkir akan terus bergeser hingga menemukan slot kosong atau berlogika 1:0. Limit switch ke 1, 2, 3, 4, 5, dan 6 ... akan berfungsi ketika mengeluarkan mobil ... tempat parkir akan terus bergeser hingga mobil di slot yang diinginkan siap untuk diambil.

#### 摘录 B

- 出处：第 3 页，`Hasil Desain HMI`，`paper_content.txt` 第 161-174 行
> Terdapat tiga alur kondisi desain yaitu alur desain saat mengaktifkan sistem parkir, alur desain saat mobil parkir dan alur desain saat mobil keluar. ... Saat menekan ikon petir akan diminta untuk memasukkan PIN kode keamanan sistem ... PIN tersebut hanya diketahui oleh petugas khusus yang ditugaskan untuk mengontrol sistem parkir. Ketika PIN sudah dimasukkan maka akan berganti ke layar keamanan sistem dimana ada ikon tombol power, konfigurasi tempat parkir, lampu indikator sistem dan tombol kembali ke layar utama.

#### 摘录 C

- 出处：第 4 页，`Program Sistem Parkir Gantung Berputar Ke Atas`，`paper_content.txt` 第 191-249 行
> Ladder diagram baris ke-0 ... mengaktifkan program ... internal relay PLC 20.00 ...
> Baris ke 1-13 adalah program untuk mengeluarkan mobil pada slot tertentu. Alamat W10.00 (Slot 1), W10.01 (Slot 2), W10.02 (Slot 3), W10.03 (Slot 4), W10.04 (Slot 5) dan W10.05 (Slot 6) ... diberi masukan data melalui HMI. Alamat input 0.00 (L.S 1) ... 0.05 (L.S 6) ... berfungsi untuk memutus arus motor DC berdasarkan slot yang dipanggil. ... internal relay 20.13 (motor keluar) ... output 100.00 ... motor DC akan berhenti jika sudah mengenai limit switch slot 1 ... telah diberi sistem interlocking supaya masing-masing limit switch tidak bisa aktif secara bersamaan.
>
> Alamat W10.06 (parkir) ... mengaktifkan alamat internal relay 30.00 (motor parkir) ... untuk memarkirkan mobil dan menyiapkan slot selanjutnya yang masih kosong. Alamat 0.06 (L.S slot kosong) dan 0.07 (Sensor INF) ... jika terdapat masukan 1:1 artinya terdapat mobil di slot berikutnya maka motor DC akan tetap berputar ... sampai mendapat masukan 1:0 yang artinya sensor infrared tidak mendeteksi mobil dan limit switch akan memutus arus motor DC ...
>
> Instruksi CMP 207 telah disetel untuk memberi batasan jumlah tidak lebih dari 6 dan tidak kurang dari 0, jika jumlah penambahan sudah mencapai 6 maka lampu indikator akan menyala merah dan jika kurang dari 6 maka lampu indikator akan menyala hijau.

#### 摘录 D

- 出处：第 5-6 页，`Hasil Pengujian Sistem Parkir Gantung Berputar Ke Atas`，`paper_content.txt` 第 283-301 行、第 316-343 行、第 357-373 行
> Ketika pemilik mobil pertama M1 telah memasukkan kode keamanan (PIN) dan menekan tombol parkir maka sistem parkir akan berputar dan berhenti ketika slot nomer 1 telah berada di depan pintu parkir. ... Proses ini akan diulangi lagi sampai semua tempat parkir telah terisi. ... Warna hijau menunjukkan tempat parkir masih tersedia sedangkan warna merah menunjukkan tempat parkir telah terisi penuh.
>
> Ketika pemilik mobil telah menekan tombol keluar, memasukkan PIN dan memilih nomer tempat parkir mobilnya maka sistem parkir akan berputar secara otomatis dan berhenti ketika mobil M3 telah berada di depan pintu parkir. ... Setelah itu mobil ketujuh M7 hendak masuk ke tempat parkir. Sistem parkir akan berputar dan mencari slot parkir yang kosong dan ternyata berhenti ketika slot nomer 5 yang kosong tepat berada di depan pintu parkir.
>
> Pada pengujian ini, kelima mobil tersebut akan keluar dari tempat parkir. ... sistem parkir akan berputar dan berhenti ketika slot parkir nomer 2 tepat berada di depan pintu parkir ... prototipe sistem parkir bekerja dengan baik ketika mobil yang tersisa hendak keluar dari tempat parkir yaitu mobil M8, M7, dan M10.

### 2. 基于原文整理后的自然语言描述

The hanging rotary parking controller manages a six-slot parking carousel through a PLC, an HMI security interface, one DC motor, six slot-specific limit switches, and a seventh empty-slot detector combined with an infrared sensor. Before any supervisory operation is enabled, the operator must enter the system `PIN` on the HMI and then choose parking, retrieval, or configuration functions from the security screen. For retrieval, HMI addresses `W10.00-W10.05` select the requested slot, the `motor keluar` chain drives output `100.00`, and the corresponding slot limit switch `0.00-0.05` stops the motor when the requested car arrives at the doorway, with interlocking preventing simultaneous slot-stop signals. For parking, address `W10.06` activates the `motor parkir` chain and the controller keeps rotating while the empty-slot detector `0.06` and infrared sensor `0.07` read `1:1`, then stops only when the next position changes to `1:0`, meaning the candidate slot is empty. The same PLC also maintains the occupancy count through `CMP 207`, caps the count between `0` and `6`, and turns the indicator red at full capacity and green otherwise; the test tables confirm that the system correctly handles sequential fill, mixed entry/exit, and complete emptying scenarios.

### 3. 逐句溯源

1. 句子 1：The hanging rotary parking controller manages a six-slot parking carousel through a PLC, an HMI security interface, one DC motor, six slot-specific limit switches, and a seventh empty-slot detector combined with an infrared sensor.
   对应摘录：A, B
2. 句子 2：Before any supervisory operation is enabled, the operator must enter the system `PIN` on the HMI and then choose parking, retrieval, or configuration functions from the security screen.
   对应摘录：B
3. 句子 3：For retrieval, HMI addresses `W10.00-W10.05` select the requested slot, the `motor keluar` chain drives output `100.00`, and the corresponding slot limit switch `0.00-0.05` stops the motor when the requested car arrives at the doorway, with interlocking preventing simultaneous slot-stop signals.
   对应摘录：A, C
4. 句子 4：For parking, address `W10.06` activates the `motor parkir` chain and the controller keeps rotating while the empty-slot detector `0.06` and infrared sensor `0.07` read `1:1`, then stops only when the next position changes to `1:0`, meaning the candidate slot is empty.
   对应摘录：A, C
5. 句子 5：The same PLC also maintains the occupancy count through `CMP 207`, caps the count between `0` and `6`, and turns the indicator red at full capacity and green otherwise; the test tables confirm that the system correctly handles sequential fill, mixed entry/exit, and complete emptying scenarios.
   对应摘录：C, D
