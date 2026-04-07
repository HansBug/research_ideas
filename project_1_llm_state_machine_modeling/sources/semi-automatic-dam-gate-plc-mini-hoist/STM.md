# Rancang Bangun Sistem Kendali Semi Otomatis Pintu Air Bendungan dengan Mini Hoist PA200 Berbasis PLC Omron CP1E-E20SDR-A - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把水位三级告警、人工确认后的自动升门/降门链、上下限位和手动旁路都写得较细，是过程与环境控制方向比较完整的双 A `EFSM + T0` 样本。

## 条目 1: Semi-Automatic Dam Gate Level Supervisor with Hoist Up/Down Sequencing

- 控制对象：过程与环境控制领域的半自动水闸门 PLC 监督控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由三枚 float switch、tower light、buzzer、mini hoist 和上下限位共同构成的半自动闸门控制器，用于在不同水位等级下提示值守人员执行开门或关门动作。
- 判断：算。对象是真实闸门控制系统，原文给出了三级水位感知、颜色/蜂鸣告警、`AUTO UP / AUTO DOWN` 顺序链、上下限位停机和手动维护分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstrak / Pendahuluan`，`paper_content.txt` 第 20-28 行、第 100-119 行
> "level 1"
>
> "level 2"
>
> "level 3"

摘要和引言已经把系统主线写清楚：三枚 float switch 对应三档水位，红黄绿 tower light 和 buzzer 对应不同告警等级，而 PLC 则控制闸门升降和限位停止。

#### 摘录 B

- 出处：第 8-9 页，`Flowchart Kerja Alat`，`paper_content.txt` 第 547-606 行
> "AUTO UP"
>
> "AUTO DOWN"

工作流程明确说明水位升到 level 3 时由值守人员按 `AUTO UP` 开门，直到上限位触发；当水位降回 level 1 时再按 `AUTO DOWN` 关门，直到下限位触发。

#### 摘录 C

- 出处：第 12-13 页，`Pengujian Black Box Testing 2-10`，`paper_content.txt` 第 774-872 行
> "Float Switch 1"
>
> "Float Switch 2"
>
> "Float Switch 3"

黑盒测试把整条运行链顺序验证了一遍：水位从 level 1 到 level 3 逐级触发不同指示灯，开门后又从 level 3 回落到 level 1，再执行关门动作并由限位开关停止。

#### 摘录 D

- 出处：第 9 页、第 14 页，`Flowchart Kerja Alat / Pengujian Manual`，`paper_content.txt` 第 607-613 行、第 883-905 行
> "Manual Up"
>
> "Manual Down"
>
> "Emergency Switch"

除正常半自动链路外，论文还保留了值守维护场景：`Emergency Switch` 可以总停，`Manual Up` 与 `Manual Down` 则能在不经过 PLC 顺控链的情况下直接驱动 hoist。

### 2. 基于原文整理后的自然语言描述

The dam-gate controller supervises water level through three float switches and does not directly open or close the gate on its own; instead, it escalates the situation into discrete operator-facing levels that then govern the next permitted control action. As the reservoir rises from `level 1` to `level 2` and then to `level 3`, the system switches the tower-light indication from green to yellow to red, and the red state additionally activates the buzzer to request operator intervention. Once the operator confirms the high-water condition and presses `AUTO UP`, the mini hoist opens the gate until the upper limit switch is reached; after the water falls back through `level 2` to `level 1`, the operator presses `AUTO DOWN` and the hoist closes the gate until the lower limit switch is reached. Outside this nominal semi-automatic loop, the same hardware also supports an emergency shutdown branch and direct `Manual Up / Manual Down` maintenance actions, which means the controller combines stateful level supervision with guarded operator-triggered transitions rather than only a single automatic pump-style threshold rule.

### 3. 逐句溯源

1. 句子 1：The dam-gate controller supervises water level through three float switches and does not directly open or close the gate on its own; instead, it escalates the situation into discrete operator-facing levels that then govern the next permitted control action.
   对应摘录：A
2. 句子 2：As the reservoir rises from `level 1` to `level 2` and then to `level 3`, the system switches the tower-light indication from green to yellow to red, and the red state additionally activates the buzzer to request operator intervention.
   对应摘录：A, C
3. 句子 3：Once the operator confirms the high-water condition and presses `AUTO UP`, the mini hoist opens the gate until the upper limit switch is reached; after the water falls back through `level 2` to `level 1`, the operator presses `AUTO DOWN` and the hoist closes the gate until the lower limit switch is reached.
   对应摘录：B, C
4. 句子 4：Outside this nominal semi-automatic loop, the same hardware also supports an emergency shutdown branch and direct `Manual Up / Manual Down` maintenance actions, which means the controller combines stateful level supervision with guarded operator-triggered transitions rather than only a single automatic pump-style threshold rule.
   对应摘录：D
