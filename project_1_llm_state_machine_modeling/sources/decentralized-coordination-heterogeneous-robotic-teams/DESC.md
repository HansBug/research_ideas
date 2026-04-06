# 异构机器人团队的去中心化协同控制 / From Design to Deployment: Decentralized Coordination of Heterogeneous Robotic Teams

## 论文在讲什么

这篇论文讨论的是 ROSBuzz 如何把 heterogeneous robotic teams 从设计阶段一路部署到真实户外实验，包括多型四旋翼与 Husky 地面车的混合编队。论文既讲软件生态，也讲两类具体 decentralized behavior，其中最值得入库的是 progressive task allocation algorithm：机器人不是预先硬编码分配任务，而是在邻居交互和共享状态基础上逐步加入任务结构。

文章的技术主线不是单纯“群体机器人很灵活”，而是把一个真实可部署的协同行为写成 FSM，并补上了同步 barrier、消息广播、超时恢复和野外实验结果。这样它留下来的不只是 swarm 概念，而是一条完整的、可以追溯到状态与转换条件的机器人协同控制链。

## 控制系统在文中的位置

我们关心的控制系统描述是论文实验部分的主角之一。作者在 Section `3.1` 明确说 progressive task allocation behavior law represented as a finite state machine，并给出 `Turned Off / Take Off / Free / Asking / Joining / Joined / Lock` 七个状态。这里的状态不是 UI、代码更新或系统管理流程，而是机器人在真实任务中的离散行为模式。

更关键的是，Section `2.4.1` 还把 barrier mechanism 写成 swarm-level state-machine synchronization 机制。也就是说，这篇论文不是只给一个抽象编队图，而是把“何时能切到下一状态”“所有机器人如何达成一致”“如果等待太久怎么办”都写到了控制逻辑里，形成了一个带定时恢复链和消息交互语义的协同控制器。

## 对我们为什么有用

它对 `sources/` 的价值在于补到了一类不太像传统 PLC/单机 supervisor 的 multi-robot coordination 样本。很多机器人群体论文即使讲任务分配，也常把重点放在性能曲线、拓扑图或算法框架上，不会把状态名、请求-批准链和 timeout 机制交代到可直接改写成 `STM` 的程度；这篇恰好把这些关键件写清楚了。

它也提供了一个很好的 `FSM + 协议交互 + 局部定时` 组合模板。这里的 barrier 不是泛泛同步概念，而是带 `BARRIER_TIMEOUT = 600` 的工程机制；`Asking / Joining / Joined` 也不是抽象标签，而是对应请求、批准、定位与移动动作。对后续训练模型理解多机器人“请求-同意-加入-同步恢复”这种状态链很有帮助。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看 `2.4.1 Barrier`，把 barrier virtual stigmergy、all-same-state 判据和 timeout fallback 先读清楚。然后直接跳到 `3.1.1 Algorithm` 和 Figure `5`，先抽七个状态的 nominal chain、root 机器人特例、`Free -> Asking -> Joining -> Joined` 的任务获取过程，再补 `Lock` 与 barrier waiting 的作用。

之后再看 `3.1.2` 和 `3.1.3` 的 simulation / field deployment 结果，用来核对这条状态链在高丢包和真实户外条件下如何表现。至于 OTA update、代码热更新、平台兼容性这类内容，第一次为了重做 `STM.md` 可以后看，因为它们更偏基础设施说明，不是主状态机抽取的第一优先级。
