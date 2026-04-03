# The landing gear system in multi-machine Hybrid Event-B - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：起落架手柄、模拟开关和四个液压 movement machines 之间的切换关系明确且带显式时钟。

## 条目 1: Landing-gear handle and movement-actuation logic
- 控制对象：飞机起落架控制系统
- 状态机类型：HSM（层次状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：层次、并行、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G6 起落架 handle-门-起落架序列）

### 0. 条目识别与判定

- 一句话说明：这是航空机电控制领域的 landing gear control system，用于根据手柄指令在门/起落架执行链之间切换并驱动伸出、收回和锁定相关动作。
- 判断：算。对象是实际飞机起落架控制系统，原文明确给出了 handle up/down、初始锁定状态、模拟开关阶段以及 door/gear movement machines。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，Requirements assumptions，对 handle 与 initial state 的说明，行 591-593
> First, we assume that the pilot controls the gear via a han-
> dlefor which handle UPmeans gear up, and handle DOWN
> means gear down. We also assume that in the initial statethe gear is down and locked.

#### 摘录 B
- 出处：第 11 页，Analogical switch，对 closing/closed/reopening episodes 的说明，行 766-789
> analogical switch is open by default. When a handle event
> occurs, the switch slowly closes (which takes from time 0
> till time CLOSED_INIT ), remains closed for a period (from
> time CLOSED_INIT till time CLOSED_FIN , allowing the
> onward transmission of commands from the computers to
> the general electrovalve), and then slowly opens again (from
> time CLOSED_FIN till time OPEN ).
> If a handle event occurs part way through this process ... during closing, no effect; while closed, the closed
> period is restarted; during reopening, closing is restarted from
> a point proportional to the remainder of the reopening period.
> A clock, clk_AnSw ... controls this activity.
> ...
> Two further events ( AnSw_CLOSED_INIT_reached and
> AnSw_CLOSED_FIN_reached ) mark the transitions
> between episodes: from closing to closed, and from closed
> to reopening.

#### 摘录 C
- 出处：第 13 页，Level 06，对 `DoorsOpen/DoorsClose/GearExtend/GearRetract` machines 的说明，行 949-952
> gives rise to a new machine: DoorsOpen_EV, Doors
> Close_EV, GearExtend_EV, GearRetract_EV. These four
> machines are identical in structure, so only DoorsOpen_EV is written out in full.

### 2. 基于原文整理后的自然语言描述

At the top level, the pilot commands the landing gear with `handle UP` for gear-up and `handle DOWN` for gear-down, and the initial state has the gear down and locked. The analogical switch is open by default; after each handle event it enters a timed closing episode from `0` to `CLOSED_INIT`, stays closed from `CLOSED_INIT` to `CLOSED_FIN` so commands can reach the general electrovalve, and then reopens from `CLOSED_FIN` to `OPEN`. This switch behavior is controlled by clock `clk_AnSw`, and a new handle event is interpreted differently depending on the current phase: it has no effect during closing, restarts the closed period while closed, and restarts closing from a proportional point during reopening; the events `AnSw_CLOSED_INIT_reached` and `AnSw_CLOSED_FIN_reached` mark the phase changes. Below this handle/switch layer, hydraulic actuation is split into four sibling movement machines, `DoorsOpen_EV`, `DoorsClose_EV`, `GearExtend_EV`, and `GearRetract_EV`, which share one structural pattern and organize the door and gear motion logic as coordinated submachines.

### 3. 逐句溯源

1. 句子 1：At the top level, the pilot commands the landing gear with `handle UP` for gear-up and `handle DOWN` for gear-down, and the initial state has the gear down and locked.
   对应摘录：A
2. 句子 2：The analogical switch is open by default; after each handle event it enters a timed closing episode from `0` to `CLOSED_INIT`, stays closed from `CLOSED_INIT` to `CLOSED_FIN` so commands can reach the general electrovalve, and then reopens from `CLOSED_FIN` to `OPEN`.
   对应摘录：B
3. 句子 3：This switch behavior is controlled by clock `clk_AnSw`, and a new handle event is interpreted differently depending on the current phase: it has no effect during closing, restarts the closed period while closed, and restarts closing from a proportional point during reopening; the events `AnSw_CLOSED_INIT_reached` and `AnSw_CLOSED_FIN_reached` mark the phase changes.
   对应摘录：B
4. 句子 4：Below this handle/switch layer, hydraulic actuation is split into four sibling movement machines, `DoorsOpen_EV`, `DoorsClose_EV`, `GearExtend_EV`, and `GearRetract_EV`, which share one structural pattern and organize the door and gear motion logic as coordinated submachines.
   对应摘录：C
