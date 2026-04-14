# Enhanced Intelligent Energy Management System for a Renewable Energy-Based AC Microgrid - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 AC 微电网的 `Mode1 / Mode2` 运行方式、十个电池状态和超级电容补偿规则直接组合成两层 EEMS，原文足以恢复完整的功率分配监督链。

## 条目 1: Two-mode battery-supercapacitor EEMS supervisor

- 控制对象：过程与环境控制领域的 AC 微电网混合储能能量管理监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向住宅 AC 微电网的 hybrid EMS，通过 `Mode1 / Mode2` 外层运行方式和十个内层状态协同分配 `PV / battery / supercapacitor / grid` 之间的功率。
- 判断：算。对象是实际微电网能量管理控制器，原文不仅写出状态机，还给出了各状态对应的 `SoC / PL / PPV / PBT / PG / PSC` 条件与输出功率规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 18-34 行
> The proposed EEMS is a hybrid control strategy, which is composed of two stages: a state machine (SM) control to ensure the optimal operation of the battery, and an operating mode (OM) for the best operation of the SC.

#### 摘录 B

- 出处：第 7-8 页，`4.2 The Enhanced Energy Management Strategy (EEMS)` 与 Figure 7，`paper_content.txt` 第 303-321 行与第 325-355 行
> To achieve this, the control strategy proposed in this work acts to provide a continuous load supply under various conditions according to hybrid energy management with a state machine and an operating mode strategy.
>
> State 1: If SoC BT = SoC BT_max && PL < PPV ... State 2: If SoC BT_min ≤ SoC BT < SoC BT_max && PL < PPV ... State 3: If SoC BT_min ≤ SoC BT ≤ SoC BT_max && PL > PPV ... State 4: If SoC BT < SoC BT_min && PL < PPV ... State 5: If SoC BT < SoC BT_min && PL > PPV ...
>
> Mode 2 ... State 6 ... State 7 ... State 8 ... State 9 ... State 10 ...

#### 摘录 C

- 出处：第 8-9 页，对 `Mode1 / Mode2` 与 SC control 的说明，`paper_content.txt` 第 356-389 行
> Mode1: |PL−PPV| ≤ PBT_Max
>
> State 1: if PPV is greater than PL, then the battery floats and the PV power is limted to load one.
>
> State 5: During the battery minimum state of charge, if PL is greater than PPV, the battery floats ... the grid ensures the difference in power between load and PV.
>
> Mode2: |PL−PPV| > PBT_max
>
> State 8: During the battery effective state of charge, if PL is greater than PPV, the battery ensures the difference in power between load and PV; then, the output battery power is PBT = PBT_Max and PG = PL − PPV − PBT_Max.
>
> If PL is greater than PBP and SoC SC is not at its maximum, the SC charges and recovers all of the power loss. If PL is less than PBP and SoC SC is not at its minimum, the SC discharges and supplies all of the needed power to the load. If PL is equal to PBP, the SC floats.

### 2. 基于原文整理后的自然语言描述

The proposed EEMS is organized as a two-layer supervisory controller rather than as a flat list of microgrid modes. At the outer layer, an operating-mode test compares `|PL - PPV|` with `PBT_max` to choose `Mode1` when the battery can absorb or supply the mismatch directly, or `Mode2` when the mismatch exceeds the battery limit. Inside those two outer modes, the battery state machine selects among ten explicit states according to `SoC_BT`, the relative values of `PL` and `PPV`, and whether the battery should float, charge, discharge, or hand the deficit to the grid. In the low-mismatch branch, the controller lets PV alone feed the load, lets the battery absorb or supply `PL - PPV` while `SoC_BT` stays in range, or moves the deficit to the grid when the battery is below the minimum charge threshold. In the high-mismatch branch, the battery output saturates at `±PBT_max`, PV is clipped or extended accordingly, and the remaining deficit is exported to `PG`. A third SC control rule then compares `PL` with `PBP = PPV + PBT` and the supercapacitor charge bounds to decide whether the supercapacitor charges, discharges, or floats, so the complete design is a hierarchical, continuous-variable-coupled EMS for an AC microgrid.

### 3. 逐句溯源

1. 句子 1：The proposed EEMS is organized as a two-layer supervisory controller rather than as a flat list of microgrid modes.
   对应摘录：A, B
2. 句子 2：At the outer layer, an operating-mode test compares `|PL - PPV|` with `PBT_max` to choose `Mode1` when the battery can absorb or supply the mismatch directly, or `Mode2` when the mismatch exceeds the battery limit.
   对应摘录：B, C
3. 句子 3：Inside those two outer modes, the battery state machine selects among ten explicit states according to `SoC_BT`, the relative values of `PL` and `PPV`, and whether the battery should float, charge, discharge, or hand the deficit to the grid.
   对应摘录：B, C
4. 句子 4：In the low-mismatch branch, the controller lets PV alone feed the load, lets the battery absorb or supply `PL - PPV` while `SoC_BT` stays in range, or moves the deficit to the grid when the battery is below the minimum charge threshold.
   对应摘录：C
5. 句子 5：In the high-mismatch branch, the battery output saturates at `±PBT_max`, PV is clipped or extended accordingly, and the remaining deficit is exported to `PG`.
   对应摘录：C
6. 句子 6：A third SC control rule then compares `PL` with `PBP = PPV + PBT` and the supercapacitor charge bounds to decide whether the supercapacitor charges, discharges, or floats, so the complete design is a hierarchical, continuous-variable-coupled EMS for an AC microgrid.
   对应摘录：A, C
