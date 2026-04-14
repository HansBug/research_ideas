# Pengendalian Sistem Parkir Mobil Putar Vertikal Otomatis Menggunakan PLC Outseal dan HMI Android - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把立体旋转车库的进车检测、车位选择、CW/CCW 旋转、取车校验、出车放行和应急界面写成完整的 PLC Outseal + Android HMI 控制链，原文和描述都能稳定达到双 A。

## 条目 1: Slot-Selected Rotary Parking and Retrieval Controller

- 控制对象：立体旋转式停车库的车位选择、旋转取放与出车放行 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是智慧停车场景里的旋转车位控制器，用 PLC Outseal、Android HMI、进出口栏杆、车位红外/接近传感器和 CW/CCW 旋转电机把进车、选位、停车、取车和应急操作组织成离散流程。
- 判断：算。对象是实际停车设备控制器，原文直接给出进车传感、车位对准、HMI 选位、取车校验、车位计数和应急手动旋转/开闸等系统级逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`Abstract / Metodologi Penelitian`，`paper_content.txt` 第 19-30、81-88、103-109 行
> In this study, a prototype of a vertical rotating parking system with 8 parking spaces was made and controlled using PLC outseal and HMI Android.
>
> The rotating parking lot uses a DC Motor that will rotate the vehicle parking lot to enter or exit. Car models that will enter and exit the parking lot are detected using proximity sensors and IR sensors.
>
> PLC Outseal Mega V.1 sebagai kontroler utama untuk mengolah perintah yang diberikan oleh pengguna melalui HMI Android, sensor proximity, sensor infrared dan push button sebagai masukan, lampu led dan motor DC sebagai keluaran.

#### 摘录 B

- 出处：第 3-4 页，`Hasil implementasi`，`paper_content.txt` 第 134-172 行
> Untuk menjalankan sistem harus menekan tombol ON (Start) ... Sensor proximity digunakan untuk mendeteksi kendaraan masuk dan sensor infrared mendeteksi kendaraan siap parkir dan mendeteksi perpindahan ruang parkir.
>
> Ketika adanya kendaraan masuk maka sensor proximity akan ON dan motor DC menggerakan palang pintu untuk terbuka ... Ketika ruang parkir sudah penuh maka motor DC penggerak palang tetap tertutup kondisi led merah ON.
>
> operator menekan “Parkir Mobil” kemudian menekan “Nomor” ruang parkir mobilnya ditempatkan dan menekan “OK”. Setelah itu motor DC penggerak rotary parkir ON ...
>
> operator menekan “Ambil Mobil” kemudian menekan “Nomor” ruang parkir mobil ditempatkan dan menekan “OK”. ... ketika ruang parkir yang ditekan pada HMI Android sudah berada dibawah maka led kuning ON dan motor DC penggerak rotary parkir OFF. ... jika sudah benar maka tombol “BENAR” ditekan maka palang pintu akan terbuka.

#### 摘录 C

- 出处：第 5-8 页，`Tampilan HMI Android / Data Pengujian`，`paper_content.txt` 第 202-210、224-294、327-425 行
> Ketika mobil keluar dari ruang parkir dan melewati sensor proximity, maka sensor proximity ON kemudian palang pintu tertutup kembali dan kondisi led kuning OFF menandakan proses selesai.
>
> Tombol untuk melakukan Parkir Mobil ... tombol nomor ruang parkir 1 sampai ruang parkir 8 untuk parkir mobil ... tombol nomor ruang parkir 1 sampai ruang parkir 8 untuk ambil mobil ... tombol untuk validasi pengambilan mobil ... tombol “DARURAT ON” ... tombol dan indikator untuk menurunkan ruang parkir CW/CCW ... tombol Reset Jumlah ... Reset Counter.
>
> Tabel 3. Data Mobil Parkir ... Perintah Parkir Aktif ... Jumlah Mobil di Area Parkir ... Nomor Ruang Parkir.

### 2. 基于原文整理后的自然语言描述

The vertical rotary parking system is controlled as a PLC Outseal workflow that combines entry detection, slot assignment, rotary motion, retrieval validation, and emergency override instead of only opening a gate. After the Start button is pressed, the controller uses the proximity sensor to detect a car at the barrier and opens the entry gate only while free slots remain; when the lot is full, the red indicator stays on and the barrier remains closed. Once the car reaches the staging position, infrared sensor `1` checks whether the vehicle is correctly aligned for parking, and the operator then uses the Android HMI to choose `Parkir Mobil`, select a slot number, and confirm with `OK`, after which the rotary motor moves until infrared sensor `2` detects the requested parking cabin. For retrieval, the operator chooses `Ambil Mobil` and a slot number, the motor rotates `CW/CCW` until the selected cabin reaches the bottom, and a validation screen requires the operator to confirm `BENAR` before the exit barrier opens. The same HMI also exposes emergency rotary, barrier, count-reset, and counter-reset functions, so the paper preserves the normal parking path, the retrieval-confirmation branch, and the manual recovery path as one detailed parking-control EFSM.

### 3. 逐句溯源

1. 句子 1：The vertical rotary parking system is controlled as a PLC Outseal workflow that combines entry detection, slot assignment, rotary motion, retrieval validation, and emergency override instead of only opening a gate.
   对应摘录：A, C
2. 句子 2：After the Start button is pressed, the controller uses the proximity sensor to detect a car at the barrier and opens the entry gate only while free slots remain; when the lot is full, the red indicator stays on and the barrier remains closed.
   对应摘录：B
3. 句子 3：Once the car reaches the staging position, infrared sensor `1` checks whether the vehicle is correctly aligned for parking, and the operator then uses the Android HMI to choose `Parkir Mobil`, select a slot number, and confirm with `OK`, after which the rotary motor moves until infrared sensor `2` detects the requested parking cabin.
   对应摘录：A, B
4. 句子 4：For retrieval, the operator chooses `Ambil Mobil` and a slot number, the motor rotates `CW/CCW` until the selected cabin reaches the bottom, and a validation screen requires the operator to confirm `BENAR` before the exit barrier opens.
   对应摘录：B, C
5. 句子 5：The same HMI also exposes emergency rotary, barrier, count-reset, and counter-reset functions, so the paper preserves the normal parking path, the retrieval-confirmation branch, and the manual recovery path as one detailed parking-control EFSM.
   对应摘录：C
