# 带模块化策略的 CaRet 博弈求胜 / Winning CaRet Games with Modular Strategies

## 基本信息

- 标题：Winning CaRet Games with Modular Strategies
- 中文标题：带模块化策略的 CaRet 博弈求胜
- 作者：Ilaria De Crescenzo、Salvatore La Torre
- 发表：*Proceedings of the 26th Italian Conference on Computational Logic (CILC 2011)*, CEUR Workshop Proceedings 810, pp. 327-331, 2011
- DOI：原文未提供
- 链接：https://ceur-ws.org/Vol-810/paper-s01.pdf
- 形式主义：`Modular CaRet Games`，即带 `CaRet` 胜利条件的 `Recursive Game Graphs (RGG)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`RGG` 胜利条件扩展 / context-sensitive temporal-game branch
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `RGG`、modular strategy、`CaRet` 公式与后续 parity-tree-automaton reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 `RGG` + modular strategy + `CaRet` 公式对 `\langle G,\varphi \rangle`。

## 简报

这篇短文做的不是一般的“在 `RGG` 上再跑一个逻辑算法”，而是把 `RGG` 的 winning-condition family 往 stack-sensitive temporal logic 方向稳定推进了一步：从 reachability / `LTL` modular games，推进到 `CaRet` modular games。对当前演化树来说，它的价值在于给 `RGG` 补出一个明确可命名的胜利条件子枝，而不是让 `RGG` 只停在普通 modular strategies 上。

- 形式主义定位：`RGG` 的 context-sensitive temporal winning-condition extension。
- 构造方式简述：底层仍是 `RGG` 与 modular strategy；新增的是胜利条件不再是 ordinary `\omega`-regular formula，而是显式区分 global / abstract / caller successors 的 `CaRet`。
- 基础设施与场景简述：论文没有工程工具，但把 `CaRet -> parity game / tree automaton` 这条 reduction 写成了稳定 family，可以作为 `RGG` 在 stack-sensitive specification 方向的经典旁枝。

```text
RGG -> modular strategy -> CaRet winning condition -> parity game / tree automaton reduction -> modular controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文沿用既有 `RGG` 骨架，只在其上加一类新的 modular winning condition。核心对象不是 plain `RGG`，而是：

1. 一个 recursive game graph `G`；
2. 一条 modular strategy；
3. 一个 `CaRet` 公式 `\varphi`；
4. 二者组成的 modular CaRet game。

### 核心抽象

文中把对象写成：

$$
\mathcal G = \langle G,\varphi \rangle
$$

上式中的符号逐项解释如下：

1. `G` 是一个 recursive game graph。
2. `\varphi` 是 `CaRet` 公式。
3. `\mathcal G` 因而表示“在 `RGG` 上以 `CaRet` 为 winning condition 的 modular game”。

由于 modular strategy 是该 family 的核心限制，论文还明确强调：

$$
f = \{f_m\}_{m \in M}
$$

这里：

1. `M` 是游戏模块集合。
2. 每个 `f_m` 只允许依赖当前模块激活的 local memory。
3. 每次重新进入某个模块时，局部记忆都会被重置。

### 一个最小例子与通俗解释

论文给出的典型说明是 pre / post-condition 风格的 `CaRet` 公式：

$$
\Box[(call \land p \land p_A) \rightarrow \bigcirc_a q]
$$

上式中的符号逐项解释如下：

1. `call` 表示当前位置是一次调用。
2. `p_A` 表示这次调用属于过程 `A`。
3. `p` 是调用前条件。
4. `\bigcirc_a` 是 `CaRet` 的 abstract-next，也就是“跳到这次调用对应的 matching return”。
5. `q` 是返回后的后置条件。

通俗地说，这个 family 表达的是：玩家不只是要“最终赢”或“满足某个普通时序性质”，而是要在每次模块调用和返回的嵌套上下文里，都保证某个 stack-sensitive 合约成立。

### 运行 / 接受 / 转移语义

文中的 winning 语义可以保守整理为：

$$
\forall p \in \mathrm{Plays}(G,f),\ p \models \varphi
$$

上式中的符号逐项解释如下：

1. `f` 是 protagonist 的 modular strategy。
2. `\mathrm{Plays}(G,f)` 是所有遵循该策略的 play。
3. `p \models \varphi` 表示该 play 满足 `CaRet` 公式。
4. 也就是说，策略必须在所有环境行为下都保证 `\varphi`。

原文进一步说明，`CaRet` 的三类 successor 是这个 family 的关键：

1. global successor：普通下一步；
2. abstract successor：若当前为 call，则跳到 matching return；
3. caller successor：沿调用栈回看最近未匹配调用。

### 语义边界

这篇论文把边界讲得很明确：

1. 它仍然基于 `RGG`，不是新的底层递归控制流图语法。
2. 新增的是 winning condition 的 stack-sensitive 逻辑层。
3. 策略仍被限制为 modular；一旦改成更强记忆模型，就不是本文 family。
4. 这条线比 ordinary `LTL` modular games 更强，因为 `CaRet` 可以直接谈 matching returns。

### 关键性质与判定边界

论文的主结论可压成：

$$
\mathrm{Win}_{mod}(\langle G,\varphi\rangle)\ \text{is}\ 2\mathrm{EXPTIME}\text{-complete}
$$

上式中的符号逐项解释如下：

1. `\mathrm{Win}_{mod}` 表示“是否存在 winning modular strategy”的判定问题。
2. `G` 是一个 `RGG`。
3. `\varphi` 是 `CaRet` 公式。
4. 结论说明把 modular games 的 winning condition 升级到 `CaRet` 后，复杂度达到 `2EXPTIME`。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 底层仍是 `RGG` 的 module / node / box / call / return。 |
| 事件 / 触发 | 强支持 | play 由节点选择与 module call / return 构成。 |
| 守卫 / 数据 | 不支持 | 重点不在有限变量。 |
| 层次 | 强支持 | 调用栈与模块层次是语义核心。 |
| 并发 / 同步 | 不支持 | 目标是 sequential recursive games。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 无概率或连续动力学。 |
| 可执行 / 可验证性 | 强理论支持 | `CaRet -> parity -> tree automata` 的判定链路完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| modular CaRet game | `$\mathcal G=\langle G,\varphi\rangle$` | family 的基本对象。 |
| modular strategy | `$f=\{f_m\}_{m\in M}$` | 每个模块各自一套局部策略。 |
| abstract post-condition | `$\Box[(call \land p \land p_A)\rightarrow \bigcirc_a q]$` | `CaRet` 能直接说 matching return 上的后置条件。 |
| winning requirement | `$\forall p\in\mathrm{Plays}(G,f),\ p\models\varphi$` | 策略必须对所有环境行为都成立。 |
| 复杂度 | `$2\mathrm{EXPTIME}$-complete` | `RGG` 的 stack-sensitive logic branch 的主边界。 |

## 构造方式与承载格式

### 建模入口

1. 先用 `RGG` 描述递归开放系统。
2. 再选择 protagonist / environment 的节点划分。
3. 用 `CaRet` 指定 stack-sensitive winning condition。
4. 最后求是否存在 winning modular strategy。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. `RGG`；
2. modular strategy family；
3. `CaRet` 公式；
4. parity / tree automaton reduction。

### 交换与互操作

它与当前文库的关系如下：

1. 向上承接 [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md) 的 `RGG` 主枝。
2. 向旁边衔接 [visibly-pushdown-modular-games/desc.md](../visibly-pushdown-modular-games/desc.md) 的 automaton-spec extension。
3. 与 `CaRet` 这类 nested-call / return temporal logic 条目形成自然桥接。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `RGG`、modular strategy 与 `CaRet` formula。
- 仿真/执行支持：可按 `RGG` play semantics 理解执行。
- 验证/分析支持：经 parity-winning condition、alternating parity tree automata 与 emptiness 检查求解。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要服务于 modular controller synthesis。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归开放系统上的控制器合成。
2. 需要显式说明 pre / post-condition、caller-sensitive 约束的 modular games。
3. 想把 `RGG` 从 `LTL` / reachability 再推进到 stack-sensitive winning conditions 的场景。

### 需求前提

1. 系统与环境可写成两人递归博弈。
2. 控制器必须是 modular 的，即只能依赖当前模块激活的局部历史。
3. 规格真正依赖 call / return 匹配，而不是 plain linear-time 条件。

### 不适用或高成本场景

如果 winning condition 只需 ordinary reachability / safety，沿用已有 `RGG` 结果更轻；若要用 automaton 而不是逻辑给规格编码，则更适合 [visibly-pushdown-modular-games/desc.md](../visibly-pushdown-modular-games/desc.md)。

## 与相邻形式主义的关系

相对普通 `RGG`，本文新增的是 `CaRet`-based winning conditions；相对 `LTL` modular games，它更强，因为可以直接谈 abstract / caller successors；相对 `VPMG`，它是逻辑规格版本，而后者是 visibly pushdown automaton 规格版本。

## 与本研究的关系

### 对 Project 1 的价值

它让当前演化树中 `RSM -> RGG` 这一分支不再只停留在“modular strategy semantics”，而是继续长出“stack-sensitive temporal winning conditions”这类稳定可命名旁枝。

### 作为目标形式主义还是中间表示

更适合作为验证 / 合成阶段的中间表示，而不是需求建模前端。

### 对需求到模型生成的启发

当需求不是单纯“模块能否到达某出口”，而是“调用 A 时若满足前置条件，则在 matching return 上必须满足后置条件”时，plain `RGG` 还不够，需要这类 `CaRet`-sensitive modular-game family。

## 重要的相关工作

1. [modular-strategies-for-infinite-games-on-recursive-graphs/desc.md](../modular-strategies-for-infinite-games-on-recursive-graphs/desc.md)：`RGG` 的 conference origin。
2. [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)：`RGG` 的 journal full version。
3. [visibly-pushdown-modular-games/desc.md](../visibly-pushdown-modular-games/desc.md)：把 winning conditions 从 `CaRet` 逻辑再转到 visibly pushdown automata family。

## 文献分类总结

- 本文不改变 `RGG` 的底层 graph grammar，但它确实给 `RGG` 长出了一条新的稳定胜利条件分支。
- 因而在当前文库里，最合适的挂接方式不是把它当成纯算法论文，而是把它当作 `RGG` 的 `CaRet` specification-sensitive sibling。
- 若后续树结构需要继续压缩，可把它与 `VPMG` 并列收在 `RGG` 下的 “modular winning-condition extensions” 小簇中。
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
