# HyTech: A model checker for hybrid systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：恒温器的 on/off 模式、连续演化方程、守卫条件和分析用 clock/stopwatch 都能从原文连续保住。

## 条目 1: Thermostat hybrid automaton
- 控制对象：温控器控制系统
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

The thermostat hybrid automaton starts with temperature x = 2 in the heater-on node, where the temperature rises at rate -x + 5 and must satisfy the invariant 1 < x < 3. When x reaches 3, the turn_off transition is taken, the heater is turned off, and the temperature thereafter falls at rate -x. For the linearized analysis, the nonlinear on-mode rate is overapproximated by the interval [2, 4], a clock y measures elapsed time, a stopwatch z measures the accumulated time spent in node on, and the invariants are strengthened with y <= 60 to check that no state with y = 60 and z > 2y/3 is reachable.

### 3. 逐句溯源

1. 句子 1：The thermostat hybrid automaton starts with temperature x = 2 in the heater-on node, where the temperature rises at rate -x + 5 and must satisfy the invariant 1 < x < 3.
   对应摘录：A
2. 句子 2：When x reaches 3, the turn_off transition is taken, the heater is turned off, and the temperature thereafter falls at rate -x.
   对应摘录：A
3. 句子 3：For the linearized analysis, the nonlinear on-mode rate is overapproximated by the interval [2, 4], a clock y measures elapsed time, a stopwatch z measures the accumulated time spent in node on, and the invariants are strengthened with y <= 60 to check that no state with y = 60 and z > 2y/3 is reachable.
   对应摘录：A, B
