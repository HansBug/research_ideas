# 基于 sEMG 运动意图的机器人膝外骨骼辅助与康复控制 / Control of a Robotic Knee Exoskeleton for Assistance and Rehabilitation Based on Motion Intention from sEMG

## 基本信息

- **标题**：Control of a Robotic Knee Exoskeleton for Assistance and Rehabilitation Based on Motion Intention from sEMG
- **中文标题**：基于 sEMG 运动意图的机器人膝外骨骼辅助与康复控制
- **作者**：Ana Cecilia Villa-Parra，Denis Delisle-Rodriguez，Thomaz Botelho，John Jairo Villarejo Mayor，Alberto Lopez Delis，Ricardo Carelli，Anselmo Frizera Neto，Teodiano Freire Bastos
- **单位**：
  - Postgraduate Program in Electrical Engineering, Federal University of Espirito Santo
  - Biomedical Engineering Research Group, Salesian Polytechnic University
  - Center of Medical Biophysics, University of Oriente
  - Postgraduate Program in Physical Education, Federal University of Parana
  - Institute of Automatics, National University of San Juan
- **发表**：Research on Biomedical Engineering，2018
- **DOI**：10.1590/2446-4740.07417
- **链接**：https://doi.org/10.1590/2446-4740.07417

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文明确给出 `HMIR + FSM + admittance/velocity/trajectory controllers` 的控制栈、6 个 motion class 以及 walking / flexion-extension 的关键参数，足以直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集下载。
- 论文给出了真实主动膝关节外骨骼 `ALLOR` 的控制结构、状态类目、gait sub-phases 与实验流程，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**机器人膝外骨骼如何根据用户的 sEMG 运动意图，在坐下、起立、屈伸和步行之间切换不同控制策略**的问题。输入是 `sEMG` 分类结果、交互力矩、足底压力识别的 gait phase、膝关节角度与速度信息，方法是用 `HMIR` 识别 `SU / SD / F/E / W / RSU / RSD` 六类意图，再由中层 `FSM` 把意图翻译成不同的 `admittance` 与 `velocity` 参数，输出是 `trajectory / velocity / admittance` 三类低层控制器的切换与参数调度。

- **输入**：`sEMG` 特征分类结果、足底压力 gait phase、交互力矩、膝关节位置与速度。
- **方法**：`HMIR` 意图识别 + 中层 `FSM` + `admittance / velocity / trajectory` 控制器组合。
- **输出**：针对 `SU / SD / F/E / W / RSU / RSD` 不同运动类的膝关节助力、锁定、屈伸与步行控制链。
- **一句话评价**：这是高质量的 `EFSM + T1` 医疗辅助控制样本，状态类目、动作输出、gait phase 调制和局部时间参数都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是主动膝关节外骨骼 `ALLOR` 的中高层监督控制器。它负责把用户的运动意图转换成不同的控制模式和参数，并驱动低层控制器完成坐下、起立、屈伸、站立支撑和步行助力。

### 状态机组织方式

原文明确把中层控制写成 `finite state machine`，并围绕六个 motion class 组织：

1. `SU`：Stand-Up
2. `SD`：Sit-Down
3. `F/E`：Knee Flexion-Extension
4. `W`：Walking
5. `RSU`：Rest in Stand-Up Position
6. `RSD`：Rest in Sit-Down Position

同时，论文把这些类再组织成两个顺序组：

1. `G1 = SU -> F/E -> RSD`
2. `G2 = RSU -> W -> SD`

### 关键控制链

论文把不同状态对应的输出动作写得很清楚：

- `W` 状态下，系统根据 `initial contact / mid-stance / terminal stance / swing` 四个 gait sub-phases 调制 admittance gain，并通过 `Δt` 平滑切换不同子相位的参数。
- `RSU` 状态下，系统锁定膝关节以支撑用户体重；`RSD` 状态下，系统提供更易活动的膝关节 admittance。
- `F/E` 状态下，`qmin / qmax` 约束屈伸范围，`downtime / uptime` 决定伸展和屈曲的停留时长，并用基于交互力矩的 `tanh` 增益表达用户想减速、加速或停止的意图。
- `SU / SD` 状态下，系统使用记录轨迹驱动的 `PI trajectory controller` 执行起立和坐下动作。
- 新运动开始前必须完成上一动作，例如 `W` 状态完成条件默认是执行两步，`F/E` 前必须先完成 `SD`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 这是一篇**真实医疗辅助设备控制器**论文，不是临床效果分析或纯连续控制论文。
- 原文直接给出状态类目、组序、低层控制器输出映射、gait sub-phases 和局部时间参数，非常适合提取为自然语言状态机样本。
- 对“人体运动意图驱动 assistive exoskeleton 模式切换”这一类人机协同控制样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `HMIR -> FSM -> low-level controllers` 的三层控制栈写法。
- 可以直接借鉴把 gait phases 映射到不同 admittance 增益的工程化表达。
- 可以直接借鉴 `downtime / uptime / stop-intention` 这种局部时间与交互力矩共同定义 guard 的方式。

### 局限性

- 论文重点在 knee exoskeleton 单关节助力，状态空间不像全下肢外骨骼那样宽。
- `FSM` 图没有像工业设备论文那样把全部转移表格化，需要结合正文段落理解。
- 故障恢复链主要体现在动作完成与安全范围限制，不像工业 PLC 样本那样有大量异常模式。

## 文献分类总结

- **文献类型**：真实医疗辅助外骨骼控制案例论文
- **控制对象**：主动膝关节外骨骼 `ALLOR` 的中高层监督控制器
- **状态机画像**：`EFSM + T1`
- **证据强度**：六类运动状态、输出动作映射、gait phase 参数调制和局部时间语义都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充基于人体运动意图的外骨骼监督控制与 gait-phase aware 样本
