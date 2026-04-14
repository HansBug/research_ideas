# High accuracy traffic light controller for increasing the given green time utilization - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：下一相位的绿灯组合与相位时长生成过程已可追溯到公式和算法步骤；在当前口径下，这条样本已达到主数据集核心保留线，但建模时仍应保留其相位调度器式的计算链。

## 条目 1: Dynamic next-phase selection for a traffic light controller
- 控制对象：动态相位决策交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是路口交通控制领域的 dynamic traffic light controller，用于在每次相位切换时根据实时车道数据计算下一相位的绿灯方向和时长。
- 判断：算，但属于相位调度控制样本。对象是实际交通灯控制器，原文给出了“到切换时刻后生成新 phase plan，再确定绿灯组合和绿灯时长，并在时间到后重触发”的完整链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6-8 页，对 phase plan 与 lane-load calculation 的说明，行 137-188
> When the time came to change the traffic light phase, the traffic light controller would receive the latest collected
> data ... The traffic light phase plan consisted of two main values: the index of the next phase green lights, and the phase time.
> ...
> LT(i,T) ← VC(i,T) * CFVA(i,T) * VC%(i,T) * (LW(i,T) + (LP(i,T) * LD(i,T)) +
> VNQB(i,T)) * (100% – VTNN%(i,T))

#### 摘录 B
- 出处：第 9-10 页，对 SIG graph green-light decision algorithm 的说明，行 193-218
> the next phase, green light determination process, started with initializing the
> neighbor lists of each node.
> ...
> The next step was listing down the
> available full-Mesh element-to-element pairs between the neighbours’ list members of the two currently green adjacent node lists.
> ...
> some undesired combinations ... were eliminated.
> The final step was to choose the two nodes of the combination with the highest weightage to act as the next phase green lights.

#### 摘录 C
- 出处：第 10-14 页，对 next phase time decision 与 retrigger 的说明，行 223-340
> After determining the two green traffic lights for the next phase ... it was the time to calculate for how long they would stay green.
> ...
> GTN1 ← VNR GN1 * Full_Cycle_Time (120 Seconds)
> GTN2 ← VNR GN2 * Full_Cycle_Time (120 Seconds)
> ...
> Next_Phase_Time ← Average (GTN1, GTN2)
> ...
> As soon as the phase time elapsed, the traffic light controller retriggered to make a new phase plan with a new set of collected data.

### 2. 基于原文整理后的自然语言描述

Whenever the current phase is about to change, the traffic light controller receives the latest approach data and produces a new phase plan consisting of two values: the next green-light pair and the next phase time. It first computes a load `LT(i,T)` for each eligible direction from vehicle count, first-arrival confirmation, queue occupancy, waiting time, emergency-priority information, back-road queue size, and downstream occupancy. The controller then maps the intersection to the SIG graph, enumerates candidate full-mesh pairs from the neighbors of the currently green adjacent nodes, eliminates self-pairs, intersecting pairs, and duplicates, and selects the highest-weight pair as the next green directions. For those chosen directions, it filters the relevant competing queues, computes each direction’s queue-length ratio against the corresponding competing total, converts those ratios into portions of the `120`-second full cycle, and sets `Next_Phase_Time` to the average of the two resulting green-time allocations. After the phase plan is sent to the display entities, the controller waits for that phase time to elapse and then retriggers the whole computation on the next data snapshot.

### 3. 逐句溯源

1. 句子 1：Whenever the current phase is about to change, the traffic light controller receives the latest approach data and produces a new phase plan consisting of two values: the next green-light pair and the next phase time.
   对应摘录：A
2. 句子 2：It first computes a load `LT(i,T)` for each eligible direction from vehicle count, first-arrival confirmation, queue occupancy, waiting time, emergency-priority information, back-road queue size, and downstream occupancy.
   对应摘录：A
3. 句子 3：The controller then maps the intersection to the SIG graph, enumerates candidate full-mesh pairs from the neighbors of the currently green adjacent nodes, eliminates self-pairs, intersecting pairs, and duplicates, and selects the highest-weight pair as the next green directions.
   对应摘录：B
4. 句子 4：For those chosen directions, it filters the relevant competing queues, computes each direction’s queue-length ratio against the corresponding competing total, converts those ratios into portions of the `120`-second full cycle, and sets `Next_Phase_Time` to the average of the two resulting green-time allocations.
   对应摘录：C
5. 句子 5：After the phase plan is sent to the display entities, the controller waits for that phase time to elapse and then retriggers the whole computation on the next data snapshot.
   对应摘录：C
