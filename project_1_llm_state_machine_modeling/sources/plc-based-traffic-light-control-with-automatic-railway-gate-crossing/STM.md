# Plc Based Traffic Light Control With Automatic Railway Gate Crossing - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向列车接近、红绿灯切换、栏杆闭合反馈与电机开闭方向串成了完整的道口控制链，可以直接整理成双 A 的 `EFSM + T0` 样本。

## 备注

- `paper_content.txt` 的 `text` 模式提取存在明显连字噪声；本条目已回到 `paper.pdf` 第 `1-2` 页逐段核对，摘录以 PDF 原文为准。

## 条目 1: Bidirectional Railway-Gate and Road-Signal Cycle
- 控制对象：轨道交通与铁路控制领域的 PLC 道口栏杆与道路信号联动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个以铁路平交道口为对象的 PLC 控制器，通过 `S1-S4` 四个轨旁传感器和门位反馈传感器联动警报、红绿灯与栏杆开闭。
- 判断：算。对象是实际铁路道口门控系统，原文明确给出了双向列车到达顺序、每个传感器对应的动作、栏杆闭合确认与开门条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction（按 `paper.pdf` 核对；对应 `paper_content.txt` 第 10-18 行、第 30-33 行）
> the objective is to atomize the working of the railway gate by using plc (programmable logic controller) based system to operate the gates automatically with help of sensors. ... the train is detected with the help of the sensors mounted at either sides of the gates that provides necessary signals to raise an alarm that provides information of the arrival of the train as well as its direction and then operate the gates.

#### 摘录 B
- 出处：第 2 页，`WORKING`（按 `paper.pdf` 核对；对应 `paper_content.txt` 第 58-67 行）
> First of all train will arrived at sensor S1 and as soon as sensor S1 sense the train then the siren / horn will scramble and red signale glow ... Then train will arrive at sensor S2, and gate start to close until gate close sensor is on. ... When train cross the sensor S3 and then train crosses the sensor S4 then we will open the gate and green signale will glow so that the vehicle will free to pass through gate.

#### 摘录 C
- 出处：第 2、8 页，`WORKING` / `CONCLUSION`（按 `paper.pdf` 核对；对应 `paper_content.txt` 第 68-74 行、第 118-124 行）
> Now the same procedure will happen when train coming from left to right which means first the sensor S4 sense the train ... Then train arrive at sensor S3 then gate will close ... As soon as train passes from sensor S1 the gate will open and green signal will glow till gate open sensor On.
>
> Here we used DC motors to open and near the gates mechanically with the aid of using its rotation in anticlockwise and clockwise instructions respectively. ... PLC sends working sign to the dc motor in line with the output sign of sensors to open / near the railway crossing gate.

### 2. 基于原文整理后的自然语言描述

The PLC railway-crossing controller uses track-side sensors on both sides of the gate to determine train arrival direction, raise alarms, switch the road signal, and drive the barrier motor automatically. For a train moving from right to left, `S1` triggers the siren and red signal, `S2` initiates gate closing until the gate-close sensor confirms the barrier is fully shut, `S3` keeps the gate closed while the train is still near the crossing, and `S4` finally releases the gate and restores the green signal. For the opposite direction, the same logic is mirrored as `S4 -> S3 -> S2 -> S1`, with reopening delayed until the final sensor confirms that the train has fully cleared the crossing. The controller also uses gate-open and gate-close feedback together with clockwise or anticlockwise `DC motor` rotation to realize the physical open-close cycle. This yields a bidirectional EFSM in which sensor events, gate-position feedback, and warning-signal outputs are bound into one recoverable road-rail crossing sequence.

### 3. 逐句溯源

1. 句子 1：The PLC railway-crossing controller uses track-side sensors on both sides of the gate to determine train arrival direction, raise alarms, switch the road signal, and drive the barrier motor automatically.
   对应摘录：A
2. 句子 2：For a train moving from right to left, `S1` triggers the siren and red signal, `S2` initiates gate closing until the gate-close sensor confirms the barrier is fully shut, `S3` keeps the gate closed while the train is still near the crossing, and `S4` finally releases the gate and restores the green signal.
   对应摘录：B
3. 句子 3：For the opposite direction, the same logic is mirrored as `S4 -> S3 -> S2 -> S1`, with reopening delayed until the final sensor confirms that the train has fully cleared the crossing.
   对应摘录：C
4. 句子 4：The controller also uses gate-open and gate-close feedback together with clockwise or anticlockwise `DC motor` rotation to realize the physical open-close cycle.
   对应摘录：C
5. 句子 5：This yields a bidirectional EFSM in which sensor events, gate-position feedback, and warning-signal outputs are bound into one recoverable road-rail crossing sequence.
   对应摘录：A, B, C
