# Model Sistem Otomatis Water Treatment Plant Menggunakan PLC Berbasis Wireless - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把水处理厂的进水、配水、反冲洗和应急告警都写成了 `PLC` 监督控制逻辑，并给出了阈值、时刻条件、泵阀联动和告警响应，足以形成双 A 的过程控制样本。

## 条目 1: Wireless PLC Water-Treatment Pump-Scheduling Supervisor

- 控制对象：过程与环境控制领域的水处理厂进水、配水、反冲洗与应急监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于无线通信的 `PLC` 水处理厂监督控制器，用液位、压力、浊度和故障参数调度 intake、distribution、backwash 与 emergency 四类子过程。
- 判断：算。对象是实际水处理厂自动控制系统，而不是单纯 `HMI/OPC` 平台；原文直接说明了 `M1-M4` 的职责、自动启泵区间、反冲洗阈值与时间条件、以及应急按钮和过流故障的响应。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-25 行
> Conventional water treatment process such as intake ... are carried out manually ... The solution to this problem is that each process is installed with sensors ... then the data from the sensors installed in the plant are processed by the PLC, so that the water treatment process can be carried out automatically ... design of the automatic water treatment plant system model in handling the scheduling of pump intake, distribution, and backwash ... This can minimize errors due to human errors ...

#### 摘录 B

- 出处：第 2 页，`Arsitektur`，`paper_content.txt` 第 137-179 行
> Perencanaan sistem otomatis pada model Sistem WTP ... mengenai peletakan titik-titik sensor dan aktuator ...
>
> M1 = Motor Intake
> M2 = Motor Backwash
> M3 = Motor Distribusi
> M4 = dosing Pump
>
> Sensor Flow & pressure ... Sensor Turbidity ... Sensor Level ...

#### 摘录 C

- 出处：第 5-6 页，`Pengujian Sistem`，`paper_content.txt` 第 461-596 行
> Pengujian sistem dilakukan ... pengujian kontrol pump intake, distribusi, backwash, dan alarm untuk emergensi ...
>
> Pada pengujian ini dilakukan pengujian penyalaan pump intake secara otomatis pada ketinggian bak reservoir 2 sampai 4.5 meter ...
>
> Untuk pengujian sistem indikator kontrol distribusi ... pump 4, pump 5, pump 6 ... bekerja sesuai dengan parameter pressure ...
>
> Proses backwash akan terjadi apabila nilai turbidity memenuhi set value ... Pump 1 dan Solenoid valve 4 akan aktif ketika kondisi turbidity bernilai 45 NTU. Kemudian untuk SV2, SV3 dan kontrol intake akan mati sampai kondisi turbidity kembali lagi mencapai nilai terendah yaitu 10 NTU.
>
> Proses backwash selain dari parameter turbidity juga dipengaruhi berdasarkan waktu ... NTU > 45 ... Waktu > 22:30:00 ... Backwash.
>
> semua kondisi emergensi dapat memberikan notofikasi pada HMI, WW, dan buzzer yang berbunyi di plant.

### 2. 基于原文整理后的自然语言描述

The system is a PLC-supervised water-treatment plant controller for intake, distribution, backwash, and emergency handling rather than a pure data-monitoring platform. Its architecture defines `M1` as intake, `M2` as backwash, `M3` as distribution, and `M4` as dosing pump, with level, flow, pressure, turbidity, pH, and related sensors feeding the automatic logic. Intake pumps start automatically when the reservoir level falls into the configured low band and stop after recovery, distribution pumps are scheduled against pressure conditions, and backwash is enabled only when turbidity reaches `45 NTU` and the time condition after `22:30:00` is satisfied; during that mode, `Pump 1` and `Solenoid Valve 4` turn on while `SV2`, `SV3`, and intake control are shut down until turbidity falls back to `10 NTU`. Separate emergency logic also raises `HMI/Wonderware` pop-ups and buzzer alarms for the emergency button or pump over-current conditions, so the paper supports a detailed EFSM/T1 supervisory sample.

### 3. 逐句溯源

1. 句子 1：The system is a PLC-supervised water-treatment plant controller for intake, distribution, backwash, and emergency handling rather than a pure data-monitoring platform.
   对应摘录：A, C
2. 句子 2：Its architecture defines `M1` as intake, `M2` as backwash, `M3` as distribution, and `M4` as dosing pump, with level, flow, pressure, turbidity, pH, and related sensors feeding the automatic logic.
   对应摘录：B
3. 句子 3：Intake pumps start automatically when the reservoir level falls into the configured low band and stop after recovery, distribution pumps are scheduled against pressure conditions, and backwash is enabled only when turbidity reaches `45 NTU` and the time condition after `22:30:00` is satisfied; during that mode, `Pump 1` and `Solenoid Valve 4` turn on while `SV2`, `SV3`, and intake control are shut down until turbidity falls back to `10 NTU`.
   对应摘录：A, C
4. 句子 4：Separate emergency logic also raises `HMI/Wonderware` pop-ups and buzzer alarms for the emergency button or pump over-current conditions, so the paper supports a detailed EFSM/T1 supervisory sample.
   对应摘录：C
