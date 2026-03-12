# Design and Assessment of an Anti-lock Braking System Controller - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：ABS 的检测-减压-再增压闭环很清楚，但表达更偏控制机理而非显式状态机。

## 条目 1: ABS pressure release and re-application logic
- 控制对象：汽车 ABS 制动压力调节控制器

### 0. 条目识别与判定

- 一句话说明：这是汽车底盘控制领域的 anti-lock braking controller，用于在车轮出现抱死趋势时调节单轮制动压力并维持车辆可转向性。
- 判断：算，但属于控制机理型样本。对象是实际 ABS 控制器，原文给出了锁止趋势检测、减压、恢复增压和循环执行的逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 1，对 ABS ECU / valves / pump 动作的描述，行 60-68
> wheel, and a hydraulic unit comprising of a return pump and at least two valves that control the
> braking pressure on each wheel. The sensors measure and transmit the speed of each wheel to
> the ECU. If the electronic control unit detects that one of the wheels is spinning slower than the
> others, condition which can cause a locking state, it will generate a command to the valves to
> lower the pressure in the braking circuit and to reduce the braking force on that respective wheel.
> The system must also be able to supply pressure by means of the electric pump from within its
> composition. After the wheel spins again, the brake pressure on the wheel increases once more.
> This increase and release of the pressure is performed up to 40 times per second and continues
> until the driver reduces the force applied to the braking pedal or until the locking tendency is

### 2. 基于原文整理后的自然语言描述

The ABS controller monitors wheel speeds and detects when one wheel is rotating slower than the others with a tendency to lock. When that tendency is detected, the electronic control unit commands the valves to lower the braking pressure on that wheel, and after the wheel spins again the brake pressure increases once more. This pressure release and re-application continues until the driver reduces the brake demand or the locking tendency disappears.

### 3. 逐句溯源

1. 句子 1：The ABS controller monitors wheel speeds and detects when one wheel is rotating slower than the others with a tendency to lock.
   对应摘录：A
2. 句子 2：When that tendency is detected, the electronic control unit commands the valves to lower the braking pressure on that wheel, and after the wheel spins again the brake pressure increases once more.
   对应摘录：A
3. 句子 3：This pressure release and re-application continues until the driver reduces the brake demand or the locking tendency disappears.
   对应摘录：A
