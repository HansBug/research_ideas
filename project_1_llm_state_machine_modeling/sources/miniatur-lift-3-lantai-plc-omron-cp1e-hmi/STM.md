# RANCANG BANGUN MINIATUR LIFT 3 LANTAI MENGGUNAKAN PLC OMRON CP1E DENGAN HMI - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：这篇本科毕业设计把三层电梯的内外呼梯、门控计时、楼层定位和运动中门禁保护都写成了完整的工程控制链，足以诚实维持双 A。

## 条目 1: Three-Floor Call-and-Door Lift Supervisor

- 控制对象：楼宇机电与电梯控制领域的三层电梯呼梯与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 Omron PLC 驱动的三层电梯控制器，统一管理外部上/下呼梯、轿厢内楼层选择、到站开关门、门控计时和运行中禁开门保护。
- 判断：算。对象是实际电梯控制样机，原文不仅写出输入输出分配和楼层/安全限位，还给出多组流程图与场景分析来说明呼梯、到站、开关门和误操作保护。

### 1. 原文摘录

#### 摘录 A

- 出处：第 38-39 页，`3.1.1 Pengoperasian Miniatur Lift`，`paper_content.txt` 第 1077-1105 行
> Dalam keadaan normal, Power On ... lift akan stand by.
>
> jika salah satu tombol naik/turun ... ditekan, maka lift akan bergerak mengikuti perintah ... Setelah lift sampai dilantai yang dituju maka pintu akan membuka secara otomatis dan menutup kembali dengan timer yang sudah diprogram.
>
> Ketika lift dalam kondisi masih bergerak naik/turun ... tombol buka pintu lift maka perintah tersebut tidak akan bekerja.

#### 摘录 B

- 出处：第 54-56 页，`Tabel 4.1 / Tabel 4.2`，`paper_content.txt` 第 1502-1586 行
> masukan (input) pada PLC ... yaitu push button dan limit switch sedangkan komponen keluaran (output) yaitu motor.
>
> Input 0.05 digunakan untuk limit switch safety up ... Input 0.06 digunakan untuk limit switch lantai satu ... 0.07 ... lantai dua ... 0.08 ... lantai tiga ... Input 0.09 digunakan untuk limit switch safety down.
>
> Input 1.04 dan 1.05 digunakan untuk push button buka dan tutup pintu lift ... Output 100.00 dan 100.01 digunakan untuk motor ketika lift naik dan lift turun ... Output 100.02-100.07 digunakan untuk motor ketika pintu lift membuka dan menutup saat berada dilantai satu, dua, dan tiga.

#### 摘录 C

- 出处：第 69 页，`4.4 Analisa Sistem Miniatur Lift 3 Lantai`，`paper_content.txt` 第 1792-1813 行
> Seseorang (A) menekan push button naik ... lift akan bergerak menuju lantai dua ... pintu lift akan otomatis terbuka ... kemudian orang (A) menekan push button lantai tiga ... setelah lift sampai dilantai tiga maka pintu lift akan terbuka dan tertutup secara otomatis.
>
> orang (B) menekan push button turun ... posisi lift sudah berada dilantai tersebut maka pintu lift akan langsung terbuka tanpa menunggu lift bergerak.
>
> orang (B) tanpa sengaja menekan push button buka pintu lift ... maka push button tersebut tidak akan berfungsi ... ketika posisi lift dalam keadaan diam di suatu lantai.

### 2. 基于原文整理后的自然语言描述

The three-floor lift controller waits in a standby state until a hall-call button or an in-car floor-selection button requests movement to a specific floor. Its PLC input map includes floor-call buttons, in-car floor buttons, `open` and `close` door buttons, floor-position limit switches for levels `1`, `2`, and `3`, plus upper and lower safety limit switches that bound the vertical travel. After the lift reaches the requested floor, the controller stops the car, opens the corresponding door automatically, and recloses it after a programmed timer interval. Manual `open` and `close` commands are only valid while the car is stationary at a floor, so a door-open request issued during upward or downward motion is ignored as a safety guard. The scenario analysis further shows that a hall call placed on the same floor can trigger immediate door opening without extra travel, while subsequent in-car requests continue the service chain to the next requested floor.

### 3. 逐句溯源

1. 句子 1：The three-floor lift controller waits in a standby state until a hall-call button or an in-car floor-selection button requests movement to a specific floor.
   对应摘录：A, B
2. 句子 2：Its PLC input map includes floor-call buttons, in-car floor buttons, `open` and `close` door buttons, floor-position limit switches for levels `1`, `2`, and `3`, plus upper and lower safety limit switches that bound the vertical travel.
   对应摘录：B
3. 句子 3：After the lift reaches the requested floor, the controller stops the car, opens the corresponding door automatically, and recloses it after a programmed timer interval.
   对应摘录：A, C
4. 句子 4：Manual `open` and `close` commands are only valid while the car is stationary at a floor, so a door-open request issued during upward or downward motion is ignored as a safety guard.
   对应摘录：A, C
5. 句子 5：The scenario analysis further shows that a hall call placed on the same floor can trigger immediate door opening without extra travel, while subsequent in-car requests continue the service chain to the next requested floor.
   对应摘录：C
