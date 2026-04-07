# PLC ve SCADA Kontrol Yöntemleri ile Sıvı Dolum Otomasyonu - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 HMI 配方输入、重量闭环灌装、五步封盖、纯/混合标签与闭环传送带联成一条完整 PLC/SCADA 产线控制链。

## 条目 1: HMI-Configured Cup Filling, Capping, and Labeling Line

- 控制对象：PLC/SCADA 液体灌装产线中的配方驱动灌装、封盖与贴标控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个液体灌装产线控制器，允许用户从 HMI 输入产品组合、重量和产量，并驱动液位检查、称重灌装、封盖、贴标和传送带闭环运输。
- 判断：算。对象是实际灌装产线控制系统，原文给出了 HMI 参数选择、阀门开闭、重量闭环、封盖五步序列、纯/混合标签分支以及输送带故障检测链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract`，`paper_content.txt` 第 46-70 行
> In the prototype system, the glasses are filled according to the product selected and their weight from the HMI screen. The contents of the product are entered by the user. The conformity of the contents entered by the user is determined according to the macro code written into the HMI panel. Depending on the desired filling number, the glasses leave the glass storage and arrive at the liquid filling stations. Liquid filling is performed by real-time control of weight sensor data. After the desired amount is filled, the cups of the glasses are attached. Labeling (pure-mixed) is made on the glass cups according to the filling type and sent to the exit ... Thus, the products in the requested quantity and ratio are produced in the automation system fully automatically.

#### 摘录 B

- 出处：第 4-6 页，`SCADA / Sıvı Dolum Prosesi`，`paper_content.txt` 第 313-363 行、第 378-442 行
> production method must be determined according to the production quantity ... if the product quantity to be filled is more than 1, automatic button selection is made from the relevant screen ... 4 different products can be selected ... their gram values are determined ... production quantity is entered ... default maximum is limited to 10.
>
> Liquid filling process ... The selected products are filled into the cups according to the product information entered by the users ... tank levels are measured ... with pressure transmitters ... When the liquid level is at the desired level and the filling signal arrives, pneumatic valves are opened ... when the cup reaches the desired weight, the weight measurement process is used to close the valve ... loadcell module is used.

#### 摘录 C

- 出处：第 6-7 页，`Kapak Takma Prosesi / Bardak Etiketleme Prosesi / Konveyör Bant Kontrolü`，`paper_content.txt` 第 444-529 行
> 1. Adım: Kapak takma istasyonuna bardak gelir. 2. Adım: Kapak deposundan kapak taşıma yerine itilir. 3. Adım: Taşıma yerinden kapak vakum yöntemi ile alınır ve bardağın olduğu konuma götürülür. 4. Adım: 50 milimetrelik dikey eksen hareketiyle kapak takılır. 5. Adım: Milsiz silindir ve vakum başlangıç konumuna döner.
>
> Kapak takma işlemi esnasında işlem adımlarının biri veya birkaçında hata olması halinde prosesin tüm işlemleri baştan başlar.
>
> Birden fazla ürün seçilip istenilen oranlarda karıştırılmasıyla karışık bir ürün içeriği elde edilir ... karışık etiketi basılır. Tek ürün seçimi yapılması durumda ... sade etiketi basılmaktadır.
>
> If the conveyor belt does not move due to the step motor or conveyor belt, errors are detected with encoder information signal.

### 2. 基于原文整理后的自然语言描述

The filling line begins with recipe and quantity selection on the HMI, where the operator chooses one or more products, enters gram values, and sets the production count under a cup-capacity limit. Once the required tank level and fill request are ready, the PLC opens the electropneumatic valve of the selected liquid source and uses loadcell feedback to stop filling when the target cup weight is reached. After filling, the capping station executes a fixed five-step sequence in which the cup arrives, a lid is pushed from storage, vacuum carries the lid to the cup position, a `50 mm` vertical motion applies the lid, and then the cylinder plus vacuum return to the initial position; if any step fails, the capping process restarts from the beginning. The completed cup is then labeled as `pure` or `mixed` according to whether the user selected a single product or a mixture, and the conveyor transport itself is monitored in closed loop by encoder feedback so movement failures can be detected instead of being assumed away.

### 3. 逐句溯源

1. 句子 1：The filling line begins with recipe and quantity selection on the HMI, where the operator chooses one or more products, enters gram values, and sets the production count under a cup-capacity limit.
   对应摘录：A, B
2. 句子 2：Once the required tank level and fill request are ready, the PLC opens the electropneumatic valve of the selected liquid source and uses loadcell feedback to stop filling when the target cup weight is reached.
   对应摘录：A, B
3. 句子 3：After filling, the capping station executes a fixed five-step sequence in which the cup arrives, a lid is pushed from storage, vacuum carries the lid to the cup position, a `50 mm` vertical motion applies the lid, and then the cylinder plus vacuum return to the initial position; if any step fails, the capping process restarts from the beginning.
   对应摘录：C
4. 句子 4：The completed cup is then labeled as `pure` or `mixed` according to whether the user selected a single product or a mixture, and the conveyor transport itself is monitored in closed loop by encoder feedback so movement failures can be detected instead of being assumed away.
   对应摘录：A, C
