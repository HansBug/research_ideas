# 多智能体任务规格与执行 / Multiagent Mission Specification and Execution

## 基本信息

- 标题：Multiagent Mission Specification and Execution
- 中文标题：多智能体任务规格与执行
- 作者：Douglas C. MacKenzie, Ronald C. Arkin, Jonathan M. Cameron
- 发表：*Autonomous Robots*, 4(1):29-52, 1997
- DOI：`10.1023/A:1008807102993`
- 链接：https://doi.org/10.1023/A:1008807102993
- 形式主义：`MissionLab / CDL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：多智能体任务规格 / `CDL` + `FSA` 执行框架
- 工具/实现获取方式：原文明确给出 `MissionLab` toolset，包括 `CfgEdit` 图形配置编辑器、multiagent simulator、AuRA/UGV code generator、operator console，并说明 source/binary 可从 Georgia Tech `MissionLab` 页面获取。
- 标准/格式获取方式：承载方式是 `CDL (Configuration Description Language)` 文本语言、graphical `CfgEdit`、以及 temporal sequencing 的 `FSA` 图；原文未给行业标准或 XML/JSON 交换格式。

## 简报

这篇论文不是在重新发明一门一般状态机理论，而是在回答一个更工程化的问题：多机器人任务怎样从一堆底层 behavior、coordination operator 和感知触发条件，组织成可复用、可部署、可换平台的 mission specification。它的核心做法有两层：第一层用 `assemblage` 把一组 primitive behaviors 打包成新的高层 agent；第二层用 temporal sequencing 把 mission 分成离散 operating states，并用感知 trigger 在这些 state 之间切换。

- 形式主义定位：面向多智能体任务编排的 mission-specification 载体，而不是单机器人局部控制算法。
- 构造方式简述：用 `assemblage` 递归组合行为社会，再用 `FSA` 选择当前 dominant agent，最后以 `CDL` 文本语言和 `CfgEdit` 图形工具固化。
- 基础设施与场景简述：依托 `MissionLab`、`CfgEdit`、simulator、AuRA/UGV code generator 和 operator console，服务 janitor、scout、search 等多机器人任务。

```text
任务需求 -> primitive behaviors / coordination operators -> assemblages + temporal sequencing FSA -> CDL / CfgEdit -> simulator / code generator / runtime architecture
```

## 形式主义定义与核心对象

### 定义对象

`MissionLab` 的核心对象不是单个 flat `FSM`，而是“行为社会 + 状态切换”二层结构：

1. 底层把 primitive behavior 与 coordination operator 组合成 `assemblage`。
2. 上层用 temporal sequencing `FSA` 选择当前应当主导的 assemblage。
3. `CDL` 负责把这些 agent、assemblage、参数和绑定关系写成可部署配置。

### 核心抽象

结合论文的 `Societal Agent`、temporal sequencing 与 `CDL` 记法，可保守整理为：

$$
M = (P, \mathcal{G}, \alpha, \Gamma, B)
$$

上式中的符号逐项解释如下：

1. `P` 是 primitive behavior / primitive agent 的集合。
2. `\mathcal{G}` 是由 coordination operator 组合得到的 assemblage 集合。
3. `\alpha` 是 temporal sequencing 使用的有限状态自动机。
4. `\Gamma` 是 `CDL` 定义与实例化语句集合。
5. `B` 是把配置绑定到具体 robot architecture 和 primitive library 的部署信息。

论文对 assemblage 的核心构造给出了直接表达：

$$
\mathcal{A} = C'(A_1, A_2, \ldots, A_n)
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是新产生的 assemblage agent。
2. `C'` 是 coordination operator。
3. `A_1, \ldots, A_n` 是 subordinate agents。
4. 该构造表示一组 agent 被协调器封装成新的 coherent agent。

temporal sequencing 则直接使用有限状态自动机：

$$
\alpha = (Q, \delta, q_0, F)
$$

其中：

1. `Q` 是 operating state 集合。
2. `\delta` 是基于 perceptual triggers 的 transition function。
3. `q_0 \in Q` 是起始状态。
4. `F \subseteq Q` 是 accepting / completion states。

### 一个最小例子与通俗解释

论文给出的 janitor robot 是最直接的最小例子：

1. 初始进入 `Look_for_can`，机器人到处找空罐子。
2. 感知到 `detect_can` 后，切换到 `Pick_up_can`。
3. 成功抓取后切到 `Look_for_basket`。
4. 找到篮子后进入 `Put_can` 并放下罐子。
5. 放下后再次回到 `Look_for_can`，循环执行。

通俗地说，`MissionLab` 把“找罐子、捡罐子、找篮子、放罐子”这些高层技能当成状态，把视觉或接触等事件当成触发条件。每个状态背后不是一条简单动作，而是一整个可复用的 assemblage。

### 运行 / 接受 / 转移语义

论文对 temporal sequencing 的核心语义写得很直接：当前活跃 agent 由当前 `FSA` state 决定。可写成：

$$
f_{\mathrm{seq}}(A_1, A_2, \ldots, A_m, \alpha) = A_i \quad \text{if state } q_i \text{ is active in } \alpha
$$

上式中的符号逐项解释如下：

1. `f_{\mathrm{seq}}` 是 temporal sequencing coordination function。
2. `A_i` 是和状态 `q_i` 对应的 dominant agent / assemblage。
3. `\alpha` 是当前运行中的 `FSA`。
4. 一次只有与当前 operating state 对应的高层 agent 主导行为。

状态更新则可保守写成：

$$
q' = \delta(q, trig)
$$

其中：

1. `q` 是当前 operating state。
2. `trig` 是 perceptual trigger。
3. `q'` 是下一 operating state。
4. `\delta` 的输入不是一般抽象事件，而是环境感知触发条件。

对 `CDL` 而言，实例化与复用的关键语义是：

$$
\mathrm{instAgent}\ name\ \mathrm{from}\ X(\ldots) \Rightarrow \text{create a unique configured agent instance}
$$

这表示 `CDL` 把 primitive 或 assemblage 的“定义”和“实例”分开；同一 primitive 的不同实例是不同实体，不共享内部状态，除非显式通过命名引用其输出。

### 语义边界

`MissionLab` 的边界很清楚：

1. 它面向 mission specification，不是底层控制律建模语言。
2. 它核心是离散 operating states 与行为组合，不提供显式时钟自动机语义。
3. 它允许 retarget 到不同 architecture，但前提仍是底层 primitive library 已存在。
4. 它更强调可部署 mission configuration，而不是严格形式验证语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| assemblage 构造 | `$\mathcal{A} = C'(A_1, \ldots, A_n)$` | 协调器可把一组 agent 封装成新的 coherent agent。 |
| temporal sequencing 核心 | `$\alpha = (Q, \delta, q_0, F)$` | mission 被分成 operating states，并由 trigger 驱动切换。 |
| dominant agent 选择 | `$f_{\mathrm{seq}}(A_1,\ldots,A_m,\alpha)=A_i$` | 当前 `FSA` state 决定哪个 agent/assemblage 主导。 |
| 配置实例化 | `$\mathrm{instAgent}\Rightarrow$ unique instance` | `CDL` 显式区分定义与实例，支持复用与参数化。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | mission 被显式分解为离散 operating states。 |
| 事件 / 触发 | 强支持 | 感知触发条件直接驱动 `FSA` 转移。 |
| 守卫 / 数据 | 支持 | primitive 和 `CDL` 参数具名传值，但不强调复杂数据守卫语义。 |
| 层次 | 强支持 | assemblage 可递归嵌套。 |
| 并发 / 同步 | 支持 | 多 agent society 与 coordination operator 支持并发协作。 |
| 时间约束 | 弱支持 | 论文重点不在显式时间约束。 |
| 连续动态 / 随机性 | 不支持 | 连续控制下沉到底层 architecture / primitive behavior。 |
| 可执行 / 可验证性 | 强执行、弱验证 | simulator、code generator、operator console 强；正式验证未形成主线。 |

### 形式化问题与性质

1. `MissionLab` 的真正核心不是单一 `FSM`，而是 `assemblage + temporal sequencing` 的二层分工。
2. `CDL` 支持把复杂配置升级为可复用高层 agent，这一点比只写状态图更工程化。
3. architecture binding 被推迟到配置完成后，说明它把“任务逻辑”和“运行平台”显式解耦。
4. 该路线很适合多机器人任务编排，但对底层 primitive library 依赖很强。

## 构造方式与承载格式

### 建模入口

建模入口有两条：

1. 在 `CfgEdit` 中图形化搭建 primitive、coordination operator、assemblage 与 `FSA`。
2. 在 `CDL` 中用 `defPrimitive`、`instAgent`、`defAgent` 等文本语句表达配置。

### 机器可处理承载方式

机器可处理承载主要是：

1. `CDL` 文本配置。
2. `CfgEdit` 图形配置。
3. architecture-specific generated code。

### 交换与互操作

`MissionLab` 不提供行业交换标准；互操作主要体现为：

1. configuration 在具体 binding 之后可生成不同 architecture 的代码。
2. primitive library 按具体平台暴露可用行为。
3. 同一高层配置可 retarget 到不同 vehicle / architecture。

## 配套基础设施

- 建模/编辑工具：`CfgEdit` 图形配置编辑器，支持递归构造和复用。
- 解析/交换/元模型支持：`CDL` 作为配置语言，支持具名实例化、参数与 assemblage 定义。
- 仿真/执行支持：multiagent simulator、operator console、运行轨迹显示。
- 验证/分析支持：原文侧重 simulation 与 deployment，未给成熟 formal verification 工具链。
- 代码生成/转换支持：可生成 `AuRA` 与 `ARPA UGV` 架构代码。
- 标准化或社区生态：研究原型明确，可下载 source/binary，但不是行业标准。

## 适用场景与需求前提

### 适用场景

适合多机器人 scouting、janitor、search、协同监视等需要显式任务阶段和团队行为组合的场景。

### 需求前提

1. 任务可拆为有限个高层 operating states。
2. 每个 state 背后都能由已有 primitive / assemblage 实现。
3. 系统存在可感知的 trigger 以驱动 state 转移。
4. 团队协作逻辑可表达为 dominance、competition、cooperation 或 sequencing。

### 不适用或高成本场景

若系统主要难点在连续动力学、严格时序验证或复杂数据结构推理，`MissionLab` 的离散任务层抽象就不够；若底层 primitive library 不成熟，mission specification 也难落地。

## 与相邻形式主义的关系

相对普通单机器人 `FSM`，它多了 assemblage 和多智能体 coordination；相对 `XABSL`、`XRobots` 这类单体机器人行为语言，它更偏 mission-level orchestration；相对 `RAFCON`，它更早、更强调 architecture binding 和 multiagent society。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：状态机式建模不一定只落在单控制器层面，也可以成为多智能体任务规格的主承载。

### 作为目标形式主义还是中间表示

它更适合作为任务层中间表示或领域特化目标载体，而不是普适形式主义终点。

### 对需求到模型生成的启发

1. 高层任务 state 后面可以挂一个复合 assemblage，而不是单动作。
2. mission-level 需求可以先分 operating states，再映射到可执行 skill library。
3. “平台绑定后置”是需求到模型自动化里很值得保留的设计。

## 重要的相关工作

- `AuRA` 与 behavior-based architecture：提供其底层 primitive / coordination 背景。
- `Societal Agent`：是论文显式采用的理论基底。
- 机器人任务控制框架如 `PLEXIL`、`RAFCON`：与其一样都在处理“高层任务如何真正执行”。

## 文献分类总结

- 这是一篇 `📦` 类应用/专用状态机载体条目，重点不在一般自动机理论，而在多智能体任务规格与执行框架。
- 其描述客体是机器人任务控制逻辑，因此记为 `🎛️`；领域落在多机器人/CPS 场景，因此记为 `🌡️`。
- 对 `project_1` 来说，它补上了“mission-level state machine + skill assemblage + deployment binding”这一条很有代表性的工程支线。
