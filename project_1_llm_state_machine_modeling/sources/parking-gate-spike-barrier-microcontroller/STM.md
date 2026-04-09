# Implementasi Sistem Kontrol pada Gerbang Parkir dan Spike Barrier Menggunakan Mikrokontroler - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车闸门的前后传感放行链和强闯时的 `spike barrier` 安全分支写在同一套控制逻辑里，主流程和异常流程都足够具体。

## 条目 1: Front-Rear Sensor Gate and Forced-Breakthrough Spike-Barrier Controller

- 控制对象：智慧停车领域的停车闸门与强闯防逃逸 `spike barrier` 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向停车出口的闸门控制器，用前后超声波传感器组织开门与关门流程，并在车辆强闯时自动升起 `spike barrier`。
- 判断：算。对象是真实停车门控系统，原文明确写出了传感器触发、闸门保持开启、车辆通过后关门、非法冲闸触发尖刺障碍以及手动复位流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`3.1. Alur Kerja Sistem`，`paper_content.txt` 第 172-178 行
> Alur dari penerapan gerbang dan spike barrier dimulai dari kendaraan yang akan memasuki tempat parkir. Sensor yang terpasang sebelum gerbang mendeteksi kendaraan yang melintas dan menginformasikan kepada mikrokontroler (Arduino Uno) bahwa kendaraan tersebut terbaca. Gerbang terbuka ketika menerima instruksi dari mikrokontroler. Sensor akan terus memberitahu mikrokontroler untuk tidak menutup gerbang sampai sensor yang berada dibelakang gerbang parkir tidak terbaca. Selanjutnya gerbang akan tertutup setelah melewati sensor belakang.

#### 摘录 B

- 出处：第 4 页，`Gambar 2. Flowchart Gerbang dan Spike Barrier`，`paper_content.txt` 第 185-213 行
> Start
>
> Buka gerbang
>
> Kendaraan telah melewati sensor belakang ? ya
>
> Tutup gerbang
>
> Kendaraan menabrak gerbang ? tidak
>
> Barrier aktif ya
>
> Untuk alur dari spike barrier dijelaskan bahwa saat gerbang pada posisi tertutup atau normal, apabila mobil memaksa menerobos gerbang parkir, tanpa melewati proses deteksi, maka spike barrier akan bertindak secara otomatis dengan cara arduino memberikan perintah untuk mengaktifkan relay sehingga motor DC bergerak, sekaligus mengaktifkan limit switch yang sudah terpasang pada spike barrier. Spike barrier kembali ke posisi semula melalui proses manual yaitu dengan berupa push button.

#### 摘录 C

- 出处：第 5 页，`Gambar 4. Rangkaian Limit Switch`，`paper_content.txt` 第 238-246 行
> Untuk proses keluar, saat arduino sudah memberikan perintah untuk membuka gerbang parkir secara otomatis, pintu gerbang dengan kondisi awal pada sisi tengah yaitu A2 dan B2 limit switch, akan berpindah posisi ke A1 dan B1. Pintu akan kembali ke posisi A2 dan B2 setelah terjadinya pengecekan oleh sensor ultrasonik. Sebaliknya, saat proses keluar, dengan kondisi awal A2 dan B2, gerbang akan berpindah posisi ke A3 dan B3.

### 2. 基于原文整理后的自然语言描述

The controller uses a front sensor to detect an approaching car and then commands the parking gate to open through the microcontroller and motor driver. Once the nominal entry or exit branch starts, the controller keeps the gate open until the rear sensor confirms that the vehicle has completely passed the barrier area, after which the gate is closed again. The limit-switch states `A1/A2/A3` and `B1/B2/B3` provide the position semantics for the moving gate, so the system can distinguish the middle, opened, and opposite travel positions during the open-close cycle. In parallel with that nominal path, the same controller monitors an abnormal branch: if a vehicle forces its way through a gate that is still in the closed or normal position, the Arduino energizes the relay, raises the spike barrier with a dedicated DC motor, and leaves recovery to a manual push-button reset. This makes the sample valuable because it combines a standard sensor-driven barrier controller with an explicit security and forced-breakthrough recovery branch.

### 3. 逐句溯源

1. 句子 1：The controller uses a front sensor to detect an approaching car and then commands the parking gate to open through the microcontroller and motor driver.
   对应摘录：A
2. 句子 2：Once the nominal entry or exit branch starts, the controller keeps the gate open until the rear sensor confirms that the vehicle has completely passed the barrier area, after which the gate is closed again.
   对应摘录：A, B
3. 句子 3：The limit-switch states `A1/A2/A3` and `B1/B2/B3` provide the position semantics for the moving gate, so the system can distinguish the middle, opened, and opposite travel positions during the open-close cycle.
   对应摘录：C
4. 句子 4：In parallel with that nominal path, the same controller monitors an abnormal branch: if a vehicle forces its way through a gate that is still in the closed or normal position, the Arduino energizes the relay, raises the spike barrier with a dedicated DC motor, and leaves recovery to a manual push-button reset.
   对应摘录：B
5. 句子 5：This makes the sample valuable because it combines a standard sensor-driven barrier controller with an explicit security and forced-breakthrough recovery branch.
   对应摘录：A, B, C
