# Study on the Control of Anti-lock Brake System based on Finite State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把单轮 ABS 的压力调节逻辑直接实现成 `increase / hold / decrease` 三态 Stateflow 图，并给出状态内阀门/泵输出与转移阈值。

## 条目 1: Three-state hydraulic pressure supervisor for a single-wheel ABS

- 控制对象：汽车与道路车辆控制领域的单轮 ABS 液压压力调节控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把轮速差/滑移误差映射为增压、保压、减压三种液压动作的 ABS 状态机控制器。
- 判断：算。对象是实际汽车 ABS 制动控制器，原文不仅说明了速度传感、滑移参考和液压阀/泵执行链，还把控制核心画成显式三态 FSM 并给出状态输出和 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-17 行
> The vehicle braking process and working principle of Anti-lock Brake System (ABS) are analyzed. According to the nonlinear ABS brake model and time-varying characteristics, a more accurate ABS hydraulic numerical model is established. Combined with Matlab software, a single wheel vehicle ABS dynamics model is established. The ABS hydraulic brake control system is realized by using control strategy based on PID control and finite-state machine method.

#### 摘录 B

- 出处：第 4 页，`F. the Finite-State Machine Control`，`paper_content.txt` 第 163-177 行
> The finite-state machine (FSM) is a mathematical model of computation used to design both computer programs and sequential logic circuits. According to the theory of finite-state machine, conditions of one state transition to another state can be designed.
>
> In the process of braking, the brake events of pressure booster, pressure holding, pressure decreasing are switched by used the finite state machine theory. The finite-state machine control flow chart is shown in Figure 6.

#### 摘录 C

- 出处：第 4 页，Figure 6 `Stateflow state of control flow graph`
> `increase`: `en: st=0`; `du: k1=1; k2=0; n=0`
>
> `hold`: `en: st=1`; `du: k1=0; k2=0; n=0`
>
> `decrease`: `en: st=2`; `du: k1=0; k2=1; n=500`
>
> Guards shown in the figure include `[st==0&&slp<=0.01]`, `[st==1&&slp>0.01]`, `[st==1&&slp<-0.01]`, and `[st==2&&slp>=-0.01]`.

#### 摘录 D

- 出处：第 5 页，`The results of simulation analysis`，`paper_content.txt` 第 183-197 行
> Figure 7 is a Simulink simulation model graph of single wheel vehicle ABS. Where, using PID controller to control the deviation between actual slip ratio and reference slip ratio, and then the output decide to the action of solenoid valve through the finite-state machine.
>
> The system has reached the expected value of the optimal slip ratio of 0.2.

### 2. 基于原文整理后的自然语言描述

The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves. The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure. The transition guards split the slip-error space into four bands, moving from `increase` to `hold` when `slp<=0.01`, from `hold` back to `increase` when `slp>0.01`, from `hold` to `decrease` when `slp<-0.01`, and from `decrease` to `hold` when `slp>=-0.01`. This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.

### 3. 逐句溯源

1. 句子 1：The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller.
   对应摘录：A, B, D
2. 句子 2：Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.
   对应摘录：A, D
3. 句子 3：The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.
   对应摘录：B, C
4. 句子 4：The transition guards split the slip-error space into four bands, moving from `increase` to `hold` when `slp<=0.01`, from `hold` back to `increase` when `slp>0.01`, from `hold` to `decrease` when `slp<-0.01`, and from `decrease` to `hold` when `slp>=-0.01`.
   对应摘录：C
5. 句子 5：This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
   对应摘录：A, C, D
