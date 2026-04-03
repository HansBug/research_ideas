# Model-checking and Model-based Testing of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 行为 TA、Interface/Behavior 同步语义以及 10ms/2ms 触发执行参数都能直接落成可追溯自然语言。

## 条目 1: BBW ABS behavior TA
- 控制对象：车载 Brake-by-Wire 系统的 ABS 计算逻辑
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：连续耦合、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G3 BBW/ABS 基准控制链）

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

#### 摘录 C
- 出处：第 30-32 页，BBW use-case timing annotations，行 1187-1209 与 1273-1280
> The Brake-by-Wire Use-case. The Brake-by-Wire (BBW) use-case is a
> braking system equipped with an ABS function, and without any mechanical
> connectors between the brake pedal and the brake actuators.
> The ABS algorithm computes the slip rate based on the
> following equation:
> slipRate =(vehicleSpeed - wheelSpeed * Radius)/vehicleSpeed
> where vehicleSpeed is the speed of the vehicle, wheelSpeed is the speed of the
> wheel, and Radius is the radius of the wheel.
> If slipRate is greater than 0.2 the brake
> actuator is released and no brake is applied, or otherwise the requested brake
> torque is used.
> In Figure 2.1, we present the BBW system model in EAST-ADL, at De-
> sign Level, with annotations for timing properties like triggering period and
> execution time.
> Each of the four ABS FunctionPrototypes are triggered every 10 ms, and their ex-
> ecution takes at most 2 ms according to the associated ExecTime Constraint.

### 2. 基于原文整理后的自然语言描述

The pABS FL FunctionPrototype is a periodic ABS controller in the Brake-by-Wire system: it is triggered every 10 ms, has execution time at most 2 ms, takes RequestedTorqueIn, VehicleSpeedIn, and WheelSpeedIn as inputs, produces ASBrakeTorqueOut, and computes brake torque from slipRate=(vehicleSpeed-wheelSpeed*Radius)/vehicleSpeed. Its Behavior TA has states idle, Entry, CalcSlipRate, and Exit, with variables mapped so that wheelABS holds the requested torque, torqueABS holds the ABS brake torque, and v and w hold the vehicle and wheel speeds. In Entry, guard v==0 takes the automaton directly to Exit with torqueABS=0, while v>0 moves the behavior to CalcSlipRate. In CalcSlipRate, guard v<5*(v-w*R) captures slipRate > 0.2 and assigns torqueABS=0, whereas the complementary guard v>=5*(v-w*R) assigns torqueABS=wheelABS. At the architectural semantics level, the interface is a separate TA with Idle, Read, Exec, and Write, where Read and Write are committed, the edge from Idle to Read updates input variables from the connectors and triggering elements, the 10-unit period allows the function to leave Idle, pABS FLbehstart and pABS FLbehstop synchronize the interface with the Behavior TA, and the component stays in Exec until clock x reaches exec=2 before Write updates the necessary variables and returns the function to Idle.

### 3. 逐句溯源

1. 句子 1：The pABS FL FunctionPrototype is a periodic ABS controller in the Brake-by-Wire system: it is triggered every 10 ms, has execution time at most 2 ms, takes RequestedTorqueIn, VehicleSpeedIn, and WheelSpeedIn as inputs, produces ASBrakeTorqueOut, and computes brake torque from slipRate=(vehicleSpeed-wheelSpeed*Radius)/vehicleSpeed.
   对应摘录：C
2. 句子 2：Its Behavior TA has states idle, Entry, CalcSlipRate, and Exit, with variables mapped so that wheelABS holds the requested torque, torqueABS holds the ABS brake torque, and v and w hold the vehicle and wheel speeds.
   对应摘录：A
3. 句子 3：In Entry, guard v==0 takes the automaton directly to Exit with torqueABS=0, while v>0 moves the behavior to CalcSlipRate.
   对应摘录：A
4. 句子 4：In CalcSlipRate, guard v<5*(v-w*R) captures slipRate > 0.2 and assigns torqueABS=0, whereas the complementary guard v>=5*(v-w*R) assigns torqueABS=wheelABS.
   对应摘录：A
5. 句子 5：At the architectural semantics level, the interface is a separate TA with Idle, Read, Exec, and Write, where Read and Write are committed, the edge from Idle to Read updates input variables from the connectors and triggering elements, the 10-unit period allows the function to leave Idle, pABS FLbehstart and pABS FLbehstop synchronize the interface with the Behavior TA, and the component stays in Exec until clock x reaches exec=2 before Write updates the necessary variables and returns the function to Idle.
   对应摘录：B, C
