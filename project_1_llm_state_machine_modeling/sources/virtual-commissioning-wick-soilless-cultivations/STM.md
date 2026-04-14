# A Mathematical Model to Enable the Virtual Commissioning Simulation of Wick Soilless Cultivations - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把营养液制备模块 `NSM` 的顺序操作、复合状态和报警分支写成三级层次化 PLC 状态机，正文细节足以支撑双 A 过程控制样本。

## 条目 1: Hierarchical nutrient-solution management supervisor

- 控制对象：过程与环境控制领域的营养液制备模块分层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于 wick soilless cultivation 灵活试验台的 `Nutrient Solution Module (NSM)` 控制软件，用过滤、配方制备、液位/酸碱/电导检测和报警逻辑来准备两条生产线的营养液。
- 判断：算。对象是实际过程控制模块的主控制链，不是单纯虚拟调试方法流程；原文明确写出了顺序填充与配液步骤、`nutrient solution generation` 复合状态、`alarm` 状态，以及 PLC 中 `region/state/substate` 三层实现。

### 1. 原文摘录

#### 摘录 A

- 出处：第 8-9 页，`4.1 Flexible test-bench for wick soilless cultivations`，`paper_content.txt` 第 348-381 行
> The Nutrient Solution Module (NSM) is responsible for preparing nutrient solutions with an established value of pH and EC ... The NSM consists of:
> Filtration Unit: Tap water is collected into the T110 tank ... the filtered water is accumulated into the T120 tank ...
>
> Recipe Preparation Unit: C200 air compressor agitates the fertilizer tanks ... Air is also delivered to the T240 mixing tank for mixing the nutrients during the preparation of the solution. ... Peristatic pumps P210, P220 and P230 delivers acid and nutrients for the control of the pH and EC of the solution. The actual value of the pH and EC is respectively sensed with the Q240 and I240 meters.

#### 摘录 B

- 出处：第 11 页，`Methodology utilized for validating ...`，`paper_content.txt` 第 447-468 行
> The control software was first conceptualized using the state machine diagram ... The state machine diagram of the NSM control software is shown in Fig. 8. A sequential behaviour is implemented by first filling tanks T110 and T120, and then sending the filtered water to the T240 mixing tank for the preparation of the nutrient solution. Since the module must manage two different nutrient solutions, a specific target value of EC and pH is assigned based on the considered sample of plants. Composite states are utilized for states that have common actions and/or transitions. For instance, the C200 air compressor must work throughout all the steps of preparation of the nutrient solution. Therefore, a ‘nutrient solution generation’ composite state is introduced. Apart from the normal functioning behaviour, an ‘alarm’ state is implemented for automatically stopping the system in case of malfunctioning. The alarm transition is triggered either when: the operator presses the ‘alarm’ interrupter on the HMI; the liquid volume within the mixing tank is above a ‘high threshold limit value’; the acid or the concentrated nutrient tanks must be refilled.

#### 摘录 C

- 出处：第 11-12 页，`PLC control software of the NSM`，`paper_content.txt` 第 469-506 行
> the control software was converted into Structured Text PLC code (ST) ... Nested states are generated with additional CASE ... OF constructs ...
>
> The NSM state machine has three hierarchical layers (i.e., composite behaviours) that are implemented with the region, state and substate scalar variables. ... The ‘waiting’ state implements an exit behaviour for selecting the tank ... Whereas the ‘nutrient solution generation’ composite state executes an entry behaviour to set the initial state among its nested substates.
>
> ... ‘on’ and ‘waiting’ LEDs are respectively on when the ‘working’ and ‘waiting’ states are active, while the C200 air compressor when the ‘nutrient solution generation’ state is active.

### 2. 基于原文整理后的自然语言描述

The `NSM` supervisor controls the preparation of nutrient solutions for a wick-soilless cultivation test-bench by coordinating filtration, recipe preparation, and sensor-based alarm handling around the tanks `T110/T120/T240` and the acid and nutrient stocks. Its state-machine design first executes a sequential chain that fills `T110` and `T120` and then sends filtered water to the `T240` mixing tank where pH and EC are corrected for the selected plant line. Because the preparation procedure shares common actions across multiple steps, the software introduces a composite `nutrient solution generation` state that keeps the `C200` air compressor active while the nested substates execute the solution-preparation sequence. In parallel with the nominal working chain, the machine includes an `alarm` branch that stops the module when the operator raises the HMI alarm, when the mixing tank exceeds the high threshold, or when the acid and nutrient stocks need refilling. The PLC implementation preserves this hierarchy explicitly through `region`, `state`, and `substate` variables, so the control logic is a true three-layer `HSM` rather than a flat sequence script.

### 3. 逐句溯源

1. 句子 1：The `NSM` supervisor controls the preparation of nutrient solutions for a wick-soilless cultivation test-bench by coordinating filtration, recipe preparation, and sensor-based alarm handling around the tanks `T110/T120/T240` and the acid and nutrient stocks.
   对应摘录：A, B
2. 句子 2：Its state-machine design first executes a sequential chain that fills `T110` and `T120` and then sends filtered water to the `T240` mixing tank where pH and EC are corrected for the selected plant line.
   对应摘录：A, B
3. 句子 3：Because the preparation procedure shares common actions across multiple steps, the software introduces a composite `nutrient solution generation` state that keeps the `C200` air compressor active while the nested substates execute the solution-preparation sequence.
   对应摘录：A, B, C
4. 句子 4：In parallel with the nominal working chain, the machine includes an `alarm` branch that stops the module when the operator raises the HMI alarm, when the mixing tank exceeds the high threshold, or when the acid and nutrient stocks need refilling.
   对应摘录：B
5. 句子 5：The PLC implementation preserves this hierarchy explicitly through `region`, `state`, and `substate` variables, so the control logic is a true three-layer `HSM` rather than a flat sequence script.
   对应摘录：C
