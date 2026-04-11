# 风能转换系统确定性 FSM 监督控制 / Wind Energy Conversion System under a Supervisor Deterministic Finite State Machine

## 论文在讲什么

这篇会议论文研究一个并网风能转换系统的高层运行监督问题。系统是变速变桨风力机加 DFIG 发电机，低层模型包含叶片和桨距、传动链、发电机和 PI 控制，作者在其上加入一个 deterministic finite state machine 来根据风速和发电机转速选择运行状态。

论文的核心不是形式化验证，而是把风机工作区间整理成 `Park / Start-up / Generating / Brake` 四个 operational states，并比较加入 supervisor 前后输出功率、桨距角和发电机转速的仿真表现。状态机虽然紧凑，但状态语义、进入条件和输出行为足够明确。

## 控制系统在文中的位置

这里的状态机是高层 supervisor，处在连续风机控制模型之上。它不直接替代 PI 控制器，而是决定风能转换系统在关停、启动、额定发电和制动这些运行模式之间如何切换，并约束发电机是否并网、是否以额定转速运行以及是否进入安全停机。

因此，`STM.md` 应把它看成过程与能源控制中的模式管理样本，而不是把大量气动、传动链和电机方程全部展开成状态。那些连续模型主要用于解释 state action 和性能评估，真正可复用的是四态 supervisor 与风速/转速阈值驱动的转移规则。

## 对我们为什么有用

对 `sources/` 来说，这篇论文能补 `🌡️` 过程与环境控制方向的非 PLC 能源系统样本。它与常见水位、灌装、交通灯样本不同，控制对象是连续能源转换设备，但离散监督层仍然很清楚，适合训练模型区分“连续控制对象上的高层 FSM”。

后续做数据集时，建议把 `Park / Start-up / Generating / Brake` 作为主状态集合，保留 wind-speed regions、generator-speed thresholds、grid connection 和 pitch curtailment 这些建模关键件。不要把它降成“风速高低切换”一句话，否则会丢掉状态动作和并网行为。

## 如果需要人工细读，建议怎么读

人工重读时，先看摘要和 Introduction 里的四个风速工作区间，再跳到 Section III-B `Supervisor` 与 Fig. 4 抽状态、转移条件和状态动作。随后只需快速查看 Section IV 的性能比较，确认 supervisor 是系统行为的一部分，而不是单纯画在背景里的概念图。

如果要进一步补精确 guard，可回 PDF 看 Fig. 4 中的风速、发电机转速符号和箭头关系；若只是重写 `STM.md`，低层空气动力学、传动链和 DFIG 状态方程可以放到第二轮，因为它们主要解释连续 plant，不是样本的离散状态机骨架。
