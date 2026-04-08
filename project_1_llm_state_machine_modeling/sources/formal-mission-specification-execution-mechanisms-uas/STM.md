# Formal Mission Specification and Execution Mechanisms for Unmanned Aircraft Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把热点侦察任务的 `Mission` 状态细化成并行计数区和扫描区，并明确写出 `scanArea / scanPoint / hold` 的事件触发、跳转与恢复逻辑，足以形成高质量 UAV 任务管理 HSM 样本。

## 条目 1: Hotspot-Analysis Mission Manager

- 控制对象：自主无人机热点侦察任务中的扫描、点检与恢复任务管理器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行控制领域的 mission supervisor，用状态图控制区域扫描、热点计数、点状复查、保持等待以及被中断扫描的恢复。
- 判断：算。对象是实际 UAS 任务管理控制器，原文不是停留在“任务规划框架”层，而是给出了 `Mission` 的分层/并行子状态、触发事件、默认下一 leg、跳转命令与恢复位置更新。

### 1. 原文摘录

#### 摘录 A

- 出处：第 92-93 页，`Mission main states / patternSelect`，`paper_content.txt` 第 3613-3615、3644-3658 行
> UAS can either perform an scan of the area ( scanArea leg), an eight pattern ( scanPoint leg) or a holding pattern ( hold leg) ...
>
> calledpatternSelect . If theresultoftheconditionis 0 scanArea is selected, scanPoint is selectedif its ...
>
> <nextList >scanArea scanPoint hold </nextList >
>
> <leg id=”scanPoint” xsi:type=”fp:ScanPointLeg” >

#### 摘录 B

- 出处：第 94-95 页，`Deferred Hotspot Analysis`，`paper_content.txt` 第 3704-3738 行
> When the Mission state is reached two parallel substates are simultaneously entered: HotSpotsCounter ... and ScanArea ...
>
> eachtimea hotspoteventisdelivered a counter is incremented by one ... we also set the coordinates of the scanPoint leg to the first non-visited potential hotspot and modify the selection condition in patternSelect so that scanPoint is picked.
>
> when entering ScanArea we set the selection condition to 2, meaning that hold is going to be our default leg ...
>
> The scanPoint leg is updated with the coordinates of the first unvisited potential hotspot ... the result of the selection condition in patternSelect is set to 1 to select scanPoint as next leg.

#### 摘录 C

- 出处：第 98-100 页，`Immediate Hotspot Analysis`，`paper_content.txt` 第 3871-3888、3901-3902 行
> The initial state is ScanArea ... on entering ScanArea the selection condition is set to 2 ( hold).
>
> A potential hotspot has been detected ... we expect the system to change its trajectory and perform an eight pattern over the point of interest. After that, the UAS should resume the scan of the area where it was left.
>
> During this transition the MMa does the following:
> 1. Update the scanPoint leg with the coordinates of the potential hotspot ...
> 2. Set the result of the selection condition to 1, i.e. select scanPoint as the next leg.
> 3. Send a command to the FPM to skip the rest of the current scan and directly jump to the scanPoint.
> 4. Update the startAt parameter of the scanArea leg with the position where it has been interrupted ...
>
> the statechart transitions to the corresponding ScanArea state.

### 2. 基于原文整理后的自然语言描述

The UAV hotspot-analysis mission manager is organized as a hierarchical `Mission` state whose flight-pattern selector can choose among `scanArea`, `scanPoint`, and `hold` legs. In the deferred-analysis version, entering `Mission` activates two parallel substates, `HotSpotsCounter` and `ScanArea`, so hotspot detections can update counters and rewrite the `scanPoint` destination while the area-scan branch continues to run. `ScanArea` initially sets `hold` as the default next leg, but each `hotspot` event rewrites the `patternSelect` condition so that `scanPoint` becomes the next leg and the system starts visiting pending hotspots one by one before falling back to `Hold`. In the immediate-analysis version, a `hotspot` event does not wait for the current sweep to finish: it updates the `scanPoint` target, selects that leg as next, sends a skip command to interrupt the current scan, and stores the interrupted `scanArea` position in `startAt` so scanning can later resume from the same place. The resulting controller is therefore a genuine HSM with both hierarchical refinement and parallel mission bookkeeping, not a flat waypoint list.

### 3. 逐句溯源

1. 句子 1：The UAV hotspot-analysis mission manager is organized as a hierarchical `Mission` state whose flight-pattern selector can choose among `scanArea`, `scanPoint`, and `hold` legs.
   对应摘录：A
2. 句子 2：In the deferred-analysis version, entering `Mission` activates two parallel substates, `HotSpotsCounter` and `ScanArea`, so hotspot detections can update counters and rewrite the `scanPoint` destination while the area-scan branch continues to run.
   对应摘录：B
3. 句子 3：`ScanArea` initially sets `hold` as the default next leg, but each `hotspot` event rewrites the `patternSelect` condition so that `scanPoint` becomes the next leg and the system starts visiting pending hotspots one by one before falling back to `Hold`.
   对应摘录：B
4. 句子 4：In the immediate-analysis version, a `hotspot` event does not wait for the current sweep to finish: it updates the `scanPoint` target, selects that leg as next, sends a skip command to interrupt the current scan, and stores the interrupted `scanArea` position in `startAt` so scanning can later resume from the same place.
   对应摘录：C
5. 句子 5：The resulting controller is therefore a genuine HSM with both hierarchical refinement and parallel mission bookkeeping, not a flat waypoint list.
   对应摘录：A, B, C
