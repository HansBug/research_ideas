# Prototype Elevator 5 Lantai Berbasis PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文用两组完整运行场景把五层电梯的呼梯、方向优先、门控延时、红外重开、超载保持开门和 emergency 停机链写得很细，可直接形成双 A 电梯样本。

## 条目 1: Five-Floor Timed Door-Cycle and Load-Guard Elevator Controller

- 控制对象：楼宇机电与电梯控制领域的五层 PLC 电梯呼梯、门控与载重保护控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个五层电梯原型的 PLC 控制器，用于管理楼层请求、方向优先服务、定时门控、红外防夹、超载报警与紧急停机。
- 判断：算。对象是真实 elevator prototype 的主控制器，不是展示平台；原文不仅有硬件列表，还用两段完整场景把门控延时、载重判定、途中停靠和 emergency 处理串成了可追溯的控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> Tombol pengendalian dapat memindahkan sangkar naik dan turun sesuai dengan tujuan yang dipilih oleh pengguna, dengan sensor proximity yang secara otomatis menghentikannya di lantai yang dituju. Pintu elevator juga berfungsi dengan baik, membuka secara otomatis ketika mendeteksi keberadaan objek di depannya dan menghentikan motor ketika pintu mencapai limit switch. ... load cell dengan kapasitas 1 kg untuk mengukur beban yang dimasukkan ke dalam lift, serta sistem pintu otomatis untuk meningkatkan keamanan dan kenyamanan.

#### 摘录 B

- 出处：第 4-5 页，Scenario `1`
> Ketika penumpang menekan tombol push button luar pada lantai 1 dengan posisi sangkar yang berada pada lantai 1, maka pintu elevator pada lantai 1 akan otomatis terbuka setelah delay 3 detik ... hingga menyentuh limit switch kanan ...
>
> Apabila tidak ada perintah yang diberikan selama 10 detik maka pintu akan otomatis menutup ...
>
> apabila sensor infrared ... mendeteksi objek maka pintu akan otomatis terbuka.
>
> ... jika berat penumpang mencapai 1 kg pintu elevator akan otomatis terbuka dan buzzer akan berbunyi ... pintu akan tetap terbuka jika berat belum mencapai dibawah 1 kg.
>
> Pada saat sangkar menuju lantai 3 dan terdapat calon penumpang pada lantai 2 yang menekan push button atas ... maka sangkar akan singgah ke lantai 2 ... setelah menyelesaikan perintah maka sangkar akan menuju ke lantai 3.

#### 摘录 C

- 出处：第 5-6 页，Scenario `2`
> Ketika penumpang menekan tombol push button bawah pada lantai 2 ... Maka sangkar pada lantai 3 akan menyelesaikan semua perintah terlebih dahulu pada lantai 3, 4, dan 5. Namun jika tidak ada perintah pada lantai 3, 4, dan 5 maka sangkar akan langsung turun ke lantai 2.
>
> Setelah sangkar sampai pada lantai 2, pintu akan terbuka setelah delay 3 detik ... Apabila tidak ada perintah yang diberikan selama 10 detik maka pintu akan otomatis menutup ...
>
> ... jika ada penumpang baru yang ingin masuk ke dalam sangkar maka sensor infrared akan mendeteksi objek dan pintu akan kembali terbuka ...

#### 摘录 D

- 出处：第 5 页，Scenario `1` / 第 6 页，Conclusion
> Namun pada kondisi yang tidak diinginkan, elevator mengalami kondisi error pada mekanik yang mengharuskan penumpang untuk menekan tombol emergency untuk menghentikan semua sistem pada elevator agar tidak terjadi hal-hal yang tidak diinginkan.
>
> Pada aspek tombol pengendalian, sangkar akan bergerak naik dan turun sesuai dengan penekanan tombol tujuan yang dipilih. Sangkar akan berhenti secara otomatis ketika mencapai lantai yang dituju dengan bantuan sensor proximity.

### 2. 基于原文整理后的自然语言描述

The five-floor PLC elevator controller combines floor-request scheduling, direction-priority service, timed door handling, overload protection, and emergency stop logic in one discrete supervisor. When the cage is already at a requested floor, the door opens after a `3 detik` delay, remains available for commands, and then closes automatically after `10 detik` unless the infrared sensor detects a person or the in-cabin open-door button reissues the open request. Before motion is allowed, the load cell checks whether the passenger load reaches `1 kg`; if the limit is reached, the buzzer is activated and the door is forced back open until the overload condition clears. Once a destination is accepted, the cage travels vertically and stops by proximity sensing at requested floors, while upward or downward hall calls are served according to direction-priority rules, such as stopping at floor 2 on the way from floor 1 to floor 3 or postponing a downward call until pending requests on floors 3-5 are completed. If a mechanical fault occurs, the passenger can trigger the emergency button to halt the whole elevator system rather than letting the controller continue normal execution.

### 3. 逐句溯源

1. 句子 1：The five-floor PLC elevator controller combines floor-request scheduling, direction-priority service, timed door handling, overload protection, and emergency stop logic in one discrete supervisor.
   对应摘录：A, B, C, D
2. 句子 2：When the cage is already at a requested floor, the door opens after a `3 detik` delay, remains available for commands, and then closes automatically after `10 detik` unless the infrared sensor detects a person or the in-cabin open-door button reissues the open request.
   对应摘录：B, C
3. 句子 3：Before motion is allowed, the load cell checks whether the passenger load reaches `1 kg`; if the limit is reached, the buzzer is activated and the door is forced back open until the overload condition clears.
   对应摘录：A, B, C
4. 句子 4：Once a destination is accepted, the cage travels vertically and stops by proximity sensing at requested floors, while upward or downward hall calls are served according to direction-priority rules, such as stopping at floor 2 on the way from floor 1 to floor 3 or postponing a downward call until pending requests on floors 3-5 are completed.
   对应摘录：A, B, C, D
5. 句子 5：If a mechanical fault occurs, the passenger can trigger the emergency button to halt the whole elevator system rather than letting the controller continue normal execution.
   对应摘录：D
