# 面向截瘫患者下肢外骨骼的自主控制方法 / A Method for the Autonomous Control of Lower Limb Exoskeletons for Persons With Paraplegia

## 基本信息

- **标题**：A Method for the Autonomous Control of Lower Limb Exoskeletons for Persons With Paraplegia
- **中文标题**：面向截瘫患者下肢外骨骼的自主控制方法
- **作者**：Hugo A. Quintero，Ryan J. Farris，Michael Goldfarb
- **单位**：
  - Department of Mechanical Engineering, Vanderbilt University
- **发表**：Journal of Medical Devices，2012
- **DOI**：10.1115/1.4007181
- **链接**：https://doi.org/10.1115/1.4007181

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文把下肢外骨骼的 supervisory FSM、12 个状态、CoP 触发阈值以及各状态对应的控制优先级与增益类型写得较完整，足以直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集下载。
- 论文给出了真实 T10 完全性截瘫受试者上的 sit/stand/walk 控制案例，并附带完整状态机和切换条件，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**截瘫患者如何通过上肢/躯干姿态驱动下肢动力外骨骼，自主完成坐下、起立和步行切换**的问题。输入是重心压力中心估计值、额状面倾斜方向、heel strike 后的停顿时长和关节传感器读数，方法是把关节级 `PD`/trajectory controller 置于一个 12 状态事件驱动 FSM 之下，输出是 `sitting -> standing -> double support -> left/right step -> stand/sit` 的完整运动监督控制链。

- **输入**：CoP 估计值 `X_c`、额状面倾斜方向、heel strike 后暂停时长、髋膝关节角度与加速度计姿态信息。
- **方法**：事件驱动 supervisory FSM + joint-level variable-gain `PD` controller + 预定义过渡轨迹。
- **输出**：坐到站、站到坐、站到走、走到站、左右步切换与双支撑停顿判定的整套外骨骼高层控制流程。
- **一句话评价**：这是高质量的 `EFSM + T1` 外骨骼监督控制样本，状态集合、用户触发逻辑和暂停转站立规则都足够完整。

## 控制系统与状态机证据

### 控制对象

论文对象是下肢动力外骨骼的高层自主监督控制器。它负责根据用户上半身姿态和步态事件，决定系统何时从坐姿起立、何时进入双支撑、何时迈左/右步，以及何时从行走恢复到站立或坐姿。

### 状态机组织方式

原文把该控制器明确写成事件驱动 `finite-state machine`。主结构包含 12 个状态：

1. `S1 sitting`
2. `S2 standing`
3. `S3 right-leg-forward double support`
4. `S4 left-leg-forward double support`
5. `S5 sit-to-stand`
6. `S6 stand-to-sit`
7. `S7 stand-to-walk with right half step`
8. `S8 left step`
9. `S9 right step`
10. `S10 walk-to-stand with left half step`
11. `S11 stand-to-walk with left half step`
12. `S12 walk-to-stand with right half step`

### 关键控制链

论文把用户驱动的切换逻辑写得很清楚：

- `S1` 中用户前倾，`CoP` 前移跨过阈值后触发 `S5 sit-to-stand`，再进入 `S2 standing`。
- 在 `S2` 中，用户前倾并向左右一侧 lean，可触发 `S7/S11` 并进入对应半步与双支撑链。
- 在 `S3/S4` 双支撑态中，若 `CoP` 再次越过阈值则继续迈步；若 heel strike 后停顿时间超过阈值，则转入 `S2 standing` 而不是继续行走。
- 用户将 `CoP` 后移到身体后方时，可由 `S2` 进入 `S6 stand-to-sit` 并回到 `S1`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实可穿戴控制系统监督器**，不是单纯康复评估或人体运动学分析。
- 原文直接给出完整状态集合、用户触发规则、阈值变量和步态暂停转站立逻辑，适合提取为高质量自然语言状态机描述。
- 对“用户姿态驱动的 assistive exoskeleton 模式切换”这一类人机协同控制样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `static state + transition state` 的状态组织方式。
- 可以直接借鉴以 `CoP` 阈值和 frontal-plane lean 作为用户触发 guard 的写法。
- 可以直接借鉴“步态暂停时间达到阈值后转入 standing”的工程化局部时间语义。

### 局限性

- 论文更偏外骨骼监督控制，低层关节控制器的动力学细节不是本文重点。
- 触发阈值的精确数值并未像工业 PLC 论文那样全部表成参数表。
- 故障处理链不如工业设备那样丰富，主线集中在正常 sit/stand/walk 切换。

## 文献分类总结

- **文献类型**：真实医疗辅助外骨骼控制案例论文
- **控制对象**：截瘫患者下肢动力外骨骼的高层自主监督控制器
- **状态机画像**：`EFSM + T1`
- **证据强度**：12 状态、用户触发 guard、双支撑暂停转站立与站坐切换都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充可穿戴医疗控制、人机姿态触发 guard 和步态监督控制样本
