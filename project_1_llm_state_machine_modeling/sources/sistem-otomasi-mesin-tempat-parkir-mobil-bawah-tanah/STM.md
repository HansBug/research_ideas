# Sistem Otomasi Mesin Tempat Parkir Mobil Bawah Tanah dengan Menggunakan Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束 / 以事件推进为主）
- 结构标签概况：无额外结构标签
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把地下立体停车装置的三自由度机械链、PC/PLC 分层控制、槽位选择、层位与槽位传感、两阶段取放车流程以及手动应急控制写得很具体，足以形成停车基础设施方向的双 A `EFSM + T0` 条目。

## 条目 1: Underground Lift-Rotate-Push Parking Controller

- 控制对象：智慧停车与车位管理领域的地下立体停车升降-旋转-推送控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束 / 以事件推进为主）
- 结构标签：-
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 PC 发出取车/放车指令、由 OMRON PLC 执行升降、旋转和气缸推送动作的地下自动停车控制器。
- 判断：算。对象是实际停车装置控制系统，原文明确给出三自由度机械结构、按楼层与槽位定位的传感链、两阶段 PLC 程序、手动应急入口以及完整停车/取车执行序列。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`METODE PENELITIAN / Model Miniatur dan Mekanik Sistem`，`paper_content.txt` 第 85-94 行、第 116-124 行
> Model mesin tempat parkir otomatis di bawah tanah dirancang berbentuk lingkaran, terdiri atas 3 lantai atau tingkat dimana setiap tingkat dapat menampung 8 mobil. ... Mekanisme pembawa mobil berada ditengah lingkaran dan memiliki 3 derajat kebebasan, yaitu gerakan naik-turun untuk menuju ke lantai atau tingkat yang diinginkan, gerakan rotasi untuk menuju lokasi slot tempat parkir yang dituju dan gerakan maju-mundur untuk meletakkan atau mengambil mobil.
>
> Selain itu, untuk dapat menuju ke slot yang diinginkan, piringan lingkaran dilengkapi dengan mekanisme pemutar. Aktuator yang digunakan untuk memutar piringan (gerakan rotasi) adalah sebuah motor steper ... Setelah sampai pada slot yang dinginkan, gerakan maju-mundur untuk meletakkan atau mengambil mobil, dilakukan dengan menggunakan silinder penumatik.

#### 摘录 B

- 出处：第 4-6 页，`Perangkat Keras Sistem`，`paper_content.txt` 第 161-179 行、第 256-259 行
> Empat buah sensor limit switch digunakan untuk mendeteksi posisi piringan pengangkat mobil. Di setiap lantai atau tingkat terdapat sebuah limit switch dimana output dari limit switch ini memberikan informasi kepada PLC bahwa piringan lift sudah sampai di lantai atau tingkat yang bersangkutan. Sedangkan untuk mendeteksi posisi slot tempat parkir, digunakan sebuah sensor photoelectric.
>
> Motor AC yang digunakan sebagai aktuator untuk gerakan naik-turun, dikontrol oleh PLC dengan menggunakan sebuah relay. Demikian juga solenoid, valve untuk pneumatic, sistem pengereman, semuanya dikontrol oleh PLC melalui relay. ... Motor steper dikontrol oleh PLC melalui sebuah interface driver motor stepper.
>
> Pada sistem ini, juga disediakan tombol manual untuk dapat menggerakkan mekanisme mesin tempat parkir otomatis dengan tujuan bila terjadi keadaan darurat, maka mesin masih dapat dikontrol secara manual.

#### 摘录 C

- 出处：第 6-7 页，`Perangkat Lunak Sistem / HASIL DAN PEMBAHASAN`，`paper_content.txt` 第 263-283 行、第 302-347 行
> Program pertama adalah program yang dibuat menggunakan bahasa pemrograman Microsoft Visual Basic 6.0. Program ini berjalan di PC dan berfungsi mengatur sistem database dari model parkir otomatis dan juga memberi perintah kepada PLC untuk mengambil atau meletakkan mobil pada slot tertentu. Program kedua adalah program PLC itu sendiri dimana program ini berfungsi mengontrol gerakan semua mekanik sesuai dengan perintah yang diberikan dari PC.
>
> Program yang dibuat untuk menggerakkan mekanik dibagi atas dua proses yaitu proses pengambilan pallet dan proses peletakan pallet. Baik dalam proses pengambilan mobil maupun peletakan mobil tetap harus melewati kedua proses tersebut.
>
> Frame 2 dan 3 menunjukkan piringan lift pembawa mobil mulai turun. Frame 4 menunjukkan piringan lift sudah sampai di lantai 1. Frame 5 dan 6 menunjukkan piringan lift pembawa mobil berputar menuju slot 2A. Frame 7 memperlihatkan silinder pneumatic bergerak maju untuk meletakkan mobil di slot 2A. ... Frame 10 sampai 14 memperlihatkan mekanik pembawa mobil kembali ke posisi semula.
>
> Waktu paling lama yang diperlukan untuk pengambilan atau peletakkan mobil dalam model sistem ini adalah 93 detik.

### 2. 基于原文整理后的自然语言描述

The controller manages a three-level underground parking mechanism whose carrier disk can move vertically, rotate to a requested slot, and translate forward or backward to place or pick up a car. A PC-side Visual Basic program maintains the slot database and issues place or retrieve commands for a selected slot, while an OMRON CPM1 ladder program executes the mechanical sequence on the PLC. The PLC uses per-floor limit switches to confirm the lift has reached the target level, a photoelectric sensor to confirm slot position, and relay-driven outputs for the reversible AC lift motor, the stepper-based rotation stage, the pneumatic cylinder, the solenoid valve, and the braking circuit. The motion logic is explicitly split into `proses pengambilan pallet` and `proses peletakan pallet`, and the illustrated `2A` scenario shows the disk descending, rotating to slot `2A`, pushing the car into the slot, retracting the cylinder, and returning the carrier to its home configuration. A manual override path is provided for emergency operation, and the 24-slot timing table shows the full place and retrieve workflow remains deterministic across all floor-slot combinations.

### 3. 逐句溯源

1. 句子 1：The controller manages a three-level underground parking mechanism whose carrier disk can move vertically, rotate to a requested slot, and translate forward or backward to place or pick up a car.
   对应摘录：A
2. 句子 2：A PC-side Visual Basic program maintains the slot database and issues place or retrieve commands for a selected slot, while an OMRON CPM1 ladder program executes the mechanical sequence on the PLC.
   对应摘录：C
3. 句子 3：The PLC uses per-floor limit switches to confirm the lift has reached the target level, a photoelectric sensor to confirm slot position, and relay-driven outputs for the reversible AC lift motor, the stepper-based rotation stage, the pneumatic cylinder, the solenoid valve, and the braking circuit.
   对应摘录：B
4. 句子 4：The motion logic is explicitly split into `proses pengambilan pallet` and `proses peletakan pallet`, and the illustrated `2A` scenario shows the disk descending, rotating to slot `2A`, pushing the car into the slot, retracting the cylinder, and returning the carrier to its home configuration.
   对应摘录：C
5. 句子 5：A manual override path is provided for emergency operation, and the 24-slot timing table shows the full place and retrieve workflow remains deterministic across all floor-slot combinations.
   对应摘录：B, C
