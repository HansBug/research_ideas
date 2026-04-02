# 使用 Petri 网的模块化人机协作安全控制系统 / Towards a Modular Human-Robot Safety Control System Using Petri Nets

## 基本信息

- 标题：Towards a Modular Human-Robot Safety Control System Using Petri Nets
- 中文标题：使用 Petri 网的模块化人机协作安全控制系统
- 作者：Philipp Kranz, Fabian Schirmer, Marian Daun, Tobias Kaupp
- 发表：*Proceedings of the 21st International Conference on Informatics in Control, Automation and Robotics*, pp. 384-391, 2024
- DOI：`10.5220/0013011900003822`
- 链接：https://doi.org/10.5220/0013011900003822
- 形式主义：`Modular Petri-Net-Based HRC Safety Control`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🏭
- 论文角色：人机协作任务级安全控制 / modular Petri net application
- 工具/实现获取方式：原文明确给出 human/robot safety control loops、`MAPE` 结构与 toy pick-up truck 用例；未给出公开代码仓库。
- 标准/格式获取方式：承载方式是 Petri nets、`MAPE` safety loops 与 `SRI` 评分规则；原文未提供独立交换标准。

## 简报

这篇论文用 `Petri Net` 做的不是一般的任务流，而是把人、机器人和人机协作步骤各自的 safety control loop 都压成可并发运行的网。它通过 `MAPE` 结构持续监测环境、计算 `SRI`、调整机器人参数或告知人类操作者风险，从而把原本按“整条装配序列一次性评估”的静态安全分析，改造成按 task-step 滚动评估的动态安全控制。

- 形式主义定位：面向 `HRC` 任务级安全评估的 `Petri Net` 应用条目，而不是新的协作语言或安全标准。
- 构造方式简述：把 assembly sequence、robot safety loop 和 human safety loop 三块用 `PN` 拼在一起，并通过共享任务条件和 `SRI` 结果协调。
- 基础设施与场景简述：依托 `MAPE`、`SRI`、depth camera、robot speed/force parameter 与 `PN` token flow，服务模块化人机协作装配。

```text
assembly step + human/robot context -> Petri-net MAPE loops -> SRI calculation -> parameter/risk adjustment -> task execution decision
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. 人、机器人与共享装配任务三个子系统。
2. `MAPE` 四阶段：Monitor / Analyze / Plan / Execute。
3. 任务相关的 components、actions、tools 与 interaction modality。
4. `SRI` 这一任务级风险指标。
5. 表达 task readiness 与 residual risk 的 `PN` transitions。

### 核心抽象

论文首先定义了 Safety Risk Indicator：

$$
SRI = 3 \times S + 2 \times O + 1 \times F
$$

上式中的符号逐项解释如下：

1. `S` 是 severity，即危险后果严重性。
2. `O` 是 occurrence，即失效或危险出现的可能性。
3. `F` 是 frequency，即暴露在危险场景中的频率。
4. 权重 `3/2/1` 说明作者把严重性看得最重，其次是发生概率，再其次是暴露频率。

论文进一步给出 robot token 的值域构成：

$$
Robot = Type \times CurrentSpeed \times CurrentForce \times Components \times Actions \times Tools \times Interaction \times SRI
$$

上式中的符号逐项解释如下：

1. `Type` 是机器人类型。
2. `CurrentSpeed` 与 `CurrentForce` 是可调整的当前执行参数。
3. `Components/Actions/Tools/Interaction` 表示当前装配步骤的任务上下文。
4. `SRI` 是当前步骤计算出的风险指标。

在人机协作步骤中，作者把 human 与 robot 信息合成共享 token：

$$
Human\text{-}Robot = Type \times CurrentSpeed \times CurrentForce \times EmployeID \times Jobtitle \times Trainings \times Components \times Actions \times Tools \times Interaction \times SRI
$$

上式中的符号逐项解释如下：

1. `EmployeID/Jobtitle/Trainings` 表示人类操作者的身份、岗位与训练背景。
2. 其余符号沿用 robot token 定义。
3. 该式说明协作安全评估不是简单把两边分开，而是把双方状态压到同一任务 token 上。

### 一个最小例子与通俗解释

原文的 toy pick-up truck 用例非常直观：

1. 机器人先执行 `Prepare Base`，人同时执行 `Prepare Sub-Assembly 1`。
2. 之后进入 `Fix Front Axle` 这类人机协作步骤，两个 safety loops 同时启动。
3. 初始 interaction 被设成 collaborative 时，`SRI = 14`，风险过高，不能直接执行。
4. 把 interaction 调整为 synchronization 后，`SRI` 下降到 `10`，任务才被允许继续。

通俗地说，这个模型像一个“会先算安全分再决定能不能干活”的协作工位控制器，而且这个安全分不是整条生产线一口气算完，而是每做一步都重算一次。

### 运行 / 接受 / 转移语义

论文虽未重新定义 `PN` 元组，但控制流显式采用 firing 语义。可保守写成：

$$
M \xrightarrow{t} M'
$$

上式中的符号逐项解释如下：

1. `M` 是当前 marking，表示任务 token 目前位于哪个 `MAPE` 阶段。
2. `t` 是某个 transition，如 `Check Environment` 完成、`SRI` 满足阈值、或需要回退重评估。
3. `M'` 是 firing 后的新 marking。
4. 这对应论文图中的 `T7/T8/T12/T14` 等“满足阈值则执行、不满足则回环”的控制机制。

### 语义边界

这篇论文的边界如下：

1. 它重心是任务级安全控制，而不是连续机器人动力学。
2. `SRI` 是离散化风险指标，因此无法覆盖细粒度连续危险变化。
3. 人的行为被抽象成被动可告知、不可像机器人那样精确调参。
4. 它更像“模块化安全控制骨架”，而不是完整工业安全认证流程。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 风险指标 | `$SRI = 3 \times S + 2 \times O + 1 \times F$` | 任务级安全评估依赖 severity / occurrence / frequency 的加权组合。 |
| 机器人 token | `$Robot = Type \times CurrentSpeed \times CurrentForce \times Components \times Actions \times Tools \times Interaction \times SRI$` | 说明 robot safety loop 需要哪些状态量。 |
| 协作 token | `$Human\text{-}Robot = Type \times CurrentSpeed \times CurrentForce \times EmployeID \times Jobtitle \times Trainings \times Components \times Actions \times Tools \times Interaction \times SRI$` | 把人和机器人共同压到同一步骤的安全状态里。 |
| firing 语义 | `$M \xrightarrow{t} M'$` | 任务 token 在 `MAPE` 阶段之间流动。 |
| 安全门槛 | `$robot.SRI \le robot.parameter \land human.SRI \le Human.risk$` | 只有双方安全条件都满足，协作任务才能启动。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 人、机器人和协作任务都有显式 places。 |
| 事件 / 触发 | 强支持 | `T0/T1/...` 等 transitions 明确控制安全回环。 |
| 守卫 / 数据 | 强支持 | `SRI`、速度/力、人员训练和 interaction modality 都进入 token 与 guard。 |
| 层次 | 部分支持 | 通过 robot/human/HRC 三块子网形成弱层次。 |
| 并发 / 同步 | 强支持 | human loop 与 robot loop 并行运行，并在共享任务处同步。 |
| 时间约束 | 弱支持 | 核心不在显式时间，而在任务级风险评估。 |
| 连续动态 / 随机性 | 不支持 | 机器人动力学与随机行为不是主体。 |
| 可执行 / 可验证性 | 强执行、部分验证 | 任务级安全逻辑明确，但形式验证深度有限。 |

### 形式化问题与性质

1. 论文最有价值之处在于把 `HRC` 安全从“整条线一次性评估”改成“任务级滚动评估”。
2. `Petri Net` 在这里承担的是并发安全控制骨架，而不是单纯工作流图。
3. `MAPE` 与 `SRI` 的组合让任务执行、风险计算和参数调节串成闭环。
4. 对 `Petri` 主干来说，这是把并发网应用到 `HRC` safety control 的新鲜案例。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先识别装配序列中的 robot-only、human-only 和 human-robot tasks。
2. 为 robot 与 human 各自建立 `MAPE` safety control loop。
3. 在协作步骤上把两边 token 的值域合并。
4. 通过 `SRI` 阈值来决定执行、回环重评估还是仅风险告知。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. `PN` 图结构。
2. 颜色区分的 assembly / robot safety / human safety 三块子网。
3. token 中的任务上下文与人员/机器人参数。
4. 基于 `SRI` 的 transition guards。

### 交换与互操作

互操作重点不在开放标准，而在任务级拼接：

1. assembly sequence 触发 human/robot safety loops。
2. loops 通过共享 task context 与 `SRI` 结果互相约束。
3. 机器人参数可主动调整，人类侧则通过风险告知做被动缓解。

## 配套基础设施

- 建模/编辑工具：原文未说明专用 `PN` 编辑器。
- 解析/交换/元模型支持：未提供独立交换格式，主要依赖作者定义的 token 结构与 `SRI` 口径。
- 仿真/执行支持：toy pick-up truck 协作装配用例。
- 验证/分析支持：任务级 `SRI` 评估、不同 interaction modality 下的风险比较。
- 代码生成/转换支持：原文未提供自动代码生成。
- 标准化或社区生态：与 `ISO`/`CE` 等安全流程有关系，但论文主体不是标准实现，而是 `PN` 控制框架。

## 适用场景与需求前提

### 适用场景

适合工业装配中的 human-robot collaboration，尤其是需要在每个 task step 动态调整风险评估和协作模式的场景。

### 需求前提

1. 协作过程可以分解成有限 task steps。
2. 每一步的 components、actions、tools 和 interaction modality 可枚举。
3. 机器人侧存在可调整参数，如 speed/force。
4. 组织愿意引入任务级安全闭环，而不是只做静态整线评估。

### 不适用或高成本场景

如果系统安全风险主要来自高速连续动力学、复杂人类不可预测行为或难以离散化的环境条件，这种 `PN + SRI` 骨架会显得过粗。

## 与相邻形式主义的关系

相对 [Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes](../towards-safety4-0-flexible-human-robot-interaction-based-on-safety-related-dynamic-finite-state-machine-with-multilayer-operation-modes/desc.md)，本文不是 multilayer FSM，而是并发 `PN` 安全控制回路；相对 [A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks](../a-hierarchical-finite-state-machine-based-task-allocation-framework-for-human-robot-collaborative-assembly-tasks/desc.md)，它更聚焦 task safety than task allocation；相对 [Human-Robot Collaborative Assembly Based on Eye-Hand and a Finite State Machine in a Virtual Environment](../human-robot-collaborative-assembly-based-on-eye-hand-and-a-finite-state-machine-in-a-virtual-environment/desc.md)，本文把人机协作的安全评估闭环显式化了。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：在人机协作装配中，如果需求核心是“并发任务 + 动态安全评估”，Petri 网比普通状态机更适合作为高层控制骨架。

### 作为目标形式主义还是中间表示

对 `HRC` 安全控制问题，它可以直接作为目标形式主义；对一般状态机生成任务，它也可作为“安全与任务并发子系统”的中间表示。

### 对需求到模型生成的启发

1. 应把 components、actions、tools、interaction modality 和风险指标一起抽出来，而不是只抽状态。
2. 人和机器人并不一定共享同一控制方式，模型需要体现“机器人可调参、人类可告知”的不对称性。
3. 安全阈值与任务步骤的耦合关系很适合通过 token 结构和 guard 自动生成。

### 现实限制

它当前主要是概念验证级应用，离大规模工业 `HRC` 系统的长期部署还需要更强的感知、验证和工具链支撑。

## 重要的相关工作

- [Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes](../towards-safety4-0-flexible-human-robot-interaction-based-on-safety-related-dynamic-finite-state-machine-with-multilayer-operation-modes/desc.md)：用 `FSM` 处理 `HRI/HRC` 安全模式。
- [A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks](../a-hierarchical-finite-state-machine-based-task-allocation-framework-for-human-robot-collaborative-assembly-tasks/desc.md)：聚焦任务分配与 workload，而非安全控制。
- [Human-Robot Collaborative Assembly Based on Eye-Hand and a Finite State Machine in a Virtual Environment](../human-robot-collaborative-assembly-based-on-eye-hand-and-a-finite-state-machine-in-a-virtual-environment/desc.md)：展示 `HRC` 任务流程的另一类状态机载体。

## 文献分类总结

- 这是一篇 `🕸️` 类应用条目，核心是用 `Petri Net` 把人、机器人和协作任务的安全控制回路组织成可并发执行的模块化结构。
- 其描述客体是并发协作过程，因此记为 `🏭`；论文语境落在工业装配与 `HRC` 安全，因此记为 `🏭`。
- 对 `project_1` 来说，它补的是“并发网模型如何服务任务级安全闭环”的关键案例，而不是单纯的交互流程图。
