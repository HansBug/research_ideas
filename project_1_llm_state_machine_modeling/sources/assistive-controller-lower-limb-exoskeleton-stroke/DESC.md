# 面向卒中康复下肢外骨骼的辅助控制器 / An Assistive Controller for a Lower-Limb Exoskeleton for Rehabilitation after Stroke, and Preliminary Assessment Thereof

## 基本信息

- **标题**：An Assistive Controller for a Lower-Limb Exoskeleton for Rehabilitation after Stroke, and Preliminary Assessment Thereof
- **中文标题**：面向卒中康复下肢外骨骼的辅助控制器
- **作者**：Spencer A. Murray，Kevin H. Ha，Michael Goldfarb
- **单位**：
  - Vanderbilt University
- **发表**：2014 36th Annual International Conference of the IEEE Engineering in Medicine and Biology Society，2014
- **DOI**：10.1109/EMBC.2014.6944521
- **链接**：https://doi.org/10.1109/EMBC.2014.6944521

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文给出了 gait assistance controller 的有限状态机、子状态、切换条件以及每个状态下的 torque component，足以直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供单独下载数据集。
- 论文描述了卒中偏瘫患者使用下肢外骨骼进行 gait rehabilitation 的具体控制架构和初步实验，可作为医疗辅助控制案例直接收纳。

## 简报

这篇论文解决的是**卒中后偏瘫患者在穿戴下肢外骨骼时，如何在不过度规定步态轨迹的前提下获得 stance 稳定和 swing 辅助**的问题。输入是脚跟着地、腿部角速度、患侧/健侧 swing 与 stance 状态以及进入子状态后的局部时间，方法是用三大 gait state 加每态两个子状态的层次状态机来切换重力补偿、swing torque pulse 和 stance soft stop，输出是 `affected swing -> double support -> unaffected swing` 的完整辅助步态闭环。

- **输入**：heel strike、thigh angular velocity、affected/unaffected knee angular velocity、各子状态进入后的时间 `t_a/t_b`、步态相位信息。
- **方法**：三态双子态有限状态机 + gravity compensation + feedforward torque pulse + stance soft stop。
- **输出**：患侧摆动、双支撑、健侧摆动的 gait assistance 切换，以及 swing/stance 子阶段的差异化关节辅助力矩。
- **一句话评价**：这是高质量的 `HSM + T1` 康复外骨骼控制样本，状态层次、切换事件和局部定时脉冲都写得比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是卒中康复下肢外骨骼的 gait assistance controller。它负责判断当前处于患侧摆动、双支撑还是健侧摆动，以及在各阶段中何时施加 swing assist torque、何时提供 stance soft stop。

### 状态机组织方式

原文把该控制器明确写成 `finite state machine`，包含三个主状态，每个主状态再细分为两个子状态：

1. `State 1`：affected-limb swing
   - `1a` affected knee flexion
   - `1b` affected knee extension
2. `State 2`：double support
   - `2a` after affected heel strike
   - `2b` after unaffected heel strike
3. `State 3`：unaffected-limb swing
   - `3a` unaffected knee flexion
   - `3b` unaffected knee extension

### 关键控制链

论文把 gait assistance 主链写得很清楚：

- 状态机在 `affected swing -> double support -> unaffected swing` 之间按正常步态循环。
- `1a/1b` 与 `3a/3b` 的切换由相应 swing leg 的 knee angular velocity 符号变化驱动。
- 从单支撑到双支撑的切换由相应 swing leg 的 heel strike 触发。
- 从 `2a/2b` 双支撑退出到 swing，则由相应 thigh angular velocity 超过阈值触发。
- 在 swing 子状态中，控制器会根据进入子状态后的时间 `t_a/t_b` 施加有限时长 torque pulse；在 stance 中则对患侧膝关节施加 soft stop。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实康复外骨骼 gait controller**，不是纯临床评估论文。
- 原文既保留了状态结构，也写清了切换事件和状态内的控制动作，适合提取成高质量状态机自然语言描述。
- 对“连续 gait phase 中的离散监督切换 + 状态内局部定时动作”这一类样本特别有价值。

### 可直接借鉴之处

- 可以直接借鉴“三个 gait state + 每态两个 sub-state”的层次建模方式。
- 可以直接借鉴用 heel strike、角速度符号变化和 thigh angular velocity 阈值构成 guard。
- 可以直接借鉴在 swing 子状态内用局部时间驱动 torque pulse 的写法。

### 局限性

- 论文重点是康复辅助策略，故障恢复和异常模式链不丰富。
- 低层 torque equation 比较多，若只关心高层状态链需要适度压缩。
- 评估部分篇幅较多，但状态机主链主要集中在控制结构章节。

## 文献分类总结

- **文献类型**：真实医疗康复外骨骼控制案例论文
- **控制对象**：卒中偏瘫患者下肢外骨骼 gait assistance controller
- **状态机画像**：`HSM + T1`
- **证据强度**：三主状态、六子状态、切换事件和局部定时 torque pulse 明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充康复步态相位监督、人机协同 torque assist 和层次状态机样本
