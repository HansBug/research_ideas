# Model-checking and Model-based Testing of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 行为图和接口执行流程都能直接落成可追溯自然语言。

## 条目 1: BBW ABS behavior TA
- 控制对象：车载 Brake-by-Wire 系统的 ABS 计算逻辑

### 0. 条目识别与判定

- 一句话说明：这是汽车底盘线控制动领域的 ABS 轮端控制逻辑，用于根据车辆速度和车轮滑移情况决定是否释放或保持制动力。
- 判断：算。它描述的是实体车辆中的闭环制动控制行为，不是测试流程或开发过程，而且原文已经把它组织成 TA 行为模型。

### 1. 原文摘录

#### 摘录 A
- 出处：第 50 页，Section 5.1 / Figure 5.1，行 2139-2158
> ure 5.1 depicts such a possible behavior model associated with the pABS FL
> FunctionPrototype, in terms of U PPAAL PORT TA. The behavior of the TA
> model is described as follows. First, the speed of the car (v ) is evaluated:
> if the car has no speed then no brake force is applied (torqueABS == 0 ),
> otherwise the slip rate is evaluated. If the slip rate exceeds 0.2, no brakingforce should be applied to not block the wheel (again torqueABS == 0 ),
> otherwise the desired braking torque wheelABS is sent to the corresponding
> actuator (torqueABS ==wheelABS ). In our TA model, we are evaluating
> sliprate > 0.2asv<5(v−w×R)(based on Equation 2.1).
> Entry
> CalcSlipRateExit
> v>0 [ ]v==0 [torqueABS=0]
> v<5*(v-w*R) [torqueABS=0]
> v>=5*(v-w*R) [torqueABS=wheelABS]
> Figure 5.1: The TA model associated with the pABS FLFunctionPrototype.
> In order to integrate the two models, ICM and the set of TA behaviors, the
> UPPAAL PORT TA tuple introduced in Section 2.3.1 is extended as follows:
> TA/defines/angbracketleftL∪{l⊥},l0,lf,VC,VD,r0,rf,E,I /angbracketright, (5.3)
> where the set of TA locations Lis extended with the idle location l⊥, repre-
> senting the location of the TA that corresponds to FunctionPrototype not being
> active. The initial location is denoted by l0∈Land the ﬁnal location is de-

#### 摘录 B
- 出处：第 54 页，Interface TA 与 Behavior TA 的同步执行，行 2372-2381
> cretely, once the TA has reached the Read location, the edge Read toExec is
> traversed, and the synchronization channel pABS FLbehstart triggers the
> edge from Init toBeh in the corresponding Behavior TA depicted in Figure
> 5.4b. The Behavior TA performs the desired computation of the brake torque
> (based on the slip rate) right away, and moves to the next location. The two TA
> stay in these locations until the clock xhas reached the execution time exec,
> which has the value of 2, at which point the edge Exec toWrite is traversed
> in the Interface TA and the synchronization channel pABS FLbehstop also
> takes the Behavior TA to the Init location. The edge between Write andIdle
> is dedicated to updating any necessary variables. Finally, the TA returns to theIdle location, and remains there until the component is triggered again.

### 2. 基于原文整理后的自然语言描述

The pABS FL behavior first checks whether the car is moving before deciding how the brake torque should be produced. When the car has no speed, no brake force is applied; otherwise slip is evaluated, and the requested wheel torque is only sent to the actuator when the slip condition does not call for wheel-lock prevention. Around this behavior, the interface reads inputs, executes the computation, writes the output, and then remains idle until the function is triggered again.

### 3. 逐句溯源

1. 句子 1：The pABS FL behavior first checks whether the car is moving before deciding how the brake torque should be produced.
   对应摘录：A
2. 句子 2：When the car has no speed, no brake force is applied; otherwise slip is evaluated, and the requested wheel torque is only sent to the actuator when the slip condition does not call for wheel-lock prevention.
   对应摘录：A
3. 句子 3：Around this behavior, the interface reads inputs, executes the computation, writes the output, and then remains idle until the function is triggered again.
   对应摘录：B
