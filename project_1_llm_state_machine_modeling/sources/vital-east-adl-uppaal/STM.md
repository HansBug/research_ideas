# ViTAL: A Verification Tool for EAST-ADL Models Using UPPAAL PORT - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：可从运行语义和 BBW slip 约束重组成函数行为描述。

## 条目 1: EAST-ADL function execution with BBW ABS rule
- 控制对象：ViTAL 中 EAST-ADL 功能块的执行语义与 BBW ABS 规则

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

### 2. 基于原文整理后的自然语言描述

In ViTAL, each function prototype is driven by periodic triggering information and obeys run-to-completion behavior, so inputs are accessed at the beginning of a trigger and outputs are written only at the end of the computation. The function’s internal behavior is captured by an automaton that reads its input flow ports, computes on the internal data, and then writes the resulting values to the output flow ports. For the Brake-by-Wire control system, one explicit functional rule is that whenever the slip rate exceeds 0.2, the brake actuator is released and no brake is applied.

### 3. 逐句溯源

1. 句子 1：In ViTAL, each function prototype is driven by periodic triggering information and obeys run-to-completion behavior, so inputs are accessed at the beginning of a trigger and outputs are written only at the end of the computation.
   对应摘录：A
2. 句子 2：The function’s internal behavior is captured by an automaton that reads its input flow ports, computes on the internal data, and then writes the resulting values to the output flow ports.
   对应摘录：A
3. 句子 3：For the Brake-by-Wire control system, one explicit functional rule is that whenever the slip rate exceeds 0.2, the brake actuator is released and no brake is applied.
   对应摘录：B
