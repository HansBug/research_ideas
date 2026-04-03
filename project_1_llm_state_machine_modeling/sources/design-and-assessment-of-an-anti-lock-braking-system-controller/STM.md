# Design and Assessment of an Anti-lock Braking System Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：ABS 的 wheel-speed sensing、pressure release/rebuild 闭环、slip reference 与 three-position controller 输出都已足够明确，可作为混成控制样本。

## 条目 1: ABS pressure release and re-application logic
- 控制对象：汽车 ABS 制动压力调节控制器
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 B
- 出处：第 7 页，Section 3，对 slip reference 与 bang-bang controller 的说明，行 171-176
> The system reference is set to 0.2, which represents the approximation of the optimum slip
> value for which the maximum coefﬁcient of friction is obtained. The bang-bang regulator was
> utilized as the controller of the system because it is the most used and simplest control solution
> for ABS, and it can be used as a benchmark for comparison with other controllers. This regulator
> reacts to the sliding error ", emulating an ABS controller. It is implemented using a sign block
> which provides the output value as –1 when "<0, 0 when"= 0, and 1 when ">0.

#### 摘录 C
- 出处：第 10-11 页，Section 3，对 three-position controller 与 hydraulic pressure states 的说明，行 279-292
> This paper proposes a performance improvement obtained by using a controller from the
> same category, namely a three-position controller, which provides the output as –1 when "<0,
> 0 when"2[0;0:1], and 1 when ">0:1. The proposed controller is implemented in a subsystem
> block using two relay blocks as seen in Fig. 8, and it replaces the bang-bang controller in the
> simulation block diagram from Fig. 4. This three-position controller considers a dead zone in the
> interval [0, 0.1] providing in this range the value 0 at the output, unlike the bang-bang controller
> where the switching was performed according to the sign in the immediate vicinity of the value
> 0.
> The output is represented by the three-values com-
> mand applied to the hydraulic unit to control the three pressure states: building up pressure,
> maintaining pressure, and reducing pressure in the brake chamber.

### 2. 基于原文整理后的自然语言描述

The ABS uses one speed sensor for each wheel together with a hydraulic unit composed of a return pump and at least two valves per wheel, and the ECU compares wheel speeds to detect when one wheel is rotating slower than the others and tends to lock. When that condition appears, the ECU commands the valves to reduce braking pressure on the affected wheel; after the wheel spins again, pressure is rebuilt by the hydraulic unit, and this release/re-application cycle can occur up to 40 times per second until the driver reduces pedal force or the locking tendency disappears. In the simulation model, the system reference slip is set to 0.2, and the controller output directly determines whether pressure is built up, maintained, or reduced. The proposed three-position controller outputs `-1` when the sliding error is below 0, `0` when the error lies in `[0, 0.1]`, and `1` when the error is above 0.1.

### 3. 逐句溯源

1. 句子 1：The ABS uses one speed sensor for each wheel together with a hydraulic unit composed of a return pump and at least two valves per wheel, and the ECU compares wheel speeds to detect when one wheel is rotating slower than the others and tends to lock.
   对应摘录：A
2. 句子 2：When that condition appears, the ECU commands the valves to reduce braking pressure on the affected wheel; after the wheel spins again, pressure is rebuilt by the hydraulic unit, and this release/re-application cycle can occur up to 40 times per second until the driver reduces pedal force or the locking tendency disappears.
   对应摘录：A
3. 句子 3：In the simulation model, the system reference slip is set to 0.2, and the controller output directly determines whether pressure is built up, maintained, or reduced.
   对应摘录：B, C
4. 句子 4：The proposed three-position controller outputs `-1` when the sliding error is below 0, `0` when the error lies in `[0, 0.1]`, and `1` when the error is above 0.1.
   对应摘录：C
