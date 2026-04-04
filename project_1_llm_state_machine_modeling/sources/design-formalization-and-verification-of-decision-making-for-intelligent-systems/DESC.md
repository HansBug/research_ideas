# 智能系统决策制定的设计、形式化与验证 / Design, Formalization, and Verification of Decision Making for Intelligent Systems

## 论文在讲什么
这篇论文解决的是自主系统高层决策模块如何系统设计、形式化并验证的问题。虽然论文有明显的方法论文属性，但它并不是空泛示例，而是把 NASA 漫游车协同任务中的 `DZR` 决策层完整地实例化成一个可追溯的 `H-FSM`，并给出状态、事件、局部时间窗口和输出参数。
从论文的展开方式看，输入侧主要落在 任务分解结果、事件向量 `EA / EB / EC / ED / EE`、相关 flag 和 rover 任务阶段，核心做法是 functional decomposition + `H-FSM` + FRET structured NL + CoCoSim verification，最终形成的则是 `DZR` 决策层状态机、形式化需求和针对 Simulink 实现的验证结果。 因此它虽然带有明显的方法或工具链背景，但控制案例并不是装饰性示例，而是整篇论证真正依附的实体对象。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统不是顺手附带的演示例子，而是论文把方法、形式化描述和验证结果真正落地的主要案例载体。 原文 case study 针对的是 NASA 自主 rover 系统中的 `Dynamic Zonal Relay` 阶段决策模块。该模块不负责连续控制本身，而是位于高层，向低层控制器下发 controller mode、activity 和 velocity 等参数，并根据任务事件切换状态。
作者把 `DZR_1` 拆成三个 meta-state，例如 `DriveToZone_11`、`CharacterizeZone_12`、`Relay_13`。 更关键的是，它不仅写了状态，还把事件条件写成了可直接落形式化模型的规则。例如 `ED_2 <=> persisted(3, F_segmentCharacterizationComplete)`、`Upon(FSM_State_3 = DZR_CharacterizeZone_Acquire & ED_2) ... FSM_State_3 = DZR_CharacterizeZone_Transmit`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文补充了 `sources` 中较少见的自治任务决策层样本。 同时具备层次状态、事件向量、局部时间窗口和参数输出映射。 即使论文整体偏验证方法，`DZR` 部分仍然具备足够强的原文证据，可直接入库。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `meta-state / sub-state / leaf-state` 的组织方式、把状态机事件定义写成 `persisted(n, flag)` 这种局部时间条件、在叶状态上附着 `controllerType / activity / velocity` 这样的接口参数 这些最容易直接转成状态机自然语言描述的部分。 论文重点仍包含方法论与工具链介绍，抽取时必须明确只保留 `DZR` 案例的控制对象部分。 具体 rover 硬件与环境约束写得不如纯控制案例论文细。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。
