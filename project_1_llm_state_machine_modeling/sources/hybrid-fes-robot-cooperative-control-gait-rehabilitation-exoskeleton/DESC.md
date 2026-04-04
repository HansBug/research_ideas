# 步行康复外骨骼的混合 FES-机器人协同控制 / Hybrid FES-Robot Cooperative Control of Ambulatory Gait Rehabilitation Exoskeleton

## 基本信息

- **标题**：Hybrid FES-Robot Cooperative Control of Ambulatory Gait Rehabilitation Exoskeleton
- **中文标题**：步行康复外骨骼的混合 FES-机器人协同控制
- **作者**：Antonio J. del-Ama，Angel Gil-Agudo，Jose L. Pons，Juan C. Moreno
- **单位**：
  - Biomechanics and Technical Aids Unit, National Hospital for Spinal Cord Injury, SESCAM
  - Bioengineering Group, Spanish National Research Council
- **发表**：Journal of NeuroEngineering and Rehabilitation，2014
- **DOI**：10.1186/1743-0003-11-27
- **链接**：https://doi.org/10.1186/1743-0003-11-27

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文明确写出 `joint controller + FES controller + MFE + FSM` 的高层协同结构、`t-FSM / c-FSM` 双层组织、`PID / ILC` 分工和 fatigue management 逻辑，足以直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集。
- 论文给出了混合步行康复外骨骼 `Kinesis` 的 gait assistance 控制链、两层状态机和健康受试者实验，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**混合外骨骼如何在步行中平衡机器人助力和电刺激肌肉驱动，并在肌肉疲劳时重新调整行为**的问题。输入是 gait event、interaction torque、swing trajectory、刺激输出积分和 fatigue estimator，方法是把 `robotic joint controller`、`FES controller`、`muscle fatigue estimator` 和双层 `FSM` 组织成协同控制架构，输出是 stance / swing 阶段下的机器人刚度调节、FES 脉宽控制、学习与监测状态切换以及疲劳后的重学习。

- **输入**：gait event、interaction torque、joint trajectory、`TTI`、stimulation pulse width 与 fatigue 指标。
- **方法**：`t-FSM + c-FSM` 双层协调 + stance `PID` + swing `ILC` + `MFE` 疲劳检测。
- **输出**：步态事件驱动的机器人刚度与 FES 协同分配、learning / monitoring 状态切换和安全回退。
- **一句话评价**：这是高质量的 `HSM + T1` 外骨骼控制样本，层次结构、阶段控制、疲劳管理和安全回退都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是混合 `FES + robot` 步行康复外骨骼 `Kinesis` 的高层协同控制器。它负责在 stance / swing 中协调机器人和刺激肌群的贡献，并在疲劳出现时调整行为。

### 状态机组织方式

原文把控制器明确组织成双层状态机：

1. 顶层 `t-FSM`：time-domain gait FSM，负责根据传感器检测 gait events，管理 stance / swing 相关状态。
2. 子层 `c-FSM`：cycle-domain FSM，在 swing 内部运行，每条腿各一个，包含 `learning` 与 `monitoring` 两个状态。

### 关键控制链

论文把控制分工和状态逻辑写得很完整：

- `t-FSM` 从传感器中检测 gait events，并在腿进入 swing 时向对应腿的 `c-FSM` 广播 `new step event`。
- 在 stance / double support，系统用 `PID` 控制 extensor muscles，以 interaction torque 为反馈避免 knee collapse。
- 在 swing，相对于时间定义的参考轨迹，系统用 `ILC` 周期性更新刺激脉宽向量，以减小 interaction torque。
- `c-FSM` 先进入 `learning`，当 `NILC` 梯度低于 `5%` 后转入 `monitoring`；此后系统重复已学得的刺激模式，同时根据 `TTI` 监测肌肉疲劳并逐周期降低机器人刚度，但仍保持至少 `60 deg` 的 knee flexion 目标。
- 一旦疲劳被检测到，系统改变刺激参数并重新进入新的学习周期；若 joint position 超限，状态机会锁住电机并把膝关节带回默认安全位置。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 这是**真实混合医疗辅助控制系统**，不是 FES 综述或单纯人体动力学建模。
- 原文同时提供层次状态机、阶段性控制目标、学习条件、疲劳阈值和安全回退，适合直接提取为高质量自然语言状态机描述。
- 对“带学习期和监测期的 gait rehabilitation supervisor”这一类样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `t-FSM` 协调 `c-FSM` 的层次化写法。
- 可以直接借鉴把 stance 和 swing 分别交给 `PID` 与 `ILC` 的控制职责分配方式。
- 可以直接借鉴以 `TTI` 变化率和 `5% / 19%` 规则定义学习切换与疲劳管理的工程表达。

### 局限性

- 论文大量篇幅用于 FES 与疲劳估计的控制机理，阅读时需要和状态机主链拆开。
- 图中的部分状态名依赖图示理解，正文更偏解释控制职责而不是列出完整转移表。
- 目标对象是单关节康复外骨骼，不是全设备级多子系统 supervisor。

## 文献分类总结

- **文献类型**：真实医疗康复外骨骼控制案例论文
- **控制对象**：混合 `FES + robot` 步行康复外骨骼 `Kinesis` 的高层协同控制器
- **状态机画像**：`HSM + T1`
- **证据强度**：双层状态机、stance/swing 控制分工、疲劳检测与安全回退都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充层次 gait assistance、周期学习与疲劳管理样本
