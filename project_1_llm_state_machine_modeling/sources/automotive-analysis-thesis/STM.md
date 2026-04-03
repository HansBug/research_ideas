# Model-driven Analysis and Verification of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 功能块给出了显式 TA 行为，并且可以从正文中重组成自然语言设计描述。

## 条目 1: Brake-by-Wire ABS timed automaton (pABS FL)
- 控制对象：车载 Brake-by-Wire 系统的前左轮 ABS 功能块
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：连续耦合、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G3 BBW/ABS 基准控制链）

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
- 出处：第 81 页，Chapter 5 / abstract test-case witness trace 说明，行 4399-4413
> The U PPAAL PORT model checker automatically generates the witness trace
> presented in Figure 5.9, which represents the execution of the pABS FL Func-
> tionPrototype. Initially, the TA is in location idle and all variables are zero.
> The ﬁrst transition to state Entry is aread transition, where the latest variable
> values of w,wheelABS , and vare read. Since v> 0, the TA moves to the
> CalcSliprate location. On the transition to Exit , thetorqueABS variable is
> 
> --- Page 81 ---
> 58 Chapter 5. Thesis Contributions
> Entry
> CalcSlipRateExit
> v>0 [ ]v==0 [torqueABS=0]
> v<5*(v-w*R) [torqueABS=0]
> v>=5*(v-w*R) [torqueABS=wheelABS]
> Figure 5.5: The TA model associated with the pABS FLFunctionPrototype.

### 2. 基于原文整理后的自然语言描述

The pABS FL FunctionPrototype is modeled with local variables wheelABS, torqueABS, v, w and constant R=1, and its TA behavior contains four locations: idle, Entry, CalcSlipRate, and Exit. The read action moves the function from idle to Entry, where v==0 goes directly to Exit with torqueABS=0, while v>0 takes the automaton to CalcSlipRate. In CalcSlipRate, the guard v>=5*(v-w*R) assigns torqueABS=wheelABS and the complementary guard v<5*(v-w*R) assigns torqueABS=0, matching the no-brake requirement when the wheel-slip condition is detected. The write action returns Exit to idle, and the witness trace shows the concrete execution order idle -> Entry -> CalcSlipRate -> Exit after the latest values of v, w, and wheelABS are read.

### 3. 逐句溯源

1. 句子 1：The pABS FL FunctionPrototype is modeled with local variables wheelABS, torqueABS, v, w and constant R=1, and its TA behavior contains four locations: idle, Entry, CalcSlipRate, and Exit.
   对应摘录：A
2. 句子 2：The read action moves the function from idle to Entry, where v==0 goes directly to Exit with torqueABS=0, while v>0 takes the automaton to CalcSlipRate.
   对应摘录：A, B
3. 句子 3：In CalcSlipRate, the guard v>=5*(v-w*R) assigns torqueABS=wheelABS and the complementary guard v<5*(v-w*R) assigns torqueABS=0, matching the no-brake requirement when the wheel-slip condition is detected.
   对应摘录：A
4. 句子 4：The write action returns Exit to idle, and the witness trace shows the concrete execution order idle -> Entry -> CalcSlipRate -> Exit after the latest values of v, w, and wheelABS are read.
   对应摘录：A, B
