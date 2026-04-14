# RANCANG BANGUN SISTEM PARKIR PINTAR BERBASIS PLC (PROGRAMMABLE LOGIC CONTROLLER) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RFID 身份匹配、空车位分配、模式进入条件、升降平台取位和满位锁闭一起写成了完整的多层停车入库控制链。

## 条目 1: RFID-Guided Empty-Slot Entry Pipeline

- 控制对象：智慧停车与车位管理领域的 RFID 导向型多层停车入库控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个多层停车场入库控制器，用 RFID 身份识别、空位检测、模式选择和机械平台/闸门动作来完成车辆入库。
- 判断：算。对象是实际停车控制系统，原文明确给出 RFID 与数据库匹配、空车位判定、`mode masuk / mode keluar` 区分、目标车位对应 memory 触发，以及平台到达地面后闸门放下作为入库桥面的顺序链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`2.5 Perancangan Visual Studio 2010`，`paper_content.txt` 第 229-255、264-280 行
> Software Visual Studio 2010 ini digunakan untuk menyambungkan data yang dibaca oleh RFID tag dan dicocokan dengan database MYSQL ...
>
> Apabila terdeteksi kamar yang kosong, maka software visual studio akan mengisi database kamar yang kosong dengan nilai 1.
>
> Apabila indikator ID bernilai 0 ... sistem akan secara langsung memilih kamar yang kosong ... Apabila kamar telah penuh, maka ... ditampilkan pesan "Maaf, kamar sudah penuh".
>
> Setelah hasil pembacaan ID cocok, maka sistem akan menampilkan data lengkap dari ID user yang akan masuk dalam sistem.

#### 摘录 B

- 出处：第 6 页，`3.2 Pengujian Sistem Secara Keseluruhan`，`paper_content.txt` 第 382-417 行
> Pengujian sistem secara keseluruhan ... dari pembacaan data RFID sampai sistem mengaktifkan kamar yang akan dituju ...
>
> ladder diagram yang mengaktifkan sistem untuk mengambil kamar 2 dengan alamat memory 220.02. Syarat untuk mengaktifkan memory ini adalah dengan menekan mode masuk ... Memory untuk masuk juga dibatasi dengan sensor photodioda pada setiap kamar. Apabila sensor tidak mendeteksi mobil dalam kamar yang dituju, maka mobil dapat masuk.
>
> Sistem akan mengambil plat dari kamar yang dituju terlebih dahulu dan setelah plat telah mencapai lantai dasar, maka gerbang akan turun sebagai jembatan untuk memasukan mobil kedalam plant.

#### 摘录 C

- 出处：第 6-7 页，`3.3 Hasil Pengujian Sistem Keseluruhan / Kesimpulan`，`paper_content.txt` 第 421-469 行
> Hasil pengujian sistem masuk ... mulai dari proses membaca data RFID sampai mobil memasuki kamar yang telah disediakan.
>
> Output dari lampu indikator penuh ini juga digunakan sebagai pembatas agar sistem tidak dapat lagi memilih mode masuk.
>
> Intelligent parking system mampu mencari kamar yang kosong secara otomatis dan mengeluarkan mobil sesuai dengan data RFID yang masuk.

### 2. 基于原文整理后的自然语言描述

The parking-entry controller begins by reading an `RFID` tag, matching that identifier against a `MySQL` database, and determining whether the vehicle is an entering user whose indicator value is still `0`. If the user is entering and at least one room remains vacant, the front-end software marks an empty room in the database and passes that selection to the PLC side so the corresponding entry sequence can be enabled. To execute the sequence, the operator activates `mode masuk`, the PLC raises the target-room memory bit such as `220.02`, and the selected room's photodiode sensor must still report that no car is occupying that slot. The system then retrieves the platform from the target room to the ground floor, lowers the gate so it becomes a bridge into the plant, and admits the vehicle toward the chosen room. When the full indicator is active, the controller blocks further selection of `mode masuk`, and the overall tests report successful RFID-guided insertion and removal with the controller automatically finding empty rooms and routing cars accordingly.

### 3. 逐句溯源

1. 句子 1：The parking-entry controller begins by reading an `RFID` tag, matching that identifier against a `MySQL` database, and determining whether the vehicle is an entering user whose indicator value is still `0`.
   对应摘录：A
2. 句子 2：If the user is entering and at least one room remains vacant, the front-end software marks an empty room in the database and passes that selection to the PLC side so the corresponding entry sequence can be enabled.
   对应摘录：A
3. 句子 3：To execute the sequence, the operator activates `mode masuk`, the PLC raises the target-room memory bit such as `220.02`, and the selected room's photodiode sensor must still report that no car is occupying that slot.
   对应摘录：B
4. 句子 4：The system then retrieves the platform from the target room to the ground floor, lowers the gate so it becomes a bridge into the plant, and admits the vehicle toward the chosen room.
   对应摘录：B
5. 句子 5：When the full indicator is active, the controller blocks further selection of `mode masuk`, and the overall tests report successful RFID-guided insertion and removal with the controller automatically finding empty rooms and routing cars accordingly.
   对应摘录：C
