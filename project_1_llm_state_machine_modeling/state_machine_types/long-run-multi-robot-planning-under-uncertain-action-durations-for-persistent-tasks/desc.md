# 不确定动作时长下持续任务的长程多机器人规划 / Long-Run Multi-Robot Planning under Uncertain Action Durations for Persistent Tasks

## 基本信息

- 标题：Long-Run Multi-Robot Planning under Uncertain Action Durations for Persistent Tasks
- 中文标题：不确定动作时长下持续任务的长程多机器人规划
- 作者：Carlos Azevedo, Bruno Lacerda, Nick Hawes, Pedro Lima
- 发表：*2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, pp. 4323-4328, 2020
- DOI：`10.1109/IROS45743.2020.9340901`
- 链接：https://doi.org/10.1109/IROS45743.2020.9340901
- 形式主义：`GSPNR / MRA for Persistent Multi-Robot Tasks`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🌡️
- 论文角色：持续任务规划 / generalized stochastic Petri net policy synthesis
- 工具/实现获取方式：原文给出 `GSPNR -> embedded MRA -> LRA policy synthesis` 的完整流程，并在 simulated monitoring problem 上评估；未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `GSPNR`、embedded `MRA`、`LRA reward` 与 `SSP` reduction；原文未给独立交换标准。

## 简报

这篇论文的亮点，不只是“Petri 网也能给多机器人规划建模”，而是把长期持续任务、动作时长不确定性和团队级目标函数一起压进一套 `GSPNR` 模型里。论文把机器人看成 token，把动作选择看成立即变迁，把持续时间不确定的执行看成指数定时变迁，再通过 `embedded MRA` 和 long-run average reward synthesis 求最优政策。相比常见的有限时域或折扣回报 formulation，它更直接面向“长期反复执行”的 persistent tasks。

- 形式主义定位：面向持续监测和长期循环任务的 `Petri Net` 应用框架，而不是一般工作流或单次任务调度网。
- 构造方式简述：先写带 rewards 的 `GSPNR`，再转为 embedded `MRA`，最后做 `LRA` policy synthesis。
- 基础设施与场景简述：依托 `GSPNR`、Markov reward automata、`SSP` reduction 和 policy extraction，服务 multi-robot monitoring under uncertain action durations。

```text
持续任务需求 + 动作时长不确定性 -> GSPNR with rewards -> embedded MRA -> LRA optimization -> 长期最优 team policy
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. places 形式化的局部机器人状态。
2. immediate / exponential transitions。
3. per-place 与 per-transition rewards。
4. stationary deterministic policy。
5. 从 `GSPNR` 到 embedded `MRA` 的转换。

### 核心抽象

论文显式定义了 generalized stochastic Petri net with rewards：

$$
G_r = \langle P, T, W^+, W^-, F, m_0, r_P, r_T \rangle
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合，对应局部机器人状态。
2. `T` 是 transitions 集合，并划分为 `T_I` 与 `T_E`。
3. `W^-` 是输入弧权重函数。
4. `W^+` 是输出弧权重函数。
5. `F` 为指数定时变迁赋予 firing rate。
6. `m_0` 是初始 marking。
7. `r_P` 为每个 place 指定单位时间奖励。
8. `r_T` 为每个立即变迁指定一次性奖励。

论文进一步把 policy 定义为：

$$
\pi : R(G_r) \to T_I \cup \{\mathrm{wait}\}
$$

上式中的符号逐项解释如下：

1. `R(G_r)` 是从初始 marking 可达的 marking 集合。
2. `T_I` 是立即变迁集合，对应可控决策动作。
3. `wait` 表示暂不选动作，等待下一个环境事件。

论文的核心优化目标是 long-run average reward：

$$
LRA_{G_r} = \max_{\pi \in \Pi_{G_r}} \mathbb{E}\left[\lim_{\tau \to \infty} \frac{rew(\pi,\tau)}{\tau}\right]
$$

上式中的符号逐项解释如下：

1. `\Pi_{G_r}` 是所有 stationary deterministic policies 集合。
2. `rew(\pi,\tau)` 是策略 `\pi` 在时间 `\tau` 内累积到的总奖励。
3. 极限比值表示长期平均收益，而不是短期折扣收益。

### 一个最小例子与通俗解释

论文的直观例子是 wildfire / monitoring scenario：

1. 多台同构机器人在若干 location 之间移动和巡检。
2. 某些 location 优先级更高，需要更频繁地被监测。
3. 每台机器人电量有限，时不时需要充电。
4. 由于拥堵、温度等因素，导航、放电和充电持续时间都不是确定值。

通俗地说，这个模型像把一个多机器人长期值班系统画成“会随机耗时的 Petri 网”，然后问：长期平均下来，怎样分配巡检和充电，才能让高优先级地点尽量一直被覆盖？

### 运行 / 接受 / 转移语义

论文把 GSPNR 的 marking process 解释成 embedded `MRA`：

$$
M_{G_r} = \langle S, s_0, Act, \to, \Rightarrow, \rho, \sigma \rangle
$$

上式中的符号逐项解释如下：

1. `S` 对应 reachable markings。
2. `s_0` 对应初始 marking `m_0`。
3. `Act` 是动作集合，包含立即变迁及内部等待动作。
4. `\to` 表示 immediate transitions 诱导的离散转移。
5. `\Rightarrow` 表示 exponential transitions 诱导的连续时间转移。
6. `\rho` 是状态奖励函数。
7. `\sigma` 是动作奖励函数。

文中对状态奖励给出：

$$
\rho(m) = \sum_{p_i \in P_{\ge 1}} r_P(p_i)
$$

上式中的符号逐项解释如下：

1. `P_{\ge 1}` 是在 marking `m` 下至少含有一个 token 的 places 集合。
2. `r_P(p_i)` 是 place `p_i` 的单位时间奖励。
3. 含义是：只要某类状态当前被至少一台机器人占据，就持续累计该 place 的奖励。

### 语义边界

这篇论文的边界同样很清楚：

1. 它主要处理 homogeneous multi-robot teams。
2. 不确定性只在 action duration，而不是状态观测或环境模型本体上。
3. 目标是长期平均收益，不是复杂任务逻辑与人机交互。
4. 连续运动细节被抽象掉，只保留 Petri-level task and resource dynamics。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 奖励型 GSPNR | `$G_r = \langle P, T, W^+, W^-, F, m_0, r_P, r_T \rangle$` | 同时建模任务逻辑、不确定时长与奖励。 |
| 策略空间 | `$\pi : R(G_r) \to T_I \cup \{\mathrm{wait}\}$` | 决策只发生在需要选动作的 markings。 |
| 长期目标 | `$LRA_{G_r} = \max_{\pi} \mathbb{E}[\lim_{\tau \to \infty} rew(\pi,\tau)/\tau]$` | 优化长期平均收益，而非单次任务收益。 |
| embedded MRA | `$M_{G_r} = \langle S, s_0, Act, \to, \Rightarrow, \rho, \sigma \rangle$` | 让奖励模型检查与 policy extraction 可行。 |
| 状态奖励 | `$\rho(m) = \sum_{p_i \in P_{\ge 1}} r_P(p_i)$` | 一个 place 只要当前有机器人驻留，就持续贡献 reward。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | places / markings 直接表达团队状态。 |
| 事件 / 触发 | 强支持 | immediate 与 exponential transitions 分别表达决策与环境事件。 |
| 守卫 / 数据 | 部分支持 | 重点在 marking 与 reward，不在复杂数据守卫。 |
| 层次 | 弱支持 | 主要是平面 Petri 结构与后续 MRA 转换。 |
| 并发 / 同步 | 强支持 | 多机器人作为多个 token 异步并发执行是核心。 |
| 时间约束 | 强支持 | 动作时长不确定性通过指数定时变迁显式进入模型。 |
| 连续动态 / 随机性 | 强随机、无连续 | 核心是 stochastic duration，不是连续动力学。 |
| 可执行 / 可验证性 | 强综合 | 可直接合成长期最优策略。 |

### 形式化问题与性质

1. 论文最有价值的地方，是把 Petri 网从“表达并发”推进到“做长期收益最优策略综合”。
2. places 被解释成局部 robot states，token 被解释成 robots，这让模型非常贴近团队执行语义。
3. `wait` 动作的引入使策略空间和环境事件自然衔接。
4. 对 Petri/concurrency 主干来说，这是一篇兼顾应用语义和策略综合的高质量样例。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先识别机器人可处的局部状态与可选动作。
2. 用 immediate transitions 表达 controllable decisions。
3. 用 exponential transitions 表达持续时间不确定的环境演化。
4. 用 rewards 表达监测优先级和长期目标。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `GSPNR` 图。
2. embedded `MRA`。
3. `LRA` reward property。
4. `SSP` reduction 与 policy extraction。

### 交换与互操作

互操作重点在：

1. `GSPNR` 负责直观建模团队任务。
2. `MRA` 负责承接模型检查与最优策略算法。
3. place rewards 与 transition rewards 共同定义 team-level objective。

## 配套基础设施

- 建模/编辑工具：原文未绑定单一 Petri 编辑器。
- 解析/交换/元模型支持：依赖 `GSPNR -> MRA -> SSP` 的算法链，而非开放交换标准。
- 仿真/执行支持：在 simulated monitoring problem 上评估策略性能。
- 验证/分析支持：`LRA` reward model checking、MEC decomposition、policy extraction。
- 代码生成/转换支持：原文未提供可下载代码。
- 标准化或社区生态：依托 stochastic Petri nets 与 Markov reward automata 研究线。

## 适用场景与需求前提

### 适用场景

适合持续监测、长期巡检、重复值守、带充电约束和动作耗时不确定性的多机器人任务。

### 需求前提

1. 团队状态可以用有限 places/markings 表达。
2. 动作时长不确定性可近似为指数分布。
3. 目标是长期平均绩效，而不是一次性最短时间。
4. 机器人最好是同构或至少在任务层可统一抽象。

### 不适用或高成本场景

如果问题核心在部分可观测性、复杂空间几何、异构大规模协同或非指数持续时间分布，这套 `GSPNR + MRA` 方法会面临抽象成本或建模偏差。

## 与相邻形式主义的关系

相对 [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文进一步把长期收益和随机时长拉进模型；相对 [Time Petri Nets](../time-petri-nets/desc.md)，它更强调 stochastic durations 与 reward-optimal policy；相对 [Coloured Petri Nets](../coloured-petri-nets/desc.md)，它不走数据颜色路线，而走任务状态与 reward 路线。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，一旦需求里主导因素是“并发团队执行 + 资源循环 + 不确定时长 + 长期绩效”，Petri 网家族比普通状态机更自然。

### 作为目标形式主义还是中间表示

对持续多机器人任务，它可以直接作为目标形式主义；对更一般控制系统，它也很适合作为并发任务层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把决策动作、环境事件和奖励口径一起抽出来。
2. “机器人是 token”这种抽象很适合让 LLM 逐步生成并发任务模型。
3. 若最终目标是长期策略而不是单次执行，奖励函数必须尽早进入模型，而不能只留在口头评价里。

## 重要的相关工作

- [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：本文在其多机器人 Petri 建模主线之上进一步走向 stochastic reward synthesis。
- [Time Petri Nets](../time-petri-nets/desc.md)：另一条时间化 Petri 主线。
- [Coloured Petri Nets](../coloured-petri-nets/desc.md)：同属 Petri 网扩展，但关注点不同。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心是用奖励型 `GSPNR` 为长期持续多机器人任务综合策略。
- 其描述客体是并发过程/资源流，因此记为 `🏭`；论文语境面向多机器人物理监测任务，因此记为 `🌡️`。
- 对 `project_1` 来说，它补的是“Petri/concurrency 模型如何承载长期团队任务与不确定时长”的关键证据。
