# 面向半自主机器人手术的基于状态图的手术流程建模 / Modeling of Surgical Procedures Using Statecharts for Semi-Autonomous Robotic Surgery

## 基本信息

- 标题：Modeling of Surgical Procedures Using Statecharts for Semi-Autonomous Robotic Surgery
- 中文标题：面向半自主机器人手术的基于状态图的手术流程建模
- 作者：Fabio Falezza, Nicola Piccinelli, Giacomo De Rossi, Andrea Roberti, Gernot Kronreif, Francesco Setti, Paolo Fiorini, Riccardo Muradore
- 发表：*IEEE Transactions on Medical Robotics and Bionics*, 3(4):888-899, 2021
- DOI：`10.1109/TMRB.2021.3110676`
- 链接：https://doi.org/10.1109/TMRB.2021.3110676
- 形式主义：`Procedure-Observer Surgical Statechart`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：半自主手术流程监督器 / observer-procedure statechart
- 工具/实现获取方式：原文直接给出 `SARAS` 项目中的双机械臂实验平台、speech recognition、force observer、catheter observer、feature observer、preoperative pose observer 和一组 surgeme primitives；未给公开代码仓库。
- 标准/格式获取方式：原文以修订后的 statechart 记法承载流程知识，核心对象是 procedure region、observer region、trigger events 和 surgeme 库；不是独立 `XML` 标准。

## 简报

这篇论文把“手术知识”和“环境感知”分到 statechart 的两个并发区域里，这是它最有价值的地方。作者没有让 procedure 自己产生事件，而是强制所有 trigger 都由 observers 提供，再由三层 hierarchy 的 procedure region 消费这些事件。这样，statechart 既能保留手术流程的可读性，又能把感知、语音、力反馈和轨迹执行统一接进半自主控制闭环。

- 形式主义定位：面向半自主机器人手术的 procedure-observer statechart，其中 procedure region 表示手术知识，observer region 表示感知与环境状态。
- 构造方式简述：固定三层 hierarchy `phase -> action -> surgeme`，同时让多个 observer `FSM` 并发生成 trigger，再由 procedure statechart 消费这些 trigger。
- 基础设施与场景简述：依托 `SARAS` 平台、speech recognition、force sensing、RGB catheter detection 和预注册位姿，服务 `RARP` 中 bladder mobilization、bladder neck transection 和 vesicourethral anastomosis。

```text
手术知识 + 传感/语音观测 -> observers 生成 triggers -> procedure statechart -> surgeme execution -> 双机械臂动作
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. procedure region：承载手术知识的主状态机。
2. observer region：并发运行的感知 `FSM` 集合。
3. 三层 hierarchy：`phase`、`action`、`surgeme`。
4. trigger events：由 observer 产生、被 procedure 消费。
5. surgeme 库：`No operation`、`Movement`、`Rotate tool`、`Open/close`。
6. 左右机械臂各自的流程 statechart。

### 核心抽象

结合论文提出的 revised statechart，可将其保守整理为：

$$
\mathcal{S} = (P, O, \Delta, q_0)
$$

上式中的符号逐项解释如下：

1. `P` 是 procedure hierarchy。
2. `O = \{o_1,\ldots,o_n\}` 是 observer `FSM` 集合。
3. `\Delta` 是基于 trigger 的转移关系。
4. `q_0` 是流程初始状态。

论文规定 procedure hierarchy 深度固定为三层，可写成：

$$
P = (L_{phase}, L_{action}, L_{surgeme}, \Delta_P)
$$

上式中的符号逐项解释如下：

1. `L_{phase}` 表示手术阶段层，如 bladder neck transection。
2. `L_{action}` 表示阶段内部的动作层，如 follow / grasp / pull。
3. `L_{surgeme}` 表示原子操作层，如 move、rotate、close tool。
4. `\Delta_P` 是 procedure region 内部的转移关系。

论文的核心限制条件可直接保留为四条规则：

$$
R_1:\ \mathrm{depth}(P)=3
$$

$$
R_2:\ \text{primitive states are atomic and hierarchy-agnostic}
$$

$$
R_3:\ \text{only observers generate triggers}
$$

$$
R_4:\ \text{no transitions across concurrent regions}
$$

上面四式中的符号逐项解释如下：

1. `R_1` 固定层级深度，避免随意嵌套。
2. `R_2` 保证 surgeme 可以复用。
3. `R_3` 强制感知和流程知识分离。
4. `R_4` 禁止跨并发 observer/procedure 直接连边。

其运行语义可保守压缩为：

$$
\mathrm{Trig}_t = \bigcup_{i=1}^{n} o_i(x_t)
$$

$$
q_{t+1} = \delta(q_t, \mathrm{Trig}_t)
$$

上面两式中的符号逐项解释如下：

1. `x_t` 是当前传感观测、语音命令和工具状态。
2. `o_i` 是某个 observer `FSM`，负责把观测转成 trigger。
3. `\mathrm{Trig}_t` 是当前控制周期可用的触发事件集合。
4. `\delta` 是 procedure region 的转移函数。

### 一个最小例子与通俗解释

论文给出的左臂 bladder neck transection 过程很适合做最小例子：

1. 左臂一开始处于 `idle phase`，停在 safe position。
2. surgeon 发出语音命令“left arm grasp the catheter”，speech observer 生成 `t_l16`。
3. procedure 进入 bladder neck transection phase，再进入 `follow action`。
4. catheter observer 检测到 catheter 可见，left arm 在安全距离上跟随。
5. 当 feature observer 检测到 catheter 停止，流程转入 `grasp action`。
6. force observer 判断抓取是否成功，若成功则进入 `pull action`，否则留在等待或 retry 分支。

通俗地说，这个模型像“手术脚本 + 多个传感哨兵”。真正决定何时跳转的不是 procedure 自己拍脑袋，而是每个 observer 先把当前环境翻译成事件。

### 运行 / 接受 / 转移语义

论文明确说明 controller 每个周期都按“高层到低层”的顺序评估 procedure，因此可保守写成：

$$
\delta : (L_{phase}, L_{action}, L_{surgeme}, \mathrm{Trig}_t) \to (L'_{phase}, L'_{action}, L'_{surgeme})
$$

上式中的符号逐项解释如下：

1. 评估从高层 phase 开始，再逐层向下。
2. 一旦某层有 trigger 匹配，就优先采用该层转移。
3. 转移发生时，内层 `FSM` 会被 reset 到初始状态。

observer 的局部语义则可概括为：

$$
o_i : x_t \mapsto t_k
$$

上式中的符号逐项解释如下：

1. `o_i` 是 force、speech、catheter、feature 或 pose observer。
2. `x_t` 是对应的传感/语音输入。
3. `t_k` 是生成的 trigger，例如 catheter found、goal reached、tool closed。

### 语义边界

这个模型的边界包括：

1. 它主要建模 procedure supervision，不直接解决高精度运动控制。
2. observer 质量高度依赖传感算法和硬件条件。
3. 论文只验证了特定 `RARP` 子流程，不是通用手术全流程标准。
4. 该方法强调可理解性和重构性，而不是形式验证上的极简语义核。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总体骨架 | `$\mathcal{S} = (P, O, \Delta, q_0)$` | procedure 和 observers 被显式区分。 |
| 三层 hierarchy | `$P = (L_{phase}, L_{action}, L_{surgeme}, \Delta_P)$` | 手术知识被压成 phase/action/surgeme 三层。 |
| 规则约束 | `$R_1..R_4$` | 限制 statechart 表达力以换取可控性和可复用性。 |
| 触发生成 | `$\mathrm{Trig}_t = \bigcup_i o_i(x_t)$` | 所有状态转移都必须来自 observer 事件。 |
| 转移语义 | `$q_{t+1} = \delta(q_t, \mathrm{Trig}_t)$` | procedure 只消费 trigger，不直接生成 trigger。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `phase/action/surgeme` 三层离散模式非常清晰。 |
| 事件 / 触发 | 强支持 | speech、force、pose、catheter visibility 等都被显式建成 trigger。 |
| 守卫 / 数据 | 强支持 | observer 把感知数据转成 trigger，相当于统一了 guard 来源。 |
| 层次 | 强支持 | 三层 hierarchy 是论文的硬约束。 |
| 并发 / 同步 | 强支持 | 多 observer 并发运行，但被限制在 sensing region 内。 |
| 时间约束 | 弱支持 | 有 sliding window 和 threshold，但不是显式 timed automata。 |
| 连续动态 / 随机性 | 中等支持 | 连续轨迹执行存在，但 statechart 主体仍是离散监督。 |
| 可执行 / 可验证性 | 强执行、较强可分析 | 实验平台可执行，且设计上强调避免死循环、未定义行为和 deadlock。 |

### 形式化问题与性质

1. 论文最重要的贡献是“谁能产生 trigger”这一条建模纪律。
2. statechart hierarchy 被主动收窄，使 procedure 更像受约束的手术脚本语言。
3. observer-procedure 分离特别适合 LLM 建模，因为它把需求知识和感知证据明确拆开了。
4. 同步多机械臂时，作者通过复制 statechart 并共享 triggers 来避免额外 synchronization states。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先从手术专家处抽取高层 procedure knowledge。
2. 再把 procedure 压成 `phase -> action -> surgeme` 三层。
3. 为每个需要的环境条件设计 observer `FSM`。
4. 最后把 observers 产生的 triggers 连接到 procedure transitions 上。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. revised statechart 图。
2. observer 列表及其 trigger 表。
3. surgeme 库及参数。
4. 左右机械臂各自的 procedure statechart。
5. 语音命令、力阈值、姿态阈值和 RGB 视觉触发器。

### 交换与互操作

互操作重点在：

1. observers 并发读取传感器和语音输入。
2. observers 生成 trigger 供 procedure 消费。
3. procedure 选择对应 surgeme。
4. surgeme 再被机械臂执行为 move、rotate、open/close 等动作。

## 配套基础设施

- 建模/编辑工具：revised statechart notation、procedure diagrams、observer tables。
- 解析/交换/元模型支持：observer triggers、speech commands、pre-registered map、tool state 与 pose events。
- 仿真/执行支持：`SARAS` 平台、双机械臂、speech recognition、RGB catheter detection、force sensing。
- 验证/分析支持：在 synthetic manikins 上验证 bladder mobilization、bladder neck transection、vesicourethral anastomosis 三个子流程。
- 代码生成/转换支持：原文未给自动代码生成链，重点在可重构 procedure modeling。
- 标准化或社区生态：与手术 workflow modeling、HTN 和 statechart 路线相连，但尚非通用临床标准。

## 适用场景与需求前提

### 适用场景

适合那些流程顺序明确、感知条件可结构化、且需要把人类专家知识与实时感知证据合并的半自主手术场景。

### 需求前提

1. 手术步骤可抽成阶段、动作和原子 surgemes。
2. 环境中至少有一组可靠 observer 可以生成触发事件。
3. 机器人动作可由较小的 primitive 库复用实现。
4. 临床团队愿意把 procedure knowledge 明确编码。

### 不适用或高成本场景

如果 procedure 高度开放、关键事件难以感知，或术中需要大量临时 improvisation，这种严格受限的 statechart 会过于僵硬。

## 与相邻形式主义的关系

相对普通 `FSM/HFSM`，它更强调 observer 和 procedure 的职责分离；相对行为树，它更强调当前 state 的可内省性；相对 HTN，它更接近可执行的监督器而不是纯规划分解结构。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合说明“需求知识”和“感知证据”在状态机生成里不应混写，而应分别进入 procedure region 和 observer region。

### 作为目标形式主义还是中间表示

对具体半自主手术系统，它可以直接作为目标监督器；对更一般的复杂控制系统，它也很适合作为连接任务知识与环境感知的中间表示。

### 对需求到模型生成的启发

1. 需求中的阶段词、动作词和原子操作词天然适合分层生成。
2. 传感条件最好先转成独立 observer，而不是直接把所有 guard 混入主状态图。
3. speech / force / vision 这类异构信号完全可以统一抽象成 trigger 集。
4. 限制 statechart 表达能力有时比无约束生成更有利于后续验证和维护。

### 现实限制

论文仍然依赖大量手工建模、observer 开发和阈值配置，距离完全自动化生成还有明显距离。

## 重要的相关工作

- `HTN` 与 surgical task automation：为三层 hierarchy 提供方法背景。
- 既有 surgical workflow `FSM/HFSM` 工作：证明流程离散建模可行。
- `SARAS` 项目中的感知与半自主手术研究：为本文提供平台基础。
- observer-based sensing 与 speech-triggered robotics：直接支撑本文 trigger 生成机制。

## 文献分类总结

- 这是一篇 `📦` 类医疗机器人应用条目，核心是如何用受约束的 statechart 表达半自主手术流程并吸纳多源感知触发。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景是医疗机器人和人机协同手术，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“流程知识与感知证据分离式建模”的高价值应用证据。
