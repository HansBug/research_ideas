# DEVELOPMENT OF THE STATE MACHINE FOR THE DISTRIBUTED ELEVATOR CONTROL SYSTEM IMPLEMENTING CONTROLLER AREA NETWORK (CAN) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把每台电梯的 `UP / DOWN / STOP` 提升机状态机、`rank()` 仲裁逻辑以及 `CAN` 广播同步机制写得非常完整，是一条典型的分布式电梯监督控制链。

## 条目 1: Rank-Based CAN-Distributed Elevator Controller

- 控制对象：楼宇机电与电梯控制领域的基于 `CAN` 广播的分布式电梯调度与运动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把每台电梯对象都做成 `Lift-Object` 的分布式控制系统，每个对象本地运行同一套 `Elevator State Machine`，并通过 `rank()` 判断自己是否接管某个楼层请求。
- 判断：算。对象是实际多电梯分布式控制系统，而不是通信仿真框架；原文明确给出 `UP / DOWN / STOP` 三状态、状态变量 `rank / fr / cd / cf`、请求服务 guard、`rank()` 的仲裁逻辑，以及周期性 `CAN` 广播后的本地决策流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section `Elevator State Machine (ESM)`，行 244-321
> A Lift-Object has only tree definite states. It is either moving up, moving down or at rest. These states are named as UP, DOWN and STOP respectively. ... There are four main process variables. They are rank(), fr, cd, cf. ... STOP state is the central state from which UP and DOWN states originate. ... If the existing floor request is equal to current floor while the Lift-Object is in STOP state, passengers are let to get on and fr is cleared. Similarly if the existing car destination is equal to current floor while the Lift-Object is in STOP state, passengers are let to get off and cd is cleared. If there is floor request or car destination while the Lift-Object is in STOP state, the state of the Lift-Object is changed either to DOWN or UP depending upon values of fr and cd.

#### 摘录 B

- 出处：第 5-6 页，Section `rank()`，行 358-400
> In DECS where many Lift-Objects exist, floor request coming from any of the Stair-Object is conveyed to all Lift-Objects simultaneously. It is the duty of individual Lift-Object to decide whether or not it should serve the request. Only one Lift-Object must serve the actual floor request. ... The logic behind the rank() function checks the position, direction and the car destination vector of the current Lift-Object against the other Lift-Objects in the vicinity of the request. If there is any other Lift-Object in the vicinity of the request whose state is more feasible then the current Lift-Object, then the other Lift-Object should serve the request ... the rank() function of the current Lift-object returns true, meaning it must serve the request.

#### 摘录 C

- 出处：第 8 页，Section `State Capsulation`，行 564-572
> In regular mode of operation, the current state of each object in the DECS is broadcasted through the CAN bus. This makes it possible the creation and the synchronization of the entire process data in each object locally. Once the process data is synchronized, the individual Lift-Object can determine its rank and runs ESM module. ESM module makes a decision how the Lift-Object behaves under current entire process data.

### 2. 基于原文整理后的自然语言描述

The distributed elevator controller assigns the same local state machine to every `Lift-Object` and lets each car decide its behavior from synchronized network data. The local `ESM` has three explicit states, `UP`, `DOWN`, and `STOP`, and it uses four process variables as guards: `rank()` for service ownership, `fr` for floor request, `cd` for car destination, and `cf` for current floor. `STOP` is the hub state: if a floor request or car destination matches the current floor, the controller opens service at that floor and clears the corresponding request, while non-matching requests shift the car to `UP` or `DOWN` according to their relative position. In the multi-lift case, every hall request is broadcast to all lift objects, but only the car whose `rank()` remains true is allowed to serve it. This `rank()` decision is itself stateful, because it compares the current car's position, direction, and destination vector against nearby lifts, and the whole arbitration only works after all objects have broadcast and synchronized their state through the `CAN` bus.

### 3. 逐句溯源

1. 句子 1：The distributed elevator controller assigns the same local state machine to every `Lift-Object` and lets each car decide its behavior from synchronized network data.
   对应摘录：C
2. 句子 2：The local `ESM` has three explicit states, `UP`, `DOWN`, and `STOP`, and it uses four process variables as guards: `rank()` for service ownership, `fr` for floor request, `cd` for car destination, and `cf` for current floor.
   对应摘录：A
3. 句子 3：`STOP` is the hub state: if a floor request or car destination matches the current floor, the controller opens service at that floor and clears the corresponding request, while non-matching requests shift the car to `UP` or `DOWN` according to their relative position.
   对应摘录：A
4. 句子 4：In the multi-lift case, every hall request is broadcast to all lift objects, but only the car whose `rank()` remains true is allowed to serve it.
   对应摘录：B, C
5. 句子 5：This `rank()` decision is itself stateful, because it compares the current car's position, direction, and destination vector against nearby lifts, and the whole arbitration only works after all objects have broadcast and synchronized their state through the `CAN` bus.
   对应摘录：B, C
