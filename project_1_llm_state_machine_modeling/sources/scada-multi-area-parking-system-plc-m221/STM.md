# SCADA for Prototype of Multi Area Parking System Based on PLC M221 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双区域停车系统写成了由 loop sensor、闸杆电机、满位指示灯和计数/计费逻辑共同驱动的入口-出口联锁控制器，主控制链清晰且可追溯。

## 条目 1: Multi-Area Entry-Exit Barrier and Full-Lot Supervisor

- 控制对象：双区域停车系统的入口/出口闸杆、满位指示与计数联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车位管理领域的多区域停车闸杆控制器，根据 loop sensor、占用计数和满位状态控制入口栏杆、出口栏杆与红绿灯。
- 判断：算。对象是实际停车控制系统，原文不仅给出系统构成，还明确写出车辆到达、入口开杆、满位闭门、出口减计数和解除满位的完整行为链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-26 行
> Loop sensor is used to detect vehicles that will enter or exit the parking door. Input from the sensor will be processed by the PLC to move the doorstop motor, indicator lights and update the display on the HMI.
>
> The system is able to control the opening and closing of the entrance and exit bars, controlling the indicator lights whether or not the parking area is full, ... calculating the number of vehicles and calculating the total cost of revenue in each parking area.

#### 摘录 B

- 出处：第 2 页，`Pendahuluan`，`paper_content.txt` 第 60-67 行
> Setelah sensor membaca bahwa ada data ... lalu data tersebut dikirim ke PLC. Setelah PLC menerima data secara langsung dari sensor loop, maka PLC akan menggerakkan palang pintu dan menyalakan lampu led.
>
> Lampu led berwarna hijau akan menyala jika keadaan parkir masih belum penuh, dan palang pintu akan terbuka. Sebaliknya ketika lampu led berwarna merah maka keadaan parkir sudah full, palang pintu tidak terbuka.

#### 摘录 C

- 出处：第 5-7 页，`hasil uji coba / Tabel 2 / Tabel 3`，`paper_content.txt` 第 191-205、270-334 行
> kondisi awal ... palang pintu dalam kondisi tertutup, lampu indikator hijau menyala, dan lampu indikator merah mati.
>
> Pada saat sensor loop mendeteksi adanya kendaraan yang akan masuk ke area parkir, maka palang pintu akan membuka ... Saat mobil telah masuk area parkir sensor loop menjadi tidak mendeteksi kendaraan sehingga palang pintu menutup ...
>
> Lampu indikator merah akan menyala saat kondisi parkir full (berjumlah 10) dan palang pintu masuk tidak akan membuka meskipun sensor mendeteksi ada mobil di depan pintu masuk.
>
> Saat ada mobil mau keluar ... palang pintu keluar membuka, lampu indikator hijau kembali menyala, dan lampu indikator merah kembali mati.

### 2. 基于原文整理后的自然语言描述

The multi-area parking supervisor starts from a closed-bar idle state in which the entrance and exit barriers are down, the green indicator is on, and the red full indicator is off. When a loop sensor detects a vehicle at an entrance, the PLC opens the corresponding barrier, keeps the green light on if capacity remains available, and updates HMI counters for current occupancy, daily entries, and revenue. After the vehicle passes and the sensor becomes inactive again, the barrier closes and the system returns to the normal monitoring state. Once the occupancy count reaches ten vehicles in an area, the controller switches to a full-lot state in which the red light turns on and the entrance barrier stays closed even if a new vehicle is detected. An exit detection opens the outbound barrier, decrements the active occupancy, and restores the green-not-full condition so entry can resume.

### 3. 逐句溯源

1. 句子 1：The multi-area parking supervisor starts from a closed-bar idle state in which the entrance and exit barriers are down, the green indicator is on, and the red full indicator is off.
   对应摘录：C
2. 句子 2：When a loop sensor detects a vehicle at an entrance, the PLC opens the corresponding barrier, keeps the green light on if capacity remains available, and updates HMI counters for current occupancy, daily entries, and revenue.
   对应摘录：A, B, C
3. 句子 3：After the vehicle passes and the sensor becomes inactive again, the barrier closes and the system returns to the normal monitoring state.
   对应摘录：C
4. 句子 4：Once the occupancy count reaches ten vehicles in an area, the controller switches to a full-lot state in which the red light turns on and the entrance barrier stays closed even if a new vehicle is detected.
   对应摘录：A, B, C
5. 句子 5：An exit detection opens the outbound barrier, decrements the active occupancy, and restores the green-not-full condition so entry can resume.
   对应摘录：A, C
