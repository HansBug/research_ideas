# Simulasi Traffic Light Persimpangan 4 Arah untuk Optimasi Alur Kendaraan Menggunakan Programmable Logic Controller (PLC) Omron CP1L - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：虽然题目和摘要反复提“optimasi”，但正文真正给出的可复用核心是一条非常清楚的四向定时交通灯循环，含初始全红、各方向绿灯 `6` 秒、黄灯过渡和循环复位。

## 条目 1: Four-Way 6-Second Timed Traffic Light Cycle

- 控制对象：道路交通信号控制领域的四向路口定时交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `Omron CP1L` 和 ladder timer 实现的四向路口交通灯顺序控制器，按 `all red -> green 1 -> green 2 -> green 3 -> green 4 -> reset` 的节拍循环运行。
- 判断：算。对象是实际交通信号控制系统，原文明确写出了初始状态、各方向放行时长、黄灯过渡、单方向互斥和定时器复位链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-8 页，`Perancangan Sistem Traffic Light`，`paper_content.txt` 第 218-280 行
> Diagram alir ini menggambarkan alur kerja sistem traffic light untuk sebuah persimpangan empat arah. Dengan menggunakan sistem pendekatan siklus sederhana yang diatur secara berurutan, di mana lampu hijau akan menyala untuk setiap arah secara bergantian dengan durasi waktu tertentu.
>
> Sistem traffic light dimulai dan masuk ke dalam siklus operasi. Pada tahap ini, semua lampu merah menyala terlebih dahulu untuk memastikan keamanan sebelum memulai siklus lampu hijau.
>
> Lampu hijau pada arah pertama tetap menyala selama 6 detik ... Lampu hijau untuk arah kedua tetap menyala selama 6 detik ... Waktu 6 detik diberikan kepada kendaraan dari arah ketiga ... Lampu hijau pada arah keempat tetap menyala selama 6 detik. Setelah waktu ini selesai, sistem akan kembali ke langkah pertama untuk memulai siklus berikutnya.

#### 摘录 B

- 出处：第 8-10 页，`Perancangan di Software CX-Programmer`，`paper_content.txt` 第 287-295 行、第 341-357 行
> Diagram ini dirancang untuk mengatur siklus lampu hijau, kuning, dan merah secara bergantian pada persimpangan empat arah dengan pendekatan berbasis waktu. Ladder diagram yang disajikan mengintegrasikan logika kontrol sederhana melalui penggunaan timer untuk mengatur durasi lampu di pada setiap simpang.
>
> Sistem dimulai dengan kondisi tombol ON yang aktif ... timer 1 akan memulai siklus pertama pada Persimpangan 1. Timer 1 akan mengaktifkan lampu hijau pada simpang 1, di sisi lain lampu merah tetap menyala di simpang yang lain ... Timer 3 akan mengaktifkan lampu hijau pada simpang 2 ...
>
> Setelah lampu hijau selesai, timer 2 mengatur durasi lampu kuning pada simpang 1 sebagai transisi sebelum lampu berubah menjadi merah. Setelah siklus lampu hijau dan kuning selesai pada satu simpang, sistem secara otomatis akan beralih ke simpang berikutnya sesuai urutan yang ditentukan.

#### 摘录 C

- 出处：第 11 页，`Gambar 9. Kondisi Lampu Hijau 4 Hidup`，`paper_content.txt` 第 371-381 行
> Setelah seluruh simpang mendapatkan giliran, mulai dari simpang 1 sampai simpang 4, sistem secara otomatis diatur ulang oleh timer 8 untuk memulai siklus kembali dari simpang 1.
>
> Pengendalian sistem dirancang untuk memastikan bahwa hanya satu simpang yang mendapatkan lampu hijau pada satu waktu, menjaga kelancaran dan keamanan lalu lintas.
>
> Lampu hijau diberikan durasi yang cukup untuk kendaraan melintas, dilanjutkan dengan lampu kuning sebagai tanda transisi sebelum berganti ke lampu merah. Saat lampu merah aktif di satu simpang, giliran akan diberikan ke simpang lainnya sesuai siklus yang telah ditentukan, dan proses ini terus berulang secara terprogram.

### 2. 基于原文整理后的自然语言描述

The controller is a timer-driven four-way traffic-light FSM that starts from an all-red safety state before entering the cyclic service sequence. It then gives the green signal to direction `1`, `2`, `3`, and `4` in order, with each green phase lasting `6` seconds before the cycle advances. The ladder program uses dedicated timers to realize not only the green intervals but also the yellow transitional phase that bridges each green-to-red handoff. While one direction is green, all other directions remain red, and once all four approaches have been served, `timer 8` resets the controller so the sequence restarts from direction `1`. This yields a canonical timed intersection cycle with explicit phase order, single-green mutual exclusion, and timer-based transition guards.

### 3. 逐句溯源

1. 句子 1：The controller is a timer-driven four-way traffic-light FSM that starts from an all-red safety state before entering the cyclic service sequence.
   对应摘录：A, B
2. 句子 2：It then gives the green signal to direction `1`, `2`, `3`, and `4` in order, with each green phase lasting `6` seconds before the cycle advances.
   对应摘录：A
3. 句子 3：The ladder program uses dedicated timers to realize not only the green intervals but also the yellow transitional phase that bridges each green-to-red handoff.
   对应摘录：B
4. 句子 4：While one direction is green, all other directions remain red, and once all four approaches have been served, `timer 8` resets the controller so the sequence restarts from direction `1`.
   对应摘录：B, C
5. 句子 5：This yields a canonical timed intersection cycle with explicit phase order, single-green mutual exclusion, and timer-based transition guards.
   对应摘录：A, B, C
