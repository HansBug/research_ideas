# Simulator Proses Pengisian dan Pemasangan Tutup Botol Terkendali PLC Berbantuan Miniatur Konveyor - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把按瓶色选泵灌装、定时停带、封盖与压盖后的重新放行链写得很完整，并明确给出传感器、I/O、自动/手动与时间参数，双 A 条件成立。

## 条目 1: Color-Based Filling and Bottle-Capping Sequence Controller

- 控制对象：工业自动化与离散制造领域的双色瓶体灌装与封盖顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 `PLC Omron` 控制的输送带灌装/封盖控制器，先用 `fiberoptic sensor` 识别红瓶或绿瓶来选择灌装泵，再用 `photoelectric sensor` 触发封盖与压盖气缸，整个过程中输送带会按工位停启。
- 判断：算。对象是论文主控制系统，原文清楚写出输入输出端口、颜色到泵的映射、停带灌装、停带封盖、自动/手动模式和灌装时间参数，不是泛化的装置展示。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，Abstract 与系统机制说明，`paper_content.txt` 第 19-31、181-188 行
> The miniature conveyor machine ... operating mechanism is based on the detection of two different colors.
>
> The performance measurement includes ... observations of the readings of installed sensors for activating all devices on the output side ...
>
> saat botol berwarna merah/hijau terdeteksi oleh photoelectric sensor, maka pompa tangki-1/tangki-2 beroperasi untuk pengisian cairan "rasa strawberry"/"rasa lemon" ... setelah proses pengisian selesai, maka sistem penutup botol beroperasi.

#### 摘录 B

- 出处：第 5-6 页，`3.1.2` 与 `3.2.2`，`paper_content.txt` 第 393-408、466-483 行
> port keluaran PLC ... digunakan untuk keperluan sistem pengisian dan pemasangan tutup botol ... (i) motor 24 Vdc untuk mesin konveyor, (ii) "red" dan "green" water pump dan solenoid valve, (iii) solenoid valve pemasangan tutup botol, dan (iv) solenoid valve pada mekanisme pressing terhadap tutup botol.
>
> I0.04 Sensor Fiber Optic "merah"
> I0.06 Sensor Fiber Optic "hijau"
> I0.08 Sensor Photoelectric "tutup botol"
> ...
> I1.04 Push Button Emergency Stop

#### 摘录 C

- 出处：第 7-8 页，`3.3.1` 与 `3.3.2`，`paper_content.txt` 第 531-559、602-612 行
> simulator dioperasikan dengan dua mode, yaitu manual atau automatic ... Saat mode manual diaktifkan, setiap aktuator ... dapat dioperasikan manual tanpa melalui mekanisme sensor detect on. Saat beroperasi mode automatic, maka program tertanam di dalam PLC beroperasi.
>
> sensor ... berdasarkan deteksi terhadap jenis warna sebagai pen-trigger untuk aktuator guna pengoperasian secara automatic terhadap pompa pengisian, dan silinder pneumatic.
>
> pengamatan terhadap botol warna merah, meliputi pendeteksian, proses pengisian air minuman ke dalam botol, dan pemasangan/pemberian tutup untuk botol, sesuai dengan pemrograman.

#### 摘录 D

- 出处：第 8-9 页，`Tabel 2` 与 `Kesimpulan`，`paper_content.txt` 第 653-669、709-720 行
> 1 Botol Merah 55 detik 470 ml Gagal
> 2 Botol Hijau 45 detik 530 ml Berhasil
> 3 Botol Merah 55 detik 530 ml Berhasil
> 4 Botol Hijau 45 detik 520 ml Berhasil
>
> Sistem pengisian air beroperasi secara otomatis pada saat fiberoptic sensor deteksi keberadaan botol, sehingga konveyor berhenti dan proses pengisian air berlangsung. Proses penutupan botol secara otomatis berfungsi, apabila photoelectric sensor deteksi botol, sehingga konveyor berhenti dan sistem pemasang tutup dan penekan tutup beroperasi. Setelah proses penutupan botol selesai, konveyor beroperasi kembali.

### 2. 基于原文整理后的自然语言描述

The filling-and-capping unit is a PLC-controlled sequential controller for a bottle conveyor with two color-dependent filling branches and a downstream capping station. In automatic mode, a `fiberoptic sensor` identifies whether the arriving bottle belongs to the red or green branch, stops the conveyor at the filling point, and activates the corresponding pump/solenoid set so the bottle is filled for the programmed interval, reported in the paper as `55 s` for red and `45 s` for green trials. After the fill phase completes, the bottle advances to the capping position, where a `photoelectric sensor` stops the conveyor again and triggers the pneumatic cap-placement and cap-pressing actuators. Once capping finishes, the conveyor restarts and the machine releases the bottle to the next process stage, so the overall chain is a clear stop-fill-run-stop-cap-run sequence. The same controller also provides manual pump, capping, and conveyor triggers plus an emergency-stop input, which means the paper preserves both the normal production sequence and the operator-maintenance branches in one explicit PLC state progression.

### 3. 逐句溯源

1. 句子 1：The filling-and-capping unit is a PLC-controlled sequential controller for a bottle conveyor with two color-dependent filling branches and a downstream capping station.
   对应摘录：A, B
2. 句子 2：In automatic mode, a `fiberoptic sensor` identifies whether the arriving bottle belongs to the red or green branch, stops the conveyor at the filling point, and activates the corresponding pump/solenoid set so the bottle is filled for the programmed interval, reported in the paper as `55 s` for red and `45 s` for green trials.
   对应摘录：A, C, D
3. 句子 3：After the fill phase completes, the bottle advances to the capping position, where a `photoelectric sensor` stops the conveyor again and triggers the pneumatic cap-placement and cap-pressing actuators.
   对应摘录：B, D
4. 句子 4：Once capping finishes, the conveyor restarts and the machine releases the bottle to the next process stage, so the overall chain is a clear stop-fill-run-stop-cap-run sequence.
   对应摘录：D
5. 句子 5：The same controller also provides manual pump, capping, and conveyor triggers plus an emergency-stop input, which means the paper preserves both the normal production sequence and the operator-maintenance branches in one explicit PLC state progression.
   对应摘录：B, C
