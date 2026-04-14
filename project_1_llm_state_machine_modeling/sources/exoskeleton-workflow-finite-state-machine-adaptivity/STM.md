# Adaptation of the support of an industrial exoskeleton based on the workflow – Finite-State-Machine based exoskeleton adaptivity - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把工业手腕外骨骼的支持策略写成“上层工作流状态机 + 下层支持控制器”的分层控制结构，并给出了四个作业状态及其由按钮、RFID、螺钉计数和扭矩阈值驱动的转移条件。

## 条目 1: Workflow-Driven Industrial Exoskeleton Support Supervisor
- 控制对象：面向板件拆装工序的工业手腕外骨骼工作流自适应支持监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业装配流程中的外骨骼上层监督器，用来根据当前工序状态切换手腕自由、屈曲助力、稳定锁止和伸展助力等支持模式。
- 判断：算。对象是实际工业外骨骼的上层控制链，原文给出了分层控制结构、四个工作流状态、各状态对应的支持策略，以及由按钮、RFID、螺钉数量和扭矩事件触发的状态转移。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，摘要，行 12-27
> "superordinate controller" ... "state machine describes the workflow"

#### 摘录 B
- 出处：第 4 页，Section 3.2，行 231-249
> "Zustand 1" ... "Zustand 4"

#### 摘录 C
- 出处：第 5 页，Section 3.2，行 264-274
> "RFID_Check > 0" ... "Anzahl_Moment < 5"

### 2. 基于原文整理后的自然语言描述

The exoskeleton controller is organized hierarchically: a superordinate state machine models the assembly workflow, while a subordinate controller applies the support curve associated with the current workflow state. In the illustrated plate-replacement process, the supervisor starts in a preparation state with free wrist motion, switches to an unscrewing state that supports counter-clockwise flexion, enters a handling state that blocks wrist motion for stabilization while the plate is exchanged, and finishes in a tightening state that supports extension while still allowing flexion. The workflow is initialized by a manual button event and later advances when the screwdriver is detected through RFID, when the counted screw events indicate that the current set is finished, and when the tool is put down or picked up again. Screw progress is inferred from torque events such as exceeding the tightening threshold, so the controller couples workflow knowledge, sensed tool context, and process counters in one explicit supervisory chain. This makes the paper a strong industrial `HSM + T0` sample rather than a generic discussion of adaptive exoskeletons.

### 3. 逐句溯源

1. 句子 1：The exoskeleton controller is organized hierarchically: a superordinate state machine models the assembly workflow, while a subordinate controller applies the support curve associated with the current workflow state.
   对应摘录：A
2. 句子 2：In the illustrated plate-replacement process, the supervisor starts in a preparation state with free wrist motion, switches to an unscrewing state that supports counter-clockwise flexion, enters a handling state that blocks wrist motion for stabilization while the plate is exchanged, and finishes in a tightening state that supports extension while still allowing flexion.
   对应摘录：B
3. 句子 3：The workflow is initialized by a manual button event and later advances when the screwdriver is detected through RFID, when the counted screw events indicate that the current set is finished, and when the tool is put down or picked up again.
   对应摘录：B, C
4. 句子 4：Screw progress is inferred from torque events such as exceeding the tightening threshold, so the controller couples workflow knowledge, sensed tool context, and process counters in one explicit supervisory chain.
   对应摘录：C
5. 句子 5：This makes the paper a strong industrial `HSM + T0` sample rather than a generic discussion of adaptive exoskeletons.
   对应摘录：A, B, C
