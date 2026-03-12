# Benchmarks for Temporal Logic Requirements for Automotive Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：自动变速器示例既有 gear 逻辑，也有以自然语言写出的时序约束。

## 条目 1: Automatic transmission switching logic
- 控制对象：自动变速器控制器

### 0. 条目识别与判定

- 一句话说明：这是汽车动力传动控制领域的自动变速器控制器，用于根据油门、制动负载、车速和当前档位决定换挡与保持时机。
- 判断：算。对象是典型车辆控制系统，原文给出了并发状态机、档位切换约束和明确的时间窗口要求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Figure 1 左侧 switching logic，行 59-89
> gear_state 1
> fourth
> entry:gear = 4;third
> entry:
> gear = 3;second
> entry:
> gear = 2;first
> entry:
> gear = 1;
> selection_state
> during: CALC_TH ;2
> steady_state
> upshifting downshiftingUP
> 1UP UP
> 1
> DOWN2
> DOWNDOWN2
> [speed > up_th]
> 1[speed < down_th]
> 2
> [speed > down_th]
> 2
> after (TWAIT,tick)
> [speed <= down_th]{gear_state.DOWN }1
> after (TWAIT,tick)
> [speed >= up_th]{gear_state.UP }1[speed < up_th]
> 2
> 0 5 10 15 20 25 30050100Throttle
> 0 5 10 15 20 25 3005000RPM
> 0 5 10 15 20 25 300100200Speed
> Figure 1: Left: The switching logic for the automatic drivetrain; Right: An input signal (top)

#### 摘录 B
- 出处：第 2 页，Section 2 Brief description，行 100-115
> 2 Brief description
> Automatic Transmission There are two inputs to the system: the throttle and break. The
> break input enables the user to model variable load to the engine, e.g., going uphill or downhill.
> The physical system has two continuous-time state variables which are also its outputs: the
> speed of the engine !(RPM) and the speed of the vehicle v(mph). Initially, the vehicle is at
> rest at time 0, i.e. the speed v= 0 and engine speed != 0. Therefore, the output trajectories
> depend only on the input signals utandubwhich model the throttle and break inputs. The
> throttle and break, at each point in time, can take any value between 0 (fully closed) to 100
> (fully open). The range for the break depends on the engine load that we would like to model.
> The system is deterministic, i.e., under the same input u, it will produce the same output y.
> The model contains 69 blocks among which there are 2 integrators (i.e., 2 continuous state
> variables), 3 look-up tables, 3 2D look-up tables and a State
> ow chart. The State
> ow chart
> (see Fig. 1 for a schematic) contains two concurrently executing Finite State Machines with 4
> and 3 states, respectively.

#### 摘录 C
- 出处：第 4 页，Table 1 中 Automatic Transmission 需求，行 217-231
> AT
> 3There should be no transition from
> gear two to gear one and back to
> gear two in less than 2.5 sec.2((g2^Xg1)!2(0;2:5]:g2)
> 
> AT
> 4After shifting into gear one, there
> should be no shift from gear one to
> any other gear within 2.5 sec.2((:g1^Xg1)!2(0;2:5]g1)
> 
> AT
> 5When shifting into any gear, there
> should be no shift from that gear to
> any other gear within 2.5sec.^4
> i=12((:gi^Xgi)!2(0;2:5]gi)

### 2. 基于原文整理后的自然语言描述

The automatic transmission benchmark takes throttle and brake as inputs and produces engine speed, vehicle speed, and transmission gear as outputs. Its Stateflow logic contains two concurrently executing finite state machines, one covering the gear positions from first through fourth and the other coordinating selection, steady running, upshifting, and downshifting. The design is constrained so that rapid reversals or immediate re-shifts after entering a gear are not allowed within the specified 2.5-second windows.

### 3. 逐句溯源

1. 句子 1：The automatic transmission benchmark takes throttle and brake as inputs and produces engine speed, vehicle speed, and transmission gear as outputs.
   对应摘录：B
2. 句子 2：Its Stateflow logic contains two concurrently executing finite state machines, one covering the gear positions from first through fourth and the other coordinating selection, steady running, upshifting, and downshifting.
   对应摘录：A, B
3. 句子 3：The design is constrained so that rapid reversals or immediate re-shifts after entering a gear are not allowed within the specified 2.5-second windows.
   对应摘录：C
