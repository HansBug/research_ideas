# Perencanaan Eskalator Lantai Satu ke Dua pada Gedung Direktorat Politeknik Negeri Samarinda dengan Kendali PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把扶梯写成“红外触发启动 -> `100 ms` 星三角切换 -> `10 min` 无人延时停机 -> 安全传感器触发 `brake` 锁停”的完整 PLC 控制链。

## 条目 1: Infrared-Triggered Star-Delta Escalator Run-Hold-Stop with Safety Brake

- 控制对象：楼宇机电领域的 PLC 扶梯乘客感知与安全制动控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个扶梯控制器，用于在乘客进入时自动启动电机、完成星三角切换、在长时间无人时延时停机，并在安全开关触发时立即制动。
- 判断：算。对象是实际楼宇扶梯控制系统，原文明确给出红外输入、安全输入、主接触器/星三角接触器/制动器输出，以及 `100 ms` 与 `10 min` 两类时间条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Abstrak`
> Escalators will work if a passenger is detected by an infrared sensor. If no passengers are detected, the escalator will stop working within the specified time period. When there is a problem in the system that can result in an accident to the passenger, the security sensor will work to stop the escalator.

#### 摘录 B

- 出处：第 14-15 页，`Y. Deskripsi Kerja Rangkaian Kontrol`
> Ketika sensor infra merah 1 mendeteksi adanya penumpang maka akan memberikan sinyal kepada input PLC untuk mengaktifkan kontaktor utama eskalator 1. Ketika kontaktor utama eskalator 1 bekerja maka akan mengaktifkan motor dengan mengaktifkan timer, mengaktifkan kontaktor star ... kemudian mengaktifkan kontaktor delta ... Timer 000 ... disetting dengan waktu jeda selama 100 ms ... Ketika tidak ada penumpang ... T001 akan bekerja ... namun jika sensor infra merah mendeteksi adanya penumpang sebelum motor listrik berhenti maka timer tersebut akan direset ... hingga benar-benar tidak ada penumpang selama jeda waktu ... 10 menit ... Ketika terjadi sebuah masalah pada eskalator ... brake 1 aktif, arus menuju kontaktor utama akan diputus, motor akan berhenti bekerja dan brake akan bekerja untuk menghentikan eskalator yang masih bergerak.

### 2. 基于原文整理后的自然语言描述

When the operator turns the escalator start key on, the PLC enables the infrared passenger sensor for that escalator. As soon as a passenger is detected, the PLC energizes the main contactor, starts the motor through the star contactor, and after a short timer of about `100 ms` transfers the motor to the delta connection for normal running. If passengers keep arriving before the idle-stop timer expires, the stop timer is reset and the escalator continues to run. Only when no passenger is detected for the full delay of about `10 minutes` does the PLC command the motor to stop. If any safety device reports a fault condition, the PLC cuts power to the main contactor and activates the brake so that the escalator is forced to stop and remain locked until the stop/reset action is applied.

### 3. 逐句溯源

1. 句子 1：When the operator turns the escalator start key on, the PLC enables the infrared passenger sensor for that escalator.
   对应摘录：B
2. 句子 2：As soon as a passenger is detected, the PLC energizes the main contactor, starts the motor through the star contactor, and after a short timer of about `100 ms` transfers the motor to the delta connection for normal running.
   对应摘录：B
3. 句子 3：If passengers keep arriving before the idle-stop timer expires, the stop timer is reset and the escalator continues to run.
   对应摘录：A, B
4. 句子 4：Only when no passenger is detected for the full delay of about `10 minutes` does the PLC command the motor to stop.
   对应摘录：A, B
5. 句子 5：If any safety device reports a fault condition, the PLC cuts power to the main contactor and activates the brake so that the escalator is forced to stop and remain locked until the stop/reset action is applied.
   对应摘录：A, B
