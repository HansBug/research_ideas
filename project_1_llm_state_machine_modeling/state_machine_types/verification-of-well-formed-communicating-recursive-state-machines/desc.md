# 良构通信递归状态机的验证 / Verification of Well-Formed Communicating Recursive State Machines

## 基本信息

- 标题：Verification of Well-Formed Communicating Recursive State Machines
- 中文标题：良构通信递归状态机的验证
- 作者：Laura Bozzelli, Salvatore La Torre, Adriano Peron
- 发表：*Verification, Model Checking, and Abstract Interpretation*, pp. 412-426, 2006
- DOI：`10.1007/11609773_27`
- 链接：https://cliplab.org/~lbozzelli/VMCAI06b.pdf
- 形式主义：`Well-Formed Communicating Recursive State Machines (CRSM / WF-CRSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / recursion + fork-join communication
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 module tuple、fork / join calls、tree-shaped global state、`ConCaRet` 与 Buchi-CRSM emptiness reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 modules、parallel-call boxes、synchronization alphabet、tree-state semantics 与 local-successor logic。

## 简报

这篇论文把 `RSM` 再往前推一步：不再只允许单线程递归调用，而是允许某个状态通过一次 fork 同时激活多个子模块，并在它们都结束后 join 回来。关键是作者没有把模型做成一般并发递归系统，而是刻意加上“同一 fork 内才能通信、调用者在 fork 期间挂起”的 well-formed 限制，从而保住 decidability。对当前演化树来说，它补出的不是另一条 UML / DSL 线，而是 `RSM` 下面“fork-join 并发递归”这一条 classic automata-theory 支线。

- 形式主义定位：`RSM` 的受限并发扩展，用 fork-join 递归模块替代普通单调用 box。
- 构造方式简述：状态既可以普通前进，也可以通过一个 box 同时调用若干模块实例；这些实例并行运行，在同步退出后再回到调用模块。
- 基础设施与场景简述：纯理论条目，但给出了 tree-shaped global semantics、`ConCaRet`、Buchi-CRSM 与 emptiness / model-checking route。

```text
recursive module -> parallel-call box -> forked module instances + join return -> tree-shaped global state -> ConCaRet / emptiness checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 `CRSM` 明确定义成“well-formed recursive concurrent programs”的抽象模型。与一般 PRS / DPN 不同，它只允许 fork-join 式并发，不允许无限自由的 spawn，因此既能表达并发递归，又不会直接落到 Turing-powerful 无判定边界的一般情形。

### 核心抽象

原文把 `CRSM` 写成：

$$
S = \langle (S_1,\ldots,S_k), start \rangle
$$

其中每个 module 可整理为：

$$
S_i = \langle \Sigma_i,\Sigma_i^s,N_i,B_i,Y_i,En_i,Ex_i,\delta_i,\eta_i \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma_i` 是 module 的动作字母表。
2. `\Sigma_i^s \subseteq \Sigma_i` 是同步符号集合。
3. `N_i` 是 nodes 集合。
4. `B_i` 是 boxes 集合。
5. `Y_i : B_i \to \{1,\ldots,k\}^+` 把一个 box 映射到一串被同时激活的 modules。
6. `En_i` 与 `Ex_i` 分别是 entry / exit nodes。
7. `\delta_i` 是从 nodes 或 returns 指向 nodes 或 calls 的转移函数。
8. `\eta_i` 是命题标签函数。

原文进一步定义：

$$
Calls_i = \{(b,e_1,\ldots,e_m)\}
$$

和

$$
Retns_i = \{(b,x_1,\ldots,x_m)\}
$$

分别表示对一个 box 的并发调用入口和同步返回出口。

### 一个最小例子与通俗解释

一个最小例子可以是“父模块把两个工人任务同时发下去，等两个都完成再继续”：

1. 父模块在某个 node 进入 box `b`。
2. `b` 同时激活两个子模块实例，它们各自从给定 entry 开始。
3. 若同步符号 `\sigma` 出现，则同一 fork 内所有相关实例必须一起走 `\sigma`。
4. 只有当这批实例都到达各自 exit 后，父模块才能 join 回来继续。

通俗地说，`CRSM` 像“会把一层任务拆给若干子流程并行执行、但要整批收回”的递归状态机。它比 `RSM` 多了 fork-join 并发，但又比一般并发递归模型更克制。

### 运行 / 接受 / 转移语义

原文把全局状态建成一棵有限树：

$$
q = (t,D)
$$

上式中的符号逐项解释如下：

1. `t` 是前缀闭合的有限树，表示当前 activation hierarchy。
2. `D : t \to B \cup V` 给每个树位置标上 box 或 vertex。
3. 叶子对应当前活跃的模块实例。
4. 从根到叶的路径对应该实例的局部调用栈。

四类全局转移分别是：

1. 单模块 internal move；
2. 同步 internal move；
3. module call；
4. return from a call。

其中最关键的 fork / join 可写成：

$$
(t,D) \xrightarrow{call} (t',D')
$$

与

$$
(t,D) \xrightarrow{return} (t'',D'')
$$

第一类把一个 leaf 展开成多个子叶，第二类在所有子叶退出后把它们收缩回父位置。

### 语义边界

这个模型的边界很明确：

1. 它允许递归与并发，但并发必须是 fork-join 式。
2. 通信只允许在同一 fork 中激活、且当前没有继续调用别的模块实例之间发生。
3. 它不允许自由 spawn，因此明显弱于一般 PRS。
4. 当 `rank(S)=1` 时，它退化成普通 `RSM`。

### 关键性质与判定边界

原文首先强调：

$$
\mathrm{rank}(S)=1 \Rightarrow S \text{ is an RSM}
$$

说明 `CRSM` 是 `RSM` 的真扩展，而不是另一套无关 family。

在验证层面，论文引入 `ConCaRet` 与 Buchi-CRSM，并给出：

$$
\mathrm{MC}_{ConCaRet}(\mathrm{CRSM}) \text{ is EXPTIME-complete}
$$

原文还指出这种复杂度与 `CaRet` on `RSM` 的已知下界一致，说明 well-formed fork-join 并发虽然增强了模型，但没有把问题直接推向不可判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modules、nodes、boxes、fork / join returns。 |
| 事件 / 触发 | 强支持 | 普通动作与同步动作并存。 |
| 守卫 / 数据 | 弱支持 | 原文主要关注有限域控制流，不把数据作为主体。 |
| 层次 | 强支持 | 递归模块层次。 |
| 并发 / 同步 | 强支持 | fork-join 并发与同 fork 同步。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `ConCaRet`、Buchi-CRSM、emptiness。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$S=\langle (S_1,\ldots,S_k),start\rangle$` | `CRSM` 总体定义。 |
| 模块元组 | `$S_i=\langle \Sigma_i,\Sigma_i^s,N_i,B_i,Y_i,En_i,Ex_i,\delta_i,\eta_i\rangle$` | 单个模块的结构骨架。 |
| 并发调用 | `$Y_i:B_i\to\{1,\ldots,k\}^+$` | 一个 box 可同时激活多个模块。 |
| 全局状态 | `$q=(t,D)$` | 用树表示 activation hierarchy。 |
| 复杂度 | `$\mathrm{MC}_{ConCaRet}(\mathrm{CRSM})$ is `EXPTIME`-complete | 该支线的主要判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义若干 finite-state modules。
2. 再决定哪些 box 表示单个递归调用，哪些 box 表示并发 fork。
3. 为每个 fork box 指定被同时激活的 module 序列。
4. 最后为需要同步的动作放入 `\Sigma^s`。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. module tuple；
2. call / return tuples；
3. tree-shaped global state；
4. `ConCaRet` 与 Buchi-CRSM product route。

### 交换与互操作

它与当前文库中的邻近 family 关系非常直接：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 与 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 的 `RSM`。
2. 向旁边吸收 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md) 的“并发 / communication”主题。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 module tuple、fork / join return tuple 与 tree semantics。
- 仿真/执行支持：可直接按 labeled transition system over trees 执行。
- 验证/分析支持：`ConCaRet`、Buchi-CRSM emptiness、`EXPTIME` model checking。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型理论路线，主要与 PRS / DPN / CaRet literature 对话。

## 适用场景与需求前提

### 适用场景

适合：

1. fork-join 形式的并发递归控制流。
2. 需要局部同步但又想保住 decidability 的 recursive concurrent programs。
3. 想在 `RSM` 支线上继续补“受限并发”这根理论枝。

### 需求前提

1. 并发结构能抽成同步 fork-join。
2. 通信只发生在同一 fork 内、且不穿透更深调用层。
3. 系统仍可用有限域模块状态表示。

### 不适用或高成本场景

如果系统需要自由 spawn、异步共享内存或跨 fork 任意同步，这个 well-formed family 就不够了，问题也往往会掉出可判定区。

## 与相邻形式主义的关系

相对 `RSM`，`CRSM` 增加了受限并发与 join；相对 `CHSM`，它把“并发 + hierarchy”进一步推进到 recursive call stack；相对一般 PRS / DPN，它更弱，但正因为这种收束才保住 decidability。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机理论线并不只有 sequential `RSM`，还存在一条克制的“并发递归”分支，可用来承接需求里那些明确带有 fork-join 结构的控制逻辑。

### 作为目标形式主义还是中间表示

更适合作为理论型中间表示和族谱节点，而不是工业建模前端。

### 对需求到模型生成的启发

如果需求文本里已出现“同时派发多个子任务，等全部完成后继续”的结构，plain `RSM` 不再够用，而 `CRSM` 这类 fork-join recursive family 是更自然的理论目标。

### 现实限制

它没有工程生态，逻辑与语义也明显偏理论，不适合直接成为实际交付语言。

## 重要的相关工作

### 奠基或前身工作

- [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)

### 同类型或同家族工作

- [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)
- [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)

## 文献分类总结

- 这篇论文把 `RSM` 扩成了 well-formed fork-join communication family。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、工具或应用案例。
- 在当前演化树里，它适合作为 `RSM` 下“受限并发递归”子枝的代表条目，并与 `CHSM` 共同补出 hierarchy + communication 的另一种推进方式。
