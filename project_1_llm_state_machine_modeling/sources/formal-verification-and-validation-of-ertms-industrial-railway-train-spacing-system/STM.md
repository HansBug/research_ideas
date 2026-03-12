# Formal Verification and Validation of ERTMS Industrial Railway Train Spacing System - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文主体偏验证方法，但仍给出了 LDS/RBS 作为实际列车间隔控制子系统的控制对象说明与调度职责。

## 条目 1: RBS-Based Train Spacing Control
- 控制对象：轨道交通领域的 ERTMS 列车间隔控制子系统

### 0. 条目识别与判定
- 一句话说明：这是 ERTMS Level 2 中的 LDS/RBS 控制子系统，用于控制列车移动、轨旁设备、逻辑进路分配以及列车间隔安全。
- 判断：算，但属于控制软件结构级样本。对象是真实铁路控制子系统，不过正文更强调验证流程和软件抽象。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Introduction / system description, 行 96-100
> The application is used to manage and control the train spacing in an ERTMS railway system. ... Our work has focused on Logica di Sicurezza (LDS), a software subsystem that controls train movements and track-side equipment that is connected to track-side units, e.g., track circuits, signals and switches. LDS also implements the logical functions that can be requested by human operators.

#### 摘录 B
- 出处：第 4-5 页，case study description, 行 132-141
> A component is a logical reservation for a segment of line. A point is a logical controller for a switch. ... A radio block section (RBS) corresponds to a logical route through the physical displacement. An RBS is composed of several components and points, and enclosed by an initial and final end-of-authority (EOA).

#### 摘录 C
- 出处：第 5-6 页，verification abstraction, 行 156-162
> The property is “no two different trains occupy the same track”. ... we abstract away non-RBS processes, and use an abstracted scheduler that repeatedly chooses one of the ten RBS’s, depending on a certain condition, starts its process by executing one of its functions, until some exiting condition is met.

### 2. 基于原文整理后的自然语言描述

The LDS subsystem manages train spacing in the ERTMS railway system by controlling train movements and track-side equipment such as track circuits, signals, and switches. Within this controller, a point acts as a logical switch controller and a radio block section corresponds to a logical route composed of reserved components and points. The scheduler repeatedly selects an RBS under certain conditions, executes its control process, and enforces the safety condition that no two different trains occupy the same track.

### 3. 逐句溯源

1. 句子 1：The LDS subsystem manages train spacing in the ERTMS railway system by controlling train movements and track-side equipment such as track circuits, signals, and switches.
   对应摘录：A
2. 句子 2：Within this controller, a point acts as a logical switch controller and a radio block section corresponds to a logical route composed of reserved components and points.
   对应摘录：B
3. 句子 3：The scheduler repeatedly selects an RBS under certain conditions, executes its control process, and enforces the safety condition that no two different trains occupy the same track.
   对应摘录：C
