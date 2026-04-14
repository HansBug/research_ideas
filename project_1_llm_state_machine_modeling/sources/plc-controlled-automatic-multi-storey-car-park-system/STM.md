# A PLC Controlled Automatic Multi-Storey Car Park System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层九车位自动停车库的密码输入、升降横移、托盘放车/取车与 `2` 秒等待写成完整顺序链，原文和抽取文本都足以支撑双 A 的停车控制样本。

## 条目 1: Cabin-and-Pallet Multi-Storey Parking Supervisor

- 控制对象：智慧停车与车位管理领域的多层停车仓升降、横移与取车放车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个三层自动停车库主控制器，利用密码输入、楼层选择、限位开关、主升降机构和各层托盘电机来完成车辆入库、出库与回初态。
- 判断：算。对象是实际多层停车设备本体，不是停车计数或界面系统；原文明确给出密码、目标层、位置检测、主电机/托盘电机动作和 `2sn` 等待，因此可以稳定整理成停车 EFSM 样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 32-39 行
> Automatic parking lots at present have wide range of usage contributing to solution of traffic problems especially in metropolitan cities. In this study, a prototype automatic parking lot for training purpose having three floors and three arrays resulting nine vehicles capacity has been designed. Application of the designed prototype has been realized by programmable logic controller (PLC). In the realized system, position of the cabin was determined by the PLC with respect to states of border switches. Procedures of placing in and removing out of the vehicle were realized by considering user password and operation requests.

#### 摘录 B

- 出处：第 7-8 页，`4.2. PLC Kontrollü Otomatik Otopark Sistemi / 4.3. Programın Akış Şeması`，`paper_content.txt` 第 257-261、313-337 行
> Araç park yerlerinde ve asansörün üzerinde sınır anahtarları ve sensörler mevcuttur. Bu sensörlerin görevi hem araçların konumunu belirlemek hem de asansörün konumunu belirlemek için uygun yerlere yerleştirilmiştir. Her katta ve her kabin içerisinde sınır anahtarları mevcuttur ve PLC nin girişine bağlıdırlar. Buradan gelen bilgilere bağlı olarak PLC programı çıkış verir.
>
> Gidilecek Katın Şifresini Giriniz ... Girilen Şifre ... Asansörü İleri (sağa) Döndür ... Asansör Motorunu Durdur. 2sn Sonra 1.Palet Motorlarını İleri (sağa) Döndür ... Asansör Motorunu Durdur. 2sn Sonra Kabin Motorunu Yukarı (sağa) Döndür.

#### 摘录 C

- 出处：第 8-9 页，`4.3. Programın Akış Şeması / 4.4. Programın Ladder Diyagramı ile İfade Edilmesi`，`paper_content.txt` 第 297-305、355-373、395-398 行
> Kabin Motorunu Durdur. 2sn Bekle ve 2.Palet Motorlarını İleri (sağa) Döndür ... Palet Motorlarını Durdur ve Asansör Kabinini Aşağı (sola) Döndür.
>
> Durdur. 2sn Bekle ve 3.Palet Motorlarını İleri (sağa) Döndür ... Asansör Motorunu Durdur. 2sn Sonra Kabin Motorunu Yukarı (sağa) Döndür.
>
> Programlar ladder denilen diyagramlarla oluşturulmaktadır. Bu diyagramlar da ayrı ayrı networklerden oluşmaktadır. Programlanan asansör diyagramında her networkün farklı bir işlevi vardır.

### 2. 基于原文整理后的自然语言描述

The parking controller governs a three-floor, nine-space automatic car park rather than a simple slot counter, and it uses PLC-monitored border switches and sensors to know both cabin position and vehicle position. After the user enters the password for the destination floor, the main parking elevator moves horizontally to the required block, then inserts explicit `2` second waits before the pallet motor pushes the vehicle and before the cabin motor lifts or lowers the cabin to the selected floor. The same flowchart also shows the reverse chain for retrieval: once the vehicle is transferred, the pallet motor stops, the cabin returns downward, and the main elevator moves back toward its initial position. Because transition conditions depend jointly on password input, floor choice, sensor-confirmed cabin position, and staged actuator outputs, the controller is better modeled as a timed engineering EFSM than as a plain occupancy FSM.

### 3. 逐句溯源

1. 句子 1：The parking controller governs a three-floor, nine-space automatic car park rather than a simple slot counter, and it uses PLC-monitored border switches and sensors to know both cabin position and vehicle position.
   对应摘录：A, B
2. 句子 2：After the user enters the password for the destination floor, the main parking elevator moves horizontally to the required block, then inserts explicit `2` second waits before the pallet motor pushes the vehicle and before the cabin motor lifts or lowers the cabin to the selected floor.
   对应摘录：B, C
3. 句子 3：The same flowchart also shows the reverse chain for retrieval: once the vehicle is transferred, the pallet motor stops, the cabin returns downward, and the main elevator moves back toward its initial position.
   对应摘录：C
4. 句子 4：Because transition conditions depend jointly on password input, floor choice, sensor-confirmed cabin position, and staged actuator outputs, the controller is better modeled as a timed engineering EFSM than as a plain occupancy FSM.
   对应摘录：A, B, C
