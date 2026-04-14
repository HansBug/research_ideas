# Implementasi Outseal PLC Pada Automatic Duck Egg Washing Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把鸭蛋清洗机的温控、输送、计数、临时停机复位和 `20` 秒烘干链全部落到 Outseal PLC ladder 上，定时与阈值信息足够完整，可直接作为工业顺序控制样本。

## 条目 1: Egg Washing-Counting-Drying Sequence Controller

- 控制对象：鸭蛋自动清洗、计数与烘干一体机的 Outseal PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是农产品清洗设备里的顺序控制器，用 Outseal PLC 协调输送带、喷淋泵、加热器、温度传感、接近计数和烘干器，完成洗蛋机的连续运行与临时复位。
- 判断：算。对象是实际鸭蛋清洗机，原文直接给出 `40°C` 温控 set point、接近传感器计数阈值、`20` 秒烘干计时、push button 启停和 reset 互锁逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 13-22、35-37 行
> The purpose of this research is to present an efficient automatic duck egg washing machine with Outseal PLC. ... The machine testing process is designed to be carried out with an automatic duck egg washing process continuously until it reaches the maximum expected results.
>
> From this research, an automatic duck egg washing product controlled using an Outseal PLC, with a maximum conveyor speed of 21 RPM ... is able to work in washing duck eggs automatically is 1,980 eggs in 1 hour.

#### 摘录 B

- 出处：第 6-7 页，`Implementasi Software / Modul Sensor Suhu / Modul Sensor Deteksi Telur`，`paper_content.txt` 第 407-420、425-452 行
> Implementasi software dilakukan dengan pembuatan modul sensor suhu terlebih dahulu ... data dikirimkan ke Outseal PLC sebagai input dalam mendeteksi heater agar suhu air dalam bak penampungan tetap stabil.
>
> Sensor suhu dirancang bekerja maksimal pada saat suhu di set 40 oC ... Jika suhu terdeteksi dibawah set point maka Outseal PLC akan mendapat input High, kemudian Heater pun aktif hingga suhu sesuai set point.
>
> Sensor pendeteksi telur dirancang menggunakan sensor adjustable proximity infrared. ... ketika input proximity atau S4 High, maka akan memberi input kepada fungsi counter untuk menghitung jumlah telur yang masuk. Jika jumlah telur sudah sesuai set point, maka akan memberi instruksi ke R10 (interlock reset) untuk me-non-aktifkan sistem sementara.

#### 摘录 C

- 出处：第 8-10 页，`Hairdyer / Counter / Reset / Kesimpulan`，`paper_content.txt` 第 489-493、597-602、618-625、640-693 行
> hairdyer akan aktif apabila input push button S7 ditekan. Hairdyer akan menyala hingga telur kering. Ketika fungsi timer sudah sesuai set point, maka hairdryer akan OFF.
>
> Jika jumlah telur telah mencapai 10, maka akan menghidupkan coil reset R10. Ketika di uji coba, hasil penghitungan telur telah sesuai.
>
> R12 dipasang NC agar ketika diberi logika high, maka jalur akan terputus dan output akan OFF sementara hingga tombol reset ditekan. ... counter akan di-reset ke-0 dan sistem kembali menyala.
>
> Melalui kontrol Outseal PLC terdapat beberapa fungsi ... counter untuk menghitung jumlah telur yang telah dicuci, timer sebagai penghitung waktu kerja pengering yang di-setting 20 detik ... suhu air di-setting 40 oC.

### 2. 基于原文整理后的自然语言描述

The automatic duck-egg washer is controlled as an Outseal PLC sequence around a conveyor, spray pump, heater, proximity counter, and hairdryer rather than as a single fixed motor loop. The temperature module keeps the wash water at a `40°C` set point: when the sensor reports below-setpoint temperature, the PLC receives a high input and turns the heater on until the set point is reached. During the washing line, a proximity sensor detects cleaned eggs, increments a counter for each egg, and when the configured count is reached the controller activates `R10` to interlock-reset the system temporarily and prevent overload in the collection area. The conveyor motor and pump run from the main power chain, while the drying stage starts when the hairdryer input is triggered and stays on until the PLC timer reaches its configured value. The paper closes the loop by stating that the drying timer is set to `20` seconds, the conveyor can reach `21 RPM`, and the whole machine can process about `33` eggs per minute, so the controller retains thresholds, timed drying, reset behavior, and actuator outputs in one coherent EFSM/T1 chain.

### 3. 逐句溯源

1. 句子 1：The automatic duck-egg washer is controlled as an Outseal PLC sequence around a conveyor, spray pump, heater, proximity counter, and hairdryer rather than as a single fixed motor loop.
   对应摘录：A, B
2. 句子 2：The temperature module keeps the wash water at a `40°C` set point: when the sensor reports below-setpoint temperature, the PLC receives a high input and turns the heater on until the set point is reached.
   对应摘录：B, C
3. 句子 3：During the washing line, a proximity sensor detects cleaned eggs, increments a counter for each egg, and when the configured count is reached the controller activates `R10` to interlock-reset the system temporarily and prevent overload in the collection area.
   对应摘录：B, C
4. 句子 4：The conveyor motor and pump run from the main power chain, while the drying stage starts when the hairdryer input is triggered and stays on until the PLC timer reaches its configured value.
   对应摘录：C
5. 句子 5：The paper closes the loop by stating that the drying timer is set to `20` seconds, the conveyor can reach `21 RPM`, and the whole machine can process about `33` eggs per minute, so the controller retains thresholds, timed drying, reset behavior, and actuator outputs in one coherent EFSM/T1 chain.
   对应摘录：A, C
