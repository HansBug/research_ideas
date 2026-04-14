# Functional Model of an Automatic Vehicle Hold Based on an Electro-Hydraulic Braking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `AVH` 的坡度等级判定、驻车保压、起步释放和防溜车逻辑写成了完整功能模型，包含压力阈值、级别迁移和阶段式释放链，可稳定形成双 A 车控样本。

## 条目 1: Slope-aware automatic vehicle hold and release supervisor

- 控制对象：车载控制与驾驶辅助领域的 `AVH` 电液制动监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个利用坡度传感、液压目标等级和驾驶员起步意图来控制驻车保压与释放的 `AVH` 功能监督器。
- 判断：算。对象是真实电液制动系统的软件功能模块，原文给出压力等级状态、驻车请求/保压/释放链、内部时间阈值以及起步三阶段策略，而不是只有 Simulink 外框图。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5-6 页，`2.4 Calculation Module`，`paper_content.txt` 第 167-182 行
> The hydraulic pressure level is pre-set to four levels, the gradient level to three ... when Vehgrd is greater than GrdLv1 ... it will enter the Lv2 frame ... If it is still greater than then it will enter the Lv3 frame; similarly, it will enter the Lv4 frame ... Hydraulic pressure will be a more considerable fluid pressure at the pressure level PTarLv4 ...

#### 摘录 B

- 出处：第 6-7 页，`2.5 Parking Function Unit Module`，`paper_content.txt` 第 195-225 行
> the vehicle is already in the state of requesting parking ... the AVH function can meet the state of pressure preservation.
>
> When the difference between the calculated output hydraulic pressure and the actual hydraulic pressure is greater than 5 bar, the AVH function will re-calculate the hydraulic pressure demand. When it exceeds the internal time threshold of the system, it will use the maximum hydraulic pressure value ...
>
> When the pressure switching flag bit signals switching ... the AVH function will enter the release mode ... when the absolute value of the difference ... is confirmed to be smaller than 3 bar ... the status of the AVH function is release complete.

#### 摘录 C

- 出处：第 10 页，Figure 7 `automatic vehicle hold strategy`，`paper_content.txt` 第 320-333 行
> Stage 1: ... if it is on a ramp, the EHB will calculate the amount of brake fluid pressure needed in the current state to prevent the vehicle from skidding when parking and starting; if it is on a flat surface, the fluid pressure will be maintained at a pre-set lower level ... and gradually released to 0 ...
>
> Stage 2: When the driver has the intention to start ... the EHB reduces the maintained hydraulic pressure according to the output of the motor ...
>
> Stage 3: If the motor output torque is not enough to start the vehicle, the EHB still provides brake fluid pressure ... until the motor output torque is greater than the resisting torque ... and the hydraulic control fluid pressure reduces to 0 ...

### 2. 基于原文整理后的自然语言描述

The AVH software works as a slope-aware brake-pressure supervisor rather than as a single hold/release flag. First, the calculation module classifies the road gradient into three threshold bands and chooses one of four hydraulic target levels `PTarLv1` to `PTarLv4`, moving up or down between frames as the measured slope crosses the configured level boundaries. Once the AVH is enabled and ready, the parking function enters a `request parking` state and then a `pressure preservation` state in which the target hold pressure is selected either from the brake pedal or from the AVH calculation result. If the commanded and measured hydraulic pressures differ by more than `5 bar`, the controller recomputes the demand, and after the internal time threshold is exceeded it escalates to the maximum hydraulic pressure to prevent rollback. When the driver signals a start request, the function enters `release mode`, gradually decreases hydraulic pressure, and marks the release as complete once the target-pressure mismatch falls below `3 bar`. The high-level strategy then keeps comparing motor torque against ramp resistance so that pressure is only reduced to zero after the powertrain can safely overcome downhill motion.

### 3. 逐句溯源

1. 句子 1：The AVH software works as a slope-aware brake-pressure supervisor rather than as a single hold/release flag.
   对应摘录：A, C
2. 句子 2：First, the calculation module classifies the road gradient into three threshold bands and chooses one of four hydraulic target levels `PTarLv1` to `PTarLv4`, moving up or down between frames as the measured slope crosses the configured level boundaries.
   对应摘录：A
3. 句子 3：Once the AVH is enabled and ready, the parking function enters a `request parking` state and then a `pressure preservation` state in which the target hold pressure is selected either from the brake pedal or from the AVH calculation result.
   对应摘录：B
4. 句子 4：If the commanded and measured hydraulic pressures differ by more than `5 bar`, the controller recomputes the demand, and after the internal time threshold is exceeded it escalates to the maximum hydraulic pressure to prevent rollback.
   对应摘录：B
5. 句子 5：When the driver signals a start request, the function enters `release mode`, gradually decreases hydraulic pressure, and marks the release as complete once the target-pressure mismatch falls below `3 bar`.
   对应摘录：B
6. 句子 6：The high-level strategy then keeps comparing motor torque against ramp resistance so that pressure is only reduced to zero after the powertrain can safely overcome downhill motion.
   对应摘录：C
