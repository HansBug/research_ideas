问题一句话：本文验证的是动态环境中的安全关键自主系统，核心问题是设计期得到的安全保证在环境变化后是否仍然成立。
方法一句话：作者先用 `UPPAAL` timed automata 和 `TCTL` 在设计期验证移动机器人满足 passive safety，再构造运行期 monitor 检查环境速度等假设是否被破坏。
验证收获一句话：在移动 service robot 场景中，若设计期假设的障碍速度上界是 `0.15` 而运行期真实环境达到 `0.25`，monitor 能检测偏差并驱动系统退入被动安全状态。

## 基本信息

- 标题：Towards the Verification of Safety-critical Autonomous Systems in Dynamic Environments
- 中文标题：面向动态环境中安全关键自主系统的验证
- 作者：Adina Aniculaesei、Daniel Arnsberger、Falk Howar、Andreas Rausch
- 单位：TU Clausthal
- 发表：V2CPS 2016 / Electronic Proceedings in Theoretical Computer Science 232
- DOI：`10.4204/EPTCS.232.10`
- 链接：[DOI](https://doi.org/10.4204/EPTCS.232.10)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：动态环境中移动 service robot 的被动安全控制与监测机制
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供独立 `UPPAAL` 模型或 monitor 实现仓库。
- 案例/数据获取方式：论文使用模拟环境中的移动机器人目标到达场景，正文给出了速度边界、车道、障碍和 monitor 假设。

## 简报

这篇论文的重点不只是“设计期能证明安全”，而是“设计期证明依赖的环境假设一旦失效，系统该如何在运行期发现并止损”。

- 系统：面向目标点行驶的移动 service robot。
- 特点：动态环境、移动障碍、部分感知、被动安全、设计期 + 运行期双阶段。
- 规模：核心场景为 `1` robot + moving obstacle；障碍速度设计期上界 `0.15`，运行期偏离示例为 `0.25`。
- 模型：robot 与 obstacle 都建成 timed automata，并用 monitor 观测系统假设是否仍成立。
- 性质：passive safety，即机器人主动移动时不应导致碰撞。
- 方法：先用 `UPPAAL` + `TCTL` 离线验证，再用 runtime monitor 追踪环境偏差。
- 结果：一旦环境超出模型假设，monitor 会触发系统进入被动安全状态。

`设计期机器人/环境模型 -> TCTL passive safety 验证 -> 运行期 monitor 追踪假设 -> 假设失效时退入 safe state`

## 论文定位

这是一篇 `🎛️ + 🤖` 条目。它的应用对象是具体移动机器人场景，而不是纯理论 runtime verification 框架。

## 验证对象与问题背景

### 系统与场景

场景是移动 service robot 在动态环境中向目标前进，对向车道上存在移动障碍，邻近车道上还有静态障碍。

### 系统组成与运行机制

论文保留了以下关键组成：

1. robot
   - 加速、匀速、刹车、停止等状态。
2. dynamic obstacle
   - 以受限速度向机器人靠近。
3. lane / environment
   - 车道结构决定是否允许侧向避让。
4. monitor
   - 检查运行期环境是否仍满足设计期假设。

### 验证边界

本文验证的是**机器人运动安全层**，而不是完整导航规划、感知算法或机器人平台硬件全部实现。

### 核心问题

即使设计期证明模型满足安全性质，只要环境速度或行为超出假设，离线证明就可能失效。

## 模型与形式化建模

作者把 robot 和 obstacle 抽成二维空间中的离散点，并把碰撞相关距离公式离散化进自动机逻辑中：

1. robot automaton
   - `Idle / Accelerate / Drive / Brake / Stop` 等位置。
2. obstacle automaton
   - 描述静止与向 robot 靠近的运动。
3. 关键变量
   - 当前 robot 速度、braking distance、障碍速度上界、lane 位置。

论文还实现了对被动安全条件的显式检查，例如机器人与障碍在同车道相邻时，机器人必须已停住。

## 验证目标与性质

### 待验证问题

1. 设计期模型是否满足 passive safety；
2. 运行期环境是否仍符合设计期假设；
3. 假设失效时系统是否能切换到安全状态。

### 性质类型

- 安全性质
- 运行期监测
- 环境假设一致性

### 查询表达

论文给出了代表性 `UPPAAL` 性质，例如：

`A[] forall (i:int[0;N-1]) R.y == obstacles[i].y ...`

它用于表达 robot 与 obstacles 在同一车道/相邻位置下的被动安全要求。

## 核心方法与验证流程

1. 建立 robot 与 environment 的设计期 timed automata 模型。
2. 用 `TCTL` 在 `UPPAAL` 中验证 passive safety。
3. 从系统与环境模型中提炼 monitor 需要观测的假设。
4. 运行期让 monitor 持续检查这些假设。
5. 一旦环境偏离，例如障碍速度超上界，系统退入 passive safe state。

## 案例与结果

核心案例是 mobile service robot 驶向目标点的模拟环境：

1. 设计期假设最大障碍速度为 `0.15`。
2. 运行期偏差场景把该上界提高到 `0.25`。
3. 论文说明 monitor 能识别此类偏差，并阻止系统继续依赖已失效的离线证明。

此外，论文在实现中只保留了单车道运行时版本，因此 lane-change 功能更多体现在设计期概念模型里。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究中的“生成-验证-修复”闭环高度相关，因为它已经把离线验证与运行时监测串成了一个闭环雏形。

### 可借鉴之处

1. 明确区分“系统模型正确”与“系统假设仍成立”。
2. 把环境假设本身也当作需要被监控的对象。
3. 用被动安全态作为运行期止损机制。

### 存在的不足与改进空间

论文场景较简化，运行期实现也弱化了换道功能，距离复杂真实机器人系统仍有差距。

### 对本研究的启发

它提示博士研究不应只关注“初次验证通过”，还应考虑模型假设失效后的再验证或修复触发条件。

## 重要的相关工作

### 1. passive safety / passive friendly safety

- 本文直接以这些机器人安全概念作为形式化目标。

### 2. 设计期验证 + 运行期监测

- 论文把两者放在同一框架中，这对闭环研究很有参考价值。

### 3. `UPPAAL` 机器人运动验证

- 这里的关键不是几何建模细节，而是如何把环境假设纳入验证边界。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文开放获取，但未公开完整 `UPPAAL` 工程、monitor 实现或仿真场景包。
- 获取方式/链接：[DOI](https://doi.org/10.4204/EPTCS.232.10)
- 对后续复用的现实影响：适合作为“运行期监测如何接在设计期验证之后”的样本，但复现需要自行重建 robot/obstacle 模型和监测逻辑。
