# Automatic Fluid Level Control Using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把储液混合罐、操作罐和用户罐的液位联锁写成了 PLC I/O 级控制链，包含干转保护、上下液位阈值、阀门/泵动作与结果步骤，能稳定支撑高质量液位控制样本。

## 条目 1: Three-Tank Fluid Level Pump-and-Valve Controller

- 控制对象：混合罐、操作罐与用户罐组成的三罐液位泵阀控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似（PLC 液位顺序控制簇）

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的三罐液位控制器，PLC 通过 I1-I6 压力开关与 Q1-Q5 泵阀输出维持 reserve tank、operation tank 和 user tank 的液位平衡。
- 判断：算。对象是实际工厂液位控制回路，不是抽象自动化介绍；正文给出了输入输出映射、各储罐上下液位动作、干转保护和结果步骤。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Block diagram，`paper_content.txt` 第 288-292 行
> The low level and high pressure switch level sensors serve as DC inputs to the PLC at input I1, I3, I2, I4, I5 I6 and output that is the motor to fetch the water and solenoid valve to drain the water are connected at out terminals Q1, Q2, Q3, Q4 and Q5 respectively.

#### 摘录 B

- 出处：第 4 页，Section 3.2.2-3.2.4，`paper_content.txt` 第 331-380 行
> In this tanker there is a low level control system which controls the dry run ... The inputs are pressure switch (I1) and pressure switch (I6) ... Q5 and the motor pump Q4 ... The upper sensor (pressure switch I2) controls the over flow of operation tank ... the lower sensor (I5) detects the minimum level of operation tank ... In this tanker we have used upper sensor ... pressure switches (I4) control the over flow of user tank. This senses signal to plc to close (Q3).

#### 摘录 C

- 出处：第 5-6 页，Result & Simulation，`paper_content.txt` 第 402-439 行
> Step 2: When I3 is on the overall system is ready ... Step 3: When I1 ON Q4 and Q5 is ON however motor Q1 is OFF ... Step 4: When I6 is ON Q1 and Q4 are ON but Q5 is OFF ... The inputs are I1, I2, I3, I4, I5, I6 and Q1, Q2, Q3, Q4 Q5 are the outputs.

### 2. 基于原文整理后的自然语言描述

The controller is organized around a main switch and six pressure-switch inputs that supervise three different tanks. When `I3` is on, the PLC enters a ready state and turns on the ready indicator, while the reserve tank uses `I1` and `I6` together with `Q4` and `Q5` to implement dry-run protection and overflow handling: low liquid in the reserve tank stops the pump, whereas the upper reserve sensor closes the corresponding solenoid path. The operation tank is regulated by `I2` and `I5`, with the upper level closing `Q2` and the lower level reopening it so that the intermediate tank is refilled when its level falls below the desired range. The user tank is kept constant by an upper sensor `I4`, which drives the PLC to close `Q3` when the working tank reaches its set level. The result section then enumerates concrete system combinations such as system-off, ready, reserve-low and reserve-full, showing how the pump and valve outputs change as the tank states change.

### 3. 逐句溯源

1. 句子 1：The controller is organized around a main switch and six pressure-switch inputs that supervise three different tanks.
   对应摘录：A；`paper_content.txt` 第 288-292 行。
2. 句子 2：When `I3` is on, the PLC enters a ready state and turns on the ready indicator, while the reserve tank uses `I1` and `I6` together with `Q4` and `Q5` to implement dry-run protection and overflow handling: low liquid in the reserve tank stops the pump, whereas the upper reserve sensor closes the corresponding solenoid path.
   对应摘录：B, C；`paper_content.txt` 第 322-327 行，343-354 行，402-409 行。
3. 句子 3：The operation tank is regulated by `I2` and `I5`, with the upper level closing `Q2` and the lower level reopening it so that the intermediate tank is refilled when its level falls below the desired range.
   对应摘录：B；`paper_content.txt` 第 356-371 行。
4. 句子 4：The user tank is kept constant by an upper sensor `I4`, which drives the PLC to close `Q3` when the working tank reaches its set level.
   对应摘录：B；`paper_content.txt` 第 373-380 行。
5. 句子 5：The result section then enumerates concrete system combinations such as system-off, ready, reserve-low and reserve-full, showing how the pump and valve outputs change as the tank states change.
   对应摘录：C；`paper_content.txt` 第 393-439 行。
