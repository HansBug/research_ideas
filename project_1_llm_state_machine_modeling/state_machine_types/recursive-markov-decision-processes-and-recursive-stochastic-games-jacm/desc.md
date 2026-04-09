# 递归马尔可夫决策过程与递归随机博弈 / Recursive Markov Decision Processes and Recursive Stochastic Games

## 基本信息

- 标题：Recursive Markov Decision Processes and Recursive Stochastic Games
- 中文标题：递归马尔可夫决策过程与递归随机博弈
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*Journal of the ACM*, 62(2):1-69, 2015
- DOI：`10.1145/2699431`
- 链接：https://homepages.inf.ed.ac.uk/kousha/j_sub_rmdp_rssg.pdf
- 形式主义：`Recursive Markov Decision Processes (RMDP)` 与 `Recursive Simple Stochastic Games (RSSG)`，并系统连接 `BMDP/BSSG`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / controlled-game recursive stochastic family 整理
- 工具/实现获取方式：原文未附单独实现；机器可处理入口是 `RSSG/RMDP` tuple、`1-exit` 非线性 min/max 方程、SM strategy 语义与 linearly-recursive 化简。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 components、boxes、玩家分区、全局递归随机博弈语义与 branching-process 对应变换。

## 简报

这篇 `JACM` 版本把 `RMDP/RSSG` 从 conference 版中的“可定义、可判定”推进成完整的 recursive stochastic-game family。它的关键价值有三层：第一，系统写清 `1-RMDP/1-RSSG` 的最小不动点语义；第二，把 `SM` 策略、`linearly-recursive` 子类、`BMDP/BSSG` 对应关系都稳定下来；第三，明确 multi-exit 与一般性质模型检查为何会失控。因此，这篇论文是 `RMC -> RMDP/RSSG` 这一节点最合适的 full version 锚点。

- 形式主义定位：`RMC` 上的 controller / adversary journal 级 family 整理，也是 probabilistic recursive branch 从“随机过程”走向“递归最优控制 / 递归博弈”的标准依据。
- 构造方式简述：递归 component 结构保持不变，但每个顶点被划入 `chance / max / min` 三类之一，并在 `1-exit` 情形下收束为最小不动点 nonlinear min/max system。
- 基础设施与场景简述：纯理论条目，但它已经把 `SM` 策略、linearly-recursive 精确求值、`BMDP/BSSG` 双向变换与 multi-exit 不可判定边界全部整理成一套家族口径。

```text
RMC -> player-partitioned recursive game -> 1-exit min/max equations -> SM strategies / linear subclass -> BMDP/BSSG correspondence
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RSSG` 看成“递归的、turn-based、零和随机博弈”，而 `RMDP` 是单控制器特例。它特别强调：`1-exit` 子类对应 controlled / game versions of branching processes 和 `SCFG`，因此这不是一般 game theory 套件，而是直接附着在递归状态机族谱上的模型分化。

### 核心抽象

原文把一个 `RSSG` 写成：

$$
A=(A_1,\ldots,A_k)
$$

其中每个 component 为：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i` 指明 box 调用的 component。
4. `En_i` 与 `Ex_i` 是 entry / exit 接口。
5. `pl_i:Q_i\to\{0,1,2\}` 指定顶点属于 chance、max 或 min。
6. `\delta_i` 给出概率边或玩家可选边。

全局状态系统写成：

$$
M_A=(V_0\cup V_1\cup V_2,\Delta,pl),\qquad V\subseteq B^*\times Q
$$

上式中的符号逐项解释如下：

1. `V_0,V_1,V_2` 分别是 chance、max、min 对应的全局状态集合。
2. `\Delta` 是全局递归随机博弈转移。
3. `B^*` 是调用栈上下文。
4. `Q` 是所有 component 顶点和端口的并集。

### 一个最小例子与通俗解释

一个最小例子可以是“递归处理任务时，控制器和环境轮流出招”：

1. 控制器在 max 顶点决定是否递归调用子过程。
2. 环境在 min 顶点决定是否把流程推向更差分支。
3. chance 顶点则表示不可控的随机结果。

通俗地说，`RMDP/RSSG` 就是“会递归调用的随机决策图 / 随机博弈图”。如果 `RMC` 只是“递归+概率”，那么这里就是“递归+概率+交互方”。

### 运行 / 接受 / 转移语义

`1-exit` 情形下，termination value 由最小不动点系统给出，向量形式写成：

$$
x=P(x)
$$

其中每个分量 `x_u` 按顶点类型被定义为：

$$
x_u=\sum p_{u,v}x_v,\ x_{(b,en)}=x_{en}\cdot x_{(b,ex)},\ x_u=\max_v x_v,\ x_u=\min_v x_v
$$

上式中的符号逐项解释如下：

1. 第一行是概率顶点的 Bellman 型更新。
2. 第二行是调用端口的乘法结构。
3. 第三、四行分别是 max / min 玩家的一步最优选择。
4. `P` 是单调算子，其最小不动点给出 `1-exit` termination values。

### 语义边界

这个 family 的边界被本文写得很清楚：

1. `1-RMDP/1-RSSG` 仍保留可判定性。
2. multi-exit 情形会迅速进入不可判定区。
3. `RMDP/RSSG` 仍是 turn-based，不是 concurrent simultaneous-move。
4. 其核心结构仍是递归 component，而不是程序语法糖或 DSL。

### 关键性质与判定边界

这篇 full version 的核心结论可以压成三组：

$$
\text{quantitative termination for 1-RMDPs / 1-RSSGs} \in \mathrm{PSPACE}
$$

$$
\text{qualitative termination for maximizing/minimizing 1-RMDPs} \in \mathrm{P}
$$

$$
\text{qualitative termination for 1-RSSGs} \in \mathrm{NP}\cap \mathrm{coNP}
$$

此外，linearly-recursive 子类在值域上退回到有理数并可显著更高效处理，而 multi-exit `RMDP` 的 termination 与更一般模型检查又会变成不可判定。论文还把 `BMDP/BSSG` 与 `1-RMDP/1-RSSG` 的等价关系系统写全，因此它不仅是算法论文，也是 family-boundary 论文。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 递归 components、boxes、entry/exit、player partition。 |
| 事件 / 触发 | 强支持 | 玩家控制边与概率边并存。 |
| 守卫 / 数据 | 不支持 | 重点不在变量。 |
| 层次 | 强支持 | call/return 递归结构保持完整。 |
| 并发 / 同步 | 不支持 | 这里是 turn-based，不是 concurrent。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 随机转移和最优决策并存。 |
| 可执行 / 可验证性 | 强理论支持 | `LFP`、SM strategies、linear subclass、BMDP/BSSG 对应。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=(A_1,\ldots,A_k)$` | 递归随机决策 / 博弈总结构。 |
| component 元组 | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)$` | 单个 component 的完整骨架。 |
| 玩家映射 | `$pl_i:Q_i\to\{0,1,2\}$` | chance / max / min 三方。 |
| 全局状态 | `$V\subseteq B^*\times Q$` | 调用栈上下文上的递归博弈状态。 |
| 不动点系统 | `$x=P(x)$` | `1-exit` termination values 的统一表达。 |

## 构造方式与承载格式

### 建模入口

1. 定义递归 components 及其 entry / exit。
2. 用 boxes 表达递归调用。
3. 划分 chance / max / min 顶点。
4. 在 `1-exit` 情形下构造对应不动点方程。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RSSG/RMDP` tuple；
2. 全局递归随机博弈 `M_A`；
3. `1-exit` nonlinear min/max equations；
4. `SM` strategy 与 linearly-recursive 化简。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md) 的 `RMC`。
2. 向旁边把 `BMDP/BSSG` 拉入同一谱系。
3. 向下为 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 提供 concurrent 之前的 turn-based 母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 tuple、player partition 与 `LFP` 系统。
- 仿真/执行支持：可按全局递归随机博弈语义运行。
- 验证/分析支持：termination quantitative / qualitative analysis、`SM` strategy、linearly-recursive exact solving。
- 代码生成/转换支持：给出与 `BMDP/BSSG` 的双向变换，不是工程代码生成。
- 标准化或社区生态：研究型 family，连接 recursive game、branching process 与 probabilistic verification。

## 适用场景与需求前提

### 适用场景

适合：

1. 概率递归系统里的最优控制。
2. 递归 system-environment 对抗分析。
3. 需要把 branching-process game 重新拉回状态机表示。

### 需求前提

1. 交互是 turn-based。
2. 系统核心复杂度来自递归调用。
3. 接口可抽成有限 entry / exit。

### 不适用或高成本场景

如果双方需要同时动作，应改用 `RCSG`；如果只是 closed stochastic model，应改用 `RMC`；如果需要时间或数据变量，则应看其他 family。

## 与相邻形式主义的关系

相对 conference 版，这里更强调 `SM` 策略、linearly-recursive 子类与 `BMDP/BSSG` 对应；相对 `RMC`，它加入 controller / adversary；相对 `RCSG`，它还没有 simultaneous independent moves。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RSM` 后的概率递归分支不再只是一条“随机过程”细线，而是能够清楚分出 `RMC -> RMDP/RSSG` 这一 controlled / game 子枝。

### 对状态机自动建模的启发

当需求文本不仅有递归与概率，还有“系统想尽量成功、环境想尽量阻止”这类目标冲突时，这篇论文给出的 family 比 `RMC` 更贴切。

### 现实限制

它依然是理论节点，不是工程语言，也不直接提供工业工具。

## 重要的相关工作

1. [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md)：conference 起点。
2. [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md)：把 turn-based 再推进到 concurrent recursive stochastic games。
3. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)：它所依附的 `RMC` 随机递归母线。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🌊 混成 / 随机扩展`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🤝 接口 / 交互契约`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC -> RMDP/RSSG` 位置，并作为该节点的 journal full version 依据。
