# Simulator Berbasis PLC untuk Pengaturan Lalu-lintas Jalan Raya pada Perlintasan Jalur Kapal - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把船道桥体升降、路侧栏杆、红黄绿灯、光电/接近/限位传感器和 auto/manual 切换写成完整的 PLC 联动控制链，还保留了 `5` 秒、`9` 秒和升降时差 `26` 秒等工程定时事实。

## 条目 1: Bridge-Lift and Road-Traffic Ship-Crossing Controller

- 控制对象：船道桥体升降与道路交通放行联动的 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通与船只通航交叉口里的桥体升降控制器，用 PLC 协调 photo sensor、proximity sensor、limit switch、液压泵、伺服栏杆和交通灯，完成封路、抬桥、放船、落桥和恢复放行。
- 判断：算。对象是真实交通设施的控制原型，原文把 auto/manual 双模式、传感器输入、红黄绿灯切换、栏杆下放保护、桥体 up/down 限位和多船通行条件都写得可追溯。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract`，`paper_content.txt` 第 21-40、63-72 行
> A simulator based-on the Programmable Logic Controller (PLC) has been assembled. ... The assembly results are (i) construction of the miniature of bridge body, (ii) placement of a number of sensors, (iii) installation the pump for the hydraulic system, (iv) installation of latches assisted by servo motors, (v) installation of traffic control lights and indicators ...
>
> The programming result for the PLC system is in the form of syntax structure based-on ladder diagram assisted by GX Works-2 32-bit.
>
> The process of lifting the bridge body is longer than the time of dropping back with the time difference of 26 seconds.

#### 摘录 B

- 出处：第 2-3 页，`Pendahuluan / Metode Penelitian`，`paper_content.txt` 第 100-117、241-258 行
> waktu penutupan palang pintu dan pembukaan jembatan setelah kapal terbaca sensor ke-1 sekitar 9 detik; ... lampu hijau OFF setelah 1 detik dilanjutkan lampu kuning ON selama 4 detik, kemudian lampu kuning OFF dan lampu merah ON ...
>
> apabila kapal yang lewat hanya satu, maka sistem dapat dioperasikan secara otomatis, sedangkan apabila kapal yang lewat lebih dari satu, maka dioperasikan secara manual ...
>
> perakitan dilakukan ... melalui (i) konstruksi miniatur badan jembatan, (ii) pemilihan dan penempatan sensor-sensor, (iii) pemasangan pompa untuk sistem hidrolik, (iv) pemasangan palang pintu berbantuan motor servo, (v) pemasangan lampu pengatur lalu-lintas dan indikator ...

#### 摘录 C

- 出处：第 8 页，`Kinerja saat sinkronisasi / Pengamatan terhadap pembacaan sensor-sensor`，`paper_content.txt` 第 760-788、797-838 行
> Panel pengoperasian meliputi ... selector switch 2 posisi, untuk pemindahan mode manual atau auto ... Input dari panel pengoperasian dan input sensor diproses dalam program PLC untuk dihasilkan output pengontrolan yang sesuai dan tepat.
>
> Prototipe dioperasikan dalam dua mode, yaitu manual dan auto. Mode manual digunakan untuk kemudahan operator saat perawatan, pengecekan, dan penanganan saat terjadi error step. ... Saat sistem dalam mode auto, maka program untuk pengoperasian miniatur badan jembatan pada PLC teraktifkan untuk beroperasi.
>
> posisi selector switch sudah pada posisi auto, lampu hijau ON untuk palang pintu naik, ketika kapal terdeteksi pada photo sensor #1 ... maka lampu kuning kondisi ON selama 5 detik, lampu merah kondisi ON, palang pintu turun. Untuk kondisi dimana di bawah palang pintu masih terdapat objek atau kendaraan, maka proximity sensor baca objek dan palang pintu tidak turun. ... maka miniatur badan jembatan terangkat sampai batas maksimal dan limit switch "up" tertekan. Setelah kapal sudah terdeteksi oleh photo sensor #2, maka badan jembatan tertutup kembali sampai batas maksimal dan limit switch pilihan down ditekan, lampu kuning ON lima detik, lampu hijau ON.

### 2. 基于原文整理后的自然语言描述

The ship-crossing simulator is controlled as a PLC EFSM that couples road traffic signals, barrier-gate motion, hydraulic bridge lifting, and ship detection into one coordinated sequence. The controller operates in two modes: manual mode is reserved for maintenance and error handling, while auto mode activates the programmed bridge sequence through the selector switch and the sensor network. In auto mode, the bridge starts with a green road signal and raised barrier, then a ship detected at photo sensor `#1` triggers a `5`-second yellow phase, turns the red light on, and lowers the barrier unless the proximity sensor still sees a vehicle under the gate. Once the road area is clear, the hydraulic bridge rises to the upper limit switch, and after the ship is later detected by photo sensor `#2`, the bridge returns to the down limit, runs another `5`-second yellow phase, and restores the green road signal. For multi-ship passages, the controller requires consistent counts from sensors `#1` and `#2` before the bridge can close again, and the paper also records that the lifting process is `26` seconds slower than the lowering return.

### 3. 逐句溯源

1. 句子 1：The ship-crossing simulator is controlled as a PLC EFSM that couples road traffic signals, barrier-gate motion, hydraulic bridge lifting, and ship detection into one coordinated sequence.
   对应摘录：A, B
2. 句子 2：The controller operates in two modes: manual mode is reserved for maintenance and error handling, while auto mode activates the programmed bridge sequence through the selector switch and the sensor network.
   对应摘录：C
3. 句子 3：In auto mode, the bridge starts with a green road signal and raised barrier, then a ship detected at photo sensor `#1` triggers a `5`-second yellow phase, turns the red light on, and lowers the barrier unless the proximity sensor still sees a vehicle under the gate.
   对应摘录：B, C
4. 句子 4：Once the road area is clear, the hydraulic bridge rises to the upper limit switch, and after the ship is later detected by photo sensor `#2`, the bridge returns to the down limit, runs another `5`-second yellow phase, and restores the green road signal.
   对应摘录：C
5. 句子 5：For multi-ship passages, the controller requires consistent counts from sensors `#1` and `#2` before the bridge can close again, and the paper also records that the lifting process is `26` seconds slower than the lowering return.
   对应摘录：A, B, C
