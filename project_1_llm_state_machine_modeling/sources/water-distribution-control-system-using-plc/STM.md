# Water Distribution Control System Using Programmable Logic Controllers (PLC) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Tank 1 / Tank 2` 液位、主泵站减泵逻辑、阀门开闭、`Jockey Pump / Booster Pump` 切换和故障告警都写成了可追溯的配水监督控制链。

## 条目 1: Tank-Level and Booster-Pump Distribution Supervisor

- 控制对象：多水库配水系统的液位、阀门和泵组监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的 water-distribution supervisor，根据 `Tank 1 / Tank 2` 水位、阀门选择、流量等级和泵故障信号，在主泵站与 booster pump station 之间切换配水模式。
- 判断：算。对象是实际供水网络控制系统，原文给出了多阶段液位门限、泵数量变化、阀门打开条件和故障响应，不是抽象的 SCADA 概述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Operation Method / System Components`，`paper_content.txt` 第 44-67 行
> The system will automatically monitor water levels in reservoirs and control the operation of pumps and valves according to consumer demand ...
>
> The system operates pumps based on the water levels within the reservoirs. When the first reservoir reaches its full capacity, the pumps start transferring water to the second reservoir. Subsequently, water distribution is managed through different pipe lines according to consumption rates. The system employs a feedback mechanism to monitor pump performance and detect faults.

#### 摘录 B

- 出处：第 5-7 页，`System Operation`，`paper_content.txt` 第 121-156 行
> Opening the Turnout Valve to fill the first reservoir (Tank 1) ...
>
> After Tank 1 reaches full capacity, the Pump Station is activated. Since the second reservoir (Tank 2) is empty, three out of five pumps operate ...
>
> When the water level in Tank 2 reaches the Low level, one pump is turned off, and two pumps continue operating instead of three ...
>
> When the water level in Tank 2 reaches the High level, one pump is turned off, leaving only a single pump in operation ...
>
> When the water level in Tank 2 reaches the High-High level, all pumps are shut off ...
>
> When the second reservoir (Tank 2) is filled, the first controller (PLC1) sends a signal to enable opening one of the valves 1A or 1B by the third controller (PLC3).

#### 摘录 C

- 出处：第 8-10 页，`Booster pump and fault handling`，`paper_content.txt` 第 165-186 行
> When valve 1A is opened, the Booster Pump system is activated, starting with the Jockey Pump to fill the pipeline ... this pump operates continuously during the valve opening as long as the consumption rate remains low.
>
> When the flow rate reaches a medium level, one of the three booster pumps operates, and the Jockey Pump is shut off ...
>
> When the flow rate exceeds the medium level, two out of the three booster pumps operate ...
>
> In the event of a pump malfunction, indicators on the control panel turn red to signal the faulty pump ...

### 2. 基于原文整理后的自然语言描述

The water-distribution controller first opens the turnout valve to fill `Tank 1`, then starts the main pump station once `Tank 1` is full and `Tank 2` still needs water. While filling `Tank 2`, the supervisor changes the number of active main pumps according to level guards: three pumps when the tank is empty, two pumps at `Low`, one pump at `High`, and zero pumps at `High-High`. After `Tank 2` is filled, `PLC1` enables `PLC3` to open one of the outlet valves, and if `valve 1A` is selected the controller begins a second-stage pressure-management sequence with the `Jockey Pump`, then replaces it by one booster pump at medium flow and by two booster pumps when the flow exceeds the medium threshold. Throughout this process, feedback is used to detect pump faults, and a malfunction raises a red control-panel indication so the failed unit can be identified and handled without losing the overall supervisory structure.

### 3. 逐句溯源

1. 句子 1：The water-distribution controller first opens the turnout valve to fill `Tank 1`, then starts the main pump station once `Tank 1` is full and `Tank 2` still needs water.
   对应摘录：A, B
2. 句子 2：While filling `Tank 2`, the supervisor changes the number of active main pumps according to level guards: three pumps when the tank is empty, two pumps at `Low`, one pump at `High`, and zero pumps at `High-High`.
   对应摘录：B
3. 句子 3：After `Tank 2` is filled, `PLC1` enables `PLC3` to open one of the outlet valves, and if `valve 1A` is selected the controller begins a second-stage pressure-management sequence with the `Jockey Pump`, then replaces it by one booster pump at medium flow and by two booster pumps when the flow exceeds the medium threshold.
   对应摘录：B, C
4. 句子 4：Throughout this process, feedback is used to detect pump faults, and a malfunction raises a red control-panel indication so the failed unit can be identified and handled without losing the overall supervisory structure.
   对应摘录：A, C
