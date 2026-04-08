# Pengembangan program PLC untuk alat pemilah benda berdasarkan warna berbasis diagram keadaan - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把颜色分拣模块的待机、输送、挡停检测和三路分拣动作展开成完整状态图与方程，定时和输出关系都很清楚。

## 条目 1: Color-coded conveyor sorting controller

- 控制对象：工业自动化与离散制造领域的颜色识别、挡停与三路分拣顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业自动化领域的颜色分拣控制器，用于在传送带上检测工件、定时停靠完成颜色识别，并把工件导向对应分拣口。
- 判断：算。对象是实际顺序控制设备，原文给出了状态图、颜色编码、传感器输入、定时触发和各分拣执行器的对应关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，`Gambar 4` 讲解，`paper_content.txt` 第 181-202 行
> Berdasarkan alur logika Gambar 3, dapat disusun diagram keadaan seperti pada Gambar 4. Diagram keadaan yang terbentuk menghasilkan 5 buah Keadaan, dimulai dari S0 yang ditandai dengan FS (first state) atau dapat juga sebagai posisi RUN (alat aktif siap menerima data berupa kedatangan benda kerja pada ujung konveyor dengan sensor kedatangan (Sensor 1), tetapi keadaan output-nya non-aktif semua. Jika Sensor 1 aktif, maka konveyor aktif membawa benda kerja ke lokasi pendeteksi warna (keadaan S1) dan timer aktif selama waktu tertentu (misalnya 3 detik). Setelah pendeteksi warna dapat menentukan kode warna, maka pengkondisi sensor warna mengeluarkan 2-bit kode warna yang mengumpan 2 kanal input PLC sebagai kode warna dan dinyatakan sebagai variabel S_M=merah, S_H=hijau, S_B=biru, dan S_Hi= hitam. Dari gambar tersebut, S3 itu keadaan yang mengaktifkan SEPARATOR1, S4 itu keadaan yang mengaktifkan SEPARATOR2, dan S5 adalah keadaan yang mengaktifkan SEPARATOR3. Sedangkan, S_Hi sebagai benda kerja warna hitam langsung menuju lokasi paling ujung. Hal ini tidak menggerakkan satu pun separator. Ketika S_Akhir berlogika 1, maka semua output akan kembali non aktif. Siklus kerja kembali berulang menanti datangnya benda kerja berikutnya yang dipindai oleh Sensor 1.

#### 摘录 B

- 出处：第 5-6 页，`Tabel 1 / Tabel 2 / Tabel 3`，`paper_content.txt` 第 211-269 行
> Keadaan Konveyor Stopper Separator 1 Separator 2 Separator 3
> S0 0 0 0 0 0
> S1 1 0 0 0 0
> S2 1 1 0 0 0
> S3 1 0 1 0 0
> S4 1 0 0 1 0
> S5 1 0 0 0 1
> T1=START Posisi alat dalam kondisi RUN
> T2= S_Awal Sensor kedatangan benda kerja
> T3=Tim1 Saklar timer aktif untuk menggerakkan STOPPER
> T4= S_M Kode warna merah
> T5= S_H Kode warna hijau
> T6= S_B Kode warna biru
> T7= S_Hi Kode warna hitam
> T8= S_Akhir Sensor akhir perjalanan benda kerja
> T9= S_Akhir Sensor akhir perjalanan benda kerja
> T10= S_Akhir Sensor akhir perjalanan benda kerja
> S0 = (S0 + T1+T8). T2̅̅̅̅ Posisi standby (semua output off)
> S1 = (S1 + T2). T3̅̅̅̅ KONVEYOR aktif
> S2 = (S2 + T3). T4̅̅̅̅.T5̅̅̅̅ STOPPER aktif
> S3 = (S3 + T4). T8̅̅̅̅ SEPARATOR1 aktif
> S4 = (S4 + T5). T9̅̅̅̅ SEPARATOR2 aktif
> S5 = (S5 + T6). T10̅̅̅̅̅ SEPARATOR3 aktif
> KONVEYOR = S1+S2+S3+S4+S5
> STOPPER = S2
> SEPARATOR1 = S3
> SEPARATOR2 = S4
> SEPARATOR3 = S5

### 2. 基于原文整理后的自然语言描述

The color-sorting controller starts in standby state `S0` with all outputs off and waits for `Sensor 1` to detect an incoming workpiece. Detection moves the system to `S1`, where the conveyor runs, and then to `S2`, where the `STOPPER` is activated for about three seconds so that the color sensor can produce one of the four codes `S_M`, `S_H`, `S_B`, or `S_Hi`. Red, green, and blue workpieces branch to `S3`, `S4`, and `S5`, activating `SEPARATOR1`, `SEPARATOR2`, or `SEPARATOR3` while the conveyor keeps running; black workpieces do not activate any separator and continue directly to the end position. When `S_Akhir` is asserted, the active branch resets to `S0`, so the machine is a timed EFSM whose guards are built from arrival sensing, color-code inputs, and an explicit detection timer.

### 3. 逐句溯源

1. 句子 1：The color-sorting controller starts in standby state `S0` with all outputs off and waits for `Sensor 1` to detect an incoming workpiece.
   对应摘录：A, B
2. 句子 2：Detection moves the system to `S1`, where the conveyor runs, and then to `S2`, where the `STOPPER` is activated for about three seconds so that the color sensor can produce one of the four codes `S_M`, `S_H`, `S_B`, or `S_Hi`.
   对应摘录：A, B
3. 句子 3：Red, green, and blue workpieces branch to `S3`, `S4`, and `S5`, activating `SEPARATOR1`, `SEPARATOR2`, or `SEPARATOR3` while the conveyor keeps running; black workpieces do not activate any separator and continue directly to the end position.
   对应摘录：A, B
4. 句子 4：When `S_Akhir` is asserted, the active branch resets to `S0`, so the machine is a timed EFSM whose guards are built from arrival sensing, color-code inputs, and an explicit detection timer.
   对应摘录：A, B
