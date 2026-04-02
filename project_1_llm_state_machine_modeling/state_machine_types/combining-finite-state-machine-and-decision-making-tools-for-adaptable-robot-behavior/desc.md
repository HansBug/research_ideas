# 结合有限状态机与决策工具实现可适应机器人行为 / Combining Finite State Machine and Decision-Making Tools for Adaptable Robot Behavior

## 基本信息

- 标题：Combining Finite State Machine and Decision-Making Tools for Adaptable Robot Behavior
- 中文标题：结合有限状态机与决策工具实现可适应机器人行为
- 作者：Michalis Foukarakis, Asterios Leonidis, Margherita Antona, Constantine Stephanidis
- 发表：收录于 *Universal Access in Human-Computer Interaction. Aging and Assistive Environments*, Springer, 2014
- DOI：`10.1007/978-3-319-07446-7_60`
- 链接：https://doi.org/10.1007/978-3-319-07446-7_60
- 形式主义：`SMACH + DMSL Decision-Augmented FSM`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：服务机器人行为组合 / `SMACH + DMSL` 决策增强执行架构
- 工具/实现获取方式：原文直接给出 `SMACH` Python 状态机库、`DMSL` 决策规则语言，以及 `HOBBIT` 陪伴机器人上的落地场景；未提供独立公开代码仓库。
- 标准/格式获取方式：原文未定义统一交换标准，主要承载方式是 `SMACH` 层次状态机、`DMSL` 的 `if-then-else` 决策块、`activate/cancel` 命令和 user / robot / environment profile 参数。

## 简报

这篇论文的核心不是重新定义一种纯理论 `FSM`，而是说明在服务机器人里，**显式状态机和独立决策块可以分层协作**。作者把高层任务流程放进 `SMACH`，再把运行时“该沿哪个分支走”的适配逻辑放进 `DMSL`。这样，状态机保留任务结构，决策块则根据用户、环境和机器人自身参数决定该激活哪条转移。

- 形式主义定位：一种面向陪伴/服务机器人的“状态机骨架 + 外部决策块”组合模型，适合处理运行时适配。
- 构造方式简述：设计者先写 `SMACH` 任务状态图，再为关键状态挂接 `DMSL` 决策块，由 `activate "..."` 结果驱动转移。
- 基础设施与场景简述：依托 `HOBBIT` 陪伴机器人、导航与交互组件、用户画像和环境参数，服务找人、避障、是否请求帮助等任务。

```text
任务状态 -> 读取 user / robot / env profile -> DMSL 决策块 -> activate 某条转移 -> SMACH 下一状态
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. `SMACH` 层次状态机中的状态集合与转移集合。
2. `DMSL` 的 component-local decision block。
3. `user / robot / environment` 三类 profile 参数。
4. `activate / cancel` 命令。
5. 由决策块返回的 linguistic outcome，例如 `plan`、`help`。
6. `HOBBIT` 任务状态，例如 “locate user” 或 `OBSTRUCTED`。

### 核心抽象

按论文结构，可将其保守整理为一个“决策增强状态机”：

$$
\mathcal{B} = (Q, q_0, O, \delta, \Pi, \mathcal{D})
$$

上式中的符号逐项解释如下：

1. `Q` 是 `SMACH` 中的任务状态集合。
2. `q_0 \in Q` 是初始状态。
3. `O` 是可返回的 outcome 集合，例如 `plan`、`help`、`success`。
4. `\delta : Q \times O \to Q` 是基于 outcome 的状态转移关系。
5. `\Pi` 是运行时 profile 参数空间，包含 user、robot 和 environment 三类属性。
6. `\mathcal{D}` 是 `DMSL` 决策块集合，每个块把当前参数映射成一个激活命令。

对单个决策块，可进一步写成：

$$
d : \Pi \to O
$$

上式中的符号逐项解释如下：

1. `d \in \mathcal{D}` 是某个具体决策块。
2. `\Pi` 是该决策块读取到的 profile 参数赋值。
3. `O` 是该块返回的激活 outcome。

论文中 `OBSTRUCTED` 状态的例子可压缩为：

$$
d_{\mathrm{obs}}(\pi) =
\begin{cases}
\texttt{plan}, & \pi \models \neg hearing \lor age > 80 \lor bond \notin willingToBond \lor time \notin userFreeTimes \\
\texttt{help}, & \pi \models battery < 10 \lor currentBestPath = false \lor currentRoom = favoriteRoom
\end{cases}
$$

上式中的符号逐项解释如下：

1. `d_{\mathrm{obs}}` 是障碍情形下的决策块。
2. `\pi` 是当前用户、环境、机器人参数的联合赋值。
3. `\models` 表示“当前赋值满足该布尔条件”。
4. `\texttt{plan}` 表示优先自己重新规划路径。
5. `\texttt{help}` 表示请求用户协助或进行更显式的人机交互。

### 一个最小例子与通俗解释

最小例子可以直接用论文给出的 `OBSTRUCTED` 场景：

1. 机器人正在执行“找用户”任务。
2. 当前 `SMACH` 状态进入 `OBSTRUCTED`，说明前路受阻。
3. 状态本身并不直接写死“下一步一定重规划”或“一定求助”。
4. 系统读取 `params.user.*`、`params.robot.*` 和 `params.env.*`。
5. 若用户年纪较大、听力欠佳，或者当前不是合适打扰时段，则 `DMSL` 返回 `plan`，机器人自己重规划。
6. 若机器人电量太低、当前最佳路径不可用，或已经在用户喜爱的房间，则 `DMSL` 返回 `help`，状态机转去请求用户帮助。

通俗地说，这个模型像“状态机 + 插件化裁判”。状态机负责流程骨架，裁判根据现场情况裁定该走哪条边。

### 运行 / 接受 / 转移语义

其运行语义可保守写成：

$$
(q_t, \pi_t) \xrightarrow{d_q} o_t \xrightarrow{\delta} q_{t+1}
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前 `SMACH` 状态。
2. `\pi_t` 是当前运行时 profile 参数。
3. `d_q` 是与当前状态绑定的决策块。
4. `o_t` 是决策块返回的 outcome。
5. `q_{t+1}` 是按该 outcome 激活后的下一状态。

如果当前状态不需要运行时适配，则语义退化成普通状态机：

$$
q_{t+1} = \delta(q_t, o_t)
$$

其中 `o_t` 可能来自传感器回调、动作结果或固定 transition label。

### 语义边界

这个模型的边界包括：

1. `DMSL` 只负责局部决策，不替代完整规划器。
2. 状态机骨架仍需人工设计，论文没有给出自动生成方法。
3. 形式化重点是工程化可适配，而不是证明某类判定性或闭包性质。
4. 决策逻辑强依赖 profile 参数质量与运行时绑定机制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 决策增强骨架 | `$\mathcal{B} = (Q, q_0, O, \delta, \Pi, \mathcal{D})$` | 任务状态和运行时决策被显式分层。 |
| 单块决策函数 | `$d : \Pi \to O$` | 决策块把 profile 参数映射成状态机 outcome。 |
| 障碍处理规则 | `$d_{\mathrm{obs}}(\pi) \in \{\texttt{plan}, \texttt{help}\}$` | 下一转移不写死，而由环境与用户条件决定。 |
| 两阶段运行语义 | `$(q_t, \pi_t) \xrightarrow{d_q} o_t \xrightarrow{\delta} q_{t+1}$` | 先做情境决策，再做状态转移。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `SMACH` 负责显式任务状态和层次流程。 |
| 事件 / 触发 | 强支持 | `activate` outcome、动作结果和传感信息都可触发转移。 |
| 守卫 / 数据 | 强支持 | `DMSL` 显式读取 user / robot / env 参数。 |
| 层次 | 中等支持 | `SMACH` 支持层次状态机，但论文重点不在深层嵌套语义。 |
| 并发 / 同步 | 弱支持 | 本文主要展示单行为链决策，不展开并发状态组合。 |
| 时间约束 | 不支持 | 没有显式时钟、不变式或时间守卫。 |
| 连续动态 / 随机性 | 不支持 | 连续运动被底层导航系统吸收，本文只建模离散决策。 |
| 可执行 / 可验证性 | 强执行、有限验证 | 运行时可执行性强，原文提到 adaptation-design verification，但未展开严格形式验证链。 |

### 形式化问题与性质

1. 论文真正补足的是“任务结构”和“适配决策”之间的接口层。
2. `DMSL` 把 profile 参数显式化，这对后续自动生成 guard 或 transition label 很有价值。
3. outcome 采用语言化标签而不是数值控制量，适合和需求文本对齐。
4. 对 `project_1` 来说，这是一种典型的“需求属性 -> 决策规则 -> 状态机边”的桥接模式。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先用 `SMACH` 画出任务骨架，例如“寻找用户”“避障”“回到用户”等状态。
2. 再识别哪些状态需要根据上下文做适配性分支。
3. 为这些状态编写 `DMSL` 决策块。
4. 把 runtime profile 参数绑定到各决策块。
5. 用 `activate` outcome 把决策块结果回填到状态机转移。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `SMACH` 状态机图与 Python 库实现。
2. `DMSL` 的 `if-then-else` 决策块。
3. profile 参数对象，如 `params.user.*`、`params.robot.*`、`params.env.*`。
4. `activate "plan"`、`activate "help"` 这类 outcome 返回值。

### 交换与互操作

互操作重点在：

1. `SMACH` 与导航、UI、底层组件之间通过 outcome 和状态接口交互。
2. `DMSL` 读取跨组件 profile 变量，形成统一决策入口。
3. 状态机和决策块之间通过 linguistic outcome 解耦。
4. 同一个 profile 参数可在多个决策块中复用。

## 配套基础设施

- 建模/编辑工具：`SMACH` Python library、`DMSL` 规则编写方式。
- 解析/交换/元模型支持：profile 参数对象、component-local decision block；原文未给独立元模型标准。
- 仿真/执行支持：`HOBBIT` 陪伴机器人上的导航、交互与行为执行组件。
- 验证/分析支持：原文提到 automatic adaptation-design verification 方向，但未给完整独立验证链。
- 代码生成/转换支持：原文未给自动生成器，主要依赖手工编写 `SMACH` 状态和 `DMSL` 规则。
- 标准化或社区生态：依托 `SMACH` 的 ROS 高层行为建模路线与辅助生活机器人研究生态。

## 适用场景与需求前提

### 适用场景

适合服务机器人、陪伴机器人、辅助生活机器人这类既有固定任务骨架、又需要依据用户画像和环境上下文动态选边的系统。

### 需求前提

1. 任务本身能先抽成稳定的离散流程骨架。
2. 运行时差异主要体现为“在某个状态该选哪条边”。
3. 用户、环境和机器人内部状态能够结构化为 profile 参数。
4. 系统更需要语义级适配，而不是连续控制优化。

### 不适用或高成本场景

若系统的复杂性主要来自连续控制、概率规划或大规模并发协同，这种“状态机 + 决策块”组合会显得过轻，可能需要规划器、行为树或混成控制框架。

## 与相邻形式主义的关系

相对普通 `FSM/HFSM`，它多了一层 profile-driven 决策块；相对行为树，它保留了显式状态和 outcome 语义；相对通用任务规划器，它更轻、更局部，也更依赖人工写好的状态骨架。

## 与本研究的关系

### 对 Project 1 的价值

它直接说明了自然语言需求里的“用户偏好”“环境上下文”“机器人资源状态”可以不都塞进状态节点，而是单独沉淀为可执行决策规则。

### 作为目标形式主义还是中间表示

对服务机器人应用来说，这类模型可以直接作为目标执行载体；对更通用的需求到模型流程，它也很适合作为“状态机边选择器”的中间表示。

### 对需求到模型生成的启发

1. 需求文本中的上下文条件很适合提取成 profile 参数，而不是直接写死在状态名里。
2. 高层状态机与局部决策规则应该分开生成。
3. LLM 可以优先生成 outcome 名称和 `if-then-else` 决策块，再回填到状态图。
4. 同一个上下文变量在多个状态中的复用关系值得被抽取为共享词表。

### 现实限制

原文没有给出形式化语义证明或统一交换格式，因此它更像一种工程有效的执行组织方式，而不是成熟标准。

## 重要的相关工作

- `SMACH High-Level Executive`：本文显式建立在该高层行为执行框架之上。
- `HOBBIT` 陪伴机器人项目：是组合状态机与决策块的真实应用背景。
- 用户界面自适应中的 `DMSL` 既有工作：为本文把 `DMSL` 移植到机器人行为适配提供前史。
- 服务机器人导航与交互模块：构成状态机 outcome 的落地执行端。

## 文献分类总结

- 这是一篇 `📦` 类执行载体条目，核心不是新自动机理论，而是把 `SMACH` 状态机与 `DMSL` 决策块组合成可适配机器人行为架构。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景是具身陪伴机器人，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“需求上下文如何转成状态机边选择规则”的应用证据。
