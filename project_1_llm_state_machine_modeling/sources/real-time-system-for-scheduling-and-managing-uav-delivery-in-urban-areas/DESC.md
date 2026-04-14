# UAV-AGV 协同配送执行中间层 / A Real-Time System for Scheduling and Managing UAV Delivery in Urban Areas

## 论文在讲什么

这篇论文关注的是城市 UAV 配送机场里的执行管理层，而不是单独的路径规划或单独的调度算法。作者把一个“机场-卸货站”配送模式拆成了主控节点、UAV 管理节点和 AGV 管理节点，再用两个有限状态机把无人机和地面搬运车的行为组织起来，让高层调度指令能够真正落到起飞、装货、转运、返航和回收动作上。

从文库视角看，这篇论文最强的价值是它没有停留在“调度框架”层，而是把执行状态写实了。UAV 有 `Ready / On Car / Waiting Go / Flying Go / Waiting Back / Flying Back` 六个状态，AGV 有 `Waiting Pickup / Waiting Working / Waiting GoAW / Waiting GoGW` 四个状态，还补了命令和 guard，所以它能提供一个带并行结构和消息交互的真实执行控制样本。

## 控制系统在文中的位置

控制系统不是附属案例，而是论文的中心内容之一。论文前半段虽然会讲配送背景和调度目标，但真正承上启下的是管理系统本身：主控节点如何收状态、如何向调度器汇总、如何再把结果分发到 UAV 和 AGV。后面的所有实验和调度方案，都依赖这套执行层把抽象计划翻译成具体动作。

换句话说，我们关心的控制系统描述在文中承担的是“中间件级执行协调器”的角色。它既不像纯飞控那样只管单个 UAV，也不是只在上层做时间表优化，而是明确负责两类执行体的状态同步、命令转发和周期闭环，这正是 `project_1` 里比较少见但很有价值的控制样本。

## 对我们为什么有用

它对 `sources/` 的意义，在于补入了一个带并行子机和消息交互的 UAV 配送执行样本。现有飞行控制或任务管理论文里，很多只给顶层 mode switch；这篇则把 UAV 与 AGV 的协同过程写到了可直接抽成状态机语言的粒度，尤其适合补“多个执行体如何通过命令和状态回报闭环配合”的描述类型。

此外，这篇论文还很适合后续做“自然语言恢复分布式控制逻辑”的实验。像 `Delivery`、`UAV Receive`、`Load Cargo`、`Retrieved`、`Landed` 这种命令与条件，本身就很接近事件和 guard；而主控节点的状态汇总与下发，也能自然转成协议交互或多机协调类样本。

## 如果需要人工细读，建议怎么读

人工细读时，建议先看第 1-2 页，只确认机场布局、AW/GW 两个区域、UAV 与 AGV 的职责分工，以及论文为什么需要一个中间层。然后直接跳到第 3-4 页，把 `Management Nodes`、`UAV Finite state machine`、`AGV Finite state machine` 和 `State Transition Process` 连续读完，先把两个 FSM 的状态、命令、条件和完整往返周期抽出来。

第二轮再看后面的 ground traffic scheduler 和 air traffic scheduler。那部分更多是在解释这套执行层怎样接住上层调度，并决定起飞/返航许可与落点分配；如果第一次阅读只为了重建 `STM.md`，优先把并行 FSM 和完整 delivery cycle 读稳即可，调度性能和实验评分可以稍后再补。
