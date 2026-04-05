# Modeling and simulation of electro-hydraulic telescopic elevator system controlled by programmable logic controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出四层伸缩电梯的状态图、优先策略、上行/下行/减速状态名及 PLC 方程，已经足够整理成完整的离散控制链。

## 条目 1: Priority-Based Four-Floor Telescopic Elevator PLC Controller

- 控制对象：楼宇机电与液压升降设备领域的四层伸缩式液压电梯 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC 控制四层伸缩液压电梯的顺序控制器，负责楼层请求解析、上下行优先选择与到层减速停车。
- 判断：算。对象是实际电梯控制系统，原文不只说“用了状态图”，而是把状态名、优先规则、减速子状态和梯形图实现都写出来了。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Section 3 `Telescopic Elevator Control System Simulator`，`paper_content.txt` 第 168-173 行
> "starts from floor one"

- 证据说明：该段随后说明从一层出发时如何按 `floor 2 -> floor 3 -> floor 4` 的请求优先链上行，以及在二层优先下行、一层三层优先上行等规则。

#### 摘录 B

- 出处：第 4-5 页，Section 4 `Converting the State Diagram into a PLC Ladder Diagram`，`paper_content.txt` 第 229-254 行
> "`U2`, `U3`, `U4`"

- 证据说明：原文把上行、下行与减速状态分别编码为 `U2/U3/U4`、`D1/D2/D3`、`SU2/SU3/SU4`、`SD1/SD2/SD3`，并给出对应的 PLC 逻辑方程。

#### 摘录 C

- 出处：第 6 页，Section 5 `Results and Discussions`，`paper_content.txt` 第 287-292 行
> "decrease the speed to stop"

- 证据说明：这段明确指出轿厢跨越目标楼层的 approach sensor 后会切入减速逻辑，再在目标层停止。

### 2. 基于原文整理后的自然语言描述

The telescopic elevator controller is organized as a PLC-based extended state machine that starts from floor 1 and evaluates pending destination requests with explicit directional priorities. From the state diagram and symbol table, the controller distinguishes full-speed movement states `U2/U3/U4` and `D1/D2/D3` from slowdown states `SU2/SU3/SU4` and `SD1/SD2/SD3`, so the state space includes both travel direction and approach-to-stop submodes. Its transition rules are written as ladder-logic equations rather than left informal, which means the paper explicitly defines when a request to a higher or lower floor is accepted and when competing requests are deferred by priority. During operation, the cabin switches to a slowdown state when it crosses the approach sensor of the selected floor and then stops at the requested level.

### 3. 逐句溯源

1. 句子 1：The telescopic elevator controller is organized as a PLC-based extended state machine that starts from floor 1 and evaluates pending destination requests with explicit directional priorities.
   对应摘录：A
2. 句子 2：From the state diagram and symbol table, the controller distinguishes full-speed movement states `U2/U3/U4` and `D1/D2/D3` from slowdown states `SU2/SU3/SU4` and `SD1/SD2/SD3`, so the state space includes both travel direction and approach-to-stop submodes.
   对应摘录：A, B
3. 句子 3：Its transition rules are written as ladder-logic equations rather than left informal, which means the paper explicitly defines when a request to a higher or lower floor is accepted and when competing requests are deferred by priority.
   对应摘录：A, B
4. 句子 4：During operation, the cabin switches to a slowdown state when it crosses the approach sensor of the selected floor and then stops at the requested level.
   对应摘录：C
