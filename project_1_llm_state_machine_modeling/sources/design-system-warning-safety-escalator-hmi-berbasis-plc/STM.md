# Design System Warning & Safety Escalator dengan HMI Berbasis PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把扶梯的儿童防护、逆向乘梯告警和夹人反转停机三条安全子链并列写清，形成了一个很强的安全监督控制样本。

## 条目 1: Three-Layer Escalator Safety Supervisor with Reverse Recovery
- 控制对象：楼宇机电与电梯控制领域的 PLC 扶梯 warning & safety 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个扶梯安全监督控制器，用于根据人员高度、上下行方向以及夹人检测结果决定扶梯是否运行、是否报警以及是否反转停机。
- 判断：算。对象是实际扶梯控制系统，原文明确写出了三类安全链、相应传感器条件、报警输出、反转动作和人工停机要求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Safety system description，`paper_content.txt` 第 163-190 行
> Untuk rancangan warning & safety system pada eskalator otomatis berbasis plc & hmi memiliki 3 safety system.
>
> Jika objek mengenai sensor untuk orang dewasa ... sensor dewasa akan mengirimkan sinyal pada PLC dan kemudian eskalator akan bekerja ... apabila objek tidak memenuhi ketinggian sensor untuk orang dewasa ... maka eskalator tidak akan bekerja dan speaker peringatan akan berbunyi.
>
> jika arah eskalator sudah diset (ke atas/ke bawah) dan kemudian ada pengguna dari arah yang berlawanan ... speaker peringatan akan berbunyi.
>
> jika ada objek yang terselip ... maka eskalator akan otomatis berbalik arah beberapa detik dan kemudian, eskalator berhenti bekerja.

#### 摘录 B
- 出处：第 4-5 页，Flowchart explanation，`paper_content.txt` 第 195-237 行
> Jika ada pengguna memenuhi setpoint sensor maka sistem akan aktif dan apabila pengguna tidak memenuhi setpoint maka sistem tidak akan bekerja dan warning system akan aktif.
>
> Pada saat kondisi escalator naik ... apabila ada pengguna eskalator dari atas dan terbaca sensor maka warning system aktif ... Pada saat kondisi escalator turun ... apabila ada pengguna eskalator dari bawah dan terbaca sensor maka warning system aktif.
>
> apabila ada pengguna escalator yang terjepit dan terbaca oleh sensor maka motor akan otomatis berbalik arah dan kemudian sistem akan non-aktif. Kemudian apabila motor tidak berbalik arah maka harus menekan tombol manual off agar motor berhenti.

### 2. 基于原文整理后的自然语言描述

The PLC escalator safety supervisor contains three coordinated protection routines: an adult/child height check at entry, a wrong-direction warning function, and a trapped-user recovery function. In the child-protection branch, two sensors at different heights distinguish adults from children; the adult sensor enables the escalator, whereas a user who only triggers the lower sensor is blocked and the warning speaker is activated. In the direction-protection branch, the active sensor depends on whether the escalator has been set to go up or down, and a user approaching from the opposite side causes the warning system to turn on instead of starting the escalator. In the entrapment branch, a sensor below the escalator triggers automatic reverse motion for a few seconds, then deactivates the system, and if reverse recovery fails the operator must press the manual-off button to stop the motor.

### 3. 逐句溯源

1. 句子 1：The PLC escalator safety supervisor contains three coordinated protection routines: an adult/child height check at entry, a wrong-direction warning function, and a trapped-user recovery function.
   对应摘录：A
2. 句子 2：In the child-protection branch, two sensors at different heights distinguish adults from children; the adult sensor enables the escalator, whereas a user who only triggers the lower sensor is blocked and the warning speaker is activated.
   对应摘录：A, B
3. 句子 3：In the direction-protection branch, the active sensor depends on whether the escalator has been set to go up or down, and a user approaching from the opposite side causes the warning system to turn on instead of starting the escalator.
   对应摘录：A, B
4. 句子 4：In the entrapment branch, a sensor below the escalator triggers automatic reverse motion for a few seconds, then deactivates the system, and if reverse recovery fails the operator must press the manual-off button to stop the motor.
   对应摘录：A, B
