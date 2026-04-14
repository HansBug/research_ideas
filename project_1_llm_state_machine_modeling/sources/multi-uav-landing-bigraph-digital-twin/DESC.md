# 多 UAV 着陆数字孪生中的 AeroCtrl 状态机 / A Bigraph-Based Digital Twin for Multi-UAV Landing Management

## 论文在讲什么

这篇论文讨论的是 multi-UAV landing management 的 formal digital twin。作者想解决的不只是“多个 UAV 怎么分配 pad”，还包括如何让形式化模型、运行时控制服务和真实 UAV 执行保持 cyber–physical consistency。为此，论文把 bigraph-based spatial model、model checking 和实际控制服务三者串成一个统一框架。

对我们最有用的部分并不是 bigraph 语法本身，而是作者为了把形式化模型真正落地，专门实现了一个叫 AeroCtrl 的 UAV controller web service。这个服务负责 take-off、landing、Cartesian navigation 等核心技能，并把状态迁移暴露成 REST endpoint，再通过 ROS2 把状态机迁移落实成真实飞行动作。

## 控制系统在文中的位置

控制系统描述在文中扮演的是“连接形式化模型与真实执行”的关键桥梁。bigraph 负责描述 pad 占用和 reaction rules，但要让这些规则能在真实 Crazyflie 平台上执行，论文必须给每架 UAV 一个真正可跑的 controller。AeroCtrl 就承担了这个角色。

这也是为什么这篇论文虽然整体偏 formal digital twin，但仍值得留在 `sources/`。作者没有停留在“验证完就结束”，而是明确给出一个 state-machine-based control service，并说明它如何把 OSGi lifecycle 与 UAV operational lifecycle 正交耦合、如何通过 `activate_idle / begin_takeoff / begin_landing` 等接口触发迁移、以及如何在 web monitor 里展示当前状态和历史迁移。

## 对我们为什么有用

对 `sources/` 而言，这篇样本补的是航空方向里比较少见的 `HSM + 并行` 控制图像。库里已有不少 UAV mission FSM、landing supervisor 或 CubeSat mode manager，但像 AeroCtrl 这样把“软件服务生命周期”和“飞行生命周期”并列建模、再通过运行时接口显式耦合的样本并不多。

它还特别适合后续讨论“形式化模型怎样接到真实控制器上”这类问题。很多 formal-methods 论文能给出很漂亮的抽象模型，却缺少运行时 controller；而这篇恰好保住了从 verified rule 到 executable controller 的那一层，因此对 project 1 的状态机样本库有补位意义。

## 如果需要人工细读，建议怎么读

人工回原文时，建议先读摘要与第 `11-12` 页的 `3.4.2 AeroCtrl`、`3.5 Execution by Cyber–Physical Synchronization`。第一轮重点不是 bigraph 反应规则，而是先把 AeroCtrl 的对象边界锁住：它究竟管理哪些 UAV 技能、状态机里有哪些并列区域、以及哪些接口真正会触发飞行动作。

第二轮如果要补 pad-allocation 或 digital twin 全链条，再回看前面关于 BRS、bigrid spatial model 和 reaction rule 的内容。那部分负责解释 landing management 的上层约束，但 `STM.md` 的主控制链已经集中在 AeroCtrl 的双生命周期状态机和其 REST/ROS2 执行接口上。
