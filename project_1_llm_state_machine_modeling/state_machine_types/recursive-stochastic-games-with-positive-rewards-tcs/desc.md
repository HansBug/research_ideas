# 带正奖励的递归随机博弈（TCS 全文版） / Recursive stochastic games with positive rewards

## 基本信息

- 标题：Recursive stochastic games with positive rewards
- 中文标题：带正奖励的递归随机博弈（TCS 全文版）
- 作者：Kousha Etessami, Dominik Wojtczak, Mihalis Yannakakis
- 发表：*Theoretical Computer Science*, 777:308-328, 2019
- DOI：`10.1016/j.tcs.2018.12.018`
- 链接：https://livrepository.liverpool.ac.uk/3052140/1/tcs-revision.pdf
- 形式主义：`1-exit Recursive Markov Decision Processes / 1-exit Recursive Simple Stochastic Games (1-RMDP / 1-RSSG)` 的 positive-reward journal full version
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / positive-reward recursive stochastic family 整理
- 工具/实现获取方式：原文提到 `PReMo` 线上的相关实现背景，但没有在文中给出完整公开仓库入口；机器可处理入口是 positive-reward `RSSG` tuple、`x=P(x)` least-fixed-point 语义、`SM` 策略与 strategy-improvement。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是带 reward 的 recursive stochastic-game 元组、call cost 映射以及与 `SCFG/BMDP/BSSG` 的等价表述。

## 简报

这篇 `TCS 2019` 全文版把 2008 年 conference 条目真正稳定成了 journal 级 family 依据。它不仅给出更完整的 positive-reward `1-RMDP / 1-RSSG` 定义，还系统整理了 `SM` 策略、least fixed point、strategy improvement、与 `SCFG/BMDP/BSSG` 的对应，以及 multi-exit reward 版本的不可判定边界。对演化树来说，它正好能把 `positive-reward 1-RMDP / 1-RSSG` 从“可补充的旁注”提升为“值得保留的正式子枝”。

- 形式主义定位：`RMDP/RSSG` 下 positive-reward 子枝的标准 journal anchor。
- 构造方式简述：在 `1-exit` recursive stochastic game 骨架上，为普通转移增加正奖励 `c_{u,v}`，为 call port 增加 call cost `\xi_i`。
- 基础设施与场景简述：原文虽然仍以理论分析为主，但把 `SCFG`、branching process、probabilistic procedural programs 与 recursive-state-machine 口径系统接通了。

```text
1-exit recursive stochastic game -> strictly positive rewards -> total expected reward -> LFP over extended reals -> SM strategies / strategy improvement
```

## 形式主义定义与核心对象

### 定义对象

原文直接把对象定义为“with positive rewards”的 `RSSG`。这不是一个换标签的旧模型，而是在 `1-exit RMDP / 1-RSSG` 上添加了新的语义轴：total expected reward。

### 核心抽象

原文给出的 canonical tuple 是：

$$
A=(A_1,\ldots,A_k)
$$

其中每个组件满足：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i,\xi_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i:B_i\to\{1,\ldots,k\}` 指出 box 调用哪个组件。
4. `En_i` 与 `Ex_i` 是 entry / exit 节点集合。
5. `pl_i` 把顶点分给 chance、player 1、player 2。
6. `\delta_i` 是带奖励的局部边关系，每条边既包含概率 / 决策信息，也包含正奖励。
7. `\xi_i:Call_i\to \mathbb R_{>0}` 给每个 call port 赋正的 call cost。

### 一个最小例子与通俗解释

原文把该 family 与带奖励的 `SCFG` / branching process 对应起来。一个最小直觉例子可以是：

1. 非终结符 `X` 以概率 `1/3` 展开成 `XX`，并获得奖励 `3`。
2. 以概率 `2/3` 展开成 `\epsilon`，并获得奖励 `2`。
3. 因为每次展开都有正奖励，只要 derivation 无限延续，总奖励就会发散到 `\infty`。

通俗地说，positive-reward recursive game 就像“每次递归展开都要记账”的递归随机状态机。一旦系统无限运行，账就会无限累积，所以它的数值行为和无 reward、或允许 `0` reward 的情况很不一样。

### 运行 / 接受 / 转移语义

原文把最优总期望奖励向量写成 least fixed point。对 `1-RMC`，文中明确指出：

$$
r^* \text{ is the LFP of } x = Ax + b
$$

对 `1-RSSG`，则提升为带 `min/max` 的方程系统：

$$
x = P(x)
$$

其中 `P` 由概率边、玩家选择、call-return 结构和 rewards 共同诱导。对 call port，值会分解为“本次调用成本 + 子过程收益 + 返回后继续收益”；对玩家顶点，则变成 `min/max` 选择；对概率顶点，则是加权和。

### 语义边界

这个 journal 版也清楚画出了边界：

1. 模型核心仍然是 `1-exit` recursive stochastic game。
2. 奖励必须严格正，这一点不是可有可无的技术细节，而是 family 稳定性的前提。
3. 多出口 reward 版本会重新掉进不可判定。
4. 这里讨论的是 turn-based recursive game，不是 simultaneous `RCSG`。

### 关键性质与判定边界

原文给出的几个最重要的 family 结论可以压成：

$$
\text{positive-reward 1-RMDP exact value} \in P
$$

以及：

$$
\text{positive-reward 1-RSSG quantitative decision} \in NP \cap coNP
$$

策略结构则满足：

$$
\text{both players have optimal deterministic stackless-memoryless strategies}
$$

同时，multi-exit reward `RMDP` 的基本判定问题会变成不可判定。这一点很关键，因为它说明正奖励不是把 family 简单“数值化”，而是重新刻画了一条有明确边界的新子枝。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | recursive components、boxes、entry / exit 完整保留。 |
| 事件 / 触发 | 强支持 | 边的选择与 reward 累积共同驱动演化。 |
| 守卫 / 数据 | 不支持 | 原文核心不是变量。 |
| 层次 | 强支持 | call-return 递归骨架完整。 |
| 并发 / 同步 | 不支持 | 这里是 turn-based。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率、博弈和 rewards 同时存在。 |
| 可执行 / 可验证性 | 强理论支持 | `LFP`、`SM`、strategy improvement、exact value。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| reward tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i,\xi_i)$` | journal 版最完整的模型元组。 |
| `1-RMC` 值语义 | `$x=Ax+b$` | 纯概率特例的线性方程口径。 |
| `1-RSSG` 值语义 | `$x=P(x)$` | 一般双玩家正奖励 family 的 LFP 表达。 |
| 策略结构 | `stackless-memoryless` | family 的强稳定性。 |
| multi-exit 边界 | undecidable | 说明该子枝真正有清晰边界。 |

## 构造方式与承载格式

### 建模入口

1. 先固定 `1-exit` recursive stochastic game 骨架。
2. 给每条转移加正奖励。
3. 给 call port 加正的 call cost。
4. 把目标从 termination probability 换成 total expected reward。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. positive-reward recursive game tuple；
2. `LFP` 方程系统；
3. `SM` 策略与 strategy-improvement；
4. `SCFG/BMDP/BSSG` 等价表述。

### 交换与互操作

它与当前文库中的互操作关系如下：

1. 直接承接 [recursive-stochastic-games-with-positive-rewards/desc.md](../recursive-stochastic-games-with-positive-rewards/desc.md) 的 conference origin。
2. 向上仍属于 [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md) 所代表的 `RMDP/RSSG` 主节点。
3. 与 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 形成“reward 扩展”与“simultaneous-move 扩展”两条平行后继。

## 配套基础设施

- 建模/编辑工具：文中提到 `PReMo` 路线背景，但未在正文给出标准化下载入口。
- 解析/交换/元模型支持：核心是 reward tuple、`x=P(x)` 与 strategy-improvement 语义。
- 仿真/执行支持：可按全局 recursive stochastic game with rewards 语义执行。
- 验证/分析支持：exact reward、`SM` determinacy、`NP \cap coNP` decision、multi-exit undecidability。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，但与 `SCFG/BMDP/BSSG` 的对应使其在不同理论社区之间具有很强的互证价值。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归概率程序 expected running time 分析。
2. 递归 system-environment 对抗中的总成本 / 总收益建模。
3. 需要把 termination-oriented `1-RMDP / 1-RSSG` 扩成 reward-oriented family。

### 需求前提

1. 系统核心是递归调用。
2. 每一步都有严格正的成本 / 奖励。
3. 模型仍是 `1-exit` 且 turn-based。

### 不适用或高成本场景

如果允许 `0` reward、需要 simultaneous moves、或必须保留 multi-exit 返回接口，那么应改用别的 family 或至少另行处理边界。

## 与相邻形式主义的关系

相对 2008 conference 版，这篇 `TCS` 版更完整地稳定了 positive-reward 子枝；相对一般 `RMDP/RSSG`，它新增 total expected reward 目标；相对 `RCSG`，这里没有 simultaneous move；相对 `RMC/HMC`，这里仍然有控制者 / 对手。

## 与本研究的关系

### 对 Project 1 的价值

它可以把 `RMDP/RSSG` 下的 positive-reward 子枝正式写进状态机族演化树，而不只是作为 conference 旁注。

### 作为目标形式主义还是中间表示

更适合作为高表达力理论中间表示和演化树分支，而不是工程建模前端。

### 对需求到模型生成的启发

如果需求文本里已经明确出现“递归流程 + 概率选择 + 期望总成本 / 奖励”，则目标 family 应优先考虑 positive-reward recursive stochastic games，而不是只保留 termination 语义。

## 重要的相关工作

1. [recursive-stochastic-games-with-positive-rewards/desc.md](../recursive-stochastic-games-with-positive-rewards/desc.md)：conference origin。
2. [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)：上游主节点。
3. [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md)：并发 simultaneous-move sibling branch。

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🤝 接口 / 交互契约`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树 `RMDP/RSSG` 节点下，作为 `positive-reward 1-RMDP / 1-RSSG` 子枝的 journal full-version 代表条目，并把这一子枝的年份稳定成 `2008 / 2019`。
