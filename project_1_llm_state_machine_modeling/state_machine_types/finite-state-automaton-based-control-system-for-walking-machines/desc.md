# 面向步行机器的有限状态自动机控制系统 / Finite State Automaton Based Control System for Walking Machines

## 基本信息

- 标题：Finite state automaton based control system for walking machines
- 中文标题：面向步行机器的有限状态自动机控制系统
- 作者：Razeen Hussain, Teresa Zielińska, Rene Hexel
- 发表：*International Journal of Advanced Robotic Systems*, 16(3), 2019
- DOI：`10.1177/1729881419853182`
- 链接：https://doi.org/10.1177/1729881419853182
- 形式主义：`LLFSM Walking Controller`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：步行机实时控制架构 / `LLFSM` 应用载体
- 工具/实现获取方式：原文直接给出 `QNX` 实时操作系统、`MiEditLLFSM` 建模工具、whiteboard 通信机制与六足机器人实验；原文未提供独立代码仓库。
- 标准/格式获取方式：原文没有定义独立 `XML/JSON` 交换格式，主要承载方式是 `MiEditLLFSM` 的图式状态机、whiteboard 数据仓、分层 `FSM` 与 `QNX` 上的模块化进程。

## 简报

这篇论文的核心贡献，不是提出新的自动机理论，而是把步行机器里最难维护的一类实时控制问题压成一套可分层、可同步、可重用的 `LLFSM` 结构。作者把全局导航、局部导航、步态切换和执行层拆成多个有限状态自动机，再用 whiteboard 共享状态，避免了传统 `send/receive/reply` 式同步过程把逻辑写成难维护的并发消息网。

- 形式主义定位：面向步行机器人实时控制的逻辑标注有限状态机体系，其中每个控制子系统都被实现为一个独立 `FSM`，上层负责任务与路径，下层负责步态与执行。
- 构造方式简述：以 `MiEditLLFSM` 图式状态机为入口，把全局导航、局部导航、步态子行为和数据仓组织成分层 `FSM + whiteboard` 架构。
- 基础设施与场景简述：依托 `QNX RTOS`、`MiEditLLFSM`、传感器仓和 gait library，服务六足/多足步行机器在未知环境中的导航、避障与步态切换。

```text
任务需求 -> Global Navigation FSM -> Local Navigation FSM -> Gait Sub-FSM -> Actuation Control
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 全局导航自动机 `\mathcal{M}_g`，负责任务初始化、用户交互、航点管理和误差监控。
2. 局部导航自动机 `\mathcal{M}_l`，负责避障、转向、目标装载与停止逻辑。
3. 子行为 / 步态自动机 `\mathcal{M}_s`，负责 tripod gait 与 wave gait 的切换与执行。
4. whiteboard 数据仓 `R_b`，用于存放 waypoint、sensor、status 等共享数据。
5. 转移条件 `f_c`，由前向障碍、航向误差、地面倾角、系统故障等布尔条件触发。
6. `MiEditLLFSM` 状态节点中的 `OnEntry / Internal / OnExit` 三段动作语义。

### 核心抽象

原文没有把整套步行机控制架构写成单一总元组，但论文给出了 `S_a^d`、`R_b`、`f_c` 等符号口径。根据这些口径，可把系统保守整理为：

$$
\mathcal{W} = (\mathcal{M}_g, \mathcal{M}_l, \{\mathcal{M}_s^\gamma\}_{\gamma \in G}, R, F, \Lambda)
$$

上式中的符号逐项解释如下：

1. `\mathcal{M}_g` 是全局导航有限状态机。
2. `\mathcal{M}_l` 是局部导航有限状态机。
3. `G` 是步态集合，例如 tripod 与 wave。
4. `\mathcal{M}_s^\gamma` 是步态 `\gamma` 对应的子行为状态机。
5. `R = \{R_b\}` 是 whiteboard 上的数据仓集合。
6. `F = \{f_c\}` 是由传感器和状态仓导出的转移条件集合。
7. `\Lambda` 表示分层自动机之间通过 whiteboard 共享数据并向下发送 demand 的连接关系。

单个 `LLFSM` 的一步转移可保守写成：

$$
S_{t+1}^d = T_d(S_t^d, R_t, F_t), \quad d \in \{g, l, s\}
$$

上式中的符号逐项解释如下：

1. `S_t^d` 是第 `d` 个层级自动机在时刻 `t` 的当前状态。
2. `R_t` 是时刻 `t` whiteboard 中可读的数据仓值。
3. `F_t` 是由 `R_t` 计算得到的布尔转移条件集合。
4. `T_d` 是该层级自动机的转移函数。
5. `S_{t+1}^d` 是转移后的下一状态。

对局部导航层，原文可直接对应到如下状态集合：

$$
Q_l = \{SloadTarget_l, SmoveFwd_l, SmoveLeft_l, SmoveRight_l, SturnLeft_l, SturnRight_l, Sstop_l\}
$$

上式中的符号逐项解释如下：

1. `SloadTarget_l` 表示装载下一航点。
2. `SmoveFwd_l` 表示向前行进。
3. `SmoveLeft_l` 与 `SmoveRight_l` 表示绕障侧移。
4. `SturnLeft_l` 与 `SturnRight_l` 表示航向修正。
5. `Sstop_l` 表示停机或任务结束。

### 一个最小例子与通俗解释

一个最小工作流是：

1. 用户输入新的目标航点。
2. 全局导航 `\mathcal{M}_g` 从 `SwaitUser_g` 进入 `SinitMotion_g`，把目标写入 whiteboard。
3. 局部导航 `\mathcal{M}_l` 读取目标后进入 `SmoveFwd_l`。
4. 若前向传感器检测到障碍，则 `f_{\text{front\_obs}}` 变为真，状态转到 `SmoveLeft_l` 或 `SmoveRight_l`。
5. 若地面条件要求更稳定步态，则步态子自动机从 tripod 子状态机切到 wave 子状态机。
6. 到达目标后再回到 `SloadTarget_l` 请求下一个目标。

通俗地说，这个系统像一个“三层行走班组长”：

1. 最上层决定“去哪”。
2. 中间层决定“怎么绕过去、什么时候转向”。
3. 最下层决定“此刻到底用哪种步态迈腿”。

它比单张扁平状态图多出的关键结构，是**导航状态机之下还挂着步态状态机**，并且所有层通过 whiteboard 共享环境与任务状态。

### 运行 / 接受 / 转移语义

论文的运行语义可以压缩成“上层 demand 下发 + 下层 whiteboard 条件驱动”的同步调度：

$$
\mathcal{M}_g \xrightarrow{\text{waypoint/status}} \mathcal{M}_l \xrightarrow{\text{gait demand}} \mathcal{M}_s \xrightarrow{\text{body trajectory}} u_t
$$

上式中的符号逐项解释如下：

1. `\mathcal{M}_g` 负责产生命令级目标与状态监控。
2. `\mathcal{M}_l` 把目标转成局部机动和避障状态。
3. `\mathcal{M}_s` 把局部机动状态转成具体步态行为。
4. `u_t` 是发送到执行层的 body trajectory 或运动需求。

`MiEditLLFSM` 的节点语义则可保守整理为：

$$
\mathrm{Exec}(q) = (\mathrm{OnEntry}(q), \mathrm{Internal}(q), \mathrm{OnExit}(q))
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态节点。
2. `\mathrm{OnEntry}(q)` 是进入状态时执行一次的动作。
3. `\mathrm{Internal}(q)` 是在没有触发转移前循环执行的动作。
4. `\mathrm{OnExit}(q)` 是离开状态时执行一次的动作。

这说明该系统不是把所有行为写在 transition 上，而是把“进入、停留、退出”三种动作职责显式分开。

### 语义边界

这个模型的边界很明确：

1. 它是步行机器人控制架构，不是一般自动机理论条目。
2. 它重在同步反应式控制和模块通信，不讨论语言接受性或复杂度理论。
3. 它依赖 whiteboard 与 `MiEditLLFSM` 的执行框架，不能简单等同于任意 `FSM` 代码。
4. 逆运动学和执行器细节被下沉到 actuation control，不由上层状态机直接展开。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 分层控制骨架 | `$\mathcal{W} = (\mathcal{M}_g, \mathcal{M}_l, \{\mathcal{M}_s^\gamma\}, R, F, \Lambda)$` | 全局导航、局部导航和步态控制被拆成可复用层级。 |
| 单层转移 | `$S_{t+1}^d = T_d(S_t^d, R_t, F_t)$` | 每层状态推进都由 whiteboard 数据和布尔条件驱动。 |
| 局部导航状态集 | `$Q_l = \{SloadTarget_l,\ldots,Sstop_l\}$` | 避障、转向、停机等机动被明确离散化。 |
| 节点执行语义 | `$\mathrm{Exec}(q) = (\mathrm{OnEntry}, \mathrm{Internal}, \mathrm{OnExit})$` | `LLFSM` 强调状态节点内部动作而不仅是边标签。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 全局导航、局部导航和步态层都有清晰状态集合。 |
| 事件 / 触发 | 强支持 | 障碍、航向误差、系统故障、用户请求等都是显式 guard。 |
| 守卫 / 数据 | 强支持 | 通过 whiteboard 数据仓和布尔条件 `f_c` 触发转移。 |
| 层次 | 强支持 | 局部导航之下还嵌有 gait sub-FSM。 |
| 并发 / 同步 | 中等支持 | 多 `FSM` 同步执行，但强调单线程时间片和共享仓，不是完全异步事件风格。 |
| 时间约束 | 中等支持 | 面向 `RTOS` 与实时反应，但没有把时间约束形式化为时钟自动机。 |
| 连续动态 / 随机性 | 弱支持 | 连续运动由轨迹与执行层处理，状态机层只管理离散控制阶段。 |
| 可执行 / 可验证性 | 强执行、有限验证 | `MiEditLLFSM + QNX` 可执行性强，但论文重点不是模型检查。 |

### 形式化问题与性质

1. 论文真正解决的是“如何把大型步行机控制逻辑拆成同步、可维护的层次 `FSM`”，而不是提出新 gait planner。
2. `LLFSM` 的价值在于把 transition condition 从消息序列里解耦出来，直接挂到布尔 guard 和数据仓上。
3. 步态切换被纳入下层子自动机，而不是散落在 if-else 或 RTOS 线程同步中。
4. 对需求建模而言，这类控制器很适合把“任务层需求”“机动层需求”“步态层需求”分别生成。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 用分层控制结构划分全局导航、局部导航、执行控制与步态子行为。
2. 用 `MiEditLLFSM` 图式状态机定义节点、布尔 guard 和节点动作。
3. 用 whiteboard 定义 status repository、sensor repository、waypoint repository 等共享数据仓。
4. 用 gait library 把 tripod / wave 等周期步态挂接到下层子状态机。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `MiEditLLFSM` 中的节点 / 弧表示。
2. `OnEntry / Internal / OnExit` 三段状态动作。
3. whiteboard 数据仓与命名变量。
4. `QNX` 下分布式模块和 `RTOS` 进程。

### 交换与互操作

互操作重点在：

1. 上层把 demand 写入下层需要读取的数据仓。
2. 传感器与状态误差通过 whiteboard 共享，而不是靠阻塞消息层层传递。
3. 步态子行为机可作为局部导航机的嵌套状态复用。
4. 控制结构可在多微处理器网络上分布部署。

## 配套基础设施

- 建模/编辑工具：`MiEditLLFSM` 图式建模工具。
- 解析/交换/元模型支持：whiteboard 数据仓、状态命名与布尔 guard 共同形成机器可处理结构；原文未给独立元模型标准。
- 仿真/执行支持：`QNX RTOS`、六足机器人实验平台、传感器仓与 gait execution。
- 验证/分析支持：论文通过仿真和实验场景验证避障与步态切换；未提供单独模型检查链路。
- 代码生成/转换支持：原文重心是 `LLFSM` 执行框架和实时控制，不强调自动代码生成。
- 标准化或社区生态：依托 `LLFSM` / statecharts 路线与 `QNX` 实时控制生态，但该载体本身不是通用国际标准。

## 适用场景与需求前提

### 适用场景

适合六足/多足步行机器、未知地形导航、需要障碍绕行和步态切换的实时移动机器人控制系统。

### 需求前提

1. 任务可以自然分解成全局任务、局部机动和步态执行三个层次。
2. 传感器读数、航向误差和系统状态能够转成显式布尔 guard。
3. 系统需要实时响应，但不需要显式时钟自动机那种时间语义。
4. 步态库和执行层已存在，状态机主要负责组织何时调用它们。

### 不适用或高成本场景

如果系统几乎没有明显模式切换、也不需要步态层复用，那么分层 `LLFSM` 会偏重；若任务需要显式连续动力学验证，则还需要与更强的混成 / 时间模型联合。

## 与相邻形式主义的关系

相对传统异步事件驱动 `FSM`，这篇更强调同步时间片执行与 whiteboard 共享数据；相对纯 `Statecharts` 语义论文，它把层次与节点动作直接落到步行机控制；相对行为树，它更适合明确 guard 密集、状态模式稳定且 RTOS 友好的机动控制逻辑。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很有代表性，因为它说明“需求到状态机”并不一定只得到一张控制图，而可能得到一套**分层状态机族**：任务层、机动层、步态层各司其职。

### 作为目标形式主义还是中间表示

它更适合作为步行机器控制软件中的目标执行载体，而不是通用中间表示。

### 对需求到模型生成的启发

1. 需求里的 mission、navigation、gait 应优先拆成多层状态机，而不是硬压成扁平单图。
2. 自动生成时要同步生成状态仓和 guard，而不能只生成状态节点名称。
3. 若后续要做验证与修复，whiteboard 里的共享变量集合本身就是需要建模的对象。

## 重要的相关工作

- `MiEditLLFSM`：本文的核心执行 / 建模工具。
- `QNX RTOS`：为实时控制和分布式部署提供执行环境。
- Harel `Statecharts`：作者明确提到其为 `LLFSM` 建模提供语义背景。
- Zielińska 等步行机器实时控制工作：构成论文分层控制设计的直接前史。

## 文献分类总结

- 这是一篇 `📦` 类实时步行机控制条目，重点是把 `LLFSM` 用作多层实时控制载体，而不是单独讨论 `FSM` 理论。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；语境以实时控制和嵌入式反应为中心，因此领域记为 `⏱️`。
- 对 `project_1` 来说，它补的是“分层状态机如何组织步行机器人 mission / navigation / gait 的工程化证据”。
