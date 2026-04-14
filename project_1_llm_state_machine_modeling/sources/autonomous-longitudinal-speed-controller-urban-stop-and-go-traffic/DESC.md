# 城市停走场景纵向跟驰监督控制器 / LONGITUDINAL VEHICLE SPEED CONTROLLER FOR AUTONOMOUS DRIVING IN URBAN STOP-AND-GO TRAFFIC SITUATIONS

## 论文在讲什么

这篇硕士论文讨论的是自动驾驶车辆在城市 stop-and-go 场景中的纵向速度控制问题，尤其关注 follower 车辆如何并入并稳定跟随 leader。作者并没有把重点放在单一控制律调参上，而是明确指出车辆在并入、接近、稳定跟随和危险逼近过程中会经历若干离散阶段，因此需要一个上层 supervisory controller 来决定何时切换控制模式和参考速度。

论文围绕这个目标提出了 `Longitudinal FSM`。这套状态机不是抽象地列出几个 maneuver 名称，而是把 `Cruise`、`Approach`、`Follow`、`Emergency Brake` 和 `Hard Braking` 五个状态的含义、阈值和进入条件都写出来，并说明 `Follow` 状态下会切换到哪类 close-following controller。这样一来，论文提供的不只是“有一个 FSM”的概念，而是一整条可追溯的车辆纵向监督控制链。

## 控制系统在文中的位置

我们关心的控制系统描述在文中是核心对象。作者先给出车辆模型和纵向控制总体结构，但一旦进入 `Chapter 3`，整个叙述就围绕 supervisory controller 展开：为什么需要 `FSM`，每个状态解决什么任务，什么距离阈值会触发状态切换，以及 follower 在不同状态应该给出什么参考速度。它不是仿真附属图，而是把底层 LQR 控制器组织起来的主控逻辑。

尤其值得保留的是，这篇论文没有只写 nominal follow path。它还明确区分了 `Emergency Brake` 和 `Hard Braking` 两级危险态，把 `1.5 m` 和 `0.5 m` 这样的阈值直接写进状态定义，并说明 leader 加速、超出 sensing range 时应回到 `Cruise` 或 `Approach`。对 `sources/` 来说，这类把异常距离工况写清楚的纵向监督器，比只给“车队跟驰效果很好”的控制论文要有用得多。

## 对我们为什么有用

这篇论文对文库的意义，首先在于它补进了一个 `🚗` 方向的高细节 `FSM + T0` 样本，而且对象非常典型：城市自动驾驶中的纵向跟驰与并入。文库里虽然已经有若干 lane change、behavior planner 或 automated driving 决策样本，但这篇材料把纵向距离管理、两级制动保护和 close-following 控制器切换讲得很具体，因此和纯横向换道或高层行为仲裁样本并不重复。

其次，这篇论文对后续建模也很友好。它一方面提供了清楚的离散状态边界，另一方面又保住了每个状态背后的连续控制含义，因此非常适合做“上层离散监督器如何包裹底层连续控制器”的训练样本。如果后续要研究 LLM 生成汽车状态机时如何表达 threshold、controller handoff 和 safety escalation，这篇论文会是很好的基准案例。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 30-31 页 `Longitudinal FSM` 的总述和 block diagram，把这套 supervisor 在整体控制框架里的位置固定下来。接着直接精读第 34-39 页的 `Cruise`、`Approach`、`Follow`、`Emergency Brake`、`Hard Braking` 五节，把每个状态负责的任务、参考速度规则和关键阈值抄出来，再配合第 40 页 `Figure 20` 对照一遍转移顺序。

第一次人工复核时，可以把更多精力放在状态与阈值，而不是底层 LQR 推导和后续控制性能分析。真正决定 `STM` 质量的是这条链：什么时候从 `Cruise` 进入 `Approach`，什么时候切入 `Follow`，何时升级到两级制动，以及 leader 消失或加速后如何退出危险态。只要把这几处逻辑读稳，这篇论文就足以支撑一个高质量汽车纵向监督控制样本。
