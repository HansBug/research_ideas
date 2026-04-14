# CADP 2010：分布式进程构造与分析工具箱 / CADP 2010: A Toolbox for the Construction and Analysis of Distributed Processes

## 基本信息

- 标题：CADP 2010: A Toolbox for the Construction and Analysis of Distributed Processes
- 中文标题：CADP 2010：分布式进程构造与分析工具箱
- 作者：Hubert Garavel，Frédéric Lang，Radu Mateescu，Wendelin Serwe
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2011)*，pp. 372-387，2011
- DOI：`10.1007/978-3-642-19835-9_33`
- 链接：https://doi.org/10.1007/978-3-642-19835-9_33
- 形式主义：`Action-based LTS / BES / CADP`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：action-based concurrency verification toolbox / `LTS`-centric multi-language infrastructure
- 工具/实现获取方式：原文明确给出 `http://vasy.inria.fr/cadp` 作为 `CADP` 获取入口。
- 标准/格式获取方式：原文说明 `CADP` 以 action-based `LTS`、`BCG`、`Open/Caesar`、`SVL`、`MCL`、`BES/PBES` 等作为主要承载；它不是单一建模语言，而是验证工具箱生态。

## 简报

这篇论文的意义，在于把并发理论里的 action-based `LTS`、equivalence checking、branching-time logic、`BES/PBES` 和多语言编译链整成一个长期演化的验证工具箱。`CADP` 不是只做一个 model checker，而是把 explicit graph、implicit graph、语言前端、`Open/Caesar` 接口、`BCG` 存储、`SVL` 脚本和一整套等价/模型检查工具拼成可组合平台。

- 形式主义定位：并发 / 分布式进程的 action-based `LTS` 工具箱，而不是新的状态机本体。
- 构造方式简述：高层规格语言或 communicating automata 先被编译成 `LTS` 或 on-the-fly post-transition interface，再交给 equivalence checking、model checking、performance evaluation、test generation 等模块。
- 基础设施与场景简述：依托 `BCG`、`Open/Caesar`、`SVL`、`MCL`、`BES/PBES`、`Eucalyptus` GUI，服务协议、并发软件、分布式进程和 action-based 行为验证。

```text
process calculus / communicating automata -> Open/Caesar or explicit LTS -> BCG / BES / MCL / SVL -> equivalence checking / model checking / test generation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. action-based labelled transition systems；
2. explicit / implicit state-space representations；
3. `BCG` binary graph format；
4. `Open/Caesar` language-independent exploration architecture；
5. `BES / PBES` 作为底层分析问题承载。

### 核心抽象

`CADP` 的核心行为对象可保守写成 action-based `LTS`：

$$ G = (S, A, \to, s_0) $$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `A` 是可观察动作集合。
3. `\to \subseteq S \times A \times S` 是带标签转移关系。
4. `s_0` 是初始状态。
5. 论文明确强调 `CADP` 依赖 action-based semantic models，而不是 state-based semantics。

对显式状态空间，论文直接区分“整个状态-转移图已知”的 extensive 表示；对隐式状态空间，则只给初始状态和 post-transition function。后者可保守整理为：

$$ Post : S \to \mathcal{P}(A \times S) $$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `A` 是动作标签集合。
3. `Post(s)` 给出从状态 `s` 出发的全部动作-后继对。
4. 论文说明 `Open/Caesar` 正是把语言相关细节隐藏在这个 higher-order iterator 风格接口之后。

论文还把大量分析问题压到 `BES` 上，可保守写成：

$$
(\sigma_1 X_1 = f_1)\;(\sigma_2 X_2 = f_2)\;\cdots\;(\sigma_n X_n = f_n)
$$

上式中的符号逐项解释如下：

1. `X_i` 是布尔变量。
2. `f_i` 是命题公式右侧。
3. `\sigma_i \in \{\mu,\nu\}` 表示最小或最大不动点符号。
4. 论文明确说 `BES` 是表达 model checking、equivalence checking、POR 与 test generation 的低层形式。
5. `PBES` 则是在此基础上再加入 typed data parameters。

### 一个最小例子与通俗解释

一个最小例子可以是两个进程通过动作 `send` / `recv` 协调：

1. 上游进程先执行 `send`，下游进程等待 `recv`。
2. 两者组合后得到一个 action-based `LTS`。
3. `CADP` 可以把这个图存成 `BCG`，或通过 `Open/Caesar` 只暴露“从当前状态还能发出哪些动作”。
4. 然后再对该 `LTS` 做 bisimulation、`MCL` 性质检查或 test generation。

通俗地说，`CADP` 不是在问“某个状态里有多少寄存器值”，而是在问“系统能做哪些动作、这些动作以什么并发/同步方式发生、不同实现的可观察动作行为是否等价”。

### 运行 / 接受 / 转移语义

`CADP` 采用 action-based semantics，其基本一步转移就是：

$$ s \xrightarrow{a} t $$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `a` 是可观察动作。
3. `t` 是后继状态。
4. 论文明确将 action-based models 与后续 equivalence checking、compositional verification 绑定起来。

若某个 `MCL` / branching-time property 被编码成 `BES`，则判定问题可保守写成：

$$ G \models \varphi \iff BES(G,\varphi)\ \text{可解且初始变量为真} $$

上式中的符号逐项解释如下：

1. `G` 是待分析的 `LTS`。
2. `\varphi` 是性质公式。
3. `BES(G,\varphi)` 是把图和公式联立得到的布尔方程系统。
4. 论文强调 `Cæsar_Solve` 支持 on-the-fly 构造并求解这样的 `BES`。

### 语义边界

1. 论文主体是 action-based concurrency infrastructure，不是面向控制工程的富数据状态机 DSL。
2. `CADP` 的强项是并发进程、协议、进程代数和 communicating automata，而不是 timed/hybrid 连续语义。
3. 它偏 branching-time / equivalence thinking，不是单纯的线性 trace 工具。
4. `BCG`、`SVL`、`MCL` 是稳定承载，但不等于中立工业标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| action-based `LTS` | `$G = (S, A, \to, s_0)$` | `CADP` 以可观察动作为中心组织状态空间。 |
| implicit exploration | `$Post : S \to \mathcal{P}(A \times S)$` | `Open/Caesar` 隐藏语言细节，只暴露 post-transition iterator。 |
| `BES` 骨架 | `$(\sigma_1 X_1 = f_1)\cdots(\sigma_n X_n = f_n)$` | 多类分析问题都可下沉为布尔方程系统。 |
| 语义判定 | `$G \models \varphi \iff BES(G,\varphi)$ 可解` | model checking 与 equivalence checking 的统一底盘。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主对象就是 action-based `LTS`。 |
| 事件 / 触发 | 很强 | 动作标签和同步行为是核心。 |
| 守卫 / 数据 | 中等支持 | 支持复杂数据结构，但前提是并发进程之间不共享这些数据结构。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 很强 | 典型面向分布式进程与协议。 |
| 时间约束 | 有限支持 | 可涵盖某些 Markovian / IMC 变体，但不是 timed-automata 主平台。 |
| 连续动态 / 随机性 | 部分支持 | 支持 Markov chains / IMC 等性能模型，但不是连续动力学工具。 |
| 可执行 / 可验证性 | 很强 | equivalence、model checking、test generation、performance evaluation 都很完整。 |

### 形式化问题与性质

1. `CADP` 的真正资产是“多语言前端 + action-based 中间层 + 丰富后端算法”的平台化架构。
2. `BCG` 解决大图持久化，`Open/Caesar` 解决隐式状态空间复用，`BES/PBES` 解决分析问题统一表示。
3. 它非常适合作为“状态机/并发规格验证基础设施”证据，而不适合作为主树里的新语言节点。

## 构造方式与承载格式

### 建模入口

原文给出以下典型入口：

1. `LOTOS`、`LOTOS NT` 等高层规格语言；
2. networks of communicating automata；
3. `FSP` 翻译入口；
4. 其他能提供 post-transition function 的形式或半形式输入。

### 机器可处理承载方式

机器可处理承载方式包括：

1. explicit `LTS`；
2. `BCG` binary format；
3. implicit graph via `Open/Caesar`；
4. `BES / PBES`；
5. `SVL` scripts 与 `MCL` properties。

### 交换与互操作

互操作是本文核心价值之一：

1. `BCG` 是显式图的统一存储层。
2. `Open/Caesar` 用编程接口把语言相关和算法相关部分解耦。
3. `SVL` 则把多步验证策略串成可复用脚本工作流。

## 配套基础设施

- 建模/编辑工具：`Eucalyptus` GUI 与多语言编译链。
- 解析/交换/元模型支持：`BCG`、`Open/Caesar`、`SVL`、多语言 compiler front-ends。
- 仿真/执行支持：支持 simulation、random execution 与 on-the-fly exploration。
- 验证/分析支持：equivalence checking、branching-time model checking、`BES/PBES` solving、test generation、performance evaluation。
- 代码生成/转换支持：支持多语言到统一 action-based verification objects 的转换。
- 标准化或社区生态：`CADP` 主站、`BCG` benchmark suite、`Open/Caesar` 编程接口共同构成长期生态。

## 适用场景与需求前提

### 适用场景

适合通信协议、分布式进程、进程代数规格、组件交互系统和任何更重“动作可观察性、并发同步、等价关系”的场景。

### 需求前提

1. 系统核心行为最好能压成 action-based `LTS`。
2. 团队需要的不只是 reachability，还包括 equivalence、compositional verification、test generation 或脚本化验证流程。
3. 若使用富数据结构，需接受其不作为共享并发状态来处理。
4. 工作流更偏 formal concurrency tooling，而不是图形状态图编辑。

### 不适用或高成本场景

如果目标是 timed automata、层次状态图、连续动力学或现代可视化控制建模前端，`CADP` 会显得过于偏并发理论和 action-based toolchain。

## 与相邻形式主义的关系

相对 [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)，`MTSA` 更偏 `FSP/MTS` 的 Eclipse 工具，而 `CADP` 是更广谱的 action-based concurrency toolbox；相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，`TorX` 通过 `Open/Caesar` 生态消费状态空间，而本文解释的是该生态本体之一；相对 [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)，两者都走 action-based concurrency 平台路线，但 `CADP` 更老、更强调 `BCG/Open-Caesar` 与 equivalence checking 传统。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示我们，若未来某些需求被压成“交互动作主导”的状态机，中间表示不一定非得是 state-based graph，也可以是 action-based `LTS`。
2. `Open/Caesar` 这种“语言相关 / 语言无关”分层，很值得作为 `project_1` 后端接口设计的参考。
3. `BES/PBES` 也说明很多验证问题可以进一步下沉到统一求解形式，这对自动化闭环很有价值。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`CADP` 更像 action-based verification backend 与工具生态证据，而不是最终输出给用户的状态机语言。

## 重要的相关工作

- [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)：现有文库中的 `FSP` / `LTS` 工具条目。
- [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：与 `Open/Caesar` 生态有直接关联的测试工具线。
- [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)：另一条 action-based 并发验证平台路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 结论：这是一篇典型的 action-based concurrency tooling 论文，适合作为 `CADP`、`BCG/Open-Caesar`、`BES/PBES` 和 equivalence-centric distributed-process verification 路线的基础设施证据入账。
