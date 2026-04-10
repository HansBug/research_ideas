# Extension and Validation of NEMA-Style Dual-Ring Controller in SUMO - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把美国 NEMA dual-ring 交通灯控制器写成带 phase state、ring/barrier、detector call、min/max green、yellow/red 与 vehicle extension timer 的状态机实现，且用真实走廊参数对 Econolite SIL 控制器做了校验。

## 条目 1: NEMA Dual-Ring Ring-and-Barrier Signal Controller

- 控制对象：NEMA dual-ring 路口信号控制器及其 SUMO 中的状态机实现
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号领域的 NEMA dual-ring controller，用双环、barrier、phase skipping、passage timer 和 offset convention 协调四路口相位切换。
- 判断：算。对象是实际交通信号控制器逻辑，不是泛仿真流程；原文明确说明控制器以 phase 为状态空间，并给出转移条件、定时参数和真实控制器配置。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，Section 2.1
> "rings and barriers"

#### 摘录 B

- 出处：第 4 页，Section 2.1
> "phase skipping is possible"

#### 摘录 C

- 出处：第 5 页，Implementation overview
> "operates as a state machine"

### 2. 基于原文整理后的自然语言描述

The NEMA dual-ring traffic controller represents intersection movements as numbered phases and organizes them into two rings separated by synchronized barriers, so only compatible mainline-side or side-street phase pairs can be served at the same time. In coordinated mode, each phase has minimum and maximum green durations, yellow and red transition times, and a cycle-length reference; non-coordinated phases may end early, and the unused time is returned to the coordinated phases. The controller also supports different offset conventions and leading-left-turn combinations, which means the exact return point to coordinated green depends on controller style rather than a single fixed rule. On the non-coordinated side, if phase skipping is enabled the machine can jump directly from `[2,5]` to `[4,8]` when no detector call is present on phases 3 or 7; otherwise it must serve `[3,7]` for at least the minimum green before crossing the barrier. Vehicle extension timers extend an active phase past minimum green when actuating detectors are hit, but only within the min/max timing envelope. The SUMO implementation states explicitly that the `NEMAController` operates as a state machine whose state space is the numbered phases, and its configuration includes detector lengths, cycle length, ring ordering, barrier phases, coordinated mode, recalls, and per-phase `minDur`, `maxDur`, `vehext`, `yellow`, and `red` parameters. Because the same logic was validated against an Econolite software-in-the-loop controller configured with a real three-intersection corridor, the paper provides both executable control semantics and grounded timing details.

### 3. 逐句溯源

1. 句子 1：The NEMA dual-ring traffic controller represents intersection movements as numbered phases and organizes them into two rings separated by synchronized barriers, so only compatible mainline-side or side-street phase pairs can be served at the same time.
   对应摘录：A；`paper_content.txt` 第 66-99 行。
2. 句子 2：In coordinated mode, each phase has minimum and maximum green durations, yellow and red transition times, and a cycle-length reference; non-coordinated phases may end early, and the unused time is returned to the coordinated phases.
   对应摘录：A；`paper_content.txt` 第 104-115 行。
3. 句子 3：The controller also supports different offset conventions and leading-left-turn combinations, which means the exact return point to coordinated green depends on controller style rather than a single fixed rule.
   对应摘录：A；`paper_content.txt` 第 116-140 行。
4. 句子 4：On the non-coordinated side, if phase skipping is enabled the machine can jump directly from `[2,5]` to `[4,8]` when no detector call is present on phases 3 or 7; otherwise it must serve `[3,7]` for at least the minimum green before crossing the barrier.
   对应摘录：B；`paper_content.txt` 第 141-145 行。
5. 句子 5：Vehicle extension timers extend an active phase past minimum green when actuating detectors are hit, but only within the min/max timing envelope.
   对应摘录：B；`paper_content.txt` 第 146-150 行。
6. 句子 6：The SUMO implementation states explicitly that the `NEMAController` operates as a state machine whose state space is the numbered phases, and its configuration includes detector lengths, cycle length, ring ordering, barrier phases, coordinated mode, recalls, and per-phase `minDur`, `maxDur`, `vehext`, `yellow`, and `red` parameters.
   对应摘录：C；`paper_content.txt` 第 181-205 行。
7. 句子 7：Because the same logic was validated against an Econolite software-in-the-loop controller configured with a real three-intersection corridor, the paper provides both executable control semantics and grounded timing details.
   对应摘录：C；`paper_content.txt` 第 20-27 行，181-205 行。
