# ViTAL: A Verification Tool for EAST-ADL Models Using UPPAAL PORT - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：正文把周期触发、read-execute-write 节拍、BBW slip 公式与 brake-release 规则都摆了出来，但仍停在功能块级语义。

## 条目 1: EAST-ADL function execution with BBW ABS rule
- 控制对象：ViTAL 中 EAST-ADL 功能块的执行语义与 BBW ABS 规则
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：连续耦合、显式时钟
- 原文细节充实度：🔴 D（摘要/背景级）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🔁 强趋同（G3 BBW/ABS 基准控制链）

### 0. 条目识别与判定

- 一句话说明：这是汽车电子架构分析领域的 Brake-by-Wire 功能原型及其 ABS 控制规则，用于在周期触发下读取输入、执行制动计算并在滑移过大时释放制动。
- 判断：算，但更接近功能块级样本。它描述的仍是实际车辆制动控制功能，而不是开发流程或纯元建模过程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，fp 接口、periodic trigger、run-to-completion 语义，行 303-343
> Each modeling element, except for the FAA ft, has a
> set of ﬂow ports, through which it can interact. Each ﬂow
> port is represented as an input or an output port that has an
> associated type. A ﬂow port is associated with the same type
> of data as the associated variable. Similar to the E AST-ADL
> language itself, connections deﬁne how data can be trans-
> ferred between two fps. We assume no knowledge about the
> time that it takes for the data to be transmitted over a con-
> nection or if data can be lost. This assumption is acceptable
> when modeling the abstract functional system in E AST-ADL
> at analysis level, and therefore most implementation details
> are hidden. Nevertheless, the transmission over a connection,
> the execution, and communication resources are modeled
> in E AST-ADL at design level. Other structural E AST-ADL
> constructs are not represented directly by any modeling
> element, hence they are not inﬂuencing the transformation.
> For the presented integration in ViTAL, the architectural
> information related to structure and timing are partially
> derived from the E AST-ADL model. Every fpis annotated in
> the intermediate model with an event function that submits to
> aperiodic constraint . An event function is a trigger generator
> annotated with a parameter T for period. A new period starts
> every T time units, and the event function generates a trigger
> after each period elapses.
> The E AST-ADL language imposes some restrictions on
> thefpbehavior that should be addressed in the intermediate
> model as well. For example, the run-to-completion semantics
> mentions that input ﬂow ports may only be accessed at
> the beginning of each triggering, and output ﬂow ports
> are only written at the end of the computation. Therefore,
> TA(fp)denotes its behavior augmented with an interface.
> The interface of an fpconsists of ﬂow ports and the
> annotated trigger information. An input ﬂow port has an
> associated variable holding the current data ﬂow. A basic fp
> corresponds to a basic intermediate functional block with an
> automaton that can capture the behavior of the associated ft
> and maybe some other information like execution time. The
> internal computation of an fpstarts with reading all input
> ﬂow ports. These internal input data is used together with
> other functional information during the fpexecution, before
> writing the variables to the output ﬂow ports.

#### 摘录 B
- 出处：第 8 页，Figure 8 / Brake by Wire control system，行 557-564
> Figure 8. Brake by Wire control system
> A[ ](BBW:reaction imply (BBW:clock < 200))
> One of the functional requirements of the system is
> related to the slip rate s. With ViTAL, we can verify
> the following functionality: in case the slip rate variable
> exceeds 0:2, the brake actuator is released and no brake is
> applied:
> A[ ](BTC:s > 0:2imply (ABS:brake = 0))

#### 摘录 C
- 出处：第 7-8 页，Section V / Brake-by-Wire functionality，行 501-544
> The intended functionality of the BBW system is the
> following: when the driver brakes, it uses the pedal, and
> the brake actuators are applying a force that relates with
> the angle of the pressed pedal.
> The system is composed of a Brake Pedal Sensor that reads the pedal position
> percentage used by the Brake Torque Calculator to
> compute the desired Global Torque used by the Global
> Brake Controller to calculate the torque required for
> each wheel.
> The ABS controls the wheel braking in order to prevent
> locking the wheel, based on the slip value. The slip value is
> calculated by the equation:
> s = (v - w * r) / v,
> where v is the vehicle speed, w the wheel speed, and r
> the wheel radius.
> The friction coefficient reaches the peak when s is around 0.2.
> For this reason, if s is greater than 0.2 the brake actuator is released and no brake
> is applied, else the requested brake torque is used.
> The architecture is encapsulated in one FAA ft that contains six
> interconnected fps modeled using the TA editor. Each TA(fp)
> defines the actual functional and timing behavior of the fp.
> The slip rate calculation is controlled by variable slipRate.
> From location calculateSlipRate, based on the current vehicle
> speed vSpeed, the wheel speed wSpeed, and the wheel
> radius wRadius, the TorqueCmd controls the wheel
> braking. Consequently, the ABS enters location BrakeTorque,
> and jumps back to location Start, provided that slipRate is greater than
> 0.2, the brake actuator is released and no brake is applied,
> else the requested brake torque is used.

### 2. 基于原文整理后的自然语言描述

In ViTAL, each basic function prototype is annotated with an event function parameter T that generates a trigger every T time units, and the function obeys run-to-completion semantics: input flow ports may only be accessed at the beginning of a triggering, output flow ports are written only at the end of the computation, and TA(fp) augments the function behavior with an interface made of flow ports and trigger information. Each input flow port has an associated variable holding the current data flow, and the internal computation starts by reading all input flow ports and then uses those internal data together with other functional information before writing the output variables. In the Brake-by-Wire case, one FAA contains six interconnected function prototypes, where the brake pedal sensor and brake torque calculator determine the requested global torque, the global brake controller calculates the torque required for each wheel, and each wheel ABS uses vehicle speed, wheel speed, and wheel radius to compute the slip value s=(v-w*r)/v. Because the tire-road friction peaks when s is around 0.2 and then decreases, the ABS rule releases the brake actuator and applies no brake whenever s>0.2; otherwise it uses the requested brake torque. In the timed-automaton description of this function chain, the slip-based decision is organized around locations such as calculateSlipRate, BrakeTorque, and Start, and ViTAL verifies both the brake-reaction bound A[](BBW:reaction imply (BBW:clock < 200)) and the functional rule A[](BTC:s > 0.2 imply (ABS:brake = 0)).

### 3. 逐句溯源

1. 句子 1：In ViTAL, each basic function prototype is annotated with an event function parameter T that generates a trigger every T time units, and the function obeys run-to-completion semantics: input flow ports may only be accessed at the beginning of a triggering, output flow ports are written only at the end of the computation, and TA(fp) augments the function behavior with an interface made of flow ports and trigger information.
   对应摘录：A
2. 句子 2：Each input flow port has an associated variable holding the current data flow, and the internal computation starts by reading all input flow ports and then uses those internal data together with other functional information before writing the output variables.
   对应摘录：A
3. 句子 3：In the Brake-by-Wire case, one FAA contains six interconnected function prototypes, where the brake pedal sensor and brake torque calculator determine the requested global torque, the global brake controller calculates the torque required for each wheel, and each wheel ABS uses vehicle speed, wheel speed, and wheel radius to compute the slip value s=(v-w*r)/v.
   对应摘录：C
4. 句子 4：Because the tire-road friction peaks when s is around 0.2 and then decreases, the ABS rule releases the brake actuator and applies no brake whenever s>0.2; otherwise it uses the requested brake torque.
   对应摘录：B, C
5. 句子 5：In the timed-automaton description of this function chain, the slip-based decision is organized around locations such as calculateSlipRate, BrakeTorque, and Start, and ViTAL verifies both the brake-reaction bound A[](BBW:reaction imply (BBW:clock < 200)) and the functional rule A[](BTC:s > 0.2 imply (ABS:brake = 0)).
   对应摘录：B, C
