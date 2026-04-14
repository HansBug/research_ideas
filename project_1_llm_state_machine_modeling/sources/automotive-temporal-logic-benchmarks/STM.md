# Benchmarks for Temporal Logic Requirements for Automotive Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、并行、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：自动变速器示例同时给出了并发状态机、速度阈值 guard、`after(TWAIT,tick)` 和 2.5 秒时序约束。

## 条目 1: Automatic transmission switching logic
- 控制对象：自动变速器控制器
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：并行、显式时钟、连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车动力传动控制领域的自动变速器控制器，用于根据油门、制动负载、车速和当前档位决定换挡与保持时机。
- 判断：算。对象是典型车辆控制系统，原文给出了并发状态机、档位切换 guard、时间等待和明确的反抖时序约束。

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

#### 摘录 B
- 出处：第 2 页，Section 2 Brief description，行 100-115
> Automatic Transmission There are two inputs to the system: the throttle and break. The
> break input enables the user to model variable load to the engine, e.g., going uphill or downhill.
> The physical system has two continuous-time state variables which are also its outputs: the
> speed of the engine !(RPM) and the speed of the vehicle v(mph). Initially, the vehicle is at
> rest at time 0, i.e. the speed v= 0 and engine speed != 0.
> ...
> The model contains 69 blocks among which there are 2 integrators (i.e., 2 continuous state
> variables), 3 look-up tables, 3 2D look-up tables and a Stateflow chart. The Stateflow chart
> (see Fig. 1 for a schematic) contains two concurrently executing Finite State Machines with 4
> and 3 states, respectively.
> ...
> the switching conditions of the Stateflow chart depend on both state variables and input signals
> and are also time dependent.

#### 摘录 C
- 出处：第 4 页，Table 1 中 Automatic Transmission 需求，行 217-231
> AT
> 3There should be no transition from
> gear two to gear one and back to
> gear two in less than 2.5 sec.
> ...
> AT
> 4After shifting into gear one, there
> should be no shift from gear one to
> any other gear within 2.5 sec.
>
> AT
> 5When shifting into any gear, there
> should be no shift from that gear to
> any other gear within 2.5sec.

### 2. 基于原文整理后的自然语言描述

The automatic transmission benchmark takes throttle and brake as inputs and produces the continuous outputs engine speed and vehicle speed together with the discrete gear selection. Its Stateflow chart contains two concurrently executing state machines: `gear_state` with the states `first`, `second`, `third`, and `fourth`, whose entry actions assign `gear = 1..4`, and `selection_state` with `steady_state`, `upshifting`, and `downshifting`. The switching logic uses explicit guards such as `[speed > up_th]`, `[speed < down_th]`, `[speed > down_th]`, and `[speed <= down_th]`, and after `after(TWAIT,tick)` the upshift or downshift transition fires the corresponding `gear_state.UP` or `gear_state.DOWN` action before returning to steady-state evaluation. The temporal requirements AT3-AT5 further constrain the controller so that there is no immediate `gear two -> gear one -> gear two` reversal and, more generally, no shift out of a newly entered gear within the specified 2.5-second window.

### 3. 逐句溯源

1. 句子 1：The automatic transmission benchmark takes throttle and brake as inputs and produces the continuous outputs engine speed and vehicle speed together with the discrete gear selection.
   对应摘录：B
2. 句子 2：Its Stateflow chart contains two concurrently executing state machines: `gear_state` with the states `first`, `second`, `third`, and `fourth`, whose entry actions assign `gear = 1..4`, and `selection_state` with `steady_state`, `upshifting`, and `downshifting`.
   对应摘录：A, B
3. 句子 3：The switching logic uses explicit guards such as `[speed > up_th]`, `[speed < down_th]`, `[speed > down_th]`, and `[speed <= down_th]`, and after `after(TWAIT,tick)` the upshift or downshift transition fires the corresponding `gear_state.UP` or `gear_state.DOWN` action before returning to steady-state evaluation.
   对应摘录：A, B
4. 句子 4：The temporal requirements AT3-AT5 further constrain the controller so that there is no immediate `gear two -> gear one -> gear two` reversal and, more generally, no shift out of a newly entered gear within the specified 2.5-second window.
   对应摘录：C
