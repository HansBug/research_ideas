# 面向地面与楼梯场景的解耦机械结构机器人及其状态机控制 / A Robot with Decoupled Mechanical Structure and Adapted State Machine Control for Both Ground and Staircase Situations

## 基本信息

- **标题**：A Robot with Decoupled Mechanical Structure and Adapted State Machine Control for Both Ground and Staircase Situations
- **中文标题**：面向地面与楼梯场景的解耦机械结构机器人及其状态机控制
- **作者**：Hao Wen，Hongcheng Yang，Yu Chen，Lin Zhou，Di Wu
- **单位**：
  - Chongqing University
  - Huazhong University of Science and Technology
- **发表**：Applied Sciences，2019
- **DOI**：10.3390/app9235185
- **链接**：https://doi.org/10.3390/app9235185

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文给出了 stair-climbing robot 的 state machine、sensor set、switch conditions 和 basic actions，可直接作为控制器设计证据使用。

### 数据集/案例获取方式

- 原文未提供外部数据集。
- 论文基于自研 last-mile delivery / stair-climbing robot 给出了 ground mode、posture adjustment、climbing cases 和 sensor-triggered transition 条件，适合直接作为单案例 source paper。

## 简报

这篇论文解决的是**一个送货机器人如何在地面行驶和上下楼梯之间切换，并在楼梯场景中维持姿态、触发不同 climbing cases**的问题。输入是 Mecanum wheel 编码器、EH 编码器和激光测距传感器，方法是构造一个带 `SC1-SC7` 触发条件的 stair-climbing state machine，输出是 `ground mode -> posture adjustment -> climb -> return to ground mode` 的完整顺序控制链。

- **输入**：wheel encoder、EH encoder、laser ranging sensor distance、step-edge distance。
- **方法**：基于 sensor-triggered switch conditions 的楼梯机器人状态机。
- **输出**：地面模式、姿态调整、上楼案例切换、下楼状态流和回到 ground mode 的控制逻辑。
- **一句话评价**：这是典型的 `FSM + T0` 机器人顺序控制案例，SC 条件、状态动作和回地面条件都足够清晰。

## 控制系统与状态机证据

### 控制对象

论文对象是一个用于 last-mile delivery 的 stair-climbing robot。控制器需要根据台阶距离和机器人姿态，在地面行驶、姿态调整和不同 stair-climbing case 之间切换。

### 状态机组织方式

原文的 state machine 由 `ground mode` 与多个 climbing / posture-adjustment cases 组成，并通过 `SC1-SC7` 条件触发切换。其核心状态和动作包括：

1. `ground mode`
2. `Case 1`
3. `Case 2`
4. `Case III`
5. `Case IV`
6. 对应 moving downstairs 的镜像状态流

### 关键控制链

论文把 stair-climbing 主链写得很明确：

- 系统启动后默认在 `ground mode`，只有检测到台阶且满足 `SC2` 才离开地面模式。
- `SC2` 触发 `Case 1` 姿态调整，使前轮靠近楼梯并让 tetrapod 落地。
- `SC7` 触发 `Case III`，正式开始上楼。
- 在 climbing 过程中根据 `SC3/SC4/SC5/SC6` 切换 `Case I / Case II / Case IV` 与姿态调整。
- 当 `SC1` 再次满足，状态机返回 `ground mode`，从而结束楼梯过程。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它是**真实机器人移动控制案例**，不是抽象步态方法综述。
- 原文明确给出 state machine、sensor triggers 和动作切换，非常适合转写成自然语言状态机样本。
- 它补充了当前文库中较少的“台阶/姿态调整/多阶段 climbing”类离散控制样本。

### 可直接借鉴之处

- 可以直接借鉴 `SC1-SC7` 这类显式传感器守卫条件写法。
- 可以直接借鉴 `ground mode -> posture adjustment -> climbing -> ground mode` 的顺序监督链。
- 可以直接借鉴通过 front-wheel 和 wheel-leg distance 区分不同 climbing cases 的 guard 设计。

### 局限性

- 论文主要展开 moving upstairs，对 moving downstairs 只说明可类似建立，不如上楼链详细。
- 低层运动学和机械结构解释较多，需要筛掉与状态机建模无关的连续几何推导。
- 时间语义主要来自动作顺序，不是显式时间窗口。

## 文献分类总结

- **文献类型**：真实机器人控制案例论文
- **控制对象**：面向地面与楼梯场景的 stair-climbing robot 控制器
- **状态机画像**：`FSM + T0`
- **证据强度**：sensor set、SC 条件和 state-machine operation 说明完整，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充姿态调整与台阶攀爬类顺序控制样本
