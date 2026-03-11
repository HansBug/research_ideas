# Model-driven Analysis and Verification of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 功能块给出了显式 TA 行为，并且可以从正文中重组成自然语言设计描述。

## 条目 1: Brake-by-Wire ABS timed automaton (pABS FL)
- 控制对象：车载 Brake-by-Wire 系统的前左轮 ABS 功能块

### 0. 条目识别与判定

- 一句话说明：这是汽车底盘电子控制领域的前左轮防抱死制动控制单元，用于在制动过程中根据车轮滑移情况调节该轮的制动力。
- 判断：算。对象是实际车辆制动控制功能，原文给出了可执行的条件分支、输入输出和返回空闲的运行逻辑，明显具有状态机属性。

### 1. 原文摘录

#### 摘录 A
- 出处：第 80-81 页，Chapter 5 / Figure 5.5-5.7，行 4345-4382
> For the pABS FL FunctionPrototype and the associated TA behavior (pre-
> sented in Figure 5.5), the formal model compatible with the input language
> of U PPAAL PORT assumes the following: (i) a mapping between the U PPAAL
> PORT local variables and the E AST-ADL port names (see Figure 5.6) and (ii)
> the behavior of the FunctionPrototype extended with the idle location and the
> read andwrite actions (see Figure 5.7). The idle state (line 2) is also the
> initial state of the system (line 3), and the resulting possible transitions of the
> TA are the read action that is represented by the transition from Idle toEntry
> (line 4), the internal transitions of the TA model (lines 5-15), and the write
> action that is represented by the transition from Exit toIdle (line 16).
> 1<MAPPING xstamodel="pABS_FL.xsta">
> 2<MAP var="wheelABS" port="RequestedTorqueIn"/>
> 3<MAP var="torqueABS" port="ABSBrakeTorqueOut"/>
> 4<MAP var="v" port="VehicleSpeedIn"/>
> 5<MAP var="w" port="WheelSpeedIn"/>
> 6</MAPPING>
> Figure 5.6: Mapping between U PPAAL PORTTA local variables and the E AST-
> ADL ports for the pABS FL.
> Formal veriﬁcation of the E AST-ADL model extended with U PPAAL PORT
> semantics. With U PPAAL PORT, we can symbolically simulate, as well as
> exhaustively check the model to verify if it meets its requirements. For re-
> quirement R1introduced in Section 2.1, the CTL query is as follows:
> A[]ABS.v > 0and ABS.v < 5(ABS.v −ABS.w ×ABS.R )imply WheelActuator.NoBrake
> The veriﬁcation results are presented in more detail in our work [52, 73].5.8 Validation on the Brake-by-Wire Use Case 59
> 1<MODEL type="uppaal:declarations">
> 2 int wheelABS, torqueABS, v, w;
> 3 int R=1;
> 4 </MODEL><MODEL type="uppaal:behaviour">
> 5 state idle, Entry, CalcSlipRate, Exit;
> 6 init idle;
> 7 trans idle->Entry { guard false; },
> 8 Entry->Exit {guard v==0; assign torqueABS=0;},
> 9 Entry->CalcSlipRate {guard v>0;},
> 10 CalcSlipRate->Exit {guard v>=5 *(v-w *R);
> 11 assign torqueABS=wheelABS;},
> 12 CalcSlipRate->Exit {guard v<5 *(v-w *R); assign torqueABS=0;},
> 13 Exit->idle {guard false;};
> 14</MODEL></BEHAVIOUR>

#### 摘录 B
- 出处：第 81 页，Chapter 5 / abstract test-case witness trace 说明，行 4399-4404
> The U PPAAL PORT model checker automatically generates the witness trace
> presented in Figure 5.9, which represents the execution of the pABS FL Func-
> tionPrototype. Initially, the TA is in location idle and all variables are zero.
> The ﬁrst transition to state Entry is aread transition, where the latest variable
> values of w,wheelABS , and vare read. Since v> 0, the TA moves to the
> CalcSliprate location. On the transition to Exit , thetorqueABS variable is

### 2. 基于原文整理后的自然语言描述

When the front-left ABS function is activated, it reads the latest requested torque and speed values and starts its computation from an idle condition. If the vehicle has no speed, it finishes with zero brake torque. If the vehicle is moving, it evaluates slip and either forwards the requested wheel torque or suppresses braking when the no-brake condition for wheel-lock prevention applies. After the result is written out, the function returns to idle and waits for the next activation.

### 3. 逐句溯源

1. 句子 1：When the front-left ABS function is activated, it reads the latest requested torque and speed values and starts its computation from an idle condition.
   对应摘录：A, B
2. 句子 2：If the vehicle has no speed, it finishes with zero brake torque.
   对应摘录：A, B
3. 句子 3：If the vehicle is moving, it evaluates slip and either forwards the requested wheel torque or suppresses braking when the no-brake condition for wheel-lock prevention applies.
   对应摘录：A
4. 句子 4：After the result is written out, the function returns to idle and waits for the next activation.
   对应摘录：A, B
