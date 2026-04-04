# 递归博弈图的模块化策略 / Modular Strategies for Recursive Game Graphs

## 基本信息

- 标题：Modular Strategies for Recursive Game Graphs
- 中文标题：递归博弈图的模块化策略
- 作者：Rajeev Alur, Salvatore La Torre, P. Madhusudan
- 发表：*Theoretical Computer Science*, 354(2):230-249, 2006
- DOI：`10.1016/j.tcs.2005.11.017`
- 链接：https://madhu.cs.illinois.edu/tcs06-tacas03.pdf
- 形式主义：`Recursive Game Graphs (RGG)`，以及其上的 modular strategies
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / game semantics
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 recursive game graph tuple、global game graph、modular strategy tuple 与 call-graph fixed-point algorithm。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 game modules、player partition、global stack semantics 与 modular-strategy winning condition。

## 简报

这篇论文把 `RSM` 明确推进到 game / controller-synthesis 方向：节点不再只是“系统怎么跑”，还要区分由 player 0 还是 player 1 决策。更关键的是，作者拒绝直接沿用 pushdown games 里“全局历史可见”的策略，而是提出 `modular strategy`，要求每个模块只能依据当前调用中的局部历史做决策。于是 `RGG` 补出的不是一般游戏图，而是“递归状态机 + 局部可组合控制器”这条非常适合挂在演化树上的分支。

- 形式主义定位：`RSM` 的博弈语义扩展，用递归模块上的双人博弈表达 controller synthesis / open-system winning condition。
- 构造方式简述：模型仍由 modules、nodes、boxes、entry / exit 组成，但每个 node / box 再额外归属给某一方玩家；全局运行就是 stack-based recursive game。
- 基础设施与场景简述：纯理论条目，但正式定义了 recursive game graph、global game graph、modular strategy 与 `NP`-complete reachability / safety 游戏。

```text
recursive control modules -> player partition + call/return recursion -> global game graph -> modular strategies -> recursive controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

原文从普通 reachability / safety games 出发，但把“flat graph”替换成由多个可递归调用模块构成的游戏图。模型的关键增强不是再加一种逻辑，而是把“局部模块控制器”固定成一等公民。

### 核心抽象

原文把 `RGG` 写成：

$$
A = \langle A_1,\ldots,A_n \rangle
$$

其中每个 game module 可整理为：

$$
A_i = (N_i,B_i,V_i^0,V_i^1,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通 nodes 集合。
2. `B_i` 是 boxes 集合。
3. `V_i^0` 与 `V_i^1` 把 nodes 与 boxes 划给 player 0 与 player 1。
4. `Y_i : B_i \to \{1,\ldots,n\}` 指定每个 box 调用哪个模块。
5. `En_i` 与 `Ex_i` 是 entry / exit nodes。
6. `\delta_i` 是从 nodes / returns 到 nodes / calls 的局部转移函数。

### 一个最小例子与通俗解释

可以把它理解成“递归子程序里还有对手或环境在出牌”的模型：

1. 某个模块 `A_1` 里，player 1 在入口节点决定走哪条调用边。
2. 进入下层模块后，player 0 只能依据这个模块内当前调用的局部历史做选择。
3. 若控制器在每次进入同一模块时都能用同一套局部规则保证到达目标出口，就形成 modular winning strategy。

通俗地说，`RGG` 像“每个模块都要能单独装一个可复用控制器的递归状态机博弈”。这比普通 pushdown game 更贴近“模块化接口 / 控制器合成”的直觉。

### 运行 / 接受 / 转移语义

原文把全局状态写成：

$$
\langle \beta,u \rangle
$$

上式中的符号逐项解释如下：

1. `\beta = b_1,\ldots,b_r` 是当前调用栈上的 boxes。
2. `u` 是当前普通 node。
3. 状态同时带有 player 归属，用来决定轮到谁选下一步。

与普通 `RSM` 一样，三类核心全局迁移分别是：

1. internal move；
2. call a module；
3. return from a call。

论文真正新增的是 modular strategy。它写成：

$$
\hat f = \{f_i\}_{i=1}^n
$$

其中每个 `f_i` 只依赖当前模块调用中的 local memory，而不能读取全局历史。也就是说，一个模块的控制策略必须能在任意调用上下文中复用。

### 语义边界

`RGG` 的边界有三点特别重要：

1. 它继承了 `RSM` 的 recursion，但把控制选择显式划分为双人博弈。
2. 它不使用全局 pushdown game 的全历史策略，而要求 modular local strategies。
3. 一旦把 local memory 放宽成 persistent local memory，reachability 会变成不可判定。

### 关键性质与判定边界

原文首先给出 reachability 的核心结论：

$$
\mathrm{Reachability}(\mathrm{RGG},\mathrm{modular}) \text{ is NP-complete}
$$

这和全局 pushdown games 的 `EXPTIME` 对比非常关键，因为它说明“限制策略必须模块化”并不是削弱表达无意义，反而更贴近模块化控制，同时把复杂度降到了 `NP`。

对 safety，论文也给出：

$$
\mathrm{Safety}(\mathrm{RGG},\mathrm{modular}) \text{ is NP-complete}
$$

而若允许 persistent local memory，则 reachability 变成 undecidable。这个边界正好说明 modularity 在理论上扮演的是“可组合性 + 可判定性”的双重角色。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modules、nodes、boxes、entry / exit。 |
| 事件 / 触发 | 强支持 | graph moves + call / return。 |
| 守卫 / 数据 | 不支持 | 核心不在数据。 |
| 层次 | 强支持 | 递归模块层次。 |
| 并发 / 同步 | 不支持 | 本文是 sequential game。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散双人博弈。 |
| 可执行 / 可验证性 | 强理论支持 | reachability / safety + modular strategy synthesis。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$A=\langle A_1,\ldots,A_n\rangle$` | recursive game graph 总体定义。 |
| 模块元组 | `$A_i=(N_i,B_i,V_i^0,V_i^1,Y_i,En_i,Ex_i,\delta_i)$` | 单个游戏模块的骨架。 |
| 全局状态 | `$\langle \beta,u\rangle$` | 调用栈 + 当前控制点。 |
| 模块化策略 | `$\hat f=\{f_i\}_{i=1}^n$` | 每个模块各自一套局部策略。 |
| reach / safety | `$\mathrm{NP}$-complete` | modular games 的主结论。 |

## 构造方式与承载格式

### 建模入口

1. 先按 `RSM` 的方式定义递归模块。
2. 再把每个 node / box 分配给 player 0 或 player 1。
3. 指定目标出口集合或 good-state 集合。
4. 最后约束策略必须是 modular local strategies。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. game-module tuple；
2. global game graph；
3. local-memory projection；
4. modular call-graph fixed-point algorithm。

### 交换与互操作

它与当前文库里的关系很清楚：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向旁边连接 open systems、interface synthesis 与 module checking 话题。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 game-module tuple、player partition 与 modular strategy semantics。
- 仿真/执行支持：可按 global game graph 展开。
- 验证/分析支持：modular reachability / safety games 与 fixed-point solution。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值是为模块化控制器合成提供 formal node。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归控制流上的 controller synthesis / open-system winning analysis。
2. 希望模块局部控制策略可复用的递归系统。
3. 需要把 `RSM` 支线继续接到博弈 / synthesis 方向。

### 需求前提

1. 环境 / 控制器交互可写成双人博弈。
2. 决策应只依赖当前模块调用中的局部历史。
3. 系统仍以 sequential recursive control 为主。

### 不适用或高成本场景

如果问题本质不是“局部模块控制能否保证赢”，而是需要全局历史或一般并发博弈，这个 family 就不再合适。

## 与相邻形式主义的关系

相对 `RSM`，`RGG` 增加了 player partition 与 winning condition；相对普通 pushdown games，它额外要求 modular strategies；相对 [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md) 的 open hierarchical modules，它更偏 closed recursive controller game，而不是 environment pruning semantics。

## 与本研究的关系

### 对 Project 1 的价值

它让层次状态机理论线不只停在“能建模什么”，还自然延伸到“局部模块控制器能否合成、能否组合”这一层，这对后续生成-验证-修复闭环尤其有启发。

### 作为目标形式主义还是中间表示

更适合作为验证 / 合成阶段的理论中间表示，而不是直接的需求建模前端。

### 对需求到模型生成的启发

当需求里出现“每个子模块都必须在任何调用上下文中独立保证某个目标”这类约束时，plain `RSM` 不够，需要考虑 `RGG` 这种带 modular strategy 语义的 family。

### 现实限制

它没有工程标准，也不面向直接执行，价值主要在 formal synthesis / module-game reasoning。

## 重要的相关工作

### 奠基或前身工作

- [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)

### 同类型或同家族工作

- [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)
- [verification-of-well-formed-communicating-recursive-state-machines/desc.md](../verification-of-well-formed-communicating-recursive-state-machines/desc.md)

## 文献分类总结

- 这篇论文把 `RSM` 明确推进成模块化 recursive games family。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL 或应用案例。
- 在当前演化树里，它最适合挂在 `RSM` 之下，作为“game / controller-synthesis”子枝的代表节点。
