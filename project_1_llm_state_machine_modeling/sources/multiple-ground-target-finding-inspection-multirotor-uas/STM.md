# A Framework for Multiple Ground Target Finding and Inspection Using a Multirotor UAS - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多目标搜索与近距检查主模块直接写成显式 FSM，并补出内部地图、票数阈值、目标确认与误检剔除逻辑，足以形成完整的 UAV 任务监督样本。

## 条目 1: Search-Move-Descend-Inspect Multi-Target Mission Controller

- 控制对象：航空航天与飞行控制领域的多旋翼 UAS 多目标搜索与近距检查任务控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个多旋翼 UAS 在搜索区域内寻找多个地面目标、下探近距检查并在误检时回退的任务级主控制器。
- 判断：算。对象是真实 UAS 高层任务控制器，不是单纯视觉算法；原文明确给出主模块 FSM 的状态集合、比例控制调整、内部地图与投票变量、目标确认与 false positive 剔除规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Figure `1`
> The ability to remotely sense and find a set of targets, and descend and hover close to each target is desirable in many applications, including inspection and search and rescue.
>
> Initially, the UAS searches for ground targets at search height hs(1). If target/s are found, the UAS picks a target ... moves toward the target and descends (2). The UAS then hovers above the target closely ... to inspect the target (3). After inspection, the UAS climbs slightly ... and moves laterally to the next target (4).

#### 摘录 B

- 出处：第 8 页，Section `3.5 Main module`
> A finite state machine (FSM) model is used to implement the main module of the system. Figure 6 shows the finite state machine. The state of the system is controlled by following an OODA loop.
>
> If a target or targets are observed in the search state, the system is updated to the move to target state. In the re-estimate target position state, the UAS moves laterally towards the target and updates the target position. In the descend state, the UAS descends by a predefined amount of height. In the adjust state, the UAS aligns its x,y position above the target by the proportional controller ...

#### 摘录 C

- 出处：第 8 页，Section `3.5 Main module`
> In the climb state, the UAS increases its height by a small amount (<2 m) and transitions into the confirm target state. The confirm target state confirms the availability of the target. If the availability of the target is not confirmed, it will be removed from the internal map, considering it as a false positive. Actions such as inspection or spraying are performed in the action state.

#### 摘录 D

- 出处：第 6-8 页，Section `3.4 Internal map` / Section `3.5 Main module`
> When the UAS descends towards a selected target for an action, other targets go out of the camera FOV. However, the target selected for the action can be visible most of the time. An internal map of the targets is maintained ...
>
> The voting-based scheme is used to reject false positives. ... If there is no target to satisfy the criterion (12), the UAS lands at a predefined position.

### 2. 基于原文整理后的自然语言描述

The UAS main module is an OODA-style finite-state controller that manages the full search-and-inspection mission over multiple ground targets. It starts in `search`, switches to `move to target` when one or more candidates are observed, laterally refines the chosen target in `re-estimate target position`, descends in steps, and uses an `adjust` state with a proportional controller to align the vehicle above the target. After that, the controller climbs slightly, enters `confirm target`, and either removes the candidate from the internal map as a false positive or executes `action` such as inspection or spraying. The internal map stores candidate targets together with distance and vote information, and the voting scheme determines whether a target is valid enough to visit and which nearby target should be served next. When the current action is complete, the machine iterates to the next qualified target; if no target satisfies the selection criterion, the vehicle terminates the mission by landing at a predefined position.

### 3. 逐句溯源

1. 句子 1：The UAS main module is an OODA-style finite-state controller that manages the full search-and-inspection mission over multiple ground targets.
   对应摘录：A, B
2. 句子 2：It starts in `search`, switches to `move to target` when one or more candidates are observed, laterally refines the chosen target in `re-estimate target position`, descends in steps, and uses an `adjust` state with a proportional controller to align the vehicle above the target.
   对应摘录：A, B
3. 句子 3：After that, the controller climbs slightly, enters `confirm target`, and either removes the candidate from the internal map as a false positive or executes `action` such as inspection or spraying.
   对应摘录：C
4. 句子 4：The internal map stores candidate targets together with distance and vote information, and the voting scheme determines whether a target is valid enough to visit and which nearby target should be served next.
   对应摘录：D
5. 句子 5：When the current action is complete, the machine iterates to the next qualified target; if no target satisfies the selection criterion, the vehicle terminates the mission by landing at a predefined position.
   对应摘录：A, C, D
