# 基于二分分解的通信优先机器人系统自顶向下设计 / Communication-Focused Top-Down Design of Robotic Systems Based on Binary Decomposition

## 基本信息

- 标题：Communication-Focused Top-Down Design of Robotic Systems Based on Binary Decomposition
- 中文标题：基于二分分解的通信优先机器人系统自顶向下设计
- 作者：Piotr Pałka, Cezary Zieliński, Wojciech Dudek, Dawid Seredyński, Wojciech Szynkiewicz
- 发表：*Energies*, 15(21):7983, 2022
- DOI：`10.3390/en15217983`
- 链接：https://doi.org/10.3390/en15217983
- 形式主义：`Embodied Agent / Binary Decomposition + FIPA HFSM`
- 主类：📦
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：通信优先设计方法 / agent-FSM 规格
- 工具/实现获取方式：原文明确说明系统以 `ROS 1` nodes 和 `RPC` 机制实现，并把 `ClassInterfaceInfo` 等通信模块作为可复用代码单元；论文未稳定给出公开仓库。
- 标准/格式获取方式：承载方式直接依赖 `IEEE FIPA ACL` message structure、`LHFSM/LSW/LWM` 内容语言、`OWL` 环境本体和各 agent 的 `FSM` 规格；不是单一 XML 文件标准。

## 简报

这篇论文的贡献不是单独发明一个新 `FSM` 语义核，而是提出一种“先按任务二分分解系统，再把通信结构固定下来”的机器人系统设计方法。作者把机器人系统视为 embodied agents 的组合，先通过 requirements tree 做 binary decomposition，再把 agent 之间的消息统一写成 `FIPA ACL` 风格的 communicates，最后为各 agent 的控制子系统指定 `FSM/HFSM`。对本 collection 来说，它补的是一种很少见但非常有价值的路线：状态机不只是任务图，还可以成为以通信为中心的系统规格组成部分。

- 形式主义定位：面向 embodied-agent 机器人系统的 top-down 规格方法，其中 communication channel、interaction protocol 和 agent `FSM` 共同构成控制骨架。
- 构造方式简述：先对系统做 binary decomposition，再指定 channels 和 protocols，最后为各 agent 的 control subsystem 建立 `FSM/HFSM`。
- 基础设施与场景简述：依托 `IEEE FIPA ACL`、`ROS 1`、`OWL` world model、`HFSM` plan notation 和 `ROS` services，服务 companion robot 等多 agent 机器人系统。

```text
requirements tree -> binary decomposition -> agent groups + channels -> FIPA protocols -> agent FSMs / HFSM plans -> ROS implementation
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. agent `a_j`：embodied agent。
2. agent group `a_g^q`：尚未细化完成的 agent 组。
3. communication channel `C_{q,q'}^k`：组或 agent 之间的通信通道。
4. interaction protocol `I`：规定一类 conversation 的消息交换顺序。
5. communicate `M^i_{j,j'}`：在时刻 `i` 发送的消息。
6. `LHFSM`：用于 plan/task 的层次状态机内容语言。
7. `LSW`：用于 worker 状态汇报的语言。
8. `LWM`：用于 world model 查询和回答的语言。
9. control subsystem `c_j`：agent 内负责通信与决策的核心控制子系统。
10. `FSM cF_j`：control subsystem 的行为状态机。

### 核心抽象

从论文方法层面，可把最终系统规格保守整理为：

$$
\mathcal{R} = (\hat a, \hat C, \hat I)
$$

上式中的符号逐项解释如下：

1. `\hat a` 是经过分解后得到的 agents 集合。
2. `\hat C` 是通信通道集合。
3. `\hat I` 是与各通道绑定的 interaction protocols 集合。

论文明确规定二分分解步骤，因此 group 分解可直接表示为：

$$
a_g^q := \langle a_g^p, a_g^r \rangle
$$

上式中的符号逐项解释如下：

1. `a_g^q` 是当前待分解的 group。
2. `a_g^p` 与 `a_g^r` 是分解后得到的两个子 group。
3. 这一步反复执行，直到 requirements 被充分下沉。

对消息结构，论文给出完整 tuple，可直接保留为：

$$
M^i_{j,j'} = \langle V, Z, L, O, I, t_b, m_w, m_t, m_c \rangle
$$

上式中的符号逐项解释如下：

1. `V` 是 performative verb，例如 `request`、`inform`、`cancel`。
2. `Z` 是 message content。
3. `L` 是表达内容的语言，如 `LHFSM`、`LSW`、`LWM`。
4. `O` 是 ontology。
5. `I` 是 interaction protocol。
6. `t_b` 是 reply-by 时间戳。
7. `m_w`、`m_t` 分别对应 reply-with 和 in-reply-to 标识。
8. `m_c` 是 conversation 标识。

论文还给出了 control subsystem 的离散更新关系，可保守压缩为：

$$
(c c^{i+1}_j, {}^e y^{i+1}_j, {}^r y^{i+1}_j, {}^T y^{i+1}_j) = {}^c f_{j,m}(c c^i_j, {}^e x^i_j, {}^r x^i_j, {}^T x^i_j)
$$

上式中的符号逐项解释如下：

1. `c c^i_j` 是 agent `a_j` 控制子系统在时刻 `i` 的内部记忆。
2. `{}^e x^i_j`、`{}^r x^i_j`、`{}^T x^i_j` 分别是来自 effectors、receptors 和 transmission buffer 的输入。
3. `{}^e y^{i+1}_j`、`{}^r y^{i+1}_j`、`{}^T y^{i+1}_j` 是下一时刻写出的输出。
4. `{}^c f_{j,m}` 是当前行为对应的 transition function。

### 一个最小例子与通俗解释

论文的 companion robot 例子很适合直观理解：

1. coordinator agent `a_co` 决定当前应该执行哪个任务。
2. task agent `a_ta` 接收一个用 `LHFSM` 表达的 plan。
3. `a_ta` 执行 plan 时，周期性用 `LSW` 回报 `Idle/Running/Error/...` 等状态。
4. 如果 `a_co` 需要中断当前 plan，就发送 `cancel`。

通俗地说，这个方法像“先把机器人系统按职责拆开，再把每条消息都写规矩，最后才给每个 agent 配自己的状态机”。它不是从现成模块开始拼，而是先把 communication 规格写清楚。

### 运行 / 接受 / 转移语义

论文明确指出，每个 agent 的 control subsystem 由 `FSM` 驱动，行为切换由 terminal condition 和 initial condition 决定，可保守表示为：

$$
cF_j = (cS_j, cB_j, cfs_j)
$$

上式中的符号逐项解释如下：

1. `cS_j` 是 agent `a_j` 控制子系统的状态集合。
2. `cB_j` 是与各状态绑定的 behaviours。
3. `cfs_j` 是初始条件/切换条件集合。

通信驱动的服务执行过程可写成：

$$
cS^m_j \xrightarrow{M^i_{j',j}} cS^{m'}_j \iff cfs_{j,m,m'}(M^i_{j',j}) = \mathrm{true}
$$

上式中的符号逐项解释如下：

1. `M^i_{j',j}` 是别的 agent 发给 `a_j` 的消息。
2. `cfs_{j,m,m'}` 是从状态 `m` 到 `m'` 的初始条件。
3. 当消息满足条件时，control subsystem 切换到新的 behaviour。

### 语义边界

这套方法的边界也很清楚：

1. 它首先是一种系统规格与分解方法，其次才是某个单一 `FSM` 方言。
2. 它默认系统可自然分解成 embodied agents，并且通信是首要设计关注点。
3. 它没有把所有机器人逻辑都塞进一个总状态机，而是用 agent + protocol + local FSM 组合表达。
4. 它很适合面向多 agent 通信和任务执行的机器人，不适合极小型单体控制器。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 规格骨架 | `$\mathcal{R} = (\hat a, \hat C, \hat I)$` | 系统由 agents、channels 和 protocols 组成。 |
| 二分分解 | `$a_g^q := \langle a_g^p, a_g^r \rangle$` | requirements 驱动的 top-down 分解是设计主线。 |
| 消息结构 | `$M^i_{j,j'} = \langle V, Z, L, O, I, t_b, m_w, m_t, m_c \rangle$` | 通信内容被严格标准化。 |
| 控制子系统更新 | `$(c c^{i+1}_j, {}^e y^{i+1}_j, {}^r y^{i+1}_j, {}^T y^{i+1}_j) = {}^c f_{j,m}(\cdots)$` | 通信输入会影响控制子系统的全部活动。 |
| 消息驱动切换 | `$cS^m_j \xrightarrow{M^i_{j',j}} cS^{m'}_j$` | agent FSM 对通信消息作出反应。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个 control subsystem 都由 `FSM` 驱动。 |
| 事件 / 触发 | 强支持 | 核心触发物就是标准化 messages。 |
| 守卫 / 数据 | 强支持 | performative、content、language、ontology 共同决定状态切换。 |
| 层次 | 强支持 | 同时存在 group decomposition 和 `HFSM` task 表达。 |
| 并发 / 同步 | 强支持 | 多 agent 通过协议并发协作。 |
| 时间约束 | 弱支持 | 有 reply-by 与 sampling time，但不是显式 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 论文关注离散规格和通信结构。 |
| 可执行 / 可验证性 | 强执行、较强可验证 | 有 `ROS 1` 实现，并强调 deadlock / protocol verification。 |

### 形式化问题与性质

1. 这篇论文最值得保留的是“先定通信，再定实现”的方法论，而不是某一张具体状态图。
2. `FIPA ACL` 风格的 message tuple 让状态机 guard 不再只是本地条件，也能显式依赖 conversation 结构。
3. `HFSM` 在这里主要承担 task content language，而不是唯一控制器载体。
4. binary decomposition 使复杂机器人系统的规格和后续死锁分析更容易局部化。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 从 requirements tree 出发识别系统任务。
2. 用 binary decomposition 把系统拆成 agent groups。
3. 为 groups/agents 建立 communication channels。
4. 为每个 channel 指定 interaction protocols 和消息语言。
5. 最后给每个 control subsystem 建立 `FSM/HFSM`。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `FIPA ACL` message tuple。
2. `LHFSM`、`LSW`、`LWM` 三类内容语言。
3. `OWL` world model ontology。
4. agent control subsystem 的 `FSM` 图。
5. `ROS 1` services / RPC 代码实现。

### 交换与互操作

互操作重点在：

1. communication channel 最终会被转换为 pairs of input/output buffers。
2. interaction protocol 规定消息顺序，而不仅是字段结构。
3. 论文用统一的 `ClassInterfaceInfo` 把 specification 与 implementation 对齐。
4. 同一 channel 可承载多个 protocol，适合多类 conversation 共存。

## 配套基础设施

- 建模/编辑工具：论文主要给出 formal notation、requirements tree、agent FSM 和 message specification。
- 解析/交换/元模型支持：`FIPA ACL`、`OWL`、`LHFSM/LSW/LWM` 是最核心的机器可处理承载。
- 仿真/执行支持：系统在 `ROS 1` 中实现，agents 被实现为 ROS nodes。
- 验证/分析支持：论文强调 communication deadlock analysis，可借助 `Colored Petri Nets` 等手段。
- 代码生成/转换支持：未强调自动代码生成，但通信部分被抽成可复用模块。
- 标准化或社区生态：高度依赖 `IEEE FIPA` 通信口径，具备很强的多 agent 互操作导向。

## 适用场景与需求前提

### 适用场景

适合 companion robot、多 agent 服务机器人、任务协调系统，以及任何 communication structure 本身就是关键设计对象的机器人系统。

### 需求前提

1. 系统能够自然分解成多个 embodied agents。
2. 任务和需求可先表达成 requirements tree。
3. 设计者愿意把 communication channels 和 protocols 显式规格化。
4. 任务执行内容能够用 `HFSM` 或相近任务语言表达。

### 不适用或高成本场景

如果系统非常小、通信极少、或更像单一控制器，这种方法会显得偏重；它更适合复杂协同系统，而不是单节点状态机。

## 与相邻形式主义的关系

相对 `LLFSM + Whiteboard`，它把通信写得更规范、更 protocol 化；相对 `CFSM`，它不是纯通信理论模型，而是系统设计方法；相对 `SMACH/FlexBE`，它更关注 system specification 和 message structure，而不是单一运行时。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的价值很高，因为它说明“需求到状态机”的过程不一定只产出一个控制器图，也可以先产出一套 communication-aware system specification。

### 作为目标形式主义还是中间表示

它更适合作为复杂机器人系统的中间规格层或高层目标架构，而不是最后交付给最终用户的一张执行图。

### 对需求到模型生成的启发

1. 需求里的 communication acts、roles 和 conversations 应该被显式建模。
2. 对多 agent 系统，状态机生成应和 protocol 生成同步进行。
3. 如果系统最终要验证死锁或协议一致性，那么 message structure 从一开始就必须标准化。

## 重要的相关工作

- `IEEE FIPA ACL Message Structure Specification`：消息字段和 performative 直接来源。
- `HFSM`：任务内容语言的重要承载。
- `OWL` / world model：支撑知识查询与回答。
- `Communication Within Multi-FSM Based Robotic Systems`：与其形成对照的另一种机器人通信状态机路线。

## 文献分类总结

- 这是一篇 `📦` 类通信优先规格条目，重点在 requirements-driven decomposition、protocol specification 与 agent `FSM` 的联合设计。
- 它主要描述交互契约与消息协同，因此记为 `🤝`；虽然场景是机器人，但研究语境明显偏通信/协议与分布式交互，因此领域记为 `🌐`。
- 对 `project_1` 来说，它补的是“需求如何先转为 agent / channel / protocol / FSM 联合结构”的系统化证据。
