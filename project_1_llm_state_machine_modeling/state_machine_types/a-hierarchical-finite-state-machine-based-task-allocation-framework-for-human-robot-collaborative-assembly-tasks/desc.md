# 面向人机协同装配任务的层次有限状态机任务分配框架 / A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks

## 基本信息

- 标题：A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks
- 中文标题：面向人机协同装配任务的层次有限状态机任务分配框架
- 作者：Ilias El Makrini, Mohsen Omidi, Fabio Fusaro, Edoardo Lamon, Arash Ajoudani, Bram Vanderborght
- 发表：*2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2022)*, pp. 10238-10244
- DOI：`10.1109/IROS47612.2022.9981618`
- 链接：https://doi.org/10.1109/IROS47612.2022.9981618
- 形式主义：`HFSM Task Allocation`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：人机协同装配任务分配 / workload-aware `HFSM`
- 工具/实现获取方式：原文直接给出 `Franka Emika Panda`、`ROS`、`Matlab` master node、`Xsens` 动作捕捉、`MoveIt` 规划框架和文本指令界面；原文未提供公开代码仓库。
- 标准/格式获取方式：原文没有定义独立交换标准，主要承载方式是四模块层次状态机、任务 / 对象信息表、工作负载模型和 `MoveIt` 驱动的机器人执行接口。

## 简报

这篇论文把“任务分解、能力评估、工作负载控制、性能比较、实际执行”统一压成一套层次有限状态机框架。作者不是简单做一个 cost function，而是把 task selector、task allocator、communication instructor、task executor 全部建成 `HFSM` 的高层状态，从而让装配任务的分派、并行和干预都落在显式状态转移上。

- 形式主义定位：面向人机协同装配的层次任务分配状态机，其中装配主任务先被拆成子任务状态机，再依据 capability、availability、workload、performance 选择执行者。
- 构造方式简述：上层 `HFSM` 含四个主状态模块；任务选择器内部再嵌套装配子任务状态机，分配器内部再嵌 workload 与 performance 判定逻辑。
- 基础设施与场景简述：依托 `Panda` 协作机器人、`ROS`、`MoveIt`、`Xsens` 与文本指令界面，服务 smoothie machine crusher unit 的协同装配。

```text
装配任务 -> Task Selector HFSM -> Task Allocator HFSM -> Human Instruction / Robot Execution -> task_finished
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 基本有限状态机 `M = \{Q, q_0, F, \Sigma, E\}`。
2. 上层四模块状态：task selector、task allocator、communication instructor、task executor。
3. 任务分解结构，把总装配任务拆成 task、sub-task、elementary task。
4. capability 模型 `C_i`，判断 agent 是否能完成某任务。
5. workload 模型 `W`，通过人体虚拟弹簧能量积分估计作业负荷。
6. performance 模型，用预计任务时长选择更高效 agent。

### 核心抽象

论文直接给出了基本 `FSM` 定义：

$$
M = \{Q, q_0, F, \Sigma, E\}
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集合。
2. `q_0` 是初始状态。
3. `F` 是终止状态集合。
4. `\Sigma` 是有限输入字母表。
5. `E \subseteq Q \times \Sigma \times Q` 是状态转移集合。

基于此，整套任务分配框架可以保守整理为：

$$
\mathcal{H} = (M_{\mathrm{sel}}, M_{\mathrm{alloc}}, M_{\mathrm{instr}}, M_{\mathrm{exec}}, A, \Gamma, \Omega, P)
$$

上式中的符号逐项解释如下：

1. `M_{\mathrm{sel}}` 是 task selector 状态机。
2. `M_{\mathrm{alloc}}` 是 task allocator 状态机。
3. `M_{\mathrm{instr}}` 是 communication instructor 状态机。
4. `M_{\mathrm{exec}}` 是 robot task executor 状态机。
5. `A` 是 agent 集合，在本文中主要是 human 与 robot。
6. `\Gamma` 是 capability 信息，包括 payload、reach、gripper、对象重量等。
7. `\Omega` 是工作负载信息。
8. `P` 是 performance / duration 估计。

论文给出了 capability 计算公式：

$$
C_i = \prod_j c_j, \quad c_j = \prod_k c_{j,k}
$$

上式中的符号逐项解释如下：

1. `C_i` 是 agent `i` 对整项任务的 capability。
2. `c_j` 是第 `j` 个子任务的 capability。
3. `c_{j,k}` 是子任务 `j` 的第 `k` 个 elementary task 的 capability。
4. 若任一 `c_{j,k} = 0`，则对应子任务与总任务 capability 都会变成 `0`。

工作负载模型也由原文直接给出：

$$
E = \sum_i \frac{1}{2} k_i (\theta_i - \theta_i^\ast)^2
$$

以及：

$$
W = \frac{1}{T} \int_0^T (E(t) - E_L)\, dt
$$

上式中的符号逐项解释如下：

1. `E` 是当前人体姿态对应的虚拟弹簧总弹性能。
2. `k_i` 是第 `i` 个关节的虚拟弹簧刚度。
3. `\theta_i` 是该关节当前角度。
4. `\theta_i^\ast` 是人体工效学最优姿态下的自由角。
5. `W` 是累计工作负载。
6. `T` 是观测时间窗口。
7. `E_L` 是工作负载阈值对应的能量基线。

### 一个最小例子与通俗解释

一个最小例子是 crusher unit 装配中的 “pick and place motor attachment”：

1. task selector 把总装配流程拆成若干装配任务与子任务。
2. task allocator 检查 human 和 robot 当前是否空闲。
3. capability 模块检查两者是否都具备搬运该部件的能力。
4. 若 human 当前累计工作负载高于阈值，则该子任务直接分给 robot。
5. 若两者都可做且工作负载不过载，则由 performance 模块选择预计时间更短的 agent。
6. 分给 human 时，communication instructor 在屏幕上显示文本指令；分给 robot 时，task executor 调 `MoveIt` 和轨迹命令执行。

通俗地说，这个框架像一个“协作装配调度员”：

1. 先把整机装配拆开。
2. 再看谁能做。
3. 然后看人现在累不累。
4. 最后才决定让谁去做下一步。

### 运行 / 接受 / 转移语义

论文的高层运行链路可以整理为：

$$
\text{start} \rightarrow M_{\mathrm{sel}} \rightarrow M_{\mathrm{alloc}} \rightarrow (M_{\mathrm{instr}} \lor M_{\mathrm{exec}}) \rightarrow \text{task\_finished}
$$

上式中的符号逐项解释如下：

1. `start` 表示装配任务开始信号。
2. `M_{\mathrm{sel}}` 负责选出下一装配子任务。
3. `M_{\mathrm{alloc}}` 负责决定执行 agent。
4. `M_{\mathrm{instr}}` 在人类执行时生成文本指令。
5. `M_{\mathrm{exec}}` 在机器人执行时发出控制命令。
6. `task_finished` 把控制权送回 task selector 继续下一任务。

这也可以压缩成：

$$
a^\ast = \mathrm{Alloc}(C, W, P, \mathrm{Avail})
$$

上式中的符号逐项解释如下：

1. `a^\ast` 是最终选中的执行 agent。
2. `C` 是 capability 结果。
3. `W` 是当前 human workload。
4. `P` 是 performance / duration 估计。
5. `\mathrm{Avail}` 是 agent availability。

### 语义边界

这个模型的边界包括：

1. 它主要是 task allocation / cooperation logic，不是一般机器人任务语言。
2. 装配任务默认可拆成离散可分配子任务，不适合高度连续、不可分段的协作操作。
3. 工作负载模型只覆盖上半身虚拟弹簧能量，不等于完整人体工效学真值。
4. 机器人执行层依赖固定物体位置与 `MoveIt`，不是开放世界装配规划。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基本 `FSM` 定义 | `$M = \{Q, q_0, F, \Sigma, E\}$` | 任务分配框架的所有模块都以 `FSM` 方式组织。 |
| 上层框架骨架 | `$\mathcal{H} = (M_{\mathrm{sel}}, M_{\mathrm{alloc}}, M_{\mathrm{instr}}, M_{\mathrm{exec}}, A, \Gamma, \Omega, P)$` | 四模块 `HFSM` 统一组织任务分派与执行。 |
| capability 计算 | `$C_i = \prod_j c_j,\ c_j = \prod_k c_{j,k}$` | 任一 elementary task 不可做，整个任务 capability 即失败。 |
| workload 计算 | `$E = \sum_i \frac{1}{2} k_i (\theta_i-\theta_i^\ast)^2$`、`$W = \frac{1}{T} \int_0^T (E(t)-E_L) dt$` | 用人体姿态偏离最优工效学姿态的累积能量近似工作负载。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 任务选择、分配、指导、执行都是显式状态。 |
| 事件 / 触发 | 强支持 | `start`、`newtask`、`task_finished`、`nomore_task` 等都是主触发。 |
| 守卫 / 数据 | 强支持 | capability、availability、workload、performance 都作为 guard。 |
| 层次 | 强支持 | 装配主任务、子任务与 elementary task 是典型多层结构。 |
| 并发 / 同步 | 中等支持 | 文中明确利用并行任务提升总装配时间。 |
| 时间约束 | 弱支持 | 有任务时长估计，但无显式时钟自动机语义。 |
| 连续动态 / 随机性 | 弱支持 | 人体姿态与机器人轨迹在低层处理，高层主要是离散分配。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 在真实协作装配场景执行良好，但不是形式验证框架。 |

### 形式化问题与性质

1. 论文真正贡献的是把 agent 选择逻辑本身建模成 `HFSM`，而不仅是给出一个打分函数。
2. capability、workload、performance 三类信息被显式嵌入状态机决策节点，因此后续可追踪、可调阈值。
3. 对装配任务而言，把“pick / place / screw / sub-assembly”做成状态机结构，比纯表格式任务清单更容易承载并发与回填。
4. 对自动建模任务来说，这说明需求文本里的“谁做、何时交接、何时让 robot 接管”都应进入模型。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先把装配任务分解成 task / sub-task / elementary task。
2. 用任务选择器把装配流程表达成状态机序列和并行分叉。
3. 用对象表和 agent 表描述 capability 所需的静态属性。
4. 用 workload 和 performance 模块给 task allocator 提供 guard。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `HFSM` 图结构。
2. task / object / agent 信息表。
3. `ROS` + `Matlab` + `MoveIt` 控制链。
4. 文本指令界面与 Xsens 人体关节数据流。

### 交换与互操作

互操作重点在：

1. task selector 把新任务传给 task allocator。
2. task allocator 把 agent 选择结果传给 instruction 或 executor 分支。
3. `Xsens` 实时更新人体姿态，从而更新 workload。
4. `MoveIt` 把对象位置映射成 Panda 关节轨迹。

## 配套基础设施

- 建模/编辑工具：`HFSM` 任务图、`Matlab` master node、`ROS`。
- 解析/交换/元模型支持：任务 / 对象 / agent 信息表、文本指令接口和工作负载数据流。
- 仿真/执行支持：`Franka Emika Panda`、`MoveIt`、`Xsens`、固定工位装配台与 kitting trays。
- 验证/分析支持：论文通过 crusher unit 协同装配、不同 workload threshold 和装配时间统计验证框架效果。
- 代码生成/转换支持：原文未强调自动代码生成，主要依赖 `MoveIt` 轨迹规划和 ROS 执行。
- 标准化或社区生态：依托 `ROS` / `MoveIt` / `IROS` 协作机器人研究生态，但该分配框架本身不是标准。

## 适用场景与需求前提

### 适用场景

适合人机协同装配、工位协同搬运、需要显式考虑人体负荷和并行作业效率的制造任务。

### 需求前提

1. 主任务能够分解成离散可分配子任务。
2. human 与 robot 的能力差异可由表格化属性刻画。
3. human workload 可被传感器或外部模型估计。
4. 机器人执行端具备稳定的对象位姿与轨迹规划条件。

### 不适用或高成本场景

如果任务高度依赖实时协商、开放世界感知或复杂多人多机协作，这套两 agent、固定工位、表格化 capability 的 `HFSM` 会显得过于简化。

## 与相邻形式主义的关系

相对行为树，它更强调装配任务的显式状态与交接点；相对单纯优化式 task allocation，它把分配逻辑变成可解释、可回填的状态机；相对协议导向多 agent 模型，它不关注 message protocol，而更关注装配子任务与 human workload。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的价值很高，因为它展示了**需求中的 agent roles、能力约束、疲劳约束和性能目标**如何一起落成状态机。

### 作为目标形式主义还是中间表示

它更适合作为人机协同装配系统中的高层目标执行载体，也可以作为从需求文本通往更具体执行状态机的中间规格层。

### 对需求到模型生成的启发

1. 需求抽取时不能只抽动作，还要抽 agent 能力和任务交接逻辑。
2. 对协作任务，workload / ergonomics 约束可以直接变成转移 guard。
3. 若未来要做生成-验证-修复闭环，这种 `HFSM` 很适合作为高层协调模型。

## 重要的相关工作

- `MoveIt`：机器人执行端的路径 / 关节映射基础设施。
- `Xsens`：工作负载模型的数据来源。
- `REBA`：人体工效学自由姿态设定的依据。
- 行为树 / 决策树 / MDP 任务分配路线：论文在相关工作中明确对照的替代方案。

## 文献分类总结

- 这是一篇 `📦` 类人机协同装配条目，重点是把 task allocation、workload 约束和 robot execution 统一进 `HFSM`。
- 它描述的核心客体是控制 / 反应式协作逻辑，因此记为 `🎛️`；应用语境明确是制造装配，因此领域记为 `🏭`。
- 对 `project_1` 来说，它补的是“人机协作装配需求如何落成层次状态机分配框架”的实例证据。
