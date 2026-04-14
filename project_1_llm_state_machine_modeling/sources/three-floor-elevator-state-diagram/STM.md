# Perancangan simulator lift 3 lantai menggunakan diagram keadaan - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电梯的外部呼梯、轿厢内选层、限位停靠与上下行输出都展开成状态图和布尔方程，证据强度足够达到双 A，但与现有电梯主簇高度趋同。

## 条目 1: Three-floor elevator request-and-floor-selection controller

- 控制对象：楼宇机电与电梯控制领域的三层电梯呼梯、选层与上下行驱动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 同向优先电梯调度与门控）

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电与电梯控制领域的三层电梯控制器，用于处理层站呼梯、轿厢内选层、上行/下行方向决策以及到层停靠。
- 判断：算。对象是实际电梯控制系统，原文不仅给出外部与内部两套状态图，还把按钮、限位开关、状态方程和上下行输出完整列成可执行的状态逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`Gambar 3` 讲解，`paper_content.txt` 第 156-170 行
> Dengan mengambil asumsi lift bekerja hanya 3 lantai terdapat tombol-tombol di setiap pintu masuk lift di setiap lantai, yakni tombol (dengan variabel) UR_1 di lantai 1, DR_2 dan UR_2 di lantai 2, serta DR_3 di lantai 3. Sementara DR_4 dan UR_3 tidak digunakan karena hanya 3 lantai yang difungsikan. Maksud permintaan (request) tombol lantai adalah kondisi pengguna menekan tombol untuk setiap lantai. Sebagai contoh, jika pengguna menekan tombol UR_1 di lantai 1 dan sementara lift berada pada posisi lantai 3 (limit switch LS_3D berlogika 1), maka motor DOWN akan aktif yang membuat box/car akan bergerak turun dan berhenti di lantai 1, dengan mekanisme dihentikan oleh limit switch LS_1D. Terlihat di Gambar 3. Dari pengguna S0, T1 berlogika 1 karena logika tombol UR_1 (tombol UP di lantai 1) serta limit switch LS_3D berlogika 1 bersamaan. Hal yang sama terjadi jika lift berada di lantai 2. Logika T2 ekivalen dengan UR_1 dan limit switch LS_2D berlogika 1 (bersamaan). Untuk kasus ini, mekanisme ini tidak berlaku (dan tidak digambarkan di diagram keadaan), seandainya box/car berada di lantai 1. Jadi, pengguna S1 s.d. S3 menggambarkan pengguna berada di lantai 1 atau 2 yang hendak ke lantai yang lebih tinggi. Demikian juga, jika pengguna berada di lantai 3 atau 2 yang hendak turun, maka mekanismenya digambarkan pada pengguna S4 s.d. S6. Perlu diketahui keadaan S0 adalah kondisi keluaran yang tidak aktif semua pada saat box/car sudah mencapai lantai tertentu.

#### 摘录 B

- 出处：第 5 页，`Tabel 1 / Tabel 2`，`paper_content.txt` 第 203-237 行
> T1= (UR_1).(LS_3U) UR lantai 1, posisi box/car di lt.3
> T2= (LS_1D) sensor posisi lt.1 akibat UR_1
> T3= (UR_1).(LS_2U) UR lantai 1, posisi box/car di lt.2
> T4= (UR_2).(LS_3U) UR lantai 2, posisi box/car di lt.3
> T5= LS_2D sensor posisi lt.2 akibat UR_2
> T6= (UR_3).(LS_1D) DR lantai 3, posisi box/car di lt.1
> T7= (LS_3U) sensor posisi lt.3 akibat DR_3
> T8= (DR_3).(LS_2D) DR lantai 3, posisi box/car di lt.2
> T9= (DR_2).(LS_1D) DR lantai 2, posisi box/car di lt.1
> T10=LS_2U sensor posisi lt.2 akibat DR_2
> T11=(LS_1D).(L_2) di dalam box/car di lt.1 Up ke lt.2
> T12=(LS_1D).(L_3) di dalam box/car di lt.1 Up ke lt.3
> T13=(LS_2D).(LS_2U).(L_3) di dalam box/car di lt.2 Up ke lt.3
> T14=(LS_2D).(LS_2U).(L_1) di dalam box/car di lt.2 Down ke lt.1
> T15=(LS_3U).(L_2) di dalam box/car di lt.3 Down ke lt.2
> T16=(LS_3U).(L_1) di dalam box/car di lt.3 Down ke lt.1
> S1 = (S1 + T1). T2̅̅̅̅ MOTOR_DN =1 , MOTOT_UP=0
> S2 = (S2 + T3). T2̅̅̅̅ MOTOR_DN=1 , MOTOT_UP=0
> S3 = (S3 + T4). T5̅̅̅̅ MOTOR_DN=1 , MOTOT_UP=0
> S4 = (S4 + T6). T7̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S5 = (S5 + T8). T7̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S6 = (S6 + T9). T10̅̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S7 = (S7 + T11). T2̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S8 = (S8 + T12). T2̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S9 = (S9 + T13). T5̅̅̅̅ MOTOR_DN=0 , MOTOT_UP=1
> S10 = (S10 + T14). T7̅̅̅̅ MOTOR_DN=1 , MOTOT_UP=0
> S11 = (S11 + T15). T7̅̅̅̅ MOTOR_DN=1 , MOTOT_UP=0
> S12 = (S12 + T16). T10̅̅̅̅̅ MOTOR_DN=1 , MOTOT_UP=0

### 2. 基于原文整理后的自然语言描述

The controller uses `S0` as a central idle state in which all outputs are off whenever the elevator car has already reached a floor. External hall calls are represented by states `S1-S6`, where requests such as `UR_1`, `UR_2`, `DR_2`, and `DR_3` are combined with the current-floor limit switches so that the car drives with either `MOTOR_DN` or `MOTOR_UP` until the corresponding arrival sensor is triggered. Internal car selections are represented by states `S7-S12`, where buttons `L_1`, `L_2`, and `L_3` are enabled only when they request a different floor from the current one, and the same limit-switch conditions are reused to stop the motion at the selected destination. The paper therefore gives a complete request-to-motion mapping from button inputs and floor sensors to up/down motor outputs, but it does not introduce a door timer or other explicit timing window, so the case is best treated as a `T0` elevator EFSM.

### 3. 逐句溯源

1. 句子 1：The controller uses `S0` as a central idle state in which all outputs are off whenever the elevator car has already reached a floor.
   对应摘录：A
2. 句子 2：External hall calls are represented by states `S1-S6`, where requests such as `UR_1`, `UR_2`, `DR_2`, and `DR_3` are combined with the current-floor limit switches so that the car drives with either `MOTOR_DN` or `MOTOR_UP` until the corresponding arrival sensor is triggered.
   对应摘录：A, B
3. 句子 3：Internal car selections are represented by states `S7-S12`, where buttons `L_1`, `L_2`, and `L_3` are enabled only when they request a different floor from the current one, and the same limit-switch conditions are reused to stop the motion at the selected destination.
   对应摘录：A, B
4. 句子 4：The paper therefore gives a complete request-to-motion mapping from button inputs and floor sensors to up/down motor outputs, but it does not introduce a door timer or other explicit timing window, so the case is best treated as a `T0` elevator EFSM.
   对应摘录：A, B
