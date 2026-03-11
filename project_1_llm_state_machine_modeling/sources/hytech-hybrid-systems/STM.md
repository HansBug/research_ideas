# HyTech: A model checker for hybrid systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：恒温器控制逻辑的原文摘录非常完整。

## 条目 1: Thermostat hybrid automaton
- 控制对象：温控器控制系统

### 0. 条目识别与判定

- 一句话说明：这是温度调节领域的恒温控制系统，用于在温度触及阈值时切换加热器开关并维持温度处于允许范围。
- 判断：算。它是控制理论里的经典控制系统案例，具备清晰的开关模式、守卫条件和连续演化约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Figure 1 与 thermostat automaton 说明，行 66-79
> A simple example. A hybrid automaton is a nondeterministic finite transition graph 
> whose nodes are labeled with differential inclusions. The hybrid automaton to the left 
> in Figure 1 models a simple thermostat. The temperature x is initially 2 degrees, and 
> rising at the rate of -x+5 degrees per minute. When the temperature reaches 3 degrees, 
> the heater is turned off, and the temperature then falls at the rate of -x degrees per 
> minute. While the automaton control resides in a given node, the behavior of the 
> continuous variables satisfies the node's differential inclusions. Nodes are a~o labeled 
> with invariant conditions on the values of the variables. For example, the invariant 
> of the node on is 1 < x < 3, implying that the automaton control must leave the 
> node before the temperature exceeds 3. Transitions between nodes may be guarded 
> by constraints on the variables (e.g. the guard on the transition labeled turn_off is 
> x = 3), and may incorporate reassignment of the variables, such as resetting a clock 
> to 0. Shared event labels allow transitions in one hybrid automaton to be synchronized 
> with transitions in another (this does not occur in the example). 

#### 摘录 B
- 出处：第 2 页，关于时间累计与不变式的继续说明，行 88-97
> For example, in order to analyze the proportion of time that the thermostat is on, 
> we use the linear hybrid automaton to the right in Figure 1, which is derived from the 
> original nonlinear hybrid automaton as follows. First, we overapproximate the nonlinear 
> behavior of the temperature by placing lower and upper bounds on its rate within each 
> node (e.g. in node on, the invariant 1 < x < 3 implies that the rate -x + 5 is bounded 
> within the interval [2, 4]). Next, we introduce a clock y that measures the elapsed time, 
> and a stopwatch z that measures the accumulated time spent in node on. We wish 
> 2 of the first hour of operation. To to check that the thermostat is on for less than 
> ensure termination of the computation, we add the conjunct y _< 60 to the invariants. 
> HYTEctt then fully automatically verifies that no state satisfying y = 60 A z > 2_y is -- 3 

### 2. 基于原文整理后的自然语言描述

The thermostat starts at 2 degrees with the heater on and the temperature rising at the stated rate. When the temperature reaches 3 degrees, the heater is turned off, after which the temperature falls. While heating remains on, the temperature must stay within the invariant 1 < x < 3, and the control must leave that condition before the temperature exceeds 3. The model can also reset clocks on transitions and use extra time variables to measure how long heating remains on.

### 3. 逐句溯源

1. 句子 1：The thermostat starts at 2 degrees with the heater on and the temperature rising at the stated rate.
   对应摘录：A
2. 句子 2：When the temperature reaches 3 degrees, the heater is turned off, after which the temperature falls.
   对应摘录：A
3. 句子 3：While heating remains on, the temperature must stay within the invariant 1 < x < 3, and the control must leave that condition before the temperature exceeds 3.
   对应摘录：A
4. 句子 4：The model can also reset clocks on transitions and use extra time variables to measure how long heating remains on.
   对应摘录：A, B
