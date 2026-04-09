# 递归图上无限博弈的模块化策略 / Modular Strategies for Infinite Games on Recursive Graphs

## 基本信息

- 标题：Modular Strategies for Infinite Games on Recursive Graphs
- 中文标题：递归图上无限博弈的模块化策略
- 作者：Rajeev Alur, Salvatore La Torre, P. Madhusudan
- 发表：*Computer Aided Verification*, pp. 67-79, 2003
- DOI：`10.1007/978-3-540-45069-6_6`
- 链接：http://dx.doi.org/10.1007/978-3-540-45069-6_6
- 形式主义：`Recursive Game Graphs (RGG)`，即带 modular strategy 语义的递归博弈图
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / conference origin of `RGG`
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `RGG` tuple、global states、module-local histories 与 strategy tree automata construction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 game modules、player partition、call/return stack semantics 与 modular strategy functions。

## 简报

这篇 `CAV 2003` 论文是当前树上 `RGG` 节点的原始 conference 起点。它不是把 `RSM` 简单改成 pushdown game，而是额外固定了 modular strategy 语义，要求每个模块里的决策只能依赖当前调用中的局部历史，而不能偷看整个全局栈上下文。对层次状态机支线来说，这意味着 `RSM` 不只是能接到 pushdown-style verification，还能长出“局部可复用控制器”的 open-system / synthesis 支线。

- 形式主义定位：`RSM` 的 game-theoretic 扩展，也是 `RGG` 节点第一次以 `\omega`-regular / `LTL` 规格形式被明确立起来的来源。
- 构造方式简述：模型仍由 modules、nodes、boxes、entries 和 exits 组成，但每个 node/box 再划给某个玩家，运行是 stack-based recursive play。
- 基础设施与场景简述：纯理论条目，但已经给出 strategy trees、two-way alternating tree automata 与 `LTL` synthesis 路线。

```text
recursive modules -> player partition + call/return recursion -> local-history modular strategies -> tree-automata acceptance -> omega-regular / LTL synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文关注的是“递归模块上的无限持续博弈”。相比普通 `RSM`，它不再只问 reachability 或 model checking，而是问：在存在环境对手的情况下，模块内部能否依靠局部策略反复赢下去。

### 核心抽象

原文把一个 `RGG` 写成：

$$
A=(M,m_{in},\{A_m\}_{m\in M})
$$

其中每个 game module 为：

$$
A_m=(N_m,B_m,Y_m,En_m,Ex_m,P^0_m,P^1_m,\delta_m,\eta_m)
$$

上式中的符号逐项解释如下：

1. `M` 是模块名集合，`m_{in}` 是初始模块。
2. `N_m` 是节点集合，`B_m` 是 boxes 集合。
3. `Y_m:B_m\to M` 指定某个 box 调用哪个模块。
4. `En_m` 与 `Ex_m` 分别是 entry / exit 节点集合。
5. `P^0_m` 与 `P^1_m` 把节点/boxes 划给 player 0 和 player 1。
6. `\delta_m` 是从 nodes / returns 到 nodes / calls 的转移函数。
7. `\eta_m` 给节点分配观测字母。

### 一个最小例子与通俗解释

可以把它想成“递归服务模块上的控制器与环境博弈”：

1. 顶层模块处理一个请求。
2. 某个 box 会递归调用子模块处理子请求。
3. player 0 控制本模块内自己的决策点，player 1 控制环境分支。
4. modular strategy 要求：每次进入同一个模块时，只能靠当前这次调用里看见的局部历史决策。

通俗地说，`RGG` 是“要求模块级策略可复用的递归状态机博弈版”。它比一般 pushdown games 更贴近组件接口和 open-system 直觉。

### 运行 / 接受 / 转移语义

原文把全局状态写成：

$$
(\gamma,u)\in B^* \times N
$$

上式中的符号逐项解释如下：

1. `\gamma` 是 boxes 组成的调用栈。
2. `u` 是当前最内层模块中的节点。
3. `B^*` 表示递归调用上下文。
4. `N` 是所有模块节点的并集。

而 modular strategy 则是按模块分解的一组函数：

$$
f=\{f_m\}_{m\in M}
$$

其中每个 `f_m` 只依赖当前模块调用的 local history，而不是整个全局历史。

### 语义边界

这个 family 的边界如下：

1. 它仍是离散递归 family，不带时间或概率。
2. 它的增强点在双人博弈和 modular strategy，而不是新数据域。
3. 它强调 local-history 可复用，因此不同于 standard pushdown games 的 global strategy。
4. 它天然更偏 open systems / synthesis，而不是 closed verification。

### 关键性质与判定边界

论文首先给出 deterministic Buchi / universal co-Buchi 规格下的复杂度：

$$
\mathrm{Decide}(RGG,\text{modular Buchi}) \text{ is } \mathrm{Exptime}\text{-complete}
$$

对固定规格，复杂度降到：

$$
\mathrm{NP}\text{-complete}
$$

对 `LTL` 规格，文中得到：

$$
\mathrm{Decide}(RGG,LTL)=2\mathrm{Exptime}\text{-complete}
$$

这些结论的重要性在于：`RGG` 节点从一开始就不是只会做 reachability / safety，它在 conference 起点上就已经被放进了 `\omega`-regular / `LTL` 合成语义里。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modules、nodes、boxes、entries/exits。 |
| 事件 / 触发 | 强支持 | 观测字母与节点转移共同决定博弈演化。 |
| 守卫 / 数据 | 不支持 | 核心不在变量或赋值。 |
| 层次 | 强支持 | boxes 与 recursive calls 构成 hierarchy。 |
| 并发 / 同步 | 不支持 | 仍是 sequential recursive game。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | modular strategies、tree automata、`LTL` synthesis。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$A=(M,m_{in},\{A_m\}_{m\in M})$` | `RGG` 顶层骨架。 |
| 模块元组 | `$A_m=(N_m,B_m,Y_m,En_m,Ex_m,P^0_m,P^1_m,\delta_m,\eta_m)$` | 单个递归博弈模块。 |
| 全局状态 | `$(\gamma,u)\in B^*\times N$` | 调用栈 + 当前节点。 |
| 模块化策略 | `$f=\{f_m\}_{m\in M}$` | 每个模块单独持有局部策略。 |
| 复杂度 | `Buchi: Exptime`, `fixed spec: NP`, `LTL: 2Exptime` | `RGG` 的经典判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先按过程/组件边界定义 modules。
2. 给每个模块标出 nodes、boxes、entries 和 exits。
3. 再把节点/boxes 分到 player 0 与 player 1。
4. 最后给节点贴上观测字母，用来与 `\omega`-regular 规格联动。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RGG` tuple；
2. stack-based global states；
3. local-history based modular strategies；
4. strategy trees；
5. two-way alternating tree automata。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 与 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM` 母线。
2. 与 [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md) 组成 `RGG` 的 conference / journal 双条目。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive game graph tuple 与 strategy tree encoding。
- 仿真/执行支持：可按 stack-based global game semantics 直接解释。
- 验证/分析支持：deterministic/universal Buchi、co-Buchi 与 `LTL` modular synthesis。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要连接 open systems、controller synthesis 与 recursive-game semantics。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归模块化控制器的对抗式合成。
2. 需要“同一模块策略能在不同上下文复用”的 open systems。
3. 想把 `RSM` 支线继续长到 `\omega`-regular / `LTL` winning condition。

### 需求前提

1. 交互必须能抽成双人博弈，而不是一般概率环境。
2. 策略必须以模块为单位可复用。
3. 系统核心复杂度来自递归调用，而不是并发或时钟。

### 不适用或高成本场景

如果只关心 closed-system reachability，则 `RSM` 足够；如果需要 fork-join 并发递归，应转向 `CRSM`；如果需要 system/environment pruning 而非双人对抗，可转向 open hierarchical modules 或 pushdown module checking。

## 与相邻形式主义的关系

相对 `RSM`，它引入 player partition 与 modular strategies；相对一般 pushdown games，它限制策略只能看当前模块局部历史；相对 [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)，它是博弈式 open semantics，而不是 environment pruning 的 branching-time module checking。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机理论树里，`RSM` 不只是 verification 终点，还会自然长出 synthesis / open-system 分支。这对后续考虑“需求到交互式控制逻辑”的自动建模非常关键。

### 对状态机自动建模的启发

如果需求中同时出现“递归过程结构”和“系统/环境对抗或博弈约束”，那目标模型就不应被压回 plain `RSM`，而应直接考虑 `RGG` 这类 family。

## 重要的相关工作

1. [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)：`RGG` 的 journal 版整理条目。
2. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：提供 `RGG` 所依附的 `RSM` 基底。
3. `module checking` 与 `interface automata`：文中把它们当作 modular open-system motivation，而不是直接蓝本。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🧩 经典离散状态机`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🤝 接口 / 交互契约`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> RGG` 位置，并作为 `RGG (2003 / 2006)` 里 `2003` 这一侧的原始 conference 锚点。
