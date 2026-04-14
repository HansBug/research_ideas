# Hybrid Verification Technique for Decision-Making of Self-Driving Vehicles - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场场景下的探索、泊车、避障、减速和停车决策链写成了基于上下文触发的有限状态行为层，并给出可直接落到状态与 guard 的计划规则。

## 条目 1: Parking-lot exploration and collision-aware parking supervisor

- 控制对象：汽车与道路车辆控制领域的停车场自动驾驶行为监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向停车场搜索空位、执行泊车并根据行人/来车距离切换避障、减速和停车动作的自动驾驶行为层监督器。
- 判断：算。对象是真实自动驾驶车辆的 parking-lot behavior layer，不是纯验证流程；原文明确把行为建模为 finite state machine，并给出 `explore -> commence parking -> slow / stop / avoid` 这类可追溯决策链与速度/距离 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 14 页，行为层说明，`paper_content.txt` 第 605-620 行
> For a given sequence of road segments specifying the selected route, the behavior layer is responsible for selecting appropriate driving behavior based on the perceived behavior of other road users and the road conditions.
>
> Since the driving contexts and behaviors available in each context can be modeled as finite sets, a natural approach to automating this decision-making is to model each behavior as a state in a finite state machine with transitions controlled by the perceived driving context as the relative position to the planned route and nearby vehicles.

#### 摘录 B

- 出处：第 17-18 页，parking maneuver executable plans，`paper_content.txt` 第 815-824 行
> if I believe that no free parking space is detected, then I believe that I need to explore the parking lot.
>
> if I believe I need to explore the parking lot, then a set of exploration waypoints should be generated, and these should be uploaded to activate the drive mode.
>
> if I believe that I have detected a free space, then I can remove the belief that I need to explore the parking lot, and I believe I can commence parking operation.
>
> if I believe that I can commence the parking operation, I should generate a set of waypoints for the parking and update the drive mode to reflect this.

#### 摘录 C

- 出处：第 18 页，Plan 5-7，`paper_content.txt` 第 828-868 行
> if it is detected at a distance between 12 m and 6 m then new set of waypoints is generated to avoid the object, if the distance between 6 m and 3 m, then the drive mode is switched to a slower mode, and a new set of waypoints is generated; otherwise, the vehicle is stopped.
>
> If^[Pedestrian detected] while ^[Distance more than 3m and less that 6m] and ^[Object getting closer] then [Activate slow mode.] [Generate object avoidance waypoints.]
>
> If^[pedestrian detected] while ^[distance less than 3m] then [Activate stop mode.] [Update drive mode.].
>
> If^[moving vehicle detected] while ^[distance more than 6m and less that 12m] and ^[object getting closer] then [Generate object avoidance waypoints.]

#### 摘录 D

- 出处：第 22 页，parking-scenario predicates and actions，`paper_content.txt` 第 1075-1081 行
> The movement actions available to AV:
> • AM1: brake to stop.
> • AM2: proceed in reduced speed (2 mph).
> • AM3: proceed in normal speed (5 mph).
>
> The parking actions available to AV:
> • AA1: generate new motion plan for parking.
> • AA2: return to previous motion plan.

### 2. 基于原文整理后的自然语言描述

The autonomous parking agent behaves as a finite-state parking supervisor whose core modes are parking-space exploration, parking execution, object avoidance, slow mode, and full stop. When no free slot is detected, the agent sets a belief that it needs to explore the parking lot, generates exploration waypoints, and updates the drive mode; once a slot is found, it clears the exploration belief, switches to `commencing parking operation`, and generates parking waypoints. The control logic is guarded by perceived context rather than by a fixed cycle, because the paper explicitly models each behavior as a state in a finite state machine whose transitions depend on nearby vehicles, pedestrians, and route-relative context. For pedestrians between `3 m` and `6 m`, the AV activates slow mode and generates avoidance waypoints, while for distances below `3 m` it brakes to a stop. For moving vehicles between `6 m` and `12 m`, it likewise generates an avoidance plan, and the available action set also distinguishes normal driving at `5 mph`, reduced driving at `2 mph`, and explicit parking-plan generation or rollback.

### 3. 逐句溯源

1. 句子 1：The autonomous parking agent behaves as a finite-state parking supervisor whose core modes are parking-space exploration, parking execution, object avoidance, slow mode, and full stop.
   对应摘录：A, B, C
2. 句子 2：When no free slot is detected, the agent sets a belief that it needs to explore the parking lot, generates exploration waypoints, and updates the drive mode; once a slot is found, it clears the exploration belief, switches to `commencing parking operation`, and generates parking waypoints.
   对应摘录：B
3. 句子 3：The control logic is guarded by perceived context rather than by a fixed cycle, because the paper explicitly models each behavior as a state in a finite state machine whose transitions depend on nearby vehicles, pedestrians, and route-relative context.
   对应摘录：A
4. 句子 4：For pedestrians between `3 m` and `6 m`, the AV activates slow mode and generates avoidance waypoints, while for distances below `3 m` it brakes to a stop.
   对应摘录：C
5. 句子 5：For moving vehicles between `6 m` and `12 m`, it likewise generates an avoidance plan, and the available action set also distinguishes normal driving at `5 mph`, reduced driving at `2 mph`, and explicit parking-plan generation or rollback.
   对应摘录：C, D
