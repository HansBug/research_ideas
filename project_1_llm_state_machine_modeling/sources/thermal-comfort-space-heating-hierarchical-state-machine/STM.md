# Thermal comfort driven space heating control via hierarchical state machine strategy interacting with multiphysics simulation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了储热电暖器的三层 `HSM`，包括 `ON/OFF`、`Mode 1/2/3` 与每个模式内的 `FH/NH` 子状态，并把 `22-23 C` 舒适区和 `60 s` 控制步长写得很清楚。

## 条目 1: Three-Layer Space-Heating HSM with Mode/FH-NH Switching

- 控制对象：储热式电暖器的层次化空间采暖监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向储热式电暖器的三层层次状态机，利用 occupant 周围温度反馈在 `ON/OFF`、`Mode 1/2/3` 和每个模式下的 `fast heating / normal heating` 子状态之间切换。
- 判断：算。对象是实际供暖控制系统，原文明确给出了层次数、状态集、模式名、舒适阈值和每步控制动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，HSM 总体设计，`paper_content.txt` 第 301-334 行
> a three-layer HSM strategy in association with the operating power of the electric heater is proposed
>
> the storage electric heater has three modes of operating power, namely Mode 1 (1 kW), Mode 2 (2 kW) and Mode 3 (3 kW).
>
> two operational states for each mode: fast heating (FH) and normal heating (NH).

#### 摘录 B

- 出处：第 5 页，舒适区与目标，`paper_content.txt` 第 357-362 行
> the HSM aims to maintain the temperature between TS1 and TS2.
>
> In this paper, a case with TS1 and TS2 set to be 22℃ and 23℃, respectively, is studied.

#### 摘录 C

- 出处：第 5 页，状态集合定义，`paper_content.txt` 第 370-403 行
> S11 and S12 denote the ON and OFF states of the first layer state machine
>
> S21, S22, and S23 denote the second layer state machine Mode 1, Mode 2, and Mode 3 states
>
> S31, S32, S33, S34, S35, and S36 denote the FH and NH states of the third layer state machine in different modes of operation

### 2. 基于原文整理后的自然语言描述

The proposed heating controller is a three-layer hierarchical state machine for a storage electric heater whose purpose is to keep the occupant-surrounding temperature inside a neutral-comfort band rather than simply regulating a fixed wall sensor. At the top layer, the supervisor switches the heater `ON` or `OFF`. The second layer selects one of three discrete power modes, namely `Mode 1 (1 kW)`, `Mode 2 (2 kW)`, and `Mode 3 (3 kW)`. Inside each power mode, the third layer further chooses between `fast heating` and `normal heating`, so the complete controller contains six sub-states `FH/NH` distributed across the three power levels. Its transitions are driven by temperature feedback around the occupant, with the control target set to the `22-23 C` comfort interval, and each control step interacts with a multiphysics room model to update the predicted temperature field before the next HSM decision is taken.

### 3. 逐句溯源

1. 句子 1：The proposed heating controller is a three-layer hierarchical state machine for a storage electric heater whose purpose is to keep the occupant-surrounding temperature inside a neutral-comfort band rather than simply regulating a fixed wall sensor.
   对应摘录：A, B
2. 句子 2：At the top layer, the supervisor switches the heater `ON` or `OFF`.
   对应摘录：C
3. 句子 3：The second layer selects one of three discrete power modes, namely `Mode 1 (1 kW)`, `Mode 2 (2 kW)`, and `Mode 3 (3 kW)`.
   对应摘录：A, C
4. 句子 4：Inside each power mode, the third layer further chooses between `fast heating` and `normal heating`, so the complete controller contains six sub-states `FH/NH` distributed across the three power levels.
   对应摘录：A, C
5. 句子 5：Its transitions are driven by temperature feedback around the occupant, with the control target set to the `22-23 C` comfort interval, and each control step interacts with a multiphysics room model to update the predicted temperature field before the next HSM decision is taken.
   对应摘录：A, B
