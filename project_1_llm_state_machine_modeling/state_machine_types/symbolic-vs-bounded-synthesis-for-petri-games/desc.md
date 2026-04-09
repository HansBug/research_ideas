# Petri 博弈的符号综合与有界综合比较 / Symbolic vs. Bounded Synthesis for Petri Games

## 基本信息

- 标题：Symbolic vs. Bounded Synthesis for Petri Games
- 中文标题：Petri 博弈的符号综合与有界综合比较
- 作者：Bernd Finkbeiner，Manuel Gieseking，Jesko Hecking-Harbusch，Ernst-Rüdiger Olderog
- 发表：*Electronic Proceedings in Theoretical Computer Science*，260:23-43，2017
- DOI：`10.4204/eptcs.260.5`
- 链接：https://doi.org/10.4204/EPTCS.260.5
- 形式主义：`Petri games / ADAM / symbolic-vs-bounded synthesis`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：distributed-synthesis comparison for Petri games / symbolic graph game vs bounded-QBF route
- 工具/实现获取方式：原文明确说明 symbolic 路线实现于 `ADAM`，bounded synthesis 路线实现为生成 `2-QBF` 的 prototype，并调用 `QuABS` 求解；正文未给稳定公开仓库链接。
- 标准/格式获取方式：主承载对象是 `Petri games`、unfolding / bounded unfolding、finite graph game、`BDD` fixed-point iteration 与 `2-QBF` 编码；它不是交换标准。

## 简报

这篇论文补的是 `Petri games` 线里很重要的一条“如何真正做 distributed synthesis”的方法比较。它不是单纯给一个新 benchmark，而是把两条完全不同的求解路线并排放到同一个形式主义上：一条是把 `Petri game` 约化成完全信息 finite graph game，再由 `ADAM` 用 `BDD` 做 fixed point；另一条是先做 bounded unfolding，再把“存在 winning strategy”编码成 `2-QBF` 交给求解器。

- 形式主义定位：围绕 `Petri games` 的综合方法路线，而不是新的 `Petri` 母型。
- 构造方式简述：一条路线走 `Petri game -> finite graph game -> BDD fixed point`，另一条路线走 `Petri game + bounds -> bounded unfolding -> 2-QBF -> strategy`。
- 基础设施与场景简述：依托 `ADAM`、bounded unfolding、`BDD`、`QuABS` 与制造/工作流 benchmark，服务分布式系统的正确性构造。

```text
Petri game -> symbolic graph game / bounded unfolding -> BDD or 2-QBF solving -> winning strategy -> local controllers
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. safe Petri games；
2. unfoldings 与 bounded unfoldings；
3. winning strategies；
4. symbolic graph-game reduction；
5. bounded synthesis 的 `2-QBF` 编码。

### 核心抽象

原文直接给出 `Petri game` 的元组：

$$
P = (P_S,P_E,T,F,In,B)
$$

上式中的符号逐项解释如下：

1. `$P_S$` 是 system places。
2. `$P_E$` 是 environment places。
3. `$T$` 是 transition 集合。
4. `$F \subseteq (P \times T) \cup (T \times P)$` 是 flow relation，其中 `$P=P_S \cup P_E$`。
5. `$In$` 是初始 marking。
6. `$B \subseteq P$` 是 bad places。

对本文的综合任务而言，策略不是全局控制器，而是 unfolding 上的局部裁剪。论文把 winning strategy 的要求压成四条：

$$
\mathrm{Win} = \mathrm{Safety} \land \mathrm{Determinism} \land \mathrm{DeadlockAvoidance} \land \mathrm{JustifiedRefusal}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{Safety}$` 要求任何可达 marking 都不含 bad place。
2. `$\mathrm{Determinism}$` 要求 system place 在任一可达 marking 上至多启用一个 outgoing transition。
3. `$\mathrm{DeadlockAvoidance}$` 禁止系统靠拒绝一切 transition 来“假装安全”。
4. `$\mathrm{JustifiedRefusal}$` 要求 system 只能一致地拒绝某类复制出的 transition，而不能利用 unfolding 副本偷看历史。

bounded synthesis 的关键形式化对象是 `2-QBF`。论文给出：

$$
\exists S.\forall M.\ f_n
$$

上式中的符号逐项解释如下：

1. `$S$` 是策略变量集合，典型变量形如 `$(p,t)$`，表示 system place `$p$` 是否选择 firing transition `$t$`。
2. `$M$` 是 marking 序列变量集合，典型变量形如 `$(p,i)$`，表示时间点 `$i$` 时 token 是否位于 `$p$`。
3. `$f_n$` 是长度界为 `$n$` 的 winning-condition 编码。
4. 量词顺序体现了“存在一套 system 决策，使任意合法 play 都满足 winning 条件”。

论文把矩阵主干写成：

$$
f_n := \left(\bigwedge_{i=1}^{n-1} sequence_i \Rightarrow win_i \right) \land (sequence_n \Rightarrow win_n \land loop)
$$

上式中的符号逐项解释如下：

1. `$sequence_i$` 表示前 `$i$` 步构成合法 play。
2. `$win_i$` 表示在第 `$i$` 步满足 no-bad-place、determinism 和 deadlock/termination 约束。
3. `$loop$` 表示在有界前缀末端已找到可重复的 marking，从而可扩成无限 winning play。
4. 这正是 bounded synthesis 能处理无限策略的关键。

### 一个最小例子与通俗解释

论文的运行例子是分布式报警系统：

1. 环境 token 先决定盗窃发生在地点 `A` 或 `B`。
2. 两个 system token 分别控制地点 `A` 和 `B` 的本地报警器。
3. 若没有通信，本地报警器无法仅凭局部信息确定应该报 `A` 还是 `B`。
4. winning strategy 因而必须先让本地控制器同步交换信息，再触发正确告警。

通俗地说，`Petri game` 把每个 token 看成一个只掌握局部历史的玩家。系统不是在求一个“知道全局状态的中心控制器”，而是在求一组分布式局部控制器，它们只能通过真正同步过的 transition 交换信息。

### 运行 / 接受 / 转移语义

本文的关键语义不在单次 firing 规则本身，而在“token 的因果历史如何变成局部可见信息”：

1. unfolding 把不同 causal past 显式展开。
2. strategy 是在 unfolding 上删去某些 system-controlled 分支。
3. symbolic 路线把 `Petri game` 约化成完全信息的 two-player finite graph game。
4. bounded 路线则在给定 unfolding bound `$b$` 和 proof bound `$n$` 下搜索 winning strategy。

两条路线的求解边界也不同：

1. symbolic 方法在本文只处理“单 environment player + 有界 system players + safety objective”。
2. bounded synthesis 能支持多个 environment players。
3. 但 bounded synthesis 不是完整决策过程，能证明存在 winning strategy，不能证明不存在。
4. 它偏向更小的策略，但需要挑选合适的 `b/n`。

### 语义边界

1. 本文处理的是 safe Petri games，不是一般高层网或无界网。
2. symbolic 路线强依赖 one-environment-player 假设。
3. bounded 路线的正确性依赖 bounds；如果 bounds 太小，可能只得到“没找到”，而不是“不存在”。
4. 论文主体是综合算法比较，不是 `Petri game` 母型定义论文。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Petri game` 元组 | `$P=(P_S,P_E,T,F,In,B)$` | system/environment token 共存的分布式博弈模型。 |
| winning 条件 | `$\mathrm{Safety} \land \mathrm{Determinism} \land \mathrm{DeadlockAvoidance} \land \mathrm{JustifiedRefusal}$` | system strategy 必须同时满足的四条硬约束。 |
| bounded synthesis 编码 | `$\exists S.\forall M.\ f_n$` | 把 winning-strategy existence 编成 `2-QBF`。 |
| bounded 矩阵 | `$f_n := (\bigwedge sequence_i \Rightarrow win_i)\land(sequence_n \Rightarrow win_n \land loop)$` | 有限前缀与无限循环都能表达。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | marking 与 unfolding histories 共同定义系统状态。 |
| 事件 / 触发 | 很强 | transition firing 是全部语义核心。 |
| 守卫 / 数据 | 弱支持 | 这里重点不在复杂数据守卫。 |
| 层次 | 不支持 | 不是层次网或 profile。 |
| 并发 / 同步 | 很强 | 多 token 并发与同步通信是模型本体。 |
| 时间约束 | 不支持 | 本文不是 timed Petri 游戏。 |
| 连续动态 / 随机性 | 不支持 | 纯离散分布式综合。 |
| 可执行 / 可验证性 | 很强 | `ADAM + BDD` 与 `QBF + QuABS` 都已实现并比较。 |

### 形式化问题与性质

1. symbolic 路线偏向完整性与总覆盖能力。
2. bounded 路线偏向小策略和更灵活的 environment-player 数量。
3. 两者差异不仅是实现技巧不同，而是“graph game exact solving”和“bound-guided search”两种不同综合哲学。
4. 对文库而言，这篇论文把 `Petri` 线从 verification 工具又往前推到 distributed synthesis。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. safe Petri game；
2. unfolding / bounded unfolding；
3. graph-game reduction；
4. `2-QBF` encoding。

### 机器可处理承载方式

机器可处理承载方式包括：

1. places / transitions / markings；
2. causal-history-sensitive unfolding；
3. BDD 编码的 finite graph game；
4. `QCIR/QBF` 风格的 bounded-synthesis 公式。

### 交换与互操作

互操作主要体现在：

1. symbolic 路线通过 `ADAM` 统一 benchmark 与 BDD 求解；
2. bounded 路线把 strategy existence 交给 `QuABS`；
3. 两者最终都输出可分解成 local controllers 的 winning strategy。

## 配套基础设施

- 建模/编辑工具：原文以 `ADAM` 为主要 symbolic synthesis 平台，并实现了 bounded synthesis prototype。
- 解析/交换/元模型支持：Petri game、bounded unfolding、finite graph game 与 `2-QBF` 编码。
- 仿真/执行支持：重点是合成 winning strategy，不主打运行时仿真。
- 验证/分析支持：`BDD` fixed point、`QBF` solving、benchmark families、strategy size 对比。
- 代码生成/转换支持：输出是 strategy / local controllers，不是部署代码生成链。
- 标准化或社区生态：依托 `ADAM`、`QuABS` 与分布式综合 benchmark 社区。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 分布式控制器自动综合；
2. manufacturing / workflow / alarm systems 这类多局部控制器协作对象；
3. 核心正确性依赖局部信息与同步通信结构的系统。

### 需求前提

1. 系统需能稳定建模为 safe Petri game。
2. system / environment place 划分要清晰。
3. 目标主要是 safety-style synthesis。
4. 若走 bounded 路线，需要能接受 `b/n` 这种搜索界参数。

### 不适用或高成本场景

若系统核心难点在复杂数据算术、概率博弈或连续动力学，而不是 causal memory 下的分布式离散决策，那么本文路线并不直接适配。

## 与相邻形式主义的关系

相对 [adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md](../adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md)，本文从 `Petri` verification 进一步走向 distributed synthesis；相对 `PRISM-games` 这类 stochastic game backend，本文的玩家信息结构不是全局状态，而是 token causal history；相对通用并发后端如 `CADP/mCRL2`，这里不是先写 process algebra 再综合，而是直接在 `Petri game` 语义上求局部控制器。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机/网模型不仅能拿来验证，还能直接合成分布式控制策略。
2. 对多组件控制需求，这种“局部信息 + 同步共享”语义很适合后续验证 profile 设计。
3. `Petri game -> strategy` 这条线也能为 `project_3 / project_4` 中的性质驱动修复提供反向参照。

### 作为目标形式主义还是中间表示

更适合作为并发控制与分布式协调问题的中间/后端表示，而不是需求工程师直接书写的前端语言。

### 对需求到模型生成的启发

1. 多主体需求不应默认转成中心化状态机，还要保留“谁知道什么”。
2. 若需求中存在显式协作、资源流和同步点，`Petri` 家族比纯 `FSM` 更自然。
3. bounded synthesis 的 `QBF` 编码也提示后续可以把“策略存在性”变成可求解 profile。

## 重要的相关工作

1. [adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md](../adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md)：同属 `Petri` 工具线，但重点在 flow-sensitive verification 而不是 synthesis。
2. [prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md](../prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md)：另一条 game-based synthesis / verification backend 代表。
3. [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)：更通用的分布式过程分析平台，可作为对比后端。

## 文献分类总结

- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Petri games / ADAM / symbolic-vs-bounded synthesis`
- 论文角色：distributed-synthesis comparison for Petri games / symbolic graph game vs bounded-QBF route
- 归类理由：论文主体讨论的是 `Petri games` 上 winning strategy 的求解方法与工具路线，核心贡献是 synthesis algorithm comparison，而不是标准载体或新的网本体定义。
