# Sistem Tertanam Berbasis PLC pada Simulator Pemberian Label dan Pemisahan Botol - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把输送带上的“检测瓶体 -> 贴标 -> 颜色识别 -> 绿色分流 / 红色直行”控制链写得很完整，含输入输出映射、自动/手动模式和结果表，足以作为工业顺序控制双 A 样本。

## 条目 1: Color-Triggered Labeling and Green-Bottle Diversion Controller

- 控制对象：工业自动化与离散制造领域的瓶体贴标与颜色分流顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC Omron CP1E-E30SDR-A` 的输送带控制器，先用 `photoelectric sensor` 触发贴标气缸，再用 `RGB fiberoptic` 判断瓶色，并用气动 `gate` 把绿色瓶导向侧向包装台。
- 判断：算。对象是论文主系统，原文明确给出传感器、执行器、输入输出地址、自动/手动模式和瓶体在输送线上经历的顺序阶段，不是单纯装置介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Introduction，`paper_content.txt` 第 20-37、158-168 行
> The labeling mechanism is based on the detection of the photoelectric sensor ... the bottle separation process is based on the detection of the fiberoptic sensor for two different colors.
>
> saat botol berwarna merah/hijau terdeteksi oleh photoelectric sensor, maka pneumatic valve untuk pemberian label beroperasi sesuai penyetelan waktu dan setelah proses pemberian label, maka sistem pemisahan botol beroperasi untuk tahapan berbeda.

#### 摘录 B

- 出处：第 4 页，`2.1 Pembatasan Pembahasan`，`paper_content.txt` 第 279-297 行
> setiap botol yang telah terisi dan tertutup secara otomatis, kemudian dideteksi oleh photoelectric sensor untuk diberi stempel berbantuan sistem pneumatik ... setelah proses pemberian stempel terhadap botol selesai, maka pemisah botol beroperasi untuk pemisahan botol berdasarkan warna berbantuan sensor fiber optic.
>
> Botol berwarna merah berjalan hingga ujung konveyor menuju packing table botol merah, dan botol berwarna hijau diarahkan ke samping ... oleh gate.

#### 摘录 C

- 出处：第 8-10 页，`3.2.2` 与 `3.3.1`，`paper_content.txt` 第 558-581、620-661 行
> I0.04 Sensor Fiber Optic "merah", I0.06 Sensor Fiber Optic "hijau", I0.08 Sensor Photoelectric "tutup botol" ... output PLC ... motor dc, solenoid valve perlabelan botol, dan solenoid valve pada mekanisme gate pemisah botol hijau.
>
> simulator dioperasikan dengan dua mode, yaitu manual atau automatic ... saat mode automatic, maka program tertanam di dalam PLC beroperasi ... sensor diproses sesuai program pada PLC untuk dihasilkan keluaran pengontrolan yang sesuai dan tepat.

#### 摘录 D

- 出处：第 10-11 页，`3.3.2` 与 `4. Kesimpulan`，`paper_content.txt` 第 669-705、731-759 行
> untuk proses pemberian label, simulator berhasil secara keseluruhan (100%) ... sedangkan saat pemisahan botol dengan keberhasilan sebesar 73,33%, kesemuanya untuk botol warna hijau.
>
> pembacaan pulse dari sensor photoelectric dan fiberoptic ... berpengaruh pada sistem perlabelan dan pemisahan botol sebagai perintah untuk pengaktifan pneumatic unit.

### 2. 基于原文整理后的自然语言描述

The bottle-processing unit is a PLC-controlled sequential machine that receives already filled and capped bottles on a miniature conveyor and then performs two ordered stages: labeling first and color-based separation second. When a bottle reaches the labeling point, the `photoelectric sensor` triggers the pneumatic labeling actuator for the preset labeling interval, so the conveyor and stamp mechanism jointly complete the marking operation before any diversion occurs. After labeling, the bottle passes the `RGB fiberoptic` sensor, which classifies the bottle as red or green and drives the separation logic: red bottles continue straight to the red packing table, while green bottles activate the pneumatic `gate` and are diverted sideways to the green packing table. The PLC implementation explicitly maps these sensors and actuators onto input/output addresses and supports both `manual` mode, where actuators are triggered directly for maintenance, and `automatic` mode, where the sensor-driven sequence executes under the embedded ladder program. The result table then confirms that labeling succeeds in all trials and that separation behavior is governed by the same sensor-to-actuator chain, with errors concentrated in the green-bottle diversion phase rather than in the existence of the control sequence itself.

### 3. 逐句溯源

1. 句子 1：The bottle-processing unit is a PLC-controlled sequential machine that receives already filled and capped bottles on a miniature conveyor and then performs two ordered stages: labeling first and color-based separation second.
   对应摘录：A, B
2. 句子 2：When a bottle reaches the labeling point, the `photoelectric sensor` triggers the pneumatic labeling actuator for the preset labeling interval, so the conveyor and stamp mechanism jointly complete the marking operation before any diversion occurs.
   对应摘录：A, B
3. 句子 3：After labeling, the bottle passes the `RGB fiberoptic` sensor, which classifies the bottle as red or green and drives the separation logic: red bottles continue straight to the red packing table, while green bottles activate the pneumatic `gate` and are diverted sideways to the green packing table.
   对应摘录：B, C
4. 句子 4：The PLC implementation explicitly maps these sensors and actuators onto input/output addresses and supports both `manual` mode, where actuators are triggered directly for maintenance, and `automatic` mode, where the sensor-driven sequence executes under the embedded ladder program.
   对应摘录：C
5. 句子 5：The result table then confirms that labeling succeeds in all trials and that separation behavior is governed by the same sensor-to-actuator chain, with errors concentrated in the green-bottle diversion phase rather than in the existence of the control sequence itself.
   对应摘录：D
