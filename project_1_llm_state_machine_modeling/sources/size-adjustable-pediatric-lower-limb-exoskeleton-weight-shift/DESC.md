# 基于重心转移的可调节儿童下肢外骨骼设计与控制 / Design and Control of a Size-Adjustable Pediatric Lower-Limb Exoskeleton Based on Weight Shift

## 基本信息

- **标题**：Design and Control of a Size-Adjustable Pediatric Lower-Limb Exoskeleton Based on Weight Shift
- **中文标题**：基于重心转移的可调节儿童下肢外骨骼设计与控制
- **作者**：Yang Zhang，Mathieu Bressel，Sander De Groof，Francois Domine，Luc Labey，Laurent Peyrodie
- **单位**：
  - HEI Junia, Lille, France
  - Faculty of Engineering Technology, KU Leuven, Geel, Belgium
- **发表**：IEEE Access，2023
- **DOI**：10.1109/ACCESS.2023.3235654
- **链接**：https://doi.org/10.1109/ACCESS.2023.3235654

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文明确给出六状态 `FSM`、八个动作、`COM` 轨迹规划、`GRF` 触发规则与 `1 kHz` 实时实现，足以直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文未提供独立数据集。
- 论文给出了 `8-12` 岁儿童适配下肢外骨骼的 gait assistance 控制案例和健康受试者实验，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**儿童下肢外骨骼如何通过双足之间的重心转移自动生成步行轨迹，并在重心真正转移到支撑腿后再触发下一步**的问题。输入是双足 ground reaction force、`COM` 位置、步长和步高参数，方法是以六状态 `FSM` 配合八个动作 `A1-A8` 组织双支撑、重心转移和左右摆腿，再通过 `minimum jerk` 轨迹与 `GRF` 阈值判断实现自动步触发，输出是完整的持续步行和半步回站立控制链。

- **输入**：`COM` 位姿、ground reaction force、步长 `ls`、步高、关节反馈。
- **方法**：六状态 `FSM` + 八动作 gait planning + `minimum jerk` 轨迹 + `GRF` 触发。
- **输出**：`double stand -> COM shift -> swing -> double stand` 的连续步行和半步停机控制流程。
- **一句话评价**：这是高质量的 `EFSM + T0` 外骨骼控制样本，状态、动作、轨迹生成和步触发 guard 都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是儿童下肢外骨骼的 gait assistance supervisor。它负责根据当前支撑态和重心位置，决定何时平移 `COM`、何时抬腿、何时迈整步或半步并回到初始站立态。

### 状态机组织方式

原文把控制器明确写成六状态 `FSM`：

1. `S1`：双脚平行站立
2. `S2`：双脚仍平行，但 `COM` 向左脚靠近
3. `S3`：右脚在前、左脚在后，`COM` 位于支撑多边形中心
4. `S4`：右脚仍在前，但 `COM` 已移到右脚
5. `S5`：与 `S3` 对称，左脚在前
6. `S6`：与 `S4` 对称，`COM` 已移到左脚

同时，状态转移通过 `A1-A8` 八个动作实现，包括左右 `COM` shift、全步 swing、半步回站和连续闭环行走。

### 关键控制链

论文给出了非常明确的主链：

- `A1 / A3 / A6` 负责在双支撑下把 `COM` 平移到支撑脚。
- `A2 / A4 / A7` 负责迈整步，并形成 `S6 -> S3 -> S4 -> S5 -> S6` 的连续 walking loop。
- `A5 / A8` 负责半步并返回 `S1`，从而结束训练流程。
- 对每个动作，论文都给出了 `COM` 在 `x-y` 平面上的 minimum-jerk 轨迹方程。
- 在 `A1 / A3 / A6` 完成后，系统持续监测未来 swing leg 的 `GRF` 降幅；只有当 `γ_GRF` 超过阈值，才触发下一步，避免重心未真正移过去就提前摆腿。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 这是**真实儿童外骨骼 gait assistance 控制器**，不是单纯结构设计或临床综述。
- 原文同时给出状态、动作、轨迹生成公式和 `GRF` 触发 guard，适合直接整理成高质量自然语言状态机描述。
- 对“重心转移驱动的康复外骨骼步态 supervisor”这一类样本很有补样价值。

### 可直接借鉴之处

- 可以直接借鉴 `state + action` 两层表达，即状态定义姿态，动作负责完成过渡。
- 可以直接借鉴以 `GRF` 下降比例判断 `COM` 是否完成转移的 guard 设计。
- 可以直接借鉴 `minimum jerk` 轨迹如何和离散动作状态机关联。

### 局限性

- 论文更关注正常 gait assistance 主链，异常与故障模式相对较少。
- 低层关节控制细节主要放在实现部分，不如高层 `FSM` 那样突出。
- 时间语义更多体现为顺序与实时执行频率，而不是复杂定时器网络。

## 文献分类总结

- **文献类型**：真实医疗康复外骨骼控制案例论文
- **控制对象**：儿童下肢外骨骼的 gait assistance supervisor
- **状态机画像**：`EFSM + T0`
- **证据强度**：六状态、八动作、`COM` 轨迹和 `GRF` 触发条件都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充 pediatrics、weight-shift guard 与自动步触发样本
