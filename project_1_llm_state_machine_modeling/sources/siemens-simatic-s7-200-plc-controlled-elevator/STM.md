# Siemens Simatic S7-200 CPU Model PLC Controlled Elevator - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电梯的呼梯、到层停靠、上下行电机与忙灯联动写成 `12` 个 ladder network，但整体画像与现有电梯同向优先簇高度接近，因此更适合作为双 A 降采样样本。

## 条目 1: Three-Floor Call-and-Limit-Switch Elevator Controller

- 控制对象：楼宇机电与电梯控制领域的三层电梯原型呼梯、停靠与电机方向控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 同向优先电梯调度与门控）

### 0. 条目识别与判定

- 一句话说明：这是一个三层电梯 `PLC` 原型控制程序，利用层外呼梯按钮、轿厢内选层按钮、楼层限位开关、上下行继电器和忙灯来组织停靠与方向切换。
- 判断：算。对象是实际电梯控制器本体，原文对按钮输入、限位触发、电机上/下行和忙灯联动给出了完整 ladder network 说明，不是单纯实验平台介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-24、32-38 行
> Bu çalışmada, Siemens'in SIMATIC S7-200 CPU 224 model PLC'si kullanarak 3 katlı bir asansör prototip kontrolü yapılmıştır. Asansör donanımı; bir DC motor, her katta birer sınır anahtarı, asansör kabini içinde ve katlarda bulunan kumanda düğmeleri ve ikaz lambalarından, yazılımı; 12 Networkten oluşmaktadır.
>
> Three floors elevator prototype control was carried out in this study used by Siemens's SIMATIC S7-200 CPU 224 model PLC. The hardware of elevator includes a DC motor, limit switches used at every floor and inside and outside of elevator control buttons and warning lights/indicators, and software includes 12 Networks.

#### 摘录 B

- 出处：第 4 页，`2. Üç katlı prototip asansör tasarımı ve PLC kontrol uygulaması`，`paper_content.txt` 第 156-183 行
> meşgul lambası, kabin dışı çağırma ve durdurma butonları bulunmaktadır. Kabin tasarımında da bir adet 7 segment display, kabin içi çağırma ve imdat butonları bulunmaktadır.
>
> Bunlar; kabin içerisinde 3 adet kat düğmesi ve bir adet imdat düğmesi, her katta bir adet çağırma düğmesi ve her katta birer sınır anahtarlarıdır. ... Kabin ilgili kat hizasındaki sınır anahtarına çarpınca sınır anahtarından giden sinyal doğrultusunda PLC'ye yüklenen program aracılığıyla motor dolayısı ile kabin durmaktadır.

#### 摘录 C

- 出处：第 7-8 页，`Network 1-8`，`paper_content.txt` 第 317-337、357-381、392-401 行
> Network 1 ... Aşağı_Röleyi (M0.1) aktif eder ve motor aşağı yönde dönmeye başlar. Kabin 1. katın sınır anahtarına çarptığı anda ... motoru kontrol eden rölenin enerjisi kesilmiş olur ve motor durur.
>
> Network 2 ... Yukarı_Röle1’i (M0.2) aktif eder ve motor yukarı yönde dönmeye başlar. Kabin 2. katın sınır anahtarına çarptığı anda ... motor durur.
>
> Network 4 ... Yukarı_Röleyi (M0.0) aktif eder ve motor yukarı yönde dönmeye başlar. Kabin 3. katın sınır anahtarına çarptığı anda ... motor durur.
>
> Motor hareket ettiği zaman meşgul lambaları yanmakta, durduğu zaman ise sönmektedir. ... Motorun yukarı yönde hareketi PLC’nin Q0.0 çıkışı ile kontrol edilmektedir ... Motorun aşağı yönde hareketi PLC’nin Q0.1 çıkışı ile kontrol edilmektedir.

### 2. 基于原文整理后的自然语言描述

The elevator controller manages a three-floor prototype with hall-call buttons, car-call buttons, floor limit switches, warning lamps, and a single DC motor driven upward or downward by PLC relay outputs. The software is organized into `12` ladder networks, and the core motion logic is explicit: a call to floor 1 energizes the downward relay until the floor-1 limit switch is hit, a call to floor 2 energizes the appropriate up or down relay depending on current position until the floor-2 limit switch is hit, and a call to floor 3 energizes the upward relay until the floor-3 limit switch is reached. The controller therefore completes calls through position-triggered stopping rather than through continuous control equations or scheduling heuristics. While the paper is detailed enough for a double-A extraction, its structure is highly similar to the existing direction-priority elevator cluster, so it is best kept as a downsampled EFSM/T0 variant rather than as a new primary representative.

### 3. 逐句溯源

1. 句子 1：The elevator controller manages a three-floor prototype with hall-call buttons, car-call buttons, floor limit switches, warning lamps, and a single DC motor driven upward or downward by PLC relay outputs.
   对应摘录：A, B
2. 句子 2：The software is organized into `12` ladder networks, and the core motion logic is explicit: a call to floor 1 energizes the downward relay until the floor-1 limit switch is hit, a call to floor 2 energizes the appropriate up or down relay depending on current position until the floor-2 limit switch is hit, and a call to floor 3 energizes the upward relay until the floor-3 limit switch is reached.
   对应摘录：A, C
3. 句子 3：The controller therefore completes calls through position-triggered stopping rather than through continuous control equations or scheduling heuristics.
   对应摘录：B, C
4. 句子 4：While the paper is detailed enough for a double-A extraction, its structure is highly similar to the existing direction-priority elevator cluster, so it is best kept as a downsampled EFSM/T0 variant rather than as a new primary representative.
   对应摘录：A, C
