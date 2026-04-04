# Research on the Decision and Planning System of Automated Valet Parking Based on Finite State Machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把代客泊车与定点召回的上层模式切换、行车子状态机和泊车子状态机都写成了明确的分层离散控制链，原文细节足够支撑双 A。

## 条目 1: Hierarchical AVP Mode and Behavior Supervisor
- 控制对象：智慧停车领域的自动代客泊车与定点召回分层决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个面向露天停车场自动代客泊车与定点召回的分层有限状态机控制器，上层负责 `初始/行车/泊车/结束` 模式切换，下层进一步细化为行车行为决策和泊车安全决策。
- 判断：算。对象是实际车辆的高层离散控制与行为监督器，不是单纯路径规划算法；原文直接给出了状态集合、事件表、行为子状态和进入/退出条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Abstract / `1.1 上层状态机设计`，`paper_content.txt` 第 27-31 行、第 129-145 行
> the upper-level functional state machine and the lower-level behavior state machine are designed, and the logical switching relationship between the behavior states of the vehicle is established according to the environment and the defined rules of the vehicle.
>
> （1）代客泊车模式　驾驶员选择代客泊车功能，车辆在接收到信号后，从初始状态跳转至行车状态；在车辆行驶至行车泊车切换区域后，车辆减速停止，随后进入泊车状态；在完成泊车后，车辆进入结束状态，完成代客泊车流程。
>
> （2）定点召回模式　驾驶员在远程选择定点召回功能并输入召回点，车辆接收召回点信息后，从初始状态跳转至泊车状态；完成泊出后，跳转至行车状态；行驶至召回点区域并完全停下后，车辆进入结束状态，完成定点召回流程。

#### 摘录 B
- 出处：第 3-4 页，`1.2 行车状态机设计 / 1.2.2 行车行为决策`，`paper_content.txt` 第 147-179 行、第 221-241 行
> 使用有限状态机设计车辆在行车过程中的主要状态。
>
> 为提高车辆的响应速度，行车过程行为决策应在满足车辆安全性的同时，保证一定效率，因此设计行车模块主要行为如下：常规行驶、跟车行驶、行车制动以及换道行驶。
>
> DE3：换道需求分为两类。第 1 类为主动换道，在车辆当前行驶车道与目标车道不一致时触发，目标车道的选取根据目标车位与召回点所处位置进行选取。第 2 类为被动换道，当自车前方跟车距离内存在速度较慢或 `0<TTCFront≤TTCT` 的障碍物，车辆同样存在换道需求。
>
> DE5：以左车道为例，当左车道前后车辆皆满足 `TTC>TTCT`，同时前后车辆与自车车距大于最小规划距离，判定左车道允许换道。

#### 摘录 C
- 出处：第 4 页，`表 2 / 1.3 泊车状态机设计`，`paper_content.txt` 第 252-284 行
> 表 2　行车状态事件
> `DE1` 前车是否在跟车范围
> `DE2` 前车是否处于制动范围
> `DE3` 是否存在换道需求
> `DE4` 是否完成换道
> `DE5` 是否允许换道
> `DE6` 是否进入目标区域
>
> 为满足车辆在泊车过程中的安全，设计车辆泊车状态机转移图，如图 5 所示，泊车事件表如表 3 所示。
>
> 关于车辆碰撞风险（`BE1`）的判断，将未来规划时间 `τp` 内，车辆轮廓在规划路径下扫掠所得到的区域作为障碍物风险区域。 在该区域内存在障碍物时，事件 `BE1` 置为 1，反之置为 0。

### 2. 基于原文整理后的自然语言描述

The valet-parking controller is organized as a hierarchical finite state machine in which the upper layer switches among `initial`, `driving`, `parking`, and `end`, while the lower layer refines the behavior inside driving and parking. In valet-parking mode, the vehicle goes from `initial` to `driving`, enters `parking` after it reaches the driving-parking switching region and stops, and terminates in `end` after parking is completed; in fixed-point recall mode, the vehicle starts from `initial`, unparks in `parking`, returns to `driving`, and finishes after reaching the recall region and stopping completely. Inside the driving sub-state machine, the controller classifies nearby obstacles in Frenet coordinates and chooses among regular driving, following, braking, and lane changing using event conditions `DE1` to `DE6`, including both active and passive lane-change requests and TTC-based lane-availability checks. Inside the parking sub-state machine, the safety event `BE1` is raised whenever an obstacle appears inside the swept risk region over the future planning horizon `τp`, so parking execution is guarded by an explicit obstacle-risk check rather than a blind trajectory handoff.

### 3. 逐句溯源

1. 句子 1：The valet-parking controller is organized as a hierarchical finite state machine in which the upper layer switches among `initial`, `driving`, `parking`, and `end`, while the lower layer refines the behavior inside driving and parking.
   对应摘录：A
2. 句子 2：In valet-parking mode, the vehicle goes from `initial` to `driving`, enters `parking` after it reaches the driving-parking switching region and stops, and terminates in `end` after parking is completed; in fixed-point recall mode, the vehicle starts from `initial`, unparks in `parking`, returns to `driving`, and finishes after reaching the recall region and stopping completely.
   对应摘录：A
3. 句子 3：Inside the driving sub-state machine, the controller classifies nearby obstacles in Frenet coordinates and chooses among regular driving, following, braking, and lane changing using event conditions `DE1` to `DE6`, including both active and passive lane-change requests and TTC-based lane-availability checks.
   对应摘录：B, C
4. 句子 4：Inside the parking sub-state machine, the safety event `BE1` is raised whenever an obstacle appears inside the swept risk region over the future planning horizon `τp`, so parking execution is guarded by an explicit obstacle-risk check rather than a blind trajectory handoff.
   对应摘录：C
